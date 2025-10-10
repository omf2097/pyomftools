#!/usr/bin/env python3
import argparse
import os
import typing
import copy
import configparser
import re
from glob import glob
from pathlib import Path

from omftools.pyshadowdive.af import AFFile
from omftools.pyshadowdive.bk import BKFile
from omftools.pyshadowdive.tournament import TournamentFile
from omftools.pyshadowdive.sounds import SoundFile
from omftools.pyshadowdive.pic import PicFile
from omftools.pyshadowdive.altpals import AltPaletteFile
from omftools.pyshadowdive.utils.exceptions import OMFInvalidDataException
from omftools.pyshadowdive.palette import Palette
from omftools.pyshadowdive.language import LanguageFile


# HAR names for reference
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

# Arena names and IDs
arena_names = {
    "ARENA0.BK": "ARENA0",
    "ARENA1.BK": "ARENA1",
    "ARENA2.BK": "ARENA2",
    "ARENA3.BK": "ARENA3",
    "ARENA4.BK": "ARENA4",
    "ARENA5.BK": "ARENA5",
    "ARENA6.BK": "ARENA6",
    "ARENA7.BK": "7",
    "ARENA8.BK": "8",
    "ARENA9.BK": "9",
    "ARENA10.BK": "10",
    "INTRO.BK": "INTRO",
    "MENU.BK": "MENU",
    "MECHLAB.BK": "MECHLAB",
    "NEWGAME.BK": "NEWGAME",
}


def create_directory_structure(base_dir: str, mod_name: str):
    """Create the directory structure for the mod"""
    mod_dir = os.path.join(base_dir, f"{mod_name}")

    # Create base directories
    Path(os.path.join(mod_dir, "scenes", "common", "audio", "sounds")).mkdir(
        parents=True, exist_ok=True
    )
    Path(os.path.join(mod_dir, "fighters", "common", "audio", "sounds")).mkdir(
        parents=True, exist_ok=True
    )
    Path(os.path.join(mod_dir, "tournaments", "legacy")).mkdir(
        parents=True, exist_ok=True
    )
    Path(os.path.join(mod_dir, "audio", "sounds")).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(mod_dir, "audio", "music")).mkdir(parents=True, exist_ok=True)

    return mod_dir


def create_scene_ini(bk: BKFile, filename: str, output_path: str):
    """Create a header.ini file for a scene"""
    config = configparser.ConfigParser()

    # Add the scene header info
    config["DEFAULT"] = {
        "file_id": str(bk.file_id),
        "background_width": str(bk.background_width),
        "background_height": str(bk.background_height),
    }

    # Save the INI file
    with open(os.path.join(output_path, "header.ini"), "w") as configfile:
        config.write(configfile)


