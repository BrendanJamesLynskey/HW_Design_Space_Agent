"""Analytical ASIC cost model for the CORDIC families on sky130 (provenance: estimate).

The second target of milestone 4. Like :mod:`hw_dse.models.cost_fpga` it is
*structural*: it counts what each family must contain and converts the
counts to cost with a handful of constants. Unlike the FPGA model, whose
constants came from two anchors, these are fitted by least squares to every
point of the ASIC synthesis sweep (57 designs over all four families,
Yosys 0.33 + OpenSTA on sky130_fd_sc_hd at tt_025C_1v80,
``eval/data/asic_synthesis.csv``), and the fit is checked **leave-one-out**,
as the L5 refit of the FPGA model is.

What it estimates
-----------------
* **area** in um^2 (the sum of cell areas, as Yosys ``stat -liberty``
  reports it) and in **gate equivalents** (area / NAND2_X1 area, 3.7536 um^2);
* **flip-flops**, the number of flip-flop cells;
* the **critical path** (register to register, post-synthesis, the
  library's wire-load model) and Fmax = 1000 / path;
* a **relative power index**: the same formula the FPGA target uses,
  switching resources x operating clock x activity, normalised to the
  reference ``iterative`` W=16 N=14 at 100 MHz = 1.0. Here the switching
  resources are a weighted sum of flip-flops and area whose weights are
  fitted to OpenSTA's vectorless ``report_power``. That makes the index a
  faithful copy of *that* tool's estimate (0.6% RMS), which is itself only a
  toggle-rate model: it is a ranking aid with no unit, never watts.

Structure (no constants in here)
--------------------------------
Notation as in the FPGA model: W data width, N iterations, A angle width,
g fractional guard bits, WX = W+2+g, WZ = A+2.

``add_bits``
    One per adder/subtractor bit, the FPGA model's ``arith_bits``: two WX-bit
    add/subs (x, y) and one WZ-bit add/sub (z) per micro-rotation, the FSM
    control term, the pipelined families' two constant trims, and the output
    rounding adders.
``mux2``
    The FSM families' variable shifters as 2:1 multiplexers: an output bit
    that can come from s distinct source bits needs s - 1 of them (a tree;
    ABC then packs them into mux4 cells), two shifters per chained rotation,
    plus one per shifter for the rounding bit. Pipelined families shift by
    constants: zero.
``reg_bits``
    The FPGA model's register count, unchanged.
``chain``, ``adder_bits``, ``mux_levels``
    Micro-rotations chained combinationally per cycle, the widest adder, and
    the 2:1-mux levels of the widest shifter (ceil(log2 s)).

The fitted model
----------------
::

    area_um2 = a_add_pipe * add_bits      (pipelined families)
             | a_add_fsm  * add_bits + a_fsm   (FSM families)
             + a_mux * mux2 + a_ff * reg_bits
    ffs      = c_ff_pipe * reg_bits | c_ff_fsm * reg_bits
    path_ns  = t_0 + chain * (t_fsm_stage [FSM only] + t_bit * adder_bits
                              + t_mux * mux_levels)
    switching = w_ff * ffs + w_area * area_um2

Why these terms (the alternatives were tried on the same data, leave-one-out
RMS in brackets; ``eval/data/asic_calibration.md``): one adder constant for
every family under-predicts the FSM families by up to 38% [14.8%]; a
separate FSM adder constant and a fixed FSM overhead [8.7%] fix most of it
(the FSM datapath's adders sit behind operand-select logic the pipelined
stages do not need). The ROM term came out negative and was dropped. The
generated FSM RTL registers W more bits than the FPGA model's register
count (the result is held in an output register while the datapath is
idle), hence the per-class flip-flop factor. The adder delay is linear in
the width (0.28 ns/bit): Yosys's default ``$alu`` mapping, re-mapped by ABC
at a 10 ns target, ripples.

Read the residuals before trusting a number: they are in the calibration
report, per family, and in the README. ``python -m hw_dse.models.cost_asic``
refits from the committed CSV, rewrites ``calibration_sky130hd.yaml`` and the
report; ``tests/test_asic.py`` checks the stored constants are what the fit
produces.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from hw_dse.families import ArchConfig
from hw_dse.models.cost_base import CostEstimate
from hw_dse.models.cost_fpga import stage_shift_sets, structure

CALIBRATION_FILE = Path(__file__).with_name("calibration_sky130hd.yaml")
NAND2_AREA_UM2 = 3.7536


@dataclass(frozen=True)
class AsicStructure:
    add_bits: int
    mux2: int
    reg_bits: int
    chain: int
    adder_bits: int
    mux_levels: int
    fsm: bool


def shifter_mux2(width: int, shifts: tuple[int, ...]) -> int:
    """2:1 muxes of a ``width``-bit arithmetic right shifter over ``shifts``."""
    return sum(len({min(b + s, width - 1) for s in shifts}) - 1 for b in range(width))


@lru_cache(maxsize=None)
def asic_structure(arch: ArchConfig) -> AsicStructure:
    s = structure(arch)
    num = arch.numerics
    mux = levels = 0
    if not arch.is_pipelined:
        for shifts in stage_shift_sets(arch):
            per = shifter_mux2(num.xy_width, shifts)
            if num.rounding == "round":
                per += len(shifts) - 1
            mux += 2 * per
            levels = max(levels, math.ceil(math.log2(len(shifts))) if len(shifts) > 1 else 0)
    return AsicStructure(s.arith_bits, mux, s.reg_bits, s.chain, s.adder_bits, levels, not arch.is_pipelined)


def area_features(s: AsicStructure) -> list[float]:
    f = 1.0 if s.fsm else 0.0
    return [s.add_bits * (1 - f), s.add_bits * f, f, float(s.mux2), float(s.reg_bits)]


AREA_TERMS = ("a_add_pipe", "a_add_fsm", "a_fsm", "a_mux", "a_ff")


def path_features(s: AsicStructure) -> list[float]:
    f = 1.0 if s.fsm else 0.0
    return [1.0, s.chain * f, float(s.chain * s.adder_bits), float(s.chain * s.mux_levels)]


PATH_TERMS = ("t_0", "t_fsm_stage", "t_bit", "t_mux")


@lru_cache(maxsize=None)
def load_calibration(path: str | None = None) -> dict[str, Any]:
    with open(path or CALIBRATION_FILE, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


class AsicCostModel:
    """CostModel implementation for sky130_fd_sc_hd standard cells."""

    name = "cost_asic"
    target = "asic"

    def __init__(self, calibration_path: str | None = None) -> None:
        self.cal = load_calibration(calibration_path)
        self.fit: dict[str, float] = self.cal["fitted"]
        self.calibration_id: str = self.cal["id"]
        self.provenance = f"estimate: {self.name} ({self.calibration_id}, {self.cal['n_points']} measured points)"
        self.src = {"activity_factor": float(self.cal["activity_factor"])}
        ref = self.cal["power_reference"]
        ref_est = self._raw(ArchConfig.from_params(ref["family"], ref["params"]))
        self.power_norm = ref_est[3] * float(ref["f_mhz"]) * self.src["activity_factor"]

    def _raw(self, arch: ArchConfig) -> tuple[float, float, float, float, AsicStructure]:
        s = asic_structure(arch)
        c = self.fit
        area = float(np.dot([c[t] for t in AREA_TERMS], area_features(s)))
        ffs = s.reg_bits * (c["c_ff_fsm"] if s.fsm else c["c_ff_pipe"])
        path = float(np.dot([c[t] for t in PATH_TERMS], path_features(s)))
        switching = c["w_ff"] * ffs + c["w_area"] * area
        return area, ffs, path, switching, s

    def estimate(self, arch: ArchConfig) -> CostEstimate:
        area, ffs, path, switching, s = self._raw(arch)
        return CostEstimate(
            area={"area_um2": area, "gate_eq": area / NAND2_AREA_UM2, "ffs": ffs},
            fmax_mhz=1000.0 / path,
            critical_path_ns=path,
            switching_resources=switching,
            activity_factor=self.src["activity_factor"],
            provenance=self.provenance,
            breakdown={"add_bits": s.add_bits, "mux2": s.mux2, "reg_bits": s.reg_bits, "chain": s.chain,
                       "adder_bits": s.adder_bits, "mux_levels": s.mux_levels},
        )


# ---------------------------------------------------------------------------
# Calibration: fit to the measured sweep, leave-one-out, report
# ---------------------------------------------------------------------------

def _nnls_rel(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Non-negative least squares on relative error: min sum ((x c - y) / y)^2."""
    from hw_dse.synth.recalibrate import _nnls

    return _nnls(x / y[:, None], np.ones(len(y)))


