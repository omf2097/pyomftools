import argparse
import re

from omftools.pyshadowdive.language import LanguageFile

re_non_alphanumeric = re.compile(r'[\W]+')


def txt(text: str) -> str:
    o = text.strip()
    o = o.replace(' ', '_')
    o = re.sub(re_non_alphanumeric, '', o)
    o = o.upper()
    return o


def generate_enum(in_file: str, out_file: str):
    language = LanguageFile.load_native(in_file)
    assert len(language.titles) == len(language.strings)

    pairs = [(title, text) for title, text in zip(language.titles, language.strings)]
    with open(out_file, "wb") as fd:
        fd.write("enum TRANSLATION {\n".encode())

        for index, pair in enumerate(pairs, start=1):
            title, text = pair
            title = txt(title) if title else 'NONE'
            text = txt(text) if text else f'NONE'

            name = f"TXT_{index}__{title[:20]}__{text[:24]}"
            fd.write(f"    {name} = {index},\n".encode())

        fd.write("};\n".encode())


def main():
    parser = argparse.ArgumentParser(description="Generate enum header for language file")
    parser.add_argument("input_file", help="Input file")
    parser.add_argument("output_file", help="Output file")
    args = parser.parse_args()

    generate_enum(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
