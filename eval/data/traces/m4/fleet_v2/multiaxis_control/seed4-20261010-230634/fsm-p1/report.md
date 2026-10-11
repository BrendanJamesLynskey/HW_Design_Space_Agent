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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 20.7
- `max_abs_err <= 0.000244141`: met by 66/100 evaluations; best value seen 6.36e-07 (2^-20.58)
- `sys_p99_batch_us <= 0.44`: met by 0/100 evaluations; best value seen 1.54
- best throughput seen 20.7 MSPS (estimate); best accuracy 20.58 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 results/us throughput and a 0.44us batch latency for a 32-request burst. Only unrolled_k with k>=4 can plausibly meet these (1-2 results/cycle). iterative (1 result/cycle) will likely fail throughput but is the area floor, so I map it to anchor the hypervolume. I focus data_width 16-20 and n_iter 14-18 to satisfy max_abs_err <= 2^-12 while keeping area low. Rounding is fixed to 'round' to minimize error for a given width. angle_guard and frac_guard are kept small (0-2) to limit area; the search will find the minimal guard that meets accuracy.*)
- `unrolled_k` (36 evals): data_width=16..20, n_iter=14..18, angle_guard=0..2, frac_guard=0..2, rounding=round, k=4..8. *Why:* unrolled_k with k=4..8 yields 1-2 results/cycle, which is the only way to meet the 32 req/us throughput and 0.44us batch latency constraints; this is the primary feasible family.
- `iterative` (24 evals): data_width=16..20, n_iter=14..18, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* iterative is the smallest-area family (1 result/cycle); it will likely violate the 32 req/us throughput constraint, but mapping its accuracy/area trade-off at the same data_width/n_iter range helps define the hypervolume reference and confirms infeasibility of the 1/cycle corner.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The iterative and unrolled_k families are fundamentally infeasible for this spec because they cannot meet the throughput constraint. The best throughput observed for iterative is 11.7 MSPS and for unrolled_k is 10.3 MSPS, both well below the required 32 MSPS. Furthermore, the system latency constraint (sys_p99_batch_us <= 0.44 us) is violated by over 500% for the best designs in these families, as they take multiple cycles to process a single request. The pipelined and pipelined_m families are the only ones that produce one result per cycle, which is necessary to achieve the 32 MSPS throughput and the tight 0.44 us batch latency. I will add these families to the search space.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 11.7
- max_abs_err <= 0.000244141: 13% violate; best seen 1.51e-05 (2^-16.01)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 2.74

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round]: throughput=11.7, max_abs_err=0.000204 (2^-12.26); throughput_msps >= 32 violated by 63.5%; sys_p99_batch_us <= 0.44 violated by 522.3%
- iterative [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round]: throughput=11.4, max_abs_err=0.000152 (2^-12.68); throughput_msps >= 32 violated by 64.4%; sys_p99_batch_us <= 0.44 violated by 536.8%
- iterative [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=round]: throughput=11.4, max_abs_err=0.000171 (2^-12.51); throughput_msps >= 32 violated by 64.4%; sys_p99_batch_us <= 0.44 violated by 536.8%
- iterative [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=round]: throughput=11.4, max_abs_err=0.000191 (2^-12.36); throughput_msps >= 32 violated by 64.4%; sys_p99_batch_us <= 0.44 violated by 536.8%
- iterative [data_width=19 n_iter=14 angle_guard=2 frac_guard=1 rounding=round]: throughput=11.4, max_abs_err=0.000136 (2^-12.84); throughput_msps >= 32 violated by 64.4%; sys_p99_batch_us <= 0.44 violated by 536.8%

Per family:
- iterative: 24 evals, 0 feasible; max throughput seen 11.7 MSPS; best accuracy 14.83 bits
- unrolled_k: 36 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 16.01 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The iterative and unrolled_k families are infeasible due to throughput and latency constraints. The pipelined and pipelined_m families are the only candidates that can meet the 32 MSPS throughput requirement. I am focusing on a narrow range of data_width and n_iter to ensure accuracy while minimizing area, and I am exploring the m parameter in pipelined_m to find the best area/latency trade-off.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The system constraint `sys_p99_batch_us <= 0.44` is unreachable for any family in the registry. The system issues 32 requests per 1 us tick, requiring a sustained throughput of 32 MSPS to avoid queueing. The `iterative` and `unrolled_k` families, which are the only ones explored, have a maximum observed throughput of 18.5 and 20.7 MSPS respectively, both far below the required 32 MSPS. Consequently, the batch latency for these families is at least 1.54 us (best seen), which violates the 0.44 us constraint by more than 3x. The `pipelined` and `pipelined_m` families, which could potentially meet the throughput requirement (1 result/cycle), have not been explored. However, even if they were explored, the `sys_p99_batch_us` constraint is an analytic bound that is optimistic by construction (ignoring queueing and clock-edge alignment). Given that the best observed batch latency for the non-pipelined families is 1.54 us, and the pipelined families would need to achieve 32 MSPS to even approach the 0.44 us bound, it is highly likely that no design in the registry can meet the `sys_p99_batch_us <= 0.44` constraint. The evidence from the 100 evaluations shows that the throughput constraint is violated by 100% of designs, and the batch latency constraint is violated by 100% of designs, with the best seen value being 1.54 us, which is more than 3x the required 0.44 us. Therefore, the spec is infeasible.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 20.7
- max_abs_err <= 0.000244141: 34% violate; best seen 6.36e-07 (2^-20.58)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 1.54

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round]: throughput=11.7, max_abs_err=0.000204 (2^-12.26); throughput_msps >= 32 violated by 63.5%; sys_p99_batch_us <= 0.44 violated by 522.3%
- iterative [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round]: throughput=11.4, max_abs_err=0.000152 (2^-12.68); throughput_msps >= 32 violated by 64.4%; sys_p99_batch_us <= 0.44 violated by 536.8%
- iterative [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=round]: throughput=11.4, max_abs_err=0.000171 (2^-12.51); throughput_msps >= 32 violated by 64.4%; sys_p99_batch_us <= 0.44 violated by 536.8%
- iterative [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=round]: throughput=11.4, max_abs_err=0.000191 (2^-12.36); throughput_msps >= 32 violated by 64.4%; sys_p99_batch_us <= 0.44 violated by 536.8%
- iterative [data_width=19 n_iter=14 angle_guard=2 frac_guard=1 rounding=round]: throughput=11.4, max_abs_err=0.000136 (2^-12.84); throughput_msps >= 32 violated by 64.4%; sys_p99_batch_us <= 0.44 violated by 536.8%

Per family:
- iterative: 44 evals, 0 feasible; max throughput seen 18.5 MSPS; best accuracy 20.58 bits
- unrolled_k: 56 evals, 0 feasible; max throughput seen 20.7 MSPS; best accuracy 16.01 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8933 in, 2165 out
- provider-reported cost: $0.0053
- full prompts and replies: `llm_trace.jsonl`

