"""LLM providers behind one tiny interface: ``structured(schema, ...)``.

The graph needs exactly one capability from a language model: "here is a
system prompt and a user prompt, answer as an instance of this Pydantic
schema". :class:`StructuredLLM` is that interface, and :func:`make_llm` is
a small factory that builds one from environment variables:

==============  ==========================================  ======================
provider        backend                                     model env var
==============  ==========================================  ======================
``fake``        :class:`ScriptedLLM` / :class:`HeuristicArchitect`  (none)
``anthropic``   ``langchain_anthropic.ChatAnthropic``        ``ANTHROPIC_MODEL``
``openai``      ``langchain_openai.ChatOpenAI``              ``OPENAI_MODEL``
``gemini``      ``langchain_google_genai``                   ``GEMINI_MODEL``
``ollama``      ``langchain_ollama.ChatOllama`` (local)      ``OLLAMA_MODEL``
``openrouter``  ``ChatOpenAI`` at openrouter.ai/api/v1       ``OPENROUTER_MODEL``
==============  ==========================================  ======================

``HW_DSE_PROVIDER`` picks the provider (default ``fake``); ``HW_DSE_MODEL``
overrides the per-provider model variable. Provider packages are imported
lazily inside the factory, so the core package and the whole test suite
need none of them.

OpenRouter is OpenAI-compatible, so it is just ``ChatOpenAI`` with a
different ``base_url`` and ``OPENROUTER_API_KEY``. Two OpenRouter request
options are set through ``extra_body``: ``usage: {include: true}`` so each
response reports its cost, and, if ``OPENROUTER_REASONING`` is set,
``reasoning`` (``off`` sends ``{"enabled": false}``; ``low``/``medium``/
``high`` set the effort). Some "thinking" models wrap or delay their JSON
when reasoning is on; switching it off is the documented fix and is
recorded in the trace.

Keys are read from the environment and handed straight to the client
object. They are never logged: the tracer only receives message text,
parsed objects and usage numbers (see :mod:`hw_dse.agent.trace`).

The fakes
---------
:class:`ScriptedLLM` replays a fixed list of answers, which is what the
tests use: graph behaviour is tested against *known* LLM decisions, so no
test ever depends on a real model's output. :class:`HeuristicArchitect`
is a small rule-based stand-in for demos and CI smoke runs. Both are
labelled ``fake`` in every trace and report; the eval refuses to put fake
results in the agent column.
"""

from __future__ import annotations

import json
import math
import os
import time
from collections.abc import Callable
from typing import Any, Protocol, TypeVar

from pydantic import BaseModel

from hw_dse.agent.schemas import AnalysisDecision, ExplorationPlan, FamilyPlan, ParamRange
from hw_dse.agent.trace import Tracer

T = TypeVar("T", bound=BaseModel)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODELS = {
    "openrouter": "anthropic/claude-sonnet-5.5",
    "anthropic": "claude-sonnet-5-5",
}


class StructuredOutputError(RuntimeError):
    pass


class StructuredLLM(Protocol):
    provider: str
    model: str
    tracer: Tracer

    def structured(self, schema: type[T], system: str, user: str, *, node: str, context: dict[str, Any] | None = None) -> T:
        ...


# ---------------------------------------------------------------------------
# Real providers via LangChain chat models
# ---------------------------------------------------------------------------

