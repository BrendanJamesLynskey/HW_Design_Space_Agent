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
`iterative:data_width=16,n_iter=12,angle_guard=1,frac_guard=0,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 163 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 97 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 13.2 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 15 | exact: schedule |
| latency_ns | 75.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.146 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000887 (2^-10.14) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 14.5 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000225 (2^-12.12) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 3.69 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.1 | exact: bit-accurate model, exhaustive (65536 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 15 cycles, a new input every 15 cycle(s). DDS tone from its exact outputs: SFDR 79.8 dBc, SNR 70.0 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (40 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=16,n_iter=12,angle_guard=1,frac_guard=0,rounding=trunc` | 163 | 97 | 13.2 | 15 | 0.146 | 0.000887 (2^-10.14) | 10.14 |
| 1 | `iterative:data_width=16,n_iter=12,angle_guard=0,frac_guard=0,rounding=round` | 167 | 96 | 13.2 | 15 | 0.148 | 0.000712 (2^-10.46) | 10.46 |
| 2 | `iterative:data_width=15,n_iter=17,angle_guard=1,frac_guard=1,rounding=trunc` | 180 | 95 | 8.1 | 20 | 0.207 | 0.000594 (2^-10.72) | 10.72 |
| 3 | `iterative:data_width=16,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc` | 180 | 98 | 10.4 | 19 | 0.198 | 0.000375 (2^-11.38) | 11.38 |
| 4 | `iterative:data_width=16,n_iter=17,angle_guard=0,frac_guard=0,rounding=round` | 192 | 97 | 8.1 | 20 | 0.217 | 0.000373 (2^-11.39) | 11.39 |
| 5 | `iterative:data_width=17,n_iter=13,angle_guard=1,frac_guard=0,rounding=round` | 191 | 102 | 12.4 | 16 | 0.176 | 0.000326 (2^-11.58) | 11.58 |
| 6 | `iterative:data_width=18,n_iter=15,angle_guard=-1,frac_guard=0,rounding=trunc` | 191 | 105 | 11.0 | 18 | 0.2 | 0.000211 (2^-12.21) | 12.21 |
| 7 | `iterative:data_width=18,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc` | 193 | 106 | 10.4 | 19 | 0.214 | 0.000182 (2^-12.43) | 12.43 |
| 8 | `iterative:data_width=17,n_iter=16,angle_guard=4,frac_guard=0,rounding=round` | 196 | 105 | 10.2 | 19 | 0.215 | 0.000146 (2^-12.74) | 12.74 |
| 9 | `iterative:data_width=18,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc` | 203 | 108 | 10.2 | 19 | 0.222 | 0.000136 (2^-12.84) | 12.84 |
| 10 | `iterative:data_width=18,n_iter=16,angle_guard=1,frac_guard=1,rounding=trunc` | 204 | 109 | 10.2 | 19 | 0.224 | 0.000104 (2^-13.23) | 13.23 |
| 11 | `iterative:data_width=18,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 214 | 111 | 10.2 | 19 | 0.232 | 8.08e-05 (2^-13.60) | 13.60 |
| 12 | `iterative:data_width=18,n_iter=28,angle_guard=2,frac_guard=0,rounding=round` | 231 | 109 | 5.1 | 31 | 0.396 | 7.75e-05 (2^-13.65) | 13.65 |
| 13 | `iterative:data_width=18,n_iter=17,angle_guard=1,frac_guard=2,rounding=trunc` | 242 | 112 | 7.9 | 20 | 0.266 | 6.92e-05 (2^-13.82) | 13.82 |
| 14 | `iterative:data_width=18,n_iter=18,angle_guard=4,frac_guard=2,rounding=trunc` | 248 | 115 | 7.6 | 21 | 0.286 | 4.84e-05 (2^-14.33) | 14.33 |
| 15 | `iterative:data_width=20,n_iter=17,angle_guard=2,frac_guard=0,rounding=trunc` | 248 | 119 | 7.9 | 20 | 0.276 | 4.61e-05 (2^-14.40) | 14.40 |
| 16 | `iterative:data_width=19,n_iter=28,angle_guard=4,frac_guard=0,rounding=round` | 252 | 116 | 5.0 | 31 | 0.429 | 3.74e-05 (2^-14.71) | 14.71 |
| 17 | `iterative:data_width=19,n_iter=27,angle_guard=4,frac_guard=0,rounding=round` | 252 | 116 | 5.2 | 30 | 0.415 | 3.74e-05 (2^-14.71) | 14.71 |
| 18 | `iterative:data_width=21,n_iter=19,angle_guard=0,frac_guard=0,rounding=trunc` | 260 | 122 | 7.2 | 22 | 0.316 | 2.66e-05 (2^-15.20) | 15.20 |
| 19 | `iterative:data_width=21,n_iter=25,angle_guard=4,frac_guard=0,rounding=trunc` | 272 | 126 | 5.6 | 28 | 0.419 | 2.36e-05 (2^-15.37) | 15.37 |
| 20 | `iterative:data_width=19,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc` | 280 | 120 | 5.7 | 28 | 0.422 | 2.18e-05 (2^-15.49) | 15.49 |
| 21 | `iterative:data_width=21,n_iter=28,angle_guard=4,frac_guard=0,rounding=round` | 287 | 126 | 5.0 | 31 | 0.482 | 1.15e-05 (2^-16.41) | 16.41 |
| 22 | `iterative:data_width=20,n_iter=25,angle_guard=3,frac_guard=3,rounding=trunc` | 301 | 126 | 5.6 | 28 | 0.45 | 1e-05 (2^-16.61) | 16.61 |
| 23 | `iterative:data_width=23,n_iter=23,angle_guard=4,frac_guard=0,rounding=trunc` | 307 | 136 | 5.9 | 26 | 0.433 | 5.84e-06 (2^-17.39) | 17.39 |
| 24 | `iterative:data_width=22,n_iter=20,angle_guard=3,frac_guard=2,rounding=trunc` | 310 | 134 | 6.8 | 23 | 0.384 | 4.63e-06 (2^-17.72) | 17.72 |
| 25 | `iterative:data_width=22,n_iter=20,angle_guard=4,frac_guard=2,rounding=trunc` | 312 | 135 | 6.8 | 23 | 0.387 | 4.4e-06 (2^-17.79) | 17.79 |
| 26 | `iterative:data_width=23,n_iter=27,angle_guard=4,frac_guard=1,rounding=trunc` | 325 | 138 | 5.1 | 30 | 0.523 | 3.08e-06 (2^-18.31) | 18.31 |
| 27 | `iterative:data_width=25,n_iter=25,angle_guard=-1,frac_guard=0,rounding=trunc` | 337 | 141 | 5.6 | 28 | 0.504 | 2.56e-06 (2^-18.57) | 18.57 |
| 28 | `iterative:data_width=24,n_iter=22,angle_guard=4,frac_guard=0,rounding=round` | 338 | 141 | 6.1 | 25 | 0.45 | 1.62e-06 (2^-19.24) | 19.24 |
| 29 | `iterative:data_width=26,n_iter=28,angle_guard=1,frac_guard=0,rounding=trunc` | 360 | 148 | 4.9 | 31 | 0.593 | 9.39e-07 (2^-20.02) | 20.02 |
| 30 | `iterative:data_width=26,n_iter=27,angle_guard=4,frac_guard=0,rounding=trunc` | 365 | 151 | 5.1 | 30 | 0.583 | 8.79e-07 (2^-20.12) | 20.12 |
| 31 | `iterative:data_width=26,n_iter=27,angle_guard=4,frac_guard=0,rounding=round` | 380 | 151 | 5.1 | 30 | 0.6 | 3.6e-07 (2^-21.40) | 21.40 |
| 32 | `iterative:data_width=25,n_iter=25,angle_guard=3,frac_guard=3,rounding=trunc` | 396 | 151 | 5.5 | 28 | 0.576 | 3.42e-07 (2^-21.48) | 21.48 |
| 33 | `iterative:data_width=26,n_iter=25,angle_guard=2,frac_guard=2,rounding=trunc` | 396 | 153 | 5.5 | 28 | 0.579 | 3.07e-07 (2^-21.63) | 21.63 |
| 34 | `iterative:data_width=28,n_iter=28,angle_guard=1,frac_guard=0,rounding=trunc` | 398 | 158 | 4.9 | 31 | 0.649 | 2.4e-07 (2^-21.99) | 21.99 |
| 35 | `iterative:data_width=28,n_iter=28,angle_guard=1,frac_guard=0,rounding=round` | 413 | 158 | 4.9 | 31 | 0.666 | 1.32e-07 (2^-22.85) | 22.85 |
| 36 | `iterative:data_width=28,n_iter=28,angle_guard=4,frac_guard=0,rounding=round` | 418 | 161 | 4.9 | 31 | 0.676 | 1.03e-07 (2^-23.22) | 23.22 |
| 37 | `iterative:data_width=28,n_iter=28,angle_guard=1,frac_guard=4,rounding=trunc` | 467 | 166 | 4.9 | 31 | 0.738 | 8.37e-08 (2^-23.51) | 23.51 |
| 38 | `iterative:data_width=28,n_iter=28,angle_guard=2,frac_guard=1,rounding=round` | 491 | 161 | 4.9 | 31 | 0.761 | 6.73e-08 (2^-23.82) | 23.82 |
| 39 | `iterative:data_width=28,n_iter=27,angle_guard=4,frac_guard=1,rounding=round` | 495 | 163 | 5.0 | 30 | 0.742 | 5.86e-08 (2^-24.02) | 24.02 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-dominated: minimise LUTs+FFs subject to throughput >=1 MSPS and max_abs_err <=2^-10. Accuracy is identical across families for the same data_width, n_iter, angle_guard, frac_guard and rounding, so the Pareto front is essentially the minimum-area implementation for each accuracy level. Iterative uses a single shared datapath and is therefore the most area-efficient family; its throughput is Fmax/(N+3), which for N<=18 requires only Fmax>=21 MHz, a very low bar for Artix-7. Unrolled_k is included only as a throughput hedge in case the iterative Fmax estimate is unexpectedly low; its larger datapath makes it unlikely to win on area. Pipelined and pipelined_m are omitted because their pipeline registers add area without helping the area objective, and the throughput constraint is already satisfiable by iterative. The proposed ranges (data_width 10..18, n_iter 8..18, angle_guard -1..2, frac_guard 0..2) cover the feasible accuracy region (data_width>=12, n_iter>=10 for 2^-10) and some infeasible low-area points, allowing the search to map the trade-off curve. Budget is split 60/40 to favour the most promising area family while still probing the throughput hedge.*)
- `iterative` (60 evals): data_width=10..18, n_iter=8..18, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Smallest area family: one shared micro-rotation datapath. Throughput = Fmax/(N+3); for N<=18 this needs only Fmax>=21 MHz, easily met on Artix-7. Accuracy depends only on data_width, n_iter, angle_guard, frac_guard and rounding, so this family can cover the whole accuracy/area trade-off with minimal LUT+FF. Ranges span the likely feasible region (data_width>=12, n_iter>=10 for 2^-10) and some infeasible low-area points to map the front.
- `unrolled_k` (40 evals): data_width=10..18, n_iter=8..18, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Hedge for throughput: if iterative Fmax is lower than expected, unrolled_k with small k reduces cycles to ceil(N/k)+3, allowing the same N at a lower clock. Area is larger than iterative for identical accuracy parameters, so it is unlikely to dominate the Pareto front, but it may be needed to satisfy the >=1 MSPS constraint for larger N or lower Fmax. Ranges mirror iterative for accuracy parameters and restrict k to 2..4 to keep area growth modest.

**Result (code):** 100 evaluations this round, 100 total; 58 feasible; hypervolume 4338 (n/a).

**LLM decision:** `map_front` — Round 1's feasible front is entirely `iterative` and spans only data_width 16..18 (registry 8..28) and accuracy_bits 10.1..13.6, i.e. a small slice of both objective ranges. With the HV reference point at (luts_plus_ffs=1500, accuracy_bits=10), the large unexplored high-accuracy region dominates the hypervolume, while the selection winner (min luts_plus_ffs=260, max_abs_err=2^-10.14) sits right on the 2^-10 error limit, so the low-area end of the curve is also unconfirmed. `pipelined`/`pipelined_m` are structurally dominated for a min-area objective (same datapath plus pipeline registers) and the throughput constraint is already met with >10x margin (best 16.9 MSPS vs 1 required), so spending budget on a new family is not warranted. Hand this round to the code-driven coverage search over the full iterative ranges, seeded with the current front, to map the whole trade-off curve.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 4338 (gain this round: n/a (first round)).
Feasible designs: 58 of 100 evaluations (44 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: pipelined, pipelined_m.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 16.9
- max_abs_err <= 0.000976562: 42% violate; best seen 8.08e-05 (2^-13.60)

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=12 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=260, accuracy_bits=10.1, luts=163, ffs=97, throughput_msps=13.2, max_abs_err=0.000887 (2^-10.14), power_index=0.146
- iterative [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=263, accuracy_bits=10.5, luts=167, ffs=96, throughput_msps=13.2, max_abs_err=0.000712 (2^-10.46), power_index=0.148
- iterative [data_width=16 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=278, accuracy_bits=11.4, luts=180, ffs=98, throughput_msps=10.4, max_abs_err=0.000375 (2^-11.38), power_index=0.198
- iterative [data_width=16 n_iter=17 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=289, accuracy_bits=11.4, luts=192, ffs=97, throughput_msps=8.1, max_abs_err=0.000373 (2^-11.39), power_index=0.217
- iterative [data_width=17 n_iter=13 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=293, accuracy_bits=11.6, luts=191, ffs=102, throughput_msps=12.4, max_abs_err=0.000326 (2^-11.58), power_index=0.176
- iterative [data_width=18 n_iter=15 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=296, accuracy_bits=12.2, luts=191, ffs=105, throughput_msps=11, max_abs_err=0.000211 (2^-12.21), power_index=0.2
- iterative [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=299, accuracy_bits=12.4, luts=193, ffs=106, throughput_msps=10.4, max_abs_err=0.000182 (2^-12.43), power_index=0.214
- iterative [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=311, accuracy_bits=12.8, luts=203, ffs=108, throughput_msps=10.2, max_abs_err=0.000136 (2^-12.84), power_index=0.222
- iterative [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=313, accuracy_bits=13.2, luts=204, ffs=109, throughput_msps=10.2, max_abs_err=0.000104 (2^-13.23), power_index=0.224
- iterative [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=325, accuracy_bits=13.6, luts=214, ffs=111, throughput_msps=10.2, max_abs_err=8.08e-05 (2^-13.60), power_index=0.232
Front coverage: luts_plus_ffs 260..325 (HV reference 1500); accuracy_bits 10.1..13.6 (HV reference 10); data_width on the front 16..18 (registry 8..28).

Per family:
- iterative: 60 evals, 36 feasible; max throughput seen 16.9 MSPS; best accuracy 13.60 bits; best feasible luts_plus_ffs=260; feasible ranges: data_width 16..18, n_iter 12..17, angle_guard -1..1, frac_guard 0..2
- unrolled_k: 40 evals, 22 feasible; max throughput seen 14 MSPS; best accuracy 12.51 bits; best feasible luts_plus_ffs=357; feasible ranges: data_width 15..18, n_iter 12..15, angle_guard -1..2, frac_guard 0..2, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=15..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (10 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 155 feasible; hypervolume 1.466e+04 (+237.8%).

**LLM decision:** `add_family` — The front is entirely iterative: 25/25 Pareto designs are iterative, with luts_plus_ffs 260..652 and accuracy_bits 10.1..23.8. The selection rule is min luts_plus_ffs, and the best feasible area is 260 (iterative W=16 N=12), but the throughput constraint is only >=1 MSPS while iterative already reaches 13.2 MSPS at that point — so the pipelined families, which trade area for 1 result/cycle, have never been tested and could plausibly beat 260 LUTs+FFs at the low-accuracy corner (accuracy_bits ~10.1 is only just above the 10-bit HV reference and the 2^-10 error limit). unrolled_k is dominated so far (best 357 area, best 12.51 bits), so the remaining budget is better spent opening pipelined and pipelined_m at small data_width / small n_iter, where the area-optimal corner lives.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.466e+04 (gain this round: +237.8%).
Feasible designs: 155 of 200 evaluations (134 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: pipelined, pipelined_m.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 16.9
- max_abs_err <= 0.000976562: 22% violate; best seen 6.73e-08 (2^-23.82)

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=12 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=260, accuracy_bits=10.1, luts=163, ffs=97, throughput_msps=13.2, max_abs_err=0.000887 (2^-10.14), power_index=0.146
- iterative [data_width=16 n_iter=17 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=289, accuracy_bits=11.4, luts=192, ffs=97, throughput_msps=8.1, max_abs_err=0.000373 (2^-11.39), power_index=0.217
- iterative [data_width=18 n_iter=15 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=296, accuracy_bits=12.2, luts=191, ffs=105, throughput_msps=11, max_abs_err=0.000211 (2^-12.21), power_index=0.2
- iterative [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=311, accuracy_bits=12.8, luts=203, ffs=108, throughput_msps=10.2, max_abs_err=0.000136 (2^-12.84), power_index=0.222
- iterative [data_width=18 n_iter=28 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=340, accuracy_bits=13.7, luts=231, ffs=109, throughput_msps=5.13, max_abs_err=7.75e-05 (2^-13.65), power_index=0.396
- iterative [data_width=18 n_iter=18 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=363, accuracy_bits=14.3, luts=248, ffs=115, throughput_msps=7.57, max_abs_err=4.84e-05 (2^-14.33), power_index=0.286
- iterative [data_width=21 n_iter=28 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=413, accuracy_bits=16.4, luts=287, ffs=126, throughput_msps=5.03, max_abs_err=1.15e-05 (2^-16.41), power_index=0.482
- iterative [data_width=26 n_iter=28 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=508, accuracy_bits=20, luts=360, ffs=148, throughput_msps=4.94, max_abs_err=9.39e-07 (2^-20.02), power_index=0.593
- iterative [data_width=28 n_iter=28 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=571, accuracy_bits=22.9, luts=413, ffs=158, throughput_msps=4.94, max_abs_err=1.32e-07 (2^-22.85), power_index=0.666
- iterative [data_width=28 n_iter=28 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=652, accuracy_bits=23.8, luts=491, ffs=161, throughput_msps=4.94, max_abs_err=6.73e-08 (2^-23.82), power_index=0.761
Front coverage: luts_plus_ffs 260..652 (HV reference 1500); accuracy_bits 10.1..23.8 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- iterative: 160 evals, 133 feasible; max throughput seen 16.9 MSPS; best accuracy 23.82 bits; best feasible luts_plus_ffs=260; feasible ranges: data_width 15..28, n_iter 11..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 40 evals, 22 feasible; max throughput seen 14 MSPS; best accuracy 12.51 bits; best feasible luts_plus_ffs=357; feasible ranges: data_width 15..18, n_iter 12..15, angle_guard -1..2, frac_guard 0..2, k 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Open the two unexplored pipelined families at the small-area corner and keep a small iterative probe on the incumbent best point.*)
- `pipelined` (51 evals): data_width=14..20, n_iter=10..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Untested family; 1 result/cycle easily clears 1 MSPS, so the question is whether its area at accuracy_bits ~10-13 can undercut iterative's 260.
- `pipelined_m` (33 evals): data_width=14..20, n_iter=10..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* Register-every-m variant may hit a lower area than full pipelining while still meeting 1 MSPS; m is the key knob for that trade.
- `iterative` (16 evals): data_width=15..18, n_iter=11..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Keep pressure on the current area-optimal corner (260 at W=16 N=12) so the low-area end of the front is not lost while the new families are probed.

**Result (code):** 100 evaluations this round, 300 total; 231 feasible; hypervolume 1.466e+04 (+0.0%).

**LLM decision:** `map_front` — Round 3 closed with +0.0% hypervolume gain and 231/300 feasible (199 unique) — the front has stopped improving, and 300/400 evals are spent, so this final round should go to code's reserved full-range front mapping. The Pareto front is currently entirely the `iterative` family (26 designs), covering luts_plus_ffs 260..652 and accuracy_bits 10.1..23.8, but only a modest slice of the data_width 8..28 registry range actually appears as extreme points; a seeded NSGA-II sweep over the full `iterative` ranges (data_width 8..28, n_iter 4..30, angle_guard -2..4, frac_guard 0..4, both roundings) is the cheapest way to fill in unsampled corners and confirm whether anything beats the current min-area point (iterative data_width=16 n_iter=12 angle_guard=1 frac_guard=0 trunc, luts_plus_ffs=260, accuracy_bits=10.1, max_abs_err=0.000887 within the 2^-10 constraint) or extends accuracy past 23.8 bits. No other registry family is relevant to this spec: they are all dominated on the min-luts_plus_ffs objective (unrolled_k best 357, pipelined 1409, pipelined_m 870 vs iterative 260), and their throughput advantage (up to 273 MSPS) is worthless because the only throughput requirement is >=1 MSPS, already met ~13x by the selected design. Constraints are comfortably reachable, so no infeasibility.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.466e+04 (gain this round: +0.0%).
Feasible designs: 231 of 300 evaluations (199 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 273
- max_abs_err <= 0.000976562: 23% violate; best seen 6.73e-08 (2^-23.82)

Pareto front (feasible, 26 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=12 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=260, accuracy_bits=10.1, luts=163, ffs=97, throughput_msps=13.2, max_abs_err=0.000887 (2^-10.14), power_index=0.146
- iterative [data_width=16 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=278, accuracy_bits=11.4, luts=180, ffs=98, throughput_msps=10.4, max_abs_err=0.000375 (2^-11.38), power_index=0.198
- iterative [data_width=18 n_iter=15 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=296, accuracy_bits=12.2, luts=191, ffs=105, throughput_msps=11, max_abs_err=0.000211 (2^-12.21), power_index=0.2
- iterative [data_width=17 n_iter=16 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=301, accuracy_bits=12.7, luts=196, ffs=105, throughput_msps=10.2, max_abs_err=0.000146 (2^-12.74), power_index=0.215
- iterative [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=325, accuracy_bits=13.6, luts=214, ffs=111, throughput_msps=10.2, max_abs_err=8.08e-05 (2^-13.60), power_index=0.232
- iterative [data_width=18 n_iter=18 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=363, accuracy_bits=14.3, luts=248, ffs=115, throughput_msps=7.57, max_abs_err=4.84e-05 (2^-14.33), power_index=0.286
- iterative [data_width=21 n_iter=28 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=413, accuracy_bits=16.4, luts=287, ffs=126, throughput_msps=5.03, max_abs_err=1.15e-05 (2^-16.41), power_index=0.482
- iterative [data_width=22 n_iter=20 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=447, accuracy_bits=17.8, luts=312, ffs=135, throughput_msps=6.78, max_abs_err=4.4e-06 (2^-17.79), power_index=0.387
- iterative [data_width=28 n_iter=28 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=571, accuracy_bits=22.9, luts=413, ffs=158, throughput_msps=4.94, max_abs_err=1.32e-07 (2^-22.85), power_index=0.666
- iterative [data_width=28 n_iter=28 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=652, accuracy_bits=23.8, luts=491, ffs=161, throughput_msps=4.94, max_abs_err=6.73e-08 (2^-23.82), power_index=0.761
Front coverage: luts_plus_ffs 260..652 (HV reference 1500); accuracy_bits 10.1..23.8 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 176 evals, 146 feasible; max throughput seen 16.9 MSPS; best accuracy 23.82 bits; best feasible luts_plus_ffs=260; feasible ranges: data_width 15..28, n_iter 11..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 40 evals, 22 feasible; max throughput seen 14 MSPS; best accuracy 12.51 bits; best feasible luts_plus_ffs=357; feasible ranges: data_width 15..18, n_iter 12..15, angle_guard -1..2, frac_guard 0..2, k 2..4
- pipelined: 51 evals, 40 feasible; max throughput seen 273 MSPS; best accuracy 14.50 bits; best feasible luts_plus_ffs=1409; feasible ranges: data_width 15..20, n_iter 12..17, angle_guard -2..2, frac_guard 0..2
- pipelined_m: 33 evals, 23 feasible; max throughput seen 164 MSPS; best accuracy 14.83 bits; best feasible luts_plus_ffs=870; feasible ranges: data_width 16..20, n_iter 12..17, angle_guard -2..2, frac_guard 0..2, m 3..8
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=14..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (26 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 319 feasible; hypervolume 1.492e+04 (+1.8%).

**LLM decision:** `stop` — Final round (4/4) and the full 400-eval budget is spent, so no further search is possible. The spec is satisfiable: 319/400 evaluations are feasible (273 unique), and the front contains a design that meets the low_area_control spec on every constraint — iterative [data_width=16 n_iter=12 angle_guard=1 frac_guard=0 rounding=trunc] at luts_plus_ffs=260, accuracy_bits=10.1 (max_abs_err=8.87e-4 = 2^-10.14 <= 2^-10) with throughput 13.2 MSPS >= 1 MSPS. That same design is also the spec's selection winner (min luts_plus_ffs). Hypervolume is 1.492e4 with only +1.8% gain in the last round, and all four families have already been sampled with their feasible ranges mapped, so the front is converged rather than truncated by unexplored territory. Feasible accuracy (10.1..24 bits) and area (260..658 LUT+FF, vs HV ref 1500) both comfortably bracket the reference point, and accuracy is exact bit-accurate model output, not an estimate. No constraint is unreachable, so infeasible is not warranted.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.492e+04 (gain this round: +1.8%).
Feasible designs: 319 of 400 evaluations (273 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 273
- max_abs_err <= 0.000976562: 20% violate; best seen 5.86e-08 (2^-24.02)

Pareto front (feasible, 40 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=12 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=260, accuracy_bits=10.1, luts=163, ffs=97, throughput_msps=13.2, max_abs_err=0.000887 (2^-10.14), power_index=0.146
- iterative [data_width=16 n_iter=17 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=289, accuracy_bits=11.4, luts=192, ffs=97, throughput_msps=8.1, max_abs_err=0.000373 (2^-11.39), power_index=0.217
- iterative [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=311, accuracy_bits=12.8, luts=203, ffs=108, throughput_msps=10.2, max_abs_err=0.000136 (2^-12.84), power_index=0.222
- iterative [data_width=18 n_iter=17 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=354, accuracy_bits=13.8, luts=242, ffs=112, throughput_msps=7.95, max_abs_err=6.92e-05 (2^-13.82), power_index=0.266
- iterative [data_width=19 n_iter=27 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=368, accuracy_bits=14.7, luts=252, ffs=116, throughput_msps=5.2, max_abs_err=3.74e-05 (2^-14.71), power_index=0.415
- iterative [data_width=20 n_iter=25 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=427, accuracy_bits=16.6, luts=301, ffs=126, throughput_msps=5.57, max_abs_err=1e-05 (2^-16.61), power_index=0.45
- iterative [data_width=23 n_iter=27 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=464, accuracy_bits=18.3, luts=325, ffs=138, throughput_msps=5.11, max_abs_err=3.08e-06 (2^-18.31), power_index=0.523
- iterative [data_width=26 n_iter=27 angle_guard=4 frac_guard=0 rounding=trunc] luts_plus_ffs=517, accuracy_bits=20.1, luts=365, ffs=151, throughput_msps=5.11, max_abs_err=8.79e-07 (2^-20.12), power_index=0.583
- iterative [data_width=28 n_iter=28 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=571, accuracy_bits=22.9, luts=413, ffs=158, throughput_msps=4.94, max_abs_err=1.32e-07 (2^-22.85), power_index=0.666
- iterative [data_width=28 n_iter=27 angle_guard=4 frac_guard=1 rounding=round] luts_plus_ffs=658, accuracy_bits=24, luts=495, ffs=163, throughput_msps=5.02, max_abs_err=5.86e-08 (2^-24.02), power_index=0.742
Front coverage: luts_plus_ffs 260..658 (HV reference 1500); accuracy_bits 10.1..24 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 276 evals, 234 feasible; max throughput seen 16.9 MSPS; best accuracy 24.02 bits; best feasible luts_plus_ffs=260; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 40 evals, 22 feasible; max throughput seen 14 MSPS; best accuracy 12.51 bits; best feasible luts_plus_ffs=357; feasible ranges: data_width 15..18, n_iter 12..15, angle_guard -1..2, frac_guard 0..2, k 2..4
- pipelined: 51 evals, 40 feasible; max throughput seen 273 MSPS; best accuracy 14.50 bits; best feasible luts_plus_ffs=1409; feasible ranges: data_width 15..20, n_iter 12..17, angle_guard -2..2, frac_guard 0..2
- pipelined_m: 33 evals, 23 feasible; max throughput seen 164 MSPS; best accuracy 14.83 bits; best feasible luts_plus_ffs=870; feasible ranges: data_width 16..20, n_iter 12..17, angle_guard -2..2, frac_guard 0..2, m 3..8
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 28473 in, 17732 out
- provider-reported cost: $0.0181
- full prompts and replies: `llm_trace.jsonl`

