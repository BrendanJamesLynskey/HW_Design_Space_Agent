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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 22
- `max_abs_err <= 0.000244141`: met by 15/100 evaluations; best value seen 3.12e-08 (2^-24.93)
- `sys_p99_batch_us <= 0.44`: met by 0/100 evaluations; best value seen 1.45
- best throughput seen 22.0 MSPS (estimate); best accuracy 24.93 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires throughput_msps >= 32, which is the binding constraint. Only unrolled_k can plausibly meet this: with k=4-8 and N=14-16, the latency is 4-7 cycles/result, requiring Fmax of 128-224 MHz, which is achievable on Artix-7. iterative cannot meet throughput (needs >500 MHz) but is the area-minimal baseline, so it anchors the Pareto front's low-area end for hypervolume coverage. I focus data_width and n_iter on 14-16 because the max_abs_err <= 2^-12 constraint is met at N=14 with modest guard bits, and going higher increases area without improving accuracy_bits beyond the HV reference of 12. Guard bits are kept at 0-1 to minimize area while allowing the accuracy model to find the exact minimum configuration. The 50/50 split balances exploring the throughput-feasible region (unrolled_k) with mapping the area-accuracy trade-off (iterative) for front coverage. The sys_p99_batch_us <= 0.44 us constraint is tight: 32 requests must complete within 0.44 us of the tick. For unrolled_k with 4-7 cycles/result, 32 results take 128-224 cycles. At 128-224 MHz, that is 0.57-1.75 us, which exceeds 0.44 us. This suggests the L1 bound may be violated, but the L2 simulation will confirm. The exploration will reveal whether any unrolled_k configuration meets all constraints or if the spec is infeasible within my assigned families.*)
- `unrolled_k` (30 evals): data_width=14..16, n_iter=14..16, angle_guard=1..1, frac_guard=0..1, rounding=trunc|round, k=4..8. *Why:* unrolled_k is the only family in my assignment that can plausibly meet the throughput_msps >= 32 constraint. With k=4..8, the unit produces 1 result every ceil(N/k)+3 cycles. For N=14..16 and k=4..8, this is 4-7 cycles/result. To hit 32 Msps, Fmax must be >= 128-224 MHz, which is feasible on Artix-7 for a moderately unrolled CORDIC. The k parameter directly trades area (more parallel datapath logic) against throughput (fewer cycles/result), making it the primary knob for the throughput constraint. I focus data_width and n_iter on 14-16 because max_abs_err <= 2^-12 requires roughly 14-16 iterations of CORDIC with modest guard bits; going higher wastes area without improving accuracy_bits meaningfully for the HV reference of 12. angle_guard and frac_guard are kept tight (0-1) because extra guard bits increase area without helping the 2^-12 error floor once n_iter >= 14. Rounding is included as a binary choice since it affects both accuracy and area slightly.
- `iterative` (30 evals): data_width=14..16, n_iter=14..16, angle_guard=1..1, frac_guard=0..1, rounding=trunc|round. *Why:* iterative is included as a baseline for the Pareto front even though it will likely fail the throughput_msps >= 32 constraint (1 result every N+3 = 17-19 cycles, requiring Fmax >= 544-608 MHz, which is unrealistic for a 16-bit CORDIC on Artix-7). However, it has the smallest area (single shared datapath, no unrolling), so it anchors the low-area end of the front. The hypervolume rewards covering the trade-off curve, and the selection rule is min luts_plus_ffs, so if no unrolled_k design meets all constraints, the iterative designs define the infeasible boundary. Keeping the same data_width/n_iter/guard ranges as unrolled_k ensures the accuracy dimension is comparable across families, so the merged front is meaningful. The tight guard ranges (0-1) keep area minimal while still allowing the accuracy model to find the minimum n_iter that meets 2^-12.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The iterative and unrolled_k families are fundamentally incapable of meeting the throughput constraint. The spec requires >= 32 MSPS (32 results/us). The iterative architecture produces 1 result every N+3 cycles. Even with the minimum N=4 (7 cycles/result) and a hypothetical 200 MHz clock, the maximum throughput is ~28.5 MSPS, which is below the 32 MSPS requirement. The observed best throughput was only 11.7 MSPS. Similarly, unrolled_k with k=8 and N=4 yields 1 result every 3 cycles, which at 200 MHz is ~66 MSPS, but the observed best was only 9.7 MSPS, likely due to Fmax penalties from the wide datapath or specific parameter choices in the search. However, the pipelined and pipelined_m families produce 1 result per cycle. To achieve 32 MSPS, a pipelined design only needs an Fmax of 32 MHz, which is easily achievable on Artix-7 even with moderate data widths. Furthermore, the accuracy constraint (max_abs_err <= 2^-12) is tight. The iterative designs struggled to reach 12 bits of accuracy without violating other constraints or being too slow. A pipelined design allows us to decouple throughput from latency (latency is N+2 cycles, but throughput is 1/cycle). We can use a higher N (e.g., 16-20) to ensure accuracy_bits >= 12, while keeping the clock frequency low enough to meet the area objective. The sys_p99_batch_us constraint (<= 0.44 us) is also critical. With a 32 MHz clock (31.25 ns/cycle), a latency of N+2 cycles must be <= 0.44 us / 31.25 ns/cycle = 14 cycles. So N+2 <= 14 => N <= 12. Wait, if Fmax is higher, say 100 MHz (10 ns/cycle), then 0.44 us = 44 cycles. N+2 <= 44 => N <= 42. This is very feasible. The key is that pipelined architectures can meet the 32 MSPS throughput easily and the latency constraint is manageable with a reasonable Fmax. The iterative/unrolled_k families are dead ends for the throughput constraint. We must explore pipelined and pipelined_m.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 11.7
- max_abs_err <= 0.000244141: 100% violate; best seen 0.00025 (2^-11.97)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 2.74

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=round]: throughput=11.7, max_abs_err=0.000311 (2^-11.65); throughput_msps >= 32 violated by 63.5%; max_abs_err <= 0.000244141 violated by 27.2%; sys_p99_batch_us <= 0.44 violated by 522.3%
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=0 rounding=round]: throughput=11, max_abs_err=0.000301 (2^-11.70); throughput_msps >= 32 violated by 65.6%; max_abs_err <= 0.000244141 violated by 23.4%; sys_p99_batch_us <= 0.44 violated by 559.0%
- iterative [data_width=16 n_iter=16 angle_guard=1 frac_guard=1 rounding=round]: throughput=10.4, max_abs_err=0.000274 (2^-11.83); throughput_msps >= 32 violated by 67.4%; max_abs_err <= 0.000244141 violated by 12.3%; sys_p99_batch_us <= 0.44 violated by 595.7%
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=1 rounding=round]: throughput=11, max_abs_err=0.00041 (2^-11.25); throughput_msps >= 32 violated by 65.6%; max_abs_err <= 0.000244141 violated by 67.8%; sys_p99_batch_us <= 0.44 violated by 559.0%
- iterative [data_width=16 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc]: throughput=10.4, max_abs_err=0.000333 (2^-11.55); throughput_msps >= 32 violated by 67.4%; max_abs_err <= 0.000244141 violated by 36.2%; sys_p99_batch_us <= 0.44 violated by 595.7%

