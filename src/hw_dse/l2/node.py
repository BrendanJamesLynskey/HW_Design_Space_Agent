"""The L2 rung of the agent: shortlist the front, simulate it, re-select.

The ``l2_simulate`` node sits between ``select`` and the L3/L4/L5 rungs
(``back_annotate``). It does three things, all in code:

1. **Candidates.** Every unique L1-feasible design the run evaluated, ordered
   by the spec's selection rule. Not only the L1 front: a design that passes
   L2 can be dominated in the L1 objectives by one that only passed the
   optimistic bound (milestone-3 review, B1). The report shows the top ``k``
   (default 5) as the "shortlist".
2. **Simulate.** Each candidate runs through the spec's system scenario
   (:mod:`hw_dse.l2.system`, SimPy) at its estimated Fmax; its ``sys_*``
   metrics become *simulated* numbers and its feasibility is re-checked
   against every constraint. Simulations are cached per (latency, ii, Fmax),
   so a run's few hundred designs cost a few dozen simulations. The selected
   design also gets the DDS spectrum and its interface contract.
3. **Re-select.** The spec's selection rule picks the best candidate that
   passes the simulated system constraints. If that is not the design
   ``select`` chose from L1, the node says so ("winner changed at L2") and why.

For a spec with no ``system`` scenario nothing is re-selected: the node only
attaches the selected design's L2 facts (contract, DDS spectrum) to the
report, so milestone-2 behaviour is untouched.
"""

from __future__ import annotations

from typing import Any

from hw_dse.benchmark import select_design
from hw_dse.evaluate import add_feasibility
from hw_dse.l2.cycle import Contract
from hw_dse.l2.dds import PROVENANCE as DDS_PROV
from hw_dse.l2.dds import dds_spectrum
from hw_dse.l2.system import provenance, system_metrics
from hw_dse.spec import Spec

DEFAULT_K = 5


def _numerics(rec: dict[str, Any]) -> Any:
    from hw_dse.families import REGISTRY, ArchConfig

    names = [p.name for p in REGISTRY[rec["family"]].params]
    return ArchConfig.from_params(rec["family"], {n: rec[n] for n in names}).numerics


def simulate_record(rec: dict[str, Any], spec: Spec) -> dict[str, Any]:
    """A copy of ``rec`` with simulated system metrics and feasibility re-checked."""
    out = {**rec, "provenance": dict(rec.get("provenance") or {})}
    if spec.system is None:
        return out
    m = system_metrics(spec.system, Contract.from_record(rec), float(rec["fmax_mhz"]))
    prov = provenance(spec.system, float(rec["fmax_mhz"]))
    for k, v in m.items():
        out[k] = v
        out["provenance"][k] = prov
    if any(c.metric in ("sys_sfdr_dbc", "sys_snr_db") for c in spec.constraints):
        out["sys_sfdr_dbc"], out["sys_snr_db"] = dds_spectrum(_numerics(rec))
        out["provenance"]["sys_sfdr_dbc"] = out["provenance"]["sys_snr_db"] = DDS_PROV
    out["l2_fidelity"] = "L2 simulated"
    return add_feasibility(out, spec)


def shortlist(front: list[dict[str, Any]], spec: Spec, k: int) -> list[dict[str, Any]]:
    """The front ordered by the spec's selection rule (best first), top ``k``."""
    ordered: list[dict[str, Any]] = []
    rest = list(front)
    while rest and len(ordered) < k:
        best = select_design(rest, spec)
        if best is None:
            break
        ordered.append(best)
        rest = [r for r in rest if r["key"] != best["key"]]
    return ordered


def l2_select(records: list[dict[str, Any]], selected: dict[str, Any] | None, spec: Spec,
              k: int = DEFAULT_K) -> dict[str, Any]:
    """The node's logic as a pure function. Returns the L2 report and the
    (possibly new) selected design.

    ``records`` is every L1 evaluation of the run (or campaign). Every unique
    L1-feasible design among them is simulated, not just the L1 front: a design
    that passes the simulated system constraints can be dominated in the L1
    objectives by one that only passed the optimistic L1 bound (on
    ``multiaxis_control``, m=4 has m=5's numerics and more area, so the L1 front
    holds m=5 alone, and m=5 fails at L2). Simulation is cached per (latency,
    ii, Fmax) tuple, of which the whole registry has 1,092, so this costs
    little. The report's ``shortlist`` is the top ``k`` by the selection rule,
    for display."""
    out: dict[str, Any] = {"status": "skipped", "shortlist": [], "selected": selected, "winner_changed": False,
                           "notes": []}
    if selected is None:
        out["reason"] = "no design selected"
        return out
    sel_num = _numerics(selected)
    sfdr, snr = dds_spectrum(sel_num)
    out["selected_facts"] = {"contract": vars(Contract.from_record(selected)), "dds_sfdr_dbc": sfdr, "dds_snr_db": snr,
                             "dds_provenance": DDS_PROV}
    if spec.system is None:
        out["status"] = "facts_only"
        out["reason"] = "the spec has no system scenario: nothing to re-select"
        return out
    uniq: dict[str, dict[str, Any]] = {}
    for r in records:
        if r.get("feasible"):
            uniq.setdefault(r["key"], r)
    cands = shortlist(list(uniq.values()), spec, len(uniq))  # every L1-feasible design, best first
    sims = [simulate_record(r, spec) for r in cands]
    passing = [s for s in sims if s["feasible"]]
    out["status"] = "simulated"
    out["k"] = k
    out["n_l1_feasible"] = len(cands)
    out["n_simulated_feasible"] = len(passing)
    out["shortlist"] = [{"key": s["key"], "feasible": s["feasible"],
                         **{c.metric: s[c.metric] for c in spec.system_constraints},
                         "l1_bound": {c.metric: r.get(c.metric) for c in spec.system_constraints},
                         "violations": {k2: v for k2, v in s["violations"].items() if v > 0}}
                        for s, r in list(zip(sims, cands))[:k]]
    best = select_design(passing, spec)
    out["selected"] = best
    if best is None:
        out["winner_changed"] = True
        out["why"] = f"none of the {len(cands)} L1-feasible designs passes the simulated system constraints"
    elif best["key"] != selected["key"]:
        out["winner_changed"] = True
        sel_sim = next((s for s in sims if s["key"] == selected["key"]), None)
        viol = "; ".join(f"{k2} by {v * 100:.1f}%" for k2, v in (sel_sim or {}).get("violations", {}).items() if v > 0)
        rank = [s["key"] for s in sims].index(best["key"]) + 1
        out["why"] = (f"the L1 selection {selected['key']} fails the simulated system constraints ({viol}); "
                      f"the best design that passes is {best['key']} (rank {rank} of {len(cands)} L1-feasible designs "
                      "by the selection rule)")
    else:
        out["why"] = "the L1 selection passes the simulated system constraints"
    return out
