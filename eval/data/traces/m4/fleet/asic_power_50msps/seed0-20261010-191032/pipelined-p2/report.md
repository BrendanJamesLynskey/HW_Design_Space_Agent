# DSE run: asic_power_50msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_power_50msps: A 50 MSPS sin/cos unit in sky130 standard cells for a battery-powered radio: max error <= 2^-12. Minimise the relative power index; accuracy is the trade-off.
  target: asic-sky130hd
  constraint: throughput_msps >= 50
  constraint: max_abs_err <= 0.000244141
  objective: min power_index (HV ref 40)
  objective: max accuracy_bits (HV ref 12)
  select: min power_index
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=3` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 28058 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 7475 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 323 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 129 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.73 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000168 (2^-12.54) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 5.49 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 4.52e-05 (2^-14.43) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.48 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.5 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (30 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=3` | 28058 | 323 | 54.3 | 7 | 1.73 | 0.000168 (2^-12.54) | 12.54 |
| 1 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=3` | 29860 | 333 | 54.3 | 7 | 1.81 | 0.000158 (2^-12.63) | 12.63 |
| 2 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=3` | 29502 | 340 | 51.9 | 7 | 1.81 | 0.000119 (2^-13.04) | 13.04 |
| 3 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=3` | 31356 | 350 | 51.9 | 7 | 1.9 | 0.000101 (2^-13.27) | 13.27 |
| 4 | `pipelined_m:data_width=20,n_iter=18,angle_guard=1,frac_guard=4,rounding=trunc,m=2` | 48335 | 704 | 62.0 | 11 | 3.38 | 2.09e-05 (2^-15.55) | 15.55 |
| 5 | `pipelined:data_width=19,n_iter=19,angle_guard=2,frac_guard=2,rounding=round` | 61732 | 1302 | 127.5 | 21 | 5.44 | 1.92e-05 (2^-15.67) | 15.67 |
| 6 | `pipelined:data_width=20,n_iter=19,angle_guard=2,frac_guard=1,rounding=round` | 62745 | 1324 | 123.1 | 21 | 5.53 | 1.51e-05 (2^-16.01) | 16.01 |
| 7 | `pipelined:data_width=20,n_iter=19,angle_guard=2,frac_guard=2,rounding=round` | 64407 | 1358 | 123.1 | 21 | 5.67 | 1.17e-05 (2^-16.38) | 16.38 |
| 8 | `pipelined:data_width=23,n_iter=18,angle_guard=0,frac_guard=1,rounding=trunc` | 64132 | 1376 | 115.0 | 20 | 5.71 | 1.03e-05 (2^-16.57) | 16.57 |
| 9 | `pipelined:data_width=22,n_iter=18,angle_guard=2,frac_guard=2,rounding=round` | 66040 | 1392 | 115.0 | 20 | 5.81 | 9.56e-06 (2^-16.67) | 16.67 |
| 10 | `pipelined:data_width=21,n_iter=19,angle_guard=2,frac_guard=2,rounding=round` | 67082 | 1414 | 118.9 | 21 | 5.91 | 7.33e-06 (2^-17.06) | 17.06 |
| 11 | `pipelined:data_width=22,n_iter=19,angle_guard=2,frac_guard=2,rounding=trunc` | 68589 | 1468 | 115.0 | 21 | 6.1 | 6.37e-06 (2^-17.26) | 17.26 |
| 12 | `pipelined:data_width=23,n_iter=20,angle_guard=0,frac_guard=1,rounding=round` | 72691 | 1532 | 115.0 | 22 | 6.4 | 4.67e-06 (2^-17.71) | 17.71 |
| 13 | `pipelined:data_width=23,n_iter=20,angle_guard=1,frac_guard=1,rounding=round` | 73613 | 1551 | 115.0 | 22 | 6.48 | 3.86e-06 (2^-17.98) | 17.98 |
| 14 | `pipelined:data_width=26,n_iter=20,angle_guard=-1,frac_guard=0,rounding=trunc` | 77091 | 1652 | 107.9 | 22 | 6.86 | 2.63e-06 (2^-18.54) | 18.54 |
| 15 | `pipelined:data_width=24,n_iter=20,angle_guard=3,frac_guard=3,rounding=trunc` | 80518 | 1719 | 104.7 | 22 | 7.15 | 2.33e-06 (2^-18.71) | 18.71 |
| 16 | `pipelined:data_width=26,n_iter=20,angle_guard=3,frac_guard=0,rounding=trunc` | 80779 | 1730 | 98.8 | 22 | 7.19 | 2.31e-06 (2^-18.72) | 18.72 |
| 17 | `pipelined:data_width=28,n_iter=20,angle_guard=-1,frac_guard=0,rounding=trunc` | 82623 | 1770 | 101.6 | 22 | 7.35 | 2.09e-06 (2^-18.87) | 18.87 |
| 18 | `pipelined:data_width=26,n_iter=20,angle_guard=3,frac_guard=2,rounding=trunc` | 84293 | 1801 | 98.8 | 22 | 7.49 | 2.03e-06 (2^-18.91) | 18.91 |
| 19 | `pipelined:data_width=28,n_iter=20,angle_guard=0,frac_guard=1,rounding=trunc` | 85302 | 1825 | 98.8 | 22 | 7.58 | 1.99e-06 (2^-18.94) | 18.94 |
| 20 | `pipelined:data_width=27,n_iter=20,angle_guard=3,frac_guard=2,rounding=trunc` | 87059 | 1860 | 96.1 | 22 | 7.73 | 1.95e-06 (2^-18.97) | 18.97 |
| 21 | `pipelined:data_width=27,n_iter=23,angle_guard=-1,frac_guard=0,rounding=round` | 92147 | 1967 | 104.7 | 25 | 8.18 | 7.31e-07 (2^-20.38) | 20.38 |
| 22 | `pipelined:data_width=28,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc` | 92117 | 1968 | 101.6 | 24 | 8.18 | 6.32e-07 (2^-20.59) | 20.59 |
| 23 | `pipelined:data_width=27,n_iter=23,angle_guard=3,frac_guard=0,rounding=trunc` | 96403 | 2058 | 96.1 | 25 | 8.56 | 5e-07 (2^-20.93) | 20.93 |
| 24 | `pipelined:data_width=28,n_iter=23,angle_guard=0,frac_guard=1,rounding=round` | 99919 | 2101 | 98.8 | 25 | 8.78 | 3.34e-07 (2^-21.51) | 21.51 |
| 25 | `pipelined:data_width=28,n_iter=26,angle_guard=-1,frac_guard=0,rounding=trunc` | 108055 | 2301 | 101.6 | 28 | 9.58 | 2.99e-07 (2^-21.67) | 21.67 |
| 26 | `pipelined:data_width=26,n_iter=26,angle_guard=3,frac_guard=1,rounding=round` | 109340 | 2299 | 98.8 | 28 | 9.61 | 2.37e-07 (2^-22.01) | 22.01 |
| 27 | `pipelined:data_width=28,n_iter=24,angle_guard=0,frac_guard=4,rounding=trunc` | 109232 | 2320 | 91.1 | 26 | 9.67 | 2.1e-07 (2^-22.18) | 22.18 |
| 28 | `pipelined:data_width=28,n_iter=30,angle_guard=2,frac_guard=1,rounding=round` | 133375 | 2800 | 96.1 | 32 | 11.7 | 6.73e-08 (2^-23.82) | 23.82 |
| 29 | `pipelined:data_width=28,n_iter=30,angle_guard=3,frac_guard=1,rounding=round` | 134771 | 2829 | 93.5 | 32 | 11.8 | 5.72e-08 (2^-24.06) | 24.06 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Both allowed families compute identical bits, so accuracy is set purely by data_width, n_iter, angle_guard, frac_guard and rounding: max_abs_err<=2^-12 forces roughly W>=14 (output LSB 2^-(W-2)) and N>=12 (residual ~2^-N), which is why both families are searched from 14/12 upward rather than lower. The two objectives pull in opposite directions: accuracy wants more W/N (more logic and FFs), power wants fewer. The throughput>=50 MSPS constraint is the discriminator between families: pipelined (1 result/cycle, register per stage) clears it comfortably but pays in FFs, while pipelined_m trades Fmax for far fewer pipeline registers and already shows a much lower best power_index (2.77 vs 4.11) at the cost of feasibility. Since the selection rule is min power_index and hypervolume rewards covering the whole curve, I weight the budget toward pipelined_m (0.6) to map the low-power end and find the largest m that still meets 50 MSPS, and keep pipelined (0.4) to secure the feasible backbone and the high-accuracy end. Ranges are deliberately wide on W/N so the search can locate the accuracy boundary rather than assume it.*)
- `pipelined_m` (60 evals): data_width=14..22, n_iter=12..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* This is where the power win lives: the fleet already has a feasible pipelined_m point at power_index 2.77, well below pipelined's best 4.11, but only 3 of 41 evals were feasible, so the family is badly under-mapped. Registering every m stages cuts pipeline FFs (the dominant power term) as m grows, but stretches the combinational path and drops Fmax, so the throughput>=50 MSPS constraint is the binding one. Sweeping m=2..8 against W/N lets the search find the largest m that still clears 50 MSPS at each accuracy level, which is exactly the low-power end of the front. W>=14 and N>=12 are the floors implied by max_abs_err<=2^-12 (output LSB 2^-(W-2), residual ~2^-N); the upper ends let the search reach the higher-accuracy_bits region that also earns hypervolume above the ref point.
- `pipelined` (40 evals): data_width=14..22, n_iter=12..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* This family is the reliable feasible backbone (49 of 59 evals feasible, 5 of 8 merged-front points) and gives 1 result/cycle, so throughput_msps = Fmax and the >=50 MSPS constraint is easy to satisfy. Its role in this round is to (a) pin the accuracy ceiling of the front by pushing W and N up, and (b) provide the reference power/accuracy points that pipelined_m must beat. Keeping the same W/N/guard ranges as pipelined_m makes the two families directly comparable, so the only difference on the front is the register/power trade from m.

**Result (code):** 100 evaluations this round, 100 total; 38 feasible; hypervolume 189.6 (n/a).

**LLM decision:** `map_front` — The feasible front is narrow: power_index 2.32..6.1 and accuracy_bits 12.4..17.3, while the registry allows accuracy up to ~28 bits and the HV reference point is (40, 12). The HV is dominated by the high-accuracy end — the 17.3-bit point alone contributes roughly (40-6.1)*(17.3-12) ≈ 180 of the 189.6 total — so extending accuracy upward is where the remaining HV lies, and the low-power corner the selection rule picks (pipelined_m m=2, power_index=2.32) is already well covered. Only pipelined and pipelined_m are feasible (iterative/unrolled_k cannot reach 50 MSPS: N+3 or ceil(N/k)+3 cycles would demand Fmax far above what those datapaths achieve), and pipelined_m was feasible only at m=2. With 100 evals left in the final round, a code-driven NSGA-II coverage search over the full ranges of the two families on the front, seeded with the current front, is the best use of the budget to map the whole trade-off curve.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 189.6 (gain this round: n/a (first round)).
Feasible designs: 38 of 100 evaluations (36 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 42% violate; best seen 156
- max_abs_err <= 0.000244141: 30% violate; best seen 4.31e-06 (2^-17.82)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=4 rounding=trunc m=2] power_index=2.32, accuracy_bits=12.4, area_um2=32856, ffs=487, throughput_msps=69.4, max_abs_err=0.000181 (2^-12.43)
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc m=2] power_index=2.56, accuracy_bits=13.2, area_um2=35202, ffs=549, throughput_msps=72.3, max_abs_err=0.000109 (2^-13.17)
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=4 rounding=trunc m=2] power_index=3.38, accuracy_bits=15.5, area_um2=48335, ffs=704, throughput_msps=62, max_abs_err=2.09e-05 (2^-15.55)
- pipelined [data_width=19 n_iter=19 angle_guard=2 frac_guard=2 rounding=round] power_index=5.44, accuracy_bits=15.7, area_um2=61732, ffs=1302, throughput_msps=128, max_abs_err=1.92e-05 (2^-15.67)
- pipelined [data_width=20 n_iter=19 angle_guard=2 frac_guard=1 rounding=round] power_index=5.53, accuracy_bits=16, area_um2=62745, ffs=1324, throughput_msps=123, max_abs_err=1.51e-05 (2^-16.01)
- pipelined [data_width=20 n_iter=19 angle_guard=2 frac_guard=2 rounding=round] power_index=5.67, accuracy_bits=16.4, area_um2=64407, ffs=1358, throughput_msps=123, max_abs_err=1.17e-05 (2^-16.38)
- pipelined [data_width=22 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] power_index=5.81, accuracy_bits=16.7, area_um2=66040, ffs=1392, throughput_msps=115, max_abs_err=9.56e-06 (2^-16.67)
- pipelined [data_width=21 n_iter=19 angle_guard=2 frac_guard=2 rounding=round] power_index=5.91, accuracy_bits=17.1, area_um2=67082, ffs=1414, throughput_msps=119, max_abs_err=7.33e-06 (2^-17.06)
- pipelined [data_width=22 n_iter=19 angle_guard=2 frac_guard=2 rounding=trunc] power_index=6.1, accuracy_bits=17.3, area_um2=68589, ffs=1468, throughput_msps=115, max_abs_err=6.37e-06 (2^-17.26)
Front coverage: power_index 2.32..6.1 (HV reference 40); accuracy_bits 12.4..17.3 (HV reference 12); data_width on the front 17..22 (registry 8..28).

Per family:
- pipelined: 40 evals, 34 feasible; max throughput seen 156 MSPS; best accuracy 17.26 bits; best feasible power_index=3.99; feasible ranges: data_width 17..22, n_iter 14..20, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 60 evals, 4 feasible; max throughput seen 82.5 MSPS; best accuracy 17.82 bits; best feasible power_index=2.32; feasible ranges: data_width 17..20, n_iter 14..22, angle_guard 1..2, frac_guard 0..4, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `pipelined_m` (7 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (3 front designs; box front_anchored)
- `pipelined` (13 evals): data_width=18..28, n_iter=16..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (6 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 51 feasible; hypervolume 345.3 (+82.1%).

**LLM decision:** `refine` — The HV of 345.3 is dominated by the high-accuracy end: with the reference power at 40, the top front point alone contributes (40-9.67)*(22.2-12)≈309 of the total, so raising accuracy above 22.2 bits is the single biggest HV lever — and it looks reachable, since the best design uses data_width=28 (output LSB 2^-26) but only n_iter=24 of the allowed 30 and angle_guard=0. At the same time the selection rule picks min power_index, and the 2.32 corner comes from pipelined_m with only m=2 explored (4 feasible designs, data_width 17..20), so smaller data_width (15-16) and m=3 may cut power further while still clearing 50 MSPS and 2^-12. The front also has a visible gap between power 2.56 and 5.44 that mid-range pipelined points can fill. No new family is flagged as unexplored, so I stay with the two families already on the front.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 345.3 (gain this round: +82.1%).
Feasible designs: 51 of 120 evaluations (49 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 41% violate; best seen 156
- max_abs_err <= 0.000244141: 27% violate; best seen 2.1e-07 (2^-22.18)

Pareto front (feasible, 14 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=4 rounding=trunc m=2] power_index=2.32, accuracy_bits=12.4, area_um2=32856, ffs=487, throughput_msps=69.4, max_abs_err=0.000181 (2^-12.43)
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc m=2] power_index=2.56, accuracy_bits=13.2, area_um2=35202, ffs=549, throughput_msps=72.3, max_abs_err=0.000109 (2^-13.17)
- pipelined [data_width=19 n_iter=19 angle_guard=2 frac_guard=2 rounding=round] power_index=5.44, accuracy_bits=15.7, area_um2=61732, ffs=1302, throughput_msps=128, max_abs_err=1.92e-05 (2^-15.67)
- pipelined [data_width=20 n_iter=19 angle_guard=2 frac_guard=1 rounding=round] power_index=5.53, accuracy_bits=16, area_um2=62745, ffs=1324, throughput_msps=123, max_abs_err=1.51e-05 (2^-16.01)
- pipelined [data_width=23 n_iter=18 angle_guard=0 frac_guard=1 rounding=trunc] power_index=5.71, accuracy_bits=16.6, area_um2=64132, ffs=1376, throughput_msps=115, max_abs_err=1.03e-05 (2^-16.57)
- pipelined [data_width=22 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] power_index=5.81, accuracy_bits=16.7, area_um2=66040, ffs=1392, throughput_msps=115, max_abs_err=9.56e-06 (2^-16.67)
- pipelined [data_width=22 n_iter=19 angle_guard=2 frac_guard=2 rounding=trunc] power_index=6.1, accuracy_bits=17.3, area_um2=68589, ffs=1468, throughput_msps=115, max_abs_err=6.37e-06 (2^-17.26)
- pipelined [data_width=23 n_iter=22 angle_guard=1 frac_guard=1 rounding=trunc] power_index=7.09, accuracy_bits=18.3, area_um2=79829, ffs=1705, throughput_msps=115, max_abs_err=3.16e-06 (2^-18.27)
- pipelined [data_width=26 n_iter=24 angle_guard=4 frac_guard=1 rounding=trunc] power_index=8.92, accuracy_bits=21, area_um2=100602, ffs=2143, throughput_msps=96.1, max_abs_err=4.63e-07 (2^-21.04)
- pipelined [data_width=28 n_iter=24 angle_guard=0 frac_guard=4 rounding=trunc] power_index=9.67, accuracy_bits=22.2, area_um2=109232, ffs=2320, throughput_msps=91.1, max_abs_err=2.1e-07 (2^-22.18)
Front coverage: power_index 2.32..9.67 (HV reference 40); accuracy_bits 12.4..22.2 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- pipelined: 53 evals, 47 feasible; max throughput seen 156 MSPS; best accuracy 22.18 bits; best feasible power_index=3.99; feasible ranges: data_width 17..28, n_iter 14..28, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 67 evals, 4 feasible; max throughput seen 82.5 MSPS; best accuracy 17.82 bits; best feasible power_index=2.32; feasible ranges: data_width 17..20, n_iter 14..22, angle_guard 1..2, frac_guard 0..4, m 2..2
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Refine the two families already on the front: pipelined_m for the min-power corner the selection rule targets, pipelined for the mid-front gap and the high-accuracy end that drives hypervolume.*)
- `pipelined_m` (36 evals): data_width=15..20, n_iter=13..18, angle_guard=-1..3, frac_guard=0..4, rounding=trunc|round, m=2..3. *Why:* Holds the min-power corner (2.32) that the selection rule picks; only m=2 was feasible so far, and data_width 15-16 with m=3 should lower power further while keeping throughput >=50 MSPS and accuracy >=12 bits.
- `pipelined` (44 evals): data_width=17..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Covers both the 2.56-5.44 power gap (data_width 17-22) and the high-accuracy end (data_width 24-28, n_iter up to 30) where HV is dominated; the current top point only uses n_iter=24 and angle_guard=0, so more iterations/guard bits should push accuracy past 22.2 bits.

**Result (code):** 80 evaluations this round, 200 total; 109 feasible; hypervolume 401.2 (+16.2%).

**LLM decision:** `stop` — Budget is exhausted (200/200 evals) and this is the final round, so no further exploration is possible. The run is not infeasible: 109/200 evaluations are feasible, and the Pareto front holds 30 feasible designs spanning power_index 1.73..11.8 and accuracy_bits 12.5..24.1, comfortably bracketing the HV reference point (power 40, accuracy 12). Both constraints are met with margin on the front: the throughput floor of 50 MSPS is satisfied by every front point (e.g. 54.3 MSPS at the low-power corner, up to 123 MSPS), and the error ceiling of 2^-12 is beaten everywhere (best front accuracy 2^-24.06, best seen overall 2^-24.06). The selection rule (min power_index) is served by the pipelined_m corner at power_index=1.73, accuracy_bits=12.5, 54.3 MSPS, max_abs_err=2^-12.54, which meets both constraints. Hypervolume is still improving (+16.2% this round), but with the evaluation budget fully spent and no rounds remaining, the front is the best achievable within the budget. Stopping here.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 401.2 (gain this round: +16.2%).
Feasible designs: 109 of 200 evaluations (98 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 32% violate; best seen 156
- max_abs_err <= 0.000244141: 20% violate; best seen 5.72e-08 (2^-24.06)

Pareto front (feasible, 30 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=1.73, accuracy_bits=12.5, area_um2=28058, ffs=323, throughput_msps=54.3, max_abs_err=0.000168 (2^-12.54)
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=3] power_index=1.9, accuracy_bits=13.3, area_um2=31356, ffs=350, throughput_msps=51.9, max_abs_err=0.000101 (2^-13.27)
- pipelined [data_width=20 n_iter=19 angle_guard=2 frac_guard=1 rounding=round] power_index=5.53, accuracy_bits=16, area_um2=62745, ffs=1324, throughput_msps=123, max_abs_err=1.51e-05 (2^-16.01)
- pipelined [data_width=21 n_iter=19 angle_guard=2 frac_guard=2 rounding=round] power_index=5.91, accuracy_bits=17.1, area_um2=67082, ffs=1414, throughput_msps=119, max_abs_err=7.33e-06 (2^-17.06)
- pipelined [data_width=23 n_iter=20 angle_guard=1 frac_guard=1 rounding=round] power_index=6.48, accuracy_bits=18, area_um2=73613, ffs=1551, throughput_msps=115, max_abs_err=3.86e-06 (2^-17.98)
- pipelined [data_width=26 n_iter=20 angle_guard=3 frac_guard=0 rounding=trunc] power_index=7.19, accuracy_bits=18.7, area_um2=80779, ffs=1730, throughput_msps=98.8, max_abs_err=2.31e-06 (2^-18.72)
- pipelined [data_width=28 n_iter=20 angle_guard=0 frac_guard=1 rounding=trunc] power_index=7.58, accuracy_bits=18.9, area_um2=85302, ffs=1825, throughput_msps=98.8, max_abs_err=1.99e-06 (2^-18.94)
- pipelined [data_width=27 n_iter=23 angle_guard=3 frac_guard=0 rounding=trunc] power_index=8.56, accuracy_bits=20.9, area_um2=96403, ffs=2058, throughput_msps=96.1, max_abs_err=5e-07 (2^-20.93)
- pipelined [data_width=26 n_iter=26 angle_guard=3 frac_guard=1 rounding=round] power_index=9.61, accuracy_bits=22, area_um2=109340, ffs=2299, throughput_msps=98.8, max_abs_err=2.37e-07 (2^-22.01)
- pipelined [data_width=28 n_iter=30 angle_guard=3 frac_guard=1 rounding=round] power_index=11.8, accuracy_bits=24.1, area_um2=134771, ffs=2829, throughput_msps=93.5, max_abs_err=5.72e-08 (2^-24.06)
Front coverage: power_index 1.73..11.8 (HV reference 40); accuracy_bits 12.5..24.1 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- pipelined: 97 evals, 91 feasible; max throughput seen 156 MSPS; best accuracy 24.06 bits; best feasible power_index=3.99; feasible ranges: data_width 17..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 103 evals, 18 feasible; max throughput seen 91.1 MSPS; best accuracy 17.82 bits; best feasible power_index=1.73; feasible ranges: data_width 17..20, n_iter 14..22, angle_guard 0..2, frac_guard 0..4, m 2..3
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 11995 in, 16354 out
- provider-reported cost: $0.0143
- full prompts and replies: `llm_trace.jsonl`

