# DSE run: asic_multiaxis_control

**Verdict:** NO FEASIBLE DESIGN FOUND within the budget (the architect did not declare infeasibility).  
**Architect (LLM):** openrouter: anthropic/claude-sonnet-5.5.  
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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 16.4
- `max_abs_err <= 0.000244141`: met by 18/100 evaluations; best value seen 1.41e-07 (2^-22.76)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 1.95
- best throughput seen 16.4 MSPS (estimate); best accuracy 22.76 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Max error <= 2^-12 needs about 13-14 bit data width with about 12-14 iterations, so I narrowed the ranges to that region to save budget. The batch of 32 results within 0.5 us is the hard constraint, and it needs high throughput from a non-pipelined design. Unrolled_k with large k is the best candidate, so it gets most of the budget. Iterative gets a small probe to check feasibility, and later rounds will tighten the ranges using the results.*)
- `unrolled_k` (45 evals): data_width=13..16, n_iter=11..15, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, k=4..8. *Why:* 32 results within 0.5 us of the tick needs roughly 64 results/us burst rate, so about 2 cycles/result at the cycle rate needed. Chaining k=4..8 micro-rotations per cycle cuts cycles per result to ceil(N/k)+3, with the area of a shared datapath.
- `iterative` (15 evals): data_width=13..16, n_iter=11..15, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* Iterative takes N+3 cycles per result, so 32 results in 0.5 us would need an implausibly fast clock. It is included as a small-budget probe, and its result also shows where the infeasibility boundary sits.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — No design is feasible. Throughput is the binding constraint: the best seen is 9.43 MSPS against the required 32, and sys_p99_batch_us is at best 3.38 against 0.5. Iterative and unrolled_k accept one request every several cycles (N+3, or ceil(N/k)+3), so 32 simultaneous requests queue and cannot finish within 0.5 us. Only pipelined and pipelined_m give 1 result/cycle, so throughput equals Fmax (at least 32 MHz) and the batch time is roughly (32 + latency) cycles at Fmax. Accuracy is reachable: iterative designs already reach 2^-12.2 to 2^-12.4 with W=15-16, N=14-15 and guard bits, with rounding set to round. The next round moves to the pipelined families, in that accuracy region, with a small share kept for lower-area variants.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 9.43
- max_abs_err <= 0.000244141: 93% violate; best seen 0.000188 (2^-12.38)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 3.38

No feasible design found yet. Least-violating designs:
- iterative [data_width=15 n_iter=14 angle_guard=3 frac_guard=3 rounding=round]: throughput=7.7, max_abs_err=0.000215 (2^-12.18); throughput_msps >= 32 violated by 75.9%; sys_p99_batch_us <= 0.5 violated by 729.4%
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round]: throughput=7.7, max_abs_err=0.000204 (2^-12.26); throughput_msps >= 32 violated by 75.9%; sys_p99_batch_us <= 0.5 violated by 729.4%
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=round]: throughput=8, max_abs_err=0.000362 (2^-11.43); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 48.1%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round]: throughput=7.7, max_abs_err=0.000294 (2^-11.73); throughput_msps >= 32 violated by 75.9%; max_abs_err <= 0.000244141 violated by 20.5%; sys_p99_batch_us <= 0.5 violated by 729.4%
- iterative [data_width=15 n_iter=15 angle_guard=2 frac_guard=2 rounding=round]: throughput=7.56, max_abs_err=0.000271 (2^-11.85); throughput_msps >= 32 violated by 76.4%; max_abs_err <= 0.000244141 violated by 11.2%; sys_p99_batch_us <= 0.5 violated by 745.5%

Per family:
- iterative: 15 evals, 0 feasible; max throughput seen 9.43 MSPS; best accuracy 12.38 bits
- unrolled_k: 45 evals, 0 feasible; max throughput seen 7.15 MSPS; best accuracy 11.59 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Pipelined families are the only ones that can satisfy throughput >= 32 and the 0.5 us batch bound. The ranges target W 14-17 and N 12-16, where iterative designs already met the 2^-12 error target.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined_m', 'pipelined'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — This is the final round, so only stop or infeasible are available. 0 of 100 evaluations are feasible and the hypervolume is 0. Throughput is violated by every design (best 16.4 MSPS against 32). sys_p99_batch_us is also violated by every design (best 1.95 us against 0.5). The per-family table shows only iterative (35 evals) and unrolled_k (65 evals) were actually evaluated. Both issue one result every several cycles, so a 32-request burst queues. Accuracy is not the blocker: designs reach 2^-12.2 and better. The pipelined and pipelined_m families, which accept one request per cycle, have no evaluations, so the evidence does not show that the registry cannot meet the constraints. I therefore do not declare infeasible. I stop with no feasible design, and the best next step would be to evaluate pipelined and pipelined_m with the remaining budget.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 16.4
- max_abs_err <= 0.000244141: 82% violate; best seen 1.41e-07 (2^-22.76)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 1.95

No feasible design found yet. Least-violating designs:
- iterative [data_width=15 n_iter=14 angle_guard=3 frac_guard=3 rounding=round]: throughput=7.7, max_abs_err=0.000215 (2^-12.18); throughput_msps >= 32 violated by 75.9%; sys_p99_batch_us <= 0.5 violated by 729.4%
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round]: throughput=7.7, max_abs_err=0.000204 (2^-12.26); throughput_msps >= 32 violated by 75.9%; sys_p99_batch_us <= 0.5 violated by 729.4%
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=round]: throughput=8, max_abs_err=0.000362 (2^-11.43); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 48.1%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round]: throughput=7.7, max_abs_err=0.000294 (2^-11.73); throughput_msps >= 32 violated by 75.9%; max_abs_err <= 0.000244141 violated by 20.5%; sys_p99_batch_us <= 0.5 violated by 729.4%
- iterative [data_width=15 n_iter=15 angle_guard=2 frac_guard=2 rounding=round]: throughput=7.56, max_abs_err=0.000271 (2^-11.85); throughput_msps >= 32 violated by 76.4%; max_abs_err <= 0.000244141 violated by 11.2%; sys_p99_batch_us <= 0.5 violated by 745.5%

Per family:
- iterative: 35 evals, 0 feasible; max throughput seen 16.4 MSPS; best accuracy 22.76 bits
- unrolled_k: 65 evals, 0 feasible; max throughput seen 10.1 MSPS; best accuracy 20.61 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 15544 in, 2810 out
- provider-reported cost: $0.0592
- full prompts and replies: `llm_trace.jsonl`

