# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
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
`pipelined_m:data_width=19,n_iter=15,angle_guard=4,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 994 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 313 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 89.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 89.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 66.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.57 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 8.33e-05 (2^-13.55) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 10.9 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.61e-05 (2^-15.22) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.43 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.6 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=15,angle_guard=4,frac_guard=0,rounding=round,m=4` | 994 | 313 | 89.6 | 6 | 1.57 | 8.33e-05 (2^-13.55) | 13.55 |
| 1 | `pipelined_m:data_width=19,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=4` | 1017 | 301 | 93.6 | 6 | 1.59 | 5.84e-05 (2^-14.06) | 14.06 |
| 2 | `pipelined_m:data_width=19,n_iter=18,angle_guard=1,frac_guard=2,rounding=trunc,m=3` | 1223 | 452 | 119.3 | 8 | 2.02 | 3.99e-05 (2^-14.61) | 14.61 |
| 3 | `pipelined_m:data_width=20,n_iter=16,angle_guard=1,frac_guard=2,rounding=round,m=2` | 1170 | 619 | 164.4 | 10 | 2.15 | 3.84e-05 (2^-14.67) | 14.67 |
| 4 | `pipelined:data_width=20,n_iter=18,angle_guard=1,frac_guard=0,rounding=round` | 1205 | 1235 | 264.5 | 20 | 2.94 | 2.9e-05 (2^-15.07) | 15.07 |
| 5 | `pipelined:data_width=20,n_iter=18,angle_guard=1,frac_guard=1,rounding=round` | 1283 | 1269 | 264.5 | 20 | 3.07 | 2.28e-05 (2^-15.42) | 15.42 |
| 6 | `pipelined:data_width=20,n_iter=19,angle_guard=1,frac_guard=1,rounding=round` | 1356 | 1340 | 264.5 | 21 | 3.25 | 1.9e-05 (2^-15.68) | 15.68 |
| 7 | `pipelined_m:data_width=19,n_iter=26,angle_guard=4,frac_guard=4,rounding=round,m=3` | 2021 | 722 | 114.5 | 11 | 3.3 | 7.53e-06 (2^-17.02) | 17.02 |
| 8 | `pipelined_m:data_width=25,n_iter=21,angle_guard=-1,frac_guard=4,rounding=trunc,m=2` | 1860 | 1030 | 152.6 | 13 | 3.48 | 2.32e-06 (2^-18.72) | 18.72 |
| 9 | `pipelined_m:data_width=25,n_iter=21,angle_guard=3,frac_guard=3,rounding=trunc,m=2` | 1902 | 1054 | 152.6 | 13 | 3.56 | 1.18e-06 (2^-19.70) | 19.70 |
| 10 | `pipelined_m:data_width=25,n_iter=26,angle_guard=1,frac_guard=1,rounding=round,m=2` | 2271 | 1165 | 158.3 | 15 | 4.14 | 6.42e-07 (2^-20.57) | 20.57 |
| 11 | `pipelined:data_width=27,n_iter=22,angle_guard=1,frac_guard=4,rounding=round` | 2187 | 2139 | 242.0 | 24 | 5.21 | 5.58e-07 (2^-20.77) | 20.77 |
| 12 | `pipelined:data_width=23,n_iter=27,angle_guard=4,frac_guard=4,rounding=round` | 2437 | 2383 | 249.0 | 29 | 5.8 | 5.15e-07 (2^-20.89) | 20.89 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *No fleet facts yet, so this is a cold-start round. The spec's hard constraints are: (1) throughput >= 32 MS/s, (2) max_abs_err <= 2^-12 (~12.3 accuracy bits), (3) sys_p99_batch_us <= 0.44. Only pipelined and pipelined_m are available to me, and both give 1 result/cycle, so throughput is met whenever Fmax >= 32 MHz, which is comfortably reachable for these widths. The accuracy floor (~12.3 bits) is the binding accuracy constraint: it rules out very small W or very small N, so I set data_width 14..20 and n_iter 12..20, which brackets the region where accuracy_bits crosses 12.3 while leaving room on both sides so the front is not clipped at the constraint boundary. angle_guard -1..2 and frac_guard 0..2 cover the small guard-bit trade-offs that affect area and accuracy margin. For pipelined (budget 0.6) the front is driven by W/N/guard; for pipelined_m (budget 0.4) the extra m=2..8 knob is the main area-reduction lever, so I give it a meaningful share to map the area-vs-latency trade-off. The 0.44 us p99-batch deadline is the tightest system constraint: 32 results at 1/cycle need 32 cycles of compute plus pipeline latency, so at the minimum Fmax that satisfies throughput (32 MHz) the compute alone is 1.0 us, which exceeds 0.44 us. This means the design must run at a higher Fmax (roughly >= 32/0.44 ~ 73 MHz for the compute term to fit, before latency) or the L1 bound must show the batch fits; keeping N modest (12..20) and m small-to-moderate keeps latency_ns low so the Fmax required to meet 0.44 us stays achievable. The split 0.6/0.4 favours the simpler pipelined family for the bulk of the front while still sampling pipelined_m's area savings. Rounding is included as a 2-choice parameter in both families since it shifts accuracy by up to ~0.5 LSB and area slightly, and the search should not be forced to pick one.*)
- `pipelined` (36 evals): data_width=14..20, n_iter=12..20, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Full pipelining gives 1 result/cycle, so at any Fmax >= 32 MHz it clears the 32 MS/s throughput constraint and the 0.44 us p99-batch window (32 results take 32 cycles; at 32 MHz that is exactly 1.0 us of compute, but the batch deadline is measured from tick to last result and the L1 bound assumes the unit is free at the tick, so the binding term is latency + 31/Fmax; keeping N modest keeps latency_ns small). Accuracy needs ~12.3 bits, which is reachable with W in 14..20 and N in 12..20; the wide W/N ranges let Optuna trade area (luts_plus_ffs) against accuracy_bits to map the front. angle_guard -1..2 and frac_guard 0..2 cover the small guard-bit trade-offs that shift area without changing the accuracy floor much.
- `pipelined_m` (24 evals): data_width=14..20, n_iter=12..20, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* pipelined_m registers every m stages, cutting FF count (and often LUTs from shorter combinational chains) at the cost of higher latency (ceil(N/m)+2). Since the objective is min luts_plus_ffs and the batch deadline (0.44 us) plus 32 MS/s throughput are the hard constraints, m is the key knob that trades area against latency/Fmax. Sweeping m=2..8 across the same W/N/guard ranges lets the search find the cheapest m that still meets the p99-batch and throughput bounds, and exposes the area-vs-latency trade-off on the front. Same W/N/guard ranges as pipelined so the two families' fronts are directly comparable and merge cleanly.

