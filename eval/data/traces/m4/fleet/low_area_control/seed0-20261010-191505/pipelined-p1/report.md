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
`pipelined_m:data_width=16,n_iter=12,angle_guard=0,frac_guard=0,rounding=trunc,m=8` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 631 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 143 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 52.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 52.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 75.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0291 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000887 (2^-10.14) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 14.5 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.00023 (2^-12.08) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 3.77 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.1 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (23 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=12,angle_guard=0,frac_guard=0,rounding=trunc,m=8` | 631 | 143 | 52.7 | 4 | 0.0291 | 0.000887 (2^-10.14) | 10.14 |
| 1 | `pipelined_m:data_width=15,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=4` | 620 | 194 | 97.8 | 5 | 0.0306 | 0.000835 (2^-10.23) | 10.23 |
| 2 | `pipelined_m:data_width=15,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=5` | 620 | 194 | 80.6 | 5 | 0.0306 | 0.000835 (2^-10.23) | 10.23 |
| 3 | `pipelined_m:data_width=15,n_iter=12,angle_guard=2,frac_guard=3,rounding=trunc,m=8` | 689 | 145 | 52.7 | 4 | 0.0314 | 0.00067 (2^-10.54) | 10.54 |
| 4 | `pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=2,rounding=trunc,m=7` | 689 | 149 | 59.6 | 4 | 0.0315 | 0.000609 (2^-10.68) | 10.68 |
| 5 | `pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=2,rounding=trunc,m=8` | 689 | 149 | 52.7 | 4 | 0.0315 | 0.000609 (2^-10.68) | 10.68 |
| 6 | `pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=2,rounding=trunc,m=6` | 689 | 149 | 68.5 | 4 | 0.0315 | 0.000609 (2^-10.68) | 10.68 |
| 7 | `pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=2,rounding=trunc,m=7` | 701 | 151 | 59.6 | 4 | 0.0321 | 0.000597 (2^-10.71) | 10.71 |
| 8 | `pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=3,rounding=round,m=8` | 746 | 153 | 50.3 | 4 | 0.0338 | 0.000587 (2^-10.73) | 10.73 |
| 9 | `pipelined_m:data_width=15,n_iter=13,angle_guard=2,frac_guard=3,rounding=round,m=7` | 783 | 147 | 59.6 | 4 | 0.035 | 0.000358 (2^-11.45) | 11.45 |
| 10 | `pipelined_m:data_width=16,n_iter=13,angle_guard=2,frac_guard=2,rounding=round,m=7` | 798 | 153 | 59.6 | 4 | 0.0358 | 0.00031 (2^-11.65) | 11.65 |
| 11 | `pipelined_m:data_width=15,n_iter=14,angle_guard=2,frac_guard=3,rounding=round,m=8` | 845 | 147 | 52.7 | 4 | 0.0373 | 0.00029 (2^-11.75) | 11.75 |
| 12 | `pipelined_m:data_width=16,n_iter=16,angle_guard=1,frac_guard=3,rounding=trunc,m=8` | 969 | 151 | 50.3 | 4 | 0.0422 | 0.000237 (2^-12.04) | 12.04 |
| 13 | `pipelined_m:data_width=16,n_iter=16,angle_guard=2,frac_guard=3,rounding=trunc,m=8` | 985 | 153 | 50.3 | 4 | 0.0428 | 0.000175 (2^-12.48) | 12.48 |
| 14 | `pipelined_m:data_width=22,n_iter=17,angle_guard=-2,frac_guard=4,rounding=round,m=8` | 1367 | 277 | 48.0 | 5 | 0.0618 | 3.29e-05 (2^-14.89) | 14.89 |
| 15 | `pipelined_m:data_width=22,n_iter=17,angle_guard=3,frac_guard=4,rounding=trunc,m=7` | 1405 | 291 | 54.3 | 5 | 0.0638 | 1.65e-05 (2^-15.89) | 15.89 |
| 16 | `pipelined_m:data_width=26,n_iter=17,angle_guard=4,frac_guard=4,rounding=trunc,m=8` | 1624 | 338 | 45.9 | 5 | 0.0738 | 1.53e-05 (2^-16.00) | 16.00 |
| 17 | `pipelined_m:data_width=23,n_iter=19,angle_guard=-1,frac_guard=1,rounding=round,m=2` | 1495 | 823 | 158.3 | 12 | 0.0872 | 8.6e-06 (2^-16.83) | 16.83 |
| 18 | `pipelined_m:data_width=23,n_iter=19,angle_guard=0,frac_guard=1,rounding=round,m=2` | 1514 | 833 | 158.3 | 12 | 0.0883 | 6.39e-06 (2^-17.25) | 17.25 |
| 19 | `pipelined_m:data_width=23,n_iter=19,angle_guard=0,frac_guard=4,rounding=round,m=2` | 1628 | 888 | 152.6 | 12 | 0.0946 | 6.1e-06 (2^-17.32) | 17.32 |
| 20 | `pipelined_m:data_width=23,n_iter=25,angle_guard=3,frac_guard=3,rounding=round,m=8` | 2178 | 385 | 48.0 | 6 | 0.0964 | 7.87e-07 (2^-20.28) | 20.28 |
| 21 | `pipelined_m:data_width=26,n_iter=24,angle_guard=4,frac_guard=2,rounding=trunc,m=7` | 2235 | 424 | 52.0 | 6 | 0.1 | 3.21e-07 (2^-21.57) | 21.57 |
| 22 | `pipelined_m:data_width=25,n_iter=24,angle_guard=4,frac_guard=4,rounding=round,m=7` | 2312 | 424 | 52.0 | 6 | 0.103 | 2.16e-07 (2^-22.14) | 22.14 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-first: minimise LUTs+FFs while meeting a modest 1 MSPS throughput and a 2^-10 max absolute error. Both assigned families are pipelined and therefore trivially satisfy throughput (1 result/cycle, Fmax >> 1 MHz). The real trade-off is area versus accuracy. Accuracy depends only on data_width, n_iter, angle_guard, frac_guard and rounding, so both families share the same accuracy parameter space. I focus the search on data_width 11-16 and n_iter 8-16: below W=11 the output LSB alone (2^-9) makes the 2^-10 error constraint nearly impossible, while above W=16 area grows quickly and is unlikely to help the hypervolume reference point (area ref 1500). Guards and rounding are varied to find cheap accuracy improvements. pipelined_m receives 70% of the budget because its m parameter can cut FFs without affecting throughput, making it the likely area winner; pipelined gets 30% to map the front and provide a higher-Fmax reference. This first round is exploratory but concentrated where feasible, low-area designs should exist.*)
- `pipelined` (18 evals): data_width=11..16, n_iter=8..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* Pipelined gives 1 result/cycle and easily meets the 1 MSPS throughput constraint. It is the baseline for area comparison; its fully registered stages may cost more FFs than pipelined_m, but it can achieve higher Fmax and serves as a reference point on the Pareto front. The ranges focus on small data widths (11-16) and iteration counts (8-16) where the 2^-10 error constraint is likely to become feasible, while guards and rounding are varied to find the cheapest way to reach that accuracy.
- `pipelined_m` (42 evals): data_width=11..16, n_iter=8..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* pipelined_m keeps the 1 result/cycle throughput but registers only every m stages, so larger m directly reduces flip-flop count. Since the throughput constraint is only 1 MSPS, Fmax can be traded for area, making this family the most promising for the min luts_plus_ffs objective. The m range 2-8 covers the full registry, and the accuracy parameters are the same as pipelined so the two families can be compared fairly on the same accuracy/area trade-off.

**Result (code):** 60 evaluations this round, 60 total; 34 feasible; hypervolume 1334 (n/a).

**LLM decision:** `stop` — Final round: the feasible front is well mapped and no further action is possible. Constraints are satisfiable — throughput_msps >= 1 is met by every feasible design (best 282, front designs 50-98 MSPS) and max_abs_err <= 2^-10 is met by all 14 front designs (best 2^-12.48). The front already spans the area objective from 774 to 1139 luts_plus_ffs against the HV reference 1500, and accuracy from 10.1 to 12.5 bits against the HV reference 10, so hypervolume coverage is strong (1334). The selection rule (min luts_plus_ffs) is satisfied by pipelined_m [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc m=8] at 774 LUTs+FFs, 10.1 accuracy bits, 52.7 MSPS, 0.000887 max_abs_err — feasible on all constraints. No infeasibility evidence exists, so stopping is correct.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1334 (gain this round: n/a (first round)).
Feasible designs: 34 of 60 evaluations (28 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 43% violate; best seen 0.000175 (2^-12.48)

Pareto front (feasible, 14 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc m=8] luts_plus_ffs=774, accuracy_bits=10.1, luts=631, ffs=143, throughput_msps=52.7, max_abs_err=0.000887 (2^-10.14), power_index=0.0291
- pipelined_m [data_width=15 n_iter=12 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=813, accuracy_bits=10.2, luts=620, ffs=194, throughput_msps=97.8, max_abs_err=0.000835 (2^-10.23), power_index=0.0306
- pipelined_m [data_width=15 n_iter=12 angle_guard=2 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=834, accuracy_bits=10.5, luts=689, ffs=145, throughput_msps=52.7, max_abs_err=0.00067 (2^-10.54), power_index=0.0314
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=838, accuracy_bits=10.7, luts=689, ffs=149, throughput_msps=59.6, max_abs_err=0.000609 (2^-10.68), power_index=0.0315
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=2 rounding=trunc m=6] luts_plus_ffs=838, accuracy_bits=10.7, luts=689, ffs=149, throughput_msps=68.5, max_abs_err=0.000609 (2^-10.68), power_index=0.0315
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=852, accuracy_bits=10.7, luts=701, ffs=151, throughput_msps=59.6, max_abs_err=0.000597 (2^-10.71), power_index=0.0321
- pipelined_m [data_width=15 n_iter=13 angle_guard=2 frac_guard=3 rounding=round m=7] luts_plus_ffs=930, accuracy_bits=11.4, luts=783, ffs=147, throughput_msps=59.6, max_abs_err=0.000358 (2^-11.45), power_index=0.035
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=round m=7] luts_plus_ffs=951, accuracy_bits=11.7, luts=798, ffs=153, throughput_msps=59.6, max_abs_err=0.00031 (2^-11.65), power_index=0.0358
- pipelined_m [data_width=16 n_iter=16 angle_guard=1 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1121, accuracy_bits=12, luts=969, ffs=151, throughput_msps=50.3, max_abs_err=0.000237 (2^-12.04), power_index=0.0422
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1139, accuracy_bits=12.5, luts=985, ffs=153, throughput_msps=50.3, max_abs_err=0.000175 (2^-12.48), power_index=0.0428
Front coverage: luts_plus_ffs 774..1139 (HV reference 1500); accuracy_bits 10.1..12.5 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- pipelined: 18 evals, 6 feasible; max throughput seen 282 MSPS; best accuracy 11.97 bits; best feasible luts_plus_ffs=1581; feasible ranges: data_width 14..16, n_iter 14..15, angle_guard -1..1, frac_guard 1..3
- pipelined_m: 42 evals, 28 feasible; max throughput seen 130 MSPS; best accuracy 12.48 bits; best feasible luts_plus_ffs=774; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard -1..2, frac_guard 0..3, m 3..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=14..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (14 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 70 feasible; hypervolume 1334 (+0.0%).

**No LLM call** (code's front-mapping round): Final round: the feasible front is well mapped and no further action is possible. Constraints are satisfiable — throughput_msps >= 1 is met by every feasible design (best 282, front designs 50-98 MSPS) and max_abs_err <= 2^-10 is met by all 14 front designs (best 2^-12.48). The front already spans the area objective from 774 to 1139 luts_plus_ffs against the HV reference 1500, and accuracy from 10.1 to 12.5 bits against the HV reference 10, so hypervolume coverage is strong (1334). The selection rule (min luts_plus_ffs) is satisfied by pipelined_m [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc m=8] at 774 LUTs+FFs, 10.1 accuracy bits, 52.7 MSPS, 0.000887 max_abs_err — feasible on all constraints. No infeasibility evidence exists, so stopping is correct.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1334 (gain this round: +0.0%).
Feasible designs: 70 of 100 evaluations (60 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 30% violate; best seen 2.16e-07 (2^-22.14)

Pareto front (feasible, 23 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc m=8] luts_plus_ffs=774, accuracy_bits=10.1, luts=631, ffs=143, throughput_msps=52.7, max_abs_err=0.000887 (2^-10.14), power_index=0.0291
- pipelined_m [data_width=15 n_iter=12 angle_guard=2 frac_guard=0 rounding=round m=5] luts_plus_ffs=813, accuracy_bits=10.2, luts=620, ffs=194, throughput_msps=80.6, max_abs_err=0.000835 (2^-10.23), power_index=0.0306
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=838, accuracy_bits=10.7, luts=689, ffs=149, throughput_msps=52.7, max_abs_err=0.000609 (2^-10.68), power_index=0.0315
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=852, accuracy_bits=10.7, luts=701, ffs=151, throughput_msps=59.6, max_abs_err=0.000597 (2^-10.71), power_index=0.0321
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=round m=7] luts_plus_ffs=951, accuracy_bits=11.7, luts=798, ffs=153, throughput_msps=59.6, max_abs_err=0.00031 (2^-11.65), power_index=0.0358
- pipelined_m [data_width=16 n_iter=16 angle_guard=1 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1121, accuracy_bits=12, luts=969, ffs=151, throughput_msps=50.3, max_abs_err=0.000237 (2^-12.04), power_index=0.0422
- pipelined_m [data_width=22 n_iter=17 angle_guard=3 frac_guard=4 rounding=trunc m=7] luts_plus_ffs=1695, accuracy_bits=15.9, luts=1405, ffs=291, throughput_msps=54.3, max_abs_err=1.65e-05 (2^-15.89), power_index=0.0638
- pipelined_m [data_width=23 n_iter=19 angle_guard=-1 frac_guard=1 rounding=round m=2] luts_plus_ffs=2319, accuracy_bits=16.8, luts=1495, ffs=823, throughput_msps=158, max_abs_err=8.6e-06 (2^-16.83), power_index=0.0872
- pipelined_m [data_width=23 n_iter=25 angle_guard=3 frac_guard=3 rounding=round m=8] luts_plus_ffs=2564, accuracy_bits=20.3, luts=2178, ffs=385, throughput_msps=48, max_abs_err=7.87e-07 (2^-20.28), power_index=0.0964
- pipelined_m [data_width=25 n_iter=24 angle_guard=4 frac_guard=4 rounding=round m=7] luts_plus_ffs=2736, accuracy_bits=22.1, luts=2312, ffs=424, throughput_msps=52, max_abs_err=2.16e-07 (2^-22.14), power_index=0.103
Front coverage: luts_plus_ffs 774..2736 (HV reference 1500); accuracy_bits 10.1..22.1 (HV reference 10); data_width on the front 15..26 (registry 8..28).

Per family:
- pipelined: 18 evals, 6 feasible; max throughput seen 282 MSPS; best accuracy 11.97 bits; best feasible luts_plus_ffs=1581; feasible ranges: data_width 14..16, n_iter 14..15, angle_guard -1..1, frac_guard 1..3
- pipelined_m: 82 evals, 64 feasible; max throughput seen 171 MSPS; best accuracy 22.14 bits; best feasible luts_plus_ffs=774; feasible ranges: data_width 15..26, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4473 in, 4552 out
- provider-reported cost: $0.0065
- full prompts and replies: `llm_trace.jsonl`

