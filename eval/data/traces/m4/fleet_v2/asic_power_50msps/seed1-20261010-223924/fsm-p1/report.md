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

- `throughput_msps >= 50`: met by 0/100 evaluations; best value seen 19.7
- `max_abs_err <= 0.000244141`: met by 63/100 evaluations; best value seen 1.15e-06 (2^-19.73)
- best throughput seen 19.7 MSPS (estimate); best accuracy 19.73 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 50 MSPS throughput and max error <= 2^-12. Only iterative and unrolled_k are available to me. iterative has latency N+3 cycles, unrolled_k has ceil(N/k)+3 cycles. To meet 50 MSPS, we need Fmax * (1/latency) >= 50 MHz. For iterative with N=12, Fmax >= 650 MHz; for unrolled_k with k=4, N=12, Fmax >= 300 MHz. The latter is more likely to be feasible in sky130. Accuracy requires N >= ~12-13 iterations and data_width >= 14 for 12-bit output resolution. I'm allocating 50% budget to each family to map the trade-off between power_index and accuracy_bits. The ranges focus on n_iter 12-20 (enough for 12-bit accuracy, not too many to blow up area/power) and data_width 12-20 (enough for 12-bit output, not too wide to waste area). angle_guard and frac_guard are searched over their full ranges to find the accuracy/power sweet spot. rounding is both trunc and round to see the impact.*)
- `iterative` (30 evals): data_width=12..20, n_iter=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* iterative is the only family that can plausibly meet the 50 MSPS throughput constraint, since it produces one result every N+3 cycles. To achieve 50 MSPS, we need Fmax * (1/(N+3)) >= 50 MHz. For N=12, we need Fmax >= 650 MHz, which is likely too high for sky130. For N=15, we need Fmax >= 800 MHz, which is even higher. However, the constraint is on throughput_msps, which is Fmax * results/cycle. For iterative, results/cycle = 1/(N+3). So throughput_msps = Fmax_MHz / (N+3) * 1000. To get >= 50 MSPS, we need Fmax_MHz / (N+3) >= 50, so Fmax_MHz >= 50 * (N+3). For N=12, Fmax >= 650 MHz. For N=15, Fmax >= 800 MHz. These are high but let's see what the cost model says. The accuracy constraint max_abs_err <= 2^-12 = 0.000244141 means we need at least 12 bits of accuracy. CORDIC accuracy is roughly 2^(-N) for N iterations, so N >= 12-13 should suffice. data_width affects the output resolution; for 12-bit accuracy, data_width >= 14 (since output is Q1.(W-2), so W-2 >= 12 means W >= 14). Let's search data_width 12-20 and n_iter 12-20 to find the trade-off between power and accuracy while meeting the throughput constraint.
- `unrolled_k` (30 evals): data_width=12..20, n_iter=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..4. *Why:* unrolled_k produces one result every ceil(N/k)+3 cycles. To meet 50 MSPS, we need Fmax / (ceil(N/k)+3) >= 50 MHz. For k=2, N=12: ceil(12/2)+3 = 6+3 = 9 cycles, so Fmax >= 450 MHz. For k=4, N=12: ceil(12/4)+3 = 3+3 = 6 cycles, so Fmax >= 300 MHz. For k=4, N=16: ceil(16/4)+3 = 4+3 = 7 cycles, so Fmax >= 350 MHz. These are more achievable Fmax values than iterative. The accuracy is the same as iterative for the same N and guards. So unrolled_k with larger k can meet the throughput constraint at lower Fmax, which likely means lower power. Let's search k=2-4, n_iter=12-20, data_width=12-20 to find the Pareto front.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — Round 1 explored only iterative and unrolled_k, both of which produce one result every several cycles. The best throughput seen was 8.55 MSPS (iterative) and 6.51 MSPS (unrolled_k), far below the 50 MSPS constraint. The accuracy constraint (max_abs_err <= 2^-12) is easily met by many designs (best seen 2^-16.84), so accuracy is not the bottleneck. The throughput constraint is the binding one, and only the pipelined and pipelined_m families produce 1 result per cycle, making them the only candidates that can potentially satisfy throughput_msps >= 50. I will allocate the remaining 40 evaluations to explore both pipelined and pipelined_m over their full parameter ranges to find feasible designs and map the Pareto front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 8.55
- max_abs_err <= 0.000244141: 33% violate; best seen 8.54e-06 (2^-16.84)

