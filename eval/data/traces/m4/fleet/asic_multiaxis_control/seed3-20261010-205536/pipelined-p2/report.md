# DSE run: asic_multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: anthropic/claude-sonnet-5.5.  
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
`pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=trunc` — selection: auto (spec rule: min area_um2)

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
| max_abs_err | 0.00024 (2^-12.03) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 15.7 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.77e-05 (2^-14.08) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.78 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (15 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=trunc` | 39973 | 867 | 132.4 | 16 | 2.3 | 0.00024 (2^-12.03) | 12.03 |
| 1 | `pipelined:data_width=17,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc` | 40790 | 881 | 143.2 | 17 | 2.34 | 0.000239 (2^-12.03) | 12.03 |
| 2 | `pipelined:data_width=16,n_iter=15,angle_guard=3,frac_guard=1,rounding=round` | 41651 | 883 | 137.6 | 17 | 2.36 | 0.000174 (2^-12.49) | 12.49 |
| 3 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` | 42125 | 893 | 132.4 | 16 | 2.38 | 0.000152 (2^-12.68) | 12.68 |
| 4 | `pipelined:data_width=16,n_iter=15,angle_guard=3,frac_guard=2,rounding=round` | 42934 | 908 | 137.6 | 17 | 2.43 | 0.000128 (2^-12.93) | 12.93 |
| 5 | `pipelined:data_width=17,n_iter=15,angle_guard=3,frac_guard=3,rounding=round` | 46324 | 978 | 132.4 | 17 | 2.61 | 8.99e-05 (2^-13.44) | 13.44 |
| 6 | `pipelined:data_width=18,n_iter=17,angle_guard=3,frac_guard=1,rounding=trunc` | 51104 | 1099 | 127.5 | 19 | 2.92 | 8.72e-05 (2^-13.49) | 13.49 |
| 7 | `pipelined:data_width=18,n_iter=17,angle_guard=3,frac_guard=3,rounding=round` | 55012 | 1160 | 127.5 | 19 | 3.1 | 3.11e-05 (2^-14.97) | 14.97 |
| 8 | `pipelined:data_width=22,n_iter=17,angle_guard=0,frac_guard=0,rounding=trunc` | 56650 | 1220 | 123.1 | 19 | 3.24 | 2.44e-05 (2^-15.32) | 15.32 |
| 9 | `pipelined:data_width=22,n_iter=17,angle_guard=4,frac_guard=3,rounding=trunc` | 64187 | 1375 | 107.9 | 19 | 3.66 | 1.68e-05 (2^-15.86) | 15.86 |
| 10 | `pipelined:data_width=23,n_iter=19,angle_guard=-1,frac_guard=0,rounding=trunc` | 65265 | 1401 | 118.9 | 21 | 3.72 | 1.05e-05 (2^-16.54) | 16.54 |
| 11 | `pipelined:data_width=23,n_iter=19,angle_guard=-1,frac_guard=1,rounding=trunc` | 66927 | 1434 | 115.0 | 21 | 3.81 | 9.39e-06 (2^-16.70) | 16.70 |
| 12 | `pipelined:data_width=24,n_iter=19,angle_guard=-1,frac_guard=0,rounding=round` | 67889 | 1457 | 115.0 | 21 | 3.87 | 6.3e-06 (2^-17.28) | 17.28 |
| 13 | `pipelined:data_width=22,n_iter=21,angle_guard=4,frac_guard=1,rounding=trunc` | 76111 | 1627 | 107.9 | 23 | 4.33 | 6.11e-06 (2^-17.32) | 17.32 |
| 14 | `pipelined:data_width=21,n_iter=21,angle_guard=4,frac_guard=2,rounding=round` | 76172 | 1604 | 111.3 | 23 | 4.29 | 3.91e-06 (2^-17.97) | 17.97 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Iterative and unrolled_k found no feasible designs, which is consistent with the 32-result burst having to return within 0.5 us. The remaining families are the pipelined ones. Pipelined has proven feasibility but larger area. Pipelined_m has the smallest area found but a poor feasibility rate. I spend more of the budget on pipelined_m with moderate m and narrowed width and iteration ranges to turn its area advantage into more feasible points. A smaller share on pipelined keeps the front covered across accuracy levels. Rounding stays open for the optimiser to choose.*)
- `pipelined_m` (60 evals): data_width=12..18, n_iter=11..16, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, m=2..5. *Why:* It holds the best feasible area (30990), but only 1 of 43 evals was feasible. Fewer pipeline registers cut area, yet a large m may lower Fmax too far for the 0.5 us batch deadline. I narrow m to 2..5 and the width and iteration counts to the region near the 2^-12 error limit, to find more feasible points.
- `pipelined` (40 evals): data_width=12..20, n_iter=11..18, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* 39 of 57 evals were feasible and 11 of the 12 designs on the merged front come from it, so it reliably meets the timing and accuracy constraints. It stays as a safe fallback and covers the higher-accuracy end of the front. I trim the ranges to where feasible points cluster and keep a smaller share than pipelined_m.

