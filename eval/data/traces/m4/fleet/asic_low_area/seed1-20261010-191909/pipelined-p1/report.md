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
`pipelined_m:data_width=19,n_iter=14,angle_guard=-2,frac_guard=1,rounding=round,m=6` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 27047 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 7206 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 226 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 25.7 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 25.7 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 195 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.0285 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000241 (2^-12.02) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 31.6 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.91e-05 (2^-14.05) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 7.75 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (16 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=14,angle_guard=-2,frac_guard=1,rounding=round,m=6` | 27047 | 226 | 25.7 | 5 | 0.0285 | 0.000241 (2^-12.02) | 12.02 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=3,frac_guard=1,rounding=round,m=6` | 27748 | 230 | 24.6 | 5 | 0.0291 | 0.000147 (2^-12.73) | 12.73 |
| 2 | `pipelined_m:data_width=19,n_iter=15,angle_guard=3,frac_guard=0,rounding=round,m=6` | 28956 | 235 | 23.6 | 5 | 0.0301 | 8.25e-05 (2^-13.57) | 13.57 |
| 3 | `pipelined_m:data_width=19,n_iter=15,angle_guard=3,frac_guard=3,rounding=round,m=5` | 32379 | 249 | 28.1 | 5 | 0.0329 | 6.68e-05 (2^-13.87) | 13.87 |
| 4 | `pipelined_m:data_width=22,n_iter=15,angle_guard=3,frac_guard=0,rounding=trunc,m=6` | 32896 | 267 | 21.0 | 5 | 0.0343 | 6.66e-05 (2^-13.87) | 13.87 |
| 5 | `pipelined_m:data_width=19,n_iter=17,angle_guard=3,frac_guard=1,rounding=round,m=6` | 34249 | 241 | 23.6 | 5 | 0.0336 | 3.23e-05 (2^-14.92) | 14.92 |
| 6 | `pipelined_m:data_width=19,n_iter=17,angle_guard=3,frac_guard=3,rounding=round,m=6` | 36059 | 249 | 23.6 | 5 | 0.0351 | 2.41e-05 (2^-15.34) | 15.34 |
| 7 | `pipelined_m:data_width=22,n_iter=17,angle_guard=2,frac_guard=0,rounding=trunc,m=8` | 36255 | 264 | 16.5 | 5 | 0.0361 | 2.27e-05 (2^-15.43) | 15.43 |
| 8 | `pipelined_m:data_width=22,n_iter=17,angle_guard=2,frac_guard=1,rounding=trunc,m=8` | 37160 | 268 | 16.5 | 5 | 0.0368 | 1.83e-05 (2^-15.74) | 15.74 |
| 9 | `pipelined_m:data_width=22,n_iter=17,angle_guard=2,frac_guard=3,rounding=trunc,m=8` | 38970 | 276 | 15.9 | 5 | 0.0383 | 1.71e-05 (2^-15.84) | 15.84 |
| 10 | `pipelined_m:data_width=25,n_iter=17,angle_guard=2,frac_guard=0,rounding=trunc,m=8` | 40655 | 297 | 14.8 | 5 | 0.0405 | 1.58e-05 (2^-15.95) | 15.95 |
| 11 | `pipelined_m:data_width=24,n_iter=21,angle_guard=-2,frac_guard=1,rounding=trunc,m=8` | 46168 | 278 | 15.9 | 5 | 0.0427 | 6.36e-06 (2^-17.26) | 17.26 |
| 12 | `pipelined_m:data_width=24,n_iter=21,angle_guard=3,frac_guard=1,rounding=trunc,m=6` | 50884 | 376 | 19.6 | 6 | 0.0509 | 2.24e-06 (2^-18.77) | 18.77 |
| 13 | `pipelined_m:data_width=25,n_iter=21,angle_guard=3,frac_guard=1,rounding=trunc,m=6` | 52723 | 389 | 19.0 | 6 | 0.0527 | 1.41e-06 (2^-19.43) | 19.43 |
| 14 | `pipelined_m:data_width=27,n_iter=23,angle_guard=-1,frac_guard=2,rounding=round,m=6` | 61184 | 409 | 18.4 | 6 | 0.0588 | 7.02e-07 (2^-20.44) | 20.44 |
| 15 | `pipelined_m:data_width=25,n_iter=24,angle_guard=4,frac_guard=3,rounding=round,m=4` | 67941 | 588 | 27.3 | 8 | 0.0727 | 2.67e-07 (2^-21.84) | 21.84 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Throughput is not the binding constraint: both allowed families emit 1 result/cycle, so >=1 MSPS only requires Fmax >= ~1 MHz, which even heavily register-collapsed designs clear. The binding constraint is max_abs_err <= 2^-10, and the objective is minimum cell area with accuracy_bits as the second objective. Accuracy is a function of data_width, n_iter, angle_guard, frac_guard and rounding only, so the search should concentrate on the smallest (W, N, guard) combination that still clears 2^-10, and on the register structure that minimises FFs for that datapath. pipelined_m is the natural area winner (fewer pipeline registers via m) and gets the larger share; pipelined is retained as the high-Fmax anchor and cross-check. Ranges are deliberately centred on the plausible feasible accuracy region (W ~ 13-18, N ~ 12-18) rather than the full 8..28 / 4..30 registry, so the 100-eval budget is spent near the feasibility boundary and along the area/accuracy trade-off, with code free to widen later once the front is located.*)
- `pipelined_m` (39 evals): data_width=10..20, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Primary area-minimiser. Both pipelined families give 1 result/cycle, so the >=1 MSPS constraint is met by any Fmax above ~1 MHz and is not binding; the real constraint is max_abs_err <= 2^-10 and the objective is cell area. Registering only every m-th micro-rotation (m up to 8) removes most of the per-stage pipeline FFs, which is the dominant area term for this family, at the cost of a longer combinational path and lower Fmax - which the loose throughput constraint tolerates. This family therefore owns the low-area end of the Pareto front. Ranges are centred on the region where accuracy can plausibly reach 2^-10 (W around 13-18, N around 12-18) while still allowing code to find the exact feasibility boundary on the low side.
- `pipelined` (21 evals): data_width=10..20, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Reference / high-Fmax anchor for the front. One register per micro-rotation maximises Fmax but also FF count, so it should be dominated on area by pipelined_m; it is kept to (a) confirm the accuracy-vs-area boundary is family-independent (accuracy depends only on W, N, guards, rounding), (b) provide the high-throughput end of the trade-off curve that hypervolume rewards, and (c) give a clean baseline against which pipelined_m's area savings are measured. Same accuracy-oriented parameter ranges as pipelined_m so the two fronts are directly comparable.

