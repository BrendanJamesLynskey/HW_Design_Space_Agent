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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 22.6
- `max_abs_err <= 0.000244141`: met by 55/100 evaluations; best value seen 1.15e-06 (2^-19.73)
- `sys_p99_batch_us <= 0.44`: met by 0/100 evaluations; best value seen 1.41
- best throughput seen 22.6 MSPS (estimate); best accuracy 19.73 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec's system constraint sys_p99_batch_us <= 0.44 is the binding one: 32 requests in 0.44 us requires ~73 Msps effective throughput. Iterative cannot achieve this because its cycles/result is at least N+3, and N must be >=12 for the 2^-12 accuracy constraint, giving >=15 cycles/result and requiring >1 GHz Fmax. unrolled_k can reduce cycles/result by chaining k micro-rotations per cycle. With N=12..16 and k=6..8, cycles/result is 5, requiring Fmax >= 363 MHz, which is challenging but plausible. We allocate the entire 100-eval budget to unrolled_k, searching data_width 12..20, n_iter 12..20, angle_guard -2..4, frac_guard 0..4, rounding trunc/round, and k 4..8. This covers the feasible region for accuracy and area while letting Optuna focus on the minimal-area designs that meet all constraints.*)
- `unrolled_k` (60 evals): data_width=12..20, n_iter=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=4..8. *Why:* Only family that can plausibly meet the system batch constraint. The control tick issues 32 requests at once and all must finish within 0.44 us, implying an effective throughput of ~73 Msps. Iterative has cycles/result = N+3 >= 15 for N>=12 (needed for 2^-12 accuracy), requiring Fmax > 1 GHz, which is infeasible on Artix-7. unrolled_k reduces cycles/result to ceil(N/k)+3; with N>=12 and k>=6, this is 5 cycles, needing Fmax >= 363 MHz. The ranges cover the trade-off between area (W, N, k, guards) and accuracy/throughput, focusing on N=12..16 and k=6..8 where cycles/result is minimal, while allowing wider exploration to map the Pareto front.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — 0/60 feasible; all unrolled_k violate throughput (best 9.97 < 32) and sys_p99_batch (best 3.2 > 0.44). Accuracy already exceeds the spec (best 2^-16.11 vs 2^-12), so the bottleneck is results/cycle and burst latency. Only pipelined / pipelined_m offer 1 result/cycle; iterative and unrolled_k with shared FSM cannot plausibly close the 3.2 us -> 0.44 us gap. Add those families next.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: unrolled_k. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 9.97
- max_abs_err <= 0.000244141: 32% violate; best seen 1.42e-05 (2^-16.11)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 3.2

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=19 n_iter=14 angle_guard=1 frac_guard=0 rounding=round k=4]: throughput=9.97, max_abs_err=0.000145 (2^-12.76); throughput_msps >= 32 violated by 68.8%; sys_p99_batch_us <= 0.44 violated by 626.2%
- unrolled_k [data_width=19 n_iter=14 angle_guard=-1 frac_guard=0 rounding=round k=4]: throughput=9.97, max_abs_err=0.000181 (2^-12.43); throughput_msps >= 32 violated by 68.8%; sys_p99_batch_us <= 0.44 violated by 626.2%
- unrolled_k [data_width=18 n_iter=14 angle_guard=-1 frac_guard=4 rounding=round k=4]: throughput=9.97, max_abs_err=0.00024 (2^-12.03); throughput_msps >= 32 violated by 68.8%; sys_p99_batch_us <= 0.44 violated by 626.2%
- unrolled_k [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=trunc k=4]: throughput=9.97, max_abs_err=0.00024 (2^-12.03); throughput_msps >= 32 violated by 68.8%; sys_p99_batch_us <= 0.44 violated by 626.2%
- unrolled_k [data_width=19 n_iter=14 angle_guard=-1 frac_guard=0 rounding=round k=5]: throughput=9.38, max_abs_err=0.000181 (2^-12.43); throughput_msps >= 32 violated by 70.7%; sys_p99_batch_us <= 0.44 violated by 671.1%

