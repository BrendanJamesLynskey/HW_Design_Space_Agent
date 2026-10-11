# DSE run: multiaxis_control

**Verdict:** INFEASIBLE: the architect concluded no design in the registry meets the spec.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec multiaxis_control: Shared sin/cos unit for a 16-axis motor-control loop: a 1 MHz control tick issues 32 requests at once (Park + inverse Park per axis); all 32 results must be back within 0.44 us of the tick (p99 over ticks). Max error <= 2^-12. Minimise LUTs + FFs.
  constraint: throughput_msps >= 32
  constraint: max_abs_err <= 0.000244141
  constraint: sys_p99_batch_us <= 0.44
  objective: min luts_plus_ffs (HV ref 4000)
  objective: max accuracy_bits (HV ref 12)
  select: min luts_plus_ffs
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average)
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
None: no evaluated design satisfies every constraint.

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 23.7
- `max_abs_err <= 0.000244141`: met by 16/100 evaluations; best value seen 2.86e-07 (2^-21.74)
- `sys_p99_batch_us <= 0.44`: met by 0/100 evaluations; best value seen 1.35
- best throughput seen 23.7 MSPS (estimate); best accuracy 21.74 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The key challenge is the 32 Msps throughput constraint. iterative produces 1 result every N+3 cycles, so for N=12 it needs Fmax >= 480 MHz to reach 32 Msps, which is infeasible on Artix-7. unrolled_k with k=8 and N=12 needs only 5 cycles/result, so Fmax >= 160 MHz suffices, which is borderline feasible. I will allocate the full budget to unrolled_k with high k values (k=6..8) and low N (N=12..14) to find configurations that meet the throughput constraint while satisfying the accuracy requirement (max_abs_err <= 2^-12). If no configuration meets all constraints, I will report infeasible. The accuracy constraint requires W>=14 and N>=12, which I have included in the ranges. I am narrowing the ranges to focus the budget on the feasible region.*)
- `iterative` (30 evals): data_width=14..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the only family that can plausibly meet the 32 Msps throughput constraint (1 result/cycle). It is the baseline for the area/accuracy trade-off. Ranges are narrowed to the accuracy-feasible region (W>=14, N>=12) to focus the budget on the Pareto front rather than infeasible points.
- `unrolled_k` (30 evals): data_width=14..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..8. *Why:* unrolled_k with k>=2 can also reach 32 Msps if Fmax is high enough (e.g., k=4, N=16 -> 4 cycles/result, needs Fmax>=8 MHz which is trivially met; but for 32 Msps we need 1 result per 31.25 ns, so k=4 at Fmax=8 MHz gives 2 Msps... wait, let me reconsider. throughput = Fmax * (1/cycles_per_result). For unrolled_k, cycles_per_result = ceil(N/k)+3. For k=4, N=16: ceil(16/4)+3 = 7 cycles. At Fmax=100 MHz, throughput = 100/7 = 14.3 Msps < 32. For k=8, N=16: ceil(16/8)+3 = 5 cycles. At Fmax=100 MHz, throughput = 20 Msps < 32. Even at Fmax=200 MHz, k=8 gives 40 Msps. But Artix-7 Fmax is typically <200 MHz. So unrolled_k likely cannot meet 32 Msps unless k is very large and Fmax is high. However, the constraint is throughput_msps >= 32, and unrolled_k may not be able to meet it. I should still include it with a small budget to confirm infeasibility or find a corner case. Actually, re-reading: iterative is 1 micro-rotation/cycle, N+3 cycles/result. For N=16, that's 19 cycles. At Fmax=100 MHz, throughput = 100/19 = 5.26 Msps. That's way below 32. So iterative also cannot meet 32 Msps! Wait, I need to re-read the spec. The constraint is throughput_msps >= 32. For iterative, 1 result every N+3 cycles. For N=12, that's 15 cycles. At Fmax=100 MHz, throughput = 6.67 Msps. Still far below 32. This means neither iterative nor unrolled_k can meet the 32 Msps constraint unless Fmax is extremely high. For iterative to reach 32 Msps with N=12 (15 cycles), Fmax must be >= 32*15 = 480 MHz, which is impossible on Artix-7. For unrolled_k with k=8, N=12: ceil(12/8)+3 = 5 cycles. Fmax >= 32*5 = 160 MHz. This is borderline but possibly achievable on Artix-7 with a simple design. So unrolled_k with high k might just barely meet the constraint. I should focus the budget on unrolled_k with high k values and check if any configuration meets the throughput constraint. If not, the problem is infeasible for my assigned families.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The iterative and unrolled_k families are fundamentally incapable of meeting the throughput constraint (>= 32 MSPS). The best throughput observed in Round 1 was 13.2 MSPS for iterative and 12.4 MSPS for unrolled_k, which is less than half the required 32 MSPS. Since these architectures produce one result every several cycles (N+3 or ceil(N/k)+3), they cannot sustain the 32 requests/us burst rate required by the system scenario, leading to massive violations of sys_p99_batch_us (best seen 2.42 us vs 0.44 us limit). The pipelined and pipelined_m families, which produce one result per cycle, are the only candidates that can potentially meet the throughput and latency constraints. We must explore these families to find a feasible design.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 13.2
- max_abs_err <= 0.000244141: 93% violate; best seen 0.00018 (2^-12.44)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 2.42

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=1 rounding=round]: throughput=12.4, max_abs_err=0.000325 (2^-11.59); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 33.2%; sys_p99_batch_us <= 0.44 violated by 485.7%
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round]: throughput=11.7, max_abs_err=0.000209 (2^-12.22); throughput_msps >= 32 violated by 63.5%; sys_p99_batch_us <= 0.44 violated by 522.3%
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=1 rounding=round]: throughput=12.4, max_abs_err=0.00038 (2^-11.36); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 55.6%; sys_p99_batch_us <= 0.44 violated by 485.7%
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=0 rounding=round]: throughput=12.4, max_abs_err=0.00041 (2^-11.25); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 68.1%; sys_p99_batch_us <= 0.44 violated by 485.7%
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round]: throughput=11, max_abs_err=0.00018 (2^-12.44); throughput_msps >= 32 violated by 65.6%; sys_p99_batch_us <= 0.44 violated by 559.0%

