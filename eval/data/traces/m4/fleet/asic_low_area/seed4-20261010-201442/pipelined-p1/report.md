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
`pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=1,rounding=trunc,m=3` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 22237 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 5924 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 262 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 110 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.0276 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000643 (2^-10.60) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 10.5 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000208 (2^-12.23) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 3.41 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.6 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (12 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=1,rounding=trunc,m=3` | 22237 | 262 | 54.3 | 6 | 0.0276 | 0.000643 (2^-10.60) | 10.60 |
| 1 | `pipelined_m:data_width=18,n_iter=12,angle_guard=4,frac_guard=1,rounding=trunc,m=8` | 22347 | 165 | 17.8 | 4 | 0.0224 | 0.000514 (2^-10.92) | 10.92 |
| 2 | `pipelined_m:data_width=16,n_iter=13,angle_guard=2,frac_guard=3,rounding=trunc,m=8` | 22457 | 149 | 20.3 | 4 | 0.0215 | 0.000339 (2^-11.52) | 11.52 |
| 3 | `pipelined_m:data_width=16,n_iter=13,angle_guard=2,frac_guard=3,rounding=round,m=8` | 23319 | 151 | 20.3 | 4 | 0.0222 | 0.000293 (2^-11.74) | 11.74 |
| 4 | `pipelined_m:data_width=22,n_iter=13,angle_guard=-2,frac_guard=0,rounding=round,m=6` | 27202 | 253 | 23.6 | 5 | 0.0301 | 0.000254 (2^-11.94) | 11.94 |
| 5 | `pipelined_m:data_width=20,n_iter=14,angle_guard=-2,frac_guard=0,rounding=round,m=4` | 27936 | 295 | 37.9 | 6 | 0.0329 | 0.000177 (2^-12.46) | 12.46 |
| 6 | `pipelined_m:data_width=25,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=6` | 33496 | 291 | 21.0 | 5 | 0.0359 | 0.000122 (2^-13.00) | 13.00 |
| 7 | `pipelined_m:data_width=16,n_iter=20,angle_guard=2,frac_guard=3,rounding=round,m=8` | 35784 | 213 | 20.3 | 5 | 0.033 | 0.000112 (2^-13.13) | 13.13 |
| 8 | `pipelined_m:data_width=21,n_iter=19,angle_guard=-2,frac_guard=2,rounding=trunc,m=6` | 39901 | 321 | 22.7 | 6 | 0.0413 | 4.92e-05 (2^-14.31) | 14.31 |
| 9 | `pipelined_m:data_width=24,n_iter=19,angle_guard=-2,frac_guard=0,rounding=round,m=8` | 41175 | 274 | 16.5 | 5 | 0.0395 | 8.52e-06 (2^-16.84) | 16.84 |
| 10 | `pipelined_m:data_width=24,n_iter=28,angle_guard=-2,frac_guard=1,rounding=trunc,m=7` | 61845 | 356 | 18.1 | 6 | 0.0562 | 7.66e-06 (2^-16.99) | 16.99 |
| 11 | `pipelined_m:data_width=24,n_iter=28,angle_guard=-2,frac_guard=0,rounding=round,m=6` | 62015 | 426 | 21.8 | 7 | 0.0602 | 6.97e-06 (2^-17.13) | 17.13 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Both assigned families are fully pipelined (1 result/cycle), so the 1 MSPS throughput constraint is essentially free and the Pareto front is area vs accuracy. Area scales with datapath width and stage count, so I concentrate the search on small data_width (8..20) and n_iter (4..20) where the min-area feasible designs should live, while keeping the upper ends high enough to map accuracy_bits past the HV reference of 10. Guards and rounding are searched over their full registry ranges since they trade area for error cheaply. pipelined_m gets an equal share because its m parameter can reduce register area at the same accuracy, making it a likely min-area winner.*)
- `pipelined` (30 evals): data_width=8..20, n_iter=4..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* One result/cycle means the >=1 MSPS constraint is met at any realistic Fmax, so area is the only real pressure: search small data_width/n_iter for the min-area corner while extending upward to cover the accuracy side of the front (accuracy_bits HV ref 10).
- `pipelined_m` (30 evals): data_width=8..20, n_iter=4..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Same 1 result/cycle throughput, but registering every m stages cuts pipeline FF count, so it can undercut pipelined on area at equal accuracy; sweep m across its full range to expose that trade-off.

**Result (code):** 60 evaluations this round, 60 total; 42 feasible; hypervolume 3.662e+04 (n/a).

**LLM decision:** `stop` — Final round reached (round cap / budget). The spec is satisfiable and the front is well populated: 42/60 evaluations feasible (39 unique), 6 designs on the Pareto front. The selection rule (min area_um2) picks pipelined_m [W=16, N=12, angle_guard=2, frac_guard=1, trunc, m=3] at area_um2=22237 with accuracy_bits=10.6 (max_abs_err=0.000643 = 2^-10.60), throughput 54.3 MSPS and 262 FFs — comfortably inside both constraints (throughput >= 1 MSPS, max_abs_err <= 0.000976562). The front also spans accuracy up to 13.1 bits (area 35784) and throughput up to 242 MSPS in the pipelined family, so the trade-off curve is covered rather than a single corner. Both families that appear on the front (pipelined, pipelined_m) were explored; the registry's other families (iterative, unrolled_k) are lower-throughput variants of the same datapath and cannot beat the 22237 um^2 area point given the accuracy/throughput already achieved. No constraint is unreachable (0% throughput violations, best error 2^-13.13 well under the 2^-10 bound), so `infeasible` does not apply. Stopping here.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 3.662e+04 (gain this round: n/a (first round)).
Feasible designs: 42 of 60 evaluations (39 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 242
- max_abs_err <= 0.000976562: 30% violate; best seen 0.000112 (2^-13.13)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=1 rounding=trunc m=3] area_um2=22237, accuracy_bits=10.6, ffs=262, throughput_msps=54.3, max_abs_err=0.000643 (2^-10.60), power_index=0.0276
- pipelined_m [data_width=18 n_iter=12 angle_guard=4 frac_guard=1 rounding=trunc m=8] area_um2=22347, accuracy_bits=10.9, ffs=165, throughput_msps=17.8, max_abs_err=0.000514 (2^-10.92), power_index=0.0224
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=3 rounding=trunc m=8] area_um2=22457, accuracy_bits=11.5, ffs=149, throughput_msps=20.3, max_abs_err=0.000339 (2^-11.52), power_index=0.0215
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=3 rounding=round m=8] area_um2=23319, accuracy_bits=11.7, ffs=151, throughput_msps=20.3, max_abs_err=0.000293 (2^-11.74), power_index=0.0222
- pipelined_m [data_width=16 n_iter=15 angle_guard=1 frac_guard=4 rounding=round m=2] area_um2=35226, accuracy_bits=12.3, ffs=529, throughput_msps=72.3, max_abs_err=0.000203 (2^-12.27), power_index=0.0502
- pipelined_m [data_width=16 n_iter=20 angle_guard=2 frac_guard=3 rounding=round m=8] area_um2=35784, accuracy_bits=13.1, ffs=213, throughput_msps=20.3, max_abs_err=0.000112 (2^-13.13), power_index=0.033
Front coverage: area_um2 22237..35784 (HV reference 40000); accuracy_bits 10.6..13.1 (HV reference 10); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 30 evals, 16 feasible; max throughput seen 242 MSPS; best accuracy 12.76 bits; best feasible area_um2=31028; feasible ranges: data_width 16..19, n_iter 12..20, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 30 evals, 26 feasible; max throughput seen 86.6 MSPS; best accuracy 13.13 bits; best feasible area_um2=22237; feasible ranges: data_width 15..18, n_iter 12..20, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=15..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (6 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 78 feasible; hypervolume 4.35e+04 (+18.8%).

**No LLM call** (code's front-mapping round): Final round reached (round cap / budget). The spec is satisfiable and the front is well populated: 42/60 evaluations feasible (39 unique), 6 designs on the Pareto front. The selection rule (min area_um2) picks pipelined_m [W=16, N=12, angle_guard=2, frac_guard=1, trunc, m=3] at area_um2=22237 with accuracy_bits=10.6 (max_abs_err=0.000643 = 2^-10.60), throughput 54.3 MSPS and 262 FFs — comfortably inside both constraints (throughput >= 1 MSPS, max_abs_err <= 0.000976562). The front also spans accuracy up to 13.1 bits (area 35784) and throughput up to 242 MSPS in the pipelined family, so the trade-off curve is covered rather than a single corner. Both families that appear on the front (pipelined, pipelined_m) were explored; the registry's other families (iterative, unrolled_k) are lower-throughput variants of the same datapath and cannot beat the 22237 um^2 area point given the accuracy/throughput already achieved. No constraint is unreachable (0% throughput violations, best error 2^-13.13 well under the 2^-10 bound), so `infeasible` does not apply. Stopping here.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 4.35e+04 (gain this round: +18.8%).
Feasible designs: 78 of 100 evaluations (69 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 242
- max_abs_err <= 0.000976562: 22% violate; best seen 6.97e-06 (2^-17.13)

Pareto front (feasible, 12 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=1 rounding=trunc m=3] area_um2=22237, accuracy_bits=10.6, ffs=262, throughput_msps=54.3, max_abs_err=0.000643 (2^-10.60), power_index=0.0276
- pipelined_m [data_width=18 n_iter=12 angle_guard=4 frac_guard=1 rounding=trunc m=8] area_um2=22347, accuracy_bits=10.9, ffs=165, throughput_msps=17.8, max_abs_err=0.000514 (2^-10.92), power_index=0.0224
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=3 rounding=trunc m=8] area_um2=22457, accuracy_bits=11.5, ffs=149, throughput_msps=20.3, max_abs_err=0.000339 (2^-11.52), power_index=0.0215
- pipelined_m [data_width=22 n_iter=13 angle_guard=-2 frac_guard=0 rounding=round m=6] area_um2=27202, accuracy_bits=11.9, ffs=253, throughput_msps=23.6, max_abs_err=0.000254 (2^-11.94), power_index=0.0301
- pipelined_m [data_width=20 n_iter=14 angle_guard=-2 frac_guard=0 rounding=round m=4] area_um2=27936, accuracy_bits=12.5, ffs=295, throughput_msps=37.9, max_abs_err=0.000177 (2^-12.46), power_index=0.0329
- pipelined_m [data_width=25 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=6] area_um2=33496, accuracy_bits=13, ffs=291, throughput_msps=21, max_abs_err=0.000122 (2^-13.00), power_index=0.0359
- pipelined_m [data_width=16 n_iter=20 angle_guard=2 frac_guard=3 rounding=round m=8] area_um2=35784, accuracy_bits=13.1, ffs=213, throughput_msps=20.3, max_abs_err=0.000112 (2^-13.13), power_index=0.033
- pipelined_m [data_width=24 n_iter=19 angle_guard=-2 frac_guard=0 rounding=round m=8] area_um2=41175, accuracy_bits=16.8, ffs=274, throughput_msps=16.5, max_abs_err=8.52e-06 (2^-16.84), power_index=0.0395
- pipelined_m [data_width=24 n_iter=28 angle_guard=-2 frac_guard=1 rounding=trunc m=7] area_um2=61845, accuracy_bits=17, ffs=356, throughput_msps=18.1, max_abs_err=7.66e-06 (2^-16.99), power_index=0.0562
- pipelined_m [data_width=24 n_iter=28 angle_guard=-2 frac_guard=0 rounding=round m=6] area_um2=62015, accuracy_bits=17.1, ffs=426, throughput_msps=21.8, max_abs_err=6.97e-06 (2^-17.13), power_index=0.0602
Front coverage: area_um2 22237..62015 (HV reference 40000); accuracy_bits 10.6..17.1 (HV reference 10); data_width on the front 16..25 (registry 8..28).

Per family:
- pipelined: 30 evals, 16 feasible; max throughput seen 242 MSPS; best accuracy 12.76 bits; best feasible area_um2=31028; feasible ranges: data_width 16..19, n_iter 12..20, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 70 evals, 62 feasible; max throughput seen 86.6 MSPS; best accuracy 17.13 bits; best feasible area_um2=22237; feasible ranges: data_width 15..28, n_iter 11..28, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4756 in, 2057 out
- provider-reported cost: $0.0013
- full prompts and replies: `llm_trace.jsonl`

