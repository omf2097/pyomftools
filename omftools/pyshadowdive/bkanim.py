from validx import Str, Dict

from .animation import Animation
from .utils.validator import UInt8, UInt16


BK_ANIMATION_NAMES = {
    6: "Round",
    7: "Number",
    8: "You lose",
    9: "You win",
    10: "Fight",
    11: "Ready",
    20: "Left wall hit",
    21: "Right wall hit",
    24: "Dust 1",
    25: "Dust 2",
    26: "Dust 3",
    27: "Match marker",
}


class BKAnimation(Animation):
    __slots__ = (
        "null",
        "chain_hit",
        "chain_no_hit",
        "repeat",
        "probability",
        "hazard_damage",
        "footer_string",
    )

    schema = Dict(
        {
            **Animation.schema.schema,
            **{
                "null": UInt8,
                "chain_hit": UInt8,
                "chain_no_hit": UInt8,
                "repeat": UInt8,
                "probability": UInt16,
                "hazard_damage": UInt8,
                "footer_string": Str(),
            },
        }
    )

    def __init__(self):
        super(BKAnimation, self).__init__()
        self.null: int = 0
        self.chain_hit: int = 0
        self.chain_no_hit: int = 0
        self.repeat: int = 0
        self.probability: int = 0
        self.hazard_damage: int = 0
        self.footer_string: str = ""

    @staticmethod
    def get_name(index: int):
        if index in BK_ANIMATION_NAMES:
            return BK_ANIMATION_NAMES[index]
        return None

    def read(self, parser):
        self.null = parser.get_uint8()
        self.chain_hit = parser.get_uint8()
        self.chain_no_hit = parser.get_uint8()
        self.repeat = parser.get_uint8()
        self.probability = parser.get_uint16()
        self.hazard_damage = parser.get_uint8()
        self.footer_string = parser.get_var_str(size_includes_zero=True)
        super(BKAnimation, self).read(parser)
        return self

    def write(self, parser):
        parser.put_uint8(self.null)
        parser.put_uint8(self.chain_hit)
        parser.put_uint8(self.chain_no_hit)
        parser.put_uint8(self.repeat)
        parser.put_uint16(self.probability)
        parser.put_uint8(self.hazard_damage)
        parser.put_var_str(self.footer_string, size_includes_zero=True)
        super(BKAnimation, self).write(parser)

    def serialize(self):
        return {
            **super(BKAnimation, self).serialize(),
            **{
                "null": self.null,
                "chain_hit": self.chain_hit,
                "chain_no_hit": self.chain_no_hit,
                "repeat": self.repeat,
                "probability": self.probability,
                "hazard_damage": self.hazard_damage,
                "footer_string": self.footer_string,
            },
        }

    def unserialize(self, data):
        super(BKAnimation, self).unserialize(data)
        self.null = data["null"]
        self.chain_hit = data["chain_hit"]
        self.chain_no_hit = data["chain_no_hit"]
        self.repeat = data["repeat"]
        self.probability = data["probability"]
        self.hazard_damage = data["hazard_damage"]
        self.footer_string = data["footer_string"]
        return self
