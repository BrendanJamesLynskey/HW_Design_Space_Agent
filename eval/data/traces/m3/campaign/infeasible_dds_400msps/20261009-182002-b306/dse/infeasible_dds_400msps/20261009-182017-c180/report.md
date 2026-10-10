# DSE run: infeasible_dds_400msps

**Verdict:** INFEASIBLE: the architect concluded no design in the registry meets the spec.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 200 of 400 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec infeasible_dds_400msps: Wideband DDS needing >= 400 MSPS single-lane sin/cos with max error <= 2^-12. Minimise LUTs.
  constraint: throughput_msps >= 400
  constraint: max_abs_err <= 0.000244141
  objective: min luts (HV ref 4000)
  objective: max accuracy_bits (HV ref 12)
  select: min luts
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
None: no evaluated design satisfies every constraint.

- `throughput_msps >= 400`: met by 0/200 evaluations; best value seen 292
- `max_abs_err <= 0.000244141`: met by 56/200 evaluations; best value seen 1.3e-05 (2^-16.24)
- best throughput seen 291.5 MSPS (estimate); best accuracy 16.24 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The 400 MSPS single-lane constraint rules out iterative (N+3 cycles/result) and unrolled_k (ceil(N/k)+3 >= 4 cycles/result), which would need Fmax >= 1600 MHz on Artix-7. Only pipelined and pipelined_m produce one result per cycle, so the first round concentrates on those two families. Ranges for data_width and n_iter bracket the 2^-12 error limit (output LSB 2^-(W-2) and CORDIC angle error ~2^-N), while angle_guard/frac_guard/rounding let the search trade extra internal bits for accuracy without inflating the output width. The budget is split toward fully pipelined because it has the best chance of meeting the throughput constraint; pipelined_m gets a smaller share to test whether fewer pipeline registers lower LUTs while still hitting 400 MSPS.*)
- `pipelined` (65 evals): data_width=12..20, n_iter=10..20, angle_guard=0..4, frac_guard=0..4, rounding=trunc|round. *Why:* One registered stage per micro-rotation gives the shortest combinational path and therefore the highest Fmax, the only realistic way to reach 400 MSPS single-lane. Widths and iteration counts span the 12-bit accuracy threshold so the search can find the minimum-LUT feasible corner.
- `pipelined_m` (35 evals): data_width=12..20, n_iter=10..20, angle_guard=0..4, frac_guard=0..4, rounding=trunc|round, m=2..3. *Why:* Still 1 result/cycle, but registering every 2-3 stages cuts pipeline FF count and may reduce the area proxy; m is kept small because larger m lengthens the combinational path and risks dropping below 400 MSPS. Check whether it yields lower LUTs than fully pipelined at the same accuracy.

**Result (code):** 100 evaluations this round, 100 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `refine` — Only pipelined can plausibly reach 400 MSPS: it emits 1 result/cycle, so throughput = Fmax, whereas unrolled_k needs Fmax >= 400*(ceil(N/k)+3) >= 1600 and iterative needs Fmax >= 400*(N+3) >= 2800 (both impossible), and pipelined_m's longer critical path already caps at 171 MSPS. The accuracy bound is already satisfiable at W=16 (2^-12.47), but that same design only reaches 282 MSPS. Since Fmax rises as data_width falls, the whole feasibility question is whether some width gives Fmax >= 400 while still holding max_abs_err <= 2^-12 (which needs W >= ~14). Round 1 never probed small widths, so I will map the pipelined throughput ceiling vs. width before judging feasibility.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 282
- max_abs_err <= 0.000244141: 47% violate; best seen 1.3e-05 (2^-16.24)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=16 n_iter=16 angle_guard=2 frac_guard=1 rounding=round]: throughput=273, max_abs_err=0.000177 (2^-12.47); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=16 n_iter=17 angle_guard=2 frac_guard=1 rounding=round]: throughput=273, max_abs_err=0.000177 (2^-12.47); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round]: throughput=273, max_abs_err=0.000176 (2^-12.48); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=20 angle_guard=2 frac_guard=2 rounding=round]: throughput=264, max_abs_err=3.99e-05 (2^-14.61); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=19 n_iter=16 angle_guard=0 frac_guard=1 rounding=round]: throughput=264, max_abs_err=7.36e-05 (2^-13.73); throughput_msps >= 400 violated by 33.9%

Per family:
- pipelined: 65 evals, 0 feasible; max throughput seen 282 MSPS; best accuracy 15.60 bits
- pipelined_m: 35 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 16.24 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Focus the whole round on pipelined at small data_width (8..16) with n_iter 8..24 and full guard/rounding ranges. If the max Fmax over this box stays below 400 at every width that still meets 2^-12, no registry family can satisfy the spec and the next decision is infeasible; if a width near 14-16 reaches 400, we refine around it.*)
- `pipelined` (100 evals): data_width=8..16, n_iter=8..24, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Pipelined is the throughput ceiling family (1 result/cycle, throughput=Fmax); sweeping data_width down to 8 exposes the max achievable Fmax and the width at which accuracy crosses 2^-12, which decides feasibility.

**Result (code):** 100 evaluations this round, 200 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The throughput constraint is unreachable. Only pipelined and pipelined_m yield 1 result/cycle; iterative (N+3 cycles/result) and unrolled_k (ceil(N/k)+3 cycles/result) are strictly slower per result, so the two unexplored families cannot help. Across 165 pipelined evals the best throughput is 292 MSPS (27% below the required 400), and pipelined_m tops out at 171 MSPS. The throughput-max designs sit at data_width=16, while the accuracy constraint (max_abs_err <= 2^-12) forces data_width >= ~15 (the only designs meeting it are W=15-18, e.g. W=15 gives 2^-12.04); shrinking W to raise Fmax would push the output LSB 2^-(W-2) above the 2^-12 error budget, so accuracy and throughput cannot be satisfied simultaneously. With 0/200 feasible and the binding constraint missed by ~32% at the best point, no registry design meets the spec.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 200 evaluations (0 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 292
- max_abs_err <= 0.000244141: 72% violate; best seen 1.3e-05 (2^-16.24)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=16 n_iter=16 angle_guard=2 frac_guard=1 rounding=round]: throughput=273, max_abs_err=0.000177 (2^-12.47); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=16 n_iter=17 angle_guard=2 frac_guard=1 rounding=round]: throughput=273, max_abs_err=0.000177 (2^-12.47); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round]: throughput=273, max_abs_err=0.000176 (2^-12.48); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=15 n_iter=21 angle_guard=2 frac_guard=3 rounding=round]: throughput=273, max_abs_err=0.000237 (2^-12.04); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=20 angle_guard=2 frac_guard=2 rounding=round]: throughput=264, max_abs_err=3.99e-05 (2^-14.61); throughput_msps >= 400 violated by 33.9%

Per family:
- pipelined: 165 evals, 0 feasible; max throughput seen 292 MSPS; best accuracy 15.60 bits
- pipelined_m: 35 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 16.24 bits
```
</details>

## LLM usage
- calls: 6 (failed/unparsed attempts: 0)
- tokens: 21558 in, 13572 out
- provider-reported cost: $0.0118
- full prompts and replies: `llm_trace.jsonl`

