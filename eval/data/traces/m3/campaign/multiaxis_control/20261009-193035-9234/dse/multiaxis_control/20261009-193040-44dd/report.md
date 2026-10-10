# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: anthropic/claude-sonnet-5.5.  
**Evaluations:** 400 of 400 budgeted, over 4 round(s).  
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
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 834 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 270 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 61.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.33 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000209 (2^-12.22) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.43 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 6.44e-05 (2^-13.92) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 1.06 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.2 | exact: bit-accurate model, exhaustive (65536 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 5 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 94.8 dBc, SNR 80.9 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=15,n_iter=14,angle_guard=3,frac_guard=3,rounding=round,m=5` | 0.4342 → 0.4465 | no |
| `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=2,rounding=round,m=4` | 0.3848 → 0.3953 | yes |

**WINNER CHANGED AT L2**: the L1 selection pipelined_m:data_width=15,n_iter=14,angle_guard=3,frac_guard=3,rounding=round,m=5 fails the simulated system constraints (sys_p99_batch_us <= 0.44 by 1.5%); the best shortlisted design that passes is pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=4.

## Pareto front (28 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=14,angle_guard=3,frac_guard=3,rounding=round,m=5` | 859 | 211 | 80.6 | 5 | 1.29 | 0.000215 (2^-12.18) | 12.18 |
| 1 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=4` | 834 | 270 | 97.8 | 6 | 1.33 | 0.000209 (2^-12.22) | 12.22 |
| 2 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=4` | 876 | 276 | 93.6 | 6 | 1.39 | 0.000148 (2^-12.72) | 12.72 |
| 3 | `pipelined_m:data_width=17,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=4` | 938 | 276 | 93.6 | 6 | 1.46 | 0.000139 (2^-12.81) | 12.81 |
| 4 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=2,rounding=round,m=4` | 971 | 291 | 93.6 | 6 | 1.52 | 0.000108 (2^-13.18) | 13.18 |
| 5 | `pipelined_m:data_width=17,n_iter=16,angle_guard=3,frac_guard=1,rounding=round,m=4` | 1021 | 289 | 93.6 | 6 | 1.58 | 9.87e-05 (2^-13.31) | 13.31 |
| 6 | `pipelined_m:data_width=17,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1037 | 291 | 93.6 | 6 | 1.6 | 8.59e-05 (2^-13.51) | 13.51 |
| 7 | `pipelined_m:data_width=17,n_iter=16,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1053 | 295 | 93.6 | 6 | 1.62 | 6.9e-05 (2^-13.82) | 13.82 |
| 8 | `pipelined_m:data_width=19,n_iter=17,angle_guard=1,frac_guard=3,rounding=round,m=3` | 1226 | 464 | 119.3 | 8 | 2.03 | 3.78e-05 (2^-14.69) | 14.69 |
| 9 | `pipelined_m:data_width=23,n_iter=17,angle_guard=0,frac_guard=2,rounding=trunc,m=4` | 1337 | 446 | 89.6 | 7 | 2.15 | 1.73e-05 (2^-15.82) | 15.82 |
| 10 | `pipelined_m:data_width=23,n_iter=17,angle_guard=1,frac_guard=3,rounding=round,m=4` | 1436 | 461 | 89.6 | 7 | 2.28 | 1.6e-05 (2^-15.93) | 15.93 |
| 11 | `pipelined_m:data_width=22,n_iter=19,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1474 | 428 | 89.6 | 7 | 2.29 | 7.47e-06 (2^-17.03) | 17.03 |
| 12 | `pipelined_m:data_width=23,n_iter=19,angle_guard=0,frac_guard=2,rounding=trunc,m=4` | 1504 | 446 | 89.6 | 7 | 2.35 | 6.49e-06 (2^-17.23) | 17.23 |
| 13 | `pipelined_m:data_width=23,n_iter=19,angle_guard=0,frac_guard=1,rounding=round,m=4` | 1514 | 440 | 89.6 | 7 | 2.35 | 6.39e-06 (2^-17.25) | 17.25 |
| 14 | `pipelined_m:data_width=23,n_iter=22,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 1709 | 517 | 89.6 | 8 | 2.68 | 4.14e-06 (2^-17.88) | 17.88 |
| 15 | `pipelined_m:data_width=23,n_iter=22,angle_guard=0,frac_guard=1,rounding=round,m=4` | 1758 | 519 | 89.6 | 8 | 2.74 | 3.95e-06 (2^-17.95) | 17.95 |
| 16 | `pipelined_m:data_width=23,n_iter=22,angle_guard=0,frac_guard=2,rounding=trunc,m=4` | 1753 | 527 | 89.6 | 8 | 2.74 | 3.59e-06 (2^-18.09) | 18.09 |
| 17 | `pipelined_m:data_width=23,n_iter=22,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1780 | 525 | 89.6 | 8 | 2.77 | 2.54e-06 (2^-18.58) | 18.58 |
| 18 | `pipelined_m:data_width=23,n_iter=22,angle_guard=3,frac_guard=1,rounding=round,m=4` | 1824 | 537 | 89.6 | 8 | 2.84 | 1.84e-06 (2^-19.05) | 19.05 |
| 19 | `pipelined_m:data_width=25,n_iter=22,angle_guard=3,frac_guard=0,rounding=trunc,m=3` | 1864 | 737 | 110.0 | 10 | 3.13 | 1.53e-06 (2^-19.31) | 19.31 |
| 20 | `pipelined_m:data_width=25,n_iter=22,angle_guard=4,frac_guard=0,rounding=round,m=3` | 1886 | 745 | 110.0 | 10 | 3.17 | 1.06e-06 (2^-19.85) | 19.85 |
| 21 | `pipelined_m:data_width=25,n_iter=23,angle_guard=4,frac_guard=0,rounding=round,m=3` | 1976 | 745 | 110.0 | 10 | 3.27 | 8.49e-07 (2^-20.17) | 20.17 |
| 22 | `pipelined_m:data_width=25,n_iter=22,angle_guard=4,frac_guard=3,rounding=round,m=3` | 2072 | 789 | 110.0 | 10 | 3.44 | 6.1e-07 (2^-20.65) | 20.65 |
| 23 | `pipelined_m:data_width=28,n_iter=23,angle_guard=-1,frac_guard=2,rounding=round,m=3` | 2220 | 813 | 110.0 | 10 | 3.65 | 3.88e-07 (2^-21.30) | 21.30 |
| 24 | `pipelined_m:data_width=28,n_iter=23,angle_guard=3,frac_guard=2,rounding=round,m=3` | 2313 | 845 | 105.9 | 10 | 3.8 | 2.6e-07 (2^-21.87) | 21.87 |
| 25 | `pipelined_m:data_width=26,n_iter=28,angle_guard=3,frac_guard=3,rounding=round,m=3` | 2706 | 997 | 110.0 | 12 | 4.46 | 1.22e-07 (2^-22.97) | 22.97 |
| 26 | `pipelined_m:data_width=28,n_iter=27,angle_guard=3,frac_guard=3,rounding=round,m=3` | 2777 | 960 | 105.9 | 11 | 4.5 | 3.85e-08 (2^-24.63) | 24.63 |
| 27 | `pipelined_m:data_width=28,n_iter=29,angle_guard=3,frac_guard=2,rounding=round,m=2` | 2926 | 1538 | 147.4 | 17 | 5.37 | 3.6e-08 (2^-24.73) | 24.73 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *32 results within 0.44 us needs about 73 Msps effective throughput. Iterative and unrolled_k accept one request every several cycles, so they would queue the burst and likely miss both the throughput and batch constraints; they are excluded for now. Only the pipelined families accept one request per cycle, so the 32-request burst plus latency has to fit in 0.44 us. Max error <= 2^-12 needs roughly 14-16 bit width and 12-14 iterations, so the ranges are centred there with some margin on each side. The search is over width, iterations and guard bits to find the cheapest design that still meets accuracy. pipelined_m gets the larger share because it targets minimum area; pipelined provides the fast baseline.*)
- `pipelined_m` (55 evals): data_width=12..18, n_iter=10..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, m=2..6. *Why:* Registering every m stages cuts FFs, which should lower LUTs+FFs. 1 result/cycle should still deliver the 32-result batch in time if Fmax holds up at moderate m.
- `pipelined` (45 evals): data_width=12..18, n_iter=10..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* Full pipeline gives the highest Fmax and 1 result/cycle, so it is the safe way to meet the 0.44 us batch bound. It serves as the baseline for the area trade-off.

