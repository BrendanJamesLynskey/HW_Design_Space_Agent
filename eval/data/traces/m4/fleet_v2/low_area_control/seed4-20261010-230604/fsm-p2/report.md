# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec low_area_control: Field-oriented motor-control loop needing sin/cos of the rotor angle at >= 1 MSPS with max error <= 2^-10. Area is everything: minimise LUTs + FFs.
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min luts_plus_ffs (HV ref 1500)
  objective: max accuracy_bits (HV ref 10)
  select: min luts_plus_ffs
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=15,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 166 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 91 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 10.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 19 | exact: schedule |
| latency_ns | 95.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.184 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00081 (2^-10.27) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.64 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00021 (2^-12.22) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.72 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (31 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 166 | 91 | 10.4 | 19 | 0.184 | 0.00081 (2^-10.27) | 10.27 |
| 1 | `iterative:data_width=15,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 170 | 93 | 10.4 | 19 | 0.188 | 0.000599 (2^-10.71) | 10.71 |
| 2 | `iterative:data_width=15,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc` | 170 | 94 | 11.0 | 18 | 0.179 | 0.000567 (2^-10.78) | 10.78 |
| 3 | `iterative:data_width=16,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 178 | 96 | 11.0 | 18 | 0.185 | 0.000373 (2^-11.39) | 11.39 |
| 4 | `iterative:data_width=16,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 179 | 97 | 11.0 | 18 | 0.187 | 0.000301 (2^-11.70) | 11.70 |
| 5 | `iterative:data_width=16,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 181 | 98 | 11.0 | 18 | 0.189 | 0.000285 (2^-11.78) | 11.78 |
| 6 | `iterative:data_width=17,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 189 | 101 | 10.4 | 19 | 0.207 | 0.000244 (2^-12.00) | 12.00 |
| 7 | `iterative:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 193 | 103 | 10.8 | 18 | 0.2 | 0.000148 (2^-12.72) | 12.72 |
| 8 | `iterative:data_width=17,n_iter=16,angle_guard=4,frac_guard=0,rounding=round` | 196 | 105 | 10.2 | 19 | 0.215 | 0.000146 (2^-12.74) | 12.74 |
| 9 | `iterative:data_width=18,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 200 | 106 | 11.0 | 18 | 0.207 | 0.000145 (2^-12.75) | 12.75 |
| 10 | `iterative:data_width=17,n_iter=18,angle_guard=2,frac_guard=0,rounding=round` | 212 | 104 | 7.6 | 21 | 0.249 | 0.000139 (2^-12.81) | 12.81 |
| 11 | `iterative:data_width=18,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc` | 214 | 111 | 10.8 | 18 | 0.22 | 0.000102 (2^-13.26) | 13.26 |
| 12 | `iterative:data_width=19,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc` | 214 | 113 | 10.8 | 18 | 0.221 | 0.000101 (2^-13.27) | 13.27 |
| 13 | `iterative:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 216 | 112 | 10.2 | 19 | 0.234 | 6.86e-05 (2^-13.83) | 13.83 |
| 14 | `iterative:data_width=18,n_iter=18,angle_guard=1,frac_guard=2,rounding=trunc` | 242 | 112 | 7.6 | 21 | 0.28 | 6.72e-05 (2^-13.86) | 13.86 |
| 15 | `iterative:data_width=18,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc` | 263 | 115 | 5.7 | 28 | 0.398 | 5.18e-05 (2^-14.24) | 14.24 |
| 16 | `iterative:data_width=22,n_iter=16,angle_guard=1,frac_guard=1,rounding=trunc` | 250 | 129 | 10.0 | 19 | 0.271 | 3.34e-05 (2^-14.87) | 14.87 |
| 17 | `iterative:data_width=21,n_iter=27,angle_guard=2,frac_guard=0,rounding=round` | 283 | 124 | 5.2 | 30 | 0.46 | 1.15e-05 (2^-16.41) | 16.41 |
| 18 | `iterative:data_width=22,n_iter=22,angle_guard=0,frac_guard=0,rounding=round` | 296 | 127 | 6.4 | 25 | 0.398 | 8.91e-06 (2^-16.78) | 16.78 |
| 19 | `iterative:data_width=22,n_iter=26,angle_guard=3,frac_guard=0,rounding=round` | 303 | 130 | 5.4 | 29 | 0.472 | 5.23e-06 (2^-17.54) | 17.54 |
| 20 | `iterative:data_width=23,n_iter=21,angle_guard=0,frac_guard=0,rounding=round` | 313 | 132 | 6.5 | 24 | 0.402 | 4.39e-06 (2^-17.80) | 17.80 |
| 21 | `iterative:data_width=23,n_iter=23,angle_guard=2,frac_guard=1,rounding=trunc` | 319 | 136 | 6.0 | 26 | 0.445 | 3.08e-06 (2^-18.31) | 18.31 |
| 22 | `iterative:data_width=23,n_iter=26,angle_guard=4,frac_guard=0,rounding=round` | 323 | 136 | 5.3 | 29 | 0.501 | 2.9e-06 (2^-18.39) | 18.39 |
| 23 | `iterative:data_width=23,n_iter=25,angle_guard=2,frac_guard=2,rounding=trunc` | 339 | 138 | 5.6 | 28 | 0.503 | 1.91e-06 (2^-18.99) | 18.99 |
| 24 | `iterative:data_width=26,n_iter=25,angle_guard=0,frac_guard=0,rounding=trunc` | 358 | 147 | 5.6 | 28 | 0.532 | 9.22e-07 (2^-20.05) | 20.05 |
| 25 | `iterative:data_width=26,n_iter=27,angle_guard=1,frac_guard=0,rounding=trunc` | 360 | 148 | 5.1 | 30 | 0.573 | 8.79e-07 (2^-20.12) | 20.12 |
| 26 | `iterative:data_width=28,n_iter=25,angle_guard=-1,frac_guard=0,rounding=trunc` | 394 | 156 | 5.5 | 28 | 0.58 | 3.14e-07 (2^-21.60) | 21.60 |
| 27 | `iterative:data_width=28,n_iter=25,angle_guard=2,frac_guard=0,rounding=trunc` | 400 | 159 | 5.5 | 28 | 0.589 | 2.16e-07 (2^-22.14) | 22.14 |
| 28 | `iterative:data_width=28,n_iter=25,angle_guard=0,frac_guard=0,rounding=round` | 411 | 157 | 5.5 | 28 | 0.599 | 2.06e-07 (2^-22.21) | 22.21 |
| 29 | `iterative:data_width=28,n_iter=25,angle_guard=3,frac_guard=0,rounding=round` | 417 | 160 | 5.4 | 28 | 0.608 | 1.38e-07 (2^-22.79) | 22.79 |
| 30 | `iterative:data_width=28,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc` | 451 | 165 | 5.4 | 28 | 0.649 | 9.99e-08 (2^-23.26) | 23.26 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show iterative is the clear winner for this low-area spec: 16 of 17 front designs are iterative, with best luts_plus_ffs of 266. unrolled_k only had 2 feasible designs and none on the front, so it is not worth further budget. I am concentrating all remaining budget on iterative, narrowing the parameter ranges to the region that already produced the best results. The data_width range 12-18 balances the accuracy constraint (max_abs_err <= 2^-10) against area minimization. n_iter 10-18 provides enough micro-rotations for the required accuracy while keeping the datapath small. angle_guard and frac_guard are kept minimal to reduce LUT and FF counts. This focused search should refine the Pareto front and identify the optimal low-area design within the remaining budget.*)
- `iterative` (100 evals): data_width=12..18, n_iter=10..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative dominates the merged front (16/17 designs) with best area 266. I am narrowing the search to the region that produced feasible, low-area designs: data_width 12-18 (enough for 2^-10 error, small enough to keep area low), n_iter 10-18 (sufficient micro-rotations for accuracy without excessive area), angle_guard -2 to 2 (smaller guards reduce LUTs), frac_guard 0-2 (minimal extra fractional bits to save area). This focuses the remaining budget on refining the Pareto front in the most promising region.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 68 feasible; hypervolume 4633 (n/a).

