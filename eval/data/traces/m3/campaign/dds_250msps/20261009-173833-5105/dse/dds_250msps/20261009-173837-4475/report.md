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
`pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts)

| metric | value | provenance |
|---|---|---|
| luts | 905 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 938 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 64.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 17.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000119 (2^-13.04) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 7.79 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 3.06e-05 (2^-14.99) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 2.01 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 17 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 100.3 dBc, SNR 87.3 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (29 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 905 | 938 | 264.5 | 17 | 17.3 | 0.000119 (2^-13.04) | 13.04 |
| 1 | `pipelined:data_width=19,n_iter=15,angle_guard=3,frac_guard=0,rounding=trunc` | 979 | 1014 | 264.5 | 17 | 18.7 | 0.000109 (2^-13.17) | 13.17 |
| 2 | `pipelined:data_width=18,n_iter=16,angle_guard=1,frac_guard=1,rounding=trunc` | 1001 | 1029 | 264.5 | 18 | 19.1 | 0.000104 (2^-13.23) | 13.23 |
| 3 | `pipelined:data_width=18,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 1033 | 1057 | 264.5 | 18 | 19.7 | 8.08e-05 (2^-13.60) | 13.60 |
| 4 | `pipelined:data_width=19,n_iter=15,angle_guard=4,frac_guard=1,rounding=round` | 1063 | 1057 | 256.5 | 17 | 19.9 | 7.38e-05 (2^-13.73) | 13.73 |
| 5 | `pipelined:data_width=19,n_iter=17,angle_guard=0,frac_guard=0,rounding=round` | 1067 | 1098 | 264.5 | 19 | 20.4 | 6.32e-05 (2^-13.95) | 13.95 |
| 6 | `pipelined:data_width=21,n_iter=16,angle_guard=-1,frac_guard=0,rounding=round` | 1080 | 1114 | 264.5 | 18 | 20.6 | 4.91e-05 (2^-14.31) | 14.31 |
| 7 | `pipelined:data_width=21,n_iter=16,angle_guard=-1,frac_guard=1,rounding=round` | 1156 | 1144 | 264.5 | 18 | 21.6 | 4.72e-05 (2^-14.37) | 14.37 |
| 8 | `pipelined:data_width=21,n_iter=16,angle_guard=0,frac_guard=1,rounding=round` | 1172 | 1160 | 264.5 | 18 | 21.9 | 4e-05 (2^-14.61) | 14.61 |
| 9 | `pipelined:data_width=20,n_iter=16,angle_guard=2,frac_guard=3,rounding=trunc` | 1175 | 1199 | 256.5 | 18 | 22.3 | 3.71e-05 (2^-14.72) | 14.72 |
| 10 | `pipelined:data_width=20,n_iter=18,angle_guard=0,frac_guard=0,rounding=round` | 1188 | 1217 | 264.5 | 20 | 22.6 | 3.54e-05 (2^-14.79) | 14.79 |
| 11 | `pipelined:data_width=23,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc` | 1222 | 1255 | 256.5 | 18 | 23.3 | 3.23e-05 (2^-14.92) | 14.92 |
| 12 | `pipelined:data_width=22,n_iter=16,angle_guard=1,frac_guard=1,rounding=round` | 1237 | 1225 | 256.5 | 18 | 23.2 | 3.23e-05 (2^-14.92) | 14.92 |
| 13 | `pipelined:data_width=23,n_iter=16,angle_guard=1,frac_guard=1,rounding=trunc` | 1238 | 1271 | 256.5 | 18 | 23.6 | 3.18e-05 (2^-14.94) | 14.94 |
| 14 | `pipelined:data_width=20,n_iter=17,angle_guard=2,frac_guard=2,rounding=round` | 1261 | 1246 | 264.5 | 19 | 23.6 | 2.23e-05 (2^-15.45) | 15.45 |
| 15 | `pipelined:data_width=21,n_iter=17,angle_guard=2,frac_guard=2,rounding=trunc` | 1270 | 1295 | 256.5 | 19 | 24.1 | 1.95e-05 (2^-15.65) | 15.65 |
| 16 | `pipelined:data_width=22,n_iter=18,angle_guard=-1,frac_guard=0,rounding=round` | 1277 | 1308 | 264.5 | 20 | 24.3 | 1.85e-05 (2^-15.72) | 15.72 |
| 17 | `pipelined:data_width=23,n_iter=17,angle_guard=1,frac_guard=0,rounding=trunc` | 1287 | 1321 | 256.5 | 19 | 24.5 | 1.83e-05 (2^-15.74) | 15.74 |
| 18 | `pipelined:data_width=22,n_iter=18,angle_guard=2,frac_guard=0,rounding=trunc` | 1331 | 1362 | 256.5 | 20 | 25.3 | 1.6e-05 (2^-15.93) | 15.93 |
| 19 | `pipelined:data_width=21,n_iter=18,angle_guard=3,frac_guard=1,rounding=round` | 1375 | 1360 | 256.5 | 20 | 25.7 | 1.19e-05 (2^-16.36) | 16.36 |
| 20 | `pipelined:data_width=22,n_iter=18,angle_guard=4,frac_guard=1,rounding=trunc` | 1403 | 1431 | 256.5 | 20 | 26.6 | 1.08e-05 (2^-16.49) | 16.49 |
| 21 | `pipelined:data_width=23,n_iter=19,angle_guard=1,frac_guard=0,rounding=round` | 1447 | 1476 | 256.5 | 21 | 27.5 | 5.76e-06 (2^-17.41) | 17.41 |
| 22 | `pipelined:data_width=25,n_iter=19,angle_guard=-1,frac_guard=1,rounding=trunc` | 1561 | 1587 | 256.5 | 21 | 29.6 | 5.1e-06 (2^-17.58) | 17.58 |
| 23 | `pipelined:data_width=23,n_iter=20,angle_guard=2,frac_guard=1,rounding=trunc` | 1587 | 1610 | 256.5 | 22 | 30.1 | 4.15e-06 (2^-17.88) | 17.88 |
| 24 | `pipelined:data_width=23,n_iter=21,angle_guard=1,frac_guard=0,rounding=round` | 1607 | 1631 | 256.5 | 23 | 30.5 | 3.03e-06 (2^-18.33) | 18.33 |
| 25 | `pipelined:data_width=25,n_iter=21,angle_guard=1,frac_guard=0,rounding=trunc` | 1733 | 1759 | 256.5 | 23 | 32.8 | 2.11e-06 (2^-18.86) | 18.86 |
| 26 | `pipelined:data_width=21,n_iter=25,angle_guard=4,frac_guard=4,rounding=round` | 2098 | 2054 | 256.5 | 27 | 39 | 2.06e-06 (2^-18.89) | 18.89 |
| 27 | `pipelined:data_width=24,n_iter=25,angle_guard=1,frac_guard=1,rounding=round` | 2104 | 2066 | 256.5 | 27 | 39.2 | 1.29e-06 (2^-19.57) | 19.57 |
| 28 | `pipelined:data_width=24,n_iter=25,angle_guard=1,frac_guard=2,rounding=round` | 2155 | 2113 | 256.5 | 27 | 40.1 | 1.06e-06 (2^-19.84) | 19.84 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Throughput >=250 MSPS with 1 sample/clock rules out iterative and unrolled_k (multi-cycle per result). Only pipelined and pipelined_m can deliver 1 result/cycle. Accuracy 2^-13 needs W>=~15 and N>=~14, so the min-LUT feasible point lies at the low-W, low-N boundary. Round 1 maps that boundary broadly; later rounds will refine and fill the front.*)
- `pipelined` (65 evals): data_width=14..20, n_iter=12..20, angle_guard=-2..2, frac_guard=0..2, rounding=round|trunc. *Why:* Only pipelined families give 1 result/cycle, needed for >=250 MSPS. This family has the shortest combinational path (register per micro-rotation) so best chance of Fmax>=250 MHz. Ranges cover the low-LUT corner where accuracy just meets 2^-13.
- `pipelined_m` (35 evals): data_width=14..20, n_iter=12..20, angle_guard=-2..2, frac_guard=0..2, rounding=round|trunc, m=2..3. *Why:* Same 1 result/cycle but fewer pipeline registers; may reduce area at the cost of Fmax. Small m (2-3) keeps combinational path short enough to plausibly meet 250 MHz. Check if it can reach lower LUTs than pipelined.

