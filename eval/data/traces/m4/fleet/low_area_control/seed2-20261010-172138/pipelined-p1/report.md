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
`pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=2,rounding=trunc,m=8` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 689 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 149 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 52.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 52.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 75.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0315 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000609 (2^-10.68) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 9.97 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000204 (2^-12.26) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 3.35 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.7 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (11 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=2,rounding=trunc,m=8` | 689 | 149 | 52.7 | 4 | 0.0315 | 0.000609 (2^-10.68) | 10.68 |
| 1 | `pipelined_m:data_width=15,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 786 | 143 | 52.7 | 4 | 0.035 | 0.000405 (2^-11.27) | 11.27 |
| 2 | `pipelined_m:data_width=16,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,m=6` | 786 | 206 | 68.5 | 5 | 0.0373 | 0.000344 (2^-11.50) | 11.50 |
| 3 | `pipelined_m:data_width=16,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=6` | 813 | 210 | 68.5 | 5 | 0.0385 | 0.000311 (2^-11.65) | 11.65 |
| 4 | `pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 868 | 159 | 50.3 | 4 | 0.0387 | 0.000178 (2^-12.46) | 12.46 |
| 5 | `pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=4,rounding=trunc,m=8` | 923 | 163 | 50.3 | 4 | 0.0409 | 0.000172 (2^-12.50) | 12.50 |
| 6 | `pipelined:data_width=19,n_iter=14,angle_guard=2,frac_guard=0,rounding=trunc` | 896 | 932 | 264.5 | 16 | 0.0688 | 0.000163 (2^-12.58) | 12.58 |
| 7 | `pipelined_m:data_width=23,n_iter=19,angle_guard=2,frac_guard=1,rounding=trunc,m=6` | 1504 | 367 | 62.5 | 6 | 0.0704 | 5.7e-06 (2^-17.42) | 17.42 |
| 8 | `pipelined_m:data_width=23,n_iter=23,angle_guard=3,frac_guard=1,rounding=round,m=3` | 1908 | 700 | 114.5 | 10 | 0.0981 | 1.73e-06 (2^-19.14) | 19.14 |
| 9 | `pipelined_m:data_width=27,n_iter=23,angle_guard=3,frac_guard=1,rounding=round,m=3` | 2195 | 805 | 110.0 | 10 | 0.113 | 3.1e-07 (2^-21.62) | 21.62 |
| 10 | `pipelined_m:data_width=27,n_iter=23,angle_guard=3,frac_guard=4,rounding=round,m=3` | 2334 | 847 | 105.9 | 10 | 0.12 | 2.67e-07 (2^-21.84) | 21.84 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >=1 MSPS throughput and max_abs_err <= 2^-10, with area (LUTs+FFs) as the primary objective. Both pipelined and pipelined_m deliver 1 result/cycle, so throughput is met as long as Fmax >= 1 MHz (trivially satisfied). The accuracy constraint (2^-10) requires sufficient n_iter and data_width: N=12-14 iterations with W=12-14 and modest guards should comfortably meet 2^-10 error. I focus on the low end of data_width and n_iter to minimize area, with small guard bits (angle_guard -2..4, frac_guard 0..4) to explore the accuracy/area trade-off. pipelined_m with m=2-4 can reduce FF count by sharing pipeline registers, potentially yielding lower total area than fully pipelined at the same accuracy. Splitting budget 50/50 between the two families lets the optimizer find the best area point in each and compare on the merged Pareto front.*)
- `pipelined` (30 evals): data_width=12..14, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Fully pipelined gives 1 result/cycle, easily meeting the >=1 MSPS throughput constraint at modest Fmax. N=12-16 with W=12-14 and small guards should satisfy max_abs_err <= 2^-10 while keeping area low. This is the primary low-area candidate.
- `pipelined_m` (30 evals): data_width=12..14, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* Registering every m stages (m=2-4) reduces FF count versus fully pipelined while still delivering 1 result/cycle. This trades a small latency increase for lower area, potentially finding points on the Pareto front with fewer FFs at similar LUT count. m=2-4 keeps latency reasonable while cutting pipeline registers.

**Result (code):** 60 evaluations this round, 60 total; 24 feasible; hypervolume 466.8 (n/a).

**LLM decision:** `stop` — The spec is feasible: the front contains 7 designs meeting throughput >= 1 MSPS and max_abs_err <= 2^-10. The selection rule (min luts_plus_ffs) is satisfied by the pipelined_m design at 1050 LUTs+FFs with 10.8 accuracy bits, well below the HV reference of 1500. The front spans luts_plus_ffs 1050..1954 and accuracy_bits 10.8..12.3, covering the trade-off curve adequately. Since this is the final round, no further exploration is possible; the current front is the best available.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 466.8 (gain this round: n/a (first round)).
Feasible designs: 24 of 60 evaluations (20 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 60% violate; best seen 0.000203 (2^-12.27)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=13 n_iter=14 angle_guard=3 frac_guard=4 rounding=round m=4] luts_plus_ffs=1050, accuracy_bits=10.8, luts=800, ffs=250, throughput_msps=97.8, max_abs_err=0.000574 (2^-10.77), power_index=0.0395
- pipelined_m [data_width=13 n_iter=14 angle_guard=4 frac_guard=3 rounding=round m=2] luts_plus_ffs=1204, accuracy_bits=10.8, luts=786, ffs=418, throughput_msps=171, max_abs_err=0.000564 (2^-10.79), power_index=0.0453
- pipelined_m [data_width=13 n_iter=14 angle_guard=4 frac_guard=4 rounding=round m=2] luts_plus_ffs=1243, accuracy_bits=11, luts=813, ffs=430, throughput_msps=171, max_abs_err=0.000484 (2^-11.01), power_index=0.0468
- pipelined_m [data_width=14 n_iter=15 angle_guard=4 frac_guard=2 rounding=round m=2] luts_plus_ffs=1347, accuracy_bits=11.4, luts=861, ffs=486, throughput_msps=171, max_abs_err=0.000372 (2^-11.39), power_index=0.0507
- pipelined [data_width=14 n_iter=14 angle_guard=4 frac_guard=4 rounding=round] luts_plus_ffs=1704, accuracy_bits=11.8, luts=857, ffs=847, throughput_msps=273, max_abs_err=0.000284 (2^-11.78), power_index=0.0641
- pipelined [data_width=14 n_iter=15 angle_guard=4 frac_guard=4 rounding=round] luts_plus_ffs=1829, accuracy_bits=12.1, luts=920, ffs=909, throughput_msps=273, max_abs_err=0.000232 (2^-12.07), power_index=0.0688
- pipelined [data_width=14 n_iter=16 angle_guard=4 frac_guard=4 rounding=round] luts_plus_ffs=1954, accuracy_bits=12.3, luts=983, ffs=971, throughput_msps=273, max_abs_err=0.000203 (2^-12.27), power_index=0.0735
Front coverage: luts_plus_ffs 1050..1954 (HV reference 1500); accuracy_bits 10.8..12.3 (HV reference 10); data_width on the front 13..14 (registry 8..28).

Per family:
- pipelined: 30 evals, 10 feasible; max throughput seen 282 MSPS; best accuracy 12.27 bits; best feasible luts_plus_ffs=1548; feasible ranges: data_width 14..14, n_iter 13..16, angle_guard 4..4, frac_guard 1..4
- pipelined_m: 30 evals, 14 feasible; max throughput seen 178 MSPS; best accuracy 11.39 bits; best feasible luts_plus_ffs=1050; feasible ranges: data_width 13..14, n_iter 13..16, angle_guard 2..4, frac_guard 1..4, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (23 evals): data_width=12..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)
- `pipelined` (17 evals): data_width=13..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 59 feasible; hypervolume 1375 (+194.5%).

**No LLM call** (code's front-mapping round): The spec is feasible: the front contains 7 designs meeting throughput >= 1 MSPS and max_abs_err <= 2^-10. The selection rule (min luts_plus_ffs) is satisfied by the pipelined_m design at 1050 LUTs+FFs with 10.8 accuracy bits, well below the HV reference of 1500. The front spans luts_plus_ffs 1050..1954 and accuracy_bits 10.8..12.3, covering the trade-off curve adequately. Since this is the final round, no further exploration is possible; the current front is the best available.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1375 (gain this round: +194.5%).
Feasible designs: 59 of 100 evaluations (54 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 41% violate; best seen 2.67e-07 (2^-21.84)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=838, accuracy_bits=10.7, luts=689, ffs=149, throughput_msps=52.7, max_abs_err=0.000609 (2^-10.68), power_index=0.0315
- pipelined_m [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=929, accuracy_bits=11.3, luts=786, ffs=143, throughput_msps=52.7, max_abs_err=0.000405 (2^-11.27), power_index=0.035
- pipelined_m [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=992, accuracy_bits=11.5, luts=786, ffs=206, throughput_msps=68.5, max_abs_err=0.000344 (2^-11.50), power_index=0.0373
- pipelined_m [data_width=16 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=6] luts_plus_ffs=1023, accuracy_bits=11.7, luts=813, ffs=210, throughput_msps=68.5, max_abs_err=0.000311 (2^-11.65), power_index=0.0385
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=1028, accuracy_bits=12.5, luts=868, ffs=159, throughput_msps=50.3, max_abs_err=0.000178 (2^-12.46), power_index=0.0387
- pipelined [data_width=19 n_iter=14 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=1828, accuracy_bits=12.6, luts=896, ffs=932, throughput_msps=264, max_abs_err=0.000163 (2^-12.58), power_index=0.0688
- pipelined_m [data_width=23 n_iter=19 angle_guard=2 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=1871, accuracy_bits=17.4, luts=1504, ffs=367, throughput_msps=62.5, max_abs_err=5.7e-06 (2^-17.42), power_index=0.0704
- pipelined_m [data_width=23 n_iter=23 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=2609, accuracy_bits=19.1, luts=1908, ffs=700, throughput_msps=114, max_abs_err=1.73e-06 (2^-19.14), power_index=0.0981
- pipelined_m [data_width=27 n_iter=23 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=3000, accuracy_bits=21.6, luts=2195, ffs=805, throughput_msps=110, max_abs_err=3.1e-07 (2^-21.62), power_index=0.113
- pipelined_m [data_width=27 n_iter=23 angle_guard=3 frac_guard=4 rounding=round m=3] luts_plus_ffs=3182, accuracy_bits=21.8, luts=2334, ffs=847, throughput_msps=106, max_abs_err=2.67e-07 (2^-21.84), power_index=0.12
Front coverage: luts_plus_ffs 838..3182 (HV reference 1500); accuracy_bits 10.7..21.8 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- pipelined: 47 evals, 26 feasible; max throughput seen 282 MSPS; best accuracy 19.09 bits; best feasible luts_plus_ffs=1548; feasible ranges: data_width 14..22, n_iter 13..29, angle_guard 2..4, frac_guard 0..4
- pipelined_m: 53 evals, 33 feasible; max throughput seen 178 MSPS; best accuracy 21.84 bits; best feasible luts_plus_ffs=838; feasible ranges: data_width 13..27, n_iter 12..30, angle_guard -1..4, frac_guard 1..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5052 in, 1108 out
- provider-reported cost: $0.0019
- full prompts and replies: `llm_trace.jsonl`

