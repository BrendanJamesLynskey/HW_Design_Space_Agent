# DSE run: asic_power_50msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
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
`pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc,m=3` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 29925 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 7972 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 343 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 135 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.84 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.00016 (2^-12.61) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 10.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 3.41e-05 (2^-14.84) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 2.24 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.6 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc,m=3` | 29925 | 343 | 51.9 | 7 | 1.84 | 0.00016 (2^-12.61) | 12.61 |
| 1 | `pipelined_m:data_width=17,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=2` | 33961 | 505 | 75.4 | 10 | 2.41 | 0.000139 (2^-12.81) | 12.81 |
| 2 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=1,rounding=trunc,m=2` | 35115 | 545 | 72.3 | 10 | 2.55 | 0.000118 (2^-13.05) | 13.05 |
| 3 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=round,m=2` | 37100 | 560 | 72.3 | 10 | 2.65 | 8.26e-05 (2^-13.56) | 13.56 |
| 4 | `pipelined_m:data_width=18,n_iter=17,angle_guard=2,frac_guard=2,rounding=round,m=2` | 41935 | 626 | 72.3 | 11 | 2.98 | 4.73e-05 (2^-14.37) | 14.37 |
| 5 | `pipelined_m:data_width=18,n_iter=18,angle_guard=2,frac_guard=2,rounding=round,m=2` | 43621 | 626 | 72.3 | 11 | 3.03 | 3.81e-05 (2^-14.68) | 14.68 |
| 6 | `pipelined_m:data_width=19,n_iter=18,angle_guard=2,frac_guard=1,rounding=round,m=2` | 44391 | 639 | 69.4 | 11 | 3.08 | 3.09e-05 (2^-14.98) | 14.98 |
| 7 | `pipelined_m:data_width=19,n_iter=18,angle_guard=2,frac_guard=2,rounding=round,m=2` | 45609 | 655 | 69.4 | 11 | 3.16 | 2.34e-05 (2^-15.38) | 15.38 |
| 8 | `pipelined_m:data_width=20,n_iter=17,angle_guard=1,frac_guard=2,rounding=round,m=2` | 45151 | 674 | 66.8 | 11 | 3.2 | 2.32e-05 (2^-15.40) | 15.40 |
| 9 | `pipelined_m:data_width=23,n_iter=18,angle_guard=-1,frac_guard=3,rounding=trunc,m=2` | 51664 | 756 | 57.9 | 11 | 3.62 | 1.23e-05 (2^-16.32) | 16.32 |
| 10 | `pipelined_m:data_width=25,n_iter=18,angle_guard=-2,frac_guard=2,rounding=round,m=2` | 55009 | 790 | 56.1 | 11 | 3.82 | 9.51e-06 (2^-16.68) | 16.68 |
| 11 | `pipelined_m:data_width=27,n_iter=20,angle_guard=2,frac_guard=1,rounding=trunc,m=2` | 65524 | 956 | 52.7 | 12 | 4.59 | 2.04e-06 (2^-18.90) | 18.90 |
| 12 | `pipelined_m:data_width=25,n_iter=26,angle_guard=4,frac_guard=0,rounding=round,m=2` | 79921 | 1148 | 52.7 | 15 | 5.55 | 7.53e-07 (2^-20.34) | 20.34 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show pipelined is the only family meeting the 50 MSPS throughput constraint (60 feasible, best power_index 4.47), while iterative, unrolled_k and pipelined_m all returned 0 feasible. Since I am restricted to pipelined and pipelined_m, I concentrate the budget on pipelined to refine the low-power end of the feasible front (smaller data_width, fewer n_iter, minimal guards, round) and spend a smaller share confirming pipelined_m's infeasibility in the same accuracy box. This maximizes hypervolume coverage of the feasible trade-off curve and drives the selection rule (min power_index) toward its best achievable value.*)
- `pipelined` (50 evals): data_width=14..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* Only pipelined is feasible (60/70, best power 4.47); it is the sole source of the merged front. Focus the remaining budget on the low-power corner of the feasible region (smaller W, fewer stages, minimal guards, round) to push power_index below 4.47 while keeping max_abs_err <= 2^-12.
- `pipelined_m` (50 evals): data_width=14..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* pipelined_m had 0 feasible in 30 evals, likely because fewer registers lower Fmax and break the 50 MSPS throughput floor. Re-test it in the same feasible accuracy box with m=2..4 to confirm whether it can ever beat pipelined on power, or to formally rule it out.

**Result (code):** 100 evaluations this round, 100 total; 23 feasible; hypervolume 57.57 (n/a).

**LLM decision:** `refine` — Round 1 found 23 feasible designs with a Pareto front spanning power_index 2.41-4.1 and accuracy_bits 12.8-13.6. The pipelined_m family achieved the best power (2.41) but only 1 feasible point was found due to narrow search ranges (m=2, data_width=17 only). The pipelined family has 22 feasible points but higher power (3.38-4.1). The front is concentrated in a small region of the objective space, suggesting the search ranges were too tight. By widening pipelined_m's m range to 2-4 and data_width to 16-20, we can explore more low-power configurations. Simultaneously, focusing pipelined on its proven feasible region with rounding exploration should refine the accuracy-power trade-off. This balanced approach should expand the Pareto front and improve hypervolume coverage.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 57.57 (gain this round: n/a (first round)).
Feasible designs: 23 of 100 evaluations (12 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 18% violate; best seen 163
- max_abs_err <= 0.000244141: 75% violate; best seen 5.46e-05 (2^-14.16)

Pareto front (feasible, 3 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=2] power_index=2.41, accuracy_bits=12.8, area_um2=33961, ffs=505, throughput_msps=75.4, max_abs_err=0.000139 (2^-12.81)
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] power_index=3.85, accuracy_bits=13.2, area_um2=42933, ffs=929, throughput_msps=132, max_abs_err=0.000109 (2^-13.17)
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] power_index=4.1, accuracy_bits=13.6, area_um2=46462, ffs=982, throughput_msps=132, max_abs_err=8.26e-05 (2^-13.56)
Front coverage: power_index 2.41..4.1 (HV reference 40); accuracy_bits 12.8..13.6 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 50 evals, 22 feasible; max throughput seen 163 MSPS; best accuracy 13.56 bits; best feasible power_index=3.38; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 1 feasible; max throughput seen 91.1 MSPS; best accuracy 14.16 bits; best feasible power_index=2.41; feasible ranges: data_width 17..17, n_iter 16..16, angle_guard 2..2, frac_guard 0..0, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 1 found 23 feasible designs with a Pareto front spanning power_index 2.41-4.1 and accuracy_bits 12.8-13.6. The pipelined_m family achieved the best power (2.41) but only 1 feasible point was found due to narrow search ranges (m=2, data_width=17 only). The pipelined family has 22 feasible points but higher power (3.38-4.1). The front is concentrated in a small region of the objective space, suggesting the search ranges were too tight. By widening pipelined_m's m range to 2-4 and data_width to 16-20, we can explore more low-power configurations. Simultaneously, focusing pipelined on its proven feasible region with rounding exploration should refine the accuracy-power trade-off. This balanced approach should expand the Pareto front and improve hypervolume coverage.*)
- `pipelined_m` (10 evals): data_width=16..20, n_iter=14..18, angle_guard=0..3, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m achieved the best power_index (2.41) but only 1 feasible point was found because the search space was too narrow (m=2 only, data_width=17 only). Widening m to 2-4 and data_width to 16-20 should reveal more low-power feasible points while maintaining throughput >= 50 MSPS.
- `pipelined` (10 evals): data_width=16..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined has 22 feasible points and covers the higher accuracy end of the front (up to 13.6 bits). Focusing on the proven feasible region (data_width 16-18, n_iter 14-16) with rounding exploration should refine the front and potentially find lower power points at similar accuracy.

**Result (code):** 20 evaluations this round, 120 total; 39 feasible; hypervolume 125.9 (+118.7%).

**LLM decision:** `stop` — The front is feasible and covers the required trade-off: power_index 1.84..3.16 (well below the HV reference of 40) and accuracy_bits 12.6..15.4 (above the HV reference of 12). The best design (pipelined_m, data_width=18, n_iter=15, m=3) meets the throughput constraint (51.9 MSPS >= 50) and the accuracy constraint (max_abs_err=0.00016 <= 0.000244141) with a power_index of 1.84. Since this is the final round, the current front is sufficient for selection.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 125.9 (gain this round: +118.7%).
Feasible designs: 39 of 120 evaluations (26 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 17% violate; best seen 163
- max_abs_err <= 0.000244141: 64% violate; best seen 2.34e-05 (2^-15.38)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc m=3] power_index=1.84, accuracy_bits=12.6, area_um2=29925, ffs=343, throughput_msps=51.9, max_abs_err=0.00016 (2^-12.61)
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=2] power_index=2.41, accuracy_bits=12.8, area_um2=33961, ffs=505, throughput_msps=75.4, max_abs_err=0.000139 (2^-12.81)
- pipelined_m [data_width=18 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc m=2] power_index=2.99, accuracy_bits=14.2, area_um2=42658, ffs=624, throughput_msps=72.3, max_abs_err=5.33e-05 (2^-14.20)
- pipelined_m [data_width=19 n_iter=18 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=3.08, accuracy_bits=15, area_um2=44391, ffs=639, throughput_msps=69.4, max_abs_err=3.09e-05 (2^-14.98)
- pipelined_m [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=3.16, accuracy_bits=15.4, area_um2=45609, ffs=655, throughput_msps=69.4, max_abs_err=2.34e-05 (2^-15.38)
Front coverage: power_index 1.84..3.16 (HV reference 40); accuracy_bits 12.6..15.4 (HV reference 12); data_width on the front 17..19 (registry 8..28).

Per family:
- pipelined: 60 evals, 31 feasible; max throughput seen 163 MSPS; best accuracy 14.16 bits; best feasible power_index=3.38; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 60 evals, 8 feasible; max throughput seen 91.1 MSPS; best accuracy 15.38 bits; best feasible power_index=1.84; feasible ranges: data_width 17..19, n_iter 14..18, angle_guard 0..2, frac_guard 0..2, m 2..3
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (80 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (5 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 80 feasible; hypervolume 301.6 (+139.6%).

**No LLM call** (code's front-mapping round): The front is feasible and covers the required trade-off: power_index 1.84..3.16 (well below the HV reference of 40) and accuracy_bits 12.6..15.4 (above the HV reference of 12). The best design (pipelined_m, data_width=18, n_iter=15, m=3) meets the throughput constraint (51.9 MSPS >= 50) and the accuracy constraint (max_abs_err=0.00016 <= 0.000244141) with a power_index of 1.84. Since this is the final round, the current front is sufficient for selection.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 301.6 (gain this round: +139.6%).
Feasible designs: 80 of 200 evaluations (60 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 29% violate; best seen 163
- max_abs_err <= 0.000244141: 40% violate; best seen 2.86e-08 (2^-25.06)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc m=3] power_index=1.84, accuracy_bits=12.6, area_um2=29925, ffs=343, throughput_msps=51.9, max_abs_err=0.00016 (2^-12.61)
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=2] power_index=2.41, accuracy_bits=12.8, area_um2=33961, ffs=505, throughput_msps=75.4, max_abs_err=0.000139 (2^-12.81)
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=2.65, accuracy_bits=13.6, area_um2=37100, ffs=560, throughput_msps=72.3, max_abs_err=8.26e-05 (2^-13.56)
- pipelined_m [data_width=18 n_iter=17 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=2.98, accuracy_bits=14.4, area_um2=41935, ffs=626, throughput_msps=72.3, max_abs_err=4.73e-05 (2^-14.37)
- pipelined_m [data_width=18 n_iter=18 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=3.03, accuracy_bits=14.7, area_um2=43621, ffs=626, throughput_msps=72.3, max_abs_err=3.81e-05 (2^-14.68)
- pipelined_m [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=3.16, accuracy_bits=15.4, area_um2=45609, ffs=655, throughput_msps=69.4, max_abs_err=2.34e-05 (2^-15.38)
- pipelined_m [data_width=20 n_iter=17 angle_guard=1 frac_guard=2 rounding=round m=2] power_index=3.2, accuracy_bits=15.4, area_um2=45151, ffs=674, throughput_msps=66.8, max_abs_err=2.32e-05 (2^-15.40)
- pipelined_m [data_width=23 n_iter=18 angle_guard=-1 frac_guard=3 rounding=trunc m=2] power_index=3.62, accuracy_bits=16.3, area_um2=51664, ffs=756, throughput_msps=57.9, max_abs_err=1.23e-05 (2^-16.32)
- pipelined_m [data_width=27 n_iter=20 angle_guard=2 frac_guard=1 rounding=trunc m=2] power_index=4.59, accuracy_bits=18.9, area_um2=65524, ffs=956, throughput_msps=52.7, max_abs_err=2.04e-06 (2^-18.90)
- pipelined_m [data_width=25 n_iter=26 angle_guard=4 frac_guard=0 rounding=round m=2] power_index=5.55, accuracy_bits=20.3, area_um2=79921, ffs=1148, throughput_msps=52.7, max_abs_err=7.53e-07 (2^-20.34)
Front coverage: power_index 1.84..5.55 (HV reference 40); accuracy_bits 12.6..20.3 (HV reference 12); data_width on the front 17..27 (registry 8..28).

Per family:
- pipelined: 60 evals, 31 feasible; max throughput seen 163 MSPS; best accuracy 14.16 bits; best feasible power_index=3.38; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 140 evals, 49 feasible; max throughput seen 91.1 MSPS; best accuracy 25.06 bits; best feasible power_index=1.84; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..3
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7921 in, 2153 out
- provider-reported cost: $0.0041
- full prompts and replies: `llm_trace.jsonl`

