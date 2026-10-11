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
`pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=3` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 28525 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 7599 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 328 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 135 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.75 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000148 (2^-12.72) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 4.86 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 4.29e-05 (2^-14.51) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.4 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.7 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (15 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=3` | 28525 | 328 | 51.9 | 7 | 1.75 | 0.000148 (2^-12.72) | 12.72 |
| 1 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=3` | 30327 | 338 | 51.9 | 7 | 1.83 | 0.00013 (2^-12.91) | 12.91 |
| 2 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=2,rounding=round,m=3` | 31217 | 346 | 51.9 | 7 | 1.88 | 0.000108 (2^-13.18) | 13.18 |
| 3 | `pipelined_m:data_width=17,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=3` | 34224 | 409 | 51.9 | 8 | 2.15 | 8.59e-05 (2^-13.51) | 13.51 |
| 4 | `pipelined_m:data_width=17,n_iter=25,angle_guard=2,frac_guard=2,rounding=round,m=3` | 52904 | 598 | 51.9 | 11 | 3.22 | 7.61e-05 (2^-13.68) | 13.68 |
| 5 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 48233 | 1020 | 132.4 | 18 | 4.26 | 6.45e-05 (2^-13.92) | 13.92 |
| 6 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 49611 | 1048 | 132.4 | 18 | 4.37 | 5.46e-05 (2^-14.16) | 14.16 |
| 7 | `pipelined:data_width=20,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 52310 | 1125 | 123.1 | 18 | 4.67 | 4.33e-05 (2^-14.50) | 14.50 |
| 8 | `pipelined:data_width=20,n_iter=16,angle_guard=4,frac_guard=2,rounding=round` | 55573 | 1174 | 115.0 | 18 | 4.9 | 3.44e-05 (2^-14.83) | 14.83 |
| 9 | `pipelined:data_width=20,n_iter=18,angle_guard=2,frac_guard=1,rounding=round` | 59407 | 1254 | 123.1 | 20 | 5.24 | 1.89e-05 (2^-15.69) | 15.69 |
| 10 | `pipelined:data_width=24,n_iter=18,angle_guard=1,frac_guard=1,rounding=round` | 68711 | 1449 | 111.3 | 20 | 6.05 | 8.36e-06 (2^-16.87) | 16.87 |
| 11 | `pipelined:data_width=24,n_iter=18,angle_guard=2,frac_guard=1,rounding=round` | 69539 | 1467 | 107.9 | 20 | 6.13 | 8.13e-06 (2^-16.91) | 16.91 |
| 12 | `pipelined:data_width=25,n_iter=18,angle_guard=1,frac_guard=3,rounding=round` | 74379 | 1565 | 101.6 | 20 | 6.54 | 7.94e-06 (2^-16.94) | 16.94 |
| 13 | `pipelined:data_width=20,n_iter=22,angle_guard=4,frac_guard=3,rounding=round` | 78686 | 1656 | 115.0 | 24 | 6.92 | 4.71e-06 (2^-17.70) | 17.70 |
| 14 | `pipelined:data_width=24,n_iter=22,angle_guard=1,frac_guard=3,rounding=round` | 88042 | 1850 | 104.7 | 24 | 7.74 | 1.27e-06 (2^-19.59) | 19.59 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show pipelined and pipelined_m are the only families producing feasible designs, with pipelined_m holding the best power_index (2.03) and pipelined dominating the front (11/14 designs). Since the spec requires 50 MSPS throughput and max_abs_err <= 2^-12, I focus on the accuracy/power trade-off region where both families are feasible. I narrow data_width to 14-18 (enough for 12-bit accuracy with margin), n_iter to 10-16 (sufficient iterations for 2^-12 error), and use rounding='round' to minimize error. For pipelined_m, I restrict m to 2-4 to balance register count (power) against latency. This concentrates the budget on the feasible region where the hypervolume will be maximized.*)
- `pipelined` (50 evals): data_width=14..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* pipelined is the dominant family (11 of 14 front designs, best power 3.66); focus on the low-power/accuracy trade-off region that meets 50 MSPS and 2^-12 error.
- `pipelined_m` (50 evals): data_width=14..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* pipelined_m already achieves the best power_index (2.03) by reducing register count; refine m and the accuracy knobs to map the low-power corner of the front.

**Result (code):** 100 evaluations this round, 100 total; 58 feasible; hypervolume 80.75 (n/a).

