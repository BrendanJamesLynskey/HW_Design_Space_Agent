"""Write a run's artefacts: report.md, pareto.png, evaluations.csv.

Everything in ``runs/<spec>/<timestamp>/``:

``report.md``
    Status and verdict, the confirmed spec, the selected design with
    every metric *and its provenance*, the final Pareto front, and one
    section per round with the plan the LLM proposed (and any clamping
    notes), what the round found, the LLM's decision and rationale, and
    any rule the code applied over it. Provider/model, token usage and
    cost close it off.
``pareto.png``
    All evaluations in the plane of the first two objectives (infeasible
    in grey, feasible coloured by family), the merged front as a line and
    the selected design as a star.
``evaluations.csv``
    One row per evaluation in canonical order, all metrics, the round and
    the provenance labels.
``llm_trace.jsonl``
    Written live by :class:`~hw_dse.agent.trace.Tracer` during the run.

No number in the report is typed by the LLM: the LLM's contributions
(plans, rationales, decisions) are quoted as text, and every figure is
read from evaluation records produced by code.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any

from hw_dse.agent.summary import merged_front
from hw_dse.evaluate import METRIC_COLUMNS, fmt_metric
from hw_dse.families import REGISTRY
from hw_dse.spec import Spec

FAMILY_COLOURS = {"iterative": "#1f77b4", "unrolled_k": "#9467bd", "pipelined": "#d62728", "pipelined_m": "#2ca02c"}
VERDICT = {
    "stopped": "converged: the architect stopped exploring",
    "converged": "converged: hypervolume gain fell below epsilon",
    "round_cap": "stopped at the round cap",
    "budget": "stopped: evaluation budget spent",
    "infeasible": "INFEASIBLE: the architect concluded no design in the registry meets the spec",
    "no_feasible": "NO FEASIBLE DESIGN FOUND within the budget (the architect did not declare infeasibility)",
    "rejected": "spec rejected by the human; nothing explored",
    "l2_no_feasible": "NO SHORTLISTED DESIGN PASSES the simulated system constraints (L2)",
}


def _llm_label(llm: Any) -> str:
    if getattr(llm, "provider", "") == "fake":
        return f"fake ({llm.model}) — not a real language model"
    return f"{llm.provider}: {llm.model}"


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    from hw_dse.agent.graph import order_evaluations

    params = ["data_width", "n_iter", "angle_guard", "frac_guard", "rounding", "k", "m"]
    cols = ["eval_index", "round", "family", *params, *METRIC_COLUMNS, "feasible", "key",
            "provenance_estimate", "provenance_exact"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for i, r in enumerate(order_evaluations(records)):
            prov = r.get("provenance", {})
            row = [i, r.get("round", ""), r["family"], *[r.get(p, "") for p in params],
                   *[r.get(c, "") for c in METRIC_COLUMNS], r.get("feasible", ""), r["key"],
                   prov.get("luts", ""), prov.get("max_abs_err", "")]
            w.writerow(row)


def plot_pareto(path: Path, spec: Spec, records: list[dict[str, Any]], selected: dict[str, Any] | None) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    xo = spec.objectives[0]
    yo = spec.objectives[1] if len(spec.objectives) > 1 else None
    ym = yo.metric if yo else "accuracy_bits"
    fig, ax = plt.subplots(figsize=(7.5, 5))
    infeas = [r for r in records if not r.get("feasible")]
    ax.scatter([r[xo.metric] for r in infeas], [r[ym] for r in infeas], s=8, c="#bbbbbb", label="infeasible", alpha=0.6)
    for fam in REGISTRY:
        pts = [r for r in records if r.get("feasible") and r["family"] == fam]
        if pts:
            ax.scatter([r[xo.metric] for r in pts], [r[ym] for r in pts], s=14, c=FAMILY_COLOURS[fam], label=f"{fam} (feasible)", alpha=0.8)
    front = merged_front(records, spec)
    if front:
        f = sorted(front, key=lambda r: r[xo.metric])
        ax.plot([r[xo.metric] for r in f], [r[ym] for r in f], "k-", lw=1.2, label="Pareto front")
    if selected:
        ax.scatter([selected[xo.metric]], [selected[ym]], marker="*", s=260, c="gold", edgecolors="k", zorder=5, label="selected")
    ax.set_xlabel(f"{xo.metric} ({xo.direction})  [estimate]" if xo.metric not in ("accuracy_bits", "max_abs_err") else xo.metric)
    yprov = "[exact]" if ym in ("accuracy_bits", "max_abs_err", "rms_err") else "[estimate]"
    ax.set_ylabel(f"{ym} ({yo.direction if yo else 'max'})  {yprov}")
    ax.set_title(f"{spec.name}: {len(records)} evaluations")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc="best")
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def _metric_table(rec: dict[str, Any]) -> list[str]:
    prov = rec.get("provenance", {})
    lines = ["| metric | value | provenance |", "|---|---|---|"]
    for m in ("luts", "ffs", "fmax_mhz", "throughput_msps", "latency_cycles", "latency_ns", "power_index",
              "max_abs_err", "max_abs_err_lsb", "rms_err", "rms_err_lsb", "accuracy_bits"):
        lines.append(f"| {m} | {fmt_metric(m, float(rec[m]))} | {prov.get(m, '')} |")
    return lines


def _plan_lines(plan: dict[str, Any]) -> list[str]:
    out = []
    for j in plan.get("jobs", []):
        box = ", ".join(f"{k}={v[0]}..{v[1]}" if len(v) == 2 and isinstance(v[0], int) else f"{k}={'|'.join(map(str, v))}"
                        for k, v in j["box"].items())
        out.append(f"- `{j['family']}` ({j['n_trials']} evals): {box}. *Why:* {j.get('why', '')}")
    for n in plan.get("notes", []):
        out.append(f"- clamped by code: {n}")
    return out


def _back_annotation_lines(ba: dict[str, Any] | None) -> list[str]:
    """L5 section: measured vs estimated for the selected design, and the winner check."""
    if not ba or ba.get("status") == "skipped":
        return []
    L = ["## L5 back-annotation: measured vs estimate", ""]
    if ba["status"] == "no_measured_data":
        L.append("No measured data for the selected design in "
                 + ", ".join(f"`{Path(s).name}`" for s in ba["measured_sources"]) + "; nothing to compare.")
    elif ba["status"] != "compared":
        L.append(f"Back-annotation did not run ({ba['status']}).")
    else:
        L.append("| tool | LUTs est → meas | FFs est → meas | Fmax MHz est → meas |")
        L.append("|---|---|---|---|")
        for c in ba["comparisons"]:
            cells = [f"{c[m]['estimate']:.0f} → {c[m]['measured']:.0f} (raw {c[m]['diff_pct']:+.1f}%"
                     + (f"; on the Vivado scale {c[m]['diff_pct_scaled']:+.1f}%)" if c.get("tool_factors_applied") else ")")
                     for m in ("luts", "ffs", "fmax_mhz")]
            L.append(f"| {c['provenance']} | " + " | ".join(cells) + " |")
        L.append("")
        flag = "**WINNER CHANGES**" if ba["winner_changed"] else "winner unchanged"
        L.append(f"Winner check ({ba['n_front_designs_measured']} of {ba['n_front_designs']} front designs have "
                 f"measurements): {flag}: {ba['why']}.")
    for n in ba.get("notes", []):
        L.append(f"- {n}")
    L.append("")
    return L


def _l2_lines(l2: dict[str, Any] | None, spec: Spec) -> list[str]:
    """L2 section: the shortlist simulated in the system, and the re-selection."""
    if not l2 or l2.get("status") == "skipped":
        return []
    L = ["## L2: cycle-level contract and system simulation", ""]
    f = l2.get("selected_facts") or {}
    if f:
        c = f["contract"]
        L.append(f"Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): "
                 f"latency {c['latency']} cycles, a new input every {c['ii']} cycle(s). DDS tone from its exact outputs: "
                 f"SFDR {f['dds_sfdr_dbc']:.1f} dBc, SNR {f['dds_snr_db']:.1f} dB (*{f['dds_provenance']}*).")
        L.append("")
    if l2.get("status") == "facts_only":
        L.append(f"No system scenario in this spec: {l2.get('reason')}.")
        L.append("")
        return L
    assert spec.system is not None
    L.append(f"System: {spec.system.describe()}. Shortlist: the front's top {l2.get('k')} by the selection rule, "
             "simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:")
    L.append("")
    cons = spec.system_constraints
    L.append("| design | " + " | ".join(f"{c} (bound → simulated)" for c in cons) + " | passes |")
    L.append("|---|" + "---|" * len(cons) + "---|")
    for row in l2.get("shortlist", []):
        cells = [f"{row['l1_bound'][c.metric]:.4g} → {row[c.metric]:.4g}" for c in cons]
        L.append(f"| `{row['key']}` | " + " | ".join(cells) + f" | {'yes' if row['feasible'] else 'no'} |")
    L.append("")
    flag = "**WINNER CHANGED AT L2**" if l2.get("winner_changed") else "winner unchanged"
    L.append(f"{flag}: {l2.get('why')}.")
    for n in l2.get("notes", []):
        L.append(f"- {n}")
    L.append("")
    return L


def _l5_lines(l5: dict[str, Any] | None) -> list[str]:
    if not l5:
        return []
    L = ["## L5 loop: re-exploration after a winner change", ""]
    if l5.get("status") != "reexplored":
        L += [f"Re-exploration did not run ({l5.get('status')}): " + "; ".join(l5.get("notes", [])), ""]
        return L
    boxes = "; ".join(f"`{f}` " + ", ".join(f"{k}={v[0]}..{v[1]}" for k, v in b.items() if isinstance(v[0], int))
                      for f, b in l5["boxes"].items())
    L.append(f"Trigger: {l5['trigger']}. Code re-explored around the measured designs ({', '.join(f'`{a}`' for a in l5['anchors'])}) "
             f"with {l5['n_evals']} evaluations of a separate L5 budget, under the refitted calibration "
             f"`{l5['calibration']}` (boxes: {boxes}).")
    L.append("")
    if l5.get("selected"):
        sel = l5["selected"]
        L.append(f"Selection under the refit: `{sel['key']}` ({'changed' if l5['changed'] else 'unchanged'}; was "
                 f"`{l5['selected_before']}`): {sel['luts']:.0f} LUTs, {sel['ffs']:.0f} FFs, "
                 f"{sel['throughput_msps']:.1f} MSPS (*{sel['provenance']['luts']}*).")
    else:
        L.append("No design meets the spec under the refitted calibration in the re-explored boxes.")
    if l5.get("l2"):
        L.append(f"- L2 re-check: {l5['l2']}")
    L.append("")
    return L


def write_report(state: dict[str, Any], llm: Any) -> Path:
    run_dir = Path(state["run_dir"])
    run_dir.mkdir(parents=True, exist_ok=True)
    spec = Spec.model_validate(state["spec"])
    records = state.get("evaluations", [])
    selected = state.get("selected")
    status = state.get("status", "?")
    front = merged_front(records, spec)
    totals = llm.tracer.totals()

    write_csv(run_dir / "evaluations.csv", records)
    if records:
        plot_pareto(run_dir / "pareto.png", spec, records, selected)

    L = [f"# DSE run: {spec.name}", ""]
    L.append(f"**Verdict:** {VERDICT.get(status, status)}.  ")
    L.append(f"**Architect (LLM):** {_llm_label(llm)}.  ")
    L.append(f"**Evaluations:** {len(records)} of {spec.budget.total_evals} budgeted, over {state.get('round', 0)} round(s).  ")
    L.append(f"**Spec intake:** {state.get('intake_mode', '?')}; confirmed before exploration.")
    L.append("")
    L.append("> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle "
             "schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points "
             "(weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route "
             "results, named by tool and version (back-annotation section). "
             "The LLM produced no numbers in this report; its plans and reasoning are quoted as text.")
    L.append("")
    L.append("## Spec")
    L.append("```")
    L.append(spec.summary())
    L.append("```")
    L.append("")
    L.append("## Selected design")
    if selected:
        L.append(f"`{selected['key']}` — selection: {state.get('selection_mode', '')}")
        L.append("")
        L += _metric_table(selected)
    elif status in ("infeasible", "no_feasible"):
        best_thr = max((float(r["throughput_msps"]) for r in records), default=float("nan"))
        best_bits = max((float(r["accuracy_bits"]) for r in records), default=float("nan"))
        L.append("None: no evaluated design satisfies every constraint.")
        L.append("")
        for c in spec.constraints:
            vals = [float(r[c.metric]) for r in records]
            if vals:
                best = min(vals) if c.op == "<=" else max(vals)
                n_ok = sum(c.satisfied(v) for v in vals)
                L.append(f"- `{c}`: met by {n_ok}/{len(vals)} evaluations; best value seen {fmt_metric(c.metric, best)}")
        L.append(f"- best throughput seen {best_thr:.1f} MSPS (estimate); best accuracy {best_bits:.2f} bits (exact)")
    else:
        L.append("None.")
    L.append("")
    L += _l2_lines(state.get("l2"), spec)
    L += _back_annotation_lines(state.get("back_annotation"))
    L += _l5_lines(state.get("l5"))
    if front:
        L.append(f"## Pareto front ({len(front)} feasible non-dominated designs)")
        L.append("")
        L.append("Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).")
        L.append("")
        L.append("| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(front):
            L.append(f"| {i} | `{r['key']}` | {r['luts']:.0f} | {r['ffs']:.0f} | {r['throughput_msps']:.1f} | "
                     f"{r['latency_cycles']} | {r['power_index']:.3g} | {fmt_metric('max_abs_err', r['max_abs_err'])} | "
                     f"{r['accuracy_bits']:.2f} |")
        L.append("")
    if records:
        L.append("![Pareto plot](pareto.png)")
        L.append("")
    L.append("## Rounds: what the architect proposed, saw and decided")
    for log in state.get("rounds_log", []):
        L.append(f"### Round {log['round']}")
        L.append("")
        L.append(f"**Plan explored** (LLM rationale: *{log['plan'].get('rationale', '')}*)")
        L += _plan_lines(log["plan"])
        gain = log.get("hv_gain")
        gain_s = "n/a" if gain is None else ("+inf" if isinstance(gain, float) and math.isinf(gain) else f"{gain * 100:+.1f}%")
        L.append("")
        L.append(f"**Result (code):** {log['evals_this_round']} evaluations this round, {log['budget_used']} total; "
                 f"{log['n_feasible']} feasible; hypervolume {log['hv']:.4g} ({gain_s}).")
        L.append("")
        if log["llm_decision"] is None:
            L.append(f"**No LLM call** (code's front-mapping round): {log['rationale']}")
        else:
            L.append(f"**LLM decision:** `{log['llm_decision']}` — {log['rationale']}")
        if log.get("overrides"):
            for o in log["overrides"]:
                L.append(f"- **rule applied by code:** {o}")
        if log["llm_decision"] is not None and log["decision"] != log["llm_decision"]:
            L.append(f"- effective decision: `{log['decision']}`")
        L.append("")
        L.append("<details><summary>Summary the LLM was shown</summary>")
        L.append("")
        L.append("```")
        L.append(log.get("summary", ""))
        L.append("```")
        L.append("</details>")
        L.append("")
    L.append("## LLM usage")
    L.append(f"- calls: {totals['calls']:.0f} (failed/unparsed attempts: {totals['failures']:.0f})")
    L.append(f"- tokens: {totals['input_tokens']:.0f} in, {totals['output_tokens']:.0f} out")
    L.append(f"- provider-reported cost: ${totals['cost_usd']:.4f}")
    L.append("- full prompts and replies: `llm_trace.jsonl`")
    L.append("")
    path = run_dir / "report.md"
    path.write_text("\n".join(L) + "\n", encoding="utf-8")
    return path
