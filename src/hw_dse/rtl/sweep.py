"""The L3 verification sweep: which configurations, and the committed table.

The generator can emit any of the registry's 635,040 designs; simulating all
of them is pointless, so the sweep picks a spread that exercises every code
path of the generator at least once and every knob at several values:

* every family at W in {8, 12, 16, 24} (exhaustive angle sweep for W <= 16,
  the documented dense sweep for W = 24);
* two variants per (family, W): a "plain" one (truncation, A = W, no guard
  bits, k = m = 2) and a "loaded" one (round half up, a wider or narrower
  angle path, fractional guard bits, k = m = 4), so both rounding modes and
  both carry-in forms are covered;
* N both a multiple and not a multiple of k / m (the final-cycle bypass in
  ``unrolled_k`` and the short last stage in ``pipelined_m``), N < k, N = 4
  (fewest rotations) and N = 30 (most, more shifts than register bits);
* the reference configuration (W=16, N=14) for every family;
* the three ground-truth winners of the eval's feasible specs.

``python scripts/run_l3_sweep.py`` runs it with every available simulator
and writes ``eval/data/l3_verification.csv``; gate-level rows (level
``gate``) are appended by ``scripts/run_gate_sim.py``. The fast pytest suite
runs only :data:`QUICK` (W=8); CI runs the full list.
"""

from __future__ import annotations

import csv
from collections.abc import Iterable
from pathlib import Path

from hw_dse.families import ArchConfig
from hw_dse.rtl.generator import REPO_ROOT
from hw_dse.rtl.sim import SIMULATORS, Verification, tool_status, verify_rtl

L3_CSV = REPO_ROOT / "eval" / "data" / "l3_verification.csv"
FAMILIES = ("iterative", "unrolled_k", "pipelined", "pipelined_m")


def _arch(family: str, w: int, n: int, ag: int = 0, g: int = 0, rnd: str = "trunc", km: int = 2) -> ArchConfig:
    return ArchConfig.from_params(family, {"data_width": w, "n_iter": n, "angle_guard": ag, "frac_guard": g,
                                           "rounding": rnd, "k": km, "m": km})


GT_WINNERS = [
    _arch("pipelined", 18, 15, 1, 0, "round"),           # dds_250msps
    _arch("iterative", 15, 12, 1, 0, "round"),           # low_area_control
    _arch("pipelined_m", 26, 22, 0, 0, "round", 6),      # high_precision
]
"""The exhaustive ground truth's winner for each feasible spec."""


def sweep_configs() -> list[ArchConfig]:
    """The full L3 sweep (deterministic order, duplicates removed)."""
    out: list[ArchConfig] = []
    for fam in FAMILIES:
        for w in (8, 12, 16, 24):
            out.append(_arch(fam, w, w - 2, 0, 0, "trunc", 2))           # plain; N even
            out.append(_arch(fam, w, w + 1, 2 if w > 8 else -1, 2, "round", 4))  # loaded; N odd
        out.append(_arch(fam, 16, 14))                                    # reference numerics
        out.append(_arch(fam, 12, 5, 1, 1, "round", 8))                   # N < k, m
        out.append(_arch(fam, 10, 30, -2, 4, "trunc", 3))                 # N = 30 > register width
        out.append(_arch(fam, 8, 4, 0, 3, "round", 3))                    # fewest rotations
    out += GT_WINNERS
    seen: set[str] = set()
    uniq = []
    for a in out:
        if a.key() not in seen:
            seen.add(a.key())
            uniq.append(a)
    return uniq


QUICK: list[ArchConfig] = [
    _arch("iterative", 8, 6),
    _arch("unrolled_k", 8, 9, -1, 2, "round", 4),
    _arch("pipelined", 8, 9, 2, 1, "round"),
    _arch("pipelined_m", 8, 7, 0, 0, "trunc", 3),
]
"""Four W=8 configurations (exhaustive, 256 angles) for the default test run."""


def run(configs: Iterable[ArchConfig], simulators: Iterable[str] = SIMULATORS, log: bool = True) -> list[Verification]:
    rows = []
    for sim in simulators:
        ok, why = tool_status(sim)
        if not ok:
            if log:
                print(f"skipping {sim}: {why}")
            continue
        for a in configs:
            v = verify_rtl(a, sim)
            rows.append(v)
            if log:
                print(f"{sim:9s} {'PASS' if v.passed else 'FAIL'} {a.key():80s} {v.mismatches:6d}/{v.n_angles} "
                      f"lat {v.latency_measured}/{v.latency_expected} {v.seconds:6.1f}s", flush=True)
    return rows


FIELDS = list(Verification.__dataclass_fields__) + ["passed"]


def read_csv(path: Path = L3_CSV) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_csv(rows: list[Verification], path: Path = L3_CSV, keep_levels: tuple[str, ...] = ()) -> None:
    """Write ``rows``; keep existing rows whose level is in ``keep_levels``."""
    kept = [r for r in read_csv(path) if r["level"] in keep_levels]
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for r in kept:
            w.writerow(r)
        for v in rows:
            w.writerow(v.row())
