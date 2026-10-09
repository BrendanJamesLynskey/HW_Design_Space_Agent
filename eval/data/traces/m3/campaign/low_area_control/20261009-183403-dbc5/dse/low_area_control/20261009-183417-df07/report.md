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

## Pareto front (36 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=16,angle_guard=1,frac_guard=1,rounding=trunc` | 170 | 94 | 10.4 | 19 | 0.189 | 0.000594 (2^-10.72) | 10.72 |
| 1 | `iterative:data_width=15,n_iter=15,angle_guard=2,frac_guard=1,rounding=trunc` | 172 | 95 | 11.0 | 18 | 0.181 | 0.000567 (2^-10.78) | 10.78 |
| 2 | `iterative:data_width=14,n_iter=16,angle_guard=4,frac_guard=3,rounding=trunc` | 183 | 96 | 10.4 | 19 | 0.199 | 0.000427 (2^-11.19) | 11.19 |
| 3 | `iterative:data_width=16,n_iter=16,angle_guard=1,frac_guard=1,rounding=trunc` | 181 | 99 | 10.4 | 19 | 0.2 | 0.000333 (2^-11.55) | 11.55 |
| 4 | `iterative:data_width=17,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 191 | 102 | 10.4 | 19 | 0.209 | 0.000149 (2^-12.71) | 12.71 |
| 5 | `iterative:data_width=17,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 193 | 103 | 10.2 | 19 | 0.211 | 0.000139 (2^-12.81) | 12.81 |
| 6 | `iterative:data_width=18,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc` | 206 | 110 | 10.2 | 19 | 0.226 | 8.82e-05 (2^-13.47) | 13.47 |
| 7 | `iterative:data_width=18,n_iter=20,angle_guard=2,frac_guard=0,rounding=round` | 228 | 109 | 6.9 | 23 | 0.291 | 7.75e-05 (2^-13.65) | 13.65 |
| 8 | `iterative:data_width=18,n_iter=16,angle_guard=2,frac_guard=3,rounding=trunc` | 225 | 114 | 10.2 | 19 | 0.243 | 5.94e-05 (2^-14.04) | 14.04 |
| 9 | `iterative:data_width=18,n_iter=16,angle_guard=4,frac_guard=3,rounding=trunc` | 229 | 116 | 10.2 | 19 | 0.247 | 5.23e-05 (2^-14.22) | 14.22 |
| 10 | `iterative:data_width=19,n_iter=17,angle_guard=2,frac_guard=0,rounding=round` | 244 | 114 | 7.9 | 20 | 0.269 | 4.23e-05 (2^-14.53) | 14.53 |
| 11 | `iterative:data_width=21,n_iter=16,angle_guard=3,frac_guard=1,rounding=trunc` | 242 | 126 | 10.0 | 19 | 0.263 | 3.85e-05 (2^-14.67) | 14.67 |
| 12 | `iterative:data_width=19,n_iter=20,angle_guard=3,frac_guard=2,rounding=trunc` | 262 | 119 | 6.9 | 23 | 0.33 | 2.62e-05 (2^-15.22) | 15.22 |
| 13 | `iterative:data_width=20,n_iter=30,angle_guard=1,frac_guard=2,rounding=trunc` | 280 | 122 | 4.8 | 33 | 0.499 | 2.15e-05 (2^-15.51) | 15.51 |
| 14 | `iterative:data_width=22,n_iter=20,angle_guard=1,frac_guard=0,rounding=trunc` | 278 | 128 | 6.8 | 23 | 0.351 | 1.22e-05 (2^-16.32) | 16.32 |
| 15 | `iterative:data_width=20,n_iter=20,angle_guard=3,frac_guard=3,rounding=trunc` | 292 | 126 | 6.8 | 23 | 0.362 | 9.41e-06 (2^-16.70) | 16.70 |
| 16 | `iterative:data_width=21,n_iter=20,angle_guard=3,frac_guard=2,rounding=trunc` | 294 | 129 | 6.8 | 23 | 0.366 | 7.58e-06 (2^-17.01) | 17.01 |
| 17 | `iterative:data_width=23,n_iter=20,angle_guard=2,frac_guard=0,rounding=trunc` | 296 | 134 | 6.8 | 23 | 0.372 | 6.2e-06 (2^-17.30) | 17.30 |
| 18 | `iterative:data_width=23,n_iter=24,angle_guard=2,frac_guard=0,rounding=trunc` | 303 | 134 | 5.8 | 27 | 0.444 | 5.84e-06 (2^-17.39) | 17.39 |
| 19 | `iterative:data_width=21,n_iter=20,angle_guard=3,frac_guard=3,rounding=trunc` | 308 | 131 | 6.8 | 23 | 0.38 | 5.52e-06 (2^-17.47) | 17.47 |
| 20 | `iterative:data_width=23,n_iter=25,angle_guard=2,frac_guard=0,rounding=round` | 320 | 134 | 5.6 | 28 | 0.478 | 2.9e-06 (2^-18.39) | 18.39 |
| 21 | `iterative:data_width=24,n_iter=23,angle_guard=4,frac_guard=0,rounding=round` | 338 | 141 | 5.9 | 26 | 0.469 | 1.62e-06 (2^-19.24) | 19.24 |
| 22 | `iterative:data_width=25,n_iter=25,angle_guard=2,frac_guard=0,rounding=trunc` | 343 | 144 | 5.5 | 28 | 0.513 | 1.47e-06 (2^-19.37) | 19.37 |
| 23 | `iterative:data_width=25,n_iter=23,angle_guard=2,frac_guard=0,rounding=round` | 352 | 144 | 5.9 | 26 | 0.485 | 8.71e-07 (2^-20.13) | 20.13 |
| 24 | `iterative:data_width=25,n_iter=23,angle_guard=3,frac_guard=0,rounding=round` | 353 | 145 | 5.9 | 26 | 0.488 | 8.23e-07 (2^-20.21) | 20.21 |
| 25 | `iterative:data_width=25,n_iter=29,angle_guard=2,frac_guard=0,rounding=round` | 359 | 144 | 4.8 | 32 | 0.606 | 8.15e-07 (2^-20.23) | 20.23 |
| 26 | `iterative:data_width=26,n_iter=23,angle_guard=1,frac_guard=1,rounding=trunc` | 369 | 150 | 5.9 | 26 | 0.508 | 5.95e-07 (2^-20.68) | 20.68 |
| 27 | `iterative:data_width=25,n_iter=28,angle_guard=2,frac_guard=2,rounding=trunc` | 377 | 148 | 4.9 | 31 | 0.613 | 5.15e-07 (2^-20.89) | 20.89 |
| 28 | `iterative:data_width=26,n_iter=27,angle_guard=2,frac_guard=0,rounding=round` | 377 | 149 | 5.1 | 30 | 0.594 | 3.74e-07 (2^-21.35) | 21.35 |
| 29 | `iterative:data_width=28,n_iter=23,angle_guard=0,frac_guard=0,rounding=round` | 401 | 157 | 5.9 | 26 | 0.546 | 3.52e-07 (2^-21.44) | 21.44 |
| 30 | `iterative:data_width=28,n_iter=26,angle_guard=2,frac_guard=0,rounding=trunc` | 400 | 159 | 5.3 | 29 | 0.61 | 2.01e-07 (2^-22.24) | 22.24 |
| 31 | `iterative:data_width=28,n_iter=26,angle_guard=2,frac_guard=0,rounding=round` | 415 | 159 | 5.3 | 29 | 0.626 | 1.17e-07 (2^-23.03) | 23.03 |
| 32 | `iterative:data_width=28,n_iter=26,angle_guard=3,frac_guard=0,rounding=round` | 417 | 160 | 5.2 | 29 | 0.629 | 1.1e-07 (2^-23.12) | 23.12 |
| 33 | `iterative:data_width=28,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc` | 453 | 166 | 5.2 | 29 | 0.676 | 5.73e-08 (2^-24.06) | 24.06 |
| 34 | `iterative:data_width=28,n_iter=26,angle_guard=3,frac_guard=4,rounding=trunc` | 470 | 168 | 5.2 | 29 | 0.697 | 5.72e-08 (2^-24.06) | 24.06 |
| 35 | `iterative:data_width=28,n_iter=28,angle_guard=4,frac_guard=4,rounding=trunc` | 472 | 169 | 4.9 | 31 | 0.748 | 3e-08 (2^-24.99) | 24.99 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-dominated: minimise LUTs+FFs subject to a loose throughput floor (>=1 MSPS) and a hard accuracy floor (max_abs_err <= 2^-10, i.e. accuracy_bits >= 10). Throughput is not binding for any iterative/unrolled design with N<=20, so the Pareto front is essentially an area-vs-accuracy curve. Accuracy depends only on data_width, n_iter, angle_guard, frac_guard and rounding, so all families produce identical accuracy for the same parameters; the family choice only changes area. Therefore the first round should heavily sample the smallest-area family (iterative) over a range that brackets the accuracy threshold (W 11..18, N 8..20), and spend smaller shares on unrolled_k and pipelined_m to verify whether any pipelined structure can undercut iterative in area for small N. The ranges are deliberately wide enough to map the front from just-below-threshold to comfortably-above-threshold accuracy, which is what the hypervolume reference point (area 1500, accuracy_bits 10) rewards.*)
- `iterative` (60 evals): data_width=11..18, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Smallest-area family: one shared datapath, no per-stage registers. Throughput = Fmax/(N+3) is far above 1 MSPS for N<=20 at any plausible Fmax, so the throughput constraint is non-binding. Accuracy target 2^-10 needs W>=12 and N>=10; the ranges bracket that with margin. This family should own the low-area corner of the Pareto front.
- `unrolled_k` (25 evals): data_width=11..18, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..4. *Why:* Shares the iterative datapath but processes k micro-rotations per cycle. Area is expected to be slightly above iterative for the same accuracy, but it may offer a useful intermediate point if the shared barrel shifters dominate. k is kept small (2..4) because area is the objective and larger k multiplies the per-cycle hardware.
- `pipelined_m` (15 evals): data_width=11..18, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Pipelined variants use fixed shifts instead of barrel shifters, so for small N and large m (few pipeline registers) they can occasionally be area-competitive with iterative. Including m up to 8 lets the search test the low-register end. This family also probes whether a 1-result/cycle architecture can enter the low-area front; if not, the next round can drop it.

