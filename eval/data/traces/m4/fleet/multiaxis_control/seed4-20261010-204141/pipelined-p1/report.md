# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec multiaxis_control: Shared sin/cos unit for a 16-axis motor-control loop: a 1 MHz control tick issues 32 requests at once (Park + inverse Park per axis); all 32 results must be back within 0.44 us of the tick (p99 over ticks). Max error <= 2^-12. Minimise LUTs + FFs.
  constraint: throughput_msps >= 32
  constraint: max_abs_err <= 0.000244141
  constraint: sys_p99_batch_us <= 0.44
  objective: min luts_plus_ffs (HV ref 4000)
  objective: max accuracy_bits (HV ref 12)
  select: min luts_plus_ffs
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average)
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=19,n_iter=16,angle_guard=-2,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 969 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 289 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.51 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00019 (2^-12.36) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 24.9 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 3.95e-05 (2^-14.63) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 5.17 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.4 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (14 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=16,angle_guard=-2,frac_guard=0,rounding=round,m=4` | 969 | 289 | 93.6 | 6 | 1.51 | 0.00019 (2^-12.36) | 12.36 |
| 1 | `pipelined_m:data_width=19,n_iter=14,angle_guard=-1,frac_guard=1,rounding=trunc,m=2` | 882 | 495 | 164.4 | 9 | 1.66 | 0.000179 (2^-12.45) | 12.45 |
| 2 | `pipelined_m:data_width=18,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=2` | 920 | 495 | 164.4 | 9 | 1.7 | 0.000152 (2^-12.68) | 12.68 |
| 3 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc,m=3` | 1017 | 428 | 119.3 | 8 | 1.74 | 8.82e-05 (2^-13.47) | 13.47 |
| 4 | `pipelined_m:data_width=25,n_iter=16,angle_guard=-2,frac_guard=0,rounding=round,m=4` | 1254 | 373 | 89.6 | 6 | 1.96 | 3.14e-05 (2^-14.96) | 14.96 |
| 5 | `pipelined_m:data_width=19,n_iter=17,angle_guard=3,frac_guard=3,rounding=round,m=3` | 1259 | 476 | 119.3 | 8 | 2.09 | 2.41e-05 (2^-15.34) | 15.34 |
| 6 | `pipelined_m:data_width=25,n_iter=17,angle_guard=3,frac_guard=0,rounding=round,m=3` | 1422 | 565 | 110.0 | 8 | 2.39 | 1.56e-05 (2^-15.97) | 15.97 |
| 7 | `pipelined_m:data_width=28,n_iter=17,angle_guard=3,frac_guard=3,rounding=round,m=3` | 1733 | 658 | 105.9 | 8 | 2.88 | 1.53e-05 (2^-16.00) | 16.00 |
| 8 | `pipelined_m:data_width=28,n_iter=19,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 1788 | 721 | 105.9 | 9 | 3.02 | 4.11e-06 (2^-17.89) | 17.89 |
| 9 | `pipelined_m:data_width=25,n_iter=27,angle_guard=-2,frac_guard=0,rounding=round,m=3` | 2170 | 777 | 114.5 | 11 | 3.55 | 3.54e-06 (2^-18.11) | 18.11 |
| 10 | `pipelined_m:data_width=28,n_iter=25,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 2383 | 913 | 105.9 | 11 | 3.97 | 5.4e-07 (2^-20.82) | 20.82 |
| 11 | `pipelined:data_width=27,n_iter=24,angle_guard=1,frac_guard=0,rounding=trunc` | 2138 | 2155 | 249.0 | 26 | 5.17 | 4.31e-07 (2^-21.14) | 21.14 |
| 12 | `pipelined:data_width=27,n_iter=24,angle_guard=4,frac_guard=0,rounding=round` | 2211 | 2228 | 242.0 | 26 | 5.34 | 2.65e-07 (2^-21.85) | 21.85 |
| 13 | `pipelined:data_width=28,n_iter=26,angle_guard=1,frac_guard=3,rounding=trunc` | 2561 | 2559 | 242.0 | 28 | 6.16 | 9.77e-08 (2^-23.29) | 23.29 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Only pipelined and pipelined_m are allowed. Both produce 1 result/cycle, so the 32 Msps throughput and 0.44 us batch deadline are met as long as Fmax stays above roughly 73 MHz (for 32 results in 0.44 us) and the pipeline latency plus 31 cycles fits in 0.44 us; at expected Fmax this is not restrictive. Accuracy requires max_abs_err <= 2^-12, so data_width must be at least about 14 and n_iter must be sufficient; the ranges include lower values to let the search locate the feasibility boundary. Area is dominated by data_width x n_iter and pipeline registers, so pipelined_m with larger m is the main lever for the min luts_plus_ffs objective. The budget split favours pipelined_m while keeping a solid baseline of fully pipelined designs.*)
- `pipelined` (21 evals): data_width=12..20, n_iter=8..22, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Baseline fully pipelined family: 1 result/cycle, highest Fmax, so it easily satisfies throughput >= 32 Msps and the 0.44 us batch deadline at typical clocks. It gives the reference area/accuracy trade-off against which pipelined_m must improve. Ranges cover the accuracy boundary (W=12..20, N=8..22) and small guard-bit variations that affect area and error.
- `pipelined_m` (39 evals): data_width=12..20, n_iter=8..22, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* Registering every m stages cuts flip-flop count relative to the fully pipelined family, which directly targets the min luts_plus_ffs objective. The m parameter trades area against Fmax and latency; larger m reduces FFs but may lower Fmax. We give it the larger share because it is the most likely source of Pareto-optimal area points. Ranges match pipelined for accuracy parameters and add m=2..8 to map the area/Fmax trade-off while keeping throughput and batch latency feasible.

