"""L4: open-source synthesis and place-and-route for Artix-7 (provenance: measured).

The analytical cost model (:mod:`hw_dse.models.cost_fpga`) *estimates* LUTs,
FFs and Fmax from structure and two Vivado anchors. This module *measures*
them, by pushing generated RTL through a real FPGA flow:

1. **Yosys** ``synth_xilinx -flatten -abc9 -arch xc7``: technology mapping to
   7-series primitives (LUT1..LUT6, MUXF7/F8, CARRY4, FDRE/FDSE/...).
   ``stat`` gives the cell counts, which are the resource numbers reported
   (LUTs = all LUTn cells incl. LUT-based shift registers; FFs = all FD*
   cells; CARRY4s). The mapped netlist is also written as Verilog for
   gate-level simulation (:mod:`hw_dse.synth.gatesim`).
2. **nextpnr-xilinx** (the openXC7 flow, prjxray-db timing data) places and
   routes that netlist on an **xc7a35tcpg236-1** (the part the Vivado anchors
   used) and runs its static timing analysis on the *routed* design. The
   reported "Max frequency for clock" after routing is recorded as Fmax.

Every result is labelled ``measured (yosys <ver> + nextpnr-xilinx <ver>)``
and stored with the exact command lines (``eval/data/l4_synthesis.csv``).

How to read these numbers next to Vivado's
------------------------------------------
They are real measurements of a *different* tool chain, and they are not
interchangeable with Vivado's:

* LUT counts: Yosys/ABC9 maps logic differently from Vivado, and Vivado
  reports *Slice LUTs* (a LUT6 site used as two LUT5s counts once) where the
  Yosys count is LUT cells. Expect systematic, design-dependent ratios.
* Fmax: nextpnr's delay model is built from prjxray timing data and its
  router differs from Vivado's; the anchors' Vivado figures are
  post-*synthesis* estimates (unplaced), these are post-*route*.

This is why :mod:`hw_dse.synth.recalibrate` fits a per-tool correction term
instead of mixing the two. Re-synthesising the two Vivado anchor designs
gives that ratio directly at W=16, N=14.

I/O and constraints
-------------------
The device needs every port bit on a package pin. :func:`xdc_for` places
``clk`` on W5 (a clock-capable MRCC pin) and the remaining port bits on the
other user I/O pins in a fixed order (LVCMOS33); 3W+4 bits fit up to W=28.
The clock target is 100 MHz (``create_clock -period 10``), the same
constraint the Vivado anchors were run with. I/O-to-register paths are not
part of the reported clock-domain Fmax.

Running the tools
-----------------
The openXC7 tools are heavy to build, so by default the flow runs them in
the public ``regymm/openxc7`` container image (``HW_DSE_SYNTH_RUNNER=docker``,
the default when ``docker`` is on PATH); with ``HW_DSE_SYNTH_RUNNER=native``
it calls ``yosys`` and ``nextpnr-xilinx`` from PATH. Either way it needs a
chip database for the part (``HW_DSE_CHIPDB_DIR``, containing
``xc7a35t.bin``); ``scripts/build_chipdb.sh`` builds one from the
prjxray-db shipped in the image. If place-and-route is unavailable the flow
can still run Yosys alone (``pnr=False``): resource counts, **no Fmax**.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path

from hw_dse.families import ArchConfig
from hw_dse.rtl.generator import REPO_ROOT, generate

PART = "xc7a35tcpg236-1"
CHIPDB_NAME = "xc7a35t.bin"
DEFAULT_IMAGE = "regymm/openxc7"
CLOCK_PIN = "W5"
TARGET_MHZ = 100.0
PINS_FILE = Path(__file__).with_name("xc7a35tcpg236_pins.csv")
SYNTH_BUILD = REPO_ROOT / "build" / "synth"

YOSYS_SCRIPT = (
    "read_verilog -sv {sources}; "
    "synth_xilinx -flatten -abc9 -arch xc7 -top {top}; "
    "tee -o stat.txt stat; "
    "write_json {top}.json; "
    "write_verilog -noattr {top}_netlist.v"
)
NEXTPNR_CMD = (
    "nextpnr-xilinx --chipdb {chipdb} --xdc {top}.xdc --json {top}.json --write {top}_routed.json "
    "--freq {freq:g} --seed {seed} --timing-allow-fail -l pnr.log"
)


def user_pins() -> list[str]:
    rows = [ln.split(",") for ln in PINS_FILE.read_text().splitlines() if ln and not ln.startswith("#")]
    return [r[0] for r in rows]


def port_bits(width: int) -> list[str]:
    """All top-level port bits of a generated module except clk, in a fixed order."""
    bits = ["rst", "valid_in", "ready", "valid_out"]
    for port in ("theta_in", "cos_out", "sin_out"):
        bits += [f"{port}[{i}]" for i in range(width)]
    return bits


REFERENCE_PORTS = {
    # The vendored reference modules have their own port names (see third_party/CORDIC).
    "cordic_rotation_iterative": (["SRST", "CE", "start", "done"], ("THETA_IN", "COS_OUT", "SIN_OUT"), "CLK"),
    "cordic_rotation_pipelined": (["SRST", "CE", "DATA_VALID_IN", "DATA_VALID_OUT"], ("THETA_IN", "COS_OUT", "SIN_OUT"), "CLK"),
}


def reference_port_bits(module: str, width: int) -> tuple[list[str], str]:
    scalars, buses, clock = REFERENCE_PORTS[module]
    bits = list(scalars)
    for port in buses:
        bits += [f"{port}[{i}]" for i in range(width)]
    return bits, clock


def xdc_for(width: int, bits: list[str] | None = None, clock: str = "clk") -> str:
    pins = [p for p in user_pins() if p != CLOCK_PIN]
    bits = bits if bits is not None else port_bits(width)
    if len(bits) > len(pins):
        raise ValueError(f"W={width} needs {len(bits)} I/O pins, the package has {len(pins)}")
    lines = [f"set_property LOC {CLOCK_PIN} [get_ports {clock}]", f"set_property IOSTANDARD LVCMOS33 [get_ports {clock}]",
             f"create_clock -period {1000.0 / TARGET_MHZ:.3f} -name {clock} [get_ports {clock}]"]
    for b, p in zip(bits, pins):
        lines.append(f"set_property LOC {p} [get_ports {{{b}}}]")
        lines.append(f"set_property IOSTANDARD LVCMOS33 [get_ports {{{b}}}]")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Tool runner: docker image or native PATH
# ---------------------------------------------------------------------------

@dataclass
class Runner:
    mode: str  # "docker" | "native"
    image: str = DEFAULT_IMAGE
    chipdb_dir: Path | None = None

    @staticmethod
    def from_env() -> Runner:
        mode = os.environ.get("HW_DSE_SYNTH_RUNNER") or ("native" if shutil.which("nextpnr-xilinx") else "docker")
        cdb = os.environ.get("HW_DSE_CHIPDB_DIR")
        return Runner(mode, os.environ.get("HW_DSE_OPENXC7_IMAGE", DEFAULT_IMAGE), Path(cdb) if cdb else None)

    def available(self, pnr: bool = True) -> tuple[bool, str]:
        if self.mode == "docker":
            if shutil.which("docker") is None:
                return False, "docker not on PATH"
            p = subprocess.run(["docker", "image", "inspect", self.image], capture_output=True, text=True)
            if p.returncode != 0:
                return False, f"docker image {self.image} not present (docker pull {self.image})"
        else:
            need = ["yosys"] + (["nextpnr-xilinx"] if pnr else [])
            miss = [t for t in need if shutil.which(t) is None]
            if miss:
                return False, f"{', '.join(miss)} not on PATH"
        if pnr and not (self.chipdb_dir and (self.chipdb_dir / CHIPDB_NAME).exists()):
            return False, f"no chip database: set HW_DSE_CHIPDB_DIR to a directory with {CHIPDB_NAME} (scripts/build_chipdb.sh)"
        return True, ""

    def run(self, shell_cmd: str, workdir: Path, timeout_s: float = 3600.0) -> subprocess.CompletedProcess[str]:
        if self.mode == "docker":
            cmd = ["docker", "run", "--rm", "-v", f"{workdir.resolve()}:/work", "-w", "/work"]
            if self.chipdb_dir:
                cmd += ["-v", f"{self.chipdb_dir.resolve()}:/chipdb:ro"]
            cmd += ["--entrypoint", "bash", self.image, "-c", shell_cmd]
        else:
            cmd = ["bash", "-c", shell_cmd]
        return subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, timeout=timeout_s)

    @property
    def chipdb_path(self) -> str:
        if self.mode == "docker":
            return f"/chipdb/{CHIPDB_NAME}"
        return str((self.chipdb_dir or Path(".")) / CHIPDB_NAME)

    def versions(self, workdir: Path) -> dict[str, str]:
        p = self.run("yosys -V; nextpnr-xilinx --version 2>&1 | head -1", workdir)
        lines = [ln.strip() for ln in p.stdout.splitlines() if ln.strip()]
        ys = next((ln for ln in lines if ln.startswith("Yosys")), "yosys ?")
        npr = next((ln for ln in lines if "nextpnr" in ln), "nextpnr-xilinx ?")
        m = re.search(r"Yosys (\S+)(?: \(git sha1 ([0-9a-f]+))?", ys)
        m2 = re.search(r"Version ([^)]+)\)", npr)
        yv = (f"{m.group(1)} (git {m.group(2)})" if m.group(2) else m.group(1)) if m else ys
        return {"yosys": yv, "nextpnr": m2.group(1) if m2 else npr,
                "runner": self.mode + (f":{self.image}" if self.mode == "docker" else "")}

    def cells_sim(self, dest: Path) -> Path:
        """Copy Yosys's Xilinx simulation models (matching *this* Yosys) to ``dest``."""
        dest.mkdir(parents=True, exist_ok=True)
        if self.mode == "docker":
            self.run("cp $(yosys-config --datdir)/xilinx/cells_sim.v /work/cells_sim.v", dest)
        else:
            if shutil.which("yosys-config"):
                dat = Path(subprocess.run(["yosys-config", "--datdir"], capture_output=True, text=True).stdout.strip())
            else:  # e.g. distro packages without yosys-dev: <prefix>/bin/yosys -> <prefix>/share/yosys
                dat = Path(shutil.which("yosys") or "yosys").resolve().parent.parent / "share" / "yosys"
            shutil.copy(dat / "xilinx" / "cells_sim.v", dest / "cells_sim.v")
        return dest / "cells_sim.v"


