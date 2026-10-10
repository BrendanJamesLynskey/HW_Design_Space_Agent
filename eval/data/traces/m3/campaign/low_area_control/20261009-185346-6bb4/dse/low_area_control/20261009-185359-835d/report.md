# DSE run: low_area_control

**Verdict:** converged: hypervolume gain fell below epsilon.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 3 round(s).  
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
`iterative:data_width=14,n_iter=15,angle_guard=3,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 172 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 93 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 11 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 90.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.179 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000648 (2^-10.59) | exact: bit-accurate model, exhaustive (16384 angles) |
| max_abs_err_lsb | 2.65 | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err | 0.00017 (2^-12.52) | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err_lsb | 0.697 | exact: bit-accurate model, exhaustive (16384 angles) |
| accuracy_bits | 10.6 | exact: bit-accurate model, exhaustive (16384 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 18 cycles, a new input every 18 cycle(s). DDS tone from its exact outputs: SFDR 77.8 dBc, SNR 72.4 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (37 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=14,n_iter=15,angle_guard=3,frac_guard=2,rounding=trunc` | 172 | 93 | 11.0 | 18 | 0.179 | 0.000648 (2^-10.59) | 10.59 |
| 1 | `iterative:data_width=16,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc` | 174 | 98 | 10.4 | 19 | 0.194 | 0.000643 (2^-10.60) | 10.60 |
| 2 | `iterative:data_width=14,n_iter=15,angle_guard=2,frac_guard=3,rounding=trunc` | 180 | 94 | 11.0 | 18 | 0.185 | 0.000513 (2^-10.93) | 10.93 |
| 3 | `iterative:data_width=16,n_iter=15,angle_guard=4,frac_guard=1,rounding=trunc` | 187 | 102 | 10.8 | 18 | 0.196 | 0.000313 (2^-11.64) | 11.64 |
| 4 | `iterative:data_width=17,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 189 | 101 | 10.4 | 19 | 0.207 | 0.000244 (2^-12.00) | 12.00 |
| 5 | `iterative:data_width=18,n_iter=15,angle_guard=-1,frac_guard=0,rounding=trunc` | 191 | 105 | 11.0 | 18 | 0.2 | 0.000211 (2^-12.21) | 12.21 |
| 6 | `iterative:data_width=17,n_iter=15,angle_guard=4,frac_guard=1,rounding=trunc` | 198 | 107 | 10.8 | 18 | 0.207 | 0.000202 (2^-12.27) | 12.27 |
| 7 | `iterative:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc` | 204 | 109 | 10.8 | 18 | 0.212 | 0.000127 (2^-12.95) | 12.95 |
| 8 | `iterative:data_width=17,n_iter=16,angle_guard=3,frac_guard=3,rounding=trunc` | 216 | 110 | 10.2 | 19 | 0.233 | 8.14e-05 (2^-13.58) | 13.58 |
| 9 | `iterative:data_width=19,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 225 | 116 | 10.2 | 19 | 0.244 | 5.43e-05 (2^-14.17) | 14.17 |
| 10 | `iterative:data_width=20,n_iter=21,angle_guard=2,frac_guard=0,rounding=trunc` | 251 | 119 | 6.6 | 24 | 0.334 | 4.27e-05 (2^-14.52) | 14.52 |
| 11 | `iterative:data_width=19,n_iter=24,angle_guard=1,frac_guard=2,rounding=trunc` | 263 | 117 | 5.9 | 27 | 0.386 | 4.05e-05 (2^-14.59) | 14.59 |
| 12 | `iterative:data_width=23,n_iter=16,angle_guard=1,frac_guard=0,rounding=trunc` | 252 | 132 | 10.0 | 19 | 0.275 | 3.34e-05 (2^-14.87) | 14.87 |
| 13 | `iterative:data_width=19,n_iter=24,angle_guard=3,frac_guard=2,rounding=trunc` | 266 | 119 | 5.9 | 27 | 0.391 | 2.95e-05 (2^-15.05) | 15.05 |
| 14 | `iterative:data_width=20,n_iter=20,angle_guard=3,frac_guard=1,rounding=trunc` | 264 | 122 | 6.8 | 23 | 0.334 | 2.4e-05 (2^-15.35) | 15.35 |
| 15 | `iterative:data_width=20,n_iter=20,angle_guard=3,frac_guard=2,rounding=trunc` | 278 | 124 | 6.8 | 23 | 0.348 | 1.42e-05 (2^-16.10) | 16.10 |
| 16 | `iterative:data_width=23,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc` | 300 | 132 | 6.2 | 25 | 0.406 | 6.55e-06 (2^-17.22) | 17.22 |
| 17 | `iterative:data_width=23,n_iter=23,angle_guard=1,frac_guard=0,rounding=trunc` | 301 | 133 | 6.0 | 26 | 0.425 | 5.86e-06 (2^-17.38) | 17.38 |
| 18 | `iterative:data_width=23,n_iter=22,angle_guard=0,frac_guard=0,rounding=round` | 313 | 132 | 6.2 | 25 | 0.419 | 3.98e-06 (2^-17.94) | 17.94 |
| 19 | `iterative:data_width=24,n_iter=20,angle_guard=1,frac_guard=0,rounding=trunc` | 310 | 138 | 6.8 | 23 | 0.388 | 3.91e-06 (2^-17.96) | 17.96 |
| 20 | `iterative:data_width=22,n_iter=21,angle_guard=3,frac_guard=2,rounding=trunc` | 319 | 134 | 6.5 | 24 | 0.409 | 3.67e-06 (2^-18.05) | 18.05 |
| 21 | `iterative:data_width=24,n_iter=20,angle_guard=1,frac_guard=0,rounding=round` | 322 | 138 | 6.8 | 23 | 0.398 | 3.1e-06 (2^-18.30) | 18.30 |
| 22 | `iterative:data_width=23,n_iter=24,angle_guard=1,frac_guard=2,rounding=trunc` | 333 | 137 | 5.8 | 27 | 0.477 | 2.68e-06 (2^-18.51) | 18.51 |
| 23 | `iterative:data_width=23,n_iter=22,angle_guard=3,frac_guard=2,rounding=trunc` | 336 | 139 | 6.2 | 25 | 0.447 | 1.83e-06 (2^-19.06) | 19.06 |
| 24 | `iterative:data_width=26,n_iter=24,angle_guard=1,frac_guard=0,rounding=trunc` | 354 | 148 | 5.7 | 27 | 0.51 | 8.42e-07 (2^-20.18) | 20.18 |
| 25 | `iterative:data_width=25,n_iter=28,angle_guard=4,frac_guard=0,rounding=round` | 361 | 146 | 4.9 | 31 | 0.592 | 7.53e-07 (2^-20.34) | 20.34 |
| 26 | `iterative:data_width=26,n_iter=23,angle_guard=0,frac_guard=0,rounding=round` | 366 | 147 | 6.0 | 26 | 0.502 | 7.26e-07 (2^-20.39) | 20.39 |
| 27 | `iterative:data_width=25,n_iter=23,angle_guard=3,frac_guard=2,rounding=trunc` | 371 | 149 | 5.9 | 26 | 0.509 | 5.8e-07 (2^-20.72) | 20.72 |
| 28 | `iterative:data_width=26,n_iter=28,angle_guard=1,frac_guard=0,rounding=round` | 375 | 148 | 4.9 | 31 | 0.61 | 3.95e-07 (2^-21.27) | 21.27 |
| 29 | `iterative:data_width=27,n_iter=24,angle_guard=1,frac_guard=1,rounding=trunc` | 387 | 155 | 5.7 | 27 | 0.551 | 3.19e-07 (2^-21.58) | 21.58 |
| 30 | `iterative:data_width=27,n_iter=27,angle_guard=1,frac_guard=0,rounding=round` | 394 | 153 | 5.1 | 30 | 0.618 | 2.33e-07 (2^-22.03) | 22.03 |
| 31 | `iterative:data_width=27,n_iter=24,angle_guard=1,frac_guard=4,rounding=trunc` | 434 | 161 | 5.6 | 27 | 0.605 | 2.25e-07 (2^-22.08) | 22.08 |
| 32 | `iterative:data_width=27,n_iter=27,angle_guard=1,frac_guard=1,rounding=round` | 468 | 155 | 5.1 | 30 | 0.703 | 1.88e-07 (2^-22.34) | 22.34 |
| 33 | `iterative:data_width=27,n_iter=28,angle_guard=4,frac_guard=1,rounding=round` | 473 | 158 | 4.9 | 31 | 0.737 | 1.18e-07 (2^-23.02) | 23.02 |
| 34 | `unrolled_k:data_width=28,n_iter=26,angle_guard=1,frac_guard=3,rounding=trunc,k=2` | 581 | 163 | 6.0 | 16 | 0.448 | 9.77e-08 (2^-23.29) | 23.29 |
| 35 | `unrolled_k:data_width=28,n_iter=26,angle_guard=1,frac_guard=4,rounding=trunc,k=2` | 600 | 165 | 6.0 | 16 | 0.461 | 9.68e-08 (2^-23.30) | 23.30 |
| 36 | `unrolled_k:data_width=28,n_iter=26,angle_guard=3,frac_guard=4,rounding=trunc,k=3` | 772 | 167 | 5.4 | 12 | 0.424 | 5.72e-08 (2^-24.06) | 24.06 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-critical (minimize luts_plus_ffs) with a throughput floor of >= 1 MSPS and accuracy <= 2^-10. Iterative is the most compact family and the primary candidate for the minimum-area corner. Unrolled_k with k=2 provides throughput headroom that may allow smaller data_width/n_iter, potentially improving the area/accuracy trade-off. Pipelined_m with large m is included as a secondary check since it achieves 1 result/cycle with fewer registers than fully pipelined, and may compete on area. We exclude fully pipelined (too many registers for area-critical spec) and unrolled_k with k>2 (too much area duplication). The budget is weighted toward iterative (45%) as the most likely winner, with unrolled_k (35%) for trade-off mapping, and pipelined_m (20%) for verification. All families search data_width 12-28 and n_iter 12-30 to cover the accuracy range needed for 2^-10 error, with guard bits explored to find minimal overhead.*)
- `iterative` (45 evals): data_width=12..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Single shared datapath with barrel shifters is the most area-efficient family. It is the primary candidate for minimizing luts_plus_ffs while meeting the 2^-10 accuracy constraint. We search a wide range of data_width and n_iter to map the accuracy/area trade-off, and include angle_guard/frac_guard to find the minimal guard bits needed to satisfy max_abs_err <= 2^-10.
- `unrolled_k` (35 evals): data_width=12..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..2. *Why:* k=2 unrolled design doubles throughput per cycle compared to iterative, which helps meet the >= 1 MSPS constraint at lower Fmax or with more margin. It adds some area (dual datapath elements) but may allow a lower data_width or n_iter to meet accuracy, potentially yielding a better luts_plus_ffs trade-off than iterative at the same accuracy. We fix k=2 to keep area low while gaining throughput headroom.
- `pipelined_m` (20 evals): data_width=12..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=4..8. *Why:* pipelined_m with large m (4-8) registers fewer stages than fully pipelined, reducing FF count significantly. It still achieves 1 result/cycle throughput, easily meeting >= 1 MSPS. This family may offer a competitive luts_plus_ffs if the reduced register count offsets the pipeline logic. We include it to check if it can beat iterative/unrolled_k on the area objective while maintaining throughput.

