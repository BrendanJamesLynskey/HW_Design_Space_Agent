"""The eval: does an LLM architect beat plain optimisers on the same budget?

Usage::

    python eval/run_eval.py ground-truth                  # exhaustive grid -> eval/data/ground_truth.json
    python eval/run_eval.py baselines --milestone m2      # NSGA-II + random, 5 seeds -> eval/data/baselines_m2.json
    python eval/run_eval.py agent --model qwen/qwen3.8-27b --reasoning off [--pilot] [--max-spend 5]
                                                          # live M2 runs -> eval/data/agent_m2/<model>/*.json
    python eval/run_eval.py report                        # everything above -> eval/results.md

Milestone 1 (3 seeds) is archived as recorded: ``baselines.json`` and
``agent/`` are never rewritten. Milestone 2 (5 seeds, the whole-curve levers
``LEVERS_M2``) writes ``baselines_m2.json`` and ``agent_m2/``; the report
puts the two side by side.

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

Metrics: HV at the end as a fraction of the true HV; evaluations to reach
95% of the true HV; selection regret (how much worse the selected design
is than the true optimum on the spec's selection metric); whether the
selected design meets the spec; whether infeasibility was called
correctly. For the baselines "declared infeasible" means "found no feasible
design"; for the agent it means the LLM itself returned ``infeasible``.

Honesty rules baked in: agent rows are only ever read from ``agent*/``
directories, which only the ``agent`` subcommand writes, and it refuses the
``fake`` provider. Each agent JSON records the model id the provider
reported, token usage and the provider-reported cost. Every live run is
appended to ``spend_ledger.jsonl``; ``agent`` refuses to start a run once the
milestone's ledger total plus the expected cost of the next run would pass
``--max-spend`` (and the key's own usage endpoint is the authoritative
figure, recorded in ``key_usage_m2.json``).
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
BASELINES = {"m1": DATA / "baselines.json", "m2": DATA / "baselines_m2.json"}
AGENT_DIRS = {"m1": DATA / "agent", "m2": DATA / "agent_m2", "m2-pilot": DATA / "agent_m2_pilot"}
RESULTS = ROOT / "eval" / "results.md"
GT_M3_FILE = DATA / "ground_truth_m3.json"
# Milestone 3 system-level specs (specs/system/). The eval runs agents and
# baselines on M3_EVAL_SPECS; dds_sfdr is ground truth only (a negative
# result: its system constraints reduce to the MSPS-only view, see results.md).
M3_EVAL_SPECS = ("multiaxis_control", "bursty_offload")
M3_GT_ONLY = ("dds_sfdr",)
SEEDS = {"m1": (0, 1, 2), "m2": (0, 1, 2, 3, 4)}
LEDGER = DATA / "spend_ledger.jsonl"


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


def system_specs() -> list[Spec]:
    return [load_spec(p) for p in sorted((ROOT / "specs" / "system").glob("*.yaml"))]


def _slim_sys(rec: dict[str, Any] | None, spec: Spec) -> dict[str, Any] | None:
    out = _slim(rec)
    if out is None or rec is None:
        return out
    for c in spec.constraints:
        if c.metric.startswith("sys_"):
            out[c.metric] = rec[c.metric]
    for k in ("m", "k", "data_width", "n_iter"):
        if k in rec:
            out[k] = rec[k]
    return out


def cmd_ground_truth_m3(_: argparse.Namespace) -> None:
    """Exhaustive ground truth for the system specs, three ways: the truth
    (system metrics simulated at L2), what L1 screening sees (analytic
    bounds), and the MSPS-only view (the spec without its system constraints,
    throughput floor = the scenario's average offered rate)."""
    import numpy as np

    from hw_dse.benchmark import _feasible_mask, select_design
    from hw_dse.evaluate import evaluate

    accuracy_table.preload()
    t0 = time.time()
    grid = build_grid()
    out: dict[str, Any] = {}
    for s in system_specs():
        gt = ground_truth(grid, s)
        alt = s.without_system()
        gt_msps = ground_truth(grid, alt)
        mb = grid.metrics(s, "bound")
        fb = _feasible_mask(mb, s)
        sel_metric = mb[s.select_by]
        idx = np.flatnonzero(fb)
        best = sel_metric[idx].min() if s.select_direction == "min" else sel_metric[idx].max()
        ties = idx[np.flatnonzero(sel_metric[idx] == best)]
        bound_sel = select_design([evaluate(grid.arch(int(i)), s) for i in ties], s)
        out[s.name] = {
            "n_designs": gt["n_designs"], "n_feasible": gt["n_feasible"], "feasible": gt["feasible"],
            "hv_true": gt.get("hv_true", 0.0), "best_throughput_msps_any": gt["best_throughput_msps_any"],
            "selected": _slim_sys(gt["selected"], s), "front": [_slim_sys(r, s) for r in gt["front"]],
            "eval": s.name in M3_EVAL_SPECS,
            "n_feasible_l1_bound": int(fb.sum()),
            "l1_bound_selected": _slim_sys(bound_sel, s),
            "msps_only": {"spec": alt.model_dump(), "n_feasible": gt_msps["n_feasible"], "hv_true": gt_msps.get("hv_true", 0.0),
                          "selected": _slim(gt_msps["selected"]), "front_size": len(gt_msps["front"])},
            "winner_changes_vs_msps_only": bool(gt["selected"] and gt_msps["selected"]
                                                and gt["selected"]["key"] != gt_msps["selected"]["key"]),
        }
        print(f"{s.name}: {gt['n_feasible']} feasible (L1 bound {int(fb.sum())}), selected "
              f"{gt['selected']['key'] if gt['selected'] else None}; L1-bound selection "
              f"{bound_sel['key'] if bound_sel else None}; MSPS-only {gt_msps['selected']['key'] if gt_msps['selected'] else None}")
    GT_M3_FILE.write_text(json.dumps(out, indent=1))
    print(f"wrote {GT_M3_FILE} in {time.time() - t0:.0f}s")


def load_gt_m3() -> dict[str, Any]:
    return json.loads(GT_M3_FILE.read_text())


def load_gt() -> dict[str, Any]:
    return json.loads(GT_FILE.read_text())


def cmd_baselines(args: argparse.Namespace) -> None:
    accuracy_table.preload()
    gts = load_gt()
    out: dict[str, Any] = {}
    for s in specs():
        for sampler in ("nsga2", "random"):
            for seed in SEEDS[args.milestone]:
                recs = run_baseline(s, sampler, seed)
                sc = score_run(recs, s, gts[s.name])
                out[f"{s.name}|{sampler}|{seed}"] = {"spec": s.name, "method": sampler, "seed": seed, **sc}
                print(s.name, sampler, seed, "HV", sc["hv_frac"], "evals95", sc["evals_to_95"])
    BASELINES[args.milestone].write_text(json.dumps(out, indent=1))
    print(f"wrote {BASELINES[args.milestone]}")


# ---------------------------------------------------------------------------
# Live agent runs
# ---------------------------------------------------------------------------

def _slug(model: str) -> str:
    return model.replace("/", "__").replace(":", "_")


def ledger(milestone: str | None = None) -> list[dict[str, Any]]:
    """Append-only record of every live run's provider-reported cost.
    M1 entries carry no ``milestone`` field."""
    if not LEDGER.exists():
        return []
    rows = [json.loads(line) for line in LEDGER.read_text().splitlines() if line.strip()]
    if milestone is None:
        return rows
    return [r for r in rows if r.get("milestone", "m1") == milestone]


def spend(milestone: str | None = None) -> float:
    return sum(float(r.get("cost_usd") or 0.0) for r in ledger(milestone))


def cmd_agent(args: argparse.Namespace) -> None:
    if args.provider == "fake":
        raise SystemExit("refusing: the agent column must come from a real LLM, not the fake provider")
    from hw_dse.agent.graph import LEVERS_M2
    from hw_dse.agent.runner import run_agent  # imported late: needs langgraph

    accuracy_table.preload()
    gts = load_gt()
    key = "m2-pilot" if args.pilot else "m2"
    outdir = AGENT_DIRS[key] / (_slug(args.model) + (f"__reasoning-{args.reasoning}" if args.reasoning else ""))
    outdir.mkdir(parents=True, exist_ok=True)
    wanted = set(args.specs.split(",")) if args.specs else None
    prior = [r for r in ledger("m2") if r["model"] == args.model]
    expected = statistics.mean(float(r["cost_usd"] or 0) for r in prior) if prior else args.expected_cost
    for s in specs():
        if wanted and s.name not in wanted:
            continue
        for seed in SEEDS["m2"][: args.seeds]:
            path = outdir / f"{s.name}_seed{seed}.json"
            if path.exists() and not args.force:
                print(f"skip (exists): {path.name}")
                continue
            spent = spend("m2")
            if spent + 2 * expected > args.max_spend:
                print(f"STOP: M2 spend ${spent:.4f} + 2x expected next run ${expected:.4f} would pass ${args.max_spend}")
                return
            t0 = time.time()
            res = run_agent(spec=s, provider=args.provider, model=args.model, seed=seed, reasoning=args.reasoning,
                            run_root=ROOT / "runs" / ("eval_m2_pilot" if args.pilot else "eval_m2"), method=args.method)
            sc = score_run(res["evaluations_ordered"], s, gts[s.name],
                           declared_infeasible=res["llm_declared_infeasible"], selected=res["selected"])
            row = {
                "milestone": "m2", "pilot": bool(args.pilot), "levers": LEVERS_M2,
                "spec": s.name, "seed": seed, "provider": args.provider, "model_requested": args.model,
                "models_served": res["models_served"], "reasoning": args.reasoning or "provider default",
                "structured_method": res["structured_method"], "status": res["status"], "rounds": res["rounds"],
                "coverage_rounds": res["coverage_rounds"], "llm_calls": res["llm"]["calls"],
                "llm_failures": res["llm"]["failures"], "input_tokens": res["llm"]["input_tokens"],
                "output_tokens": res["llm"]["output_tokens"], "cost_usd": res["llm"]["cost_usd"],
                "wall_s": round(time.time() - t0, 1), "run_dir": str(Path(res["run_dir"]).relative_to(ROOT)),
                "decisions": res["decisions"], "overrides": res["overrides"], **sc,
            }
            with open(LEDGER, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"model": args.model, "spec": s.name, "seed": seed, "cost_usd": row["cost_usd"],
                                     "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "milestone": "m2",
                                     **({"note": "pilot"} if args.pilot else {})}) + "\n")
            path.write_text(json.dumps(row, indent=1))
            expected = statistics.mean([float(r["cost_usd"] or 0) for r in ledger("m2") if r["model"] == args.model])
            print(f"{s.name} seed {seed}: {res['status']}, HV {sc['hv_frac']}, regret {sc['select_regret']}, "
                  f"evals {sc['n_evals']}, decisions {res['decisions']}, ${row['cost_usd']:.4f}, {row['wall_s']}s", flush=True)


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def _ms(xs: list[float | None], pct: bool = False, signed: bool = False, digits: int = 3) -> str:
    """mean ± population std (as in M1), or the single value."""
    v = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    if not v:
        return "n/a"
    k = 100.0 if pct else 1.0
    fmt = f"{{:{'+' if signed else ''}.{1 if pct else digits}f}}"
    m = fmt.format(statistics.mean(v) * k) + ("%" if pct else "")
    if len(v) == 1:
        return m
    return f"{m} ± {statistics.pstdev(v) * k:.{1 if pct else digits}f}" + ("" if not pct else "")