Per family:
- iterative: 30 evals, 0 feasible; max throughput seen 11.7 MSPS; best accuracy 11.83 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 9.7 MSPS; best accuracy 11.97 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Switching to pipelined families to meet the throughput and latency constraints that iterative/unrolled_k cannot satisfy.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The spec requires a throughput of at least 32 MSPS and a system p99 batch latency of <= 0.44 us. The `iterative` and `unrolled_k` families explored in the previous 100 evaluations (the entire budget) are time-multiplexed architectures that produce one result every several cycles (N+3 or ceil(N/k)+3). Even with the maximum unrolling factor (k=8) and high Fmax, the maximum throughput observed was 22 MSPS (iterative) and 19.1 MSPS (unrolled_k), both significantly below the 32 MSPS constraint. Furthermore, the system latency constraint (0.44 us) is violated by a factor of >4x in the best cases (best seen 1.45 us). The remaining families (`pipelined` and `pipelined_m`) are the only ones capable of 1 result/cycle throughput, but they require N pipeline stages (or N/m) of latency. For N >= 12 (required for the accuracy constraint of 2^-12), the latency is at least 12 cycles. To meet the 0.44 us batch latency, the clock frequency would need to be > 27 MHz (12/0.44), which is trivially achievable, BUT the throughput constraint of 32 MSPS requires Fmax >= 32 MHz. While `pipelined` could theoretically meet throughput, the previous rounds did not explore them. However, looking closely at the `sys_p99_batch_us` constraint: it requires ALL 32 results to be back within 0.44 us of the tick. In a pipelined design with 1 result/cycle, if 32 requests arrive at once, they are processed sequentially. The 32nd result arrives 31 cycles after the first. If Fmax is 32 MHz (1 cycle = 31.25 ns), 31 cycles = 968 ns = 0.968 us, which violates the 0.44 us constraint. To meet 0.44 us for 32 sequential results, you need 31 cycles < 0.44 us, so Fmax > 31/0.44 = 70.4 MHz. This is possible on Artix-7. However, the `iterative` and `unrolled_k` families are fundamentally incapable of meeting the 32 MSPS throughput constraint as evidenced by the max 22 MSPS seen. Since the budget is exhausted (100/100 evals) and the final round is reached, and the only families capable of high throughput (`pipelined`) were not explored, we must determine if they are feasible. But wait, the prompt says 

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 22
- max_abs_err <= 0.000244141: 85% violate; best seen 3.12e-08 (2^-24.93)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 1.45

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=round]: throughput=11.7, max_abs_err=0.000311 (2^-11.65); throughput_msps >= 32 violated by 63.5%; max_abs_err <= 0.000244141 violated by 27.2%; sys_p99_batch_us <= 0.44 violated by 522.3%
- unrolled_k [data_width=17 n_iter=12 angle_guard=2 frac_guard=3 rounding=round k=3]: throughput=13.1, max_abs_err=0.000523 (2^-10.90); throughput_msps >= 32 violated by 59.0%; max_abs_err <= 0.000244141 violated by 114.2%; sys_p99_batch_us <= 0.44 violated by 452.2%
- unrolled_k [data_width=22 n_iter=12 angle_guard=4 frac_guard=1 rounding=trunc k=3]: throughput=12.7, max_abs_err=0.000489 (2^-11.00); throughput_msps >= 32 violated by 60.3%; max_abs_err <= 0.000244141 violated by 100.2%; sys_p99_batch_us <= 0.44 violated by 470.0%
- unrolled_k [data_width=22 n_iter=12 angle_guard=-2 frac_guard=1 rounding=round k=3]: throughput=12.7, max_abs_err=0.000494 (2^-10.98); throughput_msps >= 32 violated by 60.3%; max_abs_err <= 0.000244141 violated by 102.3%; sys_p99_batch_us <= 0.44 violated by 470.0%
- iterative [data_width=20 n_iter=12 angle_guard=4 frac_guard=3 rounding=trunc]: throughput=12.6, max_abs_err=0.000491 (2^-10.99); throughput_msps >= 32 violated by 60.5%; max_abs_err <= 0.000244141 violated by 101.0%; sys_p99_batch_us <= 0.44 violated by 474.5%

Per family:
- iterative: 50 evals, 0 feasible; max throughput seen 22 MSPS; best accuracy 24.93 bits
- unrolled_k: 50 evals, 0 feasible; max throughput seen 19.1 MSPS; best accuracy 20.61 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7992 in, 3390 out
- provider-reported cost: $0.0082
- full prompts and replies: `llm_trace.jsonl`

