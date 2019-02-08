import argparse
import os
from glob import glob

from jinja2 import Environment, PackageLoader, select_autoescape

from omftools.pyshadowdive.af import AFFile
from omftools.pyshadowdive.bk import BKFile
from omftools.pyshadowdive.altpals import AltPalettes
from omftools.pyshadowdive.utils.exceptions import OMFInvalidDataException
from omftools.pyshadowdive.utils.types import Palette

env = Environment(
    loader=PackageLoader(__name__),
    autoescape=select_autoescape(['html'])
)


def generate_bk(file: str, bk_filenames: list, af_filenames: list, output_dir: str, alt_pals: AltPalettes):
    filename = os.path.basename(file)
    bk = BKFile().load_native(file)

    bk.save_background(os.path.join(output_dir, f'{filename}-bg.png'))

    pal = bk.palettes[0].colors
    for m in range(48):
        pal[m] = alt_pals.palettes[0][m+48]

    for key, animation in bk.animations.items():
        for idx, sprite in enumerate(animation.sprites):
            sprite_file = os.path.join(output_dir, f'{filename}-{key}-{idx}.png')
            try:
                sprite.save_png(sprite_file, pal)
            except OMFInvalidDataException:
                print(f"Skipping {sprite_file}")

    with open(os.path.join(output_dir, f'{filename}.html'), 'wb') as fd:
        tpl = env.get_template('bk_index.html')
        content = tpl.render(
            bk=bk,
            bk_files=bk_filenames,
            af_files=af_filenames,
            filename=filename)
        fd.write(content.encode())


def generate_af(file: str, bk_filenames: list, af_filenames: list, output_dir: str, alt_pals: AltPalettes):
    filename = os.path.basename(file)
    af = AFFile().load_native(file)

    pal: Palette = [(0, 0, 0) for _ in range(256)]
    for m in range(48):
        pal[m] = alt_pals.palettes[0][m+48]

    for key, animation in af.moves.items():
        for idx, sprite in enumerate(animation.sprites):
            sprite_file = os.path.join(output_dir, f'{filename}-{key}-{idx}.png')
            try:
                sprite.save_png(sprite_file, pal)
            except OMFInvalidDataException:
                print(f"Skipping {sprite_file}")

    with open(os.path.join(output_dir, f'{filename}.html'), 'wb') as fd:
        tpl = env.get_template('af_index.html')
        content = tpl.render(
            af=af,
            bk_files=bk_filenames,
            af_files=af_filenames,
            filename=filename)
        fd.write(content.encode())


def main():
    parser = argparse.ArgumentParser(description='Generate HTML pages for OMF files')
    parser.add_argument('input_dir', help="Input directory")
    parser.add_argument('output_dir', help="Output directory")
    args = parser.parse_args()

    af_files = glob(os.path.join(args.input_dir, '*.AF'))
    bk_files = glob(os.path.join(args.input_dir, '*.BK'))

    af_filenames = [os.path.basename(v) for v in af_files]
    bk_filenames = [os.path.basename(v) for v in bk_files]
    alt_pals_filename = os.path.join(args.input_dir, 'ALTPALS.DAT')

    # palettes file
    alt_pals = AltPalettes().load_native(alt_pals_filename)

    for af_file in af_files:
        print(f"Generating {af_file}")
        generate_af(af_file, bk_filenames, af_filenames, args.output_dir, alt_pals)

    for bk_file in bk_files:
        print(f"Generating {bk_file}")
        generate_bk(bk_file, bk_filenames, af_filenames, args.output_dir, alt_pals)

    exit(0)


if __name__ == "__main__":
    main()
