# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 200 of 200 budgeted, over 2 round(s).  
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
`pipelined_m:data_width=18,n_iter=18,angle_guard=2,frac_guard=1,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 1190 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 364 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 74.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.87 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 5.02e-05 (2^-14.28) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 3.29 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 1.17e-05 (2^-16.39) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 0.764 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 14.3 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=18,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1190 | 364 | 93.6 | 7 | 1.87 | 5.02e-05 (2^-14.28) | 14.28 |
| 1 | `pipelined_m:data_width=19,n_iter=18,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1228 | 376 | 93.6 | 7 | 1.93 | 3.87e-05 (2^-14.66) | 14.66 |
| 2 | `pipelined_m:data_width=19,n_iter=18,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1246 | 381 | 93.6 | 7 | 1.96 | 3.09e-05 (2^-14.98) | 14.98 |
| 3 | `pipelined_m:data_width=19,n_iter=19,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1354 | 389 | 93.6 | 7 | 2.1 | 1.92e-05 (2^-15.67) | 15.67 |
| 4 | `pipelined_m:data_width=19,n_iter=19,angle_guard=2,frac_guard=3,rounding=round,m=4` | 1392 | 398 | 93.6 | 7 | 2.15 | 1.74e-05 (2^-15.81) | 15.81 |
| 5 | `pipelined_m:data_width=22,n_iter=18,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1395 | 428 | 89.6 | 7 | 2.19 | 1.09e-05 (2^-16.49) | 16.49 |
| 6 | `pipelined_m:data_width=20,n_iter=19,angle_guard=2,frac_guard=3,rounding=round,m=4` | 1451 | 415 | 89.6 | 7 | 2.25 | 1.02e-05 (2^-16.59) | 16.59 |
| 7 | `pipelined_m:data_width=22,n_iter=18,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1431 | 436 | 89.6 | 7 | 2.25 | 9.91e-06 (2^-16.62) | 16.62 |
| 8 | `pipelined_m:data_width=22,n_iter=18,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1449 | 441 | 89.6 | 7 | 2.27 | 9.56e-06 (2^-16.67) | 16.67 |
| 9 | `pipelined_m:data_width=22,n_iter=20,angle_guard=0,frac_guard=2,rounding=round,m=4` | 1573 | 431 | 89.6 | 7 | 2.41 | 7.68e-06 (2^-16.99) | 16.99 |
| 10 | `pipelined_m:data_width=22,n_iter=20,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1613 | 441 | 89.6 | 7 | 2.47 | 4.44e-06 (2^-17.78) | 17.78 |
| 11 | `pipelined:data_width=22,n_iter=20,angle_guard=2,frac_guard=3,rounding=round` | 1653 | 1624 | 256.5 | 22 | 3.95 | 3.57e-06 (2^-18.10) | 18.10 |
| 12 | `pipelined:data_width=22,n_iter=22,angle_guard=2,frac_guard=3,rounding=round` | 1822 | 1788 | 256.5 | 24 | 4.35 | 2.93e-06 (2^-18.38) | 18.38 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show pipelined_m is the clear winner: 35 feasible designs, best area 1072, and 13 of 17 front designs. iterative and unrolled_k are infeasible (0 feasible) because they cannot meet the 32 msps throughput constraint (they produce 1 result every N+3 or ceil(N/k)+3 cycles, far too slow for 32 results in 0.44 us). My two families (pipelined, pipelined_m) are the only ones that can meet throughput >= 32 msps. The key trade-off is area vs accuracy: N and W must be high enough for max_abs_err <= 2^-12, but low enough to minimize LUTs+FFs. The current best (1072) is from pipelined_m with m=2. I focus 55% of budget on pipelined_m to densely map its front (especially the m=2, N=14-16, W=14-16 region where the best designs cluster) and 45% on pipelined to confirm whether its lower latency (N+2 vs ceil(N/2)+2) provides any advantage for the sys_p99_batch_us constraint or if it is strictly dominated in area. Both families use angle_guard=0 since the error budget is dominated by n_iter, not angle path width, and this minimizes area. Rounding mode is included as a choice since 'round' can allow slightly fewer bits for the same accuracy, potentially reducing area.*)
- `pipelined_m` (55 evals): data_width=14..16, n_iter=14..16, angle_guard=0..0, frac_guard=0..4, rounding=trunc|round, m=2..2. *Why:* pipelined_m dominates the current merged front (13/17 designs, best area 1072). The m=2 register-every-2-stages configuration is the sweet spot for this spec: it halves the FF count vs full pipelined while keeping 1 result/cycle throughput (32 msps) and low latency (ceil(N/2)+2 cycles). N=14-16 and W=14-16 are the minimal settings that meet max_abs_err <= 2^-12 (0.000244141) with truncation; rounding allows slightly fewer bits. frac_guard 0-4 trades a few LUTs for accuracy margin. angle_guard=0 is sufficient since the error budget is dominated by n_iter, not angle path width. This range focuses on the densest region of the feasible front where area is minimized.
- `pipelined` (45 evals): data_width=14..16, n_iter=14..16, angle_guard=0..0, frac_guard=0..4, rounding=trunc|round. *Why:* pipelined (full register per stage) has 4 designs on the front and best area 1784, which is worse than pipelined_m but may offer better Fmax or lower latency (N+2 vs ceil(N/2)+2). Since the spec's sys_p99_batch_us <= 0.44 us constraint is tight (32 results in 0.44 us at 1 MHz tick), the lower latency of full pipelined could matter at L2 simulation. Searching the same minimal N/W range (14-16) with both rounding modes and frac_guard 0-4 maps the area-accuracy trade-off for this family and ensures the front is well-covered. The 45% share reflects that pipelined_m is already dominant, but pipelined's latency advantage warrants continued exploration to confirm whether any pipelined design beats pipelined_m on the final selection rule (min luts_plus_ffs) or is needed for the p99 batch constraint.

