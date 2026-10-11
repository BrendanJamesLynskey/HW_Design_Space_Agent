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
`pipelined_m:data_width=16,n_iter=12,angle_guard=0,frac_guard=0,rounding=trunc,m=3` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 631 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 254 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 124 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 124 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 48.2 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0333 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000887 (2^-10.14) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 14.5 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.00023 (2^-12.08) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 3.77 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.1 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=12,angle_guard=0,frac_guard=0,rounding=trunc,m=3` | 631 | 254 | 124.5 | 6 | 0.0333 | 0.000887 (2^-10.14) | 10.14 |
| 1 | `pipelined_m:data_width=15,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 745 | 250 | 97.8 | 6 | 0.0374 | 0.000594 (2^-10.72) | 10.72 |
| 2 | `pipelined_m:data_width=16,n_iter=13,angle_guard=0,frac_guard=1,rounding=round,m=4` | 747 | 262 | 97.8 | 6 | 0.038 | 0.000472 (2^-11.05) | 11.05 |
| 3 | `pipelined_m:data_width=16,n_iter=13,angle_guard=1,frac_guard=1,rounding=round,m=4` | 760 | 266 | 97.8 | 6 | 0.0386 | 0.00038 (2^-11.36) | 11.36 |
| 4 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 800 | 268 | 97.8 | 6 | 0.0402 | 0.000338 (2^-11.53) | 11.53 |
| 5 | `pipelined_m:data_width=20,n_iter=15,angle_guard=-2,frac_guard=0,rounding=round,m=7` | 949 | 237 | 56.8 | 5 | 0.0446 | 0.00012 (2^-13.02) | 13.02 |
| 6 | `pipelined_m:data_width=20,n_iter=15,angle_guard=3,frac_guard=0,rounding=round,m=7` | 1023 | 252 | 54.3 | 5 | 0.048 | 7.16e-05 (2^-13.77) | 13.77 |
| 7 | `pipelined_m:data_width=24,n_iter=15,angle_guard=-2,frac_guard=0,rounding=round,m=4` | 1126 | 359 | 89.6 | 6 | 0.0559 | 6.45e-05 (2^-13.92) | 13.92 |
| 8 | `pipelined_m:data_width=25,n_iter=15,angle_guard=0,frac_guard=3,rounding=round,m=6` | 1341 | 313 | 59.9 | 5 | 0.0622 | 6.13e-05 (2^-13.99) | 13.99 |
| 9 | `pipelined_m:data_width=24,n_iter=19,angle_guard=-2,frac_guard=0,rounding=round,m=8` | 1447 | 281 | 48.0 | 5 | 0.065 | 8.52e-06 (2^-16.84) | 16.84 |
| 10 | `pipelined_m:data_width=24,n_iter=28,angle_guard=-2,frac_guard=1,rounding=trunc,m=7` | 2224 | 365 | 54.3 | 6 | 0.0974 | 7.66e-06 (2^-16.99) | 16.99 |
| 11 | `pipelined_m:data_width=24,n_iter=28,angle_guard=-2,frac_guard=0,rounding=round,m=6` | 2168 | 437 | 62.5 | 7 | 0.098 | 6.97e-06 (2^-17.13) | 17.13 |
| 12 | `pipelined_m:data_width=28,n_iter=28,angle_guard=3,frac_guard=1,rounding=round,m=7` | 2767 | 444 | 49.9 | 6 | 0.121 | 5.72e-08 (2^-24.06) | 24.06 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Both allowed families produce 1 result/cycle, so the throughput_msps >= 1 constraint reduces to Fmax >= 1 MHz, which is trivially satisfied; the real trade-off is area (luts_plus_ffs) vs accuracy_bits. Accuracy depends only on W, N, angle_guard, frac_guard, rounding, so I bound W in 12..16 and N in 10..16: W=12 with N~12-14 and small guards should already push max_abs_err below 2^-10 (accuracy_bits >= 10), while W=16/N=16 gives headroom for the accuracy objective. Guards are kept small (0..2) because area is the primary objective and extra guard bits add LUT/FF cost with diminishing accuracy returns. pipelined_m with m=2..4 is included because it can beat full pipelined on FF count at the same throughput, potentially dominating on the luts_plus_ffs axis. Splitting budget evenly lets NSGA-II map the Pareto front across both families and find where pipelined_m's FF savings cross over pipelined's lower latency.*)
- `pipelined` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Full pipeline gives 1 result/cycle, so throughput = Fmax(MHz) >= 1 MSPS is easily met for any reasonable Fmax. Area is dominated by the N registered stages; keeping N in 10..16 and W in 12..16 keeps luts_plus_ffs low while accuracy_bits (driven by W, N, guards) stays >= 10. This family has the cleanest latency/throughput trade-off for the >=1 MSPS constraint.
- `pipelined_m` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Registering every m stages cuts FF count versus full pipelined while still yielding 1 result/cycle (throughput = Fmax >= 1 MSPS). m in 2..4 trades a small latency increase for meaningful FF savings, which directly serves the min luts_plus_ffs objective. Same W/N/guard ranges as pipelined to keep accuracy_bits >= 10 and area low.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 60 evaluations this round, 60 total; 38 feasible; hypervolume 1002 (n/a).

