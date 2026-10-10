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
`pipelined_m:data_width=17,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 906 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 268 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 61.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.41 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000244 (2^-12.00) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 7.98 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.38e-05 (2^-14.18) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.76 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 95.7 dBc, SNR 83.5 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=17,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=17,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=3,frac_guard=1,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=16,n_iter=15,angle_guard=3,frac_guard=3,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=4,frac_guard=3,rounding=round,m=4` | 0.3848 → 0.3953 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (25 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,m=4` | 906 | 268 | 97.8 | 6 | 1.41 | 0.000244 (2^-12.00) | 12.00 |
| 1 | `pipelined_m:data_width=17,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 938 | 274 | 97.8 | 6 | 1.46 | 0.000222 (2^-12.13) | 12.13 |
| 2 | `pipelined_m:data_width=17,n_iter=15,angle_guard=3,frac_guard=1,rounding=round,m=4` | 956 | 289 | 93.6 | 6 | 1.5 | 0.000124 (2^-12.98) | 12.98 |
| 3 | `pipelined_m:data_width=16,n_iter=15,angle_guard=3,frac_guard=3,rounding=round,m=4` | 968 | 287 | 93.6 | 6 | 1.51 | 0.000117 (2^-13.06) | 13.06 |
| 4 | `pipelined_m:data_width=17,n_iter=15,angle_guard=4,frac_guard=3,rounding=round,m=4` | 1030 | 305 | 93.6 | 6 | 1.61 | 8.45e-05 (2^-13.53) | 13.53 |
| 5 | `pipelined_m:data_width=17,n_iter=16,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1053 | 295 | 93.6 | 6 | 1.62 | 6.9e-05 (2^-13.82) | 13.82 |
| 6 | `pipelined_m:data_width=19,n_iter=17,angle_guard=0,frac_guard=1,rounding=trunc,m=3` | 1101 | 436 | 119.3 | 8 | 1.85 | 6.22e-05 (2^-13.97) | 13.97 |
| 7 | `pipelined_m:data_width=18,n_iter=16,angle_guard=3,frac_guard=3,rounding=round,m=3` | 1134 | 456 | 119.3 | 8 | 1.91 | 4.52e-05 (2^-14.43) | 14.43 |
| 8 | `pipelined_m:data_width=20,n_iter=17,angle_guard=1,frac_guard=1,rounding=round,m=3` | 1211 | 464 | 119.3 | 8 | 2.02 | 2.58e-05 (2^-15.24) | 15.24 |
| 9 | `pipelined_m:data_width=20,n_iter=17,angle_guard=4,frac_guard=2,rounding=round,m=4` | 1295 | 417 | 89.6 | 7 | 2.06 | 2.01e-05 (2^-15.61) | 15.61 |
| 10 | `pipelined_m:data_width=19,n_iter=20,angle_guard=3,frac_guard=3,rounding=round,m=4` | 1487 | 403 | 93.6 | 7 | 2.27 | 1.3e-05 (2^-16.24) | 16.24 |
| 11 | `pipelined_m:data_width=20,n_iter=18,angle_guard=4,frac_guard=4,rounding=round,m=3` | 1445 | 513 | 114.5 | 8 | 2.36 | 1.06e-05 (2^-16.52) | 16.52 |
| 12 | `pipelined_m:data_width=27,n_iter=19,angle_guard=1,frac_guard=0,rounding=trunc,m=3` | 1674 | 683 | 110.0 | 9 | 2.84 | 3.98e-06 (2^-17.94) | 17.94 |
| 13 | `pipelined_m:data_width=27,n_iter=19,angle_guard=0,frac_guard=1,rounding=trunc,m=3` | 1693 | 688 | 110.0 | 9 | 2.87 | 3.97e-06 (2^-17.94) | 17.94 |
| 14 | `pipelined_m:data_width=27,n_iter=19,angle_guard=1,frac_guard=1,rounding=round,m=3` | 1769 | 697 | 110.0 | 9 | 2.97 | 3.88e-06 (2^-17.98) | 17.98 |
| 15 | `pipelined_m:data_width=28,n_iter=19,angle_guard=0,frac_guard=1,rounding=round,m=3` | 1809 | 713 | 110.0 | 9 | 3.04 | 3.87e-06 (2^-17.98) | 17.98 |
| 16 | `pipelined_m:data_width=27,n_iter=21,angle_guard=0,frac_guard=2,rounding=trunc,m=3` | 1923 | 700 | 110.0 | 9 | 3.16 | 1.1e-06 (2^-19.79) | 19.79 |
| 17 | `pipelined_m:data_width=26,n_iter=22,angle_guard=3,frac_guard=0,rounding=round,m=3` | 1930 | 763 | 110.0 | 10 | 3.24 | 6.69e-07 (2^-20.51) | 20.51 |
| 18 | `pipelined_m:data_width=27,n_iter=24,angle_guard=0,frac_guard=0,rounding=trunc,m=3` | 2114 | 765 | 110.0 | 10 | 3.46 | 4.67e-07 (2^-21.03) | 21.03 |
| 19 | `pipelined_m:data_width=27,n_iter=25,angle_guard=0,frac_guard=1,rounding=round,m=3` | 2313 | 872 | 110.0 | 11 | 3.83 | 2.97e-07 (2^-21.68) | 21.68 |
| 20 | `pipelined_m:data_width=27,n_iter=25,angle_guard=2,frac_guard=1,rounding=trunc,m=3` | 2307 | 888 | 110.0 | 11 | 3.85 | 2.59e-07 (2^-21.88) | 21.88 |
| 21 | `pipelined_m:data_width=27,n_iter=25,angle_guard=1,frac_guard=1,rounding=round,m=3` | 2338 | 881 | 110.0 | 11 | 3.87 | 2.06e-07 (2^-22.21) | 22.21 |
| 22 | `pipelined_m:data_width=27,n_iter=25,angle_guard=4,frac_guard=2,rounding=trunc,m=3` | 2408 | 922 | 105.9 | 11 | 4.01 | 1.45e-07 (2^-22.72) | 22.72 |
| 23 | `pipelined_m:data_width=27,n_iter=25,angle_guard=2,frac_guard=4,rounding=round,m=3` | 2515 | 938 | 105.9 | 11 | 4.16 | 1.1e-07 (2^-23.12) | 23.12 |
| 24 | `pipelined_m:data_width=28,n_iter=26,angle_guard=2,frac_guard=4,rounding=round,m=2` | 2699 | 1375 | 147.4 | 15 | 4.9 | 6.35e-08 (2^-23.91) | 23.91 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The system constraint is bursty: 32 requests arrive together every 1 us and all must finish within 0.44 us (p99 batch). The iterative family processes one result every N+3 cycles, so 32 results would take 32*(N+3) cycles; with the N>=12 needed for 2^-12 accuracy this implies a clock far beyond a realistic Artix-7 fabric, so iterative is very unlikely to be feasible and is skipped in round 1. The pipelined and pipelined_m families produce one result per cycle, so a 32-request burst can be absorbed in ~32+latency cycles, which is the natural way to meet the sub-microsecond batch deadline. unrolled_k is included because it can trade throughput for area and may still meet the burst deadline for large k. The data_width lower bound is 14 because the output LSB is 2^-(W-2) and max_abs_err <= 2^-12, so W=14 is the minimum width that can even represent the required accuracy; n_iter starts at 10 because CORDIC angle error scales with N and N>=12 is likely needed, but we allow 10..20 to let the search find the exact accuracy boundary. angle_guard and frac_guard are opened to their full useful ranges to let the search trade internal precision against area. Rounding is included because it can improve accuracy at little area cost. Budget is weighted toward pipelined_m because it directly targets the min luts_plus_ffs objective while still providing 1 result/cycle; pipelined anchors the high-Fmax end; unrolled_k covers the low-area alternative. Later rounds will refine around the Pareto front and use the reserved budget to map the front over the full ranges of the families that survive.*)
- `pipelined_m` (45 evals): data_width=14..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Produces 1 result/cycle, so a 32-request burst can be pipelined and drained in roughly 32+latency cycles, which is the most plausible way to meet the 0.44 us p99 batch deadline without needing an extreme clock. Registering every m stages reduces FF count versus fully pipelined, directly targeting the min luts_plus_ffs objective. m controls the area/Fmax trade-off, so it is the key parameter to map.
- `pipelined` (30 evals): data_width=14..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Fully pipelined gives 1 result/cycle and the shortest latency (N+2), so it is the reference for burst absorption and likely the highest Fmax. It may cost more FFs than pipelined_m, but it anchors the high-throughput end of the Pareto front and helps verify whether the system deadline is comfortably met.
- `unrolled_k` (25 evals): data_width=14..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* Shares the datapath across k micro-rotations per cycle, so it can be much smaller than a fully pipelined design while still achieving multiple results per cycle. For large k it may meet the 32 Msps average and the burst deadline if Fmax is high enough. It is the main low-area alternative to pipelined_m and should be explored to cover the area-optimised part of the front.

**Result (code):** 100 evaluations this round, 100 total; 31 feasible; hypervolume 1.002e+04 (n/a).

**LLM decision:** `map_front` — Round 1 leaves a feasible front of only 6 designs, all pipelined_m, spanning luts_plus_ffs 1298..1889 against an HV reference of 4000 — i.e. the area objective is mapped over only ~32-47% of its range, while accuracy_bits 12.7..16.2 already sits above the HV ref of 12. The two other feasible families are pipelined (best feasible luts_plus_ffs=1927, up to 273 MSPS) and pipelined_m; unrolled_k got 0 feasible with max throughput 9.44 MSPS, and iterative is strictly slower (1 micro-rotation/cycle, N+3 cycles/result), so it cannot reach the 32 MSPS constraint and is not worth budget. The system burst constraint (32 requests within 0.44 us) is currently met with margin (best sys_p99_batch_us 0.161 vs 0.44), so the front is not obviously at risk of being pruned at L2; the gap is coverage of the area axis, not feasibility. Per the guidance, when the front covers only a small part of an objective's range the right move is to let code map the whole front over the full ranges of the families found on it, seeded with the current front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 1.002e+04 (gain this round: n/a (first round)).
Feasible designs: 31 of 100 evaluations (24 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 25% violate; best seen 273
- max_abs_err <= 0.000244141: 62% violate; best seen 1.3e-05 (2^-16.24)
- sys_p99_batch_us <= 0.44: 38% violate; best seen 0.161

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=3 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=1298, accuracy_bits=12.7, luts=923, ffs=375, throughput_msps=119, max_abs_err=0.000151 (2^-12.69), power_index=1.56
- pipelined_m [data_width=17 n_iter=14 angle_guard=3 frac_guard=3 rounding=round m=3] luts_plus_ffs=1313, accuracy_bits=12.7, luts=945, ffs=368, throughput_msps=119, max_abs_err=0.000148 (2^-12.73), power_index=1.58
- pipelined_m [data_width=17 n_iter=16 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1347, accuracy_bits=13.8, luts=1053, ffs=295, throughput_msps=93.6, max_abs_err=6.9e-05 (2^-13.82), power_index=1.62
- pipelined_m [data_width=19 n_iter=20 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=1718, accuracy_bits=14.1, luts=1347, ffs=371, throughput_msps=93.6, max_abs_err=5.55e-05 (2^-14.14), power_index=2.07
- pipelined_m [data_width=18 n_iter=20 angle_guard=3 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=1859, accuracy_bits=14.2, luts=1347, ffs=513, throughput_msps=119, max_abs_err=5.33e-05 (2^-14.20), power_index=2.24
- pipelined_m [data_width=19 n_iter=20 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1889, accuracy_bits=16.2, luts=1487, ffs=403, throughput_msps=93.6, max_abs_err=1.3e-05 (2^-16.24), power_index=2.27
Front coverage: luts_plus_ffs 1298..1889 (HV reference 4000); accuracy_bits 12.7..16.2 (HV reference 12); data_width on the front 17..19 (registry 8..28).

Per family:
- unrolled_k: 25 evals, 0 feasible; max throughput seen 9.44 MSPS; best accuracy 12.42 bits
- pipelined: 30 evals, 10 feasible; max throughput seen 273 MSPS; best accuracy 14.97 bits; best feasible luts_plus_ffs=1927; feasible ranges: data_width 15..18, n_iter 15..17, angle_guard 3..3, frac_guard 0..3
- pipelined_m: 45 evals, 21 feasible; max throughput seen 164 MSPS; best accuracy 16.24 bits; best feasible luts_plus_ffs=1298; feasible ranges: data_width 17..20, n_iter 14..20, angle_guard -2..3, frac_guard 1..4, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (6 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 94 feasible; hypervolume 1.819e+04 (+81.6%).

**LLM decision:** `refine` — Round 2 gave a big HV jump (+81.6%) and the front is now well spread on both objectives (luts_plus_ffs 1298..3683 vs ref 4000; accuracy_bits 12.7..22.8 vs ref 12), so a full map_front is premature while 200 evals remain. The selection rule is min luts_plus_ffs, and the cheapest feasible design sits at the low-area corner (pipelined_m data_width=18/n_iter=14/m=3 -> 1298) right at the accuracy floor (12.7 bits vs the 2^-12 limit), so the highest-value move is to densify that corner to push luts_plus_ffs below 1298 and to fill the 12.7..14-bit band. pipelined_m carries 84 of 94 feasible designs and the whole front, so it gets the budget; pipelined (best feasible 1927) gets a small slice as the only other family that produced feasible designs. iterative is deliberately NOT added: it emits 1 result per N+3 cycles, so 32 back-to-back requests need 32*(N+3) cycles, which cannot fit the 0.44us batch bound at any Artix-7 clock (e.g. N=4 needs >500 MHz), and unrolled_k already returned 0 feasible in 25 evals (max 9.44 MSPS, far under the 32 MSPS floor).

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.819e+04 (gain this round: +81.6%).
Feasible designs: 94 of 200 evaluations (83 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 12% violate; best seen 273
- max_abs_err <= 0.000244141: 34% violate; best seen 4.18e-08 (2^-24.51)
- sys_p99_batch_us <= 0.44: 34% violate; best seen 0.161

Pareto front (feasible, 18 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=3 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=1298, accuracy_bits=12.7, luts=923, ffs=375, throughput_msps=119, max_abs_err=0.000151 (2^-12.69), power_index=1.56
- pipelined_m [data_width=17 n_iter=16 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1347, accuracy_bits=13.8, luts=1053, ffs=295, throughput_msps=93.6, max_abs_err=6.9e-05 (2^-13.82), power_index=1.62
- pipelined_m [data_width=19 n_iter=20 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=1718, accuracy_bits=14.1, luts=1347, ffs=371, throughput_msps=93.6, max_abs_err=5.55e-05 (2^-14.14), power_index=2.07
- pipelined_m [data_width=19 n_iter=20 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1889, accuracy_bits=16.2, luts=1487, ffs=403, throughput_msps=93.6, max_abs_err=1.3e-05 (2^-16.24), power_index=2.27
- pipelined_m [data_width=27 n_iter=19 angle_guard=0 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=2381, accuracy_bits=17.9, luts=1693, ffs=688, throughput_msps=110, max_abs_err=3.97e-06 (2^-17.94), power_index=2.87
- pipelined_m [data_width=27 n_iter=19 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=2466, accuracy_bits=18, luts=1769, ffs=697, throughput_msps=110, max_abs_err=3.88e-06 (2^-17.98), power_index=2.97
- pipelined_m [data_width=27 n_iter=21 angle_guard=0 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=2623, accuracy_bits=19.8, luts=1923, ffs=700, throughput_msps=110, max_abs_err=1.1e-06 (2^-19.79), power_index=3.16
- pipelined_m [data_width=27 n_iter=25 angle_guard=0 frac_guard=1 rounding=round m=3] luts_plus_ffs=3185, accuracy_bits=21.7, luts=2313, ffs=872, throughput_msps=110, max_abs_err=2.97e-07 (2^-21.68), power_index=3.83
- pipelined_m [data_width=27 n_iter=25 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=3219, accuracy_bits=22.2, luts=2338, ffs=881, throughput_msps=110, max_abs_err=2.06e-07 (2^-22.21), power_index=3.87
- pipelined_m [data_width=28 n_iter=25 angle_guard=2 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=3683, accuracy_bits=22.8, luts=2383, ffs=1301, throughput_msps=153, max_abs_err=1.41e-07 (2^-22.76), power_index=4.43
Front coverage: luts_plus_ffs 1298..3683 (HV reference 4000); accuracy_bits 12.7..22.8 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- unrolled_k: 25 evals, 0 feasible; max throughput seen 9.44 MSPS; best accuracy 12.42 bits
- pipelined: 30 evals, 10 feasible; max throughput seen 273 MSPS; best accuracy 14.97 bits; best feasible luts_plus_ffs=1927; feasible ranges: data_width 15..18, n_iter 15..17, angle_guard 3..3, frac_guard 0..3
- pipelined_m: 145 evals, 84 feasible; max throughput seen 164 MSPS; best accuracy 24.51 bits; best feasible luts_plus_ffs=1298; feasible ranges: data_width 17..28, n_iter 14..28, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *refine low-area corner of the front-carrying families; hold map_front for the final round once the corner is settled*)
- `pipelined_m` (75 evals): data_width=15..20, n_iter=13..20, angle_guard=0..4, frac_guard=0..3, rounding=trunc|round, m=2..5. *Why:* carries the entire feasible front; low-area corner (data_width 17-18, n_iter 14-16, m 3-4) is where min luts_plus_ffs is decided and sits at the accuracy floor
- `pipelined` (25 evals): data_width=14..19, n_iter=14..20, angle_guard=2..4, frac_guard=0..3, rounding=trunc|round. *Why:* only other family with feasible designs (10/30); feasible data_width 15..18 overlaps the low-area corner, worth checking whether it can beat 1298 luts_plus_ffs

**Result (code):** 100 evaluations this round, 300 total; 177 feasible; hypervolume 1.852e+04 (+1.8%).

**LLM decision:** `map_front` — Round 3 leaves 100 evals in one round, and the front is still only partially mapped. Evidence: (1) the front lives entirely on pipelined/pipelined_m — unrolled_k got 0 feasible in 25 evals (max 9.44 MSPS) and iterative is strictly slower (1 micro-rotation/cycle, N+3 cycles/result), so neither can reach the 32 MSPS throughput floor; adding iterative would burn budget on a family that cannot satisfy the constraints. (2) The front spans luts_plus_ffs 1175..3683 against an HV reference of 4000, and accuracy_bits 12..22.8 against a best-seen 24.51 — so the high-area/high-accuracy corner of the trade-off is unmapped, exactly the region that adds HV area near the reference point. (3) The cheapest design (pipelined_m, W=17 N=16 m=4, 1175 LUT+FF) sits exactly on the accuracy constraint (2^-12.00) and the spec warns that cheap designs only just passing the L1 sys_p99_batch bound can be lost at L2, so a denser front of robust cheap alternatives is valuable for the min-luts_plus_ffs selection rule. Spending the reserved budget on NSGA-II over the full pipelined/pipelined_m ranges, seeded with the current 22-design front, is the best use of the final round.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.852e+04 (gain this round: +1.8%).
Feasible designs: 177 of 300 evaluations (153 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 8% violate; best seen 273
- max_abs_err <= 0.000244141: 28% violate; best seen 4.18e-08 (2^-24.51)
- sys_p99_batch_us <= 0.44: 24% violate; best seen 0.161

Pareto front (feasible, 22 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=16 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1175, accuracy_bits=12, luts=906, ffs=268, throughput_msps=97.8, max_abs_err=0.000244 (2^-12.00), power_index=1.41
- pipelined_m [data_width=17 n_iter=15 angle_guard=3 frac_guard=1 rounding=round m=4] luts_plus_ffs=1244, accuracy_bits=13, luts=956, ffs=289, throughput_msps=93.6, max_abs_err=0.000124 (2^-12.98), power_index=1.5
- pipelined_m [data_width=17 n_iter=16 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1347, accuracy_bits=13.8, luts=1053, ffs=295, throughput_msps=93.6, max_abs_err=6.9e-05 (2^-13.82), power_index=1.62
- pipelined_m [data_width=18 n_iter=16 angle_guard=3 frac_guard=3 rounding=round m=3] luts_plus_ffs=1590, accuracy_bits=14.4, luts=1134, ffs=456, throughput_msps=119, max_abs_err=4.52e-05 (2^-14.43), power_index=1.91
- pipelined_m [data_width=20 n_iter=17 angle_guard=4 frac_guard=2 rounding=round m=4] luts_plus_ffs=1712, accuracy_bits=15.6, luts=1295, ffs=417, throughput_msps=89.6, max_abs_err=2.01e-05 (2^-15.61), power_index=2.06
- pipelined_m [data_width=27 n_iter=19 angle_guard=0 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=2381, accuracy_bits=17.9, luts=1693, ffs=688, throughput_msps=110, max_abs_err=3.97e-06 (2^-17.94), power_index=2.87
- pipelined_m [data_width=28 n_iter=19 angle_guard=0 frac_guard=1 rounding=round m=3] luts_plus_ffs=2523, accuracy_bits=18, luts=1809, ffs=713, throughput_msps=110, max_abs_err=3.87e-06 (2^-17.98), power_index=3.04
- pipelined_m [data_width=27 n_iter=24 angle_guard=0 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=2879, accuracy_bits=21, luts=2114, ffs=765, throughput_msps=110, max_abs_err=4.67e-07 (2^-21.03), power_index=3.46
- pipelined_m [data_width=27 n_iter=25 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=3219, accuracy_bits=22.2, luts=2338, ffs=881, throughput_msps=110, max_abs_err=2.06e-07 (2^-22.21), power_index=3.87
- pipelined_m [data_width=28 n_iter=25 angle_guard=2 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=3683, accuracy_bits=22.8, luts=2383, ffs=1301, throughput_msps=153, max_abs_err=1.41e-07 (2^-22.76), power_index=4.43
Front coverage: luts_plus_ffs 1175..3683 (HV reference 4000); accuracy_bits 12..22.8 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- unrolled_k: 25 evals, 0 feasible; max throughput seen 9.44 MSPS; best accuracy 12.42 bits
- pipelined: 55 evals, 32 feasible; max throughput seen 273 MSPS; best accuracy 15.54 bits; best feasible luts_plus_ffs=1830; feasible ranges: data_width 15..19, n_iter 14..20, angle_guard 2..4, frac_guard 0..3
- pipelined_m: 220 evals, 145 feasible; max throughput seen 171 MSPS; best accuracy 24.51 bits; best feasible luts_plus_ffs=1175; feasible ranges: data_width 16..28, n_iter 14..28, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=15..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (22 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 247 feasible; hypervolume 1.898e+04 (+2.5%).

**LLM decision:** `stop` — Final round: budget is exhausted (400/400 evals) and the round cap (4 of 4) is reached, so the front can no longer be improved in this run. Stopping is correct rather than 'infeasible' because all three constraints are demonstrably reachable by registry designs: throughput_msps best seen 273 vs required >= 32 (only 6% of evals violate), max_abs_err best seen 4.18e-08 (2^-24.51) vs required <= 2.44e-04 (23% violate), sys_p99_batch_us best seen 0.161 us vs required <= 0.44 us (25% violate). 247 of 400 evaluations (220 unique) are feasible, so no constraint is unreachable.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.898e+04 (gain this round: +2.5%).
Feasible designs: 247 of 400 evaluations (220 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 6% violate; best seen 273
- max_abs_err <= 0.000244141: 23% violate; best seen 4.18e-08 (2^-24.51)
- sys_p99_batch_us <= 0.44: 25% violate; best seen 0.161

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=16 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1175, accuracy_bits=12, luts=906, ffs=268, throughput_msps=97.8, max_abs_err=0.000244 (2^-12.00), power_index=1.41
- pipelined_m [data_width=16 n_iter=15 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1255, accuracy_bits=13.1, luts=968, ffs=287, throughput_msps=93.6, max_abs_err=0.000117 (2^-13.06), power_index=1.51
- pipelined_m [data_width=17 n_iter=16 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1347, accuracy_bits=13.8, luts=1053, ffs=295, throughput_msps=93.6, max_abs_err=6.9e-05 (2^-13.82), power_index=1.62
- pipelined_m [data_width=20 n_iter=17 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=1675, accuracy_bits=15.2, luts=1211, ffs=464, throughput_msps=119, max_abs_err=2.58e-05 (2^-15.24), power_index=2.02
- pipelined_m [data_width=20 n_iter=18 angle_guard=4 frac_guard=4 rounding=round m=3] luts_plus_ffs=1957, accuracy_bits=16.5, luts=1445, ffs=513, throughput_msps=114, max_abs_err=1.06e-05 (2^-16.52), power_index=2.36
- pipelined_m [data_width=27 n_iter=19 angle_guard=0 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=2381, accuracy_bits=17.9, luts=1693, ffs=688, throughput_msps=110, max_abs_err=3.97e-06 (2^-17.94), power_index=2.87
- pipelined_m [data_width=27 n_iter=21 angle_guard=0 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=2623, accuracy_bits=19.8, luts=1923, ffs=700, throughput_msps=110, max_abs_err=1.1e-06 (2^-19.79), power_index=3.16
- pipelined_m [data_width=27 n_iter=25 angle_guard=0 frac_guard=1 rounding=round m=3] luts_plus_ffs=3185, accuracy_bits=21.7, luts=2313, ffs=872, throughput_msps=110, max_abs_err=2.97e-07 (2^-21.68), power_index=3.83
- pipelined_m [data_width=27 n_iter=25 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=3219, accuracy_bits=22.2, luts=2338, ffs=881, throughput_msps=110, max_abs_err=2.06e-07 (2^-22.21), power_index=3.87
- pipelined_m [data_width=28 n_iter=26 angle_guard=2 frac_guard=4 rounding=round m=2] luts_plus_ffs=4074, accuracy_bits=23.9, luts=2699, ffs=1375, throughput_msps=147, max_abs_err=6.35e-08 (2^-23.91), power_index=4.9
Front coverage: luts_plus_ffs 1175..4074 (HV reference 4000); accuracy_bits 12..23.9 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- unrolled_k: 25 evals, 0 feasible; max throughput seen 9.44 MSPS; best accuracy 12.42 bits
- pipelined: 55 evals, 32 feasible; max throughput seen 273 MSPS; best accuracy 15.54 bits; best feasible luts_plus_ffs=1830; feasible ranges: data_width 15..19, n_iter 14..20, angle_guard 2..4, frac_guard 0..3
- pipelined_m: 320 evals, 215 feasible; max throughput seen 171 MSPS; best accuracy 24.51 bits; best feasible luts_plus_ffs=1175; feasible ranges: data_width 15..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 29239 in, 15160 out
- provider-reported cost: $0.0169
- full prompts and replies: `llm_trace.jsonl`

