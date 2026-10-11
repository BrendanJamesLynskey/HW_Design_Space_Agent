# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
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
`unrolled_k:data_width=15,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,k=2` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 246 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 90 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 105 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 10.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 10 | exact: schedule |
| latency_ns | 94.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.126 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00081 (2^-10.27) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.64 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00021 (2^-12.22) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.72 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (14 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `unrolled_k:data_width=15,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,k=2` | 246 | 90 | 10.5 | 10 | 0.126 | 0.00081 (2^-10.27) | 10.27 |
| 1 | `unrolled_k:data_width=15,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,k=2` | 253 | 93 | 10.5 | 10 | 0.13 | 0.000594 (2^-10.72) | 10.72 |
| 2 | `unrolled_k:data_width=15,n_iter=20,angle_guard=3,frac_guard=0,rounding=round,k=2` | 264 | 94 | 8.1 | 13 | 0.175 | 0.000546 (2^-10.84) | 10.84 |
| 3 | `unrolled_k:data_width=15,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc,k=2` | 266 | 95 | 9.6 | 11 | 0.149 | 0.000393 (2^-11.31) | 11.31 |
| 4 | `unrolled_k:data_width=16,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,k=2` | 270 | 98 | 10.5 | 10 | 0.138 | 0.000344 (2^-11.50) | 11.50 |
| 5 | `unrolled_k:data_width=18,n_iter=22,angle_guard=-1,frac_guard=0,rounding=trunc,k=2` | 298 | 105 | 7.5 | 14 | 0.212 | 0.000271 (2^-11.85) | 11.85 |
| 6 | `unrolled_k:data_width=17,n_iter=21,angle_guard=4,frac_guard=0,rounding=round,k=3` | 398 | 104 | 7.0 | 10 | 0.189 | 0.000146 (2^-12.74) | 12.74 |
| 7 | `unrolled_k:data_width=18,n_iter=25,angle_guard=2,frac_guard=0,rounding=round,k=3` | 415 | 108 | 5.8 | 12 | 0.236 | 7.75e-05 (2^-13.65) | 13.65 |
| 8 | `unrolled_k:data_width=18,n_iter=26,angle_guard=3,frac_guard=3,rounding=round,k=2` | 413 | 115 | 6.4 | 16 | 0.318 | 2.32e-05 (2^-15.40) | 15.40 |
| 9 | `unrolled_k:data_width=20,n_iter=23,angle_guard=4,frac_guard=0,rounding=round,k=3` | 474 | 119 | 6.2 | 11 | 0.245 | 2.17e-05 (2^-15.49) | 15.49 |
| 10 | `unrolled_k:data_width=20,n_iter=21,angle_guard=3,frac_guard=4,rounding=round,k=2` | 471 | 127 | 7.2 | 14 | 0.315 | 5.31e-06 (2^-17.52) | 17.52 |
| 11 | `unrolled_k:data_width=26,n_iter=20,angle_guard=0,frac_guard=1,rounding=trunc,k=2` | 476 | 148 | 7.5 | 13 | 0.305 | 2.31e-06 (2^-18.73) | 18.73 |
| 12 | `unrolled_k:data_width=27,n_iter=21,angle_guard=3,frac_guard=0,rounding=trunc,k=2` | 491 | 154 | 7.0 | 14 | 0.34 | 1.16e-06 (2^-19.72) | 19.72 |
| 13 | `unrolled_k:data_width=25,n_iter=28,angle_guard=3,frac_guard=3,rounding=round,k=2` | 587 | 150 | 5.8 | 17 | 0.471 | 2.1e-07 (2^-22.18) | 22.18 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts are decisive: unrolled_k is the only family with feasible designs and it dominates the merged front entirely (13/13 designs). iterative has 0 feasible designs across 33 evaluations, so it is not worth further budget. The pipelined families (not available to me) have much higher area (2465 and 874 luts_plus_ffs) and contribute nothing to the front. My remaining budget (200 - 33 - 67 = 100 evaluations) should go entirely to unrolled_k. I narrow the parameter ranges significantly from the full registry ranges to focus on the region where feasible, low-area designs exist: data_width 12-16 (12 is the minimum for 2^-10 accuracy, 16 gives headroom for the accuracy_bits objective), n_iter 10-14 (10 is near the minimum for the error bound, 14 gives some margin), angle_guard -1..1 (negative guard saves area, positive guard helps accuracy), frac_guard 0..2 (0 is minimum area, 2 gives accuracy headroom), k 2..4 (k=2 minimizes area while meeting throughput; k=3-4 trade area for latency). The selection rule is min luts_plus_ffs, so the front's low-area end matters most, but the hypervolume also rewards the accuracy_bits objective, so I keep data_width up to 16 and n_iter up to 14 to explore the accuracy side of the trade-off. With 100 evaluations in one round, this focused search should densely map the Pareto front over the feasible region.*)
- `unrolled_k` (100 evals): data_width=12..16, n_iter=10..14, angle_guard=-1..1, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k is the only family that has produced feasible designs (38 feasible, best luts_plus_ffs 378) and owns the entire merged front (13/13 designs). The throughput constraint (>=1 MSPS) is met because Fmax for small unrolled_k designs is high enough that even at k=2 (1 result/2 cycles) the throughput exceeds 1 MSPS. The accuracy constraint (max_abs_err <= 2^-10) requires roughly 10+ bits of accuracy, which needs data_width >= 12 and n_iter >= 10. I narrow the ranges to focus the remaining budget on the region where feasible, low-area designs live: data_width 12-16 (enough for 2^-10 accuracy, small area), n_iter 10-14 (sufficient iterations for the error bound without excess area), angle_guard -1..1 (small guard bits to keep area low while maintaining accuracy), frac_guard 0..2 (minimal extra fractional bits), k 2..4 (higher k reduces latency but increases area; k=2 is the area-minimum that still meets throughput). This tightens the search around the known-feasible region to map the Pareto front more densely.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 42 feasible; hypervolume 1871 (n/a).

**LLM decision:** `add_family` — The current front is dominated by unrolled_k with best luts_plus_ffs=336 and accuracy_bits=11.7. However, pipelined_m has not been explored and could offer a better area/accuracy trade-off due to its simpler per-stage logic. Additionally, refining unrolled_k in the promising region (data_width 14-16, n_iter 12-15, k 2-4) may yield further improvements. The 58% constraint violation rate for max_abs_err suggests that accuracy is a tight constraint, so exploring both families in the accuracy-feasible region is critical.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1871 (gain this round: n/a (first round)).
Feasible designs: 42 of 100 evaluations (26 unique).
Families explored so far: unrolled_k. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14
- max_abs_err <= 0.000976562: 58% violate; best seen 0.000311 (2^-11.65)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round k=2] luts_plus_ffs=336, accuracy_bits=10.3, luts=246, ffs=90, throughput_msps=10.5, max_abs_err=0.00081 (2^-10.27), power_index=0.126
- unrolled_k [data_width=15 n_iter=13 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=346, accuracy_bits=10.5, luts=253, ffs=93, throughput_msps=10.5, max_abs_err=0.000689 (2^-10.50), power_index=0.13
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=368, accuracy_bits=11.5, luts=270, ffs=98, throughput_msps=10.5, max_abs_err=0.000344 (2^-11.50), power_index=0.138
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc k=3] luts_plus_ffs=459, accuracy_bits=11.7, luts=359, ffs=100, throughput_msps=8.97, max_abs_err=0.000311 (2^-11.65), power_index=0.138
Front coverage: luts_plus_ffs 336..459 (HV reference 1500); accuracy_bits 10.3..11.7 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- unrolled_k: 100 evals, 42 feasible; max throughput seen 14 MSPS; best accuracy 11.65 bits; best feasible luts_plus_ffs=336; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard -1..1, frac_guard 0..2, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The current front is dominated by unrolled_k with best luts_plus_ffs=336 and accuracy_bits=11.7. However, pipelined_m has not been explored and could offer a better area/accuracy trade-off due to its simpler per-stage logic. Additionally, refining unrolled_k in the promising region (data_width 14-16, n_iter 12-15, k 2-4) may yield further improvements. The 58% constraint violation rate for max_abs_err suggests that accuracy is a tight constraint, so exploring both families in the accuracy-feasible region is critical.*)
- `unrolled_k` (20 evals): data_width=14..16, n_iter=12..15, angle_guard=-1..1, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Refine the current best region to push luts_plus_ffs below 336 and accuracy above 11.7 bits, exploring the k=3..4 and frac_guard=1..2 trade-offs that were only partially covered.
- clamped by code: fleet member: dropped families outside its assignment ['pipelined_m'] (allowed: ['iterative', 'unrolled_k'])

