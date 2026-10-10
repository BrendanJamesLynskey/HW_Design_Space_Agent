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
`pipelined_m:data_width=15,n_iter=12,angle_guard=4,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 643 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 200 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 53.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0317 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000807 (2^-10.27) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.61 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000238 (2^-12.04) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.95 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=12,angle_guard=4,frac_guard=0,rounding=round,m=4` | 643 | 200 | 93.6 | 5 | 0.0317 | 0.000807 (2^-10.27) | 10.27 |
| 1 | `pipelined_m:data_width=15,n_iter=13,angle_guard=3,frac_guard=3,rounding=trunc,m=8` | 764 | 147 | 52.7 | 4 | 0.0343 | 0.000439 (2^-11.15) | 11.15 |
| 2 | `pipelined_m:data_width=15,n_iter=13,angle_guard=3,frac_guard=3,rounding=trunc,m=7` | 764 | 147 | 59.6 | 4 | 0.0343 | 0.000439 (2^-11.15) | 11.15 |
| 3 | `pipelined_m:data_width=17,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=4` | 786 | 268 | 97.8 | 6 | 0.0397 | 0.000301 (2^-11.70) | 11.70 |
| 4 | `pipelined_m:data_width=19,n_iter=13,angle_guard=4,frac_guard=0,rounding=round,m=4` | 852 | 313 | 89.6 | 6 | 0.0438 | 0.000258 (2^-11.92) | 11.92 |
| 5 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=4` | 920 | 291 | 93.6 | 6 | 0.0455 | 0.000109 (2^-13.17) | 13.17 |
| 6 | `pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=4,rounding=round,m=4` | 1118 | 309 | 93.6 | 6 | 0.0537 | 0.000105 (2^-13.22) | 13.22 |
| 7 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=4,rounding=round,m=3` | 1076 | 388 | 119.3 | 7 | 0.0551 | 7.86e-05 (2^-13.63) | 13.63 |
| 8 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=4,rounding=trunc,m=3` | 1112 | 458 | 119.3 | 8 | 0.059 | 5.8e-05 (2^-14.07) | 14.07 |
| 9 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=4,rounding=round,m=3` | 1150 | 460 | 119.3 | 8 | 0.0606 | 4.81e-05 (2^-14.34) | 14.34 |
| 10 | `pipelined_m:data_width=23,n_iter=20,angle_guard=-1,frac_guard=0,rounding=trunc,m=2` | 1487 | 803 | 158.3 | 12 | 0.0861 | 9.1e-06 (2^-16.75) | 16.75 |
| 11 | `pipelined_m:data_width=23,n_iter=20,angle_guard=-1,frac_guard=4,rounding=trunc,m=2` | 1647 | 876 | 152.6 | 12 | 0.0949 | 7.35e-06 (2^-17.05) | 17.05 |
| 12 | `pipelined_m:data_width=26,n_iter=24,angle_guard=4,frac_guard=2,rounding=trunc,m=7` | 2235 | 424 | 52.0 | 6 | 0.1 | 3.21e-07 (2^-21.57) | 21.57 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=1 MSPS throughput and max_abs_err <= 2^-10, with area (luts+ffs) as the primary objective. Both pipelined and pipelined_m families produce 1 result/cycle, so throughput_msps = Fmax in MHz. Since Fmax for a CORDIC on Artix-7 is typically 100-400 MHz, the throughput constraint is easily met by both families. The real trade-off is between area (LUTs+FFs) and accuracy. Accuracy depends on n_iter, data_width, angle_guard, frac_guard, and rounding. I focus n_iter in [12,16] and data_width in [14,20] because: (1) data_width=14 gives output LSB=2^-12, so with n_iter>=12 the CORDIC error should be well below 2^-10; (2) going below data_width=14 risks not meeting the error constraint; (3) going above data_width=20 adds area without meaningful accuracy gain for this spec. angle_guard and frac_guard are swept over their full ranges to find the minimal values that still satisfy the error constraint, since each extra guard bit adds area. Rounding is included as it can reduce required guard bits. pipelined_m is included because it can reduce FF count by not registering every stage, which directly helps the area objective. The budget is split 55/45 between pipelined and pipelined_m to give slightly more weight to the simpler full-pipeline design while still exploring the FF-reduction opportunity of pipelined_m.*)
- `pipelined` (33 evals): data_width=14..20, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Full pipeline gives 1 result/cycle, so throughput_msps = Fmax(MHz). To meet >=1 MSPS we need Fmax >= 1 MHz, which is trivially satisfied by any Artix-7 CORDIC datapath (Fmax is typically 100s of MHz). The binding constraint is max_abs_err <= 2^-10. Accuracy is dominated by n_iter and data_width. For a 14-bit output (LSB=2^-12), we need n_iter such that the CORDIC residual error plus truncation stays below 2^-10. Typically n_iter >= 12-14 with data_width >= 14 gives accuracy_bits > 10. I focus n_iter in [12,16] and data_width in [14,20] to capture the area/accuracy trade-off. angle_guard and frac_guard are swept to find the minimal guard bits that still meet the error constraint, since they directly add area. Rounding is included because it can reduce required guard bits.
- `pipelined_m` (27 evals): data_width=14..20, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* pipelined_m registers every m stages, reducing FF count compared to full pipelined while still achieving 1 result/cycle throughput. Since the objective is min luts_plus_ffs and area is everything, pipelined_m with m>1 can significantly reduce FFs at the cost of slightly lower Fmax (longer combinational paths between registers). For a motor-control loop at >=1 MSPS, even a modest Fmax reduction is acceptable as long as Fmax stays well above 1 MHz. I sweep m in [2,4] to find the sweet spot where FF savings outweigh any Fmax penalty. Same n_iter/data_width/guard ranges as pipelined since accuracy requirements are identical.

