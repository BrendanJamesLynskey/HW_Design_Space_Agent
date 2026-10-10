# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec low_area_control: Field-oriented motor-control loop needing sin/cos of the rotor angle at >= 1 MSPS with max error <= 2^-10. Area is everything: minimise LUTs + FFs.
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min luts_plus_ffs (HV ref 1500)
  objective: max accuracy_bits (HV ref 10)
  select: min luts_plus_ffs
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=0,rounding=round,m=8` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 643 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 145 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 52.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 52.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 75.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0296 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000661 (2^-10.56) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 10.8 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000209 (2^-12.22) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 3.43 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.6 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (12 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=0,rounding=round,m=8` | 643 | 145 | 52.7 | 4 | 0.0296 | 0.000661 (2^-10.56) | 10.56 |
| 1 | `pipelined_m:data_width=17,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 802 | 159 | 50.3 | 4 | 0.0362 | 0.0003 (2^-11.70) | 11.70 |
| 2 | `pipelined_m:data_width=16,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=7` | 890 | 205 | 59.6 | 5 | 0.0412 | 0.000285 (2^-11.78) | 11.78 |
| 3 | `pipelined_m:data_width=16,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 954 | 151 | 52.7 | 4 | 0.0416 | 0.000219 (2^-12.16) | 12.16 |
| 4 | `pipelined_m:data_width=16,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=8` | 987 | 153 | 52.7 | 4 | 0.0429 | 0.000134 (2^-12.86) | 12.86 |
| 5 | `pipelined_m:data_width=19,n_iter=18,angle_guard=0,frac_guard=1,rounding=trunc,m=6` | 1170 | 236 | 65.4 | 5 | 0.0529 | 5.95e-05 (2^-14.04) | 14.04 |
| 6 | `pipelined_m:data_width=19,n_iter=18,angle_guard=2,frac_guard=2,rounding=round,m=6` | 1281 | 248 | 65.4 | 5 | 0.0575 | 2.34e-05 (2^-15.38) | 15.38 |
| 7 | `pipelined_m:data_width=24,n_iter=19,angle_guard=2,frac_guard=0,rounding=round,m=7` | 1523 | 294 | 54.3 | 5 | 0.0683 | 4.74e-06 (2^-17.69) | 17.69 |
| 8 | `pipelined_m:data_width=24,n_iter=22,angle_guard=1,frac_guard=0,rounding=round,m=7` | 1753 | 371 | 54.3 | 6 | 0.0799 | 1.91e-06 (2^-19.00) | 19.00 |
| 9 | `pipelined_m:data_width=24,n_iter=23,angle_guard=2,frac_guard=0,rounding=round,m=7` | 1860 | 375 | 54.3 | 6 | 0.0841 | 1.57e-06 (2^-19.28) | 19.28 |
| 10 | `pipelined_m:data_width=27,n_iter=22,angle_guard=1,frac_guard=1,rounding=round,m=3` | 2054 | 789 | 110.0 | 10 | 0.107 | 5.84e-07 (2^-20.71) | 20.71 |
| 11 | `pipelined_m:data_width=27,n_iter=22,angle_guard=3,frac_guard=1,rounding=round,m=3` | 2098 | 805 | 110.0 | 10 | 0.109 | 5.44e-07 (2^-20.81) | 20.81 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The throughput constraint (>=1 MSPS) is easily satisfied by both pipelined families because they produce one result per cycle; even a modest Fmax of a few MHz exceeds 1 MSPS. Therefore the binding constraints are area (min LUTs+FFs) and accuracy (max_abs_err <= 2^-10). Accuracy depends only on data_width, n_iter, angle_guard, frac_guard, and rounding, so we focus the search on the region where accuracy crosses 10 bits (data_width ~12-16, n_iter ~8-16) and let the guards/rounding provide fine trade-offs. For area, pipelined_m can reduce flip-flops by registering every m stages, trading Fmax for area; since throughput is not tight, larger m may yield lower LUT+FF. We include the plain pipelined family as the m=1 baseline. Budget is split to give more evaluations to pipelined_m because it has an extra parameter and likely contains the area-optimal designs, while still covering pipelined to avoid missing a better m=1 solution. All 100 evaluations are allocated in this first round according to the shares above.*)
- `pipelined` (24 evals): data_width=12..16, n_iter=8..16, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Baseline one-register-per-micro-rotation pipeline. It gives the highest Fmax and simplest control, but may use more FFs. Searching it ensures we do not miss the case where m=1 is area-optimal. The ranges focus on the accuracy-feasible, low-area region: data_width 12-16 and n_iter 8-16 should cross the 2^-10 error constraint, while small guards keep area low. Rounding is included because it can improve accuracy at little area cost.
- `pipelined_m` (36 evals): data_width=12..16, n_iter=8..16, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* Registers every m stages, so it can reduce FF count at the cost of lower Fmax. Since the throughput constraint is only 1 MSPS, this trade-off is likely favourable for the area objective. The extra m parameter creates a richer Pareto front, so it receives the larger budget share. m=1 is covered by the pipelined family. The same focused accuracy/area ranges are used, with m 2-8 to explore the FF-vs-Fmax trade-off.

