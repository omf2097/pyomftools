from validx import Dict, List

from .protos import DataObject
from .palette import Palette
from .utils.parser import BinaryParser
from .utils.validator import UInt8
from .utils.types import Remappings, Remapping


class PaletteMapping(DataObject):
    __slots__ = (
        "colors",
        "remaps",
    )

    schema = Dict({"colors": Palette.schema, "remaps": List(List(UInt8))})

    def __init__(self):
        self.colors: Palette = Palette()
        self.remaps: Remappings = []

    def remap(self, remap_id: int) -> Palette:
        return self.colors.remap(self.remaps[remap_id])

    def read(self, parser: BinaryParser):
        self.colors = Palette().read(parser)
        for k in range(0, 19):
            remap: Remapping = []
            for m in range(0, 256):
                remap.append(parser.get_uint8())
            self.remaps.append(remap)
        return self

    def write(self, parser):
        self.colors.write(parser)
        for k in range(0, 19):
            for m in range(0, 256):
                parser.put_uint8(self.remaps[k][m])

    def serialize(self) -> dict:
        return {"colors": self.colors.serialize(), "remaps": self.remaps}

    def unserialize(self, data: dict):
        self.colors = Palette().unserialize(data["colors"])
        self.remaps = data["remaps"]
        return self
