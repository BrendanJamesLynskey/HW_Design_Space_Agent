"""Precomputed exact accuracy for every numeric configuration in the registry.

Accuracy depends only on the numeric knobs (W, N, angle width, guard bits,
rounding), not on the family, and the registry has 21 x 27 x 7 x 5 x 2 =
39,690 such configurations. Each costs ~1-100 ms in the bit-accurate model
(exhaustive 2^W sweep for W <= 16, 131k-angle dense sweep above), so the
whole table takes a few minutes on four cores.

The exhaustive ground truth needs every entry; the baselines and repeated
agent runs revisit many. So the table is built once
(``python -m hw_dse.accuracy_table build``) and stored gzipped in
``eval/data/accuracy_table.csv.gz``. :func:`preload` loads it into the
golden model's cache. The numbers are identical to what
:func:`hw_dse.models.cordic_bitexact.accuracy` computes on demand (the
test suite spot-checks this), so their provenance is still ``exact``.
"""

from __future__ import annotations

import csv
import gzip
import math
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from hw_dse.families import COMMON_PARAMS
from hw_dse.models.cordic_bitexact import Accuracy, CordicNumerics, preload_accuracy, sweep_angles
from hw_dse.models.cordic_bitexact import _accuracy as compute_accuracy

DEFAULT_PATH = Path(__file__).resolve().parents[2] / "eval" / "data" / "accuracy_table.csv.gz"
FIELDS = ["data_width", "n_iter", "angle_width", "frac_guard", "rounding", "max_abs_lsb", "rms_lsb", "n_angles"]


def all_numerics() -> list[CordicNumerics]:
    p = {q.name: q for q in COMMON_PARAMS}
    out = []
    for w in p["data_width"].values():
        for n in p["n_iter"].values():
            for ag in p["angle_guard"].values():
                for g in p["frac_guard"].values():
                    for r in p["rounding"].values():
                        out.append(CordicNumerics(int(w), int(n), int(w) + int(ag), int(g), str(r)))  # type: ignore[arg-type]
    return out


def _row(cfg: CordicNumerics) -> list[object]:
    a = compute_accuracy(cfg)
    return [cfg.data_width, cfg.n_iter, cfg.A, cfg.frac_guard, cfg.rounding, repr(a.max_abs_lsb), repr(a.rms_lsb), a.n_angles]


def build(path: Path = DEFAULT_PATH, workers: int = 4) -> None:
    cfgs = all_numerics()
    # Big widths first so the pool stays balanced.
    cfgs.sort(key=lambda c: (-c.data_width, -c.n_iter))
    t0 = time.time()
    rows = []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for i, row in enumerate(ex.map(_row, cfgs, chunksize=16)):
            rows.append(row)
            if i % 2000 == 0:
                print(f"  {i}/{len(cfgs)}  {time.time() - t0:.0f}s", flush=True)
    rows.sort(key=lambda r: (r[0], r[1], r[2], r[3], r[4]))
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(FIELDS)
        w.writerows(rows)
    print(f"wrote {len(rows)} rows to {path} in {time.time() - t0:.0f}s")


def load(path: Path = DEFAULT_PATH) -> dict[CordicNumerics, Accuracy]:
    table: dict[CordicNumerics, Accuracy] = {}
    with gzip.open(path, "rt", newline="") as fh:
        for r in csv.DictReader(fh):
            w = int(r["data_width"])
            cfg = CordicNumerics(w, int(r["n_iter"]), int(r["angle_width"]), int(r["frac_guard"]), r["rounding"])  # type: ignore[arg-type]
            lsb = 2.0 ** -(w - 2)
            mx, rms = float(r["max_abs_lsb"]), float(r["rms_lsb"])
            table[cfg] = Accuracy(
                max_abs_lsb=mx,
                rms_lsb=rms,
                max_abs=mx * lsb,
                rms=rms * lsb,
                accuracy_bits=-math.log2(mx * lsb) if mx > 0 else float("inf"),
                n_angles=int(r["n_angles"]),
                sweep=sweep_angles(w)[1],
            )
    return table


def preload(path: Path = DEFAULT_PATH) -> int:
    """Load the table into the golden model's cache if it exists."""
    if not path.exists():
        return 0
    table = load(path)
    preload_accuracy(table)
    return len(table)


if __name__ == "__main__":  # pragma: no cover
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        build()
    else:
        print("usage: python -m hw_dse.accuracy_table build")
