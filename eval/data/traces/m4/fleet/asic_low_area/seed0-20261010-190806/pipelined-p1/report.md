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
`pipelined_m:data_width=16,n_iter=12,angle_guard=0,frac_guard=0,rounding=trunc,m=8` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 18406 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 4904 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 140 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 23.6 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 23.6 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 170 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.0186 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000887 (2^-10.14) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 14.5 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.00023 (2^-12.08) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 3.77 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.1 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (16 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=12,angle_guard=0,frac_guard=0,rounding=trunc,m=8` | 18406 | 140 | 23.6 | 4 | 0.0186 | 0.000887 (2^-10.14) | 10.14 |
| 1 | `pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=7` | 19055 | 144 | 24.2 | 4 | 0.0192 | 0.000654 (2^-10.58) | 10.58 |
| 2 | `pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=8` | 19055 | 144 | 21.3 | 4 | 0.0192 | 0.000654 (2^-10.58) | 10.58 |
| 3 | `pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=2,rounding=round,m=7` | 20804 | 147 | 24.2 | 4 | 0.0205 | 0.000602 (2^-10.70) | 10.70 |
| 4 | `pipelined_m:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=7` | 21166 | 140 | 26.8 | 4 | 0.0202 | 0.0004 (2^-11.29) | 11.29 |
| 5 | `pipelined_m:data_width=16,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=7` | 22958 | 146 | 24.2 | 4 | 0.0216 | 0.000311 (2^-11.65) | 11.65 |
| 6 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=7` | 24195 | 149 | 24.2 | 4 | 0.0226 | 0.000204 (2^-12.26) | 12.26 |
| 7 | `pipelined_m:data_width=16,n_iter=18,angle_guard=1,frac_guard=3,rounding=trunc,m=8` | 31254 | 208 | 20.3 | 5 | 0.03 | 0.000203 (2^-12.27) | 12.27 |
| 8 | `pipelined_m:data_width=16,n_iter=18,angle_guard=2,frac_guard=3,rounding=round,m=7` | 32615 | 213 | 23.1 | 5 | 0.0311 | 0.000112 (2^-13.13) | 13.13 |
| 9 | `pipelined_m:data_width=23,n_iter=17,angle_guard=3,frac_guard=3,rounding=trunc,m=7` | 40911 | 290 | 17.5 | 5 | 0.0402 | 1.59e-05 (2^-15.94) | 15.94 |
| 10 | `pipelined_m:data_width=27,n_iter=17,angle_guard=4,frac_guard=3,rounding=trunc,m=8` | 47252 | 336 | 13.0 | 5 | 0.0465 | 1.53e-05 (2^-16.00) | 16.00 |
| 11 | `pipelined_m:data_width=24,n_iter=24,angle_guard=-1,frac_guard=2,rounding=trunc,m=7` | 55854 | 366 | 17.5 | 6 | 0.0533 | 3.54e-06 (2^-18.11) | 18.11 |
| 12 | `pipelined_m:data_width=23,n_iter=26,angle_guard=3,frac_guard=1,rounding=trunc,m=7` | 59267 | 362 | 17.5 | 6 | 0.055 | 3.15e-06 (2^-18.28) | 18.28 |
| 13 | `pipelined_m:data_width=27,n_iter=23,angle_guard=4,frac_guard=1,rounding=trunc,m=7` | 61752 | 421 | 14.9 | 6 | 0.0598 | 3.68e-07 (2^-21.38) | 21.38 |
| 14 | `pipelined_m:data_width=27,n_iter=24,angle_guard=4,frac_guard=2,rounding=trunc,m=7` | 65435 | 427 | 14.9 | 6 | 0.0623 | 1.99e-07 (2^-22.26) | 22.26 |
| 15 | `pipelined_m:data_width=27,n_iter=24,angle_guard=4,frac_guard=4,rounding=round,m=8` | 67289 | 342 | 13.0 | 5 | 0.0587 | 1.43e-07 (2^-22.74) | 22.74 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires max_abs_err <= 2^-10, which sets hard lower bounds: data_width >= 11 (since output LSB = 2^-(W-2) and half-LSB must be <= 2^-10) and n_iter >= 10 (CORDIC angle approximation error ~2^-N). Throughput >= 1 MSPS is trivially satisfied by both pipelined families (1 result/cycle) even at low Fmax, so area is the only binding objective. We search both families over the accuracy boundary (W 11..16, N 10..18) and guard bits, with pipelined_m receiving most budget because its m parameter (2..8) allows trading FFs for combinational depth, directly reducing area. The ranges cover designs from just meeting 10-bit accuracy up to ~14-bit accuracy, enabling the Pareto front to be mapped. No infeasibility is expected; if no design meets the error constraint, code will report it.*)
- `pipelined` (12 evals): data_width=11..16, n_iter=10..18, angle_guard=-1..2, frac_guard=0..3, rounding=trunc|round. *Why:* Baseline pipelined family (m=1) provides a reference point and covers the high-Fmax corner. It is a special case of pipelined_m, so it helps confirm that register sharing reduces area. Small budget because pipelined_m with m>1 should dominate for area.
- `pipelined_m` (48 evals): data_width=11..16, n_iter=10..18, angle_guard=-1..2, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* Main family for area minimisation. Registering every m stages reduces flip-flop count while keeping 1 result/cycle, so larger m can yield smaller area. The m dimension is the key trade-off between FF count and combinational depth; throughput constraint (>=1 MSPS) is easily met even at low Fmax. Majority budget to explore m and the accuracy boundary.

