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
`pipelined_m:data_width=16,n_iter=15,angle_guard=1,frac_guard=2,rounding=round,m=5` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 909 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 212 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 80.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 80.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 62 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.35 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000218 (2^-12.16) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.57 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 4.79e-05 (2^-14.35) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 0.784 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.2 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (26 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=15,angle_guard=1,frac_guard=2,rounding=round,m=5` | 909 | 212 | 80.6 | 5 | 1.35 | 0.000218 (2^-12.16) | 12.16 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=4` | 841 | 287 | 93.6 | 6 | 1.36 | 0.000175 (2^-12.48) | 12.48 |
| 2 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 868 | 293 | 93.6 | 6 | 1.4 | 0.000172 (2^-12.50) | 12.50 |
| 3 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 896 | 299 | 93.6 | 6 | 1.44 | 0.000163 (2^-12.58) | 12.58 |
| 4 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=4` | 906 | 295 | 93.6 | 6 | 1.45 | 0.00016 (2^-12.61) | 12.61 |
| 5 | `pipelined_m:data_width=19,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 909 | 307 | 93.6 | 6 | 1.46 | 0.000148 (2^-12.72) | 12.72 |
| 6 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 935 | 293 | 93.6 | 6 | 1.48 | 0.000127 (2^-12.95) | 12.95 |
| 7 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 949 | 297 | 93.6 | 6 | 1.5 | 0.000118 (2^-13.05) | 13.05 |
| 8 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 964 | 299 | 93.6 | 6 | 1.52 | 0.000102 (2^-13.26) | 13.26 |
| 9 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=4` | 973 | 295 | 93.6 | 6 | 1.53 | 0.000101 (2^-13.27) | 13.27 |
| 10 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1002 | 301 | 93.6 | 6 | 1.57 | 9.56e-05 (2^-13.35) | 13.35 |
| 11 | `pipelined_m:data_width=19,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1008 | 313 | 93.6 | 6 | 1.59 | 8.04e-05 (2^-13.60) | 13.60 |
| 12 | `pipelined_m:data_width=19,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1019 | 309 | 93.6 | 6 | 1.6 | 7.94e-05 (2^-13.62) | 13.62 |
| 13 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1071 | 301 | 93.6 | 6 | 1.65 | 7.47e-05 (2^-13.71) | 13.71 |
| 14 | `pipelined_m:data_width=19,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 1064 | 311 | 93.6 | 6 | 1.66 | 6.35e-05 (2^-13.94) | 13.94 |
| 15 | `pipelined_m:data_width=19,n_iter=17,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1152 | 382 | 93.6 | 7 | 1.85 | 4.75e-05 (2^-14.36) | 14.36 |
| 16 | `pipelined_m:data_width=19,n_iter=17,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1158 | 376 | 93.6 | 7 | 1.85 | 4.63e-05 (2^-14.40) | 14.40 |
| 17 | `pipelined_m:data_width=19,n_iter=17,angle_guard=3,frac_guard=2,rounding=trunc,m=4` | 1185 | 392 | 93.6 | 7 | 1.9 | 3.38e-05 (2^-14.85) | 14.85 |
| 18 | `pipelined_m:data_width=23,n_iter=17,angle_guard=1,frac_guard=0,rounding=round,m=4` | 1287 | 435 | 89.6 | 7 | 2.07 | 1.66e-05 (2^-15.88) | 15.88 |
| 19 | `pipelined_m:data_width=26,n_iter=17,angle_guard=-1,frac_guard=1,rounding=round,m=4` | 1493 | 486 | 86.0 | 7 | 2.38 | 1.56e-05 (2^-15.97) | 15.97 |
| 20 | `pipelined_m:data_width=26,n_iter=17,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1506 | 504 | 86.0 | 7 | 2.42 | 1.54e-05 (2^-15.99) | 15.99 |
| 21 | `pipelined_m:data_width=22,n_iter=20,angle_guard=-1,frac_guard=2,rounding=trunc,m=3` | 1507 | 577 | 114.5 | 9 | 2.51 | 1.49e-05 (2^-16.04) | 16.04 |
| 22 | `pipelined_m:data_width=24,n_iter=20,angle_guard=-1,frac_guard=3,rounding=round,m=4` | 1718 | 468 | 86.0 | 7 | 2.63 | 4.19e-06 (2^-17.86) | 17.86 |
| 23 | `pipelined_m:data_width=23,n_iter=21,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1691 | 535 | 89.6 | 8 | 2.68 | 3.2e-06 (2^-18.25) | 18.25 |
| 24 | `pipelined_m:data_width=27,n_iter=20,angle_guard=-1,frac_guard=3,rounding=trunc,m=3` | 1847 | 705 | 110.0 | 9 | 3.07 | 2.27e-06 (2^-18.75) | 18.75 |
| 25 | `pipelined_m:data_width=27,n_iter=23,angle_guard=-1,frac_guard=3,rounding=trunc,m=3` | 2138 | 799 | 110.0 | 10 | 3.54 | 7.31e-07 (2^-20.38) | 20.38 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 Msps throughput (1 result/cycle), max_abs_err <= 2^-12, and sys_p99_batch_us <= 0.44us. Only pipelined and pipelined_m can meet the throughput constraint (iterative and unrolled_k produce <1 result/cycle and are infeasible, as confirmed by the fleet facts). pipelined_m has already found a better area solution (1121 vs 1716), so I'm allocating 60% of the budget to densely explore pipelined_m's parameter space, particularly the m parameter which controls the register/area trade-off. The 40% for pipelined ensures the full Pareto front is mapped, as pipelined may dominate in Fmax-sensitive regions that affect the system-level latency constraint. Both families are restricted to the accuracy-feasible region (data_width 14-18, n_iter 14-20) to avoid wasting evaluations on designs that fail the max_abs_err constraint. The angle_guard and frac_guard ranges are kept narrow (-2 to 2 and 0 to 2) since these primarily affect accuracy margin and area with diminishing returns beyond small values.*)
- `pipelined_m` (60 evals): data_width=14..18, n_iter=14..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* pipelined_m is the only family with a feasible design beating the current best (1121 vs 1716). It achieves 1 result/cycle throughput (meeting the 32 Msps constraint) while using fewer registers than fully pipelined. The current 2 feasible points are sparse; I need to densely map the trade-off between m (register spacing), n_iter, and data_width to find the true Pareto front. Narrowing data_width to 14-18 and n_iter to 14-20 focuses on the region where accuracy_bits >= 12 is achievable with minimal area. The m parameter is the key differentiator: larger m means fewer registers (lower FFs) but potentially lower Fmax, which affects the sys_p99_batch_us constraint. I want to explore the full m range to find the sweet spot.
- `pipelined` (40 evals): data_width=14..18, n_iter=14..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined already has 9 of 11 front designs and 35 feasible points, but its best (1716) is worse than pipelined_m's best (1121). However, pipelined may still contribute to the hypervolume in regions where it dominates pipelined_m (e.g., higher Fmax enabling tighter sys_p99_batch_us margins, or different accuracy/area trade-offs at specific n_iter/data_width combinations). I'll focus on the same narrow accuracy-feasible region (data_width 14-18, n_iter 14-20) to refine the front and ensure no pipelined design is missed that could improve hypervolume. The 40% share reflects that pipelined_m is the primary candidate for the final selection, but pipelined still needs coverage to map the full trade-off curve.

