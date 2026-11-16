#!/usr/bin/env python3
"""Copy the entry image to the output directory.

Reads entry.png from the same directory as this script and writes it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png). The copy is
checked byte-for-byte: the program exits non-zero unless the output file
matches the source in both size and SHA-256 digest.

Standard library only. No network access.
"""

import hashlib
import os
import shutil
import sys


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

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, dest)

    src_size = os.path.getsize(source)
    dst_size = os.path.getsize(dest)
    if src_size != dst_size:
        print(f"error: size mismatch ({src_size} vs {dst_size})", file=sys.stderr)
        return 1

    if sha256_of(source) != sha256_of(dest):
        print("error: SHA-256 mismatch after copy", file=sys.stderr)
        return 1

    print(f"wrote {dest} ({dst_size} bytes, sha256 verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
