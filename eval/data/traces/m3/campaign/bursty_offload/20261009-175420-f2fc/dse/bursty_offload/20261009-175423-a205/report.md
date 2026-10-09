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
`pipelined_m:data_width=16,n_iter=12,angle_guard=-1,frac_guard=1,rounding=trunc,m=6` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 643 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 143 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 68.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 68.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 58.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0591 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000901 (2^-10.12) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 14.8 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000246 (2^-11.99) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 4.04 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.1 | exact: bit-accurate model, exhaustive (65536 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 4 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 80.1 dBc, SNR 69.4 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: bursty requests: bursts of 8 (0 ns apart) arriving as a Poisson process, 2 requests/us on average. Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_latency_us <= 0.4 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=16,n_iter=12,angle_guard=-1,frac_guard=1,rounding=trunc,m=6` | 0.1459 → 0.1953 | yes |
| `pipelined_m:data_width=16,n_iter=12,angle_guard=-1,frac_guard=1,rounding=trunc,m=7` | 0.1678 → 0.2328 | yes |
| `pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=3,rounding=trunc,m=6` | 0.1459 → 0.1953 | yes |
| `pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=3,rounding=trunc,m=7` | 0.1678 → 0.2328 | yes |
| `pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=2,rounding=round,m=8` | 0.1896 → 0.2667 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (43 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=12,angle_guard=-1,frac_guard=1,rounding=trunc,m=6` | 643 | 143 | 68.5 | 4 | 0.0591 | 0.000901 (2^-10.12) | 10.12 |
| 1 | `pipelined_m:data_width=16,n_iter=12,angle_guard=-1,frac_guard=1,rounding=trunc,m=7` | 643 | 143 | 59.6 | 4 | 0.0591 | 0.000901 (2^-10.12) | 10.12 |
| 2 | `pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=3,rounding=trunc,m=6` | 654 | 137 | 68.5 | 4 | 0.0596 | 0.000894 (2^-10.13) | 10.13 |
| 3 | `pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=3,rounding=trunc,m=7` | 654 | 137 | 59.6 | 4 | 0.0596 | 0.000894 (2^-10.13) | 10.13 |
| 4 | `pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=2,rounding=round,m=8` | 661 | 137 | 52.7 | 4 | 0.06 | 0.000825 (2^-10.24) | 10.24 |
| 5 | `pipelined_m:data_width=16,n_iter=13,angle_guard=-1,frac_guard=1,rounding=trunc,m=7` | 701 | 143 | 59.6 | 4 | 0.0635 | 0.000761 (2^-10.36) | 10.36 |
| 6 | `pipelined_m:data_width=17,n_iter=12,angle_guard=-1,frac_guard=2,rounding=trunc,m=8` | 701 | 153 | 50.3 | 4 | 0.0643 | 0.000682 (2^-10.52) | 10.52 |
| 7 | `pipelined_m:data_width=17,n_iter=12,angle_guard=1,frac_guard=2,rounding=trunc,m=6` | 724 | 157 | 65.4 | 4 | 0.0663 | 0.000545 (2^-10.84) | 10.84 |
| 8 | `pipelined_m:data_width=16,n_iter=13,angle_guard=2,frac_guard=1,rounding=round,m=7` | 772 | 151 | 59.6 | 4 | 0.0695 | 0.000325 (2^-11.59) | 11.59 |
| 9 | `pipelined_m:data_width=19,n_iter=13,angle_guard=-1,frac_guard=1,rounding=trunc,m=8` | 815 | 167 | 50.3 | 4 | 0.0739 | 0.000296 (2^-11.72) | 11.72 |
| 10 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=7` | 855 | 157 | 56.8 | 4 | 0.0761 | 0.000204 (2^-12.26) | 12.26 |
| 11 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=3,rounding=round,m=6` | 888 | 219 | 65.4 | 5 | 0.0833 | 0.000187 (2^-12.38) | 12.38 |
| 12 | `pipelined_m:data_width=19,n_iter=14,angle_guard=-1,frac_guard=1,rounding=trunc,m=4` | 882 | 299 | 93.6 | 6 | 0.0888 | 0.000179 (2^-12.45) | 12.45 |
| 13 | `pipelined_m:data_width=23,n_iter=14,angle_guard=-1,frac_guard=0,rounding=round,m=7` | 1019 | 198 | 54.3 | 4 | 0.0915 | 0.000124 (2^-12.98) | 12.98 |
| 14 | `pipelined_m:data_width=18,n_iter=17,angle_guard=0,frac_guard=0,rounding=round,m=7` | 1017 | 221 | 59.6 | 5 | 0.0931 | 0.000114 (2^-13.10) | 13.10 |
| 15 | `pipelined_m:data_width=16,n_iter=17,angle_guard=3,frac_guard=4,rounding=trunc,m=7` | 1101 | 224 | 56.8 | 5 | 0.0997 | 0.00011 (2^-13.15) | 13.15 |
| 16 | `pipelined_m:data_width=18,n_iter=17,angle_guard=1,frac_guard=2,rounding=trunc,m=7` | 1101 | 232 | 56.8 | 5 | 0.1 | 6.92e-05 (2^-13.82) | 13.82 |
| 17 | `pipelined_m:data_width=20,n_iter=17,angle_guard=1,frac_guard=0,rounding=trunc,m=6` | 1135 | 246 | 65.4 | 5 | 0.104 | 4.89e-05 (2^-14.32) | 14.32 |
| 18 | `pipelined_m:data_width=21,n_iter=16,angle_guard=-1,frac_guard=2,rounding=trunc,m=6` | 1143 | 259 | 62.5 | 5 | 0.106 | 4.68e-05 (2^-14.38) | 14.38 |
| 19 | `pipelined_m:data_width=22,n_iter=16,angle_guard=4,frac_guard=0,rounding=round,m=8` | 1207 | 200 | 48.0 | 4 | 0.106 | 3.3e-05 (2^-14.89) | 14.89 |
| 20 | `pipelined_m:data_width=21,n_iter=18,angle_guard=0,frac_guard=0,rounding=round,m=6` | 1241 | 254 | 65.4 | 5 | 0.113 | 2.12e-05 (2^-15.53) | 15.53 |
| 21 | `pipelined_m:data_width=24,n_iter=17,angle_guard=-1,frac_guard=2,rounding=trunc,m=7` | 1371 | 293 | 54.3 | 5 | 0.125 | 1.68e-05 (2^-15.86) | 15.86 |
| 22 | `pipelined_m:data_width=23,n_iter=17,angle_guard=3,frac_guard=1,rounding=round,m=6` | 1403 | 292 | 62.5 | 5 | 0.127 | 1.61e-05 (2^-15.92) | 15.92 |
| 23 | `pipelined_m:data_width=23,n_iter=17,angle_guard=4,frac_guard=1,rounding=round,m=8` | 1419 | 295 | 45.9 | 5 | 0.129 | 1.59e-05 (2^-15.94) | 15.94 |
| 24 | `pipelined_m:data_width=23,n_iter=17,angle_guard=3,frac_guard=2,rounding=round,m=8` | 1436 | 296 | 48.0 | 5 | 0.13 | 1.57e-05 (2^-15.96) | 15.96 |
| 25 | `pipelined_m:data_width=25,n_iter=17,angle_guard=2,frac_guard=1,rounding=trunc,m=8` | 1438 | 309 | 45.9 | 5 | 0.131 | 1.54e-05 (2^-15.98) | 15.98 |
| 26 | `pipelined_m:data_width=25,n_iter=17,angle_guard=3,frac_guard=1,rounding=round,m=8` | 1508 | 314 | 45.9 | 5 | 0.137 | 1.53e-05 (2^-15.99) | 15.99 |
| 27 | `pipelined_m:data_width=22,n_iter=19,angle_guard=0,frac_guard=1,rounding=round,m=4` | 1455 | 423 | 89.6 | 7 | 0.141 | 8.92e-06 (2^-16.77) | 16.77 |
| 28 | `pipelined_m:data_width=24,n_iter=21,angle_guard=-1,frac_guard=0,rounding=trunc,m=7` | 1628 | 285 | 54.3 | 5 | 0.144 | 4.38e-06 (2^-17.80) | 17.80 |
| 29 | `pipelined_m:data_width=25,n_iter=20,angle_guard=0,frac_guard=0,rounding=trunc,m=5` | 1627 | 381 | 73.7 | 6 | 0.151 | 2.92e-06 (2^-18.39) | 18.39 |
| 30 | `pipelined_m:data_width=23,n_iter=22,angle_guard=3,frac_guard=0,rounding=round,m=7` | 1731 | 365 | 54.3 | 6 | 0.158 | 2.9e-06 (2^-18.39) | 18.39 |
| 31 | `pipelined_m:data_width=22,n_iter=21,angle_guard=4,frac_guard=3,rounding=trunc,m=6` | 1733 | 373 | 62.5 | 6 | 0.158 | 2.61e-06 (2^-18.55) | 18.55 |
| 32 | `pipelined_m:data_width=24,n_iter=21,angle_guard=3,frac_guard=4,rounding=trunc,m=7` | 1881 | 313 | 52.0 | 5 | 0.165 | 1.37e-06 (2^-19.47) | 19.47 |
| 33 | `pipelined_m:data_width=24,n_iter=22,angle_guard=3,frac_guard=1,rounding=round,m=7` | 1893 | 387 | 52.0 | 6 | 0.172 | 1.23e-06 (2^-19.63) | 19.63 |
| 34 | `pipelined_m:data_width=24,n_iter=23,angle_guard=4,frac_guard=2,rounding=trunc,m=8` | 1999 | 308 | 45.9 | 5 | 0.174 | 9.38e-07 (2^-20.02) | 20.02 |
| 35 | `pipelined_m:data_width=24,n_iter=25,angle_guard=3,frac_guard=1,rounding=round,m=7` | 2155 | 387 | 52.0 | 6 | 0.191 | 9.16e-07 (2^-20.06) | 20.06 |
| 36 | `pipelined_m:data_width=28,n_iter=24,angle_guard=-1,frac_guard=1,rounding=trunc,m=8` | 2211 | 333 | 45.9 | 5 | 0.191 | 3.05e-07 (2^-21.64) | 21.64 |
| 37 | `pipelined_m:data_width=28,n_iter=24,angle_guard=3,frac_guard=0,rounding=round,m=8` | 2259 | 341 | 44.0 | 5 | 0.196 | 1.86e-07 (2^-22.36) | 22.36 |
| 38 | `pipelined_m:data_width=28,n_iter=24,angle_guard=3,frac_guard=1,rounding=round,m=8` | 2367 | 347 | 44.0 | 5 | 0.204 | 1.53e-07 (2^-22.64) | 22.64 |
| 39 | `pipelined_m:data_width=28,n_iter=24,angle_guard=4,frac_guard=3,rounding=round,m=8` | 2488 | 358 | 44.0 | 5 | 0.214 | 1.32e-07 (2^-22.85) | 22.85 |
| 40 | `pipelined_m:data_width=27,n_iter=25,angle_guard=3,frac_guard=3,rounding=round,m=8` | 2490 | 442 | 45.9 | 6 | 0.221 | 1.04e-07 (2^-23.20) | 23.20 |
| 41 | `pipelined_m:data_width=28,n_iter=28,angle_guard=3,frac_guard=1,rounding=trunc,m=8` | 2708 | 442 | 44.0 | 6 | 0.237 | 1e-07 (2^-23.25) | 23.25 |
| 42 | `pipelined_m:data_width=28,n_iter=26,angle_guard=2,frac_guard=4,rounding=trunc,m=3` | 2640 | 966 | 105.9 | 11 | 0.271 | 7.02e-08 (2^-23.76) | 23.76 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraints are max_abs_err<=2^-10 (needs W>=12 and N>=10) and sys_p99_latency_us<=0.4 for 8-request bursts, which is dominated by per-request service time: the last request in a burst waits ~7 service times, so service time must be well under ~50 ns. That rules out long-latency iterative designs unless Fmax is very high, but iterative is still worth a small share because it is the smallest-area family and would win the min-luts_plus_ffs selection if feasible. The real trade-off is service time vs area, so I weight unrolled_k (k=4..8) and pipelined_m (m=2..8) most heavily, with pipelined as the safe fast corner. data_width spans 12..20 and n_iter 10..22 so the front covers both the low-area/just-accurate corner and the high-accuracy end for hypervolume against ref (3000, 10); angle_guard and frac_guard are kept small since they only add area. Round 1 is deliberately broad across all four families; later rounds will narrow onto whichever families actually populate the feasible front and spend the reserved budget mapping their full ranges.*)
- `iterative` (17 evals): data_width=12..20, n_iter=10..22, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Smallest-area family, so it would win the min-luts_plus_ffs objective outright if it can meet the p99 burst-latency bound; a modest share confirms or rules it out cheaply. W>=12 is needed for the 2^-10 error limit, and N>=10 for the CORDIC residual.
- `unrolled_k` (34 evals): data_width=12..20, n_iter=10..22, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=2..8. *Why:* Likely sweet spot: k chained micro-rotations cut service time to ceil(N/k)+3 cycles while keeping one shared register set, so area stays well below pipelined. k in 4..8 should give enough burst headroom (8-request burst served in ~5-6 cycles/result).
- `pipelined_m` (33 evals): data_width=12..20, n_iter=10..22, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* One result/cycle throughput makes burst queueing negligible, and registering every m stages trades Fmax for fewer FFs than full pipelining, so it may undercut pipelined on luts_plus_ffs while still passing the latency bound.
- `pipelined` (16 evals): data_width=12..20, n_iter=10..22, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Guaranteed 1 result/cycle and shortest combinational path, so it is the safe latency corner of the front; included mainly to anchor the high-area end of the trade-off curve for hypervolume.