def create_animation_ini(animation, output_path: str, is_scene: bool = True):
    """Create an animdata.ini file for an animation"""
    config = configparser.ConfigParser()

    # Add animation data
    anim_data = {}

    if is_scene:
        # For scene animations
        if hasattr(animation, "chain_hit"):
            anim_data["chain_hit"] = str(animation.chain_hit)
        if hasattr(animation, "chain_no_hit"):
            anim_data["chain_no_hit"] = str(animation.chain_no_hit)
        if hasattr(animation, "repeat"):
            anim_data["repeat"] = str(animation.repeat)
        if hasattr(animation, "probability"):
            anim_data["probability"] = str(animation.probability)
        if hasattr(animation, "hazard_damage"):
            anim_data["hazard_damage"] = str(animation.hazard_damage)
        if hasattr(animation, "footer_string"):
            anim_data["footer_string"] = str(animation.footer_string)
        if hasattr(animation, "start_x"):
            anim_data["start_x"] = str(animation.start_x)
        if hasattr(animation, "start_y"):
            anim_data["start_y"] = str(animation.start_y)
        if hasattr(animation, "base_string"):
            anim_data["base_string"] = str(animation.base_string)
    else:
        # For fighter animations
        if hasattr(animation, "ai_opts"):
            anim_data["ai_opts"] = str(animation.ai_opts)
        if hasattr(animation, "pos_constraint"):
            anim_data["pos_constraint"] = str(animation.pos_constraint)
        if hasattr(animation, "next_animation_id"):
            anim_data["next_animation_id"] = str(animation.next_animation_id)
        if hasattr(animation, "category"):
            anim_data["category"] = str(animation.category)
        if hasattr(animation, "block_damage"):
            anim_data["block_damage"] = str(animation.block_damage)
        if hasattr(animation, "block_stun_and_scrap"):
            anim_data["block_stun_and_scrap"] = str(animation.block_stun_and_scrap)
        if hasattr(animation, "successor_id"):
            anim_data["successor_id"] = str(animation.successor_id)
        if hasattr(animation, "damage_amount"):
            anim_data["damage_amount"] = str(animation.damage_amount)
        if hasattr(animation, "throw_duration"):
            anim_data["throw_duration"] = str(animation.throw_duration)
        if hasattr(animation, "extra_string_selector"):
            anim_data["extra_string_selector"] = str(animation.extra_string_selector)
        if hasattr(animation, "points"):
            anim_data["points"] = str(animation.points)
        if hasattr(animation, "move_string"):
            anim_data["move_string"] = str(animation.move_string)
        if hasattr(animation, "enemy_string"):
            anim_data["enemy_string"] = str(animation.enemy_string)
        if hasattr(animation, "start_x"):
            anim_data["start_x"] = str(animation.start_x)
        if hasattr(animation, "start_y"):
            anim_data["start_y"] = str(animation.start_y)
        if hasattr(animation, "base_string"):
            anim_data["base_string"] = str(animation.base_string)

    config["DEFAULT"] = anim_data

    # Save the INI file
    with open(os.path.join(output_path, "animdata.ini"), "w") as configfile:
        config.write(configfile)


def create_fighter_ini(af: AFFile, output_path: str):
    """Create a header.ini file for a fighter"""
    config = configparser.ConfigParser()

    # Add the fighter header info
    header_data = {}
    if hasattr(af, "endurance"):
        header_data["endurance"] = str(af.endurance)
    if hasattr(af, "health"):
        header_data["health"] = str(af.health)
    if hasattr(af, "forward_speed"):
        header_data["forward_speed"] = str(af.forward_speed)
    if hasattr(af, "reverse_speed"):
        header_data["reverse_speed"] = str(af.reverse_speed)
    if hasattr(af, "jump_speed"):
        header_data["jump_speed"] = str(af.jump_speed)
    if hasattr(af, "fall_speed"):
        header_data["fall_speed"] = str(af.fall_speed)

    config["DEFAULT"] = header_data

    # Save the INI file
    with open(os.path.join(output_path, "header.ini"), "w") as configfile:
        config.write(configfile)


