# DSE run: asic_power_50msps

**Verdict:** NO FEASIBLE DESIGN FOUND within the budget (the architect did not declare infeasibility).  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_power_50msps: A 50 MSPS sin/cos unit in sky130 standard cells for a battery-powered radio: max error <= 2^-12. Minimise the relative power index; accuracy is the trade-off.
  target: asic-sky130hd
  constraint: throughput_msps >= 50
  constraint: max_abs_err <= 0.000244141
  objective: min power_index (HV ref 40)
  objective: max accuracy_bits (HV ref 12)
  select: min power_index
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
None: no evaluated design satisfies every constraint.

- `throughput_msps >= 50`: met by 0/100 evaluations; best value seen 16.4
- `max_abs_err <= 0.000244141`: met by 60/100 evaluations; best value seen 1.41e-07 (2^-22.76)
- best throughput seen 16.4 MSPS (estimate); best accuracy 22.76 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The 50 MSPS throughput constraint is binding for our families. iterative needs Fmax >= 50*(N+3); with N>=12 for the 2^-12 accuracy constraint this requires >750 MHz, implausible for a shared barrel-shifter datapath in sky130. unrolled_k is the only plausible family: it trades k parallel micro-rotations against cycles/result = ceil(N/k)+3. We allocate most of the budget to unrolled_k, with a small iterative share to document infeasibility. Accuracy needs N>=12 and W>=14; we search around these minima to find the lowest-power feasible designs. This round uses 60 evals (51 unrolled_k, 9 iterative), reserving 40 for refinement and final front mapping.*)
- `unrolled_k` (51 evals): data_width=14..20, n_iter=12..24, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* Only family that can plausibly reach 50 MSPS. k=2..8 covers the Fmax vs cycles/result trade-off; N=12..24 covers accuracy vs cycles; W=14..20 covers output quantization vs area; guards and rounding let Optuna find the minimum-power point that still meets max_abs_err <= 2^-12.
- `iterative` (9 evals): data_width=14..20, n_iter=12..24, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Included only to confirm infeasibility: with N>=12 for accuracy, throughput requires Fmax >= 50*(N+3) >= 750 MHz, unrealistic for a shared barrel-shifter datapath in sky130. A small budget documents this and may catch any unexpected cost-model result.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — No feasible design exists in the two multi-cycle families for a structural reason, not a tuning reason: throughput_msps is Fmax/(cycles per result), and iterative (N+3) and unrolled_k (ceil(N/k)+3) pay 4-33 cycles per result, giving the observed ceiling of 7.78 MSPS. The throughput constraint therefore cannot be met by narrowing ranges. The unexplored reference families pipelined and pipelined_m return one result per clock, so 50 MSPS needs only Fmax >= 50 MHz, and their accuracy at the same data_width/n_iter/angle_guard/frac_guard is bit-identical to what round 1 already proved can hit <= 2^-12 (best seen 2^-17.10). Spending the remaining 40 evaluations on these two families is the only path to a feasible front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 7.78
- max_abs_err <= 0.000244141: 37% violate; best seen 7.14e-06 (2^-17.10)

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=15 n_iter=17 angle_guard=4 frac_guard=4 rounding=round k=2]: throughput=5.72, max_abs_err=0.000111 (2^-13.13); throughput_msps >= 50 violated by 88.6%
- unrolled_k [data_width=15 n_iter=18 angle_guard=3 frac_guard=4 rounding=trunc k=2]: throughput=5.72, max_abs_err=0.000207 (2^-12.24); throughput_msps >= 50 violated by 88.6%
- unrolled_k [data_width=15 n_iter=18 angle_guard=4 frac_guard=4 rounding=round k=2]: throughput=5.72, max_abs_err=0.000114 (2^-13.10); throughput_msps >= 50 violated by 88.6%
- unrolled_k [data_width=15 n_iter=17 angle_guard=3 frac_guard=4 rounding=trunc k=2]: throughput=5.72, max_abs_err=0.000235 (2^-12.05); throughput_msps >= 50 violated by 88.6%
- unrolled_k [data_width=18 n_iter=15 angle_guard=-1 frac_guard=4 rounding=round k=2]: throughput=5.58, max_abs_err=0.00019 (2^-12.36); throughput_msps >= 50 violated by 88.8%

