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
`pipelined:data_width=17,n_iter=15,angle_guard=3,frac_guard=2,rounding=round` — selection: auto (spec rule: min luts)

| metric | value | provenance |
|---|---|---|
| luts | 985 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 978 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 64.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 18.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 9.31e-05 (2^-13.39) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 3.05 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.8e-05 (2^-15.13) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 0.917 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.4 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 17 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 98.2 dBc, SNR 88.1 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (35 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=17,n_iter=15,angle_guard=3,frac_guard=2,rounding=round` | 985 | 978 | 264.5 | 17 | 18.5 | 9.31e-05 (2^-13.39) | 13.39 |
| 1 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=1,rounding=round` | 987 | 982 | 264.5 | 17 | 18.5 | 9.31e-05 (2^-13.39) | 13.39 |
| 2 | `pipelined:data_width=20,n_iter=16,angle_guard=-1,frac_guard=0,rounding=round` | 1033 | 1065 | 264.5 | 18 | 19.7 | 6.98e-05 (2^-13.81) | 13.81 |
| 3 | `pipelined:data_width=20,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 1048 | 1082 | 264.5 | 18 | 20 | 5.27e-05 (2^-14.21) | 14.21 |
| 4 | `pipelined:data_width=19,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 1104 | 1096 | 264.5 | 18 | 20.7 | 4.95e-05 (2^-14.30) | 14.30 |
| 5 | `pipelined:data_width=22,n_iter=16,angle_guard=-1,frac_guard=0,rounding=round` | 1128 | 1162 | 264.5 | 18 | 21.5 | 3.88e-05 (2^-14.65) | 14.65 |
| 6 | `pipelined:data_width=20,n_iter=16,angle_guard=3,frac_guard=2,rounding=trunc` | 1159 | 1186 | 256.5 | 18 | 22.1 | 3.8e-05 (2^-14.68) | 14.68 |
| 7 | `pipelined:data_width=21,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 1175 | 1203 | 256.5 | 18 | 22.4 | 3.61e-05 (2^-14.76) | 14.76 |
| 8 | `pipelined:data_width=20,n_iter=16,angle_guard=3,frac_guard=2,rounding=round` | 1201 | 1189 | 256.5 | 18 | 22.5 | 3.51e-05 (2^-14.80) | 14.80 |
| 9 | `pipelined:data_width=19,n_iter=17,angle_guard=4,frac_guard=2,rounding=trunc` | 1202 | 1227 | 256.5 | 19 | 22.8 | 3.31e-05 (2^-14.88) | 14.88 |
| 10 | `pipelined:data_width=19,n_iter=17,angle_guard=3,frac_guard=3,rounding=trunc` | 1219 | 1240 | 264.5 | 19 | 23.1 | 3.09e-05 (2^-14.98) | 14.98 |
| 11 | `pipelined:data_width=18,n_iter=17,angle_guard=4,frac_guard=3,rounding=round` | 1223 | 1208 | 264.5 | 19 | 22.9 | 3.03e-05 (2^-15.01) | 15.01 |
| 12 | `pipelined:data_width=20,n_iter=18,angle_guard=1,frac_guard=1,rounding=trunc` | 1241 | 1267 | 264.5 | 20 | 23.6 | 2.8e-05 (2^-15.12) | 15.12 |
| 13 | `pipelined:data_width=19,n_iter=17,angle_guard=4,frac_guard=2,rounding=round` | 1242 | 1229 | 256.5 | 19 | 23.2 | 2.4e-05 (2^-15.35) | 15.35 |
| 14 | `pipelined:data_width=20,n_iter=17,angle_guard=3,frac_guard=3,rounding=trunc` | 1270 | 1291 | 256.5 | 19 | 24.1 | 2.19e-05 (2^-15.48) | 15.48 |
| 15 | `pipelined:data_width=21,n_iter=18,angle_guard=2,frac_guard=0,rounding=round` | 1277 | 1308 | 256.5 | 20 | 24.3 | 1.59e-05 (2^-15.94) | 15.94 |
| 16 | `pipelined:data_width=21,n_iter=18,angle_guard=1,frac_guard=2,rounding=trunc` | 1331 | 1354 | 256.5 | 20 | 25.2 | 1.43e-05 (2^-16.10) | 16.10 |
| 17 | `pipelined:data_width=20,n_iter=18,angle_guard=3,frac_guard=2,rounding=round` | 1355 | 1338 | 256.5 | 20 | 25.3 | 1.42e-05 (2^-16.11) | 16.11 |
| 18 | `pipelined:data_width=21,n_iter=18,angle_guard=1,frac_guard=3,rounding=trunc` | 1367 | 1386 | 256.5 | 20 | 25.9 | 1.37e-05 (2^-16.16) | 16.16 |
| 19 | `pipelined:data_width=21,n_iter=18,angle_guard=1,frac_guard=2,rounding=round` | 1375 | 1356 | 256.5 | 20 | 25.7 | 1.31e-05 (2^-16.22) | 16.22 |
| 20 | `pipelined:data_width=20,n_iter=18,angle_guard=3,frac_guard=3,rounding=round` | 1391 | 1370 | 256.5 | 20 | 26 | 1.19e-05 (2^-16.36) | 16.36 |
| 21 | `pipelined:data_width=21,n_iter=18,angle_guard=2,frac_guard=2,rounding=round` | 1393 | 1374 | 256.5 | 20 | 26 | 1.11e-05 (2^-16.46) | 16.46 |
| 22 | `pipelined:data_width=21,n_iter=18,angle_guard=3,frac_guard=2,rounding=round` | 1411 | 1392 | 256.5 | 20 | 26.4 | 9.93e-06 (2^-16.62) | 16.62 |
| 23 | `pipelined:data_width=21,n_iter=18,angle_guard=4,frac_guard=2,rounding=round` | 1429 | 1410 | 256.5 | 20 | 26.7 | 9.83e-06 (2^-16.64) | 16.64 |
| 24 | `pipelined:data_width=21,n_iter=19,angle_guard=2,frac_guard=1,rounding=round` | 1434 | 1417 | 256.5 | 21 | 26.8 | 9.17e-06 (2^-16.74) | 16.74 |
| 25 | `pipelined:data_width=21,n_iter=19,angle_guard=3,frac_guard=1,rounding=round` | 1453 | 1436 | 256.5 | 21 | 27.2 | 8.82e-06 (2^-16.79) | 16.79 |
| 26 | `pipelined:data_width=22,n_iter=19,angle_guard=3,frac_guard=2,rounding=trunc` | 1504 | 1525 | 256.5 | 21 | 28.5 | 6.37e-06 (2^-17.26) | 17.26 |
| 27 | `pipelined:data_width=21,n_iter=19,angle_guard=4,frac_guard=2,rounding=round` | 1510 | 1489 | 256.5 | 21 | 28.2 | 6.19e-06 (2^-17.30) | 17.30 |
| 28 | `pipelined:data_width=24,n_iter=19,angle_guard=2,frac_guard=2,rounding=trunc` | 1599 | 1621 | 256.5 | 21 | 30.3 | 4.48e-06 (2^-17.77) | 17.77 |
| 29 | `pipelined:data_width=20,n_iter=21,angle_guard=4,frac_guard=4,rounding=round` | 1691 | 1660 | 256.5 | 23 | 31.5 | 4.37e-06 (2^-17.80) | 17.80 |
| 30 | `pipelined:data_width=25,n_iter=20,angle_guard=1,frac_guard=1,rounding=round` | 1740 | 1713 | 256.5 | 22 | 32.5 | 2.36e-06 (2^-18.69) | 18.69 |
| 31 | `pipelined:data_width=24,n_iter=22,angle_guard=0,frac_guard=2,rounding=trunc` | 1820 | 1834 | 256.5 | 24 | 34.4 | 2.2e-06 (2^-18.79) | 18.79 |
| 32 | `pipelined:data_width=23,n_iter=22,angle_guard=3,frac_guard=1,rounding=round` | 1824 | 1796 | 256.5 | 24 | 34 | 1.84e-06 (2^-19.05) | 19.05 |
| 33 | `pipelined:data_width=26,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc` | 1864 | 1887 | 256.5 | 24 | 35.3 | 1.23e-06 (2^-19.64) | 19.64 |
| 34 | `pipelined:data_width=26,n_iter=25,angle_guard=0,frac_guard=0,rounding=round` | 2130 | 2144 | 256.5 | 27 | 40.2 | 6.06e-07 (2^-20.65) | 20.65 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires one sample per clock at >=250 MSPS. Only the pipelined and pipelined_m families produce 1 result/cycle; iterative and unrolled_k have throughput = Fmax / cycles_per_result, which is far below 250 MSPS for any realistic Artix-7 Fmax (e.g. unrolled_k with k=8 and N=4 still needs 4 cycles/result, requiring Fmax >= 1000 MHz). Therefore the feasible Pareto front can only come from pipelined and pipelined_m. A tiny probe of unrolled_k is included only to confirm infeasibility. Accuracy requires max_abs_err <= 2^-13; since the output LSB is 2^-(W-2), W=14 gives half-LSB = 2^-13, so W>=14 is necessary. We explore W=14..20 and N=12..20 to cover the accuracy-vs-LUT trade-off. angle_guard and frac_guard affect both accuracy and LUTs, so their full ranges are searched. rounding is explored as trunc/round. For pipelined_m, m trades Fmax against FFs; m must be small enough to keep Fmax >= 250 MHz, so m=2..8 is explored.*)
- `pipelined` (55 evals): data_width=14..20, n_iter=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Pipelined gives 1 result/cycle and the highest Fmax, directly meeting the 250 MSPS throughput constraint. It is the primary candidate for minimum LUTs while satisfying accuracy. We search the full accuracy/LUT trade-off space: W=14..20, N=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round.
- `pipelined_m` (40 evals): data_width=14..20, n_iter=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Pipelined_m also gives 1 result/cycle but registers every m stages, reducing FFs at the cost of Fmax. It may offer a different LUT/FF trade-off and is needed to map the full Pareto front. We search the same accuracy parameters plus m=2..8 to find the largest m that still meets 250 MSPS.
- `unrolled_k` (5 evals): data_width=14..16, n_iter=4..8, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=8..8. *Why:* Unrolled_k is the best of the multi-cycle families for throughput (k=8 gives the fewest cycles/result). A small probe with k=8, N=4..8, W=14..16 is included only to confirm that even this family cannot reach 250 MSPS; if it fails, iterative will also fail, so no further budget is spent there.

**Result (code):** 100 evaluations this round, 100 total; 27 feasible; hypervolume 1.019e+04 (n/a).

**LLM decision:** `map_front` — Only the `pipelined` family can satisfy throughput >= 250 MSPS: it is the sole family with any feasible design (27/55 evals feasible, max 273 MSPS), while `unrolled_k` tops out at 26.8 MSPS and `pipelined_m` at 171 MSPS. The unexplored `iterative` family is structurally hopeless here — at N+3 cycles/result it would need Fmax >= 250*(N+3) >= 1750 MHz even at N=4, far beyond Artix-7. So the feasible front is pipelined-only and there is nothing to gain from add_family. The current front is also very narrow relative to the objectives: luts span only 985..1507 against an HV reference of 4000, and accuracy_bits only 13.4..16.7 while the registry allows far higher (data_width up to 28, n_iter up to 30). That means most of the hypervolume box (up to 4000 luts, well above 16.7 accuracy bits) is unexplored, and the front is dominated by its low-lut corner. Mapping the full pipelined ranges seeded with the current front should extend the curve to higher accuracy (and probe lower data_width/n_iter for even lower LUTs), which is exactly what the hypervolume score rewards. Refining now would only re-sample the already-dense 985..1507 region.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 1.019e+04 (gain this round: n/a (first round)).
Feasible designs: 27 of 100 evaluations (23 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 45% violate; best seen 273
- max_abs_err <= 0.00012207: 53% violate; best seen 8.54e-06 (2^-16.84)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] luts=985, accuracy_bits=13.4, ffs=978, throughput_msps=264, max_abs_err=9.31e-05 (2^-13.39), power_index=18.5
- pipelined [data_width=20 n_iter=15 angle_guard=0 frac_guard=2 rounding=trunc] luts=1038, accuracy_bits=13.6, ffs=1066, throughput_msps=264, max_abs_err=7.88e-05 (2^-13.63), power_index=19.8
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=3 rounding=trunc] luts=1096, accuracy_bits=14.2, ffs=1118, throughput_msps=264, max_abs_err=5.44e-05 (2^-14.17), power_index=20.8
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] luts=1104, accuracy_bits=14.3, ffs=1096, throughput_msps=264, max_abs_err=4.95e-05 (2^-14.30), power_index=20.7
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=trunc] luts=1135, accuracy_bits=14.3, ffs=1166, throughput_msps=264, max_abs_err=4.89e-05 (2^-14.32), power_index=21.6
- pipelined [data_width=19 n_iter=17 angle_guard=3 frac_guard=3 rounding=trunc] luts=1219, accuracy_bits=15, ffs=1240, throughput_msps=264, max_abs_err=3.09e-05 (2^-14.98), power_index=23.1
- pipelined [data_width=20 n_iter=17 angle_guard=3 frac_guard=3 rounding=trunc] luts=1270, accuracy_bits=15.5, ffs=1291, throughput_msps=257, max_abs_err=2.19e-05 (2^-15.48), power_index=24.1
- pipelined [data_width=20 n_iter=17 angle_guard=3 frac_guard=4 rounding=trunc] luts=1303, accuracy_bits=15.6, ffs=1322, throughput_msps=257, max_abs_err=2.04e-05 (2^-15.58), power_index=24.7
- pipelined [data_width=20 n_iter=20 angle_guard=3 frac_guard=2 rounding=trunc] luts=1467, accuracy_bits=16.1, ffs=1485, throughput_msps=257, max_abs_err=1.42e-05 (2^-16.10), power_index=27.8
- pipelined [data_width=20 n_iter=20 angle_guard=3 frac_guard=3 rounding=trunc] luts=1507, accuracy_bits=16.7, ffs=1521, throughput_msps=257, max_abs_err=9.41e-06 (2^-16.70), power_index=28.5
Front coverage: luts 985..1507 (HV reference 4000); accuracy_bits 13.4..16.7 (HV reference 13); data_width on the front 17..20 (registry 8..28).

Per family:
- unrolled_k: 5 evals, 0 feasible; max throughput seen 26.8 MSPS; best accuracy 6.95 bits
- pipelined: 55 evals, 27 feasible; max throughput seen 273 MSPS; best accuracy 16.70 bits; best feasible luts=985; feasible ranges: data_width 17..20, n_iter 15..20, angle_guard 0..3, frac_guard 0..4
- pipelined_m: 40 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 16.84 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined` (100 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (13 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 91 feasible; hypervolume 1.771e+04 (+73.9%).

**LLM decision:** `refine` — Only `pipelined` is feasible: unrolled_k (max 26.8 MSPS) and pipelined_m (max 171 MSPS) both fall far short of the 250 MSPS constraint, and `iterative` (1 result per N+3 cycles) would need Fmax ≈ 250·(N+3) ≥ 1750 MHz, which is unreachable — so no budget should be spent there. The front is entirely pipelined and the selection rule is min LUTs, so the decisive region is the low-LUT corner: the cheapest front point is data_width=17/n_iter=15/angle_guard=3/frac_guard=2/round at 985 LUTs, 13.4 bits, 264 MSPS. The feasible data_width range starts at 16 and n_iter at 15, yet data_width=16 never appears on the front, so there may be cheaper feasible designs just below the current corner. Refining tightly there (while keeping enough breadth to preserve HV) is the highest-value use of this round; the reserved map_front pass can follow in the final round.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.771e+04 (gain this round: +73.9%).
Feasible designs: 91 of 200 evaluations (82 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 36% violate; best seen 273
- max_abs_err <= 0.00012207: 32% violate; best seen 8.5e-08 (2^-23.49)

Pareto front (feasible, 17 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] luts=985, accuracy_bits=13.4, ffs=978, throughput_msps=264, max_abs_err=9.31e-05 (2^-13.39), power_index=18.5
- pipelined [data_width=20 n_iter=15 angle_guard=3 frac_guard=2 rounding=trunc] luts=1082, accuracy_bits=13.8, ffs=1112, throughput_msps=257, max_abs_err=6.78e-05 (2^-13.85), power_index=20.6
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] luts=1104, accuracy_bits=14.3, ffs=1096, throughput_msps=264, max_abs_err=4.95e-05 (2^-14.30), power_index=20.7
- pipelined [data_width=22 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round] luts=1128, accuracy_bits=14.7, ffs=1162, throughput_msps=264, max_abs_err=3.88e-05 (2^-14.65), power_index=21.5
- pipelined [data_width=20 n_iter=17 angle_guard=3 frac_guard=3 rounding=trunc] luts=1270, accuracy_bits=15.5, ffs=1291, throughput_msps=257, max_abs_err=2.19e-05 (2^-15.48), power_index=24.1
- pipelined [data_width=22 n_iter=19 angle_guard=-1 frac_guard=3 rounding=trunc] luts=1466, accuracy_bits=16, ffs=1483, throughput_msps=257, max_abs_err=1.52e-05 (2^-16.01), power_index=27.7
- pipelined [data_width=22 n_iter=19 angle_guard=3 frac_guard=2 rounding=trunc] luts=1504, accuracy_bits=17.3, ffs=1525, throughput_msps=257, max_abs_err=6.37e-06 (2^-17.26), power_index=28.5
- pipelined [data_width=24 n_iter=19 angle_guard=2 frac_guard=2 rounding=trunc] luts=1599, accuracy_bits=17.8, ffs=1621, throughput_msps=257, max_abs_err=4.48e-06 (2^-17.77), power_index=30.3
- pipelined [data_width=23 n_iter=22 angle_guard=3 frac_guard=1 rounding=round] luts=1824, accuracy_bits=19, ffs=1796, throughput_msps=257, max_abs_err=1.84e-06 (2^-19.05), power_index=34
- pipelined [data_width=23 n_iter=27 angle_guard=3 frac_guard=3 rounding=round] luts=2355, accuracy_bits=20.3, ffs=2305, throughput_msps=257, max_abs_err=7.87e-07 (2^-20.28), power_index=43.8
Front coverage: luts 985..2355 (HV reference 4000); accuracy_bits 13.4..20.3 (HV reference 13); data_width on the front 17..24 (registry 8..28).

Per family:
- unrolled_k: 5 evals, 0 feasible; max throughput seen 26.8 MSPS; best accuracy 6.95 bits
- pipelined: 155 evals, 91 feasible; max throughput seen 273 MSPS; best accuracy 23.49 bits; best feasible luts=985; feasible ranges: data_width 16..24, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 40 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 16.84 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Refine the sole feasible family around its min-LUT corner, where the selection rule picks, while retaining enough range to keep the accuracy end of the front populated.*)
- `pipelined` (100 evals): data_width=16..21, n_iter=14..20, angle_guard=1..4, frac_guard=0..3, rounding=trunc|round. *Why:* Pipelined is the only family meeting 250 MSPS; concentrate on the low-LUT corner (data_width 16-21, n_iter 14-20) around the 985-LUT front point to find cheaper feasible designs, since selection is min LUTs.

**Result (code):** 100 evaluations this round, 300 total; 170 feasible; hypervolume 1.786e+04 (+0.8%).

**LLM decision:** `map_front` — Only `pipelined` is viable: `unrolled_k` and `pipelined_m` produced 0 feasible designs (max throughput 26.8 and 171 MSPS, both under the 250 MSPS floor), and `iterative` cannot reach 250 MSPS by construction (N+3 cycles/result, so even N=4 needs ~7x the clock). So the front is pipelined-only and there is nothing to gain from `add_family`. The current front spans luts 985..2355 against an HV reference of 4000 and accuracy_bits 13.4..20.3 against a best-seen 23.49 bits — i.e. it covers only part of both objective ranges, leaving a large unfilled region (luts 2355..4000) that higher-accuracy pipelined designs would populate. With 300/400 evals used and this being the final round, the reserved budget is best spent letting NSGA-II map the full pipelined ranges seeded with the existing 36-point front, rather than narrowing (which would only polish the already-solid min-luts corner at 985) or widening (ranges are already effectively saturated: feasible data_width 16..24, n_iter 15..30, angle_guard -2..4, frac_guard 0..4).

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.786e+04 (gain this round: +0.8%).
Feasible designs: 170 of 300 evaluations (143 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 24% violate; best seen 273
- max_abs_err <= 0.00012207: 28% violate; best seen 8.5e-08 (2^-23.49)

Pareto front (feasible, 36 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] luts=985, accuracy_bits=13.4, ffs=978, throughput_msps=264, max_abs_err=9.31e-05 (2^-13.39), power_index=18.5
- pipelined [data_width=18 n_iter=15 angle_guard=3 frac_guard=3 rounding=round] luts=1061, accuracy_bits=13.7, ffs=1049, throughput_msps=264, max_abs_err=7.32e-05 (2^-13.74), power_index=19.8
- pipelined [data_width=22 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round] luts=1128, accuracy_bits=14.7, ffs=1162, throughput_msps=264, max_abs_err=3.88e-05 (2^-14.65), power_index=21.5
- pipelined [data_width=19 n_iter=17 angle_guard=4 frac_guard=2 rounding=trunc] luts=1202, accuracy_bits=14.9, ffs=1227, throughput_msps=257, max_abs_err=3.31e-05 (2^-14.88), power_index=22.8
- pipelined [data_width=19 n_iter=17 angle_guard=4 frac_guard=2 rounding=round] luts=1242, accuracy_bits=15.3, ffs=1229, throughput_msps=257, max_abs_err=2.4e-05 (2^-15.35), power_index=23.2
- pipelined [data_width=21 n_iter=18 angle_guard=1 frac_guard=2 rounding=trunc] luts=1331, accuracy_bits=16.1, ffs=1354, throughput_msps=257, max_abs_err=1.43e-05 (2^-16.10), power_index=25.2
- pipelined [data_width=20 n_iter=18 angle_guard=3 frac_guard=3 rounding=round] luts=1391, accuracy_bits=16.4, ffs=1370, throughput_msps=257, max_abs_err=1.19e-05 (2^-16.36), power_index=26
- pipelined [data_width=21 n_iter=19 angle_guard=2 frac_guard=1 rounding=round] luts=1434, accuracy_bits=16.7, ffs=1417, throughput_msps=257, max_abs_err=9.17e-06 (2^-16.74), power_index=26.8
- pipelined [data_width=24 n_iter=19 angle_guard=2 frac_guard=2 rounding=trunc] luts=1599, accuracy_bits=17.8, ffs=1621, throughput_msps=257, max_abs_err=4.48e-06 (2^-17.77), power_index=30.3
- pipelined [data_width=23 n_iter=27 angle_guard=3 frac_guard=3 rounding=round] luts=2355, accuracy_bits=20.3, ffs=2305, throughput_msps=257, max_abs_err=7.87e-07 (2^-20.28), power_index=43.8
Front coverage: luts 985..2355 (HV reference 4000); accuracy_bits 13.4..20.3 (HV reference 13); data_width on the front 17..24 (registry 8..28).

Per family:
- unrolled_k: 5 evals, 0 feasible; max throughput seen 26.8 MSPS; best accuracy 6.95 bits
- pipelined: 255 evals, 170 feasible; max throughput seen 273 MSPS; best accuracy 23.49 bits; best feasible luts=985; feasible ranges: data_width 16..24, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 40 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 16.84 bits
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined` (100 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (36 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 216 feasible; hypervolume 1.906e+04 (+6.8%).

**LLM decision:** `stop` — Budget is exhausted (400/400 evals, round 4 of 4) and the front is both feasible and well covered: 216 feasible designs (182 unique), 35 on the Pareto front spanning luts 985..2130 and accuracy_bits 13.4..20.7, with hypervolume 1.906e4 (+6.8% this round). Both constraints are satisfiable — best throughput seen 273 MSPS vs the 250 MSPS requirement, and best max_abs_err 8.5e-08 (2^-23.49) vs the 2^-13 limit — so `infeasible` is ruled out. The selection rule (min luts) is served by the front's cheapest point, pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] at 985 LUTs, 13.4 accuracy bits, 264 MSPS, max_abs_err 9.31e-05 (2^-13.39), which clears both constraints with margin. unrolled_k and pipelined_m were explored and produced 0 feasible designs (max throughput 26.8 and 171 MSPS), and the unexplored `iterative` family cannot reach 1 result/cycle at 250 MSPS, so no further family is worth adding. Stopping here.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.906e+04 (gain this round: +6.8%).
Feasible designs: 216 of 400 evaluations (182 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 29% violate; best seen 273
- max_abs_err <= 0.00012207: 25% violate; best seen 8.5e-08 (2^-23.49)

Pareto front (feasible, 35 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] luts=985, accuracy_bits=13.4, ffs=978, throughput_msps=264, max_abs_err=9.31e-05 (2^-13.39), power_index=18.5
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] luts=1104, accuracy_bits=14.3, ffs=1096, throughput_msps=264, max_abs_err=4.95e-05 (2^-14.30), power_index=20.7
- pipelined [data_width=20 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] luts=1201, accuracy_bits=14.8, ffs=1189, throughput_msps=257, max_abs_err=3.51e-05 (2^-14.80), power_index=22.5
- pipelined [data_width=18 n_iter=17 angle_guard=4 frac_guard=3 rounding=round] luts=1223, accuracy_bits=15, ffs=1208, throughput_msps=264, max_abs_err=3.03e-05 (2^-15.01), power_index=22.9
- pipelined [data_width=21 n_iter=18 angle_guard=2 frac_guard=0 rounding=round] luts=1277, accuracy_bits=15.9, ffs=1308, throughput_msps=257, max_abs_err=1.59e-05 (2^-15.94), power_index=24.3
- pipelined [data_width=21 n_iter=18 angle_guard=1 frac_guard=2 rounding=round] luts=1375, accuracy_bits=16.2, ffs=1356, throughput_msps=257, max_abs_err=1.31e-05 (2^-16.22), power_index=25.7
- pipelined [data_width=21 n_iter=18 angle_guard=4 frac_guard=2 rounding=round] luts=1429, accuracy_bits=16.6, ffs=1410, throughput_msps=257, max_abs_err=9.83e-06 (2^-16.64), power_index=26.7
- pipelined [data_width=22 n_iter=19 angle_guard=3 frac_guard=2 rounding=trunc] luts=1504, accuracy_bits=17.3, ffs=1525, throughput_msps=257, max_abs_err=6.37e-06 (2^-17.26), power_index=28.5
- pipelined [data_width=25 n_iter=20 angle_guard=1 frac_guard=1 rounding=round] luts=1740, accuracy_bits=18.7, ffs=1713, throughput_msps=257, max_abs_err=2.36e-06 (2^-18.69), power_index=32.5
- pipelined [data_width=26 n_iter=25 angle_guard=0 frac_guard=0 rounding=round] luts=2130, accuracy_bits=20.7, ffs=2144, throughput_msps=257, max_abs_err=6.06e-07 (2^-20.65), power_index=40.2
Front coverage: luts 985..2130 (HV reference 4000); accuracy_bits 13.4..20.7 (HV reference 13); data_width on the front 17..26 (registry 8..28).

Per family:
- unrolled_k: 5 evals, 0 feasible; max throughput seen 26.8 MSPS; best accuracy 6.95 bits
- pipelined: 355 evals, 216 feasible; max throughput seen 273 MSPS; best accuracy 23.49 bits; best feasible luts=985; feasible ranges: data_width 16..26, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 40 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 16.84 bits
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 27739 in, 15844 out
- provider-reported cost: $0.0113
- full prompts and replies: `llm_trace.jsonl`

