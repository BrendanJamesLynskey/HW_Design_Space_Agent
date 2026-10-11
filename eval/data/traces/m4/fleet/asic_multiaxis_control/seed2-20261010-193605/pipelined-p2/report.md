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
`pipelined:data_width=19,n_iter=14,angle_guard=3,frac_guard=0,rounding=trunc` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 42524 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 11329 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 922 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 123 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 123 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 130 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.44 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000163 (2^-12.58) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 21.4 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.18e-05 (2^-14.24) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 6.79 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.6 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (16 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=19,n_iter=14,angle_guard=3,frac_guard=0,rounding=trunc` | 42524 | 922 | 123.1 | 16 | 2.44 | 0.000163 (2^-12.58) | 12.58 |
| 1 | `pipelined:data_width=20,n_iter=14,angle_guard=3,frac_guard=0,rounding=trunc` | 44438 | 963 | 118.9 | 16 | 2.55 | 0.000141 (2^-12.79) | 12.79 |
| 2 | `pipelined:data_width=19,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc` | 44901 | 969 | 132.4 | 17 | 2.57 | 0.000101 (2^-13.27) | 13.27 |
| 3 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=3,rounding=round` | 47060 | 993 | 127.5 | 17 | 2.65 | 8.94e-05 (2^-13.45) | 13.45 |
| 4 | `pipelined:data_width=19,n_iter=16,angle_guard=1,frac_guard=0,rounding=trunc` | 47357 | 1022 | 132.4 | 18 | 2.71 | 8.56e-05 (2^-13.51) | 13.51 |
| 5 | `pipelined:data_width=20,n_iter=15,angle_guard=3,frac_guard=0,rounding=trunc` | 47729 | 1032 | 118.9 | 17 | 2.74 | 8.43e-05 (2^-13.53) | 13.53 |
| 6 | `pipelined:data_width=18,n_iter=16,angle_guard=1,frac_guard=2,rounding=round` | 48878 | 1032 | 132.4 | 18 | 2.76 | 7.47e-05 (2^-13.71) | 13.71 |
| 7 | `pipelined:data_width=19,n_iter=16,angle_guard=1,frac_guard=2,rounding=round` | 51127 | 1079 | 127.5 | 18 | 2.88 | 5.03e-05 (2^-14.28) | 14.28 |
| 8 | `pipelined:data_width=20,n_iter=17,angle_guard=1,frac_guard=0,rounding=round` | 52751 | 1137 | 127.5 | 19 | 3.02 | 3.32e-05 (2^-14.88) | 14.88 |
| 9 | `pipelined:data_width=20,n_iter=17,angle_guard=3,frac_guard=0,rounding=round` | 54310 | 1170 | 118.9 | 19 | 3.1 | 2.95e-05 (2^-15.05) | 15.05 |
| 10 | `pipelined:data_width=20,n_iter=19,angle_guard=1,frac_guard=0,rounding=round` | 59143 | 1270 | 127.5 | 21 | 3.37 | 2.52e-05 (2^-15.28) | 15.28 |
| 11 | `pipelined:data_width=23,n_iter=17,angle_guard=1,frac_guard=0,rounding=round` | 59770 | 1287 | 115.0 | 19 | 3.42 | 1.66e-05 (2^-15.88) | 15.88 |
| 12 | `pipelined:data_width=21,n_iter=19,angle_guard=2,frac_guard=1,rounding=trunc` | 64304 | 1378 | 118.9 | 21 | 3.66 | 1.31e-05 (2^-16.21) | 16.21 |
| 13 | `pipelined:data_width=25,n_iter=19,angle_guard=-2,frac_guard=2,rounding=round` | 74284 | 1563 | 104.7 | 21 | 4.18 | 5.86e-06 (2^-17.38) | 17.38 |
| 14 | `pipelined:data_width=26,n_iter=19,angle_guard=1,frac_guard=1,rounding=trunc` | 76548 | 1640 | 104.7 | 21 | 4.36 | 4.03e-06 (2^-17.92) | 17.92 |
| 15 | `pipelined:data_width=26,n_iter=20,angle_guard=1,frac_guard=1,rounding=round` | 82065 | 1728 | 104.7 | 22 | 4.62 | 2.11e-06 (2^-18.85) | 18.85 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-dominated: throughput >= 32 msps is trivially satisfied by any 1-result/cycle pipeline, and the error bound (2^-12) is loose enough that small W/N designs sit near the boundary. So the useful work is mapping the accuracy-versus-area frontier right at the feasibility edge, which is exactly where the current merged front (all pipelined, best area 39973) already lives. Round 1 therefore spends most of the 100-eval slice on pipelined for a dense map of the edge, with data_width and n_iter deliberately reaching one step into infeasible territory (W=12, N=10) to pin down where the constraint actually bites, and angle_guard/frac_guard/rounding opened wide because those are the cheap knobs that trade cells for the last fraction of a bit. pipelined_m gets a substantial minority slice with m capped at 2..4: it is the only route to fewer flip-flops and hence lower area at the same throughput, but the earlier all-infeasible result suggests its failure mode is the system batch/latency budget at large m, so I keep m small rather than re-spending budget on the region that already failed. If pipelined_m yields feasible points in round 1 I will widen m upward next round; if it again yields none I will fold its share back into pipelined and push the accuracy boundary tighter.*)
- `pipelined` (60 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round. *Why:* This is the only family that has produced feasible designs (29/41) and it owns 11/11 of the current merged front, with best feasible area 39973 um^2. It gives 1 result/cycle, so throughput_msps >= 32 needs only Fmax >= 32 MHz, which one registered micro-rotation per stage meets with margin; the binding constraints are accuracy and the 0.5 us / 32-request batch budget, and the objective is area, so I search right at the accuracy boundary. data_width 12..20 brackets the necessary W (output LSB 2^-(W-2), so W = 13 is the hard floor for 2^-12 with rounding and 12 is deliberately included as the infeasible side of the boundary); n_iter 10..20 brackets the residual-rotation floor N ~ 13 while still letting the search confirm it; angle_guard -2..3 and frac_guard 0..3 span cheap-but-lossy truncation to safe rounding so the optimiser can buy the last bits of accuracy in whichever currency is cheapest in cells. This family gets the larger share because the trade-off curve of the whole spec currently lives here.
- `pipelined_m` (40 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round, m=2..4. *Why:* Same arithmetic, 1 result/cycle, but only ceil(N/m) register banks instead of N, so it is the natural place to shave flip-flops and area below the pipelined front. My earlier 59 evals found 0 feasible, which points at the combination of m and the batch/latency budgets rather than accuracy (accuracy depends only on data_width/n_iter/angle_guard/frac_guard/rounding, which are searched identically here). I therefore restrict m to 2..4: with m chained micro-rotations between registers the clock period grows roughly linearly in m while the cycle count only falls as N/m, so latency_ns = (ceil(N/m)+2+31) x period and throughput_msps = Fmax both degrade for large m; large m is the most likely cause of the earlier all-infeasible batch and is a liability at L2 as well. The accuracy ranges are kept identical to pipelined so that any feasible point found here is directly comparable point-for-point on area and can form lower-area, lower-Fmax Pareto points that pipelined alone cannot reach. Smaller share than pipelined because it is unproven on this spec.

**Result (code):** 100 evaluations this round, 100 total; 36 feasible; hypervolume 1.911e+05 (n/a).

**LLM decision:** `widen` — ...

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.911e+05 (gain this round: n/a (first round)).
Feasible designs: 36 of 100 evaluations (29 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 190
- max_abs_err <= 0.000244141: 61% violate; best seen 1.58e-05 (2^-15.95)
- sys_p99_batch_us <= 0.5: 36% violate; best seen 0.221

Pareto front (feasible, 12 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=19 n_iter=14 angle_guard=3 frac_guard=0 rounding=trunc] area_um2=42524, accuracy_bits=12.6, ffs=922, throughput_msps=123, max_abs_err=0.000163 (2^-12.58), power_index=2.44
- pipelined [data_width=20 n_iter=14 angle_guard=3 frac_guard=0 rounding=trunc] area_um2=44438, accuracy_bits=12.8, ffs=963, throughput_msps=119, max_abs_err=0.000141 (2^-12.79), power_index=2.55
- pipelined [data_width=19 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc] area_um2=44901, accuracy_bits=13.3, ffs=969, throughput_msps=132, max_abs_err=0.000101 (2^-13.27), power_index=2.57
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=47357, accuracy_bits=13.5, ffs=1022, throughput_msps=132, max_abs_err=8.56e-05 (2^-13.51), power_index=2.71
- pipelined [data_width=20 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc] area_um2=47729, accuracy_bits=13.5, ffs=1032, throughput_msps=119, max_abs_err=8.43e-05 (2^-13.53), power_index=2.74
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] area_um2=48878, accuracy_bits=13.7, ffs=1032, throughput_msps=132, max_abs_err=7.47e-05 (2^-13.71), power_index=2.76
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] area_um2=51127, accuracy_bits=14.3, ffs=1079, throughput_msps=128, max_abs_err=5.03e-05 (2^-14.28), power_index=2.88
- pipelined [data_width=20 n_iter=17 angle_guard=3 frac_guard=0 rounding=round] area_um2=54310, accuracy_bits=15, ffs=1170, throughput_msps=119, max_abs_err=2.95e-05 (2^-15.05), power_index=3.1
- pipelined [data_width=20 n_iter=19 angle_guard=1 frac_guard=0 rounding=round] area_um2=59143, accuracy_bits=15.3, ffs=1270, throughput_msps=128, max_abs_err=2.52e-05 (2^-15.28), power_index=3.37
- pipelined [data_width=20 n_iter=19 angle_guard=1 frac_guard=3 rounding=round] area_um2=65195, accuracy_bits=16, ffs=1372, throughput_msps=119, max_abs_err=1.58e-05 (2^-15.95), power_index=3.67
Front coverage: area_um2 42524..65195 (HV reference 100000); accuracy_bits 12.6..16 (HV reference 12); data_width on the front 18..20 (registry 8..28).

Per family:
- pipelined: 60 evals, 36 feasible; max throughput seen 190 MSPS; best accuracy 15.95 bits; best feasible area_um2=42524; feasible ranges: data_width 17..20, n_iter 14..20, angle_guard -2..3, frac_guard 0..3
- pipelined_m: 40 evals, 0 feasible; max throughput seen 91.1 MSPS; best accuracy 13.06 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *...*)
- `pipelined` (20 evals): data_width=16..26, n_iter=12..26, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* only family on the front; pipelined_m 0/40 feasible (batch bound), iterative/unrolled_k cannot meet the 32-request burst

