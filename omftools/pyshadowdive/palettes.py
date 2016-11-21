import base64

from .protos import OMFObjectMixin
from .decorators import validate_schema


class Palette(OMFObjectMixin):
    schema = {
        'colors': {'type': 'string', 'required': True},
        'remaps': {'type': 'string', 'required': True},
    }

    def __init__(self):
        self.colors = None
        self.remaps = None

    def read(self, parser):
        self.colors = parser.get_bytes(256 * 3)
        self.remaps = parser.get_bytes(256 * 19)

    def write(self, parser):
        parser.put_bytes(self.colors)
        parser.put_bytes(self.remaps)

    def serialize(self):
        return {
            'colors': base64.b64encode(self.colors).decode() if self.colors else None,
            'remaps': base64.b64encode(self.remaps).decode() if self.remaps else None
        }

    @validate_schema(schema)
    def unserialize(self, data):
        self.colors = base64.b64decode(data['colors']) if data['colors'] else None
        self.remaps = base64.b64decode(data['remaps']) if data['remaps'] else None