**Result (code):** 100 evaluations this round, 100 total; 31 feasible; hypervolume 9413 (n/a).

**LLM decision:** `map_front` — Only the `pipelined` family can meet the 250 MSPS constraint: `pipelined_m` topped out at 171 MSPS (its m-stage combinational path lowers Fmax), and `iterative`/`unrolled_k` need >=4 cycles/result (ceil(N/k)+3 with N>=4), so at the ~273 MHz Fmax the pipelined family reaches they would deliver <=68 MSPS — structurally infeasible, not worth budget. The feasible front is therefore entirely `pipelined`, spanning luts 905..1413 and accuracy_bits 13..16.4. Against the HV reference point (luts=4000, accuracy=13) the front sits far from the luts reference and covers only 13..16.4 of the achievable accuracy range (registry allows data_width up to 28 / n_iter up to 30), so the HV is dominated by the single high-accuracy point (1413, 16.4) and the low-lut corner is barely explored (data_width only 18..20). Both the selection rule (min luts) and HV want the front extended leftward (lower data_width, e.g. 16-17) and rightward (higher data_width/n_iter for more accuracy_bits). This is exactly the 'front covers a small part of an objective's range' case, so spend this round mapping the full pipelined front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 9413 (gain this round: n/a (first round)).
Feasible designs: 31 of 100 evaluations (22 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 35% violate; best seen 273
- max_abs_err <= 0.00012207: 52% violate; best seen 1.17e-05 (2^-16.38)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts=905, accuracy_bits=13, ffs=938, throughput_msps=264, max_abs_err=0.000119 (2^-13.04), power_index=17.3
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc] luts=1001, accuracy_bits=13.2, ffs=1029, throughput_msps=264, max_abs_err=0.000104 (2^-13.23), power_index=19.1
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts=1033, accuracy_bits=13.6, ffs=1057, throughput_msps=264, max_abs_err=8.08e-05 (2^-13.60), power_index=19.7
- pipelined [data_width=20 n_iter=16 angle_guard=-1 frac_guard=2 rounding=round] luts=1138, accuracy_bits=13.9, ffs=1124, throughput_msps=264, max_abs_err=6.6e-05 (2^-13.89), power_index=21.3
- pipelined [data_width=20 n_iter=18 angle_guard=0 frac_guard=0 rounding=round] luts=1188, accuracy_bits=14.8, ffs=1217, throughput_msps=264, max_abs_err=3.54e-05 (2^-14.79), power_index=22.6
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=2 rounding=round] luts=1261, accuracy_bits=15.5, ffs=1246, throughput_msps=264, max_abs_err=2.23e-05 (2^-15.45), power_index=23.6
- pipelined [data_width=20 n_iter=18 angle_guard=2 frac_guard=1 rounding=round] luts=1301, accuracy_bits=15.7, ffs=1287, throughput_msps=264, max_abs_err=1.89e-05 (2^-15.69), power_index=24.3
- pipelined [data_width=20 n_iter=19 angle_guard=2 frac_guard=2 rounding=trunc] luts=1371, accuracy_bits=15.9, ffs=1391, throughput_msps=264, max_abs_err=1.63e-05 (2^-15.90), power_index=26
- pipelined [data_width=20 n_iter=19 angle_guard=2 frac_guard=1 rounding=round] luts=1375, accuracy_bits=16, ffs=1359, throughput_msps=264, max_abs_err=1.51e-05 (2^-16.01), power_index=25.7
- pipelined [data_width=20 n_iter=19 angle_guard=2 frac_guard=2 rounding=round] luts=1413, accuracy_bits=16.4, ffs=1393, throughput_msps=264, max_abs_err=1.17e-05 (2^-16.38), power_index=26.4
Front coverage: luts 905..1413 (HV reference 4000); accuracy_bits 13..16.4 (HV reference 13); data_width on the front 18..20 (registry 8..28).

