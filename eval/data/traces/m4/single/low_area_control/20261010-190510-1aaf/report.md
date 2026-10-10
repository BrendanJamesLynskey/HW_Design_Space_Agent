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
`iterative:data_width=14,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 170 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 92 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 11 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 90.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.177 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000648 (2^-10.59) | exact: bit-accurate model, exhaustive (16384 angles) |
| max_abs_err_lsb | 2.65 | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err | 0.000179 (2^-12.45) | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err_lsb | 0.733 | exact: bit-accurate model, exhaustive (16384 angles) |
| accuracy_bits | 10.6 | exact: bit-accurate model, exhaustive (16384 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 18 cycles, a new input every 18 cycle(s). DDS tone from its exact outputs: SFDR 77.6 dBc, SNR 72.1 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (40 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=14,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc` | 170 | 92 | 11.0 | 18 | 0.177 | 0.000648 (2^-10.59) | 10.59 |
| 1 | `iterative:data_width=16,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc` | 170 | 96 | 11.0 | 18 | 0.18 | 0.000643 (2^-10.60) | 10.60 |
| 2 | `iterative:data_width=15,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc` | 181 | 97 | 11.0 | 18 | 0.188 | 0.000344 (2^-11.51) | 11.51 |
| 3 | `iterative:data_width=17,n_iter=15,angle_guard=3,frac_guard=0,rounding=trunc` | 187 | 104 | 10.8 | 18 | 0.197 | 0.000307 (2^-11.67) | 11.67 |
| 4 | `iterative:data_width=17,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 193 | 103 | 10.2 | 19 | 0.211 | 0.000139 (2^-12.81) | 12.81 |
| 5 | `iterative:data_width=18,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 200 | 106 | 10.4 | 19 | 0.219 | 0.000121 (2^-13.02) | 13.02 |
| 6 | `iterative:data_width=19,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 214 | 112 | 10.8 | 18 | 0.221 | 8.66e-05 (2^-13.50) | 13.50 |
| 7 | `iterative:data_width=20,n_iter=15,angle_guard=2,frac_guard=0,rounding=trunc` | 219 | 118 | 10.8 | 18 | 0.229 | 8.43e-05 (2^-13.53) | 13.53 |
| 8 | `iterative:data_width=19,n_iter=20,angle_guard=3,frac_guard=0,rounding=trunc` | 233 | 115 | 6.9 | 23 | 0.301 | 7.8e-05 (2^-13.65) | 13.65 |
| 9 | `iterative:data_width=20,n_iter=15,angle_guard=2,frac_guard=1,rounding=trunc` | 229 | 120 | 10.8 | 18 | 0.236 | 7.32e-05 (2^-13.74) | 13.74 |
| 10 | `iterative:data_width=19,n_iter=26,angle_guard=0,frac_guard=0,rounding=round` | 245 | 112 | 5.5 | 29 | 0.389 | 6.48e-05 (2^-13.91) | 13.91 |
| 11 | `iterative:data_width=19,n_iter=16,angle_guard=3,frac_guard=3,rounding=trunc` | 239 | 120 | 10.2 | 19 | 0.256 | 4.32e-05 (2^-14.50) | 14.50 |
| 12 | `iterative:data_width=19,n_iter=30,angle_guard=2,frac_guard=2,rounding=trunc` | 265 | 118 | 4.8 | 33 | 0.475 | 4.16e-05 (2^-14.55) | 14.55 |
| 13 | `iterative:data_width=19,n_iter=21,angle_guard=4,frac_guard=2,rounding=trunc` | 268 | 120 | 6.5 | 24 | 0.35 | 2.55e-05 (2^-15.26) | 15.26 |
| 14 | `iterative:data_width=19,n_iter=25,angle_guard=3,frac_guard=3,rounding=trunc` | 282 | 121 | 5.7 | 28 | 0.425 | 2.05e-05 (2^-15.58) | 15.58 |
| 15 | `iterative:data_width=20,n_iter=24,angle_guard=2,frac_guard=2,rounding=trunc` | 282 | 123 | 5.9 | 27 | 0.411 | 1.54e-05 (2^-15.99) | 15.99 |
| 16 | `iterative:data_width=23,n_iter=22,angle_guard=-2,frac_guard=0,rounding=trunc` | 296 | 130 | 6.2 | 25 | 0.401 | 1.44e-05 (2^-16.08) | 16.08 |
| 17 | `iterative:data_width=20,n_iter=27,angle_guard=3,frac_guard=3,rounding=trunc` | 301 | 126 | 5.2 | 30 | 0.482 | 1.03e-05 (2^-16.56) | 16.56 |
| 18 | `iterative:data_width=23,n_iter=21,angle_guard=-1,frac_guard=0,rounding=trunc` | 298 | 131 | 6.5 | 24 | 0.387 | 8.62e-06 (2^-16.82) | 16.82 |
| 19 | `iterative:data_width=23,n_iter=25,angle_guard=0,frac_guard=0,rounding=trunc` | 301 | 132 | 5.6 | 28 | 0.456 | 6.79e-06 (2^-17.17) | 17.17 |
| 20 | `iterative:data_width=23,n_iter=25,angle_guard=0,frac_guard=0,rounding=round` | 316 | 132 | 5.6 | 28 | 0.472 | 3.98e-06 (2^-17.94) | 17.94 |
| 21 | `iterative:data_width=23,n_iter=27,angle_guard=0,frac_guard=0,rounding=round` | 316 | 132 | 5.2 | 30 | 0.506 | 3.98e-06 (2^-17.94) | 17.94 |
| 22 | `iterative:data_width=23,n_iter=22,angle_guard=3,frac_guard=0,rounding=round` | 319 | 135 | 6.2 | 25 | 0.427 | 2.9e-06 (2^-18.39) | 18.39 |
| 23 | `iterative:data_width=23,n_iter=21,angle_guard=3,frac_guard=2,rounding=trunc` | 336 | 139 | 6.5 | 24 | 0.429 | 2.24e-06 (2^-18.77) | 18.77 |
| 24 | `iterative:data_width=24,n_iter=22,angle_guard=2,frac_guard=1,rounding=trunc` | 336 | 141 | 6.2 | 25 | 0.449 | 1.76e-06 (2^-19.11) | 19.11 |
| 25 | `iterative:data_width=24,n_iter=28,angle_guard=2,frac_guard=0,rounding=round` | 339 | 139 | 5.0 | 31 | 0.557 | 1.57e-06 (2^-19.28) | 19.28 |
| 26 | `iterative:data_width=25,n_iter=23,angle_guard=3,frac_guard=0,rounding=trunc` | 340 | 145 | 5.9 | 26 | 0.475 | 1.45e-06 (2^-19.40) | 19.40 |
| 27 | `iterative:data_width=24,n_iter=23,angle_guard=3,frac_guard=2,rounding=trunc` | 354 | 144 | 5.9 | 26 | 0.487 | 9.42e-07 (2^-20.02) | 20.02 |
| 28 | `iterative:data_width=25,n_iter=23,angle_guard=3,frac_guard=0,rounding=round` | 353 | 145 | 5.9 | 26 | 0.488 | 8.23e-07 (2^-20.21) | 20.21 |
| 29 | `iterative:data_width=25,n_iter=26,angle_guard=3,frac_guard=0,rounding=round` | 360 | 145 | 5.3 | 29 | 0.551 | 7.53e-07 (2^-20.34) | 20.34 |
| 30 | `iterative:data_width=27,n_iter=29,angle_guard=0,frac_guard=0,rounding=trunc` | 379 | 152 | 4.8 | 32 | 0.639 | 5.1e-07 (2^-20.90) | 20.90 |
| 31 | `iterative:data_width=25,n_iter=23,angle_guard=3,frac_guard=3,rounding=trunc` | 387 | 151 | 5.9 | 26 | 0.526 | 4.81e-07 (2^-20.99) | 20.99 |
| 32 | `iterative:data_width=27,n_iter=28,angle_guard=0,frac_guard=0,rounding=round` | 392 | 152 | 4.9 | 31 | 0.635 | 3.4e-07 (2^-21.49) | 21.49 |
| 33 | `iterative:data_width=27,n_iter=23,angle_guard=3,frac_guard=2,rounding=trunc` | 406 | 159 | 5.9 | 26 | 0.553 | 3.16e-07 (2^-21.59) | 21.59 |
| 34 | `iterative:data_width=27,n_iter=26,angle_guard=0,frac_guard=2,rounding=trunc` | 411 | 156 | 5.3 | 29 | 0.619 | 2.81e-07 (2^-21.76) | 21.76 |
| 35 | `iterative:data_width=27,n_iter=26,angle_guard=1,frac_guard=2,rounding=trunc` | 413 | 157 | 5.3 | 29 | 0.622 | 1.72e-07 (2^-22.47) | 22.47 |
| 36 | `iterative:data_width=28,n_iter=26,angle_guard=3,frac_guard=0,rounding=round` | 417 | 160 | 5.2 | 29 | 0.629 | 1.1e-07 (2^-23.12) | 23.12 |
| 37 | `iterative:data_width=27,n_iter=26,angle_guard=4,frac_guard=3,rounding=trunc` | 436 | 162 | 5.2 | 29 | 0.653 | 9.29e-08 (2^-23.36) | 23.36 |
| 38 | `iterative:data_width=27,n_iter=26,angle_guard=3,frac_guard=4,rounding=trunc` | 451 | 163 | 5.2 | 29 | 0.67 | 8.5e-08 (2^-23.49) | 23.49 |
| 39 | `iterative:data_width=27,n_iter=26,angle_guard=3,frac_guard=3,rounding=round` | 506 | 161 | 5.3 | 29 | 0.728 | 7.41e-08 (2^-23.69) | 23.69 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraint is accuracy, not speed: with N micro-rotations the residual angle error is ~2^-(N-1) and the output LSB is 2^-(W-2), so max_abs_err <= 2^-10 needs roughly W >= 12 and N >= 11. The throughput floor of 1 MSPS is trivial for every family (even iterative at N=14 with Fmax ~100 MHz gives several MSPS), so throughput does not shape the front. The objectives therefore reduce to a pure area-vs-accuracy trade-off, and the HV reference point (1500, 10) means only designs with accuracy_bits >= 10 and luts_plus_ffs <= 1500 contribute. Round 1 should (a) put most budget on the family that shares its datapath and should give the smallest area (iterative), (b) probe pipelined_m, the only real area competitor because for small N it trades barrel shifters for a few register stages, and (c) cheaply confirm that unrolled_k and pipelined are dominated. Ranges are kept wide enough to bracket the accuracy threshold (W 11..20, N 10..20) and the guard-bit axes, so later rounds can narrow around the feasible corner and the upper end of the front.*)
- `iterative` (55 evals): data_width=11..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Shared datapath (3 adders + 2 barrel shifters + FSM) with only ~3W state is the natural minimum-area candidate, and at N~12-16 it still clears 1 MSPS by a wide margin. This family should own the low-area end of the front and the selection rule (min luts_plus_ffs), so it gets the largest share and full guard-bit/rounding coverage to find the smallest W,N that reaches 10 bits.
- `pipelined_m` (20 evals): data_width=11..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Closest area competitor to iterative: fixed (wiring-only) shifts instead of barrel shifters, paid for with ceil(N/m) register stages. For small N and large m this can approach iterative's area, and it is the only other family that could plausibly sit on the area-vs-accuracy front, so it deserves a real probe across the full m range.
- `unrolled_k` (15 evals): data_width=11..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* Replicates the datapath k times, so for k>=2 it should cost more area than iterative at equal accuracy and is expected to be dominated. A small share is enough to confirm this and to catch any surprise where a k=2 schedule with fewer guard bits lands on the front.
- `pipelined` (10 evals): data_width=11..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* One full register stage per micro-rotation is the most area-expensive structure for N>=11 and its 1 result/cycle throughput is far beyond what the 1 MSPS constraint needs, so it is almost certainly dominated. A minimal share is kept only as a sanity check on the cost model and to bound the front from above.

**Result (code):** 100 evaluations this round, 100 total; 67 feasible; hypervolume 5359 (n/a).

**LLM decision:** `map_front` — The feasible front is entirely `iterative` (8 designs), and it is narrow on both objectives: luts_plus_ffs spans only 266..359 against the HV reference of 1500, and accuracy_bits spans 10.6..14.5 against a reference of 10. The throughput constraint is trivially satisfied by every family (best seen 282 MSPS vs the 1 MSPS floor), so the real trade-off is purely area-vs-accuracy and the cheaper `iterative` family dominates the pipelined variants (pipelined_m best feasible area 924, pipelined 1810, both far above iterative's 266). The selection rule (min luts_plus_ffs) is already served by the 266 design, but hypervolume is not: the front covers only a small slice of the area axis and stops at 14.5 accuracy bits while the registry allows data_width up to 28 and n_iter up to 30. So the right move is to let code spend this round mapping the whole front over the full ranges of the family that is on it (iterative), seeded with the current front, to extend the curve toward higher accuracy/area and fill the gap up to the HV reference point.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 5359 (gain this round: n/a (first round)).
Feasible designs: 67 of 100 evaluations (61 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 33% violate; best seen 4.32e-05 (2^-14.50)

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=266, accuracy_bits=10.6, luts=170, ffs=96, throughput_msps=11, max_abs_err=0.000643 (2^-10.60), power_index=0.18
- iterative [data_width=15 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=278, accuracy_bits=11.5, luts=181, ffs=97, throughput_msps=11, max_abs_err=0.000344 (2^-11.51), power_index=0.188
- iterative [data_width=17 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=291, accuracy_bits=11.7, luts=187, ffs=104, throughput_msps=10.8, max_abs_err=0.000307 (2^-11.67), power_index=0.197
- iterative [data_width=17 n_iter=15 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=302, accuracy_bits=12.5, luts=197, ffs=106, throughput_msps=10.8, max_abs_err=0.000173 (2^-12.49), power_index=0.205
- iterative [data_width=17 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=313, accuracy_bits=12.7, luts=210, ffs=103, throughput_msps=8.1, max_abs_err=0.000149 (2^-12.71), power_index=0.235
- iterative [data_width=19 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=326, accuracy_bits=13.5, luts=214, ffs=112, throughput_msps=10.8, max_abs_err=8.66e-05 (2^-13.50), power_index=0.221
- iterative [data_width=19 n_iter=20 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=348, accuracy_bits=13.6, luts=233, ffs=115, throughput_msps=6.91, max_abs_err=7.8e-05 (2^-13.65), power_index=0.301
- iterative [data_width=19 n_iter=16 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=359, accuracy_bits=14.5, luts=239, ffs=120, throughput_msps=10.2, max_abs_err=4.32e-05 (2^-14.50), power_index=0.256
Front coverage: luts_plus_ffs 266..359 (HV reference 1500); accuracy_bits 10.6..14.5 (HV reference 10); data_width on the front 15..19 (registry 8..28).

Per family:
- iterative: 55 evals, 42 feasible; max throughput seen 15.6 MSPS; best accuracy 14.50 bits; best feasible luts_plus_ffs=266; feasible ranges: data_width 14..20, n_iter 12..20, angle_guard -2..3, frac_guard 0..4
- unrolled_k: 15 evals, 7 feasible; max throughput seen 13.5 MSPS; best accuracy 12.23 bits; best feasible luts_plus_ffs=364; feasible ranges: data_width 14..17, n_iter 12..18, angle_guard 0..4, frac_guard 0..4, k 2..8
- pipelined: 10 evals, 2 feasible; max throughput seen 282 MSPS; best accuracy 11.60 bits; best feasible luts_plus_ffs=1810; feasible ranges: data_width 16..18, n_iter 16..16, angle_guard -2..-1, frac_guard 1..1
- pipelined_m: 20 evals, 16 feasible; max throughput seen 171 MSPS; best accuracy 14.34 bits; best feasible luts_plus_ffs=924; feasible ranges: data_width 13..19, n_iter 12..20, angle_guard -1..4, frac_guard 1..4, m 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=14..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (8 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 160 feasible; hypervolume 1.457e+04 (+171.9%).

**LLM decision:** `map_front` — The feasible front (27 designs, all from the `iterative` family) already spans the accuracy objective well: 10.6..23.7 bits against the HV ref of 10. But it occupies only a narrow area band, luts_plus_ffs 266..667 against the HV reference of 1500 — i.e. the front dies out well before the reference point, and no design between ~667 and 1500 area is on it. Combined with the per-family evidence that pipelined (best feasible area 1810) and pipelined_m (best feasible area 924) are strictly dominated for a spec that only needs >=1 MSPS (iterative already yields 11 MSPS at the frontier, throughput is not an objective), the entire trade-off curve lives in `iterative`, so mapping should be done over that family's full registry ranges. Two deficits remain that a full-range NSGA-II pass can close: (a) the low-area endpoint — min data_width on the front is 16 (10.6 bits), while `iterative` was feasible down to data_width 14, so a slightly cheaper design that still clears the 2^-10 constraint may exist below 266; (b) the high-accuracy endpoint — max seen is 23.69 bits at data_width 27/n_iter 26, with data_width 28 and n_iter up to 30 only partially probed, so higher-accuracy (higher-area) points that raise HV toward the 1500 ref are unexplored. Round 3 is therefore best spent letting code map the whole front over the full `iterative` ranges seeded with the current front; the selection rule's pick (min luts_plus_ffs = 266) is already on the front, so this round is purely about widening HV coverage before the final round.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.457e+04 (gain this round: +171.9%).
Feasible designs: 160 of 200 evaluations (147 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 20% violate; best seen 7.41e-08 (2^-23.69)

Pareto front (feasible, 27 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=16 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=266, accuracy_bits=10.6, luts=170, ffs=96, throughput_msps=11, max_abs_err=0.000643 (2^-10.60), power_index=0.18
- iterative [data_width=17 n_iter=15 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=302, accuracy_bits=12.5, luts=197, ffs=106, throughput_msps=10.8, max_abs_err=0.000173 (2^-12.49), power_index=0.205
- iterative [data_width=19 n_iter=20 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=348, accuracy_bits=13.6, luts=233, ffs=115, throughput_msps=6.91, max_abs_err=7.8e-05 (2^-13.65), power_index=0.301
- iterative [data_width=19 n_iter=30 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=383, accuracy_bits=14.6, luts=265, ffs=118, throughput_msps=4.82, max_abs_err=4.16e-05 (2^-14.55), power_index=0.475
- iterative [data_width=20 n_iter=24 angle_guard=3 frac_guard=4 rounding=trunc] luts_plus_ffs=443, accuracy_bits=17, luts=315, ffs=128, throughput_msps=5.78, max_abs_err=7.48e-06 (2^-17.03), power_index=0.45
- iterative [data_width=21 n_iter=25 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=451, accuracy_bits=17.7, luts=320, ffs=131, throughput_msps=5.57, max_abs_err=4.7e-06 (2^-17.70), power_index=0.475
- iterative [data_width=25 n_iter=23 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=485, accuracy_bits=19.4, luts=340, ffs=145, throughput_msps=5.89, max_abs_err=1.45e-06 (2^-19.40), power_index=0.475
- iterative [data_width=25 n_iter=26 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=505, accuracy_bits=20.3, luts=360, ffs=145, throughput_msps=5.28, max_abs_err=7.53e-07 (2^-20.34), power_index=0.551
- iterative [data_width=28 n_iter=26 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=577, accuracy_bits=23.1, luts=417, ffs=160, throughput_msps=5.19, max_abs_err=1.1e-07 (2^-23.12), power_index=0.629
- iterative [data_width=27 n_iter=26 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=667, accuracy_bits=23.7, luts=506, ffs=161, throughput_msps=5.28, max_abs_err=7.41e-08 (2^-23.69), power_index=0.728
Front coverage: luts_plus_ffs 266..667 (HV reference 1500); accuracy_bits 10.6..23.7 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 155 evals, 135 feasible; max throughput seen 15.6 MSPS; best accuracy 23.69 bits; best feasible luts_plus_ffs=266; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 15 evals, 7 feasible; max throughput seen 13.5 MSPS; best accuracy 12.23 bits; best feasible luts_plus_ffs=364; feasible ranges: data_width 14..17, n_iter 12..18, angle_guard 0..4, frac_guard 0..4, k 2..8
- pipelined: 10 evals, 2 feasible; max throughput seen 282 MSPS; best accuracy 11.60 bits; best feasible luts_plus_ffs=1810; feasible ranges: data_width 16..18, n_iter 16..16, angle_guard -2..-1, frac_guard 1..1
- pipelined_m: 20 evals, 16 feasible; max throughput seen 171 MSPS; best accuracy 14.34 bits; best feasible luts_plus_ffs=924; feasible ranges: data_width 13..19, n_iter 12..20, angle_guard -1..4, frac_guard 1..4, m 2..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=14..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (27 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 300 total; 255 feasible; hypervolume 1.463e+04 (+0.4%).

**LLM decision:** `map_front` — The feasible front is entirely `iterative`: its 40 designs span luts_plus_ffs 262..667 and accuracy_bits 10.6..23.7, and the selection-rule winner is already present (iterative dW=14/N=15/ag=2/fg=2/trunc, luts_plus_ffs=262, max_abs_err=6.48e-4 < 9.77e-4, throughput 11 MSPS >= 1). Every other family is dominated on the front's objectives: unrolled_k best 364 @ 12.23 bits, pipelined_m best 924 @ 14.34 bits, pipelined best 1810 @ 11.60 bits — all worse in area at equal-or-lower accuracy than iterative's 302 @ 12.5 and 348 @ 13.6. Accuracy is already near the registry ceiling (23.7 bits at data_width 28), and the area end is well below the HV reference (667 vs 1500), so the +0.4% HV gain this round indicates the curve is close to saturated. With 100 evals left and one round remaining, the right use of the reserved budget is the code-driven full-range front mapping of `iterative` (seeded with the current front) to confirm coverage across data_width 8..28, n_iter 4..30, angle_guard -2..4, frac_guard 0..4 and rounding, and to check whether any lower-area point exists near the 10-bit accuracy constraint.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.463e+04 (gain this round: +0.4%).
Feasible designs: 255 of 300 evaluations (235 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 15% violate; best seen 7.41e-08 (2^-23.69)

Pareto front (feasible, 40 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=262, accuracy_bits=10.6, luts=170, ffs=92, throughput_msps=11, max_abs_err=0.000648 (2^-10.59), power_index=0.177
- iterative [data_width=17 n_iter=15 angle_guard=3 frac_guard=1 rounding=trunc] luts_plus_ffs=302, accuracy_bits=12.5, luts=197, ffs=106, throughput_msps=10.8, max_abs_err=0.000173 (2^-12.49), power_index=0.205
- iterative [data_width=19 n_iter=20 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=348, accuracy_bits=13.6, luts=233, ffs=115, throughput_msps=6.91, max_abs_err=7.8e-05 (2^-13.65), power_index=0.301
- iterative [data_width=19 n_iter=30 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=383, accuracy_bits=14.6, luts=265, ffs=118, throughput_msps=4.82, max_abs_err=4.16e-05 (2^-14.55), power_index=0.475
- iterative [data_width=23 n_iter=22 angle_guard=-2 frac_guard=0 rounding=trunc] luts_plus_ffs=426, accuracy_bits=16.1, luts=296, ffs=130, throughput_msps=6.24, max_abs_err=1.44e-05 (2^-16.08), power_index=0.401
- iterative [data_width=21 n_iter=23 angle_guard=4 frac_guard=3 rounding=trunc] luts_plus_ffs=451, accuracy_bits=17.8, luts=319, ffs=132, throughput_msps=6, max_abs_err=4.53e-06 (2^-17.75), power_index=0.441
- iterative [data_width=25 n_iter=23 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=485, accuracy_bits=19.4, luts=340, ffs=145, throughput_msps=5.89, max_abs_err=1.45e-06 (2^-19.40), power_index=0.475
- iterative [data_width=24 n_iter=24 angle_guard=3 frac_guard=4 rounding=trunc] luts_plus_ffs=533, accuracy_bits=20.9, luts=385, ffs=148, throughput_msps=5.68, max_abs_err=5.27e-07 (2^-20.86), power_index=0.542
- iterative [data_width=27 n_iter=26 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=571, accuracy_bits=22.5, luts=413, ffs=157, throughput_msps=5.28, max_abs_err=1.72e-07 (2^-22.47), power_index=0.622
- iterative [data_width=27 n_iter=26 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=667, accuracy_bits=23.7, luts=506, ffs=161, throughput_msps=5.28, max_abs_err=7.41e-08 (2^-23.69), power_index=0.728
Front coverage: luts_plus_ffs 262..667 (HV reference 1500); accuracy_bits 10.6..23.7 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 255 evals, 230 feasible; max throughput seen 15.6 MSPS; best accuracy 23.69 bits; best feasible luts_plus_ffs=262; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 15 evals, 7 feasible; max throughput seen 13.5 MSPS; best accuracy 12.23 bits; best feasible luts_plus_ffs=364; feasible ranges: data_width 14..17, n_iter 12..18, angle_guard 0..4, frac_guard 0..4, k 2..8
- pipelined: 10 evals, 2 feasible; max throughput seen 282 MSPS; best accuracy 11.60 bits; best feasible luts_plus_ffs=1810; feasible ranges: data_width 16..18, n_iter 16..16, angle_guard -2..-1, frac_guard 1..1
- pipelined_m: 20 evals, 16 feasible; max throughput seen 171 MSPS; best accuracy 14.34 bits; best feasible luts_plus_ffs=924; feasible ranges: data_width 13..19, n_iter 12..20, angle_guard -1..4, frac_guard 1..4, m 2..8
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=13..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (40 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 350 feasible; hypervolume 1.466e+04 (+0.2%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), and the front is feasible and well covered: 350/400 evaluations feasible, 40 designs on the Pareto front spanning luts_plus_ffs 262..667 against HV reference 1500 and accuracy_bits 10.6..23.7 against HV reference 10, with data_width covering 14..28 of the registry's 8..28. Both constraints are comfortably satisfiable — 0% throughput violations (best 282 MSPS vs >=1 required) and only 12% error violations (best 2^-23.69 vs <=2^-10 required) — so the spec is not infeasible. The selection rule (min luts_plus_ffs) is already served by the front's smallest point, iterative [data_width=14 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] at luts_plus_ffs=262, accuracy_bits=10.6 (max_abs_err 2^-10.59 <= 2^-10) and 11 MSPS >= 1 MSPS, and hypervolume gained only +0.2% this round, indicating the front has converged. No further exploration is warranted.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.466e+04 (gain this round: +0.2%).
Feasible designs: 350 of 400 evaluations (319 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 12% violate; best seen 7.41e-08 (2^-23.69)

Pareto front (feasible, 40 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=262, accuracy_bits=10.6, luts=170, ffs=92, throughput_msps=11, max_abs_err=0.000648 (2^-10.59), power_index=0.177
- iterative [data_width=17 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=296, accuracy_bits=12.8, luts=193, ffs=103, throughput_msps=10.2, max_abs_err=0.000139 (2^-12.81), power_index=0.211
- iterative [data_width=20 n_iter=15 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=349, accuracy_bits=13.7, luts=229, ffs=120, throughput_msps=10.8, max_abs_err=7.32e-05 (2^-13.74), power_index=0.236
- iterative [data_width=19 n_iter=21 angle_guard=4 frac_guard=2 rounding=trunc] luts_plus_ffs=388, accuracy_bits=15.3, luts=268, ffs=120, throughput_msps=6.5, max_abs_err=2.55e-05 (2^-15.26), power_index=0.35
- iterative [data_width=20 n_iter=27 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=427, accuracy_bits=16.6, luts=301, ffs=126, throughput_msps=5.2, max_abs_err=1.03e-05 (2^-16.56), power_index=0.482
- iterative [data_width=23 n_iter=22 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=454, accuracy_bits=18.4, luts=319, ffs=135, throughput_msps=6.24, max_abs_err=2.9e-06 (2^-18.39), power_index=0.427
- iterative [data_width=25 n_iter=23 angle_guard=3 frac_guard=0 rounding=trunc] luts_plus_ffs=485, accuracy_bits=19.4, luts=340, ffs=145, throughput_msps=5.89, max_abs_err=1.45e-06 (2^-19.40), power_index=0.475
- iterative [data_width=27 n_iter=29 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=531, accuracy_bits=20.9, luts=379, ffs=152, throughput_msps=4.79, max_abs_err=5.1e-07 (2^-20.90), power_index=0.639
- iterative [data_width=27 n_iter=26 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=571, accuracy_bits=22.5, luts=413, ffs=157, throughput_msps=5.28, max_abs_err=1.72e-07 (2^-22.47), power_index=0.622
- iterative [data_width=27 n_iter=26 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=667, accuracy_bits=23.7, luts=506, ffs=161, throughput_msps=5.28, max_abs_err=7.41e-08 (2^-23.69), power_index=0.728
Front coverage: luts_plus_ffs 262..667 (HV reference 1500); accuracy_bits 10.6..23.7 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 355 evals, 325 feasible; max throughput seen 15.6 MSPS; best accuracy 23.69 bits; best feasible luts_plus_ffs=262; feasible ranges: data_width 13..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 15 evals, 7 feasible; max throughput seen 13.5 MSPS; best accuracy 12.23 bits; best feasible luts_plus_ffs=364; feasible ranges: data_width 14..17, n_iter 12..18, angle_guard 0..4, frac_guard 0..4, k 2..8
- pipelined: 10 evals, 2 feasible; max throughput seen 282 MSPS; best accuracy 11.60 bits; best feasible luts_plus_ffs=1810; feasible ranges: data_width 16..18, n_iter 16..16, angle_guard -2..-1, frac_guard 1..1
- pipelined_m: 20 evals, 16 feasible; max throughput seen 171 MSPS; best accuracy 14.34 bits; best feasible luts_plus_ffs=924; feasible ranges: data_width 13..19, n_iter 12..20, angle_guard -1..4, frac_guard 1..4, m 2..8
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 15152 in, 12101 out
- provider-reported cost: $0.0103
- full prompts and replies: `llm_trace.jsonl`

