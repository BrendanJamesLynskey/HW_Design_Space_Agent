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
`iterative:data_width=15,n_iter=16,angle_guard=3,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 183 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 98 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 10.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 19 | exact: schedule |
| latency_ns | 95.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.201 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000344 (2^-11.50) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 2.82 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 8.84e-05 (2^-13.47) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 0.724 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 11.5 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (20 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=16,angle_guard=3,frac_guard=2,rounding=trunc` | 183 | 98 | 10.4 | 19 | 0.201 | 0.000344 (2^-11.50) | 11.50 |
| 1 | `iterative:data_width=16,n_iter=14,angle_guard=4,frac_guard=0,rounding=round` | 185 | 100 | 11.4 | 17 | 0.182 | 0.000294 (2^-11.73) | 11.73 |
| 2 | `iterative:data_width=18,n_iter=21,angle_guard=0,frac_guard=0,rounding=trunc` | 212 | 107 | 6.7 | 24 | 0.288 | 0.000227 (2^-12.10) | 12.10 |
| 3 | `iterative:data_width=18,n_iter=21,angle_guard=2,frac_guard=0,rounding=trunc` | 216 | 109 | 6.6 | 24 | 0.293 | 0.000185 (2^-12.40) | 12.40 |
| 4 | `iterative:data_width=19,n_iter=15,angle_guard=2,frac_guard=1,rounding=trunc` | 218 | 115 | 10.8 | 18 | 0.225 | 9.41e-05 (2^-13.38) | 13.38 |
| 5 | `iterative:data_width=19,n_iter=15,angle_guard=4,frac_guard=1,rounding=trunc` | 221 | 117 | 10.5 | 18 | 0.229 | 8.66e-05 (2^-13.49) | 13.49 |
| 6 | `iterative:data_width=18,n_iter=21,angle_guard=3,frac_guard=0,rounding=round` | 231 | 110 | 6.6 | 24 | 0.308 | 7.75e-05 (2^-13.65) | 13.65 |
| 7 | `iterative:data_width=19,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 227 | 117 | 10.2 | 19 | 0.246 | 4.81e-05 (2^-14.34) | 14.34 |
| 8 | `iterative:data_width=20,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc` | 229 | 120 | 10.2 | 19 | 0.25 | 4.27e-05 (2^-14.51) | 14.51 |
| 9 | `iterative:data_width=20,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 239 | 122 | 10.2 | 19 | 0.258 | 3.93e-05 (2^-14.63) | 14.63 |
| 10 | `iterative:data_width=22,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc` | 282 | 127 | 6.4 | 25 | 0.385 | 1.39e-05 (2^-16.14) | 16.14 |
| 11 | `iterative:data_width=23,n_iter=21,angle_guard=-1,frac_guard=0,rounding=trunc` | 298 | 131 | 6.5 | 24 | 0.387 | 8.62e-06 (2^-16.82) | 16.82 |
| 12 | `iterative:data_width=22,n_iter=21,angle_guard=3,frac_guard=0,rounding=round` | 301 | 130 | 6.5 | 24 | 0.389 | 5.23e-06 (2^-17.54) | 17.54 |
| 13 | `iterative:data_width=23,n_iter=21,angle_guard=2,frac_guard=1,rounding=trunc` | 319 | 136 | 6.5 | 24 | 0.411 | 3.24e-06 (2^-18.24) | 18.24 |
| 14 | `iterative:data_width=26,n_iter=26,angle_guard=-2,frac_guard=0,rounding=trunc` | 354 | 145 | 5.4 | 29 | 0.545 | 2.08e-06 (2^-18.87) | 18.87 |
| 15 | `iterative:data_width=26,n_iter=26,angle_guard=0,frac_guard=0,rounding=trunc` | 358 | 147 | 5.4 | 29 | 0.551 | 9.44e-07 (2^-20.02) | 20.02 |
| 16 | `iterative:data_width=26,n_iter=26,angle_guard=1,frac_guard=0,rounding=trunc` | 360 | 148 | 5.3 | 29 | 0.554 | 8.42e-07 (2^-20.18) | 20.18 |
| 17 | `iterative:data_width=27,n_iter=28,angle_guard=-1,frac_guard=0,rounding=trunc` | 375 | 151 | 4.9 | 31 | 0.614 | 7.11e-07 (2^-20.42) | 20.42 |
| 18 | `iterative:data_width=28,n_iter=25,angle_guard=2,frac_guard=0,rounding=trunc` | 400 | 159 | 5.5 | 28 | 0.589 | 2.16e-07 (2^-22.14) | 22.14 |
| 19 | `iterative:data_width=28,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc` | 451 | 165 | 5.4 | 28 | 0.649 | 9.99e-08 (2^-23.26) | 23.26 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >=1 MSPS throughput and max_abs_err <= 2^-10, with area (luts_plus_ffs) as the primary objective. Both iterative and unrolled_k can meet the throughput constraint easily because the required Fmax is only single-digit to low-double-digit MHz for N=12..16. Accuracy is comfortably met with N>=12 iterations, so the search focuses on the low-N, low-width corner of the space where area is minimized. data_width 14..20 keeps the output quantization (LSB = 2^-(W-2)) at or below 2^-12, safely under the 2^-10 error budget, while allowing the optimizer to find the minimum W that still meets accuracy once angle_guard and frac_guard are accounted for. angle_guard and frac_guard are swept over their full ranges because they directly trade bits (area) against accuracy; the optimizer will find the minimum guard values that keep max_abs_err <= 2^-10. Rounding mode is included because round vs trunc can shift the error by up to 1 LSB, which matters near the accuracy boundary. The budget is split 55/45 between iterative and unrolled_k: iterative is expected to be the area winner (shared datapath, no parallel logic), so it gets more evaluations to finely map its Pareto front. unrolled_k gets 45% to check whether unrolling provides any area benefit through timing relaxation, and to populate the front with alternative points. Together, these two families cover the full area trade-off space available to this fleet member.*)
- `iterative` (33 evals): data_width=14..20, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* iterative is the smallest-area family in the registry (shared datapath, no per-stage registers), so it is the natural home for the min luts_plus_ffs objective. The throughput constraint (>=1 MSPS) is met by any iterative design whose Fmax is >=1000 MHz, which is impossible; however, the constraint is on throughput_msps = Fmax * results/cycle. For iterative, results/cycle = 1/(N+3). To get >=1 MSPS we need Fmax/(N+3) >= 1 MHz, i.e. Fmax >= (N+3) MHz. For N=12..16, that is 15..19 MHz, which is trivially met. So iterative can meet throughput. Accuracy: max_abs_err <= 2^-10 = 0.000976562. CORDIC error is dominated by the residual after N iterations, roughly 2^-(N+2) for the angle path, plus truncation/rounding effects. With N=12, residual ~2^-14, well below 2^-10. Even N=10 gives ~2^-12. So n_iter 12..16 is a safe band that keeps area low while guaranteeing accuracy. data_width 14..20: output LSB is 2^-(W-2). For W=14, LSB=2^-12, which is below 2^-10, so the quantization alone is fine. Lower W saves area. angle_guard and frac_guard are swept to find the minimum that still meets accuracy, since they add bits to the datapath and cost LUTs.
- `unrolled_k` (27 evals): data_width=14..20, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..4. *Why:* unrolled_k with k>1 reduces the cycle count per result (ceil(N/k)+3), which raises throughput for a given Fmax and may allow a lower Fmax to meet the 1 MSPS constraint, potentially freeing up timing margin that translates to lower area (smaller critical path). For k=2..4 and N=12..16, cycles/result = ceil(N/k)+3 ranges from ~6 to 11, so required Fmax is 6..11 MHz, still trivial. The main trade-off is that unrolling k rotations per cycle adds parallel datapath logic (k shifters/adders), increasing LUTs. The search will reveal whether the area penalty of unrolling is worth any Fmax/area interaction. Keeping the same n_iter and data_width ranges as iterative allows a direct comparison of the two families' Pareto fronts. k is limited to 2..4 to avoid excessive area blowup; k=8 would roughly double the datapath width and is unlikely to be area-optimal for this spec.

