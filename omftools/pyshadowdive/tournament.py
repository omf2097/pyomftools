from __future__ import annotations
import typing

from .protos import Entrypoint
from .sprite import Sprite
from .palette import Palette
from .pilot import Pilot
from .utils.parser import BinaryParser


class TournamentFile(Entrypoint):
    MAX_ENEMIES: typing.Final[int] = 256
    MAX_LOCALES: typing.Final[int] = 10

    __slots__ = (
        "bk_name",
        "winnings_multiplier",
        "unknown_a",
        "unknown_b",
        "registration_fee",
        "assumed_initial_value",
        "tournament_id",
        "pic_filename",
        "locale_logos",
        "locale_descriptions",
        "locale_titles",
        "locale_end_texts",
        "palette",
        "pilots",
    )

    def __init__(self) -> None:
        self.bk_name: str = ""
        self.winnings_multiplier: float = 0.0
        self.unknown_a: int = 0
        self.unknown_b: int = 0
        self.registration_fee: int = 0
        self.assumed_initial_value: int = 0
        self.tournament_id: int = 0
        self.pic_filename: str = ""
        self.palette: Palette = Palette()
        self.locale_logos: list[Sprite] = []
        self.locale_descriptions: list[str] = []
        self.locale_titles: list[str] = []
        self.locale_end_texts: list[list[list[str]]] = []
        self.pilots: list[Pilot] = []

    def serialize(self) -> dict:
        return {
            "bk_name": self.bk_name,
            "winnings_multiplier": self.winnings_multiplier,
            "unknown_a": self.unknown_a,
            "unknonw_b": self.unknown_b,
            "registration_fee": self.registration_fee,
            "assumed_initial_value": self.assumed_initial_value,
            "tournament_id": self.tournament_id,
            "pic_filename": self.pic_filename,
            "locale_logos": [logo.serialize() for logo in self.locale_logos],
            "locale_descriptions": self.locale_descriptions,
            "locale_titles": self.locale_titles,
            "locale_end_texts": self.locale_end_texts,
            "palette": self.palette.serialize(),
            "pilots": [p.serialize() for p in self.pilots],
        }

    def read(self, parser: BinaryParser) -> TournamentFile:
        enemy_count = parser.get_uint16()
        unknown_b = parser.get_uint16()
        victory_text_offset = parser.get_uint32()

        self.unknown_b = unknown_b
        self.bk_name = parser.get_null_padded_str(14)
        self.winnings_multiplier = parser.get_float()
        self.unknown_a = parser.get_uint32()
        self.registration_fee = parser.get_uint32()
        self.assumed_initial_value = parser.get_uint32()
        self.tournament_id = parser.get_uint32()

        # Enemy block offsets
        parser.set_pos(300)
        offsets = [parser.get_uint32() for _ in range(enemy_count + 1)]

        # Enemy data
        for m in range(enemy_count):
            parser.set_pos(offsets[m])
            self.pilots.append(Pilot().read(parser))

        # Seek to locales
        parser.set_pos(offsets[enemy_count])

        # Load logo sprites
        self.locale_logos = [Sprite().read(parser) for _ in range(self.MAX_LOCALES)]

        # Tournament palette
        self.palette = Palette().read_range(parser, 128, 40)

        # Tournament PIC file name
        self.pic_filename = parser.get_var_str(size_includes_zero=True)

        # Locale texts
        for m in range(self.MAX_LOCALES):
            self.locale_titles.append(parser.get_var_str(size_includes_zero=True))
            self.locale_descriptions.append(parser.get_var_str(size_includes_zero=True))

        # Seek to victory texts
        parser.set_pos(victory_text_offset)

        # Get all end text pages for all pilots for all locales
        for t in range(self.MAX_LOCALES):
            pilots = []
            for h in range(11):
                pilots.append(
                    [parser.get_var_str(size_includes_zero=True) for _ in range(10)]
                )
            self.locale_end_texts.append(pilots)

        return self
