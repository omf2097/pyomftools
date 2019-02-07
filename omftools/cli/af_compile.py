import argparse

from omftools.pyshadowdive.af import AFFile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compile AF file from JSON')
    parser.add_argument('input_file', help="Input .json file")
    parser.add_argument('output_file', help="Output .AF file")
    args = parser.parse_args()

    AFFile()\
        .load_json(args.input_file)\
        .save_native(args.output_file)
    exit(0)
