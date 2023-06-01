from __future__ import annotations
from validx import Dict, List, Tuple

from .protos import DataObject
from .utils.parser import BinaryParser
from .utils.validator import UInt8
from .utils.types import Color, Remapping


class Palette(DataObject):
    __slots__ = ("data",)

    schema = Dict({"data": List(Tuple(UInt8, UInt8, UInt8))})

    def __init__(self) -> None:
        self.data: list[Color] = [(0, 0, 0) for _ in range(256)]

    def remap(self, remapping: Remapping) -> Palette:
        pal = Palette()
        pal.data = [self.data[r] for r in remapping]
        return pal

    @staticmethod
    def _read_one(parser) -> Color:
        r = parser.get_uint8()
        g = parser.get_uint8()
        b = parser.get_uint8()
        r_8 = int((r * 255.0) / 63.0)
        g_8 = int((g * 255.0) / 63.0)
        b_8 = int((b * 255.0) / 63.0)
        return r_8, g_8, b_8

    def read_range(self, parser: BinaryParser, start: int, length: int) -> Palette:
        for m in range(start, start + length):
            self.data[m] = self._read_one(parser)
        return self

    def read(self, parser: BinaryParser) -> Palette:
        self.data.clear()
        for m in range(0, 256):
            self.data.append(self._read_one(parser))
        return self

    @staticmethod
    def _write_one(parser: BinaryParser, c: Color) -> None:
        parser.put_uint8(int((c[0] * 63.0) / 255.0))
        parser.put_uint8(int((c[1] * 63.0) / 255.0))
        parser.put_uint8(int((c[2] * 63.0) / 255.0))

    def write_range(self, parser: BinaryParser, start: int, length: int) -> None:
        for m in range(start, start + length):
            self._write_one(parser, self.data[m])

    def write(self, parser: BinaryParser) -> None:
        for m in range(0, 256):
            self._write_one(parser, self.data[m])

    def serialize(self) -> dict:
        return {
            "data": self.data,
        }

    def unserialize(self, data: dict) -> Palette:
        self.data = data["data"]
        return self
