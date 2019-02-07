import typing
from validx import Dict, Int, List, Str

from .protos import DataObject
from .sprite import Sprite
from .utils.validator import Int16
from .utils.types import HitCoordinate


class Animation(DataObject):
    __slots__ = (
        'start_x',
        'start_y',
        'base_string',
        'hit_coords',
        'extra_strings',
        'sprites',
    )
    
    schema = Dict({
        'start_x': Int16,
        'start_y': Int16,
        'base_string': Str(),
        'hit_coords': List(
            Dict({
                'x': Int(min=-511, max=511),
                'null': Int(min=0, max=0),
                'y': Int(min=-511, max=511),
                'frame_id': Int(min=0, max=63),
            })
        ),
        'extra_strings': List(Str()),
        'sprites': List(Sprite.schema),
    })

    def __init__(self):
        self.start_x: int = 0
        self.start_y: int = 0
        self.hit_coords: typing.List[HitCoordinate] = []
        self.sprites: typing.List[Sprite] = []
        self.base_string: str = ""
        self.extra_strings: typing.List[str] = []

    def read(self, parser) -> 'Animation':
        self.start_x = parser.get_int16()
        self.start_y = parser.get_int16()
        assert parser.get_uint32() == 0
        coord_count = parser.get_uint16()
        sprite_count = parser.get_uint8()

        self.hit_coords = []
        for m in range(0, coord_count):
            a = parser.get_uint16()
            b = parser.get_uint16()
            x = 0x3ff & a
            y = 0x3ff & b
            self.hit_coords.append({
                'x': x if x < 512 else x - 1024,
                'null': (a >> 10),
                'y': y if y < 512 else y - 1024,
                'frame_id': (b >> 10)
            })

        self.base_string = parser.get_var_str()
        extra_str_count = parser.get_uint8()

        self.extra_strings = []
        for k in range(0, extra_str_count):
            self.extra_strings.append(parser.get_var_str())

        self.sprites = []
        for s in range(0, sprite_count):
            sprite = Sprite()
            sprite.read(parser)
            self.sprites.append(sprite)

        return self

    def write(self, parser):
        parser.put_int16(self.start_x)
        parser.put_int16(self.start_y)
        parser.put_uint32(0)
        parser.put_uint16(len(self.hit_coords))
        parser.put_uint8(len(self.sprites))

        for coord in self.hit_coords:
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

        parser.put_var_str(self.base_string)

        parser.put_uint8(len(self.extra_strings))
        for extra_string in self.extra_strings:
            parser.put_var_str(extra_string)

        for sprite in self.sprites:
            sprite.write(parser)

    def serialize(self):
        return {
            'start_x': self.start_x,
            'start_y': self.start_y,
            'hit_coords': self.hit_coords,
            'sprites': [sprite.serialize() for sprite in self.sprites],
            'base_string': self.base_string,
            'extra_strings': self.extra_strings,
        }

    def unserialize(self, data) -> 'Animation':
        self.start_x = data['start_x']
        self.start_y = data['start_y']
        self.hit_coords = data['hit_coords']

        self.sprites = []
        for sprite in data['sprites']:
            sp_obj = Sprite()
            sp_obj.unserialize(sprite)
            self.sprites.append(sp_obj)

        self.base_string = data['base_string']
        self.extra_strings = data['extra_strings']
        return self
