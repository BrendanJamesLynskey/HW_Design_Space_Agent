# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 400 of 400 budgeted, over 4 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec low_area_control: Field-oriented motor-control loop needing sin/cos of the rotor angle at >= 1 MSPS with max error <= 2^-10. Area is everything: minimise LUTs + FFs.
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min luts_plus_ffs (HV ref 1500)
  objective: max accuracy_bits (HV ref 10)
  select: min luts_plus_ffs
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=15,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 166 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 91 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 11 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 90.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.174 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00081 (2^-10.27) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.64 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00021 (2^-12.22) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.72 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (32768 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 18 cycles, a new input every 18 cycle(s). DDS tone from its exact outputs: SFDR 83.6 dBc, SNR 71.3 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (37 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 166 | 91 | 11.0 | 18 | 0.174 | 0.00081 (2^-10.27) | 10.27 |
| 1 | `iterative:data_width=16,n_iter=15,angle_guard=1,frac_guard=0,rounding=trunc` | 172 | 97 | 11.0 | 18 | 0.182 | 0.000643 (2^-10.60) | 10.60 |
| 2 | `iterative:data_width=15,n_iter=17,angle_guard=1,frac_guard=1,rounding=trunc` | 180 | 95 | 8.1 | 20 | 0.207 | 0.000594 (2^-10.72) | 10.72 |
| 3 | `iterative:data_width=16,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 179 | 97 | 11.7 | 17 | 0.177 | 0.000342 (2^-11.51) | 11.51 |
| 4 | `iterative:data_width=16,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc` | 191 | 101 | 11.0 | 18 | 0.198 | 0.00025 (2^-11.97) | 11.97 |
| 5 | `iterative:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 191 | 102 | 11.7 | 17 | 0.187 | 0.000204 (2^-12.26) | 12.26 |
| 6 | `iterative:data_width=17,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 193 | 103 | 11.4 | 17 | 0.189 | 0.000194 (2^-12.33) | 12.33 |
| 7 | `iterative:data_width=17,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` | 204 | 107 | 11.4 | 17 | 0.199 | 0.000178 (2^-12.46) | 12.46 |
| 8 | `iterative:data_width=18,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc` | 206 | 110 | 11.4 | 17 | 0.202 | 0.000166 (2^-12.55) | 12.55 |
| 9 | `iterative:data_width=16,n_iter=16,angle_guard=2,frac_guard=4,rounding=trunc` | 212 | 106 | 10.2 | 19 | 0.227 | 0.000151 (2^-12.69) | 12.69 |
| 10 | `iterative:data_width=16,n_iter=15,angle_guard=3,frac_guard=4,rounding=trunc` | 214 | 107 | 10.8 | 18 | 0.217 | 0.000148 (2^-12.73) | 12.73 |
| 11 | `iterative:data_width=18,n_iter=17,angle_guard=1,frac_guard=0,rounding=round` | 226 | 108 | 7.9 | 20 | 0.251 | 9.26e-05 (2^-13.40) | 13.40 |
| 12 | `iterative:data_width=21,n_iter=16,angle_guard=1,frac_guard=0,rounding=trunc` | 229 | 122 | 10.2 | 19 | 0.251 | 4.46e-05 (2^-14.45) | 14.45 |
| 13 | `iterative:data_width=20,n_iter=18,angle_guard=1,frac_guard=0,rounding=round` | 258 | 118 | 7.6 | 21 | 0.297 | 2.9e-05 (2^-15.07) | 15.07 |
| 14 | `iterative:data_width=20,n_iter=18,angle_guard=1,frac_guard=1,rounding=trunc` | 260 | 120 | 7.6 | 21 | 0.3 | 2.8e-05 (2^-15.12) | 15.12 |
| 15 | `iterative:data_width=20,n_iter=28,angle_guard=1,frac_guard=0,rounding=round` | 264 | 118 | 5.1 | 31 | 0.445 | 2.52e-05 (2^-15.28) | 15.28 |
| 16 | `iterative:data_width=20,n_iter=29,angle_guard=4,frac_guard=0,rounding=round` | 271 | 121 | 4.9 | 32 | 0.472 | 2.17e-05 (2^-15.49) | 15.49 |
| 17 | `iterative:data_width=22,n_iter=24,angle_guard=2,frac_guard=0,rounding=trunc` | 286 | 129 | 5.8 | 27 | 0.421 | 1.22e-05 (2^-16.32) | 16.32 |
| 18 | `iterative:data_width=22,n_iter=28,angle_guard=1,frac_guard=0,rounding=round` | 299 | 128 | 5.0 | 31 | 0.498 | 6.76e-06 (2^-17.17) | 17.17 |
| 19 | `iterative:data_width=22,n_iter=24,angle_guard=2,frac_guard=0,rounding=round` | 299 | 129 | 5.8 | 27 | 0.435 | 5.49e-06 (2^-17.47) | 17.47 |
| 20 | `iterative:data_width=23,n_iter=27,angle_guard=3,frac_guard=1,rounding=trunc` | 324 | 137 | 5.2 | 30 | 0.52 | 3.51e-06 (2^-18.12) | 18.12 |
| 21 | `iterative:data_width=24,n_iter=23,angle_guard=4,frac_guard=0,rounding=trunc` | 324 | 141 | 5.9 | 26 | 0.455 | 2.96e-06 (2^-18.37) | 18.37 |
| 22 | `iterative:data_width=24,n_iter=29,angle_guard=0,frac_guard=0,rounding=round` | 337 | 137 | 4.9 | 32 | 0.57 | 2.49e-06 (2^-18.62) | 18.62 |
| 23 | `iterative:data_width=24,n_iter=23,angle_guard=1,frac_guard=1,rounding=trunc` | 334 | 140 | 6.0 | 26 | 0.464 | 1.77e-06 (2^-19.11) | 19.11 |
| 24 | `iterative:data_width=24,n_iter=30,angle_guard=2,frac_guard=0,rounding=round` | 340 | 139 | 4.7 | 33 | 0.595 | 1.57e-06 (2^-19.28) | 19.28 |
| 25 | `iterative:data_width=24,n_iter=22,angle_guard=1,frac_guard=2,rounding=trunc` | 350 | 142 | 6.2 | 25 | 0.463 | 1.47e-06 (2^-19.37) | 19.37 |
| 26 | `iterative:data_width=25,n_iter=26,angle_guard=2,frac_guard=1,rounding=trunc` | 360 | 146 | 5.3 | 29 | 0.552 | 8.2e-07 (2^-20.22) | 20.22 |
| 27 | `iterative:data_width=24,n_iter=24,angle_guard=2,frac_guard=3,rounding=trunc` | 368 | 145 | 5.7 | 27 | 0.521 | 7.88e-07 (2^-20.27) | 20.27 |
| 28 | `iterative:data_width=24,n_iter=23,angle_guard=4,frac_guard=3,rounding=trunc` | 371 | 147 | 5.9 | 26 | 0.507 | 7.06e-07 (2^-20.43) | 20.43 |
| 29 | `iterative:data_width=26,n_iter=29,angle_guard=1,frac_guard=1,rounding=trunc` | 379 | 150 | 4.8 | 32 | 0.637 | 4.76e-07 (2^-21.00) | 21.00 |
| 30 | `iterative:data_width=25,n_iter=26,angle_guard=2,frac_guard=3,rounding=trunc` | 394 | 150 | 5.3 | 29 | 0.594 | 3.7e-07 (2^-21.37) | 21.37 |
| 31 | `iterative:data_width=26,n_iter=28,angle_guard=1,frac_guard=3,rounding=trunc` | 411 | 154 | 4.9 | 31 | 0.66 | 2.9e-07 (2^-21.72) | 21.72 |
| 32 | `iterative:data_width=26,n_iter=28,angle_guard=3,frac_guard=1,rounding=round` | 451 | 152 | 4.9 | 31 | 0.703 | 2.37e-07 (2^-22.01) | 22.01 |
| 33 | `iterative:data_width=27,n_iter=24,angle_guard=2,frac_guard=1,rounding=round` | 459 | 156 | 5.7 | 27 | 0.625 | 2.23e-07 (2^-22.10) | 22.10 |
| 34 | `iterative:data_width=27,n_iter=26,angle_guard=2,frac_guard=1,rounding=round` | 470 | 156 | 5.3 | 29 | 0.683 | 1.67e-07 (2^-22.51) | 22.51 |
| 35 | `pipelined_m:data_width=28,n_iter=25,angle_guard=1,frac_guard=1,rounding=trunc,m=7` | 2357 | 434 | 52.0 | 6 | 0.105 | 1.59e-07 (2^-22.59) | 22.59 |
| 36 | `pipelined_m:data_width=28,n_iter=25,angle_guard=3,frac_guard=4,rounding=round,m=7` | 2619 | 462 | 49.9 | 6 | 0.116 | 7.42e-08 (2^-23.68) | 23.68 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-critical with a low throughput floor (1 MSPS) and moderate accuracy (2^-10). Shared-datapath families (iterative, unrolled_k) reuse one adder/shifter chain and therefore have the smallest area; pipelined families replicate the datapath per stage and are expected to be dominated on the LUT+FF objective. Accuracy depends only on data_width, n_iter, angle_guard, frac_guard and rounding, so these are searched jointly. Ranges are kept modest to target the area-accuracy knee but wide enough to cover the feasible region: W 10..18 and N 8..18 should span from just below to comfortably above the 2^-10 error requirement. Most budget goes to iterative because it has the smallest datapath and can easily meet 1 MSPS at these N values; unrolled_k gets a smaller share to check whether a small k can improve Fmax enough to matter without adding too much area.*)
- `iterative` (70 evals): data_width=10..18, n_iter=8..18, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Smallest datapath: one shared adder/shifter chain reused over N+3 cycles. With N up to 18, the throughput floor of 1 MSPS only requires roughly 21 MHz, which is easily met on Artix-7. Search modest W and N to find the minimum LUT+FF design that still satisfies max_abs_err <= 2^-10; guards and rounding are included because they affect accuracy without changing the datapath size much.
- `unrolled_k` (30 evals): data_width=10..18, n_iter=8..18, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..4. *Why:* Shares the same accuracy model as iterative, but k chained micro-rotations per cycle reduce the cycle count at the cost of k-1 extra adders/shifters. With k=2..4 the area increase is modest, and it may provide a different area/throughput point if iterative's Fmax were limiting. Given the low 1 MSPS floor, it is likely dominated by iterative on area, so a smaller share is used to confirm and to catch any unexpected corner.

**Result (code):** 100 evaluations this round, 100 total; 52 feasible; hypervolume 4795 (n/a).

**LLM decision:** `map_front` — The Pareto front is entirely `iterative` and only occupies luts_plus_ffs 269..404 of the 1500 area reference and data_width 16..18 of the registry's 8..28 — a small part of both objective ranges. Decomposing HV over my own front (recomputing the 2-D dominated area with the last point's rectangle reaching the ref at 1500) shows the segment from the highest-accuracy point (404 area, 14.04 bits) out to the ref contributes ~4400 of the reported 4795, i.e. the HV is almost entirely set by how far accuracy extends while area stays well under 1500. So the dominant remaining lever is sweeping data_width/n_iter upward (accuracy is family-independent; only n_iter/data_width/guards/rounding set it) to fill the 404..1500 area band with higher-accuracy points, not squeezing the already-known 269-area corner (that corner already exists and is what the selection rule picks, and 0% of evals violate throughput, so throughput is not the risk). Hence spend this round letting NSGA-II map the full ranges of the family on the front, seeded with the current front. The two unexplored families are not HV candidates: their accuracy is identical by construction, and the only family that reaches the front is the cheapest one at a given accuracy — unrolled_k (k=4, i.e. only 4× replication) already costs 483 vs iterative's 269 at similar accuracy, so pipelined/pipelined_m (even more replicated datapaths) cannot supply new non-dominated points and would only burn budget that should go to extending the accuracy axis.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 4795 (gain this round: n/a (first round)).
Feasible designs: 52 of 100 evaluations (41 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: pipelined, pipelined_m.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 18.5
- max_abs_err <= 0.000976562: 48% violate; best seen 5.95e-05 (2^-14.04)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=269, accuracy_bits=10.6, luts=172, ffs=97, throughput_msps=11, max_abs_err=0.000643 (2^-10.60), power_index=0.182
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.5, luts=179, ffs=97, throughput_msps=11.7, max_abs_err=0.000342 (2^-11.51), power_index=0.177
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=292, accuracy_bits=12, luts=191, ffs=101, throughput_msps=11, max_abs_err=0.00025 (2^-11.97), power_index=0.198
- iterative [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=293, accuracy_bits=12.3, luts=191, ffs=102, throughput_msps=11.7, max_abs_err=0.000204 (2^-12.26), power_index=0.187
- iterative [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=296, accuracy_bits=12.3, luts=193, ffs=103, throughput_msps=11.4, max_abs_err=0.000194 (2^-12.33), power_index=0.189
- iterative [data_width=16 n_iter=16 angle_guard=2 frac_guard=4 rounding=trunc] luts_plus_ffs=318, accuracy_bits=12.7, luts=212, ffs=106, throughput_msps=10.2, max_abs_err=0.000151 (2^-12.69), power_index=0.227
- iterative [data_width=16 n_iter=15 angle_guard=3 frac_guard=4 rounding=trunc] luts_plus_ffs=321, accuracy_bits=12.7, luts=214, ffs=107, throughput_msps=10.8, max_abs_err=0.000148 (2^-12.73), power_index=0.217
- iterative [data_width=18 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=334, accuracy_bits=13.4, luts=226, ffs=108, throughput_msps=7.95, max_abs_err=9.26e-05 (2^-13.40), power_index=0.251
- iterative [data_width=18 n_iter=17 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=404, accuracy_bits=14, luts=292, ffs=112, throughput_msps=7.95, max_abs_err=5.95e-05 (2^-14.04), power_index=0.304
Front coverage: luts_plus_ffs 269..404 (HV reference 1500); accuracy_bits 10.6..14 (HV reference 10); data_width on the front 16..18 (registry 8..28).

Per family:
- iterative: 70 evals, 35 feasible; max throughput seen 18.5 MSPS; best accuracy 14.04 bits; best feasible luts_plus_ffs=269; feasible ranges: data_width 13..18, n_iter 14..18, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 30 evals, 17 feasible; max throughput seen 15.8 MSPS; best accuracy 13.81 bits; best feasible luts_plus_ffs=483; feasible ranges: data_width 15..17, n_iter 17..18, angle_guard -1..3, frac_guard 0..3, k 4..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (9 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 149 feasible; hypervolume 1.349e+04 (+181.3%).

**LLM decision:** `add_family` — Round 2/4, 200/400 evals used. The feasible front is entirely from iterative + unrolled_k; the two registered families (pipelined, pipelined_m) are unexplored. The spec's binding objective is min luts_plus_ffs and its only hard constraint is throughput >= 1 MSPS, which iterative already clears by ~11x (best seen 18.5 MSPS), so throughput is not the lever. However, the front's area span is only 257..626 against an HV reference of 1500, and the front is built from shared-datapath/barrel-shifter designs. pipelined_m with a large m (register every m stages) replaces the shared barrel shifters with constant-shift stages and 1 result/cycle, so its luts_plus_ffs could be competitive at the low-area corner while adding new (area, accuracy) points that raise hypervolume. Worth one round before the reserved front-mapping round.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.349e+04 (gain this round: +181.3%).
Feasible designs: 149 of 200 evaluations (131 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: pipelined, pipelined_m.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 18.5
- max_abs_err <= 0.000976562: 26% violate; best seen 1.67e-07 (2^-22.51)

Pareto front (feasible, 28 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11, max_abs_err=0.00081 (2^-10.27), power_index=0.174
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.5, luts=179, ffs=97, throughput_msps=11.7, max_abs_err=0.000342 (2^-11.51), power_index=0.177
- iterative [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=296, accuracy_bits=12.3, luts=193, ffs=103, throughput_msps=11.4, max_abs_err=0.000194 (2^-12.33), power_index=0.189
- iterative [data_width=16 n_iter=15 angle_guard=3 frac_guard=4 rounding=trunc] luts_plus_ffs=321, accuracy_bits=12.7, luts=214, ffs=107, throughput_msps=10.8, max_abs_err=0.000148 (2^-12.73), power_index=0.217
- iterative [data_width=18 n_iter=24 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=381, accuracy_bits=14.7, luts=265, ffs=116, throughput_msps=5.89, max_abs_err=3.81e-05 (2^-14.68), power_index=0.387
- iterative [data_width=18 n_iter=23 angle_guard=4 frac_guard=4 rounding=trunc] luts_plus_ffs=401, accuracy_bits=15.2, luts=282, ffs=119, throughput_msps=6.11, max_abs_err=2.65e-05 (2^-15.21), power_index=0.392
- iterative [data_width=24 n_iter=23 angle_guard=4 frac_guard=0 rounding=trunc] luts_plus_ffs=465, accuracy_bits=18.4, luts=324, ffs=141, throughput_msps=5.89, max_abs_err=2.96e-06 (2^-18.37), power_index=0.455
- iterative [data_width=24 n_iter=24 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=513, accuracy_bits=20.3, luts=368, ffs=145, throughput_msps=5.68, max_abs_err=7.88e-07 (2^-20.27), power_index=0.521
- iterative [data_width=25 n_iter=26 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=545, accuracy_bits=21.4, luts=394, ffs=150, throughput_msps=5.28, max_abs_err=3.7e-07 (2^-21.37), power_index=0.594
- iterative [data_width=27 n_iter=26 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=626, accuracy_bits=22.5, luts=470, ffs=156, throughput_msps=5.28, max_abs_err=1.67e-07 (2^-22.51), power_index=0.683
Front coverage: luts_plus_ffs 257..626 (HV reference 1500); accuracy_bits 10.3..22.5 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 170 evals, 132 feasible; max throughput seen 18.5 MSPS; best accuracy 22.51 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 13..27, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 30 evals, 17 feasible; max throughput seen 15.8 MSPS; best accuracy 13.81 bits; best feasible luts_plus_ffs=483; feasible ranges: data_width 15..17, n_iter 17..18, angle_guard -1..3, frac_guard 0..3, k 4..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *seed with the current 28-design front; keep the low-area corner (luts_plus_ffs <= 400) densely sampled since the selection rule is min luts_plus_ffs, and let the rest of the budget probe higher-accuracy/higher-area points to extend the front toward the 1500 area reference.*)
- `pipelined_m` (60 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=4..8. *Why:* large m keeps FF count down while giving 1 result/cycle; constant shifts may beat shared barrel shifters on LUTs at the low-area corner (target luts_plus_ffs near 257).
- `pipelined` (40 evals): data_width=14..24, n_iter=12..24, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* full per-stage registration is the area-worst case but bounds the family; needed to know whether any pipelined point is non-dominated.

**Result (code):** 100 evaluations this round, 300 total; 243 feasible; hypervolume 1.349e+04 (+0.0%).

**LLM decision:** `map_front` — Round 3 produced 0.0% hypervolume gain, so the front has stabilised, but 100 evaluations remain and this is the final round. The front already spans all four families (iterative, unrolled_k, pipelined, pipelined_m) and covers luts_plus_ffs 257..3081 with accuracy_bits 10.3..23.7, yet the high-accuracy end (pipelined_m at 3081) lies beyond the HV reference of 1500 and the low-area end (iterative at 257) is the selection target. The reserved final-round budget is best spent mapping the full ranges of the families already on the front, seeded with the current Pareto set, to confirm there are no gaps in the trade-off curve and to finalise the front before selection. No further narrowing is justified given the 0% gain.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.349e+04 (gain this round: +0.0%).
Feasible designs: 243 of 300 evaluations (219 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 273
- max_abs_err <= 0.000976562: 19% violate; best seen 7.42e-08 (2^-23.68)

Pareto front (feasible, 30 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11, max_abs_err=0.00081 (2^-10.27), power_index=0.174
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.5, luts=179, ffs=97, throughput_msps=11.7, max_abs_err=0.000342 (2^-11.51), power_index=0.177
- iterative [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=296, accuracy_bits=12.3, luts=193, ffs=103, throughput_msps=11.4, max_abs_err=0.000194 (2^-12.33), power_index=0.189
- iterative [data_width=18 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=334, accuracy_bits=13.4, luts=226, ffs=108, throughput_msps=7.95, max_abs_err=9.26e-05 (2^-13.40), power_index=0.251
- iterative [data_width=18 n_iter=22 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=381, accuracy_bits=14.7, luts=265, ffs=116, throughput_msps=6.36, max_abs_err=3.81e-05 (2^-14.68), power_index=0.358
- iterative [data_width=22 n_iter=24 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=415, accuracy_bits=16.3, luts=286, ffs=129, throughput_msps=5.78, max_abs_err=1.22e-05 (2^-16.32), power_index=0.421
- iterative [data_width=24 n_iter=22 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=492, accuracy_bits=19.4, luts=350, ffs=142, throughput_msps=6.24, max_abs_err=1.47e-06 (2^-19.37), power_index=0.463
- iterative [data_width=24 n_iter=23 angle_guard=4 frac_guard=4 rounding=trunc] luts_plus_ffs=536, accuracy_bits=20.7, luts=387, ffs=149, throughput_msps=5.89, max_abs_err=5.85e-07 (2^-20.71), power_index=0.524
- iterative [data_width=25 n_iter=26 angle_guard=2 frac_guard=3 rounding=round] luts_plus_ffs=612, accuracy_bits=21.6, luts=462, ffs=150, throughput_msps=5.28, max_abs_err=3.12e-07 (2^-21.61), power_index=0.668
- pipelined_m [data_width=28 n_iter=25 angle_guard=3 frac_guard=4 rounding=round m=7] luts_plus_ffs=3081, accuracy_bits=23.7, luts=2619, ffs=462, throughput_msps=49.9, max_abs_err=7.42e-08 (2^-23.68), power_index=0.116
Front coverage: luts_plus_ffs 257..3081 (HV reference 1500); accuracy_bits 10.3..23.7 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 170 evals, 132 feasible; max throughput seen 18.5 MSPS; best accuracy 22.51 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 13..27, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 30 evals, 17 feasible; max throughput seen 15.8 MSPS; best accuracy 13.81 bits; best feasible luts_plus_ffs=483; feasible ranges: data_width 15..17, n_iter 17..18, angle_guard -1..3, frac_guard 0..3, k 4..4
- pipelined: 40 evals, 34 feasible; max throughput seen 273 MSPS; best accuracy 18.65 bits; best feasible luts_plus_ffs=1542; feasible ranges: data_width 14..24, n_iter 12..24, angle_guard -2..3, frac_guard 0..4
- pipelined_m: 60 evals, 60 feasible; max throughput seen 97.8 MSPS; best accuracy 23.68 bits; best feasible luts_plus_ffs=1081; feasible ranges: data_width 14..28, n_iter 12..29, angle_guard -2..4, frac_guard 0..4, m 4..8
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (94 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (28 front designs; box front_anchored)
- `pipelined_m` (6 evals): data_width=27..28, n_iter=23..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (2 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 335 feasible; hypervolume 1.355e+04 (+0.5%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), and the front is feasible and well covered: 335/400 evaluations feasible, 37 Pareto designs spanning luts_plus_ffs 257..3081 and accuracy_bits 10.3..23.7, with hypervolume 1.355e+04 still gaining only +0.5% this round (diminishing returns). The spec's constraints are comfortably met — throughput constraint has 0% violations (best 273 MSPS, and the selected corner runs 11 MSPS >= 1) and the error constraint is met by the front's cheapest point, iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] with luts_plus_ffs=257, max_abs_err=0.00081 (2^-10.27) <= 0.000976562, accuracy_bits=10.3. That design is also the min-luts_plus_ffs selection the spec asks for, so no further exploration can improve the chosen design; all four families have been explored and no unexplored family remains.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.355e+04 (gain this round: +0.5%).
Feasible designs: 335 of 400 evaluations (301 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 273
- max_abs_err <= 0.000976562: 16% violate; best seen 7.42e-08 (2^-23.68)

Pareto front (feasible, 37 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11, max_abs_err=0.00081 (2^-10.27), power_index=0.174
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=292, accuracy_bits=12, luts=191, ffs=101, throughput_msps=11, max_abs_err=0.00025 (2^-11.97), power_index=0.198
- iterative [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=316, accuracy_bits=12.6, luts=206, ffs=110, throughput_msps=11.4, max_abs_err=0.000166 (2^-12.55), power_index=0.202
- iterative [data_width=21 n_iter=16 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=351, accuracy_bits=14.5, luts=229, ffs=122, throughput_msps=10.2, max_abs_err=4.46e-05 (2^-14.45), power_index=0.251
- iterative [data_width=20 n_iter=29 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=392, accuracy_bits=15.5, luts=271, ffs=121, throughput_msps=4.88, max_abs_err=2.17e-05 (2^-15.49), power_index=0.472
- iterative [data_width=23 n_iter=27 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=461, accuracy_bits=18.1, luts=324, ffs=137, throughput_msps=5.2, max_abs_err=3.51e-06 (2^-18.12), power_index=0.52
- iterative [data_width=24 n_iter=30 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=479, accuracy_bits=19.3, luts=340, ffs=139, throughput_msps=4.73, max_abs_err=1.57e-06 (2^-19.28), power_index=0.595
- iterative [data_width=24 n_iter=23 angle_guard=4 frac_guard=3 rounding=trunc] luts_plus_ffs=519, accuracy_bits=20.4, luts=371, ffs=147, throughput_msps=5.89, max_abs_err=7.06e-07 (2^-20.43), power_index=0.507
- iterative [data_width=26 n_iter=28 angle_guard=3 frac_guard=1 rounding=round] luts_plus_ffs=603, accuracy_bits=22, luts=451, ffs=152, throughput_msps=4.94, max_abs_err=2.37e-07 (2^-22.01), power_index=0.703
- pipelined_m [data_width=28 n_iter=25 angle_guard=3 frac_guard=4 rounding=round m=7] luts_plus_ffs=3081, accuracy_bits=23.7, luts=2619, ffs=462, throughput_msps=49.9, max_abs_err=7.42e-08 (2^-23.68), power_index=0.116
Front coverage: luts_plus_ffs 257..3081 (HV reference 1500); accuracy_bits 10.3..23.7 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 264 evals, 218 feasible; max throughput seen 18.5 MSPS; best accuracy 22.51 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 13..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 30 evals, 17 feasible; max throughput seen 15.8 MSPS; best accuracy 13.81 bits; best feasible luts_plus_ffs=483; feasible ranges: data_width 15..17, n_iter 17..18, angle_guard -1..3, frac_guard 0..3, k 4..4
- pipelined: 40 evals, 34 feasible; max throughput seen 273 MSPS; best accuracy 18.65 bits; best feasible luts_plus_ffs=1542; feasible ranges: data_width 14..24, n_iter 12..24, angle_guard -2..3, frac_guard 0..4
- pipelined_m: 66 evals, 66 feasible; max throughput seen 147 MSPS; best accuracy 23.68 bits; best feasible luts_plus_ffs=1081; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 27499 in, 18352 out
- provider-reported cost: $0.0198
- full prompts and replies: `llm_trace.jsonl`