**Result (code):** 100 evaluations this round, 100 total; 19 feasible; hypervolume 1.502e+05 (n/a).

**LLM decision:** `refine` — Only pipelined has feasible designs (19 of 40 evals). pipelined_m has 0 of 60 feasible, with max throughput 96 MSPS and no design passing all constraints. Iterative and unrolled_k cannot return 32 results in 0.5 us at these clocks, because each result takes N+3 or ceil(N/k)+3 cycles. The cheapest front point (area 41426, 12.0 bits) sits right at the 2^-12 error limit, so area can probably be pushed lower by trimming width, iterations and guard bits near that boundary. The feasible region is data_width 15..19, n_iter 14..17, frac_guard 0..3. I will concentrate on a tighter box around it. A small pipelined_m share with larger m stays in to check whether it can ever be feasible. Code will map the full accuracy range later in the reserved budget.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.502e+05 (gain this round: n/a (first round)).
Feasible designs: 19 of 100 evaluations (15 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 3% violate; best seen 171
- max_abs_err <= 0.000244141: 56% violate; best seen 3.11e-05 (2^-14.97)
- sys_p99_batch_us <= 0.5: 47% violate; best seen 0.269

Pareto front (feasible, 7 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=15 n_iter=15 angle_guard=2 frac_guard=3 rounding=round] area_um2=41426, accuracy_bits=12, ffs=875, throughput_msps=143, max_abs_err=0.000242 (2^-12.01), power_index=2.34
- pipelined [data_width=16 n_iter=15 angle_guard=3 frac_guard=1 rounding=round] area_um2=41651, accuracy_bits=12.5, ffs=883, throughput_msps=138, max_abs_err=0.000174 (2^-12.49), power_index=2.36
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=3 rounding=trunc] area_um2=42900, accuracy_bits=12.6, ffs=924, throughput_msps=128, max_abs_err=0.000157 (2^-12.64), power_index=2.45
- pipelined [data_width=16 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] area_um2=42934, accuracy_bits=12.9, ffs=908, throughput_msps=138, max_abs_err=0.000128 (2^-12.93), power_index=2.43
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=3 rounding=round] area_um2=46324, accuracy_bits=13.4, ffs=978, throughput_msps=132, max_abs_err=8.99e-05 (2^-13.44), power_index=2.61
- pipelined [data_width=18 n_iter=17 angle_guard=3 frac_guard=1 rounding=trunc] area_um2=51104, accuracy_bits=13.5, ffs=1099, throughput_msps=128, max_abs_err=8.72e-05 (2^-13.49), power_index=2.92
- pipelined [data_width=18 n_iter=17 angle_guard=3 frac_guard=3 rounding=round] area_um2=55012, accuracy_bits=15, ffs=1160, throughput_msps=128, max_abs_err=3.11e-05 (2^-14.97), power_index=3.1
Front coverage: area_um2 41426..55012 (HV reference 100000); accuracy_bits 12..15 (HV reference 12); data_width on the front 15..18 (registry 8..28).

