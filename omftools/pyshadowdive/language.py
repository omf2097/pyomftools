from __future__ import annotations
import typing

from .protos import Entrypoint
from .utils.parser import BinaryParser


class LanguageFile(Entrypoint):
    __slots__ = (
        "titles",
        "strings",
    )

    def __init__(self) -> None:
        self.titles: list[str] = []
        self.strings: list[str] = []

    def serialize(self) -> dict:
        return {
            "titles": self.titles,
            "strings": self.strings,
        }

    def read(self, parser: BinaryParser) -> LanguageFile:
        file_size = parser.get_file_size()

        # Read titles and offsets
        offsets: list[int] = []
        while True:
            offset = parser.get_uint32()
            if offset >= file_size:
                break
            offsets.append(offset)
            self.titles.append(parser.get_null_padded_str(32))
        offsets.append(file_size)

        for m in range(len(offsets) - 1):
            block_size = offsets[m + 1] - offsets[m]
            parser.set_pos(offsets[m])
            parser.set_xor_key(block_size & 0xFF)
            self.strings.append(parser.get_null_padded_str(block_size))

        return self
