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
`pipelined_m:data_width=15,n_iter=12,angle_guard=0,frac_guard=2,rounding=round,m=7` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 674 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 141 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 59.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 59.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 67.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0614 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000927 (2^-10.07) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 7.6 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000249 (2^-11.97) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 2.04 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.1 | exact: bit-accurate model, exhaustive (32768 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 4 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 80.1 dBc, SNR 69.4 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: bursty requests: bursts of 8 (0 ns apart) arriving as a Poisson process, 2 requests/us on average. Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_latency_us <= 0.4 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=15,n_iter=12,angle_guard=0,frac_guard=2,rounding=round,m=7` | 0.1678 → 0.2328 | yes |
| `pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=2,rounding=round,m=6` | 0.1459 → 0.1953 | yes |
| `pipelined_m:data_width=18,n_iter=12,angle_guard=0,frac_guard=0,rounding=round,m=4` | 0.1124 → 0.1351 | yes |
| `pipelined_m:data_width=20,n_iter=12,angle_guard=0,frac_guard=0,rounding=trunc,m=7` | 0.1759 → 0.245 | yes |
| `pipelined_m:data_width=16,n_iter=13,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 0.1226 → 0.1453 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (37 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=12,angle_guard=0,frac_guard=2,rounding=round,m=7` | 674 | 141 | 59.6 | 4 | 0.0614 | 0.000927 (2^-10.07) | 10.07 |
| 1 | `pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=2,rounding=round,m=6` | 734 | 153 | 68.5 | 4 | 0.0668 | 0.000548 (2^-10.83) | 10.83 |
| 2 | `pipelined_m:data_width=18,n_iter=12,angle_guard=0,frac_guard=0,rounding=round,m=4` | 701 | 221 | 97.8 | 5 | 0.0693 | 0.000546 (2^-10.84) | 10.84 |
| 3 | `pipelined_m:data_width=20,n_iter=12,angle_guard=0,frac_guard=0,rounding=trunc,m=7` | 770 | 176 | 56.8 | 4 | 0.0712 | 0.0005 (2^-10.97) | 10.97 |
| 4 | `pipelined_m:data_width=16,n_iter=13,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 713 | 260 | 97.8 | 6 | 0.0733 | 0.000498 (2^-10.97) | 10.97 |
| 5 | `pipelined_m:data_width=20,n_iter=13,angle_guard=-1,frac_guard=0,rounding=round,m=7` | 827 | 174 | 56.8 | 4 | 0.0753 | 0.000269 (2^-11.86) | 11.86 |
| 6 | `pipelined_m:data_width=20,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 916 | 184 | 50.3 | 4 | 0.0827 | 0.000248 (2^-11.98) | 11.98 |
| 7 | `pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=4` | 827 | 282 | 97.8 | 6 | 0.0835 | 0.0002 (2^-12.28) | 12.28 |
| 8 | `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=0,rounding=round,m=4` | 890 | 282 | 97.8 | 6 | 0.0882 | 0.000145 (2^-12.75) | 12.75 |
| 9 | `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=2,rounding=round,m=3` | 987 | 362 | 119.3 | 7 | 0.102 | 0.000123 (2^-12.99) | 12.99 |
| 10 | `pipelined_m:data_width=20,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=8` | 1185 | 186 | 50.3 | 4 | 0.103 | 3.61e-05 (2^-14.76) | 14.76 |
| 11 | `pipelined_m:data_width=21,n_iter=17,angle_guard=1,frac_guard=0,rounding=round,m=7` | 1185 | 257 | 56.8 | 5 | 0.109 | 2.44e-05 (2^-15.32) | 15.32 |
| 12 | `pipelined_m:data_width=20,n_iter=17,angle_guard=2,frac_guard=2,rounding=round,m=8` | 1261 | 259 | 50.3 | 5 | 0.114 | 2.23e-05 (2^-15.45) | 15.45 |
| 13 | `pipelined_m:data_width=23,n_iter=17,angle_guard=1,frac_guard=0,rounding=round,m=7` | 1287 | 279 | 54.3 | 5 | 0.118 | 1.66e-05 (2^-15.88) | 15.88 |
| 14 | `pipelined_m:data_width=23,n_iter=18,angle_guard=4,frac_guard=0,rounding=trunc,m=8` | 1420 | 289 | 45.9 | 5 | 0.129 | 1.07e-05 (2^-16.51) | 16.51 |
| 15 | `pipelined_m:data_width=23,n_iter=18,angle_guard=4,frac_guard=3,rounding=round,m=8` | 1576 | 303 | 45.9 | 5 | 0.141 | 7.93e-06 (2^-16.94) | 16.94 |
| 16 | `pipelined_m:data_width=23,n_iter=20,angle_guard=0,frac_guard=3,rounding=trunc,m=8` | 1627 | 289 | 48.0 | 5 | 0.144 | 4.52e-06 (2^-17.76) | 17.76 |
| 17 | `pipelined_m:data_width=23,n_iter=20,angle_guard=1,frac_guard=3,rounding=round,m=7` | 1695 | 294 | 54.3 | 5 | 0.15 | 3.39e-06 (2^-18.17) | 18.17 |
| 18 | `pipelined_m:data_width=23,n_iter=20,angle_guard=1,frac_guard=3,rounding=round,m=8` | 1695 | 294 | 48.0 | 5 | 0.15 | 3.39e-06 (2^-18.17) | 18.17 |
| 19 | `pipelined_m:data_width=23,n_iter=21,angle_guard=1,frac_guard=3,rounding=trunc,m=8` | 1733 | 292 | 48.0 | 5 | 0.152 | 2.69e-06 (2^-18.51) | 18.51 |
| 20 | `pipelined_m:data_width=23,n_iter=21,angle_guard=3,frac_guard=1,rounding=round,m=6` | 1740 | 373 | 62.5 | 6 | 0.159 | 2.29e-06 (2^-18.74) | 18.74 |
| 21 | `pipelined_m:data_width=25,n_iter=20,angle_guard=4,frac_guard=4,rounding=round,m=7` | 1920 | 329 | 52.0 | 5 | 0.169 | 1.98e-06 (2^-18.95) | 18.95 |
| 22 | `pipelined_m:data_width=23,n_iter=23,angle_guard=3,frac_guard=2,rounding=round,m=8` | 1955 | 296 | 48.0 | 5 | 0.169 | 1.18e-06 (2^-19.69) | 19.69 |
| 23 | `pipelined_m:data_width=28,n_iter=21,angle_guard=3,frac_guard=0,rounding=trunc,m=7` | 1965 | 341 | 49.9 | 5 | 0.174 | 1.05e-06 (2^-19.86) | 19.86 |
| 24 | `pipelined_m:data_width=28,n_iter=21,angle_guard=0,frac_guard=2,rounding=round,m=8` | 2045 | 342 | 45.9 | 5 | 0.18 | 1.03e-06 (2^-19.88) | 19.88 |
| 25 | `pipelined_m:data_width=28,n_iter=21,angle_guard=0,frac_guard=2,rounding=round,m=7` | 2045 | 342 | 52.0 | 5 | 0.18 | 1.03e-06 (2^-19.88) | 19.88 |
| 26 | `pipelined_m:data_width=28,n_iter=21,angle_guard=2,frac_guard=1,rounding=round,m=7` | 2045 | 344 | 52.0 | 5 | 0.18 | 9.78e-07 (2^-19.96) | 19.96 |
| 27 | `pipelined_m:data_width=28,n_iter=21,angle_guard=3,frac_guard=3,rounding=trunc,m=7` | 2092 | 353 | 49.9 | 5 | 0.184 | 9.7e-07 (2^-19.98) | 19.98 |
| 28 | `pipelined_m:data_width=28,n_iter=21,angle_guard=3,frac_guard=3,rounding=trunc,m=8` | 2092 | 353 | 44.0 | 5 | 0.184 | 9.7e-07 (2^-19.98) | 19.98 |
| 29 | `pipelined_m:data_width=24,n_iter=23,angle_guard=2,frac_guard=4,rounding=trunc,m=7` | 2045 | 400 | 52.0 | 6 | 0.184 | 9.04e-07 (2^-20.08) | 20.08 |
| 30 | `pipelined_m:data_width=24,n_iter=23,angle_guard=2,frac_guard=4,rounding=round,m=7` | 2096 | 402 | 52.0 | 6 | 0.188 | 7.74e-07 (2^-20.30) | 20.30 |
| 31 | `pipelined_m:data_width=26,n_iter=24,angle_guard=1,frac_guard=2,rounding=round,m=8` | 2217 | 323 | 45.9 | 5 | 0.191 | 3.39e-07 (2^-21.49) | 21.49 |
| 32 | `pipelined_m:data_width=28,n_iter=23,angle_guard=2,frac_guard=1,rounding=trunc,m=6` | 2184 | 438 | 59.9 | 6 | 0.197 | 3.03e-07 (2^-21.66) | 21.66 |
| 33 | `pipelined_m:data_width=25,n_iter=26,angle_guard=3,frac_guard=3,rounding=round,m=7` | 2429 | 414 | 52.0 | 6 | 0.214 | 2.16e-07 (2^-22.14) | 22.14 |
| 34 | `pipelined_m:data_width=28,n_iter=27,angle_guard=2,frac_guard=1,rounding=trunc,m=6` | 2581 | 534 | 59.9 | 7 | 0.234 | 1.02e-07 (2^-23.22) | 23.22 |
| 35 | `pipelined_m:data_width=28,n_iter=27,angle_guard=2,frac_guard=1,rounding=round,m=6` | 2640 | 536 | 59.9 | 7 | 0.239 | 6.66e-08 (2^-23.84) | 23.84 |
| 36 | `pipelined_m:data_width=28,n_iter=27,angle_guard=2,frac_guard=3,rounding=round,m=8` | 2749 | 452 | 44.0 | 6 | 0.241 | 4.86e-08 (2^-24.29) | 24.29 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires max_abs_err <= 2^-10 (accuracy_bits >= 10), throughput >= 2 Msps, and sys_p99_latency <= 0.4us under bursty Poisson traffic (8-req bursts, 2 req/us mean). The selection rule is min LUTs+FFs, so we favor low-area designs that still pass the p99 latency constraint in L2 simulation. Prior campaigns found iterative as the area winner for low-rate specs, but the p99 latency constraint under bursty traffic may favor lower-latency families (unrolled_k, pipelined_m, pipelined). I allocate 40% to iterative (likely area winner), 30% to unrolled_k (reduced latency via k=2..4), 20% to pipelined_m (1 result/cycle with moderate area), and 10% to pipelined (lowest latency, highest area). Data width 14-18 and n_iter 12-16 are chosen to satisfy the accuracy constraint while minimizing area. Angle_guard -2..0 and frac_guard 0..2 explore the accuracy/area trade-off. The ranges are narrow to focus the 400-eval budget on the feasible region where all constraints can be met.*)
- `iterative` (40 evals): data_width=14..18, n_iter=12..16, angle_guard=-2..0, frac_guard=0..2, rounding=trunc|round. *Why:* Prior campaign identified iterative as the area winner for low-rate specs. With 2 req/us mean and 8-req bursts, iterative (1 result/cycle latency N+3) can handle the average rate if N is small, but p99 latency <= 0.4us is tight. Narrowing n_iter to 12-16 and data_width to 14-18 focuses on the accuracy constraint (max_abs_err <= 2^-10) while minimizing area. angle_guard -2..0 and frac_guard 0..2 explore the accuracy/area trade-off within the feasible region.
- `unrolled_k` (30 evals): data_width=14..18, n_iter=12..16, angle_guard=-2..0, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Unrolled_k with k=2..4 reduces latency to ceil(N/k)+3 cycles, which helps meet the p99 <= 0.4us constraint under bursty traffic. While prior campaigns found unrolled families didn't reach the front, the tighter p99 constraint here may change that. Focusing on k=2..4 balances latency reduction against area overhead. Same data_width/n_iter ranges as iterative to maintain accuracy feasibility.
- `pipelined_m` (20 evals): data_width=14..18, n_iter=12..16, angle_guard=-2..0, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Pipelined_m with m=2..4 gives 1 result/cycle throughput with reduced area vs fully pipelined (m=1). The 1 result/cycle throughput easily meets the 2 req/us constraint, and latency ceil(N/m)+2 is low enough to potentially meet p99 <= 0.4us. This family offers a good area/latency trade-off for bursty traffic where sustained throughput matters.
- `pipelined` (10 evals): data_width=14..18, n_iter=12..16, angle_guard=-2..0, frac_guard=0..2, rounding=trunc|round. *Why:* Fully pipelined (m=1) has the lowest latency (N+2) and highest throughput (1 result/cycle), but highest area. Including it with a small budget share ensures we capture the low-latency end of the Pareto front, which may be necessary if p99 latency is binding under bursty traffic. The area penalty may make it non-optimal for the min LUTs+FFs selection rule, but it defines the latency boundary.

**Result (code):** 100 evaluations this round, 100 total; 18 feasible; hypervolume 5300 (n/a).

**LLM decision:** `refine` — The current Pareto front is dominated by `pipelined_m` designs (988-1217 luts_plus_ffs) which significantly outperform the `pipelined` design (2098 luts_plus_ffs) in area while maintaining comparable accuracy (10.4-12.4 bits vs 13.3 bits) and throughput. The `iterative` and `unrolled_k` families are infeasible due to low throughput (max ~13 MSPS) and high latency, failing the `sys_p99_latency_us <= 0.4` constraint. The `pipelined` family is feasible but area-inefficient compared to `pipelined_m`. To maximize hypervolume and find the true minimum area design, we should focus the search on the `pipelined_m` family, which currently holds the best area points. We will narrow the ranges around the known feasible region for `pipelined_m` (data_width 16-18, n_iter 12-16, m 2-4) and exclude the other families to concentrate the evaluation budget on refining the `pipelined_m` front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 5300 (gain this round: n/a (first round)).
Feasible designs: 18 of 100 evaluations (16 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 32% violate; best seen 0.000102 (2^-13.25)
- sys_p99_latency_us <= 0.4: 70% violate; best seen 0.0733

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=13 angle_guard=-1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=988, accuracy_bits=10.4, luts=726, ffs=262, throughput_msps=97.8, max_abs_err=0.000742 (2^-10.40), power_index=0.0744
- pipelined_m [data_width=16 n_iter=13 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1041, accuracy_bits=11.1, luts=772, ffs=268, throughput_msps=97.8, max_abs_err=0.000468 (2^-11.06), power_index=0.0783
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1217, accuracy_bits=12.4, luts=920, ffs=297, throughput_msps=93.6, max_abs_err=0.000179 (2^-12.45), power_index=0.0915
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=2 rounding=round] luts_plus_ffs=2098, accuracy_bits=13.3, luts=1055, ffs=1043, throughput_msps=264, max_abs_err=0.000102 (2^-13.25), power_index=0.158
Front coverage: luts_plus_ffs 988..2098 (HV reference 3000); accuracy_bits 10.4..13.3 (HV reference 10); data_width on the front 16..18 (registry 8..28).

Per family:
- iterative: 40 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 11.96 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 13.02 bits
- pipelined: 10 evals, 6 feasible; max throughput seen 282 MSPS; best accuracy 13.25 bits; best feasible luts_plus_ffs=1420; feasible ranges: data_width 15..18, n_iter 12..16, angle_guard -2..0, frac_guard 0..2
- pipelined_m: 20 evals, 12 feasible; max throughput seen 171 MSPS; best accuracy 12.45 bits; best feasible luts_plus_ffs=988; feasible ranges: data_width 16..18, n_iter 12..16, angle_guard -2..0, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate budget on the dominant family to refine the Pareto front in the high-value region of the objective space.*)
- `pipelined_m` (100 evals): data_width=15..18, n_iter=12..16, angle_guard=-2..0, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m dominates the area objective (988-1217 vs 2098 for pipelined) and meets all constraints. Focusing here allows refining the front to find the absolute minimum luts_plus_ffs and potentially better accuracy/area trade-offs within the feasible region.

**Result (code):** 100 evaluations this round, 200 total; 107 feasible; hypervolume 6070 (+14.5%).

**LLM decision:** `refine` — The Pareto front is dominated by `pipelined_m` designs, which are significantly more area-efficient than `pipelined` (best 947 vs 1420 luts_plus_ffs) while meeting all constraints. The current front spans accuracy_bits 10.5 to 13.3, but the hypervolume reference for accuracy is 10, meaning the 'high accuracy' end of the front is already well-covered relative to the reference, while the 'low area' end is the primary driver for the selection rule (min luts_plus_ffs). The `iterative` and `unrolled_k` families have produced 0 feasible designs due to throughput/latency bottlenecks, so they can be ignored. To maximize hypervolume and find the true minimum area design, we should narrow the search space to the most promising region of `pipelined_m` where the trade-off between area and accuracy is sharpest. Specifically, we focus on `data_width` 16-18, `n_iter` 12-15, `m` 3-4, and `angle_guard` -2 to 0. This concentrates the remaining 200 evaluations on refining the lower-left corner of the Pareto front (min area) and ensuring the accuracy constraint is met with minimal overhead.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 6070 (gain this round: +14.5%).
Feasible designs: 107 of 200 evaluations (84 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 22% violate; best seen 0.000102 (2^-13.25)
- sys_p99_latency_us <= 0.4: 35% violate; best seen 0.0733

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=12 angle_guard=-2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=947, accuracy_bits=10.5, luts=724, ffs=223, throughput_msps=93.6, max_abs_err=0.000667 (2^-10.55), power_index=0.0712
- pipelined_m [data_width=17 n_iter=13 angle_guard=-1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1040, accuracy_bits=11.1, luts=764, ffs=276, throughput_msps=93.6, max_abs_err=0.000448 (2^-11.12), power_index=0.0783
- pipelined_m [data_width=16 n_iter=14 angle_guard=0 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1066, accuracy_bits=11.3, luts=800, ffs=266, throughput_msps=97.8, max_abs_err=0.000391 (2^-11.32), power_index=0.0802
- pipelined_m [data_width=18 n_iter=14 angle_guard=-2 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1074, accuracy_bits=11.4, luts=800, ffs=274, throughput_msps=97.8, max_abs_err=0.000368 (2^-11.41), power_index=0.0808
- pipelined_m [data_width=18 n_iter=13 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=1118, accuracy_bits=11.7, luts=827, ffs=291, throughput_msps=93.6, max_abs_err=0.000298 (2^-11.71), power_index=0.0841
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1173, accuracy_bits=12.8, luts=890, ffs=282, throughput_msps=97.8, max_abs_err=0.000145 (2^-12.75), power_index=0.0882
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=2 rounding=round m=3] luts_plus_ffs=1350, accuracy_bits=13, luts=987, ffs=362, throughput_msps=119, max_abs_err=0.000123 (2^-12.99), power_index=0.102
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=round m=3] luts_plus_ffs=1441, accuracy_bits=13, luts=1023, ffs=418, throughput_msps=119, max_abs_err=0.00012 (2^-13.03), power_index=0.108
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=2 rounding=round m=3] luts_plus_ffs=1483, accuracy_bits=13.3, luts=1055, ffs=428, throughput_msps=119, max_abs_err=0.000102 (2^-13.25), power_index=0.112
Front coverage: luts_plus_ffs 947..1483 (HV reference 3000); accuracy_bits 10.5..13.3 (HV reference 10); data_width on the front 16..18 (registry 8..28).

Per family:
- iterative: 40 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 11.96 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 13.02 bits
- pipelined: 10 evals, 6 feasible; max throughput seen 282 MSPS; best accuracy 13.25 bits; best feasible luts_plus_ffs=1420; feasible ranges: data_width 15..18, n_iter 12..16, angle_guard -2..0, frac_guard 0..2
- pipelined_m: 120 evals, 101 feasible; max throughput seen 171 MSPS; best accuracy 13.25 bits; best feasible luts_plus_ffs=947; feasible ranges: data_width 15..18, n_iter 12..16, angle_guard -2..0, frac_guard 0..2, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Narrowing to pipelined_m with m=3-4 and data_width 16-18 targets the region where the best feasible designs were found, allowing Optuna to fine-tune the trade-off between luts_plus_ffs and accuracy_bits within the remaining budget.*)
- `pipelined_m` (40 evals): data_width=16..18, n_iter=12..15, angle_guard=-2..0, frac_guard=0..2, rounding=trunc|round, m=3..4. *Why:* Focus on the most efficient family and parameter region to refine the Pareto front's low-area corner.

**Result (code):** 40 evaluations this round, 240 total; 147 feasible; hypervolume 6183 (+1.9%).

**LLM decision:** `stop` — The exploration has successfully identified a robust Pareto front dominated by the `pipelined_m` family, which satisfies all constraints including the strict system-level p99 latency bound (best seen 0.0733 us vs 0.4 us limit) and throughput (best seen 171 MSPS vs 2 MSPS limit). The front covers a wide range of the primary objective `luts_plus_ffs` (919 to 1483) and the secondary objective `accuracy_bits` (10.5 to 13.3), significantly exceeding the hypervolume reference points (3000 and 10 respectively). The `iterative` and `unrolled_k` families were proven infeasible for this spec due to insufficient throughput to meet the system burst requirements, while `pipelined` and `pipelined_m` provided the necessary 1-result/cycle throughput. With 240/400 evaluations used and the front well-mapped across the feasible parameter space (data_width 16-18, n_iter 12-16), further refinement would yield diminishing returns. The selection rule (min luts_plus_ffs) will pick the 919 LUT+FF design, which is a strong candidate for the final L2 simulation shortlist.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 6183 (gain this round: +1.9%).
Feasible designs: 147 of 240 evaluations (112 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 18% violate; best seen 0.000102 (2^-13.25)
- sys_p99_latency_us <= 0.4: 29% violate; best seen 0.0733

Pareto front (feasible, 15 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=12 angle_guard=-1 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=919, accuracy_bits=10.5, luts=654, ffs=264, throughput_msps=124, max_abs_err=0.000686 (2^-10.51), power_index=0.0691
- pipelined_m [data_width=16 n_iter=13 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=974, accuracy_bits=11, luts=713, ffs=260, throughput_msps=97.8, max_abs_err=0.000498 (2^-10.97), power_index=0.0733
- pipelined_m [data_width=16 n_iter=13 angle_guard=0 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1005, accuracy_bits=11, luts=739, ffs=266, throughput_msps=97.8, max_abs_err=0.000474 (2^-11.04), power_index=0.0756
- pipelined_m [data_width=17 n_iter=13 angle_guard=-1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1040, accuracy_bits=11.1, luts=764, ffs=276, throughput_msps=93.6, max_abs_err=0.000448 (2^-11.12), power_index=0.0783
- pipelined_m [data_width=17 n_iter=13 angle_guard=0 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1057, accuracy_bits=11.4, luts=777, ffs=280, throughput_msps=93.6, max_abs_err=0.000381 (2^-11.36), power_index=0.0795
- pipelined_m [data_width=18 n_iter=13 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1078, accuracy_bits=11.7, luts=789, ffs=289, throughput_msps=93.6, max_abs_err=0.000303 (2^-11.69), power_index=0.0811
- pipelined_m [data_width=18 n_iter=13 angle_guard=0 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1109, accuracy_bits=11.7, luts=815, ffs=295, throughput_msps=93.6, max_abs_err=0.000299 (2^-11.71), power_index=0.0834
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1173, accuracy_bits=12.8, luts=890, ffs=282, throughput_msps=97.8, max_abs_err=0.000145 (2^-12.75), power_index=0.0882
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=2 rounding=round m=3] luts_plus_ffs=1350, accuracy_bits=13, luts=987, ffs=362, throughput_msps=119, max_abs_err=0.000123 (2^-12.99), power_index=0.102
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=2 rounding=round m=3] luts_plus_ffs=1483, accuracy_bits=13.3, luts=1055, ffs=428, throughput_msps=119, max_abs_err=0.000102 (2^-13.25), power_index=0.112
Front coverage: luts_plus_ffs 919..1483 (HV reference 3000); accuracy_bits 10.5..13.3 (HV reference 10); data_width on the front 16..18 (registry 8..28).

Per family:
- iterative: 40 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 11.96 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 13.02 bits
- pipelined: 10 evals, 6 feasible; max throughput seen 282 MSPS; best accuracy 13.25 bits; best feasible luts_plus_ffs=1420; feasible ranges: data_width 15..18, n_iter 12..16, angle_guard -2..0, frac_guard 0..2
- pipelined_m: 160 evals, 141 feasible; max throughput seen 171 MSPS; best accuracy 13.25 bits; best feasible luts_plus_ffs=919; feasible ranges: data_width 15..18, n_iter 12..16, angle_guard -2..0, frac_guard 0..2, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (160 evals): data_width=15..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (15 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 293 feasible; hypervolume 1.533e+04 (+147.9%).

**No LLM call** (code's front-mapping round): The exploration has successfully identified a robust Pareto front dominated by the `pipelined_m` family, which satisfies all constraints including the strict system-level p99 latency bound (best seen 0.0733 us vs 0.4 us limit) and throughput (best seen 171 MSPS vs 2 MSPS limit). The front covers a wide range of the primary objective `luts_plus_ffs` (919 to 1483) and the secondary objective `accuracy_bits` (10.5 to 13.3), significantly exceeding the hypervolume reference points (3000 and 10 respectively). The `iterative` and `unrolled_k` families were proven infeasible for this spec due to insufficient throughput to meet the system burst requirements, while `pipelined` and `pipelined_m` provided the necessary 1-result/cycle throughput. With 240/400 evaluations used and the front well-mapped across the feasible parameter space (data_width 16-18, n_iter 12-16), further refinement would yield diminishing returns. The selection rule (min luts_plus_ffs) will pick the 919 LUT+FF design, which is a strong candidate for the final L2 simulation shortlist.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.533e+04 (gain this round: +147.9%).
Feasible designs: 293 of 400 evaluations (247 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 14% violate; best seen 4.86e-08 (2^-24.29)
- sys_p99_latency_us <= 0.4: 18% violate; best seen 0.0733

Pareto front (feasible, 37 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=0 frac_guard=2 rounding=round m=7] luts_plus_ffs=816, accuracy_bits=10.1, luts=674, ffs=141, throughput_msps=59.6, max_abs_err=0.000927 (2^-10.07), power_index=0.0614
- pipelined_m [data_width=16 n_iter=13 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=974, accuracy_bits=11, luts=713, ffs=260, throughput_msps=97.8, max_abs_err=0.000498 (2^-10.97), power_index=0.0733
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1173, accuracy_bits=12.8, luts=890, ffs=282, throughput_msps=97.8, max_abs_err=0.000145 (2^-12.75), power_index=0.0882
- pipelined_m [data_width=20 n_iter=17 angle_guard=2 frac_guard=2 rounding=round m=8] luts_plus_ffs=1521, accuracy_bits=15.5, luts=1261, ffs=259, throughput_msps=50.3, max_abs_err=2.23e-05 (2^-15.45), power_index=0.114
- pipelined_m [data_width=23 n_iter=20 angle_guard=0 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1916, accuracy_bits=17.8, luts=1627, ffs=289, throughput_msps=48, max_abs_err=4.52e-06 (2^-17.76), power_index=0.144
- pipelined_m [data_width=23 n_iter=21 angle_guard=3 frac_guard=1 rounding=round m=6] luts_plus_ffs=2113, accuracy_bits=18.7, luts=1740, ffs=373, throughput_msps=62.5, max_abs_err=2.29e-06 (2^-18.74), power_index=0.159
- pipelined_m [data_width=28 n_iter=21 angle_guard=0 frac_guard=2 rounding=round m=8] luts_plus_ffs=2387, accuracy_bits=19.9, luts=2045, ffs=342, throughput_msps=45.9, max_abs_err=1.03e-06 (2^-19.88), power_index=0.18
- pipelined_m [data_width=28 n_iter=21 angle_guard=3 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=2445, accuracy_bits=20, luts=2092, ffs=353, throughput_msps=44, max_abs_err=9.7e-07 (2^-19.98), power_index=0.184
- pipelined_m [data_width=28 n_iter=23 angle_guard=2 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=2622, accuracy_bits=21.7, luts=2184, ffs=438, throughput_msps=59.9, max_abs_err=3.03e-07 (2^-21.66), power_index=0.197
- pipelined_m [data_width=28 n_iter=27 angle_guard=2 frac_guard=3 rounding=round m=8] luts_plus_ffs=3201, accuracy_bits=24.3, luts=2749, ffs=452, throughput_msps=44, max_abs_err=4.86e-08 (2^-24.29), power_index=0.241
Front coverage: luts_plus_ffs 816..3201 (HV reference 3000); accuracy_bits 10.1..24.3 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 40 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 11.96 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 13.02 bits
- pipelined: 10 evals, 6 feasible; max throughput seen 282 MSPS; best accuracy 13.25 bits; best feasible luts_plus_ffs=1420; feasible ranges: data_width 15..18, n_iter 12..16, angle_guard -2..0, frac_guard 0..2
- pipelined_m: 320 evals, 287 feasible; max throughput seen 171 MSPS; best accuracy 24.29 bits; best feasible luts_plus_ffs=816; feasible ranges: data_width 15..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 29127 in, 3746 out
- provider-reported cost: $0.0078
- full prompts and replies: `llm_trace.jsonl`

