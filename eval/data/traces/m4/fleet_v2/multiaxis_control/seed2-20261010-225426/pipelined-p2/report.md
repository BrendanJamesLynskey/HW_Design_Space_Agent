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
`pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 827 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 282 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 61.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.34 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.0002 (2^-12.28) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 13.1 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.41e-05 (2^-14.17) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.55 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (21 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=4` | 827 | 282 | 97.8 | 6 | 1.34 | 0.0002 (2^-12.28) | 12.28 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=4` | 841 | 287 | 93.6 | 6 | 1.36 | 0.000175 (2^-12.48) | 12.48 |
| 2 | `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=0,rounding=round,m=4` | 890 | 282 | 97.8 | 6 | 1.41 | 0.000145 (2^-12.75) | 12.75 |
| 3 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=4` | 920 | 291 | 93.6 | 6 | 1.46 | 0.000109 (2^-13.17) | 13.17 |
| 4 | `pipelined_m:data_width=19,n_iter=15,angle_guard=0,frac_guard=0,rounding=round,m=4` | 935 | 297 | 93.6 | 6 | 1.48 | 0.000108 (2^-13.18) | 13.18 |
| 5 | `pipelined_m:data_width=19,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=4` | 964 | 305 | 93.6 | 6 | 1.53 | 8.33e-05 (2^-13.55) | 13.55 |
| 6 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1048 | 303 | 93.6 | 6 | 1.63 | 6.86e-05 (2^-13.83) | 13.83 |
| 7 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1055 | 299 | 93.6 | 6 | 1.63 | 6.45e-05 (2^-13.92) | 13.92 |
| 8 | `pipelined_m:data_width=18,n_iter=17,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1122 | 364 | 93.6 | 7 | 1.79 | 5.64e-05 (2^-14.11) | 14.11 |
| 9 | `pipelined_m:data_width=27,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=4` | 1412 | 418 | 86.0 | 6 | 2.2 | 3.06e-05 (2^-15.00) | 15.00 |
| 10 | `pipelined_m:data_width=27,n_iter=16,angle_guard=0,frac_guard=2,rounding=round,m=4` | 1501 | 424 | 86.0 | 6 | 2.32 | 3.05e-05 (2^-15.00) | 15.00 |
| 11 | `pipelined_m:data_width=24,n_iter=19,angle_guard=1,frac_guard=0,rounding=round,m=4` | 1504 | 452 | 89.6 | 7 | 2.35 | 4.72e-06 (2^-17.69) | 17.69 |
| 12 | `pipelined_m:data_width=27,n_iter=19,angle_guard=1,frac_guard=0,rounding=round,m=4` | 1674 | 503 | 86.0 | 7 | 2.62 | 3.96e-06 (2^-17.95) | 17.95 |
| 13 | `pipelined_m:data_width=23,n_iter=22,angle_guard=3,frac_guard=1,rounding=round,m=3` | 1824 | 700 | 114.5 | 10 | 3.04 | 1.84e-06 (2^-19.05) | 19.05 |
| 14 | `pipelined_m:data_width=24,n_iter=22,angle_guard=3,frac_guard=1,rounding=round,m=3` | 1893 | 726 | 110.0 | 10 | 3.15 | 1.23e-06 (2^-19.63) | 19.63 |
| 15 | `pipelined_m:data_width=24,n_iter=23,angle_guard=3,frac_guard=1,rounding=round,m=3` | 1980 | 726 | 110.0 | 10 | 3.26 | 9.9e-07 (2^-19.95) | 19.95 |
| 16 | `pipelined_m:data_width=27,n_iter=23,angle_guard=0,frac_guard=0,rounding=round,m=3` | 2022 | 765 | 110.0 | 10 | 3.35 | 4.81e-07 (2^-20.99) | 20.99 |
| 17 | `pipelined_m:data_width=27,n_iter=23,angle_guard=0,frac_guard=1,rounding=round,m=3` | 2125 | 781 | 110.0 | 10 | 3.5 | 4.51e-07 (2^-21.08) | 21.08 |
| 18 | `pipelined_m:data_width=27,n_iter=23,angle_guard=2,frac_guard=1,rounding=trunc,m=3` | 2115 | 795 | 110.0 | 10 | 3.5 | 4.08e-07 (2^-21.22) | 21.22 |
| 19 | `pipelined_m:data_width=27,n_iter=23,angle_guard=1,frac_guard=3,rounding=round,m=3` | 2241 | 817 | 110.0 | 10 | 3.68 | 3.28e-07 (2^-21.54) | 21.54 |
| 20 | `pipelined_m:data_width=27,n_iter=26,angle_guard=3,frac_guard=1,rounding=round,m=3` | 2486 | 899 | 110.0 | 11 | 4.07 | 1.29e-07 (2^-22.88) | 22.88 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show that only pipelined and pipelined_m are feasible, with pipelined_m dominating the merged front (13/13 designs). The previous searches were too broad. I am now focusing the budget on the specific region where max_abs_err <= 2^-12 is satisfied (W=14-18, N=12-16) and optimizing the area/latency trade-off. I will fix rounding to 'round' to ensure accuracy_bits is maximized for the hypervolume objective, and I will explore m=2-4 for pipelined_m to find the sweet spot between area and the 32 MSPS throughput constraint. I am also including pipelined (m=1) to ensure the front is well-mapped at the high-Fmax end, which is important for the system-level latency constraints.*)
- `pipelined_m` (50 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..1, rounding=round, m=2..4. *Why:* pipelined_m is the only family with feasible designs (best 1256 luts+ffs) and owns the entire merged front. I am narrowing the search to the region where accuracy_bits >= 12 is met (W=14-18, N=12-16) and m=2-4 to balance area against the 32 MSPS throughput constraint, while fixing rounding to 'round' to maximize accuracy_bits for the hypervolume.
- `pipelined` (50 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..1, rounding=round. *Why:* pipelined is the fully registered baseline (m=1). While pipelined_m is more area-efficient, pipelined may offer higher Fmax which could be critical for the sys_p99_batch_us constraint if the system simulation reveals timing issues. I am exploring the same accuracy-feasible box to map the trade-off between area and timing/latency.

**Result (code):** 100 evaluations this round, 100 total; 67 feasible; hypervolume 5299 (n/a).

**LLM decision:** `refine` — The current front is dominated by `pipelined_m` with `m=4`, which offers the best area (1110 LUTs+FFs) while meeting the strict 32 MSPS throughput and 0.44us batch latency constraints. The `pipelined` family is significantly more expensive (min 1633) and does not appear on the Pareto front. The accuracy constraint (max_abs_err <= 2^-12) is the binding constraint, with 33% of evaluations failing it. The current front spans accuracy_bits 12.3 to 13.9, which is a good range, but the area range is narrow (1110-1353). To improve hypervolume, we should focus the search on the `pipelined_m` family with `m=4` (which seems optimal for area/latency trade-off in this bursty scenario) and slightly widen the `n_iter` and `angle_guard` ranges to ensure we capture the full accuracy-area trade-off curve without wasting evaluations on `m=2` or `m=3` which likely have higher area or worse latency for this specific burst size. We will narrow `m` to 4 to focus the budget, and keep `data_width` around 17-18 as wider widths increase area without necessarily improving accuracy bits significantly beyond the constraint.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 5299 (gain this round: n/a (first round)).
Feasible designs: 67 of 100 evaluations (30 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 33% violate; best seen 6.45e-05 (2^-13.92)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.161

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1110, accuracy_bits=12.3, luts=827, ffs=282, throughput_msps=97.8, max_abs_err=0.0002 (2^-12.28), power_index=1.34
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=1183, accuracy_bits=12.4, luts=893, ffs=291, throughput_msps=93.6, max_abs_err=0.000179 (2^-12.45), power_index=1.42
- pipelined_m [data_width=17 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1194, accuracy_bits=12.7, luts=922, ffs=272, throughput_msps=97.8, max_abs_err=0.000149 (2^-12.71), power_index=1.44
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1236, accuracy_bits=13, luts=954, ffs=282, throughput_msps=97.8, max_abs_err=0.000121 (2^-13.02), power_index=1.49
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1276, accuracy_bits=13.5, luts=985, ffs=291, throughput_msps=93.6, max_abs_err=8.35e-05 (2^-13.55), power_index=1.54
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1353, accuracy_bits=13.9, luts=1055, ffs=299, throughput_msps=93.6, max_abs_err=6.45e-05 (2^-13.92), power_index=1.63
Front coverage: luts_plus_ffs 1110..1353 (HV reference 4000); accuracy_bits 12.3..13.9 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 50 evals, 34 feasible; max throughput seen 273 MSPS; best accuracy 13.54 bits; best feasible luts_plus_ffs=1633; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..1
- pipelined_m: 50 evals, 33 feasible; max throughput seen 178 MSPS; best accuracy 13.92 bits; best feasible luts_plus_ffs=1110; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..1, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Refining to the most promising sub-space to maximize hypervolume gain per evaluation.*)
- `pipelined_m` (20 evals): data_width=17..19, n_iter=13..17, angle_guard=0..2, frac_guard=0..1, rounding=round, m=4..4. *Why:* Focus on the best-performing family and pipeline depth (m=4) to refine the Pareto front in the area-accuracy space. m=4 provides the best area efficiency for the 32-request burst while maintaining low latency. Rounding is fixed to 'round' as it generally provides better accuracy for the same area or better area for the same accuracy compared to truncation in CORDIC.

**Result (code):** 20 evaluations this round, 120 total; 85 feasible; hypervolume 5814 (+9.7%).

**LLM decision:** `stop` — The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 1110 LUTs+FFs) meets all constraints: throughput 97.8 MSPS >= 32, max_abs_err 2^-12.28 <= 2^-12, and sys_p99_batch_us 0.161 <= 0.44. The front spans a useful trade-off range (1110-1486 area, 12.3-14.1 accuracy bits) with 8 distinct designs. Since this is the final round, the code will proceed to L2 simulation of the shortlist to re-select among designs that pass the system constraints. The selection rule (min luts_plus_ffs) will likely pick the 1110 design, which has significant margin on all constraints.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 5814 (gain this round: +9.7%).
Feasible designs: 85 of 120 evaluations (36 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 29% violate; best seen 5.64e-05 (2^-14.11)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.161

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1110, accuracy_bits=12.3, luts=827, ffs=282, throughput_msps=97.8, max_abs_err=0.0002 (2^-12.28), power_index=1.34
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1127, accuracy_bits=12.5, luts=841, ffs=287, throughput_msps=93.6, max_abs_err=0.000175 (2^-12.48), power_index=1.36
- pipelined_m [data_width=17 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1194, accuracy_bits=12.7, luts=922, ffs=272, throughput_msps=97.8, max_abs_err=0.000149 (2^-12.71), power_index=1.44
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1210, accuracy_bits=13.2, luts=920, ffs=291, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=1.46
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=1.51
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1276, accuracy_bits=13.5, luts=985, ffs=291, throughput_msps=93.6, max_abs_err=8.35e-05 (2^-13.55), power_index=1.54
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1353, accuracy_bits=13.9, luts=1055, ffs=299, throughput_msps=93.6, max_abs_err=6.45e-05 (2^-13.92), power_index=1.63
- pipelined_m [data_width=18 n_iter=17 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1486, accuracy_bits=14.1, luts=1122, ffs=364, throughput_msps=93.6, max_abs_err=5.64e-05 (2^-14.11), power_index=1.79
Front coverage: luts_plus_ffs 1110..1486 (HV reference 4000); accuracy_bits 12.3..14.1 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 50 evals, 34 feasible; max throughput seen 273 MSPS; best accuracy 13.54 bits; best feasible luts_plus_ffs=1633; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..1
- pipelined_m: 70 evals, 51 feasible; max throughput seen 178 MSPS; best accuracy 14.11 bits; best feasible luts_plus_ffs=1110; feasible ranges: data_width 17..18, n_iter 14..17, angle_guard 0..2, frac_guard 0..1, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (80 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (8 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 147 feasible; hypervolume 1.92e+04 (+230.2%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 1110 LUTs+FFs) meets all constraints: throughput 97.8 MSPS >= 32, max_abs_err 2^-12.28 <= 2^-12, and sys_p99_batch_us 0.161 <= 0.44. The front spans a useful trade-off range (1110-1486 area, 12.3-14.1 accuracy bits) with 8 distinct designs. Since this is the final round, the code will proceed to L2 simulation of the shortlist to re-select among designs that pass the system constraints. The selection rule (min luts_plus_ffs) will likely pick the 1110 design, which has significant margin on all constraints.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.92e+04 (gain this round: +230.2%).
Feasible designs: 147 of 200 evaluations (95 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 18% violate; best seen 8.75e-08 (2^-23.45)
- sys_p99_batch_us <= 0.44: 8% violate; best seen 0.161

Pareto front (feasible, 21 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1110, accuracy_bits=12.3, luts=827, ffs=282, throughput_msps=97.8, max_abs_err=0.0002 (2^-12.28), power_index=1.34
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1173, accuracy_bits=12.8, luts=890, ffs=282, throughput_msps=97.8, max_abs_err=0.000145 (2^-12.75), power_index=1.41
- pipelined_m [data_width=19 n_iter=15 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1231, accuracy_bits=13.2, luts=935, ffs=297, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=1.48
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1353, accuracy_bits=13.9, luts=1055, ffs=299, throughput_msps=93.6, max_abs_err=6.45e-05 (2^-13.92), power_index=1.63
- pipelined_m [data_width=27 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1830, accuracy_bits=15, luts=1412, ffs=418, throughput_msps=86, max_abs_err=3.06e-05 (2^-15.00), power_index=2.2
- pipelined_m [data_width=24 n_iter=19 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1956, accuracy_bits=17.7, luts=1504, ffs=452, throughput_msps=89.6, max_abs_err=4.72e-06 (2^-17.69), power_index=2.35
- pipelined_m [data_width=23 n_iter=22 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=2524, accuracy_bits=19, luts=1824, ffs=700, throughput_msps=114, max_abs_err=1.84e-06 (2^-19.05), power_index=3.04
- pipelined_m [data_width=27 n_iter=23 angle_guard=0 frac_guard=0 rounding=round m=3] luts_plus_ffs=2787, accuracy_bits=21, luts=2022, ffs=765, throughput_msps=110, max_abs_err=4.81e-07 (2^-20.99), power_index=3.35
- pipelined_m [data_width=27 n_iter=23 angle_guard=2 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=2910, accuracy_bits=21.2, luts=2115, ffs=795, throughput_msps=110, max_abs_err=4.08e-07 (2^-21.22), power_index=3.5
- pipelined_m [data_width=27 n_iter=26 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=3385, accuracy_bits=22.9, luts=2486, ffs=899, throughput_msps=110, max_abs_err=1.29e-07 (2^-22.88), power_index=4.07
Front coverage: luts_plus_ffs 1110..3385 (HV reference 4000); accuracy_bits 12.3..22.9 (HV reference 12); data_width on the front 18..27 (registry 8..28).

Per family:
- pipelined: 50 evals, 34 feasible; max throughput seen 273 MSPS; best accuracy 13.54 bits; best feasible luts_plus_ffs=1633; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..1
- pipelined_m: 150 evals, 113 feasible; max throughput seen 178 MSPS; best accuracy 23.45 bits; best feasible luts_plus_ffs=1110; feasible ranges: data_width 17..27, n_iter 13..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 9302 in, 1844 out
- provider-reported cost: $0.0053
- full prompts and replies: `llm_trace.jsonl`

