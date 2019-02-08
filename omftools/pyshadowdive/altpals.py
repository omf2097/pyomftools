import typing

from .protos import Entrypoint
from .palettes import Palette


class AltPalettes(Entrypoint):
    __slots__ = (
        'palettes',
    )

    def __init__(self):
        self.palettes: typing.List[Palette] = []

    def serialize(self):
        return {
            'palettes': self.palettes,
        }

    def read(self, parser):
        self.palettes = []
        for p in range(11):
            colors = []
            for m in range(0, 256):
                r = parser.get_uint8()
                g = parser.get_uint8()
                b = parser.get_uint8()
                colors.append((
                    (r << 2) | ((r & 0x30) >> 4),
                    (g << 2) | ((g & 0x30) >> 4),
                    (b << 2) | ((b & 0x30) >> 4),
                ))
            self.palettes.append(colors)
        return self
