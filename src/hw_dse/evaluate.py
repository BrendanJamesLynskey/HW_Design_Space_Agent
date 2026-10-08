"""Score one design: every number, with where it came from.

:func:`evaluate` is the single place the project produces numbers about a
design. The optimisers (Optuna, random search, the exhaustive grid) and
the agent all call it, so they can never disagree about how a metric is
computed. The LLM never calls it; it only ever *reads* summaries of its
results.

Provenance labels
-----------------
Each record carries a ``provenance`` dict mapping metric name to a label:

``exact``
    Computed by the bit-accurate model over a documented angle sweep
    (accuracy metrics), or read off the schedule (latency in cycles).
``estimate``
    From the cost model, tagged with its calibration id
    (LUTs, FFs, Fmax, throughput, latency in ns, power index).
``measured``
    Reserved for milestone 2 (synthesis / place-and-route runs).

Derived metrics
---------------
* ``throughput_msps`` = Fmax (MHz) x results per cycle.
* ``latency_ns`` = latency cycles x clock period at Fmax.
* ``power_index`` = switching resources x f_op x activity, normalised to
  the reference iterative design at 100 MHz (= 1.0). ``f_op`` is the
  clock the design actually needs: if the spec requires T MSPS and the
  design produces r results per cycle, it runs at T / r MHz (capped at
  Fmax); with no throughput requirement it runs at Fmax. This makes a
  fast design that could idle along at a low clock look as cheap as it
  really is. It is a ranking aid with no unit; it is never shown in watts.
"""

from __future__ import annotations

import math
from functools import lru_cache
from typing import Any

from hw_dse.families import ArchConfig
from hw_dse.models.cordic_bitexact import accuracy
from hw_dse.models.cost_base import CostModel
from hw_dse.models.cost_fpga import FpgaCostModel
from hw_dse.spec import Spec

EvalRecord = dict[str, Any]

METRIC_COLUMNS = (
    "luts",
    "ffs",
    "luts_plus_ffs",
    "fmax_mhz",
    "throughput_msps",
    "latency_cycles",
    "latency_ns",
    "power_index",
    "max_abs_err",
    "max_abs_err_lsb",
    "rms_err",
    "rms_err_lsb",
    "accuracy_bits",
)


@lru_cache(maxsize=1)
def default_cost_model() -> FpgaCostModel:
    return FpgaCostModel()


def evaluate(arch: ArchConfig, spec: Spec | None = None, cost_model: CostModel | None = None) -> EvalRecord:
    """All metrics for one design, plus feasibility against ``spec``."""
    cm = cost_model or default_cost_model()
    acc = accuracy(arch.numerics)
    est = cm.estimate(arch)
    rpc = arch.results_per_cycle
    thr = est.fmax_mhz * rpc
    req = spec.min_throughput_msps if spec is not None else None
    f_op = est.fmax_mhz if req is None else min(est.fmax_mhz, req / rpc)
    norm = getattr(cm, "power_norm", 1.0)
    luts, ffs = est.area.get("luts", float("nan")), est.area.get("ffs", float("nan"))
    rec: EvalRecord = {
        "family": arch.family,
        **arch.params(),
        "key": arch.key(),
        "luts": luts,
        "ffs": ffs,
        "luts_plus_ffs": luts + ffs,
        "fmax_mhz": est.fmax_mhz,
        "throughput_msps": thr,
        "latency_cycles": arch.latency_cycles,
        "latency_ns": arch.latency_cycles * 1000.0 / est.fmax_mhz,
        "power_index": est.switching_resources * f_op * est.activity_factor / norm,
        "f_op_mhz": f_op,
        "max_abs_err": acc.max_abs,
        "max_abs_err_lsb": acc.max_abs_lsb,
        "rms_err": acc.rms,
        "rms_err_lsb": acc.rms_lsb,
        "accuracy_bits": acc.accuracy_bits,
    }
    exact = f"exact: bit-accurate model, {acc.sweep}"
    estimate = est.provenance
    rec["provenance"] = {
        **{m: estimate for m in ("luts", "ffs", "luts_plus_ffs", "fmax_mhz", "throughput_msps", "latency_ns", "power_index")},
        "latency_cycles": "exact: schedule",
        **{m: exact for m in ("max_abs_err", "max_abs_err_lsb", "rms_err", "rms_err_lsb", "accuracy_bits")},
    }
    if spec is not None:
        add_feasibility(rec, spec)
    return rec


def add_feasibility(rec: EvalRecord, spec: Spec) -> EvalRecord:
    """Annotate ``rec`` with per-constraint violations and ``feasible``."""
    viol = {str(c): c.violation(float(rec[c.metric])) for c in spec.constraints}
    rec["violations"] = viol
    rec["feasible"] = all(v <= 0 for v in viol.values())
    return rec


def objective_vector(rec: EvalRecord, spec: Spec) -> tuple[float, ...]:
    """Objectives in *minimisation* form (max objectives negated)."""
    return tuple(float(rec[o.metric]) * (1.0 if o.direction == "min" else -1.0) for o in spec.objectives)


def reference_point(spec: Spec) -> tuple[float, ...]:
    return tuple(o.ref * (1.0 if o.direction == "min" else -1.0) for o in spec.objectives)


def fmt_metric(metric: str, v: float) -> str:
    """Human formatting used in summaries and reports."""
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "n/a"
    if metric in ("max_abs_err", "rms_err"):
        return f"{v:.3g} (2^{math.log2(v):.2f})" if v > 0 else "0"
    if metric in ("luts", "ffs", "luts_plus_ffs", "latency_cycles"):
        return f"{v:.0f}"
    return f"{v:.3g}"
