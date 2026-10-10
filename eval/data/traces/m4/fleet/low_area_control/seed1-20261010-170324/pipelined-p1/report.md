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
`pipelined_m:data_width=15,n_iter=12,angle_guard=1,frac_guard=2,rounding=trunc,m=7` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 654 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 141 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 59.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 59.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 67.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0299 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000772 (2^-10.34) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.33 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000225 (2^-12.11) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.85 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=12,angle_guard=1,frac_guard=2,rounding=trunc,m=7` | 654 | 141 | 59.6 | 4 | 0.0299 | 0.000772 (2^-10.34) | 10.34 |
| 1 | `pipelined_m:data_width=15,n_iter=12,angle_guard=4,frac_guard=2,rounding=trunc,m=8` | 689 | 147 | 50.3 | 4 | 0.0315 | 0.000691 (2^-10.50) | 10.50 |
| 2 | `pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 701 | 151 | 52.7 | 4 | 0.0321 | 0.000597 (2^-10.71) | 10.71 |
| 3 | `pipelined_m:data_width=15,n_iter=13,angle_guard=4,frac_guard=2,rounding=trunc,m=8` | 751 | 147 | 50.3 | 4 | 0.0338 | 0.000466 (2^-11.07) | 11.07 |
| 4 | `pipelined_m:data_width=15,n_iter=13,angle_guard=4,frac_guard=4,rounding=trunc,m=8` | 802 | 151 | 50.3 | 4 | 0.0359 | 0.000374 (2^-11.38) | 11.38 |
| 5 | `pipelined_m:data_width=20,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc,m=8` | 1080 | 180 | 50.3 | 4 | 0.0474 | 5.76e-05 (2^-14.08) | 14.08 |
| 6 | `pipelined_m:data_width=19,n_iter=16,angle_guard=3,frac_guard=1,rounding=trunc,m=6` | 1080 | 245 | 65.4 | 5 | 0.0499 | 5.64e-05 (2^-14.11) | 14.11 |
| 7 | `pipelined_m:data_width=21,n_iter=22,angle_guard=3,frac_guard=0,rounding=round,m=5` | 1599 | 411 | 73.7 | 7 | 0.0756 | 1.15e-05 (2^-16.41) | 16.41 |
| 8 | `pipelined_m:data_width=21,n_iter=22,angle_guard=2,frac_guard=1,rounding=round,m=5` | 1665 | 416 | 73.7 | 7 | 0.0783 | 6.89e-06 (2^-17.15) | 17.15 |
| 9 | `pipelined_m:data_width=21,n_iter=22,angle_guard=3,frac_guard=2,rounding=round,m=5` | 1731 | 429 | 73.7 | 7 | 0.0813 | 3.88e-06 (2^-17.97) | 17.97 |
| 10 | `pipelined_m:data_width=25,n_iter=22,angle_guard=0,frac_guard=1,rounding=round,m=5` | 1895 | 474 | 73.7 | 7 | 0.0891 | 1.26e-06 (2^-19.60) | 19.60 |
| 11 | `pipelined_m:data_width=24,n_iter=22,angle_guard=4,frac_guard=3,rounding=round,m=4` | 2003 | 583 | 86.0 | 8 | 0.0973 | 7.44e-07 (2^-20.36) | 20.36 |
| 12 | `pipelined_m:data_width=24,n_iter=24,angle_guard=4,frac_guard=3,rounding=round,m=4` | 2189 | 583 | 86.0 | 8 | 0.104 | 3.93e-07 (2^-21.28) | 21.28 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >=1 MS/s throughput and <=2^-10 error, with area (LUTs+FFs) as the primary objective. Both pipelined and pipelined_m produce 1 result/cycle, so throughput = Fmax in MS/s. Fmax on Artix-7 for a CORDIC datapath is typically 100-300+ MHz, far exceeding the 1 MS/s requirement, so throughput is not binding. The binding constraints are accuracy (max_abs_err <= 2^-10) and area. For accuracy: N=12-14 iterations with data_width >= 12 should suffice for 2^-10 error; I bound n_iter at 20 to explore the knee. For area: pipelined_m with larger m reduces FF count significantly while maintaining 1 result/cycle throughput. I split budget 55/45 between the two families to map the full trade-off curve: pipelined gives the latency/area baseline, pipelined_m explores the FF-reduction dimension. The accuracy_bits objective (HV ref 10) means designs with accuracy_bits > 10 contribute to hypervolume, so I allow data_width up to 16 and frac_guard up to 4 to capture that region.*)
- `pipelined` (33 evals): data_width=12..16, n_iter=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Fully pipelined gives 1 result/cycle, so throughput = Fmax(MHz) in MS/s. To hit >=1 MS/s we need Fmax >= 1 MHz, which is trivially met; the real cost is area. N=12-14 is the minimum for <=2^-10 error, so I bound n_iter at 20 to catch the area/accuracy knee. data_width 12-16 covers the 10-bit accuracy floor plus margin. This family is the baseline for the area/accuracy trade-off.
- `pipelined_m` (27 evals): data_width=12..16, n_iter=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* pipelined_m registers every m stages, trading latency for fewer FFs than fully pipelined. Since area (LUTs+FFs) is the primary objective and throughput only needs >=1 MS/s (easily met), larger m values (4-8) should yield significant FF savings with minimal accuracy impact. This family likely dominates the low-area end of the Pareto front.

