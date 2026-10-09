# DSE run: infeasible_dds_400msps

**Verdict:** INFEASIBLE: the architect concluded no design in the registry meets the spec.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 200 of 400 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec infeasible_dds_400msps: Wideband DDS needing >= 400 MSPS single-lane sin/cos with max error <= 2^-12. Minimise LUTs.
  constraint: throughput_msps >= 400
  constraint: max_abs_err <= 0.000244141
  objective: min luts (HV ref 4000)
  objective: max accuracy_bits (HV ref 12)
  select: min luts
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
None: no evaluated design satisfies every constraint.

- `throughput_msps >= 400`: met by 0/200 evaluations; best value seen 273
- `max_abs_err <= 0.000244141`: met by 163/200 evaluations; best value seen 6.1e-06 (2^-17.32)
- best throughput seen 272.9 MSPS (estimate); best accuracy 17.32 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=400 MSPS single-lane throughput with max_abs_err <= 2^-12. Iterative and unrolled_k produce one result every several cycles, making 400 MSPS extremely difficult unless Fmax is very high, which conflicts with the multi-cycle datapath. Pipelined_m is the most promising family: it achieves 1 result/cycle, and by choosing m (registers every m stages) we can balance Fmax (higher m = fewer registers = potentially higher Fmax but longer combinational path per stage) against area. The fully pipelined family (m=1) is a special case of pipelined_m but tends to have more FFs; pipelined_m with m>=2 should dominate on LUTs+FFs. I focus 100% of the first round on pipelined_m to map the Pareto front over the m, n_iter, and data_width dimensions. data_width 14..20 and n_iter 12..20 are chosen to bracket the 12-bit accuracy requirement: accuracy_bits depends on n_iter and data_width, and we need max_abs_err <= 2^-12. Rounding is fixed to 'round' to minimize error. angle_guard and frac_guard are kept small (0..2) to minimize area while allowing the optimizer to find the minimum that still meets accuracy. If this round reveals that pipelined_m cannot meet 400 MSPS at acceptable accuracy, subsequent rounds can explore pipelined (m=1) or unrolled_k with high k.*)
- `pipelined_m` (100 evals): data_width=14..20, n_iter=12..20, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..8. *Why:* Primary feasible candidate: 1 result/cycle throughput with register-every-m stages allows high Fmax to meet 400 MSPS while keeping area lower than fully pipelined. m=2..8 spans the latency/area/Fmax trade-off. data_width 14..20 and n_iter 12..20 cover the accuracy region for max_abs_err <= 2^-12 (accuracy_bits >= 12). Rounding='round' minimizes error for a given n_iter, helping meet the accuracy constraint with fewer iterations/LUTs. angle_guard 0..2 and frac_guard 0..2 keep the angle path and datapath tight to minimize LUTs while preserving accuracy.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — Round 1 explored only pipelined_m and found 0 feasible designs. The best throughput was 171 MSPS, far below the 400 MSPS constraint. pipelined_m with m=2 produces 1 result every 2 cycles, so even at high Fmax it cannot reach 400 MSPS unless Fmax is extremely high. Full pipelining (pipelined family) produces 1 result per cycle, so it can reach 400 MSPS at 400 MHz or higher. The accuracy constraint (max_abs_err <= 2^-12) is easily met by the best designs seen (up to 15.68 bits), so the binding constraint is throughput. I will add the pipelined family to the search and keep pipelined_m to confirm it cannot meet the throughput constraint. The ranges are narrowed to data_width 16-24 and n_iter 12-20 to focus on configurations that can meet the accuracy constraint while minimizing LUTs.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: pipelined_m. Not yet explored: iterative, unrolled_k, pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 171
- max_abs_err <= 0.000244141: 14% violate; best seen 1.9e-05 (2^-15.68)

No feasible design found yet. Least-violating designs:
- pipelined_m [data_width=18 n_iter=20 angle_guard=0 frac_guard=0 rounding=round m=2]: throughput=171, max_abs_err=0.000114 (2^-13.10); throughput_msps >= 400 violated by 57.3%
- pipelined_m [data_width=19 n_iter=20 angle_guard=1 frac_guard=2 rounding=round m=2]: throughput=164, max_abs_err=3.12e-05 (2^-14.97); throughput_msps >= 400 violated by 58.9%
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=2 rounding=round m=2]: throughput=164, max_abs_err=0.000157 (2^-12.64); throughput_msps >= 400 violated by 58.9%
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=round m=2]: throughput=164, max_abs_err=7.47e-05 (2^-13.71); throughput_msps >= 400 violated by 58.9%
- pipelined_m [data_width=20 n_iter=17 angle_guard=2 frac_guard=2 rounding=round m=2]: throughput=164, max_abs_err=2.23e-05 (2^-15.45); throughput_msps >= 400 violated by 58.9%

