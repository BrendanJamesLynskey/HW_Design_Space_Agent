"""The campaign agent's tools: every rung of the ladder, with provenance, under a budget.

Each tool is a plain function of a :class:`CampaignContext` (the campaign's
ledger), wrapped as a LangChain tool by :func:`make_tools`. A tool returns
*text* for the model to read; all numbers in it were computed by code and
carry their provenance label. The model chooses which tool to call next and
with which arguments (spec name, family, a box, an evaluation count); it
never supplies a number about a design.

Budget, like the structured arm
-------------------------------
Each spec gets the same L1 evaluation budget as the structured graph and the
baselines (the spec's ``total_evals``, 400). ``run_dse`` (the structured
inner graph) and ``explore_family`` (one NSGA-II study in a box) both draw
from it; a call that would overspend is refused. L5 re-exploration has its
own small budget (60), exactly as in the structured graph, and is kept apart.

Heavy rungs use recorded data
-----------------------------
L4 synthesis is never run live inside a campaign: ``synthesize`` returns the
committed measured rows for the design if there are any, labelled
``measured (<tool> <version>), recorded``, and says plainly when there are
none. ``verify_rtl`` returns the committed L3 row (``exact, recorded``) or,
when a simulator is installed and the design is small (W <= 12), runs the
exhaustive check fresh and says so. Nothing recorded is presented as fresh.

Re-planning is enforced, not hoped for
--------------------------------------
If ``back_annotate`` flags a winner change for a spec, ``finalize`` refuses
until ``reexplore`` (the L5 loop) has run for it, so a measured winner
change always leads to re-exploration with the refitted calibration.
"""

from __future__ import annotations

import csv
import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from hw_dse.agent.summary import merged_front
from hw_dse.benchmark import select_design
from hw_dse.campaign.memory import CampaignMemory
from hw_dse.evaluate import fmt_metric
from hw_dse.families import REGISTRY, clamp_ranges
from hw_dse.rtl.generator import REPO_ROOT
from hw_dse.spec import Budget, Spec, load_spec

DATA = REPO_ROOT / "eval" / "data"
MIN_RUN = 40  # smallest run_dse budget (a 4-round graph needs room)
MAX_TOOL_CALLS = 60  # per campaign; afterwards every tool asks the agent to finalize


def spec_path(name: str) -> Path:
    for p in (REPO_ROOT / "specs" / f"{name}.yaml", REPO_ROOT / "specs" / "system" / f"{name}.yaml"):
        if p.exists():
            return p
    raise KeyError(name)


@dataclass
class SpecLedger:
    spec: Spec
    used: int = 0
    pool: list[dict[str, Any]] = field(default_factory=list)
    dse_runs: list[dict[str, Any]] = field(default_factory=list)
    l2: dict[str, Any] | None = None
    l3: str | None = None
    l4: str | None = None
    back_annotation: dict[str, Any] | None = None
    l5: dict[str, Any] | None = None
    finalized: bool = False
    final_note: str = ""
    calls: list[str] = field(default_factory=list)

    @property
    def remaining(self) -> int:
        return self.spec.budget.total_evals - self.used

    def front(self) -> list[dict[str, Any]]:
        return merged_front(self.pool, self.spec)

    def selected(self) -> dict[str, Any] | None:
        """Current selection: L2's if it ran on the current pool, else the spec's rule on the L1 front."""
        if self.l2 is not None and self.l2.get("pool_size") == len(self.pool):
            return self.l2.get("selected")
        return select_design(self.front(), self.spec)


