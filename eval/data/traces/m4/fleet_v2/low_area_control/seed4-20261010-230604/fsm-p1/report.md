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
`iterative:data_width=16,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 170 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 96 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 11 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 90.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.18 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000643 (2^-10.60) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 10.5 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000137 (2^-12.83) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 2.25 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.6 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (16 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=16,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc` | 170 | 96 | 11.0 | 18 | 0.18 | 0.000643 (2^-10.60) | 10.60 |
| 1 | `iterative:data_width=16,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc` | 170 | 96 | 10.4 | 19 | 0.19 | 0.000643 (2^-10.60) | 10.60 |
| 2 | `iterative:data_width=16,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 178 | 96 | 11.0 | 18 | 0.185 | 0.000373 (2^-11.39) | 11.39 |
| 3 | `iterative:data_width=17,n_iter=14,angle_guard=4,frac_guard=0,rounding=round` | 196 | 105 | 11.4 | 17 | 0.193 | 0.000197 (2^-12.31) | 12.31 |
| 4 | `iterative:data_width=17,n_iter=21,angle_guard=4,frac_guard=0,rounding=round` | 217 | 106 | 6.6 | 24 | 0.291 | 0.000146 (2^-12.74) | 12.74 |
| 5 | `iterative:data_width=18,n_iter=21,angle_guard=3,frac_guard=0,rounding=round` | 231 | 110 | 6.6 | 24 | 0.308 | 7.75e-05 (2^-13.65) | 13.65 |
| 6 | `iterative:data_width=18,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc` | 263 | 115 | 5.7 | 28 | 0.398 | 5.18e-05 (2^-14.24) | 14.24 |
| 7 | `iterative:data_width=22,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc` | 282 | 127 | 6.4 | 25 | 0.385 | 1.39e-05 (2^-16.14) | 16.14 |
| 8 | `iterative:data_width=23,n_iter=21,angle_guard=-1,frac_guard=0,rounding=trunc` | 298 | 131 | 6.5 | 24 | 0.387 | 8.62e-06 (2^-16.82) | 16.82 |
| 9 | `iterative:data_width=22,n_iter=26,angle_guard=3,frac_guard=0,rounding=round` | 303 | 130 | 5.4 | 29 | 0.472 | 5.23e-06 (2^-17.54) | 17.54 |
| 10 | `iterative:data_width=23,n_iter=21,angle_guard=2,frac_guard=1,rounding=trunc` | 319 | 136 | 6.5 | 24 | 0.411 | 3.24e-06 (2^-18.24) | 18.24 |
| 11 | `iterative:data_width=26,n_iter=26,angle_guard=-2,frac_guard=0,rounding=trunc` | 354 | 145 | 5.4 | 29 | 0.545 | 2.08e-06 (2^-18.87) | 18.87 |
| 12 | `iterative:data_width=26,n_iter=26,angle_guard=0,frac_guard=0,rounding=trunc` | 358 | 147 | 5.4 | 29 | 0.551 | 9.44e-07 (2^-20.02) | 20.02 |
| 13 | `iterative:data_width=26,n_iter=26,angle_guard=1,frac_guard=0,rounding=trunc` | 360 | 148 | 5.3 | 29 | 0.554 | 8.42e-07 (2^-20.18) | 20.18 |
| 14 | `iterative:data_width=28,n_iter=25,angle_guard=2,frac_guard=0,rounding=trunc` | 400 | 159 | 5.5 | 28 | 0.589 | 2.16e-07 (2^-22.14) | 22.14 |
| 15 | `iterative:data_width=28,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc` | 451 | 165 | 5.4 | 28 | 0.649 | 9.99e-08 (2^-23.26) | 23.26 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >=1 MSPS and max_abs_err <= 2^-10, with area (luts_plus_ffs) as the primary objective. iterative is the area-minimal family and the most likely to dominate the selection rule (min luts_plus_ffs). unrolled_k with small k (2-4) provides throughput headroom at low area cost, populating the Pareto front where iterative might be Fmax-limited. Both families share identical accuracy behaviour, so I focus the search on the data_width/n_iter/guard ranges that satisfy the 10-bit error constraint while keeping area minimal. angle_guard is kept low (-2..0) and frac_guard low (0..1) to minimise area; rounding is explored to capture any accuracy/area trade-off. Budget is split evenly since both families are viable and the front spans both.*)
- `iterative` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=-2..0, frac_guard=0..1, rounding=trunc|round. *Why:* iterative is the smallest-area family (single datapath, no pipeline registers). It is the only family that can plausibly minimise luts_plus_ffs while meeting max_abs_err <= 2^-10. data_width 12-16 and n_iter 10-16 cover the accuracy sweet spot; angle_guard -2..0 and frac_guard 0..1 keep area low without sacrificing the 10-bit error budget.
- `unrolled_k` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=-2..0, frac_guard=0..1, rounding=trunc|round, k=2..4. *Why:* unrolled_k with k=2..4 can hit >=1 MSPS at modest Fmax without the register overhead of full pipelining. It trades a little area for throughput headroom, giving the Pareto front a second axis to explore. Same accuracy ranges as iterative since accuracy depends only on data_width/n_iter/guards/rounding.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 60 evaluations this round, 60 total; 18 feasible; hypervolume 1794 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 4 unique designs. The minimum area design (iterative, W=16, N=15, trunc) achieves 266 LUTs+FFs with 10.6 bits accuracy, comfortably meeting the throughput (11 MSPS >= 1) and accuracy (2^-10.60 <= 2^-10) constraints. The front covers the trade-off space from 266 to 319 area units and 10.6 to 11.5 accuracy bits. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (266) as per the spec's selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1794 (gain this round: n/a (first round)).
Feasible designs: 18 of 60 evaluations (9 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 70% violate; best seen 0.000355 (2^-11.46)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=266, accuracy_bits=10.6, luts=170, ffs=96, throughput_msps=11, max_abs_err=0.000643 (2^-10.60), power_index=0.18
- iterative [data_width=16 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=266, accuracy_bits=10.6, luts=170, ffs=96, throughput_msps=10.4, max_abs_err=0.000643 (2^-10.60), power_index=0.19
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.4, luts=178, ffs=96, throughput_msps=11, max_abs_err=0.000373 (2^-11.39), power_index=0.185
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=1 rounding=round] luts_plus_ffs=319, accuracy_bits=11.5, luts=221, ffs=98, throughput_msps=11, max_abs_err=0.000355 (2^-11.46), power_index=0.216
Front coverage: luts_plus_ffs 266..319 (HV reference 1500); accuracy_bits 10.6..11.5 (HV reference 10); data_width on the front 16..16 (registry 8..28).

Per family:
- iterative: 30 evals, 16 feasible; max throughput seen 15.6 MSPS; best accuracy 11.46 bits; best feasible luts_plus_ffs=266; feasible ranges: data_width 16..16, n_iter 13..16, angle_guard 0..0, frac_guard 0..1
- unrolled_k: 30 evals, 2 feasible; max throughput seen 14 MSPS; best accuracy 10.49 bits; best feasible luts_plus_ffs=408; feasible ranges: data_width 16..16, n_iter 14..15, angle_guard -1..-1, frac_guard 0..1, k 3..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (40 evals): data_width=15..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (4 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 56 feasible; hypervolume 1.41e+04 (+685.9%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 4 unique designs. The minimum area design (iterative, W=16, N=15, trunc) achieves 266 LUTs+FFs with 10.6 bits accuracy, comfortably meeting the throughput (11 MSPS >= 1) and accuracy (2^-10.60 <= 2^-10) constraints. The front covers the trade-off space from 266 to 319 area units and 10.6 to 11.5 accuracy bits. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (266) as per the spec's selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.41e+04 (gain this round: +685.9%).
Feasible designs: 56 of 100 evaluations (47 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 44% violate; best seen 9.99e-08 (2^-23.26)

Pareto front (feasible, 16 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=266, accuracy_bits=10.6, luts=170, ffs=96, throughput_msps=11, max_abs_err=0.000643 (2^-10.60), power_index=0.18
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11.4, luts=178, ffs=96, throughput_msps=11, max_abs_err=0.000373 (2^-11.39), power_index=0.185
- iterative [data_width=17 n_iter=14 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=301, accuracy_bits=12.3, luts=196, ffs=105, throughput_msps=11.4, max_abs_err=0.000197 (2^-12.31), power_index=0.193
- iterative [data_width=18 n_iter=21 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=341, accuracy_bits=13.7, luts=231, ffs=110, throughput_msps=6.62, max_abs_err=7.75e-05 (2^-13.65), power_index=0.308
- iterative [data_width=22 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=409, accuracy_bits=16.1, luts=282, ffs=127, throughput_msps=6.36, max_abs_err=1.39e-05 (2^-16.14), power_index=0.385
- iterative [data_width=23 n_iter=21 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=429, accuracy_bits=16.8, luts=298, ffs=131, throughput_msps=6.5, max_abs_err=8.62e-06 (2^-16.82), power_index=0.387
- iterative [data_width=23 n_iter=21 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=455, accuracy_bits=18.2, luts=319, ffs=136, throughput_msps=6.5, max_abs_err=3.24e-06 (2^-18.24), power_index=0.411
- iterative [data_width=26 n_iter=26 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=505, accuracy_bits=20, luts=358, ffs=147, throughput_msps=5.38, max_abs_err=9.44e-07 (2^-20.02), power_index=0.551
- iterative [data_width=26 n_iter=26 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=508, accuracy_bits=20.2, luts=360, ffs=148, throughput_msps=5.28, max_abs_err=8.42e-07 (2^-20.18), power_index=0.554
- iterative [data_width=28 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=617, accuracy_bits=23.3, luts=451, ffs=165, throughput_msps=5.38, max_abs_err=9.99e-08 (2^-23.26), power_index=0.649
Front coverage: luts_plus_ffs 266..617 (HV reference 1500); accuracy_bits 10.6..23.3 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- iterative: 70 evals, 54 feasible; max throughput seen 15.6 MSPS; best accuracy 23.26 bits; best feasible luts_plus_ffs=266; feasible ranges: data_width 16..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 30 evals, 2 feasible; max throughput seen 14 MSPS; best accuracy 10.49 bits; best feasible luts_plus_ffs=408; feasible ranges: data_width 16..16, n_iter 14..15, angle_guard -1..-1, frac_guard 0..1, k 3..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 3984 in, 1093 out
- provider-reported cost: $0.0045
- full prompts and replies: `llm_trace.jsonl`