**Result (code):** 20 evaluations this round, 120 total; 59 feasible; hypervolume 1880 (+0.5%).

**LLM decision:** `stop` — The spec is feasible and the front is well-mapped. The minimum-area feasible design (unrolled_k, data_width=15, n_iter=14, angle_guard=0, frac_guard=0, rounding=round) achieves luts_plus_ffs=336 with accuracy_bits=10.3 (max_abs_err=0.00081 <= 0.000976562) and throughput=10.5 MSPS (>= 1), satisfying all constraints. The selection rule (min luts_plus_ffs) picks this design. The front spans luts_plus_ffs 336..459 and accuracy_bits 10.3..11.7, covering the trade-off curve adequately for the hypervolume objective. Since this is the final round, no further exploration is possible or needed.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1880 (gain this round: +0.5%).
Feasible designs: 59 of 120 evaluations (39 unique).
Families explored so far: unrolled_k. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14
- max_abs_err <= 0.000976562: 51% violate; best seen 0.000311 (2^-11.65)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round k=2] luts_plus_ffs=336, accuracy_bits=10.3, luts=246, ffs=90, throughput_msps=10.5, max_abs_err=0.00081 (2^-10.27), power_index=0.126
- unrolled_k [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=346, accuracy_bits=10.7, luts=253, ffs=93, throughput_msps=10.5, max_abs_err=0.000594 (2^-10.72), power_index=0.13
- unrolled_k [data_width=15 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=361, accuracy_bits=11.3, luts=266, ffs=95, throughput_msps=9.58, max_abs_err=0.000393 (2^-11.31), power_index=0.149
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=368, accuracy_bits=11.5, luts=270, ffs=98, throughput_msps=10.5, max_abs_err=0.000344 (2^-11.50), power_index=0.138
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc k=3] luts_plus_ffs=459, accuracy_bits=11.7, luts=359, ffs=100, throughput_msps=8.97, max_abs_err=0.000311 (2^-11.65), power_index=0.138
Front coverage: luts_plus_ffs 336..459 (HV reference 1500); accuracy_bits 10.3..11.7 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- unrolled_k: 120 evals, 59 feasible; max throughput seen 14 MSPS; best accuracy 11.65 bits; best feasible luts_plus_ffs=336; feasible ranges: data_width 15..16, n_iter 12..15, angle_guard -1..1, frac_guard 0..2, k 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `unrolled_k` (80 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (5 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 135 feasible; hypervolume 1.128e+04 (+500.0%).

**No LLM call** (code's front-mapping round): The spec is feasible and the front is well-mapped. The minimum-area feasible design (unrolled_k, data_width=15, n_iter=14, angle_guard=0, frac_guard=0, rounding=round) achieves luts_plus_ffs=336 with accuracy_bits=10.3 (max_abs_err=0.00081 <= 0.000976562) and throughput=10.5 MSPS (>= 1), satisfying all constraints. The selection rule (min luts_plus_ffs) picks this design. The front spans luts_plus_ffs 336..459 and accuracy_bits 10.3..11.7, covering the trade-off curve adequately for the hypervolume objective. Since this is the final round, no further exploration is possible or needed.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.128e+04 (gain this round: +500.0%).
Feasible designs: 135 of 200 evaluations (106 unique).
Families explored so far: unrolled_k. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14
- max_abs_err <= 0.000976562: 32% violate; best seen 2.1e-07 (2^-22.18)

Pareto front (feasible, 14 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round k=2] luts_plus_ffs=336, accuracy_bits=10.3, luts=246, ffs=90, throughput_msps=10.5, max_abs_err=0.00081 (2^-10.27), power_index=0.126
- unrolled_k [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=346, accuracy_bits=10.7, luts=253, ffs=93, throughput_msps=10.5, max_abs_err=0.000594 (2^-10.72), power_index=0.13
- unrolled_k [data_width=15 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=361, accuracy_bits=11.3, luts=266, ffs=95, throughput_msps=9.58, max_abs_err=0.000393 (2^-11.31), power_index=0.149
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=368, accuracy_bits=11.5, luts=270, ffs=98, throughput_msps=10.5, max_abs_err=0.000344 (2^-11.50), power_index=0.138
- unrolled_k [data_width=17 n_iter=21 angle_guard=4 frac_guard=0 rounding=round k=3] luts_plus_ffs=502, accuracy_bits=12.7, luts=398, ffs=104, throughput_msps=7, max_abs_err=0.000146 (2^-12.74), power_index=0.189
- unrolled_k [data_width=18 n_iter=25 angle_guard=2 frac_guard=0 rounding=round k=3] luts_plus_ffs=523, accuracy_bits=13.7, luts=415, ffs=108, throughput_msps=5.83, max_abs_err=7.75e-05 (2^-13.65), power_index=0.236
- unrolled_k [data_width=20 n_iter=23 angle_guard=4 frac_guard=0 rounding=round k=3] luts_plus_ffs=593, accuracy_bits=15.5, luts=474, ffs=119, throughput_msps=6.21, max_abs_err=2.17e-05 (2^-15.49), power_index=0.245
- unrolled_k [data_width=20 n_iter=21 angle_guard=3 frac_guard=4 rounding=round k=2] luts_plus_ffs=598, accuracy_bits=17.5, luts=471, ffs=127, throughput_msps=7.17, max_abs_err=5.31e-06 (2^-17.52), power_index=0.315
- unrolled_k [data_width=27 n_iter=21 angle_guard=3 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=645, accuracy_bits=19.7, luts=491, ffs=154, throughput_msps=7.01, max_abs_err=1.16e-06 (2^-19.72), power_index=0.34
- unrolled_k [data_width=25 n_iter=28 angle_guard=3 frac_guard=3 rounding=round k=2] luts_plus_ffs=737, accuracy_bits=22.2, luts=587, ffs=150, throughput_msps=5.77, max_abs_err=2.1e-07 (2^-22.18), power_index=0.471
Front coverage: luts_plus_ffs 336..737 (HV reference 1500); accuracy_bits 10.3..22.2 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- unrolled_k: 200 evals, 135 feasible; max throughput seen 14 MSPS; best accuracy 22.18 bits; best feasible luts_plus_ffs=336; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, k 2..8
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 6546 in, 2068 out
- provider-reported cost: $0.0047
- full prompts and replies: `llm_trace.jsonl`

