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
`iterative:data_width=14,n_iter=12,angle_guard=2,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 161 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 92 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 13.2 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 15 | exact: schedule |
| latency_ns | 75.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.143 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000894 (2^-10.13) | exact: bit-accurate model, exhaustive (16384 angles) |
| max_abs_err_lsb | 3.66 | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err | 0.000262 (2^-11.90) | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err_lsb | 1.07 | exact: bit-accurate model, exhaustive (16384 angles) |
| accuracy_bits | 10.1 | exact: bit-accurate model, exhaustive (16384 angles) |

## Pareto front (23 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=14,n_iter=12,angle_guard=2,frac_guard=2,rounding=trunc` | 161 | 92 | 13.2 | 15 | 0.143 | 0.000894 (2^-10.13) | 10.13 |
| 1 | `iterative:data_width=15,n_iter=13,angle_guard=0,frac_guard=0,rounding=round` | 166 | 91 | 12.4 | 16 | 0.155 | 0.000879 (2^-10.15) | 10.15 |
| 2 | `iterative:data_width=15,n_iter=12,angle_guard=2,frac_guard=1,rounding=trunc` | 163 | 95 | 13.2 | 15 | 0.145 | 0.000811 (2^-10.27) | 10.27 |
| 3 | `iterative:data_width=15,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 170 | 93 | 11.7 | 17 | 0.168 | 0.000599 (2^-10.71) | 10.71 |
| 4 | `iterative:data_width=15,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc` | 170 | 94 | 11.7 | 17 | 0.169 | 0.000594 (2^-10.72) | 10.72 |
| 5 | `iterative:data_width=15,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc` | 172 | 95 | 11.7 | 17 | 0.171 | 0.000567 (2^-10.78) | 10.78 |
| 6 | `iterative:data_width=15,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc` | 180 | 96 | 11.0 | 18 | 0.187 | 0.000393 (2^-11.31) | 11.31 |
| 7 | `iterative:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 204 | 108 | 11.4 | 17 | 0.2 | 0.00017 (2^-12.53) | 12.53 |
| 8 | `iterative:data_width=18,n_iter=14,angle_guard=4,frac_guard=1,rounding=trunc` | 210 | 112 | 11.4 | 17 | 0.206 | 0.000166 (2^-12.55) | 12.55 |
| 9 | `iterative:data_width=19,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 216 | 113 | 10.8 | 18 | 0.222 | 8.33e-05 (2^-13.55) | 13.55 |
| 10 | `iterative:data_width=19,n_iter=15,angle_guard=4,frac_guard=2,rounding=trunc` | 231 | 119 | 10.5 | 18 | 0.237 | 7.72e-05 (2^-13.66) | 13.66 |
| 11 | `iterative:data_width=19,n_iter=28,angle_guard=4,frac_guard=0,rounding=round` | 252 | 116 | 5.0 | 31 | 0.429 | 3.74e-05 (2^-14.71) | 14.71 |
| 12 | `iterative:data_width=19,n_iter=28,angle_guard=1,frac_guard=4,rounding=trunc` | 296 | 121 | 5.0 | 31 | 0.486 | 3.21e-05 (2^-14.93) | 14.93 |
| 13 | `iterative:data_width=22,n_iter=26,angle_guard=4,frac_guard=0,rounding=round` | 304 | 131 | 5.4 | 29 | 0.475 | 5.23e-06 (2^-17.54) | 17.54 |
| 14 | `iterative:data_width=22,n_iter=28,angle_guard=4,frac_guard=0,rounding=round` | 304 | 131 | 5.0 | 31 | 0.508 | 5.23e-06 (2^-17.54) | 17.54 |
| 15 | `iterative:data_width=23,n_iter=28,angle_guard=4,frac_guard=0,rounding=round` | 323 | 136 | 4.9 | 31 | 0.536 | 2.9e-06 (2^-18.39) | 18.39 |
| 16 | `iterative:data_width=23,n_iter=26,angle_guard=4,frac_guard=2,rounding=trunc` | 343 | 140 | 5.3 | 29 | 0.527 | 1.81e-06 (2^-19.08) | 19.08 |
| 17 | `iterative:data_width=23,n_iter=23,angle_guard=2,frac_guard=3,rounding=trunc` | 350 | 140 | 6.0 | 26 | 0.48 | 1.53e-06 (2^-19.32) | 19.32 |
| 18 | `iterative:data_width=23,n_iter=28,angle_guard=4,frac_guard=3,rounding=trunc` | 360 | 142 | 4.9 | 31 | 0.585 | 1.19e-06 (2^-19.69) | 19.69 |
| 19 | `iterative:data_width=23,n_iter=28,angle_guard=4,frac_guard=4,rounding=trunc` | 377 | 144 | 4.9 | 31 | 0.608 | 8.73e-07 (2^-20.13) | 20.13 |
| 20 | `iterative:data_width=23,n_iter=26,angle_guard=4,frac_guard=3,rounding=round` | 423 | 142 | 5.3 | 29 | 0.617 | 5.73e-07 (2^-20.73) | 20.73 |
| 21 | `iterative:data_width=24,n_iter=28,angle_guard=4,frac_guard=3,rounding=round` | 444 | 147 | 4.9 | 31 | 0.69 | 3.54e-07 (2^-21.43) | 21.43 |
| 22 | `iterative:data_width=28,n_iter=28,angle_guard=-1,frac_guard=3,rounding=round` | 520 | 162 | 4.9 | 31 | 0.796 | 2.49e-07 (2^-21.94) | 21.94 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts are decisive: iterative dominates on area (253 vs 350 for unrolled_k, 1332 for pipelined) and supplies 13 of 15 front points, so I concentrate the entire remaining budget on iterative and drop unrolled_k. The spec's binding constraints are throughput >= 1 MSPS and max_abs_err <= 2^-10; iterative meets these only in a narrow window where Fmax is high and N/W are small, so I focus the search there rather than re-sweeping the wide ranges already covered. I keep the ranges tight (W 12..16, N 10..16, angle_guard -2..2, frac_guard 0..2) to let Optuna resolve the area-vs-accuracy_bits trade-off near the front instead of wasting evals on obviously-too-large or obviously-inaccurate corners. The single objective pair (min luts_plus_ffs, max accuracy_bits) is well covered by this focused box, and the reserved front-mapping pass will then trace the curve over these ranges. I do not claim any specific LUT/FF/Fmax numbers; I am only choosing where to spend evaluations based on the reported bests and front composition.*)
- `iterative` (100 evals): data_width=12..16, n_iter=10..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the clear area winner (best 253 vs 350 for unrolled_k, 13/15 front points). It is the only family that can plausibly hit throughput >= 1 MSPS at low area, since its 1-result-per-(N+3)-cycles schedule only works when Fmax is high enough. I narrow data_width to 12..16 and n_iter to 10..16 because the error bound 2^-10 forces a modest W and N, and larger values only inflate area without buying accuracy_bits beyond the ~10-11 the spec rewards. angle_guard -2..2 and frac_guard 0..2 keep the angle/atan path and datapath tight (area is the objective) while still allowing the accuracy knobs to be explored. Both rounding modes are kept since rounding can shift max_abs_err across the 2^-10 boundary and affect accuracy_bits at near-equal area.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 49 feasible; hypervolume 2972 (n/a).

**LLM decision:** `add_family` — The current front is dominated by the `iterative` family, which suffers from high latency (N+3 cycles) and lower throughput compared to pipelined architectures. While `iterative` achieves the minimum area (253 LUTs+FFs), it is not the only feasible option. The spec requires >= 1 MSPS, which `iterative` meets easily (13.2 MSPS), but `pipelined` or `unrolled_k` families might offer better trade-offs in accuracy vs. area or allow for higher data widths within the same area budget due to different resource sharing characteristics. Specifically, `unrolled_k` with k>1 can reduce latency and potentially improve throughput while maintaining similar area to iterative if N is kept low, or `pipelined` might allow for higher n_iter (better accuracy) within the same area budget if the per-stage cost is lower. However, looking at the registry, `pipelined` has 1 result/cycle and N+2 latency. Given the area constraint is the primary objective, and `iterative` is already very efficient, exploring `unrolled_k` is a good next step to see if we can get better accuracy for the same area or lower area for the same accuracy by unrolling. Also, the current front only covers data_width 14-16. Exploring other families might reveal designs with data_width > 16 that are still feasible and offer higher accuracy bits, expanding the hypervolume. The `unrolled_k` family is a natural extension of `iterative` with a parameter `k` that can optimize the trade-off between latency/throughput and area. Let's add `unrolled_k` to the exploration.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 2972 (gain this round: n/a (first round)).
Feasible designs: 49 of 100 evaluations (35 unique).
Families explored so far: iterative. Not yet explored: unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 51% violate; best seen 0.000176 (2^-12.48)

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=253, accuracy_bits=10.1, luts=161, ffs=92, throughput_msps=13.2, max_abs_err=0.000894 (2^-10.13), power_index=0.143
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.2, luts=166, ffs=91, throughput_msps=12.4, max_abs_err=0.000879 (2^-10.15), power_index=0.155
- iterative [data_width=15 n_iter=12 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=258, accuracy_bits=10.3, luts=163, ffs=95, throughput_msps=13.2, max_abs_err=0.000811 (2^-10.27), power_index=0.145
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.6, luts=170, ffs=93, throughput_msps=12.4, max_abs_err=0.000642 (2^-10.61), power_index=0.158
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=264, accuracy_bits=10.7, luts=170, ffs=94, throughput_msps=11.7, max_abs_err=0.000594 (2^-10.72), power_index=0.169
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=267, accuracy_bits=10.8, luts=172, ffs=95, throughput_msps=11.7, max_abs_err=0.000567 (2^-10.78), power_index=0.171
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=275, accuracy_bits=11.3, luts=180, ffs=96, throughput_msps=11, max_abs_err=0.000393 (2^-11.31), power_index=0.187
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=336, accuracy_bits=12.5, luts=234, ffs=102, throughput_msps=11, max_abs_err=0.000176 (2^-12.48), power_index=0.228
Front coverage: luts_plus_ffs 253..336 (HV reference 1500); accuracy_bits 10.1..12.5 (HV reference 10); data_width on the front 14..16 (registry 8..28).

Per family:
- iterative: 100 evals, 49 feasible; max throughput seen 15.6 MSPS; best accuracy 12.48 bits; best feasible luts_plus_ffs=253; feasible ranges: data_width 13..16, n_iter 12..16, angle_guard -1..2, frac_guard 0..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Adding unrolled_k to explore if it can beat iterative on the Pareto front, particularly in terms of accuracy for a given area or area for a given accuracy. The ranges are chosen to be slightly wider than the current iterative front to allow for discovery of new trade-offs.*)
- `unrolled_k` (20 evals): data_width=12..18, n_iter=10..18, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, k=2..4. *Why:* Explore unrolled_k to find potentially better area/accuracy trade-offs than iterative, especially with k>1 which can reduce latency and might allow for different resource utilization. Focus on data_width 12-18 and n_iter 10-18 to cover the region around the current front and slightly beyond.

**Result (code):** 20 evaluations this round, 120 total; 64 feasible; hypervolume 3689 (+24.1%).

**LLM decision:** `stop` — The Pareto front is well-mapped and satisfies all constraints. The minimum area design (iterative, 253 LUTs+FFs) meets the throughput constraint (13.2 MSPS >= 1 MSPS) and the accuracy constraint (10.1 bits >= 10 bits). The front extends to 13.2 bits accuracy, providing a good trade-off curve. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (253) as per the selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 3689 (gain this round: +24.1%).
Feasible designs: 64 of 120 evaluations (50 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 47% violate; best seen 0.000109 (2^-13.16)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=253, accuracy_bits=10.1, luts=161, ffs=92, throughput_msps=13.2, max_abs_err=0.000894 (2^-10.13), power_index=0.143
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.2, luts=166, ffs=91, throughput_msps=12.4, max_abs_err=0.000879 (2^-10.15), power_index=0.155
- iterative [data_width=15 n_iter=12 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=258, accuracy_bits=10.3, luts=163, ffs=95, throughput_msps=13.2, max_abs_err=0.000811 (2^-10.27), power_index=0.145
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.6, luts=170, ffs=93, throughput_msps=12.4, max_abs_err=0.000642 (2^-10.61), power_index=0.158
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=264, accuracy_bits=10.7, luts=170, ffs=94, throughput_msps=11.7, max_abs_err=0.000594 (2^-10.72), power_index=0.169
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=267, accuracy_bits=10.8, luts=172, ffs=95, throughput_msps=11.7, max_abs_err=0.000567 (2^-10.78), power_index=0.171
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=275, accuracy_bits=11.3, luts=180, ffs=96, throughput_msps=11, max_abs_err=0.000393 (2^-11.31), power_index=0.187
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=336, accuracy_bits=12.5, luts=234, ffs=102, throughput_msps=11, max_abs_err=0.000176 (2^-12.48), power_index=0.228
- unrolled_k [data_width=17 n_iter=16 angle_guard=1 frac_guard=2 rounding=round k=2] luts_plus_ffs=449, accuracy_bits=13.2, luts=344, ffs=105, throughput_msps=9.35, max_abs_err=0.000109 (2^-13.16), power_index=0.186
Front coverage: luts_plus_ffs 253..449 (HV reference 1500); accuracy_bits 10.1..13.2 (HV reference 10); data_width on the front 14..17 (registry 8..28).

Per family:
- iterative: 100 evals, 49 feasible; max throughput seen 15.6 MSPS; best accuracy 12.48 bits; best feasible luts_plus_ffs=253; feasible ranges: data_width 13..16, n_iter 12..16, angle_guard -1..2, frac_guard 0..2
- unrolled_k: 20 evals, 15 feasible; max throughput seen 12 MSPS; best accuracy 13.16 bits; best feasible luts_plus_ffs=350; feasible ranges: data_width 15..18, n_iter 13..18, angle_guard -1..2, frac_guard 1..3, k 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `iterative` (72 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (8 front designs; box front_anchored)
- `unrolled_k` (8 evals): data_width=16..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (1 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 133 feasible; hypervolume 1.283e+04 (+247.9%).

**No LLM call** (code's front-mapping round): The Pareto front is well-mapped and satisfies all constraints. The minimum area design (iterative, 253 LUTs+FFs) meets the throughput constraint (13.2 MSPS >= 1 MSPS) and the accuracy constraint (10.1 bits >= 10 bits). The front extends to 13.2 bits accuracy, providing a good trade-off curve. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (253) as per the selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.283e+04 (gain this round: +247.9%).
Feasible designs: 133 of 200 evaluations (113 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 34% violate; best seen 2.49e-07 (2^-21.94)

Pareto front (feasible, 23 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=253, accuracy_bits=10.1, luts=161, ffs=92, throughput_msps=13.2, max_abs_err=0.000894 (2^-10.13), power_index=0.143
- iterative [data_width=15 n_iter=12 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=258, accuracy_bits=10.3, luts=163, ffs=95, throughput_msps=13.2, max_abs_err=0.000811 (2^-10.27), power_index=0.145
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=267, accuracy_bits=10.8, luts=172, ffs=95, throughput_msps=11.7, max_abs_err=0.000567 (2^-10.78), power_index=0.171
- iterative [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=312, accuracy_bits=12.5, luts=204, ffs=108, throughput_msps=11.4, max_abs_err=0.00017 (2^-12.53), power_index=0.2
- iterative [data_width=19 n_iter=15 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=350, accuracy_bits=13.7, luts=231, ffs=119, throughput_msps=10.5, max_abs_err=7.72e-05 (2^-13.66), power_index=0.237
- iterative [data_width=19 n_iter=28 angle_guard=1 frac_guard=4 rounding=trunc] luts_plus_ffs=417, accuracy_bits=14.9, luts=296, ffs=121, throughput_msps=5.03, max_abs_err=3.21e-05 (2^-14.93), power_index=0.486
- iterative [data_width=23 n_iter=28 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=460, accuracy_bits=18.4, luts=323, ffs=136, throughput_msps=4.94, max_abs_err=2.9e-06 (2^-18.39), power_index=0.536
- iterative [data_width=23 n_iter=23 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=490, accuracy_bits=19.3, luts=350, ffs=140, throughput_msps=6, max_abs_err=1.53e-06 (2^-19.32), power_index=0.48
- iterative [data_width=23 n_iter=26 angle_guard=4 frac_guard=3 rounding=round] luts_plus_ffs=566, accuracy_bits=20.7, luts=423, ffs=142, throughput_msps=5.28, max_abs_err=5.73e-07 (2^-20.73), power_index=0.617
- iterative [data_width=28 n_iter=28 angle_guard=-1 frac_guard=3 rounding=round] luts_plus_ffs=682, accuracy_bits=21.9, luts=520, ffs=162, throughput_msps=4.86, max_abs_err=2.49e-07 (2^-21.94), power_index=0.796
Front coverage: luts_plus_ffs 253..682 (HV reference 1500); accuracy_bits 10.1..21.9 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 172 evals, 110 feasible; max throughput seen 15.6 MSPS; best accuracy 21.94 bits; best feasible luts_plus_ffs=253; feasible ranges: data_width 13..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 28 evals, 23 feasible; max throughput seen 12 MSPS; best accuracy 19.86 bits; best feasible luts_plus_ffs=350; feasible ranges: data_width 15..28, n_iter 13..21, angle_guard -1..4, frac_guard 0..3, k 2..8
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7308 in, 1710 out
- provider-reported cost: $0.0054
- full prompts and replies: `llm_trace.jsonl`

