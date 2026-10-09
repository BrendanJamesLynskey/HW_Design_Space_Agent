"""Ground truth, baselines and run scoring for the eval ("why use an LLM?").

The question the eval answers: on the same evaluation budget, does an
LLM-steered exploration find a better Pareto front, sooner, than plain
optimisers with no LLM? To answer it honestly we need the *right answer*,
and the M1 design space is small enough to just enumerate it.

Ground truth (:func:`build_grid`, :func:`ground_truth`)
    Every design in the registry: 39,690 numeric configurations x
    (iterative + 7 unrolled_k + pipelined + 7 pipelined_m) = 635,040
    designs. Cost-model numbers are computed for all of them (cheap) and
    accuracy comes from the precomputed exact table. For each spec this
    gives the true feasible set, the true Pareto front and the true
    hypervolume (HV), plus the design the spec's selection rule would pick.

Baselines (:func:`run_baseline`)
    (a) Optuna NSGA-II over the union of all families and full ranges;
    (b) random search over the same space. Same evaluation function,
    same budget, several seeds.

Scoring (:func:`score_run`)
    For any ordered list of evaluations (a baseline run or an agent run):
    final HV as a fraction of the true HV, the number of evaluations
    needed to reach 95% of the true HV (or ``None`` if never), whether
    the design selected at the end meets the spec, and whether the method
    concluded "infeasible" exactly when the ground truth says so.

The grid is held as NumPy columns, not a list of dicts (635k dicts would
cost ~1 GB); only front designs are turned back into full records.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import numpy as np

from hw_dse.evaluate import EvalRecord, default_cost_model, evaluate, objective_vector, reference_point
from hw_dse.explore import run_union_study
from hw_dse.families import REGISTRY, ArchConfig, full_box
from hw_dse.models.cordic_bitexact import accuracy
from hw_dse.pareto import hv_progress, hypervolume, pareto_front_large
from hw_dse.spec import Spec

FAMILY_INDEX = {name: i for i, name in enumerate(REGISTRY)}
PARAM_COLS = ("data_width", "n_iter", "angle_guard", "frac_guard", "k", "m")


@dataclass
class Grid:
    """Spec-independent columns for every design in the registry."""

    family: np.ndarray  # int index into REGISTRY
    params: dict[str, np.ndarray]  # PARAM_COLS + "rounding" (0 trunc / 1 round)
    luts: np.ndarray
    ffs: np.ndarray
    fmax_mhz: np.ndarray
    results_per_cycle: np.ndarray
    latency_cycles: np.ndarray
    switching: np.ndarray
    max_abs_err: np.ndarray
    rms_err: np.ndarray
    accuracy_bits: np.ndarray
    power_norm: float
    activity: float
    cost_model: Any = None  # the model the columns were computed with (build_grid sets it)

    def __len__(self) -> int:
        return int(self.family.size)

    def arch(self, i: int) -> ArchConfig:
        fam = list(REGISTRY)[int(self.family[i])]
        p = {c: int(self.params[c][i]) for c in PARAM_COLS}
        p["rounding"] = "round" if self.params["rounding"][i] else "trunc"  # type: ignore[assignment]
        return ArchConfig.from_params(fam, p)

    def metrics(self, spec: Spec) -> dict[str, np.ndarray]:
        """All spec metrics as columns (power index depends on the spec)."""
        thr = self.fmax_mhz * self.results_per_cycle
        req = spec.min_throughput_msps
        f_op = self.fmax_mhz if req is None else np.minimum(self.fmax_mhz, req / self.results_per_cycle)
        return {
            "luts": self.luts,
            "ffs": self.ffs,
            "luts_plus_ffs": self.luts + self.ffs,
            "fmax_mhz": self.fmax_mhz,
            "throughput_msps": thr,
            "latency_cycles": self.latency_cycles,
            "latency_ns": self.latency_cycles * 1000.0 / self.fmax_mhz,
            "power_index": self.switching * f_op * self.activity / self.power_norm,
            "max_abs_err": self.max_abs_err,
            "rms_err": self.rms_err,
            "accuracy_bits": self.accuracy_bits,
        }


def all_designs() -> list[ArchConfig]:
    from hw_dse.explore import enumerate_box

    out: list[ArchConfig] = []
    for fam in REGISTRY:
        out.extend(enumerate_box(fam, full_box(fam)))
    return out


def build_grid(verbose: bool = False, cost_model: Any = None) -> Grid:
    """Every registry design under ``cost_model`` (default: the M1 calibration)."""
    t0 = time.time()
    cm = cost_model or default_cost_model()
    designs = all_designs()
    n = len(designs)
    cols = {c: np.zeros(n, dtype=np.int16) for c in (*PARAM_COLS, "rounding")}
    fam = np.zeros(n, dtype=np.int8)
    f = {k: np.zeros(n) for k in ("luts", "ffs", "fmax", "rpc", "lat", "sw", "err", "rms", "bits")}
    for i, a in enumerate(designs):
        est = cm.estimate(a)
        acc = accuracy(a.numerics)
        fam[i] = FAMILY_INDEX[a.family]
        nm = a.numerics
        cols["data_width"][i] = nm.data_width
        cols["n_iter"][i] = nm.n_iter
        cols["angle_guard"][i] = nm.A - nm.data_width
        cols["frac_guard"][i] = nm.frac_guard
        cols["rounding"][i] = 1 if nm.rounding == "round" else 0
        cols["k"][i] = a.k
        cols["m"][i] = a.m
        f["luts"][i], f["ffs"][i] = est.area["luts"], est.area["ffs"]
        f["fmax"][i], f["rpc"][i], f["lat"][i] = est.fmax_mhz, a.results_per_cycle, a.latency_cycles
        f["sw"][i] = est.switching_resources
        f["err"][i], f["rms"][i], f["bits"][i] = acc.max_abs, acc.rms, acc.accuracy_bits
        if verbose and i % 100_000 == 0:
            print(f"  grid {i}/{n}  {time.time() - t0:.0f}s", flush=True)
    return Grid(
        family=fam,
        params=cols,
        luts=f["luts"],
        ffs=f["ffs"],
        fmax_mhz=f["fmax"],
        results_per_cycle=f["rpc"],
        latency_cycles=f["lat"],
        switching=f["sw"],
        max_abs_err=f["err"],
        rms_err=f["rms"],
        accuracy_bits=f["bits"],
        power_norm=cm.power_norm,
        activity=cm.src["activity_factor"],
        cost_model=cm,
    )


def _feasible_mask(m: dict[str, np.ndarray], spec: Spec) -> np.ndarray:
    mask = np.ones(m["luts"].shape, dtype=bool)
    for c in spec.constraints:
        mask &= (m[c.metric] <= c.value) if c.op == "<=" else (m[c.metric] >= c.value)
    return mask


def ground_truth(grid: Grid, spec: Spec) -> dict[str, Any]:
    """True feasible set size, Pareto front, HV and auto-selected design.

    The front and the selected design are re-evaluated with the cost model the
    grid was built with (``grid.cost_model``), never silently with the default."""
    cost_model = grid.cost_model
    m = grid.metrics(spec)
    feas = _feasible_mask(m, spec)
    out: dict[str, Any] = {"spec": spec.name, "n_designs": len(grid), "n_feasible": int(feas.sum())}
    out["feasible"] = bool(feas.any())
    # Closest approach for infeasible specs: helps explain *why*.
    out["best_throughput_msps_any"] = float(m["throughput_msps"].max())
    if not feas.any():
        out.update(hv_true=0.0, front=[], selected=None)
        return out
    idx = np.flatnonzero(feas)
    sign = np.array([1.0 if o.direction == "min" else -1.0 for o in spec.objectives])
    obj = np.stack([m[o.metric][idx] for o in spec.objectives], axis=1) * sign
    front_local = pareto_front_large(obj)
    front_idx = idx[front_local]
    out["hv_true"] = hypervolume(obj[front_local], reference_point(spec))
    out["front"] = [evaluate(grid.arch(int(i)), spec, cost_model) for i in front_idx]
    sel = m[spec.select_by][idx]
    best_val = sel.min() if spec.select_direction == "min" else sel.max()
    ties = idx[np.flatnonzero(sel == best_val)]
    out["selected"] = select_design([evaluate(grid.arch(int(i)), spec, cost_model) for i in ties], spec)
    return out


def select_design(records: list[EvalRecord], spec: Spec) -> EvalRecord | None:
    """The spec's auto-selection rule applied to a set of evaluations."""
    feas = [r for r in records if r.get("feasible")]
    if not feas:
        return None
    sign = 1.0 if spec.select_direction == "min" else -1.0
    # Ties on the selection metric are broken by the objectives, then by key
    # (so selection is deterministic).
    return min(feas, key=lambda r: (sign * float(r[spec.select_by]), *objective_vector(r, spec), r["key"]))