**Result (code):** 100 evaluations this round, 100 total; 32 feasible; hypervolume 8135 (n/a).

**LLM decision:** `refine` — All 10 feasible Pareto designs are pipelined_m; iterative and unrolled_k have 0 feasible points out of 51 evaluations (their best throughput 12.7 and 11.7 MSPS cannot drain an 8-request burst inside the 0.4 us p99 budget) and pipelined's cheapest feasible point is 2029 luts_plus_ffs versus 864 for pipelined_m, so those three families should not receive further budget now. The front covers luts_plus_ffs 864..1381 against an HV reference of 3000 and accuracy_bits 10..14.32 against a feasible maximum of 15.24, so both tails are still open; since accuracy is family-independent given the same data_width/n_iter/guard/rounding settings, pipelined_m can cover the accuracy tail more cheaply than any other family. The system constraint has a large margin (best sys_p99_latency_us 0.066 against 0.4) and throughput is far above the 2 MSPS floor (best 282 MSPS), so the binding constraint in the regions to search is max_abs_err <= 2^-10, which 30% of evaluations already met. A focused refine on the cheap-small-datapath box and the high-accuracy box should add the most hypervolume before a full-range mapping round is spent.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 8135 (gain this round: n/a (first round)).
Feasible designs: 32 of 100 evaluations (29 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 30% violate; best seen 2.58e-05 (2^-15.24)
- sys_p99_latency_us <= 0.4: 51% violate; best seen 0.066

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=864, accuracy_bits=10, luts=731, ffs=133, throughput_msps=59.6, max_abs_err=0.000944 (2^-10.05), power_index=0.065
- pipelined_m [data_width=17 n_iter=12 angle_guard=1 frac_guard=2 rounding=trunc m=6] luts_plus_ffs=881, accuracy_bits=10.8, luts=724, ffs=157, throughput_msps=65.4, max_abs_err=0.000545 (2^-10.84), power_index=0.0663
- pipelined_m [data_width=20 n_iter=12 angle_guard=-1 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=932, accuracy_bits=10.9, luts=759, ffs=174, throughput_msps=65.4, max_abs_err=0.000517 (2^-10.92), power_index=0.0701
- pipelined_m [data_width=19 n_iter=13 angle_guard=-1 frac_guard=1 rounding=trunc m=8] luts_plus_ffs=982, accuracy_bits=11.7, luts=815, ffs=167, throughput_msps=50.3, max_abs_err=0.000296 (2^-11.72), power_index=0.0739
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=1012, accuracy_bits=12.3, luts=855, ffs=157, throughput_msps=56.8, max_abs_err=0.000204 (2^-12.26), power_index=0.0761
- pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1147, accuracy_bits=12.3, luts=855, ffs=293, throughput_msps=93.6, max_abs_err=0.000193 (2^-12.34), power_index=0.0863
- pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1181, accuracy_bits=12.4, luts=882, ffs=299, throughput_msps=93.6, max_abs_err=0.000179 (2^-12.45), power_index=0.0888
- pipelined_m [data_width=18 n_iter=17 angle_guard=0 frac_guard=0 rounding=round m=7] luts_plus_ffs=1238, accuracy_bits=13.1, luts=1017, ffs=221, throughput_msps=59.6, max_abs_err=0.000114 (2^-13.10), power_index=0.0931
- pipelined_m [data_width=18 n_iter=17 angle_guard=1 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=1333, accuracy_bits=13.8, luts=1101, ffs=232, throughput_msps=56.8, max_abs_err=6.92e-05 (2^-13.82), power_index=0.1
- pipelined_m [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1381, accuracy_bits=14.3, luts=1135, ffs=246, throughput_msps=65.4, max_abs_err=4.89e-05 (2^-14.32), power_index=0.104
Front coverage: luts_plus_ffs 864..1381 (HV reference 3000); accuracy_bits 10..14.3 (HV reference 10); data_width on the front 14..20 (registry 8..28).

Per family:
- iterative: 17 evals, 0 feasible; max throughput seen 12.7 MSPS; best accuracy 14.97 bits
- unrolled_k: 34 evals, 0 feasible; max throughput seen 11.7 MSPS; best accuracy 15.24 bits
- pipelined: 16 evals, 7 feasible; max throughput seen 282 MSPS; best accuracy 14.14 bits; best feasible luts_plus_ffs=2029; feasible ranges: data_width 16..18, n_iter 17..22, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 33 evals, 25 feasible; max throughput seen 171 MSPS; best accuracy 14.32 bits; best feasible luts_plus_ffs=864; feasible ranges: data_width 14..20, n_iter 12..19, angle_guard -1..2, frac_guard 0..2, m 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 1 put all 10 Pareto points on pipelined_m, with 25/33 feasible there, while iterative (17 evals) and unrolled_k (34 evals) produced 0 feasible designs and pipelined's cheapest feasible point is 2029 luts_plus_ffs, far worse than 864, so budget should stay on pipelined_m. The front's two tails are both short of what the model allows: minimum luts_plus_ffs 864 versus an HV reference of 3000, and maximum accuracy_bits 14.32 versus a feasible 15.24, so a targeted two-box refine (cheap small-datapath designs with more iterations, and large-datapath high-iteration designs) should extend the staircase in both directions before the reserved full-range mapping round.*)
- `pipelined_m` (100 evals): data_width=12..16, n_iter=10..20, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* The cheapest feasible point is pipelined_m data_width=14 n_iter=14 at luts_plus_ffs=864 with accuracy_bits 10.05, i.e. it only just clears the 2^-10 error bound, so the low-area tail is likely still open: smaller data_width (12-13) combined with more micro-rotations should hold max_abs_err under 2^-10 while cutting LUTs. Only 30% of evaluations violated the error constraint, so this region is reachable.
- clamped by code: dropped duplicate family pipelined_m

**Result (code):** 100 evaluations this round, 200 total; 85 feasible; hypervolume 8207 (+0.9%).

**LLM decision:** `map_front` — The feasible front is essentially all pipelined_m and is dense only in the low-area corner: luts_plus_ffs spans 786..1381 against an HV reference of 3000, i.e. it covers only ~26-46% of the area objective's range, while accuracy_bits reaches just 14.3 (registry allows far more; unrolled_k already showed 15.24 bits, though infeasible). Because the HV reference point is (3000, 10), most of the hypervolume comes from the top front point's extension across the large 1381->3000 area gap, so the main untapped lever is higher accuracy at moderate area (data_width/n_iter beyond the explored 13..20 / 12..20). The +0.9% gain this round shows the explored region is near-saturated, so a focused NSGA-II over the full ranges of the families on the front (pipelined_m, seeded with the current front) is the efficient way to extend the accuracy end and fill the area gap before the reserved mapping. Constraints are not the blocker: throughput best 282 vs >=2, sys_p99 best 0.066 vs <=0.4, and the accuracy floor is already met at 10.1 bits, so higher-accuracy designs remain feasible.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 8207 (gain this round: +0.9%).
Feasible designs: 85 of 200 evaluations (74 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 38% violate; best seen 2.58e-05 (2^-15.24)
- sys_p99_latency_us <= 0.4: 26% violate; best seen 0.066

Pareto front (feasible, 15 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=-1 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=786, accuracy_bits=10.1, luts=643, ffs=143, throughput_msps=68.5, max_abs_err=0.000901 (2^-10.12), power_index=0.0591
- pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=3 rounding=trunc m=6] luts_plus_ffs=792, accuracy_bits=10.1, luts=654, ffs=137, throughput_msps=68.5, max_abs_err=0.000894 (2^-10.13), power_index=0.0596
- pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=3 rounding=trunc m=7] luts_plus_ffs=792, accuracy_bits=10.1, luts=654, ffs=137, throughput_msps=59.6, max_abs_err=0.000894 (2^-10.13), power_index=0.0596
- pipelined_m [data_width=16 n_iter=13 angle_guard=-1 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=844, accuracy_bits=10.4, luts=701, ffs=143, throughput_msps=59.6, max_abs_err=0.000761 (2^-10.36), power_index=0.0635
- pipelined_m [data_width=17 n_iter=12 angle_guard=1 frac_guard=2 rounding=trunc m=6] luts_plus_ffs=881, accuracy_bits=10.8, luts=724, ffs=157, throughput_msps=65.4, max_abs_err=0.000545 (2^-10.84), power_index=0.0663
- pipelined_m [data_width=19 n_iter=13 angle_guard=-1 frac_guard=1 rounding=trunc m=8] luts_plus_ffs=982, accuracy_bits=11.7, luts=815, ffs=167, throughput_msps=50.3, max_abs_err=0.000296 (2^-11.72), power_index=0.0739
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=1012, accuracy_bits=12.3, luts=855, ffs=157, throughput_msps=56.8, max_abs_err=0.000204 (2^-12.26), power_index=0.0761
- pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1181, accuracy_bits=12.4, luts=882, ffs=299, throughput_msps=93.6, max_abs_err=0.000179 (2^-12.45), power_index=0.0888
- pipelined_m [data_width=18 n_iter=17 angle_guard=0 frac_guard=0 rounding=round m=7] luts_plus_ffs=1238, accuracy_bits=13.1, luts=1017, ffs=221, throughput_msps=59.6, max_abs_err=0.000114 (2^-13.10), power_index=0.0931
- pipelined_m [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1381, accuracy_bits=14.3, luts=1135, ffs=246, throughput_msps=65.4, max_abs_err=4.89e-05 (2^-14.32), power_index=0.104
Front coverage: luts_plus_ffs 786..1381 (HV reference 3000); accuracy_bits 10.1..14.3 (HV reference 10); data_width on the front 14..20 (registry 8..28).

Per family:
- iterative: 17 evals, 0 feasible; max throughput seen 12.7 MSPS; best accuracy 14.97 bits
- unrolled_k: 34 evals, 0 feasible; max throughput seen 11.7 MSPS; best accuracy 15.24 bits
- pipelined: 16 evals, 7 feasible; max throughput seen 282 MSPS; best accuracy 14.14 bits; best feasible luts_plus_ffs=2029; feasible ranges: data_width 16..18, n_iter 17..22, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 133 evals, 78 feasible; max throughput seen 171 MSPS; best accuracy 14.32 bits; best feasible luts_plus_ffs=786; feasible ranges: data_width 13..20, n_iter 12..20, angle_guard -1..3, frac_guard 0..3, m 2..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (15 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 240 total; 122 feasible; hypervolume 1.184e+04 (+44.2%).

**LLM decision:** `map_front` — Round 3 of 4 done, 240/400 evals used, so one 100-eval round plus the reserved mapping budget remain. HV is 1.184e4 and still climbing hard (+44.2% this round), so the last round is worth spending rather than stopping. The front is effectively single-family: every one of the 23 feasible Pareto designs shown is pipelined_m (pipelined is the only other feasible family and its best area is 2029 vs pipelined_m's 786), while iterative and unrolled_k contribute 0 feasible designs (throughput capped ~12 MSPS and they fail the sys_p99_latency bound). The front already spans area 786..3605 (HV ref 3000) and accuracy 10.1..23.8 (ref 10), but it is thin in the 1567..2655 area region and entirely one family, so the right end-game move is to let code map the whole front over the full ranges of the families actually on it (pipelined_m, pipelined), seeded with the current front, to fill the sparse mid-region and lock in coverage before the L2 system simulation re-selects. This also hedges the L2 risk noted for the cheapest designs, which may only just pass the optimistic L1 sys_p99 bound.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 1.184e+04 (gain this round: +44.2%).
Feasible designs: 122 of 240 evaluations (108 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 33% violate; best seen 7.02e-08 (2^-23.76)
- sys_p99_latency_us <= 0.4: 21% violate; best seen 0.066

Pareto front (feasible, 23 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=-1 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=786, accuracy_bits=10.1, luts=643, ffs=143, throughput_msps=68.5, max_abs_err=0.000901 (2^-10.12), power_index=0.0591
- pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=3 rounding=trunc m=6] luts_plus_ffs=792, accuracy_bits=10.1, luts=654, ffs=137, throughput_msps=68.5, max_abs_err=0.000894 (2^-10.13), power_index=0.0596
- pipelined_m [data_width=16 n_iter=13 angle_guard=-1 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=844, accuracy_bits=10.4, luts=701, ffs=143, throughput_msps=59.6, max_abs_err=0.000761 (2^-10.36), power_index=0.0635
- pipelined_m [data_width=17 n_iter=12 angle_guard=1 frac_guard=2 rounding=trunc m=6] luts_plus_ffs=881, accuracy_bits=10.8, luts=724, ffs=157, throughput_msps=65.4, max_abs_err=0.000545 (2^-10.84), power_index=0.0663
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=1012, accuracy_bits=12.3, luts=855, ffs=157, throughput_msps=56.8, max_abs_err=0.000204 (2^-12.26), power_index=0.0761
- pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1181, accuracy_bits=12.4, luts=882, ffs=299, throughput_msps=93.6, max_abs_err=0.000179 (2^-12.45), power_index=0.0888
- pipelined_m [data_width=18 n_iter=17 angle_guard=1 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=1333, accuracy_bits=13.8, luts=1101, ffs=232, throughput_msps=56.8, max_abs_err=6.92e-05 (2^-13.82), power_index=0.1
- pipelined_m [data_width=19 n_iter=17 angle_guard=2 frac_guard=3 rounding=round m=5] luts_plus_ffs=1567, accuracy_bits=15.3, luts=1242, ffs=325, throughput_msps=77, max_abs_err=2.52e-05 (2^-15.28), power_index=0.118
- pipelined_m [data_width=25 n_iter=24 angle_guard=-2 frac_guard=4 rounding=round m=5] luts_plus_ffs=2655, accuracy_bits=18.2, luts=2167, ffs=488, throughput_msps=70.6, max_abs_err=3.3e-06 (2^-18.21), power_index=0.2
- pipelined_m [data_width=28 n_iter=26 angle_guard=2 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=3605, accuracy_bits=23.8, luts=2640, ffs=966, throughput_msps=106, max_abs_err=7.02e-08 (2^-23.76), power_index=0.271
Front coverage: luts_plus_ffs 786..3605 (HV reference 3000); accuracy_bits 10.1..23.8 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 17 evals, 0 feasible; max throughput seen 12.7 MSPS; best accuracy 14.97 bits
- unrolled_k: 34 evals, 0 feasible; max throughput seen 11.7 MSPS; best accuracy 15.24 bits
- pipelined: 16 evals, 7 feasible; max throughput seen 282 MSPS; best accuracy 14.14 bits; best feasible luts_plus_ffs=2029; feasible ranges: data_width 16..18, n_iter 17..22, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 173 evals, 115 feasible; max throughput seen 171 MSPS; best accuracy 23.76 bits; best feasible luts_plus_ffs=786; feasible ranges: data_width 13..28, n_iter 12..28, angle_guard -2..3, frac_guard 0..4, m 2..8
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (23 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 340 total; 216 feasible; hypervolume 1.557e+04 (+31.5%).

**LLM decision:** `stop` — Final round (340/400 evals used, 4/4 rounds done) and the front is healthy, not stuck: 216/340 designs feasible (196 unique), 41 on the Pareto front, and hypervolume rose +31.5% this round to 1.557e4. All three constraints are reachable with wide margin: throughput best 282 MSPS vs >=2, max_abs_err best 2^-23.76 vs <=2^-10, sys_p99_latency best 0.066 us vs <=0.4 us — so issuing `infeasible` would be wrong, and every family on the registry (iterative, unrolled_k, pipelined, pipelined_m) has already been explored. The front already spans the objective ranges (luts_plus_ffs 786..3605 across HV ref 3000; accuracy_bits 10.1..23.8 across HV ref 10), i.e. it covers both the cheap/adequate corner and the high-accuracy corner that the HV rewards. For this spec's selection rule (min luts_plus_ffs) the winner is clear and comfortably feasible: pipelined_m [W=16 N=12 angle_guard=-1 frac_guard=1 trunc m=6] at luts_plus_ffs=786, accuracy_bits=10.1 (max_abs_err 9.01e-4, inside the 2^-10 limit), throughput 68.5 MSPS. Further refinement would only chase marginal HV gain on a front that is already well mapped, so `stop` is the right call.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 60 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 340 of 400.
Hypervolume of the feasible front: 1.557e+04 (gain this round: +31.5%).
Feasible designs: 216 of 340 evaluations (196 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 25% violate; best seen 7.02e-08 (2^-23.76)
- sys_p99_latency_us <= 0.4: 15% violate; best seen 0.066

Pareto front (feasible, 41 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=-1 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=786, accuracy_bits=10.1, luts=643, ffs=143, throughput_msps=68.5, max_abs_err=0.000901 (2^-10.12), power_index=0.0591
- pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=2 rounding=round m=8] luts_plus_ffs=798, accuracy_bits=10.2, luts=661, ffs=137, throughput_msps=52.7, max_abs_err=0.000825 (2^-10.24), power_index=0.06
- pipelined_m [data_width=19 n_iter=13 angle_guard=-1 frac_guard=1 rounding=trunc m=8] luts_plus_ffs=982, accuracy_bits=11.7, luts=815, ffs=167, throughput_msps=50.3, max_abs_err=0.000296 (2^-11.72), power_index=0.0739
- pipelined_m [data_width=23 n_iter=14 angle_guard=-1 frac_guard=0 rounding=round m=7] luts_plus_ffs=1217, accuracy_bits=13, luts=1019, ffs=198, throughput_msps=54.3, max_abs_err=0.000124 (2^-12.98), power_index=0.0915
- pipelined_m [data_width=21 n_iter=16 angle_guard=-1 frac_guard=2 rounding=trunc m=6] luts_plus_ffs=1403, accuracy_bits=14.4, luts=1143, ffs=259, throughput_msps=62.5, max_abs_err=4.68e-05 (2^-14.38), power_index=0.106
- pipelined_m [data_width=23 n_iter=17 angle_guard=3 frac_guard=1 rounding=round m=6] luts_plus_ffs=1694, accuracy_bits=15.9, luts=1403, ffs=292, throughput_msps=62.5, max_abs_err=1.61e-05 (2^-15.92), power_index=0.127
- pipelined_m [data_width=24 n_iter=21 angle_guard=-1 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=1913, accuracy_bits=17.8, luts=1628, ffs=285, throughput_msps=54.3, max_abs_err=4.38e-06 (2^-17.80), power_index=0.144
- pipelined_m [data_width=24 n_iter=22 angle_guard=3 frac_guard=1 rounding=round m=7] luts_plus_ffs=2280, accuracy_bits=19.6, luts=1893, ffs=387, throughput_msps=52, max_abs_err=1.23e-06 (2^-19.63), power_index=0.172
- pipelined_m [data_width=28 n_iter=24 angle_guard=3 frac_guard=1 rounding=round m=8] luts_plus_ffs=2714, accuracy_bits=22.6, luts=2367, ffs=347, throughput_msps=44, max_abs_err=1.53e-07 (2^-22.64), power_index=0.204
- pipelined_m [data_width=28 n_iter=26 angle_guard=2 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=3605, accuracy_bits=23.8, luts=2640, ffs=966, throughput_msps=106, max_abs_err=7.02e-08 (2^-23.76), power_index=0.271
Front coverage: luts_plus_ffs 786..3605 (HV reference 3000); accuracy_bits 10.1..23.8 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 17 evals, 0 feasible; max throughput seen 12.7 MSPS; best accuracy 14.97 bits
- unrolled_k: 34 evals, 0 feasible; max throughput seen 11.7 MSPS; best accuracy 15.24 bits
- pipelined: 16 evals, 7 feasible; max throughput seen 282 MSPS; best accuracy 14.14 bits; best feasible luts_plus_ffs=2029; feasible ranges: data_width 16..18, n_iter 17..22, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 273 evals, 209 feasible; max throughput seen 171 MSPS; best accuracy 23.76 bits; best feasible luts_plus_ffs=786; feasible ranges: data_width 13..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

### Round 5

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 60 evaluations*)
- `pipelined_m` (60 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (41 front designs; box front_anchored)

**Result (code):** 60 evaluations this round, 400 total; 272 feasible; hypervolume 1.572e+04 (+1.0%).

**No LLM call** (code's front-mapping round): Final round (340/400 evals used, 4/4 rounds done) and the front is healthy, not stuck: 216/340 designs feasible (196 unique), 41 on the Pareto front, and hypervolume rose +31.5% this round to 1.557e4. All three constraints are reachable with wide margin: throughput best 282 MSPS vs >=2, max_abs_err best 2^-23.76 vs <=2^-10, sys_p99_latency best 0.066 us vs <=0.4 us — so issuing `infeasible` would be wrong, and every family on the registry (iterative, unrolled_k, pipelined, pipelined_m) has already been explored. The front already spans the objective ranges (luts_plus_ffs 786..3605 across HV ref 3000; accuracy_bits 10.1..23.8 across HV ref 10), i.e. it covers both the cheap/adequate corner and the high-accuracy corner that the HV rewards. For this spec's selection rule (min luts_plus_ffs) the winner is clear and comfortably feasible: pipelined_m [W=16 N=12 angle_guard=-1 frac_guard=1 trunc m=6] at luts_plus_ffs=786, accuracy_bits=10.1 (max_abs_err 9.01e-4, inside the 2^-10 limit), throughput 68.5 MSPS. Further refinement would only chase marginal HV gain on a front that is already well mapped, so `stop` is the right call.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 5 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.572e+04 (gain this round: +1.0%).
Feasible designs: 272 of 400 evaluations (249 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 22% violate; best seen 7.02e-08 (2^-23.76)
- sys_p99_latency_us <= 0.4: 13% violate; best seen 0.066

Pareto front (feasible, 43 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=-1 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=786, accuracy_bits=10.1, luts=643, ffs=143, throughput_msps=68.5, max_abs_err=0.000901 (2^-10.12), power_index=0.0591
- pipelined_m [data_width=16 n_iter=13 angle_guard=-1 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=844, accuracy_bits=10.4, luts=701, ffs=143, throughput_msps=59.6, max_abs_err=0.000761 (2^-10.36), power_index=0.0635
- pipelined_m [data_width=19 n_iter=13 angle_guard=-1 frac_guard=1 rounding=trunc m=8] luts_plus_ffs=982, accuracy_bits=11.7, luts=815, ffs=167, throughput_msps=50.3, max_abs_err=0.000296 (2^-11.72), power_index=0.0739
- pipelined_m [data_width=18 n_iter=17 angle_guard=0 frac_guard=0 rounding=round m=7] luts_plus_ffs=1238, accuracy_bits=13.1, luts=1017, ffs=221, throughput_msps=59.6, max_abs_err=0.000114 (2^-13.10), power_index=0.0931
- pipelined_m [data_width=22 n_iter=16 angle_guard=4 frac_guard=0 rounding=round m=8] luts_plus_ffs=1406, accuracy_bits=14.9, luts=1207, ffs=200, throughput_msps=48, max_abs_err=3.3e-05 (2^-14.89), power_index=0.106
- pipelined_m [data_width=23 n_iter=17 angle_guard=4 frac_guard=1 rounding=round m=8] luts_plus_ffs=1714, accuracy_bits=15.9, luts=1419, ffs=295, throughput_msps=45.9, max_abs_err=1.59e-05 (2^-15.94), power_index=0.129
- pipelined_m [data_width=24 n_iter=21 angle_guard=-1 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=1913, accuracy_bits=17.8, luts=1628, ffs=285, throughput_msps=54.3, max_abs_err=4.38e-06 (2^-17.80), power_index=0.144
- pipelined_m [data_width=24 n_iter=22 angle_guard=3 frac_guard=1 rounding=round m=7] luts_plus_ffs=2280, accuracy_bits=19.6, luts=1893, ffs=387, throughput_msps=52, max_abs_err=1.23e-06 (2^-19.63), power_index=0.172
- pipelined_m [data_width=28 n_iter=24 angle_guard=3 frac_guard=0 rounding=round m=8] luts_plus_ffs=2600, accuracy_bits=22.4, luts=2259, ffs=341, throughput_msps=44, max_abs_err=1.86e-07 (2^-22.36), power_index=0.196
- pipelined_m [data_width=28 n_iter=26 angle_guard=2 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=3605, accuracy_bits=23.8, luts=2640, ffs=966, throughput_msps=106, max_abs_err=7.02e-08 (2^-23.76), power_index=0.271
Front coverage: luts_plus_ffs 786..3605 (HV reference 3000); accuracy_bits 10.1..23.8 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 17 evals, 0 feasible; max throughput seen 12.7 MSPS; best accuracy 14.97 bits
- unrolled_k: 34 evals, 0 feasible; max throughput seen 11.7 MSPS; best accuracy 15.24 bits
- pipelined: 16 evals, 7 feasible; max throughput seen 282 MSPS; best accuracy 14.14 bits; best feasible luts_plus_ffs=2029; feasible ranges: data_width 16..18, n_iter 17..22, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 333 evals, 265 feasible; max throughput seen 171 MSPS; best accuracy 23.76 bits; best feasible luts_plus_ffs=786; feasible ranges: data_width 13..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 31152 in, 22346 out
- provider-reported cost: $0.0207
- full prompts and replies: `llm_trace.jsonl`

