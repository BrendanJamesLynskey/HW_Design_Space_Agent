# DSE run: asic_power_50msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_power_50msps: A 50 MSPS sin/cos unit in sky130 standard cells for a battery-powered radio: max error <= 2^-12. Minimise the relative power index; accuracy is the trade-off.
  target: asic-sky130hd
  constraint: throughput_msps >= 50
  constraint: max_abs_err <= 0.000244141
  objective: min power_index (HV ref 40)
  objective: max accuracy_bits (HV ref 12)
  select: min power_index
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=16,n_iter=16,angle_guard=1,frac_guard=3,rounding=trunc,m=2` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 34902 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 9298 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 513 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 75.4 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 75.4 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 10 | exact: schedule |
| latency_ns | 133 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.45 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000237 (2^-12.04) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.89 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 5.34e-05 (2^-14.19) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 0.874 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (9 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=16,angle_guard=1,frac_guard=3,rounding=trunc,m=2` | 34902 | 513 | 75.4 | 10 | 2.45 | 0.000237 (2^-12.04) | 12.04 |
| 1 | `pipelined_m:data_width=16,n_iter=16,angle_guard=1,frac_guard=3,rounding=round,m=2` | 35763 | 515 | 75.4 | 10 | 2.49 | 0.000213 (2^-12.20) | 12.20 |
| 2 | `pipelined_m:data_width=16,n_iter=18,angle_guard=1,frac_guard=3,rounding=trunc,m=2` | 39373 | 574 | 75.4 | 11 | 2.76 | 0.000203 (2^-12.27) | 12.27 |
| 3 | `pipelined_m:data_width=20,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc,m=2` | 40699 | 602 | 66.8 | 10 | 2.87 | 4.33e-05 (2^-14.50) | 14.50 |
| 4 | `pipelined_m:data_width=20,n_iter=16,angle_guard=1,frac_guard=3,rounding=trunc,m=2` | 41772 | 615 | 64.3 | 10 | 2.94 | 4.08e-05 (2^-14.58) | 14.58 |
| 5 | `pipelined_m:data_width=20,n_iter=18,angle_guard=1,frac_guard=3,rounding=trunc,m=2` | 47117 | 688 | 64.3 | 11 | 3.3 | 2.04e-05 (2^-15.58) | 15.58 |
| 6 | `pipelined:data_width=20,n_iter=19,angle_guard=2,frac_guard=2,rounding=round` | 64407 | 1358 | 123.1 | 21 | 5.67 | 1.17e-05 (2^-16.38) | 16.38 |
| 7 | `pipelined:data_width=25,n_iter=18,angle_guard=0,frac_guard=3,rounding=trunc` | 72230 | 1545 | 101.6 | 20 | 6.42 | 8.16e-06 (2^-16.90) | 16.90 |
| 8 | `pipelined:data_width=22,n_iter=24,angle_guard=4,frac_guard=3,rounding=round` | 92703 | 1949 | 107.9 | 26 | 8.15 | 1.34e-06 (2^-19.51) | 19.51 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The 50 MSPS constraint forces ~1 result/cycle at >=50 MHz, which only the pipelined families can plausibly deliver (iterative/unrolled would need impractically high Fmax at useful N). Accuracy (max_abs_err <= 2^-12) is set by data_width/n_iter/guards/rounding, identical across families, so both plans sweep those knobs over a wide box to expose the accuracy-vs-power trade-off. pipelined_m is weighted slightly higher because the low 50 MHz floor lets large m trade Fmax for fewer FFs, which is where the minimum power_index likely lives; pipelined covers the high-accuracy/high-Fmax corner and guards against pipelined_m failing the throughput constraint.*)
- `pipelined` (27 evals): data_width=12..20, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Fully pipelined gives 1 result/cycle, so throughput_msps = Fmax; it is the reference family for the 50 MSPS floor and anchors the high-accuracy end of the front. Sweep the accuracy knobs (W, N, guards, rounding) broadly since accuracy is the second objective.
- `pipelined_m` (33 evals): data_width=12..20, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Registering every m stages cuts flip-flops (the dominant power term) while still emitting 1 result/cycle; because the throughput floor is only 50 MHz there is room to raise m and lower power until Fmax drops below 50 MHz. This is the most likely min-power corner, so it gets the larger share.