@dataclass
class CampaignContext:
    run_id: str
    run_dir: Path
    seed: int
    architect: Any  # a StructuredLLM for the inner graph (the campaign's own model)
    memory: CampaignMemory
    specs: dict[str, SpecLedger] = field(default_factory=dict)
    tool_calls: int = 0
    log: list[dict[str, Any]] = field(default_factory=list)

    @staticmethod
    def new(spec_names: list[str], run_dir: Path, seed: int, architect: Any, memory: CampaignMemory,
            run_id: str | None = None) -> CampaignContext:
        run_dir.mkdir(parents=True, exist_ok=True)
        ledgers = {n: SpecLedger(load_spec(spec_path(n))) for n in spec_names}
        return CampaignContext(run_id or run_dir.name, run_dir, seed, architect, memory, ledgers)

    def ledger(self, name: str) -> SpecLedger:
        if name not in self.specs:
            raise ValueError(f"unknown spec {name!r}; the queue is {list(self.specs)}")
        return self.specs[name]

    def record(self, tool: str, args: dict[str, Any], result: str) -> str:
        self.log.append({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "tool": tool, "args": args, "result": result[:4000]})
        return result


# ---------------------------------------------------------------------------
# Formatting helpers (code-computed numbers, with provenance labels)
# ---------------------------------------------------------------------------

def _design_line(r: dict[str, Any], spec: Spec) -> str:
    cols = list(dict.fromkeys([o.metric for o in spec.objectives] + ["luts", "ffs", "throughput_msps", "max_abs_err"]
                              + [c.metric for c in spec.system_constraints]))
    vals = ", ".join(f"{c}={fmt_metric(c, float(r[c]))}" for c in cols if c in r)
    return f"`{r['key']}`: {vals}"


def _front_text(led: SpecLedger, n: int = 6) -> str:
    from hw_dse.l2.node import shortlist

    front = led.front()
    if not front:
        return "no feasible design yet"
    top = shortlist(front, led.spec, n)
    return (f"{len(front)} front designs (feasible, non-dominated); best {len(top)} by the spec's selection rule "
            f"({led.spec.select_direction} {led.spec.select_by}):\n" + "\n".join("  - " + _design_line(r, led.spec) for r in top))


PROV_NOTE = ("Provenance: LUTs/FFs/Fmax/throughput are estimates (cost model, M1 calibration); errors exact "
             "(golden model); sys_* are L1 analytic bounds until simulate_system has run (then simulated).")


# ---------------------------------------------------------------------------
# Tool bodies
# ---------------------------------------------------------------------------

def _guard(ctx: CampaignContext) -> str | None:
    ctx.tool_calls += 1
    if ctx.tool_calls > MAX_TOOL_CALLS:
        return f"tool-call limit ({MAX_TOOL_CALLS}) reached: call finalize for every spec and stop"
    return None


def t_list_specs(ctx: CampaignContext) -> str:
    lines = []
    for n, led in ctx.specs.items():
        state = "finalized" if led.finalized else ("in progress" if led.used else "not started")
        lines.append(f"- {n} [{state}; {led.used}/{led.spec.budget.total_evals} L1 evaluations used]\n"
                     + "\n".join("    " + x for x in led.spec.summary().splitlines()))
    return "Spec queue:\n" + "\n".join(lines)


