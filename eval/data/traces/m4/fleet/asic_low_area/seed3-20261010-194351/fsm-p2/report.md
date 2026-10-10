# DSE run: asic_low_area

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_low_area: Motor-control sin/cos in sky130 standard cells: >= 1 MSPS, max error <= 2^-10. Area is everything: minimise cell area.
  target: asic-sky130hd
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min area_um2 (HV ref 40000)
  objective: max accuracy_bits (HV ref 10)
  select: min area_um2
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=15,n_iter=13,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 6870 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1830 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 98 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 147 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 9.22 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 108 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.152 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000879 (2^-10.15) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 7.2 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00022 (2^-12.15) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.8 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.2 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (16 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=13,angle_guard=0,frac_guard=0,rounding=round` | 6870 | 98 | 9.2 | 16 | 0.152 | 0.000879 (2^-10.15) | 10.15 |
| 1 | `iterative:data_width=15,n_iter=13,angle_guard=3,frac_guard=0,rounding=round` | 7060 | 102 | 8.2 | 16 | 0.157 | 0.000642 (2^-10.61) | 10.61 |
| 2 | `iterative:data_width=15,n_iter=14,angle_guard=3,frac_guard=0,rounding=round` | 7121 | 102 | 7.7 | 17 | 0.167 | 0.000546 (2^-10.84) | 10.84 |
| 3 | `iterative:data_width=15,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc` | 7396 | 105 | 8.5 | 16 | 0.163 | 0.000466 (2^-11.07) | 11.07 |
| 4 | `iterative:data_width=16,n_iter=18,angle_guard=0,frac_guard=0,rounding=round` | 7555 | 105 | 6.7 | 21 | 0.216 | 0.000373 (2^-11.39) | 11.39 |
| 5 | `iterative:data_width=16,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc` | 7933 | 111 | 7.3 | 18 | 0.195 | 0.000241 (2^-12.02) | 12.02 |
| 6 | `iterative:data_width=15,n_iter=14,angle_guard=3,frac_guard=3,rounding=round` | 9221 | 108 | 7.7 | 17 | 0.195 | 0.000215 (2^-12.18) | 12.18 |
| 7 | `iterative:data_width=15,n_iter=22,angle_guard=3,frac_guard=2,rounding=round` | 9279 | 107 | 5.2 | 25 | 0.286 | 0.000192 (2^-12.35) | 12.35 |
| 8 | `iterative:data_width=19,n_iter=21,angle_guard=4,frac_guard=1,rounding=trunc` | 9365 | 128 | 4.6 | 24 | 0.303 | 4.3e-05 (2^-14.50) | 14.50 |
| 9 | `iterative:data_width=22,n_iter=18,angle_guard=4,frac_guard=2,rounding=trunc` | 10909 | 147 | 4.8 | 21 | 0.306 | 9.31e-06 (2^-16.71) | 16.71 |
| 10 | `iterative:data_width=23,n_iter=18,angle_guard=3,frac_guard=2,rounding=trunc` | 11286 | 151 | 4.8 | 21 | 0.316 | 8.56e-06 (2^-16.83) | 16.83 |
| 11 | `iterative:data_width=24,n_iter=21,angle_guard=3,frac_guard=0,rounding=round` | 11557 | 152 | 4.1 | 24 | 0.366 | 1.9e-06 (2^-19.00) | 19.00 |
| 12 | `iterative:data_width=24,n_iter=21,angle_guard=3,frac_guard=2,rounding=trunc` | 12053 | 156 | 4.1 | 24 | 0.379 | 1.61e-06 (2^-19.24) | 19.24 |
| 13 | `iterative:data_width=23,n_iter=30,angle_guard=3,frac_guard=4,rounding=trunc` | 12753 | 155 | 3.0 | 33 | 0.533 | 1.09e-06 (2^-19.81) | 19.81 |
| 14 | `iterative:data_width=23,n_iter=30,angle_guard=4,frac_guard=4,rounding=trunc` | 12816 | 156 | 3.0 | 33 | 0.536 | 8.73e-07 (2^-20.13) | 20.13 |
| 15 | `iterative:data_width=26,n_iter=23,angle_guard=3,frac_guard=2,rounding=trunc` | 13213 | 167 | 3.6 | 26 | 0.444 | 4.05e-07 (2^-21.23) | 21.23 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Throughput is not binding (iterative already clears 1 MSPS by a wide margin), so the front is area-vs-accuracy_bits and the selection rule is min area. Because accuracy_bits depends only on data_width/n_iter/angle_guard/frac_guard/rounding, the shared-datapath iterative family is structurally the cheapest way to hit any given accuracy, which matches the fleet evidence (15/16 front points, best area 7042 um^2). I therefore spend most of this round refining iterative around the low-area feasible boundary (W 9-16, N 8-18, full guard/rounding sweep) to sharpen the knee and the accuracy tail, and keep a small share on unrolled_k to confirm it adds no non-dominated point.*)
- `iterative` (80 evals): data_width=9..16, n_iter=8..18, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Iterative owns 15/16 of the merged front and the best feasible area (7042 um^2); accuracy is a pure function of W/N/guards/rounding, so this family gives every accuracy point at the lowest area. Ranges bracket the feasible boundary (W~11-12, N~10-14) and extend upward to fill the accuracy end of the curve.
- `unrolled_k` (20 evals): data_width=9..16, n_iter=8..18, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..6. *Why:* Small share to verify whether any k-chained variant reaches an accuracy/area point iterative misses; since it computes identical bits at generally higher area, only a narrow k window is worth probing.

**Result (code):** 100 evaluations this round, 100 total; 34 feasible; hypervolume 7.958e+04 (n/a).

**LLM decision:** `map_front` — The feasible front is entirely `iterative` and covers only a sliver of the objectives: area_um2 6870..9433 against the HV reference 40000, and accuracy_bits 10.2..12.5 against a registry that allows far higher (data_width on the front is only 14..16 of 8..28). Because every feasible area is far below the 40000 reference, hypervolume is dominated by the accuracy axis, so extending accuracy_bits upward while area stays well under 40000 is where the remaining HV lies. The throughput constraint (>=1 MSPS) is already satisfied with huge margin (best 14.6, front points 6.7-9.2 MSPS), so the 1-result/cycle pipelined families buy nothing for this spec, and unrolled_k is dominated (its only feasible point is area 16893, far worse than 6870). With this being the final 100-eval round, the right move is to let code map the whole trade-off curve over the full parameter ranges of the family on the front (iterative), seeded with the current front, rather than refining a narrow box.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 7.958e+04 (gain this round: n/a (first round)).
Feasible designs: 34 of 100 evaluations (26 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14.6
- max_abs_err <= 0.000976562: 66% violate; best seen 0.000176 (2^-12.48)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] area_um2=6870, accuracy_bits=10.2, ffs=98, throughput_msps=9.22, max_abs_err=0.000879 (2^-10.15), power_index=0.152
- iterative [data_width=14 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7125, accuracy_bits=10.6, ffs=100, throughput_msps=7.86, max_abs_err=0.000648 (2^-10.59), power_index=0.175
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=7164, accuracy_bits=10.6, ffs=104, throughput_msps=8.32, max_abs_err=0.000643 (2^-10.60), power_index=0.17
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7396, accuracy_bits=11.1, ffs=105, throughput_msps=8.5, max_abs_err=0.000466 (2^-11.07), power_index=0.163
- iterative [data_width=16 n_iter=18 angle_guard=0 frac_guard=0 rounding=round] area_um2=7555, accuracy_bits=11.4, ffs=105, throughput_msps=6.74, max_abs_err=0.000373 (2^-11.39), power_index=0.216
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7933, accuracy_bits=12, ffs=111, throughput_msps=7.27, max_abs_err=0.000241 (2^-12.02), power_index=0.195
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=9433, accuracy_bits=12.5, ffs=111, throughput_msps=7.27, max_abs_err=0.000176 (2^-12.48), power_index=0.211
Front coverage: area_um2 6870..9433 (HV reference 40000); accuracy_bits 10.2..12.5 (HV reference 10); data_width on the front 14..16 (registry 8..28).

Per family:
- iterative: 80 evals, 33 feasible; max throughput seen 14.6 MSPS; best accuracy 12.48 bits; best feasible area_um2=6870; feasible ranges: data_width 14..16, n_iter 12..18, angle_guard 0..4, frac_guard 0..4
- unrolled_k: 20 evals, 1 feasible; max throughput seen 10.7 MSPS; best accuracy 10.28 bits; best feasible area_um2=16893; feasible ranges: data_width 15..15, n_iter 17..17, angle_guard 0..0, frac_guard 3..3, k 5..5
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `iterative` (20 evals): data_width=13..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (7 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 54 feasible; hypervolume 3.316e+05 (+316.7%).

**LLM decision:** `refine` — The front is entirely iterative and its low-area corner is under-explored: the smallest feasible design is 6870 um^2 at data_width=15, yet the registry allows data_width down to 8 and the front's data_width range is only 14..26 (registry 8..28). Since the selection rule is min area_um2 and the throughput constraint (>=1 MSPS, best seen 14.6) is easily met by iterative, the highest-value unexplored region is data_width 8..15 with enough n_iter/guards to still satisfy max_abs_err <= 2^-10. Symmetrically, the accuracy axis tops out at 21.2 bits while data_width=28/n_iter=30 could reach ~26 bits, so a small share should push the high-accuracy end to widen HV coverage. unrolled_k is not worth more budget (1 feasible of 20, best area 16893, worse than every iterative point), and pipelined/pipelined_m add per-stage registers, which cannot beat the shared iterative datapath on area.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 3.316e+05 (gain this round: +316.7%).
Feasible designs: 54 of 120 evaluations (44 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14.6
- max_abs_err <= 0.000976562: 55% violate; best seen 4.05e-07 (2^-21.23)

Pareto front (feasible, 14 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] area_um2=6870, accuracy_bits=10.2, ffs=98, throughput_msps=9.22, max_abs_err=0.000879 (2^-10.15), power_index=0.152
- iterative [data_width=14 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7125, accuracy_bits=10.6, ffs=100, throughput_msps=7.86, max_abs_err=0.000648 (2^-10.59), power_index=0.175
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7396, accuracy_bits=11.1, ffs=105, throughput_msps=8.5, max_abs_err=0.000466 (2^-11.07), power_index=0.163
- iterative [data_width=16 n_iter=18 angle_guard=0 frac_guard=0 rounding=round] area_um2=7555, accuracy_bits=11.4, ffs=105, throughput_msps=6.74, max_abs_err=0.000373 (2^-11.39), power_index=0.216
- iterative [data_width=19 n_iter=21 angle_guard=4 frac_guard=1 rounding=trunc] area_um2=9365, accuracy_bits=14.5, ffs=128, throughput_msps=4.6, max_abs_err=4.3e-05 (2^-14.50), power_index=0.303
- iterative [data_width=22 n_iter=18 angle_guard=4 frac_guard=2 rounding=trunc] area_um2=10909, accuracy_bits=16.7, ffs=147, throughput_msps=4.8, max_abs_err=9.31e-06 (2^-16.71), power_index=0.306
- iterative [data_width=24 n_iter=21 angle_guard=3 frac_guard=0 rounding=round] area_um2=11557, accuracy_bits=19, ffs=152, throughput_msps=4.08, max_abs_err=1.9e-06 (2^-19.00), power_index=0.366
- iterative [data_width=24 n_iter=21 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=12053, accuracy_bits=19.2, ffs=156, throughput_msps=4.08, max_abs_err=1.61e-06 (2^-19.24), power_index=0.379
- iterative [data_width=23 n_iter=30 angle_guard=4 frac_guard=4 rounding=trunc] area_um2=12816, accuracy_bits=20.1, ffs=156, throughput_msps=2.97, max_abs_err=8.73e-07 (2^-20.13), power_index=0.536
- iterative [data_width=26 n_iter=23 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=13213, accuracy_bits=21.2, ffs=167, throughput_msps=3.57, max_abs_err=4.05e-07 (2^-21.23), power_index=0.444
Front coverage: area_um2 6870..13213 (HV reference 40000); accuracy_bits 10.2..21.2 (HV reference 10); data_width on the front 14..26 (registry 8..28).

Per family:
- iterative: 100 evals, 53 feasible; max throughput seen 14.6 MSPS; best accuracy 21.23 bits; best feasible area_um2=6870; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 20 evals, 1 feasible; max throughput seen 10.7 MSPS; best accuracy 10.28 bits; best feasible area_um2=16893; feasible ranges: data_width 15..15, n_iter 17..17, angle_guard 0..0, frac_guard 3..3, k 5..5
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Refine around the two open ends of the front: the low-area corner (data_width 8..15) that the selection rule cares about, and the high-accuracy corner (data_width 24..28) that the hypervolume cares about, keeping the well-performing iterative family and dropping unrolled_k.*)
- `iterative` (80 evals): data_width=8..15, n_iter=8..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Selection is min area and the front's smallest point is 6870 um^2 at data_width=15; data_width 8..15 is unexplored and may hold smaller feasible designs that still meet max_abs_err <= 2^-10.
- clamped by code: dropped duplicate family iterative

**Result (code):** 80 evaluations this round, 200 total; 77 feasible; hypervolume 3.318e+05 (+0.0%).

**LLM decision:** `stop` — Final round and the 200-eval budget is fully spent (200/200), so no further search can be run. The front is already feasible and well-formed: a valid design exists that satisfies both constraints — iterative [d=15, n=13, ag=0, fg=0, round] at area 6870 um2 with throughput 9.22 MSPS (>= 1) and max_abs_err 8.79e-4 <= 9.766e-4 — so infeasible is not warranted. Coverage is good against the HV references: area_um2 spans 6870..13213 versus ref 40000, and accuracy_bits spans 10.2..21.2 versus ref 10, i.e. the front sits entirely inside the reference box rather than only in a corner. Gain this round was +0.0%, and the only unexplored-family signal (unrolled_k, 20 evals, 1 feasible, best area 16893) is dominated by the iterative front, which already spans data_width 15..26 across both accuracy and area. The selection rule (min area_um2) picks the 6870 um2 design, which is constraint-feasible. Stopping is therefore the correct action.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 3.318e+05 (gain this round: +0.0%).
Feasible designs: 77 of 200 evaluations (60 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 16.1
- max_abs_err <= 0.000976562: 62% violate; best seen 4.05e-07 (2^-21.23)

Pareto front (feasible, 16 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] area_um2=6870, accuracy_bits=10.2, ffs=98, throughput_msps=9.22, max_abs_err=0.000879 (2^-10.15), power_index=0.152
- iterative [data_width=15 n_iter=14 angle_guard=3 frac_guard=0 rounding=round] area_um2=7121, accuracy_bits=10.8, ffs=102, throughput_msps=7.7, max_abs_err=0.000546 (2^-10.84), power_index=0.167
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7396, accuracy_bits=11.1, ffs=105, throughput_msps=8.5, max_abs_err=0.000466 (2^-11.07), power_index=0.163
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7933, accuracy_bits=12, ffs=111, throughput_msps=7.27, max_abs_err=0.000241 (2^-12.02), power_index=0.195
- iterative [data_width=15 n_iter=22 angle_guard=3 frac_guard=2 rounding=round] area_um2=9279, accuracy_bits=12.3, ffs=107, throughput_msps=5.24, max_abs_err=0.000192 (2^-12.35), power_index=0.286
- iterative [data_width=19 n_iter=21 angle_guard=4 frac_guard=1 rounding=trunc] area_um2=9365, accuracy_bits=14.5, ffs=128, throughput_msps=4.6, max_abs_err=4.3e-05 (2^-14.50), power_index=0.303
- iterative [data_width=23 n_iter=18 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=11286, accuracy_bits=16.8, ffs=151, throughput_msps=4.8, max_abs_err=8.56e-06 (2^-16.83), power_index=0.316
- iterative [data_width=24 n_iter=21 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=12053, accuracy_bits=19.2, ffs=156, throughput_msps=4.08, max_abs_err=1.61e-06 (2^-19.24), power_index=0.379
- iterative [data_width=23 n_iter=30 angle_guard=3 frac_guard=4 rounding=trunc] area_um2=12753, accuracy_bits=19.8, ffs=155, throughput_msps=2.97, max_abs_err=1.09e-06 (2^-19.81), power_index=0.533
- iterative [data_width=26 n_iter=23 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=13213, accuracy_bits=21.2, ffs=167, throughput_msps=3.57, max_abs_err=4.05e-07 (2^-21.23), power_index=0.444
Front coverage: area_um2 6870..13213 (HV reference 40000); accuracy_bits 10.2..21.2 (HV reference 10); data_width on the front 15..26 (registry 8..28).

Per family:
- iterative: 180 evals, 76 feasible; max throughput seen 16.1 MSPS; best accuracy 21.23 bits; best feasible area_um2=6870; feasible ranges: data_width 13..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 20 evals, 1 feasible; max throughput seen 10.7 MSPS; best accuracy 10.28 bits; best feasible area_um2=16893; feasible ranges: data_width 15..15, n_iter 17..17, angle_guard 0..0, frac_guard 3..3, k 5..5
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 12363 in, 8344 out
- provider-reported cost: $0.0065
- full prompts and replies: `llm_trace.jsonl`