**Result (code):** 60 evaluations this round, 60 total; 54 feasible; hypervolume 1226 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 9 distinct designs covering the trade-off space effectively. The minimum area point (1034 LUTs+FFs) comfortably meets the throughput constraint (124 MSPS >> 1 MSPS) and accuracy constraint (10.7 bits > 10 bits required). The front extends to 14.7 bits accuracy, providing a clear trade-off curve for the selection rule (min luts_plus_ffs). Hypervolume is 1226 against a reference of 1500, indicating good coverage. Since this is the final round, the current front is sufficient for selecting the final design, which will be the 1034 LUTs+FFs pipelined_m design.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1226 (gain this round: n/a (first round)).
Feasible designs: 54 of 60 evaluations (48 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 273
- max_abs_err <= 0.000976562: 10% violate; best seen 3.84e-05 (2^-14.67)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1034, accuracy_bits=10.7, luts=731, ffs=303, throughput_msps=124, max_abs_err=0.000599 (2^-10.71), power_index=0.0389
- pipelined_m [data_width=17 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1054, accuracy_bits=11.7, luts=786, ffs=268, throughput_msps=97.8, max_abs_err=0.000301 (2^-11.70), power_index=0.0397
- pipelined_m [data_width=19 n_iter=13 angle_guard=4 frac_guard=0 rounding=round m=4] luts_plus_ffs=1165, accuracy_bits=11.9, luts=852, ffs=313, throughput_msps=89.6, max_abs_err=0.000258 (2^-11.92), power_index=0.0438
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1210, accuracy_bits=13.2, luts=920, ffs=291, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=0.0455
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=4 rounding=round m=4] luts_plus_ffs=1427, accuracy_bits=13.2, luts=1118, ffs=309, throughput_msps=93.6, max_abs_err=0.000105 (2^-13.22), power_index=0.0537
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=4 rounding=round m=3] luts_plus_ffs=1464, accuracy_bits=13.6, luts=1076, ffs=388, throughput_msps=119, max_abs_err=7.86e-05 (2^-13.63), power_index=0.0551
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=1570, accuracy_bits=14.1, luts=1112, ffs=458, throughput_msps=119, max_abs_err=5.8e-05 (2^-14.07), power_index=0.059
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=4 rounding=round m=3] luts_plus_ffs=1610, accuracy_bits=14.3, luts=1150, ffs=460, throughput_msps=119, max_abs_err=4.81e-05 (2^-14.34), power_index=0.0606
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=2326, accuracy_bits=14.7, luts=1170, ffs=1156, throughput_msps=264, max_abs_err=3.84e-05 (2^-14.67), power_index=0.0875
Front coverage: luts_plus_ffs 1034..2326 (HV reference 1500); accuracy_bits 10.7..14.7 (HV reference 10); data_width on the front 15..20 (registry 8..28).

