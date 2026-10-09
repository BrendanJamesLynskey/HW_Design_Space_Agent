"""Wire the campaign agent with LangChain Deep Agents (``deepagents==0.7.23``).

What the harness gives us, and what we add or switch off
--------------------------------------------------------
``create_deep_agent`` builds a LangGraph agent loop with middleware for:

* a **virtual filesystem** (``ls``, ``read_file``, ``write_file``,
  ``edit_file``; state-backed, so notes live in the run's state, not on
  disk). We keep those four and drop ``glob`` / ``grep`` / ``delete`` to save
  prompt tokens (a harness profile's ``excluded_tools``);
* **sub-agents** through the ``task`` tool. We define one, ``ladder``, that
  walks a selected design up L3 -> L4 -> L5 with only those tools, and switch
  off the auto-added general-purpose sub-agent (it would duplicate the main
  agent at extra cost);
* summarisation of long histories and tool-call patching.

The **planning to-do tool** (``write_todos``) is *not* in 0.7.23's default
stack any more (only one built-in model profile adds it), so we add
LangChain's ``TodoListMiddleware`` ourselves. Long-term memory is our own
typed layer over a LangGraph Store (:mod:`hw_dse.campaign.memory`), exposed
through ``recall`` / ``remember`` and a digest in the system prompt, so every
lesson carries its run IDs.
"""

from __future__ import annotations

from typing import Any

from hw_dse.campaign.tools import CampaignContext, make_tools

SYSTEM = """You run a hardware design-space-exploration CAMPAIGN for a CORDIC sin/cos unit on an
Artix-7 FPGA. You orchestrate tools; you never compute, estimate or invent a number. Every
number you see comes from code with a provenance label (estimate / exact / simulated /
measured, recorded).

For each spec in the queue, take it down the fidelity ladder:
1. L1 exploration: `run_dse` (the structured DSE graph: an inner architect plans NSGA-II
   searches; it also runs the L2 shortlist) and/or `explore_family` (one NSGA-II study in a
   box you choose). Both spend the spec's L1 budget (400 evaluations per spec, the same as
   the structured graph alone gets). Unspent budget is wasted; overspending is refused.
2. L2: `simulate_system` (SimPy system simulation of the front's top designs; essential for
   specs with a system scenario, whose sys_* numbers are optimistic bounds until simulated).
3. L3/L4/L5: `verify_rtl`, `synthesize` (recorded measurements only), `back_annotate`. If
   back_annotate flags a WINNER CHANGE, call `reexplore` (L5 loop) before `finalize`. The
   `ladder` sub-agent (via `task`) can do steps 3 for you.
4. `finalize` the spec. Then move to the next spec.

The goal per spec, scored afterwards against an exhaustive ground truth you cannot see: a
well-mapped feasible Pareto front over the spec's objectives AND a good final selection by
the spec's rule. Plan with `write_todos`; keep notes in files if useful. Use `recall` at the
start and `remember` for lessons worth keeping (text only). Be economical with tool calls.
When every spec is finalized, reply with a one-paragraph summary and stop.

Lessons from earlier campaigns (memory):
{memory}
"""

LADDER_PROMPT = """You take the CURRENT selection of one spec up the ladder: call verify_rtl, then
synthesize, then back_annotate for the spec you are given; if back_annotate reports a WINNER
CHANGE, call reexplore. Report the tools' findings in a few lines, quoting their provenance.
Never compute or invent numbers."""

EXCLUDED_TOOLS = frozenset({"glob", "grep", "delete", "execute"})


def _register_profile(model: Any) -> None:
    """Profile for this model: no general-purpose sub-agent, fewer file tools."""
    from deepagents import GeneralPurposeSubagentProfile, HarnessProfile, register_harness_profile
    from deepagents._models import get_model_identifier, get_model_provider

    prof = HarnessProfile(excluded_tools=EXCLUDED_TOOLS,
                          general_purpose_subagent=GeneralPurposeSubagentProfile(enabled=False))
    prov, ident = get_model_provider(model), get_model_identifier(model)
    for key in {f"{prov}:{ident}", str(prov)} if prov else {str(ident)}:
        register_harness_profile(key, prof)


def build_campaign_agent(model: Any, ctx: CampaignContext) -> Any:
    from deepagents import create_deep_agent
    from langchain.agents.middleware import TodoListMiddleware

    tools = make_tools(ctx)
    by_name = {t.name: t for t in tools}
    _register_profile(model)
    ladder = {
        "name": "ladder",
        "description": "Takes one spec's current selection through L3 (verify_rtl), L4 (synthesize, recorded) and "
                       "L5 (back_annotate, and reexplore if the winner changed). Give it the spec name.",
        "system_prompt": LADDER_PROMPT,
        "tools": [by_name[n] for n in ("verify_rtl", "synthesize", "back_annotate", "reexplore")],
    }
    return create_deep_agent(model=model, tools=tools, system_prompt=SYSTEM.format(memory=ctx.memory.digest()),
                             subagents=[ladder], middleware=[TodoListMiddleware()], store=ctx.memory.store,
                             name="hw_dse_campaign")
