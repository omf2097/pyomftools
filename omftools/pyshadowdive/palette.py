from validx import Dict, List, Tuple
import typing

from .protos import DataObject
from .utils.validator import UInt8
from .utils.types import Color


class Palette(DataObject):
    __slots__ = ("data",)

    schema = Dict({"data": List(Tuple(UInt8, UInt8, UInt8,)),})

    def __init__(self):
        self.data: typing.List[Color] = [(0, 0, 0) for _ in range(256)]

    def read_range(self, parser, start: int, length: int) -> "Palette":
        for m in range(start, start + length):
            r = parser.get_uint8()
            g = parser.get_uint8()
            b = parser.get_uint8()
            self.data[m] = (
                int((r * 255) / 63.0),
                int((g * 255) / 63.0),
                int((b * 255) / 63.0),
            )
        return self

    def read(self, parser) -> "Palette":
        self.data = []
        for m in range(0, 256):
            r = parser.get_uint8()
            g = parser.get_uint8()
            b = parser.get_uint8()
            self.data.append(
                (int((r * 255) / 63.0), int((g * 255) / 63.0), int((b * 255) / 63.0),)
            )
        return self

    def write(self, parser):
        for m in range(0, 256):
            c = self.data[m]
            parser.put_uint8((c[0] & 0xFF) >> 2)
            parser.put_uint8((c[1] & 0xFF) >> 2)
            parser.put_uint8((c[2] & 0xFF) >> 2)

    def serialize(self) -> dict:
        return {
            "data": self.data,
        }

    def unserialize(self, data: dict) -> "Palette":
        self.data = data["data"]
        return self
