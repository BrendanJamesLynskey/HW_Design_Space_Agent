# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 863 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 280 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 61.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.38 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000192 (2^-12.35) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 6.29 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.46e-05 (2^-14.16) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.79 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (11 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=4` | 863 | 280 | 97.8 | 6 | 1.38 | 0.000192 (2^-12.35) | 12.35 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,m=4` | 855 | 291 | 93.6 | 6 | 1.38 | 0.00017 (2^-12.53) | 12.53 |
| 2 | `pipelined_m:data_width=18,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=4` | 920 | 299 | 93.6 | 6 | 1.47 | 0.000152 (2^-12.68) | 12.68 |
| 3 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=4` | 941 | 285 | 93.6 | 6 | 1.48 | 0.00013 (2^-12.91) | 12.91 |
| 4 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=4` | 987 | 299 | 93.6 | 6 | 1.55 | 9.31e-05 (2^-13.39) | 13.39 |
| 5 | `pipelined_m:data_width=16,n_iter=21,angle_guard=3,frac_guard=3,rounding=round,m=3` | 1367 | 480 | 119.3 | 9 | 2.22 | 8.62e-05 (2^-13.50) | 13.50 |
| 6 | `pipelined_m:data_width=19,n_iter=21,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 1438 | 524 | 119.3 | 9 | 2.36 | 4.3e-05 (2^-14.50) | 14.50 |
| 7 | `pipelined_m:data_width=20,n_iter=21,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1502 | 474 | 89.6 | 8 | 2.38 | 2.4e-05 (2^-15.35) | 15.35 |
| 8 | `pipelined:data_width=19,n_iter=18,angle_guard=2,frac_guard=2,rounding=round` | 1281 | 1265 | 264.5 | 20 | 3.07 | 2.34e-05 (2^-15.38) | 15.38 |
| 9 | `pipelined_m:data_width=27,n_iter=23,angle_guard=3,frac_guard=1,rounding=round,m=3` | 2195 | 805 | 110.0 | 10 | 3.61 | 3.1e-07 (2^-21.62) | 21.62 |
| 10 | `pipelined_m:data_width=27,n_iter=23,angle_guard=3,frac_guard=4,rounding=round,m=3` | 2334 | 847 | 105.9 | 10 | 3.83 | 2.67e-07 (2^-21.84) | 21.84 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Spec requires max_abs_err <= 2^-12 and 32 results within 0.44 us of a 1 MHz tick. Throughput >=32 Msps is trivial for 1 result/cycle, but the batch deadline demands Fmax >= ~73 MHz plus latency. Pipelined and pipelined_m both give 1 result/cycle. Accuracy depends only on W, N, guards, rounding, so we search W 14-20 and N 12-20 to cover the accuracy constraint with minimal area. Guards -2..2 and frac_guard 0..2 explore rounding/angle precision trade-offs. Pipelined_m's m 2..8 trades latency and FFs against Fmax. Budget split 40/60 to emphasize pipelined_m's larger parameter space while still mapping the fully pipelined front.*)
- `pipelined` (24 evals): data_width=14..20, n_iter=12..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Fully pipelined gives the highest Fmax and lowest latency per iteration, which helps meet the 0.44 us batch deadline for 32 simultaneous requests. Search lower W/N for area, with guards to ensure the 2^-12 error constraint is met.
- `pipelined_m` (36 evals): data_width=14..20, n_iter=12..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* Registering every m stages reduces FF count and latency (ceil(N/m)+2), which can lower area and relax the Fmax needed for the batch deadline. The extra m parameter offers a richer area/latency trade-off; more budget is allocated to map it.

**Result (code):** 60 evaluations this round, 60 total; 34 feasible; hypervolume 7272 (n/a).

