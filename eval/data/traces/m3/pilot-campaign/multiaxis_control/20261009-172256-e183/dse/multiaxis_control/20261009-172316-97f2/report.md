# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
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
`pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 868 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 293 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000172 (2^-12.50) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 11.3 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.26e-05 (2^-14.21) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.45 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 5 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 95.0 dBc, SNR 82.3 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=5` | 0.4342 → 0.4465 | no |
| `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=2,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=19,n_iter=15,angle_guard=-1,frac_guard=1,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |

**WINNER CHANGED AT L2**: the L1 selection pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=5 fails the simulated system constraints (sys_p99_batch_us <= 0.44 by 1.5%); the best shortlisted design that passes is pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,m=4.

## Pareto front (25 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=5` | 863 | 219 | 80.6 | 5 | 1.3 | 0.000192 (2^-12.35) | 12.35 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 868 | 293 | 93.6 | 6 | 1.4 | 0.000172 (2^-12.50) | 12.50 |
| 2 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=2,rounding=round,m=4` | 934 | 301 | 93.6 | 6 | 1.49 | 0.000157 (2^-12.64) | 12.64 |
| 3 | `pipelined_m:data_width=19,n_iter=15,angle_guard=-1,frac_guard=1,rounding=trunc,m=4` | 949 | 299 | 93.6 | 6 | 1.5 | 0.000129 (2^-12.92) | 12.92 |
| 4 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 1001 | 293 | 93.6 | 6 | 1.56 | 0.000104 (2^-13.23) | 13.23 |
| 5 | `pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=2,rounding=round,m=4` | 1055 | 297 | 93.6 | 6 | 1.63 | 0.000102 (2^-13.25) | 13.25 |
| 6 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1071 | 301 | 93.6 | 6 | 1.65 | 7.47e-05 (2^-13.71) | 13.71 |
| 7 | `pipelined_m:data_width=21,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1112 | 337 | 93.6 | 6 | 1.74 | 6.53e-05 (2^-13.90) | 13.90 |
| 8 | `pipelined_m:data_width=23,n_iter=15,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1185 | 371 | 89.6 | 6 | 1.87 | 6.2e-05 (2^-13.98) | 13.98 |
| 9 | `pipelined_m:data_width=26,n_iter=15,angle_guard=1,frac_guard=0,rounding=trunc,m=4` | 1259 | 400 | 86.0 | 6 | 2 | 6.12e-05 (2^-14.00) | 14.00 |
| 10 | `pipelined_m:data_width=28,n_iter=15,angle_guard=-1,frac_guard=1,rounding=trunc,m=4` | 1348 | 426 | 86.0 | 6 | 2.13 | 6.11e-05 (2^-14.00) | 14.00 |
| 11 | `pipelined_m:data_width=22,n_iter=18,angle_guard=3,frac_guard=0,rounding=round,m=4` | 1349 | 428 | 89.6 | 7 | 2.14 | 1.1e-05 (2^-16.47) | 16.47 |
| 12 | `pipelined_m:data_width=24,n_iter=18,angle_guard=-1,frac_guard=1,rounding=trunc,m=3` | 1420 | 531 | 114.5 | 8 | 2.35 | 9.83e-06 (2^-16.63) | 16.63 |
| 13 | `pipelined_m:data_width=22,n_iter=20,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1547 | 434 | 89.6 | 7 | 2.38 | 5.54e-06 (2^-17.46) | 17.46 |
| 14 | `pipelined_m:data_width=21,n_iter=21,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1630 | 500 | 89.6 | 8 | 2.56 | 5.47e-06 (2^-17.48) | 17.48 |
| 15 | `pipelined_m:data_width=22,n_iter=21,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1632 | 504 | 89.6 | 8 | 2.57 | 4.62e-06 (2^-17.72) | 17.72 |
| 16 | `pipelined_m:data_width=23,n_iter=21,angle_guard=1,frac_guard=1,rounding=trunc,m=3` | 1649 | 602 | 114.5 | 9 | 2.71 | 3.47e-06 (2^-18.14) | 18.14 |
| 17 | `pipelined_m:data_width=23,n_iter=23,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 1860 | 698 | 114.5 | 10 | 3.08 | 2.86e-06 (2^-18.42) | 18.42 |
| 18 | `pipelined_m:data_width=25,n_iter=22,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 1908 | 751 | 110.0 | 10 | 3.2 | 1e-06 (2^-19.93) | 19.93 |
| 19 | `pipelined_m:data_width=24,n_iter=23,angle_guard=3,frac_guard=2,rounding=round,m=3` | 2026 | 741 | 110.0 | 10 | 3.33 | 5.75e-07 (2^-20.73) | 20.73 |
| 20 | `pipelined_m:data_width=24,n_iter=24,angle_guard=3,frac_guard=3,rounding=round,m=3` | 2164 | 755 | 110.0 | 10 | 3.51 | 4.66e-07 (2^-21.03) | 21.03 |
| 21 | `pipelined_m:data_width=28,n_iter=23,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 2208 | 829 | 105.9 | 10 | 3.66 | 3.01e-07 (2^-21.66) | 21.66 |
| 22 | `pipelined_m:data_width=27,n_iter=24,angle_guard=4,frac_guard=2,rounding=round,m=3` | 2365 | 827 | 105.9 | 10 | 3.84 | 1.63e-07 (2^-22.55) | 22.55 |
| 23 | `pipelined_m:data_width=28,n_iter=24,angle_guard=3,frac_guard=3,rounding=trunc,m=3` | 2405 | 858 | 105.9 | 10 | 3.93 | 1.45e-07 (2^-22.72) | 22.72 |
| 24 | `pipelined_m:data_width=28,n_iter=28,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 2708 | 1023 | 105.9 | 12 | 4.49 | 1e-07 (2^-23.25) | 23.25 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 Msps sustained throughput (32 requests per 1 us tick) and all 32 results back within 440 ns p99. This rules out iterative (1 result per N+3 cycles, far too slow) and makes unrolled_k marginal (needs high Fmax or large k). The pipelined and pipelined_m families are the primary candidates: both give 1 result/cycle, so throughput = Fmax in Msps. At Fmax >= 32 MHz they meet throughput; at Fmax >= ~100 MHz they meet the 440 ns latency constraint comfortably (latency ~10-20 cycles = 100-200 ns). Accuracy requires max_abs_err <= 2^-12 = 0.000244, which corresponds to accuracy_bits >= 12. For CORDIC, n_iter=12-16 with data_width=14-18 and appropriate guards should achieve this. The area objective (min luts_plus_ffs) favors pipelined_m (fewer FFs) over pipelined, and smaller data_width/n_iter. I allocate 45% to pipelined (baseline, most likely to be on the front), 35% to pipelined_m (FF savings), and 20% to unrolled_k (to check if it can compete). Ranges are kept tight around the accuracy/throughput sweet spot to maximize the chance of finding feasible designs within the 400-eval budget. angle_guard -2..0 keeps the atan-LUT small; frac_guard 0..2 provides margin without excessive width.*)
- `pipelined` (45 evals): data_width=14..18, n_iter=12..16, angle_guard=-2..0, frac_guard=0..2, rounding=trunc|round. *Why:* Pipelined gives 1 result/cycle, so at Fmax >= 32 MHz it meets the 32 Msps throughput constraint. Latency is N+2 cycles; with N=12-16 and Fmax ~100-150 MHz, latency is ~14-18 cycles = ~93-180 ns, well under 440 ns. This is the most area-efficient family for sustained 32 Msps. data_width 14-18 with n_iter 12-16 should give accuracy_bits >= 12 (max_abs_err <= 2^-12). angle_guard -2..0 keeps the atan-LUT small; frac_guard 0..2 adds margin. Rounding explored to find the cheapest that meets error.
- `pipelined_m` (35 evals): data_width=14..18, n_iter=12..16, angle_guard=-2..0, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m registers every m stages, reducing FF count vs fully pipelined while still giving 1 result/cycle throughput. With m=2-4, latency is ceil(N/m)+2 cycles, which for N=12-16 gives 5-10 cycles, easily under 440 ns at reasonable Fmax. Fewer pipeline registers means fewer FFs, potentially lower luts_plus_ffs. Same accuracy parameters as pipelined. This family trades a small latency increase for significant FF savings, which matters for the area objective.
- `unrolled_k` (20 evals): data_width=14..18, n_iter=12..16, angle_guard=-2..0, frac_guard=0..2, rounding=trunc|round, k=4..8. *Why:* unrolled_k with k=4-8 does k micro-rotations per cycle, so latency is ceil(N/k)+3 cycles. For N=12-16, k=4-8, that's 4-7 cycles. Throughput is 1 result per ceil(N/k) cycles, so at Fmax=100 MHz, k=8 gives ~12.5 Msps which may not meet 32 Msps. However, if Fmax is higher (150+ MHz) or k is larger, it could work. Including it to check if the reduced pipeline depth (fewer stages) gives a better area/throughput tradeoff than pipelined_m. Likely will be dominated but worth a small budget share to confirm.

