import argparse
import json
import os
import sys
from dataclasses import dataclass
from glob import glob

from omftools.pyshadowdive.af import AFFile
from omftools.pyshadowdive.afmove import AFMove
from omftools.pyshadowdive.bk import BKFile
from omftools.pyshadowdive.bkanim import BKAnimation
from omftools.pyshadowdive.string_parser import Script


@dataclass
class AnimString:
    data: str
    source_file: str
    type: str
    source_animation: int | None = None
    source_frame: int | None = None

    def to_dict(self) -> dict:
        return dict(
            data=list(map(lambda f: f.to_dict(), Script.decode(self.data).frames)),
            source_file=self.source_file,
            source_animation=self.source_animation,
            original=self.data,
            type=self.type,
        )


def process_af(af_file) -> list[AnimString]:
    source_file = os.path.basename(af_file)
    af = AFFile.load_native(af_file)
    out: list[AnimString] = []
    for animation_index, move in af.moves.items():  # type: int, AFMove
        if move.base_string:
            out.append(
                AnimString(
                    data=move.base_string,
                    type="base_string",
                    source_file=source_file,
                    source_animation=animation_index,
                )
            )
        if move.extra_strings:
            for extra_index, extra_string in enumerate(
                move.extra_strings
            ):  # type: int, str
                out.append(
                    AnimString(
                        data=extra_string,
                        type=f"extra_string[{extra_index}]",
                        source_file=source_file,
                        source_animation=animation_index,
                    )
                )
    return out


def process_bk(bk_file) -> list[AnimString]:
    source_file = os.path.basename(bk_file)
    bk = BKFile.load_native(bk_file)
    out: list[AnimString] = []
    for animation_index, animation in bk.animations.items():  # type: int, BKAnimation
        if animation.footer_string:
            out.append(
                AnimString(
                    data=animation.footer_string,
                    type="footer_string",
                    source_file=source_file,
                    source_animation=animation_index,
                )
            )
        if animation.base_string:
            out.append(
                AnimString(
                    data=animation.base_string,
                    type="base_string",
                    source_file=source_file,
                    source_animation=animation_index,
                )
            )
        if animation.extra_strings:
            for extra_index, extra_string in enumerate(
                animation.extra_strings
            ):  # type: int, str
                out.append(
                    AnimString(
                        data=extra_string,
                        type=f"extra_string[{extra_index}]",
                        source_file=source_file,
                        source_animation=animation_index,
                    )
                )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reads all animation strings to a JSON file"
    )
    parser.add_argument("input_dir", help="Input directory")
    parser.add_argument("output_file", help="Output .json file")
    args = parser.parse_args()

    af_files = glob(os.path.join(args.input_dir, "*.AF"))
    bk_files = glob(os.path.join(args.input_dir, "*.BK"))
    strings: list[AnimString] = []

    for af_file in af_files:
        print(f"Processing {af_file}")
        strings.extend(process_af(af_file))

    for bk_file in bk_files:
        print(f"Processing {bk_file}")
        strings.extend(process_bk(bk_file))

    with open(args.output_file, "wb") as fd:
        data = [s.to_dict() for s in strings]
        fd.write(json.dumps(data, indent=4, ensure_ascii=False).encode())

    sys.exit(0)


if __name__ == "__main__":
    main()
