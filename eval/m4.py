"""Milestone 4 eval: the ASIC target, the fleet A/B, the L2 -> L1 feedback.

Subcommands are registered into ``eval/run_eval.py`` (:func:`register`)::

    python eval/run_eval.py ground-truth-m4      # ASIC specs, exhaustive; FPGA twins; family rankings
    python eval/run_eval.py baselines-m4         # NSGA-II / random on the ASIC specs, 5 seeds
    python eval/run_eval.py models-m4            # /api/v1/models check (free) -> eval/data/models_check_m4.json
    python eval/run_eval.py key-usage-m4 --tag before_eval
    python eval/run_eval.py agent-m4 --model qwen/qwen3.8-27b --reasoning off [--pilot]
    python eval/run_eval.py fleet-m4 --model qwen/qwen3.8-27b --reasoning off [--arm fleet|single] [--pilot]

Everything is written to M4's own files and directories; M1-M3 data is never
rewritten. ``report_m4`` appends the M4 section to ``results.md``.
"""

from __future__ import annotations

import argparse
import json
import pickle
import statistics
import time
from pathlib import Path
from typing import Any

from run_eval import (  # type: ignore[import-not-found]  # noqa: E402 - eval/ is on sys.path
    DATA, LEDGER, ROOT, SEEDS, _ms, _slim, _slim_sys, _slug, accuracy_table, build_grid, ground_truth, ledger,
    load_spec, run_baseline, score_run,
)

from hw_dse.spec import Spec

ASIC_SPECS = ("asic_low_area", "asic_power_50msps", "asic_multiaxis_control")
GT_M4_FILE = DATA / "ground_truth_m4.json"
BASELINES_M4 = DATA / "baselines_m4.json"
M4_DIRS = {"agent": DATA / "agent_m4", "fleet_ab": DATA / "fleet_m4", "pilot": DATA / "m4_pilot"}
KEY_USAGE_M4 = DATA / "key_usage_m4.json"
MODELS_CHECK_M4 = DATA / "models_check_m4.json"
M4_CAP = 5.0
GRID_CACHE = ROOT / "build" / "grids"
# The FPGA twin of each ASIC spec (for the family-ranking comparison): the same
# constraints, objectives and selection with the ASIC area metric replaced by
# the FPGA one. The twins are scored on the FPGA ground truth (M1 cost model).
AREA_TWIN = {"area_um2": "luts_plus_ffs", "gate_eq": "luts_plus_ffs"}


def asic_spec(name: str) -> Spec:
    return load_spec(ROOT / "specs" / "asic" / f"{name}.yaml")


def fpga_twin(s: Spec) -> Spec:
    d = s.model_dump()
    d["name"] = s.name + "__fpga_twin"
    d["target"] = "fpga-artix7"
    for o in d["objectives"]:
        if o["metric"] in AREA_TWIN:
            o["metric"], o["ref"] = AREA_TWIN[o["metric"]], o["ref"] / 10.0  # (ref only matters for HV)
    for c in d["constraints"]:
        c["metric"] = AREA_TWIN.get(c["metric"], c["metric"])
    d["select_by"] = AREA_TWIN.get(d["select_by"], d["select_by"])
    return Spec.model_validate(d)


def cached_grid(cost_model: Any) -> Any:
    """``build_grid`` (6-7 minutes for 635,040 designs), cached under build/grids/ by calibration id."""
    GRID_CACHE.mkdir(parents=True, exist_ok=True)
    path = GRID_CACHE / f"{cost_model.calibration_id}.pkl"
    if path.exists():
        g = pickle.loads(path.read_bytes())
        g.cost_model = cost_model
        # The cache is keyed by calibration id; check a spread of designs anyway.
        for i in range(0, len(g), 9973):
            e = cost_model.estimate(g.arch(i))
            if abs(e.fmax_mhz - g.fmax_mhz[i]) > 1e-9 or abs(e.area["ffs"] - g.ffs[i]) > 1e-9:
                raise SystemExit(f"stale grid cache {path}: delete it and re-run")
        return g
    g = build_grid(verbose=True, cost_model=cost_model)
    cm, g.cost_model = g.cost_model, None
    path.write_bytes(pickle.dumps(g))
    g.cost_model = cm
    return g


def _slim4(rec: dict[str, Any] | None, spec: Spec) -> dict[str, Any] | None:
    out = _slim_sys(rec, spec)
    if out is not None and rec is not None:
        for k in ("area_um2", "gate_eq"):
            if k in rec:
                out[k] = rec[k]
        if spec.target_kind == "asic":
            out.pop("luts", None)
            out.pop("luts_plus_ffs", None)
    return out


def family_bests(grid: Any, spec: Spec, system: str = "simulated") -> dict[str, Any]:
    """Per family: the best feasible design by the spec's selection rule (truth view)."""
    import numpy as np

    from hw_dse.benchmark import _feasible_mask
    from hw_dse.families import REGISTRY

    m = grid.metrics(spec, system) if spec.system is not None else grid.metrics(spec)
    feas = _feasible_mask(m, spec)
    sign = 1.0 if spec.select_direction == "min" else -1.0
    out: dict[str, Any] = {}
    for i, fam in enumerate(REGISTRY):
        idx = np.flatnonzero(feas & (grid.family == i))
        if not idx.size:
            out[fam] = None
            continue
        vals = sign * m[spec.select_by][idx]
        j = int(idx[int(np.argmin(vals))])
        out[fam] = {"key": grid.arch(j).key(), spec.select_by: float(m[spec.select_by][j]),
                    "throughput_msps": float(m["throughput_msps"][j]), "n_feasible": int(idx.size)}
    return out


def ranking(bests: dict[str, Any], spec: Spec) -> list[str]:
    sign = 1.0 if spec.select_direction == "min" else -1.0
    have = [f for f, b in bests.items() if b]
    return sorted(have, key=lambda f: sign * bests[f][spec.select_by])


