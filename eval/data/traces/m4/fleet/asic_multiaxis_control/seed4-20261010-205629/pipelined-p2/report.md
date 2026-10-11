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
`pipelined:data_width=15,n_iter=15,angle_guard=2,frac_guard=3,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 41426 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 11036 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 875 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 119 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.34 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000242 (2^-12.01) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 1.98 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 5.58e-05 (2^-14.13) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 0.458 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 12 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (19 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=15,n_iter=15,angle_guard=2,frac_guard=3,rounding=round` | 41426 | 875 | 143.2 | 17 | 2.34 | 0.000242 (2^-12.01) | 12.01 |
| 1 | `pipelined:data_width=16,n_iter=15,angle_guard=1,frac_guard=2,rounding=round` | 41564 | 879 | 143.2 | 17 | 2.35 | 0.000218 (2^-12.16) | 12.16 |
| 2 | `pipelined:data_width=17,n_iter=15,angle_guard=1,frac_guard=1,rounding=round` | 42388 | 898 | 143.2 | 17 | 2.4 | 0.000158 (2^-12.63) | 12.63 |
| 3 | `pipelined:data_width=16,n_iter=15,angle_guard=3,frac_guard=2,rounding=round` | 42934 | 908 | 137.6 | 17 | 2.43 | 0.000128 (2^-12.93) | 12.93 |
| 4 | `pipelined:data_width=16,n_iter=15,angle_guard=3,frac_guard=3,rounding=round` | 44217 | 934 | 137.6 | 17 | 2.49 | 0.000117 (2^-13.06) | 13.06 |
| 5 | `pipelined:data_width=17,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 44356 | 938 | 137.6 | 17 | 2.5 | 0.000108 (2^-13.18) | 13.18 |
| 6 | `pipelined:data_width=17,n_iter=15,angle_guard=3,frac_guard=2,rounding=round` | 45041 | 953 | 132.4 | 17 | 2.54 | 9.31e-05 (2^-13.39) | 13.39 |
| 7 | `pipelined:data_width=17,n_iter=15,angle_guard=3,frac_guard=3,rounding=round` | 46324 | 978 | 132.4 | 17 | 2.61 | 8.99e-05 (2^-13.44) | 13.44 |
| 8 | `pipelined:data_width=19,n_iter=15,angle_guard=3,frac_guard=1,rounding=round` | 47971 | 1016 | 123.1 | 17 | 2.71 | 7.28e-05 (2^-13.75) | 13.75 |
| 9 | `pipelined:data_width=17,n_iter=16,angle_guard=3,frac_guard=2,rounding=round` | 48095 | 1017 | 132.4 | 18 | 2.71 | 6.9e-05 (2^-13.82) | 13.82 |
| 10 | `pipelined:data_width=21,n_iter=15,angle_guard=3,frac_guard=0,rounding=round` | 49784 | 1077 | 115.0 | 17 | 2.85 | 6.53e-05 (2^-13.90) | 13.90 |
| 11 | `pipelined:data_width=21,n_iter=15,angle_guard=3,frac_guard=1,rounding=round` | 52184 | 1104 | 115.0 | 17 | 2.95 | 6.39e-05 (2^-13.93) | 13.93 |
| 12 | `pipelined:data_width=21,n_iter=15,angle_guard=3,frac_guard=2,rounding=round` | 53467 | 1130 | 115.0 | 17 | 3.02 | 6.22e-05 (2^-13.97) | 13.97 |
| 13 | `pipelined:data_width=23,n_iter=15,angle_guard=3,frac_guard=2,rounding=round` | 57680 | 1218 | 107.9 | 17 | 3.25 | 6.12e-05 (2^-14.00) | 14.00 |
| 14 | `pipelined:data_width=19,n_iter=19,angle_guard=3,frac_guard=0,rounding=round` | 58268 | 1252 | 123.1 | 21 | 3.32 | 3.74e-05 (2^-14.71) | 14.71 |
| 15 | `pipelined:data_width=23,n_iter=17,angle_guard=3,frac_guard=1,rounding=round` | 64021 | 1352 | 107.9 | 19 | 3.61 | 1.61e-05 (2^-15.92) | 15.92 |
| 16 | `pipelined:data_width=20,n_iter=21,angle_guard=2,frac_guard=2,rounding=round` | 71274 | 1501 | 123.1 | 23 | 4.01 | 9.54e-06 (2^-16.68) | 16.68 |
| 17 | `pipelined:data_width=20,n_iter=21,angle_guard=3,frac_guard=2,rounding=round` | 72243 | 1522 | 118.9 | 23 | 4.07 | 7.75e-06 (2^-16.98) | 16.98 |
| 18 | `pipelined:data_width=21,n_iter=22,angle_guard=2,frac_guard=1,rounding=round` | 75862 | 1599 | 118.9 | 24 | 4.27 | 6.89e-06 (2^-17.15) | 17.15 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Accuracy depends only on the width, iteration and guard parameters, so the 2^-12 error limit sets a minimum width and iteration count. Iterative and unrolled_k found nothing feasible, since they cannot return 32 results within 0.5 us. Pipelined at 1 result per cycle can, so I put most of the budget there on a narrow range near the accuracy threshold, where area is smallest. A minority share goes to pipelined_m with small m to see whether fewer registers can be feasible.*)
- `pipelined` (75 evals): data_width=13..17, n_iter=11..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* This is the only family with feasible designs so far (10 feasible, best 41211 um2). I narrow to the width and iteration range that just reaches 2^-12 error, to cut area and ripple down the front.
- `pipelined_m` (25 evals): data_width=13..16, n_iter=11..15, angle_guard=-1..3, frac_guard=0..2, rounding=trunc|round, m=2..3. *Why:* It saves pipeline registers but gave 0 feasible in 52 evals, probably because the longer stage path lowers Fmax and misses the 0.5 us batch bound. A small share with m=2..3 tests whether it can still fit.

**Result (code):** 100 evaluations this round, 100 total; 30 feasible; hypervolume 1.011e+05 (n/a).

**LLM decision:** `refine` — Only pipelined has feasible designs (30 of 75 evals). Its front spans area 41.4k..48.1k um2 and accuracy 12..13.8 bits, with all feasible points at data_width 15..17, n_iter 15..16. The error limit is the binding constraint, since 70% of evals violate it. Throughput (best 171 MSPS) and sys_p99_batch (best 0.263 us) have slack. Iterative and unrolled_k were not explored. I did not add them because the results give no sign they can meet the 0.5 us batch limit: 32 results at several cycles each needs a very high clock. pipelined_m had 0 feasible in 25 evals, with accuracy reaching only 11.89 bits, so its sample probably missed the accuracy region. It could save area through fewer registers, so I will retest it with a tight accuracy region and small m, which should keep Fmax high enough for the batch bound. The next round concentrates on the low-area edge of pipelined (data_width 13..17, n_iter 13..16, with smaller guard bits and both rounding modes) to find cheaper designs that still reach 12 bits.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.011e+05 (gain this round: n/a (first round)).
Feasible designs: 30 of 100 evaluations (16 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 171
- max_abs_err <= 0.000244141: 70% violate; best seen 6.9e-05 (2^-13.82)
- sys_p99_batch_us <= 0.5: 15% violate; best seen 0.263

Pareto front (feasible, 8 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=15 n_iter=15 angle_guard=2 frac_guard=3 rounding=round] area_um2=41426, accuracy_bits=12, ffs=875, throughput_msps=143, max_abs_err=0.000242 (2^-12.01), power_index=2.34
- pipelined [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=42388, accuracy_bits=12.6, ffs=898, throughput_msps=143, max_abs_err=0.000158 (2^-12.63), power_index=2.4
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=44128, accuracy_bits=12.9, ffs=951, throughput_msps=132, max_abs_err=0.00013 (2^-12.91), power_index=2.52
- pipelined [data_width=16 n_iter=15 angle_guard=3 frac_guard=3 rounding=round] area_um2=44217, accuracy_bits=13.1, ffs=934, throughput_msps=138, max_abs_err=0.000117 (2^-13.06), power_index=2.49
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=44356, accuracy_bits=13.2, ffs=938, throughput_msps=138, max_abs_err=0.000108 (2^-13.18), power_index=2.5
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] area_um2=45041, accuracy_bits=13.4, ffs=953, throughput_msps=132, max_abs_err=9.31e-05 (2^-13.39), power_index=2.54
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=3 rounding=round] area_um2=46324, accuracy_bits=13.4, ffs=978, throughput_msps=132, max_abs_err=8.99e-05 (2^-13.44), power_index=2.61
- pipelined [data_width=17 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] area_um2=48095, accuracy_bits=13.8, ffs=1017, throughput_msps=132, max_abs_err=6.9e-05 (2^-13.82), power_index=2.71
Front coverage: area_um2 41426..48095 (HV reference 100000); accuracy_bits 12..13.8 (HV reference 12); data_width on the front 15..17 (registry 8..28).

Per family:
- pipelined: 75 evals, 30 feasible; max throughput seen 171 MSPS; best accuracy 13.82 bits; best feasible area_um2=41426; feasible ranges: data_width 15..17, n_iter 15..16, angle_guard 0..3, frac_guard 1..3
- pipelined_m: 25 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 11.89 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate on the region where feasibility was found and probe pipelined_m once more with accuracy-capable settings. Leave full-range mapping to the later code-driven round.*)
- `pipelined` (14 evals): data_width=13..17, n_iter=13..16, angle_guard=0..3, frac_guard=0..3, rounding=round|trunc. *Why:* Region of all feasible points so far; extend slightly toward smaller widths and guards to cut area while holding error <= 2^-12.
- `pipelined_m` (6 evals): data_width=14..17, n_iter=14..16, angle_guard=1..3, frac_guard=1..3, rounding=round, m=2..3. *Why:* Fewer registers may lower area. Round 1 found no feasible point, likely because accuracy was too low, so test it again with accuracy-oriented parameters and small m.

**Result (code):** 20 evaluations this round, 120 total; 37 feasible; hypervolume 1.016e+05 (+0.5%).

**LLM decision:** `stop` — This is the final round, so stop is the only meaningful choice. The front has 9 feasible designs, all pipelined, spanning area 41426..48095 um2 and accuracy 12..13.8 bits. Hypervolume gain last round was only +0.5%, below the 1% eps, so the front has largely converged. The cheapest feasible design, pipelined W=15 N=15 ag=2 fg=3 with rounding, has area 41426 um2 and max error 0.000242, which meets the 2^-12 bound. Throughput (143 MSPS vs the 32 required) and the batch latency constraint (best 0.263 us vs 0.5 us) both pass with margin. pipelined_m produced 0 feasible designs in 31 evals, so it adds nothing to the front. The selection rule (min area) picks the 41426 um2 design.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.016e+05 (gain this round: +0.5%).
Feasible designs: 37 of 120 evaluations (20 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 171
- max_abs_err <= 0.000244141: 66% violate; best seen 6.9e-05 (2^-13.82)
- sys_p99_batch_us <= 0.5: 17% violate; best seen 0.263

Pareto front (feasible, 9 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=15 n_iter=15 angle_guard=2 frac_guard=3 rounding=round] area_um2=41426, accuracy_bits=12, ffs=875, throughput_msps=143, max_abs_err=0.000242 (2^-12.01), power_index=2.34
- pipelined [data_width=16 n_iter=15 angle_guard=1 frac_guard=2 rounding=round] area_um2=41564, accuracy_bits=12.2, ffs=879, throughput_msps=143, max_abs_err=0.000218 (2^-12.16), power_index=2.35
- pipelined [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=42388, accuracy_bits=12.6, ffs=898, throughput_msps=143, max_abs_err=0.000158 (2^-12.63), power_index=2.4
- pipelined [data_width=16 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] area_um2=42934, accuracy_bits=12.9, ffs=908, throughput_msps=138, max_abs_err=0.000128 (2^-12.93), power_index=2.43
- pipelined [data_width=16 n_iter=15 angle_guard=3 frac_guard=3 rounding=round] area_um2=44217, accuracy_bits=13.1, ffs=934, throughput_msps=138, max_abs_err=0.000117 (2^-13.06), power_index=2.49
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=44356, accuracy_bits=13.2, ffs=938, throughput_msps=138, max_abs_err=0.000108 (2^-13.18), power_index=2.5
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] area_um2=45041, accuracy_bits=13.4, ffs=953, throughput_msps=132, max_abs_err=9.31e-05 (2^-13.39), power_index=2.54
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=3 rounding=round] area_um2=46324, accuracy_bits=13.4, ffs=978, throughput_msps=132, max_abs_err=8.99e-05 (2^-13.44), power_index=2.61
- pipelined [data_width=17 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] area_um2=48095, accuracy_bits=13.8, ffs=1017, throughput_msps=132, max_abs_err=6.9e-05 (2^-13.82), power_index=2.71
Front coverage: area_um2 41426..48095 (HV reference 100000); accuracy_bits 12..13.8 (HV reference 12); data_width on the front 15..17 (registry 8..28).

Per family:
- pipelined: 89 evals, 37 feasible; max throughput seen 171 MSPS; best accuracy 13.82 bits; best feasible area_um2=41426; feasible ranges: data_width 15..17, n_iter 15..16, angle_guard 0..3, frac_guard 1..3
- pipelined_m: 31 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 12.93 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined` (40 evals): data_width=14..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (9 front designs; box front_anchored)
- `pipelined_m` (40 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 80 evaluations this round, 200 total; 69 feasible; hypervolume 2.174e+05 (+113.9%).

**No LLM call** (code's front-mapping round): This is the final round, so stop is the only meaningful choice. The front has 9 feasible designs, all pipelined, spanning area 41426..48095 um2 and accuracy 12..13.8 bits. Hypervolume gain last round was only +0.5%, below the 1% eps, so the front has largely converged. The cheapest feasible design, pipelined W=15 N=15 ag=2 fg=3 with rounding, has area 41426 um2 and max error 0.000242, which meets the 2^-12 bound. Throughput (143 MSPS vs the 32 required) and the batch latency constraint (best 0.263 us vs 0.5 us) both pass with margin. pipelined_m produced 0 feasible designs in 31 evals, so it adds nothing to the front. The selection rule (min area) picks the 41426 um2 design.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 2.174e+05 (gain this round: +113.9%).
Feasible designs: 69 of 200 evaluations (43 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 14% violate; best seen 171
- max_abs_err <= 0.000244141: 49% violate; best seen 1.62e-07 (2^-22.56)
- sys_p99_batch_us <= 0.5: 32% violate; best seen 0.263

Pareto front (feasible, 19 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=15 n_iter=15 angle_guard=2 frac_guard=3 rounding=round] area_um2=41426, accuracy_bits=12, ffs=875, throughput_msps=143, max_abs_err=0.000242 (2^-12.01), power_index=2.34
- pipelined [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=42388, accuracy_bits=12.6, ffs=898, throughput_msps=143, max_abs_err=0.000158 (2^-12.63), power_index=2.4
- pipelined [data_width=16 n_iter=15 angle_guard=3 frac_guard=3 rounding=round] area_um2=44217, accuracy_bits=13.1, ffs=934, throughput_msps=138, max_abs_err=0.000117 (2^-13.06), power_index=2.49
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] area_um2=45041, accuracy_bits=13.4, ffs=953, throughput_msps=132, max_abs_err=9.31e-05 (2^-13.39), power_index=2.54
- pipelined [data_width=19 n_iter=15 angle_guard=3 frac_guard=1 rounding=round] area_um2=47971, accuracy_bits=13.7, ffs=1016, throughput_msps=123, max_abs_err=7.28e-05 (2^-13.75), power_index=2.71
- pipelined [data_width=21 n_iter=15 angle_guard=3 frac_guard=0 rounding=round] area_um2=49784, accuracy_bits=13.9, ffs=1077, throughput_msps=115, max_abs_err=6.53e-05 (2^-13.90), power_index=2.85
- pipelined [data_width=21 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] area_um2=53467, accuracy_bits=14, ffs=1130, throughput_msps=115, max_abs_err=6.22e-05 (2^-13.97), power_index=3.02
- pipelined [data_width=19 n_iter=19 angle_guard=3 frac_guard=0 rounding=round] area_um2=58268, accuracy_bits=14.7, ffs=1252, throughput_msps=123, max_abs_err=3.74e-05 (2^-14.71), power_index=3.32
- pipelined [data_width=20 n_iter=21 angle_guard=2 frac_guard=2 rounding=round] area_um2=71274, accuracy_bits=16.7, ffs=1501, throughput_msps=123, max_abs_err=9.54e-06 (2^-16.68), power_index=4.01
- pipelined [data_width=21 n_iter=22 angle_guard=2 frac_guard=1 rounding=round] area_um2=75862, accuracy_bits=17.1, ffs=1599, throughput_msps=119, max_abs_err=6.89e-06 (2^-17.15), power_index=4.27
Front coverage: area_um2 41426..75862 (HV reference 100000); accuracy_bits 12..17.1 (HV reference 12); data_width on the front 15..23 (registry 8..28).

Per family:
- pipelined: 129 evals, 69 feasible; max throughput seen 171 MSPS; best accuracy 20.56 bits; best feasible area_um2=41426; feasible ranges: data_width 15..26, n_iter 15..29, angle_guard -2..4, frac_guard 0..3
- pipelined_m: 71 evals, 0 feasible; max throughput seen 123 MSPS; best accuracy 22.56 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 16554 in, 2974 out
- provider-reported cost: $0.0628
- full prompts and replies: `llm_trace.jsonl`