**Result (code):** 100 evaluations this round, 100 total; 20 feasible; hypervolume 3553 (n/a).

**LLM decision:** `refine` — The cheapest feasible design is pipelined_m (1104 LUTs+FFs, 12.2 bits, m=4), but only 2 of its 55 evaluations were feasible. Most of its budget went to infeasible regions. The error constraint (<=2^-12) is the main filter, since 76% of evaluations violate it. The feasible pipelined_m designs sit at data_width 16, n_iter 14, angle_guard 2 and m 2..4, so a tighter search there should find cheaper and more accurate points. Pipelined feasible designs cluster at data_width 17..18 and n_iter 14..16, with front area 1768..2081. Iterative and unrolled_k are not worth a round. All 32 results must return within 0.44 us, and these families take N+3 or ceil(N/k)+3 cycles per result, so they would queue the burst. The requirement of 32 results/us on average also favours one result per cycle. The front spans only 12.2..13.6 bits against an HV reference of 12, so the gain lies in cheaper low-area points and in the m choice.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 3553 (gain this round: n/a (first round)).
Feasible designs: 20 of 100 evaluations (18 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 76% violate; best seen 8.08e-05 (2^-13.60)
- sys_p99_batch_us <= 0.44: 29% violate; best seen 0.154

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1104, accuracy_bits=12.2, luts=834, ffs=270, throughput_msps=97.8, max_abs_err=0.000209 (2^-12.22), power_index=1.33
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=3 rounding=round m=2] luts_plus_ffs=1361, accuracy_bits=12.4, luts=888, ffs=473, throughput_msps=164, max_abs_err=0.000187 (2^-12.38), power_index=1.64
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=1768, accuracy_bits=12.5, luts=868, ffs=900, throughput_msps=264, max_abs_err=0.000172 (2^-12.50), power_index=2.13
- pipelined [data_width=17 n_iter=14 angle_guard=1 frac_guard=3 rounding=round] luts_plus_ffs=1826, accuracy_bits=12.5, luts=918, ffs=908, throughput_msps=264, max_abs_err=0.000168 (2^-12.54), power_index=2.2
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=1955, accuracy_bits=13.3, luts=964, ffs=991, throughput_msps=264, max_abs_err=0.000102 (2^-13.26), power_index=2.35
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=3 rounding=round] luts_plus_ffs=1989, accuracy_bits=13.3, luts=1000, ffs=989, throughput_msps=264, max_abs_err=9.76e-05 (2^-13.32), power_index=2.39
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=2019, accuracy_bits=13.4, luts=1015, ffs=1004, throughput_msps=264, max_abs_err=8.99e-05 (2^-13.44), power_index=2.43
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2025, accuracy_bits=13.6, luts=1017, ffs=1008, throughput_msps=264, max_abs_err=8.26e-05 (2^-13.56), power_index=2.44
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=3 rounding=round] luts_plus_ffs=2081, accuracy_bits=13.6, luts=1046, ffs=1034, throughput_msps=264, max_abs_err=8.08e-05 (2^-13.60), power_index=2.5
Front coverage: luts_plus_ffs 1104..2081 (HV reference 4000); accuracy_bits 12.2..13.6 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 45 evals, 18 feasible; max throughput seen 282 MSPS; best accuracy 13.60 bits; best feasible luts_plus_ffs=1768; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 55 evals, 2 feasible; max throughput seen 178 MSPS; best accuracy 12.74 bits; best feasible luts_plus_ffs=1104; feasible ranges: data_width 16..16, n_iter 14..14, angle_guard 2..2, frac_guard 1..3, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate the budget on the pipelined_m region that shows feasibility, with smaller widths and iteration counts to reduce area, and keep pipelined as a secondary family for the high-accuracy end.*)
- `pipelined_m` (75 evals): data_width=14..17, n_iter=12..15, angle_guard=1..3, frac_guard=0..3, rounding=round|trunc, m=2..5. *Why:* Holds the cheapest front point (1104) and has the few feasible designs, so it needs the most focused sampling around data_width 16, n_iter 14 and small m.
- `pipelined` (25 evals): data_width=15..18, n_iter=13..16, angle_guard=0..3, frac_guard=0..3, rounding=round|trunc. *Why:* Feasible designs were consistent here; it extends the front at higher accuracy and probes slightly narrower widths for lower area.

