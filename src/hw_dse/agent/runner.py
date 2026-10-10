"""Run the agent end to end from Python (used by the CLI and the eval).

:func:`run_agent` wires the pieces together: a run directory, a tracer
writing ``llm_trace.jsonl`` into it, an LLM from the provider factory, a
SQLite checkpointer, and the compiled graph. With ``auto=True`` it passes
``auto_approve`` and ``auto_select`` so no human is needed (CI, eval);
otherwise the caller handles the interrupts (see :mod:`hw_dse.cli`).
"""

from __future__ import annotations

import sqlite3
import time
import uuid
from pathlib import Path
from typing import Any

from hw_dse.agent.graph import build_graph, order_evaluations
from hw_dse.agent.llm import StructuredLLM, make_llm
from hw_dse.agent.trace import Tracer
from hw_dse.spec import Spec

REPO_ROOT = Path(__file__).resolve().parents[3]


def new_run_dir(spec_name: str, root: Path | None = None) -> Path:
    stamp = time.strftime("%Y%m%d-%H%M%S") + f"-{uuid.uuid4().hex[:4]}"
    d = (root or REPO_ROOT / "runs") / spec_name / stamp
    d.mkdir(parents=True, exist_ok=True)
    return d


def sqlite_checkpointer(path: Path) -> Any:
    from langgraph.checkpoint.sqlite import SqliteSaver

    conn = sqlite3.connect(str(path), check_same_thread=False)
    return SqliteSaver(conn)


def run_agent(
    spec: Spec,
    provider: str | None = None,
    model: str | None = None,
    seed: int = 0,
    reasoning: str | None = None,
    run_root: Path | None = None,
    method: str | None = None,
    llm: StructuredLLM | None = None,
    levers: dict[str, Any] | None = None,
    options: dict[str, Any] | None = None,
    tracer: Tracer | None = None,
) -> dict[str, Any]:
    """Run one fully automatic agent session and return its results.

    ``levers`` overrides the whole-curve levers (default
    :func:`hw_dse.agent.graph.default_levers`: ``LEVERS_M2`` for a spec
    without a system scenario, ``LEVERS_M3`` with one; pass ``LEVERS_M1``
    for milestone-1 behaviour). ``options`` adds graph config (``l2``,
    ``back_annotate``, ``architect_notes``). ``tracer``: write the LLM trace
    there instead of a new ``llm_trace.jsonl`` in the run directory (the
    campaign agent keeps one trace for all its calls).
    """
    run_dir = new_run_dir(spec.name, run_root)
    tracer = tracer or Tracer(run_dir / "llm_trace.jsonl")
    if llm is None:
        llm = make_llm(provider, model, tracer=tracer, reasoning=reasoning, method=method)
    else:
        llm.tracer = tracer
    graph = build_graph(llm, sqlite_checkpointer(run_dir / "checkpoints.sqlite"))
    config = {"configurable": {"thread_id": f"{spec.name}-{seed}", "auto_approve": True, "auto_select": True,
                               "levers": levers or {}, **(options or {})},
              "recursion_limit": 100}
    state = graph.invoke({"spec": spec.model_dump(), "run_dir": str(run_dir), "seed": seed}, config)
    totals = tracer.totals()  # (a shared tracer: totals of everything it has seen)
    served = sorted({str(r.get("model_served")) for r in tracer.records if r.get("model_served")})
    return {
        "run_dir": str(run_dir),
        "status": state.get("status"),
        "rounds": state.get("round", 0),
        "selected": state.get("selected"),
        "evaluations_ordered": order_evaluations(state.get("evaluations", [])),
        "llm_declared_infeasible": bool(state.get("llm_declared_infeasible")),
        "decisions": [log["llm_decision"] for log in state.get("rounds_log", []) if log.get("llm_decision")],
        "coverage_rounds": int(state.get("coverage_rounds") or 0),
        "overrides": [o for log in state.get("rounds_log", []) for o in log.get("overrides", [])],
        "llm": totals,
        "models_served": served,
        "structured_method": getattr(llm, "method", "n/a"),
        "report_path": state.get("report_path"),
        "selected_l1": state.get("selected_l1"),
        "rounds_log": state.get("rounds_log", []),
        "l2": state.get("l2"),
        "back_annotation": state.get("back_annotation"),
        "l5": state.get("l5"),
        "l5_selected": state.get("l5_selected"),
    }
