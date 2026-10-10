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
- `max_abs_err <= 0.000244141`: met by 114/200 evaluations; best value seen 1.28e-07 (2^-22.89)
- best throughput seen 291.5 MSPS (estimate); best accuracy 22.89 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The 400 MSPS single-lane constraint rules out iterative and unrolled_k (their multi-cycle-per-result schedules would need Fmax far above what Artix-7 can deliver). Only pipelined and pipelined_m produce one result per cycle, so throughput equals Fmax and the search must focus there. Accuracy (max_abs_err <= 2^-12) requires roughly W>=14 and N>=14, so the ranges are centred on that boundary (W 12..20, N 12..22) with small guard-bit ranges, letting the optimiser find the minimum-LUT design that still meets both constraints. Round 1 spends most budget on the m=1 pipelined family (best Fmax) and the rest on pipelined_m with small m to map the area/throughput trade-off.*)
- `pipelined` (60 evals): data_width=12..20, n_iter=12..22, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* Only a fully pipelined (1 result/cycle) datapath can plausibly reach 400 MSPS single-lane; m=1 gives the shortest per-stage logic and thus the highest Fmax. Ranges bracket the accuracy boundary (W>=14, N>=14 for 2^-12) so the search can find the minimum-LUT feasible point.
- `pipelined_m` (40 evals): data_width=12..20, n_iter=12..22, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, m=2..4. *Why:* Still 1 result/cycle, but registering every m stages trades Fmax for fewer FFs; m=2..4 keeps the combinational path short enough that 400 MSPS may remain reachable while potentially reducing area. Included to cover the area/throughput trade-off on the front.

**Result (code):** 100 evaluations this round, 100 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — Throughput is the binding constraint: every one of the 100 evaluations violates throughput>=400, best seen 282 MSPS, while accuracy is already comfortable (best 16.38 bits vs the 12 needed, and 66% of designs meet the error bound). Both explored families are 1-result/cycle, so pipelined would need Fmax to jump from 282 to 400 MHz (+42%), which the cost model gives no evidence for. The unexplored unrolled_k family computes k micro-rotations/cycle at k/(ceil(N/k)+3) results/cycle, i.e. up to 2 results/cycle at k=8,N=8, so 400 MSPS becomes reachable at only ~200 MHz. That is the most likely route to feasibility, so I bring it in and keep a small pipelined probe at small data_width to test whether Fmax can be pushed.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 282
- max_abs_err <= 0.000244141: 34% violate; best seen 1.17e-05 (2^-16.38)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc]: throughput=264, max_abs_err=3.04e-05 (2^-15.00); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=18 n_iter=22 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=264, max_abs_err=0.000121 (2^-13.02); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=19 n_iter=16 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=264, max_abs_err=6.89e-05 (2^-13.83); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=19 n_iter=15 angle_guard=-1 frac_guard=3 rounding=round]: throughput=264, max_abs_err=0.000119 (2^-13.03); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=19 n_iter=17 angle_guard=2 frac_guard=0 rounding=round]: throughput=264, max_abs_err=4.23e-05 (2^-14.53); throughput_msps >= 400 violated by 33.9%

Per family:
- pipelined: 60 evals, 0 feasible; max throughput seen 282 MSPS; best accuracy 16.38 bits
- pipelined_m: 40 evals, 0 feasible; max throughput seen 178 MSPS; best accuracy 16.38 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Add unrolled_k (k up to 8) as the primary feasibility route since it multiplies results/cycle, and keep a narrow small-width pipelined probe to check the Fmax ceiling.*)
- `unrolled_k` (75 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=4..8. *Why:* High k gives >1 result/cycle (up to 2 at k=8,N=8), the only explored-family-independent way to clear 400 MSPS at a plausible Fmax; accuracy is already met so n_iter/data_width can be traded for speed.
- `pipelined` (25 evals): data_width=8..16, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Probe whether the smallest data_width lifts Fmax toward 400 MHz for the 1-result/cycle family; if it stays near 282 this family is confirmed throughput-infeasible.

**Result (code):** 100 evaluations this round, 200 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The binding constraint is throughput_msps >= 400 and it is unreachable in this registry. Throughput = Fmax x results/cycle, so only the one-result-per-cycle families (pipelined, pipelined_m) can hope to reach 400 MSPS, and their throughput equals Fmax directly. Across all 200 evaluations the highest throughput any design achieved is 292 MSPS (pipelined), i.e. 73% of the target; every one of the 200 evaluations violated the throughput constraint (100%), including the five least-violating designs NSGA-II could find, which all sit at 264 MSPS. The remaining family, unrolled_k, is capped by construction at 1/(ceil(N/k)+3) results per cycle and topped out at 25.5 MSPS, and the still-unexplored iterative family is strictly worse (1 result per N+3 cycles), so both are far below their own Fmax and cannot help. The accuracy constraint is easily met (best error 1.28e-07 = 2^-22.89, and the rough 2^-13 designs already satisfy <= 2^-12), so accuracy is not the blocker; the sole obstacle is the ~292 MHz Fmax ceiling of the 1-result/cycle pipelined families versus the required 400 MHz. With the two relevant families already heavily explored (85 + 40 evals) and their best effort a full 37% short of the target, no registry design can satisfy the spec, so declaring infeasible (rather than the least-violating 264 MSPS design) is correct.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 200 evaluations (0 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 292
- max_abs_err <= 0.000244141: 43% violate; best seen 1.28e-07 (2^-22.89)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc]: throughput=264, max_abs_err=3.04e-05 (2^-15.00); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=18 n_iter=22 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=264, max_abs_err=0.000121 (2^-13.02); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=19 n_iter=16 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=264, max_abs_err=6.89e-05 (2^-13.83); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=19 n_iter=15 angle_guard=-1 frac_guard=3 rounding=round]: throughput=264, max_abs_err=0.000119 (2^-13.03); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=19 n_iter=17 angle_guard=2 frac_guard=0 rounding=round]: throughput=264, max_abs_err=4.23e-05 (2^-14.53); throughput_msps >= 400 violated by 33.9%

Per family:
- unrolled_k: 75 evals, 0 feasible; max throughput seen 25.5 MSPS; best accuracy 22.89 bits
- pipelined: 85 evals, 0 feasible; max throughput seen 292 MSPS; best accuracy 16.38 bits
- pipelined_m: 40 evals, 0 feasible; max throughput seen 178 MSPS; best accuracy 16.38 bits
```
</details>

## LLM usage
- calls: 6 (failed/unparsed attempts: 0)
- tokens: 20662 in, 7271 out
- provider-reported cost: $0.0063
- full prompts and replies: `llm_trace.jsonl`

