# DSE run: asic_power_50msps

**Verdict:** INFEASIBLE: the architect concluded no design in the registry meets the spec.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
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

- `throughput_msps >= 50`: met by 0/100 evaluations; best value seen 13.6
- `max_abs_err <= 0.000244141`: met by 46/100 evaluations; best value seen 1.35e-07 (2^-22.83)
- best throughput seen 13.6 MSPS (estimate); best accuracy 22.83 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraint is throughput >= 50 MSPS, and only iterative and unrolled_k are available to me. Neither is a 1-result/cycle family, so both must run at high Fmax; unrolled_k is far more likely to be feasible because k micro-rotations/cycle cuts the cycles-per-result. I therefore split the budget evenly: half on iterative to probe whether the lowest-power corner (small N, minimal guards) can actually reach 50 MSPS, and half on unrolled_k to map the realistic feasible front across k and n_iter. Accuracy (max_abs_err <= 2^-12) is the trade-off objective, so I keep data_width at the minimum that can represent 12 fractional bits (14) up to 18, n_iter in the 12-24 band where CORDIC error crosses 2^-12, and angle/frac guards small (0-2) to keep the datapath narrow for Fmax and power. Rounding is left as a 2-choice to let the solver pick the cheaper option. This focuses the 100 evals on the region where the power/accuracy trade-off actually lives rather than wasting budget on obviously-too-accurate or obviously-too-slow corners.*)
- `iterative` (30 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the only family that can plausibly hit 50 MSPS: with 1 result every N+3 cycles, throughput = Fmax/(N+3). To reach 50 MSPS we need Fmax >= 50*(N+3) MHz, so N must be small (N~12-18 gives Fmax targets of ~750-1100 MHz, which is aggressive but the only way this family meets the constraint; larger N makes it infeasible). Accuracy must be <= 2^-12, which for CORDIC is driven by n_iter and the guard bits, so I keep n_iter in 12-18 and data_width 14-18 (W=14 gives 12 fractional output bits, the minimum to even represent 2^-12). Small angle_guard/frac_guard keep the datapath narrow to push Fmax up and cut power. This is the high-risk/high-reward corner: if it meets throughput it will be the lowest-power point on the front.
- `unrolled_k` (30 evals): data_width=14..18, n_iter=12..24, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..8. *Why:* unrolled_k produces 1 result every ceil(N/k)+3 cycles, so for the same N it needs a much lower Fmax than iterative to hit 50 MSPS (e.g. N=18, k=4 -> 8 cycles/result -> Fmax >= 400 MHz, far more realistic). This is the more likely feasible family and the main carrier of the Pareto front. I widen n_iter to 24 and add k (2-8) so the search can trade off unroll depth against the number of micro-rotations: larger k raises per-cycle logic (more area/power, lower Fmax) but cuts cycles/result. Keeping data_width 14-18 and small guards preserves the accuracy-vs-power trade-off. Together with iterative this spans the low-power end (iterative, if feasible) and the realistic feasible bulk (unrolled_k).

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — Round 1 showed that neither iterative (max 9.83 MSPS) nor unrolled_k (max 7.15 MSPS) can reach the 50 MSPS throughput constraint. The accuracy constraint is already satisfiable (best 14.11 bits vs 12 required). The pipelined family is the only remaining architecture that produces 1 result/cycle and can plausibly meet 50 MSPS. I narrow its parameter ranges to the accuracy-feasible region found in Round 1 to maximize the chance of finding a feasible design within the remaining budget.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 9.83
- max_abs_err <= 0.000244141: 48% violate; best seen 5.64e-05 (2^-14.11)

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round]: throughput=7.27, max_abs_err=0.000176 (2^-12.48); throughput_msps >= 50 violated by 85.5%
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc]: throughput=7.01, max_abs_err=0.000175 (2^-12.48); throughput_msps >= 50 violated by 86.0%
- iterative [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc]: throughput=6.77, max_abs_err=9.49e-05 (2^-13.36); throughput_msps >= 50 violated by 86.5%
- iterative [data_width=17 n_iter=16 angle_guard=2 frac_guard=1 rounding=round]: throughput=6.64, max_abs_err=0.00012 (2^-13.03); throughput_msps >= 50 violated by 86.7%
- iterative [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round]: throughput=6.64, max_abs_err=8.41e-05 (2^-13.54); throughput_msps >= 50 violated by 86.7%

Per family:
- iterative: 30 evals, 0 feasible; max throughput seen 9.83 MSPS; best accuracy 14.11 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 7.15 MSPS; best accuracy 13.11 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The throughput constraint (>= 50 MSPS) is the binding constraint. Round 1 showed iterative maxes out at 9.83 MSPS and unrolled_k at 7.15 MSPS, both far below 50. Only the pipelined and pipelined_m families produce 1 result/cycle and can plausibly reach 50 MSPS. I add pipelined first (simpler, fewer parameters) with ranges narrowed to the accuracy-feasible region (data_width 16-18, n_iter 14-16) identified in Round 1, where max_abs_err <= 2^-12 was already achieved. This focuses the 40 remaining evaluations on the only family that can satisfy throughput while maintaining accuracy.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The throughput constraint is unreachable: iterative (1 result/cycle) peaked at 13.6 MSPS and unrolled_k at 7.15 MSPS, both far below the 50 MSPS requirement. The only families that can reach 50 MSPS are pipelined/pipelined_m (1 result/cycle), but they were never explored. Since this is the final round and no feasible design exists, the spec cannot be met by the explored families.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 13.6
- max_abs_err <= 0.000244141: 54% violate; best seen 1.35e-07 (2^-22.83)

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round]: throughput=7.27, max_abs_err=0.000176 (2^-12.48); throughput_msps >= 50 violated by 85.5%
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc]: throughput=7.01, max_abs_err=0.000175 (2^-12.48); throughput_msps >= 50 violated by 86.0%
- iterative [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc]: throughput=6.77, max_abs_err=9.49e-05 (2^-13.36); throughput_msps >= 50 violated by 86.5%
- iterative [data_width=17 n_iter=16 angle_guard=2 frac_guard=1 rounding=round]: throughput=6.64, max_abs_err=0.00012 (2^-13.03); throughput_msps >= 50 violated by 86.7%
- iterative [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round]: throughput=6.64, max_abs_err=8.41e-05 (2^-13.54); throughput_msps >= 50 violated by 86.7%

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 13.6 MSPS; best accuracy 22.83 bits
- unrolled_k: 50 evals, 0 feasible; max throughput seen 7.15 MSPS; best accuracy 20.73 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 6866 in, 2148 out
- provider-reported cost: $0.0046
- full prompts and replies: `llm_trace.jsonl`

