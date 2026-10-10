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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 12.8
- `max_abs_err <= 0.000244141`: met by 27/100 evaluations; best value seen 5.51e-08 (2^-24.11)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 2.49
- best throughput seen 12.8 MSPS (estimate); best accuracy 24.11 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Only iterative and unrolled_k are available to me, and both are shared-datapath (smallest area class), so both are the right place to find the min-area design. The accuracy constraint (max_abs_err <= 2^-12) depends only on data_width, n_iter, angle_guard, frac_guard and rounding, so I bracket those tightly: data_width 14-18 and n_iter 12-16 are the region where CORDIC error crosses 2^-12, with guards 0-2 and both rounding modes to let Optuna find the cheapest accurate point. The real tension in this spec is the system constraint: a 1 MHz tick issues 32 requests simultaneously and all 32 must be back within 0.5 us (p99 over ticks), plus a 32 MS/s throughput floor. iterative (1 result per N+3 cycles) is the area floor but its burst-drain latency is the risk; unrolled_k trades area for k-fold faster drain. I weight unrolled_k slightly heavier (0.6) because the p99-batch bound is the binding system constraint and k is the only knob that attacks it, while keeping 0.4 on iterative to anchor the area floor and confirm whether it can pass at all. This split maps the area-vs-burst-latency front across both families within the 100-eval budget.*)
- `iterative` (24 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the smallest-area family (shared datapath, no per-stage registers). It is the only candidate that can plausibly hit min-area while meeting max_abs_err <= 2^-12. data_width 14-18 and n_iter 12-16 bracket the accuracy requirement (accuracy depends only on these + guards + rounding); guards kept low (0-2) to minimise area. Its throughput is the risk: 1 result per N+3 cycles, so it must clear the 32 MS/s constraint and the 0.5 us p99-batch bound - the search will reveal which (W,N) points actually pass.
- `unrolled_k` (36 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..8. *Why:* unrolled_k is the same shared-datapath area class as iterative but issues k micro-rotations/cycle, cutting result latency to ceil(N/k)+3 cycles. This is the key lever for the system constraint: a 1 MHz tick dumps 32 requests at once and all 32 must return within 0.5 us, so the per-result latency and the burst drain rate dominate. Sweeping k=2..8 maps the latency-vs-area trade-off (higher k = more parallel shift/add logic = more area, but faster burst drain). Same accuracy brackets as iterative so the two fronts are directly comparable on the accuracy objective.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The current families (iterative, unrolled_k) cannot meet the throughput constraint of 32 MSPS (best seen 9.22 and 7.94 MSPS respectively) nor the sys_p99_batch_us <= 0.5 constraint (best seen 3.46 us). Only pipelined and pipelined_m families achieve 1 result/cycle, which is necessary to meet the 32 MSPS throughput requirement and the tight 0.5us batch latency for 32 requests. I will explore both pipelined and pipelined_m with full parameter ranges to find feasible designs that meet all constraints while minimizing area.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 9.22
- max_abs_err <= 0.000244141: 75% violate; best seen 7.47e-05 (2^-13.71)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 3.46

No feasible design found yet. Least-violating designs:
- iterative [data_width=17 n_iter=13 angle_guard=1 frac_guard=1 rounding=round]: throughput=8.18, max_abs_err=0.000306 (2^-11.68); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 25.3%; sys_p99_batch_us <= 0.5 violated by 680.5%
- iterative [data_width=17 n_iter=14 angle_guard=0 frac_guard=0 rounding=round]: throughput=8, max_abs_err=0.000301 (2^-11.70); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 23.1%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=17 n_iter=13 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=8.5, max_abs_err=0.000429 (2^-11.19); throughput_msps >= 32 violated by 73.4%; max_abs_err <= 0.000244141 violated by 75.9%; sys_p99_batch_us <= 0.5 violated by 651.4%
- iterative [data_width=17 n_iter=14 angle_guard=0 frac_guard=1 rounding=round]: throughput=7.7, max_abs_err=0.000264 (2^-11.89); throughput_msps >= 32 violated by 75.9%; max_abs_err <= 0.000244141 violated by 8.0%; sys_p99_batch_us <= 0.5 violated by 729.4%
- iterative [data_width=17 n_iter=13 angle_guard=0 frac_guard=2 rounding=round]: throughput=7.89, max_abs_err=0.000365 (2^-11.42); throughput_msps >= 32 violated by 75.3%; max_abs_err <= 0.000244141 violated by 49.4%; sys_p99_batch_us <= 0.5 violated by 709.7%

Per family:
- iterative: 24 evals, 0 feasible; max throughput seen 9.22 MSPS; best accuracy 12.81 bits
- unrolled_k: 36 evals, 0 feasible; max throughput seen 7.94 MSPS; best accuracy 13.71 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The current families (iterative, unrolled_k) cannot meet the throughput constraint of 32 MSPS (best seen 9.22 and 7.94 MSPS respectively) nor the sys_p99_batch_us <= 0.5 constraint (best seen 3.46 us). Only pipelined and pipelined_m families achieve 1 result/cycle, which is necessary to meet the 32 MSPS throughput requirement and the tight 0.5us batch latency for 32 requests. I will explore both pipelined and pipelined_m with full parameter ranges to find feasible designs that meet all constraints while minimizing area.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The spec requires a throughput of >= 32 MSPS and a system p99 batch latency of <= 0.5 us for a burst of 32 requests. The `iterative` and `unrolled_k` families are fundamentally limited by their shared datapath and sequential micro-rotation schedules. In 100 evaluations across these two families, the maximum throughput achieved was only 12.8 MSPS (unrolled_k), which is less than half the required 32 MSPS. Furthermore, the best observed `sys_p99_batch_us` was 2.49 us, which is nearly 5x the 0.5 us constraint. Because the remaining families (`pipelined` and `pipelined_m`) are not yet explored but the current best-case throughput from the non-pipelined architectures is so far below the requirement, and given that this is the final round with no budget left to explore the pipelined families (which would be the only candidates to meet the 32 MSPS and 0.5 us burst constraints), the constraints are effectively unreachable within the remaining evaluation budget. The throughput constraint (>= 32 MSPS) is the primary blocker, as even the most aggressive unrolled_k configurations could not exceed 12.8 MSPS.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 12.8
- max_abs_err <= 0.000244141: 73% violate; best seen 5.51e-08 (2^-24.11)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.49

No feasible design found yet. Least-violating designs:
- iterative [data_width=17 n_iter=13 angle_guard=1 frac_guard=1 rounding=round]: throughput=8.18, max_abs_err=0.000306 (2^-11.68); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 25.3%; sys_p99_batch_us <= 0.5 violated by 680.5%
- iterative [data_width=17 n_iter=14 angle_guard=0 frac_guard=0 rounding=round]: throughput=8, max_abs_err=0.000301 (2^-11.70); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 23.1%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=17 n_iter=13 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=8.5, max_abs_err=0.000429 (2^-11.19); throughput_msps >= 32 violated by 73.4%; max_abs_err <= 0.000244141 violated by 75.9%; sys_p99_batch_us <= 0.5 violated by 651.4%
- iterative [data_width=17 n_iter=14 angle_guard=0 frac_guard=1 rounding=round]: throughput=7.7, max_abs_err=0.000264 (2^-11.89); throughput_msps >= 32 violated by 75.9%; max_abs_err <= 0.000244141 violated by 8.0%; sys_p99_batch_us <= 0.5 violated by 729.4%
- iterative [data_width=17 n_iter=13 angle_guard=0 frac_guard=2 rounding=round]: throughput=7.89, max_abs_err=0.000365 (2^-11.42); throughput_msps >= 32 violated by 75.3%; max_abs_err <= 0.000244141 violated by 49.4%; sys_p99_batch_us <= 0.5 violated by 709.7%

Per family:
- iterative: 44 evals, 0 feasible; max throughput seen 11.5 MSPS; best accuracy 19.70 bits
- unrolled_k: 56 evals, 0 feasible; max throughput seen 12.8 MSPS; best accuracy 24.11 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8119 in, 2482 out
- provider-reported cost: $0.0039
- full prompts and replies: `llm_trace.jsonl`

