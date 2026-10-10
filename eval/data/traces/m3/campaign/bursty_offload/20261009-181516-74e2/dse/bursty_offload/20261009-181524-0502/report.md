# DSE run: bursty_offload

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`pipelined_m:data_width=15,n_iter=12,angle_guard=0,frac_guard=2,rounding=trunc,m=7` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 643 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 139 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 59.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 59.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 67.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0588 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000962 (2^-10.02) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 7.88 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000256 (2^-11.93) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 2.1 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10 | exact: bit-accurate model, exhaustive (32768 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 4 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 80.1 dBc, SNR 69.1 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: bursty requests: bursts of 8 (0 ns apart) arriving as a Poisson process, 2 requests/us on average. Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_latency_us <= 0.4 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=15,n_iter=12,angle_guard=0,frac_guard=2,rounding=trunc,m=7` | 0.1678 → 0.2328 | yes |
| `pipelined_m:data_width=15,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,m=8` | 0.1896 → 0.2667 | yes |
| `pipelined_m:data_width=18,n_iter=12,angle_guard=0,frac_guard=2,rounding=round,m=7` | 0.1759 → 0.245 | yes |
| `pipelined_m:data_width=15,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=5` | 0.1365 → 0.172 | yes |
| `pipelined_m:data_width=18,n_iter=13,angle_guard=1,frac_guard=0,rounding=round,m=5` | 0.1429 → 0.183 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (39 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=12,angle_guard=0,frac_guard=2,rounding=trunc,m=7` | 643 | 139 | 59.6 | 4 | 0.0588 | 0.000962 (2^-10.02) | 10.02 |
| 1 | `pipelined_m:data_width=15,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,m=8` | 731 | 139 | 52.7 | 4 | 0.0655 | 0.000599 (2^-10.71) | 10.71 |
| 2 | `pipelined_m:data_width=18,n_iter=12,angle_guard=0,frac_guard=2,rounding=round,m=7` | 785 | 165 | 56.8 | 4 | 0.0715 | 0.000526 (2^-10.89) | 10.89 |
| 3 | `pipelined_m:data_width=15,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=5` | 790 | 200 | 80.6 | 5 | 0.0745 | 0.000403 (2^-11.28) | 11.28 |
| 4 | `pipelined_m:data_width=18,n_iter=13,angle_guard=1,frac_guard=0,rounding=round,m=5` | 777 | 224 | 77.0 | 5 | 0.0753 | 0.000289 (2^-11.76) | 11.76 |
| 5 | `pipelined_m:data_width=20,n_iter=13,angle_guard=-1,frac_guard=0,rounding=trunc,m=8` | 827 | 174 | 50.3 | 4 | 0.0753 | 0.000273 (2^-11.84) | 11.84 |
| 6 | `pipelined_m:data_width=17,n_iter=13,angle_guard=4,frac_guard=2,rounding=round,m=5` | 863 | 232 | 77.0 | 5 | 0.0824 | 0.000272 (2^-11.85) | 11.85 |
| 7 | `pipelined_m:data_width=20,n_iter=13,angle_guard=1,frac_guard=0,rounding=trunc,m=6` | 852 | 246 | 65.4 | 5 | 0.0827 | 0.000263 (2^-11.90) | 11.90 |
| 8 | `pipelined_m:data_width=19,n_iter=14,angle_guard=4,frac_guard=1,rounding=trunc,m=7` | 950 | 178 | 54.3 | 4 | 0.0849 | 0.000143 (2^-12.77) | 12.77 |
| 9 | `pipelined_m:data_width=21,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,m=8` | 978 | 188 | 48.0 | 4 | 0.0877 | 0.000127 (2^-12.95) | 12.95 |
| 10 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=5` | 973 | 230 | 77.0 | 5 | 0.0905 | 0.000101 (2^-13.27) | 13.27 |
| 11 | `pipelined_m:data_width=18,n_iter=17,angle_guard=1,frac_guard=0,rounding=round,m=6` | 1034 | 224 | 65.4 | 5 | 0.0946 | 9.26e-05 (2^-13.40) | 13.40 |
| 12 | `pipelined_m:data_width=20,n_iter=16,angle_guard=-1,frac_guard=0,rounding=round,m=6` | 1033 | 240 | 65.4 | 5 | 0.0958 | 6.98e-05 (2^-13.81) | 13.81 |
| 13 | `pipelined_m:data_width=19,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=4` | 1033 | 305 | 93.6 | 6 | 0.101 | 5.75e-05 (2^-14.09) | 14.09 |
| 14 | `pipelined_m:data_width=19,n_iter=16,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1080 | 315 | 93.6 | 6 | 0.105 | 5.64e-05 (2^-14.11) | 14.11 |
| 15 | `pipelined_m:data_width=19,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1096 | 317 | 93.6 | 6 | 0.106 | 4.81e-05 (2^-14.34) | 14.34 |
| 16 | `pipelined_m:data_width=20,n_iter=18,angle_guard=0,frac_guard=0,rounding=trunc,m=5` | 1188 | 311 | 77.0 | 6 | 0.113 | 4.53e-05 (2^-14.43) | 14.43 |
| 17 | `pipelined_m:data_width=22,n_iter=16,angle_guard=-1,frac_guard=2,rounding=round,m=7` | 1237 | 272 | 54.3 | 5 | 0.114 | 3.75e-05 (2^-14.70) | 14.70 |
| 18 | `pipelined_m:data_width=21,n_iter=16,angle_guard=4,frac_guard=3,rounding=trunc,m=7` | 1254 | 278 | 54.3 | 5 | 0.115 | 3.28e-05 (2^-14.90) | 14.90 |
| 19 | `pipelined_m:data_width=20,n_iter=18,angle_guard=2,frac_guard=0,rounding=round,m=5` | 1223 | 319 | 77.0 | 6 | 0.116 | 2.42e-05 (2^-15.34) | 15.34 |
| 20 | `pipelined_m:data_width=21,n_iter=18,angle_guard=1,frac_guard=1,rounding=trunc,m=8` | 1295 | 261 | 50.3 | 5 | 0.117 | 1.73e-05 (2^-15.82) | 15.82 |
| 21 | `pipelined_m:data_width=21,n_iter=18,angle_guard=2,frac_guard=0,rounding=round,m=5` | 1277 | 333 | 73.7 | 6 | 0.121 | 1.59e-05 (2^-15.94) | 15.94 |
| 22 | `pipelined_m:data_width=24,n_iter=18,angle_guard=1,frac_guard=0,rounding=trunc,m=8` | 1420 | 291 | 48.0 | 5 | 0.129 | 9.16e-06 (2^-16.74) | 16.74 |
| 23 | `pipelined_m:data_width=24,n_iter=18,angle_guard=1,frac_guard=0,rounding=round,m=5` | 1420 | 371 | 73.7 | 6 | 0.135 | 8.41e-06 (2^-16.86) | 16.86 |
| 24 | `pipelined_m:data_width=25,n_iter=19,angle_guard=-2,frac_guard=0,rounding=round,m=8` | 1504 | 293 | 48.0 | 5 | 0.135 | 5.96e-06 (2^-17.36) | 17.36 |
| 25 | `pipelined_m:data_width=25,n_iter=19,angle_guard=1,frac_guard=0,rounding=trunc,m=8` | 1561 | 302 | 48.0 | 5 | 0.14 | 4.66e-06 (2^-17.71) | 17.71 |
| 26 | `pipelined_m:data_width=23,n_iter=21,angle_guard=0,frac_guard=1,rounding=round,m=8` | 1677 | 282 | 48.0 | 5 | 0.147 | 4.01e-06 (2^-17.93) | 17.93 |
| 27 | `pipelined_m:data_width=25,n_iter=19,angle_guard=4,frac_guard=2,rounding=round,m=7` | 1746 | 321 | 52.0 | 5 | 0.155 | 3.94e-06 (2^-17.95) | 17.95 |
| 28 | `pipelined_m:data_width=25,n_iter=19,angle_guard=4,frac_guard=2,rounding=round,m=8` | 1746 | 321 | 45.9 | 5 | 0.155 | 3.94e-06 (2^-17.95) | 17.95 |
| 29 | `pipelined_m:data_width=24,n_iter=23,angle_guard=2,frac_guard=0,rounding=trunc,m=8` | 1860 | 294 | 48.0 | 5 | 0.162 | 2.96e-06 (2^-18.37) | 18.37 |
| 30 | `pipelined_m:data_width=24,n_iter=23,angle_guard=2,frac_guard=0,rounding=round,m=5` | 1860 | 457 | 73.7 | 7 | 0.174 | 1.57e-06 (2^-19.28) | 19.28 |
| 31 | `pipelined_m:data_width=26,n_iter=22,angle_guard=1,frac_guard=1,rounding=round,m=6` | 1985 | 408 | 59.9 | 6 | 0.18 | 6.82e-07 (2^-20.48) | 20.48 |
| 32 | `pipelined_m:data_width=26,n_iter=23,angle_guard=1,frac_guard=1,rounding=round,m=6` | 2077 | 408 | 59.9 | 6 | 0.187 | 4.43e-07 (2^-21.11) | 21.11 |
| 33 | `pipelined_m:data_width=26,n_iter=23,angle_guard=1,frac_guard=1,rounding=round,m=7` | 2077 | 408 | 52.0 | 6 | 0.187 | 4.43e-07 (2^-21.11) | 21.11 |
| 34 | `pipelined_m:data_width=26,n_iter=24,angle_guard=3,frac_guard=2,rounding=trunc,m=5` | 2211 | 513 | 70.6 | 7 | 0.205 | 3.21e-07 (2^-21.57) | 21.57 |
| 35 | `pipelined_m:data_width=26,n_iter=23,angle_guard=4,frac_guard=4,rounding=round,m=6` | 2286 | 438 | 59.9 | 6 | 0.205 | 2.81e-07 (2^-21.76) | 21.76 |
| 36 | `pipelined_m:data_width=26,n_iter=25,angle_guard=1,frac_guard=3,rounding=round,m=6` | 2361 | 513 | 59.9 | 7 | 0.216 | 2.78e-07 (2^-21.78) | 21.78 |
| 37 | `pipelined_m:data_width=28,n_iter=24,angle_guard=0,frac_guard=2,rounding=round,m=5` | 2342 | 534 | 70.6 | 7 | 0.216 | 2.22e-07 (2^-22.11) | 22.11 |
| 38 | `pipelined_m:data_width=28,n_iter=27,angle_guard=1,frac_guard=1,rounding=round,m=7` | 2612 | 436 | 52.0 | 6 | 0.229 | 8.92e-08 (2^-23.42) | 23.42 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraint is sys_p99_latency_us <= 0.4 with 8-request bursts: a design must drain ~7 results plus pipeline latency inside 400 ns, so multi-cycle-per-result families (iterative, large-k unrolled) are at risk while 1-result/cycle pipelined_m is safe. Accuracy needs roughly W>=12 and N>=10 (output LSB 2^-(W-2) plus CORDIC residual ~2^-N), so I search W 12..18 and N 8..18 to let the model locate the accuracy boundary. Area is the objective, so I weight pipelined_m (safe, but register-heavy) and unrolled_k (few FFs, moderate k) most heavily, keep iterative small to test the cheap corner, and keep pipelined for high-Fmax coverage; guards and rounding are left open since they trade area for the accuracy margin the constraint demands.*)
- `iterative` (10 evals): data_width=12..18, n_iter=8..18, angle_guard=-2..2, frac_guard=0..3, rounding=trunc|round. *Why:* Cheapest area family, but N+3 cycles/result makes it hard to drain an 8-request burst inside 0.4 us; a small share confirms whether any high-Fmax/low-N point survives the L1 p99 bound and anchors the low-area end of the front.
- `unrolled_k` (35 evals): data_width=12..18, n_iter=8..18, angle_guard=-2..2, frac_guard=0..3, rounding=trunc|round, k=2..8. *Why:* Shares one datapath (few FFs) while cutting cycles/result to ceil(N/k)+3, so small-to-mid k can plausibly meet the burst p99 with much lower area than a full pipeline; this is the most likely min-luts+ffs corner.
- `pipelined_m` (40 evals): data_width=12..18, n_iter=8..18, angle_guard=-2..2, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* One result/cycle at every m, so bursts drain in ~7 cycles regardless of Fmax; register-every-m trades FFs for latency and is the safest family against the tight (and optimistic) L1 p99 bound, giving the L2 shortlist real headroom.
- `pipelined` (15 evals): data_width=12..18, n_iter=8..18, angle_guard=-2..2, frac_guard=0..3, rounding=trunc|round. *Why:* Shortest critical path (one micro-rotation/stage) gives the highest Fmax and lowest latency_ns per cycle, useful for the high-accuracy/high-throughput end of the trade-off curve even though its per-stage registers make it area-expensive.

**Result (code):** 100 evaluations this round, 100 total; 30 feasible; hypervolume 7504 (n/a).

**LLM decision:** `refine` — The whole feasible front is pipelined_m; iterative (0/10) and unrolled_k (0/35) never pass sys_p99_latency_us (max throughput seen 18 and 14.4 MSPS, below the ~20 MSPS needed to drain an 8-request burst inside 0.4 us), and pipelined's best feasible luts_plus_ffs=1810 is far worse than pipelined_m's 1001, so budget belongs on pipelined_m. The front spans only luts_plus_ffs 1001..1440 against HV ref 3000 and accuracy_bits 11.8..14 against ref 10; the single top point (1440, 14.04) alone contributes ~6300 of the 7504 HV, so pushing accuracy higher is the dominant hypervolume lever, while the cheapest feasible design (1001) drives the min-luts_plus_ffs selection rule. Accuracy at data_width=18/n_iter=13 is 11.76 bits, well above the 2^-10 constraint, and the error is n_iter-limited rather than width-limited, so smaller data_width should cut area at little accuracy cost. I therefore widen the explored box in both directions: down to data_width 12 (the smallest width whose output LSB still allows >10 bits) with n_iter 12..16 for cheaper feasible designs, and up to data_width 24 / n_iter 28 to extend the high-accuracy end of the front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 7504 (gain this round: n/a (first round)).
Feasible designs: 30 of 100 evaluations (25 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 44% violate; best seen 5.95e-05 (2^-14.04)
- sys_p99_latency_us <= 0.4: 45% violate; best seen 0.0605

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=13 angle_guard=1 frac_guard=0 rounding=round m=5] luts_plus_ffs=1001, accuracy_bits=11.8, luts=777, ffs=224, throughput_msps=77, max_abs_err=0.000289 (2^-11.76), power_index=0.0753
- pipelined_m [data_width=18 n_iter=13 angle_guard=1 frac_guard=1 rounding=round m=5] luts_plus_ffs=1070, accuracy_bits=11.8, luts=840, ffs=230, throughput_msps=77, max_abs_err=0.000279 (2^-11.81), power_index=0.0805
- pipelined_m [data_width=18 n_iter=13 angle_guard=1 frac_guard=2 rounding=round m=5] luts_plus_ffs=1099, accuracy_bits=11.8, luts=865, ffs=234, throughput_msps=77, max_abs_err=0.000272 (2^-11.84), power_index=0.0827
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=3 rounding=round m=5] luts_plus_ffs=1145, accuracy_bits=12.5, luts=918, ffs=227, throughput_msps=77, max_abs_err=0.000168 (2^-12.54), power_index=0.0861
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=5] luts_plus_ffs=1203, accuracy_bits=13.3, luts=973, ffs=230, throughput_msps=77, max_abs_err=0.000101 (2^-13.27), power_index=0.0905
- pipelined_m [data_width=18 n_iter=17 angle_guard=1 frac_guard=0 rounding=round m=6] luts_plus_ffs=1258, accuracy_bits=13.4, luts=1034, ffs=224, throughput_msps=65.4, max_abs_err=9.26e-05 (2^-13.40), power_index=0.0946
- pipelined_m [data_width=18 n_iter=17 angle_guard=1 frac_guard=2 rounding=round m=5] luts_plus_ffs=1440, accuracy_bits=14, luts=1139, ffs=301, throughput_msps=77, max_abs_err=5.95e-05 (2^-14.04), power_index=0.108
Front coverage: luts_plus_ffs 1001..1440 (HV reference 3000); accuracy_bits 11.8..14 (HV reference 10); data_width on the front 17..18 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 18 MSPS; best accuracy 12.19 bits
- unrolled_k: 35 evals, 0 feasible; max throughput seen 14.4 MSPS; best accuracy 13.60 bits
- pipelined: 15 evals, 4 feasible; max throughput seen 282 MSPS; best accuracy 12.45 bits; best feasible luts_plus_ffs=1810; feasible ranges: data_width 16..18, n_iter 16..18, angle_guard -2..1, frac_guard 0..2
- pipelined_m: 40 evals, 26 feasible; max throughput seen 171 MSPS; best accuracy 14.04 bits; best feasible luts_plus_ffs=1001; feasible ranges: data_width 16..18, n_iter 13..18, angle_guard -2..2, frac_guard 0..3, m 2..7
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Single-family refine of pipelined_m over data_width 12..24, n_iter 12..28, angle_guard -2..2, frac_guard 0..3, rounding {round,trunc}, m 2..8, seeded by the current 7-point front, to extend the trade-off curve at both the low-area and high-accuracy ends before the reserved map_front round.*)
- `pipelined_m` (100 evals): data_width=12..24, n_iter=12..28, angle_guard=-2..2, frac_guard=0..3, rounding=round|trunc, m=2..8. *Why:* Only family with feasible designs (26/40) and the only one on the front; widen data_width/n_iter both below the current front (cheaper feasible designs for the selection rule) and above it (higher accuracy_bits, which carries ~84% of the hypervolume).

**Result (code):** 100 evaluations this round, 200 total; 118 feasible; hypervolume 1.431e+04 (+90.7%).

**LLM decision:** `map_front` — The feasible front is essentially single-family: all 26 Pareto designs are pipelined_m, while pipelined contributes only 4 feasible designs (best luts_plus_ffs=1810, dominated by 871) and iterative/unrolled_k contribute 0 feasible (their multi-cycle schedules blow the sys_p99_latency bound despite throughput >= 2). The front spans luts_plus_ffs 871..2658 against HV ref 3000 and accuracy_bits 10.7..20.5 against ref 10, but data_width on the front is only 15..24 of the registry's 8..28, so both the cheap/low-accuracy end (which the min-luts_plus_ffs selection rule cares about) and the high-accuracy tail are unmapped. With 200 evals and 2 rounds left, this is the right moment to spend the reserved budget on a code-driven NSGA-II coverage search over the full ranges of pipelined_m and pipelined, seeded with the current front, to fill the whole trade-off curve before the final refinement round.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.431e+04 (gain this round: +90.7%).
Feasible designs: 118 of 200 evaluations (109 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 28% violate; best seen 6.77e-07 (2^-20.50)
- sys_p99_latency_us <= 0.4: 22% violate; best seen 0.0605

Pareto front (feasible, 26 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=8] luts_plus_ffs=871, accuracy_bits=10.7, luts=731, ffs=139, throughput_msps=52.7, max_abs_err=0.000599 (2^-10.71), power_index=0.0655
- pipelined_m [data_width=18 n_iter=13 angle_guard=1 frac_guard=1 rounding=round m=5] luts_plus_ffs=1070, accuracy_bits=11.8, luts=840, ffs=230, throughput_msps=77, max_abs_err=0.000279 (2^-11.81), power_index=0.0805
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=3 rounding=round m=5] luts_plus_ffs=1145, accuracy_bits=12.5, luts=918, ffs=227, throughput_msps=77, max_abs_err=0.000168 (2^-12.54), power_index=0.0861
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=5] luts_plus_ffs=1203, accuracy_bits=13.3, luts=973, ffs=230, throughput_msps=77, max_abs_err=0.000101 (2^-13.27), power_index=0.0905
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1337, accuracy_bits=14.1, luts=1033, ffs=305, throughput_msps=93.6, max_abs_err=5.75e-05 (2^-14.09), power_index=0.101
- pipelined_m [data_width=21 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1536, accuracy_bits=14.8, luts=1191, ffs=345, throughput_msps=89.6, max_abs_err=3.41e-05 (2^-14.84), power_index=0.116
- pipelined_m [data_width=21 n_iter=18 angle_guard=2 frac_guard=0 rounding=round m=5] luts_plus_ffs=1610, accuracy_bits=15.9, luts=1277, ffs=333, throughput_msps=73.7, max_abs_err=1.59e-05 (2^-15.94), power_index=0.121
- pipelined_m [data_width=24 n_iter=18 angle_guard=1 frac_guard=0 rounding=round m=5] luts_plus_ffs=1792, accuracy_bits=16.9, luts=1420, ffs=371, throughput_msps=73.7, max_abs_err=8.41e-06 (2^-16.86), power_index=0.135
- pipelined_m [data_width=24 n_iter=23 angle_guard=2 frac_guard=0 rounding=trunc m=8] luts_plus_ffs=2153, accuracy_bits=18.4, luts=1860, ffs=294, throughput_msps=48, max_abs_err=2.96e-06 (2^-18.37), power_index=0.162
- pipelined_m [data_width=24 n_iter=26 angle_guard=2 frac_guard=2 rounding=round m=8] luts_plus_ffs=2658, accuracy_bits=20.5, luts=2269, ffs=389, throughput_msps=48, max_abs_err=6.77e-07 (2^-20.50), power_index=0.2
Front coverage: luts_plus_ffs 871..2658 (HV reference 3000); accuracy_bits 10.7..20.5 (HV reference 10); data_width on the front 15..24 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 18 MSPS; best accuracy 12.19 bits
- unrolled_k: 35 evals, 0 feasible; max throughput seen 14.4 MSPS; best accuracy 13.60 bits
- pipelined: 15 evals, 4 feasible; max throughput seen 282 MSPS; best accuracy 12.45 bits; best feasible luts_plus_ffs=1810; feasible ranges: data_width 16..18, n_iter 16..18, angle_guard -2..1, frac_guard 0..2
- pipelined_m: 140 evals, 114 feasible; max throughput seen 178 MSPS; best accuracy 20.50 bits; best feasible luts_plus_ffs=871; feasible ranges: data_width 15..24, n_iter 12..28, angle_guard -2..2, frac_guard 0..3, m 2..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (26 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 240 total; 153 feasible; hypervolume 1.477e+04 (+3.2%).

**LLM decision:** `map_front` — The feasible front is essentially a single family (pipelined_m: 149 of 153 feasible designs; pipelined's best feasible luts_plus_ffs=1810 is dominated), and it is truncated at the cheap end: data_width on the front spans only 15..26 of the registry's 8..28, while the selection rule is min luts_plus_ffs and the cheapest point is 871 LUT+FF at 10.7 accuracy bits. The constraint only needs max_abs_err <= 2^-10, so the unexplored data_width 8..14 region (with more n_iter / guard bits to recover the 10 bits) is exactly where a cheaper winner may sit, and it is also the region that would extend HV coverage below the current 871 floor. The 19% sys_p99_latency violation rate and best value 0.0605 us also mean the cheap, low-throughput corner needs several near-equivalent candidates so that L2 simulation does not eliminate the single cheapest design. With 160 of 400 evals left, hand this round to the code-driven NSGA-II coverage search over the full ranges of the families on the front (pipelined_m, pipelined), seeded with the current 30-design front, to map the whole trade-off curve before the final selection.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 1.477e+04 (gain this round: +3.2%).
Feasible designs: 153 of 240 evaluations (141 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 25% violate; best seen 3.21e-07 (2^-21.57)
- sys_p99_latency_us <= 0.4: 19% violate; best seen 0.0605

Pareto front (feasible, 30 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=8] luts_plus_ffs=871, accuracy_bits=10.7, luts=731, ffs=139, throughput_msps=52.7, max_abs_err=0.000599 (2^-10.71), power_index=0.0655
- pipelined_m [data_width=18 n_iter=13 angle_guard=1 frac_guard=1 rounding=round m=5] luts_plus_ffs=1070, accuracy_bits=11.8, luts=840, ffs=230, throughput_msps=77, max_abs_err=0.000279 (2^-11.81), power_index=0.0805
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=3 rounding=round m=5] luts_plus_ffs=1145, accuracy_bits=12.5, luts=918, ffs=227, throughput_msps=77, max_abs_err=0.000168 (2^-12.54), power_index=0.0861
- pipelined_m [data_width=20 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round m=6] luts_plus_ffs=1273, accuracy_bits=13.8, luts=1033, ffs=240, throughput_msps=65.4, max_abs_err=6.98e-05 (2^-13.81), power_index=0.0958
- pipelined_m [data_width=20 n_iter=18 angle_guard=0 frac_guard=0 rounding=trunc m=5] luts_plus_ffs=1498, accuracy_bits=14.4, luts=1188, ffs=311, throughput_msps=77, max_abs_err=4.53e-05 (2^-14.43), power_index=0.113
- pipelined_m [data_width=21 n_iter=18 angle_guard=1 frac_guard=1 rounding=trunc m=8] luts_plus_ffs=1556, accuracy_bits=15.8, luts=1295, ffs=261, throughput_msps=50.3, max_abs_err=1.73e-05 (2^-15.82), power_index=0.117
- pipelined_m [data_width=24 n_iter=18 angle_guard=1 frac_guard=0 rounding=round m=5] luts_plus_ffs=1792, accuracy_bits=16.9, luts=1420, ffs=371, throughput_msps=73.7, max_abs_err=8.41e-06 (2^-16.86), power_index=0.135
- pipelined_m [data_width=25 n_iter=19 angle_guard=4 frac_guard=2 rounding=round m=8] luts_plus_ffs=2067, accuracy_bits=18, luts=1746, ffs=321, throughput_msps=45.9, max_abs_err=3.94e-06 (2^-17.95), power_index=0.155
- pipelined_m [data_width=25 n_iter=21 angle_guard=4 frac_guard=3 rounding=round m=6] luts_plus_ffs=2393, accuracy_bits=19.8, luts=1976, ffs=418, throughput_msps=59.9, max_abs_err=1.09e-06 (2^-19.81), power_index=0.18
- pipelined_m [data_width=26 n_iter=24 angle_guard=3 frac_guard=2 rounding=trunc m=5] luts_plus_ffs=2723, accuracy_bits=21.6, luts=2211, ffs=513, throughput_msps=70.6, max_abs_err=3.21e-07 (2^-21.57), power_index=0.205
Front coverage: luts_plus_ffs 871..2723 (HV reference 3000); accuracy_bits 10.7..21.6 (HV reference 10); data_width on the front 15..26 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 18 MSPS; best accuracy 12.19 bits
- unrolled_k: 35 evals, 0 feasible; max throughput seen 14.4 MSPS; best accuracy 13.60 bits
- pipelined: 15 evals, 4 feasible; max throughput seen 282 MSPS; best accuracy 12.45 bits; best feasible luts_plus_ffs=1810; feasible ranges: data_width 16..18, n_iter 16..18, angle_guard -2..1, frac_guard 0..2
- pipelined_m: 180 evals, 149 feasible; max throughput seen 178 MSPS; best accuracy 21.57 bits; best feasible luts_plus_ffs=871; feasible ranges: data_width 14..27, n_iter 12..29, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (30 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 340 total; 245 feasible; hypervolume 1.496e+04 (+1.3%).

**LLM decision:** `stop` — Final round (4/4, 340/400 evals): feasible designs exist in abundance (245 of 340 evaluations feasible, 226 unique), so `infeasible` is off the table — every constraint is met with large margin: throughput best 282 MSPS vs >=2, max_abs_err best 2^-22.67 vs <=2^-10, sys_p99_latency best 0.0605 us vs <=0.4 us. The Pareto front already spans both objectives well: luts_plus_ffs 871..3620 (HV ref 3000) and accuracy_bits 10.7..22.7 (HV ref 10), i.e. the cheap corner and the high-accuracy corner are both covered, and all four families have been explored (none left to add). The last round's HV gain was only +1.3% (1.496e+04), i.e. the front has plateaued, and with a round/budget cap reached further search would be marginal. Per the selection rule (min luts_plus_ffs), the chosen design is pipelined_m[data_width=15, n_iter=14, angle_guard=2, frac_guard=0, rounding=round, m=8]: luts_plus_ffs=871, accuracy_bits=10.7 (max_abs_err=5.99e-4 <= 0.0009766), throughput_msps=52.7 (>=2), and it is the min-area corner of the feasible front. Note the system caveat: L1 system bounds are optimistic, so the L2 SimPy re-selection on the shortlist is the final arbiter for the bursty scenario; the selected design's p99 headroom (front designs pass at 0.0605 us vs the 0.4 us bound) gives it ample margin to survive L2. No further architecture exploration is warranted.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 60 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 340 of 400.
Hypervolume of the feasible front: 1.496e+04 (gain this round: +1.3%).
Feasible designs: 245 of 340 evaluations (226 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 20% violate; best seen 1.5e-07 (2^-22.67)
- sys_p99_latency_us <= 0.4: 13% violate; best seen 0.0605

Pareto front (feasible, 36 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=8] luts_plus_ffs=871, accuracy_bits=10.7, luts=731, ffs=139, throughput_msps=52.7, max_abs_err=0.000599 (2^-10.71), power_index=0.0655
- pipelined_m [data_width=20 n_iter=13 angle_guard=1 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1099, accuracy_bits=11.9, luts=852, ffs=246, throughput_msps=65.4, max_abs_err=0.000263 (2^-11.90), power_index=0.0827
- pipelined_m [data_width=18 n_iter=17 angle_guard=1 frac_guard=0 rounding=round m=6] luts_plus_ffs=1258, accuracy_bits=13.4, luts=1034, ffs=224, throughput_msps=65.4, max_abs_err=9.26e-05 (2^-13.40), power_index=0.0946
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1413, accuracy_bits=14.3, luts=1096, ffs=317, throughput_msps=93.6, max_abs_err=4.81e-05 (2^-14.34), power_index=0.106
- pipelined_m [data_width=20 n_iter=18 angle_guard=2 frac_guard=0 rounding=round m=5] luts_plus_ffs=1542, accuracy_bits=15.3, luts=1223, ffs=319, throughput_msps=77, max_abs_err=2.42e-05 (2^-15.34), power_index=0.116
- pipelined_m [data_width=24 n_iter=18 angle_guard=1 frac_guard=0 rounding=trunc m=8] luts_plus_ffs=1711, accuracy_bits=16.7, luts=1420, ffs=291, throughput_msps=48, max_abs_err=9.16e-06 (2^-16.74), power_index=0.129
- pipelined_m [data_width=23 n_iter=21 angle_guard=0 frac_guard=1 rounding=round m=8] luts_plus_ffs=1959, accuracy_bits=17.9, luts=1677, ffs=282, throughput_msps=48, max_abs_err=4.01e-06 (2^-17.93), power_index=0.147
- pipelined_m [data_width=24 n_iter=23 angle_guard=2 frac_guard=0 rounding=round m=5] luts_plus_ffs=2317, accuracy_bits=19.3, luts=1860, ffs=457, throughput_msps=73.7, max_abs_err=1.57e-06 (2^-19.28), power_index=0.174
- pipelined_m [data_width=25 n_iter=24 angle_guard=0 frac_guard=2 rounding=trunc m=5] luts_plus_ffs=2546, accuracy_bits=19.9, luts=2065, ffs=480, throughput_msps=70.6, max_abs_err=9.91e-07 (2^-19.94), power_index=0.192
- pipelined_m [data_width=28 n_iter=24 angle_guard=2 frac_guard=2 rounding=round m=2] luts_plus_ffs=3620, accuracy_bits=22.7, luts=2391, ffs=1229, throughput_msps=153, max_abs_err=1.5e-07 (2^-22.67), power_index=0.272
Front coverage: luts_plus_ffs 871..3620 (HV reference 3000); accuracy_bits 10.7..22.7 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 18 MSPS; best accuracy 12.19 bits
- unrolled_k: 35 evals, 0 feasible; max throughput seen 14.4 MSPS; best accuracy 13.60 bits
- pipelined: 15 evals, 4 feasible; max throughput seen 282 MSPS; best accuracy 12.45 bits; best feasible luts_plus_ffs=1810; feasible ranges: data_width 16..18, n_iter 16..18, angle_guard -2..1, frac_guard 0..2
- pipelined_m: 280 evals, 241 feasible; max throughput seen 178 MSPS; best accuracy 22.67 bits; best feasible luts_plus_ffs=871; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

### Round 5

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 60 evaluations*)
- `pipelined_m` (60 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (36 front designs; box front_anchored)

**Result (code):** 60 evaluations this round, 400 total; 301 feasible; hypervolume 1.524e+04 (+1.8%).

**No LLM call** (code's front-mapping round): Final round (4/4, 340/400 evals): feasible designs exist in abundance (245 of 340 evaluations feasible, 226 unique), so `infeasible` is off the table — every constraint is met with large margin: throughput best 282 MSPS vs >=2, max_abs_err best 2^-22.67 vs <=2^-10, sys_p99_latency best 0.0605 us vs <=0.4 us. The Pareto front already spans both objectives well: luts_plus_ffs 871..3620 (HV ref 3000) and accuracy_bits 10.7..22.7 (HV ref 10), i.e. the cheap corner and the high-accuracy corner are both covered, and all four families have been explored (none left to add). The last round's HV gain was only +1.3% (1.496e+04), i.e. the front has plateaued, and with a round/budget cap reached further search would be marginal. Per the selection rule (min luts_plus_ffs), the chosen design is pipelined_m[data_width=15, n_iter=14, angle_guard=2, frac_guard=0, rounding=round, m=8]: luts_plus_ffs=871, accuracy_bits=10.7 (max_abs_err=5.99e-4 <= 0.0009766), throughput_msps=52.7 (>=2), and it is the min-area corner of the feasible front. Note the system caveat: L1 system bounds are optimistic, so the L2 SimPy re-selection on the shortlist is the final arbiter for the bursty scenario; the selected design's p99 headroom (front designs pass at 0.0605 us vs the 0.4 us bound) gives it ample margin to survive L2. No further architecture exploration is warranted.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 5 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.524e+04 (gain this round: +1.8%).
Feasible designs: 301 of 400 evaluations (278 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 18% violate; best seen 8.92e-08 (2^-23.42)
- sys_p99_latency_us <= 0.4: 11% violate; best seen 0.0605

Pareto front (feasible, 39 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=0 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=782, accuracy_bits=10, luts=643, ffs=139, throughput_msps=59.6, max_abs_err=0.000962 (2^-10.02), power_index=0.0588
- pipelined_m [data_width=18 n_iter=13 angle_guard=1 frac_guard=0 rounding=round m=5] luts_plus_ffs=1001, accuracy_bits=11.8, luts=777, ffs=224, throughput_msps=77, max_abs_err=0.000289 (2^-11.76), power_index=0.0753
- pipelined_m [data_width=19 n_iter=14 angle_guard=4 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=1128, accuracy_bits=12.8, luts=950, ffs=178, throughput_msps=54.3, max_abs_err=0.000143 (2^-12.77), power_index=0.0849
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1337, accuracy_bits=14.1, luts=1033, ffs=305, throughput_msps=93.6, max_abs_err=5.75e-05 (2^-14.09), power_index=0.101
- pipelined_m [data_width=22 n_iter=16 angle_guard=-1 frac_guard=2 rounding=round m=7] luts_plus_ffs=1510, accuracy_bits=14.7, luts=1237, ffs=272, throughput_msps=54.3, max_abs_err=3.75e-05 (2^-14.70), power_index=0.114
- pipelined_m [data_width=21 n_iter=18 angle_guard=2 frac_guard=0 rounding=round m=5] luts_plus_ffs=1610, accuracy_bits=15.9, luts=1277, ffs=333, throughput_msps=73.7, max_abs_err=1.59e-05 (2^-15.94), power_index=0.121
- pipelined_m [data_width=25 n_iter=19 angle_guard=1 frac_guard=0 rounding=trunc m=8] luts_plus_ffs=1862, accuracy_bits=17.7, luts=1561, ffs=302, throughput_msps=48, max_abs_err=4.66e-06 (2^-17.71), power_index=0.14
- pipelined_m [data_width=24 n_iter=23 angle_guard=2 frac_guard=0 rounding=round m=5] luts_plus_ffs=2317, accuracy_bits=19.3, luts=1860, ffs=457, throughput_msps=73.7, max_abs_err=1.57e-06 (2^-19.28), power_index=0.174
- pipelined_m [data_width=26 n_iter=24 angle_guard=3 frac_guard=2 rounding=trunc m=5] luts_plus_ffs=2723, accuracy_bits=21.6, luts=2211, ffs=513, throughput_msps=70.6, max_abs_err=3.21e-07 (2^-21.57), power_index=0.205
- pipelined_m [data_width=28 n_iter=27 angle_guard=1 frac_guard=1 rounding=round m=7] luts_plus_ffs=3048, accuracy_bits=23.4, luts=2612, ffs=436, throughput_msps=52, max_abs_err=8.92e-08 (2^-23.42), power_index=0.229
Front coverage: luts_plus_ffs 782..3048 (HV reference 3000); accuracy_bits 10..23.4 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 18 MSPS; best accuracy 12.19 bits
- unrolled_k: 35 evals, 0 feasible; max throughput seen 14.4 MSPS; best accuracy 13.60 bits
- pipelined: 15 evals, 4 feasible; max throughput seen 282 MSPS; best accuracy 12.45 bits; best feasible luts_plus_ffs=1810; feasible ranges: data_width 16..18, n_iter 16..18, angle_guard -2..1, frac_guard 0..2
- pipelined_m: 340 evals, 297 feasible; max throughput seen 178 MSPS; best accuracy 23.42 bits; best feasible luts_plus_ffs=782; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 32765 in, 22230 out
- provider-reported cost: $0.0168
- full prompts and replies: `llm_trace.jsonl`

