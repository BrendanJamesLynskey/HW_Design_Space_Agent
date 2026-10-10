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
`pipelined:data_width=20,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts)

| metric | value | provenance |
|---|---|---|
| luts | 979 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 1014 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 64.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 18.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 8.24e-05 (2^-13.57) | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 21.6 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.58e-05 (2^-15.24) | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 6.76 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.6 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 17 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 98.2 dBc, SNR 88.8 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (26 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=20,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 979 | 1014 | 264.5 | 17 | 18.7 | 8.24e-05 (2^-13.57) | 13.57 |
| 1 | `pipelined:data_width=20,n_iter=15,angle_guard=2,frac_guard=1,rounding=trunc` | 1038 | 1070 | 264.5 | 17 | 19.8 | 7.32e-05 (2^-13.74) | 13.74 |
| 2 | `pipelined:data_width=22,n_iter=15,angle_guard=-1,frac_guard=0,rounding=round` | 1053 | 1090 | 264.5 | 17 | 20.1 | 6.93e-05 (2^-13.82) | 13.82 |
| 3 | `pipelined:data_width=20,n_iter=15,angle_guard=2,frac_guard=1,rounding=round` | 1080 | 1072 | 264.5 | 17 | 20.2 | 6.81e-05 (2^-13.84) | 13.84 |
| 4 | `pipelined:data_width=22,n_iter=15,angle_guard=2,frac_guard=0,rounding=trunc` | 1097 | 1135 | 256.5 | 17 | 21 | 6.66e-05 (2^-13.87) | 13.87 |
| 5 | `pipelined:data_width=18,n_iter=17,angle_guard=1,frac_guard=3,rounding=trunc` | 1135 | 1154 | 264.5 | 19 | 21.5 | 6.23e-05 (2^-13.97) | 13.97 |
| 6 | `pipelined:data_width=23,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc` | 1156 | 1192 | 256.5 | 17 | 22.1 | 6.22e-05 (2^-13.97) | 13.97 |
| 7 | `pipelined:data_width=19,n_iter=17,angle_guard=2,frac_guard=2,rounding=trunc` | 1169 | 1193 | 264.5 | 19 | 22.2 | 3.81e-05 (2^-14.68) | 14.68 |
| 8 | `pipelined:data_width=21,n_iter=18,angle_guard=0,frac_guard=0,rounding=trunc` | 1241 | 1271 | 264.5 | 20 | 23.6 | 2.85e-05 (2^-15.10) | 15.10 |
| 9 | `pipelined:data_width=21,n_iter=17,angle_guard=2,frac_guard=1,rounding=round` | 1280 | 1267 | 256.5 | 19 | 24 | 1.98e-05 (2^-15.62) | 15.62 |
| 10 | `pipelined:data_width=21,n_iter=18,angle_guard=1,frac_guard=1,rounding=trunc` | 1295 | 1322 | 264.5 | 20 | 24.6 | 1.73e-05 (2^-15.82) | 15.82 |
| 11 | `pipelined:data_width=25,n_iter=17,angle_guard=-2,frac_guard=0,rounding=trunc` | 1337 | 1372 | 256.5 | 19 | 25.5 | 1.68e-05 (2^-15.86) | 15.86 |
| 12 | `pipelined:data_width=21,n_iter=18,angle_guard=1,frac_guard=1,rounding=round` | 1339 | 1324 | 264.5 | 20 | 25 | 1.44e-05 (2^-16.08) | 16.08 |
| 13 | `pipelined:data_width=21,n_iter=19,angle_guard=2,frac_guard=0,rounding=round` | 1352 | 1380 | 256.5 | 21 | 25.7 | 1.21e-05 (2^-16.33) | 16.33 |
| 14 | `pipelined:data_width=22,n_iter=19,angle_guard=1,frac_guard=0,rounding=round` | 1390 | 1419 | 256.5 | 21 | 26.4 | 8.35e-06 (2^-16.87) | 16.87 |
| 15 | `pipelined:data_width=22,n_iter=19,angle_guard=2,frac_guard=1,rounding=round` | 1493 | 1474 | 256.5 | 21 | 27.9 | 6.05e-06 (2^-17.33) | 17.33 |
| 16 | `pipelined:data_width=22,n_iter=19,angle_guard=3,frac_guard=1,rounding=round` | 1512 | 1493 | 256.5 | 21 | 28.3 | 5.96e-06 (2^-17.36) | 17.36 |
| 17 | `pipelined:data_width=23,n_iter=19,angle_guard=1,frac_guard=1,rounding=round` | 1533 | 1512 | 256.5 | 21 | 28.6 | 5.75e-06 (2^-17.41) | 17.41 |
| 18 | `pipelined:data_width=22,n_iter=19,angle_guard=3,frac_guard=3,rounding=round` | 1588 | 1562 | 256.5 | 21 | 29.6 | 4.81e-06 (2^-17.67) | 17.67 |
| 19 | `pipelined:data_width=25,n_iter=19,angle_guard=1,frac_guard=1,rounding=trunc` | 1599 | 1625 | 256.5 | 21 | 30.3 | 4.24e-06 (2^-17.85) | 17.85 |
| 20 | `pipelined:data_width=25,n_iter=21,angle_guard=-1,frac_guard=0,rounding=round` | 1691 | 1716 | 256.5 | 23 | 32 | 2.56e-06 (2^-18.58) | 18.58 |
| 21 | `pipelined:data_width=23,n_iter=21,angle_guard=1,frac_guard=2,rounding=round` | 1740 | 1710 | 256.5 | 23 | 32.4 | 2.52e-06 (2^-18.60) | 18.60 |
| 22 | `pipelined:data_width=26,n_iter=21,angle_guard=-1,frac_guard=0,rounding=round` | 1754 | 1780 | 256.5 | 23 | 33.2 | 1.66e-06 (2^-19.20) | 19.20 |
| 23 | `pipelined:data_width=25,n_iter=24,angle_guard=1,frac_guard=0,rounding=round` | 1993 | 2010 | 256.5 | 26 | 37.6 | 1.05e-06 (2^-19.86) | 19.86 |
| 24 | `pipelined:data_width=25,n_iter=24,angle_guard=1,frac_guard=1,rounding=round` | 2094 | 2056 | 256.5 | 26 | 39 | 7.31e-07 (2^-20.38) | 20.38 |
| 25 | `pipelined:data_width=25,n_iter=25,angle_guard=1,frac_guard=1,rounding=round` | 2182 | 2142 | 256.5 | 27 | 40.7 | 6.42e-07 (2^-20.57) | 20.57 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires one sample per clock at >=250 MSPS. iterative and unrolled_k produce one result every N+3 or ceil(N/k)+3 cycles, so even with k=8 and small N they would need Fmax far above what an Artix-7 can deliver; they cannot meet the throughput constraint and are excluded from round 1. pipelined and pipelined_m both give 1 result/cycle, so they are the only families that can plausibly satisfy throughput_msps >= 250. Accuracy depends only on data_width, n_iter, angle_guard, frac_guard and rounding, and the constraint max_abs_err <= 2^-13 means accuracy_bits >= 13; with output LSB = 2^-(W-2) this points to W around 15-18 and N around 14-18, so the ranges are centred there but left wide enough (W 14..20, N 12..20) for the search to find the true minimum-LUT feasible point. The two families share the same arithmetic, so the first round is mainly about locating the feasible accuracy/throughput boundary and seeing whether the m-register variant offers a distinct LUT/accuracy trade-off; the reserved later rounds can then map the front over the full ranges of whichever families survive.*)
- `pipelined` (55 evals): data_width=14..20, n_iter=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Only fully pipelined families can plausibly hit 1 result/cycle at >=250 MSPS. This is the simplest such family (one register per micro-rotation), so it is the natural low-LUT candidate and should dominate the min-LUT corner of the front. Ranges start near the accuracy floor (W=14..20, N=12..20) so the search can find the smallest W/N that still satisfies max_abs_err <= 2^-13, while angle_guard/frac_guard/rounding are left open to recover accuracy cheaply.
- `pipelined_m` (45 evals): data_width=14..20, n_iter=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Same bit-accurate datapath as pipelined but registers every m stages, so it can trade Fmax against FF count and may reach a different LUT/accuracy point on the front. m is capped at 8 to keep the combinational path short enough to have a chance at >=250 MHz; the search will reveal whether any m>1 point is both fast enough and lower-LUT than the plain pipelined family.

**Result (code):** 100 evaluations this round, 100 total; 27 feasible; hypervolume 8085 (n/a).

**LLM decision:** `map_front` — Only `pipelined` is feasible: it is the sole family with any feasible design (27/55), while `pipelined_m` got 0/45 feasible (max throughput 171 MSPS < 250). The two unexplored families cannot help the 250 MSPS constraint: `iterative` needs N+3 cycles (even N=4 -> 7 cycles, requiring Fmax >= 1750 MHz) and `unrolled_k` needs ceil(N/k)+3 cycles (best case N=4,k=8 -> 4 cycles, requiring Fmax >= 1000 MHz), both far beyond what the cost model shows for this datapath (pipelined tops out at ~273 MSPS at 1 result/cycle). So adding them would only burn budget on throughput-infeasible points. Meanwhile the feasible front covers only luts 979..1469 against the HV reference of 4000 (about 12% of the luts range) and accuracy 13.6..15.9 bits, i.e. it is mapped only over a narrow slice of the luts objective. The registry permits data_width up to 28 and n_iter up to 30, so there is a large unexplored high-accuracy/higher-lut region that would extend the front rightward and add substantial hypervolume (each extra accuracy bit near luts~1500 is worth ~2500 HV units against the (4000,13) reference). This is exactly the 'front covers only a small part of an objective's range' case, so let code run NSGA-II over the full pipelined ranges seeded with the current 7-point front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 8085 (gain this round: n/a (first round)).
Feasible designs: 27 of 100 evaluations (22 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 45% violate; best seen 273
- max_abs_err <= 0.00012207: 40% violate; best seen 6.52e-06 (2^-17.23)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=20 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts=979, accuracy_bits=13.6, ffs=1014, throughput_msps=264, max_abs_err=8.24e-05 (2^-13.57), power_index=18.7
- pipelined [data_width=19 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc] luts=1169, accuracy_bits=14.7, ffs=1193, throughput_msps=264, max_abs_err=3.81e-05 (2^-14.68), power_index=22.2
- pipelined [data_width=20 n_iter=19 angle_guard=0 frac_guard=1 rounding=trunc] luts=1295, accuracy_bits=14.8, ffs=1319, throughput_msps=264, max_abs_err=3.54e-05 (2^-14.78), power_index=24.6
- pipelined [data_width=19 n_iter=19 angle_guard=2 frac_guard=2 rounding=trunc] luts=1314, accuracy_bits=15, ffs=1334, throughput_msps=264, max_abs_err=3.04e-05 (2^-15.00), power_index=24.9
- pipelined [data_width=20 n_iter=20 angle_guard=1 frac_guard=0 rounding=round] luts=1347, accuracy_bits=15.3, ffs=1372, throughput_msps=264, max_abs_err=2.52e-05 (2^-15.28), power_index=25.6
- pipelined [data_width=19 n_iter=20 angle_guard=2 frac_guard=4 rounding=trunc] luts=1467, accuracy_bits=15.6, ffs=1477, throughput_msps=257, max_abs_err=2.06e-05 (2^-15.57), power_index=27.7
- pipelined [data_width=20 n_iter=20 angle_guard=1 frac_guard=2 rounding=round] luts=1469, accuracy_bits=15.9, ffs=1447, throughput_msps=264, max_abs_err=1.61e-05 (2^-15.92), power_index=27.4
Front coverage: luts 979..1469 (HV reference 4000); accuracy_bits 13.6..15.9 (HV reference 13); data_width on the front 19..20 (registry 8..28).

Per family:
- pipelined: 55 evals, 27 feasible; max throughput seen 273 MSPS; best accuracy 15.92 bits; best feasible luts=979; feasible ranges: data_width 17..20, n_iter 15..20, angle_guard 0..2, frac_guard 0..4
- pipelined_m: 45 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 17.23 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined` (100 evals): data_width=18..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (7 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 91 feasible; hypervolume 1.778e+04 (+119.9%).

**LLM decision:** `map_front` — Only the pipelined family can satisfy the throughput constraint, so the front is (and will stay) pipelined-only: pipelined_m scored 0/45 feasible with max throughput 171 MSPS (< 250), and the two unexplored families are structurally incapable of 250 MSPS — iterative needs N+3 >= 7 cycles/result and unrolled_k needs ceil(N/k)+3 >= 4 cycles/result even at k=8/N=4, i.e. >1000 MHz at Artix-7 clocks (~270 MHz observed). Adding them would burn budget for nothing. Meanwhile the feasible front spans luts 979..2355 against an HV reference of 4000, so the high-LUT / high-accuracy region is unmapped and the curve is only partially covered (accuracy 13.6..20.3 bits, best seen 22.73). The min-LUT corner the selection rule wants is already feasible (979 LUTs, 13.6 bits, 264 MSPS), so the remaining 200 evals are best spent filling and extending the front rather than refining a corner that is already found.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.778e+04 (gain this round: +119.9%).
Feasible designs: 91 of 200 evaluations (77 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 35% violate; best seen 273
- max_abs_err <= 0.00012207: 26% violate; best seen 1.44e-07 (2^-22.73)

Pareto front (feasible, 17 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=20 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts=979, accuracy_bits=13.6, ffs=1014, throughput_msps=264, max_abs_err=8.24e-05 (2^-13.57), power_index=18.7
- pipelined [data_width=18 n_iter=17 angle_guard=1 frac_guard=1 rounding=round] luts=1105, accuracy_bits=13.8, ffs=1096, throughput_msps=264, max_abs_err=6.89e-05 (2^-13.83), power_index=20.7
- pipelined [data_width=19 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc] luts=1169, accuracy_bits=14.7, ffs=1193, throughput_msps=264, max_abs_err=3.81e-05 (2^-14.68), power_index=22.2
- pipelined [data_width=19 n_iter=18 angle_guard=1 frac_guard=3 rounding=trunc] luts=1259, accuracy_bits=14.8, ffs=1277, throughput_msps=264, max_abs_err=3.58e-05 (2^-14.77), power_index=23.9
- pipelined [data_width=25 n_iter=17 angle_guard=-2 frac_guard=0 rounding=trunc] luts=1337, accuracy_bits=15.9, ffs=1372, throughput_msps=257, max_abs_err=1.68e-05 (2^-15.86), power_index=25.5
- pipelined [data_width=21 n_iter=18 angle_guard=3 frac_guard=3 rounding=trunc] luts=1403, accuracy_bits=16.5, ffs=1423, throughput_msps=257, max_abs_err=1.08e-05 (2^-16.50), power_index=26.6
- pipelined [data_width=25 n_iter=18 angle_guard=1 frac_guard=1 rounding=round] luts=1563, accuracy_bits=16.9, ffs=1542, throughput_msps=257, max_abs_err=8.01e-06 (2^-16.93), power_index=29.2
- pipelined [data_width=21 n_iter=19 angle_guard=3 frac_guard=4 rounding=round] luts=1567, accuracy_bits=17.3, ffs=1539, throughput_msps=257, max_abs_err=6.05e-06 (2^-17.34), power_index=29.2
- pipelined [data_width=23 n_iter=21 angle_guard=1 frac_guard=2 rounding=round] luts=1740, accuracy_bits=18.6, ffs=1710, throughput_msps=257, max_abs_err=2.52e-06 (2^-18.60), power_index=32.4
- pipelined [data_width=23 n_iter=27 angle_guard=3 frac_guard=3 rounding=round] luts=2355, accuracy_bits=20.3, ffs=2305, throughput_msps=257, max_abs_err=7.87e-07 (2^-20.28), power_index=43.8
Front coverage: luts 979..2355 (HV reference 4000); accuracy_bits 13.6..20.3 (HV reference 13); data_width on the front 18..25 (registry 8..28).

Per family:
- pipelined: 155 evals, 91 feasible; max throughput seen 273 MSPS; best accuracy 22.73 bits; best feasible luts=979; feasible ranges: data_width 17..25, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 45 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 17.23 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined` (100 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (17 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 300 total; 152 feasible; hypervolume 1.791e+04 (+0.7%).

**LLM decision:** `map_front` — Only the pipelined family can satisfy the >=250 MSPS constraint: pipelined_m topped out at 171 MSPS (0 feasible in 45 evals), and iterative/unrolled_k emit one result every N+3 or ceil(N/k)+3 cycles, so even at optimistic Fmax they cannot reach 250 MSPS — adding them would burn budget on guaranteed-infeasible designs. The feasible front is entirely pipelined and spans luts 979..2355 against an HV reference of 4000, and accuracy_bits 13.6..20.3 against a best-seen 22.86, so a substantial part of both objective ranges is still unmapped (the low-LUT corner below 979 and the high-accuracy tail above 20.3 bits). With 100 evals and one round left, the reserved budget is best spent letting NSGA-II map the full pipelined ranges (data_width 8..28, n_iter 4..30, angle_guard -2..4, frac_guard 0..4, rounding trunc|round) seeded with the current 19-design front, which both extends hypervolume coverage and sharpens the min-LUT corner that the selection rule will pick from.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.791e+04 (gain this round: +0.7%).
Feasible designs: 152 of 300 evaluations (128 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 34% violate; best seen 273
- max_abs_err <= 0.00012207: 19% violate; best seen 1.31e-07 (2^-22.86)

Pareto front (feasible, 19 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=20 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts=979, accuracy_bits=13.6, ffs=1014, throughput_msps=264, max_abs_err=8.24e-05 (2^-13.57), power_index=18.7
- pipelined [data_width=18 n_iter=17 angle_guard=1 frac_guard=1 rounding=round] luts=1105, accuracy_bits=13.8, ffs=1096, throughput_msps=264, max_abs_err=6.89e-05 (2^-13.83), power_index=20.7
- pipelined [data_width=18 n_iter=17 angle_guard=1 frac_guard=3 rounding=trunc] luts=1135, accuracy_bits=14, ffs=1154, throughput_msps=264, max_abs_err=6.23e-05 (2^-13.97), power_index=21.5
- pipelined [data_width=21 n_iter=18 angle_guard=0 frac_guard=0 rounding=trunc] luts=1241, accuracy_bits=15.1, ffs=1271, throughput_msps=264, max_abs_err=2.85e-05 (2^-15.10), power_index=23.6
- pipelined [data_width=25 n_iter=17 angle_guard=-2 frac_guard=0 rounding=trunc] luts=1337, accuracy_bits=15.9, ffs=1372, throughput_msps=257, max_abs_err=1.68e-05 (2^-15.86), power_index=25.5
- pipelined [data_width=21 n_iter=18 angle_guard=3 frac_guard=3 rounding=trunc] luts=1403, accuracy_bits=16.5, ffs=1423, throughput_msps=257, max_abs_err=1.08e-05 (2^-16.50), power_index=26.6
- pipelined [data_width=25 n_iter=18 angle_guard=1 frac_guard=1 rounding=round] luts=1563, accuracy_bits=16.9, ffs=1542, throughput_msps=257, max_abs_err=8.01e-06 (2^-16.93), power_index=29.2
- pipelined [data_width=22 n_iter=19 angle_guard=3 frac_guard=3 rounding=round] luts=1588, accuracy_bits=17.7, ffs=1562, throughput_msps=257, max_abs_err=4.81e-06 (2^-17.67), power_index=29.6
- pipelined [data_width=23 n_iter=21 angle_guard=1 frac_guard=2 rounding=round] luts=1740, accuracy_bits=18.6, ffs=1710, throughput_msps=257, max_abs_err=2.52e-06 (2^-18.60), power_index=32.4
- pipelined [data_width=23 n_iter=27 angle_guard=3 frac_guard=3 rounding=round] luts=2355, accuracy_bits=20.3, ffs=2305, throughput_msps=257, max_abs_err=7.87e-07 (2^-20.28), power_index=43.8
Front coverage: luts 979..2355 (HV reference 4000); accuracy_bits 13.6..20.3 (HV reference 13); data_width on the front 18..26 (registry 8..28).

Per family:
- pipelined: 255 evals, 152 feasible; max throughput seen 273 MSPS; best accuracy 22.86 bits; best feasible luts=979; feasible ranges: data_width 17..26, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 45 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 17.23 bits
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined` (100 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (19 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 224 feasible; hypervolume 1.893e+04 (+5.7%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), so the only valid choices are stop or infeasible. Infeasible is ruled out by the evidence: 224 of 400 evaluations are feasible, the throughput constraint is met (best seen 273 MSPS >= 250) and the accuracy constraint is met with large margin (best max_abs_err 1.31e-07 = 2^-22.86, versus the 1.22e-04 = 2^-13 limit). The feasible Pareto front is well populated (26 designs, 189 unique feasible points) and spans luts 979..2182 against the HV reference 4000 and accuracy_bits 13.6..20.6 against the HV reference 13, i.e. it already brackets both reference points, and hypervolume is still improving (+5.7% this round) but no further evaluations remain. The spec's selection rule (min luts) is satisfied by the front's low-LUT corner: pipelined [data_width=20, n_iter=15, angle_guard=0, frac_guard=0, rounding=round] at 979 LUTs / 1014 FFs, 264 MSPS, max_abs_err 8.24e-05 (2^-13.57) — inside both constraints. Note pipelined_m contributed 0 feasible designs (max 171 MSPS) and iterative/unrolled_k were never needed since pipelined already meets the 1-result-per-cycle 250 MSPS requirement. Stop.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.893e+04 (gain this round: +5.7%).
Feasible designs: 224 of 400 evaluations (189 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 30% violate; best seen 273
- max_abs_err <= 0.00012207: 18% violate; best seen 1.31e-07 (2^-22.86)

Pareto front (feasible, 26 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=20 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts=979, accuracy_bits=13.6, ffs=1014, throughput_msps=264, max_abs_err=8.24e-05 (2^-13.57), power_index=18.7
- pipelined [data_width=20 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] luts=1080, accuracy_bits=13.8, ffs=1072, throughput_msps=264, max_abs_err=6.81e-05 (2^-13.84), power_index=20.2
- pipelined [data_width=23 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc] luts=1156, accuracy_bits=14, ffs=1192, throughput_msps=257, max_abs_err=6.22e-05 (2^-13.97), power_index=22.1
- pipelined [data_width=21 n_iter=18 angle_guard=0 frac_guard=0 rounding=trunc] luts=1241, accuracy_bits=15.1, ffs=1271, throughput_msps=264, max_abs_err=2.85e-05 (2^-15.10), power_index=23.6
- pipelined [data_width=25 n_iter=17 angle_guard=-2 frac_guard=0 rounding=trunc] luts=1337, accuracy_bits=15.9, ffs=1372, throughput_msps=257, max_abs_err=1.68e-05 (2^-15.86), power_index=25.5
- pipelined [data_width=22 n_iter=19 angle_guard=1 frac_guard=0 rounding=round] luts=1390, accuracy_bits=16.9, ffs=1419, throughput_msps=257, max_abs_err=8.35e-06 (2^-16.87), power_index=26.4
- pipelined [data_width=23 n_iter=19 angle_guard=1 frac_guard=1 rounding=round] luts=1533, accuracy_bits=17.4, ffs=1512, throughput_msps=257, max_abs_err=5.75e-06 (2^-17.41), power_index=28.6
- pipelined [data_width=25 n_iter=19 angle_guard=1 frac_guard=1 rounding=trunc] luts=1599, accuracy_bits=17.8, ffs=1625, throughput_msps=257, max_abs_err=4.24e-06 (2^-17.85), power_index=30.3
- pipelined [data_width=26 n_iter=21 angle_guard=-1 frac_guard=0 rounding=round] luts=1754, accuracy_bits=19.2, ffs=1780, throughput_msps=257, max_abs_err=1.66e-06 (2^-19.20), power_index=33.2
- pipelined [data_width=25 n_iter=25 angle_guard=1 frac_guard=1 rounding=round] luts=2182, accuracy_bits=20.6, ffs=2142, throughput_msps=257, max_abs_err=6.42e-07 (2^-20.57), power_index=40.7
Front coverage: luts 979..2182 (HV reference 4000); accuracy_bits 13.6..20.6 (HV reference 13); data_width on the front 18..26 (registry 8..28).

Per family:
- pipelined: 355 evals, 224 feasible; max throughput seen 273 MSPS; best accuracy 22.86 bits; best feasible luts=979; feasible ranges: data_width 17..26, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 45 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 17.23 bits
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 25547 in, 11512 out
- provider-reported cost: $0.0135
- full prompts and replies: `llm_trace.jsonl`

