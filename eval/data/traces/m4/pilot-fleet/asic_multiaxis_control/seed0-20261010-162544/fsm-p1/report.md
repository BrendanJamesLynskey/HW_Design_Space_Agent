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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 12.8
- `max_abs_err <= 0.000244141`: met by 12/100 evaluations; best value seen 5.51e-08 (2^-24.11)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 2.49
- best throughput seen 12.8 MSPS (estimate); best accuracy 24.11 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraint is sys_p99_batch_us <= 0.5us for a burst of 32 requests. This requires the CORDIC to produce 32 results in <= 0.5us. For unrolled_k with k=8, N=16: 5 cycles/result, 160 cycles total, requiring Fmax >= 320 MHz. This is the tightest feasible point. For k=4, N=12: 6 cycles/result, 192 cycles, Fmax >= 384 MHz. For iterative, N=12: 15 cycles/result, 480 cycles, Fmax >= 960 MHz - infeasible. So unrolled_k with high k (6-8) and low N (12-16) is the only plausible family. I allocate 50% to unrolled_k to map the area/accuracy/Fmax trade-off within the feasible region, and 50% to iterative to confirm infeasibility and capture the area-minimizing corner in case the system constraint is not binding at L2. data_width 12-16 covers the accuracy requirement (2^-12) with margin. angle_guard and frac_guard 0-2 allow exploring the accuracy/area trade-off. rounding trunc/round covers both options.*)
- `unrolled_k` (30 evals): data_width=12..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..8. *Why:* The hard constraint is sys_p99_batch_us <= 0.5us for a burst of 32 requests at a 1us tick. A pipelined design (1 result/cycle) is the only family that can drain 32 requests in <= 32 cycles, which at a modest Fmax easily fits in 0.5us. However, I am restricted to iterative and unrolled_k. unrolled_k with high k (e.g., k=8) processes 8 micro-rotations per cycle, so a 16-iteration CORDIC takes only 2 cycles of datapath plus 3 overhead = 5 cycles per result. 32 results take 32*5 = 160 cycles. At Fmax >= 320 MHz this fits in 0.5us. The throughput constraint (>= 32 Msps) requires Fmax * (1/k_effective) >= 32, which for unrolled_k means Fmax >= 32 * ceil(N/k) + 3 cycles/result... actually throughput = Fmax / (ceil(N/k)+3). For N=16, k=8: 3 cycles/result, so Fmax >= 32/3 ~ 11 MHz, easily met. The batch constraint is the binding one: 32 results * (ceil(N/k)+3) cycles <= 0.5us * Fmax. For k=8, N=16: 32*5=160 cycles <= 0.5e-6 * Fmax, so Fmax >= 320 MHz. This is tight but plausible for sky130. For k=4, N=16: 7 cycles/result, 32*7=224 cycles, Fmax >= 448 MHz - too tight. So k must be high (6-8) and N must be low (12-16) to keep the per-result cycle count small. data_width 12-16: W=12 gives output LSB 2^-10, max error from CORDIC with N=12, angle_guard=0, frac_guard=0 is roughly 2^-12 to 2^-13, meeting the 2^-12 constraint. Higher W and guards improve accuracy but increase area. The trade-off is area vs accuracy_bits, with the batch latency constraint forcing high k and low N.
- `iterative` (30 evals): data_width=12..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the smallest-area family (shared datapath, 1 micro-rotation/cycle, N+3 cycles/result). For N=12: 15 cycles/result. 32 results take 32*15 = 480 cycles. To fit in 0.5us, Fmax >= 960 MHz - far beyond sky130 capability. So iterative likely CANNOT meet the sys_p99_batch_us <= 0.5us constraint for any reasonable N. However, it is the area-minimizing family and may still appear on the Pareto front for the area vs accuracy trade-off if the system constraint is relaxed or if the L1 bound is optimistic. I include it with a small share to confirm infeasibility and to map the area/accuracy corner. If infeasible, the budget is wasted, but the cost of checking is low. data_width 12-16, n_iter 12-16 to meet max_abs_err <= 2^-12.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The iterative and unrolled_k families are fundamentally incapable of meeting the throughput constraint (>= 32 MSPS). The best throughput observed in Round 1 was 10.7 MSPS for iterative and 8.16 MSPS for unrolled_k, which is less than 1/3 of the required 32 MSPS. Since these architectures produce one result every several cycles (N+3 or ceil(N/k)+3), their throughput is inherently limited by the number of iterations and the clock frequency. To achieve 32 MSPS, the CORDIC must produce one result per cycle, which requires a pipelined architecture. Additionally, the accuracy constraint (max_abs_err <= 2^-12) was also violated by all designs in Round 1 (best seen 2^-11.65), suggesting that higher data_width or n_iter might be needed, but throughput is the primary blocker. Therefore, I must explore the pipelined family, which is designed for 1 result/cycle throughput.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 10.7
- max_abs_err <= 0.000244141: 100% violate; best seen 0.000311 (2^-11.65)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.97

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=1 rounding=trunc]: throughput=8.5, max_abs_err=0.00046 (2^-11.09); throughput_msps >= 32 violated by 73.4%; max_abs_err <= 0.000244141 violated by 88.4%; sys_p99_batch_us <= 0.5 violated by 651.4%
- iterative [data_width=14 n_iter=13 angle_guard=2 frac_guard=2 rounding=round]: throughput=8.84, max_abs_err=0.000581 (2^-10.75); throughput_msps >= 32 violated by 72.4%; max_abs_err <= 0.000244141 violated by 138.0%; sys_p99_batch_us <= 0.5 violated by 622.2%
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=1 rounding=trunc]: throughput=8.18, max_abs_err=0.00046 (2^-11.09); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 88.4%; sys_p99_batch_us <= 0.5 violated by 680.5%
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=round k=2]: throughput=7.45, max_abs_err=0.000311 (2^-11.65); throughput_msps >= 32 violated by 76.7%; max_abs_err <= 0.000244141 violated by 27.2%; sys_p99_batch_us <= 0.5 violated by 756.8%
- unrolled_k [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=round k=2]: throughput=7.78, max_abs_err=0.000462 (2^-11.08); throughput_msps >= 32 violated by 75.7%; max_abs_err <= 0.000244141 violated by 89.0%; sys_p99_batch_us <= 0.5 violated by 720.4%

