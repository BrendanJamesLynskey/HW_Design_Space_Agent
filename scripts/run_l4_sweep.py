#!/usr/bin/env python3
"""Run the L4 synthesis sweep and write eval/data/l4_synthesis.csv.

    export HW_DSE_CHIPDB_DIR=/path/with/xc7a35t.bin   # scripts/build_chipdb.sh
    python scripts/run_l4_sweep.py                    # every point, 3 nextpnr seeds each
    python scripts/run_l4_sweep.py --yosys-only       # fallback: resource counts, no Fmax
    python scripts/run_l4_sweep.py --smoke            # one design (CI)

Tools run in the regymm/openxc7 docker image unless HW_DSE_SYNTH_RUNNER=native
(yosys and nextpnr-xilinx on PATH). See src/hw_dse/synth/flow.py.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hw_dse.synth import measured, sweep  # noqa: E402
from hw_dse.synth.flow import SYNTH_BUILD, Runner  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--yosys-only", action="store_true")
    ap.add_argument("--smoke", action="store_true", help="synthesise one small design; do not write the CSV")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default=str(sweep.L4_CSV))
    args = ap.parse_args()
    runner = Runner.from_env()
    pnr = not args.yosys_only
    ok, why = runner.available(pnr=pnr)
    if not ok:
        print(f"synthesis flow unavailable: {why}")
        return 2
    versions = runner.versions(SYNTH_BUILD.parent if SYNTH_BUILD.parent.exists() else Path("."))
    print("tools:", versions)
    if args.smoke:
        res = sweep.run(sweep.jobs([sweep.SPREAD[0]], include_reference=False), runner, pnr, 1)
        r = res[0][1][0]
        ok = r.luts > 0 and r.ffs > 0 and (r.fmax_mhz or 0) > 0 if pnr else r.luts > 0
        print("smoke", "PASS" if ok else "FAIL")
        return 0 if ok else 1
    results = sweep.run(sweep.jobs(), runner, pnr, args.workers)
    pts = sweep.to_points(results, versions, pnr)
    measured.write(args.out, pts)
    print(f"wrote {args.out} ({len(pts)} points)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
