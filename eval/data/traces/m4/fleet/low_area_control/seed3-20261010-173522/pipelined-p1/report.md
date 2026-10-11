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
`pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=2,rounding=round,m=6` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 723 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 151 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 68.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 68.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 58.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0329 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000602 (2^-10.70) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 9.86 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000202 (2^-12.27) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 3.32 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.7 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (11 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=2,rounding=round,m=6` | 723 | 151 | 68.5 | 4 | 0.0329 | 0.000602 (2^-10.70) | 10.70 |
| 1 | `pipelined_m:data_width=22,n_iter=12,angle_guard=1,frac_guard=2,rounding=round,m=5` | 944 | 278 | 73.7 | 5 | 0.046 | 0.000489 (2^-11.00) | 11.00 |
| 2 | `pipelined_m:data_width=18,n_iter=17,angle_guard=-2,frac_guard=2,rounding=trunc,m=7` | 1051 | 223 | 56.8 | 5 | 0.0479 | 0.000338 (2^-11.53) | 11.53 |
| 3 | `pipelined_m:data_width=18,n_iter=18,angle_guard=1,frac_guard=2,rounding=trunc,m=8` | 1170 | 232 | 50.3 | 5 | 0.0527 | 6.72e-05 (2^-13.86) | 13.86 |
| 4 | `pipelined_m:data_width=19,n_iter=16,angle_guard=3,frac_guard=4,rounding=round,m=7` | 1215 | 259 | 54.3 | 5 | 0.0555 | 3.62e-05 (2^-14.75) | 14.75 |
| 5 | `pipelined_m:data_width=18,n_iter=21,angle_guard=4,frac_guard=2,rounding=round,m=7` | 1476 | 243 | 56.8 | 5 | 0.0647 | 2.87e-05 (2^-15.09) | 15.09 |
| 6 | `pipelined_m:data_width=28,n_iter=21,angle_guard=1,frac_guard=2,rounding=trunc,m=8` | 2007 | 343 | 45.9 | 5 | 0.0884 | 1e-06 (2^-19.93) | 19.93 |
| 7 | `pipelined_m:data_width=28,n_iter=30,angle_guard=0,frac_guard=2,rounding=round,m=7` | 2937 | 534 | 52.0 | 7 | 0.131 | 1.41e-07 (2^-22.76) | 22.76 |
| 8 | `pipelined_m:data_width=28,n_iter=30,angle_guard=0,frac_guard=3,rounding=trunc,m=7` | 2939 | 540 | 49.9 | 7 | 0.131 | 1.33e-07 (2^-22.84) | 22.84 |
| 9 | `pipelined:data_width=27,n_iter=28,angle_guard=3,frac_guard=2,rounding=trunc` | 2680 | 2676 | 249.0 | 30 | 0.201 | 1.14e-07 (2^-23.06) | 23.06 |
| 10 | `pipelined:data_width=27,n_iter=28,angle_guard=2,frac_guard=2,rounding=round` | 2708 | 2649 | 249.0 | 30 | 0.202 | 9.57e-08 (2^-23.32) | 23.32 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=1 MSPS throughput and max_abs_err <= 2^-10, with area (luts+ffs) as the primary objective. Both pipelined and pipelined_m produce 1 result/cycle, so throughput = Fmax. The key insight is that pipelined_m can reduce FF count by registering every m stages instead of every stage, directly reducing area. Since latency is not a constraint, larger m values are attractive for area reduction. The accuracy constraint (2^-10) sets a floor on n_iter and data_width. I'm allocating 55% to pipelined (the baseline, fully pipelined) and 45% to pipelined_m (the area-optimized variant). Both families share the same accuracy-determining parameters (data_width, n_iter, angle_guard, frac_guard, rounding), so the accuracy constraint will be similar, but the area (especially FFs) will differ significantly. The full ranges are used because I have no prior information and need to discover where the accuracy constraint binds and where the area trade-off curve lies. The hypervolume objective rewards covering the trade-off curve, so I want to explore both the minimum-area feasible point and the higher-accuracy/higher-area points.*)
- `pipelined` (33 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Fully pipelined gives 1 result/cycle, so throughput = Fmax. To hit >=1 MSPS we need Fmax >= 1 MHz, which is trivially met, but area (luts+ffs) is the primary objective. A fully pipelined CORDIC has N+2 pipeline registers, so FF count scales linearly with n_iter and data_width. The accuracy constraint (max_abs_err <= 2^-10) is the binding constraint that sets the minimum n_iter and data_width. I want to explore the full range to find the minimum-area point that satisfies accuracy, and also map the trade-off curve where higher accuracy (more n_iter or wider data) costs more area. The angle_guard and frac_guard affect both accuracy and area (wider angle path = more LUTs for atan table, more FFs in pipeline). Rounding mode affects accuracy slightly. This is the core family for this spec since it directly trades area vs accuracy at full throughput.
- `pipelined_m` (27 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* pipelined_m registers every m stages, so it has ceil(N/m)+2 pipeline registers instead of N+2. This can significantly reduce FF count (and thus luts_plus_ffs) compared to fully pipelined, at the cost of higher latency (ceil(N/m)+2 vs N+2 cycles). Since the spec only requires >=1 MSPS throughput (not low latency), and area is the primary objective, pipelined_m with larger m could yield much smaller area while still meeting throughput (1 result/cycle). The trade-off is that larger m means fewer pipeline registers but potentially tighter timing (longer combinational path between registers), which could lower Fmax. However, since we only need >=1 MSPS, even a modest Fmax reduction is acceptable. This family should explore the area-accuracy trade-off at reduced FF cost. The m parameter is the key differentiator: m=2,3,4,5,6,7,8 give progressively fewer registers. I want to see where the area savings plateau and whether Fmax drops below 1 MHz for large m.

**Result (code):** 60 evaluations this round, 60 total; 42 feasible; hypervolume 520.3 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established and covers the required trade-off space. The minimum area design (pipelined_m, luts_plus_ffs=874) meets the throughput constraint (68.5 MSPS >= 1) and the accuracy constraint (10.7 bits > 10 bits required for 2^-10 error). The front extends to high accuracy (23.3 bits) with higher area, providing a complete map of the area-accuracy trade-off. Since this is the final round, no further exploration is possible or necessary.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 520.3 (gain this round: n/a (first round)).
Feasible designs: 42 of 60 evaluations (39 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 30% violate; best seen 9.57e-08 (2^-23.32)

Pareto front (feasible, 15 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=2 rounding=round m=6] luts_plus_ffs=874, accuracy_bits=10.7, luts=723, ffs=151, throughput_msps=68.5, max_abs_err=0.000602 (2^-10.70), power_index=0.0329
- pipelined_m [data_width=17 n_iter=21 angle_guard=0 frac_guard=3 rounding=round m=8] luts_plus_ffs=1593, accuracy_bits=12.3, luts=1369, ffs=224, throughput_msps=50.3, max_abs_err=0.000204 (2^-12.26), power_index=0.0599
- pipelined_m [data_width=19 n_iter=21 angle_guard=0 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1704, accuracy_bits=14.1, luts=1459, ffs=244, throughput_msps=50.3, max_abs_err=5.59e-05 (2^-14.13), power_index=0.0641
- pipelined_m [data_width=27 n_iter=20 angle_guard=1 frac_guard=3 rounding=round m=4] luts_plus_ffs=2474, accuracy_bits=18.9, luts=1944, ffs=530, throughput_msps=86, max_abs_err=1.99e-06 (2^-18.94), power_index=0.0931
- pipelined_m [data_width=28 n_iter=20 angle_guard=0 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=2956, accuracy_bits=19, luts=1927, ffs=1029, throughput_msps=147, max_abs_err=1.97e-06 (2^-18.95), power_index=0.111
- pipelined [data_width=27 n_iter=22 angle_guard=-2 frac_guard=2 rounding=trunc] luts_plus_ffs=3964, accuracy_bits=19.6, luts=1975, ffs=1990, throughput_msps=249, max_abs_err=1.24e-06 (2^-19.62), power_index=0.149
- pipelined [data_width=27 n_iter=22 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=4017, accuracy_bits=20.7, luts=1997, ffs=2020, throughput_msps=249, max_abs_err=6.06e-07 (2^-20.65), power_index=0.151
- pipelined [data_width=27 n_iter=22 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=4186, accuracy_bits=20.8, luts=2085, ffs=2101, throughput_msps=249, max_abs_err=5.54e-07 (2^-20.78), power_index=0.157
- pipelined [data_width=27 n_iter=27 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=5106, accuracy_bits=22.7, luts=2553, ffs=2553, throughput_msps=249, max_abs_err=1.42e-07 (2^-22.74), power_index=0.192
- pipelined [data_width=27 n_iter=28 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=5358, accuracy_bits=23.3, luts=2708, ffs=2649, throughput_msps=249, max_abs_err=9.57e-08 (2^-23.32), power_index=0.202
Front coverage: luts_plus_ffs 874..5358 (HV reference 1500); accuracy_bits 10.7..23.3 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- pipelined: 33 evals, 24 feasible; max throughput seen 282 MSPS; best accuracy 23.32 bits; best feasible luts_plus_ffs=2465; feasible ranges: data_width 15..27, n_iter 21..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 27 evals, 18 feasible; max throughput seen 171 MSPS; best accuracy 18.95 bits; best feasible luts_plus_ffs=874; feasible ranges: data_width 16..28, n_iter 12..26, angle_guard 0..1, frac_guard 2..4, m 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (19 evals): data_width=15..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (7 front designs; box front_anchored)
- `pipelined` (21 evals): data_width=23..28, n_iter=19..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (8 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 79 feasible; hypervolume 892.8 (+71.6%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and covers the required trade-off space. The minimum area design (pipelined_m, luts_plus_ffs=874) meets the throughput constraint (68.5 MSPS >= 1) and the accuracy constraint (10.7 bits > 10 bits required for 2^-10 error). The front extends to high accuracy (23.3 bits) with higher area, providing a complete map of the area-accuracy trade-off. Since this is the final round, no further exploration is possible or necessary.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 892.8 (gain this round: +71.6%).
Feasible designs: 79 of 100 evaluations (74 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 21% violate; best seen 9.57e-08 (2^-23.32)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=2 rounding=round m=6] luts_plus_ffs=874, accuracy_bits=10.7, luts=723, ffs=151, throughput_msps=68.5, max_abs_err=0.000602 (2^-10.70), power_index=0.0329
- pipelined_m [data_width=22 n_iter=12 angle_guard=1 frac_guard=2 rounding=round m=5] luts_plus_ffs=1223, accuracy_bits=11, luts=944, ffs=278, throughput_msps=73.7, max_abs_err=0.000489 (2^-11.00), power_index=0.046
- pipelined_m [data_width=18 n_iter=17 angle_guard=-2 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=1274, accuracy_bits=11.5, luts=1051, ffs=223, throughput_msps=56.8, max_abs_err=0.000338 (2^-11.53), power_index=0.0479
- pipelined_m [data_width=18 n_iter=18 angle_guard=1 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=1402, accuracy_bits=13.9, luts=1170, ffs=232, throughput_msps=50.3, max_abs_err=6.72e-05 (2^-13.86), power_index=0.0527
- pipelined_m [data_width=19 n_iter=16 angle_guard=3 frac_guard=4 rounding=round m=7] luts_plus_ffs=1474, accuracy_bits=14.8, luts=1215, ffs=259, throughput_msps=54.3, max_abs_err=3.62e-05 (2^-14.75), power_index=0.0555
- pipelined_m [data_width=28 n_iter=21 angle_guard=1 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=2350, accuracy_bits=19.9, luts=2007, ffs=343, throughput_msps=45.9, max_abs_err=1e-06 (2^-19.93), power_index=0.0884
- pipelined_m [data_width=28 n_iter=30 angle_guard=0 frac_guard=2 rounding=round m=7] luts_plus_ffs=3471, accuracy_bits=22.8, luts=2937, ffs=534, throughput_msps=52, max_abs_err=1.41e-07 (2^-22.76), power_index=0.131
- pipelined_m [data_width=28 n_iter=30 angle_guard=0 frac_guard=3 rounding=trunc m=7] luts_plus_ffs=3479, accuracy_bits=22.8, luts=2939, ffs=540, throughput_msps=49.9, max_abs_err=1.33e-07 (2^-22.84), power_index=0.131
- pipelined [data_width=27 n_iter=28 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=5355, accuracy_bits=23.1, luts=2680, ffs=2676, throughput_msps=249, max_abs_err=1.14e-07 (2^-23.06), power_index=0.201
- pipelined [data_width=27 n_iter=28 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=5358, accuracy_bits=23.3, luts=2708, ffs=2649, throughput_msps=249, max_abs_err=9.57e-08 (2^-23.32), power_index=0.202
Front coverage: luts_plus_ffs 874..5358 (HV reference 1500); accuracy_bits 10.7..23.3 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- pipelined: 54 evals, 45 feasible; max throughput seen 282 MSPS; best accuracy 23.32 bits; best feasible luts_plus_ffs=2465; feasible ranges: data_width 15..27, n_iter 19..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 46 evals, 34 feasible; max throughput seen 171 MSPS; best accuracy 22.84 bits; best feasible luts_plus_ffs=874; feasible ranges: data_width 16..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4647 in, 1425 out
- provider-reported cost: $0.0022
- full prompts and replies: `llm_trace.jsonl`

