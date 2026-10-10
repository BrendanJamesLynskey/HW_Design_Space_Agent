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
`iterative:data_width=16,n_iter=15,angle_guard=1,frac_guard=0,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 172 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 97 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 11 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 90.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.182 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000643 (2^-10.60) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 10.5 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000126 (2^-12.96) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 2.06 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.6 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (17 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=16,n_iter=15,angle_guard=1,frac_guard=0,rounding=trunc` | 172 | 97 | 11.0 | 18 | 0.182 | 0.000643 (2^-10.60) | 10.60 |
| 1 | `iterative:data_width=16,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 179 | 97 | 11.0 | 18 | 0.187 | 0.000301 (2^-11.70) | 11.70 |
| 2 | `iterative:data_width=18,n_iter=16,angle_guard=-1,frac_guard=0,rounding=trunc` | 191 | 105 | 10.4 | 19 | 0.212 | 0.000207 (2^-12.24) | 12.24 |
| 3 | `iterative:data_width=17,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc` | 195 | 105 | 10.2 | 19 | 0.214 | 0.000174 (2^-12.49) | 12.49 |
| 4 | `iterative:data_width=17,n_iter=20,angle_guard=3,frac_guard=1,rounding=trunc` | 216 | 107 | 6.9 | 23 | 0.279 | 0.00017 (2^-12.52) | 12.52 |
| 5 | `iterative:data_width=18,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 214 | 111 | 10.2 | 19 | 0.232 | 8.08e-05 (2^-13.60) | 13.60 |
| 6 | `iterative:data_width=18,n_iter=16,angle_guard=3,frac_guard=2,rounding=trunc` | 218 | 113 | 10.2 | 19 | 0.236 | 6.86e-05 (2^-13.83) | 13.83 |
| 7 | `iterative:data_width=20,n_iter=16,angle_guard=3,frac_guard=0,rounding=trunc` | 221 | 119 | 10.0 | 19 | 0.243 | 5.76e-05 (2^-14.08) | 14.08 |
| 8 | `iterative:data_width=20,n_iter=20,angle_guard=3,frac_guard=0,rounding=trunc` | 249 | 120 | 6.8 | 23 | 0.32 | 4.23e-05 (2^-14.53) | 14.53 |
| 9 | `iterative:data_width=22,n_iter=18,angle_guard=3,frac_guard=0,rounding=round` | 293 | 130 | 7.4 | 21 | 0.335 | 1.1e-05 (2^-16.47) | 16.47 |
| 10 | `iterative:data_width=22,n_iter=25,angle_guard=0,frac_guard=0,rounding=round` | 297 | 127 | 5.7 | 28 | 0.447 | 8.91e-06 (2^-16.78) | 16.78 |
| 11 | `iterative:data_width=22,n_iter=27,angle_guard=2,frac_guard=0,rounding=round` | 301 | 129 | 5.2 | 30 | 0.485 | 5.49e-06 (2^-17.47) | 17.47 |
| 12 | `iterative:data_width=23,n_iter=25,angle_guard=0,frac_guard=0,rounding=round` | 316 | 132 | 5.6 | 28 | 0.472 | 3.98e-06 (2^-17.94) | 17.94 |
| 13 | `iterative:data_width=25,n_iter=22,angle_guard=1,frac_guard=0,rounding=round` | 350 | 143 | 6.2 | 25 | 0.464 | 1.41e-06 (2^-19.44) | 19.44 |
| 14 | `iterative:data_width=27,n_iter=23,angle_guard=0,frac_guard=0,rounding=round` | 383 | 152 | 5.9 | 26 | 0.524 | 4.81e-07 (2^-20.99) | 20.99 |
| 15 | `iterative:data_width=27,n_iter=25,angle_guard=0,frac_guard=0,rounding=round` | 392 | 152 | 5.5 | 28 | 0.573 | 3.32e-07 (2^-21.52) | 21.52 |
| 16 | `iterative:data_width=27,n_iter=25,angle_guard=4,frac_guard=0,rounding=round` | 399 | 156 | 5.4 | 28 | 0.585 | 2.15e-07 (2^-22.15) | 22.15 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Only iterative and unrolled_k are permitted to this architect, and for this spec they are also the right place to look: throughput >= 1 MSPS is a very weak constraint for single-result-per-many-cycles machines at these Fmax values, so it is a feasibility check rather than a design driver. That leaves min luts_plus_ffs against max accuracy_bits, which is precisely the area/accuracy front these two low-area families define. Accuracy needs roughly W >= 11-12 and N >= 10-12 to reach max_abs_err <= 2^-10, so the ranges are centred on and just below that feasibility boundary (to map the constraint edge) and extended upward to W=20 / N=22 so the front reaches toward the HV reference area of 1500 and accuracy_bits comfortably above the 10-bit reference. Guard bits (angle_guard, frac_guard) and rounding are included at small ranges because they are the cheap knobs that move a point across the accuracy constraint without adding a data-width step. Round 1 is deliberately broad rather than narrow: with 100 evals I want to locate the feasible area front in both families and see whether unrolled_k's constant-shift structure beats iterative's barrel shifters on area, before spending the reserved later rounds on fine mapping around whatever front emerges. If round 1 shows no design with max_abs_err <= 2^-10 and throughput_msps >= 1, the next decision will be infeasible rather than relaxing the spec.*)
- `iterative` (39 evals): data_width=10..20, n_iter=6..22, angle_guard=-1..3, frac_guard=0..2, rounding=trunc|round. *Why:* Area-minimal family: 1 shared datapath with barrel shifters and 1 micro-rotation/cycle. The >=1 MSPS constraint is not binding here - at these per-family Fmax values Fmax/(N+3) is far above 1 MSPS for the whole N range, so it only has to be checked, not optimised. The whole (luts_plus_ffs, accuracy_bits) front for this spec should come from here, so it gets the majority share. data_width 10..20 brackets the accuracy boundary (output LSB 2^-(W-2) => W~11-12 is the smallest width that can possibly carry 2^-10 after rounding) and extends to the HV reference area of 1500. n_iter 6..22 brackets the CORDIC residual-rotation boundary near N~10-12 and reaches accuracy_bits well above the 10-bit HV reference. angle_guard -1..3 and frac_guard 0..2 let the search buy a little internal precision cheaply instead of brute-forcing W and N, which is where the low-area end of the front will be decided. Both rounding modes are offered because round is expected to be the cheapest way to gain ~1 bit at the output.
- `unrolled_k` (21 evals): data_width=10..20, n_iter=6..22, angle_guard=-1..3, frac_guard=0..2, rounding=trunc|round, k=2..5. *Why:* Kept in the plan because it may be genuinely area-competitive with iterative: inside a k-group the shift amounts are constants, so it can avoid the barrel shifter that dominates iterative's LUTs, at the price of a few extra registers - exactly the trade-off that decides min luts_plus_ffs. Accuracy is bit-identical to iterative at the same (W, N, guards, rounding), so any point it wins on area is a strict front improvement and any point it loses on is dominated; the NSGA-II run will sort that out. k is held to 2..5 because throughput is already far above 1 MSPS at N=22 even with k=2, so larger k only adds chained logic without buying accuracy (accuracy depends on N, not k). Same W/N/guard ranges as iterative so the two families are compared on identical accuracy points.

