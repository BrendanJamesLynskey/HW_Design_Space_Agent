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
`pipelined_m:data_width=16,n_iter=12,angle_guard=0,frac_guard=1,rounding=round,m=4` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 21117 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 5626 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 200 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 43.5 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 43.5 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 115 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.0235 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000703 (2^-10.47) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 11.5 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.00021 (2^-12.22) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 3.44 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.5 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=12,angle_guard=0,frac_guard=1,rounding=round,m=4` | 21117 | 200 | 43.5 | 5 | 0.0235 | 0.000703 (2^-10.47) | 10.47 |
| 1 | `pipelined_m:data_width=15,n_iter=13,angle_guard=1,frac_guard=0,rounding=round,m=3` | 22512 | 290 | 59.9 | 7 | 0.0294 | 0.000673 (2^-10.54) | 10.54 |
| 2 | `pipelined_m:data_width=16,n_iter=13,angle_guard=1,frac_guard=0,rounding=round,m=4` | 22580 | 252 | 43.5 | 6 | 0.0273 | 0.000417 (2^-11.23) | 11.23 |
| 3 | `pipelined_m:data_width=15,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=3` | 26770 | 313 | 57.0 | 7 | 0.0332 | 0.000362 (2^-11.43) | 11.43 |
| 4 | `pipelined_m:data_width=24,n_iter=14,angle_guard=-2,frac_guard=0,rounding=trunc,m=4` | 33145 | 350 | 32.3 | 6 | 0.039 | 0.000124 (2^-12.97) | 12.97 |
| 5 | `pipelined_m:data_width=20,n_iter=19,angle_guard=-2,frac_guard=0,rounding=trunc,m=6` | 36113 | 295 | 25.7 | 6 | 0.0377 | 9.81e-05 (2^-13.32) | 13.32 |
| 6 | `pipelined_m:data_width=20,n_iter=19,angle_guard=-2,frac_guard=2,rounding=trunc,m=6` | 38215 | 307 | 23.6 | 6 | 0.0396 | 9.31e-05 (2^-13.39) | 13.39 |
| 7 | `pipelined_m:data_width=23,n_iter=19,angle_guard=-2,frac_guard=0,rounding=trunc,m=3` | 46015 | 554 | 44.1 | 9 | 0.0579 | 1.46e-05 (2^-16.06) | 16.06 |
| 8 | `pipelined_m:data_width=24,n_iter=28,angle_guard=-2,frac_guard=1,rounding=trunc,m=7` | 61845 | 356 | 18.1 | 6 | 0.0562 | 7.66e-06 (2^-16.99) | 16.99 |
| 9 | `pipelined_m:data_width=24,n_iter=26,angle_guard=-2,frac_guard=0,rounding=round,m=3` | 64852 | 729 | 42.5 | 11 | 0.0787 | 6.97e-06 (2^-17.13) | 17.13 |
| 10 | `pipelined_m:data_width=28,n_iter=24,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 73053 | 796 | 33.9 | 10 | 0.0873 | 5.95e-07 (2^-20.68) | 20.68 |
| 11 | `pipelined:data_width=27,n_iter=24,angle_guard=4,frac_guard=0,rounding=round` | 101801 | 2171 | 93.5 | 26 | 0.181 | 2.65e-07 (2^-21.85) | 21.85 |
| 12 | `pipelined:data_width=28,n_iter=25,angle_guard=1,frac_guard=3,rounding=trunc` | 112825 | 2397 | 93.5 | 27 | 0.2 | 1.15e-07 (2^-23.05) | 23.05 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *No fleet facts yet, so I start from the spec: area is the primary objective and the hard constraints are throughput >= 1 MSPS and max_abs_err <= 2^-10. Both pipelined and pipelined_m produce 1 result/cycle, so throughput is met by Fmax; the area trade-off is driven by data_width, n_iter, and the guard bits. I bound data_width to 12..16 and n_iter to 10..14 to cover the smallest configurations that plausibly satisfy the 2^-10 accuracy bound with rounding, and keep guards small to limit area. I split the budget 60/40 between the two families, weighting pipelined_m slightly less since it is a variant of the same datapath, to map the area/accuracy front across both.*)
- `pipelined` (36 evals): data_width=12..16, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* Fully pipelined gives 1 result/cycle so throughput scales with Fmax; area is the dominant objective, so I focus on the smallest widths that still satisfy max_abs_err <= 2^-10 with rounding, and the minimum n_iter that meets accuracy to keep the N+2 stage chain short.
- `pipelined_m` (24 evals): data_width=12..16, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* pipelined_m registers every m stages, cutting flip-flop count and area versus full pipelining while keeping 1 result/cycle; I search m=2..4 to find the area/latency sweet spot that still meets the 1 MSPS throughput constraint.

