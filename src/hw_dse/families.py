"""The architecture-family registry: the *only* menu the LLM can order from.

In milestone 1 the LLM never invents hardware. It picks families from this
registry and proposes parameter ranges; everything it proposes is
validated and clamped here, in code, before a single evaluation runs. This
is the first line of the project's design principle ("the LLM is never the
optimiser"): the LLM shapes the search, deterministic code bounds it.

The four CORDIC families
------------------------
All four compute exactly the same function with exactly the same integer
arithmetic (so they share one accuracy number per numeric configuration).
They differ in how the N micro-rotations are mapped onto clock cycles::

    iterative     1 micro-rotation per cycle, one shared datapath with
                  variable shifters (barrel-shifter muxes) and an FSM.
                  N+3 cycles per result.               (reference RTL)
    unrolled_k    k micro-rotations per cycle, chained combinationally,
                  same FSM. ceil(N/k)+3 cycles per result. More area and a
                  longer critical path, fewer cycles.
    pipelined     one registered stage per micro-rotation. Shifts are
                  constants (pure wiring). 1 result per cycle, N+2 cycles
                  latency.                             (reference RTL)
    pipelined_m   a register every m stages: ceil(N/m)+2 latency, still
                  1 result per cycle, fewer flip-flops, slower clock.

``iterative`` is ``unrolled_k`` with k=1 and ``pipelined`` is
``pipelined_m`` with m=1. They are listed separately because they are the
two calibration anchors and the two shapes a designer reaches for first.

Parameters
----------
Every family shares the numeric knobs of
:class:`hw_dse.models.cordic_bitexact.CordicNumerics`; the angle path width
is expressed relative to the data width (``angle_guard = A - W``) so a
single range works for every data width. ``unrolled_k`` adds ``k`` and
``pipelined_m`` adds ``m``.

Clamping
--------
:func:`clamp_ranges` turns whatever the LLM proposed into a legal search
box: unknown families are rejected, unknown parameters are dropped,
missing parameters get the registry range, reversed bounds are swapped,
out-of-range bounds are clipped and categorical choices are filtered. Every
adjustment is reported as a human-readable note that ends up in the run
report, so the human can see when the model asked for something illegal.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Literal, Union

from hw_dse.models.cordic_bitexact import CordicNumerics

ParamValue = Union[int, str]
Range = Union[tuple[int, int], tuple[str, ...]]


@dataclass(frozen=True)
class ParamSpec:
    """One searchable parameter: an integer range or a categorical set."""

    name: str
    kind: Literal["int", "cat"]
    description: str
    low: int = 0
    high: int = 0
    choices: tuple[str, ...] = ()

    def full_range(self) -> Range:
        return (self.low, self.high) if self.kind == "int" else self.choices

    def values(self, rng: Range | None = None) -> list[ParamValue]:
        rng = self.full_range() if rng is None else rng
        if self.kind == "int":
            lo, hi = rng  # type: ignore[misc]
            return list(range(int(lo), int(hi) + 1))
        return list(rng)


COMMON_PARAMS: tuple[ParamSpec, ...] = (
    ParamSpec("data_width", "int", "angle input and sin/cos output width W (Q1.(W-2) output)", 8, 28),
    ParamSpec("n_iter", "int", "number of micro-rotations N", 4, 30),
    ParamSpec("angle_guard", "int", "angle path / atan-LUT width minus W (A = W + angle_guard)", -2, 4),
    ParamSpec("frac_guard", "int", "extra fractional bits on x and y", 0, 4),
    ParamSpec("rounding", "cat", "shift and output rounding", choices=("trunc", "round")),
)


@dataclass(frozen=True)
class Family:
    name: str
    summary: str
    extra_params: tuple[ParamSpec, ...] = ()
    reference_rtl: str | None = None

    @property
    def params(self) -> tuple[ParamSpec, ...]:
        return COMMON_PARAMS + self.extra_params

    def param(self, name: str) -> ParamSpec:
        for p in self.params:
            if p.name == name:
                return p
        raise KeyError(name)


REGISTRY: dict[str, Family] = {
    f.name: f
    for f in (
        Family(
            "iterative",
            "1 micro-rotation/cycle, shared datapath with barrel shifters; N+3 cycles/result",
            reference_rtl="cordic_rotation_iterative.sv",
        ),
        Family(
            "unrolled_k",
            "k chained micro-rotations/cycle, shared FSM; ceil(N/k)+3 cycles/result",
            (ParamSpec("k", "int", "micro-rotations per cycle", 2, 8),),
        ),
        Family(
            "pipelined",
            "one registered stage per micro-rotation; 1 result/cycle, N+2 latency",
            reference_rtl="cordic_rotation_pipelined.sv",
        ),
        Family(
            "pipelined_m",
            "register every m stages; 1 result/cycle, ceil(N/m)+2 latency",
            (ParamSpec("m", "int", "micro-rotations between pipeline registers", 2, 8),),
        ),
    )
}


# ---------------------------------------------------------------------------
# A concrete design point
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ArchConfig:
    """One fully specified design: a family plus every parameter value."""

    family: str
    numerics: CordicNumerics
    k: int = 1  # micro-rotations per cycle (iterative/unrolled_k)
    m: int = 1  # micro-rotations per register (pipelined/pipelined_m)

    @staticmethod
    def from_params(family: str, params: dict[str, ParamValue]) -> ArchConfig:
        if family not in REGISTRY:
            raise KeyError(f"unknown family {family!r}")
        w = int(params["data_width"])
        num = CordicNumerics(
            data_width=w,
            n_iter=int(params["n_iter"]),
            angle_width=w + int(params.get("angle_guard", 0)),
            frac_guard=int(params.get("frac_guard", 0)),
            rounding=str(params.get("rounding", "trunc")),  # type: ignore[arg-type]
        )
        return ArchConfig(
            family=family,
            numerics=num,
            k=int(params.get("k", 1)) if family == "unrolled_k" else 1,
            m=int(params.get("m", 1)) if family == "pipelined_m" else 1,
        )

    def params(self) -> dict[str, ParamValue]:
        n = self.numerics
        out: dict[str, ParamValue] = {
            "data_width": n.data_width,
            "n_iter": n.n_iter,
            "angle_guard": n.A - n.data_width,
            "frac_guard": n.frac_guard,
            "rounding": n.rounding,
        }
        if self.family == "unrolled_k":
            out["k"] = self.k
        if self.family == "pipelined_m":
            out["m"] = self.m
        return out

    def key(self) -> str:
        return self.family + ":" + ",".join(f"{k}={v}" for k, v in self.params().items())

    # -- Schedule: how micro-rotations map to cycles -------------------
    @property
    def is_pipelined(self) -> bool:
        return self.family in ("pipelined", "pipelined_m")

    @property
    def rotations_per_step(self) -> int:
        """k for the FSM families, m for the pipelined ones (capped at N)."""
        return min(self.k if not self.is_pipelined else self.m, self.numerics.n_iter)

    @property
    def steps(self) -> int:
        """Iteration cycles (FSM families) or register stages (pipelined)."""
        return math.ceil(self.numerics.n_iter / self.rotations_per_step)

    @property
    def latency_cycles(self) -> int:
        # Reference: iterative = IDLE + PREROTATE + N iterations + OUTPUT;
        # pipelined = pre-rotation stage + N stages + output register.
        return self.steps + (2 if self.is_pipelined else 3)

    @property
    def results_per_cycle(self) -> float:
        return 1.0 if self.is_pipelined else 1.0 / self.latency_cycles


# ---------------------------------------------------------------------------
# Validation and clamping of LLM-proposed ranges
# ---------------------------------------------------------------------------

@dataclass
class ClampResult:
    family: str
    ranges: dict[str, Range]
    notes: list[str] = field(default_factory=list)


def clamp_ranges(family: str, proposed: dict[str, object] | None) -> ClampResult:
    """Validate a proposed search box for ``family`` against the registry.

    ``proposed`` maps parameter name to ``[lo, hi]`` (int params) or a list
    of choices (categorical). Anything malformed falls back to the full
    registry range, with a note.
    """
    if family not in REGISTRY:
        raise KeyError(f"family {family!r} is not in the registry {sorted(REGISTRY)}")
    fam = REGISTRY[family]
    proposed = dict(proposed or {})
    out: dict[str, Range] = {}
    notes: list[str] = []
    for name in list(proposed):
        if name not in {p.name for p in fam.params}:
            notes.append(f"{family}: dropped unknown parameter {name!r}")
            proposed.pop(name)
    for p in fam.params:
        raw = proposed.get(p.name)
        if raw is None:
            out[p.name] = p.full_range()
            continue
        if p.kind == "int":
            try:
                vals = [int(round(float(v))) for v in (raw if isinstance(raw, (list, tuple)) else [raw])]  # type: ignore[union-attr]
            except (TypeError, ValueError):
                notes.append(f"{family}.{p.name}: unparseable range {raw!r}, using full range")
                out[p.name] = p.full_range()
                continue
            if not vals:
                out[p.name] = p.full_range()
                continue
            lo, hi = min(vals), max(vals)
            if (lo, hi) != (vals[0], vals[-1]) and len(vals) == 2:
                notes.append(f"{family}.{p.name}: swapped reversed bounds {vals}")
            clo, chi = max(lo, p.low), min(hi, p.high)
            if clo > chi:  # entirely outside the legal range: snap to nearest edge
                clo = chi = p.low if hi < p.low else p.high
            if (clo, chi) != (lo, hi):
                notes.append(f"{family}.{p.name}: clamped [{lo}, {hi}] to [{clo}, {chi}] (registry {p.low}..{p.high})")
            out[p.name] = (clo, chi)
        else:
            items = raw if isinstance(raw, (list, tuple)) else [raw]  # type: ignore[assignment]
            keep = tuple(str(c) for c in items if str(c) in p.choices)  # type: ignore[union-attr]
            dropped = [c for c in items if str(c) not in p.choices]  # type: ignore[union-attr]
            if dropped:
                notes.append(f"{family}.{p.name}: dropped invalid choices {dropped}")
            out[p.name] = keep or p.choices
    return ClampResult(family, out, notes)


def full_box(family: str) -> dict[str, Range]:
    return {p.name: p.full_range() for p in REGISTRY[family].params}


def registry_table() -> str:
    """Markdown description of the registry, used in prompts and docs."""
    lines = []
    for fam in REGISTRY.values():
        lines.append(f"- `{fam.name}`: {fam.summary}")
        for p in fam.params:
            rng = f"{p.low}..{p.high}" if p.kind == "int" else "|".join(p.choices)
            lines.append(f"    - `{p.name}` ({rng}): {p.description}")
    return "\n".join(lines)