**Result (code):** 60 evaluations this round, 60 total; 29 feasible; hypervolume 1381 (n/a).

**LLM decision:** `stop` — Constraints are demonstrably reachable, so `infeasible` is wrong: 29 of 60 evaluations were feasible (21 unique), throughput >= 1 MSPS is met with a 0% violation rate (best seen 282 MSPS), and max_abs_err <= 2^-10 is met with 48% of evaluations feasible and best seen 2^-12.86. The feasible Pareto front already covers the trade-off well against the spec's HV reference point: luts_plus_ffs spans 788..1141 against ref 1500, and accuracy_bits spans 10.6..12.9 against ref 10, giving HV 1381. The spec's selection rule (min luts_plus_ffs) is served directly by the front's corner: pipelined_m [W=16 N=12 angle_guard=1 frac_guard=0 round m=8] at 788 LUT+FF, err 2^-10.56 (<= 2^-10) and 52.7 MSPS (>= 1 MSPS), with power_index 0.0296 and 145 FFs. This is the final round, so no further refinement, widening, family addition or full-range front mapping can be executed; the run ends with a feasible, constraint-satisfying front whose selection corner is already identified.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1381 (gain this round: n/a (first round)).
Feasible designs: 29 of 60 evaluations (21 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 52% violate; best seen 0.000134 (2^-12.86)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=0 rounding=round m=8] luts_plus_ffs=788, accuracy_bits=10.6, luts=643, ffs=145, throughput_msps=52.7, max_abs_err=0.000661 (2^-10.56), power_index=0.0296
- pipelined_m [data_width=16 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=8] luts_plus_ffs=1020, accuracy_bits=11.7, luts=875, ffs=145, throughput_msps=52.7, max_abs_err=0.000301 (2^-11.70), power_index=0.0384
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=7] luts_plus_ffs=1095, accuracy_bits=11.8, luts=890, ffs=205, throughput_msps=59.6, max_abs_err=0.000285 (2^-11.78), power_index=0.0412
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=1105, accuracy_bits=12.2, luts=954, ffs=151, throughput_msps=52.7, max_abs_err=0.000219 (2^-12.16), power_index=0.0416
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=8] luts_plus_ffs=1141, accuracy_bits=12.9, luts=987, ffs=153, throughput_msps=52.7, max_abs_err=0.000134 (2^-12.86), power_index=0.0429
Front coverage: luts_plus_ffs 788..1141 (HV reference 1500); accuracy_bits 10.6..12.9 (HV reference 10); data_width on the front 16..16 (registry 8..28).

