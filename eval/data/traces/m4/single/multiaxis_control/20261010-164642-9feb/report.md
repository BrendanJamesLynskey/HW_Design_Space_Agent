# DSE run: multiaxis_control

**Verdict:** converged: hypervolume gain fell below epsilon.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 3 round(s).  
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
`pipelined_m:data_width=19,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 882 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 301 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.42 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000145 (2^-12.76) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 18.9 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.05e-05 (2^-14.27) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 6.62 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.8 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 96.0 dBc, SNR 83.0 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Every L1-feasible design (182) was simulated at its estimated Fmax (SimPy); 179 pass. Top 5 by the selection rule, L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=19,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=20,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=16,angle_guard=-1,frac_guard=0,rounding=round,m=3` | 0.3053 → 0.3133 | yes |
| `pipelined_m:data_width=18,n_iter=14,angle_guard=4,frac_guard=0,rounding=round,m=2` | 0.2373 → 0.2433 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (26 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=4` | 882 | 301 | 93.6 | 6 | 1.42 | 0.000145 (2^-12.76) | 12.76 |
| 1 | `pipelined_m:data_width=20,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1006 | 327 | 93.6 | 6 | 1.6 | 0.000127 (2^-12.95) | 12.95 |
| 2 | `pipelined_m:data_width=19,n_iter=16,angle_guard=0,frac_guard=1,rounding=round,m=4` | 1073 | 305 | 93.6 | 6 | 1.66 | 7.36e-05 (2^-13.73) | 13.73 |
| 3 | `pipelined_m:data_width=20,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 1080 | 317 | 93.6 | 6 | 1.68 | 5.62e-05 (2^-14.12) | 14.12 |
| 4 | `pipelined_m:data_width=19,n_iter=16,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1089 | 309 | 93.6 | 6 | 1.68 | 5.25e-05 (2^-14.22) | 14.22 |
| 5 | `pipelined_m:data_width=19,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1096 | 317 | 93.6 | 6 | 1.7 | 4.81e-05 (2^-14.34) | 14.34 |
| 6 | `pipelined_m:data_width=20,n_iter=16,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1138 | 323 | 93.6 | 6 | 1.76 | 4.05e-05 (2^-14.59) | 14.59 |
| 7 | `pipelined_m:data_width=23,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=4` | 1207 | 357 | 89.6 | 6 | 1.88 | 3.16e-05 (2^-14.95) | 14.95 |
| 8 | `pipelined_m:data_width=20,n_iter=17,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 1185 | 397 | 93.6 | 7 | 1.9 | 3.13e-05 (2^-14.96) | 14.96 |
| 9 | `pipelined_m:data_width=23,n_iter=16,angle_guard=1,frac_guard=4,rounding=round,m=4` | 1381 | 383 | 86.0 | 6 | 2.12 | 3.12e-05 (2^-14.97) | 14.97 |
| 10 | `pipelined_m:data_width=18,n_iter=18,angle_guard=4,frac_guard=4,rounding=trunc,m=3` | 1295 | 470 | 119.3 | 8 | 2.12 | 3.07e-05 (2^-14.99) | 14.99 |
| 11 | `pipelined_m:data_width=21,n_iter=18,angle_guard=3,frac_guard=3,rounding=trunc,m=4` | 1403 | 435 | 89.6 | 7 | 2.21 | 1.08e-05 (2^-16.50) | 16.50 |
| 12 | `pipelined_m:data_width=25,n_iter=18,angle_guard=0,frac_guard=2,rounding=round,m=3` | 1581 | 569 | 110.0 | 8 | 2.59 | 8.06e-06 (2^-16.92) | 16.92 |
| 13 | `pipelined_m:data_width=26,n_iter=18,angle_guard=4,frac_guard=0,rounding=trunc,m=3` | 1582 | 591 | 110.0 | 8 | 2.62 | 7.87e-06 (2^-16.96) | 16.96 |
| 14 | `pipelined_m:data_width=25,n_iter=20,angle_guard=-2,frac_guard=2,rounding=round,m=4` | 1720 | 472 | 86.0 | 7 | 2.64 | 4.28e-06 (2^-17.84) | 17.84 |
| 15 | `pipelined_m:data_width=27,n_iter=20,angle_guard=0,frac_guard=1,rounding=trunc,m=3` | 1787 | 688 | 110.0 | 9 | 2.98 | 2.08e-06 (2^-18.87) | 18.87 |
| 16 | `pipelined_m:data_width=26,n_iter=21,angle_guard=-1,frac_guard=3,rounding=trunc,m=3` | 1881 | 682 | 110.0 | 9 | 3.09 | 1.58e-06 (2^-19.27) | 19.27 |
| 17 | `pipelined_m:data_width=25,n_iter=24,angle_guard=0,frac_guard=0,rounding=round,m=3` | 1968 | 712 | 114.5 | 10 | 3.23 | 1.37e-06 (2^-19.48) | 19.48 |
| 18 | `pipelined_m:data_width=27,n_iter=21,angle_guard=4,frac_guard=3,rounding=trunc,m=3` | 2050 | 741 | 105.9 | 9 | 3.36 | 9.92e-07 (2^-19.94) | 19.94 |
| 19 | `pipelined_m:data_width=25,n_iter=22,angle_guard=4,frac_guard=3,rounding=trunc,m=3` | 2019 | 787 | 110.0 | 10 | 3.38 | 6.88e-07 (2^-20.47) | 20.47 |
| 20 | `pipelined_m:data_width=27,n_iter=22,angle_guard=4,frac_guard=3,rounding=trunc,m=3` | 2152 | 839 | 105.9 | 10 | 3.6 | 5.17e-07 (2^-20.88) | 20.88 |
| 21 | `pipelined_m:data_width=26,n_iter=24,angle_guard=4,frac_guard=3,rounding=trunc,m=2` | 2283 | 1197 | 152.6 | 14 | 4.19 | 2.28e-07 (2^-22.06) | 22.06 |
| 22 | `pipelined:data_width=28,n_iter=24,angle_guard=3,frac_guard=4,rounding=trunc` | 2453 | 2454 | 242.0 | 26 | 5.91 | 1.43e-07 (2^-22.74) | 22.74 |
| 23 | `pipelined:data_width=28,n_iter=28,angle_guard=3,frac_guard=1,rounding=trunc` | 2708 | 2708 | 242.0 | 30 | 6.52 | 1e-07 (2^-23.25) | 23.25 |
| 24 | `pipelined:data_width=28,n_iter=28,angle_guard=3,frac_guard=4,rounding=trunc` | 2879 | 2865 | 242.0 | 30 | 6.91 | 3.75e-08 (2^-24.67) | 24.67 |
| 25 | `pipelined:data_width=28,n_iter=28,angle_guard=4,frac_guard=3,rounding=round` | 2909 | 2843 | 242.0 | 30 | 6.92 | 2.42e-08 (2^-25.30) | 25.30 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The hard constraints (throughput_msps >= 32 and sys_p99_batch_us <= 0.44) are throughput/latency constraints that only the 1-result/cycle families can meet; iterative and unrolled_k emit one result every several cycles and would be screened out, so I exclude them to spend the full 400-eval budget on the two feasible families. I focus the search on the accuracy/area trade-off: data_width 14-20 and n_iter 12-18 bracket the region where max_abs_err crosses the 2^-12 bound (accuracy_bits ~12-14), which is exactly where the min-luts_plus_ffs objective and the max-accuracy_bits objective pull in opposite directions. angle_guard 0-2 and frac_guard 0-2 give the small accuracy/area levers without wasting budget on wide guards that only inflate area. Rounding is left to both options since it is a cheap accuracy/area toggle. The two families are searched with equal weight because pipelined anchors the baseline and pipelined_m adds the FF/Fmax trade-off dimension; together they should map the feasible Pareto front over the spec's objectives. The front will then be screened at L1 and the shortlist simulated at L2 for the 0.44 us batch deadline.*)
- `pipelined` (50 evals): data_width=14..20, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* The spec demands 32 results/us (32 MS/s) and a 0.44 us p99 batch deadline. Only the 1-result/cycle families (pipelined, pipelined_m) can plausibly sustain 32 MS/s on Artix-7; iterative/unrolled_k emit one result every several cycles and will fail the throughput and batch constraints. pipelined is the baseline 1/cycle family with the simplest datapath, so it anchors the area/accuracy trade-off. data_width 14-20 and n_iter 12-18 span the region where max_abs_err crosses the 2^-12 bound (accuracy_bits ~12-14), keeping the search on the feasible accuracy side while exposing the area/accuracy trade-off that drives luts_plus_ffs.
- `pipelined_m` (50 evals): data_width=14..20, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* pipelined_m also delivers 1 result/cycle but registers every m stages, trading latency (ceil(N/m)+2) for fewer FFs and a shorter critical path (higher Fmax). Since the objective is min luts_plus_ffs and the batch deadline (0.44 us) is tight, the m knob lets the search find lower-FF / higher-Fmax points that pipelined cannot reach, directly improving the Pareto front on the area axis. Same accuracy-relevant ranges as pipelined so the two families are comparable on the accuracy axis.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 64 feasible; hypervolume 8855 (n/a).

**LLM decision:** `add_family` — The current front is well-covered by pipelined_m (low area) and pipelined (high accuracy), but unrolled_k remains unexplored. Since unrolled_k shares the FSM with iterative but processes k rotations per cycle, it may achieve similar throughput to pipelined_m with lower area (fewer registers than full pipelining) or better accuracy for the same area. Adding it with a 50% budget share (50 evals) centered on the known feasible region is the most likely way to improve hypervolume before the reserved front-mapping round.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 8855 (gain this round: n/a (first round)).
Feasible designs: 64 of 100 evaluations (45 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 25% violate; best seen 1.92e-05 (2^-15.67)
- sys_p99_batch_us <= 0.44: 16% violate; best seen 0.161

Pareto front (feasible, 12 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1183, accuracy_bits=12.8, luts=882, ffs=301, throughput_msps=93.6, max_abs_err=0.000145 (2^-12.76), power_index=1.42
- pipelined_m [data_width=20 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1333, accuracy_bits=12.9, luts=1006, ffs=327, throughput_msps=93.6, max_abs_err=0.000127 (2^-12.95), power_index=1.6
- pipelined_m [data_width=19 n_iter=16 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=1377, accuracy_bits=13.7, luts=1073, ffs=305, throughput_msps=93.6, max_abs_err=7.36e-05 (2^-13.73), power_index=1.66
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1397, accuracy_bits=14.2, luts=1089, ffs=309, throughput_msps=93.6, max_abs_err=5.25e-05 (2^-14.22), power_index=1.68
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1413, accuracy_bits=14.3, luts=1096, ffs=317, throughput_msps=93.6, max_abs_err=4.81e-05 (2^-14.34), power_index=1.7
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1461, accuracy_bits=14.6, luts=1138, ffs=323, throughput_msps=93.6, max_abs_err=4.05e-05 (2^-14.59), power_index=1.76
- pipelined_m [data_width=20 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1582, accuracy_bits=15, luts=1185, ffs=397, throughput_msps=93.6, max_abs_err=3.13e-05 (2^-14.96), power_index=1.9
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=2463, accuracy_bits=15.2, luts=1219, ffs=1244, throughput_msps=264, max_abs_err=2.57e-05 (2^-15.25), power_index=2.96
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2547, accuracy_bits=15.4, luts=1281, ffs=1265, throughput_msps=264, max_abs_err=2.34e-05 (2^-15.38), power_index=3.07
- pipelined [data_width=20 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=2613, accuracy_bits=15.7, luts=1295, ffs=1318, throughput_msps=264, max_abs_err=1.92e-05 (2^-15.67), power_index=3.14
Front coverage: luts_plus_ffs 1183..2613 (HV reference 4000); accuracy_bits 12.8..15.7 (HV reference 12); data_width on the front 19..20 (registry 8..28).

Per family:
- pipelined: 50 evals, 41 feasible; max throughput seen 273 MSPS; best accuracy 15.67 bits; best feasible luts_plus_ffs=1764; feasible ranges: data_width 17..20, n_iter 14..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 23 feasible; max throughput seen 171 MSPS; best accuracy 15.36 bits; best feasible luts_plus_ffs=1183; feasible ranges: data_width 18..20, n_iter 14..18, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The current front is well-covered by pipelined_m (low area) and pipelined (high accuracy), but unrolled_k remains unexplored. Since unrolled_k shares the FSM with iterative but processes k rotations per cycle, it may achieve similar throughput to pipelined_m with lower area (fewer registers than full pipelining) or better accuracy for the same area. Adding it with a 50% budget share (50 evals) centered on the known feasible region is the most likely way to improve hypervolume before the reserved front-mapping round.*)
- `unrolled_k` (100 evals): data_width=16..20, n_iter=12..18, angle_guard=-2..2, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* pipelined_m already achieves the minimum area (1183) and meets throughput (93.6 MSPS >= 32) and accuracy (12.8 bits >= 12). However, unrolled_k has not been explored and may offer a better area/accuracy trade-off by chaining micro-rotations (k>1) without the full register overhead of pipelined_m. The current front is dominated by pipelined_m at the low-area end and pipelined at the high-accuracy end; unrolled_k could potentially fill the gap or push the area lower for a given accuracy, improving hypervolume. The ranges are centered on the known feasible region (data_width 16-20, n_iter 12-18) to focus the budget.

**Result (code):** 100 evaluations this round, 200 total; 64 feasible; hypervolume 8855 (+0.0%).

**LLM decision:** `refine` — The current Pareto front is dominated by `pipelined_m` designs with `m=4` (e.g., 1183 LUTs+FFs at 12.8 bits), which significantly outperform the fully pipelined `pipelined` family (min 1764 LUTs+FFs) and the infeasible `unrolled_k` family. The `pipelined_m` family achieves the required throughput (93.6 MSPS > 32 MSPS) and accuracy constraints with much lower area due to reduced register overhead. The current front spans 1183-2613 LUTs+FFs, but the lower bound (1183) is likely not fully optimized because the search space for `pipelined_m` was broad (m=2..8, n_iter=4..30). The best feasible `pipelined_m` designs cluster around `data_width=19-20`, `n_iter=14-17`, `angle_guard=1-2`, `frac_guard=0-2`, and `m=4`. To improve hypervolume and find the true minimum area, we should narrow the search to this promising region and specifically focus on `pipelined_m` with `m` constrained to 3-5 (since m=4 is best, m=2/3 might offer better area/latency trade-offs, and m>4 increases latency which hurts the p99 batch constraint). We should also exclude `pipelined` and `unrolled_k` from the next round as they are clearly inferior or infeasible for this spec.
- **rule applied by code:** 'refine' overridden to stop: HV gain 0.00% < epsilon 1.00%
- **rule applied by code:** code: before stopping (converged), one front-mapping round with the remaining 200 evaluations
- effective decision: `stop`

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 8855 (gain this round: +0.0%).
Feasible designs: 64 of 200 evaluations (45 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 50% violate; best seen 273
- max_abs_err <= 0.000244141: 34% violate; best seen 1.92e-05 (2^-15.67)
- sys_p99_batch_us <= 0.44: 58% violate; best seen 0.161

Pareto front (feasible, 12 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1183, accuracy_bits=12.8, luts=882, ffs=301, throughput_msps=93.6, max_abs_err=0.000145 (2^-12.76), power_index=1.42
- pipelined_m [data_width=20 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1333, accuracy_bits=12.9, luts=1006, ffs=327, throughput_msps=93.6, max_abs_err=0.000127 (2^-12.95), power_index=1.6
- pipelined_m [data_width=19 n_iter=16 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=1377, accuracy_bits=13.7, luts=1073, ffs=305, throughput_msps=93.6, max_abs_err=7.36e-05 (2^-13.73), power_index=1.66
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1397, accuracy_bits=14.2, luts=1089, ffs=309, throughput_msps=93.6, max_abs_err=5.25e-05 (2^-14.22), power_index=1.68
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1413, accuracy_bits=14.3, luts=1096, ffs=317, throughput_msps=93.6, max_abs_err=4.81e-05 (2^-14.34), power_index=1.7
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1461, accuracy_bits=14.6, luts=1138, ffs=323, throughput_msps=93.6, max_abs_err=4.05e-05 (2^-14.59), power_index=1.76
- pipelined_m [data_width=20 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1582, accuracy_bits=15, luts=1185, ffs=397, throughput_msps=93.6, max_abs_err=3.13e-05 (2^-14.96), power_index=1.9
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=2463, accuracy_bits=15.2, luts=1219, ffs=1244, throughput_msps=264, max_abs_err=2.57e-05 (2^-15.25), power_index=2.96
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2547, accuracy_bits=15.4, luts=1281, ffs=1265, throughput_msps=264, max_abs_err=2.34e-05 (2^-15.38), power_index=3.07
- pipelined [data_width=20 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=2613, accuracy_bits=15.7, luts=1295, ffs=1318, throughput_msps=264, max_abs_err=1.92e-05 (2^-15.67), power_index=3.14
Front coverage: luts_plus_ffs 1183..2613 (HV reference 4000); accuracy_bits 12.8..15.7 (HV reference 12); data_width on the front 19..20 (registry 8..28).

Per family:
- unrolled_k: 100 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 15.28 bits
- pipelined: 50 evals, 41 feasible; max throughput seen 273 MSPS; best accuracy 15.67 bits; best feasible luts_plus_ffs=1764; feasible ranges: data_width 17..20, n_iter 14..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 23 feasible; max throughput seen 171 MSPS; best accuracy 15.36 bits; best feasible luts_plus_ffs=1183; feasible ranges: data_width 18..20, n_iter 14..18, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 200 evaluations*)
- `pipelined_m` (134 evals): data_width=18..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (8 front designs; box front_anchored)
- `pipelined` (66 evals): data_width=18..28, n_iter=15..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (4 front designs; box front_anchored)

**Result (code):** 200 evaluations this round, 400 total; 218 feasible; hypervolume 1.823e+04 (+105.9%).

**No LLM call** (code's front-mapping round): The current Pareto front is dominated by `pipelined_m` designs with `m=4` (e.g., 1183 LUTs+FFs at 12.8 bits), which significantly outperform the fully pipelined `pipelined` family (min 1764 LUTs+FFs) and the infeasible `unrolled_k` family. The `pipelined_m` family achieves the required throughput (93.6 MSPS > 32 MSPS) and accuracy constraints with much lower area due to reduced register overhead. The current front spans 1183-2613 LUTs+FFs, but the lower bound (1183) is likely not fully optimized because the search space for `pipelined_m` was broad (m=2..8, n_iter=4..30). The best feasible `pipelined_m` designs cluster around `data_width=19-20`, `n_iter=14-17`, `angle_guard=1-2`, `frac_guard=0-2`, and `m=4`. To improve hypervolume and find the true minimum area, we should narrow the search to this promising region and specifically focus on `pipelined_m` with `m` constrained to 3-5 (since m=4 is best, m=2/3 might offer better area/latency trade-offs, and m>4 increases latency which hurts the p99 batch constraint). We should also exclude `pipelined` and `unrolled_k` from the next round as they are clearly inferior or infeasible for this spec.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.823e+04 (gain this round: +105.9%).
Feasible designs: 218 of 400 evaluations (182 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 25% violate; best seen 273
- max_abs_err <= 0.000244141: 18% violate; best seen 2.42e-08 (2^-25.30)
- sys_p99_batch_us <= 0.44: 40% violate; best seen 0.161

Pareto front (feasible, 26 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1183, accuracy_bits=12.8, luts=882, ffs=301, throughput_msps=93.6, max_abs_err=0.000145 (2^-12.76), power_index=1.42
- pipelined_m [data_width=20 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1397, accuracy_bits=14.1, luts=1080, ffs=317, throughput_msps=93.6, max_abs_err=5.62e-05 (2^-14.12), power_index=1.68
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1461, accuracy_bits=14.6, luts=1138, ffs=323, throughput_msps=93.6, max_abs_err=4.05e-05 (2^-14.59), power_index=1.76
- pipelined_m [data_width=20 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1582, accuracy_bits=15, luts=1185, ffs=397, throughput_msps=93.6, max_abs_err=3.13e-05 (2^-14.96), power_index=1.9
- pipelined_m [data_width=21 n_iter=18 angle_guard=3 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1837, accuracy_bits=16.5, luts=1403, ffs=435, throughput_msps=89.6, max_abs_err=1.08e-05 (2^-16.50), power_index=2.21
- pipelined_m [data_width=25 n_iter=20 angle_guard=-2 frac_guard=2 rounding=round m=4] luts_plus_ffs=2192, accuracy_bits=17.8, luts=1720, ffs=472, throughput_msps=86, max_abs_err=4.28e-06 (2^-17.84), power_index=2.64
- pipelined_m [data_width=25 n_iter=24 angle_guard=0 frac_guard=0 rounding=round m=3] luts_plus_ffs=2681, accuracy_bits=19.5, luts=1968, ffs=712, throughput_msps=114, max_abs_err=1.37e-06 (2^-19.48), power_index=3.23
- pipelined_m [data_width=25 n_iter=22 angle_guard=4 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=2806, accuracy_bits=20.5, luts=2019, ffs=787, throughput_msps=110, max_abs_err=6.88e-07 (2^-20.47), power_index=3.38
- pipelined [data_width=28 n_iter=24 angle_guard=3 frac_guard=4 rounding=trunc] luts_plus_ffs=4907, accuracy_bits=22.7, luts=2453, ffs=2454, throughput_msps=242, max_abs_err=1.43e-07 (2^-22.74), power_index=5.91
- pipelined [data_width=28 n_iter=28 angle_guard=4 frac_guard=3 rounding=round] luts_plus_ffs=5753, accuracy_bits=25.3, luts=2909, ffs=2843, throughput_msps=242, max_abs_err=2.42e-08 (2^-25.30), power_index=6.92
Front coverage: luts_plus_ffs 1183..5753 (HV reference 4000); accuracy_bits 12.8..25.3 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- unrolled_k: 100 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 15.28 bits
- pipelined: 116 evals, 107 feasible; max throughput seen 273 MSPS; best accuracy 25.30 bits; best feasible luts_plus_ffs=1764; feasible ranges: data_width 17..28, n_iter 14..30, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 184 evals, 111 feasible; max throughput seen 171 MSPS; best accuracy 23.05 bits; best feasible luts_plus_ffs=1183; feasible ranges: data_width 18..28, n_iter 14..29, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 9189 in, 2562 out
- provider-reported cost: $0.0059
- full prompts and replies: `llm_trace.jsonl`