def _ratio_fit(x: np.ndarray, y: np.ndarray) -> float:
    """c minimising sum (c x / y - 1)^2."""
    r = x / y
    return float(r.sum() / (r * r).sum())


def fit_constants(points: list[Any]) -> dict[str, float]:
    """All constants of the model from measured :class:`~hw_dse.synth.asic.AsicPoint` rows."""
    S = [asic_structure(p.arch) for p in points]
    area = np.array([p.area_um2 for p in points])
    path = np.array([p.critical_path_ns for p in points])
    ffs = np.array([p.ffs for p in points])
    power = np.array([p.power_mw for p in points])
    ca = _nnls_rel(np.array([area_features(s) for s in S]), area)
    cp = _nnls_rel(np.array([path_features(s) for s in S]), path)
    fsm = np.array([s.fsm for s in S])
    rb = np.array([s.reg_bits for s in S], float)
    out = {**dict(zip(AREA_TERMS, map(float, ca))), **dict(zip(PATH_TERMS, map(float, cp)))}
    out["c_ff_fsm"] = _ratio_fit(rb[fsm], ffs[fsm])
    out["c_ff_pipe"] = _ratio_fit(rb[~fsm], ffs[~fsm])
    # Power weights are fitted on the *measured* flip-flop count and area, the
    # quantities OpenSTA's vectorless power actually depends on; the model then
    # applies them to its own estimates of both.
    cw = _nnls_rel(np.stack([ffs, area], axis=1), power)
    out["w_ff"], out["w_area"] = float(cw[0]), float(cw[1])
    return {k: round(v, 9) for k, v in out.items()}


