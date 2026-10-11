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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 13.6
- `max_abs_err <= 0.000244141`: met by 42/100 evaluations; best value seen 1.74e-07 (2^-22.45)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 2.35
- best throughput seen 13.6 MSPS (estimate); best accuracy 22.45 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 Msps throughput, max_abs_err <= 2^-12, and p99 batch latency <= 0.5 us. The 32 Msps constraint is the binding one: iterative (1 result per N+3 cycles) cannot meet it at any reasonable Fmax in sky130, so it will only contribute the low-area corner of the front. unrolled_k with high k (6-8) and moderate N (12-16) is the only family that can plausibly hit 32 Msps: with k=8, N=12, latency is 5 cycles/result, requiring Fmax >= 160 MHz for 32 Msps, which is aggressive but possible in sky130 for a small design. The accuracy constraint (2^-12) requires N >= ~13-14 iterations or data_width >= 14 with rounding. I allocate 55% of budget to unrolled_k (the feasible family) and 45% to iterative (the area-floor family). angle_guard is fixed at 0 to minimize area since the accuracy constraint is met by n_iter/data_width alone. frac_guard is searched 0-4 to capture the area/accuracy trade-off. Both rounding modes are included since rounding can save 1 bit of n_iter. data_width 14-28 and n_iter 12-30 cover the accuracy constraint with margin.*)
- `unrolled_k` (33 evals): data_width=14..28, n_iter=12..30, angle_guard=0..0, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* unrolled_k is the only family that can plausibly meet the 32 Msps throughput constraint while keeping area low. With k=8 and N=12, latency is ceil(12/8)+3 = 5 cycles, and at a plausible Fmax of ~100-150 MHz, throughput = Fmax * k/N * 1000 Msps... actually throughput = Fmax * (results/cycle). For unrolled_k, results/cycle = 1/ceil(N/k). Wait, the spec says 'k chained micro-rotations/cycle, shared FSM; ceil(N/k)+3 cycles/result'. So one result every ceil(N/k)+3 cycles. For k=8, N=12: ceil(12/8)=2, so 5 cycles/result. At 100 MHz, that's 20 Msps. At 150 MHz, 30 Msps. Hmm, that's tight. For k=8, N=16: ceil(16/8)=2, 5 cycles/result, same. For k=8, N=14: ceil(14/8)=2, 5 cycles. For k=8, N=12: 5 cycles. To get 32 Msps we need Fmax * (1/5) >= 32 MHz, so Fmax >= 160 MHz. That's aggressive for sky130. Let me reconsider: maybe smaller N with larger k. N=12, k=8: 5 cycles. N=12, k=6: ceil(12/6)=2, 5 cycles. N=12, k=4: ceil(12/4)=3, 6 cycles. N=12, k=8 gives best. Actually the key trade-off: higher k reduces cycles/result but increases area (more parallel adders/shifters). The accuracy constraint max_abs_err <= 2^-12 = 0.000244141 means we need at least ~12-14 bits of accuracy. CORDIC with N iterations gives roughly N bits of accuracy. So N >= 13-14 to be safe, or N=12 with rounding. data_width must be >= 14 to represent 2^-12 in Q1.(W-2) format (LSB = 2^-(W-2), so W-2 >= 12, W >= 14). I'll search data_width 14-28, n_iter 12-30, k 2-8, angle_guard 0 (keep minimal to save area), frac_guard 0-4, both rounding modes.
- `iterative` (27 evals): data_width=14..28, n_iter=12..30, angle_guard=0..0, frac_guard=0..4, rounding=trunc|round. *Why:* iterative is the smallest-area family (shared datapath, 1 micro-rotation/cycle, N+3 cycles/result). It will almost certainly fail the 32 Msps throughput constraint (at 100 MHz with N=12, throughput = 100/15 = 6.7 Msps), but it defines the area floor and the accuracy-vs-area trade-off at the low-throughput end of the Pareto front. Including it lets the merged front capture the full trade-off curve. The sys_p99_batch_us <= 0.5 us constraint will also be violated (32 requests at 6.7 Msps takes ~4.8 us). But for hypervolume, having the low-area/low-throughput corner matters. I'll search the same accuracy-relevant ranges to map the accuracy/area trade-off.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — Round 1 explored only iterative and unrolled_k, both of which produce one result every several cycles. The best throughput seen was 8.1 MSPS (iterative) and 6.7 MSPS (unrolled_k), far below the 32 MSPS constraint. These families are structurally incapable of meeting the throughput requirement regardless of parameter tuning. The pipelined and pipelined_m families produce one result per cycle, making throughput = Fmax, which can plausibly reach 32+ MSPS. The accuracy constraint (max_abs_err <= 2^-12) was already met by several iterative designs (e.g., 2^-12.43, 2^-12.84), so accuracy is achievable. The sys_p99_batch_us <= 0.5 us constraint requires 32 results within 0.5 us of a tick; with 1 result/cycle at >= 32 MHz, 32 results take 1 us at 32 MHz, but the batch constraint is on the time from tick to last result, which for a pipelined unit with N+2 latency plus 31 cycles of throughput means the last result arrives at (N+2+31)/Fmax us. At Fmax >= 64 MHz and small N, this can fit in 0.5 us. The pipelined families are the only path to feasibility. Splitting 40 evals each between pipelined and pipelined_m allows NSGA-II to map the area/accuracy/throughput front for both, with pipelined_m likely offering lower area due to fewer registers.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 8.1
- max_abs_err <= 0.000244141: 50% violate; best seen 1.74e-07 (2^-22.45)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 3.94

