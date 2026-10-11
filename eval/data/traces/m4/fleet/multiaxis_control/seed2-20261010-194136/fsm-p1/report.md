# DSE run: multiaxis_control

**Verdict:** NO FEASIBLE DESIGN FOUND within the budget (the architect did not declare infeasibility).  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 23.7
- `max_abs_err <= 0.000244141`: met by 22/100 evaluations; best value seen 2.86e-07 (2^-21.74)
- `sys_p99_batch_us <= 0.44`: met by 0/100 evaluations; best value seen 1.35
- best throughput seen 23.7 MSPS (estimate); best accuracy 21.74 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The system scenario demands 32 results within 0.44 us of a 1 MHz tick (p99 batch latency). This is a hard batch-latency constraint that dominates family choice. Iterative processes one result every N+3 cycles, so for N>=12 it would need >480 MHz to meet the batch deadline. Unrolled_k with high k (6..8) reduces cycles/result to ceil(N/k)+3; with k=8 and N=12 this is 5 cycles, requiring ~363 MHz, which is at least plausible. Therefore 90% of the budget goes to unrolled_k over wide ranges of data_width, n_iter, angle_guard, frac_guard, rounding, and k to map the area-accuracy trade-off and find the smallest design that satisfies max_abs_err <= 2^-12 and the batch bound. The remaining 10% probes iterative to confirm it cannot meet the constraints, avoiding wasted budget on a likely infeasible family.*)
- `unrolled_k` (54 evals): data_width=12..18, n_iter=10..16, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=6..8. *Why:* Only unrolled_k can plausibly meet the tight batch-latency constraint. With k=8 and N=12, cycles/result = ceil(12/8)+3 = 5, so 32 results take 160 cycles; at 0.44 us this needs Fmax >= 363 MHz. k=6..8 and N=10..16 explore the trade-off between area (lower k, lower N, lower W) and accuracy (higher N, higher W, guards). The ranges cover the minimal area that can still achieve max_abs_err <= 2^-12.
- `iterative` (6 evals): data_width=12..16, n_iter=12..14, angle_guard=0..1, frac_guard=0..1, rounding=round. *Why:* Iterative is very unlikely to meet the batch-latency constraint: cycles/result = N+3, so 32 results take 32*(N+3) cycles. For N>=12 (needed for 2^-12 accuracy), this requires Fmax >= 480 MHz, which is implausible on Artix-7. A small budget confirms infeasibility and checks whether any low-N, low-W corner could unexpectedly pass the L1 bound.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — Only sequential-throughput families (iterative, unrolled_k) have been sampled, giving 0 feasible designs and a hypervolume of 0: throughput 100% violated (best 13.5 MSPS) and sys_p99_batch_us 100% violated (best 2.36 vs 0.44). Both failures are structural, not parametric - one result every several cycles cannot drain 32 simultaneous requests inside the tick deadline, no matter how W/N/k are tuned. Accuracy is not the blocker (best seen 2^-13.39, already past the 2^-12 limit). The unexplored pipelined and pipelined_m families produce 1 result/cycle and are the only way to meet throughput_msps>=32 and the 0.44 us batch bound, so add them now rather than refining the sequential ranges.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 13.5
- max_abs_err <= 0.000244141: 83% violate; best seen 9.31e-05 (2^-13.39)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 2.36

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=17 n_iter=12 angle_guard=1 frac_guard=1 rounding=round k=6]: throughput=9.76, max_abs_err=0.00054 (2^-10.85); throughput_msps >= 32 violated by 69.5%; max_abs_err <= 0.000244141 violated by 121.3%; sys_p99_batch_us <= 0.44 violated by 640.6%
- unrolled_k [data_width=18 n_iter=12 angle_guard=1 frac_guard=0 rounding=round k=6]: throughput=9.44, max_abs_err=0.000522 (2^-10.90); throughput_msps >= 32 violated by 70.5%; max_abs_err <= 0.000244141 violated by 113.7%; sys_p99_batch_us <= 0.44 violated by 666.0%
- unrolled_k [data_width=18 n_iter=12 angle_guard=1 frac_guard=1 rounding=round k=6]: throughput=9.44, max_abs_err=0.000522 (2^-10.90); throughput_msps >= 32 violated by 70.5%; max_abs_err <= 0.000244141 violated by 113.8%; sys_p99_batch_us <= 0.44 violated by 666.0%
- unrolled_k [data_width=17 n_iter=12 angle_guard=0 frac_guard=1 rounding=round k=6]: throughput=9.76, max_abs_err=0.000616 (2^-10.67); throughput_msps >= 32 violated by 69.5%; max_abs_err <= 0.000244141 violated by 152.1%; sys_p99_batch_us <= 0.44 violated by 640.6%
- unrolled_k [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round k=6]: throughput=8.13, max_abs_err=0.000158 (2^-12.63); throughput_msps >= 32 violated by 74.6%; sys_p99_batch_us <= 0.44 violated by 789.6%

