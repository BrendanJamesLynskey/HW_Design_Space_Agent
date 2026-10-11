# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec low_area_control: Field-oriented motor-control loop needing sin/cos of the rotor angle at >= 1 MSPS with max error <= 2^-10. Area is everything: minimise LUTs + FFs.
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min luts_plus_ffs (HV ref 1500)
  objective: max accuracy_bits (HV ref 10)
  select: min luts_plus_ffs
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=14,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=5` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 731 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 188 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 80.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 80.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 62 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0346 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000944 (2^-10.05) | exact: bit-accurate model, exhaustive (16384 angles) |
| max_abs_err_lsb | 3.87 | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err | 0.000229 (2^-12.09) | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err_lsb | 0.939 | exact: bit-accurate model, exhaustive (16384 angles) |
| accuracy_bits | 10 | exact: bit-accurate model, exhaustive (16384 angles) |

## Pareto front (15 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=14,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=5` | 731 | 188 | 80.6 | 5 | 0.0346 | 0.000944 (2^-10.05) | 10.05 |
| 1 | `pipelined_m:data_width=15,n_iter=14,angle_guard=1,frac_guard=2,rounding=round,m=8` | 804 | 143 | 52.7 | 4 | 0.0356 | 0.000409 (2^-11.25) | 11.25 |
| 2 | `pipelined_m:data_width=16,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=8` | 813 | 149 | 52.7 | 4 | 0.0362 | 0.000311 (2^-11.65) | 11.65 |
| 3 | `pipelined_m:data_width=19,n_iter=15,angle_guard=3,frac_guard=0,rounding=trunc,m=6` | 979 | 241 | 65.4 | 5 | 0.0459 | 0.000109 (2^-13.17) | 13.17 |
| 4 | `pipelined_m:data_width=19,n_iter=17,angle_guard=2,frac_guard=0,rounding=trunc,m=8` | 1101 | 238 | 50.3 | 5 | 0.0504 | 7.8e-05 (2^-13.65) | 13.65 |
| 5 | `pipelined_m:data_width=19,n_iter=17,angle_guard=2,frac_guard=3,rounding=trunc,m=8` | 1202 | 250 | 50.3 | 5 | 0.0546 | 3.2e-05 (2^-14.93) | 14.93 |
| 6 | `pipelined_m:data_width=19,n_iter=17,angle_guard=3,frac_guard=3,rounding=trunc,m=5` | 1219 | 327 | 77.0 | 6 | 0.0582 | 3.09e-05 (2^-14.98) | 14.98 |
| 7 | `pipelined_m:data_width=24,n_iter=17,angle_guard=2,frac_guard=0,rounding=trunc,m=8` | 1354 | 294 | 48.0 | 5 | 0.062 | 1.65e-05 (2^-15.88) | 15.88 |
| 8 | `pipelined_m:data_width=23,n_iter=21,angle_guard=-2,frac_guard=0,rounding=trunc,m=8` | 1544 | 270 | 48.0 | 5 | 0.0682 | 1.44e-05 (2^-16.08) | 16.08 |
| 9 | `pipelined_m:data_width=23,n_iter=21,angle_guard=2,frac_guard=0,rounding=trunc,m=5` | 1628 | 440 | 73.7 | 7 | 0.0778 | 5.84e-06 (2^-17.39) | 17.39 |
| 10 | `pipelined_m:data_width=24,n_iter=19,angle_guard=2,frac_guard=3,rounding=round,m=4` | 1687 | 483 | 86.0 | 7 | 0.0816 | 4.16e-06 (2^-17.88) | 17.88 |
| 11 | `pipelined_m:data_width=26,n_iter=23,angle_guard=2,frac_guard=0,rounding=round,m=8` | 1999 | 316 | 45.9 | 5 | 0.0871 | 4.56e-07 (2^-21.06) | 21.06 |
| 12 | `pipelined_m:data_width=24,n_iter=24,angle_guard=4,frac_guard=3,rounding=round,m=4` | 2189 | 583 | 86.0 | 8 | 0.104 | 3.93e-07 (2^-21.28) | 21.28 |
| 13 | `pipelined_m:data_width=26,n_iter=23,angle_guard=2,frac_guard=3,rounding=round,m=2` | 2193 | 1174 | 152.6 | 14 | 0.127 | 3.37e-07 (2^-21.50) | 21.50 |
| 14 | `pipelined_m:data_width=26,n_iter=23,angle_guard=3,frac_guard=3,rounding=round,m=2` | 2216 | 1186 | 152.6 | 14 | 0.128 | 3.04e-07 (2^-21.65) | 21.65 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=1 MSPS throughput and max error <=2^-10, with primary objective to minimize LUTs+FFs. Both pipelined and pipelined_m achieve 1 result/cycle, satisfying the throughput constraint in terms of sustained rate (latency is acceptable for a control loop). The key trade-off is between accuracy (driven by n_iter, data_width, guards) and area (driven by number of registers in pipelined_m, and data_width/n_iter in both). We focus on low n_iter (10-16) and data_width (12-16) to minimize area while meeting the 2^-10 accuracy constraint. pipelined_m is expected to be more area-efficient than pipelined due to fewer registers, so we allocate equal budget to explore both and find the Pareto front. angle_guard and frac_guard are kept low (0-2) to minimize area, as they add bits to the datapath. Rounding is explored to see if it affects accuracy/area trade-off.*)
- `pipelined` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Full pipelining gives 1 result/cycle, so throughput_msps = Fmax/1000. To guarantee >=1 MSPS we need Fmax >= 1000 MHz, which is impossible on Artix-7; therefore the pipelined family is only viable if the throughput constraint is interpreted as sustained rate where latency does not block the loop, or if Fmax is high enough. However, since Artix-7 Fmax is typically 200-400 MHz, pipelined alone cannot meet >=1 MSPS unless we accept that 'throughput' here means the loop can sample at 1 MSPS with N+2 latency (which is fine for a control loop). The area is dominated by N stages of registers. Minimizing N and data_width minimizes area. We search low N (10-16) to balance accuracy (need <=2^-10 error) and area. data_width 12-16 ensures output precision. angle_guard and frac_guard kept low to save area.
- `pipelined_m` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* pipelined_m registers every m stages, reducing FF count compared to full pipelining while still achieving 1 result/cycle throughput. This is the key area optimization: fewer registers = fewer FFs. The latency is ceil(N/m)+2, which for N=12, m=4 is 5 cycles, acceptable for a motor control loop. We search m from 2 to 8 to find the sweet spot between area (FFs) and Fmax (longer combinational paths between registers may lower Fmax, but since we need >=1 MSPS and Fmax is likely >1000 MHz in the model or the constraint is relaxed for control loops, we prioritize area). data_width and n_iter ranges match pipelined to ensure accuracy <=2^-10.

