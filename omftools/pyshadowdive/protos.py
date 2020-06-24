import json
import typing
from enum import Enum
from abc import ABCMeta, abstractmethod
import validx
import validx.exc

from .utils.parser import BinaryParser
from .utils.exceptions import OMFInvalidDataException

PropertyDict = typing.List[
    typing.Tuple[
        str, typing.Union[str, float, int], typing.Union[str, float, int, None],
    ]
]

DataObjectType = typing.TypeVar('DataObjectType', bound='DataObject')
EntrypointType = typing.TypeVar('EntrypointType', bound='Entrypoint')


class DataObject(metaclass=ABCMeta):
    __slots__ = ()

    @abstractmethod
    def read(self, parser: BinaryParser) -> DataObjectType:
        raise NotImplementedError()

    def write(self, parser: BinaryParser) -> None:
        raise NotImplementedError()

    def unserialize(self, data: dict) -> DataObjectType:
        raise NotImplementedError()

    def serialize(self) -> dict:
        raise NotImplementedError()

    def get_selected_props(self, prop_names: typing.List[str]) -> PropertyDict:
        content: PropertyDict = []
        for attr in prop_names:
            content.append(
                (attr, getattr(self, attr, None), getattr(self, f"real_{attr}", None))
            )
        return content

    def get_props(self) -> PropertyDict:
        content: PropertyDict = []
        for slots in [getattr(cls, "__slots__", []) for cls in type(self).__mro__]:
            for attr in slots:
                var = getattr(self, attr, None)
                if type(var) in [float, int, str] or issubclass(type(var), Enum):
                    dec_var = getattr(self, f"real_{attr}", None)
                    content.append((attr, var, dec_var))
        return content


class Entrypoint(DataObject, metaclass=ABCMeta):
    __slots__ = ()

    schema: typing.ClassVar[validx.Validator] = validx.Dict()

    @classmethod
    def load_native(cls: typing.Type[EntrypointType], filename: str) -> EntrypointType:
        obj = cls()
        with open(filename, "rb", buffering=8192) as handle:
            obj.read(BinaryParser(handle))
        return obj

    def save_native(self, filename: str) -> None:
        with open(filename, "wb", buffering=8192) as handle:
            self.write(BinaryParser(handle))

    @classmethod
    def load_json(cls: typing.Type[EntrypointType], filename: str) -> EntrypointType:
        obj = cls()
        with open(filename, "rb", buffering=8192) as handle:
            obj.from_json(handle.read().decode())
        return obj

    def save_json(self, filename: str, **kwargs) -> None:
        with open(filename, "wb", buffering=8192) as handle:
            handle.write(self.to_json(**kwargs).encode())

    def to_json(self, **kwargs) -> str:
        return json.dumps(self.serialize(), **kwargs)

    @classmethod
    def from_json(cls: typing.Type[EntrypointType], data: str) -> EntrypointType:
        obj = cls()
        decoded_data = json.loads(data)

        try:
            obj.schema(decoded_data)
        except validx.exc.ValidationError as e:
            e.sort()
            rows = [f"{c}: {m}" for c, m in validx.exc.format_error(e)]
            raise OMFInvalidDataException("\n".join(rows))

        return obj.unserialize(decoded_data)
