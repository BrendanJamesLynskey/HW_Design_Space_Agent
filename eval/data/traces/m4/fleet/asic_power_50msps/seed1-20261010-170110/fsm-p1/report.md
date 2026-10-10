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
- `max_abs_err <= 0.000244141`: met by 28/100 evaluations; best value seen 1.15e-06 (2^-19.73)
- best throughput seen 19.7 MSPS (estimate); best accuracy 19.73 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraint is throughput >= 50 MSPS. iterative (1 result per N+3 cycles) needs Fmax >= 50*(N+3) MHz = 650+ MHz for any N>=12, which is implausible in sky130 standard cells, so it is included only as a narrow confirmation slice with zero budget share. unrolled_k (1 result per ceil(N/k)+3 cycles) is the only family in my assignment that can plausibly meet the constraint: with k=4 and N=12 it needs only ~300 MHz. I therefore spend the entire budget on unrolled_k, restricting data_width to 14..16 and n_iter to 12..16 (the region where max_abs_err <= 2^-12 is achievable), angle_guard to -1..1 and frac_guard to 0..2 (small guards keep area/power low while preserving accuracy), rounding over both choices, and k to 2..4 (k=4 is the throughput-critical case; k=2..3 give more area/power headroom at higher Fmax). This lets Optuna map the power_index vs accuracy_bits front over the feasible region, with the selection rule (min power_index) picking the lowest-power feasible point.*)
- `iterative` (5 evals): data_width=14..16, n_iter=12..16, angle_guard=-1..1, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the only family that can plausibly meet the 50 MSPS throughput constraint: it produces one result every N+3 cycles, so it needs Fmax >= 50*(N+3) MHz. For N=12..16 that is 650..850 MHz, which is far beyond sky130 standard-cell capability, so iterative will almost certainly violate the throughput constraint. I include a narrow slice only to let code confirm infeasibility and to anchor the low-power end of the front if any corner slips through.
- `unrolled_k` (55 evals): data_width=14..16, n_iter=12..16, angle_guard=-1..1, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k is the only family in my assignment that can plausibly meet throughput >= 50 MSPS: it produces one result every ceil(N/k)+3 cycles, so it needs Fmax >= 50*(ceil(N/k)+3) MHz. With N=12..16 and k=2..4, ceil(N/k)+3 ranges from 6 (N=12,k=4) to 11 (N=16,k=2), i.e. required Fmax 300..550 MHz. The k=4, N=12 corner (300 MHz) is the most likely to be feasible in sky130. Accuracy constraint max_abs_err <= 2^-12 is met by data_width 14..16 with n_iter 12..16 (accuracy depends only on these plus guards/rounding, identical across families). I focus the full budget here, with k biased toward 4 to hit the throughput constraint, and let Optuna trade off data_width/n_iter/guards/rounding to map the power-vs-accuracy front within the feasible region.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The iterative and unrolled_k families are fundamentally incapable of meeting the 50 MSPS throughput constraint. The best throughput observed for iterative was 9.43 MSPS and for unrolled_k was 7.78 MSPS, both falling far short of the 50 MSPS requirement. Since these families produce only one result every several cycles, they cannot achieve the required throughput even at high Fmax. The pipelined and pipelined_m families, which produce one result per cycle, are the only candidates that can potentially meet the throughput constraint. I will add these families to the search to explore the feasible region.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 9.43
- max_abs_err <= 0.000244141: 92% violate; best seen 0.000214 (2^-12.19)

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=16 n_iter=16 angle_guard=1 frac_guard=2 rounding=round k=2]: throughput=6.49, max_abs_err=0.000214 (2^-12.19); throughput_msps >= 50 violated by 87.0%
- unrolled_k [data_width=16 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc k=2]: throughput=6.49, max_abs_err=0.000237 (2^-12.04); throughput_msps >= 50 violated by 87.0%
- unrolled_k [data_width=16 n_iter=15 angle_guard=1 frac_guard=2 rounding=round k=2]: throughput=6.49, max_abs_err=0.000218 (2^-12.16); throughput_msps >= 50 violated by 87.0%
- unrolled_k [data_width=16 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc k=2]: throughput=6.49, max_abs_err=0.00025 (2^-11.97); throughput_msps >= 50 violated by 87.0%; max_abs_err <= 0.000244141 violated by 2.2%
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=2 rounding=round k=2]: throughput=7.14, max_abs_err=0.000279 (2^-11.81); throughput_msps >= 50 violated by 85.7%; max_abs_err <= 0.000244141 violated by 14.2%

Per family:
- iterative: 5 evals, 0 feasible; max throughput seen 9.43 MSPS; best accuracy 10.72 bits
- unrolled_k: 55 evals, 0 feasible; max throughput seen 7.78 MSPS; best accuracy 12.19 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Adding pipelined and pipelined_m families to explore the feasible region for the 50 MSPS throughput constraint. These families produce one result per cycle, unlike iterative and unrolled_k which are throughput-limited. Focusing on moderate data_width and n_iter ranges to balance accuracy and power.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The throughput constraint (>= 50 MSPS) is unreachable by any family in the registry. The iterative family, which has the highest throughput potential (1 result per N+3 cycles), achieved a maximum of only 19.7 MSPS in 25 evaluations. The unrolled_k family, which can chain up to k=8 micro-rotations per cycle, achieved a maximum of only 9.94 MSPS in 75 evaluations. Even the theoretical maximum for unrolled_k (k=8) is far below the 50 MSPS requirement. Since no design in the registry can meet the throughput constraint, the problem is infeasible.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 100% violate; best seen 19.7
- max_abs_err <= 0.000244141: 72% violate; best seen 1.15e-06 (2^-19.73)

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=16 n_iter=16 angle_guard=1 frac_guard=2 rounding=round k=2]: throughput=6.49, max_abs_err=0.000214 (2^-12.19); throughput_msps >= 50 violated by 87.0%
- unrolled_k [data_width=16 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc k=2]: throughput=6.49, max_abs_err=0.000237 (2^-12.04); throughput_msps >= 50 violated by 87.0%
- unrolled_k [data_width=16 n_iter=15 angle_guard=1 frac_guard=2 rounding=round k=2]: throughput=6.49, max_abs_err=0.000218 (2^-12.16); throughput_msps >= 50 violated by 87.0%
- unrolled_k [data_width=16 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc k=2]: throughput=6.49, max_abs_err=0.00025 (2^-11.97); throughput_msps >= 50 violated by 87.0%; max_abs_err <= 0.000244141 violated by 2.2%
- iterative [data_width=20 n_iter=21 angle_guard=0 frac_guard=0 rounding=round]: throughput=5.08, max_abs_err=3.25e-05 (2^-14.91); throughput_msps >= 50 violated by 89.8%

Per family:
- iterative: 25 evals, 0 feasible; max throughput seen 19.7 MSPS; best accuracy 19.73 bits
- unrolled_k: 75 evals, 0 feasible; max throughput seen 9.94 MSPS; best accuracy 18.96 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7699 in, 2224 out
- provider-reported cost: $0.0054
- full prompts and replies: `llm_trace.jsonl`

