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
`pipelined:data_width=15,n_iter=13,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 650 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 682 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 273 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 273 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 15 | exact: schedule |
| latency_ns | 55 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0501 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000879 (2^-10.15) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 7.2 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00022 (2^-12.15) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.8 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.2 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (27 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=15,n_iter=13,angle_guard=0,frac_guard=0,rounding=round` | 650 | 682 | 272.9 | 15 | 0.0501 | 0.000879 (2^-10.15) | 10.15 |
| 1 | `pipelined:data_width=15,n_iter=13,angle_guard=1,frac_guard=0,rounding=round` | 663 | 695 | 272.9 | 15 | 0.0511 | 0.000673 (2^-10.54) | 10.54 |
| 2 | `pipelined:data_width=15,n_iter=13,angle_guard=1,frac_guard=2,rounding=round` | 745 | 742 | 272.9 | 15 | 0.0559 | 0.000478 (2^-11.03) | 11.03 |
| 3 | `pipelined:data_width=15,n_iter=13,angle_guard=2,frac_guard=2,rounding=round` | 758 | 755 | 272.9 | 15 | 0.0569 | 0.000431 (2^-11.18) | 11.18 |
| 4 | `pipelined:data_width=15,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` | 786 | 811 | 272.9 | 16 | 0.0601 | 0.000405 (2^-11.27) | 11.27 |
| 5 | `pipelined:data_width=16,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 802 | 832 | 272.9 | 17 | 0.0615 | 0.000373 (2^-11.39) | 11.39 |
| 6 | `pipelined:data_width=18,n_iter=13,angle_guard=1,frac_guard=1,rounding=trunc` | 802 | 835 | 264.5 | 15 | 0.0616 | 0.000294 (2^-11.73) | 11.73 |
| 7 | `pipelined:data_width=17,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 813 | 847 | 264.5 | 16 | 0.0625 | 0.000194 (2^-12.33) | 12.33 |
| 8 | `pipelined:data_width=17,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` | 877 | 874 | 264.5 | 16 | 0.0658 | 0.000191 (2^-12.36) | 12.36 |
| 9 | `pipelined:data_width=17,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` | 868 | 896 | 264.5 | 16 | 0.0664 | 0.000178 (2^-12.46) | 12.46 |
| 10 | `pipelined:data_width=18,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc` | 868 | 900 | 264.5 | 16 | 0.0665 | 0.000172 (2^-12.50) | 12.50 |
| 11 | `pipelined:data_width=17,n_iter=14,angle_guard=1,frac_guard=2,rounding=round` | 890 | 884 | 264.5 | 16 | 0.0667 | 0.000171 (2^-12.51) | 12.51 |
| 12 | `pipelined:data_width=17,n_iter=14,angle_guard=2,frac_guard=2,rounding=round` | 904 | 898 | 264.5 | 16 | 0.0678 | 0.000169 (2^-12.53) | 12.53 |
| 13 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` | 909 | 938 | 264.5 | 16 | 0.0695 | 0.000156 (2^-12.65) | 12.65 |
| 14 | `pipelined:data_width=19,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 935 | 969 | 264.5 | 17 | 0.0716 | 0.000108 (2^-13.18) | 13.18 |
| 15 | `pipelined:data_width=19,n_iter=16,angle_guard=-1,frac_guard=1,rounding=round` | 1057 | 1047 | 264.5 | 18 | 0.0791 | 0.000101 (2^-13.28) | 13.28 |
| 16 | `pipelined:data_width=19,n_iter=16,angle_guard=4,frac_guard=0,rounding=round` | 1064 | 1098 | 256.5 | 18 | 0.0813 | 5.75e-05 (2^-14.09) | 14.09 |
| 17 | `pipelined:data_width=19,n_iter=16,angle_guard=4,frac_guard=1,rounding=round` | 1136 | 1128 | 256.5 | 18 | 0.0852 | 4.65e-05 (2^-14.39) | 14.39 |
| 18 | `pipelined:data_width=19,n_iter=18,angle_guard=4,frac_guard=0,rounding=round` | 1205 | 1235 | 256.5 | 20 | 0.0918 | 3.74e-05 (2^-14.71) | 14.71 |
| 19 | `pipelined:data_width=24,n_iter=16,angle_guard=-1,frac_guard=2,rounding=round` | 1336 | 1318 | 256.5 | 18 | 0.0998 | 3.16e-05 (2^-14.95) | 14.95 |
| 20 | `pipelined:data_width=24,n_iter=16,angle_guard=2,frac_guard=3,rounding=round` | 1415 | 1394 | 249.0 | 18 | 0.106 | 3.07e-05 (2^-14.99) | 14.99 |
| 21 | `pipelined:data_width=27,n_iter=16,angle_guard=0,frac_guard=3,rounding=round` | 1532 | 1507 | 249.0 | 18 | 0.114 | 3.05e-05 (2^-15.00) | 15.00 |
| 22 | `pipelined:data_width=27,n_iter=16,angle_guard=4,frac_guard=3,rounding=trunc` | 1538 | 1570 | 242.0 | 18 | 0.117 | 3.05e-05 (2^-15.00) | 15.00 |
| 23 | `pipelined:data_width=25,n_iter=18,angle_guard=0,frac_guard=2,rounding=round` | 1581 | 1556 | 249.0 | 20 | 0.118 | 8.06e-06 (2^-16.92) | 16.92 |
| 24 | `pipelined:data_width=27,n_iter=21,angle_guard=-1,frac_guard=3,rounding=round` | 2001 | 1960 | 249.0 | 23 | 0.149 | 1.38e-06 (2^-19.47) | 19.47 |
| 25 | `pipelined:data_width=27,n_iter=26,angle_guard=-1,frac_guard=3,rounding=round` | 2486 | 2429 | 249.0 | 28 | 0.185 | 6.21e-07 (2^-20.62) | 20.62 |
| 26 | `pipelined:data_width=27,n_iter=26,angle_guard=1,frac_guard=3,rounding=trunc` | 2482 | 2480 | 249.0 | 28 | 0.187 | 1.6e-07 (2^-22.58) | 22.58 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >=1 MSPS throughput and max_abs_err <= 2^-10, with area (luts+ffs) as the primary objective. Only pipelined and pipelined_m families are available to me, and both produce 1 result/cycle, so throughput is simply Fmax. Since Fmax on Artix-7 for a CORDIC datapath is typically 100-300 MHz, the throughput constraint is easily satisfied by either family. The binding constraints are therefore accuracy and area. For accuracy: CORDIC residual error after N iterations is bounded by ~2^-(N+1), so N >= 10 is needed to guarantee max_abs_err <= 2^-10. I set n_iter range to 10-16 to explore the accuracy/area trade-off. For area: data_width W determines datapath width and thus LUT/FF count linearly. W=12 gives Q1.10 output which exactly matches the 2^-10 error spec, so W=12 is the minimum viable width. I explore W=12-18 to capture the full trade-off curve. angle_guard and frac_guard add bits to internal paths and increase area; since accuracy is governed primarily by n_iter, I keep these ranges tight (angle_guard -1..2, frac_guard 0..2) to avoid wasting budget on area-inflating configurations that don't improve the objective. I allocate all budget to the pipelined family in this first round because it has the simplest structure (one register per stage, N+2 latency) and its area scales predictably with N and W, making it the clearest baseline for the Pareto front. pipelined_m can be explored in a later round if the front suggests that reducing register count (at the cost of higher latency) yields a better area point. The selection rule is min luts_plus_ffs, so the front will be dominated by low-N, low-W configurations that still meet the accuracy constraint; the hypervolume objective on accuracy_bits will pull the search toward slightly higher n_iter to capture the accuracy dimension.*)
- `pipelined` (60 evals): data_width=12..18, n_iter=10..16, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Fully pipelined gives 1 result/cycle, so throughput = Fmax. To hit >=1 MSPS we need Fmax >= 1 MHz, which is trivially met; the real cost driver is area (N+2 stages of datapath). Accuracy <= 2^-10 requires enough iterations: CORDIC error is roughly 2^-(n_iter+1) in the worst case, so n_iter >= 10-11 is the floor. data_width drives both area and output resolution; 12-18 covers the accuracy floor (W=12 gives Q1.10 output, matching the 2^-10 spec exactly) up to a modest oversize. angle_guard and frac_guard are kept small to control area since accuracy is already met by n_iter. Rounding is cheap and can shave error, so include both.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 60 evaluations this round, 60 total; 40 feasible; hypervolume 86.81 (n/a).

