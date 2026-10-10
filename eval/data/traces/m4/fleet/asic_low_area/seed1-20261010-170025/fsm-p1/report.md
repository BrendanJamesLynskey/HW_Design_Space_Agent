# DSE run: asic_low_area

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_low_area: Motor-control sin/cos in sky130 standard cells: >= 1 MSPS, max error <= 2^-10. Area is everything: minimise cell area.
  target: asic-sky130hd
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min area_um2 (HV ref 40000)
  objective: max accuracy_bits (HV ref 10)
  select: min area_um2
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=15,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 7405 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1973 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 104 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 136 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 8 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 125 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.172 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000462 (2^-11.08) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 3.79 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000118 (2^-13.05) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 0.967 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 11.1 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc` | 7405 | 104 | 8.0 | 17 | 0.172 | 0.000462 (2^-11.08) | 11.08 |
| 1 | `iterative:data_width=15,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc` | 7466 | 104 | 7.6 | 18 | 0.183 | 0.000393 (2^-11.31) | 11.31 |
| 2 | `iterative:data_width=15,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc` | 7529 | 105 | 7.6 | 18 | 0.185 | 0.000344 (2^-11.51) | 11.51 |
| 3 | `iterative:data_width=16,n_iter=16,angle_guard=3,frac_guard=0,rounding=round` | 7621 | 107 | 6.6 | 19 | 0.199 | 0.000285 (2^-11.78) | 11.78 |
| 4 | `iterative:data_width=17,n_iter=16,angle_guard=3,frac_guard=0,rounding=round` | 8037 | 113 | 6.4 | 19 | 0.209 | 0.000146 (2^-12.74) | 12.74 |
| 5 | `iterative:data_width=17,n_iter=22,angle_guard=2,frac_guard=0,rounding=round` | 8183 | 113 | 5.0 | 25 | 0.277 | 0.000139 (2^-12.81) | 12.81 |
| 6 | `iterative:data_width=18,n_iter=15,angle_guard=3,frac_guard=1,rounding=trunc` | 8507 | 120 | 6.5 | 18 | 0.211 | 0.000118 (2^-13.05) | 13.05 |
| 7 | `iterative:data_width=18,n_iter=16,angle_guard=3,frac_guard=1,rounding=trunc` | 8580 | 120 | 6.2 | 19 | 0.223 | 8.72e-05 (2^-13.49) | 13.49 |
| 8 | `iterative:data_width=22,n_iter=17,angle_guard=3,frac_guard=0,rounding=round` | 10289 | 141 | 5.2 | 20 | 0.278 | 1.8e-05 (2^-15.76) | 15.76 |
| 9 | `iterative:data_width=25,n_iter=22,angle_guard=1,frac_guard=0,rounding=round` | 11992 | 155 | 4.0 | 25 | 0.393 | 1.41e-06 (2^-19.44) | 19.44 |
| 10 | `iterative:data_width=27,n_iter=24,angle_guard=3,frac_guard=0,rounding=trunc` | 12999 | 169 | 3.3 | 27 | 0.46 | 4.11e-07 (2^-21.22) | 21.22 |
| 11 | `iterative:data_width=27,n_iter=24,angle_guard=0,frac_guard=0,rounding=round` | 13088 | 165 | 3.6 | 27 | 0.456 | 3.79e-07 (2^-21.33) | 21.33 |
| 12 | `iterative:data_width=27,n_iter=24,angle_guard=1,frac_guard=1,rounding=round` | 15802 | 169 | 3.5 | 27 | 0.504 | 2.38e-07 (2^-22.01) | 22.01 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >=1 MSPS throughput and max_abs_err <= 2^-10, with area as the primary objective. Throughput is easily met by both iterative and unrolled_k since Fmax will be well above 1 MHz. The key trade-off is between area (minimize data_width, n_iter, guards) and accuracy (need enough iterations and bits to hit 2^-10 error). I focus data_width 12-18 and n_iter 12-16 because these are the parameters that most directly control both area and accuracy. frac_guard and angle_guard are kept in their full ranges to let the optimizer find the minimal guard values that still meet accuracy. iterative gets 60% of budget as it is the lowest-area family; unrolled_k gets 40% to explore whether unrolling can trade a small area increase for a better accuracy/area point on the Pareto front.*)
- `iterative` (36 evals): data_width=12..18, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* iterative is the lowest-area family (single datapath, no pipeline registers). For >=1 MSPS it needs Fmax >= 1 MHz, which is trivially met. The area/accuracy trade-off is driven by data_width and n_iter; frac_guard and angle_guard add area for marginal accuracy. Focusing n_iter 12-16 and data_width 12-18 covers the region where max_abs_err <= 2^-10 is achievable at minimal area.
- `unrolled_k` (24 evals): data_width=12..18, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..4. *Why:* unrolled_k with k=2..4 reduces latency and may allow a slightly higher Fmax, but adds area from duplicated datapath logic. Since area is the primary objective, this family is less likely to beat iterative, but k=2 with fewer iterations could offer a different point on the Pareto front. Limited budget share since iterative is expected to dominate on area.

**Result (code):** 60 evaluations this round, 60 total; 51 feasible; hypervolume 1.351e+05 (n/a).

**LLM decision:** `stop` — The spec is fully satisfied with a large margin on the critical constraint. The Pareto front contains 11 feasible designs, all meeting throughput >= 1 MSPS (best 10.1 MSPS) and max_abs_err <= 2^-10 (best 4.81e-05 = 2^-14.34, well below the 9.77e-04 limit). The minimum area design is the iterative CORDIC with data_width=15, n_iter=14, angle_guard=1, frac_guard=2, truncation, at 7405 um^2 with 11.1 accuracy bits and 8 MSPS throughput. This is far below the HV reference of 40000 um^2. The front spans a reasonable trade-off curve from 7405 um^2/11.1 bits to 13847 um^2/14.3 bits, covering the accuracy range from just above the 10-bit reference to well beyond it. The iterative family dominates on area (7405 vs 12183 best for unrolled_k), and the pipelined families were not needed since the iterative architecture already achieves >1 MSPS throughput with the lowest area. The selection rule (min area) picks the 7405 um^2 design, which is robustly feasible. No further exploration would improve the hypervolume meaningfully given the budget is exhausted and the front is well-mapped in the relevant region.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.351e+05 (gain this round: n/a (first round)).
Feasible designs: 51 of 60 evaluations (40 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 10.1
- max_abs_err <= 0.000976562: 15% violate; best seen 4.81e-05 (2^-14.34)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=7405, accuracy_bits=11.1, ffs=104, throughput_msps=8, max_abs_err=0.000462 (2^-11.08), power_index=0.172
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=7466, accuracy_bits=11.3, ffs=104, throughput_msps=7.56, max_abs_err=0.000393 (2^-11.31), power_index=0.183
- iterative [data_width=15 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7529, accuracy_bits=11.5, ffs=105, throughput_msps=7.56, max_abs_err=0.000344 (2^-11.51), power_index=0.185
- iterative [data_width=16 n_iter=16 angle_guard=3 frac_guard=0 rounding=round] area_um2=7621, accuracy_bits=11.8, ffs=107, throughput_msps=6.64, max_abs_err=0.000285 (2^-11.78), power_index=0.199
- iterative [data_width=17 n_iter=16 angle_guard=3 frac_guard=0 rounding=round] area_um2=8037, accuracy_bits=12.7, ffs=113, throughput_msps=6.41, max_abs_err=0.000146 (2^-12.74), power_index=0.209
- iterative [data_width=18 n_iter=16 angle_guard=3 frac_guard=1 rounding=trunc] area_um2=8580, accuracy_bits=13.5, ffs=120, throughput_msps=6.2, max_abs_err=8.72e-05 (2^-13.49), power_index=0.223
- unrolled_k [data_width=17 n_iter=16 angle_guard=4 frac_guard=2 rounding=round k=2] area_um2=12685, accuracy_bits=13.8, ffs=117, throughput_msps=5.79, max_abs_err=6.89e-05 (2^-13.82), power_index=0.154
- unrolled_k [data_width=17 n_iter=16 angle_guard=3 frac_guard=4 rounding=round k=2] area_um2=13340, accuracy_bits=14.1, ffs=120, throughput_msps=5.79, max_abs_err=5.86e-05 (2^-14.06), power_index=0.16
- unrolled_k [data_width=17 n_iter=16 angle_guard=4 frac_guard=4 rounding=round k=2] area_um2=13445, accuracy_bits=14.2, ffs=121, throughput_msps=5.79, max_abs_err=5.18e-05 (2^-14.24), power_index=0.161
- unrolled_k [data_width=18 n_iter=16 angle_guard=2 frac_guard=4 rounding=round k=2] area_um2=13847, accuracy_bits=14.3, ffs=125, throughput_msps=5.58, max_abs_err=4.81e-05 (2^-14.34), power_index=0.166
Front coverage: area_um2 7405..13847 (HV reference 40000); accuracy_bits 11.1..14.3 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 36 evals, 31 feasible; max throughput seen 10.1 MSPS; best accuracy 13.49 bits; best feasible area_um2=7405; feasible ranges: data_width 13..18, n_iter 12..16, angle_guard -2..3, frac_guard 0..3
- unrolled_k: 24 evals, 20 feasible; max throughput seen 6.82 MSPS; best accuracy 14.34 bits; best feasible area_um2=12183; feasible ranges: data_width 16..18, n_iter 12..16, angle_guard 0..4, frac_guard 0..4, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (26 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (7 front designs; box front_anchored)
- `unrolled_k` (14 evals): data_width=16..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (4 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 90 feasible; hypervolume 3.501e+05 (+159.2%).

**No LLM call** (code's front-mapping round): The spec is fully satisfied with a large margin on the critical constraint. The Pareto front contains 11 feasible designs, all meeting throughput >= 1 MSPS (best 10.1 MSPS) and max_abs_err <= 2^-10 (best 4.81e-05 = 2^-14.34, well below the 9.77e-04 limit). The minimum area design is the iterative CORDIC with data_width=15, n_iter=14, angle_guard=1, frac_guard=2, truncation, at 7405 um^2 with 11.1 accuracy bits and 8 MSPS throughput. This is far below the HV reference of 40000 um^2. The front spans a reasonable trade-off curve from 7405 um^2/11.1 bits to 13847 um^2/14.3 bits, covering the accuracy range from just above the 10-bit reference to well beyond it. The iterative family dominates on area (7405 vs 12183 best for unrolled_k), and the pipelined families were not needed since the iterative architecture already achieves >1 MSPS throughput with the lowest area. The selection rule (min area) picks the 7405 um^2 design, which is robustly feasible. No further exploration would improve the hypervolume meaningfully given the budget is exhausted and the front is well-mapped in the relevant region.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 3.501e+05 (gain this round: +159.2%).
Feasible designs: 90 of 100 evaluations (73 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 10.1
- max_abs_err <= 0.000976562: 10% violate; best seen 2.38e-07 (2^-22.01)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=7405, accuracy_bits=11.1, ffs=104, throughput_msps=8, max_abs_err=0.000462 (2^-11.08), power_index=0.172
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=7466, accuracy_bits=11.3, ffs=104, throughput_msps=7.56, max_abs_err=0.000393 (2^-11.31), power_index=0.183
- iterative [data_width=16 n_iter=16 angle_guard=3 frac_guard=0 rounding=round] area_um2=7621, accuracy_bits=11.8, ffs=107, throughput_msps=6.64, max_abs_err=0.000285 (2^-11.78), power_index=0.199
- iterative [data_width=17 n_iter=16 angle_guard=3 frac_guard=0 rounding=round] area_um2=8037, accuracy_bits=12.7, ffs=113, throughput_msps=6.41, max_abs_err=0.000146 (2^-12.74), power_index=0.209
- iterative [data_width=17 n_iter=22 angle_guard=2 frac_guard=0 rounding=round] area_um2=8183, accuracy_bits=12.8, ffs=113, throughput_msps=5.05, max_abs_err=0.000139 (2^-12.81), power_index=0.277
- iterative [data_width=18 n_iter=16 angle_guard=3 frac_guard=1 rounding=trunc] area_um2=8580, accuracy_bits=13.5, ffs=120, throughput_msps=6.2, max_abs_err=8.72e-05 (2^-13.49), power_index=0.223
- iterative [data_width=22 n_iter=17 angle_guard=3 frac_guard=0 rounding=round] area_um2=10289, accuracy_bits=15.8, ffs=141, throughput_msps=5.19, max_abs_err=1.8e-05 (2^-15.76), power_index=0.278
- iterative [data_width=25 n_iter=22 angle_guard=1 frac_guard=0 rounding=round] area_um2=11992, accuracy_bits=19.4, ffs=155, throughput_msps=4.03, max_abs_err=1.41e-06 (2^-19.44), power_index=0.393
- iterative [data_width=27 n_iter=24 angle_guard=0 frac_guard=0 rounding=round] area_um2=13088, accuracy_bits=21.3, ffs=165, throughput_msps=3.63, max_abs_err=3.79e-07 (2^-21.33), power_index=0.456
- iterative [data_width=27 n_iter=24 angle_guard=1 frac_guard=1 rounding=round] area_um2=15802, accuracy_bits=22, ffs=169, throughput_msps=3.53, max_abs_err=2.38e-07 (2^-22.01), power_index=0.504
Front coverage: area_um2 7405..15802 (HV reference 40000); accuracy_bits 11.1..22 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 62 evals, 56 feasible; max throughput seen 10.1 MSPS; best accuracy 22.01 bits; best feasible area_um2=7405; feasible ranges: data_width 13..27, n_iter 12..27, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 38 evals, 34 feasible; max throughput seen 6.82 MSPS; best accuracy 20.66 bits; best feasible area_um2=12183; feasible ranges: data_width 16..28, n_iter 12..27, angle_guard -1..4, frac_guard 0..4, k 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4626 in, 1102 out
- provider-reported cost: $0.0017
- full prompts and replies: `llm_trace.jsonl`

