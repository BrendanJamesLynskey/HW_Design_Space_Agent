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
`iterative:data_width=16,n_iter=12,angle_guard=0,frac_guard=1,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 169 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 98 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 13.2 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 15 | exact: schedule |
| latency_ns | 75.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.151 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000711 (2^-10.46) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 11.7 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000214 (2^-12.19) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 3.51 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.5 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (27 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=16,n_iter=12,angle_guard=0,frac_guard=1,rounding=trunc` | 169 | 98 | 13.2 | 15 | 0.151 | 0.000711 (2^-10.46) | 10.46 |
| 1 | `iterative:data_width=16,n_iter=14,angle_guard=-1,frac_guard=0,rounding=round` | 176 | 95 | 11.7 | 17 | 0.173 | 0.000706 (2^-10.47) | 10.47 |
| 2 | `iterative:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` | 178 | 96 | 11.7 | 17 | 0.175 | 0.0004 (2^-11.29) | 11.29 |
| 3 | `iterative:data_width=16,n_iter=14,angle_guard=3,frac_guard=0,rounding=round` | 183 | 99 | 11.4 | 17 | 0.18 | 0.000294 (2^-11.73) | 11.73 |
| 4 | `iterative:data_width=16,n_iter=24,angle_guard=3,frac_guard=0,rounding=round` | 199 | 100 | 5.9 | 27 | 0.304 | 0.000285 (2^-11.78) | 11.78 |
| 5 | `iterative:data_width=18,n_iter=27,angle_guard=2,frac_guard=0,rounding=trunc` | 216 | 109 | 5.3 | 30 | 0.366 | 0.000277 (2^-11.82) | 11.82 |
| 6 | `iterative:data_width=18,n_iter=17,angle_guard=3,frac_guard=0,rounding=trunc` | 217 | 110 | 7.9 | 20 | 0.246 | 0.000187 (2^-12.38) | 12.38 |
| 7 | `iterative:data_width=17,n_iter=24,angle_guard=2,frac_guard=2,rounding=trunc` | 230 | 108 | 5.9 | 27 | 0.343 | 0.00013 (2^-12.91) | 12.91 |
| 8 | `iterative:data_width=17,n_iter=24,angle_guard=4,frac_guard=2,rounding=trunc` | 233 | 110 | 5.9 | 27 | 0.349 | 0.000114 (2^-13.10) | 13.10 |
| 9 | `iterative:data_width=19,n_iter=21,angle_guard=1,frac_guard=0,rounding=trunc` | 231 | 113 | 6.6 | 24 | 0.311 | 8.6e-05 (2^-13.51) | 13.51 |
| 10 | `iterative:data_width=21,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 235 | 121 | 10.8 | 18 | 0.241 | 6.94e-05 (2^-13.81) | 13.81 |
| 11 | `iterative:data_width=20,n_iter=24,angle_guard=0,frac_guard=0,rounding=trunc` | 247 | 117 | 5.9 | 27 | 0.37 | 5.66e-05 (2^-14.11) | 14.11 |
| 12 | `iterative:data_width=18,n_iter=24,angle_guard=2,frac_guard=3,rounding=trunc` | 263 | 115 | 5.9 | 27 | 0.384 | 4.69e-05 (2^-14.38) | 14.38 |
| 13 | `iterative:data_width=20,n_iter=20,angle_guard=3,frac_guard=0,rounding=round` | 262 | 120 | 6.8 | 23 | 0.33 | 2.17e-05 (2^-15.49) | 15.49 |
| 14 | `iterative:data_width=21,n_iter=25,angle_guard=3,frac_guard=1,rounding=trunc` | 286 | 127 | 5.6 | 28 | 0.435 | 1.38e-05 (2^-16.14) | 16.14 |
| 15 | `iterative:data_width=21,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc` | 320 | 131 | 5.4 | 29 | 0.492 | 5.08e-06 (2^-17.59) | 17.59 |
| 16 | `iterative:data_width=24,n_iter=24,angle_guard=0,frac_guard=0,rounding=trunc` | 317 | 137 | 5.8 | 27 | 0.461 | 3.11e-06 (2^-18.30) | 18.30 |
| 17 | `iterative:data_width=24,n_iter=24,angle_guard=0,frac_guard=2,rounding=trunc` | 348 | 141 | 5.8 | 27 | 0.497 | 2.03e-06 (2^-18.91) | 18.91 |
| 18 | `iterative:data_width=25,n_iter=24,angle_guard=0,frac_guard=0,rounding=round` | 348 | 142 | 5.8 | 27 | 0.498 | 1.37e-06 (2^-19.48) | 19.48 |
| 19 | `iterative:data_width=25,n_iter=24,angle_guard=0,frac_guard=2,rounding=trunc` | 366 | 146 | 5.7 | 27 | 0.52 | 9.91e-07 (2^-19.94) | 19.94 |
| 20 | `iterative:data_width=27,n_iter=26,angle_guard=1,frac_guard=0,rounding=round` | 394 | 153 | 5.3 | 29 | 0.597 | 2.33e-07 (2^-22.03) | 22.03 |
| 21 | `iterative:data_width=28,n_iter=26,angle_guard=0,frac_guard=1,rounding=trunc` | 413 | 159 | 5.3 | 29 | 0.625 | 1.6e-07 (2^-22.58) | 22.58 |
| 22 | `iterative:data_width=28,n_iter=30,angle_guard=2,frac_guard=0,rounding=round` | 419 | 159 | 4.6 | 33 | 0.718 | 1.02e-07 (2^-23.23) | 23.23 |
| 23 | `iterative:data_width=28,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc` | 453 | 166 | 5.2 | 29 | 0.676 | 5.73e-08 (2^-24.06) | 24.06 |
| 24 | `iterative:data_width=28,n_iter=26,angle_guard=3,frac_guard=3,rounding=round` | 527 | 166 | 5.2 | 29 | 0.757 | 4.85e-08 (2^-24.30) | 24.30 |
| 25 | `iterative:data_width=28,n_iter=30,angle_guard=2,frac_guard=3,rounding=round` | 534 | 165 | 4.6 | 33 | 0.869 | 4.14e-08 (2^-24.53) | 24.53 |
| 26 | `iterative:data_width=28,n_iter=30,angle_guard=3,frac_guard=3,rounding=round` | 536 | 166 | 4.6 | 33 | 0.872 | 2.91e-08 (2^-25.04) | 25.04 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *iterative is the clear winner on the merged front (18/18 designs, best area 295) and is the only family I can use that meets the 1 MSPS throughput constraint; unrolled_k is the only other family I can use that meets it, but it has 0 front designs and a higher best area (390). I focus the budget on iterative to densely map the low-area/accuracy trade-off curve, and spend a smaller share on unrolled_k to confirm it cannot beat iterative. I narrow data_width to 12-16 and n_iter to 10-16 to satisfy the 2^-10 error constraint while keeping area minimal, and keep angle_guard/frac_guard low to minimise LUTs.*)
- `iterative` (60 evals): data_width=12..16, n_iter=10..16, angle_guard=-2..0, frac_guard=0..1, rounding=trunc|round. *Why:* iterative dominates the merged front (18/18 designs) and is the only family I can use that meets the 1 MSPS constraint; refine the low-area corner to map the front.
- `unrolled_k` (40 evals): data_width=12..16, n_iter=10..16, angle_guard=-2..0, frac_guard=0..1, rounding=trunc|round, k=2..4. *Why:* unrolled_k is the only other family I can use that meets the throughput constraint; it has 0 front designs so far, so I probe whether any k/width combo beats iterative's 295 area.

**Result (code):** 100 evaluations this round, 100 total; 29 feasible; hypervolume 1628 (n/a).

**LLM decision:** `add_family` — The current Pareto front is dominated by the `iterative` family (best area 267 LUTs+FFs), but `iterative` designs are latency-bound (N+3 cycles). While they meet the throughput constraint (min 13.2 MSPS), they are not the most area-efficient architecture for a 1 MSPS requirement. The `pipelined` and `pipelined_m` families allow for 1 result/cycle throughput, which decouples the cycle time from the iteration count. This typically allows for a much lower Fmax (reducing power and potentially allowing for more relaxed timing that might map to fewer LUTs/FFs in the cost model, or simply a different area/latency trade-off) and often results in a different area profile. Furthermore, `unrolled_k` has been explored and found to be inferior in area (best 365 vs 267). To map the true feasible Pareto front for 'min luts_plus_ffs', we must explore the pipelined architectures which have not been evaluated yet. The accuracy constraint (<= 2^-10) is easily met by the current designs (best 2^-11.33), so the focus should be on finding if pipelined structures offer a lower area solution for the same accuracy.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1628 (gain this round: n/a (first round)).
Feasible designs: 29 of 100 evaluations (14 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.3
- max_abs_err <= 0.000976562: 71% violate; best seen 0.000389 (2^-11.33)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=12 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=267, accuracy_bits=10.5, luts=169, ffs=98, throughput_msps=13.2, max_abs_err=0.000711 (2^-10.46), power_index=0.151
- iterative [data_width=16 n_iter=14 angle_guard=-1 frac_guard=0 rounding=round] luts_plus_ffs=271, accuracy_bits=10.5, luts=176, ffs=95, throughput_msps=11.7, max_abs_err=0.000706 (2^-10.47), power_index=0.173
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.3, luts=178, ffs=96, throughput_msps=11.7, max_abs_err=0.0004 (2^-11.29), power_index=0.175
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=1 rounding=round] luts_plus_ffs=319, accuracy_bits=11.3, luts=221, ffs=98, throughput_msps=11.7, max_abs_err=0.000389 (2^-11.33), power_index=0.204
Front coverage: luts_plus_ffs 267..319 (HV reference 1500); accuracy_bits 10.5..11.3 (HV reference 10); data_width on the front 16..16 (registry 8..28).

Per family:
- iterative: 60 evals, 25 feasible; max throughput seen 15.3 MSPS; best accuracy 11.33 bits; best feasible luts_plus_ffs=267; feasible ranges: data_width 15..16, n_iter 12..15, angle_guard -1..0, frac_guard 0..1
- unrolled_k: 40 evals, 4 feasible; max throughput seen 14 MSPS; best accuracy 10.51 bits; best feasible luts_plus_ffs=365; feasible ranges: data_width 16..16, n_iter 12..14, angle_guard -1..-1, frac_guard 0..1, k 3..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Adding pipelined family to explore area trade-offs not available in iterative/unrolled_k.*)
- `iterative` (10 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (10 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 20 evaluations this round, 120 total; 47 feasible; hypervolume 1.291e+04 (+692.6%).

**LLM decision:** `stop` — The constraints are met: 100% of feasible designs satisfy throughput >= 1 MSPS (best 19 MSPS) and max_abs_err <= 2^-10 (best 2^-22.29). The Pareto front is well-populated with 10 designs spanning luts_plus_ffs 267..629 and accuracy_bits 10.5..22.3, covering the full trade-off curve from the area-optimal corner (iterative W=16, N=12, 267 LUTs+FFs) to the accuracy-optimal corner. The selection rule (min luts_plus_ffs) picks the iterative design at 267 LUTs+FFs with 10.5 bits accuracy and 13.2 MSPS throughput, which comfortably satisfies the spec. The front is mature and the hypervolume is strong; no further exploration is warranted in the final round.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.291e+04 (gain this round: +692.6%).
Feasible designs: 47 of 120 evaluations (30 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 19
- max_abs_err <= 0.000976562: 61% violate; best seen 1.94e-07 (2^-22.29)

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=12 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=267, accuracy_bits=10.5, luts=169, ffs=98, throughput_msps=13.2, max_abs_err=0.000711 (2^-10.46), power_index=0.151
- iterative [data_width=16 n_iter=14 angle_guard=-1 frac_guard=0 rounding=round] luts_plus_ffs=271, accuracy_bits=10.5, luts=176, ffs=95, throughput_msps=11.7, max_abs_err=0.000706 (2^-10.47), power_index=0.173
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.3, luts=178, ffs=96, throughput_msps=11.7, max_abs_err=0.0004 (2^-11.29), power_index=0.175
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=1 rounding=round] luts_plus_ffs=319, accuracy_bits=11.3, luts=221, ffs=98, throughput_msps=11.7, max_abs_err=0.000389 (2^-11.33), power_index=0.204
- iterative [data_width=21 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=356, accuracy_bits=13.8, luts=235, ffs=121, throughput_msps=10.8, max_abs_err=6.94e-05 (2^-13.81), power_index=0.241
- iterative [data_width=19 n_iter=18 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=397, accuracy_bits=15.4, luts=276, ffs=121, throughput_msps=7.57, max_abs_err=2.33e-05 (2^-15.39), power_index=0.314
- iterative [data_width=21 n_iter=25 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=413, accuracy_bits=16.1, luts=286, ffs=127, throughput_msps=5.57, max_abs_err=1.38e-05 (2^-16.14), power_index=0.435
- iterative [data_width=25 n_iter=24 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=490, accuracy_bits=19.5, luts=348, ffs=142, throughput_msps=5.78, max_abs_err=1.37e-06 (2^-19.48), power_index=0.498
- iterative [data_width=25 n_iter=24 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=512, accuracy_bits=19.9, luts=366, ffs=146, throughput_msps=5.68, max_abs_err=9.91e-07 (2^-19.94), power_index=0.52
- iterative [data_width=26 n_iter=24 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=629, accuracy_bits=22.3, luts=473, ffs=156, throughput_msps=5.68, max_abs_err=1.94e-07 (2^-22.29), power_index=0.639
Front coverage: luts_plus_ffs 267..629 (HV reference 1500); accuracy_bits 10.5..22.3 (HV reference 10); data_width on the front 16..26 (registry 8..28).

Per family:
- iterative: 70 evals, 34 feasible; max throughput seen 19 MSPS; best accuracy 22.29 bits; best feasible luts_plus_ffs=267; feasible ranges: data_width 15..28, n_iter 12..25, angle_guard -1..3, frac_guard 0..3
- unrolled_k: 50 evals, 13 feasible; max throughput seen 14 MSPS; best accuracy 20.70 bits; best feasible luts_plus_ffs=365; feasible ranges: data_width 15..28, n_iter 12..26, angle_guard -1..2, frac_guard 0..3, k 3..6
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `iterative` (80 evals): data_width=15..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (10 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 125 feasible; hypervolume 1.565e+04 (+21.3%).

**No LLM call** (code's front-mapping round): The constraints are met: 100% of feasible designs satisfy throughput >= 1 MSPS (best 19 MSPS) and max_abs_err <= 2^-10 (best 2^-22.29). The Pareto front is well-populated with 10 designs spanning luts_plus_ffs 267..629 and accuracy_bits 10.5..22.3, covering the full trade-off curve from the area-optimal corner (iterative W=16, N=12, 267 LUTs+FFs) to the accuracy-optimal corner. The selection rule (min luts_plus_ffs) picks the iterative design at 267 LUTs+FFs with 10.5 bits accuracy and 13.2 MSPS throughput, which comfortably satisfies the spec. The front is mature and the hypervolume is strong; no further exploration is warranted in the final round.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.565e+04 (gain this round: +21.3%).
Feasible designs: 125 of 200 evaluations (97 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 19
- max_abs_err <= 0.000976562: 38% violate; best seen 2.91e-08 (2^-25.04)

Pareto front (feasible, 27 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=12 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=267, accuracy_bits=10.5, luts=169, ffs=98, throughput_msps=13.2, max_abs_err=0.000711 (2^-10.46), power_index=0.151
- iterative [data_width=16 n_iter=14 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=282, accuracy_bits=11.7, luts=183, ffs=99, throughput_msps=11.4, max_abs_err=0.000294 (2^-11.73), power_index=0.18
- iterative [data_width=18 n_iter=17 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=327, accuracy_bits=12.4, luts=217, ffs=110, throughput_msps=7.95, max_abs_err=0.000187 (2^-12.38), power_index=0.246
- iterative [data_width=19 n_iter=21 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=344, accuracy_bits=13.5, luts=231, ffs=113, throughput_msps=6.62, max_abs_err=8.6e-05 (2^-13.51), power_index=0.311
- iterative [data_width=18 n_iter=24 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=378, accuracy_bits=14.4, luts=263, ffs=115, throughput_msps=5.89, max_abs_err=4.69e-05 (2^-14.38), power_index=0.384
- iterative [data_width=21 n_iter=25 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=413, accuracy_bits=16.1, luts=286, ffs=127, throughput_msps=5.57, max_abs_err=1.38e-05 (2^-16.14), power_index=0.435
- iterative [data_width=24 n_iter=24 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=490, accuracy_bits=18.9, luts=348, ffs=141, throughput_msps=5.78, max_abs_err=2.03e-06 (2^-18.91), power_index=0.497
- iterative [data_width=27 n_iter=26 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=547, accuracy_bits=22, luts=394, ffs=153, throughput_msps=5.28, max_abs_err=2.33e-07 (2^-22.03), power_index=0.597
- iterative [data_width=28 n_iter=26 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=619, accuracy_bits=24.1, luts=453, ffs=166, throughput_msps=5.19, max_abs_err=5.73e-08 (2^-24.06), power_index=0.676
- iterative [data_width=28 n_iter=30 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=703, accuracy_bits=25, luts=536, ffs=166, throughput_msps=4.56, max_abs_err=2.91e-08 (2^-25.04), power_index=0.872
Front coverage: luts_plus_ffs 267..703 (HV reference 1500); accuracy_bits 10.5..25 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- iterative: 150 evals, 112 feasible; max throughput seen 19 MSPS; best accuracy 25.04 bits; best feasible luts_plus_ffs=267; feasible ranges: data_width 15..28, n_iter 11..30, angle_guard -1..4, frac_guard 0..4
- unrolled_k: 50 evals, 13 feasible; max throughput seen 14 MSPS; best accuracy 20.70 bits; best feasible luts_plus_ffs=365; feasible ranges: data_width 15..28, n_iter 12..26, angle_guard -1..2, frac_guard 0..3, k 3..6
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8348 in, 1650 out
- provider-reported cost: $0.0045
- full prompts and replies: `llm_trace.jsonl`

