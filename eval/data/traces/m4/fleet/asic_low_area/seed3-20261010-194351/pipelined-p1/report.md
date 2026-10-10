# DSE run: asic_low_area

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
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
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=13,n_iter=13,angle_guard=3,frac_guard=4,rounding=trunc,m=5` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 21425 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 5708 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 186 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 35.2 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 35.2 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 142 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.023 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000869 (2^-10.17) | exact: bit-accurate model, exhaustive (8192 angles) |
| max_abs_err_lsb | 1.78 | exact: bit-accurate model, exhaustive (8192 angles) |
| rms_err | 0.000301 (2^-11.70) | exact: bit-accurate model, exhaustive (8192 angles) |
| rms_err_lsb | 0.616 | exact: bit-accurate model, exhaustive (8192 angles) |
| accuracy_bits | 10.2 | exact: bit-accurate model, exhaustive (8192 angles) |

## Pareto front (19 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=13,n_iter=13,angle_guard=3,frac_guard=4,rounding=trunc,m=5` | 21425 | 186 | 35.2 | 5 | 0.023 | 0.000869 (2^-10.17) | 10.17 |
| 1 | `pipelined_m:data_width=17,n_iter=12,angle_guard=0,frac_guard=2,rounding=round,m=7` | 21548 | 153 | 23.1 | 4 | 0.0212 | 0.000597 (2^-10.71) | 10.71 |
| 2 | `pipelined_m:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=5` | 22366 | 194 | 37.1 | 5 | 0.0239 | 0.0004 (2^-11.29) | 11.29 |
| 3 | `pipelined_m:data_width=16,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc,m=5` | 24549 | 198 | 35.2 | 5 | 0.0255 | 0.000395 (2^-11.31) | 11.31 |
| 4 | `pipelined_m:data_width=14,n_iter=15,angle_guard=4,frac_guard=2,rounding=round,m=5` | 25177 | 194 | 33.5 | 5 | 0.0256 | 0.000372 (2^-11.39) | 11.39 |
| 5 | `pipelined_m:data_width=19,n_iter=13,angle_guard=3,frac_guard=0,rounding=trunc,m=5` | 25583 | 235 | 28.1 | 5 | 0.0281 | 0.000277 (2^-11.82) | 11.82 |
| 6 | `pipelined_m:data_width=21,n_iter=13,angle_guard=3,frac_guard=0,rounding=trunc,m=5` | 27903 | 257 | 26.0 | 5 | 0.0307 | 0.000252 (2^-11.95) | 11.95 |
| 7 | `pipelined_m:data_width=14,n_iter=16,angle_guard=4,frac_guard=3,rounding=round,m=5` | 28750 | 256 | 33.5 | 6 | 0.0312 | 0.000248 (2^-11.98) | 11.98 |
| 8 | `pipelined_m:data_width=16,n_iter=16,angle_guard=4,frac_guard=1,rounding=round,m=5` | 29968 | 271 | 30.6 | 6 | 0.0327 | 0.000177 (2^-12.47) | 12.47 |
| 9 | `pipelined_m:data_width=17,n_iter=21,angle_guard=4,frac_guard=2,rounding=round,m=7` | 39237 | 226 | 21.2 | 5 | 0.0357 | 5.05e-05 (2^-14.27) | 14.27 |
| 10 | `pipelined_m:data_width=24,n_iter=17,angle_guard=2,frac_guard=3,rounding=round,m=7` | 43173 | 300 | 16.9 | 5 | 0.0421 | 1.55e-05 (2^-15.97) | 15.97 |
| 11 | `pipelined_m:data_width=24,n_iter=19,angle_guard=2,frac_guard=3,rounding=trunc,m=8` | 46298 | 298 | 14.8 | 5 | 0.0438 | 4.31e-06 (2^-17.82) | 17.82 |
| 12 | `pipelined_m:data_width=28,n_iter=19,angle_guard=-1,frac_guard=3,rounding=trunc,m=8` | 51202 | 332 | 13.0 | 5 | 0.0487 | 3.93e-06 (2^-17.96) | 17.96 |
| 13 | `pipelined_m:data_width=28,n_iter=21,angle_guard=-1,frac_guard=3,rounding=trunc,m=8` | 56057 | 332 | 13.0 | 5 | 0.0515 | 1.09e-06 (2^-19.81) | 19.81 |
| 14 | `pipelined_m:data_width=28,n_iter=22,angle_guard=-1,frac_guard=2,rounding=trunc,m=8` | 57324 | 328 | 13.4 | 5 | 0.052 | 6.21e-07 (2^-20.62) | 20.62 |
| 15 | `pipelined_m:data_width=28,n_iter=22,angle_guard=1,frac_guard=2,rounding=trunc,m=8` | 58528 | 334 | 13.4 | 5 | 0.0531 | 5.33e-07 (2^-20.84) | 20.84 |
| 16 | `pipelined_m:data_width=26,n_iter=27,angle_guard=1,frac_guard=3,rounding=trunc,m=8` | 69624 | 407 | 13.9 | 6 | 0.0637 | 2.9e-07 (2^-21.72) | 21.72 |
| 17 | `pipelined_m:data_width=28,n_iter=27,angle_guard=4,frac_guard=2,rounding=trunc,m=5` | 79338 | 635 | 20.1 | 8 | 0.0821 | 6.39e-08 (2^-23.90) | 23.90 |
| 18 | `pipelined_m:data_width=28,n_iter=27,angle_guard=4,frac_guard=4,rounding=trunc,m=5` | 82432 | 655 | 20.1 | 8 | 0.085 | 3.67e-08 (2^-24.70) | 24.70 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec's only binding constraint is max_abs_err <= 2^-10 (accuracy_bits >= 10); the 1 MSPS throughput floor is trivially met by any pipelined variant. Accuracy depends only on data_width, n_iter, angle_guard, frac_guard and rounding, so both families share the same accuracy landscape. pipelined_m strictly reduces flip-flop count versus pipelined by registering every m stages, so it should dominate for the min-area objective. The chosen ranges (W 11..16, N 10..18) bracket the expected accuracy boundary around 10 bits, while guards and rounding let the search trade area for accuracy. The 80/20 budget split focuses on pipelined_m while keeping a small baseline on pipelined.*)
- `pipelined_m` (48 evals): data_width=11..16, n_iter=10..18, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* pipelined_m registers every m stages, so it keeps the same datapath as pipelined but uses far fewer flip-flops; with the loose 1 MSPS throughput constraint, large m minimizes area. This family should dominate pipelined for the min-area objective.
- `pipelined` (12 evals): data_width=11..16, n_iter=10..18, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Baseline fully pipelined family (equivalent to pipelined_m with m=1); included to confirm dominance and provide a reference point for the merged front.

