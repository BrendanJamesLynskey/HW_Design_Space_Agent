"""Provider factory (lazy, env-driven) and secret-free tracing."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from hw_dse.agent.llm import HeuristicArchitect, make_llm, openrouter_extra_body
from hw_dse.agent.trace import Tracer, redact

FAKE_KEY = "sk-or-v1-0123456789abcdef0123456789abcdef"


def test_default_provider_is_fake(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("HW_DSE_PROVIDER", raising=False)
    assert isinstance(make_llm(), HeuristicArchitect)


def test_unknown_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(ValueError):
        make_llm("telepathy")


def test_openrouter_requires_key(monkeypatch: pytest.MonkeyPatch) -> None:
    pytest.importorskip("langchain_openai")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    with pytest.raises(ValueError):
        make_llm("openrouter", "some/model")


@pytest.mark.skipif(importlib.util.find_spec("langchain_openai") is None, reason="langchain-openai not installed")
def test_openrouter_client_config(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", FAKE_KEY)
    llm = make_llm("openrouter", "qwen/qwen3.8-27b", reasoning="off")
    assert llm.provider == "openrouter" and llm.model == "qwen/qwen3.8-27b"
    assert str(llm.chat.openai_api_base).startswith("https://openrouter.ai/api/v1")
    assert llm.chat.extra_body == {"usage": {"include": True}, "reasoning": {"enabled": False}}
    # The key is held as a secret and never appears in the recorded settings.
    assert FAKE_KEY not in json.dumps(llm.settings)
    assert FAKE_KEY not in repr(llm.chat)


def test_extra_body_effort() -> None:
    assert openrouter_extra_body("low")["reasoning"] == {"effort": "low"}
    assert "reasoning" not in openrouter_extra_body(None)


def test_tracer_redacts_secrets(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", FAKE_KEY)
    monkeypatch.setenv("SOME_SERVICE_TOKEN", "tok-very-secret-value")
    t = Tracer(tmp_path / "t.jsonl")
    t.log({"user": f"Authorization: Bearer {FAKE_KEY}", "nested": {"x": "tok-very-secret-value"},
           "other": "sk-ant-abcdefghijklmnop"})
    text = (tmp_path / "t.jsonl").read_text()
    assert FAKE_KEY not in text and "tok-very-secret-value" not in text and "sk-ant-abcdefghij" not in text
    assert text.count("[REDACTED]") == 3
    assert redact("nothing secret") == "nothing secret"
