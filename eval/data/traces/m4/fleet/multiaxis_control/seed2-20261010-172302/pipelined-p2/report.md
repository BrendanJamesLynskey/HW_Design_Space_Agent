# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
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
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=15,n_iter=14,angle_guard=4,frac_guard=3,rounding=round,m=3` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 873 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 339 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 119 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 119 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 58.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.46 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000207 (2^-12.24) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 1.7 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 6.37e-05 (2^-13.94) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 0.521 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 12.2 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=14,angle_guard=4,frac_guard=3,rounding=round,m=3` | 873 | 339 | 119.3 | 7 | 1.46 | 0.000207 (2^-12.24) | 12.24 |
| 1 | `pipelined_m:data_width=20,n_iter=15,angle_guard=0,frac_guard=0,rounding=round,m=4` | 979 | 311 | 93.6 | 6 | 1.55 | 8.24e-05 (2^-13.57) | 13.57 |
| 2 | `pipelined_m:data_width=22,n_iter=15,angle_guard=0,frac_guard=2,rounding=trunc,m=4` | 1126 | 351 | 89.6 | 6 | 1.78 | 6.44e-05 (2^-13.92) | 13.92 |
| 3 | `pipelined_m:data_width=23,n_iter=15,angle_guard=0,frac_guard=2,rounding=round,m=4` | 1219 | 367 | 89.6 | 6 | 1.91 | 6.18e-05 (2^-13.98) | 13.98 |
| 4 | `pipelined_m:data_width=24,n_iter=15,angle_guard=0,frac_guard=2,rounding=round,m=4` | 1266 | 381 | 89.6 | 6 | 1.98 | 6.16e-05 (2^-13.99) | 13.99 |
| 5 | `pipelined_m:data_width=23,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc,m=3` | 1222 | 517 | 114.5 | 8 | 2.09 | 3.23e-05 (2^-14.92) | 14.92 |
| 6 | `pipelined_m:data_width=23,n_iter=20,angle_guard=-2,frac_guard=1,rounding=round,m=4` | 1555 | 430 | 89.6 | 7 | 2.39 | 1.42e-05 (2^-16.10) | 16.10 |
| 7 | `pipelined_m:data_width=23,n_iter=20,angle_guard=0,frac_guard=0,rounding=round,m=3` | 1507 | 583 | 114.5 | 9 | 2.52 | 5.15e-06 (2^-17.57) | 17.57 |
| 8 | `pipelined_m:data_width=23,n_iter=20,angle_guard=0,frac_guard=1,rounding=trunc,m=3` | 1547 | 595 | 114.5 | 9 | 2.58 | 5.06e-06 (2^-17.59) | 17.59 |
| 9 | `pipelined_m:data_width=23,n_iter=20,angle_guard=0,frac_guard=2,rounding=round,m=3` | 1635 | 609 | 114.5 | 9 | 2.7 | 4.21e-06 (2^-17.86) | 17.86 |
| 10 | `pipelined_m:data_width=25,n_iter=20,angle_guard=0,frac_guard=0,rounding=round,m=3` | 1627 | 630 | 114.5 | 9 | 2.72 | 2.81e-06 (2^-18.44) | 18.44 |
| 11 | `pipelined_m:data_width=25,n_iter=26,angle_guard=0,frac_guard=0,rounding=round,m=3` | 2139 | 795 | 114.5 | 11 | 3.53 | 1.37e-06 (2^-19.48) | 19.48 |
| 12 | `pipelined_m:data_width=24,n_iter=26,angle_guard=4,frac_guard=1,rounding=round,m=3` | 2269 | 820 | 110.0 | 11 | 3.72 | 9.69e-07 (2^-19.98) | 19.98 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show pipelined_m is clearly the winner: 8/10 front designs, best luts_plus_ffs of 1236, and 25 feasible out of 51 evals. pipelined has 2 front designs and best luts_plus_ffs of 1843. The other families (iterative, unrolled_k) have 0 feasible designs, so they are excluded (and not in my assigned families anyway). The key insight is that pipelined_m with m>1 reduces FF count by sharing pipeline registers, which directly minimizes luts_plus_ffs while maintaining 1 result/cycle throughput. The accuracy constraint (max_abs_err <= 2^-12) requires sufficient data_width and n_iter; from the 40 feasible pipelined designs, the accuracy is achievable with data_width around 14-16 and n_iter around 12-16. I allocate 55% to pipelined_m (the dominant family) and 45% to pipelined (to cover the m=1 end of the front and ensure the trade-off curve is well-mapped). The m range is 2-4 for pipelined_m: m=2 gives the best FF reduction with minimal timing penalty, m=3-4 give further savings but may hurt Fmax. I keep angle_guard and frac_guard in their full ranges to let Optuna explore the accuracy/area trade-off within the accuracy constraint.*)
- `pipelined_m` (55 evals): data_width=14..16, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* pipelined_m dominates the merged front (8/10 designs) and has the best feasible luts_plus_ffs (1236). It meets throughput_msps >= 32 (1 result/cycle) and the 0.44us batch constraint (32 results in 32 cycles at Fmax). The m parameter (2-8) is the key trade-off: larger m reduces FFs (fewer pipeline registers) but may reduce Fmax. I focus on m=2..4 since m>4 gives diminishing FF savings while hurting timing. data_width 14-16 and n_iter 12-16 target the accuracy constraint (max_abs_err <= 2^-12 = 0.000244) with minimal area. angle_guard and frac_guard are kept in their full ranges to let Optuna find the accuracy/area trade-off.
- `pipelined` (45 evals): data_width=14..16, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* pipelined (m=1, full pipeline) has 2 designs on the merged front and best feasible luts_plus_ffs of 1843. It is the baseline for pipelined_m. I keep it in the search to map the full trade-off curve between pipelined and pipelined_m, and to ensure the front is well-covered at the m=1 end. Same accuracy-focused ranges: data_width 14-16, n_iter 12-16 to meet max_abs_err <= 2^-12 with minimal area.

