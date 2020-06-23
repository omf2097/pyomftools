import argparse

from omftools.pyshadowdive.sounds import SoundFile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decompile SOUNDS.DAT file to JSON")
    parser.add_argument("input_file", help="Input .AF file")
    parser.add_argument("output_file", help="Output .json file")
    args = parser.parse_args()

    SoundFile().load_native(args.input_file).save_json(args.output_file, indent=4)
    exit(0)