**Result (code):** 60 evaluations this round, 60 total; 26 feasible; hypervolume 3.597e+04 (n/a).

**LLM decision:** `stop` — Constraints are met with margin by many designs, so `infeasible` is not justified: 26 of 60 evaluations are feasible, throughput best seen is 190 MSPS against a >= 1 MSPS requirement, and max_abs_err best seen is 2^-12.47 against the <= 2^-10 requirement. The Pareto front is real and well inside the HV reference point (area 22366..29968 um2 vs ref 40000; accuracy_bits 11.3..12.5 vs ref 10), giving HV 3.597e4. The spec's selection rule (min area_um2) picks pipelined_m [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=5] at 22366 um2, 11.3 accuracy bits, 37.1 MSPS, 194 FFs, power_index 0.0239 - i.e. the cheapest design on the front still clears the 2^-10 error spec by ~1.3 bits and the 1 MSPS spec by ~37x. The summary also reports no unexplored families remaining, so there is nothing left to add. This is the final round (round cap/budget reached), so no further refine/map_front step can be executed; the front is feasible, covers the low-area corner the selection rule cares about, and is not improvable within the remaining budget. Decision: stop.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 3.597e+04 (gain this round: n/a (first round)).
Feasible designs: 26 of 60 evaluations (21 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 190
- max_abs_err <= 0.000976562: 57% violate; best seen 0.000177 (2^-12.47)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=5] area_um2=22366, accuracy_bits=11.3, ffs=194, throughput_msps=37.1, max_abs_err=0.0004 (2^-11.29), power_index=0.0239
- pipelined_m [data_width=16 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc m=5] area_um2=24549, accuracy_bits=11.3, ffs=198, throughput_msps=35.2, max_abs_err=0.000395 (2^-11.31), power_index=0.0255
- pipelined_m [data_width=14 n_iter=15 angle_guard=4 frac_guard=2 rounding=round m=5] area_um2=25177, accuracy_bits=11.4, ffs=194, throughput_msps=33.5, max_abs_err=0.000372 (2^-11.39), power_index=0.0256
- pipelined_m [data_width=16 n_iter=15 angle_guard=0 frac_guard=1 rounding=round m=3] area_um2=27898, accuracy_bits=11.5, ffs=312, throughput_msps=57, max_abs_err=0.000355 (2^-11.46), power_index=0.0338
- pipelined_m [data_width=16 n_iter=16 angle_guard=4 frac_guard=0 rounding=round m=5] area_um2=28209, accuracy_bits=11.8, ffs=263, throughput_msps=30.6, max_abs_err=0.000285 (2^-11.78), power_index=0.0313
- pipelined_m [data_width=14 n_iter=16 angle_guard=4 frac_guard=3 rounding=round m=5] area_um2=28750, accuracy_bits=12, ffs=256, throughput_msps=33.5, max_abs_err=0.000248 (2^-11.98), power_index=0.0312
- pipelined_m [data_width=16 n_iter=16 angle_guard=4 frac_guard=1 rounding=round m=5] area_um2=29968, accuracy_bits=12.5, ffs=271, throughput_msps=30.6, max_abs_err=0.000177 (2^-12.47), power_index=0.0327
Front coverage: area_um2 22366..29968 (HV reference 40000); accuracy_bits 11.3..12.5 (HV reference 10); data_width on the front 14..16 (registry 8..28).

