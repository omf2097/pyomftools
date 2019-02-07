from validx import Dict, List, Tuple

from .protos import DataObject
from .utils.parser import BinaryParser
from .utils.validator import UInt8
from .utils.types import Palette, Remappings, Remapping


class PaletteMapping(DataObject):
    __slots__ = (
        'colors',
        'remaps',
    )

    schema = Dict({
        'colors': List(
            Tuple(
                UInt8,
                UInt8,
                UInt8,
            )
        ),
        'remaps': List(List(UInt8)),
    })

    def __init__(self):
        self.colors: Palette = []
        self.remaps: Remappings = []

    def read(self, parser: BinaryParser) -> 'PaletteMapping':
        for m in range(0, 256):
            self.colors.append((
                parser.get_uint8(),
                parser.get_uint8(),
                parser.get_uint8(),
            ))
        for k in range(0, 19):
            remap: Remapping = []
            for m in range(0, 256):
                remap.append(parser.get_uint8())
            self.remaps.append(remap)
        return self

    def write(self, parser):
        for m in range(0, 256):
            c = self.colors[m]
            parser.put_uint8(c[0])
            parser.put_uint8(c[1])
            parser.put_uint8(c[2])

        for k in range(0, 19):
            for m in range(0, 256):
                parser.put_uint8(self.remaps[k][m])

    def serialize(self) -> dict:
        return {
            'colors': self.colors,
            'remaps': self.remaps
        }

    def unserialize(self, data: dict) -> 'PaletteMapping':
        self.colors = data['colors']
        self.remaps = data['remaps']
        return self
