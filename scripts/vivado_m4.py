#!/usr/bin/env python3
"""Milestone 4: the two Vivado runs to make locally, and the path that ingests them.

Vivado is not available where this repository's CI and eval run; the
maintainer runs it. Both exports write generated RTL plus one TCL script per
design and a ``run_all.sh``, as ``scripts/vivado_points.py`` does.

(a) ``high_precision`` at its own clock: ``pipelined_m`` W=26 N=22 round, m=8
    and m=6 (the control), synthesised at a **20 ns** constraint (the 50 MSPS
    the spec needs) instead of the anchors' 10 ns. Post-synthesis and
    post-route. This settles the post-synthesis view the README calls
    borderline (m=8 was 49.88 MSPS, 0.24% short, when synthesised at 10 ns)::

        python scripts/vivado_m4.py export-20ns --out ../vivado_m4_20ns
        (cd ../vivado_m4_20ns && ./run_all.sh)
        # copy each design directory's design_key.txt + *.rpt into eval/data/vivado_logs_m4_20ns/<design>/
        python scripts/vivado_m4.py collect-20ns --dir eval/data/vivado_logs_m4_20ns --out eval/data/vivado_measured_20ns.csv

(b) ``report_power`` on the 14 designs Vivado has measured (batches 1 and 2),
    post-synthesis and post-route, at the 10 ns clock and again with the clock
    redefined to 1 ns for the power report only (resolution: see
    ``hw_dse.synth.vivado_power``)::

        python scripts/vivado_m4.py export-power --out ../vivado_m4_power
        (cd ../vivado_m4_power && ./run_all.sh)
        # copy design_key.txt + power_*.rpt per design into eval/data/vivado_logs_m4_power/<design>/
        python scripts/vivado_m4.py collect-power --dir eval/data/vivado_logs_m4_power --out eval/data/vivado_power.csv

Then, once either CSV exists::

    python scripts/vivado_m4.py refit        # the vivado-2025.2 refit plus the 20 ns rows -> name vivado-2025.2-m4
    python scripts/vivado_m4.py compare      # -> eval/data/vivado_m4_compare.md / .json

``compare`` gives the ``high_precision`` verdict at 20 ns against every model
(M1, the ``vivado-2025.2`` refit and, once written, the ``vivado-2025.2-m4``
refit), the post-route / post-synthesis Fmax ratio per family, the power index
against measured power, and a per-family activity factor fitted to that power
(written as a separate, non-default power calibration).
``refit`` reruns ``hw_dse.synth.recalibrate`` with the committed Vivado and
Yosys/nextpnr CSVs plus the 20 ns rows (labelled tool version
``2025.2 (20 ns constraint)`` so they are kept apart from the 10 ns rows of the
same designs), and decides the per-family-class path factor by the rule in
:func:`decide_class_factor` (fixed before the 20 ns data was fitted); the
default calibration is never touched.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

import vivado_points as vp  # noqa: E402

from hw_dse.families import ArchConfig  # noqa: E402
from hw_dse.rtl.generator import generate  # noqa: E402
from hw_dse.synth import measured, vivado_power  # noqa: E402

DATA = ROOT / "eval" / "data"
HP = {"data_width": 26, "n_iter": 22, "angle_guard": 0, "frac_guard": 0, "rounding": "round"}
POINTS_20NS = [ArchConfig.from_params("pipelined_m", {**HP, "m": 8}), ArchConfig.from_params("pipelined_m", {**HP, "m": 6})]
CSV_20NS = DATA / "vivado_measured_20ns.csv"
CSV_POWER = DATA / "vivado_power.csv"
COMPARE = DATA / "vivado_m4_compare"
VERSION_20NS = "2025.2 (20 ns constraint)"
MODELS = ROOT / "src" / "hw_dse" / "models"
CAL_M4 = MODELS / "calibration_artix7_refit_vivado-2025.2-m4.yaml"
POWER_CAL = MODELS / "power_activity_artix7_vivado-2025.2-m4.yaml"
CLASS_DECISION = DATA / "l5_class_path_factor_m4"


def power_points() -> list[ArchConfig]:
    """The 14 designs of Vivado batches 1 and 2 (their committed design keys)."""
    keys = []
    for d in ("vivado_logs", "vivado_logs_2"):
        keys += [p.read_text().strip() for p in sorted((DATA / d).glob("*/design_key.txt"))]
    return [ArchConfig.from_key(k) for k in dict.fromkeys(keys)]


POWER_BLOCK = """report_power -file [file join [file dirname [info script]] power_{stage}_10ns.rpt]
create_clock -period 1.000 -name clk [get_ports clk]
report_power -file [file join [file dirname [info script]] power_{stage}_1ns.rpt]
create_clock -period {period:.3f} -name clk [get_ports clk]
"""


def _tcl(module: str, period: float, power: bool) -> str:
    tcl = vp.TCL.format(part=vp.PART, module=module, route=vp.ROUTE)
    if power:  # report_power after synthesis and after routing, at 10 ns and at 1 ns
        synth_end = "report_timing_summary -file [file join [file dirname [info script]] timing.rpt]\n"
        tcl = tcl.replace(synth_end, synth_end + POWER_BLOCK.format(stage="synth", period=period), 1)
        tcl += POWER_BLOCK.format(stage="routed", period=period)
    return f"# milestone 4: clock period {period:g} ns{'; report_power added' if power else ''}\n" + tcl


def export(out: Path, points: list[ArchConfig], period: float, power: bool) -> None:
    out.mkdir(parents=True, exist_ok=True)
    names = []
    for a in points:
        d = generate(a)
        wd = out / d.module
        d.write(wd)
        (wd / "clock.xdc").write_text(f"create_clock -period {period:.3f} -name clk [get_ports clk]\n")
        (wd / "run.tcl").write_text(_tcl(d.module, period, power))
        (wd / "design_key.txt").write_text(a.key() + "\n")
        (wd / "period_ns.txt").write_text(f"{period:g}\n")
        names.append(d.module)
    (out / "run_all.sh").write_text("#!/usr/bin/env bash\nset -e\ncd \"$(dirname \"$0\")\"\n" + "".join(
        f"vivado -mode batch -nojournal -log {n}/vivado.log -source {n}/run.tcl\n" for n in names))
    (out / "run_all.sh").chmod(0o755)
    print(f"exported {len(names)} designs ({period:g} ns{', report_power' if power else ''}) to {out}; "
          f"run {out}/run_all.sh with Vivado 2025.2")


def collect_20ns(directory: Path, out: Path, version: str = VERSION_20NS) -> list[measured.MeasuredPoint]:
    """Like ``vivado_points.collect``, with Fmax = 1000 / (period - WNS) at the design's own period."""
    pts = []
    for wd in sorted(p for p in directory.iterdir() if (p / "design_key.txt").exists()):
        arch = ArchConfig.from_key((wd / "design_key.txt").read_text().strip())
        period = float((wd / "period_ns.txt").read_text()) if (wd / "period_ns.txt").exists() else 20.0
        for suffix, kind in (("", "post-synthesis (1000/(T-WNS))"), ("_routed", "post-route (1000/(T-WNS))")):
            u, tm = wd / f"utilization{suffix}.rpt", wd / f"timing{suffix}.rpt"
            if not (u.exists() and tm.exists()):
                continue
            util, wns = vp.parse_utilization(u.read_text()), vp.parse_wns(tm.read_text())
            pts.append(measured.MeasuredPoint(
                "vivado", version, vp.PART, "generated", arch, float(util["luts"]), float(util["ffs"]),
                round(1000.0 / (period - wns), 2), float(util.get("carry4", 0)),
                {"fmax_kind": f"{kind}; WNS {wns} ns at {period:g} ns", "target_mhz": f"{1000 / period:g}",
                 "command": f"vivado -mode batch -source {wd.name}/run.tcl",
                 "source_log": f"{wd.name}/utilization{suffix}.rpt, {wd.name}/timing{suffix}.rpt"}))
    if not pts:
        raise SystemExit(f"no reports found under {directory}")
    measured.write(out, pts)
    measured.load(out)
    print(f"wrote {out} ({len(pts)} rows)")
    return pts