Per family:
- pipelined: 65 evals, 31 feasible; max throughput seen 273 MSPS; best accuracy 16.38 bits; best feasible luts=905; feasible ranges: data_width 18..20, n_iter 15..19, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 35 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.24 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined` (100 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (11 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 111 feasible; hypervolume 1.533e+04 (+62.8%).

**LLM decision:** `map_front` — Only `pipelined` can meet the 250 MSPS constraint: it is the sole family with 1 result/cycle, and it already reaches 264-273 MSPS, whereas `pipelined_m` produced 0/35 feasible designs (max 171 MSPS) and the two unexplored families have multi-cycle schedules by construction (iterative N+3 >= 7 cycles, unrolled_k ceil(N/k)+3 >= 4 cycles even at N=4,k=8), so even at an optimistic Fmax they cannot approach 250 MSPS - adding them would waste budget. The feasible front is therefore entirely pipelined, and it covers only luts 905..2098 against the HV reference of 4000 while feasible designs reach 22.76 accuracy bits but the front stops at 18.9 - i.e. the high-accuracy/higher-LUT part of the trade-off curve is unmapped. With 200 evals and 2 rounds left, this is the right moment to hand the round to the code-driven NSGA-II coverage search over the full pipelined ranges, seeded with the current 26-design front, to fill in the rest of the curve before the reserved mapping budget is spent.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.533e+04 (gain this round: +62.8%).
Feasible designs: 111 of 200 evaluations (92 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 24% violate; best seen 273
- max_abs_err <= 0.00012207: 30% violate; best seen 1.41e-07 (2^-22.76)

Pareto front (feasible, 26 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts=905, accuracy_bits=13, ffs=938, throughput_msps=264, max_abs_err=0.000119 (2^-13.04), power_index=17.3
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts=1033, accuracy_bits=13.6, ffs=1057, throughput_msps=264, max_abs_err=8.08e-05 (2^-13.60), power_index=19.7
- pipelined [data_width=21 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round] luts=1080, accuracy_bits=14.3, ffs=1114, throughput_msps=264, max_abs_err=4.91e-05 (2^-14.31), power_index=20.6
- pipelined [data_width=21 n_iter=16 angle_guard=0 frac_guard=1 rounding=round] luts=1172, accuracy_bits=14.6, ffs=1160, throughput_msps=264, max_abs_err=4e-05 (2^-14.61), power_index=21.9
- pipelined [data_width=21 n_iter=16 angle_guard=3 frac_guard=3 rounding=trunc] luts=1238, accuracy_bits=14.9, ffs=1263, throughput_msps=257, max_abs_err=3.3e-05 (2^-14.89), power_index=23.5
- pipelined [data_width=22 n_iter=18 angle_guard=-1 frac_guard=0 rounding=round] luts=1277, accuracy_bits=15.7, ffs=1308, throughput_msps=264, max_abs_err=1.85e-05 (2^-15.72), power_index=24.3
- pipelined [data_width=20 n_iter=19 angle_guard=2 frac_guard=1 rounding=round] luts=1375, accuracy_bits=16, ffs=1359, throughput_msps=264, max_abs_err=1.51e-05 (2^-16.01), power_index=25.7
- pipelined [data_width=22 n_iter=18 angle_guard=4 frac_guard=1 rounding=trunc] luts=1403, accuracy_bits=16.5, ffs=1431, throughput_msps=257, max_abs_err=1.08e-05 (2^-16.49), power_index=26.6
- pipelined [data_width=23 n_iter=20 angle_guard=1 frac_guard=2 rounding=round] luts=1655, accuracy_bits=18.1, ffs=1628, throughput_msps=257, max_abs_err=3.47e-06 (2^-18.13), power_index=30.9
- pipelined [data_width=21 n_iter=25 angle_guard=4 frac_guard=4 rounding=round] luts=2098, accuracy_bits=18.9, ffs=2054, throughput_msps=257, max_abs_err=2.06e-06 (2^-18.89), power_index=39
Front coverage: luts 905..2098 (HV reference 4000); accuracy_bits 13..18.9 (HV reference 13); data_width on the front 18..23 (registry 8..28).

Per family:
- pipelined: 165 evals, 111 feasible; max throughput seen 273 MSPS; best accuracy 22.76 bits; best feasible luts=905; feasible ranges: data_width 17..23, n_iter 15..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 35 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.24 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined` (100 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (26 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 300 total; 172 feasible; hypervolume 1.74e+04 (+13.5%).

**LLM decision:** `map_front` — Not infeasible: the pipelined family already yields 26 feasible designs, best luts=905 with max_abs_err=2^-13.04 and throughput 264 MSPS >= 250, so the spec is reachable. Do not spend the last round on iterative or unrolled_k: maximising throughput means maximising results/cycle, and those families are structurally one result per N+3 and one per ceil(N/k)+3 cycles, i.e. at best one result per 4 cycles (unrolled, k=8/N=4) or per 7 cycles (iterative, N=4). Since the fastest 1-result/cycle structure (pipelined) only reaches 273 MSPS in this model, a 4-cycle/result structure cannot reach the 250 MSPS constraint, so add_family would burn the remaining 100 evals on throughput-infeasible space. Do not widen either: pipelined_m was already given 35 evals and produced 0 feasible designs (max throughput 171 MSPS), confirming it cannot satisfy the throughput constraint in the explored ranges. The front is still narrow relative to the objective ranges: luts 905..2155 against HV ref 4000 (~39% coverage) and accuracy_bits 13..19.8, with data_width on the front spanning only 18..25 of the registry's 8..28. With one round (100 evals) left and hypervolume scored against the spec's reference point, the best use of the reserved budget is to map the whole front: NSGA-II over the full pipelined ranges (n_iter 4..30, data_width 8..28, angle_guard -2..4, frac_guard 0..4, both roundings) seeded with the current 26-design front, so code can fill in the low-LUT/throughput-limited corner below 905 LUTs and the high-accuracy tail beyond 19.8 bits.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.74e+04 (gain this round: +13.5%).
Feasible designs: 172 of 300 evaluations (142 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 28% violate; best seen 273
- max_abs_err <= 0.00012207: 22% violate; best seen 7.02e-08 (2^-23.76)

Pareto front (feasible, 26 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts=905, accuracy_bits=13, ffs=938, throughput_msps=264, max_abs_err=0.000119 (2^-13.04), power_index=17.3
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts=1033, accuracy_bits=13.6, ffs=1057, throughput_msps=264, max_abs_err=8.08e-05 (2^-13.60), power_index=19.7
- pipelined [data_width=21 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round] luts=1080, accuracy_bits=14.3, ffs=1114, throughput_msps=264, max_abs_err=4.91e-05 (2^-14.31), power_index=20.6
- pipelined [data_width=21 n_iter=16 angle_guard=0 frac_guard=1 rounding=round] luts=1172, accuracy_bits=14.6, ffs=1160, throughput_msps=264, max_abs_err=4e-05 (2^-14.61), power_index=21.9
- pipelined [data_width=23 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc] luts=1222, accuracy_bits=14.9, ffs=1255, throughput_msps=257, max_abs_err=3.23e-05 (2^-14.92), power_index=23.3
- pipelined [data_width=23 n_iter=17 angle_guard=1 frac_guard=0 rounding=trunc] luts=1287, accuracy_bits=15.7, ffs=1321, throughput_msps=257, max_abs_err=1.83e-05 (2^-15.74), power_index=24.5
- pipelined [data_width=19 n_iter=18 angle_guard=4 frac_guard=4 rounding=round] luts=1389, accuracy_bits=16.2, ffs=1366, throughput_msps=257, max_abs_err=1.35e-05 (2^-16.17), power_index=25.9
- pipelined [data_width=23 n_iter=19 angle_guard=1 frac_guard=0 rounding=round] luts=1447, accuracy_bits=17.4, ffs=1476, throughput_msps=257, max_abs_err=5.76e-06 (2^-17.41), power_index=27.5
- pipelined [data_width=25 n_iter=21 angle_guard=1 frac_guard=0 rounding=trunc] luts=1733, accuracy_bits=18.9, ffs=1759, throughput_msps=257, max_abs_err=2.11e-06 (2^-18.86), power_index=32.8
- pipelined [data_width=24 n_iter=25 angle_guard=1 frac_guard=2 rounding=round] luts=2155, accuracy_bits=19.8, ffs=2113, throughput_msps=257, max_abs_err=1.06e-06 (2^-19.84), power_index=40.1
Front coverage: luts 905..2155 (HV reference 4000); accuracy_bits 13..19.8 (HV reference 13); data_width on the front 18..25 (registry 8..28).

Per family:
- pipelined: 265 evals, 172 feasible; max throughput seen 273 MSPS; best accuracy 23.76 bits; best feasible luts=905; feasible ranges: data_width 17..25, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 35 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.24 bits
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined` (100 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (26 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 243 feasible; hypervolume 1.742e+04 (+0.1%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), and the spec is satisfiable: 243 of 400 evaluations are feasible, with a 29-design Pareto front spanning luts 905..2155 and accuracy_bits 13..19.8. The selection rule (min luts) is already met by pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] at luts=905, throughput_msps=264 (>=250) and max_abs_err=0.000119 (2^-13.04, <= 0.00012207), so no constraint is violated and the front is not infeasible. Hypervolume gain this round was only +0.1%, indicating the front has converged; the unexplored families (iterative, unrolled_k) are multi-cycle per result and cannot reach the 250 MSPS one-sample-per-clock requirement, and pipelined_m produced 0 feasible designs in 35 evals (max throughput 171 MSPS), so further exploration would not improve the min-luts corner.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.742e+04 (gain this round: +0.1%).
Feasible designs: 243 of 400 evaluations (201 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 25% violate; best seen 273
- max_abs_err <= 0.00012207: 20% violate; best seen 5.57e-08 (2^-24.10)

Pareto front (feasible, 29 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts=905, accuracy_bits=13, ffs=938, throughput_msps=264, max_abs_err=0.000119 (2^-13.04), power_index=17.3
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts=1033, accuracy_bits=13.6, ffs=1057, throughput_msps=264, max_abs_err=8.08e-05 (2^-13.60), power_index=19.7
- pipelined [data_width=21 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round] luts=1080, accuracy_bits=14.3, ffs=1114, throughput_msps=264, max_abs_err=4.91e-05 (2^-14.31), power_index=20.6
- pipelined [data_width=20 n_iter=16 angle_guard=2 frac_guard=3 rounding=trunc] luts=1175, accuracy_bits=14.7, ffs=1199, throughput_msps=257, max_abs_err=3.71e-05 (2^-14.72), power_index=22.3
- pipelined [data_width=22 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts=1237, accuracy_bits=14.9, ffs=1225, throughput_msps=257, max_abs_err=3.23e-05 (2^-14.92), power_index=23.2
- pipelined [data_width=22 n_iter=18 angle_guard=-1 frac_guard=0 rounding=round] luts=1277, accuracy_bits=15.7, ffs=1308, throughput_msps=264, max_abs_err=1.85e-05 (2^-15.72), power_index=24.3
- pipelined [data_width=21 n_iter=18 angle_guard=3 frac_guard=1 rounding=round] luts=1375, accuracy_bits=16.4, ffs=1360, throughput_msps=257, max_abs_err=1.19e-05 (2^-16.36), power_index=25.7
- pipelined [data_width=25 n_iter=19 angle_guard=-1 frac_guard=1 rounding=trunc] luts=1561, accuracy_bits=17.6, ffs=1587, throughput_msps=257, max_abs_err=5.1e-06 (2^-17.58), power_index=29.6
- pipelined [data_width=25 n_iter=21 angle_guard=1 frac_guard=0 rounding=trunc] luts=1733, accuracy_bits=18.9, ffs=1759, throughput_msps=257, max_abs_err=2.11e-06 (2^-18.86), power_index=32.8
- pipelined [data_width=24 n_iter=25 angle_guard=1 frac_guard=2 rounding=round] luts=2155, accuracy_bits=19.8, ffs=2113, throughput_msps=257, max_abs_err=1.06e-06 (2^-19.84), power_index=40.1
Front coverage: luts 905..2155 (HV reference 4000); accuracy_bits 13..19.8 (HV reference 13); data_width on the front 18..25 (registry 8..28).

Per family:
- pipelined: 365 evals, 243 feasible; max throughput seen 273 MSPS; best accuracy 24.10 bits; best feasible luts=905; feasible ranges: data_width 17..26, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 35 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.24 bits
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 28141 in, 18557 out
- provider-reported cost: $0.0165
- full prompts and replies: `llm_trace.jsonl`

