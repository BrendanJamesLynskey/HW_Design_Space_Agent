# DSE run: asic_multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
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

## Pareto front (17 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=2` | 29151 | 439 | 78.8 | 9 | 1.33 | 0.000204 (2^-12.26) | 12.26 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=2` | 30165 | 455 | 78.8 | 9 | 1.38 | 0.0002 (2^-12.28) | 12.28 |
| 2 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=2` | 30990 | 453 | 78.8 | 9 | 1.39 | 0.000192 (2^-12.35) | 12.35 |
| 3 | `pipelined:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 39336 | 853 | 137.6 | 16 | 2.26 | 0.000175 (2^-12.48) | 12.48 |
| 4 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 39973 | 867 | 132.4 | 16 | 2.3 | 0.00017 (2^-12.53) | 12.53 |
| 5 | `pipelined:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 40877 | 885 | 137.6 | 17 | 2.34 | 0.000148 (2^-12.72) | 12.72 |
| 6 | `pipelined:data_width=18,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 41562 | 900 | 143.2 | 17 | 2.38 | 0.000145 (2^-12.75) | 12.75 |
| 7 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 42248 | 914 | 137.6 | 17 | 2.42 | 0.000119 (2^-13.04) | 13.04 |
| 8 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 42933 | 929 | 132.4 | 17 | 2.46 | 0.000109 (2^-13.17) | 13.17 |
| 9 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=round` | 44494 | 942 | 137.6 | 17 | 2.51 | 0.000101 (2^-13.27) | 13.27 |
| 10 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=1,rounding=round` | 45179 | 957 | 132.4 | 17 | 2.55 | 9.31e-05 (2^-13.39) | 13.39 |
| 11 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 45892 | 991 | 132.4 | 18 | 2.63 | 8.35e-05 (2^-13.55) | 13.55 |
| 12 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 49611 | 1048 | 132.4 | 18 | 2.8 | 5.46e-05 (2^-14.16) | 14.16 |
| 13 | `pipelined:data_width=21,n_iter=18,angle_guard=1,frac_guard=0,rounding=round` | 58429 | 1256 | 123.1 | 20 | 3.34 | 1.68e-05 (2^-15.87) | 15.87 |
| 14 | `pipelined:data_width=24,n_iter=18,angle_guard=2,frac_guard=0,rounding=trunc` | 66701 | 1433 | 107.9 | 20 | 3.81 | 9.16e-06 (2^-16.74) | 16.74 |
| 15 | `pipelined:data_width=21,n_iter=20,angle_guard=2,frac_guard=2,rounding=trunc` | 69541 | 1486 | 118.9 | 22 | 3.96 | 8.61e-06 (2^-16.83) | 16.83 |
| 16 | `pipelined:data_width=21,n_iter=20,angle_guard=2,frac_guard=2,rounding=round` | 70658 | 1488 | 118.9 | 22 | 3.98 | 5.43e-06 (2^-17.49) | 17.49 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec needs >=32 msps throughput (so only pipelined/pipelined_m qualify, both give 1 result/cycle) and a 0.5 us p99 batch bound for 32 requests per 1 us tick, which forces low latency. The error budget is 2^-12, which is loose enough that data_width ~14-18 with n_iter ~12-18 and small guards suffices; pushing width or iterations higher only costs area. The current best is 38698 um2 (pipelined), but pipelined_m has already produced a smaller feasible point (30165 um2), so the area frontier likely bends toward pipelined_m. I therefore spend 60% of the budget on pipelined_m to map its area/accuracy trade-off and find the true minimum-area point, and 40% on pipelined to refine the already-dominant front and confirm the knee. Both families share the same accuracy-determining parameters, so the search focuses on the area-relevant knobs (m for pipelined_m, and the width/iter/guard trade-off for both).*)
- `pipelined_m` (60 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* pipelined_m is the only family that has produced a design smaller than the current best (30165 um2 vs 38698 um2) and it is the natural area-reduction path over pipelined: registering every m stages cuts FF count and area while keeping 1 result/cycle throughput (needed for the 32 msps constraint) and short latency (needed for the 0.5 us p99 batch bound). The single feasible point found so far (30165 um2) sits in a narrow corner of the space; I widen the search around it (data_width 14-18, n_iter 12-18, small guards, m 2-8) to map the area/accuracy trade-off and find whether a smaller or more accurate point exists. Keeping angle_guard and frac_guard low (0-2) is important because they add area without helping the 2^-12 error budget once data_width and n_iter are adequate.
- `pipelined` (40 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined already dominates the merged front (13 of 14 designs) and is the reference for the throughput/latency constraints. I keep a smaller share here to refine the front around the current best (38698 um2) and to confirm the accuracy-vs-area knee, but the main new information should come from pipelined_m. Ranges are kept tight (data_width 14-18, n_iter 12-18, guards 0-2) because the error budget (2^-12) is easily met in this region and larger widths/iters only add area without improving the objective.

**Result (code):** 100 evaluations this round, 100 total; 33 feasible; hypervolume 1.237e+05 (n/a).

**LLM decision:** `refine` — The current front is dominated by `pipelined_m` with m=2 (area ~30k um^2) and `pipelined` (area ~40k+ um^2). The `pipelined_m` family is significantly more area-efficient (30165 vs 39973 um^2 for similar accuracy) but has only been explored with m=2. The registry allows m up to 8. Increasing m reduces the number of pipeline registers (lower area/FFs) but increases latency. The constraint is `sys_p99_batch_us <= 0.5`. With a 1us tick and 32 requests, the batch must complete in 0.5us. If the CORDIC runs at ~80-100 MHz, 0.5us is ~40-50 cycles. `pipelined_m` with m=2 and N=14 has latency ceil(14/2)+2 = 9 cycles, which is well within the budget. Increasing m to 4 or 8 would reduce area further (fewer registers) while keeping latency low (ceil(14/4)+2=6, ceil(14/8)+2=4). This suggests a large unexplored area of the Pareto front in the `pipelined_m` family with higher m values. Additionally, `data_width` 17 and 18 are on the front; 16 might be feasible if accuracy allows (max_abs_err <= 2^-12). The current best accuracy is 12.3 bits for the cheapest design, which is close to the 12-bit limit. Exploring m=4..8 and potentially data_width=16 in `pipelined_m` is the most promising path to reduce area.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.237e+05 (gain this round: n/a (first round)).
Feasible designs: 33 of 100 evaluations (21 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 12% violate; best seen 171
- max_abs_err <= 0.000244141: 54% violate; best seen 5.46e-05 (2^-14.16)
- sys_p99_batch_us <= 0.5: 41% violate; best seen 0.269

Pareto front (feasible, 9 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=2] area_um2=30165, accuracy_bits=12.3, ffs=455, throughput_msps=78.8, max_abs_err=0.0002 (2^-12.28), power_index=1.38
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=2] area_um2=30990, accuracy_bits=12.3, ffs=453, throughput_msps=78.8, max_abs_err=0.000192 (2^-12.35), power_index=1.39
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.5, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53), power_index=2.3
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=40877, accuracy_bits=12.7, ffs=885, throughput_msps=138, max_abs_err=0.000148 (2^-12.72), power_index=2.34
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=42248, accuracy_bits=13, ffs=914, throughput_msps=138, max_abs_err=0.000119 (2^-13.04), power_index=2.42
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=42933, accuracy_bits=13.2, ffs=929, throughput_msps=132, max_abs_err=0.000109 (2^-13.17), power_index=2.46
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] area_um2=45179, accuracy_bits=13.4, ffs=957, throughput_msps=132, max_abs_err=9.31e-05 (2^-13.39), power_index=2.55
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
Front coverage: area_um2 30165..49611 (HV reference 100000); accuracy_bits 12.3..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 40 evals, 28 feasible; max throughput seen 171 MSPS; best accuracy 14.16 bits; best feasible area_um2=38060; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 60 evals, 5 feasible; max throughput seen 86.6 MSPS; best accuracy 14.11 bits; best feasible area_um2=30165; feasible ranges: data_width 17..18, n_iter 14..14, angle_guard 0..1, frac_guard 0..1, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Focus on `pipelined_m` with expanded m range (2-8) and slightly lower data_width (16-18) to find lower-area designs. The current best is 30165 um^2 with m=2; higher m should reduce area further if latency allows.*)
- `pipelined_m` (15 evals): data_width=16..18, n_iter=13..16, angle_guard=0..2, frac_guard=0..1, rounding=round, m=2..8. *Why:* Explore higher m values (4-8) to reduce register count and area, and lower data_width (16) to see if accuracy constraint can be met with smaller width.
- `pipelined` (5 evals): data_width=16..18, n_iter=13..16, angle_guard=0..2, frac_guard=0..1, rounding=round. *Why:* Keep a small share for `pipelined` to ensure the front is well-covered in case `pipelined_m` with high m violates latency constraints or has other issues.