def _predict(c: dict[str, float], arch: ArchConfig) -> dict[str, float]:
    s = asic_structure(arch)
    area = float(np.dot([c[t] for t in AREA_TERMS], area_features(s)))
    path = float(np.dot([c[t] for t in PATH_TERMS], path_features(s)))
    ffs = s.reg_bits * (c["c_ff_fsm"] if s.fsm else c["c_ff_pipe"])
    return {"area_um2": area, "critical_path_ns": path, "fmax_mhz": 1000.0 / path, "ffs": ffs,
            "power_mw": c["w_ff"] * ffs + c["w_area"] * area}


METRICS = ("area_um2", "ffs", "fmax_mhz", "power_mw")


def residual_table(points: list[Any], c: dict[str, float], loo: bool) -> list[dict[str, Any]]:
    rows = []
    for i, p in enumerate(points):
        ci = fit_constants(points[:i] + points[i + 1:]) if loo else c
        pr = _predict(ci, p.arch)
        meas = {"area_um2": p.area_um2, "ffs": p.ffs, "fmax_mhz": p.fmax_mhz, "power_mw": p.power_mw}
        rows.append({"key": p.arch.key(), "family": p.arch.family,
                     **{f"{m}_meas": meas[m] for m in METRICS}, **{f"{m}_est": round(pr[m], 4) for m in METRICS},
                     **{f"{m}_err_pct": round((pr[m] / meas[m] - 1) * 100, 2) for m in METRICS}})
    return rows


def _rms(xs: list[float]) -> float:
    return round(math.sqrt(sum(x * x for x in xs) / len(xs)), 2) if xs else float("nan")


