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
`unrolled_k:data_width=16,n_iter=14,angle_guard=1,frac_guard=0,rounding=trunc,k=2` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 257 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 96 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 105 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 10.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 10 | exact: schedule |
| latency_ns | 94.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.133 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000643 (2^-10.60) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 10.5 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000129 (2^-12.92) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 2.11 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.6 | exact: bit-accurate model, exhaustive (65536 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 10 cycles, a new input every 10 cycle(s). DDS tone from its exact outputs: SFDR 91.6 dBc, SNR 75.0 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (9 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `unrolled_k:data_width=16,n_iter=14,angle_guard=1,frac_guard=0,rounding=trunc,k=2` | 257 | 96 | 10.5 | 10 | 0.133 | 0.000643 (2^-10.60) | 10.60 |
| 1 | `unrolled_k:data_width=16,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,k=2` | 270 | 98 | 10.5 | 10 | 0.138 | 0.000344 (2^-11.50) | 11.50 |
| 2 | `unrolled_k:data_width=15,n_iter=20,angle_guard=4,frac_guard=2,rounding=round,k=2` | 332 | 99 | 7.9 | 13 | 0.211 | 0.000192 (2^-12.35) | 12.35 |
| 3 | `unrolled_k:data_width=20,n_iter=21,angle_guard=2,frac_guard=0,rounding=round,k=2` | 360 | 118 | 7.3 | 14 | 0.252 | 2.17e-05 (2^-15.49) | 15.49 |
| 4 | `unrolled_k:data_width=23,n_iter=22,angle_guard=4,frac_guard=1,rounding=trunc,k=2` | 431 | 137 | 7.0 | 14 | 0.299 | 3.08e-06 (2^-18.31) | 18.31 |
| 5 | `unrolled_k:data_width=25,n_iter=27,angle_guard=3,frac_guard=2,rounding=trunc,k=2` | 500 | 148 | 5.8 | 17 | 0.415 | 4.7e-07 (2^-21.02) | 21.02 |
| 6 | `unrolled_k:data_width=26,n_iter=23,angle_guard=2,frac_guard=2,rounding=trunc,k=2` | 500 | 152 | 6.5 | 15 | 0.368 | 4.26e-07 (2^-21.16) | 21.16 |
| 7 | `unrolled_k:data_width=26,n_iter=27,angle_guard=4,frac_guard=3,rounding=trunc,k=3` | 709 | 156 | 5.6 | 12 | 0.391 | 1.43e-07 (2^-22.74) | 22.74 |
| 8 | `unrolled_k:data_width=28,n_iter=28,angle_guard=3,frac_guard=1,rounding=trunc,k=4` | 847 | 160 | 4.9 | 10 | 0.379 | 1e-07 (2^-23.25) | 23.25 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >=1 MSPS throughput and max_abs_err <= 2^-10, with area (luts_plus_ffs) as the primary objective. Accuracy of 2^-10 requires roughly N>=12 micro-rotations with W>=12, which is comfortably achievable. The key trade-off is between pipelined (more FFs, simpler logic, guaranteed 1/cycle), pipelined_m (fewer FFs via sparse registration, still 1/cycle), and unrolled_k (shared datapath, fewer FFs but potentially lower Fmax or higher LUTs). I exclude iterative because it produces 1 result every N+3 cycles, making it very hard to hit 1 MSPS without very high Fmax, and its shared barrel-shifter datapath may not save enough area to compensate. I focus data_width and n_iter in the 12-16 range because lower values risk missing the 2^-10 accuracy constraint, while higher values waste area. angle_guard is kept at -2..0 to minimize the atan-LUT and angle-path width, and frac_guard at 0..2 to keep datapath narrow while preserving accuracy. The budget is split 45/35/20 to prioritize the two pipelined families (most likely to be on the Pareto front for area) while still exploring unrolled_k for potential FF savings.*)
- `pipelined` (45 evals): data_width=12..16, n_iter=12..16, angle_guard=-2..0, frac_guard=0..2, rounding=trunc|round. *Why:* Pipelined gives 1 result/cycle, easily meeting >=1 MSPS. With N=12-16 and W=12-16, max_abs_err should be well below 2^-10. This family has the simplest per-stage logic (no FSM, no barrel shifter sharing complexity) and is the primary candidate for minimal LUT+FF area while guaranteeing throughput.
- `pipelined_m` (35 evals): data_width=12..16, n_iter=12..16, angle_guard=-2..0, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Pipelined_m registers every m stages, reducing FF count versus fully pipelined while still delivering 1 result/cycle. With m=2-4, FF savings can be significant at similar LUT cost, potentially yielding lower luts_plus_ffs. Same accuracy envelope as pipelined since the computation is identical.
- `unrolled_k` (20 evals): data_width=12..16, n_iter=12..16, angle_guard=-2..0, frac_guard=0..2, rounding=trunc|round, k=4..8. *Why:* Unrolled_k with high k (4-8) can achieve 1 result/cycle or near-1 result/cycle throughput with a shared datapath and fewer pipeline registers than pipelined. The FSM overhead is small. This may trade slightly higher LUTs (wider datapath for k rotations) against lower FFs, potentially finding a different point on the Pareto front. k=4-8 with N=12-16 gives ceil(N/k)+3 = 4-7 cycles/result, which at moderate Fmax should still meet 1 MSPS.

**Result (code):** 100 evaluations this round, 100 total; 41 feasible; hypervolume 1031 (n/a).

**LLM decision:** `refine` — The current Pareto front is dominated by `unrolled_k` for the primary objective (min area), with the best design at 491 LUTs+FFs. However, 59% of evaluations violate the accuracy constraint, indicating the search space is too broad in dimensions that do not contribute to accuracy (like high `data_width` or excessive `n_iter` for low accuracy targets). The feasible region is tightly clustered around `data_width` 15-16 and `n_iter` 12-14. To maximize hypervolume and find the true minimum area point, we should narrow the search to this promising region. Specifically, we will focus on `unrolled_k` and `pipelined_m` (which showed good feasibility) and restrict `data_width` to 14-16, `n_iter` to 11-14, and `angle_guard`/`frac_guard` to their effective ranges (0 and 2 respectively for the best unrolled_k, but allowing 0-2 for pipelined_m to explore trade-offs). This focuses the 100 evaluations on the critical trade-off curve between area and accuracy within the feasible bounds.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 1031 (gain this round: n/a (first round)).
Feasible designs: 41 of 100 evaluations (26 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 59% violate; best seen 0.000373 (2^-11.39)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=15 n_iter=12 angle_guard=0 frac_guard=2 rounding=round k=4] luts_plus_ffs=491, accuracy_bits=10.1, luts=399, ffs=93, throughput_msps=12, max_abs_err=0.000927 (2^-10.07), power_index=0.111
- unrolled_k [data_width=16 n_iter=13 angle_guard=0 frac_guard=2 rounding=round k=7] luts_plus_ffs=751, accuracy_bits=11.1, luts=654, ffs=97, throughput_msps=8.4, max_abs_err=0.000468 (2^-11.06), power_index=0.141
- unrolled_k [data_width=16 n_iter=14 angle_guard=0 frac_guard=2 rounding=round k=7] luts_plus_ffs=774, accuracy_bits=11.3, luts=677, ffs=97, throughput_msps=8.4, max_abs_err=0.000389 (2^-11.33), power_index=0.146
- pipelined_m [data_width=16 n_iter=16 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1113, accuracy_bits=11.4, luts=859, ffs=254, throughput_msps=97.8, max_abs_err=0.000373 (2^-11.39), power_index=0.0419
Front coverage: luts_plus_ffs 491..1113 (HV reference 1500); accuracy_bits 10.1..11.4 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 4 feasible; max throughput seen 12 MSPS; best accuracy 11.33 bits; best feasible luts_plus_ffs=491; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..0, frac_guard 2..2, k 4..8
- pipelined: 45 evals, 11 feasible; max throughput seen 282 MSPS; best accuracy 11.29 bits; best feasible luts_plus_ffs=1273; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard -1..0, frac_guard 0..2
- pipelined_m: 35 evals, 26 feasible; max throughput seen 178 MSPS; best accuracy 11.39 bits; best feasible luts_plus_ffs=830; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard -1..0, frac_guard 0..2, m 3..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Narrowing to the observed feasible cluster (DW 14-16, N 11-14) reduces wasted evaluations on infeasible high-area/low-accuracy or low-area/infeasible-accuracy points. Focusing on the two best families allows NSGA-II to densely map the Pareto front in the critical region.*)
- `unrolled_k` (60 evals): data_width=14..16, n_iter=11..14, angle_guard=-1..1, frac_guard=0..3, rounding=trunc|round, k=2..8. *Why:* Dominates the area objective; needs focused search to find the absolute minimum area feasible point.
- `pipelined_m` (40 evals): data_width=14..16, n_iter=11..14, angle_guard=-1..1, frac_guard=0..3, rounding=trunc|round, m=2..6. *Why:* Second best area performer (830 LUTs+FFs) with high throughput; explores the trade-off curve at higher accuracy/throughput.

**Result (code):** 100 evaluations this round, 200 total; 104 feasible; hypervolume 1923 (+86.5%).

**LLM decision:** `refine` — The current Pareto front is dominated by `unrolled_k` designs (352-617 luts_plus_ffs), which are significantly more area-efficient than `pipelined` (min 1273) and `pipelined_m` (min 830). The `iterative` family is unexplored, but given that `unrolled_k` with k=2 already achieves ~10.5 MSPS with 352 area units, `iterative` (1 rot/cycle) would likely require higher n_iter or lower Fmax to meet throughput, likely resulting in higher area or lower Fmax than the current best. The main gap is in the accuracy area: the front only reaches 11.8 bits. To improve hypervolume, we need to explore if we can get higher accuracy (e.g., 12+ bits) without exploding area, or if we can push area lower. The current best area is 352. Let's refine the search around the `unrolled_k` sweet spot (data_width 15-16, n_iter 12-14, angle_guard 0-1, frac_guard 0-2, k 2-4) to see if we can find a design with lower area or higher accuracy. We should also check if `pipelined_m` with higher m (less registers) can beat 830, but it's unlikely to beat `unrolled_k`. I will focus the budget on refining `unrolled_k` and `pipelined_m` to map the front better in the low-area, high-accuracy region.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1923 (gain this round: +86.5%).
Feasible designs: 104 of 200 evaluations (76 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 48% violate; best seen 0.000279 (2^-11.81)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=352, accuracy_bits=10.6, luts=257, ffs=96, throughput_msps=10.5, max_abs_err=0.000643 (2^-10.60), power_index=0.133
- unrolled_k [data_width=15 n_iter=14 angle_guard=1 frac_guard=0 rounding=round k=3] luts_plus_ffs=404, accuracy_bits=10.6, luts=313, ffs=91, throughput_msps=8.97, max_abs_err=0.000632 (2^-10.63), power_index=0.122
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc k=3] luts_plus_ffs=459, accuracy_bits=11.7, luts=359, ffs=100, throughput_msps=8.97, max_abs_err=0.000311 (2^-11.65), power_index=0.138
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=2 rounding=round k=5] luts_plus_ffs=617, accuracy_bits=11.8, luts=518, ffs=99, throughput_msps=9.7, max_abs_err=0.000279 (2^-11.81), power_index=0.139
Front coverage: luts_plus_ffs 352..617 (HV reference 1500); accuracy_bits 10.6..11.8 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- unrolled_k: 80 evals, 46 feasible; max throughput seen 13.5 MSPS; best accuracy 11.81 bits; best feasible luts_plus_ffs=352; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard -1..1, frac_guard 0..3, k 2..8
- pipelined: 45 evals, 11 feasible; max throughput seen 282 MSPS; best accuracy 11.29 bits; best feasible luts_plus_ffs=1273; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard -1..0, frac_guard 0..2
- pipelined_m: 75 evals, 47 feasible; max throughput seen 178 MSPS; best accuracy 11.45 bits; best feasible luts_plus_ffs=830; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard -1..1, frac_guard 0..2, m 2..6
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Focus on the two most promising families to refine the front in the low-area, high-accuracy region.*)
- `unrolled_k` (24 evals): data_width=14..16, n_iter=12..15, angle_guard=-1..1, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Dominant family for area. Refine around best feasible points to find lower area or higher accuracy.
- `pipelined_m` (16 evals): data_width=14..16, n_iter=12..15, angle_guard=-1..1, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Second best family. Check if higher m (fewer registers) can reduce area below 830.

