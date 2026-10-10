# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 4 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec low_area_control: Field-oriented motor-control loop needing sin/cos of the rotor angle at >= 1 MSPS with max error <= 2^-10. Area is everything: minimise LUTs + FFs.
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min luts_plus_ffs (HV ref 1500)
  objective: max accuracy_bits (HV ref 10)
  select: min luts_plus_ffs
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`unrolled_k:data_width=15,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,k=2` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 252 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 92 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 105 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 10.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 10 | exact: schedule |
| latency_ns | 94.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.129 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000599 (2^-10.71) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 4.9 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000152 (2^-12.69) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.24 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.7 | exact: bit-accurate model, exhaustive (32768 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 10 cycles, a new input every 10 cycle(s). DDS tone from its exact outputs: SFDR 83.9 dBc, SNR 73.8 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (26 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `unrolled_k:data_width=15,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,k=2` | 252 | 92 | 10.5 | 10 | 0.129 | 0.000599 (2^-10.71) | 10.71 |
| 1 | `unrolled_k:data_width=16,n_iter=15,angle_guard=0,frac_guard=0,rounding=round,k=2` | 262 | 95 | 9.6 | 11 | 0.148 | 0.000373 (2^-11.39) | 11.39 |
| 2 | `unrolled_k:data_width=17,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc,k=2` | 270 | 100 | 9.6 | 11 | 0.153 | 0.000307 (2^-11.67) | 11.67 |
| 3 | `unrolled_k:data_width=17,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc,k=2` | 270 | 100 | 9.6 | 11 | 0.153 | 0.000307 (2^-11.67) | 11.67 |
| 4 | `unrolled_k:data_width=17,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,k=2` | 279 | 100 | 9.6 | 11 | 0.157 | 0.000244 (2^-12.00) | 12.00 |
| 5 | `unrolled_k:data_width=17,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc,k=2` | 283 | 102 | 9.6 | 11 | 0.159 | 0.000239 (2^-12.03) | 12.03 |
| 6 | `unrolled_k:data_width=17,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc,k=2` | 286 | 103 | 9.6 | 11 | 0.161 | 0.000219 (2^-12.16) | 12.16 |
| 7 | `unrolled_k:data_width=18,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc,k=2` | 286 | 105 | 9.6 | 11 | 0.162 | 0.000206 (2^-12.25) | 12.25 |
| 8 | `unrolled_k:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=trunc,k=2` | 290 | 106 | 9.3 | 11 | 0.164 | 0.000194 (2^-12.33) | 12.33 |
| 9 | `unrolled_k:data_width=17,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc,k=2` | 299 | 105 | 9.3 | 11 | 0.167 | 0.000175 (2^-12.48) | 12.48 |
| 10 | `unrolled_k:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,k=2` | 302 | 107 | 9.3 | 11 | 0.169 | 0.000109 (2^-13.17) | 13.17 |
| 11 | `unrolled_k:data_width=18,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc,k=2` | 316 | 110 | 9.3 | 11 | 0.176 | 0.000102 (2^-13.26) | 13.26 |
| 12 | `unrolled_k:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,k=2` | 320 | 111 | 9.3 | 11 | 0.178 | 9.49e-05 (2^-13.36) | 13.36 |
| 13 | `unrolled_k:data_width=19,n_iter=24,angle_guard=1,frac_guard=2,rounding=trunc,k=2` | 357 | 116 | 6.9 | 15 | 0.267 | 4.05e-05 (2^-14.59) | 14.59 |
| 14 | `unrolled_k:data_width=21,n_iter=25,angle_guard=1,frac_guard=1,rounding=trunc,k=2` | 382 | 124 | 6.4 | 16 | 0.304 | 1.56e-05 (2^-15.97) | 15.97 |
| 15 | `unrolled_k:data_width=21,n_iter=19,angle_guard=1,frac_guard=2,rounding=trunc,k=2` | 396 | 126 | 7.7 | 13 | 0.256 | 1.16e-05 (2^-16.40) | 16.40 |
| 16 | `unrolled_k:data_width=19,n_iter=24,angle_guard=4,frac_guard=3,rounding=round,k=2` | 436 | 121 | 6.7 | 15 | 0.314 | 9.32e-06 (2^-16.71) | 16.71 |
| 17 | `unrolled_k:data_width=21,n_iter=26,angle_guard=2,frac_guard=1,rounding=round,k=2` | 445 | 125 | 6.3 | 16 | 0.343 | 6.89e-06 (2^-17.15) | 17.15 |
| 18 | `unrolled_k:data_width=21,n_iter=26,angle_guard=3,frac_guard=1,rounding=round,k=2` | 448 | 126 | 6.3 | 16 | 0.346 | 6.45e-06 (2^-17.24) | 17.24 |
| 19 | `unrolled_k:data_width=25,n_iter=25,angle_guard=2,frac_guard=0,rounding=trunc,k=2` | 453 | 143 | 6.1 | 16 | 0.359 | 1.47e-06 (2^-19.37) | 19.37 |
| 20 | `unrolled_k:data_width=25,n_iter=27,angle_guard=3,frac_guard=2,rounding=trunc,k=2` | 500 | 148 | 5.8 | 17 | 0.415 | 4.7e-07 (2^-21.02) | 21.02 |
| 21 | `unrolled_k:data_width=28,n_iter=25,angle_guard=1,frac_guard=0,rounding=trunc,k=2` | 514 | 157 | 6.1 | 16 | 0.404 | 2.55e-07 (2^-21.91) | 21.91 |
| 22 | `unrolled_k:data_width=27,n_iter=25,angle_guard=1,frac_guard=3,rounding=trunc,k=2` | 546 | 158 | 6.1 | 16 | 0.424 | 1.89e-07 (2^-22.33) | 22.33 |
| 23 | `unrolled_k:data_width=28,n_iter=28,angle_guard=3,frac_guard=1,rounding=trunc,k=2` | 549 | 161 | 5.6 | 17 | 0.455 | 1e-07 (2^-23.25) | 23.25 |
| 24 | `unrolled_k:data_width=28,n_iter=27,angle_guard=3,frac_guard=3,rounding=round,k=2` | 662 | 165 | 5.6 | 17 | 0.529 | 3.85e-08 (2^-24.63) | 24.63 |
| 25 | `unrolled_k:data_width=28,n_iter=29,angle_guard=4,frac_guard=3,rounding=round,k=4` | 984 | 165 | 4.5 | 11 | 0.476 | 2.3e-08 (2^-25.37) | 25.37 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >=1 MSPS throughput, which immediately rules out `iterative` (1 result every N+3 cycles, so even at 200 MHz with N=10 it gives only ~18 MSPS... wait, 200MHz/13 = 15.4 MSPS, that actually meets it. But iterative has the longest latency and the shared datapath with barrel shifters typically has a longer critical path than pipelined variants, making it hard to hit high Fmax. More importantly, iterative produces one result every N+3 cycles, so to get 1 MSPS it needs Fmax >= (N+3) MHz. With N~12, that's ~15 MHz, which is trivially achievable. However, iterative's area is dominated by the barrel shifter datapath which is wide. Let me reconsider: iterative actually CAN meet throughput easily. But its area (LUTs+FFs) is typically higher than pipelined_m because the barrel shifter is a large combinational block. The key insight is that pipelined_m with m=4-8 has very few FFs (only N/m stages registered) and 1/cycle throughput, making it the strongest area candidate. I'll keep iterative out of round 1 to focus budget on the three families that clearly can meet constraints with competitive area. If pipelined_m and pipelined don't dominate, I can add iterative in round 2. Ranges are narrowed: data_width 12-18 because max_abs_err <= 2^-10 requires accuracy_bits >= 10; with n_iter=10-16 and modest guards, W=12-14 is typically sufficient, and W>18 wastes area. n_iter 10-16 balances accuracy vs area. angle_guard and frac_guard kept small (0-2) since the error budget is tight but not extreme. Rounding included as both options since it affects accuracy at the LSB level.*)
- `pipelined_m` (50 evals): data_width=12..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* Primary candidate. 1 result/cycle meets the >=1 MSPS throughput constraint at modest Fmax. Registering every m stages (m>1) drastically cuts FFs vs full pipelined while keeping 1/cycle throughput, directly targeting the 'minimise LUTs+FFs' objective. m is the key area lever here.
- `pipelined` (30 evals): data_width=12..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Reference point on the front. Full pipeline (m=1) has the most FFs but the shortest critical path (highest Fmax), so it anchors the high-throughput/low-latency end of the Pareto front. Needed to map the trade-off curve for hypervolume, even though pipelined_m will likely dominate on area.
- `unrolled_k` (20 evals): data_width=12..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..8. *Why:* Secondary candidate. Shared FSM with k rotations/cycle can have fewer FFs than pipelined_m for small k, but throughput = Fmax/k. Only meets >=1 MSPS if Fmax >= k MHz. Worth a small share to check if it lands on the area-optimal part of the front for low k.

**Result (code):** 100 evaluations this round, 100 total; 68 feasible; hypervolume 3606 (n/a).

**LLM decision:** `refine` — The current Pareto front is dominated by `unrolled_k` designs with `data_width=18` and `n_iter=15`. The best area design (409 LUTs+FFs) achieves 13.2 bits of accuracy, which comfortably exceeds the constraint (max_abs_err <= 2^-10). The `pipelined` and `pipelined_m` families are significantly larger (1380+ and 853+ LUTs+FFs respectively) and do not offer a better trade-off for this 'low_area' spec, as `unrolled_k` already meets the throughput constraint (>= 1 MSPS) with much less area. The `iterative` family is likely to be even larger or slower than `unrolled_k` for the same accuracy, or require more cycles, making it less promising for area minimization. The search should focus on refining the `unrolled_k` family around the known good region (data_width 16-18, n_iter 13-15) to ensure we capture the absolute minimum area point, potentially checking if `data_width=17` or `16` can still meet the accuracy constraint with fewer LUTs. The `pipelined` families can be deprioritized as they are clearly not on the efficient frontier for area.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 3606 (gain this round: n/a (first round)).
Feasible designs: 68 of 100 evaluations (53 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 32% violate; best seen 8.41e-05 (2^-13.54)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round k=2] luts_plus_ffs=409, accuracy_bits=13.2, luts=302, ffs=107, throughput_msps=9.35, max_abs_err=0.000109 (2^-13.17), power_index=0.169
- unrolled_k [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=round k=5] luts_plus_ffs=686, accuracy_bits=13.4, luts=577, ffs=109, throughput_msps=9.38, max_abs_err=9.56e-05 (2^-13.35), power_index=0.155
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=1969, accuracy_bits=13.4, luts=987, ffs=982, throughput_msps=264, max_abs_err=9.31e-05 (2^-13.39), power_index=0.0741
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts_plus_ffs=2070, accuracy_bits=13.5, luts=1039, ffs=1031, throughput_msps=264, max_abs_err=8.41e-05 (2^-13.54), power_index=0.0779
Front coverage: luts_plus_ffs 409..2070 (HV reference 1500); accuracy_bits 13.2..13.5 (HV reference 10); data_width on the front 18..18 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 11 feasible; max throughput seen 14 MSPS; best accuracy 13.35 bits; best feasible luts_plus_ffs=409; feasible ranges: data_width 16..18, n_iter 13..15, angle_guard 0..2, frac_guard 0..2, k 2..7
- pipelined: 30 evals, 19 feasible; max throughput seen 282 MSPS; best accuracy 13.54 bits; best feasible luts_plus_ffs=1380; feasible ranges: data_width 15..18, n_iter 13..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 38 feasible; max throughput seen 171 MSPS; best accuracy 13.18 bits; best feasible luts_plus_ffs=853; feasible ranges: data_width 15..17, n_iter 13..16, angle_guard 0..2, frac_guard 0..2, m 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate the remaining 300 evaluations on `unrolled_k` to thoroughly map the low-area corner of the Pareto front. The other families are too large to be competitive for this specific 'min luts_plus_ffs' objective.*)
- `unrolled_k` (100 evals): data_width=16..18, n_iter=13..15, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..8. *Why:* Focus entirely on the family that currently holds the best area-accuracy trade-off. Narrow the search to the proven feasible region to maximize the chance of finding the global minimum area design within the remaining budget.

**Result (code):** 100 evaluations this round, 200 total; 168 feasible; hypervolume 3761 (+4.3%).

**LLM decision:** `refine` — The front spans 357-2070 luts_plus_ffs and 11.4-13.5 accuracy bits, but the mid-range (400-1300 area) is sparsely covered. unrolled_k dominates the low-area corner but only reaches 11.4 bits; pipelined_m offers a natural bridge at ~853 area but needs denser sampling. The 16% error-violation rate suggests some parameter combinations are just outside the accuracy constraint, so tightening ranges around the feasible boundary (n_iter 14-16, guards 0-2) will yield more feasible points. iterative is not needed: it has N+3 latency and 1 result/cycle, so its throughput equals Fmax which is lower than unrolled_k's pipelined throughput, and its area is comparable or worse for the same accuracy. The three families on the front already cover the full trade-off; refining their ranges will improve hypervolume more than adding a fourth family.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 3761 (gain this round: +4.3%).
Feasible designs: 168 of 200 evaluations (125 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 16% violate; best seen 8.41e-05 (2^-13.54)

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=16 n_iter=15 angle_guard=0 frac_guard=0 rounding=round k=2] luts_plus_ffs=357, accuracy_bits=11.4, luts=262, ffs=95, throughput_msps=9.58, max_abs_err=0.000373 (2^-11.39), power_index=0.148
- unrolled_k [data_width=17 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=370, accuracy_bits=11.7, luts=270, ffs=100, throughput_msps=9.58, max_abs_err=0.000307 (2^-11.67), power_index=0.153
- unrolled_k [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=391, accuracy_bits=12.2, luts=286, ffs=105, throughput_msps=9.58, max_abs_err=0.000206 (2^-12.25), power_index=0.162
- unrolled_k [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=396, accuracy_bits=12.3, luts=290, ffs=106, throughput_msps=9.35, max_abs_err=0.000194 (2^-12.33), power_index=0.164
- unrolled_k [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=404, accuracy_bits=12.5, luts=299, ffs=105, throughput_msps=9.35, max_abs_err=0.000175 (2^-12.48), power_index=0.167
- unrolled_k [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round k=2] luts_plus_ffs=409, accuracy_bits=13.2, luts=302, ffs=107, throughput_msps=9.35, max_abs_err=0.000109 (2^-13.17), power_index=0.169
- unrolled_k [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=426, accuracy_bits=13.3, luts=316, ffs=110, throughput_msps=9.35, max_abs_err=0.000102 (2^-13.26), power_index=0.176
- unrolled_k [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=431, accuracy_bits=13.4, luts=320, ffs=111, throughput_msps=9.35, max_abs_err=9.49e-05 (2^-13.36), power_index=0.178
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=1969, accuracy_bits=13.4, luts=987, ffs=982, throughput_msps=264, max_abs_err=9.31e-05 (2^-13.39), power_index=0.0741
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts_plus_ffs=2070, accuracy_bits=13.5, luts=1039, ffs=1031, throughput_msps=264, max_abs_err=8.41e-05 (2^-13.54), power_index=0.0779
Front coverage: luts_plus_ffs 357..2070 (HV reference 1500); accuracy_bits 11.4..13.5 (HV reference 10); data_width on the front 16..18 (registry 8..28).

Per family:
- unrolled_k: 120 evals, 111 feasible; max throughput seen 14 MSPS; best accuracy 13.36 bits; best feasible luts_plus_ffs=357; feasible ranges: data_width 16..18, n_iter 13..15, angle_guard 0..2, frac_guard 0..2, k 2..8
- pipelined: 30 evals, 19 feasible; max throughput seen 282 MSPS; best accuracy 13.54 bits; best feasible luts_plus_ffs=1380; feasible ranges: data_width 15..18, n_iter 13..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 38 feasible; max throughput seen 171 MSPS; best accuracy 13.18 bits; best feasible luts_plus_ffs=853; feasible ranges: data_width 15..17, n_iter 13..16, angle_guard 0..2, frac_guard 0..2, m 2..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The front spans 357-2070 luts_plus_ffs and 11.4-13.5 accuracy bits, but the mid-range (400-1300 area) is sparsely covered. unrolled_k dominates the low-area corner but only reaches 11.4 bits; pipelined_m offers a natural bridge at ~853 area but needs denser sampling. The 16% error-violation rate suggests some parameter combinations are just outside the accuracy constraint, so tightening ranges around the feasible boundary (n_iter 14-16, guards 0-2) will yield more feasible points. iterative is not needed: it has N+3 latency and 1 result/cycle, so its throughput equals Fmax which is lower than unrolled_k's pipelined throughput, and its area is comparable or worse for the same accuracy. The three families on the front already cover the full trade-off; refining their ranges will improve hypervolume more than adding a fourth family.*)
- `unrolled_k` (20 evals): data_width=15..17, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..2. *Why:* unrolled_k dominates the low-area corner (357 luts_plus_ffs at 11.4 bits). The front currently stops at 11.4 bits for this family; pushing n_iter to 16 and widening angle/frac guards slightly should extend the accuracy axis while keeping area near the minimum, filling the gap between 11.4 and 13.4 bits at low area.
- `pipelined_m` (12 evals): data_width=15..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m bridges the area gap (853 best) between unrolled_k (357) and pipelined (1380+). Its throughput (171 MSPS) far exceeds the 1 MSPS constraint, so it is feasible. Focusing on m=2..4 and n_iter=14..16 should map the mid-area region of the front more densely, improving hypervolume coverage in the 800-1400 luts_plus_ffs range where the front is currently sparse.
- `pipelined` (8 evals): data_width=15..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined holds the accuracy ceiling (13.54 bits) but at high area (1380+). A small focused search here ensures the high-accuracy end of the front is well-characterized, especially since the selection rule is min luts_plus_ffs and we need the full trade-off curve for hypervolume.

**Result (code):** 40 evaluations this round, 240 total; 205 feasible; hypervolume 3774 (+0.4%).

**LLM decision:** `stop` — The feasible Pareto front is well-established and the selection rule (min luts_plus_ffs) is satisfied by a clear winner. The best design is `unrolled_k` with `data_width=15, n_iter=14, angle_guard=2, frac_guard=0, rounding=round, k=2`, achieving `luts_plus_ffs=344` and `accuracy_bits=10.7` (max_abs_err=0.000599), which comfortably meets the constraint `max_abs_err <= 0.000976562` (2^-10) and `throughput_msps >= 1` (10.5 MSPS). The front spans a wide range of area (344 to 2070) and accuracy (10.7 to 13.5 bits), covering the trade-off space effectively. The hypervolume gain in the last round was minimal (+0.4%), indicating convergence. Since this is the final round, stopping is the appropriate action to finalize the design selection.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 3774 (gain this round: +0.4%).
Feasible designs: 205 of 240 evaluations (156 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 15% violate; best seen 8.41e-05 (2^-13.54)

Pareto front (feasible, 15 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=15 n_iter=14 angle_guard=2 frac_guard=0 rounding=round k=2] luts_plus_ffs=344, accuracy_bits=10.7, luts=252, ffs=92, throughput_msps=10.5, max_abs_err=0.000599 (2^-10.71), power_index=0.129
- unrolled_k [data_width=17 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=370, accuracy_bits=11.7, luts=270, ffs=100, throughput_msps=9.58, max_abs_err=0.000307 (2^-11.67), power_index=0.153
- unrolled_k [data_width=17 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=370, accuracy_bits=11.7, luts=270, ffs=100, throughput_msps=9.58, max_abs_err=0.000307 (2^-11.67), power_index=0.153
- unrolled_k [data_width=17 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=385, accuracy_bits=12, luts=283, ffs=102, throughput_msps=9.58, max_abs_err=0.000239 (2^-12.03), power_index=0.159
- unrolled_k [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=389, accuracy_bits=12.2, luts=286, ffs=103, throughput_msps=9.58, max_abs_err=0.000219 (2^-12.16), power_index=0.161
- unrolled_k [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=396, accuracy_bits=12.3, luts=290, ffs=106, throughput_msps=9.35, max_abs_err=0.000194 (2^-12.33), power_index=0.164
- unrolled_k [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=404, accuracy_bits=12.5, luts=299, ffs=105, throughput_msps=9.35, max_abs_err=0.000175 (2^-12.48), power_index=0.167
- unrolled_k [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=426, accuracy_bits=13.3, luts=316, ffs=110, throughput_msps=9.35, max_abs_err=0.000102 (2^-13.26), power_index=0.176
- unrolled_k [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=431, accuracy_bits=13.4, luts=320, ffs=111, throughput_msps=9.35, max_abs_err=9.49e-05 (2^-13.36), power_index=0.178
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts_plus_ffs=2070, accuracy_bits=13.5, luts=1039, ffs=1031, throughput_msps=264, max_abs_err=8.41e-05 (2^-13.54), power_index=0.0779
Front coverage: luts_plus_ffs 344..2070 (HV reference 1500); accuracy_bits 10.7..13.5 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- unrolled_k: 140 evals, 129 feasible; max throughput seen 14 MSPS; best accuracy 13.36 bits; best feasible luts_plus_ffs=344; feasible ranges: data_width 15..18, n_iter 13..16, angle_guard 0..2, frac_guard 0..2, k 2..8
- pipelined: 38 evals, 27 feasible; max throughput seen 282 MSPS; best accuracy 13.54 bits; best feasible luts_plus_ffs=1380; feasible ranges: data_width 15..18, n_iter 13..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 62 evals, 49 feasible; max throughput seen 171 MSPS; best accuracy 13.18 bits; best feasible luts_plus_ffs=853; feasible ranges: data_width 15..18, n_iter 13..16, angle_guard 0..2, frac_guard 0..2, m 2..8
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `unrolled_k` (139 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (13 front designs; box front_anchored)
- `pipelined` (21 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (2 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 356 feasible; hypervolume 1.393e+04 (+269.1%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and the selection rule (min luts_plus_ffs) is satisfied by a clear winner. The best design is `unrolled_k` with `data_width=15, n_iter=14, angle_guard=2, frac_guard=0, rounding=round, k=2`, achieving `luts_plus_ffs=344` and `accuracy_bits=10.7` (max_abs_err=0.000599), which comfortably meets the constraint `max_abs_err <= 0.000976562` (2^-10) and `throughput_msps >= 1` (10.5 MSPS). The front spans a wide range of area (344 to 2070) and accuracy (10.7 to 13.5 bits), covering the trade-off space effectively. The hypervolume gain in the last round was minimal (+0.4%), indicating convergence. Since this is the final round, stopping is the appropriate action to finalize the design selection.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.393e+04 (gain this round: +269.1%).
Feasible designs: 356 of 400 evaluations (301 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 11% violate; best seen 2.3e-08 (2^-25.37)

Pareto front (feasible, 26 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=15 n_iter=14 angle_guard=2 frac_guard=0 rounding=round k=2] luts_plus_ffs=344, accuracy_bits=10.7, luts=252, ffs=92, throughput_msps=10.5, max_abs_err=0.000599 (2^-10.71), power_index=0.129
- unrolled_k [data_width=17 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=370, accuracy_bits=11.7, luts=270, ffs=100, throughput_msps=9.58, max_abs_err=0.000307 (2^-11.67), power_index=0.153
- unrolled_k [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=389, accuracy_bits=12.2, luts=286, ffs=103, throughput_msps=9.58, max_abs_err=0.000219 (2^-12.16), power_index=0.161
- unrolled_k [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=396, accuracy_bits=12.3, luts=290, ffs=106, throughput_msps=9.35, max_abs_err=0.000194 (2^-12.33), power_index=0.164
- unrolled_k [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=426, accuracy_bits=13.3, luts=316, ffs=110, throughput_msps=9.35, max_abs_err=0.000102 (2^-13.26), power_index=0.176
- unrolled_k [data_width=21 n_iter=25 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=506, accuracy_bits=16, luts=382, ffs=124, throughput_msps=6.43, max_abs_err=1.56e-05 (2^-15.97), power_index=0.304
- unrolled_k [data_width=21 n_iter=26 angle_guard=2 frac_guard=1 rounding=round k=2] luts_plus_ffs=570, accuracy_bits=17.1, luts=445, ffs=125, throughput_msps=6.28, max_abs_err=6.89e-06 (2^-17.15), power_index=0.343
- unrolled_k [data_width=25 n_iter=25 angle_guard=2 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=596, accuracy_bits=19.4, luts=453, ffs=143, throughput_msps=6.13, max_abs_err=1.47e-06 (2^-19.37), power_index=0.359
- unrolled_k [data_width=27 n_iter=25 angle_guard=1 frac_guard=3 rounding=trunc k=2] luts_plus_ffs=704, accuracy_bits=22.3, luts=546, ffs=158, throughput_msps=6.13, max_abs_err=1.89e-07 (2^-22.33), power_index=0.424
- unrolled_k [data_width=28 n_iter=29 angle_guard=4 frac_guard=3 rounding=round k=4] luts_plus_ffs=1149, accuracy_bits=25.4, luts=984, ffs=165, throughput_msps=4.49, max_abs_err=2.3e-08 (2^-25.37), power_index=0.476
Front coverage: luts_plus_ffs 344..1149 (HV reference 1500); accuracy_bits 10.7..25.4 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- unrolled_k: 279 evals, 259 feasible; max throughput seen 14 MSPS; best accuracy 25.37 bits; best feasible luts_plus_ffs=344; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, k 2..8
- pipelined: 59 evals, 48 feasible; max throughput seen 282 MSPS; best accuracy 21.29 bits; best feasible luts_plus_ffs=1380; feasible ranges: data_width 15..25, n_iter 13..30, angle_guard -1..4, frac_guard 0..2
- pipelined_m: 62 evals, 49 feasible; max throughput seen 171 MSPS; best accuracy 13.18 bits; best feasible luts_plus_ffs=853; feasible ranges: data_width 15..18, n_iter 13..16, angle_guard 0..2, frac_guard 0..2, m 2..8
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 10317 in, 3889 out
- provider-reported cost: $0.0086
- full prompts and replies: `llm_trace.jsonl`

