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
`unrolled_k:data_width=15,n_iter=14,angle_guard=4,frac_guard=2,rounding=round,k=2` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 317 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 98 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 103 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 10.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 10 | exact: schedule |
| latency_ns | 97.2 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.156 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000249 (2^-11.97) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 2.04 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 7.15e-05 (2^-13.77) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 0.586 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 12 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (15 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `unrolled_k:data_width=15,n_iter=14,angle_guard=4,frac_guard=2,rounding=round,k=2` | 317 | 98 | 10.3 | 10 | 0.156 | 0.000249 (2^-11.97) | 11.97 |
| 1 | `unrolled_k:data_width=15,n_iter=17,angle_guard=3,frac_guard=2,rounding=round,k=2` | 322 | 98 | 8.8 | 12 | 0.19 | 0.000192 (2^-12.35) | 12.35 |
| 2 | `unrolled_k:data_width=17,n_iter=17,angle_guard=3,frac_guard=2,rounding=round,k=2` | 363 | 108 | 8.6 | 12 | 0.213 | 5.72e-05 (2^-14.09) | 14.09 |
| 3 | `unrolled_k:data_width=17,n_iter=17,angle_guard=3,frac_guard=3,rounding=round,k=2` | 378 | 110 | 8.6 | 12 | 0.22 | 5.1e-05 (2^-14.26) | 14.26 |
| 4 | `unrolled_k:data_width=17,n_iter=17,angle_guard=3,frac_guard=4,rounding=round,k=2` | 393 | 112 | 8.6 | 12 | 0.228 | 4.74e-05 (2^-14.36) | 14.36 |
| 5 | `unrolled_k:data_width=18,n_iter=21,angle_guard=4,frac_guard=2,rounding=round,k=2` | 398 | 114 | 7.3 | 14 | 0.269 | 2.87e-05 (2^-15.09) | 15.09 |
| 6 | `unrolled_k:data_width=18,n_iter=23,angle_guard=3,frac_guard=4,rounding=round,k=2` | 427 | 117 | 6.9 | 15 | 0.307 | 2.02e-05 (2^-15.60) | 15.60 |
| 7 | `unrolled_k:data_width=18,n_iter=21,angle_guard=3,frac_guard=4,rounding=round,k=2` | 427 | 117 | 7.3 | 14 | 0.286 | 2.02e-05 (2^-15.60) | 15.60 |
| 8 | `unrolled_k:data_width=19,n_iter=23,angle_guard=3,frac_guard=3,rounding=round,k=2` | 432 | 120 | 6.9 | 15 | 0.312 | 1.17e-05 (2^-16.38) | 16.38 |
| 9 | `unrolled_k:data_width=20,n_iter=21,angle_guard=3,frac_guard=2,rounding=round,k=2` | 438 | 123 | 7.2 | 14 | 0.296 | 7.75e-06 (2^-16.98) | 16.98 |
| 10 | `unrolled_k:data_width=20,n_iter=23,angle_guard=3,frac_guard=2,rounding=round,k=2` | 438 | 123 | 6.7 | 15 | 0.317 | 7.75e-06 (2^-16.98) | 16.98 |
| 11 | `unrolled_k:data_width=20,n_iter=21,angle_guard=4,frac_guard=2,rounding=round,k=2` | 442 | 124 | 7.2 | 14 | 0.298 | 7.14e-06 (2^-17.10) | 17.10 |
| 12 | `unrolled_k:data_width=20,n_iter=23,angle_guard=3,frac_guard=4,rounding=round,k=2` | 471 | 127 | 6.7 | 15 | 0.337 | 5.15e-06 (2^-17.57) | 17.57 |
| 13 | `unrolled_k:data_width=20,n_iter=24,angle_guard=3,frac_guard=4,rounding=round,k=2` | 471 | 127 | 6.7 | 15 | 0.337 | 5.15e-06 (2^-17.57) | 17.57 |
| 14 | `unrolled_k:data_width=20,n_iter=22,angle_guard=4,frac_guard=4,rounding=round,k=3` | 595 | 127 | 6.2 | 11 | 0.299 | 4.1e-06 (2^-17.89) | 17.89 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >= 1 MSPS throughput and max_abs_err <= 2^-10, with area (LUT+FF) as the primary objective. Only iterative and unrolled_k are available to me, and both are shared-datapath families that minimize area. The key tension is: accuracy (max_abs_err) depends on data_width, n_iter, angle_guard, frac_guard, and rounding, while throughput depends on Fmax and latency (N+3 for iterative, ceil(N/k)+3 for unrolled_k). I allocate 55% to iterative (the area-minimal baseline) and 45% to unrolled_k (which trades a small area increase for lower latency and thus higher throughput margin). Both families search data_width 8-12 and n_iter 8-14, which is the region where the 2^-10 error constraint is likely to be met with minimal area; wider widths or more iterations would increase area without being necessary if the constraint is already satisfied. angle_guard and frac_guard are kept small (0-2, -1 to 2) to avoid inflating the atan-LUT and datapath, which directly increases LUTs. Rounding is included as a choice since it affects both accuracy and area (rounding adds a small adder). This plan focuses the 100-eval budget on the feasible region where the error constraint is met, letting Optuna find the Pareto-optimal (area, accuracy) trade-off within each family, and the merged front will then be ranked by hypervolume against the reference point.*)
- `iterative` (33 evals): data_width=8..12, n_iter=8..14, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the smallest-area family (shared datapath, no pipeline registers). It is the only candidate that can plausibly hit the 1 MSPS throughput constraint with minimal LUT+FF, since its throughput is Fmax/latency and its latency (N+3) is short for small N. I focus data_width 8-12 and n_iter 8-14 because the error constraint (<= 2^-10) is tight for low width/iter; the search will find the minimal (W, N) pair that satisfies max_abs_err while keeping area low. angle_guard and frac_guard are kept narrow (small non-negative) to avoid inflating the atan-LUT and datapath width, which directly hurts the area objective.
- `unrolled_k` (27 evals): data_width=8..12, n_iter=8..14, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k reduces latency to ceil(N/k)+3 cycles, which raises throughput (Fmax * k/N) relative to iterative for the same N. This gives a second point on the Pareto front: slightly more area (k parallel shift/add stages) but higher throughput margin, which may allow a lower Fmax or a slightly smaller N to still meet 1 MSPS. I keep k in 2-4 to bound the area increase, and mirror the same data_width/n_iter/guard ranges as iterative so the accuracy-feasible region is covered consistently. This lets the merged front trade a little area for throughput headroom, which is valuable if iterative's Fmax is marginal.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `refine` — The current results show that the accuracy constraint (max_abs_err <= 2^-10) is the bottleneck, with 100% of evaluations violating it. The best accuracy achieved is 9.32 bits (unrolled_k), which is still short of the required 10 bits. The throughput constraint is easily met (best 16.9 MSPS vs 1 MSPS required). To improve accuracy, we need to increase the number of iterations (n_iter) and/or the data width (data_width), and potentially use rounding instead of truncation. The current ranges for n_iter (4..30) and data_width (8..28) are wide, but the search has not yet explored the higher end of these ranges where accuracy improves. We should narrow the search to focus on higher n_iter and data_width values, and ensure rounding is used. Additionally, we should explore the pipelined families, which may offer better throughput/area trade-offs for the required accuracy.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 16.9
- max_abs_err <= 0.000976562: 100% violate; best seen 0.00157 (2^-9.32)

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=12 n_iter=12 angle_guard=2 frac_guard=2 rounding=round k=2]: throughput=12, max_abs_err=0.00157 (2^-9.32); max_abs_err <= 0.000976562 violated by 60.4%
- unrolled_k [data_width=12 n_iter=14 angle_guard=2 frac_guard=2 rounding=round k=2]: throughput=10.8, max_abs_err=0.00167 (2^-9.22); max_abs_err <= 0.000976562 violated by 71.2%
- unrolled_k [data_width=12 n_iter=14 angle_guard=2 frac_guard=2 rounding=round k=3]: throughput=9.2, max_abs_err=0.00167 (2^-9.22); max_abs_err <= 0.000976562 violated by 71.2%
- iterative [data_width=12 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc]: throughput=12.7, max_abs_err=0.00255 (2^-8.62); max_abs_err <= 0.000976562 violated by 160.8%
- unrolled_k [data_width=12 n_iter=11 angle_guard=2 frac_guard=2 rounding=trunc k=2]: throughput=12, max_abs_err=0.00262 (2^-8.58); max_abs_err <= 0.000976562 violated by 168.1%