def create_tournament_ini(trn: TournamentFile, output_path: str):
    """Create a tournament.ini file according to mod specification"""
    # HAR names for specific endings
    har_names = [
        "jaguar",
        "shadow",
        "thorn",
        "pyros",
        "electra",
        "katana",
        "shredder",
        "flail",
        "gargoyle",
        "chronos",
        "nova",
    ]

    # Write the file in the format required by mod spec
    with open(os.path.join(output_path, "tournament.ini"), "w") as f:
        # Tournament data
        f.write(f'tournament_end = "{trn.bk_name}"\n')
        f.write(f"registration_fee = {trn.registration_fee}\n")
        f.write(f"winnings_multiplier = {trn.winnings_multiplier:.1f}\n")
        # f.write(f'offense_addition = {trn.offense_inc}\n')
        # f.write(f'defense_addition = {trn.defense_inc}\n')
        f.write("\n")

        # English section
        f.write("# add a section for each language you want to support\n")
        f.write("language english {\n")
        f.write(f'    name = "{trn.locale_titles[0]}"\n')
        f.write(
            "    # note the description is a multi-line string and can use special formatting tags\n"
        )
        f.write(f'    description = "{trn.locale_descriptions[0]}"\n\n')

        # Process English endings
        if hasattr(trn, "locale_end_texts") and len(trn.locale_end_texts) > 0:
            english_endings = trn.locale_end_texts[0]  # English endings

            # Collect all texts for each page
            page_texts = {}  # page_id -> list of texts
            har_texts = {}  # har_id -> page_id -> text

            # Structure is endings[har_id][page_id]
            # First, get all texts for each page
            for har_idx, har_endings in enumerate(english_endings):
                if not har_endings:
                    continue

                # Index 0 is typically generic text
                for page_idx, text in enumerate(har_endings):
                    if not text:
                        continue

                    # Store by page
                    if page_idx not in page_texts:
                        page_texts[page_idx] = {}

                    if text not in page_texts[page_idx]:
                        page_texts[page_idx][text] = []

                    page_texts[page_idx][text].append(har_idx)

                    # Also store by HAR for easy lookup
                    if har_idx not in har_texts:
                        har_texts[har_idx] = {}
                    har_texts[har_idx][page_idx] = text

            # Find most common text for each page (appears in 2+ HARs)
            common_texts = {}
            for page_idx, text_counts in page_texts.items():
                most_common = None
                max_count = 1  # Must appear in at least 2 HARs

                for text, har_indices in text_counts.items():
                    if len(har_indices) > max_count:
                        most_common = text
                        max_count = len(har_indices)

                if most_common:
                    common_texts[page_idx] = most_common

            # Write "ending all" section with common texts
            f.write("    ending all {\n")
            for page_idx, text in common_texts.items():
                f.write(f'        page{page_idx + 1} = "{text}"\n')
            f.write("    }\n\n")

            # Write HAR-specific overrides
            for har_idx, pages in har_texts.items():
                has_unique = False
                unique_pages = {}

                # Check if this HAR has any unique texts
                for page_idx, text in pages.items():
                    if page_idx not in common_texts or text != common_texts[page_idx]:
                        has_unique = True
                        unique_pages[page_idx] = text

                # Only create a section if this HAR has unique texts
                if has_unique:
                    f.write(f"    ending {har_names[har_idx]} {{\n")
                    for page_idx, text in unique_pages.items():
                        f.write(f'        page{page_idx + 1} = "{text}"\n')
                    f.write("    }\n\n")
        f.write("}\n\n")

        # German section
        f.write("language german {\n")
        f.write(f'    name = "{trn.locale_titles[1]}"\n')
        f.write(f'    description = "{trn.locale_descriptions[1]}"\n\n')

        # Process German endings
        if hasattr(trn, "locale_end_texts") and len(trn.locale_end_texts) > 1:
            german_endings = trn.locale_end_texts[1]  # German endings

            # Collect all texts for each page
            page_texts = {}  # page_id -> list of texts
            har_texts = {}  # har_id -> page_id -> text

            # Structure is endings[har_id][page_id]
            # First, get all texts for each page
            for har_idx, har_endings in enumerate(german_endings):
                if not har_endings:
                    continue

                # Index 0 is typically generic text
                for page_idx, text in enumerate(har_endings):
                    if not text:
                        continue

                    # Store by page
                    if page_idx not in page_texts:
                        page_texts[page_idx] = {}

                    if text not in page_texts[page_idx]:
                        page_texts[page_idx][text] = []

                    page_texts[page_idx][text].append(har_idx)

                    # Also store by HAR for easy lookup
                    if har_idx not in har_texts:
                        har_texts[har_idx] = {}
                    har_texts[har_idx][page_idx] = text

            # Find most common text for each page (appears in 2+ HARs)
            common_texts = {}
            for page_idx, text_counts in page_texts.items():
                most_common = None
                max_count = 1  # Must appear in at least 2 HARs

                for text, har_indices in text_counts.items():
                    if len(har_indices) > max_count:
                        most_common = text
                        max_count = len(har_indices)

                if most_common:
                    common_texts[page_idx] = most_common

            # Write "ending all" section with common texts
            f.write("    ending all {\n")
            for page_idx, text in common_texts.items():
                f.write(f'        page{page_idx + 1} = "{text}"\n')
            f.write("    }\n\n")

            # Write HAR-specific overrides
            for har_idx, pages in har_texts.items():
                has_unique = False
                unique_pages = {}

                # Check if this HAR has any unique texts
                for page_idx, text in pages.items():
                    if page_idx not in common_texts or text != common_texts[page_idx]:
                        has_unique = True
                        unique_pages[page_idx] = text

                # Only create a section if this HAR has unique texts
                if has_unique:
                    f.write(f"    ending {har_names[har_idx]} {{\n")
                    for page_idx, text in unique_pages.items():
                        f.write(f'        page{page_idx + 1} = "{text}"\n')
                    f.write("    }\n\n")
        f.write("}\n")


