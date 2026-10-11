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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 21.1
- `max_abs_err <= 0.000244141`: met by 28/100 evaluations; best value seen 5.51e-08 (2^-24.11)
- `sys_p99_batch_us <= 0.44`: met by 0/100 evaluations; best value seen 1.51
- best throughput seen 21.1 MSPS (estimate); best accuracy 24.11 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires a shared sin/cos unit for a 16-axis motor-control loop with a 1 MHz tick issuing 32 requests at once, all results back within 0.44 us (p99 batch). This translates to an instantaneous throughput requirement of ~72.7 results/us during the burst, far above the average 32 results/us. The accuracy constraint max_abs_err <= 2^-12 requires at least ~12 CORDIC iterations and sufficient datapath width. Iterative designs cannot meet the burst latency because their cycles-per-result is N+3 >= 15, demanding an impossible Fmax. Unrolled_k with k >= 6 reduces cycles-per-result to ceil(N/k)+3 <= 5 for N >= 12, making the batch bound achievable at ~364 MHz. The exploration therefore focuses almost entirely on unrolled_k, searching k = 4..8 to trade off critical path (Fmax) against cycles-per-result, and N = 10..18, data_width = 12..20, angle_guard = -1..3, frac_guard = 0..3, rounding = trunc/round to find the minimum-area design that meets both accuracy and burst latency. A 5% budget is reserved for iterative to formally confirm infeasibility. The L1 system bound is optimistic, so designs with margin (e.g., batch time well under 0.44 us) are preferred; the search ranges allow Optuna to discover such designs while minimising luts_plus_ffs.*)
- `unrolled_k` (55 evals): data_width=12..20, n_iter=10..18, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, k=4..8. *Why:* The system constraint sys_p99_batch_us <= 0.44 us with 32 simultaneous requests per 1 us tick is the binding constraint. For unrolled_k, cycles per result C = ceil(N/k)+3. To meet the batch bound at a plausible Artix-7 Fmax (~400 MHz), we need C <= 5, i.e. ceil(N/k) <= 2. For N >= 12 (needed for 2^-12 accuracy), this requires k >= 6. However, higher k increases the critical path and may reduce Fmax, so we search k = 4..8 to find the area-optimal balance. N is searched 10..18 to find the minimum iterations that meet accuracy. data_width 12..20 covers the range where output LSB and internal CORDIC errors can reach 2^-12. angle_guard and frac_guard are searched to recover accuracy without over-widening the datapath. This family is the only one that can plausibly satisfy both the accuracy and the burst-latency constraints.
- `iterative` (5 evals): data_width=12..20, n_iter=10..18, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* Iterative computes one micro-rotation per cycle, so cycles per result = N+3. For N >= 12, this is >= 15 cycles. To process 32 requests within 0.44 us, the required Fmax would be >= 72.7 * (N+3) >= 1090 MHz, which is far beyond Artix-7 capabilities. A small budget is allocated only to confirm infeasibility and to check whether any very low-N design could somehow meet the accuracy constraint (it cannot, as N < 12 gives error > 2^-12). This family is not expected to contribute to the Pareto front.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — Two independent hard walls, both structural. (1) throughput_msps >= 32 is violated by 100% of evals with best 15.3 (iterative) and 12 (unrolled_k); those families spend N+3 or ceil(N/k)+3 cycles per result, so even the fastest observed is ~2x short of 32 MSPS. (2) sys_p99_batch_us <= 0.44 is violated by 100% with best 2.09 (=~21x over): a 32-request-at-once tick cannot be drained by a sub-1-result/cycle datapath, exactly the burst penalty the spec warns about. Both walls are removed only by the 1-result/cycle families (pipelined, pipelined_m), which are unexplored. Accuracy is close but not yet met (best 2^-11.85 vs required 2^-12 at d=15,n=15,guard 2/2), so the pipelined ranges keep data_width 13-18, n_iter 8-16 and both guards 0-3 to find the >=2^-12 region while letting the search trade iterations for area. n_iter is kept low enough that N+2 latency plus 32 drain cycles fits the 0.44 us window. Budget: 40 evals remain.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 15.3
- max_abs_err <= 0.000244141: 80% violate; best seen 7.18e-05 (2^-13.77)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 2.09