**Result (code):** 60 evaluations this round, 60 total; 35 feasible; hypervolume 4.782e+04 (n/a).

**LLM decision:** `stop` — Final round: the feasible front is established and the spec is satisfiable. Constraints are met with margin — throughput best seen 190 MSPS vs >=1 required (0% violations), and max_abs_err best 2^-13.13 vs <=2^-10 required. The Pareto front spans area_um2 18406..32615 against the HV reference 40000 and accuracy_bits 10.1..13.1 against reference 10, so it covers a wide portion of both objective ranges (HV 4.782e+04). The selection rule (min area_um2) picks pipelined_m [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc m=8] at area_um2=18406, accuracy_bits=10.14 (max_abs_err=0.000887 <= 0.000976562), throughput 23.6 MSPS >= 1 — a valid, constraint-satisfying optimum. No infeasibility: every constraint is achieved by multiple designs. Stopping.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 4.782e+04 (gain this round: n/a (first round)).
Feasible designs: 35 of 60 evaluations (28 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 190
- max_abs_err <= 0.000976562: 42% violate; best seen 0.000112 (2^-13.13)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc m=8] area_um2=18406, accuracy_bits=10.1, ffs=140, throughput_msps=23.6, max_abs_err=0.000887 (2^-10.14), power_index=0.0186
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=0 rounding=round m=7] area_um2=19055, accuracy_bits=10.6, ffs=144, throughput_msps=24.2, max_abs_err=0.000654 (2^-10.58), power_index=0.0192
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=0 rounding=round m=8] area_um2=19055, accuracy_bits=10.6, ffs=144, throughput_msps=21.3, max_abs_err=0.000654 (2^-10.58), power_index=0.0192
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=2 rounding=round m=7] area_um2=20804, accuracy_bits=10.7, ffs=147, throughput_msps=24.2, max_abs_err=0.000602 (2^-10.70), power_index=0.0205
- pipelined_m [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=7] area_um2=21166, accuracy_bits=11.3, ffs=140, throughput_msps=26.8, max_abs_err=0.0004 (2^-11.29), power_index=0.0202
- pipelined_m [data_width=16 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=7] area_um2=22958, accuracy_bits=11.7, ffs=146, throughput_msps=24.2, max_abs_err=0.000311 (2^-11.65), power_index=0.0216
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=7] area_um2=24195, accuracy_bits=12.3, ffs=149, throughput_msps=24.2, max_abs_err=0.000204 (2^-12.26), power_index=0.0226
- pipelined_m [data_width=16 n_iter=18 angle_guard=1 frac_guard=3 rounding=trunc m=8] area_um2=31254, accuracy_bits=12.3, ffs=208, throughput_msps=20.3, max_abs_err=0.000203 (2^-12.27), power_index=0.03
- pipelined_m [data_width=16 n_iter=18 angle_guard=2 frac_guard=3 rounding=round m=7] area_um2=32615, accuracy_bits=13.1, ffs=213, throughput_msps=23.1, max_abs_err=0.000112 (2^-13.13), power_index=0.0311
Front coverage: area_um2 18406..32615 (HV reference 40000); accuracy_bits 10.1..13.1 (HV reference 10); data_width on the front 16..16 (registry 8..28).

