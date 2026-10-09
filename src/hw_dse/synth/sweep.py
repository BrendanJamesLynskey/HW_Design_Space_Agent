"""The L4 synthesis sweep: which designs are measured, and how results are stored.

Points (all on xc7a35tcpg236-1, 100 MHz target, see :mod:`hw_dse.synth.flow`):

* **The two Vivado anchors, twice**: the vendored reference RTL itself
  (``rtl_source=reference``) and the generated equivalent
  (``rtl_source=generated``), both iterative and pipelined at W=16, N=14.
  The reference rows give a like-for-like Yosys-vs-Vivado ratio on
  identical RTL; the generated rows show how close the generator's
  structure is to the reference's.
* **The six points to be re-run in Vivado** (:data:`VIVADO_POINTS`):
  ``unrolled_k`` k=2 and k=4, ``pipelined_m`` m=2 and m=4 (W=16, N=14), and
  ``pipelined`` at W=12 and W=24. For the two widths N is kept at **14**,
  the anchors' value, so only W changes between them and the anchor (no
  ground-truth winner uses W=12 or W=24 with ``pipelined``).
* **A spread** over every family: W from 8 to 28, N from 6 to 26, k and m
  from 2 to 8, both rounding modes, guard bits.
* **The three ground-truth winners** of the feasible specs, so the eval's
  "true optimum" designs have a measured counterpart.

Fmax is the median of three nextpnr placement seeds (1, 2, 3); LUT/FF counts
come from Yosys and do not depend on the seed.
"""

from __future__ import annotations

import gzip
import shutil
import statistics
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from hw_dse.families import ArchConfig
from hw_dse.rtl.generator import REPO_ROOT, generate
from hw_dse.synth import measured
from hw_dse.synth.flow import PART, SYNTH_BUILD, TARGET_MHZ, Runner, SynthResult, reference_port_bits, synthesize

L4_CSV = REPO_ROOT / "eval" / "data" / "l4_synthesis.csv"
L4_LOGS = REPO_ROOT / "eval" / "data" / "l4_logs"
REFERENCE_DIR = REPO_ROOT / "third_party" / "CORDIC"
SEEDS = (1, 2, 3)
TOOL = "yosys+nextpnr-xilinx"


def _a(family: str, w: int = 16, n: int = 14, ag: int = 0, g: int = 0, rnd: str = "trunc", k: int = 1, m: int = 1) -> ArchConfig:
    return ArchConfig.from_params(family, {"data_width": w, "n_iter": n, "angle_guard": ag, "frac_guard": g,
                                           "rounding": rnd, "k": k, "m": m})


ANCHORS = [_a("iterative"), _a("pipelined")]
VIVADO_POINTS = [_a("unrolled_k", k=2), _a("unrolled_k", k=4), _a("pipelined_m", m=2), _a("pipelined_m", m=4),
                 _a("pipelined", w=12), _a("pipelined", w=24)]
GT_WINNERS = [
    _a("pipelined", 18, 15, 1, 0, "round"),           # dds_250msps
    _a("iterative", 15, 12, 1, 0, "round"),           # low_area_control
    _a("pipelined_m", 26, 22, 0, 0, "round", m=6),    # high_precision
]
SPREAD = [
    _a("iterative", 8, 6), _a("iterative", 12, 10), _a("iterative", 20, 18), _a("iterative", 24, 22),
    _a("iterative", 28, 26), _a("iterative", 16, 20), _a("iterative", 16, 14, 2, 2, "round"),
    _a("unrolled_k", 8, 6, k=2), _a("unrolled_k", 12, 12, k=2), _a("unrolled_k", k=3), _a("unrolled_k", k=8),
    _a("unrolled_k", 24, 22, k=4), _a("unrolled_k", 16, 14, 2, 2, "round", k=2),
    _a("pipelined", 8, 6), _a("pipelined", 16, 8), _a("pipelined", 16, 20), _a("pipelined", 20, 18),
    _a("pipelined", 28, 26), _a("pipelined", 16, 14, 2, 2, "round"),
    _a("pipelined_m", 8, 6, m=2), _a("pipelined_m", 12, 12, m=2), _a("pipelined_m", m=3), _a("pipelined_m", m=6),
    _a("pipelined_m", m=8), _a("pipelined_m", 24, 22, m=4), _a("pipelined_m", 16, 14, 2, 2, "round", m=2),
]


def points() -> list[ArchConfig]:
    seen: set[str] = set()
    out = []
    for a in ANCHORS + VIVADO_POINTS + GT_WINNERS + SPREAD:
        if a.key() not in seen:
            seen.add(a.key())
            out.append(a)
    return out


