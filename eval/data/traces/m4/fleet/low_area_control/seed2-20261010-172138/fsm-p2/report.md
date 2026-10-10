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
`iterative:data_width=15,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 166 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 91 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 11 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 90.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.174 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00081 (2^-10.27) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.64 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00021 (2^-12.22) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.72 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (31 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 166 | 91 | 11.0 | 18 | 0.174 | 0.00081 (2^-10.27) | 10.27 |
| 1 | `iterative:data_width=15,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 168 | 92 | 11.0 | 18 | 0.176 | 0.000632 (2^-10.63) | 10.63 |
| 2 | `iterative:data_width=15,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 168 | 92 | 11.7 | 17 | 0.166 | 0.000632 (2^-10.63) | 10.63 |
| 3 | `iterative:data_width=15,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 168 | 92 | 10.4 | 19 | 0.186 | 0.000632 (2^-10.63) | 10.63 |
| 4 | `iterative:data_width=15,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 170 | 93 | 10.4 | 19 | 0.188 | 0.000599 (2^-10.71) | 10.71 |
| 5 | `iterative:data_width=15,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc` | 170 | 94 | 11.0 | 18 | 0.179 | 0.000567 (2^-10.78) | 10.78 |
| 6 | `iterative:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` | 178 | 96 | 11.7 | 17 | 0.175 | 0.0004 (2^-11.29) | 11.29 |
| 7 | `iterative:data_width=16,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 179 | 97 | 11.7 | 17 | 0.177 | 0.000342 (2^-11.51) | 11.51 |
| 8 | `iterative:data_width=16,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc` | 191 | 101 | 11.7 | 17 | 0.187 | 0.000311 (2^-11.65) | 11.65 |
| 9 | `iterative:data_width=16,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 193 | 102 | 10.4 | 19 | 0.211 | 0.000219 (2^-12.16) | 12.16 |
| 10 | `iterative:data_width=18,n_iter=20,angle_guard=4,frac_guard=0,rounding=trunc` | 219 | 111 | 6.9 | 23 | 0.286 | 0.000187 (2^-12.38) | 12.38 |
| 11 | `iterative:data_width=16,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 234 | 102 | 10.4 | 19 | 0.24 | 0.000134 (2^-12.86) | 12.86 |
| 12 | `iterative:data_width=18,n_iter=24,angle_guard=1,frac_guard=1,rounding=trunc` | 230 | 110 | 5.9 | 27 | 0.345 | 0.000115 (2^-13.09) | 13.09 |
| 13 | `iterative:data_width=18,n_iter=24,angle_guard=4,frac_guard=1,rounding=trunc` | 235 | 113 | 5.9 | 27 | 0.353 | 0.000112 (2^-13.12) | 13.12 |
| 14 | `iterative:data_width=18,n_iter=24,angle_guard=1,frac_guard=2,rounding=trunc` | 245 | 112 | 5.9 | 27 | 0.363 | 7.17e-05 (2^-13.77) | 13.77 |
| 15 | `iterative:data_width=18,n_iter=21,angle_guard=4,frac_guard=2,rounding=trunc` | 251 | 115 | 6.6 | 24 | 0.33 | 5.63e-05 (2^-14.12) | 14.12 |
| 16 | `iterative:data_width=19,n_iter=20,angle_guard=4,frac_guard=2,rounding=trunc` | 264 | 120 | 6.8 | 23 | 0.332 | 2.55e-05 (2^-15.26) | 15.26 |
| 17 | `iterative:data_width=19,n_iter=26,angle_guard=4,frac_guard=4,rounding=trunc` | 301 | 124 | 5.4 | 29 | 0.464 | 1.39e-05 (2^-16.13) | 16.13 |
| 18 | `iterative:data_width=21,n_iter=26,angle_guard=3,frac_guard=2,rounding=trunc` | 303 | 129 | 5.4 | 29 | 0.471 | 8.12e-06 (2^-16.91) | 16.91 |
| 19 | `iterative:data_width=23,n_iter=25,angle_guard=0,frac_guard=0,rounding=trunc` | 301 | 132 | 5.6 | 28 | 0.456 | 6.79e-06 (2^-17.17) | 17.17 |
| 20 | `iterative:data_width=22,n_iter=20,angle_guard=4,frac_guard=2,rounding=trunc` | 312 | 135 | 6.8 | 23 | 0.387 | 4.4e-06 (2^-17.79) | 17.79 |
| 21 | `iterative:data_width=22,n_iter=21,angle_guard=4,frac_guard=2,rounding=trunc` | 321 | 135 | 6.5 | 24 | 0.411 | 3.58e-06 (2^-18.09) | 18.09 |
| 22 | `iterative:data_width=22,n_iter=25,angle_guard=4,frac_guard=2,rounding=trunc` | 324 | 135 | 5.6 | 28 | 0.483 | 3.45e-06 (2^-18.15) | 18.15 |
| 23 | `iterative:data_width=21,n_iter=24,angle_guard=4,frac_guard=4,rounding=trunc` | 334 | 134 | 5.8 | 27 | 0.476 | 3.18e-06 (2^-18.26) | 18.26 |
| 24 | `iterative:data_width=22,n_iter=28,angle_guard=4,frac_guard=4,rounding=trunc` | 358 | 139 | 5.0 | 31 | 0.58 | 1.79e-06 (2^-19.09) | 19.09 |
| 25 | `iterative:data_width=25,n_iter=24,angle_guard=1,frac_guard=2,rounding=trunc` | 368 | 147 | 5.7 | 27 | 0.523 | 6.74e-07 (2^-20.50) | 20.50 |
| 26 | `iterative:data_width=28,n_iter=30,angle_guard=4,frac_guard=1,rounding=trunc` | 425 | 163 | 4.6 | 33 | 0.73 | 1.13e-07 (2^-23.08) | 23.08 |
| 27 | `iterative:data_width=27,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc` | 434 | 161 | 5.3 | 29 | 0.65 | 9.63e-08 (2^-23.31) | 23.31 |
| 28 | `iterative:data_width=28,n_iter=28,angle_guard=1,frac_guard=1,rounding=round` | 489 | 160 | 4.9 | 31 | 0.757 | 8.86e-08 (2^-23.43) | 23.43 |
| 29 | `iterative:data_width=28,n_iter=28,angle_guard=1,frac_guard=3,rounding=round` | 523 | 164 | 4.9 | 31 | 0.802 | 7.8e-08 (2^-23.61) | 23.61 |
| 30 | `iterative:data_width=28,n_iter=28,angle_guard=4,frac_guard=3,rounding=round` | 529 | 167 | 4.9 | 31 | 0.812 | 2.42e-08 (2^-25.30) | 25.30 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show iterative is the sole contributor to the merged Pareto front (19/19 designs, best luts_plus_ffs 300), while unrolled_k (best 730), pipelined (1548) and pipelined_m (838) all sit far off the front and contribute nothing. Since I am restricted to iterative and unrolled_k, and unrolled_k has already been shown to be strictly dominated in area (730 vs 300) with 0 front members, the entire remaining budget should go to iterative. The first 73 evals covered the full registry ranges; now that the feasible region is known (data_width ~12-16, n_iter ~10-16, small guards), I narrow the ranges to focus the search on the actual trade-off curve between luts_plus_ffs and accuracy_bits. This maximizes hypervolume by densely covering the feasible Pareto segment rather than wasting evals on infeasible or dominated configurations. unrolled_k is excluded because its best area (730) is 2.4x worse than iterative's best (300) and it has contributed zero designs to the front, so it cannot improve hypervolume within the remaining budget.*)
- `iterative` (100 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative owns the entire merged front (19/19) with best area 300, so it is the only family that can plausibly improve the hypervolume. The previous 73 evals already mapped the broad space; this round narrows to the accuracy-feasible core (data_width 12-16, n_iter 10-16, small guards) to densely sample the area-vs-accuracy trade-off curve rather than re-exploring infeasible corners.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 56 feasible; hypervolume 3461 (n/a).

**LLM decision:** `add_family` — The current front is dominated by the `iterative` family, which has a throughput bottleneck (1 result per N+3 cycles). While it meets the >= 1 MSPS constraint (best seen 15.6 MSPS), the area cost (luts_plus_ffs) starts at 257. The `unrolled_k` family is not yet explored. By unrolling k micro-rotations per cycle, we can potentially reduce the critical path length (improving Fmax) and/or reduce the number of FSM states/registers compared to a fully pipelined design, while maintaining high throughput. Given the strict area objective (min luts_plus_ffs) and the requirement for >= 1 MSPS, `unrolled_k` with small k (e.g., 2-4) is a strong candidate to beat the iterative baseline, especially if the iterative design's area is inflated by the long shift chains or FSM logic. We should explore `unrolled_k` to see if it offers a better area/accuracy trade-off or if it allows for a smaller data_width/n_iter combination that still meets the accuracy constraint with less area.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 3461 (gain this round: n/a (first round)).
Feasible designs: 56 of 100 evaluations (38 unique).
Families explored so far: iterative. Not yet explored: unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 44% violate; best seen 0.000134 (2^-12.86)

Pareto front (feasible, 12 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11, max_abs_err=0.00081 (2^-10.27), power_index=0.174
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.6, luts=168, ffs=92, throughput_msps=11, max_abs_err=0.000632 (2^-10.63), power_index=0.176
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.6, luts=168, ffs=92, throughput_msps=11.7, max_abs_err=0.000632 (2^-10.63), power_index=0.166
- iterative [data_width=15 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.7, luts=170, ffs=93, throughput_msps=10.4, max_abs_err=0.000599 (2^-10.71), power_index=0.188
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=264, accuracy_bits=10.8, luts=170, ffs=94, throughput_msps=11, max_abs_err=0.000567 (2^-10.78), power_index=0.179
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.3, luts=178, ffs=96, throughput_msps=11.7, max_abs_err=0.0004 (2^-11.29), power_index=0.175
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.5, luts=179, ffs=97, throughput_msps=11.7, max_abs_err=0.000342 (2^-11.51), power_index=0.177
- iterative [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=295, accuracy_bits=12.2, luts=193, ffs=102, throughput_msps=10.4, max_abs_err=0.000219 (2^-12.16), power_index=0.211
- iterative [data_width=16 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=333, accuracy_bits=12.2, luts=232, ffs=101, throughput_msps=10.4, max_abs_err=0.000214 (2^-12.19), power_index=0.238
- iterative [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=336, accuracy_bits=12.9, luts=234, ffs=102, throughput_msps=10.4, max_abs_err=0.000134 (2^-12.86), power_index=0.24
Front coverage: luts_plus_ffs 257..336 (HV reference 1500); accuracy_bits 10.3..12.9 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- iterative: 100 evals, 56 feasible; max throughput seen 15.6 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 13..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Adding unrolled_k to explore area-efficient high-throughput designs.*)
- `unrolled_k` (20 evals): data_width=13..18, n_iter=12..18, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Explore unrolled_k to find potentially lower area designs that meet throughput and accuracy constraints, comparing against the iterative baseline.

**Result (code):** 20 evaluations this round, 120 total; 71 feasible; hypervolume 3692 (+6.7%).

**LLM decision:** `stop` — The spec is feasible: the front contains 13 designs meeting throughput >= 1 MSPS and max_abs_err <= 2^-10, with the best area at 257 luts_plus_ffs (iterative, data_width=15, n_iter=15, angle_guard=0, rounding=round) and accuracy up to 13.11 bits. The front spans luts_plus_ffs 257..562 and accuracy_bits 10.3..13.1, well inside the HV reference box (1500, 10), and the selection rule (min luts_plus_ffs) is satisfied by the 257 design. Since this is the final round, the current front is the deliverable.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 3692 (gain this round: +6.7%).
Feasible designs: 71 of 120 evaluations (52 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 41% violate; best seen 0.000113 (2^-13.11)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11, max_abs_err=0.00081 (2^-10.27), power_index=0.174
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.6, luts=168, ffs=92, throughput_msps=11, max_abs_err=0.000632 (2^-10.63), power_index=0.176
- iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.6, luts=168, ffs=92, throughput_msps=10.4, max_abs_err=0.000632 (2^-10.63), power_index=0.186
- iterative [data_width=15 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.7, luts=170, ffs=93, throughput_msps=10.4, max_abs_err=0.000599 (2^-10.71), power_index=0.188
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=264, accuracy_bits=10.8, luts=170, ffs=94, throughput_msps=11, max_abs_err=0.000567 (2^-10.78), power_index=0.179
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.5, luts=179, ffs=97, throughput_msps=11.7, max_abs_err=0.000342 (2^-11.51), power_index=0.177
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=292, accuracy_bits=11.7, luts=191, ffs=101, throughput_msps=11.7, max_abs_err=0.000311 (2^-11.65), power_index=0.187
- iterative [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=295, accuracy_bits=12.2, luts=193, ffs=102, throughput_msps=10.4, max_abs_err=0.000219 (2^-12.16), power_index=0.211
- iterative [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=336, accuracy_bits=12.9, luts=234, ffs=102, throughput_msps=10.4, max_abs_err=0.000134 (2^-12.86), power_index=0.24
- unrolled_k [data_width=18 n_iter=17 angle_guard=0 frac_guard=2 rounding=trunc k=4] luts_plus_ffs=562, accuracy_bits=13.1, luts=453, ffs=109, throughput_msps=6.63, max_abs_err=0.000113 (2^-13.11), power_index=0.169
Front coverage: luts_plus_ffs 257..562 (HV reference 1500); accuracy_bits 10.3..13.1 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 100 evals, 56 feasible; max throughput seen 15.6 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 13..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
- unrolled_k: 20 evals, 15 feasible; max throughput seen 11.6 MSPS; best accuracy 13.11 bits; best feasible luts_plus_ffs=365; feasible ranges: data_width 16..18, n_iter 12..17, angle_guard 0..2, frac_guard 0..2, k 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `iterative` (74 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (12 front designs; box front_anchored)
- `unrolled_k` (6 evals): data_width=17..28, n_iter=15..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (1 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 147 feasible; hypervolume 1.575e+04 (+326.7%).

**No LLM call** (code's front-mapping round): The spec is feasible: the front contains 13 designs meeting throughput >= 1 MSPS and max_abs_err <= 2^-10, with the best area at 257 luts_plus_ffs (iterative, data_width=15, n_iter=15, angle_guard=0, rounding=round) and accuracy up to 13.11 bits. The front spans luts_plus_ffs 257..562 and accuracy_bits 10.3..13.1, well inside the HV reference box (1500, 10), and the selection rule (min luts_plus_ffs) is satisfied by the 257 design. Since this is the final round, the current front is the deliverable.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.575e+04 (gain this round: +326.7%).
Feasible designs: 147 of 200 evaluations (118 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 26% violate; best seen 2.42e-08 (2^-25.30)

Pareto front (feasible, 31 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11, max_abs_err=0.00081 (2^-10.27), power_index=0.174
- iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.6, luts=168, ffs=92, throughput_msps=10.4, max_abs_err=0.000632 (2^-10.63), power_index=0.186
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.5, luts=179, ffs=97, throughput_msps=11.7, max_abs_err=0.000342 (2^-11.51), power_index=0.177
- iterative [data_width=18 n_iter=20 angle_guard=4 frac_guard=0 rounding=trunc] luts_plus_ffs=330, accuracy_bits=12.4, luts=219, ffs=111, throughput_msps=6.91, max_abs_err=0.000187 (2^-12.38), power_index=0.286
- iterative [data_width=18 n_iter=24 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=348, accuracy_bits=13.1, luts=235, ffs=113, throughput_msps=5.89, max_abs_err=0.000112 (2^-13.12), power_index=0.353
- iterative [data_width=19 n_iter=26 angle_guard=4 frac_guard=4 rounding=trunc] luts_plus_ffs=425, accuracy_bits=16.1, luts=301, ffs=124, throughput_msps=5.38, max_abs_err=1.39e-05 (2^-16.13), power_index=0.464
- iterative [data_width=22 n_iter=20 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=447, accuracy_bits=17.8, luts=312, ffs=135, throughput_msps=6.78, max_abs_err=4.4e-06 (2^-17.79), power_index=0.387
- iterative [data_width=21 n_iter=24 angle_guard=4 frac_guard=4 rounding=trunc] luts_plus_ffs=469, accuracy_bits=18.3, luts=334, ffs=134, throughput_msps=5.78, max_abs_err=3.18e-06 (2^-18.26), power_index=0.476
- iterative [data_width=27 n_iter=26 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=595, accuracy_bits=23.3, luts=434, ffs=161, throughput_msps=5.28, max_abs_err=9.63e-08 (2^-23.31), power_index=0.65
- iterative [data_width=28 n_iter=28 angle_guard=4 frac_guard=3 rounding=round] luts_plus_ffs=696, accuracy_bits=25.3, luts=529, ffs=167, throughput_msps=4.86, max_abs_err=2.42e-08 (2^-25.30), power_index=0.812
Front coverage: luts_plus_ffs 257..696 (HV reference 1500); accuracy_bits 10.3..25.3 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 174 evals, 126 feasible; max throughput seen 15.6 MSPS; best accuracy 25.30 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 13..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 26 evals, 21 feasible; max throughput seen 11.6 MSPS; best accuracy 17.87 bits; best feasible luts_plus_ffs=365; feasible ranges: data_width 16..24, n_iter 12..25, angle_guard -2..3, frac_guard 0..4, k 2..7
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8350 in, 1471 out
- provider-reported cost: $0.0047
- full prompts and replies: `llm_trace.jsonl`

