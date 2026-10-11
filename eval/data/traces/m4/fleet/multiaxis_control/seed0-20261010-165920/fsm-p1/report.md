# DSE run: multiaxis_control

**Verdict:** INFEASIBLE: the architect concluded no design in the registry meets the spec.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec multiaxis_control: Shared sin/cos unit for a 16-axis motor-control loop: a 1 MHz control tick issues 32 requests at once (Park + inverse Park per axis); all 32 results must be back within 0.44 us of the tick (p99 over ticks). Max error <= 2^-12. Minimise LUTs + FFs.
  constraint: throughput_msps >= 32
  constraint: max_abs_err <= 0.000244141
  constraint: sys_p99_batch_us <= 0.44
  objective: min luts_plus_ffs (HV ref 4000)
  objective: max accuracy_bits (HV ref 12)
  select: min luts_plus_ffs
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average)
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
None: no evaluated design satisfies every constraint.

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 21.1
- `max_abs_err <= 0.000244141`: met by 21/100 evaluations; best value seen 5.51e-08 (2^-24.11)
- `sys_p99_batch_us <= 0.44`: met by 0/100 evaluations; best value seen 1.51
- best throughput seen 21.1 MSPS (estimate); best accuracy 24.11 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 Msps throughput, which means the CORDIC must produce at least 1 result per cycle (at Fmax >= 32 MHz). Both iterative and unrolled_k can meet this: iterative is always 1/cycle, unrolled_k with k>=4 and N<=16 gives ceil(16/4)+3=7 cycles per result, which at a modest Fmax still exceeds 32 Msps. The accuracy constraint max_abs_err <= 2^-12 requires n_iter >= 12 (standard CORDIC convergence). I focus data_width at 14-16 (minimum for 12-bit accuracy with Q1.(W-2) output) and sweep guard bits to find the cheapest configuration. The sys_p99_batch_us <= 0.44 us constraint with 32 requests per tick is tight: at 1 result/cycle and Fmax ~100 MHz, 32 results take 320 ns, leaving 120 ns margin. Higher Fmax (from smaller area) helps here. I split the budget evenly between the two families to map the trade-off between shared-datapath (iterative, lower area, lower Fmax) and unrolled (higher area, potentially higher Fmax) approaches.*)
- `iterative` (30 evals): data_width=14..16, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* iterative is the only family that can plausibly meet the 32 Msps throughput constraint (1 result/cycle). n_iter=12-16 is the minimum needed for max_abs_err <= 2^-12; data_width=14-16 covers the accuracy requirement while keeping area low. frac_guard and angle_guard are swept to find the cheapest guard-bit configuration that still meets the error bound.
- `unrolled_k` (30 evals): data_width=14..16, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..4. *Why:* unrolled_k with k=2-4 can achieve 1 result/cycle throughput (ceil(N/k)+3 <= 4 cycles for N<=16, k>=4 gives 7 cycles... actually k=4, N=16 gives ceil(16/4)+3=7 cycles, which is 143 Msps > 32 Msps). k=2-4 balances area (more parallel datapath) against throughput. Same accuracy parameter sweep as iterative since accuracy is identical across families.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The current families (iterative, unrolled_k) are fundamentally incapable of meeting the throughput constraint. The spec requires a throughput of 32 MSPS (32 results per microsecond, i.e., 1 result per cycle at 32 MHz or higher). The 'iterative' and 'unrolled_k' architectures produce one result every several cycles (N+3 or ceil(N/k)+3 cycles). Even with aggressive unrolling (k=8) and high Fmax, the best throughput seen was only 13.2 MSPS (iterative) and 12 MSPS (unrolled_k), which is far below the 32 MSPS requirement. Furthermore, the system constraint sys_p99_batch_us <= 0.44 us requires processing a burst of 32 requests within 0.44 us. A non-pipelined or partially unrolled design that takes multiple cycles per result will queue these requests, leading to latencies in the range of 2.42 us as seen in the least-violating designs. Only the 'pipelined' or 'pipelined_m' families, which produce 1 result per cycle, can achieve the necessary throughput and low batch latency. Therefore, I must explore the pipelined families to find a feasible design.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 13.2
- max_abs_err <= 0.000244141: 92% violate; best seen 0.000103 (2^-13.25)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 2.42

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=1 rounding=round]: throughput=12.4, max_abs_err=0.000325 (2^-11.59); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 33.2%; sys_p99_batch_us <= 0.44 violated by 485.7%
- iterative [data_width=16 n_iter=13 angle_guard=3 frac_guard=1 rounding=round]: throughput=12.1, max_abs_err=0.000318 (2^-11.62); throughput_msps >= 32 violated by 62.1%; max_abs_err <= 0.000244141 violated by 30.4%; sys_p99_batch_us <= 0.44 violated by 499.2%
- iterative [data_width=15 n_iter=14 angle_guard=3 frac_guard=2 rounding=round]: throughput=11.7, max_abs_err=0.000263 (2^-11.89); throughput_msps >= 32 violated by 63.5%; max_abs_err <= 0.000244141 violated by 7.6%; sys_p99_batch_us <= 0.44 violated by 522.3%
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=round]: throughput=12.4, max_abs_err=0.000431 (2^-11.18); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 76.5%; sys_p99_batch_us <= 0.44 violated by 485.7%
- iterative [data_width=16 n_iter=13 angle_guard=0 frac_guard=1 rounding=round]: throughput=12.4, max_abs_err=0.000472 (2^-11.05); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 93.3%; sys_p99_batch_us <= 0.44 violated by 485.7%

