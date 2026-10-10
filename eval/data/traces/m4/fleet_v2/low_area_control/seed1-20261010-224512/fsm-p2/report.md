# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
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
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=15,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 166 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 91 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 11.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 85.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.164 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00081 (2^-10.27) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.64 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00021 (2^-12.22) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.72 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (30 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 166 | 91 | 11.0 | 18 | 0.174 | 0.00081 (2^-10.27) | 10.27 |
| 1 | `iterative:data_width=15,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` | 166 | 91 | 11.7 | 17 | 0.164 | 0.00081 (2^-10.27) | 10.27 |
| 2 | `iterative:data_width=15,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 168 | 92 | 11.0 | 18 | 0.176 | 0.000632 (2^-10.63) | 10.63 |
| 3 | `iterative:data_width=16,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 178 | 96 | 10.4 | 19 | 0.195 | 0.000373 (2^-11.39) | 11.39 |
| 4 | `iterative:data_width=16,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 179 | 97 | 11.0 | 18 | 0.187 | 0.000301 (2^-11.70) | 11.70 |
| 5 | `iterative:data_width=16,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 179 | 97 | 10.4 | 19 | 0.197 | 0.000301 (2^-11.70) | 11.70 |
| 6 | `iterative:data_width=16,n_iter=16,angle_guard=4,frac_guard=0,rounding=round` | 185 | 100 | 10.2 | 19 | 0.203 | 0.000285 (2^-11.78) | 11.78 |
| 7 | `iterative:data_width=17,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 189 | 101 | 11.0 | 18 | 0.196 | 0.000251 (2^-11.96) | 11.96 |
| 8 | `iterative:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 191 | 102 | 11.0 | 18 | 0.198 | 0.000168 (2^-12.54) | 12.54 |
| 9 | `iterative:data_width=17,n_iter=16,angle_guard=3,frac_guard=0,rounding=round` | 194 | 104 | 10.2 | 19 | 0.213 | 0.000146 (2^-12.74) | 12.74 |
| 10 | `iterative:data_width=18,n_iter=15,angle_guard=3,frac_guard=0,rounding=round` | 206 | 109 | 10.8 | 18 | 0.213 | 0.000119 (2^-13.04) | 13.04 |
| 11 | `iterative:data_width=18,n_iter=15,angle_guard=4,frac_guard=0,rounding=round` | 208 | 110 | 10.8 | 18 | 0.215 | 0.000106 (2^-13.20) | 13.20 |
| 12 | `iterative:data_width=20,n_iter=16,angle_guard=3,frac_guard=0,rounding=round` | 229 | 119 | 10.0 | 19 | 0.249 | 4.33e-05 (2^-14.50) | 14.50 |
| 13 | `iterative:data_width=22,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc` | 239 | 126 | 10.2 | 19 | 0.261 | 3.87e-05 (2^-14.66) | 14.66 |
| 14 | `iterative:data_width=20,n_iter=26,angle_guard=1,frac_guard=0,rounding=round` | 264 | 118 | 5.5 | 29 | 0.417 | 2.52e-05 (2^-15.28) | 15.28 |
| 15 | `iterative:data_width=21,n_iter=22,angle_guard=0,frac_guard=0,rounding=round` | 278 | 122 | 6.4 | 25 | 0.376 | 1.79e-05 (2^-15.77) | 15.77 |
| 16 | `iterative:data_width=19,n_iter=21,angle_guard=4,frac_guard=3,rounding=trunc` | 284 | 122 | 6.5 | 24 | 0.366 | 1.76e-05 (2^-15.79) | 15.79 |
| 17 | `iterative:data_width=22,n_iter=21,angle_guard=-1,frac_guard=0,rounding=trunc` | 280 | 126 | 6.6 | 24 | 0.367 | 1.68e-05 (2^-15.86) | 15.86 |
| 18 | `iterative:data_width=22,n_iter=24,angle_guard=0,frac_guard=0,rounding=trunc` | 282 | 127 | 5.9 | 27 | 0.416 | 1.39e-05 (2^-16.14) | 16.14 |
| 19 | `iterative:data_width=22,n_iter=21,angle_guard=1,frac_guard=0,rounding=trunc` | 284 | 128 | 6.5 | 24 | 0.372 | 1.22e-05 (2^-16.32) | 16.32 |
| 20 | `iterative:data_width=22,n_iter=26,angle_guard=1,frac_guard=0,rounding=round` | 299 | 128 | 5.4 | 29 | 0.466 | 6.76e-06 (2^-17.17) | 17.17 |
| 21 | `iterative:data_width=22,n_iter=24,angle_guard=3,frac_guard=0,rounding=round` | 301 | 130 | 5.8 | 27 | 0.438 | 5.23e-06 (2^-17.54) | 17.54 |
| 22 | `iterative:data_width=22,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc` | 339 | 136 | 5.4 | 29 | 0.518 | 2.39e-06 (2^-18.67) | 18.67 |
| 23 | `iterative:data_width=25,n_iter=22,angle_guard=1,frac_guard=0,rounding=trunc` | 336 | 143 | 6.2 | 25 | 0.451 | 1.63e-06 (2^-19.23) | 19.23 |
| 24 | `iterative:data_width=25,n_iter=22,angle_guard=0,frac_guard=0,rounding=round` | 348 | 142 | 6.2 | 25 | 0.461 | 1.51e-06 (2^-19.34) | 19.34 |
| 25 | `iterative:data_width=25,n_iter=22,angle_guard=1,frac_guard=0,rounding=round` | 350 | 143 | 6.2 | 25 | 0.464 | 1.41e-06 (2^-19.44) | 19.44 |
| 26 | `iterative:data_width=26,n_iter=29,angle_guard=3,frac_guard=0,rounding=round` | 380 | 150 | 4.8 | 32 | 0.638 | 3.6e-07 (2^-21.40) | 21.40 |
| 27 | `iterative:data_width=27,n_iter=26,angle_guard=1,frac_guard=0,rounding=round` | 394 | 153 | 5.3 | 29 | 0.597 | 2.33e-07 (2^-22.03) | 22.03 |
| 28 | `iterative:data_width=27,n_iter=24,angle_guard=4,frac_guard=2,rounding=round` | 479 | 160 | 5.6 | 27 | 0.649 | 1.63e-07 (2^-22.55) | 22.55 |
| 29 | `iterative:data_width=27,n_iter=26,angle_guard=1,frac_guard=2,rounding=round` | 485 | 157 | 5.3 | 29 | 0.701 | 1.48e-07 (2^-22.69) | 22.69 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The merged front is entirely owned by iterative (13/13 designs, best area 257). unrolled_k, pipelined, and pipelined_m have zero front membership, confirming iterative is the dominant family for this area-minimising spec. My plan therefore concentrates 55% of the budget on iterative, narrowing the search to the data_width/n_iter 12-18 region where accuracy_bits can be pushed toward the HV reference of 10 while keeping luts_plus_ffs near the current best of 257. The remaining 45% goes to unrolled_k with k restricted to 2-4, to either find a few non-dominated points that extend the front (e.g., slightly higher area but notably higher accuracy_bits) or to confirm it cannot compete. Both families share the same accuracy model, so the data_width/n_iter/guard ranges are identical; the only structural difference is k, which affects area and throughput but not accuracy. The throughput constraint (>=1 MSPS) is non-binding for both families at these parameter values since even iterative at N=18 gives ~5.5 cycles/result, and at a conservative 100 MHz that is ~18 MSPS. The binding constraints are max_abs_err <= 2^-10 and the area objective, both of which are addressed by the focused ranges.*)
- `iterative` (55 evals): data_width=12..18, n_iter=12..18, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* iterative already owns the entire merged front (13/13) with best luts_plus_ffs=257, so it is the only family that can plausibly improve the min-area objective. The previous search was broad; I now focus on the region where accuracy_bits is maximised for a given area: data_width 12-18 and n_iter 12-18 are the sweet spot where max_abs_err <= 2^-10 is met with minimal guard bits. Keeping angle_guard and frac_guard in their full ranges lets Optuna find the exact minimal-guard combinations that push accuracy_bits toward 10+ while keeping luts_plus_ffs near 257. The throughput constraint (>=1 MSPS) is easily met by iterative at reasonable Fmax since 1 result per N+3 cycles at ~100+ MHz gives >1 MSPS for N<=18.
- `unrolled_k` (45 evals): data_width=12..18, n_iter=12..18, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..4. *Why:* unrolled_k has 0 designs on the merged front and best luts_plus_ffs=362, well above iterative's 257. However, it has 29 feasible designs out of 38 evals, so it is not dead. The key question is whether a smaller k (2-4) with tighter data_width/n_iter can close the area gap. I restrict k to 2-4 (k=5-8 adds area without helping the area objective) and focus data_width/n_iter on 12-18 to match the accuracy sweet spot. This is a secondary exploration to confirm whether unrolled_k can contribute any non-dominated points or to definitively rule it out, freeing the front for iterative-only coverage.

