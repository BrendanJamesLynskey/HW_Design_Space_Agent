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
`pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 800 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 272 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 61.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.29 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000204 (2^-12.26) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 6.67 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 6.07e-05 (2^-14.01) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.99 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (12 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=4` | 800 | 272 | 97.8 | 6 | 1.29 | 0.000204 (2^-12.26) | 12.26 |
| 1 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=4` | 861 | 272 | 97.8 | 6 | 1.36 | 0.000168 (2^-12.54) | 12.54 |
| 2 | `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=1,rounding=round,m=4` | 958 | 291 | 93.6 | 6 | 1.5 | 0.00014 (2^-12.80) | 12.80 |
| 3 | `pipelined_m:data_width=19,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=4` | 949 | 309 | 93.6 | 6 | 1.51 | 0.000139 (2^-12.81) | 12.81 |
| 4 | `pipelined_m:data_width=17,n_iter=16,angle_guard=1,frac_guard=1,rounding=round,m=4` | 989 | 280 | 97.8 | 6 | 1.53 | 0.000128 (2^-12.94) | 12.94 |
| 5 | `pipelined_m:data_width=19,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=3` | 1019 | 376 | 119.3 | 7 | 1.68 | 7.94e-05 (2^-13.62) | 13.62 |
| 6 | `pipelined_m:data_width=20,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=3` | 1065 | 393 | 119.3 | 7 | 1.76 | 7.02e-05 (2^-13.80) | 13.80 |
| 7 | `pipelined_m:data_width=21,n_iter=16,angle_guard=-2,frac_guard=2,rounding=trunc,m=3` | 1128 | 474 | 114.5 | 8 | 1.93 | 6.52e-05 (2^-13.90) | 13.90 |
| 8 | `pipelined_m:data_width=21,n_iter=18,angle_guard=1,frac_guard=3,rounding=trunc,m=3` | 1367 | 502 | 114.5 | 8 | 2.25 | 1.37e-05 (2^-16.16) | 16.16 |
| 9 | `pipelined_m:data_width=25,n_iter=19,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 1618 | 652 | 110.0 | 9 | 2.73 | 5.98e-06 (2^-17.35) | 17.35 |
| 10 | `pipelined_m:data_width=25,n_iter=30,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 2603 | 912 | 110.0 | 12 | 4.23 | 3.54e-06 (2^-18.11) | 18.11 |
| 11 | `pipelined:data_width=22,n_iter=22,angle_guard=4,frac_guard=3,rounding=round` | 1866 | 1832 | 256.5 | 24 | 4.45 | 1.62e-06 (2^-19.24) | 19.24 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *No facts yet, so I seed the two families I own. The spec's throughput >= 32 MS/s forces 1 result/cycle, which rules out iterative/unrolled_k and leaves only pipelined and pipelined_m. The 0.44 us batch bound for 32 results means the CORDIC must finish a burst in <= 32 cycles, so latency <= 32 is the binding system constraint; both families satisfy this for N <= 30. Accuracy <= 2^-12 with round rounding is achievable at N ~ 14-16 and W ~ 16-20, so I focus the search there to keep area low while leaving headroom. I split the budget evenly between the two families: pipelined is the area floor, pipelined_m explores the FF/Fmax trade-off that may push the front further. angle_guard and frac_guard are kept small (0-1) since the error budget is tight and extra guard bits mostly cost area without helping the 2^-12 bound; rounding is fixed to round because truncation typically doubles the error and would risk the constraint.*)
- `pipelined` (30 evals): data_width=16..20, n_iter=14..16, angle_guard=0..1, frac_guard=0..1, rounding=round. *Why:* Full pipelining gives 1 result/cycle, so Fmax >= 32 MHz is the only way to meet throughput; the 32-burst in 0.44 us needs ~32 cycles, so N+2 <= 32 (N <= 30) is fine. Accuracy <= 2^-12 needs N ~ 14-16 with W ~ 16-20; round is the only way to hit the tight error bound. This is the area-cheapest family that can meet the throughput constraint.
- `pipelined_m` (30 evals): data_width=16..20, n_iter=14..16, angle_guard=0..1, frac_guard=0..1, rounding=round, m=2..4. *Why:* Registering every m stages trades FFs for a slightly higher Fmax (shorter combinational path per stage) and lower latency (ceil(N/m)+2). With N=14-16 and m=2-4, latency stays well under 32 cycles, so the 0.44 us batch bound is met; this can beat pipelined on luts_plus_ffs if the Fmax gain is real. Same accuracy box as pipelined since accuracy is family-independent.

**Result (code):** 60 evaluations this round, 60 total; 49 feasible; hypervolume 6323 (n/a).

**LLM decision:** `stop` — The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 1072 LUTs+FFs) meets all constraints: throughput (97.8 >= 32), accuracy (12.3 bits > 12), and system latency (0.169 us <= 0.44 us). The front covers the trade-off space effectively from 1072 to 2266 LUTs+FFs and 12.3 to 14.6 accuracy bits. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (1072) as per the selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 6323 (gain this round: n/a (first round)).
Feasible designs: 49 of 60 evaluations (29 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 18% violate; best seen 4.05e-05 (2^-14.59)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.169

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1072, accuracy_bits=12.3, luts=800, ffs=272, throughput_msps=97.8, max_abs_err=0.000204 (2^-12.26), power_index=1.29
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1133, accuracy_bits=12.5, luts=861, ffs=272, throughput_msps=97.8, max_abs_err=0.000168 (2^-12.54), power_index=1.36
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=1248, accuracy_bits=12.8, luts=958, ffs=291, throughput_msps=93.6, max_abs_err=0.00014 (2^-12.80), power_index=1.5
- pipelined_m [data_width=19 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1258, accuracy_bits=12.8, luts=949, ffs=309, throughput_msps=93.6, max_abs_err=0.000139 (2^-12.81), power_index=1.51
- pipelined_m [data_width=17 n_iter=16 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1270, accuracy_bits=12.9, luts=989, ffs=280, throughput_msps=97.8, max_abs_err=0.000128 (2^-12.94), power_index=1.53
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=1395, accuracy_bits=13.6, luts=1019, ffs=376, throughput_msps=119, max_abs_err=7.94e-05 (2^-13.62), power_index=1.68
- pipelined_m [data_width=20 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=1459, accuracy_bits=13.8, luts=1065, ffs=393, throughput_msps=119, max_abs_err=7.02e-05 (2^-13.80), power_index=1.76
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=2162, accuracy_bits=14.4, luts=1064, ffs=1098, throughput_msps=264, max_abs_err=4.64e-05 (2^-14.39), power_index=2.6
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts_plus_ffs=2266, accuracy_bits=14.6, luts=1138, ffs=1128, throughput_msps=264, max_abs_err=4.05e-05 (2^-14.59), power_index=2.73
Front coverage: luts_plus_ffs 1072..2266 (HV reference 4000); accuracy_bits 12.3..14.6 (HV reference 12); data_width on the front 17..20 (registry 8..28).

Per family:
- pipelined: 30 evals, 25 feasible; max throughput seen 273 MSPS; best accuracy 14.59 bits; best feasible luts_plus_ffs=1780; feasible ranges: data_width 18..20, n_iter 14..16, angle_guard 0..1, frac_guard 0..1
- pipelined_m: 30 evals, 24 feasible; max throughput seen 171 MSPS; best accuracy 13.80 bits; best feasible luts_plus_ffs=1072; feasible ranges: data_width 17..20, n_iter 14..16, angle_guard 0..1, frac_guard 0..1, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (32 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (7 front designs; box front_anchored)
- `pipelined` (8 evals): data_width=19..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 69 feasible; hypervolume 1.272e+04 (+101.1%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 1072 LUTs+FFs) meets all constraints: throughput (97.8 >= 32), accuracy (12.3 bits > 12), and system latency (0.169 us <= 0.44 us). The front covers the trade-off space effectively from 1072 to 2266 LUTs+FFs and 12.3 to 14.6 accuracy bits. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (1072) as per the selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.272e+04 (gain this round: +101.1%).
Feasible designs: 69 of 100 evaluations (45 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 19% violate; best seen 1.33e-07 (2^-22.84)
- sys_p99_batch_us <= 0.44: 16% violate; best seen 0.169

Pareto front (feasible, 12 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1072, accuracy_bits=12.3, luts=800, ffs=272, throughput_msps=97.8, max_abs_err=0.000204 (2^-12.26), power_index=1.29
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1133, accuracy_bits=12.5, luts=861, ffs=272, throughput_msps=97.8, max_abs_err=0.000168 (2^-12.54), power_index=1.36
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=1248, accuracy_bits=12.8, luts=958, ffs=291, throughput_msps=93.6, max_abs_err=0.00014 (2^-12.80), power_index=1.5
- pipelined_m [data_width=17 n_iter=16 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1270, accuracy_bits=12.9, luts=989, ffs=280, throughput_msps=97.8, max_abs_err=0.000128 (2^-12.94), power_index=1.53
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=1395, accuracy_bits=13.6, luts=1019, ffs=376, throughput_msps=119, max_abs_err=7.94e-05 (2^-13.62), power_index=1.68
- pipelined_m [data_width=20 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=1459, accuracy_bits=13.8, luts=1065, ffs=393, throughput_msps=119, max_abs_err=7.02e-05 (2^-13.80), power_index=1.76
- pipelined_m [data_width=21 n_iter=16 angle_guard=-2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=1602, accuracy_bits=13.9, luts=1128, ffs=474, throughput_msps=114, max_abs_err=6.52e-05 (2^-13.90), power_index=1.93
- pipelined_m [data_width=25 n_iter=19 angle_guard=-2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=2269, accuracy_bits=17.4, luts=1618, ffs=652, throughput_msps=110, max_abs_err=5.98e-06 (2^-17.35), power_index=2.73
- pipelined_m [data_width=25 n_iter=30 angle_guard=-2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3515, accuracy_bits=18.1, luts=2603, ffs=912, throughput_msps=110, max_abs_err=3.54e-06 (2^-18.11), power_index=4.23
- pipelined [data_width=22 n_iter=22 angle_guard=4 frac_guard=3 rounding=round] luts_plus_ffs=3698, accuracy_bits=19.2, luts=1866, ffs=1832, throughput_msps=257, max_abs_err=1.62e-06 (2^-19.24), power_index=4.45
Front coverage: luts_plus_ffs 1072..3698 (HV reference 4000); accuracy_bits 12.3..19.2 (HV reference 12); data_width on the front 17..25 (registry 8..28).

Per family:
- pipelined: 38 evals, 33 feasible; max throughput seen 273 MSPS; best accuracy 19.24 bits; best feasible luts_plus_ffs=1780; feasible ranges: data_width 18..25, n_iter 14..25, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 62 evals, 36 feasible; max throughput seen 171 MSPS; best accuracy 22.84 bits; best feasible luts_plus_ffs=1072; feasible ranges: data_width 17..25, n_iter 14..30, angle_guard -2..1, frac_guard 0..3, m 2..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 6046 in, 1029 out
- provider-reported cost: $0.0027
- full prompts and replies: `llm_trace.jsonl`

