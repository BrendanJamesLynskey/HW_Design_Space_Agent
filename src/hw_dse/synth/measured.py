"""Measured design points: one CSV schema for every tool (provenance: measured).

The L5 back-annotation step (:mod:`hw_dse.synth.recalibrate`) consumes
*measured* implementation results from any tool: the open-source flow in
this repository (Yosys + nextpnr-xilinx, written by
``scripts/run_l4_sweep.py``) and Vivado runs made elsewhere. They share one
schema so that feeding Vivado numbers in is a matter of writing a CSV.

Columns
-------
==============  ========  ===================================================
column          required  meaning
==============  ========  ===================================================
tool            yes       ``yosys+nextpnr-xilinx`` or ``vivado`` (free text;
                          the refit groups by it and fits one correction per
                          tool)
tool_version    yes       e.g. ``2025.2`` or ``yosys 0.68 + nextpnr-xilinx 0.8.2-81-g1743d0f4``
part            yes       FPGA part, e.g. ``xc7a35tcpg236-1``
rtl_source      yes       ``generated`` (hw_dse.rtl.generator) or ``reference``
                          (the vendored reference RTL)
family          yes       registry family
data_width      yes       W
n_iter          yes       N
angle_guard     yes       A - W
frac_guard      yes       g
rounding        yes       ``trunc`` | ``round``
k, m            yes       1 unless the family uses them
luts            yes       LUTs (Vivado: Slice LUTs; Yosys: LUTn + INV + SRL cells)
ffs             yes       flip-flops (Vivado: Slice Registers)
carry4          no        CARRY4 count
fmax_mhz        no        blank if not measured (e.g. Yosys-only runs)
fmax_kind       no        how Fmax was obtained, e.g. ``post-route (nextpnr STA,
                          median of 3 seeds)`` or ``post-synthesis (1000/(T-WNS))``
target_mhz      no        clock constraint used
command         no        the exact command line(s)
source_log      no        path of the log the numbers were read from (relative
                          to the repository, or a description)
notes           no        anything else
==============  ========  ===================================================

Every row read back becomes a :class:`MeasuredPoint` whose ``provenance``
string is ``measured (<tool> <tool_version>)``.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

from hw_dse.families import REGISTRY, ArchConfig

REQUIRED = ("tool", "tool_version", "part", "rtl_source", "family", "data_width", "n_iter", "angle_guard",
            "frac_guard", "rounding", "k", "m", "luts", "ffs")
OPTIONAL = ("carry4", "fmax_mhz", "fmax_kind", "target_mhz", "command", "source_log", "notes")
COLUMNS = REQUIRED + OPTIONAL


@dataclass
class MeasuredPoint:
    tool: str
    tool_version: str
    part: str
    rtl_source: str
    arch: ArchConfig
    luts: float
    ffs: float
    fmax_mhz: float | None = None
    carry4: float | None = None
    extra: dict[str, str] = field(default_factory=dict)

    @property
    def provenance(self) -> str:
        return f"measured ({self.tool} {self.tool_version})"

    def row(self) -> dict[str, object]:
        p = self.arch.params()
        out: dict[str, object] = {
            "tool": self.tool, "tool_version": self.tool_version, "part": self.part, "rtl_source": self.rtl_source,
            "family": self.arch.family, "data_width": p["data_width"], "n_iter": p["n_iter"],
            "angle_guard": p["angle_guard"], "frac_guard": p["frac_guard"], "rounding": p["rounding"],
            "k": self.arch.k, "m": self.arch.m, "luts": self.luts, "ffs": self.ffs,
            "carry4": "" if self.carry4 is None else self.carry4,
            "fmax_mhz": "" if self.fmax_mhz is None else self.fmax_mhz,
        }
        for c in ("fmax_kind", "target_mhz", "command", "source_log", "notes"):
            out[c] = self.extra.get(c, "")
        return out


class SchemaError(ValueError):
    pass


def _num(v: str) -> float | None:
    v = (v or "").strip()
    return float(v) if v else None


def parse_rows(rows: list[dict[str, str]], where: str = "") -> list[MeasuredPoint]:
    """Validate rows against the schema; raise :class:`SchemaError` with every problem found."""
    errs: list[str] = []
    out: list[MeasuredPoint] = []
    for i, r in enumerate(rows, start=2):  # line 1 is the header
        missing = [c for c in REQUIRED if not str(r.get(c, "")).strip()]
        if missing:
            errs.append(f"{where}:{i}: missing {missing}")
            continue
        fam = r["family"].strip()
        if fam not in REGISTRY:
            errs.append(f"{where}:{i}: unknown family {fam!r}")
            continue
        try:
            arch = ArchConfig.from_params(fam, {
                "data_width": int(r["data_width"]), "n_iter": int(r["n_iter"]), "angle_guard": int(r["angle_guard"]),
                "frac_guard": int(r["frac_guard"]), "rounding": r["rounding"].strip(), "k": int(r["k"]), "m": int(r["m"])})
            luts, ffs = float(r["luts"]), float(r["ffs"])
            fmax = _num(r.get("fmax_mhz", ""))
            carry = _num(r.get("carry4", ""))
        except (ValueError, KeyError) as exc:
            errs.append(f"{where}:{i}: {exc}")
            continue
        if luts <= 0 or ffs < 0 or (fmax is not None and fmax <= 0):
            errs.append(f"{where}:{i}: non-physical luts/ffs/fmax")
            continue
        if r["rtl_source"].strip() not in ("generated", "reference"):
            errs.append(f"{where}:{i}: rtl_source must be 'generated' or 'reference'")
            continue
        out.append(MeasuredPoint(r["tool"].strip(), r["tool_version"].strip(), r["part"].strip(), r["rtl_source"].strip(),
                                 arch, luts, ffs, fmax, carry, {c: r.get(c, "") or "" for c in OPTIONAL}))
    if errs:
        raise SchemaError("invalid measured-points CSV:\n" + "\n".join(errs))
    return out


def load(path: str | Path) -> list[MeasuredPoint]:
    with open(path, newline="", encoding="utf-8") as fh:
        rd = csv.DictReader(fh)
        unknown = [c for c in (rd.fieldnames or []) if c not in COLUMNS]
        rows = list(rd)
    if unknown:
        raise SchemaError(f"{path}: unknown columns {unknown} (schema: {', '.join(COLUMNS)})")
    return parse_rows(rows, str(path))


def write(path: str | Path, points: list[MeasuredPoint]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(COLUMNS))
        w.writeheader()
        for p in points:
            w.writerow(p.row())
