#!/usr/bin/env python3
"""Run the ASIC synthesis sweep (milestone 4) and write eval/data/asic_synthesis.csv.

    python scripts/run_asic_sweep.py --fetch-lib     # download + SHA-256-check the sky130hd TT liberty
    python scripts/run_asic_sweep.py                 # every point: Yosys + OpenSTA (timing, power)
    python scripts/run_asic_sweep.py --smoke         # one design (CI); does not write the CSV
    python scripts/run_asic_sweep.py --check 3       # re-synthesise 3 committed rows, must match exactly

Needs ``yosys`` (Ubuntu 24.04: Yosys 0.33) and OpenSTA's ``sta`` on PATH (or
HW_DSE_STA); see src/hw_dse/synth/asic.py and the README for installing them.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hw_dse.synth import asic, asic_sweep  # noqa: E402

COMPARE = ("area_um2", "gate_eq", "n_cells", "ffs", "critical_path_ns", "fmax_mhz", "power_mw")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fetch-lib", action="store_true", help="download the pinned liberty file into build/pdk/")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--check", type=int, default=0, help="re-measure N committed rows and compare")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default=str(asic.ASIC_CSV))
    args = ap.parse_args()
    if args.fetch_lib:
        print("liberty:", asic.fetch_liberty(), "sha256 ok")
        if not (args.smoke or args.check):
            return 0
    tools = asic.AsicTools.from_env()
    ok, why = tools.available()
    if not ok:
        print(f"ASIC flow unavailable: {why}")
        return 2
    versions = tools.versions()
    print("tools:", versions)
    if args.smoke:
        a = asic_sweep.ASIC_EXTRA[0]
        (_, r), = asic_sweep.run([a], tools, 1)
        good = r.area_um2 > 0 and r.ffs > 0 and (r.fmax_mhz or 0) > 0 and r.power.get("power_mw", 0) > 0
        print("smoke", "PASS" if good else "FAIL")
        return 0 if good else 1
    if args.check:
        with open(asic.ASIC_CSV, newline="") as fh:
            committed = list(csv.DictReader(fh))
        pts = asic.load_csv(asic.ASIC_CSV)[: args.check]
        res = asic_sweep.run([p.arch for p in pts], tools, args.workers)
        new = asic_sweep.to_rows(res, versions, keep_logs=False)
        bad = 0
        for old, now in zip(committed, new):
            diff = {c: (old[c], now[c]) for c in COMPARE if float(old[c]) != float(now[c])}  # type: ignore[arg-type]
            print(old["family"], old["data_width"], old["n_iter"], "identical" if not diff else f"DIFFERS {diff}")
            bad += bool(diff)
        return 1 if bad else 0
    results = asic_sweep.run(asic_sweep.points(), tools, args.workers)
    rows = asic_sweep.to_rows(results, versions)
    asic.write_csv(Path(args.out), rows)
    print(f"wrote {args.out} ({len(rows)} points)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
