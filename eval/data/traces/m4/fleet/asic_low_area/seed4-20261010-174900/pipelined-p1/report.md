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
`pipelined_m:data_width=18,n_iter=18,angle_guard=-2,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 32548 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 8671 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 325 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 41.5 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 41.5 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 169 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.0373 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000344 (2^-11.51) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 22.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 7.28e-05 (2^-13.74) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 4.77 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 11.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (17 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=18,angle_guard=-2,frac_guard=0,rounding=round,m=4` | 32548 | 325 | 41.5 | 7 | 0.0373 | 0.000344 (2^-11.51) | 11.51 |
| 1 | `pipelined_m:data_width=19,n_iter=17,angle_guard=4,frac_guard=1,rounding=trunc,m=6` | 33708 | 242 | 22.7 | 5 | 0.0333 | 4.85e-05 (2^-14.33) | 14.33 |
| 2 | `pipelined_m:data_width=22,n_iter=19,angle_guard=2,frac_guard=3,rounding=trunc,m=8` | 43058 | 276 | 15.9 | 5 | 0.0407 | 6.24e-06 (2^-17.29) | 17.29 |
| 3 | `pipelined_m:data_width=22,n_iter=19,angle_guard=2,frac_guard=3,rounding=trunc,m=7` | 43058 | 276 | 18.1 | 5 | 0.0407 | 6.24e-06 (2^-17.29) | 17.29 |
| 4 | `pipelined_m:data_width=24,n_iter=19,angle_guard=3,frac_guard=2,rounding=trunc,m=6` | 47693 | 381 | 19.6 | 6 | 0.0493 | 4.32e-06 (2^-17.82) | 17.82 |
| 5 | `pipelined_m:data_width=24,n_iter=19,angle_guard=3,frac_guard=2,rounding=round,m=6` | 48964 | 383 | 19.6 | 6 | 0.0502 | 4.03e-06 (2^-17.92) | 17.92 |
| 6 | `pipelined_m:data_width=28,n_iter=19,angle_guard=3,frac_guard=2,rounding=round,m=6` | 55910 | 438 | 17.3 | 6 | 0.0573 | 3.83e-06 (2^-18.00) | 18.00 |
| 7 | `pipelined_m:data_width=25,n_iter=29,angle_guard=-2,frac_guard=1,rounding=trunc,m=7` | 68080 | 450 | 17.5 | 7 | 0.0652 | 3.78e-06 (2^-18.01) | 18.01 |
| 8 | `pipelined_m:data_width=25,n_iter=27,angle_guard=-2,frac_guard=0,rounding=round,m=3` | 69421 | 757 | 41.0 | 11 | 0.083 | 3.54e-06 (2^-18.11) | 18.11 |
| 9 | `pipelined_m:data_width=25,n_iter=30,angle_guard=4,frac_guard=0,rounding=trunc,m=8` | 71717 | 387 | 13.9 | 6 | 0.0638 | 2.02e-06 (2^-18.92) | 18.92 |
| 10 | `pipelined_m:data_width=25,n_iter=30,angle_guard=-1,frac_guard=0,rounding=round,m=4` | 74647 | 686 | 31.1 | 10 | 0.0821 | 2.01e-06 (2^-18.92) | 18.92 |
| 11 | `pipelined_m:data_width=28,n_iter=29,angle_guard=-2,frac_guard=3,rounding=trunc,m=7` | 78844 | 516 | 14.9 | 7 | 0.0752 | 5.95e-07 (2^-20.68) | 20.68 |
| 12 | `pipelined_m:data_width=28,n_iter=26,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 79931 | 890 | 33.9 | 11 | 0.0966 | 5.65e-07 (2^-20.76) | 20.76 |
| 13 | `pipelined:data_width=24,n_iter=23,angle_guard=3,frac_guard=3,rounding=round` | 94219 | 1980 | 104.7 | 25 | 0.166 | 5.25e-07 (2^-20.86) | 20.86 |
| 14 | `pipelined:data_width=26,n_iter=27,angle_guard=2,frac_guard=2,rounding=trunc` | 113372 | 2408 | 101.6 | 29 | 0.201 | 2.9e-07 (2^-21.72) | 21.72 |
| 15 | `pipelined:data_width=28,n_iter=26,angle_guard=4,frac_guard=0,rounding=round` | 114086 | 2428 | 91.1 | 28 | 0.202 | 1.1e-07 (2^-23.12) | 23.12 |
| 16 | `pipelined:data_width=28,n_iter=27,angle_guard=1,frac_guard=3,rounding=trunc` | 122060 | 2590 | 93.5 | 29 | 0.216 | 8.28e-08 (2^-23.53) | 23.53 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Both allowed families deliver 1 result/cycle, so the throughput constraint (>=1 MSPS) reduces to Fmax >= 1 MHz, which is trivially satisfied at sky130 typical corner for all reasonable widths and iteration counts. The binding constraint is max_abs_err <= 2^-10, which depends only on the accuracy parameters (data_width, n_iter, angle_guard, frac_guard, rounding) and is identical across all families. Since the selection rule is min area_um2, the key question is which family achieves the required accuracy with the least area. pipelined_m dominates pipelined on area for the same accuracy (fewer registers), so I expect the Pareto front to be dominated by pipelined_m points, with pipelined contributing only at the high-accuracy end if needed. I split the budget 50/50 between the two families: pipelined_m is the primary candidate for the minimum-area design, while pipelined provides a reference and may contribute distinct points on the accuracy_bits axis for hypervolume. Full registry ranges are used so Optuna can locate the exact error-constraint boundary and map the trade-off curve; the reserved front-mapping portion of the budget will then refine the Pareto front over these ranges. No families outside my assignment are used.*)
- `pipelined` (30 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Full per-stage pipeline gives 1 result/cycle, so throughput_msps = Fmax. To hit >=1 MSPS we need Fmax >= 1 MHz, which is trivially met at sky130 typical corner for any sane width. The binding constraint is max_abs_err <= 2^-10, which depends only on data_width, n_iter, angle_guard, frac_guard, rounding. Since area is the sole selection objective and pipelined has the highest area (a register per stage), I want the search to find the minimum-area point that still satisfies the error constraint, and to map how accuracy_bits trades off against area as n_iter/data_width grow. Sweeping the full registry ranges lets Optuna find the exact knee where error just meets 2^-10 with minimal area, and also populate the accuracy_bits objective for hypervolume.
- `pipelined_m` (30 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* pipelined_m registers every m stages, so it has fewer flip-flops and less area than pipelined for the same N, while still delivering 1 result/cycle (throughput = Fmax >= 1 MSPS easily met). The extra parameter m (2..8) lets the search trade area against latency and Fmax: larger m means fewer registers (lower area) but longer combinational chains per stage group (lower Fmax, though Fmax only needs to be >= 1 MHz here so this is unlikely to bind). This family is the most promising for the min-area selection rule because it can achieve the same accuracy as pipelined with strictly less area. Sweeping the full ranges including m lets Optuna find the global minimum-area feasible point and map the area-vs-accuracy trade-off curve for hypervolume.

**Result (code):** 60 evaluations this round, 60 total; 48 feasible; hypervolume 2.726e+04 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 7 distinct designs spanning area 33708-81046 um^2 and accuracy 14.3-19.2 bits. The minimum area design (pipelined_m, 33708 um^2) meets all constraints: throughput 22.7 MSPS >= 1 MSPS and max_abs_err 4.85e-05 <= 2^-10 (0.000976562). The front covers the trade-off space adequately for the hypervolume objective, and the selection rule (min area) clearly points to the 33708 um^2 design. Since this is the final round, stopping is appropriate.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 2.726e+04 (gain this round: n/a (first round)).
Feasible designs: 48 of 60 evaluations (41 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 242
- max_abs_err <= 0.000976562: 20% violate; best seen 1.66e-06 (2^-19.20)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=19 n_iter=17 angle_guard=4 frac_guard=1 rounding=trunc m=6] area_um2=33708, accuracy_bits=14.3, ffs=242, throughput_msps=22.7, max_abs_err=4.85e-05 (2^-14.33), power_index=0.0333
- pipelined_m [data_width=22 n_iter=19 angle_guard=2 frac_guard=3 rounding=trunc m=8] area_um2=43058, accuracy_bits=17.3, ffs=276, throughput_msps=15.9, max_abs_err=6.24e-06 (2^-17.29), power_index=0.0407
- pipelined_m [data_width=22 n_iter=19 angle_guard=2 frac_guard=3 rounding=trunc m=7] area_um2=43058, accuracy_bits=17.3, ffs=276, throughput_msps=18.1, max_abs_err=6.24e-06 (2^-17.29), power_index=0.0407
- pipelined [data_width=24 n_iter=19 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=70513, accuracy_bits=17.5, ffs=1513, throughput_msps=108, max_abs_err=5.58e-06 (2^-17.45), power_index=0.126
- pipelined_m [data_width=25 n_iter=30 angle_guard=4 frac_guard=0 rounding=trunc m=8] area_um2=71717, accuracy_bits=18.9, ffs=387, throughput_msps=13.9, max_abs_err=2.02e-06 (2^-18.92), power_index=0.0638
- pipelined_m [data_width=25 n_iter=30 angle_guard=-1 frac_guard=0 rounding=round m=4] area_um2=74647, accuracy_bits=18.9, ffs=686, throughput_msps=31.1, max_abs_err=2.01e-06 (2^-18.92), power_index=0.0821
- pipelined [data_width=26 n_iter=21 angle_guard=-1 frac_guard=0 rounding=round] area_um2=81046, accuracy_bits=19.2, ffs=1734, throughput_msps=108, max_abs_err=1.66e-06 (2^-19.20), power_index=0.144
Front coverage: area_um2 33708..81046 (HV reference 40000); accuracy_bits 14.3..19.2 (HV reference 10); data_width on the front 19..26 (registry 8..28).

Per family:
- pipelined: 30 evals, 21 feasible; max throughput seen 242 MSPS; best accuracy 19.20 bits; best feasible area_um2=44252; feasible ranges: data_width 12..26, n_iter 16..30, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 30 evals, 27 feasible; max throughput seen 72.3 MSPS; best accuracy 18.92 bits; best feasible area_um2=33708; feasible ranges: data_width 19..25, n_iter 17..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (29 evals): data_width=18..28, n_iter=15..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (5 front designs; box front_anchored)
- `pipelined` (11 evals): data_width=23..28, n_iter=17..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 88 feasible; hypervolume 2.901e+04 (+6.4%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 7 distinct designs spanning area 33708-81046 um^2 and accuracy 14.3-19.2 bits. The minimum area design (pipelined_m, 33708 um^2) meets all constraints: throughput 22.7 MSPS >= 1 MSPS and max_abs_err 4.85e-05 <= 2^-10 (0.000976562). The front covers the trade-off space adequately for the hypervolume objective, and the selection rule (min area) clearly points to the 33708 um^2 design. Since this is the final round, stopping is appropriate.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 2.901e+04 (gain this round: +6.4%).
Feasible designs: 88 of 100 evaluations (79 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 242
- max_abs_err <= 0.000976562: 12% violate; best seen 8.28e-08 (2^-23.53)

Pareto front (feasible, 17 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=18 n_iter=18 angle_guard=-2 frac_guard=0 rounding=round m=4] area_um2=32548, accuracy_bits=11.5, ffs=325, throughput_msps=41.5, max_abs_err=0.000344 (2^-11.51), power_index=0.0373
- pipelined_m [data_width=22 n_iter=19 angle_guard=2 frac_guard=3 rounding=trunc m=8] area_um2=43058, accuracy_bits=17.3, ffs=276, throughput_msps=15.9, max_abs_err=6.24e-06 (2^-17.29), power_index=0.0407
- pipelined_m [data_width=24 n_iter=19 angle_guard=3 frac_guard=2 rounding=trunc m=6] area_um2=47693, accuracy_bits=17.8, ffs=381, throughput_msps=19.6, max_abs_err=4.32e-06 (2^-17.82), power_index=0.0493
- pipelined_m [data_width=24 n_iter=19 angle_guard=3 frac_guard=2 rounding=round m=6] area_um2=48964, accuracy_bits=17.9, ffs=383, throughput_msps=19.6, max_abs_err=4.03e-06 (2^-17.92), power_index=0.0502
- pipelined_m [data_width=25 n_iter=29 angle_guard=-2 frac_guard=1 rounding=trunc m=7] area_um2=68080, accuracy_bits=18, ffs=450, throughput_msps=17.5, max_abs_err=3.78e-06 (2^-18.01), power_index=0.0652
- pipelined_m [data_width=25 n_iter=30 angle_guard=4 frac_guard=0 rounding=trunc m=8] area_um2=71717, accuracy_bits=18.9, ffs=387, throughput_msps=13.9, max_abs_err=2.02e-06 (2^-18.92), power_index=0.0638
- pipelined_m [data_width=28 n_iter=29 angle_guard=-2 frac_guard=3 rounding=trunc m=7] area_um2=78844, accuracy_bits=20.7, ffs=516, throughput_msps=14.9, max_abs_err=5.95e-07 (2^-20.68), power_index=0.0752
- pipelined_m [data_width=28 n_iter=26 angle_guard=-2 frac_guard=3 rounding=trunc m=3] area_um2=79931, accuracy_bits=20.8, ffs=890, throughput_msps=33.9, max_abs_err=5.65e-07 (2^-20.76), power_index=0.0966
- pipelined [data_width=26 n_iter=27 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=113372, accuracy_bits=21.7, ffs=2408, throughput_msps=102, max_abs_err=2.9e-07 (2^-21.72), power_index=0.201
- pipelined [data_width=28 n_iter=27 angle_guard=1 frac_guard=3 rounding=trunc] area_um2=122060, accuracy_bits=23.5, ffs=2590, throughput_msps=93.5, max_abs_err=8.28e-08 (2^-23.53), power_index=0.216
Front coverage: area_um2 32548..122060 (HV reference 40000); accuracy_bits 11.5..23.5 (HV reference 10); data_width on the front 18..28 (registry 8..28).

Per family:
- pipelined: 41 evals, 32 feasible; max throughput seen 242 MSPS; best accuracy 23.53 bits; best feasible area_um2=44252; feasible ranges: data_width 12..28, n_iter 16..30, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 59 evals, 56 feasible; max throughput seen 72.3 MSPS; best accuracy 20.76 bits; best feasible area_um2=32548; feasible ranges: data_width 18..28, n_iter 16..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4399 in, 1392 out
- provider-reported cost: $0.0021
- full prompts and replies: `llm_trace.jsonl`