**Result (code):** 100 evaluations this round, 100 total; 24 feasible; hypervolume 2407 (n/a).

**LLM decision:** `refine` — The current Pareto front is dominated by `pipelined_m` with `m=3`, which achieves the best area (1212 LUTs+FFs) while meeting all constraints. The `pipelined` family is significantly worse in area (best 1829) and offers no advantage in accuracy or throughput for this specific bursty workload (32 req/us). The accuracy constraint (max_abs_err <= 2^-12) is the binding constraint, with 76% of evaluations violating it. The feasible region is tightly clustered around `data_width=15`, `n_iter=14-16`, `angle_guard=4`, and `frac_guard=1-4`. To maximize hypervolume and find the true minimum area design, we should narrow the search space to focus on the `pipelined_m` family with `m=3` (and potentially `m=2` if it offers better area/latency trade-offs, though `m=3` is currently best) and restrict `data_width` to 14-16 and `n_iter` to 13-17. This will allow the optimizer to densely sample the feasible region near the accuracy boundary, potentially finding designs with lower area or higher accuracy bits within the same area budget.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 2407 (gain this round: n/a (first round)).
Feasible designs: 24 of 100 evaluations (13 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 76% violate; best seen 0.00013 (2^-12.91)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.161

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=4 frac_guard=3 rounding=round m=3] luts_plus_ffs=1212, accuracy_bits=12.2, luts=873, ffs=339, throughput_msps=119, max_abs_err=0.000207 (2^-12.24), power_index=1.46
- pipelined_m [data_width=15 n_iter=16 angle_guard=4 frac_guard=2 rounding=round m=3] luts_plus_ffs=1361, accuracy_bits=12.3, luts=969, ffs=391, throughput_msps=119, max_abs_err=0.000192 (2^-12.35), power_index=1.64
- pipelined_m [data_width=16 n_iter=16 angle_guard=4 frac_guard=1 rounding=round m=3] luts_plus_ffs=1389, accuracy_bits=12.5, luts=987, ffs=402, throughput_msps=119, max_abs_err=0.000177 (2^-12.47), power_index=1.67
- pipelined_m [data_width=15 n_iter=16 angle_guard=4 frac_guard=3 rounding=round m=3] luts_plus_ffs=1403, accuracy_bits=12.7, luts=1001, ffs=402, throughput_msps=119, max_abs_err=0.00015 (2^-12.70), power_index=1.69
- pipelined_m [data_width=15 n_iter=16 angle_guard=4 frac_guard=4 rounding=round m=3] luts_plus_ffs=1444, accuracy_bits=12.9, luts=1033, ffs=412, throughput_msps=119, max_abs_err=0.00013 (2^-12.91), power_index=1.74
Front coverage: luts_plus_ffs 1212..1444 (HV reference 4000); accuracy_bits 12.2..12.9 (HV reference 12); data_width on the front 15..16 (registry 8..28).

