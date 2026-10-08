"""JSONL trace of every LLM call, with secrets kept out by construction.

One line per LLM call: which node asked, which provider and model, the
exact prompt text, the raw reply, the parsed object (or parse error),
token usage, the provider-reported cost (OpenRouter returns it), latency
and the attempt number. The trace is what makes the run auditable: anyone
can check what the model was told and what it said, and that no number in
the report came from it.

Keeping secrets out
-------------------
Two layers:

1. **By construction**: the tracer is handed plain strings and dicts that
   :mod:`hw_dse.agent.llm` assembles field by field (message text, the
   parsed object, a usage dict). Client objects, request options and HTTP
   headers are never passed in, so an ``Authorization: Bearer`` header has
   no route into the file.
2. **Belt and braces**: before a line is written, every value of every
   environment variable whose name looks like a credential (``*_API_KEY``,
   ``*_TOKEN``, ``*_SECRET``) and anything shaped like a well-known key
   prefix is replaced with ``[REDACTED]``. ``tests/test_trace.py`` plants a
   fake key and checks it never reaches disk.
"""

from __future__ import annotations

import json
import os
import re
import threading
import time
from pathlib import Path
from typing import Any

_KEY_SHAPES = re.compile(r"(sk-or-v1-[A-Za-z0-9]{8,}|sk-ant-[A-Za-z0-9_\-]{8,}|sk-[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_\-]{20,})")
_SECRET_NAME = re.compile(r"(API_KEY|_TOKEN|_SECRET|PASSWORD)$", re.IGNORECASE)


def _secret_values() -> list[str]:
    vals = [v for k, v in os.environ.items() if _SECRET_NAME.search(k) and v and len(v) >= 8]
    return sorted(set(vals), key=len, reverse=True)


def redact(text: str) -> str:
    for v in _secret_values():
        text = text.replace(v, "[REDACTED]")
    return _KEY_SHAPES.sub("[REDACTED]", text)


class Tracer:
    """Append-only JSONL writer. ``path=None`` keeps records in memory only."""

    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path else None
        self.records: list[dict[str, Any]] = []
        self._lock = threading.Lock()
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, record: dict[str, Any]) -> None:
        record = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), **record}
        line = redact(json.dumps(record, default=str, ensure_ascii=False))
        with self._lock:
            self.records.append(json.loads(line))
            if self.path:
                with open(self.path, "a", encoding="utf-8") as fh:
                    fh.write(line + "\n")

    def totals(self) -> dict[str, float]:
        out = {"calls": 0.0, "input_tokens": 0.0, "output_tokens": 0.0, "cost_usd": 0.0, "failures": 0.0}
        for r in self.records:
            out["calls"] += 1
            u = r.get("usage") or {}
            out["input_tokens"] += float(u.get("input_tokens") or 0)
            out["output_tokens"] += float(u.get("output_tokens") or 0)
            out["cost_usd"] += float(r.get("cost_usd") or 0)
            out["failures"] += 0 if r.get("parsed") is not None else 1
        return out
