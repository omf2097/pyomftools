from .protos import OMFEntrypointMixin
from .afmove import AFMove
from .decorators import validate_schema


class AFFile(OMFEntrypointMixin):
    MOVE_MAX_NUMBER = 70

    schema = {
        'file_id': {'type': 'integer', 'required': True, 'min': 0, 'max': 65535},
        'exec_window': {'type': 'integer', 'required': True, 'min': 0, 'max': 65535},
        'endurance': {'type': 'float', 'required': True},
        'unknown_b': {'type': 'integer', 'required': True, 'min': 0, 'max': 255},
        'health': {'type': 'integer', 'required': True, 'min': 0, 'max': 65535},
        'forward_speed': {'type': 'float', 'required': True},
        'reverse_speed': {'type': 'float', 'required': True},
        'jump_speed': {'type': 'float', 'required': True},
        'fall_speed': {'type': 'float', 'required': True},
        'unknown_c': {'type': 'float', 'required': True, 'min': 0, 'max': 255},
        'unknown_d': {'type': 'float', 'required': True, 'min': 0, 'max': 255},
        'sound_table': {
            'type': 'list',
            'required': True,
            'schema': {
                'type': 'integer',
            }
        },
        'moves': {
            'type': 'dict',
            'required': True,
            'allow_unknown': True,
        }
    }

    def __init__(self):
        self.file_id = 0
        self.exec_window = 0
        self._endurance = 0
        self.unknown_b = 0
        self.health = 0
        self._forward_speed = 0
        self._reverse_speed = 0
        self._jump_speed = 0
        self._fall_speed = 0
        self.unknown_c = 0
        self.unknown_d = 0
        self.moves = {}
        self.sound_table = []

    def serialize(self):
        moves = {}
        for key, move in self.moves.items():
            moves[key] = move.serialize()

        return {
            'file_id': self.file_id,
            'exec_window': self.exec_window,
            'endurance': self.endurance,
            'unknown_b': self.unknown_b,
            'health': self.health,
            'forward_speed': self.forward_speed,
            'reverse_speed': self.reverse_speed,
            'jump_speed': self.jump_speed,
            'fall_speed': self.fall_speed,
            'unknown_c': self.unknown_c,
            'unknown_d': self.unknown_d,
            'moves': moves,
            'sound_table': self.sound_table,
        }

    @validate_schema(schema)
    def unserialize(self, data):
        self.file_id = data['file_id']
        self.exec_window = data['exec_window']
        self.endurance = data['endurance']
        self.unknown_b = data['unknown_b']
        self.health = data['health']
        self.forward_speed = data['forward_speed']
        self.reverse_speed = data['reverse_speed']
        self.jump_speed = data['jump_speed']
        self.fall_speed = data['fall_speed']
        self.unknown_c = data['unknown_c']
        self.unknown_d = data['unknown_d']
        self.moves = {}
        for k, m in data['moves'].items():
            move = AFMove()
            move.unserialize(m)
            self.moves[int(k)] = move
        self.sound_table = data['sound_table']

    def read(self, parser):
        self.file_id = parser.get_uint16()
        self.exec_window = parser.get_uint16()
        self._endurance = parser.get_uint32()
        self.unknown_b = parser.get_uint8()
        self.health = parser.get_uint16()
        self._forward_speed = parser.get_int32()
        self._reverse_speed = parser.get_int32()
        self._jump_speed = parser.get_int32()
        self._fall_speed = parser.get_int32()
        self.unknown_c = parser.get_uint8()
        self.unknown_d = parser.get_uint8()

        # Read all animations (up to max MOVE_MAX_NUMBER)
        while True:
            move_no = parser.get_uint8()
            if move_no >= self.MOVE_MAX_NUMBER:
                break
            move = AFMove()
            move.read(parser)
            self.moves[move_no] = move

        # Read sound table
        for m in range(0, 30):
            sound = parser.get_uint8()
            self.sound_table.append(sound)

    def write(self, parser):
        parser.put_uint16(self.file_id)
        parser.put_uint16(self.exec_window)
        parser.put_uint32(self._endurance)
        parser.put_uint8(self.unknown_b)
        parser.put_uint16(self.health)
        parser.put_int32(self._forward_speed)
        parser.put_int32(self._reverse_speed)
        parser.put_int32(self._jump_speed)
        parser.put_int32(self._fall_speed)
        parser.put_uint8(self.unknown_c)
        parser.put_uint8(self.unknown_d)

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
    def endurance(self):
        return self._endurance / 256.0

    @endurance.setter
    def endurance(self, value):
        self._endurance = int(value * 256.0)

    @property
    def forward_speed(self):
        return self._forward_speed / 256.0

    @forward_speed.setter
    def forward_speed(self, value):
        self._forward_speed = int(value * 256.0)

    @property
    def reverse_speed(self):
        return self._reverse_speed / 256.0

    @reverse_speed.setter
    def reverse_speed(self, value):
        self._reverse_speed = int(value * 256.0)

    @property
    def jump_speed(self):
        return self._jump_speed / 256.0

    @jump_speed.setter
    def jump_speed(self, value):
        self._jump_speed = int(value * 256.0)

    @property
    def fall_speed(self):
        return self._fall_speed / 256.0

    @fall_speed.setter
    def fall_speed(self, value):
        self._fall_speed = int(value * 256.0)
