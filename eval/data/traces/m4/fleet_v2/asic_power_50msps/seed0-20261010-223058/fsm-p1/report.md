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

- `throughput_msps >= 50`: met by 0/100 evaluations; best value seen 16.1
- `max_abs_err <= 0.000244141`: met by 31/100 evaluations; best value seen 5.51e-08 (2^-24.11)
- best throughput seen 16.1 MSPS (estimate); best accuracy 24.11 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands 50 MSPS throughput with max_abs_err <= 2^-12, minimising power_index. Only iterative and unrolled_k are available to me, and both are shared-datapath (low power) families, so the whole budget goes to them. The binding tension is throughput: iterative needs Fmax ~ 50*(N+3) MHz, which is very high for sky130 sc_hd, while unrolled_k relaxes this to 50*(ceil(N/k)+3) MHz. I therefore give iterative the larger share (0.55) because it is the lowest-power family and I want to confirm whether any point on it can meet throughput at all (if not, the front collapses to unrolled_k), and unrolled_k 0.45 to map the k-vs-Fmax trade-off that is most likely to yield feasible, low-power designs. Accuracy ranges (n_iter 12..16, data_width 14..18, both guards, both roundings) are kept identical across families so the merged front reflects a true power-vs-accuracy trade-off rather than an artefact of different search boxes. I deliberately cap n_iter at 16 and data_width at 18: beyond that, accuracy is already well past 2^-12 and only power/area grow, so the hypervolume gain is negligible and the budget is better spent resolving the throughput-feasibility boundary.*)
- `iterative` (33 evals): data_width=14..18, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* iterative is the lowest-power family (single shared datapath, no per-stage registers), so it is the only candidate that can plausibly minimise power_index. It produces 1 result per (N+3) cycles, so to hit 50 MSPS it needs Fmax >= 50*(N+3) MHz; with N in 12..16 that is 750..1000 MHz, which is far beyond sky130 sc_hd, so the throughput constraint will force the search to the low-N end of the range. I keep n_iter 12..16 so the accuracy constraint (max_abs_err <= 2^-12) is still reachable while the cost model can find the smallest N that satisfies it; data_width 14..18 and the guard bits give the accuracy trade-off room, and both rounding modes are kept since rounding can change the achievable accuracy_bits at a given N.
- `unrolled_k` (27 evals): data_width=14..18, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* unrolled_k chains k micro-rotations per cycle, so it needs only Fmax >= 50*(ceil(N/k)+3) MHz. With k up to 8 and N 12..16, the required Fmax drops to roughly 350..550 MHz, which is much more realistic for sky130 sc_hd than the iterative case. This makes unrolled_k the family most likely to actually satisfy the 50 MSPS throughput constraint while keeping power low (still a shared datapath, just wider combinational logic). I keep the same accuracy-relevant ranges as iterative so the two fronts are directly comparable, and let k span 2..8 so the search can trade off the required Fmax against the added combinational depth (which raises power_index and lowers Fmax).

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The throughput constraint (>= 50 MSPS) is the hard blocker. The iterative and unrolled_k families are fundamentally limited by their serial or partially-parallel execution models; even with aggressive unrolling (k=3) and high Fmax estimates, the best observed throughput was only 9.07 MSPS, which is more than 5x below the 50 MSPS requirement. The pipelined and pipelined_m families are the only architectures in the registry capable of achieving 1 result/cycle throughput, which is necessary to meet the 50 MSPS target at reasonable clock frequencies. Therefore, I must explore the pipelined families to find any feasible designs.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 9.07
- max_abs_err <= 0.000244141: 78% violate; best seen 5.18e-05 (2^-14.24)

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=14 angle_guard=3 frac_guard=2 rounding=round]: throughput=7.42, max_abs_err=0.000189 (2^-12.37); throughput_msps >= 50 violated by 85.2%
- iterative [data_width=17 n_iter=16 angle_guard=4 frac_guard=1 rounding=round]: throughput=6.2, max_abs_err=9.87e-05 (2^-13.31); throughput_msps >= 50 violated by 87.6%
- iterative [data_width=17 n_iter=16 angle_guard=4 frac_guard=4 rounding=round]: throughput=6.2, max_abs_err=5.18e-05 (2^-14.24); throughput_msps >= 50 violated by 87.6%
- unrolled_k [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round k=3]: throughput=5.66, max_abs_err=0.000109 (2^-13.17); throughput_msps >= 50 violated by 88.7%
- unrolled_k [data_width=18 n_iter=15 angle_guard=2 frac_guard=4 rounding=round k=3]: throughput=5.25, max_abs_err=7.86e-05 (2^-13.63); throughput_msps >= 50 violated by 89.5%

Per family:
- iterative: 33 evals, 0 feasible; max throughput seen 9.07 MSPS; best accuracy 14.24 bits
- unrolled_k: 27 evals, 0 feasible; max throughput seen 7.07 MSPS; best accuracy 13.79 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Exploring pipelined and pipelined_m is essential to meet the 50 MSPS throughput constraint. The ranges are narrowed around the accuracy sweet spots identified in Round 1 (data_width 16-18, n_iter 14-16) to ensure the accuracy constraint is met while allowing the optimizer to find the highest Fmax/lowest power configurations.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The throughput constraint (>= 50 MSPS) is unreachable with the explored families. The iterative and unrolled_k architectures are latency-bound (N+3 and ceil(N/k)+3 cycles respectively), resulting in a maximum observed throughput of only 16.1 MSPS (unrolled_k) and 11.5 MSPS (iterative). This is a factor of ~3-4x below the required 50 MSPS. To achieve 50 MSPS, a pipelined architecture (1 result/cycle) is required, but the pipelined and pipelined_m families have not been explored in the 100 evaluations used so far. Since this is the final round and no feasible design has been found, and the current best throughput is far from the target, the spec is infeasible within the current exploration scope and budget.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 16.1
- max_abs_err <= 0.000244141: 69% violate; best seen 5.51e-08 (2^-24.11)

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=14 angle_guard=3 frac_guard=2 rounding=round]: throughput=7.42, max_abs_err=0.000189 (2^-12.37); throughput_msps >= 50 violated by 85.2%
- iterative [data_width=17 n_iter=16 angle_guard=4 frac_guard=1 rounding=round]: throughput=6.2, max_abs_err=9.87e-05 (2^-13.31); throughput_msps >= 50 violated by 87.6%
- iterative [data_width=17 n_iter=16 angle_guard=4 frac_guard=4 rounding=round]: throughput=6.2, max_abs_err=5.18e-05 (2^-14.24); throughput_msps >= 50 violated by 87.6%
- unrolled_k [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round k=3]: throughput=5.66, max_abs_err=0.000109 (2^-13.17); throughput_msps >= 50 violated by 88.7%
- unrolled_k [data_width=18 n_iter=15 angle_guard=2 frac_guard=4 rounding=round k=3]: throughput=5.25, max_abs_err=7.86e-05 (2^-13.63); throughput_msps >= 50 violated by 89.5%

Per family:
- iterative: 53 evals, 0 feasible; max throughput seen 11.5 MSPS; best accuracy 19.70 bits
- unrolled_k: 47 evals, 0 feasible; max throughput seen 16.1 MSPS; best accuracy 24.11 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 6161 in, 2374 out
- provider-reported cost: $0.0046
- full prompts and replies: `llm_trace.jsonl`