def create_pilot_ini(pilot, output_path: str, gender: str = "male"):
    """Create a pilot info.ini file"""
    config = configparser.ConfigParser()

    # Add basic pilot info
    config["DEFAULT"] = {
        "name": f'"{pilot.name}"',
        "gender": f'"{gender}"',
        "wins": str(pilot.wins),
        "losses": str(pilot.losses),
        "rank": str(pilot.rank),
        "money": str(pilot.money),
        "winnings": str(pilot.winnings),
        "total_value": str(pilot.total_value),
    }

    # Add HAR and related info
    har_names = [
        "jaguar",
        "shadow",
        "thorn",
        "pyros",
        "electra",
        "katana",
        "shredder",
        "flail",
        "gargoyle",
        "chronos",
        "nova",
    ]
    if 0 <= pilot.har_id < len(har_names):
        config["DEFAULT"]["robot"] = f'"{har_names[pilot.har_id]}"'

    # Add other sections as needed
    config["colors"] = {
        "primary": str(pilot.color_1),
        "secondary": str(pilot.color_2),
        "tertiary": str(pilot.color_3),
    }

    # Save the INI file
    with open(os.path.join(output_path, "pilot.ini"), "w") as configfile:
        config.write(configfile)


def create_manifest_ini(mod_name: str, output_path: str):
    """Create a manifest.ini file for the mod"""
    config = configparser.ConfigParser()

    config["DEFAULT"] = {
        "mod_api": "1.0",
        "version": "1.0",
        "author": "Asset Dumper",
        "email": "example@example.com",
        "name": mod_name,
        "description": f"Dumped assets for {mod_name}",
        "load_order": "0",
    }

    # Save the INI file
    with open(os.path.join(output_path, "manifest.ini"), "w") as configfile:
        config.write(configfile)


def process_scenes(bk_files: list, mod_dir: str, alt_pals: AltPaletteFile):
    """Process BK files (scenes) and save them to the mod structure"""
    for bk_file in bk_files:
        filename = os.path.basename(bk_file)
        print(f"Processing scene: {filename}")

        bk = BKFile.load_native(bk_file)
        arena_id = arena_names.get(
            filename.upper(), os.path.splitext(filename)[0].upper()
        )

        # Create arena directory
        arena_dir = os.path.join(mod_dir, "scenes", arena_id)
        Path(arena_dir).mkdir(parents=True, exist_ok=True)

        # Create palettes directory and save palettes
        palettes_dir = os.path.join(arena_dir, "palettes")
        Path(palettes_dir).mkdir(parents=True, exist_ok=True)

        # Save background
        bk.save_background(os.path.join(arena_dir, "background.png"))

        # Create header.ini
        create_scene_ini(bk, filename, arena_dir)

        # Process animations
        for key, animation in bk.animations.items():
            anim_dir = os.path.join(arena_dir, str(key))

            Path(anim_dir).mkdir(parents=True, exist_ok=True)

            # Create animation data INI
            create_animation_ini(animation, anim_dir)

            # Save sprites
            for idx, sprite in enumerate(animation.sprites):
                sprite_file = os.path.join(anim_dir, f"{idx}.png")
                try:
                    # Get the appropriate palette
                    processed_palette = bk.get_processed_palette(bk_file)
                    sprite.save_png(sprite_file, processed_palette)
                except OMFInvalidDataException:
                    print(f"Skipping {sprite_file}")
                except Exception as e:
                    print(f"Error saving sprite {sprite_file}: {e}")


