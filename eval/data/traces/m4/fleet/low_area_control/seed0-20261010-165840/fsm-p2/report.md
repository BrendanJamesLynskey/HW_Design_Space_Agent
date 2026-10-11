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

## Pareto front (25 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=12,angle_guard=1,frac_guard=0,rounding=round` | 159 | 92 | 13.2 | 15 | 0.141 | 0.000917 (2^-10.09) | 10.09 |
| 1 | `iterative:data_width=16,n_iter=12,angle_guard=0,frac_guard=0,rounding=trunc` | 161 | 96 | 13.2 | 15 | 0.145 | 0.000887 (2^-10.14) | 10.14 |
| 2 | `iterative:data_width=15,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 168 | 92 | 11.7 | 17 | 0.166 | 0.000632 (2^-10.63) | 10.63 |
| 3 | `iterative:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` | 178 | 96 | 11.7 | 17 | 0.175 | 0.0004 (2^-11.29) | 11.29 |
| 4 | `iterative:data_width=16,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 179 | 97 | 11.7 | 17 | 0.177 | 0.000342 (2^-11.51) | 11.51 |
| 5 | `iterative:data_width=18,n_iter=30,angle_guard=0,frac_guard=1,rounding=trunc` | 228 | 109 | 4.8 | 33 | 0.418 | 0.000212 (2^-12.20) | 12.20 |
| 6 | `iterative:data_width=18,n_iter=18,angle_guard=4,frac_guard=2,rounding=trunc` | 248 | 115 | 7.6 | 21 | 0.286 | 4.84e-05 (2^-14.33) | 14.33 |
| 7 | `iterative:data_width=20,n_iter=22,angle_guard=2,frac_guard=1,rounding=trunc` | 266 | 121 | 6.4 | 25 | 0.364 | 2.4e-05 (2^-15.35) | 15.35 |
| 8 | `iterative:data_width=20,n_iter=30,angle_guard=1,frac_guard=2,rounding=trunc` | 280 | 122 | 4.8 | 33 | 0.499 | 2.15e-05 (2^-15.51) | 15.51 |
| 9 | `iterative:data_width=20,n_iter=29,angle_guard=3,frac_guard=2,rounding=trunc` | 284 | 124 | 4.9 | 32 | 0.491 | 2.04e-05 (2^-15.58) | 15.58 |
| 10 | `iterative:data_width=19,n_iter=29,angle_guard=3,frac_guard=4,rounding=trunc` | 299 | 123 | 4.9 | 32 | 0.508 | 1.69e-05 (2^-15.85) | 15.85 |
| 11 | `iterative:data_width=20,n_iter=27,angle_guard=2,frac_guard=1,rounding=round` | 324 | 121 | 5.3 | 30 | 0.502 | 1.37e-05 (2^-16.15) | 16.15 |
| 12 | `iterative:data_width=20,n_iter=24,angle_guard=3,frac_guard=1,rounding=round` | 324 | 122 | 5.8 | 27 | 0.453 | 1.24e-05 (2^-16.30) | 16.30 |
| 13 | `iterative:data_width=20,n_iter=29,angle_guard=3,frac_guard=4,rounding=trunc` | 318 | 128 | 4.9 | 32 | 0.537 | 8.49e-06 (2^-16.85) | 16.85 |
| 14 | `iterative:data_width=22,n_iter=30,angle_guard=1,frac_guard=2,rounding=trunc` | 318 | 132 | 4.7 | 33 | 0.559 | 5.98e-06 (2^-17.35) | 17.35 |
| 15 | `iterative:data_width=23,n_iter=24,angle_guard=2,frac_guard=1,rounding=trunc` | 319 | 136 | 5.8 | 27 | 0.462 | 3.08e-06 (2^-18.31) | 18.31 |
| 16 | `iterative:data_width=22,n_iter=24,angle_guard=3,frac_guard=3,rounding=trunc` | 334 | 136 | 5.8 | 27 | 0.478 | 2.39e-06 (2^-18.67) | 18.67 |
| 17 | `iterative:data_width=23,n_iter=24,angle_guard=2,frac_guard=2,rounding=trunc` | 334 | 138 | 5.8 | 27 | 0.48 | 1.91e-06 (2^-18.99) | 18.99 |
| 18 | `iterative:data_width=23,n_iter=22,angle_guard=3,frac_guard=2,rounding=trunc` | 336 | 139 | 6.2 | 25 | 0.447 | 1.83e-06 (2^-19.06) | 19.06 |
| 19 | `iterative:data_width=25,n_iter=22,angle_guard=1,frac_guard=3,rounding=trunc` | 383 | 149 | 6.1 | 25 | 0.501 | 1.02e-06 (2^-19.90) | 19.90 |
| 20 | `iterative:data_width=26,n_iter=29,angle_guard=4,frac_guard=0,rounding=round` | 382 | 151 | 4.8 | 32 | 0.642 | 3.6e-07 (2^-21.40) | 21.40 |
| 21 | `iterative:data_width=25,n_iter=25,angle_guard=3,frac_guard=3,rounding=trunc` | 396 | 151 | 5.5 | 28 | 0.576 | 3.42e-07 (2^-21.48) | 21.48 |
| 22 | `iterative:data_width=27,n_iter=24,angle_guard=3,frac_guard=2,rounding=trunc` | 406 | 159 | 5.7 | 27 | 0.575 | 1.97e-07 (2^-22.28) | 22.28 |
| 23 | `iterative:data_width=27,n_iter=27,angle_guard=3,frac_guard=2,rounding=trunc` | 417 | 159 | 5.1 | 30 | 0.65 | 1.26e-07 (2^-22.92) | 22.92 |
| 24 | `iterative:data_width=28,n_iter=27,angle_guard=4,frac_guard=3,rounding=trunc` | 455 | 167 | 5.0 | 30 | 0.702 | 4.35e-08 (2^-24.45) | 24.45 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts are clear: iterative dominates (14/17 front designs, best area 345), unrolled_k is a distant second (3/17, best 446), pipelined families are far off (843-1493) and contribute nothing to the front. For this low-area spec with throughput >= 1 MSPS, iterative is the primary candidate. The key tradeoff is accuracy_bits vs luts_plus_ffs: I need to find the minimum-area design that meets max_abs_err <= 2^-10 (accuracy_bits >= 10) while maintaining throughput >= 1 MSPS. data_width 12-16 with n_iter 10-14 covers the accuracy boundary. angle_guard negative saves LUTs. I'll spend 70% on iterative (the front owner) and 30% on unrolled_k (to confirm no better tradeoff exists). Both families share the same accuracy parameters, so the search regions are aligned. The 100-eval budget is split 70/30.*)
- `iterative` (50 evals): data_width=12..16, n_iter=10..14, angle_guard=-2..1, frac_guard=0..2, rounding=trunc|round. *Why:* iterative dominates the merged front (14/17 designs) and has the best area (345). It is the only family that can meet throughput >= 1 MSPS at low area, since unrolled_k with k=2 only reaches ~0.5-1 MSPS at the Fmax needed. I will focus on the tightest feasible region: data_width 12-16 (12 gives ~11 bits accuracy with N=12-14, 16 gives margin), n_iter 10-14 (10-12 may just meet 2^-10, 14 gives safety), angle_guard -2..1 (negative saves LUTs on the atan path), frac_guard 0..2 (0 saves area, 1-2 add margin). Rounding both to see if round helps accuracy at same area. This is where the Pareto front lives.
- `unrolled_k` (50 evals): data_width=12..16, n_iter=10..14, angle_guard=-2..1, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k has 3 designs on the front and best area 446. With k=2-4 it can potentially reach 1 MSPS if Fmax is high enough. I'll search the same accuracy region as iterative but with k=2-4 to find if any unrolled_k design beats iterative on the accuracy-vs-area tradeoff. k=2 is the sweet spot: 2x throughput of iterative at modest area penalty. k=3-4 may push Fmax down too much. This is a secondary search to confirm the front shape.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 40 feasible; hypervolume 1866 (n/a).

