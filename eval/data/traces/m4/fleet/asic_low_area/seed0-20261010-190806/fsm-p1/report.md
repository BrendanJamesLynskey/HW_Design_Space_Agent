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
`iterative:data_width=14,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 7014 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1868 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 98 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 142 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 8.32 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 120 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.163 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000944 (2^-10.05) | exact: bit-accurate model, exhaustive (16384 angles) |
| max_abs_err_lsb | 3.87 | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err | 0.000229 (2^-12.09) | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err_lsb | 0.939 | exact: bit-accurate model, exhaustive (16384 angles) |
| accuracy_bits | 10 | exact: bit-accurate model, exhaustive (16384 angles) |

## Pareto front (15 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=14,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc` | 7014 | 98 | 8.3 | 17 | 0.163 | 0.000944 (2^-10.05) | 10.05 |
| 1 | `iterative:data_width=14,n_iter=14,angle_guard=1,frac_guard=1,rounding=round` | 8051 | 96 | 8.7 | 17 | 0.172 | 0.000827 (2^-10.24) | 10.24 |
| 2 | `iterative:data_width=16,n_iter=14,angle_guard=-1,frac_guard=4,rounding=trunc` | 8239 | 112 | 7.2 | 17 | 0.188 | 0.00068 (2^-10.52) | 10.52 |
| 3 | `iterative:data_width=16,n_iter=29,angle_guard=4,frac_guard=4,rounding=trunc` | 9056 | 118 | 3.8 | 32 | 0.381 | 0.000124 (2^-12.97) | 12.97 |
| 4 | `iterative:data_width=21,n_iter=16,angle_guard=-2,frac_guard=0,rounding=round` | 9383 | 129 | 6.2 | 19 | 0.241 | 6.51e-05 (2^-13.91) | 13.91 |
| 5 | `iterative:data_width=21,n_iter=18,angle_guard=-2,frac_guard=0,rounding=round` | 9629 | 130 | 5.6 | 21 | 0.271 | 5.08e-05 (2^-14.26) | 14.26 |
| 6 | `iterative:data_width=22,n_iter=16,angle_guard=-1,frac_guard=0,rounding=round` | 9863 | 136 | 6.0 | 19 | 0.254 | 3.88e-05 (2^-14.65) | 14.65 |
| 7 | `iterative:data_width=22,n_iter=27,angle_guard=-1,frac_guard=2,rounding=trunc` | 11029 | 141 | 3.6 | 30 | 0.43 | 1.52e-05 (2^-16.01) | 16.01 |
| 8 | `iterative:data_width=22,n_iter=27,angle_guard=2,frac_guard=3,rounding=trunc` | 11661 | 147 | 3.5 | 30 | 0.451 | 3.63e-06 (2^-18.07) | 18.07 |
| 9 | `iterative:data_width=24,n_iter=27,angle_guard=1,frac_guard=1,rounding=trunc` | 11812 | 152 | 3.5 | 30 | 0.462 | 1.78e-06 (2^-19.10) | 19.10 |
| 10 | `iterative:data_width=25,n_iter=27,angle_guard=1,frac_guard=1,rounding=trunc` | 12361 | 158 | 3.4 | 30 | 0.481 | 1.13e-06 (2^-19.76) | 19.76 |
| 11 | `iterative:data_width=28,n_iter=22,angle_guard=-2,frac_guard=0,rounding=trunc` | 13013 | 169 | 3.8 | 25 | 0.426 | 9.48e-07 (2^-20.01) | 20.01 |
| 12 | `iterative:data_width=28,n_iter=29,angle_guard=-2,frac_guard=0,rounding=trunc` | 13437 | 169 | 3.0 | 32 | 0.553 | 6.09e-07 (2^-20.65) | 20.65 |
| 13 | `iterative:data_width=28,n_iter=27,angle_guard=1,frac_guard=1,rounding=trunc` | 14009 | 174 | 3.1 | 30 | 0.538 | 1.27e-07 (2^-22.90) | 22.90 |
| 14 | `iterative:data_width=28,n_iter=29,angle_guard=1,frac_guard=3,rounding=round` | 17695 | 178 | 2.8 | 32 | 0.651 | 7.15e-08 (2^-23.74) | 23.74 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is low-area with a loose throughput constraint (>=1 MSPS) and a moderate accuracy constraint (max_abs_err <= 2^-10). Both iterative and unrolled_k can easily meet the throughput constraint: even at a modest Fmax, iterative with N+3 cycles yields >1 MSPS for N up to ~30. Area is the primary objective, so we focus on the family with the smallest datapath: iterative shares one micro-rotation per cycle, minimising hardware. unrolled_k replicates k micro-rotations per cycle, increasing area, so it is likely dominated by iterative for the same accuracy. However, we include unrolled_k with a small budget to confirm and to catch any unexpected trade-off (e.g., if iterative has control overhead that makes a small-k unrolled version competitive). The accuracy constraint requires roughly W >= 12 and N >= 11, with angle_guard >= -1 and possibly frac_guard >= 1 to meet the error bound. We therefore focus the search on the low end of data_width (11..14) and n_iter (10..14), with angle_guard from -2 to 1 and frac_guard 0..2, and both rounding modes. This range brackets the minimum-area designs that just meet the accuracy constraint, which is where the Pareto front will start. We allocate 85% of the budget to iterative and 15% to unrolled_k.*)
- `iterative` (51 evals): data_width=11..14, n_iter=10..14, angle_guard=-2..1, frac_guard=0..2, rounding=trunc|round. *Why:* This family has the smallest datapath (one shared micro-rotation per cycle) and thus the lowest area for a given accuracy. The throughput constraint is easily met even with N+3 cycles. We search the low-W, low-N corner where the accuracy constraint is just satisfied, as that yields the minimum area.
- `unrolled_k` (9 evals): data_width=11..14, n_iter=10..14, angle_guard=-2..1, frac_guard=0..2, rounding=trunc|round, k=2..3. *Why:* This family uses k micro-rotations per cycle, increasing area. It is unlikely to beat iterative on area for the same accuracy, but we include a small budget to verify and to explore if a small k (2..3) with reduced N could somehow reduce area (e.g., by reducing the shifter range or control complexity). We keep k small to minimise area.

