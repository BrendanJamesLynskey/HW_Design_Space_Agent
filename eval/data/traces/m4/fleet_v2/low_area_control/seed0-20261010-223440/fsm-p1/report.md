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
`iterative:data_width=13,n_iter=14,angle_guard=2,frac_guard=2,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 193 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 87 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 11.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 85.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.179 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000856 (2^-10.19) | exact: bit-accurate model, exhaustive (8192 angles) |
| max_abs_err_lsb | 1.75 | exact: bit-accurate model, exhaustive (8192 angles) |
| rms_err | 0.000251 (2^-11.96) | exact: bit-accurate model, exhaustive (8192 angles) |
| rms_err_lsb | 0.513 | exact: bit-accurate model, exhaustive (8192 angles) |
| accuracy_bits | 10.2 | exact: bit-accurate model, exhaustive (8192 angles) |

## Pareto front (20 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=13,n_iter=14,angle_guard=2,frac_guard=2,rounding=round` | 193 | 87 | 11.7 | 17 | 0.179 | 0.000856 (2^-10.19) | 10.19 |
| 1 | `iterative:data_width=13,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 193 | 87 | 11.0 | 18 | 0.19 | 0.000856 (2^-10.19) | 10.19 |
| 2 | `iterative:data_width=14,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 197 | 90 | 10.4 | 19 | 0.205 | 0.000717 (2^-10.45) | 10.45 |
| 3 | `iterative:data_width=17,n_iter=26,angle_guard=-1,frac_guard=1,rounding=trunc` | 208 | 103 | 5.6 | 29 | 0.34 | 0.000497 (2^-10.98) | 10.98 |
| 4 | `iterative:data_width=15,n_iter=13,angle_guard=2,frac_guard=2,rounding=round` | 221 | 97 | 12.4 | 16 | 0.191 | 0.000431 (2^-11.18) | 11.18 |
| 5 | `iterative:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` | 225 | 100 | 11.7 | 17 | 0.207 | 0.000209 (2^-12.22) | 12.22 |
| 6 | `iterative:data_width=17,n_iter=26,angle_guard=1,frac_guard=2,rounding=trunc` | 228 | 107 | 5.5 | 29 | 0.365 | 0.000174 (2^-12.49) | 12.49 |
| 7 | `iterative:data_width=21,n_iter=15,angle_guard=-2,frac_guard=0,rounding=round` | 231 | 119 | 10.8 | 18 | 0.237 | 9.08e-05 (2^-13.43) | 13.43 |
| 8 | `iterative:data_width=21,n_iter=15,angle_guard=4,frac_guard=0,rounding=round` | 242 | 125 | 10.5 | 18 | 0.249 | 6.66e-05 (2^-13.87) | 13.87 |
| 9 | `iterative:data_width=25,n_iter=15,angle_guard=-2,frac_guard=0,rounding=trunc` | 269 | 139 | 10.5 | 18 | 0.277 | 6.21e-05 (2^-13.98) | 13.98 |
| 10 | `iterative:data_width=25,n_iter=15,angle_guard=1,frac_guard=3,rounding=trunc` | 304 | 148 | 10.3 | 18 | 0.306 | 6.11e-05 (2^-14.00) | 14.00 |
| 11 | `iterative:data_width=21,n_iter=21,angle_guard=-2,frac_guard=1,rounding=round` | 334 | 122 | 6.6 | 24 | 0.412 | 5.3e-05 (2^-14.20) | 14.20 |
| 12 | `iterative:data_width=21,n_iter=26,angle_guard=-1,frac_guard=1,rounding=round` | 338 | 123 | 5.5 | 29 | 0.503 | 2.8e-05 (2^-15.12) | 15.12 |
| 13 | `iterative:data_width=24,n_iter=21,angle_guard=-2,frac_guard=1,rounding=trunc` | 329 | 137 | 6.5 | 24 | 0.421 | 6.36e-06 (2^-17.26) | 17.26 |
| 14 | `iterative:data_width=25,n_iter=26,angle_guard=-2,frac_guard=0,rounding=trunc` | 335 | 140 | 5.4 | 29 | 0.519 | 3.6e-06 (2^-18.09) | 18.09 |
| 15 | `iterative:data_width=24,n_iter=26,angle_guard=1,frac_guard=1,rounding=trunc` | 339 | 140 | 5.4 | 29 | 0.523 | 1.78e-06 (2^-19.10) | 19.10 |
| 16 | `iterative:data_width=28,n_iter=21,angle_guard=-2,frac_guard=0,rounding=trunc` | 383 | 155 | 6.4 | 24 | 0.486 | 1.42e-06 (2^-19.42) | 19.42 |
| 17 | `iterative:data_width=25,n_iter=26,angle_guard=1,frac_guard=3,rounding=trunc` | 392 | 149 | 5.3 | 29 | 0.591 | 6.27e-07 (2^-20.60) | 20.60 |
| 18 | `iterative:data_width=28,n_iter=26,angle_guard=-2,frac_guard=1,rounding=trunc` | 410 | 157 | 5.3 | 29 | 0.618 | 5.65e-07 (2^-20.76) | 20.76 |
| 19 | `iterative:data_width=28,n_iter=26,angle_guard=0,frac_guard=2,rounding=round` | 504 | 161 | 5.3 | 29 | 0.726 | 1.6e-07 (2^-22.58) | 22.58 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *No fleet facts yet, so I open the front with the two families I own. The spec is area-dominated (min LUTs+FFs) with a hard throughput floor of 1 MSPS and a 2^-10 accuracy ceiling. iterative is the area champion but its Fmax is the risk; unrolled_k is the throughput/area lever. I focus both on the accuracy/area sweet spot (W 12-16, N 10-16, small guards, round) where the error constraint is satisfied with minimal area, and let Optuna map the trade-off curve. Splitting the budget evenly lets the merged front cover both the low-area corner and the throughput-driven region, maximizing hypervolume against the reference point.*)
- `iterative` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* iterative is the smallest-area family; the spec's throughput floor is 1 MSPS, so the Fmax constraint is the binding one. I search the accuracy/area sweet spot (W 12-16, N 10-16) where max_abs_err <= 2^-10 is met with minimal area, and round to reduce error. This family maps the low-area end of the front.
- `unrolled_k` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=round, k=2..4. *Why:* unrolled_k trades a few extra LUTs/FFs for higher Fmax and better throughput, which is the natural lever if iterative's Fmax falls short of 1 MSPS. I keep k modest (2-4) to stay area-efficient while covering the throughput/area trade-off that iterative cannot reach.

