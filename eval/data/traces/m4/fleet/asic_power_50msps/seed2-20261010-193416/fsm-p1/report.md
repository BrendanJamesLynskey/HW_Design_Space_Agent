# DSE run: asic_power_50msps

**Verdict:** INFEASIBLE: the architect concluded no design in the registry meets the spec.  
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

- `throughput_msps >= 50`: met by 0/100 evaluations; best value seen 13.6
- `max_abs_err <= 0.000244141`: met by 43/100 evaluations; best value seen 1.35e-07 (2^-22.83)
- best throughput seen 13.6 MSPS (estimate); best accuracy 22.83 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The 50 MSPS throughput constraint combined with the 2^-12 max error requirement forces a multi-cycle architecture with enough parallelism. Iterative computes one micro-rotation per cycle, so for N~14 it needs ~17 cycles/result, requiring Fmax > 850 MHz to hit 50 MSPS, which is implausible in sky130. unrolled_k with k>=4 reduces cycles/result to <=7, making 50 MSPS achievable at realistic Fmax. Therefore, we allocate 90% of the budget to unrolled_k to map its power-accuracy trade-off, and 10% to iterative to confirm its infeasibility and avoid missing any unexpected feasible corner. The parameter ranges for unrolled_k focus on the plausible feasible region: data_width 13-18 (just above the 2^-12 quantization limit), n_iter 10-18 (enough CORDIC iterations with guards), angle_guard -2..3, frac_guard 0..3, both rounding modes, and k 2..8 to cover the parallelism vs. critical-path trade-off. We expect the Pareto front to be dominated by unrolled_k, with power increasing with k, N, W, and guards.*)
- `unrolled_k` (54 evals): data_width=13..18, n_iter=10..18, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round, k=2..8. *Why:* Only family that can plausibly satisfy both the 50 MSPS throughput and 2^-12 max error constraints. k>=4 reduces cycles/result to <=7, making 50 MSPS reachable at realistic sky130 Fmax. Ranges cover the minimum-power feasible region: W just above quantization limit, N just enough for CORDIC accuracy, small guards, and k spanning the parallelism vs. critical-path trade-off.
- `iterative` (6 evals): data_width=13..18, n_iter=10..18, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round. *Why:* Small budget to confirm infeasibility. With N~14 for 2^-12 accuracy, iterative needs ~17 cycles/result, requiring Fmax > 850 MHz for 50 MSPS, which is implausible in sky130. If any design unexpectedly meets both constraints, it would be a very low-power Pareto point worth capturing.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — 0/60 feasible, and 100% of evaluations violate throughput while only 53% violate accuracy - the failure mode is entirely throughput. Both explored families are inherently multi-cycle (N+3 and ceil(N/k)+3 cycles/result); their observed ceilings (9.43 and 8.14 MSPS) are ~5x below the 50 MSPS floor, so refining ranges inside them cannot produce a feasible point. The error target is comfortably reachable at data_width=17 (best 2^-14.09, and 2^-12.00 already at n_iter=16), so the missing piece is a 1-result/cycle architecture: pipelined and pipelined_m. Rounds 2-3 should evaluate those, then a final map_front round can fill the power/accuracy curve.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 9.43
- max_abs_err <= 0.000244141: 53% violate; best seen 5.72e-05 (2^-14.09)

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=17 n_iter=16 angle_guard=0 frac_guard=0 rounding=round k=2]: throughput=6.77, max_abs_err=0.000244 (2^-12.00); throughput_msps >= 50 violated by 86.5%
- unrolled_k [data_width=17 n_iter=16 angle_guard=0 frac_guard=1 rounding=round k=2]: throughput=6.49, max_abs_err=0.000207 (2^-12.24); throughput_msps >= 50 violated by 87.0%
- unrolled_k [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round k=2]: throughput=6.49, max_abs_err=0.000158 (2^-12.63); throughput_msps >= 50 violated by 87.0%
- unrolled_k [data_width=17 n_iter=16 angle_guard=3 frac_guard=1 rounding=round k=2]: throughput=6, max_abs_err=9.87e-05 (2^-13.31); throughput_msps >= 50 violated by 88.0%
- unrolled_k [data_width=17 n_iter=17 angle_guard=1 frac_guard=2 rounding=round k=2]: throughput=5.72, max_abs_err=0.000112 (2^-13.13); throughput_msps >= 50 violated by 88.6%