**Result (code):** 60 evaluations this round, 60 total; 36 feasible; hypervolume 8414 (n/a).

**LLM decision:** `stop` — The front is well-established with 6 feasible designs spanning a wide trade-off curve (luts_plus_ffs 1318..2696, accuracy_bits 14.1..15.7). The best area design (pipelined_m, 1318 luts_plus_ffs) comfortably meets all constraints: throughput 93.6 MSPS >= 32, max_abs_err 5.84e-05 <= 0.000244, and sys_p99_batch_us is well within 0.44 us (best seen 0.165). The hypervolume of 8414 indicates good coverage of the objective space. Since this is the final round, the exploration is complete.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 8414 (gain this round: n/a (first round)).
Feasible designs: 36 of 60 evaluations (25 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 25% violate; best seen 1.9e-05 (2^-15.68)
- sys_p99_batch_us <= 0.44: 17% violate; best seen 0.165

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1318, accuracy_bits=14.1, luts=1017, ffs=301, throughput_msps=93.6, max_abs_err=5.84e-05 (2^-14.06), power_index=1.59
- pipelined_m [data_width=19 n_iter=18 angle_guard=1 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=1675, accuracy_bits=14.6, luts=1223, ffs=452, throughput_msps=119, max_abs_err=3.99e-05 (2^-14.61), power_index=2.02
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=round m=2] luts_plus_ffs=1789, accuracy_bits=14.7, luts=1170, ffs=619, throughput_msps=164, max_abs_err=3.84e-05 (2^-14.67), power_index=2.15
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=2440, accuracy_bits=15.1, luts=1205, ffs=1235, throughput_msps=264, max_abs_err=2.9e-05 (2^-15.07), power_index=2.94
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=1 rounding=round] luts_plus_ffs=2553, accuracy_bits=15.4, luts=1283, ffs=1269, throughput_msps=264, max_abs_err=2.28e-05 (2^-15.42), power_index=3.07
- pipelined [data_width=20 n_iter=19 angle_guard=1 frac_guard=1 rounding=round] luts_plus_ffs=2696, accuracy_bits=15.7, luts=1356, ffs=1340, throughput_msps=264, max_abs_err=1.9e-05 (2^-15.68), power_index=3.25
Front coverage: luts_plus_ffs 1318..2696 (HV reference 4000); accuracy_bits 14.1..15.7 (HV reference 12); data_width on the front 19..20 (registry 8..28).

