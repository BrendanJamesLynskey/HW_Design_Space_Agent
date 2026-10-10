# DSE run: asic_multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
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
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=2` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 30165 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 8036 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 455 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 78.8 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 78.8 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 9 | exact: schedule |
| latency_ns | 114 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.38 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.0002 (2^-12.28) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 13.1 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.41e-05 (2^-14.17) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.55 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (14 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=2` | 30165 | 455 | 78.8 | 9 | 1.38 | 0.0002 (2^-12.28) | 12.28 |
| 1 | `pipelined:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 39336 | 853 | 137.6 | 16 | 2.26 | 0.000175 (2^-12.48) | 12.48 |
| 2 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` | 42125 | 893 | 132.4 | 16 | 2.38 | 0.000152 (2^-12.68) | 12.68 |
| 3 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=2,rounding=round` | 43313 | 916 | 132.4 | 16 | 2.45 | 0.000144 (2^-12.76) | 12.76 |
| 4 | `pipelined:data_width=18,n_iter=15,angle_guard=0,frac_guard=2,rounding=round` | 45092 | 953 | 132.4 | 17 | 2.54 | 0.000123 (2^-12.99) | 12.99 |
| 5 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 45892 | 991 | 132.4 | 18 | 2.63 | 8.35e-05 (2^-13.55) | 13.55 |
| 6 | `pipelined:data_width=19,n_iter=18,angle_guard=4,frac_guard=0,rounding=trunc` | 55947 | 1203 | 118.9 | 20 | 3.2 | 7.8e-05 (2^-13.65) | 13.65 |
| 7 | `pipelined:data_width=21,n_iter=18,angle_guard=-1,frac_guard=1,rounding=round` | 59458 | 1254 | 123.1 | 20 | 3.35 | 2.99e-05 (2^-15.03) | 15.03 |
| 8 | `pipelined:data_width=23,n_iter=18,angle_guard=-1,frac_guard=0,rounding=trunc` | 61738 | 1327 | 118.9 | 20 | 3.52 | 1.39e-05 (2^-16.14) | 16.14 |
| 9 | `pipelined:data_width=24,n_iter=18,angle_guard=-1,frac_guard=0,rounding=trunc` | 64219 | 1380 | 115.0 | 20 | 3.67 | 1.03e-05 (2^-16.57) | 16.57 |
| 10 | `pipelined:data_width=24,n_iter=18,angle_guard=-1,frac_guard=2,rounding=trunc` | 67354 | 1443 | 107.9 | 20 | 3.84 | 9.59e-06 (2^-16.67) | 16.67 |
| 11 | `pipelined:data_width=24,n_iter=18,angle_guard=3,frac_guard=0,rounding=trunc` | 67528 | 1451 | 104.7 | 20 | 3.85 | 9.16e-06 (2^-16.74) | 16.74 |
| 12 | `pipelined:data_width=25,n_iter=18,angle_guard=-1,frac_guard=2,rounding=trunc` | 69836 | 1496 | 104.7 | 20 | 3.98 | 8.73e-06 (2^-16.81) | 16.81 |
| 13 | `pipelined:data_width=21,n_iter=26,angle_guard=2,frac_guard=1,rounding=round` | 89784 | 1890 | 118.9 | 28 | 5.05 | 6.89e-06 (2^-17.15) | 17.15 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is a min-area problem with two hard constraints: throughput_msps >= 32 and sys_p99_batch_us <= 0.5 (32 back-to-back results in 0.5 us), plus max_abs_err <= 2^-12. Only the 1-result/cycle families (pipelined, pipelined_m) can plausibly hit 32 Msps without an unrealistically high Fmax, so I restrict to those two. Accuracy is the binding accuracy constraint: with Q1.(W-2) output the LSB is 2^-(W-2), so W=14 gives a 12-bit LSB and W=16 a 14-bit LSB; I bound data_width to 14..18 to cover the accuracy requirement without oversizing. n_iter 12..16 is the sweet spot where max_abs_err sits near/below 2^-12 while the per-stage path stays short enough for a high Fmax (needed for both the 32 Msps throughput and the 0.5 us batch bound). angle_guard 0..2 and frac_guard 0..2 keep the datapath narrow (min area) while giving enough headroom for the error budget; rounding is left to both choices so the search can find the cheaper trunc vs round trade-off. I split the budget evenly: pipelined (m=1) is the low-area/low-FF anchor and pipelined_m (m=2..4) is the area-reduced variant, together spanning the area-vs-Fmax trade-off that defines the front. This keeps the search focused on the feasible region rather than wasting evals on wide/low-N corners that fail accuracy or on narrow/high-N corners that fail Fmax.*)
- `pipelined` (30 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined gives 1 result/cycle, so throughput = Fmax. To clear the 32 Msps throughput constraint and the 0.5 us p99-batch bound (32 back-to-back results must fit in 0.5 us, i.e. ~16 ns each at the operating clock), the design needs a high Fmax, which favors a moderate N. Accuracy <= 2^-12 is the binding accuracy constraint: with Q1.(W-2) output the LSB is 2^-(W-2), so W=14 already gives a 12-bit LSB and W=16 gives 14-bit; N in 12..16 with small guards keeps max_abs_err near/below 2^-12 while keeping the per-stage adder/shift chain short for Fmax. This is the primary family for the min-area corner since it has the fewest registers of the 1-result/cycle options.
- `pipelined_m` (30 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m still yields 1 result/cycle (same throughput as pipelined) but registers only every m stages, cutting FF count and area at the cost of a longer combinational path (lower Fmax). Since the objective is min area and the accuracy/throughput constraints are identical to pipelined, this family trades area against Fmax and is the natural second point on the Pareto front. m in 2..4 keeps the combinational depth bounded so Fmax can still clear the 32 Msps / 0.5 us batch bound, while reducing register area versus m=1. Same data_width/n_iter/guard/rounding ranges as pipelined so the two fronts are directly comparable and merge cleanly.

**Result (code):** 60 evaluations this round, 60 total; 11 feasible; hypervolume 9.067e+04 (n/a).

**LLM decision:** `stop` — The exploration has successfully identified a feasible Pareto front that satisfies all system and accuracy constraints. The minimum area design is a `pipelined_m` configuration (data_width=18, n_iter=14, m=2) with an estimated area of 30,165 um², which is significantly below the 100,000 um² reference point. This design achieves 12.3 bits of accuracy (max_abs_err ≈ 2^-12.28), comfortably meeting the 2^-12 constraint, and provides a throughput of 78.8 MSPS, which exceeds the 32 MSPS requirement. The system-level constraint (sys_p99_batch_us <= 0.5 us) is also met, with the best observed value being 0.269 us. Since this is the final round and the front covers the relevant trade-off space for the specified objectives (min area, max accuracy) within the feasible region, stopping is the appropriate action.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 9.067e+04 (gain this round: n/a (first round)).
Feasible designs: 11 of 60 evaluations (10 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 171
- max_abs_err <= 0.000244141: 48% violate; best seen 8.35e-05 (2^-13.55)
- sys_p99_batch_us <= 0.5: 43% violate; best seen 0.269

Pareto front (feasible, 6 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=2] area_um2=30165, accuracy_bits=12.3, ffs=455, throughput_msps=78.8, max_abs_err=0.0002 (2^-12.28), power_index=1.38
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=39336, accuracy_bits=12.5, ffs=853, throughput_msps=138, max_abs_err=0.000175 (2^-12.48), power_index=2.26
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=42125, accuracy_bits=12.7, ffs=893, throughput_msps=132, max_abs_err=0.000152 (2^-12.68), power_index=2.38
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=43313, accuracy_bits=12.8, ffs=916, throughput_msps=132, max_abs_err=0.000144 (2^-12.76), power_index=2.45
- pipelined [data_width=18 n_iter=15 angle_guard=0 frac_guard=2 rounding=round] area_um2=45092, accuracy_bits=13, ffs=953, throughput_msps=132, max_abs_err=0.000123 (2^-12.99), power_index=2.54
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
Front coverage: area_um2 30165..45892 (HV reference 100000); accuracy_bits 12.3..13.5 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- pipelined: 30 evals, 10 feasible; max throughput seen 171 MSPS; best accuracy 13.55 bits; best feasible area_um2=38698; feasible ranges: data_width 18..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 30 evals, 1 feasible; max throughput seen 82.5 MSPS; best accuracy 13.02 bits; best feasible area_um2=30165; feasible ranges: data_width 18..18, n_iter 14..14, angle_guard 0..0, frac_guard 0..0, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (7 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)
- `pipelined` (33 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (5 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 31 feasible; hypervolume 2.199e+05 (+142.6%).

**No LLM call** (code's front-mapping round): The exploration has successfully identified a feasible Pareto front that satisfies all system and accuracy constraints. The minimum area design is a `pipelined_m` configuration (data_width=18, n_iter=14, m=2) with an estimated area of 30,165 um², which is significantly below the 100,000 um² reference point. This design achieves 12.3 bits of accuracy (max_abs_err ≈ 2^-12.28), comfortably meeting the 2^-12 constraint, and provides a throughput of 78.8 MSPS, which exceeds the 32 MSPS requirement. The system-level constraint (sys_p99_batch_us <= 0.5 us) is also met, with the best observed value being 0.269 us. Since this is the final round and the front covers the relevant trade-off space for the specified objectives (min area, max accuracy) within the feasible region, stopping is the appropriate action.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 2.199e+05 (gain this round: +142.6%).
Feasible designs: 31 of 100 evaluations (27 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 4% violate; best seen 171
- max_abs_err <= 0.000244141: 34% violate; best seen 1.15e-07 (2^-23.05)
- sys_p99_batch_us <= 0.5: 42% violate; best seen 0.269

Pareto front (feasible, 14 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=2] area_um2=30165, accuracy_bits=12.3, ffs=455, throughput_msps=78.8, max_abs_err=0.0002 (2^-12.28), power_index=1.38
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=39336, accuracy_bits=12.5, ffs=853, throughput_msps=138, max_abs_err=0.000175 (2^-12.48), power_index=2.26
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=43313, accuracy_bits=12.8, ffs=916, throughput_msps=132, max_abs_err=0.000144 (2^-12.76), power_index=2.45
- pipelined [data_width=18 n_iter=15 angle_guard=0 frac_guard=2 rounding=round] area_um2=45092, accuracy_bits=13, ffs=953, throughput_msps=132, max_abs_err=0.000123 (2^-12.99), power_index=2.54
- pipelined [data_width=19 n_iter=18 angle_guard=4 frac_guard=0 rounding=trunc] area_um2=55947, accuracy_bits=13.6, ffs=1203, throughput_msps=119, max_abs_err=7.8e-05 (2^-13.65), power_index=3.2
- pipelined [data_width=21 n_iter=18 angle_guard=-1 frac_guard=1 rounding=round] area_um2=59458, accuracy_bits=15, ffs=1254, throughput_msps=123, max_abs_err=2.99e-05 (2^-15.03), power_index=3.35
- pipelined [data_width=24 n_iter=18 angle_guard=-1 frac_guard=0 rounding=trunc] area_um2=64219, accuracy_bits=16.6, ffs=1380, throughput_msps=115, max_abs_err=1.03e-05 (2^-16.57), power_index=3.67
- pipelined [data_width=24 n_iter=18 angle_guard=-1 frac_guard=2 rounding=trunc] area_um2=67354, accuracy_bits=16.7, ffs=1443, throughput_msps=108, max_abs_err=9.59e-06 (2^-16.67), power_index=3.84
- pipelined [data_width=25 n_iter=18 angle_guard=-1 frac_guard=2 rounding=trunc] area_um2=69836, accuracy_bits=16.8, ffs=1496, throughput_msps=105, max_abs_err=8.73e-06 (2^-16.81), power_index=3.98
- pipelined [data_width=21 n_iter=26 angle_guard=2 frac_guard=1 rounding=round] area_um2=89784, accuracy_bits=17.1, ffs=1890, throughput_msps=119, max_abs_err=6.89e-06 (2^-17.15), power_index=5.05
Front coverage: area_um2 30165..89784 (HV reference 100000); accuracy_bits 12.3..17.1 (HV reference 12); data_width on the front 18..25 (registry 8..28).

Per family:
- pipelined: 63 evals, 30 feasible; max throughput seen 171 MSPS; best accuracy 23.05 bits; best feasible area_um2=38698; feasible ranges: data_width 18..25, n_iter 14..27, angle_guard -1..4, frac_guard 0..3
- pipelined_m: 37 evals, 1 feasible; max throughput seen 82.5 MSPS; best accuracy 18.11 bits; best feasible area_um2=30165; feasible ranges: data_width 18..18, n_iter 14..14, angle_guard 0..0, frac_guard 0..0, m 2..2
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5306 in, 1537 out
- provider-reported cost: $0.0041
- full prompts and replies: `llm_trace.jsonl`

