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
`pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=3` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 861 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 332 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 124 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 124 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 56.2 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.44 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000168 (2^-12.54) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 5.49 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 4.52e-05 (2^-14.43) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.48 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.5 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (9 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=3` | 861 | 332 | 124.5 | 7 | 1.44 | 0.000168 (2^-12.54) | 12.54 |
| 1 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=2,rounding=round,m=4` | 956 | 287 | 93.6 | 6 | 1.5 | 0.00014 (2^-12.80) | 12.80 |
| 2 | `pipelined_m:data_width=16,n_iter=17,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1051 | 338 | 97.8 | 7 | 1.67 | 0.000138 (2^-12.83) | 12.83 |
| 3 | `pipelined_m:data_width=17,n_iter=17,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1086 | 350 | 93.6 | 7 | 1.73 | 0.000112 (2^-13.13) | 13.13 |
| 4 | `pipelined:data_width=17,n_iter=16,angle_guard=1,frac_guard=2,rounding=round` | 1021 | 1011 | 264.5 | 18 | 2.45 | 0.000109 (2^-13.16) | 13.16 |
| 5 | `pipelined_m:data_width=16,n_iter=25,angle_guard=4,frac_guard=4,rounding=round,m=3` | 1708 | 635 | 119.3 | 11 | 2.82 | 5.92e-05 (2^-14.04) | 14.04 |
| 6 | `pipelined_m:data_width=24,n_iter=21,angle_guard=3,frac_guard=4,rounding=trunc,m=3` | 1881 | 676 | 110.0 | 9 | 3.08 | 1.37e-06 (2^-19.47) | 19.47 |
| 7 | `pipelined_m:data_width=24,n_iter=21,angle_guard=4,frac_guard=4,rounding=round,m=2` | 1953 | 1052 | 152.6 | 13 | 3.62 | 1.11e-06 (2^-19.78) | 19.78 |
| 8 | `pipelined_m:data_width=24,n_iter=25,angle_guard=4,frac_guard=1,rounding=round,m=2` | 2180 | 1163 | 152.6 | 15 | 4.02 | 9.69e-07 (2^-19.98) | 19.98 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires throughput >= 32 Msps, max_abs_err <= 2^-12, and a 32-request burst to complete within 0.44 us of a 1 MHz tick. Both pipelined and pipelined_m deliver 1 result/cycle, so throughput is satisfied as long as Fmax >= 32 MHz. The critical constraints are accuracy (needs data_width >= 14 and sufficient n_iter) and the burst deadline (needs low latency and high Fmax). Pipelined offers the best Fmax and lowest per-iteration latency, while pipelined_m trades Fmax for fewer FFs, which is attractive for the area objective. We allocate equal budget to both to map the area-accuracy trade-off. Ranges are narrowed around the likely feasible region: data_width 13..17 (W=13 may fail, W=17 gives margin), n_iter 10..16 for pipelined (latency control) and 10..20 for pipelined_m (latency relaxed by m), angle_guard -1..2, frac_guard 0..2, and rounding fixed to round to avoid wasting evaluations on trunc, which is unlikely to meet the error bound at low W. This plan uses the full 100-evaluation budget across two families and four rounds, focusing on the Pareto front between LUTs+FFs and accuracy.*)
- `pipelined` (30 evals): data_width=13..17, n_iter=10..16, angle_guard=-1..2, frac_guard=0..2, rounding=round. *Why:* Pipelined gives the highest Fmax and lowest latency per iteration, making the 32-request burst deadline (sys_p99_batch_us <= 0.44) easiest to meet. We restrict n_iter to 10..16 to keep latency N+2 low enough that 32 results finish within 0.44 us even at moderate Fmax. data_width 13..17 covers the accuracy threshold (W>=14 needed for 2^-12) while allowing area minimisation. angle_guard and frac_guard are kept small to reduce area; round rounding is fixed because trunc is unlikely to meet the error bound at low W.
- `pipelined_m` (30 evals): data_width=13..17, n_iter=10..20, angle_guard=-1..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* pipelined_m reduces flip-flop count by registering every m stages, directly targeting the min luts_plus_ffs objective. Its latency ceil(N/m)+2 is lower than pipelined for the same N, so we can allow n_iter up to 20 for better accuracy without violating the batch deadline. m=2..4 balances area savings against the longer combinational path (lower Fmax); m>4 risks failing the throughput/batch constraints. Same data_width and guard ranges as pipelined to cover the feasible accuracy region.

