# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`iterative:data_width=18,n_iter=15,angle_guard=0,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 212 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 110 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 194 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 10.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 92.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.218 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000145 (2^-12.75) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 9.48 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 3.17e-05 (2^-14.94) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 2.08 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.8 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (23 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=18,n_iter=15,angle_guard=0,frac_guard=2,rounding=trunc` | 212 | 110 | 10.8 | 18 | 0.218 | 0.000145 (2^-12.75) | 12.75 |
| 1 | `iterative:data_width=18,n_iter=15,angle_guard=0,frac_guard=3,rounding=trunc` | 222 | 112 | 10.8 | 18 | 0.226 | 0.000134 (2^-12.86) | 12.86 |
| 2 | `iterative:data_width=19,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc` | 230 | 112 | 6.4 | 25 | 0.321 | 0.000103 (2^-13.24) | 13.24 |
| 3 | `iterative:data_width=18,n_iter=17,angle_guard=3,frac_guard=1,rounding=trunc` | 232 | 112 | 7.9 | 20 | 0.259 | 8.72e-05 (2^-13.49) | 13.49 |
| 4 | `iterative:data_width=19,n_iter=23,angle_guard=4,frac_guard=0,rounding=trunc` | 237 | 116 | 6.0 | 26 | 0.345 | 8.67e-05 (2^-13.49) | 13.49 |
| 5 | `iterative:data_width=19,n_iter=22,angle_guard=0,frac_guard=0,rounding=round` | 243 | 112 | 6.4 | 25 | 0.334 | 6.48e-05 (2^-13.91) | 13.91 |
| 6 | `iterative:data_width=19,n_iter=27,angle_guard=1,frac_guard=2,rounding=trunc` | 263 | 117 | 5.3 | 30 | 0.429 | 4.74e-05 (2^-14.37) | 14.37 |
| 7 | `iterative:data_width=18,n_iter=20,angle_guard=4,frac_guard=1,rounding=round` | 283 | 113 | 6.9 | 23 | 0.343 | 4.28e-05 (2^-14.51) | 14.51 |
| 8 | `iterative:data_width=19,n_iter=19,angle_guard=4,frac_guard=3,rounding=trunc` | 278 | 122 | 7.1 | 22 | 0.331 | 1.78e-05 (2^-15.78) | 15.78 |
| 9 | `iterative:data_width=23,n_iter=19,angle_guard=-1,frac_guard=0,rounding=trunc` | 290 | 131 | 7.1 | 22 | 0.349 | 1.05e-05 (2^-16.54) | 16.54 |
| 10 | `iterative:data_width=23,n_iter=23,angle_guard=-1,frac_guard=0,rounding=trunc` | 298 | 131 | 6.0 | 26 | 0.419 | 8.62e-06 (2^-16.82) | 16.82 |
| 11 | `iterative:data_width=23,n_iter=19,angle_guard=-1,frac_guard=0,rounding=round` | 302 | 131 | 7.1 | 22 | 0.359 | 8.6e-06 (2^-16.83) | 16.83 |
| 12 | `iterative:data_width=23,n_iter=19,angle_guard=0,frac_guard=0,rounding=round` | 304 | 132 | 7.1 | 22 | 0.361 | 7.05e-06 (2^-17.11) | 17.11 |
| 13 | `iterative:data_width=23,n_iter=27,angle_guard=2,frac_guard=1,rounding=trunc` | 322 | 136 | 5.2 | 30 | 0.517 | 3.54e-06 (2^-18.11) | 18.11 |
| 14 | `iterative:data_width=23,n_iter=28,angle_guard=2,frac_guard=2,rounding=trunc` | 339 | 138 | 5.0 | 31 | 0.556 | 2.24e-06 (2^-18.77) | 18.77 |
| 15 | `iterative:data_width=23,n_iter=27,angle_guard=2,frac_guard=3,rounding=trunc` | 356 | 140 | 5.2 | 30 | 0.56 | 1.54e-06 (2^-19.31) | 19.31 |
| 16 | `iterative:data_width=25,n_iter=27,angle_guard=1,frac_guard=1,rounding=trunc` | 358 | 145 | 5.2 | 30 | 0.568 | 1.13e-06 (2^-19.76) | 19.76 |
| 17 | `iterative:data_width=26,n_iter=29,angle_guard=1,frac_guard=0,rounding=trunc` | 360 | 148 | 4.8 | 32 | 0.612 | 9.99e-07 (2^-19.93) | 19.93 |
| 18 | `iterative:data_width=27,n_iter=22,angle_guard=0,frac_guard=0,rounding=round` | 383 | 152 | 6.1 | 25 | 0.503 | 7.1e-07 (2^-20.43) | 20.43 |
| 19 | `iterative:data_width=28,n_iter=29,angle_guard=-2,frac_guard=0,rounding=trunc` | 395 | 155 | 4.8 | 32 | 0.663 | 6.09e-07 (2^-20.65) | 20.65 |
| 20 | `iterative:data_width=28,n_iter=24,angle_guard=1,frac_guard=1,rounding=trunc` | 404 | 160 | 5.7 | 27 | 0.574 | 2.18e-07 (2^-22.13) | 22.13 |
| 21 | `iterative:data_width=28,n_iter=27,angle_guard=2,frac_guard=3,rounding=trunc` | 451 | 165 | 5.0 | 30 | 0.696 | 6.09e-08 (2^-23.97) | 23.97 |
| 22 | `iterative:data_width=27,n_iter=29,angle_guard=3,frac_guard=3,rounding=round` | 514 | 161 | 4.8 | 32 | 0.812 | 5.3e-08 (2^-24.17) | 24.17 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Spec: throughput >= 1 MSPS, max_abs_err <= 2^-10, minimise luts_plus_ffs and maximise accuracy_bits. Only iterative and unrolled_k are available. unrolled_k chains k micro-rotations per cycle, multiplying datapath area and reducing Fmax; its only benefit is fewer cycles, but the throughput constraint is already easily met by iterative at the required N values. Therefore the feasible Pareto front must come from iterative. The first exploration should map that front broadly: data_width 11..28 covers the minimum feasible output width up to the registry maximum; n_iter 11..30 covers the minimum CORDIC accuracy up to the registry maximum; angle_guard -2..4 and frac_guard 0..4 cover the guard-bit trade-offs; both roundings are included because rounding can save area at the error threshold. This focuses the full 100-eval budget on the only family that can produce non-dominated points for this spec.*)
- `iterative` (60 evals): data_width=11..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Iterative shares one micro-rotation datapath and needs only N+3 cycles/result. For N in 11..30 and typical Artix-7 Fmax, throughput >=1 MSPS is easily met, so its lower area dominates unrolled_k. It computes identical bits to unrolled_k for the same (data_width, n_iter, angle_guard, frac_guard, rounding), but unrolled_k replicates the datapath k times and lengthens the critical path, so it has strictly larger luts_plus_ffs for the same accuracy and cannot be Pareto-optimal here. W>=11 is the minimum that can satisfy max_abs_err<=2^-10 (output LSB 2^-(W-2)); N>=11 is the minimum for the CORDIC angle residual. Upper bounds cover the high-accuracy/high-area region up to the HV reference area of 1500.

