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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 13.6
- `max_abs_err <= 0.000244141`: met by 15/100 evaluations; best value seen 2.86e-07 (2^-21.74)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 2.35
- best throughput seen 13.6 MSPS (estimate); best accuracy 21.74 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Error <= 2^-12 needs roughly 13-14 bit data width and about 12-14 iterations, so the ranges stay narrow around that. The batch constraint of 32 results in 0.5 us is very tight for a single non-pipelined unit, so most of the budget goes to unrolled_k with high k, which is the only family here that might meet it. A small share goes to iterative to check feasibility. Later rounds will narrow the ranges based on the results.*)
- `unrolled_k` (45 evals): data_width=13..16, n_iter=11..15, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, k=4..8. *Why:* 32 results within 0.5 us needs about 64 results/us (the batch is serial), i.e. a result every cycle at 64+ MHz or faster. Unrolling with k=4..8 shortens the per-result cycle count. If Fmax allows, k near 8 gets ceil(N/k)+3 close to 5 cycles. Narrow width and iteration ranges keep area small while holding error at or below 2^-12.
- `iterative` (15 evals): data_width=13..16, n_iter=11..15, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* The iterative design is the smallest, but it takes N+3 cycles per result and cannot serve 32 requests in 0.5 us unless it is extremely fast. A small budget share confirms feasibility and gives a low-area reference point for the front.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — No design is feasible after 60 evals. Throughput peaked at 10.3 MSPS for iterative and 5.83 for unrolled_k, against a requirement of 32. The best sys_p99_batch_us was 3.11, against a limit of 0.5. Multi-cycle families accept one request every several cycles, so the 32-request burst queues. Only a 1 result/cycle design can drain the burst, so pipelined and pipelined_m must be tried. Accuracy is reachable: unrolled_k reached 12.93 bits, so the 2^-12 limit needs roughly 16-bit width, 14-16 iterations and some guard bits. The next plan therefore targets pipelined and pipelined_m in that region. pipelined_m with small m is included to trade registers (area) against Fmax and latency cycles.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 10.3
- max_abs_err <= 0.000244141: 95% violate; best seen 0.000128 (2^-12.93)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 3.11

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc]: throughput=8, max_abs_err=0.000401 (2^-11.28); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 64.4%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=16 n_iter=12 angle_guard=0 frac_guard=1 rounding=trunc]: throughput=9.07, max_abs_err=0.000711 (2^-10.46); throughput_msps >= 32 violated by 71.7%; max_abs_err <= 0.000244141 violated by 191.3%; sys_p99_batch_us <= 0.5 violated by 604.3%
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=0 rounding=round]: throughput=9.43, max_abs_err=0.000917 (2^-10.09); throughput_msps >= 32 violated by 70.5%; max_abs_err <= 0.000244141 violated by 275.6%; sys_p99_batch_us <= 0.5 violated by 576.9%
- iterative [data_width=15 n_iter=12 angle_guard=0 frac_guard=2 rounding=round]: throughput=9.07, max_abs_err=0.000927 (2^-10.07); throughput_msps >= 32 violated by 71.7%; max_abs_err <= 0.000244141 violated by 279.9%; sys_p99_batch_us <= 0.5 violated by 604.3%
- iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=3 rounding=round]: throughput=8, max_abs_err=0.000694 (2^-10.49); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 184.2%; sys_p99_batch_us <= 0.5 violated by 698.4%

Per family:
- iterative: 15 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 11.28 bits
- unrolled_k: 45 evals, 0 feasible; max throughput seen 5.83 MSPS; best accuracy 12.93 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Both pipelined families give 1 result/cycle, the only way to meet the throughput and batch-latency constraints. Ranges are centred on the accuracy region already found.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — This is the final round, so only stop or infeasible is allowed. After 100 evaluations there is no feasible design and the hypervolume is 0. Only iterative and unrolled_k were actually evaluated (35 and 65 evals). Their best throughput was 13.6 and 6.82 MSPS against the required 32, and the best sys_p99_batch_us was 2.35 against 0.5. Both families accept one request every several cycles, so a 32-request burst queues. I am not declaring infeasible, because pipelined and pipelined_m (1 result/cycle) were never evaluated, so the evidence does not show that no registry design can meet the constraints. The accuracy constraint is reachable: max_abs_err reached 2.86e-07 (2^-21.74), and 85% of evaluations violated it. The pipelined families are the only plausible way to meet the throughput and batch-latency constraints. I report no feasible front and recommend that they be tried first if the budget is ever extended.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 13.6
- max_abs_err <= 0.000244141: 85% violate; best seen 2.86e-07 (2^-21.74)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.35

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc]: throughput=8, max_abs_err=0.000401 (2^-11.28); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 64.4%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=16 n_iter=12 angle_guard=0 frac_guard=1 rounding=trunc]: throughput=9.07, max_abs_err=0.000711 (2^-10.46); throughput_msps >= 32 violated by 71.7%; max_abs_err <= 0.000244141 violated by 191.3%; sys_p99_batch_us <= 0.5 violated by 604.3%
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=0 rounding=round]: throughput=9.43, max_abs_err=0.000917 (2^-10.09); throughput_msps >= 32 violated by 70.5%; max_abs_err <= 0.000244141 violated by 275.6%; sys_p99_batch_us <= 0.5 violated by 576.9%
- iterative [data_width=15 n_iter=12 angle_guard=0 frac_guard=2 rounding=round]: throughput=9.07, max_abs_err=0.000927 (2^-10.07); throughput_msps >= 32 violated by 71.7%; max_abs_err <= 0.000244141 violated by 279.9%; sys_p99_batch_us <= 0.5 violated by 604.3%
- iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=3 rounding=round]: throughput=8, max_abs_err=0.000694 (2^-10.49); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 184.2%; sys_p99_batch_us <= 0.5 violated by 698.4%

Per family:
- iterative: 35 evals, 0 feasible; max throughput seen 13.6 MSPS; best accuracy 21.74 bits
- unrolled_k: 65 evals, 0 feasible; max throughput seen 6.82 MSPS; best accuracy 20.73 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 15644 in, 2596 out
- provider-reported cost: $0.0572
- full prompts and replies: `llm_trace.jsonl`

