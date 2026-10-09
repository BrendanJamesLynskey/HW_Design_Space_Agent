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
`pipelined:data_width=18,n_iter=15,angle_guard=3,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts)

| metric | value | provenance |
|---|---|---|
| luts | 935 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 969 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 64.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 17.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000119 (2^-13.04) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 7.77 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 3.01e-05 (2^-15.02) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.97 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 17 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 96.7 dBc, SNR 87.4 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (25 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=15,angle_guard=3,frac_guard=0,rounding=round` | 935 | 969 | 264.5 | 17 | 17.9 | 0.000119 (2^-13.04) | 13.04 |
| 1 | `pipelined:data_width=19,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 949 | 984 | 264.5 | 17 | 18.2 | 8.66e-05 (2^-13.50) | 13.50 |
| 2 | `pipelined:data_width=19,n_iter=15,angle_guard=3,frac_guard=0,rounding=round` | 979 | 1014 | 264.5 | 17 | 18.7 | 8.25e-05 (2^-13.57) | 13.57 |
| 3 | `pipelined:data_width=20,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 994 | 1029 | 264.5 | 17 | 19 | 7.63e-05 (2^-13.68) | 13.68 |
| 4 | `pipelined:data_width=18,n_iter=15,angle_guard=3,frac_guard=3,rounding=round` | 1061 | 1049 | 264.5 | 17 | 19.8 | 7.32e-05 (2^-13.74) | 13.74 |
| 5 | `pipelined:data_width=21,n_iter=16,angle_guard=-2,frac_guard=0,rounding=round` | 1064 | 1098 | 264.5 | 18 | 20.3 | 6.51e-05 (2^-13.91) | 13.91 |
| 6 | `pipelined:data_width=21,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc` | 1096 | 1130 | 264.5 | 18 | 20.9 | 4.76e-05 (2^-14.36) | 14.36 |
| 7 | `pipelined:data_width=21,n_iter=16,angle_guard=1,frac_guard=0,rounding=trunc` | 1112 | 1146 | 264.5 | 18 | 21.2 | 4.46e-05 (2^-14.45) | 14.45 |
| 8 | `pipelined:data_width=20,n_iter=17,angle_guard=1,frac_guard=0,rounding=round` | 1135 | 1166 | 264.5 | 19 | 21.6 | 3.32e-05 (2^-14.88) | 14.88 |
| 9 | `pipelined:data_width=20,n_iter=17,angle_guard=2,frac_guard=0,rounding=round` | 1152 | 1183 | 264.5 | 19 | 22 | 2.85e-05 (2^-15.10) | 15.10 |
| 10 | `pipelined:data_width=20,n_iter=17,angle_guard=1,frac_guard=1,rounding=round` | 1211 | 1199 | 264.5 | 19 | 22.7 | 2.58e-05 (2^-15.24) | 15.24 |
| 11 | `pipelined:data_width=22,n_iter=17,angle_guard=0,frac_guard=0,rounding=round` | 1219 | 1252 | 264.5 | 19 | 23.2 | 2.12e-05 (2^-15.52) | 15.52 |
| 12 | `pipelined:data_width=21,n_iter=17,angle_guard=1,frac_guard=2,rounding=trunc` | 1253 | 1278 | 256.5 | 19 | 23.8 | 2.11e-05 (2^-15.53) | 15.53 |
| 13 | `pipelined:data_width=22,n_iter=17,angle_guard=4,frac_guard=0,rounding=round` | 1287 | 1321 | 256.5 | 19 | 24.5 | 1.83e-05 (2^-15.74) | 15.74 |
| 14 | `pipelined:data_width=23,n_iter=18,angle_guard=-1,frac_guard=0,rounding=trunc` | 1331 | 1362 | 256.5 | 20 | 25.3 | 1.39e-05 (2^-16.14) | 16.14 |
| 15 | `pipelined:data_width=22,n_iter=18,angle_guard=3,frac_guard=0,rounding=round` | 1349 | 1380 | 256.5 | 20 | 25.7 | 1.1e-05 (2^-16.47) | 16.47 |
| 16 | `pipelined:data_width=24,n_iter=18,angle_guard=-1,frac_guard=0,rounding=trunc` | 1385 | 1417 | 256.5 | 20 | 26.3 | 1.03e-05 (2^-16.57) | 16.57 |
| 17 | `pipelined:data_width=23,n_iter=18,angle_guard=0,frac_guard=1,rounding=round` | 1433 | 1415 | 256.5 | 20 | 26.8 | 9.76e-06 (2^-16.64) | 16.64 |
| 18 | `pipelined:data_width=23,n_iter=18,angle_guard=3,frac_guard=1,rounding=trunc` | 1438 | 1467 | 256.5 | 20 | 27.3 | 9.51e-06 (2^-16.68) | 16.68 |
| 19 | `pipelined:data_width=21,n_iter=19,angle_guard=4,frac_guard=1,rounding=round` | 1472 | 1455 | 256.5 | 21 | 27.5 | 8.82e-06 (2^-16.79) | 16.79 |
| 20 | `pipelined:data_width=21,n_iter=19,angle_guard=3,frac_guard=3,rounding=trunc` | 1485 | 1502 | 256.5 | 21 | 28.1 | 7.43e-06 (2^-17.04) | 17.04 |
| 21 | `pipelined:data_width=22,n_iter=20,angle_guard=1,frac_guard=2,rounding=round` | 1593 | 1568 | 256.5 | 22 | 29.7 | 4.59e-06 (2^-17.73) | 17.73 |
| 22 | `pipelined:data_width=23,n_iter=22,angle_guard=0,frac_guard=0,rounding=round` | 1665 | 1687 | 256.5 | 24 | 31.5 | 3.98e-06 (2^-17.94) | 17.94 |
| 23 | `pipelined:data_width=25,n_iter=21,angle_guard=1,frac_guard=0,rounding=round` | 1733 | 1759 | 256.5 | 23 | 32.8 | 1.73e-06 (2^-19.14) | 19.14 |
| 24 | `pipelined:data_width=26,n_iter=28,angle_guard=-1,frac_guard=0,rounding=trunc` | 2367 | 2373 | 256.5 | 30 | 44.6 | 1.17e-06 (2^-19.71) | 19.71 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=250 MSPS one sample/clock. In the registry only pipelined and pipelined_m produce one result/cycle; iterative and unrolled_k have >=4 cycles/result (unrolled_k minimum ceil(N/k)+3 with N<=k gives 4; iterative minimum N+3 gives 7), so they cannot reach 250 MSPS even with an optimistic Fmax. Therefore we search only pipelined (register every micro-rotation, best timing) and pipelined_m (register every m stages, fewer pipeline registers, potentially lower LUTs if timing still closes). The accuracy constraint max_abs_err <= 2^-13 forces data_width and n_iter to be sufficiently large; we span 14..20 bits and 12..20 iterations to explore the LUT-vs-accuracy trade-off. angle_guard and frac_guard ranges let the search trade guard bits for LUT savings, and rounding covers trunc vs round. For pipelined_m, m in 2..4 explores the register-count vs timing trade-off. Budget is split to cover both families, with slightly more to pipelined as the safer timing family.*)
- `pipelined` (55 evals): data_width=14..20, n_iter=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Registers every micro-rotation, giving the shortest logic depth per stage and the best chance to close timing at >=250 MHz. Its parameter space (W, N, angle_guard, frac_guard, rounding) directly trades LUTs for accuracy, so it should populate the feasible side of the Pareto front.
- `pipelined_m` (45 evals): data_width=14..20, n_iter=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* Registers every m stages, reducing pipeline flip-flops and potentially lowering area if timing still closes at 250 MHz. m=2..4 balances the area reduction against increased logic depth. This family is important for the min-LUT objective and for covering the low-LUT end of the front.