def collect_power(directory: Path, out: Path, version: str = "2025.2") -> list[dict[str, object]]:
    rows = []
    for wd in sorted(p for p in directory.iterdir() if (p / "design_key.txt").exists()):
        key = (wd / "design_key.txt").read_text().strip()
        for stage, tag in (("post-synthesis", "synth"), ("post-route", "routed")):
            for clk in ("10ns", "1ns"):
                f = wd / f"power_{tag}_{clk}.rpt"
                if not f.exists():
                    continue
                r = vivado_power.parse_report_power(f.read_text())
                rows.append({"tool": "vivado", "tool_version": version, "part": vp.PART, "rtl_source": "generated",
                             "design_key": key, "stage": stage, "clock_ns": clk[:-2], "toggle_rate_pct": "12.5 (default)",
                             **{k: r.get(k, "") for k in ("total_w", "dynamic_w", "static_w", "core_w", "clocks_w",
                                                          "slice_logic_w", "signals_w", "io_w", "confidence")},
                             "command": f"vivado -mode batch -source {wd.name}/run.tcl", "source_log": f"{wd.name}/{f.name}"})
    if not rows:
        raise SystemExit(f"no power reports under {directory}")
    vivado_power.write(out, rows)
    vivado_power.load(out)
    print(f"wrote {out} ({len(rows)} rows)")
    return rows


