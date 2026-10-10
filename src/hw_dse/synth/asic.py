"""L4 for an ASIC target: Yosys + OpenSTA on the open sky130 PDK (provenance: measured).

Milestones 1-3 had one target, an Artix-7 FPGA. Milestone 4 adds a second,
an ASIC standard-cell flow on an open PDK, so the same agent and the same
families can be explored where the cost structure is different: on an FPGA a
4:1 mux is one LUT and an adder bit is one LUT plus a share of a CARRY4; in
standard cells a flip-flop is 5.3 NAND2-equivalents, a 2:1 mux 3, a full
adder 5.3, and there is no carry chain for free. Which family wins can move.

The library and the corner
--------------------------
**sky130_fd_sc_hd** (SkyWater 130 nm, high-density standard cells), the
library the open-source ASIC flows (OpenROAD-flow-scripts, OpenLane) use by
default for sky130, at the **typical corner tt_025C_1v80** (TT process,
25 C, 1.80 V). Why this one: it is the most widely used open PDK, its liberty
file is public and small enough to fetch in CI (12.8 MB), and Yosys and
OpenSTA read it directly. The file is pinned to a commit of
OpenROAD-flow-scripts and checked by SHA-256 (:data:`LIB_SHA256`); the
Google sky130 repositories ship only per-corner JSON, not merged ``.lib``
files.

Cells marked do-not-use
-----------------------
Yosys 0.33 has no ``abc -dont_use``, and left alone ABC maps some logic onto
``lpflow_*`` cells (power-gating isolation cells with an extra power-domain
pin, which a real flow never uses for datapath logic). Like the
OpenROAD-flow-scripts sky130hd platform's ``DONT_USE_CELLS``, this flow
removes the ``lpflow_*`` and ``probe_*`` cells: :func:`filtered_liberty`
writes a copy of the liberty without those cell groups (35 cells), used by
Yosys *and* OpenSTA. Nothing else in the library is changed.

The flow, per design
--------------------
1. **Yosys** (``synth -flatten``; ``dfflibmap`` and ``abc -D <period ps>``
   against the liberty; ``hilomap`` for constants)::

       read_verilog -sv top.sv; synth -flatten -top top;
       dfflibmap -liberty L; abc -D 10000 -liberty L; opt_clean;
       hilomap -singleton -hicell sky130_fd_sc_hd__conb_1 HI -locell sky130_fd_sc_hd__conb_1 LO;
       tee -o stat.txt stat -liberty L; write_verilog -noattr -noexpr netlist.v

   ``stat -liberty`` gives the **cell area in um^2** (the sum of the liberty
   ``area`` of every instance) and the cell counts. **Gate equivalents** are
   that area divided by the area of ``sky130_fd_sc_hd__nand2_1``
   (3.7536 um^2), the usual definition.
2. **OpenSTA** on the mapped netlist at the same 10 ns clock: register-to-
   register paths only (``group_path`` from every register clock pin to every
   register data pin), as the FPGA flow reports the clock domain's Fmax.
   Interconnect is the liberty's default wire-load model (``Small``, mode
   ``top``): there is no placement, so this is a **post-synthesis** timing,
   like the Vivado anchors' (and unlike nextpnr's post-route Fmax).
   ``Fmax = 1000 / (period - slack)``.
3. **OpenSTA ``report_power``** at that 10 ns clock (100 MHz), vectorless,
   every net toggling with activity 0.125 per clock (the FPGA model's
   activity factor), duty 0.5: internal + switching + leakage, in mW. It is a
   tool's estimate from a toggle-rate assumption, not a simulation of real
   stimulus, and it is labelled that way.

Optional place and route (OpenROAD) is **not** part of this flow: OpenROAD
was not installable natively here (no package for Ubuntu 24.04 in apt; the
conda package needs Python <= 3.10 and an old Qt; the container route needs
a Docker daemon this environment does not run). See the README.

Every row is *measured (yosys <ver> + OpenSTA <ver>, sky130_fd_sc_hd,
tt_025C_1v80)*, stored with its command lines in
``eval/data/asic_synthesis.csv`` (:data:`COLUMNS`).

Tools are found on PATH (``yosys``, ``sta``) or through ``HW_DSE_STA``; the
liberty through ``HW_DSE_SKY130_LIB`` or the default download location
``build/pdk/``. ``scripts/run_asic_sweep.py --fetch-lib`` downloads and checks
it.
"""

