# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
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
`pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=1,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 638 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 189 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 51.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0311 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000976 (2^-10.00) | exact: bit-accurate model, exhaustive (16384 angles) |
| max_abs_err_lsb | 4 | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err | 0.000264 (2^-11.89) | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err_lsb | 1.08 | exact: bit-accurate model, exhaustive (16384 angles) |
| accuracy_bits | 10 | exact: bit-accurate model, exhaustive (16384 angles) |

## Pareto front (11 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=1,rounding=round,m=4` | 638 | 189 | 97.8 | 5 | 0.0311 | 0.000976 (2^-10.00) | 10.00 |
| 1 | `pipelined_m:data_width=16,n_iter=13,angle_guard=0,frac_guard=0,rounding=round,m=8` | 688 | 143 | 52.7 | 4 | 0.0313 | 0.000492 (2^-10.99) | 10.99 |
| 2 | `pipelined_m:data_width=16,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 764 | 151 | 52.7 | 4 | 0.0344 | 0.000378 (2^-11.37) | 11.37 |
| 3 | `pipelined_m:data_width=17,n_iter=13,angle_guard=1,frac_guard=2,rounding=trunc,m=6` | 789 | 221 | 65.4 | 5 | 0.038 | 0.000309 (2^-11.66) | 11.66 |
| 4 | `pipelined_m:data_width=17,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc,m=6` | 802 | 224 | 65.4 | 5 | 0.0386 | 0.0003 (2^-11.70) | 11.70 |
| 5 | `pipelined_m:data_width=18,n_iter=13,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 815 | 297 | 93.6 | 6 | 0.0418 | 0.000286 (2^-11.77) | 11.77 |
| 6 | `pipelined_m:data_width=18,n_iter=18,angle_guard=0,frac_guard=1,rounding=trunc,m=6` | 1116 | 225 | 65.4 | 5 | 0.0504 | 0.000122 (2^-13.01) | 13.01 |
| 7 | `pipelined_m:data_width=23,n_iter=18,angle_guard=2,frac_guard=1,rounding=trunc,m=6` | 1420 | 287 | 62.5 | 5 | 0.0642 | 9.51e-06 (2^-16.68) | 16.68 |
| 8 | `pipelined_m:data_width=23,n_iter=22,angle_guard=3,frac_guard=1,rounding=round,m=3` | 1824 | 700 | 114.5 | 10 | 0.095 | 1.84e-06 (2^-19.05) | 19.05 |
| 9 | `pipelined_m:data_width=27,n_iter=22,angle_guard=3,frac_guard=1,rounding=round,m=3` | 2098 | 805 | 110.0 | 10 | 0.109 | 5.44e-07 (2^-20.81) | 20.81 |
| 10 | `pipelined_m:data_width=27,n_iter=22,angle_guard=3,frac_guard=4,rounding=round,m=3` | 2231 | 847 | 105.9 | 10 | 0.116 | 5.06e-07 (2^-20.92) | 20.92 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >=1 MSPS throughput and max_abs_err <= 2^-10, with area (luts_plus_ffs) as the primary objective. Both pipelined and pipelined_m deliver 1 result/cycle, so throughput = Fmax, which easily exceeds 1 MSPS for any reasonable Fmax. The key trade-off is area vs accuracy: data_width and n_iter control accuracy, while the pipeline structure (full vs every-m-stages) controls FF count. I split the budget 50/50 between the two families. For pipelined, the search explores the accuracy boundary at minimal width/iterations. For pipelined_m, the additional m parameter lets the optimizer find the sweet spot where FF savings outweigh any Fmax or latency penalty. Ranges are kept tight (data_width 12-16, n_iter 10-16) because the 2^-10 error spec is modest; wider data or more iterations would waste area without improving the objective. angle_guard and frac_guard are bounded small to keep area low while giving the optimizer room to find the minimal sufficient guard.*)
- `pipelined` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Full pipelining gives 1 result/cycle, so throughput = Fmax. To hit >=1 MSPS we need Fmax >= 1 MHz, which is trivially met; the real constraint is area. N+2 latency is fine for a control loop. I focus on the low-end of the accuracy/area trade-off: data_width 12-16 and n_iter 10-16 should bracket the max_abs_err <= 2^-10 boundary. angle_guard and frac_guard are kept small to minimise area while still allowing the optimizer to find the minimal guard that meets the error spec. This family has the most registers (one per stage), so it will likely be area-heavy, but it is the baseline for the 1-result/cycle requirement.
- `pipelined_m` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* pipelined_m registers every m stages, drastically cutting FF count versus full pipelining while still delivering 1 result/cycle. This is the primary area-optimization lever for this spec. With m=2..8, the optimizer can trade a small latency increase (ceil(N/m)+2 vs N+2) against large FF savings. The same data_width/n_iter/guard ranges apply since accuracy is identical across families. This family is most likely to produce the Pareto-optimal designs for min luts_plus_ffs under the throughput and accuracy constraints.

