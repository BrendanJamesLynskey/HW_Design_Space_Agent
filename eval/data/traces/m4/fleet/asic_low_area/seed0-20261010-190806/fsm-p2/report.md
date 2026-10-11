# DSE run: asic_low_area

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`iterative:data_width=15,n_iter=13,angle_guard=2,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 6997 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1864 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 101 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 136 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 8.5 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 118 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.155 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000642 (2^-10.61) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 5.26 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00017 (2^-12.52) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.39 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.6 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (25 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=13,angle_guard=2,frac_guard=0,rounding=round` | 6997 | 101 | 8.5 | 16 | 0.155 | 0.000642 (2^-10.61) | 10.61 |
| 1 | `iterative:data_width=15,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 7042 | 100 | 7.9 | 18 | 0.174 | 0.000632 (2^-10.63) | 10.63 |
| 2 | `iterative:data_width=15,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 7106 | 101 | 7.6 | 18 | 0.176 | 0.000599 (2^-10.71) | 10.71 |
| 3 | `iterative:data_width=15,n_iter=17,angle_guard=2,frac_guard=1,rounding=trunc` | 7357 | 104 | 6.8 | 20 | 0.202 | 0.000567 (2^-10.78) | 10.78 |
| 4 | `iterative:data_width=15,n_iter=17,angle_guard=2,frac_guard=2,rounding=trunc` | 7677 | 106 | 6.8 | 20 | 0.208 | 0.000344 (2^-11.51) | 11.51 |
| 5 | `iterative:data_width=18,n_iter=29,angle_guard=3,frac_guard=0,rounding=round` | 8795 | 119 | 3.7 | 32 | 0.378 | 7.75e-05 (2^-13.65) | 13.65 |
| 6 | `iterative:data_width=18,n_iter=18,angle_guard=4,frac_guard=2,rounding=trunc` | 9149 | 125 | 5.4 | 21 | 0.259 | 4.84e-05 (2^-14.33) | 14.33 |
| 7 | `iterative:data_width=20,n_iter=30,angle_guard=1,frac_guard=2,rounding=trunc` | 10094 | 132 | 3.5 | 33 | 0.439 | 2.15e-05 (2^-15.51) | 15.51 |
| 8 | `iterative:data_width=19,n_iter=29,angle_guard=3,frac_guard=4,rounding=trunc` | 10531 | 134 | 3.4 | 32 | 0.436 | 1.69e-05 (2^-15.85) | 15.85 |
| 9 | `iterative:data_width=20,n_iter=29,angle_guard=3,frac_guard=3,rounding=trunc` | 10638 | 137 | 3.4 | 32 | 0.444 | 1.16e-05 (2^-16.39) | 16.39 |
| 10 | `iterative:data_width=23,n_iter=24,angle_guard=2,frac_guard=0,rounding=trunc` | 10884 | 146 | 3.8 | 27 | 0.392 | 5.84e-06 (2^-17.39) | 17.39 |
| 11 | `iterative:data_width=23,n_iter=29,angle_guard=0,frac_guard=1,rounding=trunc` | 11199 | 146 | 3.3 | 32 | 0.47 | 5.33e-06 (2^-17.52) | 17.52 |
| 12 | `iterative:data_width=23,n_iter=24,angle_guard=2,frac_guard=1,rounding=trunc` | 11290 | 148 | 3.8 | 27 | 0.401 | 3.08e-06 (2^-18.31) | 18.31 |
| 13 | `iterative:data_width=22,n_iter=24,angle_guard=3,frac_guard=3,rounding=trunc` | 11652 | 148 | 3.8 | 27 | 0.407 | 2.39e-06 (2^-18.67) | 18.67 |
| 14 | `iterative:data_width=23,n_iter=22,angle_guard=3,frac_guard=3,rounding=trunc` | 12031 | 153 | 4.0 | 25 | 0.39 | 1.45e-06 (2^-19.40) | 19.40 |
| 15 | `iterative:data_width=23,n_iter=25,angle_guard=3,frac_guard=3,rounding=trunc` | 12213 | 153 | 3.6 | 28 | 0.44 | 1.17e-06 (2^-19.71) | 19.71 |
| 16 | `iterative:data_width=26,n_iter=29,angle_guard=2,frac_guard=1,rounding=trunc` | 13010 | 164 | 3.0 | 32 | 0.537 | 4.7e-07 (2^-21.02) | 21.02 |
| 17 | `iterative:data_width=25,n_iter=25,angle_guard=3,frac_guard=3,rounding=trunc` | 13263 | 164 | 3.4 | 28 | 0.474 | 3.42e-07 (2^-21.48) | 21.48 |
| 18 | `iterative:data_width=27,n_iter=29,angle_guard=4,frac_guard=0,rounding=round` | 13584 | 170 | 2.8 | 32 | 0.558 | 2.03e-07 (2^-22.23) | 22.23 |
| 19 | `iterative:data_width=27,n_iter=27,angle_guard=3,frac_guard=2,rounding=trunc` | 14029 | 173 | 3.0 | 30 | 0.536 | 1.26e-07 (2^-22.92) | 22.92 |
| 20 | `iterative:data_width=27,n_iter=29,angle_guard=3,frac_guard=2,rounding=trunc` | 14114 | 173 | 2.8 | 32 | 0.574 | 1.14e-07 (2^-23.06) | 23.06 |
| 21 | `iterative:data_width=28,n_iter=29,angle_guard=4,frac_guard=1,rounding=trunc` | 14284 | 177 | 2.7 | 32 | 0.585 | 1.13e-07 (2^-23.08) | 23.08 |
| 22 | `iterative:data_width=28,n_iter=25,angle_guard=3,frac_guard=3,rounding=trunc` | 14838 | 181 | 3.1 | 28 | 0.526 | 8.56e-08 (2^-23.48) | 23.48 |
| 23 | `iterative:data_width=28,n_iter=25,angle_guard=4,frac_guard=3,rounding=trunc` | 14902 | 182 | 3.1 | 28 | 0.529 | 8.52e-08 (2^-23.48) | 23.48 |
| 24 | `iterative:data_width=28,n_iter=27,angle_guard=4,frac_guard=3,rounding=trunc` | 15084 | 182 | 2.9 | 30 | 0.57 | 4.35e-08 (2^-24.45) | 24.45 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The merged front is entirely iterative (15/15) and iterative already satisfies the 1 MSPS constraint with large margin, so the real trade-off is area versus accuracy_bits, driven only by data_width, n_iter, angle_guard, frac_guard and rounding. Round 2 therefore splits the iterative budget: the larger share refines the low-area corner around the current best 7014 um^2 where the min-area selection rule picks, and a second box pushes data_width/n_iter upward to extend the high-accuracy end of the front, which carries most of the hypervolume because the reference point sits at accuracy_bits = 10. unrolled_k gets only a small small-k probe, since it is structurally dominated here (same accuracy, k-fold datapath, and the throughput floor is already met). Round 3's reserved budget can then sweep the full iterative ranges to fill any gaps in the front.*)
- `iterative` (82 evals): data_width=10..15, n_iter=8..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Iterative owns the whole merged front (15/15) and already clears the 1 MSPS constraint by a wide margin, so area is set purely by the accuracy parameters. This tight box around the current best (7014 um^2, i.e. W near 12) is where the min-area selection rule lands, so it deserves the largest share to push the corner down and resolve the trunc-vs-round and guard-bit trade-offs.
- `unrolled_k` (18 evals): data_width=10..16, n_iter=8..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..3. *Why:* Small-k probe only: unrolled_k computes identical bits to iterative but replicates the datapath k times, so it should be strictly dominated for a spec whose throughput floor is only 1 MSPS. The previous 9 evals found 0 feasible, so this cheap box (k = 2..3, low width) checks whether any feasible unrolled_k point exists at all before the reserved full-range round.
- clamped by code: dropped duplicate family iterative

