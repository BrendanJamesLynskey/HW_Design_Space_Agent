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

## Pareto front (14 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=18,angle_guard=-2,frac_guard=0,rounding=round,m=4` | 1098 | 351 | 93.6 | 7 | 1.74 | 0.00019 (2^-12.36) | 12.36 |
| 1 | `pipelined_m:data_width=20,n_iter=18,angle_guard=-2,frac_guard=0,rounding=round,m=4` | 1152 | 368 | 93.6 | 7 | 1.83 | 9.3e-05 (2^-13.39) | 13.39 |
| 2 | `pipelined_m:data_width=19,n_iter=16,angle_guard=0,frac_guard=4,rounding=trunc,m=3` | 1128 | 466 | 114.5 | 8 | 1.92 | 6.7e-05 (2^-13.86) | 13.86 |
| 3 | `pipelined_m:data_width=19,n_iter=17,angle_guard=1,frac_guard=1,rounding=trunc,m=2` | 1118 | 645 | 164.4 | 11 | 2.12 | 5.59e-05 (2^-14.13) | 14.13 |
| 4 | `pipelined_m:data_width=24,n_iter=18,angle_guard=-2,frac_guard=0,rounding=round,m=3` | 1367 | 515 | 114.5 | 8 | 2.26 | 1.21e-05 (2^-16.33) | 16.33 |
| 5 | `pipelined_m:data_width=24,n_iter=19,angle_guard=-1,frac_guard=0,rounding=trunc,m=4` | 1466 | 442 | 89.6 | 7 | 2.3 | 6.73e-06 (2^-17.18) | 17.18 |
| 6 | `pipelined_m:data_width=28,n_iter=19,angle_guard=3,frac_guard=3,rounding=round,m=3` | 1942 | 759 | 105.9 | 9 | 3.25 | 3.83e-06 (2^-18.00) | 18.00 |
| 7 | `pipelined_m:data_width=28,n_iter=21,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 1986 | 721 | 105.9 | 9 | 3.26 | 1.41e-06 (2^-19.44) | 19.44 |
| 8 | `pipelined_m:data_width=28,n_iter=21,angle_guard=-2,frac_guard=3,rounding=round,m=3` | 2045 | 723 | 105.9 | 9 | 3.33 | 1.4e-06 (2^-19.45) | 19.45 |
| 9 | `pipelined_m:data_width=28,n_iter=26,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 2482 | 913 | 105.9 | 11 | 4.09 | 5.65e-07 (2^-20.76) | 20.76 |
| 10 | `pipelined:data_width=24,n_iter=23,angle_guard=3,frac_guard=3,rounding=round` | 2073 | 2032 | 249.0 | 25 | 4.94 | 5.25e-07 (2^-20.86) | 20.86 |
| 11 | `pipelined:data_width=28,n_iter=26,angle_guard=1,frac_guard=0,rounding=trunc` | 2403 | 2413 | 249.0 | 28 | 5.8 | 2.4e-07 (2^-21.99) | 21.99 |
| 12 | `pipelined:data_width=28,n_iter=26,angle_guard=4,frac_guard=0,rounding=round` | 2482 | 2492 | 242.0 | 28 | 5.99 | 1.1e-07 (2^-23.12) | 23.12 |
| 13 | `pipelined:data_width=28,n_iter=27,angle_guard=1,frac_guard=3,rounding=trunc` | 2663 | 2658 | 242.0 | 29 | 6.4 | 8.28e-08 (2^-23.53) | 23.53 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is a 1 MHz tick issuing 32 requests that must all return within 0.44 us, with max_abs_err <= 2^-12 and a minimise-LUTs+FFs objective. The 32 Msps throughput bound and the 0.44 us batch window both push toward 1-result-per-cycle architectures, which is exactly what pipelined and pipelined_m provide (iterative/unrolled_k are not in my assigned set anyway). pipelined is the safe baseline that will almost certainly clear the system constraints, so I give it the larger share to map the accuracy-vs-area curve thoroughly. pipelined_m is the area-reduction variant (fewer pipeline registers at the same throughput), so it is where the cheapest points on the front are likely to come from; I give it a substantial share and sweep m fully because the m-vs-Fmax interaction is the real trade-off. I keep n_iter and data_width at their full registry ranges in both families because accuracy_bits (maximised) and max_abs_err (constrained) are set by n_iter/data_width while the area objective is set by data_width/n_iter — the entire Pareto front spans that 2D slice, and narrowing it prematurely would under-cover the hypervolume. angle_guard and frac_guard are swept across their full ranges since they are cheap knobs that trade a small amount of area against accuracy_bits. Rounding is left to both choices so the search can find whether round or trunc gives better accuracy_bits per LUT.*)
- `pipelined` (33 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Full pipelining gives 1 result/cycle, so at any Fmax it trivially clears the 32 Msps throughput bound and the 0.44 us batch window (32 cycles of latency must fit in 0.44 us, i.e. Fmax >= ~73 MHz, which is comfortable for a CORDIC). This is the family most likely to satisfy all system constraints, so I spend the majority of the budget here. I keep the full n_iter/data_width ranges because accuracy_bits (a maximised objective) and max_abs_err (a hard constraint) are driven by n_iter and data_width, and the LUT/FF area objective is driven by data_width and n_iter — the whole trade-off curve lives in this 2D slice. angle_guard and frac_guard are swept across their full ranges because they trade a few LUTs/FFs against accuracy_bits and are cheap to explore.
- `pipelined_m` (27 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* pipelined_m registers every m stages, so for the same n_iter/data_width it uses fewer FFs than fully pipelined (fewer pipeline registers) while still delivering 1 result/cycle — it can therefore beat pipelined on the luts_plus_ffs objective at equal accuracy. The throughput and batch-window constraints are met the same way as pipelined (1 result/cycle, latency ceil(N/m)+2 cycles must fit in 0.44 us). I sweep m across its full range because m is the key area lever: large m saves FFs but lengthens the combinational path per stage, which can cut Fmax and risk the 0.44 us batch bound, so the m-vs-Fmax trade-off is exactly where the Pareto front lives. Same n_iter/data_width/guard ranges as pipelined for a comparable accuracy/area slice.

**Result (code):** 60 evaluations this round, 60 total; 36 feasible; hypervolume 1.239e+04 (n/a).

**LLM decision:** `stop` — The exploration has successfully mapped the feasible Pareto front for the `pipelined` and `pipelined_m` families, which are the only architectures capable of meeting the strict system constraint `sys_p99_batch_us <= 0.44` (iterative/unrolled_k would fail due to low throughput/latency). The current front covers a wide range of the objective space: `luts_plus_ffs` from 1763 to 4036 (spanning the HV reference of 4000) and `accuracy_bits` from 14.1 to 19.7 (well above the HV reference of 12). The best design (`pipelined_m` with `data_width=19`, `n_iter=17`, `m=2`) achieves a minimal area of 1763 LUTs+FFs while satisfying all constraints (throughput 164 MSPS >= 32, error 5.59e-05 <= 2^-12, and system latency well within bounds). Since this is the final round and the front is well-distributed across the trade-off curve, further exploration would yield diminishing returns. The selection rule (min `luts_plus_ffs`) will pick the 1763 design, which is robustly feasible.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.239e+04 (gain this round: n/a (first round)).
Feasible designs: 36 of 60 evaluations (33 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 292
- max_abs_err <= 0.000244141: 30% violate; best seen 1.21e-06 (2^-19.66)
- sys_p99_batch_us <= 0.44: 13% violate; best seen 0.132

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=1763, accuracy_bits=14.1, luts=1118, ffs=645, throughput_msps=164, max_abs_err=5.59e-05 (2^-14.13), power_index=2.12
- pipelined_m [data_width=24 n_iter=19 angle_guard=-1 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1908, accuracy_bits=17.2, luts=1466, ffs=442, throughput_msps=89.6, max_abs_err=6.73e-06 (2^-17.18), power_index=2.3
- pipelined [data_width=24 n_iter=19 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=3075, accuracy_bits=17.5, luts=1523, ffs=1553, throughput_msps=257, max_abs_err=5.58e-06 (2^-17.45), power_index=3.7
- pipelined_m [data_width=25 n_iter=30 angle_guard=-1 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=3318, accuracy_bits=18.3, luts=2450, ffs=868, throughput_msps=114, max_abs_err=3.16e-06 (2^-18.27), power_index=3.99
- pipelined [data_width=26 n_iter=21 angle_guard=-1 frac_guard=0 rounding=round] luts_plus_ffs=3534, accuracy_bits=19.2, luts=1754, ffs=1780, throughput_msps=257, max_abs_err=1.66e-06 (2^-19.20), power_index=4.25
- pipelined_m [data_width=24 n_iter=30 angle_guard=1 frac_guard=4 rounding=trunc m=2] luts_plus_ffs=4036, accuracy_bits=19.7, luts=2664, ffs=1372, throughput_msps=153, max_abs_err=1.21e-06 (2^-19.66), power_index=4.86
Front coverage: luts_plus_ffs 1763..4036 (HV reference 4000); accuracy_bits 14.1..19.7 (HV reference 12); data_width on the front 19..26 (registry 8..28).

Per family:
- pipelined: 33 evals, 18 feasible; max throughput seen 292 MSPS; best accuracy 19.20 bits; best feasible luts_plus_ffs=2398; feasible ranges: data_width 21..26, n_iter 16..30, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 27 evals, 18 feasible; max throughput seen 164 MSPS; best accuracy 19.66 bits; best feasible luts_plus_ffs=1763; feasible ranges: data_width 19..25, n_iter 17..30, angle_guard -2..1, frac_guard 0..4, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (27 evals): data_width=18..28, n_iter=15..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)
- `pipelined` (13 evals): data_width=23..28, n_iter=17..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 70 feasible; hypervolume 1.538e+04 (+24.1%).

**No LLM call** (code's front-mapping round): The exploration has successfully mapped the feasible Pareto front for the `pipelined` and `pipelined_m` families, which are the only architectures capable of meeting the strict system constraint `sys_p99_batch_us <= 0.44` (iterative/unrolled_k would fail due to low throughput/latency). The current front covers a wide range of the objective space: `luts_plus_ffs` from 1763 to 4036 (spanning the HV reference of 4000) and `accuracy_bits` from 14.1 to 19.7 (well above the HV reference of 12). The best design (`pipelined_m` with `data_width=19`, `n_iter=17`, `m=2`) achieves a minimal area of 1763 LUTs+FFs while satisfying all constraints (throughput 164 MSPS >= 32, error 5.59e-05 <= 2^-12, and system latency well within bounds). Since this is the final round and the front is well-distributed across the trade-off curve, further exploration would yield diminishing returns. The selection rule (min `luts_plus_ffs`) will pick the 1763 design, which is robustly feasible.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.538e+04 (gain this round: +24.1%).
Feasible designs: 70 of 100 evaluations (62 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 292
- max_abs_err <= 0.000244141: 18% violate; best seen 8.28e-08 (2^-23.53)
- sys_p99_batch_us <= 0.44: 14% violate; best seen 0.132

Pareto front (feasible, 14 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=18 angle_guard=-2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1449, accuracy_bits=12.4, luts=1098, ffs=351, throughput_msps=93.6, max_abs_err=0.00019 (2^-12.36), power_index=1.74
- pipelined_m [data_width=20 n_iter=18 angle_guard=-2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1520, accuracy_bits=13.4, luts=1152, ffs=368, throughput_msps=93.6, max_abs_err=9.3e-05 (2^-13.39), power_index=1.83
- pipelined_m [data_width=19 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=1763, accuracy_bits=14.1, luts=1118, ffs=645, throughput_msps=164, max_abs_err=5.59e-05 (2^-14.13), power_index=2.12
- pipelined_m [data_width=24 n_iter=18 angle_guard=-2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1881, accuracy_bits=16.3, luts=1367, ffs=515, throughput_msps=114, max_abs_err=1.21e-05 (2^-16.33), power_index=2.26
- pipelined_m [data_width=28 n_iter=19 angle_guard=3 frac_guard=3 rounding=round m=3] luts_plus_ffs=2701, accuracy_bits=18, luts=1942, ffs=759, throughput_msps=106, max_abs_err=3.83e-06 (2^-18.00), power_index=3.25
- pipelined_m [data_width=28 n_iter=21 angle_guard=-2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=2708, accuracy_bits=19.4, luts=1986, ffs=721, throughput_msps=106, max_abs_err=1.41e-06 (2^-19.44), power_index=3.26
- pipelined_m [data_width=28 n_iter=26 angle_guard=-2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3395, accuracy_bits=20.8, luts=2482, ffs=913, throughput_msps=106, max_abs_err=5.65e-07 (2^-20.76), power_index=4.09
- pipelined [data_width=24 n_iter=23 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=4105, accuracy_bits=20.9, luts=2073, ffs=2032, throughput_msps=249, max_abs_err=5.25e-07 (2^-20.86), power_index=4.94
- pipelined [data_width=28 n_iter=26 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=4974, accuracy_bits=23.1, luts=2482, ffs=2492, throughput_msps=242, max_abs_err=1.1e-07 (2^-23.12), power_index=5.99
- pipelined [data_width=28 n_iter=27 angle_guard=1 frac_guard=3 rounding=trunc] luts_plus_ffs=5320, accuracy_bits=23.5, luts=2663, ffs=2658, throughput_msps=242, max_abs_err=8.28e-08 (2^-23.53), power_index=6.4
Front coverage: luts_plus_ffs 1449..5320 (HV reference 4000); accuracy_bits 12.4..23.5 (HV reference 12); data_width on the front 19..28 (registry 8..28).

Per family:
- pipelined: 46 evals, 31 feasible; max throughput seen 292 MSPS; best accuracy 23.53 bits; best feasible luts_plus_ffs=2398; feasible ranges: data_width 21..28, n_iter 16..30, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 54 evals, 39 feasible; max throughput seen 164 MSPS; best accuracy 20.76 bits; best feasible luts_plus_ffs=1449; feasible ranges: data_width 19..28, n_iter 16..30, angle_guard -2..3, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5280 in, 1550 out
- provider-reported cost: $0.0028
- full prompts and replies: `llm_trace.jsonl`