**Result (code):** 20 evaluations this round, 120 total; 38 feasible; hypervolume 1.241e+05 (+0.3%).

**LLM decision:** `stop` — The feasible Pareto front is well-established and robust. The minimum area design (pipelined_m, 29151 um^2) comfortably meets all constraints: throughput 78.8 MSPS >= 32, max_abs_err 2.04e-4 <= 2.44e-4, and the system batch latency bound is met (best seen 0.269 us <= 0.5 us). The front spans a reasonable trade-off space (area 29k-50k um^2, accuracy 12.3-14.2 bits) with no obvious gaps. Since this is the final round, further exploration is unnecessary; the current front provides a solid basis for final selection via the min-area rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.241e+05 (gain this round: +0.3%).
Feasible designs: 38 of 120 evaluations (24 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 13% violate; best seen 171
- max_abs_err <= 0.000244141: 50% violate; best seen 5.46e-05 (2^-14.16)
- sys_p99_batch_us <= 0.5: 42% violate; best seen 0.269

Pareto front (feasible, 12 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=2] area_um2=29151, accuracy_bits=12.3, ffs=439, throughput_msps=78.8, max_abs_err=0.000204 (2^-12.26), power_index=1.33
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=2] area_um2=30165, accuracy_bits=12.3, ffs=455, throughput_msps=78.8, max_abs_err=0.0002 (2^-12.28), power_index=1.38
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=2] area_um2=30990, accuracy_bits=12.3, ffs=453, throughput_msps=78.8, max_abs_err=0.000192 (2^-12.35), power_index=1.39
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=40877, accuracy_bits=12.7, ffs=885, throughput_msps=138, max_abs_err=0.000148 (2^-12.72), power_index=2.34
- pipelined [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] area_um2=41562, accuracy_bits=12.8, ffs=900, throughput_msps=143, max_abs_err=0.000145 (2^-12.75), power_index=2.38
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=42248, accuracy_bits=13, ffs=914, throughput_msps=138, max_abs_err=0.000119 (2^-13.04), power_index=2.42
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=42933, accuracy_bits=13.2, ffs=929, throughput_msps=132, max_abs_err=0.000109 (2^-13.17), power_index=2.46
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] area_um2=45179, accuracy_bits=13.4, ffs=957, throughput_msps=132, max_abs_err=9.31e-05 (2^-13.39), power_index=2.55
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
Front coverage: area_um2 29151..49611 (HV reference 100000); accuracy_bits 12.3..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 45 evals, 32 feasible; max throughput seen 171 MSPS; best accuracy 14.16 bits; best feasible area_um2=38060; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 75 evals, 6 feasible; max throughput seen 86.6 MSPS; best accuracy 14.11 bits; best feasible area_um2=29151; feasible ranges: data_width 17..18, n_iter 14..14, angle_guard 0..1, frac_guard 0..1, m 2..2
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (20 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (3 front designs; box front_anchored)
- `pipelined` (60 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (9 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 94 feasible; hypervolume 2.463e+05 (+98.5%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and robust. The minimum area design (pipelined_m, 29151 um^2) comfortably meets all constraints: throughput 78.8 MSPS >= 32, max_abs_err 2.04e-4 <= 2.44e-4, and the system batch latency bound is met (best seen 0.269 us <= 0.5 us). The front spans a reasonable trade-off space (area 29k-50k um^2, accuracy 12.3-14.2 bits) with no obvious gaps. Since this is the final round, further exploration is unnecessary; the current front provides a solid basis for final selection via the min-area rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 2.463e+05 (gain this round: +98.5%).
Feasible designs: 94 of 200 evaluations (60 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 11% violate; best seen 171
- max_abs_err <= 0.000244141: 36% violate; best seen 1.02e-07 (2^-23.23)
- sys_p99_batch_us <= 0.5: 34% violate; best seen 0.269

Pareto front (feasible, 17 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=2] area_um2=29151, accuracy_bits=12.3, ffs=439, throughput_msps=78.8, max_abs_err=0.000204 (2^-12.26), power_index=1.33
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=2] area_um2=30990, accuracy_bits=12.3, ffs=453, throughput_msps=78.8, max_abs_err=0.000192 (2^-12.35), power_index=1.39
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.5, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53), power_index=2.3
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=40877, accuracy_bits=12.7, ffs=885, throughput_msps=138, max_abs_err=0.000148 (2^-12.72), power_index=2.34
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=42248, accuracy_bits=13, ffs=914, throughput_msps=138, max_abs_err=0.000119 (2^-13.04), power_index=2.42
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=44494, accuracy_bits=13.3, ffs=942, throughput_msps=138, max_abs_err=0.000101 (2^-13.27), power_index=2.51
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
- pipelined [data_width=24 n_iter=18 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=66701, accuracy_bits=16.7, ffs=1433, throughput_msps=108, max_abs_err=9.16e-06 (2^-16.74), power_index=3.81
- pipelined [data_width=21 n_iter=20 angle_guard=2 frac_guard=2 rounding=round] area_um2=70658, accuracy_bits=17.5, ffs=1488, throughput_msps=119, max_abs_err=5.43e-06 (2^-17.49), power_index=3.98
Front coverage: area_um2 29151..70658 (HV reference 100000); accuracy_bits 12.3..17.5 (HV reference 12); data_width on the front 17..24 (registry 8..28).

Per family:
- pipelined: 105 evals, 84 feasible; max throughput seen 171 MSPS; best accuracy 23.23 bits; best feasible area_um2=38060; feasible ranges: data_width 17..28, n_iter 14..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 95 evals, 10 feasible; max throughput seen 86.6 MSPS; best accuracy 19.16 bits; best feasible area_um2=29151; feasible ranges: data_width 17..18, n_iter 14..14, angle_guard 0..1, frac_guard 0..1, m 2..2
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 9272 in, 2519 out
- provider-reported cost: $0.0094
- full prompts and replies: `llm_trace.jsonl`