# ---------------------------------------------------------------------------
# One synthesis run
# ---------------------------------------------------------------------------

LUT_CELLS = re.compile(r"^(LUT[1-6]|INV|SRL16E|SRLC32E)$")  # INV is a LUT1 on 7-series
FF_CELLS = re.compile(r"^FD[RSCP]E(_1)?$")


@dataclass
class SynthResult:
    top: str
    luts: int
    ffs: int
    carry4: int
    muxf: int
    cells: dict[str, int]
    fmax_mhz: float | None
    luts_pnr: int | None
    ffs_pnr: int | None
    seed: int
    yosys_cmd: str
    nextpnr_cmd: str
    seconds: float
    workdir: str
    notes: list[str] = field(default_factory=list)


def parse_stat(text: str) -> dict[str, int]:
    """Cell counts from Yosys ``stat`` output (last module block)."""
    cells: dict[str, int] = {}
    # Yosys >= 0.4x prints "     <count>   <cell>"; older prints "     <cell>   <count>".
    for line in text.splitlines():
        s = line.split()
        if len(s) == 2:
            a, b = s
            if a.isdigit() and re.match(r"^[A-Z][A-Z0-9_]+$", b):
                cells[b] = int(a)
            elif b.isdigit() and re.match(r"^[A-Z][A-Z0-9_]+$", a):
                cells[a] = int(b)
    return cells


