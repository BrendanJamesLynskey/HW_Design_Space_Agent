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
`pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=3,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 923 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 305 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.48 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000157 (2^-12.64) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 10.3 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.12e-05 (2^-14.25) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.36 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.6 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 98.2 dBc, SNR 82.8 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=3,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=19,n_iter=15,angle_guard=3,frac_guard=0,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=3,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=19,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (24 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=3,rounding=trunc,m=4` | 923 | 305 | 93.6 | 6 | 1.48 | 0.000157 (2^-12.64) | 12.64 |
| 1 | `pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 985 | 289 | 93.6 | 6 | 1.53 | 0.000136 (2^-12.84) | 12.84 |
| 2 | `pipelined_m:data_width=19,n_iter=15,angle_guard=3,frac_guard=0,rounding=trunc,m=4` | 979 | 309 | 93.6 | 6 | 1.55 | 0.000109 (2^-13.17) | 13.17 |
| 3 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=3,rounding=trunc,m=4` | 994 | 305 | 93.6 | 6 | 1.56 | 0.000102 (2^-13.26) | 13.26 |
| 4 | `pipelined_m:data_width=19,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1008 | 313 | 93.6 | 6 | 1.59 | 8.04e-05 (2^-13.60) | 13.60 |
| 5 | `pipelined_m:data_width=19,n_iter=16,angle_guard=4,frac_guard=1,rounding=trunc,m=4` | 1096 | 319 | 89.6 | 6 | 1.7 | 5.68e-05 (2^-14.10) | 14.10 |
| 6 | `pipelined_m:data_width=19,n_iter=16,angle_guard=4,frac_guard=2,rounding=trunc,m=4` | 1128 | 325 | 89.6 | 6 | 1.75 | 4.67e-05 (2^-14.39) | 14.39 |
| 7 | `pipelined_m:data_width=19,n_iter=16,angle_guard=4,frac_guard=2,rounding=round,m=4` | 1168 | 327 | 89.6 | 6 | 1.8 | 3.9e-05 (2^-14.64) | 14.64 |
| 8 | `pipelined_m:data_width=19,n_iter=16,angle_guard=4,frac_guard=4,rounding=trunc,m=4` | 1191 | 337 | 89.6 | 6 | 1.84 | 3.9e-05 (2^-14.64) | 14.64 |
| 9 | `pipelined_m:data_width=19,n_iter=17,angle_guard=2,frac_guard=3,rounding=trunc,m=4` | 1202 | 395 | 93.6 | 7 | 1.92 | 3.2e-05 (2^-14.93) | 14.93 |
| 10 | `pipelined_m:data_width=19,n_iter=17,angle_guard=4,frac_guard=4,rounding=trunc,m=4` | 1270 | 414 | 89.6 | 7 | 2.03 | 2.49e-05 (2^-15.29) | 15.29 |
| 11 | `pipelined_m:data_width=21,n_iter=17,angle_guard=1,frac_guard=4,rounding=trunc,m=4` | 1320 | 433 | 89.6 | 7 | 2.11 | 2.08e-05 (2^-15.55) | 15.55 |
| 12 | `pipelined_m:data_width=21,n_iter=17,angle_guard=2,frac_guard=4,rounding=trunc,m=4` | 1337 | 438 | 89.6 | 7 | 2.14 | 1.83e-05 (2^-15.74) | 15.74 |
| 13 | `pipelined_m:data_width=21,n_iter=18,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1393 | 424 | 89.6 | 7 | 2.19 | 1.11e-05 (2^-16.46) | 16.46 |
| 14 | `pipelined_m:data_width=21,n_iter=19,angle_guard=2,frac_guard=3,rounding=trunc,m=4` | 1466 | 430 | 89.6 | 7 | 2.28 | 8.4e-06 (2^-16.86) | 16.86 |
| 15 | `pipelined_m:data_width=21,n_iter=21,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1630 | 500 | 89.6 | 8 | 2.56 | 5.47e-06 (2^-17.48) | 17.48 |
| 16 | `pipelined_m:data_width=23,n_iter=20,angle_guard=0,frac_guard=2,rounding=round,m=3` | 1635 | 609 | 114.5 | 9 | 2.7 | 4.21e-06 (2^-17.86) | 17.86 |
| 17 | `pipelined_m:data_width=23,n_iter=20,angle_guard=1,frac_guard=2,rounding=round,m=3` | 1655 | 616 | 114.5 | 9 | 2.73 | 3.47e-06 (2^-18.13) | 18.13 |
| 18 | `pipelined_m:data_width=24,n_iter=23,angle_guard=3,frac_guard=3,rounding=round,m=3` | 2073 | 755 | 110.0 | 10 | 3.4 | 5.25e-07 (2^-20.86) | 20.86 |
| 19 | `pipelined_m:data_width=28,n_iter=23,angle_guard=3,frac_guard=4,rounding=round,m=3` | 2406 | 874 | 105.9 | 10 | 3.95 | 2.52e-07 (2^-21.92) | 21.92 |
| 20 | `pipelined_m:data_width=28,n_iter=28,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 2708 | 1023 | 105.9 | 12 | 4.49 | 1e-07 (2^-23.25) | 23.25 |
| 21 | `pipelined_m:data_width=28,n_iter=28,angle_guard=1,frac_guard=4,rounding=trunc,m=3` | 2822 | 1057 | 105.9 | 12 | 4.67 | 8.37e-08 (2^-23.51) | 23.51 |
| 22 | `pipelined:data_width=28,n_iter=29,angle_guard=2,frac_guard=4,rounding=round` | 3015 | 2941 | 242.0 | 31 | 7.17 | 4.07e-08 (2^-24.55) | 24.55 |
| 23 | `pipelined:data_width=28,n_iter=30,angle_guard=4,frac_guard=4,rounding=round` | 3181 | 3103 | 242.0 | 32 | 7.56 | 1.68e-08 (2^-25.83) | 25.83 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraints are the 32-request burst (sys_p99_batch_us <= 0.44) and throughput >= 32 Msps, both of which force a 1-result/cycle datapath: only pipelined and pipelined_m can drain 32 requests in ~32 cycles + latency, whereas iterative (N+3 cycles/result) and unrolled_k (ceil(N/k)+3 cycles/result) cannot fit a 32-wide burst in 0.44 us at any realistic Fmax. Accuracy (max_abs_err <= 2^-12) depends only on data_width/n_iter/angle_guard/frac_guard/rounding, so the W and N ranges are set to straddle the 2^-12 output-LSB boundary (W=14) and the ~W iteration convergence point, letting the search find the smallest area that still passes. The objective min luts_plus_ffs is served by pipelined_m's register reduction, while pipelined provides the high-Fmax anchor that guarantees batch-latency margin. Budget is split ~45/45 between the two feasible families to map both ends of the area-vs-Fmax front, with a 10% probe on unrolled_k to verify infeasibility rather than assume it. Later rounds should reallocate toward whichever of pipelined/pipelined_m dominates the front and refine m, W and N near the accuracy boundary.*)
- `pipelined` (45 evals): data_width=12..20, n_iter=10..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Only 1-result/cycle families can drain a 32-request burst inside 0.44 us: 32 back-to-back results cost ~32 cycles + N+2 latency, which fits comfortably at any plausible Fmax, and throughput = Fmax >= 32 Msps is trivially met. Full per-stage registration gives the highest Fmax (best sys_p99_batch margin) at the cost of the most FFs, so it anchors the low-latency/high-area end of the front. W range straddles the 2^-12 output-LSB boundary (W=14 -> LSB 2^-12) so the search can find the smallest W that still satisfies max_abs_err; N range brackets the ~W iterations needed for convergence.
- `pipelined_m` (45 evals): data_width=12..20, n_iter=10..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Same 1-result/cycle throughput and identical bit-accurate accuracy as pipelined, but registering every m stages cuts FF count (the min-luts_plus_ffs objective) at the price of a longer combinational path and lower Fmax. This is the main area-vs-Fmax trade-off axis of the front: m=2 approaches pipelined, m=8 minimises registers. Must be explored densely because the selection rule (min luts_plus_ffs) will likely land here, while the batch constraint keeps a floor on Fmax.
- `unrolled_k` (10 evals): data_width=12..18, n_iter=8..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=6..8. *Why:* Probe only. A 32-request burst costs 32*(ceil(N/k)+3) cycles, so even k=8 needs ~128 cycles and Fmax > ~290 MHz to fit 0.44 us, and the small N that would allow it cannot reach 2^-12 accuracy. Included at low share to confirm the analytic batch bound rules it out rather than assume it, and to catch any edge case where a heavily unrolled variant is unexpectedly feasible.