class LangChainLLM:
    """Wrap a LangChain chat model; ask for structured output; trace it."""

    def __init__(self, chat: Any, provider: str, model: str, method: str, tracer: Tracer | None = None,
                 settings: dict[str, Any] | None = None, retries: int = 2) -> None:
        self.chat = chat
        self.provider = provider
        self.model = model
        self.method = method
        self.tracer = tracer or Tracer()
        self.settings = settings or {}  # non-secret request settings, recorded in the trace
        self.retries = retries

    def structured(self, schema: type[T], system: str, user: str, *, node: str, context: dict[str, Any] | None = None) -> T:
        from langchain_core.messages import HumanMessage, SystemMessage

        runnable = self.chat.with_structured_output(schema, method=self.method, include_raw=True)
        note = ""
        last_err = ""
        for attempt in range(1, self.retries + 1):
            msgs = [SystemMessage(content=system), HumanMessage(content=user + note)]
            t0 = time.time()
            rec: dict[str, Any] = {
                "node": node,
                "provider": self.provider,
                "model_requested": self.model,
                "schema": schema.__name__,
                "method": self.method,
                "settings": self.settings,
                "attempt": attempt,
                "system": system,
                "user": user + note,
            }
            try:
                out = runnable.invoke(msgs)
            except Exception as exc:  # noqa: BLE001 - provider/network errors: trace and retry
                rec.update(latency_s=round(time.time() - t0, 2), error=f"{type(exc).__name__}: {exc}"[:2000], parsed=None)
                self.tracer.log(rec)
                last_err = rec["error"]
                # Schema validation errors can surface as exceptions (JSON-schema
                # mode); tell the model what was wrong so the retry can fix it.
                note = (
                    "\n\nYour previous reply failed validation against the required schema "
                    f"({str(exc)[:300]}). Reply again using exactly the required structure."
                    if "ValidationError" in type(exc).__name__ else ""
                )
                continue
            raw = out.get("raw")
            parsed = out.get("parsed")
            perr = out.get("parsing_error")
            meta = getattr(raw, "response_metadata", {}) or {}
            tok = meta.get("token_usage") or {}
            usage = dict(getattr(raw, "usage_metadata", None) or {})
            reasoning_tokens = (tok.get("completion_tokens_details") or {}).get("reasoning_tokens")
            rec.update(
                latency_s=round(time.time() - t0, 2),
                model_served=meta.get("model_name") or meta.get("model"),
                raw_content=_raw_text(raw),
                parsed=parsed.model_dump() if parsed is not None else None,
                parse_error=str(perr)[:2000] if perr else None,
                usage={k: usage.get(k) for k in ("input_tokens", "output_tokens", "total_tokens")},
                reasoning_tokens=reasoning_tokens,
                cost_usd=tok.get("cost"),
                finish_reason=meta.get("finish_reason"),
            )
            self.tracer.log(rec)
            if parsed is not None:
                return parsed  # type: ignore[no-any-return]
            last_err = str(perr)
            note = (
                "\n\nYour previous reply could not be parsed against the required schema "
                f"({str(perr)[:300]}). Reply again using exactly the required structure."
            )
        raise StructuredOutputError(f"{self.provider}:{self.model} failed to produce {schema.__name__}: {last_err[:500]}")


def _raw_text(raw: Any) -> str:
    if raw is None:
        return ""
    parts = []
    content = getattr(raw, "content", "")
    if isinstance(content, list):
        content = json.dumps(content, default=str)
    if content:
        parts.append(str(content))
    for tc in getattr(raw, "tool_calls", None) or []:
        parts.append(json.dumps({"tool": tc.get("name"), "args": tc.get("args")}, default=str))
    return "\n".join(parts)[:20000]


def _env_model(provider: str, model: str | None) -> str:
    m = model or os.environ.get("HW_DSE_MODEL") or os.environ.get(f"{provider.upper()}_MODEL") or DEFAULT_MODELS.get(provider)
    if not m:
        raise ValueError(f"set {provider.upper()}_MODEL (or HW_DSE_MODEL) to choose a {provider} model")
    return m


def openrouter_extra_body(reasoning: str | None) -> dict[str, Any]:
    body: dict[str, Any] = {"usage": {"include": True}}
    if reasoning:
        body["reasoning"] = {"enabled": False} if reasoning == "off" else {"effort": reasoning}
    return body


def make_llm(provider: str | None = None, model: str | None = None, tracer: Tracer | None = None,
             reasoning: str | None = None, method: str | None = None) -> StructuredLLM:
    """Build a StructuredLLM from arguments or environment variables."""
    provider = (provider or os.environ.get("HW_DSE_PROVIDER") or "fake").lower()
    tracer = tracer or Tracer()
    temperature = float(os.environ.get("HW_DSE_TEMPERATURE", "0.3"))
    # OpenRouter: use the provider's structured_outputs (JSON schema) mode.
    # Forced tool_choice is rejected by some routes (e.g. Claude Sonnet 5.5
    # with extended thinking), while JSON-schema output works for every model
    # we evaluate. Other providers default to tool calling.
    method = method or os.environ.get("HW_DSE_STRUCTURED_METHOD") or ("json_schema" if provider == "openrouter" else "function_calling")

    if provider == "fake":
        return HeuristicArchitect(tracer=tracer)

    if provider == "openrouter":
        from langchain_openai import ChatOpenAI

        if not os.environ.get("OPENROUTER_API_KEY"):
            raise ValueError("OPENROUTER_API_KEY is not set")
        m = _env_model("openrouter", model)
        reasoning = reasoning if reasoning is not None else os.environ.get("OPENROUTER_REASONING") or None
        chat = ChatOpenAI(
            model=m,
            base_url=OPENROUTER_BASE_URL,
            api_key=os.environ["OPENROUTER_API_KEY"],
            temperature=temperature,
            max_tokens=int(os.environ.get("HW_DSE_MAX_TOKENS", "16000")),  # room for reasoning tokens
            timeout=180,
            max_retries=2,
            extra_body=openrouter_extra_body(reasoning),
            default_headers={"X-Title": "hw-dse"},
        )
        settings = {"temperature": temperature, "reasoning": reasoning or "provider default", "base_url": OPENROUTER_BASE_URL}
        return LangChainLLM(chat, "openrouter", m, method, tracer, settings)

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        m = _env_model("openai", model)
        return LangChainLLM(ChatOpenAI(model=m, temperature=temperature, timeout=180), "openai", m, method, tracer,
                            {"temperature": temperature})

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        m = _env_model("anthropic", model)
        return LangChainLLM(ChatAnthropic(model=m, temperature=temperature, max_tokens=4096, timeout=180), "anthropic", m,
                            method, tracer, {"temperature": temperature})

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        m = _env_model("gemini", model)
        return LangChainLLM(ChatGoogleGenerativeAI(model=m, temperature=temperature), "gemini", m, method, tracer,
                            {"temperature": temperature})

    if provider == "ollama":
        from langchain_ollama import ChatOllama

        m = _env_model("ollama", model)
        return LangChainLLM(ChatOllama(model=m, temperature=temperature), "ollama", m, method, tracer,
                            {"temperature": temperature})

    raise ValueError(f"unknown provider {provider!r}; choose fake, anthropic, openai, gemini, ollama or openrouter")


