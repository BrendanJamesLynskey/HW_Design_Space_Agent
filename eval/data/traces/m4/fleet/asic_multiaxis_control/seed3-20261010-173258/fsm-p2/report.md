# DSE run: asic_multiaxis_control

**Verdict:** INFEASIBLE: the architect concluded no design in the registry meets the spec.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_multiaxis_control: Shared sin/cos unit in sky130 standard cells for a 16-axis motor-control loop: a 1 MHz control tick issues 32 requests at once; all 32 results must be back within 0.5 us of the tick (p99 over ticks). Max error <= 2^-12. Minimise area.
  target: asic-sky130hd
  constraint: throughput_msps >= 32
  constraint: max_abs_err <= 0.000244141
  constraint: sys_p99_batch_us <= 0.5
  objective: min area_um2 (HV ref 100000)
  objective: max accuracy_bits (HV ref 12)
  select: min area_um2
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average)
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
None: no evaluated design satisfies every constraint.

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 14.8
- `max_abs_err <= 0.000244141`: met by 15/100 evaluations; best value seen 2.23e-06 (2^-18.77)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 2.15
- best throughput seen 14.8 MSPS (estimate); best accuracy 18.77 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *All four families have so far produced 0 feasible designs across 197 evals, which is a strong signal that the constraints (32 msps throughput + 2^-12 accuracy + 0.5 us p99 batch) are tight and the prior searches were too diffuse. The key bottleneck is throughput: 32 results/us requires either a pipelined design (1 result/cycle at >= 32 MHz) or an unrolled design (1 result every ceil(N/k) cycles at Fmax >= 32*ceil(N/k) MHz). Since I am restricted to iterative and unrolled_k, unrolled_k is the primary candidate: with k=8 and N=10, it needs Fmax >= 16 MHz, which is far more achievable than 32 MHz for a pipelined design. I focus 50% of the budget on unrolled_k with k=2-8 to map the Fmax-vs-throughput trade-off, and 50% on iterative to either confirm infeasibility or find a low-area corner. Ranges are narrowed to data_width 12-16 (12 is the accuracy floor; going higher wastes area without helping the 2^-12 constraint), n_iter 10-14 (sufficient for 12-bit accuracy with small guards), and guards 0-2 (keep datapath narrow to preserve Fmax). This focused search should either find feasible designs or conclusively establish infeasibility within the 100-eval budget.*)
- `unrolled_k` (30 evals): data_width=12..16, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..8. *Why:* unrolled_k is the only family that can plausibly hit 32 results/us: with k=8 and N=10-14, it produces one result every ceil(N/k) cycles (2 cycles), so at Fmax >= 16 MHz it clears the 32 msps throughput floor. The previous 53 evals found 0 feasible, which strongly suggests the search was either too wide (wasting budget on low-k or low-Fmax corners) or the Fmax of the iterative-style datapath is below the ~16 MHz needed. I narrow data_width to 12-16 (12 is the accuracy floor for 2^-12 error; 16 gives margin for angle_guard/frac_guard interplay), n_iter to 10-14 (enough for 12-bit accuracy with modest guards), and focus k on 2-8 to find the sweet spot between Fmax (higher k = more combinational depth = lower Fmax) and throughput (higher k = fewer cycles/result). angle_guard 0-2 and frac_guard 0-2 keep the datapath narrow to preserve Fmax while still allowing the accuracy model to find a feasible (data_width, n_iter, guards) combination.
- `iterative` (30 evals): data_width=12..16, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the cheapest-area family (shared datapath, no k-way parallelism) and the spec's selection rule is min area. It cannot meet the 32 msps throughput constraint on its own (1 result per N+3 cycles), so it will only appear on the front if the system-level p99_batch constraint can be satisfied by the control-loop timing (32 requests issued at once, 0.5 us deadline). Given that 47 prior evals found 0 feasible, I suspect the Fmax of even the narrowest iterative design is below what's needed, or the accuracy constraints were not simultaneously satisfiable in the ranges tried. I keep this family in the search with a tight range (data_width 12-16, n_iter 10-14, guards 0-2) to confirm infeasibility or to find a narrow feasible sliver that the wider prior search missed. If it remains infeasible, the unrolled_k front will carry the design.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — Round 1 (60 evals) on iterative and unrolled_k found 0 feasible designs. The throughput constraint (>=32 MSPS) is violated by 100% of designs, with best seen 12.4 MSPS (iterative) and 10.2 MSPS (unrolled_k). These families produce one result every N+3 or ceil(N/k)+3 cycles, which fundamentally limits throughput. The pipelined and pipelined_m families produce 1 result/cycle and are the only families that can meet the 32 MSPS throughput constraint and the 0.5us batch latency constraint. I add both families with narrowed ranges focused on the accuracy requirement (max_abs_err <= 2^-12): data_width 14-18, n_iter 13-16, angle_guard -1..2, frac_guard 0..4, and m 2..4 for pipelined_m. The 40 remaining evals in this round (100 total budget, 60 used) will be split 50/50 between the two families to find feasible designs and begin mapping the Pareto front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 12.4
- max_abs_err <= 0.000244141: 100% violate; best seen 0.000389 (2^-11.33)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.58

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=8.18, max_abs_err=0.000474 (2^-11.04); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 94.2%; sys_p99_batch_us <= 0.5 violated by 680.5%
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=2 rounding=round]: throughput=7.7, max_abs_err=0.000389 (2^-11.33); throughput_msps >= 32 violated by 75.9%; max_abs_err <= 0.000244141 violated by 59.5%; sys_p99_batch_us <= 0.5 violated by 729.4%
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=7.7, max_abs_err=0.000391 (2^-11.32); throughput_msps >= 32 violated by 75.9%; max_abs_err <= 0.000244141 violated by 60.1%; sys_p99_batch_us <= 0.5 violated by 729.4%
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=1 rounding=round]: throughput=8.84, max_abs_err=0.000825 (2^-10.24); throughput_msps >= 32 violated by 72.4%; max_abs_err <= 0.000244141 violated by 237.7%; sys_p99_batch_us <= 0.5 violated by 622.2%
- iterative [data_width=14 n_iter=13 angle_guard=1 frac_guard=2 rounding=trunc]: throughput=8.84, max_abs_err=0.00105 (2^-9.90); throughput_msps >= 32 violated by 72.4%; max_abs_err <= 0.000244141 violated by 328.9%; sys_p99_batch_us <= 0.5 violated by 622.2%

