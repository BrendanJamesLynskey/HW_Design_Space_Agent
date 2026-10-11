# DSE run: asic_multiaxis_control

**Verdict:** NO FEASIBLE DESIGN FOUND within the budget (the architect did not declare infeasibility).  
**Architect (LLM):** openrouter: anthropic/claude-sonnet-5.5.  
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
- `max_abs_err <= 0.000244141`: met by 17/100 evaluations; best value seen 1.15e-06 (2^-19.73)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 1.62
- best throughput seen 19.7 MSPS (estimate); best accuracy 19.73 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Accuracy of 2^-12 needs about 12-bit-plus precision, so I use W 12-16 and N 11-16 with guard bits. The burst constraint of 32 results in 0.5 us is hard for non-pipelined families, because each result takes several cycles. I weight the budget toward unrolled_k at high k, since it is the only one with any chance of meeting it, and keep a small iterative share as a baseline. If round 1 shows these families cannot meet the constraints, I will report infeasibility for my families and leave the pipelined families to the rest of the fleet.*)
- `unrolled_k` (45 evals): data_width=12..16, n_iter=11..16, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, k=6..8. *Why:* The system needs 32 results within 0.5 us, so throughput must be at least 64 results/us. With k=6..8, the cycle count is ceil(N/k)+3, about 5 cycles, so 32 results take roughly 160 cycles and this needs very high Fmax. Likely infeasible on cycles alone, but unrolled_k is the only shared-datapath option that could plausibly come close, so I probe it at high k.
- `iterative` (15 evals): data_width=12..16, n_iter=11..16, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* Smallest-area baseline. It needs N+3 cycles per result, so a throughput of 32 results/us is very unlikely. It serves as a reference point to confirm infeasibility and to map the accuracy/area trade-off.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — No feasible design in 60 evals. Throughput peaked at 10.3 MSPS (iterative) and 5.55 MSPS (unrolled_k) against the 32 MSPS requirement. sys_p99_batch_us is at best 3.11 against 0.5. Both families accept one request every several cycles, so a burst of 32 queues. Only the pipelined families give one result per cycle, which is what the throughput and burst-latency constraints need. Accuracy is reachable: iterative at W=15, N=15, guards 3/3 with rounding reached 2^-12.38, and W=15 with guards 1/1 gave 2^-11.25. So the next round should search pipelined and pipelined_m around W 14-17 and N 13-17 with rounding, and keep area low by using pipelined_m with larger m to cut flip-flops.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 10.3
- max_abs_err <= 0.000244141: 98% violate; best seen 0.000188 (2^-12.38)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 3.11

No feasible design found yet. Least-violating designs:
- iterative [data_width=15 n_iter=15 angle_guard=3 frac_guard=3 rounding=round]: throughput=7.27, max_abs_err=0.000188 (2^-12.38); throughput_msps >= 32 violated by 77.3%; sys_p99_batch_us <= 0.5 violated by 778.3%
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=1 rounding=round]: throughput=7.86, max_abs_err=0.00041 (2^-11.25); throughput_msps >= 32 violated by 75.4%; max_abs_err <= 0.000244141 violated by 67.8%; sys_p99_batch_us <= 0.5 violated by 712.6%
- iterative [data_width=13 n_iter=13 angle_guard=3 frac_guard=3 rounding=round]: throughput=8.84, max_abs_err=0.000681 (2^-10.52); throughput_msps >= 32 violated by 72.4%; max_abs_err <= 0.000244141 violated by 178.8%; sys_p99_batch_us <= 0.5 violated by 622.2%
- iterative [data_width=13 n_iter=14 angle_guard=3 frac_guard=3 rounding=round]: throughput=8.32, max_abs_err=0.000615 (2^-10.67); throughput_msps >= 32 violated by 74.0%; max_abs_err <= 0.000244141 violated by 152.1%; sys_p99_batch_us <= 0.5 violated by 667.4%
- iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=1 rounding=round]: throughput=7.45, max_abs_err=0.00041 (2^-11.25); throughput_msps >= 32 violated by 76.7%; max_abs_err <= 0.000244141 violated by 67.8%; sys_p99_batch_us <= 0.5 violated by 757.8%

Per family:
- iterative: 15 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 12.38 bits
- unrolled_k: 45 evals, 0 feasible; max throughput seen 5.55 MSPS; best accuracy 11.78 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Accuracy needs roughly W 14-17 and N 13-17 with rounding, based on the iterative results. Throughput and batch latency need a one-result-per-cycle pipeline, so both pipelined families are searched at these accuracy-capable ranges.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined_m', 'pipelined'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — This is the final round and the 100-eval budget is spent, so only stop or infeasible are allowed. The hypervolume is 0 with 0 of 100 designs feasible. Iterative and unrolled_k both fail throughput_msps >= 32 (best 19.7 and 9.94 MSPS) and sys_p99_batch_us <= 0.5 (best 1.62 us). Both families accept a request only every several cycles, so the 32-request burst queues. The accuracy constraint is reachable: the best design reaches 2^-19.73, and several designs near 2^-12.4 sit just inside the limit. I do not declare infeasible because the per-family results show no evaluations of pipelined or pipelined_m. Those families accept one request per cycle and would be the natural fit for the burst, but the evidence here does not show whether they meet the constraints. No feasible design was found, so no valid selection can be made from this run.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 19.7
- max_abs_err <= 0.000244141: 83% violate; best seen 1.15e-06 (2^-19.73)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 1.62

No feasible design found yet. Least-violating designs:
- iterative [data_width=15 n_iter=15 angle_guard=3 frac_guard=3 rounding=round]: throughput=7.27, max_abs_err=0.000188 (2^-12.38); throughput_msps >= 32 violated by 77.3%; sys_p99_batch_us <= 0.5 violated by 778.3%
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=1 rounding=round]: throughput=7.86, max_abs_err=0.00041 (2^-11.25); throughput_msps >= 32 violated by 75.4%; max_abs_err <= 0.000244141 violated by 67.8%; sys_p99_batch_us <= 0.5 violated by 712.6%
- iterative [data_width=20 n_iter=12 angle_guard=0 frac_guard=0 rounding=round]: throughput=8.12, max_abs_err=0.000497 (2^-10.98); throughput_msps >= 32 violated by 74.6%; max_abs_err <= 0.000244141 violated by 103.5%; sys_p99_batch_us <= 0.5 violated by 686.4%
- iterative [data_width=13 n_iter=13 angle_guard=3 frac_guard=3 rounding=round]: throughput=8.84, max_abs_err=0.000681 (2^-10.52); throughput_msps >= 32 violated by 72.4%; max_abs_err <= 0.000244141 violated by 178.8%; sys_p99_batch_us <= 0.5 violated by 622.2%
- iterative [data_width=13 n_iter=14 angle_guard=3 frac_guard=3 rounding=round]: throughput=8.32, max_abs_err=0.000615 (2^-10.67); throughput_msps >= 32 violated by 74.0%; max_abs_err <= 0.000244141 violated by 152.1%; sys_p99_batch_us <= 0.5 violated by 667.4%

Per family:
- iterative: 35 evals, 0 feasible; max throughput seen 19.7 MSPS; best accuracy 19.73 bits
- unrolled_k: 65 evals, 0 feasible; max throughput seen 9.94 MSPS; best accuracy 18.96 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 15596 in, 2778 out
- provider-reported cost: $0.0590
- full prompts and replies: `llm_trace.jsonl`

