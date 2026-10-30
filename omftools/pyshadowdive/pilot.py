from __future__ import annotations
import typing
from enum import IntEnum

from .protos import DataObject
from .palette import Palette
from .pic import Sex
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

    def __str__(self) -> str:
        return "{} ({})".format(self.name, self.value)


class Difficulty(IntEnum):
    ALUMINUM = 0
    IRON = 1
    STEEL = 2
    HEAVY_METAL = 3

    def get_hint(self) -> typing.Optional[str]:
        match self:
            case Difficulty.ALUMINUM:
                return (
                    "Easy. Score multiplier 50; opponents' offense / defense quartered "
                    "(min 10); AI ratings capped at 39 / 35."
                )
            case Difficulty.IRON:
                return (
                    "Medium. Score multiplier 100; opponents' offense / defense x2/3 "
                    "(min 20); AI ratings capped at 70 / 70."
                )
            case Difficulty.STEEL:
                return (
                    "Hard. Score multiplier 150; opponents' offense / defense x3/2 (min"
                    " 35); AI ratings capped at 120 / 120."
                )
            case Difficulty.HEAVY_METAL:
                return (
                    "Hardest. Score multiplier 200; opponents' offense / defense x2 + "
                    "10 (min 65); AI ratings capped at 240 / 240."
                )
            case _:
                return None

    def __str__(self) -> str:
        return "{} ({})".format(self.name, self.value)