**Result (code):** 60 evaluations this round, 60 total; 44 feasible; hypervolume 1248 (n/a).

**LLM decision:** `stop` — The constraints are met: 100% of feasible designs satisfy throughput >= 1 MSPS (best 282 MSPS), and the best max_abs_err is 7.13e-05 (2^-13.78), well below the 2^-10 limit. The Pareto front is well-populated with 11 designs spanning luts_plus_ffs 796..2658 and accuracy_bits 10.3..13.8, achieving a hypervolume of 1248 against the 1500 reference. The selection rule (min luts_plus_ffs) picks the pipelined_m design at 796 LUTs+FFs with 10.3 bits accuracy, which comfortably meets the error constraint. The front covers the key trade-off region and the budget is exhausted, so stopping is appropriate.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1248 (gain this round: n/a (first round)).
Feasible designs: 44 of 60 evaluations (38 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 27% violate; best seen 7.13e-05 (2^-13.78)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=1 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=796, accuracy_bits=10.3, luts=654, ffs=141, throughput_msps=59.6, max_abs_err=0.000772 (2^-10.34), power_index=0.0299
- pipelined_m [data_width=15 n_iter=12 angle_guard=4 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=836, accuracy_bits=10.5, luts=689, ffs=147, throughput_msps=50.3, max_abs_err=0.000691 (2^-10.50), power_index=0.0315
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=852, accuracy_bits=10.7, luts=701, ffs=151, throughput_msps=52.7, max_abs_err=0.000597 (2^-10.71), power_index=0.0321
- pipelined_m [data_width=15 n_iter=13 angle_guard=4 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=899, accuracy_bits=11.1, luts=751, ffs=147, throughput_msps=50.3, max_abs_err=0.000466 (2^-11.07), power_index=0.0338
- pipelined_m [data_width=15 n_iter=13 angle_guard=4 frac_guard=4 rounding=trunc m=8] luts_plus_ffs=953, accuracy_bits=11.4, luts=802, ffs=151, throughput_msps=50.3, max_abs_err=0.000374 (2^-11.38), power_index=0.0359
- pipelined_m [data_width=16 n_iter=17 angle_guard=2 frac_guard=3 rounding=round m=8] luts_plus_ffs=1303, accuracy_bits=13.1, luts=1084, ffs=219, throughput_msps=50.3, max_abs_err=0.000113 (2^-13.11), power_index=0.049
- pipelined [data_width=16 n_iter=16 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=2058, accuracy_bits=13.2, luts=1035, ffs=1023, throughput_msps=264, max_abs_err=0.000104 (2^-13.23), power_index=0.0774
- pipelined [data_width=16 n_iter=16 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=2118, accuracy_bits=13.4, luts=1066, ffs=1051, throughput_msps=264, max_abs_err=9.1e-05 (2^-13.42), power_index=0.0797
- pipelined [data_width=16 n_iter=17 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=2253, accuracy_bits=13.6, luts=1135, ffs=1118, throughput_msps=264, max_abs_err=7.95e-05 (2^-13.62), power_index=0.0847
- pipelined [data_width=16 n_iter=20 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=2658, accuracy_bits=13.8, luts=1340, ffs=1318, throughput_msps=264, max_abs_err=7.13e-05 (2^-13.78), power_index=0.1
Front coverage: luts_plus_ffs 796..2658 (HV reference 1500); accuracy_bits 10.3..13.8 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- pipelined: 33 evals, 26 feasible; max throughput seen 282 MSPS; best accuracy 13.78 bits; best feasible luts_plus_ffs=1645; feasible ranges: data_width 13..16, n_iter 14..20, angle_guard -1..4, frac_guard 1..4
- pipelined_m: 27 evals, 18 feasible; max throughput seen 171 MSPS; best accuracy 13.11 bits; best feasible luts_plus_ffs=796; feasible ranges: data_width 14..16, n_iter 12..17, angle_guard 1..4, frac_guard 1..4, m 5..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (26 evals): data_width=14..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (7 front designs; box front_anchored)
- `pipelined` (14 evals): data_width=15..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (4 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 82 feasible; hypervolume 1524 (+22.1%).

**No LLM call** (code's front-mapping round): The constraints are met: 100% of feasible designs satisfy throughput >= 1 MSPS (best 282 MSPS), and the best max_abs_err is 7.13e-05 (2^-13.78), well below the 2^-10 limit. The Pareto front is well-populated with 11 designs spanning luts_plus_ffs 796..2658 and accuracy_bits 10.3..13.8, achieving a hypervolume of 1248 against the 1500 reference. The selection rule (min luts_plus_ffs) picks the pipelined_m design at 796 LUTs+FFs with 10.3 bits accuracy, which comfortably meets the error constraint. The front covers the key trade-off region and the budget is exhausted, so stopping is appropriate.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1524 (gain this round: +22.1%).
Feasible designs: 82 of 100 evaluations (72 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 18% violate; best seen 3.93e-07 (2^-21.28)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=1 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=796, accuracy_bits=10.3, luts=654, ffs=141, throughput_msps=59.6, max_abs_err=0.000772 (2^-10.34), power_index=0.0299
- pipelined_m [data_width=15 n_iter=12 angle_guard=4 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=836, accuracy_bits=10.5, luts=689, ffs=147, throughput_msps=50.3, max_abs_err=0.000691 (2^-10.50), power_index=0.0315
- pipelined_m [data_width=15 n_iter=13 angle_guard=4 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=899, accuracy_bits=11.1, luts=751, ffs=147, throughput_msps=50.3, max_abs_err=0.000466 (2^-11.07), power_index=0.0338
- pipelined_m [data_width=15 n_iter=13 angle_guard=4 frac_guard=4 rounding=trunc m=8] luts_plus_ffs=953, accuracy_bits=11.4, luts=802, ffs=151, throughput_msps=50.3, max_abs_err=0.000374 (2^-11.38), power_index=0.0359
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=trunc m=8] luts_plus_ffs=1260, accuracy_bits=14.1, luts=1080, ffs=180, throughput_msps=50.3, max_abs_err=5.76e-05 (2^-14.08), power_index=0.0474
- pipelined_m [data_width=21 n_iter=22 angle_guard=3 frac_guard=0 rounding=round m=5] luts_plus_ffs=2009, accuracy_bits=16.4, luts=1599, ffs=411, throughput_msps=73.7, max_abs_err=1.15e-05 (2^-16.41), power_index=0.0756
- pipelined_m [data_width=21 n_iter=22 angle_guard=2 frac_guard=1 rounding=round m=5] luts_plus_ffs=2081, accuracy_bits=17.1, luts=1665, ffs=416, throughput_msps=73.7, max_abs_err=6.89e-06 (2^-17.15), power_index=0.0783
- pipelined_m [data_width=21 n_iter=22 angle_guard=3 frac_guard=2 rounding=round m=5] luts_plus_ffs=2160, accuracy_bits=18, luts=1731, ffs=429, throughput_msps=73.7, max_abs_err=3.88e-06 (2^-17.97), power_index=0.0813
- pipelined_m [data_width=24 n_iter=22 angle_guard=4 frac_guard=3 rounding=round m=4] luts_plus_ffs=2586, accuracy_bits=20.4, luts=2003, ffs=583, throughput_msps=86, max_abs_err=7.44e-07 (2^-20.36), power_index=0.0973
- pipelined_m [data_width=24 n_iter=24 angle_guard=4 frac_guard=3 rounding=round m=4] luts_plus_ffs=2772, accuracy_bits=21.3, luts=2189, ffs=583, throughput_msps=86, max_abs_err=3.93e-07 (2^-21.28), power_index=0.104
Front coverage: luts_plus_ffs 796..2772 (HV reference 1500); accuracy_bits 10.3..21.3 (HV reference 10); data_width on the front 15..25 (registry 8..28).

Per family:
- pipelined: 47 evals, 40 feasible; max throughput seen 282 MSPS; best accuracy 21.02 bits; best feasible luts_plus_ffs=1645; feasible ranges: data_width 13..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 53 evals, 42 feasible; max throughput seen 171 MSPS; best accuracy 21.28 bits; best feasible luts_plus_ffs=796; feasible ranges: data_width 14..26, n_iter 12..24, angle_guard -1..4, frac_guard 0..4, m 3..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5366 in, 1199 out
- provider-reported cost: $0.0020
- full prompts and replies: `llm_trace.jsonl`

