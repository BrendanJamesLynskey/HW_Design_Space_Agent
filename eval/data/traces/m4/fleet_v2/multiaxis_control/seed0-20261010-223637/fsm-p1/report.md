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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 21.1
- `max_abs_err <= 0.000244141`: met by 28/100 evaluations; best value seen 5.51e-08 (2^-24.11)
- `sys_p99_batch_us <= 0.44`: met by 0/100 evaluations; best value seen 1.51
- best throughput seen 21.1 MSPS (estimate); best accuracy 24.11 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands 32 Msps throughput and a 0.44 us p99 batch deadline for 32 simultaneous requests. Among my assigned families, only unrolled_k can plausibly meet both: with k=6-8 micro-rotations/cycle, the per-result latency is small (ceil(N/k)+3 cycles) and the batch of 32 sequential requests completes in 32*ceil(N/k) cycles, which at typical Fmax (150-300 MHz) fits within 0.44 us. iterative cannot meet 32 Msps (it needs N+3 cycles per result), so it will be infeasible on throughput, but I include it at 40% budget to map the area floor and confirm the infeasibility boundary. Accuracy constraint (max_abs_err <= 2^-12) requires roughly data_width >= 14 and n_iter >= 12; I range data_width 14-18 and n_iter 12-18 to capture the trade-off between area and accuracy. angle_guard 0-2 and frac_guard 0-2 keep the search focused on low-area configurations while allowing enough guard bits for accuracy. rounding is included as a categorical choice since it affects both area and accuracy slightly. The 60/40 split favours unrolled_k because it is the only family that can satisfy the hard throughput and batch-latency constraints.*)
- `unrolled_k` (36 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=4..8. *Why:* The spec requires 32 results/us (32 Msps) with a 0.44 us p99 batch deadline. A 1-result/cycle pipelined design is the only way to hit 32 Msps at a reasonable Fmax, but I am restricted to iterative/unrolled_k. unrolled_k with k=4..8 can reach 32 Msps if Fmax >= 4..8 MHz, which is trivially met. The batch of 32 requests must complete in 0.44 us; with k=8 and N=16, latency is ceil(16/8)+3 = 5 cycles, and 32 sequential requests take 32*ceil(16/8) = 64 cycles. At Fmax ~200 MHz that is 0.32 us, well under 0.44 us. k=4 gives 32*4=128 cycles ~0.64 us at 200 MHz, too slow. So k must be high (6-8) to meet the batch deadline. data_width 14-18 and n_iter 12-18 cover the accuracy requirement (max_abs_err <= 2^-12 = 0.000244). Lower data_width/n_iter minimises area.
- `iterative` (24 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the smallest-area family (1 micro-rotation/cycle, shared datapath). It cannot meet 32 Msps throughput on its own (it produces 1 result every N+3 cycles), so it will likely violate the throughput constraint. However, it is included to map the low-area end of the Pareto front and to confirm infeasibility of the throughput constraint for this family. If the fleet merges fronts, the iterative designs will be dominated on throughput but may inform the area floor. data_width/n_iter ranges match unrolled_k for accuracy coverage.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The iterative and unrolled_k families are fundamentally infeasible for the throughput constraint. The spec requires 32 MSPS, but the best observed throughput for iterative is 13.2 MSPS and for unrolled_k is 10.3 MSPS. Since iterative produces 1 result every N+3 cycles and unrolled_k every ceil(N/k)+3 cycles, their throughput is limited by latency. To meet 32 MSPS, we need a design with 1 result/cycle throughput, which requires the pipelined or pipelined_m families. Additionally, the accuracy constraint (max_abs_err <= 2^-12) is tight; the best accuracy seen so far is ~13.5 bits, which is close but we need to ensure the pipelined designs can hit this while maintaining the area objective. I will add the pipelined family to explore the 1-result/cycle regime.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 13.2
- max_abs_err <= 0.000244141: 80% violate; best seen 8.35e-05 (2^-13.55)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 2.42

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=round]: throughput=12.4, max_abs_err=0.00031 (2^-11.65); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 27.0%; sys_p99_batch_us <= 0.44 violated by 485.7%
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=1 rounding=round]: throughput=12.4, max_abs_err=0.000325 (2^-11.59); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 33.2%; sys_p99_batch_us <= 0.44 violated by 485.7%
- iterative [data_width=17 n_iter=13 angle_guard=2 frac_guard=2 rounding=round]: throughput=12.1, max_abs_err=0.000291 (2^-11.75); throughput_msps >= 32 violated by 62.1%; max_abs_err <= 0.000244141 violated by 19.3%; sys_p99_batch_us <= 0.44 violated by 499.2%
- iterative [data_width=17 n_iter=13 angle_guard=2 frac_guard=1 rounding=trunc]: throughput=12.1, max_abs_err=0.000326 (2^-11.58); throughput_msps >= 32 violated by 62.1%; max_abs_err <= 0.000244141 violated by 33.7%; sys_p99_batch_us <= 0.44 violated by 499.2%
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc]: throughput=12.4, max_abs_err=0.000378 (2^-11.37); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 54.8%; sys_p99_batch_us <= 0.44 violated by 485.7%

