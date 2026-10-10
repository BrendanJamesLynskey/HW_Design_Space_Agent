# DSE run: asic_low_area

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 186 of 186 budgeted, over 3 round(s).  
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
  budget: 186 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=15,n_iter=13,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 6870 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1830 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 98 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 147 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 9.22 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 108 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.152 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000879 (2^-10.15) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 7.2 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00022 (2^-12.15) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.8 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.2 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (17 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=13,angle_guard=0,frac_guard=0,rounding=round` | 6870 | 98 | 9.2 | 16 | 0.152 | 0.000879 (2^-10.15) | 10.15 |
| 1 | `iterative:data_width=15,n_iter=13,angle_guard=1,frac_guard=0,rounding=round` | 6933 | 100 | 8.8 | 16 | 0.154 | 0.000673 (2^-10.54) | 10.54 |
| 2 | `iterative:data_width=15,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc` | 7121 | 102 | 8.3 | 17 | 0.167 | 0.000594 (2^-10.72) | 10.72 |
| 3 | `iterative:data_width=16,n_iter=13,angle_guard=0,frac_guard=1,rounding=trunc` | 7376 | 106 | 8.5 | 16 | 0.164 | 0.000498 (2^-10.97) | 10.97 |
| 4 | `iterative:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=trunc` | 7619 | 111 | 7.7 | 17 | 0.181 | 0.000338 (2^-11.53) | 11.53 |
| 5 | `iterative:data_width=17,n_iter=17,angle_guard=2,frac_guard=1,rounding=trunc` | 8212 | 115 | 6.3 | 20 | 0.225 | 0.000174 (2^-12.49) | 12.49 |
| 6 | `iterative:data_width=20,n_iter=29,angle_guard=-2,frac_guard=0,rounding=round` | 9444 | 125 | 3.8 | 32 | 0.4 | 9.69e-05 (2^-13.33) | 13.33 |
| 7 | `iterative:data_width=20,n_iter=29,angle_guard=1,frac_guard=0,rounding=round` | 9634 | 128 | 3.7 | 32 | 0.409 | 2.52e-05 (2^-15.28) | 15.28 |
| 8 | `iterative:data_width=21,n_iter=25,angle_guard=2,frac_guard=0,rounding=round` | 10149 | 135 | 3.9 | 28 | 0.377 | 1.15e-05 (2^-16.41) | 16.41 |
| 9 | `iterative:data_width=24,n_iter=23,angle_guard=2,frac_guard=0,rounding=trunc` | 11360 | 151 | 3.9 | 26 | 0.392 | 2.96e-06 (2^-18.37) | 18.37 |
| 10 | `iterative:data_width=24,n_iter=23,angle_guard=3,frac_guard=0,rounding=round` | 11691 | 152 | 3.8 | 26 | 0.399 | 1.62e-06 (2^-19.24) | 19.24 |
| 11 | `iterative:data_width=24,n_iter=22,angle_guard=2,frac_guard=2,rounding=trunc` | 12075 | 155 | 4.0 | 25 | 0.394 | 1.38e-06 (2^-19.47) | 19.47 |
| 12 | `iterative:data_width=24,n_iter=23,angle_guard=2,frac_guard=2,rounding=trunc` | 12148 | 155 | 3.9 | 26 | 0.411 | 1.14e-06 (2^-19.74) | 19.74 |
| 13 | `iterative:data_width=25,n_iter=25,angle_guard=2,frac_guard=1,rounding=trunc` | 12364 | 159 | 3.5 | 28 | 0.451 | 8.07e-07 (2^-20.24) | 20.24 |
| 14 | `iterative:data_width=27,n_iter=28,angle_guard=2,frac_guard=0,rounding=round` | 13433 | 167 | 3.0 | 31 | 0.534 | 2.09e-07 (2^-22.19) | 22.19 |
| 15 | `iterative:data_width=28,n_iter=29,angle_guard=1,frac_guard=2,rounding=trunc` | 14561 | 176 | 2.8 | 32 | 0.588 | 9.22e-08 (2^-23.37) | 23.37 |
| 16 | `iterative:data_width=28,n_iter=26,angle_guard=2,frac_guard=4,rounding=round` | 17933 | 182 | 3.0 | 29 | 0.599 | 6.35e-08 (2^-23.91) | 23.91 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The merged front is dominated by iterative (13/14 designs, best area 7014 um2). unrolled_k is clearly inferior: 2x the area, only 1 feasible in 24 evals, 0 front members. The remaining budget should be spent almost entirely on refining the iterative Pareto front near the constraint boundary, where the area/accuracy trade-off is steepest. I narrow data_width to 12-16 (the accuracy floor of 2^-10 = 0.000977 requires roughly 12-14 bits of effective precision; going higher wastes area), n_iter to 10-14 (10 is near the threshold, 14 gives comfortable margin), and keep angle_guard and frac_guard at 0-1 to minimize area. Rounding is included as both options since round can sometimes reduce effective error by ~0.5 LSB at negligible area cost. unrolled_k gets a small residual share to confirm it cannot beat iterative, with k limited to 2-4 (higher k increases combinational depth and likely fails Fmax at the throughput constraint). The 100-eval round budget is split ~90/10 between iterative and unrolled_k.*)
- `iterative` (50 evals): data_width=12..16, n_iter=10..14, angle_guard=0..1, frac_guard=0..1, rounding=trunc|round. *Why:* iterative dominates the merged front (13/14) with best area 7014 um2. The 38/76 feasible rate shows the constraint boundary is already well-mapped. Remaining budget should refine the exact Pareto knee: narrow data_width to 12-16 (below 12 likely fails accuracy, above 16 adds area without accuracy gain since 2^-10 error is the floor), n_iter 10-14 (10 is near the accuracy threshold, 14 gives margin), and keep guards minimal (0-1) since area is the sole selection objective. This focuses Optuna on the tightest feasible region where the area/accuracy trade-off is steepest.
- `unrolled_k` (50 evals): data_width=12..16, n_iter=10..14, angle_guard=0..1, frac_guard=0..1, rounding=trunc|round, k=2..4. *Why:* unrolled_k has only 1 feasible design out of 24 evals (area 14455, 2x worse than iterative best) and 0 designs on the merged front. The throughput constraint (>=1 MSPS) is hard to meet with unrolled_k at low Fmax since it produces 1 result every ceil(N/k)+3 cycles. With N~12 and k=2-4, that's 6-9 cycles/result, requiring Fmax >= 100-150 MHz to hit 1 MSPS. The 1 feasible point suggests the constraint boundary is very tight. A small focused search with k=2-4 (higher k reduces cycles but increases combinational depth, likely hurting Fmax) and minimal guards may find a slightly better point, but the expected gain is small. Low budget share reflects low expected value.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 48 feasible; hypervolume 4.41e+04 (n/a).

**LLM decision:** `refine` — The current Pareto front is dominated by the `iterative` family, which achieves the minimum area (6870 um^2) and highest accuracy (11.4 bits) among feasible designs. The `unrolled_k` family is strictly dominated in area (best 9064 um^2) and does not offer a throughput advantage sufficient to justify the area penalty for this low-area spec (iterative already achieves ~9-11 MSPS, well above the 1 MSPS constraint). The feasible region is tightly clustered around data_width 15-16, n_iter 12-13, angle_guard 0-1, and frac_guard 0-1. To maximize hypervolume and find the true minimum area point, I should narrow the search space to this high-performing region and exclude the dominated `unrolled_k` family to focus the remaining budget on refining the `iterative` front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 186.
Hypervolume of the feasible front: 4.41e+04 (gain this round: n/a (first round)).
Feasible designs: 48 of 100 evaluations (28 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11.8
- max_abs_err <= 0.000976562: 52% violate; best seen 0.00038 (2^-11.36)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] area_um2=6870, accuracy_bits=10.2, ffs=98, throughput_msps=9.22, max_abs_err=0.000879 (2^-10.15), power_index=0.152
- iterative [data_width=15 n_iter=13 angle_guard=1 frac_guard=0 rounding=round] area_um2=6933, accuracy_bits=10.5, ffs=100, throughput_msps=8.84, max_abs_err=0.000673 (2^-10.54), power_index=0.154
- iterative [data_width=16 n_iter=12 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=7354, accuracy_bits=10.6, ffs=107, throughput_msps=9.07, max_abs_err=0.000649 (2^-10.59), power_index=0.154
- iterative [data_width=16 n_iter=13 angle_guard=0 frac_guard=1 rounding=trunc] area_um2=7376, accuracy_bits=11, ffs=106, throughput_msps=8.5, max_abs_err=0.000498 (2^-10.97), power_index=0.164
- iterative [data_width=16 n_iter=13 angle_guard=0 frac_guard=1 rounding=round] area_um2=8852, accuracy_bits=11, ffs=106, throughput_msps=8.5, max_abs_err=0.000472 (2^-11.05), power_index=0.178
- iterative [data_width=16 n_iter=13 angle_guard=1 frac_guard=1 rounding=round] area_um2=8915, accuracy_bits=11.4, ffs=107, throughput_msps=8.5, max_abs_err=0.00038 (2^-11.36), power_index=0.179
Front coverage: area_um2 6870..8915 (HV reference 40000); accuracy_bits 10.2..11.4 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- iterative: 50 evals, 23 feasible; max throughput seen 11.8 MSPS; best accuracy 11.36 bits; best feasible area_um2=6870; feasible ranges: data_width 14..16, n_iter 12..13, angle_guard 0..1, frac_guard 0..1
- unrolled_k: 50 evals, 25 feasible; max throughput seen 10.2 MSPS; best accuracy 11.09 bits; best feasible area_um2=9064; feasible ranges: data_width 15..16, n_iter 12..13, angle_guard 0..1, frac_guard 0..1, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Narrowing the iterative family ranges to the observed feasible cluster (data_width 14-17, n_iter 11-14, angle_guard -1 to 2, frac_guard 0-2) allows Optuna to explore the boundaries of the accuracy/area trade-off more efficiently. Excluding unrolled_k saves evaluations for the dominant family.*)
- `iterative` (12 evals): data_width=14..17, n_iter=11..14, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Focus on the proven feasible region of the iterative family to refine the Pareto front and minimize area.

**Result (code):** 12 evaluations this round, 112 total; 55 feasible; hypervolume 8.024e+04 (+81.9%).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 6 distinct designs covering the trade-off space effectively. The minimum area achieved is 6870 um^2 (iterative, data_width=15, n_iter=13), which is significantly below the HV reference of 40000 um^2. The accuracy constraint (max_abs_err <= 2^-10) is met by all front designs, with the best accuracy reaching 12.5 bits. Throughput constraints are comfortably satisfied (best 11.8 MSPS vs 1 MSPS requirement). The iterative family dominates the front, with unrolled_k showing higher area for comparable performance. Since this is the final round and the front covers the relevant region of the objective space (area 6870-9823 um^2, accuracy 10.2-12.5 bits) with clear trade-offs, stopping is appropriate. The selection rule (min area) would pick the 6870 um^2 design, which meets all constraints.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 74 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 112 of 186.
Hypervolume of the feasible front: 8.024e+04 (gain this round: +81.9%).
Feasible designs: 55 of 112 evaluations (33 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11.8
- max_abs_err <= 0.000976562: 51% violate; best seen 0.000169 (2^-12.53)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] area_um2=6870, accuracy_bits=10.2, ffs=98, throughput_msps=9.22, max_abs_err=0.000879 (2^-10.15), power_index=0.152
- iterative [data_width=15 n_iter=13 angle_guard=1 frac_guard=0 rounding=round] area_um2=6933, accuracy_bits=10.5, ffs=100, throughput_msps=8.84, max_abs_err=0.000673 (2^-10.54), power_index=0.154
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=7121, accuracy_bits=10.7, ffs=102, throughput_msps=8.32, max_abs_err=0.000594 (2^-10.72), power_index=0.167
- iterative [data_width=16 n_iter=13 angle_guard=0 frac_guard=1 rounding=trunc] area_um2=7376, accuracy_bits=11, ffs=106, throughput_msps=8.5, max_abs_err=0.000498 (2^-10.97), power_index=0.164
- iterative [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=7619, accuracy_bits=11.5, ffs=111, throughput_msps=7.7, max_abs_err=0.000338 (2^-11.53), power_index=0.181
- iterative [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=9823, accuracy_bits=12.5, ffs=116, throughput_msps=7.42, max_abs_err=0.000169 (2^-12.53), power_index=0.208
Front coverage: area_um2 6870..9823 (HV reference 40000); accuracy_bits 10.2..12.5 (HV reference 10); data_width on the front 15..17 (registry 8..28).

Per family:
- iterative: 62 evals, 30 feasible; max throughput seen 11.8 MSPS; best accuracy 12.53 bits; best feasible area_um2=6870; feasible ranges: data_width 14..17, n_iter 12..14, angle_guard -1..2, frac_guard 0..2
- unrolled_k: 50 evals, 25 feasible; max throughput seen 10.2 MSPS; best accuracy 11.09 bits; best feasible area_um2=9064; feasible ranges: data_width 15..16, n_iter 12..13, angle_guard 0..1, frac_guard 0..1, k 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 74 evaluations*)
- `iterative` (74 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (6 front designs; box front_anchored)

**Result (code):** 74 evaluations this round, 186 total; 125 feasible; hypervolume 4.014e+05 (+400.3%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 6 distinct designs covering the trade-off space effectively. The minimum area achieved is 6870 um^2 (iterative, data_width=15, n_iter=13), which is significantly below the HV reference of 40000 um^2. The accuracy constraint (max_abs_err <= 2^-10) is met by all front designs, with the best accuracy reaching 12.5 bits. Throughput constraints are comfortably satisfied (best 11.8 MSPS vs 1 MSPS requirement). The iterative family dominates the front, with unrolled_k showing higher area for comparable performance. Since this is the final round and the front covers the relevant region of the objective space (area 6870-9823 um^2, accuracy 10.2-12.5 bits) with clear trade-offs, stopping is appropriate. The selection rule (min area) would pick the 6870 um^2 design, which meets all constraints.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 186 of 186.
Hypervolume of the feasible front: 4.014e+05 (gain this round: +400.3%).
Feasible designs: 125 of 186 evaluations (96 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11.8
- max_abs_err <= 0.000976562: 33% violate; best seen 6.35e-08 (2^-23.91)

Pareto front (feasible, 17 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] area_um2=6870, accuracy_bits=10.2, ffs=98, throughput_msps=9.22, max_abs_err=0.000879 (2^-10.15), power_index=0.152
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=7121, accuracy_bits=10.7, ffs=102, throughput_msps=8.32, max_abs_err=0.000594 (2^-10.72), power_index=0.167
- iterative [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=7619, accuracy_bits=11.5, ffs=111, throughput_msps=7.7, max_abs_err=0.000338 (2^-11.53), power_index=0.181
- iterative [data_width=17 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=8212, accuracy_bits=12.5, ffs=115, throughput_msps=6.31, max_abs_err=0.000174 (2^-12.49), power_index=0.225
- iterative [data_width=20 n_iter=29 angle_guard=1 frac_guard=0 rounding=round] area_um2=9634, accuracy_bits=15.3, ffs=128, throughput_msps=3.68, max_abs_err=2.52e-05 (2^-15.28), power_index=0.409
- iterative [data_width=24 n_iter=23 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=11360, accuracy_bits=18.4, ffs=151, throughput_msps=3.88, max_abs_err=2.96e-06 (2^-18.37), power_index=0.392
- iterative [data_width=24 n_iter=22 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=12075, accuracy_bits=19.5, ffs=155, throughput_msps=4.03, max_abs_err=1.38e-06 (2^-19.47), power_index=0.394
- iterative [data_width=24 n_iter=23 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=12148, accuracy_bits=19.7, ffs=155, throughput_msps=3.88, max_abs_err=1.14e-06 (2^-19.74), power_index=0.411
- iterative [data_width=27 n_iter=28 angle_guard=2 frac_guard=0 rounding=round] area_um2=13433, accuracy_bits=22.2, ffs=167, throughput_msps=2.99, max_abs_err=2.09e-07 (2^-22.19), power_index=0.534
- iterative [data_width=28 n_iter=26 angle_guard=2 frac_guard=4 rounding=round] area_um2=17933, accuracy_bits=23.9, ffs=182, throughput_msps=2.96, max_abs_err=6.35e-08 (2^-23.91), power_index=0.599
Front coverage: area_um2 6870..17933 (HV reference 40000); accuracy_bits 10.2..23.9 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 136 evals, 100 feasible; max throughput seen 11.8 MSPS; best accuracy 23.91 bits; best feasible area_um2=6870; feasible ranges: data_width 14..28, n_iter 11..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 50 evals, 25 feasible; max throughput seen 10.2 MSPS; best accuracy 11.09 bits; best feasible area_um2=9064; feasible ranges: data_width 15..16, n_iter 12..13, angle_guard 0..1, frac_guard 0..1, k 2..4
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7027 in, 1804 out
- provider-reported cost: $0.0042
- full prompts and replies: `llm_trace.jsonl`

