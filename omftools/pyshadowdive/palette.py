from __future__ import annotations
from validx import Dict, List, Tuple

from .protos import DataObject
from .utils.parser import BinaryParser
from .utils.validator import UInt8
from .utils.types import Color, Remapping


"""
The palette is designed to avoid dithering errors and prevent using the wrong area of the palette.

Key features:
- Color 0x00, 0x10, and 0x20 are black
- First 3 rows contain distinct color slides starting with black
- Colors 0x30-0x5F and 0xFB-0xFF are masked with magenta (255,0,255)
- Original grayscale and game colors are preserved where appropriate

Palette arrangement:
- 0x00-0x0F: Red slide
- 0x10-0x1F: Green slide
- 0x20-0x2F: Blue slide
- 0x30-0x5F: Masked with magenta
- 0x60-0xFA: Original game colors
- 0xFB-0xFF: Masked with magenta
"""

DEFAULT_PALETTE = [
    # Row 1 (0x00-0x0F): Red slide
    (0, 0, 0),  # 0x00 - Black
    (17, 0, 0),  # 0x01
    (34, 0, 0),  # 0x02
    (51, 0, 0),  # 0x03
    (68, 0, 0),  # 0x04
    (85, 0, 0),  # 0x05
    (102, 0, 0),  # 0x06
    (119, 0, 0),  # 0x07
    (136, 0, 0),  # 0x08
    (153, 0, 0),  # 0x09
    (170, 0, 0),  # 0x0A
    (187, 0, 0),  # 0x0B
    (204, 0, 0),  # 0x0C
    (221, 0, 0),  # 0x0D
    (238, 0, 0),  # 0x0E
    (255, 0, 0),  # 0x0F
    # Row 2 (0x10-0x1F): Green slide
    (0, 0, 0),  # 0x10 - Black
    (0, 17, 0),  # 0x11
    (0, 34, 0),  # 0x12
    (0, 51, 0),  # 0x13
    (0, 68, 0),  # 0x14
    (0, 85, 0),  # 0x15
    (0, 102, 0),  # 0x16
    (0, 119, 0),  # 0x17
    (0, 136, 0),  # 0x18
    (0, 153, 0),  # 0x19
    (0, 170, 0),  # 0x1A
    (0, 187, 0),  # 0x1B
    (0, 204, 0),  # 0x1C
    (0, 221, 0),  # 0x1D
    (0, 238, 0),  # 0x1E
    (0, 255, 0),  # 0x1F
    # Row 3 (0x20-0x2F): Blue slide
    (0, 0, 0),  # 0x20 - Black
    (0, 0, 17),  # 0x21
    (0, 0, 34),  # 0x22
    (0, 0, 51),  # 0x23
    (0, 0, 68),  # 0x24
    (0, 0, 85),  # 0x25
    (0, 0, 102),  # 0x26
    (0, 0, 119),  # 0x27
    (0, 0, 136),  # 0x28
    (0, 0, 153),  # 0x29
    (0, 0, 170),  # 0x2A
    (0, 0, 187),  # 0x2B
    (0, 0, 204),  # 0x2C
    (0, 0, 221),  # 0x2D
    (0, 0, 238),  # 0x2E
    (0, 0, 255),  # 0x2F
    # Row 4-6 (0x30-0x5F): Masked with magenta
    (255, 0, 255),  # 0x30
    (255, 0, 255),  # 0x31
    (255, 0, 255),  # 0x32
    (255, 0, 255),  # 0x33
    (255, 0, 255),  # 0x34
    (255, 0, 255),  # 0x35
    (255, 0, 255),  # 0x36
    (255, 0, 255),  # 0x37
    (255, 0, 255),  # 0x38
    (255, 0, 255),  # 0x39
    (255, 0, 255),  # 0x3A
    (255, 0, 255),  # 0x3B
    (255, 0, 255),  # 0x3C
    (255, 0, 255),  # 0x3D
    (255, 0, 255),  # 0x3E
    (255, 0, 255),  # 0x3F
    (255, 0, 255),  # 0x40
    (255, 0, 255),  # 0x41
    (255, 0, 255),  # 0x42
    (255, 0, 255),  # 0x43
    (255, 0, 255),  # 0x44
    (255, 0, 255),  # 0x45
    (255, 0, 255),  # 0x46
    (255, 0, 255),  # 0x47
    (255, 0, 255),  # 0x48
    (255, 0, 255),  # 0x49
    (255, 0, 255),  # 0x4A
    (255, 0, 255),  # 0x4B
    (255, 0, 255),  # 0x4C
    (255, 0, 255),  # 0x4D
    (255, 0, 255),  # 0x4E
    (255, 0, 255),  # 0x4F
    (255, 0, 255),  # 0x50
    (255, 0, 255),  # 0x51
    (255, 0, 255),  # 0x52
    (255, 0, 255),  # 0x53
    (255, 0, 255),  # 0x54
    (255, 0, 255),  # 0x55
    (255, 0, 255),  # 0x56
    (255, 0, 255),  # 0x57
    (255, 0, 255),  # 0x58
    (255, 0, 255),  # 0x59
    (255, 0, 255),  # 0x5A
    (255, 0, 255),  # 0x5B
    (255, 0, 255),  # 0x5C
    (255, 0, 255),  # 0x5D
    (255, 0, 255),  # 0x5E
    (255, 0, 255),  # 0x5F
    # Original game colors (0x60-0xFA)
    # Row 7 (0x60-0x6F): Blue shades
    (0, 0, 48),  # 0x60
    (0, 0, 60),  # 0x61
    (0, 0, 72),  # 0x62
    (0, 0, 85),  # 0x63
    (0, 0, 97),  # 0x64
    (0, 0, 109),  # 0x65
    (0, 0, 121),  # 0x66
    (0, 0, 137),  # 0x67
    (0, 0, 149),  # 0x68
    (0, 0, 161),  # 0x69
    (0, 0, 174),  # 0x6A
    (0, 0, 186),  # 0x6B
    (0, 0, 198),  # 0x6C
    (0, 0, 210),  # 0x6D
    (0, 0, 222),  # 0x6E
    (0, 0, 238),  # 0x6F
    # Row 8 (0x70-0x7F): Dark gradient
    (0, 0, 0),  # 0x70
    (0, 0, 4),  # 0x71
    (4, 4, 8),  # 0x72
    (8, 8, 12),  # 0x73
    (12, 16, 16),  # 0x74
    (16, 20, 24),  # 0x75
    (20, 24, 28),  # 0x76
    (24, 28, 32),  # 0x77
    (28, 32, 40),  # 0x78
    (36, 40, 44),  # 0x79
    (40, 44, 48),  # 0x7A
    (44, 48, 56),  # 0x7B
    (48, 52, 60),  # 0x7C
    (52, 60, 68),  # 0x7D
    (56, 64, 72),  # 0x7E
    (60, 68, 76),  # 0x7F
    # Row 9 (0x80-0x8F): Blue-gray gradient
    (64, 72, 85),  # 0x80
    (68, 76, 89),  # 0x81
    (72, 85, 93),  # 0x82
    (76, 89, 101),  # 0x83
    (85, 93, 105),  # 0x84
    (89, 97, 109),  # 0x85
    (93, 101, 117),  # 0x86
    (97, 109, 121),  # 0x87
    (101, 113, 125),  # 0x88
    (105, 117, 133),  # 0x89
    (109, 121, 137),  # 0x8A
    (113, 125, 141),  # 0x8B
    (117, 133, 149),  # 0x8C
    (121, 137, 153),  # 0x8D
    (125, 141, 161),  # 0x8E
    (129, 145, 165),  # 0x8F
    # Row 10 (0x90-0x9F): Light blue-gray gradient
    (133, 153, 170),  # 0x90
    (137, 157, 178),  # 0x91
    (141, 161, 182),  # 0x92
    (149, 165, 186),  # 0x93
    (153, 170, 194),  # 0x94
    (157, 178, 198),  # 0x95
    (161, 182, 202),  # 0x96
    (165, 186, 210),  # 0x97
    (170, 190, 214),  # 0x98
    (174, 194, 218),  # 0x99
    (178, 202, 226),  # 0x9A
    (182, 206, 230),  # 0x9B
    (186, 210, 238),  # 0x9C
    (190, 214, 242),  # 0x9D
    (198, 222, 246),  # 0x9E
    (202, 226, 255),  # 0x9F
    # Row 11 (0xA0-0xAF): Green and blue gradients
    (0, 32, 0),  # 0xA0
    (0, 60, 0),  # 0xA1
    (0, 93, 0),  # 0xA2
    (0, 125, 0),  # 0xA3
    (0, 157, 0),  # 0xA4
    (0, 190, 0),  # 0xA5
    (0, 222, 0),  # 0xA6
    (0, 255, 0),  # 0xA7
    (0, 0, 32),  # 0xA8
    (0, 0, 60),  # 0xA9
    (0, 0, 93),  # 0xAA
    (0, 0, 125),  # 0xAB
    (0, 0, 157),  # 0xAC
    (0, 0, 190),  # 0xAD
    (0, 0, 222),  # 0xAE
    (0, 0, 255),  # 0xAF
    # Row 12 (0xB0-0xBF): Red and purple gradients
    (32, 0, 0),  # 0xB0
    (60, 0, 0),  # 0xB1
    (93, 0, 0),  # 0xB2
    (125, 0, 0),  # 0xB3
    (157, 0, 0),  # 0xB4
    (190, 0, 0),  # 0xB5
    (222, 0, 0),  # 0xB6
    (255, 0, 0),  # 0xB7
    (32, 0, 32),  # 0xB8
    (60, 0, 60),  # 0xB9
    (89, 0, 93),  # 0xBA
    (113, 0, 125),  # 0xBB
    (137, 0, 157),  # 0xBC
    (157, 0, 190),  # 0xBD
    (178, 0, 222),  # 0xBE
    (194, 0, 255),  # 0xBF
    # Row 13 (0xC0-0xCF): Gray-blue and yellow gradients
    (76, 85, 89),  # 0xC0
    (97, 109, 113),  # 0xC1
    (117, 133, 137),  # 0xC2
    (141, 157, 161),  # 0xC3
    (161, 178, 182),  # 0xC4
    (182, 202, 206),  # 0xC5
    (202, 226, 230),  # 0xC6
    (222, 250, 255),  # 0xC7
    (32, 32, 0),  # 0xC8
    (60, 60, 0),  # 0xC9
    (93, 89, 8),  # 0xCA
    (125, 117, 16),  # 0xCB
    (157, 141, 32),  # 0xCC
    (190, 170, 52),  # 0xCD
    (222, 194, 72),  # 0xCE
    (255, 222, 101),  # 0xCF
    # Row 14 (0xD0-0xDF): Grayscale gradient
    (12, 12, 12),  # 0xD0
    (24, 24, 24),  # 0xD1
    (44, 44, 44),  # 0xD2
    (60, 60, 60),  # 0xD3
    (76, 76, 76),  # 0xD4
    (93, 93, 93),  # 0xD5
    (109, 109, 109),  # 0xD6
    (125, 125, 125),  # 0xD7
    (141, 141, 141),  # 0xD8
    (157, 157, 157),  # 0xD9
    (174, 174, 174),  # 0xDA
    (190, 190, 190),  # 0xDB
    (206, 206, 206),  # 0xDC
    (222, 222, 222),  # 0xDD
    (238, 238, 238),  # 0xDE
    (255, 255, 255),  # 0xDF
    # Row 15 (0xE0-0xEF): Cyan and tan gradients
    (0, 68, 93),  # 0xE0
    (8, 93, 113),  # 0xE1
    (24, 117, 137),  # 0xE2
    (48, 145, 161),  # 0xE3
    (72, 174, 182),  # 0xE4
    (105, 198, 206),  # 0xE5
    (141, 226, 230),  # 0xE6
    (186, 255, 255),  # 0xE7
    (76, 56, 36),  # 0xE8
    (101, 76, 48),  # 0xE9
    (129, 97, 64),  # 0xEA
    (157, 117, 76),  # 0xEB
    (186, 137, 93),  # 0xEC
    (214, 157, 109),  # 0xED
    (226, 186, 141),  # 0xEE
    (250, 234, 190),  # 0xEF
    # Row 16 (0xF0-0xFA): Miscellaneous colors
    (255, 60, 0),  # 0xF0
    (255, 109, 0),  # 0xF1
    (255, 157, 0),  # 0xF2
    (255, 206, 0),  # 0xF3
    (0, 0, 4),  # 0xF4
    (0, 0, 20),  # 0xF5
    (255, 56, 109),  # 0xF6
    (0, 105, 0),  # 0xF7
    (97, 149, 186),  # 0xF8
    (89, 40, 101),  # 0xF9
    (0, 105, 0),  # 0xFA
    # Masked colors (0xFB-0xFF) with magenta
    (255, 0, 255),  # 0xFB
    (255, 0, 255),  # 0xFC
    (255, 0, 255),  # 0xFD
    (255, 0, 255),  # 0xFE
    (255, 0, 255),  # 0xFF
]


