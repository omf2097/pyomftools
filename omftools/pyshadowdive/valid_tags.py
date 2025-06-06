from typing import Final

INVALID_TAGS: Final[set[str]] = {"c", "p", "o", "z"}

# Tag: (has_argument, description)
VALID_TAGS: Final[dict[str, tuple[bool, str]]] = {
    "aa": (False, ""),
    "ab": (False, ""),
    "ac": (False, "Turn the HAR to face the center of the arena"),
    "ad": (False, ""),
    "ae": (False, ""),
    "af": (False, "Freeze opponent HAR"),
    "ag": (False, ""),
    "ai": (False, ""),
    "am": (False, "Tells the HAR when to stop walking"),
    "ao": (False, ""),
    "as": (False, "Wandering fire pit orb"),
    "at": (
        False,
        "Sets object position behind enemy har, used only by chronos' teleport",
    ),
    "aw": (False, "Tells if the HAR can pass through walls"),
    "ax": (False, ""),
    "ar": (False, "Reverse player direction"),
    "al": (False, ""),
    "b": (False, ""),
    "b1": (False, ""),
    "b2": (False, ""),
    "bb": (True, "Vertical screen shake"),
    "be": (False, "Block the end of the round"),
    "bf": (True, "Blend finish"),
    "bh": (False, ""),
    "bl": (True, "Horizontal screen shake with magnitude n"),
    "bm": (True, "Animation to play while doing something"),
    "bj": (True, "Jump to animation <n>"),
    "bs": (True, "Blend start"),
    "bu": (False, "Used by jaguar's destruct to move to center of arena"),
    "bw": (False, ""),
    "bx": (False, ""),
    "bpd": (True, "Reference palette index"),
    "bps": (True, "Start palette index"),
    "bpn": (True, "Palette entry count"),
    "bpf": (False, "Fighter palette selection"),
    "bpp": (True, "Initial and final color level"),
    "bpb": (True, "Initial color level"),
    "bpo": (False, "Disable palette effects"),
    "bz": (False, "Color tint effect"),
    "ba": (True, "Credits fade effect remapping (?)"),
    "bc": (True, "Credits fade effect color count"),
    "bd": (False, "Credits fade effect switch"),
    "bg": (False, "Credits fade effect unknown"),
    "bi": (True, "Credits fade effect color start index"),
    "bk": (True, ""),
    "bn": (False, ""),
    "bo": (True, ""),
    "br": (False, "Draw additively"),
    "bt": (False, "Dark tint, used by shadow HAR"),
    "by": (False, ""),
    "cf": (
        False,
        "Only used by shadow scrap, works with 'bm' tag to walk to far corner of arena",
    ),
    "cg": (False, ""),
    "cl": (False, ""),
    "cp": (False, ""),
    "cw": (False, ""),
    "cx": (True, ""),
    "cy": (True, ""),
    "d": (True, "Re-enter animation at N ticks"),
    "e": (False, "Set position to enemy position"),
    "f": (True, "Flip sprite vertically"),
    "g": (False, "Set position to ground and zero velocity"),
    "h": (False, "Set velocity to 0"),
    "i": (False, ""),
    "jf2": (False, "Allow chaining to destruction"),
    "jf": (False, "Allow chaining to scrap"),
    "jg": (
        False,
        "Every HAR uses this in the 'getup' animation, purpose unknown, might be 'grab' (like standing throw)?",
    ),
    "jh": (False, "Allow chaining to 'high' moves"),
    "jj": (False, "Allow chaining to airborne moves"),
    "jl": (False, "Allow chaining to 'low' moves"),
    "jm": (False, "Allow chaining to 'mid' moves"),
    "jp": (False, ""),
    "jz": (False, "Allow chaining to anything? (Katana head stomp)"),
    "jn": (True, "Allow frame to chain to animation N"),
    "k": (True, "Knockback on hit"),
    "l": (True, "Sound loudness"),
    "ma": (
        True,
        "Sets angle of new object in degrees. Velocity is then x=cos(ma), y=sin(ma).",
    ),
    "mc": (False, ""),
    "md": (True, "Destroy animation N"),
    "mg": (True, "Gravity for spawned animation, default 0"),
    "mi": (True, ""),
    "mm": (True, "Manipulate mrx and mry calculations"),
    "mn": (True, ""),
    "mo": (False, ""),
    "mp": (True, "Feature bitmask"),
    "mrx": (True, "Randomize new animation X"),
    "mry": (True, "Randomize new animation Y"),
    "ms": (False, "Set special Y position for object; y = -4 * (y - 188)"),
    "mu": (True, ""),
    "mx": (True, "X position of new animation"),
    "my": (True, "Y position of new animation"),
    "m": (True, "Create instance of animation N"),
    "n": (False, "Disable collision detection for the current frame"),
    "ox": (True, "Set sprite X correction for this frame"),
    "oy": (True, "Set sprite Y correction for this frame"),
    "pa": (False, "Enable color effect for HAR palette effects"),
    "pb": (True, "N < 512"),
    "pc": (True, "N < 512"),
    "pd": (True, "n < 256. Reference color index."),
    "pe": (False, "Switch HAR palette effect handling to the other HAR."),
    "ph": (False, "Disable HAR palette effects if HAR is not in damage animation (9)"),
    "pp": (True, "Duration of HAR palette effect in ticks."),
    "ps": (False, "Update the color palette"),
    "ptd": (True, "n < 128 Effect intensity."),
    "ptp": (True, "N < 128"),
    "ptr": (True, "N < 128"),
    "q": (True, "Enable hit on current and next n-1 frames."),
    "r": (False, "Flip sprite horizontally"),
    "s": (True, "Play sound N from sound table footer"),
    "sa": (False, ""),
    "sb": (True, "Sound panning start"),
    "sc": (True, ""),
    "sd": (False, ""),
    "se": (True, "Sound panning end 1"),
    "sf": (True, "Sound frequency"),
    "sl": (True, "Sound panning end 2"),
    "smf": (True, "Stop playing music track N"),
    "smo": (True, "Play music track N"),
    "sp": (True, ""),
    "sw": (True, ""),
    "t": (False, "Prevent sound from playing if other HAR is blocking"),
    "ua": (False, "Sets enemy HAR to damage animation, if not already set."),
    "ub": (False, "Motion blur effect"),
    "uc": (False, ""),
    "ud": (False, ""),
    "ue": (False, "Damage enemy if on the ground"),
    "uf": (False, ""),
    "ug": (False, ""),
    "uh": (False, ""),
    "uj": (False, ""),
    "ul": (False, ""),
    "un": (False, ""),
    "ur": (False, ""),
    "us": (False, ""),
    "uz": (False, ""),
    "v": (False, "Velocity modifier for x/y"),
    "vsx": (False, ""),
    "vsy": (False, ""),
    "w": (False, "Sprite caching related ?"),
    "x-": (True, "Set X coordinate to -N"),
    "x+": (True, "Set X coordinate to +N"),
    "x=": (True, "Interpolate X coordinate to N by next frame"),
    "x": (True, "Scale image as % of width (default 100)"),
    "y-": (True, "Set Y coordinate to -N"),
    "y+": (True, "Set Y coordinate to +N"),
    "y=": (True, "Interpolate Y coordinate to N by next frame"),
    "y": (True, "Scale image as % of height (default 100)"),
    "zg": (False, "Never used?"),
    "zh": (False, "Never used?"),
    "zj": (False, "Invulnerable to jumping attacks"),
    "zl": (False, "Never used?"),
    "zm": (False, "Never used?"),
    "zp": (False, "Invulnerable to projectiles"),
    "zz": (False, "Invulnerable to any attacks"),
}

VALID_TAG_KEYS: set[str] = set(VALID_TAGS.keys())


def describe_tag(tag: str) -> str:
    return VALID_TAGS[tag][1]


def tag_has_arg(tag: str) -> bool:
    return VALID_TAGS[tag][0]


def is_valid_tag(tag: str) -> bool:
    return tag in VALID_TAG_KEYS


def is_invalid_tag(tag: str) -> bool:
    return tag in INVALID_TAGS
