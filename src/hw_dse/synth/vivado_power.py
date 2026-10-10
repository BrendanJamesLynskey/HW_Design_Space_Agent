"""Measured FPGA power from Vivado ``report_power`` (milestone 4; run locally).

Milestones 1-3 never measured power: the FPGA ``power_index`` is
(LUTs + FFs) x operating clock x a fixed activity, normalised to the reference
iterative design at 100 MHz, a ranking aid with no unit. This module is the
path to check it: ``scripts/vivado_m4.py export-power`` adds ``report_power``
to the Vivado flow of the 14 designs Vivado has already measured,
``collect-power`` parses the reports into ``eval/data/vivado_power.csv``
(:data:`COLUMNS`), and :func:`compare` sets the power index next to the
measured dynamic power.

What is measured, and what is not
---------------------------------
``report_power`` here is **vectorless**: Vivado propagates a default toggle
rate (12.5% of the clock, the same 0.125 the power index assumes) from the
inputs. It is a tool estimate from toggle rates and the device's power models,
not a measurement on a board. Two things keep the comparison like for like:

* **core power only**: the generated modules' ports land on I/O buffers in an
  out-of-context-free synthesis, so the report's I/O power (and the device
  static power, constant for the part) are excluded; the compared figure is
  ``Clocks + Slice Logic + Signals`` (plus any other on-chip core rows);
* **resolution**: the report prints watts to 3 decimals (1 mW), coarse for
  designs that draw a few mW at 100 MHz. The flow therefore reports power a
  second time with the clock redefined to 1 ns (1 GHz) for the power report
  only; dynamic power is linear in frequency, so the 1 GHz figure / 10 is the
  100 MHz power with 10x the resolution. Both rows are kept (``clock_ns``).

:func:`compare` reports, per design, the power index at 100 MHz (the index's
own reference clock) and the measured core power at 100 MHz, both relative to
the reference ``iterative`` W=16 N=14, their ratio, the RMS of the log-ratio
and the Spearman rank correlation.
"""

from __future__ import annotations

import csv
import math
import re
from pathlib import Path
from typing import Any

from hw_dse.families import ArchConfig

COLUMNS = (
    "tool", "tool_version", "part", "rtl_source", "design_key", "stage", "clock_ns", "toggle_rate_pct",
    "total_w", "dynamic_w", "static_w", "core_w", "clocks_w", "slice_logic_w", "signals_w", "io_w",
    "confidence", "command", "source_log",
)
"""``stage``: ``post-synthesis`` or ``post-route``; ``clock_ns``: the clock the
power report used (10 = the design's constraint; 1 = the resolution run);
``core_w`` = clocks + slice logic + signals (+ any other non-I/O on-chip rows)."""

_SUMMARY = {"total_w": "Total On-Chip Power (W)", "dynamic_w": "Dynamic (W)", "static_w": "Device Static (W)"}
_COMPONENTS = {"Clocks": "clocks_w", "Slice Logic": "slice_logic_w", "Signals": "signals_w", "I/O": "io_w"}
_NOT_CORE = {"I/O", "Static Power", "Total", "Device Static", "On-Chip"}


def _w(text: str) -> float:
    """A report value in W: '0.012' -> 0.012; '<0.001' -> 0.0005 (half the printed resolution)."""
    t = text.strip()
    if t.startswith("<"):
        return float(t[1:]) / 2
    return float(t)


def parse_report_power(text: str) -> dict[str, Any]:
    """Summary and on-chip component rows of a Vivado ``report_power`` text report."""
    out: dict[str, Any] = {}
    for key, label in _SUMMARY.items():
        m = re.search(r"^\|\s*" + re.escape(label) + r"\s*\|\s*([<0-9.]+)\s*\|", text, re.M)
        if m:
            out[key] = _w(m.group(1))
    m = re.search(r"^\|\s*Confidence Level\s*\|\s*(\w+)\s*\|", text, re.M)
    out["confidence"] = m.group(1) if m else ""
    sec = text.split("On-Chip Components", 1)[1] if "On-Chip Components" in text else ""
    core = 0.0
    for row in re.finditer(r"^\|\s*([A-Za-z/ ]+?)\s*\|\s*([<0-9.]+)\s*\|", sec, re.M):
        name, val = row.group(1).strip(), _w(row.group(2))
        if name in _COMPONENTS:
            out[_COMPONENTS[name]] = val
        if name not in _NOT_CORE:
            core += val
        if name == "Total":
            break
    if sec:
        out["core_w"] = core
    if "dynamic_w" not in out:
        raise ValueError("no 'Dynamic (W)' row: not a report_power summary")
    return out


def write(path: Path, rows: list[dict[str, Any]]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(COLUMNS))
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLUMNS})


def load(path: Path) -> list[dict[str, Any]]:
    with open(path, newline="", encoding="utf-8") as fh:
        rd = csv.DictReader(fh)
        if tuple(rd.fieldnames or ()) != COLUMNS:
            raise ValueError(f"{path}: columns {rd.fieldnames} are not the power schema {COLUMNS}")
        rows = list(rd)
    for r in rows:
        ArchConfig.from_key(r["design_key"])  # validates the design
        for c in ("clock_ns", "dynamic_w", "core_w"):
            float(r[c])
    return rows


def _spearman(a: list[float], b: list[float]) -> float:
    def ranks(x: list[float]) -> list[float]:
        order = sorted(range(len(x)), key=lambda i: x[i])
        r = [0.0] * len(x)
        for pos, i in enumerate(order):
            r[i] = float(pos)
        return r

    ra, rb = ranks(a), ranks(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    va = math.sqrt(sum((x - ma) ** 2 for x in ra))
    vb = math.sqrt(sum((y - mb) ** 2 for y in rb))
    return cov / (va * vb) if va and vb else float("nan")


REFERENCE_KEY = "iterative:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=trunc"


def compare(rows: list[dict[str, Any]], stage: str = "post-route", resolution_clock_ns: float = 1.0) -> dict[str, Any]:
    """Power index (M1 FPGA model, at 100 MHz) vs measured core power at 100 MHz, both
    relative to the reference iterative design."""
    from hw_dse.evaluate import default_cost_model, evaluate

    cm = default_cost_model()
    meas: dict[str, float] = {}
    for r in rows:
        if r["stage"] == stage and abs(float(r["clock_ns"]) - resolution_clock_ns) < 1e-9:
            meas[r["design_key"]] = float(r["core_w"]) * resolution_clock_ns / 10.0  # -> 100 MHz
    if REFERENCE_KEY not in meas:
        raise ValueError(f"the reference design {REFERENCE_KEY} has no {stage} row at {resolution_clock_ns} ns")
    out = []
    for key, p in sorted(meas.items()):
        rec = evaluate(ArchConfig.from_key(key))  # no spec: the index at Fmax; rescale to 100 MHz below
        idx100 = rec["power_index"] * 100.0 / rec["f_op_mhz"]
        rel = p / meas[REFERENCE_KEY]
        out.append({"key": key, "power_index_100mhz": idx100, "measured_core_mw_100mhz": p * 1e3,
                    "measured_relative": rel, "ratio_index_to_measured": idx100 / rel})
    logs = [math.log(o["ratio_index_to_measured"]) for o in out if o["key"] != REFERENCE_KEY]
    return {"stage": stage, "n": len(out), "provenance_index": cm.provenance,
            "rms_log_ratio_pct": (math.exp(math.sqrt(sum(x * x for x in logs) / len(logs))) - 1) * 100 if logs else None,
            "spearman": _spearman([o["power_index_100mhz"] for o in out], [o["measured_relative"] for o in out]),
            "designs": out}
