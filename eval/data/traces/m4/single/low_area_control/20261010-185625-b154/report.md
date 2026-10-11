# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 400 of 400 budgeted, over 5 round(s).  
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
`iterative:data_width=15,n_iter=15,angle_guard=4,frac_guard=1,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 175 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 97 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 194 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 10.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 92.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.184 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000569 (2^-10.78) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 4.66 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000131 (2^-12.89) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.08 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.8 | exact: bit-accurate model, exhaustive (32768 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 18 cycles, a new input every 18 cycle(s). DDS tone from its exact outputs: SFDR 87.4 dBc, SNR 74.7 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (40 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=15,angle_guard=4,frac_guard=1,rounding=trunc` | 175 | 97 | 10.8 | 18 | 0.184 | 0.000569 (2^-10.78) | 10.78 |
| 1 | `iterative:data_width=17,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc` | 181 | 101 | 10.4 | 19 | 0.202 | 0.000307 (2^-11.67) | 11.67 |
| 2 | `iterative:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=trunc` | 193 | 106 | 11.7 | 17 | 0.191 | 0.000251 (2^-11.96) | 11.96 |
| 3 | `iterative:data_width=15,n_iter=16,angle_guard=3,frac_guard=4,rounding=trunc` | 203 | 102 | 10.2 | 19 | 0.218 | 0.000219 (2^-12.16) | 12.16 |
| 4 | `iterative:data_width=17,n_iter=16,angle_guard=0,frac_guard=2,rounding=trunc` | 201 | 105 | 10.2 | 19 | 0.218 | 0.000207 (2^-12.24) | 12.24 |
| 5 | `iterative:data_width=18,n_iter=14,angle_guard=0,frac_guard=1,rounding=trunc` | 203 | 108 | 11.4 | 17 | 0.199 | 0.000205 (2^-12.25) | 12.25 |
| 6 | `iterative:data_width=17,n_iter=21,angle_guard=1,frac_guard=0,rounding=round` | 211 | 103 | 6.7 | 24 | 0.284 | 0.000149 (2^-12.71) | 12.71 |
| 7 | `iterative:data_width=17,n_iter=21,angle_guard=3,frac_guard=0,rounding=round` | 215 | 105 | 6.6 | 24 | 0.289 | 0.000146 (2^-12.74) | 12.74 |
| 8 | `iterative:data_width=19,n_iter=15,angle_guard=2,frac_guard=0,rounding=trunc` | 208 | 113 | 10.8 | 18 | 0.217 | 0.000109 (2^-13.17) | 13.17 |
| 9 | `iterative:data_width=19,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 212 | 111 | 10.2 | 19 | 0.231 | 7.72e-05 (2^-13.66) | 13.66 |
| 10 | `iterative:data_width=19,n_iter=17,angle_guard=1,frac_guard=0,rounding=round` | 242 | 113 | 7.9 | 20 | 0.267 | 5.02e-05 (2^-14.28) | 14.28 |
| 11 | `iterative:data_width=19,n_iter=18,angle_guard=1,frac_guard=1,rounding=trunc` | 244 | 115 | 7.6 | 21 | 0.284 | 4.91e-05 (2^-14.31) | 14.31 |
| 12 | `iterative:data_width=20,n_iter=16,angle_guard=4,frac_guard=2,rounding=trunc` | 242 | 124 | 10.0 | 19 | 0.262 | 3.8e-05 (2^-14.68) | 14.68 |
| 13 | `iterative:data_width=20,n_iter=18,angle_guard=0,frac_guard=0,rounding=round` | 256 | 117 | 7.6 | 21 | 0.295 | 3.54e-05 (2^-14.79) | 14.79 |
| 14 | `iterative:data_width=20,n_iter=20,angle_guard=1,frac_guard=0,rounding=round` | 258 | 118 | 6.9 | 23 | 0.325 | 2.52e-05 (2^-15.28) | 15.28 |
| 15 | `iterative:data_width=20,n_iter=23,angle_guard=3,frac_guard=1,rounding=trunc` | 268 | 122 | 6.0 | 26 | 0.382 | 2.42e-05 (2^-15.34) | 15.34 |
| 16 | `iterative:data_width=21,n_iter=21,angle_guard=0,frac_guard=0,rounding=round` | 278 | 122 | 6.6 | 24 | 0.361 | 1.79e-05 (2^-15.77) | 15.77 |
| 17 | `iterative:data_width=21,n_iter=23,angle_guard=0,frac_guard=0,rounding=round` | 278 | 122 | 6.1 | 26 | 0.391 | 1.79e-05 (2^-15.77) | 15.77 |
| 18 | `iterative:data_width=22,n_iter=20,angle_guard=1,frac_guard=0,rounding=trunc` | 278 | 128 | 6.8 | 23 | 0.351 | 1.22e-05 (2^-16.32) | 16.32 |
| 19 | `iterative:data_width=21,n_iter=27,angle_guard=4,frac_guard=0,rounding=round` | 287 | 126 | 5.2 | 30 | 0.466 | 1.15e-05 (2^-16.41) | 16.41 |
| 20 | `iterative:data_width=22,n_iter=21,angle_guard=0,frac_guard=0,rounding=round` | 296 | 127 | 6.6 | 24 | 0.382 | 8.91e-06 (2^-16.78) | 16.78 |
| 21 | `iterative:data_width=23,n_iter=20,angle_guard=0,frac_guard=1,rounding=trunc` | 306 | 134 | 6.8 | 23 | 0.381 | 5.06e-06 (2^-17.59) | 17.59 |
| 22 | `iterative:data_width=23,n_iter=21,angle_guard=0,frac_guard=0,rounding=round` | 313 | 132 | 6.5 | 24 | 0.402 | 4.39e-06 (2^-17.80) | 17.80 |
| 23 | `iterative:data_width=23,n_iter=21,angle_guard=1,frac_guard=0,rounding=round` | 315 | 133 | 6.5 | 24 | 0.405 | 3.03e-06 (2^-18.33) | 18.33 |
| 24 | `iterative:data_width=24,n_iter=29,angle_guard=0,frac_guard=0,rounding=round` | 337 | 137 | 4.9 | 32 | 0.57 | 2.49e-06 (2^-18.62) | 18.62 |
| 25 | `iterative:data_width=23,n_iter=25,angle_guard=1,frac_guard=3,rounding=trunc` | 354 | 139 | 5.6 | 28 | 0.52 | 2.23e-06 (2^-18.78) | 18.78 |
| 26 | `iterative:data_width=24,n_iter=26,angle_guard=0,frac_guard=2,rounding=trunc` | 354 | 141 | 5.4 | 29 | 0.541 | 2.2e-06 (2^-18.79) | 18.79 |
| 27 | `iterative:data_width=26,n_iter=23,angle_guard=1,frac_guard=0,rounding=trunc` | 354 | 148 | 5.9 | 26 | 0.491 | 9.02e-07 (2^-20.08) | 20.08 |
| 28 | `iterative:data_width=26,n_iter=23,angle_guard=2,frac_guard=1,rounding=trunc` | 371 | 151 | 5.9 | 26 | 0.511 | 5.25e-07 (2^-20.86) | 20.86 |
| 29 | `iterative:data_width=26,n_iter=28,angle_guard=1,frac_guard=1,rounding=trunc` | 377 | 150 | 4.9 | 31 | 0.615 | 4.76e-07 (2^-21.00) | 21.00 |
| 30 | `iterative:data_width=26,n_iter=26,angle_guard=4,frac_guard=0,rounding=round` | 380 | 151 | 5.3 | 29 | 0.58 | 3.6e-07 (2^-21.40) | 21.40 |
| 31 | `iterative:data_width=27,n_iter=29,angle_guard=0,frac_guard=0,rounding=round` | 395 | 152 | 4.8 | 32 | 0.659 | 3.4e-07 (2^-21.49) | 21.49 |
| 32 | `iterative:data_width=28,n_iter=23,angle_guard=1,frac_guard=0,rounding=round` | 402 | 158 | 5.9 | 26 | 0.548 | 3.24e-07 (2^-21.56) | 21.56 |
| 33 | `iterative:data_width=28,n_iter=25,angle_guard=1,frac_guard=0,rounding=round` | 413 | 158 | 5.5 | 28 | 0.602 | 1.58e-07 (2^-22.59) | 22.59 |
| 34 | `iterative:data_width=28,n_iter=29,angle_guard=0,frac_guard=1,rounding=trunc` | 418 | 159 | 4.8 | 32 | 0.695 | 1.54e-07 (2^-22.63) | 22.63 |
| 35 | `iterative:data_width=28,n_iter=29,angle_guard=1,frac_guard=1,rounding=trunc` | 420 | 160 | 4.8 | 32 | 0.698 | 1.27e-07 (2^-22.90) | 22.90 |
| 36 | `iterative:data_width=28,n_iter=29,angle_guard=1,frac_guard=3,rounding=trunc` | 457 | 164 | 4.7 | 32 | 0.748 | 8.09e-08 (2^-23.56) | 23.56 |
| 37 | `iterative:data_width=28,n_iter=27,angle_guard=4,frac_guard=1,rounding=round` | 495 | 163 | 5.0 | 30 | 0.742 | 5.86e-08 (2^-24.02) | 24.02 |
| 38 | `iterative:data_width=28,n_iter=30,angle_guard=4,frac_guard=1,rounding=round` | 501 | 163 | 4.6 | 33 | 0.824 | 5.57e-08 (2^-24.10) | 24.10 |
| 39 | `iterative:data_width=27,n_iter=27,angle_guard=3,frac_guard=4,rounding=round` | 523 | 163 | 5.0 | 30 | 0.775 | 5.51e-08 (2^-24.11) | 24.11 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec's throughput floor (1 MSPS) is trivially met by every family at these Fmax values (even iterative with N+3≈33 cycles clears it by a wide margin), so throughput is NOT the binding constraint. Accuracy is family-independent (identical bit-level datapath for the same W/N/guards/rounding), so the only real trade-off is area (luts_plus_ffs) vs accuracy_bits. That means the area-minimising family (iterative, one shared datapath) should dominate the front, and the useful exploration is over the accuracy boundary: W and N near the 2^-10 error limit, plus angle_guard/frac_guard/rounding which trade a little area for error headroom. Round 1 therefore spends most of the budget on iterative over a wide W/N window that brackets the feasible edge (W≈12-14, N≈11-14 expected), and gives smaller shares to unrolled_k and pipelined_m only to confirm they cannot undercut iterative on area and to catch any throughput-driven front segment. Ranges are deliberately wide in round 1 (W 10..18, N 8..20) so the NSGA-II can locate the feasible boundary; later rounds will narrow around whatever edge appears.*)
- `iterative` (65 evals): data_width=10..18, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Smallest-area family: one shared micro-rotation datapath with barrel shifters, N+3 cycles/result. At ~100+ MHz and N<=20 this still gives >4 MSPS, so the 1 MSPS floor is never binding and area is free to be minimised. This is where the min-luts_plus_ffs selection rule will almost certainly land, and where the accuracy-vs-area front lives. Wide W/N window brackets the 2^-10 error edge; guards/rounding give the model room to trade a few LUTs for error headroom.
- `unrolled_k` (20 evals): data_width=10..18, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..4. *Why:* k chained micro-rotations/cycle raises throughput but duplicates shifters/adders, so it should be strictly larger in area than iterative for the same accuracy. Included with a modest share to verify it does not offer a cheaper area point (e.g. small k with small W) and to cover any front segment where extra throughput is traded for area. k kept small (2..4) since larger k only inflates area with no benefit given the loose throughput floor.
- `pipelined_m` (15 evals): data_width=10..18, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Register-every-m-stages pipelined variant: 1 result/cycle but N/m register banks, so area is far above iterative. Given the 1 MSPS floor is already met by iterative, this family is only sampled to confirm it never produces a smaller luts_plus_ffs point and to map the high-throughput end of the front in case the reference point rewards it. Small share; m swept 2..8 to span the register-density range.

**Result (code):** 100 evaluations this round, 100 total; 51 feasible; hypervolume 4318 (n/a).

**LLM decision:** `widen` — The feasible front is squeezed into a small corner of both objectives: accuracy_bits only 10.8..13.8 against an HV reference of 10, and luts_plus_ffs only 272..621 against an HV reference of 1500. The explored boxes were clearly too tight (iterative feasible data_width 14..18 / n_iter 13..19; unrolled_k 16..17 / 12..20), so the high-accuracy end of the curve is unexplored. Because the top-accuracy design's rectangle is ~880 wide in area (621..1500), each extra accuracy bit there is worth far more hypervolume than shaving a few LUTs off the 272-area corner, so the priority is to extend the front upward in accuracy while still covering the low-area corner (data_width 14, n_iter 13 stay inside the widened box). I deliberately do not spend budget on pipelined: pipelined_m (which is pipelined with fewer register stages, hence strictly cheaper in FFs for the same unrolled datapath) already bottoms out at 835 luts_plus_ffs for 12.86 bits, dominated by iterative's 344 luts_plus_ffs at 12.8 bits, and the 1 MSPS throughput constraint is already met 10x over by iterative (10.8 MSPS), so the 1-result/cycle families cannot reach the front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 4318 (gain this round: n/a (first round)).
Feasible designs: 51 of 100 evaluations (42 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 49% violate; best seen 6.97e-05 (2^-13.81)

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=272, accuracy_bits=10.8, luts=175, ffs=97, throughput_msps=10.8, max_abs_err=0.000569 (2^-10.78), power_index=0.184
- iterative [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=299, accuracy_bits=12, luts=193, ffs=106, throughput_msps=11.7, max_abs_err=0.000251 (2^-11.96), power_index=0.191
- iterative [data_width=15 n_iter=16 angle_guard=3 frac_guard=4 rounding=trunc] luts_plus_ffs=304, accuracy_bits=12.2, luts=203, ffs=102, throughput_msps=10.2, max_abs_err=0.000219 (2^-12.16), power_index=0.218
- iterative [data_width=16 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=333, accuracy_bits=12.2, luts=232, ffs=101, throughput_msps=10.4, max_abs_err=0.000214 (2^-12.19), power_index=0.238
- iterative [data_width=15 n_iter=16 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=344, accuracy_bits=12.8, luts=242, ffs=102, throughput_msps=10.2, max_abs_err=0.000143 (2^-12.77), power_index=0.246
- iterative [data_width=17 n_iter=19 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=381, accuracy_bits=13.1, luts=274, ffs=107, throughput_msps=7.23, max_abs_err=0.000112 (2^-13.13), power_index=0.315
- unrolled_k [data_width=17 n_iter=19 angle_guard=3 frac_guard=1 rounding=round k=4] luts_plus_ffs=621, accuracy_bits=13.4, luts=516, ffs=105, throughput_msps=6.63, max_abs_err=9.28e-05 (2^-13.40), power_index=0.187
- unrolled_k [data_width=17 n_iter=19 angle_guard=3 frac_guard=3 rounding=trunc k=4] luts_plus_ffs=621, accuracy_bits=13.8, luts=512, ffs=109, throughput_msps=6.63, max_abs_err=6.97e-05 (2^-13.81), power_index=0.187
Front coverage: luts_plus_ffs 272..621 (HV reference 1500); accuracy_bits 10.8..13.8 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 65 evals, 30 feasible; max throughput seen 18.5 MSPS; best accuracy 13.13 bits; best feasible luts_plus_ffs=272; feasible ranges: data_width 14..18, n_iter 13..19, angle_guard -1..4, frac_guard 0..4
- unrolled_k: 20 evals, 12 feasible; max throughput seen 15.3 MSPS; best accuracy 13.81 bits; best feasible luts_plus_ffs=404; feasible ranges: data_width 16..17, n_iter 12..20, angle_guard -1..3, frac_guard 0..4, k 3..4
- pipelined_m: 15 evals, 9 feasible; max throughput seen 171 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=835; feasible ranges: data_width 13..18, n_iter 12..20, angle_guard -2..4, frac_guard 1..4, m 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Widen iterative and unrolled_k in data_width/n_iter to extend the front toward higher accuracy (the dominant HV direction) while keeping the low-area corner reachable; skip the pipelined families, which are dominated by the pipelined_m evidence.*)
- `iterative` (60 evals): data_width=14..22, n_iter=13..26, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Iterative owns the whole current front (272..381 area, up to 13.13 bits) and is the most area-efficient family per accuracy bit; widening data_width/n_iter lets it extend the high-accuracy end while data_width=14/n_iter=13 keeps the min-area corner (selection rule) in play.
- `unrolled_k` (40 evals): data_width=16..22, n_iter=14..26, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..6. *Why:* unrolled_k holds the current accuracy extreme (13.81 bits at 621 area) but was only sampled at data_width 16..17 / n_iter 12..20; widening should push it toward the 1500-area reference point and add the most hypervolume.

**Result (code):** 100 evaluations this round, 200 total; 146 feasible; hypervolume 9152 (+112.0%).

**LLM decision:** `map_front` — The front is well developed at the low-area end but stops far short of the HV reference on the area axis: luts_plus_ffs spans 272..737 against a reference of 1500, while accuracy_bits already spans 10.8..18.2 against a reference of 10. The single top point (unrolled_k, 737, 18.2 bits) contributes ~6256 of the 9152 HV (~68%), because its rectangle stretches all the way to area 1500; every other segment is small. So the largest remaining HV lever is extending the high-accuracy/high-area end of the front, not shaving the low end (a new point at ~240 area/10.5 bits would add only ~16 HV). Accuracy is exact and depends only on data_width/n_iter/angle_guard/frac_guard/rounding, and the registry allows data_width up to 28 and n_iter up to 30, so points well above 18.2 bits are reachable; the current front simply has not sampled them. Constraints are not the issue (0% throughput violations, best 171 MSPS; best error 2^-18.2 vs the 2^-10 limit), so this is a coverage problem, not an infeasibility. pipelined is not worth adding: it registers every micro-rotation, so for identical accuracy (identical data_width/n_iter/guards/rounding) it has strictly more FFs than iterative/unrolled_k and is Pareto-dominated — consistent with pipelined_m already being dominated (835 area for only 12.86 bits vs iterative's 299 area for 12 bits). Therefore let code run NSGA-II over the full ranges of the two families actually on the front (iterative, unrolled_k), seeded with the current front, to fill the 464..737 gap and push the high-accuracy end toward the 1500-area reference.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 9152 (gain this round: +112.0%).
Feasible designs: 146 of 200 evaluations (129 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 27% violate; best seen 3.33e-06 (2^-18.20)

Pareto front (feasible, 18 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=272, accuracy_bits=10.8, luts=175, ffs=97, throughput_msps=10.8, max_abs_err=0.000569 (2^-10.78), power_index=0.184
- iterative [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=299, accuracy_bits=12, luts=193, ffs=106, throughput_msps=11.7, max_abs_err=0.000251 (2^-11.96), power_index=0.191
- iterative [data_width=19 n_iter=15 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=321, accuracy_bits=13.2, luts=208, ffs=113, throughput_msps=10.8, max_abs_err=0.000109 (2^-13.17), power_index=0.217
- iterative [data_width=20 n_iter=16 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=366, accuracy_bits=14.7, luts=242, ffs=124, throughput_msps=9.97, max_abs_err=3.8e-05 (2^-14.68), power_index=0.262
- iterative [data_width=21 n_iter=25 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=387, accuracy_bits=15.1, luts=265, ffs=122, throughput_msps=5.68, max_abs_err=2.83e-05 (2^-15.11), power_index=0.407
- iterative [data_width=20 n_iter=25 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=393, accuracy_bits=15.3, luts=270, ffs=123, throughput_msps=5.57, max_abs_err=2.53e-05 (2^-15.27), power_index=0.414
- iterative [data_width=20 n_iter=22 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=408, accuracy_bits=16.1, luts=284, ffs=124, throughput_msps=6.24, max_abs_err=1.42e-05 (2^-16.10), power_index=0.384
- iterative [data_width=20 n_iter=25 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=427, accuracy_bits=16.6, luts=301, ffs=126, throughput_msps=5.57, max_abs_err=1e-05 (2^-16.61), power_index=0.45
- iterative [data_width=20 n_iter=22 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=464, accuracy_bits=17, luts=340, ffs=124, throughput_msps=6.24, max_abs_err=7.75e-06 (2^-16.98), power_index=0.436
- unrolled_k [data_width=22 n_iter=20 angle_guard=3 frac_guard=2 rounding=round k=3] luts_plus_ffs=737, accuracy_bits=18.2, luts=605, ffs=132, throughput_msps=6.83, max_abs_err=3.33e-06 (2^-18.20), power_index=0.277
Front coverage: luts_plus_ffs 272..737 (HV reference 1500); accuracy_bits 10.8..18.2 (HV reference 10); data_width on the front 15..22 (registry 8..28).

Per family:
- iterative: 125 evals, 85 feasible; max throughput seen 18.5 MSPS; best accuracy 17.70 bits; best feasible luts_plus_ffs=272; feasible ranges: data_width 14..22, n_iter 13..26, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 60 evals, 52 feasible; max throughput seen 15.3 MSPS; best accuracy 18.20 bits; best feasible luts_plus_ffs=404; feasible ranges: data_width 16..22, n_iter 12..26, angle_guard -2..3, frac_guard 0..4, k 2..6
- pipelined_m: 15 evals, 9 feasible; max throughput seen 171 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=835; feasible ranges: data_width 13..18, n_iter 12..20, angle_guard -2..4, frac_guard 1..4, m 2..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (35 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (17 front designs; box front_anchored)
- `unrolled_k` (5 evals): data_width=21..28, n_iter=18..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 240 total; 186 feasible; hypervolume 1.469e+04 (+60.6%).

**LLM decision:** `map_front` — The feasible front is entirely `iterative` (all 21 designs). The other explored families are dominated on both objectives: `unrolled_k` best feasible area is 404 and `pipelined_m` best is 835, whereas `iterative` already reaches 272 at 10.8 bits and 687 at 24.1 bits — strictly better area at equal-or-higher accuracy. `pipelined` would be dominated too: for identical (data_width, n_iter, angle_guard, frac_guard, rounding) it computes the same bits as `iterative` but registers every micro-rotation, so it can only add FFs/area; and since the throughput constraint (>=1 MSPS) is already met with huge margin by `iterative` (10.8 MSPS at the min-area corner, up to 18.5 MSPS seen), it cannot enter a (min luts_plus_ffs, max accuracy_bits) front. So `add_family` buys nothing. The front also covers only part of the achievable range: data_width 15..27 of the registry's 8..28, accuracy 10.8..24.1 bits, and luts_plus_ffs tops out at 687 against an HV reference of 1500 — the remaining hypervolume is in extending the high-accuracy end (data_width 28, n_iter up to 30), not in the already-tight min-area corner (272, sitting just above the 2^-10 accuracy constraint). With 160 evals left in the final round, spend them mapping the full `iterative` front (NSGA-II seeded with the current front) rather than refining a corner that is already at the constraint boundary.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 1.469e+04 (gain this round: +60.6%).
Feasible designs: 186 of 240 evaluations (166 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 22% violate; best seen 5.51e-08 (2^-24.11)

Pareto front (feasible, 21 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=272, accuracy_bits=10.8, luts=175, ffs=97, throughput_msps=10.8, max_abs_err=0.000569 (2^-10.78), power_index=0.184
- iterative [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=299, accuracy_bits=12, luts=193, ffs=106, throughput_msps=11.7, max_abs_err=0.000251 (2^-11.96), power_index=0.191
- iterative [data_width=19 n_iter=15 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=321, accuracy_bits=13.2, luts=208, ffs=113, throughput_msps=10.8, max_abs_err=0.000109 (2^-13.17), power_index=0.217
- iterative [data_width=21 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=375, accuracy_bits=14.8, luts=248, ffs=126, throughput_msps=9.97, max_abs_err=3.61e-05 (2^-14.76), power_index=0.268
- iterative [data_width=21 n_iter=25 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=387, accuracy_bits=15.1, luts=265, ffs=122, throughput_msps=5.68, max_abs_err=2.83e-05 (2^-15.11), power_index=0.407
- iterative [data_width=20 n_iter=23 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=402, accuracy_bits=15.8, luts=280, ffs=122, throughput_msps=6.11, max_abs_err=1.79e-05 (2^-15.77), power_index=0.393
- iterative [data_width=20 n_iter=23 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=423, accuracy_bits=16.4, luts=298, ffs=125, throughput_msps=6, max_abs_err=1.16e-05 (2^-16.40), power_index=0.414
- iterative [data_width=24 n_iter=20 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=451, accuracy_bits=18, luts=312, ffs=139, throughput_msps=6.78, max_abs_err=3.91e-06 (2^-17.96), power_index=0.39
- iterative [data_width=27 n_iter=29 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=547, accuracy_bits=21.5, luts=395, ffs=152, throughput_msps=4.79, max_abs_err=3.4e-07 (2^-21.49), power_index=0.659
- iterative [data_width=27 n_iter=27 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=687, accuracy_bits=24.1, luts=523, ffs=163, throughput_msps=5.02, max_abs_err=5.51e-08 (2^-24.11), power_index=0.775
Front coverage: luts_plus_ffs 272..687 (HV reference 1500); accuracy_bits 10.8..24.1 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 160 evals, 120 feasible; max throughput seen 18.5 MSPS; best accuracy 24.11 bits; best feasible luts_plus_ffs=272; feasible ranges: data_width 14..27, n_iter 11..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 65 evals, 57 feasible; max throughput seen 15.3 MSPS; best accuracy 19.80 bits; best feasible luts_plus_ffs=404; feasible ranges: data_width 16..27, n_iter 12..26, angle_guard -2..4, frac_guard 0..4, k 2..8
- pipelined_m: 15 evals, 9 feasible; max throughput seen 171 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=835; feasible ranges: data_width 13..18, n_iter 12..20, angle_guard -2..4, frac_guard 1..4, m 2..8
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (21 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 340 total; 280 feasible; hypervolume 1.494e+04 (+1.7%).

**LLM decision:** `stop` — Final round: constraints are comfortably satisfiable, so `infeasible` is ruled out — 280/340 evaluations are feasible, 0% violate the throughput_msps >= 1 constraint (best seen 171 MSPS), and the max_abs_err <= 0.000976562 constraint is met with large margin (best seen 5.51e-08 = 2^-24.11, and even the smallest-area front point at luts_plus_ffs=272 achieves 2^-10.78). The Pareto front is well populated (32 feasible designs, 252 unique) and spans both objectives broadly: luts_plus_ffs 272..687 against the HV reference 1500, and accuracy_bits 10.8..24.1 against the HV reference 10, with data_width 15..28 covering most of the registry's 8..28. Hypervolume is 1.494e+04 with only +1.7% gain this round, indicating the front has essentially converged. The selection rule (min luts_plus_ffs) is already served by the front's low-area corner: iterative [data_width=15 n_iter=15 angle_guard=4 frac_guard=1 rounding=trunc] at luts_plus_ffs=272, accuracy_bits=10.8, throughput 10.8 MSPS — meeting both constraints with margin. The unexplored `pipelined` family is a throughput-oriented variant (1 result/cycle) whose area would be far above the 272-point corner and is irrelevant to a min-area selection rule, so adding it cannot improve the selected design. Stopping now preserves the remaining 60 evaluations rather than spending them on a converged front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 60 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 340 of 400.
Hypervolume of the feasible front: 1.494e+04 (gain this round: +1.7%).
Feasible designs: 280 of 340 evaluations (252 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 18% violate; best seen 5.51e-08 (2^-24.11)

Pareto front (feasible, 32 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=272, accuracy_bits=10.8, luts=175, ffs=97, throughput_msps=10.8, max_abs_err=0.000569 (2^-10.78), power_index=0.184
- iterative [data_width=15 n_iter=16 angle_guard=3 frac_guard=4 rounding=trunc] luts_plus_ffs=304, accuracy_bits=12.2, luts=203, ffs=102, throughput_msps=10.2, max_abs_err=0.000219 (2^-12.16), power_index=0.218
- iterative [data_width=19 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=323, accuracy_bits=13.7, luts=212, ffs=111, throughput_msps=10.2, max_abs_err=7.72e-05 (2^-13.66), power_index=0.231
- iterative [data_width=20 n_iter=18 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=373, accuracy_bits=14.8, luts=256, ffs=117, throughput_msps=7.57, max_abs_err=3.54e-05 (2^-14.79), power_index=0.295
- iterative [data_width=20 n_iter=22 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=408, accuracy_bits=16.1, luts=284, ffs=124, throughput_msps=6.24, max_abs_err=1.42e-05 (2^-16.10), power_index=0.384
- iterative [data_width=22 n_iter=23 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=445, accuracy_bits=16.9, luts=313, ffs=131, throughput_msps=6, max_abs_err=8.24e-06 (2^-16.89), power_index=0.435
- iterative [data_width=26 n_iter=23 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=523, accuracy_bits=20.9, luts=371, ffs=151, throughput_msps=5.89, max_abs_err=5.25e-07 (2^-20.86), power_index=0.511
- iterative [data_width=28 n_iter=23 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=561, accuracy_bits=21.6, luts=402, ffs=158, throughput_msps=5.89, max_abs_err=3.24e-07 (2^-21.56), power_index=0.548
- iterative [data_width=28 n_iter=29 angle_guard=1 frac_guard=3 rounding=trunc] luts_plus_ffs=621, accuracy_bits=23.6, luts=457, ffs=164, throughput_msps=4.7, max_abs_err=8.09e-08 (2^-23.56), power_index=0.748
- iterative [data_width=27 n_iter=27 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=687, accuracy_bits=24.1, luts=523, ffs=163, throughput_msps=5.02, max_abs_err=5.51e-08 (2^-24.11), power_index=0.775
Front coverage: luts_plus_ffs 272..687 (HV reference 1500); accuracy_bits 10.8..24.1 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 260 evals, 214 feasible; max throughput seen 18.5 MSPS; best accuracy 24.11 bits; best feasible luts_plus_ffs=272; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 65 evals, 57 feasible; max throughput seen 15.3 MSPS; best accuracy 19.80 bits; best feasible luts_plus_ffs=404; feasible ranges: data_width 16..27, n_iter 12..26, angle_guard -2..4, frac_guard 0..4, k 2..8
- pipelined_m: 15 evals, 9 feasible; max throughput seen 171 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=835; feasible ranges: data_width 13..18, n_iter 12..20, angle_guard -2..4, frac_guard 1..4, m 2..8
```
</details>

