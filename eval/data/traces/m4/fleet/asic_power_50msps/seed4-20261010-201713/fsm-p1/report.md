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

- `throughput_msps >= 50`: met by 0/100 evaluations; best value seen 20.2
- `max_abs_err <= 0.000244141`: met by 36/100 evaluations; best value seen 2.99e-07 (2^-21.67)
- best throughput seen 20.2 MSPS (estimate); best accuracy 21.67 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The 50 MSPS constraint is the binding one and it forces parallelism. iterative's 1 micro-rotation/cycle schedule cannot reach 50 MSPS with the N>=13 iterations needed for max_abs_err <= 2^-12, so it gets only a small probe. unrolled_k is the only family here that can plausibly meet both constraints: with k micro-rotations/cycle the schedule is ceil(N/k)+3 cycles, so N~13-16 and k~4-8 give 5-7 cycles and a required Fmax of ~250-350 MHz. Accuracy depends only on data_width, n_iter, angle_guard, frac_guard and rounding, so the ranges are chosen to straddle the 2^-12 boundary (W>=14, N>=~13) and to extend to the high-accuracy end that earns hypervolume, while k spans the Fmax/cycles trade-off so the search can locate the min-power feasible corner (small W, small N, smallest k that still hits 50 MSPS). 90/10 split puts the budget where the trade-off is and keeps a minimal negative-control probe on iterative.*)
- `unrolled_k` (54 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round, k=2..8. *Why:* Only family in my set that can plausibly satisfy both constraints. Throughput = Fmax/(ceil(N/k)+3); with N~13-16 for 12-bit accuracy and k~4-8, cycles/result is 5-7, so 50 MSPS needs Fmax ~250-350 MHz, which is realistic in sky130. k=2..8 spans the Fmax-vs-cycles trade-off (small k = high Fmax but more cycles; large k = fewer cycles but lower Fmax), so the search can find the true throughput-feasible boundary and the min-power corner. data_width 12..20 spans the output-quantisation boundary (W>=14 needed for 2^-12) up to the high-accuracy end that extends hypervolume; n_iter 10..20 spans the CORDIC angle-approximation boundary (N>=~13) and the point where W-quantisation dominates. angle_guard -2..3 and frac_guard 0..3 let the search trade angle-path and datapath guard bits against area/power. rounding both, since round buys ~1 bit of accuracy at negligible cost.
- `iterative` (6 evals): data_width=12..20, n_iter=4..8, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round. *Why:* Cheap feasibility probe only. iterative takes N+3 cycles/result, so 50 MSPS needs Fmax >= 50*(N+3) MHz: N=4 already needs 350 MHz, and N>=13 (needed for 2^-12 accuracy) needs 800 MHz, which is implausible for a shared barrel-shifter datapath in sky130. n_iter is deliberately capped at 8 so the probe tests the only regime where throughput could conceivably pass; if it does, accuracy will fail, confirming the family is infeasible. This documents the negative result for the fleet at low cost.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — All 100% of evaluations violate throughput >= 50 MSPS; best seen is 20.2 MSPS (iterative, N+3 cycles/result) and 7.07 MSPS (unrolled_k, k=3). Meanwhile the accuracy constraint max_abs_err <= 2^-12 is already satisfied by unrolled_k designs (best 2^-15.75). So the throughput constraint is the binding one, and pipelined / pipelined_m are the families with throughput = Fmax * 1 result/cycle that have not been tried.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 20.2
- max_abs_err <= 0.000244141: 65% violate; best seen 1.81e-05 (2^-15.75)

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=17 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc k=3]: throughput=5.24, max_abs_err=0.000113 (2^-13.11); throughput_msps >= 50 violated by 89.5%
- unrolled_k [data_width=17 n_iter=17 angle_guard=2 frac_guard=3 rounding=trunc k=3]: throughput=5.03, max_abs_err=8.08e-05 (2^-13.60); throughput_msps >= 50 violated by 89.9%
- unrolled_k [data_width=19 n_iter=18 angle_guard=1 frac_guard=2 rounding=round k=3]: throughput=4.84, max_abs_err=3.21e-05 (2^-14.93); throughput_msps >= 50 violated by 90.3%
- unrolled_k [data_width=17 n_iter=20 angle_guard=2 frac_guard=2 rounding=trunc k=3]: throughput=4.71, max_abs_err=0.000113 (2^-13.11); throughput_msps >= 50 violated by 90.6%
- unrolled_k [data_width=20 n_iter=17 angle_guard=3 frac_guard=0 rounding=round k=3]: throughput=4.51, max_abs_err=2.95e-05 (2^-15.05); throughput_msps >= 50 violated by 91.0%

