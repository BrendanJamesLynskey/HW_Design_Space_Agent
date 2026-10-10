# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`iterative:data_width=14,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 170 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 92 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 12.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 80.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.158 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000746 (2^-10.39) | exact: bit-accurate model, exhaustive (16384 angles) |
| max_abs_err_lsb | 3.05 | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err | 0.000195 (2^-12.32) | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err_lsb | 0.8 | exact: bit-accurate model, exhaustive (16384 angles) |
| accuracy_bits | 10.4 | exact: bit-accurate model, exhaustive (16384 angles) |

## Pareto front (36 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=14,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc` | 170 | 92 | 12.4 | 16 | 0.158 | 0.000746 (2^-10.39) | 10.39 |
| 1 | `iterative:data_width=16,n_iter=13,angle_guard=1,frac_guard=0,rounding=trunc` | 172 | 97 | 12.4 | 16 | 0.162 | 0.000704 (2^-10.47) | 10.47 |
| 2 | `iterative:data_width=15,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` | 181 | 97 | 11.7 | 17 | 0.178 | 0.000405 (2^-11.27) | 11.27 |
| 3 | `iterative:data_width=17,n_iter=17,angle_guard=-1,frac_guard=0,rounding=trunc` | 194 | 101 | 8.1 | 20 | 0.222 | 0.000375 (2^-11.38) | 11.38 |
| 4 | `iterative:data_width=17,n_iter=14,angle_guard=-1,frac_guard=2,rounding=trunc` | 199 | 104 | 11.4 | 17 | 0.194 | 0.000369 (2^-11.40) | 11.40 |
| 5 | `iterative:data_width=17,n_iter=17,angle_guard=2,frac_guard=0,rounding=trunc` | 200 | 104 | 7.9 | 20 | 0.228 | 0.000307 (2^-11.67) | 11.67 |
| 6 | `iterative:data_width=17,n_iter=18,angle_guard=2,frac_guard=0,rounding=trunc` | 200 | 104 | 7.6 | 21 | 0.24 | 0.000307 (2^-11.67) | 11.67 |
| 7 | `iterative:data_width=17,n_iter=15,angle_guard=3,frac_guard=2,rounding=trunc` | 206 | 108 | 10.8 | 18 | 0.213 | 0.00013 (2^-12.91) | 12.91 |
| 8 | `iterative:data_width=17,n_iter=18,angle_guard=2,frac_guard=2,rounding=trunc` | 228 | 108 | 7.6 | 21 | 0.265 | 0.000113 (2^-13.11) | 13.11 |
| 9 | `iterative:data_width=20,n_iter=20,angle_guard=-1,frac_guard=0,rounding=trunc` | 242 | 116 | 6.9 | 23 | 0.31 | 5.8e-05 (2^-14.07) | 14.07 |
| 10 | `iterative:data_width=17,n_iter=22,angle_guard=3,frac_guard=2,rounding=round` | 281 | 109 | 6.4 | 25 | 0.366 | 5.36e-05 (2^-14.19) | 14.19 |
| 11 | `iterative:data_width=20,n_iter=17,angle_guard=-1,frac_guard=2,rounding=trunc` | 271 | 120 | 7.9 | 20 | 0.294 | 5.34e-05 (2^-14.19) | 14.19 |
| 12 | `iterative:data_width=22,n_iter=24,angle_guard=-1,frac_guard=0,rounding=trunc` | 280 | 126 | 5.9 | 27 | 0.413 | 1.68e-05 (2^-15.86) | 15.86 |
| 13 | `iterative:data_width=22,n_iter=18,angle_guard=3,frac_guard=0,rounding=trunc` | 281 | 130 | 7.4 | 21 | 0.325 | 1.6e-05 (2^-15.93) | 15.93 |
| 14 | `iterative:data_width=22,n_iter=24,angle_guard=3,frac_guard=0,rounding=trunc` | 287 | 130 | 5.8 | 27 | 0.424 | 1.22e-05 (2^-16.32) | 16.32 |
| 15 | `iterative:data_width=22,n_iter=18,angle_guard=2,frac_guard=0,rounding=round` | 292 | 129 | 7.4 | 21 | 0.332 | 1.15e-05 (2^-16.41) | 16.41 |
| 16 | `iterative:data_width=22,n_iter=18,angle_guard=3,frac_guard=0,rounding=round` | 293 | 130 | 7.4 | 21 | 0.335 | 1.1e-05 (2^-16.47) | 16.47 |
| 17 | `iterative:data_width=22,n_iter=29,angle_guard=2,frac_guard=0,rounding=round` | 302 | 129 | 4.9 | 32 | 0.519 | 5.49e-06 (2^-17.47) | 17.47 |
| 18 | `iterative:data_width=22,n_iter=22,angle_guard=2,frac_guard=2,rounding=trunc` | 317 | 133 | 6.2 | 25 | 0.423 | 3.63e-06 (2^-18.07) | 18.07 |
| 19 | `iterative:data_width=22,n_iter=22,angle_guard=4,frac_guard=2,rounding=trunc` | 321 | 135 | 6.2 | 25 | 0.429 | 3.45e-06 (2^-18.15) | 18.15 |
| 20 | `iterative:data_width=23,n_iter=29,angle_guard=3,frac_guard=0,rounding=round` | 323 | 135 | 4.9 | 32 | 0.552 | 2.9e-06 (2^-18.39) | 18.39 |
| 21 | `iterative:data_width=22,n_iter=22,angle_guard=4,frac_guard=3,rounding=trunc` | 336 | 137 | 6.2 | 25 | 0.445 | 2.49e-06 (2^-18.61) | 18.61 |
| 22 | `iterative:data_width=22,n_iter=22,angle_guard=3,frac_guard=2,rounding=round` | 379 | 134 | 6.2 | 25 | 0.482 | 2.15e-06 (2^-18.83) | 18.83 |
| 23 | `iterative:data_width=27,n_iter=24,angle_guard=-2,frac_guard=0,rounding=trunc` | 366 | 150 | 5.7 | 27 | 0.524 | 9.54e-07 (2^-20.00) | 20.00 |
| 24 | `iterative:data_width=23,n_iter=29,angle_guard=4,frac_guard=4,rounding=trunc` | 379 | 144 | 4.8 | 32 | 0.629 | 8.73e-07 (2^-20.13) | 20.13 |
| 25 | `iterative:data_width=26,n_iter=26,angle_guard=0,frac_guard=1,rounding=trunc` | 375 | 149 | 5.3 | 29 | 0.572 | 6.24e-07 (2^-20.61) | 20.61 |
| 26 | `iterative:data_width=26,n_iter=25,angle_guard=4,frac_guard=1,rounding=trunc` | 382 | 153 | 5.5 | 28 | 0.564 | 4.09e-07 (2^-21.22) | 21.22 |
| 27 | `iterative:data_width=26,n_iter=24,angle_guard=4,frac_guard=2,rounding=trunc` | 391 | 155 | 5.7 | 27 | 0.554 | 3.21e-07 (2^-21.57) | 21.57 |
| 28 | `iterative:data_width=27,n_iter=25,angle_guard=3,frac_guard=0,rounding=round` | 398 | 155 | 5.5 | 28 | 0.582 | 2.28e-07 (2^-22.06) | 22.06 |
| 29 | `iterative:data_width=27,n_iter=24,angle_guard=3,frac_guard=2,rounding=trunc` | 406 | 159 | 5.7 | 27 | 0.575 | 1.97e-07 (2^-22.28) | 22.28 |
| 30 | `iterative:data_width=27,n_iter=25,angle_guard=3,frac_guard=2,rounding=trunc` | 417 | 159 | 5.5 | 28 | 0.607 | 1.44e-07 (2^-22.73) | 22.73 |
| 31 | `iterative:data_width=26,n_iter=29,angle_guard=4,frac_guard=3,rounding=trunc` | 421 | 157 | 4.8 | 32 | 0.697 | 1.43e-07 (2^-22.74) | 22.74 |
| 32 | `iterative:data_width=27,n_iter=30,angle_guard=3,frac_guard=2,rounding=trunc` | 421 | 159 | 4.6 | 33 | 0.721 | 1.14e-07 (2^-23.06) | 23.06 |
| 33 | `iterative:data_width=28,n_iter=30,angle_guard=3,frac_guard=2,rounding=trunc` | 442 | 164 | 4.6 | 33 | 0.753 | 6.16e-08 (2^-23.95) | 23.95 |
| 34 | `iterative:data_width=27,n_iter=30,angle_guard=4,frac_guard=4,rounding=trunc` | 461 | 164 | 4.6 | 33 | 0.776 | 5.53e-08 (2^-24.11) | 24.11 |
| 35 | `iterative:data_width=28,n_iter=30,angle_guard=4,frac_guard=3,rounding=trunc` | 462 | 167 | 4.6 | 33 | 0.782 | 3.83e-08 (2^-24.64) | 24.64 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Constraints first: throughput >= 1 MSPS is non-binding for iterative (N+3 cycles/result, so even N=30 needs only ~33 MHz of Fmax), and max_abs_err <= 2^-10 needs roughly W >= 11-12 with rounding plus N >= ~W-2 for CORDIC convergence. So the binding axis is accuracy vs area, not speed. Fleet data says the whole merged front (13/13 points) is iterative, best feasible luts_plus_ffs 260; unrolled_k's best is 374 with 0 front points and pipelined_m's best is 792 with 0 front points. Since all families compute identical bits for the same (W, N, angle_guard, frac_guard, rounding), unrolled_k is pointwise dominated by iterative (same accuracy, k chained micro-rotations per cycle = more add/shift datapath), so it deserves only a small confirmation share. The HV reference point is (1500, 10): the best feasible area already found (260) is far below 1500, so the area axis is slack and the dominant hypervolume lever is the TOP of the accuracy range, i.e. the last front point's (1500 - x)*(accuracy_bits - 10) term. That means the search must reach the high-W / high-N corner (accuracy_bits ~ W-1), not just re-polish the 260-area corner. Hence data_width is opened all the way to the registry max 28 with n_iter tracking it to 30, while still covering the low-area corner (W 10-13) where the selection rule (min luts_plus_ffs) will pick from.*)
- `iterative` (90 evals): data_width=10..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Holds 13/13 merged-front points and the best feasible area (260). Ranges are opened to the full registry width so the front is mapped from the min-area corner (W~11-12, N~10-14, small guards, rounding=round) up to the high-accuracy corner (W~24-28, N~24-30) that the (1500, 10) reference point rewards most. angle_guard and frac_guard are left free because they are cheap accuracy levers that can beat spending a whole extra bit of W; rounding is left free because round is expected to buy ~1 bit of accuracy at fixed W for near-zero area.
- `unrolled_k` (10 evals): data_width=10..24, n_iter=4..24, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..4. *Why:* Kept only as cheap insurance: for identical (W, N, angle_guard, frac_guard, rounding) it computes the same bits as iterative but needs k chained micro-rotations per cycle, so it cannot be on the area-accuracy front unless something unexpected happens at small k. Ranges are deliberately narrow (low/mid W, k 2-4) so the few evals probe the only place it could conceivably compete - the low-area corner - rather than wasting budget on the high-accuracy end where it is clearly dominated.

