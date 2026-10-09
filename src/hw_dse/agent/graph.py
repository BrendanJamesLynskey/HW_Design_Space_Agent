"""The LangGraph agent: spec in, Pareto front and a chosen design out.

The graph, node by node::

    START -> intake -> confirm_spec -> propose --Send--> explore_family (x F, parallel)
                         |                                    |
                         | (rejected)                         v
                         v                  +----------- analyse <---+
                       report <-- select <--+  (stop)        |       |
                         ^                  |                +-Send--+ (refine/widen/add_family)
                         +------------------+ (infeasible / nothing feasible)

``intake``
    YAML text that validates as a :class:`~hw_dse.spec.Spec` is loaded
    directly (no LLM needed); anything else goes to the LLM with the
    :class:`~hw_dse.agent.schemas.SpecDraft` schema and is converted to a
    ``Spec`` in code.
``confirm_spec``
    ``interrupt()``: the human sees the validated spec and approves, edits
    or rejects it. ``auto_approve`` (config) skips this for CI and batch
    runs. Nothing is explored before a human (or the flag) says yes.
``propose``
    The LLM returns an :class:`~hw_dse.agent.schemas.ExplorationPlan`.
    Code clamps every range against the registry and splits the round's
    budget between families.
``explore_family``
    One per family, fanned out with ``Send``: an Optuna NSGA-II study
    inside that family's box with that family's share of the budget. Each
    returns its evaluations, which a reducer (``operator.add``) appends to
    ``state["evaluations"]``, so parallel branches never overwrite each
    other.
``analyse``
    Code merges everything: feasibility, Pareto front, hypervolume, HV
    gain. The LLM reads a compact summary (never raw rows) and returns an
    :class:`~hw_dse.agent.schemas.AnalysisDecision`. Code then applies the
    hard rules, which the LLM cannot override: the round cap, the budget,
    the HV-gain stopping rule (gain < epsilon over a round), "infeasible"
    is rejected if feasible designs exist, and a missing next plan gets a
    deterministic fallback. Every override is logged with the reason.
``select``
    ``interrupt()``: the human picks a design off the front by index, or
    ``auto_select`` applies the spec's selection rule.
``l2_simulate`` (milestone 3)
    L2: the front's top-k designs (by the selection rule) are simulated in
    the spec's system scenario (SimPy); system constraints are re-checked on
    simulated numbers and the best passing design becomes the selection.
    For a spec without a system scenario it only attaches L2 facts to the
    report (milestone-2 behaviour is unchanged).
``back_annotate``
    L5: measured data vs estimates for the selected design; flags a winner
    change.
``l5_reexplore`` (milestone 3)
    Runs only when ``back_annotate`` flags a winner change: one code-driven
    NSGA-II round around the measured front designs under the refitted
    calibration, kept apart from the L1 evaluations and budget, and a
    re-selection under that calibration (``l5_selected``).
``report``
    Writes ``runs/<spec>/<timestamp>/``: ``report.md``, ``pareto.png``,
    ``evaluations.csv`` (the LLM trace is already being written there).

State is checkpointed after every step with whichever checkpointer the
caller passes (the CLI uses ``SqliteSaver``), so a run interrupted for
human input, or killed, resumes from the last completed step.

The LLM and the tracer are captured in closures rather than stored in
state: state must be serialisable for the checkpointer, and an LLM client
object (which holds an API key) must never be written to disk.
"""

from __future__ import annotations

import math
import operator
from typing import Annotated, Any, TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send, interrupt

from hw_dse.agent import prompts
from hw_dse.agent.llm import StructuredLLM, StructuredOutputError
from hw_dse.agent.schemas import AnalysisDecision, ExplorationPlan, FamilyPlan, ParamRange, SpecDraft
from hw_dse.agent.summary import merged_front, spec_context, summarise
from hw_dse.benchmark import select_design
from hw_dse.evaluate import objective_vector, reference_point
from hw_dse.explore import run_family_study
from hw_dse.families import REGISTRY, clamp_ranges
from hw_dse.pareto import hypervolume
from hw_dse.spec import Budget, Constraint, Objective, Spec, try_parse_spec_text

CONTINUE = ("refine", "widen", "add_family", "map_front")
MIN_TRIALS_PER_FAMILY = 5

