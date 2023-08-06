import graphlib
import io
import logging
import zipfile
from django.apps.registry import apps
from django.db.models import ManyToOneRel
from io import TextIOWrapper, BufferedReader
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

from ..errors import ModelClassNotRegistered
from ..policy import DISCARD_OBJECT, ImportPolicy, RelinkAction
from ..types import ID, Ref, ObjectData, Attachment

from .base import BaseContainer
from ._yaml import get_yaml


logger = logging.getLogger('haul.import')
logger.setLevel(logging.DEBUG)


class ImportContainer(BaseContainer):
    __instance_map: Dict[ID, Any]
    __discarded_objects: Set[ID]
    metadata: Any = None

    def __init__(
        self,
        policy: Optional[ImportPolicy] = None,
        ignore_unknown=False,
    ):
        super().__init__(ignore_unknown)
        self.__instance_map = {}
        self.__discarded_objects = set()
        self.policy = policy or ImportPolicy()

    def read(self, stream: io.RawIOBase):
        _stream = stream

        class UncloseableStream:
            # Prevents ZipFile from closing the stream
            def __getattribute__(self, name: str) -> Any:
                if name == 'close':
                    return lambda: None
                return getattr(_stream, name)

        stream = UncloseableStream()  # type: ignore

        reader = BufferedReader(stream)
        signature = reader.peek(4)

        archive: Optional[zipfile.ZipFile] = None
        if signature[:2] == b'PK':
            logger.debug('Detected a ZIP container')
            archive = zipfile.ZipFile(reader, 'r')
            try:
                metadata_stream = archive.open('metadata.yaml', 'r')
            finally:
                archive.close()
        else:
            metadata_stream = reader

        try:
            try:
                all_kinds = set(ID.kind_for_model(x) for x in apps.get_models())
                yaml = get_yaml()
                for document in yaml.load_all(TextIOWrapper(metadata_stream)):
                    if document['_'] == 'header':
                        if document['version'] != 1:
                            raise ValueError(f'Unknown container version {document["version"]}')
                        unknown_kinds = set(document['object_kinds']) - all_kinds
                        if unknown_kinds:
                            raise ValueError(f'Unknown object types {unknown_kinds}')
                        self.metadata = document.get('metadata')
                        if self.metadata:
                            logger.debug(f'Container metadata: {self.metadata}')
                    elif document['_'] == 'object':
                        id = document['id']
                        logger.debug(f'Extracting object {id}')
                        obj = ObjectData(
                            id=document['id'],
                            serialized_data=document['data'],
                            attachments=[
                                Attachment(
                                    id=item['id'],
                                    key=item['key'],
                                    _container_stream=stream,
                                )
                                for item in document['attachments']
                            ]
                        )
                        if obj.id in self._objects:
                            raise ValueError(f'Duplicate object {obj.id} found')
                        self._objects[obj.id] = obj
                    else:
                        raise ValueError(f'Unknown container segment "{document["_"]}"')
            finally:
                metadata_stream.close()
        finally:
            if archive:
                archive.close()

    def import_objects(self):
        kind_map = self.__group_by_kind(self._objects.values())

        for kind, objects in list(kind_map.items()):
            try:
                serializer_cls = self._serializer_for_kind(kind)
            except ModelClassNotRegistered:
                if self.ignore_unknown:
                    logger.debug(f'Ignoring {len(objects)} {kind} objects')
                    self.__discarded_objects |= {x.id for x in objects}
                    continue
                raise

            serializer = serializer_cls(data=[x.serialized_data for x in objects], many=True)
            serializer.is_valid(raise_exception=True)
            logger.debug(f'Deserialized {len(objects)} {kind} objects')

            if len(objects) != len(serializer.validated_data):
                raise ValueError('Serializer has failed to deserialize all objects')

            for obj, deserialized_data in zip(objects, serializer.validated_data):
                obj.fields = deserialized_data
                for key, value in obj.fields.items():
                    # Foreign key
                    if isinstance(value, Ref):
                        obj.add_reference(value)
                        logger.debug(f'Found a reference from {obj.id} to {value.ids}')

            for obj in self._objects.values():
                for ref in obj.refs:
                    for id in ref.ids:
                        if id not in self._objects:
                            raise ValueError(f'Unresolved reference to {id} from {obj.id} via {ref.field}')

        sorter = graphlib.TopologicalSorter(None)
        for obj in self._objects.values():
            if obj.id not in self.__discarded_objects:
                deps = [
                    self._objects[id]
                    for ref in obj.refs
                    for id in ref.ids
                    if id not in self.__discarded_objects and not ref.weak
                ]
                sorter.add(
                    obj,
                    *deps,
                )

        try:
            sorter.prepare()
        except graphlib.CycleError as e:
            logger.error('Cycle detected')
            for obj in e.args[1]:
                logger.error(f' - {obj}')
            raise e

        while sorter.is_active():
            objects: Tuple[ObjectData] = sorter.get_ready()
            if not len(objects):
                raise RuntimeError('Could not untangle the reference graph')

            kind_map = self.__group_by_kind(objects)

            for kind, objects in kind_map.items():
                model_meta = ID.model_for_kind(kind)._meta.concrete_model._meta

                for obj in objects:
                    for ref in obj.refs:
                        if ref.weak:
                            continue
                        remaining_ids = list(ref.ids)
                        discarded = False

                        for id in ref.ids:
                            if id not in self.__instance_map:
                                if id in self.__discarded_objects:
                                    if ref.nullable:
                                        logger.debug(f'Breaking reference {obj.id}.{ref.field} due to target object being discarded')
                                        remaining_ids.remove(id)
                                        continue
                                    else:
                                        logger.debug(f'Recursively discarding object {obj.id} due to a broken reference via {ref.field}')
                                        self.__discarded_objects.add(obj.id)
                                        sorter.done(obj)
                                        discarded = True
                                        break
                                raise ValueError(f'Consistency error: PK still unknown for {id} (referenced by {obj.id} via {ref.field})')

                        if discarded:
                            continue

                        if model_meta.get_field(ref.field).many_to_many:
                            obj.fields[ref.field] = [
                                self.__instance_map[id]
                                for id in remaining_ids
                            ]
                            logger.debug(f'Remapped M2M {obj.id}.{ref.field} reference from {ref.ids} to {obj.fields[ref.field]}')
                        else:
                            if len(remaining_ids):
                                obj.fields[ref.field] = self.__instance_map[remaining_ids[0]]
                                logger.debug(f'Remapped {obj.id}.{ref.field} reference from {ref.ids[0]} to {obj.fields[ref.field].pk}')
                            else:
                                obj.fields[ref.field] = None

                # Remove reverse FK fields
                for relation in model_meta.related_objects:
                    if isinstance(relation, ManyToOneRel):
                        obj.fields.pop(relation.related_name, None)

                # Remove many-to-many relationships from validated_data.
                # They are not valid arguments to the default `.create()` method,
                # as they require that the instance has already been saved.
                # info = model_meta.get_field_info(ModelClass)
                # many_to_many = {}
                # for field_name, relation_info in info.relations.items():
                #     if relation_info.to_many and (field_name in validated_data):
                #         many_to_many[field_name] = validated_data.pop(field_name)

                relink_actions = [
                    self.policy.relink_object(
                        ID.model_for_kind(kind),
                        obj,
                    )
                    for obj in objects
                    if obj.id not in self.__discarded_objects
                ]

                for action in set(relink_actions):
                    action_objects = [x[1] for x in zip(relink_actions, objects) if x[0] == action]

                    for obj in action_objects:
                        self.policy.postprocess_object_fields(ID.model_for_kind(kind), obj.fields)

                    # TODO separate handling even necessary?
                    if isinstance(action, RelinkAction.Discard):
                        self.__discarded_objects |= {x.id for x in action_objects}
                        logger.debug(f'Discarding {len(action_objects)} objects')
                        for obj in action_objects:
                            sorter.done(obj)
                        continue

                    logger.debug(f'Running relink action {action} on {len(action_objects)} {kind} objects')
                    instances = action._execute(ID.model_for_kind(kind), action_objects, self.policy)
                    for obj, instance in zip(action_objects, instances):
                        if instance == DISCARD_OBJECT:
                            self.__discarded_objects.add(obj.id)
                        else:
                            self.__instance_map[obj.id] = instance
                        sorter.done(obj)

        container_streams = set()
        for obj in self._objects.values():
            for attachment in obj.attachments:
                container_streams.add(attachment._container_stream)

        for stream in container_streams:
            with zipfile.ZipFile(stream, 'r') as zfile:
                for obj in self._objects.values():
                    if obj.id in self.__discarded_objects:
                        continue
                    for attachment in obj.attachments:
                        if attachment._container_stream == stream:
                            with zfile.open(f'attachments/{attachment.id}', 'r') as f:
                                self.policy.process_attachment(self.__instance_map[obj.id], attachment.key, f)

    def __group_by_kind(self, objects: Iterable[ObjectData]) -> Dict[str, List[ObjectData]]:
        kind_map: Dict[str, List[ObjectData]] = {}
        for obj in objects:
            kind_map.setdefault(obj.id.kind, []).append(obj)
        return kind_map
