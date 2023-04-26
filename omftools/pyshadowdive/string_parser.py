from dataclasses import dataclass
from pprint import pprint
from typing import List, Tuple, Dict, Optional

from .valid_tags import is_valid_tag, tag_has_arg


class InvalidAnimationString(Exception):
    pass


@dataclass
class Frame:
    key: int
    duration: int
    original: str
    tags: Dict[str, Optional[int]]


def get_total_frames_duration(frames: List[Frame]) -> int:
    return sum(frame.duration for frame in frames)


def get_frame_at_time_offset(
    frames: List[Frame], offset: int
) -> Tuple[Optional[int], Optional[Frame]]:
    current_start: int = 0
    for pos, frame in enumerate(frames):
        current_end = current_start + frame.duration
        if current_start <= offset < current_end:
            return pos, frame
        current_start = current_end
    return None, None


def _read_next_int(in_str: str, start_pos: int) -> Tuple[Optional[int], int]:
    current_pos = start_pos
    while current_pos < len(in_str) and in_str[current_pos].isdigit():
        current_pos += 1
    out: str = in_str[start_pos:current_pos]
    return int(out) if out else None, current_pos


def _read_next_tag(in_str: str, start_pos: int) -> Tuple[str, Optional[int], int]:
    for test in range(3, 0, -1):
        end_pos = start_pos + test
        possible_tag: str = in_str[start_pos:end_pos]
        possible_arg: Optional[int] = None
        if not is_valid_tag(possible_tag):
            continue
        if tag_has_arg(possible_tag):
            possible_arg, end_pos = _read_next_int(in_str, end_pos)
            assert possible_arg is not None, f"Tag {possible_tag} expected argument"
        return possible_tag, possible_arg, end_pos
    raise InvalidAnimationString("Unable to recognize tag")


def parse_string(animation_string: str) -> List[Frame]:
    pos = 0
    current_tags: Dict[str, Optional[int]] = {}
    frames: List[Frame] = []
    frame_start: int = 0
    while pos < len(animation_string):
        ch = animation_string[pos]

        if ch.isupper():  # Attempt to read a frame key & duration
            frame_key = ord(ch) - 65
            frame_duration, pos = _read_next_int(animation_string, pos + 1)
            assert frame_duration is not None, "No frame duration"
            frames.append(
                Frame(
                    tags=current_tags,
                    duration=frame_duration,
                    original=animation_string[frame_start:pos],
                    key=frame_key,
                )
            )
            current_tags = dict()
        elif ch.islower():  # Attempt to read a tag
            tag_name, tag_value, pos = _read_next_tag(animation_string, pos)
            assert (
                tag_name not in current_tags
            ), "Tag value is already set -- duplicate tag ?"
            current_tags[tag_name] = tag_value
        elif ch == "-":  # Skip frame separator
            pos += 1
            frame_start = pos
        elif ch in ["u", "c", "p", "o", "z"]:  # Skip known fillers
            pos += 1
        else:
            raise InvalidAnimationString(
                f"Invalid character in animation string pos = {pos}, ch = '{ch}'"
            )
    return frames


test_frames = parse_string(
    "Z10-bps0bpd63bpn255bpp64bpb0s1sdsc1l60sp10rB10-bps0bpd63bpn144bpp64m5mp100mn10rB10-bps0bpd63bpn144bpp0bpb64rB10-bps0bpd0bpn144bpp0Z10-Z400-bps0bpd63bpn144bpp64bpb0s1sc1sdl60sp10A10-bps0bpd63bpn144bpp64m6mp100mn10md5A10-bps0bpd63bpn144bpp0bpb64A10-bps0bpd0bpn144bpp0Z400-bps0bpd63bpn144bpp64bpb0s1sdsc1l60sp10m15mp100mn1B10-bps0bpd63bpn255bpp64B10-bps0bpd63bpn255bpp0bpb64B10-bps0bpd0bpn255bpp0Z10-Z1600"
)
pprint(test_frames)
