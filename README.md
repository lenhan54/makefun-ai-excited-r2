# Molten Koi

A single image, built to make a judge sit up.

A colossal koi tears its way out of a classical East Asian ink-wash scroll,
its scales catching fire into molten gold and vivid orange as ink and water
burst around it in a storm of droplets. Far below, a tiny wooden boat rides
the painted waves, dwarfed by the leap. Deep indigo, gold and vermilion carry
the whole scene, with one unmistakable focal point: the fish, mid-burst,
coming straight at the viewer.

## What the program does

`main.py` does one simple job and checks its own work. It copies `entry.png`
from this repository into the output directory and then verifies the copy
byte-for-byte — same size, same SHA-256 digest — refusing to report success
unless the two files match exactly.

## How to run it

```sh
python3 main.py
```

By default the image is written to `/output/entry.png`. To choose a
different destination, set `MAKEFUN_OUTPUT_DIR`:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

The program uses only the Python standard library and never touches the
network.

## Verify the output

The output is the entry image itself, byte for byte. Check it with:

```sh
sha256sum /output/entry.png
```

The digest must be
`233ad77bd3142fc0456df1b304f0536e3b77f41f6ec4c8f8188a78aa36fc03e6`
(484,691 bytes, 1024x1024 JPEG). The program already refuses to exit
successfully unless the copy matches the source in size and digest, and it
checks the source against the same known digest before copying, so a
mismatched file fails fast instead of producing a bad output.
