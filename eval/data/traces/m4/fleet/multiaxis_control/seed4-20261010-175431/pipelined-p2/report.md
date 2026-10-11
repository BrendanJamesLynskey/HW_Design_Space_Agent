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
`pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=3,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 855 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 280 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.37 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000217 (2^-12.17) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.56 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 6.18e-05 (2^-13.98) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 1.01 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.2 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (17 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=3,rounding=trunc,m=4` | 855 | 280 | 93.6 | 6 | 1.37 | 0.000217 (2^-12.17) | 12.17 |
| 1 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=3,rounding=round,m=4` | 888 | 282 | 93.6 | 6 | 1.41 | 0.000187 (2^-12.38) | 12.38 |
| 2 | `pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=3,rounding=trunc,m=4` | 920 | 280 | 93.6 | 6 | 1.44 | 0.000187 (2^-12.39) | 12.39 |
| 3 | `pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=2,rounding=round,m=4` | 924 | 276 | 97.8 | 6 | 1.45 | 0.000176 (2^-12.48) | 12.48 |
| 4 | `pipelined_m:data_width=16,n_iter=15,angle_guard=4,frac_guard=2,rounding=round,m=4` | 954 | 285 | 93.6 | 6 | 1.49 | 0.000135 (2^-12.86) | 12.86 |
| 5 | `pipelined_m:data_width=16,n_iter=16,angle_guard=4,frac_guard=2,rounding=round,m=4` | 1019 | 285 | 93.6 | 6 | 1.57 | 0.000109 (2^-13.17) | 13.17 |
| 6 | `pipelined_m:data_width=16,n_iter=16,angle_guard=4,frac_guard=3,rounding=round,m=4` | 1051 | 291 | 93.6 | 6 | 1.61 | 7.92e-05 (2^-13.63) | 13.63 |
| 7 | `pipelined_m:data_width=22,n_iter=15,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 1126 | 427 | 114.5 | 7 | 1.87 | 7.4e-05 (2^-13.72) | 13.72 |
| 8 | `pipelined_m:data_width=21,n_iter=20,angle_guard=-2,frac_guard=0,rounding=round,m=3` | 1347 | 523 | 119.3 | 9 | 2.25 | 5.11e-05 (2^-14.26) | 14.26 |
| 9 | `pipelined_m:data_width=22,n_iter=20,angle_guard=1,frac_guard=0,rounding=trunc,m=3` | 1467 | 567 | 114.5 | 9 | 2.45 | 1.22e-05 (2^-16.32) | 16.32 |
| 10 | `pipelined_m:data_width=22,n_iter=20,angle_guard=1,frac_guard=3,rounding=round,m=4` | 1633 | 444 | 89.6 | 7 | 2.5 | 4.49e-06 (2^-17.77) | 17.77 |
| 11 | `pipelined_m:data_width=22,n_iter=20,angle_guard=2,frac_guard=4,rounding=round,m=4` | 1693 | 457 | 89.6 | 7 | 2.59 | 3.57e-06 (2^-18.10) | 18.10 |
| 12 | `pipelined_m:data_width=25,n_iter=20,angle_guard=3,frac_guard=2,rounding=round,m=3` | 1820 | 677 | 110.0 | 9 | 3.01 | 2.08e-06 (2^-18.88) | 18.88 |
| 13 | `pipelined_m:data_width=27,n_iter=20,angle_guard=3,frac_guard=0,rounding=round,m=3` | 1807 | 697 | 110.0 | 9 | 3.01 | 1.99e-06 (2^-18.94) | 18.94 |
| 14 | `pipelined_m:data_width=27,n_iter=22,angle_guard=-2,frac_guard=4,rounding=round,m=2` | 2120 | 1092 | 147.4 | 13 | 3.87 | 1.24e-06 (2^-19.62) | 19.62 |
| 15 | `pipelined_m:data_width=28,n_iter=22,angle_guard=-2,frac_guard=4,rounding=round,m=2` | 2189 | 1127 | 147.4 | 13 | 3.99 | 9.18e-07 (2^-20.05) | 20.05 |
| 16 | `pipelined_m:data_width=27,n_iter=29,angle_guard=3,frac_guard=0,rounding=round,m=3` | 2661 | 973 | 110.0 | 12 | 4.37 | 2.03e-07 (2^-22.23) | 22.23 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires throughput >= 32 Msps and sys_p99_batch_us <= 0.44us for 32 burst requests. pipelined_m dominates the current front with 10/14 designs and best area 1449, so it gets 60% of the budget. pipelined gets 40% to explore whether its higher Fmax (shorter combinational paths) helps meet the tight 0.44us batch latency constraint, even at higher area. Both families are constrained to data_width 14..16 (W>=14 needed for 2^-12 accuracy) and n_iter 12..16 (sufficient for accuracy with moderate guards). frac_guard and angle_guard ranges cover the full accuracy/area trade-off. The system constraint (32 results in 0.44us) is the binding constraint: for pipelined_m with m=2, latency is ceil(N/2)+2 cycles, and 32 results take 32 cycles (1/cycle throughput), so total time is 32/Fmax us <= 0.44us requires Fmax >= 72.7 MHz. For m=4, latency is ceil(N/4)+2, but throughput is still 1/cycle, so the same Fmax requirement applies. The key trade-off is area (more registers for smaller m) vs Fmax (shorter paths for smaller m).*)
- `pipelined_m` (60 evals): data_width=14..16, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* pipelined_m dominates the current merged front (10 of 14 designs) and has the best feasible area (1449). The constraint max_abs_err <= 2^-12 requires data_width >= 14 (since output LSB is 2^-(W-2), W=14 gives LSB=2^-12). n_iter must be >= 12 to meet accuracy with reasonable guards. m=2..4 balances area (fewer registers) against Fmax (shorter combinational paths). frac_guard 0..4 and angle_guard -2..4 cover the accuracy/area trade-off. Focusing n_iter 12..16 and data_width 14..16 keeps the search in the feasible region while exploring the Pareto trade-off between area and accuracy_bits.
- `pipelined` (40 evals): data_width=14..16, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* pipelined has 4 of 14 front designs and best feasible area 2398, which is worse than pipelined_m's 1449. However, pipelined (m=1) may offer higher Fmax due to shorter per-stage paths, which could help with the sys_p99_batch_us <= 0.44us constraint (32 results in 0.44us requires ~73 MHz for pipelined_m with m=2, or higher for larger m). Keeping a smaller share here to explore whether pipelined's higher Fmax compensates for its larger area, particularly at the accuracy/area trade-off extremes.

