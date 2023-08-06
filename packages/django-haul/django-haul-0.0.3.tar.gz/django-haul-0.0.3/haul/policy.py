import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from django.db.models import Model
from typing import Dict, Hashable, List, Tuple, Type, Optional, Any, IO

from .types import ID, Attachment, ObjectData


logger = logging.getLogger('haul.policy')


DISCARD_OBJECT = object()


class ManyToManyImportAction(Enum):
    REPLACE = auto()
    APPEND = auto()


@dataclass(frozen=True)
class BaseRelinkAction:
    fallback: Optional['BaseRelinkAction'] = None

    def execute(self, model_cls: Type[Model], objects: List[ObjectData], policy: 'ImportPolicy') -> List[Model]:
        raise NotImplementedError

    def _execute(self, model_cls: Type[Model], objects: List[ObjectData], policy: 'ImportPolicy') -> List[Model]:
        instances = self.execute(model_cls, objects, policy)
        if any(not x for x in instances):
            fallback_objects, fallback_indices = zip(*[
                (objects[i], i) for (i, x) in enumerate(instances) if not x
            ])
            if len(fallback_indices):
                if not self.fallback:
                    raise RuntimeError(f'{self} failed to resolve some items and there was no fallback provided')
                logger.debug(f'Fallback to {self.fallback} for {len(fallback_objects)} objects')
                fallback_instances = self.fallback.execute(model_cls, fallback_objects, policy)  # type: ignore
                for instance, index in zip(fallback_instances, fallback_indices):
                    instances[index] = instance
        return instances


@dataclass(frozen=True)
class BaseRelinkActionWithFieldsOverwrite(BaseRelinkAction):
    overwrite_fields: Tuple[str, ...] = tuple()

    def _execute(self, model_cls: Type[Model], objects: List[ObjectData], policy: 'ImportPolicy') -> List[Model]:
        instances = super()._execute(model_cls, objects, policy)
        if self.overwrite_fields:
            for obj, instance in zip(objects, instances):
                if instance and instance is not DISCARD_OBJECT:
                    assert obj.fields is not None
                    fields = {k: v for k, v in obj.fields.items() if k in self.overwrite_fields}
                    _assign_model_fields(instance, fields, policy)
                    instance.save()

        return instances


