# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 190 of 190 budgeted, over 3 round(s).  
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
  budget: 190 evals, 100/round, <= 4 rounds, eps 0.01
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

## Pareto front (24 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` | 166 | 91 | 11.7 | 17 | 0.164 | 0.00081 (2^-10.27) | 10.27 |
| 1 | `iterative:data_width=16,n_iter=12,angle_guard=0,frac_guard=0,rounding=round` | 167 | 96 | 13.2 | 15 | 0.148 | 0.000712 (2^-10.46) | 10.46 |
| 2 | `iterative:data_width=16,n_iter=14,angle_guard=1,frac_guard=0,rounding=trunc` | 172 | 97 | 11.7 | 17 | 0.172 | 0.000643 (2^-10.60) | 10.60 |
| 3 | `iterative:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` | 178 | 96 | 11.7 | 17 | 0.175 | 0.0004 (2^-11.29) | 11.29 |
| 4 | `iterative:data_width=17,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc` | 181 | 101 | 10.4 | 19 | 0.202 | 0.000307 (2^-11.67) | 11.67 |
| 5 | `iterative:data_width=15,n_iter=16,angle_guard=3,frac_guard=3,rounding=trunc` | 193 | 100 | 10.4 | 19 | 0.209 | 0.00025 (2^-11.97) | 11.97 |
| 6 | `iterative:data_width=17,n_iter=16,angle_guard=1,frac_guard=1,rounding=round` | 236 | 104 | 10.4 | 19 | 0.243 | 0.000128 (2^-12.94) | 12.94 |
| 7 | `iterative:data_width=20,n_iter=16,angle_guard=-2,frac_guard=4,rounding=trunc` | 251 | 122 | 10.0 | 19 | 0.266 | 9.69e-05 (2^-13.33) | 13.33 |
| 8 | `iterative:data_width=21,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc` | 248 | 126 | 10.5 | 18 | 0.254 | 6.5e-05 (2^-13.91) | 13.91 |
| 9 | `iterative:data_width=24,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc` | 265 | 138 | 10.0 | 19 | 0.288 | 3.16e-05 (2^-14.95) | 14.95 |
| 10 | `iterative:data_width=21,n_iter=25,angle_guard=2,frac_guard=0,rounding=round` | 283 | 124 | 5.6 | 28 | 0.429 | 1.15e-05 (2^-16.41) | 16.41 |
| 11 | `iterative:data_width=22,n_iter=26,angle_guard=0,frac_guard=1,rounding=trunc` | 299 | 129 | 5.4 | 29 | 0.467 | 9.92e-06 (2^-16.62) | 16.62 |
| 12 | `iterative:data_width=24,n_iter=23,angle_guard=2,frac_guard=0,rounding=trunc` | 321 | 139 | 6.0 | 26 | 0.45 | 2.96e-06 (2^-18.37) | 18.37 |
| 13 | `iterative:data_width=24,n_iter=26,angle_guard=0,frac_guard=0,rounding=round` | 335 | 137 | 5.4 | 29 | 0.515 | 2.49e-06 (2^-18.62) | 18.62 |
| 14 | `iterative:data_width=24,n_iter=23,angle_guard=2,frac_guard=2,rounding=trunc` | 352 | 143 | 6.0 | 26 | 0.484 | 1.14e-06 (2^-19.74) | 19.74 |
| 15 | `iterative:data_width=24,n_iter=23,angle_guard=4,frac_guard=2,rounding=trunc` | 356 | 145 | 5.9 | 26 | 0.49 | 9.38e-07 (2^-20.02) | 20.02 |
| 16 | `iterative:data_width=25,n_iter=29,angle_guard=2,frac_guard=2,rounding=trunc` | 379 | 148 | 4.8 | 32 | 0.634 | 5.15e-07 (2^-20.89) | 20.89 |
| 17 | `iterative:data_width=28,n_iter=23,angle_guard=2,frac_guard=0,rounding=trunc` | 391 | 159 | 5.9 | 26 | 0.538 | 3.65e-07 (2^-21.38) | 21.38 |
| 18 | `iterative:data_width=27,n_iter=29,angle_guard=0,frac_guard=1,rounding=trunc` | 397 | 154 | 4.8 | 32 | 0.664 | 3.31e-07 (2^-21.53) | 21.53 |
| 19 | `iterative:data_width=28,n_iter=28,angle_guard=2,frac_guard=0,rounding=trunc` | 400 | 159 | 4.9 | 31 | 0.652 | 2.17e-07 (2^-22.13) | 22.13 |
| 20 | `iterative:data_width=28,n_iter=26,angle_guard=0,frac_guard=1,rounding=trunc` | 413 | 159 | 5.3 | 29 | 0.625 | 1.6e-07 (2^-22.58) | 22.58 |
| 21 | `iterative:data_width=28,n_iter=29,angle_guard=3,frac_guard=0,rounding=round` | 421 | 160 | 4.7 | 32 | 0.7 | 1.11e-07 (2^-23.10) | 23.10 |
| 22 | `iterative:data_width=28,n_iter=29,angle_guard=2,frac_guard=2,rounding=trunc` | 440 | 163 | 4.8 | 32 | 0.726 | 7.27e-08 (2^-23.71) | 23.71 |
| 23 | `iterative:data_width=28,n_iter=29,angle_guard=4,frac_guard=3,rounding=trunc` | 462 | 167 | 4.7 | 32 | 0.758 | 3.83e-08 (2^-24.64) | 24.64 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *iterative is the clear winner on the merged front (20 of 21 designs, best 281 luts_plus_ffs) and is the only family I can use that meets the 1 MSPS throughput constraint. unrolled_k is currently off the front (best 378) but I will spend a small share to confirm it is strictly dominated. I will focus the budget on iterative, narrowing the search to the low-area corner (data_width 12-16, n_iter 10-14, angle_guard -2..0, frac_guard 0..1, rounding=round) to maximise hypervolume on the area/accuracy trade-off curve.*)
- `iterative` (77 evals): data_width=12..16, n_iter=10..14, angle_guard=-2..0, frac_guard=0..1, rounding=round. *Why:* iterative dominates the merged front (20 of 21 designs) and is the only family I can use that meets the 1 MSPS constraint; I will refine the low-area corner of the front to maximise hypervolume.
- `unrolled_k` (23 evals): data_width=12..16, n_iter=10..14, angle_guard=-2..0, frac_guard=0..1, rounding=round, k=2..4. *Why:* unrolled_k is currently off the merged front (best 378 vs iterative 281); I will confirm whether any k=2..4 configuration can beat iterative on the area/accuracy trade-off or if it is strictly dominated.