**LLM decision:** `add_family` — The current front is dominated by the `iterative` family, which has a throughput bottleneck (1 result per N+3 cycles). While it meets the >= 1 MSPS constraint, its area (luts_plus_ffs) is relatively high for the accuracy achieved (starting at 263). The `unrolled_k` family allows multiple micro-rotations per cycle, which can significantly reduce the number of cycles per result and potentially allow for a smaller datapath or fewer iterations to meet the accuracy constraint, thereby lowering area. Additionally, `pipelined` and `pipelined_m` families offer 1 result/cycle throughput, which is much higher than `iterative`, but they typically have higher area due to pipeline registers. However, `unrolled_k` is a good middle ground that hasn't been explored yet. By adding `unrolled_k`, we can explore a different trade-off space that might yield better area/accuracy points, especially since the current front only covers data_width 15-18 and n_iter 12-18. The `unrolled_k` family might allow for lower n_iter or different data_width values that are more area-efficient.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 4633 (gain this round: n/a (first round)).
Feasible designs: 68 of 100 evaluations (51 unique).
Families explored so far: iterative. Not yet explored: unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14.5
- max_abs_err <= 0.000976562: 32% violate; best seen 6.72e-05 (2^-13.86)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.7, luts=170, ffs=93, throughput_msps=10.4, max_abs_err=0.000599 (2^-10.71), power_index=0.188
- iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=264, accuracy_bits=10.7, luts=170, ffs=94, throughput_msps=10.4, max_abs_err=0.000594 (2^-10.72), power_index=0.189
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.4, luts=178, ffs=96, throughput_msps=11, max_abs_err=0.000373 (2^-11.39), power_index=0.185
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.7, luts=179, ffs=97, throughput_msps=11, max_abs_err=0.000301 (2^-11.70), power_index=0.187
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=279, accuracy_bits=11.8, luts=181, ffs=98, throughput_msps=11, max_abs_err=0.000285 (2^-11.78), power_index=0.189
- iterative [data_width=17 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=290, accuracy_bits=12, luts=189, ffs=101, throughput_msps=10.4, max_abs_err=0.000244 (2^-12.00), power_index=0.207
- iterative [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=296, accuracy_bits=12.7, luts=193, ffs=103, throughput_msps=10.8, max_abs_err=0.000148 (2^-12.72), power_index=0.2
- iterative [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=306, accuracy_bits=12.8, luts=200, ffs=106, throughput_msps=11, max_abs_err=0.000145 (2^-12.75), power_index=0.207
- iterative [data_width=18 n_iter=18 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=354, accuracy_bits=13.9, luts=242, ffs=112, throughput_msps=7.57, max_abs_err=6.72e-05 (2^-13.86), power_index=0.28
Front coverage: luts_plus_ffs 263..354 (HV reference 1500); accuracy_bits 10.7..13.9 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 100 evals, 68 feasible; max throughput seen 14.5 MSPS; best accuracy 13.86 bits; best feasible luts_plus_ffs=263; feasible ranges: data_width 14..18, n_iter 12..18, angle_guard -2..2, frac_guard 0..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Add unrolled_k family to explore new trade-off space while continuing to refine the iterative family in its known promising region.*)
- `unrolled_k` (10 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Explore unrolled_k family to find potentially lower area designs with sufficient throughput and accuracy. Focus on k=2-4 to balance throughput and area.
- `iterative` (10 evals): data_width=14..18, n_iter=12..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Continue refining the iterative family in the known promising region to ensure we capture the best points on the current front.

**Result (code):** 20 evaluations this round, 120 total; 83 feasible; hypervolume 4635 (+0.0%).

**LLM decision:** `stop` — The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (iterative, data_width=15, n_iter=16) achieves 257 luts_plus_ffs with 10.3 bits of accuracy (max_abs_err ~2^-10.27), which meets the <= 2^-10 error constraint and >= 1 MSPS throughput constraint (10.4 MSPS). The front extends to 13.9 bits of accuracy, providing a good trade-off curve. Since this is the final round and the front covers the relevant region of the objective space (luts_plus_ffs 257..354, accuracy_bits 10.3..13.9) with no further budget available for exploration, stopping is the appropriate action. The selection rule (min luts_plus_ffs) will pick the 257-unit design, which is feasible and near the lower bound of the explored area range.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 4635 (gain this round: +0.0%).
Feasible designs: 83 of 120 evaluations (65 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14.5
- max_abs_err <= 0.000976562: 31% violate; best seen 6.72e-05 (2^-13.86)

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=10.4, max_abs_err=0.00081 (2^-10.27), power_index=0.184
- iterative [data_width=15 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.7, luts=170, ffs=93, throughput_msps=10.4, max_abs_err=0.000599 (2^-10.71), power_index=0.188
- iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=264, accuracy_bits=10.7, luts=170, ffs=94, throughput_msps=10.4, max_abs_err=0.000594 (2^-10.72), power_index=0.189
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.4, luts=178, ffs=96, throughput_msps=11, max_abs_err=0.000373 (2^-11.39), power_index=0.185
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.7, luts=179, ffs=97, throughput_msps=11, max_abs_err=0.000301 (2^-11.70), power_index=0.187
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=279, accuracy_bits=11.8, luts=181, ffs=98, throughput_msps=11, max_abs_err=0.000285 (2^-11.78), power_index=0.189
- iterative [data_width=17 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=290, accuracy_bits=12, luts=189, ffs=101, throughput_msps=10.4, max_abs_err=0.000244 (2^-12.00), power_index=0.207
- iterative [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=296, accuracy_bits=12.7, luts=193, ffs=103, throughput_msps=10.8, max_abs_err=0.000148 (2^-12.72), power_index=0.2
- iterative [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=306, accuracy_bits=12.8, luts=200, ffs=106, throughput_msps=11, max_abs_err=0.000145 (2^-12.75), power_index=0.207
- iterative [data_width=18 n_iter=18 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=354, accuracy_bits=13.9, luts=242, ffs=112, throughput_msps=7.57, max_abs_err=6.72e-05 (2^-13.86), power_index=0.28
Front coverage: luts_plus_ffs 257..354 (HV reference 1500); accuracy_bits 10.3..13.9 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 110 evals, 76 feasible; max throughput seen 14.5 MSPS; best accuracy 13.86 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 14..18, n_iter 12..18, angle_guard -2..2, frac_guard 0..2
- unrolled_k: 10 evals, 7 feasible; max throughput seen 13.5 MSPS; best accuracy 11.60 bits; best feasible luts_plus_ffs=392; feasible ranges: data_width 16..18, n_iter 12..17, angle_guard -2..1, frac_guard 0..2, k 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `iterative` (80 evals): data_width=14..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (10 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 161 feasible; hypervolume 1.424e+04 (+207.3%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (iterative, data_width=15, n_iter=16) achieves 257 luts_plus_ffs with 10.3 bits of accuracy (max_abs_err ~2^-10.27), which meets the <= 2^-10 error constraint and >= 1 MSPS throughput constraint (10.4 MSPS). The front extends to 13.9 bits of accuracy, providing a good trade-off curve. Since this is the final round and the front covers the relevant region of the objective space (luts_plus_ffs 257..354, accuracy_bits 10.3..13.9) with no further budget available for exploration, stopping is the appropriate action. The selection rule (min luts_plus_ffs) will pick the 257-unit design, which is feasible and near the lower bound of the explored area range.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.424e+04 (gain this round: +207.3%).
Feasible designs: 161 of 200 evaluations (133 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14.5
- max_abs_err <= 0.000976562: 20% violate; best seen 9.99e-08 (2^-23.26)

Pareto front (feasible, 31 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=10.4, max_abs_err=0.00081 (2^-10.27), power_index=0.184
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.4, luts=178, ffs=96, throughput_msps=11, max_abs_err=0.000373 (2^-11.39), power_index=0.185
- iterative [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=296, accuracy_bits=12.7, luts=193, ffs=103, throughput_msps=10.8, max_abs_err=0.000148 (2^-12.72), power_index=0.2
- iterative [data_width=17 n_iter=18 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=316, accuracy_bits=12.8, luts=212, ffs=104, throughput_msps=7.57, max_abs_err=0.000139 (2^-12.81), power_index=0.249
- iterative [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=328, accuracy_bits=13.8, luts=216, ffs=112, throughput_msps=10.2, max_abs_err=6.86e-05 (2^-13.83), power_index=0.234
- iterative [data_width=21 n_iter=27 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=407, accuracy_bits=16.4, luts=283, ffs=124, throughput_msps=5.2, max_abs_err=1.15e-05 (2^-16.41), power_index=0.46
- iterative [data_width=23 n_iter=21 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=445, accuracy_bits=17.8, luts=313, ffs=132, throughput_msps=6.5, max_abs_err=4.39e-06 (2^-17.80), power_index=0.402
- iterative [data_width=23 n_iter=25 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=477, accuracy_bits=19, luts=339, ffs=138, throughput_msps=5.57, max_abs_err=1.91e-06 (2^-18.99), power_index=0.503
- iterative [data_width=28 n_iter=25 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=559, accuracy_bits=22.1, luts=400, ffs=159, throughput_msps=5.47, max_abs_err=2.16e-07 (2^-22.14), power_index=0.589
- iterative [data_width=28 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=617, accuracy_bits=23.3, luts=451, ffs=165, throughput_msps=5.38, max_abs_err=9.99e-08 (2^-23.26), power_index=0.649
Front coverage: luts_plus_ffs 257..617 (HV reference 1500); accuracy_bits 10.3..23.3 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 190 evals, 154 feasible; max throughput seen 14.5 MSPS; best accuracy 23.26 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 10 evals, 7 feasible; max throughput seen 13.5 MSPS; best accuracy 11.60 bits; best feasible luts_plus_ffs=392; feasible ranges: data_width 16..18, n_iter 12..17, angle_guard -2..1, frac_guard 0..2, k 2..4
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7518 in, 1754 out
- provider-reported cost: $0.0043
- full prompts and replies: `llm_trace.jsonl`

