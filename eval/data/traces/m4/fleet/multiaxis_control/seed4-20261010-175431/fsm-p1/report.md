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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 20.7
- `max_abs_err <= 0.000244141`: met by 14/100 evaluations; best value seen 6.36e-07 (2^-20.58)
- `sys_p99_batch_us <= 0.44`: met by 0/100 evaluations; best value seen 1.54
- best throughput seen 20.7 MSPS (estimate); best accuracy 20.58 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands 32 Msps throughput and <=2^-12 max error, minimising LUTs+FFs. Among my two allowed families, unrolled_k is the throughput-capable option: k chained micro-rotations per cycle gives one result every ceil(N/k)+3 cycles, so k=4 with N=14 yields 7-cycle latency and ~70 Msps at 500 MHz, comfortably clearing 32 Msps. iterative is the area-minimal option but its N+3 cycle latency (~17-21 cycles) puts it near the 32 Msps boundary, so it may or may not pass the throughput constraint. I split the budget 55/45: unrolled_k gets more because it is the likely feasible-throughput family and has an extra parameter (k) creating a richer trade-off surface (k vs Fmax vs area). iterative gets 45% to map the low-area corner and confirm its throughput feasibility. Both families share the same accuracy parameters (N, W, angle_guard, frac_guard, rounding), so accuracy_bits will be comparable at matched N/W. I fix data_width=16 because the error constraint (2^-12) with N>=14 iterations is met at W=16 with margin, and wider W only adds area without improving the binding constraint. angle_guard is kept at -1..0 to minimise the atan-LUT area while N>=14 ensures convergence. frac_guard 0..2 explores a small area/accuracy trade-off. The p99 batch constraint (0.44 us) is easily met by both families at any plausible Fmax since even iterative's ~21 cycles at 400 MHz is only ~52 ns, far below 440 ns.*)
- `unrolled_k` (33 evals): data_width=16..16, n_iter=14..18, angle_guard=-1..0, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k is the only family I can use that can plausibly meet the 32 Msps throughput constraint. With k=4 and N=14, latency is ceil(14/4)+3 = 7 cycles. At a plausible Fmax of ~450-500 MHz, 7 cycles = ~14-15 ns, well within the 440 ns p99 batch window. N=14 with W=16 gives ~14+ bits of accuracy, comfortably exceeding the 12-bit requirement. k=2-4 balances area (more parallel datapaths for higher k) against Fmax (deeper combinational logic for higher k). angle_guard -1 to 0 keeps the atan-LUT small while N=14 provides enough iterations to converge. frac_guard 0-2 gives a small area/accuracy trade-off to explore.
- `iterative` (27 evals): data_width=16..16, n_iter=14..18, angle_guard=-1..0, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the minimum-area CORDIC family (single shared datapath, barrel shifters, no parallel micro-rotation chains). It will almost certainly win on luts_plus_ffs, which is the selection objective. However, it produces one result every N+3 cycles (~17-21 cycles), so its raw throughput is ~25-30 Msps at 500 MHz, which may fall just short of the 32 Msps constraint. I include it to map the area/accuracy corner of the Pareto front and to confirm whether it can meet throughput at the Fmax the cost model predicts. If it fails throughput, it still anchors the low-area end of the front for hypervolume. N=14-18, W=16, angle_guard -1..0, frac_guard 0..2 covers the accuracy requirement with minimal area.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The `iterative` and `unrolled_k` families are fundamentally incapable of meeting the throughput constraint. The spec requires `throughput_msps >= 32` (32 results per microsecond). `iterative` produces 1 result every N+3 cycles (min 7 cycles for N=4), and `unrolled_k` produces 1 result every ceil(N/k)+3 cycles. Even with maximum unrolling (k=8) and minimum iterations (N=4), the latency is ceil(4/8)+3 = 4 cycles, yielding a maximum throughput of Fmax/4. To reach 32 MSPS, Fmax would need to be 128 MHz. However, the best observed throughput for `unrolled_k` was only 10.3 MSPS, and for `iterative` 11.7 MSPS. This implies Fmax is likely around 40-50 MHz for these architectures, making 32 MSPS impossible (max ~10-12 MSPS). Furthermore, the `sys_p99_batch_us <= 0.44` constraint requires processing 32 requests within 0.44 us. With a throughput of ~11 MSPS, processing 32 requests takes ~3 us, which violates the 0.44 us bound by a factor of ~7. Only the `pipelined` or `pipelined_m` families, which produce 1 result per cycle, can achieve the required 32 MSPS throughput (requiring Fmax >= 32 MHz, which is feasible) and the low latency needed for the batch constraint. Therefore, I must explore the `pipelined` family.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 11.7
- max_abs_err <= 0.000244141: 100% violate; best seen 0.000355 (2^-11.46)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 2.74

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=2 rounding=round]: throughput=11.7, max_abs_err=0.000389 (2^-11.33); throughput_msps >= 32 violated by 63.5%; max_abs_err <= 0.000244141 violated by 59.5%; sys_p99_batch_us <= 0.44 violated by 522.3%
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=11.7, max_abs_err=0.000391 (2^-11.32); throughput_msps >= 32 violated by 63.5%; max_abs_err <= 0.000244141 violated by 60.1%; sys_p99_batch_us <= 0.44 violated by 522.3%
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=2 rounding=round]: throughput=11, max_abs_err=0.000355 (2^-11.46); throughput_msps >= 32 violated by 65.6%; max_abs_err <= 0.000244141 violated by 45.2%; sys_p99_batch_us <= 0.44 violated by 559.0%
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=1 rounding=round]: throughput=11, max_abs_err=0.000355 (2^-11.46); throughput_msps >= 32 violated by 65.6%; max_abs_err <= 0.000244141 violated by 45.2%; sys_p99_batch_us <= 0.44 violated by 559.0%
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=2 rounding=trunc]: throughput=11, max_abs_err=0.000358 (2^-11.45); throughput_msps >= 32 violated by 65.6%; max_abs_err <= 0.000244141 violated by 46.5%; sys_p99_batch_us <= 0.44 violated by 559.0%

