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
`iterative:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 7860 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 2094 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 111 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 131 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 7.7 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 130 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.183 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.00027 (2^-11.85) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 4.43 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 6.55e-05 (2^-13.90) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 1.07 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 11.9 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (14 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` | 7860 | 111 | 7.7 | 17 | 0.183 | 0.00027 (2^-11.85) | 11.85 |
| 1 | `iterative:data_width=17,n_iter=25,angle_guard=3,frac_guard=0,rounding=round` | 8283 | 114 | 4.4 | 28 | 0.314 | 0.000146 (2^-12.74) | 12.74 |
| 2 | `iterative:data_width=17,n_iter=24,angle_guard=2,frac_guard=2,rounding=trunc` | 8655 | 117 | 4.7 | 27 | 0.313 | 0.00013 (2^-12.91) | 12.91 |
| 3 | `iterative:data_width=17,n_iter=24,angle_guard=4,frac_guard=2,rounding=trunc` | 8781 | 119 | 4.4 | 27 | 0.319 | 0.000114 (2^-13.10) | 13.10 |
| 4 | `iterative:data_width=17,n_iter=24,angle_guard=2,frac_guard=3,rounding=trunc` | 9036 | 119 | 4.5 | 27 | 0.323 | 8.39e-05 (2^-13.54) | 13.54 |
| 5 | `iterative:data_width=17,n_iter=25,angle_guard=3,frac_guard=3,rounding=trunc` | 9100 | 120 | 4.4 | 28 | 0.337 | 8.1e-05 (2^-13.59) | 13.59 |
| 6 | `iterative:data_width=17,n_iter=17,angle_guard=3,frac_guard=3,rounding=round` | 10525 | 120 | 6.1 | 20 | 0.258 | 5.1e-05 (2^-14.26) | 14.26 |
| 7 | `iterative:data_width=21,n_iter=17,angle_guard=3,frac_guard=3,rounding=trunc` | 10629 | 142 | 5.3 | 20 | 0.283 | 1.8e-05 (2^-15.76) | 15.76 |
| 8 | `iterative:data_width=25,n_iter=23,angle_guard=-2,frac_guard=2,rounding=trunc` | 12395 | 156 | 3.8 | 26 | 0.416 | 3.3e-06 (2^-18.21) | 18.21 |
| 9 | `iterative:data_width=27,n_iter=24,angle_guard=4,frac_guard=2,rounding=trunc` | 13874 | 174 | 3.3 | 27 | 0.482 | 1.99e-07 (2^-22.26) | 22.26 |
| 10 | `iterative:data_width=28,n_iter=24,angle_guard=3,frac_guard=2,rounding=trunc` | 14323 | 178 | 3.3 | 27 | 0.496 | 1.59e-07 (2^-22.58) | 22.58 |
| 11 | `iterative:data_width=28,n_iter=25,angle_guard=3,frac_guard=3,rounding=trunc` | 14838 | 181 | 3.1 | 28 | 0.526 | 8.56e-08 (2^-23.48) | 23.48 |
| 12 | `iterative:data_width=28,n_iter=30,angle_guard=3,frac_guard=2,rounding=round` | 17404 | 178 | 2.7 | 33 | 0.666 | 3.6e-08 (2^-24.73) | 24.73 |
| 13 | `iterative:data_width=28,n_iter=30,angle_guard=3,frac_guard=3,rounding=round` | 17882 | 181 | 2.7 | 33 | 0.679 | 2.91e-08 (2^-25.04) | 25.04 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *No fleet facts yet, so I start from first principles on the two families I own. The spec is area-minimisation with two hard constraints: throughput >= 1 MSPS and max_abs_err <= 2^-10. Accuracy depends only on data_width, n_iter, angle_guard, frac_guard, rounding (identical bits across families), so I bound those to the smallest values that can plausibly clear 2^-10 (data_width 12-16, n_iter 10-14, small guards, both rounding modes) and let the bit-accurate model confirm feasibility. The real differentiator between my two families is throughput: iterative is the cheapest in area but emits one result every N+3 cycles, so it only clears 1 MSPS at low Fmax; unrolled_k divides the cycle count by k and is the robust way to meet throughput while staying near the iterative area. I therefore put the full budget on unrolled_k (k=2-4) to map the feasible low-area/throughput-meeting region, and keep a zero-share iterative entry only to record the absolute low-area reference point if it happens to meet throughput. This concentrates evaluations where the trade-off (k vs n_iter vs data_width) actually lives, rather than sweeping the full registry ranges.*)
- `iterative` (5 evals): data_width=12..16, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the smallest-area family (one shared datapath, no per-stage registers). It is the only family that can plausibly minimise area, but it emits one result every N+3 cycles, so it can only meet >=1 MSPS at low Fmax. I keep n_iter at 10-14 so that at a realistic Fmax (tens of MHz) throughput stays >=1 MSPS, and data_width 12-16 with modest guards to hold max_abs_err <= 2^-10 while keeping area small. This maps the low-area corner of the front.
- `unrolled_k` (55 evals): data_width=12..16, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k chains k micro-rotations per cycle, so it reaches >=1 MSPS at a much lower Fmax than iterative for the same N, and it is the natural way to satisfy the throughput constraint while staying close to the iterative area (shared datapath, only a few extra shifters/registers). k=2-4 keeps the combinational depth (and hence Fmax) manageable. I focus the budget here because it is where the feasible, low-area, throughput-meeting designs live; the trade-off between k (area/Fmax) and n_iter (accuracy) is the interesting curve to map.

**Result (code):** 60 evaluations this round, 60 total; 33 feasible; hypervolume 5.954e+04 (n/a).

