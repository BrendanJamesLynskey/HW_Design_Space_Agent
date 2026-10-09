# eval/data: what each file is and how it was made

Every number in these files comes from code or from a named tool. None comes
from an LLM. Provenance labels: *exact* (bit-accurate simulation),
*estimate* (cost model + calibration id), *measured (tool, version)*.

## L3: RTL verification

| file | what | regenerate |
|---|---|---|
| `l3_verification.csv` | one row per (configuration, simulator, level). `level=rtl`: generated SystemVerilog; `level=gate`: Yosys-mapped netlist simulated with that Yosys's `xilinx/cells_sim.v` (zero-delay). `mismatches` counts angles whose (cos, sin) codes differ from `cordic_sincos()`; `latency_ok` checks every result's latency against the documented one. Exhaustive sweep for W ≤ 16, dense (131,072-angle) sweep above. | `python scripts/run_l3_sweep.py` (rtl rows) and `python scripts/run_gate_sim.py` (gate rows) |
| `formal_results.csv` | SymbiYosys k-induction proofs (W = 8): `pipelined_m` ≡ `pipelined` after latency alignment, and valid/ready/latency properties per family. Jobs are in `formal/`. | `python -m hw_dse.rtl.formal` |

Simulators used for the committed rows: Verilator 5.020, Icarus Verilog 12.0
(Ubuntu 24.04 packages). Formal: Yosys 0.33, SBY (git), z3 4.8.12.

## L4: open-source synthesis (measured)

`l4_synthesis.csv` follows the measured-points schema of
`src/hw_dse/synth/measured.py` (the same schema the Vivado points will use).

* **Tools**: Yosys 0.68 (git 38e001a6f) and nextpnr-xilinx 0.8.2-81-g1743d0f4
  (openXC7), run from the `regymm/openxc7` container image (digest
  `sha256:35c910739e3a4b40850b85de31ebc8954985a66e982009f09123b70dbb0e75da`).
  Chip database built from the image's prjxray-db with `scripts/build_chipdb.sh`.
* **Part**: xc7a35tcpg236-1 (the Vivado anchors' part). Clock on pin W5, every
  other port bit on a user I/O pin (LVCMOS33); 100 MHz target (`--freq 100`), the
  anchors' 10 ns constraint.
* **Command** (per design; exact strings in the `command` column):

  ```
  yosys -p 'read_verilog -sv <top>.sv; synth_xilinx -flatten -abc9 -arch xc7 -top <top>;
            tee -o stat.txt stat; write_json <top>.json; write_verilog -noattr <top>_netlist.v'
  nextpnr-xilinx --chipdb xc7a35t.bin --xdc <top>.xdc --json <top>.json --write <top>_routed.json
                 --freq 100 --seed <1|2|3> --timing-allow-fail -l pnr.log
  ```
* **Columns**: `luts` = Yosys LUT1–LUT6 + INV (a LUT1 on 7-series) + LUT shift
  registers; `ffs` = FDRE/FDSE/FDCE/FDPE; `carry4`; `fmax_mhz` = median over
  nextpnr seeds 1, 2, 3 of the **post-route** "Max frequency for clock" figure
  (all three in `fmax_kind`). `notes` keeps nextpnr's SLICE_LUTX count, which
  counts LUT *bels* including route-throughs and is not comparable to Vivado's
  Slice LUTs.
* **Logs**: `l4_logs/<rtl_source>_<top>.log.gz` holds the Yosys `stat` output
  and the full nextpnr log of every seed.
* **Points**: the two Vivado anchors twice (vendored reference RTL and the
  generated equivalent), the six points to be re-run in Vivado (`unrolled_k`
  k=2/4, `pipelined_m` m=2/4, `pipelined` W=12/24; all N=14), the three
  ground-truth winners and a spread over every family (see
  `src/hw_dse/synth/sweep.py`).
* **Not comparable to Vivado one-to-one**: different mapper (ABC9 vs Vivado
  synthesis), different LUT accounting, and nextpnr's post-route timing model
  vs the anchors' Vivado post-synthesis estimates. `l5_refit_yosys-nextpnr.md`
  quantifies this with per-tool correction factors.

Regenerate: `HW_DSE_CHIPDB_DIR=<dir with xc7a35t.bin> python scripts/run_l4_sweep.py`
(about 10 minutes on 4 cores; `--yosys-only` for counts without place-and-route).

## L5: back-annotation

| file | what |
|---|---|
| `l5_refit_yosys-nextpnr.md` / `.json` | the cost model refitted to the 37 generated-RTL L4 points plus the two Vivado anchors, with one correction factor per tool and metric (Vivado = 1); residuals at every measured point before (M1 calibration) and after; the ground truth recomputed under the refit. Writes `src/hw_dse/models/calibration_artix7_refit_yosys-nextpnr.yaml`, which is **not** the default. |

Regenerate: `python -m hw_dse.synth.recalibrate --measured eval/data/l4_synthesis.csv --name yosys-nextpnr`.

## The eval

| file | what |
|---|---|
| `ground_truth.json` | exhaustive grid (635,040 designs) under the default (M1, 2-anchor Vivado) calibration: true front, true HV, the spec-selected design. Unchanged in M2. |
| `baselines.json` | M1 baselines (NSGA-II, random), 3 seeds. |
| `baselines_m2.json` | M2 baselines, 5 seeds. |
| `agent/` | M1 live agent runs (untouched). |
| `agent_m2/` | M2 live agent runs. |
| `spend_ledger.jsonl` | append-only provider-reported cost per live run (M1 and M2). |
| `key_usage_m2.json` | OpenRouter key usage before and after the M2 runs. |
| `levers_offline.json`, `levers_offline_round2.json` | offline tuning of the whole-curve levers by replaying the recorded M1 LLM decisions (`eval/tune_levers.py`). |
| `traces/` | M1 live-run traces; `traces/m2/` the M2 ones (`INDEX.md` in each). |
| `accuracy_table.csv.gz` | exact accuracy of every numeric configuration (golden model). |
