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

- `throughput_msps >= 50`: met by 0/100 evaluations; best value seen 11.8
- `max_abs_err <= 0.000244141`: met by 45/100 evaluations; best value seen 2.99e-07 (2^-21.67)
- best throughput seen 11.8 MSPS (estimate); best accuracy 21.67 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec minimises power_index subject to throughput>=50 MSPS and max_abs_err<=2^-12, with accuracy as the trade-off. Of the families I may use, iterative is the power floor (shared datapath, no parallelism, no per-stage registers) and unrolled_k is the next-cheapest (k-way parallelism, shared FSM). Both can plausibly meet 50 MSPS: iterative via a high Fmax with modest N, unrolled_k via k>1 shortening the result period. I therefore split the budget evenly between them so the merged front covers the full power-vs-accuracy trade-off rather than a single corner. Ranges are narrowed to where the constraints bind: W 14..20 (W<14 cannot reach 2^-12 accuracy; W>20 adds area/power with no accuracy benefit once N is sufficient), N 10..20 (N<10 risks missing 2^-12; N>20 lowers Fmax and raises latency with no accuracy gain), angle_guard -1..2 and frac_guard 0..2 (small guards keep the datapath narrow for power while still giving the accuracy headroom), and rounding over both choices since round typically buys accuracy at a small power cost. k is limited to 2..4 for unrolled_k to stay in the region where parallelism helps throughput without dominating power. This focuses the 100-eval budget on the feasible, constraint-relevant part of the space so the hypervolume is spent mapping the actual trade-off curve.*)
- `iterative` (30 evals): data_width=14..20, n_iter=10..20, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the lowest-power family (single datapath, no per-stage registers, no k-way parallelism). It is the only family that can plausibly minimise power_index while still meeting 50 MSPS, since its throughput is Fmax/(N+3). To hit 50 MSPS it needs a high Fmax, which argues for keeping N modest (10..20) and the datapath narrow (W 14..20). The accuracy constraint (<=2^-12) is met by W>=14 with N>=10 and round; the W/N/guard trade-off is exactly the power-vs-accuracy curve the spec wants mapped, so I focus the budget here.
- `unrolled_k` (30 evals): data_width=14..20, n_iter=10..20, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k raises throughput to Fmax/(ceil(N/k)+3) at the cost of k-way parallel datapath area and power. It is the second-cheapest family and gives a different point on the power-vs-accuracy/throughput curve: for the same accuracy (same W/N/guard) it trades extra power for higher Fmax margin, which can let it meet 50 MSPS at a lower clock (lower power_index) than iterative, or vice-versa. k is capped at 4 because beyond that the parallel area/power grows faster than the latency benefit, so the interesting trade-off lives at k=2..4. Same W/N/guard ranges as iterative so the two fronts are directly comparable on accuracy.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The 50 MSPS throughput constraint is the binding one: iterative peaked at 11.8 MSPS and unrolled_k at 7.02 MSPS, both far short of 50. Only the pipelined families produce one result per cycle, making throughput = Fmax, which is the only path to satisfying throughput_msps >= 50. Accuracy is already achievable (best seen 15.69 bits vs required 12 bits), so the search should focus on pipelined and pipelined_m with data_width 14-20 and n_iter 12-30 to find low-power designs that meet both constraints. Splitting the budget evenly between the two pipelined families lets us compare the power/area trade-off of full vs partial pipelining.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 11.8
- max_abs_err <= 0.000244141: 50% violate; best seen 1.89e-05 (2^-15.69)

No feasible design found yet. Least-violating designs:
- iterative [data_width=18 n_iter=15 angle_guard=-1 frac_guard=0 rounding=round]: throughput=7.27, max_abs_err=0.000201 (2^-12.28); throughput_msps >= 50 violated by 85.5%
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round]: throughput=7.27, max_abs_err=0.00018 (2^-12.44); throughput_msps >= 50 violated by 85.5%
- iterative [data_width=18 n_iter=15 angle_guard=-1 frac_guard=1 rounding=round]: throughput=7.01, max_abs_err=0.000196 (2^-12.31); throughput_msps >= 50 violated by 86.0%
- iterative [data_width=18 n_iter=15 angle_guard=-1 frac_guard=1 rounding=trunc]: throughput=7.01, max_abs_err=0.000194 (2^-12.33); throughput_msps >= 50 violated by 86.0%
- iterative [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=trunc]: throughput=6.77, max_abs_err=0.000194 (2^-12.33); throughput_msps >= 50 violated by 86.5%

Per family:
- iterative: 30 evals, 0 feasible; max throughput seen 11.8 MSPS; best accuracy 15.69 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 7.02 MSPS; best accuracy 13.50 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The 50 MSPS throughput constraint is the binding one: iterative peaked at 11.8 MSPS and unrolled_k at 7.02 MSPS, both far short of 50. Only the pipelined families produce one result per cycle, making throughput = Fmax, which is the only path to satisfying throughput_msps >= 50. Accuracy is already achievable (best seen 15.69 bits vs required 12 bits), so the search should focus on pipelined and pipelined_m with data_width 14-20 and n_iter 12-30 to find low-power designs that meet both constraints. Splitting the budget evenly between the two pipelined families lets us compare the power/area trade-off of full vs partial pipelining.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The throughput constraint is unreachable: iterative and unrolled_k produce one result every several cycles, so their maximum observed throughput is 11.8 and 10.9 MSPS respectively, far below the 50 MSPS requirement. The only families that can achieve 1 result/cycle (pipelined, pipelined_m) have not been explored, but the budget is exhausted (100/100 evals, round 4/4). Since no feasible design was found and the throughput constraint cannot be met by the explored families, the spec is infeasible within the given budget and registry.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 11.8
- max_abs_err <= 0.000244141: 55% violate; best seen 2.99e-07 (2^-21.67)

No feasible design found yet. Least-violating designs:
- iterative [data_width=18 n_iter=15 angle_guard=-1 frac_guard=0 rounding=round]: throughput=7.27, max_abs_err=0.000201 (2^-12.28); throughput_msps >= 50 violated by 85.5%
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round]: throughput=7.27, max_abs_err=0.00018 (2^-12.44); throughput_msps >= 50 violated by 85.5%
- iterative [data_width=18 n_iter=15 angle_guard=-1 frac_guard=1 rounding=round]: throughput=7.01, max_abs_err=0.000196 (2^-12.31); throughput_msps >= 50 violated by 86.0%
- iterative [data_width=18 n_iter=15 angle_guard=-1 frac_guard=1 rounding=trunc]: throughput=7.01, max_abs_err=0.000194 (2^-12.33); throughput_msps >= 50 violated by 86.0%
- iterative [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=trunc]: throughput=6.77, max_abs_err=0.000194 (2^-12.33); throughput_msps >= 50 violated by 86.5%

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 11.8 MSPS; best accuracy 21.67 bits
- unrolled_k: 50 evals, 0 feasible; max throughput seen 10.9 MSPS; best accuracy 14.73 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 6866 in, 2452 out
- provider-reported cost: $0.0050
- full prompts and replies: `llm_trace.jsonl`

