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
`unrolled_k:data_width=15,n_iter=13,angle_guard=0,frac_guard=0,rounding=round,k=2` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 246 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 90 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 105 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 10.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 10 | exact: schedule |
| latency_ns | 94.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.126 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000879 (2^-10.15) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 7.2 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00022 (2^-12.15) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.8 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.2 | exact: bit-accurate model, exhaustive (32768 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 10 cycles, a new input every 10 cycle(s). DDS tone from its exact outputs: SFDR 83.5 dBc, SNR 70.9 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (22 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `unrolled_k:data_width=15,n_iter=13,angle_guard=0,frac_guard=0,rounding=round,k=2` | 246 | 90 | 10.5 | 10 | 0.126 | 0.000879 (2^-10.15) | 10.15 |
| 1 | `unrolled_k:data_width=15,n_iter=13,angle_guard=1,frac_guard=0,rounding=round,k=2` | 249 | 91 | 10.5 | 10 | 0.128 | 0.000673 (2^-10.54) | 10.54 |
| 2 | `unrolled_k:data_width=15,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,k=2` | 253 | 93 | 10.5 | 10 | 0.13 | 0.000594 (2^-10.72) | 10.72 |
| 3 | `unrolled_k:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,k=2` | 262 | 95 | 10.5 | 10 | 0.134 | 0.0004 (2^-11.29) | 11.29 |
| 4 | `unrolled_k:data_width=16,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,k=2` | 270 | 98 | 10.5 | 10 | 0.138 | 0.000344 (2^-11.50) | 11.50 |
| 5 | `unrolled_k:data_width=17,n_iter=14,angle_guard=0,frac_guard=0,rounding=trunc,k=2` | 270 | 100 | 10.5 | 10 | 0.139 | 0.000338 (2^-11.53) | 11.53 |
| 6 | `unrolled_k:data_width=17,n_iter=15,angle_guard=-1,frac_guard=0,rounding=round,k=2` | 275 | 99 | 9.6 | 11 | 0.155 | 0.000334 (2^-11.55) | 11.55 |
| 7 | `unrolled_k:data_width=17,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,k=2` | 279 | 100 | 10.5 | 10 | 0.142 | 0.000301 (2^-11.70) | 11.70 |
| 8 | `unrolled_k:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,k=2` | 282 | 101 | 10.5 | 10 | 0.144 | 0.000204 (2^-12.26) | 12.26 |
| 9 | `unrolled_k:data_width=18,n_iter=22,angle_guard=3,frac_guard=0,rounding=trunc,k=2` | 311 | 109 | 7.3 | 14 | 0.221 | 0.0002 (2^-12.28) | 12.28 |
| 10 | `unrolled_k:data_width=17,n_iter=16,angle_guard=1,frac_guard=1,rounding=round,k=2` | 331 | 103 | 9.6 | 11 | 0.179 | 0.000128 (2^-12.94) | 12.94 |
| 11 | `unrolled_k:data_width=19,n_iter=20,angle_guard=1,frac_guard=0,rounding=round,k=2` | 336 | 112 | 7.9 | 13 | 0.219 | 4.26e-05 (2^-14.52) | 14.52 |
| 12 | `unrolled_k:data_width=19,n_iter=21,angle_guard=2,frac_guard=0,rounding=round,k=2` | 340 | 113 | 7.3 | 14 | 0.238 | 3.86e-05 (2^-14.66) | 14.66 |
| 13 | `unrolled_k:data_width=19,n_iter=20,angle_guard=2,frac_guard=0,rounding=round,k=2` | 340 | 113 | 7.9 | 13 | 0.221 | 3.86e-05 (2^-14.66) | 14.66 |
| 14 | `unrolled_k:data_width=20,n_iter=28,angle_guard=0,frac_guard=2,rounding=trunc,k=2` | 374 | 120 | 6.0 | 17 | 0.316 | 3.85e-05 (2^-14.67) | 14.67 |
| 15 | `unrolled_k:data_width=19,n_iter=27,angle_guard=1,frac_guard=1,rounding=round,k=2` | 396 | 114 | 6.0 | 17 | 0.326 | 3.6e-05 (2^-14.76) | 14.76 |
| 16 | `unrolled_k:data_width=19,n_iter=27,angle_guard=1,frac_guard=2,rounding=round,k=2` | 412 | 116 | 6.0 | 17 | 0.338 | 3.12e-05 (2^-14.97) | 14.97 |
| 17 | `unrolled_k:data_width=25,n_iter=24,angle_guard=-2,frac_guard=0,rounding=round,k=2` | 445 | 139 | 6.7 | 15 | 0.329 | 3.54e-06 (2^-18.11) | 18.11 |
| 18 | `unrolled_k:data_width=25,n_iter=21,angle_guard=-1,frac_guard=0,rounding=round,k=2` | 448 | 140 | 7.2 | 14 | 0.31 | 2.56e-06 (2^-18.58) | 18.58 |
| 19 | `unrolled_k:data_width=28,n_iter=28,angle_guard=1,frac_guard=0,rounding=round,k=2` | 538 | 157 | 5.8 | 17 | 0.445 | 1.32e-07 (2^-22.85) | 22.85 |
| 20 | `unrolled_k:data_width=27,n_iter=27,angle_guard=2,frac_guard=2,rounding=round,k=3` | 778 | 157 | 5.6 | 12 | 0.422 | 9.22e-08 (2^-23.37) | 23.37 |
| 21 | `pipelined_m:data_width=27,n_iter=29,angle_guard=4,frac_guard=3,rounding=round,m=8` | 2924 | 446 | 44.0 | 6 | 0.127 | 4.32e-08 (2^-24.46) | 24.46 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-dominated (min luts_plus_ffs) with a hard throughput floor of 1 MSPS and a hard accuracy floor of 2^-10. The iterative family is excluded: at 1 result/cycle it cannot reach 1 MSPS on Artix-7, so it cannot satisfy the throughput constraint. That leaves the three 1/cycle-capable families. pipelined_m is the primary area/throughput trade-off (FFs vs Fmax), pipelined is the high-Fmax anchor, and unrolled_k is the low-FF challenger. I bound data_width to 12..18 and n_iter to 10..16 because accuracy depends only on these plus the guards: W=12 already gives an output LSB of 2^-10, and N=10..16 with small guards comfortably meets err <= 2^-10 while leaving room to push accuracy_bits above the HV reference of 10. Guards are kept small (0..2) since area is the objective and large guards only add LUTs/FFs for accuracy we do not need. Rounding is left to both choices so the search can pick the cheaper trunc where it still meets the error bound. Budget is weighted toward pipelined_m (45%) as the expected winner, with pipelined (35%) and unrolled_k (20%) to map the rest of the front.*)
- `pipelined_m` (45 evals): data_width=12..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Meets throughput (1 result/cycle) and is the area-optimal way to get 1/cycle throughput: it registers every m stages, drastically cutting FFs vs full pipelined while keeping the 1/cycle schedule. m=2..4 balances the FF count against the critical path (Fmax) needed to hold >=1 MSPS. W=12..18 and N=10..16 cover the accuracy requirement (err <= 2^-10) with margin to explore the accuracy_bits objective.
- `pipelined` (35 evals): data_width=12..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* The reference 1/cycle architecture. It has the most FFs (one register per stage) but the shortest per-stage critical path, so it is the safe anchor for the throughput constraint and the high-Fmax / high-accuracy corner of the front. Comparing it against pipelined_m lets the search find where the FF savings of m-staging start to hurt Fmax.
- `unrolled_k` (20 evals): data_width=12..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Shared datapath with k rotations/cycle uses far fewer FFs than the pipelined families (only a small FSM + a few registers). It can plausibly hit >=1 MSPS if Fmax x k >= 1, making it a strong low-area candidate. k=2..4 keeps the per-cycle critical path manageable. This is the main competitor for the min-luts_plus_ffs selection rule, so it must be explored to map the true low-area end of the front.

**Result (code):** 100 evaluations this round, 100 total; 69 feasible; hypervolume 2533 (n/a).

**LLM decision:** `refine` — The current front spans luts_plus_ffs 378-1276 and accuracy_bits 10.6-13.5, but there are gaps: unrolled_k maxes out at ~11.9 bits accuracy, pipelined_m starts at 924 area, and pipelined is much larger. The 31% constraint violation rate on accuracy suggests many designs are too inaccurate, so we need to explore the accuracy-area trade-off more densely. Refining all three families around their promising regions with tighter ranges will focus the budget on filling these gaps and improving hypervolume coverage. The iterative family is not needed because it has the lowest throughput (1 result per N+3 cycles) and would likely violate the 1 MSPS constraint for most parameter settings, making it a poor fit for this spec.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 2533 (gain this round: n/a (first round)).
Feasible designs: 69 of 100 evaluations (48 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 31% violate; best seen 8.35e-05 (2^-13.55)

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=16 n_iter=12 angle_guard=1 frac_guard=0 rounding=round k=3] luts_plus_ffs=378, accuracy_bits=10.6, luts=283, ffs=95, throughput_msps=13.5, max_abs_err=0.000661 (2^-10.56), power_index=0.0996
- unrolled_k [data_width=17 n_iter=13 angle_guard=0 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=385, accuracy_bits=11.3, luts=283, ffs=102, throughput_msps=10.5, max_abs_err=0.000395 (2^-11.30), power_index=0.145
- unrolled_k [data_width=17 n_iter=13 angle_guard=0 frac_guard=1 rounding=round k=2] luts_plus_ffs=430, accuracy_bits=11.4, luts=328, ffs=102, throughput_msps=10.5, max_abs_err=0.000381 (2^-11.36), power_index=0.162
- unrolled_k [data_width=17 n_iter=13 angle_guard=0 frac_guard=2 rounding=round k=2] luts_plus_ffs=445, accuracy_bits=11.4, luts=341, ffs=104, throughput_msps=10.3, max_abs_err=0.000365 (2^-11.42), power_index=0.167
- unrolled_k [data_width=16 n_iter=16 angle_guard=1 frac_guard=0 rounding=round k=3] luts_plus_ffs=453, accuracy_bits=11.7, luts=357, ffs=96, throughput_msps=7.97, max_abs_err=0.000301 (2^-11.70), power_index=0.153
- unrolled_k [data_width=18 n_iter=13 angle_guard=2 frac_guard=2 rounding=round k=4] luts_plus_ffs=589, accuracy_bits=11.9, luts=479, ffs=110, throughput_msps=9.97, max_abs_err=0.000266 (2^-11.88), power_index=0.155
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1090, accuracy_bits=12.3, luts=813, ffs=276, throughput_msps=93.6, max_abs_err=0.000194 (2^-12.33), power_index=0.041
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1145, accuracy_bits=12.5, luts=855, ffs=291, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.53), power_index=0.0431
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=0.0472
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1276, accuracy_bits=13.5, luts=985, ffs=291, throughput_msps=93.6, max_abs_err=8.35e-05 (2^-13.55), power_index=0.048
Front coverage: luts_plus_ffs 378..1276 (HV reference 1500); accuracy_bits 10.6..13.5 (HV reference 10); data_width on the front 16..18 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 13 feasible; max throughput seen 13.5 MSPS; best accuracy 11.88 bits; best feasible luts_plus_ffs=378; feasible ranges: data_width 14..18, n_iter 12..16, angle_guard 0..2, frac_guard 0..2, k 2..4
- pipelined: 35 evals, 25 feasible; max throughput seen 282 MSPS; best accuracy 13.35 bits; best feasible luts_plus_ffs=1297; feasible ranges: data_width 14..18, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 45 evals, 31 feasible; max throughput seen 178 MSPS; best accuracy 13.55 bits; best feasible luts_plus_ffs=924; feasible ranges: data_width 15..18, n_iter 13..16, angle_guard 0..2, frac_guard 0..1, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The current front spans luts_plus_ffs 378-1276 and accuracy_bits 10.6-13.5, but there are gaps: unrolled_k maxes out at ~11.9 bits accuracy, pipelined_m starts at 924 area, and pipelined is much larger. The 31% constraint violation rate on accuracy suggests many designs are too inaccurate, so we need to explore the accuracy-area trade-off more densely. Refining all three families around their promising regions with tighter ranges will focus the budget on filling these gaps and improving hypervolume coverage. The iterative family is not needed because it has the lowest throughput (1 result per N+3 cycles) and would likely violate the 1 MSPS constraint for most parameter settings, making it a poor fit for this spec.*)
- `unrolled_k` (40 evals): data_width=15..17, n_iter=11..14, angle_guard=-1..1, frac_guard=0..1, rounding=trunc|round, k=2..3. *Why:* unrolled_k holds the area minimum (378) but its accuracy ceiling is low (~11.9 bits). Narrowing data_width to 15-17 and n_iter to 11-14 while allowing angle_guard down to -1 explores the trade-off between area and accuracy more densely in the region where unrolled_k is competitive.
- `pipelined_m` (35 evals): data_width=15..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..1, rounding=trunc|round, m=2..4. *Why:* pipelined_m offers the best accuracy (13.55 bits) at moderate area (924+). Refining around the current front (data_width 15-18, n_iter 12-16) with m in 2-4 helps map the accuracy-area trade-off more completely, especially the mid-range where pipelined_m might undercut pipelined on area while maintaining high throughput.
- `pipelined` (25 evals): data_width=14..18, n_iter=11..16, angle_guard=-1..2, frac_guard=0..1, rounding=trunc|round. *Why:* pipelined has the highest throughput (282 MSPS) but the worst area (1297+). Exploring lower n_iter (11-16) and angle_guard down to -1 may reveal pipelined designs that are more area-efficient while still meeting the 1 MSPS constraint, potentially filling the gap between unrolled_k and pipelined_m on the front.