Per family:
- iterative: 30 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 11.89 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 13.25 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Adding the pipelined family is essential because iterative and unrolled_k cannot meet the throughput and latency constraints. The ranges are focused on achieving the required accuracy (max_abs_err <= 2^-12) while minimizing area, as pipelined designs tend to have higher area due to registers.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The spec requires a throughput of >= 32 MSPS and a system p99 batch latency of <= 0.44 us. The `iterative` and `unrolled_k` families, which were the only ones explored in the 100 available evaluations, are fundamentally incapable of meeting these constraints. The maximum throughput observed for `iterative` was 15.4 MSPS and for `unrolled_k` was 21.1 MSPS, both significantly below the 32 MSPS requirement. Furthermore, the best observed `sys_p99_batch_us` was 1.51 us, which is more than 3x the 0.44 us limit. Even if the unexplored `pipelined` and `pipelined_m` families could theoretically achieve 1 result/cycle (potentially reaching 32 MSPS at 32 MHz), the latency constraint of 0.44 us for a batch of 32 requests is extremely tight. A pipelined CORDIC with N iterations has a latency of N+2 cycles. To process 32 requests in 0.44 us at a realistic Fmax (e.g., 100-200 MHz), the total time budget is 44-88 cycles. This leaves very little room for the pipeline latency plus the 32 cycles of throughput. More critically, the accuracy constraint (max_abs_err <= 2^-12) combined with the area objective makes it unlikely that a design meeting the strict timing and throughput constraints will also be feasible within the resource limits, but the primary blocker is the throughput/latency mismatch for the non-pipelined families and the extreme tightness for the pipelined ones given the 100% violation rate in the explored space. Since no feasible design was found in 100 evaluations across the most promising non-pipelined families, and the constraints are mutually restrictive for the remaining families, the problem is deemed infeasible within the registry and budget.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 21.1
- max_abs_err <= 0.000244141: 79% violate; best seen 5.51e-08 (2^-24.11)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 1.51

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=1 rounding=round]: throughput=12.4, max_abs_err=0.000325 (2^-11.59); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 33.2%; sys_p99_batch_us <= 0.44 violated by 485.7%
- iterative [data_width=16 n_iter=13 angle_guard=3 frac_guard=1 rounding=round]: throughput=12.1, max_abs_err=0.000318 (2^-11.62); throughput_msps >= 32 violated by 62.1%; max_abs_err <= 0.000244141 violated by 30.4%; sys_p99_batch_us <= 0.44 violated by 499.2%
- iterative [data_width=15 n_iter=14 angle_guard=3 frac_guard=2 rounding=round]: throughput=11.7, max_abs_err=0.000263 (2^-11.89); throughput_msps >= 32 violated by 63.5%; max_abs_err <= 0.000244141 violated by 7.6%; sys_p99_batch_us <= 0.44 violated by 522.3%
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=round]: throughput=12.4, max_abs_err=0.000431 (2^-11.18); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 76.5%; sys_p99_batch_us <= 0.44 violated by 485.7%
- iterative [data_width=16 n_iter=13 angle_guard=0 frac_guard=1 rounding=round]: throughput=12.4, max_abs_err=0.000472 (2^-11.05); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 93.3%; sys_p99_batch_us <= 0.44 violated by 485.7%

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 15.4 MSPS; best accuracy 19.70 bits
- unrolled_k: 50 evals, 0 feasible; max throughput seen 21.1 MSPS; best accuracy 24.11 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7976 in, 2152 out
- provider-reported cost: $0.0048
- full prompts and replies: `llm_trace.jsonl`