**Result (code):** 60 evaluations this round, 60 total; 52 feasible; hypervolume 1.461e+04 (n/a).

**LLM decision:** `stop` — Final round: only `stop` or `infeasible` are admissible, and the evidence rules out infeasible. The spec's constraints are both met with margin by many designs: 0% of evaluations violate throughput_msps >= 1 (best seen 13.5 MSPS) and only 13% violate max_abs_err <= 2^-10 (best seen 2^-24.17). The feasible Pareto front already spans the area objective from luts_plus_ffs=322 up to 675 (HV ref 1500) and accuracy from 12.8 to 24.2 bits (HV ref 10), i.e. it covers both objective ranges well past their reference points, giving hypervolume 1.461e+04. The selection rule (min luts_plus_ffs) is satisfied by the front's cheapest point, iterative [data_width=18 n_iter=15 angle_guard=0 frac_guard=2 rounding=trunc] at luts_plus_ffs=322, accuracy_bits=12.8 (max_abs_err 2^-12.75, comfortably under the 2^-10 limit) and throughput 10.8 MSPS (well above 1 MSPS). No constraint is unreachable, so `infeasible` is not justified, and with the round cap reached there is no scope to improve the front further.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.461e+04 (gain this round: n/a (first round)).
Feasible designs: 52 of 60 evaluations (49 unique).
Families explored so far: iterative. Not yet explored: unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 13.5
- max_abs_err <= 0.000976562: 13% violate; best seen 5.3e-08 (2^-24.17)