def t_run_dse(ctx: CampaignContext, spec_name: str, evals: int, notes: str = "") -> str:
    from hw_dse.agent.runner import run_agent

    led = ctx.ledger(spec_name)
    n = min(int(evals), led.remaining)
    if n < MIN_RUN:
        return f"refused: {spec_name} has {led.remaining} L1 evaluations left; run_dse needs at least {MIN_RUN}"
    b = led.spec.budget
    sub = led.spec.model_copy(update={"budget": Budget(total_evals=n, evals_per_round=min(b.evals_per_round, n),
                                                       max_rounds=b.max_rounds, hv_epsilon=b.hv_epsilon)})
    k = len(led.dse_runs)
    opts: dict[str, Any] = {"back_annotate": {"enabled": False}}  # the campaign runs L5 itself, when it decides to
    if notes:
        opts["architect_notes"] = notes
    res = run_agent(sub, llm=ctx.architect, seed=ctx.seed + 7 * k, run_root=ctx.run_dir / "dse", options=opts,
                    tracer=ctx.architect.tracer)
    recs = res["evaluations_ordered"]
    for r in recs:
        r["campaign_call"] = f"run_dse#{k}"
    led.pool += recs
    led.used += len(recs)
    led.dse_runs.append({"k": k, "evals": len(recs), "status": res["status"], "decisions": res["decisions"],
                         "run_dir": res["run_dir"], "rounds_log": res["rounds_log"], "notes": notes,
                         "llm_declared_infeasible": res["llm_declared_infeasible"]})
    led.l2 = None
    led.calls.append("run_dse")
    head = (f"run_dse on {spec_name}: {len(recs)} evaluations (inner graph status {res['status']}, architect decisions "
            f"{' -> '.join(res['decisions']) or '-'}); {led.used} used, {led.remaining} left.")
    if res["llm_declared_infeasible"]:
        head += " The inner architect declared the spec INFEASIBLE."
    return f"{head}\n{_front_text(led)}\n{PROV_NOTE}"


def t_explore_family(ctx: CampaignContext, spec_name: str, family: str, evals: int, data_width_min: int | None = None,
                     data_width_max: int | None = None, n_iter_min: int | None = None, n_iter_max: int | None = None,
                     k_or_m_min: int | None = None, k_or_m_max: int | None = None) -> str:
    from hw_dse.explore import run_family_study

    led = ctx.ledger(spec_name)
    if family not in REGISTRY:
        return f"refused: unknown family {family!r}; choose from {list(REGISTRY)}"
    n = min(int(evals), led.remaining)
    if n < 5:
        return f"refused: {spec_name} has {led.remaining} L1 evaluations left (need at least 5)"
    prop: dict[str, object] = {}
    for prm, lo, hi in (("data_width", data_width_min, data_width_max), ("n_iter", n_iter_min, n_iter_max),
                        ("k" if family == "unrolled_k" else "m", k_or_m_min, k_or_m_max)):
        if lo is not None or hi is not None:
            prop[prm] = [lo if lo is not None else hi, hi if hi is not None else lo]
    if family in ("iterative", "pipelined"):
        prop.pop("m", None)
    cl = clamp_ranges(family, prop)
    k = len([c for c in led.calls if c == "explore_family"])
    recs = run_family_study(family, cl.ranges, led.spec, n, ctx.seed * 131 + 17 * k + 3, tag={"round": f"campaign-{k}"})
    for r in recs:
        r["campaign_call"] = f"explore_family#{k}"
    led.pool += recs
    led.used += len(recs)
    led.l2 = None
    led.calls.append("explore_family")
    feas = sum(1 for r in recs if r["feasible"])
    box = ", ".join(f"{p}={v[0]}..{v[1]}" for p, v in cl.ranges.items() if isinstance(v[0], int))
    note = (" Clamped: " + "; ".join(cl.notes)) if cl.notes else ""
    return (f"explore_family {family} on {spec_name} ({box}): {n} evaluations, {feas} feasible.{note} "
            f"{led.used} used, {led.remaining} left.\n{_front_text(led)}\n{PROV_NOTE}")


