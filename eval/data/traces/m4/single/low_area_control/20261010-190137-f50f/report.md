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
`iterative:data_width=14,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 170 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 92 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 11.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 85.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.167 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000716 (2^-10.45) | exact: bit-accurate model, exhaustive (16384 angles) |
| max_abs_err_lsb | 2.93 | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err | 0.000185 (2^-12.40) | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err_lsb | 0.759 | exact: bit-accurate model, exhaustive (16384 angles) |
| accuracy_bits | 10.4 | exact: bit-accurate model, exhaustive (16384 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 17 cycles, a new input every 17 cycle(s). DDS tone from its exact outputs: SFDR 77.3 dBc, SNR 72.0 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (34 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=14,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` | 170 | 92 | 11.7 | 17 | 0.167 | 0.000716 (2^-10.45) | 10.45 |
| 1 | `iterative:data_width=14,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 170 | 92 | 10.4 | 19 | 0.187 | 0.000716 (2^-10.45) | 10.45 |
| 2 | `iterative:data_width=14,n_iter=16,angle_guard=3,frac_guard=2,rounding=trunc` | 172 | 93 | 10.4 | 19 | 0.189 | 0.000659 (2^-10.57) | 10.57 |
| 3 | `iterative:data_width=15,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc` | 172 | 95 | 10.4 | 19 | 0.191 | 0.000567 (2^-10.78) | 10.78 |
| 4 | `iterative:data_width=15,n_iter=15,angle_guard=4,frac_guard=0,rounding=round` | 173 | 95 | 10.8 | 18 | 0.182 | 0.000548 (2^-10.83) | 10.83 |
| 5 | `iterative:data_width=16,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 179 | 97 | 10.4 | 19 | 0.197 | 0.000301 (2^-11.70) | 11.70 |
| 6 | `iterative:data_width=15,n_iter=15,angle_guard=3,frac_guard=3,rounding=trunc` | 193 | 100 | 11.0 | 18 | 0.198 | 0.000289 (2^-11.76) | 11.76 |
| 7 | `iterative:data_width=15,n_iter=16,angle_guard=4,frac_guard=3,rounding=trunc` | 195 | 101 | 10.2 | 19 | 0.211 | 0.000228 (2^-12.10) | 12.10 |
| 8 | `iterative:data_width=17,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc` | 193 | 104 | 11.0 | 18 | 0.201 | 0.000219 (2^-12.16) | 12.16 |
| 9 | `iterative:data_width=17,n_iter=15,angle_guard=2,frac_guard=1,rounding=trunc` | 195 | 105 | 10.8 | 18 | 0.203 | 0.000174 (2^-12.49) | 12.49 |
| 10 | `iterative:data_width=17,n_iter=15,angle_guard=3,frac_guard=1,rounding=trunc` | 197 | 106 | 10.8 | 18 | 0.205 | 0.000173 (2^-12.49) | 12.49 |
| 11 | `iterative:data_width=17,n_iter=16,angle_guard=3,frac_guard=2,rounding=trunc` | 206 | 108 | 10.2 | 19 | 0.225 | 0.000102 (2^-13.26) | 13.26 |
| 12 | `iterative:data_width=17,n_iter=18,angle_guard=3,frac_guard=2,rounding=trunc` | 230 | 109 | 7.6 | 21 | 0.268 | 9.91e-05 (2^-13.30) | 13.30 |
| 13 | `iterative:data_width=18,n_iter=16,angle_guard=3,frac_guard=3,rounding=trunc` | 227 | 115 | 10.2 | 19 | 0.245 | 5.44e-05 (2^-14.17) | 14.17 |
| 14 | `iterative:data_width=18,n_iter=16,angle_guard=3,frac_guard=4,rounding=trunc` | 237 | 117 | 10.2 | 19 | 0.253 | 5.33e-05 (2^-14.20) | 14.20 |
| 15 | `iterative:data_width=19,n_iter=30,angle_guard=1,frac_guard=0,rounding=round` | 248 | 113 | 4.8 | 33 | 0.448 | 4.26e-05 (2^-14.52) | 14.52 |
| 16 | `iterative:data_width=18,n_iter=23,angle_guard=3,frac_guard=3,rounding=trunc` | 265 | 116 | 6.1 | 26 | 0.372 | 3.81e-05 (2^-14.68) | 14.68 |
| 17 | `iterative:data_width=19,n_iter=25,angle_guard=3,frac_guard=2,rounding=trunc` | 266 | 119 | 5.7 | 28 | 0.406 | 3.21e-05 (2^-14.93) | 14.93 |
| 18 | `iterative:data_width=18,n_iter=25,angle_guard=3,frac_guard=4,rounding=trunc` | 280 | 118 | 5.7 | 28 | 0.419 | 2.94e-05 (2^-15.05) | 15.05 |
| 19 | `iterative:data_width=20,n_iter=29,angle_guard=2,frac_guard=2,rounding=trunc` | 282 | 123 | 5.0 | 32 | 0.488 | 2.13e-05 (2^-15.52) | 15.52 |
| 20 | `iterative:data_width=22,n_iter=20,angle_guard=3,frac_guard=0,rounding=trunc` | 281 | 130 | 6.8 | 23 | 0.356 | 1.22e-05 (2^-16.32) | 16.32 |
| 21 | `iterative:data_width=21,n_iter=20,angle_guard=1,frac_guard=2,rounding=trunc` | 290 | 127 | 6.8 | 23 | 0.361 | 9.95e-06 (2^-16.62) | 16.62 |
| 22 | `iterative:data_width=21,n_iter=20,angle_guard=3,frac_guard=2,rounding=trunc` | 294 | 129 | 6.8 | 23 | 0.366 | 7.58e-06 (2^-17.01) | 17.01 |
| 23 | `iterative:data_width=22,n_iter=24,angle_guard=2,frac_guard=0,rounding=round` | 299 | 129 | 5.8 | 27 | 0.435 | 5.49e-06 (2^-17.47) | 17.47 |
| 24 | `iterative:data_width=21,n_iter=20,angle_guard=4,frac_guard=4,rounding=trunc` | 324 | 134 | 6.8 | 23 | 0.396 | 4.41e-06 (2^-17.79) | 17.79 |
| 25 | `iterative:data_width=24,n_iter=20,angle_guard=3,frac_guard=1,rounding=trunc` | 328 | 142 | 6.7 | 23 | 0.406 | 2.96e-06 (2^-18.37) | 18.37 |
| 26 | `iterative:data_width=25,n_iter=23,angle_guard=2,frac_guard=0,rounding=trunc` | 338 | 144 | 5.9 | 26 | 0.472 | 1.45e-06 (2^-19.40) | 19.40 |
| 27 | `iterative:data_width=25,n_iter=23,angle_guard=2,frac_guard=0,rounding=round` | 352 | 144 | 5.9 | 26 | 0.485 | 8.71e-07 (2^-20.13) | 20.13 |
| 28 | `iterative:data_width=26,n_iter=22,angle_guard=1,frac_guard=1,rounding=trunc` | 369 | 150 | 6.1 | 25 | 0.489 | 7.83e-07 (2^-20.28) | 20.28 |
| 29 | `iterative:data_width=25,n_iter=29,angle_guard=3,frac_guard=2,rounding=trunc` | 380 | 149 | 4.8 | 32 | 0.638 | 4.7e-07 (2^-21.02) | 21.02 |
| 30 | `iterative:data_width=28,n_iter=25,angle_guard=3,frac_guard=0,rounding=trunc` | 401 | 160 | 5.4 | 28 | 0.592 | 2.19e-07 (2^-22.13) | 22.13 |
| 31 | `iterative:data_width=26,n_iter=27,angle_guard=3,frac_guard=3,rounding=trunc` | 415 | 156 | 5.1 | 30 | 0.645 | 1.7e-07 (2^-22.49) | 22.49 |
| 32 | `iterative:data_width=28,n_iter=26,angle_guard=2,frac_guard=0,rounding=round` | 415 | 159 | 5.3 | 29 | 0.626 | 1.17e-07 (2^-23.03) | 23.03 |
| 33 | `iterative:data_width=28,n_iter=27,angle_guard=3,frac_guard=4,rounding=trunc` | 470 | 168 | 5.0 | 30 | 0.721 | 4.23e-08 (2^-24.49) | 24.49 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The throughput floor (>=1 MSPS) is essentially non-binding: even the slowest schedule here (iterative, N+3 cycles/result) needs only Fmax/(N+3) >= 1, i.e. ~30 MHz at N=30, which every family clears by a wide margin. So the binding constraint is accuracy (max_abs_err <= 2^-10, i.e. accuracy_bits >= 10) and the real objective is area (luts_plus_ffs). Accuracy depends only on (data_width, n_iter, angle_guard, frac_guard, rounding) and is identical across families, so the front is decided purely by which family gives the least area for a given accuracy point. iterative reuses ONE datapath (one adder set + barrel shifters + FSM) so its area is nearly flat in N, whereas unrolled_k/pipelined_m replicate the datapath N times (fixed shifts, but N adder sets) and pipelined_m adds ceil(N/m) register stages. I therefore expect iterative to own the low-area corner and most of the front, and I weight it accordingly, while spending enough on pipelined_m (large m) and unrolled_k to confirm they never undercut iterative at any accuracy level and to fill the front. Ranges bracket the accuracy threshold: output LSB is 2^-(W-2) so W>=12 is needed for 2^-10, and residual angle error ~2^-N needs N~10-12, so W in 10..18 and N in 6..20 straddle the feasible boundary without wasting budget far below it. angle_guard and frac_guard are searched over their full registry ranges because they trade area for error cheaply and could shift the min-area feasible point.*)
- `iterative` (55 evals): data_width=10..18, n_iter=6..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Primary bet: single shared datapath with barrel shifters, area nearly independent of N, so it should give the smallest luts_plus_ffs at every accuracy level and own the min-area corner the selection rule picks. Wide W/N ranges bracket the 2^-10 threshold so the search can find the cheapest feasible point and the accuracy/area trade-off above it.
- `pipelined_m` (25 evals): data_width=10..18, n_iter=6..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=4..8. *Why:* Closest competitor to iterative on area: large m keeps the number of register stages (ceil(N/m)) small while the combinational micro-rotations use cheap fixed shifts. Included to test whether it can beat iterative at any accuracy point and to cover the front; m restricted to 4..8 to stay in the low-area regime.
- `unrolled_k` (20 evals): data_width=10..18, n_iter=6..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* k chained micro-rotations/cycle with a shared FSM: area grows with k, so it is unlikely to win the min-area corner, but small k (2..3) may be competitive at high accuracy and it helps confirm the front is iterative-dominated. Small share to avoid over-spending on a likely-dominated family.

