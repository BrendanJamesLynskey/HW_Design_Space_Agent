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

    python scripts/vivado_m4.py compare      # -> eval/data/vivado_m4_compare.md / .json
    python scripts/vivado_m4.py refit        # the vivado-2025.2 refit plus the 20 ns rows -> name vivado-2025.2-m4

``compare`` gives the ``high_precision`` verdict at 20 ns against every model
(M1, the ``vivado-2025.2`` refit) and the power index against measured power.
``refit`` reruns ``hw_dse.synth.recalibrate`` with the committed Vivado and
Yosys/nextpnr CSVs plus the 20 ns rows (labelled tool version
``2025.2 (20 ns constraint)`` so they are kept apart from the 10 ns rows of the
same designs); the default calibration is never touched.
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
                  "vivado-2025.2 refit": FpgaCostModel(str(ROOT / "src/hw_dse/models/calibration_artix7_refit_vivado-2025.2.yaml"))}
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
    if len(L) == 2:
        L.append("Neither `eval/data/vivado_measured_20ns.csv` nor `eval/data/vivado_power.csv` exists yet.")
    COMPARE.with_suffix(".md").write_text("\n".join(L) + "\n")
    COMPARE.with_suffix(".json").write_text(json.dumps(rep, indent=1))
    print(f"wrote {COMPARE}.md / .json")
    return rep


def refit() -> None:
    from hw_dse.synth.recalibrate import markdown, refit as do_refit

    csvs = [DATA / "vivado_measured.csv", DATA / "vivado_measured_2.csv", DATA / "l4_synthesis.csv",
            DATA / "vivado_spotcheck.csv"]
    if CSV_20NS.exists():
        csvs.insert(2, CSV_20NS)
    rep = do_refit(csvs, "vivado-2025.2-m4")
    (DATA / "l5_refit_vivado-2025.2-m4.md").write_text(markdown(rep))
    (DATA / "l5_refit_vivado-2025.2-m4.json").write_text(json.dumps(rep, indent=1, default=str))
    print("wrote eval/data/l5_refit_vivado-2025.2-m4.md / .json (the default calibration is unchanged)")


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
