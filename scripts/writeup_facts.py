#!/usr/bin/env python3
"""Derived counts for docs/WRITEUP.md, computed from committed data.

    python scripts/writeup_facts.py        # -> docs/writeup_facts.json

The write-up cites numbers that no data file prints literally (how many L3
configurations, how many campaigns came down to one ``run_dse(400)``, ratios
between arms). They are computed here, by code, from the committed CSVs and
JSONs, and written to one file the write-up names as a source;
``tests/test_writeup.py`` regenerates it and requires no difference.
"""

from __future__ import annotations

import csv
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "eval" / "data"
OUT = ROOT / "docs" / "writeup_facts.json"


def _csv(name: str) -> list[dict[str, str]]:
    with open(DATA / name, newline="") as fh:
        return list(csv.DictReader(fh))


def _rows(d: Path) -> list[dict]:
    return [json.loads(p.read_text()) for p in sorted(d.glob("*/*.json"))] if d.exists() else []


def facts() -> dict:
    f: dict = {}
    l3 = _csv("l3_verification.csv")
    rtl = [r for r in l3 if r["level"] == "rtl"]
    gate = [r for r in l3 if r["level"] == "gate"]
    f["l3_rtl_configurations"] = len({r["key"] for r in rtl})
    f["l3_rtl_runs"] = len(rtl)
    f["l3_rtl_mismatches"] = sum(int(r["mismatches"]) for r in rtl)
    f["l3_gate_runs"] = len(gate)
    f["l3_gate_mismatches"] = sum(int(r["mismatches"]) for r in gate)
    fr = _csv("formal_results.csv")
    f["formal_jobs"], f["formal_pass"] = len(fr), sum(r["status"] == "PASS" for r in fr)
    l4 = _csv("l4_synthesis.csv")
    f["l4_points"] = len(l4)
    f["l4_generated_points"] = sum(r["rtl_source"] == "generated" for r in l4)
    viv = _csv("vivado_measured.csv") + _csv("vivado_measured_2.csv")
    f["vivado_designs"] = len({(r["family"], r["data_width"], r["n_iter"], r["k"], r["m"], r["rounding"]) for r in viv})
    camp = [r for r in _rows(DATA / "campaign_m3")]
    single = [r for r in camp if len(r["dse_runs"]) == 1 and r["dse_runs"][0]["evals"] == 400]
    f["m3_campaigns"] = len(camp)
    f["m3_campaigns_single_run_dse_400"] = len(single)
    structured = {(r["model_requested"], r["spec"], r["seed"]): r for r in _rows(DATA / "agent_m2") + _rows(DATA / "agent_m3")}
    ratios = {}
    for model in sorted({r["model_requested"] for r in camp}):
        mine = [r for r in camp if r["model_requested"] == model]
        base = [structured[(model, r["spec"], r["seed"])] for r in mine if (model, r["spec"], r["seed"]) in structured]
        if base:
            ratios[model] = round(statistics.mean(r["cost_usd"] for r in mine) / statistics.mean(r["cost_usd"] for r in base), 2)
    f["m3_campaign_cost_ratio_vs_structured"] = ratios
    asic = _csv("asic_synthesis.csv")
    val = _csv("asic_validation.csv")
    f["asic_calibration_points"], f["asic_validation_points"] = len(asic), len(val)
    f["asic_area_ratio_pipelined_over_iterative_w16"] = round(
        float(next(r for r in asic if r["family"] == "pipelined" and r["data_width"] == "16" and r["n_iter"] == "14"
                   and r["rounding"] == "trunc" and r["frac_guard"] == "0" and r["angle_guard"] == "0")["area_um2"])
        / float(next(r for r in asic if r["family"] == "iterative" and r["data_width"] == "16" and r["n_iter"] == "14"
                     and r["rounding"] == "trunc" and r["frac_guard"] == "0" and r["angle_guard"] == "0")["area_um2"]), 2)
    ledger = [json.loads(x) for x in (DATA / "spend_ledger.jsonl").read_text().splitlines() if x.strip()]
    f["ledger_usd_by_milestone"] = {m: round(sum(float(r.get("cost_usd") or 0) for r in ledger
                                                  if r.get("milestone", "m1") == m), 4) for m in ("m1", "m2", "m3", "m4")}
    f["ledger_entries_m4"] = sum(r.get("milestone") == "m4" for r in ledger)
    ku = json.loads((DATA / "key_usage_m4.json").read_text())["snapshots"] if (DATA / "key_usage_m4.json").exists() else {}
    if ku:
        first, last = list(ku.values())[0], list(ku.values())[-1]
        f["key_usage_m4_delta_usd"] = round(last["usage_usd"] - first["usage_usd"], 4)
    # The fleet A/B: evaluations spent on the FSM families, per arm and model (the
    # single arm read from its archived evaluations, the fleet from its store counts).
    import gzip
    import io

    fsm_spend = {}
    for mdir in sorted((DATA / "fleet_m4" / "fleet").glob("*")):
        fl = [json.loads(p.read_text()) for p in sorted(mdir.glob("*.json"))]
        pairs = {(r["spec"], r["seed"]) for r in fl}
        single = []
        for arm, src in (("structured", DATA / "agent_m4" / mdir.name), ("single", DATA / "fleet_m4" / "single" / mdir.name)):
            for p in sorted(src.glob("*.json")):
                r = json.loads(p.read_text())
                if (r["spec"], r["seed"]) not in pairs:
                    continue
                t = DATA / "traces" / "m4" / arm / r["spec"] / Path(r["run_dir"]).name / "evaluations.csv.gz"
                rows = list(csv.DictReader(io.StringIO(gzip.decompress(t.read_bytes()).decode())))
                single.append(sum(x["family"] in ("iterative", "unrolled_k") for x in rows))
        fsm_spend[mdir.name] = {"single_mean": round(statistics.mean(single)),
                                "fleet_mean": round(statistics.mean(r["store_evaluations_by_member"].get("fsm", 0) for r in fl))}
    f["fleet_ab_fsm_evaluations"] = fsm_spend
    fb = DATA / "l2_feedback_m4.json"
    if fb.exists():
        d = json.loads(fb.read_text())
        fired = [r for r in d["constructed"] if r["fires"]]
        f["l2f_recorded_searches"], f["l2f_recorded_fired"] = len(d["recorded"]), sum(r["fires"] for r in d["recorded"])
        f["l2f_live_m4_runs"], f["l2f_live_m4_fired"] = len(d["live_m4"]), sum(r["fires"] for r in d["live_m4"])
        f["l2f_constructed_searches"], f["l2f_constructed_fired"] = len(d["constructed"]), len(fired)
        f["l2f_recovered_corrected"] = sum(r["corrected"]["status"] == "recovered" for r in fired)
        f["l2f_recovered_uncorrected"] = sum(r["ablation_uncorrected"]["status"] == "recovered" for r in fired)
    return f


def main() -> int:
    OUT.write_text(json.dumps(facts(), indent=1, sort_keys=True) + "\n")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