# ---------------------------------------------------------------------------
# Fakes (tests and demos). Never used for eval agent results.
# ---------------------------------------------------------------------------

Answer = BaseModel | Callable[[type[BaseModel], dict[str, Any]], BaseModel]


class ScriptedLLM:
    """Replays a fixed sequence of answers, checking each matches the schema."""

    provider = "fake"
    model = "scripted"

    def __init__(self, answers: list[Answer], tracer: Tracer | None = None) -> None:
        self.answers = list(answers)
        self.tracer = tracer or Tracer()
        self.calls: list[tuple[str, str]] = []

    def structured(self, schema: type[T], system: str, user: str, *, node: str, context: dict[str, Any] | None = None) -> T:
        if not self.answers:
            raise StructuredOutputError(f"ScriptedLLM ran out of answers at node {node}")
        ans = self.answers.pop(0)
        obj = ans(schema, context or {}) if callable(ans) and not isinstance(ans, BaseModel) else ans
        if not isinstance(obj, schema):
            raise StructuredOutputError(f"script expected {schema.__name__} at {node}, got {type(obj).__name__}")
        self.calls.append((node, schema.__name__))
        self.tracer.log({"node": node, "provider": "fake", "model_requested": "scripted", "schema": schema.__name__,
                         "system": system, "user": user, "parsed": obj.model_dump(), "usage": {}, "cost_usd": 0.0})
        return obj  # type: ignore[return-value]