class RelinkAction:
    @dataclass(frozen=True)
    class LogToConsole(BaseRelinkAction):
        def execute(self, model_cls: Type[Model], objects: List[ObjectData], policy: 'ImportPolicy') -> List[Model]:
            for obj in objects:
                logger.info(f'[{obj.id}] -> {model_cls(**obj.fields)}')
            return [None] * len(objects)

    @dataclass(frozen=True)
    class Create(BaseRelinkAction):
        ignore_fields: Tuple[str, ...] = field(default_factory=tuple)

        def __post_init__(self):
            if not isinstance(self.ignore_fields, tuple):
                raise ValueError('ignore_fields must be a tuple')

        def execute(self, model_cls: Type[Model], objects: List[ObjectData], policy: 'ImportPolicy') -> List[Model]:
            fieldsets = [
                {k: v for k, v in obj.fields.items() if k not in self.ignore_fields}
                for obj in objects
                if obj.fields
            ]
            if False:  # TODO detect mysql
                instances = model_cls.objects.bulk_create([
                    model_cls(**_get_non_x2m_fields(model_cls, fields))
                    for fields in fieldsets
                ])
            else:
                instances = [
                    model_cls.objects.create(**_get_non_x2m_fields(model_cls, fields))
                    for fields in fieldsets
                ]
            for instance, fields in zip(instances, fieldsets):
                _assign_model_fields(instance, fields, policy)

            return instances

    @dataclass(frozen=True)
    class Discard(BaseRelinkAction):
        def execute(self, _model_cls, objects: List[ObjectData], policy: 'ImportPolicy') -> List[Model]:
            return [DISCARD_OBJECT] * len(objects)

    @dataclass(frozen=True)
    class LinkByFields(BaseRelinkActionWithFieldsOverwrite):
        lookup_fields: Tuple[str, ...] = field(default_factory=tuple)

        def __post_init__(self):
            if not isinstance(self.lookup_fields, tuple):
                raise ValueError('lookup_fields must be a tuple')
            if not len(self.lookup_fields):
                raise ValueError('lookup_fields must be set')
            if not isinstance(self.overwrite_fields, tuple):
                raise ValueError('overwrite_fields must be a tuple')

        def execute(self, model_cls: Type[Model], objects: List[ObjectData], policy: 'ImportPolicy') -> List[Model]:
            search_cache = {}
            instances = []
            for obj in objects:
                assert obj.fields is not None
                values = tuple(obj.fields.get(k) for k in self.lookup_fields)
                if values not in search_cache:
                    query = dict(zip(self.lookup_fields, values))
                    found = model_cls.objects.filter(**query).first()
                    search_cache[values] = found

                instances.append(search_cache.get(values))

            return instances

    @dataclass(frozen=True)
    class LinkByPK(BaseRelinkActionWithFieldsOverwrite):
        def __post_init__(self):
            if not isinstance(self.overwrite_fields, tuple):
                raise ValueError('overwrite_fields must be a tuple')

        def execute(self, model_cls: Type[Model], objects: List[ObjectData], policy: 'ImportPolicy') -> List[Model]:
            pks = [obj.id.pk for obj in objects]
            search_cache = {
                x.pk: x
                for x in model_cls.objects.filter(pk__in=pks)
            }
            return [
                search_cache.get(obj.id.pk)
                for obj in objects
            ]

    @dataclass(frozen=True)
    class LinkToInstance(BaseRelinkActionWithFieldsOverwrite):
        pk: Hashable = None

        def __post_init__(self):
            if not self.pk:
                raise ValueError('pk must be set')

        def execute(self, model_cls: Type[Model], objects: List[ObjectData], policy: 'ImportPolicy') -> List[Model]:
            instance = model_cls.objects.get(pk=self.pk)
            return [instance] * len(objects)


class ImportPolicy:
    def preprocess_object_fields(self, model_cls: Type[Model], fields: Dict[str, Any]):
        pass

    def postprocess_object_fields(self, model_cls: Type[Model], fields: Dict[str, Any]):
        pass

    def relink_object(self, model_cls: Type[Model], obj: ObjectData) -> BaseRelinkAction:
        return RelinkAction.Create()

    def process_many_to_many(self, instance: Model, field: str) -> ManyToManyImportAction:
        return ManyToManyImportAction.REPLACE

    def process_attachment(self, instance: Model, key: Any, stream: IO[bytes]):
        raise NotImplementedError('Attachments found but process_attachment is not implemented in the import policy')


class ExportPolicy:
    def get_attachments(self, instance: Model) -> List[Attachment]:
        return []

    def should_export_object(self, instance: Model):
        return True

    def should_follow_reference(self, instance: Model, target: ID, field: str):
        return True

    # def postprocess_object(self, instance: Model, data: Mapping[str, Any]):


def _get_non_x2m_fields(model_cls: Type[Model], fields: Dict[str, Any]):
    model_meta = model_cls._meta.concrete_model._meta
    return {
        k: v
        for k, v in fields.items()
        if not model_meta.get_field(k).many_to_many and
        not model_meta.get_field(k).one_to_many
    }


def _assign_model_fields(instance: Model, fields: Dict[str, Any], policy: ImportPolicy):
    model_meta = instance.__class__._meta.concrete_model._meta
    for key, value in fields.items():
        field_meta = model_meta.get_field(key)
        if field_meta.many_to_many:
            action = policy.process_many_to_many(instance, key)
            if action == ManyToManyImportAction.REPLACE:
                getattr(instance, key).set(value)
            else:
                for obj in value:
                    getattr(instance, key).add(obj)
        elif field_meta.one_to_many:
            # We don't need to actually *set* the field
            pass
        else:
            setattr(instance, key, value)
    instance.save()
