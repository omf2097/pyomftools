import argparse

from omftools.pyshadowdive.string_parser import Script, Errata


def join_erratas(erratas: list[Errata]) -> str:
    if not erratas:
        return ""
    out = ",".join([errata.value for errata in erratas])
    return f" ({out})"


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse an animation string")
    parser.add_argument("data", help="String data")
    args = parser.parse_args()
    data = Script.decode(args.data)
    for frame in data.frames:
        print(f"Frame {frame.key}{frame.duration}{join_erratas(frame.erratas)}:")
        for tag in frame.tags:
            print(f"\t{tag.key}: {tag.value}{join_erratas(tag.erratas)}")


if __name__ == "__main__":
    main()
