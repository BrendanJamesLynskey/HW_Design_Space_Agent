# DSE run: bursty_offload

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 5 round(s).  
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
`pipelined_m:data_width=15,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=7` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 718 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 137 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 59.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 59.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 67.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0643 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000632 (2^-10.63) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 5.18 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000164 (2^-12.58) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.34 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.6 | exact: bit-accurate model, exhaustive (32768 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 4 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 83.9 dBc, SNR 73.5 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: bursty requests: bursts of 8 (0 ns apart) arriving as a Poisson process, 2 requests/us on average. Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_latency_us <= 0.4 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=15,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=7` | 0.1678 → 0.2328 | yes |
| `pipelined_m:data_width=16,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=8` | 0.1896 → 0.2667 | yes |
| `pipelined_m:data_width=17,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=8` | 0.1896 → 0.2667 | yes |
| `pipelined_m:data_width=18,n_iter=14,angle_guard=-1,frac_guard=0,rounding=round,m=8` | 0.1896 → 0.2667 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=8` | 0.1896 → 0.2667 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (38 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=7` | 718 | 137 | 59.6 | 4 | 0.0643 | 0.000632 (2^-10.63) | 10.63 |
| 1 | `pipelined_m:data_width=16,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=8` | 759 | 145 | 52.7 | 4 | 0.068 | 0.000342 (2^-11.51) | 11.51 |
| 2 | `pipelined_m:data_width=17,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=8` | 786 | 151 | 52.7 | 4 | 0.0705 | 0.000301 (2^-11.70) | 11.70 |
| 3 | `pipelined_m:data_width=18,n_iter=14,angle_guard=-1,frac_guard=0,rounding=round,m=8` | 813 | 157 | 52.7 | 4 | 0.073 | 0.000248 (2^-11.98) | 11.98 |
| 4 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=8` | 861 | 153 | 52.7 | 4 | 0.0763 | 0.000168 (2^-12.54) | 12.54 |
| 5 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=8` | 920 | 163 | 50.3 | 4 | 0.0815 | 0.000109 (2^-13.17) | 13.17 |
| 6 | `pipelined_m:data_width=20,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=8` | 994 | 178 | 50.3 | 4 | 0.0881 | 7.63e-05 (2^-13.68) | 13.68 |
| 7 | `pipelined_m:data_width=20,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=8` | 1008 | 180 | 50.3 | 4 | 0.0894 | 7.03e-05 (2^-13.80) | 13.80 |
| 8 | `pipelined_m:data_width=20,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=8` | 1080 | 180 | 50.3 | 4 | 0.0948 | 4.12e-05 (2^-14.57) | 14.57 |
| 9 | `pipelined_m:data_width=20,n_iter=16,angle_guard=1,frac_guard=2,rounding=round,m=8` | 1170 | 184 | 50.3 | 4 | 0.102 | 3.84e-05 (2^-14.67) | 14.67 |
| 10 | `pipelined_m:data_width=22,n_iter=17,angle_guard=-1,frac_guard=0,rounding=round,m=8` | 1202 | 262 | 50.3 | 5 | 0.11 | 2.61e-05 (2^-15.23) | 15.23 |
| 11 | `pipelined_m:data_width=22,n_iter=17,angle_guard=-1,frac_guard=2,rounding=trunc,m=6` | 1270 | 270 | 62.5 | 5 | 0.116 | 2.37e-05 (2^-15.36) | 15.36 |
| 12 | `pipelined_m:data_width=22,n_iter=17,angle_guard=-1,frac_guard=2,rounding=trunc,m=8` | 1270 | 270 | 48.0 | 5 | 0.116 | 2.37e-05 (2^-15.36) | 15.36 |
| 13 | `pipelined_m:data_width=22,n_iter=19,angle_guard=-1,frac_guard=0,rounding=trunc,m=8` | 1352 | 262 | 50.3 | 5 | 0.121 | 1.72e-05 (2^-15.83) | 15.83 |
| 14 | `pipelined_m:data_width=22,n_iter=17,angle_guard=4,frac_guard=3,rounding=trunc,m=8` | 1388 | 290 | 48.0 | 5 | 0.126 | 1.68e-05 (2^-15.86) | 15.86 |
| 15 | `pipelined_m:data_width=22,n_iter=19,angle_guard=0,frac_guard=0,rounding=round,m=6` | 1371 | 339 | 65.4 | 6 | 0.129 | 1.07e-05 (2^-16.51) | 16.51 |
| 16 | `pipelined_m:data_width=24,n_iter=18,angle_guard=3,frac_guard=1,rounding=trunc,m=7` | 1492 | 301 | 52.0 | 5 | 0.135 | 8.61e-06 (2^-16.83) | 16.83 |
| 17 | `pipelined_m:data_width=25,n_iter=18,angle_guard=2,frac_guard=0,rounding=round,m=8` | 1492 | 305 | 45.9 | 5 | 0.135 | 7.98e-06 (2^-16.94) | 16.94 |
| 18 | `pipelined_m:data_width=25,n_iter=18,angle_guard=2,frac_guard=1,rounding=round,m=8` | 1581 | 311 | 45.9 | 5 | 0.142 | 7.83e-06 (2^-16.96) | 16.96 |
| 19 | `pipelined_m:data_width=24,n_iter=21,angle_guard=-1,frac_guard=0,rounding=trunc,m=7` | 1628 | 285 | 54.3 | 5 | 0.144 | 4.38e-06 (2^-17.80) | 17.80 |
| 20 | `pipelined_m:data_width=24,n_iter=20,angle_guard=3,frac_guard=0,rounding=round,m=8` | 1627 | 297 | 45.9 | 5 | 0.145 | 2.8e-06 (2^-18.44) | 18.44 |
| 21 | `pipelined_m:data_width=24,n_iter=20,angle_guard=3,frac_guard=0,rounding=round,m=7` | 1627 | 297 | 52.0 | 5 | 0.145 | 2.8e-06 (2^-18.44) | 18.44 |
| 22 | `pipelined_m:data_width=24,n_iter=20,angle_guard=3,frac_guard=2,rounding=round,m=7` | 1758 | 307 | 52.0 | 5 | 0.155 | 2.22e-06 (2^-18.78) | 18.78 |
| 23 | `pipelined_m:data_width=23,n_iter=21,angle_guard=4,frac_guard=3,rounding=trunc,m=6` | 1797 | 387 | 59.9 | 6 | 0.164 | 1.81e-06 (2^-19.08) | 19.08 |
| 24 | `pipelined_m:data_width=24,n_iter=21,angle_guard=3,frac_guard=4,rounding=trunc,m=8` | 1881 | 313 | 45.9 | 5 | 0.165 | 1.37e-06 (2^-19.47) | 19.47 |
| 25 | `pipelined_m:data_width=24,n_iter=21,angle_guard=4,frac_guard=3,rounding=round,m=6` | 1910 | 404 | 59.9 | 6 | 0.174 | 1.22e-06 (2^-19.64) | 19.64 |
| 26 | `pipelined_m:data_width=24,n_iter=23,angle_guard=3,frac_guard=2,rounding=round,m=8` | 2026 | 307 | 45.9 | 5 | 0.176 | 5.75e-07 (2^-20.73) | 20.73 |
| 27 | `pipelined_m:data_width=25,n_iter=24,angle_guard=2,frac_guard=2,rounding=round,m=8` | 2167 | 315 | 45.9 | 5 | 0.187 | 4.21e-07 (2^-21.18) | 21.18 |
| 28 | `pipelined_m:data_width=25,n_iter=24,angle_guard=2,frac_guard=3,rounding=round,m=8` | 2215 | 319 | 45.9 | 5 | 0.191 | 3.58e-07 (2^-21.41) | 21.41 |
| 29 | `pipelined_m:data_width=26,n_iter=23,angle_guard=3,frac_guard=4,rounding=trunc,m=8` | 2208 | 335 | 45.9 | 5 | 0.191 | 3.3e-07 (2^-21.53) | 21.53 |
| 30 | `pipelined_m:data_width=28,n_iter=24,angle_guard=-1,frac_guard=1,rounding=trunc,m=8` | 2211 | 333 | 45.9 | 5 | 0.191 | 3.05e-07 (2^-21.64) | 21.64 |
| 31 | `pipelined_m:data_width=28,n_iter=24,angle_guard=1,frac_guard=1,rounding=trunc,m=8` | 2259 | 339 | 45.9 | 5 | 0.195 | 2.18e-07 (2^-22.13) | 22.13 |
| 32 | `pipelined_m:data_width=28,n_iter=24,angle_guard=3,frac_guard=1,rounding=round,m=8` | 2367 | 347 | 44.0 | 5 | 0.204 | 1.53e-07 (2^-22.64) | 22.64 |
| 33 | `pipelined_m:data_width=28,n_iter=26,angle_guard=1,frac_guard=0,rounding=round,m=5` | 2403 | 613 | 70.6 | 8 | 0.227 | 1.47e-07 (2^-22.70) | 22.70 |
| 34 | `pipelined_m:data_width=28,n_iter=24,angle_guard=3,frac_guard=4,rounding=trunc,m=5` | 2453 | 563 | 67.8 | 7 | 0.227 | 1.43e-07 (2^-22.74) | 22.74 |
| 35 | `pipelined_m:data_width=27,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc,m=6` | 2534 | 538 | 59.9 | 7 | 0.231 | 9.63e-08 (2^-23.31) | 23.31 |
| 36 | `pipelined_m:data_width=28,n_iter=26,angle_guard=2,frac_guard=4,rounding=trunc,m=3` | 2640 | 966 | 105.9 | 11 | 0.271 | 7.02e-08 (2^-23.76) | 23.76 |
| 37 | `pipelined_m:data_width=28,n_iter=26,angle_guard=2,frac_guard=4,rounding=round,m=2` | 2699 | 1375 | 147.4 | 15 | 0.306 | 6.35e-08 (2^-23.91) | 23.91 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec has three constraints: throughput >= 2 MSpS, max_abs_err <= 2^-10, and sys_p99_latency <= 0.4 us. The bursty nature (8 requests 0 ns apart, Poisson 2 req/us) makes latency the critical constraint. Iterative is the area-min favorite from prior campaigns but risks p99 violation due to queue buildup. Pipelined is the latency-safe choice (1 result/cycle, short latency) but costs more area. Unrolled_k is a middle ground. I'm allocating 50% to iterative (most likely area-min winner if it passes latency), 30% to pipelined (most likely to pass latency), and 20% to unrolled_k (potential trade-off point). All families search data_width 12-20 (enough for 10-bit accuracy), n_iter 8-16 (balance accuracy vs latency/area), and truncation preferred for area. The L1 analytic bound will screen for p99 latency, and L2 simulation will re-select among the shortlist.*)
- `iterative` (50 evals): data_width=12..20, n_iter=8..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Prior campaigns show iterative reaches the front for area-min specs. The p99 latency constraint (0.4us) is tight for iterative (N+3 cycles), but with high Fmax (e.g., 200+ MHz) and small N, it may just meet the bound. The bursty nature means queue buildup is the risk, but the L1 analytic bound will screen this. Focusing on lower n_iter (8-16) and moderate data_width (12-20) to balance area vs accuracy (need >=10 bits). Truncation is preferred for area savings.
- `pipelined` (30 evals): data_width=12..20, n_iter=8..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Pipelined has 1 result/cycle throughput and N+2 latency. For bursty traffic, this is ideal: it can drain an 8-deep burst in 8 cycles. With Fmax ~150-200 MHz, 8 cycles = 40-53 ns, well within 0.4 us p99. Area is higher than iterative due to pipeline registers, but the latency constraint may force this family. Searching same parameter space as iterative to compare trade-offs.
- `unrolled_k` (20 evals): data_width=12..20, n_iter=8..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Unrolled_k with k=2-4 gives ceil(N/k)+3 cycles. For N=12, k=4: 6 cycles. This is a middle ground between iterative and pipelined. Throughput is 1 result per ceil(N/k) cycles, so for k=4, N=12, it's 1 result/3 cycles = 333 MSpS at 1 GHz, but realistically limited by Fmax. The latency is shorter than iterative, which helps with bursty p99. Area is between iterative and pipelined. Worth exploring as a potential Pareto point.

**Result (code):** 100 evaluations this round, 100 total; 15 feasible; hypervolume 3705 (n/a).

**LLM decision:** `add_family` — The current Pareto front is dominated entirely by the `pipelined` family, which has a high fixed latency (N+2 cycles). The system constraint `sys_p99_latency_us <= 0.4` is tight (70% of evaluations violated it in Round 1), and the best feasible design has a latency of 16 cycles (14+2). At the observed Fmax (~273 MHz), 16 cycles is ~58.6 ns, which is well within the 400 ns budget, but the `pipelined` architecture's area (LUTs+FFs) is high because it registers every stage. The `pipelined_m` family allows registering every m stages, which can significantly reduce FF count (and thus `luts_plus_ffs`) while maintaining 1 result/cycle throughput. Since `pipelined_m` has not been explored yet, and the goal is to minimize `luts_plus_ffs` while meeting the strict latency and accuracy constraints, exploring `pipelined_m` is the logical next step to find a potentially cheaper design on the Pareto front. The `iterative` and `unrolled_k` families were infeasible due to throughput, so they are not candidates for refinement.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 3705 (gain this round: n/a (first round)).
Feasible designs: 15 of 100 evaluations (15 unique).
Families explored so far: iterative, unrolled_k, pipelined. Not yet explored: pipelined_m.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 50% violate; best seen 7.18e-05 (2^-13.77)
- sys_p99_latency_us <= 0.4: 70% violate; best seen 0.0586

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=1438, accuracy_bits=10.3, luts=704, ffs=734, throughput_msps=273, max_abs_err=0.00081 (2^-10.27), power_index=0.108
- pipelined [data_width=15 n_iter=14 angle_guard=0 frac_guard=1 rounding=round] luts_plus_ffs=1524, accuracy_bits=10.3, luts=763, ffs=761, throughput_msps=273, max_abs_err=0.000767 (2^-10.35), power_index=0.115
- pipelined [data_width=15 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=1579, accuracy_bits=11.3, luts=790, ffs=789, throughput_msps=273, max_abs_err=0.000403 (2^-11.28), power_index=0.119
- pipelined [data_width=17 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=1605, accuracy_bits=11.7, luts=786, ffs=819, throughput_msps=273, max_abs_err=0.000301 (2^-11.70), power_index=0.121
- pipelined [data_width=16 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=1811, accuracy_bits=11.8, luts=890, ffs=920, throughput_msps=273, max_abs_err=0.000285 (2^-11.78), power_index=0.136
- pipelined [data_width=16 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=1906, accuracy_bits=12.5, luts=956, ffs=950, throughput_msps=273, max_abs_err=0.000177 (2^-12.47), power_index=0.143
- pipelined [data_width=20 n_iter=14 angle_guard=0 frac_guard=1 rounding=round] luts_plus_ffs=1952, accuracy_bits=12.9, luts=979, ffs=973, throughput_msps=264, max_abs_err=0.000135 (2^-12.86), power_index=0.147
- pipelined [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=1966, accuracy_bits=12.9, luts=987, ffs=979, throughput_msps=273, max_abs_err=0.000134 (2^-12.86), power_index=0.148
Front coverage: luts_plus_ffs 1438..1966 (HV reference 3000); accuracy_bits 10.3..12.9 (HV reference 10); data_width on the front 15..20 (registry 8..28).

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 18 MSPS; best accuracy 13.77 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 15.8 MSPS; best accuracy 12.28 bits
- pipelined: 30 evals, 15 feasible; max throughput seen 282 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=1438; feasible ranges: data_width 15..20, n_iter 14..16, angle_guard -1..2, frac_guard 0..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Focus the remaining budget on exploring the unexplored pipelined_m family within the known feasible parameter space to potentially find a design with lower luts_plus_ffs than the current best (1438) while maintaining feasibility.*)
- `pipelined_m` (100 evals): data_width=15..20, n_iter=14..16, angle_guard=-1..2, frac_guard=0..2, rounding=round, m=2..8. *Why:* Explore pipelined_m to find lower area designs (fewer FFs) that still meet the 1 result/cycle throughput and strict latency/accuracy constraints. Ranges are narrowed to the feasible region identified in Round 1 for pipelined (data_width 15-20, n_iter 14-16, angle_guard -1 to 2, frac_guard 0-2, rounding=round) to focus the search. m is explored over its full range 2-8 to find the optimal trade-off between area and latency.

**Result (code):** 100 evaluations this round, 200 total; 115 feasible; hypervolume 9126 (+146.3%).

**LLM decision:** `map_front` — The front is dominated by pipelined_m, which is strictly more efficient than pipelined (855 vs 1438 LUTs+FFs for similar accuracy) and the only family meeting the tight sys_p99_latency_us <= 0.4 us constraint. The current front covers luts_plus_ffs 855..1353 and accuracy_bits 10.6..14.7, but the registry allows data_width up to 28 and n_iter up to 30. Since the selection rule is min luts_plus_ffs and the hypervolume rewards covering the trade-off curve, we should let the code map the full feasible front to ensure we capture the true minimum area design and the full accuracy range, rather than manually refining ranges which might miss the global optimum or waste budget on already-dominated regions.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 9126 (gain this round: +146.3%).
Feasible designs: 115 of 200 evaluations (98 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 25% violate; best seen 3.84e-05 (2^-14.67)
- sys_p99_latency_us <= 0.4: 35% violate; best seen 0.0586

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=7] luts_plus_ffs=855, accuracy_bits=10.6, luts=718, ffs=137, throughput_msps=59.6, max_abs_err=0.000632 (2^-10.63), power_index=0.0643
- pipelined_m [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=8] luts_plus_ffs=904, accuracy_bits=11.5, luts=759, ffs=145, throughput_msps=52.7, max_abs_err=0.000342 (2^-11.51), power_index=0.068
- pipelined_m [data_width=17 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=8] luts_plus_ffs=937, accuracy_bits=11.7, luts=786, ffs=151, throughput_msps=52.7, max_abs_err=0.000301 (2^-11.70), power_index=0.0705
- pipelined_m [data_width=18 n_iter=14 angle_guard=-1 frac_guard=0 rounding=round m=8] luts_plus_ffs=971, accuracy_bits=12, luts=813, ffs=157, throughput_msps=52.7, max_abs_err=0.000248 (2^-11.98), power_index=0.073
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=8] luts_plus_ffs=1014, accuracy_bits=12.5, luts=861, ffs=153, throughput_msps=52.7, max_abs_err=0.000168 (2^-12.54), power_index=0.0763
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=8] luts_plus_ffs=1083, accuracy_bits=13.2, luts=920, ffs=163, throughput_msps=50.3, max_abs_err=0.000109 (2^-13.17), power_index=0.0815
- pipelined_m [data_width=20 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=8] luts_plus_ffs=1171, accuracy_bits=13.7, luts=994, ffs=178, throughput_msps=50.3, max_abs_err=7.63e-05 (2^-13.68), power_index=0.0881
- pipelined_m [data_width=20 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=8] luts_plus_ffs=1188, accuracy_bits=13.8, luts=1008, ffs=180, throughput_msps=50.3, max_abs_err=7.03e-05 (2^-13.80), power_index=0.0894
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=8] luts_plus_ffs=1260, accuracy_bits=14.6, luts=1080, ffs=180, throughput_msps=50.3, max_abs_err=4.12e-05 (2^-14.57), power_index=0.0948
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=round m=8] luts_plus_ffs=1353, accuracy_bits=14.7, luts=1170, ffs=184, throughput_msps=50.3, max_abs_err=3.84e-05 (2^-14.67), power_index=0.102
Front coverage: luts_plus_ffs 855..1353 (HV reference 3000); accuracy_bits 10.6..14.7 (HV reference 10); data_width on the front 15..20 (registry 8..28).

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 18 MSPS; best accuracy 13.77 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 15.8 MSPS; best accuracy 12.28 bits
- pipelined: 30 evals, 15 feasible; max throughput seen 282 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=1438; feasible ranges: data_width 15..20, n_iter 14..16, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 100 evals, 100 feasible; max throughput seen 171 MSPS; best accuracy 14.67 bits; best feasible luts_plus_ffs=855; feasible ranges: data_width 15..20, n_iter 14..16, angle_guard -1..2, frac_guard 0..2, m 2..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (10 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 240 total; 155 feasible; hypervolume 1.415e+04 (+55.0%).

**LLM decision:** `map_front` — The Pareto front is dominated by the `pipelined_m` family, which has achieved the best area (855 luts_plus_ffs) and the highest accuracy (23.9 bits) while satisfying all constraints. The `pipelined` family is also feasible but strictly worse in area (min 1438) and accuracy (max 12.86) compared to `pipelined_m`. `iterative` and `unrolled_k` are infeasible due to throughput constraints. The current front covers a wide range of the objective space (area 855..4074, accuracy 10.6..23.9) and the hypervolume has grown significantly (+55% in the last round). Since `pipelined_m` is the only family contributing to the high-accuracy and low-area ends of the front, and `pipelined` only contributes a small, inferior subset, the most effective use of the remaining budget (160 evals) is to let the code perform a dense NSGA-II search over the full parameter ranges of `pipelined_m` (and potentially `pipelined` for completeness, though it is unlikely to improve the front) to ensure the entire trade-off curve is mapped accurately before the final selection and L2 simulation.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 1.415e+04 (gain this round: +55.0%).
Feasible designs: 155 of 240 evaluations (135 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 21% violate; best seen 6.35e-08 (2^-23.91)
- sys_p99_latency_us <= 0.4: 29% violate; best seen 0.0586

Pareto front (feasible, 20 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=7] luts_plus_ffs=855, accuracy_bits=10.6, luts=718, ffs=137, throughput_msps=59.6, max_abs_err=0.000632 (2^-10.63), power_index=0.0643
- pipelined_m [data_width=17 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=8] luts_plus_ffs=937, accuracy_bits=11.7, luts=786, ffs=151, throughput_msps=52.7, max_abs_err=0.000301 (2^-11.70), power_index=0.0705
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=8] luts_plus_ffs=1014, accuracy_bits=12.5, luts=861, ffs=153, throughput_msps=52.7, max_abs_err=0.000168 (2^-12.54), power_index=0.0763
- pipelined_m [data_width=20 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=8] luts_plus_ffs=1171, accuracy_bits=13.7, luts=994, ffs=178, throughput_msps=50.3, max_abs_err=7.63e-05 (2^-13.68), power_index=0.0881
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=8] luts_plus_ffs=1260, accuracy_bits=14.6, luts=1080, ffs=180, throughput_msps=50.3, max_abs_err=4.12e-05 (2^-14.57), power_index=0.0948
- pipelined_m [data_width=19 n_iter=17 angle_guard=2 frac_guard=4 rounding=round m=5] luts_plus_ffs=1607, accuracy_bits=15.3, luts=1276, ffs=331, throughput_msps=73.7, max_abs_err=2.52e-05 (2^-15.28), power_index=0.121
- pipelined_m [data_width=25 n_iter=18 angle_guard=2 frac_guard=1 rounding=round m=8] luts_plus_ffs=1891, accuracy_bits=17, luts=1581, ffs=311, throughput_msps=45.9, max_abs_err=7.83e-06 (2^-16.96), power_index=0.142
- pipelined_m [data_width=28 n_iter=26 angle_guard=1 frac_guard=0 rounding=round m=5] luts_plus_ffs=3016, accuracy_bits=22.7, luts=2403, ffs=613, throughput_msps=70.6, max_abs_err=1.47e-07 (2^-22.70), power_index=0.227
- pipelined_m [data_width=28 n_iter=26 angle_guard=1 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=3570, accuracy_bits=23.3, luts=2613, ffs=956, throughput_msps=106, max_abs_err=9.68e-08 (2^-23.30), power_index=0.269
- pipelined_m [data_width=28 n_iter=26 angle_guard=2 frac_guard=4 rounding=round m=2] luts_plus_ffs=4074, accuracy_bits=23.9, luts=2699, ffs=1375, throughput_msps=147, max_abs_err=6.35e-08 (2^-23.91), power_index=0.306
Front coverage: luts_plus_ffs 855..4074 (HV reference 3000); accuracy_bits 10.6..23.9 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 18 MSPS; best accuracy 13.77 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 15.8 MSPS; best accuracy 12.28 bits
- pipelined: 30 evals, 15 feasible; max throughput seen 282 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=1438; feasible ranges: data_width 15..20, n_iter 14..16, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 140 evals, 140 feasible; max throughput seen 171 MSPS; best accuracy 23.91 bits; best feasible luts_plus_ffs=855; feasible ranges: data_width 15..28, n_iter 12..29, angle_guard -2..3, frac_guard 0..4, m 2..8
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (20 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 340 total; 252 feasible; hypervolume 1.631e+04 (+15.3%).

**LLM decision:** `stop` — The exploration is complete (Round 4 of 4, 340/400 evals used). The Pareto front is well-mapped across the full feasible range of the dominant family (pipelined_m), covering luts_plus_ffs from 855 to 4074 and accuracy_bits from 10.6 to 23.9. The front successfully satisfies all constraints: throughput is high (50-150+ MSPS vs 2 required), max_abs_err is well below the 2^-10 limit (best 2^-23.9), and sys_p99_latency_us is met (best 0.0586 us vs 0.4 us limit). The selection rule (min luts_plus_ffs) points to the pipelined_m design with data_width=15, n_iter=14, m=7, which achieves 855 LUTs+FFs and 10.6 bits of accuracy. Since this is the final round, no further refinement is possible or necessary.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 60 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 340 of 400.
Hypervolume of the feasible front: 1.631e+04 (gain this round: +15.3%).
Feasible designs: 252 of 340 evaluations (227 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 16% violate; best seen 6.35e-08 (2^-23.91)
- sys_p99_latency_us <= 0.4: 21% violate; best seen 0.0586

Pareto front (feasible, 38 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=7] luts_plus_ffs=855, accuracy_bits=10.6, luts=718, ffs=137, throughput_msps=59.6, max_abs_err=0.000632 (2^-10.63), power_index=0.0643
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=8] luts_plus_ffs=1014, accuracy_bits=12.5, luts=861, ffs=153, throughput_msps=52.7, max_abs_err=0.000168 (2^-12.54), power_index=0.0763
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=8] luts_plus_ffs=1260, accuracy_bits=14.6, luts=1080, ffs=180, throughput_msps=50.3, max_abs_err=4.12e-05 (2^-14.57), power_index=0.0948
- pipelined_m [data_width=22 n_iter=17 angle_guard=-1 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=1540, accuracy_bits=15.4, luts=1270, ffs=270, throughput_msps=48, max_abs_err=2.37e-05 (2^-15.36), power_index=0.116
- pipelined_m [data_width=24 n_iter=18 angle_guard=3 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=1793, accuracy_bits=16.8, luts=1492, ffs=301, throughput_msps=52, max_abs_err=8.61e-06 (2^-16.83), power_index=0.135
- pipelined_m [data_width=24 n_iter=20 angle_guard=3 frac_guard=0 rounding=round m=7] luts_plus_ffs=1924, accuracy_bits=18.4, luts=1627, ffs=297, throughput_msps=52, max_abs_err=2.8e-06 (2^-18.44), power_index=0.145
- pipelined_m [data_width=24 n_iter=21 angle_guard=4 frac_guard=3 rounding=round m=6] luts_plus_ffs=2314, accuracy_bits=19.6, luts=1910, ffs=404, throughput_msps=59.9, max_abs_err=1.22e-06 (2^-19.64), power_index=0.174
- pipelined_m [data_width=26 n_iter=23 angle_guard=3 frac_guard=4 rounding=trunc m=8] luts_plus_ffs=2543, accuracy_bits=21.5, luts=2208, ffs=335, throughput_msps=45.9, max_abs_err=3.3e-07 (2^-21.53), power_index=0.191
- pipelined_m [data_width=28 n_iter=26 angle_guard=1 frac_guard=0 rounding=round m=5] luts_plus_ffs=3016, accuracy_bits=22.7, luts=2403, ffs=613, throughput_msps=70.6, max_abs_err=1.47e-07 (2^-22.70), power_index=0.227
- pipelined_m [data_width=28 n_iter=26 angle_guard=2 frac_guard=4 rounding=round m=2] luts_plus_ffs=4074, accuracy_bits=23.9, luts=2699, ffs=1375, throughput_msps=147, max_abs_err=6.35e-08 (2^-23.91), power_index=0.306
Front coverage: luts_plus_ffs 855..4074 (HV reference 3000); accuracy_bits 10.6..23.9 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 18 MSPS; best accuracy 13.77 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 15.8 MSPS; best accuracy 12.28 bits
- pipelined: 30 evals, 15 feasible; max throughput seen 282 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=1438; feasible ranges: data_width 15..20, n_iter 14..16, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 240 evals, 237 feasible; max throughput seen 171 MSPS; best accuracy 23.91 bits; best feasible luts_plus_ffs=855; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

### Round 5

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 60 evaluations*)
- `pipelined_m` (60 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (38 front designs; box front_anchored)

**Result (code):** 60 evaluations this round, 400 total; 311 feasible; hypervolume 1.636e+04 (+0.3%).

**No LLM call** (code's front-mapping round): The exploration is complete (Round 4 of 4, 340/400 evals used). The Pareto front is well-mapped across the full feasible range of the dominant family (pipelined_m), covering luts_plus_ffs from 855 to 4074 and accuracy_bits from 10.6 to 23.9. The front successfully satisfies all constraints: throughput is high (50-150+ MSPS vs 2 required), max_abs_err is well below the 2^-10 limit (best 2^-23.9), and sys_p99_latency_us is met (best 0.0586 us vs 0.4 us limit). The selection rule (min luts_plus_ffs) points to the pipelined_m design with data_width=15, n_iter=14, m=7, which achieves 855 LUTs+FFs and 10.6 bits of accuracy. Since this is the final round, no further refinement is possible or necessary.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 5 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.636e+04 (gain this round: +0.3%).
Feasible designs: 311 of 400 evaluations (280 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 14% violate; best seen 6.35e-08 (2^-23.91)
- sys_p99_latency_us <= 0.4: 18% violate; best seen 0.0586

Pareto front (feasible, 38 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=7] luts_plus_ffs=855, accuracy_bits=10.6, luts=718, ffs=137, throughput_msps=59.6, max_abs_err=0.000632 (2^-10.63), power_index=0.0643
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=8] luts_plus_ffs=1014, accuracy_bits=12.5, luts=861, ffs=153, throughput_msps=52.7, max_abs_err=0.000168 (2^-12.54), power_index=0.0763
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=8] luts_plus_ffs=1260, accuracy_bits=14.6, luts=1080, ffs=180, throughput_msps=50.3, max_abs_err=4.12e-05 (2^-14.57), power_index=0.0948
- pipelined_m [data_width=22 n_iter=17 angle_guard=-1 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=1540, accuracy_bits=15.4, luts=1270, ffs=270, throughput_msps=48, max_abs_err=2.37e-05 (2^-15.36), power_index=0.116
- pipelined_m [data_width=24 n_iter=18 angle_guard=3 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=1793, accuracy_bits=16.8, luts=1492, ffs=301, throughput_msps=52, max_abs_err=8.61e-06 (2^-16.83), power_index=0.135
- pipelined_m [data_width=24 n_iter=20 angle_guard=3 frac_guard=0 rounding=round m=7] luts_plus_ffs=1924, accuracy_bits=18.4, luts=1627, ffs=297, throughput_msps=52, max_abs_err=2.8e-06 (2^-18.44), power_index=0.145
- pipelined_m [data_width=24 n_iter=21 angle_guard=4 frac_guard=3 rounding=round m=6] luts_plus_ffs=2314, accuracy_bits=19.6, luts=1910, ffs=404, throughput_msps=59.9, max_abs_err=1.22e-06 (2^-19.64), power_index=0.174
- pipelined_m [data_width=26 n_iter=23 angle_guard=3 frac_guard=4 rounding=trunc m=8] luts_plus_ffs=2543, accuracy_bits=21.5, luts=2208, ffs=335, throughput_msps=45.9, max_abs_err=3.3e-07 (2^-21.53), power_index=0.191
- pipelined_m [data_width=28 n_iter=26 angle_guard=1 frac_guard=0 rounding=round m=5] luts_plus_ffs=3016, accuracy_bits=22.7, luts=2403, ffs=613, throughput_msps=70.6, max_abs_err=1.47e-07 (2^-22.70), power_index=0.227
- pipelined_m [data_width=28 n_iter=26 angle_guard=2 frac_guard=4 rounding=round m=2] luts_plus_ffs=4074, accuracy_bits=23.9, luts=2699, ffs=1375, throughput_msps=147, max_abs_err=6.35e-08 (2^-23.91), power_index=0.306
Front coverage: luts_plus_ffs 855..4074 (HV reference 3000); accuracy_bits 10.6..23.9 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 18 MSPS; best accuracy 13.77 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 15.8 MSPS; best accuracy 12.28 bits
- pipelined: 30 evals, 15 feasible; max throughput seen 282 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=1438; feasible ranges: data_width 15..20, n_iter 14..16, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 300 evals, 296 feasible; max throughput seen 171 MSPS; best accuracy 23.91 bits; best feasible luts_plus_ffs=855; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 33584 in, 3429 out
- provider-reported cost: $0.0083
- full prompts and replies: `llm_trace.jsonl`

