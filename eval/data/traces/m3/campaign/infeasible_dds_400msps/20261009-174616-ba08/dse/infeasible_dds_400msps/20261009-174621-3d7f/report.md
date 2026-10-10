# DSE run: infeasible_dds_400msps

**Verdict:** INFEASIBLE: the architect concluded no design in the registry meets the spec.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 300 of 400 budgeted, over 3 round(s).  
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

- `throughput_msps >= 400`: met by 0/300 evaluations; best value seen 292
- `max_abs_err <= 0.000244141`: met by 67/300 evaluations; best value seen 5.02e-05 (2^-14.28)
- best throughput seen 291.5 MSPS (estimate); best accuracy 14.28 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=400 MSPS single-lane. Only pipelined and pipelined_m produce 1 result/cycle. Iterative and unrolled_k produce one result every N+3 or ceil(N/k)+3 cycles; even with the smallest N and largest k they would need Fmax > 1.6 GHz, far beyond Artix-7. Therefore they are excluded from the first round. Pipelined is the primary candidate because it has the shortest critical path and thus the highest Fmax. Pipelined_m is given a small share to confirm it is dominated for this throughput target. The parameter ranges focus on the feasible accuracy/area boundary: data_width 12-18 to find the minimum width meeting 2^-12 (W>=13 likely needed), n_iter 8-20 for convergence, and small angle_guard/frac_guard/rounding options to minimise LUTs while satisfying max_abs_err <= 0.000244141.*)
- `pipelined` (80 evals): data_width=12..18, n_iter=8..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Primary family: 1 result/cycle, so throughput = Fmax. It has the shortest critical path (one micro-rotation per stage) and therefore the highest Fmax of any family. Only pipelined can plausibly reach 400 MSPS on Artix-7. Ranges bracket the minimum data_width and n_iter needed for max_abs_err <= 2^-12 while minimising LUTs: W=12-18 (W>=13 likely required with rounding), N=8-20 for convergence, and small angle_guard/frac_guard/rounding options to trade accuracy for area.
- `pipelined_m` (20 evals): data_width=12..18, n_iter=8..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Secondary check: also 1 result/cycle, but longer combinational path (m micro-rotations per cycle) so Fmax is expected to be lower than pipelined. Included with a small budget to verify it cannot beat pipelined on Fmax or LUTs, and to catch any routing-dominated corner where fewer pipeline registers might help. m is limited to 2-4 because larger m further lengthens the critical path and is even less likely to meet 400 MSPS.

**Result (code):** 100 evaluations this round, 100 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `refine` — Throughput is the binding constraint: 100% of evaluations violate >=400 MSPS, best seen only 282. Since pipelined/pipelined_m emit 1 result/cycle, throughput equals Fmax, so we must raise Fmax. All explored pipelined points sit at data_width 16-18 and cluster at ~273-282 MSPS, while accuracy has headroom (best 14.28 bits at W=16, well above the 12-bit requirement). Reducing data_width (and frac_guard) should shorten the per-stage critical path and lift Fmax, while n_iter>=~13 and rounding=round should keep max_abs_err <= 2^-12. iterative/unrolled_k cannot help because they emit one result every several cycles, so their throughput is strictly below pipelined's.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 282
- max_abs_err <= 0.000244141: 62% violate; best seen 5.02e-05 (2^-14.28)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=16 n_iter=17 angle_guard=2 frac_guard=1 rounding=round]: throughput=273, max_abs_err=0.000177 (2^-12.47); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=18 angle_guard=0 frac_guard=0 rounding=round]: throughput=273, max_abs_err=0.000114 (2^-13.10); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=18 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=273, max_abs_err=0.000182 (2^-12.43); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=19 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=273, max_abs_err=0.000197 (2^-12.31); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=18 angle_guard=0 frac_guard=1 rounding=trunc]: throughput=264, max_abs_err=0.000122 (2^-13.01); throughput_msps >= 400 violated by 33.9%

Per family:
- pipelined: 80 evals, 0 feasible; max throughput seen 282 MSPS; best accuracy 14.28 bits
- pipelined_m: 20 evals, 0 feasible; max throughput seen 178 MSPS; best accuracy 13.27 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Focus budget on the low-width pipelined region to try to break the 400 MSPS throughput wall, keeping accuracy above 12 bits via round and sufficient n_iter.*)
- `pipelined` (80 evals): data_width=8..16, n_iter=12..20, angle_guard=-2..2, frac_guard=0..2, rounding=round. *Why:* Only family that can reach 400 MSPS (1 result/cycle); sweep low data_width to raise Fmax while round+n_iter>=12 preserves >=12-bit accuracy.
- `pipelined_m` (20 evals): data_width=8..16, n_iter=12..20, angle_guard=-2..2, frac_guard=0..2, rounding=round, m=2..3. *Why:* Cheap probe: also 1 result/cycle, so if low width lifts its Fmax it could add front coverage; small share since it lagged at 178 MSPS.

