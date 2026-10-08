"""The eval: does an LLM architect beat plain optimisers on the same budget?

Usage::

    python eval/run_eval.py ground-truth          # exhaustive grid -> eval/data/ground_truth.json
    python eval/run_eval.py baselines             # NSGA-II + random, 3 seeds -> eval/data/baselines.json
    python eval/run_eval.py agent --provider openrouter --model qwen/qwen3.8-27b [--max-spend 5]
                                                  # live agent runs -> eval/data/agent/<model>/*.json
    python eval/run_eval.py report                # everything above -> eval/results.md

What is compared (per spec, same evaluation budget = the spec's
``total_evals``):

* **ground truth**: the exhaustive grid (635,040 designs) gives the true
  Pareto front, true hypervolume (HV) and the design the spec's selection
  rule picks;
* **baseline (a)**: Optuna NSGA-II over the union of all families and full
  ranges;
* **baseline (b)**: random search over the same space;
* **agent**: the LangGraph agent with a real LLM choosing families and
  ranges each round (Optuna NSGA-II inside each family).

Metrics: evaluations needed to reach 95% of the true HV; HV at budget (as
a fraction of true HV); whether the selected design meets the spec;
whether infeasibility was called correctly. For the baselines,
"declared infeasible" simply means "found no feasible design"; for the
agent it means the LLM itself returned the ``infeasible`` decision.

Honesty rules baked in: agent rows are only ever read from
``eval/data/agent/``, which only the ``agent`` subcommand writes, and it
refuses the ``fake`` provider. Each agent JSON records the model id the
provider reported, token usage and the provider-reported cost. The
``agent`` subcommand stops starting new runs once the cumulative cost
(across every saved agent run) passes ``--max-spend`` dollars.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hw_dse import accuracy_table  # noqa: E402
from hw_dse.benchmark import build_grid, ground_truth, run_baseline, score_run  # noqa: E402
from hw_dse.spec import Spec, load_spec  # noqa: E402

DATA = ROOT / "eval" / "data"
GT_FILE = DATA / "ground_truth.json"
BASELINE_FILE = DATA / "baselines.json"
AGENT_DIR = DATA / "agent"
RESULTS = ROOT / "eval" / "results.md"
SEEDS = (0, 1, 2)


def specs() -> list[Spec]:
    return [load_spec(p) for p in sorted((ROOT / "specs").glob("*.yaml"))]


def _slim(rec: dict[str, Any] | None) -> dict[str, Any] | None:
    if rec is None:
        return None
    keep = ("key", "family", "luts", "ffs", "luts_plus_ffs", "fmax_mhz", "throughput_msps", "latency_cycles",
            "latency_ns", "power_index", "max_abs_err", "max_abs_err_lsb", "rms_err", "accuracy_bits", "feasible")
    return {k: rec[k] for k in keep if k in rec}


def cmd_ground_truth(_: argparse.Namespace) -> None:
    accuracy_table.preload()
    t0 = time.time()
    grid = build_grid(verbose=True)
    out = {}
    for s in specs():
        gt = ground_truth(grid, s)
        out[s.name] = {
            "n_designs": gt["n_designs"],
            "n_feasible": gt["n_feasible"],
            "feasible": gt["feasible"],
            "hv_true": gt.get("hv_true", 0.0),
            "best_throughput_msps_any": gt["best_throughput_msps_any"],
            "selected": _slim(gt["selected"]),
            "front": [_slim(r) for r in gt["front"]],
        }
        print(f"{s.name}: {gt['n_feasible']} feasible, HV {gt.get('hv_true', 0):.4g}, "
              f"front {len(gt['front'])}, selected {gt['selected']['key'] if gt['selected'] else None}")
    DATA.mkdir(parents=True, exist_ok=True)
    GT_FILE.write_text(json.dumps(out, indent=1))
    print(f"wrote {GT_FILE} in {time.time() - t0:.0f}s")


def load_gt() -> dict[str, Any]:
    return json.loads(GT_FILE.read_text())


def cmd_baselines(_: argparse.Namespace) -> None:
    accuracy_table.preload()
    gts = load_gt()
    out: dict[str, Any] = {}
    for s in specs():
        for sampler in ("nsga2", "random"):
            for seed in SEEDS:
                recs = run_baseline(s, sampler, seed)
                sc = score_run(recs, s, gts[s.name])
                out[f"{s.name}|{sampler}|{seed}"] = {"spec": s.name, "method": sampler, "seed": seed, **sc}
                print(s.name, sampler, seed, "HV", sc["hv_frac"], "evals95", sc["evals_to_95"])
    BASELINE_FILE.write_text(json.dumps(out, indent=1))
    print(f"wrote {BASELINE_FILE}")


# ---------------------------------------------------------------------------
# Live agent runs
# ---------------------------------------------------------------------------

def _slug(model: str) -> str:
    return model.replace("/", "__").replace(":", "_")


def total_agent_spend() -> float:
    total = 0.0
    for p in AGENT_DIR.glob("*/*.json"):
        total += float(json.loads(p.read_text()).get("cost_usd") or 0.0)
    return total


def cmd_agent(args: argparse.Namespace) -> None:
    if args.provider == "fake":
        raise SystemExit("refusing: the agent column must come from a real LLM, not the fake provider")
    from hw_dse.agent.runner import run_agent  # imported late: needs langgraph

    accuracy_table.preload()
    gts = load_gt()
    outdir = AGENT_DIR / _slug(args.model)
    outdir.mkdir(parents=True, exist_ok=True)
    wanted = set(args.specs.split(",")) if args.specs else None
    for s in specs():
        if wanted and s.name not in wanted:
            continue
        for seed in SEEDS[: args.seeds]:
            path = outdir / f"{s.name}_seed{seed}.json"
            if path.exists() and not args.force:
                print(f"skip (exists): {path.name}")
                continue
            spent = total_agent_spend()
            if spent >= args.max_spend:
                print(f"STOP: cumulative agent spend ${spent:.4f} >= ${args.max_spend}")
                return
            t0 = time.time()
            res = run_agent(spec=s, provider=args.provider, model=args.model, seed=seed,
                            reasoning=args.reasoning, run_root=ROOT / "runs" / "eval", method=args.method)
            sc = score_run(res["evaluations_ordered"], s, gts[s.name],
                           declared_infeasible=res["llm_declared_infeasible"], selected=res["selected"])
            row = {
                "spec": s.name,
                "seed": seed,
                "provider": args.provider,
                "model_requested": args.model,
                "models_served": res["models_served"],
                "reasoning": args.reasoning or "provider default",
                "structured_method": res["structured_method"],
                "status": res["status"],
                "rounds": res["rounds"],
                "llm_calls": res["llm"]["calls"],
                "llm_failures": res["llm"]["failures"],
                "input_tokens": res["llm"]["input_tokens"],
                "output_tokens": res["llm"]["output_tokens"],
                "cost_usd": res["llm"]["cost_usd"],
                "wall_s": round(time.time() - t0, 1),
                "run_dir": str(Path(res["run_dir"]).relative_to(ROOT)),
                "decisions": res["decisions"],
                **sc,
            }
            path.write_text(json.dumps(row, indent=1))
            print(f"{s.name} seed {seed}: {res['status']}, HV {sc['hv_frac']}, evals95 {sc['evals_to_95']}, "
                  f"${row['cost_usd']:.4f}, {row['wall_s']}s")


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def _fmt_frac(xs: list[float]) -> str:
    xs = [x for x in xs if x is not None and not math.isnan(x)]
    if not xs:
        return "n/a"
    if len(xs) == 1:
        return f"{xs[0]:.3f}"
    return f"{statistics.mean(xs):.3f} ± {statistics.pstdev(xs):.3f}"


def _fmt_evals(xs: list[int | None]) -> str:
    hit = [x for x in xs if x is not None]
    if not xs:
        return "n/a"
    if not hit:
        return f"not reached (0/{len(xs)})"
    med = statistics.median(hit)
    return f"{med:.0f} ({len(hit)}/{len(xs)} reached)"


def _rows_by(rows: list[dict[str, Any]], spec: str) -> list[dict[str, Any]]:
    return [r for r in rows if r["spec"] == spec]


def cmd_report(_: argparse.Namespace) -> None:
    gts = load_gt()
    base = list(json.loads(BASELINE_FILE.read_text()).values()) if BASELINE_FILE.exists() else []
    agents: dict[str, list[dict[str, Any]]] = {}
    for p in sorted(AGENT_DIR.glob("*/*.json")):
        row = json.loads(p.read_text())
        agents.setdefault(row["model_requested"], []).append(row)

    L: list[str] = []
    L.append("# Eval results: LLM architect vs plain optimisers\n")
    L.append("Generated by `python eval/run_eval.py report`. Every number below comes from code: the cost model "
             "(*estimate*, Artix-7, 2-anchor calibration) and the bit-accurate golden model (*exact*). "
             "No LLM produced any of them.\n")
    L.append("Budget per run = the spec's `total_evals` (400). Seeds 0, 1, 2. "
             "HV fraction = hypervolume of the feasible designs found / true hypervolume from the exhaustive "
             "grid of 635,040 designs. \"Evals to 95%\" = evaluations until 95% of the true HV, median over the "
             "seeds that reached it.\n")
    L.append("## Ground truth (exhaustive grid)\n")
    L.append("| spec | feasible designs | true front size | true HV | spec-selected design | its LUTs / FFs / MSPS / accuracy bits |")
    L.append("|---|---|---|---|---|---|")
    for s in specs():
        g = gts[s.name]
        sel = g["selected"]
        if sel:
            desc = f"{sel['luts']:.0f} / {sel['ffs']:.0f} / {sel['throughput_msps']:.1f} / {sel['accuracy_bits']:.2f}"
            L.append(f"| {s.name} | {g['n_feasible']:,} | {len(g['front'])} | {g['hv_true']:.4g} | `{sel['key']}` | {desc} |")
        else:
            L.append(f"| {s.name} | 0 (**infeasible**; best throughput anywhere {g['best_throughput_msps_any']:.1f} MSPS) | 0 | 0 | none | n/a |")
    L.append("")
    L.append("## Results per spec\n")
    methods: list[tuple[str, list[dict[str, Any]]]] = [
        ("baseline (a): NSGA-II, union space", [r for r in base if r["method"] == "nsga2"]),
        ("baseline (b): random search", [r for r in base if r["method"] == "random"]),
    ]
    for model, rows in agents.items():
        methods.append((f"agent: `{model}`", rows))
    for s in specs():
        L.append(f"### {s.name}\n")
        L.append("| method | runs | HV fraction at budget | evals to 95% HV | selected design meets spec | infeasibility called correctly |")
        L.append("|---|---|---|---|---|---|")
        feasible_spec = gts[s.name]["feasible"]
        for name, rows in methods:
            rs = _rows_by(rows, s.name)
            if not rs:
                continue
            if not feasible_spec:
                none_sel = sum(r["selected_key"] is None for r in rs)
                L.append(f"| {name} | {len(rs)} | n/a (infeasible) | n/a | n/a ({none_sel}/{len(rs)} selected nothing) | "
                         f"{sum(r['infeasibility_correct'] for r in rs)}/{len(rs)} |")
                continue
            L.append(
                f"| {name} | {len(rs)} | {_fmt_frac([r['hv_frac'] for r in rs])} | {_fmt_evals([r['evals_to_95'] for r in rs])} | "
                f"{sum(r['selected_meets_spec'] for r in rs)}/{len(rs)} | {sum(r['infeasibility_correct'] for r in rs)}/{len(rs)} |"
            )
        if not agents:
            L.append("| agent | pending | — | — | — | — |")
        L.append("")
    if agents:
        L.append("## Agent runs: models, tokens and cost\n")
        L.append("| model requested | model(s) served | reasoning | runs | LLM calls | failed calls | input tok | output tok | cost (USD) |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for model, rows in agents.items():
            served = sorted({m for r in rows for m in r["models_served"]})
            reas = sorted({r["reasoning"] for r in rows})
            L.append(
                f"| `{model}` | {', '.join(f'`{m}`' for m in served)} | {', '.join(reas)} | {len(rows)} | "
                f"{sum(r['llm_calls'] for r in rows):.0f} | {sum(r['llm_failures'] for r in rows):.0f} | "
                f"{sum(r['input_tokens'] for r in rows):,.0f} | {sum(r['output_tokens'] for r in rows):,.0f} | "
                f"{sum(r['cost_usd'] for r in rows):.4f} |"
            )
        total = sum(r["cost_usd"] for rows in agents.values() for r in rows)
        L.append(f"\nTotal agent spend: **${total:.4f}**.\n")
        L.append("## Agent decisions per run\n")
        for model, rows in agents.items():
            L.append(f"**`{model}`**\n")
            for r in sorted(rows, key=lambda r: (r["spec"], r["seed"])):
                L.append(f"- {r['spec']} seed {r['seed']}: {r['status']}; decisions: "
                         f"{' → '.join(r['decisions']) or '—'}; HV fraction {_fmt_frac([r['hv_frac']])}; run `{r['run_dir']}`")
            L.append("")
    else:
        L.append("## Agent results pending\n")
        L.append("No live LLM agent runs have been recorded yet. The agent column is deliberately empty: it is "
                 "never filled from the fake provider.\n")
    RESULTS.write_text("\n".join(L) + "\n")
    print(f"wrote {RESULTS}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ground-truth").set_defaults(fn=cmd_ground_truth)
    sub.add_parser("baselines").set_defaults(fn=cmd_baselines)
    a = sub.add_parser("agent")
    a.add_argument("--provider", default="openrouter")
    a.add_argument("--model", required=True)
    a.add_argument("--seeds", type=int, default=3)
    a.add_argument("--specs", default="", help="comma-separated spec names (default: all)")
    a.add_argument("--reasoning", default=None, help="OpenRouter reasoning: off|low|medium|high (default: provider default)")
    a.add_argument("--method", default=None, help="structured output method: function_calling|json_schema")
    a.add_argument("--max-spend", type=float, default=5.0, help="stop starting runs once cumulative agent spend passes this (USD)")
    a.add_argument("--force", action="store_true", help="re-run even if a result file exists")
    a.set_defaults(fn=cmd_agent)
    sub.add_parser("report").set_defaults(fn=cmd_report)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