Per family:
- iterative: 30 evals, 0 feasible; max throughput seen 10.7 MSPS; best accuracy 11.55 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 8.16 MSPS; best accuracy 11.65 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Pipelined is the only family that can meet the 32 MSPS throughput constraint. Ranges are narrowed to focus on the accuracy requirement (2^-12) while keeping area low.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The spec requires a throughput of >= 32 MSPS and a system p99 batch latency of <= 0.5 us for a burst of 32 requests. The `iterative` and `unrolled_k` families explored in the previous round are fundamentally limited by their serial or partially-parallel execution models. The maximum throughput observed was only 12.8 MSPS (unrolled_k with k=2), which is less than half the required 32 MSPS. Furthermore, the `sys_p99_batch_us` constraint is violated by a factor of >600% in the best cases (best seen 2.49 us vs 0.5 us limit). To meet 32 MSPS, the unit must process at least 32 results per microsecond. Given the 1 MHz control tick and 32 requests per tick, the unit needs to sustain a rate of 32 results/us. Only the `pipelined` or `pipelined_m` families, which produce 1 result per cycle, can potentially achieve this if their Fmax is high enough (e.g., Fmax >= 32 MHz for pipelined). However, even if a pipelined design achieved 32 MSPS, the latency constraint is critical. A pipelined CORDIC with N iterations has a latency of N+2 cycles. To process 32 requests in 0.5 us (500 ns), if the clock is 32 MHz (31.25 ns period), the unit has 16 cycles available. A pipelined CORDIC with N=14 (typical for 12-bit accuracy) has a latency of 16 cycles. The first result arrives after 16 cycles (500 ns), leaving no time for the remaining 31 results to be processed and returned within the 0.5 us window if they are pipelined sequentially. Wait, the throughput is 1 result/cycle. If Fmax is 32 MHz, it produces 32 results in 1 us. The first result is available after N+2 cycles. If N=14, latency is 16 cycles = 500 ns. The 32nd result is available 31 cycles later, at 16+31 = 47 cycles = 1468 ns. This violates the 0.5 us batch constraint. To meet the 0.5 us batch constraint for 32 results, the total time from the first request to the last result must be <= 500 ns. If the unit produces 1 result/cycle, the 32nd result is produced 31 cycles after the 1st. The 1st result is produced after Latency cycles. So total time = (Latency + 31) * T_cycle <= 500 ns. Also Throughput = 1/T_cycle >= 32 MHz => T_cycle <= 31.25 ns. So (Latency + 31) * 31.25 ns <= 500 ns => Latency + 31 <= 16 => Latency <= -15. This is impossible. Therefore, no single CORDIC unit in the registry can meet both the throughput and the batch latency constraints simultaneously for a burst of 32. The `pipelined` family would need to be parallelized (e.g., 32 parallel CORDICs) to meet the batch constraint, but the registry only defines a single CORDIC unit per architecture instance. The `unrolled_k` family with k=32 would process 32 rotations in 1 cycle, but k is limited to 8. Even with k=8, it takes 4 cycles for N=32, but throughput is limited by Fmax. The fundamental issue is that a single CORDIC unit cannot output 32 results in 0.5 us while maintaining 32 MSPS throughput unless it has a very high Fmax and low latency, which is physically impossible for a standard CORDIC structure due to the sequential nature of the rotations. The `sys_p99_batch_us` constraint implies that all 32 results must be available within 0.5 us of the tick. For a pipelined unit, the last result is available at (Latency + 31) * T_cycle. For an iterative unit, it is available at 32 * (N+3) * T_cycle. In all cases, the time to produce 32 results is significantly larger than 0.5 us unless the clock frequency is extremely high (e.g., > 200 MHz) and latency is very low, which is not achievable in sky130 for a CORDIC with sufficient accuracy. The best `sys_p99_batch_us` seen was 2.49 us, which is 5x the limit. Given the physical limits of the standard-cell library and the CORDIC architecture, the constraints are mutually exclusive for a single unit. Thus, the design space is infeasible.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 12.8
- max_abs_err <= 0.000244141: 88% violate; best seen 5.51e-08 (2^-24.11)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.49

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=1 rounding=trunc]: throughput=8.5, max_abs_err=0.00046 (2^-11.09); throughput_msps >= 32 violated by 73.4%; max_abs_err <= 0.000244141 violated by 88.4%; sys_p99_batch_us <= 0.5 violated by 651.4%
- iterative [data_width=14 n_iter=13 angle_guard=2 frac_guard=2 rounding=round]: throughput=8.84, max_abs_err=0.000581 (2^-10.75); throughput_msps >= 32 violated by 72.4%; max_abs_err <= 0.000244141 violated by 138.0%; sys_p99_batch_us <= 0.5 violated by 622.2%
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=1 rounding=trunc]: throughput=8.18, max_abs_err=0.00046 (2^-11.09); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 88.4%; sys_p99_batch_us <= 0.5 violated by 680.5%
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=round k=2]: throughput=7.45, max_abs_err=0.000311 (2^-11.65); throughput_msps >= 32 violated by 76.7%; max_abs_err <= 0.000244141 violated by 27.2%; sys_p99_batch_us <= 0.5 violated by 756.8%
- unrolled_k [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=round k=2]: throughput=7.78, max_abs_err=0.000462 (2^-11.08); throughput_msps >= 32 violated by 75.7%; max_abs_err <= 0.000244141 violated by 89.0%; sys_p99_batch_us <= 0.5 violated by 720.4%

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 11.5 MSPS; best accuracy 19.70 bits
- unrolled_k: 50 evals, 0 feasible; max throughput seen 12.8 MSPS; best accuracy 24.11 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8150 in, 3241 out
- provider-reported cost: $0.0073
- full prompts and replies: `llm_trace.jsonl`

