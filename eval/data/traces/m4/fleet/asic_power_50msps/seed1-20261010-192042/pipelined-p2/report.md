# DSE run: asic_power_50msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_power_50msps: A 50 MSPS sin/cos unit in sky130 standard cells for a battery-powered radio: max error <= 2^-12. Minimise the relative power index; accuracy is the trade-off.
  target: asic-sky130hd
  constraint: throughput_msps >= 50
  constraint: max_abs_err <= 0.000244141
  objective: min power_index (HV ref 40)
  objective: max accuracy_bits (HV ref 12)
  select: min power_index
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=16,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc,m=3` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 31211 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 8315 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 381 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 8 | exact: schedule |
| latency_ns | 147 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.98 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000237 (2^-12.04) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.88 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 5.76e-05 (2^-14.08) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 0.944 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (19 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc,m=3` | 31211 | 381 | 54.3 | 8 | 1.98 | 0.000237 (2^-12.04) | 12.04 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=3,frac_guard=0,rounding=round,m=2` | 31620 | 476 | 69.4 | 9 | 2.25 | 0.00017 (2^-12.53) | 12.53 |
| 2 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=2` | 35678 | 531 | 72.3 | 10 | 2.53 | 8.35e-05 (2^-13.55) | 13.55 |
| 3 | `pipelined_m:data_width=21,n_iter=16,angle_guard=-2,frac_guard=3,rounding=round,m=2` | 42932 | 619 | 62.0 | 10 | 2.99 | 6.41e-05 (2^-13.93) | 13.93 |
| 4 | `pipelined_m:data_width=22,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=2` | 42548 | 633 | 62.0 | 10 | 3.01 | 3.32e-05 (2^-14.88) | 14.88 |
| 5 | `pipelined_m:data_width=23,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc,m=2` | 44221 | 657 | 62.0 | 10 | 3.13 | 3.23e-05 (2^-14.92) | 14.92 |
| 6 | `pipelined_m:data_width=23,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc,m=2` | 45851 | 678 | 59.9 | 10 | 3.24 | 3.17e-05 (2^-14.94) | 14.94 |
| 7 | `pipelined_m:data_width=24,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=2` | 45982 | 684 | 57.9 | 10 | 3.26 | 3.12e-05 (2^-14.97) | 14.97 |
| 8 | `pipelined_m:data_width=23,n_iter=16,angle_guard=2,frac_guard=3,rounding=round,m=2` | 48701 | 702 | 57.9 | 10 | 3.39 | 3.07e-05 (2^-14.99) | 14.99 |
| 9 | `pipelined_m:data_width=21,n_iter=20,angle_guard=0,frac_guard=1,rounding=round,m=2` | 52304 | 749 | 66.8 | 12 | 3.62 | 1.61e-05 (2^-15.92) | 15.92 |
| 10 | `pipelined_m:data_width=21,n_iter=20,angle_guard=2,frac_guard=3,rounding=round,m=2` | 56439 | 804 | 62.0 | 12 | 3.9 | 5.18e-06 (2^-17.56) | 17.56 |
| 11 | `pipelined_m:data_width=23,n_iter=20,angle_guard=0,frac_guard=3,rounding=round,m=2` | 59444 | 847 | 57.9 | 12 | 4.11 | 4.2e-06 (2^-17.86) | 17.86 |
| 12 | `pipelined_m:data_width=23,n_iter=20,angle_guard=2,frac_guard=3,rounding=round,m=2` | 60851 | 867 | 57.9 | 12 | 4.2 | 2.65e-06 (2^-18.53) | 18.53 |
| 13 | `pipelined_m:data_width=24,n_iter=20,angle_guard=2,frac_guard=2,rounding=round,m=2` | 61693 | 881 | 57.9 | 12 | 4.27 | 2.44e-06 (2^-18.64) | 18.64 |
| 14 | `pipelined_m:data_width=24,n_iter=20,angle_guard=2,frac_guard=3,rounding=round,m=2` | 63057 | 899 | 56.1 | 12 | 4.36 | 2.42e-06 (2^-18.66) | 18.66 |
| 15 | `pipelined_m:data_width=26,n_iter=20,angle_guard=0,frac_guard=1,rounding=round,m=2` | 63334 | 906 | 56.1 | 12 | 4.39 | 2.36e-06 (2^-18.69) | 18.69 |
| 16 | `pipelined_m:data_width=23,n_iter=27,angle_guard=1,frac_guard=2,rounding=round,m=2` | 80165 | 1158 | 59.9 | 16 | 5.58 | 2.3e-06 (2^-18.73) | 18.73 |
| 17 | `pipelined_m:data_width=23,n_iter=27,angle_guard=3,frac_guard=4,rounding=round,m=2` | 85897 | 1237 | 56.1 | 16 | 5.97 | 8.03e-07 (2^-20.25) | 20.25 |
| 18 | `pipelined_m:data_width=25,n_iter=27,angle_guard=3,frac_guard=4,rounding=trunc,m=2` | 90585 | 1321 | 52.7 | 16 | 6.34 | 2.49e-07 (2^-21.93) | 21.93 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is throughput-bound at 50 MSPS with an error ceiling of 2^-12, and the selection rule is min power_index. Both my families are 1-result/cycle, so throughput == Fmax and the binding risk is Fmax falling under 50 MHz, not cycles/result. Prior fleet data says `pipelined` is broadly feasible and already supplies 15/16 of the merged front, while `pipelined_m` is nearly unexplored yet holds the single lowest-power feasible point (3.63). That makes the plan two-pronged: (1) keep `pipelined` wide on data_width/n_iter to map the high-accuracy end of the curve, since the HV reference point (power 40, accuracy_bits 12) only credits designs that beat 12 accuracy bits; (2) push the majority of budget into `pipelined_m` with m in 2..4, where the register-count reduction is the only plausible route to a lower power_index than the current 3.63 corner. Round 1 is deliberately broad on W/N/guards to locate the feasible region and the Fmax-vs-m cliff; later rounds will narrow around the m that survives the 50 MSPS floor and around the minimum W/N that still clears 2^-12, then spend the reserved budget mapping the front over the full ranges of whichever families land on it.*)
- `pipelined` (45 evals): data_width=12..24, n_iter=8..28, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round. *Why:* Only family proven broadly feasible (48/56 feasible, 15/16 of the merged front). It is the 1-result/cycle backbone that supplies the high-accuracy end of the trade-off curve: with W up to 24 and N up to 28 it can push accuracy_bits well above the 2^-12 constraint, which is exactly what the HV reference (accuracy_bits ref 12) rewards. Ranges are kept wide on W/N to cover the accuracy axis, with angle_guard/frac_guard/rounding left open so the search can find the cheapest way to clear the error bound.
- `pipelined_m` (55 evals): data_width=12..24, n_iter=8..28, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round, m=2..4. *Why:* This family already owns the lowest feasible power_index seen so far (3.63 vs 4 for pipelined) but is badly under-mapped (only 1/44 feasible), so it is the highest-value place to spend budget: registering every m stages cuts FF count and hence power, at the cost of a longer critical path. m is restricted to 2..4 because m>=5 almost certainly drops Fmax below the 50 MSPS floor (m=1 is just `pipelined`). m=2 is the likely sweet spot (halved registers, Fmax still above 50 MHz); m=3 probes the edge. W/N ranges mirror `pipelined` so the two families can be compared on the same accuracy axis and jointly fill the front.