**Result (code):** 100 evaluations this round, 100 total; 42 feasible; hypervolume 5518 (n/a).

**LLM decision:** `refine` — Round 1 established that pipelined_m is the dominant family for the area-accuracy trade-off, with a best area of 1121 and best accuracy of 14.04 bits. The front is currently sparse (9 designs) and clustered in a narrow parameter box (data_width 16-18, n_iter 14-18, m 3-5). The hypervolume is 5518, but the front only covers accuracy_bits 12.2-14.0 and area 1121-1575. To maximize hypervolume, we need to densely sample the Pareto surface within this box. Refining the ranges to the feasible region identified in Round 1 (data_width 16-18, n_iter 14-16, m 3-5 for pipelined_m; data_width 16-18, n_iter 14-16 for pipelined) will focus the 100 evals on the most promising region, allowing Optuna to find more Pareto-optimal points and better cover the trade-off curve. This should improve hypervolume by filling in gaps in the front, particularly in the mid-range accuracy/area trade-offs. The throughput constraint is easily met by all feasible designs (min 80.6 MSPS vs 32 required), so it is not a binding constraint for the search. The sys_p99_batch_us constraint is met by most feasible designs (best 0.169 us vs 0.44 us required), so it is also not a binding constraint. The main trade-off is between area and accuracy, which is what the refinement targets.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 5518 (gain this round: n/a (first round)).
Feasible designs: 42 of 100 evaluations (30 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 50% violate; best seen 5.94e-05 (2^-14.04)
- sys_p99_batch_us <= 0.44: 19% violate; best seen 0.169

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=5] luts_plus_ffs=1121, accuracy_bits=12.2, luts=909, ffs=212, throughput_msps=80.6, max_abs_err=0.000218 (2^-12.16), power_index=1.35
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=5] luts_plus_ffs=1139, accuracy_bits=12.5, luts=924, ffs=215, throughput_msps=80.6, max_abs_err=0.000176 (2^-12.48), power_index=1.37
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1161, accuracy_bits=12.5, luts=868, ffs=293, throughput_msps=93.6, max_abs_err=0.000172 (2^-12.50), power_index=1.4
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1201, accuracy_bits=12.6, luts=906, ffs=295, throughput_msps=93.6, max_abs_err=0.00016 (2^-12.61), power_index=1.45
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1227, accuracy_bits=12.9, luts=935, ffs=293, throughput_msps=93.6, max_abs_err=0.000127 (2^-12.95), power_index=1.48
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1294, accuracy_bits=13.2, luts=1001, ffs=293, throughput_msps=93.6, max_abs_err=0.000104 (2^-13.23), power_index=1.56
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1331, accuracy_bits=13.6, luts=1033, ffs=299, throughput_msps=93.6, max_abs_err=8.08e-05 (2^-13.60), power_index=1.6
- pipelined_m [data_width=18 n_iter=17 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1466, accuracy_bits=13.8, luts=1101, ffs=365, throughput_msps=93.6, max_abs_err=6.92e-05 (2^-13.82), power_index=1.77
- pipelined_m [data_width=18 n_iter=18 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1575, accuracy_bits=14, luts=1208, ffs=367, throughput_msps=93.6, max_abs_err=5.94e-05 (2^-14.04), power_index=1.9
Front coverage: luts_plus_ffs 1121..1575 (HV reference 4000); accuracy_bits 12.2..14 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 40 evals, 21 feasible; max throughput seen 273 MSPS; best accuracy 13.39 bits; best feasible luts_plus_ffs=1665; feasible ranges: data_width 16..18, n_iter 14..19, angle_guard 2..2, frac_guard 0..2
- pipelined_m: 60 evals, 21 feasible; max throughput seen 171 MSPS; best accuracy 14.04 bits; best feasible luts_plus_ffs=1121; feasible ranges: data_width 16..18, n_iter 14..19, angle_guard 0..2, frac_guard 0..2, m 3..5
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 1 established that pipelined_m is the dominant family for the area-accuracy trade-off, with a best area of 1121 and best accuracy of 14.04 bits. The front is currently sparse (9 designs) and clustered in a narrow parameter box (data_width 16-18, n_iter 14-18, m 3-5). The hypervolume is 5518, but the front only covers accuracy_bits 12.2-14.0 and area 1121-1575. To maximize hypervolume, we need to densely sample the Pareto surface within this box. Refining the ranges to the feasible region identified in Round 1 (data_width 16-18, n_iter 14-16, m 3-5 for pipelined_m; data_width 16-18, n_iter 14-16 for pipelined) will focus the 100 evals on the most promising region, allowing Optuna to find more Pareto-optimal points and better cover the trade-off curve. This should improve hypervolume by filling in gaps in the front, particularly in the mid-range accuracy/area trade-offs. The throughput constraint is easily met by all feasible designs (min 80.6 MSPS vs 32 required), so it is not a binding constraint for the search. The sys_p99_batch_us constraint is met by most feasible designs (best 0.169 us vs 0.44 us required), so it is also not a binding constraint. The main trade-off is between area and accuracy, which is what the refinement targets.*)
- `pipelined_m` (12 evals): data_width=16..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=3..5. *Why:* pipelined_m dominates the front (best area 1121 vs 1665 for pipelined) and has the best accuracy (14.04 bits). The current front is tightly clustered around data_width=16-18, n_iter=14-16, m=4-5. Refining here will sharpen the trade-off curve between area and accuracy, which directly improves hypervolume. The m=5, data_width=16 corner is the area champion; m=4, data_width=18 corners give the accuracy champion. Focusing the search on this narrow box lets Optuna densely sample the Pareto surface rather than wasting evals on infeasible or dominated regions (e.g., data_width<16 or n_iter<14 which likely violate accuracy or throughput).
- `pipelined` (8 evals): data_width=16..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined has higher throughput (273 MSPS max) but worse area (1665 min). It may contribute to the high-throughput/low-accuracy end of the front or reveal if pipelined_m's m=3-5 range can be beaten at the accuracy end. Keeping it in the search ensures the front is not missing a pipelined design that is Pareto-optimal in the throughput-accuracy-area space, even though the primary objective is area. The ranges are narrowed to the feasible region identified in Round 1 to avoid wasting evals.

**Result (code):** 20 evaluations this round, 120 total; 60 feasible; hypervolume 5530 (+0.2%).

**LLM decision:** `stop` — The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 1121 LUTs+FFs) meets all constraints: throughput 80.6 MSPS >= 32, max_abs_err 2^-12.16 <= 2^-12, and sys_p99_batch_us is well within bounds (best seen 0.169 us <= 0.44 us). The front spans accuracy from 12.2 to 14.04 bits with area from 1121 to 1575, providing a good trade-off curve. Hypervolume gain in the last round was only +0.2%, indicating convergence. The selection rule (min luts_plus_ffs) will pick the 1121 design, which is robustly feasible. No further exploration is needed.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 5530 (gain this round: +0.2%).
Feasible designs: 60 of 120 evaluations (42 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 43% violate; best seen 5.94e-05 (2^-14.04)
- sys_p99_batch_us <= 0.44: 16% violate; best seen 0.169

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=5] luts_plus_ffs=1121, accuracy_bits=12.2, luts=909, ffs=212, throughput_msps=80.6, max_abs_err=0.000218 (2^-12.16), power_index=1.35
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=5] luts_plus_ffs=1139, accuracy_bits=12.5, luts=924, ffs=215, throughput_msps=80.6, max_abs_err=0.000176 (2^-12.48), power_index=1.37
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1161, accuracy_bits=12.5, luts=868, ffs=293, throughput_msps=93.6, max_abs_err=0.000172 (2^-12.50), power_index=1.4
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1201, accuracy_bits=12.6, luts=906, ffs=295, throughput_msps=93.6, max_abs_err=0.00016 (2^-12.61), power_index=1.45
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1227, accuracy_bits=12.9, luts=935, ffs=293, throughput_msps=93.6, max_abs_err=0.000127 (2^-12.95), power_index=1.48
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1263, accuracy_bits=13.3, luts=964, ffs=299, throughput_msps=93.6, max_abs_err=0.000102 (2^-13.26), power_index=1.52
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1267, accuracy_bits=13.3, luts=973, ffs=295, throughput_msps=93.6, max_abs_err=0.000101 (2^-13.27), power_index=1.53
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1331, accuracy_bits=13.6, luts=1033, ffs=299, throughput_msps=93.6, max_abs_err=8.08e-05 (2^-13.60), power_index=1.6
- pipelined_m [data_width=18 n_iter=17 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1466, accuracy_bits=13.8, luts=1101, ffs=365, throughput_msps=93.6, max_abs_err=6.92e-05 (2^-13.82), power_index=1.77
- pipelined_m [data_width=18 n_iter=18 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1575, accuracy_bits=14, luts=1208, ffs=367, throughput_msps=93.6, max_abs_err=5.94e-05 (2^-14.04), power_index=1.9
Front coverage: luts_plus_ffs 1121..1575 (HV reference 4000); accuracy_bits 12.2..14 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 48 evals, 28 feasible; max throughput seen 273 MSPS; best accuracy 13.60 bits; best feasible luts_plus_ffs=1665; feasible ranges: data_width 16..18, n_iter 14..19, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 72 evals, 32 feasible; max throughput seen 171 MSPS; best accuracy 14.04 bits; best feasible luts_plus_ffs=1121; feasible ranges: data_width 16..18, n_iter 14..19, angle_guard 0..2, frac_guard 0..2, m 3..5
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (80 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (10 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 120 feasible; hypervolume 1.669e+04 (+201.8%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 1121 LUTs+FFs) meets all constraints: throughput 80.6 MSPS >= 32, max_abs_err 2^-12.16 <= 2^-12, and sys_p99_batch_us is well within bounds (best seen 0.169 us <= 0.44 us). The front spans accuracy from 12.2 to 14.04 bits with area from 1121 to 1575, providing a good trade-off curve. Hypervolume gain in the last round was only +0.2%, indicating convergence. The selection rule (min luts_plus_ffs) will pick the 1121 design, which is robustly feasible. No further exploration is needed.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.669e+04 (gain this round: +201.8%).
Feasible designs: 120 of 200 evaluations (89 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 30% violate; best seen 2.86e-08 (2^-25.06)
- sys_p99_batch_us <= 0.44: 17% violate; best seen 0.169

Pareto front (feasible, 26 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=5] luts_plus_ffs=1121, accuracy_bits=12.2, luts=909, ffs=212, throughput_msps=80.6, max_abs_err=0.000218 (2^-12.16), power_index=1.35
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1194, accuracy_bits=12.6, luts=896, ffs=299, throughput_msps=93.6, max_abs_err=0.000163 (2^-12.58), power_index=1.44
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1227, accuracy_bits=12.9, luts=935, ffs=293, throughput_msps=93.6, max_abs_err=0.000127 (2^-12.95), power_index=1.48
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1263, accuracy_bits=13.3, luts=964, ffs=299, throughput_msps=93.6, max_abs_err=0.000102 (2^-13.26), power_index=1.52
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1321, accuracy_bits=13.6, luts=1008, ffs=313, throughput_msps=93.6, max_abs_err=8.04e-05 (2^-13.60), power_index=1.59
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1375, accuracy_bits=13.9, luts=1064, ffs=311, throughput_msps=93.6, max_abs_err=6.35e-05 (2^-13.94), power_index=1.66
- pipelined_m [data_width=19 n_iter=17 angle_guard=3 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1578, accuracy_bits=14.9, luts=1185, ffs=392, throughput_msps=93.6, max_abs_err=3.38e-05 (2^-14.85), power_index=1.9
- pipelined_m [data_width=26 n_iter=17 angle_guard=-1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1979, accuracy_bits=16, luts=1493, ffs=486, throughput_msps=86, max_abs_err=1.56e-05 (2^-15.97), power_index=2.38
- pipelined_m [data_width=24 n_iter=20 angle_guard=-1 frac_guard=3 rounding=round m=4] luts_plus_ffs=2186, accuracy_bits=17.9, luts=1718, ffs=468, throughput_msps=86, max_abs_err=4.19e-06 (2^-17.86), power_index=2.63
- pipelined_m [data_width=27 n_iter=23 angle_guard=-1 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=2937, accuracy_bits=20.4, luts=2138, ffs=799, throughput_msps=110, max_abs_err=7.31e-07 (2^-20.38), power_index=3.54
Front coverage: luts_plus_ffs 1121..2937 (HV reference 4000); accuracy_bits 12.2..20.4 (HV reference 12); data_width on the front 16..27 (registry 8..28).

Per family:
- pipelined: 48 evals, 28 feasible; max throughput seen 273 MSPS; best accuracy 13.60 bits; best feasible luts_plus_ffs=1665; feasible ranges: data_width 16..18, n_iter 14..19, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 152 evals, 92 feasible; max throughput seen 171 MSPS; best accuracy 25.06 bits; best feasible luts_plus_ffs=1121; feasible ranges: data_width 16..27, n_iter 14..30, angle_guard -2..3, frac_guard 0..4, m 2..5
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 9343 in, 3154 out
- provider-reported cost: $0.0060
- full prompts and replies: `llm_trace.jsonl`