**Result (code):** 40 evaluations this round, 240 total; 133 feasible; hypervolume 2018 (+4.9%).

**LLM decision:** `stop` — The Pareto front is well-established and feasible. The minimum area design (unrolled_k, 352 LUTs+FFs) meets the throughput constraint (10.5 MSPS >= 1) and the accuracy constraint (10.6 bits > 10 bits required). The front covers the trade-off space from 352 to 526 LUTs+FFs and 10.6 to 11.8 accuracy bits. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (352) as per the selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 2018 (gain this round: +4.9%).
Feasible designs: 133 of 240 evaluations (99 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 45% violate; best seen 0.000279 (2^-11.81)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=352, accuracy_bits=10.6, luts=257, ffs=96, throughput_msps=10.5, max_abs_err=0.000643 (2^-10.60), power_index=0.133
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=368, accuracy_bits=11.5, luts=270, ffs=98, throughput_msps=10.5, max_abs_err=0.000344 (2^-11.50), power_index=0.138
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc k=3] luts_plus_ffs=459, accuracy_bits=11.7, luts=359, ffs=100, throughput_msps=8.97, max_abs_err=0.000311 (2^-11.65), power_index=0.138
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=2 rounding=round k=4] luts_plus_ffs=526, accuracy_bits=11.8, luts=427, ffs=99, throughput_msps=10.3, max_abs_err=0.000279 (2^-11.81), power_index=0.139
Front coverage: luts_plus_ffs 352..526 (HV reference 1500); accuracy_bits 10.6..11.8 (HV reference 10); data_width on the front 16..16 (registry 8..28).