**Result (code):** 60 evaluations this round, 60 total; 34 feasible; hypervolume 5.41e+04 (n/a).

**LLM decision:** `stop` — Final round, and the front is already feasible and well-covering: 6 Pareto designs, all satisfying both constraints with large margin (throughput 23.6-28.1 MSPS vs the 1 MSPS floor; max_abs_err 2.41e-05..2.41e-04 vs the 9.77e-04 limit). The min-area selection rule is served by pipelined_m [data_width=19 n_iter=14 angle_guard=-2 frac_guard=1 rounding=round m=6] at area_um2=27047 with 12.0 accuracy bits, and the front extends to 15.3 bits at 36059 um^2, i.e. it spans the accuracy range 12..15.3 against the HV reference of 10 bits while staying under the 40000 um^2 HV reference. pipelined_m dominates pipelined (best feasible area 27047 vs 50420 um^2), so no unexplored family is needed. Nothing indicates the constraints are unreachable, so infeasible is not warranted; further search is not justified within the remaining budget.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 5.41e+04 (gain this round: n/a (first round)).
Feasible designs: 34 of 60 evaluations (27 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 201
- max_abs_err <= 0.000976562: 43% violate; best seen 2.41e-05 (2^-15.34)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=-2 frac_guard=1 rounding=round m=6] area_um2=27047, accuracy_bits=12, ffs=226, throughput_msps=25.7, max_abs_err=0.000241 (2^-12.02), power_index=0.0285
- pipelined_m [data_width=18 n_iter=14 angle_guard=3 frac_guard=1 rounding=round m=6] area_um2=27748, accuracy_bits=12.7, ffs=230, throughput_msps=24.6, max_abs_err=0.000147 (2^-12.73), power_index=0.0291
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=0 rounding=round m=6] area_um2=28956, accuracy_bits=13.6, ffs=235, throughput_msps=23.6, max_abs_err=8.25e-05 (2^-13.57), power_index=0.0301
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=3 rounding=round m=5] area_um2=32379, accuracy_bits=13.9, ffs=249, throughput_msps=28.1, max_abs_err=6.68e-05 (2^-13.87), power_index=0.0329
- pipelined_m [data_width=19 n_iter=17 angle_guard=3 frac_guard=1 rounding=round m=6] area_um2=34249, accuracy_bits=14.9, ffs=241, throughput_msps=23.6, max_abs_err=3.23e-05 (2^-14.92), power_index=0.0336
- pipelined_m [data_width=19 n_iter=17 angle_guard=3 frac_guard=3 rounding=round m=6] area_um2=36059, accuracy_bits=15.3, ffs=249, throughput_msps=23.6, max_abs_err=2.41e-05 (2^-15.34), power_index=0.0351
Front coverage: area_um2 27047..36059 (HV reference 40000); accuracy_bits 12..15.3 (HV reference 10); data_width on the front 18..19 (registry 8..28).