**Result (code):** 100 evaluations this round, 100 total; 37 feasible; hypervolume 7913 (n/a).

**LLM decision:** `widen` — Only `pipelined` and `pipelined_m` can be on this front: both emit 1 result/cycle, whereas `unrolled_k` topped out at 13.8 MSPS (0/10 feasible) and `iterative` needs N+3 cycles/result, so it cannot reach the 32 MSPS floor at any N that also gives 12+ accuracy bits — no budget should go to those two. The current HV (7913) is dominated by two under-covered regions. (1) The top extension: the front stops at luts_plus_ffs=2618 / 15.5 bits while the HV reference is 4000, so the (4000-2618)*(15.5-12)≈4.8k term is the single largest HV contributor and is only half-filled. (2) The gap between the cheap pipelined_m cluster (1228..1552) and the pipelined cluster (2504..2618), worth ≈2.4k. Both are reachable only by pushing data_width/n_iter above what round 1 sampled: data_width on the front is just 18..20 (registry 8..28) and n_iter 14..19 (registry 4..30), i.e. the high-accuracy corner is unexplored. Separately, every cheap pipelined_m design runs at 93.6 MSPS, so a 32-request burst drains in ~32 cycles and only just fits the 0.44 us sys_p99_batch_us bound; since the L1 screen is optimistic and the cheapest design is what `select: min luts_plus_ffs` will pick, we must also probe m=2,3 (higher Fmax, more system margin) so the min-area pick is not lost at L2.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 7913 (gain this round: n/a (first round)).
Feasible designs: 37 of 100 evaluations (34 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 10% violate; best seen 282
- max_abs_err <= 0.000244141: 52% violate; best seen 2.17e-05 (2^-15.49)
- sys_p99_batch_us <= 0.44: 28% violate; best seen 0.158

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1228, accuracy_bits=12.6, luts=923, ffs=305, throughput_msps=93.6, max_abs_err=0.000157 (2^-12.64), power_index=1.48
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1274, accuracy_bits=12.8, luts=985, ffs=289, throughput_msps=93.6, max_abs_err=0.000136 (2^-12.84), power_index=1.53
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1298, accuracy_bits=13.3, luts=994, ffs=305, throughput_msps=93.6, max_abs_err=0.000102 (2^-13.26), power_index=1.56
- pipelined_m [data_width=20 n_iter=15 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1415, accuracy_bits=13.8, luts=1082, ffs=333, throughput_msps=89.6, max_abs_err=7.14e-05 (2^-13.77), power_index=1.7
- pipelined_m [data_width=18 n_iter=17 angle_guard=3 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1552, accuracy_bits=14.5, luts=1169, ffs=383, throughput_msps=93.6, max_abs_err=4.47e-05 (2^-14.45), power_index=1.87
- pipelined [data_width=18 n_iter=18 angle_guard=2 frac_guard=3 rounding=round] luts_plus_ffs=2504, accuracy_bits=14.8, luts=1261, ffs=1243, throughput_msps=264, max_abs_err=3.55e-05 (2^-14.78), power_index=3.01
- pipelined [data_width=20 n_iter=19 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=2618, accuracy_bits=15.5, luts=1295, ffs=1323, throughput_msps=264, max_abs_err=2.17e-05 (2^-15.49), power_index=3.15
Front coverage: luts_plus_ffs 1228..2618 (HV reference 4000); accuracy_bits 12.6..15.5 (HV reference 12); data_width on the front 18..20 (registry 8..28).

Per family:
- unrolled_k: 10 evals, 0 feasible; max throughput seen 13.8 MSPS; best accuracy 11.59 bits
- pipelined: 45 evals, 21 feasible; max throughput seen 282 MSPS; best accuracy 15.49 bits; best feasible luts_plus_ffs=1988; feasible ranges: data_width 15..20, n_iter 16..21, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 45 evals, 16 feasible; max throughput seen 171 MSPS; best accuracy 15.44 bits; best feasible luts_plus_ffs=1228; feasible ranges: data_width 17..20, n_iter 14..18, angle_guard -2..3, frac_guard 1..3, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *widen data_width/n_iter on the two viable families to cover the gap and the top of the front; keep m=2,3 in play for L2 system margin on the cheap designs*)
- `pipelined_m` (50 evals): data_width=16..22, n_iter=14..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* fill the 1552..2504 gap with higher data_width/n_iter, extend the cheap end below 1228, and test m=2,3 for Fmax/system margin
- `pipelined` (50 evals): data_width=18..26, n_iter=16..28, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* extend the high-accuracy end past 15.5 bits toward the 4000 luts_plus_ffs HV reference

**Result (code):** 100 evaluations this round, 200 total; 134 feasible; hypervolume 1.209e+04 (+52.8%).

**LLM decision:** `refine` — The front is feasible and improving (+52.8% HV), and its two ends are well covered (luts_plus_ffs 1228..3963 vs ref 4000; accuracy_bits 12.6..19.9 vs ref 12), so a full map_front is premature. The clear defect is a hole in the middle of the curve: pipelined_m tops out at 2078 LUT+FF / 15.6 bits while pipelined only starts at 3032 / 16.8 bits, so the 2078..3032 band is unmapped and is pure lost hypervolume. pipelined_m is also the family that owns the selection rule's target (cheapest feasible = 1228, data_width=18 n_iter=14 m=4, 93.6 MSPS, 12.6 bits), so sharpening its low-area boundary is worth budget. iterative is not worth adding: its faster cousin unrolled_k already got 0 feasible with max 13.8 MSPS, far under the 32 MSPS constraint, so 1 micro-rotation/cycle cannot qualify.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.209e+04 (gain this round: +52.8%).
Feasible designs: 134 of 200 evaluations (121 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 5% violate; best seen 282
- max_abs_err <= 0.000244141: 28% violate; best seen 1.03e-06 (2^-19.88)
- sys_p99_batch_us <= 0.44: 14% violate; best seen 0.158

Pareto front (feasible, 32 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1228, accuracy_bits=12.6, luts=923, ffs=305, throughput_msps=93.6, max_abs_err=0.000157 (2^-12.64), power_index=1.48
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1298, accuracy_bits=13.3, luts=994, ffs=305, throughput_msps=93.6, max_abs_err=0.000102 (2^-13.26), power_index=1.56
- pipelined_m [data_width=19 n_iter=16 angle_guard=4 frac_guard=2 rounding=round m=4] luts_plus_ffs=1494, accuracy_bits=14.6, luts=1168, ffs=327, throughput_msps=89.6, max_abs_err=3.9e-05 (2^-14.64), power_index=1.8
- pipelined_m [data_width=18 n_iter=17 angle_guard=4 frac_guard=2 rounding=round m=3] luts_plus_ffs=1642, accuracy_bits=14.8, luts=1190, ffs=452, throughput_msps=119, max_abs_err=3.5e-05 (2^-14.80), power_index=1.98
- pipelined_m [data_width=18 n_iter=21 angle_guard=3 frac_guard=4 rounding=round m=3] luts_plus_ffs=2078, accuracy_bits=15.6, luts=1540, ffs=539, throughput_msps=119, max_abs_err=2.02e-05 (2^-15.60), power_index=2.5
- pipelined [data_width=21 n_iter=20 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=3032, accuracy_bits=16.8, luts=1507, ffs=1525, throughput_msps=257, max_abs_err=8.61e-06 (2^-16.83), power_index=3.65
- pipelined [data_width=25 n_iter=20 angle_guard=-1 frac_guard=1 rounding=round] luts_plus_ffs=3372, accuracy_bits=18.2, luts=1700, ffs=1673, throughput_msps=257, max_abs_err=3.39e-06 (2^-18.17), power_index=4.06
- pipelined [data_width=25 n_iter=20 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=3493, accuracy_bits=18.8, luts=1760, ffs=1733, throughput_msps=249, max_abs_err=2.16e-06 (2^-18.82), power_index=4.2
- pipelined [data_width=25 n_iter=22 angle_guard=-1 frac_guard=3 rounding=trunc] luts_plus_ffs=3827, accuracy_bits=19, luts=1908, ffs=1919, throughput_msps=249, max_abs_err=1.96e-06 (2^-18.96), power_index=4.61
- pipelined [data_width=26 n_iter=21 angle_guard=4 frac_guard=2 rounding=round] luts_plus_ffs=3963, accuracy_bits=19.9, luts=1999, ffs=1964, throughput_msps=249, max_abs_err=1.03e-06 (2^-19.88), power_index=4.77
Front coverage: luts_plus_ffs 1228..3963 (HV reference 4000); accuracy_bits 12.6..19.9 (HV reference 12); data_width on the front 18..26 (registry 8..28).

Per family:
- unrolled_k: 10 evals, 0 feasible; max throughput seen 13.8 MSPS; best accuracy 11.59 bits
- pipelined: 95 evals, 70 feasible; max throughput seen 282 MSPS; best accuracy 19.88 bits; best feasible luts_plus_ffs=1988; feasible ranges: data_width 15..26, n_iter 16..28, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 95 evals, 64 feasible; max throughput seen 171 MSPS; best accuracy 16.14 bits; best feasible luts_plus_ffs=1228; feasible ranges: data_width 17..22, n_iter 14..22, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Fill the mid-front gap from both sides and sharpen the low-area boundary that the min-luts_plus_ffs selection rule actually picks, keeping the front's throughput spread (89..257 MSPS) so L2 re-selection has alternatives if the cheapest pipelined_m designs lose margin on sys_p99_batch_us.*)
- `pipelined_m` (24 evals): data_width=17..22, n_iter=13..28, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..6. *Why:* Owns the cheapest feasible design (1228 LUT+FF, 12.6 bits) and the whole low-area end; extending n_iter/data_width and m beyond the explored 2..4 should fill the 2078..3032 gap and probe whether anything below 1228 is feasible.
- `pipelined` (16 evals): data_width=18..24, n_iter=16..26, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Its cheapest front point is 3032 LUT+FF / 16.8 bits; searching smaller data_width and n_iter should push that boundary down into the 2078..3032 hole and densify the high-accuracy end.

**Result (code):** 40 evaluations this round, 240 total; 168 feasible; hypervolume 1.309e+04 (+8.3%).

**LLM decision:** `stop` — Final round: 240/400 evals used, 168 feasible designs (152 unique), 24-design Pareto front, HV 1.309e+04 (+8.3%). The spec is satisfiable — all three constraints are met with margin by front designs (throughput best 282 vs >=32; max_abs_err best 1.03e-06 vs <=2.44e-04; sys_p99_batch_us best 0.158 vs <=0.44), so `infeasible` is not warranted. The selected design (min luts_plus_ffs) is pipelined_m [W=18 N=14 ag=1 fg=3 trunc m=4] at luts_plus_ffs=1228, accuracy_bits=12.6 (max_abs_err 1.57e-04 <= 2.44e-04), throughput 93.6 MSPS >= 32, and the front covers luts_plus_ffs 1228..3963 (HV ref 4000) with accuracy_bits 12.6..19.9 (HV ref 12), i.e. the useful part of both objective ranges is already mapped. Gains are diminishing and the round cap is reached; further exploration would only be spent on the iterative family, which the registry predicts is low-throughput and cannot improve the min-area corner already found. Stop and let the spec's selection rule take the min-luts_plus_ffs front point, subject to the L2 re-selection of the shortlist.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 1.309e+04 (gain this round: +8.3%).
Feasible designs: 168 of 240 evaluations (152 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 4% violate; best seen 282
- max_abs_err <= 0.000244141: 23% violate; best seen 1.03e-06 (2^-19.88)
- sys_p99_batch_us <= 0.44: 14% violate; best seen 0.158

Pareto front (feasible, 24 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1228, accuracy_bits=12.6, luts=923, ffs=305, throughput_msps=93.6, max_abs_err=0.000157 (2^-12.64), power_index=1.48
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1298, accuracy_bits=13.3, luts=994, ffs=305, throughput_msps=93.6, max_abs_err=0.000102 (2^-13.26), power_index=1.56
- pipelined_m [data_width=19 n_iter=16 angle_guard=4 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1415, accuracy_bits=14.1, luts=1096, ffs=319, throughput_msps=89.6, max_abs_err=5.68e-05 (2^-14.10), power_index=1.7
- pipelined_m [data_width=19 n_iter=16 angle_guard=4 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=1528, accuracy_bits=14.6, luts=1191, ffs=337, throughput_msps=89.6, max_abs_err=3.9e-05 (2^-14.64), power_index=1.84
- pipelined_m [data_width=21 n_iter=17 angle_guard=1 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=1753, accuracy_bits=15.6, luts=1320, ffs=433, throughput_msps=89.6, max_abs_err=2.08e-05 (2^-15.55), power_index=2.11
- pipelined_m [data_width=22 n_iter=21 angle_guard=0 frac_guard=0 rounding=trunc m=2] luts_plus_ffs=2377, accuracy_bits=16.1, luts=1523, ffs=855, throughput_msps=164, max_abs_err=1.39e-05 (2^-16.14), power_index=2.86
- pipelined [data_width=25 n_iter=20 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=3475, accuracy_bits=18.7, luts=1727, ffs=1747, throughput_msps=249, max_abs_err=2.39e-06 (2^-18.67), power_index=4.18
- pipelined [data_width=26 n_iter=20 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=3635, accuracy_bits=18.9, luts=1807, ffs=1828, throughput_msps=249, max_abs_err=2.08e-06 (2^-18.88), power_index=4.38
- pipelined [data_width=25 n_iter=22 angle_guard=-1 frac_guard=3 rounding=trunc] luts_plus_ffs=3827, accuracy_bits=19, luts=1908, ffs=1919, throughput_msps=249, max_abs_err=1.96e-06 (2^-18.96), power_index=4.61
- pipelined [data_width=26 n_iter=21 angle_guard=4 frac_guard=2 rounding=round] luts_plus_ffs=3963, accuracy_bits=19.9, luts=1999, ffs=1964, throughput_msps=249, max_abs_err=1.03e-06 (2^-19.88), power_index=4.77
Front coverage: luts_plus_ffs 1228..3963 (HV reference 4000); accuracy_bits 12.6..19.9 (HV reference 12); data_width on the front 18..26 (registry 8..28).

Per family:
- unrolled_k: 10 evals, 0 feasible; max throughput seen 13.8 MSPS; best accuracy 11.59 bits
- pipelined: 111 evals, 86 feasible; max throughput seen 282 MSPS; best accuracy 19.88 bits; best feasible luts_plus_ffs=1988; feasible ranges: data_width 15..26, n_iter 16..28, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 119 evals, 82 feasible; max throughput seen 171 MSPS; best accuracy 18.45 bits; best feasible luts_plus_ffs=1228; feasible ranges: data_width 17..22, n_iter 14..27, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (100 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (15 front designs; box front_anchored)
- `pipelined` (60 evals): data_width=24..28, n_iter=18..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (9 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 279 feasible; hypervolume 1.863e+04 (+42.3%).

**No LLM call** (code's front-mapping round): Final round: 240/400 evals used, 168 feasible designs (152 unique), 24-design Pareto front, HV 1.309e+04 (+8.3%). The spec is satisfiable — all three constraints are met with margin by front designs (throughput best 282 vs >=32; max_abs_err best 1.03e-06 vs <=2.44e-04; sys_p99_batch_us best 0.158 vs <=0.44), so `infeasible` is not warranted. The selected design (min luts_plus_ffs) is pipelined_m [W=18 N=14 ag=1 fg=3 trunc m=4] at luts_plus_ffs=1228, accuracy_bits=12.6 (max_abs_err 1.57e-04 <= 2.44e-04), throughput 93.6 MSPS >= 32, and the front covers luts_plus_ffs 1228..3963 (HV ref 4000) with accuracy_bits 12.6..19.9 (HV ref 12), i.e. the useful part of both objective ranges is already mapped. Gains are diminishing and the round cap is reached; further exploration would only be spent on the iterative family, which the registry predicts is low-throughput and cannot improve the min-area corner already found. Stop and let the spec's selection rule take the min-luts_plus_ffs front point, subject to the L2 re-selection of the shortlist.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.863e+04 (gain this round: +42.3%).
Feasible designs: 279 of 400 evaluations (253 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 2% violate; best seen 282
- max_abs_err <= 0.000244141: 14% violate; best seen 1.68e-08 (2^-25.83)
- sys_p99_batch_us <= 0.44: 20% violate; best seen 0.158

Pareto front (feasible, 24 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1228, accuracy_bits=12.6, luts=923, ffs=305, throughput_msps=93.6, max_abs_err=0.000157 (2^-12.64), power_index=1.48
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1298, accuracy_bits=13.3, luts=994, ffs=305, throughput_msps=93.6, max_abs_err=0.000102 (2^-13.26), power_index=1.56
- pipelined_m [data_width=19 n_iter=16 angle_guard=4 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1415, accuracy_bits=14.1, luts=1096, ffs=319, throughput_msps=89.6, max_abs_err=5.68e-05 (2^-14.10), power_index=1.7
- pipelined_m [data_width=19 n_iter=16 angle_guard=4 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=1528, accuracy_bits=14.6, luts=1191, ffs=337, throughput_msps=89.6, max_abs_err=3.9e-05 (2^-14.64), power_index=1.84
- pipelined_m [data_width=19 n_iter=17 angle_guard=4 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=1683, accuracy_bits=15.3, luts=1270, ffs=414, throughput_msps=89.6, max_abs_err=2.49e-05 (2^-15.29), power_index=2.03
- pipelined_m [data_width=21 n_iter=18 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1817, accuracy_bits=16.5, luts=1393, ffs=424, throughput_msps=89.6, max_abs_err=1.11e-05 (2^-16.46), power_index=2.19
- pipelined_m [data_width=21 n_iter=21 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=2131, accuracy_bits=17.5, luts=1630, ffs=500, throughput_msps=89.6, max_abs_err=5.47e-06 (2^-17.48), power_index=2.56
- pipelined_m [data_width=24 n_iter=23 angle_guard=3 frac_guard=3 rounding=round m=3] luts_plus_ffs=2827, accuracy_bits=20.9, luts=2073, ffs=755, throughput_msps=110, max_abs_err=5.25e-07 (2^-20.86), power_index=3.4
- pipelined_m [data_width=28 n_iter=28 angle_guard=3 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=3731, accuracy_bits=23.3, luts=2708, ffs=1023, throughput_msps=106, max_abs_err=1e-07 (2^-23.25), power_index=4.49
- pipelined [data_width=28 n_iter=30 angle_guard=4 frac_guard=4 rounding=round] luts_plus_ffs=6285, accuracy_bits=25.8, luts=3181, ffs=3103, throughput_msps=242, max_abs_err=1.68e-08 (2^-25.83), power_index=7.56
Front coverage: luts_plus_ffs 1228..6285 (HV reference 4000); accuracy_bits 12.6..25.8 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- unrolled_k: 10 evals, 0 feasible; max throughput seen 13.8 MSPS; best accuracy 11.59 bits
- pipelined: 171 evals, 146 feasible; max throughput seen 282 MSPS; best accuracy 25.83 bits; best feasible luts_plus_ffs=1988; feasible ranges: data_width 15..28, n_iter 16..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 219 evals, 133 feasible; max throughput seen 171 MSPS; best accuracy 23.51 bits; best feasible luts_plus_ffs=1228; feasible ranges: data_width 17..28, n_iter 14..28, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 26811 in, 22293 out
- provider-reported cost: $0.0276
- full prompts and replies: `llm_trace.jsonl`

