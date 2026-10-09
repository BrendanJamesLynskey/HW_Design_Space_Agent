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

- `throughput_msps >= 400`: met by 0/200 evaluations; best value seen 273
- `max_abs_err <= 0.000244141`: met by 107/200 evaluations; best value seen 1.04e-05 (2^-16.56)
- best throughput seen 272.9 MSPS (estimate); best accuracy 16.56 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraint is throughput_msps >= 400 with max_abs_err <= 2^-12. Accuracy forces data_width to be at least ~14-16 (output LSB 2^-(W-2)) and n_iter to be comparable to W, so the accuracy-feasible designs are not tiny. That immediately rules out iterative (N+3 cycles/result) and makes unrolled_k marginal at best, since both need Fmax far above what an Artix-7 CORDIC datapath can deliver. Only the 1-result/cycle families (pipelined, pipelined_m) can plausibly satisfy 400 MSPS, so they take 90% of the budget. Round 1 sweeps W=14..20 and N=14..22 with small guard ranges and both rounding modes: W is the main accuracy/area/Fmax knob, N the convergence knob, and the guards/rounding are cheap accuracy levers that matter once W is near the 2^-12 boundary. pipelined_m's m=2..4 is included because if pipelined clears 400 MHz with margin, the min-LUT selection will land on a coarser-registered variant. The 10% unrolled_k probe is a boundary check, not a front candidate. If round 1 shows pipelined_m dominating the feasible set, later rounds should shift budget toward it and toward the exact W/N edge where max_abs_err crosses 2^-12, while keeping a few pipelined points to pin the max-Fmax end of the front.*)
- `pipelined` (55 evals): data_width=14..20, n_iter=14..22, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* Only 1-result/cycle families can plausibly reach 400 MSPS: throughput_msps = Fmax x 1. With one registered micro-rotation per stage there is no barrel shifter in the critical path, so this family has the best chance of a high Fmax at the W~16 needed for 2^-12 accuracy. It is also the natural anchor for the min-LUT objective once throughput is satisfied, and its (W, N, guards, rounding) sweep maps the accuracy/area trade-off directly.
- `pipelined_m` (35 evals): data_width=14..20, n_iter=14..22, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, m=2..4. *Why:* Same 1-result/cycle throughput as pipelined but registers every m stages, so it trades Fmax for far fewer FFs. If pipelined's Fmax is comfortably above 400 MHz, pipelined_m with m=2..4 can cut luts_plus_ffs at the same accuracy and still clear the throughput constraint, which is exactly the min-LUT corner the selection rule wants. m is capped at 4 so the combinational path stays short enough to keep Fmax near the 400 MSPS boundary.
- `unrolled_k` (10 evals): data_width=14..20, n_iter=14..22, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, k=6..8. *Why:* Small probe only. unrolled_k emits 1 result per ceil(N/k)+3 cycles, so even at k=8 and N=14 it needs Fmax in the GHz range to reach 400 MSPS; it is almost certainly infeasible for this spec. The share is kept just large enough to document that boundary and to catch any surprise high-k/low-N corner, rather than to compete for the front.

**Result (code):** 100 evaluations this round, 100 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `refine` — Only throughput is unmet: pipelined tops out at 273 MSPS vs the 400-MSPS requirement, a 33.9% shortfall, while accuracy is already comfortably met (2^-13.40 to 2^-16.56 max_abs_err, bound is 2^-12). Since pipelined/pipelined_m yield throughput = Fmax (one result per cycle) and pipelined is the fastest family by a wide margin (273 vs 171 vs 7.37 MSPS), any feasible point must come from a pipelined configuration with a shorter registered critical path, i.e. a smaller data_width. Round-1 leaders all sat at W=17-19, so the low-width region that raises Fmax has not been covered. Accuracy pins the smallest usable width: output LSB is 2^-(W-2), so with rounding the quantization error is ~2^-(W-1) — at W=13 that equals the 2^-12 limit with no margin, at W=14 it leaves a factor of two, hence W>=14. The decisive probe is therefore pipelined around W=14 (n_iter enough for convergence, frac_guard/angle_guard added back for error). If Fmax stays below 400 at that minimum accuracy-viable width, no registry design can satisfy the spec and the correct call is infeasible.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 273
- max_abs_err <= 0.000244141: 34% violate; best seen 1.04e-05 (2^-16.56)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=17 n_iter=19 angle_guard=2 frac_guard=1 rounding=round]: throughput=264, max_abs_err=9.28e-05 (2^-13.40); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=17 n_iter=21 angle_guard=3 frac_guard=1 rounding=round]: throughput=264, max_abs_err=9.28e-05 (2^-13.40); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=17 n_iter=19 angle_guard=2 frac_guard=1 rounding=trunc]: throughput=264, max_abs_err=0.000174 (2^-12.49); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=18 n_iter=21 angle_guard=0 frac_guard=3 rounding=round]: throughput=264, max_abs_err=0.000105 (2^-13.22); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=19 n_iter=19 angle_guard=2 frac_guard=1 rounding=round]: throughput=264, max_abs_err=2.75e-05 (2^-15.15); throughput_msps >= 400 violated by 33.9%

