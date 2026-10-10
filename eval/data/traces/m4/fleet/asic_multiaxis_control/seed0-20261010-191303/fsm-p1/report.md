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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 12.8
- `max_abs_err <= 0.000244141`: met by 31/100 evaluations; best value seen 5.51e-08 (2^-24.11)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 2.49
- best throughput seen 12.8 MSPS (estimate); best accuracy 24.11 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec's hard constraints are max_abs_err <= 2^-12 and sys_p99_batch_us <= 0.5 for 32 requests arriving together every 1us. The batch constraint is the real driver: 32 results in 0.5us means >=64 results/us, double the nominal throughput_msps>=32, and it is what separates the two families I own. Accuracy pins the search space: output LSB is 2^-(W-2), so W>=14 is needed for 2^-12 (W=14 only with round rounding), and the CORDIC angle residual needs N>=13. Those accuracy-required N values are exactly what makes the iterative family's N+3 cycles/result expensive against the burst bound, whereas unrolled_k can trade k against Fmax. I therefore put 80% of the budget on unrolled_k, concentrated on the k=4..8 / N=12..20 boundary where the feasible min-area design (the selection rule is min area_um2) will sit, and 20% on iterative to verify infeasibility or catch a surprise. Both families share identical accuracy parameters, so any feasible points merge onto one front.*)
- `unrolled_k` (48 evals): data_width=14..18, n_iter=12..20, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, k=4..8. *Why:* This is the only family I hold that can plausibly satisfy the burst constraint. The real binding constraint is sys_p99_batch_us <= 0.5 with 32 simultaneous requests, i.e. an effective >=64 results/us, twice the nominal 32 Msps. unrolled_k gives ceil(N/k)+3 cycles/result, so with the accuracy-required N>=13 a k>=4 keeps the required Fmax in a range sky130 can plausibly reach, while k=8 minimises cycles at the cost of a longer combinational chain and more area. I sweep k=4..8 to expose exactly where the Fmax/area/cycles trade-off crosses the 0.5us batch bound, and N=12..20 to find the smallest N that still meets max_abs_err<=2^-12. data_width starts at 14 because the output LSB is 2^-(W-2): W=14 with round rounding gives half-LSB 2^-13 < 2^-12, so W<14 cannot meet the error bound. angle_guard/frac_guard are swept to buy internal precision cheaply before paying for extra output width, and rounding is swept because round vs trunc is the difference between W=14 passing or failing.
- `iterative` (12 evals): data_width=14..18, n_iter=12..20, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* Smallest-area family, so it would win the min-area selection if it were feasible, and it is worth a small share to confirm or refute that rather than assume it. It needs N+3 cycles/result, so the 64 results/us burst requirement forces Fmax >= 64*(N+3); with the N>=13 that accuracy demands that is ~1 GHz, which I expect to be out of reach, but the cost model must tell me that, not me. I keep the same accuracy-relevant ranges as unrolled_k (W>=14 for the 2^-12 output-LSB bound, N=12..20, guards, rounding) so that if any iterative point does clear the batch bound it lands on the same accuracy axis and merges cleanly into the front.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — Every evaluation so far violates throughput_msps>=32 (best 9.43) and sys_p99_batch_us<=0.5 (best 3.38, i.e. ~7x over). This is structural, not a tuning problem: the system scenario issues 32 requests at one tick and needs all 32 back within 0.5 us, i.e. a burst rate of ~64 MSPS. Both explored families are multi-cycle-per-result by construction (iterative: N+3 cycles/result; unrolled_k: ceil(N/k)+3 cycles/result), so their throughput is Fmax/(cycles per result) and the observed ceiling of 9.43 MSPS is exactly that wall. No amount of narrowing data_width/n_iter/guard tuning can move a 1-result-per-N-cycles datapath to 64 MSPS. The registry's pipelined and pipelined_m families emit 1 result/cycle, so at any plausible Fmax they clear both the 32 MSPS average and the 32-results-in-0.5us burst bound. Accuracy is family-independent (identical bit-accurate datapath), so the accuracy constraint (best seen 13.90 bits, need >=12) is already satisfiable and will carry over. The remaining budget (40 evals) should go to the two unexplored 1-result/cycle families.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 9.43
- max_abs_err <= 0.000244141: 68% violate; best seen 6.55e-05 (2^-13.90)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 3.38

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=round]: throughput=8.18, max_abs_err=0.00031 (2^-11.65); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 27.0%; sys_p99_batch_us <= 0.5 violated by 680.5%
- iterative [data_width=17 n_iter=14 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=8, max_abs_err=0.000338 (2^-11.53); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 38.4%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=18 n_iter=14 angle_guard=1 frac_guard=2 rounding=round]: throughput=7.17, max_abs_err=0.000157 (2^-12.64); throughput_msps >= 32 violated by 77.6%; sys_p99_batch_us <= 0.5 violated by 791.4%
- iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 rounding=round]: throughput=8.32, max_abs_err=0.000714 (2^-10.45); throughput_msps >= 32 violated by 74.0%; max_abs_err <= 0.000244141 violated by 192.3%; sys_p99_batch_us <= 0.5 violated by 667.4%
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=trunc]: throughput=7.7, max_abs_err=0.000643 (2^-10.60); throughput_msps >= 32 violated by 75.9%; max_abs_err <= 0.000244141 violated by 163.4%; sys_p99_batch_us <= 0.5 violated by 729.4%

