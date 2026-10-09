"""Run one campaign end to end and score it offline.

:func:`run_campaign` builds the campaign's context (ledgers, memory, the inner
architect), wires the Deep Agents agent around a chat model, sends it one
user message naming the queue, and lets it run. Afterwards code:

* finalizes any spec the agent left open (and counts that as a failure),
* writes the code-derived lessons into memory (if memory is on),
* collects, per spec, the ordered L1 evaluations, the final selection, the
  L2/L5 results and the ladder steps the agent took,
* totals tokens and provider-reported cost over *every* LLM call (the
  campaign model's turns and the inner architect's structured calls), all
  written to one key-redacted ``llm_trace.jsonl``.

Scoring against the ground truth happens in the eval (``eval/run_eval.py``),
never inside the campaign: the agent cannot see it.
"""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any

from hw_dse.agent.trace import Tracer
from hw_dse.campaign.memory import CampaignMemory
from hw_dse.campaign.tools import CampaignContext, t_finalize


REPEAT_LIMIT = 4  # identical tool calls in a row before the campaign is stopped as stuck


class TraceCallback:
    """LangChain callback: log every campaign-model call (usage, cost, tool calls) to the tracer."""

    def __init__(self, tracer: Tracer, model: str, max_calls: int) -> None:
        from langchain_core.callbacks import BaseCallbackHandler

        outer = self

        class _H(BaseCallbackHandler):
            raise_error = True  # LangChain swallows callback errors unless the handler asks otherwise

            def on_chat_model_start(self, serialized: Any, messages: Any, **kw: Any) -> None:
                outer.t0 = time.time()
                outer.calls += 1
                if outer.calls > outer.max_calls:
                    raise RuntimeError(f"campaign model call limit ({outer.max_calls}) exceeded")
                if outer.repeats >= REPEAT_LIMIT:
                    raise RuntimeError(f"the model repeated the same tool call {outer.repeats} times in a row: {outer.last_sig}")

            def on_llm_end(self, response: Any, **kw: Any) -> None:
                for gens in response.generations:
                    for g in gens:
                        msg = getattr(g, "message", None)
                        meta = getattr(msg, "response_metadata", {}) or {}
                        tok = meta.get("token_usage") or {}
                        usage = dict(getattr(msg, "usage_metadata", None) or {})
                        sig = json.dumps([(c.get("name"), c.get("args")) for c in getattr(msg, "tool_calls", []) or []],
                                         sort_keys=True, default=str)
                        outer.repeats = outer.repeats + 1 if (sig == outer.last_sig and sig != "[]") else 1
                        outer.last_sig = sig
                        outer.tracer.log({
                            "node": "campaign", "provider": "openrouter" if outer.model != "fake" else "fake",
                            "model_requested": outer.model, "model_served": meta.get("model_name"),
                            "latency_s": round(time.time() - outer.t0, 2), "raw_content": str(getattr(msg, "content", ""))[:8000],
                            "tool_calls": [{"name": c.get("name"), "args": c.get("args")} for c in getattr(msg, "tool_calls", []) or []],
                            "parsed": "campaign-turn",
                            "usage": {k: usage.get(k) for k in ("input_tokens", "output_tokens", "total_tokens")},
                            "cost_usd": tok.get("cost"), "finish_reason": meta.get("finish_reason")})

            def on_llm_error(self, error: BaseException, **kw: Any) -> None:
                outer.tracer.log({"node": "campaign", "model_requested": outer.model, "parsed": None,
                                  "error": f"{type(error).__name__}: {error}"[:2000]})

        self.tracer, self.model, self.max_calls = tracer, model, max_calls
        self.calls, self.t0 = 0, time.time()
        self.repeats, self.last_sig = 0, ""
        self.handler = _H()


def make_campaign_chat(model: str, reasoning: str | None, callbacks: list[Any]) -> Any:
    """The campaign's chat model on OpenRouter (tool calling, ``tool_choice`` auto)."""
    import os

    from langchain_openai import ChatOpenAI

    from hw_dse.agent.llm import OPENROUTER_BASE_URL, openrouter_extra_body

    if not os.environ.get("OPENROUTER_API_KEY"):
        raise ValueError("OPENROUTER_API_KEY is not set")
    return ChatOpenAI(model=model, base_url=OPENROUTER_BASE_URL, api_key=os.environ["OPENROUTER_API_KEY"],
                      temperature=float(os.environ.get("HW_DSE_TEMPERATURE", "0.3")), max_tokens=8000, timeout=180,
                      max_retries=2, extra_body=openrouter_extra_body(reasoning), default_headers={"X-Title": "hw-dse"},
                      callbacks=callbacks)


