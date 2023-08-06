from django.db.models import Model
from typing import Dict

from ..errors import ModelClassNotRegistered
from ..types import ID, ObjectData


class BaseContainer:
    _objects: Dict[ID, ObjectData]

    def __init__(self, ignore_unknown=False):
        self.__serializer_registry = {}
        self._objects = {}
        self.ignore_unknown = ignore_unknown

    def register_serializer(self, serializer_cls):
        kind = ID.kind_for_model(serializer_cls.Meta.model)
        self.__serializer_registry[kind] = serializer_cls

    def dump_objects(self):
        for obj in self._objects.values():
            print(f'* {obj.id}')
            print('\n  Fields:')
            for k, v in obj.serialized_data.items():
                print(f'  - {k} = {repr(v)}')
            if obj.attachments:
                print('\n  Attachments:')
                for a in obj.attachments:
                    print(f'  - {a.id}: {repr(a.key)}')
            print()

    def _serializer_for_model(self, obj: Model, raise_exception=True):
        return self._serializer_for_kind(ID.kind_for_model(obj), raise_exception=raise_exception)

    def _serializer_for_kind(self, kind: str, raise_exception=True):
        if kind not in self.__serializer_registry:
            if not raise_exception:
                return None
            raise ModelClassNotRegistered(kind)
        return self.__serializer_registry[kind]
