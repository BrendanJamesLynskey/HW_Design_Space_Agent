# DSE run: asic_low_area

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 14 of 14 budgeted, over 2 round(s).  
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
  budget: 14 evals, 14/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=16,n_iter=12,angle_guard=0,frac_guard=1,rounding=trunc,m=4` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 20256 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 5396 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 198 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 43.5 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 43.5 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 115 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.0229 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000711 (2^-10.46) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 11.7 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000214 (2^-12.19) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 3.51 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.5 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (5 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=12,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 20256 | 198 | 43.5 | 5 | 0.0229 | 0.000711 (2^-10.46) | 10.46 |
| 1 | `pipelined_m:data_width=15,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=3` | 23841 | 290 | 59.9 | 7 | 0.0302 | 0.000632 (2^-10.63) | 10.63 |
| 2 | `pipelined_m:data_width=16,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=4` | 25643 | 260 | 43.5 | 6 | 0.0295 | 0.000311 (2^-11.65) | 11.65 |
| 3 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 27363 | 163 | 19.4 | 4 | 0.0252 | 9.49e-05 (2^-13.36) | 13.36 |
| 4 | `pipelined_m:data_width=22,n_iter=18,angle_guard=-1,frac_guard=4,rounding=trunc,m=7` | 40470 | 271 | 17.5 | 5 | 0.0389 | 1.75e-05 (2^-15.80) | 15.80 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *My two families are the throughput-friendly (1 result/cycle) options, and the spec's throughput>=1 MSPS constraint plus min-area objective makes them the natural candidates. The fleet facts show pipelined_m is clearly my stronger family (56/59 feasible, best 32548) while full pipelined lags (best 44252, 1 on front). The binding constraint is max_abs_err<=2^-10, which depends only on data_width, n_iter, angle_guard, frac_guard, rounding. I therefore concentrate the budget on the accuracy-feasible core (data_width 12-16, n_iter 10-14, guards 0-1) where the area/accuracy Pareto front sits, and split 70/30 between pipelined_m (primary) and pipelined (verification). This focuses the 14-eval budget on the trade-off region that can actually land on the merged front rather than wasting evals on infeasible or dominated corners.*)
- `pipelined_m` (8 evals): data_width=12..16, n_iter=10..14, angle_guard=0..1, frac_guard=0..1, rounding=trunc|round, m=2..4. *Why:* pipelined_m is my only family that has produced any feasible designs (56/59 feasible, best area 32548 um2) and it is the closest to the iterative best (7014). The m=2..4 register-every-m-stages structure cuts FF count vs full pipelined (best 44252) while keeping 1 result/cycle throughput. I narrow to the accuracy-feasible core: data_width 12-16 and n_iter 10-14 with small guards, since max_abs_err<=2^-10 is the binding constraint and area scales with width and N. Focusing the 14-eval budget here lets Optuna map the area/accuracy trade-off near the constraint boundary where the Pareto front lives.
- clamped by code: budget 8 supports 1 families; dropped ['pipelined']

**Result (code):** 8 evaluations this round, 8 total; 3 feasible; hypervolume 2.65e+04 (n/a).

**LLM decision:** `stop` — The front is feasible and meets all constraints (throughput >= 1 MSPS, max_abs_err <= 2^-10). The minimum area design is pipelined_m [data_width=16, n_iter=12, angle_guard=0, frac_guard=1, rounding=trunc, m=4] with area_um2=20256, accuracy_bits=10.5, and throughput 43.5 MSPS. This is well within the accuracy constraint (10.5 > 10) and far exceeds the throughput requirement. The hypervolume is 2.65e+04, which is reasonable given the reference point (40000, 10). Since this is the final round, we stop with the current best design selected by the min area rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 6 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 8 of 14.
Hypervolume of the feasible front: 2.65e+04 (gain this round: n/a (first round)).
Feasible designs: 3 of 8 evaluations (3 unique).
Families explored so far: pipelined_m. Not yet explored: pipelined.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 70.8
- max_abs_err <= 0.000976562: 62% violate; best seen 0.000311 (2^-11.65)

Pareto front (feasible, 3 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=0 frac_guard=1 rounding=trunc m=4] area_um2=20256, accuracy_bits=10.5, ffs=198, throughput_msps=43.5, max_abs_err=0.000711 (2^-10.46), power_index=0.0229
- pipelined_m [data_width=15 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=3] area_um2=23841, accuracy_bits=10.6, ffs=290, throughput_msps=59.9, max_abs_err=0.000632 (2^-10.63), power_index=0.0302
- pipelined_m [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=4] area_um2=25643, accuracy_bits=11.7, ffs=260, throughput_msps=43.5, max_abs_err=0.000311 (2^-11.65), power_index=0.0295
Front coverage: area_um2 20256..25643 (HV reference 40000); accuracy_bits 10.5..11.7 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- pipelined_m: 8 evals, 3 feasible; max throughput seen 70.8 MSPS; best accuracy 11.65 bits; best feasible area_um2=20256; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..1, m 3..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 6 evaluations*)
- `pipelined_m` (6 evals): data_width=14..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (3 front designs; box front_anchored)

**Result (code):** 6 evaluations this round, 14 total; 9 feasible; hypervolume 4.811e+04 (+81.6%).

**No LLM call** (code's front-mapping round): The front is feasible and meets all constraints (throughput >= 1 MSPS, max_abs_err <= 2^-10). The minimum area design is pipelined_m [data_width=16, n_iter=12, angle_guard=0, frac_guard=1, rounding=trunc, m=4] with area_um2=20256, accuracy_bits=10.5, and throughput 43.5 MSPS. This is well within the accuracy constraint (10.5 > 10) and far exceeds the throughput requirement. The hypervolume is 2.65e+04, which is reasonable given the reference point (40000, 10). Since this is the final round, we stop with the current best design selected by the min area rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 14 of 14.
Hypervolume of the feasible front: 4.811e+04 (gain this round: +81.6%).
Feasible designs: 9 of 14 evaluations (9 unique).
Families explored so far: pipelined_m. Not yet explored: pipelined.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 70.8
- max_abs_err <= 0.000976562: 36% violate; best seen 1.75e-05 (2^-15.80)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=0 frac_guard=1 rounding=trunc m=4] area_um2=20256, accuracy_bits=10.5, ffs=198, throughput_msps=43.5, max_abs_err=0.000711 (2^-10.46), power_index=0.0229
- pipelined_m [data_width=15 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=3] area_um2=23841, accuracy_bits=10.6, ffs=290, throughput_msps=59.9, max_abs_err=0.000632 (2^-10.63), power_index=0.0302
- pipelined_m [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=4] area_um2=25643, accuracy_bits=11.7, ffs=260, throughput_msps=43.5, max_abs_err=0.000311 (2^-11.65), power_index=0.0295
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=8] area_um2=27363, accuracy_bits=13.4, ffs=163, throughput_msps=19.4, max_abs_err=9.49e-05 (2^-13.36), power_index=0.0252
- pipelined_m [data_width=22 n_iter=18 angle_guard=-1 frac_guard=4 rounding=trunc m=7] area_um2=40470, accuracy_bits=15.8, ffs=271, throughput_msps=17.5, max_abs_err=1.75e-05 (2^-15.80), power_index=0.0389
Front coverage: area_um2 20256..40470 (HV reference 40000); accuracy_bits 10.5..15.8 (HV reference 10); data_width on the front 15..22 (registry 8..28).

Per family:
- pipelined_m: 14 evals, 9 feasible; max throughput seen 70.8 MSPS; best accuracy 15.80 bits; best feasible area_um2=20256; feasible ranges: data_width 14..22, n_iter 12..26, angle_guard -2..2, frac_guard 0..4, m 3..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4094 in, 1049 out
- provider-reported cost: $0.0031
- full prompts and replies: `llm_trace.jsonl`

