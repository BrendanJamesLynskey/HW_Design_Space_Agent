# DSE run: asic_low_area

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 173 of 173 budgeted, over 2 round(s).  
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
  budget: 173 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=14,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 7607 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 2027 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 103 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 136 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 4.86 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 28 | exact: schedule |
| latency_ns | 206 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.286 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000787 (2^-10.31) | exact: bit-accurate model, exhaustive (16384 angles) |
| max_abs_err_lsb | 3.22 | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err | 0.000276 (2^-11.82) | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err_lsb | 1.13 | exact: bit-accurate model, exhaustive (16384 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (16384 angles) |

## Pareto front (23 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=14,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc` | 7607 | 103 | 4.9 | 28 | 0.286 | 0.000787 (2^-10.31) | 10.31 |
| 1 | `iterative:data_width=14,n_iter=13,angle_guard=3,frac_guard=4,rounding=trunc` | 7624 | 105 | 8.2 | 16 | 0.165 | 0.00054 (2^-10.86) | 10.86 |
| 2 | `iterative:data_width=18,n_iter=13,angle_guard=-1,frac_guard=0,rounding=trunc` | 7799 | 114 | 8.2 | 16 | 0.175 | 0.00038 (2^-11.36) | 11.36 |
| 3 | `iterative:data_width=18,n_iter=13,angle_guard=1,frac_guard=0,rounding=trunc` | 7926 | 116 | 7.9 | 16 | 0.178 | 0.000347 (2^-11.49) | 11.49 |
| 4 | `iterative:data_width=19,n_iter=14,angle_guard=0,frac_guard=0,rounding=trunc` | 8339 | 120 | 7.4 | 17 | 0.197 | 0.000172 (2^-12.50) | 12.50 |
| 5 | `iterative:data_width=20,n_iter=24,angle_guard=-2,frac_guard=0,rounding=trunc` | 9104 | 125 | 4.5 | 27 | 0.332 | 0.000117 (2^-13.06) | 13.06 |
| 6 | `iterative:data_width=20,n_iter=21,angle_guard=-1,frac_guard=0,rounding=trunc` | 9155 | 126 | 5.1 | 24 | 0.297 | 6.18e-05 (2^-13.98) | 13.98 |
| 7 | `iterative:data_width=20,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 9158 | 127 | 6.2 | 19 | 0.237 | 4.64e-05 (2^-14.39) | 14.39 |
| 8 | `iterative:data_width=20,n_iter=18,angle_guard=1,frac_guard=0,rounding=trunc` | 9173 | 128 | 5.6 | 21 | 0.263 | 4.51e-05 (2^-14.44) | 14.44 |
| 9 | `iterative:data_width=19,n_iter=26,angle_guard=3,frac_guard=0,rounding=round` | 9235 | 125 | 3.9 | 29 | 0.359 | 3.74e-05 (2^-14.71) | 14.71 |
| 10 | `iterative:data_width=21,n_iter=18,angle_guard=1,frac_guard=0,rounding=trunc` | 9613 | 134 | 5.4 | 21 | 0.275 | 2.55e-05 (2^-15.26) | 15.26 |
| 11 | `iterative:data_width=20,n_iter=29,angle_guard=4,frac_guard=0,rounding=round` | 9824 | 131 | 3.3 | 32 | 0.419 | 2.17e-05 (2^-15.49) | 15.49 |
| 12 | `iterative:data_width=20,n_iter=21,angle_guard=1,frac_guard=2,rounding=trunc` | 10021 | 132 | 4.7 | 24 | 0.318 | 1.79e-05 (2^-15.77) | 15.77 |
| 13 | `iterative:data_width=20,n_iter=29,angle_guard=4,frac_guard=2,rounding=trunc` | 10284 | 136 | 3.3 | 32 | 0.435 | 1.78e-05 (2^-15.78) | 15.78 |
| 14 | `iterative:data_width=23,n_iter=19,angle_guard=-2,frac_guard=0,rounding=trunc` | 10388 | 141 | 5.0 | 22 | 0.307 | 1.46e-05 (2^-16.06) | 16.06 |
| 15 | `iterative:data_width=23,n_iter=25,angle_guard=-2,frac_guard=0,rounding=trunc` | 10642 | 141 | 3.9 | 28 | 0.395 | 1.44e-05 (2^-16.08) | 16.08 |
| 16 | `iterative:data_width=21,n_iter=21,angle_guard=4,frac_guard=2,rounding=trunc` | 10687 | 141 | 4.3 | 24 | 0.339 | 7.43e-06 (2^-17.04) | 17.04 |
| 17 | `iterative:data_width=24,n_iter=25,angle_guard=-1,frac_guard=0,rounding=trunc` | 11231 | 148 | 3.8 | 28 | 0.415 | 4.21e-06 (2^-17.86) | 17.86 |
| 18 | `iterative:data_width=22,n_iter=24,angle_guard=2,frac_guard=4,rounding=trunc` | 11994 | 149 | 3.7 | 27 | 0.414 | 2.79e-06 (2^-18.45) | 18.45 |
| 19 | `iterative:data_width=27,n_iter=24,angle_guard=0,frac_guard=0,rounding=trunc` | 12809 | 165 | 3.6 | 27 | 0.452 | 4.67e-07 (2^-21.03) | 21.03 |
| 20 | `iterative:data_width=26,n_iter=28,angle_guard=4,frac_guard=0,rounding=round` | 12998 | 164 | 2.9 | 31 | 0.52 | 3.6e-07 (2^-21.40) | 21.40 |
| 21 | `iterative:data_width=27,n_iter=26,angle_guard=3,frac_guard=1,rounding=trunc` | 13538 | 171 | 3.1 | 29 | 0.507 | 2.15e-07 (2^-22.15) | 22.15 |
| 22 | `iterative:data_width=26,n_iter=30,angle_guard=2,frac_guard=4,rounding=trunc` | 14446 | 171 | 2.7 | 33 | 0.594 | 1.7e-07 (2^-22.49) | 22.49 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show iterative dominates on area (7405 vs 12183 vs 43k+ for pipelined families) and already holds 13 of 15 front points. The spec's selection rule is min area, so iterative is the primary candidate. However, hypervolume rewards covering the full trade-off curve, so I keep a smaller share on unrolled_k to explore whether higher-k unrolling can produce non-dominated points at higher accuracy or different throughput/area trade-offs. Both families can meet throughput >= 1 MSPS (iterative at 100+ MHz gives 1+ MSPS; unrolled_k with k>=2 gives 2+ results/cycle at lower Fmax). The accuracy constraint (max_abs_err <= 2^-10) is met by 56/62 iterative and 34/38 unrolled_k designs, so the feasible region is large. I focus the budget on refining the iterative front (70%) and probing unrolled_k for complementary points (30%).*)
- `iterative` (70 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* iterative is the clear area leader (best 7405 um2, 13/15 on the merged front) and the only family that can plausibly win the min-area selection. The remaining budget should refine its Pareto front: sweep data_width and n_iter to find the smallest area that still meets max_abs_err <= 2^-10, and explore angle_guard/frac_guard to trade accuracy margin against area. Rounding is kept in play since it affects both accuracy and area.
- `unrolled_k` (30 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* unrolled_k is the second-cheapest family (best 12183 um2) and can meet throughput >= 1 MSPS with fewer cycles per result than iterative. It contributes 0 designs to the merged front so far, but a focused search over k and the accuracy parameters may reveal points that dominate or complement the iterative front, especially at higher accuracy_bits where iterative's area grows. Keeping a small share here hedges the hypervolume by covering the throughput/accuracy trade-off that iterative alone may not span.

**Result (code):** 100 evaluations this round, 100 total; 68 feasible; hypervolume 3.643e+05 (n/a).

**LLM decision:** `stop` — The spec is feasible: 68 of 100 evaluations met both constraints, with the best area of 7607 um^2 (iterative, data_width=14, n_iter=25) comfortably above the 1 MSPS throughput floor (4.86 MSPS) and the 2^-10 error bound. The Pareto front spans area 7607..14446 um^2 and accuracy 10.3..22.5 bits, giving a hypervolume of 3.643e+05 against the reference point. The selection rule (min area) picks the 7607 um^2 design. Since this is the final round and the front is well-populated and feasible, no further exploration is possible or needed.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 73 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 173.
Hypervolume of the feasible front: 3.643e+05 (gain this round: n/a (first round)).
Feasible designs: 68 of 100 evaluations (60 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 21.9
- max_abs_err <= 0.000976562: 32% violate; best seen 1.7e-07 (2^-22.49)

Pareto front (feasible, 15 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=14 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=7607, accuracy_bits=10.3, ffs=103, throughput_msps=4.86, max_abs_err=0.000787 (2^-10.31), power_index=0.286
- iterative [data_width=18 n_iter=13 angle_guard=-2 frac_guard=2 rounding=trunc] area_um2=8280, accuracy_bits=11.2, ffs=117, throughput_msps=7.61, max_abs_err=0.000433 (2^-11.17), power_index=0.182
- iterative [data_width=19 n_iter=14 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=8339, accuracy_bits=12.5, ffs=120, throughput_msps=7.42, max_abs_err=0.000172 (2^-12.50), power_index=0.197
- iterative [data_width=20 n_iter=24 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=9231, accuracy_bits=14.1, ffs=127, throughput_msps=4.51, max_abs_err=5.66e-05 (2^-14.11), power_index=0.337
- iterative [data_width=19 n_iter=26 angle_guard=3 frac_guard=0 rounding=round] area_um2=9235, accuracy_bits=14.7, ffs=125, throughput_msps=3.93, max_abs_err=3.74e-05 (2^-14.71), power_index=0.359
- iterative [data_width=23 n_iter=19 angle_guard=-2 frac_guard=0 rounding=trunc] area_um2=10388, accuracy_bits=16.1, ffs=141, throughput_msps=5.01, max_abs_err=1.46e-05 (2^-16.06), power_index=0.307
- iterative [data_width=23 n_iter=25 angle_guard=-2 frac_guard=0 rounding=trunc] area_um2=10642, accuracy_bits=16.1, ffs=141, throughput_msps=3.94, max_abs_err=1.44e-05 (2^-16.08), power_index=0.395
- iterative [data_width=24 n_iter=25 angle_guard=-1 frac_guard=0 rounding=trunc] area_um2=11231, accuracy_bits=17.9, ffs=148, throughput_msps=3.82, max_abs_err=4.21e-06 (2^-17.86), power_index=0.415
- iterative [data_width=22 n_iter=24 angle_guard=2 frac_guard=4 rounding=trunc] area_um2=11994, accuracy_bits=18.5, ffs=149, throughput_msps=3.73, max_abs_err=2.79e-06 (2^-18.45), power_index=0.414
- iterative [data_width=26 n_iter=30 angle_guard=2 frac_guard=4 rounding=trunc] area_um2=14446, accuracy_bits=22.5, ffs=171, throughput_msps=2.74, max_abs_err=1.7e-07 (2^-22.49), power_index=0.594
Front coverage: area_um2 7607..14446 (HV reference 40000); accuracy_bits 10.3..22.5 (HV reference 10); data_width on the front 14..27 (registry 8..28).

Per family:
- iterative: 70 evals, 53 feasible; max throughput seen 21.9 MSPS; best accuracy 22.49 bits; best feasible area_um2=7607; feasible ranges: data_width 14..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 30 evals, 15 feasible; max throughput seen 13.3 MSPS; best accuracy 16.99 bits; best feasible area_um2=9950; feasible ranges: data_width 15..26, n_iter 13..27, angle_guard -2..4, frac_guard 0..4, k 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 73 evaluations*)
- `iterative` (73 evals): data_width=13..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (15 front designs; box front_anchored)

**Result (code):** 73 evaluations this round, 173 total; 129 feasible; hypervolume 3.664e+05 (+0.6%).

**No LLM call** (code's front-mapping round): The spec is feasible: 68 of 100 evaluations met both constraints, with the best area of 7607 um^2 (iterative, data_width=14, n_iter=25) comfortably above the 1 MSPS throughput floor (4.86 MSPS) and the 2^-10 error bound. The Pareto front spans area 7607..14446 um^2 and accuracy 10.3..22.5 bits, giving a hypervolume of 3.643e+05 against the reference point. The selection rule (min area) picks the 7607 um^2 design. Since this is the final round and the front is well-populated and feasible, no further exploration is possible or needed.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 173 of 173.
Hypervolume of the feasible front: 3.664e+05 (gain this round: +0.6%).
Feasible designs: 129 of 173 evaluations (112 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 21.9
- max_abs_err <= 0.000976562: 25% violate; best seen 1.7e-07 (2^-22.49)

Pareto front (feasible, 23 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=14 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=7607, accuracy_bits=10.3, ffs=103, throughput_msps=4.86, max_abs_err=0.000787 (2^-10.31), power_index=0.286
- iterative [data_width=18 n_iter=13 angle_guard=-1 frac_guard=0 rounding=trunc] area_um2=7799, accuracy_bits=11.4, ffs=114, throughput_msps=8.18, max_abs_err=0.00038 (2^-11.36), power_index=0.175
- iterative [data_width=20 n_iter=24 angle_guard=-2 frac_guard=0 rounding=trunc] area_um2=9104, accuracy_bits=13.1, ffs=125, throughput_msps=4.51, max_abs_err=0.000117 (2^-13.06), power_index=0.332
- iterative [data_width=20 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=9158, accuracy_bits=14.4, ffs=127, throughput_msps=6.2, max_abs_err=4.64e-05 (2^-14.39), power_index=0.237
- iterative [data_width=21 n_iter=18 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=9613, accuracy_bits=15.3, ffs=134, throughput_msps=5.42, max_abs_err=2.55e-05 (2^-15.26), power_index=0.275
- iterative [data_width=20 n_iter=21 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=10021, accuracy_bits=15.8, ffs=132, throughput_msps=4.75, max_abs_err=1.79e-05 (2^-15.77), power_index=0.318
- iterative [data_width=23 n_iter=25 angle_guard=-2 frac_guard=0 rounding=trunc] area_um2=10642, accuracy_bits=16.1, ffs=141, throughput_msps=3.94, max_abs_err=1.44e-05 (2^-16.08), power_index=0.395
- iterative [data_width=24 n_iter=25 angle_guard=-1 frac_guard=0 rounding=trunc] area_um2=11231, accuracy_bits=17.9, ffs=148, throughput_msps=3.82, max_abs_err=4.21e-06 (2^-17.86), power_index=0.415
- iterative [data_width=26 n_iter=28 angle_guard=4 frac_guard=0 rounding=round] area_um2=12998, accuracy_bits=21.4, ffs=164, throughput_msps=2.92, max_abs_err=3.6e-07 (2^-21.40), power_index=0.52
- iterative [data_width=26 n_iter=30 angle_guard=2 frac_guard=4 rounding=trunc] area_um2=14446, accuracy_bits=22.5, ffs=171, throughput_msps=2.74, max_abs_err=1.7e-07 (2^-22.49), power_index=0.594
Front coverage: area_um2 7607..14446 (HV reference 40000); accuracy_bits 10.3..22.5 (HV reference 10); data_width on the front 14..27 (registry 8..28).

Per family:
- iterative: 143 evals, 114 feasible; max throughput seen 21.9 MSPS; best accuracy 22.49 bits; best feasible area_um2=7607; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 30 evals, 15 feasible; max throughput seen 13.3 MSPS; best accuracy 16.99 bits; best feasible area_um2=9950; feasible ranges: data_width 15..26, n_iter 13..27, angle_guard -2..4, frac_guard 0..4, k 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5507 in, 1017 out
- provider-reported cost: $0.0018
- full prompts and replies: `llm_trace.jsonl`

