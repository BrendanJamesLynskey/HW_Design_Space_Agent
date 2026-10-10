# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
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
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=16,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 170 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 96 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 10.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 19 | exact: schedule |
| latency_ns | 95.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.19 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000643 (2^-10.60) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 10.5 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.00014 (2^-12.80) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 2.29 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.6 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (27 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=16,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc` | 170 | 96 | 10.4 | 19 | 0.19 | 0.000643 (2^-10.60) | 10.60 |
| 1 | `iterative:data_width=16,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 178 | 96 | 11.0 | 18 | 0.185 | 0.000373 (2^-11.39) | 11.39 |
| 2 | `iterative:data_width=16,n_iter=16,angle_guard=3,frac_guard=0,rounding=round` | 183 | 99 | 10.2 | 19 | 0.201 | 0.000285 (2^-11.78) | 11.78 |
| 3 | `iterative:data_width=17,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 189 | 101 | 11.0 | 18 | 0.196 | 0.000251 (2^-11.96) | 11.96 |
| 4 | `iterative:data_width=18,n_iter=14,angle_guard=3,frac_guard=2,rounding=trunc` | 218 | 113 | 11.4 | 17 | 0.211 | 0.000151 (2^-12.69) | 12.69 |
| 5 | `iterative:data_width=18,n_iter=15,angle_guard=4,frac_guard=2,rounding=trunc` | 219 | 114 | 10.8 | 18 | 0.226 | 9.41e-05 (2^-13.38) | 13.38 |
| 6 | `iterative:data_width=21,n_iter=15,angle_guard=-2,frac_guard=0,rounding=round` | 231 | 119 | 10.8 | 18 | 0.237 | 9.08e-05 (2^-13.43) | 13.43 |
| 7 | `iterative:data_width=21,n_iter=16,angle_guard=1,frac_guard=0,rounding=trunc` | 229 | 122 | 10.2 | 19 | 0.251 | 4.46e-05 (2^-14.45) | 14.45 |
| 8 | `iterative:data_width=21,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 237 | 122 | 10.2 | 19 | 0.256 | 3.91e-05 (2^-14.64) | 14.64 |
| 9 | `iterative:data_width=22,n_iter=16,angle_guard=1,frac_guard=1,rounding=trunc` | 250 | 129 | 10.0 | 19 | 0.271 | 3.34e-05 (2^-14.87) | 14.87 |
| 10 | `iterative:data_width=21,n_iter=20,angle_guard=1,frac_guard=0,rounding=round` | 274 | 123 | 6.9 | 23 | 0.343 | 1.21e-05 (2^-16.34) | 16.34 |
| 11 | `iterative:data_width=22,n_iter=21,angle_guard=4,frac_guard=2,rounding=trunc` | 321 | 135 | 6.5 | 24 | 0.411 | 3.58e-06 (2^-18.09) | 18.09 |
| 12 | `iterative:data_width=24,n_iter=21,angle_guard=1,frac_guard=0,rounding=trunc` | 319 | 138 | 6.5 | 24 | 0.413 | 3.19e-06 (2^-18.26) | 18.26 |
| 13 | `iterative:data_width=24,n_iter=25,angle_guard=1,frac_guard=0,rounding=trunc` | 322 | 138 | 5.6 | 28 | 0.485 | 2.96e-06 (2^-18.37) | 18.37 |
| 14 | `iterative:data_width=24,n_iter=25,angle_guard=0,frac_guard=0,rounding=round` | 335 | 137 | 5.6 | 28 | 0.497 | 2.49e-06 (2^-18.62) | 18.62 |
| 15 | `iterative:data_width=24,n_iter=25,angle_guard=1,frac_guard=0,rounding=round` | 337 | 138 | 5.6 | 28 | 0.5 | 1.76e-06 (2^-19.12) | 19.12 |
| 16 | `iterative:data_width=24,n_iter=26,angle_guard=1,frac_guard=0,rounding=round` | 337 | 138 | 5.4 | 29 | 0.518 | 1.76e-06 (2^-19.12) | 19.12 |
| 17 | `iterative:data_width=25,n_iter=25,angle_guard=0,frac_guard=0,rounding=trunc` | 339 | 142 | 5.6 | 28 | 0.507 | 1.65e-06 (2^-19.21) | 19.21 |
| 18 | `iterative:data_width=24,n_iter=25,angle_guard=1,frac_guard=2,rounding=trunc` | 356 | 142 | 5.6 | 28 | 0.525 | 1.23e-06 (2^-19.63) | 19.63 |
| 19 | `iterative:data_width=25,n_iter=28,angle_guard=1,frac_guard=1,rounding=trunc` | 358 | 145 | 5.0 | 31 | 0.587 | 1.13e-06 (2^-19.76) | 19.76 |
| 20 | `iterative:data_width=24,n_iter=25,angle_guard=4,frac_guard=2,rounding=trunc` | 362 | 145 | 5.5 | 28 | 0.534 | 8.38e-07 (2^-20.19) | 20.19 |
| 21 | `iterative:data_width=25,n_iter=25,angle_guard=1,frac_guard=2,rounding=trunc` | 375 | 147 | 5.5 | 28 | 0.55 | 6.67e-07 (2^-20.52) | 20.52 |
| 22 | `iterative:data_width=24,n_iter=25,angle_guard=4,frac_guard=2,rounding=round` | 427 | 145 | 5.5 | 28 | 0.603 | 4.57e-07 (2^-21.06) | 21.06 |
| 23 | `iterative:data_width=25,n_iter=30,angle_guard=3,frac_guard=1,rounding=round` | 431 | 147 | 4.6 | 33 | 0.718 | 4.07e-07 (2^-21.23) | 21.23 |
| 24 | `iterative:data_width=28,n_iter=25,angle_guard=-1,frac_guard=2,rounding=trunc` | 429 | 160 | 5.5 | 28 | 0.62 | 2.64e-07 (2^-21.85) | 21.85 |
| 25 | `iterative:data_width=28,n_iter=28,angle_guard=-1,frac_guard=4,rounding=trunc` | 463 | 164 | 4.9 | 31 | 0.732 | 2.49e-07 (2^-21.94) | 21.94 |
| 26 | `iterative:data_width=28,n_iter=28,angle_guard=1,frac_guard=3,rounding=round` | 523 | 164 | 4.9 | 31 | 0.802 | 7.8e-08 (2^-23.61) | 23.61 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The merged front is 18/18 iterative and the smallest feasible area found anywhere is iterative at 261 LUTs+FFs; unrolled_k's best is 363 and it has never reached the front. The throughput constraint is trivially satisfied by both my families (iterative needs N+3 cycles/result, so even N=20 at a modest Fmax clears 1 MSPS by a wide margin), so the only live axis is area vs accuracy. I therefore put almost all of my budget into iterative: refine the small-area corner (where the selection rule min luts_plus_ffs will pick) and extend the accuracy end of the front out toward the HV reference area of 1500 so the hypervolume covers the whole curve. I keep a small unrolled_k share only to confirm there is no niche (e.g. very small N) where its extra barrel shifters pay off; structurally it should be dominated because it replicates the shifter k times while iterative shares one.*)
- `iterative` (85 evals): data_width=10..22, n_iter=6..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Owns the entire merged front and the global best area (261 LUTs+FFs). Accuracy depends only on W, N, angle_guard, frac_guard, rounding, so I search the full guard/rounding space and sweep W from the feasibility boundary (~12, where output LSB 2^-(W-2) starts to clear 2^-10) up to 22 to push accuracy_bits toward the HV reference of 10 and area toward 1500. n_iter is capped at 20 because CORDIC residual error saturates near W bits, so larger N only burns cycles/area without buying accuracy.
- `unrolled_k` (15 evals): data_width=10..18, n_iter=6..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..4. *Why:* Kept only as a cheap confirmation. It meets the constraints but is structurally dominated by iterative for this spec: it instantiates k barrel shifters against iterative's single shared shifter for the same N, and its only advantage (ceil(N/k)+3 cycles) is irrelevant because throughput is not the binding constraint. I restrict it to small k (2..4) and small W/N where the area penalty is smallest, in case a very short schedule lets a tiny-N design slip under iterative on LUTs+FFs.

**Result (code):** 100 evaluations this round, 100 total; 58 feasible; hypervolume 7373 (n/a).

**LLM decision:** `map_front` — Round 1 mapped only the iterative family, and the feasible front is narrow relative to the registry: accuracy_bits spans 10.6..16.3 while the registry allows up to 28, and luts_plus_ffs spans 266..397 against an HV reference of 1500, so most of the dominated region is still empty. The low-area corner is already well pinned (best feasible luts_plus_ffs=266 at accuracy 10.6, just above the 2^-10 constraint), and the constraint throughput_msps>=1 is met with huge margin (best 22 MSPS), so the remaining HV gain is in extending the front toward higher accuracy and confirming the area floor. With 100 of 200 evals left, spending this round on NSGA-II over the full ranges of the family already on the front (iterative, seeded with the 12-design front) is the best use of budget before any family expansion; unrolled_k showed only 2 feasible designs and no better area, and pipelined/pipelined_m are unlikely to help a min-area objective.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 7373 (gain this round: n/a (first round)).
Feasible designs: 58 of 100 evaluations (49 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 22
- max_abs_err <= 0.000976562: 42% violate; best seen 1.21e-05 (2^-16.34)

Pareto front (feasible, 12 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=266, accuracy_bits=10.6, luts=170, ffs=96, throughput_msps=10.4, max_abs_err=0.000643 (2^-10.60), power_index=0.19
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=280, accuracy_bits=11.1, luts=181, ffs=99, throughput_msps=12.4, max_abs_err=0.00046 (2^-11.09), power_index=0.169
- iterative [data_width=16 n_iter=16 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=282, accuracy_bits=11.8, luts=183, ffs=99, throughput_msps=10.2, max_abs_err=0.000285 (2^-11.78), power_index=0.201
- iterative [data_width=18 n_iter=14 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=331, accuracy_bits=12.7, luts=218, ffs=113, throughput_msps=11.4, max_abs_err=0.000151 (2^-12.69), power_index=0.211
- iterative [data_width=20 n_iter=15 angle_guard=-2 frac_guard=0 rounding=round] luts_plus_ffs=334, accuracy_bits=13, luts=220, ffs=114, throughput_msps=10.8, max_abs_err=0.00012 (2^-13.02), power_index=0.226
- iterative [data_width=18 n_iter=16 angle_guard=0 frac_guard=3 rounding=trunc] luts_plus_ffs=334, accuracy_bits=13.1, luts=222, ffs=112, throughput_msps=10.2, max_abs_err=0.00011 (2^-13.15), power_index=0.239
- iterative [data_width=21 n_iter=15 angle_guard=-2 frac_guard=0 rounding=round] luts_plus_ffs=350, accuracy_bits=13.4, luts=231, ffs=119, throughput_msps=10.8, max_abs_err=9.08e-05 (2^-13.43), power_index=0.237
- iterative [data_width=21 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=359, accuracy_bits=14.6, luts=237, ffs=122, throughput_msps=10.2, max_abs_err=3.91e-05 (2^-14.64), power_index=0.256
- iterative [data_width=22 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=379, accuracy_bits=14.9, luts=250, ffs=129, throughput_msps=9.97, max_abs_err=3.34e-05 (2^-14.87), power_index=0.271
- iterative [data_width=21 n_iter=20 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=397, accuracy_bits=16.3, luts=274, ffs=123, throughput_msps=6.91, max_abs_err=1.21e-05 (2^-16.34), power_index=0.343
Front coverage: luts_plus_ffs 266..397 (HV reference 1500); accuracy_bits 10.6..16.3 (HV reference 10); data_width on the front 16..22 (registry 8..28).

Per family:
- iterative: 85 evals, 56 feasible; max throughput seen 22 MSPS; best accuracy 16.34 bits; best feasible luts_plus_ffs=266; feasible ranges: data_width 15..22, n_iter 12..20, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 15 evals, 2 feasible; max throughput seen 19.8 MSPS; best accuracy 11.10 bits; best feasible luts_plus_ffs=411; feasible ranges: data_width 17..17, n_iter 13..13, angle_guard -1..-1, frac_guard 0..1, k 3..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `iterative` (20 evals): data_width=15..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (12 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 78 feasible; hypervolume 1.242e+04 (+68.4%).

**LLM decision:** `map_front` — The iterative family dominates: 76/105 feasible, best luts_plus_ffs=266 and accuracy up to 21.7 bits, while unrolled_k produced only 2 feasible designs (best area 411) and no pipelined/pipelined_m coverage at all. The spec's selection rule is min luts_plus_ffs, and the current front's low-area corner (266 LUTs+FFs, 10.6 bits) sits right at the accuracy constraint (2^-10.60 vs required 2^-10), so the true minimum-area feasible point is likely just below the current front and needs denser sampling. Accuracy on the front spans 10.6..21.7 bits but the HV reference for accuracy is only 10, so most of the accuracy range contributes little to hypervolume while the area axis (266..606 vs ref 1500) is where gains remain. A code-driven NSGA-II coverage pass over the full ranges of iterative (and unrolled_k/pipelined_m as cheap alternatives for the throughput constraint) will map the whole trade-off curve and find the true low-area corner before the final selection.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.242e+04 (gain this round: +68.4%).
Feasible designs: 78 of 120 evaluations (67 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 22
- max_abs_err <= 0.000976562: 35% violate; best seen 2.87e-07 (2^-21.73)

Pareto front (feasible, 14 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=266, accuracy_bits=10.6, luts=170, ffs=96, throughput_msps=10.4, max_abs_err=0.000643 (2^-10.60), power_index=0.19
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.4, luts=178, ffs=96, throughput_msps=11, max_abs_err=0.000373 (2^-11.39), power_index=0.185
- iterative [data_width=17 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=290, accuracy_bits=12, luts=189, ffs=101, throughput_msps=11, max_abs_err=0.000251 (2^-11.96), power_index=0.196
- iterative [data_width=18 n_iter=14 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=331, accuracy_bits=12.7, luts=218, ffs=113, throughput_msps=11.4, max_abs_err=0.000151 (2^-12.69), power_index=0.211
- iterative [data_width=18 n_iter=16 angle_guard=0 frac_guard=3 rounding=trunc] luts_plus_ffs=334, accuracy_bits=13.1, luts=222, ffs=112, throughput_msps=10.2, max_abs_err=0.00011 (2^-13.15), power_index=0.239
- iterative [data_width=21 n_iter=15 angle_guard=-2 frac_guard=0 rounding=round] luts_plus_ffs=350, accuracy_bits=13.4, luts=231, ffs=119, throughput_msps=10.8, max_abs_err=9.08e-05 (2^-13.43), power_index=0.237
- iterative [data_width=21 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=359, accuracy_bits=14.6, luts=237, ffs=122, throughput_msps=10.2, max_abs_err=3.91e-05 (2^-14.64), power_index=0.256
- iterative [data_width=22 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=379, accuracy_bits=14.9, luts=250, ffs=129, throughput_msps=9.97, max_abs_err=3.34e-05 (2^-14.87), power_index=0.271
- iterative [data_width=23 n_iter=22 angle_guard=4 frac_guard=2 rounding=round] luts_plus_ffs=540, accuracy_bits=19.6, luts=400, ffs=140, throughput_msps=6.13, max_abs_err=1.25e-06 (2^-19.61), power_index=0.508
- iterative [data_width=27 n_iter=25 angle_guard=0 frac_guard=4 rounding=trunc] luts_plus_ffs=606, accuracy_bits=21.7, luts=446, ffs=160, throughput_msps=5.38, max_abs_err=2.87e-07 (2^-21.73), power_index=0.638
Front coverage: luts_plus_ffs 266..606 (HV reference 1500); accuracy_bits 10.6..21.7 (HV reference 10); data_width on the front 16..27 (registry 8..28).

Per family:
- iterative: 105 evals, 76 feasible; max throughput seen 22 MSPS; best accuracy 21.73 bits; best feasible luts_plus_ffs=266; feasible ranges: data_width 15..27, n_iter 12..28, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 15 evals, 2 feasible; max throughput seen 19.8 MSPS; best accuracy 11.10 bits; best feasible luts_plus_ffs=411; feasible ranges: data_width 17..17, n_iter 13..13, angle_guard -1..-1, frac_guard 0..1, k 3..3
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `iterative` (80 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (14 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 156 feasible; hypervolume 1.432e+04 (+15.4%).

**LLM decision:** `stop` — Final round and the 200-eval budget is fully spent (200/200, round 3 of 4), so no further refinement, widening, adding or full-front mapping can be paid for. The spec is met with margin: throughput constraint has 0% violations (best 22 MSPS vs >=1 MSPS required) and accuracy has feasible designs down to max_abs_err 7.8e-08 (2^-23.61), far below the 2^-10 = 9.77e-04 limit. The feasible Pareto front is broad and well-covered (27 designs, luts_plus_ffs 266..688 against HV ref 1500, accuracy_bits 10.6..23.6 against HV ref 10), hypervolume 1.432e+04 with a +15.4% gain this round, so the trade-off curve is mapped reasonably for the budget. The selection rule (min luts_plus_ffs) picks iterative [data_width=16 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc] at 266 LUTs+FFs with accuracy_bits=10.6 (max_abs_err 6.43e-04 <= 9.77e-04) and 10.4 MSPS, which is feasible. The family space is exhausted too: iterative and unrolled_k both explored, no unexplored family left. No constraint is unreachable, so infeasible is not justified; stop is.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.432e+04 (gain this round: +15.4%).
Feasible designs: 156 of 200 evaluations (141 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 22
- max_abs_err <= 0.000976562: 22% violate; best seen 7.8e-08 (2^-23.61)

Pareto front (feasible, 27 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=266, accuracy_bits=10.6, luts=170, ffs=96, throughput_msps=10.4, max_abs_err=0.000643 (2^-10.60), power_index=0.19
- iterative [data_width=17 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=290, accuracy_bits=12, luts=189, ffs=101, throughput_msps=11, max_abs_err=0.000251 (2^-11.96), power_index=0.196
- iterative [data_width=21 n_iter=15 angle_guard=-2 frac_guard=0 rounding=round] luts_plus_ffs=350, accuracy_bits=13.4, luts=231, ffs=119, throughput_msps=10.8, max_abs_err=9.08e-05 (2^-13.43), power_index=0.237
- iterative [data_width=22 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=379, accuracy_bits=14.9, luts=250, ffs=129, throughput_msps=9.97, max_abs_err=3.34e-05 (2^-14.87), power_index=0.271
- iterative [data_width=24 n_iter=21 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=457, accuracy_bits=18.3, luts=319, ffs=138, throughput_msps=6.5, max_abs_err=3.19e-06 (2^-18.26), power_index=0.413
- iterative [data_width=24 n_iter=25 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=472, accuracy_bits=18.6, luts=335, ffs=137, throughput_msps=5.57, max_abs_err=2.49e-06 (2^-18.62), power_index=0.497
- iterative [data_width=25 n_iter=25 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=481, accuracy_bits=19.2, luts=339, ffs=142, throughput_msps=5.57, max_abs_err=1.65e-06 (2^-19.21), power_index=0.507
- iterative [data_width=24 n_iter=25 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=507, accuracy_bits=20.2, luts=362, ffs=145, throughput_msps=5.47, max_abs_err=8.38e-07 (2^-20.19), power_index=0.534
- iterative [data_width=25 n_iter=30 angle_guard=3 frac_guard=1 rounding=round] luts_plus_ffs=578, accuracy_bits=21.2, luts=431, ffs=147, throughput_msps=4.64, max_abs_err=4.07e-07 (2^-21.23), power_index=0.718
- iterative [data_width=28 n_iter=28 angle_guard=1 frac_guard=3 rounding=round] luts_plus_ffs=688, accuracy_bits=23.6, luts=523, ffs=164, throughput_msps=4.86, max_abs_err=7.8e-08 (2^-23.61), power_index=0.802
Front coverage: luts_plus_ffs 266..688 (HV reference 1500); accuracy_bits 10.6..23.6 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- iterative: 185 evals, 154 feasible; max throughput seen 22 MSPS; best accuracy 23.61 bits; best feasible luts_plus_ffs=266; feasible ranges: data_width 15..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 15 evals, 2 feasible; max throughput seen 19.8 MSPS; best accuracy 11.10 bits; best feasible luts_plus_ffs=411; feasible ranges: data_width 17..17, n_iter 13..13, angle_guard -1..-1, frac_guard 0..1, k 3..3
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 11111 in, 6411 out
- provider-reported cost: $0.0058
- full prompts and replies: `llm_trace.jsonl`

