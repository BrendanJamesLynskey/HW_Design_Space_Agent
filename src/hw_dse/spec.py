"""The hardware spec: what the human wants, as a validated Pydantic model.

A :class:`Spec` is the contract between the human, the LLM and the
deterministic explorer. It says:

* **constraints**: hard pass/fail limits on metrics
  (``throughput_msps >= 250``, ``max_abs_err <= 2^-13``). A design that
  violates any constraint is *infeasible*, however good it looks otherwise.
* **objectives**: the 1-3 metrics that span the Pareto front, each with a
  direction and a hypervolume *reference point* (the worst value still
  worth counting). Hypervolume is only ever computed over feasible designs.
* **select_by**: how to pick one design off the front automatically
  (the human can override at the ``select`` interrupt).
* **budget**: how many evaluations the agent may spend, per round and in
  total, the round cap and the hypervolume-gain stopping threshold.
* **system** (milestone 3, optional): the system the CORDIC sits in (a DDS
  feeding a mixer, a control loop with a fixed tick, a bursty request
  stream). Constraints on the ``sys_*`` metrics are then *system-level*
  constraints: "p99 latency <= 0.4 us with bursts of 8". They are screened
  at L1 with an analytic bound (:mod:`hw_dse.l2.bounds`) and decided at L2
  by simulation (:mod:`hw_dse.l2.system`) of the shortlisted designs. A
  spec without ``system`` behaves exactly as in milestones 1 and 2.

Specs are written as YAML (see ``specs/``). The ``intake`` node can also
build one from natural language using LLM structured output; either way
the result is validated here and then shown to the human for
confirmation before any exploration happens.

Numbers like ``2^-13`` are accepted in YAML and converted to floats, so
specs read the way engineers write accuracy budgets.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, field_validator, model_validator

MetricName = Literal[
    "luts",
    "ffs",
    "luts_plus_ffs",
    "fmax_mhz",
    "throughput_msps",
    "latency_cycles",
    "latency_ns",
    "power_index",
    "max_abs_err",
    "rms_err",
    "accuracy_bits",
    # Milestone 4: the ASIC target's area metrics (sky130_fd_sc_hd).
    "area_um2",
    "gate_eq",
    # Milestone 3: system-level metrics of the spec's `system` scenario.
    "sys_throughput_msps",
    "sys_p50_latency_us",
    "sys_p99_latency_us",
    "sys_p99_batch_us",
    "sys_stall_frac",
    "sys_utilisation",
    "sys_max_queue",
    "sys_sfdr_dbc",
    "sys_snr_db",
]

SYSTEM_METRICS: tuple[str, ...] = (
    "sys_throughput_msps", "sys_p50_latency_us", "sys_p99_latency_us", "sys_p99_batch_us", "sys_stall_frac",
    "sys_utilisation", "sys_max_queue", "sys_sfdr_dbc", "sys_snr_db",
)
"""Metrics that exist only for a spec with a ``system`` scenario (L2)."""

TARGETS: dict[str, str] = {
    "fpga-artix7": "fpga",
    "asic-sky130hd": "asic",
}
"""Implementation targets (milestone 4 adds the ASIC one) and the cost-model
family each uses (:func:`hw_dse.evaluate.cost_model_for`)."""

TARGET_ONLY_METRICS: dict[str, tuple[str, ...]] = {
    "fpga": ("luts", "luts_plus_ffs"),
    "asic": ("area_um2", "gate_eq"),
}
"""Area metrics that exist on one target only (FFs exist on both)."""

SYSTEM_CONSTRAINABLE: dict[str, str] = {
    "sys_throughput_msps": ">=",
    "sys_p50_latency_us": "<=",
    "sys_p99_latency_us": "<=",
    "sys_p99_batch_us": "<=",
    "sys_stall_frac": "<=",
    "sys_sfdr_dbc": ">=",
    "sys_snr_db": ">=",
}
"""System metrics a spec may constrain, with the only direction allowed: each
has an L1 bound that is optimistic in that direction (``hw_dse.l2.bounds``),
so L1 screening never rejects a design that L2 simulation would accept."""

METRIC_HELP: dict[str, str] = {
    "luts": "estimated LUTs",
    "ffs": "estimated flip-flops",
    "luts_plus_ffs": "estimated LUTs + FFs (area proxy)",
    "fmax_mhz": "estimated max clock (MHz)",
    "throughput_msps": "estimated results per microsecond = Fmax x results/cycle",
    "latency_cycles": "cycles from input to output (exact, from the schedule)",
    "latency_ns": "latency in ns at Fmax (estimate)",
    "power_index": "relative power index, reference iterative @100 MHz = 1.0 (estimate, not watts)",
    "max_abs_err": "max |error| vs ideal sin/cos, absolute (exact)",
    "rms_err": "RMS error, absolute (exact)",
    "accuracy_bits": "-log2(max_abs_err) (exact)",
    "area_um2": "ASIC: estimated standard-cell area in um^2 (sky130_fd_sc_hd)",
    "gate_eq": "ASIC: estimated area in NAND2 gate equivalents (area / 3.7536 um^2)",
    "sys_throughput_msps": "system: results per microsecond the system actually gets (L1 bound, L2 simulated)",
    "sys_p50_latency_us": "system: median request latency, arrival to result, in us (L1 bound, L2 simulated)",
    "sys_p99_latency_us": "system: 99th-percentile request latency in us (L1 bound, L2 simulated)",
    "sys_p99_batch_us": "system: 99th-percentile time from a control tick to its last result, us (L1 bound, L2 simulated)",
    "sys_stall_frac": "system: fraction of time the source is held off by back-pressure (L1 bound, L2 simulated)",
    "sys_utilisation": "system: fraction of the CORDIC's input slots in use (L2 simulated)",
    "sys_max_queue": "system: deepest input queue seen (L2 simulated)",
    "sys_sfdr_dbc": "system: DDS spurious-free dynamic range, dBc (golden-model DDS + FFT)",
    "sys_snr_db": "system: DDS signal-to-noise ratio, dB (golden-model DDS + FFT)",
}

_POW = re.compile(r"^\s*([+-]?\d+(?:\.\d+)?)\s*\^\s*([+-]?\d+(?:\.\d+)?)\s*$")


def parse_number(v: object) -> float:
    """Accept 250, 2.5e2, '2^-13', '2**-13'."""
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace("**", "^")
    m = _POW.match(s)
    if m:
        return float(m.group(1)) ** float(m.group(2))
    return float(s)


class Constraint(BaseModel):
    metric: MetricName
    op: Literal["<=", ">="]
    value: float

    @field_validator("value", mode="before")
    @classmethod
    def _parse_value(cls, v: object) -> float:
        return parse_number(v)

    def satisfied(self, x: float) -> bool:
        return x <= self.value if self.op == "<=" else x >= self.value

    def violation(self, x: float) -> float:
        """<= 0 when satisfied; positive amount (relative) when violated."""
        scale = abs(self.value) or 1.0
        return (x - self.value) / scale if self.op == "<=" else (self.value - x) / scale

    def __str__(self) -> str:
        return f"{self.metric} {self.op} {self.value:g}"


class Objective(BaseModel):
    metric: MetricName
    direction: Literal["min", "max"]
    ref: float = Field(description="hypervolume reference: the worst value still counted")

    @field_validator("ref", mode="before")
    @classmethod
    def _parse_ref(cls, v: object) -> float:
        return parse_number(v)


class Budget(BaseModel):
    total_evals: int = Field(400, ge=10, le=100_000, description="hard limit on evaluations for the whole run")
    evals_per_round: int = Field(
        100, ge=5,
        description="limit on the evaluations of each LLM-planned round. Exempt: the code's final front-mapping "
                    "round (whole-curve levers), which spends whatever budget is left when the run would stop")
    max_rounds: int = Field(
        4, ge=1, le=20,
        description="limit on LLM-planned rounds. Exempt: the code's final front-mapping round, so a run has at "
                    "most max_rounds + 1 rounds; total_evals is never exceeded")
    hv_epsilon: float = Field(0.01, ge=0.0, description="stop when a round improves HV by less than this fraction")


class SystemScenario(BaseModel):
    """The system around the CORDIC, simulated at L2 (milestone 3).

    ``kind`` picks one of three SimPy models (:mod:`hw_dse.l2.system`); the
    other fields parametrise it (each kind uses only its own):

    ``dds_mixer``
        An NCO emits one phase word every 1/``sample_rate_msps`` into a FIFO
        of ``fifo_depth``; the CORDIC turns it into sin/cos for a mixer. A
        full FIFO stalls the NCO (back-pressure). Also reports the DDS
        spectrum (SNR/SFDR) from the golden model's exact outputs.
    ``control_loop``
        Every 1/``loop_rate_mhz`` a control tick issues ``requests_per_tick``
        sin/cos requests at once (e.g. 16 motor axes x Park + inverse Park);
        the loop needs all of them back quickly (``sys_p99_batch_us``).
    ``bursty``
        Bursts of ``burst_size`` requests (``burst_spacing_ns`` apart inside
        a burst) arrive as a Poisson process with an average rate of
        ``mean_rate_msps`` requests per microsecond.

    The CORDIC runs on its own clock at its (estimated) Fmax, as every
    throughput figure in the project assumes; requests cross into it through
    an input FIFO and are accepted at its clock edges by the ready/valid
    contract the RTL and the formal checks pin down.
    """

    kind: Literal["dds_mixer", "control_loop", "bursty"]
    sample_rate_msps: float | None = Field(None, gt=0)
    fifo_depth: int = Field(16, ge=1)
    n_samples: int = Field(4000, ge=100, le=200_000)
    loop_rate_mhz: float | None = Field(None, gt=0)
    requests_per_tick: int | None = Field(None, ge=1)
    n_ticks: int = Field(400, ge=10, le=100_000)
    mean_rate_msps: float | None = Field(None, gt=0)
    burst_size: int | None = Field(None, ge=1)
    burst_spacing_ns: float = Field(0.0, ge=0)
    n_bursts: int = Field(1500, ge=10, le=100_000)
    seed: int = 0

    @model_validator(mode="after")
    def _check(self) -> SystemScenario:
        need = {"dds_mixer": ("sample_rate_msps",), "control_loop": ("loop_rate_mhz", "requests_per_tick"),
                "bursty": ("mean_rate_msps", "burst_size")}[self.kind]
        missing = [f for f in need if getattr(self, f) is None]
        if missing:
            raise ValueError(f"system kind {self.kind!r} needs {missing}")
        return self

    @property
    def offered_rate_msps(self) -> float:
        """Average requests per microsecond the system offers the CORDIC."""
        if self.kind == "dds_mixer":
            return float(self.sample_rate_msps)  # type: ignore[arg-type]
        if self.kind == "control_loop":
            return float(self.loop_rate_mhz) * int(self.requests_per_tick)  # type: ignore[arg-type]
        return float(self.mean_rate_msps)  # type: ignore[arg-type]

    def describe(self) -> str:
        if self.kind == "dds_mixer":
            return (f"DDS feeding a mixer: one phase word every {1000 / self.offered_rate_msps:g} ns "
                    f"({self.offered_rate_msps:g} MS/s), FIFO depth {self.fifo_depth}, NCO stalls when it is full")
        if self.kind == "control_loop":
            return (f"control loop: a tick every {1 / float(self.loop_rate_mhz):g} us issues {self.requests_per_tick} "  # type: ignore[arg-type]
                    f"requests at once ({self.offered_rate_msps:g} requests/us on average)")
        return (f"bursty requests: bursts of {self.burst_size} ({self.burst_spacing_ns:g} ns apart) arriving as a "
                f"Poisson process, {self.offered_rate_msps:g} requests/us on average")


class Spec(BaseModel):
    name: str = Field(pattern=r"^[a-z0-9_\-]+$")
    description: str = ""
    function: Literal["sincos"] = "sincos"
    target: Literal["fpga-artix7", "asic-sky130hd"] = "fpga-artix7"
    constraints: list[Constraint] = Field(default_factory=list)
    objectives: list[Objective] = Field(min_length=1, max_length=3)
    select_by: MetricName
    select_direction: Literal["min", "max"] = "min"
    budget: Budget = Field(default_factory=Budget)
    system: SystemScenario | None = None

    @model_validator(mode="after")
    def _check(self) -> Spec:
        names = [o.metric for o in self.objectives]
        if len(set(names)) != len(names):
            raise ValueError("objectives must be distinct metrics")
        sys_used = [m for m in [*names, self.select_by, *(c.metric for c in self.constraints)] if m in SYSTEM_METRICS]
        if sys_used and self.system is None:
            raise ValueError(f"{sorted(set(sys_used))} need a `system` scenario")
        if any(m in SYSTEM_METRICS for m in [*names, self.select_by]):
            raise ValueError("system metrics may constrain a spec but not be objectives or the selection metric "
                             "(they are only simulated for the shortlist at L2)")
        for c in self.constraints:
            if c.metric in SYSTEM_METRICS and SYSTEM_CONSTRAINABLE.get(c.metric) != c.op:
                raise ValueError(f"system constraint {c} must use {SYSTEM_CONSTRAINABLE.get(c.metric, 'no')} "
                                 "(the direction its L1 bound is optimistic in)")
        kind = TARGETS[self.target]
        used = [*names, self.select_by, *(c.metric for c in self.constraints)]
        for other, metrics in TARGET_ONLY_METRICS.items():
            bad = sorted({m for m in used if m in metrics}) if other != kind else []
            if bad:
                raise ValueError(f"{bad} exist only on the {other} target; this spec targets {self.target}")
        if self.budget.evals_per_round > self.budget.total_evals:
            raise ValueError("evals_per_round exceeds total_evals")
        return self

    @property
    def target_kind(self) -> str:
        """``"fpga"`` or ``"asic"``."""
        return TARGETS[self.target]

    def constraint_for(self, metric: str, op: str) -> Constraint | None:
        for c in self.constraints:
            if c.metric == metric and c.op == op:
                return c
        return None

    @property
    def system_constraints(self) -> list[Constraint]:
        return [c for c in self.constraints if c.metric in SYSTEM_METRICS]

    def without_system(self) -> Spec:
        """The "MSPS-only view": the same spec minus its system constraints
        and scenario, with the throughput floor set to the scenario's average
        offered rate if that is higher. This is how the spec would read if
        it were written in milestone-2 terms."""
        if self.system is None:
            return self
        cons = [c for c in self.constraints if c.metric not in SYSTEM_METRICS and c.metric != "throughput_msps"]
        old = self.min_throughput_msps or 0.0
        cons.insert(0, Constraint(metric="throughput_msps", op=">=", value=max(old, self.system.offered_rate_msps)))
        return self.model_copy(update={"constraints": cons, "system": None, "name": self.name + "__msps_only"})

    @property
    def min_throughput_msps(self) -> float | None:
        c = self.constraint_for("throughput_msps", ">=")
        return c.value if c else None

    def summary(self) -> str:
        lines = [f"spec {self.name}: {self.description.strip()}"]
        if self.target != "fpga-artix7":  # (the FPGA summary is unchanged from M1-M3: replayed prompts depend on it)
            lines.append(f"  target: {self.target}")
        lines += [f"  constraint: {c}" for c in self.constraints]
        lines += [f"  objective: {o.direction} {o.metric} (HV ref {o.ref:g})" for o in self.objectives]
        lines.append(f"  select: {self.select_direction} {self.select_by}")
        if self.system is not None:
            lines.append(f"  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): "
                         f"{self.system.describe()}")
        b = self.budget
        lines.append(f"  budget: {b.total_evals} evals, {b.evals_per_round}/round, <= {b.max_rounds} rounds, eps {b.hv_epsilon}")
        return "\n".join(lines)


def load_spec(path: str | Path) -> Spec:
    with open(path, encoding="utf-8") as fh:
        return Spec.model_validate(yaml.safe_load(fh))


def try_parse_spec_text(text: str) -> Spec | None:
    """If ``text`` is a YAML document that validates as a Spec, return it."""
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    try:
        return Spec.model_validate(data)
    except Exception:  # noqa: BLE001 - any validation failure means "not a YAML spec"
        return None
