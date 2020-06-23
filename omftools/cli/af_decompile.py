import argparse

from omftools.pyshadowdive.af import AFFile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decompile AF file to JSON")
    parser.add_argument("input_file", help="Input .AF file")
    parser.add_argument("output_file", help="Output .json file")
    args = parser.parse_args()

    AFFile.load_native(args.input_file).save_json(args.output_file, indent=4)
    exit(0)
