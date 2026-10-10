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

## Pareto front (17 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=4` | 800 | 272 | 97.8 | 6 | 1.29 | 0.000204 (2^-12.26) | 12.26 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=4` | 841 | 287 | 93.6 | 6 | 1.36 | 0.000175 (2^-12.48) | 12.48 |
| 2 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=3` | 861 | 332 | 124.5 | 7 | 1.44 | 0.000168 (2^-12.54) | 12.54 |
| 3 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=2,rounding=round,m=4` | 934 | 301 | 93.6 | 6 | 1.49 | 0.000157 (2^-12.64) | 12.64 |
| 4 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=2,rounding=round,m=3` | 956 | 350 | 119.3 | 7 | 1.57 | 0.00014 (2^-12.80) | 12.80 |
| 5 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=2,rounding=round,m=3` | 1002 | 367 | 119.3 | 7 | 1.65 | 9.56e-05 (2^-13.35) | 13.35 |
| 6 | `pipelined_m:data_width=17,n_iter=20,angle_guard=3,frac_guard=3,rounding=trunc,m=2` | 1327 | 704 | 164.4 | 12 | 2.44 | 6.97e-05 (2^-13.81) | 13.81 |
| 7 | `pipelined_m:data_width=17,n_iter=20,angle_guard=2,frac_guard=4,rounding=round,m=2` | 1383 | 714 | 164.4 | 12 | 2.52 | 5.57e-05 (2^-14.13) | 14.13 |
| 8 | `pipelined:data_width=18,n_iter=16,angle_guard=4,frac_guard=4,rounding=trunc` | 1143 | 1162 | 264.5 | 18 | 2.78 | 5.08e-05 (2^-14.27) | 14.27 |
| 9 | `pipelined_m:data_width=17,n_iter=25,angle_guard=3,frac_guard=4,rounding=round,m=3` | 1761 | 655 | 119.3 | 11 | 2.91 | 3.88e-05 (2^-14.65) | 14.65 |
| 10 | `pipelined_m:data_width=17,n_iter=25,angle_guard=4,frac_guard=4,rounding=round,m=3` | 1786 | 664 | 119.3 | 11 | 2.95 | 3.03e-05 (2^-15.01) | 15.01 |
| 11 | `pipelined_m:data_width=24,n_iter=20,angle_guard=-1,frac_guard=4,rounding=trunc,m=2` | 1707 | 908 | 152.6 | 12 | 3.15 | 4.26e-06 (2^-17.84) | 17.84 |
| 12 | `pipelined_m:data_width=24,n_iter=20,angle_guard=3,frac_guard=4,rounding=trunc,m=2` | 1787 | 948 | 152.6 | 12 | 3.29 | 2.23e-06 (2^-18.77) | 18.77 |
| 13 | `pipelined_m:data_width=24,n_iter=20,angle_guard=4,frac_guard=4,rounding=round,m=2` | 1858 | 960 | 152.6 | 12 | 3.39 | 2.05e-06 (2^-18.90) | 18.90 |
| 14 | `pipelined:data_width=24,n_iter=21,angle_guard=4,frac_guard=2,rounding=trunc` | 1818 | 1835 | 249.0 | 23 | 4.4 | 1.54e-06 (2^-19.31) | 19.31 |
| 15 | `pipelined:data_width=27,n_iter=21,angle_guard=1,frac_guard=4,rounding=round` | 2085 | 2041 | 242.0 | 23 | 4.97 | 1.02e-06 (2^-19.90) | 19.90 |
| 16 | `pipelined:data_width=22,n_iter=26,angle_guard=4,frac_guard=4,rounding=round` | 2265 | 2216 | 256.5 | 28 | 5.39 | 1e-06 (2^-19.93) | 19.93 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 results within 0.44us of a 1us tick, meaning the CORDIC must sustain 32 Msps throughput. Only pipelined and pipelined_m families achieve 1 result/cycle, making them the only viable options. The accuracy constraint (max_abs_err <= 2^-12) requires sufficient n_iter and data_width; N=12..16 with W=14..18 should cover the feasible accuracy range while keeping area minimal. Guards are kept tight (angle_guard -1..2, frac_guard 0..2) to minimize LUTs/FFs since the objective is to minimize luts_plus_ffs. pipelined_m with m=2..4 can reduce FF count significantly versus fully pipelined while maintaining the required throughput, so both families get equal budget to map the area-accuracy trade-off front.*)
- `pipelined` (30 evals): data_width=14..18, n_iter=12..16, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Fully pipelined gives 1 result/cycle, which is required to clear the 32 req/us burst within 0.44us without queueing. N=12..16 and W=14..18 are the minimal configs that can plausibly hit max_abs_err <= 2^-12 (0.000244) while keeping area low. Guards are kept tight to minimize LUTs/FFs.
- `pipelined_m` (30 evals): data_width=14..18, n_iter=12..16, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m registers every m stages, reducing FF count compared to fully pipelined while still maintaining 1 result/cycle throughput. This is critical for the 32 req/us burst constraint. m=2..4 balances area reduction against latency (ceil(N/m)+2 cycles). Same accuracy ranges as pipelined since accuracy is independent of m.

