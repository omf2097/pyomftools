# AGENTS.md

This file provides guidance to AI coding assistants when working with code in this repository.

## Project Overview

PyOMFTools is a Python library for decompiling and compiling One Must Fall 2097 (OMF2097) game data files. It handles two main binary file formats:
- **AF files**: Fighter animation and move data
- **BK files**: Background/arena data with animations and palettes

The library provides bidirectional conversion between binary formats and JSON for easier editing and analysis.

## Setup and Environment

1. Requires Python 3.12
2. Uses Poetry for dependency management
3. Setup:
   ```bash
   poetry env use 3.12
   poetry install --no-root
   poetry shell
   ```

## Common Commands

### Running CLI Tools

All CLI tools are run as Python modules:

```bash
# AF file operations
python -m omftools.cli.af_decompile <input.AF> <output.json>
python -m omftools.cli.af_compile <input.json> <output.AF>

# BK file operations
python -m omftools.cli.bk_decompile <input.BK> <output.json>
python -m omftools.cli.bk_compile <input.json> <output.BK>

# Generate taglist.c from tags.csv
python -m omftools.cli.tags -i omftools/resources/tags.csv taglist.c

# Other utilities
python -m omftools.cli.sounds_decompile
python -m omftools.cli.parse_string
python -m omftools.cli.anim_strings
python -m omftools.cli.generate_html
python -m omftools.cli.enumize_translation
```

### Testing and Code Quality

```bash
# Run tests
poetry run pytest

# Run single test
poetry run pytest tests/test_parser.py

# Type checking
poetry run mypy omftools

# Code formatting
poetry run black omftools tests
```

## Architecture

### Core Design Pattern: Entrypoint + DataObject

The codebase uses an abstract base class hierarchy defined in `omftools/pyshadowdive/protos.py`:

- **`DataObject`**: Base class for any object that can be read/written from binary and serialized to/from JSON
  - `read(parser)` / `write(parser)`: Binary format I/O
  - `serialize()` / `unserialize(data)`: JSON conversion

- **`Entrypoint`**: Extends `DataObject` for top-level file formats (AF, BK)
  - Adds `load_native()` / `save_native()`: Load/save binary files
  - Adds `load_json()` / `save_json()`: Load/save JSON files
  - Includes validation via `validx` schema

### Binary Parsing

`omftools/pyshadowdive/utils/parser.py` contains `BinaryParser`, which:
- Wraps a file handle for reading/writing binary data
- Provides typed methods: `get_uint8()`, `get_uint16()`, `put_int32()`, etc.
- Handles little-endian byte order
- Supports XOR encryption/decryption via `set_xor_key()`
- Uses CP437 encoding for strings (DOS character set)

### File Format Classes

**AF Files** (`omftools/pyshadowdive/af.py`):
- Contains fighter stats (health, speed, endurance)
- Up to 70 moves (`AFMove` objects)
- Each move contains animations with sprites
- Sound table mapping (30 entries)
- Properties have "real" variants (e.g., `real_endurance`) that convert from fixed-point (value/256.0)

**BK Files** (`omftools/pyshadowdive/bk.py`):
- Background image (VGA palette format)
- Up to 50 animations (`BKAnimation` objects)
- Multiple color palettes (`PaletteMapping`)
- Sound table mapping (30 entries)
- Background can be exported as PNG via `save_background()`

### Sprite Deduplication

AF files use an index-based sprite deduplication system:
- Sprites can be marked as "missing" with an index reference
- After reading all moves, missing sprites are resolved by finding the sprite with the matching index
- See `af.py:118-126` for the deduplication logic

### Validation

Uses `validx` library for schema validation when loading JSON:
- Custom validators in `omftools/pyshadowdive/utils/validator.py` (UInt8, UInt16, etc.)
- Schemas defined as class variables on each `Entrypoint`
- Validation errors are caught and formatted in `protos.py:92-97`

### CLI Structure

All CLI tools in `omftools/cli/` follow a simple pattern:
- Use `argparse` for argument parsing
- Load file via `FileType.load_native()` or `FileType.load_json()`
- Process as needed
- Save via `save_native()` or `save_json()`

## Key Dependencies

- **Pillow**: Image processing (PNG export from VGA palette data)
- **validx**: Schema validation for JSON data
- **Jinja2**: Template rendering (for HTML generation)
- **natsort**: Natural sorting for data
- **requests**: HTTP requests (for web resources)
