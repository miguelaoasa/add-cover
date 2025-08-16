#!/usr/bin/env python3

from mimetypes import guess_type
from mutagen.id3 import APIC, ID3

import argparse
import os
import sys

def add_cover(cover, file):
    audio = ID3(file)

    audio.add(
            APIC(mime=mime, type=3,
                 data=open(cover, "rb").read()
                ))

    audio.save()


def check_file(file):
    if not os.path.isfile(file):
        print(f"[!] {file} not such file.")
        sys.exit(1)

    if not os.access(file, os.R_OK):
        print(f"[!] {file} access denied.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Add a cover image to MP3 files")
    parser.add_argument("cover", help="Path to the cover image")
    parser.add_argument("files", nargs='+', help="List of MP3 files to which the cover will be added")

    args = parser.parse_args()

    cover = args.cover
    check_file(cover)

    mime = guess_type(cover)[0]
    if mime not in ["image/jpeg", "image/png"]:
        print(f"[!!] Invalid cover MIME type.")
        sys.exit(1)

    for file in args.files:
        check_file(file)
        if guess_type(file)[0] != "audio/mpeg":
            print(f"[!!] {file} invalid MIME type.")
            continue

        add_cover(cover, file)


if __name__ == "__main__":
    main()