Per family:
- pipelined: 12 evals, 5 feasible; max throughput seen 190 MSPS; best accuracy 11.83 bits; best feasible area_um2=31571; feasible ranges: data_width 16..16, n_iter 12..17, angle_guard -1..1, frac_guard 1..3
- pipelined_m: 48 evals, 30 feasible; max throughput seen 70.8 MSPS; best accuracy 13.13 bits; best feasible area_um2=18406; feasible ranges: data_width 15..16, n_iter 12..18, angle_guard 0..2, frac_guard 0..3, m 3..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=15..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (9 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 72 feasible; hypervolume 4.782e+04 (+0.0%).

**No LLM call** (code's front-mapping round): Final round: the feasible front is established and the spec is satisfiable. Constraints are met with margin — throughput best seen 190 MSPS vs >=1 required (0% violations), and max_abs_err best 2^-13.13 vs <=2^-10 required. The Pareto front spans area_um2 18406..32615 against the HV reference 40000 and accuracy_bits 10.1..13.1 against reference 10, so it covers a wide portion of both objective ranges (HV 4.782e+04). The selection rule (min area_um2) picks pipelined_m [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc m=8] at area_um2=18406, accuracy_bits=10.14 (max_abs_err=0.000887 <= 0.000976562), throughput 23.6 MSPS >= 1 — a valid, constraint-satisfying optimum. No infeasibility: every constraint is achieved by multiple designs. Stopping.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 4.782e+04 (gain this round: +0.0%).
Feasible designs: 72 of 100 evaluations (62 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 190
- max_abs_err <= 0.000976562: 28% violate; best seen 1.43e-07 (2^-22.74)

Pareto front (feasible, 16 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc m=8] area_um2=18406, accuracy_bits=10.1, ffs=140, throughput_msps=23.6, max_abs_err=0.000887 (2^-10.14), power_index=0.0186
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=0 rounding=round m=8] area_um2=19055, accuracy_bits=10.6, ffs=144, throughput_msps=21.3, max_abs_err=0.000654 (2^-10.58), power_index=0.0192
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=2 rounding=round m=7] area_um2=20804, accuracy_bits=10.7, ffs=147, throughput_msps=24.2, max_abs_err=0.000602 (2^-10.70), power_index=0.0205
- pipelined_m [data_width=16 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=7] area_um2=22958, accuracy_bits=11.7, ffs=146, throughput_msps=24.2, max_abs_err=0.000311 (2^-11.65), power_index=0.0216
- pipelined_m [data_width=16 n_iter=18 angle_guard=1 frac_guard=3 rounding=trunc m=8] area_um2=31254, accuracy_bits=12.3, ffs=208, throughput_msps=20.3, max_abs_err=0.000203 (2^-12.27), power_index=0.03
- pipelined_m [data_width=16 n_iter=18 angle_guard=2 frac_guard=3 rounding=round m=7] area_um2=32615, accuracy_bits=13.1, ffs=213, throughput_msps=23.1, max_abs_err=0.000112 (2^-13.13), power_index=0.0311
- pipelined_m [data_width=27 n_iter=17 angle_guard=4 frac_guard=3 rounding=trunc m=8] area_um2=47252, accuracy_bits=16, ffs=336, throughput_msps=13, max_abs_err=1.53e-05 (2^-16.00), power_index=0.0465
- pipelined_m [data_width=23 n_iter=26 angle_guard=3 frac_guard=1 rounding=trunc m=7] area_um2=59267, accuracy_bits=18.3, ffs=362, throughput_msps=17.5, max_abs_err=3.15e-06 (2^-18.28), power_index=0.055
- pipelined_m [data_width=27 n_iter=23 angle_guard=4 frac_guard=1 rounding=trunc m=7] area_um2=61752, accuracy_bits=21.4, ffs=421, throughput_msps=14.9, max_abs_err=3.68e-07 (2^-21.38), power_index=0.0598
- pipelined_m [data_width=27 n_iter=24 angle_guard=4 frac_guard=4 rounding=round m=8] area_um2=67289, accuracy_bits=22.7, ffs=342, throughput_msps=13, max_abs_err=1.43e-07 (2^-22.74), power_index=0.0587
Front coverage: area_um2 18406..67289 (HV reference 40000); accuracy_bits 10.1..22.7 (HV reference 10); data_width on the front 16..27 (registry 8..28).

Per family:
- pipelined: 12 evals, 5 feasible; max throughput seen 190 MSPS; best accuracy 11.83 bits; best feasible area_um2=31571; feasible ranges: data_width 16..16, n_iter 12..17, angle_guard -1..1, frac_guard 1..3
- pipelined_m: 88 evals, 67 feasible; max throughput seen 82.5 MSPS; best accuracy 22.74 bits; best feasible area_um2=18406; feasible ranges: data_width 15..27, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4396 in, 5117 out
- provider-reported cost: $0.0044
- full prompts and replies: `llm_trace.jsonl`

