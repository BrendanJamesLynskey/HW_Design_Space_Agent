# DSE run: dds_250msps

**Verdict:** converged: hypervolume gain fell below epsilon.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 3 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec dds_250msps: NCO / DDS sin-cos generator for a digital up-converter. One sample per clock at >= 250 MSPS, max error <= 2^-13. Minimise LUTs.
  constraint: throughput_msps >= 250
  constraint: max_abs_err <= 0.00012207
  objective: min luts (HV ref 4000)
  objective: max accuracy_bits (HV ref 13)
  select: min luts
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined:data_width=18,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts)

| metric | value | provenance |
|---|---|---|
| luts | 954 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 985 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 273 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 273 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 66 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 18.2 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000121 (2^-13.02) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 7.9 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.65e-05 (2^-15.20) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.74 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 18 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 102.0 dBc, SNR 88.9 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (30 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 954 | 985 | 272.9 | 18 | 18.2 | 0.000121 (2^-13.02) | 13.02 |
| 1 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc` | 964 | 991 | 264.5 | 17 | 18.4 | 0.000102 (2^-13.26) | 13.26 |
| 2 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc` | 979 | 1006 | 264.5 | 17 | 18.7 | 9.49e-05 (2^-13.36) | 13.36 |
| 3 | `pipelined:data_width=19,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc` | 1008 | 1036 | 264.5 | 17 | 19.2 | 8.04e-05 (2^-13.60) | 13.60 |
| 4 | `pipelined:data_width=19,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc` | 1023 | 1051 | 264.5 | 17 | 19.5 | 7.77e-05 (2^-13.65) | 13.65 |
| 5 | `pipelined:data_width=20,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 1048 | 1082 | 264.5 | 18 | 20 | 5.27e-05 (2^-14.21) | 14.21 |
| 6 | `pipelined:data_width=19,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 1104 | 1096 | 264.5 | 18 | 20.7 | 4.95e-05 (2^-14.30) | 14.30 |
| 7 | `pipelined:data_width=20,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc` | 1112 | 1142 | 264.5 | 18 | 21.2 | 4.27e-05 (2^-14.51) | 14.51 |
| 8 | `pipelined:data_width=20,n_iter=16,angle_guard=1,frac_guard=1,rounding=round` | 1138 | 1128 | 264.5 | 18 | 21.3 | 4.05e-05 (2^-14.59) | 14.59 |
| 9 | `pipelined:data_width=17,n_iter=17,angle_guard=4,frac_guard=4,rounding=round` | 1204 | 1186 | 264.5 | 19 | 22.5 | 3.68e-05 (2^-14.73) | 14.73 |
| 10 | `pipelined:data_width=19,n_iter=18,angle_guard=2,frac_guard=2,rounding=trunc` | 1241 | 1263 | 264.5 | 20 | 23.6 | 3.04e-05 (2^-15.00) | 15.00 |
| 11 | `pipelined:data_width=22,n_iter=17,angle_guard=3,frac_guard=0,rounding=trunc` | 1270 | 1304 | 256.5 | 19 | 24.2 | 2.27e-05 (2^-15.43) | 15.43 |
| 12 | `pipelined:data_width=22,n_iter=17,angle_guard=1,frac_guard=2,rounding=trunc` | 1303 | 1330 | 256.5 | 19 | 24.8 | 1.82e-05 (2^-15.75) | 15.75 |
| 13 | `pipelined:data_width=22,n_iter=17,angle_guard=2,frac_guard=2,rounding=trunc` | 1320 | 1347 | 256.5 | 19 | 25.1 | 1.71e-05 (2^-15.84) | 15.84 |
| 14 | `pipelined:data_width=22,n_iter=18,angle_guard=0,frac_guard=1,rounding=trunc` | 1331 | 1358 | 256.5 | 20 | 25.3 | 1.39e-05 (2^-16.14) | 16.14 |
| 15 | `pipelined:data_width=21,n_iter=18,angle_guard=4,frac_guard=2,rounding=trunc` | 1385 | 1408 | 256.5 | 20 | 26.3 | 1.19e-05 (2^-16.36) | 16.36 |
| 16 | `pipelined:data_width=21,n_iter=18,angle_guard=3,frac_guard=3,rounding=trunc` | 1403 | 1423 | 256.5 | 20 | 26.6 | 1.08e-05 (2^-16.50) | 16.50 |
| 17 | `pipelined:data_width=20,n_iter=19,angle_guard=4,frac_guard=2,rounding=round` | 1451 | 1432 | 256.5 | 21 | 27.1 | 1.04e-05 (2^-16.56) | 16.56 |
| 18 | `pipelined:data_width=23,n_iter=18,angle_guard=2,frac_guard=2,rounding=trunc` | 1456 | 1481 | 256.5 | 20 | 27.6 | 8.56e-06 (2^-16.83) | 16.83 |
| 19 | `pipelined:data_width=26,n_iter=18,angle_guard=0,frac_guard=0,rounding=trunc` | 1510 | 1544 | 256.5 | 20 | 28.7 | 8.07e-06 (2^-16.92) | 16.92 |
| 20 | `pipelined:data_width=20,n_iter=20,angle_guard=4,frac_guard=4,rounding=round` | 1609 | 1580 | 256.5 | 22 | 30 | 5.46e-06 (2^-17.48) | 17.48 |
| 21 | `pipelined:data_width=22,n_iter=21,angle_guard=2,frac_guard=2,rounding=trunc` | 1649 | 1666 | 256.5 | 23 | 31.2 | 3.8e-06 (2^-18.01) | 18.01 |
| 22 | `pipelined:data_width=23,n_iter=21,angle_guard=2,frac_guard=1,rounding=trunc` | 1670 | 1691 | 256.5 | 23 | 31.6 | 3.24e-06 (2^-18.24) | 18.24 |
| 23 | `pipelined:data_width=25,n_iter=21,angle_guard=-1,frac_guard=0,rounding=round` | 1691 | 1716 | 256.5 | 23 | 32 | 2.56e-06 (2^-18.58) | 18.58 |
| 24 | `pipelined:data_width=22,n_iter=21,angle_guard=3,frac_guard=2,rounding=round` | 1717 | 1689 | 256.5 | 23 | 32 | 2.52e-06 (2^-18.60) | 18.60 |
| 25 | `pipelined:data_width=22,n_iter=21,angle_guard=4,frac_guard=2,rounding=round` | 1738 | 1710 | 256.5 | 23 | 32.4 | 2.45e-06 (2^-18.64) | 18.64 |
| 26 | `pipelined:data_width=24,n_iter=21,angle_guard=1,frac_guard=1,rounding=round` | 1763 | 1735 | 256.5 | 23 | 32.9 | 2.11e-06 (2^-18.86) | 18.86 |
| 27 | `pipelined:data_width=23,n_iter=21,angle_guard=2,frac_guard=3,rounding=round` | 1803 | 1770 | 256.5 | 23 | 33.6 | 1.92e-06 (2^-18.99) | 18.99 |
| 28 | `pipelined:data_width=22,n_iter=24,angle_guard=4,frac_guard=4,rounding=trunc` | 2041 | 2042 | 256.5 | 26 | 38.4 | 1.68e-06 (2^-19.18) | 19.18 |
| 29 | `pipelined:data_width=23,n_iter=25,angle_guard=2,frac_guard=3,rounding=round` | 2153 | 2109 | 256.5 | 27 | 40.1 | 1.1e-06 (2^-19.79) | 19.79 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=250 MSPS throughput (1 sample/clock) and max_abs_err <= 2^-13. Only pipelined and pipelined_m families guarantee 1 result/cycle, so iterative and unrolled_k are excluded as they produce one result every several cycles and would likely fail the throughput constraint unless Fmax is extremely high. We focus on these two families with 60/40 budget split. Pipelined gets more budget as it's the baseline for 1/cycle throughput. Data width is kept modest (14-22) to control LUTs while meeting accuracy. n_iter (10-16) is chosen because CORDIC error decreases exponentially with iterations, and 10-12 iterations are typically sufficient for 13-bit accuracy. Guard bits are kept small (0-2) to minimize area. The accuracy constraint is tight, so we need to ensure enough precision in the angle and fractional paths. The selection rule is min LUTs, so we're optimizing for area while meeting the hard constraints on throughput and accuracy.*)
- `pipelined` (60 evals): data_width=14..22, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Pipelined is the only family that guarantees 1 result/cycle, which is required to meet the >=250 MSPS throughput constraint at a plausible Fmax. The accuracy constraint (max_abs_err <= 2^-13) is tight, so we need enough iterations (n_iter) and guard bits. Data width 14-22 balances LUT cost against the need for fractional precision. We focus on moderate n_iter (10-16) because CORDIC error drops exponentially with N, and 10-12 iterations are typically sufficient for 13-bit accuracy with proper guards. angle_guard and frac_guard are kept small (0-2) to minimize area while still providing enough precision to meet the error bound. Rounding is included as a binary choice since it can affect final error.
- `pipelined_m` (40 evals): data_width=14..22, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Pipelined_m also provides 1 result/cycle throughput, satisfying the >=250 MSPS constraint. By registering every m stages instead of every stage, it can reduce FF count and potentially improve Fmax or reduce area compared to fully pipelined. The m parameter (2-4) allows exploring the trade-off between pipeline depth and resource usage. Same data_width, n_iter, and guard ranges as pipelined since accuracy requirements are identical. This family may find designs with fewer LUTs or FFs than fully pipelined while maintaining the same throughput.
- clamped by code: pipelined.rounding: dropped invalid choices ['data_width', 'n_iter', 'angle_guard', 'frac_guard', 'rounding']
- clamped by code: pipelined_m.rounding: dropped invalid choices ['data_width', 'n_iter', 'angle_guard', 'frac_guard', 'rounding', 'm']

