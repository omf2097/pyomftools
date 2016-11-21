from .animation import Animation
from .protos import OMFObjectMixin
from .decorators import validate_schema


class AFMove(Animation, OMFObjectMixin):
    schema = {**Animation.schema, **{
        'unknown_0': {'type': 'integer', 'required': True, 'min': 0, 'max': 65535},
        'unknown_2': {'type': 'integer', 'required': True, 'min': 0, 'max': 65535},
        'unknown_4': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'unknown_5': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'unknown_6': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'unknown_7': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'unknown_8': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'unknown_9': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'unknown_10': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'unknown_11': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'next_anim_id': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'category': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'unknown_14': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'scrap_amount': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'successor_id': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'damage_amount': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'unknown_18': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'unknown_19': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'points': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'move_string': {'type': 'string', 'required': True, 'minlength': 21, 'maxlength': 21},
        'footer_string': {'type': 'string', 'required': True},
    }}

    def __init__(self):
        super(AFMove, self).__init__()
        self.unknown_0 = 0
        self.unknown_2 = 0
        self.unknown_4 = 0
        self.unknown_5 = 0
        self.unknown_6 = 0
        self.unknown_7 = 0
        self.unknown_8 = 0
        self.unknown_9 = 0
        self.unknown_10 = 0
        self.unknown_11 = 0
        self.next_anim_id = 0
        self.category = 0
        self.unknown_14 = 0
        self.scrap_amount = 0
        self.successor_id = 0
        self.damage_amount = 0
        self.unknown_18 = 0
        self.unknown_19 = 0
        self.points = 0
        self.move_string = ""
        self.footer_string = ""

    def read(self, parser):
        super(AFMove, self).read(parser)
        self.unknown_0 = parser.get_uint16()
        self.unknown_2 = parser.get_uint16()
        self.unknown_4 = parser.get_uint8()
        self.unknown_5 = parser.get_uint8()
        self.unknown_6 = parser.get_uint8()
        self.unknown_7 = parser.get_uint8()
        self.unknown_8 = parser.get_uint8()
        self.unknown_9 = parser.get_uint8()
        self.unknown_10 = parser.get_uint8()
        self.unknown_11 = parser.get_uint8()
        self.next_anim_id = parser.get_uint8()
        self.category = parser.get_uint8()
        self.unknown_14 = parser.get_uint8()
        self.scrap_amount = parser.get_uint8()
        self.successor_id = parser.get_uint8()
        self.damage_amount = parser.get_uint8()
        self.unknown_18 = parser.get_uint8()
        self.unknown_19 = parser.get_uint8()
        self.points = parser.get_uint8()
        self.move_string = parser.get_str(21)
        self.footer_string = parser.get_var_str(size_includes_zero=True)

    def write(self, parser):
        super(AFMove, self).write(parser)
        parser.put_uint16(self.unknown_0)
        parser.put_uint16(self.unknown_2)
        parser.put_uint8(self.unknown_4)
        parser.put_uint8(self.unknown_5)
        parser.put_uint8(self.unknown_6)
        parser.put_uint8(self.unknown_7)
        parser.put_uint8(self.unknown_8)
        parser.put_uint8(self.unknown_9)
        parser.put_uint8(self.unknown_10)
        parser.put_uint8(self.unknown_11)
        parser.put_uint8(self.next_anim_id)
        parser.put_uint8(self.category)
        parser.put_uint8(self.unknown_14)
        parser.put_uint8(self.scrap_amount)
        parser.put_uint8(self.successor_id)
        parser.put_uint8(self.damage_amount)
        parser.put_uint8(self.unknown_18)
        parser.put_uint8(self.unknown_19)
        parser.put_uint8(self.points)
        parser.put_str(self.move_string)
        parser.put_var_str(self.footer_string, size_includes_zero=True)

    def serialize(self):
        return {**super(AFMove, self).serialize(), **{
            'unknown_0': self.unknown_0,
            'unknown_2': self.unknown_2,
            'unknown_4': self.unknown_4,
            'unknown_5': self.unknown_5,
            'unknown_6': self.unknown_6,
            'unknown_7': self.unknown_7,
            'unknown_8': self.unknown_8,
            'unknown_9': self.unknown_9,
            'unknown_10': self.unknown_10,
            'unknown_11': self.unknown_11,
            'next_anim_id': self.next_anim_id,
            'category': self.category,
            'unknown_14': self.unknown_14,
            'scrap_amount': self.scrap_amount,
            'successor_id': self.successor_id,
            'damage_amount': self.damage_amount,
            'unknown_18': self.unknown_18,
            'unknown_19': self.unknown_19,
            'points': self.points,
            'move_string': self.move_string,
            'footer_string': self.footer_string
        }}

    @validate_schema(schema)
    def unserialize(self, data):
        super(AFMove, self).unserialize(data)
        self.unknown_0 = data['unknown_0']
        self.unknown_2 = data['unknown_2']
        self.unknown_4 = data['unknown_4']
        self.unknown_5 = data['unknown_5']
        self.unknown_6 = data['unknown_6']
        self.unknown_7 = data['unknown_7']
        self.unknown_8 = data['unknown_8']
        self.unknown_9 = data['unknown_9']
        self.unknown_10 = data['unknown_10']
        self.unknown_11 = data['unknown_11']
        self.next_anim_id = data['next_anim_id']
        self.category = data['category']
        self.unknown_14 = data['unknown_14']
        self.scrap_amount = data['scrap_amount']
        self.successor_id = data['successor_id']
        self.damage_amount = data['damage_amount']
        self.unknown_18 = data['unknown_18']
        self.unknown_19 = data['unknown_19']
        self.points = data['points']
        self.move_string = data['move_string']
        self.footer_string = data['footer_string']
