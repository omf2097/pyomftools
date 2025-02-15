import argparse
import os
import copy
from glob import glob
from dataclasses import dataclass
from shutil import copyfile

from natsort import natsorted
from jinja2 import Environment, PackageLoader, select_autoescape

from omftools.pyshadowdive.af import AFFile
from omftools.pyshadowdive.bk import BKFile
from omftools.pyshadowdive.tournament import TournamentFile
from omftools.pyshadowdive.sounds import SoundFile
from omftools.pyshadowdive.pic import PicFile
from omftools.pyshadowdive.altpals import AltPaletteFile
from omftools.pyshadowdive.utils.exceptions import OMFInvalidDataException
from omftools.pyshadowdive.palette import Palette
from omftools.pyshadowdive.language import LanguageFile

env = Environment(
    loader=PackageLoader(__name__), autoescape=select_autoescape(["html"])
)


@dataclass
class Filenames:
    af: list[str]
    bk: list[str]
    trn: list[str]
    pic: list[str]
    alt_pals: str
    sounds: str
    english: str
    german: str


har_names = [
    "Jaguar",
    "Shadow",
    "Thorn",
    "Pyros",
    "Electra",
    "Katana",
    "Shredder",
    "Flail",
    "Gargoyle",
    "Chronos",
    "Nova",
]

af_name_mappings = {f"FIGHTR{i}.AF": name for i, name in enumerate(har_names)}


def render(tpl_name: str, files: Filenames, filename: str, **args) -> bytes:
    return (
        env.get_template(tpl_name)
        .render(
            files=files,
            filename=filename,
            har_names=har_names,
            af_name_mappings=af_name_mappings,
            **args,
        )
        .encode()
    )


def generate_language(file: str, files: Filenames, output_dir: str) -> None:
    filename = os.path.basename(file)
    language = LanguageFile.load_native(file)

    with open(os.path.join(output_dir, f"{filename}.html"), "wb") as fd:
        fd.write(render("language_index.html", files, filename, language=language))


def generate_sounds(file: str, files: Filenames, output_dir: str) -> None:
    filename = "SOUNDS.DAT"
    sounds = SoundFile.load_native(file)

    for idx, sound in enumerate(sounds.sounds):
        if sound.data:
            sound.save_wav(os.path.join(output_dir, f"{filename}-{idx}.wav"))

    with open(os.path.join(output_dir, f"{filename}.html"), "wb") as fd:
        fd.write(render("sounds_index.html", files, filename, sounds=sounds))


def generate_pics(
    file: str, files: Filenames, output_dir: str, src_pal: Palette
) -> None:
    filename = os.path.basename(file)
    pic = PicFile.load_native(file)

    for idx, photo in enumerate(pic.photos):
        sprite_file = os.path.join(output_dir, f"{filename}-{idx}.png")
        try:
            photo.sprite.save_png(sprite_file, src_pal)
        except OMFInvalidDataException:
            print(f"Skipping {sprite_file}")

    with open(os.path.join(output_dir, f"{filename}.html"), "wb") as fd:
        fd.write(render("pic_index.html", files, filename, pic=pic))


def generate_altpals(
    alt_pals: AltPaletteFile, files: Filenames, output_dir: str
) -> None:
    filename = "ALTPALS.DAT"

    with open(os.path.join(output_dir, f"{filename}.html"), "wb") as fd:
        fd.write(render("altpals_index.html", files, filename, alt_pals=alt_pals))


def generate_trn(file: str, files: Filenames, output_dir: str) -> None:
    filename = os.path.basename(file)
    trn = TournamentFile.load_native(file)

    for idx, sprite in enumerate(trn.locale_logos):
        sprite_file = os.path.join(output_dir, f"{filename}-{idx}.png")
        try:
            sprite.save_png(sprite_file, trn.palette)
        except OMFInvalidDataException:
            print(f"Skipping {sprite_file}")

    with open(os.path.join(output_dir, f"{filename}.html"), "wb") as fd:
        fd.write(render("trn_index.html", files, filename, trn=trn))


