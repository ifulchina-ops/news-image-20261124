"""The world on Tuesday 24 November 2026, summed up in one image.

This program writes the entry image to /output/entry.png. It uses only
the Python standard library, performs no network access, and is fully
deterministic: every run writes exactly the same bytes.

The image itself is entry.png, shipped in this repository. It is a
newspaper front page, "THE WORLD TODAY — Tuesday, 24 November 2026",
with six panels covering the day's biggest world stories:

  1. COP31 climate talks collapse in Antalya (no fossil-fuel deal)
  2. Factory fire in Banten, Indonesia (24 killed, dozens missing)
  3. Russian strikes on Ukraine's Kyiv region; cargo ship Sparta II
     burning in the Gulf of Finland
  4. Nvidia soars as Jensen Huang returns as CEO after Trump's call
  5. India-Nepal rail link opens (Saryu-Kamala Express)
  6. Max Verstappen wins the Las Vegas Grand Prix

Run it with:  python3 main.py
"""

import hashlib
import os
import struct
import sys

# Competition limits for the image (see the bounty page).
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024

# The image lives beside this script in the repository.
SOURCE_NAME = "entry.png"

# Where the grader expects the finished image.
OUTPUT_PATH = "/output/entry.png"


def repo_dir():
    """Directory holding this script (the repository root)."""
    return os.path.dirname(os.path.abspath(__file__))


def read_png_size(data):
    """Return (width, height) from a PNG's IHDR chunk, stdlib only."""
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    if data[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    source_path = os.path.join(repo_dir(), SOURCE_NAME)

    with open(source_path, "rb") as handle:
        image = handle.read()

    if len(image) > MAX_BYTES:
        print("entry.png is %d bytes, over the %d-byte limit"
              % (len(image), MAX_BYTES), file=sys.stderr)
        return 1

    width, height = read_png_size(image)
    if width > MAX_SIDE or height > MAX_SIDE:
        print("entry.png is %dx%d, over the %dx%d limit"
              % (width, height, MAX_SIDE, MAX_SIDE), file=sys.stderr)
        return 1

    digest = hashlib.sha256(image).hexdigest()

    output_path = OUTPUT_PATH
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as handle:
            handle.write(image)
    except OSError:
        # The grader provides /output; fall back to a local output
        # directory so the program still completes anywhere else.
        output_path = os.path.join(repo_dir(), "output", SOURCE_NAME)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as handle:
            handle.write(image)

    # Read the file back and confirm it is byte-for-byte identical, so
    # a truncated or partial write can never pass silently.
    with open(output_path, "rb") as handle:
        written = handle.read()
    if written != image:
        print("verification failed: output differs from entry.png",
              file=sys.stderr)
        return 1

    print("Wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (output_path, width, height, len(image), digest))
    print("Verified: output matches entry.png byte for byte.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