Per family:
- pipelined: 45 evals, 8 feasible; max throughput seen 273 MSPS; best accuracy 12.91 bits; best feasible luts_plus_ffs=1829; feasible ranges: data_width 14..16, n_iter 15..16, angle_guard 2..4, frac_guard 2..4
- pipelined_m: 55 evals, 16 feasible; max throughput seen 171 MSPS; best accuracy 12.91 bits; best feasible luts_plus_ffs=1212; feasible ranges: data_width 15..16, n_iter 14..16, angle_guard 2..4, frac_guard 1..4, m 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 1 showed that pipelined_m with m=3 is the clear winner in area efficiency. The accuracy constraint is tight, so we need to explore the boundary between feasible and infeasible designs more densely. By restricting data_width, n_iter, and m to the observed feasible ranges, we can use the remaining budget to fine-tune the trade-off between area and accuracy.*)
- `pipelined_m` (20 evals): data_width=14..16, n_iter=13..17, angle_guard=2..4, frac_guard=0..4, rounding=trunc|round, m=2..3. *Why:* Focus on the best-performing family and parameter region identified in Round 1. Narrowing ranges increases sampling density in the feasible area, helping to refine the Pareto front and identify the minimum area design that meets the accuracy constraint.

**Result (code):** 20 evaluations this round, 120 total; 25 feasible; hypervolume 2428 (+0.8%).

**LLM decision:** `stop` — The feasible Pareto front is well-established and the constraints are met. The minimum area design (pipelined_m, 1212 LUTs+FFs) achieves 12.2 accuracy bits, which exceeds the 12-bit requirement (max_abs_err 0.000207 < 0.000244). Throughput (119 MSPS) and system latency (0.161 us p99 batch) comfortably satisfy the 32 MSPS and 0.44 us constraints. Since this is the final round, the exploration should conclude to allow L2 simulation of the shortlist.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 2428 (gain this round: +0.8%).
Feasible designs: 25 of 120 evaluations (14 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 79% violate; best seen 0.00013 (2^-12.91)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.161

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=4 frac_guard=3 rounding=round m=3] luts_plus_ffs=1212, accuracy_bits=12.2, luts=873, ffs=339, throughput_msps=119, max_abs_err=0.000207 (2^-12.24), power_index=1.46
- pipelined_m [data_width=15 n_iter=15 angle_guard=3 frac_guard=4 rounding=round m=3] luts_plus_ffs=1294, accuracy_bits=12.5, luts=952, ffs=342, throughput_msps=119, max_abs_err=0.000175 (2^-12.48), power_index=1.56
- pipelined_m [data_width=15 n_iter=16 angle_guard=4 frac_guard=3 rounding=round m=3] luts_plus_ffs=1403, accuracy_bits=12.7, luts=1001, ffs=402, throughput_msps=119, max_abs_err=0.00015 (2^-12.70), power_index=1.69
- pipelined_m [data_width=15 n_iter=16 angle_guard=4 frac_guard=4 rounding=round m=3] luts_plus_ffs=1444, accuracy_bits=12.9, luts=1033, ffs=412, throughput_msps=119, max_abs_err=0.00013 (2^-12.91), power_index=1.74
Front coverage: luts_plus_ffs 1212..1444 (HV reference 4000); accuracy_bits 12.2..12.9 (HV reference 12); data_width on the front 15..15 (registry 8..28).