def parse_pnr_log(text: str) -> tuple[float | None, dict[str, int]]:
    """(post-route Fmax of the clk domain, utilisation by bel type)."""
    fmax = None
    for m in re.finditer(r"Max frequency for clock\s+'([^']+)':\s+([0-9.]+) MHz", text):
        fmax = float(m.group(2))  # the last report is the post-route one
    util: dict[str, int] = {}
    for m in re.finditer(r"^Info:\s+(\w+):\s+(\d+)/\s*(\d+)", text, re.M):
        util[m.group(1)] = int(m.group(2))
    return fmax, util


def synthesize(sources: list[Path], top: str, width: int, workdir: Path, runner: Runner | None = None,
               pnr: bool = True, seed: int = 1, freq_mhz: float = TARGET_MHZ,
               ports: tuple[list[str], str] | None = None) -> SynthResult:
    """Yosys (+ nextpnr-xilinx unless ``pnr=False``) on ``sources``.

    ``ports`` = (port bits, clock name) for modules without the generated
    port list (the vendored reference RTL).
    """
    runner = runner or Runner.from_env()
    workdir.mkdir(parents=True, exist_ok=True)
    names = []
    for s in sources:
        dst = workdir / Path(s).name
        if Path(s).resolve() != dst.resolve():
            shutil.copy(s, dst)
        names.append(dst.name)
    bits, clock = ports if ports else (None, "clk")
    (workdir / f"{top}.xdc").write_text(xdc_for(width, bits, clock))
    ys = YOSYS_SCRIPT.format(sources=" ".join(names), top=top)
    npr = NEXTPNR_CMD.format(chipdb=runner.chipdb_path, top=top, freq=freq_mhz, seed=seed)
    t0 = time.time()
    p = runner.run(f"yosys -q -l yosys.log -p '{ys}'", workdir)
    if p.returncode != 0:
        raise RuntimeError(f"yosys failed:\n{p.stdout[-2000:]}\n{p.stderr[-2000:]}")
    cells = parse_stat((workdir / "stat.txt").read_text())
    fmax, util, notes = None, {}, []
    if pnr:
        p = runner.run(npr, workdir)
        log = (workdir / "pnr.log").read_text() if (workdir / "pnr.log").exists() else p.stderr
        if p.returncode != 0:
            raise RuntimeError(f"nextpnr-xilinx failed:\n{log[-3000:]}")
        fmax, util = parse_pnr_log(log)
    else:
        notes.append("Yosys only: no place-and-route, no Fmax")
    return SynthResult(
        top=top,
        luts=sum(v for k, v in cells.items() if LUT_CELLS.match(k)),
        ffs=sum(v for k, v in cells.items() if FF_CELLS.match(k)),
        carry4=cells.get("CARRY4", 0),
        muxf=cells.get("MUXF7", 0) + cells.get("MUXF8", 0),
        cells=cells,
        fmax_mhz=fmax,
        luts_pnr=util.get("SLICE_LUTX"),
        ffs_pnr=util.get("SLICE_FFX"),
        seed=seed,
        yosys_cmd=f"yosys -p '{ys}'",
        nextpnr_cmd=npr if pnr else "",
        seconds=round(time.time() - t0, 1),
        workdir=str(workdir),
        notes=notes,
    )


def synthesize_arch(arch: ArchConfig, runner: Runner | None = None, pnr: bool = True, seed: int = 1,
                    root: Path | None = None) -> SynthResult:
    d = generate(arch)
    wd = (root or SYNTH_BUILD) / d.module
    src = d.write(wd)
    return synthesize([src], d.module, arch.numerics.data_width, wd, runner, pnr, seed)
