from __future__ import annotations
import typing
from validx import Dict, Str
from enum import IntFlag, IntEnum

from .animation import Animation
from .utils.parser import BinaryParser
from .utils.validator import UInt8, UInt16


class AIMoveTriggers(IntFlag):
    """AI context bits on an AF move.

    Each bit marks a move as relevant for a specific opponent-state /
    self-state combination.
    """
    NONE = 0
    GND_STATE_1 = 0x0001            # opponent grounded, AI stance 1
    VS_HIGH_OR_IDLE = 0x0002        # opponent attack CAT_HIGH or ANIM_IDLE
    VS_LOW_OR_CROUCH = 0x0004       # opponent attack CAT_LOW or ANIM_CROUCHING
    VS_MEDIUM = 0x0008              # opponent attack CAT_MEDIUM
    VS_PROJECTILE_HIGH = 0x0010     # CAT_PROJECTILE at/above y-threshold (ref: ai_projectile_y_threshold field)
    GND_STATE_2 = 0x0020            # opponent grounded, AI stance 2
    GND_STATE_3 = 0x0040            # opponent grounded, AI stance 3
    GND_STATE_0 = 0x0080            # opponent grounded, AI stance 0
    AIR_STATE_0 = 0x0100            # opponent airborne, AI stance 0
    AIR_STATE_1 = 0x0200            # opponent airborne, AI stance 1
    AIR_STATE_2 = 0x0400            # opponent airborne, AI stance 2
    AIR_STATE_3 = 0x0800            # opponent airborne, AI stance 3
    FLAG_1000 = 0x1000              # unknown — 3 uses in data (Jaguar leap/charge)
    VS_PROJECTILE_LOW = 0x2000      # CAT_PROJECTILE below y-threshold (evade reaction) (ref: ai_projectile_y_threshold field)
    FLAG_4000 = 0x4000              # reserved
    FLAG_8000 = 0x8000              # reserved

    def __str__(self) -> str:
        return "{} ({})".format(self.name, self.value)


class PositionConstraint(IntFlag):
    """Positional / state requirements declared on an AF move.

    Every set bit must be satisfied by the HAR's current state.
    """
    NONE = 0
    WALL = 0x0001                     # HAR near wall (pos_x_shft outside [0x1500, 0x12a00])
    NO_DIST_CHECK = 0x0002            # bypass distance/position gating (chained moves)
    JUMP_WALL_BOUNCE = 0x0004         # signal on target's jump anim: wall-bounce on aerial hit
    IN_ARENA_0 = 0x0008               # require ARENA0 — unused in shipped data
    IN_ARENA_1 = 0x0010               # require ARENA1 — unused
    IN_ARENA_2 = 0x0020               # require ARENA2 — unused
    IN_ARENA_3 = 0x0040               # require ARENA3 (Fire Pit)
    IN_ARENA_4 = 0x0080               # require ARENA4 — unused
    FLAG_100 = 0x0100                 # field_5A never sets this; reserved
    FLAG_200 = 0x0200                 # reserved
    FLAG_400 = 0x0400                 # reserved
    FLAG_800 = 0x0800                 # reserved
    FLAG_1000 = 0x1000                # signal on target anim; never set in shipped data
    FIRE_ICE_ALLOWED = 0x2000         # require can_perform_fire_ice_move global
    OPP_FIRE_ICE_DESTRUCT = 0x4000    # require opponent's pilot.force_arena & 0x400
    FLAG_8000 = 0x8000                # reserved

    def __str__(self) -> str:
        return "{} ({})".format(self.name, self.value)


class ExtraStringSelector(IntEnum):
    NONE = 0

    # Select string by ARM speed or LEG speed value
    ARM_SPEED = 1
    LEG_SPEED = 2

    # The string selector uses the enhancement level but the damage modifier uses arm/leg power
    SPECIAL_ARM = 3
    SPECIAL_LEG = 4

    # I am different.
    SPECIAL = 5

    def __str__(self) -> str:
        return "{} ({})".format(self.name, self.value)


