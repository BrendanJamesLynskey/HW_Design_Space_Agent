"""L2 -> L1 feedback (milestone 4): correct the L1 system bound from L2's evidence.

The problem
-----------
L1 screens a system constraint with an analytic bound (:mod:`hw_dse.l2.bounds`)
that is optimistic by construction: a design that fails the bound fails the
simulation, but not the other way round. Usually that is enough: the run's
L1-feasible set contains designs that also pass at L2, and ``l2_simulate``
re-selects among them. It is not enough when **none** of the L1-feasible
designs passes the simulation. Then the run has spent its whole L1 budget
inside a region the bound says is fine and the system says is not; the
graph used to end with ``l2_no_feasible``.

What this module does
---------------------
The same thing L5 does for cost (refit the model to measurements, then
re-explore under the refit), with L2 simulations as the measurements:

1. **Measure the bound's error.** For every L1-feasible design that L2
   simulated, the ratio ``r = simulated / bound`` of each system-constrained
   metric. Because the bound is optimistic, r >= 1 for ``<=`` metrics and
   r <= 1 for ``>=`` metrics.
2. **Correct it, as a function of utilisation, per contract class.** The
   bound serves every burst alone; the simulation lets bursts overlap and
   queue, so the gap grows with the device's utilisation
   ``rho = offered rate x ii / Fmax`` (on the constructed spec below the
   ratio is 2.0 at rho = 0.48 and over 40 beyond rho = 1). It also depends on
   how a design accepts work (an FSM design takes one request every ``ii`` =
   latency cycles), so the correction is fitted separately for the ``fsm``
   and ``pipelined`` classes. Per class and metric, the observed
   ``(rho, r)`` pairs give a **monotone lower envelope**: at each observed
   rho, the smallest ratio seen at that or any higher utilisation.
   ``kappa(rho)`` is the envelope at the largest observed rho not above the
   design's own, and 1 (the analytic bound) below every observation. So
   ``bound * kappa`` never exceeds the simulation at any design L2 has seen
   (each one's kappa is at most its own ratio); for designs it has not seen
   it relies on one assumption, that the bound's error does not shrink as
   utilisation grows. It is an **empirical** bound, not a proven one, and it
   is labelled ``estimate (L1 bound, corrected by L2 feedback)``. A class
   with no observation keeps the analytic bound.
3. **Re-explore.** A separate, code-driven budget (default 2 rounds of 60
   evaluations, kept apart from the L1 evaluations, as the L5 loop's are;
   3 rounds: two were too few on the constructed spec):
   one NSGA-II study per family over its full box (the families that had an
   L1-feasible design, plus any the run never explored), with the system
   constraints screened by the corrected bound. Every new
   corrected-feasible design is simulated; the spec's rule picks the best
   design that passes, from the L1 and the feedback designs together. If
   nothing passes, the new simulations refine ``kappa`` and the next round
   runs; after the last round the run ends ``l2_no_feasible`` as before.

The LLM is not involved, and no number here comes from one.
"""

from __future__ import annotations

from typing import Any

from hw_dse.benchmark import select_design
from hw_dse.evaluate import add_feasibility
from hw_dse.spec import Spec

DEFAULT_ROUNDS = 3
DEFAULT_EVALS_PER_ROUND = 60
CORRECTED_PROVENANCE = "estimate: L1 analytic bound of the system metric, corrected by L2 feedback (empirical)"


def contract_class(rec: dict[str, Any]) -> str:
    return "pipelined" if rec["family"] in ("pipelined", "pipelined_m") else "fsm"


def utilisation(rec: dict[str, Any], spec: Spec) -> float:
    """rho = offered requests per us x cycles per accept / Fmax (MHz)."""
    assert spec.system is not None
    ii = 1 if contract_class(rec) == "pipelined" else int(rec["latency_cycles"])
    return spec.system.offered_rate_msps * ii / float(rec["fmax_mhz"])


def envelope(points: list[tuple[float, float]], op: str) -> list[tuple[float, float]]:
    """Monotone envelope of (rho, ratio) pairs, sorted by rho.

    ``<=`` metrics (ratio >= 1): at each rho the smallest ratio at that or a
    higher rho (non-decreasing in rho, and <= every observed ratio at its rho).
    ``>=`` metrics (ratio <= 1): the mirror image, the largest ratio at that or
    a higher rho (non-increasing)."""
    best: dict[float, float] = {}  # one entry per distinct rho (designs often share a clock and contract)
    for rho, r in points:
        best[rho] = min(best.get(rho, r), r) if op == "<=" else max(best.get(rho, r), r)
    out: list[tuple[float, float]] = []
    run = float("inf") if op == "<=" else float("-inf")
    for rho in sorted(best, reverse=True):
        run = min(run, best[rho]) if op == "<=" else max(run, best[rho])
        out.append((rho, run))
    return list(reversed(out))


def kappa_at(env: list[tuple[float, float]], rho: float) -> float:
    """The envelope at the largest observed rho <= ``rho``; 1 below every observation."""
    k = 1.0
    for x, r in env:
        if x <= rho:
            k = r
        else:
            break
    return k


