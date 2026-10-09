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
    report_m3(L)
    RESULTS.write_text("\n".join(L) + "\n")
    print(f"wrote {RESULTS}")


# ---------------------------------------------------------------------------
# Milestone 3: system specs, the structured arm, the campaign arm, memory A/B
# ---------------------------------------------------------------------------

M3_DIRS = {"agent": DATA / "agent_m3", "campaign": DATA / "campaign_m3", "memory": DATA / "campaign_m3_memory",
           "pilot": DATA / "m3_pilot"}
BASELINES_M3 = DATA / "baselines_m3.json"
KEY_USAGE_M3 = DATA / "key_usage_m3.json"
MEMORY_STORE = DATA / "campaign_m3_memory_store.json"
M2_SPEC_NAMES = ("dds_250msps", "high_precision", "infeasible_dds_400msps", "low_area_control")
MEMORY_SEQUENCE = ("low_area_control", "bursty_offload", "dds_250msps", "multiaxis_control")
M3_CAP = 5.0


def any_spec(name: str) -> Spec:
    from hw_dse.campaign.tools import spec_path

    return load_spec(spec_path(name))


def gt_for(name: str) -> dict[str, Any]:
    return load_gt_m3()[name] if name in M3_EVAL_SPECS + M3_GT_ONLY else load_gt()[name]


def score_m3(records: list[dict[str, Any]], spec: Spec, declared_infeasible: bool | None,
             selected: dict[str, Any] | None) -> dict[str, Any]:
    """score_run, with system metrics re-scored by L2 simulation (the truth) for a system spec:
    a design counts as feasible only if it passes the *simulated* system constraints."""
    if spec.system is not None:
        from hw_dse.l2.node import simulate_record

        records = [simulate_record(r, spec) for r in records]
        selected = simulate_record(selected, spec) if selected else None
    return score_run(records, spec, gt_for(spec.name), declared_infeasible=declared_infeasible, selected=selected)


def cmd_baselines_m3(_: argparse.Namespace) -> None:
    """NSGA-II and random on the system specs, 5 seeds. Same L1 information as the agent
    (system constraints screened by the L1 bound), the same L2 shortlist step at the end."""
    from hw_dse.agent.summary import merged_front
    from hw_dse.benchmark import select_design
    from hw_dse.l2.node import l2_select

    accuracy_table.preload()
    out: dict[str, Any] = {}
    for name in M3_EVAL_SPECS:
        s = any_spec(name)
        for sampler in ("nsga2", "random"):
            for seed in SEEDS["m2"]:
                recs = run_baseline(s, sampler, seed)
                front = merged_front(recs, s)
                sel = l2_select(front, select_design(front, s), s)["selected"]
                sc = score_m3(recs, s, None if sel else True, sel)
                out[f"{name}|{sampler}|{seed}"] = {"spec": name, "method": sampler, "seed": seed, **sc}
                print(name, sampler, seed, "HV", sc["hv_frac"], "regret", sc["select_regret"])
    BASELINES_M3.write_text(json.dumps(out, indent=1))
    print(f"wrote {BASELINES_M3}")


def _key_usage() -> dict[str, Any]:
    import os
    import urllib.request

    if not os.environ.get("OPENROUTER_API_KEY"):
        raise SystemExit("OPENROUTER_API_KEY is not set")
    req = urllib.request.Request("https://openrouter.ai/api/v1/key",
                                 headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"]})
    with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310 - fixed https URL
        d = json.loads(r.read())["data"]
    return {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "usage_usd": d.get("usage"),
            "limit_usd": d.get("limit"), "limit_remaining_usd": d.get("limit_remaining")}


def cmd_key_usage(args: argparse.Namespace) -> None:
    """Record the key's usage (free endpoint) under a tag; the key itself is never recorded."""
    data = json.loads(KEY_USAGE_M3.read_text()) if KEY_USAGE_M3.exists() else {
        "note": "OpenRouter GET /api/v1/key (free), read with the key from the environment; the key itself is never "
                "recorded.", "m3_spend_cap_usd": M3_CAP, "snapshots": {}}
    snap = _key_usage()
    data["snapshots"][args.tag] = snap
    KEY_USAGE_M3.write_text(json.dumps(data, indent=1))
    print(args.tag, snap)


def _ledger_add(model: str, spec: str, seed: int, cost: float, arm: str, note: str = "") -> None:
    with open(LEDGER, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"model": model, "spec": spec, "seed": seed, "cost_usd": cost, "arm": arm,
                             "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "milestone": "m3",
                             **({"note": note} if note else {})}) + "\n")


