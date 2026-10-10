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
`pipelined_m:data_width=15,n_iter=12,angle_guard=4,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 643 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 200 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 53.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0317 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000807 (2^-10.27) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.61 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000238 (2^-12.04) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.95 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (17 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=12,angle_guard=4,frac_guard=0,rounding=round,m=4` | 643 | 200 | 93.6 | 5 | 0.0317 | 0.000807 (2^-10.27) | 10.27 |
| 1 | `pipelined_m:data_width=15,n_iter=13,angle_guard=1,frac_guard=0,rounding=round,m=4` | 663 | 244 | 97.8 | 6 | 0.0341 | 0.000673 (2^-10.54) | 10.54 |
| 2 | `pipelined_m:data_width=15,n_iter=13,angle_guard=3,frac_guard=3,rounding=trunc,m=8` | 764 | 147 | 52.7 | 4 | 0.0343 | 0.000439 (2^-11.15) | 11.15 |
| 3 | `pipelined_m:data_width=16,n_iter=13,angle_guard=2,frac_guard=0,rounding=round,m=4` | 713 | 262 | 97.8 | 6 | 0.0367 | 0.00041 (2^-11.25) | 11.25 |
| 4 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,m=4` | 772 | 262 | 97.8 | 6 | 0.0389 | 0.000294 (2^-11.73) | 11.73 |
| 5 | `pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=3` | 831 | 320 | 124.5 | 7 | 0.0433 | 0.000285 (2^-11.78) | 11.78 |
| 6 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=4,rounding=round,m=4` | 916 | 289 | 93.6 | 6 | 0.0453 | 0.000177 (2^-12.46) | 12.46 |
| 7 | `pipelined_m:data_width=22,n_iter=17,angle_guard=3,frac_guard=1,rounding=trunc,m=7` | 1303 | 278 | 54.3 | 5 | 0.0595 | 1.84e-05 (2^-15.73) | 15.73 |
| 8 | `pipelined_m:data_width=22,n_iter=17,angle_guard=3,frac_guard=3,rounding=trunc,m=7` | 1371 | 287 | 54.3 | 5 | 0.0623 | 1.65e-05 (2^-15.88) | 15.88 |
| 9 | `pipelined_m:data_width=22,n_iter=17,angle_guard=3,frac_guard=4,rounding=trunc,m=7` | 1405 | 291 | 54.3 | 5 | 0.0638 | 1.65e-05 (2^-15.89) | 15.89 |
| 10 | `pipelined_m:data_width=22,n_iter=20,angle_guard=0,frac_guard=4,rounding=trunc,m=7` | 1607 | 281 | 54.3 | 5 | 0.071 | 7.68e-06 (2^-16.99) | 16.99 |
| 11 | `pipelined_m:data_width=22,n_iter=24,angle_guard=4,frac_guard=1,rounding=trunc,m=7` | 1896 | 361 | 54.3 | 6 | 0.0849 | 6.11e-06 (2^-17.32) | 17.32 |
| 12 | `pipelined_m:data_width=22,n_iter=20,angle_guard=1,frac_guard=3,rounding=trunc,m=2` | 1587 | 845 | 158.3 | 12 | 0.0915 | 5.15e-06 (2^-17.57) | 17.57 |
| 13 | `pipelined_m:data_width=23,n_iter=20,angle_guard=0,frac_guard=4,rounding=trunc,m=2` | 1667 | 886 | 152.6 | 12 | 0.096 | 4.39e-06 (2^-17.80) | 17.80 |
| 14 | `pipelined_m:data_width=22,n_iter=26,angle_guard=3,frac_guard=4,rounding=trunc,m=7` | 2192 | 375 | 54.3 | 6 | 0.0966 | 1.95e-06 (2^-18.97) | 18.97 |
| 15 | `pipelined_m:data_width=26,n_iter=24,angle_guard=3,frac_guard=2,rounding=trunc,m=7` | 2211 | 420 | 52.0 | 6 | 0.0989 | 3.21e-07 (2^-21.57) | 21.57 |
| 16 | `pipelined_m:data_width=26,n_iter=23,angle_guard=4,frac_guard=4,rounding=trunc,m=7` | 2231 | 436 | 52.0 | 6 | 0.1 | 3.14e-07 (2^-21.60) | 21.60 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=1 MSPS throughput and max_abs_err <= 2^-10, with area (luts_plus_ffs) as the primary objective. Both pipelined and pipelined_m produce 1 result/cycle, so they can meet the throughput constraint at any reasonable Fmax. The accuracy constraint (<=2^-10) is met by N>=12 iterations with modest guard bits. I focus on N=12-16 and W=12-16 because: (1) N=12 already gives ~11.5 bits accuracy, comfortably meeting the constraint; (2) N=16 gives ~13.5 bits, improving the accuracy_bits objective for hypervolume; (3) W=12-16 keeps the datapath narrow for low area while the accuracy is dominated by N, not W. The key trade-off is between pipelined (more FFs, lower latency) and pipelined_m (fewer FFs, higher latency but latency is unconstrained). Since area is the primary objective and latency is not constrained, pipelined_m with m=2-4 should find the lowest-area designs. I split the budget 50/50 between the two families to map the trade-off curve: pipelined gives the low-latency end, pipelined_m gives the low-area end. The angle_guard and frac_guard ranges are kept moderate to explore how much guard bit overhead is needed for the accuracy target without wasting area.*)
- `pipelined` (30 evals): data_width=12..16, n_iter=12..16, angle_guard=-2..2, frac_guard=0..4, rounding=trunc|round. *Why:* Fully pipelined gives 1 result/cycle, easily meeting the >=1 MSPS constraint. N=12-16 is the sweet spot: N=12 gives ~11.5 bits accuracy (meets <=2^-10), N=16 gives ~13.5 bits (better accuracy_bits for HV). W=12-16 keeps area low while maintaining accuracy. angle_guard -2..2 and frac_guard 0..4 explore the accuracy/area trade-off. This is the primary family for the low-area corner.
- `pipelined_m` (30 evals): data_width=12..16, n_iter=12..16, angle_guard=-2..2, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* pipelined_m with m=2-4 registers every m stages, reducing FF count vs full pipelining while still achieving 1 result/cycle throughput. This should dominate pipelined on the luts_plus_ffs objective for the same accuracy, since fewer pipeline registers means fewer FFs. m=2-4 is a reasonable range: m=2 halves the registers, m=4 quarters them, at the cost of slightly higher latency (ceil(N/m)+2 cycles) which is not constrained. Same accuracy parameters as pipelined since accuracy depends only on data_width, n_iter, angle_guard, frac_guard, rounding.