Per family:
- iterative: 6 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 9.61 bits
- unrolled_k: 54 evals, 0 feasible; max throughput seen 10.1 MSPS; best accuracy 13.39 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 1 explored only the two sub-unity-throughput families (iterative, unrolled_k), so 100% of the 60 evals miss throughput_msps>=32 (best 13.5) and 100% miss sys_p99_batch_us<=0.44 (best 2.36): these families accept ~1 request per N/k cycles and therefore queue a 32-request burst, which the burst-sensitive sys_p99_batch_us penalises directly. The accuracy axis is already reachable (best max_abs_err 9.31e-05 = 2^-13.39, and designs at n_iter=15 clear 2^-12), so the binding limits are purely throughput/burst. pipelined (1 result/cycle, N+2 latency) and pipelined_m (1 result/cycle, ceil(N/m)+2 latency) are the only registry families that can supply 32 results within 0.44 us while keeping luts_plus_ffs competitive, so spend the remaining budget bringing them onto the front. Keep rounding=round and W 14..20 / N 12..20 since that region already shows the 2^-12 accuracy is achievable with margin.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — Budget is exhausted (100/100 evals, final round), so the only admissible choices are stop or infeasible — and infeasible is not supported by the evidence. The two constraints that never passed are throughput_msps >= 32 and sys_p99_batch_us <= 0.44, but both were only ever measured on the registry's MULTI-CYCLE families: iterative (N+3 cycles/result, max 23.7 MSPS seen) and unrolled_k (ceil(N/k)+3 cycles/result, max 14.8 MSPS; best batch 1.35 us = 3.1x over budget). Those families are structurally incapable of the >32 MSPS needed to drain 32 requests in 0.44 us, which is exactly why 0 of 100 designs are feasible and hypervolume is 0. The registry also contains pipelined (1 result/cycle) and pipelined_m, which were never sampled by any round; a 1-result/cycle design clears 32 MSPS at any Fmax above ~32 MHz and 32 back-to-back requests in ~32 cycles, so the evidence does NOT show the constraints are unreachable. The accuracy target is clearly reachable (best max_abs_err 2.86e-07 = 2^-21.7, and 2^-12.63 at data_width=17/n_iter=15, both inside 2^-12), so accuracy is not the blocker. Verdict: no feasible design was found within the evaluation budget, and the search covered only the half of the registry that cannot satisfy the burst requirement; this is a budget-ended 'no feasible design found', not a proven infeasible registry. No design can be selected, and the front has no non-violating member to rank, so the run stops here.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 23.7
- max_abs_err <= 0.000244141: 78% violate; best seen 2.86e-07 (2^-21.74)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 1.35

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=17 n_iter=12 angle_guard=1 frac_guard=1 rounding=round k=6]: throughput=9.76, max_abs_err=0.00054 (2^-10.85); throughput_msps >= 32 violated by 69.5%; max_abs_err <= 0.000244141 violated by 121.3%; sys_p99_batch_us <= 0.44 violated by 640.6%
- unrolled_k [data_width=18 n_iter=12 angle_guard=1 frac_guard=0 rounding=round k=6]: throughput=9.44, max_abs_err=0.000522 (2^-10.90); throughput_msps >= 32 violated by 70.5%; max_abs_err <= 0.000244141 violated by 113.7%; sys_p99_batch_us <= 0.44 violated by 666.0%
- unrolled_k [data_width=18 n_iter=12 angle_guard=1 frac_guard=1 rounding=round k=6]: throughput=9.44, max_abs_err=0.000522 (2^-10.90); throughput_msps >= 32 violated by 70.5%; max_abs_err <= 0.000244141 violated by 113.8%; sys_p99_batch_us <= 0.44 violated by 666.0%
- unrolled_k [data_width=17 n_iter=12 angle_guard=0 frac_guard=1 rounding=round k=6]: throughput=9.76, max_abs_err=0.000616 (2^-10.67); throughput_msps >= 32 violated by 69.5%; max_abs_err <= 0.000244141 violated by 152.1%; sys_p99_batch_us <= 0.44 violated by 640.6%
- unrolled_k [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round k=6]: throughput=8.13, max_abs_err=0.000158 (2^-12.63); throughput_msps >= 32 violated by 74.6%; sys_p99_batch_us <= 0.44 violated by 789.6%

Per family:
- iterative: 26 evals, 0 feasible; max throughput seen 23.7 MSPS; best accuracy 21.74 bits
- unrolled_k: 74 evals, 0 feasible; max throughput seen 14.8 MSPS; best accuracy 20.73 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7709 in, 10084 out
- provider-reported cost: $0.0104
- full prompts and replies: `llm_trace.jsonl`