def score_run(records: list[EvalRecord], spec: Spec, gt: dict[str, Any], declared_infeasible: bool | None = None,
              selected: EvalRecord | None = None) -> dict[str, Any]:
    """Score one ordered list of evaluations against the ground truth."""
    if records:
        pts = np.array([objective_vector(r, spec) for r in records])
        feas = np.array([bool(r["feasible"]) for r in records])
        prog = hv_progress(pts, feas, reference_point(spec))
    else:
        prog = np.zeros(0)
    hv_true = float(gt.get("hv_true") or 0.0)
    hv_final = float(prog[-1]) if prog.size else 0.0
    evals_95 = None
    if hv_true > 0 and prog.size:
        hit = np.flatnonzero(prog >= 0.95 * hv_true)
        evals_95 = int(hit[0]) + 1 if hit.size else None
    if selected is None:
        selected = select_design(records, spec)
    if declared_infeasible is None:
        declared_infeasible = selected is None
    regret = None
    gsel = gt.get("selected")
    if selected is not None and selected.get("feasible") and gsel:
        best = float(gsel[spec.select_by])
        regret = (float(selected[spec.select_by]) - best) / abs(best) * (1 if spec.select_direction == "min" else -1)
    return {
        "n_evals": len(records),
        "hv_final": hv_final,
        # Undefined for an infeasible spec (true HV is 0): reported as n/a.
        "hv_frac": (hv_final / hv_true) if hv_true > 0 else None,
        "evals_to_95": evals_95,
        "selected_meets_spec": bool(selected is not None and selected.get("feasible")),
        "selected_key": selected["key"] if selected else None,
        # How much worse the selected design is than the true best on the
        # spec's selection metric (0 = found the optimum).
        "select_regret": regret,
        "declared_infeasible": bool(declared_infeasible),
        "infeasibility_correct": bool(declared_infeasible) == (not gt["feasible"]),
    }


def run_baseline(spec: Spec, sampler: str, seed: int, budget: int | None = None) -> list[EvalRecord]:
    return run_union_study(spec, budget or spec.budget.total_evals, seed, sampler=sampler)  # type: ignore[arg-type]