# ---------------------------------------------------------------------------
# Whole-curve levers (milestone 2)
# ---------------------------------------------------------------------------
# Milestone 1's agent was a good *selector* but a poor *front-mapper*: it
# dived at the corner the selection rule cares about and the 1% HV-gain rule
# then ended the run with a narrow front. The levers below are deterministic
# code; the LLM can only *choose* one of them (the ``map_front`` decision).
#
# coverage_reserve
#     Fraction of the evaluation budget the LLM's own rounds may not spend
#     (once a feasible design exists, and until a front-mapping round has
#     run). Whenever the run would stop (LLM ``stop``, the HV-gain rule, the
#     round cap or the LLM's share of the budget running out) with feasible
#     designs and budget left, code first spends what is left on one final
#     front-mapping round, then stops without another LLM call. 0 disables
#     it (milestone-1 behaviour).
# coverage_box
#     The search box of a front-mapping round, per family on the merged
#     front: ``"full"`` = the registry's full ranges; ``"front_anchored"`` =
#     full ranges, except that data_width and n_iter start just below the
#     smallest values on the front, by ``anchor_slack`` = (W steps, N steps)
#     (much smaller ones cannot meet the accuracy the front designs meet).
# warm_start, warm_start_max
#     Seed each front-mapping study with (up to warm_start_max of, spread
#     along) the family's current front designs -- already evaluated, so
#     free -- so NSGA-II breeds from the known front.
# hv_epsilon
#     Override for the spec's HV-gain stopping threshold (None = the spec's).
#
# The values in LEVERS_M2 were chosen offline by replaying the recorded
# milestone-1 LLM decisions against the exhaustive ground truth
# (eval/tune_levers.py; eval/data/levers_offline*.json). Replaying the 12
# recorded runs per spec, reserve 0.40 + front-anchored box lifted mean HV
# from 0.43 to 0.90 (dds_250msps) and 0.20 to 0.90 (low_area_control), with
# selection regret no worse; warm starts and the full box mapped less, and
# reserve 0.50 left the LLM too little budget. The reserve only applies once
# a feasible design exists, so infeasibility is still established with the
# whole budget.
LEVERS_M1: dict[str, Any] = {"coverage_reserve": 0.0, "coverage_box": "full", "warm_start": False, "hv_epsilon": None}
LEVERS_M2: dict[str, Any] = {"coverage_reserve": 0.40, "coverage_box": "front_anchored", "warm_start": False,
                             "hv_epsilon": None}
# Milestone 3 adds one lever, the fix for M2's front-mapping blind spot:
#
# map_unfeasible_families
#     A front-mapping round maps only the families *on* the front. In M2 a
#     family whose first box was too narrow to reach the accuracy target
#     (Qwen, high_precision seed: pipelined_m at W = 20-24) found nothing
#     feasible, never appeared on the front, and was never revisited, though
#     it held the true winner. With this lever, every family that was
#     explored but has no feasible design gets a full-box share of the
#     mapping budget (the average front family's share, over its full
#     registry ranges). Value ``True`` maps every such family; ``"reachable"``
#     (the M3 default) only those for which each constraint was met by at
#     least one of their designs, i.e. the box, not the family's structure,
#     kept them infeasible (an FSM family that never reached a 250 MSPS floor
#     is not worth mapping). Offline, over the 60 recorded M2 decisions, the
#     unconditional version cut high_precision regret but cost dds_250msps
#     hypervolume; the gate keeps the first and avoids the second (README).
#
# LEVERS_M3 is the default for specs with a system scenario (new in M3).
# Specs without one keep LEVERS_M2, so the inner graph behaves exactly as in
# M2 there (tests/test_m2_replay.py replays the committed M2 traces); the
# effect of the fix on the M2 specs is measured offline by replaying the
# same traces with it on (eval/m3_offline.py, eval/data/m3_mapfront_fix.json).
LEVERS_M3: dict[str, Any] = {**LEVERS_M2, "map_unfeasible_families": "reachable"}


def default_levers(spec: Spec) -> dict[str, Any]:
    """LEVERS_M3 for a spec with a system scenario, LEVERS_M2 otherwise."""
    return dict(LEVERS_M3 if spec.system is not None else LEVERS_M2)


