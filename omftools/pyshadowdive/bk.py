import typing
from validx import Dict, List, Str
import io

from .protos import Entrypoint
from .bkanim import BKAnimation
from .palette_mapping import PaletteMapping

from .utils.parser import BinaryParser
from .utils.types import EncodedImage
from .utils.validator import UInt16, UInt32, UInt8
from .utils.images import generate_png, save_png


class BKFile(Entrypoint):
    ANIMATION_MAX_NUMBER = 50

    __slots__ = (
        'file_id',
        'unknown_a',
        'background_width',
        'background_height',
        'background_image',
        'animations',
        'sound_table',
        'palettes',
    )

    schema = Dict({
        'file_id': UInt32,
        'unknown_a': UInt8,
        'background_width': UInt16,
        'background_height': UInt16,
        'background_image': List(UInt8),
        'animations': Dict(extra=(
            Str(pattern=r'^[0-9]+$'),
            BKAnimation.schema
        )),
        'sound_table': List(UInt8, maxlen=30, minlen=30),
        'palettes': List(PaletteMapping.schema),
    })

    def __init__(self):
        self.file_id = 0
        self.unknown_a = 0
        self.background_width = 0
        self.background_height = 0
        self.animations: typing.Dict[int, BKAnimation] = {}
        self.palettes: typing.List[PaletteMapping] = []
        self.sound_table: typing.List[int] = []
        self.background_image: EncodedImage = []

    def serialize(self):
        return {
            'file_id': self.file_id,
            'unknown_a': self.unknown_a,
            'background_width': self.background_width,
            'background_height': self.background_height,
            'background_image': self.background_image,
            'animations': {k: v.serialize()
                           for k, v in self.animations.items()},
            'palettes': [palette.serialize()
                         for palette in self.palettes],
            'sound_table': self.sound_table
        }

    def unserialize(self, data):
        self.file_id = data['file_id']
        self.unknown_a = data['unknown_a']
        self.background_width = data['background_width']
        self.background_height = data['background_height']
        self.background_image = data['background_image']
        self.sound_table = data['sound_table']
        self.palettes = [PaletteMapping().unserialize(v)
                         for v in data['palettes']]
        self.animations = {int(k): BKAnimation().unserialize(v)
                           for k, v in data['animations'].items()}
        return self

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
            self.animations[anim_no] = BKAnimation().read(parser)

        # Read the raw Background image (VGA palette format)
        background_size = self.background_height * self.background_width
        self.background_image = [parser.get_uint8()
                                 for _ in range(background_size)]

        # Read up all available color palettes
        palette_count = parser.get_uint8()
        self.palettes = [PaletteMapping().read(parser)
                         for _ in range(palette_count)]

        # Get sound mappings
        self.sound_table = [parser.get_uint8()
                            for _ in range(30)]

        return self

    def write(self, parser):
        parser.put_uint32(self.file_id)
        parser.put_uint8(self.unknown_a)
        parser.put_uint16(self.background_width)
        parser.put_uint16(self.background_height)

        for key, ani in self.animations.items():
            # Write animation to binary buffer so that
            # we can tell its length
            buf = io.BytesIO()
            ani.write(BinaryParser(buf))
            ani_data = buf.getvalue()

            # Write offset of next animation, then ID,
            # then the animation blob. Add +5 to offset to account
            # for the next offset and ID.
            offset = parser.get_pos() + len(ani_data) + 5
            parser.put_uint32(offset)
            parser.put_uint8(key)
            parser.put_bytes(ani_data)

            buf.close()

        # Write ending of the animations block
        parser.put_uint32(parser.get_pos())
        parser.put_uint8(self.ANIMATION_MAX_NUMBER+1)

        for pixel in self.background_image:
            parser.put_uint8(pixel)

        parser.put_uint8(len(self.palettes))
        for pal in self.palettes:
            pal.write(parser)

        for sound in self.sound_table:
            parser.put_uint8(sound)

    def save_background(self, filename: str):
        save_png(
            generate_png(self.background_image,
                         self.background_width,
                         self.background_height,
                         self.palettes[0].colors),
            filename
        )
