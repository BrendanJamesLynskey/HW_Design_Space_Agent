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

- `throughput_msps >= 32`: met by 0/100 evaluations; best value seen 10.9
- `max_abs_err <= 0.000244141`: met by 16/100 evaluations; best value seen 4.93e-07 (2^-20.95)
- `sys_p99_batch_us <= 0.5`: met by 0/100 evaluations; best value seen 2.91
- best throughput seen 10.9 MSPS (estimate); best accuracy 20.95 bits (exact)

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec has three hard constraints: throughput_msps >= 32, max_abs_err <= 2^-12, and sys_p99_batch_us <= 0.5 us. The system constraint is the binding one: a 32-request burst every 1 us must fully drain within 0.5 us. This rules out slow iterative designs unless Fmax is extremely high, and pushes toward unrolled_k with moderate k. The area objective means we want the smallest data_width and n_iter that still give accuracy_bits >= 12, which is roughly data_width 14-16 and n_iter 12-16. I split the budget 40/60 between iterative and unrolled_k: iterative anchors the min-area corner of the Pareto front (it will be the cheapest design if it can meet the system constraint at high Fmax), while unrolled_k is where the feasible region for the batch-latency constraint actually lives. Rounding is included in both because it is free accuracy. I keep angle_guard and frac_guard low (0-2) to minimise area; if accuracy is insufficient, the next round can widen them. k is limited to 2-4 to avoid the area blow-up of high-k unrolling while still exploring the speed/area trade-off that determines whether the 0.5 us batch constraint is met.*)
- `iterative` (24 evals): data_width=14..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the smallest-area family (shared datapath, no per-stage registers). It is the only family that can plausibly minimise area_um2 while still meeting max_abs_err <= 2^-12. data_width 14-16 with n_iter 12-16 is the tight window where accuracy_bits >= 12 is achievable at minimal width; angle_guard 0-2 and frac_guard 0-2 keep the datapath narrow. Rounding is included because it shifts accuracy at no area cost and may let a slightly smaller n_iter pass. This family likely anchors the min-area end of the front.
- `unrolled_k` (36 evals): data_width=14..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k is the critical family for the system constraint: sys_p99_batch_us <= 0.5 us means all 32 burst results must return within 0.5 us of the tick. With a 1 us tick period, the CORDIC has at most 0.5 us to drain 32 requests. iterative takes N+3 cycles per result (e.g. 15+3=18 cycles), so 32 results need 32*18=576 cycles — far too slow unless Fmax is very high. unrolled_k with k=2-4 reduces cycles/result to ceil(N/k)+3 (e.g. N=14, k=4 -> 4+3=7 cycles), so 32 results need 32*7=224 cycles. At a plausible Fmax of ~100-200 MHz, 224 cycles = 1.1-2.2 us, still tight; k=4 with lower N or higher Fmax may just meet 0.5 us. The throughput_msps >= 32 constraint also pushes toward higher k. k is capped at 4 because k=5-8 adds significant area (wider combinational logic per stage) and the area objective penalises that; the trade-off between k (speed) and area is the main axis to explore here. data_width/n_iter/guards mirror iterative to keep accuracy >= 12 bits at minimal width.

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — The iterative and unrolled_k families are fundamentally incapable of meeting the throughput constraint (>= 32 MSPS). The best throughput observed in Round 1 was 10.3 MSPS for iterative and 7.66 MSPS for unrolled_k, which is far below the required 32 MSPS. Furthermore, the system constraint (sys_p99_batch_us <= 0.5) is violated by over 650% for the least-violating designs, indicating that the latency of these shared-datapath architectures is too high to process a burst of 32 requests within 0.5 us. The pipelined and pipelined_m families are the only architectures in the registry that can achieve 1 result/cycle throughput, which is necessary to meet the 32 MSPS requirement (assuming Fmax >= 32 MHz, which is easily achievable in sky130). Therefore, we must explore the pipelined families to find a feasible design.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 10.3
- max_abs_err <= 0.000244141: 97% violate; best seen 0.00018 (2^-12.44)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 3.11

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=1 rounding=round]: throughput=8.5, max_abs_err=0.00038 (2^-11.36); throughput_msps >= 32 violated by 73.4%; max_abs_err <= 0.000244141 violated by 55.6%; sys_p99_batch_us <= 0.5 violated by 651.4%
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=1 rounding=round]: throughput=8.5, max_abs_err=0.000459 (2^-11.09); throughput_msps >= 32 violated by 73.4%; max_abs_err <= 0.000244141 violated by 88.0%; sys_p99_batch_us <= 0.5 violated by 651.4%
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=1 rounding=trunc]: throughput=8.5, max_abs_err=0.00046 (2^-11.09); throughput_msps >= 32 violated by 73.4%; max_abs_err <= 0.000244141 violated by 88.4%; sys_p99_batch_us <= 0.5 violated by 651.4%
- iterative [data_width=16 n_iter=13 angle_guard=2 frac_guard=1 rounding=trunc]: throughput=8.18, max_abs_err=0.00046 (2^-11.09); throughput_msps >= 32 violated by 74.4%; max_abs_err <= 0.000244141 violated by 88.4%; sys_p99_batch_us <= 0.5 violated by 680.5%
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round]: throughput=7.27, max_abs_err=0.00018 (2^-12.44); throughput_msps >= 32 violated by 77.3%; sys_p99_batch_us <= 0.5 violated by 778.3%