**Result (code):** 60 evaluations this round, 60 total; 36 feasible; hypervolume 2.517e+04 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (pipelined_m, 21117 um^2) meets the throughput constraint (43.5 MSPS >= 1) and accuracy constraint (10.5 bits >= 10). The front covers the trade-off space effectively from 21117 um^2 / 10.5 bits to 35509 um^2 / 11.5 bits. Since this is the final round, we stop and select the design with minimum area (21117 um^2) as per the spec's selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 2.517e+04 (gain this round: n/a (first round)).
Feasible designs: 36 of 60 evaluations (23 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 190
- max_abs_err <= 0.000976562: 40% violate; best seen 0.000342 (2^-11.51)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=0 frac_guard=1 rounding=round m=4] area_um2=21117, accuracy_bits=10.5, ffs=200, throughput_msps=43.5, max_abs_err=0.000703 (2^-10.47), power_index=0.0235
- pipelined_m [data_width=15 n_iter=13 angle_guard=1 frac_guard=0 rounding=round m=3] area_um2=22512, accuracy_bits=10.5, ffs=290, throughput_msps=59.9, max_abs_err=0.000673 (2^-10.54), power_index=0.0294
- pipelined_m [data_width=16 n_iter=13 angle_guard=1 frac_guard=0 rounding=round m=4] area_um2=22580, accuracy_bits=11.2, ffs=252, throughput_msps=43.5, max_abs_err=0.000417 (2^-11.23), power_index=0.0273
- pipelined_m [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=3] area_um2=26770, accuracy_bits=11.4, ffs=313, throughput_msps=57, max_abs_err=0.000362 (2^-11.43), power_index=0.0332
- pipelined [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=35509, accuracy_bits=11.5, ffs=771, throughput_msps=149, max_abs_err=0.000342 (2^-11.51), power_index=0.0638
Front coverage: area_um2 21117..35509 (HV reference 40000); accuracy_bits 10.5..11.5 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- pipelined: 36 evals, 21 feasible; max throughput seen 190 MSPS; best accuracy 11.51 bits; best feasible area_um2=29168; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 24 evals, 15 feasible; max throughput seen 86.6 MSPS; best accuracy 11.43 bits; best feasible area_um2=21117; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (32 evals): data_width=14..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)
- `pipelined` (8 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 72 feasible; hypervolume 3.683e+04 (+46.3%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (pipelined_m, 21117 um^2) meets the throughput constraint (43.5 MSPS >= 1) and accuracy constraint (10.5 bits >= 10). The front covers the trade-off space effectively from 21117 um^2 / 10.5 bits to 35509 um^2 / 11.5 bits. Since this is the final round, we stop and select the design with minimum area (21117 um^2) as per the spec's selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 3.683e+04 (gain this round: +46.3%).
Feasible designs: 72 of 100 evaluations (56 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 190
- max_abs_err <= 0.000976562: 28% violate; best seen 1.15e-07 (2^-23.05)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=0 frac_guard=1 rounding=round m=4] area_um2=21117, accuracy_bits=10.5, ffs=200, throughput_msps=43.5, max_abs_err=0.000703 (2^-10.47), power_index=0.0235
- pipelined_m [data_width=15 n_iter=13 angle_guard=1 frac_guard=0 rounding=round m=3] area_um2=22512, accuracy_bits=10.5, ffs=290, throughput_msps=59.9, max_abs_err=0.000673 (2^-10.54), power_index=0.0294
- pipelined_m [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=3] area_um2=26770, accuracy_bits=11.4, ffs=313, throughput_msps=57, max_abs_err=0.000362 (2^-11.43), power_index=0.0332
- pipelined_m [data_width=24 n_iter=14 angle_guard=-2 frac_guard=0 rounding=trunc m=4] area_um2=33145, accuracy_bits=13, ffs=350, throughput_msps=32.3, max_abs_err=0.000124 (2^-12.97), power_index=0.039
- pipelined_m [data_width=20 n_iter=19 angle_guard=-2 frac_guard=0 rounding=trunc m=6] area_um2=36113, accuracy_bits=13.3, ffs=295, throughput_msps=25.7, max_abs_err=9.81e-05 (2^-13.32), power_index=0.0377
- pipelined_m [data_width=23 n_iter=19 angle_guard=-2 frac_guard=0 rounding=trunc m=3] area_um2=46015, accuracy_bits=16.1, ffs=554, throughput_msps=44.1, max_abs_err=1.46e-05 (2^-16.06), power_index=0.0579
- pipelined_m [data_width=24 n_iter=28 angle_guard=-2 frac_guard=1 rounding=trunc m=7] area_um2=61845, accuracy_bits=17, ffs=356, throughput_msps=18.1, max_abs_err=7.66e-06 (2^-16.99), power_index=0.0562
- pipelined_m [data_width=24 n_iter=26 angle_guard=-2 frac_guard=0 rounding=round m=3] area_um2=64852, accuracy_bits=17.1, ffs=729, throughput_msps=42.5, max_abs_err=6.97e-06 (2^-17.13), power_index=0.0787
- pipelined [data_width=27 n_iter=24 angle_guard=4 frac_guard=0 rounding=round] area_um2=101801, accuracy_bits=21.8, ffs=2171, throughput_msps=93.5, max_abs_err=2.65e-07 (2^-21.85), power_index=0.181
- pipelined [data_width=28 n_iter=25 angle_guard=1 frac_guard=3 rounding=trunc] area_um2=112825, accuracy_bits=23, ffs=2397, throughput_msps=93.5, max_abs_err=1.15e-07 (2^-23.05), power_index=0.2
Front coverage: area_um2 21117..112825 (HV reference 40000); accuracy_bits 10.5..23 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- pipelined: 44 evals, 29 feasible; max throughput seen 190 MSPS; best accuracy 23.05 bits; best feasible area_um2=29168; feasible ranges: data_width 14..28, n_iter 12..27, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 56 evals, 43 feasible; max throughput seen 86.6 MSPS; best accuracy 20.68 bits; best feasible area_um2=21117; feasible ranges: data_width 15..28, n_iter 11..28, angle_guard -2..3, frac_guard 0..3, m 2..7
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4679 in, 992 out
- provider-reported cost: $0.0025
- full prompts and replies: `llm_trace.jsonl`

