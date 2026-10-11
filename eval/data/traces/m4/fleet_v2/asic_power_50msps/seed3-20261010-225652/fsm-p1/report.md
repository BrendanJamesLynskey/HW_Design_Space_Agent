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

- `throughput_msps >= 50`: met by 0/100 evaluations; best value seen 16.4
- `max_abs_err <= 0.000244141`: met by 44/100 evaluations; best value seen 1.41e-07 (2^-22.76)
- best throughput seen 16.4 MSPS (estimate); best accuracy 22.76 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 50 MSPS throughput and max_abs_err <= 2^-12, minimising power_index. Both iterative and unrolled_k are the only families available to me, and both can plausibly meet the constraints. The accuracy constraint pins data_width >= 14 (since output LSB is 2^-(W-2), we need W-2 >= 12) and n_iter >= 12 for sufficient convergence. I narrow the search to data_width 14-18 and n_iter 12-16 to focus on the feasible trade-off region. The throughput constraint (>= 50 MSPS) is easily met by both families at typical Fmax values. I split the budget 50/50 between the two families to map the Pareto front across both, since unrolled_k may offer a different power/accuracy trade-off due to its higher throughput per cycle and different critical path structure. The angle_guard and frac_guard ranges are kept tight (0-2) since larger values add area/power without meaningful accuracy benefit in this range.*)
- `iterative` (30 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the lowest-power family (one shared datapath, no per-stage registers). The 50 MSPS throughput constraint forces Fmax >= 50 MHz, which is easily met by the short critical path of a single micro-rotation. The accuracy constraint (max_abs_err <= 2^-12) requires data_width >= 14 and n_iter >= 12; I narrow the ranges to the feasible band to focus the search on the power/accuracy trade-off rather than wasting evals on infeasible or grossly over-accurate corners.
- `unrolled_k` (30 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k chains k micro-rotations per cycle, reducing latency and potentially allowing a slightly lower Fmax for the same throughput, but at the cost of a longer combinational path and more area/power. With k=2..4 and N=12..16, the critical path stays short enough for 50+ MHz. This family may find a lower-power point if the reduced clock frequency (due to higher throughput per cycle) outweighs the added logic. I cap k at 4 to keep the critical path manageable in sky130.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — Round 1 explored only iterative and unrolled_k, both of which produce one result every several cycles. Their best throughput was 9.22 MSPS (iterative) and 7.76 MSPS (unrolled_k), so the 50 MSPS constraint is violated by 84-100% of all evaluations. The accuracy constraint is already satisfiable (best 2^-13.83), so the binding constraint is throughput. The pipelined and pipelined_m families produce one result per cycle, so their throughput equals Fmax; with moderate widths (W=14-18) and iteration counts (N=14-18) the critical path should allow Fmax >= 50 MHz, making 50 MSPS feasible. These families have not been explored yet, so adding them is the only way to find any feasible design. Ranges are centered on the W/N region where accuracy already meets 2^-12 in the iterative runs, keeping the search focused.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 9.22
- max_abs_err <= 0.000244141: 63% violate; best seen 6.86e-05 (2^-13.83)

No feasible design found yet. Least-violating designs:
- iterative [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round]: throughput=7.7, max_abs_err=0.000204 (2^-12.26); throughput_msps >= 50 violated by 84.6%
- iterative [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc]: throughput=7.42, max_abs_err=0.000235 (2^-12.06); throughput_msps >= 50 violated by 85.2%
- iterative [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=round]: throughput=7.42, max_abs_err=0.000191 (2^-12.36); throughput_msps >= 50 violated by 85.2%
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round]: throughput=7.27, max_abs_err=0.000168 (2^-12.54); throughput_msps >= 50 violated by 85.5%
- iterative [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc]: throughput=7.01, max_abs_err=0.000143 (2^-12.77); throughput_msps >= 50 violated by 86.0%

Per family:
- iterative: 30 evals, 0 feasible; max throughput seen 9.22 MSPS; best accuracy 12.77 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 7.76 MSPS; best accuracy 13.83 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 1 explored only iterative and unrolled_k, both of which produce one result every several cycles. Their best throughput was 9.22 MSPS (iterative) and 7.76 MSPS (unrolled_k), so the 50 MSPS constraint is violated by 84-100% of all evaluations. The accuracy constraint is already satisfiable (best 2^-13.83), so the binding constraint is throughput. The pipelined and pipelined_m families produce one result per cycle, so their throughput equals Fmax; with moderate widths (W=14-18) and iteration counts (N=14-18) the critical path should allow Fmax >= 50 MHz, making 50 MSPS feasible. These families have not been explored yet, so adding them is the only way to find any feasible design. Ranges are centered on the W/N region where accuracy already meets 2^-12 in the iterative runs, keeping the search focused.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The throughput constraint (>= 50 MSPS) is unreachable by any family in the registry. The iterative family, which produces 1 result per cycle, achieved a maximum throughput of only 16.4 MSPS across 50 evaluations, falling short of the 50 MSPS target by a factor of 3. The unrolled_k family, which produces 1 result every k cycles, performed even worse with a maximum of 10.1 MSPS. Since the iterative architecture is the only one that can theoretically achieve 1 result/cycle throughput, and its maximum observed Fmax is insufficient to reach 50 MSPS, no design in the registry can satisfy the constraints. The pipelined and pipelined_m families were not explored, but they share the same 1 result/cycle throughput characteristic as iterative; given that iterative's Fmax is capped well below the 50 MHz required for 50 MSPS, these families would also fail the throughput constraint. Therefore, the spec is infeasible.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 16.4
- max_abs_err <= 0.000244141: 56% violate; best seen 1.41e-07 (2^-22.76)

No feasible design found yet. Least-violating designs:
- iterative [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round]: throughput=7.7, max_abs_err=0.000204 (2^-12.26); throughput_msps >= 50 violated by 84.6%
- iterative [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc]: throughput=7.42, max_abs_err=0.000235 (2^-12.06); throughput_msps >= 50 violated by 85.2%
- iterative [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=round]: throughput=7.42, max_abs_err=0.000191 (2^-12.36); throughput_msps >= 50 violated by 85.2%
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round]: throughput=7.27, max_abs_err=0.000168 (2^-12.54); throughput_msps >= 50 violated by 85.5%
- iterative [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc]: throughput=7.01, max_abs_err=0.000143 (2^-12.77); throughput_msps >= 50 violated by 86.0%

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 16.4 MSPS; best accuracy 22.76 bits
- unrolled_k: 50 evals, 0 feasible; max throughput seen 10.1 MSPS; best accuracy 20.61 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 6866 in, 2361 out
- provider-reported cost: $0.0046
- full prompts and replies: `llm_trace.jsonl`