**Result (code):** 60 evaluations this round, 60 total; 41 feasible; hypervolume 7302 (n/a).

**LLM decision:** `stop` — Final round (round cap reached). The front is feasible and well-covered, so `stop` is correct. Evidence: 41/60 evaluations feasible (32 unique), 0% violate the throughput constraint (best 18 MSPS vs required >=1) and the accuracy constraint is met by the whole front (best max_abs_err 9.54e-06 = 2^-16.68 vs limit 2^-10). The Pareto front spans luts_plus_ffs 274..779 and accuracy_bits 10.6..16.7, i.e. it covers a wide slice of both objectives against the HV reference (1500, 10), giving HV 7302. The selection rule (min luts_plus_ffs) is satisfied by iterative [data_width=16 n_iter=16 angle_guard=3 frac_guard=0 rounding=trunc]: luts_plus_ffs=274, accuracy_bits=10.6 (max_abs_err 2^-10.60 <= 2^-10), throughput 10.2 MSPS >= 1. No constraint is unreachable, so `infeasible` is not warranted; no further improvement is possible within the exhausted budget.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 7302 (gain this round: n/a (first round)).
Feasible designs: 41 of 60 evaluations (32 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 18
- max_abs_err <= 0.000976562: 32% violate; best seen 9.54e-06 (2^-16.68)

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=16 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=274, accuracy_bits=10.6, luts=175, ffs=99, throughput_msps=10.2, max_abs_err=0.000643 (2^-10.60), power_index=0.196
- iterative [data_width=18 n_iter=16 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=296, accuracy_bits=12.2, luts=191, ffs=105, throughput_msps=10.4, max_abs_err=0.000207 (2^-12.24), power_index=0.212
- iterative [data_width=17 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=300, accuracy_bits=12.5, luts=195, ffs=105, throughput_msps=10.2, max_abs_err=0.000174 (2^-12.49), power_index=0.214
- iterative [data_width=17 n_iter=20 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=323, accuracy_bits=12.5, luts=216, ffs=107, throughput_msps=6.91, max_abs_err=0.00017 (2^-12.52), power_index=0.279
- iterative [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=325, accuracy_bits=13.6, luts=214, ffs=111, throughput_msps=10.2, max_abs_err=8.08e-05 (2^-13.60), power_index=0.232
- iterative [data_width=18 n_iter=16 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=331, accuracy_bits=13.8, luts=218, ffs=113, throughput_msps=10.2, max_abs_err=6.86e-05 (2^-13.83), power_index=0.236
- iterative [data_width=20 n_iter=16 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=340, accuracy_bits=14.1, luts=221, ffs=119, throughput_msps=9.97, max_abs_err=5.76e-05 (2^-14.08), power_index=0.243
- iterative [data_width=20 n_iter=20 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=370, accuracy_bits=14.5, luts=249, ffs=120, throughput_msps=6.78, max_abs_err=4.23e-05 (2^-14.53), power_index=0.32
- unrolled_k [data_width=19 n_iter=21 angle_guard=3 frac_guard=2 rounding=round k=2] luts_plus_ffs=534, accuracy_bits=16, luts=416, ffs=118, throughput_msps=7.35, max_abs_err=1.48e-05 (2^-16.05), power_index=0.281
- unrolled_k [data_width=20 n_iter=22 angle_guard=2 frac_guard=2 rounding=round k=4] luts_plus_ffs=779, accuracy_bits=16.7, luts=658, ffs=121, throughput_msps=5.89, max_abs_err=9.54e-06 (2^-16.68), power_index=0.264
Front coverage: luts_plus_ffs 274..779 (HV reference 1500); accuracy_bits 10.6..16.7 (HV reference 10); data_width on the front 16..20 (registry 8..28).

Per family:
- iterative: 39 evals, 27 feasible; max throughput seen 18 MSPS; best accuracy 14.53 bits; best feasible luts_plus_ffs=274; feasible ranges: data_width 16..20, n_iter 13..20, angle_guard -1..3, frac_guard 0..2
- unrolled_k: 21 evals, 14 feasible; max throughput seen 12.7 MSPS; best accuracy 16.68 bits; best feasible luts_plus_ffs=458; feasible ranges: data_width 17..20, n_iter 14..22, angle_guard 2..3, frac_guard 0..2, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (32 evals): data_width=15..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (8 front designs; box front_anchored)
- `unrolled_k` (8 evals): data_width=18..28, n_iter=19..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 81 feasible; hypervolume 1.316e+04 (+80.3%).

**No LLM call** (code's front-mapping round): Final round (round cap reached). The front is feasible and well-covered, so `stop` is correct. Evidence: 41/60 evaluations feasible (32 unique), 0% violate the throughput constraint (best 18 MSPS vs required >=1) and the accuracy constraint is met by the whole front (best max_abs_err 9.54e-06 = 2^-16.68 vs limit 2^-10). The Pareto front spans luts_plus_ffs 274..779 and accuracy_bits 10.6..16.7, i.e. it covers a wide slice of both objectives against the HV reference (1500, 10), giving HV 7302. The selection rule (min luts_plus_ffs) is satisfied by iterative [data_width=16 n_iter=16 angle_guard=3 frac_guard=0 rounding=trunc]: luts_plus_ffs=274, accuracy_bits=10.6 (max_abs_err 2^-10.60 <= 2^-10), throughput 10.2 MSPS >= 1. No constraint is unreachable, so `infeasible` is not warranted; no further improvement is possible within the exhausted budget.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.316e+04 (gain this round: +80.3%).
Feasible designs: 81 of 100 evaluations (67 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 18
- max_abs_err <= 0.000976562: 19% violate; best seen 2.15e-07 (2^-22.15)

Pareto front (feasible, 17 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=269, accuracy_bits=10.6, luts=172, ffs=97, throughput_msps=11, max_abs_err=0.000643 (2^-10.60), power_index=0.182
- iterative [data_width=18 n_iter=16 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=296, accuracy_bits=12.2, luts=191, ffs=105, throughput_msps=10.4, max_abs_err=0.000207 (2^-12.24), power_index=0.212
- iterative [data_width=17 n_iter=20 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=323, accuracy_bits=12.5, luts=216, ffs=107, throughput_msps=6.91, max_abs_err=0.00017 (2^-12.52), power_index=0.279
- iterative [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=325, accuracy_bits=13.6, luts=214, ffs=111, throughput_msps=10.2, max_abs_err=8.08e-05 (2^-13.60), power_index=0.232
- iterative [data_width=20 n_iter=16 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=340, accuracy_bits=14.1, luts=221, ffs=119, throughput_msps=9.97, max_abs_err=5.76e-05 (2^-14.08), power_index=0.243
- iterative [data_width=22 n_iter=18 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=424, accuracy_bits=16.5, luts=293, ffs=130, throughput_msps=7.43, max_abs_err=1.1e-05 (2^-16.47), power_index=0.335
- iterative [data_width=22 n_iter=27 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=430, accuracy_bits=17.5, luts=301, ffs=129, throughput_msps=5.2, max_abs_err=5.49e-06 (2^-17.47), power_index=0.485
- iterative [data_width=23 n_iter=25 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=448, accuracy_bits=17.9, luts=316, ffs=132, throughput_msps=5.57, max_abs_err=3.98e-06 (2^-17.94), power_index=0.472
- iterative [data_width=27 n_iter=23 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=535, accuracy_bits=21, luts=383, ffs=152, throughput_msps=5.89, max_abs_err=4.81e-07 (2^-20.99), power_index=0.524
- iterative [data_width=27 n_iter=25 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=556, accuracy_bits=22.1, luts=399, ffs=156, throughput_msps=5.38, max_abs_err=2.15e-07 (2^-22.15), power_index=0.585
Front coverage: luts_plus_ffs 269..556 (HV reference 1500); accuracy_bits 10.6..22.1 (HV reference 10); data_width on the front 16..27 (registry 8..28).

Per family:
- iterative: 71 evals, 59 feasible; max throughput seen 18 MSPS; best accuracy 22.15 bits; best feasible luts_plus_ffs=269; feasible ranges: data_width 16..27, n_iter 13..29, angle_guard -1..4, frac_guard 0..4
- unrolled_k: 29 evals, 22 feasible; max throughput seen 12.7 MSPS; best accuracy 21.66 bits; best feasible luts_plus_ffs=458; feasible ranges: data_width 17..28, n_iter 14..28, angle_guard -1..4, frac_guard 0..3, k 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4417 in, 4879 out
- provider-reported cost: $0.0034
- full prompts and replies: `llm_trace.jsonl`