def _fmt_evals(xs: list[int | None]) -> str:
    hit = [x for x in xs if x is not None]
    if not xs:
        return "n/a"
    if not hit:
        return f"not reached (0/{len(xs)})"
    return f"{statistics.median(hit):.0f} ({len(hit)}/{len(xs)} reached)"


def _optimal(xs: list[float | None]) -> str:
    v = [x for x in xs if x is not None]
    return f"{sum(1 for x in v if x <= 1e-9)}/{len(xs)}"


def _label(row: dict[str, Any]) -> str:
    return row["model_requested"] + ("" if row["reasoning"] == "provider default" else f", reasoning {row['reasoning']}")


def load_agents(key: str) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for p in sorted(AGENT_DIRS[key].glob("*/*.json")):
        row = json.loads(p.read_text())
        out.setdefault(_label(row), []).append(row)
    return out


def load_baselines(key: str) -> list[dict[str, Any]]:
    return list(json.loads(BASELINES[key].read_text()).values()) if BASELINES[key].exists() else []


def _per_spec(rows: list[dict[str, Any]], spec: str) -> list[dict[str, Any]]:
    return [r for r in rows if r["spec"] == spec]


def _detail_table(L: list[str], s: Spec, gts: dict[str, Any], methods: list[tuple[str, list[dict[str, Any]]]],
                  coverage: bool = False) -> None:
    L.append(f"| method | runs | evals used | HV fraction at end | evals to 95% HV | selected meets spec | "
             f"selection regret on {s.select_by} (optimal) | infeasibility called correctly |"
             + (" front-mapping rounds |" if coverage else ""))
    L.append("|---|---|---|---|---|---|---|---|" + ("---|" if coverage else ""))
    feasible_spec = gts[s.name]["feasible"]
    for name, rows in methods:
        rs = _per_spec(rows, s.name)
        if not rs:
            continue
        cov = f" {statistics.mean(r.get('coverage_rounds', 0) for r in rs):.1f} |" if coverage else ""
        if not feasible_spec:
            none_sel = sum(r["selected_key"] is None for r in rs)
            L.append(f"| {name} | {len(rs)} | {_ms([float(r['n_evals']) for r in rs], digits=0)} | n/a (infeasible) | n/a | "
                     f"n/a ({none_sel}/{len(rs)} selected nothing) | n/a | {sum(r['infeasibility_correct'] for r in rs)}/{len(rs)} |" + cov)
            continue
        L.append(f"| {name} | {len(rs)} | {_ms([float(r['n_evals']) for r in rs], digits=0)} | {_ms([r['hv_frac'] for r in rs])} | "
                 f"{_fmt_evals([r['evals_to_95'] for r in rs])} | {sum(r['selected_meets_spec'] for r in rs)}/{len(rs)} | "
                 f"{_ms([r.get('select_regret') for r in rs], pct=True, signed=True)} ({_optimal([r.get('select_regret') for r in rs])}) | "
                 f"{sum(r['infeasibility_correct'] for r in rs)}/{len(rs)} |" + cov)
    L.append("")