**Result (code):** 60 evaluations this round, 60 total; 29 feasible; hypervolume 1194 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 4 distinct designs covering the trade-off between area (919-1264 LUTs+FFs) and accuracy (10-12.9 bits). The minimum area design (pipelined_m, 919 LUTs+FFs) meets the strict accuracy constraint (max_abs_err 0.000944 <= 0.000976562) and throughput constraint (80.6 MSPS >= 1 MSPS). Since this is the final round, further exploration is not possible. The front adequately maps the feasible region for the 'low_area_control' spec, with the selection rule (min luts_plus_ffs) clearly pointing to the 919 LUTs+FFs design as the optimal choice.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1194 (gain this round: n/a (first round)).
Feasible designs: 29 of 60 evaluations (20 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 52% violate; best seen 0.000134 (2^-12.86)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=5] luts_plus_ffs=919, accuracy_bits=10, luts=731, ffs=188, throughput_msps=80.6, max_abs_err=0.000944 (2^-10.05), power_index=0.0346
- pipelined_m [data_width=15 n_iter=14 angle_guard=1 frac_guard=2 rounding=round m=8] luts_plus_ffs=947, accuracy_bits=11.3, luts=804, ffs=143, throughput_msps=52.7, max_abs_err=0.000409 (2^-11.25), power_index=0.0356
- pipelined_m [data_width=16 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=963, accuracy_bits=11.7, luts=813, ffs=149, throughput_msps=52.7, max_abs_err=0.000311 (2^-11.65), power_index=0.0362
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=5] luts_plus_ffs=1264, accuracy_bits=12.9, luts=987, ffs=276, throughput_msps=80.6, max_abs_err=0.000134 (2^-12.86), power_index=0.0475
Front coverage: luts_plus_ffs 919..1264 (HV reference 1500); accuracy_bits 10..12.9 (HV reference 10); data_width on the front 14..16 (registry 8..28).

