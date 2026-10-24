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
    VS_AIR_STATE_1 = 0x0001
    VS_HIGH_OR_IDLE = 0x0002
    VS_LOW_OR_CROUCH = 0x0004
    VS_MEDIUM = 0x0008
    VS_PROJECTILE_HIGH = 0x0010
    VS_AIR_STATE_2 = 0x0020
    VS_AIR_STATE_3 = 0x0040
    VS_AIR_STATE_0 = 0x0080
    VS_GND_STATE_0 = 0x0100
    VS_GND_STATE_1 = 0x0200
    VS_GND_STATE_2 = 0x0400
    VS_GND_STATE_3 = 0x0800
    FLAG_1000 = 0x1000
    VS_PROJECTILE_LOW = 0x2000
    FLAG_4000 = 0x4000
    FLAG_8000 = 0x8000

    def get_hint(self) -> typing.Optional[str]:
        match self:
            case AIMoveTriggers.VS_AIR_STATE_1:
                return "Opponent is airborne, distance band 1."
            case AIMoveTriggers.VS_HIGH_OR_IDLE:
                return "Opponent is doing a high attack, or is idle."
            case AIMoveTriggers.VS_LOW_OR_CROUCH:
                return "Opponent is doing a low attack, or is crouching."
            case AIMoveTriggers.VS_MEDIUM:
                return "Opponent is doing a medium attack."
            case AIMoveTriggers.VS_PROJECTILE_HIGH:
                return (
                    "Opponent projectile at or above the HAR's "
                    "ai_projectile_y_threshold."
                )
            case AIMoveTriggers.VS_AIR_STATE_2:
                return "Opponent is airborne, distance band 2."
            case AIMoveTriggers.VS_AIR_STATE_3:
                return "Opponent is airborne, distance band 3."
            case AIMoveTriggers.VS_AIR_STATE_0:
                return "Opponent is airborne, distance band 0."
            case AIMoveTriggers.VS_GND_STATE_0:
                return "Opponent is on the ground, distance band 0."
            case AIMoveTriggers.VS_GND_STATE_1:
                return "Opponent is on the ground, distance band 1."
            case AIMoveTriggers.VS_GND_STATE_2:
                return "Opponent is on the ground, distance band 2."
            case AIMoveTriggers.VS_GND_STATE_3:
                return "Opponent is on the ground, distance band 3."
            case AIMoveTriggers.FLAG_1000:
                return (
                    "Unknown; used by 3 moves in the shipped data (Jaguar leap / "
                    "charge)."
                )
            case AIMoveTriggers.VS_PROJECTILE_LOW:
                return (
                    "Opponent projectile below the HAR's ai_projectile_y_threshold "
                    "(evade reaction)."
                )
            case AIMoveTriggers.FLAG_4000:
                return "Reserved."
            case AIMoveTriggers.FLAG_8000:
                return "Reserved."
            case _:
                return None

    def __str__(self) -> str:
        return "{} ({})".format(self.name, self.value)


class PositionConstraint(IntFlag):
    """Positional / state requirements declared on an AF move.

    Every set bit must be satisfied by the HAR's current state.
    """
    NONE = 0
    WALL = 0x0001
    NO_DIST_CHECK = 0x0002
    JUMP_WALL_BOUNCE = 0x0004
    IN_ARENA_0 = 0x0008
    IN_ARENA_1 = 0x0010
    IN_ARENA_2 = 0x0020
    IN_ARENA_3 = 0x0040
    IN_ARENA_4 = 0x0080
    FLAG_100 = 0x0100
    FLAG_200 = 0x0200
    FLAG_400 = 0x0400
    FLAG_800 = 0x0800
    FLAG_1000 = 0x1000
    FIRE_ICE_ALLOWED = 0x2000
    OPP_FIRE_ICE_DESTRUCT = 0x4000
    FLAG_8000 = 0x8000

    def get_hint(self) -> typing.Optional[str]:
        match self:
            case PositionConstraint.WALL:
                return "HAR must be near a wall (x below 21 or above 298 pixels)."
            case PositionConstraint.NO_DIST_CHECK:
                return "Skip the distance / position checks (used by chained moves)."
            case PositionConstraint.JUMP_WALL_BOUNCE:
                return (
                    "Set on the target's jump animation: an aerial hit makes it bounce "
                    "off the wall."
                )
            case PositionConstraint.IN_ARENA_0:
                return "Only in arena 0. Unused in the shipped data."
            case PositionConstraint.IN_ARENA_1:
                return "Only in arena 1. Unused in the shipped data."
            case PositionConstraint.IN_ARENA_2:
                return "Only in arena 2. Unused in the shipped data."
            case PositionConstraint.IN_ARENA_3:
                return "Only in arena 3 (Fire Pit)."
            case PositionConstraint.IN_ARENA_4:
                return "Only in arena 4. Unused in the shipped data."
            case PositionConstraint.FLAG_100:
                return "Reserved."
            case PositionConstraint.FLAG_200:
                return "Reserved."
            case PositionConstraint.FLAG_400:
                return "Reserved."
            case PositionConstraint.FLAG_800:
                return "Reserved."
            case PositionConstraint.FLAG_1000:
                return "Set on the target's animation; never set in the shipped data."
            case PositionConstraint.FIRE_ICE_ALLOWED:
                return "Only while fire / ice moves are allowed."
            case PositionConstraint.OPP_FIRE_ICE_DESTRUCT:
                return (
                    "Only when the opponent pilot has been destroyed this fight "
                    "(Pilot.destroyed)."
                )
            case PositionConstraint.FLAG_8000:
                return "Reserved."
            case _:
                return None

    def __str__(self) -> str:
        return "{} ({})".format(self.name, self.value)


class ExtraStringSelector(IntEnum):
    NONE = 0
    ARM_SPEED = 1
    LEG_SPEED = 2
    SPECIAL_ARM = 3
    SPECIAL_LEG = 4
    SPECIAL = 5

    def get_hint(self) -> typing.Optional[str]:
        match self:
            case ExtraStringSelector.ARM_SPEED:
                return "Extra string chosen by the pilot's arm speed."
            case ExtraStringSelector.LEG_SPEED:
                return "Extra string chosen by the pilot's leg speed."
            case ExtraStringSelector.SPECIAL_ARM:
                return (
                    "Extra string chosen by the special-move enhancement level; damage "
                    "scaled by arm power."
                )
            case ExtraStringSelector.SPECIAL_LEG:
                return (
                    "Extra string chosen by the special-move enhancement level; damage "
                    "scaled by leg power."
                )
            case ExtraStringSelector.SPECIAL:
                return "Special case, handled differently from the others."
            case _:
                return None

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

    def get_hint(self) -> typing.Optional[str]:
        match self:
            case MoveCategory.LOW:
                return "Low attack."
            case MoveCategory.MEDIUM:
                return "Medium-height attack."
            case MoveCategory.HIGH:
                return "High attack."
            case MoveCategory.JUMPING:
                return "Attack performed in the air."
            case MoveCategory.PROJECTILE:
                return "Projectile attack."
            case MoveCategory.BK_HAZARD:
                return "Attack by an arena hazard."
            case MoveCategory.SCRAP:
                return "Scrap finishing move."
            case MoveCategory.DESTRUCTION:
                return "Destruction finishing move (also counts as scrapping)."
            case _:
                return None

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
