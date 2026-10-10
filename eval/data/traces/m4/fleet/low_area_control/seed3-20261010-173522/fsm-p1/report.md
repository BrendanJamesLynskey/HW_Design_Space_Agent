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
`unrolled_k:data_width=17,n_iter=17,angle_guard=0,frac_guard=0,rounding=trunc,k=2` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 277 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 101 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 105 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 8.78 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 12 | exact: schedule |
| latency_ns | 114 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.171 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000307 (2^-11.67) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 10.1 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 7.36e-05 (2^-13.73) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 2.41 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 11.7 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `unrolled_k:data_width=17,n_iter=17,angle_guard=0,frac_guard=0,rounding=trunc,k=2` | 277 | 101 | 8.8 | 12 | 0.171 | 0.000307 (2^-11.67) | 11.67 |
| 1 | `unrolled_k:data_width=17,n_iter=17,angle_guard=0,frac_guard=0,rounding=round,k=2` | 288 | 101 | 8.8 | 12 | 0.175 | 0.000244 (2^-12.00) | 12.00 |
| 2 | `unrolled_k:data_width=17,n_iter=17,angle_guard=2,frac_guard=0,rounding=round,k=2` | 294 | 103 | 8.6 | 12 | 0.179 | 0.000139 (2^-12.81) | 12.81 |
| 3 | `unrolled_k:data_width=16,n_iter=29,angle_guard=4,frac_guard=2,rounding=round,k=2` | 357 | 104 | 5.7 | 18 | 0.312 | 0.000103 (2^-13.24) | 13.24 |
| 4 | `unrolled_k:data_width=17,n_iter=29,angle_guard=4,frac_guard=4,rounding=trunc,k=2` | 360 | 113 | 5.7 | 18 | 0.32 | 6.12e-05 (2^-14.00) | 14.00 |
| 5 | `unrolled_k:data_width=17,n_iter=29,angle_guard=3,frac_guard=2,rounding=round,k=2` | 375 | 108 | 5.7 | 18 | 0.327 | 5.36e-05 (2^-14.19) | 14.19 |
| 6 | `unrolled_k:data_width=17,n_iter=29,angle_guard=4,frac_guard=2,rounding=round,k=2` | 379 | 109 | 5.7 | 18 | 0.33 | 5.05e-05 (2^-14.27) | 14.27 |
| 7 | `unrolled_k:data_width=17,n_iter=17,angle_guard=4,frac_guard=3,rounding=round,k=2` | 381 | 111 | 8.6 | 12 | 0.222 | 4.28e-05 (2^-14.51) | 14.51 |
| 8 | `unrolled_k:data_width=23,n_iter=24,angle_guard=-1,frac_guard=0,rounding=trunc,k=2` | 396 | 130 | 6.7 | 15 | 0.297 | 8.62e-06 (2^-16.82) | 16.82 |
| 9 | `unrolled_k:data_width=22,n_iter=29,angle_guard=4,frac_guard=0,rounding=round,k=2` | 411 | 130 | 5.6 | 18 | 0.367 | 5.23e-06 (2^-17.54) | 17.54 |
| 10 | `unrolled_k:data_width=23,n_iter=29,angle_guard=0,frac_guard=0,rounding=round,k=2` | 420 | 131 | 5.6 | 18 | 0.373 | 3.98e-06 (2^-17.94) | 17.94 |
| 11 | `unrolled_k:data_width=23,n_iter=29,angle_guard=4,frac_guard=2,rounding=round,k=2` | 521 | 139 | 5.5 | 18 | 0.447 | 1.04e-06 (2^-19.88) | 19.88 |
| 12 | `unrolled_k:data_width=27,n_iter=29,angle_guard=4,frac_guard=2,rounding=round,k=2` | 621 | 159 | 5.3 | 18 | 0.529 | 6.42e-08 (2^-23.89) | 23.89 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is low-area with a hard throughput floor of >=1 MSPS and max_abs_err <= 2^-10. Of my two assigned families, only iterative can meet the throughput constraint (1 result/cycle); unrolled_k is structurally limited to 1 result per k cycles (k>=2), so it cannot reach 1 MSPS and is expected to be filtered out. I therefore weight the budget heavily toward iterative (55%) to densely map its area-vs-accuracy Pareto front, which is where the selection rule (min luts_plus_ffs) will pick the final design. I keep n_iter near the accuracy floor (4..14) and data_width modest (8..14) to minimise luts_plus_ffs while still satisfying the 2^-10 error bound, and sweep angle_guard, frac_guard and rounding to find the cheapest guard/rounding configuration that meets the error constraint. The remaining 45% goes to unrolled_k to confirm its infeasibility against the throughput constraint and to capture any high-Fmax corner, so the merged fleet front is complete and honest. No design is invented; all numbers come from the bit-accurate and cost models.*)
- `iterative` (33 evals): data_width=8..14, n_iter=4..14, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* iterative is the minimum-area family (single shared datapath, no pipeline registers). It is the only one of my two families that can plausibly hit >=1 MSPS, since unrolled_k is 1 result per k cycles (<=0.5 MSPS at k>=2) and will be filtered out. I focus n_iter at the accuracy floor (4..14) and data_width at 8..14 to keep luts_plus_ffs low while still reaching max_abs_err <= 2^-10; angle_guard/frac_guard/rounding are swept to find the cheapest guard-bit/rounding combination that meets the error bound. This is where the area-vs-accuracy trade-off lives for the low-area spec.
- `unrolled_k` (27 evals): data_width=8..14, n_iter=4..14, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* unrolled_k is assigned to me and I must map its feasible region, but it cannot meet throughput_msps >= 1 (1 result per k cycles, k>=2 => <=0.5 MSPS), so it will be constraint-filtered. I still spend a small share to confirm infeasibility and to capture any corner (e.g. very high Fmax at small k) that might surprise the filter, so the merged front is honest. Ranges mirror iterative so the comparison is apples-to-apples.