def post_route_ratios() -> dict[str, object]:
    """Post-route / post-synthesis Fmax for every Vivado design measured both ways (10 ns and 20 ns runs)."""
    pairs: dict[tuple[str, str], dict[str, float]] = {}
    for c in (DATA / "vivado_measured.csv", DATA / "vivado_measured_2.csv", CSV_20NS):
        if not c.exists():
            continue
        for p in measured.load(c):
            if not p.fmax_mhz or p.rtl_source != "generated":
                continue
            period = 20.0 if p.tool_version == VERSION_20NS else 10.0
            stage = "route" if p.extra.get("fmax_kind", "").lower().startswith("post-route") else "synth"
            pairs.setdefault((p.arch.key(), f"{period:g}"), {"period_ns": period})[stage] = p.fmax_mhz
    designs = [{"key": k, "family": ArchConfig.from_key(k).family, "period_ns": v["period_ns"], "synth_mhz": v["synth"],
                "route_mhz": v["route"], "ratio": round(v["route"] / v["synth"], 4)}
               for (k, _), v in sorted(pairs.items()) if "synth" in v and "route" in v]
    by_family = {}
    for fam in sorted({d["family"] for d in designs}):
        r = [d["ratio"] for d in designs if d["family"] == fam]
        by_family[fam] = {"n": len(r), "min": min(r), "max": max(r), "mean": round(sum(r) / len(r), 4)}
    return {"designs": designs, "by_family": by_family} if designs else {}


