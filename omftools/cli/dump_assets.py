#!/usr/bin/env python3
import argparse
import os
import typing
import copy

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


# HAR names for reference - used for pilot.ini and tournament.ini
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


def create_directory_structure(base_dir: str):
    """Create the directory structure for the mod"""

    # Create base directories
    Path(os.path.join(base_dir, "scenes")).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(base_dir, "fighters")).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(base_dir, "tournaments")).mkdir(parents=True, exist_ok=True)
    Path(os.path.join(base_dir, "audio", "sounds")).mkdir(parents=True, exist_ok=True)

    return base_dir


def create_scene_ini(bk: BKFile, filename: str, output_path: str):
    """Create a header.ini file for a scene"""
    # Write the file directly in the format required by mod spec
    with open(os.path.join(output_path, "header.ini"), "w") as f:
        f.write(f"file_id = {bk.file_id}\n")
        f.write(f"background_width = {bk.background_width}\n")
        f.write(f"background_height = {bk.background_height}\n")


def create_animation_ini(animation, output_path: str, is_scene: bool = True):
    """Create an animdata.ini file for an animation"""
    # Write the file directly in the format required by mod spec
    with open(os.path.join(output_path, "animdata.ini"), "w") as f:
        if is_scene:
            # For scene animations
            f.write(f"chain_hit = {animation.chain_hit}\n")
            f.write(f"chain_no_hit = {animation.chain_no_hit}\n")
            f.write(f"repeat = {animation.repeat}\n")
            f.write(f"probability = {animation.probability}\n")
            f.write(f"hazard_damage = {animation.hazard_damage}\n")
            f.write(f'footer_string = "{animation.footer_string}"\n')
            f.write(f"start_x = {animation.start_x}\n")
            f.write(f"start_y = {animation.start_y}\n")
            f.write(f'base_string = "{animation.base_string}"\n')

        else:
            # For fighter animations
            f.write(f"ai_opts = {animation.ai_opts}\n")
            f.write(f"pos_constraint = {animation.pos_constraint}\n")
            f.write(f"next_animation_id = {animation.next_animation_id}\n")
            f.write(f"category = {animation.category}\n")
            f.write(f"block_damage = {animation.block_damage}\n")
            f.write(f"block_stun_and_scrap = {animation.block_stun_and_scrap}\n")
            f.write(f"successor_id = {animation.successor_id}\n")
            f.write(f"damage_amount = {animation.damage_amount}\n")
            f.write(f"throw_duration = {animation.throw_duration}\n")
            f.write(f"extra_string_selector = {animation.extra_string_selector}\n")
            f.write(f"points = {animation.points}\n")
            f.write(f'move_string = "{animation.move_string}"\n')
            f.write(f'enemy_string = "{animation.enemy_string}"\n')
            f.write(f"start_x = {animation.start_x}\n")
            f.write(f"start_y = {animation.start_y}\n")
            f.write(f'base_string = "{animation.base_string}"\n')


def create_fighter_ini(af: AFFile, output_path: str):
    """Create a header.ini file for a fighter according to mod specification"""
    with open(os.path.join(output_path, "header.ini"), "w") as f:
        f.write(f"endurance = {af.endurance}\n")
        f.write(f"health = {af.health}\n")
        f.write(f"forward_speed = {af.forward_speed}\n")
        f.write(f"reverse_speed = {af.reverse_speed}\n")
        f.write(f"jump_speed = {af.jump_speed}\n")
        f.write(f"fall_speed = {af.fall_speed}\n")