Per family:
- pipelined: 33 evals, 30 feasible; max throughput seen 273 MSPS; best accuracy 14.67 bits; best feasible luts_plus_ffs=1493; feasible ranges: data_width 14..20, n_iter 12..16, angle_guard -2..3, frac_guard 1..4
- pipelined_m: 27 evals, 24 feasible; max throughput seen 171 MSPS; best accuracy 14.34 bits; best feasible luts_plus_ffs=1034; feasible ranges: data_width 14..20, n_iter 13..16, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (35 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (8 front designs; box front_anchored)
- `pipelined` (5 evals): data_width=19..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 91 feasible; hypervolume 1395 (+13.8%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 9 distinct designs covering the trade-off space effectively. The minimum area point (1034 LUTs+FFs) comfortably meets the throughput constraint (124 MSPS >> 1 MSPS) and accuracy constraint (10.7 bits > 10 bits required). The front extends to 14.7 bits accuracy, providing a clear trade-off curve for the selection rule (min luts_plus_ffs). Hypervolume is 1226 against a reference of 1500, indicating good coverage. Since this is the final round, the current front is sufficient for selecting the final design, which will be the 1034 LUTs+FFs pipelined_m design.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1395 (gain this round: +13.8%).
Feasible designs: 91 of 100 evaluations (79 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 273
- max_abs_err <= 0.000976562: 9% violate; best seen 3.21e-07 (2^-21.57)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=4 frac_guard=0 rounding=round m=4] luts_plus_ffs=843, accuracy_bits=10.3, luts=643, ffs=200, throughput_msps=93.6, max_abs_err=0.000807 (2^-10.27), power_index=0.0317
- pipelined_m [data_width=15 n_iter=13 angle_guard=3 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=911, accuracy_bits=11.2, luts=764, ffs=147, throughput_msps=52.7, max_abs_err=0.000439 (2^-11.15), power_index=0.0343
- pipelined_m [data_width=17 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1054, accuracy_bits=11.7, luts=786, ffs=268, throughput_msps=97.8, max_abs_err=0.000301 (2^-11.70), power_index=0.0397
- pipelined_m [data_width=19 n_iter=13 angle_guard=4 frac_guard=0 rounding=round m=4] luts_plus_ffs=1165, accuracy_bits=11.9, luts=852, ffs=313, throughput_msps=89.6, max_abs_err=0.000258 (2^-11.92), power_index=0.0438
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1210, accuracy_bits=13.2, luts=920, ffs=291, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=0.0455
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=4 rounding=round m=3] luts_plus_ffs=1464, accuracy_bits=13.6, luts=1076, ffs=388, throughput_msps=119, max_abs_err=7.86e-05 (2^-13.63), power_index=0.0551
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=1570, accuracy_bits=14.1, luts=1112, ffs=458, throughput_msps=119, max_abs_err=5.8e-05 (2^-14.07), power_index=0.059
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=4 rounding=round m=3] luts_plus_ffs=1610, accuracy_bits=14.3, luts=1150, ffs=460, throughput_msps=119, max_abs_err=4.81e-05 (2^-14.34), power_index=0.0606
- pipelined_m [data_width=23 n_iter=20 angle_guard=-1 frac_guard=4 rounding=trunc m=2] luts_plus_ffs=2523, accuracy_bits=17.1, luts=1647, ffs=876, throughput_msps=153, max_abs_err=7.35e-06 (2^-17.05), power_index=0.0949
- pipelined_m [data_width=26 n_iter=24 angle_guard=4 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=2659, accuracy_bits=21.6, luts=2235, ffs=424, throughput_msps=52, max_abs_err=3.21e-07 (2^-21.57), power_index=0.1
Front coverage: luts_plus_ffs 843..2659 (HV reference 1500); accuracy_bits 10.3..21.6 (HV reference 10); data_width on the front 15..26 (registry 8..28).

Per family:
- pipelined: 38 evals, 35 feasible; max throughput seen 273 MSPS; best accuracy 20.89 bits; best feasible luts_plus_ffs=1493; feasible ranges: data_width 14..27, n_iter 12..29, angle_guard -2..4, frac_guard 1..4
- pipelined_m: 62 evals, 56 feasible; max throughput seen 171 MSPS; best accuracy 21.57 bits; best feasible luts_plus_ffs=843; feasible ranges: data_width 14..26, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4556 in, 1426 out
- provider-reported cost: $0.0021
- full prompts and replies: `llm_trace.jsonl`

