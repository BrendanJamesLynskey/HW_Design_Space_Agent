"""Structured outputs: the only shapes the LLM is allowed to answer in.

The agent never parses free text. Each LLM call names a Pydantic schema
and the provider is asked for structured output (tool calling or JSON
schema), so the answer arrives as a validated object or the call fails
loudly and is retried / falls back.

Notice what is *not* in these schemas: there is no field for a LUT count,
an Fmax, an error figure or a "predicted" anything. The LLM can name
families, parameter ranges, a budget split, a decision and its reasons.
Every number about a design comes from code. That is the project's design
principle expressed as a type.

Ranges are a list of :class:`ParamRange` rather than a ``dict`` because
several providers' structured-output modes handle free-form object keys
poorly; a list of small fixed-shape records works everywhere.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

FamilyName = Literal["iterative", "unrolled_k", "pipelined", "pipelined_m"]
DecisionName = Literal["refine", "widen", "add_family", "infeasible", "stop"]


class ParamRange(BaseModel):
    """A search range for one parameter of one family."""

    param: str = Field(description="parameter name from the registry, e.g. data_width")
    low: int | None = Field(None, description="inclusive lower bound (integer parameters)")
    high: int | None = Field(None, description="inclusive upper bound (integer parameters)")
    choices: list[str] | None = Field(None, description="allowed values (categorical parameters, e.g. rounding)")


class FamilyPlan(BaseModel):
    family: FamilyName
    ranges: list[ParamRange] = Field(
        default_factory=list,
        description="ranges to search; omit a parameter to search its full registry range",
    )
    budget_share: float = Field(1.0, gt=0, description="relative share of this round's evaluations")
    why: str = Field(description="one or two sentences: why this family and these ranges")


class ExplorationPlan(BaseModel):
    """What to explore next: families, search boxes, and the reasoning."""

    families: list[FamilyPlan] = Field(min_length=1, max_length=4)
    rationale: str = Field(description="the architect's reasoning for this plan, in a few sentences")


class AnalysisDecision(BaseModel):
    """The architect's verdict after reading a round's results."""

    decision: DecisionName = Field(
        description=(
            "refine: narrow ranges around the promising region; "
            "widen: enlarge ranges that look too tight; "
            "add_family: bring in a family not yet explored; "
            "infeasible: the constraints cannot be met by any family in the registry; "
            "stop: the front is good enough or not improving"
        )
    )
    rationale: str = Field(description="why, citing the summary's evidence")
    next_plan: ExplorationPlan | None = Field(
        None, description="required for refine, widen and add_family; omit for stop and infeasible"
    )


class SpecDraft(BaseModel):
    """Intake from natural language: a draft of hw_dse.spec.Spec.

    Kept flat and permissive; it is converted to a real ``Spec`` (with all
    validation) in code and then shown to the human for confirmation.
    """

    name: str = Field(description="short snake_case name for the spec")
    description: str
    min_throughput_msps: float | None = Field(None, description="required throughput in MSPS, if stated")
    max_abs_err: float | None = Field(None, description="max absolute sin/cos error as a number, e.g. 0.000122 for 2^-13")
    max_luts: float | None = None
    max_latency_ns: float | None = None
    minimise: list[Literal["luts", "ffs", "luts_plus_ffs", "power_index", "latency_ns"]] = Field(
        description="what to minimise, most important first (1 or 2 entries)"
    )
