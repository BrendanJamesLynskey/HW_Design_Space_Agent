# DSE run: infeasible_dds_400msps

**Verdict:** INFEASIBLE: the architect concluded no design in the registry meets the spec.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
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

- `throughput_msps >= 400`: met by 0/100 evaluations; best value seen 273
- `max_abs_err <= 0.000244141`: met by 82/100 evaluations; best value seen 4.44e-06 (2^-17.78)
- best throughput seen 272.9 MSPS (estimate); best accuracy 17.78 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >=400 MSPS single-lane throughput, which only the pipelined family (1 result/cycle) can plausibly achieve; iterative and unrolled_k produce one result every several cycles and would need Fmax > 1000+ MHz to hit 400 MSPS, which is unrealistic on Artix-7. I focus 100% of the first round on `pipelined` with ranges tuned to the 2^-12 accuracy constraint: data_width 14-22 (accuracy_bits ~12-20), n_iter 12-20 (enough micro-rotations for 2^-12 error), and minimal guard bits to keep LUT count low. If this round shows no feasible points (Fmax too low for 400 MSPS), the next round will add pipelined_m with m=2-4 to reduce register count and potentially raise Fmax, or widen the search. The campaign notes confirm pipelined is the only viable route.*)
- `pipelined` (100 evals): data_width=14..22, n_iter=12..20, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Only pipelined/pipelined_m give 1 result/cycle, the sole route to >=400 MSPS. Full pipelining (m=1) is the baseline for max Fmax; n_iter 12-20 and data_width 14-22 bracket the 2^-12 accuracy requirement while keeping LUTs low. angle_guard/frac_guard kept small to minimize area.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `infeasible` — The throughput constraint (>= 400 MSPS) is unreachable by any family in the registry. The pipelined family, which is the only architecture capable of 1 result/cycle, achieved a maximum throughput of 273 MSPS in Round 1. Since the iterative and unrolled_k families produce fewer than 1 result per cycle (1/k or 1/N), their throughput is strictly lower than the pipelined family's 273 MSPS for any given data width and clock frequency. Therefore, no design in the registry can meet the 400 MSPS requirement.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: pipelined. Not yet explored: iterative, unrolled_k, pipelined_m.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 273
- max_abs_err <= 0.000244141: 18% violate; best seen 4.44e-06 (2^-17.78)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=16 n_iter=19 angle_guard=1 frac_guard=2 rounding=trunc]: throughput=273, max_abs_err=0.00023 (2^-12.08); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=16 n_iter=19 angle_guard=2 frac_guard=2 rounding=round]: throughput=273, max_abs_err=0.000138 (2^-12.83); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=273, max_abs_err=0.000206 (2^-12.25); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round]: throughput=273, max_abs_err=0.0002 (2^-12.28); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=16 n_iter=20 angle_guard=1 frac_guard=2 rounding=trunc]: throughput=273, max_abs_err=0.000237 (2^-12.04); throughput_msps >= 400 violated by 31.8%

Per family:
- pipelined: 100 evals, 0 feasible; max throughput seen 273 MSPS; best accuracy 17.78 bits
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 18119 in, 1023 out
- provider-reported cost: $0.0026
- full prompts and replies: `llm_trace.jsonl`