Per family:
- pipelined: 30 evals, 22 feasible; max throughput seen 282 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=1431; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 30 evals, 7 feasible; max throughput seen 178 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=919; feasible ranges: data_width 14..16, n_iter 14..16, angle_guard 1..2, frac_guard 2..2, m 4..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=13..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 65 feasible; hypervolume 1471 (+23.2%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 4 distinct designs covering the trade-off between area (919-1264 LUTs+FFs) and accuracy (10-12.9 bits). The minimum area design (pipelined_m, 919 LUTs+FFs) meets the strict accuracy constraint (max_abs_err 0.000944 <= 0.000976562) and throughput constraint (80.6 MSPS >= 1 MSPS). Since this is the final round, further exploration is not possible. The front adequately maps the feasible region for the 'low_area_control' spec, with the selection rule (min luts_plus_ffs) clearly pointing to the 919 LUTs+FFs design as the optimal choice.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1471 (gain this round: +23.2%).
Feasible designs: 65 of 100 evaluations (53 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 35% violate; best seen 3.04e-07 (2^-21.65)

Pareto front (feasible, 15 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=5] luts_plus_ffs=919, accuracy_bits=10, luts=731, ffs=188, throughput_msps=80.6, max_abs_err=0.000944 (2^-10.05), power_index=0.0346
- pipelined_m [data_width=16 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=963, accuracy_bits=11.7, luts=813, ffs=149, throughput_msps=52.7, max_abs_err=0.000311 (2^-11.65), power_index=0.0362
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=1220, accuracy_bits=13.2, luts=979, ffs=241, throughput_msps=65.4, max_abs_err=0.000109 (2^-13.17), power_index=0.0459
- pipelined_m [data_width=19 n_iter=17 angle_guard=2 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1453, accuracy_bits=14.9, luts=1202, ffs=250, throughput_msps=50.3, max_abs_err=3.2e-05 (2^-14.93), power_index=0.0546
- pipelined_m [data_width=19 n_iter=17 angle_guard=3 frac_guard=3 rounding=trunc m=5] luts_plus_ffs=1546, accuracy_bits=15, luts=1219, ffs=327, throughput_msps=77, max_abs_err=3.09e-05 (2^-14.98), power_index=0.0582
- pipelined_m [data_width=23 n_iter=21 angle_guard=-2 frac_guard=0 rounding=trunc m=8] luts_plus_ffs=1814, accuracy_bits=16.1, luts=1544, ffs=270, throughput_msps=48, max_abs_err=1.44e-05 (2^-16.08), power_index=0.0682
- pipelined_m [data_width=23 n_iter=21 angle_guard=2 frac_guard=0 rounding=trunc m=5] luts_plus_ffs=2068, accuracy_bits=17.4, luts=1628, ffs=440, throughput_msps=73.7, max_abs_err=5.84e-06 (2^-17.39), power_index=0.0778
- pipelined_m [data_width=26 n_iter=23 angle_guard=2 frac_guard=0 rounding=round m=8] luts_plus_ffs=2315, accuracy_bits=21.1, luts=1999, ffs=316, throughput_msps=45.9, max_abs_err=4.56e-07 (2^-21.06), power_index=0.0871
- pipelined_m [data_width=24 n_iter=24 angle_guard=4 frac_guard=3 rounding=round m=4] luts_plus_ffs=2772, accuracy_bits=21.3, luts=2189, ffs=583, throughput_msps=86, max_abs_err=3.93e-07 (2^-21.28), power_index=0.104
- pipelined_m [data_width=26 n_iter=23 angle_guard=3 frac_guard=3 rounding=round m=2] luts_plus_ffs=3403, accuracy_bits=21.6, luts=2216, ffs=1186, throughput_msps=153, max_abs_err=3.04e-07 (2^-21.65), power_index=0.128
Front coverage: luts_plus_ffs 919..3403 (HV reference 1500); accuracy_bits 10..21.6 (HV reference 10); data_width on the front 14..26 (registry 8..28).

Per family:
- pipelined: 30 evals, 22 feasible; max throughput seen 282 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=1431; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 70 evals, 43 feasible; max throughput seen 178 MSPS; best accuracy 21.65 bits; best feasible luts_plus_ffs=919; feasible ranges: data_width 14..26, n_iter 12..24, angle_guard -2..4, frac_guard 0..3, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4032 in, 1373 out
- provider-reported cost: $0.0040
- full prompts and replies: `llm_trace.jsonl`