Per family:
- iterative: 12 evals, 0 feasible; max throughput seen 9.43 MSPS; best accuracy 13.90 bits
- unrolled_k: 48 evals, 0 feasible; max throughput seen 5.51 MSPS; best accuracy 13.83 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Both families are 1-result/cycle, so the throughput and sys_p99_batch constraints become reachable for the first time; the search then reduces to minimising area subject to max_abs_err<=2^-12, which the bit-accurate model already shows is achievable at W~14-16, N~12-14. Ranges are kept narrow and low-width because area is the objective and the accuracy headroom is already demonstrated.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — Round cap and budget (100/100 evals) are reached, so this is the final verdict. The evidence does not prove infeasibility: only the two multi-cycle families were evaluated (iterative: 32 evals, max 11.5 MSPS; unrolled_k: 68 evals, max 12.8 MSPS), and both are structurally incapable of the required rate — the spec needs 32 results/us on average and 32 results within 0.5 us of each tick, i.e. an effective 64 MSPS, which only a 1-result/cycle family (pipelined / pipelined_m) can deliver. Those families were never evaluated, so I cannot assert that no registry design meets the constraints; equally, no evaluated design comes close (best throughput 12.8 vs 32 MSPS, best sys_p99_batch_us 2.49 us vs 0.5 us, both 100% violating). Accuracy is not the blocker (best 2^-24.11, far better than the 2^-12 requirement), so the binding constraints are throughput and batch latency. With no budget left to test the pipelined families, I stop rather than declare infeasible on incomplete evidence; the front found so far (HV 0, 0 feasible) is not usable for selection.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 12.8
- max_abs_err <= 0.000244141: 69% violate; best seen 5.51e-08 (2^-24.11)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.49

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=round]: throughput=8.18, max_abs_err=0.00031 (2^-11.65); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 27.0%; sys_p99_batch_us <= 0.5 violated by 680.5%
- iterative [data_width=17 n_iter=14 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=8, max_abs_err=0.000338 (2^-11.53); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 38.4%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=18 n_iter=14 angle_guard=1 frac_guard=2 rounding=round]: throughput=7.17, max_abs_err=0.000157 (2^-12.64); throughput_msps >= 32 violated by 77.6%; sys_p99_batch_us <= 0.5 violated by 791.4%
- iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 rounding=round]: throughput=8.32, max_abs_err=0.000714 (2^-10.45); throughput_msps >= 32 violated by 74.0%; max_abs_err <= 0.000244141 violated by 192.3%; sys_p99_batch_us <= 0.5 violated by 667.4%
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=trunc]: throughput=7.7, max_abs_err=0.000643 (2^-10.60); throughput_msps >= 32 violated by 75.9%; max_abs_err <= 0.000244141 violated by 163.4%; sys_p99_batch_us <= 0.5 violated by 729.4%

Per family:
- iterative: 32 evals, 0 feasible; max throughput seen 11.5 MSPS; best accuracy 19.70 bits
- unrolled_k: 68 evals, 0 feasible; max throughput seen 12.8 MSPS; best accuracy 24.11 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8698 in, 6979 out
- provider-reported cost: $0.0095
- full prompts and replies: `llm_trace.jsonl`