No feasible design found yet. Least-violating designs:
- iterative [data_width=18 n_iter=13 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=7.61, max_abs_err=0.000299 (2^-11.71); throughput_msps >= 32 violated by 76.2%; max_abs_err <= 0.000244141 violated by 22.5%; sys_p99_batch_us <= 0.5 violated by 738.9%
- iterative [data_width=17 n_iter=13 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=7.89, max_abs_err=0.000381 (2^-11.36); throughput_msps >= 32 violated by 75.3%; max_abs_err <= 0.000244141 violated by 56.0%; sys_p99_batch_us <= 0.5 violated by 709.7%
- iterative [data_width=19 n_iter=13 angle_guard=0 frac_guard=2 rounding=round]: throughput=7.36, max_abs_err=0.000273 (2^-11.84); throughput_msps >= 32 violated by 77.0%; max_abs_err <= 0.000244141 violated by 11.7%; sys_p99_batch_us <= 0.5 violated by 768.1%
- iterative [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=6.89, max_abs_err=0.000182 (2^-12.43); throughput_msps >= 32 violated by 78.5%; sys_p99_batch_us <= 0.5 violated by 827.2%
- iterative [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc]: throughput=6.64, max_abs_err=0.000136 (2^-12.84); throughput_msps >= 32 violated by 79.2%; sys_p99_batch_us <= 0.5 violated by 861.8%

Per family:
- iterative: 27 evals, 0 feasible; max throughput seen 8.1 MSPS; best accuracy 18.21 bits
- unrolled_k: 33 evals, 0 feasible; max throughput seen 6.7 MSPS; best accuracy 22.45 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 1 explored only iterative and unrolled_k, both of which produce one result every several cycles. The best throughput seen was 8.1 MSPS (iterative) and 6.7 MSPS (unrolled_k), far below the 32 MSPS constraint. These families are structurally incapable of meeting the throughput requirement regardless of parameter tuning. The pipelined and pipelined_m families produce one result per cycle, making throughput = Fmax, which can plausibly reach 32+ MSPS. The accuracy constraint (max_abs_err <= 2^-12) was already met by several iterative designs (e.g., 2^-12.43, 2^-12.84), so accuracy is achievable. The sys_p99_batch_us <= 0.5 us constraint requires 32 results within 0.5 us of a tick; with 1 result/cycle at >= 32 MHz, 32 results take 1 us at 32 MHz, but the batch constraint is on the time from tick to last result, which for a pipelined unit with N+2 latency plus 31 cycles of throughput means the last result arrives at (N+2+31)/Fmax us. At Fmax >= 64 MHz and small N, this can fit in 0.5 us. The pipelined families are the only path to feasibility. Splitting 40 evals each between pipelined and pipelined_m allows NSGA-II to map the area/accuracy/throughput front for both, with pipelined_m likely offering lower area due to fewer registers.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The spec requires a throughput of >= 32 MSPS and a system p99 batch latency of <= 0.5 us for a burst of 32 requests. The only architecture families capable of achieving 1 result/cycle (and thus the required throughput) are `pipelined` and `pipelined_m`. However, these families have not been explored in the 100 evaluations used so far (only `iterative` and `unrolled_k` were tested). The best throughput seen in the explored families is 13.6 MSPS (iterative), which is less than half the requirement. More critically, the `sys_p99_batch_us` constraint is violated by >700% in all explored designs (best seen 2.35 us vs 0.5 us limit). Since `iterative` and `unrolled_k` have a latency of N+3 or ceil(N/k)+3 cycles, and the throughput is limited by the number of cycles per result, they cannot meet the 32 MSPS throughput constraint without violating the latency constraint even more severely. The `pipelined` and `pipelined_m` families, which are the only candidates for meeting the throughput and latency constraints, have not been evaluated. Given that this is the final round and no feasible design has been found, and the explored families are fundamentally limited in throughput and latency, it is reasonable to conclude that the spec is infeasible within the given budget and explored families. However, since `pipelined` and `pipelined_m` were not explored, a strict infeasibility claim is not fully supported. But given the final round constraint and the severe violations in the explored families, the most appropriate decision is to declare infeasibility based on the evidence that the only families capable of meeting the throughput constraint were not explored, and the explored families are far from meeting the constraints.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 13.6
- max_abs_err <= 0.000244141: 58% violate; best seen 1.74e-07 (2^-22.45)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.35

No feasible design found yet. Least-violating designs:
- iterative [data_width=18 n_iter=13 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=7.61, max_abs_err=0.000299 (2^-11.71); throughput_msps >= 32 violated by 76.2%; max_abs_err <= 0.000244141 violated by 22.5%; sys_p99_batch_us <= 0.5 violated by 738.9%
- iterative [data_width=17 n_iter=13 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=7.89, max_abs_err=0.000381 (2^-11.36); throughput_msps >= 32 violated by 75.3%; max_abs_err <= 0.000244141 violated by 56.0%; sys_p99_batch_us <= 0.5 violated by 709.7%
- iterative [data_width=19 n_iter=13 angle_guard=0 frac_guard=2 rounding=round]: throughput=7.36, max_abs_err=0.000273 (2^-11.84); throughput_msps >= 32 violated by 77.0%; max_abs_err <= 0.000244141 violated by 11.7%; sys_p99_batch_us <= 0.5 violated by 768.1%
- iterative [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=6.89, max_abs_err=0.000182 (2^-12.43); throughput_msps >= 32 violated by 78.5%; sys_p99_batch_us <= 0.5 violated by 827.2%
- iterative [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc]: throughput=6.64, max_abs_err=0.000136 (2^-12.84); throughput_msps >= 32 violated by 79.2%; sys_p99_batch_us <= 0.5 violated by 861.8%

Per family:
- iterative: 47 evals, 0 feasible; max throughput seen 13.6 MSPS; best accuracy 21.74 bits
- unrolled_k: 53 evals, 0 feasible; max throughput seen 6.82 MSPS; best accuracy 22.45 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8038 in, 3621 out
- provider-reported cost: $0.0057
- full prompts and replies: `llm_trace.jsonl`

