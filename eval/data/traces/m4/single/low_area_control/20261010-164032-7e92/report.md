# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 4 round(s).  
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
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=15,n_iter=16,angle_guard=1,frac_guard=1,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 170 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 94 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 10.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 19 | exact: schedule |
| latency_ns | 95.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.189 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000594 (2^-10.72) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 4.86 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000154 (2^-12.66) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.26 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.7 | exact: bit-accurate model, exhaustive (32768 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 19 cycles, a new input every 19 cycle(s). DDS tone from its exact outputs: SFDR 85.3 dBc, SNR 74.0 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (34 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=16,angle_guard=1,frac_guard=1,rounding=trunc` | 170 | 94 | 10.4 | 19 | 0.189 | 0.000594 (2^-10.72) | 10.72 |
| 1 | `iterative:data_width=15,n_iter=17,angle_guard=3,frac_guard=0,rounding=round` | 182 | 95 | 8.1 | 20 | 0.208 | 0.000546 (2^-10.84) | 10.84 |
| 2 | `iterative:data_width=17,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc` | 193 | 104 | 11.0 | 18 | 0.201 | 0.000219 (2^-12.16) | 12.16 |
| 3 | `iterative:data_width=18,n_iter=16,angle_guard=1,frac_guard=0,rounding=trunc` | 195 | 107 | 10.2 | 19 | 0.216 | 0.000179 (2^-12.45) | 12.45 |
| 4 | `iterative:data_width=17,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 203 | 106 | 10.2 | 19 | 0.22 | 0.000145 (2^-12.76) | 12.76 |
| 5 | `iterative:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc` | 204 | 109 | 10.8 | 18 | 0.212 | 0.000127 (2^-12.95) | 12.95 |
| 6 | `iterative:data_width=18,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 214 | 111 | 10.2 | 19 | 0.232 | 8.08e-05 (2^-13.60) | 13.60 |
| 7 | `iterative:data_width=21,n_iter=15,angle_guard=1,frac_guard=0,rounding=trunc` | 229 | 122 | 10.8 | 18 | 0.238 | 7.32e-05 (2^-13.74) | 13.74 |
| 8 | `iterative:data_width=17,n_iter=21,angle_guard=4,frac_guard=3,rounding=trunc` | 249 | 112 | 6.6 | 24 | 0.326 | 6.86e-05 (2^-13.83) | 13.83 |
| 9 | `iterative:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 261 | 112 | 10.2 | 19 | 0.267 | 5.46e-05 (2^-14.16) | 14.16 |
| 10 | `iterative:data_width=19,n_iter=17,angle_guard=2,frac_guard=2,rounding=trunc` | 260 | 118 | 7.9 | 20 | 0.284 | 3.81e-05 (2^-14.68) | 14.68 |
| 11 | `iterative:data_width=20,n_iter=19,angle_guard=3,frac_guard=1,rounding=trunc` | 264 | 122 | 7.1 | 22 | 0.319 | 2.4e-05 (2^-15.35) | 15.35 |
| 12 | `iterative:data_width=21,n_iter=21,angle_guard=1,frac_guard=0,rounding=trunc` | 266 | 123 | 6.6 | 24 | 0.352 | 2.36e-05 (2^-15.37) | 15.37 |
| 13 | `iterative:data_width=19,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc` | 280 | 120 | 5.7 | 28 | 0.422 | 2.18e-05 (2^-15.49) | 15.49 |
| 14 | `iterative:data_width=21,n_iter=22,angle_guard=1,frac_guard=0,rounding=round` | 280 | 123 | 6.4 | 25 | 0.379 | 1.21e-05 (2^-16.34) | 16.34 |
| 15 | `iterative:data_width=21,n_iter=22,angle_guard=2,frac_guard=0,rounding=round` | 282 | 124 | 6.2 | 25 | 0.382 | 1.15e-05 (2^-16.41) | 16.41 |
| 16 | `iterative:data_width=20,n_iter=25,angle_guard=3,frac_guard=3,rounding=trunc` | 301 | 126 | 5.6 | 28 | 0.45 | 1e-05 (2^-16.61) | 16.61 |
| 17 | `iterative:data_width=22,n_iter=27,angle_guard=2,frac_guard=1,rounding=trunc` | 303 | 131 | 5.2 | 30 | 0.49 | 7.69e-06 (2^-16.99) | 16.99 |
| 18 | `iterative:data_width=22,n_iter=27,angle_guard=4,frac_guard=1,rounding=trunc` | 306 | 133 | 5.2 | 30 | 0.496 | 6.68e-06 (2^-17.19) | 17.19 |
| 19 | `iterative:data_width=23,n_iter=23,angle_guard=3,frac_guard=0,rounding=trunc` | 305 | 135 | 6.0 | 26 | 0.43 | 5.84e-06 (2^-17.39) | 17.39 |
| 20 | `iterative:data_width=23,n_iter=21,angle_guard=3,frac_guard=0,rounding=trunc` | 305 | 135 | 6.5 | 24 | 0.397 | 5.84e-06 (2^-17.39) | 17.39 |
| 21 | `iterative:data_width=23,n_iter=22,angle_guard=3,frac_guard=0,rounding=trunc` | 305 | 135 | 6.2 | 25 | 0.414 | 5.84e-06 (2^-17.39) | 17.39 |
| 22 | `iterative:data_width=23,n_iter=22,angle_guard=2,frac_guard=0,rounding=round` | 317 | 134 | 6.2 | 25 | 0.424 | 2.9e-06 (2^-18.39) | 18.39 |
| 23 | `iterative:data_width=24,n_iter=27,angle_guard=2,frac_guard=0,rounding=round` | 339 | 139 | 5.2 | 30 | 0.539 | 1.57e-06 (2^-19.28) | 19.28 |
| 24 | `iterative:data_width=26,n_iter=27,angle_guard=3,frac_guard=0,rounding=trunc` | 363 | 150 | 5.1 | 30 | 0.58 | 7.68e-07 (2^-20.31) | 20.31 |
| 25 | `iterative:data_width=26,n_iter=25,angle_guard=4,frac_guard=0,rounding=trunc` | 365 | 151 | 5.5 | 28 | 0.544 | 7.61e-07 (2^-20.32) | 20.32 |
| 26 | `iterative:data_width=26,n_iter=27,angle_guard=0,frac_guard=0,rounding=round` | 373 | 147 | 5.2 | 30 | 0.587 | 6.06e-07 (2^-20.65) | 20.65 |
| 27 | `iterative:data_width=26,n_iter=27,angle_guard=1,frac_guard=0,rounding=round` | 375 | 148 | 5.1 | 30 | 0.59 | 3.95e-07 (2^-21.27) | 21.27 |
| 28 | `iterative:data_width=26,n_iter=30,angle_guard=3,frac_guard=0,rounding=round` | 380 | 150 | 4.6 | 33 | 0.658 | 3.6e-07 (2^-21.40) | 21.40 |
| 29 | `iterative:data_width=26,n_iter=24,angle_guard=3,frac_guard=2,rounding=trunc` | 389 | 154 | 5.7 | 27 | 0.552 | 3.21e-07 (2^-21.57) | 21.57 |
| 30 | `iterative:data_width=28,n_iter=27,angle_guard=0,frac_guard=0,rounding=trunc` | 396 | 157 | 5.1 | 30 | 0.624 | 2.45e-07 (2^-21.96) | 21.96 |
| 31 | `iterative:data_width=28,n_iter=27,angle_guard=4,frac_guard=1,rounding=trunc` | 420 | 163 | 5.0 | 30 | 0.659 | 9.79e-08 (2^-23.28) | 23.28 |
| 32 | `iterative:data_width=28,n_iter=28,angle_guard=4,frac_guard=1,rounding=trunc` | 420 | 163 | 4.9 | 31 | 0.681 | 9.79e-08 (2^-23.28) | 23.28 |
| 33 | `iterative:data_width=28,n_iter=30,angle_guard=4,frac_guard=4,rounding=trunc` | 481 | 169 | 4.6 | 33 | 0.808 | 2.61e-08 (2^-25.19) | 25.19 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >= 1 MSPS throughput, which rules out iterative and unrolled_k (they produce one result every several cycles, so throughput = Fmax/cycles_per_result; even at high Fmax, e.g. 200 MHz / 13 cycles ~ 15 MSPS is fine, but the area is dominated by the shared datapath and the constraint is easily met). However, the primary objective is minimising luts_plus_ffs, and pipelined_m with m>1 offers the best area/throughput trade-off. I focus 100% of the first round on pipelined and pipelined_m because they are the only families that guarantee 1 result/cycle throughput independent of Fmax, making them the natural candidates for the Pareto front. W=12..16 and N=10..14 are chosen because: (1) max_abs_err <= 2^-10 requires sufficient precision; with W=12, N=10, truncation, the error is typically around 2^-10 to 2^-11, so this range brackets the feasibility boundary; (2) angle_guard 0..2 and frac_guard 0..2 explore the accuracy/area trade-off without wasting budget on extreme values that either blow up area or are unnecessary. Rounding is included as a categorical choice since it affects error at no significant area cost. The 50/50 split between pipelined and pipelined_m ensures we map both ends of the area trade-off: pipelined anchors the high-area/high-timing end, pipelined_m anchors the low-area end. This should reveal the Pareto front shape in round 1, allowing round 2 to refine ranges or add iterative/unrolled_k if they turn out to be competitive on area (they have fewer FFs but lower throughput, so they may still meet 1 MSPS if Fmax is high enough).*)
- `pipelined` (50 evals): data_width=12..16, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Only pipelined/pipelined_m give 1 result/cycle, so throughput_msps >= 1 requires Fmax >= 1 MHz (trivially true) but the real area/latency trade-off lives here. Full pipelining has the most registers (worst area) but the best timing; it anchors the high-accuracy/high-area end of the front and confirms the feasibility of the throughput constraint. Narrowing W to 12..16 and N to 10..14 keeps max_abs_err <= 2^-10 (0.000976562) while exploring the area/accuracy trade-off that the spec cares about.
- `pipelined_m` (50 evals): data_width=12..16, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m also gives 1 result/cycle (meets throughput) but registers every m stages, cutting FF count substantially versus full pipelining while keeping timing reasonable. This is the most promising family for minimising luts_plus_ffs under the throughput constraint. m=2..4 covers the sweet spot between area savings and Fmax; W and N ranges match pipelined to keep accuracy within 2^-10.

**Result (code):** 100 evaluations this round, 100 total; 52 feasible; hypervolume 772.7 (n/a).

**LLM decision:** `add_family` — The current front is dominated by pipelined_m designs (best area 868) which are significantly cheaper than the pipelined designs (best area 1350). However, we have not yet explored the `iterative` and `unrolled_k` families. Given the objective is to minimize area (luts_plus_ffs) and the throughput constraint is loose (>= 1 MSPS, while current designs achieve ~100-280 MSPS), the iterative family (1 micro-rotation/cycle, shared datapath) is a strong candidate for lower area than the pipelined variants, provided it can meet the throughput and accuracy constraints. The iterative family typically has lower resource usage than pipelined versions because it reuses the datapath, at the cost of higher latency and lower throughput. Since the throughput requirement is low (1 MSPS) and the current Fmax is high (~100-280 MHz), an iterative design with a reasonable data_width and n_iter should easily meet the throughput constraint while potentially offering a much smaller area footprint than the current best of 868. Exploring this family is crucial to map the true Pareto front for the area objective.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 772.7 (gain this round: n/a (first round)).
Feasible designs: 52 of 100 evaluations (35 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 48% violate; best seen 0.000209 (2^-12.22)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=868, accuracy_bits=10.5, luts=666, ffs=202, throughput_msps=97.8, max_abs_err=0.00071 (2^-10.46), power_index=0.0326
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=935, accuracy_bits=10.7, luts=723, ffs=212, throughput_msps=97.8, max_abs_err=0.000602 (2^-10.70), power_index=0.0352
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=949, accuracy_bits=10.8, luts=734, ffs=215, throughput_msps=97.8, max_abs_err=0.000548 (2^-10.83), power_index=0.0357
- pipelined_m [data_width=16 n_iter=13 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1057, accuracy_bits=11.4, luts=785, ffs=272, throughput_msps=97.8, max_abs_err=0.000358 (2^-11.45), power_index=0.0398
- pipelined [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=1601, accuracy_bits=11.5, luts=786, ffs=815, throughput_msps=273, max_abs_err=0.000344 (2^-11.50), power_index=0.0602
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=1629, accuracy_bits=11.5, luts=800, ffs=829, throughput_msps=273, max_abs_err=0.000338 (2^-11.53), power_index=0.0613
- pipelined [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=round] luts_plus_ffs=1637, accuracy_bits=11.7, luts=820, ffs=817, throughput_msps=273, max_abs_err=0.000311 (2^-11.65), power_index=0.0616
- pipelined [data_width=16 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=1653, accuracy_bits=11.7, luts=813, ffs=839, throughput_msps=273, max_abs_err=0.000311 (2^-11.65), power_index=0.0622
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=1665, accuracy_bits=12.2, luts=834, ffs=831, throughput_msps=273, max_abs_err=0.000209 (2^-12.22), power_index=0.0626
Front coverage: luts_plus_ffs 868..1665 (HV reference 1500); accuracy_bits 10.5..12.2 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- pipelined: 50 evals, 28 feasible; max throughput seen 282 MSPS; best accuracy 12.22 bits; best feasible luts_plus_ffs=1350; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 24 feasible; max throughput seen 178 MSPS; best accuracy 11.45 bits; best feasible luts_plus_ffs=868; feasible ranges: data_width 14..16, n_iter 12..13, angle_guard 1..2, frac_guard 1..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Add the iterative family to the search space. The current front is limited to pipelined and pipelined_m. The iterative family is not yet explored and is likely to offer better area efficiency for the given loose throughput constraint.*)
- `iterative` (100 evals): data_width=12..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Explore the iterative family to find potentially lower-area designs that meet the loose throughput constraint (>=1 MSPS) and accuracy constraint (<= 2^-10). The current best area is 868 from pipelined_m; iterative designs often have lower area due to datapath sharing.

**Result (code):** 100 evaluations this round, 200 total; 94 feasible; hypervolume 4960 (+541.8%).

**LLM decision:** `add_family` — The current Pareto front is dominated by the `iterative` family, which achieves the lowest area (264 LUTs+FFs) but has a throughput ceiling of ~15 MSPS. While this meets the >= 1 MSPS constraint, the `pipelined` and `pipelined_m` families are significantly more expensive (868-1350 LUTs+FFs) for similar or worse accuracy. The `unrolled_k` family has not been explored yet. It offers a middle ground: higher throughput than `iterative` (due to parallel micro-rotations) but potentially lower area than fully pipelined designs (due to shared datapath/FSM). Given that area is the primary objective and we have 200 evaluations left, exploring `unrolled_k` is the most logical step to find a design that might offer better throughput than `iterative` without the area penalty of `pipelined`, or to confirm that `iterative` is indeed the optimal area solution.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 4960 (gain this round: +541.8%).
Feasible designs: 94 of 200 evaluations (68 unique).
Families explored so far: iterative, pipelined, pipelined_m. Not yet explored: unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 53% violate; best seen 5.46e-05 (2^-14.16)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=264, accuracy_bits=10.7, luts=170, ffs=94, throughput_msps=10.4, max_abs_err=0.000594 (2^-10.72), power_index=0.189
- iterative [data_width=18 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=287, accuracy_bits=10.8, luts=181, ffs=106, throughput_msps=13.2, max_abs_err=0.000575 (2^-10.76), power_index=0.162
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=297, accuracy_bits=12.2, luts=193, ffs=104, throughput_msps=11, max_abs_err=0.000219 (2^-12.16), power_index=0.201
- iterative [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=302, accuracy_bits=12.4, luts=195, ffs=107, throughput_msps=10.2, max_abs_err=0.000179 (2^-12.45), power_index=0.216
- iterative [data_width=17 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=308, accuracy_bits=12.8, luts=203, ffs=106, throughput_msps=10.2, max_abs_err=0.000145 (2^-12.76), power_index=0.22
- iterative [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=313, accuracy_bits=12.9, luts=204, ffs=109, throughput_msps=10.8, max_abs_err=0.000127 (2^-12.95), power_index=0.212
- iterative [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=325, accuracy_bits=13.6, luts=214, ffs=111, throughput_msps=10.2, max_abs_err=8.08e-05 (2^-13.60), power_index=0.232
- iterative [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=370, accuracy_bits=13.7, luts=259, ffs=111, throughput_msps=10.2, max_abs_err=7.47e-05 (2^-13.71), power_index=0.265
- iterative [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=373, accuracy_bits=14.2, luts=261, ffs=112, throughput_msps=10.2, max_abs_err=5.46e-05 (2^-14.16), power_index=0.267
Front coverage: luts_plus_ffs 264..373 (HV reference 1500); accuracy_bits 10.7..14.2 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 100 evals, 42 feasible; max throughput seen 15.3 MSPS; best accuracy 14.16 bits; best feasible luts_plus_ffs=264; feasible ranges: data_width 13..18, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
- pipelined: 50 evals, 28 feasible; max throughput seen 282 MSPS; best accuracy 12.22 bits; best feasible luts_plus_ffs=1350; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 24 feasible; max throughput seen 178 MSPS; best accuracy 11.45 bits; best feasible luts_plus_ffs=868; feasible ranges: data_width 14..16, n_iter 12..13, angle_guard 1..2, frac_guard 1..2, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The current Pareto front is dominated by the `iterative` family, which achieves the lowest area (264 LUTs+FFs) but has a throughput ceiling of ~15 MSPS. While this meets the >= 1 MSPS constraint, the `pipelined` and `pipelined_m` families are significantly more expensive (868-1350 LUTs+FFs) for similar or worse accuracy. The `unrolled_k` family has not been explored yet. It offers a middle ground: higher throughput than `iterative` (due to parallel micro-rotations) but potentially lower area than fully pipelined designs (due to shared datapath/FSM). Given that area is the primary objective and we have 200 evaluations left, exploring `unrolled_k` is the most logical step to find a design that might offer better throughput than `iterative` without the area penalty of `pipelined`, or to confirm that `iterative` is indeed the optimal area solution.*)
- `unrolled_k` (40 evals): data_width=15..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Explore unrolled_k to find a potential area/throughput sweet spot between iterative and pipelined. Ranges are narrowed to the proven feasible regions of iterative (data_width 15-18, n_iter 12-16) to focus the search on viable accuracy/area trade-offs.

**Result (code):** 40 evaluations this round, 240 total; 133 feasible; hypervolume 4960 (+0.0%).

**LLM decision:** `stop` — The Pareto front is well-established and dominated by the `iterative` family, which offers the best area (luts_plus_ffs=264) while meeting the throughput constraint (10.4 MSPS >= 1) and accuracy constraint (10.7 bits > 10). The `pipelined` and `pipelined_m` families are significantly larger (868-1350 LUTs+FFs) and do not improve the hypervolume in the low-area region. Since this is the final round and the front covers the relevant trade-off space for the 'low_area_control' spec (minimizing area while meeting 1 MSPS and 2^-10 error), further exploration would not yield a better design for the selection rule (min luts_plus_ffs). The best design is `iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc]` with 264 LUTs+FFs.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 4960 (gain this round: +0.0%).
Feasible designs: 133 of 240 evaluations (100 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 45% violate; best seen 5.46e-05 (2^-14.16)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=264, accuracy_bits=10.7, luts=170, ffs=94, throughput_msps=10.4, max_abs_err=0.000594 (2^-10.72), power_index=0.189
- iterative [data_width=18 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=287, accuracy_bits=10.8, luts=181, ffs=106, throughput_msps=13.2, max_abs_err=0.000575 (2^-10.76), power_index=0.162
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=297, accuracy_bits=12.2, luts=193, ffs=104, throughput_msps=11, max_abs_err=0.000219 (2^-12.16), power_index=0.201
- iterative [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=302, accuracy_bits=12.4, luts=195, ffs=107, throughput_msps=10.2, max_abs_err=0.000179 (2^-12.45), power_index=0.216
- iterative [data_width=17 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=308, accuracy_bits=12.8, luts=203, ffs=106, throughput_msps=10.2, max_abs_err=0.000145 (2^-12.76), power_index=0.22
- iterative [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=313, accuracy_bits=12.9, luts=204, ffs=109, throughput_msps=10.8, max_abs_err=0.000127 (2^-12.95), power_index=0.212
- iterative [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=325, accuracy_bits=13.6, luts=214, ffs=111, throughput_msps=10.2, max_abs_err=8.08e-05 (2^-13.60), power_index=0.232
- iterative [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=370, accuracy_bits=13.7, luts=259, ffs=111, throughput_msps=10.2, max_abs_err=7.47e-05 (2^-13.71), power_index=0.265
- iterative [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=373, accuracy_bits=14.2, luts=261, ffs=112, throughput_msps=10.2, max_abs_err=5.46e-05 (2^-14.16), power_index=0.267
Front coverage: luts_plus_ffs 264..373 (HV reference 1500); accuracy_bits 10.7..14.2 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 100 evals, 42 feasible; max throughput seen 15.3 MSPS; best accuracy 14.16 bits; best feasible luts_plus_ffs=264; feasible ranges: data_width 13..18, n_iter 12..16, angle_guard 0..2, frac_guard 0..2
- unrolled_k: 40 evals, 39 feasible; max throughput seen 11.7 MSPS; best accuracy 13.83 bits; best feasible luts_plus_ffs=348; feasible ranges: data_width 16..18, n_iter 12..16, angle_guard 0..2, frac_guard 0..2, k 2..4
- pipelined: 50 evals, 28 feasible; max throughput seen 282 MSPS; best accuracy 12.22 bits; best feasible luts_plus_ffs=1350; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 24 feasible; max throughput seen 178 MSPS; best accuracy 11.45 bits; best feasible luts_plus_ffs=868; feasible ranges: data_width 14..16, n_iter 12..13, angle_guard 1..2, frac_guard 1..2, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `iterative` (160 evals): data_width=14..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (9 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 279 feasible; hypervolume 1.591e+04 (+220.7%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and dominated by the `iterative` family, which offers the best area (luts_plus_ffs=264) while meeting the throughput constraint (10.4 MSPS >= 1) and accuracy constraint (10.7 bits > 10). The `pipelined` and `pipelined_m` families are significantly larger (868-1350 LUTs+FFs) and do not improve the hypervolume in the low-area region. Since this is the final round and the front covers the relevant trade-off space for the 'low_area_control' spec (minimizing area while meeting 1 MSPS and 2^-10 error), further exploration would not yield a better design for the selection rule (min luts_plus_ffs). The best design is `iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc]` with 264 LUTs+FFs.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.591e+04 (gain this round: +220.7%).
Feasible designs: 279 of 400 evaluations (234 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 30% violate; best seen 2.61e-08 (2^-25.19)

Pareto front (feasible, 34 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=264, accuracy_bits=10.7, luts=170, ffs=94, throughput_msps=10.4, max_abs_err=0.000594 (2^-10.72), power_index=0.189
- iterative [data_width=17 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=308, accuracy_bits=12.8, luts=203, ffs=106, throughput_msps=10.2, max_abs_err=0.000145 (2^-12.76), power_index=0.22
- iterative [data_width=21 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=351, accuracy_bits=13.7, luts=229, ffs=122, throughput_msps=10.8, max_abs_err=7.32e-05 (2^-13.74), power_index=0.238
- iterative [data_width=20 n_iter=19 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=386, accuracy_bits=15.3, luts=264, ffs=122, throughput_msps=7.09, max_abs_err=2.4e-05 (2^-15.35), power_index=0.319
- iterative [data_width=21 n_iter=22 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=406, accuracy_bits=16.4, luts=282, ffs=124, throughput_msps=6.24, max_abs_err=1.15e-05 (2^-16.41), power_index=0.382
- iterative [data_width=22 n_iter=27 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=440, accuracy_bits=17.2, luts=306, ffs=133, throughput_msps=5.2, max_abs_err=6.68e-06 (2^-17.19), power_index=0.496
- iterative [data_width=23 n_iter=22 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=451, accuracy_bits=18.4, luts=317, ffs=134, throughput_msps=6.24, max_abs_err=2.9e-06 (2^-18.39), power_index=0.424
- iterative [data_width=26 n_iter=27 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=520, accuracy_bits=20.7, luts=373, ffs=147, throughput_msps=5.2, max_abs_err=6.06e-07 (2^-20.65), power_index=0.587
- iterative [data_width=26 n_iter=24 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=543, accuracy_bits=21.6, luts=389, ffs=154, throughput_msps=5.68, max_abs_err=3.21e-07 (2^-21.57), power_index=0.552
- iterative [data_width=28 n_iter=30 angle_guard=4 frac_guard=4 rounding=trunc] luts_plus_ffs=651, accuracy_bits=25.2, luts=481, ffs=169, throughput_msps=4.56, max_abs_err=2.61e-08 (2^-25.19), power_index=0.808
Front coverage: luts_plus_ffs 264..651 (HV reference 1500); accuracy_bits 10.7..25.2 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 260 evals, 188 feasible; max throughput seen 15.3 MSPS; best accuracy 25.19 bits; best feasible luts_plus_ffs=264; feasible ranges: data_width 13..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 40 evals, 39 feasible; max throughput seen 11.7 MSPS; best accuracy 13.83 bits; best feasible luts_plus_ffs=348; feasible ranges: data_width 16..18, n_iter 12..16, angle_guard 0..2, frac_guard 0..2, k 2..4
- pipelined: 50 evals, 28 feasible; max throughput seen 282 MSPS; best accuracy 12.22 bits; best feasible luts_plus_ffs=1350; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 24 feasible; max throughput seen 178 MSPS; best accuracy 11.45 bits; best feasible luts_plus_ffs=868; feasible ranges: data_width 14..16, n_iter 12..13, angle_guard 1..2, frac_guard 1..2, m 2..4
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 10519 in, 2789 out
- provider-reported cost: $0.0107
- full prompts and replies: `llm_trace.jsonl`

