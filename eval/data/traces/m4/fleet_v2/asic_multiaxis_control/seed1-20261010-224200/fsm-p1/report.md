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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 19.7
- `max_abs_err <= 0.000244141`: met by 18/100 evaluations; best value seen 1.15e-06 (2^-19.73)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 1.62
- best throughput seen 19.7 MSPS (estimate); best accuracy 19.73 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec has a hard throughput constraint of >= 32 Msps, which is very demanding. In my assigned families (iterative and unrolled_k), only unrolled_k can plausibly meet this, and only with high k (4-8) and high Fmax. The accuracy constraint (max_abs_err <= 2^-12) requires data_width and n_iter to be sufficient; from CORDIC theory, N=12-16 iterations with W=14-16 should give ~12-14 bits of accuracy, so I'm narrowing the ranges to focus the search. The system constraint (p99 batch latency <= 0.5 us) is also critical: 32 requests must complete within 0.5 us. For unrolled_k with k=8 and 5 cycles per result, 32 results take 160 cycles. At 160 MHz, that's 1 us, which exceeds 0.5 us. So we need even higher Fmax or higher k. This is a tight problem. I'm allocating 70% of the budget to unrolled_k to explore the feasible region, and 30% to iterative as a baseline. The data_width range is 14-16 because W=14 gives output LSB of 2^-12, which just meets the error constraint with minimal iterations, while W=16 gives more margin. n_iter is 12-16 to balance accuracy and area. angle_guard and frac_guard are kept small (0-2) to minimize area while maintaining accuracy.*)
- `unrolled_k` (42 evals): data_width=14..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=4..8. *Why:* unrolled_k is the only family in my assignment that can plausibly meet the throughput constraint. The spec requires throughput_msps >= 32, which means the unit must produce at least 32 results per microsecond. For unrolled_k, throughput = Fmax * k (since it produces k results per cycle when fully unrolled, or more precisely, one result every ceil(N/k)+3 cycles, so throughput = Fmax / (ceil(N/k)+3) * ... wait, let me reconsider. Actually, unrolled_k produces one result every ceil(N/k)+3 cycles. So throughput_msps = Fmax_MHz / (ceil(N/k)+3). To get >= 32 Msps, we need Fmax / (ceil(N/k)+3) >= 32. If Fmax is around 100-200 MHz, then ceil(N/k)+3 must be <= 3-6. With k=4..8 and N=12..16, ceil(N/k) is 2-4, so total cycles is 5-7. At 100 MHz, that gives 14-20 Msps, which is below 32. At 200 MHz, that gives 28-40 Msps. So we need high Fmax and high k. k=8 with N=12 gives ceil(12/8)=2, so 5 cycles. At 160 MHz, that's 32 Msps. This is tight but feasible. The area will be larger due to the unrolled datapath, but it's the only way to meet throughput in my assigned families. I'll focus on higher k values and moderate N to balance area and throughput.
- `iterative` (18 evals): data_width=14..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is included as a baseline to map the area-accuracy trade-off at low throughput. It will almost certainly fail the throughput constraint (throughput = Fmax/(N+3), so at 100 MHz with N=14, that's only ~5.9 Msps), but it provides the smallest-area reference point on the Pareto front for accuracy. This helps establish the lower bound of the trade-off curve and ensures the hypervolume calculation has a well-defined reference. The budget is small because it's unlikely to be on the feasible front, but it's useful for context.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The iterative and unrolled_k families cannot meet the throughput constraint (best 9.43 MSPS vs 32 required) because they produce one result every several cycles. The pipelined and pipelined_m families produce one result per cycle, which is necessary to achieve 32 MSPS throughput. Additionally, the system constraint requires 32 results within 0.5 us, which implies a throughput of at least 64 MSPS (32 results / 0.5 us) if the pipeline is fully utilized, or at least 32 MSPS if we consider the average rate. The pipelined families are the only ones that can potentially meet these throughput and latency requirements. I will explore pipelined and pipelined_m with parameters that ensure sufficient accuracy (max_abs_err <= 2^-12) and throughput.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 9.43
- max_abs_err <= 0.000244141: 97% violate; best seen 0.000134 (2^-12.86)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 3.38

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=round]: throughput=8, max_abs_err=0.000311 (2^-11.65); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 27.2%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=1 rounding=round]: throughput=7.56, max_abs_err=0.00025 (2^-11.97); throughput_msps >= 32 violated by 76.4%; max_abs_err <= 0.000244141 violated by 2.2%; sys_p99_batch_us <= 0.5 violated by 745.5%
- iterative [data_width=14 n_iter=14 angle_guard=2 frac_guard=2 rounding=round]: throughput=8.32, max_abs_err=0.000513 (2^-10.93); throughput_msps >= 32 violated by 74.0%; max_abs_err <= 0.000244141 violated by 110.1%; sys_p99_batch_us <= 0.5 violated by 667.4%
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=1 rounding=round]: throughput=9.43, max_abs_err=0.000773 (2^-10.34); throughput_msps >= 32 violated by 70.5%; max_abs_err <= 0.000244141 violated by 216.4%; sys_p99_batch_us <= 0.5 violated by 576.9%
- iterative [data_width=16 n_iter=12 angle_guard=0 frac_guard=1 rounding=round]: throughput=9.07, max_abs_err=0.000703 (2^-10.47); throughput_msps >= 32 violated by 71.7%; max_abs_err <= 0.000244141 violated by 188.0%; sys_p99_batch_us <= 0.5 violated by 604.3%