def t_simulate_system(ctx: CampaignContext, spec_name: str, top_k: int = 5) -> str:
    from hw_dse.l2.node import l2_select

    led = ctx.ledger(spec_name)
    front = led.front()
    if not front:
        return f"{spec_name}: nothing feasible to simulate yet"
    sel = select_design(front, led.spec)
    out = l2_select(front, sel, led.spec, k=max(1, min(int(top_k), 20)))
    out["pool_size"] = len(led.pool)
    led.l2 = out
    led.calls.append("simulate_system")
    if out["status"] == "facts_only":
        f = out["selected_facts"]
        return (f"{spec_name} has no system scenario; L2 facts for `{sel['key']}`: contract latency "
                f"{f['contract']['latency']} cycles, a new input every {f['contract']['ii']} cycle(s); DDS SFDR "
                f"{f['dds_sfdr_dbc']:.1f} dBc, SNR {f['dds_snr_db']:.1f} dB ({f['dds_provenance']}). Selection unchanged.")
    rows = []
    for r in out["shortlist"]:
        m = ", ".join(f"{c.metric} bound {r['l1_bound'][c.metric]:.4g} -> simulated {r[c.metric]:.4g}"
                      for c in led.spec.system_constraints)
        rows.append(f"  - `{r['key']}`: {m}: {'passes' if r['feasible'] else 'FAILS'}")
    s = out.get("selected")
    return (f"simulate_system {spec_name} (L2, SimPy, at estimated Fmax; top {out.get('k')} of the front):\n"
            + "\n".join(rows) + f"\n{'WINNER CHANGED AT L2' if out['winner_changed'] else 'winner unchanged'}: {out.get('why')}."
            + (f"\nL2 selection: {_design_line(s, led.spec)}" if s else ""))


def _recorded_rows(path: Path, key: str) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with open(path, newline="") as fh:
        return [r for r in csv.DictReader(fh) if r.get("key") == key]


def t_verify_rtl(ctx: CampaignContext, spec_name: str) -> str:
    led = ctx.ledger(spec_name)
    sel = led.selected()
    if sel is None:
        return f"{spec_name}: no selected design to verify"
    rows = [r for r in _recorded_rows(DATA / "l3_verification.csv", sel["key"]) if r.get("level", "rtl") == "rtl"]
    led.calls.append("verify_rtl")
    if rows:
        txt = "; ".join(f"{r['simulator_version']}: {r['n_results']}/{r['n_angles']} angles ({r['sweep']}), "
                        f"{r['mismatches']} mismatches, latency {r['latency_measured']}" for r in rows)
        led.l3 = f"exact, recorded: {txt}"
        return f"verify_rtl `{sel['key']}`: {led.l3} (from eval/data/l3_verification.csv; not re-run)."
    from hw_dse.families import ArchConfig
    from hw_dse.rtl.sim import tool_status

    arch = ArchConfig.from_key(sel["key"])
    ok, why = tool_status("icarus")
    if ok and arch.numerics.data_width <= 12:
        from hw_dse.rtl.sim import verify_rtl

        v = verify_rtl(arch, "icarus")
        led.l3 = (f"exact, fresh run ({v.simulator_version}): {v.n_results}/{v.n_angles} angles ({v.sweep}), "
                  f"{v.mismatches} mismatches, latency {v.latency_measured} (expected {v.latency_expected})")
        return f"verify_rtl `{sel['key']}`: {led.l3}."
    led.l3 = "not verified in this campaign: no recorded L3 row" + (
        f"; a fresh exhaustive run (W={arch.numerics.data_width}) is too heavy for a live campaign" if ok else f"; {why}")
    return f"verify_rtl `{sel['key']}`: {led.l3}. The RTL generator itself is verified on 47 configurations (README)."


def t_synthesize(ctx: CampaignContext, spec_name: str) -> str:
    led = ctx.ledger(spec_name)
    sel = led.selected()
    if sel is None:
        return f"{spec_name}: no selected design"
    from hw_dse.synth.measured import load

    hits = []
    for csvp in ("l4_synthesis.csv", "vivado_measured.csv", "vivado_measured_2.csv"):
        p = DATA / csvp
        if p.exists():
            hits += [(csvp, m) for m in load(p) if m.rtl_source == "generated" and m.arch.key() == sel["key"]]
    led.calls.append("synthesize")
    if not hits:
        led.l4 = "no recorded synthesis for this design (L4 is not run live in campaigns)"
        return f"synthesize `{sel['key']}`: {led.l4}."
    txt = "; ".join(f"{m.provenance}, recorded ({src}): {m.luts:.0f} LUTs, {m.ffs:.0f} FFs, "
                    f"Fmax {m.fmax_mhz if m.fmax_mhz else float('nan'):.1f} MHz" for src, m in hits)
    led.l4 = txt
    return f"synthesize `{sel['key']}`: {txt}. These are recorded measurements, not a fresh run."


