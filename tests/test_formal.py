"""SymbiYosys checks (W = 8): equivalence and latency/handshake properties.

Skipped locally without sby/yosys/z3; mandatory in CI (``HW_DSE_REQUIRE_FORMAL=1``).
Besides the committed jobs, two *mutation* checks make sure the properties are
not vacuous: a proof must fail when the expected latency is off by one, and
when the two pipelines differ in a rounding mode.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from hw_dse.families import ArchConfig
from hw_dse.rtl import formal
from tests.tooling import tool_mark

needs_formal = tool_mark("HW_DSE_REQUIRE_FORMAL", *formal.tool_status())


def test_committed_jobs_match_generator() -> None:
    """formal/*.sby and wrappers are exactly what hw_dse.rtl.formal writes."""
    for j in formal.jobs():
        assert (formal.FORMAL_DIR / f"{j.name}.sv").read_text() == j.wrapper, j.name
        assert (formal.FORMAL_DIR / f"{j.name}.sby").read_text() == formal.sby_text(j.name, j.modules, j.depth)


def test_committed_results_all_pass() -> None:
    with open(formal.RESULTS_CSV, newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert {r["job"] for r in rows} == {j.name for j in formal.jobs()}
    assert all(r["status"] == "PASS" for r in rows)


@needs_formal
@pytest.mark.parametrize("name", ["equiv_m3_round", "latency_iterative", "latency_pipelined_m"])
def test_formal_jobs_prove(name: str) -> None:
    formal.write_jobs()
    job = next(j for j in formal.jobs() if j.name == name)
    assert formal.run_job(job)["status"] == "PASS"


@needs_formal
@pytest.mark.skipif("not __import__('tests.tooling').tooling.full_sweep_requested()", reason="all jobs: HW_DSE_L3_FULL=1")
def test_all_formal_jobs_prove() -> None:
    formal.write_jobs()
    assert {j.name: formal.run_job(j)["status"] for j in formal.jobs()} == {j.name: "PASS" for j in formal.jobs()}


@needs_formal
def test_wrong_latency_is_caught(tmp_path: Path) -> None:
    a = formal.LATENCY_DUTS["latency_pipelined"]
    w = formal.latency_wrapper("mut_latency", a, latency=a.latency_cycles + 1)
    assert formal.run_custom("mut_latency", w, [a], 2 * a.latency_cycles + 8, tmp_path) == "FAIL"


@needs_formal
def test_inequivalent_pipelines_are_caught(tmp_path: Path) -> None:
    dut = ArchConfig.from_params("pipelined_m", {"data_width": 8, "n_iter": 6, "rounding": "round", "m": 2})
    ref = ArchConfig.from_params("pipelined", {"data_width": 8, "n_iter": 6, "rounding": "trunc"})
    w = formal.equiv_wrapper("mut_equiv", dut, ref_arch=ref)
    assert formal.run_custom("mut_equiv", w, [ref, dut], 12, tmp_path) == "FAIL"


@needs_formal
def test_fsm_not_ready_after_reset_is_caught(tmp_path: Path) -> None:
    """An FSM that keeps ready low for one cycle after reset must fail the latency job
    (the property is checked from the first cycle, not only after L cycles)."""
    a = formal.LATENCY_DUTS["latency_iterative"]

    def late_ready(_: str, text: str) -> str:
        return text.replace(
            "    assign ready = (state == S_IDLE);",
            "    logic woke;\n    always_ff @(posedge clk) woke <= !rst;\n"
            "    assign ready = (state == S_IDLE) && woke;")

    assert "woke" in late_ready("", __import__("hw_dse.rtl.generator", fromlist=["generate"]).generate(a).text)
    w = formal.latency_wrapper("mut_ready", a)
    assert formal.run_custom("mut_ready", w, [a], 2 * a.latency_cycles + 8, tmp_path, mutate=late_ready) == "FAIL"
