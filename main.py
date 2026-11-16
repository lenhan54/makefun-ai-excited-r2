#!/usr/bin/env python3
"""Copy the entry image to the output directory.

Reads entry.png from the same directory as this script and writes it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png). Before copying,
the source is checked against the known size and SHA-256 digest of the entry
image, so a wrong or damaged source fails fast with the expected and actual
values named. After the copy the destination is checked the same way: the
program exits non-zero unless the output matches the known digest exactly.

Standard library only. No network access.
"""

import hashlib
import os
import shutil
import sys

# Known digest of the entry image (entry.png in this directory).
EXPECTED_SIZE = 484691
EXPECTED_SHA256 = "233ad77bd3142fc0456df1b304f0536e3b77f41f6ec4c8f8188a78aa36fc03e6"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(source):
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    # Fail fast: check the source against the known digest before copying,
    # so a wrong or damaged source never produces a bad output.
    src_size = os.path.getsize(source)
    if src_size != EXPECTED_SIZE:
        print(
            f"error: source size mismatch: expected {EXPECTED_SIZE} bytes, "
            f"got {src_size} bytes for {source}",
            file=sys.stderr,
        )
        return 1
    src_sha = sha256_of(source)
    if src_sha != EXPECTED_SHA256:
        print(
            f"error: source SHA-256 mismatch: expected {EXPECTED_SHA256}, "
            f"got {src_sha} for {source}",
            file=sys.stderr,
        )
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, dest)

    dst_size = os.path.getsize(dest)
    if dst_size != EXPECTED_SIZE:
        print(
            f"error: output size mismatch: expected {EXPECTED_SIZE} bytes, "
            f"got {dst_size} bytes for {dest}",
            file=sys.stderr,
        )
        return 1

    if sha256_of(dest) != EXPECTED_SHA256:
        print(
            f"error: output SHA-256 mismatch: expected {EXPECTED_SHA256} "
            f"for {dest}",
            file=sys.stderr,
        )
        return 1

    print(f"wrote {dest} ({dst_size} bytes, sha256 verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
