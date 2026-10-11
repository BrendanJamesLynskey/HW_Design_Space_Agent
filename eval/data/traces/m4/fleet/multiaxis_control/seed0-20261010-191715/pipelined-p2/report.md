# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`pipelined_m:data_width=19,n_iter=18,angle_guard=-2,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 1098 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 351 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 74.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.74 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00019 (2^-12.36) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 25 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 3.76e-05 (2^-14.70) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 4.93 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.4 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (12 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=18,angle_guard=-2,frac_guard=0,rounding=round,m=4` | 1098 | 351 | 93.6 | 7 | 1.74 | 0.00019 (2^-12.36) | 12.36 |
| 1 | `pipelined_m:data_width=19,n_iter=17,angle_guard=1,frac_guard=0,rounding=trunc,m=3` | 1084 | 432 | 119.3 | 8 | 1.82 | 7.8e-05 (2^-13.65) | 13.65 |
| 2 | `pipelined_m:data_width=21,n_iter=17,angle_guard=3,frac_guard=0,rounding=trunc,m=3` | 1219 | 484 | 114.5 | 8 | 2.05 | 3.12e-05 (2^-14.97) | 14.97 |
| 3 | `pipelined_m:data_width=17,n_iter=19,angle_guard=4,frac_guard=4,rounding=round,m=4` | 1350 | 381 | 93.6 | 7 | 2.08 | 2.86e-05 (2^-15.09) | 15.09 |
| 4 | `pipelined_m:data_width=22,n_iter=18,angle_guard=-1,frac_guard=1,rounding=round,m=4` | 1359 | 418 | 89.6 | 7 | 2.14 | 1.78e-05 (2^-15.77) | 15.77 |
| 5 | `pipelined_m:data_width=22,n_iter=21,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 1523 | 486 | 93.6 | 8 | 2.42 | 1.39e-05 (2^-16.14) | 16.14 |
| 6 | `pipelined_m:data_width=21,n_iter=21,angle_guard=3,frac_guard=2,rounding=trunc,m=4` | 1607 | 504 | 89.6 | 8 | 2.54 | 7.43e-06 (2^-17.04) | 17.04 |
| 7 | `pipelined_m:data_width=22,n_iter=23,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1790 | 513 | 89.6 | 8 | 2.77 | 4.68e-06 (2^-17.71) | 17.71 |
| 8 | `pipelined_m:data_width=27,n_iter=22,angle_guard=0,frac_guard=2,rounding=trunc,m=3` | 2019 | 793 | 110.0 | 10 | 3.38 | 6.47e-07 (2^-20.56) | 20.56 |
| 9 | `pipelined_m:data_width=27,n_iter=25,angle_guard=3,frac_guard=2,rounding=trunc,m=3` | 2383 | 913 | 110.0 | 11 | 3.97 | 1.44e-07 (2^-22.73) | 22.73 |
| 10 | `pipelined_m:data_width=27,n_iter=29,angle_guard=3,frac_guard=2,rounding=trunc,m=3` | 2779 | 1009 | 110.0 | 12 | 4.56 | 1.14e-07 (2^-23.06) | 23.06 |
| 11 | `pipelined_m:data_width=27,n_iter=30,angle_guard=3,frac_guard=2,rounding=round,m=3` | 2935 | 1011 | 110.0 | 12 | 4.75 | 6.73e-08 (2^-23.82) | 23.82 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraints are the 0.44 us p99 batch bound (32 requests arriving at once, so ~latency+31 cycles must fit in 0.44 us) and max_abs_err <= 2^-12; throughput >= 32 msps is trivially met by any 1-result/cycle family. Accuracy is identical across families for the same (data_width, n_iter, angle_guard, frac_guard, rounding), so the family choice is purely about latency vs area: pipelined_m's ceil(N/m)+2 latency lets it trade Fmax for far fewer registers, which is why it dominates the merged front (8/9 designs, best 1193 LUT+FF). Round 1 therefore spends most of the budget mapping pipelined_m over the full m range and a data_width/n_iter box that brackets the 2^-12 accuracy requirement, with a smaller pipelined allocation to cover the high-Fmax low-N corner. Ranges are kept moderately wide for this first round so later rounds can narrow around the discovered front.*)
- `pipelined_m` (70 evals): data_width=12..20, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* pipelined_m already holds 8 of the 9 merged-front designs and the cheapest feasible point (1193 LUT+FF); its ceil(N/m)+2 latency is the only way to fit 32 back-to-back results inside the 0.44 us tick budget while keeping area low, so it deserves the bulk of the budget to map the area/latency/accuracy trade-off over m and the accuracy knobs.
- `pipelined` (30 evals): data_width=12..20, n_iter=8..18, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* pipelined gives 1 result/cycle at the highest Fmax (register per micro-rotation), so it can only meet the 0.44 us batch bound at low N and high clock; a smaller share probes that high-Fmax/low-latency corner and keeps the merged front from being single-family.

