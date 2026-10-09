"""A scripted chat model for offline campaign tests (no LLM output needed).

:class:`ScriptedChatModel` is a LangChain chat model that answers each call
with the next message from a script. A scripted message can request tool
calls (``tool("run_dse", spec_name=..., evals=...)``), so a test fixes the
campaign agent's *decisions* and checks what the harness and our tools do
with them: budget enforcement, memory reads and writes, the forced re-plan
after a winner change, the memory-off switch. A script entry may also be a
function of the conversation so far (to branch on a tool's answer).

It is labelled ``fake`` everywhere and never feeds the eval's columns.
"""

from __future__ import annotations

import itertools
from collections.abc import Callable
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult

_ids = itertools.count()


def tool(name: str, **args: Any) -> dict[str, Any]:
    return {"name": name, "args": args, "id": f"call_{next(_ids)}", "type": "tool_call"}


def say(text: str = "", *calls: dict[str, Any]) -> AIMessage:
    return AIMessage(content=text, tool_calls=list(calls))


class ScriptedChatModel(BaseChatModel):
    """Replays scripted AI messages; ``bind_tools`` is accepted and ignored."""

    script: list[Any] = []
    seen: list[list[BaseMessage]] = []
    model_name: str = "scripted-campaign"

    @property
    def _llm_type(self) -> str:
        return "scripted"

    def bind_tools(self, tools: Any, **kwargs: Any) -> ScriptedChatModel:  # noqa: ARG002
        return self

    def _generate(self, messages: list[BaseMessage], stop: Any = None, run_manager: Any = None,
                  **kwargs: Any) -> ChatResult:
        self.seen.append(list(messages))
        if not self.script:
            msg: AIMessage = AIMessage(content="[script exhausted]")
        else:
            nxt = self.script.pop(0)
            msg = nxt(messages) if isinstance(nxt, Callable) else nxt  # type: ignore[arg-type]
        msg = msg.model_copy(update={"usage_metadata": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}})
        return ChatResult(generations=[ChatGeneration(message=msg)])
