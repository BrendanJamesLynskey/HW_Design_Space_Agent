# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec multiaxis_control: Shared sin/cos unit for a 16-axis motor-control loop: a 1 MHz control tick issues 32 requests at once (Park + inverse Park per axis); all 32 results must be back within 0.44 us of the tick (p99 over ticks). Max error <= 2^-12. Minimise LUTs + FFs.
  constraint: throughput_msps >= 32
  constraint: max_abs_err <= 0.000244141
  constraint: sys_p99_batch_us <= 0.44
  objective: min luts_plus_ffs (HV ref 4000)
  objective: max accuracy_bits (HV ref 12)
  select: min luts_plus_ffs
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average)
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 827 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 282 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 61.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.34 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.0002 (2^-12.28) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 13.1 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.41e-05 (2^-14.17) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.55 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (21 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=4` | 827 | 282 | 97.8 | 6 | 1.34 | 0.0002 (2^-12.28) | 12.28 |
| 1 | `pipelined_m:data_width=17,n_iter=16,angle_guard=3,frac_guard=0,rounding=round,m=4` | 954 | 280 | 93.6 | 6 | 1.49 | 0.000146 (2^-12.74) | 12.74 |
| 2 | `pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 985 | 289 | 93.6 | 6 | 1.53 | 0.000136 (2^-12.84) | 12.84 |
| 3 | `pipelined_m:data_width=17,n_iter=16,angle_guard=3,frac_guard=3,rounding=round,m=4` | 1084 | 301 | 93.6 | 6 | 1.67 | 6.42e-05 (2^-13.93) | 13.93 |
| 4 | `pipelined_m:data_width=17,n_iter=16,angle_guard=3,frac_guard=4,rounding=round,m=3` | 1116 | 446 | 119.3 | 8 | 1.88 | 5.86e-05 (2^-14.06) | 14.06 |
| 5 | `pipelined_m:data_width=22,n_iter=16,angle_guard=3,frac_guard=4,rounding=trunc,m=4` | 1317 | 375 | 89.6 | 6 | 2.04 | 3.14e-05 (2^-14.96) | 14.96 |
| 6 | `pipelined_m:data_width=24,n_iter=18,angle_guard=-1,frac_guard=0,rounding=round,m=4` | 1385 | 442 | 89.6 | 7 | 2.2 | 9.47e-06 (2^-16.69) | 16.69 |
| 7 | `pipelined_m:data_width=24,n_iter=18,angle_guard=3,frac_guard=0,rounding=round,m=4` | 1456 | 462 | 86.0 | 7 | 2.31 | 8.29e-06 (2^-16.88) | 16.88 |
| 8 | `pipelined_m:data_width=24,n_iter=19,angle_guard=3,frac_guard=0,rounding=round,m=4` | 1542 | 462 | 86.0 | 7 | 2.41 | 4.5e-06 (2^-17.76) | 17.76 |
| 9 | `pipelined_m:data_width=25,n_iter=19,angle_guard=3,frac_guard=0,rounding=round,m=4` | 1599 | 479 | 86.0 | 7 | 2.5 | 4.33e-06 (2^-17.82) | 17.82 |
| 10 | `pipelined_m:data_width=25,n_iter=19,angle_guard=3,frac_guard=2,rounding=trunc,m=4` | 1674 | 495 | 86.0 | 7 | 2.61 | 4.04e-06 (2^-17.92) | 17.92 |
| 11 | `pipelined_m:data_width=25,n_iter=19,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1727 | 497 | 86.0 | 7 | 2.68 | 3.99e-06 (2^-17.94) | 17.94 |
| 12 | `pipelined_m:data_width=22,n_iter=20,angle_guard=3,frac_guard=4,rounding=trunc,m=3` | 1667 | 630 | 114.5 | 9 | 2.76 | 3.36e-06 (2^-18.18) | 18.18 |
| 13 | `pipelined_m:data_width=22,n_iter=20,angle_guard=4,frac_guard=4,rounding=trunc,m=3` | 1687 | 637 | 114.5 | 9 | 2.8 | 3.17e-06 (2^-18.27) | 18.27 |
| 14 | `pipelined_m:data_width=25,n_iter=23,angle_guard=-1,frac_guard=0,rounding=round,m=4` | 1860 | 541 | 89.6 | 8 | 2.89 | 2e-06 (2^-18.93) | 18.93 |
| 15 | `pipelined_m:data_width=22,n_iter=25,angle_guard=3,frac_guard=3,rounding=round,m=3` | 2100 | 785 | 114.5 | 11 | 3.47 | 1.79e-06 (2^-19.09) | 19.09 |
| 16 | `pipelined_m:data_width=24,n_iter=24,angle_guard=2,frac_guard=1,rounding=round,m=2` | 2043 | 1053 | 158.3 | 14 | 3.73 | 1.08e-06 (2^-19.82) | 19.82 |
| 17 | `pipelined:data_width=27,n_iter=22,angle_guard=-1,frac_guard=0,rounding=trunc` | 1908 | 1931 | 249.0 | 24 | 4.62 | 9.78e-07 (2^-19.96) | 19.96 |
| 18 | `pipelined:data_width=26,n_iter=26,angle_guard=4,frac_guard=0,rounding=round` | 2324 | 2335 | 249.0 | 28 | 5.61 | 3.6e-07 (2^-21.40) | 21.40 |
| 19 | `pipelined:data_width=26,n_iter=26,angle_guard=4,frac_guard=1,rounding=round` | 2431 | 2385 | 249.0 | 28 | 5.8 | 2.42e-07 (2^-21.98) | 21.98 |
| 20 | `pipelined:data_width=27,n_iter=28,angle_guard=3,frac_guard=1,rounding=round` | 2680 | 2625 | 249.0 | 30 | 6.39 | 1.16e-07 (2^-23.04) | 23.04 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show that pipelined_m is the clear winner: 13 of 16 front designs and best area 1240, versus pipelined's 3 designs and best area 1788. The iterative and unrolled_k families have 0 feasible designs, confirming that only the pipelined families can meet the 32 Msps throughput and 0.44us batch latency constraints. I am allocating 50% of the budget to pipelined_m to densely map its Pareto front in the proven-feasible region (data_width 14-18, n_iter 13-16, m 2-4), and 50% to pipelined with the same accuracy ranges to cover the higher-area end of the front. The ranges are narrowed from the full registry to focus the 100-eval budget on the region where feasible designs actually exist, maximizing hypervolume coverage of the trade-off curve between luts_plus_ffs and accuracy_bits.*)
- `pipelined_m` (50 evals): data_width=14..18, n_iter=13..16, angle_guard=-2..0, frac_guard=0..1, rounding=trunc|round, m=2..4. *Why:* pipelined_m dominates the merged front (13/16 designs, best area 1240). It is the only family that can plausibly meet the 32 Msps throughput and 0.44us batch constraint while keeping area low. I am narrowing the ranges to focus on the proven-feasible region: data_width 14-18 (14 is the minimum that can hit 2^-12 error with enough n_iter, 18 gives margin for accuracy_bits objective), n_iter 13-16 (13 is near the minimum for 2^-12 accuracy, 16 gives accuracy_bits headroom), angle_guard -2 to 0 (negative guard saves area, 0 is safe), frac_guard 0-1 (0 is cheapest, 1 adds margin), m 2-4 (smaller m means more registers but shorter latency; 2-4 balances area vs the 0.44us batch constraint). This focuses the budget on the dense Pareto region.
- `pipelined` (50 evals): data_width=14..18, n_iter=13..16, angle_guard=-2..0, frac_guard=0..1, rounding=trunc|round. *Why:* pipelined has 3 designs on the front and best area 1788, so it is less competitive than pipelined_m but still contributes to the Pareto front. I am using the same narrowed accuracy ranges (data_width 14-18, n_iter 13-16, angle_guard -2 to 0, frac_guard 0-1) to explore the full trade-off curve in the feasible region. Since pipelined has no m parameter, it has more registers than pipelined_m for the same N, so it will generally have higher area but potentially higher Fmax. This helps map the area-vs-accuracy trade-off at the higher-area end of the front.

**Result (code):** 100 evaluations this round, 100 total; 17 feasible; hypervolume 2713 (n/a).

**LLM decision:** `refine` — The current front is dominated by `pipelined_m` designs with `data_width=18` and `n_iter` between 14 and 16. The `pipelined` family is significantly more expensive (min 1902 vs 1110 luts_plus_ffs) and does not offer a better accuracy/area trade-off than the best `pipelined_m` candidates. The constraint `max_abs_err <= 0.000244141` (approx 2^-12) is the tightest bottleneck, with 83% of evaluations failing it. To improve the hypervolume and find a cheaper design that still meets the accuracy constraint, we should focus the search on the `pipelined_m` family, which has already proven to be the most efficient. We will narrow the `data_width` to 16-18 (to explore if 16 is feasible and cheaper) and `n_iter` to 12-16 (to find the minimum iterations needed for 12-bit accuracy). We will also keep `angle_guard` and `frac_guard` in their feasible ranges (-1..0 and 0..1) and `m` in 2..4. This refinement will allow Optuna to concentrate its remaining budget on the most promising region of the design space.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 2713 (gain this round: n/a (first round)).
Feasible designs: 17 of 100 evaluations (10 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 83% violate; best seen 0.00012 (2^-13.03)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.165

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1110, accuracy_bits=12.3, luts=827, ffs=282, throughput_msps=97.8, max_abs_err=0.0002 (2^-12.28), power_index=1.34
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=round m=3] luts_plus_ffs=1247, accuracy_bits=12.4, luts=893, ffs=354, throughput_msps=119, max_abs_err=0.000179 (2^-12.45), power_index=1.5
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1274, accuracy_bits=12.8, luts=985, ffs=289, throughput_msps=93.6, max_abs_err=0.000136 (2^-12.84), power_index=1.53
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=round] luts_plus_ffs=2038, accuracy_bits=13, luts=1023, ffs=1015, throughput_msps=264, max_abs_err=0.00012 (2^-13.03), power_index=2.45
Front coverage: luts_plus_ffs 1110..2038 (HV reference 4000); accuracy_bits 12.3..13 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- pipelined: 50 evals, 7 feasible; max throughput seen 282 MSPS; best accuracy 13.03 bits; best feasible luts_plus_ffs=1902; feasible ranges: data_width 17..18, n_iter 16..16, angle_guard 0..0, frac_guard 1..1
- pipelined_m: 50 evals, 10 feasible; max throughput seen 178 MSPS; best accuracy 12.84 bits; best feasible luts_plus_ffs=1110; feasible ranges: data_width 18..18, n_iter 14..16, angle_guard -1..0, frac_guard 0..1, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Refine the search to the pipelined_m family with narrowed ranges around the current Pareto front to maximize hypervolume improvement within the remaining budget.*)
- `pipelined_m` (20 evals): data_width=16..18, n_iter=12..16, angle_guard=-1..0, frac_guard=0..1, rounding=trunc|round, m=2..4. *Why:* Focus on the most efficient family and narrow the ranges around the known feasible region to find cheaper designs that meet the accuracy constraint.

**Result (code):** 20 evaluations this round, 120 total; 24 feasible; hypervolume 2713 (+0.0%).

**LLM decision:** `stop` — The exploration has successfully identified a feasible Pareto front that satisfies all constraints. The minimum area design (pipelined_m, 1110 LUTs+FFs) meets the throughput (97.8 MSPS >= 32), accuracy (12.3 bits >= 12), and system latency (0.165 us <= 0.44 us) requirements. The front covers the trade-off space well, with area ranging from 1110 to 2038 and accuracy from 12.3 to 13.0 bits. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (1110) as per the selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 2713 (gain this round: +0.0%).
Feasible designs: 24 of 120 evaluations (14 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 80% violate; best seen 0.00012 (2^-13.03)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.165

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1110, accuracy_bits=12.3, luts=827, ffs=282, throughput_msps=97.8, max_abs_err=0.0002 (2^-12.28), power_index=1.34
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=round m=3] luts_plus_ffs=1247, accuracy_bits=12.4, luts=893, ffs=354, throughput_msps=119, max_abs_err=0.000179 (2^-12.45), power_index=1.5
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1274, accuracy_bits=12.8, luts=985, ffs=289, throughput_msps=93.6, max_abs_err=0.000136 (2^-12.84), power_index=1.53
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=round] luts_plus_ffs=2038, accuracy_bits=13, luts=1023, ffs=1015, throughput_msps=264, max_abs_err=0.00012 (2^-13.03), power_index=2.45
Front coverage: luts_plus_ffs 1110..2038 (HV reference 4000); accuracy_bits 12.3..13 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- pipelined: 50 evals, 7 feasible; max throughput seen 282 MSPS; best accuracy 13.03 bits; best feasible luts_plus_ffs=1902; feasible ranges: data_width 17..18, n_iter 16..16, angle_guard 0..0, frac_guard 1..1
- pipelined_m: 70 evals, 17 feasible; max throughput seen 178 MSPS; best accuracy 12.84 bits; best feasible luts_plus_ffs=1110; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard -1..0, frac_guard 0..1, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (60 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (3 front designs; box front_anchored)
- `pipelined` (20 evals): data_width=17..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 79 feasible; hypervolume 1.633e+04 (+501.8%).

**No LLM call** (code's front-mapping round): The exploration has successfully identified a feasible Pareto front that satisfies all constraints. The minimum area design (pipelined_m, 1110 LUTs+FFs) meets the throughput (97.8 MSPS >= 32), accuracy (12.3 bits >= 12), and system latency (0.165 us <= 0.44 us) requirements. The front covers the trade-off space well, with area ranging from 1110 to 2038 and accuracy from 12.3 to 13.0 bits. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (1110) as per the selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.633e+04 (gain this round: +501.8%).
Feasible designs: 79 of 200 evaluations (67 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 51% violate; best seen 2.86e-08 (2^-25.06)
- sys_p99_batch_us <= 0.44: 10% violate; best seen 0.165

Pareto front (feasible, 21 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1110, accuracy_bits=12.3, luts=827, ffs=282, throughput_msps=97.8, max_abs_err=0.0002 (2^-12.28), power_index=1.34
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1274, accuracy_bits=12.8, luts=985, ffs=289, throughput_msps=93.6, max_abs_err=0.000136 (2^-12.84), power_index=1.53
- pipelined_m [data_width=17 n_iter=16 angle_guard=3 frac_guard=4 rounding=round m=3] luts_plus_ffs=1562, accuracy_bits=14.1, luts=1116, ffs=446, throughput_msps=119, max_abs_err=5.86e-05 (2^-14.06), power_index=1.88
- pipelined_m [data_width=24 n_iter=18 angle_guard=3 frac_guard=0 rounding=round m=4] luts_plus_ffs=1918, accuracy_bits=16.9, luts=1456, ffs=462, throughput_msps=86, max_abs_err=8.29e-06 (2^-16.88), power_index=2.31
- pipelined_m [data_width=25 n_iter=19 angle_guard=3 frac_guard=0 rounding=round m=4] luts_plus_ffs=2078, accuracy_bits=17.8, luts=1599, ffs=479, throughput_msps=86, max_abs_err=4.33e-06 (2^-17.82), power_index=2.5
- pipelined_m [data_width=25 n_iter=19 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=2224, accuracy_bits=17.9, luts=1727, ffs=497, throughput_msps=86, max_abs_err=3.99e-06 (2^-17.94), power_index=2.68
- pipelined_m [data_width=22 n_iter=20 angle_guard=4 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=2324, accuracy_bits=18.3, luts=1687, ffs=637, throughput_msps=114, max_abs_err=3.17e-06 (2^-18.27), power_index=2.8
- pipelined_m [data_width=24 n_iter=24 angle_guard=2 frac_guard=1 rounding=round m=2] luts_plus_ffs=3097, accuracy_bits=19.8, luts=2043, ffs=1053, throughput_msps=158, max_abs_err=1.08e-06 (2^-19.82), power_index=3.73
- pipelined [data_width=26 n_iter=26 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=4658, accuracy_bits=21.4, luts=2324, ffs=2335, throughput_msps=249, max_abs_err=3.6e-07 (2^-21.40), power_index=5.61
- pipelined [data_width=27 n_iter=28 angle_guard=3 frac_guard=1 rounding=round] luts_plus_ffs=5305, accuracy_bits=23, luts=2680, ffs=2625, throughput_msps=249, max_abs_err=1.16e-07 (2^-23.04), power_index=6.39
Front coverage: luts_plus_ffs 1110..5305 (HV reference 4000); accuracy_bits 12.3..23 (HV reference 12); data_width on the front 17..27 (registry 8..28).

Per family:
- pipelined: 70 evals, 26 feasible; max throughput seen 282 MSPS; best accuracy 23.04 bits; best feasible luts_plus_ffs=1902; feasible ranges: data_width 17..27, n_iter 14..28, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 130 evals, 53 feasible; max throughput seen 178 MSPS; best accuracy 25.06 bits; best feasible luts_plus_ffs=1110; feasible ranges: data_width 17..26, n_iter 14..29, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 1)
- tokens: 8193 in, 2091 out
- provider-reported cost: $0.0038
- full prompts and replies: `llm_trace.jsonl`

