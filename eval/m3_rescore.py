"""Re-score the M3 live runs after the L2 fix (review B1), offline, from committed data.

    python eval/m3_rescore.py            # rewrite the affected rows in place; pool keys -> traces
    python eval/m3_rescore.py --check    # only report what would change

The fix: L2 now simulates every L1-feasible design a run evaluated, not just
the L1 front (a design that passes L2 can be dominated in the L1 objectives
by one that only passed the bound). The L1 evaluations of the live runs do
not change, so each affected run is rebuilt *exactly* from committed data and
re-selected with today's code:

* structured runs: the run's ``evaluations.csv.gz`` (every evaluated design,
  canonical order), each design re-evaluated by ``evaluate`` (deterministic);
* campaigns: the pool rebuilt from the tool log in completion order: each
  ``run_dse`` call's ``evaluations.csv.gz`` (under ``dse/``), and each
  ``explore_family`` call re-run with its recorded arguments
  (``run_family_study`` is deterministic); for runs that saved their pool
  (``evaluations.json.gz``, after the pool-saving fix) that saved pool is used
  instead. A rebuilt call's seed index is the one that
  reproduces the feasible count the tool reported: parallel calls in the live
  runs could share an index (a race, fixed in ``campaign/tools.py``).

Only specs with a system scenario can change. Each rewritten row keeps its
previous values under ``before_b1``. For every campaign (all specs) the
rebuilt pool's design keys are written next to its trace as
``pool_keys.json.gz`` (review N5), so every campaign can be re-scored from the repo.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import io
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "eval"))

DATA = ROOT / "eval" / "data"
TRACES = DATA / "traces" / "m3"
ARMS = {"structured": DATA / "agent_m3", "campaign": DATA / "campaign_m3", "memory": DATA / "campaign_m3_memory",
        "pilot-structured": DATA / "m3_pilot" / "structured", "pilot-campaign": DATA / "m3_pilot" / "campaign"}


def csv_keys(path: Path) -> list[str]:
    with gzip.open(path, "rt", newline="") as fh:
        return [r["key"] for r in csv.DictReader(io.StringIO(fh.read()))]


def evaluate_keys(keys: list[str], spec: Any) -> list[dict[str, Any]]:
    from hw_dse.evaluate import evaluate
    from hw_dse.families import ArchConfig

    cache: dict[str, dict[str, Any]] = {}
    out = []
    for k in keys:
        if k not in cache:
            cache[k] = evaluate(ArchConfig.from_key(k), spec)
        out.append(dict(cache[k]))
    return out


def campaign_pool(row: dict[str, Any], tdir: Path, spec: Any) -> list[dict[str, Any]]:
    """The campaign's L1 pool in call order, rebuilt from its tool log."""
    from hw_dse.campaign.tools import t_explore_family  # noqa: F401  (documents the seed formula used below)
    from hw_dse.explore import run_family_study
    from hw_dse.families import clamp_ranges

    log = [json.loads(x) for x in (tdir / "tool_log.jsonl").read_text().splitlines() if x.strip()]
    inner = sorted((tdir / "dse").glob("*/*/evaluations.csv.gz"))
    pool: list[dict[str, Any]] = []
    n_dse = n_ef = 0
    for e in log:
        res = e["result"]
        if res.startswith(("refused", "error", "tool-call limit")) or e["args"].get("spec_name") != row["spec"]:
            continue
        if e["tool"] == "run_dse":
            pool += evaluate_keys(csv_keys(inner[n_dse]), spec)
            n_dse += 1
        elif e["tool"] == "explore_family":
            a = e["args"]
            fam = a["family"]
            prop: dict[str, object] = {}
            for prm, lo, hi in (("data_width", a.get("data_width_min"), a.get("data_width_max")),
                                ("n_iter", a.get("n_iter_min"), a.get("n_iter_max")),
                                ("k" if fam == "unrolled_k" else "m", a.get("k_or_m_min"), a.get("k_or_m_max"))):
                if lo is not None or hi is not None:
                    prop[prm] = [lo if lo is not None else hi, hi if hi is not None else lo]
            if fam in ("iterative", "pipelined"):
                prop.pop("m", None)
            cl = clamp_ranges(fam, prop)
            m_ = re.search(r": (\d+) evaluations, (\d+) feasible", res)
            n, feas = int(m_.group(1)), int(m_.group(2))
            # The live tool took its seed index from the number of explore_family calls
            # *finished* when it started; parallel calls could share one (fixed since).
            # Take the first index (from the most likely down) that reproduces the
            # feasible count the tool reported.
            for k in [n_ef, *range(n_ef - 1, -1, -1)]:
                recs = run_family_study(fam, cl.ranges, spec, n, int(row["seed"]) * 131 + 17 * k + 3,
                                        tag={"round": f"campaign-{k}"})
                if sum(1 for r in recs if r["feasible"]) == feas:
                    break
            else:
                raise RuntimeError(f"{tdir}: no seed index reproduces explore_family call {n_ef}")
            pool += recs
            n_ef += 1
    if n_dse != len(inner):
        raise RuntimeError(f"{tdir}: {n_dse} run_dse calls in the log but {len(inner)} inner runs")
    return pool


