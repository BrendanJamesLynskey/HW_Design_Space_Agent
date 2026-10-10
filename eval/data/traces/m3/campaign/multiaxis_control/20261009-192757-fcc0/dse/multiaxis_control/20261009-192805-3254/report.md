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
`pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 841 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 282 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.35 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000235 (2^-12.06) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 7.7 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.91e-05 (2^-14.05) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.94 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.1 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 98.4 dBc, SNR 81.6 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=19,n_iter=15,angle_guard=-1,frac_guard=1,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (26 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 841 | 282 | 93.6 | 6 | 1.35 | 0.000235 (2^-12.06) | 12.06 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 855 | 289 | 93.6 | 6 | 1.38 | 0.000205 (2^-12.25) | 12.25 |
| 2 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 905 | 282 | 93.6 | 6 | 1.43 | 0.000174 (2^-12.49) | 12.49 |
| 3 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=4` | 941 | 285 | 93.6 | 6 | 1.48 | 0.00013 (2^-12.91) | 12.91 |
| 4 | `pipelined_m:data_width=19,n_iter=15,angle_guard=-1,frac_guard=1,rounding=trunc,m=4` | 949 | 299 | 93.6 | 6 | 1.5 | 0.000129 (2^-12.92) | 12.92 |
| 5 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=3` | 973 | 359 | 119.3 | 7 | 1.6 | 0.000101 (2^-13.27) | 13.27 |
| 6 | `pipelined_m:data_width=19,n_iter=15,angle_guard=0,frac_guard=2,rounding=round,m=3` | 1034 | 379 | 119.3 | 7 | 1.7 | 9.42e-05 (2^-13.37) | 13.37 |
| 7 | `pipelined_m:data_width=17,n_iter=17,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1070 | 347 | 93.6 | 7 | 1.71 | 9.28e-05 (2^-13.40) | 13.40 |
| 8 | `pipelined_m:data_width=21,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1112 | 337 | 93.6 | 6 | 1.74 | 6.53e-05 (2^-13.90) | 13.90 |
| 9 | `pipelined_m:data_width=23,n_iter=15,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1185 | 371 | 89.6 | 6 | 1.87 | 6.2e-05 (2^-13.98) | 13.98 |
| 10 | `pipelined_m:data_width=26,n_iter=15,angle_guard=1,frac_guard=0,rounding=trunc,m=4` | 1259 | 400 | 86.0 | 6 | 2 | 6.12e-05 (2^-14.00) | 14.00 |
| 11 | `pipelined_m:data_width=19,n_iter=17,angle_guard=2,frac_guard=3,rounding=trunc,m=3` | 1202 | 468 | 119.3 | 8 | 2.01 | 3.2e-05 (2^-14.93) | 14.93 |
| 12 | `pipelined_m:data_width=22,n_iter=18,angle_guard=3,frac_guard=0,rounding=round,m=4` | 1349 | 428 | 89.6 | 7 | 2.14 | 1.1e-05 (2^-16.47) | 16.47 |
| 13 | `pipelined_m:data_width=24,n_iter=18,angle_guard=-1,frac_guard=1,rounding=trunc,m=3` | 1420 | 531 | 114.5 | 8 | 2.35 | 9.83e-06 (2^-16.63) | 16.63 |
| 14 | `pipelined_m:data_width=22,n_iter=20,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1547 | 434 | 89.6 | 7 | 2.38 | 5.54e-06 (2^-17.46) | 17.46 |
| 15 | `pipelined_m:data_width=21,n_iter=21,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1630 | 500 | 89.6 | 8 | 2.56 | 5.47e-06 (2^-17.48) | 17.48 |
| 16 | `pipelined_m:data_width=22,n_iter=21,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1632 | 504 | 89.6 | 8 | 2.57 | 4.62e-06 (2^-17.72) | 17.72 |
| 17 | `pipelined_m:data_width=23,n_iter=21,angle_guard=1,frac_guard=1,rounding=trunc,m=3` | 1649 | 602 | 114.5 | 9 | 2.71 | 3.47e-06 (2^-18.14) | 18.14 |
| 18 | `pipelined_m:data_width=23,n_iter=23,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 1860 | 698 | 114.5 | 10 | 3.08 | 2.86e-06 (2^-18.42) | 18.42 |
| 19 | `pipelined_m:data_width=25,n_iter=22,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 1908 | 751 | 110.0 | 10 | 3.2 | 1e-06 (2^-19.93) | 19.93 |
| 20 | `pipelined_m:data_width=24,n_iter=23,angle_guard=3,frac_guard=2,rounding=round,m=3` | 2026 | 741 | 110.0 | 10 | 3.33 | 5.75e-07 (2^-20.73) | 20.73 |
| 21 | `pipelined_m:data_width=24,n_iter=24,angle_guard=3,frac_guard=3,rounding=round,m=3` | 2164 | 755 | 110.0 | 10 | 3.51 | 4.66e-07 (2^-21.03) | 21.03 |
| 22 | `pipelined_m:data_width=28,n_iter=23,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 2208 | 829 | 105.9 | 10 | 3.66 | 3.01e-07 (2^-21.66) | 21.66 |
| 23 | `pipelined_m:data_width=27,n_iter=24,angle_guard=4,frac_guard=2,rounding=round,m=3` | 2365 | 827 | 105.9 | 10 | 3.84 | 1.63e-07 (2^-22.55) | 22.55 |
| 24 | `pipelined_m:data_width=28,n_iter=24,angle_guard=3,frac_guard=3,rounding=trunc,m=3` | 2405 | 858 | 105.9 | 10 | 3.93 | 1.45e-07 (2^-22.72) | 22.72 |
| 25 | `pipelined_m:data_width=28,n_iter=28,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 2708 | 1023 | 105.9 | 12 | 4.49 | 1e-07 (2^-23.25) | 23.25 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The tick issues 32 requests at once and all must return within 0.44 us, so the unit needs at least 32 results/us with low queueing. That points to 1-result-per-cycle pipelined designs, and iterative is excluded as too slow. Max error <= 2^-12 needs W of about 14-16 bits and N of about 12-15 iterations, so the ranges are centred there with guard-bit variation. Most of the budget goes to pipelined_m and pipelined to find the cheapest LUT+FF point. A small unrolled_k share checks the alternative cheaply.*)
- `pipelined_m` (54 evals): data_width=12..18, n_iter=11..17, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* Gives 1 result per cycle, which covers the throughput and batch constraints. Registering only every m stages removes FFs, so it is the likely area-minimising family. Ranges target about 12-14 accuracy bits with some headroom for the accuracy objective.
- `pipelined` (32 evals): data_width=12..18, n_iter=11..17, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* This is the fully pipelined baseline with the highest Fmax and the shortest batch time. It anchors the front and shows whether the extra FFs of a register on every stage can be justified.
- `unrolled_k` (14 evals): data_width=12..16, n_iter=11..15, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=5..8. *Why:* A small probe of whether a high-k unrolled design can reach 32 results/us and the 0.44 us batch bound. It needs ceil(N/k)+3 cycles per result, so it is probably infeasible but would be much smaller if it passes.

**Result (code):** 100 evaluations this round, 100 total; 14 feasible; hypervolume 4004 (n/a).

**LLM decision:** `refine` — pipelined_m holds the whole front (best 1254 LUTs+FFs at 12.3 bits). The 14 feasible designs sit in a narrow region: data_width 17..18, n_iter 15..17, frac_guard 1..2, m 2..4. Only 14% of evaluations violate throughput, so the binding constraints are accuracy (64% violate) and the batch deadline (47% violate). Iterative is dropped without exploring. It needs N+3 cycles per result, and unrolled_k already shows 0 feasible designs with at most 10.1 MSPS against the 32 MSPS requirement. The best front point (m=4, 93.6 MSPS) is close to the batch-deadline limit, so m above about 5 is unlikely to help. Cheaper points are probably at slightly smaller data_width, n_iter and frac_guard, so I will concentrate the budget there. Plain pipelined stays as a small comparison, since its best feasible area is 1909.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 4004 (gain this round: n/a (first round)).
Feasible designs: 14 of 100 evaluations (12 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 14% violate; best seen 282
- max_abs_err <= 0.000244141: 64% violate; best seen 8.08e-05 (2^-13.60)
- sys_p99_batch_us <= 0.44: 47% violate; best seen 0.153

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=16 angle_guard=-1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1254, accuracy_bits=12.3, luts=969, ffs=285, throughput_msps=93.6, max_abs_err=0.000192 (2^-12.35), power_index=1.51
- pipelined_m [data_width=18 n_iter=17 angle_guard=-1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1381, accuracy_bits=12.5, luts=1034, ffs=347, throughput_msps=93.6, max_abs_err=0.000179 (2^-12.45), power_index=1.66
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=2] luts_plus_ffs=1459, accuracy_bits=12.5, luts=920, ffs=539, throughput_msps=164, max_abs_err=0.000175 (2^-12.48), power_index=1.76
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=1528, accuracy_bits=12.8, luts=985, ffs=543, throughput_msps=164, max_abs_err=0.000136 (2^-12.84), power_index=1.84
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=2] luts_plus_ffs=1598, accuracy_bits=13.6, luts=1033, ffs=565, throughput_msps=164, max_abs_err=8.08e-05 (2^-13.60), power_index=1.92
Front coverage: luts_plus_ffs 1254..1598 (HV reference 4000); accuracy_bits 12.3..13.6 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- unrolled_k: 14 evals, 0 feasible; max throughput seen 10.1 MSPS; best accuracy 10.89 bits
- pipelined: 32 evals, 6 feasible; max throughput seen 282 MSPS; best accuracy 13.39 bits; best feasible luts_plus_ffs=1909; feasible ranges: data_width 15..18, n_iter 15..17, angle_guard 0..3, frac_guard 1..2
- pipelined_m: 54 evals, 8 feasible; max throughput seen 178 MSPS; best accuracy 13.60 bits; best feasible luts_plus_ffs=1254; feasible ranges: data_width 17..18, n_iter 15..17, angle_guard -1..1, frac_guard 1..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate the budget on the region around the current front, with smaller sizes and both rounding modes, to reduce area while keeping error within 2^-12.*)
- `pipelined_m` (80 evals): data_width=14..18, n_iter=12..17, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..5. *Why:* This family holds the whole front. Probing smaller widths, iteration counts and guard bits, plus rounding, should find cheaper designs that still reach at least 12 bits.
- `pipelined` (20 evals): data_width=14..18, n_iter=12..17, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* It is a low-share check that the lower-width region does not beat pipelined_m on area. Its best feasible area so far is 1909.

**Result (code):** 100 evaluations this round, 200 total; 43 feasible; hypervolume 5704 (+42.5%).

**LLM decision:** `refine` — The front is still improving (HV +42.5% last round) and 8 feasible designs sit at luts_plus_ffs 1123..2299. The cheapest ones all come from pipelined_m with m=3..4, data_width 17..18 and n_iter 14..17. I am not adding iterative: unrolled_k, the other multi-cycle family, reached only 10.1 MSPS with 0 feasible designs. Iterative takes N+3 cycles per result, so it cannot meet throughput >= 32 MSPS or return 32 results within 0.44 us. pipelined_m with m=4 gives 93.6 MSPS, which passes the throughput and batch bounds. Next I will focus on pipelined_m around the feasible region and extend m to 5 to test cheaper area. I will also widen n_iter and data_width slightly in case a smaller design just meets 2^-12. A smaller share goes to pipelined, to push the high-accuracy end (14.4 bits at 2299).

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 5704 (gain this round: +42.5%).
Feasible designs: 43 of 200 evaluations (35 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 7% violate; best seen 282
- max_abs_err <= 0.000244141: 66% violate; best seen 4.73e-05 (2^-14.37)
- sys_p99_batch_us <= 0.44: 28% violate; best seen 0.153

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1123, accuracy_bits=12.1, luts=841, ffs=282, throughput_msps=93.6, max_abs_err=0.000235 (2^-12.06), power_index=1.35
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1143, accuracy_bits=12.3, luts=855, ffs=289, throughput_msps=93.6, max_abs_err=0.000205 (2^-12.25), power_index=1.38
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1204, accuracy_bits=12.5, luts=920, ffs=285, throughput_msps=93.6, max_abs_err=0.000175 (2^-12.48), power_index=1.45
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1226, accuracy_bits=12.9, luts=941, ffs=285, throughput_msps=93.6, max_abs_err=0.00013 (2^-12.91), power_index=1.48
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=1332, accuracy_bits=13.3, luts=973, ffs=359, throughput_msps=119, max_abs_err=0.000101 (2^-13.27), power_index=1.6
- pipelined_m [data_width=17 n_iter=17 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1417, accuracy_bits=13.4, luts=1070, ffs=347, throughput_msps=93.6, max_abs_err=9.28e-05 (2^-13.40), power_index=1.71
- pipelined_m [data_width=18 n_iter=17 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1468, accuracy_bits=13.7, luts=1051, ffs=418, throughput_msps=119, max_abs_err=7.75e-05 (2^-13.65), power_index=1.77
- pipelined [data_width=18 n_iter=17 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2299, accuracy_bits=14.4, luts=1156, ffs=1143, throughput_msps=264, max_abs_err=4.73e-05 (2^-14.37), power_index=2.77
Front coverage: luts_plus_ffs 1123..2299 (HV reference 4000); accuracy_bits 12.1..14.4 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- unrolled_k: 14 evals, 0 feasible; max throughput seen 10.1 MSPS; best accuracy 10.89 bits
- pipelined: 52 evals, 17 feasible; max throughput seen 282 MSPS; best accuracy 14.37 bits; best feasible luts_plus_ffs=1740; feasible ranges: data_width 15..18, n_iter 14..17, angle_guard 0..3, frac_guard 0..2
- pipelined_m: 134 evals, 26 feasible; max throughput seen 178 MSPS; best accuracy 13.65 bits; best feasible luts_plus_ffs=1123; feasible ranges: data_width 16..18, n_iter 14..17, angle_guard -1..2, frac_guard 0..2, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Concentrate the budget on the pipelined_m region that produced the cheapest feasible designs, with a smaller share for pipelined at the high-accuracy end. Iterative stays excluded because it cannot meet the throughput and batch bounds.*)
- `pipelined_m` (30 evals): data_width=15..19, n_iter=12..18, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, m=3..5. *Why:* All low-area front points are here. Probing m=5 and slightly smaller or larger width and iteration counts should shift the front to lower area and fill the accuracy range between 12.1 and 14.4 bits.
- `pipelined` (10 evals): data_width=16..20, n_iter=14..19, angle_guard=0..3, frac_guard=0..2, rounding=trunc|round. *Why:* It holds the only high-accuracy point (14.4 bits). Exploring slightly higher width and iteration counts extends the front at the accuracy end.

**Result (code):** 40 evaluations this round, 240 total; 62 feasible; hypervolume 8818 (+54.6%).

**LLM decision:** `stop` — This is the final round, so only stop or infeasible are allowed. The constraints are clearly reachable: the front has 9 feasible designs, all pipelined_m, with luts_plus_ffs from 1123 to 1787 and accuracy_bits from 12.1 to 15.5. The cheapest design (pipelined_m, W=17, N=14, m=4) has 1123 LUTs+FFs, max_abs_err 0.000235 (just inside 2^-12) and 93.6 MSPS against the 32 MSPS requirement. Hypervolume rose 54.6% last round, but with no rounds left, stopping is the only valid choice. unrolled_k never became feasible (0 of 14, max 10.1 MSPS), and the iterative family would also be far below the throughput needed for the 0.44 us batch bound.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 8818 (gain this round: +54.6%).
Feasible designs: 62 of 240 evaluations (52 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 6% violate; best seen 282
- max_abs_err <= 0.000244141: 61% violate; best seen 2.1e-05 (2^-15.54)
- sys_p99_batch_us <= 0.44: 26% violate; best seen 0.153

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1123, accuracy_bits=12.1, luts=841, ffs=282, throughput_msps=93.6, max_abs_err=0.000235 (2^-12.06), power_index=1.35
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1143, accuracy_bits=12.3, luts=855, ffs=289, throughput_msps=93.6, max_abs_err=0.000205 (2^-12.25), power_index=1.38
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1204, accuracy_bits=12.5, luts=920, ffs=285, throughput_msps=93.6, max_abs_err=0.000175 (2^-12.48), power_index=1.45
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1226, accuracy_bits=12.9, luts=941, ffs=285, throughput_msps=93.6, max_abs_err=0.00013 (2^-12.91), power_index=1.48
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=1332, accuracy_bits=13.3, luts=973, ffs=359, throughput_msps=119, max_abs_err=0.000101 (2^-13.27), power_index=1.6
- pipelined_m [data_width=17 n_iter=17 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1417, accuracy_bits=13.4, luts=1070, ffs=347, throughput_msps=93.6, max_abs_err=9.28e-05 (2^-13.40), power_index=1.71
- pipelined_m [data_width=18 n_iter=17 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1468, accuracy_bits=13.7, luts=1051, ffs=418, throughput_msps=119, max_abs_err=7.75e-05 (2^-13.65), power_index=1.77
- pipelined_m [data_width=19 n_iter=17 angle_guard=2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=1670, accuracy_bits=14.9, luts=1202, ffs=468, throughput_msps=119, max_abs_err=3.2e-05 (2^-14.93), power_index=2.01
- pipelined_m [data_width=19 n_iter=18 angle_guard=2 frac_guard=3 rounding=round m=3] luts_plus_ffs=1787, accuracy_bits=15.5, luts=1317, ffs=470, throughput_msps=119, max_abs_err=2.1e-05 (2^-15.54), power_index=2.15
Front coverage: luts_plus_ffs 1123..1787 (HV reference 4000); accuracy_bits 12.1..15.5 (HV reference 12); data_width on the front 17..19 (registry 8..28).

Per family:
- unrolled_k: 14 evals, 0 feasible; max throughput seen 10.1 MSPS; best accuracy 10.89 bits
- pipelined: 62 evals, 24 feasible; max throughput seen 282 MSPS; best accuracy 14.45 bits; best feasible luts_plus_ffs=1740; feasible ranges: data_width 15..19, n_iter 14..19, angle_guard 0..3, frac_guard 0..2
- pipelined_m: 164 evals, 38 feasible; max throughput seen 178 MSPS; best accuracy 15.54 bits; best feasible luts_plus_ffs=1123; feasible ranges: data_width 16..19, n_iter 14..18, angle_guard -1..2, frac_guard 0..3, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (160 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (9 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 160 feasible; hypervolume 1.952e+04 (+121.4%).

**No LLM call** (code's front-mapping round): This is the final round, so only stop or infeasible are allowed. The constraints are clearly reachable: the front has 9 feasible designs, all pipelined_m, with luts_plus_ffs from 1123 to 1787 and accuracy_bits from 12.1 to 15.5. The cheapest design (pipelined_m, W=17, N=14, m=4) has 1123 LUTs+FFs, max_abs_err 0.000235 (just inside 2^-12) and 93.6 MSPS against the 32 MSPS requirement. Hypervolume rose 54.6% last round, but with no rounds left, stopping is the only valid choice. unrolled_k never became feasible (0 of 14, max 10.1 MSPS), and the iterative family would also be far below the throughput needed for the 0.44 us batch bound.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.952e+04 (gain this round: +121.4%).
Feasible designs: 160 of 400 evaluations (138 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 4% violate; best seen 282
- max_abs_err <= 0.000244141: 40% violate; best seen 3.07e-08 (2^-24.96)
- sys_p99_batch_us <= 0.44: 30% violate; best seen 0.153

Pareto front (feasible, 26 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1123, accuracy_bits=12.1, luts=841, ffs=282, throughput_msps=93.6, max_abs_err=0.000235 (2^-12.06), power_index=1.35
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1226, accuracy_bits=12.9, luts=941, ffs=285, throughput_msps=93.6, max_abs_err=0.00013 (2^-12.91), power_index=1.48
- pipelined_m [data_width=19 n_iter=15 angle_guard=0 frac_guard=2 rounding=round m=3] luts_plus_ffs=1413, accuracy_bits=13.4, luts=1034, ffs=379, throughput_msps=119, max_abs_err=9.42e-05 (2^-13.37), power_index=1.7
- pipelined_m [data_width=21 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1449, accuracy_bits=13.9, luts=1112, ffs=337, throughput_msps=93.6, max_abs_err=6.53e-05 (2^-13.90), power_index=1.74
- pipelined_m [data_width=19 n_iter=17 angle_guard=2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=1670, accuracy_bits=14.9, luts=1202, ffs=468, throughput_msps=119, max_abs_err=3.2e-05 (2^-14.93), power_index=2.01
- pipelined_m [data_width=22 n_iter=20 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1981, accuracy_bits=17.5, luts=1547, ffs=434, throughput_msps=89.6, max_abs_err=5.54e-06 (2^-17.46), power_index=2.38
- pipelined_m [data_width=23 n_iter=21 angle_guard=1 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=2251, accuracy_bits=18.1, luts=1649, ffs=602, throughput_msps=114, max_abs_err=3.47e-06 (2^-18.14), power_index=2.71
- pipelined_m [data_width=25 n_iter=22 angle_guard=3 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=2659, accuracy_bits=19.9, luts=1908, ffs=751, throughput_msps=110, max_abs_err=1e-06 (2^-19.93), power_index=3.2
- pipelined_m [data_width=28 n_iter=23 angle_guard=3 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=3037, accuracy_bits=21.7, luts=2208, ffs=829, throughput_msps=106, max_abs_err=3.01e-07 (2^-21.66), power_index=3.66
- pipelined_m [data_width=28 n_iter=28 angle_guard=3 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=3731, accuracy_bits=23.3, luts=2708, ffs=1023, throughput_msps=106, max_abs_err=1e-07 (2^-23.25), power_index=4.49
Front coverage: luts_plus_ffs 1123..3731 (HV reference 4000); accuracy_bits 12.1..23.3 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- unrolled_k: 14 evals, 0 feasible; max throughput seen 10.1 MSPS; best accuracy 10.89 bits
- pipelined: 62 evals, 24 feasible; max throughput seen 282 MSPS; best accuracy 14.45 bits; best feasible luts_plus_ffs=1740; feasible ranges: data_width 15..19, n_iter 14..19, angle_guard 0..3, frac_guard 0..2
- pipelined_m: 324 evals, 136 feasible; max throughput seen 178 MSPS; best accuracy 24.96 bits; best feasible luts_plus_ffs=1123; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 6 (failed/unparsed attempts: 0)
- tokens: 35218 in, 4943 out
- provider-reported cost: $0.1199
- full prompts and replies: `llm_trace.jsonl`