class DSEState(TypedDict, total=False):
    spec_text: str
    spec: dict[str, Any]
    intake_mode: str
    run_dir: str
    seed: int
    status: str
    plan: dict[str, Any]
    round: int
    budget_used: int
    evaluations: Annotated[list[dict[str, Any]], operator.add]
    rounds_log: Annotated[list[dict[str, Any]], operator.add]
    hv_history: list[float]
    llm_declared_infeasible: bool
    selected: dict[str, Any] | None
    selection_mode: str
    report_path: str
    levers: dict[str, Any]
    coverage_rounds: int
    pending_stop: dict[str, Any] | None
    back_annotation: dict[str, Any] | None
    selected_l1: dict[str, Any] | None
    l2: dict[str, Any] | None
    l5: dict[str, Any] | None
    l5_evaluations: list[dict[str, Any]]
    l5_selected: dict[str, Any] | None


def _cfg(config: RunnableConfig | None, key: str, default: Any = None) -> Any:
    return ((config or {}).get("configurable") or {}).get(key, default)


# ---------------------------------------------------------------------------
# Spec intake helpers
# ---------------------------------------------------------------------------

def draft_to_spec(d: SpecDraft) -> Spec:
    """Deterministic conversion of an LLM spec draft into a full Spec."""
    cons: list[Constraint] = []
    if d.min_throughput_msps:
        cons.append(Constraint(metric="throughput_msps", op=">=", value=d.min_throughput_msps))
    if d.max_abs_err:
        cons.append(Constraint(metric="max_abs_err", op="<=", value=d.max_abs_err))
    if d.max_luts:
        cons.append(Constraint(metric="luts", op="<=", value=d.max_luts))
    if d.max_latency_ns:
        cons.append(Constraint(metric="latency_ns", op="<=", value=d.max_latency_ns))
    refs = {"luts": 6000, "ffs": 6000, "luts_plus_ffs": 12000, "power_index": 50, "latency_ns": 2000}
    minimise = list(dict.fromkeys(d.minimise or ["luts"]))[:2]
    objs = [Objective(metric=m, direction="min", ref=refs[m]) for m in minimise]
    if len(objs) == 1:
        # A one-objective front is a single point; add accuracy as the trade-off axis.
        err = d.max_abs_err or 2.0**-8
        objs.append(Objective(metric="accuracy_bits", direction="max", ref=-math.log2(err)))
    name = "".join(ch if ch.isalnum() else "_" for ch in d.name.lower()).strip("_") or "nl_spec"
    return Spec(name=name, description=d.description, constraints=cons, objectives=objs,
                select_by=objs[0].metric, select_direction="min", budget=Budget())


# ---------------------------------------------------------------------------
# Plan validation: LLM plan -> clamped, budgeted jobs
# ---------------------------------------------------------------------------

def _ranges_to_dict(family: str, ranges: list[ParamRange]) -> dict[str, object]:
    """ParamRange list -> {param: [lo, hi] | [choices]} using the registry's
    parameter kinds (models sometimes fill both ``choices`` and bounds)."""
    kinds = {p.name: p.kind for p in REGISTRY[family].params}
    out: dict[str, object] = {}
    for r in ranges:
        kind = kinds.get(r.param)
        if kind == "cat":
            if r.choices:
                out[r.param] = list(r.choices)
        elif r.low is not None or r.high is not None:
            lo = r.low if r.low is not None else r.high
            hi = r.high if r.high is not None else r.low
            out[r.param] = [lo, hi]
        elif kind is None:
            out[r.param] = r.choices or []  # unknown param: let clamp_ranges report it
    return out


