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

- `throughput_msps >= 50`: met by 0/100 evaluations; best value seen 16.1
- `max_abs_err <= 0.000244141`: met by 43/100 evaluations; best value seen 5.51e-08 (2^-24.11)
- best throughput seen 16.1 MSPS (estimate); best accuracy 24.11 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands 50 MSPS and max error <= 2^-12. Accuracy depends only on data_width, n_iter, angle_guard, frac_guard and rounding, so all families share the same accuracy trade-off. Iterative is the lowest-power family but its throughput is Fmax/(N+3); meeting 50 MSPS requires either very small N or an unrealistically high Fmax. We allocate a small budget (15%) to test the only plausible iterative corner (N=10..14, W=12..16). Unrolled_k is the main sequential family that can reach 50 MSPS by processing k micro-rotations per cycle; we allocate 85% to it, covering k=2..8 and N=10..22 to map the Pareto front between power, throughput and accuracy. The ranges are chosen to include the minimum design that can meet the constraints, so the search can find the lowest-power feasible point, while still covering enough accuracy margin to avoid missing the front.*)
- `iterative` (9 evals): data_width=12..16, n_iter=10..14, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Lowest-power family, but throughput is Fmax/(N+3). To reach 50 MSPS it needs a very high Fmax and small N. This narrow range tests the only plausible feasible corner (N=10..14) while keeping W small enough to limit area/power. If no point meets both 50 MSPS and 2^-12 error, iterative is infeasible for this spec.
- `unrolled_k` (51 evals): data_width=12..20, n_iter=10..22, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, k=2..8. *Why:* Main sequential candidate for 50 MSPS. Throughput is Fmax/(ceil(N/k)+3), so k>1 is needed to reduce cycles. The range covers k=2..8 and N=10..22, which spans the trade-off between throughput (higher k, lower N), accuracy (higher N, W, guards), and power (smaller area/frequency). W and N are kept moderate to focus on the low-power corner while still allowing enough accuracy for 2^-12.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — 

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 11.5
- max_abs_err <= 0.000244141: 58% violate; best seen 1.61e-05 (2^-15.92)

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=15 n_iter=21 angle_guard=3 frac_guard=2 rounding=round k=3]: throughput=4.91, max_abs_err=0.000192 (2^-12.35); throughput_msps >= 50 violated by 90.2%
- unrolled_k [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=round k=5]: throughput=4.83, max_abs_err=0.000179 (2^-12.45); throughput_msps >= 50 violated by 90.3%
- unrolled_k [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc k=5]: throughput=4.83, max_abs_err=0.000205 (2^-12.25); throughput_msps >= 50 violated by 90.3%
- unrolled_k [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round k=5]: throughput=4.64, max_abs_err=0.000152 (2^-12.68); throughput_msps >= 50 violated by 90.7%
- unrolled_k [data_width=18 n_iter=14 angle_guard=1 frac_guard=3 rounding=round k=5]: throughput=4.46, max_abs_err=0.00015 (2^-12.70); throughput_msps >= 50 violated by 91.1%

Per family:
- iterative: 9 evals, 0 feasible; max throughput seen 11.5 MSPS; best accuracy 9.31 bits
- unrolled_k: 51 evals, 0 feasible; max throughput seen 7.77 MSPS; best accuracy 15.92 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Every evaluation so far is a multi-cycle family and the throughput constraint is violated by 100% of designs, best only 11.5 MSPS (iterative) and 7.77 MSPS (unrolled_k). That is not a parameter-tuning failure: iterative costs N+3 cycles/result and unrolled_k ceil(N/k)+3, so even the best observed 11.5 MSPS is ~4x short of 50 MSPS and cannot be closed by width/guard tweaks. The registry's 1-result-per-cycle families (pipelined, pipelined_m) are exactly the untried options that can clear 50 MSPS, while the accuracy side is already proven reachable (best max_abs_err 2^-15.92, comfortably inside the 2^-12 limit). So the constraint is reachable only by switching family, not by refining the current ranges. Spend the remaining ~40 evals on pipelined_m (higher share, low m to control FFs/power) plus pipelined as the reference point, with data_width 12-20 and n_iter 12-22 to hold accuracy at or above the 12-bit requirement with a little margin, then map the front if a feasible region appears.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined_m', 'pipelined'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — Final round, budget exhausted (100/100 evals, HV = 0, 0 feasible designs). The only hard blocker is throughput: 100% of evaluations violate throughput_msps >= 50, and the best value seen anywhere is 16.1 MSPS (unrolled_k), a ~3.1x shortfall; the accuracy constraint is clearly reachable (best max_abs_err 5.51e-08 = 2^-24.11, far inside 2^-12). However, I cannot honestly declare `infeasible`: the registry's throughput lever is results/cycle, and the two families actually evaluated (iterative, unrolled_k) are both multi-cycle-per-result by construction, so their ~5-16 MSPS ceiling is expected and says nothing about the pipelined/pipelined_m families, which emit 1 result/cycle (throughput = Fmax) and were never evaluated in this run. With no Fmax/throughput numbers for those families in the summaries, claiming no registry design can reach 50 MSPS would be inventing evidence. So the empty front is an exploration/budget artifact, not a proven infeasibility, and the correct terminal action is `stop` rather than `infeasible`. If the loop were reopened, the decisive next step would be to evaluate pipelined and pipelined_m (1 result/cycle) with data_width ~14-18, n_iter ~12-16, angle_guard 0..3, frac_guard 0..2, rounding=round, since those are the only families whose throughput can plausibly clear 50 MSPS while holding max_abs_err <= 2^-12.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 16.1
- max_abs_err <= 0.000244141: 57% violate; best seen 5.51e-08 (2^-24.11)

No feasible design found yet. Least-violating designs:
- iterative [data_width=23 n_iter=18 angle_guard=-2 frac_guard=1 rounding=trunc]: throughput=5.09, max_abs_err=1.68e-05 (2^-15.86); throughput_msps >= 50 violated by 89.8%
- iterative [data_width=24 n_iter=18 angle_guard=-2 frac_guard=0 rounding=round]: throughput=5.09, max_abs_err=1.21e-05 (2^-16.33); throughput_msps >= 50 violated by 89.8%
- unrolled_k [data_width=15 n_iter=21 angle_guard=3 frac_guard=2 rounding=round k=3]: throughput=4.91, max_abs_err=0.000192 (2^-12.35); throughput_msps >= 50 violated by 90.2%
- unrolled_k [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=round k=5]: throughput=4.83, max_abs_err=0.000179 (2^-12.45); throughput_msps >= 50 violated by 90.3%
- unrolled_k [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc k=5]: throughput=4.83, max_abs_err=0.000205 (2^-12.25); throughput_msps >= 50 violated by 90.3%

Per family:
- iterative: 29 evals, 0 feasible; max throughput seen 11.5 MSPS; best accuracy 19.70 bits
- unrolled_k: 71 evals, 0 feasible; max throughput seen 16.1 MSPS; best accuracy 24.11 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 5977 in, 6696 out
- provider-reported cost: $0.0084
- full prompts and replies: `llm_trace.jsonl`

