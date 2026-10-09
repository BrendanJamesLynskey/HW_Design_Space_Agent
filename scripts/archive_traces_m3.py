#!/usr/bin/env python3
"""Archive the M3 live runs' traces under eval/data/traces/m3/ (the M2 layout).

    python scripts/archive_traces_m3.py

Sources (summary JSONs written by ``eval/run_eval.py``):

* ``eval/data/agent_m3/``            structured graph on the system specs
* ``eval/data/campaign_m3/``         campaign agent, memory off (the A/B arm)
* ``eval/data/campaign_m3_memory/``  campaign agent, memory on
* ``eval/data/m3_pilot/``            the pilots, including the failed first campaign pilot

For a structured run it copies ``llm_trace.jsonl``, ``report.md`` and
``evaluations.csv.gz``; for a campaign run ``llm_trace.jsonl`` (campaign
turns and inner-architect calls), ``tool_log.jsonl`` (every tool call and
its answer) and, per inner ``run_dse`` call, that run's ``report.md`` and
``evaluations.csv.gz``. Layout: ``traces/m3/<arm>/<spec>/<stamp>/``, plus
``INDEX.md``.

After archiving, ``python eval/m3_rescore.py`` adds each campaign's
``pool_keys.json.gz`` (its L1 pool, rebuilt or saved; re-run it after this
script, which rewrites the directory).

Every file is scanned for key material first (credential-looking
environment variable values and provider-key shapes); a hit aborts.
"""

from __future__ import annotations

import gzip
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from archive_traces import scan  # noqa: E402

DEST = ROOT / "eval" / "data" / "traces" / "m3"
DATA = ROOT / "eval" / "data"
SOURCES = {"structured": DATA / "agent_m3", "campaign": DATA / "campaign_m3", "memory": DATA / "campaign_m3_memory",
           "pilot-structured": DATA / "m3_pilot" / "structured", "pilot-campaign": DATA / "m3_pilot" / "campaign"}


def _stage_run(run: Path, out: Path, staged: list[tuple[Path, bytes]], campaign: bool) -> None:
    names = ["llm_trace.jsonl"] + (["tool_log.jsonl"] if campaign else ["report.md"])
    for name in names:
        p = run / name
        if p.exists():
            text = p.read_text()
            scan(text, str(p))
            staged.append((out / name, text.encode()))
    if not campaign and (run / "evaluations.csv").exists():
        text = (run / "evaluations.csv").read_text()
        scan(text, str(run / "evaluations.csv"))
        staged.append((out / "evaluations.csv.gz", gzip.compress(text.encode(), mtime=0)))
    if campaign:
        for inner in sorted((run / "dse").glob("*/*")):
            _stage_run(inner, out / "dse" / inner.parent.name / inner.name, staged, False)


def main() -> int:
    staged: list[tuple[Path, bytes]] = []
    index = []
    for arm, src in SOURCES.items():
        for p in sorted(src.glob("*/*.json")):
            r = json.loads(p.read_text())
            run = ROOT / r["run_dir"]
            if not run.exists():
                print(f"missing run dir for {p}: {run}")
                return 1
            out = DEST / arm / r["spec"] / run.name
            _stage_run(run, out, staged, campaign="campaign" in arm or arm == "memory")
            label = r["model_requested"] + ("" if r.get("reasoning") in (None, "provider default") else f", reasoning {r['reasoning']}")
            what = " → ".join(r.get("ladder", []) or r.get("decisions", [])) or "—"
            index.append((str(out.relative_to(DEST)), label, arm, r["spec"], r["seed"], "FAILED" if r.get("failed") else "ok",
                          what, float(r.get("cost_usd") or 0.0)))
    if DEST.exists():
        shutil.rmtree(DEST)
    for path, data in staged:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    total = sum(i[-1] for i in index)
    L = ["# M3 live run index", "",
         "Each directory holds the run's `llm_trace.jsonl` (every LLM call: campaign turns and inner-architect calls; "
         "key-redacted in code and scanned again by `scripts/archive_traces_m3.py`). Structured runs add `report.md` and "
         "`evaluations.csv.gz`; campaign runs add `tool_log.jsonl` (every tool call with its answer) and `dse/` with each "
         "inner `run_dse` call's report and evaluations. Summary JSONs: `eval/data/agent_m3/`, `campaign_m3/`, "
         f"`campaign_m3_memory/`, `m3_pilot/`. Provider-reported cost of these runs: ${total:.4f}.", "",
         "| run dir | model | arm | spec | seed | outcome | decisions / tool sequence | cost (USD) |",
         "|---|---|---|---|---|---|---|---|"]
    for d, label, arm, spec, seed, ok, what, cost in sorted(index, key=lambda x: (x[2], x[1], x[3], x[4])):
        L.append(f"| `{d}` | `{label}` | {arm} | {spec} | {seed} | {ok} | {what} | {cost:.4f} |")
    (DEST / "INDEX.md").write_text("\n".join(L) + "\n")
    print(f"archived {len(index)} runs to {DEST} (${total:.4f}); key scan clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
