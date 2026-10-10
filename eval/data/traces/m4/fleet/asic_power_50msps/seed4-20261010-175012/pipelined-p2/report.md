# DSE run: asic_power_50msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
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
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=3` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 28058 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 7475 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 323 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 129 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.73 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000168 (2^-12.54) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 5.49 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 4.52e-05 (2^-14.43) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.48 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.5 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=3` | 28058 | 323 | 54.3 | 7 | 1.73 | 0.000168 (2^-12.54) | 12.54 |
| 1 | `pipelined_m:data_width=17,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=3` | 30828 | 381 | 54.3 | 8 | 1.97 | 0.000149 (2^-12.71) | 12.71 |
| 2 | `pipelined_m:data_width=17,n_iter=18,angle_guard=1,frac_guard=1,rounding=round,m=3` | 35792 | 393 | 54.3 | 8 | 2.15 | 0.000128 (2^-12.94) | 12.94 |
| 3 | `pipelined_m:data_width=19,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc,m=2` | 37244 | 576 | 69.4 | 10 | 2.7 | 8.04e-05 (2^-13.60) | 13.60 |
| 4 | `pipelined_m:data_width=18,n_iter=20,angle_guard=2,frac_guard=0,rounding=round,m=2` | 44765 | 655 | 72.3 | 12 | 3.14 | 7.75e-05 (2^-13.65) | 13.65 |
| 5 | `pipelined_m:data_width=20,n_iter=23,angle_guard=2,frac_guard=0,rounding=round,m=2` | 57300 | 853 | 66.8 | 14 | 4.06 | 2.17e-05 (2^-15.49) | 15.49 |
| 6 | `pipelined_m:data_width=24,n_iter=21,angle_guard=-2,frac_guard=1,rounding=round,m=2` | 61232 | 902 | 59.9 | 13 | 4.31 | 6.6e-06 (2^-17.21) | 17.21 |
| 7 | `pipelined_m:data_width=23,n_iter=21,angle_guard=1,frac_guard=2,rounding=trunc,m=2` | 61376 | 917 | 59.9 | 13 | 4.36 | 2.97e-06 (2^-18.36) | 18.36 |
| 8 | `pipelined_m:data_width=24,n_iter=22,angle_guard=2,frac_guard=2,rounding=trunc,m=2` | 66571 | 962 | 57.9 | 13 | 4.64 | 1.38e-06 (2^-19.47) | 19.47 |
| 9 | `pipelined_m:data_width=27,n_iter=22,angle_guard=-2,frac_guard=0,rounding=round,m=2` | 67566 | 983 | 56.1 | 13 | 4.72 | 1.27e-06 (2^-19.58) | 19.58 |
| 10 | `pipelined_m:data_width=24,n_iter=23,angle_guard=2,frac_guard=2,rounding=trunc,m=2` | 70573 | 1046 | 57.9 | 14 | 4.99 | 1.14e-06 (2^-19.74) | 19.74 |
| 11 | `pipelined_m:data_width=24,n_iter=23,angle_guard=2,frac_guard=2,rounding=round,m=2` | 71843 | 1048 | 57.9 | 14 | 5.03 | 7.74e-07 (2^-20.30) | 20.30 |
| 12 | `pipelined_m:data_width=24,n_iter=25,angle_guard=2,frac_guard=2,rounding=round,m=2` | 77991 | 1132 | 57.9 | 15 | 5.44 | 6.77e-07 (2^-20.50) | 20.50 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts are decisive: only the two pipelined families are feasible (iterative and unrolled_k have 0 feasible because their multi-cycle throughput cannot reach 50 MSPS at the Fmax the accuracy requires). pipelined_m is the power leader (best 1.84 vs pipelined's 3.66) because register-every-m cuts FFs and power while preserving 1 result/cycle, so it gets the larger share (0.6) and is narrowed to the feasible cluster (W 14-20, N 12-18, m 2-4) to resolve the power-vs-accuracy trade-off that the selection rule (min power_index) and the hypervolume both reward. pipelined (0.4) is retained to complete the front's high-accuracy end and because it already owns most front points; its ranges are tightened to the feasible cluster with a low frac_guard cap to stay on the low-power side. Both families are constrained to W>=14 and N>=12 to guarantee max_abs_err <= 2^-12 with small guards, and m is kept <=4 to protect the 50 MSPS throughput floor (Fmax x 1 result/cycle). This concentrates the 100-eval round where the trade-offs actually live rather than re-sampling infeasible or high-power corners.*)
- `pipelined_m` (60 evals): data_width=14..20, n_iter=12..18, angle_guard=-1..1, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m already holds the best feasible power_index (1.84) and 5 front points; it is the clear power winner because fewer registers than full pipelining cut FFs and power while still hitting 1 result/cycle. I narrow to the region that produced the feasible cluster: W 14-20 (12-bit accuracy needs ~14+ bits; going higher only adds area/power), N 12-18 (enough micro-rotations for <=2^-12 with modest guard bits), small angle/frac guards, and m 2-4 (m=2-3 balances register count vs critical-path depth; m>=4 risks Fmax dropping below the 50 MSPS throughput floor). This focuses the budget on the power-vs-accuracy trade-off that defines the front.
- `pipelined` (40 evals): data_width=14..18, n_iter=12..16, angle_guard=-1..1, frac_guard=0..1, rounding=trunc|round. *Why:* pipelined already dominates the merged front (16 of 21 points) and is the only family with a broad feasible region, so it must be kept to map the full trade-off curve for hypervolume. I tighten W to 14-18 and N to 12-16 (the feasible cluster) and cap frac_guard at 1 to avoid the high-power corner; full pipelining has the most registers so it is the power floor, and I want its best-accuracy points to complete the front. Keeping a smaller share than pipelined_m reflects that pipelined_m is the power leader and the selection rule (min power_index) will pick from there.

