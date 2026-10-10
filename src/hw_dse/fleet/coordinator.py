"""A fleet of structured graphs, orchestrated by code (milestone 4).

Milestone 3 tried an LLM as the outer loop (the Deep Agents campaign agent)
and it gained nothing: in 52 of 65 runs its plan came down to one call to
the structured graph, it cost 1.4-2.2x as much, and it looped. This module
tries the other way to scale out: **several structured graphs at once, with
deterministic code deciding everything between them.**

What the coordinator does (all code)
------------------------------------
1. **Assign.** Each member is an ordinary structured graph
   (:func:`hw_dse.agent.graph.build_graph`) restricted to some families of the
   registry. The default split is by contract class, ``fsm`` = {iterative,
   unrolled_k} and ``pipelined`` = {pipelined, pipelined_m}, the two shapes
   whose cost and timing differ most; :data:`SPLIT_BY_FAMILY` gives one
   member per family. Inside a member the LLM does exactly what it does in a
   single graph: picks families (now only its own) and ranges, reads
   summaries, takes one of the typed decisions. Code still clamps every
   range and enforces every stopping rule.
2. **Phase 1: split the budget equally.** ``phase1_frac`` (default 0.5) of
   the spec's ``total_evals``, shared equally; the members run **in
   parallel** (one thread each) and write every evaluation to the shared
   LangGraph Store (:mod:`hw_dse.fleet.store`).
3. **Lessons.** From the store, code computes per-family facts (evaluations,
   feasible designs, the best selection metric, designs on the merged front)
   and writes them back to the store's ``lessons`` namespace. No free text,
   nothing an LLM wrote.
4. **Phase 2: reallocate.** The rest of the budget goes to the members in
   proportion to their share of the *merged* Pareto front (a member whose
   families contribute nothing to it gets nothing). If nothing is feasible
   anywhere, the members share it equally, so infeasibility is still
   established with the whole budget. Each funded member runs again, with
   the lessons in its prompt (code-written facts, like the summaries).
5. **Merge and select.** The fleet's result is the union of every member's
   evaluations: one merged front, the spec's selection rule, then the same
   L2 step as a single graph (every L1-feasible design simulated for a system
   spec) and, if L2 rejects them all, the same L2 -> L1 feedback. The fleet
   never spends more than the spec's ``total_evals`` on L1, so it can be
   compared with a single graph at equal budget.

Member runs skip their own L2, L2-feedback and back-annotation steps (the
coordinator does them once, on the merged result), and each member keeps its
own run directory, trace and report.

Accounting: every Optuna trial is one evaluation (repeats included), exactly
as for a single graph and the baselines. The fleet's evaluations are ordered
round-robin across the members of a phase (they run concurrently), phase 1
before phase 2; that order only matters for "evaluations to 95% of the true
HV".
"""

from __future__ import annotations

import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from hw_dse.agent.graph import MIN_TRIALS_PER_FAMILY
from hw_dse.agent.summary import merged_front
from hw_dse.benchmark import select_design
from hw_dse.families import REGISTRY
from hw_dse.fleet import store as fstore
from hw_dse.spec import Budget, Spec

SPLIT_BY_CLASS: list[tuple[str, list[str]]] = [("fsm", ["iterative", "unrolled_k"]),
                                               ("pipelined", ["pipelined", "pipelined_m"])]
SPLIT_BY_FAMILY: list[tuple[str, list[str]]] = [(f, [f]) for f in REGISTRY]
MIN_MEMBER_BUDGET = 10  # the smallest Budget a member run accepts
MEMBER_OPTIONS = {"l2": {"enabled": False}, "l2_feedback": {"enabled": False}, "back_annotate": {"enabled": False}}

LLMFactory = Callable[[str, int], Any]
"""``factory(member_name, phase) -> StructuredLLM``: one fresh architect per member run."""


def member_spec(spec: Spec, budget: int) -> Spec:
    b = spec.budget
    return spec.model_copy(update={"budget": Budget(total_evals=budget, evals_per_round=min(b.evals_per_round, budget),
                                                    max_rounds=b.max_rounds, hv_epsilon=b.hv_epsilon)})


