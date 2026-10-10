"""The campaign layer (milestone 3): an optional outer agent on LangChain Deep Agents.

The structured LangGraph DSE graph (:mod:`hw_dse.agent.graph`) stays the
inner loop: typed decisions, replayable, comparable with milestones 1 and 2.
The campaign agent sits *around* it and does the long-horizon work: take one
or more specs down the whole ladder (system simulation, L1 exploration, L2
shortlist, L3 RTL, L4 synthesis, L5 back-annotation), re-plan when a
measurement changes the winner, and work through a queue of specs, carrying
lessons from one run to the next in a LangGraph Store.

It is built with ``deepagents.create_deep_agent`` (pinned, see the README):
the harness supplies the planning to-do tool (``write_todos``), a virtual
filesystem for notes, sub-agents through the ``task`` tool, and the model
loop. Everything that touches a number is one of *our* tools
(:mod:`hw_dse.campaign.tools`), and each tool returns numbers computed by
code with their provenance. The campaign agent orchestrates; like the inner
architect it never optimises and never produces a number.

Modules: :mod:`~hw_dse.campaign.memory` (cross-run lessons in the Store),
:mod:`~hw_dse.campaign.tools` (the tools and the per-campaign ledger),
:mod:`~hw_dse.campaign.agent` (the Deep Agents wiring and prompt),
:mod:`~hw_dse.campaign.fake` (a scripted chat model for offline tests),
:mod:`~hw_dse.campaign.runner` (one campaign end to end, scored offline).
"""

from __future__ import annotations
