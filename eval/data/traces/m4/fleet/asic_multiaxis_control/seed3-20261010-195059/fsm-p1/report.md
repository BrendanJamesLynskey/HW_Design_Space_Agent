# DSE run: asic_multiaxis_control

**Verdict:** NO FEASIBLE DESIGN FOUND within the budget (the architect did not declare infeasibility).  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 16.4
- `max_abs_err <= 0.000244141`: met by 33/100 evaluations; best value seen 1.41e-07 (2^-22.76)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 1.95
- best throughput seen 16.4 MSPS (estimate); best accuracy 22.76 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraint is the system burst: 32 requests must land within 0.5 us of the tick, i.e. an effective burst throughput of ~64 msps (with margin, ~70-80). For my families throughput_msps = Fmax/(ceil(N/k)+3) (unrolled_k) or Fmax/(N+3) (iterative). Accuracy (max_abs_err <= 2^-12) forces N >= ~13 (angle residual ~2^-N) and W >= 14 (output LSB 2^-(W-2)), so I search W 14..18, N 12..20. Iterative then needs Fmax >= 64*(N+3) >= ~1 GHz, which is far beyond sky130 for a 14-bit CORDIC, so it is almost certainly infeasible; I keep a small share to confirm and to catch the low-area corner if the model is unexpectedly fast. unrolled_k needs Fmax >= 64*(ceil(N/k)+3): 320 MHz at k=8/N=16, 448 MHz at k=4, 704 MHz at k=2. Since Fmax falls with k (longer combinational chain) while cycles/result also falls, the throughput optimum is at an intermediate k, so I sweep k 2..8. Area is minimised at small W, N, k, so the front is the accuracy/throughput boundary; angle_guard and frac_guard are swept modestly because they trade a little area for internal truncation margin.*)
- `unrolled_k` (54 evals): data_width=14..18, n_iter=12..20, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, k=2..8. *Why:* Only family of mine that can plausibly reach the ~64 msps burst rate: k chained micro-rotations cut cycles/result to ceil(N/k)+3 while keeping one shared datapath. Sweep k 2..8 to find the Fmax-vs-cycles optimum, N 12..20 and W 14..18 to trace the accuracy/area front, with small guard ranges.
- `iterative` (6 evals): data_width=14..18, n_iter=12..20, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* Smallest area (one micro-rotation/cycle) but N+3 >= 15 cycles/result, so it needs Fmax >= ~1 GHz to meet the 0.5 us batch — implausible in sky130. Small share to confirm infeasibility and to cover the low-area corner if the analytic Fmax is generous.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — Every evaluation so far violates throughput_msps >= 32 (100% violate; best seen 8.14 MSPS) and sys_p99_batch_us <= 0.5 (100% violate; best seen 3.92 us). This is structural, not a tuning problem: the two families explored, iterative (N+3 cycles/result) and unrolled_k (ceil(N/k)+3 cycles/result), both emit one result every several cycles, so their throughput is capped near 8 MSPS regardless of how the accuracy knobs are set. The spec needs 32 requests/us on average AND a 32-request burst drained within 0.5 us of the tick, which requires ~1 result/cycle. Only pipelined and pipelined_m in the registry provide 1 result/cycle (throughput = Fmax x 1), so they are the only families that can plausibly satisfy both the throughput and the batch constraint. Accuracy is family-independent (identical bit-level datapath), and the accuracy constraint is already reachable (best seen 2^-14.95, and 2^-12.61 at the least-violating point), so the binding issue is purely the schedule/throughput. Bring in the pipelined families and let the search trade area against Fmax/latency.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 8.14
- max_abs_err <= 0.000244141: 68% violate; best seen 3.15e-05 (2^-14.95)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 3.92

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=round k=2]: throughput=6.86, max_abs_err=0.00016 (2^-12.61); throughput_msps >= 32 violated by 78.6%; sys_p99_batch_us <= 0.5 violated by 829.7%
- unrolled_k [data_width=18 n_iter=12 angle_guard=1 frac_guard=1 rounding=round k=2]: throughput=7.63, max_abs_err=0.000522 (2^-10.90); throughput_msps >= 32 violated by 76.2%; max_abs_err <= 0.000244141 violated by 113.8%; sys_p99_batch_us <= 0.5 violated by 736.4%
- unrolled_k [data_width=15 n_iter=12 angle_guard=3 frac_guard=2 rounding=round k=2]: throughput=7.94, max_abs_err=0.000629 (2^-10.63); throughput_msps >= 32 violated by 75.2%; max_abs_err <= 0.000244141 violated by 157.6%; sys_p99_batch_us <= 0.5 violated by 703.6%
- unrolled_k [data_width=16 n_iter=12 angle_guard=2 frac_guard=1 rounding=trunc k=2]: throughput=7.94, max_abs_err=0.000643 (2^-10.60); throughput_msps >= 32 violated by 75.2%; max_abs_err <= 0.000244141 violated by 163.4%; sys_p99_batch_us <= 0.5 violated by 703.6%
- unrolled_k [data_width=17 n_iter=12 angle_guard=0 frac_guard=2 rounding=trunc k=2]: throughput=7.63, max_abs_err=0.0006 (2^-10.70); throughput_msps >= 32 violated by 76.2%; max_abs_err <= 0.000244141 violated by 145.6%; sys_p99_batch_us <= 0.5 violated by 736.4%