Pareto front (feasible, 21 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=18 n_iter=15 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=322, accuracy_bits=12.8, luts=212, ffs=110, throughput_msps=10.8, max_abs_err=0.000145 (2^-12.75), power_index=0.218
- iterative [data_width=19 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=342, accuracy_bits=13.2, luts=230, ffs=112, throughput_msps=6.36, max_abs_err=0.000103 (2^-13.24), power_index=0.321
- iterative [data_width=19 n_iter=23 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=350, accuracy_bits=13.4, luts=235, ffs=115, throughput_msps=6.11, max_abs_err=9.25e-05 (2^-13.40), power_index=0.342
- iterative [data_width=18 n_iter=20 angle_guard=4 frac_guard=1 rounding=round] luts_plus_ffs=396, accuracy_bits=14.5, luts=283, ffs=113, throughput_msps=6.91, max_abs_err=4.28e-05 (2^-14.51), power_index=0.343
- iterative [data_width=23 n_iter=19 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=421, accuracy_bits=16.5, luts=290, ffs=131, throughput_msps=7.09, max_abs_err=1.05e-05 (2^-16.54), power_index=0.349
- iterative [data_width=23 n_iter=19 angle_guard=-1 frac_guard=0 rounding=round] luts_plus_ffs=433, accuracy_bits=16.8, luts=302, ffs=131, throughput_msps=7.09, max_abs_err=8.6e-06 (2^-16.83), power_index=0.359
- iterative [data_width=23 n_iter=27 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=458, accuracy_bits=18.1, luts=322, ffs=136, throughput_msps=5.2, max_abs_err=3.54e-06 (2^-18.11), power_index=0.517
- iterative [data_width=27 n_iter=22 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=535, accuracy_bits=20.4, luts=383, ffs=152, throughput_msps=6.13, max_abs_err=7.1e-07 (2^-20.43), power_index=0.503
- iterative [data_width=25 n_iter=28 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=596, accuracy_bits=21.7, luts=447, ffs=149, throughput_msps=4.94, max_abs_err=2.93e-07 (2^-21.71), power_index=0.695
- iterative [data_width=27 n_iter=29 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=675, accuracy_bits=24.2, luts=514, ffs=161, throughput_msps=4.79, max_abs_err=5.3e-08 (2^-24.17), power_index=0.812
Front coverage: luts_plus_ffs 322..675 (HV reference 1500); accuracy_bits 12.8..24.2 (HV reference 10); data_width on the front 18..27 (registry 8..28).

Per family:
- iterative: 60 evals, 52 feasible; max throughput seen 13.5 MSPS; best accuracy 24.17 bits; best feasible luts_plus_ffs=322; feasible ranges: data_width 16..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (40 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (21 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 92 feasible; hypervolume 1.481e+04 (+1.4%).

**No LLM call** (code's front-mapping round): Final round: only `stop` or `infeasible` are admissible, and the evidence rules out infeasible. The spec's constraints are both met with margin by many designs: 0% of evaluations violate throughput_msps >= 1 (best seen 13.5 MSPS) and only 13% violate max_abs_err <= 2^-10 (best seen 2^-24.17). The feasible Pareto front already spans the area objective from luts_plus_ffs=322 up to 675 (HV ref 1500) and accuracy from 12.8 to 24.2 bits (HV ref 10), i.e. it covers both objective ranges well past their reference points, giving hypervolume 1.461e+04. The selection rule (min luts_plus_ffs) is satisfied by the front's cheapest point, iterative [data_width=18 n_iter=15 angle_guard=0 frac_guard=2 rounding=trunc] at luts_plus_ffs=322, accuracy_bits=12.8 (max_abs_err 2^-12.75, comfortably under the 2^-10 limit) and throughput 10.8 MSPS (well above 1 MSPS). No constraint is unreachable, so `infeasible` is not justified, and with the round cap reached there is no scope to improve the front further.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.481e+04 (gain this round: +1.4%).
Feasible designs: 92 of 100 evaluations (86 unique).
Families explored so far: iterative. Not yet explored: unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 13.5
- max_abs_err <= 0.000976562: 8% violate; best seen 5.3e-08 (2^-24.17)

Pareto front (feasible, 23 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=18 n_iter=15 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=322, accuracy_bits=12.8, luts=212, ffs=110, throughput_msps=10.8, max_abs_err=0.000145 (2^-12.75), power_index=0.218
- iterative [data_width=19 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=342, accuracy_bits=13.2, luts=230, ffs=112, throughput_msps=6.36, max_abs_err=0.000103 (2^-13.24), power_index=0.321
- iterative [data_width=19 n_iter=22 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=355, accuracy_bits=13.9, luts=243, ffs=112, throughput_msps=6.36, max_abs_err=6.48e-05 (2^-13.91), power_index=0.334
- iterative [data_width=18 n_iter=20 angle_guard=4 frac_guard=1 rounding=round] luts_plus_ffs=396, accuracy_bits=14.5, luts=283, ffs=113, throughput_msps=6.91, max_abs_err=4.28e-05 (2^-14.51), power_index=0.343
- iterative [data_width=23 n_iter=23 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=429, accuracy_bits=16.8, luts=298, ffs=131, throughput_msps=6, max_abs_err=8.62e-06 (2^-16.82), power_index=0.419
- iterative [data_width=23 n_iter=19 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=436, accuracy_bits=17.1, luts=304, ffs=132, throughput_msps=7.09, max_abs_err=7.05e-06 (2^-17.11), power_index=0.361
- iterative [data_width=23 n_iter=27 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=496, accuracy_bits=19.3, luts=356, ffs=140, throughput_msps=5.2, max_abs_err=1.54e-06 (2^-19.31), power_index=0.56
- iterative [data_width=26 n_iter=29 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=508, accuracy_bits=19.9, luts=360, ffs=148, throughput_msps=4.79, max_abs_err=9.99e-07 (2^-19.93), power_index=0.612
- iterative [data_width=28 n_iter=24 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=565, accuracy_bits=22.1, luts=404, ffs=160, throughput_msps=5.68, max_abs_err=2.18e-07 (2^-22.13), power_index=0.574
- iterative [data_width=27 n_iter=29 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=675, accuracy_bits=24.2, luts=514, ffs=161, throughput_msps=4.79, max_abs_err=5.3e-08 (2^-24.17), power_index=0.812
Front coverage: luts_plus_ffs 322..675 (HV reference 1500); accuracy_bits 12.8..24.2 (HV reference 10); data_width on the front 18..28 (registry 8..28).

Per family:
- iterative: 100 evals, 92 feasible; max throughput seen 13.5 MSPS; best accuracy 24.17 bits; best feasible luts_plus_ffs=322; feasible ranges: data_width 16..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4333 in, 10911 out
- provider-reported cost: $0.0074
- full prompts and replies: `llm_trace.jsonl`