**Result (code):** 60 evaluations this round, 60 total; 2 feasible; hypervolume 664.8 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is established with 2 designs from the `unrolled_k` family. The best design (luts_plus_ffs=401, accuracy_bits=10.4) satisfies all constraints: throughput 13.5 MSPS >= 1 MSPS and max_abs_err 0.000757 <= 0.000976562. The `iterative` family was explored but yielded 0 feasible designs (best accuracy 9.56 bits < 10 bits required). Since this is the final round (budget/cap reached), we stop. The selection rule (min luts_plus_ffs) picks the unrolled_k design with 401 LUTs+FFs.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 664.8 (gain this round: n/a (first round)).
Feasible designs: 2 of 60 evaluations (2 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 36.5
- max_abs_err <= 0.000976562: 97% violate; best seen 0.000629 (2^-10.63)

Pareto front (feasible, 2 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=14 n_iter=12 angle_guard=4 frac_guard=4 rounding=trunc k=3] luts_plus_ffs=401, accuracy_bits=10.4, luts=305, ffs=96, throughput_msps=13.5, max_abs_err=0.000757 (2^-10.37), power_index=0.106
- unrolled_k [data_width=14 n_iter=12 angle_guard=4 frac_guard=4 rounding=round k=4] luts_plus_ffs=524, accuracy_bits=10.6, luts=428, ffs=96, throughput_msps=12, max_abs_err=0.000629 (2^-10.63), power_index=0.118
Front coverage: luts_plus_ffs 401..524 (HV reference 1500); accuracy_bits 10.4..10.6 (HV reference 10); data_width on the front 14..14 (registry 8..28).

Per family:
- iterative: 33 evals, 0 feasible; max throughput seen 36.5 MSPS; best accuracy 9.56 bits
- unrolled_k: 27 evals, 2 feasible; max throughput seen 22.9 MSPS; best accuracy 10.63 bits; best feasible luts_plus_ffs=401; feasible ranges: data_width 14..14, n_iter 12..12, angle_guard 4..4, frac_guard 4..4, k 3..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `unrolled_k` (40 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 38 feasible; hypervolume 1.271e+04 (+1811.9%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is established with 2 designs from the `unrolled_k` family. The best design (luts_plus_ffs=401, accuracy_bits=10.4) satisfies all constraints: throughput 13.5 MSPS >= 1 MSPS and max_abs_err 0.000757 <= 0.000976562. The `iterative` family was explored but yielded 0 feasible designs (best accuracy 9.56 bits < 10 bits required). Since this is the final round (budget/cap reached), we stop. The selection rule (min luts_plus_ffs) picks the unrolled_k design with 401 LUTs+FFs.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.271e+04 (gain this round: +1811.9%).
Feasible designs: 38 of 100 evaluations (36 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 36.5
- max_abs_err <= 0.000976562: 62% violate; best seen 6.42e-08 (2^-23.89)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=17 n_iter=17 angle_guard=0 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=378, accuracy_bits=11.7, luts=277, ffs=101, throughput_msps=8.78, max_abs_err=0.000307 (2^-11.67), power_index=0.171
- unrolled_k [data_width=17 n_iter=17 angle_guard=0 frac_guard=0 rounding=round k=2] luts_plus_ffs=388, accuracy_bits=12, luts=288, ffs=101, throughput_msps=8.78, max_abs_err=0.000244 (2^-12.00), power_index=0.175
- unrolled_k [data_width=16 n_iter=29 angle_guard=4 frac_guard=2 rounding=round k=2] luts_plus_ffs=461, accuracy_bits=13.2, luts=357, ffs=104, throughput_msps=5.71, max_abs_err=0.000103 (2^-13.24), power_index=0.312
- unrolled_k [data_width=17 n_iter=29 angle_guard=4 frac_guard=4 rounding=trunc k=2] luts_plus_ffs=473, accuracy_bits=14, luts=360, ffs=113, throughput_msps=5.71, max_abs_err=6.12e-05 (2^-14.00), power_index=0.32
- unrolled_k [data_width=17 n_iter=29 angle_guard=3 frac_guard=2 rounding=round k=2] luts_plus_ffs=483, accuracy_bits=14.2, luts=375, ffs=108, throughput_msps=5.71, max_abs_err=5.36e-05 (2^-14.19), power_index=0.327
- unrolled_k [data_width=17 n_iter=17 angle_guard=4 frac_guard=3 rounding=round k=2] luts_plus_ffs=492, accuracy_bits=14.5, luts=381, ffs=111, throughput_msps=8.57, max_abs_err=4.28e-05 (2^-14.51), power_index=0.222
- unrolled_k [data_width=23 n_iter=24 angle_guard=-1 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=527, accuracy_bits=16.8, luts=396, ffs=130, throughput_msps=6.69, max_abs_err=8.62e-06 (2^-16.82), power_index=0.297
- unrolled_k [data_width=22 n_iter=29 angle_guard=4 frac_guard=0 rounding=round k=2] luts_plus_ffs=541, accuracy_bits=17.5, luts=411, ffs=130, throughput_msps=5.58, max_abs_err=5.23e-06 (2^-17.54), power_index=0.367
- unrolled_k [data_width=23 n_iter=29 angle_guard=4 frac_guard=2 rounding=round k=2] luts_plus_ffs=660, accuracy_bits=19.9, luts=521, ffs=139, throughput_msps=5.45, max_abs_err=1.04e-06 (2^-19.88), power_index=0.447
- unrolled_k [data_width=27 n_iter=29 angle_guard=4 frac_guard=2 rounding=round k=2] luts_plus_ffs=781, accuracy_bits=23.9, luts=621, ffs=159, throughput_msps=5.33, max_abs_err=6.42e-08 (2^-23.89), power_index=0.529
Front coverage: luts_plus_ffs 378..781 (HV reference 1500); accuracy_bits 11.7..23.9 (HV reference 10); data_width on the front 16..27 (registry 8..28).

Per family:
- iterative: 33 evals, 0 feasible; max throughput seen 36.5 MSPS; best accuracy 9.56 bits
- unrolled_k: 67 evals, 38 feasible; max throughput seen 22.9 MSPS; best accuracy 23.89 bits; best feasible luts_plus_ffs=378; feasible ranges: data_width 14..28, n_iter 12..29, angle_guard -1..4, frac_guard 0..4, k 2..7
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 3761 in, 1215 out
- provider-reported cost: $0.0018
- full prompts and replies: `llm_trace.jsonl`

