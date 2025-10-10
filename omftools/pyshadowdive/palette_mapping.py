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

    def __init__(self) -> None:
        self.colors: Palette = Palette()
        self.remaps: Remappings = []

    def remap(self, remap_id: int) -> Palette:
        return self.colors.remap(self.remaps[remap_id])

    def read(self, parser: BinaryParser, palette_type: str = "default"):
        """Read palette data from parser with specified palette type.

        Args:
            parser: BinaryParser to read data from
            palette_type: One of:
                - "default": Use BK palette intact
                - "reset": Reset indices 0-96 and 250-255 to default colors (Arenas, VS, MELEE, MECHLAB)
                - "extended_slides": Extended color slides (NORTH_AM, WAR, WORLD, KATUSHAI)
        """
        # Read the palette from the file
        self.colors = Palette().read(parser)

        # Apply palette-specific processing
        if palette_type == "reset":
            # Reset indices 0-96 and 250-255 to default colors
            # Used for Arenas, VS, MELEE, MECHLAB
            self.colors.reset_range(0, 97)
            self.colors.reset_range(250, 6)
        elif palette_type == "extended_slides":
            # Extended color slides (double length - 32 colors instead of 16)
            # Used for NORTH_AM, WAR, WORLD, KATUSHAI
            # This would be implemented elsewhere if needed
            pass
        # For "default" type, we keep the palette as read from the file

        # Read remappings
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
