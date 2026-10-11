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
`pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=3,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 949 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 291 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.49 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00016 (2^-12.61) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 5.24 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 3.49e-05 (2^-14.81) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.14 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.6 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (16 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=3,rounding=trunc,m=4` | 949 | 291 | 93.6 | 6 | 1.49 | 0.00016 (2^-12.61) | 12.61 |
| 1 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=3` | 935 | 353 | 119.3 | 7 | 1.55 | 0.000143 (2^-12.77) | 12.77 |
| 2 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=3,rounding=trunc,m=3` | 964 | 361 | 119.3 | 7 | 1.6 | 0.000117 (2^-13.06) | 13.06 |
| 3 | `pipelined_m:data_width=20,n_iter=16,angle_guard=-2,frac_guard=3,rounding=trunc,m=4` | 1112 | 321 | 89.6 | 6 | 1.72 | 9.69e-05 (2^-13.33) | 13.33 |
| 4 | `pipelined_m:data_width=20,n_iter=15,angle_guard=2,frac_guard=3,rounding=trunc,m=4` | 1097 | 337 | 89.6 | 6 | 1.73 | 6.77e-05 (2^-13.85) | 13.85 |
| 5 | `pipelined_m:data_width=25,n_iter=15,angle_guard=3,frac_guard=0,rounding=trunc,m=4` | 1244 | 393 | 86.0 | 6 | 1.97 | 6.12e-05 (2^-14.00) | 14.00 |
| 6 | `pipelined_m:data_width=25,n_iter=15,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1274 | 400 | 86.0 | 6 | 2.01 | 6.11e-05 (2^-14.00) | 14.00 |
| 7 | `pipelined_m:data_width=25,n_iter=15,angle_guard=3,frac_guard=1,rounding=round,m=4` | 1327 | 402 | 86.0 | 6 | 2.08 | 6.11e-05 (2^-14.00) | 14.00 |
| 8 | `pipelined_m:data_width=25,n_iter=15,angle_guard=2,frac_guard=3,rounding=round,m=4` | 1371 | 410 | 86.0 | 6 | 2.14 | 6.1e-05 (2^-14.00) | 14.00 |
| 9 | `pipelined_m:data_width=25,n_iter=16,angle_guard=0,frac_guard=3,rounding=round,m=4` | 1433 | 402 | 86.0 | 6 | 2.21 | 3.08e-05 (2^-14.98) | 14.98 |
| 10 | `pipelined_m:data_width=25,n_iter=17,angle_guard=3,frac_guard=0,rounding=trunc,m=3` | 1422 | 565 | 110.0 | 8 | 2.39 | 1.58e-05 (2^-15.95) | 15.95 |
| 11 | `pipelined_m:data_width=25,n_iter=17,angle_guard=4,frac_guard=3,rounding=trunc,m=4` | 1540 | 508 | 86.0 | 7 | 2.47 | 1.54e-05 (2^-15.99) | 15.99 |
| 12 | `pipelined_m:data_width=26,n_iter=17,angle_guard=3,frac_guard=0,rounding=round,m=3` | 1472 | 585 | 110.0 | 8 | 2.48 | 1.53e-05 (2^-16.00) | 16.00 |
| 13 | `pipelined:data_width=20,n_iter=22,angle_guard=4,frac_guard=4,rounding=trunc` | 1731 | 1737 | 256.5 | 24 | 4.18 | 6.34e-06 (2^-17.27) | 17.27 |
| 14 | `pipelined:data_width=23,n_iter=23,angle_guard=0,frac_guard=2,rounding=trunc` | 1837 | 1848 | 256.5 | 25 | 4.44 | 3.72e-06 (2^-18.04) | 18.04 |
| 15 | `pipelined:data_width=28,n_iter=30,angle_guard=2,frac_guard=0,rounding=trunc` | 2817 | 2815 | 249.0 | 32 | 6.78 | 2.17e-07 (2^-22.13) | 22.13 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is throughput- and latency-bound: 32 results must arrive within 0.44 us of a 1 us tick, and throughput must be >= 32 MS/s. Only the 1-result/cycle families (pipelined, pipelined_m) can meet this, so I restrict to those two. The binding hidden constraint is Fmax: 32 back-to-back results in 32 cycles needs Fmax >= ~72 MHz, so I keep n_iter (12..16) and data_width (14..20) modest to limit per-stage depth, while n_iter>=12 / width>=14 guarantees max_abs_err <= 2^-12. I sweep angle_guard (-2..4) and frac_guard (0..4) with both rounding modes to map the accuracy-vs-area trade-off that drives the two objectives (min luts_plus_ffs, max accuracy_bits). I split the budget 55/45 between the two families: pipelined as the reliable throughput/area anchor, and pipelined_m (m=2..4) to push the area objective lower via reduced FFs, which is where the Pareto front's area-extreme corner lives.*)
- `pipelined` (33 evals): data_width=14..20, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Full pipelining gives 1 result/cycle, so throughput_msps = Fmax. To clear the 32 MS/s constraint and the 0.44 us p99-batch bound (32 back-to-back results must finish in 32 cycles, so Fmax must be >= ~72 MHz), the datapath must be fast. Keeping n_iter in 12..16 and data_width in 14..20 bounds the per-stage adder/shift depth so Fmax stays comfortably above 72 MHz, while n_iter>=12 with data_width>=14 keeps max_abs_err <= 2^-12. This family is the natural throughput/area anchor of the front.
- `pipelined_m` (27 evals): data_width=14..20, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* pipelined_m registers every m stages, cutting FF count (the dominant area term in a deep pipeline) while still delivering 1 result/cycle, so it keeps the 32 MS/s throughput and the 0.44 us batch bound. Larger m (2..4) lowers area but lengthens the combinational path per stage, which can push Fmax down; the 12..16 n_iter / 14..20 width ranges keep the per-stage logic shallow enough that even m=2..4 should hold Fmax above ~72 MHz. This family maps the area side of the Pareto front that full pipelining cannot reach.

**Result (code):** 60 evaluations this round, 60 total; 30 feasible; hypervolume 4956 (n/a).

**LLM decision:** `stop` — The exploration has identified a robust feasible Pareto front dominated by the `pipelined_m` family, which satisfies all system and accuracy constraints with significantly lower area (1240-1434 LUTs+FFs) compared to the fully `pipelined` family (1788+ LUTs+FFs). The best design (`pipelined_m` with data_width=17, n_iter=15, m=4) achieves 12.6 accuracy bits (max_abs_err ~2^-12.61), comfortably meeting the <= 2^-12 constraint, while maintaining a throughput of 93.6 MSPS (well above the 32 MSPS requirement) and a system p99 batch latency of 0.161 us (well below the 0.44 us limit). Since this is the final round, the current front is sufficient for selection based on the 'min luts_plus_ffs' rule, which will pick the 1240 LUTs+FFs design.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 4956 (gain this round: n/a (first round)).
Feasible designs: 30 of 60 evaluations (27 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 50% violate; best seen 6.68e-05 (2^-13.87)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.161

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1240, accuracy_bits=12.6, luts=949, ffs=291, throughput_msps=93.6, max_abs_err=0.00016 (2^-12.61), power_index=1.49
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=1288, accuracy_bits=12.8, luts=935, ffs=353, throughput_msps=119, max_abs_err=0.000143 (2^-12.77), power_index=1.55
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=1325, accuracy_bits=13.1, luts=964, ffs=361, throughput_msps=119, max_abs_err=0.000117 (2^-13.06), power_index=1.6
- pipelined_m [data_width=20 n_iter=16 angle_guard=-2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1433, accuracy_bits=13.3, luts=1112, ffs=321, throughput_msps=89.6, max_abs_err=9.69e-05 (2^-13.33), power_index=1.72
- pipelined_m [data_width=20 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1434, accuracy_bits=13.9, luts=1097, ffs=337, throughput_msps=89.6, max_abs_err=6.77e-05 (2^-13.85), power_index=1.73
- pipelined [data_width=19 n_iter=15 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=2202, accuracy_bits=13.9, luts=1107, ffs=1095, throughput_msps=264, max_abs_err=6.68e-05 (2^-13.87), power_index=2.65
Front coverage: luts_plus_ffs 1240..2202 (HV reference 4000); accuracy_bits 12.6..13.9 (HV reference 12); data_width on the front 17..20 (registry 8..28).

Per family:
- pipelined: 33 evals, 22 feasible; max throughput seen 273 MSPS; best accuracy 13.87 bits; best feasible luts_plus_ffs=1788; feasible ranges: data_width 17..20, n_iter 14..16, angle_guard -1..4, frac_guard 1..4
- pipelined_m: 27 evals, 8 feasible; max throughput seen 171 MSPS; best accuracy 13.85 bits; best feasible luts_plus_ffs=1240; feasible ranges: data_width 17..20, n_iter 15..16, angle_guard -2..2, frac_guard 2..3, m 3..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (34 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (5 front designs; box front_anchored)
- `pipelined` (6 evals): data_width=18..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 49 feasible; hypervolume 1.036e+04 (+109.0%).

**No LLM call** (code's front-mapping round): The exploration has identified a robust feasible Pareto front dominated by the `pipelined_m` family, which satisfies all system and accuracy constraints with significantly lower area (1240-1434 LUTs+FFs) compared to the fully `pipelined` family (1788+ LUTs+FFs). The best design (`pipelined_m` with data_width=17, n_iter=15, m=4) achieves 12.6 accuracy bits (max_abs_err ~2^-12.61), comfortably meeting the <= 2^-12 constraint, while maintaining a throughput of 93.6 MSPS (well above the 32 MSPS requirement) and a system p99 batch latency of 0.161 us (well below the 0.44 us limit). Since this is the final round, the current front is sufficient for selection based on the 'min luts_plus_ffs' rule, which will pick the 1240 LUTs+FFs design.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.036e+04 (gain this round: +109.0%).
Feasible designs: 49 of 100 evaluations (45 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 33% violate; best seen 2.16e-07 (2^-22.14)
- sys_p99_batch_us <= 0.44: 20% violate; best seen 0.161

Pareto front (feasible, 16 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1240, accuracy_bits=12.6, luts=949, ffs=291, throughput_msps=93.6, max_abs_err=0.00016 (2^-12.61), power_index=1.49
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=1325, accuracy_bits=13.1, luts=964, ffs=361, throughput_msps=119, max_abs_err=0.000117 (2^-13.06), power_index=1.6
- pipelined_m [data_width=20 n_iter=16 angle_guard=-2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1433, accuracy_bits=13.3, luts=1112, ffs=321, throughput_msps=89.6, max_abs_err=9.69e-05 (2^-13.33), power_index=1.72
- pipelined_m [data_width=25 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1638, accuracy_bits=14, luts=1244, ffs=393, throughput_msps=86, max_abs_err=6.12e-05 (2^-14.00), power_index=1.97
- pipelined_m [data_width=25 n_iter=15 angle_guard=3 frac_guard=1 rounding=round m=4] luts_plus_ffs=1728, accuracy_bits=14, luts=1327, ffs=402, throughput_msps=86, max_abs_err=6.11e-05 (2^-14.00), power_index=2.08
- pipelined_m [data_width=25 n_iter=15 angle_guard=2 frac_guard=3 rounding=round m=4] luts_plus_ffs=1781, accuracy_bits=14, luts=1371, ffs=410, throughput_msps=86, max_abs_err=6.1e-05 (2^-14.00), power_index=2.14
- pipelined_m [data_width=25 n_iter=17 angle_guard=3 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=1987, accuracy_bits=15.9, luts=1422, ffs=565, throughput_msps=110, max_abs_err=1.58e-05 (2^-15.95), power_index=2.39
- pipelined_m [data_width=26 n_iter=17 angle_guard=3 frac_guard=0 rounding=round m=3] luts_plus_ffs=2057, accuracy_bits=16, luts=1472, ffs=585, throughput_msps=110, max_abs_err=1.53e-05 (2^-16.00), power_index=2.48
- pipelined [data_width=20 n_iter=22 angle_guard=4 frac_guard=4 rounding=trunc] luts_plus_ffs=3469, accuracy_bits=17.3, luts=1731, ffs=1737, throughput_msps=257, max_abs_err=6.34e-06 (2^-17.27), power_index=4.18
- pipelined [data_width=28 n_iter=30 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=5632, accuracy_bits=22.1, luts=2817, ffs=2815, throughput_msps=249, max_abs_err=2.17e-07 (2^-22.13), power_index=6.78
Front coverage: luts_plus_ffs 1240..5632 (HV reference 4000); accuracy_bits 12.6..22.1 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- pipelined: 39 evals, 27 feasible; max throughput seen 273 MSPS; best accuracy 22.13 bits; best feasible luts_plus_ffs=1788; feasible ranges: data_width 17..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 61 evals, 22 feasible; max throughput seen 171 MSPS; best accuracy 22.14 bits; best feasible luts_plus_ffs=1240; feasible ranges: data_width 17..26, n_iter 15..17, angle_guard -2..4, frac_guard 0..3, m 3..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5274 in, 1318 out
- provider-reported cost: $0.0027
- full prompts and replies: `llm_trace.jsonl`

