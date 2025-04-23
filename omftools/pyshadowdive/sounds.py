from __future__ import annotations

from .protos import Entrypoint, DataObject
from .utils.audio import save_wav
from .utils.parser import BinaryParser


class Sound(DataObject):
    __slots__ = ("data", "frequency")

    def __init__(self) -> None:
        self.data: list[int] = []
        self.frequency: int = 0

    def serialize(self) -> dict:
        return {
            "frequency": self.frequency,
            "data": self.data,
        }

    def read(self, parser: BinaryParser) -> Sound:
        length = parser.get_uint16()
        if length > 0:
            self.frequency = parser.get_uint8()
            self.data = [parser.get_uint8() for _ in range(length)]
        else:
            self.frequency = 0
            self.data = []

        return self

    @property
    def real_frequency(self) -> int:
        return int(1000000 / (256 - self.frequency))

    @real_frequency.setter
    def real_frequency(self, value: int) -> None:
        self.frequency = int(256 - (1000000 / value))

    def save_wav(self, filename: str):
        save_wav(self.data, filename)


class SoundFile(Entrypoint):
    __slots__ = ("sounds",)

    def __init__(self) -> None:
        self.sounds: list[Sound] = []

    def serialize(self) -> dict:
        return {
            "sounds": [s.serialize() for s in self.sounds],
        }

    def read(self, parser: BinaryParser) -> SoundFile:
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