**Result (code):** 100 evaluations this round, 100 total; 21 feasible; hypervolume 7049 (n/a).

**LLM decision:** `map_front` — Round 1 leaves 100 of 200 evals and the feasible front is only 3 designs, all pipelined_m, spanning luts_plus_ffs 1624..1731 against an HV reference of 4000 and accuracy_bits 12.1..15.1. That is a very thin slice of the area objective, so hypervolume is being lost to poor coverage of the trade-off curve rather than to a bad corner. The min-area corner is already pinned near the accuracy constraint (lowest front point is 12.10 bits vs the 2^-12 = 12.0-bit limit), and pipelined_m's feasible n_iter is fixed at 19, so there is little room to push area lower by refining alone; the useful gain is filling in the curve at higher accuracy. pipelined is dominated (best feasible luts_plus_ffs 1792 vs 1624) but still contributes points, and iterative/unrolled_k cannot reach the 32 MSPS throughput constraint (N+3 and ceil(N/k)+3 cycles/result), so the front families are pipelined and pipelined_m. Spending this round on NSGA-II over the full ranges of those two families, seeded with the current front, is the best use of the remaining budget to widen and densify the front before the reserved mapping pass.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 7049 (gain this round: n/a (first round)).
Feasible designs: 21 of 100 evaluations (17 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 73% violate; best seen 1.7e-05 (2^-15.84)
- sys_p99_batch_us <= 0.44: 21% violate; best seen 0.155

Pareto front (feasible, 3 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=19 angle_guard=4 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=1624, accuracy_bits=12.1, luts=1162, ffs=462, throughput_msps=119, max_abs_err=0.000228 (2^-12.10), power_index=1.96
- pipelined_m [data_width=19 n_iter=19 angle_guard=-2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1638, accuracy_bits=12.4, luts=1162, ffs=476, throughput_msps=119, max_abs_err=0.00019 (2^-12.36), power_index=1.97
- pipelined_m [data_width=17 n_iter=19 angle_guard=4 frac_guard=4 rounding=round m=4] luts_plus_ffs=1731, accuracy_bits=15.1, luts=1350, ffs=381, throughput_msps=93.6, max_abs_err=2.86e-05 (2^-15.09), power_index=2.08
Front coverage: luts_plus_ffs 1624..1731 (HV reference 4000); accuracy_bits 12.1..15.1 (HV reference 12); data_width on the front 15..19 (registry 8..28).

Per family:
- pipelined: 30 evals, 9 feasible; max throughput seen 282 MSPS; best accuracy 13.70 bits; best feasible luts_plus_ffs=1792; feasible ranges: data_width 17..20, n_iter 14..17, angle_guard -2..3, frac_guard 2..4
- pipelined_m: 70 evals, 12 feasible; max throughput seen 171 MSPS; best accuracy 15.84 bits; best feasible luts_plus_ffs=1624; feasible ranges: data_width 15..20, n_iter 19..19, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `pipelined_m` (20 evals): data_width=14..28, n_iter=17..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (3 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 31 feasible; hypervolume 1.154e+04 (+63.8%).

**LLM decision:** `map_front` — The feasible front is only 5 designs, all pipelined_m, and it is sparse: luts_plus_ffs spans 1449..3108 against the HV reference 4000, and accuracy_bits spans 12.4..19 against the reference 12. The cheapest point (1449, 12.4 bits) sits right at the 2^-12 accuracy constraint boundary, so the low-area corner that the selection rule (min luts_plus_ffs) cares about is barely resolved, and the high-accuracy end (19 bits at 3108) leaves a large uncovered band up to the 4000 reference. pipelined is dominated (best feasible luts_plus_ffs=1792 vs 1449) and never reaches the front, so the useful search space is pipelined_m's full ranges (data_width 15..28, n_iter 18..28, angle_guard -2..4, frac_guard 0..4, m 2..4). With 80 of 200 evals left and only one family on the front, the reserved budget is best spent letting NSGA-II map the whole trade-off curve seeded with the current front rather than narrowing around a 5-point sample.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.154e+04 (gain this round: +63.8%).
Feasible designs: 31 of 120 evaluations (26 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 65% violate; best seen 1.92e-06 (2^-18.99)
- sys_p99_batch_us <= 0.44: 23% violate; best seen 0.155

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=18 angle_guard=-2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1449, accuracy_bits=12.4, luts=1098, ffs=351, throughput_msps=93.6, max_abs_err=0.00019 (2^-12.36), power_index=1.74
- pipelined_m [data_width=17 n_iter=19 angle_guard=4 frac_guard=4 rounding=round m=4] luts_plus_ffs=1731, accuracy_bits=15.1, luts=1350, ffs=381, throughput_msps=93.6, max_abs_err=2.86e-05 (2^-15.09), power_index=2.08
- pipelined_m [data_width=22 n_iter=18 angle_guard=-1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1777, accuracy_bits=15.8, luts=1359, ffs=418, throughput_msps=89.6, max_abs_err=1.78e-05 (2^-15.77), power_index=2.14
- pipelined_m [data_width=20 n_iter=28 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=2832, accuracy_bits=15.9, luts=2067, ffs=765, throughput_msps=119, max_abs_err=1.61e-05 (2^-15.92), power_index=3.41
- pipelined_m [data_width=28 n_iter=20 angle_guard=3 frac_guard=3 rounding=round m=2] luts_plus_ffs=3108, accuracy_bits=19, luts=2046, ffs=1061, throughput_msps=147, max_abs_err=1.92e-06 (2^-18.99), power_index=3.74
Front coverage: luts_plus_ffs 1449..3108 (HV reference 4000); accuracy_bits 12.4..19 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- pipelined: 30 evals, 9 feasible; max throughput seen 282 MSPS; best accuracy 13.70 bits; best feasible luts_plus_ffs=1792; feasible ranges: data_width 17..20, n_iter 14..17, angle_guard -2..3, frac_guard 2..4
- pipelined_m: 90 evals, 22 feasible; max throughput seen 171 MSPS; best accuracy 18.99 bits; best feasible luts_plus_ffs=1449; feasible ranges: data_width 15..28, n_iter 18..28, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (80 evals): data_width=16..28, n_iter=16..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (5 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 77 feasible; hypervolume 1.753e+04 (+51.9%).

**LLM decision:** `stop` — Final round with the full 200-eval budget spent (100/round, 4 rounds). The exploration is complete and the constraints are all reachable: 0% of evaluations violate throughput_msps >= 32 (best 282 MSPS, far above the 32 MSPS requirement), and the feasible front contains 12 designs whose max_abs_err is at or below 2^-12 — the cheapest, pipelined_m [W=19 n_iter=18 angle_guard=-2 frac_guard=0 round m=4], has luts_plus_ffs=1449 and max_abs_err=0.00019 (2^-12.36), and the best accuracy on the front reaches 2^-23.82 (6.73e-08). The system constraint sys_p99_batch_us <= 0.44 is also met, with best seen 0.155 us, well inside the bound. Hypervolume improved +51.9% this round to 1.753e+04, and the front already spans luts_plus_ffs 1449..3946 against the HV reference 4000 and accuracy_bits 12.4..23.8 against the reference 12, i.e. it covers essentially the full objective ranges, so further mapping would yield little. Both families on the front (pipelined, pipelined_m) have been explored and no unexplored family remains. The selection rule (min luts_plus_ffs) picks the 1449-area design, which satisfies every constraint. No infeasibility evidence exists, so stopping is correct.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.753e+04 (gain this round: +51.9%).
Feasible designs: 77 of 200 evaluations (66 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 42% violate; best seen 6.73e-08 (2^-23.82)
- sys_p99_batch_us <= 0.44: 30% violate; best seen 0.155

Pareto front (feasible, 12 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=18 angle_guard=-2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1449, accuracy_bits=12.4, luts=1098, ffs=351, throughput_msps=93.6, max_abs_err=0.00019 (2^-12.36), power_index=1.74
- pipelined_m [data_width=19 n_iter=17 angle_guard=1 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=1516, accuracy_bits=13.6, luts=1084, ffs=432, throughput_msps=119, max_abs_err=7.8e-05 (2^-13.65), power_index=1.82
- pipelined_m [data_width=21 n_iter=17 angle_guard=3 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=1703, accuracy_bits=15, luts=1219, ffs=484, throughput_msps=114, max_abs_err=3.12e-05 (2^-14.97), power_index=2.05
- pipelined_m [data_width=22 n_iter=18 angle_guard=-1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1777, accuracy_bits=15.8, luts=1359, ffs=418, throughput_msps=89.6, max_abs_err=1.78e-05 (2^-15.77), power_index=2.14
- pipelined_m [data_width=22 n_iter=21 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=2009, accuracy_bits=16.1, luts=1523, ffs=486, throughput_msps=93.6, max_abs_err=1.39e-05 (2^-16.14), power_index=2.42
- pipelined_m [data_width=21 n_iter=21 angle_guard=3 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=2111, accuracy_bits=17, luts=1607, ffs=504, throughput_msps=89.6, max_abs_err=7.43e-06 (2^-17.04), power_index=2.54
- pipelined_m [data_width=22 n_iter=23 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=2303, accuracy_bits=17.7, luts=1790, ffs=513, throughput_msps=89.6, max_abs_err=4.68e-06 (2^-17.71), power_index=2.77
- pipelined_m [data_width=27 n_iter=25 angle_guard=3 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=3296, accuracy_bits=22.7, luts=2383, ffs=913, throughput_msps=110, max_abs_err=1.44e-07 (2^-22.73), power_index=3.97
- pipelined_m [data_width=27 n_iter=29 angle_guard=3 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=3788, accuracy_bits=23.1, luts=2779, ffs=1009, throughput_msps=110, max_abs_err=1.14e-07 (2^-23.06), power_index=4.56
- pipelined_m [data_width=27 n_iter=30 angle_guard=3 frac_guard=2 rounding=round m=3] luts_plus_ffs=3946, accuracy_bits=23.8, luts=2935, ffs=1011, throughput_msps=110, max_abs_err=6.73e-08 (2^-23.82), power_index=4.75
Front coverage: luts_plus_ffs 1449..3946 (HV reference 4000); accuracy_bits 12.4..23.8 (HV reference 12); data_width on the front 17..27 (registry 8..28).

Per family:
- pipelined: 30 evals, 9 feasible; max throughput seen 282 MSPS; best accuracy 13.70 bits; best feasible luts_plus_ffs=1792; feasible ranges: data_width 17..20, n_iter 14..17, angle_guard -2..3, frac_guard 2..4
- pipelined_m: 170 evals, 68 feasible; max throughput seen 171 MSPS; best accuracy 23.82 bits; best feasible luts_plus_ffs=1449; feasible ranges: data_width 15..28, n_iter 17..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 12963 in, 7886 out
- provider-reported cost: $0.0065
- full prompts and replies: `llm_trace.jsonl`

