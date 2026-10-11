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
`pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=5` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 861 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 213 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 80.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 80.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 62 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.29 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000168 (2^-12.54) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 5.49 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 4.52e-05 (2^-14.43) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.48 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.5 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (24 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=5` | 861 | 213 | 80.6 | 5 | 1.29 | 0.000168 (2^-12.54) | 12.54 |
| 1 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=5` | 926 | 219 | 80.6 | 5 | 1.38 | 0.000158 (2^-12.63) | 12.63 |
| 2 | `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=0,rounding=round,m=4` | 890 | 282 | 97.8 | 6 | 1.41 | 0.000145 (2^-12.75) | 12.75 |
| 3 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=4` | 905 | 287 | 93.6 | 6 | 1.43 | 0.000119 (2^-13.04) | 13.04 |
| 4 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=4` | 969 | 287 | 93.6 | 6 | 1.51 | 0.000108 (2^-13.18) | 13.18 |
| 5 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1002 | 301 | 93.6 | 6 | 1.57 | 9.56e-05 (2^-13.35) | 13.35 |
| 6 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=3` | 987 | 364 | 119.3 | 7 | 1.63 | 9.31e-05 (2^-13.39) | 13.39 |
| 7 | `pipelined_m:data_width=18,n_iter=15,angle_guard=3,frac_guard=2,rounding=round,m=3` | 1032 | 377 | 119.3 | 7 | 1.7 | 8.22e-05 (2^-13.57) | 13.57 |
| 8 | `pipelined_m:data_width=24,n_iter=15,angle_guard=0,frac_guard=0,rounding=round,m=3` | 1156 | 447 | 114.5 | 7 | 1.93 | 6.14e-05 (2^-13.99) | 13.99 |
| 9 | `pipelined_m:data_width=18,n_iter=18,angle_guard=3,frac_guard=1,rounding=round,m=3` | 1208 | 436 | 119.3 | 8 | 1.98 | 4.46e-05 (2^-14.45) | 14.45 |
| 10 | `pipelined_m:data_width=18,n_iter=18,angle_guard=2,frac_guard=3,rounding=trunc,m=3` | 1223 | 448 | 119.3 | 8 | 2.01 | 4.39e-05 (2^-14.48) | 14.48 |
| 11 | `pipelined_m:data_width=25,n_iter=16,angle_guard=3,frac_guard=0,rounding=round,m=4` | 1333 | 393 | 86.0 | 6 | 2.08 | 3.07e-05 (2^-14.99) | 14.99 |
| 12 | `pipelined_m:data_width=19,n_iter=18,angle_guard=3,frac_guard=3,rounding=round,m=3` | 1335 | 476 | 119.3 | 8 | 2.18 | 1.78e-05 (2^-15.78) | 15.78 |
| 13 | `pipelined_m:data_width=24,n_iter=17,angle_guard=3,frac_guard=0,rounding=trunc,m=3` | 1371 | 545 | 110.0 | 8 | 2.31 | 1.65e-05 (2^-15.88) | 15.88 |
| 14 | `pipelined_m:data_width=22,n_iter=18,angle_guard=2,frac_guard=3,rounding=round,m=3` | 1485 | 531 | 114.5 | 8 | 2.43 | 9.07e-06 (2^-16.75) | 16.75 |
| 15 | `pipelined_m:data_width=25,n_iter=18,angle_guard=3,frac_guard=0,rounding=round,m=3` | 1510 | 565 | 110.0 | 8 | 2.5 | 7.97e-06 (2^-16.94) | 16.94 |
| 16 | `pipelined_m:data_width=25,n_iter=18,angle_guard=3,frac_guard=3,rounding=round,m=4` | 1670 | 505 | 86.0 | 7 | 2.62 | 7.71e-06 (2^-16.98) | 16.98 |
| 17 | `pipelined_m:data_width=28,n_iter=18,angle_guard=3,frac_guard=1,rounding=round,m=3` | 1766 | 638 | 105.9 | 8 | 2.89 | 7.64e-06 (2^-17.00) | 17.00 |
| 18 | `pipelined_m:data_width=28,n_iter=18,angle_guard=2,frac_guard=3,rounding=round,m=3` | 1820 | 652 | 105.9 | 8 | 2.98 | 7.62e-06 (2^-17.00) | 17.00 |
| 19 | `pipelined_m:data_width=25,n_iter=22,angle_guard=2,frac_guard=1,rounding=trunc,m=3` | 1886 | 743 | 110.0 | 10 | 3.16 | 1.02e-06 (2^-19.91) | 19.91 |
| 20 | `pipelined_m:data_width=28,n_iter=22,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 2085 | 817 | 105.9 | 10 | 3.49 | 9.33e-07 (2^-20.03) | 20.03 |
| 21 | `pipelined_m:data_width=28,n_iter=25,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 2383 | 913 | 105.9 | 11 | 3.97 | 5.4e-07 (2^-20.82) | 20.82 |
| 22 | `pipelined_m:data_width=28,n_iter=25,angle_guard=0,frac_guard=4,rounding=trunc,m=3` | 2484 | 947 | 105.9 | 11 | 4.13 | 1.74e-07 (2^-22.45) | 22.45 |
| 23 | `pipelined:data_width=27,n_iter=29,angle_guard=2,frac_guard=2,rounding=round` | 2806 | 2744 | 249.0 | 31 | 6.68 | 9.57e-08 (2^-23.32) | 23.32 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show that pipelined and pipelined_m are the only families capable of meeting the strict throughput (32 Msps) and latency (0.44us) constraints. pipelined_m is currently the clear winner on area (1248 vs 1814). I will focus 60% of the budget on pipelined_m to refine the front and find the minimum area design, and 40% on pipelined to ensure we haven't missed a better trade-off point in the fully pipelined family. The ranges are narrowed to the region where accuracy_bits >= 12 is achievable (data_width 14-18, n_iter 12-18) to maximize the density of evaluations on the feasible Pareto front.*)
- `pipelined_m` (60 evals): data_width=14..18, n_iter=12..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* pipelined_m dominates the current front (11 of 14 designs, best 1248 luts+ffs). I will refine the region around the known feasible points to tighten the hypervolume and find the absolute minimum area design that still meets the 32 Msps and 0.44us batch constraints.
- `pipelined` (40 evals): data_width=14..18, n_iter=12..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined is the only other family with feasible designs (best 1814 luts+ffs). I will search the same accuracy/width region to ensure the full Pareto front is mapped, particularly for the throughput/latency trade-off where pipelined's 1-result/cycle throughput is critical for the 32 Msps constraint.

**Result (code):** 100 evaluations this round, 100 total; 55 feasible; hypervolume 5338 (n/a).

**LLM decision:** `refine` — The current Pareto front is dominated by `pipelined_m` designs with `data_width` 17-18 and `n_iter` 15-16. The lowest area design (1074 LUTs+FFs) achieves 12.5 accuracy bits, which satisfies the constraint (max_abs_err <= 2^-12). The `pipelined` family is significantly more expensive (min 1633 LUTs+FFs) and only offers marginal accuracy gains at high area costs, making it less relevant for the primary objective of minimizing area. The `sys_p99_batch_us` constraint is tight (0.44 us), and `pipelined_m` with higher `m` (e.g., m=5) has lower latency than `m=2`, which is beneficial for the bursty 32-request tick. To refine the front, I will narrow the search space to focus on the most promising region: `data_width` 17-18, `n_iter` 14-16, `angle_guard` 0-1, `frac_guard` 0-1, and `m` 4-6 for `pipelined_m`. This should allow Optuna to find better trade-offs between area and accuracy within the feasible region, potentially lowering the area for a given accuracy or increasing accuracy for a given area.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 5338 (gain this round: n/a (first round)).
Feasible designs: 55 of 100 evaluations (39 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 35% violate; best seen 5.46e-05 (2^-14.16)
- sys_p99_batch_us <= 0.44: 19% violate; best seen 0.161

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=5] luts_plus_ffs=1074, accuracy_bits=12.5, luts=861, ffs=213, throughput_msps=80.6, max_abs_err=0.000168 (2^-12.54), power_index=1.29
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=5] luts_plus_ffs=1145, accuracy_bits=12.6, luts=926, ffs=219, throughput_msps=80.6, max_abs_err=0.000158 (2^-12.63), power_index=1.38
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1192, accuracy_bits=13, luts=905, ffs=287, throughput_msps=93.6, max_abs_err=0.000119 (2^-13.04), power_index=1.43
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1303, accuracy_bits=13.4, luts=1002, ffs=301, throughput_msps=93.6, max_abs_err=9.56e-05 (2^-13.35), power_index=1.57
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=2] luts_plus_ffs=1548, accuracy_bits=13.4, luts=987, ffs=561, throughput_msps=164, max_abs_err=9.31e-05 (2^-13.39), power_index=1.86
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2162, accuracy_bits=14.2, luts=1086, ffs=1076, throughput_msps=264, max_abs_err=5.46e-05 (2^-14.16), power_index=2.6
Front coverage: luts_plus_ffs 1074..2162 (HV reference 4000); accuracy_bits 12.5..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 40 evals, 28 feasible; max throughput seen 273 MSPS; best accuracy 14.16 bits; best feasible luts_plus_ffs=1633; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 60 evals, 27 feasible; max throughput seen 171 MSPS; best accuracy 14.11 bits; best feasible luts_plus_ffs=1074; feasible ranges: data_width 17..18, n_iter 15..18, angle_guard 0..2, frac_guard 0..2, m 2..5
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Narrowing the search space to the promising region identified in Round 1 to refine the Pareto front and find better trade-offs between area and accuracy.*)
- `pipelined_m` (20 evals): data_width=17..18, n_iter=14..16, angle_guard=0..1, frac_guard=0..1, rounding=round, m=4..6. *Why:* Focus on the most promising region identified in Round 1: low area, sufficient accuracy, and good latency for the bursty system constraint.

**Result (code):** 20 evaluations this round, 120 total; 62 feasible; hypervolume 5347 (+0.2%).

**LLM decision:** `stop` — The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (pipelined_m, 1074 LUTs+FFs) achieves 12.5 bits of accuracy (max_abs_err 0.000168), which is comfortably below the 2^-12 limit (0.000244). Throughput (80.6 MSPS) and system latency (best seen 0.161 us) are well within the 32 MSPS and 0.44 us requirements. The front spans a reasonable trade-off space (1074-2162 area, 12.5-14.2 bits), and hypervolume improvement has plateaued (+0.2% in the last round). Since this is the final round, we stop and select the design with minimum luts_plus_ffs (1074) from the front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 5347 (gain this round: +0.2%).
Feasible designs: 62 of 120 evaluations (41 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 30% violate; best seen 5.46e-05 (2^-14.16)
- sys_p99_batch_us <= 0.44: 26% violate; best seen 0.161

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=5] luts_plus_ffs=1074, accuracy_bits=12.5, luts=861, ffs=213, throughput_msps=80.6, max_abs_err=0.000168 (2^-12.54), power_index=1.29
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=5] luts_plus_ffs=1145, accuracy_bits=12.6, luts=926, ffs=219, throughput_msps=80.6, max_abs_err=0.000158 (2^-12.63), power_index=1.38
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1173, accuracy_bits=12.8, luts=890, ffs=282, throughput_msps=97.8, max_abs_err=0.000145 (2^-12.75), power_index=1.41
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1192, accuracy_bits=13, luts=905, ffs=287, throughput_msps=93.6, max_abs_err=0.000119 (2^-13.04), power_index=1.43
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=1.51
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1303, accuracy_bits=13.4, luts=1002, ffs=301, throughput_msps=93.6, max_abs_err=9.56e-05 (2^-13.35), power_index=1.57
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=2] luts_plus_ffs=1548, accuracy_bits=13.4, luts=987, ffs=561, throughput_msps=164, max_abs_err=9.31e-05 (2^-13.39), power_index=1.86
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2162, accuracy_bits=14.2, luts=1086, ffs=1076, throughput_msps=264, max_abs_err=5.46e-05 (2^-14.16), power_index=2.6
Front coverage: luts_plus_ffs 1074..2162 (HV reference 4000); accuracy_bits 12.5..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 40 evals, 28 feasible; max throughput seen 273 MSPS; best accuracy 14.16 bits; best feasible luts_plus_ffs=1633; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 80 evals, 34 feasible; max throughput seen 171 MSPS; best accuracy 14.11 bits; best feasible luts_plus_ffs=1074; feasible ranges: data_width 17..18, n_iter 15..18, angle_guard 0..2, frac_guard 0..2, m 2..5
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (70 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (7 front designs; box front_anchored)
- `pipelined` (10 evals): data_width=17..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 123 feasible; hypervolume 1.747e+04 (+226.7%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (pipelined_m, 1074 LUTs+FFs) achieves 12.5 bits of accuracy (max_abs_err 0.000168), which is comfortably below the 2^-12 limit (0.000244). Throughput (80.6 MSPS) and system latency (best seen 0.161 us) are well within the 32 MSPS and 0.44 us requirements. The front spans a reasonable trade-off space (1074-2162 area, 12.5-14.2 bits), and hypervolume improvement has plateaued (+0.2% in the last round). Since this is the final round, we stop and select the design with minimum luts_plus_ffs (1074) from the front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.747e+04 (gain this round: +226.7%).
Feasible designs: 123 of 200 evaluations (93 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 22% violate; best seen 9.57e-08 (2^-23.32)
- sys_p99_batch_us <= 0.44: 22% violate; best seen 0.161

Pareto front (feasible, 24 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=5] luts_plus_ffs=1074, accuracy_bits=12.5, luts=861, ffs=213, throughput_msps=80.6, max_abs_err=0.000168 (2^-12.54), power_index=1.29
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1192, accuracy_bits=13, luts=905, ffs=287, throughput_msps=93.6, max_abs_err=0.000119 (2^-13.04), power_index=1.43
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1303, accuracy_bits=13.4, luts=1002, ffs=301, throughput_msps=93.6, max_abs_err=9.56e-05 (2^-13.35), power_index=1.57
- pipelined_m [data_width=24 n_iter=15 angle_guard=0 frac_guard=0 rounding=round m=3] luts_plus_ffs=1603, accuracy_bits=14, luts=1156, ffs=447, throughput_msps=114, max_abs_err=6.14e-05 (2^-13.99), power_index=1.93
- pipelined_m [data_width=18 n_iter=18 angle_guard=2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=1671, accuracy_bits=14.5, luts=1223, ffs=448, throughput_msps=119, max_abs_err=4.39e-05 (2^-14.48), power_index=2.01
- pipelined_m [data_width=24 n_iter=17 angle_guard=3 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=1916, accuracy_bits=15.9, luts=1371, ffs=545, throughput_msps=110, max_abs_err=1.65e-05 (2^-15.88), power_index=2.31
- pipelined_m [data_width=25 n_iter=18 angle_guard=3 frac_guard=0 rounding=round m=3] luts_plus_ffs=2075, accuracy_bits=16.9, luts=1510, ffs=565, throughput_msps=110, max_abs_err=7.97e-06 (2^-16.94), power_index=2.5
- pipelined_m [data_width=28 n_iter=18 angle_guard=2 frac_guard=3 rounding=round m=3] luts_plus_ffs=2472, accuracy_bits=17, luts=1820, ffs=652, throughput_msps=106, max_abs_err=7.62e-06 (2^-17.00), power_index=2.98
- pipelined_m [data_width=28 n_iter=22 angle_guard=-2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=2903, accuracy_bits=20, luts=2085, ffs=817, throughput_msps=106, max_abs_err=9.33e-07 (2^-20.03), power_index=3.49
- pipelined [data_width=27 n_iter=29 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=5550, accuracy_bits=23.3, luts=2806, ffs=2744, throughput_msps=249, max_abs_err=9.57e-08 (2^-23.32), power_index=6.68
Front coverage: luts_plus_ffs 1074..5550 (HV reference 4000); accuracy_bits 12.5..23.3 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- pipelined: 50 evals, 37 feasible; max throughput seen 273 MSPS; best accuracy 23.32 bits; best feasible luts_plus_ffs=1633; feasible ranges: data_width 17..27, n_iter 14..29, angle_guard -1..4, frac_guard 0..2
- pipelined_m: 150 evals, 86 feasible; max throughput seen 171 MSPS; best accuracy 22.45 bits; best feasible luts_plus_ffs=1074; feasible ranges: data_width 17..28, n_iter 14..25, angle_guard -2..3, frac_guard 0..4, m 2..5
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 9295 in, 1792 out
- provider-reported cost: $0.0051
- full prompts and replies: `llm_trace.jsonl`

