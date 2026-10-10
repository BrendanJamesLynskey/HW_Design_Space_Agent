# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`pipelined_m:data_width=18,n_iter=14,angle_guard=3,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 868 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 295 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00017 (2^-12.53) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 11.1 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.25e-05 (2^-14.22) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.44 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (26 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=14,angle_guard=3,frac_guard=0,rounding=round,m=4` | 868 | 295 | 93.6 | 6 | 1.4 | 0.00017 (2^-12.53) | 12.53 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 896 | 299 | 93.6 | 6 | 1.44 | 0.000163 (2^-12.58) | 12.58 |
| 2 | `pipelined_m:data_width=18,n_iter=14,angle_guard=3,frac_guard=2,rounding=round,m=4` | 961 | 309 | 93.6 | 6 | 1.53 | 0.000143 (2^-12.77) | 12.77 |
| 3 | `pipelined_m:data_width=18,n_iter=14,angle_guard=3,frac_guard=3,rounding=round,m=4` | 988 | 315 | 93.6 | 6 | 1.57 | 0.000134 (2^-12.86) | 12.86 |
| 4 | `pipelined_m:data_width=19,n_iter=14,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1004 | 323 | 93.6 | 6 | 1.6 | 0.000129 (2^-12.92) | 12.92 |
| 5 | `pipelined_m:data_width=20,n_iter=14,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1047 | 337 | 89.6 | 6 | 1.67 | 0.000125 (2^-12.97) | 12.97 |
| 6 | `pipelined_m:data_width=20,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc,m=3` | 1008 | 386 | 119.3 | 7 | 1.68 | 7.97e-05 (2^-13.61) | 13.61 |
| 7 | `pipelined_m:data_width=20,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc,m=3` | 1023 | 391 | 119.3 | 7 | 1.7 | 7.76e-05 (2^-13.65) | 13.65 |
| 8 | `pipelined_m:data_width=20,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1128 | 327 | 93.6 | 6 | 1.75 | 4.33e-05 (2^-14.50) | 14.50 |
| 9 | `pipelined_m:data_width=20,n_iter=16,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1170 | 329 | 93.6 | 6 | 1.8 | 3.84e-05 (2^-14.67) | 14.67 |
| 10 | `pipelined_m:data_width=18,n_iter=19,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1314 | 377 | 93.6 | 7 | 2.04 | 3.15e-05 (2^-14.95) | 14.95 |
| 11 | `pipelined_m:data_width=20,n_iter=18,angle_guard=1,frac_guard=3,rounding=round,m=4` | 1355 | 410 | 89.6 | 7 | 2.12 | 1.96e-05 (2^-15.64) | 15.64 |
| 12 | `pipelined_m:data_width=20,n_iter=19,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1394 | 402 | 93.6 | 7 | 2.16 | 1.57e-05 (2^-15.96) | 15.96 |
| 13 | `pipelined_m:data_width=20,n_iter=19,angle_guard=3,frac_guard=1,rounding=round,m=4` | 1394 | 404 | 89.6 | 7 | 2.16 | 1.31e-05 (2^-16.22) | 16.22 |
| 14 | `pipelined_m:data_width=21,n_iter=19,angle_guard=3,frac_guard=3,rounding=trunc,m=4` | 1485 | 435 | 89.6 | 7 | 2.31 | 7.43e-06 (2^-17.04) | 17.04 |
| 15 | `pipelined_m:data_width=23,n_iter=22,angle_guard=-1,frac_guard=0,rounding=round,m=3` | 1643 | 652 | 114.5 | 10 | 2.76 | 7.13e-06 (2^-17.10) | 17.10 |
| 16 | `pipelined_m:data_width=23,n_iter=22,angle_guard=0,frac_guard=0,rounding=round,m=3` | 1665 | 660 | 114.5 | 10 | 2.8 | 3.98e-06 (2^-17.94) | 17.94 |
| 17 | `pipelined_m:data_width=23,n_iter=22,angle_guard=0,frac_guard=1,rounding=round,m=2` | 1758 | 912 | 158.3 | 13 | 3.21 | 3.95e-06 (2^-17.95) | 17.95 |
| 18 | `pipelined_m:data_width=24,n_iter=22,angle_guard=0,frac_guard=4,rounding=round,m=3` | 1959 | 745 | 110.0 | 10 | 3.25 | 2.24e-06 (2^-18.77) | 18.77 |
| 19 | `pipelined_m:data_width=24,n_iter=22,angle_guard=4,frac_guard=4,rounding=trunc,m=3` | 1997 | 775 | 110.0 | 10 | 3.34 | 8.23e-07 (2^-20.21) | 20.21 |
| 20 | `pipelined_m:data_width=28,n_iter=22,angle_guard=4,frac_guard=0,rounding=round,m=3` | 2085 | 823 | 105.9 | 10 | 3.5 | 5.26e-07 (2^-20.86) | 20.86 |
| 21 | `pipelined_m:data_width=26,n_iter=27,angle_guard=1,frac_guard=2,rounding=trunc,m=3` | 2444 | 866 | 110.0 | 11 | 3.98 | 3.25e-07 (2^-21.55) | 21.55 |
| 22 | `pipelined_m:data_width=28,n_iter=28,angle_guard=4,frac_guard=0,rounding=round,m=3` | 2680 | 1015 | 105.9 | 12 | 4.45 | 1.03e-07 (2^-23.22) | 23.22 |
| 23 | `pipelined:data_width=28,n_iter=27,angle_guard=1,frac_guard=2,rounding=trunc` | 2608 | 2607 | 249.0 | 29 | 6.28 | 9.77e-08 (2^-23.29) | 23.29 |
| 24 | `pipelined:data_width=28,n_iter=27,angle_guard=3,frac_guard=2,rounding=trunc` | 2663 | 2662 | 242.0 | 29 | 6.41 | 6.96e-08 (2^-23.78) | 23.78 |
| 25 | `pipelined:data_width=28,n_iter=27,angle_guard=3,frac_guard=2,rounding=round` | 2722 | 2664 | 242.0 | 29 | 6.48 | 4.62e-08 (2^-24.37) | 24.37 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec's binding constraints are accuracy (max_abs_err <= 2^-12) and the burst deadline (32 results within 0.44 us), with area minimised. Both assigned families emit 1 result/cycle, so throughput_msps equals Fmax and the >=32 MSps constraint is trivially met; the real risk is sys_p99_batch_us, which needs Fmax high enough that ~32 accept cycles plus the pipeline latency fit in 440 ns, so m must not be pushed so large that Fmax collapses. Since accuracy depends only on W/N/guards/rounding, I search the same accuracy box in both families and let the area/Fmax difference decide. Budget is weighted toward pipelined_m because the fleet's numbers show it dominating the merged front and holding the cheapest feasible design, while pipelined is kept as the high-Fmax fallback. Ranges deliberately include the low-area corner (small W, N near the 12-bit limit, large m, round) where the min-luts_plus_ffs selection rule will land, and extend to larger W/N so the front is spanned for hypervolume.*)
- `pipelined_m` (70 evals): data_width=13..22, n_iter=10..22, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* This family already owns 10 of the 11 merged-front designs and the cheapest feasible point (1144 LUT+FF): registering only every m stages keeps 1 result/cycle while cutting FFs, which is exactly the min-area objective. I span the low-area corner (W just above the 12-bit output-LSB limit, N just above the accuracy limit, large m) up to high accuracy for hypervolume, and keep the full m range so the Fmax/burst-deadline trade-off is visible.
- `pipelined` (30 evals): data_width=13..22, n_iter=10..22, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round. *Why:* Fully-pipelined (m=1) is the high-Fmax / high-FF corner: same accuracy bits as pipelined_m for identical W/N/guards/rounding but more registers. It is the fallback if the burst deadline (32 results in 0.44 us) squeezes the low-Fmax pipelined_m points, so I keep a smaller share to cover that edge of the front.