**Result (code):** 100 evaluations this round, 100 total; 30 feasible; hypervolume 4439 (n/a).

**LLM decision:** `refine` — The current front is dominated by pipelined_m with m=4, but the feasible range for m is 2..4. Since pipelined_m with smaller m (2 or 3) has lower latency (ceil(N/m)+2) and potentially lower area (fewer registers), it could offer a better trade-off for the sys_p99_batch_us constraint (0.44 us) while maintaining throughput. The current best luts_plus_ffs is 1165, but we haven't explored m=2 or m=3 in detail. Also, data_width=15 was seen in feasible ranges but not on the front; reducing data_width to 15 might reduce area if accuracy is still sufficient. The accuracy constraint is max_abs_err <= 2^-12 (0.000244), and the best feasible design has 12.02 bits, which is just above the limit. We need to ensure accuracy while minimizing area. Refining to focus on pipelined_m with m in {2,3,4}, data_width in {15,16}, n_iter in {14,15,16}, angle_guard in {2,3,4}, frac_guard in {1,2,3}, and rounding in {trunc, round} should help find a better front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 4439 (gain this round: n/a (first round)).
Feasible designs: 30 of 100 evaluations (23 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 70% violate; best seen 7.92e-05 (2^-13.63)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.161

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1165, accuracy_bits=12, luts=890, ffs=274, throughput_msps=97.8, max_abs_err=0.000241 (2^-12.02), power_index=1.4
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1201, accuracy_bits=12.5, luts=924, ffs=276, throughput_msps=97.8, max_abs_err=0.000176 (2^-12.48), power_index=1.45
- pipelined_m [data_width=16 n_iter=15 angle_guard=4 frac_guard=2 rounding=round m=4] luts_plus_ffs=1238, accuracy_bits=12.9, luts=954, ffs=285, throughput_msps=93.6, max_abs_err=0.000135 (2^-12.86), power_index=1.49
- pipelined_m [data_width=16 n_iter=16 angle_guard=4 frac_guard=2 rounding=round m=4] luts_plus_ffs=1303, accuracy_bits=13.2, luts=1019, ffs=285, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=1.57
- pipelined_m [data_width=16 n_iter=16 angle_guard=4 frac_guard=3 rounding=round m=4] luts_plus_ffs=1341, accuracy_bits=13.6, luts=1051, ffs=291, throughput_msps=93.6, max_abs_err=7.92e-05 (2^-13.63), power_index=1.61
Front coverage: luts_plus_ffs 1165..1341 (HV reference 4000); accuracy_bits 12..13.6 (HV reference 12); data_width on the front 16..16 (registry 8..28).

Per family:
- pipelined: 40 evals, 10 feasible; max throughput seen 273 MSPS; best accuracy 12.63 bits; best feasible luts_plus_ffs=1721; feasible ranges: data_width 15..16, n_iter 14..16, angle_guard 2..4, frac_guard 1..3
- pipelined_m: 60 evals, 20 feasible; max throughput seen 171 MSPS; best accuracy 13.63 bits; best feasible luts_plus_ffs=1165; feasible ranges: data_width 15..16, n_iter 14..16, angle_guard 1..4, frac_guard 1..4, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Refine to explore pipelined_m with m=2,3 which may offer better area/latency trade-offs, and data_width=15 for potential area reduction.*)
- `pipelined_m` (20 evals): data_width=15..16, n_iter=14..16, angle_guard=2..4, frac_guard=1..3, rounding=trunc|round, m=2..4. *Why:* Focus on pipelined_m with smaller m values (2,3) to reduce latency and potentially area, while maintaining accuracy and throughput. Data_width 15 may reduce area if accuracy allows.

