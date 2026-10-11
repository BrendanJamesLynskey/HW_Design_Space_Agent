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
`pipelined_m:data_width=15,n_iter=16,angle_guard=0,frac_guard=1,rounding=round,m=6` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 875 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 194 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 68.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 68.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 73 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0402 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000744 (2^-10.39) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.1 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000181 (2^-12.43) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.48 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.4 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (17 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=16,angle_guard=0,frac_guard=1,rounding=round,m=6` | 875 | 194 | 68.5 | 5 | 0.0402 | 0.000744 (2^-10.39) | 10.39 |
| 1 | `pipelined_m:data_width=14,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=3` | 775 | 304 | 124.5 | 7 | 0.0406 | 0.000513 (2^-10.93) | 10.93 |
| 2 | `pipelined_m:data_width=19,n_iter=12,angle_guard=2,frac_guard=3,rounding=trunc,m=5` | 828 | 250 | 77.0 | 5 | 0.0406 | 0.000497 (2^-10.97) | 10.97 |
| 3 | `pipelined_m:data_width=17,n_iter=14,angle_guard=0,frac_guard=2,rounding=round,m=6` | 877 | 220 | 65.4 | 5 | 0.0413 | 0.00025 (2^-11.97) | 11.97 |
| 4 | `pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=6` | 904 | 226 | 65.4 | 5 | 0.0425 | 0.000169 (2^-12.53) | 12.53 |
| 5 | `pipelined_m:data_width=19,n_iter=15,angle_guard=3,frac_guard=0,rounding=trunc,m=6` | 979 | 241 | 65.4 | 5 | 0.0459 | 0.000109 (2^-13.17) | 13.17 |
| 6 | `pipelined_m:data_width=19,n_iter=17,angle_guard=2,frac_guard=0,rounding=trunc,m=8` | 1101 | 238 | 50.3 | 5 | 0.0504 | 7.8e-05 (2^-13.65) | 13.65 |
| 7 | `pipelined_m:data_width=19,n_iter=17,angle_guard=2,frac_guard=3,rounding=trunc,m=8` | 1202 | 250 | 50.3 | 5 | 0.0546 | 3.2e-05 (2^-14.93) | 14.93 |
| 8 | `pipelined_m:data_width=19,n_iter=17,angle_guard=3,frac_guard=3,rounding=trunc,m=5` | 1219 | 327 | 77.0 | 6 | 0.0582 | 3.09e-05 (2^-14.98) | 14.98 |
| 9 | `pipelined_m:data_width=24,n_iter=17,angle_guard=2,frac_guard=0,rounding=trunc,m=8` | 1354 | 294 | 48.0 | 5 | 0.062 | 1.65e-05 (2^-15.88) | 15.88 |
| 10 | `pipelined_m:data_width=23,n_iter=21,angle_guard=-2,frac_guard=0,rounding=trunc,m=8` | 1544 | 270 | 48.0 | 5 | 0.0682 | 1.44e-05 (2^-16.08) | 16.08 |
| 11 | `pipelined_m:data_width=23,n_iter=21,angle_guard=2,frac_guard=0,rounding=trunc,m=5` | 1628 | 440 | 73.7 | 7 | 0.0778 | 5.84e-06 (2^-17.39) | 17.39 |
| 12 | `pipelined_m:data_width=24,n_iter=19,angle_guard=2,frac_guard=3,rounding=round,m=4` | 1687 | 483 | 86.0 | 7 | 0.0816 | 4.16e-06 (2^-17.88) | 17.88 |
| 13 | `pipelined_m:data_width=26,n_iter=23,angle_guard=2,frac_guard=0,rounding=round,m=8` | 1999 | 316 | 45.9 | 5 | 0.0871 | 4.56e-07 (2^-21.06) | 21.06 |
| 14 | `pipelined_m:data_width=24,n_iter=24,angle_guard=4,frac_guard=3,rounding=round,m=4` | 2189 | 583 | 86.0 | 8 | 0.104 | 3.93e-07 (2^-21.28) | 21.28 |
| 15 | `pipelined_m:data_width=26,n_iter=23,angle_guard=2,frac_guard=3,rounding=round,m=2` | 2193 | 1174 | 152.6 | 14 | 0.127 | 3.37e-07 (2^-21.50) | 21.50 |
| 16 | `pipelined_m:data_width=26,n_iter=23,angle_guard=3,frac_guard=3,rounding=round,m=2` | 2216 | 1186 | 152.6 | 14 | 0.128 | 3.04e-07 (2^-21.65) | 21.65 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraint is max_abs_err <= 2^-10, while throughput >= 1 MSPS is trivial for any 1-result/cycle architecture on Artix-7. Therefore the search should focus on the area-accuracy trade-off. Accuracy depends only on data_width, n_iter, angle_guard, frac_guard and rounding, so both families are given the same accuracy ranges. data_width starts at 11 because the output LSB is 2^-(W-2); W=11 gives 0.5 LSB = 2^-10, the exact error limit, so W=12+ is likely needed but W=11 is kept to test the boundary. n_iter 8..20 covers the CORDIC angle-approximation error, with the lower end probing the minimum feasible iteration count. angle_guard -2..2 and frac_guard 0..3 focus on small guard widths that minimise area while still allowing enough internal precision. Both rounding modes are included because rounding can improve accuracy at no area cost. pipelined_m receives 70% of the budget because its m parameter gives a direct area/Fmax knob and it is expected to dominate the Pareto front; pipelined receives 30% as a reference and fallback. The ranges are deliberately wide enough to map the front but narrow enough to spend most evaluations near the feasible area-optimal region.*)
- `pipelined_m` (42 evals): data_width=11..18, n_iter=8..20, angle_guard=-2..2, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* pipelined_m is the most promising family for the area objective: it keeps 1 result/cycle but registers only every m stages, so increasing m directly reduces FF count. The spec's throughput constraint is only 1 MSPS, which is far below the Fmax of any plausible Artix-7 CORDIC stage, so trading Fmax for area via larger m should be beneficial. The m range 2..8 spans the area/Fmax trade-off; m=2 is close to fully pipelined, m=8 minimises registers. The accuracy parameters are searched over the same subspace as pipelined so that equal-accuracy points can be compared directly.
- `pipelined` (18 evals): data_width=11..18, n_iter=8..20, angle_guard=-2..2, frac_guard=0..3, rounding=trunc|round. *Why:* pipelined is the fully registered reference for the 1-result/cycle class. It will have the highest Fmax but also the highest FF count, so it is unlikely to win on luts_plus_ffs. It is included to (a) provide a baseline on the accuracy-area front, (b) cover cases where pipelined_m with large m might fail the 1 MSPS throughput constraint, and (c) confirm whether any accuracy level is reachable only with full pipelining. The accuracy parameter ranges match pipelined_m so that the two families can be compared at identical accuracy settings.

**Result (code):** 60 evaluations this round, 60 total; 32 feasible; hypervolume 1143 (n/a).

**LLM decision:** `stop` — Final round reached, and the spec is feasible: 32/60 evaluations were feasible and the reported Pareto front contains 5 feasible designs. Both constraints are met on the front: throughput_msps is at least 65.4 (constraint >= 1) and max_abs_err is at most 0.000744 (2^-10.39), which satisfies <= 0.000976562. The area objective is already below the HV reference: best feasible luts_plus_ffs=1068 vs HV ref 1500, with the front covering luts_plus_ffs 1068..1308 and accuracy_bits 10.4..13.2 (HV ref 10). The spec's selection rule min luts_plus_ffs would pick the pipelined_m design [data_width=15, n_iter=16, angle_guard=0, frac_guard=1, rounding=round, m=6] at luts_plus_ffs=1068, accuracy_bits=10.4, max_abs_err=0.000744, throughput_msps=68.5. Since the final round is here and no constraint is unreachable, the correct decision is stop.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1143 (gain this round: n/a (first round)).
Feasible designs: 32 of 60 evaluations (28 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 47% violate; best seen 0.000109 (2^-13.16)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=16 angle_guard=0 frac_guard=1 rounding=round m=6] luts_plus_ffs=1068, accuracy_bits=10.4, luts=875, ffs=194, throughput_msps=68.5, max_abs_err=0.000744 (2^-10.39), power_index=0.0402
- pipelined_m [data_width=14 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=3] luts_plus_ffs=1078, accuracy_bits=10.9, luts=775, ffs=304, throughput_msps=124, max_abs_err=0.000513 (2^-10.93), power_index=0.0406
- pipelined_m [data_width=17 n_iter=14 angle_guard=0 frac_guard=2 rounding=round m=6] luts_plus_ffs=1097, accuracy_bits=12, luts=877, ffs=220, throughput_msps=65.4, max_abs_err=0.00025 (2^-11.97), power_index=0.0413
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=6] luts_plus_ffs=1130, accuracy_bits=12.5, luts=904, ffs=226, throughput_msps=65.4, max_abs_err=0.000169 (2^-12.53), power_index=0.0425
- pipelined_m [data_width=17 n_iter=16 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1308, accuracy_bits=13.2, luts=1021, ffs=287, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.16), power_index=0.0492
Front coverage: luts_plus_ffs 1068..1308 (HV reference 1500); accuracy_bits 10.4..13.2 (HV reference 10); data_width on the front 14..17 (registry 8..28).

Per family:
- pipelined: 18 evals, 8 feasible; max throughput seen 282 MSPS; best accuracy 12.38 bits; best feasible luts_plus_ffs=1876; feasible ranges: data_width 17..17, n_iter 16..17, angle_guard -2..0, frac_guard 1..3
- pipelined_m: 42 evals, 24 feasible; max throughput seen 178 MSPS; best accuracy 13.16 bits; best feasible luts_plus_ffs=1068; feasible ranges: data_width 14..17, n_iter 14..19, angle_guard -2..2, frac_guard 0..3, m 2..6
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=13..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (5 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 68 feasible; hypervolume 1340 (+17.2%).

**No LLM call** (code's front-mapping round): Final round reached, and the spec is feasible: 32/60 evaluations were feasible and the reported Pareto front contains 5 feasible designs. Both constraints are met on the front: throughput_msps is at least 65.4 (constraint >= 1) and max_abs_err is at most 0.000744 (2^-10.39), which satisfies <= 0.000976562. The area objective is already below the HV reference: best feasible luts_plus_ffs=1068 vs HV ref 1500, with the front covering luts_plus_ffs 1068..1308 and accuracy_bits 10.4..13.2 (HV ref 10). The spec's selection rule min luts_plus_ffs would pick the pipelined_m design [data_width=15, n_iter=16, angle_guard=0, frac_guard=1, rounding=round, m=6] at luts_plus_ffs=1068, accuracy_bits=10.4, max_abs_err=0.000744, throughput_msps=68.5. Since the final round is here and no constraint is unreachable, the correct decision is stop.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1340 (gain this round: +17.2%).
Feasible designs: 68 of 100 evaluations (61 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 32% violate; best seen 3.04e-07 (2^-21.65)

Pareto front (feasible, 17 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=16 angle_guard=0 frac_guard=1 rounding=round m=6] luts_plus_ffs=1068, accuracy_bits=10.4, luts=875, ffs=194, throughput_msps=68.5, max_abs_err=0.000744 (2^-10.39), power_index=0.0402
- pipelined_m [data_width=19 n_iter=12 angle_guard=2 frac_guard=3 rounding=trunc m=5] luts_plus_ffs=1078, accuracy_bits=11, luts=828, ffs=250, throughput_msps=77, max_abs_err=0.000497 (2^-10.97), power_index=0.0406
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=6] luts_plus_ffs=1130, accuracy_bits=12.5, luts=904, ffs=226, throughput_msps=65.4, max_abs_err=0.000169 (2^-12.53), power_index=0.0425
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1220, accuracy_bits=13.2, luts=979, ffs=241, throughput_msps=65.4, max_abs_err=0.000109 (2^-13.17), power_index=0.0459
- pipelined_m [data_width=19 n_iter=17 angle_guard=2 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1453, accuracy_bits=14.9, luts=1202, ffs=250, throughput_msps=50.3, max_abs_err=3.2e-05 (2^-14.93), power_index=0.0546
- pipelined_m [data_width=24 n_iter=17 angle_guard=2 frac_guard=0 rounding=trunc m=8] luts_plus_ffs=1648, accuracy_bits=15.9, luts=1354, ffs=294, throughput_msps=48, max_abs_err=1.65e-05 (2^-15.88), power_index=0.062
- pipelined_m [data_width=23 n_iter=21 angle_guard=2 frac_guard=0 rounding=trunc m=5] luts_plus_ffs=2068, accuracy_bits=17.4, luts=1628, ffs=440, throughput_msps=73.7, max_abs_err=5.84e-06 (2^-17.39), power_index=0.0778
- pipelined_m [data_width=24 n_iter=19 angle_guard=2 frac_guard=3 rounding=round m=4] luts_plus_ffs=2170, accuracy_bits=17.9, luts=1687, ffs=483, throughput_msps=86, max_abs_err=4.16e-06 (2^-17.88), power_index=0.0816
- pipelined_m [data_width=24 n_iter=24 angle_guard=4 frac_guard=3 rounding=round m=4] luts_plus_ffs=2772, accuracy_bits=21.3, luts=2189, ffs=583, throughput_msps=86, max_abs_err=3.93e-07 (2^-21.28), power_index=0.104
- pipelined_m [data_width=26 n_iter=23 angle_guard=3 frac_guard=3 rounding=round m=2] luts_plus_ffs=3403, accuracy_bits=21.6, luts=2216, ffs=1186, throughput_msps=153, max_abs_err=3.04e-07 (2^-21.65), power_index=0.128
Front coverage: luts_plus_ffs 1068..3403 (HV reference 1500); accuracy_bits 10.4..21.6 (HV reference 10); data_width on the front 14..26 (registry 8..28).

Per family:
- pipelined: 18 evals, 8 feasible; max throughput seen 282 MSPS; best accuracy 12.38 bits; best feasible luts_plus_ffs=1876; feasible ranges: data_width 17..17, n_iter 16..17, angle_guard -2..0, frac_guard 1..3
- pipelined_m: 82 evals, 60 feasible; max throughput seen 178 MSPS; best accuracy 21.65 bits; best feasible luts_plus_ffs=1068; feasible ranges: data_width 14..26, n_iter 12..24, angle_guard -2..4, frac_guard 0..3, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4016 in, 4368 out
- provider-reported cost: $0.0054
- full prompts and replies: `llm_trace.jsonl`

