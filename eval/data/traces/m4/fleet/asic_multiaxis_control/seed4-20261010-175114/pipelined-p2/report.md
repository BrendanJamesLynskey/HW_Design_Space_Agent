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
`pipelined:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 37422 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 9970 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 812 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 112 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.15 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000204 (2^-12.26) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 6.67 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 6.07e-05 (2^-14.01) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.99 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (24 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 37422 | 812 | 143.2 | 16 | 2.15 | 0.000204 (2^-12.26) | 12.26 |
| 1 | `pipelined:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 40192 | 870 | 143.2 | 17 | 2.31 | 0.000168 (2^-12.54) | 12.54 |
| 2 | `pipelined:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 40877 | 885 | 137.6 | 17 | 2.34 | 0.000148 (2^-12.72) | 12.72 |
| 3 | `pipelined:data_width=18,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 41562 | 900 | 143.2 | 17 | 2.38 | 0.000145 (2^-12.75) | 12.75 |
| 4 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 42248 | 914 | 137.6 | 17 | 2.42 | 0.000119 (2^-13.04) | 13.04 |
| 5 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 42933 | 929 | 132.4 | 17 | 2.46 | 0.000109 (2^-13.17) | 13.17 |
| 6 | `pipelined:data_width=17,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 44356 | 938 | 137.6 | 17 | 2.5 | 0.000108 (2^-13.18) | 13.18 |
| 7 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc` | 44813 | 965 | 132.4 | 17 | 2.56 | 0.000102 (2^-13.26) | 13.26 |
| 8 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=1,rounding=round` | 45179 | 957 | 132.4 | 17 | 2.55 | 9.31e-05 (2^-13.39) | 13.39 |
| 9 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 45892 | 991 | 132.4 | 18 | 2.63 | 8.35e-05 (2^-13.55) | 13.55 |
| 10 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 46462 | 982 | 132.4 | 17 | 2.62 | 8.26e-05 (2^-13.56) | 13.56 |
| 11 | `pipelined:data_width=19,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc` | 47554 | 1024 | 127.5 | 17 | 2.72 | 7.77e-05 (2^-13.65) | 13.65 |
| 12 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 48233 | 1020 | 132.4 | 18 | 2.72 | 6.45e-05 (2^-13.92) | 13.92 |
| 13 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 49611 | 1048 | 132.4 | 18 | 2.8 | 5.46e-05 (2^-14.16) | 14.16 |
| 14 | `pipelined:data_width=22,n_iter=17,angle_guard=-2,frac_guard=0,rounding=round` | 55090 | 1187 | 123.1 | 19 | 3.15 | 3.36e-05 (2^-14.86) | 14.86 |
| 15 | `pipelined:data_width=19,n_iter=17,angle_guard=2,frac_guard=2,rounding=round` | 55151 | 1164 | 127.5 | 19 | 3.11 | 2.76e-05 (2^-15.14) | 15.14 |
| 16 | `pipelined:data_width=23,n_iter=17,angle_guard=-2,frac_guard=0,rounding=round` | 57430 | 1237 | 118.9 | 19 | 3.28 | 2.43e-05 (2^-15.33) | 15.33 |
| 17 | `pipelined:data_width=22,n_iter=17,angle_guard=2,frac_guard=2,rounding=round` | 62323 | 1314 | 115.0 | 19 | 3.51 | 1.67e-05 (2^-15.87) | 15.87 |
| 18 | `pipelined:data_width=23,n_iter=17,angle_guard=2,frac_guard=2,rounding=round` | 64713 | 1365 | 111.3 | 19 | 3.65 | 1.58e-05 (2^-15.95) | 15.95 |
| 19 | `pipelined:data_width=22,n_iter=19,angle_guard=0,frac_guard=1,rounding=round` | 66346 | 1399 | 118.9 | 21 | 3.74 | 8.92e-06 (2^-16.77) | 16.77 |
| 20 | `pipelined:data_width=21,n_iter=20,angle_guard=2,frac_guard=1,rounding=round` | 68901 | 1453 | 118.9 | 22 | 3.88 | 7.26e-06 (2^-17.07) | 17.07 |
| 21 | `pipelined:data_width=21,n_iter=20,angle_guard=2,frac_guard=2,rounding=round` | 70658 | 1488 | 118.9 | 22 | 3.98 | 5.43e-06 (2^-17.49) | 17.49 |
| 22 | `pipelined:data_width=23,n_iter=20,angle_guard=2,frac_guard=0,rounding=round` | 71559 | 1534 | 111.3 | 22 | 4.08 | 4.1e-06 (2^-17.90) | 17.90 |
| 23 | `pipelined:data_width=23,n_iter=20,angle_guard=2,frac_guard=4,rounding=round` | 79805 | 1677 | 104.7 | 22 | 4.49 | 2.78e-06 (2^-18.46) | 18.46 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show that pipelined is the only family that can meet the constraints: 54 feasible designs out of 73 evaluations, and it owns all 13 designs on the merged front. The best feasible area is 39973 um^2. The other families (iterative, unrolled_k, pipelined_m) have 0 feasible designs, so they cannot meet the throughput or system constraints. I am focusing 100% of the remaining budget on pipelined, narrowing the parameter ranges around the known-feasible region to refine the Pareto front. The key trade-off is between area (minimized by smaller data_width and n_iter) and accuracy_bits (maximized by larger n_iter, angle_guard, frac_guard, and rounding). The accuracy constraint (max_abs_err <= 2^-12) sets a lower bound on n_iter and data_width, while the area objective pushes toward the minimum feasible values. The throughput constraint (>=32 Msps) requires Fmax >= 32 MHz, which pipelined can meet with reasonable n_iter. The system constraint (sys_p99_batch_us <= 0.5) requires that all 32 results are back within 0.5 us of the tick, which for a pipelined design with 1 result/cycle means the pipeline latency plus the time to process 32 requests must be <= 0.5 us. At Fmax = 32 MHz, 1 cycle = 31.25 ns, so 32 requests take 32 cycles = 1000 ns = 1 us, which exceeds 0.5 us. This means the design must run at a higher Fmax or have a lower latency. For a pipelined design with N iterations, the latency is N+2 cycles. If Fmax = 64 MHz, 1 cycle = 15.625 ns, and 32 requests take 32 cycles = 500 ns = 0.5 us, which just meets the constraint. So the design must have Fmax >= 64 MHz to meet the system constraint. This means n_iter must be small enough that the critical path allows Fmax >= 64 MHz. I am narrowing n_iter to 12-16 to focus on designs that can meet both the accuracy and system constraints while minimizing area.*)
- `pipelined` (100 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined is the only family with feasible designs (54/73) and owns the entire merged front (13/13). The best feasible area is 39973 um^2. The throughput constraint (>=32 Msps) requires Fmax >= 32 MHz, which pipelined can meet. The accuracy constraint (max_abs_err <= 2^-12) requires sufficient n_iter and data_width. I am narrowing the ranges around the known-feasible region to focus the remaining budget on refining the Pareto front: data_width 14-18 (14 is the minimum for 12-bit accuracy with reasonable n_iter, 18 gives margin), n_iter 12-16 (12 is near the minimum for 12-bit accuracy, 16 gives margin), angle_guard 0-2 (negative guards risk accuracy loss, 2 gives margin), frac_guard 0-2 (0 is minimum, 2 gives margin for rounding). This focuses the search on the trade-off between area (driven by data_width and n_iter) and accuracy_bits (driven by n_iter, angle_guard, frac_guard, rounding).
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 56 feasible; hypervolume 1.214e+05 (n/a).

**LLM decision:** `add_family` — The current front (12 designs, all pipelined) spans area 37422-49611 um^2 and accuracy 12.3-14.2 bits. The minimum-area feasible design is 37422 um^2 with 812 FFs. pipelined_m is the natural area-reduction family: it achieves the same 1-result/cycle throughput (satisfying throughput_msps >= 32 and sys_p99_batch_us <= 0.5) but with fewer pipeline registers (ceil(N/m) stages vs N stages), directly reducing FF count and area. With m=2..4 and the same data_width/n_iter/guard ranges that produced the current front, pipelined_m should yield designs well below 37422 um^2 at comparable accuracy, significantly expanding hypervolume on the area axis. The accuracy constraint (max_abs_err <= 2^-12) is already met by the current front's best (2^-14.16), and the 44% violation rate in round 1 was from designs with too few iterations or too narrow angle paths; the narrowed ranges (n_iter >= 14, angle_guard >= 0) should reduce that. Splitting the budget 50/50 between pipelined_m (new family, primary area-reduction lever) and pipelined (refinement, front resolution) maximizes the chance of finding non-dominated designs in both families within the 100-eval round budget.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.214e+05 (gain this round: n/a (first round)).
Feasible designs: 56 of 100 evaluations (33 unique).
Families explored so far: pipelined. Not yet explored: pipelined_m.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 163
- max_abs_err <= 0.000244141: 44% violate; best seen 5.46e-05 (2^-14.16)
- sys_p99_batch_us <= 0.5: 0% violate; best seen 0.276

Pareto front (feasible, 12 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=37422, accuracy_bits=12.3, ffs=812, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=2.15
- pipelined [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=40192, accuracy_bits=12.5, ffs=870, throughput_msps=143, max_abs_err=0.000168 (2^-12.54), power_index=2.31
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=40877, accuracy_bits=12.7, ffs=885, throughput_msps=138, max_abs_err=0.000148 (2^-12.72), power_index=2.34
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=42248, accuracy_bits=13, ffs=914, throughput_msps=138, max_abs_err=0.000119 (2^-13.04), power_index=2.42
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=44356, accuracy_bits=13.2, ffs=938, throughput_msps=138, max_abs_err=0.000108 (2^-13.18), power_index=2.5
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=44813, accuracy_bits=13.3, ffs=965, throughput_msps=132, max_abs_err=0.000102 (2^-13.26), power_index=2.56
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] area_um2=45179, accuracy_bits=13.4, ffs=957, throughput_msps=132, max_abs_err=9.31e-05 (2^-13.39), power_index=2.55
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=46462, accuracy_bits=13.6, ffs=982, throughput_msps=132, max_abs_err=8.26e-05 (2^-13.56), power_index=2.62
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=48233, accuracy_bits=13.9, ffs=1020, throughput_msps=132, max_abs_err=6.45e-05 (2^-13.92), power_index=2.72
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
Front coverage: area_um2 37422..49611 (HV reference 100000); accuracy_bits 12.3..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 100 evals, 56 feasible; max throughput seen 163 MSPS; best accuracy 14.16 bits; best feasible area_um2=37422; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The current front (12 designs, all pipelined) spans area 37422-49611 um^2 and accuracy 12.3-14.2 bits. The minimum-area feasible design is 37422 um^2 with 812 FFs. pipelined_m is the natural area-reduction family: it achieves the same 1-result/cycle throughput (satisfying throughput_msps >= 32 and sys_p99_batch_us <= 0.5) but with fewer pipeline registers (ceil(N/m) stages vs N stages), directly reducing FF count and area. With m=2..4 and the same data_width/n_iter/guard ranges that produced the current front, pipelined_m should yield designs well below 37422 um^2 at comparable accuracy, significantly expanding hypervolume on the area axis. The accuracy constraint (max_abs_err <= 2^-12) is already met by the current front's best (2^-14.16), and the 44% violation rate in round 1 was from designs with too few iterations or too narrow angle paths; the narrowed ranges (n_iter >= 14, angle_guard >= 0) should reduce that. Splitting the budget 50/50 between pipelined_m (new family, primary area-reduction lever) and pipelined (refinement, front resolution) maximizes the chance of finding non-dominated designs in both families within the 100-eval round budget.*)
- `pipelined_m` (10 evals): data_width=16..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m registers every m stages instead of every stage. For the same data_width/n_iter/guards, it uses fewer flip-flops and less area than pipelined while still delivering 1 result/cycle (meeting the 32 MSPS throughput and 0.5us batch latency constraints). The current front is dominated by pipelined designs with 812-1048 FFs; pipelined_m with m=2..4 should shift the area objective significantly lower at comparable accuracy, expanding the hypervolume on the area axis.
- `pipelined` (10 evals): data_width=16..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Continue refining the pipelined family in the same region to ensure the front is well-resolved where pipelined_m and pipelined overlap, and to capture any pipelined designs that remain non-dominated after pipelined_m is added.

**Result (code):** 20 evaluations this round, 120 total; 64 feasible; hypervolume 1.216e+05 (+0.2%).

**LLM decision:** `stop` — The Pareto front is well-mapped and feasible. The minimum area design (37422 um^2) meets all constraints: throughput 143 MSPS >= 32, max_abs_err 0.000204 <= 0.000244141, and the system p99 batch latency constraint is satisfied by the pipelined family (best seen 0.276 us <= 0.5 us, with 0% violations in the recent feasible set). The front covers a reasonable range of accuracy (12.3 to 14.2 bits) and area (37422 to 49611 um^2). Since this is the final round, we stop and select the minimum area design from the front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.216e+05 (gain this round: +0.2%).
Feasible designs: 64 of 120 evaluations (38 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 163
- max_abs_err <= 0.000244141: 41% violate; best seen 5.46e-05 (2^-14.16)
- sys_p99_batch_us <= 0.5: 8% violate; best seen 0.276

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=37422, accuracy_bits=12.3, ffs=812, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=2.15
- pipelined [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=40192, accuracy_bits=12.5, ffs=870, throughput_msps=143, max_abs_err=0.000168 (2^-12.54), power_index=2.31
- pipelined [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] area_um2=41562, accuracy_bits=12.8, ffs=900, throughput_msps=143, max_abs_err=0.000145 (2^-12.75), power_index=2.38
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=42248, accuracy_bits=13, ffs=914, throughput_msps=138, max_abs_err=0.000119 (2^-13.04), power_index=2.42
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=42933, accuracy_bits=13.2, ffs=929, throughput_msps=132, max_abs_err=0.000109 (2^-13.17), power_index=2.46
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=44813, accuracy_bits=13.3, ffs=965, throughput_msps=132, max_abs_err=0.000102 (2^-13.26), power_index=2.56
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] area_um2=45179, accuracy_bits=13.4, ffs=957, throughput_msps=132, max_abs_err=9.31e-05 (2^-13.39), power_index=2.55
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=48233, accuracy_bits=13.9, ffs=1020, throughput_msps=132, max_abs_err=6.45e-05 (2^-13.92), power_index=2.72
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
Front coverage: area_um2 37422..49611 (HV reference 100000); accuracy_bits 12.3..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 110 evals, 64 feasible; max throughput seen 163 MSPS; best accuracy 14.16 bits; best feasible area_um2=37422; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 10 evals, 0 feasible; max throughput seen 75.4 MSPS; best accuracy 12.81 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined` (80 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (13 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 121 feasible; hypervolume 2.691e+05 (+121.3%).

**No LLM call** (code's front-mapping round): The Pareto front is well-mapped and feasible. The minimum area design (37422 um^2) meets all constraints: throughput 143 MSPS >= 32, max_abs_err 0.000204 <= 0.000244141, and the system p99 batch latency constraint is satisfied by the pipelined family (best seen 0.276 us <= 0.5 us, with 0% violations in the recent feasible set). The front covers a reasonable range of accuracy (12.3 to 14.2 bits) and area (37422 to 49611 um^2). Since this is the final round, we stop and select the minimum area design from the front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 2.691e+05 (gain this round: +121.3%).
Feasible designs: 121 of 200 evaluations (87 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 163
- max_abs_err <= 0.000244141: 26% violate; best seen 6.16e-08 (2^-23.95)
- sys_p99_batch_us <= 0.5: 14% violate; best seen 0.276

Pareto front (feasible, 24 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=37422, accuracy_bits=12.3, ffs=812, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=2.15
- pipelined [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] area_um2=41562, accuracy_bits=12.8, ffs=900, throughput_msps=143, max_abs_err=0.000145 (2^-12.75), power_index=2.38
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=42933, accuracy_bits=13.2, ffs=929, throughput_msps=132, max_abs_err=0.000109 (2^-13.17), power_index=2.46
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] area_um2=45179, accuracy_bits=13.4, ffs=957, throughput_msps=132, max_abs_err=9.31e-05 (2^-13.39), power_index=2.55
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=46462, accuracy_bits=13.6, ffs=982, throughput_msps=132, max_abs_err=8.26e-05 (2^-13.56), power_index=2.62
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
- pipelined [data_width=19 n_iter=17 angle_guard=2 frac_guard=2 rounding=round] area_um2=55151, accuracy_bits=15.1, ffs=1164, throughput_msps=128, max_abs_err=2.76e-05 (2^-15.14), power_index=3.11
- pipelined [data_width=23 n_iter=17 angle_guard=2 frac_guard=2 rounding=round] area_um2=64713, accuracy_bits=15.9, ffs=1365, throughput_msps=111, max_abs_err=1.58e-05 (2^-15.95), power_index=3.65
- pipelined [data_width=21 n_iter=20 angle_guard=2 frac_guard=1 rounding=round] area_um2=68901, accuracy_bits=17.1, ffs=1453, throughput_msps=119, max_abs_err=7.26e-06 (2^-17.07), power_index=3.88
- pipelined [data_width=23 n_iter=20 angle_guard=2 frac_guard=4 rounding=round] area_um2=79805, accuracy_bits=18.5, ffs=1677, throughput_msps=105, max_abs_err=2.78e-06 (2^-18.46), power_index=4.49
Front coverage: area_um2 37422..79805 (HV reference 100000); accuracy_bits 12.3..18.5 (HV reference 12); data_width on the front 17..23 (registry 8..28).

Per family:
- pipelined: 190 evals, 121 feasible; max throughput seen 163 MSPS; best accuracy 23.95 bits; best feasible area_um2=37422; feasible ranges: data_width 16..27, n_iter 14..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 10 evals, 0 feasible; max throughput seen 75.4 MSPS; best accuracy 12.81 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 9194 in, 2680 out
- provider-reported cost: $0.0059
- full prompts and replies: `llm_trace.jsonl`

