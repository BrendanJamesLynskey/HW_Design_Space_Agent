"""Search machinery: Optuna studies, random search and grid enumeration.

This is where the optimisation actually happens, and it is all
deterministic code. Three entry points matter:

:func:`run_family_study`
    One Optuna NSGA-II study over one family inside a search box (the box
    comes from the LLM's ExplorationPlan, already clamped by the
    registry). The agent's ``explore`` node fans out one of these per
    family with LangGraph's ``Send``.

:func:`run_union_study`
    The baselines: one study over the *union* of all families and their
    full registry ranges, with ``family`` as just another categorical
    parameter. ``sampler="nsga2"`` is baseline (a), ``sampler="random"``
    is baseline (b). Same evaluation function, same budget accounting.

:func:`enumerate_box`
    Every design in a box, for the exhaustive ground truth.

How Optuna sees a design
------------------------
Each trial suggests integers for the numeric knobs and a categorical for
``rounding``; :class:`hw_dse.families.ArchConfig` turns that into a
design and :func:`hw_dse.evaluate.evaluate` scores it. The study's
objectives are the spec's objectives (with their directions), and the
spec's constraints are passed through ``constraints_func`` so NSGA-II
prefers feasible designs and, among infeasible ones, the least-violating
(Deb's constrained-domination rule).

Budget accounting
-----------------
Every trial is one evaluation, including repeats of a design already
seen (discrete spaces make NSGA-II re-propose designs). Agent and
baselines are counted the same way, so the eval compares like with like.
"""

from __future__ import annotations

import itertools
import logging
import math
from collections.abc import Callable, Iterator
from typing import Literal

import optuna

from hw_dse.evaluate import EvalRecord, evaluate
from hw_dse.families import REGISTRY, ArchConfig, ParamValue, Range, full_box
from hw_dse.spec import Spec

optuna.logging.set_verbosity(optuna.logging.WARNING)
logging.getLogger("optuna").setLevel(logging.WARNING)

UNION_EXTRA = {"k": (2, 8), "m": (2, 8)}


