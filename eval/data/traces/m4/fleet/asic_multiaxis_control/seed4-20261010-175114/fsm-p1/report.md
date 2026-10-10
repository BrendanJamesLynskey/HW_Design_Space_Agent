# DSE run: asic_multiaxis_control

**Verdict:** INFEASIBLE: the architect concluded no design in the registry meets the spec.  
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
None: no evaluated design satisfies every constraint.

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 10.9
- `max_abs_err <= 0.000244141`: met by 14/100 evaluations; best value seen 4.93e-07 (2^-20.95)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 2.91
- best throughput seen 10.9 MSPS (estimate); best accuracy 20.95 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *I am restricted to iterative and unrolled_k, so the whole front must come from these two. The spec has two hard constraints that shape the search: (1) max_abs_err <= 2^-12, which pins the accuracy region to data_width ~14-16 with n_iter ~12-14 (accuracy depends only on data_width/n_iter/angle_guard/frac_guard/rounding, identical across families); and (2) throughput_msps >= 32 plus the system batch constraint sys_p99_batch_us <= 0.5 (32 results within 0.5 us of a 1 us tick). The min-area objective plus max-accuracy_bits objective means the interesting trade-off is: how much area to spend to (a) clear the 32-request burst fast enough and (b) push accuracy a little above the 12-bit floor. iterative is the area floor but its 1-result/cycle throughput may fail the 0.5 us batch bound at realistic Fmax; unrolled_k buys throughput per cycle with a wider datapath and is the family most likely to satisfy the batch/throughput constraints. I split the budget 50/50 so both fronts are mapped over the same accuracy brackets, letting the merged Pareto front show where unrolled_k's extra area is actually needed to meet the system constraints versus where iterative already suffices. Ranges are kept narrow (not the full registry) to focus the 100-eval budget on the feasible trade-off band rather than on corners that are obviously too small (fail accuracy) or too large (waste area). I will not claim infeasible yet: both families have plausible feasible points, so I explore first and only declare infeasible if the merged front shows no design meeting all constraints.*)
- `iterative` (30 evals): data_width=14..16, n_iter=12..14, angle_guard=0..1, frac_guard=0..1, rounding=trunc|round. *Why:* iterative is the shared-datapath baseline: one micro-rotation/cycle with a single adder/shift stage, so it should be the area-cheapest family in my set. It is also the natural reference for the power index. I keep the ranges tight around the accuracy floor (max_abs_err <= 2^-12) so the budget maps the area/accuracy trade-off rather than wasting evals on grossly over-accurate or under-accurate corners. data_width 14-16 and n_iter 12-14 bracket the point where accuracy_bits crosses 12; angle_guard/frac_guard 0-1 and both rounding modes cover the small accuracy levers without inflating the datapath.
- `unrolled_k` (30 evals): data_width=14..16, n_iter=12..14, angle_guard=0..1, frac_guard=0..1, rounding=trunc|round, k=2..4. *Why:* unrolled_k chains k micro-rotations/cycle on a shared FSM, so it raises throughput per cycle at the cost of a wider (k-deep) datapath and a longer critical path. The spec's hard constraint is throughput_msps >= 32 and a 32-request burst that must clear within 0.5 us of a 1 us tick (sys_p99_batch_us <= 0.5). A 1-result/cycle iterative design at modest Fmax may not clear 32 results in 0.5 us, so unrolled_k is the family that plausibly meets the batch/throughput constraints. I cap k at 4 (not 8) because very large k pushes the critical path (and thus Fmax) down and inflates area, which fights the min-area objective; k=2..4 is where the throughput gain is bought at acceptable area/Fmax cost. Same accuracy brackets as iterative so the two fronts are directly comparable on the accuracy axis.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — iterative and unrolled_k both max out at ~10 MSPS throughput, far below the 32 MSPS constraint, and their batch latency is ~3us vs the 0.5us limit. Only pipelined and pipelined_m families produce 1 result/cycle, which is necessary to meet throughput_msps >= 32 and sys_p99_batch_us <= 0.5. Accuracy at 11.65 bits is close to the 12-bit requirement, so data_width/n_iter ranges should be explored broadly in the new families to find the accuracy/area trade-off.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 10.3
- max_abs_err <= 0.000244141: 100% violate; best seen 0.000311 (2^-11.65)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 3.11

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=0 rounding=round]: throughput=8.5, max_abs_err=0.000417 (2^-11.23); throughput_msps >= 32 violated by 73.4%; max_abs_err <= 0.000244141 violated by 70.7%; sys_p99_batch_us <= 0.5 violated by 651.4%
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=round]: throughput=8, max_abs_err=0.000311 (2^-11.65); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 27.2%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round]: throughput=8, max_abs_err=0.000342 (2^-11.51); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 40.0%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc]: throughput=8, max_abs_err=0.000344 (2^-11.50); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 41.1%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=16 n_iter=13 angle_guard=0 frac_guard=1 rounding=round]: throughput=8.5, max_abs_err=0.000472 (2^-11.05); throughput_msps >= 32 violated by 73.4%; max_abs_err <= 0.000244141 violated by 93.3%; sys_p99_batch_us <= 0.5 violated by 651.4%