**Result (code):** 100 evaluations this round, 100 total; 38 feasible; hypervolume 1632 (n/a).

**LLM decision:** `refine` — The current front is dominated by the `iterative` family, with the best area (257) at 10.3 bits accuracy and the best accuracy (11.3 bits) at 273-319 area. The `unrolled_k` family is strictly worse in area (min 336) for the same accuracy range, so it can be deprioritized. The accuracy constraint is tight (62% violation rate in Round 1), suggesting the search space needs to be focused on configurations that reliably meet the 2^-10 error bound while minimizing area. The current feasible region is narrow (data_width 15-16, n_iter 12-14). To improve hypervolume, we need to explore if slightly larger `data_width` or `n_iter` can push accuracy higher without excessive area cost, or if smaller `data_width` (e.g., 14) with optimized guards can reduce area further while still meeting the error constraint. The `pipelined` and `pipelined_m` families have not been explored yet, but given the strict area objective and the fact that `iterative` is already very efficient (1 result every N+3 cycles, but high Fmax allows >1 MSPS easily), the area overhead of pipeline registers in `pipelined` families will likely make them suboptimal for the 'min luts_plus_ffs' objective unless they allow significantly smaller data widths. However, since `iterative` is already meeting throughput easily (11.7-15.3 MSPS vs 1 MSPS required), the bottleneck is purely area vs accuracy. I will refine the search to focus on the `iterative` family in the promising region, slightly widening `n_iter` to 15 to see if it helps accuracy without too much area penalty, and checking `data_width` 14 to see if area can be reduced further while maintaining accuracy via rounding/guards.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 190.
Hypervolume of the feasible front: 1632 (gain this round: n/a (first round)).
Feasible designs: 38 of 100 evaluations (23 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.3
- max_abs_err <= 0.000976562: 62% violate; best seen 0.000389 (2^-11.33)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11.7, max_abs_err=0.00081 (2^-10.27), power_index=0.164
- iterative [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.5, luts=167, ffs=96, throughput_msps=13.2, max_abs_err=0.000712 (2^-10.46), power_index=0.148
- iterative [data_width=16 n_iter=14 angle_guard=-1 frac_guard=0 rounding=round] luts_plus_ffs=271, accuracy_bits=10.5, luts=176, ffs=95, throughput_msps=11.7, max_abs_err=0.000706 (2^-10.47), power_index=0.173
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.3, luts=178, ffs=96, throughput_msps=11.7, max_abs_err=0.0004 (2^-11.29), power_index=0.175
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=1 rounding=round] luts_plus_ffs=319, accuracy_bits=11.3, luts=221, ffs=98, throughput_msps=11.7, max_abs_err=0.000389 (2^-11.33), power_index=0.204
Front coverage: luts_plus_ffs 257..319 (HV reference 1500); accuracy_bits 10.3..11.3 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- iterative: 77 evals, 28 feasible; max throughput seen 15.3 MSPS; best accuracy 11.33 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard -1..0, frac_guard 0..1
- unrolled_k: 23 evals, 10 feasible; max throughput seen 13.5 MSPS; best accuracy 11.33 bits; best feasible luts_plus_ffs=336; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..0, frac_guard 0..1, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate remaining budget on the dominant family to refine the Pareto front in the critical area-accuracy trade-off region.*)
- `iterative` (14 evals): data_width=14..17, n_iter=12..16, angle_guard=-1..1, frac_guard=0..2, rounding=trunc|round. *Why:* Focus on the best-performing family. Widen n_iter slightly to explore accuracy gains, and check data_width=14 for potential area savings. Expand guard ranges slightly to find optimal trade-offs.