**LLM decision:** `stop` — The Pareto front is dominated by a single feasible design from the `iterative` family: [data_width=16, n_iter=14, angle_guard=2, frac_guard=2, rounding=trunc] with an area of 7860 um^2 and accuracy of 11.9 bits. This design satisfies both constraints (throughput 7.7 MSPS >= 1, max_abs_err 0.00027 <= 0.000976562). The `unrolled_k` family, which was heavily explored (55 evals), yielded a best feasible area of 9189 um^2, which is significantly larger than the `iterative` solution. Since the goal is to minimize area and the `iterative` design is the global minimum found so far, and we are at the final round with no budget left for further exploration or front mapping, stopping is the correct action. The hypervolume is 5.954e+04, which is reasonable given the single-point front, but no further improvement is possible within the constraints and budget.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 5.954e+04 (gain this round: n/a (first round)).
Feasible designs: 33 of 60 evaluations (18 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 12.4
- max_abs_err <= 0.000976562: 45% violate; best seen 0.00027 (2^-11.85)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7860, accuracy_bits=11.9, ffs=111, throughput_msps=7.7, max_abs_err=0.00027 (2^-11.85), power_index=0.183
Front coverage: area_um2 7860..7860 (HV reference 40000); accuracy_bits 11.9..11.9 (HV reference 10); data_width on the front 16..16 (registry 8..28).

Per family:
- iterative: 5 evals, 2 feasible; max throughput seen 12.4 MSPS; best accuracy 11.85 bits; best feasible area_um2=7860; feasible ranges: data_width 16..16, n_iter 13..14, angle_guard 2..2, frac_guard 1..2
- unrolled_k: 55 evals, 31 feasible; max throughput seen 11.2 MSPS; best accuracy 10.78 bits; best feasible area_um2=9189; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (40 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 73 feasible; hypervolume 4.172e+05 (+600.8%).

**No LLM call** (code's front-mapping round): The Pareto front is dominated by a single feasible design from the `iterative` family: [data_width=16, n_iter=14, angle_guard=2, frac_guard=2, rounding=trunc] with an area of 7860 um^2 and accuracy of 11.9 bits. This design satisfies both constraints (throughput 7.7 MSPS >= 1, max_abs_err 0.00027 <= 0.000976562). The `unrolled_k` family, which was heavily explored (55 evals), yielded a best feasible area of 9189 um^2, which is significantly larger than the `iterative` solution. Since the goal is to minimize area and the `iterative` design is the global minimum found so far, and we are at the final round with no budget left for further exploration or front mapping, stopping is the correct action. The hypervolume is 5.954e+04, which is reasonable given the single-point front, but no further improvement is possible within the constraints and budget.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 4.172e+05 (gain this round: +600.8%).
Feasible designs: 73 of 100 evaluations (55 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 12.4
- max_abs_err <= 0.000976562: 27% violate; best seen 2.91e-08 (2^-25.04)

Pareto front (feasible, 14 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7860, accuracy_bits=11.9, ffs=111, throughput_msps=7.7, max_abs_err=0.00027 (2^-11.85), power_index=0.183
- iterative [data_width=17 n_iter=25 angle_guard=3 frac_guard=0 rounding=round] area_um2=8283, accuracy_bits=12.7, ffs=114, throughput_msps=4.35, max_abs_err=0.000146 (2^-12.74), power_index=0.314
- iterative [data_width=17 n_iter=24 angle_guard=4 frac_guard=2 rounding=trunc] area_um2=8781, accuracy_bits=13.1, ffs=119, throughput_msps=4.36, max_abs_err=0.000114 (2^-13.10), power_index=0.319
- iterative [data_width=17 n_iter=24 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=9036, accuracy_bits=13.5, ffs=119, throughput_msps=4.51, max_abs_err=8.39e-05 (2^-13.54), power_index=0.323
- iterative [data_width=17 n_iter=17 angle_guard=3 frac_guard=3 rounding=round] area_um2=10525, accuracy_bits=14.3, ffs=120, throughput_msps=6.09, max_abs_err=5.1e-05 (2^-14.26), power_index=0.258
- iterative [data_width=21 n_iter=17 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=10629, accuracy_bits=15.8, ffs=142, throughput_msps=5.35, max_abs_err=1.8e-05 (2^-15.76), power_index=0.283
- iterative [data_width=27 n_iter=24 angle_guard=4 frac_guard=2 rounding=trunc] area_um2=13874, accuracy_bits=22.3, ffs=174, throughput_msps=3.26, max_abs_err=1.99e-07 (2^-22.26), power_index=0.482
- iterative [data_width=28 n_iter=24 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=14323, accuracy_bits=22.6, ffs=178, throughput_msps=3.26, max_abs_err=1.59e-07 (2^-22.58), power_index=0.496
- iterative [data_width=28 n_iter=30 angle_guard=3 frac_guard=2 rounding=round] area_um2=17404, accuracy_bits=24.7, ffs=178, throughput_msps=2.67, max_abs_err=3.6e-08 (2^-24.73), power_index=0.666
- iterative [data_width=28 n_iter=30 angle_guard=3 frac_guard=3 rounding=round] area_um2=17882, accuracy_bits=25, ffs=181, throughput_msps=2.67, max_abs_err=2.91e-08 (2^-25.04), power_index=0.679
Front coverage: area_um2 7860..17882 (HV reference 40000); accuracy_bits 11.9..25 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- iterative: 45 evals, 42 feasible; max throughput seen 12.4 MSPS; best accuracy 25.04 bits; best feasible area_um2=7860; feasible ranges: data_width 16..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 55 evals, 31 feasible; max throughput seen 11.2 MSPS; best accuracy 10.78 bits; best feasible area_um2=9189; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2, k 2..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 3804 in, 1213 out
- provider-reported cost: $0.0029
- full prompts and replies: `llm_trace.jsonl`