**LLM decision:** `add_family` — The current Pareto front is dominated by the `iterative` family (best area 251 LUTs+FFs), but `iterative` designs have high latency (N+3 cycles) and lower throughput (13.2 MSPS) compared to the potential of pipelined architectures. While `unrolled_k` was explored, it yielded worse area (357 LUTs+FFs) and similar throughput. The spec requires >= 1 MSPS, which is easily met, but `pipelined` and `pipelined_m` families offer 1 result/cycle throughput (potentially much higher MSPS if Fmax allows) and might offer different area/accuracy trade-offs due to their parallel structure. Specifically, `pipelined_m` with small `m` could reduce area compared to fully `pipelined` while maintaining high throughput. Since we have 100 evals left and only 2 families explored, adding `pipelined` and `pipelined_m` is crucial to ensure we haven't missed a superior area/accuracy point on the front, especially since the current front's accuracy range (10.1-11.5 bits) is close to the constraint limit (10 bits) and might be improvable with different architectural overheads.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1866 (gain this round: n/a (first round)).
Feasible designs: 40 of 100 evaluations (29 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 60% violate; best seen 0.000342 (2^-11.51)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=251, accuracy_bits=10.1, luts=159, ffs=92, throughput_msps=13.2, max_abs_err=0.000917 (2^-10.09), power_index=0.141
- iterative [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=257, accuracy_bits=10.1, luts=161, ffs=96, throughput_msps=13.2, max_abs_err=0.000887 (2^-10.14), power_index=0.145
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.6, luts=168, ffs=92, throughput_msps=11.7, max_abs_err=0.000632 (2^-10.63), power_index=0.166
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.3, luts=178, ffs=96, throughput_msps=11.7, max_abs_err=0.0004 (2^-11.29), power_index=0.175
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.5, luts=179, ffs=97, throughput_msps=11.7, max_abs_err=0.000342 (2^-11.51), power_index=0.177
Front coverage: luts_plus_ffs 251..276 (HV reference 1500); accuracy_bits 10.1..11.5 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- iterative: 50 evals, 15 feasible; max throughput seen 15.6 MSPS; best accuracy 11.51 bits; best feasible luts_plus_ffs=251; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard -1..1, frac_guard 0..1
- unrolled_k: 50 evals, 25 feasible; max throughput seen 14 MSPS; best accuracy 11.36 bits; best feasible luts_plus_ffs=357; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..1, frac_guard 0..2, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Add pipelined and pipelined_m families to explore high-throughput architectures that may offer better area/accuracy trade-offs than the current iterative/unrolled_k front.*)
- `iterative` (10 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (10 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 20 evaluations this round, 120 total; 51 feasible; hypervolume 1.201e+04 (+543.7%).

**LLM decision:** `stop` — The Pareto front is well-mapped and the constraints are comfortably met. The minimum area design (iterative, luts_plus_ffs=251) achieves 10.1 accuracy bits (max_abs_err ~2^-10.09), which satisfies the <= 2^-10 constraint, and provides 13.2 MSPS throughput, well above the 1 MSPS requirement. The front extends to 21.4 accuracy bits at 533 luts_plus_ffs, covering the trade-off space effectively. Since this is the final round, we stop.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.201e+04 (gain this round: +543.7%).
Feasible designs: 51 of 120 evaluations (40 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 25.4
- max_abs_err <= 0.000976562: 57% violate; best seen 3.6e-07 (2^-21.40)

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=251, accuracy_bits=10.1, luts=159, ffs=92, throughput_msps=13.2, max_abs_err=0.000917 (2^-10.09), power_index=0.141
- iterative [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=257, accuracy_bits=10.1, luts=161, ffs=96, throughput_msps=13.2, max_abs_err=0.000887 (2^-10.14), power_index=0.145
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.6, luts=168, ffs=92, throughput_msps=11.7, max_abs_err=0.000632 (2^-10.63), power_index=0.166
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.3, luts=178, ffs=96, throughput_msps=11.7, max_abs_err=0.0004 (2^-11.29), power_index=0.175
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.5, luts=179, ffs=97, throughput_msps=11.7, max_abs_err=0.000342 (2^-11.51), power_index=0.177
- iterative [data_width=20 n_iter=22 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=387, accuracy_bits=15.3, luts=266, ffs=121, throughput_msps=6.36, max_abs_err=2.4e-05 (2^-15.35), power_index=0.364
- iterative [data_width=21 n_iter=21 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=524, accuracy_bits=18.2, luts=391, ffs=133, throughput_msps=6.5, max_abs_err=3.39e-06 (2^-18.17), power_index=0.473
- iterative [data_width=26 n_iter=29 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=533, accuracy_bits=21.4, luts=382, ffs=151, throughput_msps=4.79, max_abs_err=3.6e-07 (2^-21.40), power_index=0.642
Front coverage: luts_plus_ffs 251..533 (HV reference 1500); accuracy_bits 10.1..21.4 (HV reference 10); data_width on the front 15..26 (registry 8..28).

Per family:
- iterative: 60 evals, 20 feasible; max throughput seen 25.4 MSPS; best accuracy 21.40 bits; best feasible luts_plus_ffs=251; feasible ranges: data_width 15..26, n_iter 12..29, angle_guard -1..4, frac_guard 0..4
- unrolled_k: 60 evals, 31 feasible; max throughput seen 16.6 MSPS; best accuracy 20.89 bits; best feasible luts_plus_ffs=357; feasible ranges: data_width 14..23, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, k 2..7
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `iterative` (80 evals): data_width=14..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (8 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 126 feasible; hypervolume 1.514e+04 (+26.0%).

**No LLM call** (code's front-mapping round): The Pareto front is well-mapped and the constraints are comfortably met. The minimum area design (iterative, luts_plus_ffs=251) achieves 10.1 accuracy bits (max_abs_err ~2^-10.09), which satisfies the <= 2^-10 constraint, and provides 13.2 MSPS throughput, well above the 1 MSPS requirement. The front extends to 21.4 accuracy bits at 533 luts_plus_ffs, covering the trade-off space effectively. Since this is the final round, we stop.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.514e+04 (gain this round: +26.0%).
Feasible designs: 126 of 200 evaluations (106 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 25.4
- max_abs_err <= 0.000976562: 37% violate; best seen 4.35e-08 (2^-24.45)

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=251, accuracy_bits=10.1, luts=159, ffs=92, throughput_msps=13.2, max_abs_err=0.000917 (2^-10.09), power_index=0.141
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.3, luts=178, ffs=96, throughput_msps=11.7, max_abs_err=0.0004 (2^-11.29), power_index=0.175
- iterative [data_width=18 n_iter=30 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=337, accuracy_bits=12.2, luts=228, ffs=109, throughput_msps=4.82, max_abs_err=0.000212 (2^-12.20), power_index=0.418
- iterative [data_width=20 n_iter=30 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=402, accuracy_bits=15.5, luts=280, ffs=122, throughput_msps=4.82, max_abs_err=2.15e-05 (2^-15.51), power_index=0.499
- iterative [data_width=20 n_iter=27 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=445, accuracy_bits=16.2, luts=324, ffs=121, throughput_msps=5.3, max_abs_err=1.37e-05 (2^-16.15), power_index=0.502
- iterative [data_width=20 n_iter=29 angle_guard=3 frac_guard=4 rounding=trunc] luts_plus_ffs=446, accuracy_bits=16.8, luts=318, ffs=128, throughput_msps=4.88, max_abs_err=8.49e-06 (2^-16.85), power_index=0.537
- iterative [data_width=22 n_iter=24 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=471, accuracy_bits=18.7, luts=334, ffs=136, throughput_msps=5.78, max_abs_err=2.39e-06 (2^-18.67), power_index=0.478
- iterative [data_width=25 n_iter=22 angle_guard=1 frac_guard=3 rounding=trunc] luts_plus_ffs=533, accuracy_bits=19.9, luts=383, ffs=149, throughput_msps=6.13, max_abs_err=1.02e-06 (2^-19.90), power_index=0.501
- iterative [data_width=25 n_iter=25 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=547, accuracy_bits=21.5, luts=396, ffs=151, throughput_msps=5.47, max_abs_err=3.42e-07 (2^-21.48), power_index=0.576
- iterative [data_width=28 n_iter=27 angle_guard=4 frac_guard=3 rounding=trunc] luts_plus_ffs=622, accuracy_bits=24.5, luts=455, ffs=167, throughput_msps=5.02, max_abs_err=4.35e-08 (2^-24.45), power_index=0.702
Front coverage: luts_plus_ffs 251..622 (HV reference 1500); accuracy_bits 10.1..24.5 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 140 evals, 95 feasible; max throughput seen 25.4 MSPS; best accuracy 24.45 bits; best feasible luts_plus_ffs=251; feasible ranges: data_width 15..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 60 evals, 31 feasible; max throughput seen 16.6 MSPS; best accuracy 20.89 bits; best feasible luts_plus_ffs=357; feasible ranges: data_width 14..23, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, k 2..7
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7057 in, 2235 out
- provider-reported cost: $0.0070
- full prompts and replies: `llm_trace.jsonl`

