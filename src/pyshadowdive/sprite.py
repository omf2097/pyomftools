import base64

from .protos import OMFObjectMixin


class Sprite(OMFObjectMixin):
    def __init__(self):
        self.len = 0
        self.pos_x = 0
        self.pos_y = 0
        self.index = 0
        self.missing = False
        self.width = 0
        self.height = 0
        self._raw_image = None

    def read(self, parser):
        self.len = parser.get_uint16()
        self.pos_x = parser.get_int16()
        self.pos_y = parser.get_int16()
        self.width = parser.get_uint16()
        self.height = parser.get_uint16()
        self.index = parser.get_uint8()
        self.missing = parser.get_boolean()

        self._raw_image = None
        if self.len and not self.missing:
            self._raw_image = parser.get_bytes(self.len)

    def write(self, parser):
        parser.put_uint16(self.len)
        parser.put_int16(self.pos_x)
        parser.put_int16(self.pos_y)
        parser.put_uint16(self.width)
        parser.put_uint16(self.height)
        parser.put_uint8(self.index)
        parser.put_boolean(self.missing)

        if self.len and not self.missing:
            parser.put_bytes(self._raw_image)

    def serialize(self):
        return {
            'len': self.len,
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'width': self.width,
            'height': self.height,
            'index': self.index,
            'missing': self.missing,
            'raw_image': base64.b64encode(self._raw_image).decode() if self._raw_image else None
        }

    def unserialize(self, data):
        self.len = data['len']
        self.pos_x = data['pos_x']
        self.pos_y = data['pos_y']
        self.width = data['width']
        self.height = data['height']
        self.index = data['index']
        self.missing = data['missing']
        self._raw_image = base64.b64decode(data['raw_image']) if data['raw_image'] else None

    @property
    def raw_image(self):
        return self._raw_image

    @raw_image.setter
    def raw_image(self, data):
        self._raw_image = data
        self.len = len(data) if data else 0