**Result (code):** 100 evaluations this round, 100 total; 19 feasible; hypervolume 4712 (n/a).

**LLM decision:** `add_family` — The current front is dominated by the `pipelined` family, which is constrained by a maximum throughput of ~273 MSPS. The `pipelined_m` family failed to meet the throughput constraint (max 171 MSPS), likely due to the reduced clock frequency from fewer registers. The `unrolled_k` family is a promising candidate for the low-LUT end of the front because it allows for higher clock frequencies (fewer registers than `pipelined`) and can potentially meet the 250 MSPS throughput constraint while using fewer LUTs than the current best (954). The `iterative` family is also worth exploring as it has the lowest resource usage (shared datapath) and might meet the throughput constraint if the clock frequency is high enough, though it will likely have lower throughput than `unrolled_k`.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 4712 (gain this round: n/a (first round)).
Feasible designs: 19 of 100 evaluations (13 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 40% violate; best seen 273
- max_abs_err <= 0.00012207: 57% violate; best seen 3.39e-05 (2^-14.85)

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts=954, accuracy_bits=13, ffs=985, throughput_msps=273, max_abs_err=0.000121 (2^-13.02), power_index=18.2
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts=964, accuracy_bits=13.3, ffs=991, throughput_msps=264, max_abs_err=0.000102 (2^-13.26), power_index=18.4
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] luts=979, accuracy_bits=13.4, ffs=1006, throughput_msps=264, max_abs_err=9.49e-05 (2^-13.36), power_index=18.7
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts=1008, accuracy_bits=13.6, ffs=1036, throughput_msps=264, max_abs_err=8.04e-05 (2^-13.60), power_index=19.2
- pipelined [data_width=19 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] luts=1023, accuracy_bits=13.7, ffs=1051, throughput_msps=264, max_abs_err=7.77e-05 (2^-13.65), power_index=19.5
- pipelined [data_width=20 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts=1048, accuracy_bits=14.2, ffs=1082, throughput_msps=264, max_abs_err=5.27e-05 (2^-14.21), power_index=20
- pipelined [data_width=20 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] luts=1112, accuracy_bits=14.5, ffs=1142, throughput_msps=264, max_abs_err=4.27e-05 (2^-14.51), power_index=21.2
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts=1138, accuracy_bits=14.6, ffs=1128, throughput_msps=264, max_abs_err=4.05e-05 (2^-14.59), power_index=21.3
Front coverage: luts 954..1138 (HV reference 4000); accuracy_bits 13..14.6 (HV reference 13); data_width on the front 18..20 (registry 8..28).

Per family:
- pipelined: 60 evals, 19 feasible; max throughput seen 273 MSPS; best accuracy 14.59 bits; best feasible luts=954; feasible ranges: data_width 17..22, n_iter 15..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 40 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 14.85 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Exploring unrolled_k and iterative to find designs with lower LUT counts that still meet the throughput constraint, expanding the Pareto front to the left.*)
- `unrolled_k` (60 evals): data_width=18..22, n_iter=15..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k can achieve higher Fmax than pipelined_m and potentially higher throughput than pipelined, allowing for lower LUT counts while meeting the 250 MSPS constraint.
- `iterative` (40 evals): data_width=18..22, n_iter=15..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative has the lowest resource usage and might meet the throughput constraint if the clock frequency is high enough, potentially providing a lower LUT count than the current front.