def write_power_calibration(act: dict[str, object]) -> None:
    import yaml

    cal = {"id": "artix7-xc7a35t-power-activity-vivado-2025.2-m4", "default": False,
           "fitted_to": f"eval/data/vivado_power.csv, {act['stage']} core power at 100 MHz (1 ns resolution rows), "
                        "Vivado 2025.2 report_power, vectorless (12.5% default toggle, confidence Low)",
           "model": "measured core mW at 100 MHz = mw_per_index_unit[family] x power index at 100 MHz",
           "default_activity": act["default_activity"], "mw_per_index_unit": act["mw_per_index_unit"],
           "implied_activity": act["implied_activity"],
           "rms_log_pct": {k: round(float(v), 2) for k, v in act["rms_log_pct"].items()},  # type: ignore[union-attr]
           "n_designs": act["n"]}
    POWER_CAL.write_text("# Per-family activity factor for the FPGA power index -- NOT the default.\n"
                         "# Written by scripts/vivado_m4.py compare. The default index (calibration_artix7.yaml) keeps\n"
                         "# one activity for every family. Fitted to Vivado's vectorless power estimate, not to real\n"
                         "# switching activity: a calibration to the tool's power model, not to silicon.\n"
                         + yaml.safe_dump(cal, sort_keys=False, width=110))