**Result (code):** 60 evaluations this round, 60 total; 27 feasible; hypervolume 7105 (n/a).

**LLM decision:** `stop` — Final round (round cap reached). The front is feasible and well-formed, so `infeasible` does not apply: all three constraints are satisfiable — throughput_msps >= 32 has 0% violations (best 282, and even the cheapest front point delivers 164 MSPS), max_abs_err <= 2^-12 is met by every point on the front (best 2.32e-05), and sys_p99_batch_us <= 0.44 has 23% violations overall but is satisfied by the whole Pareto front (best 0.147). The front already spans the meaningful objective ranges: luts_plus_ffs 1334..2473 against the HV reference 4000, and accuracy_bits 12.3..15.4 against the reference 12, covering both objectives well past their reference points. The selection rule (min luts_plus_ffs) picks pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc m=2] at luts_plus_ffs=1334, accuracy_bits=12.3, max_abs_err=0.000205 <= 2^-12, throughput 164 MSPS >= 32, sys_p99_batch 0.147 <= 0.44 — feasible on all constraints. This cheapest point sits comfortably inside each constraint margin (accuracy ~8% below the limit, batch latency ~3x below the limit), so it is not a borderline L1-only pass likely to be culled at L2; the L2 re-selection has margin to fall back on the neighbouring front points (1377, 1415). Stopping, with the front left fitted for the spec's selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 7105 (gain this round: n/a (first round)).
Feasible designs: 27 of 60 evaluations (24 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 38% violate; best seen 2.32e-05 (2^-15.40)
- sys_p99_batch_us <= 0.44: 23% violate; best seen 0.147

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=1334, accuracy_bits=12.3, luts=855, ffs=479, throughput_msps=164, max_abs_err=0.000205 (2^-12.25), power_index=1.61
- pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=1377, accuracy_bits=12.4, luts=882, ffs=495, throughput_msps=164, max_abs_err=0.000179 (2^-12.45), power_index=1.66
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=2] luts_plus_ffs=1415, accuracy_bits=12.7, luts=920, ffs=495, throughput_msps=164, max_abs_err=0.000152 (2^-12.68), power_index=1.7
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1445, accuracy_bits=13.5, luts=1017, ffs=428, throughput_msps=119, max_abs_err=8.82e-05 (2^-13.47), power_index=1.74
- pipelined [data_width=19 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=2034, accuracy_bits=13.7, luts=1001, ffs=1033, throughput_msps=264, max_abs_err=7.72e-05 (2^-13.66), power_index=2.45
- pipelined [data_width=19 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2117, accuracy_bits=13.8, luts=1063, ffs=1053, throughput_msps=264, max_abs_err=7.18e-05 (2^-13.77), power_index=2.55
- pipelined_m [data_width=19 n_iter=22 angle_guard=0 frac_guard=1 rounding=round m=2] luts_plus_ffs=2254, accuracy_bits=14.1, luts=1484, ffs=771, throughput_msps=164, max_abs_err=5.55e-05 (2^-14.14), power_index=2.71
- pipelined_m [data_width=19 n_iter=22 angle_guard=2 frac_guard=1 rounding=round m=2] luts_plus_ffs=2321, accuracy_bits=15.2, luts=1528, ffs=793, throughput_msps=164, max_abs_err=2.75e-05 (2^-15.15), power_index=2.79
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=2473, accuracy_bits=15.4, luts=1244, ffs=1229, throughput_msps=264, max_abs_err=2.32e-05 (2^-15.40), power_index=2.98
Front coverage: luts_plus_ffs 1334..2473 (HV reference 4000); accuracy_bits 12.3..15.4 (HV reference 12); data_width on the front 18..20 (registry 8..28).

Per family:
- pipelined: 21 evals, 9 feasible; max throughput seen 282 MSPS; best accuracy 15.40 bits; best feasible luts_plus_ffs=1879; feasible ranges: data_width 18..20, n_iter 15..20, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 39 evals, 18 feasible; max throughput seen 171 MSPS; best accuracy 15.15 bits; best feasible luts_plus_ffs=1334; feasible ranges: data_width 18..19, n_iter 14..22, angle_guard -1..2, frac_guard 0..2, m 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (27 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (6 front designs; box front_anchored)
- `pipelined` (13 evals): data_width=18..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 58 feasible; hypervolume 1.451e+04 (+104.2%).

**No LLM call** (code's front-mapping round): Final round (round cap reached). The front is feasible and well-formed, so `infeasible` does not apply: all three constraints are satisfiable — throughput_msps >= 32 has 0% violations (best 282, and even the cheapest front point delivers 164 MSPS), max_abs_err <= 2^-12 is met by every point on the front (best 2.32e-05), and sys_p99_batch_us <= 0.44 has 23% violations overall but is satisfied by the whole Pareto front (best 0.147). The front already spans the meaningful objective ranges: luts_plus_ffs 1334..2473 against the HV reference 4000, and accuracy_bits 12.3..15.4 against the reference 12, covering both objectives well past their reference points. The selection rule (min luts_plus_ffs) picks pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc m=2] at luts_plus_ffs=1334, accuracy_bits=12.3, max_abs_err=0.000205 <= 2^-12, throughput 164 MSPS >= 32, sys_p99_batch 0.147 <= 0.44 — feasible on all constraints. This cheapest point sits comfortably inside each constraint margin (accuracy ~8% below the limit, batch latency ~3x below the limit), so it is not a borderline L1-only pass likely to be culled at L2; the L2 re-selection has margin to fall back on the neighbouring front points (1377, 1415). Stopping, with the front left fitted for the spec's selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.451e+04 (gain this round: +104.2%).
Feasible designs: 58 of 100 evaluations (52 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 26% violate; best seen 9.77e-08 (2^-23.29)
- sys_p99_batch_us <= 0.44: 20% violate; best seen 0.147

Pareto front (feasible, 14 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=16 angle_guard=-2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1258, accuracy_bits=12.4, luts=969, ffs=289, throughput_msps=93.6, max_abs_err=0.00019 (2^-12.36), power_index=1.51
- pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=1377, accuracy_bits=12.4, luts=882, ffs=495, throughput_msps=164, max_abs_err=0.000179 (2^-12.45), power_index=1.66
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1445, accuracy_bits=13.5, luts=1017, ffs=428, throughput_msps=119, max_abs_err=8.82e-05 (2^-13.47), power_index=1.74
- pipelined_m [data_width=25 n_iter=16 angle_guard=-2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1627, accuracy_bits=15, luts=1254, ffs=373, throughput_msps=89.6, max_abs_err=3.14e-05 (2^-14.96), power_index=1.96
- pipelined_m [data_width=25 n_iter=17 angle_guard=3 frac_guard=0 rounding=round m=3] luts_plus_ffs=1987, accuracy_bits=16, luts=1422, ffs=565, throughput_msps=110, max_abs_err=1.56e-05 (2^-15.97), power_index=2.39
- pipelined_m [data_width=28 n_iter=17 angle_guard=3 frac_guard=3 rounding=round m=3] luts_plus_ffs=2391, accuracy_bits=16, luts=1733, ffs=658, throughput_msps=106, max_abs_err=1.53e-05 (2^-16.00), power_index=2.88
- pipelined_m [data_width=25 n_iter=27 angle_guard=-2 frac_guard=0 rounding=round m=3] luts_plus_ffs=2947, accuracy_bits=18.1, luts=2170, ffs=777, throughput_msps=114, max_abs_err=3.54e-06 (2^-18.11), power_index=3.55
- pipelined_m [data_width=28 n_iter=25 angle_guard=-2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3296, accuracy_bits=20.8, luts=2383, ffs=913, throughput_msps=106, max_abs_err=5.4e-07 (2^-20.82), power_index=3.97
- pipelined [data_width=27 n_iter=24 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=4438, accuracy_bits=21.8, luts=2211, ffs=2228, throughput_msps=242, max_abs_err=2.65e-07 (2^-21.85), power_index=5.34
- pipelined [data_width=28 n_iter=26 angle_guard=1 frac_guard=3 rounding=trunc] luts_plus_ffs=5119, accuracy_bits=23.3, luts=2561, ffs=2559, throughput_msps=242, max_abs_err=9.77e-08 (2^-23.29), power_index=6.16
Front coverage: luts_plus_ffs 1258..5119 (HV reference 4000); accuracy_bits 12.4..23.3 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- pipelined: 34 evals, 20 feasible; max throughput seen 282 MSPS; best accuracy 23.29 bits; best feasible luts_plus_ffs=1879; feasible ranges: data_width 18..28, n_iter 13..28, angle_guard -1..4, frac_guard 0..3
- pipelined_m: 66 evals, 38 feasible; max throughput seen 171 MSPS; best accuracy 20.82 bits; best feasible luts_plus_ffs=1258; feasible ranges: data_width 18..28, n_iter 13..27, angle_guard -2..3, frac_guard 0..3, m 2..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5401 in, 3247 out
- provider-reported cost: $0.0042
- full prompts and replies: `llm_trace.jsonl`

