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

CONTINUE = ("refine", "widen", "add_family")
MIN_TRIALS_PER_FAMILY = 5


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

    def propose(state: DSEState) -> dict[str, Any]:
        spec = Spec.model_validate(state["spec"])
        b = spec.budget
        user = prompts.PROPOSE.format(spec=spec.summary(), budget=b.total_evals, per_round=b.evals_per_round, max_rounds=b.max_rounds)
        failure = None
        try:
            plan = llm.structured(ExplorationPlan, prompts.SYSTEM, user, node="propose", context=spec_context(spec))
        except StructuredOutputError as exc:
            failure = f"LLM produced no valid plan ({str(exc)[:200]}); used deterministic fallback: every family, full range"
            plan = fallback_plan("widen", spec, [], {})
        vp = validate_plan(plan, min(b.evals_per_round, b.total_evals))
        if failure:
            vp["notes"].insert(0, failure)
        return {"plan": vp, "round": 0, "budget_used": 0, "hv_history": [], "llm_declared_infeasible": False}

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
        recs = run_family_study(job["family"], box, spec, job["n_trials"], payload["seed"], tag={"round": payload["round"]})
        return {"evaluations": recs}

    def analyse(state: DSEState) -> dict[str, Any]:
        spec = Spec.model_validate(state["spec"])
        b = spec.budget
        rnd = state.get("round", 0) + 1
        records = state.get("evaluations", [])
        used = len(records)
        hv_hist = list(state.get("hv_history", []))
        hv = _hv(records, spec)
        hv_prev = hv_hist[-1] if hv_hist else None
        remaining = b.total_evals - used
        final = rnd >= b.max_rounds or remaining < MIN_TRIALS_PER_FAMILY
        explored = sorted({r["family"] for r in records}, key=list(REGISTRY).index)
        summary, ctx = summarise(spec, records, round_no=rnd, max_rounds=b.max_rounds, budget_used=used, hv=hv,
                                 hv_prev=hv_prev, explored=explored, final_round=final)
        user = prompts.ANALYSE.format(spec=spec.summary(), summary=summary, final_note=prompts.FINAL_NOTE if final else "")
        overrides: list[str] = []
        try:
            dec = llm.structured(AnalysisDecision, prompts.SYSTEM, user, node="analyse", context=ctx)
        except StructuredOutputError as exc:
            dec = AnalysisDecision(decision="stop", rationale=f"[LLM failed to answer: {exc}]")
            overrides.append("LLM produced no valid decision; treated as stop")
        llm_decision = dec.decision
        decision = llm_decision
        n_feas = int(ctx["n_feasible"])
        gain = ctx["hv_gain"]

        # -- hard rules (code, not LLM) ---------------------------------
        if decision == "infeasible" and n_feas > 0:
            overrides.append(f"'infeasible' rejected: {n_feas} feasible designs exist; treated as stop")
            decision = "stop"
        if decision in CONTINUE and final:
            why = "round cap" if rnd >= b.max_rounds else "budget exhausted"
            overrides.append(f"'{decision}' overridden to stop: {why}")
            decision = "stop"
        if decision in CONTINUE and hv_prev is not None and hv_prev > 0 and gain is not None and gain < b.hv_epsilon:
            overrides.append(f"'{decision}' overridden to stop: HV gain {gain * 100:.2f}% < epsilon {b.hv_epsilon * 100:.2f}%")
            decision = "stop"

        update: dict[str, Any] = {"round": rnd, "budget_used": used, "hv_history": hv_hist + [hv]}
        if decision == "infeasible":
            update["status"] = "infeasible"
            update["llm_declared_infeasible"] = True
        elif decision == "stop":
            if n_feas == 0:
                update["status"] = "no_feasible"
                overrides.append("no feasible design found and the architect did not declare infeasibility")
            elif rnd >= b.max_rounds and llm_decision in CONTINUE:
                update["status"] = "round_cap"
            elif remaining < MIN_TRIALS_PER_FAMILY and llm_decision in CONTINUE:
                update["status"] = "budget"
            elif any("HV gain" in o for o in overrides):
                update["status"] = "converged"
            else:
                update["status"] = "stopped"
        else:
            plan = dec.next_plan
            if plan is None:
                plan = fallback_plan(decision, spec, records, state.get("plan", {}))
                overrides.append(f"no next_plan given for '{decision}'; used deterministic fallback")
            update["plan"] = validate_plan(plan, min(b.evals_per_round, remaining))
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
    g.add_node("report", report)
    g.add_edge(START, "intake")
    g.add_edge("intake", "confirm_spec")
    g.add_conditional_edges("confirm_spec", route_after_confirm, ["propose", "report"])
    g.add_conditional_edges("propose", fan_out, ["explore_family"])
    g.add_edge("explore_family", "analyse")
    g.add_conditional_edges("analyse", route_after_analyse, ["explore_family", "select", "report"])
    g.add_edge("select", "report")
    g.add_edge("report", END)
    return g.compile(checkpointer=checkpointer)
