"""Every number in docs/WRITEUP.md comes from a committed source file.

The write-up declares its sources per section: an HTML comment
``<!-- sources: path [path ...] -->`` right under a heading applies to the
text up to the next heading. Every number in that text (outside code spans,
code blocks and mermaid diagrams) must appear in one of those files *at the
precision it is printed with*: "8.7%" is accepted if some number in the
sources rounds to 8.7 (or, for a fraction such as 0.0866, whose x100 does),
"635,040" if 635040 appears. Integers 0-10 are exempt (counts of things the
prose names, "two members", "5 seeds", "4 families"), and so are the
milestone and level labels (M1-M4, L0-L5) because they are not numbers.

So a number can be wrong only by matching some other figure in its own
section's sources at the same precision, and it cannot appear with no
source at all: a section without a sources line fails if it has any number.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITEUP = ROOT / "docs" / "WRITEUP.md"
NUM = re.compile(r"(?<![\w.^/=+-])[-+−]?\d[\d,]*(?:\.\d+)?(?![\w.]*\w)")
SRC_NUM = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    return re.sub(r"`[^`]*`", " ", text)


def sections(text: str) -> list[tuple[str, list[str], str]]:
    """(heading, sources, body) for every heading."""
    out = []
    parts = re.split(r"^(#{1,4} .*)$", text, flags=re.M)
    head = "(preamble)"
    for chunk in parts:
        if re.match(r"^#{1,4} ", chunk):
            head = chunk.strip()
            continue
        m = re.search(r"<!--\s*sources:\s*(.*?)-->", chunk, re.S)
        srcs = m.group(1).split() if m else []
        body = re.sub(r"<!--.*?-->", " ", chunk, flags=re.S)
        out.append((head, srcs, body))
    return out


@lru_cache(maxsize=None)
def source_numbers(path: str) -> frozenset[float]:
    p = ROOT / path
    assert p.exists(), f"declared source {path} does not exist"
    files = sorted(p.rglob("*")) if p.is_dir() else [p]
    vals: set[float] = set()
    for f in files:
        if f.is_file() and f.suffix in (".md", ".json", ".csv", ".yaml", ".yml", ".jsonl", ".txt"):
            for tok in SRC_NUM.findall(f.read_text(errors="ignore").replace(",", "")):
                try:
                    vals.add(float(tok))
                except ValueError:
                    pass
    return frozenset(vals)


def matches(token: str, vals: frozenset[float]) -> bool:
    t = token.replace(",", "").replace("−", "-").lstrip("+")
    x = float(t)
    if x.is_integer() and 0 <= x <= 10 and "." not in t:
        return True
    dec = len(t.split(".")[1]) if "." in t else 0
    for v in vals:
        for cand in (v, v * 100, -v, -v * 100):
            if round(cand, dec) == round(x, dec) and (dec > 0 or abs(cand - x) < 0.5 + 1e-9):
                return True
    return False


def test_writeup_exists_and_is_report_sized() -> None:
    words = len(re.findall(r"\w+", strip_code(WRITEUP.read_text())))
    assert 3000 <= words <= 5500, words


def test_every_number_has_a_source() -> None:
    text = WRITEUP.read_text()
    missing = []
    for head, srcs, body in sections(text):
        vals: frozenset[float] = frozenset().union(*[source_numbers(s) for s in srcs]) if srcs else frozenset()
        for tok in NUM.findall(strip_code(body)):
            if not matches(tok, vals):
                missing.append(f"{head}: {tok}" + ("" if srcs else " (section declares no sources)"))
    assert not missing, "numbers without a matching source:\n" + "\n".join(missing)


def test_the_checker_catches_an_unsourced_number() -> None:
    vals = source_numbers("eval/data/asic_calibration.md")
    assert matches("8.7", vals) and matches("57", vals)
    assert not matches("8.3141", vals)


def test_derived_facts_regenerate_identically() -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("writeup_facts", ROOT / "scripts" / "writeup_facts.py")
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    import json

    assert json.loads((ROOT / "docs" / "writeup_facts.json").read_text()) == json.loads(
        json.dumps(mod.facts(), sort_keys=True))