Per family:
- pipelined: 45 evals, 8 feasible; max throughput seen 273 MSPS; best accuracy 12.91 bits; best feasible luts_plus_ffs=1829; feasible ranges: data_width 14..16, n_iter 15..16, angle_guard 2..4, frac_guard 2..4
- pipelined_m: 75 evals, 17 feasible; max throughput seen 171 MSPS; best accuracy 12.91 bits; best feasible luts_plus_ffs=1212; feasible ranges: data_width 15..16, n_iter 14..16, angle_guard 2..4, frac_guard 1..4, m 2..3
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (80 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 68 feasible; hypervolume 1.57e+04 (+546.5%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and the constraints are met. The minimum area design (pipelined_m, 1212 LUTs+FFs) achieves 12.2 accuracy bits, which exceeds the 12-bit requirement (max_abs_err 0.000207 < 0.000244). Throughput (119 MSPS) and system latency (0.161 us p99 batch) comfortably satisfy the 32 MSPS and 0.44 us constraints. Since this is the final round, the exploration should conclude to allow L2 simulation of the shortlist.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.57e+04 (gain this round: +546.5%).
Feasible designs: 68 of 200 evaluations (55 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 50% violate; best seen 8.36e-08 (2^-23.51)
- sys_p99_batch_us <= 0.44: 17% violate; best seen 0.161

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=4 frac_guard=3 rounding=round m=3] luts_plus_ffs=1212, accuracy_bits=12.2, luts=873, ffs=339, throughput_msps=119, max_abs_err=0.000207 (2^-12.24), power_index=1.46
- pipelined_m [data_width=20 n_iter=15 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1290, accuracy_bits=13.6, luts=979, ffs=311, throughput_msps=93.6, max_abs_err=8.24e-05 (2^-13.57), power_index=1.55
- pipelined_m [data_width=23 n_iter=15 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1586, accuracy_bits=14, luts=1219, ffs=367, throughput_msps=89.6, max_abs_err=6.18e-05 (2^-13.98), power_index=1.91
- pipelined_m [data_width=24 n_iter=15 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1647, accuracy_bits=14, luts=1266, ffs=381, throughput_msps=89.6, max_abs_err=6.16e-05 (2^-13.99), power_index=1.98
- pipelined_m [data_width=23 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1739, accuracy_bits=14.9, luts=1222, ffs=517, throughput_msps=114, max_abs_err=3.23e-05 (2^-14.92), power_index=2.09
- pipelined_m [data_width=23 n_iter=20 angle_guard=0 frac_guard=0 rounding=round m=3] luts_plus_ffs=2090, accuracy_bits=17.6, luts=1507, ffs=583, throughput_msps=114, max_abs_err=5.15e-06 (2^-17.57), power_index=2.52
- pipelined_m [data_width=23 n_iter=20 angle_guard=0 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=2142, accuracy_bits=17.6, luts=1547, ffs=595, throughput_msps=114, max_abs_err=5.06e-06 (2^-17.59), power_index=2.58
- pipelined_m [data_width=23 n_iter=20 angle_guard=0 frac_guard=2 rounding=round m=3] luts_plus_ffs=2245, accuracy_bits=17.9, luts=1635, ffs=609, throughput_msps=114, max_abs_err=4.21e-06 (2^-17.86), power_index=2.7
- pipelined_m [data_width=25 n_iter=26 angle_guard=0 frac_guard=0 rounding=round m=3] luts_plus_ffs=2934, accuracy_bits=19.5, luts=2139, ffs=795, throughput_msps=114, max_abs_err=1.37e-06 (2^-19.48), power_index=3.53
- pipelined_m [data_width=24 n_iter=26 angle_guard=4 frac_guard=1 rounding=round m=3] luts_plus_ffs=3089, accuracy_bits=20, luts=2269, ffs=820, throughput_msps=110, max_abs_err=9.69e-07 (2^-19.98), power_index=3.72
Front coverage: luts_plus_ffs 1212..3089 (HV reference 4000); accuracy_bits 12.2..20 (HV reference 12); data_width on the front 15..25 (registry 8..28).

Per family:
- pipelined: 45 evals, 8 feasible; max throughput seen 273 MSPS; best accuracy 12.91 bits; best feasible luts_plus_ffs=1829; feasible ranges: data_width 14..16, n_iter 15..16, angle_guard 2..4, frac_guard 2..4
- pipelined_m: 155 evals, 60 feasible; max throughput seen 171 MSPS; best accuracy 23.51 bits; best feasible luts_plus_ffs=1212; feasible ranges: data_width 15..27, n_iter 14..29, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8307 in, 1893 out
- provider-reported cost: $0.0042
- full prompts and replies: `llm_trace.jsonl`

