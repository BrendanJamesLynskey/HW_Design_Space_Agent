# DSE run: asic_multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: anthropic/claude-sonnet-5.5.  
**Evaluations:** 200 of 200 budgeted, over 2 round(s).  
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
`pipelined:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 39385 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10493 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 834 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 112 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.23 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000204 (2^-12.26) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.34 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 5.69e-05 (2^-14.10) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 0.932 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.3 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (17 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=round` | 39385 | 834 | 143.2 | 16 | 2.23 | 0.000204 (2^-12.26) | 12.26 |
| 1 | `pipelined:data_width=16,n_iter=14,angle_guard=2,frac_guard=3,rounding=round` | 40573 | 857 | 137.6 | 16 | 2.29 | 0.000187 (2^-12.38) | 12.38 |
| 2 | `pipelined:data_width=16,n_iter=14,angle_guard=4,frac_guard=3,rounding=round` | 41848 | 885 | 132.4 | 16 | 2.36 | 0.000166 (2^-12.56) | 12.56 |
| 3 | `pipelined:data_width=19,n_iter=14,angle_guard=0,frac_guard=2,rounding=round` | 44002 | 930 | 127.5 | 16 | 2.48 | 0.000151 (2^-12.69) | 12.69 |
| 4 | `pipelined:data_width=16,n_iter=16,angle_guard=3,frac_guard=2,rounding=round` | 45846 | 969 | 137.6 | 18 | 2.59 | 0.000117 (2^-13.06) | 13.06 |
| 5 | `pipelined:data_width=16,n_iter=17,angle_guard=2,frac_guard=3,rounding=round` | 49451 | 1043 | 137.6 | 19 | 2.79 | 0.000113 (2^-13.11) | 13.11 |
| 6 | `pipelined:data_width=16,n_iter=18,angle_guard=4,frac_guard=2,rounding=round` | 52497 | 1109 | 132.4 | 20 | 2.96 | 0.000103 (2^-13.24) | 13.24 |
| 7 | `pipelined:data_width=19,n_iter=17,angle_guard=2,frac_guard=1,rounding=trunc` | 52663 | 1133 | 127.5 | 19 | 3.01 | 5.59e-05 (2^-14.13) | 14.13 |
| 8 | `pipelined:data_width=19,n_iter=17,angle_guard=3,frac_guard=2,rounding=trunc` | 54916 | 1179 | 123.1 | 19 | 3.13 | 3.38e-05 (2^-14.85) | 14.85 |
| 9 | `pipelined:data_width=20,n_iter=17,angle_guard=3,frac_guard=1,rounding=trunc` | 55783 | 1199 | 118.9 | 19 | 3.19 | 3.13e-05 (2^-14.96) | 14.96 |
| 10 | `pipelined:data_width=20,n_iter=17,angle_guard=4,frac_guard=1,rounding=round` | 57629 | 1218 | 115.0 | 19 | 3.25 | 2.24e-05 (2^-15.45) | 15.45 |
| 11 | `pipelined:data_width=20,n_iter=17,angle_guard=3,frac_guard=3,rounding=trunc` | 58728 | 1258 | 118.9 | 19 | 3.35 | 2.19e-05 (2^-15.48) | 15.48 |
| 12 | `pipelined:data_width=20,n_iter=17,angle_guard=2,frac_guard=3,rounding=round` | 59014 | 1244 | 118.9 | 19 | 3.32 | 2.07e-05 (2^-15.56) | 15.56 |
| 13 | `pipelined:data_width=20,n_iter=18,angle_guard=2,frac_guard=2,rounding=round` | 60974 | 1286 | 123.1 | 20 | 3.44 | 1.51e-05 (2^-16.01) | 16.01 |
| 14 | `pipelined:data_width=19,n_iter=19,angle_guard=4,frac_guard=3,rounding=round` | 65144 | 1372 | 118.9 | 21 | 3.67 | 1.16e-05 (2^-16.39) | 16.39 |
| 15 | `pipelined:data_width=20,n_iter=19,angle_guard=4,frac_guard=3,rounding=trunc` | 66753 | 1427 | 115.0 | 21 | 3.8 | 1.05e-05 (2^-16.53) | 16.53 |
| 16 | `pipelined:data_width=20,n_iter=19,angle_guard=4,frac_guard=3,rounding=round` | 67819 | 1428 | 115.0 | 21 | 3.82 | 7.34e-06 (2^-17.06) | 17.06 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Pipelined is the only family that has met the constraints and it holds the whole merged front. I will concentrate most evaluations on trimming its area, using the narrower width and iteration ranges that still reach 12-bit accuracy. A small probe of pipelined_m with low m stays in case its fewer registers give a smaller feasible design. The iterative and unrolled families are covered by the other fleet member and have no feasible designs.*)
- `pipelined` (80 evals): data_width=12..16, n_iter=11..16, angle_guard=-2..2, frac_guard=0..3, rounding=trunc|round. *Why:* Only family with feasible designs (36 of 68), and all 13 front designs. Narrowing to the low-width, low-iteration corner should cut area while keeping max error at or below 2^-12 and a full 32 results/cycle capacity.
- `pipelined_m` (20 evals): data_width=12..16, n_iter=11..16, angle_guard=-2..2, frac_guard=0..3, rounding=trunc|round, m=2..3. *Why:* 0 of 32 feasible so far, probably because the batch latency bound fails. A small m with fewer registers might save area, so a small probe is kept with m limited to 2-3 to test whether it can meet the 0.5 us deadline.