**Result (code):** 100 evaluations this round, 200 total; 153 feasible; hypervolume 2993 (+18.2%).

**LLM decision:** `refine` — The front is promising but sparse in the mid-area range (434-799 luts_plus_ffs). unrolled_k dominates the low-area end (336-434) and pipelined_m the high-accuracy end (799-1276). Refining all three families on their proven feasible ranges will densely map the transition region and solidify both ends of the front, maximizing hypervolume. iterative is not needed because it would be dominated by unrolled_k on throughput and area for the same accuracy.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 2993 (gain this round: +18.2%).
Feasible designs: 153 of 200 evaluations (118 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 24% violate; best seen 8.35e-05 (2^-13.55)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round k=2] luts_plus_ffs=336, accuracy_bits=10.2, luts=246, ffs=90, throughput_msps=10.5, max_abs_err=0.000879 (2^-10.15), power_index=0.126
- unrolled_k [data_width=15 n_iter=13 angle_guard=1 frac_guard=0 rounding=round k=2] luts_plus_ffs=340, accuracy_bits=10.5, luts=249, ffs=91, throughput_msps=10.5, max_abs_err=0.000673 (2^-10.54), power_index=0.128
- unrolled_k [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round k=2] luts_plus_ffs=357, accuracy_bits=11.3, luts=262, ffs=95, throughput_msps=10.5, max_abs_err=0.0004 (2^-11.29), power_index=0.134
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=368, accuracy_bits=11.5, luts=270, ffs=98, throughput_msps=10.5, max_abs_err=0.000344 (2^-11.50), power_index=0.138
- unrolled_k [data_width=17 n_iter=14 angle_guard=0 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=370, accuracy_bits=11.5, luts=270, ffs=100, throughput_msps=10.5, max_abs_err=0.000338 (2^-11.53), power_index=0.139
- unrolled_k [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round k=2] luts_plus_ffs=383, accuracy_bits=12.3, luts=282, ffs=101, throughput_msps=10.5, max_abs_err=0.000204 (2^-12.26), power_index=0.144
- unrolled_k [data_width=17 n_iter=14 angle_guard=1 frac_guard=1 rounding=round k=2] luts_plus_ffs=434, accuracy_bits=12.3, luts=331, ffs=103, throughput_msps=10.5, max_abs_err=0.000192 (2^-12.35), power_index=0.163
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1145, accuracy_bits=12.5, luts=855, ffs=291, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.53), power_index=0.0431
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=0.0472
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1276, accuracy_bits=13.5, luts=985, ffs=291, throughput_msps=93.6, max_abs_err=8.35e-05 (2^-13.55), power_index=0.048
Front coverage: luts_plus_ffs 336..1276 (HV reference 1500); accuracy_bits 10.2..13.5 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- unrolled_k: 60 evals, 47 feasible; max throughput seen 13.5 MSPS; best accuracy 12.35 bits; best feasible luts_plus_ffs=336; feasible ranges: data_width 14..18, n_iter 12..16, angle_guard -1..2, frac_guard 0..2, k 2..4
- pipelined: 60 evals, 43 feasible; max throughput seen 282 MSPS; best accuracy 13.35 bits; best feasible luts_plus_ffs=1293; feasible ranges: data_width 14..18, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 80 evals, 63 feasible; max throughput seen 178 MSPS; best accuracy 13.55 bits; best feasible luts_plus_ffs=799; feasible ranges: data_width 15..18, n_iter 12..16, angle_guard 0..2, frac_guard 0..1, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The front currently spans luts_plus_ffs 336..1276 and accuracy_bits 10.2..13.5. The selection rule is min luts_plus_ffs, so the low-area end (unrolled_k) is most critical. However, hypervolume rewards covering the whole trade-off curve. The gap between 434 (unrolled_k max) and 799 (pipelined_m min) is sparse. Refining all three families on their proven feasible ranges will densely map this transition region and solidify both ends of the front. iterative is not needed because it has the lowest throughput (1 result every N+3 cycles) and would likely be dominated by unrolled_k (k=2) on both area and throughput for the same accuracy. The 24% constraint violation rate on max_abs_err is expected in the search space but the feasible designs already achieve up to 13.55 bits, well above the 10-bit requirement, so the constraint is easily satisfiable.*)
- `unrolled_k` (20 evals): data_width=14..17, n_iter=13..16, angle_guard=-1..1, frac_guard=0..1, rounding=trunc|round, k=2..2. *Why:* unrolled_k dominates the low-area end of the front (336-434 luts_plus_ffs) and comfortably meets throughput (10.5 MSPS). The current front is sparse between 434 and 799. Narrowing to the proven feasible region (data_width 14-17, n_iter 13-16, k=2) and focusing on the accuracy/area trade-off (angle_guard -1..1, frac_guard 0..1) will densely map the critical low-area segment where the selection rule (min luts_plus_ffs) operates.
- `pipelined_m` (12 evals): data_width=15..18, n_iter=13..16, angle_guard=0..2, frac_guard=0..1, rounding=trunc|round, m=2..4. *Why:* pipelined_m provides the high-accuracy end (up to 13.55 bits) and has a best feasible area of 799, bridging the gap to unrolled_k. Refining around the proven feasible ranges (data_width 15-18, n_iter 13-16, m 2-4) will solidify the high-accuracy corner of the front and ensure the hypervolume captures the full trade-off curve up to the accuracy limit.
- `pipelined` (8 evals): data_width=15..18, n_iter=13..16, angle_guard=0..2, frac_guard=0..1, rounding=trunc|round. *Why:* pipelined has the highest throughput (282 MSPS) but the worst area on the front (1293). It is less critical for the low-area objective but helps complete the front's high-throughput/high-accuracy region. A small budget share ensures we don't miss any Pareto-optimal points in this family that might bridge the gap between pipelined_m and the high-accuracy end.

