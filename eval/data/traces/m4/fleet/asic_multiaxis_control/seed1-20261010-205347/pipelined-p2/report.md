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
`pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=2` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 29151 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 7766 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 439 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 78.8 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 78.8 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 9 | exact: schedule |
| latency_ns | 114 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.33 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000204 (2^-12.26) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 6.67 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 6.07e-05 (2^-14.01) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.99 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (16 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=2` | 29151 | 439 | 78.8 | 9 | 1.33 | 0.000204 (2^-12.26) | 12.26 |
| 1 | `pipelined:data_width=17,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 42962 | 928 | 143.2 | 18 | 2.46 | 0.000149 (2^-12.71) | 12.71 |
| 2 | `pipelined:data_width=17,n_iter=15,angle_guard=1,frac_guard=2,rounding=round` | 43671 | 923 | 137.6 | 17 | 2.47 | 0.00014 (2^-12.80) | 12.80 |
| 3 | `pipelined:data_width=18,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 44427 | 960 | 143.2 | 18 | 2.54 | 0.000121 (2^-13.02) | 13.02 |
| 4 | `pipelined:data_width=17,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 45985 | 973 | 137.6 | 18 | 2.6 | 0.00012 (2^-13.03) | 13.03 |
| 5 | `pipelined:data_width=17,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 46450 | 999 | 137.6 | 18 | 2.65 | 0.000116 (2^-13.08) | 13.08 |
| 6 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 46462 | 982 | 132.4 | 17 | 2.62 | 8.26e-05 (2^-13.56) | 13.56 |
| 7 | `pipelined:data_width=18,n_iter=17,angle_guard=2,frac_guard=0,rounding=round` | 48851 | 1053 | 132.4 | 19 | 2.79 | 7.75e-05 (2^-13.65) | 13.65 |
| 8 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 49611 | 1048 | 132.4 | 18 | 2.8 | 5.46e-05 (2^-14.16) | 14.16 |
| 9 | `pipelined:data_width=20,n_iter=16,angle_guard=1,frac_guard=1,rounding=round` | 51998 | 1099 | 127.5 | 18 | 2.94 | 4.05e-05 (2^-14.59) | 14.59 |
| 10 | `pipelined:data_width=21,n_iter=17,angle_guard=2,frac_guard=0,rounding=round` | 55870 | 1203 | 118.9 | 19 | 3.19 | 2.18e-05 (2^-15.48) | 15.48 |
| 11 | `pipelined:data_width=21,n_iter=17,angle_guard=1,frac_guard=4,rounding=round` | 62097 | 1307 | 111.3 | 19 | 3.49 | 2.07e-05 (2^-15.56) | 15.56 |
| 12 | `pipelined:data_width=22,n_iter=20,angle_guard=1,frac_guard=0,rounding=trunc` | 67871 | 1455 | 118.9 | 22 | 3.87 | 1.22e-05 (2^-16.32) | 16.32 |
| 13 | `pipelined:data_width=21,n_iter=20,angle_guard=1,frac_guard=3,rounding=trunc` | 70375 | 1502 | 115.0 | 22 | 4 | 9.21e-06 (2^-16.73) | 16.73 |
| 14 | `pipelined:data_width=22,n_iter=20,angle_guard=1,frac_guard=1,rounding=round` | 70796 | 1492 | 118.9 | 22 | 3.99 | 5.57e-06 (2^-17.45) | 17.45 |
| 15 | `pipelined:data_width=27,n_iter=19,angle_guard=-2,frac_guard=0,rounding=trunc` | 74886 | 1606 | 104.7 | 21 | 4.27 | 4.28e-06 (2^-17.83) | 17.83 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The constraints need 1 result per cycle plus a high enough clock to return 32 results within 0.5 us, and only the fully pipelined family has met that so far. Iterative and unrolled families are covered by other members and found nothing feasible. I put most of the budget into a tight pipelined search around W 13-18 and N 11-16, which is where area falls while error stays at or below 2^-12. A small pipelined_m probe at low m checks whether fewer registers can still meet timing.*)
- `pipelined` (80 evals): data_width=13..18, n_iter=11..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* It is the only family with feasible designs (22 of 48, best 39246 um2) and it holds all 8 merged-front points. I narrow to the low-width, low-iteration corner, where the 2^-12 error limit is just met and area is smallest. Widths up to 18 keep the accuracy_bits end of the front covered.
- `pipelined_m` (20 evals): data_width=13..16, n_iter=11..15, angle_guard=-2..1, frac_guard=0..2, rounding=trunc|round, m=2..3. *Why:* Its 52 evaluations gave 0 feasible, probably because chaining stages lowers Fmax and misses the 0.5 us batch deadline. Fewer registers could still save area, so I keep a small probe with m=2..3, the shallowest chaining, at the low-width corner.

**Result (code):** 100 evaluations this round, 100 total; 20 feasible; hypervolume 1.18e+05 (n/a).

**LLM decision:** `refine` — Only pipelined has feasible designs so far: 20 of 80 evals, front area 38197..49611 um2 and 12.2..14.2 accuracy bits. The error constraint is the main filter (80% violate), and every feasible design has data_width 16..18 and n_iter 14..16. The best design sits at the 12.2-bit edge of the accuracy requirement, so smaller area probably lies just below it. pipelined_m produced 0 feasible designs in 20 evals, but it failed only on accuracy (best 11.32 bits). It had a max throughput of 102 MSPS, and its register-every-m structure should give fewer FFs than a full pipeline. At 102 MSPS the batch time is roughly (latency + 31) cycles, which is inside the 0.5 us bound at small m, so it is worth retrying in the accuracy-feasible region. The iterative and unrolled_k families produce one result every several cycles. For 32 simultaneous requests that queueing very likely breaks the 0.5 us batch bound, so I leave them out. I will refine both pipelined families around the feasible region and then let code map the full front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.18e+05 (gain this round: n/a (first round)).
Feasible designs: 20 of 100 evaluations (13 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 180
- max_abs_err <= 0.000244141: 80% violate; best seen 5.46e-05 (2^-14.16)
- sys_p99_batch_us <= 0.5: 10% violate; best seen 0.244

Pareto front (feasible, 8 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=38197, accuracy_bits=12.2, ffs=810, throughput_msps=143, max_abs_err=0.000209 (2^-12.22), power_index=2.16
- pipelined [data_width=17 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=42962, accuracy_bits=12.7, ffs=928, throughput_msps=143, max_abs_err=0.000149 (2^-12.71), power_index=2.46
- pipelined [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=round] area_um2=43671, accuracy_bits=12.8, ffs=923, throughput_msps=138, max_abs_err=0.00014 (2^-12.80), power_index=2.47
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] area_um2=44427, accuracy_bits=13, ffs=960, throughput_msps=143, max_abs_err=0.000121 (2^-13.02), power_index=2.54
- pipelined [data_width=17 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=45985, accuracy_bits=13, ffs=973, throughput_msps=138, max_abs_err=0.00012 (2^-13.03), power_index=2.6
- pipelined [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=46450, accuracy_bits=13.1, ffs=999, throughput_msps=138, max_abs_err=0.000116 (2^-13.08), power_index=2.65
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=46462, accuracy_bits=13.6, ffs=982, throughput_msps=132, max_abs_err=8.26e-05 (2^-13.56), power_index=2.62
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
Front coverage: area_um2 38197..49611 (HV reference 100000); accuracy_bits 12.2..14.2 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 80 evals, 20 feasible; max throughput seen 180 MSPS; best accuracy 14.16 bits; best feasible area_um2=38197; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 20 evals, 0 feasible; max throughput seen 102 MSPS; best accuracy 11.32 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate on data_width 14..18 and n_iter 12..16, where accuracy is just above 2^-12, and test whether pipelined_m with small m beats the full pipeline on area.*)
- `pipelined` (10 evals): data_width=14..17, n_iter=12..16, angle_guard=-1..2, frac_guard=0..2, rounding=round|trunc. *Why:* Probe smaller widths and fewer iterations around the cheapest feasible design (16/14/2/1/round) to find lower area at 12+ bits.
- `pipelined_m` (10 evals): data_width=15..18, n_iter=13..16, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* Fewer pipeline registers should reduce area; aim at the accuracy-feasible region (>=12 bits) with small m so the 32-request batch still finishes within 0.5 us.

**Result (code):** 20 evaluations this round, 120 total; 23 feasible; hypervolume 1.205e+05 (+2.2%).

**LLM decision:** `stop` — This is the final round, so the only valid choices are stop or infeasible. The constraints are met: 23 of 120 evaluations are feasible, and the front has 8 designs. Its area runs from 29151 to 49611 um2 and its accuracy from 12.3 to 14.2 bits. The cheapest feasible design is pipelined_m (data_width=17, n_iter=14, m=2) at 29151 um2 with max_abs_err 0.000204, inside the 0.000244 limit. It also meets throughput (78.8 MSPS against the 32 required). Hypervolume gain last round was +2.2%, so the front is still improving slowly, but there are no rounds left to act on that.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.205e+05 (gain this round: +2.2%).
Feasible designs: 23 of 120 evaluations (16 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 180
- max_abs_err <= 0.000244141: 78% violate; best seen 5.46e-05 (2^-14.16)
- sys_p99_batch_us <= 0.5: 15% violate; best seen 0.244

Pareto front (feasible, 8 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=2] area_um2=29151, accuracy_bits=12.3, ffs=439, throughput_msps=78.8, max_abs_err=0.000204 (2^-12.26), power_index=1.33
- pipelined [data_width=17 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=42962, accuracy_bits=12.7, ffs=928, throughput_msps=143, max_abs_err=0.000149 (2^-12.71), power_index=2.46
- pipelined [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=round] area_um2=43671, accuracy_bits=12.8, ffs=923, throughput_msps=138, max_abs_err=0.00014 (2^-12.80), power_index=2.47
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] area_um2=44427, accuracy_bits=13, ffs=960, throughput_msps=143, max_abs_err=0.000121 (2^-13.02), power_index=2.54
- pipelined [data_width=17 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=45985, accuracy_bits=13, ffs=973, throughput_msps=138, max_abs_err=0.00012 (2^-13.03), power_index=2.6
- pipelined [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=46450, accuracy_bits=13.1, ffs=999, throughput_msps=138, max_abs_err=0.000116 (2^-13.08), power_index=2.65
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=46462, accuracy_bits=13.6, ffs=982, throughput_msps=132, max_abs_err=8.26e-05 (2^-13.56), power_index=2.62
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
Front coverage: area_um2 29151..49611 (HV reference 100000); accuracy_bits 12.3..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 90 evals, 22 feasible; max throughput seen 180 MSPS; best accuracy 14.16 bits; best feasible area_um2=38197; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 30 evals, 1 feasible; max throughput seen 102 MSPS; best accuracy 13.92 bits; best feasible area_um2=29151; feasible ranges: data_width 17..17, n_iter 14..14, angle_guard 1..1, frac_guard 0..0, m 2..2
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (10 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)
- `pipelined` (70 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (7 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 61 feasible; hypervolume 2.509e+05 (+108.1%).

**No LLM call** (code's front-mapping round): This is the final round, so the only valid choices are stop or infeasible. The constraints are met: 23 of 120 evaluations are feasible, and the front has 8 designs. Its area runs from 29151 to 49611 um2 and its accuracy from 12.3 to 14.2 bits. The cheapest feasible design is pipelined_m (data_width=17, n_iter=14, m=2) at 29151 um2 with max_abs_err 0.000204, inside the 0.000244 limit. It also meets throughput (78.8 MSPS against the 32 required). Hypervolume gain last round was +2.2%, so the front is still improving slowly, but there are no rounds left to act on that.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 2.509e+05 (gain this round: +108.1%).
Feasible designs: 61 of 200 evaluations (53 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 4% violate; best seen 180
- max_abs_err <= 0.000244141: 51% violate; best seen 2.86e-08 (2^-25.06)
- sys_p99_batch_us <= 0.5: 26% violate; best seen 0.244

Pareto front (feasible, 16 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=2] area_um2=29151, accuracy_bits=12.3, ffs=439, throughput_msps=78.8, max_abs_err=0.000204 (2^-12.26), power_index=1.33
- pipelined [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=round] area_um2=43671, accuracy_bits=12.8, ffs=923, throughput_msps=138, max_abs_err=0.00014 (2^-12.80), power_index=2.47
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] area_um2=44427, accuracy_bits=13, ffs=960, throughput_msps=143, max_abs_err=0.000121 (2^-13.02), power_index=2.54
- pipelined [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=46450, accuracy_bits=13.1, ffs=999, throughput_msps=138, max_abs_err=0.000116 (2^-13.08), power_index=2.65
- pipelined [data_width=18 n_iter=17 angle_guard=2 frac_guard=0 rounding=round] area_um2=48851, accuracy_bits=13.7, ffs=1053, throughput_msps=132, max_abs_err=7.75e-05 (2^-13.65), power_index=2.79
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
- pipelined [data_width=21 n_iter=17 angle_guard=2 frac_guard=0 rounding=round] area_um2=55870, accuracy_bits=15.5, ffs=1203, throughput_msps=119, max_abs_err=2.18e-05 (2^-15.48), power_index=3.19
- pipelined [data_width=22 n_iter=20 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=67871, accuracy_bits=16.3, ffs=1455, throughput_msps=119, max_abs_err=1.22e-05 (2^-16.32), power_index=3.87
- pipelined [data_width=21 n_iter=20 angle_guard=1 frac_guard=3 rounding=trunc] area_um2=70375, accuracy_bits=16.7, ffs=1502, throughput_msps=115, max_abs_err=9.21e-06 (2^-16.73), power_index=4
- pipelined [data_width=27 n_iter=19 angle_guard=-2 frac_guard=0 rounding=trunc] area_um2=74886, accuracy_bits=17.8, ffs=1606, throughput_msps=105, max_abs_err=4.28e-06 (2^-17.83), power_index=4.27
Front coverage: area_um2 29151..74886 (HV reference 100000); accuracy_bits 12.3..17.8 (HV reference 12); data_width on the front 17..27 (registry 8..28).

Per family:
- pipelined: 160 evals, 60 feasible; max throughput seen 180 MSPS; best accuracy 23.59 bits; best feasible area_um2=38197; feasible ranges: data_width 16..28, n_iter 14..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 40 evals, 1 feasible; max throughput seen 102 MSPS; best accuracy 25.06 bits; best feasible area_um2=29151; feasible ranges: data_width 17..17, n_iter 14..14, angle_guard 1..1, frac_guard 0..0, m 2..2
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 16513 in, 3019 out
- provider-reported cost: $0.0632
- full prompts and replies: `llm_trace.jsonl`

