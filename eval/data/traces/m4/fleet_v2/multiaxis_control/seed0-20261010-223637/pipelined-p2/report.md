# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec multiaxis_control: Shared sin/cos unit for a 16-axis motor-control loop: a 1 MHz control tick issues 32 requests at once (Park + inverse Park per axis); all 32 results must be back within 0.44 us of the tick (p99 over ticks). Max error <= 2^-12. Minimise LUTs + FFs.
  constraint: throughput_msps >= 32
  constraint: max_abs_err <= 0.000244141
  constraint: sys_p99_batch_us <= 0.44
  objective: min luts_plus_ffs (HV ref 4000)
  objective: max accuracy_bits (HV ref 12)
  select: min luts_plus_ffs
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average)
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 855 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 291 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.38 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00017 (2^-12.53) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 11.1 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.25e-05 (2^-14.22) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.44 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (18 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,m=4` | 855 | 291 | 93.6 | 6 | 1.38 | 0.00017 (2^-12.53) | 12.53 |
| 1 | `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=0,rounding=round,m=4` | 890 | 282 | 97.8 | 6 | 1.41 | 0.000145 (2^-12.75) | 12.75 |
| 2 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=4` | 905 | 287 | 93.6 | 6 | 1.43 | 0.000119 (2^-13.04) | 13.04 |
| 3 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=4` | 920 | 291 | 93.6 | 6 | 1.46 | 0.000109 (2^-13.17) | 13.17 |
| 4 | `pipelined_m:data_width=19,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=4` | 949 | 301 | 93.6 | 6 | 1.5 | 8.66e-05 (2^-13.50) | 13.50 |
| 5 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=4` | 985 | 291 | 93.6 | 6 | 1.54 | 8.35e-05 (2^-13.55) | 13.55 |
| 6 | `pipelined_m:data_width=19,n_iter=15,angle_guard=4,frac_guard=0,rounding=round,m=4` | 994 | 313 | 89.6 | 6 | 1.57 | 8.33e-05 (2^-13.55) | 13.55 |
| 7 | `pipelined_m:data_width=19,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=4` | 1033 | 305 | 93.6 | 6 | 1.61 | 5.75e-05 (2^-14.09) | 14.09 |
| 8 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1086 | 305 | 93.6 | 6 | 1.67 | 5.46e-05 (2^-14.16) | 14.16 |
| 9 | `pipelined_m:data_width=19,n_iter=16,angle_guard=1,frac_guard=3,rounding=trunc,m=4` | 1112 | 319 | 93.6 | 6 | 1.72 | 5.06e-05 (2^-14.27) | 14.27 |
| 10 | `pipelined_m:data_width=20,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1185 | 333 | 93.6 | 6 | 1.83 | 3.61e-05 (2^-14.76) | 14.76 |
| 11 | `pipelined_m:data_width=25,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc,m=4` | 1317 | 389 | 86.0 | 6 | 2.05 | 3.08e-05 (2^-14.99) | 14.99 |
| 12 | `pipelined_m:data_width=28,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=4` | 1459 | 432 | 86.0 | 6 | 2.28 | 3.05e-05 (2^-15.00) | 15.00 |
| 13 | `pipelined_m:data_width=20,n_iter=19,angle_guard=1,frac_guard=2,rounding=round,m=2` | 1394 | 765 | 164.4 | 12 | 2.6 | 1.57e-05 (2^-15.96) | 15.96 |
| 14 | `pipelined_m:data_width=25,n_iter=19,angle_guard=2,frac_guard=4,rounding=trunc,m=4` | 1731 | 506 | 86.0 | 7 | 2.69 | 3.99e-06 (2^-17.93) | 17.93 |
| 15 | `pipelined_m:data_width=25,n_iter=22,angle_guard=-1,frac_guard=0,rounding=round,m=2` | 1776 | 949 | 158.3 | 13 | 3.28 | 2.13e-06 (2^-18.84) | 18.84 |
| 16 | `pipelined_m:data_width=26,n_iter=21,angle_guard=3,frac_guard=3,rounding=round,m=3` | 2020 | 712 | 110.0 | 9 | 3.29 | 1.01e-06 (2^-19.92) | 19.92 |
| 17 | `pipelined_m:data_width=25,n_iter=26,angle_guard=1,frac_guard=1,rounding=round,m=3` | 2271 | 822 | 114.5 | 11 | 3.72 | 6.42e-07 (2^-20.57) | 20.57 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 Msps throughput and a 0.44us batch latency, which only pipelined/pipelined_m families can meet (iterative/unrolled_k are infeasible). pipelined_m is the area leader (1306 vs 1689), so I allocate 60% of the budget to refine its front, focusing on m=2..4 to balance area and Fmax. The remaining 40% goes to pipelined (m=1) to check if its higher Fmax is necessary for the tight 0.44us batch constraint, especially since L2 simulation may penalize designs that just barely pass the L1 bound. I restrict data_width to 14..18 and n_iter to 12..16 to ensure max_abs_err <= 2^-12 while minimizing area, and use rounding='round' to maximize accuracy_bits for the hypervolume objective.*)
- `pipelined_m` (60 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..1, rounding=round, m=2..4. *Why:* pipelined_m is the current area champion (1306 luts_plus_ffs) and dominates the merged front. Focusing on m=2..4 with tight accuracy guards (W=14..18, N=12..16) should map the low-area corner of the front while keeping throughput at 1 result/cycle to satisfy the 32 Msps and 0.44us batch constraints.
- `pipelined` (40 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..1, rounding=round. *Why:* pipelined (m=1) has higher Fmax potential due to shorter critical paths, which may be needed if pipelined_m's Fmax is too low to meet the 0.44us batch constraint at L2. Searching the same accuracy box allows direct comparison of the area/Fmax trade-off between m=1 and m>1.

**Result (code):** 100 evaluations this round, 100 total; 60 feasible; hypervolume 5279 (n/a).

**LLM decision:** `refine` — The current Pareto front is dominated by `pipelined_m` designs with `data_width=18`, which is the minimum width required to meet the `max_abs_err <= 2^-12` constraint (since `data_width=17` yields ~12 bits of accuracy, which is borderline or insufficient depending on rounding/guards, and the feasible range for `data_width` in round 1 was 17..18, but the front is exclusively 18). The `pipelined` family is significantly less efficient (best feasible area 1689 vs 1145 for `pipelined_m`). The `sys_p99_batch_us` constraint is easily met (best 0.161 us vs 0.44 us limit), and throughput is abundant (best 273 MSPS vs 32 MSPS limit). Therefore, the search should focus on minimizing area within the `pipelined_m` family by tightening the parameter ranges around the known good region: `data_width=18`, `n_iter` 14-16, `angle_guard` 0-2, `frac_guard` 0-1, and `m` 2-4. This will allow Optuna to more densely sample the trade-off between `n_iter`/`angle_guard` (accuracy) and `m` (area/latency) to find the true minimum area design that satisfies the error constraint.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 5279 (gain this round: n/a (first round)).
Feasible designs: 60 of 100 evaluations (33 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 40% violate; best seen 6.45e-05 (2^-13.92)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.161

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1145, accuracy_bits=12.5, luts=855, ffs=291, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.53), power_index=1.38
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1173, accuracy_bits=12.8, luts=890, ffs=282, throughput_msps=97.8, max_abs_err=0.000145 (2^-12.75), power_index=1.41
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1192, accuracy_bits=13, luts=905, ffs=287, throughput_msps=93.6, max_abs_err=0.000119 (2^-13.04), power_index=1.43
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1210, accuracy_bits=13.2, luts=920, ffs=291, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=1.46
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1276, accuracy_bits=13.5, luts=985, ffs=291, throughput_msps=93.6, max_abs_err=8.35e-05 (2^-13.55), power_index=1.54
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=1485, accuracy_bits=13.9, luts=1055, ffs=430, throughput_msps=119, max_abs_err=6.45e-05 (2^-13.92), power_index=1.79
Front coverage: luts_plus_ffs 1145..1485 (HV reference 4000); accuracy_bits 12.5..13.9 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- pipelined: 40 evals, 24 feasible; max throughput seen 273 MSPS; best accuracy 13.92 bits; best feasible luts_plus_ffs=1689; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..1
- pipelined_m: 60 evals, 36 feasible; max throughput seen 171 MSPS; best accuracy 13.92 bits; best feasible luts_plus_ffs=1145; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..1, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Narrowing to the proven feasible region of the best family allows for a more thorough exploration of the area-accuracy trade-off within the tight constraints.*)
- `pipelined_m` (20 evals): data_width=18..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..1, rounding=trunc|round, m=2..4. *Why:* Focus on the most efficient family and narrow ranges to the feasible region identified in Round 1 to maximize sampling density for area minimization.

**Result (code):** 20 evaluations this round, 120 total; 80 feasible; hypervolume 5279 (+0.0%).

**LLM decision:** `stop` — The feasible Pareto front is well-established and the constraints are comfortably met. The minimum area design (pipelined_m, 1145 LUTs+FFs) achieves 12.5 bits of accuracy (max_abs_err 0.00017), which is well below the 2^-12 (0.000244) requirement. Throughput (93.6 MSPS) and system latency (0.161 us p99 batch) are also well within limits. The front spans a reasonable range of the accuracy objective (12.5 to 13.9 bits) and area (1145 to 1485). Since this is the final round, further exploration would not change the selection (min luts_plus_ffs), which is already identified as the 1145-area pipelined_m design. The hypervolume gain in the last round was 0.0%, indicating convergence.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 5279 (gain this round: +0.0%).
Feasible designs: 80 of 120 evaluations (41 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 33% violate; best seen 6.45e-05 (2^-13.92)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.161

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1145, accuracy_bits=12.5, luts=855, ffs=291, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.53), power_index=1.38
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1173, accuracy_bits=12.8, luts=890, ffs=282, throughput_msps=97.8, max_abs_err=0.000145 (2^-12.75), power_index=1.41
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1192, accuracy_bits=13, luts=905, ffs=287, throughput_msps=93.6, max_abs_err=0.000119 (2^-13.04), power_index=1.43
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1210, accuracy_bits=13.2, luts=920, ffs=291, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=1.46
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=1.51
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1276, accuracy_bits=13.5, luts=985, ffs=291, throughput_msps=93.6, max_abs_err=8.35e-05 (2^-13.55), power_index=1.54
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=1485, accuracy_bits=13.9, luts=1055, ffs=430, throughput_msps=119, max_abs_err=6.45e-05 (2^-13.92), power_index=1.79
Front coverage: luts_plus_ffs 1145..1485 (HV reference 4000); accuracy_bits 12.5..13.9 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- pipelined: 40 evals, 24 feasible; max throughput seen 273 MSPS; best accuracy 13.92 bits; best feasible luts_plus_ffs=1689; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..1
- pipelined_m: 80 evals, 56 feasible; max throughput seen 171 MSPS; best accuracy 13.92 bits; best feasible luts_plus_ffs=1145; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..1, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (80 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (7 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 146 feasible; hypervolume 1.638e+04 (+210.3%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and the constraints are comfortably met. The minimum area design (pipelined_m, 1145 LUTs+FFs) achieves 12.5 bits of accuracy (max_abs_err 0.00017), which is well below the 2^-12 (0.000244) requirement. Throughput (93.6 MSPS) and system latency (0.161 us p99 batch) are also well within limits. The front spans a reasonable range of the accuracy objective (12.5 to 13.9 bits) and area (1145 to 1485). Since this is the final round, further exploration would not change the selection (min luts_plus_ffs), which is already identified as the 1145-area pipelined_m design. The hypervolume gain in the last round was 0.0%, indicating convergence.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.638e+04 (gain this round: +210.3%).
Feasible designs: 146 of 200 evaluations (98 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 22% violate; best seen 1.04e-07 (2^-23.20)
- sys_p99_batch_us <= 0.44: 6% violate; best seen 0.161

Pareto front (feasible, 18 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1145, accuracy_bits=12.5, luts=855, ffs=291, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.53), power_index=1.38
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1192, accuracy_bits=13, luts=905, ffs=287, throughput_msps=93.6, max_abs_err=0.000119 (2^-13.04), power_index=1.43
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1250, accuracy_bits=13.5, luts=949, ffs=301, throughput_msps=93.6, max_abs_err=8.66e-05 (2^-13.50), power_index=1.5
- pipelined_m [data_width=19 n_iter=15 angle_guard=4 frac_guard=0 rounding=round m=4] luts_plus_ffs=1306, accuracy_bits=13.6, luts=994, ffs=313, throughput_msps=89.6, max_abs_err=8.33e-05 (2^-13.55), power_index=1.57
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1391, accuracy_bits=14.2, luts=1086, ffs=305, throughput_msps=93.6, max_abs_err=5.46e-05 (2^-14.16), power_index=1.67
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1431, accuracy_bits=14.3, luts=1112, ffs=319, throughput_msps=93.6, max_abs_err=5.06e-05 (2^-14.27), power_index=1.72
- pipelined_m [data_width=25 n_iter=16 angle_guard=2 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1707, accuracy_bits=15, luts=1317, ffs=389, throughput_msps=86, max_abs_err=3.08e-05 (2^-14.99), power_index=2.05
- pipelined_m [data_width=20 n_iter=19 angle_guard=1 frac_guard=2 rounding=round m=2] luts_plus_ffs=2159, accuracy_bits=16, luts=1394, ffs=765, throughput_msps=164, max_abs_err=1.57e-05 (2^-15.96), power_index=2.6
- pipelined_m [data_width=25 n_iter=22 angle_guard=-1 frac_guard=0 rounding=round m=2] luts_plus_ffs=2725, accuracy_bits=18.8, luts=1776, ffs=949, throughput_msps=158, max_abs_err=2.13e-06 (2^-18.84), power_index=3.28
- pipelined_m [data_width=25 n_iter=26 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=3093, accuracy_bits=20.6, luts=2271, ffs=822, throughput_msps=114, max_abs_err=6.42e-07 (2^-20.57), power_index=3.72
Front coverage: luts_plus_ffs 1145..3093 (HV reference 4000); accuracy_bits 12.5..20.6 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- pipelined: 40 evals, 24 feasible; max throughput seen 273 MSPS; best accuracy 13.92 bits; best feasible luts_plus_ffs=1689; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..1
- pipelined_m: 160 evals, 122 feasible; max throughput seen 171 MSPS; best accuracy 23.20 bits; best feasible luts_plus_ffs=1145; feasible ranges: data_width 17..28, n_iter 14..29, angle_guard -1..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 9196 in, 1848 out
- provider-reported cost: $0.0043
- full prompts and replies: `llm_trace.jsonl`