def compare() -> dict[str, object]:
    """The high_precision verdict at 20 ns and the power-index check, from whichever CSV exists."""
    from hw_dse.evaluate import evaluate
    from hw_dse.models.cost_fpga import FpgaCostModel
    from hw_dse.spec import load_spec

    rep: dict[str, object] = {}
    L = ["# Milestone 4: the local Vivado runs, compared\n",
         "Generated by `python scripts/vivado_m4.py compare`. Measured = Vivado (version in each row), vectorless "
         "for power; estimates name their calibration.\n"]
    if CSV_20NS.exists():
        spec = load_spec(ROOT / "specs" / "high_precision.yaml")
        need = spec.min_throughput_msps
        models = {"M1 (default)": FpgaCostModel(),
                  "vivado-2025.2 refit": FpgaCostModel(str(MODELS / "calibration_artix7_refit_vivado-2025.2.yaml"))}
        if CAL_M4.exists():
            models["vivado-2025.2-m4 refit"] = FpgaCostModel(str(CAL_M4))
        rows = []
        for p in measured.load(CSV_20NS):
            est = {n: evaluate(p.arch, spec, m)["throughput_msps"] for n, m in models.items()}
            rows.append({"key": p.arch.key(), "fmax_kind": p.extra["fmax_kind"], "measured_msps": p.fmax_mhz,
                         "meets_50msps": bool(p.fmax_mhz and p.fmax_mhz >= need), "estimates_msps": est})
        rep["high_precision_20ns"] = rows
        L += [f"## `high_precision` at a 20 ns constraint (needs ≥ {need:g} MSPS)\n",
              "| design | flow | measured MSPS | meets | " + " | ".join(models) + " |", "|---|---|---|---|" + "---|" * len(models)]
        for r in rows:
            L.append(f"| `{r['key']}` | {r['fmax_kind']} | {r['measured_msps']:.2f} | {'yes' if r['meets_50msps'] else 'no'} | "
                     + " | ".join(f"{v:.2f}" for v in r["estimates_msps"].values()) + " |")  # type: ignore[union-attr]
        L.append("")
        L.append("Model columns are unrouted estimates on Vivado's post-synthesis timing scale; compare them with the "
                 "post-synthesis rows.\n")
    pr = post_route_ratios() if CSV_20NS.exists() else {}
    if pr:
        rep["post_route_over_post_synthesis"] = pr
        L += ["## Post-route / post-synthesis Fmax (Vivado 2025.2, every design measured both ways)\n",
              "The cost model's timing scale is post-synthesis (the anchors'); routing is not modelled. Every model "
              "throughput is therefore an unrouted figure, and this is how far routing moved each family.\n",
              "| family | designs | post-route / post-synthesis Fmax (min – max) | mean |", "|---|---|---|---|"]
        for fam, d in pr["by_family"].items():
            L.append(f"| `{fam}` | {d['n']} | {d['min']:.3f} – {d['max']:.3f} | {d['mean']:.3f} |")
        L += ["", "| design | constraint | post-synthesis MHz | post-route MHz | ratio |", "|---|---|---|---|---|"]
        for d in pr["designs"]:
            L.append(f"| `{d['key']}` | {d['period_ns']:g} ns | {d['synth_mhz']:.2f} | {d['route_mhz']:.2f} | {d['ratio']:.3f} |")
        L.append("")
    if CSV_POWER.exists():
        rows_p = vivado_power.load(CSV_POWER)
        for stage in ("post-synthesis", "post-route"):
            try:
                c = vivado_power.compare(rows_p, stage)
            except ValueError as exc:
                L.append(f"- {stage}: {exc}")
                continue
            rep[f"power_{stage}"] = c
            L += [f"## Power index vs Vivado `report_power`, {stage} (core power, 100 MHz)\n",
                  f"{c['n']} designs; Spearman rank correlation {c['spearman']:.3f}; RMS of the index/measured ratio "
                  f"{c['rms_log_ratio_pct']:.1f}% (log scale).\n",
                  "| design | power index | measured core mW | measured relative | index / measured |", "|---|---|---|---|---|"]
            for d in c["designs"]:  # type: ignore[union-attr]
                L.append(f"| `{d['key']}` | {d['power_index_100mhz']:.3f} | {d['measured_core_mw_100mhz']:.2f} | "
                         f"{d['measured_relative']:.3f} | {d['ratio_index_to_measured']:.3f} |")
            L.append("")
        act = vivado_power.fit_activity(rows_p, "post-synthesis")
        rep["power_activity_fit"] = act
        write_power_calibration(act)
        r = act["rms_log_pct"]
        L += ["## Per-family activity factor (a separate power calibration, not the default)\n",
              f"Fitted to the {act['n']} post-synthesis core-power rows above: measured mW at 100 MHz ≈ s_family × "
              f"power index ({act['parameters']} parameters, log least squares). Written to "
              f"`{POWER_CAL.relative_to(ROOT)}`; the default power index is unchanged (activity "
              f"{act['default_activity']} for every family). **Fitted to Vivado's vectorless estimate** (default toggle "
              "rate, confidence Low), not to real switching activity.\n",
              "| family | mW per index unit | implied activity (default 0.125) |", "|---|---|---|"]
        for fam in act["mw_per_index_unit"]:
            L.append(f"| `{fam}` | {act['mw_per_index_unit'][fam]:.3f} | {act['implied_activity'][fam]:.4f} |")
        L += ["", "| power model | parameters | RMS log error in-sample | leave-one-out |", "|---|---|---|---|",
              f"| default index, normalised to the reference design | 0 | {r['default_index_reference_normalised']:.1f}% | — |",
              f"| default index × one fitted scale | 1 | {r['global_scale_in']:.1f}% | {r['global_scale_loo']:.1f}% |",
              f"| per-family activity | {act['parameters']} | {r['per_family_in']:.1f}% | {r['per_family_loo']:.1f}% |",
              "", f"Spearman rank correlation with measured power: default {act['spearman_default']:.3f}, "
              f"per-family {act['spearman_fit']:.3f}.\n",
              "| design | family | index | measured mW | fitted / measured | leave-one-out / measured |",
              "|---|---|---|---|---|---|"]
        for d in act["designs"]:
            L.append(f"| `{d['key']}` | {d['family']} | {d['power_index_100mhz']:.3f} | {d['measured_core_mw_100mhz']:.2f} | "
                     f"{d['ratio_fit_to_measured']:.3f} | {d['ratio_loo_to_measured']:.3f} |")
        L.append("")
    if len(L) == 2:
        L.append("Neither `eval/data/vivado_measured_20ns.csv` nor `eval/data/vivado_power.csv` exists yet.")
    COMPARE.with_suffix(".md").write_text("\n".join(L) + "\n")
    COMPARE.with_suffix(".json").write_text(json.dumps(rep, indent=1))
    print(f"wrote {COMPARE}.md / .json")
    return rep


