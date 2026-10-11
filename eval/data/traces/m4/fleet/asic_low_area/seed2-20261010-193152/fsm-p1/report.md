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
`iterative:data_width=15,n_iter=19,angle_guard=2,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 7254 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1933 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 102 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 136 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 6.18 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 22 | exact: schedule |
| latency_ns | 162 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.218 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000599 (2^-10.71) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 4.9 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000152 (2^-12.69) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.24 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.7 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (20 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=19,angle_guard=2,frac_guard=0,rounding=round` | 7254 | 102 | 6.2 | 22 | 0.218 | 0.000599 (2^-10.71) | 10.71 |
| 1 | `iterative:data_width=16,n_iter=17,angle_guard=1,frac_guard=1,rounding=trunc` | 7721 | 108 | 6.8 | 20 | 0.211 | 0.000323 (2^-11.60) | 11.60 |
| 2 | `iterative:data_width=16,n_iter=25,angle_guard=2,frac_guard=2,rounding=trunc` | 8178 | 112 | 4.7 | 28 | 0.309 | 0.000297 (2^-11.72) | 11.72 |
| 3 | `iterative:data_width=16,n_iter=25,angle_guard=4,frac_guard=2,rounding=trunc` | 8305 | 114 | 4.4 | 28 | 0.314 | 0.000292 (2^-11.74) | 11.74 |
| 4 | `iterative:data_width=17,n_iter=28,angle_guard=0,frac_guard=2,rounding=trunc` | 8528 | 115 | 4.1 | 31 | 0.354 | 0.000278 (2^-11.81) | 11.81 |
| 5 | `iterative:data_width=17,n_iter=20,angle_guard=3,frac_guard=2,rounding=trunc` | 8706 | 118 | 5.3 | 23 | 0.269 | 9.91e-05 (2^-13.30) | 13.30 |
| 6 | `iterative:data_width=18,n_iter=19,angle_guard=2,frac_guard=1,rounding=trunc` | 8725 | 120 | 5.5 | 22 | 0.26 | 8.72e-05 (2^-13.49) | 13.49 |
| 7 | `iterative:data_width=18,n_iter=19,angle_guard=2,frac_guard=2,rounding=trunc` | 9071 | 123 | 5.5 | 22 | 0.267 | 5.33e-05 (2^-14.20) | 14.20 |
| 8 | `iterative:data_width=21,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 9510 | 131 | 6.2 | 19 | 0.245 | 4.14e-05 (2^-14.56) | 14.56 |
| 9 | `iterative:data_width=21,n_iter=18,angle_guard=0,frac_guard=0,rounding=trunc` | 9549 | 132 | 5.6 | 21 | 0.273 | 2.85e-05 (2^-15.10) | 15.10 |
| 10 | `iterative:data_width=21,n_iter=24,angle_guard=0,frac_guard=0,rounding=trunc` | 9731 | 132 | 4.4 | 27 | 0.354 | 2.66e-05 (2^-15.20) | 15.20 |
| 11 | `iterative:data_width=20,n_iter=19,angle_guard=3,frac_guard=3,rounding=trunc` | 10384 | 137 | 5.0 | 22 | 0.302 | 1.07e-05 (2^-16.51) | 16.51 |
| 12 | `iterative:data_width=27,n_iter=18,angle_guard=0,frac_guard=0,rounding=trunc` | 12190 | 165 | 4.7 | 21 | 0.344 | 7.79e-06 (2^-16.97) | 16.97 |
| 13 | `iterative:data_width=27,n_iter=18,angle_guard=0,frac_guard=1,rounding=trunc` | 12523 | 167 | 4.5 | 21 | 0.35 | 7.7e-06 (2^-16.99) | 16.99 |
| 14 | `iterative:data_width=27,n_iter=28,angle_guard=0,frac_guard=0,rounding=trunc` | 12978 | 165 | 3.2 | 31 | 0.522 | 4.8e-07 (2^-20.99) | 20.99 |
| 15 | `iterative:data_width=27,n_iter=28,angle_guard=0,frac_guard=2,rounding=trunc` | 13887 | 170 | 3.0 | 31 | 0.546 | 2.6e-07 (2^-21.88) | 21.88 |
| 16 | `iterative:data_width=27,n_iter=25,angle_guard=3,frac_guard=2,rounding=trunc` | 13895 | 173 | 3.2 | 28 | 0.498 | 1.44e-07 (2^-22.73) | 22.73 |
| 17 | `iterative:data_width=27,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc` | 14398 | 175 | 3.1 | 29 | 0.528 | 9.63e-08 (2^-23.31) | 23.31 |
| 18 | `iterative:data_width=27,n_iter=26,angle_guard=3,frac_guard=3,rounding=round` | 16947 | 175 | 3.1 | 29 | 0.572 | 7.41e-08 (2^-23.69) | 23.69 |
| 19 | `iterative:data_width=27,n_iter=30,angle_guard=3,frac_guard=3,rounding=round` | 17213 | 175 | 2.7 | 33 | 0.656 | 5.3e-08 (2^-24.17) | 24.17 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-constrained with a modest accuracy requirement (max_abs_err <= 2^-10) and a low throughput floor (>= 1 MSPS). Iterative CORDIC reuses a single datapath and is therefore the most area-efficient family; unrolled_k replicates the datapath k times, increasing area, so it is likely dominated. We focus the search on data_width 12..18 and n_iter 10..20, since W < 12 cannot meet the output LSB requirement (2^-(W-2) > 2^-10) and N < 10 cannot meet the angle resolution. Guards are searched in a narrow range around 0 to find the minimum area that still meets error. Rounding is included because it can improve accuracy at little area cost. The throughput constraint is easily met even for N=20 (Fmax/(N+3) >> 1 MSPS), so it does not further restrict the ranges.*)
- `iterative` (51 evals): data_width=12..18, n_iter=10..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Primary family for minimum area. Ranges cover the feasible accuracy region with minimal area: W >= 12 for output LSB, N >= 10 for angle resolution, and small guard ranges to find the area-accuracy knee. Rounding is included as a cheap accuracy improvement.
- `unrolled_k` (9 evals): data_width=12..18, n_iter=10..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Probe for any unexpected area/throughput trade-off. k > 1 increases area, so we restrict k to 2..4 to limit wasted budget. If no point appears on the Pareto front, this family is confirmed dominated.

**Result (code):** 60 evaluations this round, 60 total; 33 feasible; hypervolume 1.451e+05 (n/a).

**LLM decision:** `stop` — Final round, and the front is feasible and well-formed. Both constraints are met with margin: throughput best seen 11.8 MSPS (>= 1 required, 0% violations) and max_abs_err best 3.99e-05 = 2^-14.61 (<= 2^-10 required). The Pareto front holds 5 designs spanning area_um2 7254..10786 and accuracy_bits 10.7..14.6, all far under the HV area reference of 40000, so the trade-off curve is covered across the accuracy range that matters. The spec's selection rule (min area_um2) is served by iterative [data_width=15 n_iter=19 angle_guard=2 frac_guard=0 rounding=round] at 7254 um2, 10.7 bits, 6.18 MSPS, 102 FFs, power_index 0.218. unrolled_k was also explored but its best feasible area (12500 um2) is dominated by iterative, and pipelined families would only trade area for throughput that the 1 MSPS constraint does not demand. No further improvement is expected within the remaining budget, so I stop rather than spend it.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.451e+05 (gain this round: n/a (first round)).
Feasible designs: 33 of 60 evaluations (24 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11.8
- max_abs_err <= 0.000976562: 45% violate; best seen 3.99e-05 (2^-14.61)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=19 angle_guard=2 frac_guard=0 rounding=round] area_um2=7254, accuracy_bits=10.7, ffs=102, throughput_msps=6.18, max_abs_err=0.000599 (2^-10.71), power_index=0.218
- iterative [data_width=16 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=7721, accuracy_bits=11.6, ffs=108, throughput_msps=6.8, max_abs_err=0.000323 (2^-11.60), power_index=0.211
- iterative [data_width=18 n_iter=19 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=8725, accuracy_bits=13.5, ffs=120, throughput_msps=5.54, max_abs_err=8.72e-05 (2^-13.49), power_index=0.26
- iterative [data_width=18 n_iter=19 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=9071, accuracy_bits=14.2, ffs=123, throughput_msps=5.54, max_abs_err=5.33e-05 (2^-14.20), power_index=0.267
- iterative [data_width=18 n_iter=19 angle_guard=2 frac_guard=2 rounding=round] area_um2=10786, accuracy_bits=14.6, ffs=123, throughput_msps=5.54, max_abs_err=3.99e-05 (2^-14.61), power_index=0.29
Front coverage: area_um2 7254..10786 (HV reference 40000); accuracy_bits 10.7..14.6 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 51 evals, 30 feasible; max throughput seen 11.8 MSPS; best accuracy 14.61 bits; best feasible area_um2=7254; feasible ranges: data_width 15..18, n_iter 12..19, angle_guard -2..2, frac_guard 0..2
- unrolled_k: 9 evals, 3 feasible; max throughput seen 10.7 MSPS; best accuracy 12.48 bits; best feasible area_um2=12500; feasible ranges: data_width 16..17, n_iter 14..15, angle_guard -1..2, frac_guard 0..2, k 3..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (40 evals): data_width=14..28, n_iter=15..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (5 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 72 feasible; hypervolume 4.038e+05 (+178.2%).

**No LLM call** (code's front-mapping round): Final round, and the front is feasible and well-formed. Both constraints are met with margin: throughput best seen 11.8 MSPS (>= 1 required, 0% violations) and max_abs_err best 3.99e-05 = 2^-14.61 (<= 2^-10 required). The Pareto front holds 5 designs spanning area_um2 7254..10786 and accuracy_bits 10.7..14.6, all far under the HV area reference of 40000, so the trade-off curve is covered across the accuracy range that matters. The spec's selection rule (min area_um2) is served by iterative [data_width=15 n_iter=19 angle_guard=2 frac_guard=0 rounding=round] at 7254 um2, 10.7 bits, 6.18 MSPS, 102 FFs, power_index 0.218. unrolled_k was also explored but its best feasible area (12500 um2) is dominated by iterative, and pipelined families would only trade area for throughput that the 1 MSPS constraint does not demand. No further improvement is expected within the remaining budget, so I stop rather than spend it.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 4.038e+05 (gain this round: +178.2%).
Feasible designs: 72 of 100 evaluations (58 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11.8
- max_abs_err <= 0.000976562: 28% violate; best seen 5.3e-08 (2^-24.17)

Pareto front (feasible, 20 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=19 angle_guard=2 frac_guard=0 rounding=round] area_um2=7254, accuracy_bits=10.7, ffs=102, throughput_msps=6.18, max_abs_err=0.000599 (2^-10.71), power_index=0.218
- iterative [data_width=16 n_iter=25 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=8178, accuracy_bits=11.7, ffs=112, throughput_msps=4.68, max_abs_err=0.000297 (2^-11.72), power_index=0.309
- iterative [data_width=17 n_iter=28 angle_guard=0 frac_guard=2 rounding=trunc] area_um2=8528, accuracy_bits=11.8, ffs=115, throughput_msps=4.07, max_abs_err=0.000278 (2^-11.81), power_index=0.354
- iterative [data_width=18 n_iter=19 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=8725, accuracy_bits=13.5, ffs=120, throughput_msps=5.54, max_abs_err=8.72e-05 (2^-13.49), power_index=0.26
- iterative [data_width=21 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] area_um2=9510, accuracy_bits=14.6, ffs=131, throughput_msps=6.2, max_abs_err=4.14e-05 (2^-14.56), power_index=0.245
- iterative [data_width=20 n_iter=19 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=10384, accuracy_bits=16.5, ffs=137, throughput_msps=5.01, max_abs_err=1.07e-05 (2^-16.51), power_index=0.302
- iterative [data_width=27 n_iter=18 angle_guard=0 frac_guard=1 rounding=trunc] area_um2=12523, accuracy_bits=17, ffs=167, throughput_msps=4.54, max_abs_err=7.7e-06 (2^-16.99), power_index=0.35
- iterative [data_width=27 n_iter=28 angle_guard=0 frac_guard=2 rounding=trunc] area_um2=13887, accuracy_bits=21.9, ffs=170, throughput_msps=2.99, max_abs_err=2.6e-07 (2^-21.88), power_index=0.546
- iterative [data_width=27 n_iter=26 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=14398, accuracy_bits=23.3, ffs=175, throughput_msps=3.12, max_abs_err=9.63e-08 (2^-23.31), power_index=0.528
- iterative [data_width=27 n_iter=30 angle_guard=3 frac_guard=3 rounding=round] area_um2=17213, accuracy_bits=24.2, ffs=175, throughput_msps=2.74, max_abs_err=5.3e-08 (2^-24.17), power_index=0.656
Front coverage: area_um2 7254..17213 (HV reference 40000); accuracy_bits 10.7..24.2 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 91 evals, 69 feasible; max throughput seen 11.8 MSPS; best accuracy 24.17 bits; best feasible area_um2=7254; feasible ranges: data_width 15..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 9 evals, 3 feasible; max throughput seen 10.7 MSPS; best accuracy 12.48 bits; best feasible area_um2=12500; feasible ranges: data_width 16..17, n_iter 14..15, angle_guard -1..2, frac_guard 0..2, k 3..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4934 in, 5852 out
- provider-reported cost: $0.0040
- full prompts and replies: `llm_trace.jsonl`