def process_fighters(af_files: list, mod_dir: str):
    """Process AF files (fighters) and save them to the mod structure"""
    for af_file in af_files:
        filename = os.path.basename(af_file)
        print(f"Processing fighter: {filename}")

        af = AFFile.load_native(af_file)
        fighter_match = re.match(r"(FIGHTR\d+)\.AF", filename, re.IGNORECASE)
        fighter_id = (
            fighter_match.group(1).upper()
            if fighter_match
            else f"FIGHTR{os.path.splitext(filename)[0].upper()}"
        )

        # Create fighter directory
        fighter_dir = os.path.join(mod_dir, "fighters", fighter_id)
        Path(fighter_dir).mkdir(parents=True, exist_ok=True)

        # Create header.ini
        create_fighter_ini(af, fighter_dir)

        # Use default palette for AF sprites
        default_palette = Palette()

        # Process animations
        for key, animation in af.moves.items():
            anim_dir = os.path.join(fighter_dir, str(key))

            Path(anim_dir).mkdir(parents=True, exist_ok=True)

            # Create animation data INI
            create_animation_ini(animation, anim_dir, is_scene=False)

            # Save sprites
            for idx, sprite in enumerate(animation.sprites):
                sprite_file = os.path.join(anim_dir, f"{idx}.png")
                try:
                    sprite.save_png(
                        sprite_file, default_palette, asset_type="af_sprite"
                    )
                except OMFInvalidDataException:
                    print(f"Skipping {sprite_file}")
                except Exception as e:
                    print(f"Error saving sprite {sprite_file}: {e}")


def process_tournaments(trn_files: list, mod_dir: str):
    """Process TRN files (tournaments) and save them to the mod structure"""
    for trn_file in trn_files:
        filename = os.path.basename(trn_file)
        print(f"Processing tournament: {filename}")

        trn = TournamentFile.load_native(trn_file)
        tournament_name = os.path.splitext(filename)[0].upper()

        # Create tournament directories
        legacy_dir = os.path.join(mod_dir, "tournaments", "legacy")
        tournament_dir = os.path.join(mod_dir, "tournaments", tournament_name)
        logos_dir = os.path.join(tournament_dir, "logos")
        pilots_dir = os.path.join(tournament_dir, "pilots")

        Path(logos_dir).mkdir(parents=True, exist_ok=True)
        Path(pilots_dir).mkdir(parents=True, exist_ok=True)

        # Create tournament.ini
        create_tournament_ini(trn, tournament_dir)

        # Save logos
        for idx, sprite in enumerate(trn.locale_logos):
            # If idx is 0, it's the default logo (no ISO code)
            if idx == 0:
                sprite_file = os.path.join(logos_dir, "logo.png")
            else:
                # We would need ISO codes if available, using index for now
                sprite_file = os.path.join(logos_dir, f"en_{idx}.png")

            try:
                sprite.save_png(sprite_file, trn.palette)
            except OMFInvalidDataException:
                print(f"Skipping {sprite_file}")
            except Exception as e:
                print(f"Error saving logo {sprite_file}: {e}")

        # Process pilots
        for idx, pilot in enumerate(trn.pilots):
            if not pilot.name:  # Skip empty pilots
                continue

            # Create pilot directory
            pilot_dir = os.path.join(pilots_dir, f"{idx}")
            Path(pilot_dir).mkdir(parents=True, exist_ok=True)

            # Default gender (will be updated if photo is found)
            gender = "male"

            # Save portrait if available
            # Extract the portrait from the tournament's PIC file
            # Find PIC file case-insensitively (for DOS files on case-sensitive filesystems)
            pic_filename = trn.pic_filename
            trn_dir = os.path.dirname(trn_file)
            found = False
            for file in os.listdir(trn_dir):
                if file.lower() == pic_filename.lower():
                    pic_path = os.path.join(trn_dir, file)
                    found = True
                    break

            # Try to extract photo and gender
            # Use photo_id from pilot if available, otherwise use pilot index
            photo_id = (
                pilot.photo_id
                if hasattr(pilot, "photo_id") and pilot.photo_id is not None
                else pilot_idx
            )
            if found:
                pic = PicFile.load_native(pic_path)
                if photo_id < len(pic.photos):
                    # Create a custom palette for this photo
                    photo = pic.photos[photo_id]

                    # Extract gender from the photo
                    gender = "female" if photo.sex.value == 1 else "male"

                    custom_palette = Palette()

                    # Use the photo's own palette for indices 0x00-0x2F
                    for i in range(0x00, 0x30):
                        custom_palette.data[i] = photo.palette.data[i]

                    # Mask indices 0x60-0x9F with magenta
                    custom_palette.mask_range(0x60, 64)

                    # Ensure portrait directory exists
                    Path(pilot_dir).mkdir(parents=True, exist_ok=True)

                    # Save the portrait
                    portrait_file = os.path.join(pilot_dir, "pilot.png")
                    try:
                        photo.sprite.save_png(portrait_file, custom_palette)
                    except Exception as e:
                        print(f"Error saving portrait for {pilot_name}: {e}")
                        portrait_file = None
                else:
                    print(f"No portrait found for pilot {pilot_name} in {pic_path}")
                    portrait_file = None
            else:
                print(f"PIC file not found: {pic_filename} in {trn_dir}")
                portrait_file = None


