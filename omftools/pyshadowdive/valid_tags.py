"""Animation-string tag table, loaded from resources/tags.csv."""

import csv
from pathlib import Path
from typing import Final

TAGS_CSV_FILE: Final[Path] = Path(__file__).parent.parent / "resources" / "tags.csv"
INVALID_TAGS: Final[set[str]] = {"c", "p", "o", "z"}


def _load_tags(path: Path) -> dict[str, tuple[bool, str]]:
    tags: dict[str, tuple[bool, str]] = {}
    with path.open("r", newline="", encoding="utf-8") as in_file:
        for row in csv.reader(in_file):
            if not row:
                continue
            tag, has_arg, description = row[0], row[1], row[2] if len(row) > 2 else ""
            assert tag not in tags, f"duplicate tag {tag!r} in {path}"
            tags[tag] = (bool(int(has_arg)), description)
    return tags


VALID_TAGS: Final[dict[str, tuple[bool, str]]] = _load_tags(TAGS_CSV_FILE)

VALID_TAG_KEYS: Final[set[str]] = set(VALID_TAGS.keys())


def describe_tag(tag: str) -> str:
    return VALID_TAGS[tag][1]


def tag_has_arg(tag: str) -> bool:
    return VALID_TAGS[tag][0]


def is_valid_tag(tag: str) -> bool:
    return tag in VALID_TAG_KEYS


def is_invalid_tag(tag: str) -> bool:
    return tag in INVALID_TAGS
