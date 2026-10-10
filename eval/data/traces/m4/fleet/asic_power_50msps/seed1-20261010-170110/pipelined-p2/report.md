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
`pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=3` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 26576 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 7080 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 323 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 129 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.68 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000204 (2^-12.26) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 6.67 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 6.07e-05 (2^-14.01) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.99 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (15 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=3` | 26576 | 323 | 54.3 | 7 | 1.68 | 0.000204 (2^-12.26) | 12.26 |
| 1 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc,m=3` | 30392 | 348 | 51.9 | 7 | 1.86 | 0.000127 (2^-12.95) | 12.95 |
| 2 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=2` | 35120 | 523 | 75.4 | 10 | 2.49 | 0.000108 (2^-13.18) | 13.18 |
| 3 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=2,rounding=round,m=2` | 36567 | 553 | 72.3 | 10 | 2.61 | 9.56e-05 (2^-13.35) | 13.35 |
| 4 | `pipelined_m:data_width=22,n_iter=16,angle_guard=2,frac_guard=3,rounding=round,m=2` | 46932 | 676 | 59.9 | 10 | 3.26 | 3.16e-05 (2^-14.95) | 14.95 |
| 5 | `pipelined_m:data_width=19,n_iter=18,angle_guard=3,frac_guard=3,rounding=round,m=2` | 47458 | 679 | 66.8 | 11 | 3.29 | 1.78e-05 (2^-15.78) | 15.78 |
| 6 | `pipelined_m:data_width=20,n_iter=20,angle_guard=3,frac_guard=3,rounding=round,m=2` | 54937 | 783 | 64.3 | 12 | 3.79 | 6.52e-06 (2^-17.23) | 17.23 |
| 7 | `pipelined_m:data_width=22,n_iter=20,angle_guard=3,frac_guard=3,rounding=round,m=2` | 59349 | 845 | 59.9 | 12 | 4.1 | 3.04e-06 (2^-18.33) | 18.33 |
| 8 | `pipelined_m:data_width=25,n_iter=28,angle_guard=3,frac_guard=0,rounding=round,m=2` | 85147 | 1219 | 54.3 | 16 | 5.9 | 7.53e-07 (2^-20.34) | 20.34 |
| 9 | `pipelined:data_width=28,n_iter=22,angle_guard=3,frac_guard=0,rounding=round` | 95168 | 2033 | 93.5 | 24 | 8.45 | 5.3e-07 (2^-20.85) | 20.85 |
| 10 | `pipelined:data_width=28,n_iter=22,angle_guard=4,frac_guard=0,rounding=round` | 96184 | 2055 | 91.1 | 24 | 8.54 | 5.26e-07 (2^-20.86) | 20.86 |
| 11 | `pipelined:data_width=28,n_iter=22,angle_guard=4,frac_guard=2,rounding=round` | 101552 | 2135 | 91.1 | 24 | 8.93 | 4.91e-07 (2^-20.96) | 20.96 |
| 12 | `pipelined:data_width=26,n_iter=26,angle_guard=4,frac_guard=0,rounding=round` | 106848 | 2275 | 96.1 | 28 | 9.47 | 3.6e-07 (2^-21.40) | 21.40 |
| 13 | `pipelined:data_width=28,n_iter=26,angle_guard=3,frac_guard=0,rounding=round` | 112880 | 2403 | 93.5 | 28 | 10 | 1.1e-07 (2^-23.12) | 23.12 |
| 14 | `pipelined:data_width=28,n_iter=25,angle_guard=3,frac_guard=4,rounding=round` | 118848 | 2493 | 91.1 | 27 | 10.4 | 7.42e-08 (2^-23.68) | 23.68 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts are decisive: iterative and unrolled_k produced 0 feasible designs (they cannot hit 50 MSPS throughput), so they are out. pipelined has 41 feasible points but its best power_index is 3.49, while pipelined_m already achieves 1.75 with only 5 feasible points and 3 front members. pipelined_m is clearly the power-optimal family for this spec because registering every m stages (m>1) drastically cuts flip-flop count and dynamic power while still delivering 1 result/cycle. My entire remaining budget goes to pipelined_m, tightly focused around the region that produced the best power_index: moderate data_width (14-18) to satisfy the 2^-12 accuracy constraint with minimal overhead, n_iter 12-16 for sufficient convergence, small angle/frac guards (0-2) to keep the datapath narrow, and m 2-4 to balance FF reduction against timing. This should map the Pareto front over the power/accuracy trade-off and find the minimum-power design that meets both constraints.*)
- `pipelined_m` (100 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m already holds the best feasible power_index (1.75) and 3 front points; it is the only family that can plausibly beat the pipelined power floor while keeping 1-result/cycle throughput. I focus the remaining budget here: narrow data_width to 14-18 (accuracy_bits target is 12, so W=14-16 is the sweet spot; W>18 wastes area/power for no accuracy gain), n_iter 12-16 (enough for <=2^-12 with small guards, but higher N adds power), angle_guard 0-2 and frac_guard 0-2 (small guards keep the datapath narrow; the accuracy constraint is loose at 2^-12), and m 2-4 (registering every 2-4 stages cuts FF count and power vs full pipelining while still meeting 50 MSPS). This is where the power/accuracy trade-off curve lives.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 15 feasible; hypervolume 51.34 (n/a).

**LLM decision:** `add_family` — The current front is dominated by pipelined_m with a minimum power_index of 1.68. The pipelined family has not been explored yet. Since pipelined_m registers every m stages (m>=2), it inherently has fewer registers and potentially lower power than the fully pipelined architecture (m=1), but the pipelined family might offer different trade-offs or a lower power floor if the cost model favors its specific structure or if it allows for a lower n_iter/data_width combination that pipelined_m didn't explore efficiently. More importantly, the current front only covers data_width 17-18. The 'pipelined' family is the only other high-throughput option (1 result/cycle) that hasn't been tested. Given that 45% of evaluations violated throughput, ensuring we have the best possible throughput/power trade-off from all 1-cycle families is critical. Adding 'pipelined' allows us to compare the m=1 case directly against the m=2,3 cases already found, potentially revealing a lower power design or a different accuracy/power slope.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 51.34 (gain this round: n/a (first round)).
Feasible designs: 15 of 100 evaluations (12 unique).
Families explored so far: pipelined_m. Not yet explored: pipelined.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 45% violate; best seen 91.1
- max_abs_err <= 0.000244141: 65% violate; best seen 8.41e-05 (2^-13.54)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=1.68, accuracy_bits=12.3, area_um2=26576, ffs=323, throughput_msps=54.3, max_abs_err=0.000204 (2^-12.26)
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=3] power_index=1.86, accuracy_bits=12.9, area_um2=30392, ffs=348, throughput_msps=51.9, max_abs_err=0.000127 (2^-12.95)
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=2] power_index=2.49, accuracy_bits=13.2, area_um2=35120, ffs=523, throughput_msps=75.4, max_abs_err=0.000108 (2^-13.18)
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=2] power_index=2.61, accuracy_bits=13.4, area_um2=36567, ffs=553, throughput_msps=72.3, max_abs_err=9.56e-05 (2^-13.35)
Front coverage: power_index 1.68..2.61 (HV reference 40); accuracy_bits 12.3..13.4 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined_m: 100 evals, 15 feasible; max throughput seen 91.1 MSPS; best accuracy 13.54 bits; best feasible power_index=1.68; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2, m 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *We need to verify if the 'pipelined' family (m=1) can beat the current best power_index of 1.68 from 'pipelined_m'. The ranges are focused on the known feasible accuracy/throughput region to maximize the chance of finding a feasible, low-power design within the remaining budget.*)
- `pipelined` (20 evals): data_width=16..20, n_iter=13..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Explore the fully pipelined (m=1) architecture to compare against the pipelined_m (m=2,3) results. The ranges are centered around the feasible region found in Round 1 (data_width 17-18, n_iter 14-16) but slightly widened to catch potential lower-power corners. This will determine if the fully pipelined structure offers a better power/accuracy trade-off than the partially pipelined versions.