def corrections(pairs: list[tuple[dict[str, Any], dict[str, Any]]], spec: Spec) -> dict[str, dict[str, Any]]:
    """Per system-constrained metric and contract class: the correction envelope and its evidence.

    ``pairs`` = (L1 record with the bound's value, the same design simulated)."""
    out: dict[str, dict[str, Any]] = {}
    for c in spec.system_constraints:
        per: dict[str, Any] = {}
        for cls in ("fsm", "pipelined"):
            pts = [(utilisation(r, spec), float(s[c.metric]) / float(r[c.metric])) for r, s in pairs
                   if contract_class(r) == cls and float(r[c.metric]) > 0]
            if not pts:
                per[cls] = {"envelope": [], "n": 0, "note": "no simulated design of this class: analytic bound kept"}
                continue
            env = envelope(pts, c.op)
            per[cls] = {"envelope": env, "n": len(pts), "rho_range": [env[0][0], env[-1][0]],
                        "kappa_range": [env[0][1], env[-1][1]]}
        out[c.metric] = per
    return out


def corrected(rec: dict[str, Any], spec: Spec, corr: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """``rec`` with every system-constrained bound multiplied by kappa(rho), feasibility re-checked."""
    out = {**rec, "provenance": dict(rec.get("provenance") or {})}
    cls = contract_class(rec)
    rho = utilisation(rec, spec)
    for metric, per in corr.items():
        out[f"{metric}_bound"] = rec[metric]
        out[metric] = float(rec[metric]) * kappa_at(per[cls]["envelope"], rho)
        out["provenance"][metric] = CORRECTED_PROVENANCE
    out["l2_fidelity"] = "L1 bound, corrected by L2 feedback"
    return add_feasibility(out, spec)


def fires(l2: dict[str, Any] | None) -> bool:
    """Does the feedback apply? Only when L2 simulated and nothing passed."""
    return bool(l2 and l2.get("status") == "simulated" and l2.get("n_l1_feasible", 0) > 0
                and l2.get("n_simulated_feasible", 0) == 0)


def feedback(spec: Spec, records: list[dict[str, Any]], seed: int = 0, rounds: int = DEFAULT_ROUNDS,
             evals_per_round: int = DEFAULT_EVALS_PER_ROUND) -> dict[str, Any]:
    """The ``l2_feedback`` node's logic as a pure function of the run's L1 evaluations."""
    from hw_dse.explore import run_family_study
    from hw_dse.families import REGISTRY, full_box
    from hw_dse.l2.node import simulate_record

    uniq: dict[str, dict[str, Any]] = {}
    for r in records:
        if r.get("feasible"):
            uniq.setdefault(r["key"], r)
    pairs = [(r, simulate_record(r, spec)) for r in uniq.values()]
    passing = [s for _, s in pairs if s["feasible"]]
    log: list[dict[str, Any]] = []
    new_recs: list[dict[str, Any]] = []
    sel = select_design(passing, spec)
    for rnd in range(1, rounds + 1):
        if sel is not None:
            break
        corr = corrections(pairs, spec)
        # Where to look: families with an L1-feasible design in the run, plus
        # families the run never explored. A family whose designs all failed
        # the *analytic* bound cannot pass the corrected one (kappa >= 1 for a
        # <= metric), so its share would be wasted.
        explored = {r["family"] for r in records}
        fams = [f for f in REGISTRY if f in {r["family"] for r in uniq.values()} or f not in explored] or list(REGISTRY)
        per = [evals_per_round // len(fams)] * len(fams)
        for i in range(evals_per_round - sum(per)):
            per[i % len(fams)] += 1
        got: list[dict[str, Any]] = []
        for i, (fam, n) in enumerate(zip(fams, per)):
            got += run_family_study(fam, full_box(fam), spec, n, seed * 6151 + 977 * rnd + i,
                                    tag={"round": f"L2F{rnd}"}, transform=lambda rec, c=corr: corrected(rec, spec, c))
        new_recs += got
        cand: dict[str, dict[str, Any]] = {}
        for r in got:
            if r.get("feasible") and r["key"] not in uniq:
                cand.setdefault(r["key"], r)
        sims = [(r, simulate_record({k: v for k, v in r.items() if not k.endswith("_bound")}, spec))
                for r in cand.values()]
        # kappa is fitted against the *analytic* bound, so restore it on the pairs
        pairs += [({**r, **{m: r[f"{m}_bound"] for m in corr}}, s) for r, s in sims]
        uniq.update(cand)
        passing += [s for _, s in sims if s["feasible"]]
        sel = select_design(passing, spec)
        summary = {m: {cls: {k: v for k, v in d.items() if k != "envelope"} for cls, d in per.items()}
                   for m, per in corr.items()}
        log.append({"round": rnd, "corrections": summary, "n_evals": len(got), "n_corrected_feasible": len(cand),
                    "n_passing": sum(s["feasible"] for _, s in sims),
                    "selected_key": sel["key"] if sel else None})
    return {
        "status": "recovered" if sel is not None else "no_feasible",
        "rounds": log,
        "n_evals": len(new_recs),
        "selected": sel,
        "selected_key": sel["key"] if sel else None,
        "evaluations": new_recs,
        "notes": ["separate L2-feedback budget: these evaluations are not L1 evaluations and are not counted "
                  "against the spec's total_evals"],
    }
