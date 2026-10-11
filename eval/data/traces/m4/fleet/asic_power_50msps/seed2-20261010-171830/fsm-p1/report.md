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
- `max_abs_err <= 0.000244141`: met by 47/100 evaluations; best value seen 1.35e-07 (2^-22.83)
- best throughput seen 13.6 MSPS (estimate); best accuracy 22.83 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec's hard constraints are throughput >= 50 MSPS and max_abs_err <= 2^-12, with the objective to minimise power_index (accuracy as the trade-off). Among my two assigned families, iterative is the natural power-minimiser: one shared datapath, no pipeline registers, no parallel adder tree, so it should have the lowest power_index and the highest Fmax per area. unrolled_k is strictly heavier (k parallel micro-rotations per cycle plus a shared FSM) and its throughput is throttled by ceil(N/k)+3 cycles/result, so it can only win if its higher Fmax compensates; I keep it in the search to verify that and to cover the accuracy end of the front. I focus the ranges on the accuracy boundary: data_width 14-18 and n_iter 14-20 span the minimal corner that just clears 2^-12 up to a comfortable margin, while angle_guard (-2..2) and frac_guard (0..2) let Optuna trade guard-bit area against accuracy. Rounding is left to both options since it shifts accuracy by ~1 LSB at negligible cost. I do not push data_width/n_iter to their registry maxima (28/30) because that would waste budget on points that are far above the accuracy constraint and only increase power, which the objective penalises. The 50 MSPS throughput constraint is the binding one for unrolled_k, so I keep k modest (2-4) to keep Fmax high enough that Fmax/(ceil(N/k)+3) can still reach 50.*)
- `iterative` (30 evals): data_width=14..18, n_iter=14..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the lowest-power family (single shared datapath, no per-stage registers, no k-way parallel adders). It is the only family that can plausibly minimise power_index while meeting the 2^-12 accuracy constraint. data_width 14-18 and n_iter 14-20 bracket the accuracy boundary (need ~12+ bits, so W=14/N=14 is the minimal corner, W=18/N=20 gives margin); angle_guard -2..2 and frac_guard 0..2 let the search trade guard-bit area against accuracy. Throughput is Fmax (1 result/cycle), so Fmax must reach 50 MHz, which the small iterative datapath should achieve.
- `unrolled_k` (30 evals): data_width=14..18, n_iter=14..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k produces 1 result every ceil(N/k)+3 cycles, so throughput = Fmax/(ceil(N/k)+3). To hit 50 MSPS it needs a higher Fmax than iterative, and the k-way parallel adder tree raises both area and power. It is therefore a secondary candidate: useful to confirm whether any (k, W, N) point beats the iterative front on power while still meeting throughput, and to populate the accuracy side of the Pareto front. k capped at 4 to keep the parallel adder tree (and hence power) from exploding; data_width/n_iter/guards mirror iterative so the accuracy trade-off is comparable.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The iterative and unrolled_k families are fundamentally incapable of meeting the throughput constraint. The best throughput observed was 8.68 MSPS (iterative), which is less than 1/5th of the required 50 MSPS. Since these architectures produce one result every N+3 or ceil(N/k)+3 cycles respectively, their throughput is inherently limited by the number of iterations required for accuracy (N >= 14-15 to meet the error constraint). To achieve 50 MSPS, we need an architecture that produces one result per cycle. The 'pipelined' and 'pipelined_m' families are the only ones in the registry that offer 1 result/cycle throughput. Therefore, we must explore these families to find a feasible design.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 8.68
- max_abs_err <= 0.000244141: 47% violate; best seen 5.02e-05 (2^-14.28)

No feasible design found yet. Least-violating designs:
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round]: throughput=7.27, max_abs_err=0.000158 (2^-12.63); throughput_msps >= 50 violated by 85.5%
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round]: throughput=7.27, max_abs_err=0.000168 (2^-12.54); throughput_msps >= 50 violated by 85.5%
- iterative [data_width=17 n_iter=16 angle_guard=1 frac_guard=1 rounding=round]: throughput=6.89, max_abs_err=0.000128 (2^-12.94); throughput_msps >= 50 violated by 86.2%
- iterative [data_width=17 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc]: throughput=6.89, max_abs_err=0.000222 (2^-12.13); throughput_msps >= 50 violated by 86.2%
- iterative [data_width=16 n_iter=17 angle_guard=1 frac_guard=2 rounding=round]: throughput=6.55, max_abs_err=0.0002 (2^-12.29); throughput_msps >= 50 violated by 86.9%

Per family:
- iterative: 30 evals, 0 feasible; max throughput seen 8.68 MSPS; best accuracy 14.28 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 8.14 MSPS; best accuracy 12.86 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Switching to pipelined architectures is essential to meet the throughput constraint. We maintain accuracy-focused parameter ranges based on Round 1 findings.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The throughput constraint is unreachable for the non-pipelined families explored: iterative peaked at 13.6 MSPS and unrolled_k at 8.14 MSPS, both far below the 50 MSPS requirement, and 100% of evaluations violated it. The pipelined and pipelined_m families, which are the only registry families capable of 1 result/cycle and thus 50+ MSPS, were never explored, so no feasible design exists in the evaluated set. Since this is the final round and no feasible design was found, the constraints cannot be confirmed as met by any evaluated design.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 13.6
- max_abs_err <= 0.000244141: 53% violate; best seen 1.35e-07 (2^-22.83)

No feasible design found yet. Least-violating designs:
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round]: throughput=7.27, max_abs_err=0.000158 (2^-12.63); throughput_msps >= 50 violated by 85.5%
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round]: throughput=7.27, max_abs_err=0.000168 (2^-12.54); throughput_msps >= 50 violated by 85.5%
- iterative [data_width=17 n_iter=16 angle_guard=1 frac_guard=1 rounding=round]: throughput=6.89, max_abs_err=0.000128 (2^-12.94); throughput_msps >= 50 violated by 86.2%
- iterative [data_width=17 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc]: throughput=6.89, max_abs_err=0.000222 (2^-12.13); throughput_msps >= 50 violated by 86.2%
- iterative [data_width=16 n_iter=17 angle_guard=1 frac_guard=2 rounding=round]: throughput=6.55, max_abs_err=0.0002 (2^-12.29); throughput_msps >= 50 violated by 86.9%

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 13.6 MSPS; best accuracy 22.83 bits
- unrolled_k: 50 evals, 0 feasible; max throughput seen 8.14 MSPS; best accuracy 20.73 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 6862 in, 2099 out
- provider-reported cost: $0.0049
- full prompts and replies: `llm_trace.jsonl`