**Result (code):** 100 evaluations this round, 200 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `refine` — After 200 evals there are 0 feasible designs and the binding constraint is throughput: 100% of evaluations violate >=400 MSPS, with best seen 292 MSPS (a 37% shortfall), while accuracy is already comfortable (best 14.28 bits vs 12 required). The two unexplored families cannot help: iterative needs N+3 cycles/result and unrolled_k needs ceil(N/k)+3 (min 4) cycles/result, so even at the best observed Fmax they top out far below 400 MSPS, and pipelined_m is strictly worse than pipelined (186 vs 292 MSPS) because m>1 lengthens the combinational path. That leaves pipelined as the only candidate, and its Fmax must be raised by shrinking the datapath widths (data_width, angle_guard, frac_guard all widen the adders). Since accuracy has ~2 bits of headroom, we can push to the smallest widths that still clear 2^-12.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 200 evaluations (0 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 292
- max_abs_err <= 0.000244141: 76% violate; best seen 5.02e-05 (2^-14.28)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=16 n_iter=17 angle_guard=2 frac_guard=1 rounding=round]: throughput=273, max_abs_err=0.000177 (2^-12.47); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=18 angle_guard=0 frac_guard=0 rounding=round]: throughput=273, max_abs_err=0.000114 (2^-13.10); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=18 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=273, max_abs_err=0.000182 (2^-12.43); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=19 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=273, max_abs_err=0.000197 (2^-12.31); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=16 n_iter=18 angle_guard=1 frac_guard=2 rounding=round]: throughput=273, max_abs_err=0.0002 (2^-12.29); throughput_msps >= 400 violated by 31.8%

Per family:
- pipelined: 160 evals, 0 feasible; max throughput seen 292 MSPS; best accuracy 14.28 bits
- pipelined_m: 40 evals, 0 feasible; max throughput seen 186 MSPS; best accuracy 13.27 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Focus the whole round on pipelined at low widths: smaller data_width/angle_guard/frac_guard shorten the critical adder path (raising Fmax toward 400) and also cut LUTs, the primary objective. round is fixed because trunc already showed worse accuracy (e.g. 2^-12.43 vs 2^-13.10 at identical width). If even the smallest accuracy-feasible width cannot reach 400 MSPS, the spec is infeasible.*)
- `pipelined` (100 evals): data_width=13..16, n_iter=12..20, angle_guard=-2..2, frac_guard=0..2, rounding=round. *Why:* Only family that can reach 400 MSPS (1 result/cycle); probe the minimal-width region (data_width 13-16, angle_guard -2..2, frac_guard 0..2, round) to maximise Fmax while keeping max_abs_err <= 2^-12, and to find the smallest n_iter that still meets 12 bits so LUTs are minimised.

**Result (code):** 100 evaluations this round, 300 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The binding constraint is throughput, and it is structurally unreachable in this registry. Throughput = Fmax × results/cycle, and results/cycle ≤ 1 for every family: pipelined = 1, pipelined_m = 1, iterative = 1/(N+3), unrolled_k = k/(ceil(N/k)+3) ≤ 1. So the maximum achievable throughput over the whole registry is just the maximum Fmax of a 1-result/cycle design. Across 300 evaluations the best throughput seen is 292 MSPS (pipelined), 27% below the required 400; the only other 1-result/cycle family, pipelined_m, tops out at 186 MSPS. The two unexplored families cannot help: iterative would need Fmax ≥ 400·(N+3) ≥ 2800 MHz and unrolled_k similarly impossible rates, far beyond any Artix-7 clock. Meanwhile the accuracy constraint is comfortably satisfiable (best 14.28 bits ≥ 12), so it is not the blocker — throughput is. No design in the registry can meet throughput_msps ≥ 400, so the spec is infeasible rather than merely under-explored.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 300 evaluations (0 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 292
- max_abs_err <= 0.000244141: 78% violate; best seen 5.02e-05 (2^-14.28)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=16 n_iter=17 angle_guard=2 frac_guard=1 rounding=round]: throughput=273, max_abs_err=0.000177 (2^-12.47); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=18 angle_guard=0 frac_guard=0 rounding=round]: throughput=273, max_abs_err=0.000114 (2^-13.10); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=18 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=273, max_abs_err=0.000182 (2^-12.43); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=19 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=273, max_abs_err=0.000197 (2^-12.31); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=16 n_iter=18 angle_guard=1 frac_guard=2 rounding=round]: throughput=273, max_abs_err=0.0002 (2^-12.29); throughput_msps >= 400 violated by 31.8%

Per family:
- pipelined: 260 evals, 0 feasible; max throughput seen 292 MSPS; best accuracy 14.28 bits
- pipelined_m: 40 evals, 0 feasible; max throughput seen 186 MSPS; best accuracy 13.27 bits
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 23120 in, 25763 out
- provider-reported cost: $0.0249
- full prompts and replies: `llm_trace.jsonl`