**Result (code):** 100 evaluations this round, 100 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `widen` — No feasible design yet: 100% of evaluations violate max_abs_err <= 2^-12, and the best seen is 0.000311 (2^-11.65) at data_width 15-16. Throughput (best 190 MSPS vs 32 needed) and sys_p99_batch_us (best 0.237 vs 0.5, 12% violate) are met with wide margin, so accuracy is the only blocker. Reaching 2^-12 needs a smaller LSB plus guard bits, so data_width should go up to about 16-20 with n_iter about 14-20 and more frac_guard. Iterative and unrolled_k are not worth budget. The throughput bound of 32 MSPS and the 32-result burst within 0.5 us rule out multi-cycle designs, because 32 results at N+3 cycles each cannot fit. Pipelined and pipelined_m stay, and pipelined_m with larger m may give smaller area while keeping throughput of about 96 MSPS.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 190
- max_abs_err <= 0.000244141: 100% violate; best seen 0.000311 (2^-11.65)
- sys_p99_batch_us <= 0.5: 12% violate; best seen 0.237

No feasible design found yet. Least-violating designs:
- pipelined [data_width=15 n_iter=15 angle_guard=1 frac_guard=3 rounding=round]: throughput=143, max_abs_err=0.000314 (2^-11.64); max_abs_err <= 0.000244141 violated by 28.5%
- pipelined [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=trunc]: throughput=143, max_abs_err=0.000325 (2^-11.59); max_abs_err <= 0.000244141 violated by 33.1%
- pipelined [data_width=16 n_iter=16 angle_guard=0 frac_guard=2 rounding=round]: throughput=143, max_abs_err=0.00033 (2^-11.57); max_abs_err <= 0.000244141 violated by 35.1%
- pipelined [data_width=15 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc]: throughput=149, max_abs_err=0.000344 (2^-11.51); max_abs_err <= 0.000244141 violated by 40.8%
- pipelined [data_width=16 n_iter=15 angle_guard=0 frac_guard=3 rounding=trunc]: throughput=138, max_abs_err=0.000355 (2^-11.46); max_abs_err <= 0.000244141 violated by 45.2%

Per family:
- pipelined: 80 evals, 0 feasible; max throughput seen 190 MSPS; best accuracy 11.64 bits
- pipelined_m: 20 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 11.65 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Move the accuracy parameters upward to find the first feasible designs, then minimise area among them.*)
- `pipelined` (50 evals): data_width=15..20, n_iter=13..20, angle_guard=0..4, frac_guard=1..4, rounding=trunc|round. *Why:* Highest throughput, and the best accuracy so far came from here. Shifting up in width and iterations should cross the 2^-12 threshold.
- `pipelined_m` (50 evals): data_width=15..20, n_iter=13..20, angle_guard=0..4, frac_guard=1..4, rounding=trunc|round, m=2..4. *Why:* Fewer pipeline registers should reduce area while still meeting the 32 MSPS and 0.5 us batch constraints. It reached 11.65 bits in round 1.

