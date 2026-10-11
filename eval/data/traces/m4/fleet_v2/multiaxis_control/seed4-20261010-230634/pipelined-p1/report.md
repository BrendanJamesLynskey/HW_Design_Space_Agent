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
`pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=1,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 958 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 291 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00014 (2^-12.80) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 9.16 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 3.12e-05 (2^-14.97) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 2.05 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.8 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (14 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=1,rounding=round,m=4` | 958 | 291 | 93.6 | 6 | 1.5 | 0.00014 (2^-12.80) | 12.80 |
| 1 | `pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=1,rounding=round,m=2` | 1023 | 545 | 164.4 | 10 | 1.89 | 0.00012 (2^-13.03) | 13.03 |
| 2 | `pipelined_m:data_width=18,n_iter=18,angle_guard=0,frac_guard=1,rounding=round,m=2` | 1154 | 608 | 164.4 | 11 | 2.12 | 0.000104 (2^-13.22) | 13.22 |
| 3 | `pipelined_m:data_width=24,n_iter=17,angle_guard=-2,frac_guard=0,rounding=round,m=3` | 1287 | 515 | 114.5 | 8 | 2.17 | 1.98e-05 (2^-15.63) | 15.63 |
| 4 | `pipelined_m:data_width=19,n_iter=18,angle_guard=3,frac_guard=3,rounding=round,m=3` | 1335 | 476 | 119.3 | 8 | 2.18 | 1.78e-05 (2^-15.78) | 15.78 |
| 5 | `pipelined_m:data_width=25,n_iter=18,angle_guard=3,frac_guard=0,rounding=round,m=3` | 1510 | 565 | 110.0 | 8 | 2.5 | 7.97e-06 (2^-16.94) | 16.94 |
| 6 | `pipelined_m:data_width=28,n_iter=18,angle_guard=-2,frac_guard=3,rounding=round,m=3` | 1748 | 628 | 105.9 | 8 | 2.86 | 7.9e-06 (2^-16.95) | 16.95 |
| 7 | `pipelined_m:data_width=28,n_iter=18,angle_guard=3,frac_guard=3,rounding=round,m=3` | 1838 | 658 | 105.9 | 8 | 3 | 7.64e-06 (2^-17.00) | 17.00 |
| 8 | `pipelined_m:data_width=24,n_iter=25,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 2079 | 796 | 110.0 | 11 | 3.46 | 7.2e-06 (2^-17.08) | 17.08 |
| 9 | `pipelined_m:data_width=25,n_iter=27,angle_guard=-2,frac_guard=0,rounding=round,m=3` | 2170 | 777 | 114.5 | 11 | 3.55 | 3.54e-06 (2^-18.11) | 18.11 |
| 10 | `pipelined_m:data_width=28,n_iter=25,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 2383 | 913 | 105.9 | 11 | 3.97 | 5.4e-07 (2^-20.82) | 20.82 |
| 11 | `pipelined:data_width=27,n_iter=24,angle_guard=1,frac_guard=0,rounding=trunc` | 2138 | 2155 | 249.0 | 26 | 5.17 | 4.31e-07 (2^-21.14) | 21.14 |
| 12 | `pipelined:data_width=27,n_iter=24,angle_guard=4,frac_guard=0,rounding=round` | 2211 | 2228 | 242.0 | 26 | 5.34 | 2.65e-07 (2^-21.85) | 21.85 |
| 13 | `pipelined:data_width=28,n_iter=26,angle_guard=1,frac_guard=3,rounding=trunc` | 2561 | 2559 | 242.0 | 28 | 6.16 | 9.77e-08 (2^-23.29) | 23.29 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 results/us throughput and a 0.44 us p99 batch latency for 32 simultaneous requests. Only pipelined and pipelined_m produce 1 result/cycle, so they are the only viable families (iterative and unrolled_k would need Fmax >= 32*k MHz which is unrealistic). The throughput constraint (>=32 Msps) means Fmax must be >=32 MHz, which is easily achievable for CORDIC datapaths at these widths. The 0.44 us batch bound means the 32nd result must arrive within 0.44 us of the tick; with 1 result/cycle, the 32nd result arrives at cycle 32, so Fmax must be >= 32/0.44 = 72.7 MHz, which is still very achievable. Accuracy requires max_abs_err <= 2^-12 = 0.000244, which needs data_width >= 14 with sufficient n_iter. I focus data_width 14-18 to bracket the accuracy requirement and explore the area/accuracy trade-off. n_iter 12-18 covers the range where accuracy transitions from below to well above the 12-bit requirement. Guard bits are kept small (0-2) since the accuracy requirement is modest and large guards waste area. The two families are split evenly: pipelined for the baseline full-pipeline design, pipelined_m to find FF savings through partial pipelining. The hypervolume reference (4000 luts+ffs, 12 accuracy_bits) suggests the interesting region is around 1000-3000 luts+ffs and 12-15 accuracy bits, which these ranges should cover.*)
- `pipelined` (30 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Full pipelining is the only way to hit 32 results/us (1 result/cycle at Fmax>=32 MHz) while keeping latency low enough for the 0.44 us p99 batch bound. data_width 14-18 brackets the 12-bit accuracy requirement (14 is the tightest that can plausibly clear 2^-12 with N>=12, 18 gives margin for the accuracy_bits objective). n_iter 12-18 spans the accuracy/area trade-off. angle_guard 0-2 and frac_guard 0-2 cover the small guard-bit range that affects accuracy without large area cost. Both rounding modes included since rounding can buy ~0.5 accuracy bits at negligible area cost.
- `pipelined_m` (30 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* pipelined_m registers every m stages, trading some latency for fewer FFs than full pipelining. With m=2-8 and N=12-18, latency is ceil(N/m)+2 cycles, which at Fmax>=32 MHz stays well under 0.44 us for the 32-request batch. This family can reduce FF count significantly vs pipelined while maintaining 1 result/cycle throughput, making it a strong candidate for the min luts_plus_ffs objective. Same data_width/n_iter/guard ranges as pipelined for consistent accuracy exploration.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 60 evaluations this round, 60 total; 30 feasible; hypervolume 3874 (n/a).

**LLM decision:** `stop` — The exploration has successfully identified a feasible Pareto front that satisfies all constraints. The best design (pipelined_m, data_width=18, n_iter=15, m=4) achieves a luts_plus_ffs of 1248, which is significantly below the HV reference of 4000, and meets the accuracy requirement (12.8 bits > 12 bits) and throughput requirement (93.6 MSPS > 32 MSPS). The system constraint sys_p99_batch_us is also met (best seen 0.161 us <= 0.44 us). Since this is the final round and the front is well-defined with a clear winner for the selection rule (min luts_plus_ffs), stopping is the appropriate action.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 3874 (gain this round: n/a (first round)).
Feasible designs: 30 of 60 evaluations (22 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 38% violate; best seen 8.26e-05 (2^-13.56)
- sys_p99_batch_us <= 0.44: 18% violate; best seen 0.161

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=1248, accuracy_bits=12.8, luts=958, ffs=291, throughput_msps=93.6, max_abs_err=0.00014 (2^-12.80), power_index=1.5
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=round m=2] luts_plus_ffs=1568, accuracy_bits=13, luts=1023, ffs=545, throughput_msps=164, max_abs_err=0.00012 (2^-13.03), power_index=1.89
- pipelined_m [data_width=18 n_iter=18 angle_guard=0 frac_guard=1 rounding=round m=2] luts_plus_ffs=1762, accuracy_bits=13.2, luts=1154, ffs=608, throughput_msps=164, max_abs_err=0.000104 (2^-13.22), power_index=2.12
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=1969, accuracy_bits=13.4, luts=987, ffs=982, throughput_msps=264, max_abs_err=9.31e-05 (2^-13.39), power_index=2.37
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2025, accuracy_bits=13.6, luts=1017, ffs=1008, throughput_msps=264, max_abs_err=8.26e-05 (2^-13.56), power_index=2.44
Front coverage: luts_plus_ffs 1248..2025 (HV reference 4000); accuracy_bits 12.8..13.6 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- pipelined: 30 evals, 13 feasible; max throughput seen 282 MSPS; best accuracy 13.56 bits; best feasible luts_plus_ffs=1814; feasible ranges: data_width 17..18, n_iter 15..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 30 evals, 17 feasible; max throughput seen 171 MSPS; best accuracy 13.22 bits; best feasible luts_plus_ffs=1248; feasible ranges: data_width 17..18, n_iter 15..18, angle_guard 0..1, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (24 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (3 front designs; box front_anchored)
- `pipelined` (16 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 61 feasible; hypervolume 1.422e+04 (+267.1%).

**No LLM call** (code's front-mapping round): The exploration has successfully identified a feasible Pareto front that satisfies all constraints. The best design (pipelined_m, data_width=18, n_iter=15, m=4) achieves a luts_plus_ffs of 1248, which is significantly below the HV reference of 4000, and meets the accuracy requirement (12.8 bits > 12 bits) and throughput requirement (93.6 MSPS > 32 MSPS). The system constraint sys_p99_batch_us is also met (best seen 0.161 us <= 0.44 us). Since this is the final round and the front is well-defined with a clear winner for the selection rule (min luts_plus_ffs), stopping is the appropriate action.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.422e+04 (gain this round: +267.1%).
Feasible designs: 61 of 100 evaluations (51 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 26% violate; best seen 9.77e-08 (2^-23.29)
- sys_p99_batch_us <= 0.44: 17% violate; best seen 0.161

Pareto front (feasible, 14 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=1248, accuracy_bits=12.8, luts=958, ffs=291, throughput_msps=93.6, max_abs_err=0.00014 (2^-12.80), power_index=1.5
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=round m=2] luts_plus_ffs=1568, accuracy_bits=13, luts=1023, ffs=545, throughput_msps=164, max_abs_err=0.00012 (2^-13.03), power_index=1.89
- pipelined_m [data_width=24 n_iter=17 angle_guard=-2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1801, accuracy_bits=15.6, luts=1287, ffs=515, throughput_msps=114, max_abs_err=1.98e-05 (2^-15.63), power_index=2.17
- pipelined_m [data_width=19 n_iter=18 angle_guard=3 frac_guard=3 rounding=round m=3] luts_plus_ffs=1811, accuracy_bits=15.8, luts=1335, ffs=476, throughput_msps=119, max_abs_err=1.78e-05 (2^-15.78), power_index=2.18
- pipelined_m [data_width=28 n_iter=18 angle_guard=-2 frac_guard=3 rounding=round m=3] luts_plus_ffs=2376, accuracy_bits=16.9, luts=1748, ffs=628, throughput_msps=106, max_abs_err=7.9e-06 (2^-16.95), power_index=2.86
- pipelined_m [data_width=28 n_iter=18 angle_guard=3 frac_guard=3 rounding=round m=3] luts_plus_ffs=2496, accuracy_bits=17, luts=1838, ffs=658, throughput_msps=106, max_abs_err=7.64e-06 (2^-17.00), power_index=3
- pipelined_m [data_width=25 n_iter=27 angle_guard=-2 frac_guard=0 rounding=round m=3] luts_plus_ffs=2947, accuracy_bits=18.1, luts=2170, ffs=777, throughput_msps=114, max_abs_err=3.54e-06 (2^-18.11), power_index=3.55
- pipelined_m [data_width=28 n_iter=25 angle_guard=-2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3296, accuracy_bits=20.8, luts=2383, ffs=913, throughput_msps=106, max_abs_err=5.4e-07 (2^-20.82), power_index=3.97
- pipelined [data_width=27 n_iter=24 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=4438, accuracy_bits=21.8, luts=2211, ffs=2228, throughput_msps=242, max_abs_err=2.65e-07 (2^-21.85), power_index=5.34
- pipelined [data_width=28 n_iter=26 angle_guard=1 frac_guard=3 rounding=trunc] luts_plus_ffs=5119, accuracy_bits=23.3, luts=2561, ffs=2559, throughput_msps=242, max_abs_err=9.77e-08 (2^-23.29), power_index=6.16
Front coverage: luts_plus_ffs 1248..5119 (HV reference 4000); accuracy_bits 12.8..23.3 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- pipelined: 46 evals, 27 feasible; max throughput seen 282 MSPS; best accuracy 23.29 bits; best feasible luts_plus_ffs=1814; feasible ranges: data_width 17..28, n_iter 13..28, angle_guard -1..4, frac_guard 0..3
- pipelined_m: 54 evals, 34 feasible; max throughput seen 171 MSPS; best accuracy 20.82 bits; best feasible luts_plus_ffs=1248; feasible ranges: data_width 17..28, n_iter 14..27, angle_guard -2..3, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5161 in, 1207 out
- provider-reported cost: $0.0039
- full prompts and replies: `llm_trace.jsonl`

