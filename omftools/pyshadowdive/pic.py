import typing
from enum import IntEnum

from .protos import Entrypoint, DataObject
from .sprite import Sprite
from .palette import Palette


class Sex(IntEnum):
    MALE = 0
    FEMALE = 1


class Photo(DataObject):
    __slots__ = (
        "is_player",
        "sex",
        "palette",
        "unknown",
        "sprite",
    )

    def __init__(self):
        self.is_player: bool = False
        self.sex: Sex = 0
        self.palette: Palette = Palette()
        self.unknown: int = 0
        self.sprite: Sprite = Sprite()

    def serialize(self):
        return {
            "is_player": self.is_player,
            "sex": self.sex.value,
            "palette": self.palette.serialize(),
            "unknown": self.unknown,
            "sprite": self.sprite.serialize(),
        }

    def read(self, parser) -> "Photo":
        self.is_player = parser.get_uint8() > 0
        self.sex = Sex(parser.get_uint16())
        self.palette = Palette().read_range(parser, 0, 48)
        self.unknown = parser.get_uint8()
        self.sprite = Sprite().read(parser)
        self.sprite.width += 1  # Fix bug
        self.sprite.height += 1  # Fix bug
        return self


class PicFile(Entrypoint):
    __slots__ = ("photos",)

    def __init__(self):
        self.photos: typing.List[Photo] = []

    def serialize(self):
        return {
            "photos": [p.serialize() for p in self.photos],
        }

    def read(self, parser) -> "PicFile":
        photo_count = parser.get_uint32()
        assert 0 <= photo_count <= 256

        parser.set_pos(200)
        offsets = [parser.get_uint32() for _ in range(photo_count)]

        self.photos = []
        for offset in offsets:
            parser.set_pos(offset)
            self.photos.append(Photo().read(parser))

        return self