def summarise(rows: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {"all": {m: _rms([r[f"{m}_err_pct"] for r in rows]) for m in METRICS}}
    for fam in dict.fromkeys(r["family"] for r in rows):
        mine = [r for r in rows if r["family"] == fam]
        out[fam] = {m: _rms([r[f"{m}_err_pct"] for r in mine]) for m in METRICS}
        out[fam]["n"] = len(mine)
        out[fam]["worst"] = {m: max((r[f"{m}_err_pct"] for r in mine), key=abs) for m in METRICS}
    return out


def calibrate(csv_path: Path | None = None) -> dict[str, Any]:
    """Fit, residuals in-sample and leave-one-out; returns the calibration and its report."""
    from hw_dse.synth import asic

    pts = asic.load_csv(csv_path or asic.ASIC_CSV)
    c = fit_constants(pts)
    ins = residual_table(pts, c, loo=False)
    loo = residual_table(pts, c, loo=True)
    tv = sorted({p.row["tool_version"] for p in pts})
    cal = {
        "id": "sky130hd-tt_025C_1v80-yosys0.33-opensta-v1",
        "target": "asic",
        "library": asic.LIBRARY,
        "corner": asic.CORNER,
        "tool": "; ".join(tv) + (f"; liberty {asic.LIB_NAME} (OpenROAD-flow-scripts {asic.ORFS_COMMIT[:9]}, "
                                 f"sha256 {asic.LIB_SHA256[:12]}...) minus lpflow_*/probe_* cells; "
                                 f"{asic.CLOCK_NS:g} ns clock; post-synthesis STA, wire-load model"),
        "n_points": len(pts),
        "source": "eval/data/asic_synthesis.csv",
        "activity_factor": asic.ACTIVITY,
        "fitted": c,
        "power_reference": {"family": "iterative", "f_mhz": 100.0,
                            "params": {"data_width": 16, "n_iter": 14, "angle_guard": 0, "frac_guard": 0,
                                       "rounding": "trunc"}},
        "residuals_rms_pct": {"in_sample": summarise(ins)["all"], "leave_one_out": summarise(loo)["all"]},
    }
    return {"calibration": cal, "in_sample": ins, "leave_one_out": loo,
            "summary": {"in_sample": summarise(ins), "leave_one_out": summarise(loo)}}


ALTERNATIVES = {
    # name -> (area feature function, path feature function); evaluated in the report only
    "area: one adder constant": lambda s: [s.add_bits, s.mux2, s.reg_bits],
    "area: + FSM adder constant + FSM overhead (chosen)": area_features,
    "path: one stage constant": lambda s: [1.0, s.chain, s.chain * s.adder_bits, s.chain * s.mux_levels],
    "path: FSM stage constant (chosen)": path_features,
}


def alternatives(points: list[Any]) -> dict[str, float]:
    """Leave-one-out RMS of each alternative feature set (the report's table)."""
    out = {}
    for name, fn in ALTERNATIVES.items():
        y = np.array([p.area_um2 if name.startswith("area") else p.critical_path_ns for p in points])
        x = np.array([fn(asic_structure(p.arch)) for p in points], float)
        errs = []
        for i in range(len(y)):
            m = np.arange(len(y)) != i
            ci = _nnls_rel(x[m], y[m])
            errs.append((x[i] @ ci / y[i] - 1) * 100)
        out[name] = _rms(errs)
    return out


def markdown(rep: dict[str, Any], alts: dict[str, float]) -> str:
    cal = rep["calibration"]
    L = ["# ASIC cost model calibration (sky130_fd_sc_hd, tt_025C_1v80)\n",
         "Generated by `python -m hw_dse.models.cost_asic` from `eval/data/asic_synthesis.csv`. Every *measured* "
         f"number: {cal['tool']}. Every *estimate*: `{cal['id']}`.\n",
         f"Points: {cal['n_points']} generated designs, all four families. Errors are (estimate / measured − 1).\n",
         "## Fitted constants\n", "| constant | value |", "|---|---|"]
    L += [f"| `{k}` | {v:.6g} |" for k, v in cal["fitted"].items()]
    L.append("\n## RMS error (%), in-sample and leave-one-out\n")
    L.append("| family | n | area in / LOO | FFs in / LOO | Fmax in / LOO | power in / LOO | worst LOO area / Fmax |")
    L.append("|---|---|---|---|---|---|---|")
    ins, loo = rep["summary"]["in_sample"], rep["summary"]["leave_one_out"]
    for fam in ("all", "iterative", "unrolled_k", "pipelined", "pipelined_m"):
        n = loo[fam].get("n", cal["n_points"]) if fam != "all" else cal["n_points"]
        worst = (f"{loo[fam]['worst']['area_um2']:+.1f} / {loo[fam]['worst']['fmax_mhz']:+.1f}" if fam != "all" else "")
        L.append(f"| {fam} | {n} | " + " | ".join(f"{ins[fam][m]:.1f} / {loo[fam][m]:.1f}" for m in METRICS)
                 + f" | {worst} |")
    L.append("\n## Feature sets compared (leave-one-out RMS %)\n")
    L.append("| model | LOO RMS % |")
    L.append("|---|---|")
    L += [f"| {k} | {v:.1f} |" for k, v in alts.items()]
    L.append("\n## Every point, leave-one-out\n")
    L.append("| design | area meas / err | FFs meas / err | Fmax meas / err | power mW meas / err |")
    L.append("|---|---|---|---|---|")
    for r in rep["leave_one_out"]:
        L.append(f"| `{r['key']}` | " + " | ".join(
            f"{r[m + '_meas']:.4g} / {r[m + '_err_pct']:+.1f}%" for m in METRICS) + " |")
    L.append("\nThe power column checks the model's power index (before normalisation) against OpenSTA's "
             "vectorless `report_power`: agreement means the index reproduces *that tool's* toggle-rate "
             "estimate, not measured silicon power.")
    return "\n".join(L) + "\n"


def main() -> None:  # pragma: no cover - CLI
    from hw_dse.rtl.generator import REPO_ROOT
    from hw_dse.synth import asic

    rep = calibrate()
    alts = alternatives(asic.load_csv())
    with open(CALIBRATION_FILE, "w", encoding="utf-8") as fh:
        fh.write("# Calibration of hw_dse.models.cost_asic: fitted by `python -m hw_dse.models.cost_asic`\n"
                 "# to every point of eval/data/asic_synthesis.csv. tests/test_asic.py fails if these\n"
                 "# constants drift from what the fit produces. Residuals: eval/data/asic_calibration.md.\n")
        yaml.safe_dump(rep["calibration"], fh, sort_keys=False)
    out = REPO_ROOT / "eval" / "data" / "asic_calibration"
    out.with_suffix(".md").write_text(markdown(rep, alts))
    out.with_suffix(".json").write_text(json.dumps({**rep, "alternatives": alts}, indent=1))
    print(json.dumps(rep["summary"]["leave_one_out"]["all"]), "->", CALIBRATION_FILE)


if __name__ == "__main__":  # pragma: no cover
    main()
