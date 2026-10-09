#!/usr/bin/env python3
"""Gate-level simulation of synthesised netlists; appends level=gate rows to
eval/data/l3_verification.csv (existing gate rows are replaced).

    python scripts/run_gate_sim.py                 # all GATE_CONFIGS, both simulators
    python scripts/run_gate_sim.py --sim verilator # one simulator

Needs Yosys (docker image or native, see src/hw_dse/synth/flow.py) and
Verilator and/or Icarus. Icarus is skipped for W > 8 FSM designs unless
--icarus-all is given (an exhaustive W=16 iterative gate-level run takes
tens of minutes in an event-driven simulator).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hw_dse.rtl import sweep  # noqa: E402
from hw_dse.rtl.sim import SIMULATORS, tool_status  # noqa: E402
from hw_dse.synth.flow import Runner  # noqa: E402
from hw_dse.synth.gatesim import GATE_CONFIGS, netlist_for, verify_gate  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sim", choices=SIMULATORS, action="append")
    ap.add_argument("--icarus-all", action="store_true")
    args = ap.parse_args()
    runner = Runner.from_env()
    ok, why = runner.available(pnr=False)
    if not ok:
        print(f"yosys unavailable: {why}")
        return 2
    sims = [s for s in (args.sim or SIMULATORS) if tool_status(s)[0]]
    rows = []
    for a in GATE_CONFIGS:
        net = netlist_for(a, runner)
        for s in sims:
            if s == "icarus" and a.numerics.data_width > 8 and not a.is_pipelined and not args.icarus_all:
                continue
            v = verify_gate(a, s, runner, netlist=net)
            rows.append(v)
            print(f"{s:9s} {'PASS' if v.passed else 'FAIL'} {a.key():78s} {v.mismatches}/{v.n_angles} "
                  f"lat {v.latency_measured}/{v.latency_expected} {v.seconds:.1f}s", flush=True)
    keep = [r for r in sweep.read_csv() if r["level"] != "gate"]
    import csv

    with open(sweep.L3_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=sweep.FIELDS)
        w.writeheader()
        for r in keep:
            w.writerow(r)
        for v in rows:
            w.writerow(v.row())
    print(f"appended {len(rows)} gate rows to {sweep.L3_CSV}")
    return 1 if any(not v.passed for v in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
