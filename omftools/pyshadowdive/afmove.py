from validx import Dict, Str
from enum import Flag, IntEnum

from .animation import Animation
from .utils.validator import UInt8, UInt16


class AIOptions(Flag):
    NONE = 0
    FLAG_1 = 0x1
    FLAG_2 = 0x2
    FLAG_3 = 0x4
    FLAG_4 = 0x8
    FLAG_5 = 0x10
    FLAG_6 = 0x20
    FLAG_7 = 0x40
    FLAG_8 = 0x80
    FLAG_9 = 0x100
    FLAG_10 = 0x200
    FLAG_11 = 0x400
    FLAG_12 = 0x800
    FLAG_13 = 0x1000
    FLAG_14 = 0x2000
    FLAG_15 = 0x4000
    FLAG_16 = 0x8000


class PositionConstraint(Flag):
    NONE = 0
    WALL = 1
    AIRBORNE = 2
    CLOSE = 4
    SOMETHING_1 = 0x40
    SOMETHING_2 = 0x2000
    SOMETHING_3 = 0x4000


class MoveCategory(IntEnum):
    MISCELLANEOUS = 0
    UNKNOWN_A = 1
    CLOSE = 2
    UNKNOWN_B = 3
    LOW = 4
    MEDIUM = 5
    HIGH = 6
    JUMPING = 7
    PROJECTILE = 8
    BASIC = 9
    VICTORY_DEFEAT = 10
    UNKNOWN_C = 11
    SCRAP = 12
    DESTRUCTION = 13


AF_ANIMATION_NAMES = {
    1: 'Jumping',
    2: 'Getting up',
    3: 'Stunned',
    4: 'Crouching',
    5: 'Standing block',
    6: 'Crouching block',
    7: 'Burning oil',
    8: 'Blocking scrape',
    9: 'Damage',
    10: 'Walking',
    11: 'Idle',
    12: 'Scrap',
    13: 'Bolt',
    14: 'Screw',
    48: 'Victory',
    49: 'Loss',
    55: 'Blast 1',
    56: 'Blast 2',
    57: 'Blast 3',
}


class AFMove(Animation):
    __slots__ = (
       'ai_opts',
       'pos_constraint',
       'unknown_4',
       'unknown_5',
       'unknown_6',
       'unknown_7',
       'unknown_8',
       'unknown_9',
       'unknown_10',
       'unknown_11',
       'next_animation_id',
       'category',
       'unknown_14',
       'scrap_amount',
       'successor_id',
       'damage_amount',
       'collision_opts',
       'extra_string_selector',
       'points',
       'move_string',
       'enemy_string',
    )

    schema = Dict({**Animation.schema.schema, **{
        'ai_opts': UInt16,
        'pos_constraint': UInt16,
        'unknown_4': UInt8,
        'unknown_5': UInt8,
        'unknown_6': UInt8,
        'unknown_7': UInt8,
        'unknown_8': UInt8,
        'unknown_9': UInt8,
        'unknown_10': UInt8,
        'unknown_11': UInt8,
        'next_animation_id': UInt8,
        'category': UInt8,
        'unknown_14': UInt8,
        'scrap_amount': UInt8,
        'successor_id': UInt8,
        'damage_amount': UInt8,
        'collision_opts': UInt8,
        'extra_string_selector': UInt8,
        'points': UInt8,
        'move_string': Str(maxlen=21),
        'enemy_string': Str(),
    }})

    def __init__(self):
        super(AFMove, self).__init__()
        self.ai_opts: AIOptions = 0
        self.pos_constraint: PositionConstraint = 0
        self.unknown_4: int = 0
        self.unknown_5: int = 0
        self.unknown_6: int = 0
        self.unknown_7: int = 0
        self.unknown_8: int = 0
        self.unknown_9: int = 0
        self.unknown_10: int = 0
        self.unknown_11: int = 0
        self.next_animation_id: int = 0
        self.category: MoveCategory = 0
        self.unknown_14: int = 0
        self.scrap_amount: int = 0
        self.successor_id: int = 0
        self.damage_amount: int = 0
        self.collision_opts: int = 0
        self.extra_string_selector: int = 0
        self.points: int = 0
        self.move_string: str = ""
        self.enemy_string: str = ""

    @staticmethod
    def get_name(index: int):
        if index in AF_ANIMATION_NAMES:
            return AF_ANIMATION_NAMES[index]
        return None

    def read(self, parser) -> 'AFMove':
        super(AFMove, self).read(parser)
        self.ai_opts = AIOptions(parser.get_uint16())
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
        self.unknown_14 = parser.get_uint8()
        self.scrap_amount = parser.get_uint8()
        self.successor_id = parser.get_uint8()
        self.damage_amount = parser.get_uint8()
        self.collision_opts = parser.get_uint8()
        self.extra_string_selector = parser.get_uint8()
        self.points = parser.get_uint8()
        self.move_string = parser.get_null_padded_str(21)
        self.enemy_string = parser.get_var_str(size_includes_zero=True)
        return self

    def write(self, parser):
        super(AFMove, self).write(parser)
        parser.put_uint16(self.ai_opts.value)
        parser.put_uint16(self.pos_constraint.value)
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
        parser.put_uint8(self.unknown_14)
        parser.put_uint8(self.scrap_amount)
        parser.put_uint8(self.successor_id)
        parser.put_uint8(self.damage_amount)
        parser.put_uint8(self.collision_opts)
        parser.put_uint8(self.extra_string_selector)
        parser.put_uint8(self.points)
        parser.put_null_padded_str(self.move_string, 21)
        parser.put_var_str(self.enemy_string, size_includes_zero=True)

    def serialize(self) -> dict:
        return {**super(AFMove, self).serialize(), **{
            'ai_opts': self.ai_opts.value,
            'pos_constraint': self.pos_constraint.value,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'next_animation_id': self.next_animation_id,
            'category': self.category.value,
            'unknown_14': self.unknown_14,
            'scrap_amount': self.scrap_amount,
            'successor_id': self.successor_id,
            'damage_amount': self.damage_amount,
            'collision_opts': self.collision_opts,
            'extra_string_selector': self.extra_string_selector,
            'points': self.points,
            'move_string': self.move_string,
            'enemy_string': self.enemy_string
        }}

    def unserialize(self, data: dict) -> 'AFMove':
        super(AFMove, self).unserialize(data)
        self.ai_opts = AIOptions(data['ai_opts'])
        self.pos_constraint = PositionConstraint(data['pos_constraint'])
        self.unknown_4 = data['unknown_4']
        self.unknown_5 = data['unknown_5']
        self.unknown_6 = data['unknown_6']
        self.unknown_7 = data['unknown_7']
        self.unknown_8 = data['unknown_8']
        self.unknown_9 = data['unknown_9']
        self.unknown_10 = data['unknown_10']
        self.unknown_11 = data['unknown_11']
        self.next_animation_id = data['next_animation_id']
        self.category = MoveCategory(data['category'])
        self.unknown_14 = data['unknown_14']
        self.scrap_amount = data['scrap_amount']
        self.successor_id = data['successor_id']
        self.damage_amount = data['damage_amount']
        self.collision_opts = data['collision_opts']
        self.extra_string_selector = data['extra_string_selector']
        self.points = data['points']
        self.move_string = data['move_string']
        self.enemy_string = data['enemy_string']
        return self