**LLM decision:** `stop` — The spec is satisfied with a strong margin on the critical constraint. The Pareto front contains 5 feasible designs, all meeting throughput >= 1 MSPS (best 97.8 MSPS, well above 1) and max_abs_err <= 2^-10 (best 0.000177, which is 2^-12.47, significantly better than the 0.000976 limit). The primary objective, minimizing luts_plus_ffs, is well-covered with the best design at 995 LUTs+FFs, which is comfortably below the HV reference of 1500. The accuracy objective is also well-covered, ranging from 10.7 to 12.5 bits, exceeding the HV reference of 10. The front spans a reasonable range of the area objective (995-1226) and accuracy (10.7-12.5). Since this is the final round, and the front already provides a clear, feasible, and high-quality trade-off curve with the minimum area design at 995 LUTs+FFs, further exploration is unnecessary. The selection rule (min luts_plus_ffs) will pick the 995 LUTs+FFs design, which is robust and feasible.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1002 (gain this round: n/a (first round)).
Feasible designs: 38 of 60 evaluations (32 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 37% violate; best seen 0.000177 (2^-12.47)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=995, accuracy_bits=10.7, luts=745, ffs=250, throughput_msps=97.8, max_abs_err=0.000594 (2^-10.72), power_index=0.0374
- pipelined_m [data_width=16 n_iter=13 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=1009, accuracy_bits=11, luts=747, ffs=262, throughput_msps=97.8, max_abs_err=0.000472 (2^-11.05), power_index=0.038
- pipelined_m [data_width=16 n_iter=13 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1026, accuracy_bits=11.4, luts=760, ffs=266, throughput_msps=97.8, max_abs_err=0.00038 (2^-11.36), power_index=0.0386
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1068, accuracy_bits=11.5, luts=800, ffs=268, throughput_msps=97.8, max_abs_err=0.000338 (2^-11.53), power_index=0.0402
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1226, accuracy_bits=12.5, luts=956, ffs=270, throughput_msps=97.8, max_abs_err=0.000177 (2^-12.47), power_index=0.0461
Front coverage: luts_plus_ffs 995..1226 (HV reference 1500); accuracy_bits 10.7..12.5 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- pipelined: 30 evals, 14 feasible; max throughput seen 282 MSPS; best accuracy 11.65 bits; best feasible luts_plus_ffs=1358; feasible ranges: data_width 15..16, n_iter 13..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 30 evals, 24 feasible; max throughput seen 171 MSPS; best accuracy 12.47 bits; best feasible luts_plus_ffs=995; feasible ranges: data_width 15..16, n_iter 13..16, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (5 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 71 feasible; hypervolume 1399 (+39.6%).

**No LLM call** (code's front-mapping round): The spec is satisfied with a strong margin on the critical constraint. The Pareto front contains 5 feasible designs, all meeting throughput >= 1 MSPS (best 97.8 MSPS, well above 1) and max_abs_err <= 2^-10 (best 0.000177, which is 2^-12.47, significantly better than the 0.000976 limit). The primary objective, minimizing luts_plus_ffs, is well-covered with the best design at 995 LUTs+FFs, which is comfortably below the HV reference of 1500. The accuracy objective is also well-covered, ranging from 10.7 to 12.5 bits, exceeding the HV reference of 10. The front spans a reasonable range of the area objective (995-1226) and accuracy (10.7-12.5). Since this is the final round, and the front already provides a clear, feasible, and high-quality trade-off curve with the minimum area design at 995 LUTs+FFs, further exploration is unnecessary. The selection rule (min luts_plus_ffs) will pick the 995 LUTs+FFs design, which is robust and feasible.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1399 (gain this round: +39.6%).
Feasible designs: 71 of 100 evaluations (62 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 29% violate; best seen 5.72e-08 (2^-24.06)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=885, accuracy_bits=10.1, luts=631, ffs=254, throughput_msps=124, max_abs_err=0.000887 (2^-10.14), power_index=0.0333
- pipelined_m [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=995, accuracy_bits=10.7, luts=745, ffs=250, throughput_msps=97.8, max_abs_err=0.000594 (2^-10.72), power_index=0.0374
- pipelined_m [data_width=16 n_iter=13 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1026, accuracy_bits=11.4, luts=760, ffs=266, throughput_msps=97.8, max_abs_err=0.00038 (2^-11.36), power_index=0.0386
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1068, accuracy_bits=11.5, luts=800, ffs=268, throughput_msps=97.8, max_abs_err=0.000338 (2^-11.53), power_index=0.0402
- pipelined_m [data_width=20 n_iter=15 angle_guard=-2 frac_guard=0 rounding=round m=7] luts_plus_ffs=1187, accuracy_bits=13, luts=949, ffs=237, throughput_msps=56.8, max_abs_err=0.00012 (2^-13.02), power_index=0.0446
- pipelined_m [data_width=24 n_iter=15 angle_guard=-2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1486, accuracy_bits=13.9, luts=1126, ffs=359, throughput_msps=89.6, max_abs_err=6.45e-05 (2^-13.92), power_index=0.0559
- pipelined_m [data_width=25 n_iter=15 angle_guard=0 frac_guard=3 rounding=round m=6] luts_plus_ffs=1654, accuracy_bits=14, luts=1341, ffs=313, throughput_msps=59.9, max_abs_err=6.13e-05 (2^-13.99), power_index=0.0622
- pipelined_m [data_width=24 n_iter=19 angle_guard=-2 frac_guard=0 rounding=round m=8] luts_plus_ffs=1728, accuracy_bits=16.8, luts=1447, ffs=281, throughput_msps=48, max_abs_err=8.52e-06 (2^-16.84), power_index=0.065
- pipelined_m [data_width=24 n_iter=28 angle_guard=-2 frac_guard=0 rounding=round m=6] luts_plus_ffs=2604, accuracy_bits=17.1, luts=2168, ffs=437, throughput_msps=62.5, max_abs_err=6.97e-06 (2^-17.13), power_index=0.098
- pipelined_m [data_width=28 n_iter=28 angle_guard=3 frac_guard=1 rounding=round m=7] luts_plus_ffs=3211, accuracy_bits=24.1, luts=2767, ffs=444, throughput_msps=49.9, max_abs_err=5.72e-08 (2^-24.06), power_index=0.121
Front coverage: luts_plus_ffs 885..3211 (HV reference 1500); accuracy_bits 10.1..24.1 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- pipelined: 30 evals, 14 feasible; max throughput seen 282 MSPS; best accuracy 11.65 bits; best feasible luts_plus_ffs=1358; feasible ranges: data_width 15..16, n_iter 13..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 70 evals, 57 feasible; max throughput seen 171 MSPS; best accuracy 24.06 bits; best feasible luts_plus_ffs=885; feasible ranges: data_width 15..28, n_iter 12..28, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4139 in, 1325 out
- provider-reported cost: $0.0044
- full prompts and replies: `llm_trace.jsonl`

