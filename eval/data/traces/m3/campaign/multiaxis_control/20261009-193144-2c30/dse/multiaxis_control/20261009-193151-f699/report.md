# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: anthropic/claude-sonnet-5.5.  
**Evaluations:** 300 of 300 budgeted, over 3 round(s).  
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
  budget: 300 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 895 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 270 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 61.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00018 (2^-12.44) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 2.94 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 5.01e-05 (2^-14.29) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 0.82 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.4 | exact: bit-accurate model, exhaustive (65536 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 93.3 dBc, SNR 83.6 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=17,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=20,n_iter=14,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 0.4016 → 0.4126 | yes |
| `pipelined_m:data_width=21,n_iter=15,angle_guard=-2,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=20,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc,m=3` | 0.3103 → 0.3186 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (29 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=4` | 895 | 270 | 97.8 | 6 | 1.4 | 0.00018 (2^-12.44) | 12.44 |
| 1 | `pipelined_m:data_width=17,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 969 | 282 | 93.6 | 6 | 1.51 | 0.000174 (2^-12.49) | 12.49 |
| 2 | `pipelined_m:data_width=20,n_iter=14,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 978 | 329 | 89.6 | 6 | 1.57 | 0.000132 (2^-12.89) | 12.89 |
| 3 | `pipelined_m:data_width=21,n_iter=15,angle_guard=-2,frac_guard=0,rounding=round,m=4` | 994 | 317 | 93.6 | 6 | 1.58 | 9.08e-05 (2^-13.43) | 13.43 |
| 4 | `pipelined_m:data_width=20,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc,m=3` | 979 | 378 | 119.3 | 7 | 1.63 | 8.73e-05 (2^-13.48) | 13.48 |
| 5 | `pipelined_m:data_width=20,n_iter=15,angle_guard=1,frac_guard=0,rounding=trunc,m=3` | 994 | 383 | 119.3 | 7 | 1.66 | 8.71e-05 (2^-13.49) | 13.49 |
| 6 | `pipelined_m:data_width=20,n_iter=15,angle_guard=2,frac_guard=0,rounding=trunc,m=3` | 1008 | 388 | 119.3 | 7 | 1.68 | 8.43e-05 (2^-13.53) | 13.53 |
| 7 | `pipelined_m:data_width=20,n_iter=15,angle_guard=2,frac_guard=1,rounding=trunc,m=3` | 1038 | 397 | 119.3 | 7 | 1.73 | 7.32e-05 (2^-13.74) | 13.74 |
| 8 | `pipelined_m:data_width=21,n_iter=15,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1141 | 343 | 89.6 | 6 | 1.79 | 6.34e-05 (2^-13.94) | 13.94 |
| 9 | `pipelined_m:data_width=21,n_iter=15,angle_guard=2,frac_guard=2,rounding=round,m=3` | 1156 | 424 | 114.5 | 7 | 1.9 | 6.29e-05 (2^-13.96) | 13.96 |
| 10 | `pipelined_m:data_width=24,n_iter=15,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 1215 | 381 | 89.6 | 6 | 1.92 | 6.16e-05 (2^-13.99) | 13.99 |
| 11 | `pipelined_m:data_width=22,n_iter=17,angle_guard=-2,frac_guard=1,rounding=trunc,m=4` | 1219 | 411 | 89.6 | 7 | 1.96 | 3.48e-05 (2^-14.81) | 14.81 |
| 12 | `pipelined_m:data_width=24,n_iter=17,angle_guard=-2,frac_guard=0,rounding=trunc,m=4` | 1287 | 437 | 89.6 | 7 | 2.07 | 1.98e-05 (2^-15.63) | 15.63 |
| 13 | `pipelined_m:data_width=23,n_iter=17,angle_guard=1,frac_guard=0,rounding=trunc,m=3` | 1287 | 513 | 114.5 | 8 | 2.17 | 1.83e-05 (2^-15.74) | 15.74 |
| 14 | `pipelined_m:data_width=23,n_iter=17,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1354 | 451 | 89.6 | 7 | 2.17 | 1.65e-05 (2^-15.89) | 15.89 |
| 15 | `pipelined_m:data_width=24,n_iter=17,angle_guard=1,frac_guard=1,rounding=trunc,m=3` | 1371 | 543 | 114.5 | 8 | 2.3 | 1.61e-05 (2^-15.93) | 15.93 |
| 16 | `pipelined_m:data_width=21,n_iter=20,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1531 | 419 | 89.6 | 7 | 2.35 | 8.09e-06 (2^-16.91) | 16.91 |
| 17 | `pipelined_m:data_width=23,n_iter=20,angle_guard=-1,frac_guard=1,rounding=round,m=4` | 1575 | 435 | 89.6 | 7 | 2.42 | 7.46e-06 (2^-17.03) | 17.03 |
| 18 | `pipelined_m:data_width=23,n_iter=20,angle_guard=3,frac_guard=0,rounding=trunc,m=4` | 1567 | 445 | 89.6 | 7 | 2.42 | 6.2e-06 (2^-17.30) | 17.30 |
| 19 | `pipelined_m:data_width=23,n_iter=20,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1607 | 453 | 89.6 | 7 | 2.48 | 4.15e-06 (2^-17.88) | 17.88 |
| 20 | `pipelined_m:data_width=24,n_iter=20,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1667 | 468 | 89.6 | 7 | 2.57 | 2.81e-06 (2^-18.44) | 18.44 |
| 21 | `pipelined_m:data_width=25,n_iter=20,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1727 | 487 | 86.0 | 7 | 2.67 | 2.31e-06 (2^-18.72) | 18.72 |
| 22 | `pipelined_m:data_width=25,n_iter=20,angle_guard=4,frac_guard=4,rounding=trunc,m=4` | 1867 | 517 | 86.0 | 7 | 2.87 | 2.05e-06 (2^-18.90) | 18.90 |
| 23 | `pipelined_m:data_width=24,n_iter=23,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1957 | 551 | 89.6 | 8 | 3.02 | 1.08e-06 (2^-19.82) | 19.82 |
| 24 | `pipelined_m:data_width=28,n_iter=22,angle_guard=-2,frac_guard=2,rounding=trunc,m=3` | 2041 | 803 | 110.0 | 10 | 3.42 | 9.33e-07 (2^-20.03) | 20.03 |
| 25 | `pipelined_m:data_width=27,n_iter=29,angle_guard=-1,frac_guard=1,rounding=trunc,m=3` | 2602 | 950 | 110.0 | 12 | 4.28 | 6.81e-07 (2^-20.49) | 20.49 |
| 26 | `pipelined_m:data_width=28,n_iter=28,angle_guard=-2,frac_guard=2,rounding=round,m=3` | 2682 | 993 | 110.0 | 12 | 4.42 | 5.8e-07 (2^-20.72) | 20.72 |
| 27 | `pipelined_m:data_width=27,n_iter=29,angle_guard=2,frac_guard=2,rounding=trunc,m=3` | 2749 | 999 | 110.0 | 12 | 4.51 | 1.42e-07 (2^-22.74) | 22.74 |
| 28 | `pipelined_m:data_width=28,n_iter=28,angle_guard=2,frac_guard=1,rounding=round,m=3` | 2739 | 1015 | 110.0 | 12 | 4.52 | 6.73e-08 (2^-23.82) | 23.82 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *placeholder*)
- `pipelined_m` (100 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* placeholder

**Result (code):** 100 evaluations this round, 100 total; 48 feasible; hypervolume 1.673e+04 (n/a).

**LLM decision:** `add_family` — Only pipelined_m has been explored. Its front starts at 1310 LUT+FF and 13.4 bits, so the low-area end near the 12-bit error limit (2^-12) is empty and likely holds cheaper designs. 36% of evaluations violate the error constraint and 36% violate the batch-latency constraint, with the best batch time at 0.221 us against a 0.44 us limit. Plain pipelined (1 result/cycle, no m-stage combinational chains) has not been tried and may reach higher Fmax. I am leaving out iterative and unrolled_k. They accept a result only every several cycles, so 32 simultaneous requests would queue, and the 0.44 us batch bound looks unreachable for them. Next round: pipelined_m with smaller widths and iteration counts plus larger m, and pipelined over the same low-area region.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 300.
Hypervolume of the feasible front: 1.673e+04 (gain this round: n/a (first round)).
Feasible designs: 48 of 100 evaluations (43 unique).
Families explored so far: pipelined_m. Not yet explored: iterative, unrolled_k, pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 178
- max_abs_err <= 0.000244141: 36% violate; best seen 9.33e-07 (2^-20.03)
- sys_p99_batch_us <= 0.44: 36% violate; best seen 0.221

Pareto front (feasible, 14 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=21 n_iter=15 angle_guard=-2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1310, accuracy_bits=13.4, luts=994, ffs=317, throughput_msps=93.6, max_abs_err=9.08e-05 (2^-13.43), power_index=1.58
- pipelined_m [data_width=21 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1484, accuracy_bits=13.9, luts=1141, ffs=343, throughput_msps=89.6, max_abs_err=6.34e-05 (2^-13.94), power_index=1.79
- pipelined_m [data_width=24 n_iter=15 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1596, accuracy_bits=14, luts=1215, ffs=381, throughput_msps=89.6, max_abs_err=6.16e-05 (2^-13.99), power_index=1.92
- pipelined_m [data_width=21 n_iter=17 angle_guard=-2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=1677, accuracy_bits=14.2, luts=1202, ffs=474, throughput_msps=114, max_abs_err=5.3e-05 (2^-14.20), power_index=2.02
- pipelined_m [data_width=24 n_iter=17 angle_guard=-2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1807, accuracy_bits=15.6, luts=1354, ffs=453, throughput_msps=89.6, max_abs_err=1.98e-05 (2^-15.63), power_index=2.18
- pipelined_m [data_width=24 n_iter=17 angle_guard=-2 frac_guard=1 rounding=round m=3] luts_plus_ffs=1898, accuracy_bits=15.6, luts=1371, ffs=527, throughput_msps=114, max_abs_err=1.98e-05 (2^-15.63), power_index=2.28
- pipelined_m [data_width=21 n_iter=20 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1950, accuracy_bits=16.9, luts=1531, ffs=419, throughput_msps=89.6, max_abs_err=8.09e-06 (2^-16.91), power_index=2.35
- pipelined_m [data_width=24 n_iter=20 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=2135, accuracy_bits=18.4, luts=1667, ffs=468, throughput_msps=89.6, max_abs_err=2.81e-06 (2^-18.44), power_index=2.57
- pipelined_m [data_width=24 n_iter=23 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=2508, accuracy_bits=19.8, luts=1957, ffs=551, throughput_msps=89.6, max_abs_err=1.08e-06 (2^-19.82), power_index=3.02
- pipelined_m [data_width=28 n_iter=22 angle_guard=-2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=2844, accuracy_bits=20, luts=2041, ffs=803, throughput_msps=110, max_abs_err=9.33e-07 (2^-20.03), power_index=3.42
Front coverage: luts_plus_ffs 1310..2844 (HV reference 4000); accuracy_bits 13.4..20 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- pipelined_m: 100 evals, 48 feasible; max throughput seen 178 MSPS; best accuracy 20.03 bits; best feasible luts_plus_ffs=1310; feasible ranges: data_width 18..28, n_iter 15..30, angle_guard -2..3, frac_guard 0..3, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Cover the empty low-area region with both pipelined variants, and keep accuracy at or above 12 bits so the error constraint is met.*)
- `pipelined_m` (48 evals): data_width=14..20, n_iter=11..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..6. *Why:* Push the front toward lower area near the 2^-12 error limit; the feasible front is empty below 1310 LUT+FF, and larger m cuts FFs while batch time still has margin.
- `pipelined` (32 evals): data_width=14..22, n_iter=11..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Not yet explored; per-stage registers may give higher Fmax and lower latency, so it may be competitive in the low-area, moderate-accuracy region.

**Result (code):** 80 evaluations this round, 180 total; 66 feasible; hypervolume 1.682e+04 (+0.5%).

**LLM decision:** `stop` — This is the final round, so stop is the only valid choice. The front is feasible and well populated: 20 designs, with luts_plus_ffs from 1165 to 2844 and accuracy_bits from 12.4 to 20. The cheapest feasible design is pipelined_m (W=16, N=15, round, m=4) at 1165 LUTs+FFs with max error 2^-12.44. It meets all three constraints: throughput 97.8 MSPS against 32, error 0.00018 against 0.000244, and a best p99 batch time of 0.158 us against 0.44. HV gain this round was only +0.5%, below the 0.01 eps, so the search has converged. The pipelined and pipelined_m families already meet the system bound, so the iterative and unrolled_k families are unlikely to beat 1165 given their multi-cycle batch latency.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 120 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 180 of 300.
Hypervolume of the feasible front: 1.682e+04 (gain this round: +0.5%).
Feasible designs: 66 of 180 evaluations (58 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 51% violate; best seen 9.33e-07 (2^-20.03)
- sys_p99_batch_us <= 0.44: 28% violate; best seen 0.158

Pareto front (feasible, 20 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1165, accuracy_bits=12.4, luts=895, ffs=270, throughput_msps=97.8, max_abs_err=0.00018 (2^-12.44), power_index=1.4
- pipelined_m [data_width=21 n_iter=15 angle_guard=-2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1310, accuracy_bits=13.4, luts=994, ffs=317, throughput_msps=93.6, max_abs_err=9.08e-05 (2^-13.43), power_index=1.58
- pipelined_m [data_width=20 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=1377, accuracy_bits=13.5, luts=994, ffs=383, throughput_msps=119, max_abs_err=8.71e-05 (2^-13.49), power_index=1.66
- pipelined_m [data_width=20 n_iter=15 angle_guard=2 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1434, accuracy_bits=13.7, luts=1038, ffs=397, throughput_msps=119, max_abs_err=7.32e-05 (2^-13.74), power_index=1.73
- pipelined_m [data_width=21 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=3] luts_plus_ffs=1580, accuracy_bits=14, luts=1156, ffs=424, throughput_msps=114, max_abs_err=6.29e-05 (2^-13.96), power_index=1.9
- pipelined_m [data_width=18 n_iter=20 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1762, accuracy_bits=15, luts=1385, ffs=377, throughput_msps=93.6, max_abs_err=3.15e-05 (2^-14.95), power_index=2.12
- pipelined_m [data_width=24 n_iter=17 angle_guard=-2 frac_guard=1 rounding=round m=3] luts_plus_ffs=1898, accuracy_bits=15.6, luts=1371, ffs=527, throughput_msps=114, max_abs_err=1.98e-05 (2^-15.63), power_index=2.28
- pipelined_m [data_width=21 n_iter=20 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1950, accuracy_bits=16.9, luts=1531, ffs=419, throughput_msps=89.6, max_abs_err=8.09e-06 (2^-16.91), power_index=2.35
- pipelined_m [data_width=24 n_iter=20 angle_guard=3 frac_guard=2 rounding=round m=3] luts_plus_ffs=2411, accuracy_bits=18.8, luts=1758, ffs=654, throughput_msps=110, max_abs_err=2.22e-06 (2^-18.78), power_index=2.9
- pipelined_m [data_width=28 n_iter=22 angle_guard=-2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=2844, accuracy_bits=20, luts=2041, ffs=803, throughput_msps=110, max_abs_err=9.33e-07 (2^-20.03), power_index=3.42
Front coverage: luts_plus_ffs 1165..2844 (HV reference 4000); accuracy_bits 12.4..20 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- pipelined: 32 evals, 3 feasible; max throughput seen 273 MSPS; best accuracy 14.64 bits; best feasible luts_plus_ffs=1843; feasible ranges: data_width 17..21, n_iter 16..16, angle_guard 0..0, frac_guard 0..2
- pipelined_m: 148 evals, 63 feasible; max throughput seen 178 MSPS; best accuracy 20.03 bits; best feasible luts_plus_ffs=1165; feasible ranges: data_width 16..28, n_iter 15..30, angle_guard -2..3, frac_guard 0..3, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 120 evaluations*)
- `pipelined_m` (120 evals): data_width=15..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (20 front designs; box front_anchored)

**Result (code):** 120 evaluations this round, 300 total; 148 feasible; hypervolume 1.822e+04 (+8.3%).

**No LLM call** (code's front-mapping round): This is the final round, so stop is the only valid choice. The front is feasible and well populated: 20 designs, with luts_plus_ffs from 1165 to 2844 and accuracy_bits from 12.4 to 20. The cheapest feasible design is pipelined_m (W=16, N=15, round, m=4) at 1165 LUTs+FFs with max error 2^-12.44. It meets all three constraints: throughput 97.8 MSPS against 32, error 0.00018 against 0.000244, and a best p99 batch time of 0.158 us against 0.44. HV gain this round was only +0.5%, below the 0.01 eps, so the search has converged. The pipelined and pipelined_m families already meet the system bound, so the iterative and unrolled_k families are unlikely to beat 1165 given their multi-cycle batch latency.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 300.
Hypervolume of the feasible front: 1.822e+04 (gain this round: +8.3%).
Feasible designs: 148 of 300 evaluations (132 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 35% violate; best seen 6.73e-08 (2^-23.82)
- sys_p99_batch_us <= 0.44: 27% violate; best seen 0.158

Pareto front (feasible, 29 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1165, accuracy_bits=12.4, luts=895, ffs=270, throughput_msps=97.8, max_abs_err=0.00018 (2^-12.44), power_index=1.4
- pipelined_m [data_width=21 n_iter=15 angle_guard=-2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1310, accuracy_bits=13.4, luts=994, ffs=317, throughput_msps=93.6, max_abs_err=9.08e-05 (2^-13.43), power_index=1.58
- pipelined_m [data_width=20 n_iter=15 angle_guard=2 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=1397, accuracy_bits=13.5, luts=1008, ffs=388, throughput_msps=119, max_abs_err=8.43e-05 (2^-13.53), power_index=1.68
- pipelined_m [data_width=21 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=3] luts_plus_ffs=1580, accuracy_bits=14, luts=1156, ffs=424, throughput_msps=114, max_abs_err=6.29e-05 (2^-13.96), power_index=1.9
- pipelined_m [data_width=24 n_iter=17 angle_guard=-2 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1723, accuracy_bits=15.6, luts=1287, ffs=437, throughput_msps=89.6, max_abs_err=1.98e-05 (2^-15.63), power_index=2.07
- pipelined_m [data_width=21 n_iter=20 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1950, accuracy_bits=16.9, luts=1531, ffs=419, throughput_msps=89.6, max_abs_err=8.09e-06 (2^-16.91), power_index=2.35
- pipelined_m [data_width=23 n_iter=20 angle_guard=3 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=2060, accuracy_bits=17.9, luts=1607, ffs=453, throughput_msps=89.6, max_abs_err=4.15e-06 (2^-17.88), power_index=2.48
- pipelined_m [data_width=25 n_iter=20 angle_guard=4 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=2384, accuracy_bits=18.9, luts=1867, ffs=517, throughput_msps=86, max_abs_err=2.05e-06 (2^-18.90), power_index=2.87
- pipelined_m [data_width=27 n_iter=29 angle_guard=-1 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=3552, accuracy_bits=20.5, luts=2602, ffs=950, throughput_msps=110, max_abs_err=6.81e-07 (2^-20.49), power_index=4.28
- pipelined_m [data_width=28 n_iter=28 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=3754, accuracy_bits=23.8, luts=2739, ffs=1015, throughput_msps=110, max_abs_err=6.73e-08 (2^-23.82), power_index=4.52
Front coverage: luts_plus_ffs 1165..3754 (HV reference 4000); accuracy_bits 12.4..23.8 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- pipelined: 32 evals, 3 feasible; max throughput seen 273 MSPS; best accuracy 14.64 bits; best feasible luts_plus_ffs=1843; feasible ranges: data_width 17..21, n_iter 16..16, angle_guard 0..0, frac_guard 0..2
- pipelined_m: 268 evals, 145 feasible; max throughput seen 178 MSPS; best accuracy 23.82 bits; best feasible luts_plus_ffs=1165; feasible ranges: data_width 16..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 29561 in, 2154 out
- provider-reported cost: $0.0807
- full prompts and replies: `llm_trace.jsonl`

