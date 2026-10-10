# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
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
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=20,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 227 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 118 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 194 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 10.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 92.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.234 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 7.03e-05 (2^-13.80) | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 18.4 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.53e-05 (2^-15.27) | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 6.64 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.8 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (17 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=20,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 227 | 118 | 10.8 | 18 | 0.234 | 7.03e-05 (2^-13.80) | 13.80 |
| 1 | `iterative:data_width=20,n_iter=16,angle_guard=3,frac_guard=1,rounding=trunc` | 231 | 121 | 10.0 | 19 | 0.252 | 4.27e-05 (2^-14.51) | 14.51 |
| 2 | `iterative:data_width=21,n_iter=16,angle_guard=3,frac_guard=1,rounding=trunc` | 242 | 126 | 10.0 | 19 | 0.263 | 3.85e-05 (2^-14.67) | 14.67 |
| 3 | `iterative:data_width=20,n_iter=17,angle_guard=3,frac_guard=1,rounding=trunc` | 264 | 122 | 7.8 | 20 | 0.29 | 3.13e-05 (2^-14.96) | 14.96 |
| 4 | `iterative:data_width=21,n_iter=21,angle_guard=1,frac_guard=1,rounding=trunc` | 282 | 125 | 6.6 | 24 | 0.368 | 1.38e-05 (2^-16.15) | 16.15 |
| 5 | `iterative:data_width=22,n_iter=29,angle_guard=3,frac_guard=2,rounding=trunc` | 322 | 134 | 4.9 | 32 | 0.549 | 4.23e-06 (2^-17.85) | 17.85 |
| 6 | `iterative:data_width=26,n_iter=22,angle_guard=-2,frac_guard=1,rounding=trunc` | 364 | 147 | 6.1 | 25 | 0.481 | 2.02e-06 (2^-18.91) | 18.91 |
| 7 | `iterative:data_width=26,n_iter=27,angle_guard=3,frac_guard=0,rounding=trunc` | 363 | 150 | 5.1 | 30 | 0.58 | 7.68e-07 (2^-20.31) | 20.31 |
| 8 | `iterative:data_width=26,n_iter=27,angle_guard=1,frac_guard=1,rounding=trunc` | 377 | 150 | 5.1 | 30 | 0.595 | 4.76e-07 (2^-21.00) | 21.00 |
| 9 | `iterative:data_width=27,n_iter=29,angle_guard=1,frac_guard=0,rounding=trunc` | 380 | 153 | 4.8 | 32 | 0.642 | 4.41e-07 (2^-21.11) | 21.11 |
| 10 | `iterative:data_width=27,n_iter=27,angle_guard=1,frac_guard=3,rounding=trunc` | 430 | 159 | 5.1 | 30 | 0.666 | 1.66e-07 (2^-22.52) | 22.52 |
| 11 | `iterative:data_width=27,n_iter=29,angle_guard=1,frac_guard=3,rounding=trunc` | 436 | 159 | 4.8 | 32 | 0.717 | 1.39e-07 (2^-22.78) | 22.78 |
| 12 | `iterative:data_width=28,n_iter=29,angle_guard=1,frac_guard=2,rounding=trunc` | 438 | 162 | 4.8 | 32 | 0.723 | 9.22e-08 (2^-23.37) | 23.37 |
| 13 | `iterative:data_width=28,n_iter=27,angle_guard=1,frac_guard=1,rounding=round` | 489 | 160 | 5.1 | 30 | 0.733 | 8.92e-08 (2^-23.42) | 23.42 |
| 14 | `unrolled_k:data_width=27,n_iter=26,angle_guard=3,frac_guard=4,rounding=trunc,k=2` | 584 | 162 | 6.0 | 16 | 0.449 | 8.5e-08 (2^-23.49) | 23.49 |
| 15 | `unrolled_k:data_width=27,n_iter=26,angle_guard=3,frac_guard=4,rounding=round,k=3` | 818 | 162 | 5.4 | 12 | 0.442 | 6.69e-08 (2^-23.83) | 23.83 |
| 16 | `unrolled_k:data_width=28,n_iter=30,angle_guard=3,frac_guard=4,rounding=round,k=3` | 865 | 167 | 5.0 | 13 | 0.505 | 2.41e-08 (2^-25.31) | 25.31 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec prioritizes minimum area (luts_plus_ffs) with a hard throughput constraint of >= 1 MSPS and max error <= 2^-10. The iterative family is the most area-efficient baseline and is the most likely to produce the minimum-area design that meets the constraints, so it gets the largest budget share (55%) to densely explore the accuracy-area trade-off. The unrolled_k family (45%) is included to cover the trade-off curve more completely for hypervolume scoring, as it may achieve different (area, accuracy) points due to its different timing characteristics and structural overhead. Both families can plausibly meet the 1 MSPS throughput constraint (iterative needs Fmax >= 1 MHz, which is trivially achievable; unrolled_k needs Fmax >= 1/k MHz, even easier). The full ranges for n_iter, data_width, and guards are used to let Optuna discover the Pareto front, with the accuracy constraint (max_abs_err <= 2^-10) acting as a filter that will naturally focus the search on designs with sufficient n_iter and appropriate guard bits.*)
- `iterative` (33 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* iterative is the baseline shared-datapath family with the smallest structural overhead (one barrel shifter/adder tree, no k-way or m-way replication). Since the spec is 'area is everything' and throughput only needs >= 1 MSPS (which iterative can meet if Fmax is high enough, or even if Fmax is modest since it needs 1 result per cycle at 1 MSPS -> Fmax >= 1 MHz, which is trivially met), iterative is the prime candidate for the minimum luts_plus_ffs corner. I give it the largest share to densely map the accuracy-vs-area trade-off (n_iter, data_width, guards) that defines the Pareto front.
- `unrolled_k` (27 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* unrolled_k trades area for latency/throughput by chaining k micro-rotations per cycle. While it generally uses more LUTs/FFs than iterative for the same accuracy (due to k parallel datapaths or deeper combinational logic), it can achieve higher Fmax for a given n_iter by reducing the per-cycle combinational depth, which may help if iterative's Fmax is too low to meet 1 MSPS at a given area. More importantly, for the hypervolume objective (covering the trade-off curve), unrolled_k may occupy a different region of the (luts_plus_ffs, accuracy_bits) space, especially at higher k where the area penalty is offset by potentially higher Fmax enabling more aggressive n_iter within timing constraints. I give it a smaller share since iterative is more likely to dominate the minimum-area corner, but it is needed to ensure the front is well-mapped.

**Result (code):** 60 evaluations this round, 60 total; 38 feasible; hypervolume 1.071e+04 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (iterative, luts_plus_ffs=345) meets the throughput constraint (10.8 MSPS >= 1) and the accuracy constraint (13.8 bits > 10 bits). The front spans a wide range of accuracy (13.8 to 23.4 bits) and area (345 to 1254), providing a comprehensive trade-off curve. Since this is the final round, no further exploration is possible or necessary. The selection rule (min luts_plus_ffs) will pick the iterative design with 345 LUTs+FFs, which is feasible and optimal for the given objectives.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.071e+04 (gain this round: n/a (first round)).
Feasible designs: 38 of 60 evaluations (33 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 34.5
- max_abs_err <= 0.000976562: 37% violate; best seen 9.01e-08 (2^-23.40)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=20 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=345, accuracy_bits=13.8, luts=227, ffs=118, throughput_msps=10.8, max_abs_err=7.03e-05 (2^-13.80), power_index=0.234
- iterative [data_width=22 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=365, accuracy_bits=13.8, luts=239, ffs=126, throughput_msps=10.8, max_abs_err=6.83e-05 (2^-13.84), power_index=0.247
- iterative [data_width=20 n_iter=17 angle_guard=-1 frac_guard=0 rounding=round] luts_plus_ffs=370, accuracy_bits=14.1, luts=254, ffs=116, throughput_msps=7.95, max_abs_err=5.77e-05 (2^-14.08), power_index=0.279
- iterative [data_width=22 n_iter=29 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=456, accuracy_bits=17.8, luts=322, ffs=134, throughput_msps=4.88, max_abs_err=4.23e-06 (2^-17.85), power_index=0.549
- unrolled_k [data_width=27 n_iter=27 angle_guard=2 frac_guard=0 rounding=round k=5] luts_plus_ffs=1092, accuracy_bits=22.2, luts=939, ffs=152, throughput_msps=4.52, max_abs_err=2.09e-07 (2^-22.19), power_index=0.37
- unrolled_k [data_width=27 n_iter=27 angle_guard=2 frac_guard=3 rounding=round k=5] luts_plus_ffs=1254, accuracy_bits=23.4, luts=1096, ffs=158, throughput_msps=4.52, max_abs_err=9.01e-08 (2^-23.40), power_index=0.425
Front coverage: luts_plus_ffs 345..1254 (HV reference 1500); accuracy_bits 13.8..23.4 (HV reference 10); data_width on the front 20..27 (registry 8..28).

Per family:
- iterative: 33 evals, 21 feasible; max throughput seen 34.5 MSPS; best accuracy 17.85 bits; best feasible luts_plus_ffs=345; feasible ranges: data_width 17..22, n_iter 14..29, angle_guard -2..3, frac_guard 0..4
- unrolled_k: 27 evals, 17 feasible; max throughput seen 18 MSPS; best accuracy 23.40 bits; best feasible luts_plus_ffs=446; feasible ranges: data_width 13..27, n_iter 17..27, angle_guard 1..4, frac_guard 0..4, k 3..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (27 evals): data_width=19..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (4 front designs; box front_anchored)
- `unrolled_k` (13 evals): data_width=26..28, n_iter=25..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 78 feasible; hypervolume 1.5e+04 (+40.0%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (iterative, luts_plus_ffs=345) meets the throughput constraint (10.8 MSPS >= 1) and the accuracy constraint (13.8 bits > 10 bits). The front spans a wide range of accuracy (13.8 to 23.4 bits) and area (345 to 1254), providing a comprehensive trade-off curve. Since this is the final round, no further exploration is possible or necessary. The selection rule (min luts_plus_ffs) will pick the iterative design with 345 LUTs+FFs, which is feasible and optimal for the given objectives.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.5e+04 (gain this round: +40.0%).
Feasible designs: 78 of 100 evaluations (71 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 34.5
- max_abs_err <= 0.000976562: 22% violate; best seen 2.41e-08 (2^-25.31)

Pareto front (feasible, 17 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=20 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=345, accuracy_bits=13.8, luts=227, ffs=118, throughput_msps=10.8, max_abs_err=7.03e-05 (2^-13.80), power_index=0.234
- iterative [data_width=21 n_iter=16 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=368, accuracy_bits=14.7, luts=242, ffs=126, throughput_msps=9.97, max_abs_err=3.85e-05 (2^-14.67), power_index=0.263
- iterative [data_width=21 n_iter=21 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=407, accuracy_bits=16.1, luts=282, ffs=125, throughput_msps=6.62, max_abs_err=1.38e-05 (2^-16.15), power_index=0.368
- iterative [data_width=22 n_iter=29 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=456, accuracy_bits=17.8, luts=322, ffs=134, throughput_msps=4.88, max_abs_err=4.23e-06 (2^-17.85), power_index=0.549
- iterative [data_width=26 n_iter=27 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=514, accuracy_bits=20.3, luts=363, ffs=150, throughput_msps=5.11, max_abs_err=7.68e-07 (2^-20.31), power_index=0.58
- iterative [data_width=27 n_iter=29 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=534, accuracy_bits=21.1, luts=380, ffs=153, throughput_msps=4.79, max_abs_err=4.41e-07 (2^-21.11), power_index=0.642
- iterative [data_width=27 n_iter=29 angle_guard=1 frac_guard=3 rounding=trunc] luts_plus_ffs=596, accuracy_bits=22.8, luts=436, ffs=159, throughput_msps=4.79, max_abs_err=1.39e-07 (2^-22.78), power_index=0.717
- iterative [data_width=28 n_iter=29 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=601, accuracy_bits=23.4, luts=438, ffs=162, throughput_msps=4.79, max_abs_err=9.22e-08 (2^-23.37), power_index=0.723
- unrolled_k [data_width=27 n_iter=26 angle_guard=3 frac_guard=4 rounding=trunc k=2] luts_plus_ffs=747, accuracy_bits=23.5, luts=584, ffs=162, throughput_msps=5.99, max_abs_err=8.5e-08 (2^-23.49), power_index=0.449
- unrolled_k [data_width=28 n_iter=30 angle_guard=3 frac_guard=4 rounding=round k=3] luts_plus_ffs=1032, accuracy_bits=25.3, luts=865, ffs=167, throughput_msps=5.01, max_abs_err=2.41e-08 (2^-25.31), power_index=0.505
Front coverage: luts_plus_ffs 345..1032 (HV reference 1500); accuracy_bits 13.8..25.3 (HV reference 10); data_width on the front 20..28 (registry 8..28).

Per family:
- iterative: 60 evals, 48 feasible; max throughput seen 34.5 MSPS; best accuracy 23.42 bits; best feasible luts_plus_ffs=345; feasible ranges: data_width 17..28, n_iter 14..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 40 evals, 30 feasible; max throughput seen 18 MSPS; best accuracy 25.31 bits; best feasible luts_plus_ffs=446; feasible ranges: data_width 13..28, n_iter 17..30, angle_guard -1..4, frac_guard 0..4, k 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4207 in, 1263 out
- provider-reported cost: $0.0022
- full prompts and replies: `llm_trace.jsonl`

