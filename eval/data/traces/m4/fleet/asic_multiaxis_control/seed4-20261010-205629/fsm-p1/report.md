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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 11.5
- `max_abs_err <= 0.000244141`: met by 17/100 evaluations; best value seen 4.93e-07 (2^-20.95)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 2.78
- best throughput seen 11.5 MSPS (estimate); best accuracy 20.95 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Accuracy of 2^-12 max error needs roughly W>=14 with N around 12-14 and some guard bits, so I focus on W 12-16 and N 11-16. The batch bound of 32 results in 0.5 us demands high throughput, which only heavily unrolled designs could provide, so most of the budget goes to unrolled_k with high k, plus a small iterative probe to confirm infeasibility and map the low-area end.*)
- `unrolled_k` (45 evals): data_width=12..16, n_iter=11..16, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, k=6..8. *Why:* Constraints need 32 results within 0.5 us (about 64 results/us), so the single-result-per-cycle paths are unlikely without large k. High k with ceil(N/k)+3 cycles gives the most plausible fit for the batch bound, while sharing hardware to keep area low.
- `iterative` (15 evals): data_width=12..16, n_iter=11..16, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* Iterative at N+3 cycles per result almost certainly cannot clear 32 results in 0.5 us, but a small probe verifies this cheaply and shows the lower-area corner of the front.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — No feasible design in 60 evaluations. Iterative and unrolled_k peak at 11.5 and 5.55 MSPS against the 32 MSPS requirement, and their best sys_p99_batch_us is 2.78 against 0.5 (a 32-request burst has to drain within 0.5 us). Accepting one request every few cycles cannot meet that, so more refinement of these two families would not help. Only one-result-per-cycle designs (pipelined, pipelined_m) can plausibly clear both throughput and the burst deadline, and neither has been evaluated. Accuracy is reachable: the best seen is 2^-12.74 with n_iter around 13 and data_width 16, and about 95% of designs fail the 2^-12 error bound, so the next plan centres on data_width 14-18 and n_iter 12-17 with some guard bits. Pipelined_m is included because fewer registers should cut area, which is the objective.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 11.5
- max_abs_err <= 0.000244141: 95% violate; best seen 0.000146 (2^-12.74)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.78

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=2 rounding=round]: throughput=8.18, max_abs_err=0.000358 (2^-11.45); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 46.4%; sys_p99_batch_us <= 0.5 violated by 680.5%
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=2 rounding=trunc]: throughput=8.18, max_abs_err=0.000384 (2^-11.35); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 57.1%; sys_p99_batch_us <= 0.5 violated by 680.5%
- iterative [data_width=16 n_iter=13 angle_guard=3 frac_guard=1 rounding=round]: throughput=7.89, max_abs_err=0.000318 (2^-11.62); throughput_msps >= 32 violated by 75.3%; max_abs_err <= 0.000244141 violated by 30.4%; sys_p99_batch_us <= 0.5 violated by 709.7%
- iterative [data_width=15 n_iter=13 angle_guard=3 frac_guard=1 rounding=round]: throughput=8.18, max_abs_err=0.000445 (2^-11.14); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 82.1%; sys_p99_batch_us <= 0.5 violated by 680.5%
- iterative [data_width=16 n_iter=13 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=8.18, max_abs_err=0.000474 (2^-11.04); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 94.2%; sys_p99_batch_us <= 0.5 violated by 680.5%

Per family:
- iterative: 15 evals, 0 feasible; max throughput seen 11.5 MSPS; best accuracy 12.19 bits
- unrolled_k: 45 evals, 0 feasible; max throughput seen 5.55 MSPS; best accuracy 12.74 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Move to the pipelined families, which are the only ones able to meet throughput and burst-latency constraints, using the accuracy region identified in round 1.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — The budget is spent (100 of 100 evaluations) and this is the final round, so only stop or infeasible are allowed. None of the 100 evaluations is feasible, and the hypervolume is 0. I am not declaring infeasible because the evidence covers only iterative and unrolled_k. Their best throughput is 11.5 and 10.9 MSPS against the required 32, and their best sys_p99_batch_us is 2.78 against 0.5. That shows multi-cycle-per-result designs cannot meet the 32-requests-in-0.5-us burst. It does not show that pipelined or pipelined_m cannot, because neither appears in the per-family results and no evaluations were spent on them. They accept one request per cycle, so they are the only families in the registry that could plausibly meet the throughput and batch-latency constraints. The accuracy limit is reachable: 83% of designs violate it, but the best seen is 2^-20.95. So the limiting constraints are throughput and batch latency, not accuracy. Stopping with no feasible design; any further search should begin with pipelined or pipelined_m, with data_width around 14-16, n_iter around 13-16 and angle_guard of 2 or more, to meet the 2^-12 error bound at minimum area.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 11.5
- max_abs_err <= 0.000244141: 83% violate; best seen 4.93e-07 (2^-20.95)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.78

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=2 rounding=round]: throughput=8.18, max_abs_err=0.000358 (2^-11.45); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 46.4%; sys_p99_batch_us <= 0.5 violated by 680.5%
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=2 rounding=trunc]: throughput=8.18, max_abs_err=0.000384 (2^-11.35); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 57.1%; sys_p99_batch_us <= 0.5 violated by 680.5%
- iterative [data_width=16 n_iter=13 angle_guard=3 frac_guard=1 rounding=round]: throughput=7.89, max_abs_err=0.000318 (2^-11.62); throughput_msps >= 32 violated by 75.3%; max_abs_err <= 0.000244141 violated by 30.4%; sys_p99_batch_us <= 0.5 violated by 709.7%
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=round]: throughput=8, max_abs_err=0.000362 (2^-11.43); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 48.1%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=15 n_iter=13 angle_guard=3 frac_guard=1 rounding=round]: throughput=8.18, max_abs_err=0.000445 (2^-11.14); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 82.1%; sys_p99_batch_us <= 0.5 violated by 680.5%

Per family:
- iterative: 35 evals, 0 feasible; max throughput seen 11.5 MSPS; best accuracy 20.95 bits
- unrolled_k: 65 evals, 0 feasible; max throughput seen 10.9 MSPS; best accuracy 14.73 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 15648 in, 2677 out
- provider-reported cost: $0.0581
- full prompts and replies: `llm_trace.jsonl`