def cmd_ground_truth_m4(_: argparse.Namespace) -> None:
    """Exhaustive ground truth on the ASIC target (system metrics simulated for the
    system spec, with the L1-bound view alongside), each ASIC spec's per-family
    bests, and the same for its FPGA twin (M1 cost model): does the family
    ranking differ between targets?"""
    import numpy as np

    from hw_dse.benchmark import _feasible_mask, select_design
    from hw_dse.evaluate import default_asic_cost_model, default_cost_model, evaluate

    accuracy_table.preload()
    t0 = time.time()
    ga = cached_grid(default_asic_cost_model())
    gf = cached_grid(default_cost_model())
    out: dict[str, Any] = {"cost_model": ga.cost_model.provenance, "fpga_cost_model": gf.cost_model.provenance}
    for name in ASIC_SPECS:
        s = asic_spec(name)
        gt = ground_truth(ga, s)
        row: dict[str, Any] = {
            "n_designs": gt["n_designs"], "n_feasible": gt["n_feasible"], "feasible": gt["feasible"],
            "hv_true": gt.get("hv_true", 0.0), "best_throughput_msps_any": gt["best_throughput_msps_any"],
            "selected": _slim4(gt["selected"], s), "front": [_slim4(r, s) for r in gt["front"]],
            "family_bests": family_bests(ga, s),
        }
        row["family_ranking"] = ranking(row["family_bests"], s)
        if s.system is not None:
            mb = ga.metrics(s, "bound")
            fb = _feasible_mask(mb, s)
            idx = np.flatnonzero(fb)
            sel = mb[s.select_by][idx]
            ties = idx[np.flatnonzero(sel == (sel.min() if s.select_direction == "min" else sel.max()))]
            bsel = select_design([evaluate(ga.arch(int(i)), s) for i in ties], s)
            row["n_feasible_l1_bound"] = int(fb.sum())
            row["l1_bound_selected"] = _slim4(bsel, s)
            row["l2_changes_winner"] = bool(bsel and gt["selected"] and bsel["key"] != gt["selected"]["key"])
            row["family_bests_l1_bound"] = family_bests(ga, s, "bound")
        tw = fpga_twin(s)
        gtw = ground_truth(gf, tw)
        row["fpga_twin"] = {"spec": tw.model_dump(), "n_feasible": gtw["n_feasible"],
                            "selected": _slim4(gtw["selected"], tw), "family_bests": family_bests(gf, tw)}
        row["fpga_twin"]["family_ranking"] = ranking(row["fpga_twin"]["family_bests"], tw)
        row["ranking_differs"] = row["family_ranking"] != row["fpga_twin"]["family_ranking"]
        row["winner_family_differs"] = (bool(gt["selected"] and gtw["selected"])
                                        and gt["selected"]["family"] != gtw["selected"]["family"])
        out[name] = row
        print(f"{name}: {gt['n_feasible']} feasible, selected {gt['selected']['key'] if gt['selected'] else None}; "
              f"ranking ASIC {row['family_ranking']} vs FPGA twin {row['fpga_twin']['family_ranking']}", flush=True)
    GT_M4_FILE.write_text(json.dumps(out, indent=1))
    print(f"wrote {GT_M4_FILE} in {time.time() - t0:.0f}s")


def load_gt_m4() -> dict[str, Any]:
    return json.loads(GT_M4_FILE.read_text())


def score_m4(records: list[dict[str, Any]], spec: Spec, declared_infeasible: bool | None,
             selected: dict[str, Any] | None) -> dict[str, Any]:
    """score_run against the ASIC ground truth; system metrics re-scored by L2 simulation."""
    if spec.system is not None:
        from hw_dse.l2.node import simulate_record

        records = [simulate_record(r, spec) for r in records]
        selected = simulate_record(selected, spec) if selected else None
    return score_run(records, spec, load_gt_m4()[spec.name], declared_infeasible=declared_infeasible,
                     selected=selected)


def cmd_baselines_m4(_: argparse.Namespace) -> None:
    from hw_dse.agent.summary import merged_front
    from hw_dse.benchmark import select_design
    from hw_dse.l2.node import l2_select

    accuracy_table.preload()
    out: dict[str, Any] = {}
    for name in ASIC_SPECS:
        s = asic_spec(name)
        for sampler in ("nsga2", "random"):
            for seed in SEEDS["m2"]:
                recs = run_baseline(s, sampler, seed)
                sel = select_design(merged_front(recs, s), s)
                if s.system is not None:
                    sel = l2_select(recs, sel, s)["selected"]
                sc = score_m4(recs, s, None if sel else True, sel)
                out[f"{name}|{sampler}|{seed}"] = {"spec": name, "method": sampler, "seed": seed, **sc}
                print(name, sampler, seed, "HV", sc["hv_frac"], "regret", sc["select_regret"], flush=True)
    BASELINES_M4.write_text(json.dumps(out, indent=1))
    print(f"wrote {BASELINES_M4}")


# ---------------------------------------------------------------------------
# Live runs: model check, key usage, ledger, the structured arm, the fleet A/B
# ---------------------------------------------------------------------------

M4_MODELS = ("qwen/qwen3.8-27b", "anthropic/claude-sonnet-5.5", "deepseek/deepseek-v4.1-flash")
FPGA_AB_SPECS = ("low_area_control", "multiaxis_control")  # the A/B's FPGA specs (one plain, one system)


def cmd_models_m4(_: argparse.Namespace) -> None:
    """Check (free, no key needed) that each model is listed with tools and structured_outputs."""
    import urllib.request

    with urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=60) as r:  # noqa: S310 - fixed URL
        data = json.loads(r.read())["data"]
    by_id = {m["id"]: m for m in data}
    out: dict[str, Any] = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                           "endpoint": "GET https://openrouter.ai/api/v1/models", "n_models_listed": len(data),
                           "required": ["tools", "structured_outputs"], "models": {}}
    for mid in M4_MODELS:
        m = by_id.get(mid)
        sp = sorted((m or {}).get("supported_parameters") or [])
        out["models"][mid] = {"listed": m is not None, "tools": "tools" in sp, "structured_outputs": "structured_outputs" in sp,
                              "ok": m is not None and "tools" in sp and "structured_outputs" in sp,
                              "pricing": (m or {}).get("pricing"), "context_length": (m or {}).get("context_length"),
                              "supported_parameters": sp}
        print(mid, out["models"][mid]["ok"])
    MODELS_CHECK_M4.write_text(json.dumps(out, indent=1))
    print(f"wrote {MODELS_CHECK_M4}")


def cmd_key_usage_m4(args: argparse.Namespace) -> None:
    """Record the key's usage and limit (free endpoint) under a tag; the key itself is never recorded."""
    from run_eval import _key_usage  # type: ignore[import-not-found]

    data = json.loads(KEY_USAGE_M4.read_text()) if KEY_USAGE_M4.exists() else {
        "note": "OpenRouter GET /api/v1/key (free), read with the key from the environment; the key itself is never "
                "recorded.", "m4_spend_cap_usd": M4_CAP, "snapshots": {}}
    data["snapshots"][args.tag] = _key_usage()
    KEY_USAGE_M4.write_text(json.dumps(data, indent=1))
    print(args.tag, data["snapshots"][args.tag])


