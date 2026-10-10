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
- `max_abs_err <= 0.000244141`: met by 82/100 evaluations; best value seen 1.15e-06 (2^-19.73)
- best throughput seen 272.9 MSPS (estimate); best accuracy 19.73 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=400 MSPS single-lane throughput, which rules out iterative and unrolled_k (they produce 1 result every several cycles, so even at high Fmax they likely cannot reach 400 MSPS unless Fmax is extremely high, which is unlikely for wide CORDIC datapaths). Only pipelined and pipelined_m guarantee 1 result/cycle. The accuracy constraint (max_abs_err <= 2^-12) requires accuracy_bits >= 12, which depends on data_width, n_iter, angle_guard, frac_guard, and rounding. We focus data_width 16-28 (narrower widths save LUTs but may not meet accuracy; 16 is a reasonable lower bound for 12-bit accuracy with sufficient n_iter) and n_iter 12-24 (fewer iterations save area but reduce accuracy). angle_guard and frac_guard are kept in tight ranges since they have smaller impact on LUTs than data_width and n_iter. We split budget 55/45 between pipelined and pipelined_m since pipelined_m can potentially achieve lower LUTs by reducing register count and datapath width per stage, while pipelined serves as the baseline. Both families share the same accuracy characteristics, so the trade-off is purely in area (LUTs/FFs) vs Fmax, which affects throughput. The min-LUT objective will favor designs with smaller data_width and n_iter that still meet the accuracy constraint.*)
- `pipelined` (55 evals): data_width=16..28, n_iter=12..24, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Only pipelined/pipelined_m guarantee 1 result/cycle, which is required to hit >=400 MSPS. Pipelined is the baseline for the throughput constraint. We focus data_width 16-28 and n_iter 12-24 to find the minimal LUT design that meets max_abs_err <= 2^-12 (accuracy_bits >= 12). Lower n_iter and data_width reduce LUTs but risk missing the accuracy constraint; the search will map this trade-off.
- `pipelined_m` (45 evals): data_width=16..28, n_iter=12..24, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Pipelined_m registers every m stages, reducing FF count and potentially LUTs (smaller datapath segments) while still delivering 1 result/cycle. This can yield lower LUT counts than fully pipelined for the same accuracy, making it a strong candidate for the min-LUT objective. m in 2-4 balances latency vs area. Same accuracy parameter ranges as pipelined since accuracy is identical across families.

**Result (code):** 100 evaluations this round, 100 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `infeasible` — The throughput constraint (>= 400 MSPS) is unreachable for all families in the registry. The pipelined family, which offers the highest throughput (1 result/cycle), achieved a maximum of 273 MSPS in Round 1. This is a 31.8% shortfall. Since throughput is defined as Fmax * results/cycle, and the pipelined architecture already maximizes results/cycle at 1, the only way to increase throughput is to increase Fmax. However, the cost model estimates Fmax based on the critical path delay of the micro-rotation stage. The least-violating designs show that even with minimal guard bits (angle_guard=0, frac_guard=0) and rounding, the Fmax is capped such that throughput remains below 400 MSPS. The iterative and unrolled_k families have lower throughput (1 result every k or N+3 cycles), so they cannot exceed the pipelined family's throughput. Therefore, no design in the registry can meet the 400 MSPS constraint.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 273
- max_abs_err <= 0.000244141: 18% violate; best seen 1.15e-06 (2^-19.73)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=17 n_iter=23 angle_guard=0 frac_guard=0 rounding=round]: throughput=273, max_abs_err=0.000244 (2^-12.00); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=17 n_iter=20 angle_guard=1 frac_guard=1 rounding=trunc]: throughput=273, max_abs_err=0.000198 (2^-12.30); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=17 n_iter=16 angle_guard=1 frac_guard=1 rounding=round]: throughput=273, max_abs_err=0.000128 (2^-12.94); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=17 n_iter=23 angle_guard=1 frac_guard=1 rounding=round]: throughput=273, max_abs_err=0.000128 (2^-12.94); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=17 n_iter=20 angle_guard=1 frac_guard=0 rounding=round]: throughput=273, max_abs_err=0.000149 (2^-12.71); throughput_msps >= 400 violated by 31.8%

Per family:
- pipelined: 55 evals, 0 feasible; max throughput seen 273 MSPS; best accuracy 19.73 bits
- pipelined_m: 45 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 19.47 bits
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 17419 in, 1523 out
- provider-reported cost: $0.0031
- full prompts and replies: `llm_trace.jsonl`