def generate_bk(file: str, files: Filenames, output_dir: str) -> None:
    filename = os.path.basename(file)
    bk = BKFile.load_native(file)

    bk.save_background(os.path.join(output_dir, f"{filename}-bg.png"))

    pal = copy.deepcopy(bk.palettes[0].colors)

    for key, animation in bk.animations.items():
        for idx, sprite in enumerate(animation.sprites):
            sprite_file = os.path.join(output_dir, f"{filename}-{key}-{idx}.png")
            try:
                sprite.save_png(sprite_file, pal)
            except OMFInvalidDataException:
                print(f"Skipping {sprite_file}")

    with open(os.path.join(output_dir, f"{filename}.html"), "wb") as fd:
        fd.write(render("bk_index.html", files, filename, bk=bk))


def generate_af(
    file: str, files: Filenames, output_dir: str, alt_pals: AltPaletteFile
) -> None:
    filename = os.path.basename(file)
    af = AFFile.load_native(file)

    for key, animation in af.moves.items():
        for idx, sprite in enumerate(animation.sprites):
            sprite_file = os.path.join(output_dir, f"{filename}-{key}-{idx}.png")
            try:
                sprite.save_png(sprite_file, alt_pals.palettes[0])
            except OMFInvalidDataException:
                print(f"Skipping {sprite_file}")

    with open(os.path.join(output_dir, f"{filename}.html"), "wb") as fd:
        fd.write(render("af_index.html", files, filename, af=af))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate HTML pages for OMF files")
    parser.add_argument("input_dir", help="Input directory")
    parser.add_argument("output_dir", help="Output directory")
    args = parser.parse_args()

    af_files = glob(os.path.join(args.input_dir, "*.AF"))
    bk_files = glob(os.path.join(args.input_dir, "*.BK"))
    trn_files = glob(os.path.join(args.input_dir, "*.TRN"))
    pic_files = glob(os.path.join(args.input_dir, "*.PIC"))
    alt_pals_file = os.path.join(args.input_dir, "ALTPALS.DAT")
    sounds_file = os.path.join(args.input_dir, "SOUNDS.DAT")
    english_file = os.path.join(args.input_dir, "ENGLISH.DAT")
    german_file = os.path.join(args.input_dir, "GERMAN.DAT")

    files = Filenames(
        af=natsorted([os.path.basename(v) for v in af_files]),
        bk=[os.path.basename(v) for v in bk_files],
        trn=[os.path.basename(v) for v in trn_files],
        pic=[os.path.basename(v) for v in pic_files],
        alt_pals=os.path.basename(alt_pals_file),
        sounds=os.path.basename(sounds_file),
        english=os.path.basename(english_file),
        german=os.path.basename(german_file),
    )

    # palettes file
    alt_pals = AltPaletteFile.load_native(alt_pals_file)
    src_pal = copy.deepcopy(BKFile.load_native(bk_files[0]).palettes[0].colors)

    print("Generating ALTPALS.DAT")
    generate_altpals(alt_pals, files, args.output_dir)

    print("Generating SOUNDS.DAT")
    generate_sounds(sounds_file, files, args.output_dir)

    print("Generating ENGLISH.DAT")
    generate_language(english_file, files, args.output_dir)

    print("Generating GERMAN.DAT")
    generate_language(german_file, files, args.output_dir)

    for pic_file in pic_files:
        print(f"Generating {pic_file}")
        generate_pics(pic_file, files, args.output_dir, src_pal)

    for trn_file in trn_files:
        print(f"Generating {trn_file}")
        generate_trn(trn_file, files, args.output_dir)

    for af_file in af_files:
        print(f"Generating {af_file}")
        generate_af(af_file, files, args.output_dir, alt_pals)

    for bk_file in bk_files:
        print(f"Generating {bk_file}")
        generate_bk(bk_file, files, args.output_dir)

    copyfile(
        os.path.join(args.output_dir, f"ARENA0.BK.html"),
        os.path.join(args.output_dir, "index.html"),
    )

    exit(0)


if __name__ == "__main__":
    main()