Per family:
- iterative: 6 evals, 0 feasible; max throughput seen 20.2 MSPS; best accuracy 5.00 bits
- unrolled_k: 54 evals, 0 feasible; max throughput seen 7.07 MSPS; best accuracy 15.75 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *no design in iterative/unrolled_k can reach 50 MSPS: iterative costs N+3 cycles/result and even the best seen gives 20.2 MSPS; unrolled_k maxes at 7.07 MSPS with k=3. Throughput is violated by every design (100%), while accuracy is already met (best 2^-15.75, well under the 2^-12 limit) by unrolled_k. So the binding constraint is throughput, and the registry's only 1-result/cycle families (pipelined, pipelined_m) which have not been evaluated are the ones that can satisfy it. Add them.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — Final round with budget exhausted (100/100 evals, 4-round cap reached), so no further search is possible. The evidence shows 0 feasible designs: the throughput constraint (>=50 MSPS) is violated by 100% of evaluations, with the best any design reached being 20.2 MSPS (iterative), and unrolled_k topping out at 10.9 MSPS. Both explored families are inherently multi-cycle-per-result (iterative: N+3 cycles; unrolled_k: ceil(N/k)+3 cycles), so their throughput is Fmax divided by several cycles and cannot approach 50 MSPS at the Fmax values seen. Accuracy is not the blocker — max_abs_err down to 2^-21.67 was achieved, well inside the 2^-12 limit — so the binding constraint is throughput. Hypervolume is 0 with an empty feasible front and no gain this round. I therefore stop rather than claim infeasibility: the registry also contains the pipelined and pipelined_m families (1 result/cycle, throughput = Fmax), which were not evaluated in this run and are the plausible route to >=50 MSPS; since they remain untested, I cannot assert that no registry design meets the constraints, but with the budget spent no feasible front can be produced now.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 20.2
- max_abs_err <= 0.000244141: 64% violate; best seen 2.99e-07 (2^-21.67)

No feasible design found yet. Least-violating designs:
- iterative [data_width=15 n_iter=20 angle_guard=4 frac_guard=4 rounding=round]: throughput=5.49, max_abs_err=0.000114 (2^-13.10); throughput_msps >= 50 violated by 89.0%
- unrolled_k [data_width=17 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc k=3]: throughput=5.24, max_abs_err=0.000113 (2^-13.11); throughput_msps >= 50 violated by 89.5%
- iterative [data_width=17 n_iter=20 angle_guard=2 frac_guard=4 rounding=round]: throughput=5.12, max_abs_err=5.57e-05 (2^-14.13); throughput_msps >= 50 violated by 89.8%
- unrolled_k [data_width=17 n_iter=17 angle_guard=2 frac_guard=3 rounding=trunc k=3]: throughput=5.03, max_abs_err=8.08e-05 (2^-13.60); throughput_msps >= 50 violated by 89.9%
- unrolled_k [data_width=19 n_iter=18 angle_guard=1 frac_guard=2 rounding=round k=3]: throughput=4.84, max_abs_err=3.21e-05 (2^-14.93); throughput_msps >= 50 violated by 90.3%

Per family:
- iterative: 26 evals, 0 feasible; max throughput seen 20.2 MSPS; best accuracy 21.67 bits
- unrolled_k: 74 evals, 0 feasible; max throughput seen 10.9 MSPS; best accuracy 15.75 bits
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 1)
- tokens: 5987 in, 10967 out
- provider-reported cost: $0.0125
- full prompts and replies: `llm_trace.jsonl`