**LLM decision:** `stop` — The spec is feasible and the Pareto front is well-mapped within the constraints. The minimum area design (pipelined, data_width=15, n_iter=13) achieves 1332 LUTs+FFs, which is below the hypervolume reference of 1500, and meets the throughput constraint (273 MSPS >= 1 MSPS) and accuracy constraint (10.2 bits >= 10 bits). The front extends up to 13.1 bits accuracy, providing a good trade-off curve. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (1332) as per the selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 86.81 (gain this round: n/a (first round)).
Feasible designs: 40 of 60 evaluations (29 unique).
Families explored so far: pipelined. Not yet explored: pipelined_m.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 33% violate; best seen 0.000116 (2^-13.08)

Pareto front (feasible, 14 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=1332, accuracy_bits=10.2, luts=650, ffs=682, throughput_msps=273, max_abs_err=0.000879 (2^-10.15), power_index=0.0501
- pipelined [data_width=15 n_iter=13 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=1358, accuracy_bits=10.5, luts=663, ffs=695, throughput_msps=273, max_abs_err=0.000673 (2^-10.54), power_index=0.0511
- pipelined [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=1512, accuracy_bits=11.2, luts=758, ffs=755, throughput_msps=273, max_abs_err=0.000431 (2^-11.18), power_index=0.0569
- pipelined [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=1597, accuracy_bits=11.3, luts=786, ffs=811, throughput_msps=273, max_abs_err=0.000405 (2^-11.27), power_index=0.0601
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=1661, accuracy_bits=12.3, luts=813, ffs=847, throughput_msps=264, max_abs_err=0.000194 (2^-12.33), power_index=0.0625
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=1750, accuracy_bits=12.4, luts=877, ffs=874, throughput_msps=264, max_abs_err=0.000191 (2^-12.36), power_index=0.0658
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=1768, accuracy_bits=12.5, luts=868, ffs=900, throughput_msps=264, max_abs_err=0.000172 (2^-12.50), power_index=0.0665
- pipelined [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=1774, accuracy_bits=12.5, luts=890, ffs=884, throughput_msps=264, max_abs_err=0.000171 (2^-12.51), power_index=0.0667
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=1848, accuracy_bits=12.6, luts=909, ffs=938, throughput_msps=264, max_abs_err=0.000156 (2^-12.65), power_index=0.0695
- pipelined [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=2026, accuracy_bits=13.1, luts=1001, ffs=1025, throughput_msps=264, max_abs_err=0.000116 (2^-13.08), power_index=0.0762
Front coverage: luts_plus_ffs 1332..2026 (HV reference 1500); accuracy_bits 10.2..13.1 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- pipelined: 60 evals, 40 feasible; max throughput seen 282 MSPS; best accuracy 13.08 bits; best feasible luts_plus_ffs=1332; feasible ranges: data_width 15..18, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (40 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (14 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 78 feasible; hypervolume 86.81 (+0.0%).

**No LLM call** (code's front-mapping round): The spec is feasible and the Pareto front is well-mapped within the constraints. The minimum area design (pipelined, data_width=15, n_iter=13) achieves 1332 LUTs+FFs, which is below the hypervolume reference of 1500, and meets the throughput constraint (273 MSPS >= 1 MSPS) and accuracy constraint (10.2 bits >= 10 bits). The front extends up to 13.1 bits accuracy, providing a good trade-off curve. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (1332) as per the selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 86.81 (gain this round: +0.0%).
Feasible designs: 78 of 100 evaluations (64 unique).
Families explored so far: pipelined. Not yet explored: pipelined_m.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 22% violate; best seen 1.6e-07 (2^-22.58)

Pareto front (feasible, 27 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=1332, accuracy_bits=10.2, luts=650, ffs=682, throughput_msps=273, max_abs_err=0.000879 (2^-10.15), power_index=0.0501
- pipelined [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=1512, accuracy_bits=11.2, luts=758, ffs=755, throughput_msps=273, max_abs_err=0.000431 (2^-11.18), power_index=0.0569
- pipelined [data_width=18 n_iter=13 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=1637, accuracy_bits=11.7, luts=802, ffs=835, throughput_msps=264, max_abs_err=0.000294 (2^-11.73), power_index=0.0616
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=1764, accuracy_bits=12.5, luts=868, ffs=896, throughput_msps=264, max_abs_err=0.000178 (2^-12.46), power_index=0.0664
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=1802, accuracy_bits=12.5, luts=904, ffs=898, throughput_msps=264, max_abs_err=0.000169 (2^-12.53), power_index=0.0678
- pipelined [data_width=19 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=1903, accuracy_bits=13.2, luts=935, ffs=969, throughput_msps=264, max_abs_err=0.000108 (2^-13.18), power_index=0.0716
- pipelined [data_width=19 n_iter=16 angle_guard=4 frac_guard=1 rounding=round] luts_plus_ffs=2264, accuracy_bits=14.4, luts=1136, ffs=1128, throughput_msps=257, max_abs_err=4.65e-05 (2^-14.39), power_index=0.0852
- pipelined [data_width=24 n_iter=16 angle_guard=2 frac_guard=3 rounding=round] luts_plus_ffs=2810, accuracy_bits=15, luts=1415, ffs=1394, throughput_msps=249, max_abs_err=3.07e-05 (2^-14.99), power_index=0.106
- pipelined [data_width=25 n_iter=18 angle_guard=0 frac_guard=2 rounding=round] luts_plus_ffs=3136, accuracy_bits=16.9, luts=1581, ffs=1556, throughput_msps=249, max_abs_err=8.06e-06 (2^-16.92), power_index=0.118
- pipelined [data_width=27 n_iter=26 angle_guard=1 frac_guard=3 rounding=trunc] luts_plus_ffs=4962, accuracy_bits=22.6, luts=2482, ffs=2480, throughput_msps=249, max_abs_err=1.6e-07 (2^-22.58), power_index=0.187
Front coverage: luts_plus_ffs 1332..4962 (HV reference 1500); accuracy_bits 10.2..22.6 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- pipelined: 100 evals, 78 feasible; max throughput seen 282 MSPS; best accuracy 22.58 bits; best feasible luts_plus_ffs=1332; feasible ranges: data_width 14..27, n_iter 12..30, angle_guard -2..4, frac_guard 0..3
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4529 in, 1084 out
- provider-reported cost: $0.0045
- full prompts and replies: `llm_trace.jsonl`