**Result (code):** 60 evaluations this round, 60 total; 36 feasible; hypervolume 1135 (n/a).

**LLM decision:** `stop` — The current Pareto front is robust and satisfies all constraints. The minimum area design (pipelined_m, 907 LUTs+FFs) achieves 10.5 bits of accuracy (max_abs_err ~2^-10.54), which comfortably meets the spec requirement of max_abs_err <= 2^-10 (0.000976562). Throughput is also vastly above the 1 MSPS requirement (97.8 MSPS). Since this is the final round, we stop and select the design with the minimum luts_plus_ffs (907) as per the selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1135 (gain this round: n/a (first round)).
Feasible designs: 36 of 60 evaluations (31 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 40% violate; best seen 0.000177 (2^-12.46)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=13 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=907, accuracy_bits=10.5, luts=663, ffs=244, throughput_msps=97.8, max_abs_err=0.000673 (2^-10.54), power_index=0.0341
- pipelined_m [data_width=15 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=962, accuracy_bits=10.6, luts=718, ffs=244, throughput_msps=97.8, max_abs_err=0.000632 (2^-10.63), power_index=0.0362
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=976, accuracy_bits=11.3, luts=713, ffs=262, throughput_msps=97.8, max_abs_err=0.00041 (2^-11.25), power_index=0.0367
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1035, accuracy_bits=11.7, luts=772, ffs=262, throughput_msps=97.8, max_abs_err=0.000294 (2^-11.73), power_index=0.0389
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1151, accuracy_bits=11.8, luts=831, ffs=320, throughput_msps=124, max_abs_err=0.000285 (2^-11.78), power_index=0.0433
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=4 rounding=round m=4] luts_plus_ffs=1204, accuracy_bits=12.5, luts=916, ffs=289, throughput_msps=93.6, max_abs_err=0.000177 (2^-12.46), power_index=0.0453
Front coverage: luts_plus_ffs 907..1204 (HV reference 1500); accuracy_bits 10.5..12.5 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- pipelined: 30 evals, 17 feasible; max throughput seen 282 MSPS; best accuracy 11.57 bits; best feasible luts_plus_ffs=1346; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard -1..0, frac_guard 1..4
- pipelined_m: 30 evals, 19 feasible; max throughput seen 171 MSPS; best accuracy 12.46 bits; best feasible luts_plus_ffs=907; feasible ranges: data_width 15..16, n_iter 13..16, angle_guard 1..2, frac_guard 0..4, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (6 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 74 feasible; hypervolume 1192 (+4.9%).

**No LLM call** (code's front-mapping round): The current Pareto front is robust and satisfies all constraints. The minimum area design (pipelined_m, 907 LUTs+FFs) achieves 10.5 bits of accuracy (max_abs_err ~2^-10.54), which comfortably meets the spec requirement of max_abs_err <= 2^-10 (0.000976562). Throughput is also vastly above the 1 MSPS requirement (97.8 MSPS). Since this is the final round, we stop and select the design with the minimum luts_plus_ffs (907) as per the selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1192 (gain this round: +4.9%).
Feasible designs: 74 of 100 evaluations (67 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 26% violate; best seen 3.14e-07 (2^-21.60)

Pareto front (feasible, 17 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=4 frac_guard=0 rounding=round m=4] luts_plus_ffs=843, accuracy_bits=10.3, luts=643, ffs=200, throughput_msps=93.6, max_abs_err=0.000807 (2^-10.27), power_index=0.0317
- pipelined_m [data_width=15 n_iter=13 angle_guard=3 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=911, accuracy_bits=11.2, luts=764, ffs=147, throughput_msps=52.7, max_abs_err=0.000439 (2^-11.15), power_index=0.0343
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1035, accuracy_bits=11.7, luts=772, ffs=262, throughput_msps=97.8, max_abs_err=0.000294 (2^-11.73), power_index=0.0389
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1151, accuracy_bits=11.8, luts=831, ffs=320, throughput_msps=124, max_abs_err=0.000285 (2^-11.78), power_index=0.0433
- pipelined_m [data_width=22 n_iter=17 angle_guard=3 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=1582, accuracy_bits=15.7, luts=1303, ffs=278, throughput_msps=54.3, max_abs_err=1.84e-05 (2^-15.73), power_index=0.0595
- pipelined_m [data_width=22 n_iter=17 angle_guard=3 frac_guard=4 rounding=trunc m=7] luts_plus_ffs=1695, accuracy_bits=15.9, luts=1405, ffs=291, throughput_msps=54.3, max_abs_err=1.65e-05 (2^-15.89), power_index=0.0638
- pipelined_m [data_width=22 n_iter=24 angle_guard=4 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=2257, accuracy_bits=17.3, luts=1896, ffs=361, throughput_msps=54.3, max_abs_err=6.11e-06 (2^-17.32), power_index=0.0849
- pipelined_m [data_width=22 n_iter=20 angle_guard=1 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=2432, accuracy_bits=17.6, luts=1587, ffs=845, throughput_msps=158, max_abs_err=5.15e-06 (2^-17.57), power_index=0.0915
- pipelined_m [data_width=22 n_iter=26 angle_guard=3 frac_guard=4 rounding=trunc m=7] luts_plus_ffs=2567, accuracy_bits=19, luts=2192, ffs=375, throughput_msps=54.3, max_abs_err=1.95e-06 (2^-18.97), power_index=0.0966
- pipelined_m [data_width=26 n_iter=23 angle_guard=4 frac_guard=4 rounding=trunc m=7] luts_plus_ffs=2667, accuracy_bits=21.6, luts=2231, ffs=436, throughput_msps=52, max_abs_err=3.14e-07 (2^-21.60), power_index=0.1
Front coverage: luts_plus_ffs 843..2667 (HV reference 1500); accuracy_bits 10.3..21.6 (HV reference 10); data_width on the front 15..26 (registry 8..28).

Per family:
- pipelined: 30 evals, 17 feasible; max throughput seen 282 MSPS; best accuracy 11.57 bits; best feasible luts_plus_ffs=1346; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard -1..0, frac_guard 1..4
- pipelined_m: 70 evals, 57 feasible; max throughput seen 171 MSPS; best accuracy 21.60 bits; best feasible luts_plus_ffs=843; feasible ranges: data_width 15..26, n_iter 11..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4241 in, 1249 out
- provider-reported cost: $0.0018
- full prompts and replies: `llm_trace.jsonl`