def ledger_add(model: str, spec: str, seed: int, cost: float, arm: str, note: str = "") -> None:
    with open(LEDGER, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"model": model, "spec": spec, "seed": seed, "cost_usd": cost, "arm": arm,
                             "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "milestone": "m4",
                             **({"note": note} if note else {})}) + "\n")


def spend_m4() -> float:
    return sum(float(r.get("cost_usd") or 0.0) for r in ledger("m4"))


def cap_ok(model: str, arm: str, default: float, cap: float) -> bool:
    prior = [float(r.get("cost_usd") or 0) for r in ledger("m4") if r["model"] == model and r.get("arm") == arm]
    exp = statistics.mean(prior) if prior else default
    spent = spend_m4()
    # The key's own usage is authoritative (calls that fail inside the client report no
    # usage to the ledger): measured against the first M4 snapshot, read before the run
    # starts (outside its timed window).
    if KEY_USAGE_M4.exists():
        from run_eval import _key_usage  # type: ignore[import-not-found]

        first = list(json.loads(KEY_USAGE_M4.read_text())["snapshots"].values())[0]
        try:
            spent = max(spent, float(_key_usage()["usage_usd"]) - float(first["usage_usd"]))
        except Exception as exc:  # noqa: BLE001 - no reading: refuse rather than risk the cap
            print(f"STOP: could not read the key's usage ({type(exc).__name__})")
            return False
    if spent + 2 * exp > cap:
        print(f"STOP: M4 spend ${spent:.4f} + 2x expected next {arm} run ${exp:.4f} would pass ${cap}")
        return False
    return True


def any_spec(name: str) -> Spec:
    from hw_dse.campaign.tools import spec_path

    return load_spec(spec_path(name))


def score_any(records: list[dict[str, Any]], spec: Spec, declared: bool | None,
              selected: dict[str, Any] | None) -> dict[str, Any]:
    """Score against the right ground truth: ASIC (M4), FPGA system (M3, simulated) or FPGA (M1/M2)."""
    if spec.target_kind == "asic":
        return score_m4(records, spec, declared, selected)
    if spec.system is not None:
        from run_eval import score_m3  # type: ignore[import-not-found]

        return score_m3(records, spec, declared, selected)
    from run_eval import load_gt  # type: ignore[import-not-found]

    return score_run(records, spec, load_gt()[spec.name], declared_infeasible=declared, selected=selected)


def _model_dir(model: str, reasoning: str | None) -> str:
    return _slug(model) + (f"__reasoning-{reasoning}" if reasoning else "")


def _row_common(res: dict[str, Any], name: str, seed: int, args: argparse.Namespace, arm: str, wall: float) -> dict[str, Any]:
    s = any_spec(name)
    sc = score_any(res["evaluations_ordered"], s, res["llm_declared_infeasible"], res["selected"])
    return {"milestone": "m4", "arm": arm, "pilot": bool(args.pilot), "spec": name, "target": s.target, "seed": seed,
            "provider": "openrouter", "model_requested": args.model, "models_served": res["models_served"],
            "reasoning": args.reasoning or "provider default", "status": res["status"],
            "llm_calls": res["llm"]["calls"], "llm_failures": res["llm"]["failures"],
            "input_tokens": res["llm"]["input_tokens"], "output_tokens": res["llm"]["output_tokens"],
            "cost_usd": res["llm"]["cost_usd"], "wall_s": round(wall, 1), "decisions": res["decisions"],
            "l1_selected_key": (res.get("selected_l1") or {}).get("key"),
            "l2_winner_changed": bool((res.get("l2") or {}).get("winner_changed")),
            "l2_feedback": (res.get("l2_feedback") or {}).get("status"),
            "back_annotation_winner_changed": bool((res.get("back_annotation") or {}).get("winner_changed")),
            "failed": False, **sc}


def cmd_agent_m4(args: argparse.Namespace) -> None:
    """The structured graph, one run per (spec, seed), sequentially (wall-clock measured alone).
    Default specs: the ASIC ones; ``--specs`` adds the A/B's FPGA specs (``--arm single``)."""
    from hw_dse.agent.runner import run_agent

    accuracy_table.preload()
    arm = args.arm or "structured"
    base = M4_DIRS["pilot"] if args.pilot else (M4_DIRS["agent"] if arm == "structured" else M4_DIRS["fleet_ab"])
    outdir = base / (arm if arm != "structured" else "") / _model_dir(args.model, args.reasoning)
    outdir.mkdir(parents=True, exist_ok=True)
    names = args.specs.split(",") if args.specs else list(ASIC_SPECS)
    for seed in SEEDS["m2"][: args.seeds]:
        for name in names:
            path = outdir / f"{name}_seed{seed}.json"
            if path.exists() and not args.force:
                print(f"skip (exists): {path.name}")
                continue
            # The ledger's ``arm`` is the kind of run whose cost predicts the next one
            # (an A/B single-arm run is a structured-graph run); the A/B arm is the note.
            if not cap_ok(args.model, "structured", args.expected_cost, args.max_spend):
                return
            s = any_spec(name)
            t0 = time.time()
            res = run_agent(spec=s, provider="openrouter", model=args.model, seed=seed, reasoning=args.reasoning,
                            run_root=ROOT / "runs" / ("eval_m4_pilot" if args.pilot else "eval_m4") / arm)
            wall = time.time() - t0
            row = {**_row_common(res, name, seed, args, arm, wall), "rounds": res["rounds"],
                   "coverage_rounds": res["coverage_rounds"], "structured_method": res["structured_method"],
                   "run_dir": str(Path(res["run_dir"]).relative_to(ROOT)), "overrides": res["overrides"]}
            ledger_add(args.model, name, seed, row["cost_usd"], "structured", "pilot" if args.pilot else arm)
            path.write_text(json.dumps(row, indent=1, default=str))
            print(f"[{arm}] {name} seed {seed}: {res['status']}, HV {row['hv_frac']}, regret {row['select_regret']}, "
                  f"${row['cost_usd']:.4f}, {row['wall_s']}s", flush=True)


