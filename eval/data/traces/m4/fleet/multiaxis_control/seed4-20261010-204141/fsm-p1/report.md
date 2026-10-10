# DSE run: multiaxis_control

**Verdict:** INFEASIBLE: the architect concluded no design in the registry meets the spec.  
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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 20.7
- `max_abs_err <= 0.000244141`: met by 39/100 evaluations; best value seen 6.36e-07 (2^-20.58)
- `sys_p99_batch_us <= 0.44`: met by 0/100 evaluations; best value seen 1.54
- best throughput seen 20.7 MSPS (estimate); best accuracy 20.58 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *iterative cannot meet the system batch constraint: it produces one result every N+3 cycles, so 32 requests take 32*(N+3) cycles. For any N that meets the 2^-12 accuracy requirement (N>=13), this needs Fmax > 1 GHz, which is infeasible on Artix-7. Therefore I allocate the entire 100-eval budget to unrolled_k, which can meet both the throughput (>=32 MSPS) and batch (<=0.44 us) constraints with k>=4 and N~13-18. The parameter ranges focus on the minimal-area corner (small W, small N, small guards) while still allowing enough k to reduce cycles and enough guard bits/rounding to achieve the required accuracy. This should map the Pareto front between luts_plus_ffs and accuracy_bits under the system constraints.*)
- `unrolled_k` (60 evals): data_width=14..18, n_iter=13..18, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=4..8. *Why:* unrolled_k is the only family in my assignment that can plausibly satisfy the 0.44 us batch constraint. With N>=13 for 12-bit accuracy, the minimum cycles/result is ceil(N/k)+3; k>=4 keeps this at 5-7 cycles, requiring Fmax >= 364-509 MHz for 32 sequential results in 0.44 us. The ranges cover the smallest W and N that can meet max_abs_err <= 2^-12 (W>=14, N>=13), the k values that reduce cycles enough for the batch constraint (k>=4), and guard bits/rounding to tune accuracy vs area.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — unrolled_k is the wrong shape for this spec, not merely mistuned: no amount of parameter tuning fixes a family that yields one result every several cycles when the spec needs 32 results inside 0.44 us. Best observed values (throughput 9.7 MSPS vs >=32; sys_p99_batch 3.28 us vs <=0.44) are far outside the bounds, while accuracy (best 2^-14.20, need 2^-12) is already met in the explored set. The 1-result/cycle families pipelined and pipelined_m are unmeasured and are the natural fit; explore them before drawing any infeasibility conclusion.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: unrolled_k. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 9.7
- max_abs_err <= 0.000244141: 58% violate; best seen 5.33e-05 (2^-14.20)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 3.28

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round k=5]: throughput=9.7, max_abs_err=0.000209 (2^-12.22); throughput_msps >= 32 violated by 69.7%; sys_p99_batch_us <= 0.44 violated by 645.7%
- unrolled_k [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round k=5]: throughput=9.38, max_abs_err=0.000175 (2^-12.48); throughput_msps >= 32 violated by 70.7%; sys_p99_batch_us <= 0.44 violated by 671.1%
- unrolled_k [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=round k=5]: throughput=9.38, max_abs_err=0.00016 (2^-12.61); throughput_msps >= 32 violated by 70.7%; sys_p99_batch_us <= 0.44 violated by 671.1%
- unrolled_k [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=round k=5]: throughput=9.38, max_abs_err=0.000179 (2^-12.45); throughput_msps >= 32 violated by 70.7%; sys_p99_batch_us <= 0.44 violated by 671.1%
- unrolled_k [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round k=5]: throughput=9.38, max_abs_err=0.000152 (2^-12.68); throughput_msps >= 32 violated by 70.7%; sys_p99_batch_us <= 0.44 violated by 671.1%

