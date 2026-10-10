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

- `throughput_msps >= 400`: met by 0/100 evaluations; best value seen 282
- `max_abs_err <= 0.000244141`: met by 37/100 evaluations; best value seen 4.73e-05 (2^-14.37)
- best throughput seen 281.9 MSPS (estimate); best accuracy 14.37 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >= 400 MSPS single-lane throughput with max_abs_err <= 2^-12. Only pipelined and pipelined_m guarantee 1 result/cycle, making them the primary candidates for meeting the throughput constraint. unrolled_k can also meet throughput if Fmax is high enough relative to its multi-cycle latency, so it is included as a secondary candidate. iterative is excluded because its 1 result per N+3 cycles makes 400 MSPS infeasible unless Fmax is extremely high (>1000 MHz for N=12), which is unrealistic on Artix-7. We focus data_width 12-18 and n_iter 12-18 to balance accuracy (need ~12+ bits of precision) against LUT cost. angle_guard and frac_guard are kept modest to minimize area. The budget is split 40/35/25 across pipelined, pipelined_m, and unrolled_k respectively, reflecting pipelined_m's likely advantage in Fmax due to reduced register pressure.*)
- `pipelined` (40 evals): data_width=12..18, n_iter=12..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Only family with guaranteed 1 result/cycle throughput. To hit 400 MSPS, Fmax must be >= 400 MHz. Pipelined has the longest critical path (N stages), so it is the hardest to meet 400 MHz. We search a wide range of n_iter (12-18) to find the minimum N that meets accuracy (err <= 2^-12) while keeping the pipeline short enough for high Fmax. data_width 12-18 balances accuracy vs LUT cost.
- `pipelined_m` (35 evals): data_width=12..18, n_iter=12..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* Pipelined_m registers every m stages, reducing FF count and potentially improving Fmax compared to fully pipelined by breaking the long chain. Still 1 result/cycle. The m parameter allows trading off latency for area/timing. We search m=2..8 to find the best Fmax/LUT tradeoff. This is the most promising family for meeting 400 MSPS with minimal LUTs.
- `unrolled_k` (25 evals): data_width=12..18, n_iter=12..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..8. *Why:* Unrolled_k produces 1 result every ceil(N/k)+3 cycles. For 400 MSPS, we need Fmax * k / (ceil(N/k)+3) >= 400. With k=8 and N=12, latency is ceil(12/8)+3 = 5 cycles, so Fmax >= 200 MHz is needed. This is more achievable than 400 MHz for pipelined. However, LUT cost may be higher due to parallel datapaths. We include it to map the tradeoff and find if it offers lower LUTs at feasible Fmax.

**Result (code):** 100 evaluations this round, 100 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `infeasible` — The throughput constraint (>= 400 MSPS) is unreachable for all families in the registry. The pipelined family, which offers the highest throughput (1 result/cycle), achieved a maximum of only 282 MSPS in Round 1. To reach 400 MSPS, the clock frequency would need to increase by a factor of ~1.42 (400/282). However, the designs that achieved the best accuracy (meeting the error constraint) were already operating at the limit of the cost model's Fmax estimates for their respective data widths and iteration counts. Increasing the clock frequency further to meet the throughput target would require reducing the data width or iteration count, which would violate the max_abs_err <= 2^-12 constraint (best seen error was 4.73e-05, but the designs meeting this error had throughput capped at 282 MSPS). The unrolled_k and pipelined_m families have even lower throughput ceilings (12 and 178 MSPS respectively) due to their multi-cycle or partial-pipeline nature. Since the best possible throughput from the highest-throughput family (pipelined) is 282 MSPS, which is significantly below the 400 MSPS requirement, and no other family can exceed this, the spec is infeasible.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 282
- max_abs_err <= 0.000244141: 63% violate; best seen 4.73e-05 (2^-14.37)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=16 n_iter=17 angle_guard=1 frac_guard=2 rounding=round]: throughput=273, max_abs_err=0.0002 (2^-12.29); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=17 n_iter=17 angle_guard=1 frac_guard=1 rounding=round]: throughput=273, max_abs_err=0.000128 (2^-12.94); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=17 angle_guard=-1 frac_guard=0 rounding=round]: throughput=273, max_abs_err=0.000186 (2^-12.39); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=17 n_iter=18 angle_guard=1 frac_guard=1 rounding=round]: throughput=273, max_abs_err=0.000128 (2^-12.94); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=16 n_iter=17 angle_guard=2 frac_guard=1 rounding=round]: throughput=273, max_abs_err=0.000177 (2^-12.47); throughput_msps >= 400 violated by 31.8%

Per family:
- unrolled_k: 25 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 14.37 bits
- pipelined: 40 evals, 0 feasible; max throughput seen 282 MSPS; best accuracy 13.83 bits
- pipelined_m: 35 evals, 0 feasible; max throughput seen 178 MSPS; best accuracy 13.83 bits
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 17626 in, 2141 out
- provider-reported cost: $0.0050
- full prompts and replies: `llm_trace.jsonl`

