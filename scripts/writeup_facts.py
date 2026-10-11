#!/usr/bin/env python3
"""Named facts for docs/WRITEUP.md, read or computed from committed data.

    python scripts/writeup_facts.py          # -> docs/writeup_facts.json
    python scripts/writeup_facts.py --bind   # authoring aid: rewrite each section's declaration
                                             # as the ordered list of the facts its numbers print

Every number the write-up prints is bound to one named fact here: each
section of the write-up lists, in an HTML comment under its heading
(``<!-- facts: ... -->``), one fact name per number, in reading order, and
``tests/test_writeup.py`` requires the i-th number to equal the i-th fact at
the precision it is printed with (so a changed digit always fails).
``--bind`` helps write those lists: given a section whose comment names a
pool of facts (``*`` globs allowed), it replaces the comment with the
ordered list, picking for each number a matching fact from the pool, and
fails on a number no fact in the pool matches.

A fact is either

* **computed** from the committed CSVs and JSONs (counts, ratios, the paired
  tests of the fleet A/B), or
* **read** from one named cell of a committed, code-generated report
  (``eval/results.md``, ``eval/data/*.md``) by :func:`cell`: the first table
  after a named anchor line, the one row whose first cell matches, a column.
  A locator that matches nothing, or more than one row, fails, so a fact
  cannot silently drift to another number.

Values are stored as the write-up prints them: percentages as percent
(``8.66`` for 8.7%), versions as strings. ``tests/test_writeup.py``
regenerates this file and requires no difference.
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import re
import statistics
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "eval" / "data"
RESULTS = ROOT / "eval" / "results.md"
OUT = ROOT / "docs" / "writeup_facts.json"
MODELS = {"sonnet": "anthropic/claude-sonnet-5.5", "deepseek": "deepseek/deepseek-v4.1-flash",
          "qwen": "qwen/qwen3.8-27b, reasoning off"}
NUM = re.compile(r"[-+−]?\d[\d,]*(?:\.\d+)?(?:e[-+]?\d+)?")


# ---------------------------------------------------------------------------
# Locators
# ---------------------------------------------------------------------------

def nums(text: str) -> list[float]:
    """Every number in a table cell ('+12.2% ± 16.5 → **+3.7%**' -> [12.2, 16.5, 3.7])."""
    return [float(t.replace(",", "").replace("−", "-")) for t in NUM.findall(text.replace("*", ""))]


def table(path: Path, anchor: str) -> list[list[str]]:
    """Rows (cells, header and separator dropped) of the first table after the line containing ``anchor``."""
    lines = path.read_text().splitlines()
    hits = [i for i, ln in enumerate(lines) if anchor in ln]
    assert len(hits) == 1, f"anchor {anchor!r} found {len(hits)} times in {path.name}"
    i = hits[0] if lines[hits[0]].startswith("|") else hits[0] + 1  # the anchor may be the header row itself
    while i < len(lines) and not lines[i].startswith("|"):
        i += 1
    rows = []
    while i < len(lines) and lines[i].startswith("|"):
        rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
        i += 1
    return [r for r in rows[2:]]


def cell(path: Path, anchor: str, row: str, col: int) -> str:
    """The cell in column ``col`` of the one row whose first cell is ``row`` (code and
    bold marks ignored); ``row`` may be a tuple: the first cell, then substrings of the row."""
    want = (row,) if isinstance(row, str) else row
    hits = [r for r in table(path, anchor)
            if all(w in " | ".join(r) if i else w.strip("`*") == r[0].strip("`*") for i, w in enumerate(want))]
    assert len(hits) == 1, f"{path.name} / {anchor!r}: row {row!r} matched {len(hits)} rows"
    return hits[0][col]


def num(path: Path, anchor: str, row: Any, col: int, i: int = 0) -> float:
    return nums(cell(path, anchor, row, col))[i]


def _csv(name: str) -> list[dict[str, str]]:
    with open(DATA / name, newline="") as fh:
        return list(csv.DictReader(fh))


def _rows(d: Path) -> list[dict]:
    return [json.loads(p.read_text()) for p in sorted(d.glob("*/*.json"))] if d.exists() else []


def _eval_m4() -> Any:
    sys.path.insert(0, str(ROOT / "eval"))
    import m4  # type: ignore[import-not-found]

    return m4


# ---------------------------------------------------------------------------
# Facts
# ---------------------------------------------------------------------------

def facts() -> dict[str, Any]:  # noqa: PLR0915 - one flat registry, by write-up section
    f: dict[str, Any] = {}
    R = RESULTS
    from hw_dse.agent.graph import LEVERS_M2
    from hw_dse.families import REGISTRY
    from hw_dse.l2.feedback import DEFAULT_EVALS_PER_ROUND, DEFAULT_ROUNDS
    from hw_dse.spec import load_spec

    # ---- the question ------------------------------------------------------
    f["grid_designs"] = json.loads((DATA / "ground_truth.json").read_text())["low_area_control"]["n_designs"]
    f["n_families"] = len(REGISTRY)
    f["budget_evals"] = load_spec(ROOT / "specs" / "low_area_control.yaml").budget.total_evals
    f["max_objectives"] = 3

    # ---- the ladder -------------------------------------------------------
    f["golden_exhaustive_angles"] = 1 << 16  # every 16-bit input angle of the reference configuration
    l3 = _csv("l3_verification.csv")
    rtl = [r for r in l3 if r["level"] == "rtl"]
    gate = [r for r in l3 if r["level"] == "gate"]
    f["l3_rtl_configurations"] = len({r["key"] for r in rtl})
    f["l3_rtl_runs"] = len(rtl)
    f["l3_rtl_mismatches"] = sum(int(r["mismatches"]) for r in rtl)
    f["l3_simulators"] = len({r["simulator"] for r in rtl})
    f["l3_gate_runs"] = len(gate)
    f["l3_gate_mismatches"] = sum(int(r["mismatches"]) for r in gate)
    fr = _csv("formal_results.csv")
    f["formal_jobs"], f["formal_pass"] = len(fr), sum(r["status"] == "PASS" for r in fr)
    l4 = _csv("l4_synthesis.csv")
    f["l4_points"] = len(l4)
    viv = _csv("vivado_measured.csv") + _csv("vivado_measured_2.csv")
    f["vivado_designs"] = len({(r["family"], r["data_width"], r["n_iter"], r["k"], r["m"], r["rounding"]) for r in viv})
    asic = _csv("asic_synthesis.csv")
    val = _csv("asic_validation.csv")
    f["asic_calibration_points"], f["asic_validation_points"] = len(asic), len(val)

    # ---- M1 ---------------------------------------------------------------
    rel = "**Agent HV relative to NSGA-II**"
    for spec in ("dds_250msps", "low_area_control", "high_precision"):
        for j, m in enumerate(MODELS, start=1):
            v = nums(cell(R, rel, spec, j))
            f[f"m1.hv_rel.{spec}.{m}"], f[f"m2.hv_rel.{spec}.{m}"] = v[0], v[1]
    reg = "**Selection regret** (M1 → M2)"
    f["m1.regret.low_area_control.qwen"] = num(R, reg, "low_area_control", 5, 0)
    f["m1.regret.low_area_control.nsga2"] = num(R, reg, "low_area_control", 1, 0)
    inf = "**Infeasible spec**"
    agent_evals = [nums(cell(R, inf, f"`{MODELS[m]}`", 1))[2] for m in MODELS]
    f["m1.infeasible_evals_min"], f["m1.infeasible_evals_max"] = min(agent_evals), max(agent_evals)
    f["m1.calibration_anchors"] = 2
    f["m1.cost_model_constants"] = 5
    f["m1.hv_gain_rule_pct"] = round(load_spec(ROOT / "specs" / "low_area_control.yaml").budget.hv_epsilon * 100)
    f["m1.regret_cells_better"] = sum(
        nums(cell(R, reg, s, j))[0] < nums(cell(R, reg, s, 1))[0]
        for s in ("dds_250msps", "high_precision", "low_area_control") for j in (3, 4, 5))
    f["m1.regret_cells"] = 9

    # ---- M2 ---------------------------------------------------------------
    f["m2.coverage_reserve_pct"] = round(LEVERS_M2["coverage_reserve"] * 100)
    for spec, key in (("dds_250msps", "dds"), ("low_area_control", "low_area")):
        v = nums(cell(R, reg, spec, 4))
        f[f"m2.regret.{key}.deepseek.m1"], f[f"m2.regret.{key}.deepseek.m2"] = v[0], v[2]
    v = nums(cell(R, reg, "high_precision", 5))
    f["m2.regret.high_precision.qwen"], f["m2.regret.high_precision.qwen_std"] = v[2], v[3]
    f["m2.hv_rel_min"] = min(f[k] for k in f if k.startswith("m2.hv_rel."))
    f["m2.hv_rel_max"] = max(f[k] for k in f if k.startswith("m2.hv_rel."))
    f["yosys_fpga_version"] = re.search(r"yosys (\d+\.\d+)", l4[0]["tool_version"]).group(1)  # type: ignore[union-attr]
    f["vivado_version"] = re.search(r"(\d{4}\.\d)", viv[0]["tool_version"]).group(1)  # type: ignore[union-attr]
    L5 = DATA / "l5_refit_vivado-2025.2.md"
    pts = [r for r in table(L5, "## Residuals at every measured point") if r[0] == "vivado" and r[1] == "generated"]

    def errs(fam: str, col: int, ks: tuple[str, ...] = ()) -> list[float]:
        return [nums(r[col].split("(")[1])[0] for r in pts
                if r[2].startswith(f"`{fam}:") and (not ks or any(f"k={k}`" in r[2] for k in ks))]

    pf, itf, ul = errs("pipelined", 10), errs("iterative", 10), errs("unrolled_k", 4, ("3", "4"))
    f["m2.viv_pipelined_fmax_low_min"], f["m2.viv_pipelined_fmax_low_max"] = min(-x for x in pf), max(-x for x in pf)
    f["m2.viv_iterative_fmax_high_min"], f["m2.viv_iterative_fmax_high_max"] = min(itf), max(itf)
    f["m2.viv_unrolled_luts_low_min"], f["m2.viv_unrolled_luts_low_max"] = min(-x for x in ul), max(-x for x in ul)
    f["m2.viv_unrolled_k_lo"], f["m2.viv_unrolled_k_hi"] = 3, 4
    f["m2.refit_points"] = int(re.search(r"fitted on (\d+) points", L5.read_text()).group(1))  # type: ignore[union-attr]

    # ---- M3 ---------------------------------------------------------------
    l2v = _csv("l2_cycle_validation.csv")
    f["m3.l2_traces"] = len(l2v)
    f["m3.l2_traces_identical"] = sum(r["passed"] == "True" for r in l2v)
    f["m3.l2_clock_edges"] = int(nums(re.search(r"([\d,]+) clock edges", R.read_text()).group(1))[0])  # type: ignore[union-attr]
    sysv = "## System specs: exhaustive ground truth, three views"
    mx = nums(cell(R, sysv, "multiaxis_control", 2))
    f["m3.multiaxis.l1_bound_feasible"], f["m3.multiaxis.sim_feasible"] = mx[1], mx[0]
    st = re.search(r"Structured arm: (\d+)/(\d+)", R.read_text())
    f["m3.l2_reselect_structured"], f["m3.structured_runs"] = int(st.group(1)), int(st.group(2))  # type: ignore[union-attr]
    resel = re.search(r"Campaign arm: (\d+)/(\d+)", R.read_text())
    f["m3.l2_reselect_campaign"], f["m3.campaigns"] = int(resel.group(1)), int(resel.group(2))  # type: ignore[union-attr]
    camp = _rows(DATA / "campaign_m3")
    single = [r for r in camp if len(r["dse_runs"]) == 1 and r["dse_runs"][0]["evals"] == 400]
    assert len(camp) == f["m3.campaigns"]
    f["m3.campaigns_single_run_dse_400"] = len(single)
    structured = {(r["model_requested"], r["spec"], r["seed"]): r for r in _rows(DATA / "agent_m2") + _rows(DATA / "agent_m3")}
    for model in sorted({r["model_requested"] for r in camp}):
        mine = [r for r in camp if r["model_requested"] == model]
        base = [structured[(model, r["spec"], r["seed"])] for r in mine if (model, r["spec"], r["seed"]) in structured]
        short = next(k for k, v in MODELS.items() if v.split(",")[0] == model)
        f[f"m3.campaign_cost_ratio.{short}"] = round(statistics.mean(r["cost_usd"] for r in mine)
                                                      / statistics.mean(r["cost_usd"] for r in base), 2)
    fail = nums(cell(R, "**Cost, tokens, time and failures per run**", f"`{MODELS['qwen']}`", 6))
    f["m3.qwen_campaign_failed"], f["m3.qwen_campaigns"] = fail[2], fail[3]
    ms = re.search(r"## Memory on vs off .*seeds (\d)–(\d)\)", R.read_text())
    f["m3.memory_seeds"] = int(ms.group(2)) - int(ms.group(1)) + 1  # type: ignore[union-attr]

    # ---- M4: ASIC target --------------------------------------------------
    f["asic.yosys_version"] = re.search(r"yosys (\d+\.\d+)", asic[0]["tool_version"]).group(1)  # type: ignore[union-attr]
    f["asic.opensta_version"] = re.search(r"OpenSTA (\d+\.\d+\.\d+)", asic[0]["tool_version"]).group(1)  # type: ignore[union-attr]
    corner = re.fullmatch(r"tt_(\d+)C_(\d)v(\d+)", asic[0]["corner"])
    f["asic.corner_temp_c"], f["asic.corner_v"] = int(corner.group(1)), float(f"{corner.group(2)}.{corner.group(3)}")  # type: ignore[union-attr]
    f["asic.clock_ns"] = float(asic[0]["clock_ns"])
    CAL = DATA / "asic_calibration.md"
    rms = "## RMS error (%), in-sample and leave-one-out"
    for col, name in ((2, "area"), (3, "ffs"), (4, "fmax"), (5, "power")):
        f[f"asic.loo_rms.{name}"] = num(CAL, rms, "all", col, 1)
        f[f"asic.in_rms.{name}"] = num(CAL, rms, "all", col, 0)
    for fam in REGISTRY:
        f[f"asic.loo_area.{fam}"] = num(CAL, rms, fam, 2, 1)
        f[f"asic.loo_fmax.{fam}"] = num(CAL, rms, fam, 4, 1)
    f["asic.loo_one_adder_area"] = num(CAL, "## Feature sets compared", "area: one adder constant", 1)
    cal = json.loads((DATA / "asic_calibration.json").read_text())["calibration"]
    f["asic.t_bit_ns"] = round(float(cal["fitted"]["t_bit"]), 2)
    gt = json.loads((DATA / "ground_truth_m4.json").read_text())
    rank = "## ASIC specs: exhaustive ground truth and the family ranking"
    fam_tab = "| spec | family | ASIC best (selection metric)"

    def winner_param(spec: str, col: int, p: str) -> int:
        return int(re.search(p + r"=(\d+)", cell(R, rank, spec, col)).group(1))  # type: ignore[union-attr]

    f["asic.power.rate_msps"] = load_spec(ROOT / "specs" / "asic" / "asic_power_50msps.yaml").constraints[0].value
    f["asic.power.winner_m"] = winner_param("asic_power_50msps", 2, "m")
    f["asic.power.twin_m"] = winner_param("asic_power_50msps", 6, "m")
    f["asic.multiaxis.winner_m"] = winner_param("asic_multiaxis_control", 2, "m")
    f["asic.multiaxis.twin_m"] = winner_param("asic_multiaxis_control", 6, "m")
    f["asic.multiaxis.deadline_us"] = next(c.value for c in load_spec(
        ROOT / "specs" / "asic" / "asic_multiaxis_control.yaml").constraints if c.metric == "sys_p99_batch_us")
    f["asic.low_area.pipelined_ratio"] = num(R, fam_tab, ("asic_low_area", "| pipelined |"), 3)
    f["asic.low_area.pipelined_ratio_fpga"] = num(R, fam_tab, ("asic_low_area", "| pipelined |"), 5)
    f["asic_area_ratio_pipelined_over_iterative_w16"] = round(
        float(next(r for r in asic if r["family"] == "pipelined" and r["data_width"] == "16" and r["n_iter"] == "14"
                   and r["rounding"] == "trunc" and r["frac_guard"] == "0" and r["angle_guard"] == "0")["area_um2"])
        / float(next(r for r in asic if r["family"] == "iterative" and r["data_width"] == "16" and r["n_iter"] == "14"
                     and r["rounding"] == "trunc" and r["frac_guard"] == "0" and r["angle_guard"] == "0")["area_um2"]), 2)
    f["anchor_w"], f["anchor_n"] = 16, 14
    f["asic.multiaxis.l1_bound_feasible"] = gt["asic_multiaxis_control"]["n_feasible_l1_bound"]
    f["asic.multiaxis.sim_feasible"] = gt["asic_multiaxis_control"]["n_feasible"]

    # ---- M4: held-out check -----------------------------------------------
    ho = "## Held-out sky130 check of the ground-truth designs"
    errs_f = [nums(r[2].split("(")[1])[0] for r in table(R, ho)]
    errs_a = [abs(nums(r[1].split("(")[1])[0]) for r in table(R, ho)]
    f["asic.ho.n"], f["asic.ho.area_err_bound_pct"] = len(errs_f), 5
    assert max(errs_a) <= 5
    f["asic.ho.fmax_err_min"], f["asic.ho.fmax_err_max"] = min(errs_f), max(errs_f)
    f["asic.ho.twin_power_fmax"] = num(R, ho, "`pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=7`", 2, 0)
    f["asic.ho.multiaxis_winner_fmax"] = num(R, ho, "`pipelined_m:data_width=17,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,m=2`", 2, 0)
    f["asic.ho.multiaxis_winner_fmax_est"] = num(R, ho, "`pipelined_m:data_width=17,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,m=2`", 2, 1)
    f["asic.ho.pipelined_fmax"] = num(R, ho, "`pipelined:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round`", 2, 0)
    f["asic.ho.pipelined_w"], f["asic.ho.pipelined_n"] = 17, 14
    f["asic.ho.multiaxis_winner_p99_us"] = num(R, ho, "`pipelined_m:data_width=17,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,m=2`", 5)

    # ---- M4: ASIC eval ----------------------------------------------------
    hv, rg = "**HV fraction**\n", "**Selection regret**\n"
    m4tab = "## ASIC specs: structured graph vs baselines"
    text = R.read_text().split(m4tab, 1)[1]
    tmp = ROOT / "build" / "_m4_section.md"
    tmp.parent.mkdir(exist_ok=True)
    tmp.write_text(text)
    for spec in ("asic_low_area", "asic_power_50msps", "asic_multiaxis_control"):
        for j, m in enumerate(("nsga2", "random", *MODELS), start=1):
            f[f"asic.hv.{spec}.{m}"] = num(tmp, hv.strip(), spec, j)
            f[f"asic.regret.{spec}.{m}"] = num(tmp, rg.strip(), spec, j)
        f[f"asic.regret_std.{spec}.nsga2"] = num(tmp, rg.strip(), spec, 1, 1)
    meets = [nums(cell(tmp, "| model | runs | selected meets spec", f"`{MODELS[m]}`", 2)) for m in MODELS]
    f["asic.runs_per_model"] = int(meets[0][1])
    f["asic.meets_per_model_min"] = int(min(x[0] for x in meets))
    assert all(x[0] == x[1] for x in meets)
    f["asic.l2_changed.sonnet"] = int(num(tmp, "| model | runs | selected meets spec", f"`{MODELS['sonnet']}`", 3))
    f["asic.multiaxis.regret_min"] = min(f[f"asic.regret.asic_multiaxis_control.{m}"] for m in ("nsga2", *MODELS))
    f["asic.multiaxis.regret_max"] = max(f[f"asic.regret.asic_multiaxis_control.{m}"] for m in ("nsga2", *MODELS))
    tmp.unlink()

    # ---- M4: fleet A/B ----------------------------------------------------
    m4 = _eval_m4()
    arms = m4.ab_arms()
    short = {v: k for k, v in MODELS.items()}
    for mname, a in arms.items():
        m = short[mname]
        for arm in ("single", *m4.FLEET_ARMS):
            rs = a.get(arm) or []
            if not rs:
                continue
            k = f"ab.{m}.{arm}"
            f[f"{k}.runs"] = len(rs)
            f[f"{k}.hv"] = statistics.mean(r["hv_frac"] for r in rs)
            f[f"{k}.hv_std"] = statistics.pstdev(r["hv_frac"] for r in rs)
            f[f"{k}.regret"] = statistics.mean(r["select_regret"] for r in rs) * 100
            f[f"{k}.regret_std"] = statistics.pstdev(r["select_regret"] for r in rs) * 100
            f[f"{k}.cost"] = statistics.mean(r["cost_usd"] for r in rs)
            f[f"{k}.wall"] = statistics.mean(r["wall_s"] for r in rs)
            f[f"{k}.wall_std"] = statistics.pstdev(r["wall_s"] for r in rs)
            f[f"{k}.failed_calls"] = sum(int(r["llm_failures"]) for r in rs)
            f[f"{k}.failures"] = sum(1 for r in rs if not r["selected_meets_spec"] and not r.get("declared_infeasible"))
            f[f"{k}.designs_per_hour"] = sum(r["n_evals"] for r in rs) / sum(r["wall_s"] for r in rs) * 3600
            if arm != "single":
                f[f"{k}.cost_ratio"] = f[f"{k}.cost"] / f[f"ab.{m}.single.cost"]
                p2 = [r["phase2_budgets"] for r in rs]
                f[f"{k}.phase2_all_pipelined"] = sum(1 for b in p2 if b.get("fsm", 0) == 0)
                f[f"{k}.fsm_declared_infeasible"] = sum(1 for r in rs for mm in r["members"]
                                                        if mm["member"] == "fsm" and mm["llm_declared_infeasible"])
                f[f"{k}.evals_mean"] = statistics.mean(r["n_evals"] for r in rs)
                f[f"{k}.evals_min"] = min(r["n_evals"] for r in rs)
                f[f"{k}.min_member_budget"] = 10 if arm == "fleet" else 20  # MIN_MEMBER_BUDGET before / after the fix
    for row in m4.paired_tests(arms):
        m = short.get(row["model"], row["model"])
        for met, nm in (("hv_frac", "hv"), ("select_regret", "regret")):
            s, t = row[met]["sign"], row[met]["t"]
            k = f"ab.paired.{m}.{row['arm']}.{nm}"
            f[f"{k}.pairs"] = t["n"]
            f[f"{k}.fleet_higher"], f[f"{k}.fleet_lower"] = s["positive"], s["negative"]
            f[f"{k}.sign_p"] = s["p"]
            f[f"{k}.untied"] = s["n"]
            f[f"{k}.t"], f[f"{k}.t_p"] = t["t"], t["p"]
            f[f"{k}.mean_diff"] = None if t["mean"] is None else t["mean"] * (100 if nm == "regret" else 1)
    # evaluations spent on the FSM families, per arm (single from its archived evaluations)
    fsm_spend = {}
    for mname, a in arms.items():
        m = short[mname]
        for arm in m4.FLEET_ARMS:
            fl = a.get(arm) or []
            if not fl:
                continue
            pairs = {(r["spec"], r["seed"]) for r in fl}
            single_spend = []
            for src_arm, src in (("structured", DATA / "agent_m4"), ("single", DATA / "fleet_m4" / "single")):
                for r in _rows(src):
                    if r["model_requested"] + ("" if r["reasoning"] == "provider default" else f", reasoning {r['reasoning']}") != mname:
                        continue
                    if (r["spec"], r["seed"]) not in pairs:
                        continue
                    t = DATA / "traces" / "m4" / src_arm / r["spec"] / Path(r["run_dir"]).name / "evaluations.csv.gz"
                    rows = list(csv.DictReader(io.StringIO(gzip.decompress(t.read_bytes()).decode())))
                    single_spend.append(sum(x["family"] in ("iterative", "unrolled_k") for x in rows))
            fsm_spend[f"{m}.{arm}"] = (statistics.mean(single_spend),
                                       statistics.mean(r["store_evaluations_by_member"].get("fsm", 0) for r in fl))
            f[f"ab.{m}.single_fsm_evals_vs_{arm}"] = fsm_spend[f"{m}.{arm}"][0]
            f[f"ab.{m}.{arm}.fsm_evals"] = fsm_spend[f"{m}.{arm}"][1]
    f["ab.qd.fleet.fsm_evals"] = statistics.mean([f["ab.qwen.fleet.fsm_evals"], f["ab.deepseek.fleet.fsm_evals"]])
    f["ab.qwen.fleet.failed_calls_qd"] = f["ab.qwen.fleet.failed_calls"] + f["ab.deepseek.fleet.failed_calls"]
    f["ab.qwen.single.failed_calls_qd"] = f["ab.qwen.single.failed_calls"] + f["ab.deepseek.single.failed_calls"]
    f["ab.n_specs"], f["ab.n_asic_specs"], f["ab.n_fpga_specs"] = 5, 3, 2
    seeds = sorted({r["seed"] for a in arms.values() for rs in a.values() for r in rs})
    f["ab.seed_first"], f["ab.seed_last"] = seeds[0], seeds[-1]
    f["ab.members"] = 2
    for arm in ("single", *m4.FLEET_ARMS):
        rs = [r for r in arms[MODELS["qwen"]].get(arm) or [] if r["spec"] == "multiaxis_control"]
        f[f"ab.qwen.multiaxis.hv_{arm}"] = statistics.mean(r["hv_frac"] for r in rs)
    q = [r for r in (arms[MODELS["qwen"]]["single"]) if r["spec"] == "low_area_control"]
    f["drift.qwen.low_area.m2_regret"] = num(R, reg, "low_area_control", 5, 2)
    f["drift.qwen.low_area.m4_regret"] = statistics.mean(r["select_regret"] for r in q) * 100
    # projection (labelled as such in the text)
    qs = arms[MODELS["qwen"]]["single"]
    f["proj.qwen.designs_per_day"] = f["ab.qwen.single.designs_per_hour"] * 24
    f["proj.qwen.specs_per_day"] = 3600 / statistics.mean(r["wall_s"] for r in qs) * 24
    f["proj.qwen.cost_per_day"] = f["ab.qwen.single.cost"] * f["proj.qwen.specs_per_day"]

    # ---- spend ------------------------------------------------------------
    ledger = [json.loads(x) for x in (DATA / "spend_ledger.jsonl").read_text().splitlines() if x.strip()]
    for ms in ("m1", "m2", "m3", "m4"):
        f[f"ledger_usd.{ms}"] = round(sum(float(r.get("cost_usd") or 0) for r in ledger if r.get("milestone", "m1") == ms), 4)
    ku = json.loads((DATA / "key_usage_m4.json").read_text())["snapshots"]
    first, last = list(ku.values())[0], list(ku.values())[-1]
    f["key_usage_m4_delta_usd"] = round(last["usage_usd"] - first["usage_usd"], 4)
    f["m4_cap_usd"] = 5

    # ---- L2 -> L1 feedback ------------------------------------------------
    d = json.loads((DATA / "l2_feedback_m4.json").read_text())
    fired = [r for r in d["constructed"] if r["fires"]]
    f["l2f.rounds"], f["l2f.evals_per_round"] = DEFAULT_ROUNDS, DEFAULT_EVALS_PER_ROUND
    f["l2f.recorded_searches"], f["l2f.recorded_fired"] = len(d["recorded"]), sum(r["fires"] for r in d["recorded"])
    f["l2f.live_m4_runs"], f["l2f.live_m4_fired"] = len(d["live_m4"]), sum(r["fires"] for r in d["live_m4"])
    f["l2f.constructed_searches"], f["l2f.constructed_fired"] = len(d["constructed"]), len(fired)
    f["l2f.recovered_corrected"] = sum(r["corrected"]["status"] == "recovered" for r in fired)
    f["l2f.recovered_uncorrected"] = sum(r["ablation_uncorrected"]["status"] == "recovered" for r in fired)
    reg_c = [r["corrected"]["regret"] * 100 for r in fired if r["corrected"]["regret"] is not None]
    f["l2f.regret_mean"], f["l2f.regret_std"] = statistics.mean(reg_c), statistics.pstdev(reg_c)
    f["l2f.l1_bound_feasible"] = d["constructed_gt"]["n_feasible_l1_bound"]
    f["l2f.sim_feasible"] = d["constructed_gt"]["n_feasible_simulated"]
    fs = load_spec(ROOT / "specs" / "m4" / "l2_feedback_bursty.yaml")
    f["l2f.burst"] = fs.system.burst_size  # type: ignore[union-attr]
    f["l2f.rate_msps"] = fs.system.mean_rate_msps  # type: ignore[union-attr]
    f["l2f.p99_us"] = next(c.value for c in fs.constraints if c.metric == "sys_p99_latency_us")
    f["l2f.throughput_floor"] = next(c.value for c in fs.constraints if c.metric == "throughput_msps")
    f["l2f.searches_per_method"] = 5
    # The first version of the constructed spec (throughput floor 1 MS/s, review S6), kept for the record
    v1 = json.loads((DATA / "l2_feedback_m4_v1_floor1.json").read_text())
    f["l2f_v1.throughput_floor"] = 1
    f["l2f_v1.constructed_fired"] = sum(r["fires"] for r in v1["constructed"])
    f["l2f_v1.constructed_searches"] = len(v1["constructed"])

    # ---- limitations / next ------------------------------------------------
    f["fpga.fmax_err_vs_vivado_max"] = f["m2.viv_pipelined_fmax_low_max"]
    sys.path.insert(0, str(ROOT / "scripts"))
    import vivado_m4  # type: ignore[import-not-found]

    f["hp.vivado_constraint_ns"] = float(re.search(r"POINTS_20NS, ([\d.]+), power=False", (ROOT / "scripts" / "vivado_m4.py").read_text()).group(1))  # type: ignore[union-attr]
    f["hp.m"] = max(int(a.params()["m"]) for a in vivado_m4.POINTS_20NS)
    f["infeasible.rate_msps"] = next(c.value for c in load_spec(ROOT / "specs" / "infeasible_dds_400msps.yaml").constraints
                                     if c.metric == "throughput_msps")
    # 10 significant digits: float sums differ in the last bit between Python versions
    # (3.12 made sum() compensated), and no printed number needs more.
    return {k: (float(f"{v:.10g}") if isinstance(v, float) else v) for k, v in f.items()}


def bind() -> int:
    """Rewrite each section's fact pool as the ordered per-number binding (authoring aid)."""
    sys.path.insert(0, str(ROOT / "tests"))
    import test_writeup as tw  # type: ignore[import-not-found]

    fx = tw.load_facts()
    parts = re.split(r"^(#{1,4} .*)$", tw.WRITEUP.read_text(), flags=re.M)
    bad = []
    head = "(preamble)"
    for i, chunk in enumerate(parts):
        if re.match(r"^#{1,4} ", chunk):
            head = chunk.strip()
            continue
        m = re.search(r"<!--\s*facts:\s*(.*?)-->", chunk, re.S)
        if not m:
            continue
        pool = tw.expand(m.group(1).split(), fx)
        order: list[str] = []
        for tok in tw.tokens(re.sub(r"<!--.*?-->", " ", chunk, flags=re.S)):
            hit = [k for k in pool if tw.matches(tok, pool[k])]
            if not hit:
                bad.append(f"{head}: {tok}")
                continue
            fresh = [k for k in hit if k not in order]
            order.append((fresh or hit)[0])
        lines, cur = [], "<!-- facts:"
        for k in order:
            if len(cur) + len(k) + 1 > 95:
                lines.append(cur)
                cur = "    "
            cur += " " + k
        lines.append(cur + " -->")
        parts[i] = chunk.replace(m.group(0), "\n".join(lines), 1)
    if bad:
        print("no fact in the pool matches:\n" + "\n".join(bad))
        return 1
    tw.WRITEUP.write_text("".join(parts))
    print(f"bound every number of {tw.WRITEUP.name}")
    return 0


def main() -> int:
    if "--bind" in sys.argv:
        return bind()
    OUT.write_text(json.dumps(facts(), indent=1, sort_keys=True) + "\n")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