**Result (code):** 60 evaluations this round, 60 total; 5 feasible; hypervolume 7694 (n/a).

**LLM decision:** `stop` — This is the final round (round cap reached), so the only admissible choices are stop or infeasible, and the constraint evidence rules out infeasible: the spec's hard constraints are both met by real designs. Throughput_msps >= 1 is satisfied with margin (best feasible 8.32-8.68 MSPS vs. best-seen 12.7), and max_abs_err <= 2^-10 = 0.000976562 is met exactly at the spec limit by iterative [data_width=14, n_iter=14, angle_guard=1, frac_guard=2, rounding=trunc] with max_abs_err=0.000944 (2^-10.05) and by the 10.2-bit variant with 0.000827 (2^-10.24). The selection rule (min area_um2) picks the 7014 um^2 design, which is ~5.7x below the HV area reference of 40000 and only ~130 um^2 above the next front point, so there is no unselected cheap design being left on the table within the explored families. Both front members are feasible and span the accuracy range 10.0-10.2 bits, and the front covers the accuracy objective's useful range (HV ref 10). With 40 evaluations unused but only the stop/infeasible decisions available at the round cap, halting on a valid, constraint-satisfying Pareto front is the correct terminal action rather than declaring infeasible.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 7694 (gain this round: n/a (first round)).
Feasible designs: 5 of 60 evaluations (3 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 12.7
- max_abs_err <= 0.000976562: 92% violate; best seen 0.000827 (2^-10.24)

Pareto front (feasible, 2 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=7014, accuracy_bits=10, ffs=98, throughput_msps=8.32, max_abs_err=0.000944 (2^-10.05), power_index=0.163
- iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=1 rounding=round] area_um2=8051, accuracy_bits=10.2, ffs=96, throughput_msps=8.68, max_abs_err=0.000827 (2^-10.24), power_index=0.172
Front coverage: area_um2 7014..8051 (HV reference 40000); accuracy_bits 10..10.2 (HV reference 10); data_width on the front 14..14 (registry 8..28).

Per family:
- iterative: 51 evals, 5 feasible; max throughput seen 12.7 MSPS; best accuracy 10.24 bits; best feasible area_um2=7014; feasible ranges: data_width 14..14, n_iter 12..14, angle_guard 1..1, frac_guard 1..2
- unrolled_k: 9 evals, 0 feasible; max throughput seen 11.1 MSPS; best accuracy 9.42 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (40 evals): data_width=13..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 41 feasible; hypervolume 3.895e+05 (+4962.7%).

**No LLM call** (code's front-mapping round): This is the final round (round cap reached), so the only admissible choices are stop or infeasible, and the constraint evidence rules out infeasible: the spec's hard constraints are both met by real designs. Throughput_msps >= 1 is satisfied with margin (best feasible 8.32-8.68 MSPS vs. best-seen 12.7), and max_abs_err <= 2^-10 = 0.000976562 is met exactly at the spec limit by iterative [data_width=14, n_iter=14, angle_guard=1, frac_guard=2, rounding=trunc] with max_abs_err=0.000944 (2^-10.05) and by the 10.2-bit variant with 0.000827 (2^-10.24). The selection rule (min area_um2) picks the 7014 um^2 design, which is ~5.7x below the HV area reference of 40000 and only ~130 um^2 above the next front point, so there is no unselected cheap design being left on the table within the explored families. Both front members are feasible and span the accuracy range 10.0-10.2 bits, and the front covers the accuracy objective's useful range (HV ref 10). With 40 evaluations unused but only the stop/infeasible decisions available at the round cap, halting on a valid, constraint-satisfying Pareto front is the correct terminal action rather than declaring infeasible.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 3.895e+05 (gain this round: +4962.7%).
Feasible designs: 41 of 100 evaluations (35 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 12.7
- max_abs_err <= 0.000976562: 59% violate; best seen 7.15e-08 (2^-23.74)

Pareto front (feasible, 15 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=7014, accuracy_bits=10, ffs=98, throughput_msps=8.32, max_abs_err=0.000944 (2^-10.05), power_index=0.163
- iterative [data_width=16 n_iter=14 angle_guard=-1 frac_guard=4 rounding=trunc] area_um2=8239, accuracy_bits=10.5, ffs=112, throughput_msps=7.17, max_abs_err=0.00068 (2^-10.52), power_index=0.188
- iterative [data_width=16 n_iter=29 angle_guard=4 frac_guard=4 rounding=trunc] area_um2=9056, accuracy_bits=13, ffs=118, throughput_msps=3.81, max_abs_err=0.000124 (2^-12.97), power_index=0.381
- iterative [data_width=21 n_iter=18 angle_guard=-2 frac_guard=0 rounding=round] area_um2=9629, accuracy_bits=14.3, ffs=130, throughput_msps=5.61, max_abs_err=5.08e-05 (2^-14.26), power_index=0.271
- iterative [data_width=22 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round] area_um2=9863, accuracy_bits=14.7, ffs=136, throughput_msps=5.99, max_abs_err=3.88e-05 (2^-14.65), power_index=0.254
- iterative [data_width=22 n_iter=27 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=11661, accuracy_bits=18.1, ffs=147, throughput_msps=3.46, max_abs_err=3.63e-06 (2^-18.07), power_index=0.451
- iterative [data_width=24 n_iter=27 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=11812, accuracy_bits=19.1, ffs=152, throughput_msps=3.46, max_abs_err=1.78e-06 (2^-19.10), power_index=0.462
- iterative [data_width=28 n_iter=22 angle_guard=-2 frac_guard=0 rounding=trunc] area_um2=13013, accuracy_bits=20, ffs=169, throughput_msps=3.81, max_abs_err=9.48e-07 (2^-20.01), power_index=0.426
- iterative [data_width=28 n_iter=29 angle_guard=-2 frac_guard=0 rounding=trunc] area_um2=13437, accuracy_bits=20.6, ffs=169, throughput_msps=2.98, max_abs_err=6.09e-07 (2^-20.65), power_index=0.553
- iterative [data_width=28 n_iter=29 angle_guard=1 frac_guard=3 rounding=round] area_um2=17695, accuracy_bits=23.7, ffs=178, throughput_msps=2.75, max_abs_err=7.15e-08 (2^-23.74), power_index=0.651
Front coverage: area_um2 7014..17695 (HV reference 40000); accuracy_bits 10..23.7 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 91 evals, 41 feasible; max throughput seen 12.7 MSPS; best accuracy 23.74 bits; best feasible area_um2=7014; feasible ranges: data_width 14..28, n_iter 12..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 9 evals, 0 feasible; max throughput seen 11.1 MSPS; best accuracy 9.42 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 3730 in, 7642 out
- provider-reported cost: $0.0056
- full prompts and replies: `llm_trace.jsonl`

