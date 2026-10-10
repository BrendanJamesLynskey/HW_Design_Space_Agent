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
`iterative:data_width=15,n_iter=12,angle_guard=1,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 159 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 92 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 13.2 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 15 | exact: schedule |
| latency_ns | 75.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.141 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000917 (2^-10.09) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 7.51 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000249 (2^-11.97) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 2.04 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.1 | exact: bit-accurate model, exhaustive (32768 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 15 cycles, a new input every 15 cycle(s). DDS tone from its exact outputs: SFDR 79.8 dBc, SNR 69.5 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (30 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=12,angle_guard=1,frac_guard=0,rounding=round` | 159 | 92 | 13.2 | 15 | 0.141 | 0.000917 (2^-10.09) | 10.09 |
| 1 | `iterative:data_width=15,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` | 166 | 91 | 11.7 | 17 | 0.164 | 0.00081 (2^-10.27) | 10.27 |
| 2 | `iterative:data_width=15,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 168 | 92 | 11.7 | 17 | 0.166 | 0.000632 (2^-10.63) | 10.63 |
| 3 | `iterative:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` | 178 | 96 | 11.7 | 17 | 0.175 | 0.0004 (2^-11.29) | 11.29 |
| 4 | `iterative:data_width=16,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 179 | 97 | 10.4 | 19 | 0.197 | 0.000301 (2^-11.70) | 11.70 |
| 5 | `iterative:data_width=16,n_iter=19,angle_guard=2,frac_guard=0,rounding=round` | 196 | 99 | 7.4 | 22 | 0.244 | 0.000285 (2^-11.78) | 11.78 |
| 6 | `iterative:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=trunc` | 195 | 107 | 11.4 | 17 | 0.193 | 0.00024 (2^-12.03) | 12.03 |
| 7 | `iterative:data_width=17,n_iter=14,angle_guard=3,frac_guard=1,rounding=trunc` | 197 | 106 | 11.4 | 17 | 0.193 | 0.000231 (2^-12.08) | 12.08 |
| 8 | `iterative:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 202 | 107 | 11.4 | 17 | 0.198 | 0.000175 (2^-12.48) | 12.48 |
| 9 | `iterative:data_width=19,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc` | 208 | 113 | 10.2 | 19 | 0.229 | 8.56e-05 (2^-13.51) | 13.51 |
| 10 | `iterative:data_width=19,n_iter=16,angle_guard=3,frac_guard=0,rounding=round` | 217 | 114 | 10.2 | 19 | 0.237 | 5.41e-05 (2^-14.17) | 14.17 |
| 11 | `iterative:data_width=21,n_iter=16,angle_guard=4,frac_guard=0,rounding=round` | 242 | 125 | 10.0 | 19 | 0.262 | 3.63e-05 (2^-14.75) | 14.75 |
| 12 | `iterative:data_width=21,n_iter=24,angle_guard=1,frac_guard=0,rounding=trunc` | 266 | 123 | 5.9 | 27 | 0.396 | 2.58e-05 (2^-15.24) | 15.24 |
| 13 | `iterative:data_width=21,n_iter=23,angle_guard=4,frac_guard=0,rounding=trunc` | 272 | 126 | 6.0 | 26 | 0.389 | 2.36e-05 (2^-15.37) | 15.37 |
| 14 | `iterative:data_width=19,n_iter=23,angle_guard=2,frac_guard=3,rounding=trunc` | 280 | 120 | 6.1 | 26 | 0.391 | 2.18e-05 (2^-15.49) | 15.49 |
| 15 | `iterative:data_width=21,n_iter=23,angle_guard=0,frac_guard=1,rounding=trunc` | 280 | 124 | 6.1 | 26 | 0.395 | 1.69e-05 (2^-15.85) | 15.85 |
| 16 | `iterative:data_width=21,n_iter=24,angle_guard=1,frac_guard=1,rounding=trunc` | 282 | 125 | 5.9 | 27 | 0.413 | 1.38e-05 (2^-16.15) | 16.15 |
| 17 | `iterative:data_width=21,n_iter=23,angle_guard=4,frac_guard=0,rounding=round` | 285 | 126 | 6.0 | 26 | 0.402 | 1.15e-05 (2^-16.41) | 16.41 |
| 18 | `iterative:data_width=21,n_iter=28,angle_guard=1,frac_guard=3,rounding=trunc` | 316 | 129 | 5.0 | 31 | 0.52 | 1.05e-05 (2^-16.54) | 16.54 |
| 19 | `iterative:data_width=21,n_iter=24,angle_guard=4,frac_guard=3,rounding=trunc` | 319 | 132 | 5.8 | 27 | 0.458 | 4.53e-06 (2^-17.75) | 17.75 |
| 20 | `iterative:data_width=25,n_iter=29,angle_guard=2,frac_guard=0,rounding=trunc` | 343 | 144 | 4.8 | 32 | 0.586 | 1.91e-06 (2^-19.00) | 19.00 |
| 21 | `iterative:data_width=25,n_iter=25,angle_guard=1,frac_guard=0,rounding=round` | 356 | 143 | 5.6 | 28 | 0.526 | 1.05e-06 (2^-19.86) | 19.86 |
| 22 | `iterative:data_width=25,n_iter=23,angle_guard=4,frac_guard=0,rounding=round` | 355 | 146 | 5.9 | 26 | 0.491 | 8.49e-07 (2^-20.17) | 20.17 |
| 23 | `iterative:data_width=25,n_iter=25,angle_guard=1,frac_guard=2,rounding=trunc` | 375 | 147 | 5.5 | 28 | 0.55 | 6.67e-07 (2^-20.52) | 20.52 |
| 24 | `iterative:data_width=27,n_iter=24,angle_guard=1,frac_guard=0,rounding=trunc` | 371 | 153 | 5.7 | 27 | 0.533 | 4.31e-07 (2^-21.14) | 21.14 |
| 25 | `iterative:data_width=27,n_iter=23,angle_guard=1,frac_guard=1,rounding=trunc` | 387 | 155 | 5.9 | 26 | 0.53 | 4.09e-07 (2^-21.22) | 21.22 |
| 26 | `iterative:data_width=28,n_iter=24,angle_guard=1,frac_guard=0,rounding=trunc` | 389 | 158 | 5.7 | 27 | 0.556 | 2.99e-07 (2^-21.67) | 21.67 |
| 27 | `iterative:data_width=27,n_iter=28,angle_guard=1,frac_guard=0,rounding=round` | 394 | 153 | 4.9 | 31 | 0.638 | 2.33e-07 (2^-22.03) | 22.03 |
| 28 | `iterative:data_width=28,n_iter=24,angle_guard=2,frac_guard=0,rounding=round` | 404 | 159 | 5.7 | 27 | 0.572 | 1.98e-07 (2^-22.27) | 22.27 |
| 29 | `iterative:data_width=28,n_iter=27,angle_guard=3,frac_guard=4,rounding=trunc` | 470 | 168 | 5.0 | 30 | 0.721 | 4.23e-08 (2^-24.49) | 24.49 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands minimum area (LUTs+FFs) with throughput >= 1 MSPS and max error <= 2^-10. The iterative family is the most compact architecture and should dominate the Pareto front for area. With 10-14 iterations, the CORDIC convergence error is well below 2^-10, and data_width 11-16 gives sufficient precision. I focus 2/3 of the budget on iterative to map its area-accuracy trade-off, and 1/3 on unrolled_k to check if the latency/throughput benefit justifies the area cost. Pipelined variants are likely too area-hungry for this spec since area is the primary objective.*)
- `iterative` (67 evals): data_width=11..16, n_iter=10..14, angle_guard=0..1, frac_guard=0..1, rounding=round. *Why:* Iterative is the most area-efficient family; with 10-14 iterations and 11-16 bit width it should meet the 2^-10 error constraint while keeping LUTs+FFs minimal. Throughput at 100+ MHz easily exceeds 1 MSPS.
- `unrolled_k` (33 evals): data_width=11..16, n_iter=10..14, angle_guard=0..1, frac_guard=0..1, rounding=round, k=2..4. *Why:* Unrolled with k=2-4 reduces latency and may allow slightly higher Fmax, but adds area. Worth checking if the area penalty is acceptable for the throughput margin.

**Result (code):** 100 evaluations this round, 100 total; 55 feasible; hypervolume 1865 (n/a).

**LLM decision:** `add_family` — The current Pareto front is dominated by the `iterative` family, with a minimum area of 251 LUTs+FFs. However, the spec requires >= 1 MSPS throughput, which `iterative` meets only because its Fmax is high (13.2 MSPS). The `unrolled_k` family is significantly more expensive (min 336 LUTs+FFs) and offers no advantage over `iterative` in this low-area regime. The `pipelined` and `pipelined_m` families have not been explored. While `pipelined` typically has higher area due to registers, `pipelined_m` (registering every m stages) might offer a better area/throughput trade-off or allow for a higher Fmax that could enable a smaller data_width or n_iter configuration that meets the accuracy constraint with less area. More importantly, we have only explored 2 of 4 families. To ensure we are not missing a lower-area solution that meets the throughput constraint (especially if `iterative`'s Fmax drops for slightly different parameters or if a pipelined variant allows a more efficient datapath), we must explore the remaining families. The current front's area range (251-276) is narrow, and we have 300 evaluations left. Adding `pipelined_m` is the most logical next step as it interpolates between the low-area `iterative` and the high-throughput `pipelined`, potentially finding a sweet spot where the area is lower than `unrolled_k` but the throughput is robustly high, or simply confirming that `iterative` is indeed the best low-area option.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 1865 (gain this round: n/a (first round)).
Feasible designs: 55 of 100 evaluations (26 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: pipelined, pipelined_m.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 45% violate; best seen 0.000342 (2^-11.51)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=251, accuracy_bits=10.1, luts=159, ffs=92, throughput_msps=13.2, max_abs_err=0.000917 (2^-10.09), power_index=0.141
- iterative [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11.7, max_abs_err=0.00081 (2^-10.27), power_index=0.164
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.6, luts=168, ffs=92, throughput_msps=11.7, max_abs_err=0.000632 (2^-10.63), power_index=0.166
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.5, luts=179, ffs=97, throughput_msps=11.7, max_abs_err=0.000342 (2^-11.51), power_index=0.177
Front coverage: luts_plus_ffs 251..276 (HV reference 1500); accuracy_bits 10.1..11.5 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- iterative: 67 evals, 37 feasible; max throughput seen 15.6 MSPS; best accuracy 11.51 bits; best feasible luts_plus_ffs=251; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..1
- unrolled_k: 33 evals, 18 feasible; max throughput seen 14 MSPS; best accuracy 11.51 bits; best feasible luts_plus_ffs=336; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..1, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *We have 300 evals left. We will split them 50/50 between pipelined_m and pipelined, focusing on the narrow parameter ranges identified as feasible in Round 1 (data_width 14-16, n_iter 12-14, angle_guard 0-1, frac_guard 0-1, rounding=round). This ensures we are comparing the new families directly against the current best iterative designs in the same accuracy/throughput regime.*)
- `pipelined_m` (50 evals): data_width=14..16, n_iter=12..14, angle_guard=0..1, frac_guard=0..1, rounding=round, m=2..8. *Why:* Explore the middle ground between iterative and fully pipelined. The feasible region for iterative is narrow (data_width 14-16, n_iter 12-14). We test if pipelined_m can achieve similar or better area with guaranteed 1 result/cycle throughput, potentially allowing for a higher Fmax that might permit a smaller data_width if the critical path is broken up.
- `pipelined` (50 evals): data_width=14..16, n_iter=12..14, angle_guard=0..1, frac_guard=0..1, rounding=round. *Why:* Fully pipelined baseline. Although likely higher area, it is necessary to complete the family exploration and confirm the Pareto front's extent in the high-throughput/low-latency region, ensuring we haven't missed a design that trades area for a much higher Fmax which might allow a smaller data_width to meet accuracy.

**Result (code):** 100 evaluations this round, 200 total; 138 feasible; hypervolume 1938 (+3.9%).

**LLM decision:** `refine` — The Pareto front is dominated by the `iterative` family, which achieves the minimum area (251 LUTs+FFs) while meeting the throughput constraint (13.2 MSPS >= 1 MSPS) and accuracy constraint (10.1 bits >= 10 bits). The `pipelined` and `pipelined_m` families are significantly larger (788-1250 LUTs+FFs) and do not offer a trade-off benefit for this spec, as the throughput requirement is very low (1 MSPS) and `iterative` already provides 10-15 MSPS. The current front covers luts_plus_ffs 251..969, but the area objective is the primary driver for selection. To maximize hypervolume and find the true minimum area point, we should focus the search on the `iterative` family in the region where it is feasible and competitive. The feasible region for `iterative` is data_width 14..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..1. We will narrow the ranges slightly to focus on the high-accuracy, low-area corner of the `iterative` family, specifically targeting data_width 15-16 and n_iter 13-14 to see if we can push accuracy higher without increasing area, or if we can find a slightly smaller area configuration with data_width 15.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1938 (gain this round: +3.9%).
Feasible designs: 138 of 200 evaluations (72 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 273
- max_abs_err <= 0.000976562: 31% violate; best seen 0.000311 (2^-11.65)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=251, accuracy_bits=10.1, luts=159, ffs=92, throughput_msps=13.2, max_abs_err=0.000917 (2^-10.09), power_index=0.141
- iterative [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11.7, max_abs_err=0.00081 (2^-10.27), power_index=0.164
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.6, luts=168, ffs=92, throughput_msps=11.7, max_abs_err=0.000632 (2^-10.63), power_index=0.166
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.5, luts=179, ffs=97, throughput_msps=11.7, max_abs_err=0.000342 (2^-11.51), power_index=0.177
- pipelined_m [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=7] luts_plus_ffs=969, accuracy_bits=11.7, luts=820, ffs=149, throughput_msps=59.6, max_abs_err=0.000311 (2^-11.65), power_index=0.0365
- pipelined_m [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=8] luts_plus_ffs=969, accuracy_bits=11.7, luts=820, ffs=149, throughput_msps=52.7, max_abs_err=0.000311 (2^-11.65), power_index=0.0365
Front coverage: luts_plus_ffs 251..969 (HV reference 1500); accuracy_bits 10.1..11.7 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- iterative: 67 evals, 37 feasible; max throughput seen 15.6 MSPS; best accuracy 11.51 bits; best feasible luts_plus_ffs=251; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..1
- unrolled_k: 33 evals, 18 feasible; max throughput seen 14 MSPS; best accuracy 11.51 bits; best feasible luts_plus_ffs=336; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..1, k 2..4
- pipelined: 50 evals, 41 feasible; max throughput seen 273 MSPS; best accuracy 11.51 bits; best feasible luts_plus_ffs=1250; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..1
- pipelined_m: 50 evals, 42 feasible; max throughput seen 178 MSPS; best accuracy 11.65 bits; best feasible luts_plus_ffs=788; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..1, m 2..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The iterative family is the clear winner for area. The current front shows that data_width 15 with n_iter 12-14 is the sweet spot. By narrowing the search to this specific region, we can use the remaining budget to densely sample the Pareto front in the most relevant area, potentially finding a design with slightly better accuracy or lower area than the current best (251 LUTs+FFs). The other families are too large to be competitive for the 'min luts_plus_ffs' selection rule.*)
- `iterative` (40 evals): data_width=15..16, n_iter=13..14, angle_guard=0..1, frac_guard=0..1, rounding=round. *Why:* Focus on the best-performing family for area. Narrowing to data_width 15-16 and n_iter 13-14 targets the region where accuracy is sufficient and area is minimal. Rounding is fixed to 'round' as it generally provides better accuracy for the same area or allows for smaller widths.

**Result (code):** 40 evaluations this round, 240 total; 178 feasible; hypervolume 2030 (+4.7%).

**LLM decision:** `stop` — The Pareto front is well-established and dominated by the `iterative` family, which is optimal for the 'min luts_plus_ffs' objective given the throughput constraint. The best feasible design (iterative, W=15, N=12) achieves 251 LUTs+FFs with 10.1 bits of accuracy, comfortably meeting the max_abs_err <= 2^-10 constraint (0.000917 < 0.000976) and throughput >= 1 MSPS (13.2 MSPS). Other families (pipelined, pipelined_m, unrolled_k) offer higher throughput but at a significant area cost (788-1250+ LUTs+FFs), placing them far from the minimum area corner. Since the selection rule is 'min luts_plus_ffs', the iterative design at 251 is the clear winner. The front covers the relevant trade-off space for this specific spec (low area, moderate accuracy), and further exploration would only yield designs with higher area or negligible accuracy gains that do not change the selected design. The hypervolume gain in the last round was small (+4.7%), indicating convergence.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 2030 (gain this round: +4.7%).
Feasible designs: 178 of 240 evaluations (76 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 273
- max_abs_err <= 0.000976562: 26% violate; best seen 0.000311 (2^-11.65)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=251, accuracy_bits=10.1, luts=159, ffs=92, throughput_msps=13.2, max_abs_err=0.000917 (2^-10.09), power_index=0.141
- iterative [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11.7, max_abs_err=0.00081 (2^-10.27), power_index=0.164
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.6, luts=168, ffs=92, throughput_msps=11.7, max_abs_err=0.000632 (2^-10.63), power_index=0.166
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.3, luts=178, ffs=96, throughput_msps=11.7, max_abs_err=0.0004 (2^-11.29), power_index=0.175
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.5, luts=179, ffs=97, throughput_msps=11.7, max_abs_err=0.000342 (2^-11.51), power_index=0.177
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=round] luts_plus_ffs=322, accuracy_bits=11.7, luts=223, ffs=99, throughput_msps=11.7, max_abs_err=0.000311 (2^-11.65), power_index=0.206
Front coverage: luts_plus_ffs 251..322 (HV reference 1500); accuracy_bits 10.1..11.7 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- iterative: 107 evals, 77 feasible; max throughput seen 15.6 MSPS; best accuracy 11.65 bits; best feasible luts_plus_ffs=251; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..1
- unrolled_k: 33 evals, 18 feasible; max throughput seen 14 MSPS; best accuracy 11.51 bits; best feasible luts_plus_ffs=336; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..1, k 2..4
- pipelined: 50 evals, 41 feasible; max throughput seen 273 MSPS; best accuracy 11.51 bits; best feasible luts_plus_ffs=1250; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..1
- pipelined_m: 50 evals, 42 feasible; max throughput seen 178 MSPS; best accuracy 11.65 bits; best feasible luts_plus_ffs=788; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..1, m 2..8
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `iterative` (160 evals): data_width=14..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (6 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 322 feasible; hypervolume 1.527e+04 (+652.5%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and dominated by the `iterative` family, which is optimal for the 'min luts_plus_ffs' objective given the throughput constraint. The best feasible design (iterative, W=15, N=12) achieves 251 LUTs+FFs with 10.1 bits of accuracy, comfortably meeting the max_abs_err <= 2^-10 constraint (0.000917 < 0.000976) and throughput >= 1 MSPS (13.2 MSPS). Other families (pipelined, pipelined_m, unrolled_k) offer higher throughput but at a significant area cost (788-1250+ LUTs+FFs), placing them far from the minimum area corner. Since the selection rule is 'min luts_plus_ffs', the iterative design at 251 is the clear winner. The front covers the relevant trade-off space for this specific spec (low area, moderate accuracy), and further exploration would only yield designs with higher area or negligible accuracy gains that do not change the selected design. The hypervolume gain in the last round was small (+4.7%), indicating convergence.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.527e+04 (gain this round: +652.5%).
Feasible designs: 322 of 400 evaluations (205 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 273
- max_abs_err <= 0.000976562: 20% violate; best seen 4.23e-08 (2^-24.49)

Pareto front (feasible, 30 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=251, accuracy_bits=10.1, luts=159, ffs=92, throughput_msps=13.2, max_abs_err=0.000917 (2^-10.09), power_index=0.141
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.3, luts=178, ffs=96, throughput_msps=11.7, max_abs_err=0.0004 (2^-11.29), power_index=0.175
- iterative [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=302, accuracy_bits=12, luts=195, ffs=107, throughput_msps=11.4, max_abs_err=0.00024 (2^-12.03), power_index=0.193
- iterative [data_width=19 n_iter=16 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=331, accuracy_bits=14.2, luts=217, ffs=114, throughput_msps=10.2, max_abs_err=5.41e-05 (2^-14.17), power_index=0.237
- iterative [data_width=21 n_iter=23 angle_guard=4 frac_guard=0 rounding=trunc] luts_plus_ffs=398, accuracy_bits=15.4, luts=272, ffs=126, throughput_msps=6, max_abs_err=2.36e-05 (2^-15.37), power_index=0.389
- iterative [data_width=21 n_iter=24 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=407, accuracy_bits=16.1, luts=282, ffs=125, throughput_msps=5.89, max_abs_err=1.38e-05 (2^-16.15), power_index=0.413
- iterative [data_width=21 n_iter=24 angle_guard=4 frac_guard=3 rounding=trunc] luts_plus_ffs=451, accuracy_bits=17.8, luts=319, ffs=132, throughput_msps=5.78, max_abs_err=4.53e-06 (2^-17.75), power_index=0.458
- iterative [data_width=25 n_iter=25 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=523, accuracy_bits=20.5, luts=375, ffs=147, throughput_msps=5.47, max_abs_err=6.67e-07 (2^-20.52), power_index=0.55
- iterative [data_width=28 n_iter=24 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=547, accuracy_bits=21.7, luts=389, ffs=158, throughput_msps=5.68, max_abs_err=2.99e-07 (2^-21.67), power_index=0.556
- iterative [data_width=28 n_iter=27 angle_guard=3 frac_guard=4 rounding=trunc] luts_plus_ffs=639, accuracy_bits=24.5, luts=470, ffs=168, throughput_msps=5.02, max_abs_err=4.23e-08 (2^-24.49), power_index=0.721
Front coverage: luts_plus_ffs 251..639 (HV reference 1500); accuracy_bits 10.1..24.5 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 267 evals, 221 feasible; max throughput seen 15.6 MSPS; best accuracy 24.49 bits; best feasible luts_plus_ffs=251; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 33 evals, 18 feasible; max throughput seen 14 MSPS; best accuracy 11.51 bits; best feasible luts_plus_ffs=336; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..1, k 2..4
- pipelined: 50 evals, 41 feasible; max throughput seen 273 MSPS; best accuracy 11.51 bits; best feasible luts_plus_ffs=1250; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..1
- pipelined_m: 50 evals, 42 feasible; max throughput seen 178 MSPS; best accuracy 11.65 bits; best feasible luts_plus_ffs=788; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..1, m 2..8
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 23690 in, 3248 out
- provider-reported cost: $0.0091
- full prompts and replies: `llm_trace.jsonl`

