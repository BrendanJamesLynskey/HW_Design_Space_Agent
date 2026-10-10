"""Every number in docs/WRITEUP.md is a named fact computed from committed data.

``scripts/writeup_facts.py`` builds ``docs/writeup_facts.json``: named facts,
each computed from the committed CSVs/JSONs or read from one named cell of a
code-generated report. Every section of the write-up declares the facts it
uses in an HTML comment right under its heading::

    <!-- facts: asic.loo_rms.area asic.loo_rms.fmax ab.qwen.single.* -->

(``*`` expands over fact names, for one table's cells.) The test requires:

1. every number in the section's text (outside code spans, code blocks and
   mermaid diagrams; parameter values such as ``m=3`` and versions such as
   ``3.1.0`` included, small integers included) to equal one of the section's
   declared facts at the precision it is printed with: "8.7" matches 8.66,
   "57" matches 57, "+14.8" matches 14.83; a version is compared as text;
2. every declared fact to be used at least once in its section, so a section
   cannot declare a wide pool;
3. the **negative test**: change the last digit of any one number and the
   check must fail for (almost) every such mutant; the few that survive are
   numbers whose neighbour value is also a declared fact of their section.

Not numbers, and so not checked: list markers ("1."), the milestone and level
labels (M1-M4, L0-L5) and model names ("Sonnet 5.5", "V4.1", "Qwen3.8-27B").
"""

from __future__ import annotations

import fnmatch
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WRITEUP = ROOT / "docs" / "WRITEUP.md"
FACTS = ROOT / "docs" / "writeup_facts.json"
NUM = re.compile(r"(?<![\w.^/\-−+])[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)*(?!\w)")
NOT_NUMBERS = (re.compile(r"Sonnet \d+\.\d+"), re.compile(r"^\s*\d+\.\s", re.M))
MAX_SURVIVING_MUTANTS = 0.03


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    for pat in NOT_NUMBERS:
        text = pat.sub(" ", text)
    return text


def sections(text: str) -> list[tuple[str, list[str], str]]:
    """(heading, declared fact patterns, body) for every heading."""
    out = []
    head = "(preamble)"
    for chunk in re.split(r"^(#{1,4} .*)$", text, flags=re.M):
        if re.match(r"^#{1,4} ", chunk):
            head = chunk.strip()
            continue
        m = re.search(r"<!--\s*facts:\s*(.*?)-->", chunk, re.S)
        keys = m.group(1).split() if m else []
        out.append((head, keys, re.sub(r"<!--.*?-->", " ", chunk, flags=re.S)))
    return out


def load_facts() -> dict[str, Any]:
    return json.loads(FACTS.read_text())


def expand(patterns: list[str], facts: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for p in patterns:
        hit = {k: v for k, v in facts.items() if fnmatch.fnmatchcase(k, p)}
        assert hit, f"declared fact {p!r} is not in {FACTS.name}"
        out.update(hit)
    return out


def _norm(token: str) -> str:
    return token.replace(",", "").replace("−", "-").lstrip("+")


def matches(token: str, value: Any) -> bool:
    """Is ``value`` what ``token`` prints, at the token's precision?"""
    t = _norm(token)
    if isinstance(value, str):
        return t == value
    if value is None or isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    if t.count(".") > 1:
        return False
    dec = len(t.split(".")[1]) if "." in t else 0
    return abs(float(value) - float(t)) <= 0.5 * 10 ** -dec + 1e-9


def tokens(body: str) -> list[str]:
    return NUM.findall(strip_code(body))


def mutate(token: str) -> str:
    """The same number with its last digit changed (9 -> 8, else +1)."""
    i = max(j for j, c in enumerate(token) if c.isdigit())
    d = int(token[i])
    return token[:i] + str(d - 1 if d == 9 else d + 1) + token[i + 1:]


def check(text: str, facts: dict[str, Any]) -> tuple[list[str], list[str]]:
    """(numbers with no matching fact, declared facts never used)."""
    missing, unused = [], []
    for head, pats, body in sections(text):
        decl = expand(pats, facts)
        used: set[str] = set()
        for tok in tokens(body):
            hit = [k for k, v in decl.items() if matches(tok, v)]
            if not hit:
                missing.append(f"{head}: {tok}" + ("" if pats else " (section declares no facts)"))
            used.update(hit)
        unused += [f"{head}: {k}" for k in decl if k not in used]
    return missing, unused


def test_writeup_exists_and_is_report_sized() -> None:
    words = len(re.findall(r"\w+", strip_code(WRITEUP.read_text())))
    assert 3000 <= words <= 5500, words


def test_every_number_is_a_declared_fact() -> None:
    missing, unused = check(WRITEUP.read_text(), load_facts())
    assert not missing, "numbers without a matching declared fact:\n" + "\n".join(missing)
    assert not unused, "declared facts the section never prints:\n" + "\n".join(unused)


def test_last_digit_mutants_are_caught() -> None:
    """The negative test: one changed digit anywhere must (almost always) fail the check."""
    facts = load_facts()
    total, survivors = 0, []
    for head, pats, body in sections(WRITEUP.read_text()):
        decl = expand(pats, facts)
        for tok in set(tokens(body)):
            total += 1
            mut = mutate(tok)
            if any(matches(mut, v) for v in decl.values()):
                survivors.append(f"{head}: {tok} -> {mut}")
    assert total > 200
    assert len(survivors) <= MAX_SURVIVING_MUTANTS * total, (
        f"{len(survivors)} of {total} mutants survive:\n" + "\n".join(survivors))


def test_the_checker_rejects_wrong_and_unsourced_numbers() -> None:
    facts = {"a": 8.66, "b": 57, "v": "3.1.0", "r": -14.93}
    text = "## S\n\n<!-- facts: a b v r -->\n\nRMS 8.7%, 57 points, OpenSTA 3.1.0, error −14.9%.\n"
    assert check(text, facts) == ([], [])
    for bad, tok in (("8.8%", "8.8"), ("58 points", "58"), ("3.1.1", "3.1.1"), ("−14.8%", "−14.8"), ("W=12", "12")):
        wrong = text.replace({"8.8%": "8.7%", "58 points": "57 points", "3.1.1": "3.1.0", "−14.8%": "−14.9%"}.get(bad, "57 points"),
                             bad if bad != "W=12" else "57 points, W=12")
        assert f"## S: {tok}" in check(wrong, facts)[0], bad
    assert check(text.replace("<!-- facts: a b v r -->", "<!-- facts: a b v r a -->").replace("8.7%", "8.7"), facts) == ([], [])
    assert check("## S\n\n<!-- facts: a b -->\n\n57 points.\n", facts)[1] == ["## S: a"]  # declared, never used
    assert check("## S\n\nno facts declared, 12 numbers.\n", facts)[0] == ["## S: 12 (section declares no facts)"]
    assert mutate("+14.8") == "+14.9" and mutate("635,040") == "635,041" and mutate("3.1.0") == "3.1.1"


def test_derived_facts_regenerate_identically() -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("writeup_facts", ROOT / "scripts" / "writeup_facts.py")
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    assert load_facts() == json.loads(json.dumps(mod.facts(), sort_keys=True))
