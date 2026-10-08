"""Run the reference CORDIC RTL in Icarus Verilog and capture its outputs.

This is the bridge between the Python golden model and real hardware
description code. It exists for one purpose: to *prove* that
``cordic_bitexact.cordic_sincos`` produces the same output codes as the
reference SystemVerilog for the reference configuration (W=16, N=14).

How it works
------------
1. Write the angle codes to a text file, one signed decimal per line.
2. Compile ``rtl_harness/tb_bitexact.sv`` together with the reference
   module using ``iverilog -g2012`` (``-DDUT_PIPELINED`` picks the
   pipelined module; otherwise the iterative one).
3. Run ``vvp``; the harness writes ``theta cos sin`` per angle.
4. Parse that back into NumPy arrays.

Where the reference RTL comes from
----------------------------------
The reference lives in its own public repo (BrendanJamesLynskey/CORDIC).
``scripts/fetch_reference_rtl.sh`` clones it at a pinned commit into
``third_party/CORDIC`` (git-ignored). ``CORDIC_RTL_DIR`` overrides that
location. If neither the RTL nor ``iverilog`` is available,
:func:`rtl_available` says so and the test is skipped cleanly.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[3]
HARNESS = REPO_ROOT / "rtl_harness" / "tb_bitexact.sv"

MODULE_FILES = {
    "iterative": "cordic_rotation_iterative.sv",
    "pipelined": "cordic_rotation_pipelined.sv",
}


def reference_rtl_dir() -> Path:
    env = os.environ.get("CORDIC_RTL_DIR")
    return Path(env) if env else REPO_ROOT / "third_party" / "CORDIC"


def rtl_available() -> tuple[bool, str]:
    """(available, reason). Used by the test to decide whether to skip."""
    if shutil.which("iverilog") is None or shutil.which("vvp") is None:
        return False, "iverilog/vvp not on PATH"
    d = reference_rtl_dir()
    missing = [f for f in MODULE_FILES.values() if not (d / f).exists()]
    if missing:
        return False, f"reference RTL not found in {d} (run scripts/fetch_reference_rtl.sh)"
    return True, ""


def simulate(angles: np.ndarray, dut: str = "iterative", timeout_s: float = 600.0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Simulate the reference module on ``angles``.

    Returns ``(theta, cos, sin)`` as int64 arrays in the order the harness
    reported them (which is input order for both DUTs).
    """
    if dut not in MODULE_FILES:
        raise ValueError(f"dut must be one of {sorted(MODULE_FILES)}")
    ok, why = rtl_available()
    if not ok:
        raise RuntimeError(why)
    rtl = reference_rtl_dir() / MODULE_FILES[dut]
    with tempfile.TemporaryDirectory(prefix="hw_dse_rtl_") as tmp:
        t = Path(tmp)
        angles_file, out_file, exe = t / "angles.txt", t / "out.txt", t / "sim.vvp"
        angles_file.write_text("\n".join(str(int(a)) for a in angles) + "\n")
        cmd = ["iverilog", "-g2012", "-o", str(exe)]
        if dut == "pipelined":
            cmd.append("-DDUT_PIPELINED")
        cmd += [str(HARNESS), str(rtl)]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        subprocess.run(
            ["vvp", "-n", str(exe), f"+angles={angles_file}", f"+out={out_file}"],
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        data = np.loadtxt(out_file, dtype=np.int64, ndmin=2)
    return data[:, 0], data[:, 1], data[:, 2]
