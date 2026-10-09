"""The campaign agent offline: scripted chat model, rule-based inner architect.

No LLM output is needed: :class:`ScriptedChatModel` fixes the campaign
agent's tool calls, so these tests check what the Deep Agents harness and our
tools do with them (budget, ladder, memory, the forced re-plan, the
memory-off switch).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

if os.environ.get("HW_DSE_REQUIRE_CAMPAIGN") == "1":
    import deepagents  # noqa: F401  (CI on Python >= 3.11: a missing install must fail, not skip)
else:
    pytest.importorskip("deepagents")

from langchain_core.messages import SystemMessage, ToolMessage  # noqa: E402

from hw_dse.agent.llm import HeuristicArchitect  # noqa: E402
from hw_dse.campaign.agent import build_campaign_agent  # noqa: E402
from hw_dse.campaign.fake import ScriptedChatModel, say, tool  # noqa: E402
from hw_dse.campaign.memory import CampaignMemory  # noqa: E402
from hw_dse.campaign.runner import run_campaign  # noqa: E402
from hw_dse.campaign.tools import CampaignContext  # noqa: E402
from hw_dse.explore import run_family_study  # noqa: E402
from hw_dse.families import full_box  # noqa: E402


def _last_tool_text(msgs: list) -> str:
    return next(str(m.content) for m in reversed(msgs) if isinstance(m, ToolMessage))


def test_campaign_walks_the_ladder_with_todos_files_and_a_subagent(tmp_path: Path) -> None:
    s = "low_area_control"
    chat = ScriptedChatModel(script=[
        say("", tool("recall"), tool("list_specs")),
        say("", tool("write_todos", todos=[{"content": f"explore {s}", "status": "in_progress"},
                                           {"content": f"ladder {s}", "status": "pending"}])),
        say("", tool("run_dse", spec_name=s, evals=300)),
        say("", tool("explore_family", spec_name=s, family="iterative", evals=100, data_width_min=12, data_width_max=16)),
        say("", tool("write_file", file_path="/notes.md", content="front looks iterative")),
        say("", tool("simulate_system", spec_name=s)),
        say("", tool("task", description=f"ladder for {s}", subagent_type="ladder")),
        # inside the ladder sub-agent (same scripted model)
        say("", tool("verify_rtl", spec_name=s), tool("synthesize", spec_name=s), tool("back_annotate", spec_name=s)),
        say("ladder done: findings quoted from the tools"),
        # back in the main agent
        say("", tool("finalize", spec_name=s, note="iterative wins")),
        say("All specs finalized."),
    ])
    res = run_campaign([s], seed=0, chat=chat, model="fake", architect=HeuristicArchitect(),
                       memory=CampaignMemory(enabled=False), run_root=tmp_path)
    assert res["error"] is None, res["error"]
    ps = res["per_spec"][s]
    assert ps["used"] == 400 and len(ps["evaluations"]) == 400 and not ps["left_open"]
    assert ps["calls"][:3] == ["run_dse", "explore_family", "simulate_system"]
    assert sorted(ps["calls"][3:]) == ["back_annotate", "synthesize", "verify_rtl"]  # parallel calls in the sub-agent
    assert ps["selected"] is not None and ps["selected"]["feasible"]
    assert res["todos"] and res["todos"][0]["content"] == f"explore {s}"
    tools_used = [r["tool"] for r in map(json.loads, (Path(res["run_dir"]) / "tool_log.jsonl").read_text().splitlines())]
    assert tools_used[:2] == ["recall", "list_specs"] and "verify_rtl" in tools_used
    trace = [json.loads(x) for x in (Path(res["run_dir"]) / "llm_trace.jsonl").read_text().splitlines()]
    assert any(t["node"] == "campaign" for t in trace) and any(t["node"] == "propose" for t in trace)
    # the ladder sub-agent ran with its own prompt
    assert any(isinstance(m, SystemMessage) and "CURRENT selection" in str(m.content) for msgs in chat.seen for m in msgs)


def test_budget_is_the_structured_arms_budget(tmp_path: Path) -> None:
    s = "low_area_control"
    chat = ScriptedChatModel(script=[
        say("", tool("run_dse", spec_name=s, evals=1000)),
        say("", tool("explore_family", spec_name=s, family="pipelined", evals=50)),
        say("", tool("run_dse", spec_name="no_such_spec", evals=100)),
        say("", tool("finalize", spec_name=s)),
        say("done"),
    ])
    res = run_campaign([s], chat=chat, model="fake", architect=HeuristicArchitect(), run_root=tmp_path)
    log = [json.loads(x) for x in (Path(res["run_dir"]) / "tool_log.jsonl").read_text().splitlines()]
    assert res["per_spec"][s]["used"] == 400
    assert log[1]["result"].startswith("refused") and "unknown spec" in log[2]["result"]


def test_a_flagged_winner_change_forces_the_l5_replan(tmp_path: Path) -> None:
    """Recorded L4 data flags the dds_250msps optimum (4.4% short of 250 MSPS in
    nextpnr): finalize refuses until reexplore has run."""
    s = "dds_250msps"
    ctx = CampaignContext.new([s], tmp_path / "c", 0, HeuristicArchitect(), CampaignMemory(enabled=False))
    led = ctx.specs[s]
    box = {**full_box("pipelined"), "data_width": (18, 18), "n_iter": (15, 15), "angle_guard": (1, 1), "frac_guard": (0, 0)}
    led.pool = run_family_study("pipelined", box, led.spec, 20, 0)
    led.used = 20
    seen: list[str] = []

    def after_finalize(msgs: list) -> object:
        seen.append(_last_tool_text(msgs))
        return say("", tool("reexplore", spec_name=s))

    chat = ScriptedChatModel(script=[
        say("", tool("back_annotate", spec_name=s)),
        say("", tool("finalize", spec_name=s)),
        after_finalize,
        say("", tool("finalize", spec_name=s)),
        say("done"),
    ])
    agent = build_campaign_agent(chat, ctx)
    out = agent.invoke({"messages": [{"role": "user", "content": "go"}]}, {"recursion_limit": 50})
    assert seen and seen[0].startswith("refused: back_annotate flagged a winner change")
    assert led.l5 is not None and led.l5["status"] == "reexplored" and led.finalized
    assert "finalized dds_250msps" in _last_tool_text(out["messages"])


def test_memory_written_with_run_ids_read_back_and_switchable(tmp_path: Path) -> None:
    s = "low_area_control"

    def campaign(mem: CampaignMemory, run_id: str) -> tuple[dict, ScriptedChatModel]:
        chat = ScriptedChatModel(script=[
            say("", tool("recall")),
            say("", tool("run_dse", spec_name=s, evals=400)),
            say("", tool("remember", key="tip", lesson="FSM families win low-rate specs")),
            say("", tool("finalize", spec_name=s)),
            say("done"),
        ])
        return run_campaign([s], chat=chat, model="fake", architect=HeuristicArchitect(), memory=mem,
                            run_root=tmp_path, run_id=run_id), chat

    mem = CampaignMemory(enabled=True)
    campaign(mem, "run-A")
    lessons = mem.lessons()
    fam = [x for x in lessons if x["kind"] == "family"]
    assert fam and all(x["run_ids"] == ["run-A"] and x["author"] == "code" for x in fam)
    assert any(x["kind"] == "note" and x["author"] == "llm" and x["run_ids"] == ["run-A"] for x in lessons)
    assert any(x["kind"] == "spec_class" for x in lessons)
    # persisted and reloaded: the next campaign's system prompt carries the digest, recall returns it
    path = tmp_path / "store.json"
    mem.save(path)
    mem2 = CampaignMemory.load(path)
    _, chat2 = campaign(mem2, "run-B")
    sys_msg = next(m for m in chat2.seen[0] if isinstance(m, SystemMessage))
    assert "FSM families win low-rate specs" in str(sys_msg.content) and "run-A" in str(sys_msg.content)
    assert any(set(x["run_ids"]) == {"run-A", "run-B"} for x in mem2.lessons() if x["kind"] == "family")
    # memory off: nothing read, nothing written
    off = CampaignMemory(enabled=False)
    _, chat3 = campaign(off, "run-C")
    sys3 = next(m for m in chat3.seen[0] if isinstance(m, SystemMessage))
    assert "(memory is switched off)" in str(sys3.content) and off.dump() == {}
    texts = [str(m.content) for m in chat3.seen[-1] if isinstance(m, ToolMessage)]
    assert any("memory is switched off" in t for t in texts)


def test_a_stuck_model_is_stopped_and_counted_as_a_failure(tmp_path: Path) -> None:
    s = "low_area_control"
    chat = ScriptedChatModel(script=[say("", tool("list_specs")) for _ in range(10)])
    res = run_campaign([s], chat=chat, model="fake", architect=HeuristicArchitect(), run_root=tmp_path)
    assert res["error"] and "repeated the same tool call" in res["error"]
    assert res["campaign_model_calls"] <= 5 and res["per_spec"][s]["left_open"]


def test_the_model_call_cap_stops_a_campaign(tmp_path: Path) -> None:
    s = "low_area_control"
    chat = ScriptedChatModel(script=[say("", tool("write_todos", todos=[{"content": f"step {i}", "status": "pending"}]))
                                     for i in range(10)])
    res = run_campaign([s], chat=chat, model="fake", architect=HeuristicArchitect(), run_root=tmp_path, max_model_calls=3)
    assert res["error"] and "call limit (3)" in res["error"]


def test_llm_notes_carry_no_numbers() -> None:
    """M3 review S5: an LLM note restating tool numbers (and getting them wrong) must
    not reach memory or the inner architect with its numbers."""
    from hw_dse.campaign.memory import mask_numbers

    mem = CampaignMemory(enabled=True)
    mem.remember("note", "low_area_control", "M1 under-predicts LUTs ~19% (216 LUT vs est 159), use m=4", ["r"], "llm")
    note = mem.lessons(("note",))[0]["lesson"]
    assert not any(ch.isdigit() for ch in note.replace("M1", ""))
    assert mask_numbers("2^-12 at 32 MSPS") == "#^# at # MSPS"
    mem.remember("family", "iterative", "explored in 3 spec(s) (353 evaluations)", ["r"], "code")
    assert "353" in mem.lessons(("family",))[0]["lesson"]  # code-written lessons keep their numbers
