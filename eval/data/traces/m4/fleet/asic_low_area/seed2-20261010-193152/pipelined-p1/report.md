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
`pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=1,rounding=round,m=8` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 18385 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 4898 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 132 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 23.6 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 23.6 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 170 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.0182 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000976 (2^-10.00) | exact: bit-accurate model, exhaustive (16384 angles) |
| max_abs_err_lsb | 4 | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err | 0.000264 (2^-11.89) | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err_lsb | 1.08 | exact: bit-accurate model, exhaustive (16384 angles) |
| accuracy_bits | 10 | exact: bit-accurate model, exhaustive (16384 angles) |

## Pareto front (20 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=1,rounding=round,m=8` | 18385 | 132 | 23.6 | 4 | 0.0182 | 0.000976 (2^-10.00) | 10.00 |
| 1 | `pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=2,rounding=round,m=8` | 18991 | 134 | 23.6 | 4 | 0.0186 | 0.000825 (2^-10.24) | 10.24 |
| 2 | `pipelined_m:data_width=14,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 19611 | 132 | 23.6 | 4 | 0.0189 | 0.000746 (2^-10.39) | 10.39 |
| 3 | `pipelined_m:data_width=14,n_iter=13,angle_guard=2,frac_guard=2,rounding=round,m=8` | 20370 | 134 | 23.6 | 4 | 0.0194 | 0.000581 (2^-10.75) | 10.75 |
| 4 | `pipelined_m:data_width=16,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 21800 | 147 | 21.3 | 4 | 0.021 | 0.000378 (2^-11.37) | 11.37 |
| 5 | `pipelined_m:data_width=16,n_iter=13,angle_guard=2,frac_guard=2,rounding=round,m=3` | 26656 | 329 | 54.3 | 7 | 0.034 | 0.00031 (2^-11.65) | 11.65 |
| 6 | `pipelined_m:data_width=23,n_iter=13,angle_guard=2,frac_guard=0,rounding=round,m=7` | 28148 | 199 | 18.1 | 4 | 0.0276 | 0.000244 (2^-12.00) | 12.00 |
| 7 | `pipelined_m:data_width=18,n_iter=18,angle_guard=0,frac_guard=1,rounding=trunc,m=6` | 31929 | 219 | 26.8 | 5 | 0.031 | 0.000122 (2^-13.01) | 13.01 |
| 8 | `pipelined_m:data_width=18,n_iter=18,angle_guard=2,frac_guard=1,rounding=round,m=6` | 33892 | 227 | 25.7 | 5 | 0.0326 | 5.02e-05 (2^-14.28) | 14.28 |
| 9 | `pipelined_m:data_width=23,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc,m=7` | 34856 | 269 | 19.5 | 5 | 0.0355 | 3.32e-05 (2^-14.88) | 14.88 |
| 10 | `pipelined_m:data_width=23,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc,m=5` | 37412 | 350 | 26.0 | 6 | 0.0415 | 3.23e-05 (2^-14.92) | 14.92 |
| 11 | `pipelined_m:data_width=23,n_iter=18,angle_guard=0,frac_guard=1,rounding=round,m=8` | 40864 | 275 | 16.5 | 5 | 0.0394 | 9.76e-06 (2^-16.64) | 16.64 |
| 12 | `pipelined_m:data_width=23,n_iter=19,angle_guard=2,frac_guard=0,rounding=round,m=7` | 41657 | 275 | 18.1 | 5 | 0.0399 | 6.01e-06 (2^-17.34) | 17.34 |
| 13 | `pipelined_m:data_width=23,n_iter=19,angle_guard=2,frac_guard=1,rounding=trunc,m=5` | 44410 | 358 | 25.1 | 6 | 0.0461 | 5.7e-06 (2^-17.42) | 17.42 |
| 14 | `pipelined_m:data_width=23,n_iter=23,angle_guard=2,frac_guard=0,rounding=round,m=7` | 51230 | 352 | 18.1 | 6 | 0.0498 | 2.9e-06 (2^-18.39) | 18.39 |
| 15 | `pipelined_m:data_width=23,n_iter=22,angle_guard=2,frac_guard=3,rounding=trunc,m=7` | 52874 | 370 | 17.5 | 6 | 0.0517 | 1.77e-06 (2^-19.11) | 19.11 |
| 16 | `pipelined_m:data_width=27,n_iter=22,angle_guard=3,frac_guard=0,rounding=round,m=7` | 57548 | 411 | 15.3 | 6 | 0.0568 | 6.06e-07 (2^-20.65) | 20.65 |
| 17 | `pipelined_m:data_width=27,n_iter=22,angle_guard=3,frac_guard=1,rounding=round,m=3` | 68294 | 785 | 34.9 | 10 | 0.0839 | 5.44e-07 (2^-20.81) | 20.81 |
| 18 | `pipelined_m:data_width=27,n_iter=29,angle_guard=0,frac_guard=1,rounding=round,m=7` | 76188 | 495 | 16.3 | 7 | 0.0725 | 2.97e-07 (2^-21.68) | 21.68 |
| 19 | `pipelined_m:data_width=27,n_iter=29,angle_guard=3,frac_guard=1,rounding=round,m=7` | 78662 | 510 | 15.3 | 7 | 0.0747 | 1.16e-07 (2^-23.04) | 23.04 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=1 MSPS and max error <= 2^-10 while minimising area. Pipelined_m with high m (8) reduces pipeline registers without hurting throughput, so it is the most promising family for the area-optimal front. We focus the budget on the minimal-area feasible region (W=11-14, N=10-14) and include a small baseline for pipelined to verify dominance. The reserved budget can later map the full ranges of whichever family appears on the front.*)
- `pipelined_m` (54 evals): data_width=11..14, n_iter=10..14, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=8..8. *Why:* Pipelined_m with maximum m=8 minimises pipeline registers while keeping 1 result/cycle, so it should dominate pipelined (m=1) in area for the same accuracy. The ranges focus on the minimal-area feasible region: W=11 is the smallest width that can meet the 2^-10 error bound with rounding, N=10-14 gives enough CORDIC convergence, and angle_guard/frac_guard explore the accuracy-area trade-off.
- `pipelined` (6 evals): data_width=11..14, n_iter=10..14, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Baseline pipelined (m=1) is expected to be area-dominated by pipelined_m with m>=2, but a small share confirms this and provides a reference point for the merged Pareto front.

