# DSE run: asic_power_50msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
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
`pipelined:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 38197 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10176 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 810 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 112 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 3.38 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000209 (2^-12.22) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.43 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 6.44e-05 (2^-13.92) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 1.06 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.2 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (33 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` | 38197 | 810 | 143.2 | 16 | 3.38 | 0.000209 (2^-12.22) | 12.22 |
| 1 | `pipelined:data_width=16,n_iter=14,angle_guard=4,frac_guard=1,rounding=round` | 39472 | 838 | 132.4 | 16 | 3.49 | 0.000203 (2^-12.26) | 12.26 |
| 2 | `pipelined:data_width=17,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` | 40437 | 873 | 137.6 | 16 | 3.62 | 0.000178 (2^-12.46) | 12.46 |
| 3 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` | 42125 | 893 | 132.4 | 16 | 3.72 | 0.000152 (2^-12.68) | 12.68 |
| 4 | `pipelined:data_width=16,n_iter=15,angle_guard=3,frac_guard=2,rounding=round` | 42934 | 908 | 137.6 | 17 | 3.79 | 0.000128 (2^-12.93) | 12.93 |
| 5 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 42933 | 929 | 132.4 | 17 | 3.85 | 0.000109 (2^-13.17) | 13.17 |
| 6 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=round` | 44494 | 942 | 137.6 | 17 | 3.93 | 0.000101 (2^-13.27) | 13.27 |
| 7 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=3,rounding=round` | 47060 | 993 | 127.5 | 17 | 4.15 | 8.94e-05 (2^-13.45) | 13.45 |
| 8 | `pipelined:data_width=18,n_iter=15,angle_guard=3,frac_guard=3,rounding=round` | 48430 | 1022 | 127.5 | 17 | 4.27 | 7.32e-05 (2^-13.74) | 13.74 |
| 9 | `pipelined:data_width=18,n_iter=16,angle_guard=3,frac_guard=1,rounding=round` | 48966 | 1036 | 127.5 | 18 | 4.32 | 6.51e-05 (2^-13.91) | 13.91 |
| 10 | `pipelined:data_width=18,n_iter=16,angle_guard=3,frac_guard=2,rounding=round` | 50343 | 1064 | 127.5 | 18 | 4.44 | 5.17e-05 (2^-14.24) | 14.24 |
| 11 | `pipelined:data_width=18,n_iter=17,angle_guard=4,frac_guard=1,rounding=round` | 52847 | 1118 | 123.1 | 19 | 4.66 | 4.97e-05 (2^-14.30) | 14.30 |
| 12 | `pipelined:data_width=22,n_iter=16,angle_guard=-1,frac_guard=1,rounding=trunc` | 53862 | 1160 | 118.9 | 18 | 4.81 | 3.88e-05 (2^-14.66) | 14.66 |
| 13 | `pipelined:data_width=21,n_iter=16,angle_guard=4,frac_guard=0,rounding=round` | 53949 | 1164 | 111.3 | 18 | 4.82 | 3.63e-05 (2^-14.75) | 14.75 |
| 14 | `pipelined:data_width=21,n_iter=16,angle_guard=4,frac_guard=1,rounding=round` | 56444 | 1194 | 111.3 | 18 | 4.98 | 3.39e-05 (2^-14.85) | 14.85 |
| 15 | `pipelined:data_width=20,n_iter=17,angle_guard=4,frac_guard=1,rounding=round` | 57629 | 1218 | 115.0 | 19 | 5.08 | 2.24e-05 (2^-15.45) | 15.45 |
| 16 | `pipelined:data_width=22,n_iter=17,angle_guard=0,frac_guard=2,rounding=round` | 60763 | 1281 | 115.0 | 19 | 5.35 | 1.98e-05 (2^-15.63) | 15.63 |
| 17 | `pipelined:data_width=22,n_iter=17,angle_guard=4,frac_guard=1,rounding=round` | 62410 | 1318 | 107.9 | 19 | 5.5 | 1.67e-05 (2^-15.87) | 15.87 |
| 18 | `pipelined:data_width=23,n_iter=17,angle_guard=3,frac_guard=2,rounding=round` | 65493 | 1381 | 107.9 | 19 | 5.77 | 1.57e-05 (2^-15.96) | 15.96 |
| 19 | `pipelined:data_width=26,n_iter=17,angle_guard=1,frac_guard=2,rounding=trunc` | 69733 | 1496 | 101.6 | 19 | 6.21 | 1.54e-05 (2^-15.99) | 15.99 |
| 20 | `pipelined:data_width=23,n_iter=20,angle_guard=-1,frac_guard=1,rounding=round` | 71769 | 1512 | 115.0 | 22 | 6.32 | 7.46e-06 (2^-17.03) | 17.03 |
| 21 | `pipelined:data_width=23,n_iter=20,angle_guard=2,frac_guard=0,rounding=trunc` | 71559 | 1534 | 111.3 | 22 | 6.37 | 6.2e-06 (2^-17.30) | 17.30 |
| 22 | `pipelined:data_width=26,n_iter=20,angle_guard=1,frac_guard=1,rounding=round` | 82065 | 1728 | 104.7 | 22 | 7.22 | 2.11e-06 (2^-18.85) | 18.85 |
| 23 | `pipelined:data_width=26,n_iter=20,angle_guard=1,frac_guard=2,rounding=round` | 83821 | 1764 | 101.6 | 22 | 7.37 | 2.05e-06 (2^-18.89) | 18.89 |
| 24 | `pipelined:data_width=26,n_iter=20,angle_guard=3,frac_guard=1,rounding=round` | 83909 | 1768 | 98.8 | 22 | 7.38 | 2.01e-06 (2^-18.92) | 18.92 |
| 25 | `pipelined:data_width=26,n_iter=21,angle_guard=1,frac_guard=1,rounding=trunc` | 84836 | 1813 | 104.7 | 23 | 7.54 | 1.23e-06 (2^-19.63) | 19.63 |
| 26 | `pipelined:data_width=24,n_iter=21,angle_guard=4,frac_guard=3,rounding=round` | 86901 | 1828 | 101.6 | 23 | 7.64 | 1.22e-06 (2^-19.64) | 19.64 |
| 27 | `pipelined:data_width=26,n_iter=21,angle_guard=3,frac_guard=2,rounding=round` | 89999 | 1894 | 98.8 | 23 | 7.91 | 1.04e-06 (2^-19.87) | 19.87 |
| 28 | `pipelined:data_width=26,n_iter=22,angle_guard=1,frac_guard=3,rounding=round` | 94245 | 1980 | 98.8 | 24 | 8.28 | 6.23e-07 (2^-20.62) | 20.62 |
| 29 | `pipelined:data_width=26,n_iter=23,angle_guard=1,frac_guard=1,rounding=round` | 94496 | 1988 | 104.7 | 25 | 8.31 | 4.43e-07 (2^-21.11) | 21.11 |
| 30 | `pipelined:data_width=26,n_iter=23,angle_guard=1,frac_guard=2,rounding=round` | 96537 | 2029 | 101.6 | 25 | 8.48 | 4.28e-07 (2^-21.16) | 21.16 |
| 31 | `pipelined:data_width=25,n_iter=27,angle_guard=4,frac_guard=1,rounding=round` | 111020 | 2334 | 98.8 | 29 | 9.76 | 3.9e-07 (2^-21.29) | 21.29 |
| 32 | `pipelined:data_width=26,n_iter=27,angle_guard=1,frac_guard=1,rounding=round` | 111071 | 2334 | 104.7 | 29 | 9.76 | 3.7e-07 (2^-21.37) | 21.37 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *iterative and unrolled_k produced zero feasible designs (they cannot hit 50 MSPS), so they are excluded. pipelined already dominates the merged front with 22/22 designs, confirming it is the right family for the throughput constraint. The key trade-off is power_index vs accuracy_bits: I narrow n_iter to 12-16 and data_width to 14-18 because these are the parameters that jointly determine whether max_abs_err <= 2^-12 is met. Below these ranges, accuracy fails; above them, power/area grows without accuracy benefit. I split the budget 50/50 between pipelined and pipelined_m: pipelined to refine the known-feasible region and map the accuracy boundary precisely, and pipelined_m to explore whether reduced register density (larger m) yields lower power_index at the same accuracy, which would shift the Pareto front toward the power-minimum corner that the selection rule targets. Keeping angle_guard and frac_guard in full ranges ensures the search can find the minimal guard-bit configurations that still satisfy the error constraint, which is critical for minimizing power.*)
- `pipelined` (50 evals): data_width=14..18, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* The only family with feasible points (77/100) and the entire current merged front. The 50 MSPS constraint forces pipelined throughput (1 result/cycle). To minimize power_index (the selection rule) while keeping max_abs_err <= 2^-12, I focus on the minimal n_iter/data_width that satisfy accuracy. n_iter 12-16 and data_width 14-18 cover the accuracy boundary: too few iterations or too narrow width fails the 2^-12 error constraint, while going higher only increases area/power without improving accuracy_bits beyond the constraint. angle_guard and frac_guard are kept in their full ranges because they directly affect the error budget and thus the minimum viable n_iter/data_width combination.
- `pipelined_m` (50 evals): data_width=14..18, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* pipelined_m registers every m stages, reducing flip-flop count and potentially power_index versus fully pipelined, while still delivering 1 result/cycle to meet 50 MSPS. The same accuracy-determining parameters (n_iter, data_width, angle_guard, frac_guard, rounding) are constrained identically to pipelined since accuracy is family-independent. m is searched 2-4: m=2 halves the register count vs pipelined, m=4 quarters it, but larger m increases combinational depth per stage which may lower Fmax and hurt throughput. This trade-off between register savings and timing is exactly where the power/accuracy Pareto front for this family lives.

**Result (code):** 100 evaluations this round, 100 total; 18 feasible; hypervolume 80.33 (n/a).

**LLM decision:** `refine` — The `pipelined` family is the only one meeting the 50 MSPS throughput constraint (best 171 MSPS vs `pipelined_m` max 86.6 MSPS, which is borderline but yielded 0 feasible designs in Round 1, likely due to area/power/accuracy trade-offs or specific parameter combinations not yet optimized for throughput). The current Pareto front is clustered in a narrow region: data_width 16-18, n_iter 14-16, power_index 3.38-4.44. The accuracy constraint (<= 2^-12) is tight, with 82% of evaluations violating it, suggesting that higher n_iter or specific guard bits are critical. The `pipelined_m` family failed to produce feasible designs, likely because its throughput (max 86.6 MSPS) is too close to the 50 MSPS limit to allow for the necessary accuracy/area trade-offs, or its power/area overheads are too high. To improve the hypervolume and find a better minimum power design, we should focus the search on the `pipelined` family, narrowing the ranges to the promising region identified (data_width 16-18, n_iter 14-16) while allowing slight expansion in guard bits to explore accuracy/power trade-offs more densely. We will drop `pipelined_m` as it appears inefficient for this high-throughput, low-power spec.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 80.33 (gain this round: n/a (first round)).
Feasible designs: 18 of 100 evaluations (12 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 25% violate; best seen 171
- max_abs_err <= 0.000244141: 82% violate; best seen 5.17e-05 (2^-14.24)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] power_index=3.38, accuracy_bits=12.2, area_um2=38197, ffs=810, throughput_msps=143, max_abs_err=0.000209 (2^-12.22)
- pipelined [data_width=16 n_iter=14 angle_guard=4 frac_guard=1 rounding=round] power_index=3.49, accuracy_bits=12.3, area_um2=39472, ffs=838, throughput_msps=132, max_abs_err=0.000203 (2^-12.26)
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] power_index=3.62, accuracy_bits=12.5, area_um2=40437, ffs=873, throughput_msps=138, max_abs_err=0.000178 (2^-12.46)
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] power_index=3.72, accuracy_bits=12.7, area_um2=42125, ffs=893, throughput_msps=132, max_abs_err=0.000152 (2^-12.68)
- pipelined [data_width=18 n_iter=14 angle_guard=4 frac_guard=1 rounding=round] power_index=3.84, accuracy_bits=12.7, area_um2=43401, ffs=920, throughput_msps=123, max_abs_err=0.000146 (2^-12.75)
- pipelined [data_width=18 n_iter=14 angle_guard=4 frac_guard=2 rounding=round] power_index=3.94, accuracy_bits=12.8, area_um2=44589, ffs=944, throughput_msps=123, max_abs_err=0.000136 (2^-12.85)
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] power_index=4.44, accuracy_bits=14.2, area_um2=50343, ffs=1064, throughput_msps=128, max_abs_err=5.17e-05 (2^-14.24)
Front coverage: power_index 3.38..4.44 (HV reference 40); accuracy_bits 12.2..14.2 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 50 evals, 18 feasible; max throughput seen 171 MSPS; best accuracy 14.24 bits; best feasible power_index=3.38; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 1..4, frac_guard 1..3
- pipelined_m: 50 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 11.93 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate remaining budget on the `pipelined` family's promising region to refine the Pareto front and minimize power index while maintaining accuracy and throughput.*)
- `pipelined` (20 evals): data_width=16..18, n_iter=14..16, angle_guard=1..4, frac_guard=0..3, rounding=trunc|round. *Why:* Focus on the only family meeting throughput constraints, narrowing to the region where feasible designs were found to densely map the power/accuracy trade-off.

**Result (code):** 20 evaluations this round, 120 total; 36 feasible; hypervolume 80.72 (+0.5%).

**LLM decision:** `stop` — The feasible Pareto front is well-established and meets all constraints. The minimum power_index is 3.38 (pipelined, W=16, N=14), which is significantly better than the HV reference of 40. The accuracy range on the front spans 12.2 to 14.2 bits, comfortably exceeding the constraint of 12 bits (max_abs_err <= 2^-12). The pipelined family dominates the front, with pipelined_m proving infeasible for the 50 MSPS throughput requirement (max 86.6 MSPS seen, but 0 feasible designs likely due to latency/area/power trade-offs at high throughput). The front covers the relevant trade-off space for the spec's objectives (min power, max accuracy) within the feasible region. Since this is the final round and the front is stable and comprehensive for the constraints, stopping is the appropriate action.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 80.72 (gain this round: +0.5%).
Feasible designs: 36 of 120 evaluations (28 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 21% violate; best seen 171
- max_abs_err <= 0.000244141: 70% violate; best seen 5.17e-05 (2^-14.24)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] power_index=3.38, accuracy_bits=12.2, area_um2=38197, ffs=810, throughput_msps=143, max_abs_err=0.000209 (2^-12.22)
- pipelined [data_width=16 n_iter=14 angle_guard=4 frac_guard=1 rounding=round] power_index=3.49, accuracy_bits=12.3, area_um2=39472, ffs=838, throughput_msps=132, max_abs_err=0.000203 (2^-12.26)
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] power_index=3.62, accuracy_bits=12.5, area_um2=40437, ffs=873, throughput_msps=138, max_abs_err=0.000178 (2^-12.46)
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] power_index=3.72, accuracy_bits=12.7, area_um2=42125, ffs=893, throughput_msps=132, max_abs_err=0.000152 (2^-12.68)
- pipelined [data_width=16 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] power_index=3.79, accuracy_bits=12.9, area_um2=42934, ffs=908, throughput_msps=138, max_abs_err=0.000128 (2^-12.93)
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] power_index=3.93, accuracy_bits=13.3, area_um2=44494, ffs=942, throughput_msps=138, max_abs_err=0.000101 (2^-13.27)
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=3 rounding=round] power_index=4.15, accuracy_bits=13.4, area_um2=47060, ffs=993, throughput_msps=128, max_abs_err=8.94e-05 (2^-13.45)
- pipelined [data_width=18 n_iter=15 angle_guard=3 frac_guard=3 rounding=round] power_index=4.27, accuracy_bits=13.7, area_um2=48430, ffs=1022, throughput_msps=128, max_abs_err=7.32e-05 (2^-13.74)
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=1 rounding=round] power_index=4.32, accuracy_bits=13.9, area_um2=48966, ffs=1036, throughput_msps=128, max_abs_err=6.51e-05 (2^-13.91)
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] power_index=4.44, accuracy_bits=14.2, area_um2=50343, ffs=1064, throughput_msps=128, max_abs_err=5.17e-05 (2^-14.24)
Front coverage: power_index 3.38..4.44 (HV reference 40); accuracy_bits 12.2..14.2 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 70 evals, 36 feasible; max throughput seen 171 MSPS; best accuracy 14.24 bits; best feasible power_index=3.38; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 1..4, frac_guard 0..3
- pipelined_m: 50 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 11.93 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined` (80 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (11 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 108 feasible; hypervolume 316.8 (+292.5%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and meets all constraints. The minimum power_index is 3.38 (pipelined, W=16, N=14), which is significantly better than the HV reference of 40. The accuracy range on the front spans 12.2 to 14.2 bits, comfortably exceeding the constraint of 12 bits (max_abs_err <= 2^-12). The pipelined family dominates the front, with pipelined_m proving infeasible for the 50 MSPS throughput requirement (max 86.6 MSPS seen, but 0 feasible designs likely due to latency/area/power trade-offs at high throughput). The front covers the relevant trade-off space for the spec's objectives (min power, max accuracy) within the feasible region. Since this is the final round and the front is stable and comprehensive for the constraints, stopping is the appropriate action.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 316.8 (gain this round: +292.5%).
Feasible designs: 108 of 200 evaluations (93 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 12% violate; best seen 171
- max_abs_err <= 0.000244141: 46% violate; best seen 3.7e-07 (2^-21.37)

Pareto front (feasible, 33 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] power_index=3.38, accuracy_bits=12.2, area_um2=38197, ffs=810, throughput_msps=143, max_abs_err=0.000209 (2^-12.22)
- pipelined [data_width=16 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] power_index=3.79, accuracy_bits=12.9, area_um2=42934, ffs=908, throughput_msps=138, max_abs_err=0.000128 (2^-12.93)
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=3 rounding=round] power_index=4.15, accuracy_bits=13.4, area_um2=47060, ffs=993, throughput_msps=128, max_abs_err=8.94e-05 (2^-13.45)
- pipelined [data_width=18 n_iter=17 angle_guard=4 frac_guard=1 rounding=round] power_index=4.66, accuracy_bits=14.3, area_um2=52847, ffs=1118, throughput_msps=123, max_abs_err=4.97e-05 (2^-14.30)
- pipelined [data_width=21 n_iter=16 angle_guard=4 frac_guard=1 rounding=round] power_index=4.98, accuracy_bits=14.9, area_um2=56444, ffs=1194, throughput_msps=111, max_abs_err=3.39e-05 (2^-14.85)
- pipelined [data_width=23 n_iter=17 angle_guard=3 frac_guard=2 rounding=round] power_index=5.77, accuracy_bits=16, area_um2=65493, ffs=1381, throughput_msps=108, max_abs_err=1.57e-05 (2^-15.96)
- pipelined [data_width=23 n_iter=20 angle_guard=2 frac_guard=0 rounding=trunc] power_index=6.37, accuracy_bits=17.3, area_um2=71559, ffs=1534, throughput_msps=111, max_abs_err=6.2e-06 (2^-17.30)
- pipelined [data_width=26 n_iter=21 angle_guard=1 frac_guard=1 rounding=trunc] power_index=7.54, accuracy_bits=19.6, area_um2=84836, ffs=1813, throughput_msps=105, max_abs_err=1.23e-06 (2^-19.63)
- pipelined [data_width=26 n_iter=22 angle_guard=1 frac_guard=3 rounding=round] power_index=8.28, accuracy_bits=20.6, area_um2=94245, ffs=1980, throughput_msps=98.8, max_abs_err=6.23e-07 (2^-20.62)
- pipelined [data_width=26 n_iter=27 angle_guard=1 frac_guard=1 rounding=round] power_index=9.76, accuracy_bits=21.4, area_um2=111071, ffs=2334, throughput_msps=105, max_abs_err=3.7e-07 (2^-21.37)
Front coverage: power_index 3.38..9.76 (HV reference 40); accuracy_bits 12.2..21.4 (HV reference 12); data_width on the front 16..26 (registry 8..28).

Per family:
- pipelined: 150 evals, 108 feasible; max throughput seen 171 MSPS; best accuracy 21.37 bits; best feasible power_index=3.38; feasible ranges: data_width 16..26, n_iter 14..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 50 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 11.93 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7376 in, 2063 out
- provider-reported cost: $0.0046
- full prompts and replies: `llm_trace.jsonl`