def _expected(model: str, arm: str, default: float) -> float:
    prior = [float(r.get("cost_usd") or 0) for r in ledger("m3") if r["model"] == model and r.get("arm") == arm]
    return statistics.mean(prior) if prior else default


def _cap_ok(model: str, arm: str, default: float, cap: float) -> bool:
    spent, exp = spend("m3"), _expected(model, arm, default)
    if spent + 2 * exp > cap:
        print(f"STOP: M3 spend ${spent:.4f} + 2x expected next {arm} run ${exp:.4f} would pass ${cap}")
        return False
    return True


def _model_dir(model: str, reasoning: str | None) -> str:
    return _slug(model) + (f"__reasoning-{reasoning}" if reasoning else "")


def cmd_agent_m3(args: argparse.Namespace) -> None:
    """Structured arm, fresh, on the new system specs (the M2 specs reuse the M2 runs: replay-proven)."""
    from hw_dse.agent.graph import default_levers
    from hw_dse.agent.runner import run_agent

    accuracy_table.preload()
    outdir = (M3_DIRS["pilot"] / "structured" if args.pilot else M3_DIRS["agent"]) / _model_dir(args.model, args.reasoning)
    outdir.mkdir(parents=True, exist_ok=True)
    names = args.specs.split(",") if args.specs else list(M3_EVAL_SPECS)
    for name in names:
        s = any_spec(name)
        for seed in SEEDS["m2"][: args.seeds]:
            path = outdir / f"{name}_seed{seed}.json"
            if path.exists() and not args.force:
                print(f"skip (exists): {path.name}")
                continue
            if not _cap_ok(args.model, "structured", args.expected_cost, args.max_spend):
                return
            t0 = time.time()
            res = run_agent(spec=s, provider="openrouter", model=args.model, seed=seed, reasoning=args.reasoning,
                            run_root=ROOT / "runs" / ("eval_m3_pilot" if args.pilot else "eval_m3"))
            sc = score_m3(res["evaluations_ordered"], s, res["llm_declared_infeasible"], res["selected"])
            row = {"milestone": "m3", "arm": "structured", "pilot": bool(args.pilot), "levers": default_levers(s),
                   "spec": name, "seed": seed, "provider": "openrouter", "model_requested": args.model,
                   "models_served": res["models_served"], "reasoning": args.reasoning or "provider default",
                   "structured_method": res["structured_method"], "status": res["status"], "rounds": res["rounds"],
                   "coverage_rounds": res["coverage_rounds"], "llm_calls": res["llm"]["calls"],
                   "llm_failures": res["llm"]["failures"], "input_tokens": res["llm"]["input_tokens"],
                   "output_tokens": res["llm"]["output_tokens"], "cost_usd": res["llm"]["cost_usd"],
                   "wall_s": round(time.time() - t0, 1), "run_dir": str(Path(res["run_dir"]).relative_to(ROOT)),
                   "decisions": res["decisions"], "overrides": res["overrides"],
                   "l1_selected_key": (res["selected_l1"] or {}).get("key"),
                   "l2_winner_changed": bool((res["l2"] or {}).get("winner_changed")), "failed": False, **sc}
            _ledger_add(args.model, name, seed, row["cost_usd"], "structured", "pilot" if args.pilot else "")
            path.write_text(json.dumps(row, indent=1, default=str))
            print(f"{name} seed {seed}: {res['status']}, HV {sc['hv_frac']}, regret {sc['select_regret']}, "
                  f"L2 changed {row['l2_winner_changed']}, ${row['cost_usd']:.4f}, {row['wall_s']}s", flush=True)


