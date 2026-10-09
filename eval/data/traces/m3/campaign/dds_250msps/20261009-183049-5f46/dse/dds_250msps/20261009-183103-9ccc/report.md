# DSE run: dds_250msps

**Verdict:** converged: hypervolume gain fell below epsilon.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 3 round(s).  
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

## Pareto front (29 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 920 | 953 | 264.5 | 17 | 17.6 | 0.000109 (2^-13.17) | 13.17 |
| 1 | `pipelined:data_width=17,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 971 | 963 | 264.5 | 17 | 18.2 | 0.000108 (2^-13.18) | 13.18 |
| 2 | `pipelined:data_width=20,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 979 | 1014 | 264.5 | 17 | 18.7 | 8.24e-05 (2^-13.57) | 13.57 |
| 3 | `pipelined:data_width=18,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 1033 | 1057 | 264.5 | 18 | 19.7 | 8.08e-05 (2^-13.60) | 13.60 |
| 4 | `pipelined:data_width=17,n_iter=16,angle_guard=3,frac_guard=2,rounding=round` | 1053 | 1043 | 264.5 | 18 | 19.7 | 6.9e-05 (2^-13.82) | 13.82 |
| 5 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 1055 | 1047 | 264.5 | 18 | 19.8 | 6.45e-05 (2^-13.92) | 13.92 |
| 6 | `pipelined:data_width=19,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc` | 1064 | 1094 | 264.5 | 18 | 20.3 | 6.35e-05 (2^-13.94) | 13.94 |
| 7 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 1086 | 1076 | 264.5 | 18 | 20.3 | 5.46e-05 (2^-14.16) | 14.16 |
| 8 | `pipelined:data_width=19,n_iter=16,angle_guard=1,frac_guard=1,rounding=round` | 1089 | 1080 | 264.5 | 18 | 20.4 | 5.25e-05 (2^-14.22) | 14.22 |
| 9 | `pipelined:data_width=19,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 1096 | 1122 | 264.5 | 18 | 20.9 | 4.81e-05 (2^-14.34) | 14.34 |
| 10 | `pipelined:data_width=19,n_iter=16,angle_guard=3,frac_guard=2,rounding=trunc` | 1112 | 1138 | 264.5 | 18 | 21.2 | 4.67e-05 (2^-14.39) | 14.39 |
| 11 | `pipelined:data_width=20,n_iter=17,angle_guard=0,frac_guard=0,rounding=round` | 1118 | 1149 | 264.5 | 19 | 21.3 | 4.25e-05 (2^-14.52) | 14.52 |
| 12 | `pipelined:data_width=21,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 1175 | 1203 | 256.5 | 18 | 22.4 | 3.61e-05 (2^-14.76) | 14.76 |
| 13 | `pipelined:data_width=23,n_iter=16,angle_guard=-1,frac_guard=1,rounding=trunc` | 1207 | 1239 | 256.5 | 18 | 23 | 3.42e-05 (2^-14.84) | 14.84 |
| 14 | `pipelined:data_width=21,n_iter=18,angle_guard=-1,frac_guard=0,rounding=round` | 1223 | 1253 | 264.5 | 20 | 23.3 | 3.13e-05 (2^-14.97) | 14.97 |
| 15 | `pipelined:data_width=21,n_iter=18,angle_guard=0,frac_guard=0,rounding=round` | 1241 | 1271 | 264.5 | 20 | 23.6 | 2.12e-05 (2^-15.53) | 15.53 |
| 16 | `pipelined:data_width=23,n_iter=17,angle_guard=-1,frac_guard=0,rounding=trunc` | 1253 | 1286 | 256.5 | 19 | 23.9 | 2.1e-05 (2^-15.54) | 15.54 |
| 17 | `pipelined:data_width=21,n_iter=18,angle_guard=2,frac_guard=0,rounding=round` | 1277 | 1308 | 256.5 | 20 | 24.3 | 1.59e-05 (2^-15.94) | 15.94 |
| 18 | `pipelined:data_width=21,n_iter=18,angle_guard=1,frac_guard=2,rounding=trunc` | 1331 | 1354 | 256.5 | 20 | 25.2 | 1.43e-05 (2^-16.10) | 16.10 |
| 19 | `pipelined:data_width=21,n_iter=18,angle_guard=2,frac_guard=1,rounding=round` | 1357 | 1342 | 256.5 | 20 | 25.4 | 1.24e-05 (2^-16.30) | 16.30 |
| 20 | `pipelined:data_width=24,n_iter=18,angle_guard=-1,frac_guard=0,rounding=round` | 1385 | 1417 | 256.5 | 20 | 26.3 | 9.47e-06 (2^-16.69) | 16.69 |
| 21 | `pipelined:data_width=23,n_iter=19,angle_guard=0,frac_guard=0,rounding=trunc` | 1428 | 1457 | 256.5 | 21 | 27.1 | 8.46e-06 (2^-16.85) | 16.85 |
| 22 | `pipelined:data_width=23,n_iter=19,angle_guard=0,frac_guard=1,rounding=round` | 1514 | 1493 | 256.5 | 21 | 28.3 | 6.39e-06 (2^-17.25) | 17.25 |
| 23 | `pipelined:data_width=22,n_iter=20,angle_guard=2,frac_guard=1,rounding=trunc` | 1527 | 1550 | 256.5 | 22 | 28.9 | 6.11e-06 (2^-17.32) | 17.32 |
| 24 | `pipelined:data_width=22,n_iter=22,angle_guard=3,frac_guard=1,rounding=round` | 1756 | 1729 | 256.5 | 24 | 32.8 | 3.28e-06 (2^-18.22) | 18.22 |
| 25 | `pipelined:data_width=22,n_iter=23,angle_guard=2,frac_guard=3,rounding=round` | 1906 | 1870 | 256.5 | 25 | 35.5 | 2.28e-06 (2^-18.74) | 18.74 |
| 26 | `pipelined:data_width=24,n_iter=25,angle_guard=2,frac_guard=1,rounding=trunc` | 2079 | 2089 | 256.5 | 27 | 39.2 | 1.76e-06 (2^-19.11) | 19.11 |
| 27 | `pipelined:data_width=24,n_iter=26,angle_guard=2,frac_guard=0,rounding=round` | 2113 | 2125 | 256.5 | 28 | 39.8 | 1.57e-06 (2^-19.28) | 19.28 |
| 28 | `pipelined:data_width=24,n_iter=26,angle_guard=2,frac_guard=1,rounding=round` | 2216 | 2175 | 256.5 | 28 | 41.3 | 1.08e-06 (2^-19.82) | 19.82 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands one sample per clock at >=250 MSPS, which rules out iterative and unrolled_k (they emit one result every several cycles and cannot plausibly hit 250 MSPS). I therefore restrict the search to the two 1-result/cycle families, pipelined and pipelined_m. Accuracy is a hard floor (max_abs_err <= 2^-13) and depends only on data_width, n_iter, angle_guard, frac_guard and rounding, so I bracket those tightly around the 13-bit requirement (W=14..20, N=13..18, small guards) to avoid oversizing while still letting the optimizer find the cheapest point that clears the floor. The single objective is min LUTs with a secondary max accuracy_bits, so the interesting trade-off is LUTs vs accuracy_bits: pipelined gives the base curve, and pipelined_m adds an FF/latency/Fmax dimension that can lower area or raise Fmax at equal accuracy. I split the budget roughly evenly between the two families so the Pareto front is mapped across both the accuracy axis and the area/latency axis, maximising hypervolume against the reference point (4000 LUTs, 13 accuracy bits).*)
- `pipelined` (50 evals): data_width=14..20, n_iter=13..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* One result/cycle is required for >=250 MSPS; pipelined is the cleanest 1-sample/clock family. Accuracy depends only on (W, N, guards, rounding), so I bracket the 13-bit floor: W=14..20 and N=13..18 with small guards, letting the optimizer find the cheapest (W,N) that clears 2^-13 while minimising LUTs. This is the primary LUT-vs-accuracy trade-off curve.
- `pipelined_m` (50 evals): data_width=14..20, n_iter=13..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* Same 1-result/cycle throughput as pipelined but registers only every m stages, so it can trade latency for fewer FFs and a shorter critical path (higher Fmax). Since accuracy is identical to pipelined for the same (W,N,guards), this family can reach the same accuracy at lower area/clock cost. Searching m=2..8 exposes the area-vs-latency/Fmax trade-off that pipelined cannot.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 28 feasible; hypervolume 6809 (n/a).

**LLM decision:** `refine` — The `pipelined` family is the only one meeting the throughput constraint (264-273 MSPS vs 250 MSPS required), while `pipelined_m` failed (max 171 MSPS). The current Pareto front is tight (1005-1281 LUTs) and covers the accuracy requirement (13-15.4 bits vs 13 bits required). To maximize hypervolume and find the absolute minimum LUT design, I need to explore the lower bound of the feasible region more aggressively. The current best is 1005 LUTs at 13.03 bits. I will narrow the search to `pipelined` only, focusing on `data_width` 16-18, `n_iter` 14-16, and `angle_guard` 0-2 to see if we can push LUTs below 1005 while maintaining >= 13 bits accuracy and >= 250 MSPS throughput. `iterative` and `unrolled_k` are excluded because their throughput (1 result per N cycles) will be far below 250 MSPS for N>=14.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 6809 (gain this round: n/a (first round)).
Feasible designs: 28 of 100 evaluations (16 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 50% violate; best seen 273
- max_abs_err <= 0.00012207: 41% violate; best seen 1.51e-05 (2^-16.01)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=17 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] luts=1005, accuracy_bits=13, ffs=999, throughput_msps=264, max_abs_err=0.00012 (2^-13.03), power_index=18.8
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=round] luts=1023, accuracy_bits=13, ffs=1015, throughput_msps=264, max_abs_err=0.00012 (2^-13.03), power_index=19.2
- pipelined [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts=1037, accuracy_bits=13.5, ffs=1027, throughput_msps=264, max_abs_err=8.59e-05 (2^-13.51), power_index=19.4
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts=1039, accuracy_bits=13.5, ffs=1031, throughput_msps=264, max_abs_err=8.41e-05 (2^-13.54), power_index=19.5
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] luts=1055, accuracy_bits=13.9, ffs=1047, throughput_msps=264, max_abs_err=6.45e-05 (2^-13.92), power_index=19.8
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts=1089, accuracy_bits=14.2, ffs=1080, throughput_msps=264, max_abs_err=5.25e-05 (2^-14.22), power_index=20.4
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts=1096, accuracy_bits=14.3, ffs=1122, throughput_msps=264, max_abs_err=4.81e-05 (2^-14.34), power_index=20.9
- pipelined [data_width=19 n_iter=18 angle_guard=1 frac_guard=1 rounding=round] luts=1228, accuracy_bits=14.7, ffs=1215, throughput_msps=264, max_abs_err=3.87e-05 (2^-14.66), power_index=23
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=1 rounding=round] luts=1246, accuracy_bits=15, ffs=1233, throughput_msps=264, max_abs_err=3.09e-05 (2^-14.98), power_index=23.3
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] luts=1281, accuracy_bits=15.4, ffs=1265, throughput_msps=264, max_abs_err=2.34e-05 (2^-15.38), power_index=23.9
Front coverage: luts 1005..1281 (HV reference 4000); accuracy_bits 13..15.4 (HV reference 13); data_width on the front 17..19 (registry 8..28).

Per family:
- pipelined: 50 evals, 28 feasible; max throughput seen 273 MSPS; best accuracy 15.38 bits; best feasible luts=1005; feasible ranges: data_width 17..19, n_iter 16..18, angle_guard 0..2, frac_guard 1..2
- pipelined_m: 50 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 16.01 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Refine the search space to the most promising region of the only feasible family to maximize hypervolume gain in the remaining budget.*)
- `pipelined` (100 evals): data_width=16..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Focus on the only feasible family. Narrow ranges to the promising region identified in Round 1 (data_width 17-19, n_iter 16-18) but extend slightly lower (data_width 16, n_iter 14) to probe for lower LUT counts. Exclude pipelined_m (failed throughput) and iterative/unrolled_k (will fail throughput).

**Result (code):** 100 evaluations this round, 200 total; 58 feasible; hypervolume 6836 (+0.4%).

**LLM decision:** `add_family` — The current front is dominated by the `pipelined` family, which is constrained by a high area cost (971-1281 LUTs) and a throughput ceiling of ~264-273 MSPS. The `pipelined_m` family failed to meet the throughput constraint (max 171 MSPS) because its reduced register density likely pushed the Fmax below the 250 MHz requirement. However, the `iterative` and `unrolled_k` families have not been explored. These families use a shared datapath, which typically results in significantly lower LUT counts (potentially well below the 971 LUT minimum currently seen). Although they have lower throughput (1 result per N or N/k cycles), if their Fmax is high enough (e.g., > 1.5 GHz for iterative with N=6), they could satisfy the 250 MSPS constraint while offering a much better area-accuracy trade-off. Exploring these families is essential to map the full Pareto front, especially the low-LUT region.
- **rule applied by code:** 'add_family' overridden to stop: HV gain 0.39% < epsilon 1.00%
- **rule applied by code:** code: before stopping (converged), one front-mapping round with the remaining 200 evaluations
- effective decision: `stop`

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 6836 (gain this round: +0.4%).
Feasible designs: 58 of 200 evaluations (26 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 25% violate; best seen 273
- max_abs_err <= 0.00012207: 56% violate; best seen 1.51e-05 (2^-16.01)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] luts=971, accuracy_bits=13.2, ffs=963, throughput_msps=264, max_abs_err=0.000108 (2^-13.18), power_index=18.2
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] luts=979, accuracy_bits=13.4, ffs=1006, throughput_msps=264, max_abs_err=9.49e-05 (2^-13.36), power_index=18.7
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] luts=1017, accuracy_bits=13.5, ffs=1045, throughput_msps=264, max_abs_err=8.82e-05 (2^-13.47), power_index=19.4
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts=1033, accuracy_bits=13.6, ffs=1057, throughput_msps=264, max_abs_err=8.08e-05 (2^-13.60), power_index=19.7
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] luts=1055, accuracy_bits=13.9, ffs=1047, throughput_msps=264, max_abs_err=6.45e-05 (2^-13.92), power_index=19.8
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts=1086, accuracy_bits=14.2, ffs=1076, throughput_msps=264, max_abs_err=5.46e-05 (2^-14.16), power_index=20.3
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts=1089, accuracy_bits=14.2, ffs=1080, throughput_msps=264, max_abs_err=5.25e-05 (2^-14.22), power_index=20.4
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts=1096, accuracy_bits=14.3, ffs=1122, throughput_msps=264, max_abs_err=4.81e-05 (2^-14.34), power_index=20.9
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=1 rounding=round] luts=1246, accuracy_bits=15, ffs=1233, throughput_msps=264, max_abs_err=3.09e-05 (2^-14.98), power_index=23.3
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] luts=1281, accuracy_bits=15.4, ffs=1265, throughput_msps=264, max_abs_err=2.34e-05 (2^-15.38), power_index=23.9
Front coverage: luts 971..1281 (HV reference 4000); accuracy_bits 13.2..15.4 (HV reference 13); data_width on the front 17..19 (registry 8..28).

Per family:
- pipelined: 150 evals, 58 feasible; max throughput seen 273 MSPS; best accuracy 15.38 bits; best feasible luts=971; feasible ranges: data_width 17..19, n_iter 15..18, angle_guard 0..2, frac_guard 1..2
- pipelined_m: 50 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 16.01 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 200 evaluations*)
- `pipelined` (200 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (13 front designs; box front_anchored)

**Result (code):** 200 evaluations this round, 400 total; 189 feasible; hypervolume 1.71e+04 (+150.1%).

**No LLM call** (code's front-mapping round): The current front is dominated by the `pipelined` family, which is constrained by a high area cost (971-1281 LUTs) and a throughput ceiling of ~264-273 MSPS. The `pipelined_m` family failed to meet the throughput constraint (max 171 MSPS) because its reduced register density likely pushed the Fmax below the 250 MHz requirement. However, the `iterative` and `unrolled_k` families have not been explored. These families use a shared datapath, which typically results in significantly lower LUT counts (potentially well below the 971 LUT minimum currently seen). Although they have lower throughput (1 result per N or N/k cycles), if their Fmax is high enough (e.g., > 1.5 GHz for iterative with N=6), they could satisfy the 250 MSPS constraint while offering a much better area-accuracy trade-off. Exploring these families is essential to map the full Pareto front, especially the low-LUT region.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.71e+04 (gain this round: +150.1%).
Feasible designs: 189 of 400 evaluations (139 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 24% violate; best seen 273
- max_abs_err <= 0.00012207: 34% violate; best seen 1.13e-07 (2^-23.08)

Pareto front (feasible, 29 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] luts=920, accuracy_bits=13.2, ffs=953, throughput_msps=264, max_abs_err=0.000109 (2^-13.17), power_index=17.6
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts=1033, accuracy_bits=13.6, ffs=1057, throughput_msps=264, max_abs_err=8.08e-05 (2^-13.60), power_index=19.7
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] luts=1064, accuracy_bits=13.9, ffs=1094, throughput_msps=264, max_abs_err=6.35e-05 (2^-13.94), power_index=20.3
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts=1096, accuracy_bits=14.3, ffs=1122, throughput_msps=264, max_abs_err=4.81e-05 (2^-14.34), power_index=20.9
- pipelined [data_width=21 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts=1175, accuracy_bits=14.8, ffs=1203, throughput_msps=257, max_abs_err=3.61e-05 (2^-14.76), power_index=22.4
- pipelined [data_width=23 n_iter=17 angle_guard=-1 frac_guard=0 rounding=trunc] luts=1253, accuracy_bits=15.5, ffs=1286, throughput_msps=257, max_abs_err=2.1e-05 (2^-15.54), power_index=23.9
- pipelined [data_width=21 n_iter=18 angle_guard=2 frac_guard=1 rounding=round] luts=1357, accuracy_bits=16.3, ffs=1342, throughput_msps=257, max_abs_err=1.24e-05 (2^-16.30), power_index=25.4
- pipelined [data_width=23 n_iter=19 angle_guard=0 frac_guard=1 rounding=round] luts=1514, accuracy_bits=17.3, ffs=1493, throughput_msps=257, max_abs_err=6.39e-06 (2^-17.25), power_index=28.3
- pipelined [data_width=22 n_iter=23 angle_guard=2 frac_guard=3 rounding=round] luts=1906, accuracy_bits=18.7, ffs=1870, throughput_msps=257, max_abs_err=2.28e-06 (2^-18.74), power_index=35.5
- pipelined [data_width=24 n_iter=26 angle_guard=2 frac_guard=1 rounding=round] luts=2216, accuracy_bits=19.8, ffs=2175, throughput_msps=257, max_abs_err=1.08e-06 (2^-19.82), power_index=41.3
Front coverage: luts 920..2216 (HV reference 4000); accuracy_bits 13.2..19.8 (HV reference 13); data_width on the front 17..24 (registry 8..28).

Per family:
- pipelined: 350 evals, 189 feasible; max throughput seen 273 MSPS; best accuracy 23.08 bits; best feasible luts=920; feasible ranges: data_width 17..25, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 50 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 16.01 bits
```
</details>

## LLM usage
- calls: 6 (failed/unparsed attempts: 0)
- tokens: 21701 in, 2866 out
- provider-reported cost: $0.0080
- full prompts and replies: `llm_trace.jsonl`

