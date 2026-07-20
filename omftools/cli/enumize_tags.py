import argparse
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TAGS_CSV_FILE = PROJECT_ROOT / "resources" / "tags.csv"

InputRows = list[list[str]]

# Map symbol characters that are not valid in C identifiers to words.
SYMBOLS = {"-": "_MINUS", "+": "_PLUS", "=": "_EQ"}


def to_ident(tag: str) -> str:
    out = "".join(SYMBOLS.get(ch, ch) for ch in tag)
    return f"TAG_{out.upper()}"


def read_csv(filename: str) -> InputRows:
    with open(filename, "r") as in_file:
        reader = csv.reader(in_file)
        return [r for r in reader]


def generate_enum(in_file: str, out_file: str) -> None:
    rows = read_csv(in_file)

    idents = [to_ident(row[0]) for row in rows]
    assert len(idents) == len(set(idents)), "Generated enum names are not unique"

    with open(out_file, "wb") as fd:
        fd.write(b"#ifndef SCRIPT_TAG_H\n")
        fd.write(b"#define SCRIPT_TAG_H\n\n")
        fd.write(b"typedef enum script_tag {\n")

        for index, ident in enumerate(idents):
            assign = " = 0" if index == 0 else ""
            fd.write(f"    {ident}{assign},\n".encode())

        fd.write(b"    TAG_INVALID = 0xFF,\n")
        fd.write(b"} script_tag;\n\n")
        fd.write(b"#endif // SCRIPT_TAG_H\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a C enum header for all script tags"
    )
    parser.add_argument(
        "-i",
        "--input_file",
        default=str(TAGS_CSV_FILE.absolute()),
        help="Input .CSV file",
    )
    parser.add_argument("output_file", help="Output .h file")
    args = parser.parse_args()

    generate_enum(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
