# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`pipelined_m:data_width=19,n_iter=14,angle_guard=-2,frac_guard=1,rounding=trunc,m=3` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 868 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 359 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 119 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 119 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 58.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.48 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000241 (2^-12.02) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 31.6 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.95e-05 (2^-14.04) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 7.79 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 7 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 97.0 dBc, SNR 81.8 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Every L1-feasible design (204) was simulated at its estimated Fmax (SimPy); 204 pass. Top 5 by the selection rule, L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=19,n_iter=14,angle_guard=-2,frac_guard=1,rounding=trunc,m=3` | 0.3103 → 0.3186 | yes |
| `pipelined_m:data_width=18,n_iter=14,angle_guard=-1,frac_guard=2,rounding=round,m=3` | 0.3103 → 0.3186 | yes |
| `pipelined_m:data_width=16,n_iter=16,angle_guard=3,frac_guard=3,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=14,angle_guard=4,frac_guard=2,rounding=round,m=3` | 0.3103 → 0.3186 | yes |
| `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=3,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (30 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=14,angle_guard=-2,frac_guard=1,rounding=trunc,m=3` | 868 | 359 | 119.3 | 7 | 1.48 | 0.000241 (2^-12.02) | 12.02 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=-1,frac_guard=2,rounding=round,m=3` | 906 | 357 | 119.3 | 7 | 1.52 | 0.00024 (2^-12.03) | 12.03 |
| 2 | `pipelined_m:data_width=16,n_iter=16,angle_guard=3,frac_guard=3,rounding=trunc,m=4` | 1001 | 285 | 93.6 | 6 | 1.55 | 0.000146 (2^-12.74) | 12.74 |
| 3 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=3,rounding=trunc,m=4` | 994 | 305 | 93.6 | 6 | 1.56 | 0.000102 (2^-13.26) | 13.26 |
| 4 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 1017 | 297 | 93.6 | 6 | 1.58 | 8.82e-05 (2^-13.47) | 13.47 |
| 5 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1086 | 305 | 93.6 | 6 | 1.67 | 5.46e-05 (2^-14.16) | 14.16 |
| 6 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=3,rounding=round,m=4` | 1118 | 311 | 93.6 | 6 | 1.72 | 5.03e-05 (2^-14.28) | 14.28 |
| 7 | `pipelined_m:data_width=19,n_iter=16,angle_guard=3,frac_guard=2,rounding=trunc,m=4` | 1112 | 321 | 93.6 | 6 | 1.72 | 4.67e-05 (2^-14.39) | 14.39 |
| 8 | `pipelined_m:data_width=19,n_iter=16,angle_guard=2,frac_guard=3,rounding=trunc,m=4` | 1128 | 323 | 93.6 | 6 | 1.75 | 4.57e-05 (2^-14.42) | 14.42 |
| 9 | `pipelined_m:data_width=19,n_iter=16,angle_guard=4,frac_guard=2,rounding=round,m=4` | 1168 | 327 | 89.6 | 6 | 1.8 | 3.9e-05 (2^-14.64) | 14.64 |
| 10 | `pipelined_m:data_width=18,n_iter=19,angle_guard=3,frac_guard=3,rounding=round,m=4` | 1352 | 385 | 93.6 | 7 | 2.09 | 2.16e-05 (2^-15.50) | 15.50 |
| 11 | `pipelined_m:data_width=18,n_iter=19,angle_guard=3,frac_guard=4,rounding=round,m=3` | 1390 | 539 | 119.3 | 9 | 2.32 | 2.1e-05 (2^-15.54) | 15.54 |
| 12 | `pipelined_m:data_width=20,n_iter=19,angle_guard=3,frac_guard=1,rounding=round,m=3` | 1394 | 549 | 114.5 | 9 | 2.34 | 1.31e-05 (2^-16.22) | 16.22 |
| 13 | `pipelined_m:data_width=20,n_iter=18,angle_guard=4,frac_guard=4,rounding=round,m=3` | 1445 | 513 | 114.5 | 8 | 2.36 | 1.06e-05 (2^-16.52) | 16.52 |
| 14 | `pipelined_m:data_width=20,n_iter=19,angle_guard=3,frac_guard=2,rounding=round,m=3` | 1432 | 561 | 114.5 | 9 | 2.4 | 1.04e-05 (2^-16.56) | 16.56 |
| 15 | `pipelined_m:data_width=20,n_iter=19,angle_guard=2,frac_guard=3,rounding=round,m=3` | 1451 | 566 | 114.5 | 9 | 2.43 | 1.02e-05 (2^-16.59) | 16.59 |
| 16 | `pipelined_m:data_width=21,n_iter=19,angle_guard=1,frac_guard=2,rounding=round,m=3` | 1453 | 570 | 114.5 | 9 | 2.44 | 9.84e-06 (2^-16.63) | 16.63 |
| 17 | `pipelined_m:data_width=20,n_iter=19,angle_guard=3,frac_guard=4,rounding=round,m=3` | 1508 | 585 | 114.5 | 9 | 2.52 | 8.2e-06 (2^-16.90) | 16.90 |
| 18 | `pipelined_m:data_width=26,n_iter=19,angle_guard=-2,frac_guard=2,rounding=trunc,m=3` | 1636 | 663 | 110.0 | 9 | 2.77 | 4.93e-06 (2^-17.63) | 17.63 |
| 19 | `pipelined_m:data_width=24,n_iter=21,angle_guard=-1,frac_guard=2,rounding=trunc,m=3` | 1712 | 624 | 114.5 | 9 | 2.81 | 3.76e-06 (2^-18.02) | 18.02 |
| 20 | `pipelined_m:data_width=26,n_iter=23,angle_guard=-1,frac_guard=1,rounding=trunc,m=3` | 1976 | 745 | 110.0 | 10 | 3.27 | 1.05e-06 (2^-19.86) | 19.86 |
| 21 | `pipelined_m:data_width=28,n_iter=22,angle_guard=0,frac_guard=1,rounding=trunc,m=3` | 2041 | 805 | 110.0 | 10 | 3.43 | 5.73e-07 (2^-20.74) | 20.74 |
| 22 | `pipelined_m:data_width=25,n_iter=24,angle_guard=2,frac_guard=1,rounding=round,m=3` | 2118 | 745 | 110.0 | 10 | 3.45 | 4.78e-07 (2^-21.00) | 21.00 |
| 23 | `pipelined_m:data_width=26,n_iter=25,angle_guard=2,frac_guard=1,rounding=trunc,m=3` | 2231 | 859 | 110.0 | 11 | 3.72 | 4.09e-07 (2^-21.22) | 21.22 |
| 24 | `pipelined_m:data_width=27,n_iter=25,angle_guard=2,frac_guard=1,rounding=trunc,m=3` | 2307 | 888 | 110.0 | 11 | 3.85 | 2.59e-07 (2^-21.88) | 21.88 |
| 25 | `pipelined_m:data_width=27,n_iter=24,angle_guard=2,frac_guard=4,rounding=round,m=3` | 2413 | 839 | 105.9 | 10 | 3.92 | 1.68e-07 (2^-22.51) | 22.51 |
| 26 | `pipelined_m:data_width=27,n_iter=26,angle_guard=1,frac_guard=4,rounding=round,m=3` | 2591 | 929 | 105.9 | 11 | 4.24 | 1.42e-07 (2^-22.75) | 22.75 |
| 27 | `pipelined_m:data_width=28,n_iter=26,angle_guard=0,frac_guard=1,rounding=round,m=2` | 2488 | 1276 | 152.6 | 15 | 4.53 | 1.41e-07 (2^-22.76) | 22.76 |
| 28 | `pipelined_m:data_width=28,n_iter=25,angle_guard=4,frac_guard=4,rounding=trunc,m=2` | 2585 | 1399 | 147.4 | 15 | 4.8 | 7.8e-08 (2^-23.61) | 23.61 |
| 29 | `pipelined_m:data_width=28,n_iter=26,angle_guard=2,frac_guard=4,rounding=round,m=2` | 2699 | 1375 | 147.4 | 15 | 4.9 | 6.35e-08 (2^-23.91) | 23.91 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraints are the burst deadline and the accuracy floor. A 1 MHz tick dumps 32 requests at once and the last result must be back within 0.44 us, i.e. the unit must drain a 32-deep burst in ~32 service intervals plus pipeline latency. Only the fully-pipelined families (pipelined, pipelined_m) sustain 1 result/cycle, so 32 results cost ~32 cycles + latency, which is comfortably inside 0.44 us at any realistic Artix-7 clock (>= ~80 MHz suffices). iterative (N+3 cycles/result) and unrolled_k (ceil(N/k)+3 cycles/result) cannot drain the burst in time at achievable Fmax (e.g. unrolled_k k=8,N=8 still needs ~124 cycles for the last of 32 results), so they are excluded rather than wasting budget. Accuracy is identical across families and depends only on data_width/n_iter/angle_guard/frac_guard/rounding, so I sweep those around the 2^-12 boundary (W~13-16, N~13-15) and out to high accuracy to map the whole luts+ffs vs accuracy_bits front. Because the objective is min luts+ffs, pipelined_m is important: registering every m stages cuts pipeline FFs (area) at the cost of Fmax, and Fmax only has to stay above the ~80 MHz the batch deadline needs, so large m may be area-optimal. Round 1 is a broad coarse sweep of both families; later rounds will refine the feasible boundary and the m/Fmax trade-off.*)
- `pipelined` (45 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Baseline 1 result/cycle family with one micro-rotation per pipeline stage, giving the shortest combinational path and highest Fmax, hence the most margin on the 0.44 us batch deadline. Sweep W and N across the 2^-12 accuracy boundary (and beyond, up to ~20 bits) to locate the cheapest feasible point and the low-area end of the front; angle_guard/frac_guard/rounding are swept because they shift the accuracy/cost boundary at fixed W,N.
- `pipelined_m` (55 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Same 1 result/cycle throughput and identical accuracy model, but registers every m stages, so pipeline FF count drops roughly by a factor m while the combinational path (and thus Fmax) grows. Since the area objective is min luts+ffs and the batch deadline only needs Fmax above ~80 MHz, this family can dominate the low-area end of the front. Sweep m 2..8 together with W/N/guards/rounding to find the area-optimal design that still meets the burst deadline, and to expose the Fmax-limited boundary where large m stops being viable.

**Result (code):** 100 evaluations this round, 100 total; 50 feasible; hypervolume 1.117e+04 (n/a).

**LLM decision:** `map_front` — Round 1 gives a feasible front (10 designs, HV 1.117e4) but it is narrow and one-sided: luts_plus_ffs spans only 1459..2093 against an HV reference of 4000, with nothing below 1459 and nothing between 2093 and 4000, while accuracy_bits (13..16.9) sits entirely above the 12-bit reference. So the front covers only a small part of the area objective's range and leaves the accuracy-for-area trade unexplored. Every front design is pipelined/pipelined_m — the 1-result/cycle families — which is exactly what the system needs: the 32-request/0.44us burst implies ~73 MSPS effective, and the best sys_p99_batch seen is 0.154us vs the 0.44us limit. The unexplored families are the slow shared-datapath ones (iterative = N+3 cycles/result, unrolled_k = ceil(N/k)+3), which cannot sustain that burst rate, so spending a round on them is likely wasted. The right move is to let NSGA-II map the full front over the full ranges of pipelined and pipelined_m, seeded with the current front, to push toward cheaper designs (lower data_width/n_iter that still clear 12 bits) and extend the high-accuracy end.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 1.117e+04 (gain this round: n/a (first round)).
Feasible designs: 50 of 100 evaluations (39 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 45% violate; best seen 8.2e-06 (2^-16.90)
- sys_p99_batch_us <= 0.44: 12% violate; best seen 0.154

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=20 n_iter=14 angle_guard=3 frac_guard=2 rounding=round m=3] luts_plus_ffs=1459, accuracy_bits=13, luts=1047, ffs=412, throughput_msps=114, max_abs_err=0.000125 (2^-12.97), power_index=1.76
- pipelined_m [data_width=20 n_iter=14 angle_guard=3 frac_guard=4 rounding=round m=3] luts_plus_ffs=1530, accuracy_bits=13, luts=1102, ffs=428, throughput_msps=114, max_abs_err=0.000124 (2^-12.98), power_index=1.84
- pipelined_m [data_width=18 n_iter=16 angle_guard=3 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=1592, accuracy_bits=14.2, luts=1128, ffs=464, throughput_msps=119, max_abs_err=5.33e-05 (2^-14.20), power_index=1.92
- pipelined_m [data_width=20 n_iter=18 angle_guard=-1 frac_guard=1 rounding=round m=3] luts_plus_ffs=1700, accuracy_bits=14.2, luts=1248, ffs=452, throughput_msps=119, max_abs_err=5.19e-05 (2^-14.23), power_index=2.05
- pipelined_m [data_width=18 n_iter=19 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1737, accuracy_bits=15.5, luts=1352, ffs=385, throughput_msps=93.6, max_abs_err=2.16e-05 (2^-15.50), power_index=2.09
- pipelined_m [data_width=18 n_iter=19 angle_guard=3 frac_guard=4 rounding=round m=3] luts_plus_ffs=1929, accuracy_bits=15.5, luts=1390, ffs=539, throughput_msps=119, max_abs_err=2.1e-05 (2^-15.54), power_index=2.32
- pipelined_m [data_width=20 n_iter=19 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=1943, accuracy_bits=16.2, luts=1394, ffs=549, throughput_msps=114, max_abs_err=1.31e-05 (2^-16.22), power_index=2.34
- pipelined_m [data_width=20 n_iter=19 angle_guard=3 frac_guard=2 rounding=round m=3] luts_plus_ffs=1993, accuracy_bits=16.6, luts=1432, ffs=561, throughput_msps=114, max_abs_err=1.04e-05 (2^-16.56), power_index=2.4
- pipelined_m [data_width=20 n_iter=19 angle_guard=2 frac_guard=3 rounding=round m=3] luts_plus_ffs=2017, accuracy_bits=16.6, luts=1451, ffs=566, throughput_msps=114, max_abs_err=1.02e-05 (2^-16.59), power_index=2.43
- pipelined_m [data_width=20 n_iter=19 angle_guard=3 frac_guard=4 rounding=round m=3] luts_plus_ffs=2093, accuracy_bits=16.9, luts=1508, ffs=585, throughput_msps=114, max_abs_err=8.2e-06 (2^-16.90), power_index=2.52
Front coverage: luts_plus_ffs 1459..2093 (HV reference 4000); accuracy_bits 13..16.9 (HV reference 12); data_width on the front 18..20 (registry 8..28).

Per family:
- pipelined: 45 evals, 22 feasible; max throughput seen 282 MSPS; best accuracy 15.38 bits; best feasible luts_plus_ffs=1998; feasible ranges: data_width 16..20, n_iter 16..20, angle_guard -2..4, frac_guard 1..4
- pipelined_m: 55 evals, 28 feasible; max throughput seen 171 MSPS; best accuracy 16.90 bits; best feasible luts_plus_ffs=1459; feasible ranges: data_width 18..20, n_iter 14..20, angle_guard -1..4, frac_guard 0..4, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (10 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 118 feasible; hypervolume 1.766e+04 (+58.0%).

**LLM decision:** `refine` — The front already spans luts_plus_ffs 1459..3984 against HV ref 4000 and accuracy 13..23.6 bits against ref 12, so the high-luts/high-accuracy side is well covered and further HV gain must come from extending the low-luts corner (cheapest feasible is 1459, pipelined_m W=20/N=14/m=3). That same cheapest design has only 114 MSPS and ~16-cycle latency, i.e. a 32-request burst lands near 0.42 us vs the 0.44 us bound, so it is exactly the kind of design the L2 sim may drop; pushing data_width and n_iter down both lowers area and buys batch margin. iterative/unrolled_k are not worth budget: their throughput is Fmax/(N+3) or Fmax/(ceil(N/k)+3), which cannot sustain 32 requests inside 0.44 us (best pipelined throughput seen is 282 MSPS, and even k=8/N=4 unrolled gives ~4 cycles/result), so they cannot meet sys_p99_batch_us.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.766e+04 (gain this round: +58.0%).
Feasible designs: 118 of 200 evaluations (99 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 25% violate; best seen 4.18e-08 (2^-24.51)
- sys_p99_batch_us <= 0.44: 20% violate; best seen 0.154

Pareto front (feasible, 20 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=20 n_iter=14 angle_guard=3 frac_guard=2 rounding=round m=3] luts_plus_ffs=1459, accuracy_bits=13, luts=1047, ffs=412, throughput_msps=114, max_abs_err=0.000125 (2^-12.97), power_index=1.76
- pipelined_m [data_width=18 n_iter=16 angle_guard=3 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=1592, accuracy_bits=14.2, luts=1128, ffs=464, throughput_msps=119, max_abs_err=5.33e-05 (2^-14.20), power_index=1.92
- pipelined_m [data_width=18 n_iter=19 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1737, accuracy_bits=15.5, luts=1352, ffs=385, throughput_msps=93.6, max_abs_err=2.16e-05 (2^-15.50), power_index=2.09
- pipelined_m [data_width=20 n_iter=19 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=1943, accuracy_bits=16.2, luts=1394, ffs=549, throughput_msps=114, max_abs_err=1.31e-05 (2^-16.22), power_index=2.34
- pipelined_m [data_width=20 n_iter=19 angle_guard=2 frac_guard=3 rounding=round m=3] luts_plus_ffs=2017, accuracy_bits=16.6, luts=1451, ffs=566, throughput_msps=114, max_abs_err=1.02e-05 (2^-16.59), power_index=2.43
- pipelined_m [data_width=26 n_iter=19 angle_guard=-2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=2299, accuracy_bits=17.6, luts=1636, ffs=663, throughput_msps=110, max_abs_err=4.93e-06 (2^-17.63), power_index=2.77
- pipelined_m [data_width=26 n_iter=23 angle_guard=-1 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=2720, accuracy_bits=19.9, luts=1976, ffs=745, throughput_msps=110, max_abs_err=1.05e-06 (2^-19.86), power_index=3.27
- pipelined_m [data_width=26 n_iter=25 angle_guard=2 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=3089, accuracy_bits=21.2, luts=2231, ffs=859, throughput_msps=110, max_abs_err=4.09e-07 (2^-21.22), power_index=3.72
- pipelined_m [data_width=25 n_iter=25 angle_guard=4 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=3253, accuracy_bits=21.9, luts=2357, ffs=896, throughput_msps=110, max_abs_err=2.52e-07 (2^-21.92), power_index=3.92
- pipelined_m [data_width=28 n_iter=25 angle_guard=4 frac_guard=4 rounding=trunc m=2] luts_plus_ffs=3984, accuracy_bits=23.6, luts=2585, ffs=1399, throughput_msps=147, max_abs_err=7.8e-08 (2^-23.61), power_index=4.8
Front coverage: luts_plus_ffs 1459..3984 (HV reference 4000); accuracy_bits 13..23.6 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- pipelined: 45 evals, 22 feasible; max throughput seen 282 MSPS; best accuracy 15.38 bits; best feasible luts_plus_ffs=1998; feasible ranges: data_width 16..20, n_iter 16..20, angle_guard -2..4, frac_guard 1..4
- pipelined_m: 155 evals, 96 feasible; max throughput seen 171 MSPS; best accuracy 24.51 bits; best feasible luts_plus_ffs=1459; feasible ranges: data_width 17..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Refine the low-luts corner of the two families already on the front; reserve the final round for a full-range map_front over pipelined/pipelined_m.*)
- `pipelined_m` (75 evals): data_width=15..20, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..5. *Why:* Dominant family (96 feasible, cheapest front point 1459); search below the current cheapest corner in data_width/n_iter while keeping accuracy >= 12 bits, and probe m=5 for lower latency.
- `pipelined` (25 evals): data_width=15..20, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Best feasible luts_plus_ffs is 1998 but it registers every stage, so it may reach higher Fmax (better batch margin) at low data_width; small share to check the low-area corner.

**Result (code):** 100 evaluations this round, 300 total; 171 feasible; hypervolume 1.822e+04 (+3.2%).

**LLM decision:** `map_front` — Round 3 left the front well-covered: luts_plus_ffs 1227..3984 against HV ref 4000 and accuracy_bits 12..23.6 against HV ref 12, i.e. the front already spans nearly the whole reference box, and the only objective range still open is the low-area end (data_width 16 on the front vs registry 8..28, but accuracy >= 2^-12 caps how low W can go). The two unexplored families are poor bets: the system scenario needs 32 results back within 0.44 us of each 1 us tick, i.e. ~1 result/cycle sustained, whereas iterative (N+3 cycles/result) and unrolled_k (ceil(N/k)+3, >=5 cycles/result even at k=8) would need 160-544 cycles per burst and so would fail the L1 sys_p99_batch_us bound outright (best feasible value seen is 0.154 us, and L1 is already optimistic). Spending the last 100 evals on them would only produce L1-infeasible points. The reserved end-of-run mapping is therefore the right use of the remaining budget: NSGA-II over the full ranges of the two families that actually sit on the front (pipelined, pipelined_m), seeded with the current 25-design front, to close the low-area gap and densify the curve before selection (min luts_plus_ffs).

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.822e+04 (gain this round: +3.2%).
Feasible designs: 171 of 300 evaluations (142 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 31% violate; best seen 4.18e-08 (2^-24.51)
- sys_p99_batch_us <= 0.44: 15% violate; best seen 0.154

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=-2 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1227, accuracy_bits=12, luts=868, ffs=359, throughput_msps=119, max_abs_err=0.000241 (2^-12.02), power_index=1.48
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1313, accuracy_bits=13.5, luts=1017, ffs=297, throughput_msps=93.6, max_abs_err=8.82e-05 (2^-13.47), power_index=1.58
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=3 rounding=round m=4] luts_plus_ffs=1429, accuracy_bits=14.3, luts=1118, ffs=311, throughput_msps=93.6, max_abs_err=5.03e-05 (2^-14.28), power_index=1.72
- pipelined_m [data_width=19 n_iter=16 angle_guard=4 frac_guard=2 rounding=round m=4] luts_plus_ffs=1494, accuracy_bits=14.6, luts=1168, ffs=327, throughput_msps=89.6, max_abs_err=3.9e-05 (2^-14.64), power_index=1.8
- pipelined_m [data_width=20 n_iter=19 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=1943, accuracy_bits=16.2, luts=1394, ffs=549, throughput_msps=114, max_abs_err=1.31e-05 (2^-16.22), power_index=2.34
- pipelined_m [data_width=20 n_iter=19 angle_guard=2 frac_guard=3 rounding=round m=3] luts_plus_ffs=2017, accuracy_bits=16.6, luts=1451, ffs=566, throughput_msps=114, max_abs_err=1.02e-05 (2^-16.59), power_index=2.43
- pipelined_m [data_width=26 n_iter=19 angle_guard=-2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=2299, accuracy_bits=17.6, luts=1636, ffs=663, throughput_msps=110, max_abs_err=4.93e-06 (2^-17.63), power_index=2.77
- pipelined_m [data_width=28 n_iter=22 angle_guard=0 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=2846, accuracy_bits=20.7, luts=2041, ffs=805, throughput_msps=110, max_abs_err=5.73e-07 (2^-20.74), power_index=3.43
- pipelined_m [data_width=27 n_iter=25 angle_guard=2 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=3195, accuracy_bits=21.9, luts=2307, ffs=888, throughput_msps=110, max_abs_err=2.59e-07 (2^-21.88), power_index=3.85
- pipelined_m [data_width=28 n_iter=25 angle_guard=4 frac_guard=4 rounding=trunc m=2] luts_plus_ffs=3984, accuracy_bits=23.6, luts=2585, ffs=1399, throughput_msps=147, max_abs_err=7.8e-08 (2^-23.61), power_index=4.8
Front coverage: luts_plus_ffs 1227..3984 (HV reference 4000); accuracy_bits 12..23.6 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- pipelined: 70 evals, 29 feasible; max throughput seen 282 MSPS; best accuracy 15.38 bits; best feasible luts_plus_ffs=1875; feasible ranges: data_width 16..20, n_iter 14..20, angle_guard -2..4, frac_guard 1..4
- pipelined_m: 230 evals, 142 feasible; max throughput seen 171 MSPS; best accuracy 24.51 bits; best feasible luts_plus_ffs=1227; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (25 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 237 feasible; hypervolume 1.866e+04 (+2.4%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), so no further exploration is possible. The front is feasible and well-covered: 237 feasible designs (204 unique), 30 on the Pareto front, spanning luts_plus_ffs 1227..4074 against an HV reference of 4000 and accuracy_bits 12..23.9 against an HV reference of 12, with hypervolume 1.866e+04 still gaining (+2.4%). All three constraints are comfortably met by the front's cheapest design (pipelined_m, data_width=19, n_iter=14, angle_guard=-2, frac_guard=1, trunc, m=3): throughput 119 MSPS >= 32, max_abs_err 2.41e-4 <= 2.44e-4, and sys_p99_batch_us best seen 0.154 <= 0.44. The selection rule (min luts_plus_ffs) picks that 1227 LUT+FF design, which is the smallest feasible point found. No constraint is unreachable, so infeasible is not warranted; the front is good enough to stop.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.866e+04 (gain this round: +2.4%).
Feasible designs: 237 of 400 evaluations (204 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 26% violate; best seen 4.18e-08 (2^-24.51)
- sys_p99_batch_us <= 0.44: 19% violate; best seen 0.154

Pareto front (feasible, 30 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=-2 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1227, accuracy_bits=12, luts=868, ffs=359, throughput_msps=119, max_abs_err=0.000241 (2^-12.02), power_index=1.48
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1298, accuracy_bits=13.3, luts=994, ffs=305, throughput_msps=93.6, max_abs_err=0.000102 (2^-13.26), power_index=1.56
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=3 rounding=round m=4] luts_plus_ffs=1429, accuracy_bits=14.3, luts=1118, ffs=311, throughput_msps=93.6, max_abs_err=5.03e-05 (2^-14.28), power_index=1.72
- pipelined_m [data_width=18 n_iter=19 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1737, accuracy_bits=15.5, luts=1352, ffs=385, throughput_msps=93.6, max_abs_err=2.16e-05 (2^-15.50), power_index=2.09
- pipelined_m [data_width=20 n_iter=18 angle_guard=4 frac_guard=4 rounding=round m=3] luts_plus_ffs=1957, accuracy_bits=16.5, luts=1445, ffs=513, throughput_msps=114, max_abs_err=1.06e-05 (2^-16.52), power_index=2.36
- pipelined_m [data_width=21 n_iter=19 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=2023, accuracy_bits=16.6, luts=1453, ffs=570, throughput_msps=114, max_abs_err=9.84e-06 (2^-16.63), power_index=2.44
- pipelined_m [data_width=24 n_iter=21 angle_guard=-1 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=2336, accuracy_bits=18, luts=1712, ffs=624, throughput_msps=114, max_abs_err=3.76e-06 (2^-18.02), power_index=2.81
- pipelined_m [data_width=26 n_iter=25 angle_guard=2 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=3089, accuracy_bits=21.2, luts=2231, ffs=859, throughput_msps=110, max_abs_err=4.09e-07 (2^-21.22), power_index=3.72
- pipelined_m [data_width=27 n_iter=26 angle_guard=1 frac_guard=4 rounding=round m=3] luts_plus_ffs=3520, accuracy_bits=22.8, luts=2591, ffs=929, throughput_msps=106, max_abs_err=1.42e-07 (2^-22.75), power_index=4.24
- pipelined_m [data_width=28 n_iter=26 angle_guard=2 frac_guard=4 rounding=round m=2] luts_plus_ffs=4074, accuracy_bits=23.9, luts=2699, ffs=1375, throughput_msps=147, max_abs_err=6.35e-08 (2^-23.91), power_index=4.9
Front coverage: luts_plus_ffs 1227..4074 (HV reference 4000); accuracy_bits 12..23.9 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- pipelined: 70 evals, 29 feasible; max throughput seen 282 MSPS; best accuracy 15.38 bits; best feasible luts_plus_ffs=1875; feasible ranges: data_width 16..20, n_iter 14..20, angle_guard -2..4, frac_guard 1..4
- pipelined_m: 330 evals, 208 feasible; max throughput seen 171 MSPS; best accuracy 24.51 bits; best feasible luts_plus_ffs=1227; feasible ranges: data_width 15..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 16643 in, 26381 out
- provider-reported cost: $0.0185
- full prompts and replies: `llm_trace.jsonl`