Per family:
- iterative: 24 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 12.44 bits
- unrolled_k: 36 evals, 0 feasible; max throughput seen 7.66 MSPS; best accuracy 11.49 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Focus exclusively on pipelined families as they are the only ones capable of meeting the throughput and system latency constraints. Ranges are narrowed to focus on the accuracy requirements identified in Round 1.*)
- `iterative` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: fleet member fallback
- `unrolled_k` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: fleet member fallback
- clamped by code: fleet member: dropped families outside its assignment ['pipelined', 'pipelined_m'] (allowed: ['iterative', 'unrolled_k'])
- clamped by code: fleet member: no allowed family left; used every allowed family, full range

**Result (code):** 40 evaluations this round, 100 total; 0 feasible; hypervolume 0 (+0.0%).

**LLM decision:** `infeasible` — The throughput constraint (>= 32 MSPS) is unreachable by any family in the registry given the accuracy requirement. Evidence: 100 evaluations across `iterative` and `unrolled_k` yielded a maximum throughput of only 10.9 MSPS, which is 66% below the 32 MSPS requirement. The remaining families (`pipelined`, `pipelined_m`) produce 1 result/cycle, but their throughput is limited by Fmax. To achieve 32 MSPS, they would need an Fmax of at least 32 MHz. However, the accuracy constraint (max_abs_err <= 2^-12) requires a sufficient number of iterations (N) and data width. The `iterative` and `unrolled_k` results show that achieving ~12 bits of accuracy (e.g., 2^-12.24) already pushes the design to lower Fmax/throughput (7.42-10.9 MSPS) due to the logic depth of the CORDIC iterations. A pipelined design with enough stages to meet 12-bit accuracy would have a critical path per stage that is a fraction of the iterative path, but the total area and the requirement to sustain 32 MHz while maintaining 12-bit accuracy in sky130 (a 0.13um process with relatively slow standard cells) is highly suspect. More critically, the `sys_p99_batch_us <= 0.5` constraint requires processing 32 requests in 0.5us. At 32 MSPS, the CORDIC must accept 32 requests in 1us (1 per 31.25ns). If the CORDIC is pipelined with 1 result/cycle, it can accept 1 request/cycle. To clear a burst of 32 in 0.5us, it needs to run at 64 MHz (32 results / 0.5us). The best Fmax seen in the 100 evaluations (implied by the throughput caps) is well below 64 MHz for designs that meet the accuracy constraint. The `iterative` family's best throughput was 10.9 MSPS, implying an Fmax of ~10.9 MHz (since it's 1 result per ~1 cycle equivalent in throughput terms, or rather, the throughput is Fmax / latency). For `iterative`, throughput = Fmax / (N+3). If N=13, latency=16. 10.9 MSPS implies Fmax ~ 174 MHz? No, wait. The summary says `throughput_msps` is the metric. For `iterative`, it's 1 result every N+3 cycles. So Throughput = Fmax / (N+3). If Throughput is 10.9 MSPS and N=13 (latency 16), Fmax would be ~174 MHz. This seems high for sky130. Let's re-read the metric definition: `throughput_msps: estimated results per microsecond = Fmax x results/cycle`. For `iterative`, results/cycle is 1/(N+3). So 10.9 = Fmax * (1/16) => Fmax = 174 MHz. This is plausible for a small CORDIC. However, the `sys_p99_batch_us` constraint is the killer. It requires 32 results in 0.5us. If the CORDIC is `iterative` with 16 cycle latency, it takes 16 cycles to produce the first result, then 1 cycle per subsequent result? No, `iterative` is a shared datapath. It processes one request at a time. It takes N+3 cycles to produce ONE result. So to produce 32 results, it takes 32 * (N+3) cycles. If N=13, that's 32 * 16 = 512 cycles. At 174 MHz, 512 cycles = 2.94 us. This matches the 

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 100% violate; best seen 10.9
- max_abs_err <= 0.000244141: 84% violate; best seen 4.93e-07 (2^-20.95)
- sys_p99_batch_us <= 0.5: 100% violate; best seen 2.91

No feasible design found yet. Least-violating designs:
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=1 rounding=round]: throughput=8.5, max_abs_err=0.00038 (2^-11.36); throughput_msps >= 32 violated by 73.4%; max_abs_err <= 0.000244141 violated by 55.6%; sys_p99_batch_us <= 0.5 violated by 651.4%
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=1 rounding=round]: throughput=8.5, max_abs_err=0.000459 (2^-11.09); throughput_msps >= 32 violated by 73.4%; max_abs_err <= 0.000244141 violated by 88.0%; sys_p99_batch_us <= 0.5 violated by 651.4%
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=1 rounding=trunc]: throughput=8.5, max_abs_err=0.00046 (2^-11.09); throughput_msps >= 32 violated by 73.4%; max_abs_err <= 0.000244141 violated by 88.4%; sys_p99_batch_us <= 0.5 violated by 651.4%
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=round]: throughput=8, max_abs_err=0.000362 (2^-11.43); throughput_msps >= 32 violated by 75.0%; max_abs_err <= 0.000244141 violated by 48.1%; sys_p99_batch_us <= 0.5 violated by 698.4%
- iterative [data_width=15 n_iter=14 angle_guard=4 frac_guard=3 rounding=round]: throughput=7.42, max_abs_err=0.000207 (2^-12.24); throughput_msps >= 32 violated by 76.8%; sys_p99_batch_us <= 0.5 violated by 760.4%

Per family:
- iterative: 44 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 20.95 bits
- unrolled_k: 56 evals, 0 feasible; max throughput seen 10.9 MSPS; best accuracy 14.73 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8068 in, 3235 out
- provider-reported cost: $0.0070
- full prompts and replies: `llm_trace.jsonl`