No feasible design found yet. Least-violating designs:
- iterative [data_width=18 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=13.2, max_abs_err=0.000575 (2^-10.76); throughput_msps >= 32 violated by 58.7%; max_abs_err <= 0.000244141 violated by 135.7%; sys_p99_batch_us <= 0.44 violated by 449.0%
- unrolled_k [data_width=15 n_iter=15 angle_guard=2 frac_guard=2 rounding=round k=4]: throughput=10.3, max_abs_err=0.000271 (2^-11.85); throughput_msps >= 32 violated by 67.8%; max_abs_err <= 0.000244141 violated by 11.2%; sys_p99_batch_us <= 0.44 violated by 602.5%
- unrolled_k [data_width=20 n_iter=12 angle_guard=1 frac_guard=1 rounding=round k=4]: throughput=11.6, max_abs_err=0.000494 (2^-10.98); throughput_msps >= 32 violated by 63.7%; max_abs_err <= 0.000244141 violated by 102.2%; sys_p99_batch_us <= 0.44 violated by 522.0%
- unrolled_k [data_width=20 n_iter=12 angle_guard=0 frac_guard=0 rounding=round k=4]: throughput=11.6, max_abs_err=0.000497 (2^-10.98); throughput_msps >= 32 violated by 63.7%; max_abs_err <= 0.000244141 violated by 103.5%; sys_p99_batch_us <= 0.44 violated by 522.0%
- unrolled_k [data_width=19 n_iter=12 angle_guard=2 frac_guard=1 rounding=round k=4]: throughput=11.6, max_abs_err=0.000498 (2^-10.97); throughput_msps >= 32 violated by 63.7%; max_abs_err <= 0.000244141 violated by 104.1%; sys_p99_batch_us <= 0.44 violated by 522.0%

Per family:
- iterative: 5 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 10.76 bits
- unrolled_k: 55 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 13.77 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *throughput and batch constraints are structurally out of reach for the two explored families*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — Round 2 is complete with the full 100-eval budget spent and it is the final round, so only stop/infeasible are available. Evidence says the explored front is empty and cannot improve: 0 of 100 evaluations feasible, hypervolume 0 (gain +0.0%), and the two binding constraints are violated by every design — throughput_msps best seen 21.1 (unrolled_k) vs 32 required, and sys_p99_batch_us best 1.51 vs 0.44 required. Accuracy is not the blocker at all: 28% of designs already satisfy max_abs_err <= 2.44e-4, with a best of 5.51e-8 (2^-24.11 bits), far better than the 2^-12 floor. Both failing constraints have the same root cause: iterative (best 15.4 MSPS) and unrolled_k (best 21.1 MSPS, even at k=4-8) emit one result every several cycles, so their Fmax x results/cycle ceiling sits well under the 32 requests/us the control tick demands, and the 32-request burst then needs 1.51 us or more to drain versus the 0.44 us p99 batch budget. I am NOT declaring infeasible, because the registry still contains the 1-result/cycle families pipelined and pipelined_m: a pipelined_m design (e.g. m around 8, N around 12, latency ceil(N/m)+2 cycles) at a few tens of MHz would give throughput = Fmax x 1 >= 32 MSPS and drain a 32-request burst in roughly 32 + latency cycles, inside 0.44 us, so feasibility is plausible and unproven either way. Those families were never evaluated (only iterative and unrolled_k were), so the correct honest outcome at the round cap is to stop with an empty front rather than label the spec infeasible on evidence we do not have; the recorded gap is the unexplored 1-result/cycle region, which is where any future run on this spec should start.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 21.1
- max_abs_err <= 0.000244141: 72% violate; best seen 5.51e-08 (2^-24.11)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 1.51

No feasible design found yet. Least-violating designs:
- iterative [data_width=18 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=13.2, max_abs_err=0.000575 (2^-10.76); throughput_msps >= 32 violated by 58.7%; max_abs_err <= 0.000244141 violated by 135.7%; sys_p99_batch_us <= 0.44 violated by 449.0%
- unrolled_k [data_width=15 n_iter=15 angle_guard=2 frac_guard=2 rounding=round k=4]: throughput=10.3, max_abs_err=0.000271 (2^-11.85); throughput_msps >= 32 violated by 67.8%; max_abs_err <= 0.000244141 violated by 11.2%; sys_p99_batch_us <= 0.44 violated by 602.5%
- unrolled_k [data_width=20 n_iter=12 angle_guard=1 frac_guard=1 rounding=round k=4]: throughput=11.6, max_abs_err=0.000494 (2^-10.98); throughput_msps >= 32 violated by 63.7%; max_abs_err <= 0.000244141 violated by 102.2%; sys_p99_batch_us <= 0.44 violated by 522.0%
- unrolled_k [data_width=20 n_iter=12 angle_guard=0 frac_guard=0 rounding=round k=4]: throughput=11.6, max_abs_err=0.000497 (2^-10.98); throughput_msps >= 32 violated by 63.7%; max_abs_err <= 0.000244141 violated by 103.5%; sys_p99_batch_us <= 0.44 violated by 522.0%
- unrolled_k [data_width=19 n_iter=12 angle_guard=2 frac_guard=1 rounding=round k=4]: throughput=11.6, max_abs_err=0.000498 (2^-10.97); throughput_msps >= 32 violated by 63.7%; max_abs_err <= 0.000244141 violated by 104.1%; sys_p99_batch_us <= 0.44 violated by 522.0%

Per family:
- iterative: 25 evals, 0 feasible; max throughput seen 15.4 MSPS; best accuracy 19.70 bits
- unrolled_k: 75 evals, 0 feasible; max throughput seen 21.1 MSPS; best accuracy 24.11 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7735 in, 11156 out
- provider-reported cost: $0.0115
- full prompts and replies: `llm_trace.jsonl`

