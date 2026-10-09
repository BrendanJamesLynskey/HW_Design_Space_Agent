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
- `max_abs_err <= 0.000244141`: met by 76/100 evaluations; best value seen 2.18e-05 (2^-15.49)
- best throughput seen 272.9 MSPS (estimate); best accuracy 15.49 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=400 MSPS single-lane throughput and max_abs_err <= 2^-12 (~0.000244). The iterative family (1 result per N+3 cycles) cannot plausibly reach 400 MSPS unless Fmax is extremely high (e.g., 4000+ MHz for N=14), which is unrealistic on Artix-7, so it is excluded. The three throughput-capable families are pipelined_m, unrolled_k, and pipelined. For accuracy: max_abs_err <= 2^-12 requires roughly data_width >= 14 and n_iter >= 14 (since CORDIC error ~ 2^-(n_iter+1) for the angle, and output quantization is 2^-(W-2); W=14 gives LSB=2^-12, so W>=14 is the minimum). I set data_width 14-20 and n_iter 14-20 to cover the accuracy constraint with margin while keeping LUTs low (the objective). angle_guard 0-2 and frac_guard 0-2 are small ranges since the accuracy constraint is tight at 2^-12 and large guards would waste bits without helping. m is 2-8 for pipelined_m to explore the area/latency/Fmax trade-off. k is 4-8 for unrolled_k since k<4 would need Fmax > 100 MHz x (400/k) which is tight. Budget is weighted toward pipelined_m (55%) as the most likely feasible and area-efficient family, unrolled_k (30%) as a potentially lower-area alternative, and pipelined (15%) to map the high-Fmax/low-latency corner.*)
- `pipelined_m` (55 evals): data_width=14..20, n_iter=14..20, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* 1 result/cycle architecture; with Fmax ~200-300 MHz, throughput = Fmax x 1 easily exceeds 400 MSPS. m controls area/latency trade-off. This is the most likely feasible family for the throughput constraint.
- `unrolled_k` (30 evals): data_width=14..20, n_iter=14..20, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=4..8. *Why:* k micro-rotations/cycle gives throughput = Fmax x k. With k=4-8 and Fmax ~100-200 MHz, throughput can reach 400-1600 MSPS. Fewer pipeline stages than pipelined_m, potentially fewer LUTs. k>=4 needed to plausibly hit 400 MSPS at realistic Fmax.
- `pipelined` (15 evals): data_width=14..20, n_iter=14..20, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Fully pipelined (m=1 equivalent), 1 result/cycle. Highest Fmax potential due to shortest critical path per stage, but most registers. Included to map the area/Fmax trade-off at the extreme end. Likely more LUTs+FFs than pipelined_m but may allow higher Fmax.

**Result (code):** 100 evaluations this round, 100 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `infeasible` — The throughput constraint (>= 400 MSPS) is unreachable for all families in the registry. The pipelined family, which offers the highest theoretical throughput (1 result/cycle), achieved a maximum of only 273 MSPS in Round 1. This is a 31.8% shortfall. The other families (unrolled_k, pipelined_m) have significantly lower maximum throughputs (9.7 and 171 MSPS respectively) due to their multi-cycle or reduced-register architectures, making them even further from the 400 MSPS target. Since the best-case architecture (pipelined) cannot meet the throughput requirement even with optimal parameter tuning (as evidenced by the search exploring the full range of n_iter and data_width), no design in the registry can satisfy the spec.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 273
- max_abs_err <= 0.000244141: 24% violate; best seen 2.18e-05 (2^-15.49)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=17 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc]: throughput=273, max_abs_err=0.000239 (2^-12.03); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=19 n_iter=18 angle_guard=1 frac_guard=2 rounding=trunc]: throughput=264, max_abs_err=3.99e-05 (2^-14.61); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=17 n_iter=18 angle_guard=1 frac_guard=2 rounding=trunc]: throughput=264, max_abs_err=0.000137 (2^-12.84); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=19 n_iter=17 angle_guard=1 frac_guard=2 rounding=round]: throughput=264, max_abs_err=3.97e-05 (2^-14.62); throughput_msps >= 400 violated by 33.9%
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc]: throughput=264, max_abs_err=3.04e-05 (2^-15.00); throughput_msps >= 400 violated by 33.9%

Per family:
- unrolled_k: 30 evals, 0 feasible; max throughput seen 9.7 MSPS; best accuracy 15.35 bits
- pipelined: 15 evals, 0 feasible; max throughput seen 273 MSPS; best accuracy 15.00 bits
- pipelined_m: 55 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.49 bits
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 17471 in, 1715 out
- provider-reported cost: $0.0041
- full prompts and replies: `llm_trace.jsonl`