**Result (code):** 100 evaluations this round, 100 total; 48 feasible; hypervolume 243.8 (n/a).

**LLM decision:** `map_front` — The hypervolume is almost entirely set by the highest-accuracy front point: the rectangle (40 - 5.58) x (18.73 - 12) = 231.7 accounts for ~232 of the 243.8 total HV, so HV grows ~34 per extra accuracy bit at the top of the front, versus only ~6.7 per unit of power shaved. The front's accuracy range is 12..18.7 bits, but the registry allows data_width up to 28 (output LSB 2^-26) and n_iter up to 30, so roughly 26 bits is reachable - the front covers only about half the accuracy range and has just 9 points. The explored ranges are correspondingly narrow (pipelined_m data_width 16..23, n_iter 14..27 vs registry 8..28, 4..30), leaving the high-accuracy region (data_width 24..28, n_iter 20..30) essentially unmapped. The low-power corner is already tight: best power_index 1.98 sits at 54.3 MSPS (just above the 50 MSPS floor) and 12.04 bits (just above the 2^-12 limit), so there is little HV left to win there. All 9 front designs are pipelined_m and pipelined's feasible designs are dominated (best feasible power 3.47, best accuracy 17.95), so the front should be mapped over pipelined_m's full parameter ranges. With only the final 100-eval round left, spending it on full-range front mapping (seeded with the current front) is the highest-HV action.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 243.8 (gain this round: n/a (first round)).
Feasible designs: 48 of 100 evaluations (41 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 26% violate; best seen 180
- max_abs_err <= 0.000244141: 37% violate; best seen 2.3e-06 (2^-18.73)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=16 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=3] power_index=1.98, accuracy_bits=12, area_um2=31211, ffs=381, throughput_msps=54.3, max_abs_err=0.000237 (2^-12.04)
- pipelined_m [data_width=18 n_iter=14 angle_guard=3 frac_guard=0 rounding=round m=2] power_index=2.25, accuracy_bits=12.5, area_um2=31620, ffs=476, throughput_msps=69.4, max_abs_err=0.00017 (2^-12.53)
- pipelined_m [data_width=20 n_iter=14 angle_guard=0 frac_guard=3 rounding=trunc m=2] power_index=2.55, accuracy_bits=12.9, area_um2=35941, ffs=536, throughput_msps=64.3, max_abs_err=0.000135 (2^-12.86)
- pipelined_m [data_width=23 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=2] power_index=2.84, accuracy_bits=13, area_um2=39995, ffs=599, throughput_msps=59.9, max_abs_err=0.000123 (2^-12.99)
- pipelined_m [data_width=23 n_iter=14 angle_guard=0 frac_guard=3 rounding=trunc m=2] power_index=2.87, accuracy_bits=13, area_um2=40436, ffs=604, throughput_msps=57.9, max_abs_err=0.000123 (2^-12.99)
- pipelined_m [data_width=23 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc m=2] power_index=3.13, accuracy_bits=14.9, area_um2=44221, ffs=657, throughput_msps=62, max_abs_err=3.23e-05 (2^-14.92)
- pipelined_m [data_width=23 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=2] power_index=3.24, accuracy_bits=14.9, area_um2=45851, ffs=678, throughput_msps=59.9, max_abs_err=3.17e-05 (2^-14.94)
- pipelined_m [data_width=23 n_iter=20 angle_guard=0 frac_guard=3 rounding=round m=2] power_index=4.11, accuracy_bits=17.9, area_um2=59444, ffs=847, throughput_msps=57.9, max_abs_err=4.2e-06 (2^-17.86)
- pipelined_m [data_width=23 n_iter=27 angle_guard=1 frac_guard=2 rounding=round m=2] power_index=5.58, accuracy_bits=18.7, area_um2=80165, ffs=1158, throughput_msps=59.9, max_abs_err=2.3e-06 (2^-18.73)
Front coverage: power_index 1.98..5.58 (HV reference 40); accuracy_bits 12..18.7 (HV reference 12); data_width on the front 16..23 (registry 8..28).