**Result (code):** 40 evaluations this round, 240 total; 187 feasible; hypervolume 3437 (+14.9%).

**LLM decision:** `stop` — The Pareto front is well-mapped and satisfies all constraints. The minimum area design (unrolled_k, luts_plus_ffs=336) meets the throughput constraint (10.5 MSPS >= 1 MSPS) and the accuracy constraint (max_abs_err=0.000879 <= 0.000976562). The front spans a wide range of accuracy (10.2 to 13.5 bits) and area (336 to 1276), providing a good trade-off curve for the hypervolume objective. Since this is the final round and the selection rule (min luts_plus_ffs) is clearly satisfied by the existing front, no further exploration is needed.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 3437 (gain this round: +14.9%).
Feasible designs: 187 of 240 evaluations (146 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 22% violate; best seen 8.35e-05 (2^-13.55)

Pareto front (feasible, 12 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round k=2] luts_plus_ffs=336, accuracy_bits=10.2, luts=246, ffs=90, throughput_msps=10.5, max_abs_err=0.000879 (2^-10.15), power_index=0.126
- unrolled_k [data_width=15 n_iter=13 angle_guard=1 frac_guard=0 rounding=round k=2] luts_plus_ffs=340, accuracy_bits=10.5, luts=249, ffs=91, throughput_msps=10.5, max_abs_err=0.000673 (2^-10.54), power_index=0.128
- unrolled_k [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=346, accuracy_bits=10.7, luts=253, ffs=93, throughput_msps=10.5, max_abs_err=0.000594 (2^-10.72), power_index=0.13
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=368, accuracy_bits=11.5, luts=270, ffs=98, throughput_msps=10.5, max_abs_err=0.000344 (2^-11.50), power_index=0.138
- unrolled_k [data_width=17 n_iter=14 angle_guard=0 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=370, accuracy_bits=11.5, luts=270, ffs=100, throughput_msps=10.5, max_abs_err=0.000338 (2^-11.53), power_index=0.139
- unrolled_k [data_width=17 n_iter=15 angle_guard=-1 frac_guard=0 rounding=round k=2] luts_plus_ffs=374, accuracy_bits=11.5, luts=275, ffs=99, throughput_msps=9.58, max_abs_err=0.000334 (2^-11.55), power_index=0.155
- unrolled_k [data_width=17 n_iter=14 angle_guard=0 frac_guard=0 rounding=round k=2] luts_plus_ffs=379, accuracy_bits=11.7, luts=279, ffs=100, throughput_msps=10.5, max_abs_err=0.000301 (2^-11.70), power_index=0.142
- unrolled_k [data_width=17 n_iter=16 angle_guard=1 frac_guard=1 rounding=round k=2] luts_plus_ffs=434, accuracy_bits=12.9, luts=331, ffs=103, throughput_msps=9.58, max_abs_err=0.000128 (2^-12.94), power_index=0.179
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=0.0472
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1276, accuracy_bits=13.5, luts=985, ffs=291, throughput_msps=93.6, max_abs_err=8.35e-05 (2^-13.55), power_index=0.048
Front coverage: luts_plus_ffs 336..1276 (HV reference 1500); accuracy_bits 10.2..13.5 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- unrolled_k: 80 evals, 62 feasible; max throughput seen 13.5 MSPS; best accuracy 12.94 bits; best feasible luts_plus_ffs=336; feasible ranges: data_width 14..18, n_iter 12..16, angle_guard -1..2, frac_guard 0..2, k 2..4
- pipelined: 68 evals, 51 feasible; max throughput seen 282 MSPS; best accuracy 13.35 bits; best feasible luts_plus_ffs=1293; feasible ranges: data_width 14..18, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 92 evals, 74 feasible; max throughput seen 178 MSPS; best accuracy 13.55 bits; best feasible luts_plus_ffs=799; feasible ranges: data_width 15..18, n_iter 12..16, angle_guard 0..2, frac_guard 0..1, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `unrolled_k` (134 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (10 front designs; box front_anchored)
- `pipelined_m` (26 evals): data_width=17..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (2 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 336 feasible; hypervolume 1.245e+04 (+262.1%).

**No LLM call** (code's front-mapping round): The Pareto front is well-mapped and satisfies all constraints. The minimum area design (unrolled_k, luts_plus_ffs=336) meets the throughput constraint (10.5 MSPS >= 1 MSPS) and the accuracy constraint (max_abs_err=0.000879 <= 0.000976562). The front spans a wide range of accuracy (10.2 to 13.5 bits) and area (336 to 1276), providing a good trade-off curve for the hypervolume objective. Since this is the final round and the selection rule (min luts_plus_ffs) is clearly satisfied by the existing front, no further exploration is needed.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.245e+04 (gain this round: +262.1%).
Feasible designs: 336 of 400 evaluations (283 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 16% violate; best seen 4.32e-08 (2^-24.46)

Pareto front (feasible, 22 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round k=2] luts_plus_ffs=336, accuracy_bits=10.2, luts=246, ffs=90, throughput_msps=10.5, max_abs_err=0.000879 (2^-10.15), power_index=0.126
- unrolled_k [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=346, accuracy_bits=10.7, luts=253, ffs=93, throughput_msps=10.5, max_abs_err=0.000594 (2^-10.72), power_index=0.13
- unrolled_k [data_width=17 n_iter=14 angle_guard=0 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=370, accuracy_bits=11.5, luts=270, ffs=100, throughput_msps=10.5, max_abs_err=0.000338 (2^-11.53), power_index=0.139
- unrolled_k [data_width=17 n_iter=14 angle_guard=0 frac_guard=0 rounding=round k=2] luts_plus_ffs=379, accuracy_bits=11.7, luts=279, ffs=100, throughput_msps=10.5, max_abs_err=0.000301 (2^-11.70), power_index=0.142
- unrolled_k [data_width=18 n_iter=22 angle_guard=3 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=420, accuracy_bits=12.3, luts=311, ffs=109, throughput_msps=7.35, max_abs_err=0.0002 (2^-12.28), power_index=0.221
- unrolled_k [data_width=19 n_iter=21 angle_guard=2 frac_guard=0 rounding=round k=2] luts_plus_ffs=453, accuracy_bits=14.7, luts=340, ffs=113, throughput_msps=7.35, max_abs_err=3.86e-05 (2^-14.66), power_index=0.238
- unrolled_k [data_width=20 n_iter=28 angle_guard=0 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=495, accuracy_bits=14.7, luts=374, ffs=120, throughput_msps=6.05, max_abs_err=3.85e-05 (2^-14.67), power_index=0.316
- unrolled_k [data_width=19 n_iter=27 angle_guard=1 frac_guard=2 rounding=round k=2] luts_plus_ffs=528, accuracy_bits=15, luts=412, ffs=116, throughput_msps=6.05, max_abs_err=3.12e-05 (2^-14.97), power_index=0.338
- unrolled_k [data_width=28 n_iter=28 angle_guard=1 frac_guard=0 rounding=round k=2] luts_plus_ffs=695, accuracy_bits=22.9, luts=538, ffs=157, throughput_msps=5.77, max_abs_err=1.32e-07 (2^-22.85), power_index=0.445
- pipelined_m [data_width=27 n_iter=29 angle_guard=4 frac_guard=3 rounding=round m=8] luts_plus_ffs=3370, accuracy_bits=24.5, luts=2924, ffs=446, throughput_msps=44, max_abs_err=4.32e-08 (2^-24.46), power_index=0.127
Front coverage: luts_plus_ffs 336..3370 (HV reference 1500); accuracy_bits 10.2..24.5 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- unrolled_k: 214 evals, 185 feasible; max throughput seen 13.5 MSPS; best accuracy 23.37 bits; best feasible luts_plus_ffs=336; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4, k 2..8
- pipelined: 68 evals, 51 feasible; max throughput seen 282 MSPS; best accuracy 13.35 bits; best feasible luts_plus_ffs=1293; feasible ranges: data_width 14..18, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 118 evals, 100 feasible; max throughput seen 178 MSPS; best accuracy 24.46 bits; best feasible luts_plus_ffs=799; feasible ranges: data_width 15..27, n_iter 12..29, angle_guard 0..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 10936 in, 4605 out
- provider-reported cost: $0.0090
- full prompts and replies: `llm_trace.jsonl`

