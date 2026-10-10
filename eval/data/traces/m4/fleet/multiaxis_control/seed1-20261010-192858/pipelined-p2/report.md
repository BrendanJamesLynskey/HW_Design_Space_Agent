# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
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
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=18,n_iter=16,angle_guard=-1,frac_guard=0,rounding=round,m=3` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 938 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 400 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 124 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 124 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 8 | exact: schedule |
| latency_ns | 64.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.61 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000192 (2^-12.35) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 12.6 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 4.31e-05 (2^-14.50) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 2.82 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (20 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=16,angle_guard=-1,frac_guard=0,rounding=round,m=3` | 938 | 400 | 124.5 | 8 | 1.61 | 0.000192 (2^-12.35) | 12.35 |
| 1 | `pipelined_m:data_width=19,n_iter=14,angle_guard=-1,frac_guard=2,rounding=trunc,m=2` | 909 | 507 | 164.4 | 9 | 1.71 | 0.00018 (2^-12.44) | 12.44 |
| 2 | `pipelined_m:data_width=19,n_iter=18,angle_guard=3,frac_guard=0,rounding=round,m=4` | 1188 | 376 | 93.6 | 7 | 1.88 | 3.74e-05 (2^-14.71) | 14.71 |
| 3 | `pipelined_m:data_width=24,n_iter=16,angle_guard=-1,frac_guard=0,rounding=round,m=3` | 1222 | 521 | 114.5 | 8 | 2.1 | 3.2e-05 (2^-14.93) | 14.93 |
| 4 | `pipelined_m:data_width=19,n_iter=18,angle_guard=2,frac_guard=4,rounding=round,m=3` | 1353 | 480 | 114.5 | 8 | 2.21 | 2.09e-05 (2^-15.55) | 15.55 |
| 5 | `pipelined_m:data_width=22,n_iter=18,angle_guard=-1,frac_guard=4,rounding=round,m=4` | 1467 | 442 | 89.6 | 7 | 2.3 | 1.78e-05 (2^-15.77) | 15.77 |
| 6 | `pipelined_m:data_width=24,n_iter=18,angle_guard=3,frac_guard=0,rounding=round,m=4` | 1456 | 462 | 86.0 | 7 | 2.31 | 8.29e-06 (2^-16.88) | 16.88 |
| 7 | `pipelined_m:data_width=24,n_iter=18,angle_guard=4,frac_guard=0,rounding=round,m=4` | 1474 | 467 | 86.0 | 7 | 2.34 | 8.26e-06 (2^-16.88) | 16.88 |
| 8 | `pipelined_m:data_width=22,n_iter=18,angle_guard=3,frac_guard=4,rounding=round,m=4` | 1538 | 462 | 89.6 | 7 | 2.41 | 8.25e-06 (2^-16.89) | 16.89 |
| 9 | `pipelined_m:data_width=26,n_iter=18,angle_guard=3,frac_guard=4,rounding=round,m=4` | 1762 | 531 | 86.0 | 7 | 2.76 | 7.68e-06 (2^-16.99) | 16.99 |
| 10 | `pipelined_m:data_width=22,n_iter=20,angle_guard=2,frac_guard=4,rounding=round,m=3` | 1693 | 625 | 114.5 | 9 | 2.79 | 3.57e-06 (2^-18.10) | 18.10 |
| 11 | `pipelined_m:data_width=23,n_iter=20,angle_guard=2,frac_guard=3,rounding=round,m=3` | 1716 | 636 | 114.5 | 9 | 2.83 | 2.65e-06 (2^-18.53) | 18.53 |
| 12 | `pipelined_m:data_width=25,n_iter=23,angle_guard=-1,frac_guard=0,rounding=round,m=4` | 1860 | 541 | 89.6 | 8 | 2.89 | 2e-06 (2^-18.93) | 18.93 |
| 13 | `pipelined_m:data_width=24,n_iter=23,angle_guard=4,frac_guard=0,rounding=round,m=3` | 1906 | 718 | 110.0 | 10 | 3.16 | 1.62e-06 (2^-19.24) | 19.24 |
| 14 | `pipelined_m:data_width=24,n_iter=24,angle_guard=2,frac_guard=0,rounding=round,m=3` | 1944 | 702 | 114.5 | 10 | 3.19 | 1.57e-06 (2^-19.28) | 19.28 |
| 15 | `pipelined_m:data_width=25,n_iter=23,angle_guard=2,frac_guard=0,rounding=round,m=3` | 1929 | 728 | 110.0 | 10 | 3.2 | 8.71e-07 (2^-20.13) | 20.13 |
| 16 | `pipelined_m:data_width=26,n_iter=23,angle_guard=4,frac_guard=1,rounding=round,m=3` | 2146 | 787 | 110.0 | 10 | 3.53 | 3.97e-07 (2^-21.26) | 21.26 |
| 17 | `pipelined_m:data_width=28,n_iter=23,angle_guard=0,frac_guard=4,rounding=round,m=3` | 2336 | 850 | 105.9 | 10 | 3.83 | 3.13e-07 (2^-21.61) | 21.61 |
| 18 | `pipelined_m:data_width=28,n_iter=28,angle_guard=-1,frac_guard=4,rounding=round,m=3` | 2824 | 1039 | 105.9 | 12 | 4.65 | 2.49e-07 (2^-21.94) | 21.94 |
| 19 | `pipelined_m:data_width=26,n_iter=27,angle_guard=3,frac_guard=4,rounding=trunc,m=2` | 2608 | 1400 | 152.6 | 16 | 4.82 | 1.42e-07 (2^-22.74) | 22.74 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Both my families deliver 1 result/cycle, so throughput_msps>=32 is easy; the real fights are max_abs_err<=2^-12 (forces data_width>=~14 and n_iter>=~13) and sys_p99_batch_us<=0.44 (32 back-to-back results must drain in 0.44us, i.e. latency+31 cycles at Fmax, so Fmax and low N matter). pipelined is the safe, high-Fmax family and pipelined_m is the low-FF family that currently holds the cheapest front points, so I split the round roughly evenly, biasing slightly to pipelined_m to map its narrow feasible band (small m). Ranges are centred on the minimum (W,N) that can meet 12-bit accuracy and extended upward to keep covering the accuracy end of the hypervolume, while guards are kept small since they only add area. Because the L1 system bound is optimistic, I keep N low enough that the resulting Fmax has margin over the batch requirement rather than sitting exactly on it.*)
- `pipelined` (45 evals): data_width=13..19, n_iter=11..18, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Round 1 made pipelined the robustly feasible family (48/55 feasible, 6/14 front designs, best area 1848). The binding constraints are accuracy (needs W>=~14 and N>=~13) and the 32-request/0.44us batch (needs high Fmax, so low latency N+2). I search the low-area corner W 13-19 / N 11-18 with small guards, plus a few higher-accuracy points to extend the front toward the HV reference.
- `pipelined_m` (55 evals): data_width=13..19, n_iter=11..18, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, m=2..5. *Why:* pipelined_m owns the area-efficient end of the merged front (8/14 designs, best area 1335) but only 9/45 were feasible, so its feasible region is under-mapped. Registering every m stages cuts FFs but lengthens the combinational path and lowers Fmax, which is exactly what the 0.44us batch bound punishes; I therefore restrict m to 2-5 (small m keeps Fmax up) and search the same accuracy box so the cheapest feasible design can be found.