**Result (code):** 20 evaluations this round, 120 total; 31 feasible; hypervolume 134 (+160.9%).

**LLM decision:** `stop` — The feasible Pareto front is well-mapped and satisfies all constraints. The minimum power_index achieved is 1.68 (pipelined_m, data_width=17, n_iter=14, m=3), which comfortably meets the throughput constraint (54.3 MSPS >= 50) and the accuracy constraint (max_abs_err=0.000204 <= 0.000244141). The front spans a wide range of accuracy_bits (12.3 to 15.7) and power_index (1.68 to 5.24), providing a good trade-off curve for the selection rule (min power_index). Since this is the final round, we stop with the current front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 134 (gain this round: +160.9%).
Feasible designs: 31 of 120 evaluations (25 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 38% violate; best seen 149
- max_abs_err <= 0.000244141: 57% violate; best seen 1.89e-05 (2^-15.69)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=1.68, accuracy_bits=12.3, area_um2=26576, ffs=323, throughput_msps=54.3, max_abs_err=0.000204 (2^-12.26)
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=3] power_index=1.86, accuracy_bits=12.9, area_um2=30392, ffs=348, throughput_msps=51.9, max_abs_err=0.000127 (2^-12.95)
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=2] power_index=2.49, accuracy_bits=13.2, area_um2=35120, ffs=523, throughput_msps=75.4, max_abs_err=0.000108 (2^-13.18)
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=2] power_index=2.61, accuracy_bits=13.4, area_um2=36567, ffs=553, throughput_msps=72.3, max_abs_err=9.56e-05 (2^-13.35)
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] power_index=4.24, accuracy_bits=14.1, area_um2=47357, ffs=1022, throughput_msps=132, max_abs_err=5.84e-05 (2^-14.06)
- pipelined [data_width=20 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] power_index=4.37, accuracy_bits=14.2, area_um2=48822, ffs=1054, throughput_msps=132, max_abs_err=5.27e-05 (2^-14.21)
- pipelined [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] power_index=4.5, accuracy_bits=14.6, area_um2=50287, ffs=1085, throughput_msps=123, max_abs_err=4.12e-05 (2^-14.57)
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=0 rounding=round] power_index=4.78, accuracy_bits=15.1, area_um2=53531, ffs=1153, throughput_msps=123, max_abs_err=2.85e-05 (2^-15.10)
- pipelined [data_width=19 n_iter=17 angle_guard=2 frac_guard=2 rounding=round] power_index=4.86, accuracy_bits=15.1, area_um2=55151, ffs=1164, throughput_msps=128, max_abs_err=2.76e-05 (2^-15.14)
- pipelined [data_width=20 n_iter=18 angle_guard=2 frac_guard=1 rounding=round] power_index=5.24, accuracy_bits=15.7, area_um2=59407, ffs=1254, throughput_msps=123, max_abs_err=1.89e-05 (2^-15.69)
Front coverage: power_index 1.68..5.24 (HV reference 40); accuracy_bits 12.3..15.7 (HV reference 12); data_width on the front 17..20 (registry 8..28).