def cmd_report(_: argparse.Namespace) -> None:
    gts = load_gt()
    base = {k: load_baselines(k) for k in ("m1", "m2")}
    agents = {k: load_agents(k) for k in ("m1", "m2", "m2-pilot")}
    sp = specs()
    feas_specs = [s for s in sp if gts[s.name]["feasible"]]

    L: list[str] = []
    L.append("# Eval results: LLM architect vs plain optimisers (M1 and M2)\n")
    L.append("Generated by `python eval/run_eval.py report` from the committed data; no LLM produced any number below. "
             "Numbers are *estimates* (cost model, the M1 two-anchor Vivado calibration, unchanged in M2 so both "
             "milestones are scored on the same ground truth) and *exact* (bit-accurate golden model).\n")
    L.append("Budget per run = the spec's `total_evals` (400). **M1**: seeds 0–2, the M1 agent. **M2**: seeds 0–4, the "
             "agent with the whole-curve levers (`LEVERS_M2`: a 40% front-mapping reserve, front-anchored box, the "
             "`map_front` decision). Before an M2 run stops, code spends any budget left on one final front-mapping round, "
             "which is exempt from `max_rounds` and `evals_per_round` (so up to 5 rounds, and one round can exceed 100 "
             "evaluations); `total_evals` is never exceeded. Cells are mean ± population std over seeds. HV fraction = hypervolume of the "
             "feasible designs found / true hypervolume of the exhaustive grid (635,040 designs). Selection regret = how "
             "much worse the selected design is than the true optimum on the spec's selection metric (0% = optimal). "
             "M1 numbers are read from the archived M1 data and are not re-run.\n")

    L.append("## Ground truth (exhaustive grid)\n")
    L.append("| spec | feasible designs | true front size | true HV | spec-selected design | its LUTs / FFs / MSPS / accuracy bits |")
    L.append("|---|---|---|---|---|---|")
    for s in sp:
        g = gts[s.name]
        sel = g["selected"]
        if sel:
            desc = f"{sel['luts']:.0f} / {sel['ffs']:.0f} / {sel['throughput_msps']:.1f} / {sel['accuracy_bits']:.2f}"
            L.append(f"| {s.name} | {g['n_feasible']:,} | {len(g['front'])} | {g['hv_true']:.4g} | `{sel['key']}` | {desc} |")
        else:
            L.append(f"| {s.name} | 0 (**infeasible**; best throughput anywhere {g['best_throughput_msps_any']:.1f} MSPS) | 0 | 0 | none | n/a |")
    L.append("")

    # ---- headline ------------------------------------------------------
    models_m2 = list(agents["m2"])
    L.append("## M1 vs M2 at a glance\n")
    for metric, title in (("hv_frac", "HV fraction at end"), ("select_regret", "Selection regret"), ("n_evals", "Evaluations used")):
        L.append(f"**{title}** (M1 → M2)\n")
        L.append("| spec | NSGA-II | random | " + " | ".join(f"`{m}`" for m in models_m2) + " |")
        L.append("|---|---|---|" + "---|" * len(models_m2))
        for s in feas_specs:
            cells = []
            for k in ("nsga2", "random"):
                c = [_ms([float(r[metric]) if r[metric] is not None else None for r in base[mk] if r["spec"] == s.name and r["method"] == k],
                         pct=metric == "select_regret", signed=metric == "select_regret", digits=0 if metric == "n_evals" else 3)
                     for mk in ("m1", "m2")]
                cells.append(f"{c[0]} → {c[1]}")
            for m in models_m2:
                c = [_ms([float(r[metric]) if r[metric] is not None else None for r in _per_spec(agents[mk].get(m, []), s.name)],
                         pct=metric == "select_regret", signed=metric == "select_regret", digits=0 if metric == "n_evals" else 3)
                     for mk in ("m1", "m2")]
                cells.append(f"{c[0]} → **{c[1]}**")
            L.append(f"| {s.name} | " + " | ".join(cells) + " |")
        L.append("")
    L.append("**Agent HV relative to NSGA-II** (mean agent HV / mean NSGA-II HV on the same milestone's seeds; 1.00 = parity)\n")
    L.append("| spec | " + " | ".join(f"`{m}` M1 → M2" for m in models_m2) + " |")
    L.append("|---|" + "---|" * len(models_m2))
    for s in feas_specs:
        cells = []
        for m in models_m2:
            vals = []
            for mk in ("m1", "m2"):
                nsga = [r["hv_frac"] for r in base[mk] if r["spec"] == s.name and r["method"] == "nsga2"]
                ag = [r["hv_frac"] for r in _per_spec(agents[mk].get(m, []), s.name)]
                vals.append(f"{statistics.mean(ag) / statistics.mean(nsga):.2f}" if ag and nsga else "n/a")
            cells.append(f"{vals[0]} → **{vals[1]}**")
        L.append(f"| {s.name} | " + " | ".join(cells) + " |")
    L.append("")
    inf = [s for s in sp if not gts[s.name]["feasible"]]
    if inf:
        s = inf[0]
        L.append(f"**Infeasible spec** (`{s.name}`): infeasibility called correctly, and evaluations used (M1 → M2)\n")
        L.append("| method | M1 | M2 |")
        L.append("|---|---|---|")
        for name, rows1, rows2 in [("NSGA-II", [r for r in base["m1"] if r["method"] == "nsga2"], [r for r in base["m2"] if r["method"] == "nsga2"]),
                                   ("random", [r for r in base["m1"] if r["method"] == "random"], [r for r in base["m2"] if r["method"] == "random"])] + \
                [(f"`{m}`", agents["m1"].get(m, []), agents["m2"].get(m, [])) for m in models_m2]:
            cell = []
            for rows in (rows1, rows2):
                rs = _per_spec(rows, s.name)
                cell.append(f"{sum(r['infeasibility_correct'] for r in rs)}/{len(rs)}, {_ms([float(r['n_evals']) for r in rs], digits=0)} evals" if rs else "—")
            L.append(f"| {name} | {cell[0]} | {cell[1]} |")
        L.append("")

    # ---- tokens and cost ------------------------------------------------
    L.append("## Tokens, cost and time per run (M1 → M2)\n")
    L.append("| model | runs | LLM calls / run | failed calls | input tokens / run | output tokens / run | cost / run (USD) | total cost (USD) | wall time / run (s) |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    all_models = list(dict.fromkeys(list(agents["m1"]) + models_m2))
    for m in all_models:
        a1, a2 = agents["m1"].get(m, []), agents["m2"].get(m, [])

        def pair(f: Any, digits: int = 0) -> str:
            return " → ".join(_ms([float(f(r)) for r in rs], digits=digits) if rs else "—" for rs in (a1, a2))

        L.append(f"| `{m}` | {len(a1)} → {len(a2)} | {pair(lambda r: r['llm_calls'], 1)} | "
                 f"{sum(r['llm_failures'] for r in a1):.0f} → {sum(r['llm_failures'] for r in a2):.0f} | "
                 f"{pair(lambda r: r['input_tokens'])} | {pair(lambda r: r['output_tokens'])} | {pair(lambda r: r['cost_usd'], 4)} | "
                 f"{sum(r['cost_usd'] for r in a1):.4f} → {sum(r['cost_usd'] for r in a2):.4f} | {pair(lambda r: r['wall_s'])} |")
    tot = {k: sum(r["cost_usd"] for rows in agents[k].values() for r in rows) for k in agents}
    L.append(f"\nProvider-reported cost of the recorded runs: M1 **${tot['m1']:.4f}**, M2 **${tot['m2']:.4f}** "
             f"(+ M2 pilot ${tot['m2-pilot']:.4f}). Calls that fail inside the client report no usage, so these undercount; the "
             "authoritative figures are the key's usage before/after (`eval/data/key_usage_m2.json`).\n")
    served = sorted({x for rows in agents["m2"].values() for r in rows for x in r["models_served"]})
    if served:
        L.append("Models served in M2 (as reported by the provider): " + ", ".join(f"`{x}`" for x in served) + ".\n")

    # ---- M2 detail -----------------------------------------------------
    L.append("## M2 results per spec (5 seeds)\n")
    methods = [("baseline (a): NSGA-II, union space", [r for r in base["m2"] if r["method"] == "nsga2"]),
               ("baseline (b): random search", [r for r in base["m2"] if r["method"] == "random"])]
    methods += [(f"agent M2: `{m}`", rows) for m, rows in agents["m2"].items()]
    for s in sp:
        L.append(f"### {s.name}\n")
        _detail_table(L, s, gts, methods, coverage=True)
    if agents["m2-pilot"]:
        L.append("### Live pilot (before the full M2 run)\n")
        L.append("One seed, the two specs the levers target, the cheapest model; recorded separately "
                 "(`eval/data/agent_m2_pilot/`) and not part of the tables above.\n")
        for m, rows in agents["m2-pilot"].items():
            for r in sorted(rows, key=lambda r: (r["spec"], r["seed"])):
                L.append(f"- `{m}` {r['spec']} seed {r['seed']}: HV {_ms([r['hv_frac']])}, regret "
                         f"{_ms([r['select_regret']], pct=True, signed=True)}, {r['n_evals']} evals, decisions "
                         f"{' → '.join(r['decisions']) or '—'}, front-mapping rounds {r.get('coverage_rounds', 0)}, ${r['cost_usd']:.4f}")
        L.append("")
    if agents["m2"]:
        L.append("### M2 agent decisions per run\n")
        for m, rows in agents["m2"].items():
            L.append(f"**`{m}`**\n")
            for r in sorted(rows, key=lambda r: (r["spec"], r["seed"])):
                cov = " + code front-mapping" * (r.get("coverage_rounds", 0) and "map_front" not in r["decisions"])
                L.append(f"- {r['spec']} seed {r['seed']}: {r['status']}; decisions: {' → '.join(r['decisions']) or '—'}{cov}; "
                         f"HV {_ms([r['hv_frac']])}; run `{r['run_dir']}`")
            L.append("")

    # ---- M1 archive ----------------------------------------------------
    L.append("## M1 results per spec (archived, 3 seeds)\n")
    methods = [("baseline (a): NSGA-II, union space", [r for r in base["m1"] if r["method"] == "nsga2"]),
               ("baseline (b): random search", [r for r in base["m1"] if r["method"] == "random"])]
    methods += [(f"agent M1: `{m}`", rows) for m, rows in agents["m1"].items()]
    for s in sp:
        L.append(f"### {s.name}\n")
        _detail_table(L, s, gts, methods)
    L.append("### M1 agent decisions per run\n")
    for m, rows in agents["m1"].items():
        L.append(f"**`{m}`**\n")
        for r in sorted(rows, key=lambda r: (r["spec"], r["seed"])):
            L.append(f"- {r['spec']} seed {r['seed']}: {r['status']}; decisions: {' → '.join(r['decisions']) or '—'}; "
                     f"HV {_ms([r['hv_frac']])}; run `{r['run_dir']}`")
        L.append("")
    RESULTS.write_text("\n".join(L) + "\n")
    print(f"wrote {RESULTS}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ground-truth").set_defaults(fn=cmd_ground_truth)
    sub.add_parser("ground-truth-m3").set_defaults(fn=cmd_ground_truth_m3)
    b = sub.add_parser("baselines")
    b.add_argument("--milestone", choices=("m1", "m2"), default="m2")
    b.set_defaults(fn=cmd_baselines)
    a = sub.add_parser("agent")
    a.add_argument("--provider", default="openrouter")
    a.add_argument("--model", required=True)
    a.add_argument("--seeds", type=int, default=5)
    a.add_argument("--specs", default="", help="comma-separated spec names (default: all)")
    a.add_argument("--reasoning", default=None, help="OpenRouter reasoning: off|low|medium|high (default: provider default)")
    a.add_argument("--method", default=None, help="structured output method: function_calling|json_schema")
    a.add_argument("--pilot", action="store_true", help="write to agent_m2_pilot/ (not part of the eval tables)")
    a.add_argument("--max-spend", type=float, default=5.0, help="M2 spend cap (USD), checked before every run")
    a.add_argument("--expected-cost", type=float, default=0.10, help="assumed cost of a run before any is recorded")
    a.add_argument("--force", action="store_true", help="re-run even if a result file exists")
    a.set_defaults(fn=cmd_agent)
    sub.add_parser("report").set_defaults(fn=cmd_report)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
