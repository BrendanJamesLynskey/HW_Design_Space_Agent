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
`iterative:data_width=16,n_iter=27,angle_guard=2,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 199 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 99 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 162 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 5.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 30 | exact: schedule |
| latency_ns | 185 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.336 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000285 (2^-11.78) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 4.67 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 7.17e-05 (2^-13.77) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 1.17 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 11.8 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (28 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=16,n_iter=27,angle_guard=2,frac_guard=0,rounding=round` | 199 | 99 | 5.4 | 30 | 0.336 | 0.000285 (2^-11.78) | 11.78 |
| 1 | `iterative:data_width=16,n_iter=22,angle_guard=1,frac_guard=2,rounding=trunc` | 210 | 102 | 6.5 | 25 | 0.294 | 0.000283 (2^-11.78) | 11.78 |
| 2 | `iterative:data_width=17,n_iter=30,angle_guard=0,frac_guard=0,rounding=round` | 213 | 102 | 4.9 | 33 | 0.39 | 0.000244 (2^-12.00) | 12.00 |
| 3 | `iterative:data_width=17,n_iter=28,angle_guard=4,frac_guard=0,rounding=round` | 218 | 106 | 5.1 | 31 | 0.378 | 0.000146 (2^-12.74) | 12.74 |
| 4 | `iterative:data_width=18,n_iter=22,angle_guard=2,frac_guard=1,rounding=trunc` | 231 | 111 | 6.4 | 25 | 0.322 | 0.000102 (2^-13.26) | 13.26 |
| 5 | `iterative:data_width=19,n_iter=28,angle_guard=0,frac_guard=1,rounding=trunc` | 245 | 114 | 5.1 | 31 | 0.419 | 8.95e-05 (2^-13.45) | 13.45 |
| 6 | `iterative:data_width=19,n_iter=28,angle_guard=1,frac_guard=1,rounding=trunc` | 247 | 115 | 5.1 | 31 | 0.422 | 7.32e-05 (2^-13.74) | 13.74 |
| 7 | `iterative:data_width=19,n_iter=22,angle_guard=2,frac_guard=1,rounding=trunc` | 249 | 116 | 6.4 | 25 | 0.343 | 4.92e-05 (2^-14.31) | 14.31 |
| 8 | `iterative:data_width=19,n_iter=22,angle_guard=2,frac_guard=2,rounding=trunc` | 265 | 118 | 6.4 | 25 | 0.36 | 3.04e-05 (2^-15.00) | 15.00 |
| 9 | `iterative:data_width=20,n_iter=22,angle_guard=2,frac_guard=1,rounding=trunc` | 266 | 121 | 6.4 | 25 | 0.364 | 2.4e-05 (2^-15.35) | 15.35 |
| 10 | `iterative:data_width=20,n_iter=26,angle_guard=1,frac_guard=2,rounding=trunc` | 280 | 122 | 5.5 | 29 | 0.439 | 1.79e-05 (2^-15.77) | 15.77 |
| 11 | `iterative:data_width=20,n_iter=26,angle_guard=2,frac_guard=2,rounding=trunc` | 282 | 123 | 5.5 | 29 | 0.442 | 1.75e-05 (2^-15.80) | 15.80 |
| 12 | `iterative:data_width=22,n_iter=26,angle_guard=0,frac_guard=0,rounding=trunc` | 282 | 127 | 5.5 | 29 | 0.446 | 1.56e-05 (2^-15.97) | 15.97 |
| 13 | `iterative:data_width=21,n_iter=22,angle_guard=1,frac_guard=2,rounding=trunc` | 298 | 127 | 6.2 | 25 | 0.4 | 9.95e-06 (2^-16.62) | 16.62 |
| 14 | `iterative:data_width=21,n_iter=22,angle_guard=2,frac_guard=2,rounding=trunc` | 300 | 128 | 6.2 | 25 | 0.402 | 7.43e-06 (2^-17.04) | 17.04 |
| 15 | `iterative:data_width=22,n_iter=26,angle_guard=2,frac_guard=1,rounding=trunc` | 303 | 131 | 5.4 | 29 | 0.473 | 7.16e-06 (2^-17.09) | 17.09 |
| 16 | `iterative:data_width=23,n_iter=19,angle_guard=2,frac_guard=1,rounding=trunc` | 310 | 136 | 7.1 | 22 | 0.369 | 5.7e-06 (2^-17.42) | 17.42 |
| 17 | `iterative:data_width=24,n_iter=27,angle_guard=0,frac_guard=0,rounding=trunc` | 320 | 137 | 5.2 | 30 | 0.516 | 3.78e-06 (2^-18.01) | 18.01 |
| 18 | `iterative:data_width=24,n_iter=27,angle_guard=-1,frac_guard=0,rounding=round` | 333 | 136 | 5.2 | 30 | 0.53 | 3.68e-06 (2^-18.05) | 18.05 |
| 19 | `iterative:data_width=25,n_iter=22,angle_guard=-2,frac_guard=0,rounding=trunc` | 331 | 140 | 6.2 | 25 | 0.443 | 3.54e-06 (2^-18.11) | 18.11 |
| 20 | `iterative:data_width=24,n_iter=23,angle_guard=2,frac_guard=0,rounding=round` | 334 | 139 | 6.0 | 26 | 0.463 | 1.57e-06 (2^-19.28) | 19.28 |
| 21 | `iterative:data_width=23,n_iter=23,angle_guard=3,frac_guard=3,rounding=trunc` | 352 | 141 | 6.0 | 26 | 0.482 | 1.25e-06 (2^-19.61) | 19.61 |
| 22 | `iterative:data_width=26,n_iter=22,angle_guard=1,frac_guard=0,rounding=trunc` | 354 | 148 | 6.1 | 25 | 0.472 | 1.09e-06 (2^-19.81) | 19.81 |
| 23 | `iterative:data_width=26,n_iter=22,angle_guard=3,frac_guard=1,rounding=trunc` | 373 | 152 | 6.1 | 25 | 0.494 | 7.61e-07 (2^-20.32) | 20.32 |
| 24 | `iterative:data_width=27,n_iter=24,angle_guard=4,frac_guard=0,rounding=trunc` | 377 | 156 | 5.6 | 27 | 0.541 | 4.11e-07 (2^-21.22) | 21.22 |
| 25 | `iterative:data_width=27,n_iter=29,angle_guard=4,frac_guard=0,rounding=round` | 402 | 156 | 4.7 | 32 | 0.673 | 2.03e-07 (2^-22.23) | 22.23 |
| 26 | `iterative:data_width=28,n_iter=28,angle_guard=4,frac_guard=1,rounding=trunc` | 420 | 163 | 4.9 | 31 | 0.681 | 9.79e-08 (2^-23.28) | 23.28 |
| 27 | `iterative:data_width=27,n_iter=29,angle_guard=2,frac_guard=4,rounding=trunc` | 457 | 162 | 4.7 | 32 | 0.746 | 8.91e-08 (2^-23.42) | 23.42 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The merged front is 17/17 iterative, and iterative also holds the lowest feasible area (269 vs 458 unrolled_k, 1068 pipelined_m, 1876 pipelined). The throughput constraint (>=1 MSPS) is trivially satisfied by iterative even at the slowest schedule (N=30 -> ~33 cycles/result, still tens of MSPS at Artix-7 Fmax), so the only binding constraint is accuracy (max_abs_err <= 2^-10, i.e. accuracy_bits >= 10) and the only objective that matters for selection is luts_plus_ffs. unrolled_k computes identical bits but chains k micro-rotations per cycle, so for the same (W,N) it costs ~k times the datapath and can never beat iterative on area; its 0/17 front membership confirms it is dominated. I therefore put ~95% of the budget on iterative and only a token share on unrolled_k to confirm no surprise. Ranges span the full useful W/N window so NSGA-II can trace the whole trade-off curve: the low-area corner (small W/N, guards minimal, round) that the selection rule will pick, up to the HV reference area (1500) where larger W/N push accuracy toward ~24 bits. angle_guard and frac_guard are opened over their full ranges because they trade area for accuracy independently of W/N and are the cheapest knobs near the accuracy boundary.*)
- `iterative` (95 evals): data_width=11..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Sole owner of the merged front and the area winner. Broad W/N range maps the full curve from the min-area feasible corner (~269 luts+ffs, ~10 bits) up to the HV reference area (1500, high accuracy). Full guard ranges let the search find the cheapest way to clear the 2^-10 error bound at each area point; both rounding modes included since round is essentially free accuracy near the boundary.
- `unrolled_k` (5 evals): data_width=11..18, n_iter=10..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Strictly dominated: identical bit-accurate results to iterative but k chained micro-rotations multiply the datapath, so it cannot win on luts_plus_ffs for any accuracy point, and throughput is not a binding constraint here. Token share only, restricted to the small-k / low-area corner where it is closest to iterative, to confirm the 0/17 front result before the reserved full-range mapping is spent elsewhere.

