"""The target-agnostic cost-model interface.

A cost model turns a concrete design (:class:`hw_dse.families.ArchConfig`)
into *estimated* implementation costs. Milestone 1 ships one
implementation, an analytical FPGA model calibrated to Artix-7
(:mod:`hw_dse.models.cost_fpga`). Later milestones can add an ASIC
gate-equivalent model, or a model recalibrated against real synthesis
runs, without touching the explorer or the agent: they only see this
protocol.

Provenance
----------
Every number a cost model returns is an **estimate**. The
:class:`CostEstimate` carries a ``provenance`` string naming the model and
its calibration, and that string is copied next to the number into every
CSV row and report table. Compare the golden model, whose accuracy
numbers are ``exact``, and milestone 2's synthesis runs, which will be
``measured``.

Area is a dictionary rather than fixed fields because targets count
different things: an FPGA model reports LUTs and FFs, an ASIC model would
report gate equivalents. ``switching_resources`` is the one
target-neutral area-like number, used for the relative power index.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from hw_dse.families import ArchConfig


@dataclass(frozen=True)
class CostEstimate:
    area: dict[str, float]  # e.g. {"luts": 170.0, "ffs": 95.0}
    fmax_mhz: float
    critical_path_ns: float
    switching_resources: float  # resources that toggle, for the power index
    activity_factor: float
    provenance: str  # "estimate: <model> (<calibration id>)"
    breakdown: dict[str, float] = field(default_factory=dict)


@runtime_checkable
class CostModel(Protocol):
    """What the explorer needs from any cost model."""

    name: str
    target: str
    calibration_id: str

    def estimate(self, arch: ArchConfig) -> CostEstimate:
        """Estimate area, Fmax and switching resources for one design."""
        ...