def cmd_fleet_m4(args: argparse.Namespace) -> None:
    """The fleet arm of the A/B: the code-orchestrated fleet at the spec's total budget, sequentially."""
    from hw_dse.agent.llm import make_llm
    from hw_dse.agent.trace import Tracer
    from hw_dse.fleet.coordinator import run_fleet

    accuracy_table.preload()
    # v1: the first A/B (phase-2 members started cold; member minimum 10). v2, after
    # review: phase-2 studies warm-started from the Store, spendable member minimum.
    v2 = args.fleet_version == "v2"
    arm_dir = "fleet_v2" if v2 else "fleet"
    outdir = (M4_DIRS["pilot"] / "fleet" if args.pilot else M4_DIRS["fleet_ab"] / arm_dir) / _model_dir(args.model, args.reasoning)
    outdir.mkdir(parents=True, exist_ok=True)
    names = args.specs.split(",") if args.specs else list(ASIC_SPECS + FPGA_AB_SPECS)
    for seed in SEEDS["m2"][: args.seeds]:
        for name in names:
            path = outdir / f"{name}_seed{seed}.json"
            if path.exists() and not args.force:
                print(f"skip (exists): {path.name}")
                continue
            if not cap_ok(args.model, "fleet", args.expected_cost, args.max_spend):
                return
            s = any_spec(name)
            root = (ROOT / "runs" / ("fleet_m4_pilot" if args.pilot else ("fleet_m4_v2" if v2 else "fleet_m4")) / name
                    / f"seed{seed}-{time.strftime('%Y%m%d-%H%M%S')}")

            def factory(member: str, phase: int) -> Any:
                return make_llm("openrouter", args.model, tracer=Tracer(), reasoning=args.reasoning)

            t0 = time.time()
            res = run_fleet(s, factory, seed=seed, run_root=root, warm_start=v2)
            wall = time.time() - t0
            members = [{**mm, "run_dir": str(Path(mm["run_dir"]).relative_to(ROOT))} for mm in res["members"]]
            row = {**_row_common(res, name, seed, args, arm_dir, wall), "members": members, "fleet_version": args.fleet_version,
                   "warm_start": res["warm_start"],
                   "phase2_budgets": res["phase2_budgets"], "lessons": res["lessons"],
                   "store_evaluations_by_member": res["store_evaluations_by_member"],
                   "store_distinct_designs": res["store_distinct_designs"],
                   "run_dir": str(root.relative_to(ROOT))}
            ledger_add(args.model, name, seed, row["cost_usd"], "fleet", "pilot" if args.pilot else ("v2" if v2 else ""))
            path.write_text(json.dumps(row, indent=1, default=str))
            print(f"[{arm_dir}] {name} seed {seed}: {res['status']}, HV {row['hv_frac']}, regret {row['select_regret']}, "
                  f"evals {row['n_evals']}, ${row['cost_usd']:.4f}, {row['wall_s']}s", flush=True)


# ---------------------------------------------------------------------------
# L2 -> L1 feedback, offline on recorded data
# ---------------------------------------------------------------------------

def _recorded_m3_structured() -> list[tuple[str, list[dict[str, Any]]]]:
    """Each committed M3 structured run's L1 evaluations, rebuilt from its archived evaluation keys."""
    from hw_dse.agent.replay import m3_runs, recorded_keys
    from hw_dse.evaluate import evaluate
    from hw_dse.families import ArchConfig

    out = []
    for row in m3_runs():
        s = any_spec(row["spec"])
        out.append((f"M3 structured {row['model_requested'].split('/')[-1]} {row['spec']} s{row['seed']}",
                    [evaluate(ArchConfig.from_key(k), s) for k in recorded_keys(row["_trace_dir"])]))
    return out


def _recorded_m3_campaign_pools() -> list[tuple[str, list[dict[str, Any]]]]:
    import gzip

    from hw_dse.evaluate import evaluate
    from hw_dse.families import ArchConfig

    out = []
    for p in sorted((DATA / "traces" / "m3").glob("*/*/*/pool_keys.json.gz")):
        spec_name = p.parent.parent.name
        s = any_spec(spec_name)
        if s.system is None:
            continue
        keys = json.loads(gzip.decompress(p.read_bytes()))
        keys = keys["keys"] if isinstance(keys, dict) else keys
        out.append((f"M3 campaign pool {p.parent.relative_to(DATA / 'traces' / 'm3')}",
                    [evaluate(ArchConfig.from_key(k), s) for k in keys]))
    return out


