from PIL import Image
from typing import List

from .types import RawImage
from ..palette import Palette


def generate_png(data: RawImage, w: int, h: int, palette: Palette) -> Image.Image:
    n_pal: List[int] = []
    for triplet in palette.data:
        n_pal.extend(triplet)
    img = Image.new("P", (w, h), color=0)
    img.putdata(data)
    img.putpalette(n_pal)
    return img


def save_png(img: Image.Image, filename: str, transparency=None):
    with open(filename, "wb") as fd:
        img.save(fd, "png", transparency=transparency)
