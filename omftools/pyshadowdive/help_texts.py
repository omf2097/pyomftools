"""Long-form help pages for animation string tags."""

from pathlib import Path
from typing import Final

from markdown_it import MarkdownIt

HELP_TEXTS_DIR: Final[Path] = Path(__file__).parent.parent / "resources" / "help_texts"

_renderer = MarkdownIt("commonmark")


def help_text_path(tag: str) -> Path:
    return HELP_TEXTS_DIR / f"{tag}.md"


def has_help_text(tag: str) -> bool:
    return help_text_path(tag).is_file()


def help_text_markdown(tag: str) -> str | None:
    """Raw Markdown source of the tag's help page, or None when no page exists."""
    path = help_text_path(tag)
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def help_text(tag: str) -> str | None:
    """Help page rendered to an HTML fragment, or None when no page exists."""
    source = help_text_markdown(tag)
    if source is None:
        return None
    return _renderer.render(source)


def tags_with_help_text() -> list[str]:
    return sorted(p.stem for p in HELP_TEXTS_DIR.glob("*.md"))