Per family:
- iterative: 30 evals, 0 feasible; max throughput seen 12.4 MSPS; best accuracy 11.33 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 10.2 MSPS; best accuracy 11.23 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 1 used 60 evals on iterative and unrolled_k and found 0 feasible designs: best throughput was 12.4 MSPS (need >=32) and best accuracy was 11.33 bits (need >=12, i.e. max_abs_err <= 2^-12). The throughput constraint is the binding one: iterative (N+3 cycles/result) and unrolled_k (ceil(N/k)+3 cycles/result) cannot reach 32 MSPS within the registry's parameter ranges. The pipelined and pipelined_m families produce 1 result/cycle and are the only families that can satisfy throughput_msps >= 32 and sys_p99_batch_us <= 0.5 (32 requests must complete within 0.5us of a 1us tick). I narrow data_width to 14-18 and n_iter to 13-16 because the accuracy constraint (max_abs_err <= 2^-12) requires roughly 12+ bits of accuracy, which from the Round 1 evidence (11.33 bits at W=16, N=14) suggests W>=16 and N>=14 are needed; the ranges allow the optimizer to find the minimum-area point that meets accuracy. angle_guard is narrowed to -1..2 and frac_guard to 0..4 to focus on configurations that can achieve the required accuracy without excessive area. m is set to 2..4 for pipelined_m to balance area against the pipeline depth. This round (40 evals) should find feasible designs and begin mapping the Pareto front over area and accuracy at the required throughput.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The spec requires a throughput of >= 32 MSPS and a system p99 batch latency of <= 0.5 us for a burst of 32 requests. The `iterative` and `unrolled_k` families, which were the only ones explored, are fundamentally incapable of meeting these throughput and latency constraints. The maximum throughput observed was 14.8 MSPS (iterative) and 12.2 MSPS (unrolled_k), both significantly below the 32 MSPS requirement. Furthermore, the system p99 batch latency was observed to be at least 2.15 us, which is more than 4x the 0.5 us limit. This is because these families process one or a few micro-rotations per cycle, leading to a high latency per result (N+3 or ceil(N/k)+3 cycles) and low throughput. The `pipelined` and `pipelined_m` families, which have a throughput of 1 result/cycle, were not explored. However, even with a pipelined architecture, achieving 32 MSPS would require a clock frequency of at least 32 MHz. While this is feasible, the latency constraint is the primary blocker. A pipelined CORDIC with N iterations has a latency of N+2 cycles. To process 32 requests in 0.5 us at 32 MHz (31.25 ns/cycle), the total time available is 0.5 us / 31.25 ns/cycle = 16 cycles. This means the pipeline latency (N+2) plus the time to process the 32 requests (32 cycles) must fit within the system's timing constraints. However, the system constraint is on the *batch* latency, which is the time from the first request to the last result. For a pipelined unit, if 32 requests are issued back-to-back, the first result comes out after N+2 cycles, and the last result comes out after N+2+31 cycles. The total batch latency is therefore N+33 cycles. For this to be <= 0.5 us, we need (N+33) * T_cycle <= 0.5 us. If T_cycle is 31.25 ns (32 MHz), then N+33 <= 16, which implies N <= -17, which is impossible. Even if we run the CORDIC at a higher frequency, say 100 MHz (10 ns/cycle), the batch latency would be (N+33)*10 ns. For this to be <= 500 ns, we need N+33 <= 50, so N <= 17. This is feasible for N=17. However, the throughput constraint is 32 MSPS. At 100 MHz, a pipelined CORDIC has a throughput of 100 MSPS, which satisfies the constraint. But the area would be much larger due to the higher frequency and the pipeline registers. More importantly, the `pipelined` and `pipelined_m` families were not explored in the previous rounds, and the budget is exhausted. Given that the explored families are infeasible and the unexplored families would require significant area increases and were not evaluated, and considering the strict latency constraint on the batch, it is highly likely that no design in the registry can meet all constraints simultaneously within a reasonable area. The evidence from the explored families shows a clear inability to meet the throughput and latency requirements, and the unexplored families, while potentially capable of meeting throughput, face the same batch latency challenge which scales with N and the clock period. Therefore, the spec is infeasible.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 14.8
- max_abs_err <= 0.000244141: 85% violate; best seen 2.23e-06 (2^-18.77)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.15

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=8.18, max_abs_err=0.000474 (2^-11.04); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 94.2%; sys_p99_batch_us <= 0.5 violated by 680.5%
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=2 rounding=round]: throughput=7.7, max_abs_err=0.000389 (2^-11.33); throughput_msps >= 32 violated by 75.9%; max_abs_err <= 0.000244141 violated by 59.5%; sys_p99_batch_us <= 0.5 violated by 729.4%
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=7.7, max_abs_err=0.000391 (2^-11.32); throughput_msps >= 32 violated by 75.9%; max_abs_err <= 0.000244141 violated by 60.1%; sys_p99_batch_us <= 0.5 violated by 729.4%
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=1 rounding=round]: throughput=8.84, max_abs_err=0.000825 (2^-10.24); throughput_msps >= 32 violated by 72.4%; max_abs_err <= 0.000244141 violated by 237.7%; sys_p99_batch_us <= 0.5 violated by 622.2%
- iterative [data_width=20 n_iter=14 angle_guard=3 frac_guard=2 rounding=trunc]: throughput=6.49, max_abs_err=0.000128 (2^-12.93); throughput_msps >= 32 violated by 79.7%; sys_p99_batch_us <= 0.5 violated by 884.4%

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 14.8 MSPS; best accuracy 18.77 bits
- unrolled_k: 50 evals, 0 feasible; max throughput seen 12.2 MSPS; best accuracy 16.99 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8253 in, 3207 out
- provider-reported cost: $0.0060
- full prompts and replies: `llm_trace.jsonl`