**Result (code):** 100 evaluations this round, 100 total; 45 feasible; hypervolume 5342 (n/a).

**LLM decision:** `map_front` — The feasible front is entirely the `iterative` family (10/10 designs), spanning only luts_plus_ffs 267..419 and accuracy_bits 10.8..14.6, while the HV reference point is (1500, 10). That leaves a large unexplored region: the registry allows data_width up to 28 and n_iter up to 30, so higher-accuracy (higher-area) iterative designs could extend the curve well to the right of 419, and lower-area designs near the 2^-10 constraint boundary (front's cheapest point is 267 @ 10.8 bits, constraint is 10 bits) could extend it leftward — both add hypervolume. The other families are not competitive for this low-area spec: unrolled_k's best feasible area is 354 and pipelined_m's is 1022 (vs 267), and the unexplored `pipelined` family registers every stage (1 result/cycle, N+2 latency) so it will only be larger still. Rather than spend budget on a family that cannot win on area, let code run NSGA-II over the full ranges of the family actually on the front (iterative), seeded with the current front, to map the whole trade-off curve before the reserved mapping budget is used up.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 5342 (gain this round: n/a (first round)).
Feasible designs: 45 of 100 evaluations (42 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 124
- max_abs_err <= 0.000976562: 55% violate; best seen 4.12e-05 (2^-14.57)

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=267, accuracy_bits=10.8, luts=172, ffs=95, throughput_msps=11, max_abs_err=0.000567 (2^-10.78), power_index=0.181
- iterative [data_width=16 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=280, accuracy_bits=11.6, luts=181, ffs=99, throughput_msps=10.4, max_abs_err=0.000333 (2^-11.55), power_index=0.2
- iterative [data_width=16 n_iter=19 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=295, accuracy_bits=11.8, luts=196, ffs=99, throughput_msps=7.36, max_abs_err=0.000285 (2^-11.78), power_index=0.244
- iterative [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=295, accuracy_bits=12.2, luts=193, ffs=102, throughput_msps=10.4, max_abs_err=0.000219 (2^-12.16), power_index=0.211
- iterative [data_width=16 n_iter=17 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=334, accuracy_bits=12.8, luts=228, ffs=106, throughput_msps=7.95, max_abs_err=0.000142 (2^-12.78), power_index=0.251
- iterative [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=336, accuracy_bits=12.9, luts=234, ffs=102, throughput_msps=10.4, max_abs_err=0.000134 (2^-12.86), power_index=0.24
- iterative [data_width=16 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=339, accuracy_bits=13.1, luts=236, ffs=103, throughput_msps=10.2, max_abs_err=0.000117 (2^-13.06), power_index=0.242
- iterative [data_width=16 n_iter=19 angle_guard=3 frac_guard=4 rounding=trunc] luts_plus_ffs=350, accuracy_bits=13.2, luts=242, ffs=108, throughput_msps=7.23, max_abs_err=0.000108 (2^-13.18), power_index=0.29
- iterative [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=355, accuracy_bits=13.5, luts=248, ffs=107, throughput_msps=10.2, max_abs_err=8.59e-05 (2^-13.51), power_index=0.253
- iterative [data_width=17 n_iter=18 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=419, accuracy_bits=14.6, luts=306, ffs=113, throughput_msps=7.57, max_abs_err=4.12e-05 (2^-14.57), power_index=0.331
Front coverage: luts_plus_ffs 267..419 (HV reference 1500); accuracy_bits 10.8..14.6 (HV reference 10); data_width on the front 15..17 (registry 8..28).

Per family:
- iterative: 60 evals, 29 feasible; max throughput seen 18 MSPS; best accuracy 14.57 bits; best feasible luts_plus_ffs=267; feasible ranges: data_width 14..17, n_iter 12..19, angle_guard -1..4, frac_guard 0..4
- unrolled_k: 25 evals, 13 feasible; max throughput seen 12.4 MSPS; best accuracy 13.11 bits; best feasible luts_plus_ffs=354; feasible ranges: data_width 14..16, n_iter 14..18, angle_guard -1..4, frac_guard 0..4, k 2..4
- pipelined_m: 15 evals, 3 feasible; max throughput seen 124 MSPS; best accuracy 10.52 bits; best feasible luts_plus_ffs=1022; feasible ranges: data_width 16..17, n_iter 16..17, angle_guard -2..-1, frac_guard 0..3, m 5..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=14..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (10 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 140 feasible; hypervolume 1.487e+04 (+178.3%).

**LLM decision:** `refine` — The feasible front is entirely iterative and the selection rule is min luts_plus_ffs, so the decisive region is the low-area corner: the current best is 267 (data_width=15, n_iter=15, accuracy 10.8 bits), only ~0.8 bits above the 2^-10 constraint. Yet the iterative feasible ranges show data_width 14 and n_iter 12 were reachable, so the true minimum-area feasible point is likely below 267 and the search has not yet pinned it down. unrolled_k (best feasible 354) and pipelined_m (best feasible 1022) are far worse on area, and pipelined (unexplored) is register-per-stage so cannot beat pipelined_m's 1022 — none of them can win the min-area selection or add non-dominated points, so budget should go to tightening the iterative low-area corner rather than adding a family.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.487e+04 (gain this round: +178.3%).
Feasible designs: 140 of 200 evaluations (119 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 124
- max_abs_err <= 0.000976562: 30% violate; best seen 5.73e-08 (2^-24.06)

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=267, accuracy_bits=10.8, luts=172, ffs=95, throughput_msps=11, max_abs_err=0.000567 (2^-10.78), power_index=0.181
- iterative [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=295, accuracy_bits=12.2, luts=193, ffs=102, throughput_msps=10.4, max_abs_err=0.000219 (2^-12.16), power_index=0.211
- iterative [data_width=16 n_iter=17 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=334, accuracy_bits=12.8, luts=228, ffs=106, throughput_msps=7.95, max_abs_err=0.000142 (2^-12.78), power_index=0.251
- iterative [data_width=18 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=339, accuracy_bits=13.5, luts=225, ffs=114, throughput_msps=10.8, max_abs_err=8.58e-05 (2^-13.51), power_index=0.23
- iterative [data_width=19 n_iter=20 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=381, accuracy_bits=15.2, luts=262, ffs=119, throughput_msps=6.91, max_abs_err=2.62e-05 (2^-15.22), power_index=0.33
- iterative [data_width=22 n_iter=20 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=406, accuracy_bits=16.3, luts=278, ffs=128, throughput_msps=6.78, max_abs_err=1.22e-05 (2^-16.32), power_index=0.351
- iterative [data_width=23 n_iter=20 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=430, accuracy_bits=17.3, luts=296, ffs=134, throughput_msps=6.78, max_abs_err=6.2e-06 (2^-17.30), power_index=0.372
- iterative [data_width=23 n_iter=25 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=454, accuracy_bits=18.4, luts=320, ffs=134, throughput_msps=5.57, max_abs_err=2.9e-06 (2^-18.39), power_index=0.478
- iterative [data_width=25 n_iter=29 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=503, accuracy_bits=20.2, luts=359, ffs=144, throughput_msps=4.79, max_abs_err=8.15e-07 (2^-20.23), power_index=0.606
- iterative [data_width=28 n_iter=26 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=619, accuracy_bits=24.1, luts=453, ffs=166, throughput_msps=5.19, max_abs_err=5.73e-08 (2^-24.06), power_index=0.676
Front coverage: luts_plus_ffs 267..619 (HV reference 1500); accuracy_bits 10.8..24.1 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 160 evals, 124 feasible; max throughput seen 18 MSPS; best accuracy 24.06 bits; best feasible luts_plus_ffs=267; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 25 evals, 13 feasible; max throughput seen 12.4 MSPS; best accuracy 13.11 bits; best feasible luts_plus_ffs=354; feasible ranges: data_width 14..16, n_iter 14..18, angle_guard -1..4, frac_guard 0..4, k 2..4
- pipelined_m: 15 evals, 3 feasible; max throughput seen 124 MSPS; best accuracy 10.52 bits; best feasible luts_plus_ffs=1022; feasible ranges: data_width 16..17, n_iter 16..17, angle_guard -2..-1, frac_guard 0..3, m 5..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Focus the round on the min-area corner of the iterative front (the region the selection rule cares about) while cheaply checking unrolled_k; skip pipelined/pipelined_m since their register-heavy structure cannot compete on luts_plus_ffs.*)
- `iterative` (80 evals): data_width=14..18, n_iter=12..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Front is entirely iterative; lowest area 267 sits at 10.8 bits, just above the 10-bit constraint, and data_width 14 / n_iter 12 were feasible, so a smaller design likely exists in this box.
- `unrolled_k` (20 evals): data_width=14..17, n_iter=14..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..4. *Why:* Best feasible area 354 is well above iterative's 267, but a small budget confirms whether any low-area unrolled_k point can enter the front.

**Result (code):** 100 evaluations this round, 300 total; 229 feasible; hypervolume 1.492e+04 (+0.3%).

**LLM decision:** `map_front` — The feasible front is entirely `iterative` and already satisfies both constraints with margin: the min-area corner is iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=1 trunc] at luts_plus_ffs=264, accuracy 10.7 bits, throughput 10.4 MSPS (constraints: >=1 MSPS, err <=2^-10), so the selection rule (min luts_plus_ffs) is already served. The other explored families are dominated: unrolled_k best feasible area 354 and pipelined_m best 1022, both worse than 264, and pipelined_m's best accuracy (10.52) is below the iterative corner's 10.7 — so adding `pipelined` (registered stages, strictly more area) is unlikely to help the min-area objective. The front's accuracy span (10.7..24.1 bits) already clears the HV ref of 10, but its area span only reaches 619 against the HV ref of 1500, so the largest hypervolume gains lie in extending the high-accuracy end of the iterative curve (data_width up to 28, n_iter up to 30). With 100 evals and one round left, the reserved budget is best spent letting code map the full iterative front (seeded with the current front) rather than narrowing around a corner that is already found.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.492e+04 (gain this round: +0.3%).
Feasible designs: 229 of 300 evaluations (193 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 124
- max_abs_err <= 0.000976562: 24% violate; best seen 5.73e-08 (2^-24.06)

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=264, accuracy_bits=10.7, luts=170, ffs=94, throughput_msps=10.4, max_abs_err=0.000594 (2^-10.72), power_index=0.189
- iterative [data_width=16 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=280, accuracy_bits=11.6, luts=181, ffs=99, throughput_msps=10.4, max_abs_err=0.000333 (2^-11.55), power_index=0.2
- iterative [data_width=17 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=296, accuracy_bits=12.8, luts=193, ffs=103, throughput_msps=10.2, max_abs_err=0.000139 (2^-12.81), power_index=0.211
- iterative [data_width=18 n_iter=16 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=339, accuracy_bits=14, luts=225, ffs=114, throughput_msps=10.2, max_abs_err=5.94e-05 (2^-14.04), power_index=0.243
- iterative [data_width=19 n_iter=20 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=381, accuracy_bits=15.2, luts=262, ffs=119, throughput_msps=6.91, max_abs_err=2.62e-05 (2^-15.22), power_index=0.33
- iterative [data_width=22 n_iter=20 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=406, accuracy_bits=16.3, luts=278, ffs=128, throughput_msps=6.78, max_abs_err=1.22e-05 (2^-16.32), power_index=0.351
- iterative [data_width=23 n_iter=20 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=430, accuracy_bits=17.3, luts=296, ffs=134, throughput_msps=6.78, max_abs_err=6.2e-06 (2^-17.30), power_index=0.372
- iterative [data_width=23 n_iter=25 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=454, accuracy_bits=18.4, luts=320, ffs=134, throughput_msps=5.57, max_abs_err=2.9e-06 (2^-18.39), power_index=0.478
- iterative [data_width=25 n_iter=29 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=503, accuracy_bits=20.2, luts=359, ffs=144, throughput_msps=4.79, max_abs_err=8.15e-07 (2^-20.23), power_index=0.606
- iterative [data_width=28 n_iter=26 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=619, accuracy_bits=24.1, luts=453, ffs=166, throughput_msps=5.19, max_abs_err=5.73e-08 (2^-24.06), power_index=0.676
Front coverage: luts_plus_ffs 264..619 (HV reference 1500); accuracy_bits 10.7..24.1 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 240 evals, 197 feasible; max throughput seen 18 MSPS; best accuracy 24.06 bits; best feasible luts_plus_ffs=264; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 45 evals, 29 feasible; max throughput seen 12.4 MSPS; best accuracy 13.81 bits; best feasible luts_plus_ffs=354; feasible ranges: data_width 14..17, n_iter 14..20, angle_guard -1..4, frac_guard 0..4, k 2..4
- pipelined_m: 15 evals, 3 feasible; max throughput seen 124 MSPS; best accuracy 10.52 bits; best feasible luts_plus_ffs=1022; feasible ranges: data_width 16..17, n_iter 16..17, angle_guard -2..-1, frac_guard 0..3, m 5..8
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `iterative` (100 evals): data_width=13..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (25 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 323 feasible; hypervolume 1.584e+04 (+6.2%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), and the front is feasible and well covered: 323/400 evaluations feasible, 36 Pareto designs spanning luts_plus_ffs 264..642 against the HV reference 1500 and accuracy_bits 10.7..25 against the reference 10, with hypervolume 1.584e+04 still gaining (+6.2%). Both constraints are comfortably met by many designs (0% throughput violations, best 124 MSPS vs the 1 MSPS floor; only 19% error violations, best 2^-24.99 vs the 2^-10 limit), so `infeasible` is not warranted. The selection rule (min luts_plus_ffs) is already served by iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc] at luts_plus_ffs=264, accuracy_bits=10.7, throughput 10.4 MSPS — the cheapest design on the front and still 0.7 bits above the error constraint. The only unexplored family, pipelined, is a throughput-oriented family whose sibling pipelined_m already showed a much worse area floor (best feasible luts_plus_ffs=1022) at 124 MSPS, which this >=1 MSPS spec does not need; with no budget left there is no evidence it would improve the min-area corner. Stopping here preserves the mapped front.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.584e+04 (gain this round: +6.2%).
Feasible designs: 323 of 400 evaluations (276 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 124
- max_abs_err <= 0.000976562: 19% violate; best seen 3e-08 (2^-24.99)

Pareto front (feasible, 36 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=264, accuracy_bits=10.7, luts=170, ffs=94, throughput_msps=10.4, max_abs_err=0.000594 (2^-10.72), power_index=0.189
- iterative [data_width=17 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=293, accuracy_bits=12.7, luts=191, ffs=102, throughput_msps=10.4, max_abs_err=0.000149 (2^-12.71), power_index=0.209
- iterative [data_width=18 n_iter=16 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=339, accuracy_bits=14, luts=225, ffs=114, throughput_msps=10.2, max_abs_err=5.94e-05 (2^-14.04), power_index=0.243
- iterative [data_width=19 n_iter=20 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=381, accuracy_bits=15.2, luts=262, ffs=119, throughput_msps=6.91, max_abs_err=2.62e-05 (2^-15.22), power_index=0.33
- iterative [data_width=21 n_iter=20 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=423, accuracy_bits=17, luts=294, ffs=129, throughput_msps=6.78, max_abs_err=7.58e-06 (2^-17.01), power_index=0.366
- iterative [data_width=21 n_iter=20 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=439, accuracy_bits=17.5, luts=308, ffs=131, throughput_msps=6.78, max_abs_err=5.52e-06 (2^-17.47), power_index=0.38
- iterative [data_width=25 n_iter=23 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=496, accuracy_bits=20.1, luts=352, ffs=144, throughput_msps=5.89, max_abs_err=8.71e-07 (2^-20.13), power_index=0.485
- iterative [data_width=25 n_iter=28 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=525, accuracy_bits=20.9, luts=377, ffs=148, throughput_msps=4.94, max_abs_err=5.15e-07 (2^-20.89), power_index=0.613
- iterative [data_width=28 n_iter=26 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=574, accuracy_bits=23, luts=415, ffs=159, throughput_msps=5.28, max_abs_err=1.17e-07 (2^-23.03), power_index=0.626
- iterative [data_width=28 n_iter=28 angle_guard=4 frac_guard=4 rounding=trunc] luts_plus_ffs=642, accuracy_bits=25, luts=472, ffs=169, throughput_msps=4.86, max_abs_err=3e-08 (2^-24.99), power_index=0.748
Front coverage: luts_plus_ffs 264..642 (HV reference 1500); accuracy_bits 10.7..25 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 340 evals, 291 feasible; max throughput seen 18 MSPS; best accuracy 24.99 bits; best feasible luts_plus_ffs=264; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 45 evals, 29 feasible; max throughput seen 12.4 MSPS; best accuracy 13.81 bits; best feasible luts_plus_ffs=354; feasible ranges: data_width 14..17, n_iter 14..20, angle_guard -1..4, frac_guard 0..4, k 2..4
- pipelined_m: 15 evals, 3 feasible; max throughput seen 124 MSPS; best accuracy 10.52 bits; best feasible luts_plus_ffs=1022; feasible ranges: data_width 16..17, n_iter 16..17, angle_guard -2..-1, frac_guard 0..3, m 5..8
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 29411 in, 12279 out
- provider-reported cost: $0.0153
- full prompts and replies: `llm_trace.jsonl`