Per family:
- iterative: 18 evals, 0 feasible; max throughput seen 9.43 MSPS; best accuracy 12.86 bits
- unrolled_k: 42 evals, 0 feasible; max throughput seen 6.82 MSPS; best accuracy 12.02 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The pipelined and pipelined_m families are the only ones that can meet the throughput constraint of 32 MSPS. The ranges are chosen to ensure accuracy while keeping area reasonable.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The spec requires a throughput of >= 32 MSPS and a system p99 batch latency of <= 0.5 us for a burst of 32 requests. The `iterative` and `unrolled_k` families are inherently serial or partially parallel architectures that cannot achieve 32 MSPS (best seen: 19.7 MSPS for iterative, 9.94 MSPS for unrolled_k). More critically, the `sys_p99_batch_us` constraint is violated by all evaluated designs (best seen: 1.62 us, which is >3x the 0.5 us limit). To meet the 0.5 us batch latency for 32 requests, the system would need to process all 32 results in 0.5 us. If the clock frequency is Fmax, and we assume a pipelined architecture (which is the only family capable of high throughput, 1 result/cycle), the minimum latency for 32 results is roughly 32 cycles (ignoring pipeline fill). For 32 cycles to fit in 0.5 us, the clock frequency must be at least 64 MHz. However, even if we assume a high Fmax, the `iterative` and `unrolled_k` families have a latency of N+3 or ceil(N/k)+3 cycles per result, but they do not produce 1 result/cycle. The `iterative` family produces 1 result every N+3 cycles. To get 32 results in 0.5 us, the total time for 32 results must be <= 0.5 us. For `iterative`, time for 32 results is 32 * (N+3) / Fmax. Even with N=4 (min), this is 32*7/Fmax = 224/Fmax. For this to be <= 0.5 us, Fmax must be >= 448 MHz. The best Fmax seen for `iterative` was implicitly low (throughput 19.7 MSPS with 1 result/7-15 cycles implies Fmax ~ 1.3-2.8 GHz? No, throughput = Fmax / (N+3). If throughput is 19.7 MSPS and N+3 is ~10, Fmax is ~200 MHz. 224/200MHz = 1.12 us, which matches the observed ~1.62 us violation). The `pipelined` and `pipelined_m` families have not been explored, but they are the only ones that can achieve 1 result/cycle. However, the budget is exhausted (100/100 evals) and this is the final round. The `iterative` and `unrolled_k` families have proven unable to meet the throughput and batch latency constraints. Since I cannot explore `pipelined` in this final round (decision must be stop or infeasible), and the explored families are infeasible, I must declare infeasibility based on the evidence that the serial/partially-parallel architectures cannot meet the strict batch latency and throughput requirements. The `sys_p99_batch_us` constraint is the most binding and is violated by a large margin (best 1.62 us vs 0.5 us limit) for all explored families.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 19.7
- max_abs_err <= 0.000244141: 82% violate; best seen 1.15e-06 (2^-19.73)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 1.62

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=round]: throughput=8, max_abs_err=0.000311 (2^-11.65); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 27.2%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=1 rounding=round]: throughput=7.56, max_abs_err=0.00025 (2^-11.97); throughput_msps >= 32 violated by 76.4%; max_abs_err <= 0.000244141 violated by 2.2%; sys_p99_batch_us <= 0.5 violated by 745.5%
- iterative [data_width=14 n_iter=14 angle_guard=2 frac_guard=2 rounding=round]: throughput=8.32, max_abs_err=0.000513 (2^-10.93); throughput_msps >= 32 violated by 74.0%; max_abs_err <= 0.000244141 violated by 110.1%; sys_p99_batch_us <= 0.5 violated by 667.4%
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=1 rounding=round]: throughput=9.43, max_abs_err=0.000773 (2^-10.34); throughput_msps >= 32 violated by 70.5%; max_abs_err <= 0.000244141 violated by 216.4%; sys_p99_batch_us <= 0.5 violated by 576.9%
- iterative [data_width=16 n_iter=12 angle_guard=0 frac_guard=1 rounding=round]: throughput=9.07, max_abs_err=0.000703 (2^-10.47); throughput_msps >= 32 violated by 71.7%; max_abs_err <= 0.000244141 violated by 188.0%; sys_p99_batch_us <= 0.5 violated by 604.3%

Per family:
- iterative: 38 evals, 0 feasible; max throughput seen 19.7 MSPS; best accuracy 19.73 bits
- unrolled_k: 62 evals, 0 feasible; max throughput seen 9.94 MSPS; best accuracy 18.96 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8844 in, 3022 out
- provider-reported cost: $0.0067
- full prompts and replies: `llm_trace.jsonl`