**Result (code):** 100 evaluations this round, 100 total; 17 feasible; hypervolume 3031 (n/a).

**LLM decision:** `refine` — The current Pareto front is dominated by `pipelined_m` designs with `data_width=18` and `n_iter` in [14, 15]. The `pipelined` family is significantly more expensive (min 1902 vs 1110 luts_plus_ffs) for comparable or slightly better accuracy, making it less attractive for the primary objective of minimizing area. `unrolled_k` failed to meet throughput constraints. The `iterative` family was not explored in Round 1; given its shared datapath and low resource usage, it is a strong candidate for the minimum area corner, especially if its throughput (1 result/cycle) can meet the 32 MSPS requirement (which requires Fmax >= 32 MHz, easily achievable). To maximize hypervolume and find the true minimum area design, we should explore `iterative` and refine the `pipelined_m` search around the known good region (data_width 16-18, n_iter 12-16) to see if lower area is possible with slightly lower accuracy (still > 12 bits) or if `iterative` offers a better trade-off.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 3031 (gain this round: n/a (first round)).
Feasible designs: 17 of 100 evaluations (13 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 20% violate; best seen 282
- max_abs_err <= 0.000244141: 82% violate; best seen 0.000102 (2^-13.25)
- sys_p99_batch_us <= 0.44: 20% violate; best seen 0.16

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1110, accuracy_bits=12.3, luts=827, ffs=282, throughput_msps=97.8, max_abs_err=0.0002 (2^-12.28), power_index=1.34
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=1183, accuracy_bits=12.4, luts=893, ffs=291, throughput_msps=93.6, max_abs_err=0.000179 (2^-12.45), power_index=1.42
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round m=2] luts_plus_ffs=1419, accuracy_bits=12.8, luts=890, ffs=529, throughput_msps=171, max_abs_err=0.000145 (2^-12.75), power_index=1.71
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=1998, accuracy_bits=12.8, luts=985, ffs=1013, throughput_msps=264, max_abs_err=0.000136 (2^-12.84), power_index=2.41
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=2 rounding=round] luts_plus_ffs=2098, accuracy_bits=13.3, luts=1055, ffs=1043, throughput_msps=264, max_abs_err=0.000102 (2^-13.25), power_index=2.53
Front coverage: luts_plus_ffs 1110..2098 (HV reference 4000); accuracy_bits 12.3..13.3 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 12.23 bits
- pipelined: 45 evals, 9 feasible; max throughput seen 282 MSPS; best accuracy 13.25 bits; best feasible luts_plus_ffs=1902; feasible ranges: data_width 17..18, n_iter 16..16, angle_guard -1..0, frac_guard 1..2
- pipelined_m: 35 evals, 8 feasible; max throughput seen 171 MSPS; best accuracy 12.75 bits; best feasible luts_plus_ffs=1110; feasible ranges: data_width 18..18, n_iter 14..15, angle_guard 0..0, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Explore iterative for potential area savings and refine pipelined_m to map the front better in the low-area region.*)
- `iterative` (50 evals): data_width=14..18, n_iter=12..16, angle_guard=-1..1, frac_guard=0..2, rounding=trunc|round. *Why:* Unexplored family with potentially lowest area due to shared datapath. Need to check if it meets throughput and accuracy constraints.
- `pipelined_m` (50 evals): data_width=16..18, n_iter=12..16, angle_guard=-1..1, frac_guard=0..2, rounding=trunc|round, m=2..6. *Why:* Refine around the current best feasible region to explore the trade-off curve more densely and potentially find lower area designs with acceptable accuracy.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 200 total; 39 feasible; hypervolume 3073 (+1.4%).

