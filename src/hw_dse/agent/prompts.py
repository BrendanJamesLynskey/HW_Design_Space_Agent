"""Prompt text for the three LLM roles: intake, propose, analyse.

The prompts make the division of labour explicit to the model. It is the
*architect*: it reads the spec, picks families and ranges from a fixed
registry, reads compact results and decides what to do next. It is told,
in so many words, that it must not estimate or invent PPA or accuracy
numbers, because the code will compute them and the numbers it sees are
the only ones that count.

The registry table and metric glossary are generated from code
(:func:`hw_dse.families.registry_table`, :data:`hw_dse.spec.METRIC_HELP`),
so the prompt can never drift from what the explorer actually supports.
"""

from __future__ import annotations

from hw_dse.families import registry_table
from hw_dse.spec import METRIC_HELP, SYSTEM_METRICS, TARGET_ONLY_METRICS, Spec

SYSTEM = f"""You are the hardware architect in a design-space exploration loop for a
CORDIC sin/cos unit on an Artix-7 FPGA.

Division of labour (strict):
- YOU choose architecture families and parameter ranges from the registry below,
  read compact summaries of results, and decide what to do next.
- CODE does all the numbers: a bit-accurate model gives exact accuracy, an
  analytical cost model gives LUT/FF/Fmax estimates, Optuna NSGA-II searches inside
  the ranges you choose, and Pareto/hypervolume maths ranks the results.
- Never estimate, predict or invent LUTs, FFs, Fmax, throughput, power or error
  figures. Reason only from the numbers in the summaries you are given.

Architecture registry (the only families and parameters that exist):
{registry_table()}

Goal: map the feasible Pareto front over the spec's objectives as well as possible
within the evaluation budget (scored by hypervolume against the spec's reference
point); the final design is then picked from that front by the spec's selection
rule. Both matter: the hypervolume rewards covering the whole trade-off curve, not
just the corner the selection rule picks. Before the run ends, code spends a reserved
part of the budget mapping the front over the full ranges of the families you found on
it. If no design in the registry can meet the constraints, say so (decision
`infeasible`) rather than settling for a design that violates them.

Notes:
- Accuracy depends only on data_width, n_iter, angle_guard, frac_guard and rounding
  (all families compute identical bits); output LSB is 2^-(data_width-2).
- iterative/unrolled_k produce one result every several cycles; pipelined/pipelined_m
  produce one result per cycle.
- Ranges are inclusive. Narrow ranges focus the evaluation budget; ranges outside the
  registry are clamped by code.

Metrics:
""" + "\n".join(f"- {k}: {v}" for k, v in METRIC_HELP.items()
                if k not in SYSTEM_METRICS and k not in TARGET_ONLY_METRICS["asic"])
# (The system metrics are listed only for specs that have a system scenario,
# below, so a milestone-2 spec gets exactly the milestone-2 prompt. The ASIC
# metrics of milestone 4 are left out of it for the same reason: an FPGA spec's
# prompt is byte-identical to milestones 1-3, which the replay tests check.)

# Milestone 4: the same architect role for the ASIC target. Only the target,
# the cost-model wording and the metric list differ; the registry, the goal and
# the notes are the FPGA prompt's own text.
SYSTEM_ASIC = (
    SYSTEM.split("Metrics:")[0]
    .replace("CORDIC sin/cos unit on an Artix-7 FPGA.",
             "CORDIC sin/cos unit as an ASIC in the open sky130 standard-cell library\n(sky130_fd_sc_hd, typical corner).")
    .replace("analytical cost model gives LUT/FF/Fmax estimates",
             "analytical cost model gives cell-area/FF/Fmax estimates")
    .replace("invent LUTs, FFs, Fmax", "invent area, gate counts, FFs, Fmax")
    + "Metrics:\n"
    + "\n".join(f"- {k}: {v}" for k, v in METRIC_HELP.items()
                if k not in SYSTEM_METRICS and k not in TARGET_ONLY_METRICS["fpga"])
)

SYSTEM_L2_ADDENDUM = """
This spec also has a SYSTEM scenario (milestone 3): the CORDIC sits in a system
(a DDS, a control loop or a bursty request stream) and some constraints are on
system metrics (sys_*). During exploration those metrics are ANALYTIC BOUNDS,
optimistic by construction (queueing between bursts and clock-edge alignment are
ignored). After selection, code simulates the top designs of the front in the
system (SimPy, L2) and re-selects among those that pass, so a front whose cheapest
designs only just pass the bound may lose them at L2. Throughput alone does not
capture bursts: a design that accepts one request every few cycles queues the rest
of a burst. System metrics:
""" + "\n".join(f"- {k}: {METRIC_HELP[k]}" for k in SYSTEM_METRICS)


def system_prompt(spec: Spec) -> str:
    """The architect's system prompt: :data:`SYSTEM`, plus the L2 addendum for a
    spec with a system scenario (milestone-2 specs get :data:`SYSTEM` unchanged)."""
    base = SYSTEM_ASIC if spec.target_kind == "asic" else SYSTEM
    return base if spec.system is None else base + "\n" + SYSTEM_L2_ADDENDUM

INTAKE = """Turn this natural-language request into a structured spec draft.
Only record requirements the text actually states; leave the rest empty.
Accuracy targets like "2^-13" or "13 bits" mean max_abs_err = 2^-13 = 0.0001220703125.

Request:
{text}
"""

PROPOSE = """Spec:
{spec}

Evaluation budget: {budget} evaluations in total, up to {per_round} per round,
at most {max_rounds} rounds.

Propose the first exploration plan: which families to search (1-4) and the
parameter ranges for each, with a relative budget share. Prefer families that can
plausibly meet the constraints; spend the budget where the trade-offs are. Explain
your reasoning briefly in `rationale` and per family in `why`.
"""

CAMPAIGN_NOTES = """
Notes from the campaign agent that launched this run (lessons from earlier runs;
advisory, not numbers to rely on):
{notes}
"""

ANALYSE = """Spec:
{spec}

Results so far (computed by code; these are the only valid numbers):
{summary}

Decide the next step:
- refine: narrow ranges around the promising region (give next_plan)
- widen: enlarge ranges that look too tight (give next_plan)
- add_family: bring in a family not yet explored (give next_plan)
- map_front: let code spend this round mapping the whole front (NSGA-II over the full
  ranges of the families on the front, seeded with it); use it when the front covers
  only a small part of an objective's range (no next_plan needed)
- infeasible: no family in the registry can meet the constraints (explain which
  constraint is unreachable and the evidence)
- stop: the front is good enough or no longer improving
{final_note}
Give a short rationale that cites the evidence above."""

FINAL_NOTE = """
NOTE: this is the final round (round cap or budget reached). Choose `stop` or
`infeasible`; any other decision will be treated as `stop`.
"""