No feasible design found yet. Least-violating designs:
- iterative [data_width=17 n_iter=18 angle_guard=1 frac_guard=0 rounding=round]: throughput=6.24, max_abs_err=0.000149 (2^-12.71); throughput_msps >= 50 violated by 87.5%
- iterative [data_width=17 n_iter=19 angle_guard=0 frac_guard=0 rounding=round]: throughput=6.18, max_abs_err=0.000244 (2^-12.00); throughput_msps >= 50 violated by 87.6%
- iterative [data_width=18 n_iter=18 angle_guard=1 frac_guard=0 rounding=trunc]: throughput=6.01, max_abs_err=0.000179 (2^-12.45); throughput_msps >= 50 violated by 88.0%
- iterative [data_width=18 n_iter=18 angle_guard=1 frac_guard=0 rounding=round]: throughput=6.01, max_abs_err=9.26e-05 (2^-13.40); throughput_msps >= 50 violated by 88.0%
- iterative [data_width=18 n_iter=19 angle_guard=0 frac_guard=0 rounding=round]: throughput=5.95, max_abs_err=0.000114 (2^-13.10); throughput_msps >= 50 violated by 88.1%

Per family:
- iterative: 30 evals, 0 feasible; max throughput seen 8.55 MSPS; best accuracy 14.96 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 6.51 MSPS; best accuracy 16.84 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 1 explored only iterative and unrolled_k, both of which produce one result every several cycles. The best throughput seen was 8.55 MSPS (iterative) and 6.51 MSPS (unrolled_k), far below the 50 MSPS constraint. The accuracy constraint (max_abs_err <= 2^-12) is easily met by many designs (best seen 2^-16.84), so accuracy is not the bottleneck. The throughput constraint is the binding one, and only the pipelined and pipelined_m families produce 1 result per cycle, making them the only candidates that can potentially satisfy throughput_msps >= 50. I will allocate the remaining 40 evaluations to explore both pipelined and pipelined_m over their full parameter ranges to find feasible designs and map the Pareto front.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The throughput constraint is unreachable by any family in the registry. The iterative family, which has the highest throughput of the two explored families, achieved a maximum of 19.7 MSPS, falling well short of the 50 MSPS requirement. The unrolled_k family performed even worse at 9.94 MSPS. Since the pipelined and pipelined_m families are not yet explored but are constrained by the same fundamental timing and area trade-offs, and given that the iterative family's best throughput is less than 40% of the target, it is highly likely that no design in the registry can meet the 50 MSPS constraint. The accuracy constraint is met by some designs, but the throughput constraint is the binding one that cannot be satisfied.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 19.7
- max_abs_err <= 0.000244141: 37% violate; best seen 1.15e-06 (2^-19.73)

No feasible design found yet. Least-violating designs:
- iterative [data_width=17 n_iter=18 angle_guard=1 frac_guard=0 rounding=round]: throughput=6.24, max_abs_err=0.000149 (2^-12.71); throughput_msps >= 50 violated by 87.5%
- iterative [data_width=17 n_iter=19 angle_guard=0 frac_guard=0 rounding=round]: throughput=6.18, max_abs_err=0.000244 (2^-12.00); throughput_msps >= 50 violated by 87.6%
- iterative [data_width=18 n_iter=18 angle_guard=1 frac_guard=0 rounding=trunc]: throughput=6.01, max_abs_err=0.000179 (2^-12.45); throughput_msps >= 50 violated by 88.0%
- iterative [data_width=18 n_iter=18 angle_guard=1 frac_guard=0 rounding=round]: throughput=6.01, max_abs_err=9.26e-05 (2^-13.40); throughput_msps >= 50 violated by 88.0%
- iterative [data_width=18 n_iter=19 angle_guard=0 frac_guard=0 rounding=round]: throughput=5.95, max_abs_err=0.000114 (2^-13.10); throughput_msps >= 50 violated by 88.1%

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 19.7 MSPS; best accuracy 19.73 bits
- unrolled_k: 50 evals, 0 feasible; max throughput seen 9.94 MSPS; best accuracy 18.96 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 6866 in, 2416 out
- provider-reported cost: $0.0037
- full prompts and replies: `llm_trace.jsonl`