**LLM decision:** `refine` — The current Pareto front is dominated by `pipelined_m` designs with `m=3` and `data_width=17`, achieving a power_index as low as 1.75 while meeting the 50 MSPS throughput constraint (51.9 MSPS). The `pipelined` family is significantly more power-hungry (min 3.38) and has higher latency/area, making it less relevant for the primary objective of minimizing power. The accuracy constraint (max_abs_err <= 2^-12) is easily met by the current front (best 12.7 bits, worst on front 12.7 bits, all > 12 bits). To improve hypervolume, we should focus the search on the `pipelined_m` family where the best power efficiency lies. We will narrow the ranges to `data_width` 16-18, `n_iter` 14-16, `angle_guard` 0-2, `frac_guard` 0-2, and `m` 2-4 to explore the trade-off between power and accuracy more densely in this promising region. We will exclude `pipelined` as it is clearly inferior in power for this spec.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 80.75 (gain this round: n/a (first round)).
Feasible designs: 58 of 100 evaluations (32 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 14% violate; best seen 163
- max_abs_err <= 0.000244141: 39% violate; best seen 5.46e-05 (2^-14.16)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=3] power_index=1.75, accuracy_bits=12.7, area_um2=28525, ffs=328, throughput_msps=51.9, max_abs_err=0.000148 (2^-12.72)
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=3] power_index=1.83, accuracy_bits=12.9, area_um2=30327, ffs=338, throughput_msps=51.9, max_abs_err=0.00013 (2^-12.91)
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=3] power_index=1.88, accuracy_bits=13.2, area_um2=31217, ffs=346, throughput_msps=51.9, max_abs_err=0.000108 (2^-13.18)
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=3] power_index=2.15, accuracy_bits=13.5, area_um2=34224, ffs=409, throughput_msps=51.9, max_abs_err=8.59e-05 (2^-13.51)
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] power_index=4.19, accuracy_bits=13.5, area_um2=47501, ffs=1005, throughput_msps=138, max_abs_err=8.41e-05 (2^-13.54)
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] power_index=4.26, accuracy_bits=13.9, area_um2=48233, ffs=1020, throughput_msps=132, max_abs_err=6.45e-05 (2^-13.92)
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] power_index=4.37, accuracy_bits=14.2, area_um2=49611, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16)
Front coverage: power_index 1.75..4.37 (HV reference 40); accuracy_bits 12.7..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 50 evals, 38 feasible; max throughput seen 163 MSPS; best accuracy 14.16 bits; best feasible power_index=3.38; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 20 feasible; max throughput seen 78.8 MSPS; best accuracy 13.92 bits; best feasible power_index=1.75; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2, m 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Focus on pipelined_m to refine the power-accuracy trade-off in the most efficient region.*)
- `pipelined_m` (20 evals): data_width=16..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* pipelined_m with m=3 showed the best power_index (1.75) while meeting throughput. Narrowing ranges focuses the budget on the efficient region.

**Result (code):** 20 evaluations this round, 120 total; 70 feasible; hypervolume 80.75 (+0.0%).

