"""Every number in docs/WRITEUP.md is a named fact computed from committed data.

``scripts/writeup_facts.py`` builds ``docs/writeup_facts.json``: named facts,
each computed from the committed CSVs/JSONs or read from one named cell of a
code-generated report. Every section of the write-up binds its numbers to
facts in an HTML comment right under its heading, **one fact name per number,
in reading order**::

    <!-- facts: asic.loo_rms.area asic.loo_rms.ffs asic.loo_rms.fmax -->

The test requires:

1. the section to print exactly as many numbers as it names facts, and the
   i-th number (outside code spans, code blocks and mermaid diagrams;
   parameter values such as ``m=3``, versions such as ``3.1.0`` and small
   integers included) to equal the i-th fact at the precision it is printed
   with: "8.7" matches 8.66, "57" matches 57, "+14.8" matches 14.83; a version
   is compared as text;
2. the **negative test**: change the last digit of any number and the check
   fails, for every number in the write-up (a changed digit is a different
   value at the same precision, so it cannot match the same fact).

``python scripts/writeup_facts.py --bind`` writes the ordered lists from a
pool of facts while editing.

Not numbers, and so not checked: list markers ("1."), the milestone and level
labels (M1-M4, L0-L5, "phase 2") and model names ("Sonnet 5.5", "V4.1", "Qwen3.8-27B").
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
NOT_NUMBERS = (re.compile(r"Sonnet \d+\.\d+"), re.compile(r"^\s*\d+\.\s", re.M), re.compile(r"\b[Pp]hase \d\b"))


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
    """A pool of facts from names and ``*`` globs (for ``--bind``)."""
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


def check(text: str, facts: dict[str, Any]) -> list[str]:
    """Every problem: a number that does not equal its bound fact, a count mismatch, an unknown fact."""
    errors = []
    for head, keys, body in sections(text):
        toks = tokens(body)
        for k in keys:
            if k not in facts:
                errors.append(f"{head}: unknown fact {k!r}")
        if len(toks) != len(keys):
            errors.append(f"{head}: {len(toks)} numbers but {len(keys)} facts"
                          + ("" if keys else " (section binds no facts)"))
        for tok, k in zip(toks, keys):
            if k in facts and not matches(tok, facts[k]):
                errors.append(f"{head}: {tok} is not {k} = {facts[k]!r}")
    return errors


def test_writeup_exists_and_is_report_sized() -> None:
    words = len(re.findall(r"\w+", strip_code(WRITEUP.read_text())))
    assert 3000 <= words <= 5500, words


def test_every_number_is_its_bound_fact() -> None:
    errors = check(WRITEUP.read_text(), load_facts())
    assert not errors, "\n".join(errors)


def test_last_digit_mutants_are_caught() -> None:
    """The negative test: change one digit of any number in the write-up and its check fails."""
    facts = load_facts()
    total, survivors = 0, []
    for head, keys, body in sections(WRITEUP.read_text()):
        for tok, k in zip(tokens(body), keys):
            total += 1
            if matches(mutate(tok), facts[k]):
                survivors.append(f"{head}: {tok} -> {mutate(tok)} still matches {k}")
    assert total > 250, total
    assert not survivors, f"{len(survivors)} of {total} mutants survive:\n" + "\n".join(survivors)


def test_the_checker_rejects_wrong_swapped_and_unbound_numbers() -> None:
    facts = {"a": 8.66, "b": 57, "v": "3.1.0", "r": -14.93, "c": 58}
    text = "## S\n\n<!-- facts: a b v r -->\n\nRMS 8.7%, 57 points, OpenSTA 3.1.0, error −14.9%.\n"
    assert check(text, facts) == []
    for old, new in (("8.7%", "8.8%"), ("57 points", "58 points"), ("3.1.0", "3.1.1"), ("−14.9%", "−14.8%")):
        assert check(text.replace(old, new), facts), new
    assert check(text.replace("57 points", "57 points, W=12"), facts)  # an extra, unbound number
    assert check(text.replace("<!-- facts: a b v r -->", "<!-- facts: b a v r -->"), facts)  # swapped binding
    assert check(text.replace("57 points", "58 points").replace("a b v r", "a c v r"), facts) == []
    assert check("## S\n\nno facts bound, 12 numbers.\n", facts) == ["## S: 1 numbers but 0 facts (section binds no facts)"]
    assert check(text.replace(" b ", " zz "), facts)[0] == "## S: unknown fact 'zz'"
    assert mutate("+14.8") == "+14.9" and mutate("635,040") == "635,041" and mutate("3.1.0") == "3.1.1"


def test_derived_facts_regenerate_identically() -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("writeup_facts", ROOT / "scripts" / "writeup_facts.py")
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    assert load_facts() == json.loads(json.dumps(mod.facts(), sort_keys=True))
