import pytest

from omftools.pyshadowdive.string_parser import Script
from tests.animation_strings import TEST_STRINGS


@pytest.mark.parametrize("animation_string", TEST_STRINGS)
def test_string(animation_string):
    parsed = Script.decode(animation_string)
    assert parsed.encode() == animation_string
