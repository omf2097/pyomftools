import typing

from .protos import Entrypoint
from .palette import Palette


class AltPaletteFile(Entrypoint):
    __slots__ = ("palettes",)

    def __init__(self):
        self.palettes: typing.List[Palette] = []

    def serialize(self):
        return {
            "palettes": [p.serialize() for p in self.palettes],
        }

    def read(self, parser):
        self.palettes = [Palette().read(parser) for _ in range(11)]
        return self
