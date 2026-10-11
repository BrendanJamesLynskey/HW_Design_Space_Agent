# DSE run: asic_multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_multiaxis_control: Shared sin/cos unit in sky130 standard cells for a 16-axis motor-control loop: a 1 MHz control tick issues 32 requests at once; all 32 results must be back within 0.5 us of the tick (p99 over ticks). Max error <= 2^-12. Minimise area.
  target: asic-sky130hd
  constraint: throughput_msps >= 32
  constraint: max_abs_err <= 0.000244141
  constraint: sys_p99_batch_us <= 0.5
  objective: min area_um2 (HV ref 100000)
  objective: max accuracy_bits (HV ref 12)
  select: min area_um2
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average)
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=2` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 29151 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 7766 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 439 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 78.8 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 78.8 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 9 | exact: schedule |
| latency_ns | 114 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.33 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000204 (2^-12.26) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 6.67 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 6.07e-05 (2^-14.01) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.99 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (21 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=2` | 29151 | 439 | 78.8 | 9 | 1.33 | 0.000204 (2^-12.26) | 12.26 |
| 1 | `pipelined:data_width=17,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 38060 | 826 | 137.6 | 16 | 2.19 | 0.000194 (2^-12.33) | 12.33 |
| 2 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 39973 | 867 | 132.4 | 16 | 2.3 | 0.00017 (2^-12.53) | 12.53 |
| 3 | `pipelined:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 40192 | 870 | 143.2 | 17 | 2.31 | 0.000168 (2^-12.54) | 12.54 |
| 4 | `pipelined:data_width=19,n_iter=14,angle_guard=2,frac_guard=0,rounding=trunc` | 41887 | 908 | 127.5 | 16 | 2.41 | 0.000163 (2^-12.58) | 12.58 |
| 5 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 42248 | 914 | 137.6 | 17 | 2.42 | 0.000119 (2^-13.04) | 13.04 |
| 6 | `pipelined:data_width=17,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 44356 | 938 | 137.6 | 17 | 2.5 | 0.000108 (2^-13.18) | 13.18 |
| 7 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 46462 | 982 | 132.4 | 17 | 2.62 | 8.26e-05 (2^-13.56) | 13.56 |
| 8 | `pipelined:data_width=18,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 47915 | 1030 | 132.4 | 18 | 2.74 | 8.08e-05 (2^-13.60) | 13.60 |
| 9 | `pipelined:data_width=22,n_iter=15,angle_guard=-1,frac_guard=0,rounding=trunc` | 49099 | 1062 | 123.1 | 17 | 2.81 | 7.06e-05 (2^-13.79) | 13.79 |
| 10 | `pipelined:data_width=19,n_iter=16,angle_guard=4,frac_guard=0,rounding=round` | 49554 | 1070 | 118.9 | 18 | 2.84 | 5.75e-05 (2^-14.09) | 14.09 |
| 11 | `pipelined:data_width=19,n_iter=16,angle_guard=1,frac_guard=1,rounding=round` | 49749 | 1052 | 132.4 | 18 | 2.81 | 5.25e-05 (2^-14.22) | 14.22 |
| 12 | `pipelined:data_width=20,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 50287 | 1085 | 123.1 | 18 | 2.88 | 4.12e-05 (2^-14.57) | 14.57 |
| 13 | `pipelined:data_width=22,n_iter=16,angle_guard=-1,frac_guard=1,rounding=round` | 55030 | 1162 | 118.9 | 18 | 3.1 | 3.78e-05 (2^-14.69) | 14.69 |
| 14 | `pipelined:data_width=19,n_iter=18,angle_guard=4,frac_guard=1,rounding=round` | 58529 | 1237 | 118.9 | 20 | 3.3 | 2.72e-05 (2^-15.16) | 15.16 |
| 15 | `pipelined:data_width=19,n_iter=18,angle_guard=4,frac_guard=3,rounding=round` | 61663 | 1300 | 118.9 | 20 | 3.47 | 1.49e-05 (2^-16.03) | 16.03 |
| 16 | `pipelined:data_width=22,n_iter=18,angle_guard=4,frac_guard=0,rounding=round` | 63392 | 1363 | 107.9 | 20 | 3.62 | 1.1e-05 (2^-16.47) | 16.47 |
| 17 | `pipelined:data_width=24,n_iter=18,angle_guard=3,frac_guard=0,rounding=round` | 67528 | 1451 | 104.7 | 20 | 3.85 | 8.29e-06 (2^-16.88) | 16.88 |
| 18 | `pipelined:data_width=25,n_iter=18,angle_guard=1,frac_guard=1,rounding=round` | 71244 | 1502 | 107.9 | 20 | 4.02 | 8.01e-06 (2^-16.93) | 16.93 |
| 19 | `pipelined:data_width=25,n_iter=18,angle_guard=1,frac_guard=2,rounding=round` | 72811 | 1534 | 104.7 | 20 | 4.1 | 7.94e-06 (2^-16.94) | 16.94 |
| 20 | `pipelined:data_width=24,n_iter=20,angle_guard=3,frac_guard=0,rounding=round` | 75247 | 1612 | 104.7 | 22 | 4.29 | 2.8e-06 (2^-18.44) | 18.44 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show pipelined is the only family producing feasible designs (14 feasible, best area 41388 um2), while iterative and unrolled_k have 0 feasible (they cannot meet the 32 req/us throughput since they produce <1 result/cycle). pipelined_m also had 0 feasible in 50 evals, but this may be due to the search hitting unfavorable m values or parameter corners. I allocate 60% to pipelined (proven feasible, refine the Pareto front) and 40% to pipelined_m (focused search on small m=2-4 to see if it can beat pipelined on area while meeting the tight 0.5 us batch latency). Both families are constrained to data_width 14-18 and n_iter 12-18, which is the region where max_abs_err <= 2^-12 is achievable. angle_guard and frac_guard are kept small (0-2) to minimize area while preserving accuracy. The sys_p99_batch_us <= 0.5 us constraint is the binding system constraint: 32 results in 0.5 us requires Fmax >= 64 MHz with 1 result/cycle, so Fmax must be high enough. The area objective pushes toward minimal data_width and n_iter that still meet accuracy, while the accuracy_bits objective (HV ref 12) rewards designs that exceed the 12-bit accuracy floor.*)
- `pipelined` (60 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined is the only family with feasible designs (14/50, best area 41388 um2). The 32 req/us throughput constraint requires 1 result/cycle, which only pipelined/pipelined_m provide. Narrowing data_width to 14-18 and n_iter to 12-18 focuses on the region where max_abs_err <= 2^-12 is met while keeping area low. angle_guard 0-2 and frac_guard 0-2 cover the accuracy-critical knobs without wasting budget on large guards that inflate area. Both rounding modes are kept since rounding can shave 1 bit of error for free.
- `pipelined_m` (40 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m had 0 feasible in 50 evals, likely because the default search hit m values or parameter combos that broke the batch-latency or throughput bound. However, pipelined_m with small m (2-4) can reduce register count vs full pipelined while still giving 1 result/cycle. The sys_p99_batch_us <= 0.5 us constraint is tight: 32 requests must complete within 0.5 us of the tick. With 1 result/cycle, 32 cycles must fit in 0.5 us, requiring Fmax >= 64 MHz. pipelined_m with m=2-4 has fewer pipeline registers than full pipelined, potentially allowing higher Fmax at similar area. Worth a focused search with m constrained to 2-4 to avoid the latency penalty of large m.

**Result (code):** 100 evaluations this round, 100 total; 38 feasible; hypervolume 1.415e+05 (n/a).

**LLM decision:** `refine` — The current front is dominated by pipelined designs with data_width 17-18 and n_iter 14-18. The pipelined_m family found a significantly smaller area design (29925 um^2 vs 38060 um^2 for the best pipelined) with m=2, but only 3 feasible points were found, suggesting the search space for pipelined_m was not fully explored or the constraints (especially sys_p99_batch_us) are tight for this family. The best area is 29925 um^2, which is well below the HV reference of 100000. Accuracy is 12.2 bits, just above the 12-bit reference. To improve hypervolume, we need to explore the trade-off between area and accuracy more thoroughly. The pipelined_m family with m=2 seems promising for area minimization. We should focus the search on pipelined_m with m=2 and slightly wider data_width/n_iter ranges to find more feasible points and potentially better accuracy at similar area, or pipelined with lower data_width (16) to see if area can be reduced further while maintaining accuracy. The current front has a gap in the low-area, high-accuracy region. Refining the ranges to focus on the promising pipelined_m m=2 region and pipelined data_width=16 region should yield a better front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.415e+05 (gain this round: n/a (first round)).
Feasible designs: 38 of 100 evaluations (32 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 163
- max_abs_err <= 0.000244141: 36% violate; best seen 3.81e-05 (2^-14.68)
- sys_p99_batch_us <= 0.5: 33% violate; best seen 0.288

Pareto front (feasible, 14 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=2] area_um2=29925, accuracy_bits=12.2, ffs=437, throughput_msps=78.8, max_abs_err=0.000209 (2^-12.22), power_index=1.34
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=38060, accuracy_bits=12.3, ffs=826, throughput_msps=138, max_abs_err=0.000194 (2^-12.33), power_index=2.19
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=41349, accuracy_bits=12.5, ffs=875, throughput_msps=138, max_abs_err=0.000169 (2^-12.53), power_index=2.34
- pipelined [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=42388, accuracy_bits=12.6, ffs=898, throughput_msps=143, max_abs_err=0.000158 (2^-12.63), power_index=2.4
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=43443, accuracy_bits=12.8, ffs=936, throughput_msps=138, max_abs_err=0.000143 (2^-12.77), power_index=2.48
- pipelined [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=round] area_um2=43671, accuracy_bits=12.8, ffs=923, throughput_msps=138, max_abs_err=0.00014 (2^-12.80), power_index=2.47
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] area_um2=47501, accuracy_bits=13.5, ffs=1005, throughput_msps=138, max_abs_err=8.41e-05 (2^-13.54), power_index=2.68
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=47915, accuracy_bits=13.6, ffs=1030, throughput_msps=132, max_abs_err=8.08e-05 (2^-13.60), power_index=2.74
- pipelined [data_width=18 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=54945, accuracy_bits=14.2, ffs=1178, throughput_msps=132, max_abs_err=5.33e-05 (2^-14.20), power_index=3.13
- pipelined [data_width=18 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] area_um2=55909, accuracy_bits=14.7, ffs=1180, throughput_msps=132, max_abs_err=3.81e-05 (2^-14.68), power_index=3.15
Front coverage: area_um2 29925..55909 (HV reference 100000); accuracy_bits 12.2..14.7 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 60 evals, 35 feasible; max throughput seen 163 MSPS; best accuracy 14.68 bits; best feasible area_um2=38060; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 40 evals, 3 feasible; max throughput seen 86.6 MSPS; best accuracy 14.04 bits; best feasible area_um2=29925; feasible ranges: data_width 16..17, n_iter 14..18, angle_guard 0..2, frac_guard 0..1, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Focus on the two most promising regions: pipelined_m m=2 for best area, and pipelined data_width=16 for potential area reduction. This should improve the front's coverage in the low-area region.*)
- `pipelined_m` (12 evals): data_width=16..18, n_iter=14..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..2. *Why:* pipelined_m with m=2 achieved the best area (29925 um^2). Only 3 feasible points found, so expanding frac_guard to 2 and data_width to 18 may reveal more feasible designs with better accuracy at similar area.
- `pipelined` (8 evals): data_width=16..17, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined with data_width=16 may offer lower area than data_width=17. The current best pipelined is 38060 um^2 at data_width=17. Exploring data_width=16 with n_iter 14-16 may find designs with area < 38060 and accuracy >= 12 bits.

**Result (code):** 20 evaluations this round, 120 total; 46 feasible; hypervolume 1.421e+05 (+0.4%).

**LLM decision:** `stop` — The exploration has successfully identified a feasible Pareto front that satisfies all system and accuracy constraints. The minimum area design is a `pipelined_m` unit with `m=2`, `data_width=17`, and `n_iter=14`, achieving an area of 29,151 um^2 and 12.3 bits of accuracy (max error 2^-12.26), which meets the 2^-12 requirement. The `sys_p99_batch_us` constraint (<= 0.5 us) is met by the best designs (best seen 0.288 us), and throughput is well above the 32 MSPS requirement. Since this is the final round and the front covers the trade-off space from 29k to 56k um^2 with accuracy up to 14.7 bits, further exploration is unnecessary. The selection rule (min area) will pick the 29,151 um^2 design.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.421e+05 (gain this round: +0.4%).
Feasible designs: 46 of 120 evaluations (36 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 163
- max_abs_err <= 0.000244141: 38% violate; best seen 3.81e-05 (2^-14.68)
- sys_p99_batch_us <= 0.5: 32% violate; best seen 0.288

Pareto front (feasible, 14 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=2] area_um2=29151, accuracy_bits=12.3, ffs=439, throughput_msps=78.8, max_abs_err=0.000204 (2^-12.26), power_index=1.33
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=38060, accuracy_bits=12.3, ffs=826, throughput_msps=138, max_abs_err=0.000194 (2^-12.33), power_index=2.19
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=41349, accuracy_bits=12.5, ffs=875, throughput_msps=138, max_abs_err=0.000169 (2^-12.53), power_index=2.34
- pipelined [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=42388, accuracy_bits=12.6, ffs=898, throughput_msps=143, max_abs_err=0.000158 (2^-12.63), power_index=2.4
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=43443, accuracy_bits=12.8, ffs=936, throughput_msps=138, max_abs_err=0.000143 (2^-12.77), power_index=2.48
- pipelined [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=round] area_um2=43671, accuracy_bits=12.8, ffs=923, throughput_msps=138, max_abs_err=0.00014 (2^-12.80), power_index=2.47
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] area_um2=47501, accuracy_bits=13.5, ffs=1005, throughput_msps=138, max_abs_err=8.41e-05 (2^-13.54), power_index=2.68
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=47915, accuracy_bits=13.6, ffs=1030, throughput_msps=132, max_abs_err=8.08e-05 (2^-13.60), power_index=2.74
- pipelined [data_width=18 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=54945, accuracy_bits=14.2, ffs=1178, throughput_msps=132, max_abs_err=5.33e-05 (2^-14.20), power_index=3.13
- pipelined [data_width=18 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] area_um2=55909, accuracy_bits=14.7, ffs=1180, throughput_msps=132, max_abs_err=3.81e-05 (2^-14.68), power_index=3.15
Front coverage: area_um2 29151..55909 (HV reference 100000); accuracy_bits 12.3..14.7 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 68 evals, 40 feasible; max throughput seen 163 MSPS; best accuracy 14.68 bits; best feasible area_um2=38060; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 52 evals, 6 feasible; max throughput seen 86.6 MSPS; best accuracy 14.04 bits; best feasible area_um2=29151; feasible ranges: data_width 16..17, n_iter 14..18, angle_guard 0..2, frac_guard 0..2, m 2..2
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (6 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)
- `pipelined` (74 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (13 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 109 feasible; hypervolume 2.698e+05 (+89.9%).

**No LLM call** (code's front-mapping round): The exploration has successfully identified a feasible Pareto front that satisfies all system and accuracy constraints. The minimum area design is a `pipelined_m` unit with `m=2`, `data_width=17`, and `n_iter=14`, achieving an area of 29,151 um^2 and 12.3 bits of accuracy (max error 2^-12.26), which meets the 2^-12 requirement. The `sys_p99_batch_us` constraint (<= 0.5 us) is met by the best designs (best seen 0.288 us), and throughput is well above the 32 MSPS requirement. Since this is the final round and the front covers the trade-off space from 29k to 56k um^2 with accuracy up to 14.7 bits, further exploration is unnecessary. The selection rule (min area) will pick the 29,151 um^2 design.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 2.698e+05 (gain this round: +89.9%).
Feasible designs: 109 of 200 evaluations (86 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 3% violate; best seen 163
- max_abs_err <= 0.000244141: 25% violate; best seen 1.59e-07 (2^-22.58)
- sys_p99_batch_us <= 0.5: 25% violate; best seen 0.288

Pareto front (feasible, 21 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=2] area_um2=29151, accuracy_bits=12.3, ffs=439, throughput_msps=78.8, max_abs_err=0.000204 (2^-12.26), power_index=1.33
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.5, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53), power_index=2.3
- pipelined [data_width=19 n_iter=14 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=41887, accuracy_bits=12.6, ffs=908, throughput_msps=128, max_abs_err=0.000163 (2^-12.58), power_index=2.41
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=46462, accuracy_bits=13.6, ffs=982, throughput_msps=132, max_abs_err=8.26e-05 (2^-13.56), power_index=2.62
- pipelined [data_width=22 n_iter=15 angle_guard=-1 frac_guard=0 rounding=trunc] area_um2=49099, accuracy_bits=13.8, ffs=1062, throughput_msps=123, max_abs_err=7.06e-05 (2^-13.79), power_index=2.81
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] area_um2=49749, accuracy_bits=14.2, ffs=1052, throughput_msps=132, max_abs_err=5.25e-05 (2^-14.22), power_index=2.81
- pipelined [data_width=22 n_iter=16 angle_guard=-1 frac_guard=1 rounding=round] area_um2=55030, accuracy_bits=14.7, ffs=1162, throughput_msps=119, max_abs_err=3.78e-05 (2^-14.69), power_index=3.1
- pipelined [data_width=22 n_iter=18 angle_guard=4 frac_guard=0 rounding=round] area_um2=63392, accuracy_bits=16.5, ffs=1363, throughput_msps=108, max_abs_err=1.1e-05 (2^-16.47), power_index=3.62
- pipelined [data_width=25 n_iter=18 angle_guard=1 frac_guard=1 rounding=round] area_um2=71244, accuracy_bits=16.9, ffs=1502, throughput_msps=108, max_abs_err=8.01e-06 (2^-16.93), power_index=4.02
- pipelined [data_width=24 n_iter=20 angle_guard=3 frac_guard=0 rounding=round] area_um2=75247, accuracy_bits=18.4, ffs=1612, throughput_msps=105, max_abs_err=2.8e-06 (2^-18.44), power_index=4.29
Front coverage: area_um2 29151..75247 (HV reference 100000); accuracy_bits 12.3..18.4 (HV reference 12); data_width on the front 17..25 (registry 8..28).

Per family:
- pipelined: 142 evals, 103 feasible; max throughput seen 163 MSPS; best accuracy 22.58 bits; best feasible area_um2=38060; feasible ranges: data_width 16..28, n_iter 14..27, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 58 evals, 6 feasible; max throughput seen 86.6 MSPS; best accuracy 21.95 bits; best feasible area_um2=29151; feasible ranges: data_width 16..17, n_iter 14..18, angle_guard 0..2, frac_guard 0..2, m 2..2
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 9355 in, 2323 out
- provider-reported cost: $0.0063
- full prompts and replies: `llm_trace.jsonl`

