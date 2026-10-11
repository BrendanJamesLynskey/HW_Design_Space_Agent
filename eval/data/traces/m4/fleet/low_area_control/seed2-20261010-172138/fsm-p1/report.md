# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
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
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=17,n_iter=15,angle_guard=-2,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 197 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 103 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 194 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 10.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 92.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.203 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000639 (2^-10.61) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 20.9 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 0.000154 (2^-12.67) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 5.04 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 10.6 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (19 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=17,n_iter=15,angle_guard=-2,frac_guard=2,rounding=trunc` | 197 | 103 | 10.8 | 18 | 0.203 | 0.000639 (2^-10.61) | 10.61 |
| 1 | `iterative:data_width=18,n_iter=14,angle_guard=-1,frac_guard=0,rounding=round` | 199 | 105 | 11.7 | 17 | 0.194 | 0.000248 (2^-11.98) | 11.98 |
| 2 | `iterative:data_width=17,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc` | 203 | 106 | 10.8 | 18 | 0.209 | 0.000175 (2^-12.48) | 12.48 |
| 3 | `iterative:data_width=18,n_iter=28,angle_guard=0,frac_guard=2,rounding=trunc` | 243 | 111 | 5.1 | 31 | 0.413 | 0.000141 (2^-12.79) | 12.79 |
| 4 | `iterative:data_width=18,n_iter=24,angle_guard=2,frac_guard=2,rounding=trunc` | 247 | 113 | 5.9 | 27 | 0.366 | 6.45e-05 (2^-13.92) | 13.92 |
| 5 | `iterative:data_width=18,n_iter=24,angle_guard=4,frac_guard=2,rounding=trunc` | 251 | 115 | 5.9 | 27 | 0.371 | 5.87e-05 (2^-14.06) | 14.06 |
| 6 | `iterative:data_width=18,n_iter=24,angle_guard=2,frac_guard=3,rounding=trunc` | 263 | 115 | 5.9 | 27 | 0.384 | 4.69e-05 (2^-14.38) | 14.38 |
| 7 | `iterative:data_width=18,n_iter=28,angle_guard=3,frac_guard=3,rounding=trunc` | 265 | 116 | 5.1 | 31 | 0.444 | 4.6e-05 (2^-14.41) | 14.41 |
| 8 | `iterative:data_width=22,n_iter=17,angle_guard=0,frac_guard=0,rounding=trunc` | 276 | 127 | 7.9 | 20 | 0.303 | 2.44e-05 (2^-15.32) | 15.32 |
| 9 | `iterative:data_width=22,n_iter=17,angle_guard=0,frac_guard=0,rounding=round` | 288 | 127 | 7.9 | 20 | 0.312 | 2.12e-05 (2^-15.52) | 15.52 |
| 10 | `iterative:data_width=21,n_iter=18,angle_guard=3,frac_guard=2,rounding=trunc` | 294 | 129 | 7.4 | 21 | 0.334 | 1.24e-05 (2^-16.30) | 16.30 |
| 11 | `iterative:data_width=24,n_iter=26,angle_guard=3,frac_guard=0,rounding=trunc` | 325 | 140 | 5.3 | 29 | 0.508 | 2.96e-06 (2^-18.37) | 18.37 |
| 12 | `iterative:data_width=26,n_iter=24,angle_guard=3,frac_guard=2,rounding=trunc` | 389 | 154 | 5.7 | 27 | 0.552 | 3.21e-07 (2^-21.57) | 21.57 |
| 13 | `iterative:data_width=27,n_iter=26,angle_guard=3,frac_guard=2,rounding=trunc` | 417 | 159 | 5.3 | 29 | 0.629 | 1.26e-07 (2^-22.92) | 22.92 |
| 14 | `iterative:data_width=27,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc` | 434 | 161 | 5.3 | 29 | 0.65 | 9.63e-08 (2^-23.31) | 23.31 |
| 15 | `iterative:data_width=27,n_iter=26,angle_guard=3,frac_guard=4,rounding=trunc` | 451 | 163 | 5.2 | 29 | 0.67 | 8.5e-08 (2^-23.49) | 23.49 |
| 16 | `iterative:data_width=28,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc` | 453 | 166 | 5.2 | 29 | 0.676 | 5.73e-08 (2^-24.06) | 24.06 |
| 17 | `iterative:data_width=28,n_iter=30,angle_guard=3,frac_guard=2,rounding=round` | 517 | 164 | 4.6 | 33 | 0.846 | 3.6e-08 (2^-24.73) | 24.73 |
| 18 | `iterative:data_width=28,n_iter=30,angle_guard=3,frac_guard=3,rounding=round` | 536 | 166 | 4.6 | 33 | 0.872 | 2.91e-08 (2^-25.04) | 25.04 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-dominated (min luts_plus_ffs, selection by min luts_plus_ffs) with a hard throughput floor of 1 MSPS and a hard accuracy floor of max_abs_err <= 2^-10. Both of my assigned families (iterative, unrolled_k) produce one result every several cycles, so the throughput constraint reduces to Fmax >= (N+3)/k MHz, which is comfortably met for the N that satisfy the error bound; the binding constraints are therefore accuracy and area. I split the budget 55/45: iterative gets the larger share because it is the lowest-area family and most likely to contain the selected (min-area) design, while unrolled_k gets the remainder to populate the higher-area / higher-accuracy and lower-latency portion of the front that iterative cannot reach. I leave n_iter, data_width, and both guards at their full registry ranges in the first round so Optuna NSGA-II can discover where the accuracy floor actually binds and where the area/accuracy trade-off curve lies, rather than pre-committing to a narrow region with no prior fleet data. Rounding is left as a 2-value choice since it affects the exact error bits and is cheap to explore.*)
- `iterative` (33 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* iterative is the canonical minimum-area CORDIC datapath (single shared barrel-shifter/adder path, no per-stage registers). It is the only family here that can plausibly hit the lowest luts_plus_ffs, which is the selection objective. The throughput constraint (>=1 MSPS) is met as long as Fmax >= (N+3) MHz, which is easily satisfied for the N values that give max_abs_err <= 2^-10. I keep n_iter wide (4..30) because accuracy_bits is a maximisation objective and the Pareto front spans the accuracy-vs-area trade-off; data_width wide (8..28) since W drives both accuracy and area; guards left open so Optuna can find the cheapest guard combination that still meets the error bound.
- `unrolled_k` (27 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* unrolled_k chains k micro-rotations per cycle, cutting latency and raising Fmax headroom, but it replicates the datapath k times so luts_plus_ffs grows. It is the second family I am allowed and it adds a distinct trade-off axis (k) that iterative cannot express, so it helps cover the Pareto front where a slightly larger area buys higher accuracy_bits or lower latency at the same throughput. I keep k at its full 2..8 range so the front can show the area penalty of unrolling; n_iter/data_width/guards match iterative so the two fronts are directly comparable on the shared accuracy/area axes.

**Result (code):** 60 evaluations this round, 60 total; 40 feasible; hypervolume 1.378e+04 (n/a).

**LLM decision:** `stop` — The Pareto front is well-established and feasible. The minimum area design (iterative, luts_plus_ffs=300) meets the throughput constraint (10.8 MSPS >= 1) and the accuracy constraint (10.6 bits > 10 bits required). The front covers a wide range of accuracy (10.6 to 23.5 bits) and area (300 to 615 LUTs+FFs), providing a good trade-off curve for hypervolume. Since this is the final round, we stop to finalize the design selection based on the 'min luts_plus_ffs' rule, which picks the 300 LUTs+FFs design.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.378e+04 (gain this round: n/a (first round)).
Feasible designs: 40 of 60 evaluations (36 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 37.6
- max_abs_err <= 0.000976562: 33% violate; best seen 8.5e-08 (2^-23.49)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=17 n_iter=15 angle_guard=-2 frac_guard=2 rounding=trunc] luts_plus_ffs=300, accuracy_bits=10.6, luts=197, ffs=103, throughput_msps=10.8, max_abs_err=0.000639 (2^-10.61), power_index=0.203
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=308, accuracy_bits=12.5, luts=203, ffs=106, throughput_msps=10.8, max_abs_err=0.000175 (2^-12.48), power_index=0.209
- iterative [data_width=22 n_iter=15 angle_guard=2 frac_guard=3 rounding=round] luts_plus_ffs=459, accuracy_bits=14, luts=325, ffs=134, throughput_msps=10.5, max_abs_err=6.17e-05 (2^-13.98), power_index=0.311
- iterative [data_width=24 n_iter=26 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=466, accuracy_bits=18.4, luts=325, ffs=140, throughput_msps=5.28, max_abs_err=2.96e-06 (2^-18.37), power_index=0.508
- iterative [data_width=27 n_iter=26 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=576, accuracy_bits=22.9, luts=417, ffs=159, throughput_msps=5.28, max_abs_err=1.26e-07 (2^-22.92), power_index=0.629
- iterative [data_width=27 n_iter=26 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=595, accuracy_bits=23.3, luts=434, ffs=161, throughput_msps=5.28, max_abs_err=9.63e-08 (2^-23.31), power_index=0.65
- iterative [data_width=27 n_iter=26 angle_guard=3 frac_guard=4 rounding=trunc] luts_plus_ffs=615, accuracy_bits=23.5, luts=451, ffs=163, throughput_msps=5.19, max_abs_err=8.5e-08 (2^-23.49), power_index=0.67
Front coverage: luts_plus_ffs 300..615 (HV reference 1500); accuracy_bits 10.6..23.5 (HV reference 10); data_width on the front 17..27 (registry 8..28).

Per family:
- iterative: 33 evals, 21 feasible; max throughput seen 37.6 MSPS; best accuracy 23.49 bits; best feasible luts_plus_ffs=300; feasible ranges: data_width 17..27, n_iter 13..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 27 evals, 19 feasible; max throughput seen 19.7 MSPS; best accuracy 16.52 bits; best feasible luts_plus_ffs=730; feasible ranges: data_width 16..23, n_iter 12..30, angle_guard -1..4, frac_guard 0..4, k 5..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (40 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (7 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 80 feasible; hypervolume 1.547e+04 (+12.3%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and feasible. The minimum area design (iterative, luts_plus_ffs=300) meets the throughput constraint (10.8 MSPS >= 1) and the accuracy constraint (10.6 bits > 10 bits required). The front covers a wide range of accuracy (10.6 to 23.5 bits) and area (300 to 615 LUTs+FFs), providing a good trade-off curve for hypervolume. Since this is the final round, we stop to finalize the design selection based on the 'min luts_plus_ffs' rule, which picks the 300 LUTs+FFs design.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.547e+04 (gain this round: +12.3%).
Feasible designs: 80 of 100 evaluations (72 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 37.6
- max_abs_err <= 0.000976562: 20% violate; best seen 2.91e-08 (2^-25.04)

Pareto front (feasible, 19 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=17 n_iter=15 angle_guard=-2 frac_guard=2 rounding=trunc] luts_plus_ffs=300, accuracy_bits=10.6, luts=197, ffs=103, throughput_msps=10.8, max_abs_err=0.000639 (2^-10.61), power_index=0.203
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=308, accuracy_bits=12.5, luts=203, ffs=106, throughput_msps=10.8, max_abs_err=0.000175 (2^-12.48), power_index=0.209
- iterative [data_width=18 n_iter=24 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=360, accuracy_bits=13.9, luts=247, ffs=113, throughput_msps=5.89, max_abs_err=6.45e-05 (2^-13.92), power_index=0.366
- iterative [data_width=18 n_iter=24 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=378, accuracy_bits=14.4, luts=263, ffs=115, throughput_msps=5.89, max_abs_err=4.69e-05 (2^-14.38), power_index=0.384
- iterative [data_width=22 n_iter=17 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=403, accuracy_bits=15.3, luts=276, ffs=127, throughput_msps=7.95, max_abs_err=2.44e-05 (2^-15.32), power_index=0.303
- iterative [data_width=21 n_iter=18 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=423, accuracy_bits=16.3, luts=294, ffs=129, throughput_msps=7.43, max_abs_err=1.24e-05 (2^-16.30), power_index=0.334
- iterative [data_width=26 n_iter=24 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=543, accuracy_bits=21.6, luts=389, ffs=154, throughput_msps=5.68, max_abs_err=3.21e-07 (2^-21.57), power_index=0.552
- iterative [data_width=27 n_iter=26 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=595, accuracy_bits=23.3, luts=434, ffs=161, throughput_msps=5.28, max_abs_err=9.63e-08 (2^-23.31), power_index=0.65
- iterative [data_width=28 n_iter=26 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=619, accuracy_bits=24.1, luts=453, ffs=166, throughput_msps=5.19, max_abs_err=5.73e-08 (2^-24.06), power_index=0.676
- iterative [data_width=28 n_iter=30 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=703, accuracy_bits=25, luts=536, ffs=166, throughput_msps=4.56, max_abs_err=2.91e-08 (2^-25.04), power_index=0.872
Front coverage: luts_plus_ffs 300..703 (HV reference 1500); accuracy_bits 10.6..25 (HV reference 10); data_width on the front 17..28 (registry 8..28).

Per family:
- iterative: 73 evals, 61 feasible; max throughput seen 37.6 MSPS; best accuracy 25.04 bits; best feasible luts_plus_ffs=300; feasible ranges: data_width 17..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 27 evals, 19 feasible; max throughput seen 19.7 MSPS; best accuracy 16.52 bits; best feasible luts_plus_ffs=730; feasible ranges: data_width 16..23, n_iter 12..30, angle_guard -1..4, frac_guard 0..4, k 5..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4290 in, 1270 out
- provider-reported cost: $0.0019
- full prompts and replies: `llm_trace.jsonl`