**Result (code):** 60 evaluations this round, 60 total; 18 feasible; hypervolume 1.515e+04 (n/a).

**LLM decision:** `stop` — This is the final round, so only stop/infeasible apply. Infeasibility is ruled out: the constraints are demonstrably satisfiable — throughput_msps >= 1 has 0% violations (best seen 190 MSPS) and max_abs_err <= 2^-10 is met by 18 feasible evaluations, with the best at 2^-10.75 (0.000581). A feasible Pareto front of 4 designs exists, spanning area_um2 18385..20370 and accuracy_bits 10..10.7, all on pipelined_m with data_width=14. The selection rule (min area_um2) is served by the front's corner design pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=1 rounding=round m=8] at area_um2=18385, accuracy_bits=10.0, throughput 23.6 MSPS — comfortably inside both constraints. The front already covers the accuracy objective's useful range (10 to 10.7 bits, HV ref 10) and the area range is well below the HV reference (40000). No further improvement is expected within the exhausted budget, so stopping is appropriate.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.515e+04 (gain this round: n/a (first round)).
Feasible designs: 18 of 60 evaluations (9 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 190
- max_abs_err <= 0.000976562: 70% violate; best seen 0.000581 (2^-10.75)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=1 rounding=round m=8] area_um2=18385, accuracy_bits=10, ffs=132, throughput_msps=23.6, max_abs_err=0.000976 (2^-10.00), power_index=0.0182
- pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=2 rounding=round m=8] area_um2=18991, accuracy_bits=10.2, ffs=134, throughput_msps=23.6, max_abs_err=0.000825 (2^-10.24), power_index=0.0186
- pipelined_m [data_width=14 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc m=8] area_um2=19611, accuracy_bits=10.4, ffs=132, throughput_msps=23.6, max_abs_err=0.000746 (2^-10.39), power_index=0.0189
- pipelined_m [data_width=14 n_iter=13 angle_guard=2 frac_guard=2 rounding=round m=8] area_um2=20370, accuracy_bits=10.7, ffs=134, throughput_msps=23.6, max_abs_err=0.000581 (2^-10.75), power_index=0.0194
Front coverage: area_um2 18385..20370 (HV reference 40000); accuracy_bits 10..10.7 (HV reference 10); data_width on the front 14..14 (registry 8..28).

Per family:
- pipelined: 6 evals, 1 feasible; max throughput seen 190 MSPS; best accuracy 10.05 bits; best feasible area_um2=34059; feasible ranges: data_width 14..14, n_iter 14..14, angle_guard 1..1, frac_guard 2..2
- pipelined_m: 54 evals, 17 feasible; max throughput seen 30.1 MSPS; best accuracy 10.75 bits; best feasible area_um2=18385; feasible ranges: data_width 14..14, n_iter 12..14, angle_guard 1..2, frac_guard 1..2, m 8..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 53 feasible; hypervolume 5.342e+04 (+252.7%).

