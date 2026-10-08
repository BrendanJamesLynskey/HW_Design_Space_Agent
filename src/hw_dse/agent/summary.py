"""Turn hundreds of evaluation rows into a summary an LLM can actually read.

The ``analyse`` node never shows the model raw evaluation rows: a round
produces ~100 of them and the run up to 400, which would drown the signal
and cost tokens. Instead, code computes what an architect would look at:

* progress: round, budget used, hypervolume (HV) and its gain this round;
* feasibility: how many designs met every constraint, and for each
  constraint how often it failed and the best value any design achieved
  (this is what lets the model notice "nothing gets above 291 MSPS");
* the merged Pareto front (feasible designs only), at most ``MAX_FRONT``
  rows, spread along the first objective;
* per family: evaluations, feasible count, best value of the selection
  metric, and the range of each parameter that produced feasible designs;
* if nothing is feasible: the least-violating designs and their violations.

The same function also returns a small ``context`` dict (round, feasible
count, front boxes ...) that the rule-based fake architect uses in place
of reading text. Real LLMs only see the text.

All numbers here were produced by code, and the summary says which are
estimates and which are exact.
"""

from __future__ import annotations

import math
from collections import defaultdict
from typing import Any

import numpy as np

from hw_dse.evaluate import EvalRecord, fmt_metric, objective_vector
from hw_dse.families import REGISTRY
from hw_dse.pareto import pareto_mask
from hw_dse.spec import Spec

MAX_FRONT = 10


def merged_front(records: list[EvalRecord], spec: Spec) -> list[EvalRecord]:
    """Unique feasible non-dominated designs, sorted by the first objective."""
    uniq: dict[str, EvalRecord] = {}
    for r in records:
        if r.get("feasible"):
            uniq.setdefault(r["key"], r)
    feas = list(uniq.values())
    if not feas:
        return []
    pts = np.array([objective_vector(r, spec) for r in feas])
    front = [r for r, keep in zip(feas, pareto_mask(pts)) if keep]
    return sorted(front, key=lambda r: objective_vector(r, spec))


def _spread(rows: list[EvalRecord], n: int) -> list[EvalRecord]:
    if len(rows) <= n:
        return rows
    idx = np.unique(np.linspace(0, len(rows) - 1, n).round().astype(int))
    return [rows[i] for i in idx]


def _params_str(r: EvalRecord) -> str:
    keys = [p.name for p in REGISTRY[r["family"]].params]
    return " ".join(f"{k}={r[k]}" for k in keys)


def front_boxes(front: list[EvalRecord]) -> dict[str, list[dict[str, Any]]]:
    """Per family on the front: a box around the front designs (+/-1)."""
    out: dict[str, list[dict[str, Any]]] = {}
    by_fam: dict[str, list[EvalRecord]] = defaultdict(list)
    for r in front:
        by_fam[r["family"]].append(r)
    for fam, rows in by_fam.items():
        ranges = []
        for p in REGISTRY[fam].params:
            if p.kind == "int":
                vals = [int(r[p.name]) for r in rows]
                ranges.append({"param": p.name, "low": max(p.low, min(vals) - 1), "high": min(p.high, max(vals) + 1)})
            else:
                ranges.append({"param": p.name, "choices": sorted({str(r[p.name]) for r in rows})})
        out[fam] = ranges
    return out