class MoveCategory(IntEnum):
    """ Animation/move category """
    MISCELLANEOUS = 0
    UNKNOWN_1 = 1
    CLOSE = 2
    UNKNOWN_3 = 3
    LOW = 4
    MEDIUM = 5
    HIGH = 6
    JUMPING = 7
    PROJECTILE = 8
    BASIC = 9
    BK_HAZARD = 10
    VICTORY = 11
    SCRAP = 12
    DESTRUCTION = 13

    def __str__(self) -> str:
        return "{} ({})".format(self.name, self.value)


AF_ANIMATION_NAMES: typing.Final[dict[int, str]] = {
    1: "Jumping",
    2: "Getting up",
    3: "Stunned",
    4: "Crouching",
    5: "Standing block",
    6: "Crouching block",
    7: "Burning oil",
    8: "Blocking scrape",
    9: "Damage",
    10: "Walking",
    11: "Idle",
    12: "Scrap",
    13: "Bolt",
    14: "Screw",
    48: "Victory",
    49: "Loss",
}


class AFMove(Animation):
    __slots__ = (
        "ai_flags",
        "pos_constraint",
        "unknown_4",
        "unknown_5",
        "unknown_6",
        "unknown_7",
        "unknown_8",
        "unknown_9",
        "unknown_10",
        "unknown_11",
        "next_animation_id",
        "category",
        "block_damage",
        "block_stun_and_scrap",
        "successor_id",
        "damage_amount",
        "throw_duration",
        "extra_string_selector",
        "points",
        "move_string",
        "enemy_string",
    )

    schema = Dict(
        {
            **Animation.schema.schema,  # type: ignore
            **{
                "ai_flags": UInt16,
                "pos_constraint": UInt16,
                "unknown_4": UInt8,
                "unknown_5": UInt8,
                "unknown_6": UInt8,
                "unknown_7": UInt8,
                "unknown_8": UInt8,
                "unknown_9": UInt8,
                "unknown_10": UInt8,
                "unknown_11": UInt8,
                "next_animation_id": UInt8,
                "category": UInt8,
                "block_damage": UInt8,
                "block_stun_and_scrap": UInt8,
                "successor_id": UInt8,
                "damage_amount": UInt8,
                "throw_duration": UInt8,
                "extra_string_selector": UInt8,
                "points": UInt8,
                "move_string": Str(maxlen=21),
                "enemy_string": Str(),
            },
        }
    )

    def __init__(self) -> None:
        super(AFMove, self).__init__()
        self.ai_flags: AIMoveTriggers = AIMoveTriggers.NONE
        self.pos_constraint: PositionConstraint = PositionConstraint.NONE
        self.unknown_4: int = 0
        self.unknown_5: int = 0
        self.unknown_6: int = 0
        self.unknown_7: int = 0
        self.unknown_8: int = 0
        self.unknown_9: int = 0
        self.unknown_10: int = 0
        self.unknown_11: int = 0
        self.next_animation_id: int = 0
        self.category: MoveCategory = MoveCategory.MISCELLANEOUS
        self.block_damage: int = 0
        self.block_stun_and_scrap: int = 0
        self.successor_id: int = 0
        self.damage_amount: int = 0
        self.throw_duration: int = 0
        self.extra_string_selector: ExtraStringSelector = ExtraStringSelector.NONE
        self.points: int = 0
        self.move_string: str = ""
        self.enemy_string: str = ""

    @staticmethod
    def get_name(index: int) -> str | None:
        return AF_ANIMATION_NAMES.get(index)

    @property
    def has_move_string(self):
        return self.move_string not in ['"!"', "!", "0"]

    def read(self, parser: BinaryParser) -> AFMove:
        super(AFMove, self).read(parser)
        self.ai_flags = AIMoveTriggers(parser.get_uint16())
        self.pos_constraint = PositionConstraint(parser.get_uint16())
        self.unknown_4 = parser.get_uint8()
        self.unknown_5 = parser.get_uint8()
        self.unknown_6 = parser.get_uint8()
        self.unknown_7 = parser.get_uint8()
        self.unknown_8 = parser.get_uint8()
        self.unknown_9 = parser.get_uint8()
        self.unknown_10 = parser.get_uint8()
        self.unknown_11 = parser.get_uint8()
        self.next_animation_id = parser.get_uint8()
        self.category = MoveCategory(parser.get_uint8())
        self.block_damage = parser.get_uint8()
        self.block_stun_and_scrap = parser.get_uint8()
        self.successor_id = parser.get_uint8()
        self.damage_amount = parser.get_uint8()
        self.throw_duration = parser.get_uint8()
        self.extra_string_selector = ExtraStringSelector(parser.get_uint8())
        self.points = parser.get_uint8()
        self.move_string = parser.get_null_padded_str(21)
        self.enemy_string = parser.get_var_str(size_includes_zero=True)
        return self

    def write(self, parser: BinaryParser) -> None:
        super(AFMove, self).write(parser)
        parser.put_uint16(self.ai_flags)
        parser.put_uint16(self.pos_constraint)
        parser.put_uint8(self.unknown_4)
        parser.put_uint8(self.unknown_5)
        parser.put_uint8(self.unknown_6)
        parser.put_uint8(self.unknown_7)
        parser.put_uint8(self.unknown_8)
        parser.put_uint8(self.unknown_9)
        parser.put_uint8(self.unknown_10)
        parser.put_uint8(self.unknown_11)
        parser.put_uint8(self.next_animation_id)
        parser.put_uint8(self.category.value)
        parser.put_uint8(self.block_damage)
        parser.put_uint8(self.block_stun_and_scrap)
        parser.put_uint8(self.successor_id)
        parser.put_uint8(self.damage_amount)
        parser.put_uint8(self.throw_duration)
        parser.put_uint8(self.extra_string_selector.value)
        parser.put_uint8(self.points)
        parser.put_null_padded_str(self.move_string, 21)
        parser.put_var_str(self.enemy_string, size_includes_zero=True)

    def serialize(self) -> dict:
        return {
            **super(AFMove, self).serialize(),
            **{
                "ai_flags": self.ai_flags.value,
                "pos_constraint": self.pos_constraint.value,
                "unknown_4": self.unknown_4,
                "unknown_5": self.unknown_5,
                "unknown_6": self.unknown_6,
                "unknown_7": self.unknown_7,
                "unknown_8": self.unknown_8,
                "unknown_9": self.unknown_9,
                "unknown_10": self.unknown_10,
                "unknown_11": self.unknown_11,
                "next_animation_id": self.next_animation_id,
                "category": self.category.value,
                "block_damage": self.block_damage,
                "block_stun_and_scrap": self.block_stun_and_scrap,
                "successor_id": self.successor_id,
                "damage_amount": self.damage_amount,
                "throw_duration": self.throw_duration,
                "extra_string_selector": self.extra_string_selector,
                "points": self.points,
                "move_string": self.move_string,
                "enemy_string": self.enemy_string,
            },
        }

    def unserialize(self, data: dict) -> AFMove:
        super(AFMove, self).unserialize(data)
        self.ai_flags = AIMoveTriggers(data["ai_flags"])
        self.pos_constraint = PositionConstraint(data["pos_constraint"])
        self.unknown_4 = data["unknown_4"]
        self.unknown_5 = data["unknown_5"]
        self.unknown_6 = data["unknown_6"]
        self.unknown_7 = data["unknown_7"]
        self.unknown_8 = data["unknown_8"]
        self.unknown_9 = data["unknown_9"]
        self.unknown_10 = data["unknown_10"]
        self.unknown_11 = data["unknown_11"]
        self.next_animation_id = data["next_animation_id"]
        self.category = MoveCategory(data["category"])
        self.block_damage = data["block_damage"]
        self.block_stun_and_scrap = data["block_stun_and_scrap"]
        self.successor_id = data["successor_id"]
        self.damage_amount = data["damage_amount"]
        self.throw_duration = data["throw_duration"]
        self.extra_string_selector = data["extra_string_selector"]
        self.points = data["points"]
        self.move_string = data["move_string"]
        self.enemy_string = data["enemy_string"]
        return self