**Result (code):** 20 evaluations this round, 120 total; 38 feasible; hypervolume 4456 (+0.4%).

**LLM decision:** `stop` — The front is well-mapped and feasible. The minimum area design (1135 LUTs+FFs) meets all constraints: throughput 93.6 MSPS (>=32), max_abs_err 0.000217 (<=0.000244), and sys_p99_batch_us 0.161 us (<=0.44 us). The front spans accuracy_bits 12.2 to 13.6, covering the requirement (>=12 bits) with margin. Hypervolume gain in the last round was only +0.4%, indicating convergence. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (1135) from the front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 4456 (gain this round: +0.4%).
Feasible designs: 38 of 120 evaluations (28 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 68% violate; best seen 7.92e-05 (2^-13.63)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.161

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1135, accuracy_bits=12.2, luts=855, ffs=280, throughput_msps=93.6, max_abs_err=0.000217 (2^-12.17), power_index=1.37
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=3 rounding=round m=4] luts_plus_ffs=1171, accuracy_bits=12.4, luts=888, ffs=282, throughput_msps=93.6, max_abs_err=0.000187 (2^-12.38), power_index=1.41
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1200, accuracy_bits=12.4, luts=920, ffs=280, throughput_msps=93.6, max_abs_err=0.000187 (2^-12.39), power_index=1.44
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1201, accuracy_bits=12.5, luts=924, ffs=276, throughput_msps=97.8, max_abs_err=0.000176 (2^-12.48), power_index=1.45
- pipelined_m [data_width=16 n_iter=15 angle_guard=4 frac_guard=2 rounding=round m=4] luts_plus_ffs=1238, accuracy_bits=12.9, luts=954, ffs=285, throughput_msps=93.6, max_abs_err=0.000135 (2^-12.86), power_index=1.49
- pipelined_m [data_width=16 n_iter=16 angle_guard=4 frac_guard=2 rounding=round m=4] luts_plus_ffs=1303, accuracy_bits=13.2, luts=1019, ffs=285, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=1.57
- pipelined_m [data_width=16 n_iter=16 angle_guard=4 frac_guard=3 rounding=round m=4] luts_plus_ffs=1341, accuracy_bits=13.6, luts=1051, ffs=291, throughput_msps=93.6, max_abs_err=7.92e-05 (2^-13.63), power_index=1.61
Front coverage: luts_plus_ffs 1135..1341 (HV reference 4000); accuracy_bits 12.2..13.6 (HV reference 12); data_width on the front 16..16 (registry 8..28).

