from .protos import OMFObjectMixin
from .sprite import Sprite


class Animation(OMFObjectMixin):
    schema = {
        'start_x': {'type': 'integer', 'required': True, 'min': -32767, 'max': 32767},
        'start_y': {'type': 'integer', 'required': True, 'min': -32767, 'max': 32767},
        'null': {'type': 'integer', 'required': True, 'min': 0, 'max': 0},
        'anim_string': {'type': 'string', 'required': True},
        'coord_table': {
            'type': 'list',
            'required': True,
            'schema': {
                'type': 'dict',
                'schema': {
                    'x': {'type': 'integer', 'required': True, 'min': -511, 'max': 511},
                    'y': {'type': 'integer', 'required': True, 'min': -511, 'max': 511},
                    'null': {'type': 'integer', 'required': True, 'min': 0, 'max': 0},
                    'frame_id': {'type': 'integer', 'required': True, 'min': 0, 'max': 63},
                }
            }
        },
        'extra_strings': {
            'type': 'list',
            'required': True,
            'schema': {
                'type': 'string',
            }
        },
        'sprite_table': {
            'type': 'list',
            'required': True,
            'allow_unknown': True,
        }
    }

    def __init__(self):
        self.start_x = 0
        self.start_y = 0
        self.null = 0
        self.coord_table = []
        self.sprite_table = []
        self.anim_string = ""
        self.extra_strings = []

    def read(self, parser):
        self.start_x = parser.get_int16()
        self.start_y = parser.get_int16()
        self.null = parser.get_uint32()
        coord_count = parser.get_uint16()
        sprite_count = parser.get_uint8()

        for m in range(0, coord_count):
            a = parser.get_uint16()
            b = parser.get_uint16()
            x = 0x3ff & a
            y = 0x3ff & b
            self.coord_table.append({
                'x': x if x < 512 else x - 1024,
                'null': (a >> 10),
                'y': y if y < 512 else y - 1024,
                'frame_id': (b >> 10)
            })

        self.anim_string = parser.get_var_str()

        extra_str_count = parser.get_uint8()
        for k in range(0, extra_str_count):
            self.extra_strings.append(parser.get_var_str())

        for s in range(0, sprite_count):
            sprite = Sprite()
            sprite.read(parser)
            self.sprite_table.append(sprite)

    def write(self, parser):
        parser.put_int16(self.start_x)
        parser.put_int16(self.start_y)
        parser.put_uint32(self.null)
        parser.put_uint16(len(self.coord_table))
        parser.put_uint8(len(self.sprite_table))

        for coord in self.coord_table:
            frame_id = coord['frame_id']
            null = coord['null']
            x = coord['x']
            y = coord['y']
            tmp = frame_id & 0x3f
            tmp <<= 10
            tmp |= (y & 0x3ff)
            tmp <<= 6
            tmp |= (null & 0x3f)
            tmp <<= 10
            tmp |= (x & 0x3ff)
            parser.put_uint32(tmp)

        parser.put_var_str(self.anim_string)

        parser.put_uint8(len(self.extra_strings))
        for extra_string in self.extra_strings:
            parser.put_var_str(extra_string)

        for sprite in self.sprite_table:
            sprite.write(parser)

    def serialize(self):
        return {
            'start_x': self.start_x,
            'start_y': self.start_y,
            'null': self.null,
            'coord_table': self.coord_table,
            'sprite_table': [sprite.serialize() for sprite in self.sprite_table],
            'anim_string': self.anim_string,
            'extra_strings': self.extra_strings,
        }

    def unserialize(self, data):
        self.start_x = data['start_x']
        self.start_y = data['start_y']
        self.null = data['null']
        self.coord_table = data['coord_table']

        self.sprite_table = []
        for sprite in data['sprite_table']:
            sp_obj = Sprite()
            sp_obj.unserialize(sprite)
            self.sprite_table.append(sp_obj)

        self.anim_string = data['anim_string']
        self.extra_strings = data['extra_strings']