**Result (code):** 100 evaluations this round, 200 total; 70 feasible; hypervolume 5438 (+53.1%).

**LLM decision:** `refine` — Both families explored so far are feasible, and pipelined_m holds the cheapest points (luts_plus_ffs 1070..1383), which is where the selection rule picks. pipelined is only competitive at the high-accuracy end (2025..2194). I am not adding iterative or unrolled_k. Their results come every N/k+3 cycles or more, so 32 back-to-back requests would take well over 0.44 us. Throughput would also likely fall below the 32 MSPS constraint, and I have no result that shows otherwise. The error constraint cuts out 62% of evaluations, and feasible pipelined_m designs sit at data_width 15..17, n_iter 14..15 and m 2..5. The best sys_p99_batch_us seen is 0.154 against the 0.44 bound, so there is room to push m higher to save FFs. I will concentrate the budget on pipelined_m with slightly wider m and smaller data_width/n_iter, and keep a small pipelined share to fill the gap between 1383 and 2025.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 5438 (gain this round: +53.1%).
Feasible designs: 70 of 200 evaluations (49 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 62% violate; best seen 5.17e-05 (2^-14.24)
- sys_p99_batch_us <= 0.44: 15% violate; best seen 0.154

Pareto front (feasible, 11 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=3 frac_guard=3 rounding=round m=5] luts_plus_ffs=1070, accuracy_bits=12.2, luts=859, ffs=211, throughput_msps=80.6, max_abs_err=0.000215 (2^-12.18), power_index=1.29
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1104, accuracy_bits=12.2, luts=834, ffs=270, throughput_msps=97.8, max_abs_err=0.000209 (2^-12.22), power_index=1.33
- pipelined_m [data_width=17 n_iter=15 angle_guard=3 frac_guard=0 rounding=round m=3] luts_plus_ffs=1232, accuracy_bits=12.6, luts=890, ffs=342, throughput_msps=119, max_abs_err=0.000164 (2^-12.58), power_index=1.48
- pipelined_m [data_width=16 n_iter=15 angle_guard=3 frac_guard=2 rounding=round m=3] luts_plus_ffs=1282, accuracy_bits=12.9, luts=939, ffs=343, throughput_msps=119, max_abs_err=0.000128 (2^-12.93), power_index=1.54
- pipelined_m [data_width=16 n_iter=15 angle_guard=3 frac_guard=3 rounding=round m=3] luts_plus_ffs=1320, accuracy_bits=13.1, luts=968, ffs=351, throughput_msps=119, max_abs_err=0.000117 (2^-13.06), power_index=1.59
- pipelined_m [data_width=17 n_iter=15 angle_guard=3 frac_guard=3 rounding=round m=3] luts_plus_ffs=1383, accuracy_bits=13.4, luts=1015, ffs=368, throughput_msps=119, max_abs_err=8.99e-05 (2^-13.44), power_index=1.66
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2025, accuracy_bits=13.6, luts=1017, ffs=1008, throughput_msps=264, max_abs_err=8.26e-05 (2^-13.56), power_index=2.44
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=3 rounding=round] luts_plus_ffs=2081, accuracy_bits=13.6, luts=1046, ffs=1034, throughput_msps=264, max_abs_err=8.08e-05 (2^-13.60), power_index=2.5
- pipelined [data_width=17 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=2096, accuracy_bits=13.8, luts=1053, ffs=1043, throughput_msps=264, max_abs_err=6.9e-05 (2^-13.82), power_index=2.52
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=2194, accuracy_bits=14.2, luts=1102, ffs=1092, throughput_msps=264, max_abs_err=5.17e-05 (2^-14.24), power_index=2.64
Front coverage: luts_plus_ffs 1070..2194 (HV reference 4000); accuracy_bits 12.2..14.2 (HV reference 12); data_width on the front 15..18 (registry 8..28).

Per family:
- pipelined: 70 evals, 33 feasible; max throughput seen 282 MSPS; best accuracy 14.24 bits; best feasible luts_plus_ffs=1713; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 130 evals, 37 feasible; max throughput seen 178 MSPS; best accuracy 13.44 bits; best feasible luts_plus_ffs=1070; feasible ranges: data_width 15..17, n_iter 14..15, angle_guard 1..3, frac_guard 0..3, m 2..5
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Focus on pipelined_m near the feasibility boundary to lower the minimum LUTs+FFs. Keep a small pipelined share for the front's accuracy end.*)
- `pipelined_m` (32 evals): data_width=14..17, n_iter=13..16, angle_guard=1..3, frac_guard=0..3, rounding=round, m=3..7. *Why:* Cheapest feasible region. Larger m cuts FFs while the batch-latency bound still has margin, and data_width 14..17 / n_iter 13..16 probe the 2^-12 error edge and the accuracy gap.
- `pipelined` (8 evals): data_width=15..18, n_iter=14..16, angle_guard=1..3, frac_guard=0..3, rounding=round. *Why:* Fills the 1400..2000 gap and the high-accuracy end of the front at one result per cycle.

**Result (code):** 40 evaluations this round, 240 total; 90 feasible; hypervolume 5871 (+8.0%).

**LLM decision:** `stop` — This is the final round, so stop is the only valid choice. The front has 10 feasible designs with luts_plus_ffs from 1070 to 2222 and accuracy_bits from 12.2 to 14.3, and it satisfies all three constraints. The cheapest design, pipelined_m at W=15, N=14, round, m=5, has 1070 LUTs+FFs, 12.2 accuracy bits, 80.6 MSPS against the 32 required, and max error 0.000215 against the 0.000244 limit. Round 3 still raised hypervolume by 8.0%, so the front is not fully saturated. Iterative and unrolled_k remain unexplored. They would accept only one request every several cycles, which risks the 0.44 us batch bound for 32 simultaneous requests, so they are unlikely to be a safe win. The remaining budget is reserved for code-driven front mapping.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 5871 (gain this round: +8.0%).
Feasible designs: 90 of 240 evaluations (67 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 57% violate; best seen 5.03e-05 (2^-14.28)
- sys_p99_batch_us <= 0.44: 18% violate; best seen 0.154

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=3 frac_guard=3 rounding=round m=5] luts_plus_ffs=1070, accuracy_bits=12.2, luts=859, ffs=211, throughput_msps=80.6, max_abs_err=0.000215 (2^-12.18), power_index=1.29
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1104, accuracy_bits=12.2, luts=834, ffs=270, throughput_msps=97.8, max_abs_err=0.000209 (2^-12.22), power_index=1.33
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1152, accuracy_bits=12.7, luts=876, ffs=276, throughput_msps=93.6, max_abs_err=0.000148 (2^-12.72), power_index=1.39
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1214, accuracy_bits=12.8, luts=938, ffs=276, throughput_msps=93.6, max_abs_err=0.000139 (2^-12.81), power_index=1.46
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1261, accuracy_bits=13.2, luts=971, ffs=291, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=1.52
- pipelined_m [data_width=17 n_iter=16 angle_guard=3 frac_guard=1 rounding=round m=4] luts_plus_ffs=1310, accuracy_bits=13.3, luts=1021, ffs=289, throughput_msps=93.6, max_abs_err=9.87e-05 (2^-13.31), power_index=1.58
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1327, accuracy_bits=13.5, luts=1037, ffs=291, throughput_msps=93.6, max_abs_err=8.59e-05 (2^-13.51), power_index=1.6
- pipelined_m [data_width=17 n_iter=16 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1347, accuracy_bits=13.8, luts=1053, ffs=295, throughput_msps=93.6, max_abs_err=6.9e-05 (2^-13.82), power_index=1.62
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=2194, accuracy_bits=14.2, luts=1102, ffs=1092, throughput_msps=264, max_abs_err=5.17e-05 (2^-14.24), power_index=2.64
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=3 rounding=round] luts_plus_ffs=2222, accuracy_bits=14.3, luts=1118, ffs=1104, throughput_msps=264, max_abs_err=5.03e-05 (2^-14.28), power_index=2.67
Front coverage: luts_plus_ffs 1070..2222 (HV reference 4000); accuracy_bits 12.2..14.3 (HV reference 12); data_width on the front 15..18 (registry 8..28).

Per family:
- pipelined: 78 evals, 37 feasible; max throughput seen 282 MSPS; best accuracy 14.28 bits; best feasible luts_plus_ffs=1689; feasible ranges: data_width 15..18, n_iter 14..16, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 162 evals, 53 feasible; max throughput seen 178 MSPS; best accuracy 13.82 bits; best feasible luts_plus_ffs=1070; feasible ranges: data_width 15..17, n_iter 14..16, angle_guard 1..3, frac_guard 0..3, m 2..5
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (128 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (8 front designs; box front_anchored)
- `pipelined` (32 evals): data_width=17..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (2 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 196 feasible; hypervolume 1.956e+04 (+233.1%).

**No LLM call** (code's front-mapping round): This is the final round, so stop is the only valid choice. The front has 10 feasible designs with luts_plus_ffs from 1070 to 2222 and accuracy_bits from 12.2 to 14.3, and it satisfies all three constraints. The cheapest design, pipelined_m at W=15, N=14, round, m=5, has 1070 LUTs+FFs, 12.2 accuracy bits, 80.6 MSPS against the 32 required, and max error 0.000215 against the 0.000244 limit. Round 3 still raised hypervolume by 8.0%, so the front is not fully saturated. Iterative and unrolled_k remain unexplored. They would accept only one request every several cycles, which risks the 0.44 us batch bound for 32 simultaneous requests, so they are unlikely to be a safe win. The remaining budget is reserved for code-driven front mapping.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.956e+04 (gain this round: +233.1%).
Feasible designs: 196 of 400 evaluations (162 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 38% violate; best seen 3.6e-08 (2^-24.73)
- sys_p99_batch_us <= 0.44: 21% violate; best seen 0.154

Pareto front (feasible, 28 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=3 frac_guard=3 rounding=round m=5] luts_plus_ffs=1070, accuracy_bits=12.2, luts=859, ffs=211, throughput_msps=80.6, max_abs_err=0.000215 (2^-12.18), power_index=1.29
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1214, accuracy_bits=12.8, luts=938, ffs=276, throughput_msps=93.6, max_abs_err=0.000139 (2^-12.81), power_index=1.46
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1327, accuracy_bits=13.5, luts=1037, ffs=291, throughput_msps=93.6, max_abs_err=8.59e-05 (2^-13.51), power_index=1.6
- pipelined_m [data_width=23 n_iter=17 angle_guard=0 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1783, accuracy_bits=15.8, luts=1337, ffs=446, throughput_msps=89.6, max_abs_err=1.73e-05 (2^-15.82), power_index=2.15
- pipelined_m [data_width=23 n_iter=19 angle_guard=0 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1950, accuracy_bits=17.2, luts=1504, ffs=446, throughput_msps=89.6, max_abs_err=6.49e-06 (2^-17.23), power_index=2.35
- pipelined_m [data_width=23 n_iter=22 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=2276, accuracy_bits=17.9, luts=1758, ffs=519, throughput_msps=89.6, max_abs_err=3.95e-06 (2^-17.95), power_index=2.74
- pipelined_m [data_width=23 n_iter=22 angle_guard=3 frac_guard=1 rounding=round m=4] luts_plus_ffs=2361, accuracy_bits=19, luts=1824, ffs=537, throughput_msps=89.6, max_abs_err=1.84e-06 (2^-19.05), power_index=2.84
- pipelined_m [data_width=25 n_iter=23 angle_guard=4 frac_guard=0 rounding=round m=3] luts_plus_ffs=2720, accuracy_bits=20.2, luts=1976, ffs=745, throughput_msps=110, max_abs_err=8.49e-07 (2^-20.17), power_index=3.27
- pipelined_m [data_width=28 n_iter=23 angle_guard=3 frac_guard=2 rounding=round m=3] luts_plus_ffs=3158, accuracy_bits=21.9, luts=2313, ffs=845, throughput_msps=106, max_abs_err=2.6e-07 (2^-21.87), power_index=3.8
- pipelined_m [data_width=28 n_iter=29 angle_guard=3 frac_guard=2 rounding=round m=2] luts_plus_ffs=4464, accuracy_bits=24.7, luts=2926, ffs=1538, throughput_msps=147, max_abs_err=3.6e-08 (2^-24.73), power_index=5.37
Front coverage: luts_plus_ffs 1070..4464 (HV reference 4000); accuracy_bits 12.2..24.7 (HV reference 12); data_width on the front 15..28 (registry 8..28).

Per family:
- pipelined: 110 evals, 69 feasible; max throughput seen 282 MSPS; best accuracy 20.86 bits; best feasible luts_plus_ffs=1689; feasible ranges: data_width 15..28, n_iter 14..29, angle_guard -2..3, frac_guard 0..4
- pipelined_m: 290 evals, 127 feasible; max throughput seen 178 MSPS; best accuracy 24.73 bits; best feasible luts_plus_ffs=1070; feasible ranges: data_width 15..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..5
```
</details>

## LLM usage
- calls: 6 (failed/unparsed attempts: 0)
- tokens: 35827 in, 4976 out
- provider-reported cost: $0.1214
- full prompts and replies: `llm_trace.jsonl`

