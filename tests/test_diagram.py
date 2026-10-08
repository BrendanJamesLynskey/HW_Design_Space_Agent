"""The README's Mermaid diagram must match the compiled graph.

Compares node and edge sets (not raw text) so cosmetic differences
between LangGraph versions do not cause false failures. Regenerate with
``python -m hw_dse.cli diagram`` and paste between the README markers.
"""

from __future__ import annotations

import re
from pathlib import Path

from hw_dse.cli import mermaid

README = Path(__file__).resolve().parents[1] / "README.md"
EDGE = re.compile(r"^\s*([\w]+)\s*(-->|-\.->)\s*([\w]+);?\s*$")


def edges(text: str) -> set[tuple[str, str, str]]:
    return {(m.group(1), m.group(2), m.group(3)) for line in text.splitlines() if (m := EDGE.match(line))}


def readme_block() -> str:
    text = README.read_text()
    start, end = "<!-- graph:start -->", "<!-- graph:end -->"
    assert start in text and end in text, "README is missing the graph markers"
    return text.split(start, 1)[1].split(end, 1)[0]


def test_readme_diagram_matches_graph() -> None:
    live = edges(mermaid())
    assert live, "no edges parsed from the live diagram"
    assert edges(readme_block()) == live