def t_back_annotate(ctx: CampaignContext, spec_name: str) -> str:
    from hw_dse.agent.backannotate import back_annotate

    led = ctx.ledger(spec_name)
    sel = led.selected()
    ba = back_annotate(led.spec, led.front(), sel, {})
    led.back_annotation = ba
    led.calls.append("back_annotate")
    if ba.get("status") != "compared":
        return f"back_annotate {spec_name}: {ba.get('status')}; " + "; ".join(ba.get("notes", []))
    cmp = "; ".join(f"{c['provenance']}: LUT {c['luts']['diff_pct_scaled']:+.1f}%, FF {c['ffs']['diff_pct_scaled']:+.1f}%, "
                    f"Fmax {c['fmax_mhz']['diff_pct_scaled']:+.1f}% vs estimate (Vivado scale)" for c in ba["comparisons"])
    flag = "WINNER CHANGED (call reexplore before finalize)" if ba["winner_changed"] else "winner unchanged"
    return f"back_annotate {spec_name} `{ba['selected_key']}`: {cmp}. {flag}: {ba['why']}."


def t_reexplore(ctx: CampaignContext, spec_name: str) -> str:
    from hw_dse.agent.backannotate import reexplore

    led = ctx.ledger(spec_name)
    if not led.back_annotation or not led.back_annotation.get("winner_changed"):
        return f"reexplore {spec_name}: refused, back_annotate has not flagged a winner change for this spec"
    out = reexplore(led.spec, led.front(), led.selected(), led.back_annotation, {}, seed=ctx.seed)
    out.pop("evaluations")
    led.l5 = out
    led.calls.append("reexplore")
    s = out.get("selected")
    return (f"reexplore {spec_name} (L5 loop, {out['n_evals']} evaluations of the separate L5 budget, calibration "
            f"{out['calibration']}): selection {'changed' if out['changed'] else 'unchanged'}"
            + (f": {_design_line(s, led.spec)} (estimate under the refit)" if s else ": nothing meets the spec under the refit"))


def t_finalize(ctx: CampaignContext, spec_name: str, note: str = "") -> str:
    led = ctx.ledger(spec_name)
    ba = led.back_annotation or {}
    if ba.get("winner_changed") and led.l5 is None:
        return (f"refused: back_annotate flagged a winner change for {spec_name}; run reexplore first "
                "(the campaign must re-plan when a measurement changes the winner)")
    if led.spec.system is not None and led.pool and (led.l2 is None or led.l2.get("pool_size") != len(led.pool)):
        t_simulate_system(ctx, spec_name)  # a system spec is never finalized on L1 bounds alone
    led.finalized = True
    led.final_note = note[:1000]
    sel = led.selected()
    return (f"finalized {spec_name}: " + (_design_line(sel, led.spec) if sel else "no design selected")
            + f" ({led.used} L1 evaluations).")


def t_recall(ctx: CampaignContext) -> str:
    return "Lessons from earlier campaigns:\n" + ctx.memory.digest()


def t_remember(ctx: CampaignContext, kind: str, key: str, lesson: str) -> str:
    return ctx.memory.remember("note" if kind not in ("note",) else kind, key[:80], lesson[:500], [ctx.run_id], "llm")


# ---------------------------------------------------------------------------
# LangChain tool wrappers
# ---------------------------------------------------------------------------

