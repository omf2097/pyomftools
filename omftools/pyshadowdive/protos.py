import json
import typing
from enum import Enum, Flag
from abc import ABCMeta, abstractmethod
import validx
import validx.exc

from .utils.parser import BinaryParser
from .utils.exceptions import OMFInvalidDataException

# (name, value, decoded value or None, field hint or None, value hint or None)
PropertyDict = list[
    typing.Tuple[
        str,
        typing.Union[str, float, int],
        typing.Union[str, float, int, None],
        typing.Optional[str],
        typing.Optional[str],
    ]
]


def enum_value_hint(value: typing.Any) -> typing.Optional[str]:
    """Hint text for an enum value, from the enum's `get_hint()` method.
    For flags, one line per set bit."""
    if not isinstance(value, Enum) or not hasattr(value, "get_hint"):
        return None
    if isinstance(value, Flag):
        lines = []
        hinted = False
        for member in type(value):
            if member.value and member in value:
                hint = member.get_hint()
                hinted = hinted or bool(hint)
                lines.append(f"{member.name}: {hint}" if hint else member.name)
        return "\n".join(lines) if hinted else None
    return value.get_hint()


EntrypointType = typing.TypeVar("EntrypointType", bound="Entrypoint")


class DataObject(metaclass=ABCMeta):
    __slots__ = ()

    def get_hint(self, attr: str) -> typing.Optional[str]:
        """Human-readable explanation of field `attr`, shown as a tooltip by the HTML
        generator; not part of serialized data. Subclasses override this with a
        `match attr:` and fall back to `super().get_hint(attr)`."""
        return None

    @abstractmethod
    def read(self, parser: BinaryParser):
        raise NotImplementedError()

    def write(self, parser: BinaryParser) -> None:
        raise NotImplementedError()

    def unserialize(self, data: dict):
        raise NotImplementedError()

    def serialize(self) -> dict:
        raise NotImplementedError()

    def get_selected_props(self, prop_names: list[str]) -> PropertyDict:
        content: PropertyDict = []
        for attr in prop_names:
            value = getattr(self, attr)
            content.append(
                (
                    attr,
                    value,
                    getattr(self, f"real_{attr}", None),
                    self.get_hint(attr),
                    enum_value_hint(value),
                )
            )
        return content

    def get_props(self) -> PropertyDict:
        content: PropertyDict = []
        for slots in [getattr(cls, "__slots__", []) for cls in type(self).__mro__]:
            for attr in slots:
                var = getattr(self, attr)
                if type(var) in [float, int, str] or issubclass(type(var), Enum):
                    dec_var = getattr(self, f"real_{attr}", None)
                    content.append(
                        (attr, var, dec_var, self.get_hint(attr), enum_value_hint(var))
                    )
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