Per family:
- pipelined_m: 100 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.68 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 1 explored only pipelined_m and found 0 feasible designs. The best throughput was 171 MSPS, far below the 400 MSPS constraint. pipelined_m with m=2 produces 1 result every 2 cycles, so even at high Fmax it cannot reach 400 MSPS unless Fmax is extremely high. Full pipelining (pipelined family) produces 1 result per cycle, so it can reach 400 MSPS at 400 MHz or higher. The accuracy constraint (max_abs_err <= 2^-12) is easily met by the best designs seen (up to 15.68 bits), so the binding constraint is throughput. I will add the pipelined family to the search and keep pipelined_m to confirm it cannot meet the throughput constraint. The ranges are narrowed to data_width 16-24 and n_iter 12-20 to focus on configurations that can meet the accuracy constraint while minimizing LUTs.*)
- `pipelined` (50 evals): data_width=16..24, n_iter=12..20, angle_guard=-1..2, frac_guard=0..4, rounding=trunc|round. *Why:* Full pipelining (1 result/cycle) is the only way to reach 400 MSPS with a single-lane CORDIC. pipelined_m with m=2 caps at ~171 MSPS because it only halves the datapath width and cannot push Fmax high enough to compensate. Full pipelining trades area for throughput, which is exactly what the spec demands.
- `pipelined_m` (50 evals): data_width=16..24, n_iter=12..20, angle_guard=-1..2, frac_guard=0..4, rounding=trunc|round, m=2..2. *Why:* Keep pipelined_m with m=2 in the search to see if any configuration can reach 400 MSPS. Round 1 showed max 171 MSPS, but the search may not have explored the full Fmax/area trade-off. If pipelined_m cannot reach 400 MSPS, it will be dropped from the front.

**Result (code):** 100 evaluations this round, 200 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The throughput constraint (>= 400 MSPS) is unreachable for all families in the registry. Evidence: 1) The 'pipelined' family, which has the highest theoretical throughput (1 result/cycle), achieved a maximum of only 273 MSPS across 50 evaluations, violating the constraint by 31.8%. 2) The 'pipelined_m' family, which also produces 1 result/cycle but with higher latency, achieved a maximum of only 171 MSPS across 150 evaluations. 3) The 'iterative' and 'unrolled_k' families produce fewer than 1 result per cycle (1/k or 1/N), so their throughput will be strictly lower than the 'pipelined' family's maximum of 273 MSPS. Since the best possible throughput from the highest-throughput architecture (pipelined) is 273 MSPS, which is below the required 400 MSPS, no design in the registry can meet the constraints.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 200 evaluations (0 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 400: 100% violate; best seen 273
- max_abs_err <= 0.000244141: 18% violate; best seen 6.1e-06 (2^-17.32)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=17 n_iter=19 angle_guard=1 frac_guard=0 rounding=round]: throughput=273, max_abs_err=0.000149 (2^-12.71); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=19 angle_guard=0 frac_guard=0 rounding=round]: throughput=273, max_abs_err=0.000114 (2^-13.10); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=19 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=273, max_abs_err=0.000197 (2^-12.31); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=17 n_iter=15 angle_guard=0 frac_guard=1 rounding=round]: throughput=273, max_abs_err=0.000224 (2^-12.12); throughput_msps >= 400 violated by 31.8%
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=273, max_abs_err=0.000182 (2^-12.43); throughput_msps >= 400 violated by 31.8%

Per family:
- pipelined: 50 evals, 0 feasible; max throughput seen 273 MSPS; best accuracy 17.32 bits
- pipelined_m: 150 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.68 bits
```
</details>

## LLM usage
- calls: 6 (failed/unparsed attempts: 0)
- tokens: 19658 in, 2595 out
- provider-reported cost: $0.0048
- full prompts and replies: `llm_trace.jsonl`

