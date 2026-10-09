# DSE run: bursty_offload

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 4 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec bursty_offload: Sin/cos offload for an 8-channel sensor front end: bursts of 8 requests arrive as a Poisson process, 2 requests/us on average; p99 request latency must be <= 0.4 us. Max error <= 2^-10. Minimise LUTs + FFs.
  constraint: throughput_msps >= 2
  constraint: max_abs_err <= 0.000976562
  constraint: sys_p99_latency_us <= 0.4
  objective: min luts_plus_ffs (HV ref 3000)
  objective: max accuracy_bits (HV ref 10)
  select: min luts_plus_ffs
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): bursty requests: bursts of 8 (0 ns apart) arriving as a Poisson process, 2 requests/us on average
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=15,n_iter=12,angle_guard=1,frac_guard=2,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 654 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 199 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 51.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0642 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000772 (2^-10.34) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.33 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000225 (2^-12.11) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.85 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (32768 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 5 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 79.9 dBc, SNR 70.3 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: bursty requests: bursts of 8 (0 ns apart) arriving as a Poisson process, 2 requests/us on average. Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_latency_us <= 0.4 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=15,n_iter=12,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 0.1124 → 0.1351 | yes |
| `pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=4,rounding=round,m=4` | 0.1124 → 0.1351 | yes |
| `pipelined_m:data_width=15,n_iter=12,angle_guard=2,frac_guard=2,rounding=round,m=3` | 0.09642 → 0.1066 | yes |
| `pipelined_m:data_width=15,n_iter=13,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 0.1226 → 0.1453 | yes |
| `pipelined_m:data_width=15,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 0.1226 → 0.1453 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (24 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=12,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 654 | 199 | 97.8 | 5 | 0.0642 | 0.000772 (2^-10.34) | 10.34 |
| 1 | `pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=4,rounding=round,m=4` | 707 | 201 | 97.8 | 5 | 0.0683 | 0.00074 (2^-10.40) | 10.40 |
| 2 | `pipelined_m:data_width=15,n_iter=12,angle_guard=2,frac_guard=2,rounding=round,m=3` | 698 | 262 | 124.5 | 6 | 0.0722 | 0.000649 (2^-10.59) | 10.59 |
| 3 | `pipelined_m:data_width=15,n_iter=13,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 713 | 256 | 97.8 | 6 | 0.0729 | 0.000528 (2^-10.89) | 10.89 |
| 4 | `pipelined_m:data_width=15,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 726 | 260 | 97.8 | 6 | 0.0742 | 0.000466 (2^-11.07) | 11.07 |
| 5 | `pipelined_m:data_width=15,n_iter=13,angle_guard=2,frac_guard=2,rounding=round,m=4` | 758 | 262 | 97.8 | 6 | 0.0767 | 0.000431 (2^-11.18) | 11.18 |
| 6 | `pipelined_m:data_width=15,n_iter=13,angle_guard=2,frac_guard=4,rounding=trunc,m=4` | 777 | 272 | 93.6 | 6 | 0.0789 | 0.000424 (2^-11.20) | 11.20 |
| 7 | `pipelined_m:data_width=15,n_iter=14,angle_guard=2,frac_guard=3,rounding=trunc,m=4` | 813 | 266 | 97.8 | 6 | 0.0812 | 0.000359 (2^-11.44) | 11.44 |
| 8 | `pipelined_m:data_width=15,n_iter=15,angle_guard=2,frac_guard=3,rounding=trunc,m=4` | 876 | 266 | 97.8 | 6 | 0.0859 | 0.000302 (2^-11.69) | 11.69 |
| 9 | `pipelined_m:data_width=15,n_iter=15,angle_guard=2,frac_guard=2,rounding=round,m=3` | 878 | 321 | 124.5 | 7 | 0.0902 | 0.000271 (2^-11.85) | 11.85 |
| 10 | `pipelined_m:data_width=15,n_iter=15,angle_guard=2,frac_guard=4,rounding=round,m=3` | 937 | 337 | 119.3 | 7 | 0.0958 | 0.00024 (2^-12.03) | 12.03 |
| 11 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=2` | 863 | 465 | 171.0 | 9 | 0.0999 | 0.000192 (2^-12.35) | 12.35 |
| 12 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=2` | 906 | 488 | 164.4 | 9 | 0.105 | 0.00016 (2^-12.61) | 12.61 |
| 13 | `pipelined_m:data_width=17,n_iter=17,angle_guard=3,frac_guard=4,rounding=trunc,m=5` | 1152 | 305 | 77.0 | 6 | 0.11 | 7.04e-05 (2^-13.79) | 13.79 |
| 14 | `pipelined_m:data_width=23,n_iter=17,angle_guard=-1,frac_guard=4,rounding=trunc,m=5` | 1388 | 373 | 70.6 | 6 | 0.132 | 1.98e-05 (2^-15.63) | 15.63 |
| 15 | `pipelined_m:data_width=27,n_iter=17,angle_guard=2,frac_guard=3,rounding=round,m=6` | 1664 | 341 | 59.9 | 5 | 0.151 | 1.53e-05 (2^-16.00) | 16.00 |
| 16 | `pipelined_m:data_width=24,n_iter=23,angle_guard=-2,frac_guard=1,rounding=round,m=6` | 1864 | 367 | 62.5 | 6 | 0.168 | 7.2e-06 (2^-17.08) | 17.08 |
| 17 | `pipelined_m:data_width=23,n_iter=19,angle_guard=0,frac_guard=4,rounding=round,m=3` | 1628 | 634 | 110.0 | 9 | 0.17 | 6.1e-06 (2^-17.32) | 17.32 |
| 18 | `pipelined_m:data_width=23,n_iter=24,angle_guard=4,frac_guard=0,rounding=round,m=5` | 1920 | 450 | 70.6 | 7 | 0.178 | 2.9e-06 (2^-18.39) | 18.39 |
| 19 | `pipelined_m:data_width=27,n_iter=23,angle_guard=-2,frac_guard=4,rounding=trunc,m=8` | 2161 | 331 | 44.0 | 5 | 0.187 | 1.04e-06 (2^-19.88) | 19.88 |
| 20 | `pipelined_m:data_width=24,n_iter=24,angle_guard=4,frac_guard=3,rounding=round,m=6` | 2189 | 404 | 59.9 | 6 | 0.195 | 3.93e-07 (2^-21.28) | 21.28 |
| 21 | `pipelined_m:data_width=26,n_iter=28,angle_guard=2,frac_guard=3,rounding=round,m=8` | 2678 | 424 | 45.9 | 6 | 0.233 | 1.5e-07 (2^-22.66) | 22.66 |
| 22 | `pipelined_m:data_width=28,n_iter=26,angle_guard=3,frac_guard=0,rounding=round,m=3` | 2455 | 910 | 105.9 | 11 | 0.253 | 1.1e-07 (2^-23.12) | 23.12 |
| 23 | `pipelined_m:data_width=27,n_iter=30,angle_guard=3,frac_guard=3,rounding=round,m=5` | 2996 | 638 | 70.6 | 8 | 0.273 | 5.3e-08 (2^-24.17) | 24.17 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires throughput >= 2 Msps, max_abs_err <= 2^-10, and sys_p99_latency <= 0.4 us for bursty Poisson traffic (bursts of 8, 2 req/us avg). The pipelined and pipelined_m families are the strongest candidates because they produce 1 result/cycle, which is critical for draining bursts of 8 without queue buildup that would violate the p99 latency constraint. The iterative family is excluded because at 1 result/(N+3) cycles, even at high Fmax, it cannot sustain 2 Msps with acceptable latency for bursts. Unrolled_k is included as a third option because with k=2..4 it can achieve sufficient throughput (1 result per 2-3 cycles) with lower area than pipelined, and its latency (ceil(N/k)+3 cycles) is short enough. For accuracy: max_abs_err <= 2^-10 = 0.000977. CORDIC error is dominated by residual angle after N iterations (~2^-N for the gain-compensated case, but practically ~2^-(N-1) to 2^-N depending on implementation). N >= 10 should suffice; I range N from 8 to 14 to capture the trade-off. Data width W must be >= 12 for the output to have enough fractional bits (Q1.(W-2) means W=12 gives 10 fractional bits, matching 2^-10). I range W from 8 to 14 to explore the area-accuracy trade-off. angle_guard and frac_guard are ranged broadly (-2..4 and 0..4) since they affect both accuracy and area. Rounding is included as a choice since it affects accuracy. The budget is split 45/35/20 favoring pipelined (most likely to meet all constraints) and pipelined_m (best area candidate), with unrolled_k as a secondary area option. This covers the main trade-off axes: area (FF count via m or k), accuracy (N, W, guards), and timing (Fmax via path length).*)
- `pipelined` (45 evals): data_width=8..14, n_iter=8..14, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Pipelined gives 1 result/cycle, essential for handling bursts of 8 with p99 latency <= 0.4us. At 2 Msps average, pipelined can sustain throughput without queue buildup. N+2 latency with N=8..14 gives 10..16 cycles; at ~100-150 MHz that's ~67-160 ns, well under 400 ns. Accuracy: N=10+ with W=12+ should meet 2^-10. Area is moderate (N stages of registers). This is the primary candidate for meeting all constraints with reasonable area.
- `pipelined_m` (35 evals): data_width=8..14, n_iter=8..14, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* Pipelined_m reduces register count by only registering every m stages, cutting FF area significantly vs full pipelined while still achieving 1 result/cycle throughput. Latency is ceil(N/m)+2 cycles, which for N=10, m=2 gives 7 cycles (~50-70 ns), still well under 400 ns. This family should dominate the area objective while maintaining the throughput and latency needed for bursty traffic. Key trade-off: larger m means fewer FFs but potentially lower Fmax due to longer combinational paths.
- `unrolled_k` (20 evals): data_width=8..14, n_iter=8..14, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..4. *Why:* Unrolled_k with k=2..4 does multiple micro-rotations per cycle, reducing latency to ceil(N/k)+3 cycles. For N=10, k=4: 3+3=6 cycles (~40-60 ns). Throughput is 1 result per ceil(N/k) cycles, so k=4 gives 1 result/3 cycles = ~33-50 Msps at 100-150 MHz, well above 2 Msps. Area is smaller than pipelined (no per-stage registers, just shared datapath + FSM). However, the shared datapath with k chained rotations may have longer combinational paths, potentially lowering Fmax. Worth exploring for the area-accuracy trade-off.

**Result (code):** 100 evaluations this round, 100 total; 3 feasible; hypervolume 564.6 (n/a).

**LLM decision:** `refine` — The current front is dominated by `pipelined_m` (1120 LUTs+FFs) and `pipelined` (1364 LUTs+FFs). The `unrolled_k` family failed completely (0 feasible) because its throughput (max 14 MSPS) is far below the 2 MSPS requirement when combined with the accuracy constraints, or rather, it likely failed accuracy at low N or throughput at high N/low k. The `pipelined` and `pipelined_m` families are the only viable candidates. The feasible region for `pipelined` is narrow (data_width 13-14, n_iter 12-14), and for `pipelined_m` it is a single point so far (data_width 12, n_iter 13, m=2). To improve the hypervolume and find a better trade-off between area and accuracy, we should focus the search on these two families. Specifically, `pipelined_m` with m=2 or m=3 might offer lower area than `pipelined` for similar accuracy, or `pipelined` with slightly lower n_iter/data_width might reduce area while staying within the error bound. The `iterative` family is not yet explored, but given its low throughput (1 result per N+3 cycles), it is unlikely to meet the 2 MSPS throughput constraint at reasonable Fmax unless N is very small, which would violate accuracy. Thus, focusing on `pipelined` and `pipelined_m` is the most efficient use of the remaining budget.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 564.6 (gain this round: n/a (first round)).
Feasible designs: 3 of 100 evaluations (3 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 292
- max_abs_err <= 0.000976562: 97% violate; best seen 0.000785 (2^-10.31)
- sys_p99_latency_us <= 0.4: 20% violate; best seen 0.0568

Pareto front (feasible, 2 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=12 n_iter=13 angle_guard=4 frac_guard=4 rounding=round m=2] luts_plus_ffs=1120, accuracy_bits=10.2, luts=713, ffs=407, throughput_msps=171, max_abs_err=0.000847 (2^-10.20), power_index=0.0843
- pipelined [data_width=14 n_iter=12 angle_guard=2 frac_guard=3 rounding=round] luts_plus_ffs=1364, accuracy_bits=10.3, luts=684, ffs=680, throughput_msps=273, max_abs_err=0.000785 (2^-10.31), power_index=0.103
Front coverage: luts_plus_ffs 1120..1364 (HV reference 3000); accuracy_bits 10.2..10.3 (HV reference 10); data_width on the front 12..14 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 14 MSPS; best accuracy 6.87 bits
- pipelined: 45 evals, 2 feasible; max throughput seen 292 MSPS; best accuracy 10.31 bits; best feasible luts_plus_ffs=1364; feasible ranges: data_width 13..14, n_iter 12..14, angle_guard 2..2, frac_guard 2..3
- pipelined_m: 35 evals, 1 feasible; max throughput seen 178 MSPS; best accuracy 10.20 bits; best feasible luts_plus_ffs=1120; feasible ranges: data_width 12..12, n_iter 13..13, angle_guard 4..4, frac_guard 4..4, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Focus on the two feasible families to refine the Pareto front. The `pipelined` family is explored with slightly wider ranges to find lower area designs, and the `pipelined_m` family is explored with wider ranges and more m values to find the optimal area/accuracy trade-off. The `iterative` and `unrolled_k` families are excluded due to throughput constraints.*)
- `pipelined` (50 evals): data_width=12..15, n_iter=11..15, angle_guard=1..3, frac_guard=2..4, rounding=trunc|round. *Why:* Current best pipelined design is at 1364 LUTs+FFs. Expanding data_width down to 12 and n_iter down to 11 may find lower area designs that still meet the 2^-10 error bound. Angle_guard and frac_guard are varied to explore the accuracy/area trade-off.
- `pipelined_m` (50 evals): data_width=11..15, n_iter=11..16, angle_guard=1..4, frac_guard=2..4, rounding=trunc|round, m=2..4. *Why:* Current best pipelined_m design is at 1120 LUTs+FFs. This family has the potential for lower area due to reduced register count. Expanding the ranges allows finding if a slightly lower accuracy (but still > 10 bits) design with lower area exists, or if a higher accuracy design with comparable area exists. m=2,3,4 are explored to find the optimal pipeline depth for area/latency trade-off.

**Result (code):** 100 evaluations this round, 200 total; 70 feasible; hypervolume 4207 (+645.1%).

**LLM decision:** `refine` — The front spans 853-1762 luts_plus_ffs and 10.3-12.2 accuracy bits. The selection rule (min luts_plus_ffs) will pick the 853 pipelined_m design, but hypervolume requires covering the full curve. The gap between pipelined_m's max accuracy (12.03) and pipelined's min area (1710) at 12.24 bits suggests unexplored mid-area designs. unrolled_k is infeasible (0 feasible, max throughput 14 MSPS but best accuracy only 6.87 bits, far below the 10-bit requirement). iterative is not yet explored but is unlikely to help: it has the same accuracy as other families for the same parameters, but its throughput is 1 result per N+3 cycles, which for N>=12 gives <= ~80 MSPS at typical Fmax, and its area is typically higher than pipelined_m due to the shared datapath with barrel shifters. The 65% max_abs_err violation rate indicates many designs are too inaccurate, so narrowing to the proven feasible accuracy ranges (data_width >= 14, n_iter >= 12) is essential. Refining both pipelined and pipelined_m in their proven feasible ranges with 100 evals each should fill the mid-area gap and confirm the front's extent before the final mapping round.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 4207 (gain this round: +645.1%).
Feasible designs: 70 of 200 evaluations (52 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 292
- max_abs_err <= 0.000976562: 65% violate; best seen 0.000207 (2^-12.24)
- sys_p99_latency_us <= 0.4: 10% violate; best seen 0.0568

Pareto front (feasible, 11 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=853, accuracy_bits=10.3, luts=654, ffs=199, throughput_msps=97.8, max_abs_err=0.000772 (2^-10.34), power_index=0.0642
- pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=4 rounding=round m=4] luts_plus_ffs=908, accuracy_bits=10.4, luts=707, ffs=201, throughput_msps=97.8, max_abs_err=0.00074 (2^-10.40), power_index=0.0683
- pipelined_m [data_width=15 n_iter=12 angle_guard=2 frac_guard=2 rounding=round m=3] luts_plus_ffs=960, accuracy_bits=10.6, luts=698, ffs=262, throughput_msps=124, max_abs_err=0.000649 (2^-10.59), power_index=0.0722
- pipelined_m [data_width=15 n_iter=13 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=970, accuracy_bits=10.9, luts=713, ffs=256, throughput_msps=97.8, max_abs_err=0.000528 (2^-10.89), power_index=0.0729
- pipelined_m [data_width=15 n_iter=13 angle_guard=1 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=1032, accuracy_bits=11, luts=764, ffs=268, throughput_msps=93.6, max_abs_err=0.000503 (2^-10.96), power_index=0.0777
- pipelined_m [data_width=14 n_iter=14 angle_guard=2 frac_guard=4 rounding=round m=3] luts_plus_ffs=1149, accuracy_bits=11.2, luts=829, ffs=320, throughput_msps=124, max_abs_err=0.000413 (2^-11.24), power_index=0.0865
- pipelined_m [data_width=15 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=3] luts_plus_ffs=1199, accuracy_bits=11.8, luts=878, ffs=321, throughput_msps=124, max_abs_err=0.000271 (2^-11.85), power_index=0.0902
- pipelined_m [data_width=15 n_iter=15 angle_guard=2 frac_guard=4 rounding=round m=3] luts_plus_ffs=1274, accuracy_bits=12, luts=937, ffs=337, throughput_msps=119, max_abs_err=0.00024 (2^-12.03), power_index=0.0958
- pipelined [data_width=15 n_iter=14 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=1710, accuracy_bits=12.2, luts=859, ffs=852, throughput_msps=273, max_abs_err=0.000215 (2^-12.18), power_index=0.129
- pipelined [data_width=15 n_iter=14 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=1762, accuracy_bits=12.2, luts=886, ffs=876, throughput_msps=264, max_abs_err=0.000207 (2^-12.24), power_index=0.133
Front coverage: luts_plus_ffs 853..1762 (HV reference 3000); accuracy_bits 10.3..12.2 (HV reference 10); data_width on the front 14..15 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 14 MSPS; best accuracy 6.87 bits
- pipelined: 95 evals, 34 feasible; max throughput seen 292 MSPS; best accuracy 12.24 bits; best feasible luts_plus_ffs=1364; feasible ranges: data_width 13..15, n_iter 12..15, angle_guard 1..3, frac_guard 2..4
- pipelined_m: 85 evals, 36 feasible; max throughput seen 178 MSPS; best accuracy 12.03 bits; best feasible luts_plus_ffs=853; feasible ranges: data_width 12..15, n_iter 12..16, angle_guard 1..4, frac_guard 2..4, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The front spans 853-1762 luts_plus_ffs and 10.3-12.2 accuracy bits. The selection rule (min luts_plus_ffs) will pick the 853 pipelined_m design, but hypervolume requires covering the full curve. The gap between pipelined_m's max accuracy (12.03) and pipelined's min area (1710) at 12.24 bits suggests unexplored mid-area designs. unrolled_k is infeasible (0 feasible, max throughput 14 MSPS but best accuracy only 6.87 bits, far below the 10-bit requirement). iterative is not yet explored but is unlikely to help: it has the same accuracy as other families for the same parameters, but its throughput is 1 result per N+3 cycles, which for N>=12 gives <= ~80 MSPS at typical Fmax, and its area is typically higher than pipelined_m due to the shared datapath with barrel shifters. The 65% max_abs_err violation rate indicates many designs are too inaccurate, so narrowing to the proven feasible accuracy ranges (data_width >= 14, n_iter >= 12) is essential. Refining both pipelined and pipelined_m in their proven feasible ranges with 100 evals each should fill the mid-area gap and confirm the front's extent before the final mapping round.*)
- `pipelined_m` (20 evals): data_width=14..15, n_iter=12..15, angle_guard=1..3, frac_guard=2..4, rounding=trunc|round, m=2..4. *Why:* pipelined_m dominates the low-area end of the front (853-1274 luts_plus_ffs) and has the best feasible area (853). The current front only reaches 12.03 accuracy bits in this family, while pipelined reaches 12.24 at much higher area (1710+). There is likely a gap in the mid-area region (1300-1700) where pipelined_m with slightly higher n_iter or data_width=16 could bridge the accuracy gap without the full FF cost of pipelined. Narrowing to the proven feasible ranges (data_width 14-15, n_iter 12-15, angle_guard 1-3, frac_guard 2-4, m 2-4) focuses the budget on the trade-off curve between the two families.
- `pipelined` (20 evals): data_width=14..16, n_iter=12..16, angle_guard=1..3, frac_guard=2..4, rounding=trunc|round. *Why:* pipelined provides the high-accuracy end of the front (12.24 bits) but at high area (1710+). The selection rule minimizes luts_plus_ffs, so the cheapest feasible design (853, pipelined_m) is likely the final pick. However, hypervolume rewards covering the full trade-off curve. Extending data_width to 16 and n_iter to 16 in pipelined may reveal whether accuracy can be pushed beyond 12.24 bits, or whether there are cheaper pipelined variants (e.g., data_width=14 with higher n_iter) that fill the gap between 1274 and 1710 luts_plus_ffs. The 10% sys_p99_latency violation rate suggests some pipelined designs are too slow for the bursty system, so focusing on the proven feasible ranges (angle_guard 1-3, frac_guard 2-4) avoids wasting budget on infeasible high-latency corners.

**Result (code):** 40 evaluations this round, 240 total; 110 feasible; hypervolume 4314 (+2.6%).

**LLM decision:** `stop` — The exploration has successfully mapped a robust Pareto front for the `pipelined_m` and `pipelined` families that satisfies all system and accuracy constraints. The front spans `luts_plus_ffs` from 853 to 2054 and `accuracy_bits` from 10.3 to 12.3, providing a clear trade-off curve. The minimum area design (853 LUTs+FFs) meets the throughput (97.8 MSPS >= 2), accuracy (10.3 bits >= 10), and system latency constraints. The `unrolled_k` family was proven infeasible for this spec due to insufficient throughput and accuracy. Since this is the final round and the front is well-defined with a clear selection candidate (min area), stopping is the appropriate action to finalize the design selection.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 4314 (gain this round: +2.6%).
Feasible designs: 110 of 240 evaluations (85 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 292
- max_abs_err <= 0.000976562: 54% violate; best seen 0.0002 (2^-12.29)
- sys_p99_latency_us <= 0.4: 8% violate; best seen 0.0568

Pareto front (feasible, 15 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=853, accuracy_bits=10.3, luts=654, ffs=199, throughput_msps=97.8, max_abs_err=0.000772 (2^-10.34), power_index=0.0642
- pipelined_m [data_width=15 n_iter=12 angle_guard=2 frac_guard=2 rounding=round m=3] luts_plus_ffs=960, accuracy_bits=10.6, luts=698, ffs=262, throughput_msps=124, max_abs_err=0.000649 (2^-10.59), power_index=0.0722
- pipelined_m [data_width=15 n_iter=13 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=970, accuracy_bits=10.9, luts=713, ffs=256, throughput_msps=97.8, max_abs_err=0.000528 (2^-10.89), power_index=0.0729
- pipelined_m [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1020, accuracy_bits=11.2, luts=758, ffs=262, throughput_msps=97.8, max_abs_err=0.000431 (2^-11.18), power_index=0.0767
- pipelined_m [data_width=15 n_iter=13 angle_guard=2 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=1049, accuracy_bits=11.2, luts=777, ffs=272, throughput_msps=93.6, max_abs_err=0.000424 (2^-11.20), power_index=0.0789
- pipelined_m [data_width=15 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1142, accuracy_bits=11.7, luts=876, ffs=266, throughput_msps=97.8, max_abs_err=0.000302 (2^-11.69), power_index=0.0859
- pipelined_m [data_width=15 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=3] luts_plus_ffs=1199, accuracy_bits=11.8, luts=878, ffs=321, throughput_msps=124, max_abs_err=0.000271 (2^-11.85), power_index=0.0902
- pipelined [data_width=15 n_iter=14 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=1710, accuracy_bits=12.2, luts=859, ffs=852, throughput_msps=273, max_abs_err=0.000215 (2^-12.18), power_index=0.129
- pipelined [data_width=15 n_iter=14 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=1762, accuracy_bits=12.2, luts=886, ffs=876, throughput_msps=264, max_abs_err=0.000207 (2^-12.24), power_index=0.133
- pipelined [data_width=16 n_iter=16 angle_guard=1 frac_guard=4 rounding=round] luts_plus_ffs=2054, accuracy_bits=12.3, luts=1035, ffs=1019, throughput_msps=264, max_abs_err=0.0002 (2^-12.29), power_index=0.155
Front coverage: luts_plus_ffs 853..2054 (HV reference 3000); accuracy_bits 10.3..12.3 (HV reference 10); data_width on the front 14..16 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 14 MSPS; best accuracy 6.87 bits
- pipelined: 115 evals, 54 feasible; max throughput seen 292 MSPS; best accuracy 12.29 bits; best feasible luts_plus_ffs=1364; feasible ranges: data_width 13..16, n_iter 12..16, angle_guard 1..3, frac_guard 2..4
- pipelined_m: 105 evals, 56 feasible; max throughput seen 178 MSPS; best accuracy 12.03 bits; best feasible luts_plus_ffs=853; feasible ranges: data_width 12..15, n_iter 12..16, angle_guard 1..4, frac_guard 2..4, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (118 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (11 front designs; box front_anchored)
- `pipelined` (42 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (4 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 257 feasible; hypervolume 1.243e+04 (+188.1%).

**No LLM call** (code's front-mapping round): The exploration has successfully mapped a robust Pareto front for the `pipelined_m` and `pipelined` families that satisfies all system and accuracy constraints. The front spans `luts_plus_ffs` from 853 to 2054 and `accuracy_bits` from 10.3 to 12.3, providing a clear trade-off curve. The minimum area design (853 LUTs+FFs) meets the throughput (97.8 MSPS >= 2), accuracy (10.3 bits >= 10), and system latency constraints. The `unrolled_k` family was proven infeasible for this spec due to insufficient throughput and accuracy. Since this is the final round and the front is well-defined with a clear selection candidate (min area), stopping is the appropriate action to finalize the design selection.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.243e+04 (gain this round: +188.1%).
Feasible designs: 257 of 400 evaluations (222 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 292
- max_abs_err <= 0.000976562: 36% violate; best seen 5.3e-08 (2^-24.17)
- sys_p99_latency_us <= 0.4: 5% violate; best seen 0.0568

Pareto front (feasible, 24 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=853, accuracy_bits=10.3, luts=654, ffs=199, throughput_msps=97.8, max_abs_err=0.000772 (2^-10.34), power_index=0.0642
- pipelined_m [data_width=15 n_iter=13 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=970, accuracy_bits=10.9, luts=713, ffs=256, throughput_msps=97.8, max_abs_err=0.000528 (2^-10.89), power_index=0.0729
- pipelined_m [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1020, accuracy_bits=11.2, luts=758, ffs=262, throughput_msps=97.8, max_abs_err=0.000431 (2^-11.18), power_index=0.0767
- pipelined_m [data_width=15 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1142, accuracy_bits=11.7, luts=876, ffs=266, throughput_msps=97.8, max_abs_err=0.000302 (2^-11.69), power_index=0.0859
- pipelined_m [data_width=15 n_iter=15 angle_guard=2 frac_guard=4 rounding=round m=3] luts_plus_ffs=1274, accuracy_bits=12, luts=937, ffs=337, throughput_msps=119, max_abs_err=0.00024 (2^-12.03), power_index=0.0958
- pipelined_m [data_width=17 n_iter=17 angle_guard=3 frac_guard=4 rounding=trunc m=5] luts_plus_ffs=1456, accuracy_bits=13.8, luts=1152, ffs=305, throughput_msps=77, max_abs_err=7.04e-05 (2^-13.79), power_index=0.11
- pipelined_m [data_width=27 n_iter=17 angle_guard=2 frac_guard=3 rounding=round m=6] luts_plus_ffs=2005, accuracy_bits=16, luts=1664, ffs=341, throughput_msps=59.9, max_abs_err=1.53e-05 (2^-16.00), power_index=0.151
- pipelined_m [data_width=23 n_iter=24 angle_guard=4 frac_guard=0 rounding=round m=5] luts_plus_ffs=2370, accuracy_bits=18.4, luts=1920, ffs=450, throughput_msps=70.6, max_abs_err=2.9e-06 (2^-18.39), power_index=0.178
- pipelined_m [data_width=24 n_iter=24 angle_guard=4 frac_guard=3 rounding=round m=6] luts_plus_ffs=2592, accuracy_bits=21.3, luts=2189, ffs=404, throughput_msps=59.9, max_abs_err=3.93e-07 (2^-21.28), power_index=0.195
- pipelined_m [data_width=27 n_iter=30 angle_guard=3 frac_guard=3 rounding=round m=5] luts_plus_ffs=3633, accuracy_bits=24.2, luts=2996, ffs=638, throughput_msps=70.6, max_abs_err=5.3e-08 (2^-24.17), power_index=0.273
Front coverage: luts_plus_ffs 853..3633 (HV reference 3000); accuracy_bits 10.3..24.2 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 14 MSPS; best accuracy 6.87 bits
- pipelined: 157 evals, 94 feasible; max throughput seen 292 MSPS; best accuracy 22.51 bits; best feasible luts_plus_ffs=1364; feasible ranges: data_width 13..28, n_iter 12..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 223 evals, 163 feasible; max throughput seen 178 MSPS; best accuracy 24.17 bits; best feasible luts_plus_ffs=853; feasible ranges: data_width 12..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 25906 in, 4980 out
- provider-reported cost: $0.0089
- full prompts and replies: `llm_trace.jsonl`

