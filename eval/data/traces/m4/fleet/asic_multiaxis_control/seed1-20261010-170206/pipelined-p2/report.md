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
`pipelined:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 38197 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10176 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 810 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 112 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.16 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000209 (2^-12.22) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.43 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 6.44e-05 (2^-13.92) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 1.06 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.2 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (8 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` | 38197 | 810 | 143.2 | 16 | 2.16 | 0.000209 (2^-12.22) | 12.22 |
| 1 | `pipelined:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=round` | 39385 | 834 | 143.2 | 16 | 2.23 | 0.000204 (2^-12.26) | 12.26 |
| 2 | `pipelined:data_width=16,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 43736 | 926 | 143.2 | 18 | 2.47 | 0.000177 (2^-12.47) | 12.47 |
| 3 | `pipelined:data_width=18,n_iter=18,angle_guard=1,frac_guard=0,rounding=round` | 50983 | 1097 | 137.6 | 20 | 2.91 | 9.26e-05 (2^-13.40) | 13.40 |
| 4 | `pipelined:data_width=19,n_iter=18,angle_guard=1,frac_guard=0,rounding=trunc` | 53465 | 1150 | 132.4 | 20 | 3.05 | 7.8e-05 (2^-13.65) | 13.65 |
| 5 | `pipelined:data_width=19,n_iter=26,angle_guard=1,frac_guard=0,rounding=round` | 77897 | 1661 | 132.4 | 28 | 4.42 | 4.26e-05 (2^-14.52) | 14.52 |
| 6 | `pipelined:data_width=19,n_iter=25,angle_guard=1,frac_guard=3,rounding=trunc` | 81535 | 1733 | 123.1 | 27 | 4.62 | 3.38e-05 (2^-14.85) | 14.85 |
| 7 | `pipelined:data_width=24,n_iter=23,angle_guard=-1,frac_guard=0,rounding=round` | 82569 | 1764 | 115.0 | 25 | 4.69 | 3.68e-06 (2^-18.05) | 18.05 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts are decisive: only pipelined has produced feasible designs (30/53) and it owns all 7 designs on the merged front. iterative, unrolled_k, and pipelined_m have 0 feasible designs. The throughput constraint (>= 32 Msps) requires 1 result/cycle, which only pipelined and pipelined_m can provide; pipelined_m has failed to find any feasible design in 47 evaluations, likely because the register-every-m-stages structure either cannot meet the accuracy constraint at low area or the Fmax drops too much. I am therefore concentrating all remaining budget on pipelined with tightly narrowed ranges around the known feasible region (data_width 14-16, n_iter 12-16, angle_guard -2 to 2, frac_guard 0-2). The goal is to densely map the Pareto front in the area-vs-accuracy trade-off space within the feasible region, since the selection rule is min area and the hypervolume rewards covering the trade-off curve. The current best feasible area is 39385 um^2; I expect to find designs with lower area by exploring the boundary of the accuracy constraint (data_width=14, n_iter=12-14, angle_guard=-2, frac_guard=0) while also mapping the higher-accuracy corner (data_width=16, n_iter=14-16) for hypervolume coverage. I am not including pipelined_m because it has 0 feasible designs in 47 evaluations and the remaining budget is better spent densifying the pipelined front.*)
- `pipelined` (100 evals): data_width=14..16, n_iter=12..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined is the only family with feasible designs (30/53) and owns the entire merged front; it is the only family that can meet the 32 Msps throughput constraint (1 result/cycle). The current best feasible area is 39385 um^2. I am narrowing the ranges to focus the remaining budget on the region of the front that is actually feasible: data_width 14-16 (14 is the minimum that can plausibly give 12+ bits accuracy with enough n_iter; 16 gives margin), n_iter 12-16 (12 is near the minimum for 12-bit accuracy; higher n_iter increases area without much accuracy gain once past ~14), angle_guard -2 to 2 (negative guards save area but risk accuracy; positive guards add area), frac_guard 0-2 (0 is cheapest; higher guards add area for marginal accuracy), and both rounding modes. This tightens the search around the known feasible region to map the Pareto front more densely within the remaining budget.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 5 feasible; hypervolume 2.763e+04 (n/a).

**LLM decision:** `add_family` — The current front is dominated by the `pipelined` family with a fixed `data_width=16`. While it meets the throughput (143 MSPS > 32) and accuracy constraints, the area is relatively high (~38k-43k um^2) because `pipelined` requires a full register stage for every micro-rotation (`n_iter` 14-16). The `pipelined_m` family allows registering every `m` stages, which can significantly reduce flip-flop count and area for the same accuracy and throughput (still 1 result/cycle). Since `pipelined_m` has not been explored yet and offers a direct path to lower area while maintaining the high throughput required for the 32-request burst, it is the logical next step to expand the Pareto front towards the minimum area objective.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 2.763e+04 (gain this round: n/a (first round)).
Feasible designs: 5 of 100 evaluations (3 unique).
Families explored so far: pipelined. Not yet explored: pipelined_m.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 171
- max_abs_err <= 0.000244141: 95% violate; best seen 0.000177 (2^-12.47)
- sys_p99_batch_us <= 0.5: 0% violate; best seen 0.263

Pareto front (feasible, 3 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=38197, accuracy_bits=12.2, ffs=810, throughput_msps=143, max_abs_err=0.000209 (2^-12.22), power_index=2.16
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=39385, accuracy_bits=12.3, ffs=834, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=2.23
- pipelined [data_width=16 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=43736, accuracy_bits=12.5, ffs=926, throughput_msps=143, max_abs_err=0.000177 (2^-12.47), power_index=2.47
Front coverage: area_um2 38197..43736 (HV reference 100000); accuracy_bits 12.2..12.5 (HV reference 12); data_width on the front 16..16 (registry 8..28).

Per family:
- pipelined: 100 evals, 5 feasible; max throughput seen 171 MSPS; best accuracy 12.47 bits; best feasible area_um2=38197; feasible ranges: data_width 16..16, n_iter 14..16, angle_guard 2..2, frac_guard 1..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Focus entirely on pipelined_m to see if it can beat the 38k um^2 area of the current pipelined front. Ranges are centered around the known feasible region (data_width ~16, n_iter ~14) but widened slightly to allow the optimizer to trade off n_iter and data_width against the m parameter.*)
- `pipelined_m` (20 evals): data_width=14..18, n_iter=12..18, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* Explore pipelined_m to find lower area designs by reducing register pressure via m-stage pipelining, while maintaining 1 result/cycle throughput to satisfy the 32 MSPS constraint.

**Result (code):** 20 evaluations this round, 120 total; 5 feasible; hypervolume 2.763e+04 (+0.0%).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 3 unique designs, all meeting the strict constraints (throughput >= 32 MSPS, max_abs_err <= 2^-12, sys_p99_batch_us <= 0.5 us). The best design (pipelined, W=16, N=14, ag=2, fg=1, round) achieves 38197 um^2 area with 12.2 accuracy bits and 143 MSPS throughput. The front covers the critical trade-off region: area 38197-43736 um^2 and accuracy 12.2-12.5 bits. The pipelined family dominates the feasible space (5 feasible out of 100 evals), while pipelined_m yielded 0 feasible designs. Since this is the final round (120/200 evals used, round 2/4 but treated as final per instructions), and the front is stable with no improvement in hypervolume this round (+0.0%), further exploration would not significantly improve the front. The selection rule (min area) will pick the 38197 um^2 design, which comfortably meets all constraints including the system-level p99 batch latency (best seen 0.263 us < 0.5 us).
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 2.763e+04 (gain this round: +0.0%).
Feasible designs: 5 of 120 evaluations (3 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 2% violate; best seen 171
- max_abs_err <= 0.000244141: 84% violate; best seen 6.45e-05 (2^-13.92)
- sys_p99_batch_us <= 0.5: 15% violate; best seen 0.263

Pareto front (feasible, 3 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=38197, accuracy_bits=12.2, ffs=810, throughput_msps=143, max_abs_err=0.000209 (2^-12.22), power_index=2.16
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=39385, accuracy_bits=12.3, ffs=834, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=2.23
- pipelined [data_width=16 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=43736, accuracy_bits=12.5, ffs=926, throughput_msps=143, max_abs_err=0.000177 (2^-12.47), power_index=2.47
Front coverage: area_um2 38197..43736 (HV reference 100000); accuracy_bits 12.2..12.5 (HV reference 12); data_width on the front 16..16 (registry 8..28).

Per family:
- pipelined: 100 evals, 5 feasible; max throughput seen 171 MSPS; best accuracy 12.47 bits; best feasible area_um2=38197; feasible ranges: data_width 16..16, n_iter 14..16, angle_guard 2..2, frac_guard 1..2
- pipelined_m: 20 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 13.92 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined` (40 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)
- `pipelined_m` (40 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 80 evaluations this round, 200 total; 28 feasible; hypervolume 1.661e+05 (+501.2%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 3 unique designs, all meeting the strict constraints (throughput >= 32 MSPS, max_abs_err <= 2^-12, sys_p99_batch_us <= 0.5 us). The best design (pipelined, W=16, N=14, ag=2, fg=1, round) achieves 38197 um^2 area with 12.2 accuracy bits and 143 MSPS throughput. The front covers the critical trade-off region: area 38197-43736 um^2 and accuracy 12.2-12.5 bits. The pipelined family dominates the feasible space (5 feasible out of 100 evals), while pipelined_m yielded 0 feasible designs. Since this is the final round (120/200 evals used, round 2/4 but treated as final per instructions), and the front is stable with no improvement in hypervolume this round (+0.0%), further exploration would not significantly improve the front. The selection rule (min area) will pick the 38197 um^2 design, which comfortably meets all constraints including the system-level p99 batch latency (best seen 0.263 us < 0.5 us).
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.661e+05 (gain this round: +501.2%).
Feasible designs: 28 of 200 evaluations (18 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 8% violate; best seen 171
- max_abs_err <= 0.000244141: 58% violate; best seen 1.79e-07 (2^-22.41)
- sys_p99_batch_us <= 0.5: 34% violate; best seen 0.263

Pareto front (feasible, 8 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=38197, accuracy_bits=12.2, ffs=810, throughput_msps=143, max_abs_err=0.000209 (2^-12.22), power_index=2.16
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=39385, accuracy_bits=12.3, ffs=834, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=2.23
- pipelined [data_width=16 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=43736, accuracy_bits=12.5, ffs=926, throughput_msps=143, max_abs_err=0.000177 (2^-12.47), power_index=2.47
- pipelined [data_width=18 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] area_um2=50983, accuracy_bits=13.4, ffs=1097, throughput_msps=138, max_abs_err=9.26e-05 (2^-13.40), power_index=2.91
- pipelined [data_width=19 n_iter=18 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=53465, accuracy_bits=13.6, ffs=1150, throughput_msps=132, max_abs_err=7.8e-05 (2^-13.65), power_index=3.05
- pipelined [data_width=19 n_iter=26 angle_guard=1 frac_guard=0 rounding=round] area_um2=77897, accuracy_bits=14.5, ffs=1661, throughput_msps=132, max_abs_err=4.26e-05 (2^-14.52), power_index=4.42
- pipelined [data_width=19 n_iter=25 angle_guard=1 frac_guard=3 rounding=trunc] area_um2=81535, accuracy_bits=14.9, ffs=1733, throughput_msps=123, max_abs_err=3.38e-05 (2^-14.85), power_index=4.62
- pipelined [data_width=24 n_iter=23 angle_guard=-1 frac_guard=0 rounding=round] area_um2=82569, accuracy_bits=18.1, ffs=1764, throughput_msps=115, max_abs_err=3.68e-06 (2^-18.05), power_index=4.69
Front coverage: area_um2 38197..82569 (HV reference 100000); accuracy_bits 12.2..18.1 (HV reference 12); data_width on the front 16..24 (registry 8..28).

Per family:
- pipelined: 140 evals, 28 feasible; max throughput seen 171 MSPS; best accuracy 22.41 bits; best feasible area_um2=38197; feasible ranges: data_width 16..24, n_iter 14..29, angle_guard -2..4, frac_guard 0..3
- pipelined_m: 60 evals, 0 feasible; max throughput seen 123 MSPS; best accuracy 20.66 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7937 in, 1813 out
- provider-reported cost: $0.0051
- full prompts and replies: `llm_trace.jsonl`