**LLM decision:** `stop` — This is the final round, and the front is feasible and well-covered, so no further exploration is possible. All three constraints are satisfiable: throughput_msps >= 32 (best seen 273, 0% violations), max_abs_err <= 0.000244141 (best 2.34e-05 = 2^-15.38), and sys_p99_batch_us <= 0.44 (best 0.165). The feasible Pareto front spans luts_plus_ffs 1144..2547 against HV ref 4000 and accuracy_bits 12.3..15.4 against HV ref 12, giving hypervolume 7272 with 26 unique feasible designs. The selection rule (min luts_plus_ffs) is served by the pipelined_m corner at luts_plus_ffs=1144, accuracy_bits=12.3, which still clears the error constraint (2^-12.35 <= 2^-12) and the system batch bound. No constraint is unreachable, so `infeasible` is not warranted; the front is good enough to stop.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 7272 (gain this round: n/a (first round)).
Feasible designs: 34 of 60 evaluations (26 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 27% violate; best seen 2.34e-05 (2^-15.38)
- sys_p99_batch_us <= 0.44: 27% violate; best seen 0.165

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1144, accuracy_bits=12.3, luts=863, ffs=280, throughput_msps=97.8, max_abs_err=0.000192 (2^-12.35), power_index=1.38
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1145, accuracy_bits=12.5, luts=855, ffs=291, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.53), power_index=1.38
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1219, accuracy_bits=12.7, luts=920, ffs=299, throughput_msps=93.6, max_abs_err=0.000152 (2^-12.68), power_index=1.47
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1226, accuracy_bits=12.9, luts=941, ffs=285, throughput_msps=93.6, max_abs_err=0.00013 (2^-12.91), power_index=1.48
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1286, accuracy_bits=13.4, luts=987, ffs=299, throughput_msps=93.6, max_abs_err=9.31e-05 (2^-13.39), power_index=1.55
- pipelined [data_width=20 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=2023, accuracy_bits=13.5, luts=994, ffs=1029, throughput_msps=264, max_abs_err=8.71e-05 (2^-13.49), power_index=2.43
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=2162, accuracy_bits=14.4, luts=1064, ffs=1098, throughput_msps=264, max_abs_err=4.64e-05 (2^-14.39), power_index=2.6
- pipelined [data_width=20 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2358, accuracy_bits=14.8, luts=1185, ffs=1172, throughput_msps=264, max_abs_err=3.61e-05 (2^-14.76), power_index=2.84
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=2440, accuracy_bits=15.1, luts=1205, ffs=1235, throughput_msps=264, max_abs_err=2.9e-05 (2^-15.07), power_index=2.94
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2547, accuracy_bits=15.4, luts=1281, ffs=1265, throughput_msps=264, max_abs_err=2.34e-05 (2^-15.38), power_index=3.07
Front coverage: luts_plus_ffs 1144..2547 (HV reference 4000); accuracy_bits 12.3..15.4 (HV reference 12); data_width on the front 17..20 (registry 8..28).

Per family:
- pipelined: 24 evals, 20 feasible; max throughput seen 273 MSPS; best accuracy 15.38 bits; best feasible luts_plus_ffs=1689; feasible ranges: data_width 17..20, n_iter 14..19, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 36 evals, 14 feasible; max throughput seen 171 MSPS; best accuracy 14.91 bits; best feasible luts_plus_ffs=1144; feasible ranges: data_width 17..18, n_iter 14..15, angle_guard 0..2, frac_guard 0..1, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (20 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (5 front designs; box front_anchored)
- `pipelined` (20 evals): data_width=18..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (5 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 63 feasible; hypervolume 1.433e+04 (+97.0%).

**No LLM call** (code's front-mapping round): This is the final round, and the front is feasible and well-covered, so no further exploration is possible. All three constraints are satisfiable: throughput_msps >= 32 (best seen 273, 0% violations), max_abs_err <= 0.000244141 (best 2.34e-05 = 2^-15.38), and sys_p99_batch_us <= 0.44 (best 0.165). The feasible Pareto front spans luts_plus_ffs 1144..2547 against HV ref 4000 and accuracy_bits 12.3..15.4 against HV ref 12, giving hypervolume 7272 with 26 unique feasible designs. The selection rule (min luts_plus_ffs) is served by the pipelined_m corner at luts_plus_ffs=1144, accuracy_bits=12.3, which still clears the error constraint (2^-12.35 <= 2^-12) and the system batch bound. No constraint is unreachable, so `infeasible` is not warranted; the front is good enough to stop.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.433e+04 (gain this round: +97.0%).
Feasible designs: 63 of 100 evaluations (54 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 19% violate; best seen 2.67e-07 (2^-21.84)
- sys_p99_batch_us <= 0.44: 25% violate; best seen 0.165

Pareto front (feasible, 11 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1144, accuracy_bits=12.3, luts=863, ffs=280, throughput_msps=97.8, max_abs_err=0.000192 (2^-12.35), power_index=1.38
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1145, accuracy_bits=12.5, luts=855, ffs=291, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.53), power_index=1.38
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1219, accuracy_bits=12.7, luts=920, ffs=299, throughput_msps=93.6, max_abs_err=0.000152 (2^-12.68), power_index=1.47
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1226, accuracy_bits=12.9, luts=941, ffs=285, throughput_msps=93.6, max_abs_err=0.00013 (2^-12.91), power_index=1.48
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1286, accuracy_bits=13.4, luts=987, ffs=299, throughput_msps=93.6, max_abs_err=9.31e-05 (2^-13.39), power_index=1.55
- pipelined_m [data_width=19 n_iter=21 angle_guard=3 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1962, accuracy_bits=14.5, luts=1438, ffs=524, throughput_msps=119, max_abs_err=4.3e-05 (2^-14.50), power_index=2.36
- pipelined_m [data_width=20 n_iter=21 angle_guard=3 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1976, accuracy_bits=15.3, luts=1502, ffs=474, throughput_msps=89.6, max_abs_err=2.4e-05 (2^-15.35), power_index=2.38
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2547, accuracy_bits=15.4, luts=1281, ffs=1265, throughput_msps=264, max_abs_err=2.34e-05 (2^-15.38), power_index=3.07
- pipelined_m [data_width=27 n_iter=23 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=3000, accuracy_bits=21.6, luts=2195, ffs=805, throughput_msps=110, max_abs_err=3.1e-07 (2^-21.62), power_index=3.61
- pipelined_m [data_width=27 n_iter=23 angle_guard=3 frac_guard=4 rounding=round m=3] luts_plus_ffs=3182, accuracy_bits=21.8, luts=2334, ffs=847, throughput_msps=106, max_abs_err=2.67e-07 (2^-21.84), power_index=3.83
Front coverage: luts_plus_ffs 1144..3182 (HV reference 4000); accuracy_bits 12.3..21.8 (HV reference 12); data_width on the front 16..27 (registry 8..28).

Per family:
- pipelined: 44 evals, 40 feasible; max throughput seen 273 MSPS; best accuracy 21.22 bits; best feasible luts_plus_ffs=1689; feasible ranges: data_width 17..24, n_iter 14..29, angle_guard -1..3, frac_guard 0..4
- pipelined_m: 56 evals, 23 feasible; max throughput seen 171 MSPS; best accuracy 21.84 bits; best feasible luts_plus_ffs=1144; feasible ranges: data_width 16..27, n_iter 14..29, angle_guard 0..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5490 in, 3379 out
- provider-reported cost: $0.0044
- full prompts and replies: `llm_trace.jsonl`