def cmd_l2_feedback_m4(_: argparse.Namespace) -> None:
    """Where does the L2 -> L1 feedback fire? Recorded runs, baselines, and the constructed spec,
    with an ablation (same re-exploration budget, uncorrected bound)."""
    import numpy as np

    from hw_dse.agent.llm import HeuristicArchitect
    from hw_dse.agent.runner import run_agent
    from hw_dse.agent.summary import merged_front
    from hw_dse.benchmark import _feasible_mask, select_design
    from hw_dse.evaluate import default_cost_model
    from hw_dse.l2.feedback import feedback, fires
    from hw_dse.l2.node import l2_select

    accuracy_table.preload()
    t0 = time.time()

    def check(recs: list[dict[str, Any]], s: Spec) -> dict[str, Any]:
        sel = select_design(merged_front(recs, s), s)
        l2 = l2_select(recs, sel, s) if sel else {"status": "no L1 selection"}
        return {"fires": fires(l2), "n_l1_feasible": l2.get("n_l1_feasible"), "n_l2_pass": l2.get("n_simulated_feasible")}

    recorded: list[dict[str, Any]] = []
    for label, recs in _recorded_m3_structured() + _recorded_m3_campaign_pools():
        name = label.split()[-2] if label.startswith("M3 structured") else label.split()[3].split("/")[1]
        recorded.append({"run": label, **check(recs, any_spec(name))})
    for name in ("bursty_offload", "multiaxis_control", "asic_multiaxis_control"):
        s = any_spec(name)
        for sampler in ("nsga2", "random"):
            for seed in SEEDS["m2"]:
                recorded.append({"run": f"baseline {sampler} {name} s{seed}", **check(run_baseline(s, sampler, seed), s)})
    live = []
    for d in (M4_DIRS["agent"], M4_DIRS["fleet_ab"] / "single", *(M4_DIRS["fleet_ab"] / a for a in FLEET_ARMS)):
        for rows in _rows(d).values():
            for r in rows:
                if any_spec(r["spec"]).system is not None:
                    live.append({"run": f"M4 {r['arm']} {r['model_requested'].split('/')[-1]} {r['spec']} s{r['seed']}",
                                 "fires": r.get("l2_feedback") is not None, "outcome": r.get("l2_feedback")})
    # The constructed spec: ground truth, then searches that can and cannot see the passing region.
    s = any_spec("l2_feedback_bursty")
    grid = cached_grid(default_cost_model())
    m = grid.metrics(s, "simulated")
    fs = _feasible_mask(m, s)
    fb_ = _feasible_mask(grid.metrics(s, "bound"), s)
    idx = np.flatnonzero(fs)
    best = float(m[s.select_by][idx].min())
    gtrow = {"n_feasible_simulated": int(fs.sum()), "n_feasible_l1_bound": int(fb_.sum()),
             "best_" + s.select_by: best, "winner_key": grid.arch(int(idx[np.argmin(m[s.select_by][idx])])).key()}
    constructed = []
    searches: list[tuple[str, list[dict[str, Any]], int]] = []
    for sampler in ("nsga2", "random"):
        for seed in SEEDS["m2"]:
            searches.append((f"{sampler} s{seed}", run_baseline(s, sampler, seed), seed))
    import tempfile
    for seed in SEEDS["m2"]:
        with tempfile.TemporaryDirectory() as tmp:
            res = run_agent(s, llm=HeuristicArchitect(), seed=seed, run_root=Path(tmp),
                            options={"l2_feedback": {"enabled": False}})
        searches.append((f"rule-based architect s{seed}", res["evaluations_ordered"], seed))
    for label, recs, seed in searches:
        c = check(recs, s)
        row: dict[str, Any] = {"search": label, **c}
        if c["fires"]:
            for tag, corr in (("corrected", True), ("ablation_uncorrected", False)):
                out = feedback(s, recs, seed=seed, correct=corr)
                sel = out["selected"]
                row[tag] = {"status": out["status"], "n_evals": out["n_evals"], "selected_key": out["selected_key"],
                            "regret": (float(sel[s.select_by]) - best) / best if sel else None,
                            "rounds": [{k: v for k, v in r.items() if k != "corrections"} for r in out["rounds"]]}
        constructed.append(row)
    n_rec = sum(r["fires"] for r in recorded)
    fired = [r for r in constructed if r["fires"]]
    rec_ok = sum(1 for r in fired if r["corrected"]["status"] == "recovered")
    abl_ok = sum(1 for r in fired if r["ablation_uncorrected"]["status"] == "recovered")
    reg = [r["corrected"]["regret"] for r in fired if r["corrected"]["regret"] is not None]
    md = (f"Recorded data (M3 structured runs rebuilt from their archived evaluations, M3 campaign pools, NSGA-II/random "
          f"baselines on every system spec, and the live M4 runs on the system specs): the feedback **fires in "
          f"{n_rec} of {len(recorded)} recorded searches and {sum(r['fires'] for r in live)} of {len(live)} live M4 runs**: "
          "L2 always found a passing design among the L1-feasible ones, so on the committed specs it never fires.\n\n"
          f"The constructed spec `l2_feedback_bursty` (bursts of 32 at 130 MS/s, throughput >= 130 MS/s, p99 <= 0.4 us, "
          f"{gtrow['n_feasible_l1_bound']:,} designs pass the L1 bound, {gtrow['n_feasible_simulated']:,} the simulation; "
          f"true winner `{gtrow['winner_key']}`): it fires in **{len(fired)} of {len(constructed)}** searches "
          f"(5 NSGA-II, 5 random, 5 rule-based-architect runs of 400 evaluations). With the correction it recovers a "
          f"passing design in **{rec_ok} of {len(fired)}** (regret {_pct(reg)}); the ablation, the same re-exploration "
          f"budget screened with the uncorrected bound, recovers in **{abl_ok} of {len(fired)}**.\n\n"
          "| search | L1-feasible | pass L2 | fires | corrected: outcome, evals, regret | uncorrected: outcome, evals |\n"
          "|---|---|---|---|---|---|\n" + "".join(
              f"| {r['search']} | {r['n_l1_feasible']} | {r['n_l2_pass']} | {'yes' if r['fires'] else 'no'} | "
              + (f"{r['corrected']['status']}, {r['corrected']['n_evals']}, "
                 f"{'n/a' if r['corrected']['regret'] is None else format(r['corrected']['regret'] * 100, '+.1f') + '%'} | "
                 f"{r['ablation_uncorrected']['status']}, {r['ablation_uncorrected']['n_evals']} |" if r["fires"] else "— | — |")
              + "\n" for r in constructed))
    L2F_FILE.write_text(json.dumps({"recorded": recorded, "live_m4": live, "constructed_gt": gtrow,
                                    "constructed": constructed, "summary_md": md}, indent=1, default=str))
    print(md)
    print(f"wrote {L2F_FILE} in {time.time() - t0:.0f}s")


# ---------------------------------------------------------------------------
# Registration into run_eval.py
# ---------------------------------------------------------------------------

def register(sub: Any) -> None:
    sub.add_parser("ground-truth-m4").set_defaults(fn=cmd_ground_truth_m4)
    sub.add_parser("baselines-m4").set_defaults(fn=cmd_baselines_m4)
    sub.add_parser("models-m4").set_defaults(fn=cmd_models_m4)
    sub.add_parser("l2-feedback-m4").set_defaults(fn=cmd_l2_feedback_m4)
    ku = sub.add_parser("key-usage-m4")
    ku.add_argument("--tag", required=True)
    ku.set_defaults(fn=cmd_key_usage_m4)
    for nm, fn in (("agent-m4", cmd_agent_m4), ("fleet-m4", cmd_fleet_m4)):
        p4 = sub.add_parser(nm)
        p4.add_argument("--model", required=True)
        p4.add_argument("--reasoning", default=None)
        p4.add_argument("--seeds", type=int, default=5)
        p4.add_argument("--specs", default="")
        p4.add_argument("--arm", default=None, help="agent-m4: structured (default) or single (the A/B's FPGA specs)")
        p4.add_argument("--pilot", action="store_true")
        p4.add_argument("--force", action="store_true")
        p4.add_argument("--max-spend", type=float, default=M4_CAP, help="M4 spend cap (USD) from the ledger")
        p4.add_argument("--expected-cost", type=float, default=0.10)
        if nm == "fleet-m4":
            p4.add_argument("--fleet-version", choices=("v1", "v2"), default="v2",
                            help="v1: the first A/B's fleet (cold phase 2); v2: phase 2 warm-started from the Store")
        p4.set_defaults(fn=fn)


# ---------------------------------------------------------------------------
# results.md, milestone 4 section
# ---------------------------------------------------------------------------

L2F_FILE = DATA / "l2_feedback_m4.json"


def _rows(d: Path) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for p in sorted(d.glob("*/*.json")) if d.exists() else []:
        r = json.loads(p.read_text())
        out.setdefault(r["model_requested"] + ("" if r["reasoning"] == "provider default" else f", reasoning {r['reasoning']}"),
                       []).append(r)
    return out


def _pct(xs: list[float | None]) -> str:
    return _ms(xs, pct=True, signed=True)


