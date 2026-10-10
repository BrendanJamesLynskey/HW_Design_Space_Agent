# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 400 of 400 budgeted, over 5 round(s).  
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
`pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 841 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 287 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.36 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00024 (2^-12.03) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 15.7 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.81e-05 (2^-14.07) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.81 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 98.4 dBc, SNR 81.7 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=0,frac_guard=2,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=3,frac_guard=2,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (36 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=trunc,m=4` | 841 | 287 | 93.6 | 6 | 1.36 | 0.00024 (2^-12.03) | 12.03 |
| 1 | `pipelined_m:data_width=17,n_iter=15,angle_guard=0,frac_guard=2,rounding=trunc,m=4` | 905 | 280 | 93.6 | 6 | 1.43 | 0.000217 (2^-12.17) | 12.17 |
| 2 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=trunc,m=4` | 905 | 287 | 93.6 | 6 | 1.43 | 0.000194 (2^-12.33) | 12.33 |
| 3 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 920 | 285 | 93.6 | 6 | 1.45 | 0.000175 (2^-12.48) | 12.48 |
| 4 | `pipelined_m:data_width=17,n_iter=15,angle_guard=3,frac_guard=2,rounding=trunc,m=4` | 949 | 293 | 93.6 | 6 | 1.5 | 0.00013 (2^-12.91) | 12.91 |
| 5 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=4` | 969 | 287 | 93.6 | 6 | 1.51 | 0.000108 (2^-13.18) | 13.18 |
| 6 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=4` | 973 | 295 | 93.6 | 6 | 1.53 | 0.000101 (2^-13.27) | 13.27 |
| 7 | `pipelined_m:data_width=17,n_iter=15,angle_guard=3,frac_guard=2,rounding=round,m=4` | 985 | 295 | 93.6 | 6 | 1.54 | 9.31e-05 (2^-13.39) | 13.39 |
| 8 | `pipelined_m:data_width=19,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1008 | 313 | 93.6 | 6 | 1.59 | 8.04e-05 (2^-13.60) | 13.60 |
| 9 | `pipelined_m:data_width=19,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1023 | 317 | 93.6 | 6 | 1.61 | 7.77e-05 (2^-13.65) | 13.65 |
| 10 | `pipelined_m:data_width=19,n_iter=15,angle_guard=3,frac_guard=2,rounding=trunc,m=4` | 1038 | 321 | 93.6 | 6 | 1.64 | 7.72e-05 (2^-13.66) | 13.66 |
| 11 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1071 | 301 | 93.6 | 6 | 1.65 | 7.47e-05 (2^-13.71) | 13.71 |
| 12 | `pipelined_m:data_width=20,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1053 | 327 | 93.6 | 6 | 1.66 | 7.38e-05 (2^-13.73) | 13.73 |
| 13 | `pipelined_m:data_width=20,n_iter=15,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1053 | 329 | 89.6 | 6 | 1.66 | 7.32e-05 (2^-13.74) | 13.74 |
| 14 | `pipelined_m:data_width=20,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1065 | 323 | 93.6 | 6 | 1.67 | 7.02e-05 (2^-13.80) | 13.80 |
| 15 | `pipelined_m:data_width=20,n_iter=16,angle_guard=0,frac_guard=1,rounding=round,m=4` | 1122 | 319 | 93.6 | 6 | 1.73 | 5.03e-05 (2^-14.28) | 14.28 |
| 16 | `pipelined_m:data_width=18,n_iter=19,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1257 | 364 | 93.6 | 7 | 1.95 | 5.02e-05 (2^-14.28) | 14.28 |
| 17 | `pipelined_m:data_width=25,n_iter=16,angle_guard=-1,frac_guard=0,rounding=round,m=4` | 1270 | 377 | 89.6 | 6 | 1.98 | 3.15e-05 (2^-14.95) | 14.95 |
| 18 | `pipelined_m:data_width=19,n_iter=19,angle_guard=3,frac_guard=1,rounding=round,m=4` | 1335 | 386 | 93.6 | 7 | 2.07 | 2.28e-05 (2^-15.42) | 15.42 |
| 19 | `pipelined_m:data_width=20,n_iter=19,angle_guard=3,frac_guard=2,rounding=trunc,m=4` | 1390 | 410 | 89.6 | 7 | 2.17 | 1.63e-05 (2^-15.90) | 15.90 |
| 20 | `pipelined_m:data_width=22,n_iter=18,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1385 | 434 | 89.6 | 7 | 2.19 | 1.1e-05 (2^-16.48) | 16.48 |
| 21 | `pipelined_m:data_width=23,n_iter=18,angle_guard=2,frac_guard=0,rounding=trunc,m=4` | 1385 | 440 | 89.6 | 7 | 2.2 | 1.07e-05 (2^-16.51) | 16.51 |
| 22 | `pipelined_m:data_width=22,n_iter=18,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1403 | 439 | 89.6 | 7 | 2.22 | 1.01e-05 (2^-16.60) | 16.60 |
| 23 | `pipelined_m:data_width=22,n_iter=20,angle_guard=2,frac_guard=0,rounding=round,m=4` | 1487 | 423 | 89.6 | 7 | 2.3 | 6.45e-06 (2^-17.24) | 17.24 |
| 24 | `pipelined_m:data_width=22,n_iter=20,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1573 | 433 | 89.6 | 7 | 2.41 | 4.46e-06 (2^-17.77) | 17.77 |
| 25 | `pipelined_m:data_width=22,n_iter=20,angle_guard=2,frac_guard=3,rounding=trunc,m=4` | 1607 | 447 | 89.6 | 7 | 2.47 | 4.33e-06 (2^-17.82) | 17.82 |
| 26 | `pipelined_m:data_width=23,n_iter=20,angle_guard=4,frac_guard=1,rounding=round,m=4` | 1675 | 460 | 86.0 | 7 | 2.57 | 2.88e-06 (2^-18.40) | 18.40 |
| 27 | `pipelined_m:data_width=25,n_iter=21,angle_guard=-1,frac_guard=0,rounding=round,m=4` | 1691 | 541 | 89.6 | 8 | 2.69 | 2.56e-06 (2^-18.58) | 18.58 |
| 28 | `pipelined_m:data_width=23,n_iter=21,angle_guard=3,frac_guard=1,rounding=round,m=3` | 1740 | 618 | 114.5 | 9 | 2.84 | 2.29e-06 (2^-18.74) | 18.74 |
| 29 | `pipelined_m:data_width=27,n_iter=21,angle_guard=-1,frac_guard=0,rounding=trunc,m=3` | 1818 | 669 | 110.0 | 9 | 2.99 | 1.44e-06 (2^-19.40) | 19.40 |
| 30 | `pipelined_m:data_width=27,n_iter=21,angle_guard=-1,frac_guard=1,rounding=round,m=3` | 1917 | 683 | 110.0 | 9 | 3.13 | 1.38e-06 (2^-19.47) | 19.47 |
| 31 | `pipelined_m:data_width=26,n_iter=22,angle_guard=4,frac_guard=0,rounding=trunc,m=3` | 1953 | 771 | 110.0 | 10 | 3.28 | 1e-06 (2^-19.93) | 19.93 |
| 32 | `pipelined_m:data_width=28,n_iter=21,angle_guard=2,frac_guard=2,rounding=round,m=3` | 2087 | 740 | 110.0 | 9 | 3.4 | 9.72e-07 (2^-19.97) | 19.97 |
| 33 | `pipelined_m:data_width=27,n_iter=23,angle_guard=2,frac_guard=1,rounding=round,m=3` | 2172 | 797 | 110.0 | 10 | 3.57 | 3.26e-07 (2^-21.55) | 21.55 |
| 34 | `pipelined_m:data_width=28,n_iter=23,angle_guard=2,frac_guard=4,rounding=round,m=2` | 2383 | 1273 | 147.4 | 14 | 4.4 | 2.57e-07 (2^-21.89) | 21.89 |
| 35 | `pipelined_m:data_width=28,n_iter=25,angle_guard=2,frac_guard=2,rounding=round,m=2` | 2492 | 1327 | 152.6 | 15 | 4.6 | 9.27e-08 (2^-23.36) | 23.36 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec needs 32 results/us with a 0.44 us p99 batch deadline, so only 1-result-per-cycle families (pipelined, pipelined_m) can plausibly satisfy the system constraint; unrolled_k with large k is a long shot and iterative is a low-area anchor. Accuracy needs >=12 bits (max_abs_err <= 2^-12), so I keep W and N high enough to leave margin for the L2-simulated re-selection, while focusing the search on the low-area end of the pipelined families since luts_plus_ffs is the objective and the selection rule.*)
- `pipelined` (40 evals): data_width=14..20, n_iter=12..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* 1 result/cycle is the only way to absorb a 32-request burst within 0.44 us; full pipelining gives the highest Fmax, and W=14..20 with N=12..20 should clear 12 accuracy bits with margin while keeping area low.
- `pipelined_m` (30 evals): data_width=14..20, n_iter=12..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, m=2..4. *Why:* Registering every m stages trades Fmax for fewer FFs; m=2..4 may reach the same 1 result/cycle throughput with lower area, which is the primary objective.
- `unrolled_k` (20 evals): data_width=14..20, n_iter=12..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, k=4..8. *Why:* High k (4..8) gives 1 result every few cycles with a shared datapath; worth checking whether it can still meet the 32 Msps / 0.44 us burst bound at lower area than a full pipeline.
- `iterative` (10 evals): data_width=14..20, n_iter=12..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* Smallest area family; included as a low-area reference point, though N+3 cycles/result likely cannot serve 32 requests/us, so it mainly anchors the Pareto front.