**Result (code):** 100 evaluations this round, 100 total; 25 feasible; hypervolume 6104 (n/a).

**LLM decision:** `map_front` — The feasible front is very narrow: only 3 designs, all pipelined_m with data_width pinned at 19, spanning luts_plus_ffs 1417..1884 against an HV reference of 4000 and accuracy_bits 12.4..14.6 against a reference of 12. It covers only a small slice of the area objective's range and none of the data_width range (registry 8..28), so hypervolume is leaving large regions unmapped. Meanwhile pipelined alone produced 21 feasible designs (best luts_plus_ffs=1772, best accuracy 14.53 bits) yet contributes nothing to the front, and pipelined_m had only 4 feasible of 55 evals — both families clearly have unexplored feasible territory (e.g. smaller data_width with more n_iter could be cheaper while still meeting max_abs_err<=2^-12). With 100 evals and 3 rounds remaining, spending this round on a seeded NSGA-II over the full ranges of the two families already on the front (pipelined, pipelined_m) is the right way to widen coverage of the trade-off curve before any refinement. Constraints are not the blocker: throughput (best 282 vs 32) and sys_p99_batch_us (best 0.158 vs 0.44) have ample margin, and accuracy is reachable (best 2^-14.61), so the front is feasible and worth mapping, not infeasible.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 6104 (gain this round: n/a (first round)).
Feasible designs: 25 of 100 evaluations (19 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 63% violate; best seen 3.99e-05 (2^-14.61)
- sys_p99_batch_us <= 0.44: 20% violate; best seen 0.158

Pareto front (feasible, 3 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=2 rounding=trunc m=2] luts_plus_ffs=1417, accuracy_bits=12.4, luts=909, ffs=507, throughput_msps=164, max_abs_err=0.00018 (2^-12.44), power_index=1.71
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=2] luts_plus_ffs=1671, accuracy_bits=14.2, luts=1080, ffs=591, throughput_msps=164, max_abs_err=5.43e-05 (2^-14.17), power_index=2.01
- pipelined_m [data_width=19 n_iter=18 angle_guard=1 frac_guard=2 rounding=trunc m=2] luts_plus_ffs=1884, accuracy_bits=14.6, luts=1223, ffs=661, throughput_msps=164, max_abs_err=3.99e-05 (2^-14.61), power_index=2.27
Front coverage: luts_plus_ffs 1417..1884 (HV reference 4000); accuracy_bits 12.4..14.6 (HV reference 12); data_width on the front 19..19 (registry 8..28).

