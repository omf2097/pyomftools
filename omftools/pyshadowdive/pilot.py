from __future__ import annotations
import typing
from enum import IntEnum

from .protos import DataObject
from .palette import Palette
from .utils.parser import BinaryParser


class Har(IntEnum):
    JAGUAR = 0
    SHADOW = 1
    THORN = 2
    PYROS = 3
    ELECTRA = 4
    KATANA = 5
    SHREDDER = 6
    FLAIL = 7
    GARGOYLE = 8
    CHRONOS = 9
    NOVA = 10
    RANDOM = 255


class Difficulty(IntEnum):
    ALUMINUM = 0
    IRON = 1
    STEEL = 2
    HEAVY_METAL = 3


class Pilot(DataObject):
    PILOT_BLOCK_LENGTH: typing.Final[int] = 428

    PILOT_GROUP: typing.Final[tuple] = (
        "unknown_a",
        "name",
        "wins",
        "losses",
        "rank",
        "har_id",
        "arm_power",
        "leg_power",
        "arm_speed",
        "leg_speed",
        "armor",
        "stun_resistance",
        "power",
        "agility",
        "endurance",
        "offense",
        "defense",
        "money",
        "color_1",
        "color_2",
        "color_3",
    )

    TOURNAMENT_GROUP: typing.Final[tuple] = (
        "trn_name",
        "trn_desc",
        "trn_image",
        "unk_f_c",
        "unk_f_d",
        "pilot_id",
        "unknown_k",
        "force_arena",
        "difficulty",
        "unk_block_b",
        "movement",
        "unk_block_c",
    )

    ENHANCEMENTS_GROUP: typing.Final[tuple] = ("enhancements",)

    REQUIREMENTS_GROUP: typing.Final[tuple] = (
        "secret",
        "only_fight_once",
        "req_enemy",
        "req_difficulty",
        "req_rank",
        "req_vitality",
        "req_fighter",
        "req_accuracy",
        "req_avg_dmg",
        "req_max_rank",
        "req_scrap",
        "req_destroy",
    )

    AI_OPTS_GROUP: typing.Final[tuple] = (
        "att_normal",
        "att_hyper",
        "att_jump",
        "att_def",
        "att_sniper",
        "unk_block_d",
        "ap_throw",
        "ap_special",
        "ap_jump",
        "ap_high",
        "ap_low",
        "ap_middle",
        "pref_jump",
        "pref_fwd",
        "pref_back",
        "unknown_e",
        "learning",
        "forget",
    )

    OTHER_GROUP: typing.Final[tuple] = (
        "unk_block_f",
        "enemies_inc_unranked",
        "enemies_ex_unranked",
        "unk_d_a",
        "unk_d_b",
        "winnings",
        "total_value",
        "unk_f_a",
        "unk_f_b",
        "unk_block_i",
        "photo_id",
    )

    QUOTES_BLOCK: typing.Final[tuple] = ("quotes",)

    __slots__ = (
        "unknown_a",
        "name",
        "wins",
        "losses",
        "rank",
        "har_id",
        "arm_power",
        "leg_power",
        "arm_speed",
        "leg_speed",
        "armor",
        "stun_resistance",
        "power",
        "agility",
        "endurance",
        "offense",
        "defense",
        "money",
        "color_1",
        "color_2",
        "color_3",
        "trn_name",
        "trn_desc",
        "trn_image",
        "unk_f_c",
        "unk_f_d",
        "pilot_id",
        "unknown_k",
        "force_arena",
        "difficulty",
        "unk_block_b",
        "movement",
        "unk_block_c",
        "enhancements",
        "secret",
        "only_fight_once",
        "req_enemy",
        "req_difficulty",
        "req_rank",
        "req_vitality",
        "req_fighter",
        "req_accuracy",
        "req_avg_dmg",
        "req_max_rank",
        "req_scrap",
        "req_destroy",
        "att_normal",
        "att_hyper",
        "att_jump",
        "att_def",
        "att_sniper",
        "unk_block_d",
        "ap_throw",
        "ap_special",
        "ap_jump",
        "ap_high",
        "ap_low",
        "ap_middle",
        "pref_jump",
        "pref_fwd",
        "pref_back",
        "unknown_e",
        "learning",
        "forget",
        "unk_block_f",
        "enemies_inc_unranked",
        "enemies_ex_unranked",
        "unk_d_a",
        "unk_d_b",
        "winnings",
        "total_value",
        "unk_f_a",
        "unk_f_b",
        "palette",
        "unk_block_i",
        "photo_id",
        "quotes",
    )

    def __init__(self) -> None:
        self.unknown_a: int = 0  # uint32_t
        self.name: str = ""  # char
        self.wins: int = 0  # uint16_t
        self.losses: int = 0  # uint16_t
        self.rank: int = 0  # uint8_t
        self.har_id: Har = Har.JAGUAR  # uint8_t
        self.arm_power: int = 0  # uint8_t
        self.leg_power: int = 0  # uint8_t
        self.arm_speed: int = 0  # uint8_t
        self.leg_speed: int = 0  # uint8_t
        self.armor: int = 0  # uint8_t
        self.stun_resistance: int = 0  # uint8_t
        self.power: int = 0  # uint8_t
        self.agility: int = 0  # uint8_t
        self.endurance: int = 0  # uint8_t
        self.offense: int = 0  # uint16_t
        self.defense: int = 0  # uint16_t
        self.money: int = 0  # uint32_t
        self.color_1: int = 0  # uint8_t
        self.color_2: int = 0  # uint8_t
        self.color_3: int = 0  # uint8_t

        self.trn_name: str = ""  # char
        self.trn_desc: str = ""  # char
        self.trn_image: str = ""  # char
        self.unk_f_c: float = 0.0  # float
        self.unk_f_d: float = 0.0  # float
        self.pilot_id: int = 0  # uint8_t
        self.unknown_k: int = 0  # uint8_t
        self.force_arena: int = 0  # uint16_t
        self.difficulty: Difficulty = Difficulty.ALUMINUM  # uint8_t
        self.unk_block_b: list[int] = []  # char
        self.movement: int = 0  # uint8_t
        self.unk_block_c: list[int] = []  # uint16_t
        self.enhancements: list[int] = []  # char

        self.secret: int = 0  # uint8_t
        self.only_fight_once: int = 0  # uint8_t
        self.req_enemy: int = 0  # uint8_t
        self.req_difficulty: int = 0  # uint8_t
        self.req_rank: int = 0  # uint8_t
        self.req_vitality: int = 0  # uint8_t
        self.req_fighter: int = 0  # uint8_t
        self.req_accuracy: int = 0  # uint8_t
        self.req_avg_dmg: int = 0  # uint8_t
        self.req_max_rank: int = 0  # uint8_t
        self.req_scrap: int = 0  # uint8_t
        self.req_destroy: int = 0  # uint8_t

        self.att_normal: int = 0  # uint8_t
        self.att_hyper: int = 0  # uint8_t
        self.att_jump: int = 0  # uint8_t
        self.att_def: int = 0  # uint8_t
        self.att_sniper: int = 0  # uint8_t

        self.unk_block_d: list[int] = []  # uint16_t
        self.ap_throw: int = 0  # int16_t
        self.ap_special: int = 0  # int16_t
        self.ap_jump: int = 0  # int16_t
        self.ap_high: int = 0  # int16_t
        self.ap_low: int = 0  # int16_t
        self.ap_middle: int = 0  # int16_t
        self.pref_jump: int = 0  # int16_t
        self.pref_fwd: int = 0  # int16_t
        self.pref_back: int = 0  # int16_t
        self.unknown_e: int = 0  # uint32_t
        self.learning: float = 0.0  # float
        self.forget: float = 0.0  # float
        self.unk_block_f: list[int] = []  # char
        self.enemies_inc_unranked: int = 0  # uint16_t
        self.enemies_ex_unranked: int = 0  # uint16_t

        self.unk_d_a: int = 0  # uint16_t
        self.unk_d_b: int = 0  # uint32_t

        self.winnings: int = 0  # uint32_t
        self.total_value: int = 0  # uint32_t
        self.unk_f_a: float = 0.0  # float
        self.unk_f_b: float = 0.0  # float
        self.palette: Palette = Palette()  # sd_palette
        self.unk_block_i: int = 0  # uint16_t
        self.photo_id: int = 0  # uint16_t

        self.quotes: list[str] = []

    def serialize(self) -> dict:
        return {
            "unknown_a": self.unknown_a,
            "name": self.name,
            "wins": self.wins,
            "losses": self.losses,
            "rank": self.rank,
            "har_id": self.har_id.value,
            "arm_power": self.arm_power,
            "leg_power": self.leg_power,
            "arm_speed": self.arm_speed,
            "leg_speed": self.leg_speed,
            "armor": self.armor,
            "stun_resistance": self.stun_resistance,
            "power": self.power,
            "agility": self.agility,
            "endurance": self.endurance,
            "offense": self.offense,
            "defense": self.defense,
            "money": self.money,
            "color_1": self.color_1,
            "color_2": self.color_2,
            "color_3": self.color_3,
            "trn_name": self.trn_name,
            "trn_desc": self.trn_desc,
            "trn_image": self.trn_image,
            "unk_f_c": self.unk_f_c,
            "unk_f_d": self.unk_f_d,
            "pilot_id": self.pilot_id,
            "unknown_k": self.unknown_k,
            "force_arena": self.force_arena,
            "difficulty": self.difficulty.value,
            "unk_block_b": self.unk_block_b,
            "movement": self.movement,
            "unk_block_c": self.unk_block_c,
            "enhancements": self.enhancements,
            "secret": self.secret,
            "only_fight_once": self.only_fight_once,
            "req_enemy": self.req_enemy,
            "req_difficulty": self.req_difficulty,
            "req_rank": self.req_rank,
            "req_vitality": self.req_vitality,
            "req_fighter": self.req_fighter,
            "req_accuracy": self.req_accuracy,
            "req_avg_dmg": self.req_avg_dmg,
            "req_max_rank": self.req_max_rank,
            "req_scrap": self.req_scrap,
            "req_destroy": self.req_destroy,
            "att_normal": self.att_normal,
            "att_hyper": self.att_hyper,
            "att_jump": self.att_jump,
            "att_def": self.att_def,
            "att_sniper": self.att_sniper,
            "unk_block_d": self.unk_block_d,
            "ap_throw": self.ap_throw,
            "ap_special": self.ap_special,
            "ap_jump": self.ap_jump,
            "ap_high": self.ap_high,
            "ap_low": self.ap_low,
            "ap_middle": self.ap_middle,
            "pref_jump": self.pref_jump,
            "pref_fwd": self.pref_fwd,
            "pref_back": self.pref_back,
            "unknown_e": self.unknown_e,
            "learning": self.learning,
            "forget": self.forget,
            "unk_block_f": self.unk_block_f,
            "enemies_inc_unranked": self.enemies_inc_unranked,
            "enemies_ex_unranked": self.enemies_ex_unranked,
            "unk_d_a": self.unk_d_a,
            "unk_d_b": self.unk_d_b,
            "winnings": self.winnings,
            "total_value": self.total_value,
            "unk_f_a": self.unk_f_a,
            "unk_f_b": self.unk_f_b,
            "palette": self.palette,
            "unk_block_i": self.unk_block_i,
            "photo_id": self.photo_id,
            "quotes": self.quotes,
        }

    def read_player_block(self, parser: BinaryParser) -> None:
        self.name = parser.get_null_padded_str(18)
        self.wins = parser.get_uint16()
        self.losses = parser.get_uint16()
        self.rank = parser.get_uint8()
        self.har_id = Har(parser.get_uint8())

        stats_a = parser.get_uint16()
        stats_b = parser.get_uint16()
        stats_c = parser.get_uint16()
        stats_d = parser.get_uint8()

        self.arm_power = (stats_a >> 0) & 0x1F
        self.leg_power = (stats_a >> 5) & 0x1F
        self.arm_speed = (stats_a >> 10) & 0x1F
        self.leg_speed = (stats_b >> 0) & 0x1F
        self.armor = (stats_b >> 5) & 0x1F
        self.stun_resistance = (stats_b >> 10) & 0x1F
        self.agility = (stats_c >> 0) & 0x7F
        self.power = (stats_c >> 7) & 0x7F
        self.endurance = (stats_d >> 0) & 0x7F
        parser.skip(1)  # Nothing useful here

        self.offense = parser.get_uint16()
        self.defense = parser.get_uint16()
        self.money = parser.get_uint32()
        self.color_1 = parser.get_uint8()
        self.color_2 = parser.get_uint8()
        self.color_3 = parser.get_uint8()

    def read_pilot_block(self, parser: BinaryParser) -> None:
        self.trn_name = parser.get_null_padded_str(13)
        self.trn_desc = parser.get_null_padded_str(31)
        self.trn_image = parser.get_null_padded_str(13)

        self.unk_f_c = parser.get_float()
        self.unk_f_d = parser.get_float()
        parser.skip(40)
        self.pilot_id = parser.get_uint8()
        self.unknown_k = parser.get_uint8()
        self.force_arena = parser.get_uint16()
        self.difficulty = Difficulty((parser.get_uint8() >> 3) & 0x3)
        self.unk_block_b = [parser.get_uint8() for _ in range(2)]
        self.movement = parser.get_uint8()
        self.unk_block_c = [parser.get_uint16() for _ in range(3)]

        self.enhancements = [parser.get_uint8() for _ in range(11)]

        parser.skip(1)  # Nothing here
        flags = parser.get_uint8()
        self.secret = bool(flags & 0x02)
        self.only_fight_once = bool(flags & 0x08)
        parser.skip(1)  # Nothing here either

        reqs = [parser.get_uint16() for _ in range(5)]
        self.req_rank = reqs[0] & 0xFF
        self.req_max_rank = (reqs[0] >> 8) & 0xFF
        self.req_fighter = reqs[1] & 0x1F
        self.req_difficulty = (reqs[2] >> 8) & 0x0F
        self.req_enemy = reqs[2] & 0xFF
        self.req_vitality = reqs[3] & 0x7F
        self.req_accuracy = (reqs[3] >> 7) & 0x7F
        self.req_avg_dmg = reqs[4] & 0x7F
        self.req_scrap = bool(reqs[4] & 0x80)
        self.req_destroy = bool((reqs[4] >> 8) & 0x01)

        att = [parser.get_uint16() for _ in range(3)]
        self.att_normal = (att[0] >> 4) & 0x7F
        self.att_hyper = att[1] & 0x7F
        self.att_jump = (att[1] >> 7) & 0x7F
        self.att_def = att[2] & 0x7F
        self.att_sniper = (att[2] >> 7) & 0x7F

        self.unk_block_d = [parser.get_uint16() for _ in range(3)]

        self.ap_throw = parser.get_int16()
        self.ap_special = parser.get_int16()
        self.ap_jump = parser.get_int16()
        self.ap_high = parser.get_int16()
        self.ap_low = parser.get_int16()
        self.ap_middle = parser.get_int16()
        self.pref_jump = parser.get_int16()
        self.pref_fwd = parser.get_int16()
        self.pref_back = parser.get_int16()

        self.unknown_e = parser.get_uint32()
        self.learning = parser.get_float()
        self.forget = parser.get_float()

        self.unk_block_f = [parser.get_uint8() for _ in range(14)]

        self.enemies_inc_unranked = parser.get_uint16()
        self.enemies_ex_unranked = parser.get_uint16()
        self.unk_d_a = parser.get_uint16()
        self.unk_d_b = parser.get_uint32()
        self.winnings = parser.get_uint32()
        self.total_value = parser.get_uint32()

        self.unk_f_a = parser.get_float()
        self.unk_f_b = parser.get_float()
        parser.skip(8)

        self.palette = Palette().read_range(parser, 0, 48)

        self.unk_block_i = parser.get_uint16()
        self.photo_id = parser.get_uint16() & 0x3FF

    def read(self, parser: BinaryParser) -> Pilot:
        parser.set_xor_key(self.PILOT_BLOCK_LENGTH & 0xFF)
        self.unknown_a = parser.get_uint32()
        self.read_player_block(parser)
        self.read_pilot_block(parser)
        parser.set_xor_key(None)
        self.quotes = [parser.get_var_str(size_includes_zero=True) for _ in range(10)]
        return self
