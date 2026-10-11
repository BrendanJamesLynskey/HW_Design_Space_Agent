# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`iterative:data_width=16,n_iter=15,angle_guard=-1,frac_guard=0,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 168 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 95 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 11 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 90.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.178 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000829 (2^-10.24) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 13.6 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000193 (2^-12.34) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 3.17 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.2 | exact: bit-accurate model, exhaustive (65536 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 18 cycles, a new input every 18 cycle(s). DDS tone from its exact outputs: SFDR 85.7 dBc, SNR 71.6 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (40 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=16,n_iter=15,angle_guard=-1,frac_guard=0,rounding=trunc` | 168 | 95 | 11.0 | 18 | 0.178 | 0.000829 (2^-10.24) | 10.24 |
| 1 | `iterative:data_width=15,n_iter=16,angle_guard=3,frac_guard=1,rounding=trunc` | 174 | 96 | 10.4 | 19 | 0.193 | 0.000569 (2^-10.78) | 10.78 |
| 2 | `iterative:data_width=15,n_iter=13,angle_guard=3,frac_guard=2,rounding=trunc` | 183 | 98 | 12.4 | 16 | 0.169 | 0.000466 (2^-11.07) | 11.07 |
| 3 | `iterative:data_width=15,n_iter=16,angle_guard=4,frac_guard=3,rounding=trunc` | 195 | 101 | 10.2 | 19 | 0.211 | 0.000228 (2^-12.10) | 12.10 |
| 4 | `iterative:data_width=17,n_iter=16,angle_guard=4,frac_guard=0,rounding=round` | 196 | 105 | 10.2 | 19 | 0.215 | 0.000146 (2^-12.74) | 12.74 |
| 5 | `iterative:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 202 | 107 | 10.8 | 18 | 0.209 | 0.000119 (2^-13.04) | 13.04 |
| 6 | `iterative:data_width=18,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc` | 206 | 110 | 10.2 | 19 | 0.226 | 8.82e-05 (2^-13.47) | 13.47 |
| 7 | `iterative:data_width=17,n_iter=16,angle_guard=4,frac_guard=3,rounding=trunc` | 218 | 111 | 10.2 | 19 | 0.235 | 8.02e-05 (2^-13.61) | 13.61 |
| 8 | `iterative:data_width=18,n_iter=20,angle_guard=3,frac_guard=0,rounding=round` | 230 | 110 | 6.9 | 23 | 0.294 | 7.75e-05 (2^-13.65) | 13.65 |
| 9 | `iterative:data_width=20,n_iter=16,angle_guard=4,frac_guard=0,rounding=trunc` | 223 | 120 | 10.0 | 19 | 0.245 | 5.76e-05 (2^-14.08) | 14.08 |
| 10 | `iterative:data_width=18,n_iter=20,angle_guard=3,frac_guard=2,rounding=trunc` | 246 | 114 | 6.9 | 23 | 0.311 | 5.33e-05 (2^-14.20) | 14.20 |
| 11 | `iterative:data_width=22,n_iter=16,angle_guard=-1,frac_guard=0,rounding=trunc` | 237 | 125 | 10.2 | 19 | 0.259 | 4.1e-05 (2^-14.57) | 14.57 |
| 12 | `iterative:data_width=21,n_iter=16,angle_guard=4,frac_guard=0,rounding=round` | 242 | 125 | 10.0 | 19 | 0.262 | 3.63e-05 (2^-14.75) | 14.75 |
| 13 | `iterative:data_width=20,n_iter=20,angle_guard=0,frac_guard=0,rounding=round` | 256 | 117 | 6.9 | 23 | 0.323 | 3.25e-05 (2^-14.91) | 14.91 |
| 14 | `iterative:data_width=19,n_iter=20,angle_guard=3,frac_guard=2,rounding=trunc` | 262 | 119 | 6.9 | 23 | 0.33 | 2.62e-05 (2^-15.22) | 15.22 |
| 15 | `iterative:data_width=21,n_iter=21,angle_guard=1,frac_guard=0,rounding=trunc` | 266 | 123 | 6.6 | 24 | 0.352 | 2.36e-05 (2^-15.37) | 15.37 |
| 16 | `iterative:data_width=20,n_iter=25,angle_guard=4,frac_guard=0,rounding=round` | 269 | 121 | 5.6 | 28 | 0.411 | 2.17e-05 (2^-15.49) | 15.49 |
| 17 | `iterative:data_width=21,n_iter=20,angle_guard=1,frac_guard=1,rounding=trunc` | 276 | 125 | 6.9 | 23 | 0.347 | 1.38e-05 (2^-16.15) | 16.15 |
| 18 | `iterative:data_width=21,n_iter=21,angle_guard=2,frac_guard=0,rounding=round` | 282 | 124 | 6.5 | 24 | 0.366 | 1.15e-05 (2^-16.41) | 16.41 |
| 19 | `iterative:data_width=20,n_iter=20,angle_guard=3,frac_guard=3,rounding=trunc` | 292 | 126 | 6.8 | 23 | 0.362 | 9.41e-06 (2^-16.70) | 16.70 |
| 20 | `iterative:data_width=21,n_iter=20,angle_guard=1,frac_guard=3,rounding=trunc` | 304 | 129 | 6.8 | 23 | 0.375 | 9.21e-06 (2^-16.73) | 16.73 |
| 21 | `iterative:data_width=22,n_iter=28,angle_guard=3,frac_guard=1,rounding=trunc` | 305 | 132 | 5.0 | 31 | 0.509 | 7.82e-06 (2^-16.96) | 16.96 |
| 22 | `iterative:data_width=24,n_iter=21,angle_guard=-2,frac_guard=0,rounding=trunc` | 313 | 135 | 6.5 | 24 | 0.405 | 6.93e-06 (2^-17.14) | 17.14 |
| 23 | `iterative:data_width=23,n_iter=24,angle_guard=2,frac_guard=0,rounding=round` | 317 | 134 | 5.8 | 27 | 0.458 | 2.9e-06 (2^-18.39) | 18.39 |
| 24 | `iterative:data_width=25,n_iter=27,angle_guard=-1,frac_guard=0,rounding=trunc` | 337 | 141 | 5.2 | 30 | 0.54 | 2.8e-06 (2^-18.45) | 18.45 |
| 25 | `iterative:data_width=25,n_iter=20,angle_guard=3,frac_guard=0,rounding=round` | 341 | 145 | 6.7 | 23 | 0.421 | 2.49e-06 (2^-18.61) | 18.61 |
| 26 | `iterative:data_width=24,n_iter=26,angle_guard=4,frac_guard=1,rounding=trunc` | 344 | 143 | 5.3 | 29 | 0.532 | 1.76e-06 (2^-19.11) | 19.11 |
| 27 | `iterative:data_width=25,n_iter=21,angle_guard=1,frac_guard=0,rounding=round` | 350 | 143 | 6.5 | 24 | 0.445 | 1.73e-06 (2^-19.14) | 19.14 |
| 28 | `iterative:data_width=23,n_iter=25,angle_guard=4,frac_guard=3,rounding=trunc` | 360 | 142 | 5.5 | 28 | 0.529 | 1.17e-06 (2^-19.70) | 19.70 |
| 29 | `iterative:data_width=27,n_iter=23,angle_guard=-2,frac_guard=0,rounding=round` | 379 | 150 | 5.9 | 26 | 0.518 | 1.05e-06 (2^-19.86) | 19.86 |
| 30 | `iterative:data_width=27,n_iter=23,angle_guard=4,frac_guard=0,rounding=trunc` | 377 | 156 | 5.8 | 26 | 0.521 | 5e-07 (2^-20.93) | 20.93 |
| 31 | `iterative:data_width=27,n_iter=26,angle_guard=0,frac_guard=0,rounding=round` | 392 | 152 | 5.3 | 29 | 0.594 | 3.4e-07 (2^-21.49) | 21.49 |
| 32 | `iterative:data_width=28,n_iter=24,angle_guard=1,frac_guard=0,rounding=trunc` | 389 | 158 | 5.7 | 27 | 0.556 | 2.99e-07 (2^-21.67) | 21.67 |
| 33 | `iterative:data_width=28,n_iter=25,angle_guard=1,frac_guard=0,rounding=trunc` | 398 | 158 | 5.5 | 28 | 0.586 | 2.55e-07 (2^-21.91) | 21.91 |
| 34 | `iterative:data_width=28,n_iter=24,angle_guard=2,frac_guard=1,rounding=trunc` | 406 | 161 | 5.7 | 27 | 0.577 | 1.87e-07 (2^-22.35) | 22.35 |
| 35 | `iterative:data_width=28,n_iter=28,angle_guard=4,frac_guard=0,rounding=round` | 418 | 161 | 4.9 | 31 | 0.676 | 1.03e-07 (2^-23.22) | 23.22 |
| 36 | `iterative:data_width=28,n_iter=25,angle_guard=4,frac_guard=1,rounding=round` | 495 | 163 | 5.4 | 28 | 0.693 | 9.69e-08 (2^-23.30) | 23.30 |
| 37 | `iterative:data_width=27,n_iter=25,angle_guard=4,frac_guard=3,rounding=round` | 508 | 162 | 5.4 | 28 | 0.706 | 9.01e-08 (2^-23.40) | 23.40 |
| 38 | `iterative:data_width=28,n_iter=25,angle_guard=3,frac_guard=4,rounding=round` | 544 | 168 | 5.4 | 28 | 0.751 | 7.42e-08 (2^-23.68) | 23.68 |
| 39 | `iterative:data_width=28,n_iter=25,angle_guard=4,frac_guard=4,rounding=round` | 546 | 169 | 5.4 | 28 | 0.754 | 7.07e-08 (2^-23.75) | 23.75 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraint is accuracy, not throughput: 1 MSPS is far below what any family reaches (even iterative at N=22 and a pessimistic 100 MHz gives ~4 MSPS), so the throughput constraint is essentially free and the real problem is 'smallest area that still hits max_abs_err <= 2^-10'. Because accuracy depends only on (data_width, n_iter, angle_guard, frac_guard, rounding) and is identical across families, the min-area design at every accuracy level is the family with the smallest datapath — the shared-datapath iterative core. So the Pareto front should be iterative-dominated, and that is where most of the budget goes. I hedge with the two next-smallest families (unrolled_k with small k, pipelined_m with large m) in case the cost model makes one of them competitive at some accuracy point, and I drop the fully pipelined family because pipelined_m with small m strictly dominates it in area. Ranges are centred on the accuracy threshold: output LSB is 2^-(W-2) and CORDIC angle error is ~2^-N, so both W and N must clear ~11-12; I extend W and N upward to trace the front out toward the HV reference area of 1500, and allow negative angle_guard / zero frac_guard so the optimiser can strip area where accuracy permits.*)
- `iterative` (60 evals): data_width=10..22, n_iter=9..22, angle_guard=-2..4, frac_guard=0..3, rounding=trunc|round. *Why:* Smallest-area family (one shared micro-rotation datapath with barrel shifters). Throughput is trivially satisfied at every N in range, and since accuracy is family-independent it should own the whole area/accuracy front. Widest ranges and the majority of the budget.
- `unrolled_k` (28 evals): data_width=10..22, n_iter=9..22, angle_guard=-2..4, frac_guard=0..3, rounding=trunc|round, k=2..4. *Why:* Shares the datapath but chains k rotations per cycle, so it sits between iterative and pipelined in area. Cycles are not an objective here, so it is probably dominated, but small k (2-3) keeps it close to iterative and it is a cheap hedge in case the cost model favours it at some accuracy points.
- `pipelined_m` (12 evals): data_width=10..22, n_iter=9..22, angle_guard=-2..4, frac_guard=0..3, rounding=trunc|round, m=4..8. *Why:* Unrolled datapath with registers every m stages; large m (6-8) minimises register count, but it still carries N adders, so area should exceed iterative. Small share to confirm dominance and to cover the unlikely case where its higher Fmax changes the picture. Replaces the fully pipelined family, which it dominates at small m.

**Result (code):** 100 evaluations this round, 100 total; 72 feasible; hypervolume 7696 (n/a).

**LLM decision:** `map_front` — The feasible front is entirely `iterative` and spans only luts_plus_ffs 281..418 against an HV reference of 1500, and accuracy_bits 10.7..16.7 while the registry (data_width up to 28, n_iter up to 30) can clearly reach far higher accuracy — the best accuracy seen anywhere is only 16.70 bits. So the front covers a small part of both objectives' ranges, and since the area reference point (1500) is far above every front point, each extra accuracy bit added at low area buys a large HV rectangle. The throughput constraint (>=1 MSPS) is already satisfied by every design (0% violate, best 108 MSPS), so the high-throughput pipelined/pipelined_m families are irrelevant to the min-area objective and adding `pipelined` would only burn budget on dominated, high-area designs (pipelined_m best area already 1465). The right move is to let code spend this round mapping the whole front over the full ranges of the families on it (iterative, plus the feasible unrolled_k/pipelined_m points), seeded with the current front, to extend the accuracy/area coverage before the reserved mapping phase.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 7696 (gain this round: n/a (first round)).
Feasible designs: 72 of 100 evaluations (64 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 108
- max_abs_err <= 0.000976562: 28% violate; best seen 9.41e-06 (2^-16.70)

Pareto front (feasible, 12 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=18 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=281, accuracy_bits=10.7, luts=184, ffs=97, throughput_msps=7.71, max_abs_err=0.000586 (2^-10.74), power_index=0.222
- iterative [data_width=15 n_iter=13 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=281, accuracy_bits=11.1, luts=183, ffs=98, throughput_msps=12.4, max_abs_err=0.000466 (2^-11.07), power_index=0.169
- iterative [data_width=18 n_iter=13 angle_guard=-2 frac_guard=2 rounding=trunc] luts_plus_ffs=317, accuracy_bits=11.2, luts=209, ffs=108, throughput_msps=12.1, max_abs_err=0.000433 (2^-11.17), power_index=0.191
- iterative [data_width=18 n_iter=20 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=331, accuracy_bits=13.1, luts=224, ffs=107, throughput_msps=7.04, max_abs_err=0.000114 (2^-13.10), power_index=0.286
- iterative [data_width=18 n_iter=20 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=340, accuracy_bits=13.7, luts=230, ffs=110, throughput_msps=6.91, max_abs_err=7.75e-05 (2^-13.65), power_index=0.294
- iterative [data_width=18 n_iter=20 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=360, accuracy_bits=14.2, luts=246, ffs=114, throughput_msps=6.91, max_abs_err=5.33e-05 (2^-14.20), power_index=0.311
- iterative [data_width=20 n_iter=20 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=370, accuracy_bits=14.5, luts=249, ffs=120, throughput_msps=6.78, max_abs_err=4.23e-05 (2^-14.53), power_index=0.32
- iterative [data_width=19 n_iter=20 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=381, accuracy_bits=15.2, luts=262, ffs=119, throughput_msps=6.91, max_abs_err=2.62e-05 (2^-15.22), power_index=0.33
- iterative [data_width=20 n_iter=20 angle_guard=1 frac_guard=3 rounding=trunc] luts_plus_ffs=412, accuracy_bits=15.9, luts=288, ffs=124, throughput_msps=6.78, max_abs_err=1.68e-05 (2^-15.86), power_index=0.357
- iterative [data_width=20 n_iter=20 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=418, accuracy_bits=16.7, luts=292, ffs=126, throughput_msps=6.78, max_abs_err=9.41e-06 (2^-16.70), power_index=0.362
Front coverage: luts_plus_ffs 281..418 (HV reference 1500); accuracy_bits 10.7..16.7 (HV reference 10); data_width on the front 15..20 (registry 8..28).

Per family:
- iterative: 60 evals, 45 feasible; max throughput seen 16.5 MSPS; best accuracy 16.70 bits; best feasible luts_plus_ffs=281; feasible ranges: data_width 15..21, n_iter 13..22, angle_guard -2..3, frac_guard 0..3
- unrolled_k: 28 evals, 20 feasible; max throughput seen 14.8 MSPS; best accuracy 16.70 bits; best feasible luts_plus_ffs=348; feasible ranges: data_width 15..21, n_iter 12..21, angle_guard -1..3, frac_guard 0..3, k 2..4
- pipelined_m: 12 evals, 7 feasible; max throughput seen 108 MSPS; best accuracy 15.18 bits; best feasible luts_plus_ffs=1465; feasible ranges: data_width 18..22, n_iter 16..20, angle_guard -2..4, frac_guard 0..2, m 4..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (12 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 164 feasible; hypervolume 1.447e+04 (+88.0%).

**LLM decision:** `map_front` — Both constraints are already comfortably satisfied everywhere they matter (0% throughput violations, best throughput 108 MSPS vs the 1 MSPS floor; best err 2^-23.75 vs the 2^-10 ceiling), so this is purely a front-coverage/HV problem, not a feasibility problem. The feasible front is densely populated but strongly one-sided: accuracy spans 10.8..23.8 bits (near its achievable ceiling given data_width caps at 28), while luts_plus_ffs only reaches 716 against an HV reference of 1500, and the whole registry was only ever sampled down to data_width=14 (front min is d=15). The covered area band (269..716 of 0..1500) is therefore a small part of the objective range, and the deep low-area corner that the selection rule (min luts_plus_ffs) actually picks is thin - only the 269 and 316 points sit below ~350. A seeded NSGA-II pass over the full ranges of the families on the front (iterative, plus unrolled_k/pipelined_m where they contribute) is the right use of this round: it applies budget exactly where the staircase is under-sampled (low data_width/low n_iter to push the 269 corner down, and the 716..1500 area gap where higher-accuracy points can still add HV). Adding pipelined is not worth a round: it cannot win min luts_plus_ffs (its per-stage registers make it more area-expensive than pipelined_m, whose best feasible area is already 1465, and iterative is 269), its accuracy is bounded by the same (data_width,n_iter,angle_guard,frac_guard,rounding) parameters that iterative already maxes out at 23.75 bits, and its extra throughput beyond the 1 MSPS requirement earns no HV - so it would be dominated and the reserved mapping pass would only re-confirm that.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.447e+04 (gain this round: +88.0%).
Feasible designs: 164 of 200 evaluations (149 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 108
- max_abs_err <= 0.000976562: 18% violate; best seen 7.07e-08 (2^-23.75)

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=16 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=269, accuracy_bits=10.8, luts=174, ffs=96, throughput_msps=10.4, max_abs_err=0.000569 (2^-10.78), power_index=0.193
- iterative [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=316, accuracy_bits=13.5, luts=206, ffs=110, throughput_msps=10.2, max_abs_err=8.82e-05 (2^-13.47), power_index=0.226
- iterative [data_width=20 n_iter=16 angle_guard=4 frac_guard=0 rounding=trunc] luts_plus_ffs=343, accuracy_bits=14.1, luts=223, ffs=120, throughput_msps=9.97, max_abs_err=5.76e-05 (2^-14.08), power_index=0.245
- iterative [data_width=20 n_iter=20 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=373, accuracy_bits=14.9, luts=256, ffs=117, throughput_msps=6.91, max_abs_err=3.25e-05 (2^-14.91), power_index=0.323
- iterative [data_width=20 n_iter=24 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=405, accuracy_bits=16, luts=282, ffs=123, throughput_msps=5.89, max_abs_err=1.54e-05 (2^-15.99), power_index=0.411
- iterative [data_width=22 n_iter=28 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=437, accuracy_bits=17, luts=305, ffs=132, throughput_msps=5.03, max_abs_err=7.82e-06 (2^-16.96), power_index=0.509
- iterative [data_width=24 n_iter=26 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=488, accuracy_bits=19.1, luts=344, ffs=143, throughput_msps=5.28, max_abs_err=1.76e-06 (2^-19.11), power_index=0.532
- iterative [data_width=25 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=545, accuracy_bits=21.2, luts=394, ffs=150, throughput_msps=5.47, max_abs_err=4.08e-07 (2^-21.23), power_index=0.574
- iterative [data_width=28 n_iter=24 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=580, accuracy_bits=22.1, luts=418, ffs=161, throughput_msps=5.68, max_abs_err=2.15e-07 (2^-22.15), power_index=0.589
- iterative [data_width=28 n_iter=25 angle_guard=4 frac_guard=4 rounding=round] luts_plus_ffs=716, accuracy_bits=23.8, luts=546, ffs=169, throughput_msps=5.38, max_abs_err=7.07e-08 (2^-23.75), power_index=0.754
Front coverage: luts_plus_ffs 269..716 (HV reference 1500); accuracy_bits 10.8..23.8 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 160 evals, 137 feasible; max throughput seen 16.5 MSPS; best accuracy 23.75 bits; best feasible luts_plus_ffs=269; feasible ranges: data_width 14..28, n_iter 12..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 28 evals, 20 feasible; max throughput seen 14.8 MSPS; best accuracy 16.70 bits; best feasible luts_plus_ffs=348; feasible ranges: data_width 15..21, n_iter 12..21, angle_guard -1..3, frac_guard 0..3, k 2..4
- pipelined_m: 12 evals, 7 feasible; max throughput seen 108 MSPS; best accuracy 15.18 bits; best feasible luts_plus_ffs=1465; feasible ranges: data_width 18..22, n_iter 16..20, angle_guard -2..4, frac_guard 0..2, m 4..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (25 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 300 total; 258 feasible; hypervolume 1.456e+04 (+0.6%).

**LLM decision:** `map_front` — Round 3 is near-converged: HV gain was only +0.6% and the feasible front (36 designs) is entirely `iterative`. The selection rule (min luts_plus_ffs) is already secured by iterative [d16 n15 ag-1 fg0 trunc] at luts_plus_ffs=263, accuracy 10.2 bits — comfortably inside both constraints (throughput 11 MSPS >= 1, err 2^-10.24 <= 2^-10). The front spans accuracy_bits 10.2..23.8 against an HV ref of 10, i.e. it already reaches the accuracy ceiling (best seen 23.75 bits at data_width=28, the registry max), so no family can push accuracy further. The area range 263..716 vs ref 1500 is the only 'uncovered' stretch, but that is inherent to a min-area objective and cannot be filled by higher-accuracy points (accuracy is capped). Adding `pipelined` is not worth budget: its cheaper sibling `pipelined_m` already bottoms out at luts_plus_ffs=1465 (near the 1500 ref) with only 15.2 bits, and `pipelined` registers every stage so it is strictly larger — it cannot improve the min-area corner nor add HV. `unrolled_k` (best 348) and `pipelined_m` (best 1465) are both dominated by iterative on area. So the right use of the last 100 evals is the reserved front-mapping pass over the family that actually owns the front.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.456e+04 (gain this round: +0.6%).
Feasible designs: 258 of 300 evaluations (228 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 108
- max_abs_err <= 0.000976562: 14% violate; best seen 7.07e-08 (2^-23.75)

Pareto front (feasible, 36 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=15 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=263, accuracy_bits=10.2, luts=168, ffs=95, throughput_msps=11, max_abs_err=0.000829 (2^-10.24), power_index=0.178
- iterative [data_width=17 n_iter=16 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=301, accuracy_bits=12.7, luts=196, ffs=105, throughput_msps=10.2, max_abs_err=0.000146 (2^-12.74), power_index=0.215
- iterative [data_width=20 n_iter=16 angle_guard=4 frac_guard=0 rounding=trunc] luts_plus_ffs=343, accuracy_bits=14.1, luts=223, ffs=120, throughput_msps=9.97, max_abs_err=5.76e-05 (2^-14.08), power_index=0.245
- iterative [data_width=19 n_iter=20 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=381, accuracy_bits=15.2, luts=262, ffs=119, throughput_msps=6.91, max_abs_err=2.62e-05 (2^-15.22), power_index=0.33
- iterative [data_width=21 n_iter=21 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=416, accuracy_bits=16.2, luts=287, ffs=128, throughput_msps=6.5, max_abs_err=1.31e-05 (2^-16.21), power_index=0.375
- iterative [data_width=22 n_iter=28 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=437, accuracy_bits=17, luts=305, ffs=132, throughput_msps=5.03, max_abs_err=7.82e-06 (2^-16.96), power_index=0.509
- iterative [data_width=24 n_iter=26 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=488, accuracy_bits=19.1, luts=344, ffs=143, throughput_msps=5.28, max_abs_err=1.76e-06 (2^-19.11), power_index=0.532
- iterative [data_width=25 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=545, accuracy_bits=21.2, luts=394, ffs=150, throughput_msps=5.47, max_abs_err=4.08e-07 (2^-21.23), power_index=0.574
- iterative [data_width=25 n_iter=29 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=620, accuracy_bits=22.2, luts=468, ffs=151, throughput_msps=4.79, max_abs_err=2.1e-07 (2^-22.18), power_index=0.746
- iterative [data_width=28 n_iter=25 angle_guard=4 frac_guard=4 rounding=round] luts_plus_ffs=716, accuracy_bits=23.8, luts=546, ffs=169, throughput_msps=5.38, max_abs_err=7.07e-08 (2^-23.75), power_index=0.754
Front coverage: luts_plus_ffs 263..716 (HV reference 1500); accuracy_bits 10.2..23.8 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 260 evals, 231 feasible; max throughput seen 16.5 MSPS; best accuracy 23.75 bits; best feasible luts_plus_ffs=263; feasible ranges: data_width 14..28, n_iter 11..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 28 evals, 20 feasible; max throughput seen 14.8 MSPS; best accuracy 16.70 bits; best feasible luts_plus_ffs=348; feasible ranges: data_width 15..21, n_iter 12..21, angle_guard -1..3, frac_guard 0..3, k 2..4
- pipelined_m: 12 evals, 7 feasible; max throughput seen 108 MSPS; best accuracy 15.18 bits; best feasible luts_plus_ffs=1465; feasible ranges: data_width 18..22, n_iter 16..20, angle_guard -2..4, frac_guard 0..2, m 4..8
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (36 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 346 feasible; hypervolume 1.467e+04 (+0.8%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), so the only admissible decisions are stop or infeasible. Infeasible is ruled out by evidence: 346 of 400 evaluations are feasible, and both constraints are met with wide margin — throughput best seen 108 MSPS vs the >=1 MSPS requirement (0% of evaluations violate it), and max_abs_err best seen 7.07e-08 (2^-23.75) vs the <=2^-10 requirement. The feasible front already spans luts_plus_ffs 263..716 against the HV reference 1500 and accuracy_bits 10.2..23.8 against the reference 10, i.e. it covers both objective ranges well past their reference points, and this round's hypervolume gain was only +0.8% (1.467e+04), indicating the front has converged. The spec's selection rule (min luts_plus_ffs) is served by iterative [data_width=16 n_iter=15 angle_guard=-1 frac_guard=0 rounding=trunc] at luts_plus_ffs=263, accuracy_bits=10.2 (max_abs_err 8.29e-04 <= 9.77e-04) and 11 MSPS >= 1 MSPS, so a valid, constraint-satisfying minimum-area design exists. The unexplored `pipelined` family is not needed: its only advantage is throughput, which is already satisfied by a large margin by the cheapest iterative design, and it would cost area (pipelined_m's best feasible luts_plus_ffs was 1465, ~5.6x the front's minimum).

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.467e+04 (gain this round: +0.8%).
Feasible designs: 346 of 400 evaluations (306 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 108
- max_abs_err <= 0.000976562: 14% violate; best seen 7.07e-08 (2^-23.75)

Pareto front (feasible, 40 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=15 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=263, accuracy_bits=10.2, luts=168, ffs=95, throughput_msps=11, max_abs_err=0.000829 (2^-10.24), power_index=0.178
- iterative [data_width=17 n_iter=16 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=301, accuracy_bits=12.7, luts=196, ffs=105, throughput_msps=10.2, max_abs_err=0.000146 (2^-12.74), power_index=0.215
- iterative [data_width=20 n_iter=16 angle_guard=4 frac_guard=0 rounding=trunc] luts_plus_ffs=343, accuracy_bits=14.1, luts=223, ffs=120, throughput_msps=9.97, max_abs_err=5.76e-05 (2^-14.08), power_index=0.245
- iterative [data_width=20 n_iter=20 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=373, accuracy_bits=14.9, luts=256, ffs=117, throughput_msps=6.91, max_abs_err=3.25e-05 (2^-14.91), power_index=0.323
- iterative [data_width=21 n_iter=20 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=401, accuracy_bits=16.1, luts=276, ffs=125, throughput_msps=6.91, max_abs_err=1.38e-05 (2^-16.15), power_index=0.347
- iterative [data_width=24 n_iter=21 angle_guard=-2 frac_guard=0 rounding=trunc] luts_plus_ffs=449, accuracy_bits=17.1, luts=313, ffs=135, throughput_msps=6.5, max_abs_err=6.93e-06 (2^-17.14), power_index=0.405
- iterative [data_width=24 n_iter=26 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=488, accuracy_bits=19.1, luts=344, ffs=143, throughput_msps=5.28, max_abs_err=1.76e-06 (2^-19.11), power_index=0.532
- iterative [data_width=27 n_iter=23 angle_guard=4 frac_guard=0 rounding=trunc] luts_plus_ffs=533, accuracy_bits=20.9, luts=377, ffs=156, throughput_msps=5.79, max_abs_err=5e-07 (2^-20.93), power_index=0.521
- iterative [data_width=28 n_iter=28 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=580, accuracy_bits=23.2, luts=418, ffs=161, throughput_msps=4.86, max_abs_err=1.03e-07 (2^-23.22), power_index=0.676
- iterative [data_width=28 n_iter=25 angle_guard=4 frac_guard=4 rounding=round] luts_plus_ffs=716, accuracy_bits=23.8, luts=546, ffs=169, throughput_msps=5.38, max_abs_err=7.07e-08 (2^-23.75), power_index=0.754
Front coverage: luts_plus_ffs 263..716 (HV reference 1500); accuracy_bits 10.2..23.8 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 360 evals, 319 feasible; max throughput seen 16.5 MSPS; best accuracy 23.75 bits; best feasible luts_plus_ffs=263; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 28 evals, 20 feasible; max throughput seen 14.8 MSPS; best accuracy 16.70 bits; best feasible luts_plus_ffs=348; feasible ranges: data_width 15..21, n_iter 12..21, angle_guard -1..3, frac_guard 0..3, k 2..4
- pipelined_m: 12 evals, 7 feasible; max throughput seen 108 MSPS; best accuracy 15.18 bits; best feasible luts_plus_ffs=1465; feasible ranges: data_width 18..22, n_iter 16..20, angle_guard -2..4, frac_guard 0..2, m 4..8
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 13206 in, 18938 out
- provider-reported cost: $0.0148
- full prompts and replies: `llm_trace.jsonl`

