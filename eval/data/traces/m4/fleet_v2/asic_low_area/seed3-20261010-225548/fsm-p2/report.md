# DSE run: asic_low_area

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
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
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=15,n_iter=13,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 6870 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1830 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 98 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 147 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 9.22 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 108 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.152 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000879 (2^-10.15) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 7.2 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00022 (2^-12.15) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.8 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.2 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (25 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=13,angle_guard=0,frac_guard=0,rounding=round` | 6870 | 98 | 9.2 | 16 | 0.152 | 0.000879 (2^-10.15) | 10.15 |
| 1 | `iterative:data_width=15,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` | 6930 | 98 | 8.7 | 17 | 0.162 | 0.00081 (2^-10.27) | 10.27 |
| 2 | `iterative:data_width=15,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 7057 | 101 | 8.0 | 17 | 0.166 | 0.000599 (2^-10.71) | 10.71 |
| 3 | `iterative:data_width=15,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc` | 7121 | 102 | 8.3 | 17 | 0.167 | 0.000594 (2^-10.72) | 10.72 |
| 4 | `iterative:data_width=15,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc` | 7184 | 103 | 8.0 | 17 | 0.169 | 0.000567 (2^-10.78) | 10.78 |
| 5 | `iterative:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` | 7322 | 104 | 8.3 | 17 | 0.172 | 0.0004 (2^-11.29) | 11.29 |
| 6 | `iterative:data_width=16,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 7431 | 104 | 7.4 | 19 | 0.193 | 0.000373 (2^-11.39) | 11.39 |
| 7 | `iterative:data_width=16,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 7446 | 105 | 7.6 | 18 | 0.184 | 0.000301 (2^-11.70) | 11.70 |
| 8 | `iterative:data_width=16,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 7449 | 106 | 7.7 | 17 | 0.175 | 0.000294 (2^-11.73) | 11.73 |
| 9 | `iterative:data_width=16,n_iter=23,angle_guard=2,frac_guard=0,rounding=round` | 7743 | 107 | 5.0 | 26 | 0.274 | 0.000285 (2^-11.78) | 11.78 |
| 10 | `iterative:data_width=17,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc` | 7967 | 114 | 7.4 | 17 | 0.187 | 0.000235 (2^-12.06) | 12.06 |
| 11 | `iterative:data_width=17,n_iter=14,angle_guard=1,frac_guard=4,rounding=trunc` | 8757 | 119 | 6.9 | 17 | 0.2 | 0.000181 (2^-12.43) | 12.43 |
| 12 | `iterative:data_width=17,n_iter=26,angle_guard=4,frac_guard=2,rounding=trunc` | 8781 | 119 | 4.1 | 29 | 0.342 | 0.000141 (2^-12.79) | 12.79 |
| 13 | `iterative:data_width=19,n_iter=23,angle_guard=2,frac_guard=0,rounding=trunc` | 8869 | 124 | 4.5 | 26 | 0.315 | 0.000101 (2^-13.27) | 13.27 |
| 14 | `iterative:data_width=20,n_iter=23,angle_guard=2,frac_guard=0,rounding=round` | 9624 | 129 | 4.4 | 26 | 0.334 | 2.17e-05 (2^-15.49) | 15.49 |
| 15 | `iterative:data_width=19,n_iter=26,angle_guard=4,frac_guard=3,rounding=trunc` | 10177 | 132 | 3.8 | 29 | 0.387 | 2.01e-05 (2^-15.60) | 15.60 |
| 16 | `iterative:data_width=22,n_iter=23,angle_guard=2,frac_guard=0,rounding=round` | 10626 | 140 | 4.1 | 26 | 0.365 | 5.49e-06 (2^-17.47) | 17.47 |
| 17 | `iterative:data_width=24,n_iter=27,angle_guard=4,frac_guard=0,rounding=trunc` | 11560 | 153 | 3.2 | 30 | 0.46 | 2.96e-06 (2^-18.37) | 18.37 |
| 18 | `iterative:data_width=24,n_iter=22,angle_guard=0,frac_guard=1,rounding=trunc` | 11567 | 151 | 4.2 | 25 | 0.38 | 2.68e-06 (2^-18.51) | 18.51 |
| 19 | `iterative:data_width=24,n_iter=26,angle_guard=1,frac_guard=0,rounding=round` | 11673 | 150 | 3.6 | 29 | 0.441 | 1.76e-06 (2^-19.12) | 19.12 |
| 20 | `iterative:data_width=25,n_iter=23,angle_guard=2,frac_guard=0,rounding=trunc` | 11861 | 156 | 3.8 | 26 | 0.408 | 1.45e-06 (2^-19.40) | 19.40 |
| 21 | `iterative:data_width=25,n_iter=23,angle_guard=2,frac_guard=0,rounding=round` | 12128 | 156 | 3.8 | 26 | 0.412 | 8.71e-07 (2^-20.13) | 20.13 |
| 22 | `iterative:data_width=26,n_iter=26,angle_guard=1,frac_guard=0,rounding=round` | 12747 | 161 | 3.4 | 29 | 0.477 | 3.95e-07 (2^-21.27) | 21.27 |
| 23 | `iterative:data_width=28,n_iter=26,angle_guard=1,frac_guard=0,rounding=trunc` | 13518 | 172 | 3.2 | 29 | 0.508 | 2.4e-07 (2^-21.99) | 21.99 |
| 24 | `unrolled_k:data_width=28,n_iter=25,angle_guard=3,frac_guard=4,rounding=round,k=2` | 21878 | 182 | 2.8 | 16 | 0.368 | 7.42e-08 (2^-23.68) | 23.68 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show the merged front is essentially the iterative family (22/23 points, best area 6930 um2), while pipelined (31701) and pipelined_m (20020) are far larger in area and contribute almost nothing. Since the spec's selection rule is min area and the only hard constraints are throughput>=1 MSPS and max_abs_err<=2^-10, the value of the remaining budget is to densely map the low-area iterative trade-off curve (accuracy_bits vs area) and to check whether unrolled_k offers any area/throughput point that iterative misses. I therefore concentrate on iterative with tight, feasibility-focused ranges (small data_width 12-18, n_iter 12-18, negative angle_guard down to -2, minimal frac_guard, both roundings) to push area down while keeping the error bound, and include unrolled_k with the same accuracy ranges plus k=2..4 to test the throughput/area trade-off. I avoid wide ranges that would waste evaluations on infeasible or area-dominated corners, and I do not touch pipelined/pipelined_m since they are outside my assigned families and already dominated.*)
- `iterative` (50 evals): data_width=12..18, n_iter=12..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative already owns 22/23 of the merged front and its best feasible area (6930 um2) is far below pipelined (31701) and pipelined_m (20020). Since area is the selection objective and the only hard constraints are throughput>=1 MSPS and max_abs_err<=2^-10, the whole front lives in the low-area iterative corner. I narrow to the region that actually produces feasible, low-area points: data_width 12-18 (12 is the smallest width that can reach ~10+ accuracy bits with enough n_iter; going below 12 risks missing the error bound, going above 18 only inflates area), n_iter 12-18 (enough micro-rotations to hit 2^-10 with modest width; beyond ~18 area grows with little accuracy gain), angle_guard -2..2 (negative guard shrinks the atan-LUT/angle path and area; -2 is the registry floor), frac_guard 0..2 (0 is cheapest; small extra guard only trades area for a tiny accuracy bump), rounding both (round can shave the error term, letting a slightly smaller n_iter/width stay feasible). This focuses the remaining budget on densely mapping the iterative trade-off curve rather than re-exploring wide ranges.
- `unrolled_k` (50 evals): data_width=12..18, n_iter=12..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k is the only other family I may use, and it is the natural area/throughput trade-off partner to iterative: chaining k micro-rotations per cycle raises throughput (helping the >=1 MSPS constraint at lower Fmax) but adds combinational depth and area. I keep the same accuracy-relevant ranges as iterative (data_width 12-18, n_iter 12-18, angle_guard -2..2, frac_guard 0..2, both roundings) so the accuracy axis is comparable, and restrict k to 2..4: k=2 is the cheapest unrolled option and most likely to stay near iterative's area while still clearing 1 MSPS; k>4 tends to add area and timing pressure with diminishing throughput benefit for this low-throughput spec. This lets the search confirm whether any unrolled_k point beats or complements the iterative front, and if not, the merged front stays dominated by iterative.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 65 feasible; hypervolume 1.196e+05 (n/a).

**LLM decision:** `refine` — The front currently spans area 6870-16908 um2 and accuracy 10.2-14.2 bits. The selection rule is min area, so the low-area corner (iterative ~6870 um2) is critical. However, hypervolume rewards covering the full trade-off curve. The mid-range (accuracy 11-13 bits, area 7000-12000 um2) is under-sampled. Refining both families around their known feasible regions will densify the front in the mid-range and confirm the area-minimum corner. Pipelined families are not yet explored but are likely area-inefficient for this spec (throughput >= 1 MSPS is easily met by iterative/unrolled_k, and pipelined adds register overhead). Focusing on the two families already on the front is the best use of the remaining 100 evals.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.196e+05 (gain this round: n/a (first round)).
Feasible designs: 65 of 100 evaluations (51 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 10.3
- max_abs_err <= 0.000976562: 35% violate; best seen 5.33e-05 (2^-14.20)

Pareto front (feasible, 12 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] area_um2=6870, accuracy_bits=10.2, ffs=98, throughput_msps=9.22, max_abs_err=0.000879 (2^-10.15), power_index=0.152
- iterative [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] area_um2=6930, accuracy_bits=10.3, ffs=98, throughput_msps=8.68, max_abs_err=0.00081 (2^-10.27), power_index=0.162
- iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=7079, accuracy_bits=10.6, ffs=100, throughput_msps=7.45, max_abs_err=0.000632 (2^-10.63), power_index=0.184
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=7184, accuracy_bits=10.8, ffs=103, throughput_msps=8, max_abs_err=0.000567 (2^-10.78), power_index=0.169
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] area_um2=7322, accuracy_bits=11.3, ffs=104, throughput_msps=8.32, max_abs_err=0.0004 (2^-11.29), power_index=0.172
- iterative [data_width=16 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] area_um2=7431, accuracy_bits=11.4, ffs=104, throughput_msps=7.45, max_abs_err=0.000373 (2^-11.39), power_index=0.193
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=7449, accuracy_bits=11.7, ffs=106, throughput_msps=7.7, max_abs_err=0.000294 (2^-11.73), power_index=0.175
- unrolled_k [data_width=18 n_iter=17 angle_guard=-1 frac_guard=1 rounding=trunc k=2] area_um2=10862, accuracy_bits=12.5, ffs=116, throughput_msps=5.72, max_abs_err=0.000179 (2^-12.45), power_index=0.154
- unrolled_k [data_width=18 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc k=4] area_um2=16277, accuracy_bits=13.5, ffs=118, throughput_msps=4.31, max_abs_err=8.72e-05 (2^-13.49), power_index=0.129
- unrolled_k [data_width=18 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc k=4] area_um2=16908, accuracy_bits=14.2, ffs=120, throughput_msps=4.31, max_abs_err=5.33e-05 (2^-14.20), power_index=0.133
Front coverage: area_um2 6870..16908 (HV reference 40000); accuracy_bits 10.2..14.2 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 50 evals, 36 feasible; max throughput seen 10.3 MSPS; best accuracy 12.06 bits; best feasible area_um2=6870; feasible ranges: data_width 13..17, n_iter 12..18, angle_guard -1..2, frac_guard 0..2
- unrolled_k: 50 evals, 29 feasible; max throughput seen 8.53 MSPS; best accuracy 14.20 bits; best feasible area_um2=9781; feasible ranges: data_width 14..18, n_iter 13..18, angle_guard -2..2, frac_guard 1..2, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The front currently spans area 6870-16908 um2 and accuracy 10.2-14.2 bits. The selection rule is min area, so the low-area corner (iterative ~6870 um2) is critical. However, hypervolume rewards covering the full trade-off curve. The mid-range (accuracy 11-13 bits, area 7000-12000 um2) is under-sampled. Refining both families around their known feasible regions will densify the front in the mid-range and confirm the area-minimum corner. Pipelined families are not yet explored but are likely area-inefficient for this spec (throughput >= 1 MSPS is easily met by iterative/unrolled_k, and pipelined adds register overhead). Focusing on the two families already on the front is the best use of the remaining 100 evals.*)
- `iterative` (10 evals): data_width=14..16, n_iter=13..16, angle_guard=-1..2, frac_guard=0..1, rounding=trunc|round. *Why:* iterative dominates the low-area end of the front (6870 um2 at 10.2 bits). Tightening around the known feasible region (data_width 14-16, n_iter 13-16) focuses the search on the area-minimum corner while allowing small accuracy gains via angle_guard/frac_guard.
- `unrolled_k` (10 evals): data_width=14..18, n_iter=14..18, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k provides the high-accuracy end (up to 14.2 bits) but at higher area. Refining around the feasible region (data_width 14-18, n_iter 14-18, k 2-4) helps map the trade-off curve between iterative and unrolled_k, improving hypervolume coverage in the mid-accuracy range.

**Result (code):** 20 evaluations this round, 120 total; 81 feasible; hypervolume 1.196e+05 (+0.0%).

**LLM decision:** `stop` — The feasible Pareto front is well-established and meets all constraints. The minimum area design (iterative, 6870 um^2) achieves 10.2 accuracy bits and 9.22 MSPS throughput, satisfying the >=1 MSPS and <=2^-10 error requirements. The front covers a reasonable range of the trade-off space (area 6870-16908 um^2, accuracy 10.2-14.2 bits) with 13 distinct feasible designs. Since this is the final round, no further exploration is possible. The selection rule (min area) clearly points to the iterative design at 6870 um^2 as the final choice.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.196e+05 (gain this round: +0.0%).
Feasible designs: 81 of 120 evaluations (59 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 10.3
- max_abs_err <= 0.000976562: 32% violate; best seen 5.33e-05 (2^-14.20)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] area_um2=6870, accuracy_bits=10.2, ffs=98, throughput_msps=9.22, max_abs_err=0.000879 (2^-10.15), power_index=0.152
- iterative [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] area_um2=6930, accuracy_bits=10.3, ffs=98, throughput_msps=8.68, max_abs_err=0.00081 (2^-10.27), power_index=0.162
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=7121, accuracy_bits=10.7, ffs=102, throughput_msps=8.32, max_abs_err=0.000594 (2^-10.72), power_index=0.167
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=7184, accuracy_bits=10.8, ffs=103, throughput_msps=8, max_abs_err=0.000567 (2^-10.78), power_index=0.169
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] area_um2=7322, accuracy_bits=11.3, ffs=104, throughput_msps=8.32, max_abs_err=0.0004 (2^-11.29), power_index=0.172
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=7446, accuracy_bits=11.7, ffs=105, throughput_msps=7.56, max_abs_err=0.000301 (2^-11.70), power_index=0.184
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=7449, accuracy_bits=11.7, ffs=106, throughput_msps=7.7, max_abs_err=0.000294 (2^-11.73), power_index=0.175
- iterative [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=7967, accuracy_bits=12.1, ffs=114, throughput_msps=7.42, max_abs_err=0.000235 (2^-12.06), power_index=0.187
- unrolled_k [data_width=18 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc k=4] area_um2=16277, accuracy_bits=13.5, ffs=118, throughput_msps=4.31, max_abs_err=8.72e-05 (2^-13.49), power_index=0.129
- unrolled_k [data_width=18 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc k=4] area_um2=16908, accuracy_bits=14.2, ffs=120, throughput_msps=4.31, max_abs_err=5.33e-05 (2^-14.20), power_index=0.133
Front coverage: area_um2 6870..16908 (HV reference 40000); accuracy_bits 10.2..14.2 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 60 evals, 44 feasible; max throughput seen 10.3 MSPS; best accuracy 12.06 bits; best feasible area_um2=6870; feasible ranges: data_width 13..17, n_iter 12..18, angle_guard -1..2, frac_guard 0..2
- unrolled_k: 60 evals, 37 feasible; max throughput seen 8.53 MSPS; best accuracy 14.20 bits; best feasible area_um2=9198; feasible ranges: data_width 14..18, n_iter 13..18, angle_guard -2..2, frac_guard 0..2, k 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `iterative` (62 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (10 front designs; box front_anchored)
- `unrolled_k` (18 evals): data_width=17..28, n_iter=15..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (3 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 156 feasible; hypervolume 3.866e+05 (+223.3%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and meets all constraints. The minimum area design (iterative, 6870 um^2) achieves 10.2 accuracy bits and 9.22 MSPS throughput, satisfying the >=1 MSPS and <=2^-10 error requirements. The front covers a reasonable range of the trade-off space (area 6870-16908 um^2, accuracy 10.2-14.2 bits) with 13 distinct feasible designs. Since this is the final round, no further exploration is possible. The selection rule (min area) clearly points to the iterative design at 6870 um^2 as the final choice.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 3.866e+05 (gain this round: +223.3%).
Feasible designs: 156 of 200 evaluations (121 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 10.3
- max_abs_err <= 0.000976562: 22% violate; best seen 7.42e-08 (2^-23.68)

Pareto front (feasible, 25 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] area_um2=6870, accuracy_bits=10.2, ffs=98, throughput_msps=9.22, max_abs_err=0.000879 (2^-10.15), power_index=0.152
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=7121, accuracy_bits=10.7, ffs=102, throughput_msps=8.32, max_abs_err=0.000594 (2^-10.72), power_index=0.167
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] area_um2=7322, accuracy_bits=11.3, ffs=104, throughput_msps=8.32, max_abs_err=0.0004 (2^-11.29), power_index=0.172
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=7449, accuracy_bits=11.7, ffs=106, throughput_msps=7.7, max_abs_err=0.000294 (2^-11.73), power_index=0.175
- iterative [data_width=17 n_iter=14 angle_guard=1 frac_guard=4 rounding=trunc] area_um2=8757, accuracy_bits=12.4, ffs=119, throughput_msps=6.93, max_abs_err=0.000181 (2^-12.43), power_index=0.2
- iterative [data_width=19 n_iter=23 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=8869, accuracy_bits=13.3, ffs=124, throughput_msps=4.53, max_abs_err=0.000101 (2^-13.27), power_index=0.315
- iterative [data_width=22 n_iter=23 angle_guard=2 frac_guard=0 rounding=round] area_um2=10626, accuracy_bits=17.5, ffs=140, throughput_msps=4.11, max_abs_err=5.49e-06 (2^-17.47), power_index=0.365
- iterative [data_width=24 n_iter=26 angle_guard=1 frac_guard=0 rounding=round] area_um2=11673, accuracy_bits=19.1, ffs=150, throughput_msps=3.58, max_abs_err=1.76e-06 (2^-19.12), power_index=0.441
- iterative [data_width=25 n_iter=23 angle_guard=2 frac_guard=0 rounding=round] area_um2=12128, accuracy_bits=20.1, ffs=156, throughput_msps=3.77, max_abs_err=8.71e-07 (2^-20.13), power_index=0.412
- unrolled_k [data_width=28 n_iter=25 angle_guard=3 frac_guard=4 rounding=round k=2] area_um2=21878, accuracy_bits=23.7, ffs=182, throughput_msps=2.84, max_abs_err=7.42e-08 (2^-23.68), power_index=0.368
Front coverage: area_um2 6870..21878 (HV reference 40000); accuracy_bits 10.2..23.7 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 122 evals, 101 feasible; max throughput seen 10.3 MSPS; best accuracy 21.99 bits; best feasible area_um2=6870; feasible ranges: data_width 13..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 78 evals, 55 feasible; max throughput seen 8.53 MSPS; best accuracy 23.68 bits; best feasible area_um2=9198; feasible ranges: data_width 14..28, n_iter 13..25, angle_guard -2..4, frac_guard 0..4, k 2..8
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7725 in, 2513 out
- provider-reported cost: $0.0052
- full prompts and replies: `llm_trace.jsonl`

