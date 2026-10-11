# DSE run: asic_multiaxis_control

**Verdict:** NO FEASIBLE DESIGN FOUND within the budget (the architect did not declare infeasibility).  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 19.7
- `max_abs_err <= 0.000244141`: met by 39/100 evaluations; best value seen 1.15e-06 (2^-19.73)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 1.62
- best throughput seen 19.7 MSPS (estimate); best accuracy 19.73 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraint is the system burst: 32 simultaneous requests per 1 us tick, all back within 0.5 us (sys_p99_batch_us <= 0.5). For a multi-cycle unit this is 32*c/Fmax <= 0.5 us where c is cycles/result, so c/Fmax <= 15.6 ns. Accuracy (max_abs_err <= 2^-12, i.e. accuracy_bits >= 12) pins N>=13 and W>=14, which sets c>=N+3=16 for iterative (needs >1 GHz, implausible) and c=ceil(N/k)+3>=5 for unrolled_k at k=8 (needs ~320 MHz, the only credible corner). I therefore put 80% of the budget on unrolled_k with k spanning 4..8 (the speed/area trade-off) and W/N/guards just above the accuracy floor (area is the objective), and 20% on iterative to confirm/deny its feasibility. Both objectives (min area_um2, max accuracy_bits) are covered: the front should run from the smallest W/N/guards/k that still clears 2^-12 up to higher-accuracy, higher-area points. I will re-aim ranges in later rounds from the returned numbers (e.g. widen k or N if the feasible corner sits at a range edge, or drop iterative if it returns nothing feasible).*)
- `unrolled_k` (48 evals): data_width=14..18, n_iter=12..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, k=4..8. *Why:* Only plausible multi-cycle route to the batch constraint. A tick of 32 requests must finish in 0.5 us, so 32*(ceil(N/k)+3)/Fmax <= 0.5 us. Accuracy (max_abs_err <= 2^-12) forces N>=13 (residual angle ~2^-(N-1)) and W>=14 (output LSB 2^-(W-2)=2^-12 at W=14), so c=ceil(N/k)+3 is at best 5 (N=14,k=8), needing Fmax>=320 MHz; smaller k needs even higher Fmax. k is therefore the speed knob and also the area knob (k chained micro-rotations), which is exactly the trade-off to map. W/N/guards are kept just above the accuracy floor (14..18, 12..20, 0..3) because area is the objective and larger values only buy accuracy_bits beyond 12.
- `iterative` (12 evals): data_width=14..18, n_iter=12..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* Small share to document the boundary rather than to find a winner. iterative needs c=N+3 cycles/result, so the batch constraint becomes 32*(N+3)/Fmax <= 0.5 us, i.e. Fmax >= 64*(N+3) MHz. With the accuracy floor N>=13 that is Fmax >= 1024 MHz, which is not credible in sky130_fd_sc_hd; even N=4 would need 448 MHz. I keep the accuracy-feasible range (W 14..18, N 12..20) so code can confirm no iterative point satisfies both max_abs_err<=2^-12 and sys_p99_batch_us<=0.5, and so any surprising fast corner is not missed.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The binding constraints are throughput_msps >= 32 and sys_p99_batch_us <= 0.5, and neither can be reached by the two families tried. iterative and unrolled_k emit one result every several cycles, so their throughput is capped far below 32 MSPS (best seen 8.73 and 5.84 MSPS), and the 32-request burst needs ~64 MSPS of burst rate to clear in 0.5 us — 100% of evaluations violate both, with sys_p99_batch_us best 3.66 us (7x over). Accuracy is not the blocker: iterative already reached 14.37 bits (2^-14.37), well past the 2^-12 requirement, so the fix is architectural, not precision. Only pipelined / pipelined_m emit 1 result/cycle, making throughput = Fmax (easily > 32 MHz) and letting a 32-deep burst drain in ~32 cycles + latency. These families have not been evaluated at all, so the current front is not evidence of infeasibility.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 8.73
- max_abs_err <= 0.000244141: 62% violate; best seen 4.73e-05 (2^-14.37)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 3.66

