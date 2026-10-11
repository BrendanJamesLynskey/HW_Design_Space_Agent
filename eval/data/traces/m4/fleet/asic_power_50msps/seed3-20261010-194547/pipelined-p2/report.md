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
`pipelined_m:data_width=16,n_iter=16,angle_guard=2,frac_guard=1,rounding=round,m=2` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 34177 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 9105 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 495 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 78.8 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 78.8 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 10 | exact: schedule |
| latency_ns | 127 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.38 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000177 (2^-12.47) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 2.9 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 4.53e-05 (2^-14.43) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 0.742 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.5 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (26 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=16,angle_guard=2,frac_guard=1,rounding=round,m=2` | 34177 | 495 | 78.8 | 10 | 2.38 | 0.000177 (2^-12.47) | 12.47 |
| 1 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=1,rounding=trunc,m=2` | 36192 | 537 | 75.4 | 10 | 2.56 | 0.000104 (2^-13.23) | 13.23 |
| 2 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=2,rounding=round,m=2` | 38228 | 553 | 72.3 | 10 | 2.66 | 7.47e-05 (2^-13.71) | 13.71 |
| 3 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc,m=2` | 37823 | 558 | 72.3 | 10 | 2.67 | 6.86e-05 (2^-13.83) | 13.83 |
| 4 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=2` | 38786 | 560 | 72.3 | 10 | 2.7 | 5.46e-05 (2^-14.16) | 14.16 |
| 5 | `pipelined_m:data_width=20,n_iter=16,angle_guard=2,frac_guard=1,rounding=round,m=2` | 41251 | 598 | 66.8 | 10 | 2.88 | 3.91e-05 (2^-14.64) | 14.64 |
| 6 | `pipelined_m:data_width=20,n_iter=16,angle_guard=4,frac_guard=2,rounding=trunc,m=2` | 42373 | 625 | 62.0 | 10 | 2.99 | 3.8e-05 (2^-14.68) | 14.68 |
| 7 | `pipelined_m:data_width=19,n_iter=16,angle_guard=4,frac_guard=4,rounding=round,m=2` | 43815 | 629 | 64.3 | 10 | 3.04 | 3.52e-05 (2^-14.79) | 14.79 |
| 8 | `pipelined_m:data_width=20,n_iter=17,angle_guard=1,frac_guard=1,rounding=round,m=2` | 43984 | 659 | 69.4 | 11 | 3.13 | 2.58e-05 (2^-15.24) | 15.24 |
| 9 | `pipelined_m:data_width=19,n_iter=18,angle_guard=2,frac_guard=2,rounding=round,m=2` | 45609 | 655 | 69.4 | 11 | 3.16 | 2.34e-05 (2^-15.38) | 15.38 |
| 10 | `pipelined_m:data_width=20,n_iter=18,angle_guard=1,frac_guard=1,rounding=round,m=2` | 45747 | 659 | 69.4 | 11 | 3.18 | 2.28e-05 (2^-15.42) | 15.42 |
| 11 | `pipelined_m:data_width=20,n_iter=18,angle_guard=1,frac_guard=3,rounding=trunc,m=2` | 47117 | 688 | 64.3 | 11 | 3.3 | 2.04e-05 (2^-15.58) | 15.58 |
| 12 | `pipelined_m:data_width=20,n_iter=20,angle_guard=1,frac_guard=1,rounding=round,m=2` | 50801 | 728 | 69.4 | 12 | 3.52 | 1.75e-05 (2^-15.80) | 15.80 |
| 13 | `pipelined_m:data_width=23,n_iter=18,angle_guard=4,frac_guard=0,rounding=trunc,m=2` | 51164 | 753 | 56.1 | 11 | 3.6 | 1.07e-05 (2^-16.51) | 16.51 |
| 14 | `pipelined_m:data_width=22,n_iter=20,angle_guard=2,frac_guard=0,rounding=round,m=2` | 53385 | 781 | 62.0 | 12 | 3.74 | 6.45e-06 (2^-17.24) | 17.24 |
| 15 | `pipelined_m:data_width=22,n_iter=20,angle_guard=2,frac_guard=1,rounding=trunc,m=2` | 54749 | 798 | 62.0 | 12 | 3.83 | 6.11e-06 (2^-17.32) | 17.32 |
| 16 | `pipelined_m:data_width=22,n_iter=20,angle_guard=2,frac_guard=1,rounding=round,m=2` | 55917 | 800 | 62.0 | 12 | 3.87 | 4.46e-06 (2^-17.77) | 17.77 |
| 17 | `pipelined_m:data_width=22,n_iter=20,angle_guard=4,frac_guard=1,rounding=round,m=2` | 57325 | 820 | 57.9 | 12 | 3.97 | 4.04e-06 (2^-17.92) | 17.92 |
| 18 | `pipelined_m:data_width=22,n_iter=20,angle_guard=4,frac_guard=2,rounding=round,m=2` | 58689 | 838 | 57.9 | 12 | 4.06 | 3.15e-06 (2^-18.27) | 18.27 |
| 19 | `pipelined_m:data_width=23,n_iter=20,angle_guard=2,frac_guard=2,rounding=round,m=2` | 59487 | 849 | 59.9 | 12 | 4.11 | 2.95e-06 (2^-18.37) | 18.37 |
| 20 | `pipelined_m:data_width=24,n_iter=20,angle_guard=1,frac_guard=2,rounding=round,m=2` | 60990 | 871 | 57.9 | 12 | 4.22 | 2.62e-06 (2^-18.54) | 18.54 |
| 21 | `pipelined_m:data_width=24,n_iter=20,angle_guard=2,frac_guard=2,rounding=trunc,m=2` | 60423 | 879 | 57.9 | 12 | 4.22 | 2.57e-06 (2^-18.57) | 18.57 |
| 22 | `pipelined_m:data_width=24,n_iter=20,angle_guard=2,frac_guard=3,rounding=trunc,m=2` | 61787 | 897 | 56.1 | 12 | 4.31 | 2.46e-06 (2^-18.63) | 18.63 |
| 23 | `pipelined_m:data_width=24,n_iter=20,angle_guard=3,frac_guard=3,rounding=round,m=2` | 63761 | 908 | 56.1 | 12 | 4.4 | 2.18e-06 (2^-18.81) | 18.81 |
| 24 | `pipelined_m:data_width=24,n_iter=23,angle_guard=4,frac_guard=0,rounding=round,m=2` | 69012 | 1026 | 54.3 | 14 | 4.89 | 1.62e-06 (2^-19.24) | 19.24 |
| 25 | `pipelined_m:data_width=24,n_iter=23,angle_guard=4,frac_guard=1,rounding=round,m=2` | 71887 | 1050 | 54.3 | 14 | 5.04 | 9.35e-07 (2^-20.03) | 20.03 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Only pipelined and pipelined_m are allowed for me, and the fleet facts show the iterative/unrolled_k families are entirely infeasible (0 feasible in 100 evals) because a shared datapath cannot reach 50 MSPS. Both of my families are 1-result/cycle, so the throughput constraint is essentially free and the real fight is power_index vs accuracy_bits. pipelined_m already owns the merged front (6/9) and the best power (2.45), so it gets the larger share; pipelined keeps 40% because it still holds 3/9 front points and gives the high-Fmax end of the curve. Accuracy depends only on data_width/n_iter/angle_guard/frac_guard/rounding, so I sweep those identically in both families and let m be the pipelined_m-specific power knob. The window 13..20 for W and 12..20 for N brackets the feasible accuracy threshold (max_abs_err <= 2^-12 needs about W>=14 with round rounding and N~W) while still reaching well past 12 accuracy bits so the hypervolume against the (power 40, accuracy 12) reference is covered across the whole trade-off curve, not just the min-power corner the selection rule will pick.*)
- `pipelined_m` (60 evals): data_width=13..20, n_iter=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Best family so far: 9 feasible designs, best power_index 2.45, and 6 of the 9 merged-front points. It emits 1 result/cycle, so throughput >= 50 MSPS is trivially met (Fmax only needs to clear 50 MHz), and the register-every-m-stages knob lets us trade Fmax for FF count and power. The low-power corner is reached with large m and minimal guard bits, so I keep m fully open (2..8) and let the search push it up. data_width/n_iter start at 13/12 because the 2^-12 max-error constraint needs roughly W>=14 with round rounding plus N~W micro-rotations; the upper ends (20/20) exist to populate the higher-accuracy end of the front for hypervolume, not for the selection rule.
- `pipelined` (40 evals): data_width=13..20, n_iter=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Second-best family: 20 feasible designs, best power_index 4.04, 3 of 9 merged-front points. It is the fully-registered variant (one stage per micro-rotation), so it costs more FFs/power than pipelined_m at the same accuracy but has the shortest latency and highest Fmax. It still contributes distinct front points, so I keep a meaningful share to avoid collapsing the front onto pipelined_m alone. Same accuracy-driven W/N window (13..20 / 12..20) and full guard/rounding sweep so the two families are compared on identical accuracy settings.

**Result (code):** 100 evaluations this round, 100 total; 43 feasible; hypervolume 152.4 (n/a).

**LLM decision:** `map_front` — Constraints are reachable, so this is not infeasible: 43/100 evaluations were feasible, throughput reaches 163 MSPS (constraint 50) and max_abs_err reaches 2^-16.11 (constraint 2^-12). The feasible Pareto front is 13 designs, all pipelined_m, spanning power_index 2.38..3.73 and accuracy_bits 12.5..16.1, with data_width only 16..20 against the registry's 8..28. Because the HV reference point is (40, 12) and every front design sits at power ~2.4..3.7 (all far below 40), the hypervolume reduces to approximately sum_i (40 - p_i)*delta_a_i ~= 37*(a_max - 12): it is dominated by the accuracy extent, and a_max is only 16.1 bits. The accuracy objective is therefore mapped over only ~4 of the many bits the registry can reach (higher data_width/n_iter designs cost more power but remain non-dominated because 40 >> their power), so most of the available hypervolume is still unclaimed. map_front (NSGA-II over the full ranges of pipelined_m, seeded with the current front) is the right move: it pushes a_max upward to fill the uncovered accuracy range while retaining the min-power corner (2.38) that the min-power_index selection rule needs. Refining narrow ranges would only polish the already-dense 16..20/12..16 region, and no new family is needed: pipelined's best feasible power_index (3.86) is already worse than the front's 3.73, and iterative/unrolled_k are listed as not-yet-explored = none.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 152.4 (gain this round: n/a (first round)).
Feasible designs: 43 of 100 evaluations (34 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 29% violate; best seen 163
- max_abs_err <= 0.000244141: 41% violate; best seen 1.42e-05 (2^-16.11)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.38, accuracy_bits=12.5, area_um2=34177, ffs=495, throughput_msps=78.8, max_abs_err=0.000177 (2^-12.47)
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc m=2] power_index=2.56, accuracy_bits=13.2, area_um2=36192, ffs=537, throughput_msps=75.4, max_abs_err=0.000104 (2^-13.23)
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc m=2] power_index=2.67, accuracy_bits=13.8, area_um2=37823, ffs=558, throughput_msps=72.3, max_abs_err=6.86e-05 (2^-13.83)
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=2.7, accuracy_bits=14.2, area_um2=38786, ffs=560, throughput_msps=72.3, max_abs_err=5.46e-05 (2^-14.16)
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.88, accuracy_bits=14.6, area_um2=41251, ffs=598, throughput_msps=66.8, max_abs_err=3.91e-05 (2^-14.64)
- pipelined_m [data_width=19 n_iter=16 angle_guard=4 frac_guard=4 rounding=round m=2] power_index=3.04, accuracy_bits=14.8, area_um2=43815, ffs=629, throughput_msps=64.3, max_abs_err=3.52e-05 (2^-14.79)
- pipelined_m [data_width=20 n_iter=17 angle_guard=1 frac_guard=1 rounding=round m=2] power_index=3.13, accuracy_bits=15.2, area_um2=43984, ffs=659, throughput_msps=69.4, max_abs_err=2.58e-05 (2^-15.24)
- pipelined_m [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=3.16, accuracy_bits=15.4, area_um2=45609, ffs=655, throughput_msps=69.4, max_abs_err=2.34e-05 (2^-15.38)
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=3 rounding=trunc m=2] power_index=3.3, accuracy_bits=15.6, area_um2=47117, ffs=688, throughput_msps=64.3, max_abs_err=2.04e-05 (2^-15.58)
- pipelined_m [data_width=20 n_iter=19 angle_guard=1 frac_guard=4 rounding=round m=2] power_index=3.73, accuracy_bits=16.1, area_um2=52976, ffs=781, throughput_msps=62, max_abs_err=1.42e-05 (2^-16.11)
Front coverage: power_index 2.38..3.73 (HV reference 40); accuracy_bits 12.5..16.1 (HV reference 12); data_width on the front 16..20 (registry 8..28).

Per family:
- pipelined: 40 evals, 18 feasible; max throughput seen 163 MSPS; best accuracy 15.56 bits; best feasible power_index=3.86; feasible ranges: data_width 16..19, n_iter 14..18, angle_guard 0..4, frac_guard 0..4
- pipelined_m: 60 evals, 25 feasible; max throughput seen 86.6 MSPS; best accuracy 16.11 bits; best feasible power_index=2.38; feasible ranges: data_width 16..20, n_iter 15..19, angle_guard 0..4, frac_guard 1..4, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `pipelined_m` (20 evals): data_width=15..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (13 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 49 feasible; hypervolume 181.2 (+18.9%).

**LLM decision:** `widen` — mapper: widen_niter_datawidth_for_pipelined_m (feasible front is pipelined_m-only; accuracy tail truncated)

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 181.2 (gain this round: +18.9%).
Feasible designs: 49 of 120 evaluations (38 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 36% violate; best seen 163
- max_abs_err <= 0.000244141: 35% violate; best seen 1.63e-06 (2^-19.23)

Pareto front (feasible, 14 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.38, accuracy_bits=12.5, area_um2=34177, ffs=495, throughput_msps=78.8, max_abs_err=0.000177 (2^-12.47)
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc m=2] power_index=2.56, accuracy_bits=13.2, area_um2=36192, ffs=537, throughput_msps=75.4, max_abs_err=0.000104 (2^-13.23)
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc m=2] power_index=2.67, accuracy_bits=13.8, area_um2=37823, ffs=558, throughput_msps=72.3, max_abs_err=6.86e-05 (2^-13.83)
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=2.7, accuracy_bits=14.2, area_um2=38786, ffs=560, throughput_msps=72.3, max_abs_err=5.46e-05 (2^-14.16)
- pipelined_m [data_width=20 n_iter=16 angle_guard=4 frac_guard=2 rounding=trunc m=2] power_index=2.99, accuracy_bits=14.7, area_um2=42373, ffs=625, throughput_msps=62, max_abs_err=3.8e-05 (2^-14.68)
- pipelined_m [data_width=19 n_iter=16 angle_guard=4 frac_guard=4 rounding=round m=2] power_index=3.04, accuracy_bits=14.8, area_um2=43815, ffs=629, throughput_msps=64.3, max_abs_err=3.52e-05 (2^-14.79)
- pipelined_m [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=3.16, accuracy_bits=15.4, area_um2=45609, ffs=655, throughput_msps=69.4, max_abs_err=2.34e-05 (2^-15.38)
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=1 rounding=round m=2] power_index=3.18, accuracy_bits=15.4, area_um2=45747, ffs=659, throughput_msps=69.4, max_abs_err=2.28e-05 (2^-15.42)
- pipelined_m [data_width=23 n_iter=18 angle_guard=4 frac_guard=0 rounding=trunc m=2] power_index=3.6, accuracy_bits=16.5, area_um2=51164, ffs=753, throughput_msps=56.1, max_abs_err=1.07e-05 (2^-16.51)
- pipelined_m [data_width=23 n_iter=18 angle_guard=4 frac_guard=2 rounding=round m=2] power_index=3.8, accuracy_bits=16.9, area_um2=54820, ffs=787, throughput_msps=56.1, max_abs_err=8.19e-06 (2^-16.90)
Front coverage: power_index 2.38..3.8 (HV reference 40); accuracy_bits 12.5..16.9 (HV reference 12); data_width on the front 16..23 (registry 8..28).

Per family:
- pipelined: 40 evals, 18 feasible; max throughput seen 163 MSPS; best accuracy 15.56 bits; best feasible power_index=3.86; feasible ranges: data_width 16..19, n_iter 14..18, angle_guard 0..4, frac_guard 0..4
- pipelined_m: 80 evals, 31 feasible; max throughput seen 86.6 MSPS; best accuracy 19.23 bits; best feasible power_index=2.38; feasible ranges: data_width 16..23, n_iter 15..19, angle_guard -2..4, frac_guard 0..4, m 2..2
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The feasible front is owned entirely by pipelined_m (best power_index 2.38 vs pipelined's 3.86, and pipelined_m reaches 19.23 accuracy bits vs pipelined's 15.56), so concentrate here. Two gaps are visible: (1) n_iter was only sampled 15..19 although the registry allows 4..30, and for pipelined_m throughput = Fmax essentially independent of N, so the accuracy tail is artificially cut — the reported HV 181.2 is dominated by the single term (40 - 3.8)*(16.9 - 12) = 177.4, i.e. by the highest-accuracy front point, so raising a_max is the cheapest HV gain; (2) data_width was only sampled to 23, but throughput is 56.1 MSPS at W=23 (57 at W=22), leaving ~1-2 widths of room before the 50 MSPS floor. Widening n_iter to 30 at data_width ~22-24 should move a_max from 16.9 toward the 19+ bits already observed, while a smaller slice checks the low-power corner and m=3. pipelined (best throughput 163 but best feasible power 3.86, accuracy 15.56) stays off the search this round; it is dominated on both objectives that matter for selection.*)
- `pipelined_m` (80 evals): data_width=20..24, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=round|trunc, m=2..3. *Why:* extend the accuracy tail: N is nearly throughput-free for pipelined_m (1 result/cycle, Fmax set by m stages x data_width, not by N), so use high n_iter at high data_width to lift accuracy_bits well past the current 16.9
- clamped by code: dropped duplicate family pipelined_m

**Result (code):** 80 evaluations this round, 200 total; 110 feasible; hypervolume 292.7 (+61.5%).

**LLM decision:** `stop` — Budget is exhausted (200/200 evals) and this is the final round, so only stop/infeasible are valid. Infeasible is ruled out: 110 of 200 evaluations are feasible, and the selection rule (min power_index) is already satisfiable — the front's cheapest point, pipelined_m [W=16 N=16 angle_guard=2 frac_guard=1 round m=2], has power_index=2.38 with throughput 78.8 MSPS (>=50) and max_abs_err 1.77e-4 (<=2.44e-4), i.e. it meets both constraints. The front is also well-covered for the hypervolume objective: power_index spans 2.38..5.04 and accuracy_bits spans 12.5..20 (HV reference 12), with 26 Pareto designs and a +61.5% HV gain this round, so further mapping is not warranted. Both families on the front (pipelined, pipelined_m) were explored, and the registry has no unexplored family left to add. Stopping on the current front.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 292.7 (gain this round: +61.5%).
Feasible designs: 110 of 200 evaluations (90 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 31% violate; best seen 163
- max_abs_err <= 0.000244141: 21% violate; best seen 3.54e-07 (2^-21.43)

Pareto front (feasible, 26 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.38, accuracy_bits=12.5, area_um2=34177, ffs=495, throughput_msps=78.8, max_abs_err=0.000177 (2^-12.47)
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc m=2] power_index=2.67, accuracy_bits=13.8, area_um2=37823, ffs=558, throughput_msps=72.3, max_abs_err=6.86e-05 (2^-13.83)
- pipelined_m [data_width=20 n_iter=16 angle_guard=4 frac_guard=2 rounding=trunc m=2] power_index=2.99, accuracy_bits=14.7, area_um2=42373, ffs=625, throughput_msps=62, max_abs_err=3.8e-05 (2^-14.68)
- pipelined_m [data_width=20 n_iter=17 angle_guard=1 frac_guard=1 rounding=round m=2] power_index=3.13, accuracy_bits=15.2, area_um2=43984, ffs=659, throughput_msps=69.4, max_abs_err=2.58e-05 (2^-15.24)
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=3 rounding=trunc m=2] power_index=3.3, accuracy_bits=15.6, area_um2=47117, ffs=688, throughput_msps=64.3, max_abs_err=2.04e-05 (2^-15.58)
- pipelined_m [data_width=22 n_iter=20 angle_guard=2 frac_guard=0 rounding=round m=2] power_index=3.74, accuracy_bits=17.2, area_um2=53385, ffs=781, throughput_msps=62, max_abs_err=6.45e-06 (2^-17.24)
- pipelined_m [data_width=22 n_iter=20 angle_guard=4 frac_guard=1 rounding=round m=2] power_index=3.97, accuracy_bits=17.9, area_um2=57325, ffs=820, throughput_msps=57.9, max_abs_err=4.04e-06 (2^-17.92)
- pipelined_m [data_width=23 n_iter=20 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=4.11, accuracy_bits=18.4, area_um2=59487, ffs=849, throughput_msps=59.9, max_abs_err=2.95e-06 (2^-18.37)
- pipelined_m [data_width=24 n_iter=20 angle_guard=2 frac_guard=3 rounding=trunc m=2] power_index=4.31, accuracy_bits=18.6, area_um2=61787, ffs=897, throughput_msps=56.1, max_abs_err=2.46e-06 (2^-18.63)
- pipelined_m [data_width=24 n_iter=23 angle_guard=4 frac_guard=1 rounding=round m=2] power_index=5.04, accuracy_bits=20, area_um2=71887, ffs=1050, throughput_msps=54.3, max_abs_err=9.35e-07 (2^-20.03)
Front coverage: power_index 2.38..5.04 (HV reference 40); accuracy_bits 12.5..20 (HV reference 12); data_width on the front 16..24 (registry 8..28).

Per family:
- pipelined: 40 evals, 18 feasible; max throughput seen 163 MSPS; best accuracy 15.56 bits; best feasible power_index=3.86; feasible ranges: data_width 16..19, n_iter 14..18, angle_guard 0..4, frac_guard 0..4
- pipelined_m: 160 evals, 92 feasible; max throughput seen 86.6 MSPS; best accuracy 21.43 bits; best feasible power_index=2.38; feasible ranges: data_width 16..24, n_iter 15..30, angle_guard -2..4, frac_guard 0..4, m 2..2
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 1)
- tokens: 10368 in, 19051 out
- provider-reported cost: $0.0157
- full prompts and replies: `llm_trace.jsonl`