Per family:
- iterative: 9 evals, 0 feasible; max throughput seen 6.64 MSPS; best accuracy 16.71 bits
- unrolled_k: 51 evals, 0 feasible; max throughput seen 7.78 MSPS; best accuracy 17.10 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Every 60 evaluations of iterative/unrolled_k is throughput-limited by their schedule: iterative costs N+3 cycles/result and unrolled_k ceil(N/k)+3, so against the observed best 7.78 MSPS (implying Fmax ~ 90-100 MHz, since 12 cycles x ~90 MHz = 7.78) even the best case k=8, N=4 would need ~200 MHz and N=4 cannot reach 2^-12. The 88.6% throughput shortfall on all five least-violating designs confirms the multiplier, not the clock, is the binding term. pipelined/pipelined_m produce 1 result/cycle, so the 50 MSPS floor collapses to just Fmax >= 50 MHz, which the cost model should clear easily. Accuracy is family-independent, and round 1 already showed max_abs_err <= 2^-12 is reachable at data_width=15, n_iter=17-18, angle_guard >= 3, frac_guard=4, rounding=round (best 2^-17.10), so the accuracy ranges above are anchored on that proven corner and extended downward in W/N to expose the low-power end of the front. Remaining budget: 40 evals for round 2.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — Budget is exhausted (100/100 evals, round 2 of 4, final round). No feasible design was found: every one of the 100 evaluations violates throughput_msps >= 50, with the best seen only 16.4 MSPS (iterative) and 10.1 MSPS (unrolled_k), and 0/100 designs are feasible. However, I cannot declare `infeasible`: the two families actually explored (iterative, unrolled_k) are both multi-cycle-per-result architectures whose throughput is structurally capped well below 50 MSPS, whereas the registry's pipelined / pipelined_m families produce 1 result/cycle and were never evaluated — they are the plausible route to 50 MSPS. With no evaluations of those families and no remaining budget, infeasibility is unproven, so the honest terminal decision is `stop` (budget/round cap reached) rather than `infeasible`. Note the accuracy side is already comfortably satisfiable (best max_abs_err 1.41e-07 = 2^-22.76, far under the 2^-12 limit), so the binding constraint is purely throughput, and it is a family-selection problem that this run did not get to test.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 16.4
- max_abs_err <= 0.000244141: 40% violate; best seen 1.41e-07 (2^-22.76)

No feasible design found yet. Least-violating designs:
- iterative [data_width=18 n_iter=19 angle_guard=0 frac_guard=0 rounding=round]: throughput=5.95, max_abs_err=0.000114 (2^-13.10); throughput_msps >= 50 violated by 88.1%
- unrolled_k [data_width=15 n_iter=17 angle_guard=4 frac_guard=4 rounding=round k=2]: throughput=5.72, max_abs_err=0.000111 (2^-13.13); throughput_msps >= 50 violated by 88.6%
- unrolled_k [data_width=15 n_iter=18 angle_guard=3 frac_guard=4 rounding=trunc k=2]: throughput=5.72, max_abs_err=0.000207 (2^-12.24); throughput_msps >= 50 violated by 88.6%
- unrolled_k [data_width=15 n_iter=18 angle_guard=4 frac_guard=4 rounding=round k=2]: throughput=5.72, max_abs_err=0.000114 (2^-13.10); throughput_msps >= 50 violated by 88.6%
- unrolled_k [data_width=15 n_iter=17 angle_guard=3 frac_guard=4 rounding=trunc k=2]: throughput=5.72, max_abs_err=0.000235 (2^-12.05); throughput_msps >= 50 violated by 88.6%

Per family:
- iterative: 29 evals, 0 feasible; max throughput seen 16.4 MSPS; best accuracy 22.76 bits
- unrolled_k: 71 evals, 0 feasible; max throughput seen 10.1 MSPS; best accuracy 20.61 bits
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 1)
- tokens: 5979 in, 10844 out
- provider-reported cost: $0.0119
- full prompts and replies: `llm_trace.jsonl`

