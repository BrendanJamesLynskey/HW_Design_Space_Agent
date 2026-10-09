#!/usr/bin/env python3
"""Archive the M2 live runs' traces under eval/data/traces/m2/ (same layout as M1).

    python scripts/archive_traces.py

For every live M2 run recorded in ``eval/data/agent_m2/`` and
``eval/data/agent_m2_pilot/`` it copies, from the run's ``runs/`` directory:

* ``llm_trace.jsonl``      -- every LLM call (prompt, reply, parsed object, usage, cost);
* ``evaluations.csv.gz``   -- every evaluation, gzipped;
* ``report.md``            -- the run report;

into ``eval/data/traces/m2/<spec>/<run stamp>/`` (PNG plots and SQLite
checkpoints are left out), and writes ``eval/data/traces/m2/INDEX.md``.

Before writing anything it scans every file for key material: the value of
every environment variable that looks like a credential, and anything shaped
like a provider key. A hit aborts the archive (the tracer redacts in code, so
this is a second check, not the first line of defence).
"""

from __future__ import annotations

import gzip
import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "eval" / "data" / "traces" / "m2"
SOURCES = {"eval": ROOT / "eval" / "data" / "agent_m2", "pilot": ROOT / "eval" / "data" / "agent_m2_pilot"}
KEY_SHAPES = re.compile(r"(sk-or-v1-[A-Za-z0-9]{8,}|sk-ant-[A-Za-z0-9_\-]{8,}|sk-[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_\-]{20,})")
SECRET_NAME = re.compile(r"(API_KEY|_TOKEN|_SECRET|PASSWORD)$", re.IGNORECASE)


def secrets() -> list[str]:
    return [v for k, v in os.environ.items() if SECRET_NAME.search(k) and v and len(v) >= 8]


def scan(text: str, where: str) -> None:
    for v in secrets():
        if v in text:
            raise SystemExit(f"ABORT: credential value of an environment variable found in {where}")
    m = KEY_SHAPES.search(text)
    if m:
        raise SystemExit(f"ABORT: key-shaped string found in {where} (offset {m.start()})")


def main() -> int:
    rows = []
    for kind, src in SOURCES.items():
        for p in sorted(src.glob("*/*.json")):
            r = json.loads(p.read_text())
            rows.append((kind, r))
    if not rows:
        print("no M2 runs recorded")
        return 1
    staged: list[tuple[Path, bytes]] = []
    index = []
    for kind, r in rows:
        run = ROOT / r["run_dir"]
        rel = Path(*Path(r["run_dir"]).parts[2:])  # runs/<eval_m2...>/<spec>/<stamp> -> <spec>/<stamp>
        out = DEST / ("pilot" if kind == "pilot" else "") / rel
        trace = (run / "llm_trace.jsonl").read_text()
        report = (run / "report.md").read_text()
        csv_text = (run / "evaluations.csv").read_text()
        for name, text in (("llm_trace.jsonl", trace), ("report.md", report), ("evaluations.csv", csv_text)):
            scan(text, f"{run}/{name}")
        staged += [(out / "llm_trace.jsonl", trace.encode()), (out / "report.md", report.encode()),
                   (out / "evaluations.csv.gz", gzip.compress(csv_text.encode(), mtime=0))]
        label = r["model_requested"] + ("" if r["reasoning"] == "provider default" else f", reasoning {r['reasoning']}")
        index.append((str(out.relative_to(DEST)), label, kind, r["spec"], r["seed"], r["status"],
                      " → ".join(r["decisions"]) or "—", r.get("coverage_rounds", 0), r["cost_usd"]))
    if DEST.exists():
        shutil.rmtree(DEST)
    for path, data in staged:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    total = sum(i[-1] for i in index)
    L = ["# M2 eval run index", "",
         "Each directory holds `llm_trace.jsonl` (every LLM call, key-redacted in code and scanned again by "
         "`scripts/archive_traces.py`), `evaluations.csv.gz` and `report.md`, copied from the live M2 runs' `runs/` "
         "output (PNG plots and SQLite checkpoints omitted). Summary JSONs are in `eval/data/agent_m2/` (and "
         f"`agent_m2_pilot/` for the pilot). Provider-reported cost of these runs: ${total:.4f}.", "",
         "| run dir | model | kind | spec | seed | status | LLM decisions | front-mapping rounds | cost (USD) |",
         "|---|---|---|---|---|---|---|---|---|"]
    for d, label, kind, spec, seed, status, dec, cov, cost in sorted(index, key=lambda x: (x[2] != "pilot", x[1], x[3], x[4])):
        L.append(f"| `{d}` | `{label}` | {kind} | {spec} | {seed} | {status} | {dec} | {cov} | {cost:.4f} |")
    (DEST / "INDEX.md").write_text("\n".join(L) + "\n")
    print(f"archived {len(index)} runs to {DEST} (${total:.4f}); key scan clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