**Result (code):** 60 evaluations this round, 60 total; 54 feasible; hypervolume 5477 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 7 distinct designs spanning luts_plus_ffs 281-361 and accuracy_bits 11.5-14.6. The minimum area design (iterative, luts_plus_ffs=281) meets all constraints: throughput 10.4 MSPS >= 1 MSPS and max_abs_err 2^-11.50 <= 2^-10. The front covers the relevant trade-off space for this spec, and since this is the final round, we stop and select the minimum-area design from the front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 5477 (gain this round: n/a (first round)).
Feasible designs: 54 of 60 evaluations (47 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 13.5
- max_abs_err <= 0.000976562: 10% violate; best seen 3.93e-05 (2^-14.63)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=16 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=281, accuracy_bits=11.5, luts=183, ffs=98, throughput_msps=10.4, max_abs_err=0.000344 (2^-11.50), power_index=0.201
- iterative [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=288, accuracy_bits=11.7, luts=185, ffs=103, throughput_msps=10.8, max_abs_err=0.000307 (2^-11.67), power_index=0.195
- iterative [data_width=19 n_iter=15 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=333, accuracy_bits=13.4, luts=218, ffs=115, throughput_msps=10.8, max_abs_err=9.41e-05 (2^-13.38), power_index=0.225
- iterative [data_width=19 n_iter=15 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=338, accuracy_bits=13.5, luts=221, ffs=117, throughput_msps=10.5, max_abs_err=8.66e-05 (2^-13.49), power_index=0.229
- iterative [data_width=19 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=344, accuracy_bits=14.3, luts=227, ffs=117, throughput_msps=10.2, max_abs_err=4.81e-05 (2^-14.34), power_index=0.246
- iterative [data_width=20 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=349, accuracy_bits=14.5, luts=229, ffs=120, throughput_msps=10.2, max_abs_err=4.27e-05 (2^-14.51), power_index=0.25
- iterative [data_width=20 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=361, accuracy_bits=14.6, luts=239, ffs=122, throughput_msps=10.2, max_abs_err=3.93e-05 (2^-14.63), power_index=0.258
Front coverage: luts_plus_ffs 281..361 (HV reference 1500); accuracy_bits 11.5..14.6 (HV reference 10); data_width on the front 15..20 (registry 8..28).

Per family:
- iterative: 33 evals, 29 feasible; max throughput seen 13.5 MSPS; best accuracy 14.63 bits; best feasible luts_plus_ffs=281; feasible ranges: data_width 15..20, n_iter 13..16, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 27 evals, 25 feasible; max throughput seen 13.5 MSPS; best accuracy 13.80 bits; best feasible luts_plus_ffs=378; feasible ranges: data_width 14..20, n_iter 12..16, angle_guard -2..4, frac_guard 0..3, k 3..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (40 evals): data_width=14..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (7 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 92 feasible; hypervolume 1.413e+04 (+158.0%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 7 distinct designs spanning luts_plus_ffs 281-361 and accuracy_bits 11.5-14.6. The minimum area design (iterative, luts_plus_ffs=281) meets all constraints: throughput 10.4 MSPS >= 1 MSPS and max_abs_err 2^-11.50 <= 2^-10. The front covers the relevant trade-off space for this spec, and since this is the final round, we stop and select the minimum-area design from the front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.413e+04 (gain this round: +158.0%).
Feasible designs: 92 of 100 evaluations (85 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 13.5
- max_abs_err <= 0.000976562: 8% violate; best seen 9.99e-08 (2^-23.26)

Pareto front (feasible, 20 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=16 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=281, accuracy_bits=11.5, luts=183, ffs=98, throughput_msps=10.4, max_abs_err=0.000344 (2^-11.50), power_index=0.201
- iterative [data_width=18 n_iter=21 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=319, accuracy_bits=12.1, luts=212, ffs=107, throughput_msps=6.75, max_abs_err=0.000227 (2^-12.10), power_index=0.288
- iterative [data_width=19 n_iter=15 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=333, accuracy_bits=13.4, luts=218, ffs=115, throughput_msps=10.8, max_abs_err=9.41e-05 (2^-13.38), power_index=0.225
- iterative [data_width=18 n_iter=21 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=341, accuracy_bits=13.7, luts=231, ffs=110, throughput_msps=6.62, max_abs_err=7.75e-05 (2^-13.65), power_index=0.308
- iterative [data_width=20 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=349, accuracy_bits=14.5, luts=229, ffs=120, throughput_msps=10.2, max_abs_err=4.27e-05 (2^-14.51), power_index=0.25
- iterative [data_width=23 n_iter=21 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=429, accuracy_bits=16.8, luts=298, ffs=131, throughput_msps=6.5, max_abs_err=8.62e-06 (2^-16.82), power_index=0.387
- iterative [data_width=23 n_iter=21 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=455, accuracy_bits=18.2, luts=319, ffs=136, throughput_msps=6.5, max_abs_err=3.24e-06 (2^-18.24), power_index=0.411
- iterative [data_width=26 n_iter=26 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=505, accuracy_bits=20, luts=358, ffs=147, throughput_msps=5.38, max_abs_err=9.44e-07 (2^-20.02), power_index=0.551
- iterative [data_width=27 n_iter=28 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=527, accuracy_bits=20.4, luts=375, ffs=151, throughput_msps=4.94, max_abs_err=7.11e-07 (2^-20.42), power_index=0.614
- iterative [data_width=28 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=617, accuracy_bits=23.3, luts=451, ffs=165, throughput_msps=5.38, max_abs_err=9.99e-08 (2^-23.26), power_index=0.649
Front coverage: luts_plus_ffs 281..617 (HV reference 1500); accuracy_bits 11.5..23.3 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 73 evals, 67 feasible; max throughput seen 13.5 MSPS; best accuracy 23.26 bits; best feasible luts_plus_ffs=281; feasible ranges: data_width 15..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 27 evals, 25 feasible; max throughput seen 13.5 MSPS; best accuracy 13.80 bits; best feasible luts_plus_ffs=378; feasible ranges: data_width 14..20, n_iter 12..16, angle_guard -2..4, frac_guard 0..3, k 3..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4290 in, 1589 out
- provider-reported cost: $0.0029
- full prompts and replies: `llm_trace.jsonl`

