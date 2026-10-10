# DSE run: asic_multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_multiaxis_control: Shared sin/cos unit in sky130 standard cells for a 16-axis motor-control loop: a 1 MHz control tick issues 32 requests at once; all 32 results must be back within 0.5 us of the tick (p99 over ticks). Max error <= 2^-12. Minimise area.
  target: asic-sky130hd
  constraint: throughput_msps >= 32
  constraint: max_abs_err <= 0.000244141
  constraint: sys_p99_batch_us <= 0.5
  objective: min area_um2 (HV ref 100000)
  objective: max accuracy_bits (HV ref 12)
  select: min area_um2
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average)
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 39973 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10649 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 867 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 132 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 132 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 121 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.00017 (2^-12.53) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 11.1 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.25e-05 (2^-14.22) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.44 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (16 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 39973 | 867 | 132.4 | 16 | 2.3 | 0.00017 (2^-12.53) | 12.53 |
| 1 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc` | 41162 | 891 | 132.4 | 16 | 2.36 | 0.000166 (2^-12.55) | 12.55 |
| 2 | `pipelined:data_width=19,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 41887 | 908 | 127.5 | 16 | 2.41 | 0.000142 (2^-12.78) | 12.78 |
| 3 | `pipelined:data_width=21,n_iter=14,angle_guard=-1,frac_guard=0,rounding=round` | 43800 | 950 | 127.5 | 16 | 2.51 | 0.000137 (2^-12.84) | 12.84 |
| 4 | `pipelined:data_width=20,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc` | 44350 | 960 | 127.5 | 16 | 2.54 | 0.000135 (2^-12.86) | 12.86 |
| 5 | `pipelined:data_width=21,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 45075 | 977 | 123.1 | 16 | 2.59 | 0.000127 (2^-12.95) | 12.95 |
| 6 | `pipelined:data_width=21,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 45713 | 991 | 118.9 | 16 | 2.62 | 0.000127 (2^-12.95) | 12.95 |
| 7 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 45892 | 991 | 132.4 | 18 | 2.63 | 8.35e-05 (2^-13.55) | 13.55 |
| 8 | `pipelined:data_width=18,n_iter=16,angle_guard=3,frac_guard=1,rounding=round` | 48966 | 1036 | 127.5 | 18 | 2.77 | 6.51e-05 (2^-13.91) | 13.91 |
| 9 | `pipelined:data_width=18,n_iter=16,angle_guard=3,frac_guard=3,rounding=round` | 51721 | 1091 | 127.5 | 18 | 2.92 | 4.52e-05 (2^-14.43) | 14.43 |
| 10 | `pipelined:data_width=21,n_iter=16,angle_guard=3,frac_guard=0,rounding=round` | 53217 | 1148 | 115.0 | 18 | 3.05 | 3.65e-05 (2^-14.74) | 14.74 |
| 11 | `pipelined:data_width=20,n_iter=18,angle_guard=1,frac_guard=0,rounding=round` | 55947 | 1203 | 127.5 | 20 | 3.2 | 2.9e-05 (2^-15.07) | 15.07 |
| 12 | `pipelined:data_width=20,n_iter=25,angle_guard=2,frac_guard=0,rounding=round` | 79479 | 1696 | 123.1 | 27 | 4.51 | 2.17e-05 (2^-15.49) | 15.49 |
| 13 | `pipelined:data_width=20,n_iter=25,angle_guard=2,frac_guard=1,rounding=round` | 82775 | 1743 | 123.1 | 27 | 4.66 | 1.37e-05 (2^-16.15) | 16.15 |
| 14 | `pipelined:data_width=25,n_iter=23,angle_guard=-1,frac_guard=0,rounding=round` | 85762 | 1832 | 111.3 | 25 | 4.87 | 2e-06 (2^-18.93) | 18.93 |
| 15 | `pipelined:data_width=25,n_iter=23,angle_guard=0,frac_guard=0,rounding=round` | 86826 | 1854 | 111.3 | 25 | 4.93 | 1.33e-06 (2^-19.52) | 19.52 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The merged front is 100% pipelined and pipelined is 39/53 feasible, so the front I must cover is a pipelined area-vs-accuracy curve; most of the budget goes there. The selection rule is min area_um2 under max_abs_err <= 2^-12 and the 32-results-per-0.5-us burst bound, so I want dense coverage of the small-area feasible corner (the likely winner) plus enough of the higher-W/N accuracy region to fill the hypervolume box out to the area reference point. pipelined_m gets a smaller share purely as a bounded probe at small m, where it could undercut pipelined on area if it meets the burst bound; it has shown nothing yet, so I cap its share and will reallocate if it stays infeasible.*)
- `pipelined` (68 evals): data_width=12..22, n_iter=8..22, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round. *Why:* Only family with any feasible designs so far (39/53 feasible, and every one of the 12 designs on the merged front). The spec's binding constraints are accuracy (max_abs_err <= 2^-12) and the burst constraint (32 results in 0.5 us), and a 1-result/cycle pipelined unit with N+2 latency clears the burst easily at its Fmax. So this is where the area-vs-accuracy trade-off actually lives and where hypervolume is won or lost. Ranges: data_width 12..22 and n_iter 8..22 bracket both ends of the front - the min-area feasible corner needs W just large enough that the 2^-(W-2) output LSB plus rounding does not exceed 2^-12, while W/N up to ~22 supplies the high-accuracy_bits end that the HV reference (accuracy 12) rewards without pushing area past the area reference point. angle_guard -2..3 and frac_guard 0..3 let the search buy accuracy with guard bits instead of full data_width when that is cheaper, and negative angle_guard is the cheapest area lever if accuracy survives. rounding trunc|round is nearly free to try and round is worth several bits of LSB error.
- `pipelined_m` (32 evals): data_width=13..20, n_iter=8..20, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, m=2..4. *Why:* Still 0/47 feasible, so it is either dead or it was searched in the wrong corner. It computes the same bits as pipelined for the same accuracy parameters, so the error constraint cannot be what kills it; the plausible failure mode is Fmax (and hence the 0.5 us / 32-result burst budget) collapsing as m grows, since m micro-rotations sit in one combinational path. That points at small m, not the whole 2..8 range, so I restrict m to 2..4 and keep data_width/n_iter in the low-to-mid band (13..20 / 8..20) where area - its only reason to exist - is smallest. If registering every 2-3 stages keeps Fmax high enough to still fit latency+31 cycles inside 0.5 us, pipelined_m with m=2-3 would have fewer pipeline FFs than pipelined at the same W/N and could take the min-area selection; that upside is worth ~1/3 of the round. If this share returns 0 feasible again, drop the family and put the remaining round into full-range pipelined front mapping.

