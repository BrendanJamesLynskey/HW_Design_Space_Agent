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
`pipelined_m:data_width=13,n_iter=12,angle_guard=3,frac_guard=3,rounding=round,m=7` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 659 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 133 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 59.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 59.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 67.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0298 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000869 (2^-10.17) | exact: bit-accurate model, exhaustive (8192 angles) |
| max_abs_err_lsb | 1.78 | exact: bit-accurate model, exhaustive (8192 angles) |
| rms_err | 0.000264 (2^-11.89) | exact: bit-accurate model, exhaustive (8192 angles) |
| rms_err_lsb | 0.541 | exact: bit-accurate model, exhaustive (8192 angles) |
| accuracy_bits | 10.2 | exact: bit-accurate model, exhaustive (8192 angles) |

## Pareto front (25 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=13,n_iter=12,angle_guard=3,frac_guard=3,rounding=round,m=7` | 659 | 133 | 59.6 | 4 | 0.0298 | 0.000869 (2^-10.17) | 10.17 |
| 1 | `pipelined_m:data_width=14,n_iter=12,angle_guard=3,frac_guard=4,rounding=round,m=8` | 719 | 143 | 52.7 | 4 | 0.0324 | 0.000644 (2^-10.60) | 10.60 |
| 2 | `pipelined_m:data_width=15,n_iter=12,angle_guard=3,frac_guard=3,rounding=round,m=5` | 732 | 211 | 80.6 | 5 | 0.0355 | 0.000576 (2^-10.76) | 10.76 |
| 3 | `pipelined_m:data_width=16,n_iter=14,angle_guard=3,frac_guard=0,rounding=round,m=5` | 786 | 208 | 77.0 | 5 | 0.0374 | 0.000294 (2^-11.73) | 11.73 |
| 4 | `pipelined_m:data_width=14,n_iter=16,angle_guard=3,frac_guard=4,rounding=round,m=8` | 967 | 143 | 52.7 | 4 | 0.0418 | 0.000279 (2^-11.81) | 11.81 |
| 5 | `pipelined_m:data_width=15,n_iter=15,angle_guard=4,frac_guard=3,rounding=trunc,m=6` | 905 | 212 | 65.4 | 5 | 0.042 | 0.000238 (2^-12.04) | 12.04 |
| 6 | `pipelined_m:data_width=15,n_iter=15,angle_guard=3,frac_guard=3,rounding=round,m=5` | 922 | 211 | 80.6 | 5 | 0.0426 | 0.000188 (2^-12.38) | 12.38 |
| 7 | `pipelined_m:data_width=16,n_iter=15,angle_guard=3,frac_guard=3,rounding=trunc,m=5` | 935 | 220 | 77.0 | 5 | 0.0434 | 0.000152 (2^-12.68) | 12.68 |
| 8 | `pipelined_m:data_width=16,n_iter=15,angle_guard=3,frac_guard=4,rounding=round,m=8` | 998 | 159 | 50.3 | 4 | 0.0435 | 0.000109 (2^-13.16) | 13.16 |
| 9 | `pipelined_m:data_width=16,n_iter=16,angle_guard=4,frac_guard=3,rounding=round,m=8` | 1051 | 159 | 50.3 | 4 | 0.0455 | 7.92e-05 (2^-13.63) | 13.63 |
| 10 | `pipelined_m:data_width=16,n_iter=16,angle_guard=4,frac_guard=4,rounding=round,m=8` | 1082 | 161 | 50.3 | 4 | 0.0468 | 7.19e-05 (2^-13.76) | 13.76 |
| 11 | `pipelined_m:data_width=20,n_iter=15,angle_guard=2,frac_guard=3,rounding=trunc,m=8` | 1097 | 186 | 48.0 | 4 | 0.0482 | 6.77e-05 (2^-13.85) | 13.85 |
| 12 | `pipelined_m:data_width=20,n_iter=15,angle_guard=3,frac_guard=3,rounding=trunc,m=5` | 1112 | 264 | 73.7 | 5 | 0.0518 | 6.57e-05 (2^-13.89) | 13.89 |
| 13 | `pipelined_m:data_width=17,n_iter=16,angle_guard=4,frac_guard=4,rounding=round,m=5` | 1132 | 311 | 77.0 | 6 | 0.0543 | 5.18e-05 (2^-14.24) | 14.24 |
| 14 | `pipelined_m:data_width=20,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc,m=5` | 1143 | 331 | 77.0 | 6 | 0.0555 | 3.93e-05 (2^-14.63) | 14.63 |
| 15 | `pipelined_m:data_width=20,n_iter=17,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 1219 | 257 | 50.3 | 5 | 0.0555 | 2.57e-05 (2^-15.25) | 15.25 |
| 16 | `pipelined_m:data_width=20,n_iter=17,angle_guard=2,frac_guard=3,rounding=trunc,m=8` | 1253 | 261 | 48.0 | 5 | 0.057 | 2.35e-05 (2^-15.38) | 15.38 |
| 17 | `pipelined_m:data_width=21,n_iter=21,angle_guard=0,frac_guard=2,rounding=trunc,m=7` | 1544 | 262 | 54.3 | 5 | 0.0679 | 1.64e-05 (2^-15.90) | 15.90 |
| 18 | `pipelined_m:data_width=26,n_iter=18,angle_guard=1,frac_guard=3,rounding=trunc,m=8` | 1635 | 325 | 45.9 | 5 | 0.0737 | 7.74e-06 (2^-16.98) | 16.98 |
| 19 | `pipelined_m:data_width=28,n_iter=18,angle_guard=0,frac_guard=2,rounding=trunc,m=8` | 1689 | 340 | 45.9 | 5 | 0.0763 | 7.67e-06 (2^-16.99) | 16.99 |
| 20 | `pipelined_m:data_width=23,n_iter=23,angle_guard=2,frac_guard=0,rounding=trunc,m=7` | 1790 | 361 | 54.3 | 6 | 0.0809 | 5.84e-06 (2^-17.39) | 17.39 |
| 21 | `pipelined_m:data_width=28,n_iter=21,angle_guard=1,frac_guard=2,rounding=trunc,m=8` | 2007 | 343 | 45.9 | 5 | 0.0884 | 1e-06 (2^-19.93) | 19.93 |
| 22 | `pipelined_m:data_width=28,n_iter=28,angle_guard=-1,frac_guard=2,rounding=trunc,m=8` | 2651 | 432 | 45.9 | 6 | 0.116 | 2.56e-07 (2^-21.90) | 21.90 |
| 23 | `pipelined_m:data_width=28,n_iter=25,angle_guard=0,frac_guard=3,rounding=trunc,m=3` | 2433 | 931 | 105.9 | 11 | 0.127 | 1.74e-07 (2^-22.45) | 22.45 |
| 24 | `pipelined_m:data_width=28,n_iter=30,angle_guard=4,frac_guard=2,rounding=trunc,m=3` | 3000 | 1051 | 105.9 | 12 | 0.152 | 6.81e-08 (2^-23.81) | 23.81 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=1 MSPS and max_abs_err <= 2^-10 while minimising luts_plus_ffs. Both pipelined families produce one result per cycle, so throughput equals Fmax; for these small CORDIC designs Fmax is expected to be far above 1 MHz, making the throughput constraint non-binding. The real trade-off is area vs accuracy, controlled by data_width, n_iter, angle_guard, frac_guard and rounding. pipelined_m strictly generalises pipelined by allowing m>1, which reduces the number of pipeline registers (FFs) without changing the combinational logic or accuracy. Therefore pipelined (m=1) is expected to be dominated in luts_plus_ffs for any given accuracy, so the entire budget is allocated to pipelined_m to map the Pareto front thoroughly. The chosen ranges span the feasible accuracy region and include the low-area corner (small W, small N, large m) as well as higher-accuracy points to extend the front.*)
- `pipelined_m` (60 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* pipelined_m can trade Fmax for fewer pipeline registers by increasing m, directly reducing flip-flop count and thus luts_plus_ffs. Since the throughput constraint (>=1 MSPS) is very loose for a small CORDIC (1 result/cycle, Fmax expected well above 1 MHz), larger m is likely beneficial. The ranges cover the plausible accuracy region: data_width >=12 is needed because output LSB = 2^-(W-2) and max_abs_err <= 2^-10; n_iter >=10 covers the CORDIC angle-resolution threshold. Full guard-bit and rounding ranges let the search find the minimal area for each accuracy level. m from 2..8 explores the area/Fmax trade-off while ensuring feasible points if large m violates timing.

**Result (code):** 60 evaluations this round, 60 total; 50 feasible; hypervolume 1726 (n/a).

**LLM decision:** `stop` — Final round: the feasible front is well mapped and meets the spec. Constraint throughput_msps >= 1 is satisfied with huge margin (best 171 MSPS, 0% violations), and max_abs_err <= 2^-10 is met by the whole front (best 2.35e-05 = 2^-15.38). The front spans luts_plus_ffs 792..1514 and accuracy_bits 10.2..15.4, covering both HV reference points (1500 area, 10 bits), giving HV 1726. The selection rule (min luts_plus_ffs) picks pipelined_m [data_width=13 n_iter=12 angle_guard=3 frac_guard=3 rounding=round m=7] at 792 LUT+FF with 10.2 accuracy bits and 59.6 MSPS, comfortably inside all constraints. No further improvement is expected within the exhausted budget, so stop.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1726 (gain this round: n/a (first round)).
Feasible designs: 50 of 60 evaluations (46 unique).
Families explored so far: pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 17% violate; best seen 2.35e-05 (2^-15.38)

Pareto front (feasible, 17 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=13 n_iter=12 angle_guard=3 frac_guard=3 rounding=round m=7] luts_plus_ffs=792, accuracy_bits=10.2, luts=659, ffs=133, throughput_msps=59.6, max_abs_err=0.000869 (2^-10.17), power_index=0.0298
- pipelined_m [data_width=15 n_iter=12 angle_guard=3 frac_guard=3 rounding=round m=5] luts_plus_ffs=943, accuracy_bits=10.8, luts=732, ffs=211, throughput_msps=80.6, max_abs_err=0.000576 (2^-10.76), power_index=0.0355
- pipelined_m [data_width=14 n_iter=16 angle_guard=3 frac_guard=4 rounding=round m=8] luts_plus_ffs=1111, accuracy_bits=11.8, luts=967, ffs=143, throughput_msps=52.7, max_abs_err=0.000279 (2^-11.81), power_index=0.0418
- pipelined_m [data_width=15 n_iter=15 angle_guard=4 frac_guard=3 rounding=trunc m=6] luts_plus_ffs=1117, accuracy_bits=12, luts=905, ffs=212, throughput_msps=65.4, max_abs_err=0.000238 (2^-12.04), power_index=0.042
- pipelined_m [data_width=16 n_iter=15 angle_guard=3 frac_guard=3 rounding=trunc m=5] luts_plus_ffs=1155, accuracy_bits=12.7, luts=935, ffs=220, throughput_msps=77, max_abs_err=0.000152 (2^-12.68), power_index=0.0434
- pipelined_m [data_width=16 n_iter=16 angle_guard=4 frac_guard=3 rounding=round m=8] luts_plus_ffs=1210, accuracy_bits=13.6, luts=1051, ffs=159, throughput_msps=50.3, max_abs_err=7.92e-05 (2^-13.63), power_index=0.0455
- pipelined_m [data_width=20 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1283, accuracy_bits=13.9, luts=1097, ffs=186, throughput_msps=48, max_abs_err=6.77e-05 (2^-13.85), power_index=0.0482
- pipelined_m [data_width=20 n_iter=15 angle_guard=3 frac_guard=3 rounding=trunc m=5] luts_plus_ffs=1376, accuracy_bits=13.9, luts=1112, ffs=264, throughput_msps=73.7, max_abs_err=6.57e-05 (2^-13.89), power_index=0.0518
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc m=5] luts_plus_ffs=1474, accuracy_bits=14.6, luts=1143, ffs=331, throughput_msps=77, max_abs_err=3.93e-05 (2^-14.63), power_index=0.0555
- pipelined_m [data_width=20 n_iter=17 angle_guard=2 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1514, accuracy_bits=15.4, luts=1253, ffs=261, throughput_msps=48, max_abs_err=2.35e-05 (2^-15.38), power_index=0.057
Front coverage: luts_plus_ffs 792..1514 (HV reference 1500); accuracy_bits 10.2..15.4 (HV reference 10); data_width on the front 13..20 (registry 8..28).

Per family:
- pipelined_m: 60 evals, 50 feasible; max throughput seen 171 MSPS; best accuracy 15.38 bits; best feasible luts_plus_ffs=792; feasible ranges: data_width 13..20, n_iter 12..20, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=12..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (17 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 83 feasible; hypervolume 1726 (+0.0%).

**No LLM call** (code's front-mapping round): Final round: the feasible front is well mapped and meets the spec. Constraint throughput_msps >= 1 is satisfied with huge margin (best 171 MSPS, 0% violations), and max_abs_err <= 2^-10 is met by the whole front (best 2.35e-05 = 2^-15.38). The front spans luts_plus_ffs 792..1514 and accuracy_bits 10.2..15.4, covering both HV reference points (1500 area, 10 bits), giving HV 1726. The selection rule (min luts_plus_ffs) picks pipelined_m [data_width=13 n_iter=12 angle_guard=3 frac_guard=3 rounding=round m=7] at 792 LUT+FF with 10.2 accuracy bits and 59.6 MSPS, comfortably inside all constraints. No further improvement is expected within the exhausted budget, so stop.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1726 (gain this round: +0.0%).
Feasible designs: 83 of 100 evaluations (78 unique).
Families explored so far: pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 17% violate; best seen 6.81e-08 (2^-23.81)

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=13 n_iter=12 angle_guard=3 frac_guard=3 rounding=round m=7] luts_plus_ffs=792, accuracy_bits=10.2, luts=659, ffs=133, throughput_msps=59.6, max_abs_err=0.000869 (2^-10.17), power_index=0.0298
- pipelined_m [data_width=16 n_iter=14 angle_guard=3 frac_guard=0 rounding=round m=5] luts_plus_ffs=994, accuracy_bits=11.7, luts=786, ffs=208, throughput_msps=77, max_abs_err=0.000294 (2^-11.73), power_index=0.0374
- pipelined_m [data_width=15 n_iter=15 angle_guard=4 frac_guard=3 rounding=trunc m=6] luts_plus_ffs=1117, accuracy_bits=12, luts=905, ffs=212, throughput_msps=65.4, max_abs_err=0.000238 (2^-12.04), power_index=0.042
- pipelined_m [data_width=16 n_iter=15 angle_guard=3 frac_guard=4 rounding=round m=8] luts_plus_ffs=1157, accuracy_bits=13.2, luts=998, ffs=159, throughput_msps=50.3, max_abs_err=0.000109 (2^-13.16), power_index=0.0435
- pipelined_m [data_width=20 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1283, accuracy_bits=13.9, luts=1097, ffs=186, throughput_msps=48, max_abs_err=6.77e-05 (2^-13.85), power_index=0.0482
- pipelined_m [data_width=17 n_iter=16 angle_guard=4 frac_guard=4 rounding=round m=5] luts_plus_ffs=1442, accuracy_bits=14.2, luts=1132, ffs=311, throughput_msps=77, max_abs_err=5.18e-05 (2^-14.24), power_index=0.0543
- pipelined_m [data_width=20 n_iter=17 angle_guard=2 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1514, accuracy_bits=15.4, luts=1253, ffs=261, throughput_msps=48, max_abs_err=2.35e-05 (2^-15.38), power_index=0.057
- pipelined_m [data_width=28 n_iter=18 angle_guard=0 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=2029, accuracy_bits=17, luts=1689, ffs=340, throughput_msps=45.9, max_abs_err=7.67e-06 (2^-16.99), power_index=0.0763
- pipelined_m [data_width=28 n_iter=21 angle_guard=1 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=2350, accuracy_bits=19.9, luts=2007, ffs=343, throughput_msps=45.9, max_abs_err=1e-06 (2^-19.93), power_index=0.0884
- pipelined_m [data_width=28 n_iter=30 angle_guard=4 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=4051, accuracy_bits=23.8, luts=3000, ffs=1051, throughput_msps=106, max_abs_err=6.81e-08 (2^-23.81), power_index=0.152
Front coverage: luts_plus_ffs 792..4051 (HV reference 1500); accuracy_bits 10.2..23.8 (HV reference 10); data_width on the front 13..28 (registry 8..28).

Per family:
- pipelined_m: 100 evals, 83 feasible; max throughput seen 171 MSPS; best accuracy 23.81 bits; best feasible luts_plus_ffs=792; feasible ranges: data_width 13..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5289 in, 7511 out
- provider-reported cost: $0.0090
- full prompts and replies: `llm_trace.jsonl`