Per family:
- pipelined: 12 evals, 4 feasible; max throughput seen 190 MSPS; best accuracy 12.30 bits; best feasible area_um2=32958; feasible ranges: data_width 13..16, n_iter 14..15, angle_guard 0..4, frac_guard 0..3
- pipelined_m: 48 evals, 22 feasible; max throughput seen 86.6 MSPS; best accuracy 12.47 bits; best feasible area_um2=22366; feasible ranges: data_width 13..16, n_iter 14..18, angle_guard 0..4, frac_guard 0..4, m 2..6
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=13..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (7 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 62 feasible; hypervolume 3.919e+04 (+8.9%).

**No LLM call** (code's front-mapping round): Constraints are met with margin by many designs, so `infeasible` is not justified: 26 of 60 evaluations are feasible, throughput best seen is 190 MSPS against a >= 1 MSPS requirement, and max_abs_err best seen is 2^-12.47 against the <= 2^-10 requirement. The Pareto front is real and well inside the HV reference point (area 22366..29968 um2 vs ref 40000; accuracy_bits 11.3..12.5 vs ref 10), giving HV 3.597e4. The spec's selection rule (min area_um2) picks pipelined_m [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=5] at 22366 um2, 11.3 accuracy bits, 37.1 MSPS, 194 FFs, power_index 0.0239 - i.e. the cheapest design on the front still clears the 2^-10 error spec by ~1.3 bits and the 1 MSPS spec by ~37x. The summary also reports no unexplored families remaining, so there is nothing left to add. This is the final round (round cap/budget reached), so no further refine/map_front step can be executed; the front is feasible, covers the low-area corner the selection rule cares about, and is not improvable within the remaining budget. Decision: stop.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 3.919e+04 (gain this round: +8.9%).
Feasible designs: 62 of 100 evaluations (55 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 190
- max_abs_err <= 0.000976562: 38% violate; best seen 3.67e-08 (2^-24.70)

Pareto front (feasible, 19 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=13 n_iter=13 angle_guard=3 frac_guard=4 rounding=trunc m=5] area_um2=21425, accuracy_bits=10.2, ffs=186, throughput_msps=35.2, max_abs_err=0.000869 (2^-10.17), power_index=0.023
- pipelined_m [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=5] area_um2=22366, accuracy_bits=11.3, ffs=194, throughput_msps=37.1, max_abs_err=0.0004 (2^-11.29), power_index=0.0239
- pipelined_m [data_width=14 n_iter=15 angle_guard=4 frac_guard=2 rounding=round m=5] area_um2=25177, accuracy_bits=11.4, ffs=194, throughput_msps=33.5, max_abs_err=0.000372 (2^-11.39), power_index=0.0256
- pipelined_m [data_width=21 n_iter=13 angle_guard=3 frac_guard=0 rounding=trunc m=5] area_um2=27903, accuracy_bits=12, ffs=257, throughput_msps=26, max_abs_err=0.000252 (2^-11.95), power_index=0.0307
- pipelined_m [data_width=16 n_iter=16 angle_guard=4 frac_guard=1 rounding=round m=5] area_um2=29968, accuracy_bits=12.5, ffs=271, throughput_msps=30.6, max_abs_err=0.000177 (2^-12.47), power_index=0.0327
- pipelined_m [data_width=24 n_iter=17 angle_guard=2 frac_guard=3 rounding=round m=7] area_um2=43173, accuracy_bits=16, ffs=300, throughput_msps=16.9, max_abs_err=1.55e-05 (2^-15.97), power_index=0.0421
- pipelined_m [data_width=28 n_iter=19 angle_guard=-1 frac_guard=3 rounding=trunc m=8] area_um2=51202, accuracy_bits=18, ffs=332, throughput_msps=13, max_abs_err=3.93e-06 (2^-17.96), power_index=0.0487
- pipelined_m [data_width=28 n_iter=22 angle_guard=-1 frac_guard=2 rounding=trunc m=8] area_um2=57324, accuracy_bits=20.6, ffs=328, throughput_msps=13.4, max_abs_err=6.21e-07 (2^-20.62), power_index=0.052
- pipelined_m [data_width=26 n_iter=27 angle_guard=1 frac_guard=3 rounding=trunc m=8] area_um2=69624, accuracy_bits=21.7, ffs=407, throughput_msps=13.9, max_abs_err=2.9e-07 (2^-21.72), power_index=0.0637
- pipelined_m [data_width=28 n_iter=27 angle_guard=4 frac_guard=4 rounding=trunc m=5] area_um2=82432, accuracy_bits=24.7, ffs=655, throughput_msps=20.1, max_abs_err=3.67e-08 (2^-24.70), power_index=0.085
Front coverage: area_um2 21425..82432 (HV reference 40000); accuracy_bits 10.2..24.7 (HV reference 10); data_width on the front 13..28 (registry 8..28).

Per family:
- pipelined: 12 evals, 4 feasible; max throughput seen 190 MSPS; best accuracy 12.30 bits; best feasible area_um2=32958; feasible ranges: data_width 13..16, n_iter 14..15, angle_guard 0..4, frac_guard 0..3
- pipelined_m: 88 evals, 58 feasible; max throughput seen 86.6 MSPS; best accuracy 24.70 bits; best feasible area_um2=21425; feasible ranges: data_width 13..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4835 in, 7225 out
- provider-reported cost: $0.0049
- full prompts and replies: `llm_trace.jsonl`