Per family:
- iterative: 30 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 12.44 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 12.4 MSPS; best accuracy 11.95 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Shift exploration to pipelined and pipelined_m families, which are the only ones capable of meeting the 32 MSPS throughput constraint. Focus on parameter ranges that balance accuracy (>= 12 bits) and area.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The spec requires a throughput of >= 32 MSPS and a system p99 batch latency of <= 0.44 us. The system issues 32 requests every 1 us (1 MHz tick). To meet the 32 MSPS throughput constraint, the CORDIC must be able to process at least one result per cycle at a clock frequency of at least 32 MHz (since 32 results/us = 32 results per 1us). 

1. **Throughput Constraint:** The `iterative` and `unrolled_k` families were explored in Round 2. `iterative` has a latency of N+3 cycles and produces 1 result every N+3 cycles. Even with a high Fmax, its throughput is limited by the number of cycles per result. The best throughput seen for `iterative` was 23.7 MSPS, which violates the 32 MSPS constraint. `unrolled_k` with k>1 can improve throughput, but the best seen was only 14.8 MSPS, likely due to the increased logic depth reducing Fmax significantly or the search not finding a sweet spot. 

2. **System Latency Constraint:** The `sys_p99_batch_us` constraint is <= 0.44 us. The best seen was 1.35 us. For a burst of 32 requests, if the unit is pipelined (1 result/cycle), the time to process the burst is 32 cycles. If Fmax is 32 MHz (period 31.25 ns), 32 cycles take 1000 ns = 1 us. This already exceeds the 0.44 us limit. To get 32 results in 0.44 us, the unit would need to process them in ~14 cycles (0.44us / 31.25ns/cycle), implying a throughput of >32 MSPS just for the burst duration, but more critically, the *latency* of the first result plus the time to stream out the remaining 31 must fit in 0.44 us. 

3. **Missing Families:** The `pipelined` and `pipelined_m` families were **not explored** in Round 2. These families produce 1 result per cycle. A `pipelined` design with N=13 (for ~12 bits accuracy) has a latency of N+2 = 15 cycles. If Fmax is high enough (e.g., 100 MHz), 15 cycles = 150 ns. The burst of 32 requests would take 32 cycles to drain = 320 ns. Total time from tick to last result ~ 150 ns (latency) + 320 ns (drain) - 150 ns (overlap) = 320 ns? No, the first result comes out at cycle 15. The last result comes out at cycle 15 + 31 = 46 cycles. At 100 MHz, 46 cycles = 460 ns = 0.46 us. This is very close to the 0.44 us limit. At 120 MHz, 46 cycles = 383 ns = 0.383 us, which would pass. 

However, the decision must be based on the evidence provided. The prompt states: 

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 23.7
- max_abs_err <= 0.000244141: 84% violate; best seen 2.86e-07 (2^-21.74)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 1.35

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=1 rounding=round]: throughput=12.4, max_abs_err=0.000325 (2^-11.59); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 33.2%; sys_p99_batch_us <= 0.44 violated by 485.7%
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round]: throughput=11.7, max_abs_err=0.000209 (2^-12.22); throughput_msps >= 32 violated by 63.5%; sys_p99_batch_us <= 0.44 violated by 522.3%
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=1 rounding=round]: throughput=12.4, max_abs_err=0.00038 (2^-11.36); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 55.6%; sys_p99_batch_us <= 0.44 violated by 485.7%
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=0 rounding=round]: throughput=12.4, max_abs_err=0.00041 (2^-11.25); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 68.1%; sys_p99_batch_us <= 0.44 violated by 485.7%
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round]: throughput=11, max_abs_err=0.00018 (2^-12.44); throughput_msps >= 32 violated by 65.6%; sys_p99_batch_us <= 0.44 violated by 559.0%

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 23.7 MSPS; best accuracy 21.74 bits
- unrolled_k: 50 evals, 0 feasible; max throughput seen 14.8 MSPS; best accuracy 20.73 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7873 in, 3267 out
- provider-reported cost: $0.0077
- full prompts and replies: `llm_trace.jsonl`

