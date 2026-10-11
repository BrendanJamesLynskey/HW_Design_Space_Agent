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
`pipelined_m:data_width=19,n_iter=14,angle_guard=2,frac_guard=0,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 896 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 305 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.44 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000163 (2^-12.58) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 21.4 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.18e-05 (2^-14.24) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 6.79 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.6 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 96.7 dBc, SNR 82.7 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Every L1-feasible design (212) was simulated at its estimated Fmax (SimPy); 198 pass. Top 5 by the selection rule, L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=19,n_iter=14,angle_guard=2,frac_guard=0,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=1,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=4,frac_guard=1,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=19,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=16,n_iter=15,angle_guard=4,frac_guard=2,rounding=round,m=3` | 0.3103 → 0.3186 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (22 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=14,angle_guard=2,frac_guard=0,rounding=trunc,m=4` | 896 | 305 | 93.6 | 6 | 1.44 | 0.000163 (2^-12.58) | 12.58 |
| 1 | `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=1,rounding=round,m=4` | 958 | 291 | 93.6 | 6 | 1.5 | 0.00014 (2^-12.80) | 12.80 |
| 2 | `pipelined_m:data_width=17,n_iter=15,angle_guard=4,frac_guard=1,rounding=round,m=4` | 971 | 293 | 93.6 | 6 | 1.52 | 0.000126 (2^-12.95) | 12.95 |
| 3 | `pipelined_m:data_width=19,n_iter=15,angle_guard=3,frac_guard=0,rounding=trunc,m=3` | 979 | 376 | 119.3 | 7 | 1.63 | 0.000109 (2^-13.17) | 13.17 |
| 4 | `pipelined_m:data_width=20,n_iter=16,angle_guard=0,frac_guard=1,rounding=round,m=4` | 1122 | 319 | 93.6 | 6 | 1.73 | 5.03e-05 (2^-14.28) | 14.28 |
| 5 | `pipelined_m:data_width=18,n_iter=19,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1257 | 364 | 93.6 | 7 | 1.95 | 5.02e-05 (2^-14.28) | 14.28 |
| 6 | `pipelined_m:data_width=19,n_iter=16,angle_guard=4,frac_guard=2,rounding=round,m=3` | 1168 | 472 | 114.5 | 8 | 1.97 | 3.9e-05 (2^-14.64) | 14.64 |
| 7 | `pipelined_m:data_width=22,n_iter=17,angle_guard=-2,frac_guard=2,rounding=trunc,m=4` | 1253 | 419 | 89.6 | 7 | 2.01 | 3.38e-05 (2^-14.85) | 14.85 |
| 8 | `pipelined_m:data_width=19,n_iter=18,angle_guard=4,frac_guard=1,rounding=round,m=4` | 1281 | 391 | 89.6 | 7 | 2.01 | 2.72e-05 (2^-15.16) | 15.16 |
| 9 | `pipelined_m:data_width=19,n_iter=20,angle_guard=2,frac_guard=3,rounding=trunc,m=4` | 1427 | 395 | 93.6 | 7 | 2.19 | 2.18e-05 (2^-15.49) | 15.49 |
| 10 | `pipelined_m:data_width=22,n_iter=18,angle_guard=-1,frac_guard=1,rounding=round,m=3` | 1359 | 492 | 114.5 | 8 | 2.23 | 1.78e-05 (2^-15.77) | 15.77 |
| 11 | `pipelined_m:data_width=19,n_iter=19,angle_guard=4,frac_guard=4,rounding=round,m=4` | 1468 | 416 | 89.6 | 7 | 2.27 | 1.02e-05 (2^-16.58) | 16.58 |
| 12 | `pipelined_m:data_width=22,n_iter=20,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 1527 | 431 | 89.6 | 7 | 2.36 | 6.11e-06 (2^-17.32) | 17.32 |
| 13 | `pipelined_m:data_width=22,n_iter=20,angle_guard=3,frac_guard=4,rounding=trunc,m=4` | 1667 | 460 | 89.6 | 7 | 2.56 | 3.36e-06 (2^-18.18) | 18.18 |
| 14 | `pipelined_m:data_width=23,n_iter=20,angle_guard=4,frac_guard=1,rounding=round,m=4` | 1675 | 460 | 86.0 | 7 | 2.57 | 2.88e-06 (2^-18.40) | 18.40 |
| 15 | `pipelined_m:data_width=25,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 1798 | 547 | 89.6 | 8 | 2.82 | 1.75e-06 (2^-19.13) | 19.13 |
| 16 | `pipelined_m:data_width=26,n_iter=22,angle_guard=4,frac_guard=0,rounding=trunc,m=3` | 1953 | 771 | 110.0 | 10 | 3.28 | 1e-06 (2^-19.93) | 19.93 |
| 17 | `pipelined_m:data_width=24,n_iter=23,angle_guard=2,frac_guard=3,rounding=round,m=3` | 2050 | 747 | 110.0 | 10 | 3.37 | 7.74e-07 (2^-20.30) | 20.30 |
| 18 | `pipelined_m:data_width=26,n_iter=24,angle_guard=1,frac_guard=4,rounding=trunc,m=3` | 2259 | 803 | 110.0 | 10 | 3.69 | 3.5e-07 (2^-21.45) | 21.45 |
| 19 | `pipelined_m:data_width=26,n_iter=24,angle_guard=1,frac_guard=4,rounding=round,m=3` | 2314 | 805 | 110.0 | 10 | 3.75 | 3.27e-07 (2^-21.54) | 21.54 |
| 20 | `pipelined_m:data_width=26,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc,m=3` | 2455 | 900 | 110.0 | 11 | 4.04 | 1.72e-07 (2^-22.47) | 22.47 |
| 21 | `pipelined_m:data_width=26,n_iter=28,angle_guard=3,frac_guard=3,rounding=trunc,m=3` | 2651 | 995 | 110.0 | 12 | 4.39 | 1.67e-07 (2^-22.51) | 22.51 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraints here are the burst latency and 12-bit accuracy, not raw throughput. A 1 MHz tick dumps 32 requests at once and all must return within 0.44 us, i.e. the unit must sustain ~32/0.44 ≈ 73 results/us during the burst (well above the 32 msps throughput floor) plus pipeline latency. That immediately rules out `iterative`: at 1 result per N+3 cycles it would need Fmax ≈ 73·(N+3) ≥ 500 MHz, impossible on Artix-7. `pipelined` and `pipelined_m` both issue 1 result/cycle, so they only need Fmax ≈ (32+N+2)/0.44 ≈ 100–125 MHz, which is the only realistic way to satisfy sys_p99_batch_us; `pipelined_m` is the area-lever (fewer pipeline registers → lower luts_plus_ffs, at the cost of Fmax), so it is the likely area-optimal family and deserves a large share. `unrolled_k` gets a small share only to test whether k=8 can reach the required issue rate. Accuracy needs roughly W≥14 (output LSB 2^-(W-2)) and N≥13 (residual ≈2^-N), so ranges are centred there but kept wide enough to map the area-vs-accuracy front up to ~18 bits for hypervolume coverage. Rounding and both guard fields are left open because they buy accuracy cheaply and shift the front.*)
- `pipelined` (45 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* 1 result/cycle gives the highest Fmax of the feasible families, so it has the best chance of clearing sys_p99_batch_us with margin (important because the L1 bound is optimistic and L2 re-screens). It registers every stage, so it is FF-heavy and anchors the low-latency / high-area end of the front.
- `pipelined_m` (40 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..6. *Why:* Same 1 result/cycle throughput as `pipelined` but registers only every m stages, cutting FFs and therefore luts_plus_ffs — the primary objective. The risk is a longer combinational path lowering Fmax below what the burst bound needs, so m is kept small (2–6) to preserve enough clock speed while still saving registers. This is the most likely source of the area-optimal, selection-winning design.
- `unrolled_k` (15 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=4..8. *Why:* k chained micro-rotations/cycle gives 1 result per ceil(N/k)+3 cycles, so meeting the burst bound needs Fmax ≈ 73·(ceil(N/k)+3) ≈ 290–365 MHz even at k=8 — probably infeasible on Artix-7. A small share is spent only to confirm this and to catch any low-area point if high k does reach the required issue rate.

**Result (code):** 100 evaluations this round, 100 total; 29 feasible; hypervolume 9667 (n/a).

**LLM decision:** `map_front` — The feasible front is only 4 designs, all pipelined_m with data_width pinned at 19, spanning luts_plus_ffs 1355..2037 against an HV reference of 4000 and accuracy_bits 13.2..16.2 against a reference of 12. So the front covers only a narrow middle band of the area objective (nothing below 1355, nothing between 2037 and the 4000 reference) and a single data_width value out of the registry's 8..28, while pipelined already has 21 feasible designs (best luts_plus_ffs=1860) that never reach the front. The trade-off curve is therefore far from mapped: the cheap-area end and the high-accuracy/high-area end are both unexplored, and the accuracy dimension is saturated above the reference so hypervolume is driven almost entirely by filling the area axis. A code-driven NSGA-II coverage search over the full ranges of the two families that actually produce feasible designs (pipelined, pipelined_m), seeded with the current front, is the right use of this round. iterative/unrolled_k are not worth adding: unrolled_k gave 0 feasible in 15 evals with max throughput 10.3 MSPS, and iterative's 1-result-per-(N+3)-cycles schedule cannot reach the 32 MSPS floor at the N needed for 2^-12 accuracy.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 9667 (gain this round: n/a (first round)).
Feasible designs: 29 of 100 evaluations (24 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 15% violate; best seen 273
- max_abs_err <= 0.000244141: 45% violate; best seen 1.3e-05 (2^-16.24)
- sys_p99_batch_us <= 0.44: 42% violate; best seen 0.154

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=1355, accuracy_bits=13.2, luts=979, ffs=376, throughput_msps=119, max_abs_err=0.000109 (2^-13.17), power_index=1.63
- pipelined_m [data_width=19 n_iter=20 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1822, accuracy_bits=15.5, luts=1427, ffs=395, throughput_msps=93.6, max_abs_err=2.18e-05 (2^-15.49), power_index=2.19
- pipelined_m [data_width=19 n_iter=19 angle_guard=3 frac_guard=3 rounding=round m=3] luts_plus_ffs=1961, accuracy_bits=16.2, luts=1411, ffs=550, throughput_msps=119, max_abs_err=1.31e-05 (2^-16.22), power_index=2.36
- pipelined_m [data_width=19 n_iter=20 angle_guard=3 frac_guard=3 rounding=round m=3] luts_plus_ffs=2037, accuracy_bits=16.2, luts=1487, ffs=550, throughput_msps=119, max_abs_err=1.3e-05 (2^-16.24), power_index=2.45
Front coverage: luts_plus_ffs 1355..2037 (HV reference 4000); accuracy_bits 13.2..16.2 (HV reference 12); data_width on the front 19..19 (registry 8..28).

Per family:
- unrolled_k: 15 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 14.28 bits
- pipelined: 45 evals, 21 feasible; max throughput seen 273 MSPS; best accuracy 14.64 bits; best feasible luts_plus_ffs=1860; feasible ranges: data_width 16..20, n_iter 14..20, angle_guard 0..3, frac_guard 0..4
- pipelined_m: 40 evals, 8 feasible; max throughput seen 171 MSPS; best accuracy 16.24 bits; best feasible luts_plus_ffs=1355; feasible ranges: data_width 19..19, n_iter 15..20, angle_guard 2..3, frac_guard 0..3, m 3..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=18..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 105 feasible; hypervolume 1.832e+04 (+89.5%).

**LLM decision:** `refine` — The entire 15-design front is pipelined_m, spanning luts_plus_ffs 1200..3646 (HV ref 4000) and accuracy_bits 12.6..22.5 (HV ref 12). Both the selection rule (min luts_plus_ffs) and the hypervolume hinge on the low-area end, and the cheapest point (1200 LUT+FF, 12.6 bits, max_abs_err 1.63e-4) sits only just above the 2^-12 = 2.44e-4 error limit, so cheaper feasible points are plausible at data_width<18 if n_iter/frac_guard/angle_guard are raised. The other families offer nothing here: unrolled_k was 0/15 feasible with max throughput 10.3 MSPS and iterative is strictly slower (1 micro-rotation/cycle), so neither can reach the 32 MSPS constraint; pipelined is dominated on area (best feasible 1860 vs 1200) and its only advantage (273 MSPS) is not an objective. I therefore spend this round tightening pipelined_m around the low/mid-area region and probing data_width below the current 18 floor, while keeping m open to 2..5 since the front shows m=3 (119 MSPS) out-throughputs m=4 (93.6 MSPS), which matters for the L2 system re-selection risk on the cheapest designs.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.832e+04 (gain this round: +89.5%).
Feasible designs: 105 of 200 evaluations (92 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 8% violate; best seen 273
- max_abs_err <= 0.000244141: 23% violate; best seen 5.36e-08 (2^-24.15)
- sys_p99_batch_us <= 0.44: 32% violate; best seen 0.154

Pareto front (feasible, 15 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=2 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1200, accuracy_bits=12.6, luts=896, ffs=305, throughput_msps=93.6, max_abs_err=0.000163 (2^-12.58), power_index=1.44
- pipelined_m [data_width=19 n_iter=17 angle_guard=0 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1512, accuracy_bits=14.1, luts=1135, ffs=377, throughput_msps=93.6, max_abs_err=5.67e-05 (2^-14.11), power_index=1.82
- pipelined_m [data_width=18 n_iter=17 angle_guard=2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=1600, accuracy_bits=14.1, luts=1152, ffs=448, throughput_msps=119, max_abs_err=5.51e-05 (2^-14.15), power_index=1.93
- pipelined_m [data_width=19 n_iter=20 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1822, accuracy_bits=15.5, luts=1427, ffs=395, throughput_msps=93.6, max_abs_err=2.18e-05 (2^-15.49), power_index=2.19
- pipelined_m [data_width=19 n_iter=19 angle_guard=4 frac_guard=4 rounding=round m=4] luts_plus_ffs=1884, accuracy_bits=16.6, luts=1468, ffs=416, throughput_msps=89.6, max_abs_err=1.02e-05 (2^-16.58), power_index=2.27
- pipelined_m [data_width=24 n_iter=20 angle_guard=-2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=2060, accuracy_bits=17.1, luts=1607, ffs=453, throughput_msps=89.6, max_abs_err=7.2e-06 (2^-17.08), power_index=2.48
- pipelined_m [data_width=22 n_iter=21 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=2168, accuracy_bits=18, luts=1649, ffs=519, throughput_msps=89.6, max_abs_err=3.8e-06 (2^-18.01), power_index=2.61
- pipelined_m [data_width=25 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=2345, accuracy_bits=19.1, luts=1798, ffs=547, throughput_msps=89.6, max_abs_err=1.75e-06 (2^-19.13), power_index=2.82
- pipelined_m [data_width=24 n_iter=23 angle_guard=2 frac_guard=3 rounding=round m=3] luts_plus_ffs=2796, accuracy_bits=20.3, luts=2050, ffs=747, throughput_msps=110, max_abs_err=7.74e-07 (2^-20.30), power_index=3.37
- pipelined_m [data_width=26 n_iter=28 angle_guard=3 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3646, accuracy_bits=22.5, luts=2651, ffs=995, throughput_msps=110, max_abs_err=1.67e-07 (2^-22.51), power_index=4.39
Front coverage: luts_plus_ffs 1200..3646 (HV reference 4000); accuracy_bits 12.6..22.5 (HV reference 12); data_width on the front 18..26 (registry 8..28).

Per family:
- unrolled_k: 15 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 14.28 bits
- pipelined: 45 evals, 21 feasible; max throughput seen 273 MSPS; best accuracy 14.64 bits; best feasible luts_plus_ffs=1860; feasible ranges: data_width 16..20, n_iter 14..20, angle_guard 0..3, frac_guard 0..4
- pipelined_m: 140 evals, 84 feasible; max throughput seen 171 MSPS; best accuracy 24.15 bits; best feasible luts_plus_ffs=1200; feasible ranges: data_width 18..28, n_iter 13..29, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Focus the remaining budget on the low-area pipelined_m region that drives both the min-area selection and the hypervolume, since iterative/unrolled_k cannot meet the 32 MSPS throughput constraint and pipelined is area-dominated.*)
- `pipelined_m` (100 evals): data_width=15..22, n_iter=13..24, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..5. *Why:* Only family on the front; push data_width below the current 18 floor with more iterations/guard bits to find cheaper feasible points at the accuracy limit, and fill the 2345..3646 area gap, keeping m 2..5 to expose higher-Fmax low-area options for the L2 system screen.

**Result (code):** 100 evaluations this round, 300 total; 181 feasible; hypervolume 1.86e+04 (+1.5%).

**LLM decision:** `map_front` — Round 3 gained only +1.5% HV (1.86e+04) and we have exactly one round / 100 evals left, so the marginal value is in covering the unused part of the objective ranges rather than chasing local refinement. The feasible front lives entirely in pipelined and pipelined_m (pipelined_m dominant: 160 unique feasible, best luts_plus_ffs=1200; pipelined best feasible luts_plus_ffs=1860), and it is truncated on the area axis: it spans luts_plus_ffs 1200..3646 against the HV reference of 4000 (nothing below 1200 explored), while on the accuracy axis it over-covers (12.6..22.5 vs ref 12). Accuracy is therefore not the binding dimension; the unexplored cheap side (data_width 17..26 on the front, registry allows 8) is where remaining hypervolume and the min-luts_plus_ffs selection rule both point. All three constraints are comfortably reachable (throughput best 273 vs 32; max_abs_err best 5.36e-08 vs 2.44e-04; sys_p99_batch_us best 0.154 vs 0.44), so this is not infeasible. iterative is deliberately not added: it yields one result per N+3 cycles (and unrolled_k already produced 0 feasible with max throughput 10.3 MSPS), so it cannot clear the >=32 MSPS constraint and would waste budget. Spending the final round on a seeded NSGA-II over the full ranges of pipelined/pipelined_m maps the whole front, pushes into the <1200 LUT+FF region, and gives the L2 system re-selection the widest set of pass-margin candidates.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.86e+04 (gain this round: +1.5%).
Feasible designs: 181 of 300 evaluations (160 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 5% violate; best seen 273
- max_abs_err <= 0.000244141: 20% violate; best seen 5.36e-08 (2^-24.15)
- sys_p99_batch_us <= 0.44: 25% violate; best seen 0.154

Pareto front (feasible, 20 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=2 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1200, accuracy_bits=12.6, luts=896, ffs=305, throughput_msps=93.6, max_abs_err=0.000163 (2^-12.58), power_index=1.44
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=1355, accuracy_bits=13.2, luts=979, ffs=376, throughput_msps=119, max_abs_err=0.000109 (2^-13.17), power_index=1.63
- pipelined_m [data_width=19 n_iter=17 angle_guard=0 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1512, accuracy_bits=14.1, luts=1135, ffs=377, throughput_msps=93.6, max_abs_err=5.67e-05 (2^-14.11), power_index=1.82
- pipelined_m [data_width=20 n_iter=18 angle_guard=-1 frac_guard=0 rounding=round m=3] luts_plus_ffs=1610, accuracy_bits=14.2, luts=1170, ffs=440, throughput_msps=119, max_abs_err=5.25e-05 (2^-14.22), power_index=1.94
- pipelined_m [data_width=22 n_iter=17 angle_guard=-2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1672, accuracy_bits=14.9, luts=1253, ffs=419, throughput_msps=89.6, max_abs_err=3.38e-05 (2^-14.85), power_index=2.01
- pipelined_m [data_width=22 n_iter=18 angle_guard=-1 frac_guard=1 rounding=round m=3] luts_plus_ffs=1852, accuracy_bits=15.8, luts=1359, ffs=492, throughput_msps=114, max_abs_err=1.78e-05 (2^-15.77), power_index=2.23
- pipelined_m [data_width=22 n_iter=20 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1958, accuracy_bits=17.3, luts=1527, ffs=431, throughput_msps=89.6, max_abs_err=6.11e-06 (2^-17.32), power_index=2.36
- pipelined_m [data_width=22 n_iter=20 angle_guard=3 frac_guard=3 rounding=round m=3] luts_plus_ffs=2293, accuracy_bits=18.3, luts=1673, ffs=619, throughput_msps=114, max_abs_err=3.04e-06 (2^-18.33), power_index=2.76
- pipelined_m [data_width=24 n_iter=23 angle_guard=2 frac_guard=3 rounding=round m=3] luts_plus_ffs=2796, accuracy_bits=20.3, luts=2050, ffs=747, throughput_msps=110, max_abs_err=7.74e-07 (2^-20.30), power_index=3.37
- pipelined_m [data_width=26 n_iter=28 angle_guard=3 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3646, accuracy_bits=22.5, luts=2651, ffs=995, throughput_msps=110, max_abs_err=1.67e-07 (2^-22.51), power_index=4.39
Front coverage: luts_plus_ffs 1200..3646 (HV reference 4000); accuracy_bits 12.6..22.5 (HV reference 12); data_width on the front 17..26 (registry 8..28).

Per family:
- unrolled_k: 15 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 14.28 bits
- pipelined: 45 evals, 21 feasible; max throughput seen 273 MSPS; best accuracy 14.64 bits; best feasible luts_plus_ffs=1860; feasible ranges: data_width 16..20, n_iter 14..20, angle_guard 0..3, frac_guard 0..4
- pipelined_m: 240 evals, 160 feasible; max throughput seen 171 MSPS; best accuracy 24.15 bits; best feasible luts_plus_ffs=1200; feasible ranges: data_width 16..28, n_iter 13..29, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (20 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 237 feasible; hypervolume 1.914e+04 (+2.9%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), so no further exploration is possible. The front is clearly feasible, not infeasible: every constraint has designs that pass with margin — throughput best seen 273 MSPS vs the >=32 requirement, max_abs_err best 5.36e-08 (2^-24.15) vs the 2^-12=2.44e-4 limit, and sys_p99_batch best 0.154 us vs the 0.44 us bound. The feasible front holds 22 designs (212 unique of 400 evals) and has good spread on both objectives: luts_plus_ffs 1200..3646 against the HV reference 4000, accuracy_bits 12.6..22.5 against the HV reference 12, giving HV 1.914e4 with a +2.9% gain in the last round. The selection rule (min luts_plus_ffs) is served directly by the front's cheapest point, pipelined_m [data_width=19 n_iter=14 angle_guard=2 frac_guard=0 rounding=trunc m=4] at luts_plus_ffs=1200, accuracy_bits=12.6 (max_abs_err 1.63e-4, still within the 2^-12 limit), 93.6 MSPS — comfortably meeting both the throughput and error constraints, with ample sys_p99_batch headroom relative to the 0.44 us bound for the L2 simulation. Since constraints are met, the curve is well covered, and no further evaluations remain, stop is the correct call.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.914e+04 (gain this round: +2.9%).
Feasible designs: 237 of 400 evaluations (212 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 4% violate; best seen 273
- max_abs_err <= 0.000244141: 18% violate; best seen 5.36e-08 (2^-24.15)
- sys_p99_batch_us <= 0.44: 28% violate; best seen 0.154

Pareto front (feasible, 22 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=2 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1200, accuracy_bits=12.6, luts=896, ffs=305, throughput_msps=93.6, max_abs_err=0.000163 (2^-12.58), power_index=1.44
- pipelined_m [data_width=17 n_iter=15 angle_guard=4 frac_guard=1 rounding=round m=4] luts_plus_ffs=1263, accuracy_bits=13, luts=971, ffs=293, throughput_msps=93.6, max_abs_err=0.000126 (2^-12.95), power_index=1.52
- pipelined_m [data_width=18 n_iter=19 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1621, accuracy_bits=14.3, luts=1257, ffs=364, throughput_msps=93.6, max_abs_err=5.02e-05 (2^-14.28), power_index=1.95
- pipelined_m [data_width=22 n_iter=17 angle_guard=-2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1672, accuracy_bits=14.9, luts=1253, ffs=419, throughput_msps=89.6, max_abs_err=3.38e-05 (2^-14.85), power_index=2.01
- pipelined_m [data_width=19 n_iter=20 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1822, accuracy_bits=15.5, luts=1427, ffs=395, throughput_msps=93.6, max_abs_err=2.18e-05 (2^-15.49), power_index=2.19
- pipelined_m [data_width=22 n_iter=20 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1958, accuracy_bits=17.3, luts=1527, ffs=431, throughput_msps=89.6, max_abs_err=6.11e-06 (2^-17.32), power_index=2.36
- pipelined_m [data_width=23 n_iter=20 angle_guard=4 frac_guard=1 rounding=round m=4] luts_plus_ffs=2136, accuracy_bits=18.4, luts=1675, ffs=460, throughput_msps=86, max_abs_err=2.88e-06 (2^-18.40), power_index=2.57
- pipelined_m [data_width=26 n_iter=22 angle_guard=4 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=2723, accuracy_bits=19.9, luts=1953, ffs=771, throughput_msps=110, max_abs_err=1e-06 (2^-19.93), power_index=3.28
- pipelined_m [data_width=26 n_iter=24 angle_guard=1 frac_guard=4 rounding=round m=3] luts_plus_ffs=3119, accuracy_bits=21.5, luts=2314, ffs=805, throughput_msps=110, max_abs_err=3.27e-07 (2^-21.54), power_index=3.75
- pipelined_m [data_width=26 n_iter=28 angle_guard=3 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3646, accuracy_bits=22.5, luts=2651, ffs=995, throughput_msps=110, max_abs_err=1.67e-07 (2^-22.51), power_index=4.39
Front coverage: luts_plus_ffs 1200..3646 (HV reference 4000); accuracy_bits 12.6..22.5 (HV reference 12); data_width on the front 17..26 (registry 8..28).

Per family:
- unrolled_k: 15 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 14.28 bits
- pipelined: 45 evals, 21 feasible; max throughput seen 273 MSPS; best accuracy 14.64 bits; best feasible luts_plus_ffs=1860; feasible ranges: data_width 16..20, n_iter 14..20, angle_guard 0..3, frac_guard 0..4
- pipelined_m: 340 evals, 216 feasible; max throughput seen 171 MSPS; best accuracy 24.15 bits; best feasible luts_plus_ffs=1200; feasible ranges: data_width 16..28, n_iter 13..29, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 17154 in, 19903 out
- provider-reported cost: $0.0148
- full prompts and replies: `llm_trace.jsonl`

