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
]

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
    total_evals: int = Field(400, ge=10, le=100_000)
    evals_per_round: int = Field(100, ge=5)
    max_rounds: int = Field(4, ge=1, le=20)
    hv_epsilon: float = Field(0.01, ge=0.0, description="stop when a round improves HV by less than this fraction")


class Spec(BaseModel):
    name: str = Field(pattern=r"^[a-z0-9_\-]+$")
    description: str = ""
    function: Literal["sincos"] = "sincos"
    target: Literal["fpga-artix7"] = "fpga-artix7"
    constraints: list[Constraint] = Field(default_factory=list)
    objectives: list[Objective] = Field(min_length=1, max_length=3)
    select_by: MetricName
    select_direction: Literal["min", "max"] = "min"
    budget: Budget = Field(default_factory=Budget)

    @model_validator(mode="after")
    def _check(self) -> Spec:
        names = [o.metric for o in self.objectives]
        if len(set(names)) != len(names):
            raise ValueError("objectives must be distinct metrics")
        if self.budget.evals_per_round > self.budget.total_evals:
            raise ValueError("evals_per_round exceeds total_evals")
        return self

    def constraint_for(self, metric: str, op: str) -> Constraint | None:
        for c in self.constraints:
            if c.metric == metric and c.op == op:
                return c
        return None

    @property
    def min_throughput_msps(self) -> float | None:
        c = self.constraint_for("throughput_msps", ">=")
        return c.value if c else None

    def summary(self) -> str:
        lines = [f"spec {self.name}: {self.description.strip()}"]
        lines += [f"  constraint: {c}" for c in self.constraints]
        lines += [f"  objective: {o.direction} {o.metric} (HV ref {o.ref:g})" for o in self.objectives]
        lines.append(f"  select: {self.select_direction} {self.select_by}")
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