**Result (code):** 100 evaluations this round, 100 total; 31 feasible; hypervolume 5130 (n/a).

**LLM decision:** `map_front` — Round 1 shows the feasible set is essentially single-family. pipelined_m produced 0/45 feasible designs (max throughput 171 MSPS < 250), and the two unexplored families are structurally unable to meet the throughput constraint: iterative needs N+3 cycles/result and unrolled_k needs ceil(N/k)+3 cycles/result, so both are >1 cycle/result and cannot reach 250 MSPS given the best Fmax observed anywhere is 282 MSPS. That leaves pipelined as the only family that can satisfy throughput_msps >= 250. Its front, however, is narrow: data_width 18..20 and n_iter 15..20 only, luts 949..1333 against an HV reference of 4000, i.e. it covers only a small part of the LUT objective's range, and accuracy_bits 13.5..14.8 against a reference of 13. With 300 of 400 evals still unspent, the highest-value move is the reserved front-mapping pass: run NSGA-II over the full pipelined ranges (data_width 8..28, n_iter 4..30, angle_guard -2..4, frac_guard 0..4, rounding) seeded with the current 7-design front, so the whole trade-off curve (lower-LUT corner and higher-accuracy tail) is covered rather than just the region round 1 happened to sample. No next_plan is needed for map_front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 5130 (gain this round: n/a (first round)).
Feasible designs: 31 of 100 evaluations (21 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 45% violate; best seen 282
- max_abs_err <= 0.00012207: 51% violate; best seen 2.4e-05 (2^-15.35)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts=949, accuracy_bits=13.5, ffs=984, throughput_msps=264, max_abs_err=8.66e-05 (2^-13.50), power_index=18.2
- pipelined [data_width=20 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts=994, accuracy_bits=13.7, ffs=1029, throughput_msps=264, max_abs_err=7.63e-05 (2^-13.68), power_index=19
- pipelined [data_width=19 n_iter=15 angle_guard=2 frac_guard=3 rounding=round] luts=1093, accuracy_bits=13.8, ffs=1080, throughput_msps=264, max_abs_err=7.02e-05 (2^-13.80), power_index=20.4
- pipelined [data_width=20 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] luts=1110, accuracy_bits=13.9, ffs=1099, throughput_msps=264, max_abs_err=6.58e-05 (2^-13.89), power_index=20.8
- pipelined [data_width=18 n_iter=17 angle_guard=2 frac_guard=3 rounding=round] luts=1190, accuracy_bits=14.6, ffs=1173, throughput_msps=264, max_abs_err=4.11e-05 (2^-14.57), power_index=22.2
- pipelined [data_width=19 n_iter=19 angle_guard=2 frac_guard=0 rounding=round] luts=1238, accuracy_bits=14.7, ffs=1265, throughput_msps=264, max_abs_err=3.86e-05 (2^-14.66), power_index=23.5
- pipelined [data_width=18 n_iter=19 angle_guard=2 frac_guard=3 rounding=round] luts=1333, accuracy_bits=14.8, ffs=1313, throughput_msps=264, max_abs_err=3.58e-05 (2^-14.77), power_index=24.9
Front coverage: luts 949..1333 (HV reference 4000); accuracy_bits 13.5..14.8 (HV reference 13); data_width on the front 18..20 (registry 8..28).

Per family:
- pipelined: 55 evals, 31 feasible; max throughput seen 282 MSPS; best accuracy 14.77 bits; best feasible luts=949; feasible ranges: data_width 18..20, n_iter 15..20, angle_guard -1..2, frac_guard 0..4
- pipelined_m: 45 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.35 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined` (100 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (7 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 91 feasible; hypervolume 1.646e+04 (+220.9%).

**LLM decision:** `refine` — Only `pipelined` can meet the 250 MSPS throughput constraint: `pipelined_m` produced 0 feasible designs (max throughput 171 MSPS), and the multi-cycle families `iterative`/`unrolled_k` (N+3 and ceil(N/k)+3 cycles/result) cannot reach 250 MSPS at any plausible Fmax, so they are not worth budget. The selection rule is min LUTs, and the current min-LUT corner is 949 LUTs at accuracy 13.5 bits (data_width=19, n_iter=15); the front's feasible data_width starts at 17, so lower-width designs may cut LUTs while still clearing the 2^-13 error bound (the 949-LUT design's error 2^-13.5 is CORDIC-limited, not output-quantisation-limited, so shrinking W is promising). There is also an empty accuracy band between the HV reference (13) and the front's low end (13.5) that a lower-LUT design would fill, raising hypervolume. Refine pipelined around this low-LUT / near-constraint region.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.646e+04 (gain this round: +220.9%).
Feasible designs: 91 of 200 evaluations (74 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 36% violate; best seen 282
- max_abs_err <= 0.00012207: 32% violate; best seen 7.07e-08 (2^-23.75)

Pareto front (feasible, 17 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts=949, accuracy_bits=13.5, ffs=984, throughput_msps=264, max_abs_err=8.66e-05 (2^-13.50), power_index=18.2
- pipelined [data_width=21 n_iter=16 angle_guard=-2 frac_guard=0 rounding=round] luts=1064, accuracy_bits=13.9, ffs=1098, throughput_msps=264, max_abs_err=6.51e-05 (2^-13.91), power_index=20.3
- pipelined [data_width=21 n_iter=16 angle_guard=1 frac_guard=0 rounding=trunc] luts=1112, accuracy_bits=14.5, ffs=1146, throughput_msps=264, max_abs_err=4.46e-05 (2^-14.45), power_index=21.2
- pipelined [data_width=21 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] luts=1159, accuracy_bits=14.7, ffs=1191, throughput_msps=257, max_abs_err=3.79e-05 (2^-14.69), power_index=22.1
- pipelined [data_width=22 n_iter=17 angle_guard=4 frac_guard=0 rounding=round] luts=1287, accuracy_bits=15.7, ffs=1321, throughput_msps=257, max_abs_err=1.83e-05 (2^-15.74), power_index=24.5
- pipelined [data_width=22 n_iter=18 angle_guard=3 frac_guard=0 rounding=round] luts=1349, accuracy_bits=16.5, ffs=1380, throughput_msps=257, max_abs_err=1.1e-05 (2^-16.47), power_index=25.7
- pipelined [data_width=23 n_iter=18 angle_guard=0 frac_guard=1 rounding=round] luts=1433, accuracy_bits=16.6, ffs=1415, throughput_msps=257, max_abs_err=9.76e-06 (2^-16.64), power_index=26.8
- pipelined [data_width=23 n_iter=18 angle_guard=3 frac_guard=1 rounding=trunc] luts=1438, accuracy_bits=16.7, ffs=1467, throughput_msps=257, max_abs_err=9.51e-06 (2^-16.68), power_index=27.3
- pipelined [data_width=23 n_iter=22 angle_guard=0 frac_guard=3 rounding=round] luts=1846, accuracy_bits=18.2, ffs=1810, throughput_msps=257, max_abs_err=3.26e-06 (2^-18.23), power_index=34.4
- pipelined [data_width=26 n_iter=28 angle_guard=-1 frac_guard=0 rounding=trunc] luts=2367, accuracy_bits=19.7, ffs=2373, throughput_msps=257, max_abs_err=1.17e-06 (2^-19.71), power_index=44.6
Front coverage: luts 949..2367 (HV reference 4000); accuracy_bits 13.5..19.7 (HV reference 13); data_width on the front 19..26 (registry 8..28).

Per family:
- pipelined: 155 evals, 91 feasible; max throughput seen 282 MSPS; best accuracy 23.75 bits; best feasible luts=949; feasible ranges: data_width 17..26, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 45 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.35 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Target the min-LUT corner (selection rule) and the empty accuracy band just above the HV reference, using the only throughput-feasible family.*)
- `pipelined` (100 evals): data_width=16..21, n_iter=14..20, angle_guard=-2..4, frac_guard=0..3, rounding=trunc|round. *Why:* Pipelined is the only family that clears 250 MSPS; focus on low data_width / low n_iter to push the min-LUT corner below 949 LUTs and fill the 13.0-13.5 accuracy gap, while keeping angle_guard/frac_guard/rounding free to hold max_abs_err <= 2^-13.

**Result (code):** 100 evaluations this round, 300 total; 163 feasible; hypervolume 1.658e+04 (+0.7%).

**LLM decision:** `map_front` — Only `pipelined` can satisfy the 250 MSPS constraint, so the last round must be spent on it. `pipelined_m` produced 0 feasible designs in 45 evals (max throughput 171 MSPS < 250), and `iterative`/`unrolled_k` are strictly worse on throughput (1 result per N+3 or ceil(N/k)+3 cycles, i.e. ≤1/4 results/cycle), so `add_family` would burn the final 100 evals on families that cannot reach 250 MSPS. The front is also clearly under-explored at the high-accuracy end: it spans luts 935..2367 (HV ref 4000) and accuracy_bits only 13..19.7, while the best accuracy seen anywhere is 23.75 bits. Since accuracy depends only on (data_width, n_iter, angle_guard, frac_guard, rounding) and not on family, a pipelined design with those same parameters would be feasible at ~257 MSPS and would sit on the front — it is absent only because it was never evaluated as `pipelined`. Extending the front from (2367, 19.7) toward ~23.75 bits at luts < 4000 adds a large rectangle to the HV (roughly (4000-luts)*(23.75-19.7)), far more than the +0.7% seen this round. Refining around the current region would not reach it.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.658e+04 (gain this round: +0.7%).
Feasible designs: 163 of 300 evaluations (131 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 24% violate; best seen 282
- max_abs_err <= 0.00012207: 31% violate; best seen 7.07e-08 (2^-23.75)

Pareto front (feasible, 23 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=3 frac_guard=0 rounding=round] luts=935, accuracy_bits=13, ffs=969, throughput_msps=264, max_abs_err=0.000119 (2^-13.04), power_index=17.9
- pipelined [data_width=20 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts=994, accuracy_bits=13.7, ffs=1029, throughput_msps=264, max_abs_err=7.63e-05 (2^-13.68), power_index=19
- pipelined [data_width=21 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc] luts=1096, accuracy_bits=14.4, ffs=1130, throughput_msps=264, max_abs_err=4.76e-05 (2^-14.36), power_index=20.9
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=0 rounding=round] luts=1152, accuracy_bits=15.1, ffs=1183, throughput_msps=264, max_abs_err=2.85e-05 (2^-15.10), power_index=22
- pipelined [data_width=21 n_iter=17 angle_guard=1 frac_guard=2 rounding=trunc] luts=1253, accuracy_bits=15.5, ffs=1278, throughput_msps=257, max_abs_err=2.11e-05 (2^-15.53), power_index=23.8
- pipelined [data_width=23 n_iter=18 angle_guard=-1 frac_guard=0 rounding=trunc] luts=1331, accuracy_bits=16.1, ffs=1362, throughput_msps=257, max_abs_err=1.39e-05 (2^-16.14), power_index=25.3
- pipelined [data_width=23 n_iter=18 angle_guard=0 frac_guard=1 rounding=round] luts=1433, accuracy_bits=16.6, ffs=1415, throughput_msps=257, max_abs_err=9.76e-06 (2^-16.64), power_index=26.8
- pipelined [data_width=21 n_iter=19 angle_guard=4 frac_guard=1 rounding=round] luts=1472, accuracy_bits=16.8, ffs=1455, throughput_msps=257, max_abs_err=8.82e-06 (2^-16.79), power_index=27.5
- pipelined [data_width=23 n_iter=22 angle_guard=0 frac_guard=3 rounding=round] luts=1846, accuracy_bits=18.2, ffs=1810, throughput_msps=257, max_abs_err=3.26e-06 (2^-18.23), power_index=34.4
- pipelined [data_width=26 n_iter=28 angle_guard=-1 frac_guard=0 rounding=trunc] luts=2367, accuracy_bits=19.7, ffs=2373, throughput_msps=257, max_abs_err=1.17e-06 (2^-19.71), power_index=44.6
Front coverage: luts 935..2367 (HV reference 4000); accuracy_bits 13..19.7 (HV reference 13); data_width on the front 18..26 (registry 8..28).

Per family:
- pipelined: 255 evals, 163 feasible; max throughput seen 282 MSPS; best accuracy 23.75 bits; best feasible luts=935; feasible ranges: data_width 16..26, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 45 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.35 bits
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined` (100 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (23 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 229 feasible; hypervolume 1.712e+04 (+3.3%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), so no further search is possible. The run is not infeasible: 229 of 400 evaluations are feasible, and the constraints are met with margin — throughput reaches 282 MSPS against the 250 MSPS floor, and max_abs_err reaches 2^-23.75 against the 2^-13 limit. The feasible Pareto front spans luts 935..2367 and accuracy_bits 13..19.7, i.e. it already covers the accuracy objective's full useful range and a good part of the LUT range (HV ref 4000), and hypervolume is still improving (+3.3% this round, 1.712e+04). The spec's selection rule (min luts) is satisfied by pipelined [data_width=18 n_iter=15 angle_guard=3 frac_guard=0 rounding=round]: 935 LUTs, 969 FFs, 264 MSPS, max_abs_err 2^-13.04, accuracy_bits 13.0 — the cheapest design that clears both constraints. The unexplored families cannot help the min-LUT corner: iterative/unrolled_k emit one result every several cycles and pipelined_m topped out at 171 MSPS, all below the 250 MSPS floor, so they cannot produce a feasible design, let alone a cheaper one. Stopping here.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.712e+04 (gain this round: +3.3%).
Feasible designs: 229 of 400 evaluations (190 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 22% violate; best seen 282
- max_abs_err <= 0.00012207: 28% violate; best seen 7.07e-08 (2^-23.75)

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=3 frac_guard=0 rounding=round] luts=935, accuracy_bits=13, ffs=969, throughput_msps=264, max_abs_err=0.000119 (2^-13.04), power_index=17.9
- pipelined [data_width=20 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts=994, accuracy_bits=13.7, ffs=1029, throughput_msps=264, max_abs_err=7.63e-05 (2^-13.68), power_index=19
- pipelined [data_width=21 n_iter=16 angle_guard=-2 frac_guard=0 rounding=round] luts=1064, accuracy_bits=13.9, ffs=1098, throughput_msps=264, max_abs_err=6.51e-05 (2^-13.91), power_index=20.3
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] luts=1135, accuracy_bits=14.9, ffs=1166, throughput_msps=264, max_abs_err=3.32e-05 (2^-14.88), power_index=21.6
- pipelined [data_width=22 n_iter=17 angle_guard=0 frac_guard=0 rounding=round] luts=1219, accuracy_bits=15.5, ffs=1252, throughput_msps=264, max_abs_err=2.12e-05 (2^-15.52), power_index=23.2
- pipelined [data_width=22 n_iter=17 angle_guard=4 frac_guard=0 rounding=round] luts=1287, accuracy_bits=15.7, ffs=1321, throughput_msps=257, max_abs_err=1.83e-05 (2^-15.74), power_index=24.5
- pipelined [data_width=24 n_iter=18 angle_guard=-1 frac_guard=0 rounding=trunc] luts=1385, accuracy_bits=16.6, ffs=1417, throughput_msps=257, max_abs_err=1.03e-05 (2^-16.57), power_index=26.3
- pipelined [data_width=21 n_iter=19 angle_guard=4 frac_guard=1 rounding=round] luts=1472, accuracy_bits=16.8, ffs=1455, throughput_msps=257, max_abs_err=8.82e-06 (2^-16.79), power_index=27.5
- pipelined [data_width=22 n_iter=20 angle_guard=1 frac_guard=2 rounding=round] luts=1593, accuracy_bits=17.7, ffs=1568, throughput_msps=257, max_abs_err=4.59e-06 (2^-17.73), power_index=29.7
- pipelined [data_width=26 n_iter=28 angle_guard=-1 frac_guard=0 rounding=trunc] luts=2367, accuracy_bits=19.7, ffs=2373, throughput_msps=257, max_abs_err=1.17e-06 (2^-19.71), power_index=44.6
Front coverage: luts 935..2367 (HV reference 4000); accuracy_bits 13..19.7 (HV reference 13); data_width on the front 18..26 (registry 8..28).

Per family:
- pipelined: 355 evals, 229 feasible; max throughput seen 282 MSPS; best accuracy 23.75 bits; best feasible luts=935; feasible ranges: data_width 16..26, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 45 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.35 bits
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 26511 in, 20607 out
- provider-reported cost: $0.0193
- full prompts and replies: `llm_trace.jsonl`

