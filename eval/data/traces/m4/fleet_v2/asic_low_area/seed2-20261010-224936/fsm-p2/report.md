# DSE run: asic_low_area

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_low_area: Motor-control sin/cos in sky130 standard cells: >= 1 MSPS, max error <= 2^-10. Area is everything: minimise cell area.
  target: asic-sky130hd
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min area_um2 (HV ref 40000)
  objective: max accuracy_bits (HV ref 10)
  select: min area_um2
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=15,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 6979 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1859 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 98 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 147 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 8.19 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 122 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.173 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.00081 (2^-10.27) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.64 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00021 (2^-12.22) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.72 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (33 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 6979 | 98 | 8.2 | 18 | 0.173 | 0.00081 (2^-10.27) | 10.27 |
| 1 | `iterative:data_width=14,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc` | 7016 | 100 | 8.8 | 16 | 0.155 | 0.000746 (2^-10.39) | 10.39 |
| 2 | `iterative:data_width=15,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 7042 | 100 | 7.9 | 18 | 0.174 | 0.000632 (2^-10.63) | 10.63 |
| 3 | `iterative:data_width=15,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 7057 | 101 | 8.0 | 17 | 0.166 | 0.000599 (2^-10.71) | 10.71 |
| 4 | `iterative:data_width=16,n_iter=13,angle_guard=0,frac_guard=0,rounding=round` | 7249 | 104 | 8.8 | 16 | 0.161 | 0.000492 (2^-10.99) | 10.99 |
| 5 | `iterative:data_width=16,n_iter=13,angle_guard=1,frac_guard=0,rounding=round` | 7313 | 105 | 8.5 | 16 | 0.162 | 0.000417 (2^-11.23) | 11.23 |
| 6 | `iterative:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` | 7322 | 104 | 8.3 | 17 | 0.172 | 0.0004 (2^-11.29) | 11.29 |
| 7 | `iterative:data_width=16,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 7383 | 104 | 7.9 | 18 | 0.182 | 0.000373 (2^-11.39) | 11.39 |
| 8 | `iterative:data_width=16,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 7385 | 105 | 8.0 | 17 | 0.173 | 0.000342 (2^-11.51) | 11.51 |
| 9 | `iterative:data_width=16,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 7449 | 106 | 7.7 | 17 | 0.175 | 0.000294 (2^-11.73) | 11.73 |
| 10 | `iterative:data_width=16,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 7558 | 106 | 6.9 | 19 | 0.197 | 0.000285 (2^-11.78) | 11.78 |
| 11 | `iterative:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` | 7860 | 111 | 7.7 | 17 | 0.183 | 0.00027 (2^-11.85) | 11.85 |
| 12 | `iterative:data_width=16,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc` | 7869 | 109 | 7.3 | 18 | 0.193 | 0.00025 (2^-11.97) | 11.97 |
| 13 | `iterative:data_width=17,n_iter=25,angle_guard=3,frac_guard=0,rounding=round` | 8283 | 114 | 4.4 | 28 | 0.314 | 0.000146 (2^-12.74) | 12.74 |
| 14 | `iterative:data_width=17,n_iter=28,angle_guard=3,frac_guard=3,rounding=trunc` | 9100 | 120 | 3.9 | 31 | 0.374 | 9.27e-05 (2^-13.40) | 13.40 |
| 15 | `iterative:data_width=17,n_iter=24,angle_guard=3,frac_guard=4,rounding=trunc` | 9493 | 123 | 4.4 | 27 | 0.335 | 6.21e-05 (2^-13.97) | 13.97 |
| 16 | `iterative:data_width=21,n_iter=24,angle_guard=2,frac_guard=0,rounding=trunc` | 9858 | 135 | 4.1 | 27 | 0.359 | 2.5e-05 (2^-15.29) | 15.29 |
| 17 | `iterative:data_width=21,n_iter=25,angle_guard=3,frac_guard=0,rounding=round` | 10213 | 136 | 3.8 | 28 | 0.38 | 1.15e-05 (2^-16.41) | 16.41 |
| 18 | `iterative:data_width=21,n_iter=24,angle_guard=1,frac_guard=2,rounding=trunc` | 10606 | 138 | 4.1 | 27 | 0.376 | 9.95e-06 (2^-16.62) | 16.62 |
| 19 | `iterative:data_width=21,n_iter=24,angle_guard=3,frac_guard=2,rounding=trunc` | 10733 | 140 | 4.0 | 27 | 0.381 | 7.43e-06 (2^-17.04) | 17.04 |
| 20 | `iterative:data_width=21,n_iter=26,angle_guard=2,frac_guard=3,rounding=trunc` | 11112 | 141 | 3.7 | 29 | 0.417 | 5.95e-06 (2^-17.36) | 17.36 |
| 21 | `iterative:data_width=21,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc` | 11175 | 142 | 3.7 | 29 | 0.42 | 5.08e-06 (2^-17.59) | 17.59 |
| 22 | `iterative:data_width=23,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc` | 12250 | 153 | 3.5 | 29 | 0.456 | 1.25e-06 (2^-19.61) | 19.61 |
| 23 | `iterative:data_width=24,n_iter=24,angle_guard=3,frac_guard=2,rounding=trunc` | 12272 | 156 | 3.6 | 27 | 0.43 | 9.21e-07 (2^-20.05) | 20.05 |
| 24 | `iterative:data_width=25,n_iter=23,angle_guard=2,frac_guard=2,rounding=trunc` | 12649 | 161 | 3.8 | 26 | 0.426 | 6.35e-07 (2^-20.59) | 20.59 |
| 25 | `iterative:data_width=25,n_iter=23,angle_guard=2,frac_guard=3,rounding=trunc` | 13042 | 163 | 3.7 | 26 | 0.435 | 5.4e-07 (2^-20.82) | 20.82 |
| 26 | `iterative:data_width=25,n_iter=24,angle_guard=2,frac_guard=3,rounding=trunc` | 13127 | 163 | 3.5 | 27 | 0.454 | 4.5e-07 (2^-21.08) | 21.08 |
| 27 | `iterative:data_width=26,n_iter=24,angle_guard=2,frac_guard=2,rounding=trunc` | 13234 | 166 | 3.5 | 27 | 0.46 | 3.49e-07 (2^-21.45) | 21.45 |
| 28 | `iterative:data_width=26,n_iter=25,angle_guard=2,frac_guard=2,rounding=trunc` | 13307 | 166 | 3.4 | 28 | 0.478 | 3.07e-07 (2^-21.63) | 21.63 |
| 29 | `iterative:data_width=26,n_iter=24,angle_guard=2,frac_guard=3,rounding=trunc` | 13640 | 169 | 3.4 | 27 | 0.47 | 2.59e-07 (2^-21.88) | 21.88 |
| 30 | `iterative:data_width=28,n_iter=25,angle_guard=3,frac_guard=0,rounding=round` | 13876 | 174 | 3.1 | 28 | 0.5 | 1.38e-07 (2^-22.79) | 22.79 |
| 31 | `iterative:data_width=28,n_iter=30,angle_guard=2,frac_guard=3,rounding=trunc` | 15139 | 179 | 2.7 | 33 | 0.624 | 5.37e-08 (2^-24.15) | 24.15 |
| 32 | `iterative:data_width=28,n_iter=30,angle_guard=3,frac_guard=3,rounding=trunc` | 15202 | 181 | 2.7 | 33 | 0.627 | 4.04e-08 (2^-24.56) | 24.56 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts are unambiguous: iterative dominates the merged front (14/14 designs, best area 7860 um2), while unrolled_k (best 9189), pipelined (31433) and pipelined_m (19953) contribute nothing to the front. The spec is area-minimisation with a hard 1 MSPS throughput floor and a 2^-10 max-error cap. iterative's shared-datapath, one-rotation-per-cycle structure is the natural low-area candidate; unrolled_k's k chained rotations per cycle add combinational depth and area for a throughput we do not need (iterative already clears 1 MSPS at its Fmax). I therefore concentrate the entire remaining budget on iterative, but tighten the ranges around the accuracy/area knee rather than re-sweeping the full space: data_width 12-16 (below 12 the Q1.(W-2) output cannot represent 2^-10 error; above 16 area grows with little accuracy gain), n_iter 10-16 (the minimum N that reaches 2^-10 max error, plus headroom), and small angle_guard/frac_guard (0-2) since the error budget is already met at modest widths. Keeping both rounding modes lets Optuna trade a handful of gates for accuracy_bits, which is the second hypervolume objective. unrolled_k is dropped from this round because it has 0 front designs and a worse best area; spending budget there would not improve the front or hypervolume.*)
- `iterative` (100 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the only family on the merged front (14/14 designs) and holds the best feasible area (7860 um2). The prior 45 evals already mapped a broad region; this round narrows to the accuracy/area knee: data_width 12-16 (10-bit error bound needs ~12+ bits of output precision), n_iter 10-16 (enough micro-rotations to hit 2^-10 max error without over-rotating and inflating area), angle_guard 0-2 and frac_guard 0-2 (small guards keep the datapath narrow; larger guards add area with diminishing accuracy return). rounding both kept since round can trade a few gates for accuracy_bits, which is the second HV objective.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 59 feasible; hypervolume 7.977e+04 (n/a).

**LLM decision:** `add_family` — The iterative family has been explored and shows a clear Pareto front with best area 6979 um^2 at 10.3 bits accuracy. The throughput constraint is easily met (best 11.3 MSPS). The accuracy constraint is met by most designs on the front. However, unrolled_k has not been explored yet. Unrolled architectures can sometimes reduce area by sharing logic more efficiently or improving Fmax through shorter critical paths, which could yield better area/accuracy trade-offs. Exploring unrolled_k with k=2..4 in the same parameter ranges as the iterative front is a logical next step to see if it can beat the current best area of 6979 um^2 while maintaining accuracy >= 10 bits. The iterative family will also be refined to ensure the front is well-mapped.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 7.977e+04 (gain this round: n/a (first round)).
Feasible designs: 59 of 100 evaluations (38 unique).
Families explored so far: iterative. Not yet explored: unrolled_k.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11.3
- max_abs_err <= 0.000976562: 41% violate; best seen 0.000177 (2^-12.47)

Pareto front (feasible, 14 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] area_um2=6979, accuracy_bits=10.3, ffs=98, throughput_msps=8.19, max_abs_err=0.00081 (2^-10.27), power_index=0.173
- iterative [data_width=14 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7016, accuracy_bits=10.4, ffs=100, throughput_msps=8.84, max_abs_err=0.000746 (2^-10.39), power_index=0.155
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=7057, accuracy_bits=10.7, ffs=101, throughput_msps=8, max_abs_err=0.000599 (2^-10.71), power_index=0.166
- iterative [data_width=16 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] area_um2=7249, accuracy_bits=11, ffs=104, throughput_msps=8.84, max_abs_err=0.000492 (2^-10.99), power_index=0.161
- iterative [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] area_um2=7322, accuracy_bits=11.3, ffs=104, throughput_msps=8.32, max_abs_err=0.0004 (2^-11.29), power_index=0.172
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=7385, accuracy_bits=11.5, ffs=105, throughput_msps=8, max_abs_err=0.000342 (2^-11.51), power_index=0.173
- iterative [data_width=16 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=7558, accuracy_bits=11.8, ffs=106, throughput_msps=6.89, max_abs_err=0.000285 (2^-11.78), power_index=0.197
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7860, accuracy_bits=11.9, ffs=111, throughput_msps=7.7, max_abs_err=0.00027 (2^-11.85), power_index=0.183
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=9064, accuracy_bits=12.2, ffs=108, throughput_msps=7.7, max_abs_err=0.000209 (2^-12.22), power_index=0.193
- iterative [data_width=16 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=9197, accuracy_bits=12.5, ffs=108, throughput_msps=6.89, max_abs_err=0.000177 (2^-12.47), power_index=0.217
Front coverage: area_um2 6979..9197 (HV reference 40000); accuracy_bits 10.3..12.5 (HV reference 10); data_width on the front 14..16 (registry 8..28).

Per family:
- iterative: 100 evals, 59 feasible; max throughput seen 11.3 MSPS; best accuracy 12.47 bits; best feasible area_um2=6979; feasible ranges: data_width 14..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The iterative family has been explored and shows a clear Pareto front with best area 6979 um^2 at 10.3 bits accuracy. The throughput constraint is easily met (best 11.3 MSPS). The accuracy constraint is met by most designs on the front. However, unrolled_k has not been explored yet. Unrolled architectures can sometimes reduce area by sharing logic more efficiently or improving Fmax through shorter critical paths, which could yield better area/accuracy trade-offs. Exploring unrolled_k with k=2..4 in the same parameter ranges as the iterative front is a logical next step to see if it can beat the current best area of 6979 um^2 while maintaining accuracy >= 10 bits. The iterative family will also be refined to ensure the front is well-mapped.*)
- `unrolled_k` (10 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k with k>1 can achieve higher Fmax or lower area for the same accuracy by reducing FSM overhead and critical path length compared to iterative, potentially improving the area/accuracy trade-off.
- `iterative` (10 evals): data_width=14..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Refine the iterative family around the current Pareto front (data_width 14-16, n_iter 12-16) to ensure no better area/accuracy points are missed in this family.

**Result (code):** 20 evaluations this round, 120 total; 78 feasible; hypervolume 1.164e+05 (+45.9%).

**LLM decision:** `stop` — The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (iterative, 6979 um^2) meets the throughput requirement (8.19 MSPS >= 1) and accuracy requirement (10.3 bits >= 10). The front covers a reasonable range of trade-offs from 6979 um^2/10.3 bits to 16623 um^2/13.8 bits. Since this is the final round, we stop. The selection rule (min area) picks the iterative design with data_width=15, n_iter=15, angle_guard=0, frac_guard=0, rounding=round at 6979 um^2.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.164e+05 (gain this round: +45.9%).
Feasible designs: 78 of 120 evaluations (51 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11.3
- max_abs_err <= 0.000976562: 35% violate; best seen 6.92e-05 (2^-13.82)

Pareto front (feasible, 16 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] area_um2=6979, accuracy_bits=10.3, ffs=98, throughput_msps=8.19, max_abs_err=0.00081 (2^-10.27), power_index=0.173
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=7042, accuracy_bits=10.6, ffs=100, throughput_msps=7.86, max_abs_err=0.000632 (2^-10.63), power_index=0.174
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=7057, accuracy_bits=10.7, ffs=101, throughput_msps=8, max_abs_err=0.000599 (2^-10.71), power_index=0.166
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=0 rounding=round] area_um2=7313, accuracy_bits=11.2, ffs=105, throughput_msps=8.5, max_abs_err=0.000417 (2^-11.23), power_index=0.162
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=7385, accuracy_bits=11.5, ffs=105, throughput_msps=8, max_abs_err=0.000342 (2^-11.51), power_index=0.173
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=7449, accuracy_bits=11.7, ffs=106, throughput_msps=7.7, max_abs_err=0.000294 (2^-11.73), power_index=0.175
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7860, accuracy_bits=11.9, ffs=111, throughput_msps=7.7, max_abs_err=0.00027 (2^-11.85), power_index=0.183
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=9064, accuracy_bits=12.2, ffs=108, throughput_msps=7.7, max_abs_err=0.000209 (2^-12.22), power_index=0.193
- iterative [data_width=16 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=9197, accuracy_bits=12.5, ffs=108, throughput_msps=6.89, max_abs_err=0.000177 (2^-12.47), power_index=0.217
- unrolled_k [data_width=18 n_iter=17 angle_guard=1 frac_guard=2 rounding=trunc k=4] area_um2=16623, accuracy_bits=13.8, ffs=119, throughput_msps=4.31, max_abs_err=6.92e-05 (2^-13.82), power_index=0.131
Front coverage: area_um2 6979..16623 (HV reference 40000); accuracy_bits 10.3..13.8 (HV reference 10); data_width on the front 14..18 (registry 8..28).

Per family:
- iterative: 110 evals, 69 feasible; max throughput seen 11.3 MSPS; best accuracy 12.47 bits; best feasible area_um2=6979; feasible ranges: data_width 14..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
- unrolled_k: 10 evals, 9 feasible; max throughput seen 7.66 MSPS; best accuracy 13.82 bits; best feasible area_um2=9351; feasible ranges: data_width 15..18, n_iter 12..17, angle_guard 1..2, frac_guard 0..2, k 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `iterative` (70 evals): data_width=13..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (14 front designs; box front_anchored)
- `unrolled_k` (10 evals): data_width=16..28, n_iter=15..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (2 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 155 feasible; hypervolume 4.194e+05 (+260.2%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (iterative, 6979 um^2) meets the throughput requirement (8.19 MSPS >= 1) and accuracy requirement (10.3 bits >= 10). The front covers a reasonable range of trade-offs from 6979 um^2/10.3 bits to 16623 um^2/13.8 bits. Since this is the final round, we stop. The selection rule (min area) picks the iterative design with data_width=15, n_iter=15, angle_guard=0, frac_guard=0, rounding=round at 6979 um^2.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 4.194e+05 (gain this round: +260.2%).
Feasible designs: 155 of 200 evaluations (117 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11.3
- max_abs_err <= 0.000976562: 22% violate; best seen 4.04e-08 (2^-24.56)

Pareto front (feasible, 33 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] area_um2=6979, accuracy_bits=10.3, ffs=98, throughput_msps=8.19, max_abs_err=0.00081 (2^-10.27), power_index=0.173
- iterative [data_width=16 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] area_um2=7249, accuracy_bits=11, ffs=104, throughput_msps=8.84, max_abs_err=0.000492 (2^-10.99), power_index=0.161
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] area_um2=7383, accuracy_bits=11.4, ffs=104, throughput_msps=7.86, max_abs_err=0.000373 (2^-11.39), power_index=0.182
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7860, accuracy_bits=11.9, ffs=111, throughput_msps=7.7, max_abs_err=0.00027 (2^-11.85), power_index=0.183
- iterative [data_width=17 n_iter=28 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=9100, accuracy_bits=13.4, ffs=120, throughput_msps=3.93, max_abs_err=9.27e-05 (2^-13.40), power_index=0.374
- iterative [data_width=21 n_iter=24 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=10606, accuracy_bits=16.6, ffs=138, throughput_msps=4.09, max_abs_err=9.95e-06 (2^-16.62), power_index=0.376
- iterative [data_width=21 n_iter=26 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=11175, accuracy_bits=17.6, ffs=142, throughput_msps=3.69, max_abs_err=5.08e-06 (2^-17.59), power_index=0.42
- iterative [data_width=25 n_iter=23 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=13042, accuracy_bits=20.8, ffs=163, throughput_msps=3.67, max_abs_err=5.4e-07 (2^-20.82), power_index=0.435
- iterative [data_width=26 n_iter=25 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=13307, accuracy_bits=21.6, ffs=166, throughput_msps=3.4, max_abs_err=3.07e-07 (2^-21.63), power_index=0.478
- iterative [data_width=28 n_iter=30 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=15202, accuracy_bits=24.6, ffs=181, throughput_msps=2.67, max_abs_err=4.04e-08 (2^-24.56), power_index=0.627
Front coverage: area_um2 6979..15202 (HV reference 40000); accuracy_bits 10.3..24.6 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 180 evals, 136 feasible; max throughput seen 11.3 MSPS; best accuracy 24.56 bits; best feasible area_um2=6979; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 20 evals, 19 feasible; max throughput seen 7.66 MSPS; best accuracy 17.87 bits; best feasible area_um2=9351; feasible ranges: data_width 15..23, n_iter 12..25, angle_guard -2..3, frac_guard 0..4, k 2..7
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7637 in, 2054 out
- provider-reported cost: $0.0045
- full prompts and replies: `llm_trace.jsonl`

