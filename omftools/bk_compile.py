import argparse

from .pyshadowdive.bk import BKFile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compile BK file from JSON')
    parser.add_argument('input_file', help="Input .json file")
    parser.add_argument('output_file', help="Output .BK file")
    args = parser.parse_args()

    f = BKFile()
    f.load_json(args.input_file)
    f.save_native(args.output_file)
    exit(0)
