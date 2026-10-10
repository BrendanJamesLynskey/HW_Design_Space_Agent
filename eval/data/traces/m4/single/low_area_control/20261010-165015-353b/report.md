# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 4 round(s).  
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
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`unrolled_k:data_width=15,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,k=2` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 246 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 90 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 105 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 10.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 10 | exact: schedule |
| latency_ns | 94.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.126 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00081 (2^-10.27) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.64 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00021 (2^-12.22) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.72 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (32768 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 10 cycles, a new input every 10 cycle(s). DDS tone from its exact outputs: SFDR 83.6 dBc, SNR 71.3 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (20 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `unrolled_k:data_width=15,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,k=2` | 246 | 90 | 10.5 | 10 | 0.126 | 0.00081 (2^-10.27) | 10.27 |
| 1 | `unrolled_k:data_width=15,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,k=2` | 252 | 92 | 10.5 | 10 | 0.129 | 0.000599 (2^-10.71) | 10.71 |
| 2 | `unrolled_k:data_width=15,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc,k=2` | 257 | 94 | 10.5 | 10 | 0.132 | 0.000567 (2^-10.78) | 10.78 |
| 3 | `unrolled_k:data_width=15,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,k=2` | 297 | 94 | 10.5 | 10 | 0.147 | 0.000403 (2^-11.28) | 11.28 |
| 4 | `unrolled_k:data_width=17,n_iter=23,angle_guard=3,frac_guard=0,rounding=round,k=2` | 304 | 104 | 6.9 | 15 | 0.23 | 0.000146 (2^-12.74) | 12.74 |
| 5 | `unrolled_k:data_width=17,n_iter=21,angle_guard=1,frac_guard=4,rounding=trunc,k=2` | 349 | 110 | 7.3 | 14 | 0.242 | 0.000108 (2^-13.17) | 13.17 |
| 6 | `unrolled_k:data_width=17,n_iter=26,angle_guard=2,frac_guard=4,rounding=trunc,k=2` | 353 | 111 | 6.4 | 16 | 0.279 | 8.01e-05 (2^-13.61) | 13.61 |
| 7 | `unrolled_k:data_width=17,n_iter=22,angle_guard=4,frac_guard=2,rounding=round,k=2` | 376 | 109 | 7.3 | 14 | 0.255 | 5.05e-05 (2^-14.27) | 14.27 |
| 8 | `unrolled_k:data_width=20,n_iter=20,angle_guard=3,frac_guard=0,rounding=round,k=3` | 468 | 118 | 6.8 | 10 | 0.221 | 2.17e-05 (2^-15.49) | 15.49 |
| 9 | `unrolled_k:data_width=26,n_iter=18,angle_guard=0,frac_guard=0,rounding=trunc,k=2` | 460 | 146 | 8.4 | 12 | 0.274 | 8.07e-06 (2^-16.92) | 16.92 |
| 10 | `unrolled_k:data_width=25,n_iter=30,angle_guard=0,frac_guard=0,rounding=round,k=2` | 466 | 141 | 5.6 | 18 | 0.411 | 1.37e-06 (2^-19.48) | 19.48 |
| 11 | `unrolled_k:data_width=27,n_iter=21,angle_guard=0,frac_guard=2,rounding=trunc,k=2` | 512 | 155 | 7.0 | 14 | 0.352 | 1.1e-06 (2^-19.79) | 19.79 |
| 12 | `unrolled_k:data_width=25,n_iter=22,angle_guard=4,frac_guard=1,rounding=round,k=2` | 535 | 147 | 7.0 | 14 | 0.36 | 7.29e-07 (2^-20.39) | 20.39 |
| 13 | `unrolled_k:data_width=25,n_iter=22,angle_guard=4,frac_guard=2,rounding=round,k=2` | 552 | 149 | 7.0 | 14 | 0.369 | 6.63e-07 (2^-20.52) | 20.52 |
| 14 | `unrolled_k:data_width=25,n_iter=26,angle_guard=2,frac_guard=2,rounding=round,k=2` | 564 | 147 | 6.1 | 16 | 0.428 | 3.7e-07 (2^-21.37) | 21.37 |
| 15 | `unrolled_k:data_width=28,n_iter=23,angle_guard=2,frac_guard=2,rounding=round,k=2` | 610 | 162 | 6.5 | 15 | 0.436 | 2.66e-07 (2^-21.84) | 21.84 |
| 16 | `unrolled_k:data_width=28,n_iter=28,angle_guard=3,frac_guard=1,rounding=round,k=2` | 623 | 161 | 5.6 | 17 | 0.502 | 5.72e-08 (2^-24.06) | 24.06 |
| 17 | `unrolled_k:data_width=28,n_iter=30,angle_guard=2,frac_guard=4,rounding=trunc,k=3` | 782 | 166 | 5.0 | 13 | 0.464 | 4.72e-08 (2^-24.34) | 24.34 |
| 18 | `unrolled_k:data_width=28,n_iter=30,angle_guard=2,frac_guard=2,rounding=round,k=3` | 810 | 162 | 5.1 | 13 | 0.476 | 4.62e-08 (2^-24.37) | 24.37 |
| 19 | `unrolled_k:data_width=28,n_iter=28,angle_guard=4,frac_guard=2,rounding=round,k=4` | 957 | 163 | 4.9 | 10 | 0.422 | 3.55e-08 (2^-24.75) | 24.75 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >=1 MSPS throughput and max error <= 2^-10, with primary objective minimizing LUT+FFs. Iterative is excluded because it produces 1 result every N+3 cycles, making it impossible to hit 1 MSPS unless Fmax is extremely high (unlikely for N>=10). Pipelined_m is the strongest candidate for low area + high throughput, as it reduces FFs by registering every m stages. Pipelined is included as a baseline for Fmax/area trade-offs. Unrolled_k is included as a tertiary option for potential area savings via shared datapath. The n_iter range 10-16 is chosen because CORDIC error converges rapidly; 10 iterations typically give ~2^-10 accuracy, and going higher adds area without significant accuracy gain. Data width 12-16 ensures the output Q1.(W-2) format meets the 2^-10 error requirement (W=12 gives 10 fractional bits, which is borderline; W=14-16 provides margin). Angle and frac guards are kept low (0-2) to minimize area, as the error constraint is not extremely tight.*)
- `pipelined_m` (50 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m is the primary candidate for low-area 1 MSPS throughput. By registering every m stages (m=2..4), it drastically cuts FF count compared to full pipelining while maintaining 1 result/cycle. The n_iter=10..16 range targets the sweet spot where CORDIC error drops below 2^-10 with minimal iterations. data_width 12-16 balances the Q1.(W-2) output precision against area. This family offers the best LUT+FF trade-off for the 'area is everything' constraint.
- `pipelined` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Full pipelined serves as a baseline for the throughput constraint. While it has higher FF count than pipelined_m, it may have slightly better Fmax due to shorter critical paths, which could help if pipelined_m struggles to hit 1 MSPS at low n_iter. It helps map the upper bound of the area trade-off curve for the hypervolume.
- `unrolled_k` (20 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k with k=2..4 can achieve 1 result/cycle throughput (if Fmax is high enough) with potentially lower FF count than pipelined_m because it shares the datapath more aggressively. It's a secondary candidate to explore if pipelined_m's FF count is still too high. The k parameter allows trading latency for area/throughput.

**Result (code):** 100 evaluations this round, 100 total; 56 feasible; hypervolume 1361 (n/a).

**LLM decision:** `refine` — The current Pareto front is dominated by pipelined_m designs (luts_plus_ffs > 900) because the unrolled_k candidate (431) is an outlier from a very narrow search region (data_width=15, n_iter=15, k=3..4). The spec prioritizes area (min luts_plus_ffs) with a throughput constraint of >= 1 MSPS. Since unrolled_k achieves 8.97 MSPS (well above 1) at 431 area, it is the clear winner for the selection rule. However, the front lacks coverage in the low-area region (431..900) and high-accuracy region (>12 bits). The previous round explored unrolled_k very sparsely (only 20 evals, 3 feasible). To maximize hypervolume, we need to densely map the unrolled_k family around the known good point (W=15, N=15) to find if we can push area lower or accuracy higher, and also check if pipelined_m can be pushed to lower area (currently best is 946, but the front shows 1007+). The 'iterative' family is likely too slow (1 result/cycle but N+3 latency, low throughput) or too large for this specific low-area/high-throughput mix, so we focus on refining the existing families. We will narrow the ranges for unrolled_k to focus on W=14..16, N=12..18, k=2..6 to find the true minimum area point, and for pipelined_m to W=14..16, N=12..16, m=2..4 to see if we can beat 946.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 1361 (gain this round: n/a (first round)).
Feasible designs: 56 of 100 evaluations (44 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 44% violate; best seen 0.000241 (2^-12.02)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=15 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc k=3] luts_plus_ffs=431, accuracy_bits=10.8, luts=338, ffs=93, throughput_msps=8.97, max_abs_err=0.000567 (2^-10.78), power_index=0.13
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1007, accuracy_bits=11.1, luts=739, ffs=268, throughput_msps=97.8, max_abs_err=0.00046 (2^-11.09), power_index=0.0379
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1038, accuracy_bits=11.4, luts=764, ffs=274, throughput_msps=97.8, max_abs_err=0.000378 (2^-11.37), power_index=0.0391
- pipelined_m [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=3] luts_plus_ffs=1073, accuracy_bits=11.5, luts=759, ffs=315, throughput_msps=124, max_abs_err=0.000342 (2^-11.51), power_index=0.0404
- pipelined_m [data_width=16 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1110, accuracy_bits=11.6, luts=846, ffs=264, throughput_msps=97.8, max_abs_err=0.000323 (2^-11.60), power_index=0.0418
- pipelined_m [data_width=16 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1146, accuracy_bits=12, luts=876, ffs=270, throughput_msps=97.8, max_abs_err=0.00025 (2^-11.97), power_index=0.0431
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1165, accuracy_bits=12, luts=890, ffs=274, throughput_msps=97.8, max_abs_err=0.000241 (2^-12.02), power_index=0.0438
Front coverage: luts_plus_ffs 431..1165 (HV reference 1500); accuracy_bits 10.8..12 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 3 feasible; max throughput seen 13.5 MSPS; best accuracy 10.78 bits; best feasible luts_plus_ffs=431; feasible ranges: data_width 15..15, n_iter 15..15, angle_guard 1..1, frac_guard 1..1, k 3..4
- pipelined: 30 evals, 20 feasible; max throughput seen 282 MSPS; best accuracy 11.70 bits; best feasible luts_plus_ffs=1273; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 33 feasible; max throughput seen 178 MSPS; best accuracy 12.02 bits; best feasible luts_plus_ffs=946; feasible ranges: data_width 14..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Narrowing the search to the promising regions identified in Round 1. unrolled_k is the area leader, so it gets 60% of the budget to ensure we find the absolute minimum area point. pipelined_m gets 40% to fill the gap in the Pareto front between 431 and 1000 area units.*)
- `unrolled_k` (60 evals): data_width=14..16, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..6. *Why:* Focus on the low-area winner. The previous search was too narrow (only W=15, N=15 feasible). Expanding slightly to W=14..16 and N=12..18 with k=2..6 will reveal if we can get <431 area or >10.8 bits accuracy while maintaining >1 MSPS.
- `pipelined_m` (40 evals): data_width=14..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Refine the pipelined_m family to see if we can push the area below 946 (current best feasible) or improve accuracy beyond 12 bits. The front currently jumps from 431 to 1007, leaving a gap. This helps fill the hypervolume in the mid-area range.

**Result (code):** 100 evaluations this round, 200 total; 145 feasible; hypervolume 2781 (+104.3%).

**LLM decision:** `refine` — The current Pareto front is dominated by unrolled_k designs in the low-area region (342-424 LUTs+FFs) and pipelined_m in the high-accuracy region (12.9 bits, 1264 LUTs+FFs). There is a gap in the middle of the accuracy range (10.5-12 bits) where unrolled_k might be able to provide better accuracy at lower area than pipelined_m. By refining the search around the promising regions of unrolled_k (data_width=15, n_iter=12-14, k=2-3) and pipelined_m (data_width=15-16, m=2-4), we can better map the trade-off curve and potentially find non-dominated points that improve the hypervolume. The iterative family is not yet explored, but given that unrolled_k and pipelined_m are already providing a good front, and iterative is likely to have lower throughput (1 result every N+3 cycles) which might not be necessary for the 1 MSPS requirement, we focus on refining the existing families first. If the front does not improve significantly, we can consider adding iterative in the next round.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 2781 (gain this round: +104.3%).
Feasible designs: 145 of 200 evaluations (117 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 28% violate; best seen 0.000134 (2^-12.86)

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=15 n_iter=13 angle_guard=0 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=342, accuracy_bits=10, luts=250, ffs=92, throughput_msps=10.5, max_abs_err=0.000944 (2^-10.05), power_index=0.129
- unrolled_k [data_width=16 n_iter=12 angle_guard=2 frac_guard=0 rounding=trunc k=3] luts_plus_ffs=379, accuracy_bits=10.1, luts=283, ffs=96, throughput_msps=13.5, max_abs_err=0.000887 (2^-10.14), power_index=0.0999
- unrolled_k [data_width=15 n_iter=16 angle_guard=0 frac_guard=1 rounding=round k=2] luts_plus_ffs=383, accuracy_bits=10.4, luts=291, ffs=92, throughput_msps=9.58, max_abs_err=0.000744 (2^-10.39), power_index=0.158
- unrolled_k [data_width=15 n_iter=13 angle_guard=1 frac_guard=0 rounding=round k=3] luts_plus_ffs=383, accuracy_bits=10.5, luts=292, ffs=91, throughput_msps=8.97, max_abs_err=0.000673 (2^-10.54), power_index=0.115
- unrolled_k [data_width=16 n_iter=13 angle_guard=0 frac_guard=1 rounding=round k=2] luts_plus_ffs=406, accuracy_bits=11, luts=309, ffs=97, throughput_msps=10.5, max_abs_err=0.000472 (2^-11.05), power_index=0.153
- unrolled_k [data_width=16 n_iter=13 angle_guard=1 frac_guard=1 rounding=trunc k=3] luts_plus_ffs=416, accuracy_bits=11.1, luts=318, ffs=98, throughput_msps=8.97, max_abs_err=0.00046 (2^-11.09), power_index=0.125
- unrolled_k [data_width=16 n_iter=17 angle_guard=2 frac_guard=1 rounding=round k=2] luts_plus_ffs=424, accuracy_bits=12.5, luts=324, ffs=100, throughput_msps=8.78, max_abs_err=0.000177 (2^-12.47), power_index=0.191
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1264, accuracy_bits=12.9, luts=987, ffs=276, throughput_msps=97.8, max_abs_err=0.000134 (2^-12.86), power_index=0.0475
Front coverage: luts_plus_ffs 342..1264 (HV reference 1500); accuracy_bits 10..12.9 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- unrolled_k: 80 evals, 58 feasible; max throughput seen 13.5 MSPS; best accuracy 12.47 bits; best feasible luts_plus_ffs=342; feasible ranges: data_width 15..16, n_iter 12..18, angle_guard 0..2, frac_guard 0..2, k 2..6
- pipelined: 30 evals, 20 feasible; max throughput seen 282 MSPS; best accuracy 11.70 bits; best feasible luts_plus_ffs=1273; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 90 evals, 67 feasible; max throughput seen 178 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=868; feasible ranges: data_width 14..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The current Pareto front is dominated by unrolled_k designs in the low-area region (342-424 LUTs+FFs) and pipelined_m in the high-accuracy region (12.9 bits, 1264 LUTs+FFs). There is a gap in the middle of the accuracy range (10.5-12 bits) where unrolled_k might be able to provide better accuracy at lower area than pipelined_m. By refining the search around the promising regions of unrolled_k (data_width=15, n_iter=12-14, k=2-3) and pipelined_m (data_width=15-16, m=2-4), we can better map the trade-off curve and potentially find non-dominated points that improve the hypervolume. The iterative family is not yet explored, but given that unrolled_k and pipelined_m are already providing a good front, and iterative is likely to have lower throughput (1 result every N+3 cycles) which might not be necessary for the 1 MSPS requirement, we focus on refining the existing families first. If the front does not improve significantly, we can consider adding iterative in the next round.*)
- `unrolled_k` (20 evals): data_width=15..15, n_iter=12..14, angle_guard=0..2, frac_guard=0..1, rounding=trunc|round, k=2..2. *Why:* The current Pareto front is dominated by unrolled_k designs with luts_plus_ffs between 342 and 424, which is significantly lower than the pipelined families (868+). The spec prioritizes area minimization (min luts_plus_ffs) and the selection rule is also min luts_plus_ffs. The best area design is unrolled_k [data_width=15, n_iter=13, angle_guard=0, frac_guard=1, rounding=trunc, k=2] with 342 LUTs+FFs and 10.05 bits accuracy. To improve hypervolume, we need to explore if we can push accuracy higher (towards 12+ bits) while keeping area low, or if we can reduce area further. The current front has a gap in accuracy between 10.5 and 11.0 bits. Focusing on data_width=15 (cheaper) with n_iter 12-14 and k=2 (best area) allows us to map the accuracy-area trade-off more densely in the low-area region. We also include k=3 to see if it offers better accuracy at similar area.
- `pipelined_m` (12 evals): data_width=15..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m offers the highest accuracy on the front (12.9 bits) but at a much higher area cost (1264 LUTs+FFs). The spec requires >= 1 MSPS throughput, which pipelined_m easily meets (97.8 MSPS for the best accuracy design). However, since area is the primary objective, we should explore if pipelined_m can achieve high accuracy (12+ bits) at a lower area cost than the current 1264. The current best area for pipelined_m is 868, but its accuracy is not listed on the Pareto front, suggesting it might be dominated by unrolled_k in the area-accuracy trade-off. By focusing on data_width=15-16 and m=2-4, we can see if pipelined_m can provide a non-dominated point in the high-accuracy, moderate-area region that unrolled_k cannot reach.
- `pipelined` (8 evals): data_width=15..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined has the highest throughput (282 MSPS) but the highest area (1273 LUTs+FFs) among the feasible designs. It is likely dominated by pipelined_m in most cases since pipelined_m can achieve similar or better accuracy at lower area by using fewer registers. However, pipelined might have a slight edge in Fmax or power in some configurations. We allocate a small budget to confirm if pipelined can offer any non-dominated points, particularly in the very high throughput region, although the spec only requires 1 MSPS.

**Result (code):** 40 evaluations this round, 240 total; 176 feasible; hypervolume 2827 (+1.7%).

**LLM decision:** `stop` — The feasible Pareto front is well-established and the selection rule (min luts_plus_ffs) is satisfied by the unrolled_k design at 336 LUTs+FFs, which comfortably beats the HV reference of 1500. This design meets the throughput constraint (10.5 MSPS >= 1) and the accuracy constraint (max_abs_err 0.00081 <= 0.000976562). The front covers the relevant trade-off space for this low-area spec: the area objective is dominated by the unrolled_k family (336-424), while pipelined/pipelined_m are significantly larger (868-1264) and thus irrelevant for the min-area selection. Accuracy bits on the front range from 10.3 to 12.9, covering the constraint boundary and beyond. Since this is the final round and the front is stable with a clear winner for the selection rule, stopping is appropriate.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 2827 (gain this round: +1.7%).
Feasible designs: 176 of 240 evaluations (139 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 27% violate; best seen 0.000134 (2^-12.86)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round k=2] luts_plus_ffs=336, accuracy_bits=10.3, luts=246, ffs=90, throughput_msps=10.5, max_abs_err=0.00081 (2^-10.27), power_index=0.126
- unrolled_k [data_width=15 n_iter=14 angle_guard=2 frac_guard=0 rounding=round k=2] luts_plus_ffs=344, accuracy_bits=10.7, luts=252, ffs=92, throughput_msps=10.5, max_abs_err=0.000599 (2^-10.71), power_index=0.129
- unrolled_k [data_width=15 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=350, accuracy_bits=10.8, luts=257, ffs=94, throughput_msps=10.5, max_abs_err=0.000567 (2^-10.78), power_index=0.132
- unrolled_k [data_width=15 n_iter=14 angle_guard=2 frac_guard=1 rounding=round k=2] luts_plus_ffs=391, accuracy_bits=11.3, luts=297, ffs=94, throughput_msps=10.5, max_abs_err=0.000403 (2^-11.28), power_index=0.147
- unrolled_k [data_width=16 n_iter=17 angle_guard=2 frac_guard=1 rounding=round k=2] luts_plus_ffs=424, accuracy_bits=12.5, luts=324, ffs=100, throughput_msps=8.78, max_abs_err=0.000177 (2^-12.47), power_index=0.191
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1264, accuracy_bits=12.9, luts=987, ffs=276, throughput_msps=97.8, max_abs_err=0.000134 (2^-12.86), power_index=0.0475
Front coverage: luts_plus_ffs 336..1264 (HV reference 1500); accuracy_bits 10.3..12.9 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- unrolled_k: 100 evals, 72 feasible; max throughput seen 13.5 MSPS; best accuracy 12.47 bits; best feasible luts_plus_ffs=336; feasible ranges: data_width 15..16, n_iter 12..18, angle_guard 0..2, frac_guard 0..2, k 2..6
- pipelined: 38 evals, 28 feasible; max throughput seen 282 MSPS; best accuracy 12.04 bits; best feasible luts_plus_ffs=1273; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 102 evals, 76 feasible; max throughput seen 178 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=868; feasible ranges: data_width 14..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `unrolled_k` (134 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (5 front designs; box front_anchored)
- `pipelined_m` (26 evals): data_width=15..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 331 feasible; hypervolume 1.307e+04 (+362.3%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and the selection rule (min luts_plus_ffs) is satisfied by the unrolled_k design at 336 LUTs+FFs, which comfortably beats the HV reference of 1500. This design meets the throughput constraint (10.5 MSPS >= 1) and the accuracy constraint (max_abs_err 0.00081 <= 0.000976562). The front covers the relevant trade-off space for this low-area spec: the area objective is dominated by the unrolled_k family (336-424), while pipelined/pipelined_m are significantly larger (868-1264) and thus irrelevant for the min-area selection. Accuracy bits on the front range from 10.3 to 12.9, covering the constraint boundary and beyond. Since this is the final round and the front is stable with a clear winner for the selection rule, stopping is appropriate.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.307e+04 (gain this round: +362.3%).
Feasible designs: 331 of 400 evaluations (283 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 17% violate; best seen 3.55e-08 (2^-24.75)

Pareto front (feasible, 20 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round k=2] luts_plus_ffs=336, accuracy_bits=10.3, luts=246, ffs=90, throughput_msps=10.5, max_abs_err=0.00081 (2^-10.27), power_index=0.126
- unrolled_k [data_width=15 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=350, accuracy_bits=10.8, luts=257, ffs=94, throughput_msps=10.5, max_abs_err=0.000567 (2^-10.78), power_index=0.132
- unrolled_k [data_width=17 n_iter=23 angle_guard=3 frac_guard=0 rounding=round k=2] luts_plus_ffs=408, accuracy_bits=12.7, luts=304, ffs=104, throughput_msps=6.86, max_abs_err=0.000146 (2^-12.74), power_index=0.23
- unrolled_k [data_width=17 n_iter=26 angle_guard=2 frac_guard=4 rounding=trunc k=2] luts_plus_ffs=464, accuracy_bits=13.6, luts=353, ffs=111, throughput_msps=6.43, max_abs_err=8.01e-05 (2^-13.61), power_index=0.279
- unrolled_k [data_width=20 n_iter=20 angle_guard=3 frac_guard=0 rounding=round k=3] luts_plus_ffs=586, accuracy_bits=15.5, luts=468, ffs=118, throughput_msps=6.83, max_abs_err=2.17e-05 (2^-15.49), power_index=0.221
- unrolled_k [data_width=27 n_iter=21 angle_guard=0 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=668, accuracy_bits=19.8, luts=512, ffs=155, throughput_msps=7.01, max_abs_err=1.1e-06 (2^-19.79), power_index=0.352
- unrolled_k [data_width=25 n_iter=22 angle_guard=4 frac_guard=2 rounding=round k=2] luts_plus_ffs=701, accuracy_bits=20.5, luts=552, ffs=149, throughput_msps=7.01, max_abs_err=6.63e-07 (2^-20.52), power_index=0.369
- unrolled_k [data_width=28 n_iter=23 angle_guard=2 frac_guard=2 rounding=round k=2] luts_plus_ffs=773, accuracy_bits=21.8, luts=610, ffs=162, throughput_msps=6.54, max_abs_err=2.66e-07 (2^-21.84), power_index=0.436
- unrolled_k [data_width=28 n_iter=30 angle_guard=2 frac_guard=4 rounding=trunc k=3] luts_plus_ffs=949, accuracy_bits=24.3, luts=782, ffs=166, throughput_msps=5.01, max_abs_err=4.72e-08 (2^-24.34), power_index=0.464
- unrolled_k [data_width=28 n_iter=28 angle_guard=4 frac_guard=2 rounding=round k=4] luts_plus_ffs=1121, accuracy_bits=24.7, luts=957, ffs=163, throughput_msps=4.94, max_abs_err=3.55e-08 (2^-24.75), power_index=0.422
Front coverage: luts_plus_ffs 336..1121 (HV reference 1500); accuracy_bits 10.3..24.7 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- unrolled_k: 234 evals, 201 feasible; max throughput seen 13.5 MSPS; best accuracy 24.75 bits; best feasible luts_plus_ffs=336; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, k 2..8
- pipelined: 38 evals, 28 feasible; max throughput seen 282 MSPS; best accuracy 12.04 bits; best feasible luts_plus_ffs=1273; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 128 evals, 102 feasible; max throughput seen 178 MSPS; best accuracy 20.97 bits; best feasible luts_plus_ffs=868; feasible ranges: data_width 14..27, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..6
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 10017 in, 4969 out
- provider-reported cost: $0.0093
- full prompts and replies: `llm_trace.jsonl`