@dataclass
class Job:
    arch: ArchConfig
    rtl_source: str  # generated | reference
    top: str
    sources: list[Path]
    ports: tuple[list[str], str] | None


def jobs(arches: list[ArchConfig] | None = None, include_reference: bool = True) -> list[Job]:
    out = []
    if include_reference:
        for a, mod in ((ANCHORS[0], "cordic_rotation_iterative"), (ANCHORS[1], "cordic_rotation_pipelined")):
            out.append(Job(a, "reference", mod, [REFERENCE_DIR / f"{mod}.sv"], reference_port_bits(mod, 16)))
    for a in arches if arches is not None else points():
        d = generate(a)
        out.append(Job(a, "generated", d.module, [], None))
    return out


def _run_one(job: Job, runner: Runner, pnr: bool, root: Path) -> tuple[Job, list[SynthResult]]:
    wd0 = root / f"{job.top}"
    if job.rtl_source == "generated":
        src = generate(job.arch).write(wd0)
        job.sources = [src]
    results = []
    for seed in (SEEDS if pnr else (1,)):
        wd = wd0 / f"seed{seed}"
        results.append(synthesize(job.sources, job.top, job.arch.numerics.data_width, wd, runner, pnr, seed,
                                  ports=job.ports))
    return job, results


def run(job_list: list[Job], runner: Runner | None = None, pnr: bool = True, workers: int = 4,
        root: Path = SYNTH_BUILD, log: bool = True) -> list[tuple[Job, list[SynthResult]]]:
    runner = runner or Runner.from_env()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(_run_one, j, runner, pnr, root) for j in job_list]
        out = []
        for f in futs:
            j, rs = f.result()
            if log:
                fm = [r.fmax_mhz for r in rs]
                print(f"{j.rtl_source:9s} {j.arch.key():78s} LUT {rs[0].luts:5d} FF {rs[0].ffs:5d} "
                      f"CARRY4 {rs[0].carry4:4d} Fmax {fm}", flush=True)
            out.append((j, rs))
    return out


def to_points(results: list[tuple[Job, list[SynthResult]]], versions: dict[str, str], pnr: bool = True,
              keep_logs: bool = True) -> list[measured.MeasuredPoint]:
    tv = f"yosys {versions['yosys']} + nextpnr-xilinx {versions['nextpnr']}" if pnr else f"yosys {versions['yosys']}"
    pts = []
    L4_LOGS.mkdir(parents=True, exist_ok=True)
    for job, rs in results:
        r0 = rs[0]
        fms = [r.fmax_mhz for r in rs if r.fmax_mhz is not None]
        log_rel = ""
        if keep_logs:
            name = f"{job.rtl_source}_{job.top}"
            with gzip.open(L4_LOGS / f"{name}.log.gz", "wt", encoding="utf-8") as fh:
                for r in rs:
                    wd = Path(r.workdir)
                    fh.write(f"===== seed {r.seed}: {r.yosys_cmd}\n")
                    fh.write((wd / "stat.txt").read_text())
                    if (wd / "pnr.log").exists():
                        fh.write(f"===== seed {r.seed}: {r.nextpnr_cmd}\n")
                        fh.write((wd / "pnr.log").read_text())
            log_rel = str((L4_LOGS / f"{name}.log.gz").relative_to(REPO_ROOT))
        extra = {
            "fmax_kind": (f"post-route (nextpnr-xilinx STA), median of seeds {','.join(map(str, SEEDS))}: "
                          + ";".join(f"{f:.2f}" for f in fms)) if fms else "",
            "target_mhz": f"{TARGET_MHZ:g}",
            "command": r0.yosys_cmd + (" && " + r0.nextpnr_cmd.replace(f"--seed {r0.seed}", "--seed <s>") if pnr else ""),
            "source_log": log_rel,
            "notes": f"runner {versions['runner']}; CARRY4 {r0.carry4}; MUXF7/8 {r0.muxf}; nextpnr SLICE_LUTX {r0.luts_pnr}",
        }
        pts.append(measured.MeasuredPoint(TOOL if pnr else "yosys", tv, PART, job.rtl_source, job.arch,
                                          float(r0.luts), float(r0.ffs),
                                          round(statistics.median(fms), 2) if fms else None, float(r0.carry4), extra))
    return pts


def clean_build(root: Path = SYNTH_BUILD) -> None:
    shutil.rmtree(root, ignore_errors=True)