Per family:
- unrolled_k: 60 evals, 0 feasible; max throughput seen 9.7 MSPS; best accuracy 14.20 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Every evaluation so far is from unrolled_k, a multi-cycle-per-result family, and it is structurally unable to satisfy the two binding system constraints. Its best throughput is 9.7 MSPS (69.7% short of the 32 MSPS floor) and its best sys_p99_batch_us is 3.28 us (7.5x over the 0.44 us bound) because a k=5, N=14 design needs ceil(14/5)+3 = 6 cycles/result, so 32 simultaneous requests take ~192 cycles. Accuracy is NOT the blocker: max_abs_err=0.000209 already beats the 0.000244141 bound, so a data_width/n_iter region only slightly wider is safe. The registry's 1-result/cycle families (pipelined, pipelined_m) accept one request per cycle, so a 32-request tick drains in ~32 cycles plus latency and throughput = Fmax; neither is anywhere near its limit at Artix-7 Fmax. These families have never been evaluated, so no infeasibility claim is warranted yet. This round should spend the remaining ~40 evals on pipelined and pipelined_m; once a feasible region exists, a later round can map_front over its full ranges.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — Round 2 closed with 0 of 100 evaluations feasible and hypervolume 0 (no gain), so no design in the explored registry space satisfies the spec. The binding constraints are hard, not marginal: (1) throughput_msps >= 32 is violated by 100% of evaluations, best seen 20.7 MSPS (unrolled_k) and 18.5 MSPS (iterative) — a 35-55% shortfall, and these families are structurally multi-cycle per result (N+3 and ceil(N/k)+3 cycles). (2) sys_p99_batch_us <= 0.44 is violated by 100%, best seen 1.54 us (3.5x over the bound); the interface point is decisive: a 1 MHz tick issuing 32 requests at once with all 32 back inside 0.44 us demands ~32/0.44us = ~73 MSPS effective service rate, i.e. more than twice the 32 MSPS average gate, which no evaluated design approaches. (3) Accuracy is not the blocker — 39% of designs already meet 2^-12 (best 6.36e-7), so tightening the accuracy side cannot rescue feasibility. The most promising mixed design (iterative W=15, N=14, angle_guard=4, frac_guard=3, round) still misses throughput by 64% and batch latency by 537%. Evidence therefore points to the throughput/batch-time pair being unreachable by the registry families that can be built here, so I report infeasible rather than selecting a constraint-violating design.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 20.7
- max_abs_err <= 0.000244141: 61% violate; best seen 6.36e-07 (2^-20.58)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 1.54

No feasible design found yet. Least-violating designs:
- iterative [data_width=15 n_iter=14 angle_guard=4 frac_guard=3 rounding=round]: throughput=11.4, max_abs_err=0.000207 (2^-12.24); throughput_msps >= 32 violated by 64.4%; sys_p99_batch_us <= 0.44 violated by 536.8%
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=3 rounding=trunc]: throughput=11.7, max_abs_err=0.000359 (2^-11.44); throughput_msps >= 32 violated by 63.5%; max_abs_err <= 0.000244141 violated by 47.0%; sys_p99_batch_us <= 0.44 violated by 522.3%
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=round]: throughput=11.7, max_abs_err=0.000362 (2^-11.43); throughput_msps >= 32 violated by 63.5%; max_abs_err <= 0.000244141 violated by 48.1%; sys_p99_batch_us <= 0.44 violated by 522.3%
- iterative [data_width=17 n_iter=14 angle_guard=3 frac_guard=0 rounding=trunc]: throughput=11.4, max_abs_err=0.000338 (2^-11.53); throughput_msps >= 32 violated by 64.4%; max_abs_err <= 0.000244141 violated by 38.4%; sys_p99_batch_us <= 0.44 violated by 536.8%
- unrolled_k [data_width=19 n_iter=15 angle_guard=-2 frac_guard=3 rounding=round k=4]: throughput=9.97, max_abs_err=0.000194 (2^-12.33); throughput_msps >= 32 violated by 68.8%; sys_p99_batch_us <= 0.44 violated by 626.2%

Per family:
- iterative: 20 evals, 0 feasible; max throughput seen 18.5 MSPS; best accuracy 20.58 bits
- unrolled_k: 80 evals, 0 feasible; max throughput seen 20.7 MSPS; best accuracy 14.73 bits
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 1)
- tokens: 7569 in, 8532 out
- provider-reported cost: $0.0084
- full prompts and replies: `llm_trace.jsonl`

