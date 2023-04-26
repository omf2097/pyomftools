from __future__ import annotations
import typing

from .protos import Entrypoint
from .palette import Palette
from .utils.parser import BinaryParser


class AltPaletteFile(Entrypoint):
    __slots__ = ("palettes",)

    def __init__(self) -> None:
        self.palettes: list[Palette] = []

    def serialize(self) -> dict:
        return {
            "palettes": [p.serialize() for p in self.palettes],
        }

    def read(self, parser: BinaryParser) -> AltPaletteFile:
        self.palettes = [Palette().read(parser) for _ in range(11)]
        return self
