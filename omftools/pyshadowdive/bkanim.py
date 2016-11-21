from .animation import Animation
from .protos import OMFObjectMixin
from .decorators import validate_schema


class BKAnim(Animation, OMFObjectMixin):
    schema = {**Animation.schema, **{
        'null': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'chain_hit': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'chain_no_hit': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'load_on_start': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'probability': {'type': 'integer', 'required': True, 'min': 0, 'max': 65535},
        'hazard_damage': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'footer_string': {'type': 'string', 'required': True},
    }}

    def __init__(self):
        super(BKAnim, self).__init__()
        self.null = 0
        self.chain_hit = 0
        self.chain_no_hit = 0
        self.load_on_start = 0
        self.probability = 0
        self.hazard_damage = 0
        self.footer_string = ""

    def read(self, parser):
        self.null = parser.get_uint8()
        self.chain_hit = parser.get_uint8()
        self.chain_no_hit = parser.get_uint8()
        self.load_on_start = parser.get_uint8()
        self.probability = parser.get_uint16()
        self.hazard_damage = parser.get_uint8()
        self.footer_string = parser.get_var_str(size_includes_zero=True)
        super(BKAnim, self).read(parser)

    def write(self, parser):
        parser.put_uint8(self.null)
        parser.put_uint8(self.chain_hit)
        parser.put_uint8(self.chain_no_hit)
        parser.put_uint8(self.load_on_start)
        parser.put_uint16(self.probability)
        parser.put_uint8(self.hazard_damage)
        parser.put_var_str(self.footer_string, size_includes_zero=True)
        super(BKAnim, self).write(parser)

    def serialize(self):
        return {**super(BKAnim, self).serialize(), **{
            'null': self.null,
            'chain_hit': self.chain_hit,
            'chain_no_hit': self.chain_no_hit,
            'load_on_start': self.load_on_start,
            'probability': self.probability,
            'hazard_damage': self.hazard_damage,
            'footer_string': self.footer_string,
        }}

    @validate_schema(schema)
    def unserialize(self, data):
        super(BKAnim, self).unserialize(data)
        self.null = data['null']
        self.chain_hit = data['chain_hit']
        self.chain_no_hit = data['chain_no_hit']
        self.load_on_start = data['load_on_start']
        self.probability = data['probability']
        self.hazard_damage = data['hazard_damage']
        self.footer_string = data['footer_string']