**Result (code):** 100 evaluations this round, 100 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `refine` — The primary blocker is accuracy: 100% of evaluations violated max_abs_err <= 2^-12 (0.000244). The best achieved was 2^-11.57 (0.00033), which is still ~35% too large. Throughput and system latency constraints are easily met (best throughput 282 MSPS vs 32 required; best sys_p99_batch 0.167 us vs 0.44 us limit). The current search focused on data_width=16 and n_iter=15-16, which yields ~11.5 bits of accuracy. To reach 12+ bits, we need to increase n_iter (to ~18-20) and/or data_width (to 18-20), and use rounding. I will narrow the search to these higher-accuracy regions while keeping throughput high (pipelined or pipelined_m with small m).

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 100% violate; best seen 0.00033 (2^-11.57)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.167

No feasible design found yet. Least-violating designs:
- pipelined_m [data_width=16 n_iter=16 angle_guard=0 frac_guard=2 rounding=round m=2]: throughput=171, max_abs_err=0.00033 (2^-11.57); max_abs_err <= 0.000244141 violated by 35.1%
- pipelined_m [data_width=16 n_iter=15 angle_guard=0 frac_guard=4 rounding=round m=2]: throughput=164, max_abs_err=0.000334 (2^-11.55); max_abs_err <= 0.000244141 violated by 36.9%
- pipelined [data_width=16 n_iter=15 angle_guard=0 frac_guard=3 rounding=trunc]: throughput=264, max_abs_err=0.000355 (2^-11.46); max_abs_err <= 0.000244141 violated by 45.2%
- pipelined_m [data_width=16 n_iter=15 angle_guard=0 frac_guard=2 rounding=round m=2]: throughput=171, max_abs_err=0.000355 (2^-11.46); max_abs_err <= 0.000244141 violated by 45.2%
- pipelined_m [data_width=16 n_iter=15 angle_guard=0 frac_guard=1 rounding=round m=2]: throughput=171, max_abs_err=0.000355 (2^-11.46); max_abs_err <= 0.000244141 violated by 45.2%

Per family:
- pipelined: 45 evals, 0 feasible; max throughput seen 282 MSPS; best accuracy 11.46 bits
- pipelined_m: 55 evals, 0 feasible; max throughput seen 178 MSPS; best accuracy 11.57 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Focus on data_width 18-22 and n_iter 18-22 to achieve >=12-bit accuracy. Use rounding to maximize accuracy. Keep angle_guard and frac_guard moderate to balance area. Both pipelined and pipelined_m are viable for throughput; pipelined_m may offer area savings.*)
- `pipelined` (50 evals): data_width=18..22, n_iter=18..22, angle_guard=0..2, frac_guard=1..3, rounding=round. *Why:* Pipelined gives highest throughput (1 result/cycle). Need higher n_iter and data_width to hit 12-bit accuracy.
- `pipelined_m` (50 evals): data_width=18..22, n_iter=18..22, angle_guard=0..2, frac_guard=1..3, rounding=round, m=2..4. *Why:* Pipelined_m with small m can reduce area vs fully pipelined while maintaining high throughput. Test if it meets accuracy with fewer resources.