No feasible design found yet. Least-violating designs:
- iterative [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round]: throughput=7.7, max_abs_err=0.000204 (2^-12.26); throughput_msps >= 32 violated by 75.9%; sys_p99_batch_us <= 0.5 violated by 729.4%
- iterative [data_width=16 n_iter=12 angle_guard=2 frac_guard=2 rounding=round]: throughput=8.73, max_abs_err=0.000548 (2^-10.83); throughput_msps >= 32 violated by 72.7%; max_abs_err <= 0.000244141 violated by 124.4%; sys_p99_batch_us <= 0.5 violated by 631.7%
- iterative [data_width=17 n_iter=12 angle_guard=1 frac_guard=0 rounding=round]: throughput=8.73, max_abs_err=0.000568 (2^-10.78); throughput_msps >= 32 violated by 72.7%; max_abs_err <= 0.000244141 violated by 132.6%; sys_p99_batch_us <= 0.5 violated by 631.7%
- iterative [data_width=15 n_iter=16 angle_guard=3 frac_guard=3 rounding=round]: throughput=6.89, max_abs_err=0.000158 (2^-12.63); throughput_msps >= 32 violated by 78.5%; sys_p99_batch_us <= 0.5 violated by 827.2%
- iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 rounding=round]: throughput=8.32, max_abs_err=0.000714 (2^-10.45); throughput_msps >= 32 violated by 74.0%; max_abs_err <= 0.000244141 violated by 192.3%; sys_p99_batch_us <= 0.5 violated by 667.4%

Per family:
- iterative: 12 evals, 0 feasible; max throughput seen 8.73 MSPS; best accuracy 14.37 bits
- unrolled_k: 48 evals, 0 feasible; max throughput seen 5.84 MSPS; best accuracy 14.28 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Spend the remaining ~40 evals on the only families that can satisfy the throughput/burst constraints, keeping W/N ranges that already proved accurate enough. If pipelined/pipelined_m also fail the L1 batch bound, that is the point to declare infeasible.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — Budget is exhausted (100/100 evals, round 2 of 4) and the feasible front is empty: 0/100 designs feasible, hypervolume 0, no gain this round. Accuracy is not the binding constraint — the best design already reaches 2^-19.73, far better than the required 2^-12 — while the two explored families fail the throughput and burst constraints by wide margins: best throughput_msps seen is 19.7 (iterative) and 9.94 (unrolled_k) against the required 32, and best sys_p99_batch_us is 1.62 against the required 0.5 (100% violation on both). Both explored families emit only one result every N+3 or ceil(N/k)+3 cycles, so they structurally cannot serve a 32-request burst inside 0.5 us. I deliberately do NOT declare `infeasible`: the registry's pipelined and pipelined_m families (1 result/cycle) were never evaluated, and they are the only families whose schedule could plausibly reach 32 MSPS and drain a 32-request burst within 0.5 us, so impossibility is not established by the evidence. With no budget left to test them, the honest verdict is to stop with an empty front rather than assert infeasibility or settle for a design that violates the constraints.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 19.7
- max_abs_err <= 0.000244141: 61% violate; best seen 1.15e-06 (2^-19.73)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 1.62

No feasible design found yet. Least-violating designs:
- iterative [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round]: throughput=7.7, max_abs_err=0.000204 (2^-12.26); throughput_msps >= 32 violated by 75.9%; sys_p99_batch_us <= 0.5 violated by 729.4%
- iterative [data_width=16 n_iter=12 angle_guard=2 frac_guard=2 rounding=round]: throughput=8.73, max_abs_err=0.000548 (2^-10.83); throughput_msps >= 32 violated by 72.7%; max_abs_err <= 0.000244141 violated by 124.4%; sys_p99_batch_us <= 0.5 violated by 631.7%
- iterative [data_width=17 n_iter=12 angle_guard=1 frac_guard=0 rounding=round]: throughput=8.73, max_abs_err=0.000568 (2^-10.78); throughput_msps >= 32 violated by 72.7%; max_abs_err <= 0.000244141 violated by 132.6%; sys_p99_batch_us <= 0.5 violated by 631.7%
- iterative [data_width=20 n_iter=12 angle_guard=0 frac_guard=0 rounding=round]: throughput=8.12, max_abs_err=0.000497 (2^-10.98); throughput_msps >= 32 violated by 74.6%; max_abs_err <= 0.000244141 violated by 103.5%; sys_p99_batch_us <= 0.5 violated by 686.4%
- iterative [data_width=15 n_iter=16 angle_guard=3 frac_guard=3 rounding=round]: throughput=6.89, max_abs_err=0.000158 (2^-12.63); throughput_msps >= 32 violated by 78.5%; sys_p99_batch_us <= 0.5 violated by 827.2%

Per family:
- iterative: 32 evals, 0 feasible; max throughput seen 19.7 MSPS; best accuracy 19.73 bits
- unrolled_k: 68 evals, 0 feasible; max throughput seen 9.94 MSPS; best accuracy 18.96 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8662 in, 12611 out
- provider-reported cost: $0.0150
- full prompts and replies: `llm_trace.jsonl`