**No LLM call** (code's front-mapping round): This is the final round, so only stop/infeasible apply. Infeasibility is ruled out: the constraints are demonstrably satisfiable — throughput_msps >= 1 has 0% violations (best seen 190 MSPS) and max_abs_err <= 2^-10 is met by 18 feasible evaluations, with the best at 2^-10.75 (0.000581). A feasible Pareto front of 4 designs exists, spanning area_um2 18385..20370 and accuracy_bits 10..10.7, all on pipelined_m with data_width=14. The selection rule (min area_um2) is served by the front's corner design pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=1 rounding=round m=8] at area_um2=18385, accuracy_bits=10.0, throughput 23.6 MSPS — comfortably inside both constraints. The front already covers the accuracy objective's useful range (10 to 10.7 bits, HV ref 10) and the area range is well below the HV reference (40000). No further improvement is expected within the exhausted budget, so stopping is appropriate.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 5.342e+04 (gain this round: +252.7%).
Feasible designs: 53 of 100 evaluations (43 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 190
- max_abs_err <= 0.000976562: 47% violate; best seen 1.16e-07 (2^-23.04)

Pareto front (feasible, 20 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=1 rounding=round m=8] area_um2=18385, accuracy_bits=10, ffs=132, throughput_msps=23.6, max_abs_err=0.000976 (2^-10.00), power_index=0.0182
- pipelined_m [data_width=14 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc m=8] area_um2=19611, accuracy_bits=10.4, ffs=132, throughput_msps=23.6, max_abs_err=0.000746 (2^-10.39), power_index=0.0189
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc m=8] area_um2=21800, accuracy_bits=11.4, ffs=147, throughput_msps=21.3, max_abs_err=0.000378 (2^-11.37), power_index=0.021
- pipelined_m [data_width=23 n_iter=13 angle_guard=2 frac_guard=0 rounding=round m=7] area_um2=28148, accuracy_bits=12, ffs=199, throughput_msps=18.1, max_abs_err=0.000244 (2^-12.00), power_index=0.0276
- pipelined_m [data_width=18 n_iter=18 angle_guard=2 frac_guard=1 rounding=round m=6] area_um2=33892, accuracy_bits=14.3, ffs=227, throughput_msps=25.7, max_abs_err=5.02e-05 (2^-14.28), power_index=0.0326
- pipelined_m [data_width=23 n_iter=18 angle_guard=0 frac_guard=1 rounding=round m=8] area_um2=40864, accuracy_bits=16.6, ffs=275, throughput_msps=16.5, max_abs_err=9.76e-06 (2^-16.64), power_index=0.0394
- pipelined_m [data_width=23 n_iter=19 angle_guard=2 frac_guard=1 rounding=trunc m=5] area_um2=44410, accuracy_bits=17.4, ffs=358, throughput_msps=25.1, max_abs_err=5.7e-06 (2^-17.42), power_index=0.0461
- pipelined_m [data_width=23 n_iter=22 angle_guard=2 frac_guard=3 rounding=trunc m=7] area_um2=52874, accuracy_bits=19.1, ffs=370, throughput_msps=17.5, max_abs_err=1.77e-06 (2^-19.11), power_index=0.0517
- pipelined_m [data_width=27 n_iter=22 angle_guard=3 frac_guard=1 rounding=round m=3] area_um2=68294, accuracy_bits=20.8, ffs=785, throughput_msps=34.9, max_abs_err=5.44e-07 (2^-20.81), power_index=0.0839
- pipelined_m [data_width=27 n_iter=29 angle_guard=3 frac_guard=1 rounding=round m=7] area_um2=78662, accuracy_bits=23, ffs=510, throughput_msps=15.3, max_abs_err=1.16e-07 (2^-23.04), power_index=0.0747
Front coverage: area_um2 18385..78662 (HV reference 40000); accuracy_bits 10..23 (HV reference 10); data_width on the front 14..27 (registry 8..28).

Per family:
- pipelined: 6 evals, 1 feasible; max throughput seen 190 MSPS; best accuracy 10.05 bits; best feasible area_um2=34059; feasible ranges: data_width 14..14, n_iter 14..14, angle_guard 1..1, frac_guard 2..2
- pipelined_m: 94 evals, 52 feasible; max throughput seen 78.8 MSPS; best accuracy 23.04 bits; best feasible area_um2=18385; feasible ranges: data_width 13..27, n_iter 12..29, angle_guard -1..3, frac_guard 0..4, m 3..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4583 in, 12597 out
- provider-reported cost: $0.0090
- full prompts and replies: `llm_trace.jsonl`

