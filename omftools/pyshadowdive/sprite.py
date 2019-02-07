from validx import Dict, Bool, List

from .protos import DataObject
from .utils.validator import UInt16, Int16, UInt8
from .utils.types import Image


class Sprite(DataObject):
    __slots__ = (
        'pos_x',
        'pos_y',
        'width',
        'height',
        'index',
        'missing',
        'image',
    )

    schema = Dict({
        'pos_x': Int16,
        'pos_y': Int16,
        'width': UInt16,
        'height': UInt16,
        'index': UInt8,
        'missing': Bool(),
        'image': List(UInt8, maxlen=65535)
    })

    def __init__(self):
        self.pos_x: int = 0
        self.pos_y: int = 0
        self.index: int = 0
        self.missing: bool = False
        self.width: int = 0
        self.height: int = 0
        self.image: Image = []

    def read(self, parser):
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

    def write(self, parser):
        image_len = len(self.image)
        parser.put_uint16(image_len)
        parser.put_int16(self.pos_x)
        parser.put_int16(self.pos_y)
        parser.put_uint16(self.width)
        parser.put_uint16(self.height)
        parser.put_uint8(self.index)
        parser.put_boolean(self.missing)

        if image_len and not self.missing:
            for m in range(image_len):
                parser.put_uint8(self.image[m])

    def serialize(self):
        return {
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'width': self.width,
            'height': self.height,
            'index': self.index,
            'missing': self.missing,
            'image': self.image,
        }

    def unserialize(self, data):
        self.pos_x = data['pos_x']
        self.pos_y = data['pos_y']
        self.width = data['width']
        self.height = data['height']
        self.index = data['index']
        self.missing = data['missing']
        self.image = data['image']
        return self

    @property
    def len(self) -> int:
        return len(self.image)