Per family:
- iterative: 33 evals, 0 feasible; max throughput seen 16.9 MSPS; best accuracy 8.62 bits
- unrolled_k: 27 evals, 0 feasible; max throughput seen 16.4 MSPS; best accuracy 9.32 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Narrow ranges to focus on higher accuracy configurations (data_width 14-20, n_iter 14-24) with rounding enabled. Add pipelined family to explore alternative architectures that may offer better area efficiency at the required accuracy level.*)
- `unrolled_k` (40 evals): data_width=14..20, n_iter=14..24, angle_guard=2..4, frac_guard=2..4, rounding=round, k=2..4. *Why:* Focus on higher data_width and n_iter to achieve 10-bit accuracy, with rounding enabled. Limit k to 2-4 to balance throughput and area.
- clamped by code: fleet member: dropped families outside its assignment ['pipelined'] (allowed: ['iterative', 'unrolled_k'])

**Result (code):** 40 evaluations this round, 100 total; 40 feasible; hypervolume 7910 (+inf).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 15 unique designs spanning luts_plus_ffs 415..722 and accuracy_bits 12..17.9. The minimum area design (unrolled_k, 415 LUTs+FFs) meets all constraints: throughput 10.3 MSPS >= 1 and max_abs_err 2^-11.97 <= 2^-10. The front covers the trade-off space adequately for the hypervolume objective, and the selection rule (min luts_plus_ffs) clearly points to the 415-unit design. No further exploration is possible due to round/budget cap.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 7910 (gain this round: +inf (first feasible designs)).
Feasible designs: 40 of 100 evaluations (37 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 16.9
- max_abs_err <= 0.000976562: 60% violate; best seen 4.1e-06 (2^-17.89)

Pareto front (feasible, 15 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=15 n_iter=14 angle_guard=4 frac_guard=2 rounding=round k=2] luts_plus_ffs=415, accuracy_bits=12, luts=317, ffs=98, throughput_msps=10.3, max_abs_err=0.000249 (2^-11.97), power_index=0.156
- unrolled_k [data_width=17 n_iter=17 angle_guard=3 frac_guard=2 rounding=round k=2] luts_plus_ffs=471, accuracy_bits=14.1, luts=363, ffs=108, throughput_msps=8.57, max_abs_err=5.72e-05 (2^-14.09), power_index=0.213
- unrolled_k [data_width=17 n_iter=17 angle_guard=3 frac_guard=3 rounding=round k=2] luts_plus_ffs=488, accuracy_bits=14.3, luts=378, ffs=110, throughput_msps=8.57, max_abs_err=5.1e-05 (2^-14.26), power_index=0.22
- unrolled_k [data_width=18 n_iter=21 angle_guard=4 frac_guard=2 rounding=round k=2] luts_plus_ffs=512, accuracy_bits=15.1, luts=398, ffs=114, throughput_msps=7.35, max_abs_err=2.87e-05 (2^-15.09), power_index=0.269
- unrolled_k [data_width=18 n_iter=23 angle_guard=3 frac_guard=4 rounding=round k=2] luts_plus_ffs=544, accuracy_bits=15.6, luts=427, ffs=117, throughput_msps=6.86, max_abs_err=2.02e-05 (2^-15.60), power_index=0.307
- unrolled_k [data_width=19 n_iter=23 angle_guard=3 frac_guard=3 rounding=round k=2] luts_plus_ffs=552, accuracy_bits=16.4, luts=432, ffs=120, throughput_msps=6.86, max_abs_err=1.17e-05 (2^-16.38), power_index=0.312
- unrolled_k [data_width=20 n_iter=21 angle_guard=3 frac_guard=2 rounding=round k=2] luts_plus_ffs=561, accuracy_bits=17, luts=438, ffs=123, throughput_msps=7.17, max_abs_err=7.75e-06 (2^-16.98), power_index=0.296
- unrolled_k [data_width=20 n_iter=21 angle_guard=4 frac_guard=2 rounding=round k=2] luts_plus_ffs=566, accuracy_bits=17.1, luts=442, ffs=124, throughput_msps=7.17, max_abs_err=7.14e-06 (2^-17.10), power_index=0.298
- unrolled_k [data_width=20 n_iter=23 angle_guard=3 frac_guard=4 rounding=round k=2] luts_plus_ffs=598, accuracy_bits=17.6, luts=471, ffs=127, throughput_msps=6.69, max_abs_err=5.15e-06 (2^-17.57), power_index=0.337
- unrolled_k [data_width=20 n_iter=22 angle_guard=4 frac_guard=4 rounding=round k=3] luts_plus_ffs=722, accuracy_bits=17.9, luts=595, ffs=127, throughput_msps=6.21, max_abs_err=4.1e-06 (2^-17.89), power_index=0.299
Front coverage: luts_plus_ffs 415..722 (HV reference 1500); accuracy_bits 12..17.9 (HV reference 10); data_width on the front 15..20 (registry 8..28).

Per family:
- iterative: 33 evals, 0 feasible; max throughput seen 16.9 MSPS; best accuracy 8.62 bits
- unrolled_k: 67 evals, 40 feasible; max throughput seen 16.4 MSPS; best accuracy 17.89 bits; best feasible luts_plus_ffs=415; feasible ranges: data_width 14..20, n_iter 14..24, angle_guard 2..4, frac_guard 2..4, k 2..4
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 6801 in, 2306 out
- provider-reported cost: $0.0041
- full prompts and replies: `llm_trace.jsonl`