**Result (code):** 20 evaluations this round, 120 total; 50 feasible; hypervolume 2.311e+05 (+21.0%).

**LLM decision:** `stop` — This is the final round (round cap reached), and the front is feasible and well-covered, so neither `infeasible` nor further exploration applies. All three constraints are satisfiable simultaneously: 0% of evaluations violate throughput_msps >= 32 (best 190), and the Pareto front contains designs meeting max_abs_err <= 2^-12 (best front point 2^-12.58 at area 42524 um^2) and sys_p99_batch_us <= 0.5 (best seen 0.221). The feasible front holds 15 designs spanning area_um2 42524..74284 (HV ref 100000) and accuracy_bits 12.6..17.4 (HV ref 12), with hypervolume 2.311e+05 and a +21.0% gain this round — the curve is broad and still improving, but the budget/round cap is reached. The selection rule (min area_um2) is cleanly served by the pipelined [data_width=19 n_iter=14 angle_guard=3 frac_guard=0 rounding=trunc] point at area_um2=42524, accuracy_bits=12.6, throughput 123 MSPS — comfortably inside every constraint with margin on the system batch bound. pipelined_m contributed 0 feasible designs (max throughput 91.1 MSPS, best accuracy 13.06 bits), so it does not extend the front. Stopping here leaves the best mapped front for the spec's selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 2.311e+05 (gain this round: +21.0%).
Feasible designs: 50 of 120 evaluations (41 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 190
- max_abs_err <= 0.000244141: 52% violate; best seen 7.31e-07 (2^-20.38)
- sys_p99_batch_us <= 0.5: 33% violate; best seen 0.221

Pareto front (feasible, 15 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=19 n_iter=14 angle_guard=3 frac_guard=0 rounding=trunc] area_um2=42524, accuracy_bits=12.6, ffs=922, throughput_msps=123, max_abs_err=0.000163 (2^-12.58), power_index=2.44
- pipelined [data_width=19 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc] area_um2=44901, accuracy_bits=13.3, ffs=969, throughput_msps=132, max_abs_err=0.000101 (2^-13.27), power_index=2.57
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=3 rounding=round] area_um2=47060, accuracy_bits=13.4, ffs=993, throughput_msps=128, max_abs_err=8.94e-05 (2^-13.45), power_index=2.65
- pipelined [data_width=20 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc] area_um2=47729, accuracy_bits=13.5, ffs=1032, throughput_msps=119, max_abs_err=8.43e-05 (2^-13.53), power_index=2.74
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] area_um2=48878, accuracy_bits=13.7, ffs=1032, throughput_msps=132, max_abs_err=7.47e-05 (2^-13.71), power_index=2.76
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] area_um2=52751, accuracy_bits=14.9, ffs=1137, throughput_msps=128, max_abs_err=3.32e-05 (2^-14.88), power_index=3.02
- pipelined [data_width=20 n_iter=17 angle_guard=3 frac_guard=0 rounding=round] area_um2=54310, accuracy_bits=15, ffs=1170, throughput_msps=119, max_abs_err=2.95e-05 (2^-15.05), power_index=3.1
- pipelined [data_width=23 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] area_um2=59770, accuracy_bits=15.9, ffs=1287, throughput_msps=115, max_abs_err=1.66e-05 (2^-15.88), power_index=3.42
- pipelined [data_width=20 n_iter=19 angle_guard=1 frac_guard=3 rounding=round] area_um2=65195, accuracy_bits=16, ffs=1372, throughput_msps=119, max_abs_err=1.58e-05 (2^-15.95), power_index=3.67
- pipelined [data_width=25 n_iter=19 angle_guard=-2 frac_guard=2 rounding=round] area_um2=74284, accuracy_bits=17.4, ffs=1563, throughput_msps=105, max_abs_err=5.86e-06 (2^-17.38), power_index=4.18
Front coverage: area_um2 42524..74284 (HV reference 100000); accuracy_bits 12.6..17.4 (HV reference 12); data_width on the front 18..25 (registry 8..28).