Per family:
- pipelined: 45 evals, 21 feasible; max throughput seen 282 MSPS; best accuracy 14.53 bits; best feasible luts_plus_ffs=1772; feasible ranges: data_width 17..19, n_iter 14..17, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 55 evals, 4 feasible; max throughput seen 178 MSPS; best accuracy 14.61 bits; best feasible luts_plus_ffs=1417; feasible ranges: data_width 18..19, n_iter 14..18, angle_guard -1..1, frac_guard 1..2, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `pipelined_m` (20 evals): data_width=18..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (3 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 41 feasible; hypervolume 1.386e+04 (+127.2%).

**LLM decision:** `map_front` — The feasible front already spans nearly the whole objective box — luts_plus_ffs 1417..4008 against HV ref 4000 and accuracy_bits 12.4..22.7 against HV ref 12 — and this round's hypervolume jumped +127%, so the promising region is found and both families on the front (pipelined, pipelined_m) are known. With 80 of 200 evals left and 2 rounds, the best use is the reserved coverage pass: NSGA-II over the full registry ranges of the front families, seeded with the current front, to fill any interior gaps and probe the cheap end (best feasible 1417, pipelined_m data_width=19/n_iter=14/m=2) that the min-luts_plus_ffs selection rule cares about. Note iterative and unrolled_k cannot meet the 32-requests-in-0.44us batch bound (they emit one result every several cycles), so the front is correctly confined to the 1-result/cycle families.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.386e+04 (gain this round: +127.2%).
Feasible designs: 41 of 120 evaluations (35 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 52% violate; best seen 1.42e-07 (2^-22.74)
- sys_p99_batch_us <= 0.44: 20% violate; best seen 0.158

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=2 rounding=trunc m=2] luts_plus_ffs=1417, accuracy_bits=12.4, luts=909, ffs=507, throughput_msps=164, max_abs_err=0.00018 (2^-12.44), power_index=1.71
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=2] luts_plus_ffs=1671, accuracy_bits=14.2, luts=1080, ffs=591, throughput_msps=164, max_abs_err=5.43e-05 (2^-14.17), power_index=2.01
- pipelined_m [data_width=23 n_iter=16 angle_guard=-1 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=1842, accuracy_bits=14.8, luts=1301, ffs=541, throughput_msps=110, max_abs_err=3.42e-05 (2^-14.84), power_index=2.22
- pipelined_m [data_width=22 n_iter=20 angle_guard=-2 frac_guard=4 rounding=round m=3] luts_plus_ffs=2210, accuracy_bits=15.2, luts=1613, ffs=596, throughput_msps=114, max_abs_err=2.69e-05 (2^-15.18), power_index=2.66
- pipelined_m [data_width=22 n_iter=20 angle_guard=2 frac_guard=4 rounding=round m=3] luts_plus_ffs=2318, accuracy_bits=18.1, luts=1693, ffs=625, throughput_msps=114, max_abs_err=3.57e-06 (2^-18.10), power_index=2.79
- pipelined_m [data_width=26 n_iter=20 angle_guard=0 frac_guard=1 rounding=round m=2] luts_plus_ffs=2712, accuracy_bits=18.7, luts=1782, ffs=930, throughput_msps=153, max_abs_err=2.36e-06 (2^-18.69), power_index=3.26
- pipelined_m [data_width=25 n_iter=20 angle_guard=2 frac_guard=3 rounding=round m=2] luts_plus_ffs=2794, accuracy_bits=18.9, luts=1840, ffs=954, throughput_msps=153, max_abs_err=2.06e-06 (2^-18.89), power_index=3.36
- pipelined_m [data_width=23 n_iter=27 angle_guard=2 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=3506, accuracy_bits=19.3, luts=2279, ffs=1227, throughput_msps=158, max_abs_err=1.54e-06 (2^-19.31), power_index=4.22
- pipelined_m [data_width=28 n_iter=29 angle_guard=-1 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=3904, accuracy_bits=21.9, luts=2867, ffs=1037, throughput_msps=106, max_abs_err=2.49e-07 (2^-21.94), power_index=4.7
- pipelined_m [data_width=26 n_iter=27 angle_guard=3 frac_guard=4 rounding=trunc m=2] luts_plus_ffs=4008, accuracy_bits=22.7, luts=2608, ffs=1400, throughput_msps=153, max_abs_err=1.42e-07 (2^-22.74), power_index=4.82
Front coverage: luts_plus_ffs 1417..4008 (HV reference 4000); accuracy_bits 12.4..22.7 (HV reference 12); data_width on the front 19..28 (registry 8..28).

Per family:
- pipelined: 45 evals, 21 feasible; max throughput seen 282 MSPS; best accuracy 14.53 bits; best feasible luts_plus_ffs=1772; feasible ranges: data_width 17..19, n_iter 14..17, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 75 evals, 20 feasible; max throughput seen 178 MSPS; best accuracy 22.74 bits; best feasible luts_plus_ffs=1417; feasible ranges: data_width 18..28, n_iter 14..30, angle_guard -2..3, frac_guard 1..4, m 2..3
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (80 evals): data_width=18..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (13 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 88 feasible; hypervolume 1.787e+04 (+28.9%).

**LLM decision:** `stop` — Budget is exhausted (200/200 evaluations, round 3 of 4 complete), so this is the final round and only `stop` or `infeasible` is valid. The design is clearly feasible, not infeasible: 88 of 200 evaluations (78 unique) satisfy all three constraints, with 0% throughput violations (best 282 MSPS vs the 32 MSPS requirement), 32% error violations but a best max_abs_err of 2.86e-08 (2^-25.06, far inside the 2^-12 limit), and 28% batch-latency violations with a best sys_p99_batch_us of 0.158 us against the 0.44 us bound. The feasible Pareto front holds 20 designs spanning luts_plus_ffs 1337..4008 (HV reference 4000) and accuracy_bits 12.3..22.7 (HV reference 12), i.e. it already covers both objective ranges essentially end-to-end, and hypervolume reached 1.787e+04 with a +28.9% gain this round. The selection rule (min luts_plus_ffs) is served by the front's cheapest point, pipelined_m [data_width=18 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round m=3] at luts_plus_ffs=1337, accuracy_bits=12.3 (max_abs_err=0.000192 <= 0.000244141) and throughput 124 MSPS >= 32, with sys_p99_batch_us within the 0.44 us bound. Both families on the front (pipelined, pipelined_m) were explored, and no unexplored family remains, so further rounds would not add coverage. Caveat for the L2 stage: the cheapest front points sit closest to the error and batch-latency limits, so the L2 system simulation may drop them and re-select a slightly larger design from the same front; the front contains ample alternatives (e.g. 1564 and 1833 luts_plus_ffs points with 14.7-15.5 accuracy bits) if that happens.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.787e+04 (gain this round: +28.9%).
Feasible designs: 88 of 200 evaluations (78 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 32% violate; best seen 2.86e-08 (2^-25.06)
- sys_p99_batch_us <= 0.44: 28% violate; best seen 0.158

Pareto front (feasible, 20 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round m=3] luts_plus_ffs=1337, accuracy_bits=12.3, luts=938, ffs=400, throughput_msps=124, max_abs_err=0.000192 (2^-12.35), power_index=1.61
- pipelined_m [data_width=19 n_iter=18 angle_guard=3 frac_guard=0 rounding=round m=4] luts_plus_ffs=1564, accuracy_bits=14.7, luts=1188, ffs=376, throughput_msps=93.6, max_abs_err=3.74e-05 (2^-14.71), power_index=1.88
- pipelined_m [data_width=19 n_iter=18 angle_guard=2 frac_guard=4 rounding=round m=3] luts_plus_ffs=1833, accuracy_bits=15.5, luts=1353, ffs=480, throughput_msps=114, max_abs_err=2.09e-05 (2^-15.55), power_index=2.21
- pipelined_m [data_width=24 n_iter=18 angle_guard=3 frac_guard=0 rounding=round m=4] luts_plus_ffs=1918, accuracy_bits=16.9, luts=1456, ffs=462, throughput_msps=86, max_abs_err=8.29e-06 (2^-16.88), power_index=2.31
- pipelined_m [data_width=22 n_iter=18 angle_guard=3 frac_guard=4 rounding=round m=4] luts_plus_ffs=2001, accuracy_bits=16.9, luts=1538, ffs=462, throughput_msps=89.6, max_abs_err=8.25e-06 (2^-16.89), power_index=2.41
- pipelined_m [data_width=23 n_iter=20 angle_guard=2 frac_guard=3 rounding=round m=3] luts_plus_ffs=2351, accuracy_bits=18.5, luts=1716, ffs=636, throughput_msps=114, max_abs_err=2.65e-06 (2^-18.53), power_index=2.83
- pipelined_m [data_width=24 n_iter=23 angle_guard=4 frac_guard=0 rounding=round m=3] luts_plus_ffs=2625, accuracy_bits=19.2, luts=1906, ffs=718, throughput_msps=110, max_abs_err=1.62e-06 (2^-19.24), power_index=3.16
- pipelined_m [data_width=25 n_iter=23 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=2658, accuracy_bits=20.1, luts=1929, ffs=728, throughput_msps=110, max_abs_err=8.71e-07 (2^-20.13), power_index=3.2
- pipelined_m [data_width=28 n_iter=23 angle_guard=0 frac_guard=4 rounding=round m=3] luts_plus_ffs=3186, accuracy_bits=21.6, luts=2336, ffs=850, throughput_msps=106, max_abs_err=3.13e-07 (2^-21.61), power_index=3.83
- pipelined_m [data_width=26 n_iter=27 angle_guard=3 frac_guard=4 rounding=trunc m=2] luts_plus_ffs=4008, accuracy_bits=22.7, luts=2608, ffs=1400, throughput_msps=153, max_abs_err=1.42e-07 (2^-22.74), power_index=4.82
Front coverage: luts_plus_ffs 1337..4008 (HV reference 4000); accuracy_bits 12.3..22.7 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- pipelined: 45 evals, 21 feasible; max throughput seen 282 MSPS; best accuracy 14.53 bits; best feasible luts_plus_ffs=1772; feasible ranges: data_width 17..19, n_iter 14..17, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 155 evals, 67 feasible; max throughput seen 178 MSPS; best accuracy 25.06 bits; best feasible luts_plus_ffs=1337; feasible ranges: data_width 18..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 13419 in, 10562 out
- provider-reported cost: $0.0098
- full prompts and replies: `llm_trace.jsonl`

