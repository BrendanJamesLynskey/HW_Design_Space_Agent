# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 5 round(s).  
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
`pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=3` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 895 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 330 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 124 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 124 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 56.2 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.47 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00018 (2^-12.44) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 2.94 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 5.01e-05 (2^-14.29) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 0.82 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.4 | exact: bit-accurate model, exhaustive (65536 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 7 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 93.3 dBc, SNR 83.6 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=3` | 0.2973 → 0.3052 | yes |
| `pipelined_m:data_width=19,n_iter=14,angle_guard=3,frac_guard=0,rounding=round,m=3` | 0.3103 → 0.3186 | yes |
| `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=3,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=16,angle_guard=3,frac_guard=1,rounding=round,m=2` | 0.2433 → 0.2494 | yes |
| `pipelined_m:data_width=25,n_iter=16,angle_guard=-2,frac_guard=4,rounding=round,m=4` | 0.4185 → 0.43 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (17 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=3` | 895 | 330 | 124.5 | 7 | 1.47 | 0.00018 (2^-12.44) | 12.44 |
| 1 | `pipelined_m:data_width=19,n_iter=14,angle_guard=3,frac_guard=0,rounding=round,m=3` | 909 | 376 | 119.3 | 7 | 1.55 | 0.00014 (2^-12.80) | 12.80 |
| 2 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=3,rounding=trunc,m=4` | 1064 | 305 | 93.6 | 6 | 1.65 | 7.75e-05 (2^-13.65) | 13.65 |
| 3 | `pipelined_m:data_width=18,n_iter=16,angle_guard=3,frac_guard=1,rounding=round,m=2` | 1071 | 569 | 164.4 | 10 | 1.97 | 6.51e-05 (2^-13.91) | 13.91 |
| 4 | `pipelined_m:data_width=25,n_iter=16,angle_guard=-2,frac_guard=4,rounding=round,m=4` | 1433 | 400 | 86.0 | 6 | 2.21 | 3.14e-05 (2^-14.96) | 14.96 |
| 5 | `pipelined_m:data_width=20,n_iter=20,angle_guard=2,frac_guard=1,rounding=trunc,m=3` | 1407 | 540 | 119.3 | 9 | 2.34 | 2.4e-05 (2^-15.35) | 15.35 |
| 6 | `pipelined_m:data_width=20,n_iter=18,angle_guard=4,frac_guard=4,rounding=round,m=3` | 1445 | 513 | 114.5 | 8 | 2.36 | 1.06e-05 (2^-16.52) | 16.52 |
| 7 | `pipelined_m:data_width=25,n_iter=19,angle_guard=-2,frac_guard=1,rounding=trunc,m=4` | 1542 | 462 | 89.6 | 7 | 2.41 | 5.98e-06 (2^-17.35) | 17.35 |
| 8 | `pipelined_m:data_width=25,n_iter=19,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 1618 | 482 | 86.0 | 7 | 2.53 | 4.2e-06 (2^-17.86) | 17.86 |
| 9 | `pipelined_m:data_width=25,n_iter=20,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1727 | 487 | 86.0 | 7 | 2.67 | 2.31e-06 (2^-18.72) | 18.72 |
| 10 | `pipelined_m:data_width=25,n_iter=20,angle_guard=3,frac_guard=1,rounding=round,m=3` | 1780 | 665 | 110.0 | 9 | 2.94 | 2.14e-06 (2^-18.83) | 18.83 |
| 11 | `pipelined_m:data_width=28,n_iter=20,angle_guard=0,frac_guard=2,rounding=round,m=3` | 1946 | 725 | 110.0 | 9 | 3.22 | 1.97e-06 (2^-18.95) | 18.95 |
| 12 | `pipelined_m:data_width=26,n_iter=22,angle_guard=3,frac_guard=0,rounding=round,m=3` | 1930 | 763 | 110.0 | 10 | 3.24 | 6.69e-07 (2^-20.51) | 20.51 |
| 13 | `pipelined_m:data_width=24,n_iter=25,angle_guard=2,frac_guard=4,rounding=round,m=3` | 2281 | 851 | 110.0 | 11 | 3.77 | 6.05e-07 (2^-20.66) | 20.66 |
| 14 | `pipelined_m:data_width=26,n_iter=25,angle_guard=2,frac_guard=4,rounding=trunc,m=3` | 2383 | 907 | 110.0 | 11 | 3.96 | 2.1e-07 (2^-22.18) | 22.18 |
| 15 | `pipelined_m:data_width=27,n_iter=25,angle_guard=2,frac_guard=4,rounding=round,m=3` | 2515 | 938 | 105.9 | 11 | 4.16 | 1.1e-07 (2^-23.12) | 23.12 |
| 16 | `pipelined_m:data_width=28,n_iter=26,angle_guard=2,frac_guard=4,rounding=round,m=2` | 2699 | 1375 | 147.4 | 15 | 4.9 | 6.35e-08 (2^-23.91) | 23.91 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 simultaneous results within 0.44us per 1us tick, which is a tight batch latency constraint. Pipelined_m is the most promising family because it can achieve high throughput (1 result/cycle) with reduced latency via m-stage grouping, and it allows trading off area (fewer registers) against latency. I allocate 50% of the budget to pipelined_m to thoroughly explore the m and n_iter trade-offs. Pipelined (m=1) gets 30% as a baseline to confirm it's likely too slow for the batch constraint but may have lower area. Unrolled_k gets 20% to check if higher k values can meet the latency constraint with acceptable area. I exclude iterative because it's too slow (N+3 cycles per result, no parallelism) and cannot meet the 32 results in 0.44us constraint. Data width is constrained to 14-16 to meet the 12-bit accuracy requirement (max_abs_err <= 2^-12) while minimizing area. Angle and frac guards are kept small (0-2) to reduce area while maintaining accuracy.*)
- `pipelined_m` (50 evals): data_width=14..16, n_iter=14..20, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Primary candidate. The system issues 32 requests per 1us tick and requires all results within 0.44us. A pipelined_m unit with m=2 or m=4 can process multiple micro-rotations per cycle, reducing latency and increasing effective throughput. With n_iter=14-20, we can achieve the required 12-bit accuracy while keeping area reasonable. The m parameter allows trading off latency (ceil(N/m)+2) against area (fewer registers). This family offers the best balance of throughput, latency, and area for bursty 32-request workloads.
- `pipelined` (30 evals): data_width=14..16, n_iter=14..20, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Baseline comparison. Fully pipelined (m=1) gives 1 result/cycle and N+2 latency. With n_iter=14-20, latency is 16-22 cycles. At Fmax ~200-300 MHz, this is 53-110 ns per result, so 32 results take 1.7-3.5 us, which likely violates the 0.44us batch constraint. However, it may have lower area than pipelined_m with small m, so it's worth exploring to map the area-latency trade-off and confirm whether pipelined_m is strictly better for this spec.
- `unrolled_k` (20 evals): data_width=14..16, n_iter=14..20, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=4..8. *Why:* Secondary candidate. Unrolled_k with k=4-8 processes k micro-rotations per cycle, giving ceil(N/k)+3 cycles per result. With N=14-20 and k=4-8, this is 5-8 cycles per result. At Fmax ~200-300 MHz, 32 results take 1.1-1.6 us, which likely violates the 0.44us constraint. However, it may have lower area than pipelined_m for some configurations, so it's worth a small budget share to confirm it's not competitive for this bursty workload.

**Result (code):** 100 evaluations this round, 100 total; 9 feasible; hypervolume 2183 (n/a).

**LLM decision:** `refine` — The current front is narrow (1225-1515 area, 12.4-12.8 bits). pipelined_m dominates with 8 feasible points vs 1 for pipelined. unrolled_k is infeasible (max throughput 8.32 < 32). iterative is unexplored but likely infeasible for throughput (1 result/cycle max, but latency N+3 cycles; for N=15, 18 cycles/result = ~5.5 MSPS at 100MHz, far below 32 MSPS requirement). The key trade-off is area vs accuracy. The best area design (1225) has 12.4 bits accuracy, which is close to the 12-bit constraint. I want to see if we can get below 1225 area by relaxing frac_guard to 0 or using m=2 in pipelined_m, or if pipelined with frac_guard=1 can beat 1225. The accuracy constraint is max_abs_err <= 2^-12, so we have some headroom (12.4 bits > 12 bits). Throughput constraint is >= 32 MSPS, and both families easily exceed this (97-124 MSPS). sys_p99_batch_us <= 0.44 is also met (0.172 best seen). So the binding constraint is area, with accuracy as a secondary objective. Refining around the current best points should reveal if there are cheaper designs.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 2183 (gain this round: n/a (first round)).
Feasible designs: 9 of 100 evaluations (7 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 20% violate; best seen 273
- max_abs_err <= 0.000244141: 91% violate; best seen 0.000138 (2^-12.83)
- sys_p99_batch_us <= 0.44: 20% violate; best seen 0.172

Pareto front (feasible, 2 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=1225, accuracy_bits=12.4, luts=895, ffs=330, throughput_msps=124, max_abs_err=0.00018 (2^-12.44), power_index=1.47
- pipelined_m [data_width=16 n_iter=19 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1515, accuracy_bits=12.8, luts=1177, ffs=338, throughput_msps=97.8, max_abs_err=0.000138 (2^-12.83), power_index=1.82
Front coverage: luts_plus_ffs 1225..1515 (HV reference 4000); accuracy_bits 12.4..12.8 (HV reference 12); data_width on the front 16..16 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 8.32 MSPS; best accuracy 11.59 bits
- pipelined: 30 evals, 1 feasible; max throughput seen 273 MSPS; best accuracy 12.02 bits; best feasible luts_plus_ffs=1806; feasible ranges: data_width 16..16, n_iter 15..15, angle_guard 2..2, frac_guard 2..2
- pipelined_m: 50 evals, 8 feasible; max throughput seen 171 MSPS; best accuracy 12.83 bits; best feasible luts_plus_ffs=1225; feasible ranges: data_width 16..16, n_iter 14..20, angle_guard 1..2, frac_guard 1..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The current front is narrow (1225-1515 area, 12.4-12.8 bits). pipelined_m dominates with 8 feasible points vs 1 for pipelined. unrolled_k is infeasible (max throughput 8.32 < 32). iterative is unexplored but likely infeasible for throughput (1 result/cycle max, but latency N+3 cycles; for N=15, 18 cycles/result = ~5.5 MSPS at 100MHz, far below 32 MSPS requirement). The key trade-off is area vs accuracy. The best area design (1225) has 12.4 bits accuracy, which is close to the 12-bit constraint. I want to see if we can get below 1225 area by relaxing frac_guard to 0 or using m=2 in pipelined_m, or if pipelined with frac_guard=1 can beat 1225. The accuracy constraint is max_abs_err <= 2^-12, so we have some headroom (12.4 bits > 12 bits). Throughput constraint is >= 32 MSPS, and both families easily exceed this (97-124 MSPS). sys_p99_batch_us <= 0.44 is also met (0.172 best seen). So the binding constraint is area, with accuracy as a secondary objective. Refining around the current best points should reveal if there are cheaper designs.*)
- `pipelined_m` (50 evals): data_width=16..16, n_iter=15..15, angle_guard=2..2, frac_guard=0..1, rounding=trunc|round, m=2..3. *Why:* Tighten around the current best feasible point (1225 area, 12.4 bits) to probe if m=2 or frac_guard=0 can drop area further while keeping throughput >= 32 and sys_p99_batch <= 0.44.
- `pipelined` (50 evals): data_width=16..16, n_iter=15..15, angle_guard=2..2, frac_guard=1..2, rounding=trunc|round. *Why:* pipelined had 1 feasible point at 1806 area. Check if reducing frac_guard to 1 (from 2) reduces area below the pipelined_m best of 1225, or if it violates accuracy/throughput.

**Result (code):** 100 evaluations this round, 200 total; 75 feasible; hypervolume 2183 (+0.0%).

**LLM decision:** `map_front` — The front is dominated by pipelined_m (1225, 1515) and pipelined (1786), but the hypervolume gain this round was 0.0% and the front covers only a narrow slice of the objective space (luts_plus_ffs 1225..1515, accuracy 12.4..12.8 bits, data_width stuck at 16). The accuracy constraint (max_abs_err <= 2^-12) is the binding one: 62% of evaluations violate it, and pipelined_m's best feasible accuracy is 12.83 bits while pipelined's is 12.48 bits. The throughput and sys_p99_batch constraints are easily met by the pipelined families (best seen 273 MSPS, 0.172 us), so the trade-off is purely between area and accuracy. Since the front covers only a small part of the accuracy range and the area range, and the two families on the front have overlapping but distinct feasible regions (pipelined_m: n_iter 14..20, m 2..4; pipelined: n_iter 15, m fixed), a code-driven NSGA-II coverage search over the full parameter ranges of these two families, seeded with the current front, is the right move to map the whole trade-off curve and maximize hypervolume before the final selection. The iterative family is not yet explored, but its throughput (1 result every N+3 cycles) makes it unlikely to meet the 32 MSPS throughput constraint for reasonable N, and unrolled_k already failed to meet throughput (max 8.32 MSPS), so adding iterative is low priority. The remaining 200 evaluations should be spent mapping the front over pipelined and pipelined_m.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 2183 (gain this round: +0.0%).
Feasible designs: 75 of 200 evaluations (10 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 10% violate; best seen 273
- max_abs_err <= 0.000244141: 62% violate; best seen 0.000138 (2^-12.83)
- sys_p99_batch_us <= 0.44: 10% violate; best seen 0.172

Pareto front (feasible, 2 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=1225, accuracy_bits=12.4, luts=895, ffs=330, throughput_msps=124, max_abs_err=0.00018 (2^-12.44), power_index=1.47
- pipelined_m [data_width=16 n_iter=19 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1515, accuracy_bits=12.8, luts=1177, ffs=338, throughput_msps=97.8, max_abs_err=0.000138 (2^-12.83), power_index=1.82
Front coverage: luts_plus_ffs 1225..1515 (HV reference 4000); accuracy_bits 12.4..12.8 (HV reference 12); data_width on the front 16..16 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 8.32 MSPS; best accuracy 11.59 bits
- pipelined: 80 evals, 45 feasible; max throughput seen 273 MSPS; best accuracy 12.48 bits; best feasible luts_plus_ffs=1786; feasible ranges: data_width 16..16, n_iter 15..15, angle_guard 2..2, frac_guard 1..2
- pipelined_m: 100 evals, 30 feasible; max throughput seen 171 MSPS; best accuracy 12.83 bits; best feasible luts_plus_ffs=1225; feasible ranges: data_width 16..16, n_iter 14..20, angle_guard 1..2, frac_guard 1..2, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=15..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 240 total; 102 feasible; hypervolume 1.59e+04 (+628.1%).

**LLM decision:** `map_front` — The Pareto front is dominated by `pipelined_m` designs, which have successfully mapped the trade-off from the minimum area corner (1225 LUTs+FFs, 12.4 bits) to the high-accuracy corner (3506 LUTs+FFs, 20.9 bits). The `pipelined` family is strictly dominated by `pipelined_m` (best feasible area 1786 vs 1225, and lower max throughput). `unrolled_k` is infeasible for the throughput constraint (max 8.32 MSPS < 32 MSPS). The `iterative` family is also infeasible for throughput (1 result/cycle at ~100-200 MHz yields < 200 MSPS, but the latency/throughput trade-off for a 32-burst in 0.44us requires high throughput which iterative cannot provide efficiently compared to pipelined_m; specifically, iterative takes N+3 cycles, so for N=15 it takes 18 cycles. At 100MHz, 18 cycles = 180ns. 32 requests * 180ns = 5.76us >> 0.44us. Thus iterative is infeasible for the system constraint). Since `pipelined_m` is the only viable family and the front already spans a wide range of both objectives, the remaining budget (160 evals) should be used to densely map the `pipelined_m` front to ensure no gaps in the trade-off curve, maximizing hypervolume.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 1.59e+04 (gain this round: +628.1%).
Feasible designs: 102 of 240 evaluations (34 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 8% violate; best seen 273
- max_abs_err <= 0.000244141: 54% violate; best seen 5.15e-07 (2^-20.89)
- sys_p99_batch_us <= 0.44: 12% violate; best seen 0.172

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=1225, accuracy_bits=12.4, luts=895, ffs=330, throughput_msps=124, max_abs_err=0.00018 (2^-12.44), power_index=1.47
- pipelined_m [data_width=16 n_iter=19 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1515, accuracy_bits=12.8, luts=1177, ffs=338, throughput_msps=97.8, max_abs_err=0.000138 (2^-12.83), power_index=1.82
- pipelined_m [data_width=18 n_iter=20 angle_guard=3 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1674, accuracy_bits=13.5, luts=1307, ffs=367, throughput_msps=93.6, max_abs_err=8.72e-05 (2^-13.49), power_index=2.01
- pipelined_m [data_width=25 n_iter=19 angle_guard=-2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=2004, accuracy_bits=17.4, luts=1542, ffs=462, throughput_msps=89.6, max_abs_err=5.98e-06 (2^-17.35), power_index=2.41
- pipelined_m [data_width=25 n_iter=19 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=2100, accuracy_bits=17.9, luts=1618, ffs=482, throughput_msps=86, max_abs_err=4.2e-06 (2^-17.86), power_index=2.53
- pipelined_m [data_width=25 n_iter=20 angle_guard=3 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=2214, accuracy_bits=18.7, luts=1727, ffs=487, throughput_msps=86, max_abs_err=2.31e-06 (2^-18.72), power_index=2.67
- pipelined_m [data_width=25 n_iter=20 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=2445, accuracy_bits=18.8, luts=1780, ffs=665, throughput_msps=110, max_abs_err=2.14e-06 (2^-18.83), power_index=2.94
- pipelined_m [data_width=28 n_iter=20 angle_guard=0 frac_guard=2 rounding=round m=3] luts_plus_ffs=2672, accuracy_bits=19, luts=1946, ffs=725, throughput_msps=110, max_abs_err=1.97e-06 (2^-18.95), power_index=3.22
- pipelined_m [data_width=28 n_iter=21 angle_guard=3 frac_guard=2 rounding=round m=3] luts_plus_ffs=2855, accuracy_bits=20, luts=2109, ffs=747, throughput_msps=106, max_abs_err=9.64e-07 (2^-19.98), power_index=3.44
- pipelined_m [data_width=25 n_iter=29 angle_guard=2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=3506, accuracy_bits=20.9, luts=2572, ffs=934, throughput_msps=110, max_abs_err=5.15e-07 (2^-20.89), power_index=4.22
Front coverage: luts_plus_ffs 1225..3506 (HV reference 4000); accuracy_bits 12.4..20.9 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 8.32 MSPS; best accuracy 11.59 bits
- pipelined: 80 evals, 45 feasible; max throughput seen 273 MSPS; best accuracy 12.48 bits; best feasible luts_plus_ffs=1786; feasible ranges: data_width 16..16, n_iter 15..15, angle_guard 2..2, frac_guard 1..2
- pipelined_m: 140 evals, 57 feasible; max throughput seen 171 MSPS; best accuracy 20.89 bits; best feasible luts_plus_ffs=1225; feasible ranges: data_width 16..28, n_iter 13..29, angle_guard -2..3, frac_guard 0..3, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=15..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (10 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 340 total; 172 feasible; hypervolume 1.877e+04 (+18.1%).

**LLM decision:** `stop` — The exploration has successfully mapped a robust Pareto front for the `pipelined_m` family that satisfies all constraints. The front spans a wide range of area (1225 to 4074 LUTs+FFs) and accuracy (12.4 to 23.9 bits), ensuring good hypervolume coverage. The minimum area feasible design (1225 LUTs+FFs) meets the throughput (124 MSPS >= 32) and accuracy (12.4 bits >= 12) requirements. Since this is the final round and the front is well-established with no unexplored promising families (iterative is too slow for the throughput constraint, unrolled_k failed to meet throughput), stopping is the correct action to finalize the selection.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 60 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 340 of 400.
Hypervolume of the feasible front: 1.877e+04 (gain this round: +18.1%).
Feasible designs: 172 of 340 evaluations (101 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 6% violate; best seen 273
- max_abs_err <= 0.000244141: 41% violate; best seen 6.35e-08 (2^-23.91)
- sys_p99_batch_us <= 0.44: 17% violate; best seen 0.172

Pareto front (feasible, 16 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=1225, accuracy_bits=12.4, luts=895, ffs=330, throughput_msps=124, max_abs_err=0.00018 (2^-12.44), power_index=1.47
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1369, accuracy_bits=13.7, luts=1064, ffs=305, throughput_msps=93.6, max_abs_err=7.75e-05 (2^-13.65), power_index=1.65
- pipelined_m [data_width=18 n_iter=16 angle_guard=3 frac_guard=1 rounding=round m=2] luts_plus_ffs=1640, accuracy_bits=13.9, luts=1071, ffs=569, throughput_msps=164, max_abs_err=6.51e-05 (2^-13.91), power_index=1.97
- pipelined_m [data_width=20 n_iter=18 angle_guard=4 frac_guard=4 rounding=round m=3] luts_plus_ffs=1957, accuracy_bits=16.5, luts=1445, ffs=513, throughput_msps=114, max_abs_err=1.06e-05 (2^-16.52), power_index=2.36
- pipelined_m [data_width=25 n_iter=19 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=2100, accuracy_bits=17.9, luts=1618, ffs=482, throughput_msps=86, max_abs_err=4.2e-06 (2^-17.86), power_index=2.53
- pipelined_m [data_width=25 n_iter=20 angle_guard=3 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=2214, accuracy_bits=18.7, luts=1727, ffs=487, throughput_msps=86, max_abs_err=2.31e-06 (2^-18.72), power_index=2.67
- pipelined_m [data_width=28 n_iter=20 angle_guard=0 frac_guard=2 rounding=round m=3] luts_plus_ffs=2672, accuracy_bits=19, luts=1946, ffs=725, throughput_msps=110, max_abs_err=1.97e-06 (2^-18.95), power_index=3.22
- pipelined_m [data_width=24 n_iter=25 angle_guard=2 frac_guard=4 rounding=round m=3] luts_plus_ffs=3132, accuracy_bits=20.7, luts=2281, ffs=851, throughput_msps=110, max_abs_err=6.05e-07 (2^-20.66), power_index=3.77
- pipelined_m [data_width=26 n_iter=25 angle_guard=2 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=3290, accuracy_bits=22.2, luts=2383, ffs=907, throughput_msps=110, max_abs_err=2.1e-07 (2^-22.18), power_index=3.96
- pipelined_m [data_width=28 n_iter=26 angle_guard=2 frac_guard=4 rounding=round m=2] luts_plus_ffs=4074, accuracy_bits=23.9, luts=2699, ffs=1375, throughput_msps=147, max_abs_err=6.35e-08 (2^-23.91), power_index=4.9
Front coverage: luts_plus_ffs 1225..4074 (HV reference 4000); accuracy_bits 12.4..23.9 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 8.32 MSPS; best accuracy 11.59 bits
- pipelined: 80 evals, 45 feasible; max throughput seen 273 MSPS; best accuracy 12.48 bits; best feasible luts_plus_ffs=1786; feasible ranges: data_width 16..16, n_iter 15..15, angle_guard 2..2, frac_guard 1..2
- pipelined_m: 240 evals, 127 feasible; max throughput seen 171 MSPS; best accuracy 23.91 bits; best feasible luts_plus_ffs=1225; feasible ranges: data_width 15..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 5

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 60 evaluations*)
- `pipelined_m` (60 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (16 front designs; box front_anchored)

**Result (code):** 60 evaluations this round, 400 total; 208 feasible; hypervolume 1.877e+04 (+0.0%).

**No LLM call** (code's front-mapping round): The exploration has successfully mapped a robust Pareto front for the `pipelined_m` family that satisfies all constraints. The front spans a wide range of area (1225 to 4074 LUTs+FFs) and accuracy (12.4 to 23.9 bits), ensuring good hypervolume coverage. The minimum area feasible design (1225 LUTs+FFs) meets the throughput (124 MSPS >= 32) and accuracy (12.4 bits >= 12) requirements. Since this is the final round and the front is well-established with no unexplored promising families (iterative is too slow for the throughput constraint, unrolled_k failed to meet throughput), stopping is the correct action to finalize the selection.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 5 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.877e+04 (gain this round: +0.0%).
Feasible designs: 208 of 400 evaluations (133 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 5% violate; best seen 273
- max_abs_err <= 0.000244141: 38% violate; best seen 6.35e-08 (2^-23.91)
- sys_p99_batch_us <= 0.44: 18% violate; best seen 0.172

Pareto front (feasible, 17 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=1225, accuracy_bits=12.4, luts=895, ffs=330, throughput_msps=124, max_abs_err=0.00018 (2^-12.44), power_index=1.47
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1369, accuracy_bits=13.7, luts=1064, ffs=305, throughput_msps=93.6, max_abs_err=7.75e-05 (2^-13.65), power_index=1.65
- pipelined_m [data_width=25 n_iter=16 angle_guard=-2 frac_guard=4 rounding=round m=4] luts_plus_ffs=1833, accuracy_bits=15, luts=1433, ffs=400, throughput_msps=86, max_abs_err=3.14e-05 (2^-14.96), power_index=2.21
- pipelined_m [data_width=20 n_iter=20 angle_guard=2 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1947, accuracy_bits=15.3, luts=1407, ffs=540, throughput_msps=119, max_abs_err=2.4e-05 (2^-15.35), power_index=2.34
- pipelined_m [data_width=25 n_iter=19 angle_guard=-2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=2004, accuracy_bits=17.4, luts=1542, ffs=462, throughput_msps=89.6, max_abs_err=5.98e-06 (2^-17.35), power_index=2.41
- pipelined_m [data_width=25 n_iter=20 angle_guard=3 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=2214, accuracy_bits=18.7, luts=1727, ffs=487, throughput_msps=86, max_abs_err=2.31e-06 (2^-18.72), power_index=2.67
- pipelined_m [data_width=28 n_iter=20 angle_guard=0 frac_guard=2 rounding=round m=3] luts_plus_ffs=2672, accuracy_bits=19, luts=1946, ffs=725, throughput_msps=110, max_abs_err=1.97e-06 (2^-18.95), power_index=3.22
- pipelined_m [data_width=26 n_iter=22 angle_guard=3 frac_guard=0 rounding=round m=3] luts_plus_ffs=2693, accuracy_bits=20.5, luts=1930, ffs=763, throughput_msps=110, max_abs_err=6.69e-07 (2^-20.51), power_index=3.24
- pipelined_m [data_width=26 n_iter=25 angle_guard=2 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=3290, accuracy_bits=22.2, luts=2383, ffs=907, throughput_msps=110, max_abs_err=2.1e-07 (2^-22.18), power_index=3.96
- pipelined_m [data_width=28 n_iter=26 angle_guard=2 frac_guard=4 rounding=round m=2] luts_plus_ffs=4074, accuracy_bits=23.9, luts=2699, ffs=1375, throughput_msps=147, max_abs_err=6.35e-08 (2^-23.91), power_index=4.9
Front coverage: luts_plus_ffs 1225..4074 (HV reference 4000); accuracy_bits 12.4..23.9 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 8.32 MSPS; best accuracy 11.59 bits
- pipelined: 80 evals, 45 feasible; max throughput seen 273 MSPS; best accuracy 12.48 bits; best feasible luts_plus_ffs=1786; feasible ranges: data_width 16..16, n_iter 15..15, angle_guard 2..2, frac_guard 1..2
- pipelined_m: 300 evals, 163 feasible; max throughput seen 171 MSPS; best accuracy 23.91 bits; best feasible luts_plus_ffs=1225; feasible ranges: data_width 15..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 29606 in, 4248 out
- provider-reported cost: $0.0084
- full prompts and replies: `llm_trace.jsonl`

