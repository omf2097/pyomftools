from validx import Dict, List, Tuple
import typing

from .protos import DataObject
from .utils.validator import UInt8
from .utils.types import Color, Remapping


class Palette(DataObject):
    __slots__ = ("data",)

    schema = Dict({"data": List(Tuple(UInt8, UInt8, UInt8))})

    def __init__(self):
        self.data: typing.List[Color] = [(0, 0, 0) for _ in range(256)]

    def remap(self, remapping: Remapping) -> "Palette":
        pal = Palette()
        pal.data = [self.data[r] for r in remapping]
        return pal

    @staticmethod
    def _read_one(parser) -> Color:
        r = parser.get_uint8()
        g = parser.get_uint8()
        b = parser.get_uint8()
        r_8 = int((r * 255) / 63.0)
        g_8 = int((g * 255) / 63.0)
        b_8 = int((b * 255) / 63.0)
        return r_8, g_8, b_8

    def read_range(self, parser, start: int, length: int):
        for m in range(start, start + length):
            self.data[m] = self._read_one(parser)
        return self

    def read(self, parser):
        self.data.clear()
        for m in range(0, 256):
            self.data.append(self._read_one(parser))
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

    def unserialize(self, data: dict):
        self.data = data["data"]
        return self