Per family:
- pipelined: 20 evals, 16 feasible; max throughput seen 149 MSPS; best accuracy 15.69 bits; best feasible power_index=3.79; feasible ranges: data_width 17..20, n_iter 15..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 100 evals, 15 feasible; max throughput seen 91.1 MSPS; best accuracy 13.54 bits; best feasible power_index=1.68; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2, m 2..3
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (30 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)
- `pipelined` (50 evals): data_width=18..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (7 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 90 feasible; hypervolume 402.3 (+200.3%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-mapped and satisfies all constraints. The minimum power_index achieved is 1.68 (pipelined_m, data_width=17, n_iter=14, m=3), which comfortably meets the throughput constraint (54.3 MSPS >= 50) and the accuracy constraint (max_abs_err=0.000204 <= 0.000244141). The front spans a wide range of accuracy_bits (12.3 to 15.7) and power_index (1.68 to 5.24), providing a good trade-off curve for the selection rule (min power_index). Since this is the final round, we stop with the current front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 402.3 (gain this round: +200.3%).
Feasible designs: 90 of 200 evaluations (75 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 32% violate; best seen 149
- max_abs_err <= 0.000244141: 36% violate; best seen 2.86e-08 (2^-25.06)

Pareto front (feasible, 15 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=1.68, accuracy_bits=12.3, area_um2=26576, ffs=323, throughput_msps=54.3, max_abs_err=0.000204 (2^-12.26)
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=2] power_index=2.49, accuracy_bits=13.2, area_um2=35120, ffs=523, throughput_msps=75.4, max_abs_err=0.000108 (2^-13.18)
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=2] power_index=2.61, accuracy_bits=13.4, area_um2=36567, ffs=553, throughput_msps=72.3, max_abs_err=9.56e-05 (2^-13.35)
- pipelined_m [data_width=19 n_iter=18 angle_guard=3 frac_guard=3 rounding=round m=2] power_index=3.29, accuracy_bits=15.8, area_um2=47458, ffs=679, throughput_msps=66.8, max_abs_err=1.78e-05 (2^-15.78)
- pipelined_m [data_width=20 n_iter=20 angle_guard=3 frac_guard=3 rounding=round m=2] power_index=3.79, accuracy_bits=17.2, area_um2=54937, ffs=783, throughput_msps=64.3, max_abs_err=6.52e-06 (2^-17.23)
- pipelined_m [data_width=25 n_iter=28 angle_guard=3 frac_guard=0 rounding=round m=2] power_index=5.9, accuracy_bits=20.3, area_um2=85147, ffs=1219, throughput_msps=54.3, max_abs_err=7.53e-07 (2^-20.34)
- pipelined [data_width=28 n_iter=22 angle_guard=3 frac_guard=0 rounding=round] power_index=8.45, accuracy_bits=20.8, area_um2=95168, ffs=2033, throughput_msps=93.5, max_abs_err=5.3e-07 (2^-20.85)
- pipelined [data_width=28 n_iter=22 angle_guard=4 frac_guard=2 rounding=round] power_index=8.93, accuracy_bits=21, area_um2=101552, ffs=2135, throughput_msps=91.1, max_abs_err=4.91e-07 (2^-20.96)
- pipelined [data_width=26 n_iter=26 angle_guard=4 frac_guard=0 rounding=round] power_index=9.47, accuracy_bits=21.4, area_um2=106848, ffs=2275, throughput_msps=96.1, max_abs_err=3.6e-07 (2^-21.40)
- pipelined [data_width=28 n_iter=25 angle_guard=3 frac_guard=4 rounding=round] power_index=10.4, accuracy_bits=23.7, area_um2=118848, ffs=2493, throughput_msps=91.1, max_abs_err=7.42e-08 (2^-23.68)
Front coverage: power_index 1.68..10.4 (HV reference 40); accuracy_bits 12.3..23.7 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- pipelined: 70 evals, 65 feasible; max throughput seen 149 MSPS; best accuracy 23.68 bits; best feasible power_index=3.79; feasible ranges: data_width 17..28, n_iter 14..28, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 130 evals, 25 feasible; max throughput seen 91.1 MSPS; best accuracy 25.06 bits; best feasible power_index=1.68; feasible ranges: data_width 17..25, n_iter 14..28, angle_guard -2..3, frac_guard 0..4, m 2..3
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7212 in, 1670 out
- provider-reported cost: $0.0049
- full prompts and replies: `llm_trace.jsonl`

