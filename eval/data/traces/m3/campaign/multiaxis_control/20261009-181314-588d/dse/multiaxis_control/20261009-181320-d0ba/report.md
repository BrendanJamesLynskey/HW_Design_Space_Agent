# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 400 of 400 budgeted, over 5 round(s).  
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
`pipelined_m:data_width=19,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 1023 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 317 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.61 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 7.77e-05 (2^-13.65) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 10.2 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.55e-05 (2^-15.26) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.35 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.7 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 96.8 dBc, SNR 88.9 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=19,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=23,n_iter=15,angle_guard=2,frac_guard=0,rounding=trunc,m=4` | 0.4016 → 0.4126 | yes |
| `pipelined_m:data_width=23,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 0.4016 → 0.4126 | yes |
| `pipelined_m:data_width=21,n_iter=16,angle_guard=3,frac_guard=3,rounding=round,m=4` | 0.4016 → 0.4126 | yes |
| `pipelined_m:data_width=22,n_iter=16,angle_guard=1,frac_guard=3,rounding=round,m=4` | 0.4016 → 0.4126 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (24 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1023 | 317 | 93.6 | 6 | 1.61 | 7.77e-05 (2^-13.65) | 13.65 |
| 1 | `pipelined_m:data_width=23,n_iter=15,angle_guard=2,frac_guard=0,rounding=trunc,m=4` | 1141 | 361 | 89.6 | 6 | 1.81 | 6.27e-05 (2^-13.96) | 13.96 |
| 2 | `pipelined_m:data_width=23,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1200 | 373 | 89.6 | 6 | 1.89 | 6.14e-05 (2^-13.99) | 13.99 |
| 3 | `pipelined_m:data_width=21,n_iter=16,angle_guard=3,frac_guard=3,rounding=round,m=4` | 1282 | 357 | 89.6 | 6 | 1.97 | 3.21e-05 (2^-14.93) | 14.93 |
| 4 | `pipelined_m:data_width=22,n_iter=16,angle_guard=1,frac_guard=3,rounding=round,m=4` | 1300 | 363 | 89.6 | 6 | 2 | 3.19e-05 (2^-14.94) | 14.94 |
| 5 | `pipelined_m:data_width=22,n_iter=17,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 1253 | 421 | 89.6 | 7 | 2.01 | 2.15e-05 (2^-15.50) | 15.50 |
| 6 | `pipelined_m:data_width=22,n_iter=17,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 1270 | 426 | 89.6 | 7 | 2.04 | 1.91e-05 (2^-15.67) | 15.67 |
| 7 | `pipelined_m:data_width=22,n_iter=17,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1350 | 436 | 89.6 | 7 | 2.15 | 1.73e-05 (2^-15.82) | 15.82 |
| 8 | `pipelined_m:data_width=21,n_iter=19,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1409 | 419 | 89.6 | 7 | 2.2 | 1.33e-05 (2^-16.20) | 16.20 |
| 9 | `pipelined_m:data_width=24,n_iter=19,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1592 | 462 | 89.6 | 7 | 2.47 | 4.63e-06 (2^-17.72) | 17.72 |
| 10 | `pipelined_m:data_width=24,n_iter=21,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 1649 | 527 | 89.6 | 8 | 2.62 | 3.35e-06 (2^-18.19) | 18.19 |
| 11 | `pipelined_m:data_width=22,n_iter=21,angle_guard=3,frac_guard=1,rounding=round,m=4` | 1674 | 517 | 89.6 | 8 | 2.64 | 3.21e-06 (2^-18.25) | 18.25 |
| 12 | `pipelined_m:data_width=24,n_iter=20,angle_guard=4,frac_guard=2,rounding=trunc,m=4` | 1727 | 483 | 86.0 | 7 | 2.66 | 2.49e-06 (2^-18.61) | 18.61 |
| 13 | `pipelined_m:data_width=23,n_iter=21,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1712 | 539 | 89.6 | 8 | 2.71 | 2.39e-06 (2^-18.67) | 18.67 |
| 14 | `pipelined_m:data_width=25,n_iter=21,angle_guard=0,frac_guard=0,rounding=round,m=4` | 1712 | 547 | 89.6 | 8 | 2.72 | 1.99e-06 (2^-18.94) | 18.94 |
| 15 | `pipelined_m:data_width=23,n_iter=24,angle_guard=3,frac_guard=2,rounding=round,m=4` | 2041 | 547 | 89.6 | 8 | 3.12 | 1.19e-06 (2^-19.68) | 19.68 |
| 16 | `pipelined_m:data_width=25,n_iter=22,angle_guard=4,frac_guard=1,rounding=trunc,m=2` | 1930 | 1025 | 152.6 | 13 | 3.56 | 1e-06 (2^-19.93) | 19.93 |
| 17 | `pipelined_m:data_width=25,n_iter=22,angle_guard=3,frac_guard=2,rounding=trunc,m=2` | 1953 | 1034 | 152.6 | 13 | 3.6 | 8.19e-07 (2^-20.22) | 20.22 |
| 18 | `pipelined_m:data_width=26,n_iter=24,angle_guard=1,frac_guard=3,rounding=round,m=3` | 2266 | 791 | 110.0 | 10 | 3.68 | 3.38e-07 (2^-21.50) | 21.50 |
| 19 | `pipelined_m:data_width=26,n_iter=24,angle_guard=2,frac_guard=3,rounding=trunc,m=2` | 2235 | 1172 | 152.6 | 14 | 4.1 | 2.59e-07 (2^-21.88) | 21.88 |
| 20 | `pipelined_m:data_width=28,n_iter=24,angle_guard=1,frac_guard=1,rounding=trunc,m=2` | 2259 | 1193 | 152.6 | 14 | 4.15 | 2.18e-07 (2^-22.13) | 22.13 |
| 21 | `pipelined_m:data_width=28,n_iter=25,angle_guard=3,frac_guard=0,rounding=round,m=2` | 2357 | 1289 | 147.4 | 15 | 4.39 | 1.38e-07 (2^-22.79) | 22.79 |
| 22 | `pipelined_m:data_width=28,n_iter=25,angle_guard=3,frac_guard=1,rounding=trunc,m=2` | 2408 | 1314 | 147.4 | 15 | 4.48 | 1.3e-07 (2^-22.88) | 22.88 |
| 23 | `pipelined_m:data_width=27,n_iter=28,angle_guard=4,frac_guard=3,rounding=trunc,m=2` | 2765 | 1433 | 147.4 | 16 | 5.05 | 7.43e-08 (2^-23.68) | 23.68 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The system constraint (32 results within 0.44 us of a 1 us tick) demands II=1 throughput with short latency, so pipelined and pipelined_m get the bulk of the budget; unrolled_k with large k is a cheaper-datapath alternative worth probing, and iterative is kept as a low-area anchor to confirm it is infeasible and to fill the front. Accuracy needs accuracy_bits>=12, so widths 14-22 and N 10-20 bracket the smallest design that clears 2^-12; guards and rounding are swept to find cheap accuracy gains. Budget is weighted toward the II=1 families where the real area/latency trade-off lives.*)
- `pipelined` (34 evals): data_width=14..22, n_iter=10..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* II=1 with N+2 latency; the only family that can plausibly deliver 32 results within 0.44 us at 1 result/cycle while keeping area low. Sweep width/iterations to find the smallest design that still hits accuracy_bits>=12.
- `pipelined_m` (33 evals): data_width=14..22, n_iter=10..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* Same II=1 throughput as pipelined but fewer registers (lower FF cost) at the price of longer latency; m trades area vs latency, so it may dominate pipelined on luts_plus_ffs if latency stays under the batch budget.
- `unrolled_k` (22 evals): data_width=14..22, n_iter=10..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, k=4..8. *Why:* High k gives near-II=1 throughput with a shared datapath (fewer FFs than full pipelining); worth probing whether ceil(N/k)+3 cycles still fits the 0.44 us batch window and whether it beats pipelined on area.
- `iterative` (11 evals): data_width=14..22, n_iter=10..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* Smallest area but N+3 cycles/result cannot meet 32 Msps or the 0.44 us batch latency; included only to confirm infeasibility and to anchor the low-area end of the Pareto front for hypervolume coverage.

**Result (code):** 100 evaluations this round, 100 total; 45 feasible; hypervolume 1.16e+04 (n/a).

**LLM decision:** `refine` — Round 1: 45/100 feasible, HV 1.16e4. Feasibility splits cleanly by family -- iterative (max 14.6 MSPS) and unrolled_k (max 12 MSPS) all fail throughput_msps >= 32, while pipelined_m (18/33 feasible, cheapest luts_plus_ffs 1364) and pipelined (27/34 feasible, up to 273 MSPS) carry the front. The front's cheapest point (1364, acc 12.9) and its best-accuracy point (2318, acc 17.0) are both pipelined_m. Two gaps remain that the registry can fill: accuracy only reaches 17 bits while n_iter/data_width were probed only to 20/22, and the m=4 samples that sit at 89.6 MSPS leave little headroom under sys_p99_batch_us (>= 0.36 us of servicing for one 32-request tick against 0.44 us) with no m=3 points on the front to fall back on. Refining pipelined_m over n_iter 12..24, data_width 18..26, angle_guard 0..4, frac_guard 0..4, m 2..4 (plus a smaller pipelined slice at the high-throughput end) should push the top of the curve past 17 bits under the 4000-lut reference and firm up the system-margin side of the front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 1.16e+04 (gain this round: n/a (first round)).
Feasible designs: 45 of 100 evaluations (39 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 33% violate; best seen 273
- max_abs_err <= 0.000244141: 32% violate; best seen 7.33e-06 (2^-17.06)
- sys_p99_batch_us <= 0.44: 40% violate; best seen 0.154

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=22 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1364, accuracy_bits=12.9, luts=1019, ffs=345, throughput_msps=89.6, max_abs_err=0.000126 (2^-12.95), power_index=1.64
- pipelined_m [data_width=22 n_iter=14 angle_guard=3 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1484, accuracy_bits=13, luts=1115, ffs=369, throughput_msps=89.6, max_abs_err=0.000123 (2^-12.99), power_index=1.79
- pipelined_m [data_width=22 n_iter=15 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1526, accuracy_bits=13.9, luts=1173, ffs=353, throughput_msps=89.6, max_abs_err=6.41e-05 (2^-13.93), power_index=1.84
- pipelined_m [data_width=22 n_iter=16 angle_guard=1 frac_guard=3 rounding=round m=4] luts_plus_ffs=1664, accuracy_bits=14.9, luts=1300, ffs=363, throughput_msps=89.6, max_abs_err=3.19e-05 (2^-14.94), power_index=2
- pipelined_m [data_width=22 n_iter=17 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1674, accuracy_bits=15.5, luts=1253, ffs=421, throughput_msps=89.6, max_abs_err=2.15e-05 (2^-15.50), power_index=2.01
- pipelined_m [data_width=22 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1696, accuracy_bits=15.7, luts=1270, ffs=426, throughput_msps=89.6, max_abs_err=1.91e-05 (2^-15.67), power_index=2.04
- pipelined_m [data_width=22 n_iter=17 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1786, accuracy_bits=15.8, luts=1350, ffs=436, throughput_msps=89.6, max_abs_err=1.73e-05 (2^-15.82), power_index=2.15
- pipelined_m [data_width=21 n_iter=19 angle_guard=3 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1828, accuracy_bits=16.2, luts=1409, ffs=419, throughput_msps=89.6, max_abs_err=1.33e-05 (2^-16.20), power_index=2.2
- pipelined_m [data_width=22 n_iter=18 angle_guard=1 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=2185, accuracy_bits=16.6, luts=1420, ffs=765, throughput_msps=158, max_abs_err=1.04e-05 (2^-16.56), power_index=2.63
- pipelined_m [data_width=21 n_iter=19 angle_guard=3 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=2318, accuracy_bits=17, luts=1485, ffs=833, throughput_msps=158, max_abs_err=7.43e-06 (2^-17.04), power_index=2.79
Front coverage: luts_plus_ffs 1364..2318 (HV reference 4000); accuracy_bits 12.9..17 (HV reference 12); data_width on the front 21..22 (registry 8..28).

Per family:
- iterative: 11 evals, 0 feasible; max throughput seen 14.6 MSPS; best accuracy 16.89 bits
- unrolled_k: 22 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 17.06 bits
- pipelined: 34 evals, 27 feasible; max throughput seen 273 MSPS; best accuracy 16.10 bits; best feasible luts_plus_ffs=1816; feasible ranges: data_width 17..21, n_iter 14..20, angle_guard 0..3, frac_guard 0..3
- pipelined_m: 33 evals, 18 feasible; max throughput seen 164 MSPS; best accuracy 17.04 bits; best feasible luts_plus_ffs=1364; feasible ranges: data_width 16..22, n_iter 14..20, angle_guard 0..3, frac_guard 0..3, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *All four families are already explored; iterative (11 evals, 0 feasible, max 14.6 MSPS) and unrolled_k (22 evals, 0 feasible, max 12 MSPS) cannot clear throughput_msps >= 32, so the feasible set is exactly pipelined + pipelined_m and no new family is worth adding. The front is 8/10 pipelined_m, so budget belongs there. Hypervolume is dominated by the strip luts_plus_ffs 2318..4000 at the max accuracy 17.0 (about 8.4k of the 1.16e4 total, by the given ref point 4000 / 12); that strip is set by the single highest-accuracy point, and round 1 capped at n_iter 20 / dw 22 while the registry allows 30 / 28, so the biggest HV lever is a higher-accuracy point still under luts 4000 -- hence extending n_iter/dw upward while keeping the low-area corner (acc 12.9, luts 1364) in range. Separately, the cheapest front designs are m=4 at throughput_msps 89.6: 32 tick requests cost >= 32/89.6 = 0.36 us of pure servicing against the 0.44 us sys_p99_batch bound before any latency/queueing, which is exactly the thin-margin case the spec warns can be lost at L2, and the front currently contains no m=3 design -- so m=3 is added to buy system margin at intermediate cost. Do not stop: the front's accuracy span (12.9..17) is well inside what the registry can still produce.*)
- `pipelined_m` (75 evals): data_width=18..26, n_iter=12..24, angle_guard=0..4, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* 6 of the 10 front designs are here and it owns both the cheapest point (luts_plus_ffs 1364 @ dw22/n14/ag0/fg1/trunc/m4) and the unique highest-accuracy point (2318 @ acc 17.0). Round 1 only reached n_iter<=20, dw<=22; broaden n_iter upward and dw both ways around the front's 21..22, and add m=3 (front has m=4 and m=2 only).
- `pipelined` (25 evals): data_width=16..24, n_iter=12..22, angle_guard=0..4, frac_guard=0..3, rounding=trunc|round. *Why:* Only family reaching 273 MSPS (best feasible luts_plus_ffs 1816, 27/34 evals feasible); keep it seeded as the high-throughput / low-sys-batch-risk end of the curve since the goal asks for whole-curve coverage, not just the min-area corner.

**Result (code):** 100 evaluations this round, 200 total; 128 feasible; hypervolume 1.84e+04 (+58.6%).

**LLM decision:** `map_front` — The feasible front is entirely pipelined_m (16 designs) and spans luts_plus_ffs 1340..3407 against the HV ref 4000 and accuracy_bits 13.7..21.9 against the ref 12, so both extremes are unmapped: the 12..13.7-bit corner (exactly where the min-luts_plus_ffs selection rule operates, since the cheapest design is 1340 at 13.7 bits) and the 3407..4000 area tail. The other families are dominated — iterative and unrolled_k have 0 feasible designs (max throughput 14.6/12 MSPS, below the 32 MSPS constraint) and pipelined's best feasible luts_plus_ffs is 1816 vs pipelined_m's 1340 — so the front is single-family and only pipelined_m needs coverage. With 200 of 400 evals left, this is the right point to spend the reserved budget on an NSGA-II coverage search over the full pipelined_m ranges (data_width 8..28, n_iter 4..30, angle_guard -2..4, frac_guard 0..4, m 2..8, both roundings) seeded with the current front, to fill the low-area/low-accuracy corner and extend the high-accuracy tail before the final round.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.84e+04 (gain this round: +58.6%).
Feasible designs: 128 of 200 evaluations (113 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 16% violate; best seen 273
- max_abs_err <= 0.000244141: 22% violate; best seen 2.59e-07 (2^-21.88)
- sys_p99_batch_us <= 0.44: 22% violate; best seen 0.154

Pareto front (feasible, 16 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1340, accuracy_bits=13.7, luts=1023, ffs=317, throughput_msps=93.6, max_abs_err=7.77e-05 (2^-13.65), power_index=1.61
- pipelined_m [data_width=23 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1574, accuracy_bits=14, luts=1200, ffs=373, throughput_msps=89.6, max_abs_err=6.14e-05 (2^-13.99), power_index=1.89
- pipelined_m [data_width=22 n_iter=16 angle_guard=1 frac_guard=3 rounding=round m=4] luts_plus_ffs=1664, accuracy_bits=14.9, luts=1300, ffs=363, throughput_msps=89.6, max_abs_err=3.19e-05 (2^-14.94), power_index=2
- pipelined_m [data_width=22 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1696, accuracy_bits=15.7, luts=1270, ffs=426, throughput_msps=89.6, max_abs_err=1.91e-05 (2^-15.67), power_index=2.04
- pipelined_m [data_width=21 n_iter=19 angle_guard=3 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1828, accuracy_bits=16.2, luts=1409, ffs=419, throughput_msps=89.6, max_abs_err=1.33e-05 (2^-16.20), power_index=2.2
- pipelined_m [data_width=24 n_iter=19 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=2054, accuracy_bits=17.7, luts=1592, ffs=462, throughput_msps=89.6, max_abs_err=4.63e-06 (2^-17.72), power_index=2.47
- pipelined_m [data_width=24 n_iter=20 angle_guard=4 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=2210, accuracy_bits=18.6, luts=1727, ffs=483, throughput_msps=86, max_abs_err=2.49e-06 (2^-18.61), power_index=2.66
- pipelined_m [data_width=25 n_iter=21 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=2259, accuracy_bits=18.9, luts=1712, ffs=547, throughput_msps=89.6, max_abs_err=1.99e-06 (2^-18.94), power_index=2.72
- pipelined_m [data_width=23 n_iter=24 angle_guard=3 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=2596, accuracy_bits=19.6, luts=2041, ffs=555, throughput_msps=89.6, max_abs_err=1.25e-06 (2^-19.61), power_index=3.12
- pipelined_m [data_width=26 n_iter=24 angle_guard=2 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=3407, accuracy_bits=21.9, luts=2235, ffs=1172, throughput_msps=153, max_abs_err=2.59e-07 (2^-21.88), power_index=4.1
Front coverage: luts_plus_ffs 1340..3407 (HV reference 4000); accuracy_bits 13.7..21.9 (HV reference 12); data_width on the front 19..26 (registry 8..28).

Per family:
- iterative: 11 evals, 0 feasible; max throughput seen 14.6 MSPS; best accuracy 16.89 bits
- unrolled_k: 22 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 17.06 bits
- pipelined: 59 evals, 43 feasible; max throughput seen 273 MSPS; best accuracy 18.54 bits; best feasible luts_plus_ffs=1816; feasible ranges: data_width 16..24, n_iter 14..21, angle_guard 0..4, frac_guard 0..3
- pipelined_m: 108 evals, 85 feasible; max throughput seen 164 MSPS; best accuracy 21.88 bits; best feasible luts_plus_ffs=1340; feasible ranges: data_width 16..26, n_iter 13..24, angle_guard 0..4, frac_guard 0..4, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=18..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (16 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 240 total; 157 feasible; hypervolume 1.847e+04 (+0.4%).

**LLM decision:** `map_front` — Three of four rounds are done and this round's HV gain was only +0.4% (1.847e+04), so refinement is in diminishing-returns territory. The evidence shows the feasible set is confined to two families — pipelined (43/59 feasible) and pipelined_m (114/148 feasible) — while iterative (0/11) and unrolled_k (0/22) are structurally infeasible because their best throughputs (14.6 and 12 MSPS) fall far short of the 32 MSPS floor. The Pareto front is therefore a pipelined / pipelined_m front, and it leaves clear objective headroom that a final mapping pass can cover: luts_plus_ffs spans 1340..4198 (HV ref 4000, best design already at 1340), accuracy_bits spans 13.7..23.7 while the registry and the family's observed best reach higher (data_width on front only 19..27 of 8..28; pipelined_m best accuracy 23.68 vs 28-bit capability). With the reserved final-round budget (160 evals remaining) the right move is to spend it mapping the whole front over the full ranges of pipelined and pipelined_m, seeded with the current 20-design front, so the HV covers the high-accuracy tail and any cheaper low-area designs; the L2 system screen (sys_p99_batch_us <= 0.44) can then re-select from a fully mapped front using the min-luts_plus_ffs rule without risking a thin corner.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 1.847e+04 (gain this round: +0.4%).
Feasible designs: 157 of 240 evaluations (135 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 14% violate; best seen 273
- max_abs_err <= 0.000244141: 19% violate; best seen 7.43e-08 (2^-23.68)
- sys_p99_batch_us <= 0.44: 23% violate; best seen 0.154

Pareto front (feasible, 20 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1340, accuracy_bits=13.7, luts=1023, ffs=317, throughput_msps=93.6, max_abs_err=7.77e-05 (2^-13.65), power_index=1.61
- pipelined_m [data_width=23 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1574, accuracy_bits=14, luts=1200, ffs=373, throughput_msps=89.6, max_abs_err=6.14e-05 (2^-13.99), power_index=1.89
- pipelined_m [data_width=22 n_iter=16 angle_guard=1 frac_guard=3 rounding=round m=4] luts_plus_ffs=1664, accuracy_bits=14.9, luts=1300, ffs=363, throughput_msps=89.6, max_abs_err=3.19e-05 (2^-14.94), power_index=2
- pipelined_m [data_width=22 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1696, accuracy_bits=15.7, luts=1270, ffs=426, throughput_msps=89.6, max_abs_err=1.91e-05 (2^-15.67), power_index=2.04
- pipelined_m [data_width=21 n_iter=19 angle_guard=3 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1828, accuracy_bits=16.2, luts=1409, ffs=419, throughput_msps=89.6, max_abs_err=1.33e-05 (2^-16.20), power_index=2.2
- pipelined_m [data_width=24 n_iter=20 angle_guard=4 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=2210, accuracy_bits=18.6, luts=1727, ffs=483, throughput_msps=86, max_abs_err=2.49e-06 (2^-18.61), power_index=2.66
- pipelined_m [data_width=25 n_iter=21 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=2259, accuracy_bits=18.9, luts=1712, ffs=547, throughput_msps=89.6, max_abs_err=1.99e-06 (2^-18.94), power_index=2.72
- pipelined_m [data_width=25 n_iter=22 angle_guard=4 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=2956, accuracy_bits=19.9, luts=1930, ffs=1025, throughput_msps=153, max_abs_err=1e-06 (2^-19.93), power_index=3.56
- pipelined_m [data_width=26 n_iter=24 angle_guard=1 frac_guard=3 rounding=round m=3] luts_plus_ffs=3057, accuracy_bits=21.5, luts=2266, ffs=791, throughput_msps=110, max_abs_err=3.38e-07 (2^-21.50), power_index=3.68
- pipelined_m [data_width=27 n_iter=28 angle_guard=4 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=4198, accuracy_bits=23.7, luts=2765, ffs=1433, throughput_msps=147, max_abs_err=7.43e-08 (2^-23.68), power_index=5.05
Front coverage: luts_plus_ffs 1340..4198 (HV reference 4000); accuracy_bits 13.7..23.7 (HV reference 12); data_width on the front 19..27 (registry 8..28).

Per family:
- iterative: 11 evals, 0 feasible; max throughput seen 14.6 MSPS; best accuracy 16.89 bits
- unrolled_k: 22 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 17.06 bits
- pipelined: 59 evals, 43 feasible; max throughput seen 273 MSPS; best accuracy 18.54 bits; best feasible luts_plus_ffs=1816; feasible ranges: data_width 16..24, n_iter 14..21, angle_guard 0..4, frac_guard 0..3
- pipelined_m: 148 evals, 114 feasible; max throughput seen 164 MSPS; best accuracy 23.68 bits; best feasible luts_plus_ffs=1340; feasible ranges: data_width 16..27, n_iter 13..29, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=18..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (20 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 340 total; 224 feasible; hypervolume 1.89e+04 (+2.3%).

**LLM decision:** `stop` — Final round: the front is feasible and well covered, so `stop` (not `infeasible`). Evidence: 224/340 evaluations are feasible, and every constraint is met by a wide margin — throughput best 273 MSPS vs >=32 (only 10% violate), max_abs_err best 2^-24.80 vs <=0.000244141 (2^-12), sys_p99_batch_us best 0.154 us vs <=0.44 (nearly 3x headroom, so the L1->L2 re-selection risk is small). The Pareto front has 24 designs spanning luts_plus_ffs 1340..4198 (HV ref 4000) and accuracy_bits 13.7..23.7 (HV ref 12), i.e. it exceeds both HV references and hypervolume is still gaining (+2.3% this round). All four families have been explored; iterative and unrolled_k produced 0 feasible designs (max throughput 14.6 and 12 MSPS, below 32), while pipelined (43 feasible, best area 1816) and pipelined_m (181 feasible, best area 1340) carry the front. The selection rule (min luts_plus_ffs) would pick the pipelined_m [data_width=19 n_iter=15 angle_guard=2 frac_guard=2 trunc m=4] point at 1340 LUT+FF, 13.7 accuracy bits, 93.6 MSPS — comfortably satisfying all constraints.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 60 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 340 of 400.
Hypervolume of the feasible front: 1.89e+04 (gain this round: +2.3%).
Feasible designs: 224 of 340 evaluations (191 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 10% violate; best seen 273
- max_abs_err <= 0.000244141: 14% violate; best seen 3.42e-08 (2^-24.80)
- sys_p99_batch_us <= 0.44: 26% violate; best seen 0.154

Pareto front (feasible, 24 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1340, accuracy_bits=13.7, luts=1023, ffs=317, throughput_msps=93.6, max_abs_err=7.77e-05 (2^-13.65), power_index=1.61
- pipelined_m [data_width=21 n_iter=16 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1640, accuracy_bits=14.9, luts=1282, ffs=357, throughput_msps=89.6, max_abs_err=3.21e-05 (2^-14.93), power_index=1.97
- pipelined_m [data_width=22 n_iter=17 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1674, accuracy_bits=15.5, luts=1253, ffs=421, throughput_msps=89.6, max_abs_err=2.15e-05 (2^-15.50), power_index=2.01
- pipelined_m [data_width=21 n_iter=19 angle_guard=3 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1828, accuracy_bits=16.2, luts=1409, ffs=419, throughput_msps=89.6, max_abs_err=1.33e-05 (2^-16.20), power_index=2.2
- pipelined_m [data_width=24 n_iter=21 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=2176, accuracy_bits=18.2, luts=1649, ffs=527, throughput_msps=89.6, max_abs_err=3.35e-06 (2^-18.19), power_index=2.62
- pipelined_m [data_width=23 n_iter=21 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=2251, accuracy_bits=18.7, luts=1712, ffs=539, throughput_msps=89.6, max_abs_err=2.39e-06 (2^-18.67), power_index=2.71
- pipelined_m [data_width=23 n_iter=24 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=2588, accuracy_bits=19.7, luts=2041, ffs=547, throughput_msps=89.6, max_abs_err=1.19e-06 (2^-19.68), power_index=3.12
- pipelined_m [data_width=26 n_iter=24 angle_guard=1 frac_guard=3 rounding=round m=3] luts_plus_ffs=3057, accuracy_bits=21.5, luts=2266, ffs=791, throughput_msps=110, max_abs_err=3.38e-07 (2^-21.50), power_index=3.68
- pipelined_m [data_width=28 n_iter=24 angle_guard=1 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=3452, accuracy_bits=22.1, luts=2259, ffs=1193, throughput_msps=153, max_abs_err=2.18e-07 (2^-22.13), power_index=4.15
- pipelined_m [data_width=27 n_iter=28 angle_guard=4 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=4198, accuracy_bits=23.7, luts=2765, ffs=1433, throughput_msps=147, max_abs_err=7.43e-08 (2^-23.68), power_index=5.05
Front coverage: luts_plus_ffs 1340..4198 (HV reference 4000); accuracy_bits 13.7..23.7 (HV reference 12); data_width on the front 19..28 (registry 8..28).

Per family:
- iterative: 11 evals, 0 feasible; max throughput seen 14.6 MSPS; best accuracy 16.89 bits
- unrolled_k: 22 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 17.06 bits
- pipelined: 59 evals, 43 feasible; max throughput seen 273 MSPS; best accuracy 18.54 bits; best feasible luts_plus_ffs=1816; feasible ranges: data_width 16..24, n_iter 14..21, angle_guard 0..4, frac_guard 0..3
- pipelined_m: 248 evals, 181 feasible; max throughput seen 171 MSPS; best accuracy 24.80 bits; best feasible luts_plus_ffs=1340; feasible ranges: data_width 16..28, n_iter 13..29, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 5

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 60 evaluations*)
- `pipelined_m` (60 evals): data_width=18..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (24 front designs; box front_anchored)

**Result (code):** 60 evaluations this round, 400 total; 258 feasible; hypervolume 1.89e+04 (+0.0%).

**No LLM call** (code's front-mapping round): Final round: the front is feasible and well covered, so `stop` (not `infeasible`). Evidence: 224/340 evaluations are feasible, and every constraint is met by a wide margin — throughput best 273 MSPS vs >=32 (only 10% violate), max_abs_err best 2^-24.80 vs <=0.000244141 (2^-12), sys_p99_batch_us best 0.154 us vs <=0.44 (nearly 3x headroom, so the L1->L2 re-selection risk is small). The Pareto front has 24 designs spanning luts_plus_ffs 1340..4198 (HV ref 4000) and accuracy_bits 13.7..23.7 (HV ref 12), i.e. it exceeds both HV references and hypervolume is still gaining (+2.3% this round). All four families have been explored; iterative and unrolled_k produced 0 feasible designs (max throughput 14.6 and 12 MSPS, below 32), while pipelined (43 feasible, best area 1816) and pipelined_m (181 feasible, best area 1340) carry the front. The selection rule (min luts_plus_ffs) would pick the pipelined_m [data_width=19 n_iter=15 angle_guard=2 frac_guard=2 trunc m=4] point at 1340 LUT+FF, 13.7 accuracy bits, 93.6 MSPS — comfortably satisfying all constraints.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 5 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.89e+04 (gain this round: +0.0%).
Feasible designs: 258 of 400 evaluations (223 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 8% violate; best seen 273
- max_abs_err <= 0.000244141: 13% violate; best seen 3.42e-08 (2^-24.80)
- sys_p99_batch_us <= 0.44: 28% violate; best seen 0.154

Pareto front (feasible, 24 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1340, accuracy_bits=13.7, luts=1023, ffs=317, throughput_msps=93.6, max_abs_err=7.77e-05 (2^-13.65), power_index=1.61
- pipelined_m [data_width=21 n_iter=16 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1640, accuracy_bits=14.9, luts=1282, ffs=357, throughput_msps=89.6, max_abs_err=3.21e-05 (2^-14.93), power_index=1.97
- pipelined_m [data_width=22 n_iter=17 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1674, accuracy_bits=15.5, luts=1253, ffs=421, throughput_msps=89.6, max_abs_err=2.15e-05 (2^-15.50), power_index=2.01
- pipelined_m [data_width=21 n_iter=19 angle_guard=3 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1828, accuracy_bits=16.2, luts=1409, ffs=419, throughput_msps=89.6, max_abs_err=1.33e-05 (2^-16.20), power_index=2.2
- pipelined_m [data_width=24 n_iter=21 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=2176, accuracy_bits=18.2, luts=1649, ffs=527, throughput_msps=89.6, max_abs_err=3.35e-06 (2^-18.19), power_index=2.62
- pipelined_m [data_width=23 n_iter=21 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=2251, accuracy_bits=18.7, luts=1712, ffs=539, throughput_msps=89.6, max_abs_err=2.39e-06 (2^-18.67), power_index=2.71
- pipelined_m [data_width=23 n_iter=24 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=2588, accuracy_bits=19.7, luts=2041, ffs=547, throughput_msps=89.6, max_abs_err=1.19e-06 (2^-19.68), power_index=3.12
- pipelined_m [data_width=26 n_iter=24 angle_guard=1 frac_guard=3 rounding=round m=3] luts_plus_ffs=3057, accuracy_bits=21.5, luts=2266, ffs=791, throughput_msps=110, max_abs_err=3.38e-07 (2^-21.50), power_index=3.68
- pipelined_m [data_width=28 n_iter=24 angle_guard=1 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=3452, accuracy_bits=22.1, luts=2259, ffs=1193, throughput_msps=153, max_abs_err=2.18e-07 (2^-22.13), power_index=4.15
- pipelined_m [data_width=27 n_iter=28 angle_guard=4 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=4198, accuracy_bits=23.7, luts=2765, ffs=1433, throughput_msps=147, max_abs_err=7.43e-08 (2^-23.68), power_index=5.05
Front coverage: luts_plus_ffs 1340..4198 (HV reference 4000); accuracy_bits 13.7..23.7 (HV reference 12); data_width on the front 19..28 (registry 8..28).

Per family:
- iterative: 11 evals, 0 feasible; max throughput seen 14.6 MSPS; best accuracy 16.89 bits
- unrolled_k: 22 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 17.06 bits
- pipelined: 59 evals, 43 feasible; max throughput seen 273 MSPS; best accuracy 18.54 bits; best feasible luts_plus_ffs=1816; feasible ranges: data_width 16..24, n_iter 14..21, angle_guard 0..4, frac_guard 0..3
- pipelined_m: 308 evals, 215 feasible; max throughput seen 171 MSPS; best accuracy 24.80 bits; best feasible luts_plus_ffs=1340; feasible ranges: data_width 16..28, n_iter 13..29, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 31406 in, 17650 out
- provider-reported cost: $0.0177
- full prompts and replies: `llm_trace.jsonl`