class Palette(DataObject):
    __slots__ = ("data",)

    schema = Dict({"data": List(Tuple(UInt8, UInt8, UInt8))})

    def __init__(self) -> None:
        self.data: list[Color] = list(DEFAULT_PALETTE)

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

    def mask_range(self, start: int, length: int) -> Palette:
        """Fill a range of palette indices with magenta (255,0,255).

        This is useful for marking regions of the palette that should not be used
        for specific asset types.

        Args:
            start: Starting index to mask
            length: Number of indices to mask

        Returns:
            Self for method chaining
        """
        for m in range(start, start + length):
            if 0 <= m < 256:
                self.data[m] = (255, 0, 255)  # Magenta
        return self

    def reset_range(self, start: int, length: int) -> Palette:
        """Reset a range of palette indices back to default values.

        This is useful for restoring parts of the palette to their original colors
        after reading specific asset data.

        Args:
            start: Starting index to reset
            length: Number of indices to reset

        Returns:
            Self for method chaining
        """
        for m in range(start, start + length):
            if 0 <= m < 256 and m < len(DEFAULT_PALETTE):
                self.data[m] = DEFAULT_PALETTE[m]
        return self

    def create_extended_slides(self) -> Palette:
        """Create extended color slides that span 32 colors each instead of 16.

        This creates three extended color slides:
        - Red slide:   indices 0x00-0x1F (32 colors)
        - Green slide: indices 0x20-0x3F (32 colors)
        - Blue slide:  indices 0x40-0x5F (32 colors)

        This is used by certain BK files (NORTH_AM, WAR, WORLD, KATUSHAI).

        Returns:
            Self for method chaining
        """
        # Preserve the first color of each slide (typically black)
        first_red = self.data[0x00]
        first_green = self.data[0x20]
        first_blue = self.data[0x40]

        # Create extended red slide (0x00-0x1F)
        for i in range(32):
            if i > 0:  # Skip the first color
                red_value = min(255, i * 8)  # Increase by 8 for each step
                self.data[i] = (red_value, 0, 0)

        # Create extended green slide (0x20-0x3F)
        for i in range(32):
            if i > 0:  # Skip the first color
                green_value = min(255, i * 8)  # Increase by 8 for each step
                self.data[0x20 + i] = (0, green_value, 0)

        # Create extended blue slide (0x40-0x5F)
        for i in range(32):
            if i > 0:  # Skip the first color
                blue_value = min(255, i * 8)  # Increase by 8 for each step
                self.data[0x40 + i] = (0, 0, blue_value)

        # Restore first colors
        self.data[0x00] = first_red
        self.data[0x20] = first_green
        self.data[0x40] = first_blue

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
