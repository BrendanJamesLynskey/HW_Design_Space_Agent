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
`pipelined_m:data_width=19,n_iter=15,angle_guard=3,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 979 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 309 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.55 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 8.25e-05 (2^-13.57) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 10.8 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.62e-05 (2^-15.22) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.43 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.6 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (34 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=15,angle_guard=3,frac_guard=0,rounding=round,m=4` | 979 | 309 | 93.6 | 6 | 1.55 | 8.25e-05 (2^-13.57) | 13.57 |
| 1 | `pipelined_m:data_width=20,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=4` | 994 | 315 | 93.6 | 6 | 1.57 | 7.63e-05 (2^-13.68) | 13.68 |
| 2 | `pipelined_m:data_width=20,n_iter=15,angle_guard=3,frac_guard=0,rounding=round,m=4` | 1023 | 323 | 89.6 | 6 | 1.62 | 7.16e-05 (2^-13.77) | 13.77 |
| 3 | `pipelined_m:data_width=20,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1080 | 327 | 93.6 | 6 | 1.69 | 6.81e-05 (2^-13.84) | 13.84 |
| 4 | `pipelined_m:data_width=21,n_iter=15,angle_guard=4,frac_guard=0,rounding=round,m=3` | 1082 | 416 | 114.5 | 7 | 1.8 | 6.66e-05 (2^-13.87) | 13.87 |
| 5 | `pipelined_m:data_width=21,n_iter=16,angle_guard=4,frac_guard=0,rounding=round,m=4` | 1159 | 341 | 89.6 | 6 | 1.81 | 3.63e-05 (2^-14.75) | 14.75 |
| 6 | `pipelined_m:data_width=19,n_iter=17,angle_guard=3,frac_guard=1,rounding=round,m=4` | 1192 | 386 | 93.6 | 7 | 1.9 | 3.23e-05 (2^-14.92) | 14.92 |
| 7 | `pipelined_m:data_width=21,n_iter=17,angle_guard=2,frac_guard=0,rounding=round,m=4` | 1202 | 406 | 89.6 | 7 | 1.94 | 2.18e-05 (2^-15.48) | 15.48 |
| 8 | `pipelined_m:data_width=21,n_iter=17,angle_guard=3,frac_guard=0,rounding=round,m=4` | 1219 | 411 | 89.6 | 7 | 1.96 | 2.15e-05 (2^-15.50) | 15.50 |
| 9 | `pipelined_m:data_width=21,n_iter=18,angle_guard=0,frac_guard=0,rounding=round,m=3` | 1241 | 466 | 119.3 | 8 | 2.06 | 2.12e-05 (2^-15.53) | 15.53 |
| 10 | `pipelined_m:data_width=21,n_iter=17,angle_guard=3,frac_guard=1,rounding=round,m=4` | 1297 | 421 | 89.6 | 7 | 2.07 | 1.95e-05 (2^-15.64) | 15.64 |
| 11 | `pipelined_m:data_width=20,n_iter=18,angle_guard=3,frac_guard=1,rounding=round,m=4` | 1319 | 404 | 89.6 | 7 | 2.07 | 1.69e-05 (2^-15.85) | 15.85 |
| 12 | `pipelined_m:data_width=20,n_iter=18,angle_guard=4,frac_guard=1,rounding=round,m=4` | 1337 | 409 | 89.6 | 7 | 2.1 | 1.59e-05 (2^-15.94) | 15.94 |
| 13 | `pipelined_m:data_width=20,n_iter=18,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1355 | 412 | 89.6 | 7 | 2.13 | 1.42e-05 (2^-16.11) | 16.11 |
| 14 | `pipelined_m:data_width=21,n_iter=18,angle_guard=4,frac_guard=1,rounding=round,m=4` | 1393 | 426 | 89.6 | 7 | 2.19 | 1.13e-05 (2^-16.43) | 16.43 |
| 15 | `pipelined_m:data_width=21,n_iter=19,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1415 | 411 | 93.6 | 7 | 2.2 | 1.06e-05 (2^-16.52) | 16.52 |
| 16 | `pipelined_m:data_width=21,n_iter=18,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1411 | 429 | 89.6 | 7 | 2.21 | 9.93e-06 (2^-16.62) | 16.62 |
| 17 | `pipelined_m:data_width=21,n_iter=18,angle_guard=4,frac_guard=2,rounding=round,m=4` | 1429 | 434 | 89.6 | 7 | 2.24 | 9.83e-06 (2^-16.64) | 16.64 |
| 18 | `pipelined_m:data_width=22,n_iter=18,angle_guard=3,frac_guard=1,rounding=round,m=4` | 1431 | 438 | 89.6 | 7 | 2.25 | 9.77e-06 (2^-16.64) | 16.64 |
| 19 | `pipelined_m:data_width=21,n_iter=19,angle_guard=2,frac_guard=1,rounding=round,m=3` | 1434 | 565 | 114.5 | 9 | 2.41 | 9.17e-06 (2^-16.74) | 16.74 |
| 20 | `pipelined_m:data_width=22,n_iter=19,angle_guard=1,frac_guard=1,rounding=round,m=3` | 1474 | 581 | 114.5 | 9 | 2.47 | 7.47e-06 (2^-17.03) | 17.03 |
| 21 | `pipelined_m:data_width=21,n_iter=21,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1630 | 500 | 89.6 | 8 | 2.56 | 5.47e-06 (2^-17.48) | 17.48 |
| 22 | `pipelined_m:data_width=21,n_iter=20,angle_guard=3,frac_guard=2,rounding=round,m=3` | 1571 | 584 | 114.5 | 9 | 2.59 | 5.13e-06 (2^-17.57) | 17.57 |
| 23 | `pipelined_m:data_width=21,n_iter=21,angle_guard=2,frac_guard=3,rounding=round,m=4` | 1672 | 511 | 89.6 | 8 | 2.63 | 4.46e-06 (2^-17.77) | 17.77 |
| 24 | `pipelined_m:data_width=22,n_iter=20,angle_guard=3,frac_guard=1,rounding=round,m=3` | 1593 | 595 | 114.5 | 9 | 2.63 | 4.05e-06 (2^-17.91) | 17.91 |
| 25 | `pipelined_m:data_width=25,n_iter=24,angle_guard=-2,frac_guard=0,rounding=trunc,m=4` | 1920 | 535 | 89.6 | 8 | 2.95 | 3.52e-06 (2^-18.12) | 18.12 |
| 26 | `pipelined_m:data_width=25,n_iter=21,angle_guard=2,frac_guard=2,rounding=round,m=2` | 1891 | 1025 | 152.6 | 13 | 3.51 | 1.2e-06 (2^-19.67) | 19.67 |
| 27 | `pipelined:data_width=27,n_iter=21,angle_guard=0,frac_guard=1,rounding=round` | 1938 | 1905 | 249.0 | 23 | 4.63 | 1.13e-06 (2^-19.76) | 19.76 |
| 28 | `pipelined:data_width=27,n_iter=21,angle_guard=1,frac_guard=1,rounding=round` | 1959 | 1926 | 249.0 | 23 | 4.68 | 1.05e-06 (2^-19.86) | 19.86 |
| 29 | `pipelined:data_width=27,n_iter=21,angle_guard=1,frac_guard=2,rounding=round` | 2001 | 1964 | 249.0 | 23 | 4.77 | 1.03e-06 (2^-19.88) | 19.88 |
| 30 | `pipelined:data_width=27,n_iter=22,angle_guard=1,frac_guard=2,rounding=round` | 2098 | 2058 | 249.0 | 24 | 5 | 5.58e-07 (2^-20.77) | 20.77 |
| 31 | `pipelined:data_width=27,n_iter=24,angle_guard=1,frac_guard=0,rounding=round` | 2138 | 2155 | 249.0 | 26 | 5.17 | 2.86e-07 (2^-21.74) | 21.74 |
| 32 | `pipelined:data_width=28,n_iter=27,angle_guard=1,frac_guard=1,rounding=round` | 2612 | 2559 | 249.0 | 29 | 6.22 | 8.92e-08 (2^-23.42) | 23.42 |
| 33 | `pipelined:data_width=28,n_iter=29,angle_guard=4,frac_guard=3,rounding=trunc` | 2956 | 2943 | 242.0 | 31 | 7.1 | 3.83e-08 (2^-24.64) | 24.64 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *fallback plan (LLM gave none)*)
- `pipelined` (50 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* fallback: full range
- `pipelined_m` (50 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* fallback: full range
- clamped by code: LLM produced no valid plan (openrouter:qwen/qwen3.8-27b failed to produce ExplorationPlan: LengthFinishReasonError: Could not parse response content as the length limit was reached - CompletionUsage(completion_tokens=16000, prom); used deterministic fallback: every family, full range

**Result (code):** 100 evaluations this round, 100 total; 56 feasible; hypervolume 1.498e+04 (n/a).

**LLM decision:** `map_front` — The current front is dominated by pipelined_m designs, which are significantly cheaper (1500-2100 LUTs+FFs) than the pipelined designs (2500-5000+). The pipelined_m family achieves the required throughput (89.6 MSPS > 32) and accuracy (14.7-17.8 bits > 12) with much lower area. The front currently spans a wide area range (1500-5171) but the high-area end is inefficient. Mapping the front will allow the code to densely sample the trade-off curve, particularly focusing on the pipelined_m region which offers the best area/accuracy ratio, and to ensure the hypervolume is maximized by covering the full feasible range of the cheaper family.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.498e+04 (gain this round: n/a (first round)).
Feasible designs: 56 of 100 evaluations (48 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 27% violate; best seen 8.92e-08 (2^-23.42)
- sys_p99_batch_us <= 0.44: 19% violate; best seen 0.136

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=21 n_iter=16 angle_guard=4 frac_guard=0 rounding=round m=4] luts_plus_ffs=1500, accuracy_bits=14.7, luts=1159, ffs=341, throughput_msps=89.6, max_abs_err=3.63e-05 (2^-14.75), power_index=1.81
- pipelined_m [data_width=21 n_iter=17 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1608, accuracy_bits=15.5, luts=1202, ffs=406, throughput_msps=89.6, max_abs_err=2.18e-05 (2^-15.48), power_index=1.94
- pipelined_m [data_width=21 n_iter=21 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=2131, accuracy_bits=17.5, luts=1630, ffs=500, throughput_msps=89.6, max_abs_err=5.47e-06 (2^-17.48), power_index=2.56
- pipelined_m [data_width=21 n_iter=21 angle_guard=2 frac_guard=3 rounding=round m=4] luts_plus_ffs=2183, accuracy_bits=17.8, luts=1672, ffs=511, throughput_msps=89.6, max_abs_err=4.46e-06 (2^-17.77), power_index=2.63
- pipelined_m [data_width=25 n_iter=21 angle_guard=2 frac_guard=2 rounding=round m=2] luts_plus_ffs=2917, accuracy_bits=19.7, luts=1891, ffs=1025, throughput_msps=153, max_abs_err=1.2e-06 (2^-19.67), power_index=3.51
- pipelined [data_width=27 n_iter=21 angle_guard=0 frac_guard=1 rounding=round] luts_plus_ffs=3843, accuracy_bits=19.8, luts=1938, ffs=1905, throughput_msps=249, max_abs_err=1.13e-06 (2^-19.76), power_index=4.63
- pipelined [data_width=27 n_iter=21 angle_guard=1 frac_guard=1 rounding=round] luts_plus_ffs=3885, accuracy_bits=19.9, luts=1959, ffs=1926, throughput_msps=249, max_abs_err=1.05e-06 (2^-19.86), power_index=4.68
- pipelined [data_width=27 n_iter=21 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=3965, accuracy_bits=19.9, luts=2001, ffs=1964, throughput_msps=249, max_abs_err=1.03e-06 (2^-19.88), power_index=4.77
- pipelined [data_width=27 n_iter=22 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=4156, accuracy_bits=20.8, luts=2098, ffs=2058, throughput_msps=249, max_abs_err=5.58e-07 (2^-20.77), power_index=5
- pipelined [data_width=28 n_iter=27 angle_guard=1 frac_guard=1 rounding=round] luts_plus_ffs=5171, accuracy_bits=23.4, luts=2612, ffs=2559, throughput_msps=249, max_abs_err=8.92e-08 (2^-23.42), power_index=6.22
Front coverage: luts_plus_ffs 1500..5171 (HV reference 4000); accuracy_bits 14.7..23.4 (HV reference 12); data_width on the front 21..28 (registry 8..28).

Per family:
- pipelined: 50 evals, 37 feasible; max throughput seen 282 MSPS; best accuracy 23.42 bits; best feasible luts_plus_ffs=2553; feasible ranges: data_width 19..28, n_iter 16..29, angle_guard -1..3, frac_guard 0..4
- pipelined_m: 50 evals, 19 feasible; max throughput seen 186 MSPS; best accuracy 22.66 bits; best feasible luts_plus_ffs=1500; feasible ranges: data_width 15..25, n_iter 14..21, angle_guard 0..4, frac_guard 0..3, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `pipelined_m` (10 evals): data_width=20..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (5 front designs; box front_anchored)
- `pipelined` (10 evals): data_width=26..28, n_iter=19..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (5 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 74 feasible; hypervolume 1.517e+04 (+1.3%).

**LLM decision:** `refine` — The current Pareto front is dominated by `pipelined_m` designs at the low-area end (1500-2183 LUTs+FFs) and `pipelined` at the high-accuracy end. The `pipelined_m` family is significantly more area-efficient (best 1500 vs 2553 for `pipelined`) and meets the throughput constraint (>=32 MSPS) comfortably (89.6 MSPS). The selection rule is `min luts_plus_ffs`, and the current best feasible design is a `pipelined_m` with 1500 LUTs+FFs. To improve hypervolume and potentially find a better minimum-area design, we should focus the search on the `pipelined_m` family in the region where it is most competitive: low `data_width` (19-22), moderate `n_iter` (16-20), and `m=4` (which appears in the top 4 front designs). We should also explore if `m=2` or `m=3` can offer a better trade-off at slightly higher area but potentially better accuracy or Fmax, though `m=4` seems optimal for area. The `pipelined` family is less relevant for the minimum-area selection but contributes to the high-accuracy end of the front; however, since the selection rule prioritizes area, refining `pipelined_m` is the highest-value action. We will narrow the ranges for `pipelined_m` to focus on the promising low-area, high-accuracy region.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.517e+04 (gain this round: +1.3%).
Feasible designs: 74 of 120 evaluations (65 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 22% violate; best seen 3.83e-08 (2^-24.64)
- sys_p99_batch_us <= 0.44: 18% violate; best seen 0.136

Pareto front (feasible, 14 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=21 n_iter=16 angle_guard=4 frac_guard=0 rounding=round m=4] luts_plus_ffs=1500, accuracy_bits=14.7, luts=1159, ffs=341, throughput_msps=89.6, max_abs_err=3.63e-05 (2^-14.75), power_index=1.81
- pipelined_m [data_width=21 n_iter=17 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1608, accuracy_bits=15.5, luts=1202, ffs=406, throughput_msps=89.6, max_abs_err=2.18e-05 (2^-15.48), power_index=1.94
- pipelined_m [data_width=21 n_iter=21 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=2131, accuracy_bits=17.5, luts=1630, ffs=500, throughput_msps=89.6, max_abs_err=5.47e-06 (2^-17.48), power_index=2.56
- pipelined_m [data_width=21 n_iter=21 angle_guard=2 frac_guard=3 rounding=round m=4] luts_plus_ffs=2183, accuracy_bits=17.8, luts=1672, ffs=511, throughput_msps=89.6, max_abs_err=4.46e-06 (2^-17.77), power_index=2.63
- pipelined_m [data_width=25 n_iter=21 angle_guard=2 frac_guard=2 rounding=round m=2] luts_plus_ffs=2917, accuracy_bits=19.7, luts=1891, ffs=1025, throughput_msps=153, max_abs_err=1.2e-06 (2^-19.67), power_index=3.51
- pipelined [data_width=27 n_iter=21 angle_guard=0 frac_guard=1 rounding=round] luts_plus_ffs=3843, accuracy_bits=19.8, luts=1938, ffs=1905, throughput_msps=249, max_abs_err=1.13e-06 (2^-19.76), power_index=4.63
- pipelined [data_width=27 n_iter=21 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=3965, accuracy_bits=19.9, luts=2001, ffs=1964, throughput_msps=249, max_abs_err=1.03e-06 (2^-19.88), power_index=4.77
- pipelined [data_width=27 n_iter=22 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=4156, accuracy_bits=20.8, luts=2098, ffs=2058, throughput_msps=249, max_abs_err=5.58e-07 (2^-20.77), power_index=5
- pipelined [data_width=28 n_iter=27 angle_guard=1 frac_guard=1 rounding=round] luts_plus_ffs=5171, accuracy_bits=23.4, luts=2612, ffs=2559, throughput_msps=249, max_abs_err=8.92e-08 (2^-23.42), power_index=6.22
- pipelined [data_width=28 n_iter=29 angle_guard=4 frac_guard=3 rounding=trunc] luts_plus_ffs=5899, accuracy_bits=24.6, luts=2956, ffs=2943, throughput_msps=242, max_abs_err=3.83e-08 (2^-24.64), power_index=7.1
Front coverage: luts_plus_ffs 1500..5899 (HV reference 4000); accuracy_bits 14.7..24.6 (HV reference 12); data_width on the front 21..28 (registry 8..28).

Per family:
- pipelined: 60 evals, 47 feasible; max throughput seen 282 MSPS; best accuracy 24.64 bits; best feasible luts_plus_ffs=2553; feasible ranges: data_width 19..28, n_iter 16..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 60 evals, 27 feasible; max throughput seen 186 MSPS; best accuracy 22.66 bits; best feasible luts_plus_ffs=1500; feasible ranges: data_width 15..26, n_iter 14..29, angle_guard -2..4, frac_guard 0..3, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Refine the search to the most promising region of the pipelined_m family to find a potentially better minimum-area design and improve the hypervolume of the low-area end of the front.*)
- `pipelined_m` (80 evals): data_width=19..22, n_iter=15..20, angle_guard=0..4, frac_guard=0..2, rounding=round, m=3..5. *Why:* Focus on the area-efficient pipelined_m family in the region where it dominates the front (low area, sufficient accuracy). Narrowing data_width and n_iter focuses the search on the trade-off curve relevant to the min-area selection rule.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 80 evaluations this round, 200 total; 144 feasible; hypervolume 1.6e+04 (+5.5%).

**LLM decision:** `stop` — The budget (200 evals) and round cap (4) have been reached. The Pareto front is well-mapped across the feasible trade-off space: it spans luts_plus_ffs from 1288 to 5899 and accuracy_bits from 13.6 to 24.6, comfortably covering the hypervolume reference point (4000, 12). The front includes designs that satisfy all constraints (throughput >= 32 MSPS, max_abs_err <= 2^-12, sys_p99_batch_us <= 0.44 us). The selection rule (min luts_plus_ffs) points to the pipelined_m design with luts_plus_ffs=1288, which has 13.6 bits of accuracy and 93.6 MSPS throughput, well within the system requirements. No further exploration is possible or needed.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.6e+04 (gain this round: +5.5%).
Feasible designs: 144 of 200 evaluations (118 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 14% violate; best seen 3.83e-08 (2^-24.64)
- sys_p99_batch_us <= 0.44: 16% violate; best seen 0.136

Pareto front (feasible, 34 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=0 rounding=round m=4] luts_plus_ffs=1288, accuracy_bits=13.6, luts=979, ffs=309, throughput_msps=93.6, max_abs_err=8.25e-05 (2^-13.57), power_index=1.55
- pipelined_m [data_width=21 n_iter=15 angle_guard=4 frac_guard=0 rounding=round m=3] luts_plus_ffs=1498, accuracy_bits=13.9, luts=1082, ffs=416, throughput_msps=114, max_abs_err=6.66e-05 (2^-13.87), power_index=1.8
- pipelined_m [data_width=21 n_iter=17 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1608, accuracy_bits=15.5, luts=1202, ffs=406, throughput_msps=89.6, max_abs_err=2.18e-05 (2^-15.48), power_index=1.94
- pipelined_m [data_width=20 n_iter=18 angle_guard=3 frac_guard=1 rounding=round m=4] luts_plus_ffs=1723, accuracy_bits=15.9, luts=1319, ffs=404, throughput_msps=89.6, max_abs_err=1.69e-05 (2^-15.85), power_index=2.07
- pipelined_m [data_width=21 n_iter=19 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1826, accuracy_bits=16.5, luts=1415, ffs=411, throughput_msps=93.6, max_abs_err=1.06e-05 (2^-16.52), power_index=2.2
- pipelined_m [data_width=22 n_iter=18 angle_guard=3 frac_guard=1 rounding=round m=4] luts_plus_ffs=1869, accuracy_bits=16.6, luts=1431, ffs=438, throughput_msps=89.6, max_abs_err=9.77e-06 (2^-16.64), power_index=2.25
- pipelined_m [data_width=21 n_iter=20 angle_guard=3 frac_guard=2 rounding=round m=3] luts_plus_ffs=2155, accuracy_bits=17.6, luts=1571, ffs=584, throughput_msps=114, max_abs_err=5.13e-06 (2^-17.57), power_index=2.59
- pipelined_m [data_width=25 n_iter=21 angle_guard=2 frac_guard=2 rounding=round m=2] luts_plus_ffs=2917, accuracy_bits=19.7, luts=1891, ffs=1025, throughput_msps=153, max_abs_err=1.2e-06 (2^-19.67), power_index=3.51
- pipelined [data_width=27 n_iter=21 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=3965, accuracy_bits=19.9, luts=2001, ffs=1964, throughput_msps=249, max_abs_err=1.03e-06 (2^-19.88), power_index=4.77
- pipelined [data_width=28 n_iter=29 angle_guard=4 frac_guard=3 rounding=trunc] luts_plus_ffs=5899, accuracy_bits=24.6, luts=2956, ffs=2943, throughput_msps=242, max_abs_err=3.83e-08 (2^-24.64), power_index=7.1
Front coverage: luts_plus_ffs 1288..5899 (HV reference 4000); accuracy_bits 13.6..24.6 (HV reference 12); data_width on the front 19..28 (registry 8..28).

Per family:
- pipelined: 60 evals, 47 feasible; max throughput seen 282 MSPS; best accuracy 24.64 bits; best feasible luts_plus_ffs=2553; feasible ranges: data_width 19..28, n_iter 16..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 140 evals, 97 feasible; max throughput seen 186 MSPS; best accuracy 22.66 bits; best feasible luts_plus_ffs=1288; feasible ranges: data_width 15..26, n_iter 14..29, angle_guard -2..4, frac_guard 0..3, m 2..4
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 2)
- tokens: 11519 in, 1204 out
- provider-reported cost: $0.0036
- full prompts and replies: `llm_trace.jsonl`