**Result (code):** 100 evaluations this round, 100 total; 19 feasible; hypervolume 60.32 (n/a).

**LLM decision:** `refine` — The current Pareto front is dominated by `pipelined_m` designs with `m=2` and `m=3`, achieving a minimum power index of 2.08. The `pipelined` family is significantly less efficient (best feasible power 3.72) and should be excluded from further search to focus the budget. The `pipelined_m` family shows a clear trend: lower `m` (2) yields lower power but slightly lower accuracy, while higher `m` (3) increases power but allows for better accuracy or lower data width. The current front spans accuracy 12.3 to 13.6 bits. To maximize hypervolume, we need to explore the trade-off more densely. Specifically, we should narrow the `pipelined_m` search space to the most promising region identified in Round 1: `data_width` 16-18 (to allow for lower power at the cost of accuracy, or slightly higher for robustness), `n_iter` 12-16 (sufficient for 12+ bits accuracy), `angle_guard` 0-1, `frac_guard` 0-1, and `m` 2-3. This focuses the 100 evaluations on refining the curve between the low-power/low-accuracy corner and the higher-accuracy/higher-power corner, rather than wasting evaluations on infeasible or dominated regions like `pipelined` or high `m` values that likely increase power without sufficient accuracy gain for the hypervolume objective.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 60.32 (gain this round: n/a (first round)).
Feasible designs: 19 of 100 evaluations (14 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 34% violate; best seen 163
- max_abs_err <= 0.000244141: 58% violate; best seen 2.58e-05 (2^-15.24)

Pareto front (feasible, 3 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=2] power_index=2.08, accuracy_bits=12.3, area_um2=29151, ffs=439, throughput_msps=78.8, max_abs_err=0.000204 (2^-12.26)
- pipelined_m [data_width=17 n_iter=18 angle_guard=1 frac_guard=1 rounding=round m=3] power_index=2.15, accuracy_bits=12.9, area_um2=35792, ffs=393, throughput_msps=54.3, max_abs_err=0.000128 (2^-12.94)
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=2] power_index=2.7, accuracy_bits=13.6, area_um2=37244, ffs=576, throughput_msps=69.4, max_abs_err=8.04e-05 (2^-13.60)
Front coverage: power_index 2.08..2.7 (HV reference 40); accuracy_bits 12.3..13.6 (HV reference 12); data_width on the front 17..19 (registry 8..28).

