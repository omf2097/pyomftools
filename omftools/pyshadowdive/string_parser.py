from dataclasses import dataclass, field
from enum import Enum
from typing import List

from .valid_tags import is_valid_tag, tag_has_arg, is_invalid_tag


class InvalidAnimationString(Exception):
    pass


class Errata(Enum):
    LEADING_ZERO = "LEADING_ZERO"
    LEADING_PLUS = "LEADING_PLUS"
    INVALID = "INVALID"


@dataclass(frozen=True, slots=True)
class Tag:
    key: str
    value: int | None = None
    erratas: list[Errata] = field(default_factory=list)

    def to_dict(self) -> dict:
        return dict(
            key=self.key,
            value=self.value,
            erratas=[errata.value for errata in self.erratas],
        )


@dataclass(frozen=True, slots=True)
class Frame:
    key: str
    duration: int
    tags: list[Tag]
    erratas: list[Errata] = field(default_factory=list)

    def to_dict(self):
        return dict(
            key=self.key,
            duration=self.duration,
            tags=[tag.to_dict() for tag in self.tags],
            erratas=[errata.value for errata in self.erratas],
        )


def is_frame_like(test: str) -> bool:
    return test.isupper() and test.isalpha()


def is_tag_like(test: str) -> bool:
    return test == "-" or (test.islower() and test.isalpha())


class Script:
    def __init__(self, frames: List[Frame]) -> None:
        self.frames: List[Frame] = frames

    @staticmethod
    def find_numeric_span(test: str, pos: int) -> int:
        if pos < len(test) and test[pos] in ["+", "-"]:
            pos += 1
        while pos < len(test) and test[pos].isdigit():
            pos += 1
        return pos

    @classmethod
    def read_int(cls, test: str, pos: int) -> tuple[int | None, list[Errata], int]:
        end = cls.find_numeric_span(test, pos)
        if pos == end:
            return None, [], end
        value = test[pos:end]

        erratas: list[Errata] = []
        sign = 1
        if value.startswith("+"):
            sign = 1
            value = value[1:]
            erratas.append(Errata.LEADING_PLUS)
        elif value.startswith("-"):
            sign = -1
            value = value[1:]

        if value.startswith("0") and len(value) > 1:
            erratas.append(Errata.LEADING_ZERO)

        return sign * int(value), erratas, end

    @classmethod
    def parse_frame(
        cls, in_str: str, pos: int
    ) -> tuple[str, int | None, list[Errata], int] | None:
        if not is_frame_like(in_str[pos]):
            return None
        key = in_str[pos]
        duration, erratas, pos = cls.read_int(in_str, pos + 1)
        return key, duration, erratas, pos

    @classmethod
    def parse_tag(
        cls, in_str: str, start_pos: int
    ) -> tuple[str, int | None, list[Errata], int] | None:
        if not is_tag_like(in_str[start_pos]):
            return None
        for test in range(3, 0, -1):
            end_pos = start_pos + test
            tag = in_str[start_pos:end_pos]

            if tag == "usw" and cls.find_numeric_span(in_str, end_pos) > end_pos:
                return None

            value: int | None = None
            erratas: list[Errata] = []
            if not is_valid_tag(tag):
                continue
            if tag_has_arg(tag):
                value, erratas, end_pos = cls.read_int(in_str, end_pos)
            elif cls.find_numeric_span(in_str, end_pos) > end_pos:
                return None  # If value is not expected and we got one, fail.
            return tag, value, erratas, end_pos
        return None

    @classmethod
    def parse_invalid_tag(
        cls, in_str: str, pos: int
    ) -> tuple[str, list[Errata], int] | None:
        tag = in_str[pos]
        if is_invalid_tag(tag):
            return tag, [Errata.INVALID], pos + 1
        return None

    @classmethod
    def parse_bad_frame(
        cls, in_str: str, pos: int
    ) -> tuple[str, int | None, list[Errata], int] | None:
        ch = in_str[pos]
        if not is_tag_like(ch):  # Expect lowercase frame key
            return None
        next_ch = in_str[pos + 1]
        if not next_ch.isdigit():
            return None  # Next char must be a digit

        # Read as normal, but convert frame key to uppercase.
        key = in_str[pos].upper()
        duration, erratas, pos = cls.read_int(in_str, pos + 1)
        return key, duration, erratas, pos

    @classmethod
    def parse_next_frame(cls, in_str: str, now: int) -> tuple[Frame, int] | None:
        if not in_str or now >= len(in_str):
            return None

        frame_key: str | None = None
        frame_duration: int | None = None
        frame_erratas: list[Errata] = []
        tags: list[Tag] = []

        while now < len(in_str):
            if frame_data := cls.parse_frame(in_str, now):
                frame_key, frame_duration, frame_erratas, now = frame_data
                continue
            if tag_data := cls.parse_tag(in_str, now):
                tag, value, erratas, now = tag_data
                tags.append(Tag(tag, value, erratas))
                continue
            if inv_tag_data := cls.parse_invalid_tag(in_str, now):
                tag, erratas, now = inv_tag_data
                tags.append(Tag(tag, None, erratas))
                continue
            if bad_frame_data := cls.parse_bad_frame(in_str, now):
                frame_key, frame_duration, frame_erratas, now = bad_frame_data
                continue
            if in_str[now] == "-":
                now += 1
                if frame_key is None or frame_duration is None:
                    tags.append(Tag("-", None, [Errata.INVALID]))
                    continue
                else:
                    break
            raise InvalidAnimationString(
                f"Unrecognized script element '{in_str[now]}'@{now}"
            )
        if frame_key is None or frame_duration is None:
            raise InvalidAnimationString("Frame missing a key or duration")
        return Frame(frame_key, frame_duration, tags, frame_erratas), now

    @classmethod
    def decode(cls, in_str: str) -> "Script":
        if not in_str or in_str == "!":
            return Script([])
        now = 0
        frames: List[Frame] = []
        while data := cls.parse_next_frame(in_str, now):
            frame, now = data
            frames.append(frame)
        return cls(frames)

    def encode(self) -> str:
        pieces: list[str] = []
        for frame in self.frames:
            tags: list[str] = []
            for tag in frame.tags:
                if tag.value is None:
                    repr_prefix = ""
                    repr_value = ""
                else:
                    repr_value = str(abs(tag.value))
                    repr_prefix = ""
                    if Errata.LEADING_PLUS in tag.erratas:
                        repr_prefix = "+"
                    elif tag.value < 0:
                        repr_prefix = "-"
                    if Errata.LEADING_ZERO in tag.erratas:
                        repr_prefix = f"{repr_prefix}0"
                tags.append("".join([tag.key, f"{repr_prefix}{repr_value}"]))
            frame_duration = str(frame.duration)
            if Errata.LEADING_ZERO in frame.erratas:
                frame_duration = f"0{frame_duration}"
            tags.append("".join([frame.key, frame_duration]))
            pieces.append("".join(tags))
        return "-".join(pieces)
