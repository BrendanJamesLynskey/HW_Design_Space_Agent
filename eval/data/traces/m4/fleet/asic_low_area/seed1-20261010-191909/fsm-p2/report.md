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
`iterative:data_width=16,n_iter=23,angle_guard=0,frac_guard=0,rounding=trunc` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 7349 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1958 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 105 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 142 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 5.44 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 26 | exact: schedule |
| latency_ns | 184 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.264 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000965 (2^-10.02) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 15.8 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000359 (2^-11.44) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 5.88 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (21 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=16,n_iter=23,angle_guard=0,frac_guard=0,rounding=trunc` | 7349 | 105 | 5.4 | 26 | 0.264 | 0.000965 (2^-10.02) | 10.02 |
| 1 | `iterative:data_width=14,n_iter=15,angle_guard=2,frac_guard=3,rounding=trunc` | 7422 | 102 | 7.6 | 18 | 0.181 | 0.000513 (2^-10.93) | 10.93 |
| 2 | `iterative:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=trunc` | 7743 | 112 | 7.0 | 18 | 0.194 | 0.000307 (2^-11.67) | 11.67 |
| 3 | `iterative:data_width=16,n_iter=27,angle_guard=4,frac_guard=0,rounding=round` | 7918 | 109 | 4.1 | 30 | 0.322 | 0.000285 (2^-11.78) | 11.78 |
| 4 | `iterative:data_width=18,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc` | 8266 | 116 | 5.2 | 25 | 0.283 | 0.000243 (2^-12.01) | 12.01 |
| 5 | `iterative:data_width=18,n_iter=18,angle_guard=2,frac_guard=0,rounding=trunc` | 8356 | 118 | 5.8 | 21 | 0.241 | 0.000179 (2^-12.45) | 12.45 |
| 6 | `iterative:data_width=17,n_iter=18,angle_guard=1,frac_guard=2,rounding=trunc` | 8519 | 116 | 6.0 | 21 | 0.241 | 0.000137 (2^-12.84) | 12.84 |
| 7 | `iterative:data_width=19,n_iter=18,angle_guard=1,frac_guard=0,rounding=trunc` | 8733 | 123 | 5.8 | 21 | 0.251 | 7.8e-05 (2^-13.65) | 13.65 |
| 8 | `iterative:data_width=18,n_iter=18,angle_guard=2,frac_guard=2,rounding=trunc` | 9022 | 123 | 5.8 | 21 | 0.255 | 5.33e-05 (2^-14.20) | 14.20 |
| 9 | `iterative:data_width=19,n_iter=22,angle_guard=1,frac_guard=0,rounding=round` | 9060 | 123 | 4.9 | 25 | 0.304 | 4.26e-05 (2^-14.52) | 14.52 |
| 10 | `iterative:data_width=20,n_iter=18,angle_guard=2,frac_guard=0,rounding=trunc` | 9236 | 129 | 5.4 | 21 | 0.265 | 4.23e-05 (2^-14.53) | 14.53 |
| 11 | `iterative:data_width=19,n_iter=18,angle_guard=1,frac_guard=2,rounding=trunc` | 9399 | 127 | 5.6 | 21 | 0.264 | 3.99e-05 (2^-14.61) | 14.61 |
| 12 | `iterative:data_width=21,n_iter=17,angle_guard=0,frac_guard=0,rounding=trunc` | 9477 | 132 | 5.9 | 20 | 0.259 | 3.42e-05 (2^-14.83) | 14.83 |
| 13 | `iterative:data_width=19,n_iter=23,angle_guard=4,frac_guard=2,rounding=trunc` | 9771 | 130 | 4.2 | 26 | 0.338 | 2.56e-05 (2^-15.25) | 15.25 |
| 14 | `iterative:data_width=21,n_iter=28,angle_guard=0,frac_guard=0,rounding=round` | 10059 | 132 | 3.8 | 31 | 0.412 | 1.79e-05 (2^-15.77) | 15.77 |
| 15 | `iterative:data_width=20,n_iter=24,angle_guard=3,frac_guard=2,rounding=trunc` | 10220 | 135 | 4.1 | 27 | 0.365 | 1.42e-05 (2^-16.10) | 16.10 |
| 16 | `iterative:data_width=23,n_iter=23,angle_guard=0,frac_guard=0,rounding=trunc` | 10733 | 143 | 4.2 | 26 | 0.372 | 6.55e-06 (2^-17.22) | 17.22 |
| 17 | `iterative:data_width=23,n_iter=27,angle_guard=2,frac_guard=0,rounding=round` | 11211 | 146 | 3.5 | 30 | 0.441 | 2.9e-06 (2^-18.39) | 18.39 |
| 18 | `iterative:data_width=26,n_iter=28,angle_guard=4,frac_guard=0,rounding=round` | 12998 | 164 | 2.9 | 31 | 0.52 | 3.6e-07 (2^-21.40) | 21.40 |
| 19 | `iterative:data_width=27,n_iter=25,angle_guard=2,frac_guard=4,rounding=trunc` | 14668 | 176 | 3.1 | 28 | 0.516 | 1.34e-07 (2^-22.84) | 22.84 |
| 20 | `iterative:data_width=27,n_iter=29,angle_guard=2,frac_guard=4,rounding=trunc` | 14983 | 176 | 2.8 | 32 | 0.596 | 8.91e-08 (2^-23.42) | 23.42 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec's only binding constraint is max_abs_err <= 2^-10 (throughput >= 1 MSPS is trivially met by both families), and the HV reference point is (area 40000 um2, accuracy_bits 10), so useful designs live in area 7k-40k um2 with accuracy_bits >= 10. iterative dominates the merged front and holds the min-area design, so it gets the bulk of the budget, aimed at filling the accuracy axis above 10 bits rather than re-mining the already-dense low-area corner. unrolled_k gets a smaller share because it is under-sampled but still contributes front points, and its fixed-shift datapath may be competitive at high accuracy where iterative's barrel shifters get expensive. Both families get the full angle_guard/frac_guard/rounding ranges since those are cheap accuracy levers that directly move the accuracy_bits objective.*)
- `iterative` (70 evals): data_width=10..24, n_iter=8..26, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* iterative owns 23/25 of the merged front and the min-area feasible design (7106 um2), so it is the family that will decide the selection rule; the box keeps the low-area corner reachable (W=10, N=8) while extending data_width/n_iter upward so the front is mapped out to accuracy_bits well above the 10-bit constraint and up to the 40000 um2 HV area reference.
- `unrolled_k` (30 evals): data_width=10..24, n_iter=8..26, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* unrolled_k is heavily under-sampled (14 evals) yet still holds 2 of the 25 merged-front points, so its trade-off region is not yet mapped; a smaller share over the same accuracy box plus the full k range will either confirm those points or replace them with better ones.

**Result (code):** 100 evaluations this round, 100 total; 74 feasible; hypervolume 2.225e+05 (n/a).

**LLM decision:** `map_front` — The feasible front is only 10 designs, all `iterative`; `unrolled_k` is fully dominated (best feasible area 9127 > 7349, best accuracy 16.88 < 17.22 bits), and pipelined families only add per-stage registers, so they cannot win on the min-area objective. The throughput constraint is trivially satisfied (best seen 13 MSPS vs 1 required), so area and accuracy are the only live axes. The front spans area 7349..10733 against an HV reference of 40000 and accuracy 10..17.2 against a reference of 10 — i.e. it covers only a small slice of the area range, and the HV (2.225e5) is dominated by the single highest-accuracy point's box (≈(40000-7349)*(17.2-10)), so pushing accuracy higher at low area is the biggest HV lever. The registry allows data_width up to 28 and n_iter up to 30, well beyond the front's 23/23, so there is clear unexplored headroom. With 100 evals left in a single round, a seeded NSGA-II coverage search over the full ranges of the family on the front is the best use of the budget: it keeps the min-area corner (the selection rule's pick) while filling the curve and extending accuracy.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 2.225e+05 (gain this round: n/a (first round)).
Feasible designs: 74 of 100 evaluations (66 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 13
- max_abs_err <= 0.000976562: 26% violate; best seen 6.55e-06 (2^-17.22)

Pareto front (feasible, 10 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=16 n_iter=23 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=7349, accuracy_bits=10, ffs=105, throughput_msps=5.44, max_abs_err=0.000965 (2^-10.02), power_index=0.264
- iterative [data_width=14 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=7422, accuracy_bits=10.9, ffs=102, throughput_msps=7.56, max_abs_err=0.000513 (2^-10.93), power_index=0.181
- iterative [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=7743, accuracy_bits=11.7, ffs=112, throughput_msps=7.01, max_abs_err=0.000307 (2^-11.67), power_index=0.194
- iterative [data_width=18 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=8266, accuracy_bits=12, ffs=116, throughput_msps=5.24, max_abs_err=0.000243 (2^-12.01), power_index=0.283
- iterative [data_width=19 n_iter=16 angle_guard=-2 frac_guard=0 rounding=trunc] area_um2=8370, accuracy_bits=12.4, ffs=118, throughput_msps=6.64, max_abs_err=0.000185 (2^-12.40), power_index=0.219
- iterative [data_width=19 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=8742, accuracy_bits=13.2, ffs=121, throughput_msps=5.05, max_abs_err=0.000103 (2^-13.24), power_index=0.298
- iterative [data_width=20 n_iter=18 angle_guard=-2 frac_guard=0 rounding=trunc] area_um2=8982, accuracy_bits=13.4, ffs=125, throughput_msps=5.8, max_abs_err=9.43e-05 (2^-13.37), power_index=0.257
- iterative [data_width=18 n_iter=23 angle_guard=4 frac_guard=2 rounding=trunc] area_um2=9270, accuracy_bits=14.2, ffs=125, throughput_msps=4.38, max_abs_err=5.37e-05 (2^-14.18), power_index=0.322
- iterative [data_width=19 n_iter=23 angle_guard=4 frac_guard=2 rounding=trunc] area_um2=9771, accuracy_bits=15.3, ffs=130, throughput_msps=4.24, max_abs_err=2.56e-05 (2^-15.25), power_index=0.338
- iterative [data_width=23 n_iter=23 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=10733, accuracy_bits=17.2, ffs=143, throughput_msps=4.24, max_abs_err=6.55e-06 (2^-17.22), power_index=0.372
Front coverage: area_um2 7349..10733 (HV reference 40000); accuracy_bits 10..17.2 (HV reference 10); data_width on the front 14..23 (registry 8..28).

Per family:
- iterative: 70 evals, 54 feasible; max throughput seen 13 MSPS; best accuracy 17.22 bits; best feasible area_um2=7349; feasible ranges: data_width 14..24, n_iter 15..26, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 30 evals, 20 feasible; max throughput seen 10.5 MSPS; best accuracy 16.88 bits; best feasible area_um2=9127; feasible ranges: data_width 15..23, n_iter 12..26, angle_guard -2..4, frac_guard 0..4, k 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `iterative` (20 evals): data_width=13..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (10 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 88 feasible; hypervolume 3.361e+05 (+51.1%).

**LLM decision:** `map_front` — Round 2 left the front well-populated on the accuracy axis (10.0 to 21.4 bits, i.e. essentially the full feasible span) but only 13 designs, and the high-accuracy end stops at 21.4 bits / area 12998 while the registry still allows data_width up to 28 and n_iter up to 30 — so the right-hand (high-accuracy) part of the trade-off curve is under-sampled and there is clear hypervolume left against the (40000, 10) reference. The low-area end is also pinned right against the constraint boundary (best design area 7349 at accuracy 10.02 bits, max_abs_err 0.000965 vs limit 0.000976562), so the exact minimum-area feasible corner is fragile and worth re-mapping. Both families found on the front (iterative, unrolled_k) should be swept over their full ranges seeded with the current front, which is exactly the reserved mapping step. With 80 of 200 evals still available and 2 rounds left, spending this round on a seeded NSGA-II front map is the highest-value use of budget before any final refinement.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 3.361e+05 (gain this round: +51.1%).
Feasible designs: 88 of 120 evaluations (77 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 13
- max_abs_err <= 0.000976562: 27% violate; best seen 3.6e-07 (2^-21.40)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=16 n_iter=23 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=7349, accuracy_bits=10, ffs=105, throughput_msps=5.44, max_abs_err=0.000965 (2^-10.02), power_index=0.264
- iterative [data_width=14 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=7422, accuracy_bits=10.9, ffs=102, throughput_msps=7.56, max_abs_err=0.000513 (2^-10.93), power_index=0.181
- iterative [data_width=18 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=8266, accuracy_bits=12, ffs=116, throughput_msps=5.24, max_abs_err=0.000243 (2^-12.01), power_index=0.283
- iterative [data_width=19 n_iter=16 angle_guard=-2 frac_guard=0 rounding=trunc] area_um2=8370, accuracy_bits=12.4, ffs=118, throughput_msps=6.64, max_abs_err=0.000185 (2^-12.40), power_index=0.219
- iterative [data_width=19 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=8742, accuracy_bits=13.2, ffs=121, throughput_msps=5.05, max_abs_err=0.000103 (2^-13.24), power_index=0.298
- iterative [data_width=20 n_iter=19 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=9221, accuracy_bits=14.4, ffs=128, throughput_msps=5.35, max_abs_err=4.51e-05 (2^-14.44), power_index=0.276
- iterative [data_width=21 n_iter=17 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=9477, accuracy_bits=14.8, ffs=132, throughput_msps=5.89, max_abs_err=3.42e-05 (2^-14.83), power_index=0.259
- iterative [data_width=19 n_iter=23 angle_guard=4 frac_guard=2 rounding=trunc] area_um2=9771, accuracy_bits=15.3, ffs=130, throughput_msps=4.24, max_abs_err=2.56e-05 (2^-15.25), power_index=0.338
- iterative [data_width=23 n_iter=23 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=10733, accuracy_bits=17.2, ffs=143, throughput_msps=4.24, max_abs_err=6.55e-06 (2^-17.22), power_index=0.372
- iterative [data_width=26 n_iter=28 angle_guard=4 frac_guard=0 rounding=round] area_um2=12998, accuracy_bits=21.4, ffs=164, throughput_msps=2.92, max_abs_err=3.6e-07 (2^-21.40), power_index=0.52
Front coverage: area_um2 7349..12998 (HV reference 40000); accuracy_bits 10..21.4 (HV reference 10); data_width on the front 14..26 (registry 8..28).

Per family:
- iterative: 90 evals, 68 feasible; max throughput seen 13 MSPS; best accuracy 21.40 bits; best feasible area_um2=7349; feasible ranges: data_width 14..26, n_iter 13..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 30 evals, 20 feasible; max throughput seen 10.5 MSPS; best accuracy 16.88 bits; best feasible area_um2=9127; feasible ranges: data_width 15..23, n_iter 12..26, angle_guard -2..4, frac_guard 0..4, k 2..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `iterative` (80 evals): data_width=13..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (13 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 159 feasible; hypervolume 3.898e+05 (+16.0%).

**LLM decision:** `stop` — Budget is exhausted (200/200 evals) and this is the capped final round, so the choice is between `stop` and `infeasible`. It is not infeasible: 159/200 evaluations are feasible, 140 unique, and neither constraint is binding at the front — 0% of evaluations violate throughput_msps >= 1 (best seen 13 MSPS) and only 20% violate the error bound, with best seen max_abs_err 8.91e-08 (2^-23.42). The feasible Pareto front spans area_um2 7349..14983 against the HV reference 40000 and accuracy_bits 10..23.4 against reference 10, i.e. the objective range is well covered, and hypervolume is still gaining (+16.0% this round, HV 3.898e+05), from an already dense front of 21 designs. The selection rule (min area_um2) is satisfied by a design on the front: iterative [data_width=16 n_iter=23 angle_guard=0 frac_guard=0 rounding=trunc] at area_um2=7349, ffs=105, throughput_msps=5.44, max_abs_err=0.000965 (2^-10.02) — inside the 2^-10 error budget with ~1.2% margin and 5.4x the required 1 MSPS. Both explored families contribute (iterative best area 7349; unrolled_k best 9127, best accuracy 16.88 bits), so there is no unexplored family that could plausibly push the low-area corner below the current front — and the full-range mapping pass for the families on the front was already spent within the budget. Further rounds would only refine accuracy on the already-covered high-accuracy tail, which the area-minimising selection rule does not pick. Stop here; the front is the deliverable and the min-area point meets the spec.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 3.898e+05 (gain this round: +16.0%).
Feasible designs: 159 of 200 evaluations (140 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 13
- max_abs_err <= 0.000976562: 20% violate; best seen 8.91e-08 (2^-23.42)

Pareto front (feasible, 21 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=16 n_iter=23 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=7349, accuracy_bits=10, ffs=105, throughput_msps=5.44, max_abs_err=0.000965 (2^-10.02), power_index=0.264
- iterative [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=7743, accuracy_bits=11.7, ffs=112, throughput_msps=7.01, max_abs_err=0.000307 (2^-11.67), power_index=0.194
- iterative [data_width=18 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=8266, accuracy_bits=12, ffs=116, throughput_msps=5.24, max_abs_err=0.000243 (2^-12.01), power_index=0.283
- iterative [data_width=19 n_iter=18 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=8733, accuracy_bits=13.6, ffs=123, throughput_msps=5.8, max_abs_err=7.8e-05 (2^-13.65), power_index=0.251
- iterative [data_width=19 n_iter=22 angle_guard=1 frac_guard=0 rounding=round] area_um2=9060, accuracy_bits=14.5, ffs=123, throughput_msps=4.87, max_abs_err=4.26e-05 (2^-14.52), power_index=0.304
- iterative [data_width=19 n_iter=18 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=9399, accuracy_bits=14.6, ffs=127, throughput_msps=5.61, max_abs_err=3.99e-05 (2^-14.61), power_index=0.264
- iterative [data_width=19 n_iter=23 angle_guard=4 frac_guard=2 rounding=trunc] area_um2=9771, accuracy_bits=15.3, ffs=130, throughput_msps=4.24, max_abs_err=2.56e-05 (2^-15.25), power_index=0.338
- iterative [data_width=23 n_iter=23 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=10733, accuracy_bits=17.2, ffs=143, throughput_msps=4.24, max_abs_err=6.55e-06 (2^-17.22), power_index=0.372
- iterative [data_width=26 n_iter=28 angle_guard=4 frac_guard=0 rounding=round] area_um2=12998, accuracy_bits=21.4, ffs=164, throughput_msps=2.92, max_abs_err=3.6e-07 (2^-21.40), power_index=0.52
- iterative [data_width=27 n_iter=29 angle_guard=2 frac_guard=4 rounding=trunc] area_um2=14983, accuracy_bits=23.4, ffs=176, throughput_msps=2.75, max_abs_err=8.91e-08 (2^-23.42), power_index=0.596
Front coverage: area_um2 7349..14983 (HV reference 40000); accuracy_bits 10..23.4 (HV reference 10); data_width on the front 14..27 (registry 8..28).

Per family:
- iterative: 170 evals, 139 feasible; max throughput seen 13 MSPS; best accuracy 23.42 bits; best feasible area_um2=7349; feasible ranges: data_width 14..27, n_iter 13..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 30 evals, 20 feasible; max throughput seen 10.5 MSPS; best accuracy 16.88 bits; best feasible area_um2=9127; feasible ranges: data_width 15..23, n_iter 12..26, angle_guard -2..4, frac_guard 0..4, k 2..8
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 11685 in, 10090 out
- provider-reported cost: $0.0088
- full prompts and replies: `llm_trace.jsonl`

