"""The L2 rung of the agent: shortlist the front, simulate it, re-select.

The ``l2_simulate`` node sits between ``select`` and the L3/L4/L5 rungs
(``back_annotate``). It does three things, all in code:

1. **Shortlist.** The run's merged L1 front, ordered by the spec's selection
   rule, top ``k`` (default 5). Only these are simulated: L2 is cheap but
   not free, and in a real flow the next rungs (RTL, synthesis) are dearer
   still, so the ladder narrows as fidelity rises.
2. **Simulate.** Each shortlisted design runs through the spec's system
   scenario (:mod:`hw_dse.l2.system`, SimPy) at its estimated Fmax; its
   ``sys_*`` metrics become *simulated* numbers and its feasibility is
   re-checked against every constraint. The selected design also gets the
   DDS spectrum and its interface contract, for the report.
3. **Re-select.** The spec's selection rule picks the best shortlisted design
   that passes the simulated system constraints. If that is not the design
   ``select`` chose from L1, the node says so ("winner changed at L2") and why.
   If no shortlisted design passes, the shortlist is extended down the
   front (up to ``max_k``) before giving up.

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
MAX_K = 20


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


def l2_select(front: list[dict[str, Any]], selected: dict[str, Any] | None, spec: Spec,
              k: int = DEFAULT_K, max_k: int = MAX_K) -> dict[str, Any]:
    """The node's logic as a pure function. Returns the L2 report and the
    (possibly new) selected design."""
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
    kk = k
    while True:
        cands = shortlist(front, spec, kk)
        sims = [simulate_record(r, spec) for r in cands]
        passing = [s for s in sims if s["feasible"]]
        if passing or kk >= max_k or len(cands) < kk:
            break
        out["notes"].append(f"none of the top {kk} passes the simulated system constraints; extending the shortlist")
        kk = min(max_k, kk * 2)
    out["status"] = "simulated"
    out["k"] = kk
    out["shortlist"] = [{"key": s["key"], "feasible": s["feasible"],
                         **{c.metric: s[c.metric] for c in spec.system_constraints},
                         "l1_bound": {c.metric: r.get(c.metric) for c in spec.system_constraints},
                         "violations": {k: v for k, v in s["violations"].items() if v > 0}}
                        for s, r in zip(sims, cands)]
    best = select_design(passing, spec)
    out["selected"] = best
    if best is None:
        out["winner_changed"] = True
        out["why"] = f"no design in the top {kk} of the front passes the simulated system constraints"
    elif best["key"] != selected["key"]:
        out["winner_changed"] = True
        sel_sim = next((s for s in sims if s["key"] == selected["key"]), None)
        viol = "; ".join(f"{k} by {v * 100:.1f}%" for k, v in (sel_sim or {}).get("violations", {}).items() if v > 0)
        out["why"] = (f"the L1 selection {selected['key']} fails the simulated system constraints ({viol}); "
                      f"the best shortlisted design that passes is {best['key']}")
    else:
        out["why"] = "the L1 selection passes the simulated system constraints"
    return out