**Result (code):** 60 evaluations this round, 60 total; 34 feasible; hypervolume 4400 (n/a).

**LLM decision:** `stop` — The exploration has successfully identified a feasible Pareto front that satisfies all system and accuracy constraints. The minimum area design (pipelined_m, 1072 LUTs+FFs) meets the throughput (97.8 MSPS >= 32), accuracy (12.3 bits >= 12), and system latency (0.161 us <= 0.44 us) requirements. The front extends to higher accuracy (13.7 bits) at the cost of area (2130 LUTs+FFs), providing a good trade-off curve. Since this is the final round and the front covers the relevant design space for the given objectives (min area, max accuracy) with feasible solutions, stopping is the appropriate action.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 4400 (gain this round: n/a (first round)).
Feasible designs: 34 of 60 evaluations (23 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 43% violate; best seen 7.47e-05 (2^-13.71)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.161

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1072, accuracy_bits=12.3, luts=800, ffs=272, throughput_msps=97.8, max_abs_err=0.000204 (2^-12.26), power_index=1.29
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1127, accuracy_bits=12.5, luts=841, ffs=287, throughput_msps=93.6, max_abs_err=0.000175 (2^-12.48), power_index=1.36
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=3] luts_plus_ffs=1193, accuracy_bits=12.5, luts=861, ffs=332, throughput_msps=124, max_abs_err=0.000168 (2^-12.54), power_index=1.44
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1234, accuracy_bits=12.6, luts=934, ffs=301, throughput_msps=93.6, max_abs_err=0.000157 (2^-12.64), power_index=1.49
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=1306, accuracy_bits=12.8, luts=956, ffs=350, throughput_msps=119, max_abs_err=0.00014 (2^-12.80), power_index=1.57
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=1369, accuracy_bits=13.4, luts=1002, ffs=367, throughput_msps=119, max_abs_err=9.56e-05 (2^-13.35), power_index=1.65
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts_plus_ffs=2070, accuracy_bits=13.5, luts=1039, ffs=1031, throughput_msps=264, max_abs_err=8.41e-05 (2^-13.54), power_index=2.49
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=2090, accuracy_bits=13.6, luts=1033, ffs=1057, throughput_msps=264, max_abs_err=8.08e-05 (2^-13.60), power_index=2.52
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=2130, accuracy_bits=13.7, luts=1071, ffs=1059, throughput_msps=264, max_abs_err=7.47e-05 (2^-13.71), power_index=2.56
Front coverage: luts_plus_ffs 1072..2130 (HV reference 4000); accuracy_bits 12.3..13.7 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 30 evals, 17 feasible; max throughput seen 273 MSPS; best accuracy 13.71 bits; best feasible luts_plus_ffs=1784; feasible ranges: data_width 17..18, n_iter 15..16, angle_guard -1..1, frac_guard 0..2
- pipelined_m: 30 evals, 17 feasible; max throughput seen 171 MSPS; best accuracy 13.35 bits; best feasible luts_plus_ffs=1072; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 1..1, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (27 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (6 front designs; box front_anchored)
- `pipelined` (13 evals): data_width=17..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 63 feasible; hypervolume 1.202e+04 (+173.1%).

**No LLM call** (code's front-mapping round): The exploration has successfully identified a feasible Pareto front that satisfies all system and accuracy constraints. The minimum area design (pipelined_m, 1072 LUTs+FFs) meets the throughput (97.8 MSPS >= 32), accuracy (12.3 bits >= 12), and system latency (0.161 us <= 0.44 us) requirements. The front extends to higher accuracy (13.7 bits) at the cost of area (2130 LUTs+FFs), providing a good trade-off curve. Since this is the final round and the front covers the relevant design space for the given objectives (min area, max accuracy) with feasible solutions, stopping is the appropriate action.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.202e+04 (gain this round: +173.1%).
Feasible designs: 63 of 100 evaluations (49 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 31% violate; best seen 1.45e-07 (2^-22.72)
- sys_p99_batch_us <= 0.44: 7% violate; best seen 0.161

Pareto front (feasible, 17 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1072, accuracy_bits=12.3, luts=800, ffs=272, throughput_msps=97.8, max_abs_err=0.000204 (2^-12.26), power_index=1.29
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=3] luts_plus_ffs=1193, accuracy_bits=12.5, luts=861, ffs=332, throughput_msps=124, max_abs_err=0.000168 (2^-12.54), power_index=1.44
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=1306, accuracy_bits=12.8, luts=956, ffs=350, throughput_msps=119, max_abs_err=0.00014 (2^-12.80), power_index=1.57
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=1369, accuracy_bits=13.4, luts=1002, ffs=367, throughput_msps=119, max_abs_err=9.56e-05 (2^-13.35), power_index=1.65
- pipelined_m [data_width=17 n_iter=20 angle_guard=2 frac_guard=4 rounding=round m=2] luts_plus_ffs=2097, accuracy_bits=14.1, luts=1383, ffs=714, throughput_msps=164, max_abs_err=5.57e-05 (2^-14.13), power_index=2.52
- pipelined_m [data_width=17 n_iter=25 angle_guard=3 frac_guard=4 rounding=round m=3] luts_plus_ffs=2416, accuracy_bits=14.7, luts=1761, ffs=655, throughput_msps=119, max_abs_err=3.88e-05 (2^-14.65), power_index=2.91
- pipelined_m [data_width=24 n_iter=20 angle_guard=-1 frac_guard=4 rounding=trunc m=2] luts_plus_ffs=2615, accuracy_bits=17.8, luts=1707, ffs=908, throughput_msps=153, max_abs_err=4.26e-06 (2^-17.84), power_index=3.15
- pipelined_m [data_width=24 n_iter=20 angle_guard=3 frac_guard=4 rounding=trunc m=2] luts_plus_ffs=2736, accuracy_bits=18.8, luts=1787, ffs=948, throughput_msps=153, max_abs_err=2.23e-06 (2^-18.77), power_index=3.29
- pipelined [data_width=24 n_iter=21 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=3653, accuracy_bits=19.3, luts=1818, ffs=1835, throughput_msps=249, max_abs_err=1.54e-06 (2^-19.31), power_index=4.4
- pipelined [data_width=22 n_iter=26 angle_guard=4 frac_guard=4 rounding=round] luts_plus_ffs=4480, accuracy_bits=19.9, luts=2265, ffs=2216, throughput_msps=257, max_abs_err=1e-06 (2^-19.93), power_index=5.39
Front coverage: luts_plus_ffs 1072..4480 (HV reference 4000); accuracy_bits 12.3..19.9 (HV reference 12); data_width on the front 17..27 (registry 8..28).

Per family:
- pipelined: 43 evals, 28 feasible; max throughput seen 273 MSPS; best accuracy 19.93 bits; best feasible luts_plus_ffs=1784; feasible ranges: data_width 17..27, n_iter 14..30, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 57 evals, 35 feasible; max throughput seen 171 MSPS; best accuracy 22.72 bits; best feasible luts_plus_ffs=1072; feasible ranges: data_width 17..24, n_iter 14..26, angle_guard -1..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5570 in, 1199 out
- provider-reported cost: $0.0018
- full prompts and replies: `llm_trace.jsonl`

