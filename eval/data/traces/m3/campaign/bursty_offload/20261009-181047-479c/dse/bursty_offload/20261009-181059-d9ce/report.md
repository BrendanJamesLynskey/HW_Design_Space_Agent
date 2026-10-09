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
`pipelined_m:data_width=16,n_iter=13,angle_guard=4,frac_guard=0,rounding=trunc,m=7` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 739 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 151 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 56.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 56.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 70.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.067 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000704 (2^-10.47) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 11.5 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000148 (2^-12.73) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 2.42 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.5 | exact: bit-accurate model, exhaustive (65536 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 4 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 84.0 dBc, SNR 73.7 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: bursty requests: bursts of 8 (0 ns apart) arriving as a Poisson process, 2 requests/us on average. Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_latency_us <= 0.4 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=16,n_iter=13,angle_guard=4,frac_guard=0,rounding=trunc,m=7` | 0.1759 → 0.245 | yes |
| `pipelined_m:data_width=16,n_iter=14,angle_guard=0,frac_guard=1,rounding=trunc,m=8` | 0.1896 → 0.2667 | yes |
| `pipelined_m:data_width=16,n_iter=14,angle_guard=3,frac_guard=0,rounding=round,m=7` | 0.1759 → 0.245 | yes |
| `pipelined_m:data_width=19,n_iter=14,angle_guard=-1,frac_guard=0,rounding=trunc,m=7` | 0.1759 → 0.245 | yes |
| `pipelined_m:data_width=19,n_iter=14,angle_guard=0,frac_guard=1,rounding=trunc,m=7` | 0.1759 → 0.245 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (40 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=13,angle_guard=4,frac_guard=0,rounding=trunc,m=7` | 739 | 151 | 56.8 | 4 | 0.067 | 0.000704 (2^-10.47) | 10.47 |
| 1 | `pipelined_m:data_width=16,n_iter=14,angle_guard=0,frac_guard=1,rounding=trunc,m=8` | 772 | 145 | 52.7 | 4 | 0.069 | 0.000401 (2^-11.28) | 11.28 |
| 2 | `pipelined_m:data_width=16,n_iter=14,angle_guard=3,frac_guard=0,rounding=round,m=7` | 786 | 149 | 56.8 | 4 | 0.0704 | 0.000294 (2^-11.73) | 11.73 |
| 3 | `pipelined_m:data_width=19,n_iter=14,angle_guard=-1,frac_guard=0,rounding=trunc,m=7` | 855 | 165 | 56.8 | 4 | 0.0767 | 0.000193 (2^-12.34) | 12.34 |
| 4 | `pipelined_m:data_width=19,n_iter=14,angle_guard=0,frac_guard=1,rounding=trunc,m=7` | 896 | 169 | 56.8 | 4 | 0.0801 | 0.000158 (2^-12.63) | 12.63 |
| 5 | `pipelined_m:data_width=19,n_iter=14,angle_guard=3,frac_guard=2,rounding=trunc,m=7` | 964 | 178 | 56.8 | 4 | 0.0859 | 0.000136 (2^-12.85) | 12.85 |
| 6 | `pipelined_m:data_width=19,n_iter=14,angle_guard=3,frac_guard=4,rounding=trunc,m=8` | 1019 | 182 | 48.0 | 4 | 0.0903 | 0.00013 (2^-12.90) | 12.90 |
| 7 | `pipelined_m:data_width=22,n_iter=14,angle_guard=0,frac_guard=1,rounding=trunc,m=8` | 1019 | 194 | 48.0 | 4 | 0.0912 | 0.000126 (2^-12.95) | 12.95 |
| 8 | `pipelined_m:data_width=19,n_iter=16,angle_guard=-1,frac_guard=2,rounding=trunc,m=8` | 1048 | 169 | 50.3 | 4 | 0.0916 | 0.000103 (2^-13.25) | 13.25 |
| 9 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=3,rounding=trunc,m=7` | 994 | 236 | 56.8 | 5 | 0.0925 | 0.000102 (2^-13.26) | 13.26 |
| 10 | `pipelined_m:data_width=20,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc,m=7` | 1023 | 250 | 56.8 | 5 | 0.0958 | 7.76e-05 (2^-13.65) | 13.65 |
| 11 | `pipelined_m:data_width=20,n_iter=17,angle_guard=1,frac_guard=0,rounding=trunc,m=6` | 1135 | 246 | 65.4 | 5 | 0.104 | 4.89e-05 (2^-14.32) | 14.32 |
| 12 | `pipelined_m:data_width=20,n_iter=17,angle_guard=3,frac_guard=0,rounding=round,m=7` | 1169 | 252 | 54.3 | 5 | 0.107 | 2.95e-05 (2^-15.05) | 15.05 |
| 13 | `pipelined_m:data_width=21,n_iter=17,angle_guard=0,frac_guard=0,rounding=round,m=7` | 1169 | 254 | 56.8 | 5 | 0.107 | 2.7e-05 (2^-15.18) | 15.18 |
| 14 | `pipelined_m:data_width=22,n_iter=17,angle_guard=-1,frac_guard=0,rounding=round,m=7` | 1202 | 262 | 56.8 | 5 | 0.11 | 2.61e-05 (2^-15.23) | 15.23 |
| 15 | `pipelined_m:data_width=21,n_iter=17,angle_guard=1,frac_guard=1,rounding=trunc,m=7` | 1219 | 261 | 56.8 | 5 | 0.111 | 2.41e-05 (2^-15.34) | 15.34 |
| 16 | `pipelined_m:data_width=22,n_iter=17,angle_guard=-1,frac_guard=1,rounding=trunc,m=7` | 1236 | 266 | 54.3 | 5 | 0.113 | 2.39e-05 (2^-15.36) | 15.36 |
| 17 | `pipelined_m:data_width=22,n_iter=17,angle_guard=1,frac_guard=0,rounding=round,m=7` | 1236 | 268 | 54.3 | 5 | 0.113 | 1.95e-05 (2^-15.64) | 15.64 |
| 18 | `pipelined_m:data_width=22,n_iter=17,angle_guard=1,frac_guard=0,rounding=round,m=6` | 1236 | 268 | 62.5 | 5 | 0.113 | 1.95e-05 (2^-15.64) | 15.64 |
| 19 | `pipelined_m:data_width=22,n_iter=17,angle_guard=1,frac_guard=1,rounding=trunc,m=5` | 1270 | 349 | 73.7 | 6 | 0.122 | 1.91e-05 (2^-15.67) | 15.67 |
| 20 | `pipelined_m:data_width=22,n_iter=17,angle_guard=4,frac_guard=1,rounding=round,m=7` | 1367 | 284 | 54.3 | 5 | 0.124 | 1.67e-05 (2^-15.87) | 15.87 |
| 21 | `pipelined_m:data_width=24,n_iter=17,angle_guard=1,frac_guard=1,rounding=trunc,m=7` | 1371 | 295 | 54.3 | 5 | 0.125 | 1.61e-05 (2^-15.93) | 15.93 |
| 22 | `pipelined_m:data_width=22,n_iter=17,angle_guard=4,frac_guard=3,rounding=round,m=7` | 1434 | 292 | 54.3 | 5 | 0.13 | 1.59e-05 (2^-15.94) | 15.94 |
| 23 | `pipelined_m:data_width=22,n_iter=19,angle_guard=-1,frac_guard=1,rounding=trunc,m=5` | 1390 | 341 | 73.7 | 6 | 0.13 | 1.52e-05 (2^-16.01) | 16.01 |
| 24 | `pipelined_m:data_width=20,n_iter=20,angle_guard=4,frac_guard=1,rounding=round,m=7` | 1489 | 261 | 54.3 | 5 | 0.132 | 1.24e-05 (2^-16.30) | 16.30 |
| 25 | `pipelined_m:data_width=22,n_iter=18,angle_guard=4,frac_guard=2,rounding=round,m=7` | 1485 | 288 | 54.3 | 5 | 0.133 | 8.74e-06 (2^-16.80) | 16.80 |
| 26 | `pipelined_m:data_width=23,n_iter=20,angle_guard=0,frac_guard=0,rounding=trunc,m=7` | 1507 | 276 | 54.3 | 5 | 0.134 | 7.02e-06 (2^-17.12) | 17.12 |
| 27 | `pipelined_m:data_width=22,n_iter=20,angle_guard=4,frac_guard=1,rounding=trunc,m=8` | 1567 | 281 | 48.0 | 5 | 0.139 | 6.11e-06 (2^-17.32) | 17.32 |
| 28 | `pipelined_m:data_width=22,n_iter=20,angle_guard=3,frac_guard=0,rounding=round,m=5` | 1507 | 351 | 73.7 | 6 | 0.14 | 5.85e-06 (2^-17.38) | 17.38 |
| 29 | `pipelined_m:data_width=22,n_iter=20,angle_guard=3,frac_guard=1,rounding=round,m=7` | 1593 | 280 | 54.3 | 5 | 0.141 | 4.05e-06 (2^-17.91) | 17.91 |
| 30 | `pipelined_m:data_width=24,n_iter=20,angle_guard=2,frac_guard=1,rounding=trunc,m=7` | 1647 | 298 | 54.3 | 5 | 0.146 | 3e-06 (2^-18.35) | 18.35 |
| 31 | `pipelined_m:data_width=23,n_iter=20,angle_guard=4,frac_guard=1,rounding=round,m=7` | 1675 | 295 | 52.0 | 5 | 0.148 | 2.88e-06 (2^-18.40) | 18.40 |
| 32 | `pipelined_m:data_width=24,n_iter=21,angle_guard=2,frac_guard=1,rounding=trunc,m=8` | 1733 | 298 | 48.0 | 5 | 0.153 | 2.24e-06 (2^-18.77) | 18.77 |
| 33 | `pipelined_m:data_width=24,n_iter=21,angle_guard=2,frac_guard=1,rounding=round,m=7` | 1784 | 300 | 54.3 | 5 | 0.157 | 1.69e-06 (2^-19.17) | 19.17 |
| 34 | `pipelined_m:data_width=24,n_iter=21,angle_guard=2,frac_guard=3,rounding=round,m=7` | 1868 | 308 | 52.0 | 5 | 0.164 | 1.47e-06 (2^-19.38) | 19.38 |
| 35 | `pipelined_m:data_width=24,n_iter=22,angle_guard=1,frac_guard=2,rounding=round,m=6` | 1893 | 385 | 62.5 | 6 | 0.171 | 1.24e-06 (2^-19.63) | 19.63 |
| 36 | `pipelined_m:data_width=24,n_iter=22,angle_guard=1,frac_guard=2,rounding=round,m=7` | 1893 | 385 | 54.3 | 6 | 0.171 | 1.24e-06 (2^-19.63) | 19.63 |
| 37 | `pipelined_m:data_width=24,n_iter=22,angle_guard=4,frac_guard=2,rounding=trunc,m=6` | 1908 | 395 | 59.9 | 6 | 0.173 | 1.06e-06 (2^-19.84) | 19.84 |
| 38 | `pipelined_m:data_width=28,n_iter=24,angle_guard=-1,frac_guard=0,rounding=trunc,m=8` | 2162 | 329 | 45.9 | 5 | 0.187 | 3.63e-07 (2^-21.39) | 21.39 |
| 39 | `pipelined_m:data_width=28,n_iter=24,angle_guard=3,frac_guard=0,rounding=round,m=8` | 2259 | 341 | 44.0 | 5 | 0.196 | 1.86e-07 (2^-22.36) | 22.36 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec has three hard constraints: throughput_msps >= 2, max_abs_err <= 2^-10, and sys_p99_latency_us <= 0.4us. The p99 latency constraint is the tightest because it involves bursty Poisson arrivals of 8 requests 0ns apart. A burst of 8 must be cleared within ~0.4us to keep p99 latency low. This favors families with high per-burst throughput: pipelined_m (1 result/cycle, area-efficient via m), unrolled_k (k rotations/cycle, shared datapath), and pipelined (1 result/cycle, full area). iterative is likely infeasible for the latency constraint but is included to map the area floor. The accuracy constraint (max_abs_err <= 2^-10) requires sufficient n_iter and data_width; this is a secondary constraint that all families can meet with moderate parameters. The objective is to minimize luts_plus_ffs while maximizing accuracy_bits, so the Pareto front will trade area against accuracy. Budget is allocated 40% to pipelined_m (best area/latency trade-off), 30% to unrolled_k (high burst throughput, lower area), 20% to pipelined (safest latency, highest area), and 10% to iterative (area floor). This distribution focuses the search where the trade-offs are most interesting and where feasible designs are most likely to be found.*)
- `pipelined_m` (40 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* pipelined_m is the primary candidate for meeting the tight sys_p99_latency_us <= 0.4us constraint with bursts of 8. By registering every m stages, it achieves 1 result/cycle throughput (satisfying throughput_msps >= 2) while reducing area (LUTs+FFs) compared to fully pipelined (m=1). The m parameter allows trading off latency (ceil(N/m)+2) against area, which is critical for minimizing luts_plus_ffs while keeping burst clearance time low. The 0.4us p99 latency bound means a burst of 8 must clear in ~0.4us; with 1 result/cycle, this requires Fmax >= 20 MHz (8 cycles / 0.4us), which is easily achievable. Lower m values give lower latency but higher area; higher m values save area but increase latency. This family spans the key trade-off space.
- `unrolled_k` (30 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* unrolled_k processes k micro-rotations per cycle, so a burst of 8 requests can be cleared in ceil(N/k)+3 cycles. With k=8, a burst of 8 could potentially be handled in ~4-6 cycles total (depending on N), which at moderate Fmax (e.g., 50-100 MHz) gives burst clearance well under 0.4us. This family has lower area than pipelined_m for equivalent throughput because it shares the datapath across k rotations rather than duplicating pipeline stages. The k parameter directly controls the burst-clearance speed vs area trade-off. Throughput is ceil(N/k)+3 cycles/result, so for throughput_msps >= 2, we need Fmax * 1/(ceil(N/k)+3) >= 2, which is easily met. The p99 latency constraint is the binding one, and unrolled_k with high k minimizes the cycles-per-burst.
- `pipelined` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* pipelined (m=1) gives the lowest latency (N+2 cycles) and highest throughput (1 result/cycle), making it the safest choice for the p99 latency constraint. However, it has the highest area due to full pipeline registers. Including it at 20% budget helps map the upper-left corner of the Pareto front (low latency, high area) and provides a reference point for how much area pipelined_m and unrolled_k save. It also serves as a fallback if the other families fail to meet the latency constraint at reasonable Fmax.
- `iterative` (10 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* iterative has the lowest area (shared datapath, no pipeline registers) but the worst throughput (N+3 cycles/result) and highest latency. It is included at 10% budget primarily to map the low-area corner of the Pareto front and to verify whether it can meet the throughput_msps >= 2 constraint at high Fmax. For a burst of 8, iterative would take 8*(N+3) cycles, which at 100 MHz with N=12 gives 8*15=120 cycles = 1.2us, far exceeding the 0.4us p99 bound. So iterative is likely infeasible for the system constraint, but it defines the area floor and helps the hypervolume calculation by covering the extreme low-area, high-latency region.
- clamped by code: pipelined_m.rounding: dropped invalid choices ['rounding', 'data_width', 'n_iter', 'angle_guard', 'frac_guard', 'm']
- clamped by code: unrolled_k.rounding: dropped invalid choices ['rounding', 'data_width', 'n_iter', 'angle_guard', 'frac_guard', 'k']
- clamped by code: pipelined.rounding: dropped invalid choices ['rounding', 'data_width', 'n_iter', 'angle_guard', 'frac_guard']
- clamped by code: iterative.rounding: dropped invalid choices ['rounding', 'data_width', 'n_iter', 'angle_guard', 'frac_guard']

**Result (code):** 100 evaluations this round, 100 total; 43 feasible; hypervolume 1.288e+04 (n/a).

**LLM decision:** `refine` — The `pipelined_m` family is the only one producing feasible designs (31 feasible vs 0 for iterative/unrolled_k and 12 for pipelined). The current Pareto front is dominated by `pipelined_m` with `m` values of 6 and 7, and `data_width` 18-24. The `pipelined` family's best feasible area (2208) is significantly worse than `pipelined_m`'s best (1046), and `iterative`/`unrolled_k` fail the throughput constraint entirely. To maximize hypervolume and find the true minimum area design, we should focus the search exclusively on `pipelined_m` in the region where it has already proven feasible and efficient: `data_width` 16-24, `n_iter` 10-22, `angle_guard` -1 to 4, `frac_guard` 0-3, and `m` 5-8. This narrows the search space to let Optuna explore the trade-off between area and accuracy more densely within the viable region.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 1.288e+04 (gain this round: n/a (first round)).
Feasible designs: 43 of 100 evaluations (40 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 38% violate; best seen 2.56e-07 (2^-21.90)
- sys_p99_latency_us <= 0.4: 37% violate; best seen 0.0482

Pareto front (feasible, 12 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=23 n_iter=11 angle_guard=4 frac_guard=0 rounding=round m=6] luts_plus_ffs=1046, accuracy_bits=10, luts=838, ffs=208, throughput_msps=59.9, max_abs_err=0.000976 (2^-10.00), power_index=0.0787
- pipelined_m [data_width=18 n_iter=20 angle_guard=2 frac_guard=1 rounding=round m=7] luts_plus_ffs=1558, accuracy_bits=14.3, luts=1325, ffs=233, throughput_msps=56.8, max_abs_err=5.02e-05 (2^-14.28), power_index=0.117
- pipelined_m [data_width=18 n_iter=20 angle_guard=2 frac_guard=3 rounding=trunc m=7] luts_plus_ffs=1606, accuracy_bits=14.4, luts=1367, ffs=239, throughput_msps=56.8, max_abs_err=4.69e-05 (2^-14.38), power_index=0.121
- pipelined_m [data_width=18 n_iter=20 angle_guard=4 frac_guard=3 rounding=round m=7] luts_plus_ffs=1692, accuracy_bits=15.7, luts=1445, ffs=247, throughput_msps=56.8, max_abs_err=1.82e-05 (2^-15.74), power_index=0.127
- pipelined_m [data_width=23 n_iter=20 angle_guard=0 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=1783, accuracy_bits=17.1, luts=1507, ffs=276, throughput_msps=54.3, max_abs_err=7.02e-06 (2^-17.12), power_index=0.134
- pipelined_m [data_width=24 n_iter=20 angle_guard=2 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=1945, accuracy_bits=18.3, luts=1647, ffs=298, throughput_msps=54.3, max_abs_err=3e-06 (2^-18.35), power_index=0.146
- pipelined_m [data_width=24 n_iter=21 angle_guard=2 frac_guard=1 rounding=trunc m=8] luts_plus_ffs=2031, accuracy_bits=18.8, luts=1733, ffs=298, throughput_msps=48, max_abs_err=2.24e-06 (2^-18.77), power_index=0.153
- pipelined_m [data_width=24 n_iter=21 angle_guard=2 frac_guard=3 rounding=round m=7] luts_plus_ffs=2176, accuracy_bits=19.4, luts=1868, ffs=308, throughput_msps=52, max_abs_err=1.47e-06 (2^-19.38), power_index=0.164
- pipelined_m [data_width=24 n_iter=24 angle_guard=4 frac_guard=3 rounding=trunc m=7] luts_plus_ffs=2540, accuracy_bits=20.7, luts=2138, ffs=402, throughput_msps=52, max_abs_err=5.94e-07 (2^-20.68), power_index=0.191
- pipelined_m [data_width=24 n_iter=24 angle_guard=4 frac_guard=3 rounding=round m=6] luts_plus_ffs=2592, accuracy_bits=21.3, luts=2189, ffs=404, throughput_msps=59.9, max_abs_err=3.93e-07 (2^-21.28), power_index=0.195
Front coverage: luts_plus_ffs 1046..2592 (HV reference 3000); accuracy_bits 10..21.3 (HV reference 10); data_width on the front 18..24 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 23.2 MSPS; best accuracy 20.02 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 27.7 MSPS; best accuracy 21.90 bits
- pipelined: 20 evals, 12 feasible; max throughput seen 282 MSPS; best accuracy 19.77 bits; best feasible luts_plus_ffs=2208; feasible ranges: data_width 20..27, n_iter 13..26, angle_guard -2..2, frac_guard 0..4
- pipelined_m: 40 evals, 31 feasible; max throughput seen 164 MSPS; best accuracy 21.28 bits; best feasible luts_plus_ffs=1046; feasible ranges: data_width 16..25, n_iter 11..26, angle_guard -1..4, frac_guard 0..4, m 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate all remaining budget on the proven family to refine the Pareto front.*)
- `pipelined_m` (100 evals): data_width=16..24, n_iter=10..22, angle_guard=-1..4, frac_guard=0..3, rounding=trunc|round, m=5..8. *Why:* pipelined_m is the only family with a strong feasible front; focusing here allows dense mapping of the area-accuracy trade-off.

**Result (code):** 100 evaluations this round, 200 total; 133 feasible; hypervolume 1.524e+04 (+18.3%).

**LLM decision:** `refine` — The Pareto front is dominated by `pipelined_m` designs, which are significantly more area-efficient than `pipelined` (best 890 vs 2208 luts_plus_ffs) while meeting all constraints. The current front covers luts_plus_ffs from 890 to 2592 and accuracy_bits from 10.5 to 21.3. The minimum area point (890) has data_width=16, n_iter=13, m=7. The maximum accuracy point (21.3) has data_width=24, n_iter=24, m=6. The `pipelined` family is strictly dominated in area for comparable accuracy/throughput and should be excluded from further search to focus the budget. The `iterative` and `unrolled_k` families have 0 feasible designs, likely due to throughput or latency constraints, so they can also be excluded. We should narrow the search to `pipelined_m` only, focusing on the region that defines the current front: data_width 16..24, n_iter 12..24, m 5..7, angle_guard -1..4, frac_guard 0..3. This will allow Optuna to densely sample the trade-off curve between area and accuracy within the feasible region, improving hypervolume by filling in gaps on the front.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.524e+04 (gain this round: +18.3%).
Feasible designs: 133 of 200 evaluations (123 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 24% violate; best seen 2.56e-07 (2^-21.90)
- sys_p99_latency_us <= 0.4: 18% violate; best seen 0.0482

Pareto front (feasible, 36 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=13 angle_guard=4 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=890, accuracy_bits=10.5, luts=739, ffs=151, throughput_msps=56.8, max_abs_err=0.000704 (2^-10.47), power_index=0.067
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=trunc m=5] luts_plus_ffs=1048, accuracy_bits=12, luts=827, ffs=221, throughput_msps=80.6, max_abs_err=0.000251 (2^-11.96), power_index=0.0789
- pipelined_m [data_width=23 n_iter=14 angle_guard=0 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=1232, accuracy_bits=13, luts=1033, ffs=200, throughput_msps=54.3, max_abs_err=0.000123 (2^-12.99), power_index=0.0927
- pipelined_m [data_width=20 n_iter=17 angle_guard=3 frac_guard=0 rounding=round m=7] luts_plus_ffs=1421, accuracy_bits=15, luts=1169, ffs=252, throughput_msps=54.3, max_abs_err=2.95e-05 (2^-15.05), power_index=0.107
- pipelined_m [data_width=22 n_iter=17 angle_guard=-1 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=1502, accuracy_bits=15.4, luts=1236, ffs=266, throughput_msps=54.3, max_abs_err=2.39e-05 (2^-15.36), power_index=0.113
- pipelined_m [data_width=22 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc m=5] luts_plus_ffs=1619, accuracy_bits=15.7, luts=1270, ffs=349, throughput_msps=73.7, max_abs_err=1.91e-05 (2^-15.67), power_index=0.122
- pipelined_m [data_width=24 n_iter=18 angle_guard=4 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1774, accuracy_bits=16.7, luts=1474, ffs=300, throughput_msps=59.9, max_abs_err=9.16e-06 (2^-16.74), power_index=0.133
- pipelined_m [data_width=24 n_iter=20 angle_guard=2 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=1945, accuracy_bits=18.3, luts=1647, ffs=298, throughput_msps=54.3, max_abs_err=3e-06 (2^-18.35), power_index=0.146
- pipelined_m [data_width=24 n_iter=22 angle_guard=1 frac_guard=2 rounding=round m=6] luts_plus_ffs=2278, accuracy_bits=19.6, luts=1893, ffs=385, throughput_msps=62.5, max_abs_err=1.24e-06 (2^-19.63), power_index=0.171
- pipelined_m [data_width=24 n_iter=24 angle_guard=4 frac_guard=3 rounding=round m=6] luts_plus_ffs=2592, accuracy_bits=21.3, luts=2189, ffs=404, throughput_msps=59.9, max_abs_err=3.93e-07 (2^-21.28), power_index=0.195
Front coverage: luts_plus_ffs 890..2592 (HV reference 3000); accuracy_bits 10.5..21.3 (HV reference 10); data_width on the front 16..24 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 23.2 MSPS; best accuracy 20.02 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 27.7 MSPS; best accuracy 21.90 bits
- pipelined: 20 evals, 12 feasible; max throughput seen 282 MSPS; best accuracy 19.77 bits; best feasible luts_plus_ffs=2208; feasible ranges: data_width 20..27, n_iter 13..26, angle_guard -2..2, frac_guard 0..4
- pipelined_m: 140 evals, 121 feasible; max throughput seen 164 MSPS; best accuracy 21.28 bits; best feasible luts_plus_ffs=890; feasible ranges: data_width 16..25, n_iter 11..26, angle_guard -1..4, frac_guard 0..4, m 2..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Focus exclusively on pipelined_m with narrowed ranges to densely map the Pareto front between area and accuracy.*)
- `pipelined_m` (40 evals): data_width=16..24, n_iter=12..24, angle_guard=-1..4, frac_guard=0..3, rounding=trunc|round, m=5..7. *Why:* pipelined_m dominates the front in area efficiency; narrowing to the observed feasible region (data_width 16-24, n_iter 12-24, m 5-7) focuses the search on the trade-off curve.

**Result (code):** 40 evaluations this round, 240 total; 173 feasible; hypervolume 1.537e+04 (+0.9%).

**LLM decision:** `stop` — The exploration has converged on a robust Pareto front dominated by the `pipelined_m` family, which is the only family capable of meeting the strict system latency constraint (`sys_p99_latency_us <= 0.4`) while maintaining high throughput. The front covers the objective space well, ranging from 890 LUTs+FFs (10.5 bits accuracy) to 2592 LUTs+FFs (21.3 bits accuracy). The selection rule (`min luts_plus_ffs`) points to the 890 LUT+FF design, which comfortably satisfies the accuracy constraint (10.5 bits > 10 bits required) and the throughput constraint (56.8 MSPS > 2 MSPS). Since this is the final round, further refinement would yield diminishing returns, and the current front provides a clear, feasible design for the system simulation stage.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 1.537e+04 (gain this round: +0.9%).
Feasible designs: 173 of 240 evaluations (156 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 20% violate; best seen 2.56e-07 (2^-21.90)
- sys_p99_latency_us <= 0.4: 15% violate; best seen 0.0482

Pareto front (feasible, 38 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=13 angle_guard=4 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=890, accuracy_bits=10.5, luts=739, ffs=151, throughput_msps=56.8, max_abs_err=0.000704 (2^-10.47), power_index=0.067
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1048, accuracy_bits=12, luts=827, ffs=221, throughput_msps=68.5, max_abs_err=0.000251 (2^-11.96), power_index=0.0789
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=3 rounding=trunc m=7] luts_plus_ffs=1230, accuracy_bits=13.3, luts=994, ffs=236, throughput_msps=56.8, max_abs_err=0.000102 (2^-13.26), power_index=0.0925
- pipelined_m [data_width=21 n_iter=17 angle_guard=0 frac_guard=0 rounding=round m=7] luts_plus_ffs=1423, accuracy_bits=15.2, luts=1169, ffs=254, throughput_msps=56.8, max_abs_err=2.7e-05 (2^-15.18), power_index=0.107
- pipelined_m [data_width=22 n_iter=17 angle_guard=1 frac_guard=0 rounding=round m=7] luts_plus_ffs=1504, accuracy_bits=15.6, luts=1236, ffs=268, throughput_msps=54.3, max_abs_err=1.95e-05 (2^-15.64), power_index=0.113
- pipelined_m [data_width=22 n_iter=17 angle_guard=4 frac_guard=3 rounding=round m=7] luts_plus_ffs=1726, accuracy_bits=15.9, luts=1434, ffs=292, throughput_msps=54.3, max_abs_err=1.59e-05 (2^-15.94), power_index=0.13
- pipelined_m [data_width=23 n_iter=20 angle_guard=0 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=1783, accuracy_bits=17.1, luts=1507, ffs=276, throughput_msps=54.3, max_abs_err=7.02e-06 (2^-17.12), power_index=0.134
- pipelined_m [data_width=23 n_iter=20 angle_guard=4 frac_guard=1 rounding=round m=7] luts_plus_ffs=1970, accuracy_bits=18.4, luts=1675, ffs=295, throughput_msps=52, max_abs_err=2.88e-06 (2^-18.40), power_index=0.148
- pipelined_m [data_width=24 n_iter=22 angle_guard=1 frac_guard=2 rounding=round m=6] luts_plus_ffs=2278, accuracy_bits=19.6, luts=1893, ffs=385, throughput_msps=62.5, max_abs_err=1.24e-06 (2^-19.63), power_index=0.171
- pipelined_m [data_width=24 n_iter=24 angle_guard=4 frac_guard=3 rounding=round m=6] luts_plus_ffs=2592, accuracy_bits=21.3, luts=2189, ffs=404, throughput_msps=59.9, max_abs_err=3.93e-07 (2^-21.28), power_index=0.195
Front coverage: luts_plus_ffs 890..2592 (HV reference 3000); accuracy_bits 10.5..21.3 (HV reference 10); data_width on the front 16..24 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 23.2 MSPS; best accuracy 20.02 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 27.7 MSPS; best accuracy 21.90 bits
- pipelined: 20 evals, 12 feasible; max throughput seen 282 MSPS; best accuracy 19.77 bits; best feasible luts_plus_ffs=2208; feasible ranges: data_width 20..27, n_iter 13..26, angle_guard -2..2, frac_guard 0..4
- pipelined_m: 180 evals, 161 feasible; max throughput seen 164 MSPS; best accuracy 21.28 bits; best feasible luts_plus_ffs=890; feasible ranges: data_width 16..25, n_iter 11..26, angle_guard -1..4, frac_guard 0..4, m 2..8
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (54 evals): data_width=15..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (38 front designs; box front_anchored)
- `iterative` (53 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: iterative was explored but found nothing feasible; full-box share (M3 lever)
- `unrolled_k` (53 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: unrolled_k was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 160 evaluations this round, 400 total; 226 feasible; hypervolume 1.6e+04 (+4.1%).

**No LLM call** (code's front-mapping round): The exploration has converged on a robust Pareto front dominated by the `pipelined_m` family, which is the only family capable of meeting the strict system latency constraint (`sys_p99_latency_us <= 0.4`) while maintaining high throughput. The front covers the objective space well, ranging from 890 LUTs+FFs (10.5 bits accuracy) to 2592 LUTs+FFs (21.3 bits accuracy). The selection rule (`min luts_plus_ffs`) points to the 890 LUT+FF design, which comfortably satisfies the accuracy constraint (10.5 bits > 10 bits required) and the throughput constraint (56.8 MSPS > 2 MSPS). Since this is the final round, further refinement would yield diminishing returns, and the current front provides a clear, feasible design for the system simulation stage.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.6e+04 (gain this round: +4.1%).
Feasible designs: 226 of 400 evaluations (209 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 22% violate; best seen 1.86e-07 (2^-22.36)
- sys_p99_latency_us <= 0.4: 35% violate; best seen 0.0482

Pareto front (feasible, 40 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=13 angle_guard=4 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=890, accuracy_bits=10.5, luts=739, ffs=151, throughput_msps=56.8, max_abs_err=0.000704 (2^-10.47), power_index=0.067
- pipelined_m [data_width=19 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=1065, accuracy_bits=12.6, luts=896, ffs=169, throughput_msps=56.8, max_abs_err=0.000158 (2^-12.63), power_index=0.0801
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=3 rounding=trunc m=7] luts_plus_ffs=1230, accuracy_bits=13.3, luts=994, ffs=236, throughput_msps=56.8, max_abs_err=0.000102 (2^-13.26), power_index=0.0925
- pipelined_m [data_width=21 n_iter=17 angle_guard=0 frac_guard=0 rounding=round m=7] luts_plus_ffs=1423, accuracy_bits=15.2, luts=1169, ffs=254, throughput_msps=56.8, max_abs_err=2.7e-05 (2^-15.18), power_index=0.107
- pipelined_m [data_width=22 n_iter=17 angle_guard=1 frac_guard=0 rounding=round m=7] luts_plus_ffs=1504, accuracy_bits=15.6, luts=1236, ffs=268, throughput_msps=54.3, max_abs_err=1.95e-05 (2^-15.64), power_index=0.113
- pipelined_m [data_width=22 n_iter=17 angle_guard=4 frac_guard=3 rounding=round m=7] luts_plus_ffs=1726, accuracy_bits=15.9, luts=1434, ffs=292, throughput_msps=54.3, max_abs_err=1.59e-05 (2^-15.94), power_index=0.13
- pipelined_m [data_width=23 n_iter=20 angle_guard=0 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=1783, accuracy_bits=17.1, luts=1507, ffs=276, throughput_msps=54.3, max_abs_err=7.02e-06 (2^-17.12), power_index=0.134
- pipelined_m [data_width=24 n_iter=20 angle_guard=2 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=1945, accuracy_bits=18.3, luts=1647, ffs=298, throughput_msps=54.3, max_abs_err=3e-06 (2^-18.35), power_index=0.146
- pipelined_m [data_width=24 n_iter=22 angle_guard=1 frac_guard=2 rounding=round m=6] luts_plus_ffs=2278, accuracy_bits=19.6, luts=1893, ffs=385, throughput_msps=62.5, max_abs_err=1.24e-06 (2^-19.63), power_index=0.171
- pipelined_m [data_width=28 n_iter=24 angle_guard=3 frac_guard=0 rounding=round m=8] luts_plus_ffs=2600, accuracy_bits=22.4, luts=2259, ffs=341, throughput_msps=44, max_abs_err=1.86e-07 (2^-22.36), power_index=0.196
Front coverage: luts_plus_ffs 890..2600 (HV reference 3000); accuracy_bits 10.5..22.4 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- iterative: 63 evals, 0 feasible; max throughput seen 35.5 MSPS; best accuracy 20.02 bits
- unrolled_k: 83 evals, 0 feasible; max throughput seen 27.7 MSPS; best accuracy 21.90 bits
- pipelined: 20 evals, 12 feasible; max throughput seen 282 MSPS; best accuracy 19.77 bits; best feasible luts_plus_ffs=2208; feasible ranges: data_width 20..27, n_iter 13..26, angle_guard -2..2, frac_guard 0..4
- pipelined_m: 234 evals, 214 feasible; max throughput seen 164 MSPS; best accuracy 22.36 bits; best feasible luts_plus_ffs=890; feasible ranges: data_width 16..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 26963 in, 4539 out
- provider-reported cost: $0.0091
- full prompts and replies: `llm_trace.jsonl`