def create_tournament_ini(trn: TournamentFile, output_path: str):
    """Create a tournament.ini file according to mod specification"""

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

        # Process endings for both languages
        def process_locale(language_idx, language_name):
            """Process tournament locales for the given language index"""
            f.write(f"language {language_name} {{\n")
            f.write(f'    name = "{trn.locale_titles[language_idx]}"\n')
            f.write(f'    description = "{trn.locale_descriptions[language_idx]}"\n\n')

            if len(trn.locale_end_texts) > language_idx:
                endings = trn.locale_end_texts[
                    language_idx
                ]  # Get endings for this language

                # Collect all texts for each page
                page_texts = {}  # page_id -> list of texts
                har_texts = {}  # har_id -> page_id -> text

                # Structure is endings[har_id][page_id]
                # First, get all texts for each page
                for har_idx, har_endings in enumerate(endings):
                    if not har_endings:
                        continue

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
                        if (
                            page_idx not in common_texts
                            or text != common_texts[page_idx]
                        ):
                            has_unique = True
                            unique_pages[page_idx] = text

                    # Only create a section if this HAR has unique texts
                    if has_unique:
                        f.write(f"    ending {har_names[har_idx]} {{\n")
                        for page_idx, text in unique_pages.items():
                            f.write(f'        page{page_idx + 1} = "{text}"\n')
                        f.write("    }\n\n")
            f.write("}\n")

        # Process English locale strings
        process_locale(0, "english")
        f.write("\n")

        # Process German locale strings
        process_locale(1, "german")


def create_pilot_ini(pilot, output_path: str, gender: str = "male"):
    """Create a pilot info.ini file according to mod specification"""
    # Write the file directly in the format required by mod spec
    with open(os.path.join(output_path, "pilot.ini"), "w") as f:
        # Basic info
        f.write(f'name = "{pilot.name}"\n\n')
        f.write(f'gender = "{gender}"\n\n')

        # Language sections
        f.write("language english {\n")
        f.write(f'  quote = "{pilot.quotes[0]}"\n')
        f.write("}\n\n")

        f.write("language german {\n")
        f.write(f'  quote = "{pilot.quotes[1]}"\n')
        f.write("}\n\n")

        # HAR and record
        if 0 <= pilot.har_id < len(har_names):
            f.write(f'robot = "{har_names[pilot.har_id]}"\n')
        f.write(f'wins = "{pilot.wins}"\n')
        f.write(f'losses = "{pilot.losses}"\n\n')

        # HAR upgrades
        f.write("# HAR upgrades\n")
        f.write(f"arm_speed = {pilot.arm_speed}\n")
        f.write(f"arm_power = {pilot.arm_power}\n\n")

        f.write(f"leg_speed = {pilot.leg_speed}\n")
        f.write(f"leg_power = {pilot.leg_power}\n\n")

        f.write(f"armor = {pilot.armor}\n")
        f.write(f"stun_resistance = {pilot.stun_resistance}\n\n")

        # Pilot stats
        f.write("# pilot stats\n")
        f.write(f"speed = {pilot.agility}\n")
        f.write(f"power = {pilot.power}\n")
        f.write(f"endurance = {pilot.endurance}\n\n")

        # Offense and defense
        f.write("# General AI preferences for offense and defense. Max is 200.\n")
        f.write(f"offense = {pilot.offense}\n")
        f.write(f"defense = {pilot.defense}\n\n")

        # Attitude section
        f.write("attitude {\n")
        f.write(f"  normal = {pilot.att_normal}\n")
        f.write(f"  hyper = {pilot.att_hyper}\n")
        f.write(f"  jump = {pilot.att_jump}\n")
        f.write(f"  defense = {pilot.att_def}\n")
        f.write(f"  sniper = {pilot.att_sniper}\n")
        f.write("}\n\n")

        # Attacks section
        f.write("attacks {\n")
        f.write(f"  throw = {pilot.ap_throw}\n")
        f.write(f"  special = {pilot.ap_special}\n")
        f.write(f"  jump = {pilot.ap_jump}\n")
        f.write(f"  low = {pilot.ap_low}\n")
        f.write(f"  middle = {pilot.ap_middle}\n")
        f.write(f"  high = {pilot.ap_high}\n")
        f.write("}\n\n")

        # Preferences section
        f.write("preferences {\n")
        f.write(f"  jump = {pilot.pref_jump}\n")
        f.write(f"  forward = {pilot.pref_fwd}\n")
        f.write(f"  back = {pilot.pref_back}\n")
        f.write("}\n\n")

        # Learning and money
        f.write(f"learning = {pilot.learning:.1f}\n")
        f.write(f"forget = {pilot.forget:.1f}\n")
        f.write(f"money = {pilot.money}\n\n")

        # Colors section
        f.write(
            "# colors 0-15 are the predefined HAR colors, 16 and above use the colors from the first 48 colors in the pilot photo\n"
        )
        f.write("colors {\n")
        f.write(f"  primary = {pilot.color_1}\n")
        f.write(f"  secondary = {pilot.color_2}\n")
        f.write(f"  tertiary = {pilot.color_3}\n")
        f.write("}\n\n")

        # Movement and winnings
        if pilot.movement == 0:
            f.write(
                "# movement false setting will not allow player to move up and down in rank.\n"
            )
            f.write("movement = false\n")
        f.write(f"winnings = {pilot.winnings}\n")

        # Add requirements section for secret pilots
        if pilot.secret:
            f.write("\nsecret = true\n")
            f.write("\n# Requirements for unlocking this secret character\n")
            f.write("requirements {\n")
            if pilot.req_enemy:
                f.write(f"  enemy = {pilot.req_enemy}\n")
            if pilot.req_difficulty:
                f.write(f"  difficulty = {pilot.req_difficulty}\n")
            if pilot.req_rank:
                f.write(f"  rank = {pilot.req_rank}\n")
            if pilot.req_max_rank:
                f.write(f"  max_rank = {pilot.req_max_rank}\n")
            if pilot.req_vitality:
                f.write(f"  vitality = {pilot.req_vitality}\n")
            if pilot.req_fighter:
                f.write(f"  fighter = {pilot.req_fighter}\n")
            if pilot.req_accuracy:
                f.write(f"  accuracy = {pilot.req_accuracy}\n")
            if pilot.req_avg_dmg:
                f.write(f"  avg_dmg = {pilot.req_avg_dmg}\n")
            if pilot.req_scrap:
                f.write(f"  scrap = {pilot.req_scrap}\n")
            if pilot.req_destroy:
                f.write(f"  destroy = {pilot.req_destroy}\n")
            f.write("}\n")