def _campaign_row(res: dict[str, Any], name: str, seed: int, model: str, reasoning: str | None, arm: str,
                  memory: bool, pilot: bool) -> dict[str, Any]:
    s = any_spec(name)
    ps = res["per_spec"][name]
    recs = ps["evaluations"]  # already in call order (run_dse runs are canonically ordered inside)
    declared = None if ps["selected"] else bool(ps["llm_declared_infeasible"]) or not ps["evaluations"]
    sc = score_m3(ps["evaluations"], s, declared, ps["selected"])
    failed = bool(res["error"]) or ps["left_open"]
    return {"milestone": "m3", "arm": arm, "pilot": pilot, "memory": memory, "spec": name, "seed": seed,
            "provider": "openrouter", "model_requested": model, "models_served": res["models_served"],
            "reasoning": reasoning or "provider default", "error": res["error"], "failed": failed,
            "left_open": ps["left_open"], "campaign_model_calls": res["campaign_model_calls"],
            "tool_calls": res["tool_calls"], "ladder": ps["calls"], "dse_runs": ps["dse_runs"], "l2": ps["l2"],
            "l3": ps["l3"], "l4": ps["l4"], "back_annotation": ps["back_annotation"], "l5": ps["l5"],
            "llm_calls": res["llm"]["calls"], "llm_failures": res["llm"]["failures"],
            "input_tokens": res["llm"]["input_tokens"], "output_tokens": res["llm"]["output_tokens"],
            "cost_usd": res["llm"]["cost_usd"], "wall_s": res["wall_s"],
            "run_dir": str(Path(res["run_dir"]).relative_to(ROOT)), "run_id": res["run_id"],
            "final_text": res["final_text"], "n_recs_ordered": len(recs), **sc}


def cmd_campaign_m3(args: argparse.Namespace) -> None:
    """Campaign arm: one single-spec campaign per (spec, seed), memory off (the A/B condition)."""
    from hw_dse.campaign.memory import CampaignMemory
    from hw_dse.campaign.runner import run_campaign

    accuracy_table.preload()
    outdir = (M3_DIRS["pilot"] / "campaign" if args.pilot else M3_DIRS["campaign"]) / _model_dir(args.model, args.reasoning)
    outdir.mkdir(parents=True, exist_ok=True)
    names = args.specs.split(",") if args.specs else list(M2_SPEC_NAMES + M3_EVAL_SPECS)
    for seed in SEEDS["m2"][: args.seeds]:
        for name in names:
            path = outdir / f"{name}_seed{seed}.json"
            if path.exists() and not args.force:
                print(f"skip (exists): {path.name}")
                continue
            if not _cap_ok(args.model, "campaign", args.expected_cost, args.max_spend):
                return
            res = run_campaign([name], seed=seed, model=args.model, reasoning=args.reasoning,
                               memory=CampaignMemory(enabled=False),
                               run_root=ROOT / "runs" / ("campaign_m3_pilot" if args.pilot else "campaign_m3"))
            row = _campaign_row(res, name, seed, args.model, args.reasoning, "campaign", False, bool(args.pilot))
            _ledger_add(args.model, name, seed, row["cost_usd"], "campaign", "pilot" if args.pilot else "")
            path.write_text(json.dumps(row, indent=1, default=str))
            print(f"{name} seed {seed}: HV {row['hv_frac']}, regret {row['select_regret']}, evals {row['n_evals']}, "
                  f"ladder {row['ladder']}, failed {row['failed']} ({row['error']}), ${row['cost_usd']:.4f}, "
                  f"{row['wall_s']}s", flush=True)