def high_precision_msps(cal_path: Path) -> dict[str, float]:
    """Model throughput of the two 20 ns designs (m=6, m=8) under a calibration (unrouted, post-synthesis scale)."""
    from hw_dse.evaluate import evaluate
    from hw_dse.models.cost_fpga import FpgaCostModel
    from hw_dse.spec import load_spec

    spec, cm = load_spec(ROOT / "specs" / "high_precision.yaml"), FpgaCostModel(str(cal_path))
    return {f"m={a.m}": round(float(evaluate(a, spec, cm)["throughput_msps"]), 3) for a in POINTS_20NS}


def decide_class_factor(without: dict, with_: dict, msps_with: dict[str, float], need_msps: float = 50.0) -> dict:
    """The rule, fixed before the 20 ns points were fitted: adopt the per-family-class
    path factor into the milestone-4 refit (never the default) only if

    (a) Vivado Fmax leave-one-out RMS improves on the milestone-4 refit without it, **and**
    (b) it puts ``high_precision`` m=8 infeasible and m=6 feasible at 50 MSPS
        (post-synthesis model throughput), as Vivado measures at 20 ns.

    Otherwise reject it. Both sets of numbers are recorded either way."""
    loo_without = without["loo_summary"]["all vivado"]["fmax_loo"]
    loo_with = with_["loo_summary"]["all vivado"]["fmax_loo"]
    a = loo_with < loo_without
    b = msps_with["m=8"] < need_msps <= msps_with["m=6"]
    return {"rule": decide_class_factor.__doc__, "vivado_fmax_loo_without": loo_without, "vivado_fmax_loo_with": loo_with,
            "a_loo_improves": a, "msps_with": msps_with, "b_m8_infeasible_m6_feasible": b, "adopt": a and b}


def refit() -> dict[str, object]:
    import tempfile

    from hw_dse.synth.recalibrate import markdown, refit as do_refit

    csvs = [DATA / "vivado_measured.csv", DATA / "vivado_measured_2.csv", DATA / "l4_synthesis.csv",
            DATA / "vivado_spotcheck.csv"]
    if CSV_20NS.exists():
        csvs.insert(2, CSV_20NS)
    cand, msps = {}, {}
    with tempfile.TemporaryDirectory() as tmp:  # the two candidates; only the decided one is committed
        for cp in (False, True):  # a directory each: calibrations are cached by path
            d = Path(tmp) / ("class" if cp else "single")
            d.mkdir()
            cand[cp] = do_refit(csvs, "vivado-2025.2-m4", class_path=cp, cal_dir=d)
            msps[cp] = high_precision_msps(d / "calibration_artix7_refit_vivado-2025.2-m4.yaml")
    dec = decide_class_factor(cand[False], cand[True], msps[True])
    dec["msps_without"] = msps[False]
    for cp, tag in ((False, "without"), (True, "with")):
        dec[f"loo_summary_{tag}"] = cand[cp]["loo_summary"]
        dec[f"tool_corrections_{tag}"] = cand[cp]["tool_corrections"]
        dec[f"ground_truth_{tag}"] = cand[cp]["ground_truth_impact"]
    rep = do_refit(csvs, "vivado-2025.2-m4", class_path=dec["adopt"])
    (DATA / "l5_refit_vivado-2025.2-m4.md").write_text(markdown(rep))
    (DATA / "l5_refit_vivado-2025.2-m4.json").write_text(json.dumps(rep, indent=1, default=str))
    CLASS_DECISION.with_suffix(".json").write_text(json.dumps(dec, indent=1))
    CLASS_DECISION.with_suffix(".md").write_text(class_decision_markdown(dec))
    print(f"class path factor: {'ADOPTED' if dec['adopt'] else 'REJECTED'} (a={dec['a_loo_improves']}, "
          f"b={dec['b_m8_infeasible_m6_feasible']}); wrote eval/data/l5_refit_vivado-2025.2-m4.md / .json and "
          f"{CLASS_DECISION.name}.md / .json (the default calibration is unchanged)")
    return dec


