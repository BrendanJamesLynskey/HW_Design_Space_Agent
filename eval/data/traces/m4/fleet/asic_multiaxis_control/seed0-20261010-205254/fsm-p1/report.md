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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 12.8
- `max_abs_err <= 0.000244141`: met by 22/100 evaluations; best value seen 5.51e-08 (2^-24.11)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 2.49
- best throughput seen 12.8 MSPS (estimate); best accuracy 24.11 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The accuracy limit of 2^-12 implies about 12 bits of accuracy, so data_width should be around 12 to 16 and n_iter around 11 to 16, with guard bits used to cut rounding error. The batch constraint of 32 results in 0.5 us is tight, so most of the budget goes to unrolled_k with large k, where fewer cycles per result might meet the bound. The iterative family gets a small probe, since it likely fails the batch latency bound. Later rounds should narrow the width, n_iter and guard bits to minimise area while keeping accuracy at or above 12 bits.*)
- `unrolled_k` (45 evals): data_width=12..16, n_iter=11..16, angle_guard=0..3, frac_guard=1..3, rounding=trunc|round, k=4..8. *Why:* Throughput must be at least 32 results/us and all 32 results must be back within 0.5 us. That needs about 64 results/us at the batch level, so a unit that accepts a request every cycle is out. A high k cuts cycles per result, so high k at a modest clock is the only plausible route for this family to meet the bound, and it stays much smaller than a fully pipelined design.
- `iterative` (15 evals): data_width=12..15, n_iter=11..15, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* A small probe to check whether the iterative family can meet the constraints at all. With N+3 cycles per result, 32 results in 0.5 us look infeasible unless Fmax is very high. If it fails, the fleet can drop this family.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — No design is feasible. Throughput is the hardest constraint: the best seen is 11.5 MSPS for iterative and 6.45 for unrolled_k, against a requirement of 32. sys_p99_batch_us is 100% violated, with a best of 2.78 us against 0.5 us. Both families take several cycles per result, so a burst of 32 requests queues up. Only pipelined and pipelined_m accept one request per cycle, and the pipelined families have no evaluations in the results. Accuracy is reachable, since 17% of designs met 2^-12 and the best reached 2^-12.38, with data_width around 14-16, n_iter 12-16 and guard bits above 0. The next round therefore evaluates the pipelined families in the accuracy-feasible region. pipelined_m with small m is included to save flip-flops while keeping Fmax high enough for the 0.5 us batch window.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 11.5
- max_abs_err <= 0.000244141: 83% violate; best seen 0.000187 (2^-12.38)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.78

No feasible design found yet. Least-violating designs:
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=1 rounding=trunc]: throughput=9.43, max_abs_err=0.000833 (2^-10.23); throughput_msps >= 32 violated by 70.5%; max_abs_err <= 0.000244141 violated by 241.1%; sys_p99_batch_us <= 0.5 violated by 576.9%
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc]: throughput=7.86, max_abs_err=0.000567 (2^-10.78); throughput_msps >= 32 violated by 75.4%; max_abs_err <= 0.000244141 violated by 132.3%; sys_p99_batch_us <= 0.5 violated by 712.6%
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=0 rounding=trunc]: throughput=9.43, max_abs_err=0.00116 (2^-9.75); throughput_msps >= 32 violated by 70.5%; max_abs_err <= 0.000244141 violated by 374.1%; sys_p99_batch_us <= 0.5 violated by 576.9%
- iterative [data_width=14 n_iter=12 angle_guard=2 frac_guard=1 rounding=trunc]: throughput=9.43, max_abs_err=0.00116 (2^-9.75); throughput_msps >= 32 violated by 70.5%; max_abs_err <= 0.000244141 violated by 374.1%; sys_p99_batch_us <= 0.5 violated by 576.9%
- iterative [data_width=14 n_iter=11 angle_guard=2 frac_guard=2 rounding=round]: throughput=10.1, max_abs_err=0.00127 (2^-9.62); throughput_msps >= 32 violated by 68.4%; max_abs_err <= 0.000244141 violated by 421.6%; sys_p99_batch_us <= 0.5 violated by 531.7%

Per family:
- iterative: 15 evals, 0 feasible; max throughput seen 11.5 MSPS; best accuracy 10.78 bits
- unrolled_k: 45 evals, 0 feasible; max throughput seen 6.45 MSPS; best accuracy 12.38 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Only designs that accept one request per cycle can meet 32 MSPS and the burst deadline, so the budget goes to the pipelined families at accuracy-feasible widths and iteration counts.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — Round cap and budget are exhausted (100/100 evals), and no feasible design was found: hypervolume is 0 and 0 of 100 evaluations passed. Only iterative and unrolled_k were evaluated. They top out at 11.5 and 12.8 MSPS against the required 32, and the best sys_p99_batch_us is 2.49 against 0.5. Accuracy is not the blocker, since unrolled_k reaches 24.11 bits against the 12 needed. I am not declaring infeasible because the pipelined and pipelined_m families, which issue one result per cycle, have no evaluations in the per-family results. Their throughput could in principle clear the 32 MSPS and batch-latency constraints, but I have no numbers for them, so infeasibility of the whole registry is not proven. Stopping with no feasible front; the unexplored pipelined families are the only plausible route to feasibility if the budget were extended.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 12.8
- max_abs_err <= 0.000244141: 78% violate; best seen 5.51e-08 (2^-24.11)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.49

No feasible design found yet. Least-violating designs:
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=1 rounding=trunc]: throughput=9.43, max_abs_err=0.000833 (2^-10.23); throughput_msps >= 32 violated by 70.5%; max_abs_err <= 0.000244141 violated by 241.1%; sys_p99_batch_us <= 0.5 violated by 576.9%
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc]: throughput=7.86, max_abs_err=0.000567 (2^-10.78); throughput_msps >= 32 violated by 75.4%; max_abs_err <= 0.000244141 violated by 132.3%; sys_p99_batch_us <= 0.5 violated by 712.6%
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=0 rounding=trunc]: throughput=9.43, max_abs_err=0.00116 (2^-9.75); throughput_msps >= 32 violated by 70.5%; max_abs_err <= 0.000244141 violated by 374.1%; sys_p99_batch_us <= 0.5 violated by 576.9%
- iterative [data_width=14 n_iter=12 angle_guard=2 frac_guard=1 rounding=trunc]: throughput=9.43, max_abs_err=0.00116 (2^-9.75); throughput_msps >= 32 violated by 70.5%; max_abs_err <= 0.000244141 violated by 374.1%; sys_p99_batch_us <= 0.5 violated by 576.9%
- iterative [data_width=14 n_iter=11 angle_guard=2 frac_guard=2 rounding=round]: throughput=10.1, max_abs_err=0.00127 (2^-9.62); throughput_msps >= 32 violated by 68.4%; max_abs_err <= 0.000244141 violated by 421.6%; sys_p99_batch_us <= 0.5 violated by 531.7%

Per family:
- iterative: 35 evals, 0 feasible; max throughput seen 11.5 MSPS; best accuracy 19.70 bits
- unrolled_k: 65 evals, 0 feasible; max throughput seen 12.8 MSPS; best accuracy 24.11 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 15660 in, 2761 out
- provider-reported cost: $0.0589
- full prompts and replies: `llm_trace.jsonl`