def process_sounds(sounds_file: str, mod_dir: str):
    """Process SOUNDS.DAT and save to the toplevel audio folder"""
    if not os.path.exists(sounds_file):
        print(f"Sounds file not found: {sounds_file}")
        return

    print(f"Processing sounds: {sounds_file}")

    sounds = SoundFile.load_native(sounds_file)

    # Save sounds to audio/sounds directory
    sounds_dir = os.path.join(mod_dir, "audio", "sounds")

    for idx, sound in enumerate(sounds.sounds):
        if sound.data:
            sound_file = os.path.join(sounds_dir, f"{idx}.wav")
            sound.save_wav(sound_file)


def process_pics(pic_files: list, mod_dir: str, alt_pals: AltPaletteFile):
    """Process PIC files - empty function as we no longer dump PIC files independently"""
    # PIC files are now processed directly in process_tournaments
    pass


def main():
    parser = argparse.ArgumentParser(
        description="Dump game assets according to the mod structure"
    )
    parser.add_argument("input_dir", help="Input directory containing OMF game files")
    parser.add_argument("output_dir", help="Output directory for the mod")
    parser.add_argument(
        "--mod-name",
        dest="mod_name",
        default="omf_assets_dump",
        help="Name for the mod (default: omf_assets_dump)",
    )
    args = parser.parse_args()

    # Find all relevant files
    af_files = glob(os.path.join(args.input_dir, "*.AF"))
    bk_files = glob(os.path.join(args.input_dir, "*.BK"))
    trn_files = glob(os.path.join(args.input_dir, "*.TRN"))
    pic_files = glob(os.path.join(args.input_dir, "*.PIC"))
    alt_pals_file = os.path.join(args.input_dir, "ALTPALS.DAT")
    sounds_file = os.path.join(args.input_dir, "SOUNDS.DAT")

    # Load ALTPALS.DAT for palette references
    alt_pals = AltPaletteFile.load_native(alt_pals_file)

    # Create mod directory structure
    mod_dir = create_directory_structure(args.output_dir, args.mod_name)

    # Create manifest.ini
    create_manifest_ini(args.mod_name, mod_dir)

    # Process different types of assets
    process_scenes(bk_files, mod_dir, alt_pals)
    process_fighters(af_files, mod_dir)
    process_tournaments(trn_files, mod_dir)
    process_sounds(sounds_file, mod_dir)
    # PIC files are now processed directly in process_tournaments

    print(f"\nAsset dumping complete. Mod created at: {mod_dir}")
    print("\nNOTE: Some manual organization may be needed, particularly for:")
    print(
        "1. Creating appropriate 'animdata.ini' files if special configuration is needed"
    )

    return 0


if __name__ == "__main__":
    main()