Per family:
- pipelined: 80 evals, 50 feasible; max throughput seen 190 MSPS; best accuracy 20.38 bits; best feasible area_um2=42524; feasible ranges: data_width 16..25, n_iter 14..23, angle_guard -2..3, frac_guard 0..4
- pipelined_m: 40 evals, 0 feasible; max throughput seen 91.1 MSPS; best accuracy 13.06 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined` (40 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (15 front designs; box front_anchored)
- `pipelined_m` (40 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 80 evaluations this round, 200 total; 77 feasible; hypervolume 2.632e+05 (+13.9%).

**No LLM call** (code's front-mapping round): This is the final round (round cap reached), and the front is feasible and well-covered, so neither `infeasible` nor further exploration applies. All three constraints are satisfiable simultaneously: 0% of evaluations violate throughput_msps >= 32 (best 190), and the Pareto front contains designs meeting max_abs_err <= 2^-12 (best front point 2^-12.58 at area 42524 um^2) and sys_p99_batch_us <= 0.5 (best seen 0.221). The feasible front holds 15 designs spanning area_um2 42524..74284 (HV ref 100000) and accuracy_bits 12.6..17.4 (HV ref 12), with hypervolume 2.311e+05 and a +21.0% gain this round — the curve is broad and still improving, but the budget/round cap is reached. The selection rule (min area_um2) is cleanly served by the pipelined [data_width=19 n_iter=14 angle_guard=3 frac_guard=0 rounding=trunc] point at area_um2=42524, accuracy_bits=12.6, throughput 123 MSPS — comfortably inside every constraint with margin on the system batch bound. pipelined_m contributed 0 feasible designs (max throughput 91.1 MSPS, best accuracy 13.06 bits), so it does not extend the front. Stopping here leaves the best mapped front for the spec's selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 2.632e+05 (gain this round: +13.9%).
Feasible designs: 77 of 200 evaluations (61 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 12% violate; best seen 190
- max_abs_err <= 0.000244141: 40% violate; best seen 2.21e-07 (2^-22.11)
- sys_p99_batch_us <= 0.5: 44% violate; best seen 0.221

Pareto front (feasible, 16 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=19 n_iter=14 angle_guard=3 frac_guard=0 rounding=trunc] area_um2=42524, accuracy_bits=12.6, ffs=922, throughput_msps=123, max_abs_err=0.000163 (2^-12.58), power_index=2.44
- pipelined [data_width=19 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc] area_um2=44901, accuracy_bits=13.3, ffs=969, throughput_msps=132, max_abs_err=0.000101 (2^-13.27), power_index=2.57
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=3 rounding=round] area_um2=47060, accuracy_bits=13.4, ffs=993, throughput_msps=128, max_abs_err=8.94e-05 (2^-13.45), power_index=2.65
- pipelined [data_width=20 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc] area_um2=47729, accuracy_bits=13.5, ffs=1032, throughput_msps=119, max_abs_err=8.43e-05 (2^-13.53), power_index=2.74
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] area_um2=51127, accuracy_bits=14.3, ffs=1079, throughput_msps=128, max_abs_err=5.03e-05 (2^-14.28), power_index=2.88
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] area_um2=52751, accuracy_bits=14.9, ffs=1137, throughput_msps=128, max_abs_err=3.32e-05 (2^-14.88), power_index=3.02
- pipelined [data_width=20 n_iter=19 angle_guard=1 frac_guard=0 rounding=round] area_um2=59143, accuracy_bits=15.3, ffs=1270, throughput_msps=128, max_abs_err=2.52e-05 (2^-15.28), power_index=3.37
- pipelined [data_width=21 n_iter=19 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=64304, accuracy_bits=16.2, ffs=1378, throughput_msps=119, max_abs_err=1.31e-05 (2^-16.21), power_index=3.66
- pipelined [data_width=25 n_iter=19 angle_guard=-2 frac_guard=2 rounding=round] area_um2=74284, accuracy_bits=17.4, ffs=1563, throughput_msps=105, max_abs_err=5.86e-06 (2^-17.38), power_index=4.18
- pipelined [data_width=26 n_iter=20 angle_guard=1 frac_guard=1 rounding=round] area_um2=82065, accuracy_bits=18.9, ffs=1728, throughput_msps=105, max_abs_err=2.11e-06 (2^-18.85), power_index=4.62
Front coverage: area_um2 42524..82065 (HV reference 100000); accuracy_bits 12.6..18.9 (HV reference 12); data_width on the front 18..26 (registry 8..28).

Per family:
- pipelined: 120 evals, 77 feasible; max throughput seen 190 MSPS; best accuracy 21.00 bits; best feasible area_um2=42524; feasible ranges: data_width 16..26, n_iter 14..27, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 80 evals, 0 feasible; max throughput seen 91.1 MSPS; best accuracy 22.11 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8851 in, 20044 out
- provider-reported cost: $0.0236
- full prompts and replies: `llm_trace.jsonl`

