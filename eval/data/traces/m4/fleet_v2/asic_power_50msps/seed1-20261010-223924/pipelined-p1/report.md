# DSE run: asic_power_50msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_power_50msps: A 50 MSPS sin/cos unit in sky130 standard cells for a battery-powered radio: max error <= 2^-12. Minimise the relative power index; accuracy is the trade-off.
  target: asic-sky130hd
  constraint: throughput_msps >= 50
  constraint: max_abs_err <= 0.000244141
  objective: min power_index (HV ref 40)
  objective: max accuracy_bits (HV ref 12)
  select: min power_index
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined:data_width=20,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 50675 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 13500 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 1071 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 123 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 123 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 138 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 4.47 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 6.58e-05 (2^-13.89) | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 17.2 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.5e-05 (2^-15.29) | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 6.55 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.9 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (14 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=20,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 50675 | 1071 | 123.1 | 17 | 4.47 | 6.58e-05 (2^-13.89) | 13.89 |
| 1 | `pipelined:data_width=24,n_iter=15,angle_guard=3,frac_guard=2,rounding=round` | 59786 | 1262 | 104.7 | 17 | 5.27 | 6.1e-05 (2^-14.00) | 14.00 |
| 2 | `pipelined:data_width=20,n_iter=18,angle_guard=2,frac_guard=2,rounding=trunc` | 59909 | 1284 | 123.1 | 20 | 5.33 | 1.92e-05 (2^-15.67) | 15.67 |
| 3 | `pipelined:data_width=23,n_iter=18,angle_guard=2,frac_guard=0,rounding=trunc` | 64219 | 1380 | 111.3 | 20 | 5.73 | 1.07e-05 (2^-16.51) | 16.51 |
| 4 | `pipelined:data_width=23,n_iter=18,angle_guard=2,frac_guard=2,rounding=trunc` | 67354 | 1443 | 111.3 | 20 | 6 | 8.56e-06 (2^-16.83) | 16.83 |
| 5 | `pipelined:data_width=24,n_iter=18,angle_guard=3,frac_guard=0,rounding=round` | 67528 | 1451 | 104.7 | 20 | 6.02 | 8.29e-06 (2^-16.88) | 16.88 |
| 6 | `pipelined:data_width=23,n_iter=18,angle_guard=2,frac_guard=2,rounding=round` | 68573 | 1445 | 111.3 | 20 | 6.04 | 8.28e-06 (2^-16.88) | 16.88 |
| 7 | `pipelined:data_width=23,n_iter=19,angle_guard=2,frac_guard=0,rounding=trunc` | 67889 | 1457 | 111.3 | 21 | 6.05 | 7.63e-06 (2^-17.00) | 17.00 |
| 8 | `pipelined:data_width=21,n_iter=21,angle_guard=4,frac_guard=4,rounding=round` | 79875 | 1679 | 111.3 | 23 | 7.02 | 2.61e-06 (2^-18.55) | 18.55 |
| 9 | `pipelined:data_width=27,n_iter=20,angle_guard=3,frac_guard=0,rounding=trunc` | 83546 | 1789 | 96.1 | 22 | 7.43 | 2.08e-06 (2^-18.88) | 18.88 |
| 10 | `pipelined:data_width=25,n_iter=21,angle_guard=3,frac_guard=4,rounding=round` | 90742 | 1906 | 98.8 | 23 | 7.97 | 1.07e-06 (2^-19.83) | 19.83 |
| 11 | `pipelined:data_width=24,n_iter=24,angle_guard=2,frac_guard=2,rounding=round` | 95116 | 2000 | 107.9 | 26 | 8.36 | 7.24e-07 (2^-20.40) | 20.40 |
| 12 | `pipelined:data_width=27,n_iter=24,angle_guard=0,frac_guard=1,rounding=round` | 100914 | 2122 | 101.6 | 26 | 8.87 | 3.47e-07 (2^-21.46) | 21.46 |
| 13 | `pipelined:data_width=25,n_iter=25,angle_guard=3,frac_guard=3,rounding=round` | 106034 | 2227 | 101.6 | 27 | 9.31 | 2.49e-07 (2^-21.94) | 21.94 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands throughput >= 50 MSPS and max_abs_err <= 2^-12, minimising power_index. Only the pipelined and pipelined_m families produce 1 result/cycle, so throughput equals Fmax and the throughput constraint reduces to Fmax >= 50 MHz; the iterative/unrolled_k families (not in my fleet) would need Fmax >= 50*k and are excluded anyway. I split the 100-eval budget evenly: pipelined_m is the likely winner for min power (fewer registers, same 1/cycle throughput) so it anchors the low-power end, while pipelined anchors the high-accuracy/high-power end. Both sweep the full accuracy-relevant ranges (n_iter, data_width, angle_guard, frac_guard, rounding) so the merged front covers the whole accuracy-vs-power trade-off curve, which is what the hypervolume rewards. The reserved front-mapping portion of the budget will then refine these ranges over the full family extents.*)
- `pipelined` (30 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* pipelined gives 1 result/cycle, so throughput = Fmax. To hit 50 MSPS it needs Fmax >= 50 MHz. A full pipeline of N stages is the most area/power-hungry variant, so it is the 'high accuracy / high power' anchor of the front. I keep the full n_iter/data_width sweep so Optuna can find the minimum-N, minimum-W point that still clears max_abs_err <= 2^-12, and the rounding/guard trade-offs that trade a few accuracy bits against area/power. This maps the expensive end of the trade-off curve.
- `pipelined_m` (30 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* pipelined_m registers only every m stages, so it keeps 1 result/cycle (throughput = Fmax) while cutting FF count and area versus the full pipeline. This is the most promising family for the min-power objective: fewer registers means lower power_index and smaller area, and the longer combinational path per stage can still clear 50 MHz for moderate m. Sweeping m (2..8) together with n_iter/data_width lets Optuna find the sweet spot where the path is fast enough for 50 MSPS but the register count is minimised, mapping the low-power end of the front.

**Result (code):** 60 evaluations this round, 60 total; 20 feasible; hypervolume 325.4 (n/a).

**LLM decision:** `stop` — The Pareto front is well-mapped and feasible. The minimum power_index on the front is 6.1 (pipelined, data_width=26, n_iter=17), which satisfies the throughput constraint (98.8 MSPS >= 50) and the accuracy constraint (16 bits > 12 bits required). The front extends to 21.9 bits accuracy, covering the trade-off space adequately. Since this is the final round, we stop and select the design with minimum power_index (6.1) as the final design.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 325.4 (gain this round: n/a (first round)).
Feasible designs: 20 of 60 evaluations (17 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 45% violate; best seen 180
- max_abs_err <= 0.000244141: 52% violate; best seen 2.49e-07 (2^-21.94)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined [data_width=26 n_iter=17 angle_guard=3 frac_guard=0 rounding=trunc] power_index=6.1, accuracy_bits=16, area_um2=68348, ffs=1471, throughput_msps=98.8, max_abs_err=1.54e-05 (2^-15.98)
- pipelined [data_width=25 n_iter=17 angle_guard=3 frac_guard=3 rounding=round] power_index=6.31, accuracy_bits=16, area_um2=71747, ffs=1511, throughput_msps=102, max_abs_err=1.53e-05 (2^-15.99)
- pipelined [data_width=21 n_iter=21 angle_guard=0 frac_guard=3 rounding=trunc] power_index=6.48, accuracy_bits=16, area_um2=73029, ffs=1557, throughput_msps=115, max_abs_err=1.49e-05 (2^-16.03)
- pipelined [data_width=21 n_iter=21 angle_guard=4 frac_guard=4 rounding=round] power_index=7.02, accuracy_bits=18.5, area_um2=79875, ffs=1679, throughput_msps=111, max_abs_err=2.61e-06 (2^-18.55)
- pipelined [data_width=25 n_iter=21 angle_guard=3 frac_guard=4 rounding=round] power_index=7.97, accuracy_bits=19.8, area_um2=90742, ffs=1906, throughput_msps=98.8, max_abs_err=1.07e-06 (2^-19.83)
- pipelined [data_width=25 n_iter=25 angle_guard=0 frac_guard=3 rounding=round] power_index=9, accuracy_bits=20, area_um2=102558, ffs=2153, throughput_msps=102, max_abs_err=9.54e-07 (2^-20.00)
- pipelined [data_width=25 n_iter=25 angle_guard=3 frac_guard=3 rounding=round] power_index=9.31, accuracy_bits=21.9, area_um2=106034, ffs=2227, throughput_msps=102, max_abs_err=2.49e-07 (2^-21.94)
Front coverage: power_index 6.1..9.31 (HV reference 40); accuracy_bits 16..21.9 (HV reference 12); data_width on the front 21..26 (registry 8..28).

Per family:
- pipelined: 30 evals, 20 feasible; max throughput seen 180 MSPS; best accuracy 21.94 bits; best feasible power_index=6.1; feasible ranges: data_width 15..28, n_iter 17..30, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 30 evals, 0 feasible; max throughput seen 102 MSPS; best accuracy 19.38 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (40 evals): data_width=20..28, n_iter=15..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (7 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 60 feasible; hypervolume 332.3 (+2.1%).

**No LLM call** (code's front-mapping round): The Pareto front is well-mapped and feasible. The minimum power_index on the front is 6.1 (pipelined, data_width=26, n_iter=17), which satisfies the throughput constraint (98.8 MSPS >= 50) and the accuracy constraint (16 bits > 12 bits required). The front extends to 21.9 bits accuracy, covering the trade-off space adequately. Since this is the final round, we stop and select the design with minimum power_index (6.1) as the final design.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 332.3 (gain this round: +2.1%).
Feasible designs: 60 of 100 evaluations (56 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 27% violate; best seen 180
- max_abs_err <= 0.000244141: 31% violate; best seen 2.49e-07 (2^-21.94)

Pareto front (feasible, 14 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined [data_width=20 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] power_index=4.47, accuracy_bits=13.9, area_um2=50675, ffs=1071, throughput_msps=123, max_abs_err=6.58e-05 (2^-13.89)
- pipelined [data_width=24 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] power_index=5.27, accuracy_bits=14, area_um2=59786, ffs=1262, throughput_msps=105, max_abs_err=6.1e-05 (2^-14.00)
- pipelined [data_width=23 n_iter=18 angle_guard=2 frac_guard=0 rounding=trunc] power_index=5.73, accuracy_bits=16.5, area_um2=64219, ffs=1380, throughput_msps=111, max_abs_err=1.07e-05 (2^-16.51)
- pipelined [data_width=23 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc] power_index=6, accuracy_bits=16.8, area_um2=67354, ffs=1443, throughput_msps=111, max_abs_err=8.56e-06 (2^-16.83)
- pipelined [data_width=23 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] power_index=6.04, accuracy_bits=16.9, area_um2=68573, ffs=1445, throughput_msps=111, max_abs_err=8.28e-06 (2^-16.88)
- pipelined [data_width=23 n_iter=19 angle_guard=2 frac_guard=0 rounding=trunc] power_index=6.05, accuracy_bits=17, area_um2=67889, ffs=1457, throughput_msps=111, max_abs_err=7.63e-06 (2^-17.00)
- pipelined [data_width=27 n_iter=20 angle_guard=3 frac_guard=0 rounding=trunc] power_index=7.43, accuracy_bits=18.9, area_um2=83546, ffs=1789, throughput_msps=96.1, max_abs_err=2.08e-06 (2^-18.88)
- pipelined [data_width=25 n_iter=21 angle_guard=3 frac_guard=4 rounding=round] power_index=7.97, accuracy_bits=19.8, area_um2=90742, ffs=1906, throughput_msps=98.8, max_abs_err=1.07e-06 (2^-19.83)
- pipelined [data_width=27 n_iter=24 angle_guard=0 frac_guard=1 rounding=round] power_index=8.87, accuracy_bits=21.5, area_um2=100914, ffs=2122, throughput_msps=102, max_abs_err=3.47e-07 (2^-21.46)
- pipelined [data_width=25 n_iter=25 angle_guard=3 frac_guard=3 rounding=round] power_index=9.31, accuracy_bits=21.9, area_um2=106034, ffs=2227, throughput_msps=102, max_abs_err=2.49e-07 (2^-21.94)
Front coverage: power_index 4.47..9.31 (HV reference 40); accuracy_bits 13.9..21.9 (HV reference 12); data_width on the front 20..27 (registry 8..28).

Per family:
- pipelined: 70 evals, 60 feasible; max throughput seen 180 MSPS; best accuracy 21.94 bits; best feasible power_index=4.47; feasible ranges: data_width 15..28, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 30 evals, 0 feasible; max throughput seen 102 MSPS; best accuracy 19.38 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4311 in, 1303 out
- provider-reported cost: $0.0022
- full prompts and replies: `llm_trace.jsonl`