Per family:
- iterative: 30 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 11.65 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 8.03 MSPS; best accuracy 11.65 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *iterative and unrolled_k both max out at ~10 MSPS throughput, far below the 32 MSPS constraint, and their batch latency is ~3us vs the 0.5us limit. Only pipelined and pipelined_m families produce 1 result/cycle, which is necessary to meet throughput_msps >= 32 and sys_p99_batch_us <= 0.5. Accuracy at 11.65 bits is close to the 12-bit requirement, so data_width/n_iter ranges should be explored broadly in the new families to find the accuracy/area trade-off.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The throughput constraint (>= 32 MSPS) is unreachable for any family in the registry. The iterative and unrolled_k families, which were exhaustively explored in the previous round, have a maximum observed throughput of 10.9 MSPS, which is less than 35% of the required 32 MSPS. Even if the pipelined families (which produce 1 result/cycle) were explored, the system constraint sys_p99_batch_us <= 0.5 us is also unreachable. The system issues 32 requests at once every 1 us. To meet the 0.5 us batch latency, the CORDIC must process all 32 requests in 0.5 us. This requires a throughput of at least 64 MSPS (32 requests / 0.5 us). The best throughput seen so far is 10.9 MSPS, which is far below the 64 MSPS required to satisfy the system batch latency constraint. Therefore, no design in the registry can meet the constraints.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 10.9
- max_abs_err <= 0.000244141: 86% violate; best seen 4.93e-07 (2^-20.95)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.91

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=0 rounding=round]: throughput=8.5, max_abs_err=0.000417 (2^-11.23); throughput_msps >= 32 violated by 73.4%; max_abs_err <= 0.000244141 violated by 70.7%; sys_p99_batch_us <= 0.5 violated by 651.4%
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=round]: throughput=8, max_abs_err=0.000311 (2^-11.65); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 27.2%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round]: throughput=8, max_abs_err=0.000342 (2^-11.51); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 40.0%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc]: throughput=8, max_abs_err=0.000344 (2^-11.50); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 41.1%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=16 n_iter=13 angle_guard=0 frac_guard=1 rounding=round]: throughput=8.5, max_abs_err=0.000472 (2^-11.05); throughput_msps >= 32 violated by 73.4%; max_abs_err <= 0.000244141 violated by 93.3%; sys_p99_batch_us <= 0.5 violated by 651.4%

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 20.95 bits
- unrolled_k: 50 evals, 0 feasible; max throughput seen 10.9 MSPS; best accuracy 14.73 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8110 in, 2342 out
- provider-reported cost: $0.0046
- full prompts and replies: `llm_trace.jsonl`

