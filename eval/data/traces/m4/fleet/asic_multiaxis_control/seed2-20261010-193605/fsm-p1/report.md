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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 13.6
- `max_abs_err <= 0.000244141`: met by 30/100 evaluations; best value seen 2.86e-07 (2^-21.74)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 2.35
- best throughput seen 13.6 MSPS (estimate); best accuracy 21.74 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Two constraints dominate the geometry. (1) Accuracy: max_abs_err <= 2^-12 needs N >= ~13 micro-rotations and W >= ~14 (output LSB 2^-(W-2)), so the useful search box is N 12..20, W 12..18, with angle_guard/frac_guard/rounding as the fine-tuning knobs. (2) The system scenario: a 1 MHz tick dumps 32 requests at once and all must land within 0.5 us, i.e. ~64 Msps burst service, twice the 32 Msps average constraint. For serial families this means cycles-per-result C = ceil(N/k)+3 (unrolled_k) or N+3 (iterative) must be small at high Fmax. iterative is essentially out (C>=15 needs ~1 GHz); unrolled_k is the only family I own with a shot, and only at large k. So the budget is weighted 70/30 toward unrolled_k, sweeping k across its full 2..8 range to expose the C-vs-Fmax trade-off, while iterative anchors the low-area end. I am not pre-empting the infeasibility decision: code computes Fmax, area and the L1 batch bound, and if no point clears all three constraints the correct outcome is `infeasible` rather than a violating design.*)
- `unrolled_k` (42 evals): data_width=12..18, n_iter=12..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, k=2..8. *Why:* Only family I own that can plausibly reach the burst rate. The system constraint (32 results within 0.5 us of a 1 MHz tick) demands ~64 Msps of burst service, i.e. cycles-per-result C = ceil(N/k)+3 must be small while Fmax stays high. Accuracy (max_abs_err <= 2^-12) pins N to roughly 13-16 and W to roughly 14-16, so C is minimised by pushing k up (k=8 gives C=5 at N=13-16). The k sweep 2..8 is exactly the C-vs-Fmax trade-off the front needs: large k lowers C but lengthens the combinational chain, small k does the reverse. angle_guard/frac_guard/rounding are swept because they buy accuracy bits cheaply and let the search trade area for error near the 2^-12 boundary.
- `iterative` (18 evals): data_width=12..18, n_iter=12..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* Area baseline and the cheapest possible datapath (one shared micro-rotation, barrel shifters). C = N+3 >= 15 at the N needed for 2^-12, so it almost certainly cannot satisfy sys_p99_batch_us <= 0.5 us, but it is the minimum-area anchor of the accuracy/area curve and the reference point for the fleet's merged front. Keeping it in the search is cheap insurance in case the L1 batch bound is looser than the serial-service model suggests, and it gives the hypervolume a low-area end if any iterative point is feasible.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — Both explored families are structurally unable to reach the throughput constraint: iterative and unrolled_k issue one result every several cycles, and their best observed throughput is 9.47 MSPS and 8.43 MSPS respectively, i.e. 100% of evaluations violate throughput_msps >= 32. The system constraint sys_p99_batch_us <= 0.5 is also violated by ~700-940% because 32 back-to-back requests cannot be drained at <10 MSPS. The registry contains two families not yet tried, pipelined and pipelined_m, which produce 1 result/cycle (throughput = Fmax) and have short latency (N+2 or ceil(N/m)+2 cycles). Those are the only families whose structure can plausibly satisfy both the 32 MSPS throughput and the 0.5 us batch bound, so the next round should bring them in.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 9.47
- max_abs_err <= 0.000244141: 70% violate; best seen 3.99e-05 (2^-14.61)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 3.37

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round]: throughput=8, max_abs_err=0.000342 (2^-11.51); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 40.0%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc]: throughput=7.42, max_abs_err=0.000205 (2^-12.25); throughput_msps >= 32 violated by 76.8%; sys_p99_batch_us <= 0.5 violated by 760.4%
- iterative [data_width=18 n_iter=14 angle_guard=1 frac_guard=3 rounding=trunc]: throughput=6.93, max_abs_err=0.000157 (2^-12.64); throughput_msps >= 32 violated by 78.4%; sys_p99_batch_us <= 0.5 violated by 822.4%
- iterative [data_width=15 n_iter=14 angle_guard=0 frac_guard=2 rounding=round]: throughput=8, max_abs_err=0.000741 (2^-10.40); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 203.5%; sys_p99_batch_us <= 0.5 violated by 698.4%
- unrolled_k [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round k=3]: throughput=6.14, max_abs_err=0.000168 (2^-12.54); throughput_msps >= 32 violated by 80.8%; sys_p99_batch_us <= 0.5 violated by 938.6%