def cmd_memory_m3(args: argparse.Namespace) -> None:
    """Memory ON over a fixed spec sequence (one store per seed, carried from spec to spec).
    The memory-OFF condition is the campaign arm's runs for the same specs and seeds."""
    from hw_dse.campaign.memory import CampaignMemory
    from hw_dse.campaign.runner import run_campaign

    accuracy_table.preload()
    outdir = M3_DIRS["memory"] / _model_dir(args.model, args.reasoning)
    outdir.mkdir(parents=True, exist_ok=True)
    stores = json.loads(MEMORY_STORE.read_text()) if MEMORY_STORE.exists() else {}
    for seed in SEEDS["m2"][: args.seeds]:
        mem = CampaignMemory(enabled=True)
        for k, v in stores.get(f"seed{seed}", {}).items():
            for kk, vv in v.items():
                mem.store.put(tuple(k.split("/")), kk, vv)
        for name in MEMORY_SEQUENCE:
            path = outdir / f"{name}_seed{seed}.json"
            if path.exists() and not args.force:
                print(f"skip (exists): {path.name}")
                continue
            if not _cap_ok(args.model, "campaign", args.expected_cost, args.max_spend):
                return
            res = run_campaign([name], seed=seed, model=args.model, reasoning=args.reasoning, memory=mem,
                               run_root=ROOT / "runs" / "campaign_m3_memory")
            row = _campaign_row(res, name, seed, args.model, args.reasoning, "campaign", True, False)
            row["memory_lessons_before"] = None
            _ledger_add(args.model, name, seed, row["cost_usd"], "campaign", "memory-on")
            path.write_text(json.dumps(row, indent=1, default=str))
            stores[f"seed{seed}"] = mem.dump()
            MEMORY_STORE.write_text(json.dumps(stores, indent=1, sort_keys=True))
            print(f"[memory on] {name} seed {seed}: HV {row['hv_frac']}, regret {row['select_regret']}, "
                  f"${row['cost_usd']:.4f}", flush=True)


def _load_rows(d: Path) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for p in sorted(d.glob("*/*.json")):
        row = json.loads(p.read_text())
        if "attempt" in row:
            continue
        out.setdefault(_label(row), []).append(row)
    return out


def _fail_rate(rows: list[dict[str, Any]]) -> str:
    return f"{sum(bool(r.get('failed')) for r in rows)}/{len(rows)}"