Per family:
- pipelined: 40 evals, 6 feasible; max throughput seen 163 MSPS; best accuracy 13.18 bits; best feasible power_index=3.72; feasible ranges: data_width 17..18, n_iter 15..16, angle_guard 0..1, frac_guard 0..0
- pipelined_m: 60 evals, 13 feasible; max throughput seen 82.5 MSPS; best accuracy 15.24 bits; best feasible power_index=2.08; feasible ranges: data_width 17..19, n_iter 14..18, angle_guard -1..1, frac_guard 0..2, m 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Refine `pipelined_m` ranges to focus on the trade-off curve between power and accuracy.*)
- `pipelined_m` (20 evals): data_width=16..18, n_iter=12..16, angle_guard=0..1, frac_guard=0..1, rounding=trunc|round, m=2..3. *Why:* Focuses search on the efficient `pipelined_m` family in the region where feasible designs were found, narrowing ranges to improve density of the Pareto front.

**Result (code):** 20 evaluations this round, 120 total; 22 feasible; hypervolume 60.56 (+0.4%).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 4 distinct designs covering the trade-off space from power_index=1.73 (accuracy_bits=12.5) to power_index=2.7 (accuracy_bits=13.6). The hypervolume has stabilized (only +0.4% gain in the last round), indicating diminishing returns. The best design (pipelined_m, data_width=17, n_iter=15, m=3) meets all constraints: throughput 54.3 MSPS >= 50, max_abs_err 2^-12.54 <= 2^-12, and has the minimum power_index of 1.73. Since this is the final round, we stop and select the design with minimum power_index from the front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 60.56 (gain this round: +0.4%).
Feasible designs: 22 of 120 evaluations (17 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 28% violate; best seen 163
- max_abs_err <= 0.000244141: 62% violate; best seen 2.58e-05 (2^-15.24)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=1.73, accuracy_bits=12.5, area_um2=28058, ffs=323, throughput_msps=54.3, max_abs_err=0.000168 (2^-12.54)
- pipelined_m [data_width=17 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=1.97, accuracy_bits=12.7, area_um2=30828, ffs=381, throughput_msps=54.3, max_abs_err=0.000149 (2^-12.71)
- pipelined_m [data_width=17 n_iter=18 angle_guard=1 frac_guard=1 rounding=round m=3] power_index=2.15, accuracy_bits=12.9, area_um2=35792, ffs=393, throughput_msps=54.3, max_abs_err=0.000128 (2^-12.94)
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=2] power_index=2.7, accuracy_bits=13.6, area_um2=37244, ffs=576, throughput_msps=69.4, max_abs_err=8.04e-05 (2^-13.60)
Front coverage: power_index 1.73..2.7 (HV reference 40); accuracy_bits 12.5..13.6 (HV reference 12); data_width on the front 17..19 (registry 8..28).

Per family:
- pipelined: 40 evals, 6 feasible; max throughput seen 163 MSPS; best accuracy 13.18 bits; best feasible power_index=3.72; feasible ranges: data_width 17..18, n_iter 15..16, angle_guard 0..1, frac_guard 0..0
- pipelined_m: 80 evals, 16 feasible; max throughput seen 82.5 MSPS; best accuracy 15.24 bits; best feasible power_index=1.73; feasible ranges: data_width 17..19, n_iter 14..18, angle_guard -1..1, frac_guard 0..2, m 2..3
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (80 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 46 feasible; hypervolume 305.9 (+405.1%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 4 distinct designs covering the trade-off space from power_index=1.73 (accuracy_bits=12.5) to power_index=2.7 (accuracy_bits=13.6). The hypervolume has stabilized (only +0.4% gain in the last round), indicating diminishing returns. The best design (pipelined_m, data_width=17, n_iter=15, m=3) meets all constraints: throughput 54.3 MSPS >= 50, max_abs_err 2^-12.54 <= 2^-12, and has the minimum power_index of 1.73. Since this is the final round, we stop and select the design with minimum power_index from the front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 305.9 (gain this round: +405.1%).
Feasible designs: 46 of 200 evaluations (35 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 41% violate; best seen 163
- max_abs_err <= 0.000244141: 44% violate; best seen 3.14e-08 (2^-24.93)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=1.73, accuracy_bits=12.5, area_um2=28058, ffs=323, throughput_msps=54.3, max_abs_err=0.000168 (2^-12.54)
- pipelined_m [data_width=17 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=1.97, accuracy_bits=12.7, area_um2=30828, ffs=381, throughput_msps=54.3, max_abs_err=0.000149 (2^-12.71)
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=2] power_index=2.7, accuracy_bits=13.6, area_um2=37244, ffs=576, throughput_msps=69.4, max_abs_err=8.04e-05 (2^-13.60)
- pipelined_m [data_width=18 n_iter=20 angle_guard=2 frac_guard=0 rounding=round m=2] power_index=3.14, accuracy_bits=13.7, area_um2=44765, ffs=655, throughput_msps=72.3, max_abs_err=7.75e-05 (2^-13.65)
- pipelined_m [data_width=20 n_iter=23 angle_guard=2 frac_guard=0 rounding=round m=2] power_index=4.06, accuracy_bits=15.5, area_um2=57300, ffs=853, throughput_msps=66.8, max_abs_err=2.17e-05 (2^-15.49)
- pipelined_m [data_width=23 n_iter=21 angle_guard=1 frac_guard=2 rounding=trunc m=2] power_index=4.36, accuracy_bits=18.4, area_um2=61376, ffs=917, throughput_msps=59.9, max_abs_err=2.97e-06 (2^-18.36)
- pipelined_m [data_width=24 n_iter=22 angle_guard=2 frac_guard=2 rounding=trunc m=2] power_index=4.64, accuracy_bits=19.5, area_um2=66571, ffs=962, throughput_msps=57.9, max_abs_err=1.38e-06 (2^-19.47)
- pipelined_m [data_width=27 n_iter=22 angle_guard=-2 frac_guard=0 rounding=round m=2] power_index=4.72, accuracy_bits=19.6, area_um2=67566, ffs=983, throughput_msps=56.1, max_abs_err=1.27e-06 (2^-19.58)
- pipelined_m [data_width=24 n_iter=23 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=5.03, accuracy_bits=20.3, area_um2=71843, ffs=1048, throughput_msps=57.9, max_abs_err=7.74e-07 (2^-20.30)
- pipelined_m [data_width=24 n_iter=25 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=5.44, accuracy_bits=20.5, area_um2=77991, ffs=1132, throughput_msps=57.9, max_abs_err=6.77e-07 (2^-20.50)
Front coverage: power_index 1.73..5.44 (HV reference 40); accuracy_bits 12.5..20.5 (HV reference 12); data_width on the front 17..27 (registry 8..28).

Per family:
- pipelined: 40 evals, 6 feasible; max throughput seen 163 MSPS; best accuracy 13.18 bits; best feasible power_index=3.72; feasible ranges: data_width 17..18, n_iter 15..16, angle_guard 0..1, frac_guard 0..0
- pipelined_m: 160 evals, 40 feasible; max throughput seen 82.5 MSPS; best accuracy 24.93 bits; best feasible power_index=1.73; feasible ranges: data_width 16..27, n_iter 14..25, angle_guard -2..2, frac_guard 0..4, m 2..3
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 6647 in, 2141 out
- provider-reported cost: $0.0058
- full prompts and replies: `llm_trace.jsonl`

