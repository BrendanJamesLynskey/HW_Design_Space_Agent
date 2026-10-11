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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 10.9
- `max_abs_err <= 0.000244141`: met by 28/100 evaluations; best value seen 4.93e-07 (2^-20.95)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 2.91
- best throughput seen 10.9 MSPS (estimate); best accuracy 20.95 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraints are the system batch bound and accuracy, not the 32 msps average-throughput bound. A 1 MHz tick that dumps 32 requests and requires the last result within 0.5 us means the unit must drain at ~64 results/us during the burst, i.e. Fmax >= 64 * (cycles per result). Accuracy max_abs_err <= 2^-12 forces N >= ~13 and W >= ~14, which fixes the cycles-per-result options. For iterative that is >= 1024 MHz (hopeless), so unrolled_k is the real hope: with k=7..8 and N=13..16 it needs only 320 MHz, with k=5..6 it needs 384 MHz, k=4 needs 448 MHz, k=3 needs 512 MHz, k=2 needs 640 MHz. Since area scales roughly with k, the min-area feasible design sits at the smallest k whose model Fmax clears 64*ceil(N/k)+192 MHz, and that crossing point is exactly what round 1 must locate. I therefore give unrolled_k 80% of the budget over the full k range and the accuracy-relevant W/N window, and reserve 20% for iterative to establish feasibility with code-computed numbers. Round 2+ should narrow to the k/N band that survives, then let the reserved front-mapping pass sweep the full ranges of whichever families land on the front.*)
- `unrolled_k` (48 evals): data_width=13..18, n_iter=12..18, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* This is my only family that can plausibly clear the system batch bound. The tick issues 32 requests at once and the last must land within 0.5 us, so the unit must sustain ~64 results/us during a burst. unrolled_k needs ceil(N/k)+3 cycles/result, so it needs Fmax >= 64*(ceil(N/k)+3) MHz. Accuracy (max_abs_err <= 2^-12) forces N >= ~13, which pins the achievable cycle counts: c=5 for k>=7 (N<=16), c=6 for k=5..6, c=7 for k=4, c=8 for k=3, c=10 for k=2. So the feasible region, if it exists, is a narrow band where the model's Fmax for that k beats 64*c. k spans its full 2..8 range because the Fmax requirement grows with c while the critical path grows with k, so the crossing point is not obvious a priori; area is roughly proportional to k, so the min-area feasible point is likely at the smallest k that still hits its Fmax target. data_width 13..18 and n_iter 12..18 bracket the accuracy constraint (W=13/N=12 are right at the 2^-12 edge, W=16/N=14 gives margin) while letting the front extend to higher accuracy_bits for hypervolume. angle_guard/frac_guard are kept wide because they trade area for accuracy and may be the cheapest way to buy the last fraction of a bit.
- `iterative` (12 evals): data_width=13..18, n_iter=12..18, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Cheapest possible datapath (one shared micro-rotation stage), so if it could meet the batch bound it would dominate the min-area objective. But it needs N+3 cycles/result, i.e. 32*(N+3) cycles for a burst, so the batch bound demands Fmax >= 64*(N+3) MHz; with N >= 13 for 2^-12 accuracy that is >= 1024 MHz, which is implausible for a sky130 iterative CORDIC. I am spending a small share only to let code confirm/deny that with real numbers rather than my arithmetic, and to catch the case where the L1 batch bound is optimistic enough that a low-N iterative design slips through. Same accuracy-oriented ranges as unrolled_k so the two families are directly comparable.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — Every evaluation so far is from the two multi-cycle families (iterative, unrolled_k), and both are structurally incapable of the spec's throughput/burst demands: best throughput seen is 9.83 MSPS (iterative) and 7.32 MSPS (unrolled_k), i.e. 100% of designs violate throughput_msps >= 32, and sys_p99_batch_us is violated by 686-822% (best 3.25 us vs 0.5 us limit). These families emit one result every several cycles, so a 32-request burst cannot drain in 0.5 us no matter how the accuracy knobs are tuned. The registry's pipelined and pipelined_m families emit 1 result/cycle, so throughput_msps = Fmax (>=32 MSPS is easy) and a 32-request burst drains in ~latency+31 cycles, which at realistic Fmax lands inside the 0.5 us window. Accuracy is family-independent (identical bit-accurate datapath), and the accuracy constraint is already reachable (best seen 2^-14.27, and 2^-12.23/2^-12.40 designs exist), so the only missing ingredient is a 1-result/cycle family. Bring in pipelined and pipelined_m over their full ranges.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 9.83
- max_abs_err <= 0.000244141: 77% violate; best seen 5.07e-05 (2^-14.27)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 3.25

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=4 rounding=trunc]: throughput=7.61, max_abs_err=0.000325 (2^-11.59); throughput_msps >= 32 violated by 76.2%; max_abs_err <= 0.000244141 violated by 33.1%; sys_p99_batch_us <= 0.5 violated by 738.9%
- iterative [data_width=18 n_iter=12 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=8.12, max_abs_err=0.000528 (2^-10.89); throughput_msps >= 32 violated by 74.6%; max_abs_err <= 0.000244141 violated by 116.3%; sys_p99_batch_us <= 0.5 violated by 686.4%
- iterative [data_width=17 n_iter=15 angle_guard=0 frac_guard=2 rounding=round]: throughput=7.01, max_abs_err=0.000209 (2^-12.23); throughput_msps >= 32 violated by 78.1%; sys_p99_batch_us <= 0.5 violated by 811.1%
- iterative [data_width=17 n_iter=14 angle_guard=4 frac_guard=1 rounding=round]: throughput=6.93, max_abs_err=0.000185 (2^-12.40); throughput_msps >= 32 violated by 78.4%; sys_p99_batch_us <= 0.5 violated by 822.4%
- iterative [data_width=18 n_iter=12 angle_guard=4 frac_guard=3 rounding=trunc]: throughput=7.59, max_abs_err=0.0005 (2^-10.97); throughput_msps >= 32 violated by 76.3%; max_abs_err <= 0.000244141 violated by 104.7%; sys_p99_batch_us <= 0.5 violated by 741.1%

Per family:
- iterative: 12 evals, 0 feasible; max throughput seen 9.83 MSPS; best accuracy 13.31 bits
- unrolled_k: 48 evals, 0 feasible; max throughput seen 7.32 MSPS; best accuracy 14.27 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Add the two 1-result/cycle families; keep accuracy ranges around the region already shown to reach <=2^-12 (W 12-20, N 10-18, guards 0..4). This directly attacks the two 100%-violated constraints (throughput and sys_p99_batch_us) that the current families cannot satisfy.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — Budget is exhausted (100/100 evaluations, round 2 of 4) with 0 feasible designs and 0.0% hypervolume gain, so the front is empty and cannot be improved further this run. The two families actually evaluated (iterative, unrolled_k) are both multi-cycle-per-result and top out at 10.9 MSPS against the 32 MSPS requirement (3x short) and 2.91 us against the 0.5 us sys_p99_batch bound (~6x over), with 100% of evaluations violating both — so no design found can be selected without violating the spec. I do not claim `infeasible` for the whole registry: the 1-result/cycle families (pipelined, pipelined_m) were never evaluated and are the natural candidates for the throughput/burst constraint, so unreachability is not demonstrated by these numbers; the run simply ends with no feasible design in hand.
- **rule applied by code:** no feasible design found and the architect did not declare infeasibility

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 10.9
- max_abs_err <= 0.000244141: 72% violate; best seen 4.93e-07 (2^-20.95)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.91

No feasible design found yet. Least-violating designs:
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=round]: throughput=8, max_abs_err=0.000362 (2^-11.43); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 48.1%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=15 n_iter=14 angle_guard=4 frac_guard=3 rounding=round]: throughput=7.42, max_abs_err=0.000207 (2^-12.24); throughput_msps >= 32 violated by 76.8%; sys_p99_batch_us <= 0.5 violated by 760.4%
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=4 rounding=trunc]: throughput=7.61, max_abs_err=0.000325 (2^-11.59); throughput_msps >= 32 violated by 76.2%; max_abs_err <= 0.000244141 violated by 33.1%; sys_p99_batch_us <= 0.5 violated by 738.9%
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=3 rounding=trunc]: throughput=7.7, max_abs_err=0.000359 (2^-11.44); throughput_msps >= 32 violated by 75.9%; max_abs_err <= 0.000244141 violated by 47.0%; sys_p99_batch_us <= 0.5 violated by 729.4%
- iterative [data_width=18 n_iter=12 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=8.12, max_abs_err=0.000528 (2^-10.89); throughput_msps >= 32 violated by 74.6%; max_abs_err <= 0.000244141 violated by 116.3%; sys_p99_batch_us <= 0.5 violated by 686.4%

Per family:
- iterative: 32 evals, 0 feasible; max throughput seen 9.83 MSPS; best accuracy 20.95 bits
- unrolled_k: 68 evals, 0 feasible; max throughput seen 10.9 MSPS; best accuracy 14.73 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8684 in, 18826 out
- provider-reported cost: $0.0203
- full prompts and replies: `llm_trace.jsonl`