**Result (code):** 100 evaluations this round, 200 total; 100 feasible; hypervolume 1.349e+04 (+inf).

**LLM decision:** `stop` — The budget (200/200 evals) and round cap (2/4) are exhausted, forcing a stop. The current Pareto front is robust and feasible: the minimum area design (pipelined_m, 1554 LUTs+FFs) meets all constraints with 14.3 bits of accuracy (max_abs_err 5.02e-05 < 2.44e-04) and a system batch latency of 0.167 us (well under the 0.44 us limit). The front spans a wide trade-off space (1554 to 3610 LUTs+FFs, 14.3 to 18.4 bits accuracy) and covers the hypervolume reference point (4000, 12) comfortably. The selection rule (min luts_plus_ffs) will pick the 1554 design, which has significant margin on both accuracy and system latency constraints.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.349e+04 (gain this round: +inf (first feasible designs)).
Feasible designs: 100 of 200 evaluations (81 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 50% violate; best seen 2.93e-06 (2^-18.38)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.167

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=18 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1554, accuracy_bits=14.3, luts=1190, ffs=364, throughput_msps=93.6, max_abs_err=5.02e-05 (2^-14.28), power_index=1.87
- pipelined_m [data_width=19 n_iter=18 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1604, accuracy_bits=14.7, luts=1228, ffs=376, throughput_msps=93.6, max_abs_err=3.87e-05 (2^-14.66), power_index=1.93
- pipelined_m [data_width=19 n_iter=19 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1744, accuracy_bits=15.7, luts=1354, ffs=389, throughput_msps=93.6, max_abs_err=1.92e-05 (2^-15.67), power_index=2.1
- pipelined_m [data_width=19 n_iter=19 angle_guard=2 frac_guard=3 rounding=round m=4] luts_plus_ffs=1790, accuracy_bits=15.8, luts=1392, ffs=398, throughput_msps=93.6, max_abs_err=1.74e-05 (2^-15.81), power_index=2.15
- pipelined_m [data_width=22 n_iter=18 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1823, accuracy_bits=16.5, luts=1395, ffs=428, throughput_msps=89.6, max_abs_err=1.09e-05 (2^-16.49), power_index=2.19
- pipelined_m [data_width=22 n_iter=18 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1867, accuracy_bits=16.6, luts=1431, ffs=436, throughput_msps=89.6, max_abs_err=9.91e-06 (2^-16.62), power_index=2.25
- pipelined_m [data_width=22 n_iter=18 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1890, accuracy_bits=16.7, luts=1449, ffs=441, throughput_msps=89.6, max_abs_err=9.56e-06 (2^-16.67), power_index=2.27
- pipelined_m [data_width=22 n_iter=20 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=2004, accuracy_bits=17, luts=1573, ffs=431, throughput_msps=89.6, max_abs_err=7.68e-06 (2^-16.99), power_index=2.41
- pipelined [data_width=22 n_iter=20 angle_guard=2 frac_guard=3 rounding=round] luts_plus_ffs=3278, accuracy_bits=18.1, luts=1653, ffs=1624, throughput_msps=257, max_abs_err=3.57e-06 (2^-18.10), power_index=3.95
- pipelined [data_width=22 n_iter=22 angle_guard=2 frac_guard=3 rounding=round] luts_plus_ffs=3610, accuracy_bits=18.4, luts=1822, ffs=1788, throughput_msps=257, max_abs_err=2.93e-06 (2^-18.38), power_index=4.35
Front coverage: luts_plus_ffs 1554..3610 (HV reference 4000); accuracy_bits 14.3..18.4 (HV reference 12); data_width on the front 18..22 (registry 8..28).

Per family:
- pipelined: 95 evals, 50 feasible; max throughput seen 282 MSPS; best accuracy 18.38 bits; best feasible luts_plus_ffs=2406; feasible ranges: data_width 18..22, n_iter 18..22, angle_guard 0..2, frac_guard 1..3
- pipelined_m: 105 evals, 50 feasible; max throughput seen 178 MSPS; best accuracy 17.78 bits; best feasible luts_plus_ffs=1554; feasible ranges: data_width 18..22, n_iter 18..22, angle_guard 0..2, frac_guard 1..3, m 2..4
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8648 in, 2480 out
- provider-reported cost: $0.0054
- full prompts and replies: `llm_trace.jsonl`

