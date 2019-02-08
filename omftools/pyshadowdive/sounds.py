import typing

from .protos import Entrypoint, DataObject
from .utils.audio import save_wav


class Sound(DataObject):
    __slots__ = ('data', 'unknown')

    def __init__(self):
        self.data: typing.List[int] = []
        self.unknown: int = 0

    def serialize(self):
        return {
            'unknown': self.unknown,
            'data': self.data,
        }

    def read(self, parser):
        length = parser.get_uint16()
        if length > 0:
            self.unknown = parser.get_uint8()
            self.data = [parser.get_uint8() for _ in range(length)]
        else:
            self.unknown = 0
            self.data = []

        return self

    def save_wav(self, filename: str):
        save_wav(self.data, filename)


class SoundFile(Entrypoint):
    __slots__ = (
        'sounds',
    )

    def __init__(self):
        self.sounds: typing.List[Sound] = []

    def serialize(self):
        return {
            'sounds': [s.serialize() for s in self.sounds],
        }

    def read(self, parser):
        first = parser.get_uint32()
        assert first == 0

        header_size = parser.get_uint32()
        block_count, remainder = divmod(header_size, 4)
        assert remainder == 0
        block_count = block_count - 2

        # Skip offsets
        offsets = [1200]
        for m in range(block_count):
            offsets.append(parser.get_uint32())

        self.sounds = []
        for m in range(block_count):
            assert parser.get_pos() == offsets[m]
            self.sounds.append(Sound().read(parser))

        return self