**Result (code):** 100 evaluations this round, 200 total; 44 feasible; hypervolume 2.265e+05 (+inf).

**LLM decision:** `stop` — The evaluation budget is fully used (200 of 200) and this is the final round, so only stop or infeasible are valid. The constraints are clearly reachable: 44 of 200 evaluations are feasible and the front has 17 designs. The cheapest feasible design is pipelined at W=16, N=14, with 39385 um2, 12.3 accuracy bits, 143 MSPS and max error 0.000204 (below the 0.000244 limit). The front spans area 39385 to 67819 um2 and accuracy 12.3 to 17.1 bits, so it covers the trade-off well. The pipelined family dominates the front. pipelined_m produced 0 feasible designs out of 70.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 2.265e+05 (gain this round: +inf (first feasible designs)).
Feasible designs: 44 of 200 evaluations (35 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 190
- max_abs_err <= 0.000244141: 57% violate; best seen 7.34e-06 (2^-17.06)
- sys_p99_batch_us <= 0.5: 30% violate; best seen 0.237

Pareto front (feasible, 17 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=39385, accuracy_bits=12.3, ffs=834, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=2.23
- pipelined [data_width=16 n_iter=14 angle_guard=4 frac_guard=3 rounding=round] area_um2=41848, accuracy_bits=12.6, ffs=885, throughput_msps=132, max_abs_err=0.000166 (2^-12.56), power_index=2.36
- pipelined [data_width=16 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] area_um2=45846, accuracy_bits=13.1, ffs=969, throughput_msps=138, max_abs_err=0.000117 (2^-13.06), power_index=2.59
- pipelined [data_width=16 n_iter=17 angle_guard=2 frac_guard=3 rounding=round] area_um2=49451, accuracy_bits=13.1, ffs=1043, throughput_msps=138, max_abs_err=0.000113 (2^-13.11), power_index=2.79
- pipelined [data_width=19 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=52663, accuracy_bits=14.1, ffs=1133, throughput_msps=128, max_abs_err=5.59e-05 (2^-14.13), power_index=3.01
- pipelined [data_width=20 n_iter=17 angle_guard=3 frac_guard=1 rounding=trunc] area_um2=55783, accuracy_bits=15, ffs=1199, throughput_msps=119, max_abs_err=3.13e-05 (2^-14.96), power_index=3.19
- pipelined [data_width=20 n_iter=17 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=58728, accuracy_bits=15.5, ffs=1258, throughput_msps=119, max_abs_err=2.19e-05 (2^-15.48), power_index=3.35
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=3 rounding=round] area_um2=59014, accuracy_bits=15.6, ffs=1244, throughput_msps=119, max_abs_err=2.07e-05 (2^-15.56), power_index=3.32
- pipelined [data_width=19 n_iter=19 angle_guard=4 frac_guard=3 rounding=round] area_um2=65144, accuracy_bits=16.4, ffs=1372, throughput_msps=119, max_abs_err=1.16e-05 (2^-16.39), power_index=3.67
- pipelined [data_width=20 n_iter=19 angle_guard=4 frac_guard=3 rounding=round] area_um2=67819, accuracy_bits=17.1, ffs=1428, throughput_msps=115, max_abs_err=7.34e-06 (2^-17.06), power_index=3.82
Front coverage: area_um2 39385..67819 (HV reference 100000); accuracy_bits 12.3..17.1 (HV reference 12); data_width on the front 16..20 (registry 8..28).

Per family:
- pipelined: 130 evals, 44 feasible; max throughput seen 190 MSPS; best accuracy 17.06 bits; best feasible area_um2=39385; feasible ranges: data_width 15..20, n_iter 14..20, angle_guard 0..4, frac_guard 1..4
- pipelined_m: 70 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 15.88 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 16156 in, 2311 out
- provider-reported cost: $0.0554
- full prompts and replies: `llm_trace.jsonl`