def run_campaign(spec_names: list[str], *, seed: int = 0, chat: Any = None, model: str = "fake",
                 reasoning: str | None = None, architect: Any = None, memory: CampaignMemory | None = None,
                 run_root: Path | None = None, max_model_calls: int = 40, run_id: str | None = None) -> dict[str, Any]:
    """One campaign over ``spec_names`` (a queue, worked through in one agent run)."""
    from hw_dse.agent.llm import make_llm
    from hw_dse.agent.runner import REPO_ROOT
    from hw_dse.campaign.agent import build_campaign_agent

    stamp = time.strftime("%Y%m%d-%H%M%S") + f"-{uuid.uuid4().hex[:4]}"
    run_dir = (run_root or REPO_ROOT / "runs" / "campaign") / stamp
    run_dir.mkdir(parents=True, exist_ok=True)
    tracer = Tracer(run_dir / "llm_trace.jsonl")
    cb = TraceCallback(tracer, model, max_model_calls)
    if chat is None:
        chat = make_campaign_chat(model, reasoning, [cb.handler])
    else:
        chat.callbacks = [cb.handler]
    if architect is None:
        architect = make_llm("openrouter", model, tracer=tracer, reasoning=reasoning)
    else:
        architect.tracer = tracer
    memory = memory if memory is not None else CampaignMemory(enabled=False)
    ctx = CampaignContext.new(spec_names, run_dir, seed, architect, memory, run_id=run_id or stamp)
    agent = build_campaign_agent(chat, ctx)
    t0 = time.time()
    error = None
    final_text = ""
    try:
        out = agent.invoke({"messages": [{"role": "user", "content":
                            f"Campaign queue: {', '.join(spec_names)}. Seed {seed}. Start with recall and list_specs, "
                            "plan with write_todos, then take every spec down the ladder and finalize it."}]},
                           {"recursion_limit": 400})
        msgs = out.get("messages", [])
        final_text = str(msgs[-1].content)[:4000] if msgs else ""
        todos = out.get("todos")
    except Exception as exc:  # noqa: BLE001 - a failed campaign is a result, recorded as such
        error = f"{type(exc).__name__}: {exc}"[:2000]
        todos = None
    wall = time.time() - t0
    per_spec: dict[str, Any] = {}
    for name, led in ctx.specs.items():
        left_open = not led.finalized
        if left_open:
            t_finalize(ctx, name, "finalized by code after the campaign ended")
        sel = led.selected()
        logs = [r["rounds_log"] for r in led.dse_runs]
        if memory.enabled:
            memory.observe(ctx.run_id, led.spec, led.pool, led.front(), logs, led.back_annotation, led.l5)
        per_spec[name] = {
            "evaluations": led.pool, "used": led.used, "selected": sel, "left_open": left_open,
            "llm_declared_infeasible": any(r["llm_declared_infeasible"] for r in led.dse_runs) and not led.front(),
            "calls": led.calls, "dse_runs": [{k: v for k, v in r.items() if k != "rounds_log"} for r in led.dse_runs],
            "l2": {k: v for k, v in (led.l2 or {}).items() if k != "selected"} or None,
            "l3": led.l3, "l4": led.l4,
            "back_annotation": {k: led.back_annotation.get(k) for k in ("status", "winner_changed", "why")} if led.back_annotation else None,
            "l5": {k: v for k, v in (led.l5 or {}).items() if k != "selected"} or None,
            "final_note": led.final_note,
        }
    (run_dir / "tool_log.jsonl").write_text("\n".join(json.dumps(r, default=str) for r in ctx.log) + "\n")
    totals = tracer.totals()
    served = sorted({str(r.get("model_served")) for r in tracer.records if r.get("model_served")})
    return {"run_dir": str(run_dir), "run_id": ctx.run_id, "error": error, "wall_s": round(wall, 1), "per_spec": per_spec,
            "llm": totals, "campaign_model_calls": cb.calls, "tool_calls": ctx.tool_calls, "models_served": served,
            "final_text": final_text, "todos": todos}
