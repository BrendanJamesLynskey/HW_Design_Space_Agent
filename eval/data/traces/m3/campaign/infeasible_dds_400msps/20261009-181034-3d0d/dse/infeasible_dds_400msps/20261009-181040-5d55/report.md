# DSE run: infeasible_dds_400msps

**Verdict:** INFEASIBLE: the architect concluded no design in the registry meets the spec.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 100 of 400 budgeted, over 1 round(s).  
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

- `throughput_msps >= 400`: met by 0/100 evaluations; best value seen 282
- `max_abs_err <= 0.000244141`: met by 60/100 evaluations; best value seen 2.04e-05 (2^-15.58)
- best throughput seen 281.9 MSPS (estimate); best accuracy 15.58 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The throughput constraint of 400 MSPS single-lane requires one result per cycle at >=400 MHz, which only pipelined families can plausibly achieve. Iterative and unrolled_k produce one result every several cycles and would need impractically high clock rates. Accuracy constraint of 12 bits requires data_width >= 14 and n_iter >= ~13. We search pipelined and pipelined_m over data_width 12..20, n_iter 10..20, full guard ranges, both rounding modes, and m 2..8 for pipelined_m, to map the trade-off between LUTs, Fmax, and accuracy. Budget split favours pipelined as it has the shortest critical path and best chance of meeting 400 MHz.*)
- `pipelined` (60 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Pipelined gives 1 result/cycle, so throughput equals Fmax; only this family can plausibly reach 400 MSPS. Ranges cover the accuracy boundary (W>=14, N>=13) and the area/Fmax trade-off.
- `pipelined_m` (40 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Pipelined_m also gives 1 result/cycle but with fewer registers; it may offer a different area/Fmax trade-off. Search m to find the best balance.

**Result (code):** 100 evaluations this round, 100 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `infeasible` — The binding constraint is throughput_msps >= 400, and it is unreachable in this registry. Across 100 evaluations the best throughput seen is 282 MSPS (pipelined), 31.8% short of the target, and 100% of designs violate it. Only the pipelined/pipelined_m families can produce 1 result/cycle, so their throughput equals Fmax; pipelined_m already tops out lower (171 MSPS), and the two unexplored families are structurally slower still: iterative yields 1 result per N+3 cycles and unrolled_k 1 per ceil(N/k)+3 cycles, so neither can exceed the Fmax-limited throughput of pipelined. Accuracy is not the blocker — up to 15.58 bits is achievable versus the 12 bits required — so no amount of re-tuning data_width/n_iter/guards can close a 42% throughput gap that is set by the per-stage Fmax ceiling. No design in the registry can meet the spec.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 282
- max_abs_err <= 0.000244141: 40% violate; best seen 2.04e-05 (2^-15.58)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=17 n_iter=18 angle_guard=0 frac_guard=0 rounding=round]: throughput=273, max_abs_err=0.000244 (2^-12.00); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=15 n_iter=18 angle_guard=3 frac_guard=3 rounding=round]: throughput=273, max_abs_err=0.000158 (2^-12.63); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=17 n_iter=18 angle_guard=0 frac_guard=1 rounding=round]: throughput=273, max_abs_err=0.000209 (2^-12.22); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=15 n_iter=18 angle_guard=2 frac_guard=3 rounding=round]: throughput=273, max_abs_err=0.000237 (2^-12.04); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=17 n_iter=18 angle_guard=1 frac_guard=1 rounding=round]: throughput=273, max_abs_err=0.000128 (2^-12.94); throughput_msps >= 400 violated by 31.8%

Per family:
- pipelined: 60 evals, 0 feasible; max throughput seen 282 MSPS; best accuracy 14.78 bits
- pipelined_m: 40 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.58 bits
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 18611 in, 8101 out
- provider-reported cost: $0.0060
- full prompts and replies: `llm_trace.jsonl`

