import argparse
import csv
import json
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TAGS_CSV_FILE = PROJECT_ROOT / "resources" / "tags.csv"

InputRows = list[list[str]]


def to_c_array(file_name: str, rows: InputRows) -> None:
    with open(file_name, "wb") as output_file:
        output_file.write(b"#include <stdlib.h>\n")
        output_file.write(b'#include "formats/taglist.h"\n\n')
        output_file.write(b"// This file is generated automatically\n\n")
        output_file.write(b"const sd_tag sd_taglist[] = {\n")

        for row in rows:
            row[2] = f'"{row[2]}"' if row[2] else "NULL"
            output_file.write(f'    {{"{row[0]}", {row[1]}, {row[2]}}},\n'.encode())

        output_file.write(b"};\n\n")
        output_file.write(b"const int sd_taglist_size = %d;\n\n" % len(rows))


def to_json(file_name: str, rows: InputRows) -> None:
    with open(file_name, "wb") as output_file:
        tags = [
            dict(tag=row[0], has_param=bool(row[1]), desc=str(row[2])) for row in rows
        ]
        output_file.write(json.dumps(tags, ensure_ascii=False, indent=4).encode())


def to_sqlite(file_name: str, rows: InputRows) -> None:
    with sqlite3.connect(file_name) as conn:
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS tags")
        c.execute(
            "CREATE TABLE tags (tag varchar(3) UNIQUE PRIMARY KEY, has_param int, description text)"
        )
        for row in rows:
            out = [row[0], int(row[1]), str(row[2])]
            c.execute(
                "INSERT INTO tags (tag,has_param,description) VALUES (?,?,?)", out
            )
        conn.commit()


def read_csv(filename: str) -> InputRows:
    with open(filename, "r") as in_file:
        reader = csv.reader(in_file)
        return [r for r in reader]


def main():
    parser = argparse.ArgumentParser(description="Converts json.csv to other formats")
    parser.add_argument(
        "-i",
        "--input_file",
        default=str(TAGS_CSV_FILE.absolute()),
        help="Input .CSV file",
    )
    parser.add_argument("output_file", help="Output .[json|c|sqlite] file")
    args = parser.parse_args()

    rows = read_csv(args.input_file)
    if args.output_file.endswith(".c"):
        to_c_array(args.output_file, rows)
    elif args.output_file.endswith(".json"):
        to_json(args.output_file, rows)
    elif args.output_file.endswith(".sqlite"):
        to_sqlite(args.output_file, rows)
    else:
        print("Unrecognized output file type")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