Per family:
- pipelined: 40 evals, 10 feasible; max throughput seen 273 MSPS; best accuracy 12.63 bits; best feasible luts_plus_ffs=1721; feasible ranges: data_width 15..16, n_iter 14..16, angle_guard 2..4, frac_guard 1..3
- pipelined_m: 80 evals, 28 feasible; max throughput seen 171 MSPS; best accuracy 13.63 bits; best feasible luts_plus_ffs=1135; feasible ranges: data_width 15..16, n_iter 14..16, angle_guard 1..4, frac_guard 1..4, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (80 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (7 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 86 feasible; hypervolume 1.618e+04 (+263.1%).

**No LLM call** (code's front-mapping round): The front is well-mapped and feasible. The minimum area design (1135 LUTs+FFs) meets all constraints: throughput 93.6 MSPS (>=32), max_abs_err 0.000217 (<=0.000244), and sys_p99_batch_us 0.161 us (<=0.44 us). The front spans accuracy_bits 12.2 to 13.6, covering the requirement (>=12 bits) with margin. Hypervolume gain in the last round was only +0.4%, indicating convergence. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (1135) from the front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.618e+04 (gain this round: +263.1%).
Feasible designs: 86 of 200 evaluations (70 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 50% violate; best seen 3.14e-08 (2^-24.93)
- sys_p99_batch_us <= 0.44: 10% violate; best seen 0.161

Pareto front (feasible, 17 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1135, accuracy_bits=12.2, luts=855, ffs=280, throughput_msps=93.6, max_abs_err=0.000217 (2^-12.17), power_index=1.37
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1200, accuracy_bits=12.4, luts=920, ffs=280, throughput_msps=93.6, max_abs_err=0.000187 (2^-12.39), power_index=1.44
- pipelined_m [data_width=16 n_iter=15 angle_guard=4 frac_guard=2 rounding=round m=4] luts_plus_ffs=1238, accuracy_bits=12.9, luts=954, ffs=285, throughput_msps=93.6, max_abs_err=0.000135 (2^-12.86), power_index=1.49
- pipelined_m [data_width=16 n_iter=16 angle_guard=4 frac_guard=2 rounding=round m=4] luts_plus_ffs=1303, accuracy_bits=13.2, luts=1019, ffs=285, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=1.57
- pipelined_m [data_width=22 n_iter=15 angle_guard=-2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=1553, accuracy_bits=13.7, luts=1126, ffs=427, throughput_msps=114, max_abs_err=7.4e-05 (2^-13.72), power_index=1.87
- pipelined_m [data_width=22 n_iter=20 angle_guard=1 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=2034, accuracy_bits=16.3, luts=1467, ffs=567, throughput_msps=114, max_abs_err=1.22e-05 (2^-16.32), power_index=2.45
- pipelined_m [data_width=22 n_iter=20 angle_guard=2 frac_guard=4 rounding=round m=4] luts_plus_ffs=2150, accuracy_bits=18.1, luts=1693, ffs=457, throughput_msps=89.6, max_abs_err=3.57e-06 (2^-18.10), power_index=2.59
- pipelined_m [data_width=25 n_iter=20 angle_guard=3 frac_guard=2 rounding=round m=3] luts_plus_ffs=2497, accuracy_bits=18.9, luts=1820, ffs=677, throughput_msps=110, max_abs_err=2.08e-06 (2^-18.88), power_index=3.01
- pipelined_m [data_width=27 n_iter=22 angle_guard=-2 frac_guard=4 rounding=round m=2] luts_plus_ffs=3212, accuracy_bits=19.6, luts=2120, ffs=1092, throughput_msps=147, max_abs_err=1.24e-06 (2^-19.62), power_index=3.87
- pipelined_m [data_width=27 n_iter=29 angle_guard=3 frac_guard=0 rounding=round m=3] luts_plus_ffs=3633, accuracy_bits=22.2, luts=2661, ffs=973, throughput_msps=110, max_abs_err=2.03e-07 (2^-22.23), power_index=4.37
Front coverage: luts_plus_ffs 1135..3633 (HV reference 4000); accuracy_bits 12.2..22.2 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- pipelined: 40 evals, 10 feasible; max throughput seen 273 MSPS; best accuracy 12.63 bits; best feasible luts_plus_ffs=1721; feasible ranges: data_width 15..16, n_iter 14..16, angle_guard 2..4, frac_guard 1..3
- pipelined_m: 160 evals, 76 feasible; max throughput seen 171 MSPS; best accuracy 24.93 bits; best feasible luts_plus_ffs=1135; feasible ranges: data_width 15..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 1)
- tokens: 8629 in, 1936 out
- provider-reported cost: $0.0037
- full prompts and replies: `llm_trace.jsonl`