def _fails(rows: list[dict[str, Any]]) -> str:
    bad = sum(1 for r in rows if not r["selected_meets_spec"] and not r.get("declared_infeasible"))
    return f"{bad}/{len(rows)}"


FLEET_ARMS = ("fleet", "fleet_v2")


def ab_arms() -> dict[str, dict[str, list[dict[str, Any]]]]:
    """model -> {"single": rows, "fleet": rows, "fleet_v2": rows}; the single arm on the ASIC specs
    is the ASIC structured eval. A model's single arm counts only the (spec, seed) pairs one of its
    fleet arms ran; :func:`paired` pairs them run by run."""
    single = _rows(M4_DIRS["agent"])
    for k, v in _rows(M4_DIRS["fleet_ab"] / "single").items():
        single.setdefault(k, []).extend(v)
    fleets = {a: _rows(M4_DIRS["fleet_ab"] / a) for a in FLEET_ARMS}
    out = {}
    for m in fleets["fleet"]:
        fx = {a: fleets[a].get(m, []) for a in FLEET_ARMS}
        pairs = {(r["spec"], r["seed"]) for rs in fx.values() for r in rs}
        out[m] = {"single": [r for r in single.get(m, []) if (r["spec"], r["seed"]) in pairs], **fx}
    return out


def paired(single: list[dict[str, Any]], fleet: list[dict[str, Any]], metric: str) -> list[float]:
    """fleet - single on ``metric``, one difference per (spec, seed) both arms ran (sorted by spec, seed)."""
    s = {(r["spec"], r["seed"]): r for r in single}
    out = []
    for r in sorted(fleet, key=lambda r: (r["spec"], r["seed"])):
        x = s.get((r["spec"], r["seed"]))
        if x is not None and r.get(metric) is not None and x.get(metric) is not None:
            out.append(float(r[metric]) - float(x[metric]))
    return out


def paired_tests(arms: dict[str, dict[str, list[dict[str, Any]]]]) -> list[dict[str, Any]]:
    """Per model and fleet arm (and pooled over models for each fleet arm): sign test and paired t
    on fleet - single, for HV fraction and selection regret."""
    from hw_dse.stats import paired_t, sign_test

    rows = []
    for arm in FLEET_ARMS:
        pool: dict[str, list[float]] = {"hv_frac": [], "select_regret": []}
        n_models = 0
        for m, a in arms.items():
            if not a.get(arm):
                continue
            n_models += 1
            row: dict[str, Any] = {"model": m, "arm": arm}
            for met in pool:
                d = paired(a["single"], a[arm], met)
                pool[met] += d
                row[met] = {"sign": sign_test(d), "t": paired_t(d)}
            rows.append(row)
        if n_models > 1:
            rows.append({"model": "pooled", "arm": arm,
                         **{met: {"sign": sign_test(d), "t": paired_t(d)} for met, d in pool.items()}})
    return rows