def report_m3(L: list[str]) -> None:
    """Milestone 3 section of results.md (appended; the M1/M2 sections above are untouched)."""
    if not GT_M3_FILE.exists():
        return
    import csv as _csv

    gt3 = load_gt_m3()
    gt2 = load_gt()
    L.append("# Milestone 3: system-level specs (L2), the campaign agent, the A/B\n")
    L.append("Everything below is generated from committed data as well. *simulated* = L2 SimPy system model (clock = the "
             "design's estimated Fmax) or the golden-model DDS; *estimate (L1 bound)* = the analytic bound L1 screens "
             "system constraints with. M3 runs use the same 400-evaluation budget per spec as M1/M2.\n")

    # ---- ground truth --------------------------------------------------
    L.append("## System specs: exhaustive ground truth, three views\n")
    L.append("Truth = system metrics simulated for every one of the 635,040 designs (they share 1,092 distinct "
             "(latency, ii, Fmax) tuples). L1-bound view = what L1 screening sees. MSPS-only view = the same spec without "
             "its system constraints, throughput floor = the scenario's average offered rate (how it reads in M2 terms).\n")
    L.append("| spec | system | feasible (simulated / L1 bound / MSPS-only) | true winner (simulated) | L1-bound winner | MSPS-only winner | winner changes vs MSPS-only |")
    L.append("|---|---|---|---|---|---|---|")
    for name, g in gt3.items():
        s = any_spec(name)
        sel, bsel, msel = g["selected"], g["l1_bound_selected"], g["msps_only"]["selected"]
        def k(r: dict[str, Any] | None) -> str:
            return f"`{r['key']}` ({r[s.select_by]:.0f})" if r else "none"
        L.append(f"| {name}{'' if g['eval'] else ' (ground truth only)'} | {s.system.describe() if s.system else ''} | "
                 f"{g['n_feasible']:,} / {g['n_feasible_l1_bound']:,} / {g['msps_only']['n_feasible']:,} | {k(sel)} | {k(bsel)} | "
                 f"{k(msel)} | {'**yes**' if g['winner_changes_vs_msps_only'] else 'no'} |")
    L.append("")
    for name, g in gt3.items():
        s = any_spec(name)
        sel = g["selected"]
        if sel:
            sysv = ", ".join(f"{c.metric} = {sel[c.metric]:.4g} (limit {c.value:g})" for c in s.system_constraints)
            L.append(f"- `{name}` true winner: {sel['luts']:.0f} LUTs / {sel['ffs']:.0f} FFs, {sel['throughput_msps']:.1f} MSPS, "
                     f"{sel['accuracy_bits']:.2f} bits; {sysv} (simulated).")
    L.append("")

    # ---- L2 validation --------------------------------------------------
    cv = DATA / "l2_cycle_validation.csv"
    if cv.exists():
        rows = list(_csv.DictReader(open(cv)))
        sims = sorted({r["simulator_version"] for r in rows})
        L.append("## L2 cycle model vs generated RTL\n")
        L.append(f"{len(rows)} short bursty traces (8 designs covering every family and both rounding modes x 3 seeds x "
                 f"{', '.join(sims)}), {sum(int(r['n_edges']) for r in rows):,} clock edges: **"
                 f"{sum(r['passed'] == 'True' for r in rows)}/{len(rows)} identical** on ready, valid_out and the output codes "
                 f"(ready mismatches {sum(int(r['ready_mismatches']) for r in rows)}, valid {sum(int(r['valid_mismatches']) for r in rows)}, "
                 f"data {sum(int(r['data_mismatches']) for r in rows)}). Source: `eval/data/l2_cycle_validation.csv`.\n")

    # ---- replay + map_front fix -------------------------------------------
    rp, fx = DATA / "m2_replay.json", DATA / "m3_mapfront_fix.json"
    if rp.exists():
        r = json.loads(rp.read_text())
        L.append("## Comparability: the M2 runs replayed through the M3 graph\n")
        L.append(f"**{r['n_identical']}/{r['n_runs']} identical**: same decisions, status, rounds, front-mapping rounds, every "
                 "evaluated design key in order, HV fraction, selection regret and selected design (`eval/data/m2_replay.json`). "
                 "This is what allows the structured arm of the A/B to reuse the M2 live runs on the four M2 specs.\n")
    if fx.exists():
        rows = json.loads(fx.read_text())["rows"]
        sys.path.insert(0, str(ROOT / "eval"))
        from m3_offline import table_fix

        L.append("## The map_front fix on the M2 specs (offline, scripted architects)\n")
        L.append("Unconditional (every explored family without a feasible design gets a full-box share):\n")
        L.append(table_fix(rows, "fix-all"))
        L.append("\nGated (the M3 default, `LEVERS_M3`; structural constraints must have been met by the family's own designs):\n")
        L.append(table_fix(rows, "fix"))
        L.append("")

    # ---- structured arm on the system specs --------------------------------
    base3 = list(json.loads(BASELINES_M3.read_text()).values()) if BASELINES_M3.exists() else []
    ag3 = _load_rows(M3_DIRS["agent"])
    cp3 = _load_rows(M3_DIRS["campaign"])
    gts_all = {**gt2, **gt3}
    L.append("## Structured graph on the system specs (5 seeds)\n")
    methods = [("baseline (a): NSGA-II + L2 shortlist", [r for r in base3 if r["method"] == "nsga2"]),
               ("baseline (b): random + L2 shortlist", [r for r in base3 if r["method"] == "random"])]
    methods += [(f"structured: `{m}`", rows) for m, rows in ag3.items()]
    for name in M3_EVAL_SPECS:
        s = any_spec(name)
        L.append(f"### {name}\n")
        _detail_table(L, s, gts_all, methods)
        ch = [(m, sum(r.get("l2_winner_changed", False) for r in rows if r["spec"] == name),
               len([r for r in rows if r["spec"] == name])) for m, rows in ag3.items()]
        if ch:
            L.append("L2 changed the L1 selection in: " + "; ".join(f"`{m}` {a}/{b}" for m, a, b in ch) + " runs.\n")

    # ---- the A/B --------------------------------------------------------
    ag2 = load_agents("m2")
    L.append("## A/B: structured graph vs campaign agent (same specs, seeds, budget)\n")
    L.append("Structured arm: the M2 live runs on the four M2 specs (replay-proven identical graph) and the fresh M3 runs on "
             "the system specs. Campaign arm: one single-spec campaign per (spec, seed), memory off, the same model as both "
             "the campaign agent and the inner architect. Failure = the campaign raised (stuck, call cap, provider error) or "
             "left the spec unfinalized. Cells: mean ± population std over seeds.\n")
    models = list(dict.fromkeys(list(ag2) + list(ag3) + list(cp3)))
    all_specs = list(M2_SPEC_NAMES) + list(M3_EVAL_SPECS)
    for metric, title, pct in (("hv_frac", "HV fraction", False), ("select_regret", "selection regret", True),
                               ("n_evals", "L1 evaluations used", False)):
        L.append(f"**{title}** (structured → campaign)\n")
        L.append("| spec | " + " | ".join(f"`{m}`" for m in models) + " |")
        L.append("|---|" + "---|" * len(models))
        for name in all_specs:
            cells = []
            for m in models:
                st = [r for r in (ag2.get(m, []) + ag3.get(m, [])) if r["spec"] == name]
                cp = [r for r in cp3.get(m, []) if r["spec"] == name]
                f = lambda rows: _ms([float(r[metric]) if r.get(metric) is not None else None for r in rows], pct=pct,
                                     signed=pct, digits=0 if metric == "n_evals" else 3) if rows else "—"
                cells.append(f"{f(st)} → **{f(cp)}**")
            L.append(f"| {name} | " + " | ".join(cells) + " |")
        L.append("")
    L.append("**Cost, tokens, time and failures per run** (structured → campaign; all specs)\n")
    L.append("| model | runs | input tokens / run | output tokens / run | cost / run (USD) | wall time / run (s) | failure rate |")
    L.append("|---|---|---|---|---|---|---|")
    for m in models:
        st = [r for r in (ag2.get(m, []) + ag3.get(m, [])) if r["spec"] in all_specs]
        cp = cp3.get(m, [])
        def pair(key: str, digits: int = 0) -> str:
            return " → ".join(_ms([float(r[key]) for r in rows], digits=digits) if rows else "—" for rows in (st, cp))
        L.append(f"| `{m}` | {len(st)} → {len(cp)} | {pair('input_tokens')} | {pair('output_tokens')} | {pair('cost_usd', 4)} | "
                 f"{pair('wall_s')} | {_fail_rate(st) if st else '—'} → {_fail_rate(cp) if cp else '—'} |")
    L.append("")
    if cp3:
        L.append("**What the campaign agent did** (tool sequence per run, condensed)\n")
        for m, rows in cp3.items():
            L.append(f"`{m}`:\n")
            for r in sorted(rows, key=lambda r: (r["spec"], r["seed"])):
                runs = ", ".join(f"run_dse({d['evals']})" for d in r.get("dse_runs", []))
                L.append(f"- {r['spec']} seed {r['seed']}: {' → '.join(r.get('ladder', [])) or '—'} [{runs}]"
                         + (f"; **failed**: {r['error'][:160]}" if r.get("failed") else "")
                         + (f"; L5 re-explore → `{r['l5'].get('selected_key')}`" if r.get("l5") else ""))
            L.append("")

    # ---- memory on/off ---------------------------------------------------
    mem = _load_rows(M3_DIRS["memory"])
    if mem:
        L.append("## Memory on vs off (campaign agent, fixed spec sequence, seeds 0–2)\n")
        L.append(f"Sequence: {' → '.join(MEMORY_SEQUENCE)}. Memory on: one LangGraph Store per seed, carried from spec to "
                 "spec (lessons written by code after each spec, plus the agent's own notes). Memory off: the campaign arm's "
                 "runs for the same spec and seed. The first spec of the sequence starts with an empty store in both "
                 "conditions. Store contents after the eval: `eval/data/campaign_m3_memory_store.json`.\n")
        L.append("| model | spec (position) | HV off → on | regret off → on | evals off → on | cost off → on (USD) |")
        L.append("|---|---|---|---|---|---|")
        for m, rows in mem.items():
            for i, name in enumerate(MEMORY_SEQUENCE):
                on = [r for r in rows if r["spec"] == name]
                off = [r for r in cp3.get(m, []) if r["spec"] == name and r["seed"] in {x["seed"] for x in on}]
                def c(key: str, pct: bool = False, digits: int = 3) -> str:
                    return " → ".join(_ms([float(r[key]) if r.get(key) is not None else None for r in rows_], pct=pct,
                                          signed=pct, digits=digits) if rows_ else "—" for rows_ in (off, on))
                L.append(f"| `{m}` | {name} ({i + 1}) | {c('hv_frac')} | {c('select_regret', True)} | {c('n_evals', digits=0)} | "
                         f"{c('cost_usd', digits=4)} |")
        L.append("")

    # ---- spend ------------------------------------------------------------
    rows = ledger("m3")
    if rows:
        L.append("## M3 spend\n")
        by: dict[str, float] = {}
        for r in rows:
            k2 = f"{r.get('arm', '?')}{' (' + r['note'] + ')' if r.get('note') else ''}"
            by[k2] = by.get(k2, 0.0) + float(r.get("cost_usd") or 0)
        L.append("| ledger entry | runs | provider-reported cost (USD) |")
        L.append("|---|---|---|")
        for k2 in sorted(by):
            n = sum(1 for r in rows if f"{r.get('arm', '?')}{' (' + r['note'] + ')' if r.get('note') else ''}" == k2)
            L.append(f"| {k2} | {n} | {by[k2]:.4f} |")
        L.append(f"| **total** | {len(rows)} | **{sum(by.values()):.4f}** |")
        L.append("")
        if KEY_USAGE_M3.exists():
            ku = json.loads(KEY_USAGE_M3.read_text())["snapshots"]
            L.append("Key usage snapshots (authoritative; `eval/data/key_usage_m3.json`): " + "; ".join(
                f"{k} {v['ts']} ${v['usage_usd']:.4f}" for k, v in ku.items()) + ".\n")


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
    sub.add_parser("baselines-m3").set_defaults(fn=cmd_baselines_m3)
    ku = sub.add_parser("key-usage")
    ku.add_argument("--tag", required=True)
    ku.set_defaults(fn=cmd_key_usage)
    for nm, fn in (("agent-m3", cmd_agent_m3), ("campaign-m3", cmd_campaign_m3), ("memory-m3", cmd_memory_m3)):
        p3 = sub.add_parser(nm)
        p3.add_argument("--model", required=True)
        p3.add_argument("--reasoning", default=None)
        p3.add_argument("--seeds", type=int, default=5)
        p3.add_argument("--specs", default="")
        p3.add_argument("--pilot", action="store_true")
        p3.add_argument("--force", action="store_true")
        p3.add_argument("--max-spend", type=float, default=M3_CAP, help="M3 spend cap (USD) from the ledger")
        p3.add_argument("--expected-cost", type=float, default=0.10)
        p3.set_defaults(fn=fn)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