**Result (code):** 100 evaluations this round, 100 total; 31 feasible; hypervolume 5.061e+04 (n/a).

**LLM decision:** `map_front` — The feasible front is confined to a narrow slice of both objectives: area_um2 6997..10027 and accuracy_bits 10.6..11.6, while the registry allows data_width up to 28 and n_iter up to 30, so much higher accuracy is reachable. With the HV area reference at 40000, the (40000-area) factor is ~33000 for every front point, so extending accuracy_bits upward adds large HV rectangles; the current front stops at 11.55 bits. The throughput constraint is already trivially satisfied (best seen 14.8 MSPS vs >=1), and the summary reports no unexplored families, so pipelined/pipelined_m cannot help the min-area objective (same accuracy bits at strictly more registers). The remaining 100 evals are therefore best spent letting NSGA-II map the full ranges of the two families already on the front (iterative, unrolled_k), seeded with the current front, to cover the accuracy dimension and any lower-area corner before the final min-area selection.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 5.061e+04 (gain this round: n/a (first round)).
Feasible designs: 31 of 100 evaluations (27 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14.8
- max_abs_err <= 0.000976562: 69% violate; best seen 0.000333 (2^-11.55)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=0 rounding=round] area_um2=6997, accuracy_bits=10.6, ffs=101, throughput_msps=8.5, max_abs_err=0.000642 (2^-10.61), power_index=0.155
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=7042, accuracy_bits=10.6, ffs=100, throughput_msps=7.86, max_abs_err=0.000632 (2^-10.63), power_index=0.174
- iterative [data_width=15 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=7106, accuracy_bits=10.7, ffs=101, throughput_msps=7.56, max_abs_err=0.000599 (2^-10.71), power_index=0.176
- iterative [data_width=15 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=7357, accuracy_bits=10.8, ffs=104, throughput_msps=6.8, max_abs_err=0.000567 (2^-10.78), power_index=0.202
- iterative [data_width=15 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7677, accuracy_bits=11.5, ffs=106, throughput_msps=6.8, max_abs_err=0.000344 (2^-11.51), power_index=0.208
- unrolled_k [data_width=16 n_iter=18 angle_guard=1 frac_guard=1 rounding=trunc k=2] area_um2=10027, accuracy_bits=11.6, ffs=107, throughput_msps=6.21, max_abs_err=0.000333 (2^-11.55), power_index=0.142
Front coverage: area_um2 6997..10027 (HV reference 40000); accuracy_bits 10.6..11.6 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- iterative: 82 evals, 23 feasible; max throughput seen 14.8 MSPS; best accuracy 11.51 bits; best feasible area_um2=6997; feasible ranges: data_width 14..15, n_iter 13..18, angle_guard 0..2, frac_guard 0..2
- unrolled_k: 18 evals, 8 feasible; max throughput seen 11.2 MSPS; best accuracy 11.55 bits; best feasible area_um2=9258; feasible ranges: data_width 14..16, n_iter 15..18, angle_guard -1..2, frac_guard 0..2, k 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `iterative` (15 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (5 front designs; box front_anchored)
- `unrolled_k` (5 evals): data_width=15..28, n_iter=16..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (1 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 49 feasible; hypervolume 3.551e+05 (+601.5%).

**LLM decision:** `map_front` — The feasible front is entirely `iterative`: unrolled_k's best feasible area is 9258 um^2 vs 6997 um^2 for iterative, and its throughput edge (11.2 vs 8.5 MSPS) is worthless here because the only throughput constraint is >= 1 MSPS, which iterative already clears by ~8x; pipelined/pipelined_m register every stage (or every m stages) and can only be larger than the shared-datapath iterative design, so they cannot enter a min-area front. The min-area corner looks converged (W=15, n_iter=13 = the smallest feasible n_iter, angle_guard=2/frac_guard=0, err 6.42e-4 = 2^-10.61, i.e. only 0.6 bits of margin over the 2^-10 limit, and W=14 is evidently infeasible at low area since no front point has area < 6997). What is NOT converged is the rest of the curve: the front jumps 11.5 -> 13.7 bits between 7677 and 8795 um^2, and 18.3 -> 22.2 bits between 11290 and 13584 um^2, leaving large uncovered HV regions, while the front's area span (6997..13584) is only ~17% of the 40000 HV reference. With 80 of 200 evals left and this being the last funded round, a front-seeded NSGA-II over the full iterative ranges is the best use of the budget: it fills the accuracy gaps that drive hypervolume and simultaneously re-probes the low-area corner for anything below 6997 um^2 that the selection rule (min area_um2) would prefer.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 3.551e+05 (gain this round: +601.5%).
Feasible designs: 49 of 120 evaluations (45 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14.8
- max_abs_err <= 0.000976562: 59% violate; best seen 2.03e-07 (2^-22.23)

Pareto front (feasible, 10 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=0 rounding=round] area_um2=6997, accuracy_bits=10.6, ffs=101, throughput_msps=8.5, max_abs_err=0.000642 (2^-10.61), power_index=0.155
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=7042, accuracy_bits=10.6, ffs=100, throughput_msps=7.86, max_abs_err=0.000632 (2^-10.63), power_index=0.174
- iterative [data_width=15 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=7106, accuracy_bits=10.7, ffs=101, throughput_msps=7.56, max_abs_err=0.000599 (2^-10.71), power_index=0.176
- iterative [data_width=15 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=7357, accuracy_bits=10.8, ffs=104, throughput_msps=6.8, max_abs_err=0.000567 (2^-10.78), power_index=0.202
- iterative [data_width=15 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7677, accuracy_bits=11.5, ffs=106, throughput_msps=6.8, max_abs_err=0.000344 (2^-11.51), power_index=0.208
- iterative [data_width=18 n_iter=29 angle_guard=3 frac_guard=0 rounding=round] area_um2=8795, accuracy_bits=13.7, ffs=119, throughput_msps=3.68, max_abs_err=7.75e-05 (2^-13.65), power_index=0.378
- iterative [data_width=17 n_iter=29 angle_guard=3 frac_guard=3 rounding=round] area_um2=10853, accuracy_bits=14.4, ffs=120, throughput_msps=3.81, max_abs_err=4.73e-05 (2^-14.37), power_index=0.419
- iterative [data_width=23 n_iter=24 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=10884, accuracy_bits=17.4, ffs=146, throughput_msps=3.84, max_abs_err=5.84e-06 (2^-17.39), power_index=0.392
- iterative [data_width=23 n_iter=24 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=11290, accuracy_bits=18.3, ffs=148, throughput_msps=3.84, max_abs_err=3.08e-06 (2^-18.31), power_index=0.401
- iterative [data_width=27 n_iter=29 angle_guard=4 frac_guard=0 rounding=round] area_um2=13584, accuracy_bits=22.2, ffs=170, throughput_msps=2.75, max_abs_err=2.03e-07 (2^-22.23), power_index=0.558
Front coverage: area_um2 6997..13584 (HV reference 40000); accuracy_bits 10.6..22.2 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 97 evals, 36 feasible; max throughput seen 14.8 MSPS; best accuracy 22.23 bits; best feasible area_um2=6997; feasible ranges: data_width 14..27, n_iter 13..29, angle_guard 0..4, frac_guard 0..4
- unrolled_k: 23 evals, 13 feasible; max throughput seen 11.2 MSPS; best accuracy 18.42 bits; best feasible area_um2=9258; feasible ranges: data_width 14..28, n_iter 15..25, angle_guard -2..4, frac_guard 0..3, k 2..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `iterative` (80 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (10 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 125 feasible; hypervolume 4.168e+05 (+17.4%).

**LLM decision:** `stop` — Budget is exhausted (200/200 evals) and this is the final round, so only stop/infeasible apply. Infeasible is ruled out: 125 of 200 evaluations are feasible, 0% violate throughput_msps >= 1 (best 14.8 vs. required 1), and the accuracy constraint max_abs_err <= 0.000976562 is achievable with huge margin (best 4.35e-08 = 2^-24.45; even the selected design's 6.42e-04 passes). The Pareto front is well covered over the region that matters for the spec: area_um2 spans 6997..15084 against the HV reference of 40000, and accuracy_bits spans 10.6..24.5 against the HV reference of 10, with data_width 15..28 on the front. Hypervolume is still improving (+17.4% this round to 4.168e+05), but with no further evaluations available there is nothing more to gain. Under the selection rule (min area_um2), the pick is the iterative design [data_width=15, n_iter=13, angle_guard=2, frac_guard=0, rounding=round]: area_um2=6997, accuracy_bits=10.6 (max_abs_err=0.000642, satisfying the <=2^-10 limit), throughput 8.5 MSPS (>= 1 MSPS), 101 FFs, power_index 0.155.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 4.168e+05 (gain this round: +17.4%).
Feasible designs: 125 of 200 evaluations (110 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14.8
- max_abs_err <= 0.000976562: 38% violate; best seen 4.35e-08 (2^-24.45)

Pareto front (feasible, 25 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=0 rounding=round] area_um2=6997, accuracy_bits=10.6, ffs=101, throughput_msps=8.5, max_abs_err=0.000642 (2^-10.61), power_index=0.155
- iterative [data_width=15 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=7357, accuracy_bits=10.8, ffs=104, throughput_msps=6.8, max_abs_err=0.000567 (2^-10.78), power_index=0.202
- iterative [data_width=18 n_iter=29 angle_guard=3 frac_guard=0 rounding=round] area_um2=8795, accuracy_bits=13.7, ffs=119, throughput_msps=3.68, max_abs_err=7.75e-05 (2^-13.65), power_index=0.378
- iterative [data_width=19 n_iter=29 angle_guard=3 frac_guard=4 rounding=trunc] area_um2=10531, accuracy_bits=15.9, ffs=134, throughput_msps=3.45, max_abs_err=1.69e-05 (2^-15.85), power_index=0.436
- iterative [data_width=23 n_iter=29 angle_guard=0 frac_guard=1 rounding=trunc] area_um2=11199, accuracy_bits=17.5, ffs=146, throughput_msps=3.34, max_abs_err=5.33e-06 (2^-17.52), power_index=0.47
- iterative [data_width=22 n_iter=24 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=11652, accuracy_bits=18.7, ffs=148, throughput_msps=3.84, max_abs_err=2.39e-06 (2^-18.67), power_index=0.407
- iterative [data_width=26 n_iter=29 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=13010, accuracy_bits=21, ffs=164, throughput_msps=2.98, max_abs_err=4.7e-07 (2^-21.02), power_index=0.537
- iterative [data_width=27 n_iter=27 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=14029, accuracy_bits=22.9, ffs=173, throughput_msps=3.01, max_abs_err=1.26e-07 (2^-22.92), power_index=0.536
- iterative [data_width=28 n_iter=29 angle_guard=4 frac_guard=1 rounding=trunc] area_um2=14284, accuracy_bits=23.1, ffs=177, throughput_msps=2.69, max_abs_err=1.13e-07 (2^-23.08), power_index=0.585
- iterative [data_width=28 n_iter=27 angle_guard=4 frac_guard=3 rounding=trunc] area_um2=15084, accuracy_bits=24.5, ffs=182, throughput_msps=2.87, max_abs_err=4.35e-08 (2^-24.45), power_index=0.57
Front coverage: area_um2 6997..15084 (HV reference 40000); accuracy_bits 10.6..24.5 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 177 evals, 112 feasible; max throughput seen 14.8 MSPS; best accuracy 24.45 bits; best feasible area_um2=6997; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 23 evals, 13 feasible; max throughput seen 11.2 MSPS; best accuracy 18.42 bits; best feasible area_um2=9258; feasible ranges: data_width 14..28, n_iter 15..25, angle_guard -2..4, frac_guard 0..3, k 2..8
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 11388 in, 13828 out
- provider-reported cost: $0.0109
- full prompts and replies: `llm_trace.jsonl`

