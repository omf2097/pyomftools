from __future__ import annotations
import typing
from validx import Dict, List, Str

from .protos import Entrypoint
from .afmove import AFMove
from .sprite import Sprite
from .utils.parser import BinaryParser

from .utils.validator import UInt8, UInt16, UInt32, Int32


class AFFile(Entrypoint):
    MOVE_MAX_NUMBER = 70

    __slots__ = (
        "fighter_id",
        "move_timeout_window",
        "endurance",
        "upwards_jump_frame_limit",
        "health",
        "forward_speed",
        "reverse_speed",
        "jump_speed",
        "fall_speed",
        "version_1",
        "ai_projectile_y_threshold",
        "sound_table",
        "moves",
    )

    schema = Dict(
        {
            "fighter_id": UInt16,
            "move_timeout_window": UInt16,
            "endurance": UInt32,
            "upwards_jump_frame_limit": UInt8,
            "health": UInt16,
            "forward_speed": Int32,
            "reverse_speed": Int32,
            "jump_speed": Int32,
            "fall_speed": Int32,
            "version_1": UInt8,
            "ai_projectile_y_threshold": UInt8,
            "sound_table": List(UInt8, maxlen=30, minlen=30),
            "moves": Dict(extra=(Str(pattern=r"^[0-9]+$"), AFMove.schema)),
        }
    )

    def __init__(self) -> None:
        self.fighter_id: int = 0
        self.move_timeout_window: int = 0
        self.endurance: int = 0
        self.upwards_jump_frame_limit: int = 0
        self.health: int = 0
        self.forward_speed: int = 0
        self.reverse_speed: int = 0
        self.jump_speed: int = 0
        self.fall_speed: int = 0
        self.version_1: int = 0
        self.ai_projectile_y_threshold: int = 0
        self.moves: dict[int, AFMove] = {}
        self.sound_table: list[int] = []

    def get_hint(self, attr: str) -> typing.Optional[str]:
        match attr:
            case "endurance":
                return (
                    "24.8 fixed point. Scaled by the pilot's stats when the HAR is "
                    "loaded."
                )
            case "forward_speed":
                return (
                    "24.8 fixed point; the decoded value is pixels per tick, before "
                    "pilot-stat scaling."
                )
            case "reverse_speed":
                return (
                    "24.8 fixed point; the decoded value is pixels per tick, before "
                    "pilot-stat scaling."
                )
            case "jump_speed":
                return (
                    "24.8 fixed point; the decoded value is pixels per tick, before "
                    "pilot-stat scaling."
                )
            case "fall_speed":
                return (
                    "24.8 fixed point; gravity added to the vertical speed every tick, "
                    "before pilot-stat scaling."
                )
            case "move_timeout_window":
                return (
                    "Ticks a held direction stays part of a motion input (e.g. the "
                    "down, down-forward, forward of a special move)."
                )
            case "version_1":
                return "Always 50 (0x32). The game reads it but never uses it."
            case _:
                return super().get_hint(attr)

    def serialize(self) -> dict[str, typing.Any]:
        return {
            "fighter_id": self.fighter_id,
            "move_timeout_window": self.move_timeout_window,
            "endurance": self.endurance,
            "upwards_jump_frame_limit": self.upwards_jump_frame_limit,
            "health": self.health,
            "forward_speed": self.forward_speed,
            "reverse_speed": self.reverse_speed,
            "jump_speed": self.jump_speed,
            "fall_speed": self.fall_speed,
            "version_1": self.version_1,
            "ai_projectile_y_threshold": self.ai_projectile_y_threshold,
            "moves": {k: v.serialize() for k, v in self.moves.items()},
            "sound_table": self.sound_table,
        }

    def unserialize(self, data: dict) -> AFFile:
        self.fighter_id = data["fighter_id"]
        self.move_timeout_window = data["move_timeout_window"]
        self.endurance = data["endurance"]
        self.upwards_jump_frame_limit = data["upwards_jump_frame_limit"]
        self.health = data["health"]
        self.forward_speed = data["forward_speed"]
        self.reverse_speed = data["reverse_speed"]
        self.jump_speed = data["jump_speed"]
        self.fall_speed = data["fall_speed"]
        self.version_1 = data["version_1"]
        self.ai_projectile_y_threshold = data["ai_projectile_y_threshold"]
        self.moves = {int(k): AFMove().unserialize(v) for k, v in data["moves"].items()}
        self.sound_table = data["sound_table"]
        return self

    def read(self, parser: BinaryParser) -> AFFile:
        self.fighter_id = parser.get_uint16()
        self.move_timeout_window = parser.get_uint16()
        self.endurance = parser.get_uint32()
        self.upwards_jump_frame_limit = parser.get_uint8()
        self.health = parser.get_uint16()
        self.forward_speed = parser.get_int32()
        self.reverse_speed = parser.get_int32()
        self.jump_speed = parser.get_int32()
        self.fall_speed = parser.get_int32()
        self.version_1 = parser.get_uint8()
        self.ai_projectile_y_threshold = parser.get_uint8()

        # Read all animations (up to max MOVE_MAX_NUMBER)
        while True:
            move_no = parser.get_uint8()
            if move_no >= self.MOVE_MAX_NUMBER:
                break
            self.moves[move_no] = AFMove().read(parser)

        # Find missing image data by index
        index_table: typing.Dict[int, Sprite] = {}
        for key, m in self.moves.items():
            for idx, sprite in enumerate(m.sprites):
                if sprite.missing:
                    if sprite.index in index_table:
                        sprite.image = index_table[sprite.index].image
                else:
                    index_table[sprite.index] = sprite

        # Read sound table
        for _ in range(0, 30):
            self.sound_table.append(parser.get_uint8())

        return self

    def write(self, parser: BinaryParser) -> None:
        parser.put_uint16(self.fighter_id)
        parser.put_uint16(self.move_timeout_window)
        parser.put_uint32(self.endurance)
        parser.put_uint8(self.upwards_jump_frame_limit)
        parser.put_uint16(self.health)
        parser.put_int32(self.forward_speed)
        parser.put_int32(self.reverse_speed)
        parser.put_int32(self.jump_speed)
        parser.put_int32(self.fall_speed)
        parser.put_uint8(self.version_1)
        parser.put_uint8(self.ai_projectile_y_threshold)

        # Write moves
        for key, move in self.moves.items():
            parser.put_uint8(key)
            move.write(parser)

        # Mark the end of moves
        parser.put_uint8(250)

        # Write sounds
        for sound in self.sound_table:
            parser.put_uint8(sound)

    @property
    def real_endurance(self) -> float:
        return self.endurance / 256.0

    @real_endurance.setter
    def real_endurance(self, value: float) -> None:
        self.endurance = int(value * 256.0)

    @property
    def real_forward_speed(self) -> float:
        return self.forward_speed / 256.0

    @real_forward_speed.setter
    def real_forward_speed(self, value: float) -> None:
        self.forward_speed = int(value * 256.0)

    @property
    def real_reverse_speed(self) -> float:
        return self.reverse_speed / 256.0

    @real_reverse_speed.setter
    def real_reverse_speed(self, value: float) -> None:
        self.reverse_speed = int(value * 256.0)

    @property
    def real_jump_speed(self) -> float:
        return self.jump_speed / 256.0

    @real_jump_speed.setter
    def real_jump_speed(self, value: float) -> None:
        self.jump_speed = int(value * 256.0)

    @property
    def real_fall_speed(self) -> float:
        return self.fall_speed / 256.0

    @real_fall_speed.setter
    def real_fall_speed(self, value: float) -> None:
        self.fall_speed = int(value * 256.0)
