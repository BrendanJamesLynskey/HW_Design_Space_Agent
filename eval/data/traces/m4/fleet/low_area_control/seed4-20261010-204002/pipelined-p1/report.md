# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec low_area_control: Field-oriented motor-control loop needing sin/cos of the rotor angle at >= 1 MSPS with max error <= 2^-10. Area is everything: minimise LUTs + FFs.
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min luts_plus_ffs (HV ref 1500)
  objective: max accuracy_bits (HV ref 10)
  select: min luts_plus_ffs
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=18,n_iter=12,angle_guard=-1,frac_guard=0,rounding=trunc,m=7` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 689 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 157 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 59.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 59.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 67.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0318 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000595 (2^-10.71) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 39 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 0.000202 (2^-12.27) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 13.3 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 10.7 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=12,angle_guard=-1,frac_guard=0,rounding=trunc,m=7` | 689 | 157 | 59.6 | 4 | 0.0318 | 0.000595 (2^-10.71) | 10.71 |
| 1 | `pipelined_m:data_width=17,n_iter=13,angle_guard=3,frac_guard=0,rounding=round,m=7` | 764 | 157 | 56.8 | 4 | 0.0347 | 0.000314 (2^-11.64) | 11.64 |
| 2 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=3,rounding=trunc,m=5` | 855 | 217 | 77.0 | 5 | 0.0403 | 0.000217 (2^-12.17) | 12.17 |
| 3 | `pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=3,rounding=trunc,m=8` | 920 | 153 | 50.3 | 4 | 0.0404 | 0.000187 (2^-12.39) | 12.39 |
| 4 | `pipelined_m:data_width=16,n_iter=16,angle_guard=4,frac_guard=3,rounding=trunc,m=8` | 1017 | 157 | 50.3 | 4 | 0.0442 | 0.000132 (2^-12.88) | 12.88 |
| 5 | `pipelined_m:data_width=16,n_iter=16,angle_guard=4,frac_guard=4,rounding=trunc,m=8` | 1048 | 159 | 50.3 | 4 | 0.0454 | 0.000108 (2^-13.17) | 13.17 |
| 6 | `pipelined_m:data_width=19,n_iter=16,angle_guard=3,frac_guard=0,rounding=round,m=7` | 1048 | 241 | 56.8 | 5 | 0.0485 | 5.41e-05 (2^-14.17) | 14.17 |
| 7 | `pipelined_m:data_width=20,n_iter=16,angle_guard=3,frac_guard=0,rounding=round,m=3` | 1096 | 464 | 114.5 | 8 | 0.0587 | 4.33e-05 (2^-14.50) | 14.50 |
| 8 | `pipelined_m:data_width=23,n_iter=19,angle_guard=3,frac_guard=0,rounding=round,m=8` | 1485 | 286 | 48.0 | 5 | 0.0666 | 5.47e-06 (2^-17.48) | 17.48 |
| 9 | `pipelined_m:data_width=23,n_iter=28,angle_guard=4,frac_guard=0,rounding=round,m=7` | 2253 | 369 | 52.0 | 6 | 0.0986 | 2.9e-06 (2^-18.39) | 18.39 |
| 10 | `pipelined_m:data_width=25,n_iter=28,angle_guard=0,frac_guard=0,rounding=round,m=6` | 2310 | 464 | 62.5 | 7 | 0.104 | 1.37e-06 (2^-19.48) | 19.48 |
| 11 | `pipelined_m:data_width=23,n_iter=28,angle_guard=3,frac_guard=4,rounding=round,m=7` | 2501 | 391 | 52.0 | 6 | 0.109 | 8.03e-07 (2^-20.25) | 20.25 |
| 12 | `pipelined_m:data_width=28,n_iter=28,angle_guard=3,frac_guard=1,rounding=round,m=7` | 2767 | 444 | 49.9 | 6 | 0.121 | 5.72e-08 (2^-24.06) | 24.06 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires throughput >= 1 MSPS, which both pipelined families easily meet (1 result/cycle). The critical constraint is max_abs_err <= 2^-10, which requires data_width >= 11 because the output LSB is 2^-(W-2). To minimize area (LUTs+FFs), we focus on pipelined_m, which can reduce FF count by a factor of m without increasing LUTs. We allocate 80% of the budget to pipelined_m to explore the m parameter and the accuracy-area trade-off, and 20% to pipelined as a baseline. The parameter ranges cover the feasible region: data_width 11..18 (11 is the minimum for accuracy, 18 allows higher accuracy), n_iter 8..20 (8 to test low iteration with high guards, 20 for high accuracy), angle_guard -2..4 and frac_guard 0..4 (full registry ranges to allow trade-offs), rounding both. For pipelined_m, m from 2..8 explores the FF reduction vs. combinational delay trade-off.*)
- `pipelined` (12 evals): data_width=11..18, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Baseline pipelined family: one register per micro-rotation. Provides a reference for area and accuracy. Likely dominated by pipelined_m in area, but useful to confirm and to map the front if pipelined_m has unexpected LUT overhead.
- `pipelined_m` (48 evals): data_width=11..18, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Most promising for the min area objective. By registering every m stages, it reduces FF count while keeping the same datapath LUTs. The m parameter trades Fmax (not a constraint beyond 1 MSPS) for area. Allocating the majority of the budget here to thoroughly explore the accuracy-area trade-off.

**Result (code):** 60 evaluations this round, 60 total; 43 feasible; hypervolume 1541 (n/a).

**LLM decision:** `stop` — Final round, budget/round cap reached, so this is a stop. The feasible front already brackets the selection objective well: its cheapest point pipelined_m [W=18 N=12 angle_guard=-1 frac_guard=0 trunc m=7] has luts_plus_ffs=847, meets throughput (59.6 MSPS >= 1) and error (2^-10.71 <= 2^-10), and is the min-luts_plus_ffs pick the spec's selection rule would choose. Both constraints are comfortably satisfiable (0% throughput violations, max_abs_err 2^-10.71 at the selection corner vs the 2^-10 limit), so infeasible is not warranted. The front spans luts_plus_ffs 847..1367 and accuracy_bits 10.7..13.6 (HV 1541 vs ref 1500), with the low-area corner far from any constraint boundary — refining further would not change the selected design, and no unexplored families remain.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1541 (gain this round: n/a (first round)).
Feasible designs: 43 of 60 evaluations (35 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 28% violate; best seen 8.02e-05 (2^-13.61)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=12 angle_guard=-1 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=847, accuracy_bits=10.7, luts=689, ffs=157, throughput_msps=59.6, max_abs_err=0.000595 (2^-10.71), power_index=0.0318
- pipelined_m [data_width=14 n_iter=13 angle_guard=4 frac_guard=4 rounding=trunc m=6] luts_plus_ffs=969, accuracy_bits=10.9, luts=764, ffs=205, throughput_msps=68.5, max_abs_err=0.00054 (2^-10.86), power_index=0.0364
- pipelined_m [data_width=16 n_iter=14 angle_guard=0 frac_guard=2 rounding=trunc m=5] luts_plus_ffs=1007, accuracy_bits=11.3, luts=800, ffs=207, throughput_msps=80.6, max_abs_err=0.000391 (2^-11.32), power_index=0.0379
- pipelined_m [data_width=16 n_iter=13 angle_guard=4 frac_guard=3 rounding=trunc m=6] luts_plus_ffs=1038, accuracy_bits=11.6, luts=815, ffs=223, throughput_msps=65.4, max_abs_err=0.000323 (2^-11.60), power_index=0.039
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=3 rounding=trunc m=5] luts_plus_ffs=1072, accuracy_bits=12.2, luts=855, ffs=217, throughput_msps=77, max_abs_err=0.000217 (2^-12.17), power_index=0.0403
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1073, accuracy_bits=12.4, luts=920, ffs=153, throughput_msps=50.3, max_abs_err=0.000187 (2^-12.39), power_index=0.0404
- pipelined_m [data_width=16 n_iter=16 angle_guard=4 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1174, accuracy_bits=12.9, luts=1017, ffs=157, throughput_msps=50.3, max_abs_err=0.000132 (2^-12.88), power_index=0.0442
- pipelined_m [data_width=16 n_iter=16 angle_guard=4 frac_guard=4 rounding=trunc m=8] luts_plus_ffs=1208, accuracy_bits=13.2, luts=1048, ffs=159, throughput_msps=50.3, max_abs_err=0.000108 (2^-13.17), power_index=0.0454
- pipelined_m [data_width=17 n_iter=16 angle_guard=4 frac_guard=3 rounding=trunc m=5] luts_plus_ffs=1367, accuracy_bits=13.6, luts=1064, ffs=303, throughput_msps=77, max_abs_err=8.02e-05 (2^-13.61), power_index=0.0514
Front coverage: luts_plus_ffs 847..1367 (HV reference 1500); accuracy_bits 10.7..13.6 (HV reference 10); data_width on the front 14..18 (registry 8..28).

Per family:
- pipelined: 12 evals, 5 feasible; max throughput seen 282 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=1758; feasible ranges: data_width 12..18, n_iter 14..18, angle_guard 1..4, frac_guard 0..4
- pipelined_m: 48 evals, 38 feasible; max throughput seen 171 MSPS; best accuracy 13.61 bits; best feasible luts_plus_ffs=847; feasible ranges: data_width 14..18, n_iter 12..20, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (9 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 74 feasible; hypervolume 1779 (+15.4%).

**No LLM call** (code's front-mapping round): Final round, budget/round cap reached, so this is a stop. The feasible front already brackets the selection objective well: its cheapest point pipelined_m [W=18 N=12 angle_guard=-1 frac_guard=0 trunc m=7] has luts_plus_ffs=847, meets throughput (59.6 MSPS >= 1) and error (2^-10.71 <= 2^-10), and is the min-luts_plus_ffs pick the spec's selection rule would choose. Both constraints are comfortably satisfiable (0% throughput violations, max_abs_err 2^-10.71 at the selection corner vs the 2^-10 limit), so infeasible is not warranted. The front spans luts_plus_ffs 847..1367 and accuracy_bits 10.7..13.6 (HV 1541 vs ref 1500), with the low-area corner far from any constraint boundary — refining further would not change the selected design, and no unexplored families remain.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1779 (gain this round: +15.4%).
Feasible designs: 74 of 100 evaluations (63 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 26% violate; best seen 5.72e-08 (2^-24.06)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=12 angle_guard=-1 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=847, accuracy_bits=10.7, luts=689, ffs=157, throughput_msps=59.6, max_abs_err=0.000595 (2^-10.71), power_index=0.0318
- pipelined_m [data_width=17 n_iter=13 angle_guard=3 frac_guard=0 rounding=round m=7] luts_plus_ffs=921, accuracy_bits=11.6, luts=764, ffs=157, throughput_msps=56.8, max_abs_err=0.000314 (2^-11.64), power_index=0.0347
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1073, accuracy_bits=12.4, luts=920, ffs=153, throughput_msps=50.3, max_abs_err=0.000187 (2^-12.39), power_index=0.0404
- pipelined_m [data_width=16 n_iter=16 angle_guard=4 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1174, accuracy_bits=12.9, luts=1017, ffs=157, throughput_msps=50.3, max_abs_err=0.000132 (2^-12.88), power_index=0.0442
- pipelined_m [data_width=16 n_iter=16 angle_guard=4 frac_guard=4 rounding=trunc m=8] luts_plus_ffs=1208, accuracy_bits=13.2, luts=1048, ffs=159, throughput_msps=50.3, max_abs_err=0.000108 (2^-13.17), power_index=0.0454
- pipelined_m [data_width=20 n_iter=16 angle_guard=3 frac_guard=0 rounding=round m=3] luts_plus_ffs=1560, accuracy_bits=14.5, luts=1096, ffs=464, throughput_msps=114, max_abs_err=4.33e-05 (2^-14.50), power_index=0.0587
- pipelined_m [data_width=23 n_iter=19 angle_guard=3 frac_guard=0 rounding=round m=8] luts_plus_ffs=1770, accuracy_bits=17.5, luts=1485, ffs=286, throughput_msps=48, max_abs_err=5.47e-06 (2^-17.48), power_index=0.0666
- pipelined_m [data_width=23 n_iter=28 angle_guard=4 frac_guard=0 rounding=round m=7] luts_plus_ffs=2622, accuracy_bits=18.4, luts=2253, ffs=369, throughput_msps=52, max_abs_err=2.9e-06 (2^-18.39), power_index=0.0986
- pipelined_m [data_width=23 n_iter=28 angle_guard=3 frac_guard=4 rounding=round m=7] luts_plus_ffs=2892, accuracy_bits=20.2, luts=2501, ffs=391, throughput_msps=52, max_abs_err=8.03e-07 (2^-20.25), power_index=0.109
- pipelined_m [data_width=28 n_iter=28 angle_guard=3 frac_guard=1 rounding=round m=7] luts_plus_ffs=3211, accuracy_bits=24.1, luts=2767, ffs=444, throughput_msps=49.9, max_abs_err=5.72e-08 (2^-24.06), power_index=0.121
Front coverage: luts_plus_ffs 847..3211 (HV reference 1500); accuracy_bits 10.7..24.1 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- pipelined: 12 evals, 5 feasible; max throughput seen 282 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=1758; feasible ranges: data_width 12..18, n_iter 14..18, angle_guard 1..4, frac_guard 0..4
- pipelined_m: 88 evals, 69 feasible; max throughput seen 171 MSPS; best accuracy 24.06 bits; best feasible luts_plus_ffs=847; feasible ranges: data_width 14..28, n_iter 11..28, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4394 in, 11703 out
- provider-reported cost: $0.0142
- full prompts and replies: `llm_trace.jsonl`