**Result (code):** 60 evaluations this round, 60 total; 26 feasible; hypervolume 2875 (n/a).

**LLM decision:** `stop` — The Pareto front is well-established and feasible. The minimum area design (iterative, luts_plus_ffs=280) meets the throughput constraint (11.7 MSPS >= 1) and the accuracy constraint (max_abs_err=0.000856 <= 0.000976562). The front covers a reasonable range of the trade-off space (area 280-519, accuracy 10.2-12.5 bits) with 6 distinct feasible designs. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (280) as per the selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 2875 (gain this round: n/a (first round)).
Feasible designs: 26 of 60 evaluations (20 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.3
- max_abs_err <= 0.000976562: 57% violate; best seen 0.000177 (2^-12.47)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=13 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=280, accuracy_bits=10.2, luts=193, ffs=87, throughput_msps=11.7, max_abs_err=0.000856 (2^-10.19), power_index=0.179
- iterative [data_width=13 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=280, accuracy_bits=10.2, luts=193, ffs=87, throughput_msps=11, max_abs_err=0.000856 (2^-10.19), power_index=0.19
- iterative [data_width=14 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=287, accuracy_bits=10.4, luts=197, ffs=90, throughput_msps=10.4, max_abs_err=0.000717 (2^-10.45), power_index=0.205
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=317, accuracy_bits=11.2, luts=221, ffs=97, throughput_msps=12.4, max_abs_err=0.000431 (2^-11.18), power_index=0.191
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=324, accuracy_bits=12.2, luts=225, ffs=100, throughput_msps=11.7, max_abs_err=0.000209 (2^-12.22), power_index=0.207
- unrolled_k [data_width=16 n_iter=16 angle_guard=2 frac_guard=1 rounding=round k=4] luts_plus_ffs=519, accuracy_bits=12.5, luts=422, ffs=98, throughput_msps=10.3, max_abs_err=0.000177 (2^-12.47), power_index=0.137
Front coverage: luts_plus_ffs 280..519 (HV reference 1500); accuracy_bits 10.2..12.5 (HV reference 10); data_width on the front 13..16 (registry 8..28).

Per family:
- iterative: 30 evals, 8 feasible; max throughput seen 15.3 MSPS; best accuracy 12.22 bits; best feasible luts_plus_ffs=280; feasible ranges: data_width 13..16, n_iter 13..16, angle_guard 0..2, frac_guard 1..2
- unrolled_k: 30 evals, 18 feasible; max throughput seen 13.5 MSPS; best accuracy 12.47 bits; best feasible luts_plus_ffs=408; feasible ranges: data_width 14..16, n_iter 12..16, angle_guard 0..2, frac_guard 1..2, k 3..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (34 evals): data_width=12..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (5 front designs; box front_anchored)
- `unrolled_k` (6 evals): data_width=15..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 56 feasible; hypervolume 1.303e+04 (+353.4%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and feasible. The minimum area design (iterative, luts_plus_ffs=280) meets the throughput constraint (11.7 MSPS >= 1) and the accuracy constraint (max_abs_err=0.000856 <= 0.000976562). The front covers a reasonable range of the trade-off space (area 280-519, accuracy 10.2-12.5 bits) with 6 distinct feasible designs. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (280) as per the selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.303e+04 (gain this round: +353.4%).
Feasible designs: 56 of 100 evaluations (50 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.3
- max_abs_err <= 0.000976562: 44% violate; best seen 1.6e-07 (2^-22.58)

Pareto front (feasible, 20 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=13 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=280, accuracy_bits=10.2, luts=193, ffs=87, throughput_msps=11.7, max_abs_err=0.000856 (2^-10.19), power_index=0.179
- iterative [data_width=14 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=287, accuracy_bits=10.4, luts=197, ffs=90, throughput_msps=10.4, max_abs_err=0.000717 (2^-10.45), power_index=0.205
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=317, accuracy_bits=11.2, luts=221, ffs=97, throughput_msps=12.4, max_abs_err=0.000431 (2^-11.18), power_index=0.191
- iterative [data_width=17 n_iter=26 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=335, accuracy_bits=12.5, luts=228, ffs=107, throughput_msps=5.48, max_abs_err=0.000174 (2^-12.49), power_index=0.365
- iterative [data_width=21 n_iter=15 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=367, accuracy_bits=13.9, luts=242, ffs=125, throughput_msps=10.5, max_abs_err=6.66e-05 (2^-13.87), power_index=0.249
- iterative [data_width=21 n_iter=21 angle_guard=-2 frac_guard=1 rounding=round] luts_plus_ffs=457, accuracy_bits=14.2, luts=334, ffs=122, throughput_msps=6.62, max_abs_err=5.3e-05 (2^-14.20), power_index=0.412
- iterative [data_width=24 n_iter=21 angle_guard=-2 frac_guard=1 rounding=trunc] luts_plus_ffs=466, accuracy_bits=17.3, luts=329, ffs=137, throughput_msps=6.5, max_abs_err=6.36e-06 (2^-17.26), power_index=0.421
- iterative [data_width=24 n_iter=26 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=479, accuracy_bits=19.1, luts=339, ffs=140, throughput_msps=5.38, max_abs_err=1.78e-06 (2^-19.10), power_index=0.523
- iterative [data_width=25 n_iter=26 angle_guard=1 frac_guard=3 rounding=trunc] luts_plus_ffs=542, accuracy_bits=20.6, luts=392, ffs=149, throughput_msps=5.28, max_abs_err=6.27e-07 (2^-20.60), power_index=0.591
- iterative [data_width=28 n_iter=26 angle_guard=0 frac_guard=2 rounding=round] luts_plus_ffs=666, accuracy_bits=22.6, luts=504, ffs=161, throughput_msps=5.28, max_abs_err=1.6e-07 (2^-22.58), power_index=0.726
Front coverage: luts_plus_ffs 280..666 (HV reference 1500); accuracy_bits 10.2..22.6 (HV reference 10); data_width on the front 13..28 (registry 8..28).

Per family:
- iterative: 64 evals, 32 feasible; max throughput seen 15.3 MSPS; best accuracy 22.58 bits; best feasible luts_plus_ffs=280; feasible ranges: data_width 13..28, n_iter 13..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 36 evals, 24 feasible; max throughput seen 13.5 MSPS; best accuracy 17.08 bits; best feasible luts_plus_ffs=408; feasible ranges: data_width 14..25, n_iter 12..26, angle_guard -1..3, frac_guard 1..4, k 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4659 in, 879 out
- provider-reported cost: $0.0023
- full prompts and replies: `llm_trace.jsonl`

