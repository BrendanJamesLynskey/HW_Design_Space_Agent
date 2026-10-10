# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`iterative:data_width=14,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 168 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 91 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 11.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 85.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.166 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000944 (2^-10.05) | exact: bit-accurate model, exhaustive (16384 angles) |
| max_abs_err_lsb | 3.87 | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err | 0.000229 (2^-12.09) | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err_lsb | 0.939 | exact: bit-accurate model, exhaustive (16384 angles) |
| accuracy_bits | 10 | exact: bit-accurate model, exhaustive (16384 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 17 cycles, a new input every 17 cycle(s). DDS tone from its exact outputs: SFDR 77.2 dBc, SNR 70.1 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (37 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=14,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc` | 168 | 91 | 11.7 | 17 | 0.166 | 0.000944 (2^-10.05) | 10.05 |
| 1 | `iterative:data_width=15,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 168 | 92 | 10.4 | 19 | 0.186 | 0.000632 (2^-10.63) | 10.63 |
| 2 | `iterative:data_width=15,n_iter=16,angle_guard=4,frac_guard=0,rounding=round` | 173 | 95 | 10.2 | 19 | 0.192 | 0.000548 (2^-10.83) | 10.83 |
| 3 | `iterative:data_width=16,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 179 | 97 | 11.0 | 18 | 0.187 | 0.000301 (2^-11.70) | 11.70 |
| 4 | `iterative:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 191 | 102 | 11.7 | 17 | 0.187 | 0.000204 (2^-12.26) | 12.26 |
| 5 | `iterative:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc` | 197 | 108 | 10.2 | 19 | 0.218 | 0.000179 (2^-12.45) | 12.45 |
| 6 | `iterative:data_width=16,n_iter=15,angle_guard=4,frac_guard=4,rounding=trunc` | 216 | 108 | 10.8 | 18 | 0.219 | 0.00014 (2^-12.80) | 12.80 |
| 7 | `iterative:data_width=20,n_iter=16,angle_guard=-2,frac_guard=0,rounding=trunc` | 212 | 114 | 10.2 | 19 | 0.233 | 9.85e-05 (2^-13.31) | 13.31 |
| 8 | `iterative:data_width=18,n_iter=17,angle_guard=1,frac_guard=0,rounding=round` | 226 | 108 | 7.9 | 20 | 0.251 | 9.26e-05 (2^-13.40) | 13.40 |
| 9 | `iterative:data_width=20,n_iter=15,angle_guard=1,frac_guard=0,rounding=trunc` | 218 | 117 | 10.8 | 18 | 0.227 | 8.71e-05 (2^-13.49) | 13.49 |
| 10 | `iterative:data_width=18,n_iter=16,angle_guard=2,frac_guard=3,rounding=trunc` | 225 | 114 | 10.2 | 19 | 0.243 | 5.94e-05 (2^-14.04) | 14.04 |
| 11 | `iterative:data_width=20,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc` | 225 | 118 | 10.2 | 19 | 0.246 | 5.62e-05 (2^-14.12) | 14.12 |
| 12 | `iterative:data_width=20,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 227 | 118 | 10.2 | 19 | 0.247 | 4.12e-05 (2^-14.57) | 14.57 |
| 13 | `iterative:data_width=20,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 239 | 122 | 10.2 | 19 | 0.258 | 3.93e-05 (2^-14.63) | 14.63 |
| 14 | `iterative:data_width=20,n_iter=24,angle_guard=1,frac_guard=0,rounding=round` | 262 | 118 | 5.9 | 27 | 0.386 | 2.52e-05 (2^-15.28) | 15.28 |
| 15 | `iterative:data_width=21,n_iter=28,angle_guard=0,frac_guard=0,rounding=round` | 280 | 122 | 5.1 | 31 | 0.468 | 1.79e-05 (2^-15.77) | 15.77 |
| 16 | `iterative:data_width=22,n_iter=22,angle_guard=4,frac_guard=0,rounding=trunc` | 289 | 131 | 6.2 | 25 | 0.395 | 1.22e-05 (2^-16.32) | 16.32 |
| 17 | `iterative:data_width=20,n_iter=24,angle_guard=3,frac_guard=3,rounding=trunc` | 300 | 126 | 5.8 | 27 | 0.432 | 9.47e-06 (2^-16.69) | 16.69 |
| 18 | `iterative:data_width=22,n_iter=24,angle_guard=4,frac_guard=0,rounding=round` | 303 | 131 | 5.8 | 27 | 0.441 | 5.23e-06 (2^-17.54) | 17.54 |
| 19 | `iterative:data_width=23,n_iter=28,angle_guard=1,frac_guard=1,rounding=trunc` | 320 | 135 | 5.0 | 31 | 0.531 | 4.11e-06 (2^-17.89) | 17.89 |
| 20 | `iterative:data_width=23,n_iter=24,angle_guard=3,frac_guard=1,rounding=trunc` | 321 | 137 | 5.8 | 27 | 0.465 | 2.86e-06 (2^-18.42) | 18.42 |
| 21 | `iterative:data_width=22,n_iter=24,angle_guard=3,frac_guard=3,rounding=trunc` | 334 | 136 | 5.8 | 27 | 0.478 | 2.39e-06 (2^-18.67) | 18.67 |
| 22 | `iterative:data_width=26,n_iter=28,angle_guard=1,frac_guard=0,rounding=round` | 375 | 148 | 4.9 | 31 | 0.61 | 3.95e-07 (2^-21.27) | 21.27 |
| 23 | `iterative:data_width=26,n_iter=29,angle_guard=2,frac_guard=2,rounding=trunc` | 399 | 153 | 4.8 | 32 | 0.665 | 2.9e-07 (2^-21.72) | 21.72 |
| 24 | `iterative:data_width=28,n_iter=28,angle_guard=1,frac_guard=0,rounding=trunc` | 398 | 158 | 4.9 | 31 | 0.649 | 2.4e-07 (2^-21.99) | 21.99 |
| 25 | `iterative:data_width=27,n_iter=28,angle_guard=1,frac_guard=2,rounding=trunc` | 413 | 157 | 4.9 | 31 | 0.665 | 1.69e-07 (2^-22.50) | 22.50 |
| 26 | `iterative:data_width=27,n_iter=28,angle_guard=3,frac_guard=2,rounding=trunc` | 417 | 159 | 4.9 | 31 | 0.672 | 1.14e-07 (2^-23.06) | 23.06 |
| 27 | `iterative:data_width=28,n_iter=28,angle_guard=4,frac_guard=0,rounding=round` | 418 | 161 | 4.9 | 31 | 0.676 | 1.03e-07 (2^-23.22) | 23.22 |
| 28 | `iterative:data_width=27,n_iter=28,angle_guard=3,frac_guard=3,rounding=trunc` | 434 | 161 | 4.9 | 31 | 0.694 | 8.12e-08 (2^-23.55) | 23.55 |
| 29 | `iterative:data_width=28,n_iter=28,angle_guard=2,frac_guard=2,rounding=trunc` | 434 | 163 | 4.9 | 31 | 0.697 | 7.27e-08 (2^-23.71) | 23.71 |
| 30 | `iterative:data_width=28,n_iter=27,angle_guard=3,frac_guard=2,rounding=trunc` | 436 | 164 | 5.0 | 30 | 0.677 | 6.96e-08 (2^-23.78) | 23.78 |
| 31 | `iterative:data_width=28,n_iter=27,angle_guard=3,frac_guard=3,rounding=trunc` | 453 | 166 | 5.0 | 30 | 0.699 | 4.57e-08 (2^-24.38) | 24.38 |
| 32 | `iterative:data_width=28,n_iter=27,angle_guard=4,frac_guard=3,rounding=trunc` | 455 | 167 | 5.0 | 30 | 0.702 | 4.35e-08 (2^-24.45) | 24.45 |
| 33 | `iterative:data_width=28,n_iter=30,angle_guard=4,frac_guard=3,rounding=trunc` | 462 | 167 | 4.6 | 33 | 0.782 | 3.83e-08 (2^-24.64) | 24.64 |
| 34 | `iterative:data_width=28,n_iter=28,angle_guard=3,frac_guard=4,rounding=trunc` | 470 | 168 | 4.9 | 31 | 0.745 | 3.75e-08 (2^-24.67) | 24.67 |
| 35 | `iterative:data_width=28,n_iter=28,angle_guard=4,frac_guard=4,rounding=trunc` | 472 | 169 | 4.9 | 31 | 0.748 | 3e-08 (2^-24.99) | 24.99 |
| 36 | `iterative:data_width=28,n_iter=30,angle_guard=4,frac_guard=3,rounding=round` | 538 | 167 | 4.6 | 33 | 0.876 | 2.08e-08 (2^-25.52) | 25.52 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-first: throughput >=1 MSPS is trivially met by every family (even iterative at N=18 gives several MSPS), and accuracy depends only on data_width/n_iter/angle_guard/frac_guard/rounding, not on the family. Therefore the Pareto front in (luts_plus_ffs, accuracy_bits) is almost certainly owned by the smallest-area family, iterative, and the other families are only worth probing to confirm domination. Round 1 is a broad sweep: W=10..20 straddles the 2^-10 error constraint (output LSB 2^-(W-2)), N=8..18 straddles the CORDIC angle-approximation floor, and the guard/rounding knobs expose the cheap accuracy levers. 70% of the budget goes to iterative to densely map the front near the constraint boundary and just above it (the HV reference is 1500 LUTs+FFs / 10 accuracy bits, so designs far above 1500 area or far below 10 bits are not worth many samples). The remaining 30% is split between unrolled_k and pipelined_m to test whether any non-iterative point is non-dominated; pipelined is omitted from round 1 because it is the largest-area family (N register stages) and cannot beat iterative on the only objective. Later rounds will re-allocate toward whichever family actually appears on the front and extend its ranges.*)
- `iterative` (70 evals): data_width=10..20, n_iter=8..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Area is the sole objective and throughput only needs >=1 MSPS, which the shared-datapath iterative core meets easily (Fmax/(N+3) is still several MSPS for N<=18). Accuracy is family-independent, so for any accuracy point the iterative core is the smallest-area realisation and should own most of the Pareto front. Ranges bracket the accuracy constraint: W=10..20 spans output LSB 2^-8..2^-18 around the 2^-10 limit, N=8..18 spans the CORDIC angle-approximation floor, and the guard/rounding knobs let the search trade datapath bits for error.
- `unrolled_k` (15 evals): data_width=10..20, n_iter=8..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Same accuracy model as iterative but k micro-rotations/cycle, so it should be area-dominated by iterative for this spec. A small share confirms whether any k=2 point sneaks onto the front (it cannot help throughput, which is already satisfied) and guards against a modelling surprise.
- `pipelined_m` (15 evals): data_width=10..20, n_iter=8..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* Registers every m stages: 1 result/cycle but N-stage datapath, so FFs scale with N and it should be area-dominated for a 1 MSPS target. Included at low share to verify it stays off the front and to catch any case where its higher Fmax changes the area/accuracy picture.

**Result (code):** 100 evaluations this round, 100 total; 48 feasible; hypervolume 5247 (n/a).

**LLM decision:** `map_front` — The feasible front is entirely iterative (11 designs) and covers only a narrow slice of the achievable trade-off: luts_plus_ffs 259..367 against the HV reference of 1500, and accuracy_bits 10..14.4 while data_width on the front is only 14..20 versus the registry's 8..28. The accuracy axis is therefore far from mapped, and the throughput constraint (>=1 MSPS) is already met with huge margin (best seen 171 MSPS, iterative front designs 8-13 MSPS), so the binding objective is area/accuracy coverage. A code-driven NSGA-II coverage search over the full iterative ranges, seeded with the current front, is the right way to extend the curve upward in accuracy and probe below the current 259 luts_plus_ffs minimum before spending later rounds refining. pipelined_m (best feasible luts_plus_ffs=884) and unrolled_k (372) are both far worse on area than iterative, so they are unlikely to add useful front points; pipelined is the same 1-result/cycle regime as pipelined_m and is not worth a dedicated round given area is everything.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 5247 (gain this round: n/a (first round)).
Feasible designs: 48 of 100 evaluations (39 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 52% violate; best seen 4.61e-05 (2^-14.40)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=259, accuracy_bits=10, luts=168, ffs=91, throughput_msps=11.7, max_abs_err=0.000944 (2^-10.05), power_index=0.166
- iterative [data_width=17 n_iter=12 angle_guard=-2 frac_guard=0 rounding=trunc] luts_plus_ffs=266, accuracy_bits=10.1, luts=167, ffs=99, throughput_msps=13.2, max_abs_err=0.000901 (2^-10.12), power_index=0.15
- iterative [data_width=16 n_iter=16 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=271, accuracy_bits=10.6, luts=174, ffs=98, throughput_msps=10.4, max_abs_err=0.000643 (2^-10.60), power_index=0.194
- iterative [data_width=17 n_iter=12 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=281, accuracy_bits=10.8, luts=179, ffs=102, throughput_msps=13.2, max_abs_err=0.000568 (2^-10.78), power_index=0.158
- iterative [data_width=17 n_iter=16 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=285, accuracy_bits=11.7, luts=183, ffs=102, throughput_msps=10.4, max_abs_err=0.000307 (2^-11.67), power_index=0.204
- iterative [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=304, accuracy_bits=12.4, luts=197, ffs=108, throughput_msps=10.2, max_abs_err=0.000179 (2^-12.45), power_index=0.218
- iterative [data_width=20 n_iter=16 angle_guard=-2 frac_guard=0 rounding=trunc] luts_plus_ffs=326, accuracy_bits=13.3, luts=212, ffs=114, throughput_msps=10.2, max_abs_err=9.85e-05 (2^-13.31), power_index=0.233
- iterative [data_width=19 n_iter=17 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=343, accuracy_bits=13.6, luts=230, ffs=113, throughput_msps=7.95, max_abs_err=7.8e-05 (2^-13.65), power_index=0.258
- iterative [data_width=20 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=344, accuracy_bits=14.1, luts=225, ffs=118, throughput_msps=10.2, max_abs_err=5.62e-05 (2^-14.12), power_index=0.246
- iterative [data_width=20 n_iter=17 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=367, accuracy_bits=14.4, luts=248, ffs=119, throughput_msps=7.95, max_abs_err=4.61e-05 (2^-14.40), power_index=0.276
Front coverage: luts_plus_ffs 259..367 (HV reference 1500); accuracy_bits 10..14.4 (HV reference 10); data_width on the front 14..20 (registry 8..28).

Per family:
- iterative: 70 evals, 39 feasible; max throughput seen 16.9 MSPS; best accuracy 14.40 bits; best feasible luts_plus_ffs=259; feasible ranges: data_width 14..20, n_iter 12..17, angle_guard -2..2, frac_guard 0..2
- unrolled_k: 15 evals, 5 feasible; max throughput seen 14 MSPS; best accuracy 12.82 bits; best feasible luts_plus_ffs=372; feasible ranges: data_width 15..19, n_iter 12..15, angle_guard -1..1, frac_guard 2..2, k 2..4
- pipelined_m: 15 evals, 4 feasible; max throughput seen 171 MSPS; best accuracy 11.96 bits; best feasible luts_plus_ffs=884; feasible ranges: data_width 16..17, n_iter 12..15, angle_guard -1..0, frac_guard 0..2, m 4..7
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (11 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 137 feasible; hypervolume 1.424e+04 (+171.5%).

**LLM decision:** `refine` — Round 2 left a 22-design front that is entirely `iterative` (area 259..633, accuracy 10..23.5 bits), so the two families still on the front are just iterative; unrolled_k (best feasible 372) and pipelined_m (best feasible 884) are already dominated on area at equal accuracy, and `pipelined` would be too (identical accuracy model, strictly more area) — adding it would only burn budget on dominated points for an area-minimising spec whose throughput constraint is already met at 11.7 MSPS. Two facts drive the next round. (1) The selection rule is min luts_plus_ffs, and the current pick is iterative[W=14,N=14,ag=1,fg=2,trunc] at 259 with accuracy 10.05 bits — only 0.05 bits of margin over the 2^-10 constraint, so the low-area corner is fragile and must be tightened (W=13 is the only way below 259 and is borderline feasible). (2) The HV is dominated by the top of the front: the point (633, 23.5) alone contributes roughly (1500-633)x(23.5-10) ~ 1.17e4 of the 1.424e4 HV, so each extra accuracy bit at the top is worth ~870 HV, whereas the low corner contributes almost nothing to HV. The best seen accuracy (23.51 bits at W=28,N=28,fg=4) is well short of the ~26-bit ceiling implied by the W=28 output LSB (2^-26), so the high-accuracy end is clearly extendable and is the highest-leverage HV move. Hence refine both ends rather than map the whole front (code already reserves budget for full-range mapping before the run ends).

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.424e+04 (gain this round: +171.5%).
Feasible designs: 137 of 200 evaluations (119 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 32% violate; best seen 8.37e-08 (2^-23.51)

Pareto front (feasible, 22 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=259, accuracy_bits=10, luts=168, ffs=91, throughput_msps=11.7, max_abs_err=0.000944 (2^-10.05), power_index=0.166
- iterative [data_width=15 n_iter=16 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=268, accuracy_bits=10.8, luts=173, ffs=95, throughput_msps=10.2, max_abs_err=0.000548 (2^-10.83), power_index=0.192
- iterative [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=304, accuracy_bits=12.4, luts=197, ffs=108, throughput_msps=10.2, max_abs_err=0.000179 (2^-12.45), power_index=0.218
- iterative [data_width=20 n_iter=16 angle_guard=-2 frac_guard=0 rounding=trunc] luts_plus_ffs=326, accuracy_bits=13.3, luts=212, ffs=114, throughput_msps=10.2, max_abs_err=9.85e-05 (2^-13.31), power_index=0.233
- iterative [data_width=20 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=335, accuracy_bits=13.5, luts=218, ffs=117, throughput_msps=10.8, max_abs_err=8.71e-05 (2^-13.49), power_index=0.227
- iterative [data_width=20 n_iter=18 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=361, accuracy_bits=14.4, luts=244, ffs=117, throughput_msps=7.57, max_abs_err=4.53e-05 (2^-14.43), power_index=0.285
- iterative [data_width=20 n_iter=26 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=393, accuracy_bits=15.1, luts=270, ffs=123, throughput_msps=5.38, max_abs_err=2.91e-05 (2^-15.07), power_index=0.429
- iterative [data_width=20 n_iter=18 angle_guard=2 frac_guard=4 rounding=trunc] luts_plus_ffs=431, accuracy_bits=16, luts=304, ffs=127, throughput_msps=7.43, max_abs_err=1.54e-05 (2^-15.99), power_index=0.341
- iterative [data_width=28 n_iter=28 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=556, accuracy_bits=22, luts=398, ffs=158, throughput_msps=4.94, max_abs_err=2.4e-07 (2^-21.99), power_index=0.649
- iterative [data_width=28 n_iter=28 angle_guard=1 frac_guard=4 rounding=trunc] luts_plus_ffs=633, accuracy_bits=23.5, luts=467, ffs=166, throughput_msps=4.86, max_abs_err=8.37e-08 (2^-23.51), power_index=0.738
Front coverage: luts_plus_ffs 259..633 (HV reference 1500); accuracy_bits 10..23.5 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 170 evals, 128 feasible; max throughput seen 16.9 MSPS; best accuracy 23.51 bits; best feasible luts_plus_ffs=259; feasible ranges: data_width 14..28, n_iter 12..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 15 evals, 5 feasible; max throughput seen 14 MSPS; best accuracy 12.82 bits; best feasible luts_plus_ffs=372; feasible ranges: data_width 15..19, n_iter 12..15, angle_guard -1..1, frac_guard 2..2, k 2..4
- pipelined_m: 15 evals, 4 feasible; max throughput seen 171 MSPS; best accuracy 11.96 bits; best feasible luts_plus_ffs=884; feasible ranges: data_width 16..17, n_iter 12..15, angle_guard -1..0, frac_guard 0..2, m 4..7
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Target the HV-critical high-accuracy end and the selection-critical low-area corner of the iterative front.*)
- `iterative` (100 evals): data_width=26..28, n_iter=26..30, angle_guard=0..4, frac_guard=2..4, rounding=trunc|round. *Why:* only family on the front; same accuracy model as the others but lowest area
- clamped by code: dropped duplicate family iterative

**Result (code):** 100 evaluations this round, 300 total; 237 feasible; hypervolume 1.598e+04 (+12.2%).

**LLM decision:** `map_front` — Round 3 of 4 is done (300/400 evals); only one 100-eval round remains, which is exactly the reserved budget for final front mapping. The feasible front already spans luts_plus_ffs 259..705 against an HV reference of 1500, and accuracy_bits 10..25.5 against a reference of 10, with the min-area corner (iterative W=14 N=14, 259 luts+ffs, 10.05 bits, 11.7 MSPS) satisfying both constraints (throughput >= 1, err <= 2^-10). The only unexplored family, pipelined, is 1 result/cycle and therefore the most area-heavy; with area as the sole objective and the accuracy ceiling already near the 28-bit/30-iteration limit (best seen 25.52 bits), it is very unlikely to place a non-dominated point on a min-area front, so spending the last round exploring it would risk leaving the existing front under-mapped. Mapping the full ranges of the families already on the front (iterative, unrolled_k, pipelined_m) is the best use of the final 100 evals to fill any gaps in the 259..705 / 10..25.5 region and confirm the front before selection.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.598e+04 (gain this round: +12.2%).
Feasible designs: 237 of 300 evaluations (191 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 21% violate; best seen 2.08e-08 (2^-25.52)

Pareto front (feasible, 33 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=259, accuracy_bits=10, luts=168, ffs=91, throughput_msps=11.7, max_abs_err=0.000944 (2^-10.05), power_index=0.166
- iterative [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=293, accuracy_bits=12.3, luts=191, ffs=102, throughput_msps=11.7, max_abs_err=0.000204 (2^-12.26), power_index=0.187
- iterative [data_width=20 n_iter=16 angle_guard=-2 frac_guard=0 rounding=trunc] luts_plus_ffs=326, accuracy_bits=13.3, luts=212, ffs=114, throughput_msps=10.2, max_abs_err=9.85e-05 (2^-13.31), power_index=0.233
- iterative [data_width=20 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=344, accuracy_bits=14.1, luts=225, ffs=118, throughput_msps=10.2, max_abs_err=5.62e-05 (2^-14.12), power_index=0.246
- iterative [data_width=20 n_iter=26 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=393, accuracy_bits=15.1, luts=270, ffs=123, throughput_msps=5.38, max_abs_err=2.91e-05 (2^-15.07), power_index=0.429
- iterative [data_width=26 n_iter=28 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=523, accuracy_bits=21.3, luts=375, ffs=148, throughput_msps=4.94, max_abs_err=3.95e-07 (2^-21.27), power_index=0.61
- iterative [data_width=27 n_iter=28 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=571, accuracy_bits=22.5, luts=413, ffs=157, throughput_msps=4.94, max_abs_err=1.69e-07 (2^-22.50), power_index=0.665
- iterative [data_width=28 n_iter=28 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=597, accuracy_bits=23.7, luts=434, ffs=163, throughput_msps=4.94, max_abs_err=7.27e-08 (2^-23.71), power_index=0.697
- iterative [data_width=28 n_iter=27 angle_guard=4 frac_guard=3 rounding=trunc] luts_plus_ffs=622, accuracy_bits=24.5, luts=455, ffs=167, throughput_msps=5.02, max_abs_err=4.35e-08 (2^-24.45), power_index=0.702
- iterative [data_width=28 n_iter=30 angle_guard=4 frac_guard=3 rounding=round] luts_plus_ffs=705, accuracy_bits=25.5, luts=538, ffs=167, throughput_msps=4.56, max_abs_err=2.08e-08 (2^-25.52), power_index=0.876
Front coverage: luts_plus_ffs 259..705 (HV reference 1500); accuracy_bits 10..25.5 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 270 evals, 228 feasible; max throughput seen 16.9 MSPS; best accuracy 25.52 bits; best feasible luts_plus_ffs=259; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 15 evals, 5 feasible; max throughput seen 14 MSPS; best accuracy 12.82 bits; best feasible luts_plus_ffs=372; feasible ranges: data_width 15..19, n_iter 12..15, angle_guard -1..1, frac_guard 2..2, k 2..4
- pipelined_m: 15 evals, 4 feasible; max throughput seen 171 MSPS; best accuracy 11.96 bits; best feasible luts_plus_ffs=884; feasible ranges: data_width 16..17, n_iter 12..15, angle_guard -1..0, frac_guard 0..2, m 4..7
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=13..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (33 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 329 feasible; hypervolume 1.621e+04 (+1.4%).

**LLM decision:** `stop` — Final round and the full 400-eval budget is spent (400/400, 4/4 rounds). The front is feasible and well covered, so `infeasible` is not warranted: 0% of evaluations violate throughput (best seen 171 MSPS vs the >=1 MSPS constraint) and the error constraint is met with large margin (best 2.08e-08 = 2^-25.52 vs <=2^-10). The Pareto front spans luts_plus_ffs 259..705 against the HV reference 1500 and accuracy_bits 10..25.5 against the HV reference 10, i.e. it already covers the whole useful trade-off range, and the selection rule (min luts_plus_ffs) lands on iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 trunc] at 259 LUT+FF, 10.05 accuracy bits, 11.7 MSPS — comfortably inside both constraints. The last round added only +1.4% hypervolume, indicating the front has converged. The one unexplored family, pipelined, is a 1-result/cycle architecture whose nearest explored relative pipelined_m has best feasible luts_plus_ffs=884, ~3.4x the current area-optimal corner, so it cannot plausibly improve the min-area selection; with no budget left to map it, stopping is the correct call.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.621e+04 (gain this round: +1.4%).
Feasible designs: 329 of 400 evaluations (272 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 18% violate; best seen 2.08e-08 (2^-25.52)

Pareto front (feasible, 37 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=259, accuracy_bits=10, luts=168, ffs=91, throughput_msps=11.7, max_abs_err=0.000944 (2^-10.05), power_index=0.166
- iterative [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=293, accuracy_bits=12.3, luts=191, ffs=102, throughput_msps=11.7, max_abs_err=0.000204 (2^-12.26), power_index=0.187
- iterative [data_width=18 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=334, accuracy_bits=13.4, luts=226, ffs=108, throughput_msps=7.95, max_abs_err=9.26e-05 (2^-13.40), power_index=0.251
- iterative [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=345, accuracy_bits=14.6, luts=227, ffs=118, throughput_msps=10.2, max_abs_err=4.12e-05 (2^-14.57), power_index=0.247
- iterative [data_width=22 n_iter=22 angle_guard=4 frac_guard=0 rounding=trunc] luts_plus_ffs=420, accuracy_bits=16.3, luts=289, ffs=131, throughput_msps=6.24, max_abs_err=1.22e-05 (2^-16.32), power_index=0.395
- iterative [data_width=23 n_iter=24 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=458, accuracy_bits=18.4, luts=321, ffs=137, throughput_msps=5.78, max_abs_err=2.86e-06 (2^-18.42), power_index=0.465
- iterative [data_width=28 n_iter=28 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=556, accuracy_bits=22, luts=398, ffs=158, throughput_msps=4.94, max_abs_err=2.4e-07 (2^-21.99), power_index=0.649
- iterative [data_width=27 n_iter=28 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=595, accuracy_bits=23.6, luts=434, ffs=161, throughput_msps=4.94, max_abs_err=8.12e-08 (2^-23.55), power_index=0.694
- iterative [data_width=28 n_iter=27 angle_guard=4 frac_guard=3 rounding=trunc] luts_plus_ffs=622, accuracy_bits=24.5, luts=455, ffs=167, throughput_msps=5.02, max_abs_err=4.35e-08 (2^-24.45), power_index=0.702
- iterative [data_width=28 n_iter=30 angle_guard=4 frac_guard=3 rounding=round] luts_plus_ffs=705, accuracy_bits=25.5, luts=538, ffs=167, throughput_msps=4.56, max_abs_err=2.08e-08 (2^-25.52), power_index=0.876
Front coverage: luts_plus_ffs 259..705 (HV reference 1500); accuracy_bits 10..25.5 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 370 evals, 320 feasible; max throughput seen 16.9 MSPS; best accuracy 25.52 bits; best feasible luts_plus_ffs=259; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 15 evals, 5 feasible; max throughput seen 14 MSPS; best accuracy 12.82 bits; best feasible luts_plus_ffs=372; feasible ranges: data_width 15..19, n_iter 12..15, angle_guard -1..1, frac_guard 2..2, k 2..4
- pipelined_m: 15 evals, 4 feasible; max throughput seen 171 MSPS; best accuracy 11.96 bits; best feasible luts_plus_ffs=884; feasible ranges: data_width 16..17, n_iter 12..15, angle_guard -1..0, frac_guard 0..2, m 4..7
```
</details>

## LLM usage
- calls: 6 (failed/unparsed attempts: 1)
- tokens: 14084 in, 16997 out
- provider-reported cost: $0.0145
- full prompts and replies: `llm_trace.jsonl`