def process_scenes(bk_files: list, mod_dir: str, alt_pals: AltPaletteFile):
    """Process BK files (scenes) and save them to the mod structure"""
    for bk_file in bk_files:
        filename = os.path.basename(bk_file)
        print(f"Processing scene: {filename}")

        bk = BKFile.load_native(bk_file)
        arena_id = os.path.splitext(filename)[0].upper()

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
                    processed_palette = bk.get_processed_palette(
                        os.path.basename(bk_file)
                    )
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
        # mask off the scene colors
        default_palette.mask_range(0x60, 64)

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
            photo_id = pilot.photo_id
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
                        print(f"Error saving portrait for {pilot.name}: {e}")
                        portrait_file = None
                else:
                    print(f"No portrait found for pilot {pilot.name} in {pic_path}")
                    portrait_file = None
            else:
                print(f"PIC file not found: {pic_filename} in {trn_dir}")
                portrait_file = None

            # Create pilot.ini with all the extracted information
            create_pilot_ini(pilot, pilot_dir, gender)


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


def main():
    parser = argparse.ArgumentParser(
        description="Dump game assets according to the mod structure"
    )
    parser.add_argument("input_dir", help="Input directory containing OMF game files")
    parser.add_argument("output_dir", help="Output directory for the mod")
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
    mod_dir = create_directory_structure(args.output_dir)

    # Process different types of assets
    process_scenes(bk_files, mod_dir, alt_pals)
    process_fighters(af_files, mod_dir)
    process_tournaments(trn_files, mod_dir)
    process_sounds(sounds_file, mod_dir)

    return 0


if __name__ == "__main__":
    main()
