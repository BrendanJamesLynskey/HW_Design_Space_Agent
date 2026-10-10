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
`pipelined:data_width=17,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 38060 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10140 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 826 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 138 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 138 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 116 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.19 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000194 (2^-12.33) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 6.36 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 6.02e-05 (2^-14.02) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.97 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=17,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 38060 | 826 | 137.6 | 16 | 2.19 | 0.000194 (2^-12.33) | 12.33 |
| 1 | `pipelined:data_width=17,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` | 40161 | 851 | 137.6 | 16 | 2.27 | 0.000191 (2^-12.36) | 12.36 |
| 2 | `pipelined:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 40192 | 870 | 143.2 | 17 | 2.31 | 0.000168 (2^-12.54) | 12.54 |
| 3 | `pipelined:data_width=17,n_iter=15,angle_guard=2,frac_guard=1,rounding=round` | 43073 | 912 | 137.6 | 17 | 2.43 | 0.00013 (2^-12.91) | 12.91 |
| 4 | `pipelined:data_width=17,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 44356 | 938 | 137.6 | 17 | 2.5 | 0.000108 (2^-13.18) | 13.18 |
| 5 | `pipelined:data_width=20,n_iter=19,angle_guard=2,frac_guard=0,rounding=trunc` | 60018 | 1289 | 123.1 | 21 | 3.42 | 4.23e-05 (2^-14.53) | 14.53 |
| 6 | `pipelined:data_width=20,n_iter=19,angle_guard=2,frac_guard=2,rounding=trunc` | 63342 | 1356 | 123.1 | 21 | 3.61 | 1.63e-05 (2^-15.90) | 15.90 |
| 7 | `pipelined:data_width=21,n_iter=20,angle_guard=4,frac_guard=1,rounding=trunc` | 69628 | 1490 | 111.3 | 22 | 3.96 | 1.31e-05 (2^-16.21) | 16.21 |
| 8 | `pipelined:data_width=21,n_iter=20,angle_guard=4,frac_guard=2,rounding=trunc` | 71385 | 1526 | 111.3 | 22 | 4.06 | 7.58e-06 (2^-17.01) | 17.01 |
| 9 | `pipelined:data_width=23,n_iter=19,angle_guard=4,frac_guard=2,rounding=trunc` | 72963 | 1561 | 104.7 | 21 | 4.15 | 4.79e-06 (2^-17.67) | 17.67 |
| 10 | `pipelined:data_width=26,n_iter=19,angle_guard=1,frac_guard=1,rounding=trunc` | 76548 | 1640 | 104.7 | 21 | 4.36 | 4.03e-06 (2^-17.92) | 17.92 |
| 11 | `pipelined:data_width=23,n_iter=20,angle_guard=4,frac_guard=2,rounding=trunc` | 76917 | 1644 | 104.7 | 22 | 4.37 | 3.08e-06 (2^-18.31) | 18.31 |
| 12 | `pipelined:data_width=26,n_iter=20,angle_guard=1,frac_guard=1,rounding=round` | 82065 | 1728 | 104.7 | 22 | 4.62 | 2.11e-06 (2^-18.85) | 18.85 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Pipelined designs are the only feasible ones so far. The iterative and unrolled families issue results too slowly for a 32-request burst. I concentrate most of the budget on pipelined inside the data_width, n_iter and guard-bit region that should still meet max error <= 2^-12, to push area below the current best of 40877 while keeping the accuracy trade-off covered. A small probe of pipelined_m at m=2..3 checks whether fewer registers can pass the batch-latency bound. If it still yields no feasible designs, later rounds can drop it.*)
- `pipelined` (80 evals): data_width=13..17, n_iter=10..15, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* It is the only family with feasible designs so far (30 of 47) and holds the whole merged front. Narrowing to the low-width, low-iteration corner that still meets the 2^-12 error bound should cut area further while keeping the accuracy objective covered.
- `pipelined_m` (20 evals): data_width=13..17, n_iter=10..15, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, m=2..3. *Why:* Registering every m stages removes flip-flops, which could lower area, but 53 evaluations found 0 feasible. Larger m probably breaks the 0.5 us batch deadline, so I probe only m=2..3 with a small share.

**Result (code):** 100 evaluations this round, 100 total; 16 feasible; hypervolume 6.884e+04 (n/a).

**LLM decision:** `refine` — Only pipelined designs are feasible so far (16 of 100 evals), with area 38060..44356 um2 and 12.3..13.2 accuracy bits. The accuracy constraint is what kills most evals (83% violate). Throughput (180 MSPS best) and the batch bound (18% violate, best 0.233 us) are not limiting. Feasible designs sit at data_width 16..17 and n_iter 14..15, so area can likely still drop by trimming width and iterations near the 2^-12 error edge, with frac_guard and rounding=round used to recover accuracy. pipelined_m got 0 feasible in 20 evals, but its best accuracy of 12.17 bits is close and it should need fewer FFs. Its 86.6 MSPS best throughput is still above the 32 MSPS constraint and plausibly fits the 0.5 us batch bound, so it gets one more focused try. Iterative and unrolled_k are skipped: 32 simultaneous requests at several cycles each cannot finish within 0.5 us. The next round narrows to the promising region and leaves a later round for map_front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 6.884e+04 (gain this round: n/a (first round)).
Feasible designs: 16 of 100 evaluations (12 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 180
- max_abs_err <= 0.000244141: 83% violate; best seen 0.000108 (2^-13.18)
- sys_p99_batch_us <= 0.5: 18% violate; best seen 0.233

Pareto front (feasible, 4 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=38060, accuracy_bits=12.3, ffs=826, throughput_msps=138, max_abs_err=0.000194 (2^-12.33), power_index=2.19
- pipelined [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=40192, accuracy_bits=12.5, ffs=870, throughput_msps=143, max_abs_err=0.000168 (2^-12.54), power_index=2.31
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] area_um2=43073, accuracy_bits=12.9, ffs=912, throughput_msps=138, max_abs_err=0.00013 (2^-12.91), power_index=2.43
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=44356, accuracy_bits=13.2, ffs=938, throughput_msps=138, max_abs_err=0.000108 (2^-13.18), power_index=2.5
Front coverage: area_um2 38060..44356 (HV reference 100000); accuracy_bits 12.3..13.2 (HV reference 12); data_width on the front 17..17 (registry 8..28).

Per family:
- pipelined: 80 evals, 16 feasible; max throughput seen 180 MSPS; best accuracy 13.18 bits; best feasible area_um2=38060; feasible ranges: data_width 16..17, n_iter 14..15, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 20 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 12.17 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate on the narrow region where feasibility appeared, push toward smaller area, and give pipelined_m a targeted attempt at the accuracy edge.*)
- `pipelined` (14 evals): data_width=14..17, n_iter=12..16, angle_guard=0..3, frac_guard=0..3, rounding=round. *Why:* All feasible designs are here. Probe slightly smaller widths and iteration counts to cut area while holding max error <= 2^-12.
- `pipelined_m` (6 evals): data_width=15..17, n_iter=13..16, angle_guard=0..3, frac_guard=0..3, rounding=round, m=2..3. *Why:* Fewer pipeline registers may cut area. Its best accuracy (12.17 bits) is near the limit, so it needs a higher-accuracy region and a small m to keep throughput and the batch bound met.

**Result (code):** 20 evaluations this round, 120 total; 18 feasible; hypervolume 6.884e+04 (+0.0%).

**LLM decision:** `stop` — This is the final round, so only stop or infeasible is allowed. The constraints are clearly reachable: 18 of 120 evaluations were feasible and the front has 5 designs. The cheapest feasible design is pipelined at data_width=17, n_iter=14, angle_guard=2, frac_guard=0 with rounding. It has area 38060 um2, 12.3 accuracy bits, throughput 138 MSPS, and meets the 2^-12 error bound. The last round added +0.0% hypervolume, so the front is no longer improving. The front covers area 38060..44356 and accuracy 12.3..13.2 bits. Families explored are pipelined and pipelined_m. pipelined_m had 0 feasible designs out of 26.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 6.884e+04 (gain this round: +0.0%).
Feasible designs: 18 of 120 evaluations (14 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 180
- max_abs_err <= 0.000244141: 82% violate; best seen 9.31e-05 (2^-13.39)
- sys_p99_batch_us <= 0.5: 18% violate; best seen 0.233

Pareto front (feasible, 5 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=38060, accuracy_bits=12.3, ffs=826, throughput_msps=138, max_abs_err=0.000194 (2^-12.33), power_index=2.19
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=40161, accuracy_bits=12.4, ffs=851, throughput_msps=138, max_abs_err=0.000191 (2^-12.36), power_index=2.27
- pipelined [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=40192, accuracy_bits=12.5, ffs=870, throughput_msps=143, max_abs_err=0.000168 (2^-12.54), power_index=2.31
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] area_um2=43073, accuracy_bits=12.9, ffs=912, throughput_msps=138, max_abs_err=0.00013 (2^-12.91), power_index=2.43
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=44356, accuracy_bits=13.2, ffs=938, throughput_msps=138, max_abs_err=0.000108 (2^-13.18), power_index=2.5
Front coverage: area_um2 38060..44356 (HV reference 100000); accuracy_bits 12.3..13.2 (HV reference 12); data_width on the front 17..17 (registry 8..28).

Per family:
- pipelined: 94 evals, 18 feasible; max throughput seen 180 MSPS; best accuracy 13.18 bits; best feasible area_um2=38060; feasible ranges: data_width 16..17, n_iter 14..15, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 26 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 13.39 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined` (40 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (5 front designs; box front_anchored)
- `pipelined_m` (40 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 80 evaluations this round, 200 total; 46 feasible; hypervolume 2.48e+05 (+260.3%).

**No LLM call** (code's front-mapping round): This is the final round, so only stop or infeasible is allowed. The constraints are clearly reachable: 18 of 120 evaluations were feasible and the front has 5 designs. The cheapest feasible design is pipelined at data_width=17, n_iter=14, angle_guard=2, frac_guard=0 with rounding. It has area 38060 um2, 12.3 accuracy bits, throughput 138 MSPS, and meets the 2^-12 error bound. The last round added +0.0% hypervolume, so the front is no longer improving. The front covers area 38060..44356 and accuracy 12.3..13.2 bits. Families explored are pipelined and pipelined_m. pipelined_m had 0 feasible designs out of 26.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 2.48e+05 (gain this round: +260.3%).
Feasible designs: 46 of 200 evaluations (38 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 12% violate; best seen 180
- max_abs_err <= 0.000244141: 56% violate; best seen 2.21e-07 (2^-22.11)
- sys_p99_batch_us <= 0.5: 36% violate; best seen 0.233

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=38060, accuracy_bits=12.3, ffs=826, throughput_msps=138, max_abs_err=0.000194 (2^-12.33), power_index=2.19
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=40161, accuracy_bits=12.4, ffs=851, throughput_msps=138, max_abs_err=0.000191 (2^-12.36), power_index=2.27
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] area_um2=43073, accuracy_bits=12.9, ffs=912, throughput_msps=138, max_abs_err=0.00013 (2^-12.91), power_index=2.43
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=44356, accuracy_bits=13.2, ffs=938, throughput_msps=138, max_abs_err=0.000108 (2^-13.18), power_index=2.5
- pipelined [data_width=20 n_iter=19 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=60018, accuracy_bits=14.5, ffs=1289, throughput_msps=123, max_abs_err=4.23e-05 (2^-14.53), power_index=3.42
- pipelined [data_width=21 n_iter=20 angle_guard=4 frac_guard=1 rounding=trunc] area_um2=69628, accuracy_bits=16.2, ffs=1490, throughput_msps=111, max_abs_err=1.31e-05 (2^-16.21), power_index=3.96
- pipelined [data_width=21 n_iter=20 angle_guard=4 frac_guard=2 rounding=trunc] area_um2=71385, accuracy_bits=17, ffs=1526, throughput_msps=111, max_abs_err=7.58e-06 (2^-17.01), power_index=4.06
- pipelined [data_width=23 n_iter=19 angle_guard=4 frac_guard=2 rounding=trunc] area_um2=72963, accuracy_bits=17.7, ffs=1561, throughput_msps=105, max_abs_err=4.79e-06 (2^-17.67), power_index=4.15
- pipelined [data_width=23 n_iter=20 angle_guard=4 frac_guard=2 rounding=trunc] area_um2=76917, accuracy_bits=18.3, ffs=1644, throughput_msps=105, max_abs_err=3.08e-06 (2^-18.31), power_index=4.37
- pipelined [data_width=26 n_iter=20 angle_guard=1 frac_guard=1 rounding=round] area_um2=82065, accuracy_bits=18.9, ffs=1728, throughput_msps=105, max_abs_err=2.11e-06 (2^-18.85), power_index=4.62
Front coverage: area_um2 38060..82065 (HV reference 100000); accuracy_bits 12.3..18.9 (HV reference 12); data_width on the front 17..26 (registry 8..28).

Per family:
- pipelined: 134 evals, 46 feasible; max throughput seen 180 MSPS; best accuracy 21.00 bits; best feasible area_um2=38060; feasible ranges: data_width 16..26, n_iter 14..27, angle_guard 0..4, frac_guard 0..4
- pipelined_m: 66 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 22.11 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 15712 in, 2909 out
- provider-reported cost: $0.0605
- full prompts and replies: `llm_trace.jsonl`

