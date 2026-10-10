# DSE run: bursty_offload

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`pipelined_m:data_width=18,n_iter=13,angle_guard=-1,frac_guard=0,rounding=round,m=7` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 751 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 157 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 59.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 59.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 67.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0684 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000357 (2^-11.45) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 23.4 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 0.000105 (2^-13.22) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 6.86 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 11.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 4 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 86.2 dBc, SNR 76.7 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: bursty requests: bursts of 8 (0 ns apart) arriving as a Poisson process, 2 requests/us on average. Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_latency_us <= 0.4 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=18,n_iter=13,angle_guard=-1,frac_guard=0,rounding=round,m=7` | 0.1678 → 0.2328 | yes |
| `pipelined_m:data_width=18,n_iter=13,angle_guard=1,frac_guard=1,rounding=trunc,m=5` | 0.1429 → 0.183 | yes |
| `pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=5` | 0.1429 → 0.183 | yes |
| `pipelined_m:data_width=17,n_iter=14,angle_guard=3,frac_guard=1,rounding=round,m=5` | 0.1429 → 0.183 | yes |
| `pipelined_m:data_width=19,n_iter=15,angle_guard=3,frac_guard=0,rounding=trunc,m=6` | 0.1682 → 0.2229 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (35 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=13,angle_guard=-1,frac_guard=0,rounding=round,m=7` | 751 | 157 | 59.6 | 4 | 0.0684 | 0.000357 (2^-11.45) | 11.45 |
| 1 | `pipelined_m:data_width=18,n_iter=13,angle_guard=1,frac_guard=1,rounding=trunc,m=5` | 802 | 228 | 77.0 | 5 | 0.0775 | 0.000294 (2^-11.73) | 11.73 |
| 2 | `pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=5` | 877 | 222 | 77.0 | 5 | 0.0827 | 0.000191 (2^-12.36) | 12.36 |
| 3 | `pipelined_m:data_width=17,n_iter=14,angle_guard=3,frac_guard=1,rounding=round,m=5` | 890 | 225 | 77.0 | 5 | 0.0839 | 0.000185 (2^-12.40) | 12.40 |
| 4 | `pipelined_m:data_width=19,n_iter=15,angle_guard=3,frac_guard=0,rounding=trunc,m=6` | 979 | 241 | 65.4 | 5 | 0.0918 | 0.000109 (2^-13.17) | 13.17 |
| 5 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=2,rounding=round,m=6` | 1002 | 234 | 65.4 | 5 | 0.093 | 9.56e-05 (2^-13.35) | 13.35 |
| 6 | `pipelined_m:data_width=20,n_iter=15,angle_guard=2,frac_guard=0,rounding=trunc,m=6` | 1008 | 249 | 65.4 | 5 | 0.0946 | 8.43e-05 (2^-13.53) | 13.53 |
| 7 | `pipelined_m:data_width=21,n_iter=16,angle_guard=-1,frac_guard=0,rounding=trunc,m=8` | 1080 | 182 | 50.3 | 4 | 0.0949 | 5.44e-05 (2^-14.16) | 14.16 |
| 8 | `pipelined_m:data_width=20,n_iter=17,angle_guard=1,frac_guard=0,rounding=trunc,m=8` | 1135 | 246 | 50.3 | 5 | 0.104 | 4.89e-05 (2^-14.32) | 14.32 |
| 9 | `pipelined_m:data_width=20,n_iter=17,angle_guard=1,frac_guard=1,rounding=trunc,m=8` | 1169 | 250 | 50.3 | 5 | 0.107 | 3.57e-05 (2^-14.78) | 14.78 |
| 10 | `pipelined_m:data_width=19,n_iter=18,angle_guard=3,frac_guard=2,rounding=trunc,m=6` | 1259 | 249 | 65.4 | 5 | 0.113 | 2.81e-05 (2^-15.12) | 15.12 |
| 11 | `pipelined_m:data_width=21,n_iter=17,angle_guard=1,frac_guard=2,rounding=trunc,m=6` | 1253 | 265 | 62.5 | 5 | 0.114 | 2.11e-05 (2^-15.53) | 15.53 |
| 12 | `pipelined_m:data_width=23,n_iter=17,angle_guard=0,frac_guard=1,rounding=trunc,m=7` | 1303 | 280 | 54.3 | 5 | 0.119 | 1.75e-05 (2^-15.80) | 15.80 |
| 13 | `pipelined_m:data_width=25,n_iter=17,angle_guard=2,frac_guard=0,rounding=round,m=8` | 1405 | 305 | 45.9 | 5 | 0.129 | 1.56e-05 (2^-15.97) | 15.97 |
| 14 | `pipelined_m:data_width=25,n_iter=17,angle_guard=2,frac_guard=0,rounding=round,m=7` | 1405 | 305 | 52.0 | 5 | 0.129 | 1.56e-05 (2^-15.97) | 15.97 |
| 15 | `pipelined_m:data_width=21,n_iter=19,angle_guard=3,frac_guard=1,rounding=round,m=5` | 1453 | 345 | 73.7 | 6 | 0.135 | 8.82e-06 (2^-16.79) | 16.79 |
| 16 | `pipelined_m:data_width=25,n_iter=18,angle_guard=-1,frac_guard=1,rounding=round,m=7` | 1527 | 302 | 54.3 | 5 | 0.138 | 8.61e-06 (2^-16.83) | 16.83 |
| 17 | `pipelined_m:data_width=21,n_iter=19,angle_guard=3,frac_guard=4,rounding=round,m=7` | 1567 | 281 | 54.3 | 5 | 0.139 | 6.05e-06 (2^-17.34) | 17.34 |
| 18 | `pipelined_m:data_width=21,n_iter=21,angle_guard=3,frac_guard=3,rounding=round,m=7` | 1693 | 277 | 54.3 | 5 | 0.148 | 3.55e-06 (2^-18.10) | 18.10 |
| 19 | `pipelined_m:data_width=26,n_iter=20,angle_guard=-2,frac_guard=2,rounding=round,m=8` | 1782 | 314 | 45.9 | 5 | 0.158 | 3.27e-06 (2^-18.22) | 18.22 |
| 20 | `pipelined_m:data_width=24,n_iter=20,angle_guard=1,frac_guard=2,rounding=round,m=6` | 1718 | 385 | 62.5 | 6 | 0.158 | 2.62e-06 (2^-18.54) | 18.54 |
| 21 | `pipelined_m:data_width=24,n_iter=20,angle_guard=1,frac_guard=4,rounding=trunc,m=6` | 1747 | 395 | 59.9 | 6 | 0.161 | 2.61e-06 (2^-18.54) | 18.54 |
| 22 | `pipelined_m:data_width=25,n_iter=20,angle_guard=0,frac_guard=2,rounding=round,m=5` | 1760 | 395 | 70.6 | 6 | 0.162 | 2.56e-06 (2^-18.57) | 18.57 |
| 23 | `pipelined_m:data_width=26,n_iter=20,angle_guard=-1,frac_guard=1,rounding=round,m=5` | 1762 | 400 | 70.6 | 6 | 0.163 | 2.52e-06 (2^-18.60) | 18.60 |
| 24 | `pipelined_m:data_width=26,n_iter=20,angle_guard=1,frac_guard=2,rounding=round,m=8` | 1842 | 323 | 45.9 | 5 | 0.163 | 2.05e-06 (2^-18.89) | 18.89 |
| 25 | `pipelined_m:data_width=25,n_iter=21,angle_guard=3,frac_guard=1,rounding=round,m=8` | 1870 | 314 | 45.9 | 5 | 0.164 | 1.25e-06 (2^-19.60) | 19.60 |
| 26 | `pipelined_m:data_width=25,n_iter=24,angle_guard=2,frac_guard=3,rounding=round,m=7` | 2215 | 410 | 52.0 | 6 | 0.197 | 3.58e-07 (2^-21.41) | 21.41 |
| 27 | `pipelined_m:data_width=26,n_iter=25,angle_guard=1,frac_guard=2,rounding=trunc,m=7` | 2256 | 412 | 52.0 | 6 | 0.201 | 3.48e-07 (2^-21.45) | 21.45 |
| 28 | `pipelined_m:data_width=28,n_iter=23,angle_guard=0,frac_guard=3,rounding=trunc,m=7` | 2231 | 442 | 49.9 | 6 | 0.201 | 3.2e-07 (2^-21.58) | 21.58 |
| 29 | `pipelined_m:data_width=28,n_iter=23,angle_guard=2,frac_guard=3,rounding=trunc,m=7` | 2277 | 450 | 49.9 | 6 | 0.205 | 2.72e-07 (2^-21.81) | 21.81 |
| 30 | `pipelined_m:data_width=25,n_iter=24,angle_guard=4,frac_guard=4,rounding=round,m=7` | 2312 | 424 | 52.0 | 6 | 0.206 | 2.16e-07 (2^-22.14) | 22.14 |
| 31 | `pipelined_m:data_width=27,n_iter=24,angle_guard=3,frac_guard=3,rounding=round,m=7` | 2389 | 442 | 52.0 | 6 | 0.213 | 1.54e-07 (2^-22.63) | 22.63 |
| 32 | `pipelined_m:data_width=28,n_iter=24,angle_guard=4,frac_guard=3,rounding=trunc,m=7` | 2429 | 458 | 49.9 | 6 | 0.217 | 1.42e-07 (2^-22.74) | 22.74 |
| 33 | `pipelined_m:data_width=27,n_iter=25,angle_guard=3,frac_guard=3,rounding=round,m=7` | 2490 | 442 | 52.0 | 6 | 0.221 | 1.04e-07 (2^-23.20) | 23.20 |
| 34 | `pipelined_m:data_width=28,n_iter=28,angle_guard=2,frac_guard=3,rounding=trunc,m=2` | 2793 | 1449 | 147.4 | 16 | 0.319 | 5.37e-08 (2^-24.15) | 24.15 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Binding constraints are accuracy (max_abs_err <= 2^-10, i.e. accuracy_bits >= 10) and the system p99 latency of 0.4 us for 8-request bursts; the 2 msps throughput floor is met by every family and is not binding. Because a burst arrives 0 ns apart, the p99 latency is dominated by burst drain time ~ 7/throughput plus pipeline latency, so families that retire ~1 result/cycle (pipelined, pipelined_m) or k results/cycle (unrolled_k, k>=4) are strongly favoured, while iterative (N+3 cycles/result) is borderline-to-infeasible and gets only a small probe. The objective is min luts_plus_ffs, so the search is weighted toward pipelined_m (fewest pipeline registers for a given N) and unrolled_k (shared datapath), with plain pipelined kept for Fmax/latency safety and front coverage. Accuracy ranges are centred where 10 bits is reachable: data_width 10..20 (output LSB 2^-(W-2), so W>=11 with rounding), n_iter 8..20 (residual angle error ~2^-N), angle_guard -1..3 and frac_guard 0..3 to expose the accuracy-vs-area trade-off. Round 1 is a broad sweep of these four families; later rounds will narrow around the feasible front and use the reserved budget to map it over the full ranges of the families that actually appear on it.*)
- `pipelined_m` (35 evals): data_width=10..20, n_iter=8..20, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* Best candidate for the min-luts_plus_ffs objective: still 1 result/cycle (so burst drain is ~1 cycle/req and the p99 screen is easy), but registers only every m stages, so FF count drops roughly by m versus plain pipelined. m is the key knob trading Fmax/latency against area; sweep it fully (2..8) to find the area-optimal feasible point.
- `unrolled_k` (30 evals): data_width=10..20, n_iter=8..20, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, k=2..8. *Why:* Shares one datapath (low LUTs) while k micro-rotations/cycle gives throughput Fmax*k/(ceil(N/k)+3), which is enough to drain an 8-burst well inside 0.4 us for k>=4. This is the main alternative area point to pipelined_m; k is the throughput/area knob and must be swept.
- `pipelined` (25 evals): data_width=10..20, n_iter=8..20, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* Highest Fmax and 1 result/cycle, so it is the safest family for the p99 latency screen and anchors the high-accuracy / high-throughput end of the front. It costs the most FFs (a register per stage), so it is unlikely to win min luts_plus_ffs, but it is needed to cover the trade-off curve for hypervolume.
- `iterative` (10 evals): data_width=10..20, n_iter=8..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* Cheapest family in LUTs+FFs (one shared datapath), so if it can pass the p99 screen it would dominate the selection rule. But N+3 cycles/result means an 8-burst drains in ~7*(N+3)/Fmax cycles, which is right at the 0.4 us edge for the N>=11 needed for 10-bit accuracy. Small probe only, to confirm/deny feasibility rather than to map the front.

**Result (code):** 100 evaluations this round, 100 total; 45 feasible; hypervolume 9041 (n/a).

**LLM decision:** `map_front` — Round 1 leaves a large, obviously under-mapped trade-off curve, and the front families are now known so this is the right time to map it broadly. Evidence: 45/100 feasible, but the front has only 8 designs and is clustered — five pipelined_m points packed into luts_plus_ffs 1109..1508, then a single pipelined point at 2724, i.e. an almost empty band ~1500..2700 that HV (ref luts_plus_ffs=3000) rewards filling. The accuracy objective spans only 11.7..15.6 bits even though the registry allows data_width up to 28 and the HV reference is 10, so the entire high-accuracy end of the curve is unexplored; data_width on the front is only 17..20 of the registry's 8..28. iterative and unrolled_k are dead ends here (0 feasible, max 18.5/11.7 MSPS, cannot drain an 8-request zero-spacing burst inside the 0.4 us p99 bound), so the front families are exactly pipelined and pipelined_m. Running NSGA-II over the full ranges of those two families, seeded with the current front, should both span the accuracy range and fill the 1500..2700 area gap, raising hypervolume well beyond 9041. No infeasibility: the binding constraints are met with margin (best max_abs_err 2^-15.58 vs 2^-10; best sys_p99 0.0568 us vs 0.4; throughput 282 vs 2), and low-area pipelined_m designs sit safely inside the L1 latency bound, so the front is not at risk of being emptied at L2.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 9041 (gain this round: n/a (first round)).
Feasible designs: 45 of 100 evaluations (41 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 34% violate; best seen 2.04e-05 (2^-15.58)
- sys_p99_latency_us <= 0.4: 40% violate; best seen 0.0568

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1109, accuracy_bits=11.7, luts=890, ffs=219, throughput_msps=65.4, max_abs_err=0.000307 (2^-11.67), power_index=0.0835
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1220, accuracy_bits=13.2, luts=979, ffs=241, throughput_msps=65.4, max_abs_err=0.000109 (2^-13.17), power_index=0.0918
- pipelined_m [data_width=20 n_iter=15 angle_guard=2 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1258, accuracy_bits=13.5, luts=1008, ffs=249, throughput_msps=65.4, max_abs_err=8.43e-05 (2^-13.53), power_index=0.0946
- pipelined_m [data_width=20 n_iter=15 angle_guard=0 frac_guard=2 rounding=trunc m=5] luts_plus_ffs=1289, accuracy_bits=13.6, luts=1038, ffs=251, throughput_msps=77, max_abs_err=7.88e-05 (2^-13.63), power_index=0.097
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=2 rounding=round m=6] luts_plus_ffs=1329, accuracy_bits=13.8, luts=1078, ffs=251, throughput_msps=65.4, max_abs_err=7.06e-05 (2^-13.79), power_index=0.1
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1452, accuracy_bits=14.4, luts=1205, ffs=246, throughput_msps=65.4, max_abs_err=4.51e-05 (2^-14.44), power_index=0.109
- pipelined_m [data_width=19 n_iter=18 angle_guard=3 frac_guard=2 rounding=trunc m=6] luts_plus_ffs=1508, accuracy_bits=15.1, luts=1259, ffs=249, throughput_msps=65.4, max_abs_err=2.81e-05 (2^-15.12), power_index=0.113
- pipelined [data_width=20 n_iter=19 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=2724, accuracy_bits=15.6, luts=1352, ffs=1372, throughput_msps=264, max_abs_err=2.04e-05 (2^-15.58), power_index=0.205
Front coverage: luts_plus_ffs 1109..2724 (HV reference 3000); accuracy_bits 11.7..15.6 (HV reference 10); data_width on the front 17..20 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 18.5 MSPS; best accuracy 11.12 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 11.7 MSPS; best accuracy 14.48 bits
- pipelined: 25 evals, 17 feasible; max throughput seen 282 MSPS; best accuracy 15.58 bits; best feasible luts_plus_ffs=1384; feasible ranges: data_width 16..20, n_iter 13..19, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 35 evals, 28 feasible; max throughput seen 178 MSPS; best accuracy 15.12 bits; best feasible luts_plus_ffs=1109; feasible ranges: data_width 15..20, n_iter 12..18, angle_guard -1..3, frac_guard 0..3, m 2..6
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (88 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (7 front designs; box front_anchored)
- `pipelined` (12 evals): data_width=19..28, n_iter=17..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 144 feasible; hypervolume 1.44e+04 (+59.3%).

**LLM decision:** `map_front` — Round 2 leaves 200 of 400 evals and the front is now essentially single-family: all 25 Pareto designs are pipelined_m, while pipelined's best feasible luts_plus_ffs=1384 is dominated and iterative/unrolled_k produced 0 feasible designs (max throughput 18.5 and 11.7 MSPS, both below the 2 MSPS constraint only marginally but with no feasible point). The front already spans luts_plus_ffs 909..2932 against the HV ref 3000 and accuracy_bits 11.5..23.2 against ref 10, so the remaining budget is best spent mapping the whole trade-off curve over the full ranges of the family that owns it (pipelined_m, feasible ranges data_width 15..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8) rather than narrowing around a single corner. The min-area corner (909 LUT+FF, throughput 59.6 MSPS, sys_p99 0.0568 us best seen) is far inside the throughput/latency constraints, so the L2 burst simulation risk is low and coverage, not feasibility, is the limiting factor for hypervolume.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.44e+04 (gain this round: +59.3%).
Feasible designs: 144 of 200 evaluations (135 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 18% violate; best seen 1.04e-07 (2^-23.20)
- sys_p99_latency_us <= 0.4: 20% violate; best seen 0.0568

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=13 angle_guard=-1 frac_guard=0 rounding=round m=7] luts_plus_ffs=909, accuracy_bits=11.5, luts=751, ffs=157, throughput_msps=59.6, max_abs_err=0.000357 (2^-11.45), power_index=0.0684
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1220, accuracy_bits=13.2, luts=979, ffs=241, throughput_msps=65.4, max_abs_err=0.000109 (2^-13.17), power_index=0.0918
- pipelined_m [data_width=20 n_iter=15 angle_guard=2 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1258, accuracy_bits=13.5, luts=1008, ffs=249, throughput_msps=65.4, max_abs_err=8.43e-05 (2^-13.53), power_index=0.0946
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=2 rounding=round m=6] luts_plus_ffs=1329, accuracy_bits=13.8, luts=1078, ffs=251, throughput_msps=65.4, max_abs_err=7.06e-05 (2^-13.79), power_index=0.1
- pipelined_m [data_width=23 n_iter=17 angle_guard=0 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=1584, accuracy_bits=15.8, luts=1303, ffs=280, throughput_msps=54.3, max_abs_err=1.75e-05 (2^-15.80), power_index=0.119
- pipelined_m [data_width=25 n_iter=17 angle_guard=2 frac_guard=0 rounding=round m=7] luts_plus_ffs=1709, accuracy_bits=16, luts=1405, ffs=305, throughput_msps=52, max_abs_err=1.56e-05 (2^-15.97), power_index=0.129
- pipelined_m [data_width=25 n_iter=19 angle_guard=2 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=2010, accuracy_bits=17.9, luts=1693, ffs=317, throughput_msps=45.9, max_abs_err=3.99e-06 (2^-17.93), power_index=0.151
- pipelined_m [data_width=25 n_iter=24 angle_guard=2 frac_guard=3 rounding=round m=7] luts_plus_ffs=2625, accuracy_bits=21.4, luts=2215, ffs=410, throughput_msps=52, max_abs_err=3.58e-07 (2^-21.41), power_index=0.197
- pipelined_m [data_width=25 n_iter=24 angle_guard=4 frac_guard=4 rounding=round m=7] luts_plus_ffs=2736, accuracy_bits=22.1, luts=2312, ffs=424, throughput_msps=52, max_abs_err=2.16e-07 (2^-22.14), power_index=0.206
- pipelined_m [data_width=27 n_iter=25 angle_guard=3 frac_guard=3 rounding=round m=7] luts_plus_ffs=2932, accuracy_bits=23.2, luts=2490, ffs=442, throughput_msps=52, max_abs_err=1.04e-07 (2^-23.20), power_index=0.221
Front coverage: luts_plus_ffs 909..2932 (HV reference 3000); accuracy_bits 11.5..23.2 (HV reference 10); data_width on the front 17..28 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 18.5 MSPS; best accuracy 11.12 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 11.7 MSPS; best accuracy 14.48 bits
- pipelined: 37 evals, 29 feasible; max throughput seen 282 MSPS; best accuracy 20.89 bits; best feasible luts_plus_ffs=1384; feasible ranges: data_width 16..27, n_iter 13..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 123 evals, 115 feasible; max throughput seen 178 MSPS; best accuracy 23.20 bits; best feasible luts_plus_ffs=909; feasible ranges: data_width 15..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=16..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (25 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 300 total; 242 feasible; hypervolume 1.471e+04 (+2.2%).

**LLM decision:** `map_front` — All four families have now been explored (registry: 'Not yet explored: none'), and the feasible front is essentially single-family: pipelined_m supplied 213 of 223 feasible evals and every one of the 35 front points shown, while iterative (10 evals, 0 feasible) and unrolled_k (30 evals, 0 feasible) cannot meet the constraints at all, and pipelined's best feasible luts_plus_ffs (1384) is dominated by pipelined_m's 909. So there is no new family to add and no obviously over-tight range to widen. The front spans luts_plus_ffs 909..4242 and accuracy_bits 11.5..24.2, but the HV reference point is (3000, 10): the low-accuracy end of the front stops at 11.5 bits, so the strip accuracy_bits 10..11.5 at area below 909 is unmapped and is exactly where extra hypervolume is available, and the data_width range on the front (18..28) leaves the registry's 8..17 unused. With one round (100 evals) left and a reserved budget for front mapping, the best use is to let NSGA-II sweep the full ranges of the families on the front (pipelined_m, plus pipelined for the mid-range) seeded with the current front, rather than refining a narrow region. The +2.2% HV gain this round shows the front is still moving, so a full-range mapping pass is more valuable than a local refine.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.471e+04 (gain this round: +2.2%).
Feasible designs: 242 of 300 evaluations (224 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 12% violate; best seen 5.37e-08 (2^-24.15)
- sys_p99_latency_us <= 0.4: 13% violate; best seen 0.0568

Pareto front (feasible, 35 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=13 angle_guard=-1 frac_guard=0 rounding=round m=7] luts_plus_ffs=909, accuracy_bits=11.5, luts=751, ffs=157, throughput_msps=59.6, max_abs_err=0.000357 (2^-11.45), power_index=0.0684
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1220, accuracy_bits=13.2, luts=979, ffs=241, throughput_msps=65.4, max_abs_err=0.000109 (2^-13.17), power_index=0.0918
- pipelined_m [data_width=18 n_iter=15 angle_guard=4 frac_guard=2 rounding=round m=7] luts_plus_ffs=1290, accuracy_bits=13.7, luts=1046, ffs=243, throughput_msps=56.8, max_abs_err=7.73e-05 (2^-13.66), power_index=0.097
- pipelined_m [data_width=20 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc m=8] luts_plus_ffs=1419, accuracy_bits=14.8, luts=1169, ffs=250, throughput_msps=50.3, max_abs_err=3.57e-05 (2^-14.78), power_index=0.107
- pipelined_m [data_width=25 n_iter=17 angle_guard=2 frac_guard=0 rounding=round m=8] luts_plus_ffs=1709, accuracy_bits=16, luts=1405, ffs=305, throughput_msps=45.9, max_abs_err=1.56e-05 (2^-15.97), power_index=0.129
- pipelined_m [data_width=25 n_iter=19 angle_guard=2 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=2010, accuracy_bits=17.9, luts=1693, ffs=317, throughput_msps=45.9, max_abs_err=3.99e-06 (2^-17.93), power_index=0.151
- pipelined_m [data_width=26 n_iter=20 angle_guard=-1 frac_guard=1 rounding=round m=5] luts_plus_ffs=2161, accuracy_bits=18.6, luts=1762, ffs=400, throughput_msps=70.6, max_abs_err=2.52e-06 (2^-18.60), power_index=0.163
- pipelined_m [data_width=25 n_iter=24 angle_guard=2 frac_guard=3 rounding=round m=7] luts_plus_ffs=2625, accuracy_bits=21.4, luts=2215, ffs=410, throughput_msps=52, max_abs_err=3.58e-07 (2^-21.41), power_index=0.197
- pipelined_m [data_width=25 n_iter=24 angle_guard=4 frac_guard=4 rounding=round m=7] luts_plus_ffs=2736, accuracy_bits=22.1, luts=2312, ffs=424, throughput_msps=52, max_abs_err=2.16e-07 (2^-22.14), power_index=0.206
- pipelined_m [data_width=28 n_iter=28 angle_guard=2 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=4242, accuracy_bits=24.2, luts=2793, ffs=1449, throughput_msps=147, max_abs_err=5.37e-08 (2^-24.15), power_index=0.319
Front coverage: luts_plus_ffs 909..4242 (HV reference 3000); accuracy_bits 11.5..24.2 (HV reference 10); data_width on the front 18..28 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 18.5 MSPS; best accuracy 11.12 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 11.7 MSPS; best accuracy 14.48 bits
- pipelined: 37 evals, 29 feasible; max throughput seen 282 MSPS; best accuracy 20.89 bits; best feasible luts_plus_ffs=1384; feasible ranges: data_width 16..27, n_iter 13..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 223 evals, 213 feasible; max throughput seen 178 MSPS; best accuracy 24.15 bits; best feasible luts_plus_ffs=909; feasible ranges: data_width 15..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=17..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (35 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 339 feasible; hypervolume 1.534e+04 (+4.3%).

**LLM decision:** `stop` — Budget is exhausted (400/400 evals, round 4 of 4) and the run is at its cap, so no further exploration is possible. The feasible front is well mapped: 339/400 evaluations feasible, 35 Pareto designs spanning luts_plus_ffs 909..4242 and accuracy_bits 11.5..24.2, with hypervolume 1.534e+04 (+4.3% this round, a small gain indicating convergence). All constraints are comfortably met by many designs: throughput best 282 MSPS vs >=2 required, max_abs_err best 2^-24.15 vs <=2^-10 required, sys_p99_latency_us best 0.0568 us vs <=0.4 us required. The selection rule (min luts_plus_ffs) picks the pipelined_m design at 909 LUTs+FFs, accuracy 11.5 bits, which satisfies every constraint with margin. No family is unexplored and no constraint is unreachable, so the front is good enough to stop.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.534e+04 (gain this round: +4.3%).
Feasible designs: 339 of 400 evaluations (315 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 10% violate; best seen 5.37e-08 (2^-24.15)
- sys_p99_latency_us <= 0.4: 10% violate; best seen 0.0568

Pareto front (feasible, 35 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=13 angle_guard=-1 frac_guard=0 rounding=round m=7] luts_plus_ffs=909, accuracy_bits=11.5, luts=751, ffs=157, throughput_msps=59.6, max_abs_err=0.000357 (2^-11.45), power_index=0.0684
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1220, accuracy_bits=13.2, luts=979, ffs=241, throughput_msps=65.4, max_abs_err=0.000109 (2^-13.17), power_index=0.0918
- pipelined_m [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=trunc m=8] luts_plus_ffs=1381, accuracy_bits=14.3, luts=1135, ffs=246, throughput_msps=50.3, max_abs_err=4.89e-05 (2^-14.32), power_index=0.104
- pipelined_m [data_width=21 n_iter=17 angle_guard=1 frac_guard=2 rounding=trunc m=6] luts_plus_ffs=1518, accuracy_bits=15.5, luts=1253, ffs=265, throughput_msps=62.5, max_abs_err=2.11e-05 (2^-15.53), power_index=0.114
- pipelined_m [data_width=21 n_iter=19 angle_guard=3 frac_guard=1 rounding=round m=5] luts_plus_ffs=1798, accuracy_bits=16.8, luts=1453, ffs=345, throughput_msps=73.7, max_abs_err=8.82e-06 (2^-16.79), power_index=0.135
- pipelined_m [data_width=26 n_iter=20 angle_guard=-2 frac_guard=2 rounding=round m=8] luts_plus_ffs=2096, accuracy_bits=18.2, luts=1782, ffs=314, throughput_msps=45.9, max_abs_err=3.27e-06 (2^-18.22), power_index=0.158
- pipelined_m [data_width=26 n_iter=20 angle_guard=-1 frac_guard=1 rounding=round m=5] luts_plus_ffs=2161, accuracy_bits=18.6, luts=1762, ffs=400, throughput_msps=70.6, max_abs_err=2.52e-06 (2^-18.60), power_index=0.163
- pipelined_m [data_width=25 n_iter=24 angle_guard=2 frac_guard=3 rounding=round m=7] luts_plus_ffs=2625, accuracy_bits=21.4, luts=2215, ffs=410, throughput_msps=52, max_abs_err=3.58e-07 (2^-21.41), power_index=0.197
- pipelined_m [data_width=25 n_iter=24 angle_guard=4 frac_guard=4 rounding=round m=7] luts_plus_ffs=2736, accuracy_bits=22.1, luts=2312, ffs=424, throughput_msps=52, max_abs_err=2.16e-07 (2^-22.14), power_index=0.206
- pipelined_m [data_width=28 n_iter=28 angle_guard=2 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=4242, accuracy_bits=24.2, luts=2793, ffs=1449, throughput_msps=147, max_abs_err=5.37e-08 (2^-24.15), power_index=0.319
Front coverage: luts_plus_ffs 909..4242 (HV reference 3000); accuracy_bits 11.5..24.2 (HV reference 10); data_width on the front 17..28 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 18.5 MSPS; best accuracy 11.12 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 11.7 MSPS; best accuracy 14.48 bits
- pipelined: 37 evals, 29 feasible; max throughput seen 282 MSPS; best accuracy 20.89 bits; best feasible luts_plus_ffs=1384; feasible ranges: data_width 16..27, n_iter 13..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 323 evals, 310 feasible; max throughput seen 178 MSPS; best accuracy 24.15 bits; best feasible luts_plus_ffs=909; feasible ranges: data_width 15..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 31374 in, 14236 out
- provider-reported cost: $0.0172
- full prompts and replies: `llm_trace.jsonl`

