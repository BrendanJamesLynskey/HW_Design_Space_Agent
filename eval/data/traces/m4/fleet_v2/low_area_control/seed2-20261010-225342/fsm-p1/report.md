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
`iterative:data_width=16,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 193 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 102 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 11 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 90.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.2 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000241 (2^-12.02) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.94 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 5.15e-05 (2^-14.25) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 0.844 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (18 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=16,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc` | 193 | 102 | 11.0 | 18 | 0.2 | 0.000241 (2^-12.02) | 12.02 |
| 1 | `iterative:data_width=18,n_iter=17,angle_guard=-1,frac_guard=0,rounding=trunc` | 210 | 106 | 8.1 | 20 | 0.238 | 0.000195 (2^-12.32) | 12.32 |
| 2 | `iterative:data_width=16,n_iter=15,angle_guard=2,frac_guard=1,rounding=round` | 225 | 100 | 11.0 | 18 | 0.22 | 0.00018 (2^-12.44) | 12.44 |
| 3 | `iterative:data_width=17,n_iter=24,angle_guard=2,frac_guard=2,rounding=trunc` | 230 | 108 | 5.9 | 27 | 0.343 | 0.00013 (2^-12.91) | 12.91 |
| 4 | `iterative:data_width=17,n_iter=24,angle_guard=4,frac_guard=2,rounding=trunc` | 233 | 110 | 5.9 | 27 | 0.349 | 0.000114 (2^-13.10) | 13.10 |
| 5 | `iterative:data_width=17,n_iter=24,angle_guard=2,frac_guard=3,rounding=trunc` | 245 | 110 | 5.9 | 27 | 0.361 | 8.39e-05 (2^-13.54) | 13.54 |
| 6 | `iterative:data_width=21,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 235 | 121 | 10.8 | 18 | 0.241 | 6.94e-05 (2^-13.81) | 13.81 |
| 7 | `iterative:data_width=21,n_iter=17,angle_guard=0,frac_guard=0,rounding=trunc` | 260 | 122 | 7.9 | 20 | 0.287 | 3.42e-05 (2^-14.83) | 14.83 |
| 8 | `iterative:data_width=21,n_iter=24,angle_guard=3,frac_guard=0,rounding=trunc` | 270 | 125 | 5.8 | 27 | 0.401 | 2.36e-05 (2^-15.37) | 15.37 |
| 9 | `iterative:data_width=21,n_iter=30,angle_guard=0,frac_guard=0,rounding=round` | 281 | 122 | 4.8 | 33 | 0.501 | 1.79e-05 (2^-15.77) | 15.77 |
| 10 | `iterative:data_width=21,n_iter=26,angle_guard=2,frac_guard=1,rounding=trunc` | 284 | 126 | 5.4 | 29 | 0.447 | 1.51e-05 (2^-16.02) | 16.02 |
| 11 | `iterative:data_width=21,n_iter=18,angle_guard=3,frac_guard=3,rounding=trunc` | 308 | 131 | 7.4 | 21 | 0.347 | 1.08e-05 (2^-16.50) | 16.50 |
| 12 | `iterative:data_width=21,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc` | 320 | 131 | 5.4 | 29 | 0.492 | 5.08e-06 (2^-17.59) | 17.59 |
| 13 | `iterative:data_width=25,n_iter=24,angle_guard=0,frac_guard=0,rounding=trunc` | 334 | 142 | 5.8 | 27 | 0.484 | 1.65e-06 (2^-19.21) | 19.21 |
| 14 | `iterative:data_width=28,n_iter=24,angle_guard=3,frac_guard=2,rounding=trunc` | 424 | 164 | 5.6 | 27 | 0.597 | 1.59e-07 (2^-22.58) | 22.58 |
| 15 | `iterative:data_width=28,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc` | 453 | 166 | 5.2 | 29 | 0.676 | 5.73e-08 (2^-24.06) | 24.06 |
| 16 | `iterative:data_width=28,n_iter=26,angle_guard=3,frac_guard=3,rounding=round` | 527 | 166 | 5.2 | 29 | 0.757 | 4.85e-08 (2^-24.30) | 24.30 |
| 17 | `iterative:data_width=28,n_iter=30,angle_guard=3,frac_guard=3,rounding=round` | 536 | 166 | 4.6 | 33 | 0.872 | 2.91e-08 (2^-25.04) | 25.04 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-dominated (minimise luts_plus_ffs) with a hard throughput floor (>=1 MSPS) and a hard accuracy ceiling (max_abs_err <= 2^-10). Among my two allowed families, unrolled_k is the only one that can meet the throughput constraint while staying low-area, so it is the primary target and receives the full budget. iterative is included with zero share as a low-area anchor to characterise the area/accuracy end of the front (it will mostly be throughput-infeasible, but it defines the minimum-area reference point and guards against missing a feasible low-area corner). Parameter ranges are deliberately narrow and centred on the accuracy threshold (W ~ 10-16, N ~ 10-16, guards near 0) so that Optuna's NSGA-II spends its 100 evals mapping the genuine trade-off curve (area vs accuracy_bits vs throughput) rather than exploring grossly infeasible or over-provisioned regions. Rounding is left to both options so the optimizer can pick the cheaper truncation where it still meets 2^-10. The selection rule (min luts_plus_ffs) and the hypervolume objective (ref 1500 area / 10 accuracy) both reward the low-area, just-meets-accuracy corner, which is exactly where these ranges focus the search.*)
- `iterative` (5 evals): data_width=10..16, n_iter=10..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the smallest-area family (single shared datapath, no k-way or pipeline register duplication). It is the only candidate that can plausibly minimise luts_plus_ffs while still meeting max_abs_err <= 2^-10. It is kept in the search so the front's low-area corner is covered, but it is throughput-limited (1 result per N+3 cycles), so it will generally fail the >=1 MSPS constraint at realistic Fmax; it mainly anchors the area/accuracy trade-off. Ranges are kept tight around the accuracy threshold (W~12-14, N~12-14) to avoid wasting evals on grossly over- or under-accurate points.
- `unrolled_k` (55 evals): data_width=10..16, n_iter=10..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..8. *Why:* unrolled_k is the only family that can satisfy BOTH constraints: k chained micro-rotations/cycle raises throughput to Fmax*ceil(N/k) results/cycle, which can clear >=1 MSPS, while the shared FSM keeps area far below a fully pipelined design. This is where the feasible Pareto front lives for this spec, so it takes the entire budget. k is swept 2..8 to map the throughput-vs-area trade-off (larger k = more parallel datapath = more LUTs/FFs but higher throughput); data_width/n_iter are centred on the 2^-10 accuracy requirement so the search spends evals on the accuracy/area boundary rather than trivially over-accurate or infeasible points. angle_guard/frac_guard are kept near zero to minimise area, with a little headroom to let the optimizer trade a few guard bits for accuracy_bits.

**Result (code):** 60 evaluations this round, 60 total; 29 feasible; hypervolume 2931 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is established with 2 designs. The best design (iterative, W=16, N=15, ag=2, fg=2, trunc) achieves luts_plus_ffs=295 and accuracy_bits=12.02, satisfying all constraints (throughput 11 MSPS >= 1, max_abs_err 2^-12.02 <= 2^-10). The selection rule (min luts_plus_ffs) picks this design. Since this is the final round, the exploration concludes with this feasible front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 2931 (gain this round: n/a (first round)).
Feasible designs: 29 of 60 evaluations (20 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 52% violate; best seen 0.00018 (2^-12.44)

Pareto front (feasible, 2 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=295, accuracy_bits=12, luts=193, ffs=102, throughput_msps=11, max_abs_err=0.000241 (2^-12.02), power_index=0.2
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=324, accuracy_bits=12.4, luts=225, ffs=100, throughput_msps=11, max_abs_err=0.00018 (2^-12.44), power_index=0.22
Front coverage: luts_plus_ffs 295..324 (HV reference 1500); accuracy_bits 12..12.4 (HV reference 10); data_width on the front 16..16 (registry 8..28).

Per family:
- iterative: 5 evals, 2 feasible; max throughput seen 15.6 MSPS; best accuracy 12.44 bits; best feasible luts_plus_ffs=295; feasible ranges: data_width 16..16, n_iter 15..15, angle_guard 2..2, frac_guard 1..2
- unrolled_k: 55 evals, 27 feasible; max throughput seen 14 MSPS; best accuracy 11.95 bits; best feasible luts_plus_ffs=390; feasible ranges: data_width 14..16, n_iter 12..16, angle_guard 1..2, frac_guard 0..2, k 2..7
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (40 evals): data_width=15..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 69 feasible; hypervolume 1.542e+04 (+426.2%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is established with 2 designs. The best design (iterative, W=16, N=15, ag=2, fg=2, trunc) achieves luts_plus_ffs=295 and accuracy_bits=12.02, satisfying all constraints (throughput 11 MSPS >= 1, max_abs_err 2^-12.02 <= 2^-10). The selection rule (min luts_plus_ffs) picks this design. Since this is the final round, the exploration concludes with this feasible front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.542e+04 (gain this round: +426.2%).
Feasible designs: 69 of 100 evaluations (57 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 31% violate; best seen 2.91e-08 (2^-25.04)

Pareto front (feasible, 18 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=295, accuracy_bits=12, luts=193, ffs=102, throughput_msps=11, max_abs_err=0.000241 (2^-12.02), power_index=0.2
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=324, accuracy_bits=12.4, luts=225, ffs=100, throughput_msps=11, max_abs_err=0.00018 (2^-12.44), power_index=0.22
- iterative [data_width=17 n_iter=24 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=343, accuracy_bits=13.1, luts=233, ffs=110, throughput_msps=5.89, max_abs_err=0.000114 (2^-13.10), power_index=0.349
- iterative [data_width=21 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=356, accuracy_bits=13.8, luts=235, ffs=121, throughput_msps=10.8, max_abs_err=6.94e-05 (2^-13.81), power_index=0.241
- iterative [data_width=21 n_iter=24 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=395, accuracy_bits=15.4, luts=270, ffs=125, throughput_msps=5.78, max_abs_err=2.36e-05 (2^-15.37), power_index=0.401
- iterative [data_width=21 n_iter=30 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=403, accuracy_bits=15.8, luts=281, ffs=122, throughput_msps=4.82, max_abs_err=1.79e-05 (2^-15.77), power_index=0.501
- iterative [data_width=21 n_iter=18 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=439, accuracy_bits=16.5, luts=308, ffs=131, throughput_msps=7.43, max_abs_err=1.08e-05 (2^-16.50), power_index=0.347
- iterative [data_width=25 n_iter=24 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=477, accuracy_bits=19.2, luts=334, ffs=142, throughput_msps=5.78, max_abs_err=1.65e-06 (2^-19.21), power_index=0.484
- iterative [data_width=28 n_iter=26 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=619, accuracy_bits=24.1, luts=453, ffs=166, throughput_msps=5.19, max_abs_err=5.73e-08 (2^-24.06), power_index=0.676
- iterative [data_width=28 n_iter=30 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=703, accuracy_bits=25, luts=536, ffs=166, throughput_msps=4.56, max_abs_err=2.91e-08 (2^-25.04), power_index=0.872
Front coverage: luts_plus_ffs 295..703 (HV reference 1500); accuracy_bits 12..25 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- iterative: 45 evals, 42 feasible; max throughput seen 15.6 MSPS; best accuracy 25.04 bits; best feasible luts_plus_ffs=295; feasible ranges: data_width 16..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 55 evals, 27 feasible; max throughput seen 14 MSPS; best accuracy 11.95 bits; best feasible luts_plus_ffs=390; feasible ranges: data_width 14..16, n_iter 12..16, angle_guard 1..2, frac_guard 0..2, k 2..7
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 3789 in, 1188 out
- provider-reported cost: $0.0025
- full prompts and replies: `llm_trace.jsonl`

