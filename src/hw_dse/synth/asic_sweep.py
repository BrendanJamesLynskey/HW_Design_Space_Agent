"""The ASIC synthesis sweep (milestone 4): which designs are measured on sky130.

Points (all generated RTL, sky130_fd_sc_hd, tt_025C_1v80, 10 ns clock; see
:mod:`hw_dse.synth.asic`):

* **every generated point of the FPGA sweep** (:func:`hw_dse.synth.sweep.points`:
  the two anchors, the six Vivado points, the three FPGA ground-truth winners
  and the spread over every family), so the two targets can be compared
  design for design;
* **an ASIC spread** (:data:`ASIC_EXTRA`) that fills the gaps the cost-model
  calibration needs: k and m from 2 to 8 at a second width, iterative at more
  widths, both rounding modes and guard bits off the anchors' defaults;
* **the ASIC specs' ground-truth winners** (:data:`ASIC_GT_WINNERS`), so the
  eval's "true optimum" designs on the new target have measured counterparts.

There is no placement seed to vary (no place-and-route), and Yosys/ABC and
OpenSTA are deterministic, so each design is synthesised once.
"""

from __future__ import annotations

import gzip
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from hw_dse.families import ArchConfig
from hw_dse.rtl.generator import REPO_ROOT, generate
from hw_dse.synth import asic
from hw_dse.synth.sweep import _a
from hw_dse.synth.sweep import points as fpga_points

ASIC_EXTRA = [
    _a("iterative", 10, 8), _a("iterative", 14, 12, 1, 0, "round"), _a("iterative", 18, 16), _a("iterative", 22, 20, 0, 2),
    _a("iterative", 26, 24, 1, 1, "round"),
    _a("unrolled_k", 12, 12, k=3), _a("unrolled_k", 12, 12, k=4), _a("unrolled_k", 12, 12, k=6),
    _a("unrolled_k", 12, 12, k=8), _a("unrolled_k", 20, 18, 0, 1, "round", k=2), _a("unrolled_k", 16, 14, k=6),
    _a("pipelined", 12, 10), _a("pipelined", 24, 22, 1, 1, "round"), _a("pipelined", 14, 12, 0, 2),
    _a("pipelined_m", 20, 18, m=2), _a("pipelined_m", 20, 18, m=3), _a("pipelined_m", 20, 18, m=5),
    _a("pipelined_m", 20, 18, m=7), _a("pipelined_m", 20, 18, 1, 1, "round", m=4), _a("pipelined_m", 12, 10, m=8),
]
# Filled in once the ASIC ground truth exists (eval/run_eval.py ground-truth-m4).
ASIC_GT_WINNERS: list[ArchConfig] = []


def points() -> list[ArchConfig]:
    seen: set[str] = set()
    out = []
    for a in fpga_points() + ASIC_EXTRA + ASIC_GT_WINNERS:
        if a.key() not in seen:
            seen.add(a.key())
            out.append(a)
    return out


def run(arches: list[ArchConfig], tools: asic.AsicTools | None = None, workers: int = 4,
        root: Path = asic.ASIC_BUILD, log: bool = True) -> list[tuple[ArchConfig, asic.AsicResult]]:
    tools = tools or asic.AsicTools.from_env()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(asic.synthesize_arch, a, tools, True, root) for a in arches]
        out = []
        for a, f in zip(arches, futs):
            r = f.result()
            if log:
                print(f"{a.key():78s} {r.area_um2:9.1f} um2 {r.gate_eq:7.0f} GE FF {r.ffs:4d} "
                      f"path {r.critical_path_ns:.3f} ns  P {r.power.get('power_mw', 0):.4f} mW  {r.seconds}s", flush=True)
            out.append((a, r))
    return out


def to_rows(results: list[tuple[ArchConfig, asic.AsicResult]], versions: dict[str, str],
            keep_logs: bool = True) -> list[dict[str, object]]:
    rows = []
    if keep_logs:
        asic.ASIC_LOGS.mkdir(parents=True, exist_ok=True)
    tv = f"yosys {versions['yosys']} + OpenSTA {versions.get('sta', '?')}"
    for a, r in results:
        log_rel = ""
        if keep_logs:
            name = generate(a).module
            wd = Path(r.workdir)
            # mtime=0: the gzip header carries no timestamp, so a re-run writes identical bytes
            text = (f"===== {r.yosys_cmd}\n" + (wd / "stat.txt").read_text() + f"===== {r.sta_cmd}\n"
                    + (wd / "sta.tcl").read_text() + (wd / "sta.log").read_text())
            text = text.replace(str(REPO_ROOT) + "/", "")  # no local paths in committed logs
            with open(asic.ASIC_LOGS / f"{name}.log.gz", "wb") as raw, \
                    gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz:
                gz.write(text.encode())
            log_rel = str((asic.ASIC_LOGS / f"{name}.log.gz").relative_to(REPO_ROOT))
        p = a.params()
        lib_rel = f"{asic.LIB_NAME} minus lpflow_*/probe_* cells"
        rows.append({
            "tool": asic.TOOL, "tool_version": tv, "library": asic.LIBRARY, "corner": asic.CORNER,
            "rtl_source": "generated", "family": a.family, "data_width": p["data_width"], "n_iter": p["n_iter"],
            "angle_guard": p["angle_guard"], "frac_guard": p["frac_guard"], "rounding": p["rounding"], "k": a.k,
            "m": a.m, "area_um2": round(r.area_um2, 4), "gate_eq": round(r.gate_eq, 2), "n_cells": r.n_cells,
            "ffs": r.ffs, "critical_path_ns": round(r.critical_path_ns or 0.0, 4),
            "fmax_mhz": round(r.fmax_mhz or 0.0, 3),
            "fmax_kind": "post-synthesis (OpenSTA, reg2reg, wire-load 'Small', no placement): 1000/(T - slack)",
            "power_mw": round(r.power.get("power_mw", 0.0), 6),
            "power_internal_mw": round(r.power.get("power_internal_mw", 0.0), 6),
            "power_switching_mw": round(r.power.get("power_switching_mw", 0.0), 6),
            "power_leakage_mw": round(r.power.get("power_leakage_mw", 0.0), 9),
            "power_kind": f"OpenSTA report_power, vectorless: every net activity {asic.ACTIVITY:g}/clock, duty 0.5, "
                          f"at the {asic.CLOCK_NS:g} ns clock",
            "clock_ns": f"{asic.CLOCK_NS:g}",
            "command": (r.yosys_cmd + " && " + r.sta_cmd).replace(str(REPO_ROOT) + "/", ""),
            "source_log": log_rel,
            "notes": f"liberty {lib_rel}; cells {r.n_cells}",
        })
    return rows