**Result (code):** 100 evaluations this round, 100 total; 45 feasible; hypervolume 4439 (n/a).

**LLM decision:** `map_front` — Round 1's feasible front is entirely `iterative` and covers only luts_plus_ffs 262..391 against the HV reference of 1500, with accuracy_bits 10.4..13.7 — so the high-accuracy/high-area half of the trade-off curve is completely unmapped and hypervolume is capped. Throughput is non-binding (best seen 97.8 MSPS vs the >=1 MSPS constraint, and iterative alone already reaches 10-22 MSPS), and the other explored families are area-dominated for the same accuracy (unrolled_k best 526, pipelined_m best 917 vs iterative 262), so the front is purely an iterative area-vs-accuracy curve. The low-area corner is already found (data_width=14 is the smallest feasible width; the 55% error violations confirm smaller widths fail the 2^-10 constraint), so the remaining HV gain is in extending accuracy upward. Hand this round to a code-driven NSGA-II coverage search over the full iterative ranges (data_width 8..28, n_iter 4..30, angle_guard -2..4, frac_guard 0..4, both roundings), seeded with the current front, to map the whole curve toward the reference point.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 4439 (gain this round: n/a (first round)).
Feasible designs: 45 of 100 evaluations (38 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 97.8
- max_abs_err <= 0.000976562: 55% violate; best seen 7.53e-05 (2^-13.70)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=262, accuracy_bits=10.4, luts=170, ffs=92, throughput_msps=11.7, max_abs_err=0.000716 (2^-10.45), power_index=0.167
- iterative [data_width=14 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=262, accuracy_bits=10.4, luts=170, ffs=92, throughput_msps=10.4, max_abs_err=0.000716 (2^-10.45), power_index=0.187
- iterative [data_width=14 n_iter=16 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=265, accuracy_bits=10.6, luts=172, ffs=93, throughput_msps=10.4, max_abs_err=0.000659 (2^-10.57), power_index=0.189
- iterative [data_width=16 n_iter=16 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=269, accuracy_bits=10.6, luts=172, ffs=97, throughput_msps=10.4, max_abs_err=0.000643 (2^-10.60), power_index=0.192
- iterative [data_width=16 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.7, luts=179, ffs=97, throughput_msps=10.4, max_abs_err=0.000301 (2^-11.70), power_index=0.197
- iterative [data_width=17 n_iter=15 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=300, accuracy_bits=12.5, luts=195, ffs=105, throughput_msps=10.8, max_abs_err=0.000174 (2^-12.49), power_index=0.203
- iterative [data_width=17 n_iter=16 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=314, accuracy_bits=13.3, luts=206, ffs=108, throughput_msps=10.2, max_abs_err=0.000102 (2^-13.26), power_index=0.225
- iterative [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=370, accuracy_bits=13.4, luts=259, ffs=111, throughput_msps=10.8, max_abs_err=9.56e-05 (2^-13.35), power_index=0.251
- iterative [data_width=18 n_iter=15 angle_guard=2 frac_guard=3 rounding=round] luts_plus_ffs=385, accuracy_bits=13.6, luts=271, ffs=114, throughput_msps=10.8, max_abs_err=8.08e-05 (2^-13.60), power_index=0.261
- iterative [data_width=18 n_iter=15 angle_guard=4 frac_guard=3 rounding=round] luts_plus_ffs=391, accuracy_bits=13.7, luts=275, ffs=116, throughput_msps=10.8, max_abs_err=7.53e-05 (2^-13.70), power_index=0.264
Front coverage: luts_plus_ffs 262..391 (HV reference 1500); accuracy_bits 10.4..13.7 (HV reference 10); data_width on the front 14..18 (registry 8..28).

Per family:
- iterative: 55 evals, 32 feasible; max throughput seen 22.6 MSPS; best accuracy 13.70 bits; best feasible luts_plus_ffs=262; feasible ranges: data_width 14..18, n_iter 14..18, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 20 evals, 3 feasible; max throughput seen 8.42 MSPS; best accuracy 10.48 bits; best feasible luts_plus_ffs=526; feasible ranges: data_width 16..17, n_iter 16..18, angle_guard -2..-1, frac_guard 0..1, k 5..8
- pipelined_m: 25 evals, 10 feasible; max throughput seen 97.8 MSPS; best accuracy 11.56 bits; best feasible luts_plus_ffs=917; feasible ranges: data_width 13..16, n_iter 13..17, angle_guard -1..4, frac_guard 0..4, m 4..7
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=13..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (11 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 139 feasible; hypervolume 1.356e+04 (+205.4%).

**LLM decision:** `refine` — The whole 28-design front is iterative, and its low-area corner (262 LUT+FF at data_width=14, accuracy 10.4 bits) sits right on the 2^-10 accuracy constraint, so the selection rule's winner is accuracy-limited and may be beaten by a narrower datapath (W=12/13 give half-LSB 2^-11/2^-12, still under 2^-10) if enough iterations are used — the reported feasible data_width range 14..28 suggests W<=13 was simply under-explored, not impossible. At the other end the front stops at 658 LUT+FF / 22.6 bits, far short of the 1500 HV reference, so pushing data_width toward 28 with high n_iter should extend the curve and raise hypervolume. pipelined is the only unexplored family; a small probe checks whether it can place any point the iterative family cannot (expected dominated, since it registers every stage).

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.356e+04 (gain this round: +205.4%).
Feasible designs: 139 of 200 evaluations (120 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 97.8
- max_abs_err <= 0.000976562: 30% violate; best seen 1.59e-07 (2^-22.58)

Pareto front (feasible, 28 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=262, accuracy_bits=10.4, luts=170, ffs=92, throughput_msps=11.7, max_abs_err=0.000716 (2^-10.45), power_index=0.167
- iterative [data_width=16 n_iter=16 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=269, accuracy_bits=10.6, luts=172, ffs=97, throughput_msps=10.4, max_abs_err=0.000643 (2^-10.60), power_index=0.192
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=297, accuracy_bits=12.2, luts=193, ffs=104, throughput_msps=11, max_abs_err=0.000219 (2^-12.16), power_index=0.201
- iterative [data_width=17 n_iter=16 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=314, accuracy_bits=13.3, luts=206, ffs=108, throughput_msps=10.2, max_abs_err=0.000102 (2^-13.26), power_index=0.225
- iterative [data_width=17 n_iter=22 angle_guard=4 frac_guard=3 rounding=trunc] luts_plus_ffs=361, accuracy_bits=13.8, luts=249, ffs=112, throughput_msps=6.36, max_abs_err=6.86e-05 (2^-13.83), power_index=0.339
- iterative [data_width=22 n_iter=20 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=412, accuracy_bits=16.3, luts=281, ffs=130, throughput_msps=6.78, max_abs_err=1.22e-05 (2^-16.32), power_index=0.356
- iterative [data_width=22 n_iter=24 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=428, accuracy_bits=17.5, luts=299, ffs=129, throughput_msps=5.78, max_abs_err=5.49e-06 (2^-17.47), power_index=0.435
- iterative [data_width=24 n_iter=29 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=496, accuracy_bits=18.6, luts=354, ffs=141, throughput_msps=4.88, max_abs_err=2.44e-06 (2^-18.64), power_index=0.597
- iterative [data_width=26 n_iter=22 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=520, accuracy_bits=20.3, luts=369, ffs=150, throughput_msps=6.13, max_abs_err=7.83e-07 (2^-20.28), power_index=0.489
- iterative [data_width=26 n_iter=27 angle_guard=2 frac_guard=4 rounding=round] luts_plus_ffs=658, accuracy_bits=22.6, luts=500, ffs=157, throughput_msps=5.11, max_abs_err=1.59e-07 (2^-22.58), power_index=0.742
Front coverage: luts_plus_ffs 262..658 (HV reference 1500); accuracy_bits 10.4..22.6 (HV reference 10); data_width on the front 14..26 (registry 8..28).

Per family:
- iterative: 155 evals, 126 feasible; max throughput seen 22.6 MSPS; best accuracy 22.58 bits; best feasible luts_plus_ffs=262; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 20 evals, 3 feasible; max throughput seen 8.42 MSPS; best accuracy 10.48 bits; best feasible luts_plus_ffs=526; feasible ranges: data_width 16..17, n_iter 16..18, angle_guard -2..-1, frac_guard 0..1, k 5..8
- pipelined_m: 25 evals, 10 feasible; max throughput seen 97.8 MSPS; best accuracy 11.56 bits; best feasible luts_plus_ffs=917; feasible ranges: data_width 13..16, n_iter 13..17, angle_guard -1..4, frac_guard 0..4, m 4..7
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Refine the accuracy-limited low-area corner and extend the high-accuracy end of the iterative front, with a small probe of the unexplored pipelined family.*)
- `iterative` (77 evals): data_width=12..15, n_iter=12..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Nail the min-luts_plus_ffs corner the selection rule picks: test whether W=12/13 with sufficient n_iter can still meet 2^-10 and undercut the current 262 LUT+FF.
- `pipelined` (23 evals): data_width=12..16, n_iter=12..18, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Only unexplored family; cheap probe of its low-area region to confirm it is dominated for the min-area objective.
- clamped by code: dropped duplicate family iterative

**Result (code):** 100 evaluations this round, 300 total; 196 feasible; hypervolume 1.356e+04 (+0.0%).

**LLM decision:** `map_front` — Round 3 gave +0.0% hypervolume gain and the feasible front is now entirely `iterative` (30 designs, luts_plus_ffs 262..658, accuracy_bits 10.4..22.6). The other families are strictly dominated for this spec: accuracy depends only on data_width/n_iter/angle_guard/frac_guard/rounding (identical bits across families), so pipelined (best 1437), pipelined_m (best 917) and unrolled_k (best 526) can never beat iterative's 262 on the min-area objective, and their higher throughput is irrelevant since the constraint is only >=1 MSPS (iterative already reaches 11.7 MSPS at the selected point). The front is converged (no gain) but does not yet span the full accuracy range the registry permits: max accuracy on the front is 22.6 bits at data_width=26, while data_width up to 28 and n_iter up to 30 are allowed, so higher-accuracy/higher-area points are likely still unmapped and would add hypervolume against the accuracy reference of 10. With 100 evals left and one round, this is exactly the reserved end-of-run front-mapping step: run NSGA-II over the full ranges of the family on the front (iterative), seeded with the current front, to fill out the area/accuracy trade-off curve.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.356e+04 (gain this round: +0.0%).
Feasible designs: 196 of 300 evaluations (165 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 35% violate; best seen 1.59e-07 (2^-22.58)

Pareto front (feasible, 30 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=262, accuracy_bits=10.4, luts=170, ffs=92, throughput_msps=11.7, max_abs_err=0.000716 (2^-10.45), power_index=0.167
- iterative [data_width=15 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=267, accuracy_bits=10.8, luts=172, ffs=95, throughput_msps=10.4, max_abs_err=0.000567 (2^-10.78), power_index=0.191
- iterative [data_width=15 n_iter=15 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=293, accuracy_bits=11.8, luts=193, ffs=100, throughput_msps=11, max_abs_err=0.000289 (2^-11.76), power_index=0.198
- iterative [data_width=17 n_iter=15 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=302, accuracy_bits=12.5, luts=197, ffs=106, throughput_msps=10.8, max_abs_err=0.000173 (2^-12.49), power_index=0.205
- iterative [data_width=17 n_iter=25 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=358, accuracy_bits=13.6, luts=247, ffs=111, throughput_msps=5.68, max_abs_err=8.1e-05 (2^-13.59), power_index=0.377
- iterative [data_width=19 n_iter=25 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=385, accuracy_bits=14.9, luts=266, ffs=119, throughput_msps=5.68, max_abs_err=3.21e-05 (2^-14.93), power_index=0.406
- iterative [data_width=21 n_iter=20 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=423, accuracy_bits=17, luts=294, ffs=129, throughput_msps=6.78, max_abs_err=7.58e-06 (2^-17.01), power_index=0.366
- iterative [data_width=24 n_iter=29 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=496, accuracy_bits=18.6, luts=354, ffs=141, throughput_msps=4.88, max_abs_err=2.44e-06 (2^-18.64), power_index=0.597
- iterative [data_width=26 n_iter=22 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=520, accuracy_bits=20.3, luts=369, ffs=150, throughput_msps=6.13, max_abs_err=7.83e-07 (2^-20.28), power_index=0.489
- iterative [data_width=26 n_iter=27 angle_guard=2 frac_guard=4 rounding=round] luts_plus_ffs=658, accuracy_bits=22.6, luts=500, ffs=157, throughput_msps=5.11, max_abs_err=1.59e-07 (2^-22.58), power_index=0.742
Front coverage: luts_plus_ffs 262..658 (HV reference 1500); accuracy_bits 10.4..22.6 (HV reference 10); data_width on the front 14..26 (registry 8..28).

Per family:
- iterative: 232 evals, 173 feasible; max throughput seen 22.6 MSPS; best accuracy 22.58 bits; best feasible luts_plus_ffs=262; feasible ranges: data_width 13..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 20 evals, 3 feasible; max throughput seen 8.42 MSPS; best accuracy 10.48 bits; best feasible luts_plus_ffs=526; feasible ranges: data_width 16..17, n_iter 16..18, angle_guard -2..-1, frac_guard 0..1, k 5..8
- pipelined: 23 evals, 10 feasible; max throughput seen 282 MSPS; best accuracy 12.60 bits; best feasible luts_plus_ffs=1437; feasible ranges: data_width 13..16, n_iter 12..18, angle_guard 0..4, frac_guard 0..4
- pipelined_m: 25 evals, 10 feasible; max throughput seen 97.8 MSPS; best accuracy 11.56 bits; best feasible luts_plus_ffs=917; feasible ranges: data_width 13..16, n_iter 13..17, angle_guard -1..4, frac_guard 0..4, m 4..7
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=13..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (30 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 290 feasible; hypervolume 1.533e+04 (+13.1%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), and the front is feasible and well covered: 290 feasible designs, 34 on the Pareto front, with the constraint throughput_msps >= 1 met by every evaluation (best 282 MSPS; the front's cheapest point runs 11.7 MSPS) and max_abs_err <= 2^-10 met by all front points (cheapest point 2^-10.45, best 2^-24.49). The front spans luts_plus_ffs 262..639 against the HV reference 1500 and accuracy_bits 10.4..24.5 against reference 10, i.e. it already covers essentially the whole achievable trade-off range, and hypervolume still improved +13.1% this round, so further exploration is not needed. The selection rule (min luts_plus_ffs) is satisfied by iterative [data_width=14 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] at 262 LUTs+FFs, 10.4 accuracy bits, 11.7 MSPS, 0.167 power index — comfortably inside both constraints. No constraint is unreachable, so infeasible does not apply.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.533e+04 (gain this round: +13.1%).
Feasible designs: 290 of 400 evaluations (251 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 28% violate; best seen 4.23e-08 (2^-24.49)

Pareto front (feasible, 34 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=262, accuracy_bits=10.4, luts=170, ffs=92, throughput_msps=11.7, max_abs_err=0.000716 (2^-10.45), power_index=0.167
- iterative [data_width=15 n_iter=15 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=268, accuracy_bits=10.8, luts=173, ffs=95, throughput_msps=10.8, max_abs_err=0.000548 (2^-10.83), power_index=0.182
- iterative [data_width=15 n_iter=16 angle_guard=4 frac_guard=3 rounding=trunc] luts_plus_ffs=296, accuracy_bits=12.1, luts=195, ffs=101, throughput_msps=10.2, max_abs_err=0.000228 (2^-12.10), power_index=0.211
- iterative [data_width=17 n_iter=16 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=314, accuracy_bits=13.3, luts=206, ffs=108, throughput_msps=10.2, max_abs_err=0.000102 (2^-13.26), power_index=0.225
- iterative [data_width=19 n_iter=30 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=361, accuracy_bits=14.5, luts=248, ffs=113, throughput_msps=4.82, max_abs_err=4.26e-05 (2^-14.52), power_index=0.448
- iterative [data_width=18 n_iter=25 angle_guard=3 frac_guard=4 rounding=trunc] luts_plus_ffs=398, accuracy_bits=15.1, luts=280, ffs=118, throughput_msps=5.68, max_abs_err=2.94e-05 (2^-15.05), power_index=0.419
- iterative [data_width=21 n_iter=20 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=423, accuracy_bits=17, luts=294, ffs=129, throughput_msps=6.78, max_abs_err=7.58e-06 (2^-17.01), power_index=0.366
- iterative [data_width=25 n_iter=23 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=482, accuracy_bits=19.4, luts=338, ffs=144, throughput_msps=5.89, max_abs_err=1.45e-06 (2^-19.40), power_index=0.472
- iterative [data_width=25 n_iter=29 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=530, accuracy_bits=21, luts=380, ffs=149, throughput_msps=4.79, max_abs_err=4.7e-07 (2^-21.02), power_index=0.638
- iterative [data_width=28 n_iter=27 angle_guard=3 frac_guard=4 rounding=trunc] luts_plus_ffs=639, accuracy_bits=24.5, luts=470, ffs=168, throughput_msps=5.02, max_abs_err=4.23e-08 (2^-24.49), power_index=0.721
Front coverage: luts_plus_ffs 262..639 (HV reference 1500); accuracy_bits 10.4..24.5 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 332 evals, 267 feasible; max throughput seen 22.6 MSPS; best accuracy 24.49 bits; best feasible luts_plus_ffs=262; feasible ranges: data_width 13..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 20 evals, 3 feasible; max throughput seen 8.42 MSPS; best accuracy 10.48 bits; best feasible luts_plus_ffs=526; feasible ranges: data_width 16..17, n_iter 16..18, angle_guard -2..-1, frac_guard 0..1, k 5..8
- pipelined: 23 evals, 10 feasible; max throughput seen 282 MSPS; best accuracy 12.60 bits; best feasible luts_plus_ffs=1437; feasible ranges: data_width 13..16, n_iter 12..18, angle_guard 0..4, frac_guard 0..4
- pipelined_m: 25 evals, 10 feasible; max throughput seen 97.8 MSPS; best accuracy 11.56 bits; best feasible luts_plus_ffs=917; feasible ranges: data_width 13..16, n_iter 13..17, angle_guard -1..4, frac_guard 0..4, m 4..7
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 16076 in, 14981 out
- provider-reported cost: $0.0109
- full prompts and replies: `llm_trace.jsonl`

