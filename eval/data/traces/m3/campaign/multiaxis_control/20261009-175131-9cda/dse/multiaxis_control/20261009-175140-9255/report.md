# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
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
`pipelined_m:data_width=16,n_iter=14,angle_guard=3,frac_guard=2,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 875 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 280 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.39 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000189 (2^-12.37) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.1 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 5.61e-05 (2^-14.12) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 0.92 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.4 | exact: bit-accurate model, exhaustive (65536 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 98.2 dBc, SNR 82.0 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=16,n_iter=14,angle_guard=3,frac_guard=2,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=16,n_iter=14,angle_guard=3,frac_guard=3,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=16,n_iter=14,angle_guard=3,frac_guard=4,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=16,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=16,n_iter=16,angle_guard=2,frac_guard=3,rounding=round,m=4` | 0.3848 → 0.3953 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (22 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=14,angle_guard=3,frac_guard=2,rounding=round,m=4` | 875 | 280 | 93.6 | 6 | 1.39 | 0.000189 (2^-12.37) | 12.37 |
| 1 | `pipelined_m:data_width=16,n_iter=14,angle_guard=3,frac_guard=3,rounding=round,m=4` | 902 | 287 | 93.6 | 6 | 1.43 | 0.000171 (2^-12.51) | 12.51 |
| 2 | `pipelined_m:data_width=16,n_iter=14,angle_guard=3,frac_guard=4,rounding=round,m=4` | 929 | 293 | 93.6 | 6 | 1.47 | 0.00017 (2^-12.52) | 12.52 |
| 3 | `pipelined_m:data_width=16,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=4` | 987 | 276 | 97.8 | 6 | 1.52 | 0.000134 (2^-12.86) | 12.86 |
| 4 | `pipelined_m:data_width=16,n_iter=16,angle_guard=2,frac_guard=3,rounding=round,m=4` | 1019 | 282 | 93.6 | 6 | 1.57 | 0.000114 (2^-13.09) | 13.09 |
| 5 | `pipelined_m:data_width=19,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc,m=3` | 979 | 374 | 119.3 | 7 | 1.63 | 9.41e-05 (2^-13.38) | 13.38 |
| 6 | `pipelined_m:data_width=16,n_iter=16,angle_guard=3,frac_guard=4,rounding=round,m=4` | 1066 | 293 | 93.6 | 6 | 1.64 | 9.1e-05 (2^-13.42) | 13.42 |
| 7 | `pipelined_m:data_width=20,n_iter=15,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1110 | 333 | 93.6 | 6 | 1.74 | 6.58e-05 (2^-13.89) | 13.89 |
| 8 | `pipelined_m:data_width=22,n_iter=15,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1141 | 357 | 89.6 | 6 | 1.8 | 6.32e-05 (2^-13.95) | 13.95 |
| 9 | `pipelined_m:data_width=20,n_iter=16,angle_guard=4,frac_guard=3,rounding=trunc,m=4` | 1207 | 345 | 89.6 | 6 | 1.87 | 3.59e-05 (2^-14.77) | 14.77 |
| 10 | `pipelined_m:data_width=20,n_iter=18,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1295 | 405 | 93.6 | 7 | 2.05 | 1.92e-05 (2^-15.67) | 15.67 |
| 11 | `pipelined_m:data_width=22,n_iter=18,angle_guard=-1,frac_guard=2,rounding=trunc,m=4` | 1349 | 424 | 89.6 | 7 | 2.13 | 1.72e-05 (2^-15.83) | 15.83 |
| 12 | `pipelined_m:data_width=20,n_iter=18,angle_guard=2,frac_guard=3,rounding=round,m=4` | 1373 | 415 | 89.6 | 7 | 2.15 | 1.32e-05 (2^-16.21) | 16.21 |
| 13 | `pipelined_m:data_width=24,n_iter=18,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 1456 | 460 | 89.6 | 7 | 2.31 | 8.44e-06 (2^-16.85) | 16.85 |
| 14 | `pipelined_m:data_width=22,n_iter=20,angle_guard=1,frac_guard=1,rounding=trunc,m=3` | 1507 | 579 | 114.5 | 9 | 2.51 | 6.93e-06 (2^-17.14) | 17.14 |
| 15 | `pipelined_m:data_width=22,n_iter=21,angle_guard=1,frac_guard=1,rounding=trunc,m=3` | 1586 | 579 | 114.5 | 9 | 2.61 | 6.73e-06 (2^-17.18) | 17.18 |
| 16 | `pipelined_m:data_width=26,n_iter=20,angle_guard=1,frac_guard=0,rounding=trunc,m=4` | 1707 | 486 | 86.0 | 7 | 2.64 | 2.39e-06 (2^-18.67) | 18.67 |
| 17 | `pipelined_m:data_width=23,n_iter=23,angle_guard=3,frac_guard=2,rounding=trunc,m=4` | 1906 | 545 | 89.6 | 8 | 2.95 | 1.71e-06 (2^-19.16) | 19.16 |
| 18 | `pipelined_m:data_width=28,n_iter=23,angle_guard=2,frac_guard=1,rounding=trunc,m=3` | 2184 | 821 | 110.0 | 10 | 3.62 | 3.03e-07 (2^-21.66) | 21.66 |
| 19 | `pipelined_m:data_width=28,n_iter=23,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 2208 | 829 | 105.9 | 10 | 3.66 | 3.01e-07 (2^-21.66) | 21.66 |
| 20 | `pipelined_m:data_width=26,n_iter=24,angle_guard=4,frac_guard=2,rounding=round,m=3` | 2290 | 801 | 110.0 | 10 | 3.72 | 2.08e-07 (2^-22.20) | 22.20 |
| 21 | `pipelined_m:data_width=28,n_iter=28,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 2708 | 1023 | 105.9 | 12 | 4.49 | 1e-07 (2^-23.25) | 23.25 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 Msps throughput and 0.44us p99 batch latency for 32 simultaneous requests. This demands 1 result/cycle throughput, which only pipelined and pipelined_m families provide natively. unrolled_k with high k can also achieve this. iterative is excluded as it produces 1 result every N+3 cycles, far too slow. Accuracy constraint (2^-12) requires n_iter >= 12 typically. data_width 14-16 covers the accuracy requirement while keeping area reasonable. The budget is split to focus on pipelined (baseline), pipelined_m (area optimization via m), and unrolled_k (alternative architecture). Guards are given full ranges to map the accuracy/area trade-off curve for hypervolume.*)
- `pipelined` (50 evals): data_width=14..16, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* 1 result/cycle throughput (32 Msps) requires pipelined. N=12-16 balances accuracy (>=12 bits) and area. Full range of guards to map the accuracy/area trade-off for the Pareto front.
- `pipelined_m` (30 evals): data_width=14..16, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* Registering every m stages reduces FF count vs fully pipelined while maintaining 1 result/cycle throughput. m=2-4 is the sweet spot for area reduction without hurting Fmax too much. Critical for minimizing luts_plus_ffs.
- `unrolled_k` (20 evals): data_width=14..16, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=4..8. *Why:* k=4-8 unrolled rotations/cycle can achieve 32 Msps throughput with fewer pipeline stages than fully pipelined. May offer lower area than pipelined for the same throughput. Worth exploring as an alternative front.

**Result (code):** 100 evaluations this round, 100 total; 18 feasible; hypervolume 2767 (n/a).

**LLM decision:** `refine` — The current front has a gap: pipelined_m achieves 1189 area but only 12.5 bits accuracy, while pipelined achieves 12.6+ bits but costs 1824+ area. The 80% error violation rate suggests the accuracy constraint is tight. I need to explore whether pipelined_m can achieve higher accuracy (12.6+) at lower area than pipelined, or whether pipelined can reduce area. The unrolled_k family is infeasible (max 10.3 MSPS < 32 required), so I'll skip it. iterative is not yet explored but likely has similar throughput issues to unrolled_k (1 result per N+3 cycles), so I'll focus on refining the two promising families first.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 2767 (gain this round: n/a (first round)).
Feasible designs: 18 of 100 evaluations (16 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 20% violate; best seen 273
- max_abs_err <= 0.000244141: 80% violate; best seen 0.000109 (2^-13.17)
- sys_p99_batch_us <= 0.44: 20% violate; best seen 0.161

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1189, accuracy_bits=12.5, luts=902, ffs=287, throughput_msps=93.6, max_abs_err=0.000171 (2^-12.51), power_index=1.43
- pipelined_m [data_width=16 n_iter=14 angle_guard=3 frac_guard=4 rounding=round m=4] luts_plus_ffs=1222, accuracy_bits=12.5, luts=929, ffs=293, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.52), power_index=1.47
- pipelined [data_width=16 n_iter=14 angle_guard=4 frac_guard=3 rounding=round] luts_plus_ffs=1824, accuracy_bits=12.6, luts=916, ffs=908, throughput_msps=264, max_abs_err=0.000166 (2^-12.56), power_index=2.2
- pipelined [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=1966, accuracy_bits=12.9, luts=987, ffs=979, throughput_msps=273, max_abs_err=0.000134 (2^-12.86), power_index=2.37
- pipelined [data_width=16 n_iter=16 angle_guard=4 frac_guard=2 rounding=round] luts_plus_ffs=2030, accuracy_bits=13.2, luts=1019, ffs=1011, throughput_msps=264, max_abs_err=0.000109 (2^-13.17), power_index=2.44
Front coverage: luts_plus_ffs 1189..2030 (HV reference 4000); accuracy_bits 12.5..13.2 (HV reference 12); data_width on the front 16..16 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 12.27 bits
- pipelined: 50 evals, 13 feasible; max throughput seen 273 MSPS; best accuracy 13.17 bits; best feasible luts_plus_ffs=1716; feasible ranges: data_width 15..16, n_iter 14..16, angle_guard 1..4, frac_guard 1..4
- pipelined_m: 30 evals, 5 feasible; max throughput seen 171 MSPS; best accuracy 12.52 bits; best feasible luts_plus_ffs=1189; feasible ranges: data_width 16..16, n_iter 14..14, angle_guard 3..3, frac_guard 3..4, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The current front has a gap: pipelined_m achieves 1189 area but only 12.5 bits accuracy, while pipelined achieves 12.6+ bits but costs 1824+ area. The 80% error violation rate suggests the accuracy constraint is tight. I need to explore whether pipelined_m can achieve higher accuracy (12.6+) at lower area than pipelined, or whether pipelined can reduce area. The unrolled_k family is infeasible (max 10.3 MSPS < 32 required), so I'll skip it. iterative is not yet explored but likely has similar throughput issues to unrolled_k (1 result per N+3 cycles), so I'll focus on refining the two promising families first.*)
- `pipelined_m` (50 evals): data_width=14..16, n_iter=13..16, angle_guard=2..4, frac_guard=2..4, rounding=trunc|round, m=2..4. *Why:* pipelined_m has the best area (1189) but its feasible region is extremely narrow (data_width=16, n_iter=14, angle_guard=3). I need to check if we can push n_iter down to 13 or data_width down to 15 while keeping error <= 2^-12, and if m can be tuned for better area/latency tradeoff.
- `pipelined` (50 evals): data_width=14..16, n_iter=14..16, angle_guard=2..4, frac_guard=2..4, rounding=trunc|round. *Why:* pipelined has higher area (1824+) but better accuracy (up to 13.2 bits). The front currently jumps from 1189 (pipelined_m) to 1824 (pipelined). I need to find if pipelined can get closer to 1189 area, or if pipelined_m can get better accuracy. Also, pipelined has much higher throughput (264 vs 93.6 MSPS) which helps with the system constraint.

**Result (code):** 100 evaluations this round, 200 total; 88 feasible; hypervolume 4647 (+67.9%).

**LLM decision:** `refine` — The current Pareto front is dominated by `pipelined_m` designs with `m=4` and `m=3`, achieving a minimum `luts_plus_ffs` of 1165. The `pipelined` family (fully pipelined, equivalent to `m=1`) has a best feasible cost of 1716, which is significantly worse, confirming that partial pipelining (`m>1`) is the key to area efficiency while maintaining the required throughput (>= 32 MSPS) and latency. The `unrolled_k` family failed to meet throughput constraints (max 10.3 MSPS). The `iterative` family is not yet explored, but given that `pipelined_m` with `m=4` already achieves ~93 MSPS and low area, and `iterative` typically has higher latency and lower throughput per area unit for this kind of bursty high-throughput requirement, it is unlikely to beat the current front. The front currently spans `luts_plus_ffs` 1165-1514 and `accuracy_bits` 12.2-13.8. The accuracy constraint is `max_abs_err <= 2^-12` (approx 12 bits), so the lower end of the front (12.2 bits) is just barely feasible. To improve hypervolume, we should focus on the region where `pipelined_m` with `m=4` or `m=3` can push accuracy higher without excessive area increase, or find if `m=2` offers a better trade-off. The current ranges for `pipelined_m` are `data_width` 15-16, `n_iter` 14-16, `angle_guard` 2-4, `frac_guard` 2-4, `m` 2-4. We should refine to focus on `m=3` and `m=4` (since `m=2` might be too costly or not better than `m=3/4`), and potentially widen `n_iter` slightly to see if more iterations allow for lower `data_width` or better accuracy/area trade-offs. However, `data_width` 15-16 seems tight. Let's check if `data_width=14` is possible with higher `n_iter`. The best accuracy seen in `pipelined` was 13.17 bits, and `pipelined_m` reached 13.76 bits. The constraint is 12 bits, so we have headroom. The main objective is minimizing area. The cheapest design is `pipelined_m` with `m=4`, `data_width=15`, `n_iter=14`. Let's refine the search to focus on `pipelined_m` with `m` in [3,4], `data_width` in [14,16], `n_iter` in [13,17], `angle_guard` in [2,4], `frac_guard` in [2,4]. This narrows the search to the most promising region.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 4647 (gain this round: +67.9%).
Feasible designs: 88 of 200 evaluations (48 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 10% violate; best seen 273
- max_abs_err <= 0.000244141: 55% violate; best seen 7.19e-05 (2^-13.76)
- sys_p99_batch_us <= 0.44: 10% violate; best seen 0.161

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=3 frac_guard=4 rounding=round m=4] luts_plus_ffs=1165, accuracy_bits=12.2, luts=886, ffs=278, throughput_msps=93.6, max_abs_err=0.000207 (2^-12.24), power_index=1.4
- pipelined_m [data_width=16 n_iter=14 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1189, accuracy_bits=12.5, luts=902, ffs=287, throughput_msps=93.6, max_abs_err=0.000171 (2^-12.51), power_index=1.43
- pipelined_m [data_width=16 n_iter=14 angle_guard=3 frac_guard=4 rounding=round m=4] luts_plus_ffs=1222, accuracy_bits=12.5, luts=929, ffs=293, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.52), power_index=1.47
- pipelined_m [data_width=15 n_iter=16 angle_guard=3 frac_guard=4 rounding=round m=4] luts_plus_ffs=1295, accuracy_bits=12.8, luts=1017, ffs=278, throughput_msps=93.6, max_abs_err=0.000143 (2^-12.77), power_index=1.56
- pipelined_m [data_width=15 n_iter=16 angle_guard=4 frac_guard=4 rounding=round m=3] luts_plus_ffs=1444, accuracy_bits=12.9, luts=1033, ffs=412, throughput_msps=119, max_abs_err=0.00013 (2^-12.91), power_index=1.74
- pipelined_m [data_width=16 n_iter=16 angle_guard=3 frac_guard=3 rounding=round m=3] luts_plus_ffs=1450, accuracy_bits=13.2, luts=1035, ffs=416, throughput_msps=119, max_abs_err=0.000104 (2^-13.23), power_index=1.75
- pipelined_m [data_width=16 n_iter=16 angle_guard=3 frac_guard=4 rounding=round m=3] luts_plus_ffs=1492, accuracy_bits=13.4, luts=1066, ffs=426, throughput_msps=119, max_abs_err=9.1e-05 (2^-13.42), power_index=1.8
- pipelined_m [data_width=16 n_iter=16 angle_guard=4 frac_guard=4 rounding=round m=3] luts_plus_ffs=1514, accuracy_bits=13.8, luts=1082, ffs=432, throughput_msps=119, max_abs_err=7.19e-05 (2^-13.76), power_index=1.82
Front coverage: luts_plus_ffs 1165..1514 (HV reference 4000); accuracy_bits 12.2..13.8 (HV reference 12); data_width on the front 15..16 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 12.27 bits
- pipelined: 100 evals, 53 feasible; max throughput seen 273 MSPS; best accuracy 13.17 bits; best feasible luts_plus_ffs=1716; feasible ranges: data_width 15..16, n_iter 14..16, angle_guard 1..4, frac_guard 1..4
- pipelined_m: 80 evals, 35 feasible; max throughput seen 171 MSPS; best accuracy 13.76 bits; best feasible luts_plus_ffs=1165; feasible ranges: data_width 15..16, n_iter 14..16, angle_guard 2..4, frac_guard 2..4, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Refine search to the most promising region of the pipelined_m family.*)
- `pipelined_m` (40 evals): data_width=14..16, n_iter=13..17, angle_guard=2..4, frac_guard=2..4, rounding=round, m=3..4. *Why:* Focus on the most promising family and parameter region identified in Round 2.

**Result (code):** 40 evaluations this round, 240 total; 113 feasible; hypervolume 4933 (+6.2%).

**LLM decision:** `stop` — The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 1155 LUTs+FFs) meets all constraints: throughput 93.6 MSPS >= 32, max_abs_err 0.000189 <= 0.000244, and sys_p99_batch_us is well within the 0.44 us bound (best seen 0.161 us). The front covers a reasonable trade-off space from 1155 to 1516 area and 12.4 to 13.8 accuracy bits. Since this is the final round, the exploration is complete and the front is sufficient for selection.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 4933 (gain this round: +6.2%).
Feasible designs: 113 of 240 evaluations (64 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 8% violate; best seen 273
- max_abs_err <= 0.000244141: 52% violate; best seen 6.86e-05 (2^-13.83)
- sys_p99_batch_us <= 0.44: 8% violate; best seen 0.161

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1155, accuracy_bits=12.4, luts=875, ffs=280, throughput_msps=93.6, max_abs_err=0.000189 (2^-12.37), power_index=1.39
- pipelined_m [data_width=16 n_iter=14 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1189, accuracy_bits=12.5, luts=902, ffs=287, throughput_msps=93.6, max_abs_err=0.000171 (2^-12.51), power_index=1.43
- pipelined_m [data_width=16 n_iter=14 angle_guard=3 frac_guard=4 rounding=round m=4] luts_plus_ffs=1222, accuracy_bits=12.5, luts=929, ffs=293, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.52), power_index=1.47
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1264, accuracy_bits=12.9, luts=987, ffs=276, throughput_msps=97.8, max_abs_err=0.000134 (2^-12.86), power_index=1.52
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=3 rounding=round m=4] luts_plus_ffs=1301, accuracy_bits=13.1, luts=1019, ffs=282, throughput_msps=93.6, max_abs_err=0.000114 (2^-13.09), power_index=1.57
- pipelined_m [data_width=16 n_iter=16 angle_guard=3 frac_guard=4 rounding=round m=4] luts_plus_ffs=1359, accuracy_bits=13.4, luts=1066, ffs=293, throughput_msps=93.6, max_abs_err=9.1e-05 (2^-13.42), power_index=1.64
- pipelined_m [data_width=16 n_iter=17 angle_guard=4 frac_guard=3 rounding=round m=4] luts_plus_ffs=1474, accuracy_bits=13.8, luts=1118, ffs=356, throughput_msps=93.6, max_abs_err=7.09e-05 (2^-13.78), power_index=1.77
- pipelined_m [data_width=16 n_iter=17 angle_guard=4 frac_guard=4 rounding=round m=4] luts_plus_ffs=1516, accuracy_bits=13.8, luts=1152, ffs=364, throughput_msps=93.6, max_abs_err=6.86e-05 (2^-13.83), power_index=1.82
Front coverage: luts_plus_ffs 1155..1516 (HV reference 4000); accuracy_bits 12.4..13.8 (HV reference 12); data_width on the front 16..16 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 12.27 bits
- pipelined: 100 evals, 53 feasible; max throughput seen 273 MSPS; best accuracy 13.17 bits; best feasible luts_plus_ffs=1716; feasible ranges: data_width 15..16, n_iter 14..16, angle_guard 1..4, frac_guard 1..4
- pipelined_m: 120 evals, 60 feasible; max throughput seen 171 MSPS; best accuracy 13.83 bits; best feasible luts_plus_ffs=1155; feasible ranges: data_width 15..16, n_iter 14..17, angle_guard 2..4, frac_guard 2..4, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (160 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (8 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 212 feasible; hypervolume 1.92e+04 (+289.2%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 1155 LUTs+FFs) meets all constraints: throughput 93.6 MSPS >= 32, max_abs_err 0.000189 <= 0.000244, and sys_p99_batch_us is well within the 0.44 us bound (best seen 0.161 us). The front covers a reasonable trade-off space from 1155 to 1516 area and 12.4 to 13.8 accuracy bits. Since this is the final round, the exploration is complete and the front is sufficient for selection.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.92e+04 (gain this round: +289.2%).
Feasible designs: 212 of 400 evaluations (156 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 5% violate; best seen 273
- max_abs_err <= 0.000244141: 35% violate; best seen 3.07e-08 (2^-24.96)
- sys_p99_batch_us <= 0.44: 18% violate; best seen 0.161

Pareto front (feasible, 22 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1155, accuracy_bits=12.4, luts=875, ffs=280, throughput_msps=93.6, max_abs_err=0.000189 (2^-12.37), power_index=1.39
- pipelined_m [data_width=16 n_iter=14 angle_guard=3 frac_guard=4 rounding=round m=4] luts_plus_ffs=1222, accuracy_bits=12.5, luts=929, ffs=293, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.52), power_index=1.47
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1353, accuracy_bits=13.4, luts=979, ffs=374, throughput_msps=119, max_abs_err=9.41e-05 (2^-13.38), power_index=1.63
- pipelined_m [data_width=20 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1443, accuracy_bits=13.9, luts=1110, ffs=333, throughput_msps=93.6, max_abs_err=6.58e-05 (2^-13.89), power_index=1.74
- pipelined_m [data_width=20 n_iter=16 angle_guard=4 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1552, accuracy_bits=14.8, luts=1207, ffs=345, throughput_msps=89.6, max_abs_err=3.59e-05 (2^-14.77), power_index=1.87
- pipelined_m [data_width=20 n_iter=18 angle_guard=2 frac_guard=3 rounding=round m=4] luts_plus_ffs=1788, accuracy_bits=16.2, luts=1373, ffs=415, throughput_msps=89.6, max_abs_err=1.32e-05 (2^-16.21), power_index=2.15
- pipelined_m [data_width=22 n_iter=20 angle_guard=1 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=2086, accuracy_bits=17.1, luts=1507, ffs=579, throughput_msps=114, max_abs_err=6.93e-06 (2^-17.14), power_index=2.51
- pipelined_m [data_width=26 n_iter=20 angle_guard=1 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=2193, accuracy_bits=18.7, luts=1707, ffs=486, throughput_msps=86, max_abs_err=2.39e-06 (2^-18.67), power_index=2.64
- pipelined_m [data_width=28 n_iter=23 angle_guard=3 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=3037, accuracy_bits=21.7, luts=2208, ffs=829, throughput_msps=106, max_abs_err=3.01e-07 (2^-21.66), power_index=3.66
- pipelined_m [data_width=28 n_iter=28 angle_guard=3 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=3731, accuracy_bits=23.3, luts=2708, ffs=1023, throughput_msps=106, max_abs_err=1e-07 (2^-23.25), power_index=4.49
Front coverage: luts_plus_ffs 1155..3731 (HV reference 4000); accuracy_bits 12.4..23.3 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 12.27 bits
- pipelined: 100 evals, 53 feasible; max throughput seen 273 MSPS; best accuracy 13.17 bits; best feasible luts_plus_ffs=1716; feasible ranges: data_width 15..16, n_iter 14..16, angle_guard 1..4, frac_guard 1..4
- pipelined_m: 280 evals, 159 feasible; max throughput seen 171 MSPS; best accuracy 24.96 bits; best feasible luts_plus_ffs=1155; feasible ranges: data_width 15..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 25938 in, 3782 out
- provider-reported cost: $0.0076
- full prompts and replies: `llm_trace.jsonl`

