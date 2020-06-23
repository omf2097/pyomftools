import argparse

from omftools.pyshadowdive.bk import BKFile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decompile BK file to JSON")
    parser.add_argument("input_file", help="Input .BK file")
    parser.add_argument("output_file", help="Output .json file")
    args = parser.parse_args()

    BKFile.load_native(args.input_file).save_json(args.output_file, indent=4)
    exit(0)