**Result (code):** 60 evaluations this round, 60 total; 19 feasible; hypervolume 3131 (n/a).

**LLM decision:** `stop` — Final round: only stop/infeasible are admissible, and the front is clearly feasible, so infeasible is not warranted. All three constraints are met with margin by the 5-design Pareto front: throughput_msps best seen 282 vs required 32 (0% violations), sys_p99_batch_us best 0.154 vs 0.44 (0% violations), and max_abs_err best 0.000109 (2^-13.16) vs the 2^-12 = 0.000244 limit (68% of evaluations violate it, but the front does not). The front spans luts_plus_ffs 1193..2032 against the HV reference 4000 and accuracy_bits 12.5..13.2 against the reference 12, i.e. it already covers the accuracy objective past the reference and the area objective over a wide band, giving hypervolume 3131. The selection rule (min luts_plus_ffs) is satisfied by pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=3] at luts_plus_ffs=1193, accuracy_bits=12.5, throughput 124 MSPS, sys_p99_batch 0.154 us — comfortably inside every constraint. The remaining unexplored families (iterative, unrolled_k) are strictly lower-throughput per area on this spec (iterative/unrolled_k give one result every several cycles, while the 32-request burst needs the 1-result/cycle pipelined/pipelined_m behaviour that already dominates the front), so no further gain is expected within the remaining budget. Stopping with the current feasible front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 3131 (gain this round: n/a (first round)).
Feasible designs: 19 of 60 evaluations (11 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 68% violate; best seen 0.000109 (2^-13.16)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.154

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=3] luts_plus_ffs=1193, accuracy_bits=12.5, luts=861, ffs=332, throughput_msps=124, max_abs_err=0.000168 (2^-12.54), power_index=1.44
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1242, accuracy_bits=12.8, luts=956, ffs=287, throughput_msps=93.6, max_abs_err=0.00014 (2^-12.80), power_index=1.5
- pipelined_m [data_width=16 n_iter=17 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1389, accuracy_bits=12.8, luts=1051, ffs=338, throughput_msps=97.8, max_abs_err=0.000138 (2^-12.83), power_index=1.67
- pipelined_m [data_width=17 n_iter=17 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1437, accuracy_bits=13.1, luts=1086, ffs=350, throughput_msps=93.6, max_abs_err=0.000112 (2^-13.13), power_index=1.73
- pipelined [data_width=17 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=2032, accuracy_bits=13.2, luts=1021, ffs=1011, throughput_msps=264, max_abs_err=0.000109 (2^-13.16), power_index=2.45
Front coverage: luts_plus_ffs 1193..2032 (HV reference 4000); accuracy_bits 12.5..13.2 (HV reference 12); data_width on the front 16..17 (registry 8..28).

Per family:
- pipelined: 30 evals, 10 feasible; max throughput seen 282 MSPS; best accuracy 13.16 bits; best feasible luts_plus_ffs=1723; feasible ranges: data_width 17..17, n_iter 14..16, angle_guard 0..1, frac_guard 1..2
- pipelined_m: 30 evals, 9 feasible; max throughput seen 171 MSPS; best accuracy 13.13 bits; best feasible luts_plus_ffs=1193; feasible ranges: data_width 16..17, n_iter 15..20, angle_guard 1..2, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (32 evals): data_width=15..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)
- `pipelined` (8 evals): data_width=16..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 43 feasible; hypervolume 1.287e+04 (+311.0%).

**No LLM call** (code's front-mapping round): Final round: only stop/infeasible are admissible, and the front is clearly feasible, so infeasible is not warranted. All three constraints are met with margin by the 5-design Pareto front: throughput_msps best seen 282 vs required 32 (0% violations), sys_p99_batch_us best 0.154 vs 0.44 (0% violations), and max_abs_err best 0.000109 (2^-13.16) vs the 2^-12 = 0.000244 limit (68% of evaluations violate it, but the front does not). The front spans luts_plus_ffs 1193..2032 against the HV reference 4000 and accuracy_bits 12.5..13.2 against the reference 12, i.e. it already covers the accuracy objective past the reference and the area objective over a wide band, giving hypervolume 3131. The selection rule (min luts_plus_ffs) is satisfied by pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=3] at luts_plus_ffs=1193, accuracy_bits=12.5, throughput 124 MSPS, sys_p99_batch 0.154 us — comfortably inside every constraint. The remaining unexplored families (iterative, unrolled_k) are strictly lower-throughput per area on this spec (iterative/unrolled_k give one result every several cycles, while the 32-request burst needs the 1-result/cycle pipelined/pipelined_m behaviour that already dominates the front), so no further gain is expected within the remaining budget. Stopping with the current feasible front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.287e+04 (gain this round: +311.0%).
Feasible designs: 43 of 100 evaluations (33 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 49% violate; best seen 1.45e-07 (2^-22.72)
- sys_p99_batch_us <= 0.44: 8% violate; best seen 0.154

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=3] luts_plus_ffs=1193, accuracy_bits=12.5, luts=861, ffs=332, throughput_msps=124, max_abs_err=0.000168 (2^-12.54), power_index=1.44
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1242, accuracy_bits=12.8, luts=956, ffs=287, throughput_msps=93.6, max_abs_err=0.00014 (2^-12.80), power_index=1.5
- pipelined_m [data_width=16 n_iter=17 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1389, accuracy_bits=12.8, luts=1051, ffs=338, throughput_msps=97.8, max_abs_err=0.000138 (2^-12.83), power_index=1.67
- pipelined_m [data_width=17 n_iter=17 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1437, accuracy_bits=13.1, luts=1086, ffs=350, throughput_msps=93.6, max_abs_err=0.000112 (2^-13.13), power_index=1.73
- pipelined [data_width=17 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=2032, accuracy_bits=13.2, luts=1021, ffs=1011, throughput_msps=264, max_abs_err=0.000109 (2^-13.16), power_index=2.45
- pipelined_m [data_width=16 n_iter=25 angle_guard=4 frac_guard=4 rounding=round m=3] luts_plus_ffs=2343, accuracy_bits=14, luts=1708, ffs=635, throughput_msps=119, max_abs_err=5.92e-05 (2^-14.04), power_index=2.82
- pipelined_m [data_width=24 n_iter=21 angle_guard=3 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=2557, accuracy_bits=19.5, luts=1881, ffs=676, throughput_msps=110, max_abs_err=1.37e-06 (2^-19.47), power_index=3.08
- pipelined_m [data_width=24 n_iter=21 angle_guard=4 frac_guard=4 rounding=round m=2] luts_plus_ffs=3005, accuracy_bits=19.8, luts=1953, ffs=1052, throughput_msps=153, max_abs_err=1.11e-06 (2^-19.78), power_index=3.62
- pipelined_m [data_width=24 n_iter=25 angle_guard=4 frac_guard=1 rounding=round m=2] luts_plus_ffs=3343, accuracy_bits=20, luts=2180, ffs=1163, throughput_msps=153, max_abs_err=9.69e-07 (2^-19.98), power_index=4.02
Front coverage: luts_plus_ffs 1193..3343 (HV reference 4000); accuracy_bits 12.5..20 (HV reference 12); data_width on the front 16..24 (registry 8..28).

Per family:
- pipelined: 38 evals, 17 feasible; max throughput seen 282 MSPS; best accuracy 19.93 bits; best feasible luts_plus_ffs=1723; feasible ranges: data_width 16..27, n_iter 14..30, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 62 evals, 26 feasible; max throughput seen 171 MSPS; best accuracy 22.72 bits; best feasible luts_plus_ffs=1193; feasible ranges: data_width 16..25, n_iter 14..26, angle_guard -1..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5037 in, 4813 out
- provider-reported cost: $0.0072
- full prompts and replies: `llm_trace.jsonl`