**LLM decision:** `stop` — The feasible Pareto front is well-established and the constraints are met. The minimum power_index achieved is 1.75 (pipelined_m, data_width=17, n_iter=15, m=3), which satisfies the throughput constraint (51.9 MSPS >= 50) and the accuracy constraint (12.7 bits > 12 bits). The front spans a reasonable range of the trade-off space (power 1.75-4.37, accuracy 12.7-14.2 bits). Since this is the final round and the hypervolume gain in the last round was 0.0%, further exploration is unlikely to significantly improve the front. The selection rule (min power_index) picks the pipelined_m design with power_index=1.75, which is a valid and efficient solution for the battery-powered radio spec.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 80.75 (gain this round: +0.0%).
Feasible designs: 70 of 120 evaluations (38 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 16% violate; best seen 163
- max_abs_err <= 0.000244141: 37% violate; best seen 5.46e-05 (2^-14.16)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=3] power_index=1.75, accuracy_bits=12.7, area_um2=28525, ffs=328, throughput_msps=51.9, max_abs_err=0.000148 (2^-12.72)
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=3] power_index=1.83, accuracy_bits=12.9, area_um2=30327, ffs=338, throughput_msps=51.9, max_abs_err=0.00013 (2^-12.91)
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=3] power_index=1.88, accuracy_bits=13.2, area_um2=31217, ffs=346, throughput_msps=51.9, max_abs_err=0.000108 (2^-13.18)
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=3] power_index=2.15, accuracy_bits=13.5, area_um2=34224, ffs=409, throughput_msps=51.9, max_abs_err=8.59e-05 (2^-13.51)
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] power_index=4.19, accuracy_bits=13.5, area_um2=47501, ffs=1005, throughput_msps=138, max_abs_err=8.41e-05 (2^-13.54)
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] power_index=4.26, accuracy_bits=13.9, area_um2=48233, ffs=1020, throughput_msps=132, max_abs_err=6.45e-05 (2^-13.92)
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] power_index=4.37, accuracy_bits=14.2, area_um2=49611, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16)
Front coverage: power_index 1.75..4.37 (HV reference 40); accuracy_bits 12.7..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 50 evals, 38 feasible; max throughput seen 163 MSPS; best accuracy 14.16 bits; best feasible power_index=3.38; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 70 evals, 32 feasible; max throughput seen 78.8 MSPS; best accuracy 13.92 bits; best feasible power_index=1.75; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2, m 2..3
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (46 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)
- `pipelined` (34 evals): data_width=17..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 123 feasible; hypervolume 262.9 (+225.5%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and the constraints are met. The minimum power_index achieved is 1.75 (pipelined_m, data_width=17, n_iter=15, m=3), which satisfies the throughput constraint (51.9 MSPS >= 50) and the accuracy constraint (12.7 bits > 12 bits). The front spans a reasonable range of the trade-off space (power 1.75-4.37, accuracy 12.7-14.2 bits). Since this is the final round and the hypervolume gain in the last round was 0.0%, further exploration is unlikely to significantly improve the front. The selection rule (min power_index) picks the pipelined_m design with power_index=1.75, which is a valid and efficient solution for the battery-powered radio spec.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 262.9 (gain this round: +225.5%).
Feasible designs: 123 of 200 evaluations (72 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 21% violate; best seen 163
- max_abs_err <= 0.000244141: 24% violate; best seen 2.47e-07 (2^-21.95)

Pareto front (feasible, 15 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=3] power_index=1.75, accuracy_bits=12.7, area_um2=28525, ffs=328, throughput_msps=51.9, max_abs_err=0.000148 (2^-12.72)
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=3] power_index=1.88, accuracy_bits=13.2, area_um2=31217, ffs=346, throughput_msps=51.9, max_abs_err=0.000108 (2^-13.18)
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=3] power_index=2.15, accuracy_bits=13.5, area_um2=34224, ffs=409, throughput_msps=51.9, max_abs_err=8.59e-05 (2^-13.51)
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] power_index=4.26, accuracy_bits=13.9, area_um2=48233, ffs=1020, throughput_msps=132, max_abs_err=6.45e-05 (2^-13.92)
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] power_index=4.37, accuracy_bits=14.2, area_um2=49611, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16)
- pipelined [data_width=20 n_iter=16 angle_guard=4 frac_guard=2 rounding=round] power_index=4.9, accuracy_bits=14.8, area_um2=55573, ffs=1174, throughput_msps=115, max_abs_err=3.44e-05 (2^-14.83)
- pipelined [data_width=20 n_iter=18 angle_guard=2 frac_guard=1 rounding=round] power_index=5.24, accuracy_bits=15.7, area_um2=59407, ffs=1254, throughput_msps=123, max_abs_err=1.89e-05 (2^-15.69)
- pipelined [data_width=24 n_iter=18 angle_guard=2 frac_guard=1 rounding=round] power_index=6.13, accuracy_bits=16.9, area_um2=69539, ffs=1467, throughput_msps=108, max_abs_err=8.13e-06 (2^-16.91)
- pipelined [data_width=25 n_iter=18 angle_guard=1 frac_guard=3 rounding=round] power_index=6.54, accuracy_bits=16.9, area_um2=74379, ffs=1565, throughput_msps=102, max_abs_err=7.94e-06 (2^-16.94)
- pipelined [data_width=24 n_iter=22 angle_guard=1 frac_guard=3 rounding=round] power_index=7.74, accuracy_bits=19.6, area_um2=88042, ffs=1850, throughput_msps=105, max_abs_err=1.27e-06 (2^-19.59)
Front coverage: power_index 1.75..7.74 (HV reference 40); accuracy_bits 12.7..19.6 (HV reference 12); data_width on the front 17..25 (registry 8..28).

Per family:
- pipelined: 84 evals, 71 feasible; max throughput seen 163 MSPS; best accuracy 19.59 bits; best feasible power_index=3.38; feasible ranges: data_width 16..25, n_iter 14..26, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 116 evals, 52 feasible; max throughput seen 78.8 MSPS; best accuracy 21.95 bits; best feasible power_index=1.75; feasible ranges: data_width 16..18, n_iter 14..25, angle_guard 0..2, frac_guard 0..2, m 2..3
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7763 in, 1671 out
- provider-reported cost: $0.0047
- full prompts and replies: `llm_trace.jsonl`

