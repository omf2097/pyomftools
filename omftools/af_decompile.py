import argparse

from .pyshadowdive.af import AFFile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decompile AF file to JSON')
    parser.add_argument('input_file', help="Input .AF file")
    parser.add_argument('output_file', help="Output .json file")
    args = parser.parse_args()

    f = AFFile()
    f.load_af(args.input_file)
    f.save_json(args.output_file, indent=4)