**Result (code):** 100 evaluations this round, 100 total; 50 feasible; hypervolume 9921 (n/a).

**LLM decision:** `refine` — Round 1 shows the front is entirely pipelined_m (8 of 9 points) plus one pipelined point, and the cheap end is where the selection rule (min luts_plus_ffs) lives. Two facts say that cheap end is under-explored, not exhausted: (1) pipelined_m got only 30 evals and its reported feasible data_width range is 18..20, yet the pipelined family — which computes identical bits for the same data_width/n_iter/guards/rounding — found data_width 15 feasible. So accuracy >= 2^-12 is reachable well below data_width 18, and a pipelined_m design at data_width 14..17 with enough n_iter should be cheaper than the current cheapest 1252. (2) The front's accuracy span (12.8..16.1) sits just above the 12-bit constraint, i.e. the whole low-cost/low-width corner is missing. iterative and unrolled_k are dead ends (0 feasible, max throughput 12.9 and 11.6 MSPS < 32), so budget should not go there. I also want to keep m=3 (119 MSPS) candidates alive: the cheapest m=4 designs run at 93.6 MSPS, giving a 32-request batch time near the 0.44 us bound, and the L1 system bound is optimistic, so those may be lost at L2 — a slightly costlier m=3 point is valuable insurance.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 9921 (gain this round: n/a (first round)).
Feasible designs: 50 of 100 evaluations (36 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 30% violate; best seen 273
- max_abs_err <= 0.000244141: 32% violate; best seen 6.52e-06 (2^-17.23)
- sys_p99_batch_us <= 0.44: 30% violate; best seen 0.161

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1252, accuracy_bits=12.8, luts=947, ffs=305, throughput_msps=93.6, max_abs_err=0.000144 (2^-12.76), power_index=1.51
- pipelined_m [data_width=20 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1271, accuracy_bits=12.9, luts=950, ffs=321, throughput_msps=93.6, max_abs_err=0.000135 (2^-12.86), power_index=1.53
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1274, accuracy_bits=13.2, luts=920, ffs=354, throughput_msps=119, max_abs_err=0.000109 (2^-13.17), power_index=1.53
- pipelined_m [data_width=20 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1397, accuracy_bits=13.8, luts=1008, ffs=388, throughput_msps=119, max_abs_err=7.03e-05 (2^-13.80), power_index=1.68
- pipelined_m [data_width=18 n_iter=20 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1697, accuracy_bits=14.2, luts=1327, ffs=370, throughput_msps=93.6, max_abs_err=5.33e-05 (2^-14.20), power_index=2.04
- pipelined_m [data_width=20 n_iter=20 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1705, accuracy_bits=14.4, luts=1327, ffs=378, throughput_msps=93.6, max_abs_err=4.53e-05 (2^-14.43), power_index=2.05
- pipelined_m [data_width=19 n_iter=19 angle_guard=3 frac_guard=1 rounding=round m=4] luts_plus_ffs=1722, accuracy_bits=15.4, luts=1335, ffs=386, throughput_msps=93.6, max_abs_err=2.28e-05 (2^-15.42), power_index=2.07
- pipelined_m [data_width=20 n_iter=20 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1851, accuracy_bits=16, luts=1447, ffs=405, throughput_msps=93.6, max_abs_err=1.54e-05 (2^-15.99), power_index=2.23
- pipelined [data_width=20 n_iter=18 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=2693, accuracy_bits=16.1, luts=1355, ffs=1338, throughput_msps=257, max_abs_err=1.42e-05 (2^-16.11), power_index=3.24
Front coverage: luts_plus_ffs 1252..2693 (HV reference 4000); accuracy_bits 12.8..16.1 (HV reference 12); data_width on the front 18..20 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 12.9 MSPS; best accuracy 17.23 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 11.6 MSPS; best accuracy 14.80 bits
- pipelined: 40 evals, 28 feasible; max throughput seen 273 MSPS; best accuracy 16.11 bits; best feasible luts_plus_ffs=1780; feasible ranges: data_width 15..20, n_iter 15..20, angle_guard 0..3, frac_guard 0..3
- pipelined_m: 30 evals, 22 feasible; max throughput seen 171 MSPS; best accuracy 15.99 bits; best feasible luts_plus_ffs=1252; feasible ranges: data_width 18..20, n_iter 14..20, angle_guard 0..3, frac_guard 0..3, m 3..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Refine the cheap end of pipelined_m (and pipelined for the high-throughput tail), extending data_width downward to where pipelined already proved feasibility, and keeping m small enough to hold the 0.44 us batch bound.*)
- `pipelined_m` (70 evals): data_width=14..20, n_iter=13..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, m=3..5. *Why:* Dominates the front (8/9 points) and holds the cheapest feasible design (1252). Only 30 evals so far; its data_width 18..20 feasible range is a sampling artifact, not a real floor.
- `pipelined` (30 evals): data_width=14..20, n_iter=13..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* Only family with a data_width 15 feasible point and the highest throughput seen (273 MSPS); keep it for the high-throughput / L2-margin tail of the front.

**Result (code):** 100 evaluations this round, 200 total; 123 feasible; hypervolume 1.154e+04 (+16.4%).

**LLM decision:** `map_front` — iterative and unrolled_k are dead ends here: both have 0 feasible designs because their max throughput (12.9 and 11.6 MSPS) is far below the 32 MSPS constraint, so only pipelined and pipelined_m can appear on the front. The feasible front is pipelined_m-dominated at the cheap corner (1127 luts+ffs, 12.03 bits) and spans luts_plus_ffs 1127..2043 against the HV reference 4000, accuracy_bits 12..16.8, and data_width only 17..20 of the registry's 8..28. That is a small slice of both the area and data_width ranges, so the curve is under-mapped: a code-driven coverage search over the full ranges of pipelined and pipelined_m, seeded with the current front, should fill in the cheap-corner boundary (near the 2^-12 error limit) and extend the high-accuracy end toward the 4000-area reference, raising hypervolume. With 200 of 400 evals left this is the right round to spend on coverage before any final refinement.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.154e+04 (gain this round: +16.4%).
Feasible designs: 123 of 200 evaluations (93 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 15% violate; best seen 282
- max_abs_err <= 0.000244141: 27% violate; best seen 6.52e-06 (2^-17.23)
- sys_p99_batch_us <= 0.44: 20% violate; best seen 0.161

Pareto front (feasible, 23 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1127, accuracy_bits=12, luts=841, ffs=287, throughput_msps=93.6, max_abs_err=0.00024 (2^-12.03), power_index=1.36
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1192, accuracy_bits=12.3, luts=905, ffs=287, throughput_msps=93.6, max_abs_err=0.000194 (2^-12.33), power_index=1.43
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=1.51
- pipelined_m [data_width=17 n_iter=15 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1280, accuracy_bits=13.4, luts=985, ffs=295, throughput_msps=93.6, max_abs_err=9.31e-05 (2^-13.39), power_index=1.54
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1359, accuracy_bits=13.7, luts=1038, ffs=321, throughput_msps=93.6, max_abs_err=7.72e-05 (2^-13.66), power_index=1.64
- pipelined_m [data_width=20 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1380, accuracy_bits=13.7, luts=1053, ffs=327, throughput_msps=93.6, max_abs_err=7.38e-05 (2^-13.73), power_index=1.66
- pipelined_m [data_width=19 n_iter=18 angle_guard=0 frac_guard=0 rounding=round m=3] luts_plus_ffs=1560, accuracy_bits=13.9, luts=1134, ffs=426, throughput_msps=119, max_abs_err=6.48e-05 (2^-13.91), power_index=1.88
- pipelined_m [data_width=20 n_iter=20 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1705, accuracy_bits=14.4, luts=1327, ffs=378, throughput_msps=93.6, max_abs_err=4.53e-05 (2^-14.43), power_index=2.05
- pipelined_m [data_width=20 n_iter=19 angle_guard=3 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1800, accuracy_bits=15.9, luts=1390, ffs=410, throughput_msps=89.6, max_abs_err=1.63e-05 (2^-15.90), power_index=2.17
- pipelined_m [data_width=20 n_iter=19 angle_guard=3 frac_guard=3 rounding=round m=3] luts_plus_ffs=2043, accuracy_bits=16.8, luts=1470, ffs=573, throughput_msps=114, max_abs_err=8.96e-06 (2^-16.77), power_index=2.46
Front coverage: luts_plus_ffs 1127..2043 (HV reference 4000); accuracy_bits 12..16.8 (HV reference 12); data_width on the front 17..20 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 12.9 MSPS; best accuracy 17.23 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 11.6 MSPS; best accuracy 14.80 bits
- pipelined: 70 evals, 51 feasible; max throughput seen 282 MSPS; best accuracy 16.11 bits; best feasible luts_plus_ffs=1780; feasible ranges: data_width 15..20, n_iter 14..20, angle_guard 0..3, frac_guard 0..3
- pipelined_m: 100 evals, 72 feasible; max throughput seen 171 MSPS; best accuracy 16.77 bits; best feasible luts_plus_ffs=1127; feasible ranges: data_width 16..20, n_iter 14..20, angle_guard 0..3, frac_guard 0..3, m 3..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (23 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 240 total; 149 feasible; hypervolume 1.829e+04 (+58.5%).

**LLM decision:** `map_front` — The feasible front is entirely pipelined_m (25 designs, 98/140 feasible), spanning luts_plus_ffs 1127..2969 against the HV reference 4000 and accuracy_bits 12..21.5, so the upper-cost region (2969..4000) is still unmapped while the low-cost corner is thin. The cheapest design (1127, accuracy 12.03 bits, throughput 93.6 MSPS) sits near the sys_p99_batch bound at L1 — with 32 requests/cycle-limited acceptance plus ~6-cycle latency it lands around 0.4 us of the 0.44 us limit, exactly the marginal case the notes warn L2 simulation may drop — so we want the full trade-off curve mapped, not just this corner. iterative and unrolled_k are dead ends (0 feasible, max throughput 12.9/11.6 MSPS << 32), and pipelined is dominated (best feasible luts_plus_ffs 1780, best accuracy 16.11 bits vs pipelined_m's 1127 / 22.64), so no new family is warranted. With 160 evals left and one round, a code-driven NSGA-II coverage pass over the full pipelined_m ranges seeded with the current front is the best use of the budget.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 1.829e+04 (gain this round: +58.5%).
Feasible designs: 149 of 240 evaluations (118 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 12% violate; best seen 282
- max_abs_err <= 0.000244141: 23% violate; best seen 1.53e-07 (2^-22.64)
- sys_p99_batch_us <= 0.44: 22% violate; best seen 0.161

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1127, accuracy_bits=12, luts=841, ffs=287, throughput_msps=93.6, max_abs_err=0.00024 (2^-12.03), power_index=1.36
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1204, accuracy_bits=12.5, luts=920, ffs=285, throughput_msps=93.6, max_abs_err=0.000175 (2^-12.48), power_index=1.45
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=1.51
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1321, accuracy_bits=13.6, luts=1008, ffs=313, throughput_msps=93.6, max_abs_err=8.04e-05 (2^-13.60), power_index=1.59
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1371, accuracy_bits=13.7, luts=1071, ffs=301, throughput_msps=93.6, max_abs_err=7.47e-05 (2^-13.71), power_index=1.65
- pipelined_m [data_width=20 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1388, accuracy_bits=13.8, luts=1065, ffs=323, throughput_msps=93.6, max_abs_err=7.02e-05 (2^-13.80), power_index=1.67
- pipelined_m [data_width=25 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1647, accuracy_bits=15, luts=1270, ffs=377, throughput_msps=89.6, max_abs_err=3.15e-05 (2^-14.95), power_index=1.98
- pipelined_m [data_width=20 n_iter=19 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1844, accuracy_bits=16.6, luts=1432, ffs=412, throughput_msps=89.6, max_abs_err=1.04e-05 (2^-16.56), power_index=2.22
- pipelined_m [data_width=25 n_iter=21 angle_guard=-1 frac_guard=0 rounding=round m=4] luts_plus_ffs=2232, accuracy_bits=18.6, luts=1691, ffs=541, throughput_msps=89.6, max_abs_err=2.56e-06 (2^-18.58), power_index=2.69
- pipelined_m [data_width=27 n_iter=23 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=2969, accuracy_bits=21.5, luts=2172, ffs=797, throughput_msps=110, max_abs_err=3.26e-07 (2^-21.55), power_index=3.57
Front coverage: luts_plus_ffs 1127..2969 (HV reference 4000); accuracy_bits 12..21.5 (HV reference 12); data_width on the front 17..27 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 12.9 MSPS; best accuracy 17.23 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 11.6 MSPS; best accuracy 14.80 bits
- pipelined: 70 evals, 51 feasible; max throughput seen 282 MSPS; best accuracy 16.11 bits; best feasible luts_plus_ffs=1780; feasible ranges: data_width 15..20, n_iter 14..20, angle_guard 0..3, frac_guard 0..3
- pipelined_m: 140 evals, 98 feasible; max throughput seen 171 MSPS; best accuracy 22.64 bits; best feasible luts_plus_ffs=1127; feasible ranges: data_width 16..27, n_iter 14..25, angle_guard -1..4, frac_guard 0..4, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (25 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 340 total; 205 feasible; hypervolume 1.869e+04 (+2.1%).

**LLM decision:** `stop` — Final round (4/4 complete, 340/400 evals). All four registry families have been explored, 205/340 evaluations are feasible (170 unique), and the feasible Pareto front holds 29 designs with HV 1.869e+04; the round-4 gain was only +2.1%, so the front has flattened. Constraints are met with margin, not marginally: throughput best 282 MSPS vs required 32, max_abs_err best 2^-22.64 vs required 2^-12, sys_p99_batch best 0.161 us vs bound 0.44 us. Coverage is adequate for the objective range: luts_plus_ffs spans 1127..2969 against the HV reference 4000, and accuracy_bits spans 12..21.5 against the reference 12. The selection rule (min luts_plus_ffs) lands on pipelined_m [W=18, N=14, angle_guard=1, frac_guard=0, trunc, m=4] at 1127 LUT+FF (841/287), 12.03 accuracy bits, 93.6 MSPS — feasible on all three constraints, with accuracy (exact, bit-accurate) safely inside 2^-12 and throughput ~3x the requirement. The only infeasible families are iterative and unrolled_k (0 feasible in 10 and 20 evals; max throughput 12.9 and 11.6 MSPS vs 32 required), which is structural, not a search gap. Nothing further is worth the remaining budget.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 60 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 340 of 400.
Hypervolume of the feasible front: 1.869e+04 (gain this round: +2.1%).
Feasible designs: 205 of 340 evaluations (170 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 9% violate; best seen 282
- max_abs_err <= 0.000244141: 20% violate; best seen 1.53e-07 (2^-22.64)
- sys_p99_batch_us <= 0.44: 26% violate; best seen 0.161

Pareto front (feasible, 29 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1127, accuracy_bits=12, luts=841, ffs=287, throughput_msps=93.6, max_abs_err=0.00024 (2^-12.03), power_index=1.36
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1204, accuracy_bits=12.5, luts=920, ffs=285, throughput_msps=93.6, max_abs_err=0.000175 (2^-12.48), power_index=1.45
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1267, accuracy_bits=13.3, luts=973, ffs=295, throughput_msps=93.6, max_abs_err=0.000101 (2^-13.27), power_index=1.53
- pipelined_m [data_width=19 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1340, accuracy_bits=13.7, luts=1023, ffs=317, throughput_msps=93.6, max_abs_err=7.77e-05 (2^-13.65), power_index=1.61
- pipelined_m [data_width=20 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1380, accuracy_bits=13.7, luts=1053, ffs=327, throughput_msps=93.6, max_abs_err=7.38e-05 (2^-13.73), power_index=1.66
- pipelined_m [data_width=25 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1647, accuracy_bits=15, luts=1270, ffs=377, throughput_msps=89.6, max_abs_err=3.15e-05 (2^-14.95), power_index=1.98
- pipelined_m [data_width=20 n_iter=19 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1844, accuracy_bits=16.6, luts=1432, ffs=412, throughput_msps=89.6, max_abs_err=1.04e-05 (2^-16.56), power_index=2.22
- pipelined_m [data_width=23 n_iter=20 angle_guard=4 frac_guard=1 rounding=round m=4] luts_plus_ffs=2136, accuracy_bits=18.4, luts=1675, ffs=460, throughput_msps=86, max_abs_err=2.88e-06 (2^-18.40), power_index=2.57
- pipelined_m [data_width=27 n_iter=21 angle_guard=-1 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=2487, accuracy_bits=19.4, luts=1818, ffs=669, throughput_msps=110, max_abs_err=1.44e-06 (2^-19.40), power_index=2.99
- pipelined_m [data_width=27 n_iter=23 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=2969, accuracy_bits=21.5, luts=2172, ffs=797, throughput_msps=110, max_abs_err=3.26e-07 (2^-21.55), power_index=3.57
Front coverage: luts_plus_ffs 1127..2969 (HV reference 4000); accuracy_bits 12..21.5 (HV reference 12); data_width on the front 17..27 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 12.9 MSPS; best accuracy 17.23 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 11.6 MSPS; best accuracy 14.80 bits
- pipelined: 70 evals, 51 feasible; max throughput seen 282 MSPS; best accuracy 16.11 bits; best feasible luts_plus_ffs=1780; feasible ranges: data_width 15..20, n_iter 14..20, angle_guard 0..3, frac_guard 0..3
- pipelined_m: 240 evals, 154 feasible; max throughput seen 171 MSPS; best accuracy 22.64 bits; best feasible luts_plus_ffs=1127; feasible ranges: data_width 16..28, n_iter 14..28, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 5

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 60 evaluations*)
- `pipelined_m` (60 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (29 front designs; box front_anchored)

**Result (code):** 60 evaluations this round, 400 total; 249 feasible; hypervolume 1.929e+04 (+3.2%).

**No LLM call** (code's front-mapping round): Final round (4/4 complete, 340/400 evals). All four registry families have been explored, 205/340 evaluations are feasible (170 unique), and the feasible Pareto front holds 29 designs with HV 1.869e+04; the round-4 gain was only +2.1%, so the front has flattened. Constraints are met with margin, not marginally: throughput best 282 MSPS vs required 32, max_abs_err best 2^-22.64 vs required 2^-12, sys_p99_batch best 0.161 us vs bound 0.44 us. Coverage is adequate for the objective range: luts_plus_ffs spans 1127..2969 against the HV reference 4000, and accuracy_bits spans 12..21.5 against the reference 12. The selection rule (min luts_plus_ffs) lands on pipelined_m [W=18, N=14, angle_guard=1, frac_guard=0, trunc, m=4] at 1127 LUT+FF (841/287), 12.03 accuracy bits, 93.6 MSPS — feasible on all three constraints, with accuracy (exact, bit-accurate) safely inside 2^-12 and throughput ~3x the requirement. The only infeasible families are iterative and unrolled_k (0 feasible in 10 and 20 evals; max throughput 12.9 and 11.6 MSPS vs 32 required), which is structural, not a search gap. Nothing further is worth the remaining budget.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 5 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.929e+04 (gain this round: +3.2%).
Feasible designs: 249 of 400 evaluations (207 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 8% violate; best seen 282
- max_abs_err <= 0.000244141: 17% violate; best seen 5.37e-08 (2^-24.15)
- sys_p99_batch_us <= 0.44: 26% violate; best seen 0.161

Pareto front (feasible, 36 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1127, accuracy_bits=12, luts=841, ffs=287, throughput_msps=93.6, max_abs_err=0.00024 (2^-12.03), power_index=1.36
- pipelined_m [data_width=17 n_iter=15 angle_guard=3 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1242, accuracy_bits=12.9, luts=949, ffs=293, throughput_msps=93.6, max_abs_err=0.00013 (2^-12.91), power_index=1.5
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1321, accuracy_bits=13.6, luts=1008, ffs=313, throughput_msps=93.6, max_abs_err=8.04e-05 (2^-13.60), power_index=1.59
- pipelined_m [data_width=20 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1380, accuracy_bits=13.7, luts=1053, ffs=327, throughput_msps=93.6, max_abs_err=7.38e-05 (2^-13.73), power_index=1.66
- pipelined_m [data_width=18 n_iter=19 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1621, accuracy_bits=14.3, luts=1257, ffs=364, throughput_msps=93.6, max_abs_err=5.02e-05 (2^-14.28), power_index=1.95
- pipelined_m [data_width=20 n_iter=19 angle_guard=3 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1800, accuracy_bits=15.9, luts=1390, ffs=410, throughput_msps=89.6, max_abs_err=1.63e-05 (2^-15.90), power_index=2.17
- pipelined_m [data_width=22 n_iter=20 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1910, accuracy_bits=17.2, luts=1487, ffs=423, throughput_msps=89.6, max_abs_err=6.45e-06 (2^-17.24), power_index=2.3
- pipelined_m [data_width=25 n_iter=21 angle_guard=-1 frac_guard=0 rounding=round m=4] luts_plus_ffs=2232, accuracy_bits=18.6, luts=1691, ffs=541, throughput_msps=89.6, max_abs_err=2.56e-06 (2^-18.58), power_index=2.69
- pipelined_m [data_width=26 n_iter=22 angle_guard=4 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=2723, accuracy_bits=19.9, luts=1953, ffs=771, throughput_msps=110, max_abs_err=1e-06 (2^-19.93), power_index=3.28
- pipelined_m [data_width=28 n_iter=25 angle_guard=2 frac_guard=2 rounding=round m=2] luts_plus_ffs=3819, accuracy_bits=23.4, luts=2492, ffs=1327, throughput_msps=153, max_abs_err=9.27e-08 (2^-23.36), power_index=4.6
Front coverage: luts_plus_ffs 1127..3819 (HV reference 4000); accuracy_bits 12..23.4 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 12.9 MSPS; best accuracy 17.23 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 11.6 MSPS; best accuracy 14.80 bits
- pipelined: 70 evals, 51 feasible; max throughput seen 282 MSPS; best accuracy 16.11 bits; best feasible luts_plus_ffs=1780; feasible ranges: data_width 15..20, n_iter 14..20, angle_guard 0..3, frac_guard 0..3
- pipelined_m: 300 evals, 198 feasible; max throughput seen 171 MSPS; best accuracy 24.15 bits; best feasible luts_plus_ffs=1127; feasible ranges: data_width 16..28, n_iter 14..29, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 32079 in, 17688 out
- provider-reported cost: $0.0142
- full prompts and replies: `llm_trace.jsonl`