**Result (code):** 100 evaluations this round, 200 total; 19 feasible; hypervolume 4712 (+0.0%).

**LLM decision:** `refine` — The throughput constraint (>= 250 MSPS) is the hard bottleneck, eliminating iterative, unrolled_k, and pipelined_m (max 171 MSPS). Only the 'pipelined' family is feasible, with a best throughput of 273 MSPS. The current Pareto front is dominated by pipelined designs with data_width 18-20 and n_iter 15-16. To maximize hypervolume, we need to explore the trade-off between LUTs and accuracy more densely within this narrow feasible window. Specifically, we should narrow the search space to focus on the pipelined family with data_width 17-21, n_iter 14-18, and guard bits 0-3 to find lower LUT counts for the same accuracy or higher accuracy for the same LUTs, while ensuring throughput remains above 250 MSPS.
- **rule applied by code:** 'refine' overridden to stop: HV gain 0.00% < epsilon 1.00%
- **rule applied by code:** code: before stopping (converged), one front-mapping round with the remaining 200 evaluations
- effective decision: `stop`

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 4712 (gain this round: +0.0%).
Feasible designs: 19 of 200 evaluations (13 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 70% violate; best seen 273
- max_abs_err <= 0.00012207: 32% violate; best seen 9.56e-06 (2^-16.67)

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts=954, accuracy_bits=13, ffs=985, throughput_msps=273, max_abs_err=0.000121 (2^-13.02), power_index=18.2
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts=964, accuracy_bits=13.3, ffs=991, throughput_msps=264, max_abs_err=0.000102 (2^-13.26), power_index=18.4
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] luts=979, accuracy_bits=13.4, ffs=1006, throughput_msps=264, max_abs_err=9.49e-05 (2^-13.36), power_index=18.7
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts=1008, accuracy_bits=13.6, ffs=1036, throughput_msps=264, max_abs_err=8.04e-05 (2^-13.60), power_index=19.2
- pipelined [data_width=19 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] luts=1023, accuracy_bits=13.7, ffs=1051, throughput_msps=264, max_abs_err=7.77e-05 (2^-13.65), power_index=19.5
- pipelined [data_width=20 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts=1048, accuracy_bits=14.2, ffs=1082, throughput_msps=264, max_abs_err=5.27e-05 (2^-14.21), power_index=20
- pipelined [data_width=20 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] luts=1112, accuracy_bits=14.5, ffs=1142, throughput_msps=264, max_abs_err=4.27e-05 (2^-14.51), power_index=21.2
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts=1138, accuracy_bits=14.6, ffs=1128, throughput_msps=264, max_abs_err=4.05e-05 (2^-14.59), power_index=21.3
Front coverage: luts 954..1138 (HV reference 4000); accuracy_bits 13..14.6 (HV reference 13); data_width on the front 18..20 (registry 8..28).

Per family:
- iterative: 40 evals, 0 feasible; max throughput seen 11 MSPS; best accuracy 15.56 bits
- unrolled_k: 60 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 16.67 bits
- pipelined: 60 evals, 19 feasible; max throughput seen 273 MSPS; best accuracy 14.59 bits; best feasible luts=954; feasible ranges: data_width 17..22, n_iter 15..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 40 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 14.85 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 200 evaluations*)
- `pipelined` (200 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (8 front designs; box front_anchored)

**Result (code):** 200 evaluations this round, 400 total; 154 feasible; hypervolume 1.724e+04 (+266.0%).

**No LLM call** (code's front-mapping round): The throughput constraint (>= 250 MSPS) is the hard bottleneck, eliminating iterative, unrolled_k, and pipelined_m (max 171 MSPS). Only the 'pipelined' family is feasible, with a best throughput of 273 MSPS. The current Pareto front is dominated by pipelined designs with data_width 18-20 and n_iter 15-16. To maximize hypervolume, we need to explore the trade-off between LUTs and accuracy more densely within this narrow feasible window. Specifically, we should narrow the search space to focus on the pipelined family with data_width 17-21, n_iter 14-18, and guard bits 0-3 to find lower LUT counts for the same accuracy or higher accuracy for the same LUTs, while ensuring throughput remains above 250 MSPS.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.724e+04 (gain this round: +266.0%).
Feasible designs: 154 of 400 evaluations (131 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 47% violate; best seen 273
- max_abs_err <= 0.00012207: 21% violate; best seen 8.86e-08 (2^-23.43)

Pareto front (feasible, 30 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts=954, accuracy_bits=13, ffs=985, throughput_msps=273, max_abs_err=0.000121 (2^-13.02), power_index=18.2
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts=1008, accuracy_bits=13.6, ffs=1036, throughput_msps=264, max_abs_err=8.04e-05 (2^-13.60), power_index=19.2
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] luts=1104, accuracy_bits=14.3, ffs=1096, throughput_msps=264, max_abs_err=4.95e-05 (2^-14.30), power_index=20.7
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc] luts=1241, accuracy_bits=15, ffs=1263, throughput_msps=264, max_abs_err=3.04e-05 (2^-15.00), power_index=23.6
- pipelined [data_width=22 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc] luts=1320, accuracy_bits=15.8, ffs=1347, throughput_msps=257, max_abs_err=1.71e-05 (2^-15.84), power_index=25.1
- pipelined [data_width=21 n_iter=18 angle_guard=3 frac_guard=3 rounding=trunc] luts=1403, accuracy_bits=16.5, ffs=1423, throughput_msps=257, max_abs_err=1.08e-05 (2^-16.50), power_index=26.6
- pipelined [data_width=26 n_iter=18 angle_guard=0 frac_guard=0 rounding=trunc] luts=1510, accuracy_bits=16.9, ffs=1544, throughput_msps=257, max_abs_err=8.07e-06 (2^-16.92), power_index=28.7
- pipelined [data_width=25 n_iter=21 angle_guard=-1 frac_guard=0 rounding=round] luts=1691, accuracy_bits=18.6, ffs=1716, throughput_msps=257, max_abs_err=2.56e-06 (2^-18.58), power_index=32
- pipelined [data_width=24 n_iter=21 angle_guard=1 frac_guard=1 rounding=round] luts=1763, accuracy_bits=18.9, ffs=1735, throughput_msps=257, max_abs_err=2.11e-06 (2^-18.86), power_index=32.9
- pipelined [data_width=23 n_iter=25 angle_guard=2 frac_guard=3 rounding=round] luts=2153, accuracy_bits=19.8, ffs=2109, throughput_msps=257, max_abs_err=1.1e-06 (2^-19.79), power_index=40.1
Front coverage: luts 954..2153 (HV reference 4000); accuracy_bits 13..19.8 (HV reference 13); data_width on the front 17..26 (registry 8..28).

Per family:
- iterative: 40 evals, 0 feasible; max throughput seen 11 MSPS; best accuracy 15.56 bits
- unrolled_k: 60 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 16.67 bits
- pipelined: 260 evals, 154 feasible; max throughput seen 273 MSPS; best accuracy 23.43 bits; best feasible luts=954; feasible ranges: data_width 17..26, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 40 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 14.85 bits
```
</details>

## LLM usage
- calls: 6 (failed/unparsed attempts: 0)
- tokens: 21367 in, 3071 out
- provider-reported cost: $0.0065
- full prompts and replies: `llm_trace.jsonl`