def population_size(n_trials: int) -> int:
    """NSGA-II population: enough generations to evolve inside a budget.

    Optuna's default (50) would spend a 40-trial round entirely on the
    random first generation; a quarter of the budget, clamped to 8..50,
    gives at least ~4 generations.
    """
    return max(8, min(50, n_trials // 4))


def _suggest(trial: optuna.Trial, name: str, rng: Range) -> ParamValue:
    if isinstance(rng[0], str):
        return trial.suggest_categorical(name, list(rng))
    lo, hi = int(rng[0]), int(rng[1])  # type: ignore[arg-type]
    return trial.suggest_int(name, lo, hi)


# Optuna 5 moved constraints from the sampler's ``constraints_func`` to
# ``Trial.set_constraint``; support both so optuna>=4 works.
_HAS_SET_CONSTRAINT = hasattr(optuna.trial.Trial, "set_constraint")


def _make_sampler(kind: str, seed: int, n_trials: int) -> optuna.samplers.BaseSampler:
    if kind == "random":
        return optuna.samplers.RandomSampler(seed=seed)
    kw: dict[str, object] = {}
    if not _HAS_SET_CONSTRAINT:
        kw["constraints_func"] = lambda t: t.user_attrs["constraints"]
    return optuna.samplers.NSGAIISampler(population_size=population_size(n_trials), seed=seed, **kw)


def _seed_study(study: optuna.Study, spec: Spec, seeds: list[tuple[dict[str, ParamValue], dict[str, Range]]]) -> int:
    """Warm-start NSGA-II with designs that were *already evaluated* earlier in the run.

    Each seed is added as a completed trial of generation 0, with its
    objective values and constraint violations recomputed by
    :func:`evaluate` (deterministic, so identical to what the earlier round
    saw). Seeds are not new evaluations and are not counted against the
    budget or returned as records: they only tell NSGA-II where the known
    front is, so its first offspring are bred from it instead of from
    random designs. Returns the number of seeds added.
    """
    gen_key = (NSGAIISampler_generation_key())
    n = 0
    for values, box in seeds:
        fam = str(values.get("family", ""))
        params = {k: v for k, v in values.items() if k in box}
        dists: dict[str, optuna.distributions.BaseDistribution] = {}
        ok = True
        for name, rng in box.items():
            v = params.get(name)
            if isinstance(rng[0], str):
                if v not in rng:
                    ok = False
                    break
                dists[name] = optuna.distributions.CategoricalDistribution(list(rng))
            else:
                lo, hi = int(rng[0]), int(rng[1])  # type: ignore[arg-type]
                if v is None or not lo <= int(v) <= hi:
                    ok = False
                    break
                dists[name] = optuna.distributions.IntDistribution(lo, hi)
        if not ok:
            continue
        arch_params = {k: v for k, v in params.items() if k != "family"}
        arch = ArchConfig.from_params(fam, arch_params)
        rec = evaluate(arch, spec)
        cons = list(rec["violations"].values()) or [0.0]
        attrs: dict[str, object] = {gen_key: 0}
        if _HAS_SET_CONSTRAINT:
            attrs.update({f"constraints:c{i}": float(c) for i, c in enumerate(cons)})
        else:
            attrs["constraints"] = [float(c) for c in cons]
        vals = [float(rec[o.metric]) for o in spec.objectives]
        study.add_trial(optuna.trial.create_trial(
            params=params, distributions=dists, values=[v if math.isfinite(v) else 1e9 for v in vals],
            system_attrs=attrs, user_attrs={"constraints": cons, "seed_design": True}))
        n += 1
    return n


def NSGAIISampler_generation_key() -> str:  # noqa: N802 - mirrors Optuna's class name
    """The system-attr key Optuna's NSGA-II uses for a trial's generation."""
    getter = getattr(optuna.samplers.NSGAIISampler, "_get_generation_key", None)
    return getter() if callable(getter) else "nsga2:generation"


def _run(
    spec: Spec,
    n_trials: int,
    seed: int,
    sampler: str,
    design_of: Callable[[optuna.Trial], ArchConfig],
    tag: dict[str, object],
    seeds: list[tuple[dict[str, ParamValue], dict[str, Range]]] | None = None,
    cost_model: object | None = None,
    transform: Callable[[EvalRecord], EvalRecord] | None = None,
) -> list[EvalRecord]:
    directions = ["minimize" if o.direction == "min" else "maximize" for o in spec.objectives]
    study = optuna.create_study(directions=directions, sampler=_make_sampler(sampler, seed, n_trials))
    if seeds and sampler == "nsga2":
        _seed_study(study, spec, seeds)
    records: list[EvalRecord] = []

    def objective(trial: optuna.Trial) -> tuple[float, ...]:
        arch = design_of(trial)
        rec = evaluate(arch, spec, cost_model)  # type: ignore[arg-type]
        if transform is not None:  # M4: e.g. the L2 -> L1 feedback's corrected system bounds
            rec = transform(rec)
        rec.update(tag)
        rec["trial"] = trial.number
        records.append(rec)
        # Optuna feasibility: every value <= 0 means feasible.
        cons = list(rec["violations"].values()) or [0.0]
        if _HAS_SET_CONSTRAINT:
            for i, v in enumerate(cons):
                trial.set_constraint(f"c{i}", v)
        else:
            trial.set_user_attr("constraints", cons)
        vals = tuple(float(rec[o.metric]) for o in spec.objectives)
        # Optuna rejects inf; accuracy_bits is inf only for a perfect design.
        return tuple(v if math.isfinite(v) else 1e9 for v in vals)

    study.optimize(objective, n_trials=n_trials, show_progress_bar=False)
    return records


def run_family_study(
    family: str,
    box: dict[str, Range],
    spec: Spec,
    n_trials: int,
    seed: int,
    sampler: Literal["nsga2", "random"] = "nsga2",
    tag: dict[str, object] | None = None,
    seed_designs: list[dict[str, ParamValue]] | None = None,
    cost_model: object | None = None,
    transform: Callable[[EvalRecord], EvalRecord] | None = None,
) -> list[EvalRecord]:
    """NSGA-II (default) over one family inside ``box``.

    ``seed_designs`` (parameter dicts of this family, already evaluated
    earlier in the run) warm-start NSGA-II; see :func:`_seed_study`.
    ``cost_model`` (default: the M1 calibration) lets the L5 re-exploration
    search under a refitted calibration. ``transform`` (milestone 4) rewrites
    each record before its feasibility reaches NSGA-II (the L2 -> L1 feedback
    uses it to screen with empirically corrected system bounds).
    """
    if family not in REGISTRY:
        raise KeyError(family)
    params = [p.name for p in REGISTRY[family].params]

    def design_of(trial: optuna.Trial) -> ArchConfig:
        values = {name: _suggest(trial, name, box[name]) for name in params}
        return ArchConfig.from_params(family, values)

    seeds = [({**d, "family": family}, box) for d in (seed_designs or [])]
    return _run(spec, n_trials, seed, sampler, design_of, {"source": f"study:{family}", **(tag or {})}, seeds,
                cost_model=cost_model, transform=transform)


def union_box() -> dict[str, Range]:
    box: dict[str, Range] = {"family": tuple(REGISTRY)}
    box.update(full_box("iterative"))
    box.update(UNION_EXTRA)
    return box


def run_union_study(
    spec: Spec,
    n_trials: int,
    seed: int,
    sampler: Literal["nsga2", "random"] = "nsga2",
) -> list[EvalRecord]:
    """Baselines: one flat study over every family and full range.

    ``k`` and ``m`` are always suggested (so the search space is fixed,
    which NSGA-II needs) and ignored by families that do not use them.
    """
    box = union_box()

    def design_of(trial: optuna.Trial) -> ArchConfig:
        values = {name: _suggest(trial, name, rng) for name, rng in box.items()}
        return ArchConfig.from_params(str(values.pop("family")), values)

    return _run(spec, n_trials, seed, sampler, design_of, {"source": f"baseline:{sampler}"})


def enumerate_box(family: str, box: dict[str, Range] | None = None) -> Iterator[ArchConfig]:
    """Every design of ``family`` in ``box`` (default: full registry range)."""
    box = box or full_box(family)
    fam = REGISTRY[family]
    names = [p.name for p in fam.params]
    axes = [fam.param(n).values(box[n]) for n in names]
    for combo in itertools.product(*axes):
        yield ArchConfig.from_params(family, dict(zip(names, combo)))


def box_size(family: str, box: dict[str, Range]) -> int:
    fam = REGISTRY[family]
    return math.prod(len(fam.param(n).values(box[n])) for n in box)
