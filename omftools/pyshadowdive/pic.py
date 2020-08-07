import typing
from enum import IntEnum
from copy import deepcopy

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
        "has_photo",
        "sprite",
    )

    def __init__(self):
        self.is_player: bool = False
        self.sex: Sex = Sex.MALE
        self.palette: Palette = Palette()
        self.has_photo: bool = True
        self.sprite: Sprite = Sprite()

    def serialize(self):
        return {
            "is_player": self.is_player,
            "sex": self.sex.value,
            "palette": self.palette.serialize(),
            "has_photo": self.has_photo,
            "sprite": self.sprite.serialize(),
        }

    def read(self, parser):
        self.is_player = parser.get_uint8() > 0
        self.sex = Sex(parser.get_uint16())
        self.palette = Palette().read_range(parser, 0, 48)
        self.has_photo = parser.get_boolean()
        if self.has_photo:
            self.sprite = Sprite().read(parser)
            self.sprite.width += 1  # Fix bug
            self.sprite.height += 1  # Fix bug
        return self

    def write(self, parser):
        parser.put_uint8(self.is_player)
        parser.put_uint16(self.sex.value)
        self.palette.write_range(parser, 0, 48)
        parser.put_boolean(self.has_photo)
        if self.has_photo:
            new: Sprite = deepcopy(self.sprite)
            new.width -= 1
            new.height -= 1
            new.write(parser)


class PicFile(Entrypoint):
    __slots__ = ("photos",)

    def __init__(self):
        self.photos: typing.List[Photo] = []

    def serialize(self):
        return {
            "photos": [p.serialize() for p in self.photos],
        }

    def read(self, parser):
        photo_count = parser.get_uint32()
        assert 0 <= photo_count <= 256

        parser.set_pos(200)
        offsets = [parser.get_uint32() for _ in range(photo_count)]

        self.photos = []
        for offset in offsets:
            parser.set_pos(offset)
            self.photos.append(Photo().read(parser))

        return self

    def write(self, parser):
        photos_count = len(self.photos)
        catalog_offset = 200

        # Initial block from 0 to 200
        parser.put_uint32(photos_count)
        parser.put_padding(catalog_offset - 4)

        # Offset catalog -- Just fill with 0 at first
        for m in range(photos_count):
            parser.put_uint32(0)

        # Actual photo data. Write photo, then fill offset in catalog
        for m, photo in enumerate(self.photos):
            current = parser.get_pos()
            # Write catalog
            parser.set_pos(catalog_offset + m * 4)
            parser.put_uint32(current)
            # Write data
            parser.set_pos(current)
            photo.write(parser)