**Result (code):** 100 evaluations this round, 100 total; 58 feasible; hypervolume 1.219e+04 (n/a).

**LLM decision:** `map_front` — Round 1 explored only pipelined and pipelined_m (code reports no other family left to add), and the feasible front is thin: 14 designs, all clustered at data_width 18..21, n_iter 14..19, m=4. The per-family feasible ranges are much wider (pipelined_m: data_width 16..22, n_iter 14..21, m 2..4), so the current front covers only a narrow slice of the area objective (1163..1920 against HV ref 4000) and never probes m=2/3 or data_width 16..17, which are exactly where the min-luts_plus_ffs selection rule could find a cheaper design. Constraints are not the bottleneck: throughput best 273 MSPS vs >=32, sys_p99_batch best 0.158 us vs <=0.44, and accuracy already reaches 2^-17.04 vs the 2^-12 requirement, so there is room to trade accuracy for area. With 100 evals left, spending this round on NSGA-II over the full ranges of pipelined/pipelined_m seeded with the current front is the best way to fill in the trade-off curve and possibly lower the cheapest feasible design before the reserved final mapping round.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.219e+04 (gain this round: n/a (first round)).
Feasible designs: 58 of 100 evaluations (50 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 33% violate; best seen 7.43e-06 (2^-17.04)
- sys_p99_batch_us <= 0.44: 18% violate; best seen 0.158

Pareto front (feasible, 14 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=3 frac_guard=0 rounding=round m=4] luts_plus_ffs=1163, accuracy_bits=12.5, luts=868, ffs=295, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.53), power_index=1.4
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1194, accuracy_bits=12.6, luts=896, ffs=299, throughput_msps=93.6, max_abs_err=0.000163 (2^-12.58), power_index=1.44
- pipelined_m [data_width=18 n_iter=14 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1303, accuracy_bits=12.9, luts=988, ffs=315, throughput_msps=93.6, max_abs_err=0.000134 (2^-12.86), power_index=1.57
- pipelined_m [data_width=19 n_iter=14 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1327, accuracy_bits=12.9, luts=1004, ffs=323, throughput_msps=93.6, max_abs_err=0.000129 (2^-12.92), power_index=1.6
- pipelined_m [data_width=21 n_iter=14 angle_guard=3 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1429, accuracy_bits=13, luts=1074, ffs=355, throughput_msps=89.6, max_abs_err=0.000124 (2^-12.97), power_index=1.72
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1454, accuracy_bits=14.5, luts=1128, ffs=327, throughput_msps=93.6, max_abs_err=4.33e-05 (2^-14.50), power_index=1.75
- pipelined_m [data_width=18 n_iter=19 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1691, accuracy_bits=15, luts=1314, ffs=377, throughput_msps=93.6, max_abs_err=3.15e-05 (2^-14.95), power_index=2.04
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=3 rounding=round m=4] luts_plus_ffs=1765, accuracy_bits=15.6, luts=1355, ffs=410, throughput_msps=89.6, max_abs_err=1.96e-05 (2^-15.64), power_index=2.12
- pipelined_m [data_width=20 n_iter=19 angle_guard=3 frac_guard=1 rounding=round m=4] luts_plus_ffs=1798, accuracy_bits=16.2, luts=1394, ffs=404, throughput_msps=89.6, max_abs_err=1.31e-05 (2^-16.22), power_index=2.16
- pipelined_m [data_width=21 n_iter=19 angle_guard=3 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1920, accuracy_bits=17, luts=1485, ffs=435, throughput_msps=89.6, max_abs_err=7.43e-06 (2^-17.04), power_index=2.31
Front coverage: luts_plus_ffs 1163..1920 (HV reference 4000); accuracy_bits 12.5..17 (HV reference 12); data_width on the front 18..21 (registry 8..28).

Per family:
- pipelined: 30 evals, 19 feasible; max throughput seen 273 MSPS; best accuracy 17.04 bits; best feasible luts_plus_ffs=2002; feasible ranges: data_width 18..21, n_iter 16..22, angle_guard -1..2, frac_guard 0..3
- pipelined_m: 70 evals, 39 feasible; max throughput seen 171 MSPS; best accuracy 17.04 bits; best feasible luts_plus_ffs=1163; feasible ranges: data_width 16..22, n_iter 14..21, angle_guard -2..3, frac_guard 0..3, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `pipelined_m` (20 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (14 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 67 feasible; hypervolume 1.572e+04 (+29.0%).

**LLM decision:** `refine` — All families are already explored (none left to add) and the feasible ranges are not obviously clamped (pipelined_m feasible data_width 16..26 vs registry 8..28, n_iter 14..29 vs 4..30, m 2..4 vs 2..8), so widening is not indicated. The front is well spread in accuracy (12.5..21.6 bits vs HV ref 12) but the selection rule is min luts_plus_ffs, and the cheapest point (1163, 12.5 bits, 93.6 MSPS) sits only ~0.5 bit above the 2^-12 constraint and its L1 sys_p99_batch bound is the tightest region (best seen 0.158 us vs 0.44 limit, and 23% of evals violate it), so it is the design most at risk of being dropped at L2. Spending this round refining the low-area corner of pipelined_m (to find a cheaper or more robust design that still clears 12 bits) plus a slice on pipelined (the only family reaching 273 MSPS) is the highest-value use of the remaining 80 evals; code still holds reserved budget to map the full front at the end.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.572e+04 (gain this round: +29.0%).
Feasible designs: 67 of 120 evaluations (59 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 32% violate; best seen 3.25e-07 (2^-21.55)
- sys_p99_batch_us <= 0.44: 23% violate; best seen 0.158

Pareto front (feasible, 16 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=3 frac_guard=0 rounding=round m=4] luts_plus_ffs=1163, accuracy_bits=12.5, luts=868, ffs=295, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.53), power_index=1.4
- pipelined_m [data_width=18 n_iter=14 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1270, accuracy_bits=12.8, luts=961, ffs=309, throughput_msps=93.6, max_abs_err=0.000143 (2^-12.77), power_index=1.53
- pipelined_m [data_width=18 n_iter=14 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1303, accuracy_bits=12.9, luts=988, ffs=315, throughput_msps=93.6, max_abs_err=0.000134 (2^-12.86), power_index=1.57
- pipelined_m [data_width=20 n_iter=14 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1384, accuracy_bits=13, luts=1047, ffs=337, throughput_msps=89.6, max_abs_err=0.000125 (2^-12.97), power_index=1.67
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1454, accuracy_bits=14.5, luts=1128, ffs=327, throughput_msps=93.6, max_abs_err=4.33e-05 (2^-14.50), power_index=1.75
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1499, accuracy_bits=14.7, luts=1170, ffs=329, throughput_msps=93.6, max_abs_err=3.84e-05 (2^-14.67), power_index=1.8
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=3 rounding=round m=4] luts_plus_ffs=1765, accuracy_bits=15.6, luts=1355, ffs=410, throughput_msps=89.6, max_abs_err=1.96e-05 (2^-15.64), power_index=2.12
- pipelined_m [data_width=20 n_iter=19 angle_guard=3 frac_guard=1 rounding=round m=4] luts_plus_ffs=1798, accuracy_bits=16.2, luts=1394, ffs=404, throughput_msps=89.6, max_abs_err=1.31e-05 (2^-16.22), power_index=2.16
- pipelined_m [data_width=21 n_iter=19 angle_guard=3 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1920, accuracy_bits=17, luts=1485, ffs=435, throughput_msps=89.6, max_abs_err=7.43e-06 (2^-17.04), power_index=2.31
- pipelined_m [data_width=26 n_iter=27 angle_guard=1 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=3309, accuracy_bits=21.6, luts=2444, ffs=866, throughput_msps=110, max_abs_err=3.25e-07 (2^-21.55), power_index=3.98
Front coverage: luts_plus_ffs 1163..3309 (HV reference 4000); accuracy_bits 12.5..21.6 (HV reference 12); data_width on the front 18..26 (registry 8..28).

Per family:
- pipelined: 30 evals, 19 feasible; max throughput seen 273 MSPS; best accuracy 17.04 bits; best feasible luts_plus_ffs=2002; feasible ranges: data_width 18..21, n_iter 16..22, angle_guard -1..2, frac_guard 0..3
- pipelined_m: 90 evals, 48 feasible; max throughput seen 171 MSPS; best accuracy 21.55 bits; best feasible luts_plus_ffs=1163; feasible ranges: data_width 16..26, n_iter 14..29, angle_guard -2..3, frac_guard 0..4, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *All families are already explored (none left to add) and the feasible ranges are not obviously clamped (pipelined_m feasible data_width 16..26 vs registry 8..28, n_iter 14..29 vs 4..30, m 2..4 vs 2..8), so widening is not indicated. The front is well spread in accuracy (12.5..21.6 bits vs HV ref 12) but the selection rule is min luts_plus_ffs, and the cheapest point (1163, 12.5 bits, 93.6 MSPS) sits only ~0.5 bit above the 2^-12 constraint and its L1 sys_p99_batch bound is the tightest region (best seen 0.158 us vs 0.44 limit, and 23% of evals violate it), so it is the design most at risk of being dropped at L2. Spending this round refining the low-area corner of pipelined_m (to find a cheaper or more robust design that still clears 12 bits) plus a slice on pipelined (the only family reaching 273 MSPS) is the highest-value use of the remaining 80 evals; code still holds reserved budget to map the full front at the end.*)
- `pipelined_m` (56 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* cheapest feasible designs and the whole low-area corner live here; tighten around the 1163-1500 region to try to push luts_plus_ffs below 1163 while keeping accuracy_bits >= 12
- `pipelined` (24 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* only family with a distinct throughput point (max 273 MSPS); check whether a higher-throughput, still-cheap design can survive the L2 system screen better than the marginal 93.6 MSPS pipelined_m corner

**Result (code):** 80 evaluations this round, 200 total; 118 feasible; hypervolume 1.828e+04 (+16.3%).

**LLM decision:** `stop` — Budget is exhausted (200/200 evals, round 3 of 4) and the front is both feasible and well covered, so no further exploration is possible or needed. All three constraints are met by existing designs: throughput_msps >= 32 (0% violations, best 273), max_abs_err <= 2^-12 (best 4.62e-08 = 2^-24.37), and sys_p99_batch_us <= 0.44 (best 0.14). The feasible Pareto front holds 26 designs spanning luts_plus_ffs 1163..5385 against the HV reference 4000 and accuracy_bits 12.5..24.4 against the HV reference 12, i.e. it covers both objective ranges rather than a single corner, and hypervolume is still improving (+16.3% this round, 1.828e+04). The selection rule (min luts_plus_ffs) is served by pipelined_m [data_width=18 n_iter=14 angle_guard=3 frac_guard=0 rounding=round m=4] at luts_plus_ffs=1163 with accuracy_bits=12.5, comfortably inside the error bound. Both families on the front (pipelined, pipelined_m) have been explored and no family remains unexplored, so there is nothing to add or widen. Note only that the cheapest designs sit near the sys_p99_batch_us bound (best 0.14 vs 0.44), so the L2 re-selection may drop some of them; this is a selection-stage risk, not a reason to continue exploring.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.828e+04 (gain this round: +16.3%).
Feasible designs: 118 of 200 evaluations (105 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 27% violate; best seen 4.62e-08 (2^-24.37)
- sys_p99_batch_us <= 0.44: 24% violate; best seen 0.14

Pareto front (feasible, 26 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=3 frac_guard=0 rounding=round m=4] luts_plus_ffs=1163, accuracy_bits=12.5, luts=868, ffs=295, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.53), power_index=1.4
- pipelined_m [data_width=18 n_iter=14 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1303, accuracy_bits=12.9, luts=988, ffs=315, throughput_msps=93.6, max_abs_err=0.000134 (2^-12.86), power_index=1.57
- pipelined_m [data_width=20 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1395, accuracy_bits=13.6, luts=1008, ffs=386, throughput_msps=119, max_abs_err=7.97e-05 (2^-13.61), power_index=1.68
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1454, accuracy_bits=14.5, luts=1128, ffs=327, throughput_msps=93.6, max_abs_err=4.33e-05 (2^-14.50), power_index=1.75
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=3 rounding=round m=4] luts_plus_ffs=1765, accuracy_bits=15.6, luts=1355, ffs=410, throughput_msps=89.6, max_abs_err=1.96e-05 (2^-15.64), power_index=2.12
- pipelined_m [data_width=21 n_iter=19 angle_guard=3 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1920, accuracy_bits=17, luts=1485, ffs=435, throughput_msps=89.6, max_abs_err=7.43e-06 (2^-17.04), power_index=2.31
- pipelined_m [data_width=23 n_iter=22 angle_guard=0 frac_guard=1 rounding=round m=2] luts_plus_ffs=2670, accuracy_bits=17.9, luts=1758, ffs=912, throughput_msps=158, max_abs_err=3.95e-06 (2^-17.95), power_index=3.21
- pipelined_m [data_width=24 n_iter=22 angle_guard=4 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=2772, accuracy_bits=20.2, luts=1997, ffs=775, throughput_msps=110, max_abs_err=8.23e-07 (2^-20.21), power_index=3.34
- pipelined_m [data_width=28 n_iter=28 angle_guard=4 frac_guard=0 rounding=round m=3] luts_plus_ffs=3695, accuracy_bits=23.2, luts=2680, ffs=1015, throughput_msps=106, max_abs_err=1.03e-07 (2^-23.22), power_index=4.45
- pipelined [data_width=28 n_iter=27 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=5385, accuracy_bits=24.4, luts=2722, ffs=2664, throughput_msps=242, max_abs_err=4.62e-08 (2^-24.37), power_index=6.48
Front coverage: luts_plus_ffs 1163..5385 (HV reference 4000); accuracy_bits 12.5..24.4 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- pipelined: 54 evals, 38 feasible; max throughput seen 273 MSPS; best accuracy 24.37 bits; best feasible luts_plus_ffs=2002; feasible ranges: data_width 18..28, n_iter 14..28, angle_guard -2..3, frac_guard 0..4
- pipelined_m: 146 evals, 80 feasible; max throughput seen 171 MSPS; best accuracy 23.22 bits; best feasible luts_plus_ffs=1163; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 13165 in, 12608 out
- provider-reported cost: $0.0142
- full prompts and replies: `llm_trace.jsonl`