from __future__ import annotations

import csv
import hashlib
import os
import re
import shutil
import subprocess
import time
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from hw_dse.families import REGISTRY, ArchConfig
from hw_dse.rtl.generator import REPO_ROOT, generate

LIBRARY = "sky130_fd_sc_hd"
CORNER = "tt_025C_1v80"
LIB_NAME = f"{LIBRARY}__{CORNER}.lib"
ORFS_COMMIT = "5a76f84edc02baf49b75ccbd1a3a9e6a458a8d90"
LIB_URL = ("https://raw.githubusercontent.com/The-OpenROAD-Project/OpenROAD-flow-scripts/"
           f"{ORFS_COMMIT}/flow/platforms/sky130hd/lib/{LIB_NAME}")
LIB_SHA256 = "ec0e1067a35c8bf20b11e58d1e8ac53326067e4dac84a125cc1b917a3518d0d9"
DONT_USE = re.compile(r"lpflow_|probe_")
NAND2_AREA_UM2 = 3.7536  # sky130_fd_sc_hd__nand2_1, the gate-equivalent unit
CLOCK_NS = 10.0          # the same 100 MHz target as the FPGA flow
ACTIVITY = 0.125         # toggles per clock, every net (the FPGA model's activity factor)
PDK_DIR = REPO_ROOT / "build" / "pdk"
ASIC_BUILD = REPO_ROOT / "build" / "asic"
ASIC_CSV = REPO_ROOT / "eval" / "data" / "asic_synthesis.csv"
ASIC_LOGS = REPO_ROOT / "eval" / "data" / "asic_logs"
TOOL = "yosys+opensta"

# Flip-flop cells of sky130_fd_sc_hd: df* (plain, reset, set), edf* (enable),
# sdf*/sedf* (scan). Latches (dl*) are not expected in this RTL.
FF_CELL = re.compile(r"__(s?e?df[a-z]*|dl[a-z]*)_\d+$")

YOSYS_SCRIPT = (
    "read_verilog -sv {sources}; "
    "synth -flatten -top {top}; "
    "dfflibmap -liberty {lib}; "
    "abc -D {period_ps} -liberty {lib}; "
    "opt_clean; "
    "hilomap -singleton -hicell sky130_fd_sc_hd__conb_1 HI -locell sky130_fd_sc_hd__conb_1 LO; "
    "tee -o stat.txt stat -liberty {lib}; "
    "write_verilog -noattr -noexpr {top}_netlist.v"
)

STA_SCRIPT = """\
read_liberty {lib}
read_verilog {top}_netlist.v
link_design {top}
create_clock -name clk -period {period:g} [get_ports clk]
set_input_delay 0 -clock clk [delete_from_list [all_inputs] [get_ports clk]]
set_output_delay 0 -clock clk [all_outputs]
group_path -name reg2reg -from [all_registers -clock_pins] -to [all_registers -data_pins]
report_checks -path_delay max -path_group reg2reg -digits 4
set_power_activity -global -activity {activity:g} -duty 0.5
report_power -digits 6
"""
STA_CMD = "sta -no_init -no_splash -exit sta.tcl"


