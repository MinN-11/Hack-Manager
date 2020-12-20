#!/usr/bin/env python3
# GBA FE Hack Manager by MinN
#
# To use: run this once to create a rom folder for your hack roms and a patch folder for your patches
# Put FE6_clean.gba FE7_clean.gba FE8_clean.gba in the parent folder as patching targets
# This tool will not verify your FE roms' checksum so do it yourself
# Put your patches in the patch folder and
# run this script to patch and/or update your hack roms

import sys
import ups
import os
import os.path
import shutil
import re
import platform
from distutils.version import LooseVersion

INHERIT_SAVE = True


# solves various issues
# on macOS, click on a #! script, your cwd is still ~
# and .app bundles doesn't give you a good sys.argv[0]
def cd_current():
    dirname = os.path.dirname(sys.argv[0])  # standard thing to do
    if platform.system() == "Darwin":
        if ".app" in dirname:
            dirname = re.sub(r"\.app.*$", ".app", dirname)
            dirname = os.path.dirname(dirname)
    os.chdir(dirname)


# This only accepts version number separated by . or - and does not support dates
def try_inherit_save(saves, gba_file):
    if not INHERIT_SAVE:
        return
    possible_saves = []
    for i in saves:
        save_name = i[:-4]
        f = re.sub(r"[0-9.\-]+$", "", save_name).replace(" ", "")
        g = re.sub(r"[0-9.\-]+$", "", gba_file).replace(" ", "")
        if len(f) == 0 or len(g) == 0:
            continue
        if g.upper() in f.upper() or f.upper() in g.upper() and 0.5 <= len(f)/len(g) <= 2:
            possible_saves.append(i)
    if len(possible_saves) > 0:
        file = max(possible_saves, key=LooseVersion)
        shutil.copy(os.path.join("rom", file), os.path.join("rom", gba_file + ".sav"))
        print("New ROM {} inherited save file from {}.".format(gba_file, file))


def main():
    bad_ups_count = 0
    patched_ups_count = 0
    skipped_ups_count = 0
    if not os.path.isdir("patch"):
        os.mkdir("patch")
    if not os.path.isdir("rom"):
        os.mkdir("rom")

    fe6_checksum = ups.checksum("FE6_clean.gba") if os.path.isfile("FE6_clean.gba") else -1
    fe7_checksum = ups.checksum("FE7_clean.gba") if os.path.isfile("FE7_clean.gba") else -1
    fe8_checksum = ups.checksum("FE8_clean.gba") if os.path.isfile("FE8_clean.gba") else -1
    patches = [f for f in os.listdir("patch") if os.path.isfile(os.path.join("patch", f)) and f.endswith(".ups")]
    roms = [f for f in os.listdir("rom") if os.path.isfile(os.path.join("rom", f)) and f.endswith(".gba")]
    saves = [f for f in os.listdir("rom") if os.path.isfile(os.path.join("rom", f)) and f.endswith(".sav")]

    for i in patches:
        try:
            src_checksum, target_checksum, _ = ups.get_checksum(os.path.join("patch", i))
            if i[:-3] + "gba" in roms:
                if ups.checksum(os.path.join("rom", i[:-3] + "gba")) == target_checksum:
                    print("{} exists, skipped".format(i[:-3] + "gba"))
                    skipped_ups_count += 1
                    continue
                else:
                    print("{} is ready for update".format(i[:-3] + "gba"))
            if src_checksum == fe6_checksum:
                base_rom = "FE6_clean.gba"
            elif src_checksum == fe7_checksum:
                base_rom = "FE7_clean.gba"
            elif src_checksum == fe8_checksum:
                base_rom = "FE8_clean.gba"
            else:
                bad_ups_count += 1
                print("Cannot find a ROM for patch {}".format(i))
                continue
            try:
                ups.patch_ups(base_rom, os.path.join("patch", i), os.path.join("rom", i[:-3] + "gba"))
                patched_ups_count += 1
            except ups.ChecksumError:
                bad_ups_count += 1
                print("In patching {} patch {}, one or more checksums didn't match".format(base_rom[:3], i))
                continue
            except Exception:
                bad_ups_count += 1
                print("Error occured in patching {} patch {}".format(base_rom[:3], i))
                continue
            print("Patched ROM {}".format(i[:-4]))
            if i[:-3] + "sav" not in roms:
                try_inherit_save(saves, i[:-4])
        except Exception:
            bad_ups_count += 1
            print("Error occured in patching {}".format(i))
    print("{} ups files successfully patched".format(patched_ups_count))
    print("{} ups files failed to be patched".format(bad_ups_count))
    print("{} ups files skipped".format(skipped_ups_count))


if __name__ == '__main__':
    cd_current()
    main()