Per family:
- unrolled_k: 60 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 16.11 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *All 60 evaluations so far are unrolled_k and 0/60 feasible. The binding constraints are throughput_msps >= 32 and sys_p99_batch_us <= 0.44: best unrolled_k throughput is only 9.97 MSPS and best sys_p99_batch is 3.2 us, both structurally limited by multi-cycle shared-FSM scheduling. Accuracy is not the bottleneck: best max_abs_err seen is 2^-16.11, far below the required 2^-12. iterative is even worse for throughput, so the missing families that can produce one result per cycle are pipelined and pipelined_m. Explore those next, with n_iter biased low for latency and data_width/guards wide enough to keep accuracy above 12 bits.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — Budget exhausted (100/100 evals) and the run must terminate. The front is empty (0/100 feasible, hypervolume 0, +0.0% gain), and both evaluated families are structurally wrong for this spec: iterative and unrolled_k emit one result every several cycles (N+3 and ceil(N/k)+3), so the best throughput ever seen is 22.6 MSPS (< 32 required) and the best sys_p99_batch_us is 1.41 us vs the 0.44 us burst bound (3.2x over). Accuracy is not the blocker: the bit-accurate model already shows 2^-12.76 at n_iter=14, so max_abs_err <= 2^-12 is reachable. Crucially, I cannot justify `infeasible`: the registry's one-result-per-cycle families (pipelined, pipelined_m) received 0 of the 100 evaluations, and the 32-request/0.44 us burst bound structurally calls for exactly that 1-result/cycle behaviour (32 results need ~32 cycles plus N+2 latency, i.e. only a moderate Fmax once N>=14 is chosen for 12-bit accuracy). Declaring the whole registry infeasible would therefore be an unproven claim about untested families, so I stop rather than settle on a design that violates the constraints, and flag that the exploration missed the pipelined families.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 22.6
- max_abs_err <= 0.000244141: 45% violate; best seen 1.15e-06 (2^-19.73)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 1.41

No feasible design found yet. Least-violating designs:
- iterative [data_width=19 n_iter=12 angle_guard=3 frac_guard=2 rounding=round]: throughput=12.9, max_abs_err=0.000494 (2^-10.98); throughput_msps >= 32 violated by 59.6%; max_abs_err <= 0.000244141 violated by 102.3%; sys_p99_batch_us <= 0.44 violated by 461.7%
- iterative [data_width=20 n_iter=12 angle_guard=0 frac_guard=2 rounding=round]: throughput=12.9, max_abs_err=0.000495 (2^-10.98); throughput_msps >= 32 violated by 59.6%; max_abs_err <= 0.000244141 violated by 102.6%; sys_p99_batch_us <= 0.44 violated by 461.7%
- iterative [data_width=20 n_iter=12 angle_guard=0 frac_guard=0 rounding=round]: throughput=12.9, max_abs_err=0.000497 (2^-10.98); throughput_msps >= 32 violated by 59.6%; max_abs_err <= 0.000244141 violated by 103.5%; sys_p99_batch_us <= 0.44 violated by 461.7%
- unrolled_k [data_width=24 n_iter=12 angle_guard=0 frac_guard=3 rounding=round k=3]: throughput=12.3, max_abs_err=0.000488 (2^-11.00); throughput_msps >= 32 violated by 61.5%; max_abs_err <= 0.000244141 violated by 99.9%; sys_p99_batch_us <= 0.44 violated by 487.8%
- unrolled_k [data_width=19 n_iter=14 angle_guard=1 frac_guard=0 rounding=round k=4]: throughput=9.97, max_abs_err=0.000145 (2^-12.76); throughput_msps >= 32 violated by 68.8%; sys_p99_batch_us <= 0.44 violated by 626.2%

Per family:
- iterative: 20 evals, 0 feasible; max throughput seen 22.6 MSPS; best accuracy 19.73 bits
- unrolled_k: 80 evals, 0 feasible; max throughput seen 17.4 MSPS; best accuracy 18.96 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7591 in, 25100 out
- provider-reported cost: $0.0203
- full prompts and replies: `llm_trace.jsonl`