**LLM decision:** `refine` — The feasible front is dominated by `pipelined_m` designs (7 of 8 points), with the best area (1082 LUTs+FFs) and a clear trade-off curve extending to higher accuracy. `iterative` and `unrolled_k` are infeasible due to throughput limits (<13 MSPs vs 32 required). `pipelined` is feasible but significantly more expensive (min 1902 vs 1082) and offers no advantage in the area-accuracy trade-off compared to `pipelined_m` with smaller `m`. The current front covers data_width 17-18 and n_iter 14-16. To maximize hypervolume and ensure the selection rule (min area) picks the optimal design, we should focus the remaining budget on refining the `pipelined_m` family around the known feasible region (data_width 17-18, n_iter 14-16, m 2-5) to tighten the Pareto front, particularly checking if slightly lower n_iter or different guard bits can reduce area further while maintaining the 12.3+ bit accuracy and throughput constraints.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 3073 (gain this round: +1.4%).
Feasible designs: 39 of 200 evaluations (20 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 35% violate; best seen 282
- max_abs_err <= 0.000244141: 72% violate; best seen 0.000102 (2^-13.25)
- sys_p99_batch_us <= 0.44: 40% violate; best seen 0.16

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=5] luts_plus_ffs=1082, accuracy_bits=12.3, luts=863, ffs=219, throughput_msps=80.6, max_abs_err=0.000192 (2^-12.35), power_index=1.3
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=1183, accuracy_bits=12.4, luts=893, ffs=291, throughput_msps=93.6, max_abs_err=0.000179 (2^-12.45), power_index=1.42
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=3] luts_plus_ffs=1190, accuracy_bits=12.5, luts=841, ffs=349, throughput_msps=119, max_abs_err=0.000175 (2^-12.48), power_index=1.43
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1225, accuracy_bits=12.5, luts=868, ffs=357, throughput_msps=119, max_abs_err=0.000172 (2^-12.50), power_index=1.48
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=1265, accuracy_bits=12.6, luts=906, ffs=359, throughput_msps=119, max_abs_err=0.00016 (2^-12.61), power_index=1.52
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round m=2] luts_plus_ffs=1419, accuracy_bits=12.8, luts=890, ffs=529, throughput_msps=171, max_abs_err=0.000145 (2^-12.75), power_index=1.71
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=1998, accuracy_bits=12.8, luts=985, ffs=1013, throughput_msps=264, max_abs_err=0.000136 (2^-12.84), power_index=2.41
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=2 rounding=round] luts_plus_ffs=2098, accuracy_bits=13.3, luts=1055, ffs=1043, throughput_msps=264, max_abs_err=0.000102 (2^-13.25), power_index=2.53
Front coverage: luts_plus_ffs 1082..2098 (HV reference 4000); accuracy_bits 12.3..13.3 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 13.03 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 12.23 bits
- pipelined: 45 evals, 9 feasible; max throughput seen 282 MSPS; best accuracy 13.25 bits; best feasible luts_plus_ffs=1902; feasible ranges: data_width 17..18, n_iter 16..16, angle_guard -1..0, frac_guard 1..2
- pipelined_m: 85 evals, 30 feasible; max throughput seen 171 MSPS; best accuracy 12.80 bits; best feasible luts_plus_ffs=1082; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..1, frac_guard 0..2, m 2..5
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Narrowing to the proven feasible region of pipelined_m allows Optuna to densely sample the trade-off curve, ensuring the hypervolume is maximized and the minimum-area design is robustly identified.*)
- `pipelined_m` (40 evals): data_width=17..18, n_iter=14..16, angle_guard=0..1, frac_guard=0..2, rounding=trunc|round, m=2..5. *Why:* Focus exclusively on the dominant feasible family to refine the Pareto front in the area-accuracy space.