**Result (code):** 100 evaluations this round, 100 total; 92 feasible; hypervolume 1.337e+04 (n/a).

**LLM decision:** `add_family` — The current front is dominated by iterative and unrolled_k designs, with pipelined_m only appearing at high area (>=1098). The pipelined family is unexplored and is the only one that can potentially offer a 1-result/cycle throughput at high Fmax with a different area/accuracy trade-off than pipelined_m. Adding it is the highest-value next step to expand the front. Simultaneously, refining the iterative family around its low-area corner (data_width 14..18, n_iter 12..25) should help fill in the mid-accuracy region of the front, improving hypervolume coverage between 10 and 15 accuracy bits at low area. This two-pronged approach uses the 100-eval budget to both explore a new family and refine the existing best family.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 1.337e+04 (gain this round: n/a (first round)).
Feasible designs: 92 of 100 evaluations (86 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 97.8
- max_abs_err <= 0.000976562: 8% violate; best seen 1.42e-07 (2^-22.74)

Pareto front (feasible, 16 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=20 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=288, accuracy_bits=10.1, luts=192, ffs=96, throughput_msps=7.04, max_abs_err=0.000913 (2^-10.10), power_index=0.249
- iterative [data_width=17 n_iter=16 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=326, accuracy_bits=13.6, luts=216, ffs=110, throughput_msps=10.2, max_abs_err=8.14e-05 (2^-13.58), power_index=0.233
- iterative [data_width=17 n_iter=23 angle_guard=3 frac_guard=4 rounding=trunc] luts_plus_ffs=376, accuracy_bits=14, luts=263, ffs=113, throughput_msps=6.11, max_abs_err=6.21e-05 (2^-13.97), power_index=0.367
- iterative [data_width=20 n_iter=20 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=386, accuracy_bits=15.3, luts=264, ffs=122, throughput_msps=6.78, max_abs_err=2.4e-05 (2^-15.35), power_index=0.334
- iterative [data_width=21 n_iter=24 angle_guard=1 frac_guard=3 rounding=trunc] luts_plus_ffs=443, accuracy_bits=16.7, luts=313, ffs=129, throughput_msps=5.78, max_abs_err=9.21e-06 (2^-16.73), power_index=0.449
- iterative [data_width=23 n_iter=29 angle_guard=0 frac_guard=3 rounding=trunc] luts_plus_ffs=491, accuracy_bits=17.9, luts=353, ffs=138, throughput_msps=4.88, max_abs_err=4.01e-06 (2^-17.93), power_index=0.591
- iterative [data_width=26 n_iter=20 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=531, accuracy_bits=18.9, luts=375, ffs=155, throughput_msps=6.66, max_abs_err=2.03e-06 (2^-18.91), power_index=0.459
- iterative [data_width=26 n_iter=23 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=561, accuracy_bits=21.4, luts=404, ffs=156, throughput_msps=5.89, max_abs_err=3.59e-07 (2^-21.41), power_index=0.548
- unrolled_k [data_width=27 n_iter=25 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=665, accuracy_bits=21.9, luts=510, ffs=154, throughput_msps=6.13, max_abs_err=2.6e-07 (2^-21.88), power_index=0.4
- unrolled_k [data_width=27 n_iter=26 angle_guard=2 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=700, accuracy_bits=22.7, luts=542, ffs=157, throughput_msps=6.13, max_abs_err=1.42e-07 (2^-22.74), power_index=0.421
Front coverage: luts_plus_ffs 288..700 (HV reference 1500); accuracy_bits 10.1..22.7 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 45 evals, 43 feasible; max throughput seen 12.4 MSPS; best accuracy 21.41 bits; best feasible luts_plus_ffs=288; feasible ranges: data_width 15..26, n_iter 13..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 35 evals, 32 feasible; max throughput seen 10.9 MSPS; best accuracy 22.74 bits; best feasible luts_plus_ffs=414; feasible ranges: data_width 17..28, n_iter 12..29, angle_guard -2..4, frac_guard 0..4, k 2..2
- pipelined_m: 20 evals, 17 feasible; max throughput seen 97.8 MSPS; best accuracy 18.07 bits; best feasible luts_plus_ffs=1098; feasible ranges: data_width 18..26, n_iter 14..26, angle_guard 0..4, frac_guard 0..4, m 4..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The current front is dominated by iterative and unrolled_k designs, with pipelined_m only appearing at high area (>=1098). The pipelined family is unexplored and is the only one that can potentially offer a 1-result/cycle throughput at high Fmax with a different area/accuracy trade-off than pipelined_m. Adding it is the highest-value next step to expand the front. Simultaneously, refining the iterative family around its low-area corner (data_width 14..18, n_iter 12..25) should help fill in the mid-accuracy region of the front, improving hypervolume coverage between 10 and 15 accuracy bits at low area. This two-pronged approach uses the 100-eval budget to both explore a new family and refine the existing best family.*)
- `pipelined` (50 evals): data_width=14..22, n_iter=10..30, angle_guard=0..4, frac_guard=0..4, rounding=trunc|round. *Why:* pipelined is the only family not yet explored and it is the only one that can hit the >=1 MSPS throughput constraint with a full 1 result/cycle schedule at high Fmax. pipelined_m already shows 97.8 MSPS but its best area is 1098 LUT+FF, far above the iterative/unrolled_k front (288..700). A fully pipelined design with a small m-equivalent (every stage registered) may trade a bit more area for a much higher Fmax, potentially opening a new low-area, high-throughput corner of the front that the current families cannot reach. I restrict data_width to 14..22 and n_iter to 10..30 to focus on the region where accuracy_bits >= 10 (the constraint) is achievable without blowing up area, and keep angle/frac guards in the 0..4 range that has proven feasible in the other families.
- `iterative` (50 evals): data_width=14..18, n_iter=12..25, angle_guard=0..4, frac_guard=0..4, rounding=trunc|round. *Why:* The current front's low-area corner is dominated by iterative designs (288..561 LUT+FF). The best feasible iterative design has luts_plus_ffs=288 with accuracy_bits=10.1, which barely meets the 2^-10 constraint. I want to refine the iterative family around this low-area region to see if we can push accuracy_bits higher (toward 12-15) while keeping area under 400, which would improve the hypervolume in the mid-accuracy region. I narrow data_width to 14..18 and n_iter to 12..25 to focus on the sweet spot where area is minimal but accuracy is still above the constraint.

**Result (code):** 100 evaluations this round, 200 total; 184 feasible; hypervolume 1.34e+04 (+0.3%).

**LLM decision:** `refine` — The current Pareto front is dominated by the `iterative` family (8 of the top 10 designs), which achieves the lowest area (265 LUTs+FFs) while meeting the throughput constraint (11 MSPS >= 1 MSPS). The `pipelined` and `pipelined_m` families are significantly more expensive (1586 and 1098 LUTs+FFs respectively) and do not appear on the efficient part of the front for this low-throughput spec. The `unrolled_k` family is also less efficient than `iterative` for the low-end of the front. Since the goal is to minimize area and the `iterative` family clearly dominates the feasible region of interest, we should narrow the search to focus exclusively on `iterative` and refine its parameters to better map the trade-off between area and accuracy within the feasible bounds. Specifically, we will restrict `data_width` to 14-18, `n_iter` to 14-20, and keep guards/rounding flexible to capture the optimal balance.
- **rule applied by code:** 'refine' overridden to stop: HV gain 0.25% < epsilon 1.00%
- **rule applied by code:** code: before stopping (converged), one front-mapping round with the remaining 200 evaluations
- effective decision: `stop`

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.34e+04 (gain this round: +0.3%).
Feasible designs: 184 of 200 evaluations (170 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 8% violate; best seen 1.42e-07 (2^-22.74)

Pareto front (feasible, 21 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=15 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=265, accuracy_bits=10.6, luts=172, ffs=93, throughput_msps=11, max_abs_err=0.000648 (2^-10.59), power_index=0.179
- iterative [data_width=16 n_iter=15 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=289, accuracy_bits=11.6, luts=187, ffs=102, throughput_msps=10.8, max_abs_err=0.000313 (2^-11.64), power_index=0.196
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=297, accuracy_bits=12.2, luts=193, ffs=104, throughput_msps=11, max_abs_err=0.000219 (2^-12.16), power_index=0.201
- iterative [data_width=17 n_iter=16 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=326, accuracy_bits=13.6, luts=216, ffs=110, throughput_msps=10.2, max_abs_err=8.14e-05 (2^-13.58), power_index=0.233
- iterative [data_width=17 n_iter=23 angle_guard=4 frac_guard=4 rounding=trunc] luts_plus_ffs=379, accuracy_bits=14.3, luts=265, ffs=114, throughput_msps=6.11, max_abs_err=4.92e-05 (2^-14.31), power_index=0.37
- iterative [data_width=20 n_iter=20 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=402, accuracy_bits=16.1, luts=278, ffs=124, throughput_msps=6.78, max_abs_err=1.42e-05 (2^-16.10), power_index=0.348
- iterative [data_width=23 n_iter=29 angle_guard=0 frac_guard=3 rounding=trunc] luts_plus_ffs=491, accuracy_bits=17.9, luts=353, ffs=138, throughput_msps=4.88, max_abs_err=4.01e-06 (2^-17.93), power_index=0.591
- iterative [data_width=26 n_iter=23 angle_guard=0 frac_guard=3 rounding=trunc] luts_plus_ffs=552, accuracy_bits=20.5, luts=399, ffs=153, throughput_msps=5.89, max_abs_err=6.95e-07 (2^-20.46), power_index=0.54
- unrolled_k [data_width=27 n_iter=25 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=665, accuracy_bits=21.9, luts=510, ffs=154, throughput_msps=6.13, max_abs_err=2.6e-07 (2^-21.88), power_index=0.4
- unrolled_k [data_width=27 n_iter=26 angle_guard=2 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=700, accuracy_bits=22.7, luts=542, ffs=157, throughput_msps=6.13, max_abs_err=1.42e-07 (2^-22.74), power_index=0.421
Front coverage: luts_plus_ffs 265..700 (HV reference 1500); accuracy_bits 10.6..22.7 (HV reference 10); data_width on the front 14..27 (registry 8..28).

Per family:
- iterative: 95 evals, 88 feasible; max throughput seen 12.4 MSPS; best accuracy 21.41 bits; best feasible luts_plus_ffs=265; feasible ranges: data_width 14..26, n_iter 13..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 35 evals, 32 feasible; max throughput seen 10.9 MSPS; best accuracy 22.74 bits; best feasible luts_plus_ffs=414; feasible ranges: data_width 17..28, n_iter 12..29, angle_guard -2..4, frac_guard 0..4, k 2..2
- pipelined: 50 evals, 47 feasible; max throughput seen 282 MSPS; best accuracy 19.76 bits; best feasible luts_plus_ffs=1586; feasible ranges: data_width 15..22, n_iter 13..30, angle_guard 0..4, frac_guard 0..4
- pipelined_m: 20 evals, 17 feasible; max throughput seen 97.8 MSPS; best accuracy 18.07 bits; best feasible luts_plus_ffs=1098; feasible ranges: data_width 18..26, n_iter 14..26, angle_guard 0..4, frac_guard 0..4, m 4..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 200 evaluations*)
- `iterative` (172 evals): data_width=13..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (18 front designs; box front_anchored)
- `unrolled_k` (28 evals): data_width=26..28, n_iter=23..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (3 front designs; box front_anchored)

**Result (code):** 200 evaluations this round, 400 total; 369 feasible; hypervolume 1.467e+04 (+9.4%).

**No LLM call** (code's front-mapping round): The current Pareto front is dominated by the `iterative` family (8 of the top 10 designs), which achieves the lowest area (265 LUTs+FFs) while meeting the throughput constraint (11 MSPS >= 1 MSPS). The `pipelined` and `pipelined_m` families are significantly more expensive (1586 and 1098 LUTs+FFs respectively) and do not appear on the efficient part of the front for this low-throughput spec. The `unrolled_k` family is also less efficient than `iterative` for the low-end of the front. Since the goal is to minimize area and the `iterative` family clearly dominates the feasible region of interest, we should narrow the search to focus exclusively on `iterative` and refine its parameters to better map the trade-off between area and accuracy within the feasible bounds. Specifically, we will restrict `data_width` to 14-18, `n_iter` to 14-20, and keep guards/rounding flexible to capture the optimal balance.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.467e+04 (gain this round: +9.4%).
Feasible designs: 369 of 400 evaluations (329 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 8% violate; best seen 5.72e-08 (2^-24.06)

Pareto front (feasible, 37 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=15 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=265, accuracy_bits=10.6, luts=172, ffs=93, throughput_msps=11, max_abs_err=0.000648 (2^-10.59), power_index=0.179
- iterative [data_width=17 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=290, accuracy_bits=12, luts=189, ffs=101, throughput_msps=10.4, max_abs_err=0.000244 (2^-12.00), power_index=0.207
- iterative [data_width=17 n_iter=16 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=326, accuracy_bits=13.6, luts=216, ffs=110, throughput_msps=10.2, max_abs_err=8.14e-05 (2^-13.58), power_index=0.233
- iterative [data_width=23 n_iter=16 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=384, accuracy_bits=14.9, luts=252, ffs=132, throughput_msps=9.97, max_abs_err=3.34e-05 (2^-14.87), power_index=0.275
- iterative [data_width=23 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=432, accuracy_bits=17.2, luts=300, ffs=132, throughput_msps=6.24, max_abs_err=6.55e-06 (2^-17.22), power_index=0.406
- iterative [data_width=22 n_iter=21 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=453, accuracy_bits=18.1, luts=319, ffs=134, throughput_msps=6.5, max_abs_err=3.67e-06 (2^-18.05), power_index=0.409
- iterative [data_width=26 n_iter=24 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=502, accuracy_bits=20.2, luts=354, ffs=148, throughput_msps=5.68, max_abs_err=8.42e-07 (2^-20.18), power_index=0.51
- iterative [data_width=26 n_iter=28 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=523, accuracy_bits=21.3, luts=375, ffs=148, throughput_msps=4.94, max_abs_err=3.95e-07 (2^-21.27), power_index=0.61
- iterative [data_width=27 n_iter=27 angle_guard=1 frac_guard=1 rounding=round] luts_plus_ffs=623, accuracy_bits=22.3, luts=468, ffs=155, throughput_msps=5.11, max_abs_err=1.88e-07 (2^-22.34), power_index=0.703
- unrolled_k [data_width=28 n_iter=26 angle_guard=3 frac_guard=4 rounding=trunc k=3] luts_plus_ffs=940, accuracy_bits=24.1, luts=772, ffs=167, throughput_msps=5.43, max_abs_err=5.72e-08 (2^-24.06), power_index=0.424
Front coverage: luts_plus_ffs 265..940 (HV reference 1500); accuracy_bits 10.6..24.1 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 267 evals, 245 feasible; max throughput seen 12.4 MSPS; best accuracy 23.02 bits; best feasible luts_plus_ffs=265; feasible ranges: data_width 13..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 63 evals, 60 feasible; max throughput seen 10.9 MSPS; best accuracy 24.06 bits; best feasible luts_plus_ffs=414; feasible ranges: data_width 17..28, n_iter 12..29, angle_guard -2..4, frac_guard 0..4, k 2..8
- pipelined: 50 evals, 47 feasible; max throughput seen 282 MSPS; best accuracy 19.76 bits; best feasible luts_plus_ffs=1586; feasible ranges: data_width 15..22, n_iter 13..30, angle_guard 0..4, frac_guard 0..4
- pipelined_m: 20 evals, 17 feasible; max throughput seen 97.8 MSPS; best accuracy 18.07 bits; best feasible luts_plus_ffs=1098; feasible ranges: data_width 18..26, n_iter 14..26, angle_guard 0..4, frac_guard 0..4, m 4..8
```
</details>

## LLM usage
- calls: 6 (failed/unparsed attempts: 0)
- tokens: 21495 in, 3451 out
- provider-reported cost: $0.0060
- full prompts and replies: `llm_trace.jsonl`