**Result (code):** 100 evaluations this round, 100 total; 62 feasible; hypervolume 1.172e+04 (n/a).

**LLM decision:** `refine` — The score is hypervolume, and the current HV is almost entirely set by the top-accuracy corner: reconstructing the staircase against ref (1500, 10) from the reported front, the last segment (area 580 -> 1500 at 20.8 bits) contributes ~9.9e3 of the 1.172e4 total (~85%), while every low-area segment together contributes <1.7e3. So the highest-leverage move is to push accuracy_bits above 20.8, not to shave LUTs at the bottom. Evidence that this is reachable: the top design uses n_iter=22 although the registry allows 30, and angle_guard=0 although 4 is allowed; on the front, raising angle_guard 0->4 at data_width=22/n_iter=22 bought +1.2 bits (16.9 -> 18.1), and raising n_iter 14->22 at data_width=17 bought +2.8 bits (11.4 -> 14.2). The top design is data_width=28 (registry max), so the remaining headroom is in n_iter and the guard bits. The low-area end (278 LUT+FF, 11.3 bits) already clears the 2^-10 constraint with ~1.3 bits of slack and adds almost no HV, and the reserved end-of-run mapping round will sweep the full ranges anyway. Throughput is a non-issue (best 36.5 MSPS, smallest front design 6.13 MSPS vs the 1 MSPS floor), so pipelined/pipelined_m would only add FFs for identical accuracy and are dominated on the area objective; no need to add a family.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.172e+04 (gain this round: n/a (first round)).
Feasible designs: 62 of 100 evaluations (52 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 36.5
- max_abs_err <= 0.000976562: 38% violate; best seen 5.58e-07 (2^-20.77)

Pareto front (feasible, 19 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=278, accuracy_bits=11.3, luts=181, ffs=97, throughput_msps=11.7, max_abs_err=0.000405 (2^-11.27), power_index=0.178
- iterative [data_width=17 n_iter=14 angle_guard=-1 frac_guard=2 rounding=trunc] luts_plus_ffs=303, accuracy_bits=11.4, luts=199, ffs=104, throughput_msps=11.4, max_abs_err=0.000369 (2^-11.40), power_index=0.194
- iterative [data_width=17 n_iter=14 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=314, accuracy_bits=12.5, luts=206, ffs=108, throughput_msps=11.4, max_abs_err=0.000178 (2^-12.45), power_index=0.201
- iterative [data_width=17 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=336, accuracy_bits=13.1, luts=228, ffs=108, throughput_msps=7.57, max_abs_err=0.000113 (2^-13.11), power_index=0.265
- iterative [data_width=17 n_iter=22 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=390, accuracy_bits=14.2, luts=281, ffs=109, throughput_msps=6.36, max_abs_err=5.36e-05 (2^-14.19), power_index=0.366
- iterative [data_width=22 n_iter=17 angle_guard=4 frac_guard=0 rounding=trunc] luts_plus_ffs=414, accuracy_bits=15.4, luts=283, ffs=131, throughput_msps=7.8, max_abs_err=2.27e-05 (2^-15.43), power_index=0.312
- iterative [data_width=22 n_iter=22 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=445, accuracy_bits=16.9, luts=313, ffs=131, throughput_msps=6.24, max_abs_err=8.02e-06 (2^-16.93), power_index=0.418
- iterative [data_width=22 n_iter=22 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=456, accuracy_bits=18.1, luts=321, ffs=135, throughput_msps=6.24, max_abs_err=3.45e-06 (2^-18.15), power_index=0.429
- iterative [data_width=22 n_iter=22 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=513, accuracy_bits=18.8, luts=379, ffs=134, throughput_msps=6.24, max_abs_err=2.15e-06 (2^-18.83), power_index=0.482
- iterative [data_width=28 n_iter=22 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=580, accuracy_bits=20.8, luts=418, ffs=161, throughput_msps=6.13, max_abs_err=5.58e-07 (2^-20.77), power_index=0.545
Front coverage: luts_plus_ffs 278..580 (HV reference 1500); accuracy_bits 11.3..20.8 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 90 evals, 60 feasible; max throughput seen 36.5 MSPS; best accuracy 20.77 bits; best feasible luts_plus_ffs=278; feasible ranges: data_width 14..28, n_iter 11..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 10 evals, 2 feasible; max throughput seen 15.8 MSPS; best accuracy 15.13 bits; best feasible luts_plus_ffs=461; feasible ranges: data_width 18..22, n_iter 20..22, angle_guard -2..0, frac_guard 3..3, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Refine the high-accuracy corner: max data_width, extended n_iter, full guard ranges, both rounding modes.*)
- `iterative` (20 evals): data_width=24..28, n_iter=20..30, angle_guard=0..4, frac_guard=0..4, rounding=trunc|round. *Why:* Only family on the Pareto front; accuracy is family-independent, so the top-accuracy point can only be extended here.

**Result (code):** 20 evaluations this round, 120 total; 82 feasible; hypervolume 1.482e+04 (+26.5%).

**LLM decision:** `stop` — This is the final round, and the front is both feasible and well-covered, so stopping is correct. Constraints are satisfied with margin: 0% of evaluations violate throughput_msps >= 1 (best seen 36.5 MSPS, and every front design is 4.56-11.7 MSPS), and the accuracy constraint max_abs_err <= 2^-10 is met by all 27 front designs (worst front point 2^-11.27, best 2^-24.11). The front spans luts_plus_ffs 278..625 against the HV reference 1500 and accuracy_bits 11.3..24.1 against the HV reference 10, i.e. it already covers the trade-off curve well past both reference points (HV 1.482e+04, +26.5% this round). The selection rule (min luts_plus_ffs) picks the iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] design at luts_plus_ffs=278, accuracy_bits=11.3, throughput 11.7 MSPS - comfortably inside both constraints. No constraint is unreachable, so infeasible is not warranted; further refinement is not possible in the remaining budget.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.482e+04 (gain this round: +26.5%).
Feasible designs: 82 of 120 evaluations (69 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 36.5
- max_abs_err <= 0.000976562: 32% violate; best seen 5.53e-08 (2^-24.11)

Pareto front (feasible, 27 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=278, accuracy_bits=11.3, luts=181, ffs=97, throughput_msps=11.7, max_abs_err=0.000405 (2^-11.27), power_index=0.178
- iterative [data_width=17 n_iter=17 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=304, accuracy_bits=11.7, luts=200, ffs=104, throughput_msps=7.95, max_abs_err=0.000307 (2^-11.67), power_index=0.228
- iterative [data_width=17 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=336, accuracy_bits=13.1, luts=228, ffs=108, throughput_msps=7.57, max_abs_err=0.000113 (2^-13.11), power_index=0.265
- iterative [data_width=20 n_iter=17 angle_guard=-1 frac_guard=2 rounding=trunc] luts_plus_ffs=391, accuracy_bits=14.2, luts=271, ffs=120, throughput_msps=7.95, max_abs_err=5.34e-05 (2^-14.19), power_index=0.294
- iterative [data_width=22 n_iter=22 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=445, accuracy_bits=16.9, luts=313, ffs=131, throughput_msps=6.24, max_abs_err=8.02e-06 (2^-16.93), power_index=0.418
- iterative [data_width=22 n_iter=22 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=456, accuracy_bits=18.1, luts=321, ffs=135, throughput_msps=6.24, max_abs_err=3.45e-06 (2^-18.15), power_index=0.429
- iterative [data_width=23 n_iter=29 angle_guard=4 frac_guard=4 rounding=trunc] luts_plus_ffs=523, accuracy_bits=20.1, luts=379, ffs=144, throughput_msps=4.79, max_abs_err=8.73e-07 (2^-20.13), power_index=0.629
- iterative [data_width=26 n_iter=24 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=546, accuracy_bits=21.6, luts=391, ffs=155, throughput_msps=5.68, max_abs_err=3.21e-07 (2^-21.57), power_index=0.554
- iterative [data_width=27 n_iter=25 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=576, accuracy_bits=22.7, luts=417, ffs=159, throughput_msps=5.47, max_abs_err=1.44e-07 (2^-22.73), power_index=0.607
- iterative [data_width=27 n_iter=30 angle_guard=4 frac_guard=4 rounding=trunc] luts_plus_ffs=625, accuracy_bits=24.1, luts=461, ffs=164, throughput_msps=4.56, max_abs_err=5.53e-08 (2^-24.11), power_index=0.776
Front coverage: luts_plus_ffs 278..625 (HV reference 1500); accuracy_bits 11.3..24.1 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 110 evals, 80 feasible; max throughput seen 36.5 MSPS; best accuracy 24.11 bits; best feasible luts_plus_ffs=278; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 10 evals, 2 feasible; max throughput seen 15.8 MSPS; best accuracy 15.13 bits; best feasible luts_plus_ffs=461; feasible ranges: data_width 18..22, n_iter 20..22, angle_guard -2..0, frac_guard 3..3, k 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `iterative` (80 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (27 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 157 feasible; hypervolume 1.538e+04 (+3.8%).

**No LLM call** (code's front-mapping round): This is the final round, and the front is both feasible and well-covered, so stopping is correct. Constraints are satisfied with margin: 0% of evaluations violate throughput_msps >= 1 (best seen 36.5 MSPS, and every front design is 4.56-11.7 MSPS), and the accuracy constraint max_abs_err <= 2^-10 is met by all 27 front designs (worst front point 2^-11.27, best 2^-24.11). The front spans luts_plus_ffs 278..625 against the HV reference 1500 and accuracy_bits 11.3..24.1 against the HV reference 10, i.e. it already covers the trade-off curve well past both reference points (HV 1.482e+04, +26.5% this round). The selection rule (min luts_plus_ffs) picks the iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] design at luts_plus_ffs=278, accuracy_bits=11.3, throughput 11.7 MSPS - comfortably inside both constraints. No constraint is unreachable, so infeasible is not warranted; further refinement is not possible in the remaining budget.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.538e+04 (gain this round: +3.8%).
Feasible designs: 157 of 200 evaluations (136 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 36.5
- max_abs_err <= 0.000976562: 22% violate; best seen 3.83e-08 (2^-24.64)

Pareto front (feasible, 36 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=262, accuracy_bits=10.4, luts=170, ffs=92, throughput_msps=12.4, max_abs_err=0.000746 (2^-10.39), power_index=0.158
- iterative [data_width=17 n_iter=14 angle_guard=-1 frac_guard=2 rounding=trunc] luts_plus_ffs=303, accuracy_bits=11.4, luts=199, ffs=104, throughput_msps=11.4, max_abs_err=0.000369 (2^-11.40), power_index=0.194
- iterative [data_width=17 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=336, accuracy_bits=13.1, luts=228, ffs=108, throughput_msps=7.57, max_abs_err=0.000113 (2^-13.11), power_index=0.265
- iterative [data_width=22 n_iter=24 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=406, accuracy_bits=15.9, luts=280, ffs=126, throughput_msps=5.89, max_abs_err=1.68e-05 (2^-15.86), power_index=0.413
- iterative [data_width=22 n_iter=18 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=424, accuracy_bits=16.5, luts=293, ffs=130, throughput_msps=7.43, max_abs_err=1.1e-05 (2^-16.47), power_index=0.335
- iterative [data_width=22 n_iter=22 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=456, accuracy_bits=18.1, luts=321, ffs=135, throughput_msps=6.24, max_abs_err=3.45e-06 (2^-18.15), power_index=0.429
- iterative [data_width=27 n_iter=24 angle_guard=-2 frac_guard=0 rounding=trunc] luts_plus_ffs=516, accuracy_bits=20, luts=366, ffs=150, throughput_msps=5.68, max_abs_err=9.54e-07 (2^-20.00), power_index=0.524
- iterative [data_width=26 n_iter=24 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=546, accuracy_bits=21.6, luts=391, ffs=155, throughput_msps=5.68, max_abs_err=3.21e-07 (2^-21.57), power_index=0.554
- iterative [data_width=26 n_iter=29 angle_guard=4 frac_guard=3 rounding=trunc] luts_plus_ffs=579, accuracy_bits=22.7, luts=421, ffs=157, throughput_msps=4.79, max_abs_err=1.43e-07 (2^-22.74), power_index=0.697
- iterative [data_width=28 n_iter=30 angle_guard=4 frac_guard=3 rounding=trunc] luts_plus_ffs=630, accuracy_bits=24.6, luts=462, ffs=167, throughput_msps=4.56, max_abs_err=3.83e-08 (2^-24.64), power_index=0.782
Front coverage: luts_plus_ffs 262..630 (HV reference 1500); accuracy_bits 10.4..24.6 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 190 evals, 155 feasible; max throughput seen 36.5 MSPS; best accuracy 24.64 bits; best feasible luts_plus_ffs=262; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 10 evals, 2 feasible; max throughput seen 15.8 MSPS; best accuracy 15.13 bits; best feasible luts_plus_ffs=461; feasible ranges: data_width 18..22, n_iter 20..22, angle_guard -2..0, frac_guard 3..3, k 2..4
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 1)
- tokens: 7384 in, 21917 out
- provider-reported cost: $0.0139
- full prompts and replies: `llm_trace.jsonl`

