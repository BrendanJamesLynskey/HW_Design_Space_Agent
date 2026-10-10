# DSE run: asic_low_area

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
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
`pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 19953 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 5316 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 197 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 43.5 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 43.5 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 115 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.0227 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000661 (2^-10.56) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 10.8 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000209 (2^-12.22) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 3.43 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.6 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (14 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=0,rounding=round,m=4` | 19953 | 197 | 43.5 | 5 | 0.0227 | 0.000661 (2^-10.56) | 10.56 |
| 1 | `pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=4` | 20299 | 200 | 41.5 | 5 | 0.0231 | 0.000654 (2^-10.58) | 10.58 |
| 2 | `pipelined_m:data_width=17,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 22895 | 155 | 20.3 | 4 | 0.0221 | 0.0003 (2^-11.70) | 11.70 |
| 3 | `pipelined_m:data_width=18,n_iter=13,angle_guard=1,frac_guard=1,rounding=trunc,m=6` | 24379 | 222 | 26.8 | 5 | 0.0267 | 0.000294 (2^-11.73) | 11.73 |
| 4 | `pipelined_m:data_width=19,n_iter=13,angle_guard=0,frac_guard=2,rounding=trunc,m=8` | 24383 | 167 | 18.6 | 4 | 0.0237 | 0.000273 (2^-11.84) | 11.84 |
| 5 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=4` | 26062 | 263 | 41.5 | 6 | 0.03 | 0.000209 (2^-12.22) | 12.22 |
| 6 | `pipelined_m:data_width=19,n_iter=18,angle_guard=0,frac_guard=1,rounding=trunc,m=6` | 33472 | 230 | 25.7 | 5 | 0.0325 | 5.95e-05 (2^-14.04) | 14.04 |
| 7 | `pipelined_m:data_width=23,n_iter=16,angle_guard=3,frac_guard=1,rounding=trunc,m=6` | 37056 | 282 | 20.3 | 5 | 0.0375 | 3.15e-05 (2^-14.95) | 14.95 |
| 8 | `pipelined_m:data_width=24,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc,m=6` | 37997 | 290 | 20.3 | 5 | 0.0385 | 3.11e-05 (2^-14.97) | 14.97 |
| 9 | `pipelined_m:data_width=24,n_iter=18,angle_guard=2,frac_guard=1,rounding=trunc,m=6` | 42188 | 290 | 20.3 | 5 | 0.041 | 8.44e-06 (2^-16.85) | 16.85 |
| 10 | `pipelined_m:data_width=24,n_iter=22,angle_guard=2,frac_guard=2,rounding=round,m=8` | 53001 | 296 | 15.3 | 5 | 0.0477 | 1.01e-06 (2^-19.91) | 19.91 |
| 11 | `pipelined_m:data_width=25,n_iter=22,angle_guard=3,frac_guard=1,rounding=round,m=6` | 56242 | 391 | 19.0 | 6 | 0.0549 | 7.78e-07 (2^-20.29) | 20.29 |
| 12 | `pipelined_m:data_width=27,n_iter=22,angle_guard=3,frac_guard=4,rounding=trunc,m=6` | 62364 | 435 | 17.3 | 6 | 0.0609 | 5.21e-07 (2^-20.87) | 20.87 |
| 13 | `pipelined_m:data_width=27,n_iter=24,angle_guard=3,frac_guard=2,rounding=trunc,m=6` | 64760 | 423 | 17.8 | 6 | 0.0617 | 1.97e-07 (2^-22.28) | 22.28 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >=1 MSPS and <=2^-10 error with area as the primary objective. Only pipelined and pipelined_m produce 1 result/cycle, so throughput is governed by Fmax; both are viable. I focus on W=12-16 and N=10-14 because the 2^-10 error bound is tight enough that very small N/W will fail, but large N/W wastes area. Rounding is fixed to 'round' to maximize accuracy per bit, leaving the budget to explore the area/accuracy trade-off. The fully pipelined family gets the larger share since it has the shortest critical path (best Fmax per area), while pipelined_m with m=2-4 explores the area-reduction axis by removing some registers at the cost of a longer path.*)
- `pipelined` (36 evals): data_width=12..16, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* Fully pipelined gives 1 result/cycle so throughput scales with Fmax; moderate N (10-14) keeps the critical path short for high Fmax while meeting the 2^-10 error bound, and W=12-16 balances area against accuracy margin.
- `pipelined_m` (24 evals): data_width=12..16, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* Registering every m stages trades some area (fewer FFs) for a longer combinational path; m=2-4 lets the optimizer find the area/Fmax sweet spot that still clears 1 MSPS, mapping the area-accuracy trade-off curve.

**Result (code):** 60 evaluations this round, 60 total; 37 feasible; hypervolume 3.711e+04 (n/a).