**Result (code):** 60 evaluations this round, 60 total; 24 feasible; hypervolume 160.1 (n/a).

**LLM decision:** `stop` — Final round: the feasible front already satisfies every spec constraint and covers the needed region. Constraint evidence — throughput_msps >= 50 is met by all 7 Pareto designs (64.3-123 MSPS, best seen 171), and max_abs_err <= 0.000244141 is met with margin by all of them (worst front point 2.37e-4 = 2^-12.04, best 1.17e-5 = 2^-16.38), so nothing here is infeasible. Objective evidence — the front spans power_index 2.45..5.67 against HV ref 40 and accuracy_bits 12..16.4 against HV ref 12, i.e. it already brackets both HV reference points, giving HV 160.1. The selection rule (min power_index) lands on pipelined_m [data_width=16 n_iter=16 angle_guard=1 frac_guard=3 rounding=trunc m=2]: power_index=2.45, accuracy_bits=12.0, max_abs_err=2.37e-4 (constraint-compliant), throughput 75.4 MSPS (>50), area 34902 um^2, 513 FFs. pipelined supplies the high-accuracy tail (up to 16.38 bits) while pipelined_m supplies the low-power head, so the trade-off curve is covered; no unexplored family remains in the registry to add. Only 60/100 evals were used, but the round cap binds and any further refinement decision would be treated as stop, so I stop with the front as-is.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 160.1 (gain this round: n/a (first round)).
Feasible designs: 24 of 60 evaluations (22 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 32% violate; best seen 171
- max_abs_err <= 0.000244141: 57% violate; best seen 1.17e-05 (2^-16.38)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=16 n_iter=16 angle_guard=1 frac_guard=3 rounding=trunc m=2] power_index=2.45, accuracy_bits=12, area_um2=34902, ffs=513, throughput_msps=75.4, max_abs_err=0.000237 (2^-12.04)
- pipelined_m [data_width=16 n_iter=16 angle_guard=1 frac_guard=3 rounding=round m=2] power_index=2.49, accuracy_bits=12.2, area_um2=35763, ffs=515, throughput_msps=75.4, max_abs_err=0.000213 (2^-12.20)
- pipelined_m [data_width=16 n_iter=18 angle_guard=1 frac_guard=3 rounding=trunc m=2] power_index=2.76, accuracy_bits=12.3, area_um2=39373, ffs=574, throughput_msps=75.4, max_abs_err=0.000203 (2^-12.27)
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=2] power_index=2.87, accuracy_bits=14.5, area_um2=40699, ffs=602, throughput_msps=66.8, max_abs_err=4.33e-05 (2^-14.50)
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=3 rounding=trunc m=2] power_index=2.94, accuracy_bits=14.6, area_um2=41772, ffs=615, throughput_msps=64.3, max_abs_err=4.08e-05 (2^-14.58)
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=3 rounding=trunc m=2] power_index=3.3, accuracy_bits=15.6, area_um2=47117, ffs=688, throughput_msps=64.3, max_abs_err=2.04e-05 (2^-15.58)
- pipelined [data_width=20 n_iter=19 angle_guard=2 frac_guard=2 rounding=round] power_index=5.67, accuracy_bits=16.4, area_um2=64407, ffs=1358, throughput_msps=123, max_abs_err=1.17e-05 (2^-16.38)
Front coverage: power_index 2.45..5.67 (HV reference 40); accuracy_bits 12..16.4 (HV reference 12); data_width on the front 16..20 (registry 8..28).

Per family:
- pipelined: 27 evals, 15 feasible; max throughput seen 171 MSPS; best accuracy 16.38 bits; best feasible power_index=4.04; feasible ranges: data_width 16..20, n_iter 16..20, angle_guard 2..4, frac_guard 0..4
- pipelined_m: 33 evals, 9 feasible; max throughput seen 82.5 MSPS; best accuracy 15.58 bits; best feasible power_index=2.45; feasible ranges: data_width 16..20, n_iter 16..18, angle_guard 0..1, frac_guard 2..4, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (35 evals): data_width=15..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (6 front designs; box front_anchored)
- `pipelined` (5 evals): data_width=19..28, n_iter=17..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 29 feasible; hypervolume 260.8 (+62.8%).