Per family:
- iterative: 18 evals, 0 feasible; max throughput seen 9.47 MSPS; best accuracy 14.48 bits
- unrolled_k: 42 evals, 0 feasible; max throughput seen 8.43 MSPS; best accuracy 14.61 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Focus the remaining 40 evaluations on the two 1-result/cycle families. Keep data_width and n_iter ranges wide enough to expose the area/accuracy Pareto front, but cap n_iter at 16 so latency does not dominate the 0.5 us batch budget. If the L1 system bound is met, the L2 simulation will later re-check the cheapest designs.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `stop` — Budget is exhausted (100/100 evals, round 2 of 4, final round) with 0 feasible designs and hypervolume 0, so there is nothing to refine or map. The binding constraints are throughput and batch latency, not accuracy: best accuracy seen is 2^-21.74 (far better than the 2^-12 requirement), while the best throughput is 13.6 MSPS (iterative) and 8.43 MSPS (unrolled_k) against the required 32 MSPS, and the best sys_p99_batch_us is 2.35 us against the required 0.5 us — both off by more than 2x. Both explored families issue one result every several cycles, so at the observed Fmax they structurally cannot reach 32 MSPS. I do not claim infeasibility for the registry as a whole, because the one-result-per-cycle families (pipelined, pipelined_m) were never evaluated and are the only plausible route to 32 MSPS; with no evaluations left, the honest verdict is to stop with no feasible design found rather than assert infeasibility without evidence.
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
- max_abs_err <= 0.000244141: 70% violate; best seen 2.86e-07 (2^-21.74)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.35

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round]: throughput=8, max_abs_err=0.000342 (2^-11.51); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 40.0%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc]: throughput=7.42, max_abs_err=0.000205 (2^-12.25); throughput_msps >= 32 violated by 76.8%; sys_p99_batch_us <= 0.5 violated by 760.4%
- iterative [data_width=18 n_iter=14 angle_guard=1 frac_guard=3 rounding=trunc]: throughput=6.93, max_abs_err=0.000157 (2^-12.64); throughput_msps >= 32 violated by 78.4%; sys_p99_batch_us <= 0.5 violated by 822.4%
- iterative [data_width=15 n_iter=14 angle_guard=0 frac_guard=2 rounding=round]: throughput=8, max_abs_err=0.000741 (2^-10.40); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 203.5%; sys_p99_batch_us <= 0.5 violated by 698.4%
- unrolled_k [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round k=3]: throughput=6.14, max_abs_err=0.000168 (2^-12.54); throughput_msps >= 32 violated by 80.8%; sys_p99_batch_us <= 0.5 violated by 938.6%

Per family:
- iterative: 38 evals, 0 feasible; max throughput seen 13.6 MSPS; best accuracy 21.74 bits
- unrolled_k: 62 evals, 0 feasible; max throughput seen 8.43 MSPS; best accuracy 20.73 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8632 in, 9161 out
- provider-reported cost: $0.0112
- full prompts and replies: `llm_trace.jsonl`