def class_decision_markdown(dec: dict) -> str:
    def yn(x: bool) -> str:
        return "**yes**" if x else "**no**"

    L = ["# The per-family-class path factor: decision on the milestone-4 data\n",
         "Generated by `python scripts/vivado_m4.py refit`. Both candidates are the `vivado-2025.2-m4` refit "
         "(the `vivado-2025.2` points plus the two 20 ns post-synthesis rows); they differ only in whether "
         "Yosys/nextpnr gets one path factor or one per family class (FSM / pipelined; Vivado = 1 for both). "
         "Neither is the default.\n",
         "## The rule (fixed before the 20 ns points were fitted)\n",
         "Adopt it into the milestone-4 refit only if (a) Vivado Fmax leave-one-out RMS improves on the refit "
         "without it **and** (b) it puts `high_precision` m=8 infeasible and m=6 feasible at 50 MSPS "
         "(post-synthesis model throughput), as Vivado measures at 20 ns. Otherwise reject it.\n",
         "## The numbers\n",
         "| check | without the class factor | with it | holds? |", "|---|---|---|---|",
         f"| (a) Vivado Fmax leave-one-out RMS | {dec['vivado_fmax_loo_without']}% | {dec['vivado_fmax_loo_with']}% | "
         f"{yn(dec['a_loo_improves'])} |",
         f"| (b) m=8 model MSPS (measured 49.88 post-synthesis at 20 ns) | {dec['msps_without']['m=8']:.2f} | "
         f"{dec['msps_with']['m=8']:.2f} | {yn(dec['b_m8_infeasible_m6_feasible'])} |",
         f"| (b) m=6 model MSPS (measured 65.39) | {dec['msps_without']['m=6']:.2f} | {dec['msps_with']['m=6']:.2f} | |",
         "", f"**Outcome: {'adopted' if dec['adopt'] else 'rejected'}.**\n",
         "## Leave-one-out RMS error, in-sample → leave-one-out (%)\n",
         "| group | points | LUT | FF | Fmax without | Fmax with |", "|---|---|---|---|---|---|"]
    for g, s in dec["loo_summary_without"].items():
        w = dec["loo_summary_with"][g]
        L.append(f"| {g} | {s['n']} | {s['luts_in']} → {s['luts_loo']} | {s['ffs_in']} → {s['ffs_loo']} | "
                 f"{s['fmax_in']} → {s['fmax_loo']} | {w['fmax_in']} → {w['fmax_loo']} |")
    L += ["", "## Ground truth under each candidate\n", "| spec | winner (M1) | without | with |", "|---|---|---|---|"]
    for s, g in dec["ground_truth_without"].items():
        h = dec["ground_truth_with"][s]
        L.append(f"| {s} | `{g['winner_m1']}` | `{g['winner_refit']}`{' (changed)' if g['winner_changed'] else ''} | "
                 f"`{h['winner_refit']}`{' (changed)' if h['winner_changed'] else ''} |")
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("export-20ns", "export-power"):
        e = sub.add_parser(name)
        e.add_argument("--out", default="vivado_m4_" + name.split("-")[1])
    for name, default in (("collect-20ns", CSV_20NS), ("collect-power", CSV_POWER)):
        c = sub.add_parser(name)
        c.add_argument("--dir", required=True)
        c.add_argument("--out", default=str(default))
    sub.add_parser("compare")
    sub.add_parser("refit")
    args = ap.parse_args()
    if args.cmd == "export-20ns":
        export(Path(args.out), POINTS_20NS, 20.0, power=False)
    elif args.cmd == "export-power":
        export(Path(args.out), power_points(), 10.0, power=True)
    elif args.cmd == "collect-20ns":
        collect_20ns(Path(args.dir), Path(args.out))
    elif args.cmd == "collect-power":
        collect_power(Path(args.dir), Path(args.out))
    elif args.cmd == "compare":
        compare()
    else:
        refit()


if __name__ == "__main__":
    main()