**No LLM call** (code's front-mapping round): Final round: the feasible front already satisfies every spec constraint and covers the needed region. Constraint evidence — throughput_msps >= 50 is met by all 7 Pareto designs (64.3-123 MSPS, best seen 171), and max_abs_err <= 0.000244141 is met with margin by all of them (worst front point 2.37e-4 = 2^-12.04, best 1.17e-5 = 2^-16.38), so nothing here is infeasible. Objective evidence — the front spans power_index 2.45..5.67 against HV ref 40 and accuracy_bits 12..16.4 against HV ref 12, i.e. it already brackets both HV reference points, giving HV 160.1. The selection rule (min power_index) lands on pipelined_m [data_width=16 n_iter=16 angle_guard=1 frac_guard=3 rounding=trunc m=2]: power_index=2.45, accuracy_bits=12.0, max_abs_err=2.37e-4 (constraint-compliant), throughput 75.4 MSPS (>50), area 34902 um^2, 513 FFs. pipelined supplies the high-accuracy tail (up to 16.38 bits) while pipelined_m supplies the low-power head, so the trade-off curve is covered; no unexplored family remains in the registry to add. Only 60/100 evals were used, but the round cap binds and any further refinement decision would be treated as stop, so I stop with the front as-is.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 260.8 (gain this round: +62.8%).
Feasible designs: 29 of 100 evaluations (27 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 53% violate; best seen 171
- max_abs_err <= 0.000244141: 42% violate; best seen 1.33e-07 (2^-22.84)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=16 n_iter=16 angle_guard=1 frac_guard=3 rounding=trunc m=2] power_index=2.45, accuracy_bits=12, area_um2=34902, ffs=513, throughput_msps=75.4, max_abs_err=0.000237 (2^-12.04)
- pipelined_m [data_width=16 n_iter=16 angle_guard=1 frac_guard=3 rounding=round m=2] power_index=2.49, accuracy_bits=12.2, area_um2=35763, ffs=515, throughput_msps=75.4, max_abs_err=0.000213 (2^-12.20)
- pipelined_m [data_width=16 n_iter=18 angle_guard=1 frac_guard=3 rounding=trunc m=2] power_index=2.76, accuracy_bits=12.3, area_um2=39373, ffs=574, throughput_msps=75.4, max_abs_err=0.000203 (2^-12.27)
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=2] power_index=2.87, accuracy_bits=14.5, area_um2=40699, ffs=602, throughput_msps=66.8, max_abs_err=4.33e-05 (2^-14.50)
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=3 rounding=trunc m=2] power_index=2.94, accuracy_bits=14.6, area_um2=41772, ffs=615, throughput_msps=64.3, max_abs_err=4.08e-05 (2^-14.58)
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=3 rounding=trunc m=2] power_index=3.3, accuracy_bits=15.6, area_um2=47117, ffs=688, throughput_msps=64.3, max_abs_err=2.04e-05 (2^-15.58)
- pipelined [data_width=20 n_iter=19 angle_guard=2 frac_guard=2 rounding=round] power_index=5.67, accuracy_bits=16.4, area_um2=64407, ffs=1358, throughput_msps=123, max_abs_err=1.17e-05 (2^-16.38)
- pipelined [data_width=25 n_iter=18 angle_guard=0 frac_guard=3 rounding=trunc] power_index=6.42, accuracy_bits=16.9, area_um2=72230, ffs=1545, throughput_msps=102, max_abs_err=8.16e-06 (2^-16.90)
- pipelined [data_width=22 n_iter=24 angle_guard=4 frac_guard=3 rounding=round] power_index=8.15, accuracy_bits=19.5, area_um2=92703, ffs=1949, throughput_msps=108, max_abs_err=1.34e-06 (2^-19.51)
Front coverage: power_index 2.45..8.15 (HV reference 40); accuracy_bits 12..19.5 (HV reference 12); data_width on the front 16..25 (registry 8..28).

Per family:
- pipelined: 32 evals, 20 feasible; max throughput seen 171 MSPS; best accuracy 19.51 bits; best feasible power_index=4.04; feasible ranges: data_width 16..25, n_iter 16..26, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 68 evals, 9 feasible; max throughput seen 82.5 MSPS; best accuracy 22.84 bits; best feasible power_index=2.45; feasible ranges: data_width 16..20, n_iter 16..18, angle_guard 0..1, frac_guard 2..4, m 2..2
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4829 in, 2602 out
- provider-reported cost: $0.0015
- full prompts and replies: `llm_trace.jsonl`