def rescore(check: bool) -> None:
    from hw_dse import accuracy_table
    from hw_dse.agent.summary import merged_front
    from hw_dse.benchmark import select_design
    from hw_dse.l2.node import l2_select
    from run_eval import any_spec, score_m3

    accuracy_table.preload()
    changed = []
    pool_src: dict[str, str] = {}
    for arm, src in ARMS.items():
        for p in sorted(src.glob("*/*.json")):
            row = json.loads(p.read_text())
            if "attempt" in row:
                continue
            spec = any_spec(row["spec"])
            tdir = TRACES / arm / row["spec"] / Path(row["run_dir"]).name
            campaign = "campaign" in arm or arm == "memory"
            if campaign:
                saved = ROOT / row["run_dir"] / "evaluations.json.gz"
                if saved.exists():  # the run's own record of its pool
                    with gzip.open(saved, "rt") as fh:
                        pool = evaluate_keys([r["key"] for r in json.load(fh)[row["spec"]]], spec)
                    src_note = "saved by the run"
                else:
                    pool = campaign_pool(row, tdir, spec)
                    src_note = "rebuilt from the tool log"
                pool_src[str(p.relative_to(ROOT))] = src_note
                if not check:
                    with gzip.open(tdir / "pool_keys.json.gz", "wt") as fh:
                        json.dump([r["key"] for r in pool], fh)
            else:
                pool = evaluate_keys(csv_keys(tdir / "evaluations.csv.gz"), spec)
            if len(pool) != row["n_evals"]:
                raise RuntimeError(f"{p}: rebuilt {len(pool)} evaluations, row says {row['n_evals']}")
            if spec.system is None:
                continue
            front = merged_front(pool, spec)
            l1 = select_design(front, spec)
            l2 = l2_select(pool, l1, spec)
            sel = l2["selected"]
            declared = None if sel else bool(row.get("llm_declared_infeasible"))
            sc = score_m3(pool, spec, declared, sel)
            if sc["selected_key"] == row["selected_key"] and sc["hv_frac"] == row["hv_frac"]:
                continue
            keys = ("selected_key", "select_regret", "hv_frac", "selected_meets_spec", "evals_to_95")
            changed.append((p.relative_to(ROOT), {k: (row.get(k), sc[k]) for k in keys}))
            if not check:
                row["before_b1"] = {k: row.get(k) for k in (*keys, "l2_winner_changed")}
                row.update(sc)
                row["l1_selected_key"] = l1["key"] if l1 else None
                row["l2_winner_changed"] = bool(l2.get("winner_changed"))
                row["rescored"] = ("after the L2 fix (review B1): selection over every L1-feasible design; "
                                   "L1 evaluations unchanged (eval/m3_rescore.py)")
                p.write_text(json.dumps(row, indent=1, default=str))
    for path, d in changed:
        print(path, {k: v for k, v in d.items() if v[0] != v[1]})
    print(f"{len(changed)} rows {'would change' if check else 'rewritten'}; campaign pools: "
          f"{sum(v == 'saved by the run' for v in pool_src.values())} saved by the run, "
          f"{sum(v != 'saved by the run' for v in pool_src.values())} rebuilt from the tool log")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    rescore(ap.parse_args().check)


if __name__ == "__main__":
    main()