class PilotPhoto(DataObject):

    __slots__ = ("palette", "is_player", "photo_id", "sex")

    def __init__(self) -> None:
        self.palette: Palette = Palette()
        self.is_player: int = 0  # int16
        self.photo_id: int = 0  # low 10 bits of char_sex (PHOTOS.DAT index)
        self.sex: Sex = Sex.MALE  # bits 10-11 of char_sex

    def get_hint(self, attr: str) -> typing.Optional[str]:
        match attr:
            case "photo_id":
                return (
                    "Index of the pilot portrait in PHOTOS.DAT (low 10 bits of a packed"
                    " field)."
                )
            case "sex":
                return (
                    "Bits 10-11 of the packed field. Copied into the pilot when it is "
                    "loaded and used by the newsroom to pick his/her, him/her and "
                    "he/she."
                )
            case _:
                return super().get_hint(attr)

    def serialize(self) -> dict:
        return {
            "palette": self.palette.serialize(),
            "is_player": self.is_player,
            "photo_id": self.photo_id,
            "sex": self.sex.value,
        }

    def read(self, parser: BinaryParser) -> "PilotPhoto":
        self.palette = Palette().read_range(parser, 0, 48)  # photo.palette (144 B)
        self.is_player = parser.get_int16()  # photo.is_player
        # photo.char_sex packs photo_id in bits 0-9 and sex in bits 10-11.
        char_sex = parser.get_uint16()
        self.photo_id = char_sex & 0x3FF
        self.sex = Sex((char_sex >> 10) & 0x3)
        return self


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
        "winnings_scale",
        "winnings_multiplier",
        "pilot_id",
        "unknown_k",
        "force_arena",
        "hazard_death",
        "scrapped",
        "destroyed",
        "difficulty",
        "unknown_9c",
        "unk_block_b",
        "can_move",
        "movement",
        "fight_damage",
        "fight_hits",
        "fight_moves",
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
        "req_arena",
        "req_accuracy",
        "req_win_ratio",
        "req_avg_dmg",
        "req_max_rank",
        "req_scrap",
        "req_destroy",
    )

    AI_OPTS_GROUP: typing.Final[tuple] = (
        "att_personality",
        "att_normal",
        "att_hyper",
        "att_jump",
        "att_def",
        "att_sniper",
        "unk_block_d",
        "ap_close",
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
        "sound_1",
        "sound_2",
        "sound_3",
        "unk_block_f",
        "enemies_inc_unranked",
        "enemies_ex_unranked",
        "unk_d_a",
        "unk_d_b",
        "winnings",
        "total_value",
        "current_health",
        "maximum_health",
        "last_pos_x",
        "last_pos_y",
        # `photo` (PilotPhoto) is rendered as its own cards in trn_index.html.
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
        "winnings_scale",
        "winnings_multiplier",
        "pilot_id",
        "unknown_k",
        "force_arena",
        "hazard_death",
        "scrapped",
        "destroyed",
        "difficulty",
        "unknown_9c",
        "unk_block_b",
        "can_move",
        "movement",
        "fight_damage",
        "fight_hits",
        "fight_moves",
        "enhancements",
        "secret",
        "only_fight_once",
        "req_enemy",
        "req_difficulty",
        "req_rank",
        "req_vitality",
        "req_fighter",
        "req_arena",
        "req_accuracy",
        "req_win_ratio",
        "req_avg_dmg",
        "req_max_rank",
        "req_scrap",
        "req_destroy",
        "att_personality",
        "att_normal",
        "att_hyper",
        "att_jump",
        "att_def",
        "att_sniper",
        "unk_block_d",
        "ap_close",
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
        "sound_1",
        "sound_2",
        "sound_3",
        "unk_block_f",
        "enemies_inc_unranked",
        "enemies_ex_unranked",
        "unk_d_a",
        "unk_d_b",
        "winnings",
        "total_value",
        "current_health",
        "maximum_health",
        "last_pos_x",
        "last_pos_y",
        "photo",
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
        self.winnings_scale: float = 0.0  # float
        self.winnings_multiplier: float = 0.0  # float
        self.pilot_id: int = 0  # uint8_t
        self.unknown_k: int = 0  # uint8_t
        self.force_arena: int = 0  # bits 1-6
        self.hazard_death: bool = False  # bit 8
        self.scrapped: bool = False  # bit 9
        self.destroyed: bool = False  # bit 10
        self.difficulty: Difficulty = Difficulty.ALUMINUM  # bits 11-13
        self.unknown_9c: int = 0  # uint8_t
        self.unk_block_b: list[int] = []  # 2 x uint8_t
        self.can_move: bool = False
        self.movement: int = 0  # uint8_t, raw
        self.fight_damage: int = 0  # & 0xFFF
        self.fight_hits: int = 0  # & 0x1FF
        self.fight_moves: int = 0  # & 0xFFF
        self.enhancements: list[int] = []  # char

        self.secret: int = 0  # uint8_t
        self.only_fight_once: int = 0  # uint8_t
        self.req_enemy: int = 0  # uint8_t
        self.req_difficulty: int = 0  # uint8_t
        self.req_rank: int = 0  # uint8_t
        self.req_vitality: int = 0  # uint8_t
        self.req_fighter: int = 0  # uint8_t
        self.req_arena: int = 0  # uint8_t
        self.req_accuracy: int = 0  # uint8_t
        self.req_win_ratio: int = 0  # uint8_t
        self.req_avg_dmg: int = 0  # uint8_t
        self.req_max_rank: int = 0  # uint8_t
        self.req_scrap: int = 0  # uint8_t
        self.req_destroy: int = 0  # uint8_t

        self.att_personality: int = 0  # uint8_t
        self.att_normal: int = 0  # uint8_t
        self.att_hyper: int = 0  # uint8_t
        self.att_jump: int = 0  # uint8_t
        self.att_def: int = 0  # uint8_t
        self.att_sniper: int = 0  # uint8_t

        self.unk_block_d: list[int] = ([])  # uint16_t × 2
        self.ap_close: int = 0  # int16_t
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
        self.sound_1: int = 0  # int16_t
        self.sound_2: int = 0  # int16_t
        self.sound_3: int = 0  # int16_t
        self.unk_block_f: list[int] = []  # uint16_t × 4
        self.enemies_inc_unranked: int = 0  # uint16_t
        self.enemies_ex_unranked: int = 0  # uint16_t

        self.unk_d_a: int = 0  # uint16_t
        self.unk_d_b: int = 0  # uint32_t

        self.winnings: int = 0  # uint32_t
        self.total_value: int = 0  # uint32_t
        self.current_health: int = 0  # int16_t
        self.maximum_health: int = 0  # int16_t
        self.last_pos_x: int = 0  # int16_t
        self.last_pos_y: int = 0  # int16_t
        self.photo: PilotPhoto = PilotPhoto()

        self.quotes: list[str] = []

    def get_hint(self, attr: str) -> typing.Optional[str]:
        match attr:
            case "winnings_scale":
                return (
                    "Set when a tournament pilot is created; scales the per-rank prize "
                    "bonus paid for a tournament win."
                )
            case "winnings_multiplier":
                return (
                    "Copied from the tournament's TRN header when the pilot is created;"
                    " multiplies every tournament prize."
                )
            case "force_arena":
                return (
                    "Arena forced for fights against this pilot: 0 = random, otherwise "
                    "arena index + 1. Bits 1-6 of a packed 16-bit field."
                )
            case "hazard_death":
                return (
                    "Died to an arena hazard in the last fight. Bit 8 of the packed "
                    "field; written by the game but never read."
                )
            case "scrapped":
                return "Was scrapped in the current fight. Bit 9 of the packed field."
            case "destroyed":
                return (
                    "Was destroyed in the current fight (destruction also sets "
                    "'scrapped'). Bit 10 of the packed field."
                )
            case "difficulty":
                return (
                    "Tournament difficulty, chosen when the pilot is created. Bits "
                    "11-13 of the packed field."
                )
            case "unknown_9c":
                return "Unused by the game."
            case "unk_block_b":
                return "Unused by the game."
            case "can_move":
                return (
                    "May change place on the tournament ladder when AI pilots fight "
                    "each other. Set on every ranked entry except the champion. Bit 0 "
                    "of 'movement'."
                )
            case "movement":
                return (
                    "Raw byte. Bit 0 = can_move; bits 1-2 = copy of the photo's sex, "
                    "filled in when the pilot is loaded (always 0 in TRN files)."
                )
            case "fight_damage":
                return (
                    "Damage dealt in the last fight, after the pilot-power scaling but "
                    "before arm / leg power and armor. Arena hazard hits are not "
                    "counted. Used for the average-damage requirement and the shop "
                    "report."
                )
            case "fight_hits":
                return "Hits landed in the last fight."
            case "fight_moves":
                return (
                    "Moves started in the last fight; hits / moves is the accuracy used"
                    " by the accuracy requirement."
                )
            case "winnings":
                return (
                    "Prize value of this opponent; feeds the tournament payout when the"
                    " pilot is beaten. The game never adds to it."
                )
            case "last_pos_x":
                return (
                    "HAR x position in pixels when the pilot's last fight ended; the "
                    "newsroom zoom effect starts there."
                )
            case "last_pos_y":
                return (
                    "HAR y position in pixels when the pilot's last fight ended; the "
                    "newsroom zoom effect starts there."
                )
            case "offense":
                return (
                    "AI aggression weight. Together with defense it also sets this "
                    "pilot's strength in the simulated fights between tournament "
                    "opponents."
                )
            case "att_personality":
                return (
                    "Current AI personality code 0-4 (0 normal, 1 hyper, 2 jump, "
                    "3 def, 4 sniper). The game generates it from the five att_* "
                    "chances during fights."
                )
            case "req_win_ratio":
                return (
                    "Minimum wins × 100 / losses for the player before this opponent "
                    "can be fought; 0 = no requirement. Bits 4-10 of the flags word."
                )
            case "req_arena":
                return (
                    "Required arena, bits 5-9 of the second requirement word. The game "
                    "checks it wrongly: when non-zero, the fight is allowed only if the "
                    "arena index equals req_fighter. 0 in every shipped TRN."
                )
            case "defense":
                return (
                    "AI defensiveness weight. Together with offense it also sets this "
                    "pilot's strength in the simulated fights between tournament "
                    "opponents."
                )
            case _:
                return super().get_hint(attr)

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
            "winnings_scale": self.winnings_scale,
            "winnings_multiplier": self.winnings_multiplier,
            "pilot_id": self.pilot_id,
            "unknown_k": self.unknown_k,
            "force_arena": self.force_arena,
            "hazard_death": self.hazard_death,
            "scrapped": self.scrapped,
            "destroyed": self.destroyed,
            "difficulty": self.difficulty.value,
            "unknown_9c": self.unknown_9c,
            "unk_block_b": self.unk_block_b,
            "can_move": self.can_move,
            "movement": self.movement,
            "fight_damage": self.fight_damage,
            "fight_hits": self.fight_hits,
            "fight_moves": self.fight_moves,
            "enhancements": self.enhancements,
            "secret": self.secret,
            "only_fight_once": self.only_fight_once,
            "req_enemy": self.req_enemy,
            "req_difficulty": self.req_difficulty,
            "req_rank": self.req_rank,
            "req_vitality": self.req_vitality,
            "req_fighter": self.req_fighter,
            "req_arena": self.req_arena,
            "req_accuracy": self.req_accuracy,
            "req_win_ratio": self.req_win_ratio,
            "req_avg_dmg": self.req_avg_dmg,
            "req_max_rank": self.req_max_rank,
            "req_scrap": self.req_scrap,
            "req_destroy": self.req_destroy,
            "att_personality": self.att_personality,
            "att_normal": self.att_normal,
            "att_hyper": self.att_hyper,
            "att_jump": self.att_jump,
            "att_def": self.att_def,
            "att_sniper": self.att_sniper,
            "unk_block_d": self.unk_block_d,
            "ap_close": self.ap_close,
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
            "sound_1": self.sound_1,
            "sound_2": self.sound_2,
            "sound_3": self.sound_3,
            "unk_block_f": self.unk_block_f,
            "enemies_inc_unranked": self.enemies_inc_unranked,
            "enemies_ex_unranked": self.enemies_ex_unranked,
            "unk_d_a": self.unk_d_a,
            "unk_d_b": self.unk_d_b,
            "winnings": self.winnings,
            "total_value": self.total_value,
            "current_health": self.current_health,
            "maximum_health": self.maximum_health,
            "last_pos_x": self.last_pos_x,
            "last_pos_y": self.last_pos_y,
            "photo": self.photo.serialize(),
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

        self.winnings_scale = parser.get_float()
        self.winnings_multiplier = parser.get_float()
        parser.skip(40)
        self.pilot_id = parser.get_uint8()
        self.unknown_k = parser.get_uint8()
        packed = parser.get_uint16()
        self.force_arena = (packed >> 1) & 0x3F
        self.hazard_death = bool(packed & 0x100)
        self.scrapped = bool(packed & 0x200)
        self.destroyed = bool(packed & 0x400)
        self.difficulty = Difficulty((packed >> 11) & 0x7)
        self.unknown_9c = parser.get_uint8()
        self.unk_block_b = [parser.get_uint8() for _ in range(2)]
        self.movement = parser.get_uint8()
        self.can_move = bool(self.movement & 0x01)
        self.fight_damage = parser.get_uint16() & 0xFFF
        self.fight_hits = parser.get_uint16() & 0x1FF
        self.fight_moves = parser.get_uint16() & 0xFFF

        self.enhancements = [parser.get_uint8() for _ in range(11)]

        parser.skip(1)  # Nothing here
        flags = parser.get_uint16()
        self.secret = bool(flags & 0x02)
        self.only_fight_once = bool(flags & 0x08)
        self.req_win_ratio = (flags >> 4) & 0x7F

        reqs = [parser.get_uint16() for _ in range(5)]
        self.req_rank = reqs[0] & 0xFF
        self.req_max_rank = (reqs[0] >> 8) & 0xFF
        self.req_fighter = reqs[1] & 0x1F
        self.req_arena = (reqs[1] >> 5) & 0x1F
        self.req_difficulty = (reqs[2] >> 8) & 0x0F
        self.req_enemy = reqs[2] & 0xFF
        self.req_vitality = reqs[3] & 0x7F
        self.req_accuracy = (reqs[3] >> 7) & 0x7F
        self.req_avg_dmg = reqs[4] & 0x7F
        self.req_scrap = bool(reqs[4] & 0x80)
        self.req_destroy = bool((reqs[4] >> 8) & 0x01)

        att = [parser.get_uint16() for _ in range(3)]
        self.att_personality = att[0] & 0x0F
        self.att_normal = (att[0] >> 4) & 0x7F
        self.att_hyper = att[1] & 0x7F
        self.att_jump = (att[1] >> 7) & 0x7F
        self.att_def = att[2] & 0x7F
        self.att_sniper = (att[2] >> 7) & 0x7F

        self.unk_block_d = [parser.get_uint16() for _ in range(2)]
        self.ap_close = parser.get_int16()

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

        self.sound_1 = parser.get_int16()
        self.sound_2 = parser.get_int16()
        self.sound_3 = parser.get_int16()
        self.unk_block_f = [parser.get_uint16() for _ in range(4)]

        self.enemies_inc_unranked = parser.get_uint16()
        self.enemies_ex_unranked = parser.get_uint16()
        self.unk_d_a = parser.get_uint16()
        self.unk_d_b = parser.get_uint32()
        self.winnings = parser.get_uint32()
        self.total_value = parser.get_uint32()

        self.current_health = parser.get_int16()
        self.maximum_health = parser.get_int16()
        self.last_pos_x = parser.get_int16()
        self.last_pos_y = parser.get_int16()
        parser.skip(8)

        self.photo = PilotPhoto().read(parser)

    def read(self, parser: BinaryParser) -> Pilot:
        parser.set_xor_key(self.PILOT_BLOCK_LENGTH & 0xFF)
        self.unknown_a = parser.get_uint32()
        self.read_player_block(parser)
        self.read_pilot_block(parser)
        parser.set_xor_key(None)
        self.quotes = [parser.get_var_str(size_includes_zero=True) for _ in range(10)]
        return self