def report_m4(L: list[str]) -> None:
    """Milestone 4 section of results.md (appended; M1-M3 sections untouched)."""
    if not GT_M4_FILE.exists():
        return
    import csv as _csv

    from hw_dse.evaluate import evaluate
    from hw_dse.families import ArchConfig

    gt = load_gt_m4()
    L.append("# Milestone 4: an ASIC target, a fleet of agents, L2 -> L1 feedback\n")
    L.append("Generated from committed data like everything above. *measured (yosys 0.33 + OpenSTA 3.1.0, "
             "sky130_fd_sc_hd, tt_025C_1v80)* = this repository's ASIC flow; *estimate* on the ASIC target = "
             f"`{gt['cost_model']}`. FPGA numbers are unchanged from M1-M3 (the M1 two-anchor model).\n")

    cal = json.loads((DATA / "asic_calibration.json").read_text())
    L.append("## ASIC cost model: fit and leave-one-out\n")
    L.append(f"{cal['calibration']['n_points']} synthesised designs over all four families "
             "(`eval/data/asic_synthesis.csv`; report `eval/data/asic_calibration.md`). RMS error, %:\n")
    L.append("| family | n | area in / LOO | FFs in / LOO | Fmax in / LOO | power (vs OpenSTA) in / LOO |")
    L.append("|---|---|---|---|---|---|")
    ins, loo = cal["summary"]["in_sample"], cal["summary"]["leave_one_out"]
    for fam in ("all", "iterative", "unrolled_k", "pipelined", "pipelined_m"):
        n = loo[fam].get("n", cal["calibration"]["n_points"])
        L.append(f"| {fam} | {n} | " + " | ".join(f"{ins[fam][m]:.1f} / {loo[fam][m]:.1f}"
                                                for m in ("area_um2", "ffs", "fmax_mhz", "power_mw")) + " |")
    L.append("")

    # ---- ground truth + ranking ----------------------------------------
    L.append("## ASIC specs: exhaustive ground truth and the family ranking on both targets\n")
    L.append("Per spec, the best design of each family by the spec's selection rule (system metrics simulated). The "
             "FPGA twin is the same spec with the area metric replaced by LUTs + FFs, scored on the FPGA ground "
             "truth (M1 cost model).\n")
    L.append("| spec | feasible | true winner | ASIC family ranking | FPGA twin ranking | ranking differs | FPGA twin winner |")
    L.append("|---|---|---|---|---|---|---|")
    for name in ASIC_SPECS:
        g = gt[name]
        s = asic_spec(name)
        L.append(f"| {name} | {g['n_feasible']:,} | `{g['selected']['key']}` ({s.select_by} {g['selected'][s.select_by]:.4g}) | "
                 f"{' < '.join(g['family_ranking'])} | {' < '.join(g['fpga_twin']['family_ranking'])} | "
                 f"{'yes' if g['ranking_differs'] else 'no'} | `{g['fpga_twin']['selected']['key']}` |")
    L.append("")
    L.append("| spec | family | ASIC best (selection metric) | ratio to the ASIC winner | FPGA twin best | ratio to the FPGA winner |")
    L.append("|---|---|---|---|---|---|")
    for name in ASIC_SPECS:
        g, s = gt[name], asic_spec(name)
        tw = fpga_twin(s)
        wa = g["selected"][s.select_by]
        wf = g["fpga_twin"]["selected"][tw.select_by]
        for fam, b in g["family_bests"].items():
            bf = g["fpga_twin"]["family_bests"][fam]
            if not b and not bf:
                continue
            ca = f"`{b['key']}` {b[s.select_by]:.4g}" if b else "none"
            ra = f"{b[s.select_by] / wa:.2f}" if b else "—"
            cf = f"`{bf['key']}` {bf[tw.select_by]:.4g}" if bf else "none"
            rf = f"{bf[tw.select_by] / wf:.2f}" if bf else "—"
            L.append(f"| {name} | {fam} | {ca} | {ra} | {cf} | {rf} |")
    L.append("")
    sys_name = [n for n in ASIC_SPECS if asic_spec(n).system is not None][0]
    gs = gt[sys_name]
    L.append(f"`{sys_name}`: {gs['n_feasible_l1_bound']:,} designs pass the L1 bound and {gs['n_feasible']:,} the "
             f"simulation; the bound's winner `{gs['l1_bound_selected']['key']}` "
             f"({gs['l1_bound_selected']['area_um2']:.0f} um2) misses the deadline in simulation, so L2 changes the "
             f"winner to `{gs['selected']['key']}` ({gs['selected']['area_um2']:.0f} um2): "
             f"{'yes' if gs['l2_changes_winner'] else 'no'}.\n")

    # ---- held-out validation -------------------------------------------
    vcsv = DATA / "asic_validation.csv"
    if vcsv.exists():
        from hw_dse.synth.asic import load_csv

        L.append("## Held-out sky130 check of the ground-truth designs\n")
        L.append("Each spec's per-family optima, the FPGA twin's optima and the L1-bound pick, synthesised and timed "
                 "(`eval/data/asic_validation.csv`, never fitted), against the model's estimates; *meets* = the "
                 "spec's constraints with the measured numbers (system metrics simulated at the measured clock).\n")
        L.append("| design | area um2 meas / est (err) | Fmax MHz meas / est (err) | power mW (100 MHz) meas | meets: asic_low_area / asic_power_50msps / asic_multiaxis_control |")
        L.append("|---|---|---|---|---|")
        from hw_dse.agent.backannotate import _MeasuredAsicCost
        from hw_dse.l2.node import simulate_record

        for p in load_csv(vcsv):
            e = evaluate(p.arch, asic_spec(ASIC_SPECS[0]))
            meets = []
            for name in ASIC_SPECS:
                sp = asic_spec(name)
                r = evaluate(p.arch, sp, cost_model=_MeasuredAsicCost(p))  # type: ignore[arg-type]
                if sp.system is not None:
                    r = simulate_record(r, sp)
                meets.append("yes" if r["feasible"] else "no")
            L.append(f"| `{p.arch.key()}` | {p.area_um2:.0f} / {e['area_um2']:.0f} ({(e['area_um2'] / p.area_um2 - 1) * 100:+.1f}%) | "
                     f"{p.fmax_mhz:.1f} / {e['fmax_mhz']:.1f} ({(e['fmax_mhz'] / p.fmax_mhz - 1) * 100:+.1f}%) | "
                     f"{p.power_mw:.3f} | {' / '.join(meets)} |")
        L.append("")

    # ---- ASIC eval ---------------------------------------------------------
    base = list(json.loads(BASELINES_M4.read_text()).values()) if BASELINES_M4.exists() else []
    agents = _rows(M4_DIRS["agent"])
    L.append("## ASIC specs: structured graph vs baselines (5 seeds, 400 evaluations)\n")
    L.append("Scored on the ASIC ground truth; for the system spec on *simulated* feasibility. Mean ± population std.\n")
    for metric, title in (("hv_frac", "HV fraction"), ("select_regret", "Selection regret")):
        L.append(f"**{title}**\n")
        L.append("| spec | NSGA-II | random | " + " | ".join(f"`{m}`" for m in agents) + " |")
        L.append("|---|---|---|" + "---|" * len(agents))
        for name in ASIC_SPECS:
            f = (lambda xs: _pct(xs)) if metric == "select_regret" else (lambda xs: _ms(xs))
            cells = [f([r[metric] for r in base if r["spec"] == name and r["method"] == k]) for k in ("nsga2", "random")]
            cells += [f([r[metric] for r in agents[m] if r["spec"] == name]) for m in agents]
            L.append(f"| {name} | " + " | ".join(cells) + " |")
        L.append("")
    L.append("| model | runs | selected meets spec | L2 changed the L1 pick | back-annotation flags a winner change | cost / run | wall / run (s) |")
    L.append("|---|---|---|---|---|---|---|")
    for m, rs in agents.items():
        L.append(f"| `{m}` | {len(rs)} | {sum(r['selected_meets_spec'] for r in rs)}/{len(rs)} | "
                 f"{sum(r['l2_winner_changed'] for r in rs)} | {sum(r['back_annotation_winner_changed'] for r in rs)} | "
                 f"${statistics.mean(r['cost_usd'] for r in rs):.4f} | {_ms([r['wall_s'] for r in rs], digits=0)} |")
    L.append("")

    # ---- fleet A/B ---------------------------------------------------------
    arms = ab_arms()
    if arms:
        L.append("## A/B: single structured graph vs the code-orchestrated fleet\n")
        L.append(f"Same specs ({', '.join(ASIC_SPECS + FPGA_AB_SPECS)}), seeds 0-4 and total L1 budget (400 "
                 "evaluations). Fleet = two members (fsm, pipelined), half the budget split equally, the rest by "
                 "share of the merged front. Wall-clock: every run was started after the previous one finished, "
                 "with nothing else running (the fleet's two members run in parallel threads inside its run). "
                 "Failure = the selected design does not meet the spec (excluding a correct infeasible call); "
                 "failed LLM calls are counted separately. Mean ± population std over all runs of the arm.\n")
        L.append("| model | arm | runs | HV fraction | selection regret | L1 evals | input tokens | output tokens | "
                 "cost / run (USD) | failures | failed LLM calls | wall / run (s) |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for m, a in arms.items():
            for arm in ("single",) + FLEET_ARMS:
                rs = a[arm]
                if not rs:
                    continue
                L.append(f"| `{m}` | {arm} | {len(rs)} | {_ms([r['hv_frac'] for r in rs])} | "
                         f"{_pct([r['select_regret'] for r in rs])} | {_ms([float(r['n_evals']) for r in rs], digits=0)} | "
                         f"{_ms([r['input_tokens'] for r in rs], digits=0)} | {_ms([r['output_tokens'] for r in rs], digits=0)} | "
                         f"{_ms([r['cost_usd'] for r in rs], digits=4)} | {_fails(rs)} | "
                         f"{sum(int(r['llm_failures']) for r in rs)} | {_ms([r['wall_s'] for r in rs], digits=0)} |")
        L.append("")
        L.append("`fleet_v2` (run after review, Qwen only): the same fleet with each phase-2 study warm-started from "
                 "the Store (the fleet's stored front designs of its family, as NSGA-II seeds) and a member minimum "
                 "budget of 20 that the 40% coverage reserve can always spend. `fleet` is the first A/B's fleet "
                 "(phase-2 members started cold, minimum 10).\n")
        L.append("**Paired tests** (fleet − single on the same spec and seed; sign test exact, two-sided, ties "
                 "dropped; paired t two-sided). HV: + = fleet higher. Regret: + = fleet worse.\n")
        L.append("| model | fleet arm | pairs | HV: fleet higher / lower | HV sign p | HV mean diff | HV t | HV t p | "
                 "regret: fleet lower / higher | regret sign p | regret mean diff (pts) | regret t | regret t p |")
        L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")

        def _f(x: Any, fmt: str) -> str:
            return "n/a" if x is None else format(x, fmt)

        for row in paired_tests(arms):
            h, g = row["hv_frac"], row["select_regret"]
            L.append(f"| `{row['model']}` | {row['arm']} | {h['t']['n']} | {h['sign']['positive']} / {h['sign']['negative']} | "
                     f"{h['sign']['p']:.3f} | {_f(h['t']['mean'], '+.3f')} | {_f(h['t']['t'], '.2f')} | {_f(h['t']['p'], '.3f')} | "
                     f"{g['sign']['negative']} / {g['sign']['positive']} | {g['sign']['p']:.3f} | "
                     f"{_f(None if g['t']['mean'] is None else g['t']['mean'] * 100, '+.1f')} | {_f(g['t']['t'], '.2f')} | "
                     f"{_f(g['t']['p'], '.3f')} |")
        L.append("")
        L.append("Per spec (HV fraction / regret, single → fleet):\n")
        L.append("| spec | " + " | ".join(f"`{m}`" for m in arms) + " |")
        L.append("|---|" + "---|" * len(arms))
        for name in ASIC_SPECS + FPGA_AB_SPECS:
            cells = []
            for m, a in arms.items():
                sx = [r for r in a["single"] if r["spec"] == name]
                fx = [r for r in a["fleet"] if r["spec"] == name]
                cells.append(f"{_ms([r['hv_frac'] for r in sx])} → {_ms([r['hv_frac'] for r in fx])}; "
                             f"{_pct([r['select_regret'] for r in sx])} → {_pct([r['select_regret'] for r in fx])}")
            L.append(f"| {name} | " + " | ".join(cells) + " |")
        L.append("")
        L.append("**Throughput, measured** (L1 evaluations per hour of wall-clock, one run at a time; cost per spec = "
                 "mean provider-reported cost of one 400-evaluation run):\n")
        L.append("| model | arm | designs evaluated / hour | cost per spec (USD) | *projection*: designs / 24 h | *projection*: specs / 24 h | *projection*: cost / 24 h (USD) |")
        L.append("|---|---|---|---|---|---|---|")
        for m, a in arms.items():
            for arm in ("single",) + FLEET_ARMS:
                rs = a[arm]
                if not rs:
                    continue
                dph = sum(r["n_evals"] for r in rs) / sum(r["wall_s"] for r in rs) * 3600
                cps = statistics.mean(r["cost_usd"] for r in rs)
                sph = 3600 / statistics.mean(r["wall_s"] for r in rs)
                L.append(f"| `{m}` | {arm} | {dph:,.0f} | {cps:.4f} | {dph * 24:,.0f} | {sph * 24:.0f} | {cps * sph * 24:.2f} |")
        L.append("\nThe three *projection* columns multiply the measured rates by 24 hours of back-to-back runs on "
                 "one machine like this one; they assume nothing else changes (provider latency, rate limits, the "
                 "spec mix) and were not run.\n")
        L.append("Fleet behaviour (from the run records):\n")
        for m, a in arms.items():
            for farm in FLEET_ARMS:
                fx = a[farm]
                if not fx:
                    continue
                p2 = [r["phase2_budgets"] for r in fx]
                to_pipe = sum(1 for b in p2 if b.get("fsm", 0) == 0)
                fsm_infeas = sum(1 for r in fx for mm in r["members"] if mm["member"] == "fsm" and mm["llm_declared_infeasible"])
                L.append(f"- `{m}`, {farm}: phase 2 went entirely to the pipelined member in {to_pipe} of {len(fx)} runs; the fsm "
                         f"member's architect declared its families infeasible {fsm_infeas} times; distinct designs in the "
                         f"store per run {_ms([float(r['store_distinct_designs']) for r in fx], digits=0)}.")
        L.append("")

    # ---- L2 -> L1 feedback ---------------------------------------------
    if L2F_FILE.exists():
        fb = json.loads(L2F_FILE.read_text())
        L.append("## L2 -> L1 feedback\n")
        L.append(fb["summary_md"] + "\n")

    # ---- models, spend -----------------------------------------------------
    if MODELS_CHECK_M4.exists():
        mc = json.loads(MODELS_CHECK_M4.read_text())
        L.append(f"## Models and spend\n\nModel check (`eval/data/models_check_m4.json`, {mc['ts']}, "
                 f"{mc['n_models_listed']} models listed): " + "; ".join(
                     f"`{k}` listed {v['listed']}, tools {v['tools']}, structured_outputs {v['structured_outputs']}"
                     for k, v in mc["models"].items()) + ". No substitution.\n")
    rows = ledger("m4")
    if rows:
        by: dict[str, float] = {}
        n: dict[str, int] = {}
        for r in rows:
            k = f"{r['model']} / {r.get('arm')}" + (f" ({r['note']})" if r.get("note") else "")
            by[k] = by.get(k, 0.0) + float(r.get("cost_usd") or 0)
            n[k] = n.get(k, 0) + 1
        L.append("| ledger entry (model / arm) | runs | provider-reported USD |")
        L.append("|---|---|---|")
        for k in sorted(by):
            L.append(f"| {k} | {n[k]} | {by[k]:.4f} |")
        L.append(f"| **total** | {len(rows)} | **{sum(by.values()):.4f}** |\n")
    if KEY_USAGE_M4.exists():
        ku = json.loads(KEY_USAGE_M4.read_text())["snapshots"]
        L.append("Key usage snapshots (authoritative; `eval/data/key_usage_m4.json`): " + "; ".join(
            f"{k} {v['ts']} ${v['usage_usd']:.4f}" for k, v in ku.items()) + ".\n")


__all__ = ["register", "report_m4", "ASIC_SPECS", "LEDGER", "_ms", "_slim", "_slug", "ledger", "statistics", "Path"]