**LLM decision:** `stop` — The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 19953 um^2) meets all constraints (throughput 43.5 MSPS >= 1, max_abs_err 0.000661 <= 0.000977). The front covers a reasonable range of accuracy (10.6 to 12.3 bits) against the reference (10 bits) and area (19953 to 39385 um^2) against the reference (40000 um^2). Since this is the final round, further exploration is not possible. The current front provides a clear trade-off curve for the selection rule (min area), which would pick the 19953 um^2 design.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 3.711e+04 (gain this round: n/a (first round)).
Feasible designs: 37 of 60 evaluations (27 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 38% violate; best seen 0.000204 (2^-12.26)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=0 rounding=round m=4] area_um2=19953, accuracy_bits=10.6, ffs=197, throughput_msps=43.5, max_abs_err=0.000661 (2^-10.56), power_index=0.0227
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=0 rounding=round m=4] area_um2=20299, accuracy_bits=10.6, ffs=200, throughput_msps=41.5, max_abs_err=0.000654 (2^-10.58), power_index=0.0231
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=1 rounding=round m=3] area_um2=23098, accuracy_bits=10.8, ffs=263, throughput_msps=54.3, max_abs_err=0.000568 (2^-10.78), power_index=0.0283
- pipelined_m [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=4] area_um2=23566, accuracy_bits=11.3, ffs=248, throughput_msps=45.8, max_abs_err=0.0004 (2^-11.29), power_index=0.0277
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] area_um2=24405, accuracy_bits=11.7, ffs=256, throughput_msps=41.5, max_abs_err=0.000294 (2^-11.73), power_index=0.0286
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=4] area_um2=26062, accuracy_bits=12.2, ffs=263, throughput_msps=41.5, max_abs_err=0.000209 (2^-12.22), power_index=0.03
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=39385, accuracy_bits=12.3, ffs=834, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=0.0695
Front coverage: area_um2 19953..39385 (HV reference 40000); accuracy_bits 10.6..12.3 (HV reference 10); data_width on the front 16..16 (registry 8..28).

Per family:
- pipelined: 36 evals, 18 feasible; max throughput seen 171 MSPS; best accuracy 12.26 bits; best feasible area_um2=31433; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 1..2, frac_guard 0..2
- pipelined_m: 24 evals, 19 feasible; max throughput seen 91.1 MSPS; best accuracy 12.22 bits; best feasible area_um2=19953; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (35 evals): data_width=15..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (6 front designs; box front_anchored)
- `pipelined` (5 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 75 feasible; hypervolume 5.287e+04 (+42.5%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 19953 um^2) meets all constraints (throughput 43.5 MSPS >= 1, max_abs_err 0.000661 <= 0.000977). The front covers a reasonable range of accuracy (10.6 to 12.3 bits) against the reference (10 bits) and area (19953 to 39385 um^2) against the reference (40000 um^2). Since this is the final round, further exploration is not possible. The current front provides a clear trade-off curve for the selection rule (min area), which would pick the 19953 um^2 design.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 5.287e+04 (gain this round: +42.5%).
Feasible designs: 75 of 100 evaluations (62 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 25% violate; best seen 1.97e-07 (2^-22.28)

Pareto front (feasible, 14 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=0 rounding=round m=4] area_um2=19953, accuracy_bits=10.6, ffs=197, throughput_msps=43.5, max_abs_err=0.000661 (2^-10.56), power_index=0.0227
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=0 rounding=round m=4] area_um2=20299, accuracy_bits=10.6, ffs=200, throughput_msps=41.5, max_abs_err=0.000654 (2^-10.58), power_index=0.0231
- pipelined_m [data_width=18 n_iter=13 angle_guard=1 frac_guard=1 rounding=trunc m=6] area_um2=24379, accuracy_bits=11.7, ffs=222, throughput_msps=26.8, max_abs_err=0.000294 (2^-11.73), power_index=0.0267
- pipelined_m [data_width=19 n_iter=13 angle_guard=0 frac_guard=2 rounding=trunc m=8] area_um2=24383, accuracy_bits=11.8, ffs=167, throughput_msps=18.6, max_abs_err=0.000273 (2^-11.84), power_index=0.0237
- pipelined_m [data_width=19 n_iter=18 angle_guard=0 frac_guard=1 rounding=trunc m=6] area_um2=33472, accuracy_bits=14, ffs=230, throughput_msps=25.7, max_abs_err=5.95e-05 (2^-14.04), power_index=0.0325
- pipelined_m [data_width=23 n_iter=16 angle_guard=3 frac_guard=1 rounding=trunc m=6] area_um2=37056, accuracy_bits=15, ffs=282, throughput_msps=20.3, max_abs_err=3.15e-05 (2^-14.95), power_index=0.0375
- pipelined_m [data_width=24 n_iter=18 angle_guard=2 frac_guard=1 rounding=trunc m=6] area_um2=42188, accuracy_bits=16.9, ffs=290, throughput_msps=20.3, max_abs_err=8.44e-06 (2^-16.85), power_index=0.041
- pipelined_m [data_width=24 n_iter=22 angle_guard=2 frac_guard=2 rounding=round m=8] area_um2=53001, accuracy_bits=19.9, ffs=296, throughput_msps=15.3, max_abs_err=1.01e-06 (2^-19.91), power_index=0.0477
- pipelined_m [data_width=27 n_iter=22 angle_guard=3 frac_guard=4 rounding=trunc m=6] area_um2=62364, accuracy_bits=20.9, ffs=435, throughput_msps=17.3, max_abs_err=5.21e-07 (2^-20.87), power_index=0.0609
- pipelined_m [data_width=27 n_iter=24 angle_guard=3 frac_guard=2 rounding=trunc m=6] area_um2=64760, accuracy_bits=22.3, ffs=423, throughput_msps=17.8, max_abs_err=1.97e-07 (2^-22.28), power_index=0.0617
Front coverage: area_um2 19953..64760 (HV reference 40000); accuracy_bits 10.6..22.3 (HV reference 10); data_width on the front 16..27 (registry 8..28).

Per family:
- pipelined: 41 evals, 22 feasible; max throughput seen 171 MSPS; best accuracy 20.28 bits; best feasible area_um2=31433; feasible ranges: data_width 14..23, n_iter 12..26, angle_guard 1..3, frac_guard 0..4
- pipelined_m: 59 evals, 53 feasible; max throughput seen 91.1 MSPS; best accuracy 22.28 bits; best feasible area_um2=19953; feasible ranges: data_width 14..27, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4869 in, 1022 out
- provider-reported cost: $0.0027
- full prompts and replies: `llm_trace.jsonl`

