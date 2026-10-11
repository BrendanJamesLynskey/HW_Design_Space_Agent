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
`iterative:data_width=15,n_iter=12,angle_guard=1,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 6860 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1828 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 100 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 142 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 9.43 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 15 | exact: schedule |
| latency_ns | 106 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.144 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000917 (2^-10.09) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 7.51 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000249 (2^-11.97) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 2.04 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.1 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=12,angle_guard=1,frac_guard=0,rounding=round` | 6860 | 100 | 9.4 | 15 | 0.144 | 0.000917 (2^-10.09) | 10.09 |
| 1 | `iterative:data_width=15,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 7079 | 100 | 7.4 | 19 | 0.184 | 0.000632 (2^-10.63) | 10.63 |
| 2 | `iterative:data_width=15,n_iter=15,angle_guard=3,frac_guard=1,rounding=trunc` | 7296 | 104 | 7.3 | 18 | 0.181 | 0.000569 (2^-10.78) | 10.78 |
| 3 | `iterative:data_width=16,n_iter=15,angle_guard=1,frac_guard=3,rounding=trunc` | 8166 | 112 | 7.0 | 18 | 0.198 | 0.000227 (2^-12.10) | 12.10 |
| 4 | `iterative:data_width=17,n_iter=19,angle_guard=1,frac_guard=1,rounding=trunc` | 8210 | 114 | 6.0 | 22 | 0.246 | 0.00019 (2^-12.36) | 12.36 |
| 5 | `iterative:data_width=21,n_iter=15,angle_guard=-2,frac_guard=0,rounding=round` | 9274 | 129 | 6.5 | 18 | 0.228 | 9.08e-05 (2^-13.43) | 13.43 |
| 6 | `iterative:data_width=21,n_iter=15,angle_guard=4,frac_guard=0,rounding=round` | 9655 | 136 | 5.8 | 18 | 0.238 | 6.66e-05 (2^-13.87) | 13.87 |
| 7 | `iterative:data_width=25,n_iter=15,angle_guard=-2,frac_guard=0,rounding=round` | 10889 | 151 | 5.8 | 18 | 0.267 | 6.18e-05 (2^-13.98) | 13.98 |
| 8 | `iterative:data_width=25,n_iter=21,angle_guard=-2,frac_guard=1,rounding=trunc` | 11844 | 154 | 4.2 | 24 | 0.373 | 3.68e-06 (2^-18.05) | 18.05 |
| 9 | `iterative:data_width=25,n_iter=26,angle_guard=1,frac_guard=1,rounding=trunc` | 12337 | 158 | 3.5 | 29 | 0.465 | 1.01e-06 (2^-19.92) | 19.92 |
| 10 | `iterative:data_width=26,n_iter=29,angle_guard=1,frac_guard=0,rounding=trunc` | 12480 | 161 | 3.1 | 32 | 0.521 | 9.99e-07 (2^-19.93) | 19.93 |
| 11 | `iterative:data_width=26,n_iter=26,angle_guard=1,frac_guard=3,rounding=trunc` | 13734 | 167 | 3.2 | 29 | 0.505 | 3.1e-07 (2^-21.62) | 21.62 |
| 12 | `unrolled_k:data_width=27,n_iter=29,angle_guard=3,frac_guard=4,rounding=round,k=3` | 25558 | 176 | 2.4 | 13 | 0.323 | 4.54e-08 (2^-24.39) | 24.39 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *No fleet facts yet, so I start from first principles on the two families I own. The spec is area-first with a hard accuracy bound (max_abs_err <= 2^-10, i.e. accuracy_bits >= 10) and a hard throughput bound (>= 1 MSPS). Accuracy depends only on data_width, n_iter, angle_guard, frac_guard, rounding, so I bound those tightly around the 10-bit accuracy target: data_width 12-16 and n_iter 10-16 give enough headroom to clear 2^-10 without oversizing the datapath (which would inflate area for no accuracy benefit, since the accuracy_bits reference is 10). angle_guard -2..1 and frac_guard 0..2 let Optuna trade a little accuracy margin against area, and both rounding modes are kept. For the throughput constraint, iterative is the cheapest area but its Fmax is uncertain; unrolled_k with small k (2-4) is the area-minimal way to guarantee >=1 MSPS if iterative falls short. I split the budget 50/50 between the two so the merged front captures the area/accuracy/throughput trade-off and the final min-area selection has a feasible candidate from whichever family clears the constraints. If iterative proves infeasible on throughput, the unrolled_k front still covers the spec; if unrolled_k is too area-heavy, iterative wins on the min-area selection rule.*)
- `iterative` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=-2..1, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the smallest-area family (single shared datapath, no pipeline registers, no k-way fanout). It is the only family I can plausibly use to hit min-area while still meeting >=1 MSPS if Fmax is high enough. I focus data_width 12-16 and n_iter 10-16 because the error constraint (<=2^-10) is the binding accuracy bound: too few iterations or too narrow a word fails it, and going much wider than ~16 wastes area for no accuracy gain (accuracy_bits ref is 10). angle_guard -2..1 and frac_guard 0..2 let the search trade a little accuracy headroom against area, and both rounding modes are kept since rounding can shave the error budget.
- `unrolled_k` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=-2..1, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k is my fallback if iterative's Fmax is too low to reach 1 MSPS: k chained micro-rotations/cycle raises throughput at the cost of a wider combinational datapath (more area). I keep k modest (2-4) because the spec is area-first, so I only want enough unrolling to clear the throughput constraint, not to chase throughput. Same accuracy-focused data_width/n_iter/guard ranges as iterative so the two fronts are directly comparable and the merged Pareto front covers the area-vs-accuracy trade-off.

**Result (code):** 60 evaluations this round, 60 total; 16 feasible; hypervolume 4.679e+04 (n/a).

**LLM decision:** `stop` — The constraints are met and the Pareto front is well-established. The minimum area design (iterative, 6860 um^2) satisfies the throughput constraint (9.43 MSPS >= 1) and the accuracy constraint (10.1 bits >= 10). The front covers a reasonable range of the accuracy objective (10.1 to 11.6 bits) and area (6860 to 13980 um^2). Since this is the final round, we stop. The selection rule (min area) will pick the iterative design with 6860 um^2.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 4.679e+04 (gain this round: n/a (first round)).
Feasible designs: 16 of 60 evaluations (14 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11.8
- max_abs_err <= 0.000976562: 73% violate; best seen 0.00033 (2^-11.57)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=0 rounding=round] area_um2=6860, accuracy_bits=10.1, ffs=100, throughput_msps=9.43, max_abs_err=0.000917 (2^-10.09), power_index=0.144
- iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=7079, accuracy_bits=10.6, ffs=100, throughput_msps=7.45, max_abs_err=0.000632 (2^-10.63), power_index=0.184
- unrolled_k [data_width=16 n_iter=16 angle_guard=0 frac_guard=0 rounding=round k=3] area_um2=11748, accuracy_bits=11.4, ffs=103, throughput_msps=5.96, max_abs_err=0.000373 (2^-11.39), power_index=0.114
- unrolled_k [data_width=16 n_iter=16 angle_guard=0 frac_guard=2 rounding=round k=3] area_um2=13980, accuracy_bits=11.6, ffs=107, throughput_msps=5.46, max_abs_err=0.00033 (2^-11.57), power_index=0.128
Front coverage: area_um2 6860..13980 (HV reference 40000); accuracy_bits 10.1..11.6 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- iterative: 30 evals, 8 feasible; max throughput seen 11.8 MSPS; best accuracy 10.63 bits; best feasible area_um2=6860; feasible ranges: data_width 14..15, n_iter 12..16, angle_guard 0..1, frac_guard 0..2
- unrolled_k: 30 evals, 8 feasible; max throughput seen 10.5 MSPS; best accuracy 11.57 bits; best feasible area_um2=8927; feasible ranges: data_width 15..16, n_iter 14..16, angle_guard 0..0, frac_guard 0..2, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (20 evals): data_width=14..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (2 front designs; box front_anchored)
- `unrolled_k` (20 evals): data_width=15..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 54 feasible; hypervolume 3.764e+05 (+704.5%).

**No LLM call** (code's front-mapping round): The constraints are met and the Pareto front is well-established. The minimum area design (iterative, 6860 um^2) satisfies the throughput constraint (9.43 MSPS >= 1) and the accuracy constraint (10.1 bits >= 10). The front covers a reasonable range of the accuracy objective (10.1 to 11.6 bits) and area (6860 to 13980 um^2). Since this is the final round, we stop. The selection rule (min area) will pick the iterative design with 6860 um^2.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 3.764e+05 (gain this round: +704.5%).
Feasible designs: 54 of 100 evaluations (50 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11.8
- max_abs_err <= 0.000976562: 46% violate; best seen 4.54e-08 (2^-24.39)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=0 rounding=round] area_um2=6860, accuracy_bits=10.1, ffs=100, throughput_msps=9.43, max_abs_err=0.000917 (2^-10.09), power_index=0.144
- iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=7079, accuracy_bits=10.6, ffs=100, throughput_msps=7.45, max_abs_err=0.000632 (2^-10.63), power_index=0.184
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=3 rounding=trunc] area_um2=8166, accuracy_bits=12.1, ffs=112, throughput_msps=7.01, max_abs_err=0.000227 (2^-12.10), power_index=0.198
- iterative [data_width=17 n_iter=19 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=8210, accuracy_bits=12.4, ffs=114, throughput_msps=5.95, max_abs_err=0.00019 (2^-12.36), power_index=0.246
- iterative [data_width=21 n_iter=15 angle_guard=-2 frac_guard=0 rounding=round] area_um2=9274, accuracy_bits=13.4, ffs=129, throughput_msps=6.54, max_abs_err=9.08e-05 (2^-13.43), power_index=0.228
- iterative [data_width=25 n_iter=15 angle_guard=-2 frac_guard=0 rounding=round] area_um2=10889, accuracy_bits=14, ffs=151, throughput_msps=5.77, max_abs_err=6.18e-05 (2^-13.98), power_index=0.267
- iterative [data_width=25 n_iter=21 angle_guard=-2 frac_guard=1 rounding=trunc] area_um2=11844, accuracy_bits=18.1, ffs=154, throughput_msps=4.2, max_abs_err=3.68e-06 (2^-18.05), power_index=0.373
- iterative [data_width=25 n_iter=26 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=12337, accuracy_bits=19.9, ffs=158, throughput_msps=3.48, max_abs_err=1.01e-06 (2^-19.92), power_index=0.465
- iterative [data_width=26 n_iter=26 angle_guard=1 frac_guard=3 rounding=trunc] area_um2=13734, accuracy_bits=21.6, ffs=167, throughput_msps=3.2, max_abs_err=3.1e-07 (2^-21.62), power_index=0.505
- unrolled_k [data_width=27 n_iter=29 angle_guard=3 frac_guard=4 rounding=round k=3] area_um2=25558, accuracy_bits=24.4, ffs=176, throughput_msps=2.44, max_abs_err=4.54e-08 (2^-24.39), power_index=0.323
Front coverage: area_um2 6860..25558 (HV reference 40000); accuracy_bits 10.1..24.4 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 50 evals, 27 feasible; max throughput seen 11.8 MSPS; best accuracy 21.62 bits; best feasible area_um2=6860; feasible ranges: data_width 14..28, n_iter 12..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 50 evals, 27 feasible; max throughput seen 10.5 MSPS; best accuracy 24.39 bits; best feasible area_um2=8927; feasible ranges: data_width 15..27, n_iter 14..30, angle_guard -1..4, frac_guard 0..4, k 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4081 in, 1342 out
- provider-reported cost: $0.0032
- full prompts and replies: `llm_trace.jsonl`