def summarise(
    spec: Spec,
    records: list[EvalRecord],
    *,
    round_no: int,
    max_rounds: int,
    budget_used: int,
    hv: float,
    hv_prev: float | None,
    explored: list[str],
    final_round: bool,
) -> tuple[str, dict[str, Any]]:
    """Compact text summary for the LLM, plus a context dict for fakes/routing."""
    n = len(records)
    feas = [r for r in records if r.get("feasible")]
    front = merged_front(records, spec)
    L: list[str] = []
    gain = None
    if hv_prev is not None:
        gain = (hv - hv_prev) / hv_prev if hv_prev > 0 else (math.inf if hv > 0 else 0.0)
    L.append(f"Round {round_no} of at most {max_rounds} complete. Evaluations used: {budget_used} of {spec.budget.total_evals}.")
    gain_txt = "n/a (first round)" if gain is None else ("+inf (first feasible designs)" if math.isinf(gain) else f"{gain * 100:+.1f}%")
    L.append(f"Hypervolume of the feasible front: {hv:.4g} (gain this round: {gain_txt}).")
    L.append(f"Feasible designs: {len(feas)} of {n} evaluations ({len({r['key'] for r in feas})} unique).")
    L.append(f"Families explored so far: {', '.join(explored)}. Not yet explored: "
             f"{', '.join(f for f in REGISTRY if f not in explored) or 'none'}.")
    L.append("Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); "
             "errors/accuracy bits are EXACT (bit-accurate model).")

    L.append("\nConstraints (fraction of evaluations violating; best value any design achieved):")
    for c in spec.constraints:
        vals = np.array([float(r[c.metric]) for r in records]) if records else np.array([])
        fail = float(np.mean([not c.satisfied(v) for v in vals])) if vals.size else 0.0
        best = (vals.min() if c.op == "<=" else vals.max()) if vals.size else float("nan")
        L.append(f"- {c}: {fail * 100:.0f}% violate; best seen {fmt_metric(c.metric, best)}")

    obj_names = [o.metric for o in spec.objectives]
    if front:
        L.append(f"\nPareto front (feasible, {len(front)} designs; showing up to {MAX_FRONT}), objectives: "
                 + ", ".join(f"{o.direction} {o.metric}" for o in spec.objectives))
        cols = ["luts", "ffs", "throughput_msps", "max_abs_err", "power_index"]
        for r in _spread(front, MAX_FRONT):
            L.append(f"- {r['family']} [{_params_str(r)}] " + ", ".join(
                f"{c}={fmt_metric(c, float(r[c]))}" for c in dict.fromkeys(obj_names + cols)))
    else:
        L.append("\nNo feasible design found yet. Least-violating designs:")
        ranked = sorted(records, key=lambda r: sum(max(v, 0.0) for v in r["violations"].values()))
        seen: set[str] = set()
        for r in ranked:
            if r["key"] in seen:
                continue
            seen.add(r["key"])
            viol = "; ".join(f"{k} violated by {v * 100:.1f}%" for k, v in r["violations"].items() if v > 0)
            L.append(f"- {r['family']} [{_params_str(r)}]: throughput={fmt_metric('throughput_msps', r['throughput_msps'])}, "
                     f"max_abs_err={fmt_metric('max_abs_err', r['max_abs_err'])}; {viol}")
            if len(seen) >= 5:
                break

    L.append("\nPer family:")
    by_fam: dict[str, list[EvalRecord]] = defaultdict(list)
    for r in records:
        by_fam[r["family"]].append(r)
    for fam in REGISTRY:
        rows = by_fam.get(fam)
        if not rows:
            continue
        f_rows = [r for r in rows if r.get("feasible")]
        line = f"- {fam}: {len(rows)} evals, {len(f_rows)} feasible"
        thr = max(float(r["throughput_msps"]) for r in rows)
        bits = max(float(r["accuracy_bits"]) for r in rows)
        line += f"; max throughput seen {fmt_metric('throughput_msps', thr)} MSPS; best accuracy {bits:.2f} bits"
        if f_rows:
            sel = [float(r[spec.select_by]) for r in f_rows]
            best = min(sel) if spec.select_direction == "min" else max(sel)
            line += f"; best feasible {spec.select_by}={fmt_metric(spec.select_by, best)}"
            spans = []
            for p in REGISTRY[fam].params:
                if p.kind == "int":
                    v = [int(r[p.name]) for r in f_rows]
                    spans.append(f"{p.name} {min(v)}..{max(v)}")
            line += "; feasible ranges: " + ", ".join(spans)
        L.append(line)

    ctx: dict[str, Any] = {
        "round": round_no,
        "n_feasible": len(feas),
        "hv": hv,
        "hv_gain": gain,
        "final_round": final_round,
        "front_boxes": front_boxes(front),
        "min_throughput_msps": spec.min_throughput_msps,
        "max_abs_err": (spec.constraint_for("max_abs_err", "<=").value if spec.constraint_for("max_abs_err", "<=") else None),
    }
    return "\n".join(L), ctx


def spec_context(spec: Spec) -> dict[str, Any]:
    c = spec.constraint_for("max_abs_err", "<=")
    return {"min_throughput_msps": spec.min_throughput_msps, "max_abs_err": c.value if c else None, "round": 0}