Per family:
- pipelined: 21 evals, 8 feasible; max throughput seen 201 MSPS; best accuracy 14.69 bits; best feasible area_um2=50420; feasible ranges: data_width 18..19, n_iter 16..17, angle_guard -2..1, frac_guard 2..4
- pipelined_m: 39 evals, 26 feasible; max throughput seen 75.4 MSPS; best accuracy 15.34 bits; best feasible area_um2=27047; feasible ranges: data_width 17..19, n_iter 14..20, angle_guard -2..4, frac_guard 0..4, m 2..6
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (6 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 74 feasible; hypervolume 5.542e+04 (+2.4%).

**No LLM call** (code's front-mapping round): Final round, and the front is already feasible and well-covering: 6 Pareto designs, all satisfying both constraints with large margin (throughput 23.6-28.1 MSPS vs the 1 MSPS floor; max_abs_err 2.41e-05..2.41e-04 vs the 9.77e-04 limit). The min-area selection rule is served by pipelined_m [data_width=19 n_iter=14 angle_guard=-2 frac_guard=1 rounding=round m=6] at area_um2=27047 with 12.0 accuracy bits, and the front extends to 15.3 bits at 36059 um^2, i.e. it spans the accuracy range 12..15.3 against the HV reference of 10 bits while staying under the 40000 um^2 HV reference. pipelined_m dominates pipelined (best feasible area 27047 vs 50420 um^2), so no unexplored family is needed. Nothing indicates the constraints are unreachable, so infeasible is not warranted; further search is not justified within the remaining budget.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 5.542e+04 (gain this round: +2.4%).
Feasible designs: 74 of 100 evaluations (65 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 201
- max_abs_err <= 0.000976562: 26% violate; best seen 2.67e-07 (2^-21.84)

Pareto front (feasible, 16 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=-2 frac_guard=1 rounding=round m=6] area_um2=27047, accuracy_bits=12, ffs=226, throughput_msps=25.7, max_abs_err=0.000241 (2^-12.02), power_index=0.0285
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=0 rounding=round m=6] area_um2=28956, accuracy_bits=13.6, ffs=235, throughput_msps=23.6, max_abs_err=8.25e-05 (2^-13.57), power_index=0.0301
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=3 rounding=round m=5] area_um2=32379, accuracy_bits=13.9, ffs=249, throughput_msps=28.1, max_abs_err=6.68e-05 (2^-13.87), power_index=0.0329
- pipelined_m [data_width=19 n_iter=17 angle_guard=3 frac_guard=1 rounding=round m=6] area_um2=34249, accuracy_bits=14.9, ffs=241, throughput_msps=23.6, max_abs_err=3.23e-05 (2^-14.92), power_index=0.0336
- pipelined_m [data_width=22 n_iter=17 angle_guard=2 frac_guard=0 rounding=trunc m=8] area_um2=36255, accuracy_bits=15.4, ffs=264, throughput_msps=16.5, max_abs_err=2.27e-05 (2^-15.43), power_index=0.0361
- pipelined_m [data_width=22 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc m=8] area_um2=37160, accuracy_bits=15.7, ffs=268, throughput_msps=16.5, max_abs_err=1.83e-05 (2^-15.74), power_index=0.0368
- pipelined_m [data_width=25 n_iter=17 angle_guard=2 frac_guard=0 rounding=trunc m=8] area_um2=40655, accuracy_bits=15.9, ffs=297, throughput_msps=14.8, max_abs_err=1.58e-05 (2^-15.95), power_index=0.0405
- pipelined_m [data_width=24 n_iter=21 angle_guard=3 frac_guard=1 rounding=trunc m=6] area_um2=50884, accuracy_bits=18.8, ffs=376, throughput_msps=19.6, max_abs_err=2.24e-06 (2^-18.77), power_index=0.0509
- pipelined_m [data_width=25 n_iter=21 angle_guard=3 frac_guard=1 rounding=trunc m=6] area_um2=52723, accuracy_bits=19.4, ffs=389, throughput_msps=19, max_abs_err=1.41e-06 (2^-19.43), power_index=0.0527
- pipelined_m [data_width=25 n_iter=24 angle_guard=4 frac_guard=3 rounding=round m=4] area_um2=67941, accuracy_bits=21.8, ffs=588, throughput_msps=27.3, max_abs_err=2.67e-07 (2^-21.84), power_index=0.0727
Front coverage: area_um2 27047..67941 (HV reference 40000); accuracy_bits 12..21.8 (HV reference 10); data_width on the front 18..27 (registry 8..28).

Per family:
- pipelined: 21 evals, 8 feasible; max throughput seen 201 MSPS; best accuracy 14.69 bits; best feasible area_um2=50420; feasible ranges: data_width 18..19, n_iter 16..17, angle_guard -2..1, frac_guard 2..4
- pipelined_m: 79 evals, 66 feasible; max throughput seen 75.4 MSPS; best accuracy 21.84 bits; best feasible area_um2=27047; feasible ranges: data_width 17..27, n_iter 12..27, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5054 in, 2772 out
- provider-reported cost: $0.0022
- full prompts and replies: `llm_trace.jsonl`