def validate_plan(plan: ExplorationPlan, round_budget: int) -> dict[str, Any]:
    """Clamp ranges, dedupe families, split the round budget. Pure code."""
    notes: list[str] = []
    fams: list[FamilyPlan] = []
    seen: set[str] = set()
    for fp in plan.families:
        if fp.family in seen:
            notes.append(f"dropped duplicate family {fp.family}")
            continue
        seen.add(fp.family)
        fams.append(fp)
    max_fams = max(1, round_budget // MIN_TRIALS_PER_FAMILY)
    if len(fams) > max_fams:
        notes.append(f"budget {round_budget} supports {max_fams} families; dropped {[f.family for f in fams[max_fams:]]}")
        fams = fams[:max_fams]
    shares = [f.budget_share if f.budget_share > 0 else 0.0 for f in fams]
    if sum(shares) <= 0:
        shares = [1.0] * len(fams)
        notes.append("budget shares were all zero; split equally")
    total_share = sum(shares)
    raw = [round_budget * sh / total_share for sh in shares]
    trials = [max(MIN_TRIALS_PER_FAMILY, int(math.floor(x))) for x in raw]
    while sum(trials) > round_budget:  # min-per-family may overshoot: trim the largest
        trials[trials.index(max(trials))] -= 1
    i = 0
    while sum(trials) < round_budget:  # hand out the rounding remainder
        trials[i % len(trials)] += 1
        i += 1
    jobs = []
    for fp, n in zip(fams, trials):
        clamped = clamp_ranges(fp.family, _ranges_to_dict(fp.family, fp.ranges))
        notes.extend(clamped.notes)
        jobs.append({"family": fp.family, "box": {k: list(v) for k, v in clamped.ranges.items()}, "n_trials": n, "why": fp.why})
    return {"jobs": jobs, "rationale": plan.rationale, "notes": notes}


def fallback_plan(decision: str, spec: Spec, records: list[dict[str, Any]], plan: dict[str, Any]) -> ExplorationPlan:
    """Deterministic next plan when the LLM asked to continue but gave none."""
    explored = [j["family"] for j in plan.get("jobs", [])]
    if decision == "add_family":
        new = [f for f in REGISTRY if f not in explored][:1] or explored[:1]
        return ExplorationPlan(families=[FamilyPlan(family=f, why="fallback: add unexplored family") for f in new],  # type: ignore[arg-type]
                               rationale="fallback plan (LLM gave none)")
    if decision == "refine":
        from hw_dse.agent.summary import front_boxes

        boxes = front_boxes(merged_front(records, spec))
        if boxes:
            return ExplorationPlan(
                families=[FamilyPlan(family=f, ranges=[ParamRange(**r) for r in rs], why="fallback: box around front")  # type: ignore[arg-type]
                          for f, rs in list(boxes.items())[:4]],
                rationale="fallback plan (LLM gave none)")
    return ExplorationPlan(families=[FamilyPlan(family=f, why="fallback: full range") for f in (explored or list(REGISTRY))[:4]],  # type: ignore[arg-type]
                           rationale="fallback plan (LLM gave none)")


def _hv(records: list[dict[str, Any]], spec: Spec) -> float:
    front = merged_front(records, spec)
    if not front:
        return 0.0
    return hypervolume([objective_vector(r, spec) for r in front], reference_point(spec))


def _llm_budget(total: int, levers: dict[str, Any]) -> int:
    """Evaluations the LLM's own rounds may spend before a front-mapping round."""
    return total - int(round(total * float(levers.get("coverage_reserve") or 0.0)))


def coverage_plan(spec: Spec, records: list[dict[str, Any]], budget: int, levers: dict[str, Any]) -> dict[str, Any] | None:
    """A deterministic front-mapping round (the ``map_front`` lever).

    One NSGA-II study per family on the merged feasible front, over that
    family's full registry ranges (or the front-anchored box), budget split
    in proportion to each family's share of the front, optionally seeded
    with the family's front designs. Returns ``None`` if nothing is feasible.
    """
    from hw_dse.families import full_box

    front = merged_front(records, spec)
    if not front or budget < MIN_TRIALS_PER_FAMILY:
        return None
    fams = list(dict.fromkeys(r["family"] for r in front))
    counts = [float(sum(r["family"] == f for r in front)) for f in fams]
    unfeasible: list[str] = []
    if levers.get("map_unfeasible_families"):
        # M3 fix: families explored but with no feasible design get a full-box
        # share (the average front family's) so a too-narrow first box is not
        # the end of a family.
        feas_fams = {r["family"] for r in records if r.get("feasible")}
        unfeasible = [f for f in REGISTRY if f in {r["family"] for r in records} and f not in feas_fams]
        if levers.get("map_unfeasible_families") == "reachable":
            # Only families for which every constraint was met by at least one
            # design (not necessarily the same one): the box, not the family's
            # structure, is what kept them infeasible. Accuracy depends only on
            # the numeric knobs every family shares, so an accuracy constraint
            # counts as met if *any* design met it; a structural one
            # (throughput, latency, system timing) must be met by one of the
            # family's own designs. An FSM family that never reached a
            # 250 MSPS floor is left alone.
            numeric_only = {"max_abs_err", "rms_err", "accuracy_bits", "sys_sfdr_dbc", "sys_snr_db"}

            def met(c: Constraint, rows: list[dict[str, Any]]) -> bool:
                return any(r["violations"].get(str(c), 1.0) <= 0 for r in rows)

            def reachable(fam: str) -> bool:
                mine = [r for r in records if r["family"] == fam]
                return all(met(c, records if c.metric in numeric_only else mine) for c in spec.constraints)

            unfeasible = [f for f in unfeasible if reachable(f)]
        avg = sum(counts) / len(counts)
        fams += unfeasible
        counts += [avg] * len(unfeasible)
    max_fams = max(1, budget // MIN_TRIALS_PER_FAMILY)
    fams, counts = fams[:max_fams], counts[:max_fams]
    trials = [max(MIN_TRIALS_PER_FAMILY, int(budget * c / sum(counts))) for c in counts]
    while sum(trials) > budget:
        trials[trials.index(max(trials))] -= 1
    i = 0
    while sum(trials) < budget:
        trials[i % len(trials)] += 1
        i += 1
    jobs = []
    for fam, n in zip(fams, trials):
        box = {k: list(v) for k, v in full_box(fam).items()}
        rows = [r for r in front if r["family"] == fam]
        if fam in unfeasible:
            jobs.append({"family": fam, "box": box, "n_trials": n, "seeds": [],
                         "why": f"code: {fam} was explored but found nothing feasible; full-box share (M3 lever)"})
            continue
        if levers.get("coverage_box") == "front_anchored":
            w_slack, n_slack = levers.get("anchor_slack") or (1, 2)
            for prm, slack in (("data_width", int(w_slack)), ("n_iter", int(n_slack))):
                lo, hi = box[prm]
                box[prm] = [max(lo, min(int(r[prm]) for r in rows) - slack), hi]
        seeds = []
        if levers.get("warm_start"):
            names = [pp.name for pp in REGISTRY[fam].params]
            seeds = [{nm: r[nm] for nm in names} for r in rows]
            cap = levers.get("warm_start_max")
            if cap and len(seeds) > cap:  # an even spread along the front, ends included
                pick = sorted({round(i * (len(seeds) - 1) / (cap - 1)) for i in range(cap)}) if cap > 1 else [0]
                seeds = [seeds[i] for i in pick]
        jobs.append({"family": fam, "box": box, "n_trials": n, "seeds": seeds,
                     "why": f"code: map the front of {fam} ({len(rows)} front designs"
                            f"{', seeded with them' if seeds else ''}; box {levers.get('coverage_box')})"})
    return {"jobs": jobs, "kind": "coverage", "notes": [],
            "rationale": "code-driven front-mapping round: NSGA-II over the front families' "
                         f"{levers.get('coverage_box')} ranges with {budget} evaluations"}


def order_evaluations(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Canonical evaluation order: by round, then trial index across the
    parallel family studies (round-robin), modelling concurrent execution."""
    fam_idx = {f: i for i, f in enumerate(REGISTRY)}
    return sorted(records, key=lambda r: (r.get("round", 0), r.get("trial", 0), fam_idx.get(r["family"], 9)))


# ---------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------

def build_graph(llm: StructuredLLM, checkpointer: Any = None) -> Any:
    """Compile the DSE graph around one LLM. ``checkpointer`` may be None."""

    def intake(state: DSEState) -> dict[str, Any]:
        if state.get("spec"):
            return {"intake_mode": state.get("intake_mode") or "provided as a validated Spec"}
        text = state.get("spec_text", "")
        spec = try_parse_spec_text(text)
        if spec is not None:
            return {"spec": spec.model_dump(), "intake_mode": "yaml"}
        draft = llm.structured(SpecDraft, prompts.SYSTEM, prompts.INTAKE.format(text=text), node="intake")
        return {"spec": draft_to_spec(draft).model_dump(), "intake_mode": "llm"}

    def confirm_spec(state: DSEState, config: RunnableConfig) -> dict[str, Any]:
        spec = Spec.model_validate(state["spec"])
        if _cfg(config, "auto_approve", False):
            return {"status": "running"}
        answer = interrupt({"type": "confirm_spec", "summary": spec.summary(), "spec": state["spec"]})
        if isinstance(answer, dict) and answer.get("approve") is False:
            return {"status": "rejected"}
        if isinstance(answer, dict) and answer.get("spec"):
            return {"spec": Spec.model_validate(answer["spec"]).model_dump(), "status": "running"}
        return {"status": "running"}

    def route_after_confirm(state: DSEState) -> str:
        return "report" if state.get("status") == "rejected" else "propose"

    def propose(state: DSEState, config: RunnableConfig) -> dict[str, Any]:
        spec = Spec.model_validate(state["spec"])
        levers = {**default_levers(spec), **(_cfg(config, "levers") or {})}
        b = spec.budget
        user = prompts.PROPOSE.format(spec=spec.summary(), budget=b.total_evals, per_round=b.evals_per_round, max_rounds=b.max_rounds)
        notes = _cfg(config, "architect_notes")
        if notes:  # milestone 3: advisory text from the campaign agent (never numbers it produced)
            user += prompts.CAMPAIGN_NOTES.format(notes=str(notes)[:2000])
        failure = None
        try:
            plan = llm.structured(ExplorationPlan, prompts.system_prompt(spec), user, node="propose", context=spec_context(spec))
        except StructuredOutputError as exc:
            failure = f"LLM produced no valid plan ({str(exc)[:200]}); used deterministic fallback: every family, full range"
            plan = fallback_plan("widen", spec, [], {})
        vp = validate_plan(plan, min(b.evals_per_round, _llm_budget(b.total_evals, levers)))
        if failure:
            vp["notes"].insert(0, failure)
        return {"plan": vp, "round": 0, "budget_used": 0, "hv_history": [], "llm_declared_infeasible": False,
                "levers": levers, "coverage_rounds": 0, "pending_stop": None}

    def fan_out(state: DSEState) -> list[Send]:
        rnd = state.get("round", 0) + 1
        seed = int(state.get("seed", 0))
        return [
            Send("explore_family", {"spec": state["spec"], "job": job, "round": rnd,
                                    "seed": seed * 10007 + rnd * 101 + i})
            for i, job in enumerate(state["plan"]["jobs"])
        ]

    def explore_family(payload: dict[str, Any]) -> dict[str, Any]:
        spec = Spec.model_validate(payload["spec"])
        job = payload["job"]
        box = {k: tuple(v) for k, v in job["box"].items()}
        recs = run_family_study(job["family"], box, spec, job["n_trials"], payload["seed"], tag={"round": payload["round"]},
                                seed_designs=job.get("seeds") or None)
        return {"evaluations": recs}

    def analyse(state: DSEState) -> dict[str, Any]:
        spec = Spec.model_validate(state["spec"])
        b = spec.budget
        # Checkpoints from before milestone 2 carry no levers: behave as M1 did.
        levers = {**LEVERS_M1, **(state.get("levers") or {})}
        eps = b.hv_epsilon if levers.get("hv_epsilon") is None else float(levers["hv_epsilon"])
        rnd = state.get("round", 0) + 1
        records = state.get("evaluations", [])
        used = len(records)
        hv_hist = list(state.get("hv_history", []))
        hv = _hv(records, spec)
        hv_prev = hv_hist[-1] if hv_hist else None
        remaining = b.total_evals - used
        cov_rounds = int(state.get("coverage_rounds", 0))
        # The LLM's own rounds may not touch the coverage reserve until a
        # front-mapping round has run -- but only once there is a front to
        # map: while nothing is feasible (e.g. an infeasible spec), the LLM
        # keeps the whole budget to establish that.
        any_feasible = any(r.get("feasible") for r in records)
        llm_remaining = (_llm_budget(b.total_evals, levers) - used) if (cov_rounds == 0 and any_feasible) else remaining
        final = rnd >= b.max_rounds or llm_remaining < MIN_TRIALS_PER_FAMILY
        explored = sorted({r["family"] for r in records}, key=list(REGISTRY).index)
        summary, ctx = summarise(spec, records, round_no=rnd, max_rounds=b.max_rounds, budget_used=used, hv=hv,
                                 hv_prev=hv_prev, explored=explored, final_round=final)
        n_feas = int(ctx["n_feasible"])
        gain = ctx["hv_gain"]
        overrides: list[str] = []
        update: dict[str, Any] = {"round": rnd, "budget_used": used, "hv_history": hv_hist + [hv], "pending_stop": None}

        pending = state.get("pending_stop")
        if pending:
            # The round that just ran was the code's front-mapping round,
            # inserted after the architect (or a hard rule) had already
            # decided to stop. Stop now, without asking the LLM again.
            dec = AnalysisDecision(decision="stop", rationale=pending["rationale"])
            llm_decision = None
            decision = "stop"
            update["status"] = pending["status"]
            overrides.append("code: front-mapping round complete; stopping as decided before it")
        else:
            user = prompts.ANALYSE.format(spec=spec.summary(), summary=summary, final_note=prompts.FINAL_NOTE if final else "")
            try:
                dec = llm.structured(AnalysisDecision, prompts.system_prompt(spec), user, node="analyse", context=ctx)
            except StructuredOutputError as exc:
                dec = AnalysisDecision(decision="stop", rationale=f"[LLM failed to answer: {exc}]")
                overrides.append("LLM produced no valid decision; treated as stop")
            llm_decision = dec.decision
            decision = llm_decision

            # -- hard rules (code, not LLM) -----------------------------
            if decision == "infeasible" and n_feas > 0:
                overrides.append(f"'infeasible' rejected: {n_feas} feasible designs exist; treated as stop")
                decision = "stop"
            if decision in CONTINUE and final:
                why = "round cap" if rnd >= b.max_rounds else "budget exhausted"
                overrides.append(f"'{decision}' overridden to stop: {why}")
                decision = "stop"
            if (decision in CONTINUE and decision != "map_front" and hv_prev is not None and hv_prev > 0
                    and gain is not None and gain < eps):
                overrides.append(f"'{decision}' overridden to stop: HV gain {gain * 100:.2f}% < epsilon {eps * 100:.2f}%")
                decision = "stop"

            if decision == "infeasible":
                update["status"] = "infeasible"
                update["llm_declared_infeasible"] = True
            elif decision == "stop":
                if n_feas == 0:
                    status = "no_feasible"
                    overrides.append("no feasible design found and the architect did not declare infeasibility")
                elif rnd >= b.max_rounds and llm_decision in CONTINUE:
                    status = "round_cap"
                elif llm_remaining < MIN_TRIALS_PER_FAMILY and llm_decision in CONTINUE:
                    status = "budget"
                elif any("HV gain" in o for o in overrides):
                    status = "converged"
                else:
                    status = "stopped"
                update["status"] = status
                # Lever: never stop with budget left while there is a front to
                # map (also after an LLM-chosen map_front round; the pending
                # branch above ends the run after the code's own final round).
                if (n_feas > 0 and levers.get("coverage_reserve", 0) > 0
                        and remaining >= MIN_TRIALS_PER_FAMILY):
                    cov = coverage_plan(spec, records, remaining, levers)
                    if cov is not None:
                        overrides.append(f"code: before stopping ({status}), one front-mapping round with the "
                                         f"remaining {remaining} evaluations")
                        update.update(plan=cov, status="running", coverage_rounds=cov_rounds + 1,
                                      pending_stop={"status": status, "rationale": dec.rationale})
            elif decision == "map_front":
                cov = coverage_plan(spec, records, min(b.evals_per_round, llm_remaining), levers)
                if cov is None:
                    overrides.append("'map_front' with no feasible design to map: used the widen fallback instead")
                    update["plan"] = validate_plan(fallback_plan("widen", spec, records, state.get("plan", {})),
                                                   min(b.evals_per_round, llm_remaining))
                else:
                    update["plan"] = cov
                    update["coverage_rounds"] = cov_rounds + 1
                update["status"] = "running"
            else:
                plan = dec.next_plan
                if plan is None:
                    plan = fallback_plan(decision, spec, records, state.get("plan", {}))
                    overrides.append(f"no next_plan given for '{decision}'; used deterministic fallback")
                update["plan"] = validate_plan(plan, min(b.evals_per_round, llm_remaining))
                update["status"] = "running"
        update["rounds_log"] = [{
            "round": rnd,
            "plan": state.get("plan", {}),
            "evals_this_round": sum(1 for r in records if r.get("round") == rnd),
            "budget_used": used,
            "n_feasible": n_feas,
            "hv": hv,
            "hv_gain": gain,
            "summary": summary,
            "llm_decision": llm_decision,
            "decision": decision,
            "rationale": dec.rationale,
            "next_plan": update.get("plan"),
            "overrides": overrides,
        }]
        return update

    def route_after_analyse(state: DSEState) -> list[Send] | str:
        status = state.get("status")
        if status == "running":
            return fan_out(state)
        if status in ("infeasible", "no_feasible"):
            return "report"
        return "select"

    def select(state: DSEState, config: RunnableConfig) -> dict[str, Any]:
        spec = Spec.model_validate(state["spec"])
        front = merged_front(state.get("evaluations", []), spec)
        auto = select_design(front, spec)
        if _cfg(config, "auto_select", False) or not front:
            return {"selected": auto, "selection_mode": "auto (spec rule: "
                    f"{spec.select_direction} {spec.select_by})"}
        rows = [{"index": i, "key": r["key"], **{o.metric: r[o.metric] for o in spec.objectives}} for i, r in enumerate(front)]
        answer = interrupt({"type": "select", "front": rows, "auto_choice": front.index(auto) if auto in front else 0})
        choice = answer.get("choice", "auto") if isinstance(answer, dict) else answer
        if choice == "auto" or choice is None:
            return {"selected": auto, "selection_mode": "auto (human deferred to spec rule)"}
        idx = int(choice)
        if not 0 <= idx < len(front):
            return {"selected": auto, "selection_mode": f"auto (invalid human choice {choice!r})"}
        return {"selected": front[idx], "selection_mode": f"human picked front index {idx}"}

    def l2_simulate(state: DSEState, config: RunnableConfig) -> dict[str, Any]:
        from hw_dse.l2.node import DEFAULT_K, l2_select

        spec = Spec.model_validate(state["spec"])
        opts = _cfg(config, "l2") or {}
        selected = state.get("selected")
        if opts.get("enabled") is False:
            return {"l2": {"status": "skipped", "reason": "disabled"}, "selected_l1": selected}
        out = l2_select(state.get("evaluations", []), selected, spec, k=int(opts.get("k", DEFAULT_K)))
        new_sel = out.pop("selected")
        upd: dict[str, Any] = {"l2": out, "selected_l1": selected}
        if spec.system is not None:
            upd["selected"] = new_sel
            if new_sel is None:
                upd["status"] = "l2_no_feasible"
        return upd

    def back_annotate(state: DSEState, config: RunnableConfig) -> dict[str, Any]:
        from hw_dse.agent.backannotate import back_annotate as annotate

        spec = Spec.model_validate(state["spec"])
        front = merged_front(state.get("evaluations", []), spec)
        try:
            ba = annotate(spec, front, state.get("selected"), _cfg(config, "back_annotate") or {})
        except Exception as exc:  # noqa: BLE001 - a broken CSV must not lose the run
            ba = {"status": "error", "notes": [f"back-annotation failed: {type(exc).__name__}: {exc}"],
                  "measured_sources": [], "comparisons": []}
        return {"back_annotation": ba}

    def route_after_back_annotate(state: DSEState, config: RunnableConfig) -> str:
        opts = _cfg(config, "back_annotate") or {}
        ba = state.get("back_annotation") or {}
        if ba.get("winner_changed") and opts.get("reexplore", True):
            return "l5_reexplore"
        return "report"

    def l5_reexplore(state: DSEState, config: RunnableConfig) -> dict[str, Any]:
        from hw_dse.agent.backannotate import reexplore

        spec = Spec.model_validate(state["spec"])
        front = merged_front(state.get("evaluations", []), spec)
        try:
            out = reexplore(spec, front, state.get("selected"), state.get("back_annotation") or {},
                            _cfg(config, "back_annotate") or {}, seed=int(state.get("seed", 0)))
        except Exception as exc:  # noqa: BLE001 - never lose the run to the optional L5 loop
            return {"l5": {"status": "error", "notes": [f"L5 re-exploration failed: {type(exc).__name__}: {exc}"]}}
        recs = out.pop("evaluations")
        return {"l5": out, "l5_evaluations": recs, "l5_selected": out.get("selected")}

    def report(state: DSEState) -> dict[str, Any]:
        from hw_dse.agent.report import write_report

        path = write_report(dict(state), llm)
        return {"report_path": str(path)}

    g = StateGraph(DSEState)
    g.add_node("intake", intake)
    g.add_node("confirm_spec", confirm_spec)
    g.add_node("propose", propose)
    g.add_node("explore_family", explore_family)
    g.add_node("analyse", analyse)
    g.add_node("select", select)
    g.add_node("l2_simulate", l2_simulate)
    g.add_node("back_annotate", back_annotate)
    g.add_node("l5_reexplore", l5_reexplore)
    g.add_node("report", report)
    g.add_edge(START, "intake")
    g.add_edge("intake", "confirm_spec")
    g.add_conditional_edges("confirm_spec", route_after_confirm, ["propose", "report"])
    g.add_conditional_edges("propose", fan_out, ["explore_family"])
    g.add_edge("explore_family", "analyse")
    g.add_conditional_edges("analyse", route_after_analyse, ["explore_family", "select", "report"])
    g.add_edge("select", "l2_simulate")
    g.add_edge("l2_simulate", "back_annotate")
    g.add_conditional_edges("back_annotate", route_after_back_annotate, ["l5_reexplore", "report"])
    g.add_edge("l5_reexplore", "report")
    g.add_edge("report", END)
    return g.compile(checkpointer=checkpointer)
