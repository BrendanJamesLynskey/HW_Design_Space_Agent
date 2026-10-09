#!/usr/bin/env python3
"""Run the L3 verification sweep and write eval/data/l3_verification.csv.

    python scripts/run_l3_sweep.py              # full sweep, every available simulator
    python scripts/run_l3_sweep.py --quick      # the four W=8 configurations only
    python scripts/run_l3_sweep.py --sim icarus # one simulator

Generated RTL (level ``rtl``) rows are rewritten; gate-level rows (level
``gate``, from scripts/run_gate_sim.py) are kept. Exit status is non-zero if
any configuration fails (a mismatch, a missing result or a wrong latency).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hw_dse.rtl import sweep  # noqa: E402
from hw_dse.rtl.sim import SIMULATORS  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--sim", choices=SIMULATORS, action="append")
    ap.add_argument("--no-write", action="store_true", help="do not rewrite the CSV")
    args = ap.parse_args()
    cfgs = sweep.QUICK if args.quick else sweep.sweep_configs()
    rows = sweep.run(cfgs, args.sim or SIMULATORS)
    if not args.no_write:
        sweep.write_csv(rows, keep_levels=("gate",))
        print(f"wrote {sweep.L3_CSV} ({len(rows)} rtl rows)")
    failed = [r for r in rows if not r.passed]
    print(f"{len(rows)} runs, {len(failed)} failed")
    return 1 if failed or not rows else 0


if __name__ == "__main__":
    sys.exit(main())