**Result (code):** 100 evaluations this round, 100 total; 70 feasible; hypervolume 3855 (n/a).

**LLM decision:** `add_family` — Round 1 found 8 feasible Pareto designs, all iterative or unrolled_k, with luts_plus_ffs 257-405 and accuracy 10.3-13.2 bits. The minimum-area design is iterative at 257 LUTs+FFs with 10.3 bits accuracy and 11 MSPS throughput. However, pipelined and pipelined_m families remain unexplored. These families produce 1 result/cycle, which may allow different area/throughput trade-offs. Since the spec prioritizes area (min luts_plus_ffs) with a loose throughput constraint (>=1 MSPS, easily met at 10+ MSPS), pipeline architectures could potentially reduce area by simplifying the datapath or improving Fmax. The accuracy constraint is comfortably met (best 13.2 bits vs required 10 bits), so there is room to trade accuracy for area if pipeline designs offer lower luts_plus_ffs. I will allocate 50% of the remaining 100 evals to pipelined and 50% to pipelined_m, focusing on the data_width 14-18 and n_iter 12-18 ranges where iterative found feasible designs, with angle_guard -1..2 and frac_guard 0..1 to keep area low while maintaining accuracy >=10 bits.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 3855 (gain this round: n/a (first round)).
Feasible designs: 70 of 100 evaluations (59 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 13.2
- max_abs_err <= 0.000976562: 30% violate; best seen 0.000108 (2^-13.18)

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11, max_abs_err=0.00081 (2^-10.27), power_index=0.174
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.6, luts=168, ffs=92, throughput_msps=11, max_abs_err=0.000632 (2^-10.63), power_index=0.176
- iterative [data_width=16 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.4, luts=178, ffs=96, throughput_msps=10.4, max_abs_err=0.000373 (2^-11.39), power_index=0.195
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.7, luts=179, ffs=97, throughput_msps=11, max_abs_err=0.000301 (2^-11.70), power_index=0.187
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=293, accuracy_bits=12.5, luts=191, ffs=102, throughput_msps=11, max_abs_err=0.000168 (2^-12.54), power_index=0.198
- iterative [data_width=17 n_iter=16 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=298, accuracy_bits=12.7, luts=194, ffs=104, throughput_msps=10.2, max_abs_err=0.000146 (2^-12.74), power_index=0.213
- iterative [data_width=16 n_iter=16 angle_guard=4 frac_guard=2 rounding=round] luts_plus_ffs=342, accuracy_bits=13.2, luts=238, ffs=104, throughput_msps=10.2, max_abs_err=0.000109 (2^-13.17), power_index=0.244
- unrolled_k [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round k=2] luts_plus_ffs=405, accuracy_bits=13.2, luts=299, ffs=106, throughput_msps=9.35, max_abs_err=0.000108 (2^-13.18), power_index=0.167
Front coverage: luts_plus_ffs 257..405 (HV reference 1500); accuracy_bits 10.3..13.2 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 55 evals, 41 feasible; max throughput seen 13.2 MSPS; best accuracy 13.17 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 14..18, n_iter 12..18, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 45 evals, 29 feasible; max throughput seen 11.7 MSPS; best accuracy 13.18 bits; best feasible luts_plus_ffs=340; feasible ranges: data_width 14..18, n_iter 12..18, angle_guard -2..3, frac_guard 0..4, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The current front is dominated by iterative (7 of 8 designs) with luts_plus_ffs 257-342 and throughput 10-11 MSPS. The spec requires >=1 MSPS (easily met) and min area. Pipelined families have not been explored; they offer 1 result/cycle throughput which may allow higher Fmax or lower area trade-offs. The accuracy constraint (<=2^-10) is met by all front designs (10.3-13.2 bits), so area is the binding objective. Exploring pipelined/pipelined_m in the same data_width/n_iter ranges (14-18, 12-18) where iterative found feasible designs will reveal if pipeline architectures can achieve lower luts_plus_ffs while maintaining throughput >=1 MSPS. Rounding fixed to 'round' since all front designs use it and it gives better accuracy per bit-width. angle_guard narrowed to -1..2 and frac_guard to 0..1 since the front shows angle_guard 0-1 and frac_guard 0 are optimal for area; higher guards add area without needed accuracy.*)
- `iterative` (10 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (10 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 20 evaluations this round, 120 total; 85 feasible; hypervolume 1.221e+04 (+216.6%).

**LLM decision:** `stop` — The constraints are met (0% throughput violations, best accuracy 21.48 bits vs 10-bit requirement) and the Pareto front is well-populated with 13 feasible designs spanning luts_plus_ffs 257..1098 and accuracy_bits 10.3..21.5. The selection rule (min luts_plus_ffs) is satisfied by the iterative design at 257 LUTs+FFs with 10.3 bits accuracy and 11 MSPS throughput. The front covers the full trade-off curve from the area-optimal corner to the accuracy-optimal corner, and the hypervolume gain of +216.6% in this round confirms the front is well-mapped. Since this is the final round, the current front is sufficient for selection.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.221e+04 (gain this round: +216.6%).
Feasible designs: 85 of 120 evaluations (73 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 26.8
- max_abs_err <= 0.000976562: 29% violate; best seen 3.41e-07 (2^-21.48)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11, max_abs_err=0.00081 (2^-10.27), power_index=0.174
- iterative [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11.7, max_abs_err=0.00081 (2^-10.27), power_index=0.164
- iterative [data_width=16 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.4, luts=178, ffs=96, throughput_msps=10.4, max_abs_err=0.000373 (2^-11.39), power_index=0.195
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.7, luts=179, ffs=97, throughput_msps=11, max_abs_err=0.000301 (2^-11.70), power_index=0.187
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=293, accuracy_bits=12.5, luts=191, ffs=102, throughput_msps=11, max_abs_err=0.000168 (2^-12.54), power_index=0.198
- iterative [data_width=16 n_iter=16 angle_guard=4 frac_guard=2 rounding=round] luts_plus_ffs=342, accuracy_bits=13.2, luts=238, ffs=104, throughput_msps=10.2, max_abs_err=0.000109 (2^-13.17), power_index=0.244
- unrolled_k [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round k=2] luts_plus_ffs=405, accuracy_bits=13.2, luts=299, ffs=106, throughput_msps=9.35, max_abs_err=0.000108 (2^-13.18), power_index=0.167
- iterative [data_width=22 n_iter=21 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=406, accuracy_bits=15.9, luts=280, ffs=126, throughput_msps=6.62, max_abs_err=1.68e-05 (2^-15.86), power_index=0.367
- iterative [data_width=26 n_iter=29 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=530, accuracy_bits=21.4, luts=380, ffs=150, throughput_msps=4.79, max_abs_err=3.6e-07 (2^-21.40), power_index=0.638
- unrolled_k [data_width=25 n_iter=24 angle_guard=3 frac_guard=2 rounding=round k=5] luts_plus_ffs=1098, accuracy_bits=21.5, luts=951, ffs=147, throughput_msps=5.08, max_abs_err=3.41e-07 (2^-21.48), power_index=0.331
Front coverage: luts_plus_ffs 257..1098 (HV reference 1500); accuracy_bits 10.3..21.5 (HV reference 10); data_width on the front 15..26 (registry 8..28).

Per family:
- iterative: 65 evals, 48 feasible; max throughput seen 13.2 MSPS; best accuracy 21.40 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 14..27, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 55 evals, 37 feasible; max throughput seen 26.8 MSPS; best accuracy 21.48 bits; best feasible luts_plus_ffs=340; feasible ranges: data_width 14..25, n_iter 12..27, angle_guard -2..4, frac_guard 0..4, k 2..5
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `iterative` (68 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (11 front designs; box front_anchored)
- `unrolled_k` (12 evals): data_width=17..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (2 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 161 feasible; hypervolume 1.372e+04 (+12.4%).

**No LLM call** (code's front-mapping round): The constraints are met (0% throughput violations, best accuracy 21.48 bits vs 10-bit requirement) and the Pareto front is well-populated with 13 feasible designs spanning luts_plus_ffs 257..1098 and accuracy_bits 10.3..21.5. The selection rule (min luts_plus_ffs) is satisfied by the iterative design at 257 LUTs+FFs with 10.3 bits accuracy and 11 MSPS throughput. The front covers the full trade-off curve from the area-optimal corner to the accuracy-optimal corner, and the hypervolume gain of +216.6% in this round confirms the front is well-mapped. Since this is the final round, the current front is sufficient for selection.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.372e+04 (gain this round: +12.4%).
Feasible designs: 161 of 200 evaluations (138 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 26.8
- max_abs_err <= 0.000976562: 20% violate; best seen 1.48e-07 (2^-22.69)

Pareto front (feasible, 30 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11, max_abs_err=0.00081 (2^-10.27), power_index=0.174
- iterative [data_width=16 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.4, luts=178, ffs=96, throughput_msps=10.4, max_abs_err=0.000373 (2^-11.39), power_index=0.195
- iterative [data_width=16 n_iter=16 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=285, accuracy_bits=11.8, luts=185, ffs=100, throughput_msps=10.2, max_abs_err=0.000285 (2^-11.78), power_index=0.203
- iterative [data_width=18 n_iter=15 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=315, accuracy_bits=13, luts=206, ffs=109, throughput_msps=10.8, max_abs_err=0.000119 (2^-13.04), power_index=0.213
- iterative [data_width=22 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=365, accuracy_bits=14.7, luts=239, ffs=126, throughput_msps=10.2, max_abs_err=3.87e-05 (2^-14.66), power_index=0.261
- iterative [data_width=19 n_iter=21 angle_guard=4 frac_guard=3 rounding=trunc] luts_plus_ffs=406, accuracy_bits=15.8, luts=284, ffs=122, throughput_msps=6.5, max_abs_err=1.76e-05 (2^-15.79), power_index=0.366
- iterative [data_width=22 n_iter=21 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=412, accuracy_bits=16.3, luts=284, ffs=128, throughput_msps=6.5, max_abs_err=1.22e-05 (2^-16.32), power_index=0.372
- iterative [data_width=25 n_iter=22 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=480, accuracy_bits=19.2, luts=336, ffs=143, throughput_msps=6.24, max_abs_err=1.63e-06 (2^-19.23), power_index=0.451
- iterative [data_width=26 n_iter=29 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=530, accuracy_bits=21.4, luts=380, ffs=150, throughput_msps=4.79, max_abs_err=3.6e-07 (2^-21.40), power_index=0.638
- iterative [data_width=27 n_iter=26 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=643, accuracy_bits=22.7, luts=485, ffs=157, throughput_msps=5.28, max_abs_err=1.48e-07 (2^-22.69), power_index=0.701
Front coverage: luts_plus_ffs 257..643 (HV reference 1500); accuracy_bits 10.3..22.7 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 133 evals, 112 feasible; max throughput seen 13.2 MSPS; best accuracy 22.69 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 14..27, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 67 evals, 49 feasible; max throughput seen 26.8 MSPS; best accuracy 21.48 bits; best feasible luts_plus_ffs=340; feasible ranges: data_width 14..25, n_iter 12..27, angle_guard -2..4, frac_guard 0..4, k 2..5
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8266 in, 2576 out
- provider-reported cost: $0.0040
- full prompts and replies: `llm_trace.jsonl`