Per family:
- pipelined: 24 evals, 15 feasible; max throughput seen 282 MSPS; best accuracy 12.26 bits; best feasible luts_plus_ffs=1321; feasible ranges: data_width 16..16, n_iter 12..15, angle_guard 1..2, frac_guard 0..2
- pipelined_m: 36 evals, 14 feasible; max throughput seen 178 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=788; feasible ranges: data_width 14..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2, m 4..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=15..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (5 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 69 feasible; hypervolume 1559 (+12.9%).

**No LLM call** (code's front-mapping round): Constraints are demonstrably reachable, so `infeasible` is wrong: 29 of 60 evaluations were feasible (21 unique), throughput >= 1 MSPS is met with a 0% violation rate (best seen 282 MSPS), and max_abs_err <= 2^-10 is met with 48% of evaluations feasible and best seen 2^-12.86. The feasible Pareto front already covers the trade-off well against the spec's HV reference point: luts_plus_ffs spans 788..1141 against ref 1500, and accuracy_bits spans 10.6..12.9 against ref 10, giving HV 1381. The spec's selection rule (min luts_plus_ffs) is served directly by the front's corner: pipelined_m [W=16 N=12 angle_guard=1 frac_guard=0 round m=8] at 788 LUT+FF, err 2^-10.56 (<= 2^-10) and 52.7 MSPS (>= 1 MSPS), with power_index 0.0296 and 145 FFs. This is the final round, so no further refinement, widening, family addition or full-range front mapping can be executed; the run ends with a feasible, constraint-satisfying front whose selection corner is already identified.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1559 (gain this round: +12.9%).
Feasible designs: 69 of 100 evaluations (57 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 31% violate; best seen 5.44e-07 (2^-20.81)

Pareto front (feasible, 12 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=0 rounding=round m=8] luts_plus_ffs=788, accuracy_bits=10.6, luts=643, ffs=145, throughput_msps=52.7, max_abs_err=0.000661 (2^-10.56), power_index=0.0296
- pipelined_m [data_width=17 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=961, accuracy_bits=11.7, luts=802, ffs=159, throughput_msps=50.3, max_abs_err=0.0003 (2^-11.70), power_index=0.0362
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=7] luts_plus_ffs=1095, accuracy_bits=11.8, luts=890, ffs=205, throughput_msps=59.6, max_abs_err=0.000285 (2^-11.78), power_index=0.0412
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=8] luts_plus_ffs=1141, accuracy_bits=12.9, luts=987, ffs=153, throughput_msps=52.7, max_abs_err=0.000134 (2^-12.86), power_index=0.0429
- pipelined_m [data_width=19 n_iter=18 angle_guard=0 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=1406, accuracy_bits=14, luts=1170, ffs=236, throughput_msps=65.4, max_abs_err=5.95e-05 (2^-14.04), power_index=0.0529
- pipelined_m [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=round m=6] luts_plus_ffs=1530, accuracy_bits=15.4, luts=1281, ffs=248, throughput_msps=65.4, max_abs_err=2.34e-05 (2^-15.38), power_index=0.0575
- pipelined_m [data_width=24 n_iter=19 angle_guard=2 frac_guard=0 rounding=round m=7] luts_plus_ffs=1816, accuracy_bits=17.7, luts=1523, ffs=294, throughput_msps=54.3, max_abs_err=4.74e-06 (2^-17.69), power_index=0.0683
- pipelined_m [data_width=24 n_iter=23 angle_guard=2 frac_guard=0 rounding=round m=7] luts_plus_ffs=2235, accuracy_bits=19.3, luts=1860, ffs=375, throughput_msps=54.3, max_abs_err=1.57e-06 (2^-19.28), power_index=0.0841
- pipelined_m [data_width=27 n_iter=22 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=2843, accuracy_bits=20.7, luts=2054, ffs=789, throughput_msps=110, max_abs_err=5.84e-07 (2^-20.71), power_index=0.107
- pipelined_m [data_width=27 n_iter=22 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=2903, accuracy_bits=20.8, luts=2098, ffs=805, throughput_msps=110, max_abs_err=5.44e-07 (2^-20.81), power_index=0.109
Front coverage: luts_plus_ffs 788..2903 (HV reference 1500); accuracy_bits 10.6..20.8 (HV reference 10); data_width on the front 16..27 (registry 8..28).

Per family:
- pipelined: 24 evals, 15 feasible; max throughput seen 282 MSPS; best accuracy 12.26 bits; best feasible luts_plus_ffs=1321; feasible ranges: data_width 16..16, n_iter 12..15, angle_guard 1..2, frac_guard 0..2
- pipelined_m: 76 evals, 54 feasible; max throughput seen 178 MSPS; best accuracy 20.81 bits; best feasible luts_plus_ffs=788; feasible ranges: data_width 14..27, n_iter 12..29, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4017 in, 6644 out
- provider-reported cost: $0.0077
- full prompts and replies: `llm_trace.jsonl`

