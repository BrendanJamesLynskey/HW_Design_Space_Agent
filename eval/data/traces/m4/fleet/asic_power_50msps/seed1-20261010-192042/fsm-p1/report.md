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

- `throughput_msps >= 50`: met by 0/100 evaluations; best value seen 19.7
- `max_abs_err <= 0.000244141`: met by 54/100 evaluations; best value seen 1.15e-06 (2^-19.73)
- best throughput seen 19.7 MSPS (estimate); best accuracy 19.73 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *iterative is analytically infeasible for this spec: throughput = Fmax/(N+3), and accuracy <= 2^-12 requires N >= 13, so Fmax >= 50*(13+3) = 800 MHz, which is implausible for sky130 standard cells. Therefore I allocate 0 budget to iterative and focus all 100 evaluations on unrolled_k, the only assigned family that can reduce cycles/result via unrolling while keeping N high for accuracy. The chosen ranges bracket the likely feasible corner (N~13-14, W~14-16, k~7-8) and extend outward to map the trade-off curve and confirm feasibility.*)
- `unrolled_k` (60 evals): data_width=12..18, n_iter=12..18, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=4..8. *Why:* Only family that can plausibly meet 50 MSPS: unrolling k micro-rotations per cycle reduces cycles/result to ceil(N/k)+3, so high k (7-8) with N~13-14 gives 5 cycles/result, requiring Fmax >= 250 MHz. The ranges cover the accuracy-throughput trade-off: n_iter 12-18 for max_abs_err <= 2^-12, data_width 12-18 for output quantization, k 4-8 to trade Fmax against cycles, and small guards to keep area/power low. This will reveal whether any unrolled_k design meets both constraints and where the power-accuracy Pareto front lies.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The binding constraint is throughput, not accuracy: unrolled_k tops out at 6.8 MSPS (needs 50) because it retires one result every ceil(N/k)+3 cycles, while accuracy is already met (best 2^-14.11, and W=17/N=15/guard=0/frac=1/round gives 2^-12.12 <= 2^-12). The registry's only 1-result-per-cycle families are pipelined and pipelined_m, neither yet explored; at any plausible Fmax they clear 50 MSPS, and pipelined_m (m>1) can cut the per-stage register cost that drives power_index. unrolled_k is dropped as it cannot close a 7x throughput gap.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: unrolled_k. Not yet explored: iterative.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 6.8
- max_abs_err <= 0.000244141: 48% violate; best seen 5.64e-05 (2^-14.11)

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=17 n_iter=15 angle_guard=0 frac_guard=1 rounding=round k=4]: throughput=5.34, max_abs_err=0.000224 (2^-12.12); throughput_msps >= 50 violated by 89.3%
- unrolled_k [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc k=4]: throughput=5.13, max_abs_err=0.000235 (2^-12.06); throughput_msps >= 50 violated by 89.7%
- unrolled_k [data_width=18 n_iter=15 angle_guard=0 frac_guard=2 rounding=round k=4]: throughput=4.92, max_abs_err=0.000123 (2^-12.99); throughput_msps >= 50 violated by 90.2%
- unrolled_k [data_width=18 n_iter=14 angle_guard=0 frac_guard=2 rounding=round k=4]: throughput=4.92, max_abs_err=0.000179 (2^-12.45); throughput_msps >= 50 violated by 90.2%
- unrolled_k [data_width=18 n_iter=15 angle_guard=0 frac_guard=2 rounding=round k=5]: throughput=4.64, max_abs_err=0.000123 (2^-12.99); throughput_msps >= 50 violated by 90.7%

Per family:
- unrolled_k: 60 evals, 0 feasible; max throughput seen 6.8 MSPS; best accuracy 14.11 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Spend the remaining 40 evals on the two 1-result-per-cycle families, which are the only ones that can satisfy throughput_msps >= 50; keep the accuracy box tight around the already-proven feasible accuracy region so the search optimises power_index rather than re-discovering accuracy.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — Final round: only `stop` or `infeasible` are permitted. I cannot honestly declare `infeasible`, because the throughput constraint is not proven unreachable — the registry contains the `pipelined`/`pipelined_m` families that emit 1 result/cycle, so any Fmax >= 50 MHz would satisfy throughput_msps >= 50, and the accuracy constraint is already comfortably met (best seen 2^-19.73, far better than the required 2^-12). The failure is a search-coverage failure, not a registry limitation: only `iterative` (max 19.7 MSPS) and `unrolled_k` (max 9.94 MSPS) were actually evaluated, and both are inherently multi-cycle, so 100% of the 100 evaluations violate throughput. With the budget exhausted (100/100 evals, round 2 of 4, HV 0, 0 feasible), no further refinement, widening, or family addition can be run, so the run must end. Evidence: 0/100 feasible; throughput best 19.7 MSPS vs 50 required; accuracy best 1.15e-06 vs 2.44e-04 required. Recommendation for any future run: seed directly on `pipelined`/`pipelined_m` with data_width ~17-20, n_iter ~14-16, which should clear both constraints.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 19.7
- max_abs_err <= 0.000244141: 46% violate; best seen 1.15e-06 (2^-19.73)

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=17 n_iter=15 angle_guard=0 frac_guard=1 rounding=round k=4]: throughput=5.34, max_abs_err=0.000224 (2^-12.12); throughput_msps >= 50 violated by 89.3%
- unrolled_k [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc k=4]: throughput=5.13, max_abs_err=0.000235 (2^-12.06); throughput_msps >= 50 violated by 89.7%
- iterative [data_width=20 n_iter=21 angle_guard=0 frac_guard=0 rounding=round]: throughput=5.08, max_abs_err=3.25e-05 (2^-14.91); throughput_msps >= 50 violated by 89.8%
- unrolled_k [data_width=18 n_iter=15 angle_guard=0 frac_guard=2 rounding=round k=4]: throughput=4.92, max_abs_err=0.000123 (2^-12.99); throughput_msps >= 50 violated by 90.2%
- unrolled_k [data_width=18 n_iter=14 angle_guard=0 frac_guard=2 rounding=round k=4]: throughput=4.92, max_abs_err=0.000179 (2^-12.45); throughput_msps >= 50 violated by 90.2%

Per family:
- iterative: 20 evals, 0 feasible; max throughput seen 19.7 MSPS; best accuracy 19.73 bits
- unrolled_k: 80 evals, 0 feasible; max throughput seen 9.94 MSPS; best accuracy 18.96 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 6853 in, 9819 out
- provider-reported cost: $0.0119
- full prompts and replies: `llm_trace.jsonl`