Per family:
- unrolled_k: 10 evals, 0 feasible; max throughput seen 7.37 MSPS; best accuracy 14.14 bits
- pipelined: 55 evals, 0 feasible; max throughput seen 273 MSPS; best accuracy 16.56 bits
- pipelined_m: 35 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.03 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Only throughput_msps>=400 is unmet (best 273 MSPS, 33.9% short); accuracy is already satisfiable (least-violating design hits 2^-13.40 max_abs_err, best seen 2^-16.56). For pipelined and pipelined_m the throughput equals Fmax (1 result/cycle), and pipelined has by far the highest Fmax (273 vs 171 vs 7.37 MSPS), so 400 MSPS can only come from pipelined with a shorter registered path. Round-1 winners were all at W=17-19; Fmax is dominated by the per-stage adder/shifter width, so lower data_width must be probed. Accuracy fixes the lower bound on width: output LSB = 2^-(W-2), and with rounding the quantization error is ~2^-(W-1); at W=13 that is exactly 2^-12 = the constraint (no margin) and at W=14 it is 2^-13, leaving headroom. So W>=14 is the smallest accuracy-viable width; the decisive experiment is whether pipelined at W~14 reaches 400 MSPS. If Fmax is still <400 at W=14 (and larger W only lowers it), the throughput constraint is unreachable at any accuracy-feasible width and the spec is infeasible.*)
- `pipelined` (85 evals): data_width=12..16, n_iter=12..24, angle_guard=2..4, frac_guard=2..4, rounding=round|trunc. *Why:* pipelined is the only family whose throughput = Fmax with 1 result/cycle and the highest Fmax seen (273 MSPS vs 171 pipelined_m, 7.37 unrolled_k). The binding constraint is throughput>=400, so shrink the registered-stage logic depth by sweeping small data_width.
- `pipelined_m` (15 evals): data_width=12..15, n_iter=12..24, angle_guard=2..4, frac_guard=2..4, rounding=round, m=2..3. *Why:* keep a small probe on the other 1-result/cycle family at small width / short m=2..3, in case its Fmax exceeds pipelined at low W.
- clamped by code: pipelined: dropped unknown parameter 'family'
- clamped by code: pipelined_m: dropped unknown parameter 'family'

**Result (code):** 100 evaluations this round, 200 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The binding constraint is throughput_msps >= 400, and it is structurally unreachable in this registry. Every one of the 200 evaluations violates it (100% violation), with the best value seen being 273 MSPS — 31.8% short of the requirement. The highest-throughput family is `pipelined` (1 result/cycle, so throughput = Fmax), and its best observed Fmax is 273 MHz; `pipelined_m` (also 1/cycle) tops out at 171 MSPS and `unrolled_k` at 7.37 MSPS. The only unexplored family, `iterative`, is strictly slower (1 result per N+3 cycles), so it cannot help. Reaching 400 MSPS would require Fmax >= 400 MHz, a 46% increase over the best Fmax any design achieved. The accuracy constraint does not rescue this: max_abs_err <= 2^-12 forces data_width >= 14 (output LSB is 2^-(W-2), so W=13 already has 2^-11 quantization and cannot meet 2^-12), and at the required widths the Fmax estimate saturates at ~273 MHz (e.g. the least-violating pipelined designs at W=14/15 all report throughput=273). Accuracy itself is easily met (best 2^-16.56), so the two constraints are mutually exclusive: no design in the registry can simultaneously satisfy throughput >= 400 MSPS and max_abs_err <= 2^-12. Declaring infeasible rather than settling for a throughput-violating design.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 200 evaluations (0 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 273
- max_abs_err <= 0.000244141: 46% violate; best seen 1.04e-05 (2^-16.56)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=15 n_iter=23 angle_guard=3 frac_guard=3 rounding=round]: throughput=273, max_abs_err=0.000158 (2^-12.63); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=15 n_iter=16 angle_guard=3 frac_guard=3 rounding=round]: throughput=273, max_abs_err=0.000158 (2^-12.63); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=15 n_iter=24 angle_guard=3 frac_guard=2 rounding=round]: throughput=273, max_abs_err=0.000192 (2^-12.35); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=15 n_iter=17 angle_guard=2 frac_guard=3 rounding=round]: throughput=273, max_abs_err=0.000237 (2^-12.04); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=14 n_iter=23 angle_guard=4 frac_guard=4 rounding=round]: throughput=273, max_abs_err=0.000224 (2^-12.12); throughput_msps >= 400 violated by 31.8%

Per family:
- unrolled_k: 10 evals, 0 feasible; max throughput seen 7.37 MSPS; best accuracy 14.14 bits
- pipelined: 140 evals, 0 feasible; max throughput seen 273 MSPS; best accuracy 16.56 bits
- pipelined_m: 50 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.03 bits
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 14479 in, 14661 out
- provider-reported cost: $0.0166
- full prompts and replies: `llm_trace.jsonl`