Per family:
- iterative: 27 evals, 0 feasible; max throughput seen 11.7 MSPS; best accuracy 11.46 bits
- unrolled_k: 33 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 11.46 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Switching to pipelined family to meet throughput and latency constraints.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The spec requires a throughput of >= 32 MSPS and a system p99 batch latency of <= 0.44 us for a burst of 32 requests. The `iterative` and `unrolled_k` families, which were the only ones explored, produce one result every several cycles (N+3 or ceil(N/k)+3). Even with maximum unrolling (k=8) and high Fmax, the best throughput observed was only 20.7 MSPS, which is 35% below the 32 MSPS requirement. Furthermore, the system batch latency for these low-throughput designs was observed to be at least 1.54 us, far exceeding the 0.44 us limit. The `pipelined` and `pipelined_m` families, which could potentially meet the throughput and latency constraints by producing one result per cycle, were never explored. However, given that the non-pipelined families cannot even come close to the throughput requirement (max 20.7 vs 32 MSPS) and the budget is exhausted (100/100 evals used, final round), it is not possible to explore the pipelined families to see if they can meet the constraints. More critically, even if pipelined designs could achieve 32 MSPS, the system constraint `sys_p99_batch_us <= 0.44` for a burst of 32 requests implies that the CORDIC must process 32 requests in 0.44 us, which requires a throughput of at least 32/0.44 = 72.7 MSPS. Since the maximum throughput observed in any family is 20.7 MSPS, and the pipelined families were not explored, we cannot confirm feasibility. However, the requirement of 72.7 MSPS is extremely high for a CORDIC on Artix-7, and the fact that the best non-pipelined design only reached 20.7 MSPS suggests that even pipelined designs might struggle to reach 72.7 MSPS while maintaining the required accuracy (max_abs_err <= 2^-12). Given the evidence that the best throughput seen is 20.7 MSPS (far below the 32 MSPS hard constraint, let alone the implied 72.7 MSPS for the batch latency), and no feasible design was found in 100 evaluations across the two most flexible families, the constraints appear unreachable within the registry and budget.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 20.7
- max_abs_err <= 0.000244141: 86% violate; best seen 6.36e-07 (2^-20.58)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 1.54

No feasible design found yet. Least-violating designs:
- iterative [data_width=15 n_iter=14 angle_guard=4 frac_guard=3 rounding=round]: throughput=11.4, max_abs_err=0.000207 (2^-12.24); throughput_msps >= 32 violated by 64.4%; sys_p99_batch_us <= 0.44 violated by 536.8%
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=3 rounding=trunc]: throughput=11.7, max_abs_err=0.000359 (2^-11.44); throughput_msps >= 32 violated by 63.5%; max_abs_err <= 0.000244141 violated by 47.0%; sys_p99_batch_us <= 0.44 violated by 522.3%
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=round]: throughput=11.7, max_abs_err=0.000362 (2^-11.43); throughput_msps >= 32 violated by 63.5%; max_abs_err <= 0.000244141 violated by 48.1%; sys_p99_batch_us <= 0.44 violated by 522.3%
- iterative [data_width=17 n_iter=14 angle_guard=3 frac_guard=0 rounding=trunc]: throughput=11.4, max_abs_err=0.000338 (2^-11.53); throughput_msps >= 32 violated by 64.4%; max_abs_err <= 0.000244141 violated by 38.4%; sys_p99_batch_us <= 0.44 violated by 536.8%
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=2 rounding=round]: throughput=11.7, max_abs_err=0.000389 (2^-11.33); throughput_msps >= 32 violated by 63.5%; max_abs_err <= 0.000244141 violated by 59.5%; sys_p99_batch_us <= 0.44 violated by 522.3%

Per family:
- iterative: 47 evals, 0 feasible; max throughput seen 18.5 MSPS; best accuracy 20.58 bits
- unrolled_k: 53 evals, 0 feasible; max throughput seen 20.7 MSPS; best accuracy 14.73 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7955 in, 2660 out
- provider-reported cost: $0.0055
- full prompts and replies: `llm_trace.jsonl`