**Result (code):** 60 evaluations this round, 60 total; 36 feasible; hypervolume 895.6 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (pipelined_m, 826 LUTs+FFs) meets the throughput constraint (97.8 MSPS >= 1) and the accuracy constraint (max_abs_err 0.000976 <= 0.000976562). The front covers the trade-off space effectively, with area ranging from 826 to 1716 and accuracy from 10 to 12.3 bits. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (826) as per the selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 895.6 (gain this round: n/a (first round)).
Feasible designs: 36 of 60 evaluations (28 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 40% violate; best seen 0.000204 (2^-12.26)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=826, accuracy_bits=10, luts=638, ffs=189, throughput_msps=97.8, max_abs_err=0.000976 (2^-10.00), power_index=0.0311
- pipelined_m [data_width=16 n_iter=13 angle_guard=0 frac_guard=0 rounding=round m=8] luts_plus_ffs=831, accuracy_bits=11, luts=688, ffs=143, throughput_msps=52.7, max_abs_err=0.000492 (2^-10.99), power_index=0.0313
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1068, accuracy_bits=11.5, luts=800, ffs=268, throughput_msps=97.8, max_abs_err=0.000338 (2^-11.53), power_index=0.0402
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=1578, accuracy_bits=11.7, luts=772, ffs=805, throughput_msps=273, max_abs_err=0.000294 (2^-11.73), power_index=0.0593
- pipelined [data_width=16 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=1694, accuracy_bits=11.8, luts=831, ffs=863, throughput_msps=273, max_abs_err=0.000285 (2^-11.78), power_index=0.0637
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=1716, accuracy_bits=12.3, luts=861, ffs=856, throughput_msps=273, max_abs_err=0.000204 (2^-12.26), power_index=0.0646
Front coverage: luts_plus_ffs 826..1716 (HV reference 1500); accuracy_bits 10..12.3 (HV reference 10); data_width on the front 14..16 (registry 8..28).

Per family:
- pipelined: 30 evals, 21 feasible; max throughput seen 282 MSPS; best accuracy 12.26 bits; best feasible luts_plus_ffs=1321; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 30 evals, 15 feasible; max throughput seen 178 MSPS; best accuracy 11.53 bits; best feasible luts_plus_ffs=826; feasible ranges: data_width 14..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2, m 3..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (20 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (3 front designs; box front_anchored)
- `pipelined` (20 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 72 feasible; hypervolume 1270 (+41.8%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (pipelined_m, 826 LUTs+FFs) meets the throughput constraint (97.8 MSPS >= 1) and the accuracy constraint (max_abs_err 0.000976 <= 0.000976562). The front covers the trade-off space effectively, with area ranging from 826 to 1716 and accuracy from 10 to 12.3 bits. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (826) as per the selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1270 (gain this round: +41.8%).
Feasible designs: 72 of 100 evaluations (62 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 28% violate; best seen 5.06e-07 (2^-20.92)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=826, accuracy_bits=10, luts=638, ffs=189, throughput_msps=97.8, max_abs_err=0.000976 (2^-10.00), power_index=0.0311
- pipelined_m [data_width=16 n_iter=13 angle_guard=0 frac_guard=0 rounding=round m=8] luts_plus_ffs=831, accuracy_bits=11, luts=688, ffs=143, throughput_msps=52.7, max_abs_err=0.000492 (2^-10.99), power_index=0.0313
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=915, accuracy_bits=11.4, luts=764, ffs=151, throughput_msps=52.7, max_abs_err=0.000378 (2^-11.37), power_index=0.0344
- pipelined_m [data_width=17 n_iter=13 angle_guard=1 frac_guard=2 rounding=trunc m=6] luts_plus_ffs=1010, accuracy_bits=11.7, luts=789, ffs=221, throughput_msps=65.4, max_abs_err=0.000309 (2^-11.66), power_index=0.038
- pipelined_m [data_width=17 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc m=6] luts_plus_ffs=1026, accuracy_bits=11.7, luts=802, ffs=224, throughput_msps=65.4, max_abs_err=0.0003 (2^-11.70), power_index=0.0386
- pipelined_m [data_width=18 n_iter=18 angle_guard=0 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=1341, accuracy_bits=13, luts=1116, ffs=225, throughput_msps=65.4, max_abs_err=0.000122 (2^-13.01), power_index=0.0504
- pipelined_m [data_width=23 n_iter=18 angle_guard=2 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=1707, accuracy_bits=16.7, luts=1420, ffs=287, throughput_msps=62.5, max_abs_err=9.51e-06 (2^-16.68), power_index=0.0642
- pipelined_m [data_width=23 n_iter=22 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=2524, accuracy_bits=19, luts=1824, ffs=700, throughput_msps=114, max_abs_err=1.84e-06 (2^-19.05), power_index=0.095
- pipelined_m [data_width=27 n_iter=22 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=2903, accuracy_bits=20.8, luts=2098, ffs=805, throughput_msps=110, max_abs_err=5.44e-07 (2^-20.81), power_index=0.109
- pipelined_m [data_width=27 n_iter=22 angle_guard=3 frac_guard=4 rounding=round m=3] luts_plus_ffs=3078, accuracy_bits=20.9, luts=2231, ffs=847, throughput_msps=106, max_abs_err=5.06e-07 (2^-20.92), power_index=0.116
Front coverage: luts_plus_ffs 826..3078 (HV reference 1500); accuracy_bits 10..20.9 (HV reference 10); data_width on the front 14..27 (registry 8..28).

Per family:
- pipelined: 50 evals, 40 feasible; max throughput seen 282 MSPS; best accuracy 20.28 bits; best feasible luts_plus_ffs=1321; feasible ranges: data_width 15..23, n_iter 12..29, angle_guard 0..3, frac_guard 0..4
- pipelined_m: 50 evals, 32 feasible; max throughput seen 178 MSPS; best accuracy 20.92 bits; best feasible luts_plus_ffs=826; feasible ranges: data_width 13..27, n_iter 12..30, angle_guard -1..3, frac_guard 0..4, m 3..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4225 in, 1257 out
- provider-reported cost: $0.0033
- full prompts and replies: `llm_trace.jsonl`

