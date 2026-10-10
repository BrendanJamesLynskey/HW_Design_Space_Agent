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
`iterative:data_width=15,n_iter=12,angle_guard=2,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 161 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 93 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 13.2 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 15 | exact: schedule |
| latency_ns | 75.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.143 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000835 (2^-10.23) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.84 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00024 (2^-12.02) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.97 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.2 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (23 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=12,angle_guard=2,frac_guard=0,rounding=round` | 161 | 93 | 13.2 | 15 | 0.143 | 0.000835 (2^-10.23) | 10.23 |
| 1 | `iterative:data_width=15,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc` | 168 | 93 | 11.0 | 18 | 0.177 | 0.000822 (2^-10.25) | 10.25 |
| 2 | `iterative:data_width=16,n_iter=12,angle_guard=0,frac_guard=0,rounding=round` | 167 | 96 | 13.2 | 15 | 0.148 | 0.000712 (2^-10.46) | 10.46 |
| 3 | `iterative:data_width=15,n_iter=13,angle_guard=1,frac_guard=1,rounding=trunc` | 170 | 94 | 12.4 | 16 | 0.159 | 0.000689 (2^-10.50) | 10.50 |
| 4 | `iterative:data_width=16,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc` | 170 | 96 | 11.0 | 18 | 0.18 | 0.000643 (2^-10.60) | 10.60 |
| 5 | `iterative:data_width=15,n_iter=15,angle_guard=2,frac_guard=1,rounding=trunc` | 172 | 95 | 11.0 | 18 | 0.181 | 0.000567 (2^-10.78) | 10.78 |
| 6 | `iterative:data_width=15,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc` | 172 | 95 | 11.7 | 17 | 0.171 | 0.000567 (2^-10.78) | 10.78 |
| 7 | `iterative:data_width=16,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 178 | 96 | 11.0 | 18 | 0.185 | 0.000373 (2^-11.39) | 11.39 |
| 8 | `iterative:data_width=15,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc` | 181 | 97 | 11.0 | 18 | 0.188 | 0.000344 (2^-11.51) | 11.51 |
| 9 | `iterative:data_width=16,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 181 | 98 | 11.0 | 18 | 0.189 | 0.000285 (2^-11.78) | 11.78 |
| 10 | `iterative:data_width=17,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 189 | 101 | 10.4 | 19 | 0.207 | 0.000244 (2^-12.00) | 12.00 |
| 11 | `iterative:data_width=17,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 191 | 102 | 10.4 | 19 | 0.209 | 0.000149 (2^-12.71) | 12.71 |
| 12 | `iterative:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 202 | 107 | 10.8 | 18 | 0.209 | 0.000119 (2^-13.04) | 13.04 |
| 13 | `iterative:data_width=18,n_iter=15,angle_guard=2,frac_guard=1,rounding=trunc` | 206 | 110 | 10.8 | 18 | 0.214 | 0.000118 (2^-13.05) | 13.05 |
| 14 | `iterative:data_width=19,n_iter=15,angle_guard=2,frac_guard=0,rounding=trunc` | 208 | 113 | 10.8 | 18 | 0.217 | 0.000109 (2^-13.17) | 13.17 |
| 15 | `iterative:data_width=20,n_iter=15,angle_guard=-1,frac_guard=0,rounding=trunc` | 214 | 115 | 10.8 | 18 | 0.223 | 9.65e-05 (2^-13.34) | 13.34 |
| 16 | `iterative:data_width=18,n_iter=19,angle_guard=1,frac_guard=0,rounding=round` | 226 | 108 | 7.2 | 22 | 0.276 | 9.26e-05 (2^-13.40) | 13.40 |
| 17 | `iterative:data_width=18,n_iter=24,angle_guard=2,frac_guard=0,rounding=round` | 229 | 109 | 5.9 | 27 | 0.344 | 7.75e-05 (2^-13.65) | 13.65 |
| 18 | `iterative:data_width=19,n_iter=19,angle_guard=1,frac_guard=0,rounding=round` | 242 | 113 | 7.2 | 22 | 0.294 | 4.26e-05 (2^-14.52) | 14.52 |
| 19 | `iterative:data_width=23,n_iter=24,angle_guard=2,frac_guard=0,rounding=trunc` | 303 | 134 | 5.8 | 27 | 0.444 | 5.84e-06 (2^-17.39) | 17.39 |
| 20 | `iterative:data_width=23,n_iter=24,angle_guard=2,frac_guard=1,rounding=trunc` | 319 | 136 | 5.8 | 27 | 0.462 | 3.08e-06 (2^-18.31) | 18.31 |
| 21 | `iterative:data_width=27,n_iter=29,angle_guard=4,frac_guard=0,rounding=round` | 402 | 156 | 4.7 | 32 | 0.673 | 2.03e-07 (2^-22.23) | 22.23 |
| 22 | `iterative:data_width=27,n_iter=25,angle_guard=4,frac_guard=4,rounding=trunc` | 453 | 164 | 5.4 | 28 | 0.65 | 1.05e-07 (2^-23.18) | 23.18 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec's only hard constraints are throughput >= 1 MSPS and max_abs_err <= 2^-10; area is the sole real cost (objective min luts_plus_ffs, selection min luts_plus_ffs). The fleet data already shows iterative owns the entire merged front (23/23 designs, best feasible luts_plus_ffs 322) while pipelined/pipelined_m are far behind (1581 / 774). iterative also trivially clears the throughput bar: N+3 cycles/result at ~100+ MHz is several MSPS even for N=20, so unrolled_k's only advantage (fewer cycles/result) buys nothing here while it replicates the datapath k times for identical output bits. I therefore spend ~90% of the remaining budget refining/extending the iterative front and only ~10% probing unrolled_k to confirm it is dominated rather than assume it. Accuracy reasoning (from the stated model, not invented numbers): output LSB is 2^-(W-2), so half-LSB rounding error is 2^-(W-1) and the CORDIC residual is ~2^-N; meeting 2^-10 therefore needs W >= ~12 and N >= ~11, putting the low-area corner near W=12-13, N=12-14, while the HV reference point (area 1500, accuracy_bits 10) means the front should also be pushed to larger W/N where accuracy_bits climbs well above 10. angle_guard/frac_guard are included on both sides of 0 because they trade angle-path and x/y fractional width against area and are the cheapest knobs to shave LUTs+FFs at fixed W/N.*)
- `iterative` (90 evals): data_width=11..20, n_iter=9..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Proven front owner: 92/100 feasible, best luts_plus_ffs 322, all 23 merged-front points. Throughput is a non-issue (N+3 cycles/result >> 1 MSPS), so the whole trade-off is area vs accuracy. Ranges straddle the predicted feasibility boundary (W>=12, N>=11) to pin the minimum-area corner, and extend to W,N=20 so the front reaches high accuracy_bits toward the HV reference area of 1500. angle_guard -2..2 and frac_guard 0..2 let the search buy accuracy with the cheapest bits instead of raw W/N; rounding is left free since round costs little area but can rescue the W=12 corner.
- `unrolled_k` (10 evals): data_width=11..16, n_iter=10..16, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Cheap dominance check, not a front candidate. unrolled_k computes bit-identical results for the same (data_width, n_iter, angle_guard, frac_guard, rounding) but chains k micro-rotations per cycle, so it should carry strictly more LUTs at equal accuracy and be dominated in the (luts_plus_ffs, accuracy_bits) plane; its throughput edge is worthless against a 1 MSPS floor. Ranges are deliberately narrow and centred on the region where iterative is cheapest (W 11..16, N 10..16) with small k (2..4) so a handful of evals either confirms domination or reveals a surprise worth a later round.

**Result (code):** 100 evaluations this round, 100 total; 67 feasible; hypervolume 5398 (n/a).

**LLM decision:** `map_front` — Two of the four families (pipelined, pipelined_m) can be ruled out on the evidence: the throughput constraint is trivially met by the cheapest designs (min-area front point runs 13.2 MSPS vs the 1 MSPS requirement, best seen 16.2), so throughput is not binding and a per-cycle pipeline only adds FFs/LUTs that hurt the min-luts_plus_ffs objective and can't help HV (throughput is a constraint, not an axis). That leaves iterative as the family actually on the front, and the exact fit constraint is satisfiable at the low-area end (dw=15/n_iter=12 gives max_abs_err=2^-10.23 <= 2^-10 at luts_plus_ffs=253, which is also the selection-rule pick). The problem is coverage, not feasibility: the feasible front spans luts_plus_ffs 253..355 against an HV reference of 1500, and accuracy_bits only 10.2..14.5 while the registry (data_width up to 28, n_iter up to 30, angle_guard to +4, frac_guard to +4) can clearly push accuracy much higher; data_width on the front stops at 20 of a possible 28. So a large, all-feasible region of the (area, accuracy) plane is unmapped, and HV against (1500, 10) is dominated by the unclaimed high-accuracy part of the curve. This is exactly the map_front trigger, and it also matches the reserved end-of-budget step: NSGA-II over the full iterative ranges (and unrolled_k, which was feasible but never reached the front, as the only other area-competitive family), seeded with the current 18-point front, to extend accuracy upward and fill the area gap up to the 1500 reference.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 5398 (gain this round: n/a (first round)).
Feasible designs: 67 of 100 evaluations (59 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 16.2
- max_abs_err <= 0.000976562: 33% violate; best seen 4.26e-05 (2^-14.52)

Pareto front (feasible, 18 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=253, accuracy_bits=10.2, luts=161, ffs=93, throughput_msps=13.2, max_abs_err=0.000835 (2^-10.23), power_index=0.143
- iterative [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.5, luts=167, ffs=96, throughput_msps=13.2, max_abs_err=0.000712 (2^-10.46), power_index=0.148
- iterative [data_width=15 n_iter=15 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=267, accuracy_bits=10.8, luts=172, ffs=95, throughput_msps=11, max_abs_err=0.000567 (2^-10.78), power_index=0.181
- iterative [data_width=18 n_iter=15 angle_guard=-2 frac_guard=0 rounding=trunc] luts_plus_ffs=293, accuracy_bits=11.6, luts=189, ffs=104, throughput_msps=11, max_abs_err=0.000333 (2^-11.55), power_index=0.199
- iterative [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=299, accuracy_bits=12.2, luts=193, ffs=106, throughput_msps=11, max_abs_err=0.000206 (2^-12.25), power_index=0.202
- iterative [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=302, accuracy_bits=12.3, luts=195, ffs=107, throughput_msps=10.8, max_abs_err=0.000194 (2^-12.33), power_index=0.204
- iterative [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=309, accuracy_bits=13, luts=202, ffs=107, throughput_msps=10.8, max_abs_err=0.000119 (2^-13.04), power_index=0.209
- iterative [data_width=19 n_iter=15 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=321, accuracy_bits=13.2, luts=208, ffs=113, throughput_msps=10.8, max_abs_err=0.000109 (2^-13.17), power_index=0.217
- iterative [data_width=18 n_iter=19 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=334, accuracy_bits=13.4, luts=226, ffs=108, throughput_msps=7.23, max_abs_err=9.26e-05 (2^-13.40), power_index=0.276
- iterative [data_width=19 n_iter=19 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=355, accuracy_bits=14.5, luts=242, ffs=113, throughput_msps=7.23, max_abs_err=4.26e-05 (2^-14.52), power_index=0.294
Front coverage: luts_plus_ffs 253..355 (HV reference 1500); accuracy_bits 10.2..14.5 (HV reference 10); data_width on the front 15..20 (registry 8..28).

Per family:
- iterative: 90 evals, 63 feasible; max throughput seen 16.2 MSPS; best accuracy 14.52 bits; best feasible luts_plus_ffs=253; feasible ranges: data_width 15..20, n_iter 12..19, angle_guard -2..2, frac_guard 0..2
- unrolled_k: 10 evals, 4 feasible; max throughput seen 14 MSPS; best accuracy 11.57 bits; best feasible luts_plus_ffs=357; feasible ranges: data_width 14..16, n_iter 13..16, angle_guard 0..2, frac_guard 0..2, k 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `iterative` (20 evals): data_width=14..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (18 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 85 feasible; hypervolume 1.394e+04 (+158.2%).

**LLM decision:** `refine` — Budget: 80 of 200 evals left over ~2 rounds. HV jumped +158% this round, so the front is still moving fast and is worth refining rather than freezing now. Evidence: (1) 0% of evals violate throughput (need >=1 MSPS, best seen 16.2), so throughput is free and only area/accuracy matter; (2) 29% violate the error bound, and the selecting design is only 0.23 bits clear of it - the low-area corner is where refinement pays and where a missed smaller design would directly change the selected answer; (3) unrolled_k is strictly worse on area (best feasible luts_plus_ffs=357 vs iterative 253) and is not on the front, so it does not need budget; (4) the front already spans accuracy 10.2..23.2 against HV ref 10 and 253..617 against HV ref 1500, so coverage of the high-accuracy tail is adequate - the missing coverage is sub-253 area. After this refinement, the final round should be used to map the full iterative front (the only family on the front) seeded with the refined front.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.394e+04 (gain this round: +158.2%).
Feasible designs: 85 of 120 evaluations (77 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 16.2
- max_abs_err <= 0.000976562: 29% violate; best seen 1.05e-07 (2^-23.18)

Pareto front (feasible, 22 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=253, accuracy_bits=10.2, luts=161, ffs=93, throughput_msps=13.2, max_abs_err=0.000835 (2^-10.23), power_index=0.143
- iterative [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.5, luts=167, ffs=96, throughput_msps=13.2, max_abs_err=0.000712 (2^-10.46), power_index=0.148
- iterative [data_width=15 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=278, accuracy_bits=11.5, luts=181, ffs=97, throughput_msps=11, max_abs_err=0.000344 (2^-11.51), power_index=0.188
- iterative [data_width=18 n_iter=15 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=296, accuracy_bits=12.2, luts=191, ffs=105, throughput_msps=11, max_abs_err=0.000211 (2^-12.21), power_index=0.2
- iterative [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=302, accuracy_bits=12.3, luts=195, ffs=107, throughput_msps=10.8, max_abs_err=0.000194 (2^-12.33), power_index=0.204
- iterative [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=316, accuracy_bits=13.1, luts=206, ffs=110, throughput_msps=10.8, max_abs_err=0.000118 (2^-13.05), power_index=0.214
- iterative [data_width=20 n_iter=15 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=329, accuracy_bits=13.3, luts=214, ffs=115, throughput_msps=10.8, max_abs_err=9.65e-05 (2^-13.34), power_index=0.223
- iterative [data_width=18 n_iter=24 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=338, accuracy_bits=13.7, luts=229, ffs=109, throughput_msps=5.89, max_abs_err=7.75e-05 (2^-13.65), power_index=0.344
- iterative [data_width=23 n_iter=24 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=455, accuracy_bits=18.3, luts=319, ffs=136, throughput_msps=5.78, max_abs_err=3.08e-06 (2^-18.31), power_index=0.462
- iterative [data_width=27 n_iter=25 angle_guard=4 frac_guard=4 rounding=trunc] luts_plus_ffs=617, accuracy_bits=23.2, luts=453, ffs=164, throughput_msps=5.38, max_abs_err=1.05e-07 (2^-23.18), power_index=0.65
Front coverage: luts_plus_ffs 253..617 (HV reference 1500); accuracy_bits 10.2..23.2 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 110 evals, 81 feasible; max throughput seen 16.2 MSPS; best accuracy 23.18 bits; best feasible luts_plus_ffs=253; feasible ranges: data_width 15..27, n_iter 12..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 10 evals, 4 feasible; max throughput seen 14 MSPS; best accuracy 11.57 bits; best feasible luts_plus_ffs=357; feasible ranges: data_width 14..16, n_iter 13..16, angle_guard 0..2, frac_guard 0..2, k 2..3
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The whole feasible front is iterative-only and the selection rule (min luts_plus_ffs) lands at its low-area corner. That corner is also the riskiest: the winner (dw=15, n_iter=12, ag=2, fg=0, round) sits at 253 LUT+FF and max_abs_err=2^-10.23, only 0.23 bits above the 2^-10 constraint. The front below 300 is thin (253, 263, 278, 296) and the current lowest data_width on it is 15 while the registry allows 8, so a data_width 13-14 design with more iterations may satisfy 2^-10 at lower area but is not yet sampled. Narrowing to data_width 13..17 / n_iter 10..17 / guard 0..3 aims to pin the true low-area minimum before spending the reserved budget on a full front map.*)
- `iterative` (80 evals): data_width=13..17, n_iter=10..17, angle_guard=0..3, frac_guard=0..1, rounding=round|trunc. *Why:* Holds the selection target under the binding error constraint; only region that has produced the smallest feasible area.

**Result (code):** 80 evaluations this round, 200 total; 148 feasible; hypervolume 1.395e+04 (+0.1%).

**LLM decision:** `stop` — Budget is exhausted (200/200 evals, round 3 of 4) and the rules make this the final round, so only stop/infeasible are available. Infeasible is ruled out: the feasible front has 23 designs, throughput constraint is met by 100% of evaluations (best seen 16.2 MSPS vs the 1 MSPS floor) and max_abs_err reaches 2^-23.18, far below the 2^-10 limit (best feasible = 1.05e-07). The front also spans both objectives well: luts_plus_ffs 253..617 against the HV reference 1500, accuracy_bits 10.2..23.2 against the HV reference 10, with data_width 15..27 covered. The spec's selection rule (min luts_plus_ffs) is satisfied directly by the front's leading point — iterative [W=15, N=12, angle_guard=2, frac_guard=0, trunc/round=round] at luts_plus_ffs=253 (luts=161, ffs=93), throughput 13.2 MSPS >= 1, max_abs_err 0.000835 = 2^-10.23 <= 2^-10 — i.e. a design that meets every constraint while minimising the area proxy. The last round produced only +0.1% hypervolume, so returns are diminishing and further exploration is not warranted.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.395e+04 (gain this round: +0.1%).
Feasible designs: 148 of 200 evaluations (122 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 16.2
- max_abs_err <= 0.000976562: 26% violate; best seen 1.05e-07 (2^-23.18)

Pareto front (feasible, 23 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=253, accuracy_bits=10.2, luts=161, ffs=93, throughput_msps=13.2, max_abs_err=0.000835 (2^-10.23), power_index=0.143
- iterative [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.5, luts=167, ffs=96, throughput_msps=13.2, max_abs_err=0.000712 (2^-10.46), power_index=0.148
- iterative [data_width=15 n_iter=15 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=267, accuracy_bits=10.8, luts=172, ffs=95, throughput_msps=11, max_abs_err=0.000567 (2^-10.78), power_index=0.181
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.4, luts=178, ffs=96, throughput_msps=11, max_abs_err=0.000373 (2^-11.39), power_index=0.185
- iterative [data_width=17 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=290, accuracy_bits=12, luts=189, ffs=101, throughput_msps=10.4, max_abs_err=0.000244 (2^-12.00), power_index=0.207
- iterative [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=309, accuracy_bits=13, luts=202, ffs=107, throughput_msps=10.8, max_abs_err=0.000119 (2^-13.04), power_index=0.209
- iterative [data_width=20 n_iter=15 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=329, accuracy_bits=13.3, luts=214, ffs=115, throughput_msps=10.8, max_abs_err=9.65e-05 (2^-13.34), power_index=0.223
- iterative [data_width=18 n_iter=24 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=338, accuracy_bits=13.7, luts=229, ffs=109, throughput_msps=5.89, max_abs_err=7.75e-05 (2^-13.65), power_index=0.344
- iterative [data_width=23 n_iter=24 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=455, accuracy_bits=18.3, luts=319, ffs=136, throughput_msps=5.78, max_abs_err=3.08e-06 (2^-18.31), power_index=0.462
- iterative [data_width=27 n_iter=25 angle_guard=4 frac_guard=4 rounding=trunc] luts_plus_ffs=617, accuracy_bits=23.2, luts=453, ffs=164, throughput_msps=5.38, max_abs_err=1.05e-07 (2^-23.18), power_index=0.65
Front coverage: luts_plus_ffs 253..617 (HV reference 1500); accuracy_bits 10.2..23.2 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 190 evals, 144 feasible; max throughput seen 16.2 MSPS; best accuracy 23.18 bits; best feasible luts_plus_ffs=253; feasible ranges: data_width 15..27, n_iter 12..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 10 evals, 4 feasible; max throughput seen 14 MSPS; best accuracy 11.57 bits; best feasible luts_plus_ffs=357; feasible ranges: data_width 14..16, n_iter 13..16, angle_guard 0..2, frac_guard 0..2, k 2..3
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 10171 in, 12952 out
- provider-reported cost: $0.0089
- full prompts and replies: `llm_trace.jsonl`

