#!/usr/bin/env python3
"""Archive the M4 live runs' traces under eval/data/traces/m4/ (the M3 layout).

    python scripts/archive_traces_m4.py

Sources (summary JSONs written by ``eval/run_eval.py``):

* ``eval/data/agent_m4/``        structured graph on the ASIC specs (also the A/B's single arm there)
* ``eval/data/fleet_m4/single/`` structured graph on the A/B's FPGA specs
* ``eval/data/fleet_m4/fleet/``  the code-orchestrated fleet (the first A/B, "before_fix")
* ``eval/data/fleet_m4/fleet_v2/`` the fleet after review fixes S3/S4 (Qwen re-run)
* ``eval/data/m4_pilot/``        the pilots

A structured run keeps ``llm_trace.jsonl``, ``report.md`` and
``evaluations.csv.gz``; a fleet run keeps the same three files for every member
run, under ``<member>-p<phase>/``. Layout ``traces/m4/<arm>/<spec>/<run>/``,
plus ``INDEX.md``. Every file is scanned for key material first
(credential-looking environment variable values and provider-key shapes); a
hit aborts before anything is written.
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

DEST = ROOT / "eval" / "data" / "traces" / "m4"
DATA = ROOT / "eval" / "data"
SOURCES = {"structured": DATA / "agent_m4", "single": DATA / "fleet_m4" / "single", "fleet": DATA / "fleet_m4" / "fleet",
           "fleet_v2": DATA / "fleet_m4" / "fleet_v2",
           "pilot-structured": DATA / "m4_pilot" / "structured", "pilot-fleet": DATA / "m4_pilot" / "fleet"}


def _stage_run(run: Path, out: Path, staged: list[tuple[Path, bytes]]) -> None:
    for name in ("llm_trace.jsonl", "report.md"):
        p = run / name
        if p.exists():
            text = p.read_text()
            scan(text, str(p))
            staged.append((out / name, text.encode()))
    if (run / "evaluations.csv").exists():
        text = (run / "evaluations.csv").read_text()
        scan(text, str(run / "evaluations.csv"))
        staged.append((out / "evaluations.csv.gz", gzip.compress(text.encode(), mtime=0)))


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
            if "fleet" in arm:
                for m in r["members"]:
                    mdir = ROOT / m["run_dir"]
                    _stage_run(mdir, out / f"{m['member']}-p{m['phase']}", staged)
            else:
                _stage_run(run, out, staged)
            label = r["model_requested"] + ("" if r.get("reasoning") in (None, "provider default") else f", reasoning {r['reasoning']}")
            index.append((str(out.relative_to(DEST)), label, arm, r["spec"], r["seed"], r["status"],
                          " → ".join(r.get("decisions", [])) or "—", float(r.get("cost_usd") or 0.0)))
    if DEST.exists():
        shutil.rmtree(DEST)
    for path, data in staged:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    total = sum(i[-1] for i in index)
    L = ["# M4 live run index", "",
         "Each structured run directory holds `llm_trace.jsonl` (every LLM call; key-redacted in code and scanned again "
         "by `scripts/archive_traces_m4.py`), `report.md` and `evaluations.csv.gz`; a fleet run holds the same per "
         "member run, under `<member>-p<phase>/`. Summary JSONs: `eval/data/agent_m4/`, `fleet_m4/`, `m4_pilot/`. "
         f"Provider-reported cost of these runs: ${total:.4f}.", "",
         "| run dir | model | arm | spec | seed | status | decisions | cost (USD) |", "|---|---|---|---|---|---|---|---|"]
    for d, label, arm, spec, seed, st, what, cost in sorted(index, key=lambda x: (x[2], x[1], x[3], x[4])):
        L.append(f"| `{d}` | `{label}` | {arm} | {spec} | {seed} | {st} | {what} | {cost:.4f} |")
    (DEST / "INDEX.md").write_text("\n".join(L) + "\n")
    print(f"archived {len(index)} runs to {DEST} (${total:.4f}); key scan clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