**Result (code):** 14 evaluations this round, 114 total; 52 feasible; hypervolume 3520 (+115.7%).

**LLM decision:** `stop` — The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (iterative, luts_plus_ffs=257) meets the throughput constraint (11.7 MSPS >= 1 MSPS) and the accuracy constraint (10.3 bits >= 10 bits). The front covers a reasonable range of the trade-off space (area 257-340, accuracy 10.3-12.9 bits). Since this is the final round, we stop and select the design with minimum luts_plus_ffs (257) as per the selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 76 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 114 of 190.
Hypervolume of the feasible front: 3520 (gain this round: +115.7%).
Feasible designs: 52 of 114 evaluations (33 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.3
- max_abs_err <= 0.000976562: 54% violate; best seen 0.000128 (2^-12.94)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11.7, max_abs_err=0.00081 (2^-10.27), power_index=0.164
- iterative [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.5, luts=167, ffs=96, throughput_msps=13.2, max_abs_err=0.000712 (2^-10.46), power_index=0.148
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=269, accuracy_bits=10.6, luts=172, ffs=97, throughput_msps=11.7, max_abs_err=0.000643 (2^-10.60), power_index=0.172
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.3, luts=178, ffs=96, throughput_msps=11.7, max_abs_err=0.0004 (2^-11.29), power_index=0.175
- iterative [data_width=17 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=282, accuracy_bits=11.7, luts=181, ffs=101, throughput_msps=10.4, max_abs_err=0.000307 (2^-11.67), power_index=0.202
- iterative [data_width=17 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts_plus_ffs=340, accuracy_bits=12.9, luts=236, ffs=104, throughput_msps=10.4, max_abs_err=0.000128 (2^-12.94), power_index=0.243
Front coverage: luts_plus_ffs 257..340 (HV reference 1500); accuracy_bits 10.3..12.9 (HV reference 10); data_width on the front 15..17 (registry 8..28).

Per family:
- iterative: 91 evals, 42 feasible; max throughput seen 15.3 MSPS; best accuracy 12.94 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 14..17, n_iter 12..16, angle_guard -1..1, frac_guard 0..2
- unrolled_k: 23 evals, 10 feasible; max throughput seen 13.5 MSPS; best accuracy 11.33 bits; best feasible luts_plus_ffs=336; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..0, frac_guard 0..1, k 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 76 evaluations*)
- `iterative` (76 evals): data_width=14..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (6 front designs; box front_anchored)

**Result (code):** 76 evaluations this round, 190 total; 120 feasible; hypervolume 1.534e+04 (+335.9%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (iterative, luts_plus_ffs=257) meets the throughput constraint (11.7 MSPS >= 1 MSPS) and the accuracy constraint (10.3 bits >= 10 bits). The front covers a reasonable range of the trade-off space (area 257-340, accuracy 10.3-12.9 bits). Since this is the final round, we stop and select the design with minimum luts_plus_ffs (257) as per the selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 190 of 190.
Hypervolume of the feasible front: 1.534e+04 (gain this round: +335.9%).
Feasible designs: 120 of 190 evaluations (96 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.3
- max_abs_err <= 0.000976562: 37% violate; best seen 3.83e-08 (2^-24.64)

Pareto front (feasible, 24 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11.7, max_abs_err=0.00081 (2^-10.27), power_index=0.164
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.3, luts=178, ffs=96, throughput_msps=11.7, max_abs_err=0.0004 (2^-11.29), power_index=0.175
- iterative [data_width=15 n_iter=16 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=293, accuracy_bits=12, luts=193, ffs=100, throughput_msps=10.4, max_abs_err=0.00025 (2^-11.97), power_index=0.209
- iterative [data_width=21 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=375, accuracy_bits=13.9, luts=248, ffs=126, throughput_msps=10.5, max_abs_err=6.5e-05 (2^-13.91), power_index=0.254
- iterative [data_width=21 n_iter=25 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=407, accuracy_bits=16.4, luts=283, ffs=124, throughput_msps=5.57, max_abs_err=1.15e-05 (2^-16.41), power_index=0.429
- iterative [data_width=24 n_iter=26 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=472, accuracy_bits=18.6, luts=335, ffs=137, throughput_msps=5.38, max_abs_err=2.49e-06 (2^-18.62), power_index=0.515
- iterative [data_width=24 n_iter=23 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=501, accuracy_bits=20, luts=356, ffs=145, throughput_msps=5.89, max_abs_err=9.38e-07 (2^-20.02), power_index=0.49
- iterative [data_width=27 n_iter=29 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=552, accuracy_bits=21.5, luts=397, ffs=154, throughput_msps=4.79, max_abs_err=3.31e-07 (2^-21.53), power_index=0.664
- iterative [data_width=28 n_iter=26 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=573, accuracy_bits=22.6, luts=413, ffs=159, throughput_msps=5.28, max_abs_err=1.6e-07 (2^-22.58), power_index=0.625
- iterative [data_width=28 n_iter=29 angle_guard=4 frac_guard=3 rounding=trunc] luts_plus_ffs=630, accuracy_bits=24.6, luts=462, ffs=167, throughput_msps=4.7, max_abs_err=3.83e-08 (2^-24.64), power_index=0.758
Front coverage: luts_plus_ffs 257..630 (HV reference 1500); accuracy_bits 10.3..24.6 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 167 evals, 110 feasible; max throughput seen 15.3 MSPS; best accuracy 24.64 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 14..28, n_iter 11..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 23 evals, 10 feasible; max throughput seen 13.5 MSPS; best accuracy 11.33 bits; best feasible luts_plus_ffs=336; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..0, frac_guard 0..1, k 2..4
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7338 in, 1595 out
- provider-reported cost: $0.0040
- full prompts and replies: `llm_trace.jsonl`

