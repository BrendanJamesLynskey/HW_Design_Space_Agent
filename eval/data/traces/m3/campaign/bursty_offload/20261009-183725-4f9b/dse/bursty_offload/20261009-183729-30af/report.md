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
`pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=2,rounding=trunc,m=3` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 631 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 246 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 124 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 124 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 48.2 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.066 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000894 (2^-10.13) | exact: bit-accurate model, exhaustive (16384 angles) |
| max_abs_err_lsb | 3.66 | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err | 0.000262 (2^-11.90) | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err_lsb | 1.07 | exact: bit-accurate model, exhaustive (16384 angles) |
| accuracy_bits | 10.1 | exact: bit-accurate model, exhaustive (16384 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 77.4 dBc, SNR 68.9 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: bursty requests: bursts of 8 (0 ns apart) arriving as a Poisson process, 2 requests/us on average. Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_latency_us <= 0.4 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=2,rounding=trunc,m=3` | 0.09642 → 0.1066 | yes |
| `pipelined_m:data_width=14,n_iter=12,angle_guard=3,frac_guard=1,rounding=round,m=3` | 0.09642 → 0.1066 | yes |
| `pipelined_m:data_width=15,n_iter=13,angle_guard=2,frac_guard=1,rounding=trunc,m=6` | 0.1605 → 0.2099 | yes |
| `pipelined_m:data_width=18,n_iter=12,angle_guard=4,frac_guard=0,rounding=round,m=7` | 0.1759 → 0.245 | yes |
| `pipelined_m:data_width=15,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc,m=6` | 0.1605 → 0.2099 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (39 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=14,n_iter=12,angle_guard=2,frac_guard=2,rounding=trunc,m=3` | 631 | 246 | 124.5 | 6 | 0.066 | 0.000894 (2^-10.13) | 10.13 |
| 1 | `pipelined_m:data_width=14,n_iter=12,angle_guard=3,frac_guard=1,rounding=round,m=3` | 649 | 246 | 124.5 | 6 | 0.0674 | 0.000889 (2^-10.14) | 10.14 |
| 2 | `pipelined_m:data_width=15,n_iter=13,angle_guard=2,frac_guard=1,rounding=trunc,m=6` | 701 | 198 | 68.5 | 5 | 0.0676 | 0.000689 (2^-10.50) | 10.50 |
| 3 | `pipelined_m:data_width=18,n_iter=12,angle_guard=4,frac_guard=0,rounding=round,m=7` | 747 | 167 | 56.8 | 4 | 0.0688 | 0.000513 (2^-10.93) | 10.93 |
| 4 | `pipelined_m:data_width=15,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc,m=6` | 726 | 202 | 68.5 | 5 | 0.0698 | 0.000466 (2^-11.07) | 11.07 |
| 5 | `pipelined_m:data_width=15,n_iter=13,angle_guard=2,frac_guard=3,rounding=round,m=7` | 783 | 147 | 59.6 | 4 | 0.07 | 0.000358 (2^-11.45) | 11.45 |
| 6 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc,m=8` | 920 | 157 | 50.3 | 4 | 0.081 | 0.000175 (2^-12.48) | 12.48 |
| 7 | `pipelined_m:data_width=18,n_iter=15,angle_guard=3,frac_guard=1,rounding=trunc,m=8` | 964 | 167 | 50.3 | 4 | 0.0851 | 0.000118 (2^-13.05) | 13.05 |
| 8 | `pipelined_m:data_width=17,n_iter=17,angle_guard=1,frac_guard=2,rounding=round,m=8` | 1086 | 223 | 50.3 | 5 | 0.0985 | 0.000112 (2^-13.13) | 13.13 |
| 9 | `pipelined_m:data_width=19,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1019 | 309 | 93.6 | 6 | 0.0999 | 7.94e-05 (2^-13.62) | 13.62 |
| 10 | `pipelined_m:data_width=17,n_iter=17,angle_guard=4,frac_guard=3,rounding=trunc,m=6` | 1135 | 234 | 65.4 | 5 | 0.103 | 7.73e-05 (2^-13.66) | 13.66 |
| 11 | `pipelined_m:data_width=17,n_iter=17,angle_guard=3,frac_guard=3,rounding=round,m=6` | 1154 | 233 | 65.4 | 5 | 0.104 | 5.1e-05 (2^-14.26) | 14.26 |
| 12 | `pipelined_m:data_width=18,n_iter=19,angle_guard=3,frac_guard=3,rounding=trunc,m=8` | 1314 | 242 | 50.3 | 5 | 0.117 | 3.81e-05 (2^-14.68) | 14.68 |
| 13 | `pipelined_m:data_width=19,n_iter=19,angle_guard=4,frac_guard=0,rounding=round,m=6` | 1276 | 313 | 62.5 | 6 | 0.12 | 3.74e-05 (2^-14.71) | 14.71 |
| 14 | `pipelined_m:data_width=18,n_iter=19,angle_guard=4,frac_guard=3,rounding=round,m=7` | 1371 | 247 | 56.8 | 5 | 0.122 | 1.91e-05 (2^-15.68) | 15.68 |
| 15 | `pipelined_m:data_width=21,n_iter=18,angle_guard=1,frac_guard=2,rounding=round,m=7` | 1375 | 267 | 54.3 | 5 | 0.124 | 1.31e-05 (2^-16.22) | 16.22 |
| 16 | `pipelined_m:data_width=21,n_iter=18,angle_guard=2,frac_guard=3,rounding=trunc,m=7` | 1385 | 272 | 54.3 | 5 | 0.125 | 1.12e-05 (2^-16.44) | 16.44 |
| 17 | `pipelined_m:data_width=21,n_iter=18,angle_guard=2,frac_guard=3,rounding=round,m=7` | 1429 | 274 | 54.3 | 5 | 0.128 | 1.04e-05 (2^-16.56) | 16.56 |
| 18 | `pipelined_m:data_width=24,n_iter=18,angle_guard=-1,frac_guard=1,rounding=trunc,m=6` | 1420 | 289 | 62.5 | 5 | 0.129 | 9.83e-06 (2^-16.63) | 16.63 |
| 19 | `pipelined_m:data_width=21,n_iter=19,angle_guard=3,frac_guard=2,rounding=trunc,m=8` | 1447 | 271 | 48.0 | 5 | 0.129 | 9.33e-06 (2^-16.71) | 16.71 |
| 20 | `pipelined_m:data_width=22,n_iter=19,angle_guard=4,frac_guard=1,rounding=trunc,m=8` | 1485 | 281 | 48.0 | 5 | 0.133 | 8.01e-06 (2^-16.93) | 16.93 |
| 21 | `pipelined_m:data_width=26,n_iter=18,angle_guard=1,frac_guard=0,rounding=trunc,m=8` | 1528 | 313 | 45.9 | 5 | 0.138 | 7.99e-06 (2^-16.93) | 16.93 |
| 22 | `pipelined_m:data_width=26,n_iter=18,angle_guard=2,frac_guard=0,rounding=trunc,m=6` | 1546 | 316 | 59.9 | 5 | 0.14 | 7.88e-06 (2^-16.95) | 16.95 |
| 23 | `pipelined_m:data_width=26,n_iter=18,angle_guard=2,frac_guard=0,rounding=trunc,m=8` | 1546 | 316 | 45.9 | 5 | 0.14 | 7.88e-06 (2^-16.95) | 16.95 |
| 24 | `pipelined_m:data_width=25,n_iter=19,angle_guard=1,frac_guard=0,rounding=trunc,m=7` | 1561 | 302 | 54.3 | 5 | 0.14 | 4.66e-06 (2^-17.71) | 17.71 |
| 25 | `pipelined_m:data_width=22,n_iter=20,angle_guard=4,frac_guard=2,rounding=trunc,m=8` | 1607 | 286 | 48.0 | 5 | 0.142 | 4.4e-06 (2^-17.79) | 17.79 |
| 26 | `pipelined_m:data_width=24,n_iter=21,angle_guard=1,frac_guard=0,rounding=round,m=7` | 1670 | 291 | 54.3 | 5 | 0.148 | 2.39e-06 (2^-18.68) | 18.68 |
| 27 | `pipelined_m:data_width=24,n_iter=21,angle_guard=1,frac_guard=1,rounding=trunc,m=7` | 1712 | 295 | 54.3 | 5 | 0.151 | 2.25e-06 (2^-18.76) | 18.76 |
| 28 | `pipelined_m:data_width=24,n_iter=21,angle_guard=2,frac_guard=1,rounding=trunc,m=7` | 1733 | 298 | 54.3 | 5 | 0.153 | 2.24e-06 (2^-18.77) | 18.77 |
| 29 | `pipelined_m:data_width=24,n_iter=21,angle_guard=1,frac_guard=3,rounding=trunc,m=8` | 1797 | 303 | 45.9 | 5 | 0.158 | 1.77e-06 (2^-19.11) | 19.11 |
| 30 | `pipelined_m:data_width=24,n_iter=23,angle_guard=1,frac_guard=2,rounding=trunc,m=8` | 1929 | 299 | 48.0 | 5 | 0.168 | 1.34e-06 (2^-19.51) | 19.51 |
| 31 | `pipelined_m:data_width=27,n_iter=21,angle_guard=4,frac_guard=0,rounding=round,m=7` | 1923 | 333 | 49.9 | 5 | 0.17 | 1.06e-06 (2^-19.85) | 19.85 |
| 32 | `pipelined_m:data_width=25,n_iter=24,angle_guard=1,frac_guard=1,rounding=round,m=8` | 2094 | 308 | 48.0 | 5 | 0.181 | 7.31e-07 (2^-20.38) | 20.38 |
| 33 | `pipelined_m:data_width=27,n_iter=24,angle_guard=2,frac_guard=0,rounding=round,m=6` | 2162 | 418 | 59.9 | 6 | 0.194 | 2.66e-07 (2^-21.84) | 21.84 |
| 34 | `pipelined_m:data_width=26,n_iter=24,angle_guard=2,frac_guard=4,rounding=round,m=7` | 2338 | 430 | 52.0 | 6 | 0.208 | 2.22e-07 (2^-22.10) | 22.10 |
| 35 | `pipelined_m:data_width=26,n_iter=24,angle_guard=2,frac_guard=4,rounding=round,m=6` | 2338 | 430 | 59.9 | 6 | 0.208 | 2.22e-07 (2^-22.10) | 22.10 |
| 36 | `pipelined_m:data_width=27,n_iter=26,angle_guard=1,frac_guard=2,rounding=trunc,m=8` | 2429 | 426 | 45.9 | 6 | 0.215 | 1.72e-07 (2^-22.47) | 22.47 |
| 37 | `pipelined_m:data_width=26,n_iter=25,angle_guard=4,frac_guard=4,rounding=round,m=6` | 2488 | 536 | 59.9 | 7 | 0.227 | 1.09e-07 (2^-23.12) | 23.12 |
| 38 | `pipelined_m:data_width=28,n_iter=27,angle_guard=3,frac_guard=3,rounding=trunc,m=7` | 2718 | 454 | 49.9 | 6 | 0.239 | 4.57e-08 (2^-24.38) | 24.38 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Throughput >= 2 Msps is trivially met by every family, so the binding constraints are accuracy (output LSB 2^-(W-2) forces W>=12, and the ~2^-N angle residual forces N>=~11) and the system p99 latency of 0.4 us under bursts of 8 arriving 0 ns apart. Because the L1 system metric is an optimistic bound, I bias the budget toward families that drain a burst quickly with margin: unrolled_k (shared datapath, area-lean, k rotations/cycle) and pipelined_m (1 result/cycle, tunable register density), with pipelined covering the max-throughput corner and iterative probing the minimum-area corner. Ranges are centred on W 12..16 and N 10..16 so the optimizer can trade accuracy against burst-drain latency, with guard bits and rounding left open since they are cheap accuracy levers.*)
- `unrolled_k` (35 evals): data_width=12..16, n_iter=10..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, k=2..6. *Why:* Shared datapath keeps LUTs low (area is the objective) while k chained rotations/cycle drain a burst of 8 in ~8*ceil(N/k) cycles, which is the likely binding system constraint; k is the main latency/area knob.
- `pipelined_m` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* 1 result/cycle gives the largest latency margin for the L1->L2 system screen (bursts of 8 drain in ~8 cycles), and m trades Fmax against register count so the optimizer can find the area-leanest point that still meets p99.
- `pipelined` (20 evals): data_width=12..16, n_iter=10..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* The m=1 corner of the pipelined family: highest Fmax / lowest latency, useful for covering the high-throughput end of the Pareto front even if its FF count is higher.
- `iterative` (15 evals): data_width=12..16, n_iter=10..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* Smallest-area family and the selection-rule favourite if it is feasible; a modest share probes the low-area end of the front and confirms whether N+3 cycles/result can still drain a burst of 8 within 0.4 us.

