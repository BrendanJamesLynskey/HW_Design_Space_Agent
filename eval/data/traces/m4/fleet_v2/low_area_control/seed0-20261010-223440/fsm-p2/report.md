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
`iterative:data_width=15,n_iter=12,angle_guard=2,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 161 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 93 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 13.2 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 15 | exact: schedule |
| latency_ns | 75.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.143 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000835 (2^-10.23) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.84 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00024 (2^-12.02) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.97 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.2 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (28 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=12,angle_guard=2,frac_guard=0,rounding=round` | 161 | 93 | 13.2 | 15 | 0.143 | 0.000835 (2^-10.23) | 10.23 |
| 1 | `iterative:data_width=14,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc` | 170 | 92 | 12.4 | 16 | 0.158 | 0.000746 (2^-10.39) | 10.39 |
| 2 | `iterative:data_width=15,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 170 | 93 | 11.7 | 17 | 0.168 | 0.000599 (2^-10.71) | 10.71 |
| 3 | `iterative:data_width=15,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 170 | 93 | 11.0 | 18 | 0.178 | 0.000599 (2^-10.71) | 10.71 |
| 4 | `iterative:data_width=16,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 179 | 97 | 10.4 | 19 | 0.197 | 0.000301 (2^-11.70) | 11.70 |
| 5 | `iterative:data_width=16,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 193 | 102 | 10.4 | 19 | 0.211 | 0.000219 (2^-12.16) | 12.16 |
| 6 | `iterative:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` | 225 | 100 | 11.7 | 17 | 0.207 | 0.000209 (2^-12.22) | 12.22 |
| 7 | `iterative:data_width=19,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 216 | 113 | 11.4 | 17 | 0.21 | 0.000142 (2^-12.78) | 12.78 |
| 8 | `iterative:data_width=21,n_iter=15,angle_guard=-2,frac_guard=0,rounding=trunc` | 224 | 119 | 10.8 | 18 | 0.232 | 9.21e-05 (2^-13.41) | 13.41 |
| 9 | `iterative:data_width=20,n_iter=15,angle_guard=4,frac_guard=0,rounding=trunc` | 223 | 120 | 10.5 | 18 | 0.232 | 8.43e-05 (2^-13.53) | 13.53 |
| 10 | `iterative:data_width=21,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 238 | 123 | 10.5 | 18 | 0.245 | 6.66e-05 (2^-13.87) | 13.87 |
| 11 | `iterative:data_width=22,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 246 | 126 | 10.2 | 19 | 0.266 | 3.59e-05 (2^-14.77) | 14.77 |
| 12 | `iterative:data_width=21,n_iter=26,angle_guard=0,frac_guard=0,rounding=trunc` | 265 | 122 | 5.5 | 29 | 0.422 | 3.02e-05 (2^-15.02) | 15.02 |
| 13 | `iterative:data_width=22,n_iter=19,angle_guard=4,frac_guard=0,rounding=trunc` | 283 | 131 | 7.1 | 22 | 0.343 | 1.32e-05 (2^-16.21) | 16.21 |
| 14 | `iterative:data_width=22,n_iter=19,angle_guard=2,frac_guard=0,rounding=round` | 292 | 129 | 7.1 | 22 | 0.348 | 8.18e-06 (2^-16.90) | 16.90 |
| 15 | `iterative:data_width=22,n_iter=22,angle_guard=2,frac_guard=0,rounding=round` | 299 | 129 | 6.2 | 25 | 0.403 | 5.49e-06 (2^-17.47) | 17.47 |
| 16 | `iterative:data_width=24,n_iter=20,angle_guard=4,frac_guard=0,rounding=trunc` | 315 | 141 | 6.7 | 23 | 0.395 | 3.91e-06 (2^-17.96) | 17.96 |
| 17 | `iterative:data_width=25,n_iter=27,angle_guard=-2,frac_guard=0,rounding=trunc` | 335 | 140 | 5.2 | 30 | 0.537 | 3.72e-06 (2^-18.04) | 18.04 |
| 18 | `iterative:data_width=24,n_iter=26,angle_guard=3,frac_guard=1,rounding=trunc` | 343 | 142 | 5.3 | 29 | 0.529 | 1.76e-06 (2^-19.11) | 19.11 |
| 19 | `iterative:data_width=25,n_iter=26,angle_guard=1,frac_guard=2,rounding=trunc` | 375 | 147 | 5.3 | 29 | 0.57 | 6.67e-07 (2^-20.52) | 20.52 |
| 20 | `iterative:data_width=25,n_iter=28,angle_guard=2,frac_guard=3,rounding=trunc` | 394 | 150 | 4.9 | 31 | 0.635 | 3.7e-07 (2^-21.37) | 21.37 |
| 21 | `iterative:data_width=25,n_iter=28,angle_guard=3,frac_guard=3,rounding=trunc` | 396 | 151 | 4.9 | 31 | 0.638 | 2.97e-07 (2^-21.68) | 21.68 |
| 22 | `iterative:data_width=27,n_iter=26,angle_guard=0,frac_guard=2,rounding=trunc` | 411 | 156 | 5.3 | 29 | 0.619 | 2.81e-07 (2^-21.76) | 21.76 |
| 23 | `iterative:data_width=27,n_iter=26,angle_guard=1,frac_guard=2,rounding=trunc` | 413 | 157 | 5.3 | 29 | 0.622 | 1.72e-07 (2^-22.47) | 22.47 |
| 24 | `iterative:data_width=28,n_iter=28,angle_guard=2,frac_guard=2,rounding=trunc` | 434 | 163 | 4.9 | 31 | 0.697 | 7.27e-08 (2^-23.71) | 23.71 |
| 25 | `iterative:data_width=28,n_iter=28,angle_guard=3,frac_guard=3,rounding=trunc` | 453 | 166 | 4.9 | 31 | 0.722 | 4.18e-08 (2^-24.51) | 24.51 |
| 26 | `iterative:data_width=28,n_iter=28,angle_guard=3,frac_guard=3,rounding=round` | 527 | 166 | 4.9 | 31 | 0.809 | 3.07e-08 (2^-24.96) | 24.96 |
| 27 | `iterative:data_width=28,n_iter=30,angle_guard=3,frac_guard=3,rounding=round` | 536 | 166 | 4.6 | 33 | 0.872 | 2.91e-08 (2^-25.04) | 25.04 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show that iterative is the clear winner for area (280 vs 408 for unrolled_k, and >800 for pipelined families). Since the spec prioritizes minimizing luts_plus_ffs and iterative already dominates the merged front, the goal is to refine the Pareto front in the low-area, high-accuracy region. I am narrowing the search space for both iterative and unrolled_k to the specific parameter ranges (data_width 12-16, n_iter 12-16) where the max_abs_err constraint (<= 2^-10) is likely just satisfied. This focuses the remaining budget on mapping the precise trade-off curve between area and accuracy_bits in the feasible region, rather than exploring infeasible or dominated areas. I allocate 60% to iterative to densely sample the dominant family and 40% to unrolled_k to check if it offers any non-dominated points in the accuracy dimension.*)
- `iterative` (60 evals): data_width=12..16, n_iter=12..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the only family currently on the merged front (20/20 designs) and has the best feasible area (280). The previous 64 evals likely covered a broad space; I am now narrowing to the region where area is minimal while still meeting max_abs_err <= 2^-10. Since accuracy depends on n_iter and guards, and area scales with data_width and n_iter, I focus on the lower end of data_width (12-16) and n_iter (12-16) where the error constraint is just met. I include both rounding modes and a tight range on guards to find the exact minimum area point and map the local trade-off between accuracy_bits and luts_plus_ffs.
- `unrolled_k` (40 evals): data_width=12..16, n_iter=12..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..2. *Why:* unrolled_k has a best feasible area of 408, which is worse than iterative's 280, and 0 of its designs are on the merged front. However, it might offer a different trade-off shape (e.g., slightly higher area for significantly higher accuracy_bits) that could improve hypervolume if it extends the front in the accuracy direction. I restrict k=2 to keep area low (higher k increases area) and focus on the same low data_width/n_iter region to see if it can beat iterative on accuracy at a comparable area cost. If it cannot, the budget is spent confirming it is dominated.

**Result (code):** 100 evaluations this round, 100 total; 61 feasible; hypervolume 2677 (n/a).

**LLM decision:** `refine` — The current Pareto front is dominated by the `iterative` family, with the best area (262 LUTs+FFs) and a reasonable accuracy range (10.4-12.2 bits). The `unrolled_k` family performed poorly in this round (best area 344), likely because the search space was too broad or the specific `k` values didn't yield better area/accuracy trade-offs than the iterative baseline for this specific low-area constraint. The `pipelined` and `pipelined_m` families have not been explored yet. Given the strict area constraint (minimize LUTs+FFs) and the throughput requirement (>= 1 MSPS, which is easily met by iterative at ~12 MSPS), it is crucial to explore the pipelined families to see if they can offer a better area/accuracy trade-off or if they are strictly worse in area. However, since the `iterative` family has already found a very good low-area point (262), and `unrolled_k` was worse, the most efficient next step is to refine the search around the promising `iterative` region to ensure we have the absolute best low-area point, while also introducing `pipelined` to check if it can beat 262. But wait, the prompt asks for a single decision. Let's look at the options. `add_family` is a strong candidate because `pipelined` is unexplored. `refine` is also strong. Let's look at the budget. 100 evals left. If I `add_family` `pipelined`, I can search it. If I `refine` `iterative`, I might find a slightly better point. The current best is 262. The HV reference is 1500. The front is quite tight in area (262-333). To maximize hypervolume, I need to cover the trade-off curve. The accuracy range on the front is 10.4-12.2. The constraint is max_abs_err <= 2^-10 (approx 10 bits). So 10.4 is just barely feasible. I should try to push accuracy higher while keeping area low, or find if pipelined allows lower area for the same accuracy. Let's add `pipelined` to see if it offers a different trade-off. Actually, `pipelined` usually has higher area due to registers. `iterative` is often the most area-efficient. The fact that `unrolled_k` was worse suggests that adding complexity doesn't help area here. I will refine the `iterative` family to squeeze out the best possible area/accuracy points, as it is the clear winner so far. I will narrow the ranges to focus on the best-performing region: data_width 14-16, n_iter 12-16, angle_guard 1-2, frac_guard 0-2. This will allow the optimizer to focus on the most promising sub-space.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 2677 (gain this round: n/a (first round)).
Feasible designs: 61 of 100 evaluations (42 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 13.5
- max_abs_err <= 0.000976562: 39% violate; best seen 0.000214 (2^-12.19)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=262, accuracy_bits=10.4, luts=170, ffs=92, throughput_msps=12.4, max_abs_err=0.000746 (2^-10.39), power_index=0.158
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.7, luts=170, ffs=93, throughput_msps=11.7, max_abs_err=0.000599 (2^-10.71), power_index=0.168
- iterative [data_width=16 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.7, luts=179, ffs=97, throughput_msps=10.4, max_abs_err=0.000301 (2^-11.70), power_index=0.197
- iterative [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=295, accuracy_bits=12.2, luts=193, ffs=102, throughput_msps=10.4, max_abs_err=0.000219 (2^-12.16), power_index=0.211
- iterative [data_width=16 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=333, accuracy_bits=12.2, luts=232, ffs=101, throughput_msps=10.4, max_abs_err=0.000214 (2^-12.19), power_index=0.238
Front coverage: luts_plus_ffs 262..333 (HV reference 1500); accuracy_bits 10.4..12.2 (HV reference 10); data_width on the front 14..16 (registry 8..28).

Per family:
- iterative: 60 evals, 33 feasible; max throughput seen 13.5 MSPS; best accuracy 12.19 bits; best feasible luts_plus_ffs=262; feasible ranges: data_width 13..16, n_iter 12..16, angle_guard -1..2, frac_guard 0..2
- unrolled_k: 40 evals, 28 feasible; max throughput seen 11.7 MSPS; best accuracy 11.78 bits; best feasible luts_plus_ffs=344; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2, k 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Focus on the best-performing family to refine the Pareto front.*)
- `iterative` (20 evals): data_width=14..16, n_iter=12..16, angle_guard=1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Iterative is the best-performing family so far with the lowest area (262). Refining the search around the known good region (data_width 14-16, n_iter 12-16) will help find the optimal trade-off points on the Pareto front.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 20 evaluations this round, 120 total; 77 feasible; hypervolume 2764 (+3.2%).

**LLM decision:** `stop` — The constraints are met: 0% of evaluations violate throughput (best 13.5 MSPS) and the best accuracy is 12.26 bits (0.000204), well under the 2^-10 limit. The Pareto front is well-populated with 8 feasible designs spanning luts_plus_ffs 253..336 and accuracy_bits 10.2..12.3, with the minimum-area design at 253 LUTs+FFs. The iterative family dominates the front (best area 253 vs unrolled_k's 344), and the front covers the relevant trade-off space. Since this is the final round, the current front is sufficient for selection.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 2764 (gain this round: +3.2%).
Feasible designs: 77 of 120 evaluations (52 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 13.5
- max_abs_err <= 0.000976562: 36% violate; best seen 0.000204 (2^-12.26)

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=253, accuracy_bits=10.2, luts=161, ffs=93, throughput_msps=13.2, max_abs_err=0.000835 (2^-10.23), power_index=0.143
- iterative [data_width=14 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=262, accuracy_bits=10.4, luts=170, ffs=92, throughput_msps=12.4, max_abs_err=0.000746 (2^-10.39), power_index=0.158
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.7, luts=170, ffs=93, throughput_msps=11.7, max_abs_err=0.000599 (2^-10.71), power_index=0.168
- iterative [data_width=15 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.7, luts=170, ffs=93, throughput_msps=11, max_abs_err=0.000599 (2^-10.71), power_index=0.178
- iterative [data_width=16 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.7, luts=179, ffs=97, throughput_msps=10.4, max_abs_err=0.000301 (2^-11.70), power_index=0.197
- iterative [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=295, accuracy_bits=12.2, luts=193, ffs=102, throughput_msps=10.4, max_abs_err=0.000219 (2^-12.16), power_index=0.211
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=324, accuracy_bits=12.2, luts=225, ffs=100, throughput_msps=11.7, max_abs_err=0.000209 (2^-12.22), power_index=0.207
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=336, accuracy_bits=12.3, luts=234, ffs=102, throughput_msps=11.7, max_abs_err=0.000204 (2^-12.26), power_index=0.215
Front coverage: luts_plus_ffs 253..336 (HV reference 1500); accuracy_bits 10.2..12.3 (HV reference 10); data_width on the front 14..16 (registry 8..28).

Per family:
- iterative: 80 evals, 49 feasible; max throughput seen 13.5 MSPS; best accuracy 12.26 bits; best feasible luts_plus_ffs=253; feasible ranges: data_width 13..16, n_iter 12..16, angle_guard -1..2, frac_guard 0..2
- unrolled_k: 40 evals, 28 feasible; max throughput seen 11.7 MSPS; best accuracy 11.78 bits; best feasible luts_plus_ffs=344; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2, k 2..2
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `iterative` (80 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (8 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 152 feasible; hypervolume 1.572e+04 (+468.7%).

**No LLM call** (code's front-mapping round): The constraints are met: 0% of evaluations violate throughput (best 13.5 MSPS) and the best accuracy is 12.26 bits (0.000204), well under the 2^-10 limit. The Pareto front is well-populated with 8 feasible designs spanning luts_plus_ffs 253..336 and accuracy_bits 10.2..12.3, with the minimum-area design at 253 LUTs+FFs. The iterative family dominates the front (best area 253 vs unrolled_k's 344), and the front covers the relevant trade-off space. Since this is the final round, the current front is sufficient for selection.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.572e+04 (gain this round: +468.7%).
Feasible designs: 152 of 200 evaluations (117 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14.3
- max_abs_err <= 0.000976562: 24% violate; best seen 2.91e-08 (2^-25.04)

Pareto front (feasible, 28 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=253, accuracy_bits=10.2, luts=161, ffs=93, throughput_msps=13.2, max_abs_err=0.000835 (2^-10.23), power_index=0.143
- iterative [data_width=15 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.7, luts=170, ffs=93, throughput_msps=11, max_abs_err=0.000599 (2^-10.71), power_index=0.178
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=324, accuracy_bits=12.2, luts=225, ffs=100, throughput_msps=11.7, max_abs_err=0.000209 (2^-12.22), power_index=0.207
- iterative [data_width=20 n_iter=15 angle_guard=4 frac_guard=0 rounding=trunc] luts_plus_ffs=343, accuracy_bits=13.5, luts=223, ffs=120, throughput_msps=10.5, max_abs_err=8.43e-05 (2^-13.53), power_index=0.232
- iterative [data_width=21 n_iter=26 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=387, accuracy_bits=15, luts=265, ffs=122, throughput_msps=5.48, max_abs_err=3.02e-05 (2^-15.02), power_index=0.422
- iterative [data_width=22 n_iter=22 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=428, accuracy_bits=17.5, luts=299, ffs=129, throughput_msps=6.24, max_abs_err=5.49e-06 (2^-17.47), power_index=0.403
- iterative [data_width=24 n_iter=26 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=485, accuracy_bits=19.1, luts=343, ffs=142, throughput_msps=5.28, max_abs_err=1.76e-06 (2^-19.11), power_index=0.529
- iterative [data_width=25 n_iter=28 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=547, accuracy_bits=21.7, luts=396, ffs=151, throughput_msps=4.94, max_abs_err=2.97e-07 (2^-21.68), power_index=0.638
- iterative [data_width=28 n_iter=28 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=597, accuracy_bits=23.7, luts=434, ffs=163, throughput_msps=4.94, max_abs_err=7.27e-08 (2^-23.71), power_index=0.697
- iterative [data_width=28 n_iter=30 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=703, accuracy_bits=25, luts=536, ffs=166, throughput_msps=4.56, max_abs_err=2.91e-08 (2^-25.04), power_index=0.872
Front coverage: luts_plus_ffs 253..703 (HV reference 1500); accuracy_bits 10.2..25 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 160 evals, 124 feasible; max throughput seen 14.3 MSPS; best accuracy 25.04 bits; best feasible luts_plus_ffs=253; feasible ranges: data_width 13..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 40 evals, 28 feasible; max throughput seen 11.7 MSPS; best accuracy 11.78 bits; best feasible luts_plus_ffs=344; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2, k 2..2
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7780 in, 2220 out
- provider-reported cost: $0.0045
- full prompts and replies: `llm_trace.jsonl`