**Result (code):** 100 evaluations this round, 100 total; 76 feasible; hypervolume 1.403e+04 (n/a).

**LLM decision:** `map_front` — Round 1 shows a feasible front that is entirely iterative (unrolled_k: 0/5 feasible, best accuracy 9.56 bits < the required 10 bits, so nothing to add there yet) and covers luts_plus_ffs 298..584 against an HV reference of 1500, and accuracy_bits 11.8..23.3 against an HV reference of 10. Two things are clearly unmapped: (1) the low-accuracy band just above the constraint (accuracy_bits ~10..11.8), which is exactly where the spec's selection rule (min luts_plus_ffs, max_abs_err <= 2^-10) will land, so the 298 luts+ffs point is very likely not the true area floor; (2) the whole bandwidth of the trade-off curve below 298 and across 11.8 bits, even though throughput is a non-issue (best seen 15.6 MSPS vs >= 1 required) and 24% of round-1 samples already violated the error bound, leaving a lot of room near the accuracy constraint. With 100 of 200 evaluations remaining and the front spanning only one family and one corner of both objectives, mapping the full-range front seeded with these 21 designs is the highest-value use of the budget for hypervolume and for the selection rule alike; narrowing now would risk locking onto a non-minimal area point. Stop is premature (first round, all figures estimates) and infeasible is contradicted by 76 feasible evaluations.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.403e+04 (gain this round: n/a (first round)).
Feasible designs: 76 of 100 evaluations (71 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 24% violate; best seen 9.79e-08 (2^-23.28)

Pareto front (feasible, 21 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=27 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=298, accuracy_bits=11.8, luts=199, ffs=99, throughput_msps=5.4, max_abs_err=0.000285 (2^-11.78), power_index=0.336
- iterative [data_width=16 n_iter=24 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=333, accuracy_bits=12.4, luts=228, ffs=105, throughput_msps=5.89, max_abs_err=0.000186 (2^-12.39), power_index=0.338
- iterative [data_width=19 n_iter=28 angle_guard=4 frac_guard=0 rounding=trunc] luts_plus_ffs=353, accuracy_bits=13, luts=237, ffs=116, throughput_msps=5.03, max_abs_err=0.000125 (2^-12.97), power_index=0.411
- iterative [data_width=19 n_iter=28 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=362, accuracy_bits=13.7, luts=247, ffs=115, throughput_msps=5.13, max_abs_err=7.32e-05 (2^-13.74), power_index=0.422
- iterative [data_width=20 n_iter=28 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=382, accuracy_bits=14.3, luts=263, ffs=119, throughput_msps=5.13, max_abs_err=4.99e-05 (2^-14.29), power_index=0.445
- iterative [data_width=21 n_iter=30 angle_guard=4 frac_guard=0 rounding=trunc] luts_plus_ffs=398, accuracy_bits=14.9, luts=272, ffs=126, throughput_msps=4.73, max_abs_err=3.32e-05 (2^-14.88), power_index=0.494
- iterative [data_width=22 n_iter=26 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=409, accuracy_bits=16, luts=282, ffs=127, throughput_msps=5.48, max_abs_err=1.56e-05 (2^-15.97), power_index=0.446
- iterative [data_width=24 n_iter=27 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=457, accuracy_bits=18, luts=320, ffs=137, throughput_msps=5.2, max_abs_err=3.78e-06 (2^-18.01), power_index=0.516
- iterative [data_width=24 n_iter=24 angle_guard=1 frac_guard=4 rounding=trunc] luts_plus_ffs=528, accuracy_bits=19.8, luts=382, ffs=146, throughput_msps=5.68, max_abs_err=1.11e-06 (2^-19.78), power_index=0.536
- iterative [data_width=28 n_iter=28 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=584, accuracy_bits=23.3, luts=420, ffs=163, throughput_msps=4.86, max_abs_err=9.79e-08 (2^-23.28), power_index=0.681
Front coverage: luts_plus_ffs 298..584 (HV reference 1500); accuracy_bits 11.8..23.3 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- iterative: 95 evals, 76 feasible; max throughput seen 15.6 MSPS; best accuracy 23.28 bits; best feasible luts_plus_ffs=298; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 5 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 9.56 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `iterative` (20 evals): data_width=15..28, n_iter=21..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (21 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 95 feasible; hypervolume 1.414e+04 (+0.8%).

**LLM decision:** `map_front` — The feasible front is entirely `iterative` and covers only luts_plus_ffs 298..584 against the HV reference of 1500, and data_width 16..28 against the registry's 8..28 — i.e. only a small part of both the area and width ranges, while the accuracy axis (11.8..23.3 bits vs ref 10) is already well covered. The round-over-round HV gain is only +0.8%, so further hand-narrowing (refine) is unlikely to move the curve much; the reserved budget is better spent letting NSGA-II map the whole front over the full ranges of the family that actually appears on it (iterative), seeded with the current 24-point front. This will both probe the low-area corner around the selection target (best feasible luts_plus_ffs=298 at data_width=16, where accuracy 11.8 bits still has ~1.8 bits of margin over the 2^-10 constraint) and push the high-accuracy end (data_width up to 28, n_iter up to 30), which dominates the hypervolume since the rightmost front point contributes the (584..1500) x (10..23.3) rectangle. `unrolled_k` (5 evals, 0 feasible, best 9.56 bits) and the pipelined families are not needed: throughput is already 5.4 MSPS vs the 1 MSPS constraint, so their extra registers/shifters cannot beat iterative on the min-luts_plus_ffs objective.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.414e+04 (gain this round: +0.8%).
Feasible designs: 95 of 120 evaluations (85 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 21% violate; best seen 9.79e-08 (2^-23.28)

Pareto front (feasible, 24 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=27 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=298, accuracy_bits=11.8, luts=199, ffs=99, throughput_msps=5.4, max_abs_err=0.000285 (2^-11.78), power_index=0.336
- iterative [data_width=16 n_iter=27 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=348, accuracy_bits=12.5, luts=247, ffs=101, throughput_msps=5.4, max_abs_err=0.000177 (2^-12.47), power_index=0.392
- iterative [data_width=20 n_iter=25 angle_guard=-2 frac_guard=0 rounding=trunc] luts_plus_ffs=358, accuracy_bits=13, luts=243, ffs=115, throughput_msps=5.68, max_abs_err=0.000121 (2^-13.01), power_index=0.378
- iterative [data_width=19 n_iter=28 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=371, accuracy_bits=13.9, luts=252, ffs=118, throughput_msps=5.03, max_abs_err=6.72e-05 (2^-13.86), power_index=0.432
- iterative [data_width=21 n_iter=30 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=387, accuracy_bits=14.7, luts=265, ffs=122, throughput_msps=4.82, max_abs_err=3.78e-05 (2^-14.69), power_index=0.48
- iterative [data_width=22 n_iter=26 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=409, accuracy_bits=16, luts=282, ffs=127, throughput_msps=5.48, max_abs_err=1.56e-05 (2^-15.97), power_index=0.446
- iterative [data_width=22 n_iter=26 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=434, accuracy_bits=17.1, luts=303, ffs=131, throughput_msps=5.38, max_abs_err=7.16e-06 (2^-17.09), power_index=0.473
- iterative [data_width=24 n_iter=23 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=473, accuracy_bits=19.3, luts=334, ffs=139, throughput_msps=6, max_abs_err=1.57e-06 (2^-19.28), power_index=0.463
- iterative [data_width=26 n_iter=21 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=524, accuracy_bits=19.8, luts=373, ffs=151, throughput_msps=6.39, max_abs_err=1.1e-06 (2^-19.80), power_index=0.473
- iterative [data_width=28 n_iter=28 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=584, accuracy_bits=23.3, luts=420, ffs=163, throughput_msps=4.86, max_abs_err=9.79e-08 (2^-23.28), power_index=0.681
Front coverage: luts_plus_ffs 298..584 (HV reference 1500); accuracy_bits 11.8..23.3 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- iterative: 115 evals, 95 feasible; max throughput seen 15.6 MSPS; best accuracy 23.28 bits; best feasible luts_plus_ffs=298; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 5 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 9.56 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `iterative` (80 evals): data_width=15..28, n_iter=19..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (24 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 169 feasible; hypervolume 1.431e+04 (+1.2%).

**LLM decision:** `stop` — Budget is exhausted (200/200 evals, final round) and the constraints are demonstrably satisfiable: 169 of 200 evaluations are feasible, with 0% violating throughput_msps >= 1 (best 15.6 MSPS) and the best max_abs_err 8.91e-08 (2^-23.42) far inside the 2^-10 limit. The feasible Pareto front is well populated (28 designs, 148 unique feasible points) and spans luts_plus_ffs 298..619 against the HV reference 1500 and accuracy_bits 11.8..23.4 against the reference 10, so hypervolume is already large (1.431e+04) with only +1.2% gain this round — diminishing returns. The spec's selection rule (min luts_plus_ffs) is directly served by the front's corner design iterative [data_width=16 n_iter=27 angle_guard=2 frac_guard=0 rounding=round] at luts_plus_ffs=298, accuracy_bits=11.8 (max_abs_err 2^-11.78, still within the 2^-10 constraint) and 5.4 MSPS throughput. unrolled_k produced 0 feasible designs in its 5 evals, but this does not affect feasibility since iterative covers the whole trade-off curve. No further exploration is warranted.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.431e+04 (gain this round: +1.2%).
Feasible designs: 169 of 200 evaluations (148 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 16% violate; best seen 8.91e-08 (2^-23.42)

Pareto front (feasible, 28 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=27 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=298, accuracy_bits=11.8, luts=199, ffs=99, throughput_msps=5.4, max_abs_err=0.000285 (2^-11.78), power_index=0.336
- iterative [data_width=17 n_iter=28 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=324, accuracy_bits=12.7, luts=218, ffs=106, throughput_msps=5.13, max_abs_err=0.000146 (2^-12.74), power_index=0.378
- iterative [data_width=19 n_iter=28 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=362, accuracy_bits=13.7, luts=247, ffs=115, throughput_msps=5.13, max_abs_err=7.32e-05 (2^-13.74), power_index=0.422
- iterative [data_width=20 n_iter=22 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=387, accuracy_bits=15.3, luts=266, ffs=121, throughput_msps=6.36, max_abs_err=2.4e-05 (2^-15.35), power_index=0.364
- iterative [data_width=22 n_iter=26 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=409, accuracy_bits=16, luts=282, ffs=127, throughput_msps=5.48, max_abs_err=1.56e-05 (2^-15.97), power_index=0.446
- iterative [data_width=22 n_iter=26 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=434, accuracy_bits=17.1, luts=303, ffs=131, throughput_msps=5.38, max_abs_err=7.16e-06 (2^-17.09), power_index=0.473
- iterative [data_width=24 n_iter=27 angle_guard=-1 frac_guard=0 rounding=round] luts_plus_ffs=469, accuracy_bits=18.1, luts=333, ffs=136, throughput_msps=5.2, max_abs_err=3.68e-06 (2^-18.05), power_index=0.53
- iterative [data_width=23 n_iter=23 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=493, accuracy_bits=19.6, luts=352, ffs=141, throughput_msps=6, max_abs_err=1.25e-06 (2^-19.61), power_index=0.482
- iterative [data_width=27 n_iter=24 angle_guard=4 frac_guard=0 rounding=trunc] luts_plus_ffs=533, accuracy_bits=21.2, luts=377, ffs=156, throughput_msps=5.58, max_abs_err=4.11e-07 (2^-21.22), power_index=0.541
- iterative [data_width=27 n_iter=29 angle_guard=2 frac_guard=4 rounding=trunc] luts_plus_ffs=619, accuracy_bits=23.4, luts=457, ffs=162, throughput_msps=4.7, max_abs_err=8.91e-08 (2^-23.42), power_index=0.746
Front coverage: luts_plus_ffs 298..619 (HV reference 1500); accuracy_bits 11.8..23.4 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- iterative: 195 evals, 169 feasible; max throughput seen 15.6 MSPS; best accuracy 23.42 bits; best feasible luts_plus_ffs=298; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 5 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 9.56 bits
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 11916 in, 12078 out
- provider-reported cost: $0.0087
- full prompts and replies: `llm_trace.jsonl`