**Result (code):** 40 evaluations this round, 240 total; 71 feasible; hypervolume 4687 (+52.5%).

**LLM decision:** `stop` — The feasible Pareto front is well-established and robust. The `pipelined_m` family dominates the solution space, providing designs that satisfy all constraints (throughput >= 32 MSPS, max_abs_err <= 2^-12, sys_p99_batch_us <= 0.44 us) with a minimum area of 1082 LUTs+FFs. The front spans a reasonable range of accuracy (12.3 to 13.7 bits) and area (1082 to 1371), covering the trade-off curve effectively. The `pipelined` family offers higher throughput but at a significantly higher area cost (min 1902), making it less optimal for the 'min luts_plus_ffs' selection rule. Other families (`iterative`, `unrolled_k`) fail to meet the throughput constraint. Since this is the final round and the front is mature with no significant gaps in the objective space, stopping is the appropriate action.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 4687 (gain this round: +52.5%).
Feasible designs: 71 of 240 evaluations (39 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 29% violate; best seen 282
- max_abs_err <= 0.000244141: 62% violate; best seen 7.47e-05 (2^-13.71)
- sys_p99_batch_us <= 0.44: 35% violate; best seen 0.16

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=5] luts_plus_ffs=1082, accuracy_bits=12.3, luts=863, ffs=219, throughput_msps=80.6, max_abs_err=0.000192 (2^-12.35), power_index=1.3
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1161, accuracy_bits=12.5, luts=868, ffs=293, throughput_msps=93.6, max_abs_err=0.000172 (2^-12.50), power_index=1.4
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1234, accuracy_bits=12.6, luts=934, ffs=301, throughput_msps=93.6, max_abs_err=0.000157 (2^-12.64), power_index=1.49
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1294, accuracy_bits=13.2, luts=1001, ffs=293, throughput_msps=93.6, max_abs_err=0.000104 (2^-13.23), power_index=1.56
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1351, accuracy_bits=13.3, luts=1055, ffs=297, throughput_msps=93.6, max_abs_err=0.000102 (2^-13.25), power_index=1.63
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1371, accuracy_bits=13.7, luts=1071, ffs=301, throughput_msps=93.6, max_abs_err=7.47e-05 (2^-13.71), power_index=1.65
Front coverage: luts_plus_ffs 1082..1371 (HV reference 4000); accuracy_bits 12.3..13.7 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 13.03 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 12.23 bits
- pipelined: 45 evals, 9 feasible; max throughput seen 282 MSPS; best accuracy 13.25 bits; best feasible luts_plus_ffs=1902; feasible ranges: data_width 17..18, n_iter 16..16, angle_guard -1..0, frac_guard 1..2
- pipelined_m: 125 evals, 62 feasible; max throughput seen 171 MSPS; best accuracy 13.71 bits; best feasible luts_plus_ffs=1082; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..1, frac_guard 0..2, m 2..5
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (160 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (6 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 169 feasible; hypervolume 1.948e+04 (+315.6%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and robust. The `pipelined_m` family dominates the solution space, providing designs that satisfy all constraints (throughput >= 32 MSPS, max_abs_err <= 2^-12, sys_p99_batch_us <= 0.44 us) with a minimum area of 1082 LUTs+FFs. The front spans a reasonable range of accuracy (12.3 to 13.7 bits) and area (1082 to 1371), covering the trade-off curve effectively. The `pipelined` family offers higher throughput but at a significantly higher area cost (min 1902), making it less optimal for the 'min luts_plus_ffs' selection rule. Other families (`iterative`, `unrolled_k`) fail to meet the throughput constraint. Since this is the final round and the front is mature with no significant gaps in the objective space, stopping is the appropriate action.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.948e+04 (gain this round: +315.6%).
Feasible designs: 169 of 400 evaluations (125 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 18% violate; best seen 282
- max_abs_err <= 0.000244141: 40% violate; best seen 3.07e-08 (2^-24.96)
- sys_p99_batch_us <= 0.44: 35% violate; best seen 0.16

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=5] luts_plus_ffs=1082, accuracy_bits=12.3, luts=863, ffs=219, throughput_msps=80.6, max_abs_err=0.000192 (2^-12.35), power_index=1.3
- pipelined_m [data_width=19 n_iter=15 angle_guard=-1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1248, accuracy_bits=12.9, luts=949, ffs=299, throughput_msps=93.6, max_abs_err=0.000129 (2^-12.92), power_index=1.5
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1351, accuracy_bits=13.3, luts=1055, ffs=297, throughput_msps=93.6, max_abs_err=0.000102 (2^-13.25), power_index=1.63
- pipelined_m [data_width=23 n_iter=15 angle_guard=3 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1557, accuracy_bits=14, luts=1185, ffs=371, throughput_msps=89.6, max_abs_err=6.2e-05 (2^-13.98), power_index=1.87
- pipelined_m [data_width=22 n_iter=18 angle_guard=3 frac_guard=0 rounding=round m=4] luts_plus_ffs=1777, accuracy_bits=16.5, luts=1349, ffs=428, throughput_msps=89.6, max_abs_err=1.1e-05 (2^-16.47), power_index=2.14
- pipelined_m [data_width=22 n_iter=20 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1981, accuracy_bits=17.5, luts=1547, ffs=434, throughput_msps=89.6, max_abs_err=5.54e-06 (2^-17.46), power_index=2.38
- pipelined_m [data_width=23 n_iter=21 angle_guard=1 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=2251, accuracy_bits=18.1, luts=1649, ffs=602, throughput_msps=114, max_abs_err=3.47e-06 (2^-18.14), power_index=2.71
- pipelined_m [data_width=24 n_iter=23 angle_guard=3 frac_guard=2 rounding=round m=3] luts_plus_ffs=2767, accuracy_bits=20.7, luts=2026, ffs=741, throughput_msps=110, max_abs_err=5.75e-07 (2^-20.73), power_index=3.33
- pipelined_m [data_width=28 n_iter=23 angle_guard=3 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=3037, accuracy_bits=21.7, luts=2208, ffs=829, throughput_msps=106, max_abs_err=3.01e-07 (2^-21.66), power_index=3.66
- pipelined_m [data_width=28 n_iter=28 angle_guard=3 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=3731, accuracy_bits=23.3, luts=2708, ffs=1023, throughput_msps=106, max_abs_err=1e-07 (2^-23.25), power_index=4.49
Front coverage: luts_plus_ffs 1082..3731 (HV reference 4000); accuracy_bits 12.3..23.3 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 13.03 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 12.23 bits
- pipelined: 45 evals, 9 feasible; max throughput seen 282 MSPS; best accuracy 13.25 bits; best feasible luts_plus_ffs=1902; feasible ranges: data_width 17..18, n_iter 16..16, angle_guard -1..0, frac_guard 1..2
- pipelined_m: 285 evals, 160 feasible; max throughput seen 171 MSPS; best accuracy 24.96 bits; best feasible luts_plus_ffs=1082; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..5
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 26172 in, 3780 out
- provider-reported cost: $0.0083
- full prompts and replies: `llm_trace.jsonl`

