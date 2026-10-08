#!/usr/bin/env bash
# Fetch the reference CORDIC RTL at a pinned commit into third_party/CORDIC.
#
# The bit-exact test (tests/test_bitexact_rtl.py) simulates these files with
# Icarus Verilog. They live in a separate public repo, so we clone it rather
# than copy it. Override the location with CORDIC_RTL_DIR=/path/to/CORDIC.
set -euo pipefail
REF_SHA="5bd6bf5"   # "Add Vivado synthesis results for Artix-7 (xc7a35tcpg236-1)"
DEST="$(cd "$(dirname "$0")/.." && pwd)/third_party/CORDIC"
if [ -d "$DEST/.git" ]; then
  echo "already present: $DEST"; exit 0
fi
git clone --quiet https://github.com/BrendanJamesLynskey/CORDIC.git "$DEST"
git -C "$DEST" checkout --quiet "$REF_SHA"
echo "reference RTL at $DEST ($(git -C "$DEST" rev-parse --short HEAD))"
