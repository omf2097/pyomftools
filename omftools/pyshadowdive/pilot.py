import typing

from .protos import DataObject
from .utils.types import Color


class Pilot(DataObject):
    __slots__ = (
        'data',
    )

    def __init__(self):
        self.data: typing.List[Color] = []

    def serialize(self) -> dict:
        return {
            'data': self.data,
        }

    def read(self, parser) -> 'Pilot':
        for m in range(0, 256):
            r = parser.get_uint8()
            g = parser.get_uint8()
            b = parser.get_uint8()
            self.data.append((
                (r << 2) | ((r & 0x30) >> 4),
                (g << 2) | ((g & 0x30) >> 4),
                (b << 2) | ((b & 0x30) >> 4),
            ))
        return self