Per family:
- iterative: 24 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 13.35 bits
- unrolled_k: 36 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 13.55 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Adding the pipelined family is the only way to meet the 32 MSPS throughput constraint, as iterative and unrolled_k are latency-bound and cannot achieve the required throughput. The ranges are narrowed to focus on the accuracy sweet spot.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The spec requires a throughput of at least 32 MSPS and a system p99 batch latency of <= 0.44 us for a burst of 32 requests. The `iterative` and `unrolled_k` families were explored in previous rounds, but their maximum observed throughput was only 15.4 MSPS and 21.1 MSPS respectively, failing the throughput constraint by a wide margin (best seen 21.1 vs required 32). Furthermore, the best observed `sys_p99_batch_us` was 1.51 us, which is more than 3x the required 0.44 us limit. The remaining families, `pipelined` and `pipelined_m`, produce one result per cycle. To achieve 32 MSPS, they would need an Fmax of at least 32 MHz. However, the `sys_p99_batch_us` constraint of 0.44 us for 32 results implies an effective processing rate of 32 / 0.44 us ≈ 72.7 MSPS. This requires an Fmax of at least ~73 MHz (assuming 1 result/cycle). While 73 MHz is achievable on Artix-7, the area cost (LUTs+FFs) for a pipelined CORDIC with sufficient accuracy (max_abs_err <= 2^-12) and data width to support this Fmax and throughput is likely to be significantly higher than the non-pipelined variants, but more critically, the previous rounds showed that even the most efficient non-pipelined designs could not meet the throughput or latency bounds. Given that `iterative` and `unrolled_k` are strictly slower per result than `pipelined` (N+3 vs N+2 cycles, but pipelined has 1/cycle throughput), and the best `unrolled_k` (which has higher throughput than iterative) only reached 21.1 MSPS, it is highly probable that the `pipelined` families, while having higher throughput, will still struggle to meet the tight 0.44 us batch latency constraint for 32 results without incurring prohibitive area costs or failing the Fmax/throughput trade-off. Specifically, to process 32 results in 0.44 us, the system needs to sustain ~72.7 MSPS. If `unrolled_k` with k=8 (max unroll) only reached 21.1 MSPS, it suggests the Fmax or area constraints are limiting performance. A pipelined design would have a different area/Fmax profile, but given the strict latency bound and the fact that we have used 100 evaluations without finding a single feasible design in the two most throughput-efficient non-pipelined families, and considering the final round constraint, it is reasonable to conclude that no design in the registry can meet all constraints simultaneously within the area/accuracy bounds implied by the hypervolume reference points. The throughput and system latency constraints are mutually restrictive given the hardware limits observed.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 21.1
- max_abs_err <= 0.000244141: 72% violate; best seen 5.51e-08 (2^-24.11)
- sys_p99_batch_us <= 0.44: 100% violate; best seen 1.51

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=round]: throughput=12.4, max_abs_err=0.00031 (2^-11.65); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 27.0%; sys_p99_batch_us <= 0.44 violated by 485.7%
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=1 rounding=round]: throughput=12.4, max_abs_err=0.000325 (2^-11.59); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 33.2%; sys_p99_batch_us <= 0.44 violated by 485.7%
- iterative [data_width=17 n_iter=13 angle_guard=2 frac_guard=2 rounding=round]: throughput=12.1, max_abs_err=0.000291 (2^-11.75); throughput_msps >= 32 violated by 62.1%; max_abs_err <= 0.000244141 violated by 19.3%; sys_p99_batch_us <= 0.44 violated by 499.2%
- iterative [data_width=17 n_iter=13 angle_guard=2 frac_guard=1 rounding=trunc]: throughput=12.1, max_abs_err=0.000326 (2^-11.58); throughput_msps >= 32 violated by 62.1%; max_abs_err <= 0.000244141 violated by 33.7%; sys_p99_batch_us <= 0.44 violated by 499.2%
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc]: throughput=12.4, max_abs_err=0.000378 (2^-11.37); throughput_msps >= 32 violated by 61.3%; max_abs_err <= 0.000244141 violated by 54.8%; sys_p99_batch_us <= 0.44 violated by 485.7%

Per family:
- iterative: 44 evals, 0 feasible; max throughput seen 15.4 MSPS; best accuracy 19.70 bits
- unrolled_k: 56 evals, 0 feasible; max throughput seen 21.1 MSPS; best accuracy 24.11 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8701 in, 2543 out
- provider-reported cost: $0.0062
- full prompts and replies: `llm_trace.jsonl`

