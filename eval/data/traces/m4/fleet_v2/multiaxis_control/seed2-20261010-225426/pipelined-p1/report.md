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
`pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 969 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 287 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.51 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000108 (2^-13.18) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 7.07 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.3e-05 (2^-15.41) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.51 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.2 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=4` | 969 | 287 | 93.6 | 6 | 1.51 | 0.000108 (2^-13.18) | 13.18 |
| 1 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1039 | 295 | 93.6 | 6 | 1.61 | 8.41e-05 (2^-13.54) | 13.54 |
| 2 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=1,rounding=round,m=3` | 1055 | 430 | 119.3 | 8 | 1.79 | 6.45e-05 (2^-13.92) | 13.92 |
| 3 | `pipelined_m:data_width=18,n_iter=17,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1122 | 364 | 93.6 | 7 | 1.79 | 5.64e-05 (2^-14.11) | 14.11 |
| 4 | `pipelined_m:data_width=19,n_iter=21,angle_guard=1,frac_guard=2,rounding=trunc,m=3` | 1438 | 522 | 119.3 | 9 | 2.36 | 3.5e-05 (2^-14.80) | 14.80 |
| 5 | `pipelined_m:data_width=19,n_iter=22,angle_guard=1,frac_guard=3,rounding=round,m=3` | 1594 | 607 | 119.3 | 10 | 2.65 | 2.63e-05 (2^-15.21) | 15.21 |
| 6 | `pipelined_m:data_width=27,n_iter=19,angle_guard=0,frac_guard=1,rounding=round,m=3` | 1750 | 690 | 110.0 | 9 | 2.94 | 3.91e-06 (2^-17.97) | 17.97 |
| 7 | `pipelined_m:data_width=27,n_iter=22,angle_guard=3,frac_guard=0,rounding=round,m=3` | 1997 | 789 | 110.0 | 10 | 3.35 | 6.06e-07 (2^-20.65) | 20.65 |
| 8 | `pipelined_m:data_width=27,n_iter=22,angle_guard=2,frac_guard=1,rounding=round,m=3` | 2076 | 797 | 110.0 | 10 | 3.46 | 5.58e-07 (2^-20.77) | 20.77 |
| 9 | `pipelined_m:data_width=27,n_iter=23,angle_guard=0,frac_guard=1,rounding=round,m=3` | 2125 | 781 | 110.0 | 10 | 3.5 | 4.51e-07 (2^-21.08) | 21.08 |
| 10 | `pipelined_m:data_width=27,n_iter=23,angle_guard=3,frac_guard=1,rounding=round,m=3` | 2195 | 805 | 110.0 | 10 | 3.61 | 3.1e-07 (2^-21.62) | 21.62 |
| 11 | `pipelined_m:data_width=27,n_iter=28,angle_guard=1,frac_guard=2,rounding=trunc,m=3` | 2623 | 989 | 110.0 | 12 | 4.35 | 1.69e-07 (2^-22.50) | 22.50 |
| 12 | `pipelined_m:data_width=27,n_iter=29,angle_guard=3,frac_guard=1,rounding=round,m=3` | 2777 | 993 | 110.0 | 12 | 4.54 | 1.16e-07 (2^-23.04) | 23.04 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 results/us throughput and a 0.44us p99 batch latency, which rules out iterative and unrolled_k families (they produce <1 result/cycle). Both pipelined and pipelined_m achieve 1 result/cycle, so they are the only viable families. pipelined has the lowest latency (N+2) but highest FF count; pipelined_m trades some latency for lower FF count. Since the objective is min luts_plus_ffs, I allocate 60% to pipelined (to map the full latency/area trade-off) and 40% to pipelined_m (to find area-optimized designs). The data_width and n_iter ranges are chosen to bracket the 2^-12 accuracy constraint: W=14-18 and N=12-18 should cover the feasible accuracy region. angle_guard and frac_guard are kept small (0-2) to minimize area while still allowing sufficient precision. Rounding is fixed to 'round' for optimal accuracy per bit.*)
- `pipelined` (36 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* Full pipelining gives 1 result/cycle, so it is the only family that can meet the 32 req/us throughput and the 0.44us p99 batch constraint without queueing. Focusing on W=14-18 and N=12-18 brackets the 2^-12 accuracy requirement while keeping area low; rounding is fixed to 'round' for best accuracy per bit.
- `pipelined_m` (24 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* pipelined_m with m=2-4 reduces FF count versus full pipelining while still achieving 1 result/cycle throughput. This trades a small latency increase (ceil(N/m)+2) for significant area savings, which is critical for the min luts_plus_ffs objective. The latency increase is small enough to still meet the 0.44us batch constraint at reasonable Fmax.

**Result (code):** 60 evaluations this round, 60 total; 40 feasible; hypervolume 5640 (n/a).

**LLM decision:** `stop` — The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 1256 LUTs+FFs) meets all constraints: throughput 93.6 MSPS >= 32, max_abs_err 1.08e-4 <= 2.44e-4, and sys_p99_batch_us 0.165 <= 0.44. The front spans a reasonable range of accuracy (13.2 to 14.1 bits) and area (1256 to 1486), covering the trade-off space effectively. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (1256) as per the selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 5640 (gain this round: n/a (first round)).
Feasible designs: 40 of 60 evaluations (31 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 33% violate; best seen 5.64e-05 (2^-14.11)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.165

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=1.51
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1334, accuracy_bits=13.5, luts=1039, ffs=295, throughput_msps=93.6, max_abs_err=8.41e-05 (2^-13.54), power_index=1.61
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=1485, accuracy_bits=13.9, luts=1055, ffs=430, throughput_msps=119, max_abs_err=6.45e-05 (2^-13.92), power_index=1.79
- pipelined_m [data_width=18 n_iter=17 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1486, accuracy_bits=14.1, luts=1122, ffs=364, throughput_msps=93.6, max_abs_err=5.64e-05 (2^-14.11), power_index=1.79
Front coverage: luts_plus_ffs 1256..1486 (HV reference 4000); accuracy_bits 13.2..14.1 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- pipelined: 36 evals, 21 feasible; max throughput seen 273 MSPS; best accuracy 14.04 bits; best feasible luts_plus_ffs=1633; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 1..2, frac_guard 0..2
- pipelined_m: 24 evals, 19 feasible; max throughput seen 171 MSPS; best accuracy 14.11 bits; best feasible luts_plus_ffs=1256; feasible ranges: data_width 16..18, n_iter 15..18, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=17..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 66 feasible; hypervolume 1.682e+04 (+198.2%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 1256 LUTs+FFs) meets all constraints: throughput 93.6 MSPS >= 32, max_abs_err 1.08e-4 <= 2.44e-4, and sys_p99_batch_us 0.165 <= 0.44. The front spans a reasonable range of accuracy (13.2 to 14.1 bits) and area (1256 to 1486), covering the trade-off space effectively. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (1256) as per the selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.682e+04 (gain this round: +198.2%).
Feasible designs: 66 of 100 evaluations (55 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 21% violate; best seen 1.16e-07 (2^-23.04)
- sys_p99_batch_us <= 0.44: 14% violate; best seen 0.165

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=1.51
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1334, accuracy_bits=13.5, luts=1039, ffs=295, throughput_msps=93.6, max_abs_err=8.41e-05 (2^-13.54), power_index=1.61
- pipelined_m [data_width=18 n_iter=17 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1486, accuracy_bits=14.1, luts=1122, ffs=364, throughput_msps=93.6, max_abs_err=5.64e-05 (2^-14.11), power_index=1.79
- pipelined_m [data_width=19 n_iter=21 angle_guard=1 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=1960, accuracy_bits=14.8, luts=1438, ffs=522, throughput_msps=119, max_abs_err=3.5e-05 (2^-14.80), power_index=2.36
- pipelined_m [data_width=19 n_iter=22 angle_guard=1 frac_guard=3 rounding=round m=3] luts_plus_ffs=2202, accuracy_bits=15.2, luts=1594, ffs=607, throughput_msps=119, max_abs_err=2.63e-05 (2^-15.21), power_index=2.65
- pipelined_m [data_width=27 n_iter=22 angle_guard=3 frac_guard=0 rounding=round m=3] luts_plus_ffs=2786, accuracy_bits=20.7, luts=1997, ffs=789, throughput_msps=110, max_abs_err=6.06e-07 (2^-20.65), power_index=3.35
- pipelined_m [data_width=27 n_iter=22 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=2873, accuracy_bits=20.8, luts=2076, ffs=797, throughput_msps=110, max_abs_err=5.58e-07 (2^-20.77), power_index=3.46
- pipelined_m [data_width=27 n_iter=23 angle_guard=0 frac_guard=1 rounding=round m=3] luts_plus_ffs=2906, accuracy_bits=21.1, luts=2125, ffs=781, throughput_msps=110, max_abs_err=4.51e-07 (2^-21.08), power_index=3.5
- pipelined_m [data_width=27 n_iter=28 angle_guard=1 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=3612, accuracy_bits=22.5, luts=2623, ffs=989, throughput_msps=110, max_abs_err=1.69e-07 (2^-22.50), power_index=4.35
- pipelined_m [data_width=27 n_iter=29 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=3769, accuracy_bits=23, luts=2777, ffs=993, throughput_msps=110, max_abs_err=1.16e-07 (2^-23.04), power_index=4.54
Front coverage: luts_plus_ffs 1256..3769 (HV reference 4000); accuracy_bits 13.2..23 (HV reference 12); data_width on the front 18..27 (registry 8..28).

Per family:
- pipelined: 36 evals, 21 feasible; max throughput seen 273 MSPS; best accuracy 14.04 bits; best feasible luts_plus_ffs=1633; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 1..2, frac_guard 0..2
- pipelined_m: 64 evals, 45 feasible; max throughput seen 171 MSPS; best accuracy 23.04 bits; best feasible luts_plus_ffs=1256; feasible ranges: data_width 16..27, n_iter 15..29, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5547 in, 1124 out
- provider-reported cost: $0.0028
- full prompts and replies: `llm_trace.jsonl`