Per family:
- pipelined: 40 evals, 19 feasible; max throughput seen 171 MSPS; best accuracy 14.97 bits; best feasible area_um2=41426; feasible ranges: data_width 15..19, n_iter 14..17, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 60 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 13.03 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The selection rule is min area, and the front's cheapest point sits at the error limit, so a narrower search at smaller widths and iteration counts should find cheaper feasible designs. Most budget goes to pipelined and a minor share to pipelined_m.*)
- `pipelined` (15 evals): data_width=13..17, n_iter=12..16, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* Push minimum area below 41426 by shrinking width and iterations while holding max error at or below 2^-12.
- `pipelined_m` (5 evals): data_width=14..18, n_iter=13..16, angle_guard=0..3, frac_guard=1..3, rounding=round, m=2..3. *Why:* Small probe with low m (2..3) near the accuracy-feasible region, to see whether it can pass the 0.5 us batch bound at a lower area than pipelined.

**Result (code):** 20 evaluations this round, 120 total; 20 feasible; hypervolume 1.502e+05 (+0.0%).

**LLM decision:** `stop` — This is the final round. The feasible front has 7 pipelined designs spanning area 40790..55012 um2 and accuracy 12..15 bits. The cheapest feasible design (data_width=17, n_iter=15, angle_guard=0, frac_guard=1, trunc) has area 40790, max_abs_err 0.000239 (just under the 2^-12 limit) and throughput 143 MSPS, well above the 32 required. The last round added +0.0% hypervolume, so the front has stopped improving. pipelined_m produced 0 feasible designs in 65 evaluations. The iterative and unrolled_k families were not run, and their multi-cycle issue would queue the 32-request burst against the 0.5 us batch bound. The constraints are met, so the problem is not infeasible.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.502e+05 (gain this round: +0.0%).
Feasible designs: 20 of 120 evaluations (16 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 2% violate; best seen 171
- max_abs_err <= 0.000244141: 61% violate; best seen 3.11e-05 (2^-14.97)
- sys_p99_batch_us <= 0.5: 42% violate; best seen 0.269

Pareto front (feasible, 7 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc] area_um2=40790, accuracy_bits=12, ffs=881, throughput_msps=143, max_abs_err=0.000239 (2^-12.03), power_index=2.34
- pipelined [data_width=16 n_iter=15 angle_guard=3 frac_guard=1 rounding=round] area_um2=41651, accuracy_bits=12.5, ffs=883, throughput_msps=138, max_abs_err=0.000174 (2^-12.49), power_index=2.36
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=3 rounding=trunc] area_um2=42900, accuracy_bits=12.6, ffs=924, throughput_msps=128, max_abs_err=0.000157 (2^-12.64), power_index=2.45
- pipelined [data_width=16 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] area_um2=42934, accuracy_bits=12.9, ffs=908, throughput_msps=138, max_abs_err=0.000128 (2^-12.93), power_index=2.43
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=3 rounding=round] area_um2=46324, accuracy_bits=13.4, ffs=978, throughput_msps=132, max_abs_err=8.99e-05 (2^-13.44), power_index=2.61
- pipelined [data_width=18 n_iter=17 angle_guard=3 frac_guard=1 rounding=trunc] area_um2=51104, accuracy_bits=13.5, ffs=1099, throughput_msps=128, max_abs_err=8.72e-05 (2^-13.49), power_index=2.92
- pipelined [data_width=18 n_iter=17 angle_guard=3 frac_guard=3 rounding=round] area_um2=55012, accuracy_bits=15, ffs=1160, throughput_msps=128, max_abs_err=3.11e-05 (2^-14.97), power_index=3.1
Front coverage: area_um2 40790..55012 (HV reference 100000); accuracy_bits 12..15 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 55 evals, 20 feasible; max throughput seen 171 MSPS; best accuracy 14.97 bits; best feasible area_um2=40790; feasible ranges: data_width 15..19, n_iter 14..17, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 65 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 14.24 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined` (40 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (7 front designs; box front_anchored)
- `pipelined_m` (40 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 80 evaluations this round, 200 total; 47 feasible; hypervolume 2.487e+05 (+65.6%).

**No LLM call** (code's front-mapping round): This is the final round. The feasible front has 7 pipelined designs spanning area 40790..55012 um2 and accuracy 12..15 bits. The cheapest feasible design (data_width=17, n_iter=15, angle_guard=0, frac_guard=1, trunc) has area 40790, max_abs_err 0.000239 (just under the 2^-12 limit) and throughput 143 MSPS, well above the 32 required. The last round added +0.0% hypervolume, so the front has stopped improving. pipelined_m produced 0 feasible designs in 65 evaluations. The iterative and unrolled_k families were not run, and their multi-cycle issue would queue the 32-request burst against the 0.5 us batch bound. The constraints are met, so the problem is not infeasible.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 2.487e+05 (gain this round: +65.6%).
Feasible designs: 47 of 200 evaluations (40 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 9% violate; best seen 171
- max_abs_err <= 0.000244141: 50% violate; best seen 7.32e-08 (2^-23.70)
- sys_p99_batch_us <= 0.5: 47% violate; best seen 0.269

Pareto front (feasible, 15 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=39973, accuracy_bits=12, ffs=867, throughput_msps=132, max_abs_err=0.00024 (2^-12.03), power_index=2.3
- pipelined [data_width=16 n_iter=15 angle_guard=3 frac_guard=1 rounding=round] area_um2=41651, accuracy_bits=12.5, ffs=883, throughput_msps=138, max_abs_err=0.000174 (2^-12.49), power_index=2.36
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=42125, accuracy_bits=12.7, ffs=893, throughput_msps=132, max_abs_err=0.000152 (2^-12.68), power_index=2.38
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=3 rounding=round] area_um2=46324, accuracy_bits=13.4, ffs=978, throughput_msps=132, max_abs_err=8.99e-05 (2^-13.44), power_index=2.61
- pipelined [data_width=18 n_iter=17 angle_guard=3 frac_guard=1 rounding=trunc] area_um2=51104, accuracy_bits=13.5, ffs=1099, throughput_msps=128, max_abs_err=8.72e-05 (2^-13.49), power_index=2.92
- pipelined [data_width=22 n_iter=17 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=56650, accuracy_bits=15.3, ffs=1220, throughput_msps=123, max_abs_err=2.44e-05 (2^-15.32), power_index=3.24
- pipelined [data_width=22 n_iter=17 angle_guard=4 frac_guard=3 rounding=trunc] area_um2=64187, accuracy_bits=15.9, ffs=1375, throughput_msps=108, max_abs_err=1.68e-05 (2^-15.86), power_index=3.66
- pipelined [data_width=23 n_iter=19 angle_guard=-1 frac_guard=1 rounding=trunc] area_um2=66927, accuracy_bits=16.7, ffs=1434, throughput_msps=115, max_abs_err=9.39e-06 (2^-16.70), power_index=3.81
- pipelined [data_width=24 n_iter=19 angle_guard=-1 frac_guard=0 rounding=round] area_um2=67889, accuracy_bits=17.3, ffs=1457, throughput_msps=115, max_abs_err=6.3e-06 (2^-17.28), power_index=3.87
- pipelined [data_width=21 n_iter=21 angle_guard=4 frac_guard=2 rounding=round] area_um2=76172, accuracy_bits=18, ffs=1604, throughput_msps=111, max_abs_err=3.91e-06 (2^-17.97), power_index=4.29
Front coverage: area_um2 39973..76172 (HV reference 100000); accuracy_bits 12..18 (HV reference 12); data_width on the front 16..24 (registry 8..28).

Per family:
- pipelined: 95 evals, 47 feasible; max throughput seen 171 MSPS; best accuracy 23.70 bits; best feasible area_um2=39973; feasible ranges: data_width 15..24, n_iter 14..25, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 105 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 17.77 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 16245 in, 2950 out
- provider-reported cost: $0.0620
- full prompts and replies: `llm_trace.jsonl`