### Round 5

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 60 evaluations*)
- `iterative` (60 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (32 front designs; box front_anchored)

**Result (code):** 60 evaluations this round, 400 total; 339 feasible; hypervolume 1.499e+04 (+0.3%).

**No LLM call** (code's front-mapping round): Final round: constraints are comfortably satisfiable, so `infeasible` is ruled out — 280/340 evaluations are feasible, 0% violate the throughput_msps >= 1 constraint (best seen 171 MSPS), and the max_abs_err <= 0.000976562 constraint is met with large margin (best seen 5.51e-08 = 2^-24.11, and even the smallest-area front point at luts_plus_ffs=272 achieves 2^-10.78). The Pareto front is well populated (32 feasible designs, 252 unique) and spans both objectives broadly: luts_plus_ffs 272..687 against the HV reference 1500, and accuracy_bits 10.8..24.1 against the HV reference 10, with data_width 15..28 covering most of the registry's 8..28. Hypervolume is 1.494e+04 with only +1.7% gain this round, indicating the front has essentially converged. The selection rule (min luts_plus_ffs) is already served by the front's low-area corner: iterative [data_width=15 n_iter=15 angle_guard=4 frac_guard=1 rounding=trunc] at luts_plus_ffs=272, accuracy_bits=10.8, throughput 10.8 MSPS — meeting both constraints with margin. The unexplored `pipelined` family is a throughput-oriented variant (1 result/cycle) whose area would be far above the 272-point corner and is irrelevant to a min-area selection rule, so adding it cannot improve the selected design. Stopping now preserves the remaining 60 evaluations rather than spending them on a converged front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 5 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.499e+04 (gain this round: +0.3%).
Feasible designs: 339 of 400 evaluations (308 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 15% violate; best seen 5.51e-08 (2^-24.11)

Pareto front (feasible, 40 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=272, accuracy_bits=10.8, luts=175, ffs=97, throughput_msps=10.8, max_abs_err=0.000569 (2^-10.78), power_index=0.184
- iterative [data_width=17 n_iter=16 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=306, accuracy_bits=12.2, luts=201, ffs=105, throughput_msps=10.2, max_abs_err=0.000207 (2^-12.24), power_index=0.218
- iterative [data_width=19 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=323, accuracy_bits=13.7, luts=212, ffs=111, throughput_msps=10.2, max_abs_err=7.72e-05 (2^-13.66), power_index=0.231
- iterative [data_width=20 n_iter=18 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=373, accuracy_bits=14.8, luts=256, ffs=117, throughput_msps=7.57, max_abs_err=3.54e-05 (2^-14.79), power_index=0.295
- iterative [data_width=21 n_iter=23 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=400, accuracy_bits=15.8, luts=278, ffs=122, throughput_msps=6.11, max_abs_err=1.79e-05 (2^-15.77), power_index=0.391
- iterative [data_width=23 n_iter=21 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=445, accuracy_bits=17.8, luts=313, ffs=132, throughput_msps=6.5, max_abs_err=4.39e-06 (2^-17.80), power_index=0.402
- iterative [data_width=24 n_iter=26 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=496, accuracy_bits=18.8, luts=354, ffs=141, throughput_msps=5.38, max_abs_err=2.2e-06 (2^-18.79), power_index=0.541
- iterative [data_width=26 n_iter=26 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=532, accuracy_bits=21.4, luts=380, ffs=151, throughput_msps=5.28, max_abs_err=3.6e-07 (2^-21.40), power_index=0.58
- iterative [data_width=28 n_iter=29 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=580, accuracy_bits=22.9, luts=420, ffs=160, throughput_msps=4.79, max_abs_err=1.27e-07 (2^-22.90), power_index=0.698
- iterative [data_width=27 n_iter=27 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=687, accuracy_bits=24.1, luts=523, ffs=163, throughput_msps=5.02, max_abs_err=5.51e-08 (2^-24.11), power_index=0.775
Front coverage: luts_plus_ffs 272..687 (HV reference 1500); accuracy_bits 10.8..24.1 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 320 evals, 273 feasible; max throughput seen 18.5 MSPS; best accuracy 24.11 bits; best feasible luts_plus_ffs=272; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 65 evals, 57 feasible; max throughput seen 15.3 MSPS; best accuracy 19.80 bits; best feasible luts_plus_ffs=404; feasible ranges: data_width 16..27, n_iter 12..26, angle_guard -2..4, frac_guard 0..4, k 2..8
- pipelined_m: 15 evals, 9 feasible; max throughput seen 171 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=835; feasible ranges: data_width 13..18, n_iter 12..20, angle_guard -2..4, frac_guard 1..4, m 2..8
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 13930 in, 26107 out
- provider-reported cost: $0.0181
- full prompts and replies: `llm_trace.jsonl`