# ---------------------------------------------------------------------------
# The liberty file
# ---------------------------------------------------------------------------

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch_liberty(dest_dir: Path = PDK_DIR) -> Path:
    """Download the pinned liberty file (if absent) and check its SHA-256."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / LIB_NAME
    if not dest.exists():
        tmp = dest.with_suffix(".part")
        with urllib.request.urlopen(LIB_URL, timeout=300) as r, open(tmp, "wb") as fh:  # noqa: S310 - pinned https URL
            shutil.copyfileobj(r, fh)
        tmp.rename(dest)
    got = sha256(dest)
    if got != LIB_SHA256:
        raise RuntimeError(f"{dest}: SHA-256 {got} is not the pinned {LIB_SHA256}")
    return dest


def strip_cells(text: str, drop: re.Pattern[str] = DONT_USE) -> tuple[str, list[str]]:
    """Remove every ``cell (<name>) { ... }`` group whose name matches ``drop``.

    A brace-matching scan, not a full liberty parser: the cell groups of a
    liberty file are top-level children of ``library``, and braces inside
    them are balanced, so skipping from ``cell (`` to its matching ``}`` is
    exact. Returns the new text and the dropped cell names.
    """
    pat = re.compile(r'\n(\s*)cell \("?([A-Za-z0-9_]+)"?\)\s*\{')
    out: list[str] = []
    dropped: list[str] = []
    pos = 0
    while True:
        m = pat.search(text, pos)
        if not m:
            out.append(text[pos:])
            break
        j, depth = m.end(), 1
        while depth:
            c = text[j]
            depth += 1 if c == "{" else -1 if c == "}" else 0
            j += 1
        if drop.search(m.group(2)):
            out.append(text[pos:m.start()])
            dropped.append(m.group(2))
        else:
            out.append(text[pos:j])
        pos = j
    return "".join(out), dropped


def filtered_liberty(lib: Path, dest_dir: Path | None = None) -> Path:
    """The liberty without the do-not-use cells (cached next to it)."""
    dest = (dest_dir or lib.parent) / (lib.stem + "__dont_use_removed.lib")
    if not dest.exists() or dest.stat().st_mtime < lib.stat().st_mtime:
        text, _ = strip_cells(lib.read_text())
        dest.write_text(text)
    return dest


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@dataclass
class AsicTools:
    yosys: str | None
    sta: str | None
    lib: Path | None

    @staticmethod
    def from_env() -> AsicTools:
        lib_env = os.environ.get("HW_DSE_SKY130_LIB")
        lib = Path(lib_env) if lib_env else PDK_DIR / LIB_NAME
        return AsicTools(shutil.which("yosys"), os.environ.get("HW_DSE_STA") or shutil.which("sta"),
                         lib if lib.exists() else None)

    def available(self, sta: bool = True) -> tuple[bool, str]:
        miss = [n for n, v in (("yosys", self.yosys), ("sta (OpenSTA)", self.sta if sta else "x")) if not v]
        if self.lib is None:
            miss.append(f"liberty {LIB_NAME} (set HW_DSE_SKY130_LIB or run scripts/run_asic_sweep.py --fetch-lib)")
        return (not miss), ("missing: " + ", ".join(miss)) if miss else ""

    def versions(self) -> dict[str, str]:
        y = subprocess.run([self.yosys or "yosys", "-V"], capture_output=True, text=True).stdout.strip()
        m = re.search(r"Yosys (\S+)", y)
        out = {"yosys": m.group(1) if m else y}
        if self.sta:
            s = subprocess.run([self.sta, "-version"], capture_output=True, text=True).stdout.strip()
            out["sta"] = s
        return out


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_stat_liberty(text: str) -> tuple[float, dict[str, int]]:
    """(chip area in um^2, cell counts) from ``stat -liberty`` output."""
    m = re.findall(r"Chip area for (?:module|top module) '[^']*':\s+([0-9.]+)", text)
    if not m:
        raise ValueError("no 'Chip area' line in stat output")
    cells: dict[str, int] = {}
    for line in text.splitlines():
        s = line.split()
        if len(s) == 2 and s[0].startswith(LIBRARY + "__") and s[1].isdigit():
            cells[s[0]] = int(s[1])
        elif len(s) == 2 and s[1].startswith(LIBRARY + "__") and s[0].isdigit():
            cells[s[1]] = int(s[0])
    return float(m[-1]), cells


def parse_sta(text: str) -> dict[str, float | None]:
    """Worst reg-to-reg slack, arrival, required; power totals (mW)."""
    out: dict[str, float | None] = {"slack_ns": None, "arrival_ns": None, "required_ns": None}
    m = re.search(r"([-0-9.]+)\s+data arrival time", text)
    if m:
        out["arrival_ns"] = float(m.group(1))
    m = re.search(r"([-0-9.]+)\s+data required time", text)
    if m:
        out["required_ns"] = float(m.group(1))
    m = re.search(r"([-0-9.]+)\s+slack \((?:MET|VIOLATED)\)", text)
    if m:
        out["slack_ns"] = float(m.group(1))
    # report_power: "Total  <internal> <switching> <leakage> <total> 100.0%" in W
    m = re.search(r"^Total\s+([-0-9.e+]+)\s+([-0-9.e+]+)\s+([-0-9.e+]+)\s+([-0-9.e+]+)", text, re.M)
    if m:
        out.update(power_internal_mw=float(m.group(1)) * 1e3, power_switching_mw=float(m.group(2)) * 1e3,
                   power_leakage_mw=float(m.group(3)) * 1e3, power_mw=float(m.group(4)) * 1e3)
    return out


# ---------------------------------------------------------------------------
# One design
# ---------------------------------------------------------------------------

@dataclass
class AsicResult:
    top: str
    area_um2: float
    cells: dict[str, int]
    n_cells: int
    ffs: int
    critical_path_ns: float | None
    fmax_mhz: float | None
    power: dict[str, float]
    yosys_cmd: str
    sta_cmd: str
    seconds: float
    workdir: str
    notes: list[str] = field(default_factory=list)

    @property
    def gate_eq(self) -> float:
        return self.area_um2 / NAND2_AREA_UM2


def synthesize(sources: list[Path], top: str, workdir: Path, tools: AsicTools | None = None,
               sta: bool = True, period_ns: float = CLOCK_NS) -> AsicResult:
    """Yosys (+ OpenSTA unless ``sta=False``) on ``sources`` against sky130_fd_sc_hd."""
    tools = tools or AsicTools.from_env()
    ok, why = tools.available(sta)
    if not ok:
        raise RuntimeError(f"ASIC flow unavailable: {why}")
    assert tools.lib is not None
    workdir.mkdir(parents=True, exist_ok=True)
    lib = filtered_liberty(tools.lib, PDK_DIR if tools.lib.parent == PDK_DIR else workdir)
    names = []
    for s in sources:
        dst = workdir / Path(s).name
        if Path(s).resolve() != dst.resolve():
            shutil.copy(s, dst)
        names.append(dst.name)
    ys = YOSYS_SCRIPT.format(sources=" ".join(names), top=top, lib=lib, period_ps=int(round(period_ns * 1000)))
    t0 = time.time()
    p = subprocess.run([tools.yosys or "yosys", "-q", "-l", "yosys.log", "-p", ys], cwd=workdir,
                       capture_output=True, text=True, timeout=3600)
    if p.returncode != 0:
        raise RuntimeError(f"yosys failed:\n{p.stdout[-2000:]}\n{p.stderr[-2000:]}")
    area, cells = parse_stat_liberty((workdir / "stat.txt").read_text())
    ffs = sum(v for k, v in cells.items() if FF_CELL.search(k))
    path = fmax = None
    power: dict[str, float] = {}
    notes: list[str] = []
    if sta:
        (workdir / "sta.tcl").write_text(STA_SCRIPT.format(lib=lib, top=top, period=period_ns, activity=ACTIVITY))
        q = subprocess.run(["bash", "-c", STA_CMD.replace("sta ", f"{tools.sta} ", 1) + " > sta.log 2>&1"],
                           cwd=workdir, capture_output=True, text=True, timeout=3600)
        log = (workdir / "sta.log").read_text()
        if q.returncode != 0:
            raise RuntimeError(f"OpenSTA failed:\n{log[-3000:]}")
        r = parse_sta(log)
        if r["slack_ns"] is None:
            raise RuntimeError(f"OpenSTA reported no reg2reg path:\n{log[-3000:]}")
        path = period_ns - float(r["slack_ns"])
        fmax = 1000.0 / path
        power = {k: float(v) for k, v in r.items() if k.startswith("power") and v is not None}
    else:
        notes.append("Yosys only: no OpenSTA timing or power")
    return AsicResult(top, area, cells, sum(cells.values()), ffs, path, fmax, power, f"yosys -p '{ys}'",
                      STA_CMD if sta else "", round(time.time() - t0, 1), str(workdir), notes)


def synthesize_arch(arch: ArchConfig, tools: AsicTools | None = None, sta: bool = True,
                    root: Path | None = None) -> AsicResult:
    d = generate(arch)
    wd = (root or ASIC_BUILD) / d.module
    src = d.write(wd)
    return synthesize([src], d.module, wd, tools, sta)


# ---------------------------------------------------------------------------
# The measured-points CSV for the ASIC target
# ---------------------------------------------------------------------------

COLUMNS = (
    "tool", "tool_version", "library", "corner", "rtl_source", "family", "data_width", "n_iter", "angle_guard",
    "frac_guard", "rounding", "k", "m", "area_um2", "gate_eq", "n_cells", "ffs", "critical_path_ns", "fmax_mhz",
    "fmax_kind", "power_mw", "power_internal_mw", "power_switching_mw", "power_leakage_mw", "power_kind",
    "clock_ns", "command", "source_log", "notes",
)
"""Columns of ``eval/data/asic_synthesis.csv``. ``area_um2``: Yosys ``stat
-liberty`` cell area; ``gate_eq``: area / NAND2_X1 area; ``ffs``: flip-flop
cells; ``critical_path_ns``/``fmax_mhz``: OpenSTA worst reg-to-reg path at the
``clock_ns`` constraint, wire-load model, no placement; ``power_*``: OpenSTA
``report_power`` at ``clock_ns``, vectorless (``power_kind`` says how)."""


@dataclass
class AsicPoint:
    """One row of ``asic_synthesis.csv``, read back."""

    arch: ArchConfig
    area_um2: float
    gate_eq: float
    ffs: float
    fmax_mhz: float | None
    critical_path_ns: float | None
    power_mw: float | None
    row: dict[str, str]

    @property
    def provenance(self) -> str:
        return (f"measured ({self.row['tool']} {self.row['tool_version']}, {self.row['library']}, "
                f"{self.row['corner']})")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(COLUMNS))
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLUMNS})


def load_csv(path: Path = ASIC_CSV) -> list[AsicPoint]:
    with open(path, newline="", encoding="utf-8") as fh:
        rd = csv.DictReader(fh)
        if tuple(rd.fieldnames or ()) != COLUMNS:
            raise ValueError(f"{path}: columns {rd.fieldnames} are not the ASIC schema {COLUMNS}")
        rows = list(rd)
    out = []
    for r in rows:
        if r["family"] not in REGISTRY:
            raise ValueError(f"{path}: unknown family {r['family']!r}")
        arch = ArchConfig.from_params(r["family"], {k: (r[k] if k == "rounding" else int(r[k])) for k in
                                                    ("data_width", "n_iter", "angle_guard", "frac_guard", "rounding",
                                                     "k", "m")})

        def num(c: str) -> float | None:
            return float(r[c]) if r.get(c, "").strip() else None

        out.append(AsicPoint(arch, float(r["area_um2"]), float(r["gate_eq"]), float(r["ffs"]), num("fmax_mhz"),
                             num("critical_path_ns"), num("power_mw"), r))
    return out
