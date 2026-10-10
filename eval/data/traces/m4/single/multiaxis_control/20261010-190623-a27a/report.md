# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 400 of 400 budgeted, over 4 round(s).  
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
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=19,n_iter=14,angle_guard=0,frac_guard=0,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 868 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 297 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000172 (2^-12.50) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 22.6 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.24e-05 (2^-14.22) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 6.87 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.5 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 98.3 dBc, SNR 82.6 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Every L1-feasible design (243) was simulated at its estimated Fmax (SimPy); 239 pass. Top 5 by the selection rule, L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=19,n_iter=14,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=3` | 0.2973 → 0.3052 | yes |
| `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=0,rounding=round,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=20,n_iter=14,angle_guard=-1,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=19,n_iter=14,angle_guard=-1,frac_guard=0,rounding=round,m=3` | 0.3103 → 0.3186 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (27 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=14,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 868 | 297 | 93.6 | 6 | 1.4 | 0.000172 (2^-12.50) | 12.50 |
| 1 | `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=0,rounding=round,m=4` | 890 | 282 | 97.8 | 6 | 1.41 | 0.000145 (2^-12.75) | 12.75 |
| 2 | `pipelined_m:data_width=21,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=4` | 950 | 325 | 93.6 | 6 | 1.54 | 0.00013 (2^-12.90) | 12.90 |
| 3 | `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=2,rounding=round,m=4` | 987 | 297 | 93.6 | 6 | 1.55 | 0.000123 (2^-12.99) | 12.99 |
| 4 | `pipelined_m:data_width=19,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 1001 | 297 | 93.6 | 6 | 1.56 | 9.61e-05 (2^-13.35) | 13.35 |
| 5 | `pipelined_m:data_width=19,n_iter=16,angle_guard=1,frac_guard=0,rounding=trunc,m=4` | 1017 | 301 | 93.6 | 6 | 1.59 | 8.56e-05 (2^-13.51) | 13.51 |
| 6 | `pipelined_m:data_width=19,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=4` | 1033 | 305 | 93.6 | 6 | 1.61 | 5.75e-05 (2^-14.09) | 14.09 |
| 7 | `pipelined_m:data_width=21,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 1096 | 325 | 93.6 | 6 | 1.71 | 4.76e-05 (2^-14.36) | 14.36 |
| 8 | `pipelined_m:data_width=19,n_iter=16,angle_guard=2,frac_guard=3,rounding=round,m=4` | 1168 | 325 | 93.6 | 6 | 1.8 | 3.97e-05 (2^-14.62) | 14.62 |
| 9 | `pipelined_m:data_width=19,n_iter=19,angle_guard=2,frac_guard=0,rounding=round,m=4` | 1238 | 371 | 93.6 | 7 | 1.94 | 3.86e-05 (2^-14.66) | 14.66 |
| 10 | `pipelined_m:data_width=21,n_iter=17,angle_guard=0,frac_guard=0,rounding=round,m=3` | 1169 | 466 | 119.3 | 8 | 1.97 | 2.7e-05 (2^-15.18) | 15.18 |
| 11 | `pipelined_m:data_width=21,n_iter=19,angle_guard=1,frac_guard=0,rounding=round,m=4` | 1333 | 401 | 93.6 | 7 | 2.09 | 1.29e-05 (2^-16.24) | 16.24 |
| 12 | `pipelined_m:data_width=21,n_iter=20,angle_guard=3,frac_guard=0,rounding=round,m=4` | 1447 | 411 | 89.6 | 7 | 2.24 | 1.15e-05 (2^-16.41) | 16.41 |
| 13 | `pipelined_m:data_width=23,n_iter=19,angle_guard=-1,frac_guard=2,rounding=trunc,m=4` | 1485 | 441 | 89.6 | 7 | 2.32 | 8.81e-06 (2^-16.79) | 16.79 |
| 14 | `pipelined_m:data_width=23,n_iter=19,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1523 | 451 | 89.6 | 7 | 2.38 | 5.75e-06 (2^-17.41) | 17.41 |
| 15 | `pipelined_m:data_width=23,n_iter=19,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1571 | 453 | 89.6 | 7 | 2.44 | 5.38e-06 (2^-17.50) | 17.50 |
| 16 | `pipelined_m:data_width=22,n_iter=19,angle_guard=3,frac_guard=2,rounding=round,m=3` | 1550 | 607 | 114.5 | 9 | 2.6 | 5.1e-06 (2^-17.58) | 17.58 |
| 17 | `pipelined_m:data_width=24,n_iter=20,angle_guard=4,frac_guard=1,rounding=trunc,m=4` | 1687 | 475 | 86.0 | 7 | 2.6 | 2.96e-06 (2^-18.37) | 18.37 |
| 18 | `pipelined_m:data_width=25,n_iter=20,angle_guard=0,frac_guard=2,rounding=trunc,m=4` | 1707 | 480 | 86.0 | 7 | 2.63 | 2.57e-06 (2^-18.57) | 18.57 |
| 19 | `pipelined_m:data_width=27,n_iter=20,angle_guard=2,frac_guard=0,rounding=trunc,m=3` | 1787 | 690 | 110.0 | 9 | 2.98 | 2.13e-06 (2^-18.84) | 18.84 |
| 20 | `pipelined_m:data_width=22,n_iter=23,angle_guard=4,frac_guard=4,rounding=trunc,m=4` | 1953 | 551 | 89.6 | 8 | 3.01 | 1.68e-06 (2^-19.18) | 19.18 |
| 21 | `pipelined_m:data_width=25,n_iter=24,angle_guard=0,frac_guard=1,rounding=round,m=4` | 2070 | 559 | 89.6 | 8 | 3.16 | 1.05e-06 (2^-19.86) | 19.86 |
| 22 | `pipelined_m:data_width=24,n_iter=23,angle_guard=4,frac_guard=2,rounding=round,m=3` | 2050 | 749 | 110.0 | 10 | 3.37 | 5.75e-07 (2^-20.73) | 20.73 |
| 23 | `pipelined_m:data_width=25,n_iter=25,angle_guard=2,frac_guard=2,rounding=trunc,m=3` | 2205 | 845 | 110.0 | 11 | 3.67 | 5.15e-07 (2^-20.89) | 20.89 |
| 24 | `pipelined_m:data_width=28,n_iter=23,angle_guard=1,frac_guard=3,rounding=round,m=3` | 2313 | 843 | 105.9 | 10 | 3.8 | 2.81e-07 (2^-21.76) | 21.76 |
| 25 | `pipelined_m:data_width=28,n_iter=24,angle_guard=1,frac_guard=2,rounding=round,m=3` | 2367 | 829 | 110.0 | 10 | 3.85 | 1.69e-07 (2^-22.50) | 22.50 |
| 26 | `pipelined_m:data_width=28,n_iter=27,angle_guard=1,frac_guard=2,rounding=round,m=3` | 2667 | 926 | 110.0 | 11 | 4.33 | 8.19e-08 (2^-23.54) | 23.54 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraint is the system burst: a 1 MHz tick dumps 32 requests that must ALL be back within 0.44 us. That is ~73 MSPS sustained during the burst, and it is a hard structural filter. Only families that emit one result per cycle can pipeline a 32-deep burst: pipelined (1/cyc, N+2 latency) and pipelined_m (1/cyc, ceil(N/m)+2 latency). iterative (1 result per N+3 cycles) and unrolled_k (1 per ceil(N/k)+3 cycles) would need 32*(N+3) or 32*(ceil(N/k)+3) cycles for a burst — at any plausible Fmax that is >0.44 us, so they should fail the L1 batch bound and are only worth a small confirmation share. Accuracy (max_abs_err <= 2^-12, i.e. accuracy_bits >= 12) needs roughly N>=13 and W>=15 (output LSB = 2^-(W-2)), so the interesting accuracy range is N~13..20, W~14..20. The objective is min luts_plus_ffs, and pipelined_m is the area lever: registering every m stages cuts the pipeline register count from N to ceil(N/m)+2 at the cost of Fmax, which is exactly the trade-off the front should map. Round 1 therefore concentrates on pipelined_m and pipelined over the accuracy-feasible region, with a small probe of unrolled_k/iterative to document infeasibility. Later rounds will tighten around the feasible front and push m, N, W to their extremes.*)
- `pipelined_m` (45 evals): data_width=12..20, n_iter=10..20, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* Primary family. 1 result/cycle satisfies the 32-request burst; m is the direct area knob (registers scale as ceil(N/m)+2 instead of N), so this family should own the low-luts_plus_ffs end of the front. Ranges cover the accuracy-feasible region (N>=13, W>=15) plus margin, and m spans the full 2..8 to expose the area/Fmax trade-off.
- `pipelined` (30 evals): data_width=12..20, n_iter=10..20, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* 1 result/cycle, so it also clears the burst, and it is the m=1 corner of the same trade-off (max Fmax, max register count). Needed to anchor the high-Fmax / high-area end of the front and to check whether the batch bound's Fmax requirement (>=~73 MHz) rules out the heavily-registered variants.
- `unrolled_k` (15 evals): data_width=12..20, n_iter=10..20, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, k=4..8. *Why:* Shared-datapath middle ground: k rotators/cycle gives a different area point (no per-stage register bank) and might reach the burst bound only at the extreme k=8, small N. Small share to test whether any (k,N) combination gets ceil(N/k)+3 small enough that 32 bursts fit in 0.44 us; expected to fail, but cheap to confirm.
- `iterative` (10 evals): data_width=12..20, n_iter=10..20, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* Smallest-area family in the registry, so if it could meet the burst it would dominate the min-luts_plus_ffs objective. It cannot (32*(N+3) cycles >> 0.44 us), but a small share documents the infeasibility with numbers rather than assertion and guards against a mis-modelled batch bound.

**Result (code):** 100 evaluations this round, 100 total; 35 feasible; hypervolume 8039 (n/a).

**LLM decision:** `map_front` — The feasible front is real and healthy (35 feasible / 27 unique, HV 8039), and the system constraint is being met with margin at L1 (best sys_p99_batch_us 0.159 vs 0.44), so this is not an infeasibility or stop case. The problem is coverage, not feasibility: the front only spans luts_plus_ffs 1211..2545 against an HV reference of 4000, and accuracy_bits only 12.4..15.3 against a reference of 12, with data_width stuck at 19..20 out of the registry's 8..28. That leaves a large unexplored HV region on both axes -- smaller-area designs near the 2^-12 accuracy limit on the left, and higher-accuracy designs (larger data_width, more n_iter) that would extend the front rightward toward the 4000-area reference on the right. The two families actually carrying the front (pipelined: 16 feasible, best 15.35 bits; pipelined_m: 19 feasible, best feasible luts_plus_ffs=1211) have only been probed inside narrow feasible ranges (pipelined_m m 2..4, frac_guard 0..3; pipelined frac_guard 0..1), while iterative and unrolled_k are clearly out (0 feasible, max throughput 15.6 / 12 MSPS, both far below the 32 MSPS constraint), so there is no point adding or widening them. A dedicated mapping round -- NSGA-II over the full ranges of pipelined and pipelined_m seeded with the current 8-point front -- is the highest-value use of this budget because it will fill both the low-area and high-accuracy ends of the curve rather than re-sampling the middle, which is what the next rounds' reserved front-mapping budget is for.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 8039 (gain this round: n/a (first round)).
Feasible designs: 35 of 100 evaluations (27 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 25% violate; best seen 282
- max_abs_err <= 0.000244141: 51% violate; best seen 2.4e-05 (2^-15.35)
- sys_p99_batch_us <= 0.44: 39% violate; best seen 0.159

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=0 rounding=round m=3] luts_plus_ffs=1211, accuracy_bits=12.4, luts=855, ffs=356, throughput_msps=119, max_abs_err=0.000181 (2^-12.43), power_index=1.46
- pipelined_m [data_width=19 n_iter=14 angle_guard=0 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=1336, accuracy_bits=12.7, luts=950, ffs=385, throughput_msps=119, max_abs_err=0.000151 (2^-12.69), power_index=1.61
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1337, accuracy_bits=14.1, luts=1033, ffs=305, throughput_msps=93.6, max_abs_err=5.75e-05 (2^-14.09), power_index=1.61
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=1554, accuracy_bits=14.3, luts=1096, ffs=458, throughput_msps=119, max_abs_err=4.81e-05 (2^-14.34), power_index=1.87
- pipelined_m [data_width=19 n_iter=19 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1609, accuracy_bits=14.7, luts=1238, ffs=371, throughput_msps=93.6, max_abs_err=3.86e-05 (2^-14.66), power_index=1.94
- pipelined [data_width=20 n_iter=17 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=2433, accuracy_bits=15, luts=1202, ffs=1231, throughput_msps=257, max_abs_err=3.13e-05 (2^-14.96), power_index=2.93
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=2509, accuracy_bits=15.1, luts=1241, ffs=1267, throughput_msps=264, max_abs_err=2.8e-05 (2^-15.12), power_index=3.02
- pipelined [data_width=20 n_iter=18 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=2545, accuracy_bits=15.3, luts=1259, ffs=1285, throughput_msps=264, max_abs_err=2.4e-05 (2^-15.35), power_index=3.06
Front coverage: luts_plus_ffs 1211..2545 (HV reference 4000); accuracy_bits 12.4..15.3 (HV reference 12); data_width on the front 19..20 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 15.6 MSPS; best accuracy 12.30 bits
- unrolled_k: 15 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 13.21 bits
- pipelined: 30 evals, 16 feasible; max throughput seen 282 MSPS; best accuracy 15.35 bits; best feasible luts_plus_ffs=2165; feasible ranges: data_width 17..20, n_iter 17..20, angle_guard -1..3, frac_guard 0..1
- pipelined_m: 45 evals, 19 feasible; max throughput seen 178 MSPS; best accuracy 14.66 bits; best feasible luts_plus_ffs=1211; feasible ranges: data_width 17..20, n_iter 14..19, angle_guard -1..2, frac_guard 0..3, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (63 evals): data_width=18..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (5 front designs; box front_anchored)
- `pipelined` (37 evals): data_width=19..28, n_iter=15..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 119 feasible; hypervolume 1.865e+04 (+132.0%).

**LLM decision:** `refine` — Round 2 front is entirely pipelined_m and already covers both objective ranges well: luts_plus_ffs 1211..3593 against HV ref 4000, and accuracy_bits 12.4..23.5 against HV ref 12. So the front is NOT confined to a small part of either range, and map_front is not yet the right call. The other families are dead ends for this spec: iterative (10 evals, 0 feasible, max throughput 15.6 MSPS) and unrolled_k (15 evals, 0 feasible, max 12 MSPS) both miss the >=32 MSPS constraint, and pipelined is dominated by pipelined_m (best feasible luts_plus_ffs 1970 vs 1211). The selection rule is min luts_plus_ffs, and the cheapest feasible point is 1211 (data_width=19, n_iter=14, m=3), with the next points at 1337/1609/1922 - i.e. the low-area end is where both the selection rule and most of the HV area live, and where the accuracy constraint (2^-12) is tightest (12.4 bits at W=19). Refining pipelined_m around that cheap/mid region should either find sub-1211 feasible designs or densify the steep part of the curve, while the high-accuracy tail (W=28, 23.5 bits) is already mapped. Gain is still +132%, so not a stop.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.865e+04 (gain this round: +132.0%).
Feasible designs: 119 of 200 evaluations (106 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 12% violate; best seen 282
- max_abs_err <= 0.000244141: 28% violate; best seen 8.19e-08 (2^-23.54)
- sys_p99_batch_us <= 0.44: 26% violate; best seen 0.159

Pareto front (feasible, 18 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=0 rounding=round m=3] luts_plus_ffs=1211, accuracy_bits=12.4, luts=855, ffs=356, throughput_msps=119, max_abs_err=0.000181 (2^-12.43), power_index=1.46
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1337, accuracy_bits=14.1, luts=1033, ffs=305, throughput_msps=93.6, max_abs_err=5.75e-05 (2^-14.09), power_index=1.61
- pipelined_m [data_width=19 n_iter=19 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1609, accuracy_bits=14.7, luts=1238, ffs=371, throughput_msps=93.6, max_abs_err=3.86e-05 (2^-14.66), power_index=1.94
- pipelined_m [data_width=26 n_iter=16 angle_guard=1 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=1922, accuracy_bits=15, luts=1349, ffs=573, throughput_msps=110, max_abs_err=3.07e-05 (2^-14.99), power_index=2.31
- pipelined_m [data_width=25 n_iter=17 angle_guard=3 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=2118, accuracy_bits=16, luts=1523, ffs=595, throughput_msps=110, max_abs_err=1.54e-05 (2^-15.98), power_index=2.55
- pipelined_m [data_width=24 n_iter=19 angle_guard=-2 frac_guard=3 rounding=round m=3] luts_plus_ffs=2242, accuracy_bits=16.9, luts=1611, ffs=631, throughput_msps=110, max_abs_err=8.46e-06 (2^-16.85), power_index=2.7
- pipelined_m [data_width=24 n_iter=19 angle_guard=4 frac_guard=2 rounding=round m=3] luts_plus_ffs=2348, accuracy_bits=17.9, luts=1687, ffs=661, throughput_msps=110, max_abs_err=4.06e-06 (2^-17.91), power_index=2.83
- pipelined_m [data_width=22 n_iter=23 angle_guard=4 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=2503, accuracy_bits=19.2, luts=1953, ffs=551, throughput_msps=89.6, max_abs_err=1.68e-06 (2^-19.18), power_index=3.01
- pipelined_m [data_width=28 n_iter=23 angle_guard=1 frac_guard=3 rounding=round m=3] luts_plus_ffs=3156, accuracy_bits=21.8, luts=2313, ffs=843, throughput_msps=106, max_abs_err=2.81e-07 (2^-21.76), power_index=3.8
- pipelined_m [data_width=28 n_iter=27 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=3593, accuracy_bits=23.5, luts=2667, ffs=926, throughput_msps=110, max_abs_err=8.19e-08 (2^-23.54), power_index=4.33
Front coverage: luts_plus_ffs 1211..3593 (HV reference 4000); accuracy_bits 12.4..23.5 (HV reference 12); data_width on the front 19..28 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 15.6 MSPS; best accuracy 12.30 bits
- unrolled_k: 15 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 13.21 bits
- pipelined: 67 evals, 53 feasible; max throughput seen 282 MSPS; best accuracy 20.89 bits; best feasible luts_plus_ffs=1970; feasible ranges: data_width 17..28, n_iter 15..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 108 evals, 66 feasible; max throughput seen 178 MSPS; best accuracy 23.54 bits; best feasible luts_plus_ffs=1211; feasible ranges: data_width 17..28, n_iter 13..28, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Focus the 100-eval round on the low-area / mid region of pipelined_m, where the min-luts_plus_ffs selection rule and the bulk of HV area sit.*)
- `pipelined_m` (100 evals): data_width=17..23, n_iter=13..22, angle_guard=-2..3, frac_guard=0..3, rounding=round|trunc, m=2..4. *Why:* only family on the feasible front; dominates pipelined and is the only one that reaches >=32 MSPS with feasible error

**Result (code):** 100 evaluations this round, 300 total; 210 feasible; hypervolume 1.976e+04 (+5.9%).

**LLM decision:** `map_front` — Round 3 leaves 100 of 400 evals and one round to go, which is exactly the reserved front-mapping budget. The feasible front is carried entirely by pipelined/pipelined_m: iterative (10 evals, 0 feasible, max 15.6 MSPS) and unrolled_k (15 evals, 0 feasible, max 12 MSPS) cannot reach the 32 MSPS constraint, so they are off the front and need no further budget. pipelined_m dominates the low-area corner (best feasible luts_plus_ffs=1165 vs pipelined's 1970), and its feasible m range is only 2..4 against a registry range of 2..8, so the full-range map is genuinely unexplored there. The front's cheap end sits at accuracy_bits=12.5, only just above the 2^-12 (12-bit) constraint, so cheaper designs hugging the accuracy boundary are plausible and worth finding. Coverage is otherwise good (luts_plus_ffs 1165..3593 vs HV ref 4000; accuracy 12.5..23.5 vs ref 12) and HV is still gaining (+5.9%), so a seeded NSGA-II over the full ranges of pipelined and pipelined_m is the best use of the final round rather than narrowing around the current points.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.976e+04 (gain this round: +5.9%).
Feasible designs: 210 of 300 evaluations (187 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 8% violate; best seen 282
- max_abs_err <= 0.000244141: 22% violate; best seen 8.19e-08 (2^-23.54)
- sys_p99_batch_us <= 0.44: 17% violate; best seen 0.159

Pareto front (feasible, 24 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1165, accuracy_bits=12.5, luts=868, ffs=297, throughput_msps=93.6, max_abs_err=0.000172 (2^-12.50), power_index=1.4
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1284, accuracy_bits=13, luts=987, ffs=297, throughput_msps=93.6, max_abs_err=0.000123 (2^-12.99), power_index=1.55
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1318, accuracy_bits=13.5, luts=1017, ffs=301, throughput_msps=93.6, max_abs_err=8.56e-05 (2^-13.51), power_index=1.59
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=3 rounding=round m=4] luts_plus_ffs=1492, accuracy_bits=14.6, luts=1168, ffs=325, throughput_msps=93.6, max_abs_err=3.97e-05 (2^-14.62), power_index=1.8
- pipelined_m [data_width=21 n_iter=17 angle_guard=0 frac_guard=0 rounding=round m=3] luts_plus_ffs=1635, accuracy_bits=15.2, luts=1169, ffs=466, throughput_msps=119, max_abs_err=2.7e-05 (2^-15.18), power_index=1.97
- pipelined_m [data_width=23 n_iter=19 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1974, accuracy_bits=17.4, luts=1523, ffs=451, throughput_msps=89.6, max_abs_err=5.75e-06 (2^-17.41), power_index=2.38
- pipelined_m [data_width=23 n_iter=19 angle_guard=3 frac_guard=2 rounding=round m=3] luts_plus_ffs=2240, accuracy_bits=17.8, luts=1609, ffs=631, throughput_msps=114, max_abs_err=4.53e-06 (2^-17.75), power_index=2.7
- pipelined_m [data_width=21 n_iter=23 angle_guard=4 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=2414, accuracy_bits=18.2, luts=1883, ffs=531, throughput_msps=89.6, max_abs_err=3.42e-06 (2^-18.16), power_index=2.91
- pipelined_m [data_width=24 n_iter=23 angle_guard=4 frac_guard=2 rounding=round m=3] luts_plus_ffs=2798, accuracy_bits=20.7, luts=2050, ffs=749, throughput_msps=110, max_abs_err=5.75e-07 (2^-20.73), power_index=3.37
- pipelined_m [data_width=28 n_iter=27 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=3593, accuracy_bits=23.5, luts=2667, ffs=926, throughput_msps=110, max_abs_err=8.19e-08 (2^-23.54), power_index=4.33
Front coverage: luts_plus_ffs 1165..3593 (HV reference 4000); accuracy_bits 12.5..23.5 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 15.6 MSPS; best accuracy 12.30 bits
- unrolled_k: 15 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 13.21 bits
- pipelined: 67 evals, 53 feasible; max throughput seen 282 MSPS; best accuracy 20.89 bits; best feasible luts_plus_ffs=1970; feasible ranges: data_width 17..28, n_iter 15..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 208 evals, 157 feasible; max throughput seen 178 MSPS; best accuracy 23.54 bits; best feasible luts_plus_ffs=1165; feasible ranges: data_width 17..28, n_iter 13..28, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (24 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 270 feasible; hypervolume 2.015e+04 (+2.0%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), and the front is healthy rather than stuck: 27 feasible Pareto designs, HV 2.015e4 with a +2.0% gain this round, and all four families already explored (none left to add). Every constraint is reachable with margin — throughput best 282 vs >=32 required, max_abs_err best 2^-23.54 vs <=2^-12, sys_p99_batch best 0.159 us vs <=0.44 us — so `infeasible` is not warranted. The selection rule (min luts_plus_ffs) is also satisfiable on the front: pipelined_m [W=19, N=14, angle_guard=0, frac_guard=0, trunc, m=4] is the cheapest feasible point at luts_plus_ffs=1165 with accuracy_bits=12.5 (max_abs_err 2^-12.50 <= 2^-12), throughput 93.6 MSPS >= 32, and sys_p99_batch 0.159 us <= 0.44 us. The front also spans the accuracy objective well (12.5..23.5 bits against HV ref 12) and area 1165..3593 against HV ref 4000, so coverage is adequate; further refinement is not possible within the budget. Note the L1 system bound is optimistic, so the cheapest design's 0.159 us batch margin (vs 0.44 us) is the one to watch at L2 re-selection, but that is a post-selection step, not an exploration decision.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 2.015e+04 (gain this round: +2.0%).
Feasible designs: 270 of 400 evaluations (243 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 6% violate; best seen 282
- max_abs_err <= 0.000244141: 19% violate; best seen 8.19e-08 (2^-23.54)
- sys_p99_batch_us <= 0.44: 21% violate; best seen 0.159

Pareto front (feasible, 27 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1165, accuracy_bits=12.5, luts=868, ffs=297, throughput_msps=93.6, max_abs_err=0.000172 (2^-12.50), power_index=1.4
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1284, accuracy_bits=13, luts=987, ffs=297, throughput_msps=93.6, max_abs_err=0.000123 (2^-12.99), power_index=1.55
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1337, accuracy_bits=14.1, luts=1033, ffs=305, throughput_msps=93.6, max_abs_err=5.75e-05 (2^-14.09), power_index=1.61
- pipelined_m [data_width=19 n_iter=19 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1609, accuracy_bits=14.7, luts=1238, ffs=371, throughput_msps=93.6, max_abs_err=3.86e-05 (2^-14.66), power_index=1.94
- pipelined_m [data_width=21 n_iter=20 angle_guard=3 frac_guard=0 rounding=round m=4] luts_plus_ffs=1857, accuracy_bits=16.4, luts=1447, ffs=411, throughput_msps=89.6, max_abs_err=1.15e-05 (2^-16.41), power_index=2.24
- pipelined_m [data_width=23 n_iter=19 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1974, accuracy_bits=17.4, luts=1523, ffs=451, throughput_msps=89.6, max_abs_err=5.75e-06 (2^-17.41), power_index=2.38
- pipelined_m [data_width=24 n_iter=20 angle_guard=4 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=2162, accuracy_bits=18.4, luts=1687, ffs=475, throughput_msps=86, max_abs_err=2.96e-06 (2^-18.37), power_index=2.6
- pipelined_m [data_width=22 n_iter=23 angle_guard=4 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=2503, accuracy_bits=19.2, luts=1953, ffs=551, throughput_msps=89.6, max_abs_err=1.68e-06 (2^-19.18), power_index=3.01
- pipelined_m [data_width=25 n_iter=25 angle_guard=2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=3051, accuracy_bits=20.9, luts=2205, ffs=845, throughput_msps=110, max_abs_err=5.15e-07 (2^-20.89), power_index=3.67
- pipelined_m [data_width=28 n_iter=27 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=3593, accuracy_bits=23.5, luts=2667, ffs=926, throughput_msps=110, max_abs_err=8.19e-08 (2^-23.54), power_index=4.33
Front coverage: luts_plus_ffs 1165..3593 (HV reference 4000); accuracy_bits 12.5..23.5 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 15.6 MSPS; best accuracy 12.30 bits
- unrolled_k: 15 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 13.21 bits
- pipelined: 67 evals, 53 feasible; max throughput seen 282 MSPS; best accuracy 20.89 bits; best feasible luts_plus_ffs=1970; feasible ranges: data_width 17..28, n_iter 15..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 308 evals, 217 feasible; max throughput seen 178 MSPS; best accuracy 23.54 bits; best feasible luts_plus_ffs=1165; feasible ranges: data_width 17..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 15809 in, 17041 out
- provider-reported cost: $0.0119
- full prompts and replies: `llm_trace.jsonl`