Per family:
- pipelined: 45 evals, 30 feasible; max throughput seen 180 MSPS; best accuracy 17.95 bits; best feasible power_index=3.47; feasible ranges: data_width 18..24, n_iter 14..25, angle_guard -2..2, frac_guard 0..3
- pipelined_m: 55 evals, 18 feasible; max throughput seen 108 MSPS; best accuracy 18.73 bits; best feasible power_index=1.98; feasible ranges: data_width 16..23, n_iter 14..27, angle_guard 0..3, frac_guard 0..3, m 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `pipelined_m` (20 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (9 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 60 feasible; hypervolume 354.2 (+45.3%).

**LLM decision:** `map_front` — Round 2 gained +45.3% HV (354.2) and the front is still expanding, but it covers only part of the objectives' ranges: accuracy_bits spans 12..21.9 while the registry (data_width up to 28, output LSB 2^-(W-2)) permits roughly 26 bits, and power_index spans only 1.98..6.34 against an HV reference of 40. All 10 shown Pareto points are pipelined_m (pipelined's best feasible power_index is 3.47), and the feasible pipelined_m ranges already seen (data_width 16..26, n_iter 14..30, angle_guard -2..3, frac_guard 0..4, m 2..3) are wider than what the front samples, so the high-accuracy tail (21.9..~26 bits) and the low-power corner near the 2^-12 constraint are under-mapped. With 80 evals left and 2 rounds, spending this round on NSGA-II over the full ranges of the two on-front families (pipelined, pipelined_m), seeded with the current 16-design front, is the best way to cover the whole trade-off curve before the reserved end-of-run mapping. No family change is needed (iterative/unrolled_k cannot reach the 50 MSPS constraint), and the constraints are clearly reachable (best max_abs_err 2.49e-07, best throughput 180 MSPS), so infeasible/stop are not warranted.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 354.2 (gain this round: +45.3%).
Feasible designs: 60 of 120 evaluations (53 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 28% violate; best seen 180
- max_abs_err <= 0.000244141: 32% violate; best seen 2.49e-07 (2^-21.93)

Pareto front (feasible, 16 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=16 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=3] power_index=1.98, accuracy_bits=12, area_um2=31211, ffs=381, throughput_msps=54.3, max_abs_err=0.000237 (2^-12.04)
- pipelined_m [data_width=20 n_iter=14 angle_guard=0 frac_guard=3 rounding=trunc m=2] power_index=2.55, accuracy_bits=12.9, area_um2=35941, ffs=536, throughput_msps=64.3, max_abs_err=0.000135 (2^-12.86)
- pipelined_m [data_width=23 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=2] power_index=2.84, accuracy_bits=13, area_um2=39995, ffs=599, throughput_msps=59.9, max_abs_err=0.000123 (2^-12.99)
- pipelined_m [data_width=23 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc m=2] power_index=3.13, accuracy_bits=14.9, area_um2=44221, ffs=657, throughput_msps=62, max_abs_err=3.23e-05 (2^-14.92)
- pipelined_m [data_width=21 n_iter=20 angle_guard=0 frac_guard=1 rounding=round m=2] power_index=3.62, accuracy_bits=15.9, area_um2=52304, ffs=749, throughput_msps=66.8, max_abs_err=1.61e-05 (2^-15.92)
- pipelined_m [data_width=21 n_iter=20 angle_guard=2 frac_guard=3 rounding=round m=2] power_index=3.9, accuracy_bits=17.6, area_um2=56439, ffs=804, throughput_msps=62, max_abs_err=5.18e-06 (2^-17.56)
- pipelined_m [data_width=23 n_iter=20 angle_guard=2 frac_guard=3 rounding=round m=2] power_index=4.2, accuracy_bits=18.5, area_um2=60851, ffs=867, throughput_msps=57.9, max_abs_err=2.65e-06 (2^-18.53)
- pipelined_m [data_width=26 n_iter=20 angle_guard=0 frac_guard=1 rounding=round m=2] power_index=4.39, accuracy_bits=18.7, area_um2=63334, ffs=906, throughput_msps=56.1, max_abs_err=2.36e-06 (2^-18.69)
- pipelined_m [data_width=23 n_iter=27 angle_guard=1 frac_guard=2 rounding=round m=2] power_index=5.58, accuracy_bits=18.7, area_um2=80165, ffs=1158, throughput_msps=59.9, max_abs_err=2.3e-06 (2^-18.73)
- pipelined_m [data_width=25 n_iter=27 angle_guard=3 frac_guard=4 rounding=trunc m=2] power_index=6.34, accuracy_bits=21.9, area_um2=90585, ffs=1321, throughput_msps=52.7, max_abs_err=2.49e-07 (2^-21.93)
Front coverage: power_index 1.98..6.34 (HV reference 40); accuracy_bits 12..21.9 (HV reference 12); data_width on the front 16..26 (registry 8..28).

Per family:
- pipelined: 45 evals, 30 feasible; max throughput seen 180 MSPS; best accuracy 17.95 bits; best feasible power_index=3.47; feasible ranges: data_width 18..24, n_iter 14..25, angle_guard -2..2, frac_guard 0..3
- pipelined_m: 75 evals, 30 feasible; max throughput seen 108 MSPS; best accuracy 21.93 bits; best feasible power_index=1.98; feasible ranges: data_width 16..26, n_iter 14..30, angle_guard -2..3, frac_guard 0..4, m 2..3
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (80 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (16 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 80 feasible; hypervolume 354.8 (+0.2%).

**LLM decision:** `stop` — Budget is exhausted (200/200 evals, final round) and the front is feasible and well-covered, so neither refine nor map_front is available. Constraints are met: the throughput constraint (>=50 MSPS) is satisfied by every front point (54.3-72.3 MSPS) and the error constraint (<=2^-12) is met with margin by the selection-rule winner pipelined_m [data_width=16 n_iter=16 angle_guard=1 frac_guard=2 trunc m=3] at power_index=1.98, accuracy_bits=12.04, max_abs_err=0.000237, throughput=54.3 MSPS. The front spans power_index 1.98..6.34 and accuracy_bits 12..21.9 (data_width 16..26), i.e. it already covers the low-power corner the spec selects on plus a long accuracy tail, and the round's hypervolume gain was only +0.2%, indicating convergence. No infeasibility: 80 of 200 evaluations were feasible and 19 designs sit on the Pareto front, so the registry can meet the spec.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 354.8 (gain this round: +0.2%).
Feasible designs: 80 of 200 evaluations (72 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 44% violate; best seen 180
- max_abs_err <= 0.000244141: 24% violate; best seen 2.86e-08 (2^-25.06)

Pareto front (feasible, 19 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=16 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=3] power_index=1.98, accuracy_bits=12, area_um2=31211, ffs=381, throughput_msps=54.3, max_abs_err=0.000237 (2^-12.04)
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=2] power_index=2.53, accuracy_bits=13.5, area_um2=35678, ffs=531, throughput_msps=72.3, max_abs_err=8.35e-05 (2^-13.55)
- pipelined_m [data_width=22 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=2] power_index=3.01, accuracy_bits=14.9, area_um2=42548, ffs=633, throughput_msps=62, max_abs_err=3.32e-05 (2^-14.88)
- pipelined_m [data_width=23 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=2] power_index=3.24, accuracy_bits=14.9, area_um2=45851, ffs=678, throughput_msps=59.9, max_abs_err=3.17e-05 (2^-14.94)
- pipelined_m [data_width=23 n_iter=16 angle_guard=2 frac_guard=3 rounding=round m=2] power_index=3.39, accuracy_bits=15, area_um2=48701, ffs=702, throughput_msps=57.9, max_abs_err=3.07e-05 (2^-14.99)
- pipelined_m [data_width=21 n_iter=20 angle_guard=2 frac_guard=3 rounding=round m=2] power_index=3.9, accuracy_bits=17.6, area_um2=56439, ffs=804, throughput_msps=62, max_abs_err=5.18e-06 (2^-17.56)
- pipelined_m [data_width=23 n_iter=20 angle_guard=2 frac_guard=3 rounding=round m=2] power_index=4.2, accuracy_bits=18.5, area_um2=60851, ffs=867, throughput_msps=57.9, max_abs_err=2.65e-06 (2^-18.53)
- pipelined_m [data_width=24 n_iter=20 angle_guard=2 frac_guard=3 rounding=round m=2] power_index=4.36, accuracy_bits=18.7, area_um2=63057, ffs=899, throughput_msps=56.1, max_abs_err=2.42e-06 (2^-18.66)
- pipelined_m [data_width=23 n_iter=27 angle_guard=1 frac_guard=2 rounding=round m=2] power_index=5.58, accuracy_bits=18.7, area_um2=80165, ffs=1158, throughput_msps=59.9, max_abs_err=2.3e-06 (2^-18.73)
- pipelined_m [data_width=25 n_iter=27 angle_guard=3 frac_guard=4 rounding=trunc m=2] power_index=6.34, accuracy_bits=21.9, area_um2=90585, ffs=1321, throughput_msps=52.7, max_abs_err=2.49e-07 (2^-21.93)
Front coverage: power_index 1.98..6.34 (HV reference 40); accuracy_bits 12..21.9 (HV reference 12); data_width on the front 16..26 (registry 8..28).

Per family:
- pipelined: 45 evals, 30 feasible; max throughput seen 180 MSPS; best accuracy 17.95 bits; best feasible power_index=3.47; feasible ranges: data_width 18..24, n_iter 14..25, angle_guard -2..2, frac_guard 0..3
- pipelined_m: 155 evals, 50 feasible; max throughput seen 108 MSPS; best accuracy 25.06 bits; best feasible power_index=1.98; feasible ranges: data_width 16..26, n_iter 14..30, angle_guard -2..3, frac_guard 0..4, m 2..3
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 11162 in, 12913 out
- provider-reported cost: $0.0126
- full prompts and replies: `llm_trace.jsonl`