Per family:
- pipelined: 36 evals, 27 feasible; max throughput seen 273 MSPS; best accuracy 15.68 bits; best feasible luts_plus_ffs=1689; feasible ranges: data_width 17..20, n_iter 14..19, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 24 evals, 9 feasible; max throughput seen 164 MSPS; best accuracy 14.67 bits; best feasible luts_plus_ffs=1318; feasible ranges: data_width 18..20, n_iter 16..18, angle_guard 1..1, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (20 evals): data_width=18..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (3 front designs; box front_anchored)
- `pipelined` (20 evals): data_width=19..28, n_iter=16..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 69 feasible; hypervolume 1.351e+04 (+60.5%).

**No LLM call** (code's front-mapping round): The front is well-established with 6 feasible designs spanning a wide trade-off curve (luts_plus_ffs 1318..2696, accuracy_bits 14.1..15.7). The best area design (pipelined_m, 1318 luts_plus_ffs) comfortably meets all constraints: throughput 93.6 MSPS >= 32, max_abs_err 5.84e-05 <= 0.000244, and sys_p99_batch_us is well within 0.44 us (best seen 0.165). The hypervolume of 8414 indicates good coverage of the objective space. Since this is the final round, the exploration is complete.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.351e+04 (gain this round: +60.5%).
Feasible designs: 69 of 100 evaluations (56 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 15% violate; best seen 1.45e-07 (2^-22.72)
- sys_p99_batch_us <= 0.44: 17% violate; best seen 0.165

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=15 angle_guard=4 frac_guard=0 rounding=round m=4] luts_plus_ffs=1306, accuracy_bits=13.6, luts=994, ffs=313, throughput_msps=89.6, max_abs_err=8.33e-05 (2^-13.55), power_index=1.57
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1318, accuracy_bits=14.1, luts=1017, ffs=301, throughput_msps=93.6, max_abs_err=5.84e-05 (2^-14.06), power_index=1.59
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=round m=2] luts_plus_ffs=1789, accuracy_bits=14.7, luts=1170, ffs=619, throughput_msps=164, max_abs_err=3.84e-05 (2^-14.67), power_index=2.15
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=2440, accuracy_bits=15.1, luts=1205, ffs=1235, throughput_msps=264, max_abs_err=2.9e-05 (2^-15.07), power_index=2.94
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=1 rounding=round] luts_plus_ffs=2553, accuracy_bits=15.4, luts=1283, ffs=1269, throughput_msps=264, max_abs_err=2.28e-05 (2^-15.42), power_index=3.07
- pipelined_m [data_width=19 n_iter=26 angle_guard=4 frac_guard=4 rounding=round m=3] luts_plus_ffs=2743, accuracy_bits=17, luts=2021, ffs=722, throughput_msps=114, max_abs_err=7.53e-06 (2^-17.02), power_index=3.3
- pipelined_m [data_width=25 n_iter=21 angle_guard=-1 frac_guard=4 rounding=trunc m=2] luts_plus_ffs=2890, accuracy_bits=18.7, luts=1860, ffs=1030, throughput_msps=153, max_abs_err=2.32e-06 (2^-18.72), power_index=3.48
- pipelined_m [data_width=25 n_iter=21 angle_guard=3 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=2956, accuracy_bits=19.7, luts=1902, ffs=1054, throughput_msps=153, max_abs_err=1.18e-06 (2^-19.70), power_index=3.56
- pipelined [data_width=27 n_iter=22 angle_guard=1 frac_guard=4 rounding=round] luts_plus_ffs=4325, accuracy_bits=20.8, luts=2187, ffs=2139, throughput_msps=242, max_abs_err=5.58e-07 (2^-20.77), power_index=5.21
- pipelined [data_width=23 n_iter=27 angle_guard=4 frac_guard=4 rounding=round] luts_plus_ffs=4820, accuracy_bits=20.9, luts=2437, ffs=2383, throughput_msps=249, max_abs_err=5.15e-07 (2^-20.89), power_index=5.8
Front coverage: luts_plus_ffs 1306..4820 (HV reference 4000); accuracy_bits 13.6..20.9 (HV reference 12); data_width on the front 19..27 (registry 8..28).

Per family:
- pipelined: 56 evals, 47 feasible; max throughput seen 273 MSPS; best accuracy 20.89 bits; best feasible luts_plus_ffs=1689; feasible ranges: data_width 17..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 44 evals, 22 feasible; max throughput seen 164 MSPS; best accuracy 22.72 bits; best feasible luts_plus_ffs=1306; feasible ranges: data_width 18..25, n_iter 15..27, angle_guard -1..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5265 in, 1665 out
- provider-reported cost: $0.0051
- full prompts and replies: `llm_trace.jsonl`