class HeuristicArchitect:
    """A deterministic rule-based 'architect' for demos and smoke runs.

    It reads the same context the real LLM gets (as a dict) and applies a
    few textbook rules: pipelined families for high rates, FSM families for
    low rates, data width from the accuracy target, refine once around the
    front, declare infeasible if two rounds find nothing feasible. It is
    *not* an LLM and is always labelled ``fake``.
    """

    provider = "fake"
    model = "heuristic-architect"

    def __init__(self, tracer: Tracer | None = None) -> None:
        self.tracer = tracer or Tracer()

    def structured(self, schema: type[T], system: str, user: str, *, node: str, context: dict[str, Any] | None = None) -> T:
        ctx = context or {}
        if schema is ExplorationPlan:
            obj: BaseModel = self._initial_plan(ctx)
        elif schema is AnalysisDecision:
            obj = self._decide(ctx)
        else:
            raise StructuredOutputError(f"HeuristicArchitect cannot produce {schema.__name__}; use a YAML spec")
        self.tracer.log({"node": node, "provider": "fake", "model_requested": self.model, "schema": schema.__name__,
                         "system": system, "user": user, "parsed": obj.model_dump(), "usage": {}, "cost_usd": 0.0})
        return obj  # type: ignore[return-value]

    @staticmethod
    def _width_range(ctx: dict[str, Any]) -> tuple[int, int]:
        err = ctx.get("max_abs_err")
        bits = -math.log2(err) if err else 12
        lo = max(8, min(28, int(math.ceil(bits)) + 1))
        return lo, min(28, lo + 5)

    def _initial_plan(self, ctx: dict[str, Any]) -> ExplorationPlan:
        thr = ctx.get("min_throughput_msps") or 0.0
        wlo, whi = self._width_range(ctx)
        common = [ParamRange(param="data_width", low=wlo, high=whi),
                  ParamRange(param="n_iter", low=max(4, wlo - 2), high=min(30, whi + 3))]
        if thr >= 100:
            fams = ["pipelined", "pipelined_m"]
        elif thr >= 20:
            fams = ["pipelined_m", "iterative", "unrolled_k"]
        else:
            fams = ["iterative", "unrolled_k"]
        return ExplorationPlan(
            families=[FamilyPlan(family=f, ranges=common, why=f"rule: throughput {thr:g} MSPS") for f in fams],  # type: ignore[arg-type]
            rationale="Heuristic: family from the throughput requirement, width from the accuracy target.",
        )

    def _decide(self, ctx: dict[str, Any]) -> AnalysisDecision:
        rnd, n_feas = int(ctx.get("round", 1)), int(ctx.get("n_feasible", 0))
        if n_feas == 0:
            if rnd >= 2:
                return AnalysisDecision(decision="infeasible", rationale="Two rounds, no feasible design in any family.")
            fams = ["iterative", "unrolled_k", "pipelined", "pipelined_m"]
            return AnalysisDecision(
                decision="widen",
                rationale="Nothing feasible yet: search every family over full ranges.",
                next_plan=ExplorationPlan(families=[FamilyPlan(family=f, why="widen") for f in fams],  # type: ignore[arg-type]
                                          rationale="full ranges"),
            )
        if rnd == 1 and ctx.get("front_boxes"):
            fams = [FamilyPlan(family=f, ranges=[ParamRange(**r) for r in rs], why="refine around front")
                    for f, rs in ctx["front_boxes"].items()]
            return AnalysisDecision(decision="refine", rationale="Refine around the front.",
                                    next_plan=ExplorationPlan(families=fams[:4], rationale="refine"))
        return AnalysisDecision(decision="stop", rationale="Front found and refined once.")


class ReplayArchitect:
    """Replays the decisions a *real* LLM made in a recorded run (offline lever tuning).

    It reads a recorded ``llm_trace.jsonl`` and answers each ``propose`` /
    ``analyse`` call with the parsed object the live model returned for the
    same call in the same order. A call whose attempts all failed in the
    recording raises :class:`StructuredOutputError` again, as it did live. If
    the graph asks for more decisions than were recorded (because a lever
    changed the control flow), it answers ``stop``.

    This lets deterministic code (the whole-curve levers) be tuned against
    how the evaluated LLMs actually behaved, at zero cost and with no live
    calls. It is labelled ``fake`` like the other stand-ins and never feeds
    the eval's agent columns.
    """

    provider = "fake"

    def __init__(self, trace_path: str, tracer: Tracer | None = None) -> None:
        import ast
        from pathlib import Path

        self.model = f"replay:{Path(trace_path).parent.name}"
        self.tracer = tracer or Tracer()
        calls: list[list[dict[str, Any]]] = []
        for line in Path(trace_path).read_text().splitlines():
            r = json.loads(line)
            if r.get("node") not in ("propose", "analyse"):
                continue
            if int(r.get("attempt") or 1) == 1 or not calls or calls[-1][0]["node"] != r["node"]:
                calls.append([])
            parsed = r.get("parsed")
            if isinstance(parsed, str):
                parsed = ast.literal_eval(parsed)
            calls[-1].append({**r, "parsed": parsed})
        self.calls = calls
        self.served = 0

    def structured(self, schema: type[T], system: str, user: str, *, node: str, context: dict[str, Any] | None = None) -> T:
        if self.served >= len(self.calls):
            if schema is AnalysisDecision:
                obj: BaseModel = AnalysisDecision(decision="stop", rationale="[replay: no further recorded decision]")
                self.tracer.log({"node": node, "provider": "fake", "model_requested": self.model, "parsed": obj.model_dump()})
                return obj  # type: ignore[return-value]
            raise StructuredOutputError("replay exhausted")
        call = self.calls[self.served]
        self.served += 1
        if call[0]["node"] != node:
            raise StructuredOutputError(f"replay out of step: recorded {call[0]['node']}, asked {node}")
        ok = [c["parsed"] for c in call if c.get("parsed") is not None]
        if not ok:
            raise StructuredOutputError("recorded call failed live")
        obj = schema.model_validate(ok[-1])
        self.tracer.log({"node": node, "provider": "fake", "model_requested": self.model, "schema": schema.__name__,
                         "parsed": obj.model_dump(), "usage": {}, "cost_usd": 0.0})
        return obj  # type: ignore[return-value]
