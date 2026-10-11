# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 158 of 158 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec low_area_control: Field-oriented motor-control loop needing sin/cos of the rotor angle at >= 1 MSPS with max error <= 2^-10. Area is everything: minimise LUTs + FFs.
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min luts_plus_ffs (HV ref 1500)
  objective: max accuracy_bits (HV ref 10)
  select: min luts_plus_ffs
  budget: 158 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=16,n_iter=13,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 178 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 96 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 12.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 80.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.165 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000492 (2^-10.99) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 8.06 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000131 (2^-12.90) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 2.14 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 11 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (6 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=16,n_iter=13,angle_guard=0,frac_guard=0,rounding=round` | 178 | 96 | 12.4 | 16 | 0.165 | 0.000492 (2^-10.99) | 10.99 |
| 1 | `unrolled_k:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,k=2` | 262 | 95 | 10.5 | 10 | 0.134 | 0.0004 (2^-11.29) | 11.29 |
| 2 | `iterative:data_width=17,n_iter=20,angle_guard=0,frac_guard=4,rounding=trunc` | 253 | 110 | 6.9 | 23 | 0.314 | 0.000216 (2^-12.17) | 12.17 |
| 3 | `iterative:data_width=21,n_iter=18,angle_guard=1,frac_guard=0,rounding=trunc` | 262 | 123 | 7.6 | 21 | 0.304 | 2.55e-05 (2^-15.26) | 15.26 |
| 4 | `iterative:data_width=22,n_iter=20,angle_guard=0,frac_guard=4,rounding=trunc` | 333 | 135 | 6.8 | 23 | 0.405 | 7.68e-06 (2^-16.99) | 16.99 |
| 5 | `iterative:data_width=27,n_iter=28,angle_guard=4,frac_guard=0,rounding=round` | 399 | 156 | 4.9 | 31 | 0.648 | 2.03e-07 (2^-22.23) | 22.23 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show unrolled_k is my workhorse: 40 feasible points, best area 415, and 15 of 19 merged-front designs. iterative has been infeasible so far (0/33), likely a throughput wall. The spec's binding constraints are throughput >=1 MSPS and max_abs_err <= 2^-10. For unrolled_k, the key trade-off is k (throughput vs area) and n_iter/data_width (accuracy vs area). I focus 70% of budget on unrolled_k with tight ranges around the known-feasible region (W 12-16, N 10-14, k 2-4, minimal guards) to densely map the Pareto front in the area/accuracy space. The remaining 30% probes iterative at the same accuracy settings to check if any low-area point sneaks through the throughput constraint, which would extend the front to lower luts_plus_ffs. Both families compute identical bits, so accuracy tuning is shared; the difference is purely in the datapath structure and resulting Fmax/area.*)
- `unrolled_k` (67 evals): data_width=12..16, n_iter=10..14, angle_guard=-2..0, frac_guard=0..1, rounding=trunc|round, k=2..4. *Why:* unrolled_k is the only family I control that has produced feasible points (40 feasible, best luts_plus_ffs 415, 15/19 on the merged front). The spec needs >=1 MSPS throughput and <=2^-10 error. unrolled_k with k=2..4 gives ceil(N/k)+3 cycles/result; with N~10-14 and k=2-4 that is ~5-10 cycles/result, so Fmax must be >=100-200 MHz to hit 1 MSPS. Narrowing data_width to 12-16 and n_iter to 10-14 focuses on the accuracy/area sweet spot: W=12 gives output LSB 2^-10, so n_iter must be high enough that CORDIC residual error stays below 2^-10. angle_guard -2..0 and frac_guard 0..1 keep the datapath narrow to minimize LUTs+FFs while still meeting the error bound. k=2..4 balances throughput (need enough rotations/cycle) against area (more parallel shift/add chains). This is where the trade-off curve lives for my assigned families.
- `iterative` (28 evals): data_width=12..16, n_iter=10..14, angle_guard=-2..0, frac_guard=0..1, rounding=trunc|round. *Why:* iterative produced 0 feasible points in 33 evals, likely because its N+3 cycle latency (N~10-14 means 13-17 cycles/result) requires Fmax >= 130-170 MHz for 1 MSPS, and the shared datapath may not reach that Fmax at the widths needed for 2^-10 accuracy. However, iterative has the smallest area per rotation (single datapath, no k-way parallelism), so if it can meet throughput at all, it could dominate on luts_plus_ffs. I keep a small share to probe whether any iterative config clears the throughput constraint at the minimal area, which would expand the Pareto front toward the low-area end. If it remains infeasible, the budget is cheap insurance.

**Result (code):** 95 evaluations this round, 95 total; 27 feasible; hypervolume 1597 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is established and the primary objective (min luts_plus_ffs) is satisfied by the `iterative` family design with 273 LUTs+FFs, which is well below the HV reference of 1500. The constraint `max_abs_err <= 0.000976562` is met by all 3 designs on the front (best 0.000389). The constraint `throughput_msps >= 1` is met by all designs (best 15.6). The front covers the trade-off space adequately for the selection rule (min luts_plus_ffs), which picks the 273 LUTs+FFs design. Since this is the final round and the front is stable with a clear winner for the selection rule, stopping is appropriate.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 63 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 95 of 158.
Hypervolume of the feasible front: 1597 (gain this round: n/a (first round)).
Feasible designs: 27 of 95 evaluations (21 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 72% violate; best seen 0.000389 (2^-11.33)

Pareto front (feasible, 3 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11, luts=178, ffs=96, throughput_msps=12.4, max_abs_err=0.000492 (2^-10.99), power_index=0.165
- unrolled_k [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round k=2] luts_plus_ffs=357, accuracy_bits=11.3, luts=262, ffs=95, throughput_msps=10.5, max_abs_err=0.0004 (2^-11.29), power_index=0.134
- unrolled_k [data_width=16 n_iter=14 angle_guard=0 frac_guard=1 rounding=round k=2] luts_plus_ffs=406, accuracy_bits=11.3, luts=309, ffs=97, throughput_msps=10.5, max_abs_err=0.000389 (2^-11.33), power_index=0.153
Front coverage: luts_plus_ffs 273..406 (HV reference 1500); accuracy_bits 11..11.3 (HV reference 10); data_width on the front 16..16 (registry 8..28).

Per family:
- iterative: 28 evals, 2 feasible; max throughput seen 15.6 MSPS; best accuracy 10.99 bits; best feasible luts_plus_ffs=273; feasible ranges: data_width 16..16, n_iter 13..14, angle_guard -1..0, frac_guard 0..1
- unrolled_k: 67 evals, 25 feasible; max throughput seen 14 MSPS; best accuracy 11.33 bits; best feasible luts_plus_ffs=357; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard -1..0, frac_guard 0..1, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 63 evaluations*)
- `iterative` (21 evals): data_width=15..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (1 front designs; box front_anchored)
- `unrolled_k` (42 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (2 front designs; box front_anchored)

**Result (code):** 63 evaluations this round, 158 total; 87 feasible; hypervolume 1.274e+04 (+697.9%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is established and the primary objective (min luts_plus_ffs) is satisfied by the `iterative` family design with 273 LUTs+FFs, which is well below the HV reference of 1500. The constraint `max_abs_err <= 0.000976562` is met by all 3 designs on the front (best 0.000389). The constraint `throughput_msps >= 1` is met by all designs (best 15.6). The front covers the trade-off space adequately for the selection rule (min luts_plus_ffs), which picks the 273 LUTs+FFs design. Since this is the final round and the front is stable with a clear winner for the selection rule, stopping is appropriate.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 158 of 158.
Hypervolume of the feasible front: 1.274e+04 (gain this round: +697.9%).
Feasible designs: 87 of 158 evaluations (73 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 45% violate; best seen 2.03e-07 (2^-22.23)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=273, accuracy_bits=11, luts=178, ffs=96, throughput_msps=12.4, max_abs_err=0.000492 (2^-10.99), power_index=0.165
- unrolled_k [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round k=2] luts_plus_ffs=357, accuracy_bits=11.3, luts=262, ffs=95, throughput_msps=10.5, max_abs_err=0.0004 (2^-11.29), power_index=0.134
- iterative [data_width=17 n_iter=20 angle_guard=0 frac_guard=4 rounding=trunc] luts_plus_ffs=363, accuracy_bits=12.2, luts=253, ffs=110, throughput_msps=6.91, max_abs_err=0.000216 (2^-12.17), power_index=0.314
- iterative [data_width=21 n_iter=18 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=385, accuracy_bits=15.3, luts=262, ffs=123, throughput_msps=7.57, max_abs_err=2.55e-05 (2^-15.26), power_index=0.304
- iterative [data_width=22 n_iter=20 angle_guard=0 frac_guard=4 rounding=trunc] luts_plus_ffs=468, accuracy_bits=17, luts=333, ffs=135, throughput_msps=6.78, max_abs_err=7.68e-06 (2^-16.99), power_index=0.405
- iterative [data_width=27 n_iter=28 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=556, accuracy_bits=22.2, luts=399, ffs=156, throughput_msps=4.86, max_abs_err=2.03e-07 (2^-22.23), power_index=0.648
Front coverage: luts_plus_ffs 273..556 (HV reference 1500); accuracy_bits 11..22.2 (HV reference 10); data_width on the front 16..27 (registry 8..28).

Per family:
- iterative: 49 evals, 20 feasible; max throughput seen 15.6 MSPS; best accuracy 22.23 bits; best feasible luts_plus_ffs=273; feasible ranges: data_width 16..27, n_iter 11..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 109 evals, 67 feasible; max throughput seen 14 MSPS; best accuracy 19.51 bits; best feasible luts_plus_ffs=357; feasible ranges: data_width 15..24, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, k 2..8
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 1)
- tokens: 4069 in, 1443 out
- provider-reported cost: $0.0035
- full prompts and replies: `llm_trace.jsonl`