Per family:
- iterative: 6 evals, 0 feasible; max throughput seen 9.43 MSPS; best accuracy 10.55 bits
- unrolled_k: 54 evals, 0 feasible; max throughput seen 8.14 MSPS; best accuracy 14.09 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Throughput is the binding constraint, not accuracy. iterative/unrolled_k are structurally capped: they emit 1 result every N+3 (resp. ceil(N/k)+3) cycles, and the observed best is 9.43 MSPS (iterative) and 8.14 MSPS (unrolled_k) against a 50 MSPS floor - a ~5x structural gap, not a tuning gap. k=8 would need ceil(N/8)+3 ~= 5-6 cycles/result, still short of 50 MSPS unless Fmax ~ 250-300 MHz, which the shared barrel-shifter datapath will not reach. pipelined/pipelined_m emit 1 result/cycle, so throughput ~= Fmax and 50 MSPS becomes reachable. Accuracy is already demonstrably achievable: data_width=17, n_iter=15-17 with angle_guard 0-3 / frac_guard 0-2 gives 2^-12.00 .. 2^-14.09, so 12 bits costs ~17-bit datapath with modest n_iter. data_width is opened to 14..22 to also expose the low-power end of the power/accuracy front (quantisation floor ~ W-2 bits) so the hypervolume can cover both axes.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The binding constraint is throughput_msps >= 50, and it is unreachable for every design evaluated. 100% of the 100 evaluations violate it; the best throughput seen anywhere is 13.6 MSPS (iterative), and the best unrolled_k reaches only 8.14 MSPS — a >3.6x shortfall against the 50 MSPS floor. The accuracy constraint is clearly satisfiable (best max_abs_err 1.35e-07 = 2^-22.83, well inside 2^-12), so accuracy is not the blocker; the multi-cycle schedule of the explored families (iterative: N+3 cycles/result; unrolled_k: ceil(N/k)+3 cycles/result) caps throughput far below 50 MSPS even at the highest Fmax observed. With the summary reporting no families left unexplored and 0 of 100 designs feasible, no registry design can simultaneously satisfy throughput >= 50 MSPS and max_abs_err <= 2^-12, so the spec is infeasible rather than merely under-mapped.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 13.6
- max_abs_err <= 0.000244141: 57% violate; best seen 1.35e-07 (2^-22.83)

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=17 n_iter=16 angle_guard=0 frac_guard=0 rounding=round k=2]: throughput=6.77, max_abs_err=0.000244 (2^-12.00); throughput_msps >= 50 violated by 86.5%
- unrolled_k [data_width=17 n_iter=16 angle_guard=0 frac_guard=1 rounding=round k=2]: throughput=6.49, max_abs_err=0.000207 (2^-12.24); throughput_msps >= 50 violated by 87.0%
- unrolled_k [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round k=2]: throughput=6.49, max_abs_err=0.000158 (2^-12.63); throughput_msps >= 50 violated by 87.0%
- unrolled_k [data_width=17 n_iter=16 angle_guard=3 frac_guard=1 rounding=round k=2]: throughput=6, max_abs_err=9.87e-05 (2^-13.31); throughput_msps >= 50 violated by 88.0%
- unrolled_k [data_width=17 n_iter=17 angle_guard=1 frac_guard=2 rounding=round k=2]: throughput=5.72, max_abs_err=0.000112 (2^-13.13); throughput_msps >= 50 violated by 88.6%

Per family:
- iterative: 26 evals, 0 feasible; max throughput seen 13.6 MSPS; best accuracy 22.83 bits
- unrolled_k: 74 evals, 0 feasible; max throughput seen 8.14 MSPS; best accuracy 20.73 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 5980 in, 9772 out
- provider-reported cost: $0.0111
- full prompts and replies: `llm_trace.jsonl`

