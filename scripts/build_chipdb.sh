#!/usr/bin/env bash
# Build the nextpnr-xilinx chip database for xc7a35tcpg236-1 from the
# prjxray-db shipped inside the openXC7 container image (about a minute).
#
#   scripts/build_chipdb.sh [output-dir]       (default: ./build/chipdb)
#   export HW_DSE_CHIPDB_DIR=<output-dir>
set -euo pipefail
OUT="$(realpath -m "${1:-build/chipdb}")"
IMAGE="${HW_DSE_OPENXC7_IMAGE:-regymm/openxc7}"
mkdir -p "$OUT"
docker run --rm -v "$OUT:/out" --entrypoint bash "$IMAGE" -c '
  set -e; cd /out
  python3 /nextpnr-xilinx/xilinx/python/bbaexport.py --device xc7a35tcpg236-1 --bba xc7a35t.bba
  bbasm -l xc7a35t.bba xc7a35t.bin
  rm -f xc7a35t.bba'
ls -la "$OUT/xc7a35t.bin"
echo "export HW_DSE_CHIPDB_DIR=$OUT"
