"""The fleet's shared memory: one LangGraph Store for evaluated designs and lessons.

Every member of a fleet (:mod:`hw_dse.fleet.coordinator`) is an ordinary
structured graph; the only thing they share is this store. Two namespaces per
spec:

``("fleet", <spec>, "evaluated")``
    One item per design key: the evaluation record (all metrics, their
    provenance, feasibility) as code computed it, plus which members evaluated
    it and how often. Written by the graph's ``explore_family`` node as each
    study finishes, so a member's evaluations are visible to the coordinator
    (and to members started later) without passing state around.
``("fleet", <spec>, "lessons")``
    Code-written facts the coordinator derives between phases: per family,
    how many designs were evaluated, how many were feasible, the best value
    of the selection metric and how many designs sit on the merged front.
    Every value is computed by code from the evaluated designs; there is no
    free-text field and nothing an LLM wrote ever reaches this namespace.
    (The M3 campaign agent's free-text notes into the inner architect were
    one of its two failure modes; here there is no channel for them.)

LangGraph's ``InMemoryStore`` is used (no persistence is needed: a fleet run
is one process). Puts from parallel members are serialised by a lock, since
the record of a design two members both evaluated is read-modify-written.
"""

from __future__ import annotations

import threading
from typing import Any

from langgraph.store.memory import InMemoryStore

_LOCK = threading.Lock()


def new_store() -> InMemoryStore:
    return InMemoryStore()


def ns(spec_name: str, kind: str) -> tuple[str, str, str]:
    return ("fleet", spec_name, kind)


def put_evaluations(store: Any, spec_name: str, member: str, records: list[dict[str, Any]]) -> None:
    """Record ``member``'s evaluations (called from the graph's explore node)."""
    with _LOCK:
        for r in records:
            item = store.get(ns(spec_name, "evaluated"), r["key"])
            val = dict(item.value) if item else {"record": {k: v for k, v in r.items() if k not in ("round", "trial")},
                                                 "by": {}, "n": 0}
            by = dict(val["by"])
            by[member] = by.get(member, 0) + 1
            val.update(by=by, n=int(val["n"]) + 1)
            store.put(ns(spec_name, "evaluated"), r["key"], val)


def evaluated(store: Any, spec_name: str) -> list[dict[str, Any]]:
    """Every distinct design the fleet has evaluated for ``spec_name`` (the stored records)."""
    return [it.value["record"] for it in store.search(ns(spec_name, "evaluated"), limit=1_000_000)]


def evaluation_counts(store: Any, spec_name: str) -> dict[str, int]:
    """Evaluations per member, repeats included (the budget accounting)."""
    out: dict[str, int] = {}
    for it in store.search(ns(spec_name, "evaluated"), limit=1_000_000):
        for m, n in it.value["by"].items():
            out[m] = out.get(m, 0) + int(n)
    return out


def put_lessons(store: Any, spec_name: str, lessons: dict[str, dict[str, Any]]) -> None:
    with _LOCK:
        for fam, val in lessons.items():
            store.put(ns(spec_name, "lessons"), fam, val)


def lessons(store: Any, spec_name: str) -> dict[str, dict[str, Any]]:
    return {it.key: it.value for it in store.search(ns(spec_name, "lessons"), limit=1000)}