def split(total: int, weights: list[float]) -> list[int]:
    """Integer split of ``total`` in proportion to ``weights`` (largest remainders);
    shares below MIN_MEMBER_BUDGET are given to the others."""
    if not weights or sum(weights) <= 0:
        return [0] * len(weights)
    raw = [total * w / sum(weights) for w in weights]
    out = [int(x) for x in raw]
    for i in sorted(range(len(raw)), key=lambda i: raw[i] - out[i], reverse=True)[: total - sum(out)]:
        out[i] += 1
    small = [i for i, n in enumerate(out) if 0 < n < MIN_MEMBER_BUDGET]
    if small and len(small) < sum(1 for n in out if n > 0):
        freed = sum(out[i] for i in small)
        for i in small:
            out[i] = 0
        big = [i for i, n in enumerate(out) if n > 0]
        for j in range(freed):
            out[big[j % len(big)]] += 1
    return out


def interleave(lists: list[list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Round-robin merge (members of a phase run concurrently)."""
    out: list[dict[str, Any]] = []
    for i in range(max((len(x) for x in lists), default=0)):
        out += [x[i] for x in lists if i < len(x)]
    return out


def compute_lessons(records: list[dict[str, Any]], spec: Spec, members: list[tuple[str, list[str]]]) -> dict[str, Any]:
    """Per-family facts from the fleet's evaluations (all numbers computed by code)."""
    front = merged_front(records, spec)
    owner = {f: m for m, fams in members for f in fams}
    out: dict[str, Any] = {}
    for fam in REGISTRY:
        rows = [r for r in records if r["family"] == fam]
        if not rows:
            continue
        feas = [r for r in rows if r.get("feasible")]
        best = select_design(feas, spec)
        out[fam] = {"member": owner.get(fam), "evaluations": len(rows), "feasible": len(feas),
                    "best_" + spec.select_by: (float(best[spec.select_by]) if best else None),
                    "on_merged_front": sum(r["family"] == fam for r in front), "merged_front_size": len(front),
                    "provenance": "code: counted from the fleet's evaluated designs"}
    return out


def lessons_text(lessons: dict[str, Any], spec: Spec) -> str:
    """Code-templated text of the lessons for a member's prompt."""
    from hw_dse.evaluate import fmt_metric

    lines = []
    for fam, v in lessons.items():
        best = v["best_" + spec.select_by]
        lines.append(f"- {fam} (member {v['member']}): {v['evaluations']} evaluations, {v['feasible']} feasible; "
                     f"best feasible {spec.select_by} "
                     f"{fmt_metric(spec.select_by, best) if best is not None else 'none'}; "
                     f"{v['on_merged_front']} of the {v['merged_front_size']} designs on the merged front")
    return "\n".join(lines) or "none yet"


def run_fleet(spec: Spec, llm_factory: LLMFactory, seed: int = 0, members: list[tuple[str, list[str]]] | None = None,
              phase1_frac: float = 0.5, run_root: Path | None = None, parallel: bool = True,
              options: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run the fleet on ``spec``; returns the merged result in the shape of ``run_agent``'s."""
    from hw_dse.agent.runner import run_agent

    members = members or SPLIT_BY_CLASS
    store = fstore.new_store()
    total = spec.budget.total_evals
    t0 = time.time()
    runs: list[dict[str, Any]] = []

    def one(i: int, name: str, fams: list[str], budget: int, phase: int, lessons: str | None) -> dict[str, Any]:
        opts = {**MEMBER_OPTIONS, **(options or {}), "fleet": {"member": name, "families": fams, "lessons": lessons}}
        t = time.time()
        res = run_agent(member_spec(spec, budget), llm=llm_factory(name, phase), seed=seed * 1009 + 97 * phase + i,
                        run_root=(run_root / f"{name}-p{phase}") if run_root else None, options=opts, store=store)
        return {"member": name, "families": fams, "phase": phase, "budget": budget, "wall_s": round(time.time() - t, 1),
                **res}

    def phase(n: int, budgets: list[int], lessons: str | None) -> list[dict[str, Any]]:
        jobs = [(i, m, f, b) for i, ((m, f), b) in enumerate(zip(members, budgets)) if b >= MIN_MEMBER_BUDGET]
        if parallel and len(jobs) > 1:
            with ThreadPoolExecutor(max_workers=len(jobs)) as ex:
                futs = [ex.submit(one, i, m, f, b, n, lessons) for i, m, f, b in jobs]
                return [fu.result() for fu in futs]
        return [one(i, m, f, b, n, lessons) for i, m, f, b in jobs]

    p1_total = int(round(total * phase1_frac))
    p1 = phase(1, split(p1_total, [1.0] * len(members)), None)
    runs += p1
    recs1 = interleave([r["evaluations_ordered"] for r in p1])
    les = compute_lessons(recs1, spec, members)
    fstore.put_lessons(store, spec.name, les)
    remaining = total - len(recs1)
    front = merged_front(recs1, spec)
    weights = [float(sum(r["family"] in fams for r in front)) for _, fams in members]
    if sum(weights) == 0:  # nothing feasible yet: keep searching everywhere
        weights = [1.0] * len(members)
    p2_budgets = split(remaining, weights) if remaining >= MIN_MEMBER_BUDGET else [0] * len(members)
    p2 = phase(2, p2_budgets, lessons_text(les, spec)) if any(p2_budgets) else []
    runs += p2
    recs = recs1 + interleave([r["evaluations_ordered"] for r in p2])
    assert len(recs) <= total, (len(recs), total)
    front = merged_front(recs, spec)
    selected = select_design(front, spec)
    out: dict[str, Any] = {"selected_l1": selected, "l2": None, "l2_feedback": None, "l2_feedback_evaluations": []}
    status = "stopped" if selected else "no_feasible"
    if spec.system is not None and selected is not None:
        from hw_dse.l2.feedback import feedback, fires
        from hw_dse.l2.node import l2_select

        l2 = l2_select(recs, selected, spec)
        selected = l2.pop("selected")
        out["l2"] = l2
        if selected is None:
            status = "l2_no_feasible"
            if fires(l2) and ((options or {}).get("l2_feedback") or {}).get("enabled", True):
                fb = feedback(spec, recs, seed=seed)
                out["l2_feedback_evaluations"] = fb.pop("evaluations")
                out["l2_feedback"] = fb
                if fb["selected"] is not None:
                    selected, status = fb["selected"], "l2_feedback_recovered"
    last = {r["member"]: r for r in runs}  # each member's latest run
    declared = selected is None and bool(last) and all(r["llm_declared_infeasible"] for r in last.values())
    if declared:
        status = "infeasible"
    totals = {k: sum(float(r["llm"].get(k) or 0) for r in runs) for k in ("calls", "failures", "input_tokens",
                                                                         "output_tokens", "cost_usd")}
    counts = fstore.evaluation_counts(store, spec.name)
    out.update({
        "status": status, "selected": selected, "evaluations_ordered": recs, "llm_declared_infeasible": declared,
        "llm": totals, "models_served": sorted({m for r in runs for m in r["models_served"]}),
        "wall_s": round(time.time() - t0, 1), "members": [
            {k: r[k] for k in ("member", "families", "phase", "budget", "status", "rounds", "decisions",
                               "coverage_rounds", "wall_s", "run_dir", "llm_declared_infeasible")}
            | {"n_evals": len(r["evaluations_ordered"]), "cost_usd": r["llm"]["cost_usd"]} for r in runs],
        "phase2_budgets": dict(zip([m for m, _ in members], p2_budgets)),
        "lessons": les, "store_evaluations_by_member": counts,
        "store_distinct_designs": len(fstore.evaluated(store, spec.name)),
        "decisions": [d for r in runs for d in r["decisions"]],
    })
    assert sum(counts.values()) == len(recs), (counts, len(recs))  # the store saw every evaluation
    return out
