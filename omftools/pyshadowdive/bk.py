import base64

from .protos import OMFEntrypointMixin
from .decorators import validate_schema
from .bkanim import BKAnim
from .palettes import Palette


class BKFile(OMFEntrypointMixin):
    ANIMATION_MAX_NUMBER = 50

    schema = {
        'file_id': {'type': 'integer', 'required': True, 'min': 0, 'max': 0xFFFFFFFF},
        'unknown_a': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'background_width': {'type': 'integer', 'required': True, 'min': 0, 'max': 65535},
        'background_height': {'type': 'integer', 'required': True, 'min': 0, 'max': 65535},
        'animations': {
            'type': 'dict',
            'required': True,
            'allow_unknown': True,
        },
        'sound_table': {
            'type': 'list',
            'required': True,
            'schema': {
                'type': 'integer',
            }
        },
        'palette_table': {
            'type': 'list',
            'required': True,
            'schema': {
                'type': 'dict',
                'allow_unknown': True,
            }
        }
    }

    def __init__(self):
        self.file_id = 0
        self.unknown_a = 0
        self.background_width = 0
        self.background_height = 0
        self.animations = {}
        self.palette_table = []
        self.sound_table = []
        self._raw_bg_image = None

    def serialize(self):
        animations = {}
        for key, anim in self.animations.items():
            animations[key] = anim.serialize()

        return {
            'file_id': self.file_id,
            'unknown_a': self.unknown_a,
            'background_width': self.background_width,
            'background_height': self.background_height,
            'raw_background_image': base64.b64encode(self._raw_bg_image).decode() if self._raw_bg_image else None,
            'animations': animations,
            'palette_table': [palette.serialize() for palette in self.palette_table],
            'sound_table': self.sound_table
        }

    @validate_schema(schema)
    def unserialize(self, data):
        self.file_id = data['file_id']
        self.unknown_a = data['unknown_a']
        self.background_width = data['background_width']
        self.background_height = data['background_height']
        self._raw_bg_image = base64.b64decode(data['raw_background_image']) if data['raw_background_image'] else None
        self.sound_table = data['sound_table']

        self.palette_table = []
        for palette in data['palette_table']:
            pal_obj = Palette()
            pal_obj.unserialize(palette)
            self.palette_table.append(pal_obj)

        self.animations = {}
        for key, anim in data['animations'].items():
            anim_obj = BKAnim()
            anim_obj.unserialize(anim)
            self.animations[key] = anim_obj

    def read(self, parser):
        self.file_id = parser.get_uint32()
        self.unknown_a = parser.get_uint8()
        self.background_width = parser.get_uint16()
        self.background_height = parser.get_uint16()

        # Read all animations (up to max ANIMATION_MAX_NUMBER)
        while True:
            parser.get_uint32()  # Skip
            anim_no = parser.get_uint8()
            if anim_no >= self.ANIMATION_MAX_NUMBER:
                break
            anim = BKAnim()
            anim.read(parser)
            self.animations[anim_no] = anim

        # Read the raw Background image (VGA palette format)
        self._raw_bg_image = parser.get_bytes(self.background_width * self.background_height)

        # Read up all available color palettes
        palette_count = parser.get_uint8()
        for p in range(0, palette_count):
            palette = Palette()
            palette.read(parser)
            self.palette_table.append(palette)

        # Read sound table
        for m in range(0, 30):
            sound = parser.get_uint8()
            self.sound_table.append(sound)

    def write(self, parser):
        parser.put_uint16(self.file_id)
        parser.put_uint8(self.unknown_a)
        parser.put_uint16(self.background_width)
        parser.put_uint16(self.background_height)

        # TODO