def make_tools(ctx: CampaignContext) -> list[Any]:
    """The tools, bound to one campaign's ledger. Errors come back as text."""
    from langchain_core.tools import tool

    def wrap(name: str, fn: Any, args: dict[str, Any]) -> str:
        g = _guard(ctx)
        if g:
            return ctx.record(name, args, g)
        try:
            return ctx.record(name, args, fn(ctx, **args))
        except Exception as exc:  # noqa: BLE001 - the model sees the error and can correct itself
            return ctx.record(name, args, f"error: {type(exc).__name__}: {exc}")

    @tool
    def list_specs() -> str:
        """Show the spec queue: each spec's constraints, objectives, system scenario and budget used."""
        return wrap("list_specs", t_list_specs, {})

    @tool
    def run_dse(spec_name: str, evals: int, notes: str = "") -> str:
        """Run the structured DSE graph (L1 exploration + L2 shortlist) on a spec with `evals` of its L1 budget
        (at least 40). `notes`: optional advice for the inner architect (e.g. lessons from memory)."""
        return wrap("run_dse", t_run_dse, {"spec_name": spec_name, "evals": evals, "notes": notes})

    @tool
    def explore_family(spec_name: str, family: str, evals: int, data_width_min: int | None = None,
                       data_width_max: int | None = None, n_iter_min: int | None = None, n_iter_max: int | None = None,
                       k_or_m_min: int | None = None, k_or_m_max: int | None = None) -> str:
        """Spend `evals` of a spec's L1 budget on one NSGA-II study of one family inside a box (omitted bounds =
        full registry range). Families: iterative, unrolled_k (k), pipelined, pipelined_m (m)."""
        return wrap("explore_family", t_explore_family, {k: v for k, v in dict(
            spec_name=spec_name, family=family, evals=evals, data_width_min=data_width_min, data_width_max=data_width_max,
            n_iter_min=n_iter_min, n_iter_max=n_iter_max, k_or_m_min=k_or_m_min, k_or_m_max=k_or_m_max).items()})

    @tool
    def simulate_system(spec_name: str, top_k: int = 5) -> str:
        """L2: simulate the front's top_k designs in the spec's system (SimPy) and re-select on simulated constraints."""
        return wrap("simulate_system", t_simulate_system, {"spec_name": spec_name, "top_k": top_k})

    @tool
    def verify_rtl(spec_name: str) -> str:
        """L3: RTL verification of the current selection (recorded result, or a fresh run for small designs)."""
        return wrap("verify_rtl", t_verify_rtl, {"spec_name": spec_name})

    @tool
    def synthesize(spec_name: str) -> str:
        """L4: recorded synthesis / place-and-route results for the current selection (never run live)."""
        return wrap("synthesize", t_synthesize, {"spec_name": spec_name})

    @tool
    def back_annotate(spec_name: str) -> str:
        """L5: compare the current selection's estimates with measured data; flags a winner change."""
        return wrap("back_annotate", t_back_annotate, {"spec_name": spec_name})

    @tool
    def reexplore(spec_name: str) -> str:
        """L5 loop: after a flagged winner change, re-explore around the measured designs with the refitted calibration."""
        return wrap("reexplore", t_reexplore, {"spec_name": spec_name})

    @tool
    def finalize(spec_name: str, note: str = "") -> str:
        """Close a spec: record the current selection (by the spec's rule; L2-checked for system specs)."""
        return wrap("finalize", t_finalize, {"spec_name": spec_name, "note": note})

    @tool
    def recall() -> str:
        """Read the lessons kept from earlier campaigns (per family, per spec class, calibration history, notes)."""
        return wrap("recall", t_recall, {})

    @tool
    def remember(key: str, lesson: str) -> str:
        """Keep a short note for future campaigns (stored with this run's ID). Text only."""
        return wrap("remember", t_remember, {"kind": "note", "key": key, "lesson": lesson})

    return [list_specs, run_dse, explore_family, simulate_system, verify_rtl, synthesize, back_annotate, reexplore,
            finalize, recall, remember]


def ledger_json(ctx: CampaignContext) -> str:
    return json.dumps({n: {"used": led.used, "finalized": led.finalized, "calls": led.calls}
                       for n, led in ctx.specs.items()}, indent=1)
