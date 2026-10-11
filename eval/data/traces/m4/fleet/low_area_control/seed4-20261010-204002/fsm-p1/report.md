# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`iterative:data_width=16,n_iter=20,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 192 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 97 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 162 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 7.04 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 23 | exact: schedule |
| latency_ns | 142 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.25 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000373 (2^-11.39) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 6.11 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 9.67e-05 (2^-13.34) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 1.58 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 11.4 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (15 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=16,n_iter=20,angle_guard=0,frac_guard=0,rounding=round` | 192 | 97 | 7.0 | 23 | 0.25 | 0.000373 (2^-11.39) | 11.39 |
| 1 | `iterative:data_width=16,n_iter=23,angle_guard=3,frac_guard=0,rounding=round` | 199 | 100 | 6.1 | 26 | 0.292 | 0.000285 (2^-11.78) | 11.78 |
| 2 | `iterative:data_width=18,n_iter=26,angle_guard=1,frac_guard=0,rounding=trunc` | 214 | 108 | 5.5 | 29 | 0.351 | 0.00025 (2^-11.97) | 11.97 |
| 3 | `iterative:data_width=18,n_iter=20,angle_guard=2,frac_guard=0,rounding=trunc` | 216 | 109 | 6.9 | 23 | 0.281 | 0.000179 (2^-12.45) | 12.45 |
| 4 | `iterative:data_width=18,n_iter=20,angle_guard=3,frac_guard=0,rounding=round` | 230 | 110 | 6.9 | 23 | 0.294 | 7.75e-05 (2^-13.65) | 13.65 |
| 5 | `iterative:data_width=19,n_iter=20,angle_guard=2,frac_guard=1,rounding=trunc` | 246 | 116 | 6.9 | 23 | 0.313 | 4.83e-05 (2^-14.34) | 14.34 |
| 6 | `iterative:data_width=19,n_iter=28,angle_guard=2,frac_guard=2,rounding=trunc` | 265 | 118 | 5.1 | 31 | 0.446 | 3.83e-05 (2^-14.67) | 14.67 |
| 7 | `iterative:data_width=20,n_iter=20,angle_guard=3,frac_guard=1,rounding=trunc` | 264 | 122 | 6.8 | 23 | 0.334 | 2.4e-05 (2^-15.35) | 15.35 |
| 8 | `iterative:data_width=22,n_iter=26,angle_guard=0,frac_guard=0,rounding=trunc` | 282 | 127 | 5.5 | 29 | 0.446 | 1.56e-05 (2^-15.97) | 15.97 |
| 9 | `iterative:data_width=22,n_iter=25,angle_guard=3,frac_guard=0,rounding=trunc` | 287 | 130 | 5.6 | 28 | 0.44 | 1.32e-05 (2^-16.21) | 16.21 |
| 10 | `iterative:data_width=23,n_iter=27,angle_guard=-1,frac_guard=0,rounding=trunc` | 299 | 131 | 5.2 | 30 | 0.486 | 9.92e-06 (2^-16.62) | 16.62 |
| 11 | `iterative:data_width=22,n_iter=26,angle_guard=3,frac_guard=0,rounding=round` | 303 | 130 | 5.4 | 29 | 0.472 | 5.23e-06 (2^-17.54) | 17.54 |
| 12 | `iterative:data_width=27,n_iter=28,angle_guard=-1,frac_guard=0,rounding=trunc` | 375 | 151 | 4.9 | 31 | 0.614 | 7.11e-07 (2^-20.42) | 20.42 |
| 13 | `iterative:data_width=28,n_iter=25,angle_guard=4,frac_guard=0,rounding=trunc` | 403 | 161 | 5.4 | 28 | 0.595 | 2.16e-07 (2^-22.14) | 22.14 |
| 14 | `iterative:data_width=28,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc` | 451 | 165 | 5.4 | 28 | 0.649 | 9.99e-08 (2^-23.26) | 23.26 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Throughput >= 1 MSPS is not binding for these families: iterative needs N+3 cycles and unrolled_k ceil(N/k)+3, and both stay under ~31 cycles for N<=28, i.e. tens of MHz of Fmax already clears 1 MSPS. The binding constraint is max_abs_err <= 2^-10 (accuracy_bits >= 10), which needs W near 12 and N near 12-14, with round-mode helping at the low-W edge. Accuracy depends only on (data_width, n_iter, angle_guard, frac_guard, rounding) and is family-independent, while area is family- and k-dependent; since these families share/reuse their datapath, n_iter adds essentially no area, so I push n_iter high and let the search spend area only on data_width and the guards. Ranges straddle the feasibility boundary (W=11 borderline, up to 20 for the high-accuracy end) and cover the two HV axes (area ref 1500, accuracy ref 10). rounding is swept because round roughly halves quantization error at zero area cost. unrolled_k carries the larger share because k is an extra family-specific area axis that could hold the min-area corner; iterative is kept as the reference control structure. Suggested allocation: ~60 of the 100 evals this round at these relative shares (24 iterative / 36 unrolled_k), leaving budget for a focused refinement and the mandatory full-range front-mapping pass.*)
- `iterative` (24 evals): data_width=11..20, n_iter=10..28, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round. *Why:* Cheapest control structure (one shared micro-rotation + FSM) and the natural min-area candidate for the select rule. N does not add datapath area here, so n_iter is swept to 28 to buy angle-accuracy 'for free'; the area axis is really driven by data_width and the two guards. W starts at 11 so the search can see the round-mode borderline around LSB=2^-10 and runs to 20 to cover the high-accuracy end of the front toward the HV accuracy reference. angle_guard range lets Optuna trim angle-path/LUT width while frac_guard 0..3 covers the x/y truncation trade.
- `unrolled_k` (36 evals): data_width=11..20, n_iter=10..28, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round, k=2..6. *Why:* Same accuracy physics as iterative (identical bit-level path), but a different area/shift cost: k chained rotations with the FSM reuse may need fewer/cheaper shift stages than one barrel-shifted rotation, so this is where the real area trade-off may be won or lost. k is kept to 2..6 because the >=1 MSPS throughput constraint is already loose for these cycle counts; large k only burns area. Accuracy-carrying params (data_width, n_iter, guards, rounding) use the same ranges as iterative so the two families can be compared point-for-point on area at equal accuracy.

**Result (code):** 60 evaluations this round, 60 total; 39 feasible; hypervolume 7835 (n/a).

**LLM decision:** `stop` — Final round reached. The feasible front is well-populated (7 Pareto designs, 39/60 feasible) and spans the trade-off curve from luts_plus_ffs=326 (accuracy 11.5 bits) to 464 (17 bits), all comfortably meeting both constraints (throughput >= 1 MSPS, max_abs_err <= 2^-10). The selection rule (min luts_plus_ffs) is satisfied by the iterative [data_width=15 n_iter=24 angle_guard=3 frac_guard=1 rounding=round] design at 326 LUT+FF with 11.5 accuracy bits, well above the 10-bit requirement. No further improvement is expected within the remaining budget, so stopping is appropriate.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 7835 (gain this round: n/a (first round)).
Feasible designs: 39 of 60 evaluations (33 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 35% violate; best seen 7.75e-06 (2^-16.98)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=24 angle_guard=3 frac_guard=1 rounding=round] luts_plus_ffs=326, accuracy_bits=11.5, luts=229, ffs=97, throughput_msps=6, max_abs_err=0.000346 (2^-11.50), power_index=0.331
- iterative [data_width=20 n_iter=14 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=352, accuracy_bits=12.9, luts=231, ffs=121, throughput_msps=11.1, max_abs_err=0.000132 (2^-12.89), power_index=0.225
- iterative [data_width=19 n_iter=20 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=362, accuracy_bits=14.3, luts=246, ffs=116, throughput_msps=6.91, max_abs_err=4.83e-05 (2^-14.34), power_index=0.313
- iterative [data_width=19 n_iter=28 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=383, accuracy_bits=14.7, luts=265, ffs=118, throughput_msps=5.13, max_abs_err=3.83e-05 (2^-14.67), power_index=0.446
- iterative [data_width=20 n_iter=20 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=386, accuracy_bits=15.3, luts=264, ffs=122, throughput_msps=6.78, max_abs_err=2.4e-05 (2^-15.35), power_index=0.334
- iterative [data_width=20 n_iter=28 angle_guard=3 frac_guard=1 rounding=round] luts_plus_ffs=447, accuracy_bits=16.3, luts=325, ffs=122, throughput_msps=5.03, max_abs_err=1.24e-05 (2^-16.30), power_index=0.522
- iterative [data_width=20 n_iter=24 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=464, accuracy_bits=17, luts=340, ffs=124, throughput_msps=5.78, max_abs_err=7.75e-06 (2^-16.98), power_index=0.471
Front coverage: luts_plus_ffs 326..464 (HV reference 1500); accuracy_bits 11.5..17 (HV reference 10); data_width on the front 15..20 (registry 8..28).

Per family:
- iterative: 24 evals, 18 feasible; max throughput seen 15.6 MSPS; best accuracy 16.98 bits; best feasible luts_plus_ffs=326; feasible ranges: data_width 15..20, n_iter 14..28, angle_guard -1..3, frac_guard 0..2
- unrolled_k: 36 evals, 21 feasible; max throughput seen 12 MSPS; best accuracy 15.96 bits; best feasible luts_plus_ffs=391; feasible ranges: data_width 14..20, n_iter 12..26, angle_guard 0..3, frac_guard 1..3, k 2..6
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (40 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (7 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 77 feasible; hypervolume 1.4e+04 (+78.7%).

**No LLM call** (code's front-mapping round): Final round reached. The feasible front is well-populated (7 Pareto designs, 39/60 feasible) and spans the trade-off curve from luts_plus_ffs=326 (accuracy 11.5 bits) to 464 (17 bits), all comfortably meeting both constraints (throughput >= 1 MSPS, max_abs_err <= 2^-10). The selection rule (min luts_plus_ffs) is satisfied by the iterative [data_width=15 n_iter=24 angle_guard=3 frac_guard=1 rounding=round] design at 326 LUT+FF with 11.5 accuracy bits, well above the 10-bit requirement. No further improvement is expected within the remaining budget, so stopping is appropriate.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.4e+04 (gain this round: +78.7%).
Feasible designs: 77 of 100 evaluations (67 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 23% violate; best seen 9.99e-08 (2^-23.26)

Pareto front (feasible, 15 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=20 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=289, accuracy_bits=11.4, luts=192, ffs=97, throughput_msps=7.04, max_abs_err=0.000373 (2^-11.39), power_index=0.25
- iterative [data_width=18 n_iter=26 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=322, accuracy_bits=12, luts=214, ffs=108, throughput_msps=5.48, max_abs_err=0.00025 (2^-11.97), power_index=0.351
- iterative [data_width=18 n_iter=20 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=325, accuracy_bits=12.4, luts=216, ffs=109, throughput_msps=6.91, max_abs_err=0.000179 (2^-12.45), power_index=0.281
- iterative [data_width=19 n_iter=20 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=362, accuracy_bits=14.3, luts=246, ffs=116, throughput_msps=6.91, max_abs_err=4.83e-05 (2^-14.34), power_index=0.313
- iterative [data_width=19 n_iter=28 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=383, accuracy_bits=14.7, luts=265, ffs=118, throughput_msps=5.13, max_abs_err=3.83e-05 (2^-14.67), power_index=0.446
- iterative [data_width=22 n_iter=26 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=409, accuracy_bits=16, luts=282, ffs=127, throughput_msps=5.48, max_abs_err=1.56e-05 (2^-15.97), power_index=0.446
- iterative [data_width=22 n_iter=25 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=418, accuracy_bits=16.2, luts=287, ffs=130, throughput_msps=5.57, max_abs_err=1.32e-05 (2^-16.21), power_index=0.44
- iterative [data_width=22 n_iter=26 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=433, accuracy_bits=17.5, luts=303, ffs=130, throughput_msps=5.38, max_abs_err=5.23e-06 (2^-17.54), power_index=0.472
- iterative [data_width=27 n_iter=28 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=527, accuracy_bits=20.4, luts=375, ffs=151, throughput_msps=4.94, max_abs_err=7.11e-07 (2^-20.42), power_index=0.614
- iterative [data_width=28 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=617, accuracy_bits=23.3, luts=451, ffs=165, throughput_msps=5.38, max_abs_err=9.99e-08 (2^-23.26), power_index=0.649
Front coverage: luts_plus_ffs 289..617 (HV reference 1500); accuracy_bits 11.4..23.3 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- iterative: 64 evals, 56 feasible; max throughput seen 15.6 MSPS; best accuracy 23.26 bits; best feasible luts_plus_ffs=289; feasible ranges: data_width 15..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 36 evals, 21 feasible; max throughput seen 12 MSPS; best accuracy 15.96 bits; best feasible luts_plus_ffs=391; feasible ranges: data_width 14..20, n_iter 12..26, angle_guard 0..3, frac_guard 1..3, k 2..6
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5028 in, 6761 out
- provider-reported cost: $0.0045
- full prompts and replies: `llm_trace.jsonl`