**Result (code):** 100 evaluations this round, 100 total; 35 feasible; hypervolume 1.462e+05 (n/a).

**LLM decision:** `map_front` — Round 1 leaves the front entirely inside one family and only partially spanning the objective ranges, so the biggest marginal HV gain now is to let code sweep the full registry ranges of that family seeded with the round-1 front (this is also the reserved front-mapping step).

Evidence:
- Family: all 11 front designs are `pipelined`; `pipelined_m` (32 evals) produced 0 feasible designs, and the multi-cycle families cannot reach the system constraint at all — 32 requests in 0.5 us needs ~64 results/us, which for `iterative` (N+3 cycles/result) would need >1 GHz and for `unrolled_k` a clock its chained datapath cannot hit; so no `add_family` candidate can land on the front. The front family is pipelined.
- Coverage is partial: area_um2 39973..53217 vs HV ref 100000 (~13% of the axis), accuracy_bits 12.5..14.7 vs HV ref 12, while round 1 only sampled n_iter 14..20 and data_width 17..22. The high-accuracy end (larger n_iter/data_width) and the low-area corner (accuracy pushed down toward the 2^-12 constraint, which the front currently overshoots at 12.5 bits) both look under-mapped.
- Both objectives are estimates/exact from code and the front is still cheap to expand: 100 of 200 evals remain, and mapping the whole pipelined front with NSGA-II seeded by the current front can extend it at both ends and lift hypervolume, which also protects the min-area selection corner. `refine` would over-concentrate on the current cluster, and the front is clearly not converged enough to `stop`.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.462e+05 (gain this round: n/a (first round)).
Feasible designs: 35 of 100 evaluations (27 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 190
- max_abs_err <= 0.000244141: 53% violate; best seen 3.65e-05 (2^-14.74)
- sys_p99_batch_us <= 0.5: 29% violate; best seen 0.227

Pareto front (feasible, 11 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.5, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53), power_index=2.3
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=41162, accuracy_bits=12.6, ffs=891, throughput_msps=132, max_abs_err=0.000166 (2^-12.55), power_index=2.36
- pipelined [data_width=19 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=41887, accuracy_bits=12.8, ffs=908, throughput_msps=128, max_abs_err=0.000142 (2^-12.78), power_index=2.41
- pipelined [data_width=21 n_iter=14 angle_guard=-1 frac_guard=0 rounding=round] area_um2=43800, accuracy_bits=12.8, ffs=950, throughput_msps=128, max_abs_err=0.000137 (2^-12.84), power_index=2.51
- pipelined [data_width=20 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=44350, accuracy_bits=12.9, ffs=960, throughput_msps=128, max_abs_err=0.000135 (2^-12.86), power_index=2.54
- pipelined [data_width=21 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=45713, accuracy_bits=12.9, ffs=991, throughput_msps=119, max_abs_err=0.000127 (2^-12.95), power_index=2.62
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=1 rounding=round] area_um2=48966, accuracy_bits=13.9, ffs=1036, throughput_msps=128, max_abs_err=6.51e-05 (2^-13.91), power_index=2.77
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=3 rounding=round] area_um2=51721, accuracy_bits=14.4, ffs=1091, throughput_msps=128, max_abs_err=4.52e-05 (2^-14.43), power_index=2.92
- pipelined [data_width=21 n_iter=16 angle_guard=3 frac_guard=0 rounding=round] area_um2=53217, accuracy_bits=14.7, ffs=1148, throughput_msps=115, max_abs_err=3.65e-05 (2^-14.74), power_index=3.05
Front coverage: area_um2 39973..53217 (HV reference 100000); accuracy_bits 12.5..14.7 (HV reference 12); data_width on the front 18..21 (registry 8..28).

Per family:
- pipelined: 68 evals, 35 feasible; max throughput seen 190 MSPS; best accuracy 14.74 bits; best feasible area_um2=39973; feasible ranges: data_width 17..22, n_iter 14..20, angle_guard -2..3, frac_guard 0..3
- pipelined_m: 32 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 13.64 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `pipelined` (10 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (11 front designs; box front_anchored)
- `pipelined_m` (10 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 20 evaluations this round, 120 total; 41 feasible; hypervolume 2.092e+05 (+43.1%).

**LLM decision:** `map_front` — The feasible front is still improving strongly (+43.1% HV this round) but is sparse and does not span the objectives' useful ranges: only 12 designs, with a large hole between area 53217 (14.7 bits) and area 86826 (19.5 bits), and the front's largest area (86826) falls short of the HV reference area (100000) while the best accuracy seen anywhere is 21.37 bits versus the front's top of 19.5 bits. Filling that middle band and extending the high-accuracy end is where the remaining HV is: e.g. a design near area 60000/16 bits would dominate a wide strip currently covered only by the 86826-area design. Only `pipelined` is on the front (`pipelined_m` was 0/42 feasible, max throughput 96 MSPS), so a seeded NSGA-II coverage search over pipelined's full ranges is the right use of the remaining ~80 evaluations before the run ends.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 2.092e+05 (gain this round: +43.1%).
Feasible designs: 41 of 120 evaluations (33 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 5% violate; best seen 190
- max_abs_err <= 0.000244141: 48% violate; best seen 3.7e-07 (2^-21.37)
- sys_p99_batch_us <= 0.5: 35% violate; best seen 0.227

Pareto front (feasible, 12 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.5, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53), power_index=2.3
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=41162, accuracy_bits=12.6, ffs=891, throughput_msps=132, max_abs_err=0.000166 (2^-12.55), power_index=2.36
- pipelined [data_width=19 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=41887, accuracy_bits=12.8, ffs=908, throughput_msps=128, max_abs_err=0.000142 (2^-12.78), power_index=2.41
- pipelined [data_width=20 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=44350, accuracy_bits=12.9, ffs=960, throughput_msps=128, max_abs_err=0.000135 (2^-12.86), power_index=2.54
- pipelined [data_width=21 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=45075, accuracy_bits=12.9, ffs=977, throughput_msps=123, max_abs_err=0.000127 (2^-12.95), power_index=2.59
- pipelined [data_width=21 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=45713, accuracy_bits=12.9, ffs=991, throughput_msps=119, max_abs_err=0.000127 (2^-12.95), power_index=2.62
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=3 rounding=round] area_um2=51721, accuracy_bits=14.4, ffs=1091, throughput_msps=128, max_abs_err=4.52e-05 (2^-14.43), power_index=2.92
- pipelined [data_width=21 n_iter=16 angle_guard=3 frac_guard=0 rounding=round] area_um2=53217, accuracy_bits=14.7, ffs=1148, throughput_msps=115, max_abs_err=3.65e-05 (2^-14.74), power_index=3.05
- pipelined [data_width=25 n_iter=23 angle_guard=0 frac_guard=0 rounding=round] area_um2=86826, accuracy_bits=19.5, ffs=1854, throughput_msps=111, max_abs_err=1.33e-06 (2^-19.52), power_index=4.93
Front coverage: area_um2 39973..86826 (HV reference 100000); accuracy_bits 12.5..19.5 (HV reference 12); data_width on the front 18..25 (registry 8..28).

Per family:
- pipelined: 78 evals, 41 feasible; max throughput seen 190 MSPS; best accuracy 21.37 bits; best feasible area_um2=39973; feasible ranges: data_width 17..26, n_iter 14..29, angle_guard -2..3, frac_guard 0..3
- pipelined_m: 42 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 17.08 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined` (40 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (12 front designs; box front_anchored)
- `pipelined_m` (40 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 80 evaluations this round, 200 total; 66 feasible; hypervolume 2.283e+05 (+9.1%).

**LLM decision:** `stop` — Budget is exhausted (200/200 evals, round 3 of 4) and the front is both feasible and still improving (+9.1% HV this round), so no further exploration is possible or needed. All three constraints are met by the front: throughput best seen 190 MSPS vs >=32, max_abs_err best 1.15e-07 vs <=2.44e-04, sys_p99_batch_us best 0.227 vs <=0.5. The min-area selection rule picks pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] at area_um2=39973, accuracy_bits=12.5 (max_abs_err=1.7e-04, inside the 2^-12 limit), throughput 132 MSPS, power_index 2.3. Coverage is reasonable (area 39973..86826 against HV ref 100000; accuracy 12.5..19.5 against ref 12; data_width 18..25 of registry 8..28), and pipelined_m contributed 0 feasible designs, so no unexplored family remains. Caveat to carry into L2: the cheapest front points pass the sys_p99_batch bound only with margin (0.227 vs 0.5 at best), so the L2 re-selection may drop the very smallest designs; that is handled by the post-selection simulation, not by more exploration.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 2.283e+05 (gain this round: +9.1%).
Feasible designs: 66 of 200 evaluations (49 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 10% violate; best seen 190
- max_abs_err <= 0.000244141: 35% violate; best seen 1.15e-07 (2^-23.05)
- sys_p99_batch_us <= 0.5: 48% violate; best seen 0.227

Pareto front (feasible, 16 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.5, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53), power_index=2.3
- pipelined [data_width=19 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=41887, accuracy_bits=12.8, ffs=908, throughput_msps=128, max_abs_err=0.000142 (2^-12.78), power_index=2.41
- pipelined [data_width=21 n_iter=14 angle_guard=-1 frac_guard=0 rounding=round] area_um2=43800, accuracy_bits=12.8, ffs=950, throughput_msps=128, max_abs_err=0.000137 (2^-12.84), power_index=2.51
- pipelined [data_width=21 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=45075, accuracy_bits=12.9, ffs=977, throughput_msps=123, max_abs_err=0.000127 (2^-12.95), power_index=2.59
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=1 rounding=round] area_um2=48966, accuracy_bits=13.9, ffs=1036, throughput_msps=128, max_abs_err=6.51e-05 (2^-13.91), power_index=2.77
- pipelined [data_width=21 n_iter=16 angle_guard=3 frac_guard=0 rounding=round] area_um2=53217, accuracy_bits=14.7, ffs=1148, throughput_msps=115, max_abs_err=3.65e-05 (2^-14.74), power_index=3.05
- pipelined [data_width=20 n_iter=25 angle_guard=2 frac_guard=0 rounding=round] area_um2=79479, accuracy_bits=15.5, ffs=1696, throughput_msps=123, max_abs_err=2.17e-05 (2^-15.49), power_index=4.51
- pipelined [data_width=20 n_iter=25 angle_guard=2 frac_guard=1 rounding=round] area_um2=82775, accuracy_bits=16.2, ffs=1743, throughput_msps=123, max_abs_err=1.37e-05 (2^-16.15), power_index=4.66
- pipelined [data_width=25 n_iter=23 angle_guard=0 frac_guard=0 rounding=round] area_um2=86826, accuracy_bits=19.5, ffs=1854, throughput_msps=111, max_abs_err=1.33e-06 (2^-19.52), power_index=4.93
Front coverage: area_um2 39973..86826 (HV reference 100000); accuracy_bits 12.5..19.5 (HV reference 12); data_width on the front 18..25 (registry 8..28).

Per family:
- pipelined: 118 evals, 66 feasible; max throughput seen 190 MSPS; best accuracy 23.05 bits; best feasible area_um2=39973; feasible ranges: data_width 17..26, n_iter 14..29, angle_guard -2..4, frac_guard 0..3
- pipelined_m: 82 evals, 0 feasible; max throughput seen 123 MSPS; best accuracy 20.66 bits
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 1)
- tokens: 13931 in, 19412 out
- provider-reported cost: $0.0138
- full prompts and replies: `llm_trace.jsonl`