Per family:
- unrolled_k: 104 evals, 65 feasible; max throughput seen 13.5 MSPS; best accuracy 11.81 bits; best feasible luts_plus_ffs=352; feasible ranges: data_width 14..16, n_iter 12..15, angle_guard -1..1, frac_guard 0..3, k 2..8
- pipelined: 45 evals, 11 feasible; max throughput seen 282 MSPS; best accuracy 11.29 bits; best feasible luts_plus_ffs=1273; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard -1..0, frac_guard 0..2
- pipelined_m: 91 evals, 57 feasible; max throughput seen 178 MSPS; best accuracy 11.45 bits; best feasible luts_plus_ffs=830; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard -1..1, frac_guard 0..2, m 2..6
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `unrolled_k` (160 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (4 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 287 feasible; hypervolume 1.214e+04 (+501.4%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and feasible. The minimum area design (unrolled_k, 352 LUTs+FFs) meets the throughput constraint (10.5 MSPS >= 1) and the accuracy constraint (10.6 bits > 10 bits required). The front covers the trade-off space from 352 to 526 LUTs+FFs and 10.6 to 11.8 accuracy bits. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (352) as per the selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.214e+04 (gain this round: +501.4%).
Feasible designs: 287 of 400 evaluations (245 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 28% violate; best seen 1e-07 (2^-23.25)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=trunc k=2] luts_plus_ffs=352, accuracy_bits=10.6, luts=257, ffs=96, throughput_msps=10.5, max_abs_err=0.000643 (2^-10.60), power_index=0.133
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=368, accuracy_bits=11.5, luts=270, ffs=98, throughput_msps=10.5, max_abs_err=0.000344 (2^-11.50), power_index=0.138
- unrolled_k [data_width=15 n_iter=20 angle_guard=4 frac_guard=2 rounding=round k=2] luts_plus_ffs=431, accuracy_bits=12.3, luts=332, ffs=99, throughput_msps=7.91, max_abs_err=0.000192 (2^-12.35), power_index=0.211
- unrolled_k [data_width=20 n_iter=21 angle_guard=2 frac_guard=0 rounding=round k=2] luts_plus_ffs=478, accuracy_bits=15.5, luts=360, ffs=118, throughput_msps=7.35, max_abs_err=2.17e-05 (2^-15.49), power_index=0.252
- unrolled_k [data_width=23 n_iter=22 angle_guard=4 frac_guard=1 rounding=trunc k=2] luts_plus_ffs=568, accuracy_bits=18.3, luts=431, ffs=137, throughput_msps=7.01, max_abs_err=3.08e-06 (2^-18.31), power_index=0.299
- unrolled_k [data_width=25 n_iter=27 angle_guard=3 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=648, accuracy_bits=21, luts=500, ffs=148, throughput_msps=5.77, max_abs_err=4.7e-07 (2^-21.02), power_index=0.415
- unrolled_k [data_width=26 n_iter=23 angle_guard=2 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=652, accuracy_bits=21.2, luts=500, ffs=152, throughput_msps=6.54, max_abs_err=4.26e-07 (2^-21.16), power_index=0.368
- unrolled_k [data_width=26 n_iter=27 angle_guard=4 frac_guard=3 rounding=trunc k=3] luts_plus_ffs=865, accuracy_bits=22.7, luts=709, ffs=156, throughput_msps=5.56, max_abs_err=1.43e-07 (2^-22.74), power_index=0.391
- unrolled_k [data_width=28 n_iter=28 angle_guard=3 frac_guard=1 rounding=trunc k=4] luts_plus_ffs=1008, accuracy_bits=23.3, luts=847, ffs=160, throughput_msps=4.94, max_abs_err=1e-07 (2^-23.25), power_index=0.379
Front coverage: luts_plus_ffs 352..1008 (HV reference 1500); accuracy_bits 10.6..23.3 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- unrolled_k: 264 evals, 219 feasible; max throughput seen 13.5 MSPS; best accuracy 23.25 bits; best feasible luts_plus_ffs=352; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, k 2..8
- pipelined: 45 evals, 11 feasible; max throughput seen 282 MSPS; best accuracy 11.29 bits; best feasible luts_plus_ffs=1273; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard -1..0, frac_guard 0..2
- pipelined_m: 91 evals, 57 feasible; max throughput seen 178 MSPS; best accuracy 11.45 bits; best feasible luts_plus_ffs=830; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard -1..1, frac_guard 0..2, m 2..6
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 22818 in, 3906 out
- provider-reported cost: $0.0077
- full prompts and replies: `llm_trace.jsonl`