**Result (code):** 100 evaluations this round, 100 total; 15 feasible; hypervolume 2231 (n/a).

**LLM decision:** `map_front` — Round 1 left a very narrow feasible front: only 4 designs, all pipelined_m, with data_width 14..15, n_iter 12..13, m 3..6, luts_plus_ffs 877..928 and accuracy_bits 10.1..11.1. The HV reference for luts_plus_ffs is 3000, so the front occupies only the extreme low-area corner, and the accuracy range is far from the best accuracy seen anywhere (11.59 bits, unrolled_k) and from the best feasible accuracy (11.07 bits, pipelined_m). Because the HV rectangle area is roughly (3000 - luts_plus_ffs) * (accuracy_bits - 10), even a modest accuracy gain at ~900 area would add large hypervolume, while a lower-area feasible point would also help. The pipelined family is feasible (best luts_plus_ffs=1466) but absent from the front, so its full range may contain useful trade-offs. With 300 evaluations left and 3 rounds, the right move is to spend this round mapping the full ranges of the families that produced the front (pipelined_m and pipelined), seeded with the current front, before refining.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 2231 (gain this round: n/a (first round)).
Feasible designs: 15 of 100 evaluations (11 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 68% violate; best seen 0.000325 (2^-11.59)
- sys_p99_latency_us <= 0.4: 50% violate; best seen 0.0639

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=877, accuracy_bits=10.1, luts=631, ffs=246, throughput_msps=124, max_abs_err=0.000894 (2^-10.13), power_index=0.066
- pipelined_m [data_width=14 n_iter=12 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=895, accuracy_bits=10.1, luts=649, ffs=246, throughput_msps=124, max_abs_err=0.000889 (2^-10.14), power_index=0.0674
- pipelined_m [data_width=15 n_iter=13 angle_guard=2 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=898, accuracy_bits=10.5, luts=701, ffs=198, throughput_msps=68.5, max_abs_err=0.000689 (2^-10.50), power_index=0.0676
- pipelined_m [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc m=6] luts_plus_ffs=928, accuracy_bits=11.1, luts=726, ffs=202, throughput_msps=68.5, max_abs_err=0.000466 (2^-11.07), power_index=0.0698
Front coverage: luts_plus_ffs 877..928 (HV reference 3000); accuracy_bits 10.1..11.1 (HV reference 10); data_width on the front 14..15 (registry 8..28).

Per family:
- iterative: 15 evals, 0 feasible; max throughput seen 15.6 MSPS; best accuracy 11.50 bits
- unrolled_k: 35 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 11.59 bits
- pipelined: 20 evals, 3 feasible; max throughput seen 282 MSPS; best accuracy 10.78 bits; best feasible luts_plus_ffs=1466; feasible ranges: data_width 15..15, n_iter 14..15, angle_guard 1..3, frac_guard 0..1
- pipelined_m: 30 evals, 12 feasible; max throughput seen 171 MSPS; best accuracy 11.07 bits; best feasible luts_plus_ffs=877; feasible ranges: data_width 14..15, n_iter 12..13, angle_guard 2..3, frac_guard 1..3, m 2..6
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 109 feasible; hypervolume 1.457e+04 (+553.1%).

**LLM decision:** `refine` — Round 2 gave +553% HV and the front is now entirely pipelined_m over the full contributing objective range; the other three families are either infeasible (iterative 0/15, unrolled_k 0/35 — they cannot supply 1 result/cycle so a burst of 8 blows the 0.4 us p99 bound) or dominated (pipelined). With 200 evals and 2 rounds left, refine pipelined_m around the region that produces the front (data_width 13..28, n_iter 12..26, angle_guard -1..4, frac_guard 0..3, m 2..8) — keeping everything below the 3000-lut HV reference and densifying the cheap corner (877 luts+ffs, 10.13 acc) where the min-luts_plus_ffs selection rule operates and where the accuracy margin over 2^-10 is thinnest.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.457e+04 (gain this round: +553.1%).
Feasible designs: 109 of 200 evaluations (101 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 37% violate; best seen 4.57e-08 (2^-24.38)
- sys_p99_latency_us <= 0.4: 25% violate; best seen 0.0639

Pareto front (feasible, 28 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=877, accuracy_bits=10.1, luts=631, ffs=246, throughput_msps=124, max_abs_err=0.000894 (2^-10.13), power_index=0.066
- pipelined_m [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc m=6] luts_plus_ffs=928, accuracy_bits=11.1, luts=726, ffs=202, throughput_msps=68.5, max_abs_err=0.000466 (2^-11.07), power_index=0.0698
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1328, accuracy_bits=13.6, luts=1019, ffs=309, throughput_msps=93.6, max_abs_err=7.94e-05 (2^-13.62), power_index=0.0999
- pipelined_m [data_width=19 n_iter=19 angle_guard=4 frac_guard=0 rounding=round m=6] luts_plus_ffs=1589, accuracy_bits=14.7, luts=1276, ffs=313, throughput_msps=62.5, max_abs_err=3.74e-05 (2^-14.71), power_index=0.12
- pipelined_m [data_width=21 n_iter=19 angle_guard=3 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=1718, accuracy_bits=16.7, luts=1447, ffs=271, throughput_msps=48, max_abs_err=9.33e-06 (2^-16.71), power_index=0.129
- pipelined_m [data_width=26 n_iter=18 angle_guard=2 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1862, accuracy_bits=17, luts=1546, ffs=316, throughput_msps=59.9, max_abs_err=7.88e-06 (2^-16.95), power_index=0.14
- pipelined_m [data_width=22 n_iter=20 angle_guard=4 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=1892, accuracy_bits=17.8, luts=1607, ffs=286, throughput_msps=48, max_abs_err=4.4e-06 (2^-17.79), power_index=0.142
- pipelined_m [data_width=27 n_iter=20 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=2319, accuracy_bits=18.9, luts=1807, ffs=512, throughput_msps=86, max_abs_err=2.05e-06 (2^-18.90), power_index=0.174
- pipelined_m [data_width=28 n_iter=23 angle_guard=-1 frac_guard=2 rounding=round m=7] luts_plus_ffs=2654, accuracy_bits=21.3, luts=2220, ffs=434, throughput_msps=52, max_abs_err=3.88e-07 (2^-21.30), power_index=0.2
- pipelined_m [data_width=28 n_iter=27 angle_guard=3 frac_guard=3 rounding=trunc m=7] luts_plus_ffs=3172, accuracy_bits=24.4, luts=2718, ffs=454, throughput_msps=49.9, max_abs_err=4.57e-08 (2^-24.38), power_index=0.239
Front coverage: luts_plus_ffs 877..3172 (HV reference 3000); accuracy_bits 10.1..24.4 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 15 evals, 0 feasible; max throughput seen 15.6 MSPS; best accuracy 11.50 bits
- unrolled_k: 35 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 11.59 bits
- pipelined: 20 evals, 3 feasible; max throughput seen 282 MSPS; best accuracy 10.78 bits; best feasible luts_plus_ffs=1466; feasible ranges: data_width 15..15, n_iter 14..15, angle_guard 1..3, frac_guard 0..1
- pipelined_m: 130 evals, 106 feasible; max throughput seen 171 MSPS; best accuracy 24.38 bits; best feasible luts_plus_ffs=877; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Front already spans the objectives (luts_plus_ffs 877..3172 vs ref 3000, accuracy 10.1..24.4 vs ref 10), so map_front is not indicated. 2 rounds / 200 evals remain. Extract max HV value by densifying the contributing band of pipelined_m and probing just below data_width=14 / n_iter=12 where the 877-lut selection winner sits (10.13 bits vs the 10-bit constraint — it only just passes, so extra feasible neighbours at the cheap corner are worth finding).*)
- `pipelined_m` (85 evals): data_width=13..28, n_iter=12..26, angle_guard=-1..4, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* Only pipelined/pipelined_m can satisfy sys_p99 <= 0.4 us (iterative best 15.6 MSPS and unrolled_k 13.5 MSPS gave 0/15 and 0/35 feasible; they cannot feed 1 result/cycle against 8-deep bursts). pipelined_m strictly dominates pipelined (registry: >=1 result/cycle, fewer registers), so spend everything here. Target the whole region that actually contributes HV: luts_plus_ffs below the 3000 reference, i.e. the cheap corner where the selection rule lives (877 luts+ffs) up through the ~2654/21.3-bit knee (data_width 28, n_iter 23), with a mild trim of the extremes that only produced >3000-lut non-contributing designs (n_iter>26, frac_guard=4, angle_guard=-2) to densify the contributing band.
- `pipelined` (5 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* feasible but dominated by pipelined_m
- `iterative` (5 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* 0/15 feasible; cannot meet sys_p99 at 1 result/N+3 cycles
- `unrolled_k` (5 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* 0/35 feasible; same throughput-per-cycle wall

**Result (code):** 100 evaluations this round, 300 total; 196 feasible; hypervolume 1.538e+04 (+5.6%).

**LLM decision:** `map_front` — Round 3 leaves 100 evals (1 round). The feasible front is 37 designs, essentially all `pipelined_m`, and it already spans the full extent of the HV reference box: luts_plus_ffs 877..3172 (ref 3000) and accuracy_bits 10.1..24.4 (ref 10). The other families are dead ends for this spec: `iterative` (0/20 feasible) and `unrolled_k` (0/40 feasible) cannot meet sys_p99_latency_us<=0.4 because their multi-cycle-per-result schedule queues bursts, and `pipelined`'s best feasible area (1466) is dominated by `pipelined_m` (877). The `pipelined_m` feasible ranges already reach the registry edges (data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8), so widening is pointless and refining would only shrink coverage. The cheap end is accuracy-limited, not range-limited: the 877 design sits at max_abs_err=2^-10.13, just inside the 2^-10 constraint, so lower data_width cannot go cheaper. HV is still climbing (+5.6% this round), so stopping is premature. The right use of the last round is to densely map the existing front over the full ranges of the families on it (the reserved front-mapping pass), filling the staircase between 877 and 3172 to maximise hypervolume coverage.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.538e+04 (gain this round: +5.6%).
Feasible designs: 196 of 300 evaluations (178 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 28% violate; best seen 4.57e-08 (2^-24.38)
- sys_p99_latency_us <= 0.4: 19% violate; best seen 0.0532

Pareto front (feasible, 37 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=877, accuracy_bits=10.1, luts=631, ffs=246, throughput_msps=124, max_abs_err=0.000894 (2^-10.13), power_index=0.066
- pipelined_m [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc m=6] luts_plus_ffs=928, accuracy_bits=11.1, luts=726, ffs=202, throughput_msps=68.5, max_abs_err=0.000466 (2^-11.07), power_index=0.0698
- pipelined_m [data_width=17 n_iter=17 angle_guard=1 frac_guard=2 rounding=round m=8] luts_plus_ffs=1309, accuracy_bits=13.1, luts=1086, ffs=223, throughput_msps=50.3, max_abs_err=0.000112 (2^-13.13), power_index=0.0985
- pipelined_m [data_width=18 n_iter=19 angle_guard=3 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1556, accuracy_bits=14.7, luts=1314, ffs=242, throughput_msps=50.3, max_abs_err=3.81e-05 (2^-14.68), power_index=0.117
- pipelined_m [data_width=21 n_iter=18 angle_guard=2 frac_guard=3 rounding=trunc m=7] luts_plus_ffs=1657, accuracy_bits=16.4, luts=1385, ffs=272, throughput_msps=54.3, max_abs_err=1.12e-05 (2^-16.44), power_index=0.125
- pipelined_m [data_width=22 n_iter=19 angle_guard=4 frac_guard=1 rounding=trunc m=8] luts_plus_ffs=1766, accuracy_bits=16.9, luts=1485, ffs=281, throughput_msps=48, max_abs_err=8.01e-06 (2^-16.93), power_index=0.133
- pipelined_m [data_width=25 n_iter=19 angle_guard=1 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=1862, accuracy_bits=17.7, luts=1561, ffs=302, throughput_msps=54.3, max_abs_err=4.66e-06 (2^-17.71), power_index=0.14
- pipelined_m [data_width=24 n_iter=21 angle_guard=2 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=2031, accuracy_bits=18.8, luts=1733, ffs=298, throughput_msps=54.3, max_abs_err=2.24e-06 (2^-18.77), power_index=0.153
- pipelined_m [data_width=25 n_iter=24 angle_guard=1 frac_guard=1 rounding=round m=8] luts_plus_ffs=2402, accuracy_bits=20.4, luts=2094, ffs=308, throughput_msps=48, max_abs_err=7.31e-07 (2^-20.38), power_index=0.181
- pipelined_m [data_width=28 n_iter=27 angle_guard=3 frac_guard=3 rounding=trunc m=7] luts_plus_ffs=3172, accuracy_bits=24.4, luts=2718, ffs=454, throughput_msps=49.9, max_abs_err=4.57e-08 (2^-24.38), power_index=0.239
Front coverage: luts_plus_ffs 877..3172 (HV reference 3000); accuracy_bits 10.1..24.4 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 20 evals, 0 feasible; max throughput seen 37.6 MSPS; best accuracy 14.97 bits
- unrolled_k: 40 evals, 0 feasible; max throughput seen 20.4 MSPS; best accuracy 20.20 bits
- pipelined: 25 evals, 7 feasible; max throughput seen 282 MSPS; best accuracy 15.13 bits; best feasible luts_plus_ffs=1466; feasible ranges: data_width 15..22, n_iter 12..29, angle_guard -2..3, frac_guard 0..4
- pipelined_m: 215 evals, 189 feasible; max throughput seen 171 MSPS; best accuracy 24.38 bits; best feasible luts_plus_ffs=877; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (34 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (37 front designs; box front_anchored)
- `iterative` (33 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: iterative was explored but found nothing feasible; full-box share (M3 lever)
- `unrolled_k` (33 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: unrolled_k was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 100 evaluations this round, 400 total; 229 feasible; hypervolume 1.56e+04 (+1.4%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), and the front is feasible and still improving slightly (+1.4% HV this round, HV 1.56e+04). All three constraints are satisfiable: throughput best 282 MSPS vs >=2 required (0% violations), max_abs_err best 4.57e-08 vs <=9.77e-04 (26% violations but many pass), sys_p99_latency best 0.0532 us vs <=0.4 us (30% violations but many pass). 229 feasible designs (210 unique) span luts_plus_ffs 877..3172 and accuracy_bits 10.1..24.4, covering the HV reference point (3000, 10) on both axes, so the front is well mapped. The selection rule (min luts_plus_ffs) picks pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=2 trunc m=3] at luts_plus_ffs=877, accuracy 10.13 bits (max_abs_err 8.94e-04 <= 9.77e-04), throughput 124 MSPS, power_index 0.066 — it passes every L1 constraint with margin, so no infeasibility. iterative and unrolled_k produced 0 feasible designs (max throughput 37.6 and 24.3 MSPS with 30%+ latency violations), confirming pipelined_m is the right family; nothing further to explore.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.56e+04 (gain this round: +1.4%).
Feasible designs: 229 of 400 evaluations (210 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 26% violate; best seen 4.57e-08 (2^-24.38)
- sys_p99_latency_us <= 0.4: 30% violate; best seen 0.0532

Pareto front (feasible, 39 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=14 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=877, accuracy_bits=10.1, luts=631, ffs=246, throughput_msps=124, max_abs_err=0.000894 (2^-10.13), power_index=0.066
- pipelined_m [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc m=6] luts_plus_ffs=928, accuracy_bits=11.1, luts=726, ffs=202, throughput_msps=68.5, max_abs_err=0.000466 (2^-11.07), power_index=0.0698
- pipelined_m [data_width=17 n_iter=17 angle_guard=1 frac_guard=2 rounding=round m=8] luts_plus_ffs=1309, accuracy_bits=13.1, luts=1086, ffs=223, throughput_msps=50.3, max_abs_err=0.000112 (2^-13.13), power_index=0.0985
- pipelined_m [data_width=19 n_iter=19 angle_guard=4 frac_guard=0 rounding=round m=6] luts_plus_ffs=1589, accuracy_bits=14.7, luts=1276, ffs=313, throughput_msps=62.5, max_abs_err=3.74e-05 (2^-14.71), power_index=0.12
- pipelined_m [data_width=21 n_iter=18 angle_guard=2 frac_guard=3 rounding=round m=7] luts_plus_ffs=1703, accuracy_bits=16.6, luts=1429, ffs=274, throughput_msps=54.3, max_abs_err=1.04e-05 (2^-16.56), power_index=0.128
- pipelined_m [data_width=26 n_iter=18 angle_guard=1 frac_guard=0 rounding=trunc m=8] luts_plus_ffs=1841, accuracy_bits=16.9, luts=1528, ffs=313, throughput_msps=45.9, max_abs_err=7.99e-06 (2^-16.93), power_index=0.138
- pipelined_m [data_width=22 n_iter=20 angle_guard=4 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=1892, accuracy_bits=17.8, luts=1607, ffs=286, throughput_msps=48, max_abs_err=4.4e-06 (2^-17.79), power_index=0.142
- pipelined_m [data_width=24 n_iter=23 angle_guard=1 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=2228, accuracy_bits=19.5, luts=1929, ffs=299, throughput_msps=48, max_abs_err=1.34e-06 (2^-19.51), power_index=0.168
- pipelined_m [data_width=26 n_iter=24 angle_guard=2 frac_guard=4 rounding=round m=7] luts_plus_ffs=2768, accuracy_bits=22.1, luts=2338, ffs=430, throughput_msps=52, max_abs_err=2.22e-07 (2^-22.10), power_index=0.208
- pipelined_m [data_width=28 n_iter=27 angle_guard=3 frac_guard=3 rounding=trunc m=7] luts_plus_ffs=3172, accuracy_bits=24.4, luts=2718, ffs=454, throughput_msps=49.9, max_abs_err=4.57e-08 (2^-24.38), power_index=0.239
Front coverage: luts_plus_ffs 877..3172 (HV reference 3000); accuracy_bits 10.1..24.4 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 53 evals, 0 feasible; max throughput seen 37.6 MSPS; best accuracy 20.68 bits
- unrolled_k: 73 evals, 0 feasible; max throughput seen 24.3 MSPS; best accuracy 20.20 bits
- pipelined: 25 evals, 7 feasible; max throughput seen 282 MSPS; best accuracy 15.13 bits; best feasible luts_plus_ffs=1466; feasible ranges: data_width 15..22, n_iter 12..29, angle_guard -2..3, frac_guard 0..4
- pipelined_m: 249 evals, 222 feasible; max throughput seen 171 MSPS; best accuracy 24.38 bits; best feasible luts_plus_ffs=877; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 30614 in, 19179 out
- provider-reported cost: $0.0187
- full prompts and replies: `llm_trace.jsonl`