Per family:
- iterative: 6 evals, 0 feasible; max throughput seen 8 MSPS; best accuracy 14.95 bits
- unrolled_k: 54 evals, 0 feasible; max throughput seen 8.14 MSPS; best accuracy 13.92 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *n_iter kept 8..20 because accuracy only needs ~2^-12 (already achievable) and larger N directly worsens latency/area; data_width 12..20 spans the accuracy/area knee. angle_guard/frac_guard/rounding kept at full registry range since they are cheap accuracy levers. m 2..8 spans the register-count/latency trade-off for pipelined_m.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — Budget is exhausted (100/100 evals, round 2 of 4) and the feasible front is empty: 0/100 designs feasible, hypervolume 0, no gain this round. The two families actually evaluated cannot reach the binding throughput constraint — iterative peaks at 16.4 MSPS and unrolled_k at 10.1 MSPS against the required 32 MSPS (best design violates it by 78.6%), and the system batch bound is violated by 700-830% (best sys_p99_batch_us 1.95 vs 0.5). Accuracy is not the blocker: best max_abs_err 1.41e-07 (2^-22.76) is far inside 2^-12, so the failure is purely throughput/scheduling. I deliberately do NOT declare `infeasible`: the registry's pipelined and pipelined_m families (1 result/cycle, so throughput = Fmax in MSPS, needing only ~32 MHz plus N+2 cycles of latency to fit 32 results in 0.5 us) were never evaluated in the per-family breakdown, so the evidence does not prove that no registry family can meet the constraints — it only proves the two families searched cannot. With no evaluation budget left to test them, the run stops here rather than settling on a constraint-violating design.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 16.4
- max_abs_err <= 0.000244141: 67% violate; best seen 1.41e-07 (2^-22.76)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 1.95

No feasible design found yet. Least-violating designs:
- unrolled_k [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=round k=2]: throughput=6.86, max_abs_err=0.00016 (2^-12.61); throughput_msps >= 32 violated by 78.6%; sys_p99_batch_us <= 0.5 violated by 829.7%
- unrolled_k [data_width=18 n_iter=12 angle_guard=1 frac_guard=1 rounding=round k=2]: throughput=7.63, max_abs_err=0.000522 (2^-10.90); throughput_msps >= 32 violated by 76.2%; max_abs_err <= 0.000244141 violated by 113.8%; sys_p99_batch_us <= 0.5 violated by 736.4%
- unrolled_k [data_width=15 n_iter=12 angle_guard=3 frac_guard=2 rounding=round k=2]: throughput=7.94, max_abs_err=0.000629 (2^-10.63); throughput_msps >= 32 violated by 75.2%; max_abs_err <= 0.000244141 violated by 157.6%; sys_p99_batch_us <= 0.5 violated by 703.6%
- unrolled_k [data_width=16 n_iter=12 angle_guard=2 frac_guard=1 rounding=trunc k=2]: throughput=7.94, max_abs_err=0.000643 (2^-10.60); throughput_msps >= 32 violated by 75.2%; max_abs_err <= 0.000244141 violated by 163.4%; sys_p99_batch_us <= 0.5 violated by 703.6%
- unrolled_k [data_width=17 n_iter=12 angle_guard=0 frac_guard=2 rounding=trunc k=2]: throughput=7.63, max_abs_err=0.0006 (2^-10.70); throughput_msps >= 32 violated by 76.2%; max_abs_err <= 0.000244141 violated by 145.6%; sys_p99_batch_us <= 0.5 violated by 736.4%

Per family:
- iterative: 26 evals, 0 feasible; max throughput seen 16.4 MSPS; best accuracy 22.76 bits
- unrolled_k: 74 evals, 0 feasible; max throughput seen 10.1 MSPS; best accuracy 20.61 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8750 in, 17372 out
- provider-reported cost: $0.0204
- full prompts and replies: `llm_trace.jsonl`

