"""Cross-run memory for the campaign agent, kept in a LangGraph Store.

What gets remembered
--------------------
Three kinds of lesson, each stored under ``("hw_dse", "memory", <kind>)``
with a key, a text and **the run IDs it came from**:

``family``
    Per architecture family, from code: in which specs it was explored, how
    many evaluations it got and whether it reached the front, e.g.
    "``unrolled_k``: explored in 3 specs (178 evaluations), on the front in 0;
    never reached a front on this device".
``spec_class``
    Per class of spec (rate band x system kind), from code: whether the
    front-mapping rounds paid, as the hypervolume gain they produced in
    those runs.
``calibration``
    From code: every back-annotation verdict (which tool, which design,
    winner changed or not, why) and every L5 re-selection.
``note``
    Free-text notes the campaign LLM chose to keep (``remember`` tool),
    labelled as LLM-authored, with every number masked (:func:`mask_numbers`):
    they are advice for the next campaign, never data. (In the M3 live eval the
    notes still carried numbers copied from tool outputs; masking was added
    after review.)

Code-derived lessons are recomputed from the accumulated *observations*
(also in the Store, namespace ``("hw_dse", "observations")``), so a lesson's
numbers always come from code. Memory can be switched off
(``enabled=False``): then nothing is read or written and the agent's tools
say so. ``save`` / ``load`` turn the Store's contents into the JSON file the
eval commits.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

from langgraph.store.memory import InMemoryStore

KINDS = ("family", "spec_class", "calibration", "note")

# Every digit run, including one glued to letters (W15, p99, M1): a sign or ~ is
# taken only when it does not join two tokens.
_NUMBER = re.compile(r"(?:(?<![A-Za-z0-9_])[-+~≈])?\d+(?:[.,]\d+)*(?:\s*%)?")


def mask_numbers(text: str) -> str:
    """Replace every number in LLM-authored text with ``#``.

    The LLM never produces a number, and that includes a number it *restates*:
    a campaign note copied from a tool output can garble it (M3 review, S5: a
    note gave Vivado-scale percentages next to a raw measurement pair). Notes
    keep the reasoning; numbers stay in code-written lessons and tool outputs,
    where they carry provenance."""
    return _NUMBER.sub("#", text)


def spec_class(spec: Any) -> str:
    thr = spec.min_throughput_msps or 0.0
    band = "high-rate (>= 100 MSPS)" if thr >= 100 else ("mid-rate (10-100 MSPS)" if thr >= 10 else "low-rate (< 10 MSPS)")
    return band + (f", system: {spec.system.kind}" if spec.system is not None else ", no system scenario")


class CampaignMemory:
    """A thin, typed layer over a LangGraph :class:`InMemoryStore`."""

    def __init__(self, enabled: bool = True, store: InMemoryStore | None = None) -> None:
        self.enabled = enabled
        self.store = store or InMemoryStore()

    # -- raw access ----------------------------------------------------
    def _put(self, ns: tuple[str, ...], key: str, value: dict[str, Any]) -> None:
        self.store.put(ns, key, value)

    def _all(self, ns: tuple[str, ...]) -> list[Any]:
        return list(self.store.search(ns, limit=10_000))

    # -- lessons ---------------------------------------------------------
    def remember(self, kind: str, key: str, lesson: str, run_ids: list[str], author: str) -> str:
        if not self.enabled:
            return "memory is switched off for this campaign; nothing was stored"
        if kind not in KINDS:
            return f"unknown kind {kind!r}; use one of {KINDS}"
        if author == "llm":
            key, lesson = mask_numbers(key), mask_numbers(lesson)
        ns = ("hw_dse", "memory", kind)
        old = self.store.get(ns, key)
        ids = sorted(set((old.value.get("run_ids", []) if old else []) + list(run_ids)))
        self._put(ns, key, {"lesson": lesson, "run_ids": ids, "author": author,
                            "updated": time.strftime("%Y-%m-%dT%H:%M:%S")})
        return f"stored {kind}/{key} (from runs {', '.join(ids)})"

    def lessons(self, kinds: tuple[str, ...] = KINDS) -> list[dict[str, Any]]:
        if not self.enabled:
            return []
        out = []
        for k in kinds:
            for it in self._all(("hw_dse", "memory", k)):
                out.append({"kind": k, "key": it.key, **it.value})
        return sorted(out, key=lambda r: (KINDS.index(r["kind"]), r["key"]))

    def digest(self) -> str:
        """The lessons as text, for the campaign agent's prompt."""
        ls = self.lessons()
        if not ls:
            return "(no lessons yet)" if self.enabled else "(memory is switched off)"
        lines = []
        for r in ls:
            who = "LLM note" if r["author"] == "llm" else "code"
            lines.append(f"- [{r['kind']}/{r['key']}] {r['lesson']} ({who}; runs {', '.join(r['run_ids'])})")
        return "\n".join(lines)

    # -- observations -> code-derived lessons ------------------------------
    def observe(self, run_id: str, spec: Any, pool: list[dict[str, Any]], front: list[dict[str, Any]],
                rounds_logs: list[list[dict[str, Any]]], back_annotation: dict[str, Any] | None,
                l5: dict[str, Any] | None) -> list[str]:
        """Record what code saw in one spec of a campaign and refresh the code lessons."""
        if not self.enabled:
            return []
        from hw_dse.families import REGISTRY

        written = []
        on_front = {r["family"] for r in front}
        for fam in REGISTRY:
            n = sum(r["family"] == fam for r in pool)
            if n:
                self._put(("hw_dse", "observations", "family"), f"{run_id}|{spec.name}|{fam}",
                          {"family": fam, "spec": spec.name, "evals": n, "on_front": fam in on_front, "run_id": run_id})
        # front-mapping rounds: HV gain of each code/LLM mapping round, from the rounds logs
        gains = []
        for log in rounds_logs:
            for i, rl in enumerate(log):
                kind = (rl.get("plan") or {}).get("kind")
                if kind == "coverage" and i > 0 and log[i - 1]["hv"] > 0:
                    gains.append(rl["hv"] / log[i - 1]["hv"] - 1.0)
        self._put(("hw_dse", "observations", "spec_class"), f"{run_id}|{spec.name}",
                  {"class": spec_class(spec), "spec": spec.name, "mapping_gains": gains, "run_id": run_id})
        if back_annotation and back_annotation.get("status") == "compared":
            l5txt = ""
            if l5 and l5.get("status") == "reexplored":
                l5txt = (f"; L5 re-exploration under {l5['calibration']} selected {l5['selected_key']}"
                         f" ({'changed' if l5['changed'] else 'unchanged'})")
            self.remember("calibration", f"{spec.name}|{back_annotation['selected_key']}",
                          f"{spec.name}: {back_annotation['why']}{l5txt}", [run_id], "code")
            written.append("calibration")
        written += self._refresh_code_lessons()
        return written

    def _refresh_code_lessons(self) -> list[str]:
        from hw_dse.families import REGISTRY

        obs = [it.value for it in self._all(("hw_dse", "observations", "family"))]
        written = []
        for fam in REGISTRY:
            mine = [o for o in obs if o["family"] == fam]
            if not mine:
                continue
            specs = sorted({o["spec"] for o in mine})
            fronts = sorted({o["spec"] for o in mine if o["on_front"]})
            ev = sum(o["evals"] for o in mine)
            tail = "; never reached a front on this device so far" if not fronts else f"; on the front in {', '.join(fronts)}"
            self.remember("family", fam, f"`{fam}`: explored in {len(specs)} spec(s) ({ev} evaluations), on the front in "
                          f"{len(fronts)}{tail}", sorted({o["run_id"] for o in mine}), "code")
            written.append(f"family/{fam}")
        sc = [it.value for it in self._all(("hw_dse", "observations", "spec_class"))]
        for cls in sorted({o["class"] for o in sc}):
            mine = [o for o in sc if o["class"] == cls]
            g = [x for o in mine for x in o["mapping_gains"]]
            txt = (f"spec class '{cls}': {len(g)} front-mapping round(s) in {len(mine)} spec run(s), mean HV gain "
                   f"{sum(g) / len(g) * 100:+.1f}% (min {min(g) * 100:+.1f}%, max {max(g) * 100:+.1f}%)" if g else
                   f"spec class '{cls}': no front-mapping round ran in {len(mine)} spec run(s)")
            self.remember("spec_class", cls, txt, sorted({o["run_id"] for o in mine}), "code")
            written.append(f"spec_class/{cls}")
        return written

    # -- persistence -----------------------------------------------------
    def dump(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for prefix in (("hw_dse", "memory"), ("hw_dse", "observations")):
            for it in self._all(prefix):
                out.setdefault("/".join(it.namespace), {})[it.key] = it.value
        return out

    def save(self, path: str | Path) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(self.dump(), indent=1, sort_keys=True))

    @staticmethod
    def load(path: str | Path, enabled: bool = True) -> CampaignMemory:
        mem = CampaignMemory(enabled=enabled)
        p = Path(path)
        if p.exists():
            for ns, items in json.loads(p.read_text()).items():
                for k, v in items.items():
                    mem.store.put(tuple(ns.split("/")), k, v)
        return mem
