# DSE run: asic_low_area

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_low_area: Motor-control sin/cos in sky130 standard cells: >= 1 MSPS, max error <= 2^-10. Area is everything: minimise cell area.
  target: asic-sky130hd
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min area_um2 (HV ref 40000)
  objective: max accuracy_bits (HV ref 10)
  select: min area_um2
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=16,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc,m=8` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 21800 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 5808 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 147 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 21.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 21.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 188 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.021 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000378 (2^-11.37) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 6.19 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000108 (2^-13.18) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 1.77 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 11.4 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (20 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 21800 | 147 | 21.3 | 4 | 0.021 | 0.000378 (2^-11.37) | 11.37 |
| 1 | `pipelined_m:data_width=17,n_iter=13,angle_guard=3,frac_guard=0,rounding=round,m=4` | 24594 | 273 | 37.9 | 6 | 0.0297 | 0.000314 (2^-11.64) | 11.64 |
| 2 | `pipelined_m:data_width=16,n_iter=13,angle_guard=2,frac_guard=2,rounding=round,m=3` | 26656 | 329 | 54.3 | 7 | 0.034 | 0.00031 (2^-11.65) | 11.65 |
| 3 | `pipelined_m:data_width=23,n_iter=13,angle_guard=2,frac_guard=0,rounding=round,m=7` | 28148 | 199 | 18.1 | 4 | 0.0276 | 0.000244 (2^-12.00) | 12.00 |
| 4 | `pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,m=2` | 29636 | 446 | 75.4 | 9 | 0.0423 | 0.000194 (2^-12.33) | 12.33 |
| 5 | `pipelined_m:data_width=18,n_iter=18,angle_guard=0,frac_guard=1,rounding=trunc,m=6` | 31929 | 219 | 26.8 | 5 | 0.031 | 0.000122 (2^-13.01) | 13.01 |
| 6 | `pipelined_m:data_width=17,n_iter=16,angle_guard=2,frac_guard=4,rounding=round,m=4` | 33226 | 295 | 36.3 | 6 | 0.036 | 7.74e-05 (2^-13.66) | 13.66 |
| 7 | `pipelined_m:data_width=20,n_iter=16,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 33516 | 313 | 36.3 | 6 | 0.0371 | 4.71e-05 (2^-14.37) | 14.37 |
| 8 | `pipelined_m:data_width=20,n_iter=16,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 34458 | 321 | 33.5 | 6 | 0.0381 | 4.27e-05 (2^-14.51) | 14.51 |
| 9 | `pipelined_m:data_width=23,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc,m=7` | 34856 | 269 | 19.5 | 5 | 0.0355 | 3.32e-05 (2^-14.88) | 14.88 |
| 10 | `pipelined_m:data_width=23,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc,m=5` | 37412 | 350 | 26.0 | 6 | 0.0415 | 3.23e-05 (2^-14.92) | 14.92 |
| 11 | `pipelined_m:data_width=23,n_iter=18,angle_guard=0,frac_guard=1,rounding=round,m=8` | 40864 | 275 | 16.5 | 5 | 0.0394 | 9.76e-06 (2^-16.64) | 16.64 |
| 12 | `pipelined_m:data_width=23,n_iter=19,angle_guard=2,frac_guard=0,rounding=round,m=7` | 41657 | 275 | 18.1 | 5 | 0.0399 | 6.01e-06 (2^-17.34) | 17.34 |
| 13 | `pipelined_m:data_width=23,n_iter=19,angle_guard=2,frac_guard=1,rounding=trunc,m=5` | 44410 | 358 | 25.1 | 6 | 0.0461 | 5.7e-06 (2^-17.42) | 17.42 |
| 14 | `pipelined_m:data_width=23,n_iter=23,angle_guard=2,frac_guard=0,rounding=round,m=7` | 51230 | 352 | 18.1 | 6 | 0.0498 | 2.9e-06 (2^-18.39) | 18.39 |
| 15 | `pipelined_m:data_width=23,n_iter=22,angle_guard=2,frac_guard=3,rounding=trunc,m=7` | 52874 | 370 | 17.5 | 6 | 0.0517 | 1.77e-06 (2^-19.11) | 19.11 |
| 16 | `pipelined_m:data_width=27,n_iter=22,angle_guard=3,frac_guard=0,rounding=round,m=7` | 57548 | 411 | 15.3 | 6 | 0.0568 | 6.06e-07 (2^-20.65) | 20.65 |
| 17 | `pipelined_m:data_width=27,n_iter=22,angle_guard=3,frac_guard=1,rounding=round,m=3` | 68294 | 785 | 34.9 | 10 | 0.0839 | 5.44e-07 (2^-20.81) | 20.81 |
| 18 | `pipelined_m:data_width=27,n_iter=29,angle_guard=0,frac_guard=1,rounding=round,m=7` | 76188 | 495 | 16.3 | 7 | 0.0725 | 2.97e-07 (2^-21.68) | 21.68 |
| 19 | `pipelined_m:data_width=27,n_iter=29,angle_guard=3,frac_guard=1,rounding=round,m=7` | 78662 | 510 | 15.3 | 7 | 0.0747 | 1.16e-07 (2^-23.04) | 23.04 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-minimisation subject to throughput >= 1 MSPS and max_abs_err <= 2^-10. Both allowed families emit 1 result/cycle, so throughput = Fmax and the throughput constraint reduces to Fmax >= 1 MHz, which is trivially met for any sane CORDIC depth; the real trade-off is area vs accuracy. Accuracy depends only on data_width, n_iter, angle_guard, frac_guard, rounding, so I bound n_iter to 10..16 (enough to reach ~2^-10 with modest guards, but not so high that area balloons) and data_width to 12..20 (wide enough for the error budget, narrow enough to keep area low). I keep both rounding modes and the full guard ranges so Optuna can find the cheapest guard/rounding combination that clears 2^-10. I split budget 55/45 between pipelined (the clean area-vs-accuracy curve) and pipelined_m (which should push the area end lower via fewer registers). I deliberately avoid very low n_iter (would fail accuracy) and very high data_width (pure area waste), focusing the 100-eval budget on the region where the Pareto front actually lives.*)
- `pipelined` (33 evals): data_width=12..20, n_iter=10..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Full pipelining gives 1 result/cycle, so throughput = Fmax; with N=10..16 the combinational depth is modest and Fmax should comfortably clear 1 MSPS. Accuracy is set by n_iter/guards, so this family lets me trade area (fewer stages, narrower W) against accuracy_bits directly. This is the primary area-vs-accuracy trade-off curve for the spec.
- `pipelined_m` (27 evals): data_width=12..20, n_iter=10..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* Registering every m stages cuts FF count (and area) versus full pipelining while still delivering 1 result/cycle, so it can dominate on area at equal accuracy. m=2..4 keeps the combinational block small enough to hold Fmax >= 1 MSPS. This maps the area side of the front that pipelined alone would overpay for in registers.

**Result (code):** 60 evaluations this round, 60 total; 46 feasible; hypervolume 4.755e+04 (n/a).

**LLM decision:** `stop` — The Pareto front is well-established with 9 feasible designs spanning area 22208-42881 um^2 and accuracy 10.2-14.8 bits. The minimum area design (pipelined_m, data_width=17, n_iter=12, m=4) achieves 22208 um^2 with 10.2 bits accuracy, comfortably meeting the max_abs_err <= 2^-10 constraint (0.000861 < 0.000977) and throughput >= 1 MSPS (39.6 MSPS). The front covers the full trade-off curve from the area-optimal corner to high-accuracy designs, and the hypervolume of 4.755e+04 indicates good coverage relative to the reference point. Since this is the final round, the current front is sufficient for selection: the min-area design at 22208 um^2 is the clear winner under the spec's selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 4.755e+04 (gain this round: n/a (first round)).
Feasible designs: 46 of 60 evaluations (38 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 163
- max_abs_err <= 0.000976562: 23% violate; best seen 3.51e-05 (2^-14.80)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=17 n_iter=12 angle_guard=-2 frac_guard=2 rounding=round m=4] area_um2=22208, accuracy_bits=10.2, ffs=208, throughput_msps=39.6, max_abs_err=0.000861 (2^-10.18), power_index=0.0247
- pipelined_m [data_width=14 n_iter=13 angle_guard=2 frac_guard=4 rounding=round m=4] area_um2=24260, accuracy_bits=11, ffs=254, throughput_msps=41.5, max_abs_err=0.000496 (2^-10.98), power_index=0.0284
- pipelined_m [data_width=17 n_iter=13 angle_guard=3 frac_guard=0 rounding=round m=4] area_um2=24594, accuracy_bits=11.6, ffs=273, throughput_msps=37.9, max_abs_err=0.000314 (2^-11.64), power_index=0.0297
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=0 rounding=trunc m=4] area_um2=28723, accuracy_bits=11.7, ffs=269, throughput_msps=39.6, max_abs_err=0.000307 (2^-11.67), power_index=0.0319
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=2] area_um2=29636, accuracy_bits=12.3, ffs=446, throughput_msps=75.4, max_abs_err=0.000194 (2^-12.33), power_index=0.0423
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=4 rounding=round m=4] area_um2=33226, accuracy_bits=13.7, ffs=295, throughput_msps=36.3, max_abs_err=7.74e-05 (2^-13.66), power_index=0.036
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc m=4] area_um2=33516, accuracy_bits=14.4, ffs=313, throughput_msps=36.3, max_abs_err=4.71e-05 (2^-14.37), power_index=0.0371
- pipelined_m [data_width=20 n_iter=16 angle_guard=3 frac_guard=1 rounding=trunc m=4] area_um2=34458, accuracy_bits=14.5, ffs=321, throughput_msps=33.5, max_abs_err=4.27e-05 (2^-14.51), power_index=0.0381
- pipelined_m [data_width=20 n_iter=16 angle_guard=3 frac_guard=2 rounding=round m=2] area_um2=42881, accuracy_bits=14.8, ffs=619, throughput_msps=64.3, max_abs_err=3.51e-05 (2^-14.80), power_index=0.0597
Front coverage: area_um2 22208..42881 (HV reference 40000); accuracy_bits 10.2..14.8 (HV reference 10); data_width on the front 14..20 (registry 8..28).

Per family:
- pipelined: 33 evals, 27 feasible; max throughput seen 163 MSPS; best accuracy 13.92 bits; best feasible area_um2=36227; feasible ranges: data_width 13..20, n_iter 12..16, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 27 evals, 19 feasible; max throughput seen 86.6 MSPS; best accuracy 14.80 bits; best feasible area_um2=22208; feasible ranges: data_width 14..20, n_iter 12..16, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (9 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 81 feasible; hypervolume 5.406e+04 (+13.7%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established with 9 feasible designs spanning area 22208-42881 um^2 and accuracy 10.2-14.8 bits. The minimum area design (pipelined_m, data_width=17, n_iter=12, m=4) achieves 22208 um^2 with 10.2 bits accuracy, comfortably meeting the max_abs_err <= 2^-10 constraint (0.000861 < 0.000977) and throughput >= 1 MSPS (39.6 MSPS). The front covers the full trade-off curve from the area-optimal corner to high-accuracy designs, and the hypervolume of 4.755e+04 indicates good coverage relative to the reference point. Since this is the final round, the current front is sufficient for selection: the min-area design at 22208 um^2 is the clear winner under the spec's selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 5.406e+04 (gain this round: +13.7%).
Feasible designs: 81 of 100 evaluations (72 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 163
- max_abs_err <= 0.000976562: 19% violate; best seen 1.16e-07 (2^-23.04)

Pareto front (feasible, 20 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc m=8] area_um2=21800, accuracy_bits=11.4, ffs=147, throughput_msps=21.3, max_abs_err=0.000378 (2^-11.37), power_index=0.021
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=round m=3] area_um2=26656, accuracy_bits=11.7, ffs=329, throughput_msps=54.3, max_abs_err=0.00031 (2^-11.65), power_index=0.034
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=2] area_um2=29636, accuracy_bits=12.3, ffs=446, throughput_msps=75.4, max_abs_err=0.000194 (2^-12.33), power_index=0.0423
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=4 rounding=round m=4] area_um2=33226, accuracy_bits=13.7, ffs=295, throughput_msps=36.3, max_abs_err=7.74e-05 (2^-13.66), power_index=0.036
- pipelined_m [data_width=20 n_iter=16 angle_guard=3 frac_guard=1 rounding=trunc m=4] area_um2=34458, accuracy_bits=14.5, ffs=321, throughput_msps=33.5, max_abs_err=4.27e-05 (2^-14.51), power_index=0.0381
- pipelined_m [data_width=23 n_iter=18 angle_guard=0 frac_guard=1 rounding=round m=8] area_um2=40864, accuracy_bits=16.6, ffs=275, throughput_msps=16.5, max_abs_err=9.76e-06 (2^-16.64), power_index=0.0394
- pipelined_m [data_width=23 n_iter=19 angle_guard=2 frac_guard=1 rounding=trunc m=5] area_um2=44410, accuracy_bits=17.4, ffs=358, throughput_msps=25.1, max_abs_err=5.7e-06 (2^-17.42), power_index=0.0461
- pipelined_m [data_width=23 n_iter=22 angle_guard=2 frac_guard=3 rounding=trunc m=7] area_um2=52874, accuracy_bits=19.1, ffs=370, throughput_msps=17.5, max_abs_err=1.77e-06 (2^-19.11), power_index=0.0517
- pipelined_m [data_width=27 n_iter=22 angle_guard=3 frac_guard=1 rounding=round m=3] area_um2=68294, accuracy_bits=20.8, ffs=785, throughput_msps=34.9, max_abs_err=5.44e-07 (2^-20.81), power_index=0.0839
- pipelined_m [data_width=27 n_iter=29 angle_guard=3 frac_guard=1 rounding=round m=7] area_um2=78662, accuracy_bits=23, ffs=510, throughput_msps=15.3, max_abs_err=1.16e-07 (2^-23.04), power_index=0.0747
Front coverage: area_um2 21800..78662 (HV reference 40000); accuracy_bits 11.4..23 (HV reference 10); data_width on the front 16..27 (registry 8..28).

Per family:
- pipelined: 33 evals, 27 feasible; max throughput seen 163 MSPS; best accuracy 13.92 bits; best feasible area_um2=36227; feasible ranges: data_width 13..20, n_iter 12..16, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 67 evals, 54 feasible; max throughput seen 86.6 MSPS; best accuracy 23.04 bits; best feasible area_um2=21800; feasible ranges: data_width 13..27, n_iter 12..29, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4596 in, 1192 out
- provider-reported cost: $0.0046
- full prompts and replies: `llm_trace.jsonl`

