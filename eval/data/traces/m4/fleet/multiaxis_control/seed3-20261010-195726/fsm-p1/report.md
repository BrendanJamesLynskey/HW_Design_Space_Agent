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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 22
- `max_abs_err <= 0.000244141`: met by 35/100 evaluations; best value seen 3.12e-08 (2^-24.93)
- `sys_p99_batch_us <= 0.44`: met by 0/100 evaluations; best value seen 1.45
- best throughput seen 22.0 MSPS (estimate); best accuracy 24.93 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec's system constraint (32 requests within 0.44 us of a 1 MHz tick) demands very high instantaneous throughput. iterative cannot plausibly meet this because its serial nature forces Fmax >= 72.7*(N+3) MHz, which for N>=12 (needed for 2^-12 accuracy) exceeds 1 GHz. unrolled_k can meet it by processing k micro-rotations per cycle, trading area for throughput. We allocate 10% of the budget to iterative to confirm infeasibility and 90% to unrolled_k to map the Pareto front over k, N, and data_width, focusing on the feasible region where accuracy_bits >= 12 and sys_p99_batch_us <= 0.44.*)
- `iterative` (6 evals): data_width=12..20, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Low area but serial (1 micro-rotation/cycle). To meet the 32-request burst within 0.44 us, it would need Fmax >= 72.7*(N+3) MHz; for N>=12 (needed for 2^-12 accuracy) this exceeds 1 GHz, likely infeasible on Artix-7. Small budget to confirm infeasibility and catch any edge case with very high Fmax and low N.
- `unrolled_k` (54 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=3..8. *Why:* Processes k micro-rotations/cycle, reducing cycles/result to ceil(N/k)+3. With k=8 and N=12..16, cycles/result is 5..6, requiring Fmax ~360..440 MHz, which is plausible on Artix-7. Main family to map the feasible Pareto front of area vs accuracy under the batch constraint. Ranges cover the accuracy boundary (N~12-16, W~14-16) and throughput boundary (k~4-8).

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — Accuracy is not the blocker (best 2^-16.57 vs required 2^-12, and it is family-independent); the blockers are throughput_msps >= 32 (best 17.2) and sys_p99_batch_us <= 0.44 (best 1.85 us), both rate constraints unreachable in the multi-cycle iterative/unrolled_k families. Only the pipelined families deliver 1 result/cycle.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 17.2
- max_abs_err <= 0.000244141: 67% violate; best seen 1.03e-05 (2^-16.57)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 1.85

No feasible design found yet. Least-violating designs:
- iterative [data_width=18 n_iter=15 angle_guard=4 frac_guard=0 rounding=trunc]: throughput=10.8, max_abs_err=0.000202 (2^-12.27); throughput_msps >= 32 violated by 66.4%; sys_p99_batch_us <= 0.44 violated by 574.3%
- iterative [data_width=17 n_iter=15 angle_guard=3 frac_guard=2 rounding=trunc]: throughput=10.8, max_abs_err=0.00013 (2^-12.91); throughput_msps >= 32 violated by 66.4%; sys_p99_batch_us <= 0.44 violated by 574.3%
- iterative [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round]: throughput=10.4, max_abs_err=0.000121 (2^-13.02); throughput_msps >= 32 violated by 67.4%; sys_p99_batch_us <= 0.44 violated by 595.7%
- unrolled_k [data_width=17 n_iter=13 angle_guard=1 frac_guard=4 rounding=round k=4]: throughput=9.97, max_abs_err=0.000284 (2^-11.78); throughput_msps >= 32 violated by 68.8%; max_abs_err <= 0.000244141 violated by 16.3%; sys_p99_batch_us <= 0.44 violated by 626.2%
- unrolled_k [data_width=20 n_iter=13 angle_guard=4 frac_guard=4 rounding=round k=4]: throughput=9.65, max_abs_err=0.000245 (2^-12.00); throughput_msps >= 32 violated by 69.8%; max_abs_err <= 0.000244141 violated by 0.3%; sys_p99_batch_us <= 0.44 violated by 649.9%

Per family:
- iterative: 6 evals, 0 feasible; max throughput seen 17.2 MSPS; best accuracy 13.02 bits
- unrolled_k: 54 evals, 0 feasible; max throughput seen 14 MSPS; best accuracy 16.57 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The front is empty and the failure pattern is unambiguous. Accuracy is already solved: the best design seen reaches 2^-16.57 (constraint is 2^-12), and rule says accuracy depends only on data_width/n_iter/angle_guard/frac_guard/rounding, i.e. it is family-independent. The two binding constraints are throughput_msps >= 32 (100% violate, best 17.2 MSPS) and sys_p99_batch_us <= 0.44 (100% violate, best 1.85 us) - both are rate constraints. iterative and unrolled_k are inherently multi-cycle-per-result families: their best observed throughputs (17.2 and 14.0 MSPS) are far below 32 and their N+3 / ceil(N/k)+3 result intervals make a 32-request burst take ~1.9-2.9 us. No amount of parameter refinement inside those families can close a 2x rate gap, so refine/widen are wasted budget. pipelined and pipelined_m emit 1 result/cycle, so throughput_msps = fmax (Artix-7 CORDIC pipelines clear 32 MSPS comfortably), and a 32-deep burst completes in roughly (N+2)+31 cycles - at ~100 MHz with N~12-16 that is ~0.33-0.49 us, which is why I pin n_iter to 10..16 so the batch tail fits the 0.44 us window. Budget: 40 evals left, ~24 to pipelined and ~16 to pipelined_m, data_width 14..20 to hold accuracy well above 12 bits without paying area, and m 2..4 to probe the Fmax/register-count trade that directly drives the luts_plus_ffs objective.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — Budget exhausted (100/100 evals, final round) and no feasible design found: 0/100 evaluations satisfy the constraints. The hard blockers are throughput and burst latency: best throughput seen is 22 MSPS (iterative) vs the required 32 MSPS, and best sys_p99_batch_us is 1.45 us vs the required 0.44 us. Accuracy is not the blocker — best max_abs_err is 3.12e-08 (2^-24.93), far below the 2^-12 limit. The explored families (iterative, unrolled_k) top out well below 32 MSPS and their 32-request batch times are ~1.45 us, >0.44 us. Pipelined/pipelined_m would be the natural families to test for 1 result/cycle, but no evaluation budget remains, so I stop rather than claim the entire registry is infeasible.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 22
- max_abs_err <= 0.000244141: 65% violate; best seen 3.12e-08 (2^-24.93)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 1.45

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=17 n_iter=12 angle_guard=2 frac_guard=3 rounding=round k=3]: throughput=13.1, max_abs_err=0.000523 (2^-10.90); throughput_msps >= 32 violated by 59.0%; max_abs_err <= 0.000244141 violated by 114.2%; sys_p99_batch_us <= 0.44 violated by 452.2%
- unrolled_k [data_width=22 n_iter=12 angle_guard=4 frac_guard=1 rounding=trunc k=3]: throughput=12.7, max_abs_err=0.000489 (2^-11.00); throughput_msps >= 32 violated by 60.3%; max_abs_err <= 0.000244141 violated by 100.2%; sys_p99_batch_us <= 0.44 violated by 470.0%
- unrolled_k [data_width=22 n_iter=12 angle_guard=-2 frac_guard=1 rounding=round k=3]: throughput=12.7, max_abs_err=0.000494 (2^-10.98); throughput_msps >= 32 violated by 60.3%; max_abs_err <= 0.000244141 violated by 102.3%; sys_p99_batch_us <= 0.44 violated by 470.0%
- iterative [data_width=20 n_iter=12 angle_guard=4 frac_guard=3 rounding=trunc]: throughput=12.6, max_abs_err=0.000491 (2^-10.99); throughput_msps >= 32 violated by 60.5%; max_abs_err <= 0.000244141 violated by 101.0%; sys_p99_batch_us <= 0.44 violated by 474.5%
- iterative [data_width=21 n_iter=12 angle_guard=-1 frac_guard=4 rounding=round]: throughput=12.6, max_abs_err=0.000493 (2^-10.99); throughput_msps >= 32 violated by 60.5%; max_abs_err <= 0.000244141 violated by 101.9%; sys_p99_batch_us <= 0.44 violated by 474.5%

Per family:
- iterative: 26 evals, 0 feasible; max throughput seen 22 MSPS; best accuracy 24.93 bits
- unrolled_k: 74 evals, 0 feasible; max throughput seen 19.1 MSPS; best accuracy 20.61 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7664 in, 9951 out
- provider-reported cost: $0.0096
- full prompts and replies: `llm_trace.jsonl`

