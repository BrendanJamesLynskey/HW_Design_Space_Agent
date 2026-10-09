# DSE run: dds_250msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 400 of 400 budgeted, over 4 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec dds_250msps: NCO / DDS sin-cos generator for a digital up-converter. One sample per clock at >= 250 MSPS, max error <= 2^-13. Minimise LUTs.
  constraint: throughput_msps >= 250
  constraint: max_abs_err <= 0.00012207
  objective: min luts (HV ref 4000)
  objective: max accuracy_bits (HV ref 13)
  select: min luts
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts)

| metric | value | provenance |
|---|---|---|
| luts | 920 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 953 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 64.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 17.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000109 (2^-13.17) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 7.12 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 3e-05 (2^-15.02) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.97 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.2 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 17 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 98.2 dBc, SNR 87.5 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (30 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 920 | 953 | 264.5 | 17 | 17.6 | 0.000109 (2^-13.17) | 13.17 |
| 1 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 985 | 1017 | 264.5 | 18 | 18.8 | 8.35e-05 (2^-13.55) | 13.55 |
| 2 | `pipelined:data_width=18,n_iter=17,angle_guard=2,frac_guard=0,rounding=round` | 1051 | 1081 | 264.5 | 19 | 20 | 7.75e-05 (2^-13.65) | 13.65 |
| 3 | `pipelined:data_width=19,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc` | 1064 | 1094 | 264.5 | 18 | 20.3 | 6.35e-05 (2^-13.94) | 13.94 |
| 4 | `pipelined:data_width=19,n_iter=16,angle_guard=3,frac_guard=1,rounding=trunc` | 1080 | 1110 | 264.5 | 18 | 20.6 | 5.64e-05 (2^-14.11) | 14.11 |
| 5 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 1086 | 1076 | 264.5 | 18 | 20.3 | 5.46e-05 (2^-14.16) | 14.16 |
| 6 | `pipelined:data_width=18,n_iter=16,angle_guard=3,frac_guard=2,rounding=round` | 1102 | 1092 | 264.5 | 18 | 20.6 | 5.17e-05 (2^-14.24) | 14.24 |
| 7 | `pipelined:data_width=19,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 1104 | 1096 | 264.5 | 18 | 20.7 | 4.95e-05 (2^-14.30) | 14.30 |
| 8 | `pipelined:data_width=19,n_iter=16,angle_guard=3,frac_guard=1,rounding=round` | 1120 | 1112 | 264.5 | 18 | 21 | 4.5e-05 (2^-14.44) | 14.44 |
| 9 | `pipelined:data_width=19,n_iter=16,angle_guard=3,frac_guard=2,rounding=round` | 1152 | 1140 | 264.5 | 18 | 21.6 | 4.29e-05 (2^-14.51) | 14.51 |
| 10 | `pipelined:data_width=19,n_iter=16,angle_guard=4,frac_guard=3,rounding=trunc` | 1159 | 1182 | 256.5 | 18 | 22 | 4.13e-05 (2^-14.56) | 14.56 |
| 11 | `pipelined:data_width=22,n_iter=16,angle_guard=3,frac_guard=1,rounding=trunc` | 1222 | 1255 | 256.5 | 18 | 23.3 | 3.3e-05 (2^-14.89) | 14.89 |
| 12 | `pipelined:data_width=20,n_iter=19,angle_guard=3,frac_guard=0,rounding=round` | 1314 | 1342 | 256.5 | 21 | 25 | 2.17e-05 (2^-15.49) | 15.49 |
| 13 | `pipelined:data_width=21,n_iter=18,angle_guard=0,frac_guard=1,rounding=round` | 1321 | 1306 | 264.5 | 20 | 24.7 | 1.88e-05 (2^-15.70) | 15.70 |
| 14 | `pipelined:data_width=23,n_iter=17,angle_guard=2,frac_guard=1,rounding=trunc` | 1337 | 1368 | 256.5 | 19 | 25.4 | 1.66e-05 (2^-15.88) | 15.88 |
| 15 | `pipelined:data_width=23,n_iter=17,angle_guard=2,frac_guard=1,rounding=round` | 1386 | 1370 | 256.5 | 19 | 25.9 | 1.61e-05 (2^-15.92) | 15.92 |
| 16 | `pipelined:data_width=20,n_iter=19,angle_guard=3,frac_guard=1,rounding=round` | 1394 | 1378 | 256.5 | 21 | 26.1 | 1.31e-05 (2^-16.22) | 16.22 |
| 17 | `pipelined:data_width=22,n_iter=18,angle_guard=1,frac_guard=3,rounding=trunc` | 1420 | 1441 | 256.5 | 20 | 26.9 | 1.04e-05 (2^-16.56) | 16.56 |
| 18 | `pipelined:data_width=21,n_iter=19,angle_guard=3,frac_guard=1,rounding=round` | 1453 | 1436 | 256.5 | 21 | 27.2 | 8.82e-06 (2^-16.79) | 16.79 |
| 19 | `pipelined:data_width=22,n_iter=19,angle_guard=1,frac_guard=2,rounding=trunc` | 1466 | 1487 | 256.5 | 21 | 27.8 | 7.45e-06 (2^-17.04) | 17.04 |
| 20 | `pipelined:data_width=22,n_iter=19,angle_guard=3,frac_guard=2,rounding=trunc` | 1504 | 1525 | 256.5 | 21 | 28.5 | 6.37e-06 (2^-17.26) | 17.26 |
| 21 | `pipelined:data_width=23,n_iter=19,angle_guard=3,frac_guard=2,rounding=trunc` | 1561 | 1583 | 256.5 | 21 | 29.6 | 4.81e-06 (2^-17.66) | 17.66 |
| 22 | `pipelined:data_width=22,n_iter=20,angle_guard=1,frac_guard=2,rounding=round` | 1593 | 1568 | 256.5 | 22 | 29.7 | 4.59e-06 (2^-17.73) | 17.73 |
| 23 | `pipelined:data_width=22,n_iter=21,angle_guard=3,frac_guard=2,rounding=trunc` | 1670 | 1687 | 256.5 | 23 | 31.6 | 3.67e-06 (2^-18.05) | 18.05 |
| 24 | `pipelined:data_width=22,n_iter=21,angle_guard=3,frac_guard=3,rounding=trunc` | 1712 | 1725 | 256.5 | 23 | 32.3 | 2.72e-06 (2^-18.49) | 18.49 |
| 25 | `pipelined:data_width=23,n_iter=20,angle_guard=2,frac_guard=3,rounding=round` | 1716 | 1685 | 256.5 | 22 | 32 | 2.65e-06 (2^-18.53) | 18.53 |
| 26 | `pipelined:data_width=22,n_iter=21,angle_guard=3,frac_guard=4,rounding=trunc` | 1754 | 1764 | 256.5 | 23 | 33.1 | 2.49e-06 (2^-18.61) | 18.61 |
| 27 | `pipelined:data_width=22,n_iter=21,angle_guard=3,frac_guard=4,rounding=round` | 1801 | 1766 | 256.5 | 23 | 33.5 | 1.95e-06 (2^-18.97) | 18.97 |
| 28 | `pipelined:data_width=22,n_iter=21,angle_guard=4,frac_guard=4,rounding=round` | 1822 | 1787 | 256.5 | 23 | 33.9 | 1.84e-06 (2^-19.05) | 19.05 |
| 29 | `pipelined:data_width=23,n_iter=28,angle_guard=3,frac_guard=1,rounding=round` | 2330 | 2286 | 256.5 | 30 | 43.4 | 1.73e-06 (2^-19.14) | 19.14 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The hard throughput floor of 250 MSPS eliminates the iterative family: it emits one result every N+3 cycles, so even its best case (small N, high Fmax) is far below 250 MSPS, and spending budget there would only confirm infeasibility. The three remaining families all reach 1 result/cycle (pipelined, pipelined_m) or a small number of cycles/result (unrolled_k), so they are the only plausible feasible set. Accuracy is family-independent (same W, N, guards, rounding), so I keep an identical accuracy box (W 12..22, N 10..20, angle_guard -1..3, frac_guard 0..3, both roundings) across all three and let the families differ only on the area/throughput axis: pipelined maximises Fmax margin at high LUT cost, pipelined_m trades Fmax for fewer FFs via m, and unrolled_k minimises LUTs via datapath sharing at the risk of missing the throughput floor. This spread should populate the whole LUT-vs-accuracy Pareto curve in round 1, and the low-W/low-N edges will reveal the cheapest designs that still satisfy max_abs_err <= 2^-13.*)
- `pipelined` (35 evals): data_width=12..22, n_iter=10..20, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* One registered micro-rotation per stage gives the highest Fmax and therefore the most throughput margin above 250 MSPS; it is the reference for the LUT-vs-accuracy front, at the cost of the most registers/LUTs. W 12..22 and N 10..20 bracket the 13-bit accuracy requirement and let the search find the smallest W/N that still meets it.
- `pipelined_m` (30 evals): data_width=12..22, n_iter=10..20, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* Still 1 result/cycle (so throughput = Fmax), but registering every m stages cuts FF count and area versus full pipelining; m trades combinational depth (Fmax) against area, which is exactly the axis the min-LUT objective cares about. Same accuracy box as pipelined so the two fronts are directly comparable.
- `unrolled_k` (35 evals): data_width=12..22, n_iter=10..20, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, k=2..8. *Why:* Shares one k-deep datapath over ceil(N/k) cycles, so it has the best chance of the lowest LUT count; the risk is Fmax, since throughput = Fmax/ceil(N/k) must still clear 250 MSPS. Sweeping k 2..8 and N 10..20 maps exactly where that throughput wall sits and whether a low-LUT feasible point exists.

**Result (code):** 100 evaluations this round, 100 total; 10 feasible; hypervolume 3824 (n/a).

**LLM decision:** `map_front` — Only the pipelined family is feasible: unrolled_k (0/35 feasible, max 8.4 MSPS) and pipelined_m (0/30 feasible, max 171 MSPS) both fall short of the 250 MSPS throughput constraint, and iterative (1 result per N+3 cycles) cannot reach 250 MSPS either, so the feasible front lives entirely in pipelined. The current front is narrow: accuracy_bits spans only 13..14.3 while the best accuracy seen anywhere is 15.0 (pipelined_m) and 14.74 (unrolled_k), and luts spans only 1005..1104 against an HV reference of 4000. That means the front covers only a small part of the accuracy objective's achievable range, so hypervolume is being left on the table. The right move is to let NSGA-II map the full pipelined ranges (data_width 8..28, n_iter 4..30, angle_guard -2..4, frac_guard 0..4, both roundings), seeded with the current 4-design front, to extend the trade-off curve toward higher accuracy_bits while keeping throughput >= 250 and max_abs_err <= 2^-13.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 3824 (gain this round: n/a (first round)).
Feasible designs: 10 of 100 evaluations (6 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 65% violate; best seen 282
- max_abs_err <= 0.00012207: 59% violate; best seen 3.04e-05 (2^-15.00)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=17 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] luts=1005, accuracy_bits=13, ffs=999, throughput_msps=264, max_abs_err=0.00012 (2^-13.03), power_index=18.8
- pipelined [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts=1037, accuracy_bits=13.5, ffs=1027, throughput_msps=264, max_abs_err=8.59e-05 (2^-13.51), power_index=19.4
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] luts=1064, accuracy_bits=13.9, ffs=1094, throughput_msps=264, max_abs_err=6.35e-05 (2^-13.94), power_index=20.3
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] luts=1104, accuracy_bits=14.3, ffs=1096, throughput_msps=264, max_abs_err=4.95e-05 (2^-14.30), power_index=20.7
Front coverage: luts 1005..1104 (HV reference 4000); accuracy_bits 13..14.3 (HV reference 13); data_width on the front 17..19 (registry 8..28).

Per family:
- unrolled_k: 35 evals, 0 feasible; max throughput seen 8.4 MSPS; best accuracy 14.74 bits
- pipelined: 35 evals, 10 feasible; max throughput seen 282 MSPS; best accuracy 14.30 bits; best feasible luts=1005; feasible ranges: data_width 17..19, n_iter 16..19, angle_guard 2..2, frac_guard 1..2
- pipelined_m: 30 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.00 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined` (100 evals): data_width=16..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (4 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 83 feasible; hypervolume 1.573e+04 (+311.4%).

**LLM decision:** `refine` — Only the pipelined family is feasible: unrolled_k tops out at 8.4 MSPS and pipelined_m at 171 MSPS, both below the 250 MSPS floor, and iterative's N+3 cycles/result cannot reach 250 MSPS at any realistic Fmax (it was not even worth spending evals on). The front is entirely pipelined, spanning luts 1005..1822 and accuracy 13..19.1 bits. The selection rule is min luts, and the current min-luts feasible design is pipelined[data_width=17 n_iter=16 angle_guard=2 frac_guard=1 round] at 1005 LUTs / 13.03 accuracy bits - it clears the 2^-13 error floor by only 0.03 bits, so the binding trade-off is exactly here. The highest-value use of this round is to probe whether smaller data_width / n_iter (and cheaper trunc rounding) can drop LUTs below 1005 while still meeting max_abs_err <= 0.00012207, rather than re-mapping the already well-covered accuracy range. Round 4 can then spend the reserved budget on map_front over the full pipelined ranges seeded with the resulting front.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.573e+04 (gain this round: +311.4%).
Feasible designs: 83 of 200 evaluations (65 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 42% violate; best seen 282
- max_abs_err <= 0.00012207: 34% violate; best seen 8.4e-08 (2^-23.51)

Pareto front (feasible, 22 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=17 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] luts=1005, accuracy_bits=13, ffs=999, throughput_msps=264, max_abs_err=0.00012 (2^-13.03), power_index=18.8
- pipelined [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts=1037, accuracy_bits=13.5, ffs=1027, throughput_msps=264, max_abs_err=8.59e-05 (2^-13.51), power_index=19.4
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] luts=1104, accuracy_bits=14.3, ffs=1096, throughput_msps=264, max_abs_err=4.95e-05 (2^-14.30), power_index=20.7
- pipelined [data_width=19 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] luts=1152, accuracy_bits=14.5, ffs=1140, throughput_msps=264, max_abs_err=4.29e-05 (2^-14.51), power_index=21.6
- pipelined [data_width=22 n_iter=16 angle_guard=3 frac_guard=1 rounding=trunc] luts=1222, accuracy_bits=14.9, ffs=1255, throughput_msps=257, max_abs_err=3.3e-05 (2^-14.89), power_index=23.3
- pipelined [data_width=21 n_iter=19 angle_guard=3 frac_guard=1 rounding=round] luts=1453, accuracy_bits=16.8, ffs=1436, throughput_msps=257, max_abs_err=8.82e-06 (2^-16.79), power_index=27.2
- pipelined [data_width=22 n_iter=19 angle_guard=3 frac_guard=2 rounding=trunc] luts=1504, accuracy_bits=17.3, ffs=1525, throughput_msps=257, max_abs_err=6.37e-06 (2^-17.26), power_index=28.5
- pipelined [data_width=22 n_iter=20 angle_guard=1 frac_guard=2 rounding=round] luts=1593, accuracy_bits=17.7, ffs=1568, throughput_msps=257, max_abs_err=4.59e-06 (2^-17.73), power_index=29.7
- pipelined [data_width=22 n_iter=21 angle_guard=3 frac_guard=4 rounding=trunc] luts=1754, accuracy_bits=18.6, ffs=1764, throughput_msps=257, max_abs_err=2.49e-06 (2^-18.61), power_index=33.1
- pipelined [data_width=22 n_iter=21 angle_guard=4 frac_guard=4 rounding=round] luts=1822, accuracy_bits=19.1, ffs=1787, throughput_msps=257, max_abs_err=1.84e-06 (2^-19.05), power_index=33.9
Front coverage: luts 1005..1822 (HV reference 4000); accuracy_bits 13..19.1 (HV reference 13); data_width on the front 17..23 (registry 8..28).

Per family:
- unrolled_k: 35 evals, 0 feasible; max throughput seen 8.4 MSPS; best accuracy 14.74 bits
- pipelined: 135 evals, 83 feasible; max throughput seen 282 MSPS; best accuracy 23.51 bits; best feasible luts=1005; feasible ranges: data_width 17..23, n_iter 16..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 30 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.00 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Only the pipelined family is feasible: unrolled_k tops out at 8.4 MSPS and pipelined_m at 171 MSPS, both below the 250 MSPS floor, and iterative's N+3 cycles/result cannot reach 250 MSPS at any realistic Fmax (it was not even worth spending evals on). The front is entirely pipelined, spanning luts 1005..1822 and accuracy 13..19.1 bits. The selection rule is min luts, and the current min-luts feasible design is pipelined[data_width=17 n_iter=16 angle_guard=2 frac_guard=1 round] at 1005 LUTs / 13.03 accuracy bits - it clears the 2^-13 error floor by only 0.03 bits, so the binding trade-off is exactly here. The highest-value use of this round is to probe whether smaller data_width / n_iter (and cheaper trunc rounding) can drop LUTs below 1005 while still meeting max_abs_err <= 0.00012207, rather than re-mapping the already well-covered accuracy range. Round 4 can then spend the reserved budget on map_front over the full pipelined ranges seeded with the resulting front.*)
- `pipelined` (100 evals): data_width=15..18, n_iter=12..20, angle_guard=0..3, frac_guard=0..2, rounding=round|trunc. *Why:* Only pipelined is feasible; selection rule is min luts, so push the low-LUT corner below 1005.

**Result (code):** 100 evaluations this round, 300 total; 124 feasible; hypervolume 1.577e+04 (+0.2%).

**LLM decision:** `map_front` — Only the pipelined family is viable: unrolled_k peaked at 8.4 MSPS and pipelined_m at 171 MSPS, both below the 250 MSPS floor, and iterative is structurally excluded (1 micro-rotation/cycle gives N+3>=7 cycles/result, so even a ~400 MHz Artix-7 clock yields well under 250 MSPS). So there is no point adding iterative or re-spending on the other two families. The feasible front is a single-family (pipelined) curve that covers only luts 920..1822 against the HV reference of 4000, and accuracy_bits only 13.2..19.1 while pipelined designs already achieve 23.51 bits; the +0.2% gain this round shows local refinement has saturated. The right use of the last 100 evals is to spread NSGA-II over the full pipelined ranges (data_width 8..28, n_iter 4..30, angle_guard -2..4, frac_guard 0..4, both roundings), seeded with the existing front, to fill in the higher-luts/higher-accuracy part of the trade-off and lift hypervolume. The min-luts corner (920 LUTs, 13.17 bits, ~264 MSPS) that the selection rule would pick is already safely inside the feasible region (max_abs_err 1.09e-4 vs 1.22e-4 limit), so it just needs to stay on the mapped front.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.577e+04 (gain this round: +0.2%).
Feasible designs: 124 of 300 evaluations (89 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 28% violate; best seen 282
- max_abs_err <= 0.00012207: 42% violate; best seen 8.4e-08 (2^-23.51)

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] luts=920, accuracy_bits=13.2, ffs=953, throughput_msps=264, max_abs_err=0.000109 (2^-13.17), power_index=17.6
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] luts=1064, accuracy_bits=13.9, ffs=1094, throughput_msps=264, max_abs_err=6.35e-05 (2^-13.94), power_index=20.3
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts=1086, accuracy_bits=14.2, ffs=1076, throughput_msps=264, max_abs_err=5.46e-05 (2^-14.16), power_index=20.3
- pipelined [data_width=19 n_iter=16 angle_guard=3 frac_guard=1 rounding=round] luts=1120, accuracy_bits=14.4, ffs=1112, throughput_msps=264, max_abs_err=4.5e-05 (2^-14.44), power_index=21
- pipelined [data_width=22 n_iter=16 angle_guard=3 frac_guard=1 rounding=trunc] luts=1222, accuracy_bits=14.9, ffs=1255, throughput_msps=257, max_abs_err=3.3e-05 (2^-14.89), power_index=23.3
- pipelined [data_width=22 n_iter=16 angle_guard=3 frac_guard=4 rounding=trunc] luts=1317, accuracy_bits=15, ffs=1340, throughput_msps=257, max_abs_err=3.14e-05 (2^-14.96), power_index=25
- pipelined [data_width=22 n_iter=19 angle_guard=1 frac_guard=2 rounding=trunc] luts=1466, accuracy_bits=17, ffs=1487, throughput_msps=257, max_abs_err=7.45e-06 (2^-17.04), power_index=27.8
- pipelined [data_width=22 n_iter=20 angle_guard=1 frac_guard=2 rounding=round] luts=1593, accuracy_bits=17.7, ffs=1568, throughput_msps=257, max_abs_err=4.59e-06 (2^-17.73), power_index=29.7
- pipelined [data_width=22 n_iter=21 angle_guard=3 frac_guard=3 rounding=trunc] luts=1712, accuracy_bits=18.5, ffs=1725, throughput_msps=257, max_abs_err=2.72e-06 (2^-18.49), power_index=32.3
- pipelined [data_width=22 n_iter=21 angle_guard=4 frac_guard=4 rounding=round] luts=1822, accuracy_bits=19.1, ffs=1787, throughput_msps=257, max_abs_err=1.84e-06 (2^-19.05), power_index=33.9
Front coverage: luts 920..1822 (HV reference 4000); accuracy_bits 13.2..19.1 (HV reference 13); data_width on the front 18..23 (registry 8..28).

Per family:
- unrolled_k: 35 evals, 0 feasible; max throughput seen 8.4 MSPS; best accuracy 14.74 bits
- pipelined: 235 evals, 124 feasible; max throughput seen 282 MSPS; best accuracy 23.51 bits; best feasible luts=920; feasible ranges: data_width 16..23, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 30 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.00 bits
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined` (100 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (25 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 190 feasible; hypervolume 1.6e+04 (+1.5%).

**LLM decision:** `stop` — Budget is exhausted (400/400 evals, round 4 of 4) and the front is feasible and well covered: 190 feasible designs (142 unique), 30 on the Pareto front spanning luts 920..2330 and accuracy_bits 13.2..19.1, with both constraints satisfied at the front's cheap end (pipelined data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round: 920 LUTs, 264 MSPS >= 250, max_abs_err 1.09e-4 <= 1.22e-4, 13.2 bits). Hypervolume gain this round was only +1.5%, so the front has essentially converged, and the min-luts selection rule already has a clear winner at 920 LUTs. The unexplored `iterative` family cannot help: it yields one result per N+3 cycles, and the only non-pipelined families measured (unrolled_k 8.4 MSPS, pipelined_m 171 MSPS) both failed the 250 MSPS constraint in every evaluation, so no unexplored family can plausibly beat the pipelined front. Nothing is infeasible — the constraints are met — so stopping is correct.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.6e+04 (gain this round: +1.5%).
Feasible designs: 190 of 400 evaluations (142 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 27% violate; best seen 282
- max_abs_err <= 0.00012207: 34% violate; best seen 4.98e-08 (2^-24.26)

Pareto front (feasible, 30 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] luts=920, accuracy_bits=13.2, ffs=953, throughput_msps=264, max_abs_err=0.000109 (2^-13.17), power_index=17.6
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] luts=1064, accuracy_bits=13.9, ffs=1094, throughput_msps=264, max_abs_err=6.35e-05 (2^-13.94), power_index=20.3
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] luts=1102, accuracy_bits=14.2, ffs=1092, throughput_msps=264, max_abs_err=5.17e-05 (2^-14.24), power_index=20.6
- pipelined [data_width=19 n_iter=16 angle_guard=4 frac_guard=3 rounding=trunc] luts=1159, accuracy_bits=14.6, ffs=1182, throughput_msps=257, max_abs_err=4.13e-05 (2^-14.56), power_index=22
- pipelined [data_width=21 n_iter=18 angle_guard=0 frac_guard=1 rounding=round] luts=1321, accuracy_bits=15.7, ffs=1306, throughput_msps=264, max_abs_err=1.88e-05 (2^-15.70), power_index=24.7
- pipelined [data_width=20 n_iter=19 angle_guard=3 frac_guard=1 rounding=round] luts=1394, accuracy_bits=16.2, ffs=1378, throughput_msps=257, max_abs_err=1.31e-05 (2^-16.22), power_index=26.1
- pipelined [data_width=22 n_iter=19 angle_guard=1 frac_guard=2 rounding=trunc] luts=1466, accuracy_bits=17, ffs=1487, throughput_msps=257, max_abs_err=7.45e-06 (2^-17.04), power_index=27.8
- pipelined [data_width=22 n_iter=21 angle_guard=3 frac_guard=2 rounding=trunc] luts=1670, accuracy_bits=18.1, ffs=1687, throughput_msps=257, max_abs_err=3.67e-06 (2^-18.05), power_index=31.6
- pipelined [data_width=22 n_iter=21 angle_guard=3 frac_guard=4 rounding=trunc] luts=1754, accuracy_bits=18.6, ffs=1764, throughput_msps=257, max_abs_err=2.49e-06 (2^-18.61), power_index=33.1
- pipelined [data_width=23 n_iter=28 angle_guard=3 frac_guard=1 rounding=round] luts=2330, accuracy_bits=19.1, ffs=2286, throughput_msps=257, max_abs_err=1.73e-06 (2^-19.14), power_index=43.4
Front coverage: luts 920..2330 (HV reference 4000); accuracy_bits 13.2..19.1 (HV reference 13); data_width on the front 18..23 (registry 8..28).

Per family:
- unrolled_k: 35 evals, 0 feasible; max throughput seen 8.4 MSPS; best accuracy 14.74 bits
- pipelined: 335 evals, 190 feasible; max throughput seen 282 MSPS; best accuracy 24.26 bits; best feasible luts=920; feasible ranges: data_width 16..23, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 30 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.00 bits
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 27100 in, 11115 out
- provider-reported cost: $0.0125
- full prompts and replies: `llm_trace.jsonl`

