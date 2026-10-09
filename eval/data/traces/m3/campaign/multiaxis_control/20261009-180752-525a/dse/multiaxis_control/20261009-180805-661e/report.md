# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
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
`pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 813 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 276 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.31 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000194 (2^-12.33) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 6.36 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 6.02e-05 (2^-14.02) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.97 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 98.3 dBc, SNR 81.7 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=19,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (21 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,m=4` | 813 | 276 | 93.6 | 6 | 1.31 | 0.000194 (2^-12.33) | 12.33 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,m=4` | 855 | 291 | 93.6 | 6 | 1.38 | 0.00017 (2^-12.53) | 12.53 |
| 2 | `pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,m=4` | 954 | 282 | 97.8 | 6 | 1.49 | 0.000121 (2^-13.02) | 13.02 |
| 3 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=4` | 985 | 291 | 93.6 | 6 | 1.54 | 8.35e-05 (2^-13.55) | 13.55 |
| 4 | `pipelined_m:data_width=19,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=4` | 1017 | 301 | 93.6 | 6 | 1.59 | 5.84e-05 (2^-14.06) | 14.06 |
| 5 | `pipelined_m:data_width=19,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=3` | 1033 | 438 | 119.3 | 8 | 1.77 | 5.75e-05 (2^-14.09) | 14.09 |
| 6 | `pipelined_m:data_width=20,n_iter=18,angle_guard=1,frac_guard=0,rounding=round,m=4` | 1205 | 383 | 93.6 | 7 | 1.91 | 2.9e-05 (2^-15.07) | 15.07 |
| 7 | `pipelined_m:data_width=20,n_iter=18,angle_guard=2,frac_guard=0,rounding=round,m=4` | 1223 | 388 | 93.6 | 7 | 1.94 | 2.42e-05 (2^-15.34) | 15.34 |
| 8 | `pipelined_m:data_width=20,n_iter=18,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1337 | 407 | 93.6 | 7 | 2.1 | 1.51e-05 (2^-16.01) | 16.01 |
| 9 | `pipelined_m:data_width=21,n_iter=18,angle_guard=3,frac_guard=1,rounding=round,m=4` | 1375 | 421 | 89.6 | 7 | 2.16 | 1.19e-05 (2^-16.36) | 16.36 |
| 10 | `pipelined_m:data_width=22,n_iter=21,angle_guard=2,frac_guard=0,rounding=round,m=4` | 1565 | 498 | 89.6 | 8 | 2.48 | 5.49e-06 (2^-17.47) | 17.47 |
| 11 | `pipelined_m:data_width=22,n_iter=21,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1632 | 504 | 89.6 | 8 | 2.57 | 4.62e-06 (2^-17.72) | 17.72 |
| 12 | `pipelined_m:data_width=22,n_iter=21,angle_guard=3,frac_guard=1,rounding=round,m=4` | 1674 | 517 | 89.6 | 8 | 2.64 | 3.21e-06 (2^-18.25) | 18.25 |
| 13 | `pipelined_m:data_width=23,n_iter=23,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1883 | 539 | 89.6 | 8 | 2.92 | 1.91e-06 (2^-18.99) | 18.99 |
| 14 | `pipelined_m:data_width=24,n_iter=23,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 1906 | 549 | 89.6 | 8 | 2.96 | 1.76e-06 (2^-19.11) | 19.11 |
| 15 | `pipelined_m:data_width=24,n_iter=23,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1953 | 559 | 89.6 | 8 | 3.02 | 1.14e-06 (2^-19.74) | 19.74 |
| 16 | `pipelined_m:data_width=25,n_iter=22,angle_guard=1,frac_guard=2,rounding=round,m=2` | 1961 | 1014 | 152.6 | 13 | 3.58 | 1.03e-06 (2^-19.89) | 19.89 |
| 17 | `pipelined_m:data_width=28,n_iter=21,angle_guard=3,frac_guard=4,rounding=round,m=2` | 2193 | 1182 | 147.4 | 13 | 4.06 | 9.64e-07 (2^-19.98) | 19.98 |
| 18 | `pipelined_m:data_width=28,n_iter=23,angle_guard=1,frac_guard=3,rounding=trunc,m=2` | 2254 | 1237 | 147.4 | 14 | 4.2 | 2.94e-07 (2^-21.70) | 21.70 |
| 19 | `pipelined_m:data_width=28,n_iter=25,angle_guard=1,frac_guard=0,rounding=trunc,m=2` | 2307 | 1263 | 152.6 | 15 | 4.3 | 2.55e-07 (2^-21.91) | 21.91 |
| 20 | `pipelined_m:data_width=28,n_iter=25,angle_guard=1,frac_guard=3,rounding=trunc,m=2` | 2458 | 1336 | 147.4 | 15 | 4.57 | 1.15e-07 (2^-23.05) | 23.05 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 Msps throughput and all 32 results within 0.44 us of a 1 us tick. Only pipelined and pipelined_m families can achieve 1 result/cycle throughput. iterative and unrolled_k produce one result every several cycles, making it very hard to hit 32 Msps unless Fmax is extremely high (e.g., iterative with N=12 needs 15 cycles/result, so Fmax >= 480 MHz for 32 Msps, which is unrealistic). pipelined is the natural choice: 1 result/cycle, latency N+2 cycles. For N=12-20, latency is 14-22 cycles. At Fmax ~100-200 MHz, latency is 70-220 ns, well within 440 ns. The 32-request burst arrives at once; the pipelined unit processes them in 32 cycles (one per cycle), so the last result comes 32 cycles after the first. At 100 MHz that's 320 ns, within 440 ns. Accuracy: max_abs_err <= 2^-12 = 0.000244. CORDIC error is dominated by residual angle after N iterations (~2^-N) and truncation. N=12 gives ~2^-12 residual, so N>=12 is needed. W=14-20 gives output precision. I focus budget on pipelined since it's the only family that can plausibly meet all constraints. I'll use a single family to concentrate the 400 evals on the most promising trade-off space. data_width 14-20, n_iter 12-20, small guards to minimize area. Rounding: both trunc and round to see the trade-off.*)
- `pipelined` (100 evals): data_width=14..20, n_iter=12..20, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Pipelined gives 1 result/cycle, so throughput = Fmax. To meet 32 Msps, Fmax must be >= 32 MHz, which is easily achievable on Artix-7 for moderate N. This is the primary family for meeting the throughput constraint while keeping area low. N=12-20 with W=14-20 should cover the accuracy constraint (max_abs_err <= 2^-12) with some margin. angle_guard and frac_guard kept small to minimize area.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 70 feasible; hypervolume 6459 (n/a).

**LLM decision:** `add_family` — The current front is dominated by the `pipelined` family, which incurs high area costs (1661+ LUTs+FFs) due to registering every stage. The `pipelined_m` family is the most promising unexplored candidate because it can significantly reduce FF count by registering every m stages (m > 1) while maintaining 1 result/cycle throughput, which is required to meet the `throughput_msps >= 32` and `sys_p99_batch_us <= 0.44` constraints (32 requests in 0.44us implies a very high effective rate or low latency, but 1/cycle is the safest bet for burst handling). `iterative` and `unrolled_k` are less likely to beat the area of a well-tuned `pipelined_m` because they have lower throughput (1 result per k or N cycles), which might violate the system latency constraints for a 32-request burst unless the clock is extremely fast, but `pipelined_m` offers a direct area reduction path for the same throughput class. We should explore `pipelined_m` to see if it can push the `luts_plus_ffs` objective lower than 1661 while maintaining accuracy > 12 bits.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 6459 (gain this round: n/a (first round)).
Feasible designs: 70 of 100 evaluations (52 unique).
Families explored so far: pipelined. Not yet explored: iterative, unrolled_k, pipelined_m.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 30% violate; best seen 2.34e-05 (2^-15.38)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.161

Pareto front (feasible, 16 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=1661, accuracy_bits=12.3, luts=813, ffs=847, throughput_msps=264, max_abs_err=0.000194 (2^-12.33), power_index=2
- pipelined [data_width=19 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=1800, accuracy_bits=12.8, luts=882, ffs=918, throughput_msps=264, max_abs_err=0.000145 (2^-12.76), power_index=2.17
- pipelined [data_width=20 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=1884, accuracy_bits=12.8, luts=923, ffs=960, throughput_msps=264, max_abs_err=0.000137 (2^-12.83), power_index=2.27
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=1933, accuracy_bits=13.2, luts=971, ffs=963, throughput_msps=264, max_abs_err=0.000108 (2^-13.18), power_index=2.33
- pipelined [data_width=19 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=1963, accuracy_bits=13.6, luts=964, ffs=999, throughput_msps=264, max_abs_err=8.33e-05 (2^-13.55), power_index=2.36
- pipelined [data_width=19 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=2034, accuracy_bits=13.7, luts=1001, ffs=1033, throughput_msps=264, max_abs_err=7.72e-05 (2^-13.66), power_index=2.45
- pipelined [data_width=20 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=2130, accuracy_bits=14.2, luts=1048, ffs=1082, throughput_msps=264, max_abs_err=5.27e-05 (2^-14.21), power_index=2.56
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2260, accuracy_bits=14.5, luts=1136, ffs=1124, throughput_msps=264, max_abs_err=4.29e-05 (2^-14.51), power_index=2.72
- pipelined [data_width=20 n_iter=18 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=2404, accuracy_bits=14.8, luts=1188, ffs=1217, throughput_msps=264, max_abs_err=3.54e-05 (2^-14.79), power_index=2.89
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2547, accuracy_bits=15.4, luts=1281, ffs=1265, throughput_msps=264, max_abs_err=2.34e-05 (2^-15.38), power_index=3.07
Front coverage: luts_plus_ffs 1661..2547 (HV reference 4000); accuracy_bits 12.3..15.4 (HV reference 12); data_width on the front 17..20 (registry 8..28).

Per family:
- pipelined: 100 evals, 70 feasible; max throughput seen 273 MSPS; best accuracy 15.38 bits; best feasible luts_plus_ffs=1661; feasible ranges: data_width 16..20, n_iter 14..20, angle_guard 0..2, frac_guard 0..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Add pipelined_m family to explore area reduction via partial pipelining. The current pipelined front has a minimum area of 1661. pipelined_m with m>1 should reduce FFs significantly. We restrict the search to the proven feasible ranges from Round 1 to ensure we find feasible designs quickly within the 100 eval budget.*)
- `pipelined_m` (100 evals): data_width=16..20, n_iter=14..20, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..8. *Why:* Explore pipelined_m to reduce area (FFs) compared to pipelined while keeping 1 result/cycle throughput to satisfy system latency and throughput constraints. Ranges are narrowed to the feasible region found in Round 1 (data_width 16-20, n_iter 14-20) to focus the search on designs that meet accuracy and throughput constraints.

**Result (code):** 100 evaluations this round, 200 total; 122 feasible; hypervolume 1.107e+04 (+71.4%).

**LLM decision:** `add_family` — The current Pareto front is entirely composed of pipelined and pipelined_m designs, with the cheapest feasible design at 1090 luts_plus_ffs (pipelined_m, data_width=17, n_iter=14, m=4). The selection rule is min luts_plus_ffs, so finding a cheaper design is the primary goal. The unrolled_k family has not been explored yet. It uses a shared FSM and processes k micro-rotations per cycle, which often results in lower area than fully pipelined designs because it avoids the register overhead of every stage. The throughput constraint (>=32 MSPS) is easily satisfied by unrolled_k for reasonable k values (e.g., k=2 gives 2 results/cycle, so at 16 MHz it meets 32 MSPS; the cost model will estimate Fmax, but it is likely much higher). The sys_p99_batch_us constraint (<=0.44 us) is also easily met because the latency of unrolled_k is ceil(N/k)+3 cycles, which is small (e.g., 7 cycles for N=14, k=4). At any reasonable Fmax (>=100 MHz), 7 cycles is 70 ns, well within 0.44 us. The accuracy constraint (max_abs_err <= 2^-12) is the main driver for n_iter and data_width. The current front shows that data_width=17, n_iter=14 gives 12.3 bits, which is feasible. unrolled_k with similar parameters might achieve the same accuracy with lower area due to the shared datapath. Therefore, exploring unrolled_k in the region data_width 14-20, n_iter 12-20, k 2-8, angle_guard -2 to 4, frac_guard 0-4 is the most promising next step to potentially find a design with luts_plus_ffs < 1090. The budget of 100 evals for this round is allocated entirely to unrolled_k to focus the search.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.107e+04 (gain this round: +71.4%).
Feasible designs: 122 of 200 evaluations (98 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 20% violate; best seen 1.11e-05 (2^-16.46)
- sys_p99_batch_us <= 0.44: 20% violate; best seen 0.161

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1090, accuracy_bits=12.3, luts=813, ffs=276, throughput_msps=93.6, max_abs_err=0.000194 (2^-12.33), power_index=1.31
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1145, accuracy_bits=12.5, luts=855, ffs=291, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.53), power_index=1.38
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1236, accuracy_bits=13, luts=954, ffs=282, throughput_msps=97.8, max_abs_err=0.000121 (2^-13.02), power_index=1.49
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1276, accuracy_bits=13.5, luts=985, ffs=291, throughput_msps=93.6, max_abs_err=8.35e-05 (2^-13.55), power_index=1.54
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1318, accuracy_bits=14.1, luts=1017, ffs=301, throughput_msps=93.6, max_abs_err=5.84e-05 (2^-14.06), power_index=1.59
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1471, accuracy_bits=14.1, luts=1033, ffs=438, throughput_msps=119, max_abs_err=5.75e-05 (2^-14.09), power_index=1.77
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1589, accuracy_bits=15.1, luts=1205, ffs=383, throughput_msps=93.6, max_abs_err=2.9e-05 (2^-15.07), power_index=1.91
- pipelined_m [data_width=20 n_iter=18 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1612, accuracy_bits=15.3, luts=1223, ffs=388, throughput_msps=93.6, max_abs_err=2.42e-05 (2^-15.34), power_index=1.94
- pipelined_m [data_width=20 n_iter=18 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1744, accuracy_bits=16, luts=1337, ffs=407, throughput_msps=93.6, max_abs_err=1.51e-05 (2^-16.01), power_index=2.1
- pipelined_m [data_width=20 n_iter=20 angle_guard=2 frac_guard=2 rounding=round m=2] luts_plus_ffs=2264, accuracy_bits=16.5, luts=1489, ffs=775, throughput_msps=164, max_abs_err=1.11e-05 (2^-16.46), power_index=2.72
Front coverage: luts_plus_ffs 1090..2264 (HV reference 4000); accuracy_bits 12.3..16.5 (HV reference 12); data_width on the front 17..20 (registry 8..28).

Per family:
- pipelined: 100 evals, 70 feasible; max throughput seen 273 MSPS; best accuracy 15.38 bits; best feasible luts_plus_ffs=1661; feasible ranges: data_width 16..20, n_iter 14..20, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 100 evals, 52 feasible; max throughput seen 171 MSPS; best accuracy 16.46 bits; best feasible luts_plus_ffs=1090; feasible ranges: data_width 16..20, n_iter 14..20, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The current Pareto front is entirely composed of pipelined and pipelined_m designs, with the cheapest feasible design at 1090 luts_plus_ffs (pipelined_m, data_width=17, n_iter=14, m=4). The selection rule is min luts_plus_ffs, so finding a cheaper design is the primary goal. The unrolled_k family has not been explored yet. It uses a shared FSM and processes k micro-rotations per cycle, which often results in lower area than fully pipelined designs because it avoids the register overhead of every stage. The throughput constraint (>=32 MSPS) is easily satisfied by unrolled_k for reasonable k values (e.g., k=2 gives 2 results/cycle, so at 16 MHz it meets 32 MSPS; the cost model will estimate Fmax, but it is likely much higher). The sys_p99_batch_us constraint (<=0.44 us) is also easily met because the latency of unrolled_k is ceil(N/k)+3 cycles, which is small (e.g., 7 cycles for N=14, k=4). At any reasonable Fmax (>=100 MHz), 7 cycles is 70 ns, well within 0.44 us. The accuracy constraint (max_abs_err <= 2^-12) is the main driver for n_iter and data_width. The current front shows that data_width=17, n_iter=14 gives 12.3 bits, which is feasible. unrolled_k with similar parameters might achieve the same accuracy with lower area due to the shared datapath. Therefore, exploring unrolled_k in the region data_width 14-20, n_iter 12-20, k 2-8, angle_guard -2 to 4, frac_guard 0-4 is the most promising next step to potentially find a design with luts_plus_ffs < 1090. The budget of 100 evals for this round is allocated entirely to unrolled_k to focus the search.*)
- `unrolled_k` (40 evals): data_width=14..20, n_iter=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* unrolled_k shares the FSM and datapath across k micro-rotations per cycle, which typically yields lower LUT/FF area than the fully pipelined variants at similar accuracy. The current front is dominated by pipelined_m with a minimum luts_plus_ffs of 1090. Since the selection rule is min luts_plus_ffs, exploring unrolled_k in the region where accuracy is just above the 12-bit constraint (data_width 14-20, n_iter 12-20) is the most direct way to find a cheaper design that still meets the throughput and batch latency constraints. The throughput constraint (>=32 MSPS) is easily met by unrolled_k if k is chosen appropriately (e.g., k=4 gives 4 results/cycle, so even at 100 MHz it is 400 MSPS). The sys_p99_batch_us constraint (<=0.44 us) requires the 32 requests to complete within 0.44 us. With unrolled_k, the latency is ceil(N/k)+3 cycles. If N=14, k=4, latency is ceil(14/4)+3 = 4+3 = 7 cycles. At 100 MHz, 7 cycles = 70 ns = 0.07 us, which is well within 0.44 us. Even at lower Fmax, this should be fine. The main risk is if Fmax is very low, but the cost model will estimate Fmax. The accuracy constraint (max_abs_err <= 2^-12) is the binding one for the lower end of the front. The current front starts at 12.3 bits, so unrolled_k might find designs with 12.0-12.5 bits at lower area.

**Result (code):** 40 evaluations this round, 240 total; 122 feasible; hypervolume 1.107e+04 (+0.0%).

**LLM decision:** `stop` — The Pareto front is well-established and stable (0% hypervolume gain in Round 3). The `pipelined_m` family dominates the front, with the minimum area design (1090 LUTs+FFs) meeting all constraints: throughput 93.6 MSPS >= 32, max_abs_err 0.000194 <= 0.000244, and sys_p99_batch_us 0.161 <= 0.44. The front covers the relevant trade-off space (1090-2264 area, 12.3-16.5 bits accuracy) sufficiently for the selection rule (min luts_plus_ffs). `unrolled_k` is infeasible for throughput, and `iterative` would likely be infeasible or dominated given the 32 MSPS throughput requirement and the fact that `pipelined_m` already achieves 93+ MSPS with lower area than `pipelined`. No further exploration is needed.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 1.107e+04 (gain this round: +0.0%).
Feasible designs: 122 of 240 evaluations (98 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 17% violate; best seen 273
- max_abs_err <= 0.000244141: 24% violate; best seen 1.11e-05 (2^-16.46)
- sys_p99_batch_us <= 0.44: 33% violate; best seen 0.161

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1090, accuracy_bits=12.3, luts=813, ffs=276, throughput_msps=93.6, max_abs_err=0.000194 (2^-12.33), power_index=1.31
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1145, accuracy_bits=12.5, luts=855, ffs=291, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.53), power_index=1.38
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1236, accuracy_bits=13, luts=954, ffs=282, throughput_msps=97.8, max_abs_err=0.000121 (2^-13.02), power_index=1.49
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1276, accuracy_bits=13.5, luts=985, ffs=291, throughput_msps=93.6, max_abs_err=8.35e-05 (2^-13.55), power_index=1.54
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1318, accuracy_bits=14.1, luts=1017, ffs=301, throughput_msps=93.6, max_abs_err=5.84e-05 (2^-14.06), power_index=1.59
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1471, accuracy_bits=14.1, luts=1033, ffs=438, throughput_msps=119, max_abs_err=5.75e-05 (2^-14.09), power_index=1.77
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1589, accuracy_bits=15.1, luts=1205, ffs=383, throughput_msps=93.6, max_abs_err=2.9e-05 (2^-15.07), power_index=1.91
- pipelined_m [data_width=20 n_iter=18 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1612, accuracy_bits=15.3, luts=1223, ffs=388, throughput_msps=93.6, max_abs_err=2.42e-05 (2^-15.34), power_index=1.94
- pipelined_m [data_width=20 n_iter=18 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1744, accuracy_bits=16, luts=1337, ffs=407, throughput_msps=93.6, max_abs_err=1.51e-05 (2^-16.01), power_index=2.1
- pipelined_m [data_width=20 n_iter=20 angle_guard=2 frac_guard=2 rounding=round m=2] luts_plus_ffs=2264, accuracy_bits=16.5, luts=1489, ffs=775, throughput_msps=164, max_abs_err=1.11e-05 (2^-16.46), power_index=2.72
Front coverage: luts_plus_ffs 1090..2264 (HV reference 4000); accuracy_bits 12.3..16.5 (HV reference 12); data_width on the front 17..20 (registry 8..28).

Per family:
- unrolled_k: 40 evals, 0 feasible; max throughput seen 10 MSPS; best accuracy 15.49 bits
- pipelined: 100 evals, 70 feasible; max throughput seen 273 MSPS; best accuracy 15.38 bits; best feasible luts_plus_ffs=1661; feasible ranges: data_width 16..20, n_iter 14..20, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 100 evals, 52 feasible; max throughput seen 171 MSPS; best accuracy 16.46 bits; best feasible luts_plus_ffs=1090; feasible ranges: data_width 16..20, n_iter 14..20, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (160 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (10 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 226 feasible; hypervolume 1.834e+04 (+65.7%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and stable (0% hypervolume gain in Round 3). The `pipelined_m` family dominates the front, with the minimum area design (1090 LUTs+FFs) meeting all constraints: throughput 93.6 MSPS >= 32, max_abs_err 0.000194 <= 0.000244, and sys_p99_batch_us 0.161 <= 0.44. The front covers the relevant trade-off space (1090-2264 area, 12.3-16.5 bits accuracy) sufficiently for the selection rule (min luts_plus_ffs). `unrolled_k` is infeasible for throughput, and `iterative` would likely be infeasible or dominated given the 32 MSPS throughput requirement and the fact that `pipelined_m` already achieves 93+ MSPS with lower area than `pipelined`. No further exploration is needed.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.834e+04 (gain this round: +65.7%).
Feasible designs: 226 of 400 evaluations (195 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 10% violate; best seen 273
- max_abs_err <= 0.000244141: 17% violate; best seen 1.1e-07 (2^-23.12)
- sys_p99_batch_us <= 0.44: 32% violate; best seen 0.161

Pareto front (feasible, 21 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1090, accuracy_bits=12.3, luts=813, ffs=276, throughput_msps=93.6, max_abs_err=0.000194 (2^-12.33), power_index=1.31
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1236, accuracy_bits=13, luts=954, ffs=282, throughput_msps=97.8, max_abs_err=0.000121 (2^-13.02), power_index=1.49
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1318, accuracy_bits=14.1, luts=1017, ffs=301, throughput_msps=93.6, max_abs_err=5.84e-05 (2^-14.06), power_index=1.59
- pipelined_m [data_width=20 n_iter=18 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1612, accuracy_bits=15.3, luts=1223, ffs=388, throughput_msps=93.6, max_abs_err=2.42e-05 (2^-15.34), power_index=1.94
- pipelined_m [data_width=21 n_iter=18 angle_guard=3 frac_guard=1 rounding=round m=4] luts_plus_ffs=1796, accuracy_bits=16.4, luts=1375, ffs=421, throughput_msps=89.6, max_abs_err=1.19e-05 (2^-16.36), power_index=2.16
- pipelined_m [data_width=22 n_iter=21 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=2137, accuracy_bits=17.7, luts=1632, ffs=504, throughput_msps=89.6, max_abs_err=4.62e-06 (2^-17.72), power_index=2.57
- pipelined_m [data_width=23 n_iter=23 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=2422, accuracy_bits=19, luts=1883, ffs=539, throughput_msps=89.6, max_abs_err=1.91e-06 (2^-18.99), power_index=2.92
- pipelined_m [data_width=25 n_iter=22 angle_guard=1 frac_guard=2 rounding=round m=2] luts_plus_ffs=2975, accuracy_bits=19.9, luts=1961, ffs=1014, throughput_msps=153, max_abs_err=1.03e-06 (2^-19.89), power_index=3.58
- pipelined_m [data_width=28 n_iter=23 angle_guard=1 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=3491, accuracy_bits=21.7, luts=2254, ffs=1237, throughput_msps=147, max_abs_err=2.94e-07 (2^-21.70), power_index=4.2
- pipelined_m [data_width=28 n_iter=25 angle_guard=1 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=3794, accuracy_bits=23, luts=2458, ffs=1336, throughput_msps=147, max_abs_err=1.15e-07 (2^-23.05), power_index=4.57
Front coverage: luts_plus_ffs 1090..3794 (HV reference 4000); accuracy_bits 12.3..23 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- unrolled_k: 40 evals, 0 feasible; max throughput seen 10 MSPS; best accuracy 15.49 bits
- pipelined: 100 evals, 70 feasible; max throughput seen 273 MSPS; best accuracy 15.38 bits; best feasible luts_plus_ffs=1661; feasible ranges: data_width 16..20, n_iter 14..20, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 260 evals, 156 feasible; max throughput seen 171 MSPS; best accuracy 23.12 bits; best feasible luts_plus_ffs=1090; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 26701 in, 3747 out
- provider-reported cost: $0.0078
- full prompts and replies: `llm_trace.jsonl`

