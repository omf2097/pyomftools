from __future__ import annotations

from functools import cache

from validx import Dict, Bool, List

from .protos import DataObject
from .palette import Palette
from .utils.parser import BinaryParser
from .utils.validator import UInt16, Int16, UInt8
from .utils.types import EncodedImage, RawImage
from .utils.exceptions import OMFInvalidDataException
from .utils.images import save_png, generate_png


class Sprite(DataObject):
    TRANSPARENCY_INDEX = 256

    __slots__ = (
        "pos_x",
        "pos_y",
        "width",
        "height",
        "index",
        "missing",
        "image",
    )

    schema = Dict(
        {
            "pos_x": Int16,
            "pos_y": Int16,
            "width": UInt16,
            "height": UInt16,
            "index": UInt8,
            "missing": Bool(),
            "image": List(UInt8, maxlen=65535),
        }
    )

    def __init__(self) -> None:
        self.pos_x: int = 0
        self.pos_y: int = 0
        self.index: int = 0
        self.missing: bool = False
        self.width: int = 0
        self.height: int = 0
        self.image: EncodedImage = []

    def read(self, parser: BinaryParser) -> Sprite:
        image_len = parser.get_uint16()
        self.pos_x = parser.get_int16()
        self.pos_y = parser.get_int16()
        self.width = parser.get_uint16()
        self.height = parser.get_uint16()
        self.index = parser.get_uint8()
        self.missing = parser.get_boolean()

        self.image = []
        if image_len and not self.missing:
            self.image = [parser.get_uint8() for _ in range(image_len)]

        return self

    @cache
    def scan_image(self) -> tuple[int, int, list[int]]:
        start_index: int = 255
        end_index: int = 0
        indexes: set[int] = set()

        image = self.decode_image()
        for index in image:
            if index == self.TRANSPARENCY_INDEX:
                continue
            if index < start_index:
                start_index = index
            if index > end_index:
                end_index = index
            indexes.add(index)

        return start_index, end_index, sorted(indexes)

    @property
    def pal_start_index(self) -> int:
        return self.scan_image()[0]

    @property
    def pal_end_index(self) -> int:
        return self.scan_image()[1]

    @property
    def pal_indexes(self) -> list[int]:
        return self.scan_image()[2]

    @property
    def size(self) -> int:
        return len(self.image)

    def decode_image(self) -> RawImage:
        if self.width == 0 or self.height == 0 or len(self.image) == 0:
            return []

        in_size = len(self.image)
        out_size: int = self.width * self.height
        out: RawImage = [self.TRANSPARENCY_INDEX for _ in range(out_size)]

        x: int = 0
        y: int = 0
        i: int = 0
        while i < in_size:
            c: int = self.image[i] + (self.image[i + 1] << 8)
            data, op = divmod(c, 4)
            i += 2

            if op == 0:
                x = data
            elif op == 2:
                y = data
            elif op == 1:
                while data > 0:
                    pos = (y * self.width) + x
                    out[pos] = self.image[i]
                    i += 1
                    x += 1
                    data -= 1
                x = 0
            elif op == 3:
                if i != in_size:
                    raise OMFInvalidDataException("Bad image data!")

        return out

    def save_png(self, filename: str, palette: Palette) -> None:
        dec_data = self.decode_image()
        if not dec_data:
            raise OMFInvalidDataException(
                "Decoded image data resulted in an image of size 0!"
            )
        save_png(
            img=generate_png(dec_data, self.width, self.height, palette),
            filename=filename,
            transparency=self.TRANSPARENCY_INDEX,
        )

    def write(self, parser: BinaryParser) -> None:
        image_len = len(self.image)
        parser.put_uint16(image_len if image_len and not self.missing else 0)
        parser.put_int16(self.pos_x)
        parser.put_int16(self.pos_y)
        parser.put_uint16(self.width)
        parser.put_uint16(self.height)
        parser.put_uint8(self.index)
        parser.put_boolean(self.missing)

        if image_len and not self.missing:
            for m in range(image_len):
                parser.put_uint8(self.image[m])

    def serialize(self) -> dict:
        return {
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "width": self.width,
            "height": self.height,
            "index": self.index,
            "missing": self.missing,
            "image": self.image,
        }

    def unserialize(self, data: dict) -> Sprite:
        self.pos_x = data["pos_x"]
        self.pos_y = data["pos_y"]
        self.width = data["width"]
        self.height = data["height"]
        self.index = data["index"]
        self.missing = data["missing"]
        self.image = data["image"]
        return self

    @property
    def len(self) -> int:
        return len(self.image)
