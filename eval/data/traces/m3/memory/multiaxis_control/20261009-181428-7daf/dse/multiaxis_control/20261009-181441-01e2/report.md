# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 4 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec multiaxis_control: Shared sin/cos unit for a 16-axis motor-control loop: a 1 MHz control tick issues 32 requests at once (Park + inverse Park per axis); all 32 results must be back within 0.44 us of the tick (p99 over ticks). Max error <= 2^-12. Minimise LUTs + FFs.
  constraint: throughput_msps >= 32
  constraint: max_abs_err <= 0.000244141
  constraint: sys_p99_batch_us <= 0.44
  objective: min luts_plus_ffs (HV ref 4000)
  objective: max accuracy_bits (HV ref 12)
  select: min luts_plus_ffs
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average)
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=19,n_iter=14,angle_guard=-1,frac_guard=2,rounding=trunc,m=2` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 909 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 507 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 164 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 164 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 9 | exact: schedule |
| latency_ns | 54.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.71 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00018 (2^-12.44) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 23.6 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.18e-05 (2^-14.24) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 6.79 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.4 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 9 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 94.9 dBc, SNR 82.8 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=19,n_iter=14,angle_guard=-1,frac_guard=2,rounding=trunc,m=2` | 0.2373 → 0.2433 | yes |
| `pipelined_m:data_width=19,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=2` | 0.2373 → 0.2433 | yes |
| `pipelined_m:data_width=19,n_iter=16,angle_guard=-1,frac_guard=1,rounding=trunc,m=2` | 0.2433 → 0.2494 | yes |
| `pipelined_m:data_width=19,n_iter=16,angle_guard=-1,frac_guard=1,rounding=round,m=2` | 0.2433 → 0.2494 | yes |
| `pipelined_m:data_width=20,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc,m=2` | 0.2433 → 0.2494 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (30 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=14,angle_guard=-1,frac_guard=2,rounding=trunc,m=2` | 909 | 507 | 164.4 | 9 | 1.71 | 0.00018 (2^-12.44) | 12.44 |
| 1 | `pipelined_m:data_width=19,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=2` | 991 | 531 | 164.4 | 9 | 1.83 | 0.000133 (2^-12.88) | 12.88 |
| 2 | `pipelined_m:data_width=19,n_iter=16,angle_guard=-1,frac_guard=1,rounding=trunc,m=2` | 1017 | 561 | 164.4 | 10 | 1.9 | 0.000105 (2^-13.21) | 13.21 |
| 3 | `pipelined_m:data_width=19,n_iter=16,angle_guard=-1,frac_guard=1,rounding=round,m=2` | 1057 | 563 | 164.4 | 10 | 1.95 | 0.000101 (2^-13.28) | 13.28 |
| 4 | `pipelined_m:data_width=20,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc,m=2` | 1023 | 603 | 164.4 | 10 | 1.96 | 7.76e-05 (2^-13.65) | 13.65 |
| 5 | `pipelined_m:data_width=18,n_iter=20,angle_guard=4,frac_guard=0,rounding=round,m=4` | 1287 | 364 | 93.6 | 7 | 1.99 | 7.75e-05 (2^-13.65) | 13.65 |
| 6 | `pipelined_m:data_width=20,n_iter=16,angle_guard=-1,frac_guard=1,rounding=trunc,m=2` | 1064 | 587 | 164.4 | 10 | 1.99 | 6.62e-05 (2^-13.88) | 13.88 |
| 7 | `pipelined_m:data_width=20,n_iter=16,angle_guard=-1,frac_guard=1,rounding=round,m=2` | 1106 | 589 | 164.4 | 10 | 2.04 | 6.6e-05 (2^-13.89) | 13.89 |
| 8 | `pipelined_m:data_width=20,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc,m=2` | 1112 | 611 | 164.4 | 10 | 2.07 | 4.27e-05 (2^-14.51) | 14.51 |
| 9 | `pipelined_m:data_width=20,n_iter=16,angle_guard=2,frac_guard=1,rounding=round,m=2` | 1154 | 613 | 164.4 | 10 | 2.13 | 3.91e-05 (2^-14.64) | 14.64 |
| 10 | `pipelined_m:data_width=24,n_iter=20,angle_guard=4,frac_guard=0,rounding=round,m=4` | 1647 | 467 | 86.0 | 7 | 2.54 | 2.71e-06 (2^-18.49) | 18.49 |
| 11 | `pipelined_m:data_width=26,n_iter=20,angle_guard=1,frac_guard=4,rounding=round,m=4` | 1922 | 521 | 86.0 | 7 | 2.94 | 2.05e-06 (2^-18.89) | 18.89 |
| 12 | `pipelined_m:data_width=28,n_iter=20,angle_guard=-1,frac_guard=2,rounding=round,m=4` | 1926 | 529 | 86.0 | 7 | 2.95 | 2.04e-06 (2^-18.91) | 18.91 |
| 13 | `pipelined_m:data_width=26,n_iter=20,angle_guard=4,frac_guard=1,rounding=round,m=3` | 1862 | 695 | 110.0 | 9 | 3.08 | 2.01e-06 (2^-18.92) | 18.92 |
| 14 | `pipelined_m:data_width=26,n_iter=22,angle_guard=0,frac_guard=1,rounding=round,m=3` | 1963 | 755 | 110.0 | 10 | 3.27 | 9.82e-07 (2^-19.96) | 19.96 |
| 15 | `pipelined_m:data_width=26,n_iter=22,angle_guard=4,frac_guard=1,rounding=round,m=3` | 2052 | 787 | 110.0 | 10 | 3.42 | 6.36e-07 (2^-20.58) | 20.58 |
| 16 | `pipelined_m:data_width=28,n_iter=22,angle_guard=-1,frac_guard=3,rounding=round,m=3` | 2167 | 827 | 105.9 | 10 | 3.6 | 6.24e-07 (2^-20.61) | 20.61 |
| 17 | `pipelined_m:data_width=26,n_iter=26,angle_guard=0,frac_guard=1,rounding=round,m=3` | 2326 | 842 | 110.0 | 11 | 3.81 | 6.05e-07 (2^-20.66) | 20.66 |
| 18 | `pipelined:data_width=26,n_iter=22,angle_guard=2,frac_guard=2,rounding=round` | 2052 | 2014 | 249.0 | 24 | 4.89 | 5.86e-07 (2^-20.70) | 20.70 |
| 19 | `pipelined:data_width=28,n_iter=22,angle_guard=2,frac_guard=0,rounding=round` | 2041 | 2064 | 249.0 | 24 | 4.94 | 5.32e-07 (2^-20.84) | 20.84 |
| 20 | `pipelined:data_width=28,n_iter=22,angle_guard=1,frac_guard=2,rounding=round` | 2167 | 2125 | 249.0 | 24 | 5.17 | 5.2e-07 (2^-20.87) | 20.87 |
| 21 | `pipelined:data_width=25,n_iter=24,angle_guard=2,frac_guard=4,rounding=round` | 2263 | 2214 | 249.0 | 26 | 5.39 | 3.58e-07 (2^-21.41) | 21.41 |
| 22 | `pipelined:data_width=25,n_iter=24,angle_guard=3,frac_guard=4,rounding=round` | 2288 | 2238 | 249.0 | 26 | 5.45 | 2.44e-07 (2^-21.97) | 21.97 |
| 23 | `pipelined:data_width=28,n_iter=24,angle_guard=4,frac_guard=1,rounding=trunc` | 2332 | 2345 | 242.0 | 26 | 5.63 | 1.85e-07 (2^-22.37) | 22.37 |
| 24 | `pipelined:data_width=25,n_iter=25,angle_guard=4,frac_guard=4,rounding=round` | 2410 | 2357 | 249.0 | 27 | 5.74 | 1.68e-07 (2^-22.51) | 22.51 |
| 25 | `pipelined:data_width=28,n_iter=24,angle_guard=3,frac_guard=2,rounding=round` | 2415 | 2367 | 242.0 | 26 | 5.76 | 1.43e-07 (2^-22.74) | 22.74 |
| 26 | `pipelined:data_width=28,n_iter=25,angle_guard=3,frac_guard=4,rounding=round` | 2619 | 2559 | 242.0 | 27 | 6.23 | 7.42e-08 (2^-23.68) | 23.68 |
| 27 | `pipelined:data_width=28,n_iter=26,angle_guard=2,frac_guard=3,rounding=round` | 2646 | 2587 | 242.0 | 28 | 6.3 | 6.35e-08 (2^-23.91) | 23.91 |
| 28 | `pipelined:data_width=28,n_iter=26,angle_guard=4,frac_guard=3,rounding=round` | 2699 | 2639 | 242.0 | 28 | 6.43 | 4.35e-08 (2^-24.46) | 24.46 |
| 29 | `pipelined:data_width=28,n_iter=30,angle_guard=4,frac_guard=4,rounding=round` | 3181 | 3103 | 242.0 | 32 | 7.56 | 1.68e-08 (2^-25.83) | 25.83 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 results within 0.44us of a 1us tick, with max_abs_err <= 2^-12. Throughput >= 32 Msps is easily met by any 1-result/cycle family at modest Fmax, so the binding constraints are (1) accuracy, (2) system p99 batch latency under L2 simulation (which under-predicts by ~1.4-1.5x), and (3) area minimization. pipelined_m is the primary candidate because it offers 1/cycle throughput with tunable latency via m, and prior runs show m=4..7 dominating similar bursty specs. pipelined (m=1) is included as a fallback for lower latency if pipelined_m's p99 is too tight after L2 penalty. unrolled_k is included as a lower-area alternative with higher per-result latency, in case the area/latency trade-off favors it. iterative is excluded because it cannot achieve 1 result/cycle and would struggle with the 32-request burst within 0.44us. Budget is split roughly 50/30/20 across the three families, with the front-mapping phase (reserved portion) focusing on pipelined_m and pipelined where the Pareto front is expected to lie. Ranges are kept tight around the accuracy constraint boundary to maximize information per evaluation: dw 14..20 and n_iter 11..16 span the region where max_abs_err crosses 2^-12, while angle_guard and frac_guard are kept narrow since they have secondary effects on accuracy and area.*)
- `pipelined_m` (34 evals): data_width=14..20, n_iter=11..15, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=3..8. *Why:* Primary candidate: 1 result/cycle meets throughput_msps>=32 easily at modest Fmax. m=3..8 balances pipeline depth (latency) vs area; m=4..7 was strong on similar bursty specs. dw 14..20 and n_iter 11..15 cover the accuracy constraint (max_abs_err <= 2^-12) with margin for the L2 p99 penalty (~1.4-1.5x under-prediction). angle_guard and frac_guard kept narrow to focus budget on the dominant area/accuracy trade-off.
- `pipelined` (33 evals): data_width=14..20, n_iter=12..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Full pipeline (m=1) gives minimum latency (N+2 cycles) which helps the tight 0.44us p99 batch constraint under L2 simulation. Higher area than pipelined_m but may be needed if pipelined_m's latency is too high after the L2 penalty. n_iter 12..16 ensures accuracy margin. dw 14..20 covers the accuracy requirement.
- `unrolled_k` (33 evals): data_width=14..20, n_iter=11..15, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=4..8. *Why:* Secondary candidate: k=4..8 gives 1 result every ceil(N/k) cycles. With N=11..15 and k=4..8, that's 2-4 cycles/result. At Fmax ~200-300 MHz, throughput is 50-150 Msps, well above 32. Lower area than pipelined (no per-stage registers) but higher latency per result than pipelined_m. Worth exploring for the area/latency trade-off, though prior runs suggest it rarely reaches the front.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 6 feasible; hypervolume 4735 (n/a).

**LLM decision:** `refine` — The `pipelined` family is the only one yielding feasible designs (6/33 evals), while `unrolled_k` and `pipelined_m` failed primarily on throughput (max 12-124 MSPS vs required 32, but likely constrained by latency/queueing in the system bound or simply inefficient area for the speed). The current Pareto front is very narrow (data_width=20, n_iter=15-16). To maximize hypervolume and find a better trade-off, we need to explore if slightly wider data widths (e.g., 21-22) or different n_iter values (14-18) can reduce area while maintaining the strict accuracy (>= 12 bits, ideally higher) and throughput constraints. The `iterative` family is not yet explored but is likely too slow for the 32 MSPS throughput requirement given the 1 result/cycle limit of pipelined vs 1/N of iterative, so focusing on refining `pipelined` is the highest value action.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 4735 (gain this round: n/a (first round)).
Feasible designs: 6 of 100 evaluations (3 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 33% violate; best seen 273
- max_abs_err <= 0.000244141: 93% violate; best seen 3.84e-05 (2^-14.67)
- sys_p99_batch_us <= 0.44: 56% violate; best seen 0.161

Pareto front (feasible, 2 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined [data_width=20 n_iter=15 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=2178, accuracy_bits=13.8, luts=1095, ffs=1084, throughput_msps=264, max_abs_err=6.89e-05 (2^-13.82), power_index=2.62
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=2326, accuracy_bits=14.7, luts=1170, ffs=1156, throughput_msps=264, max_abs_err=3.84e-05 (2^-14.67), power_index=2.8
Front coverage: luts_plus_ffs 2178..2326 (HV reference 4000); accuracy_bits 13.8..14.7 (HV reference 12); data_width on the front 20..20 (registry 8..28).

Per family:
- unrolled_k: 33 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 12.75 bits
- pipelined: 33 evals, 6 feasible; max throughput seen 273 MSPS; best accuracy 14.67 bits; best feasible luts_plus_ffs=2178; feasible ranges: data_width 20..20, n_iter 15..16, angle_guard -2..1, frac_guard 2..2
- pipelined_m: 34 evals, 0 feasible; max throughput seen 124 MSPS; best accuracy 11.94 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Focus 100% of the next round on the `pipelined` family, narrowing the search space around the feasible cluster found in Round 1 to efficiently map the Pareto front.*)
- `pipelined` (100 evals): data_width=19..22, n_iter=14..18, angle_guard=-1..2, frac_guard=1..3, rounding=trunc|round. *Why:* Refine around the known feasible region (DW=20, N=15-16) to explore the trade-off curve. Slightly lower DW (19) might reduce area if accuracy holds; higher DW (21-22) might allow lower N or guards. Adjusting guards explores the accuracy/area trade-off.

**Result (code):** 100 evaluations this round, 200 total; 106 feasible; hypervolume 7954 (+68.0%).

**LLM decision:** `refine` — The `pipelined` family dominates the current Pareto front, achieving the minimum area of 1848 LUTs+FFs. The `unrolled_k` and `pipelined_m` families failed to produce feasible designs in Round 2, likely because their throughput or area characteristics were not well-sampled in the feasible region. 

1. **Refine `pipelined`**: The current front spans data_width 19-22. To improve hypervolume, we need to densely sample the low-area corner (data_width 19-20, n_iter 14-16) to ensure we have found the absolute minimum area design that meets the 2^-12 accuracy constraint. The previous search may have missed optimal combinations of `angle_guard` and `frac_guard` in this tight range.

2. **Retry `pipelined_m` with m=2**: `pipelined_m` with m=2 has the same throughput as `pipelined` (1 result/cycle) but different register overhead. It is possible that for specific `n_iter` and `data_width` combinations, `pipelined_m` (m=2) could have lower area than `pipelined` due to different critical path or LUT usage patterns. The previous round's 0 feasible designs for `pipelined_m` suggests the search space was too broad or poorly targeted. Focusing on m=2 and the known feasible data_width/n_iter ranges from `pipelined` gives it a fair chance to compete.

3. **Skip `iterative`**: `iterative` has a throughput of 1 result per N+3 cycles. For N=14, this is ~1/17 results/cycle. To meet 32 MSPS, Fmax would need to be >544 MHz, which is likely infeasible on Artix-7 for this logic depth. Thus, `iterative` is unlikely to be feasible for the throughput constraint.

4. **Skip `unrolled_k`**: Similar to `iterative`, `unrolled_k` with k=2 has throughput 1 result per ceil(N/2)+3 cycles. For N=14, this is 1/10 results/cycle. To meet 32 MSPS, Fmax > 320 MHz. While more plausible than `iterative`, the previous round showed max throughput of 12 MSPS for `unrolled_k`, suggesting the cost model estimates Fmax to be much lower or the area/latency trade-off is unfavorable. Given the strong performance of `pipelined`, it is more efficient to refine `pipelined` and retry `pipelined_m` (m=2) than to spend budget on `unrolled_k` which has already shown poor throughput estimates.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 7954 (gain this round: +68.0%).
Feasible designs: 106 of 200 evaluations (83 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 16% violate; best seen 273
- max_abs_err <= 0.000244141: 46% violate; best seen 9.91e-06 (2^-16.62)
- sys_p99_batch_us <= 0.44: 28% violate; best seen 0.161

Pareto front (feasible, 28 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined [data_width=19 n_iter=14 angle_guard=-1 frac_guard=2 rounding=trunc] luts_plus_ffs=1848, accuracy_bits=12.4, luts=909, ffs=938, throughput_msps=264, max_abs_err=0.00018 (2^-12.44), power_index=2.22
- pipelined [data_width=20 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=1963, accuracy_bits=12.9, luts=964, ffs=999, throughput_msps=264, max_abs_err=0.000132 (2^-12.89), power_index=2.36
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=1989, accuracy_bits=13.4, luts=979, ffs=1010, throughput_msps=264, max_abs_err=9.41e-05 (2^-13.38), power_index=2.39
- pipelined [data_width=19 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2117, accuracy_bits=13.8, luts=1063, ffs=1053, throughput_msps=264, max_abs_err=7.18e-05 (2^-13.77), power_index=2.55
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=2186, accuracy_bits=14.2, luts=1080, ffs=1106, throughput_msps=264, max_abs_err=5.43e-05 (2^-14.17), power_index=2.63
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=2326, accuracy_bits=14.7, luts=1170, ffs=1156, throughput_msps=264, max_abs_err=3.84e-05 (2^-14.67), power_index=2.8
- pipelined [data_width=21 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc] luts_plus_ffs=2467, accuracy_bits=15.3, luts=1219, ffs=1248, throughput_msps=264, max_abs_err=2.41e-05 (2^-15.34), power_index=2.97
- pipelined [data_width=20 n_iter=18 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=2589, accuracy_bits=15.7, luts=1301, ffs=1287, throughput_msps=264, max_abs_err=1.89e-05 (2^-15.69), power_index=3.12
- pipelined [data_width=21 n_iter=18 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=2653, accuracy_bits=15.8, luts=1313, ffs=1340, throughput_msps=257, max_abs_err=1.7e-05 (2^-15.85), power_index=3.19
- pipelined [data_width=22 n_iter=18 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=2841, accuracy_bits=16.6, luts=1431, ffs=1410, throughput_msps=257, max_abs_err=9.91e-06 (2^-16.62), power_index=3.42
Front coverage: luts_plus_ffs 1848..2841 (HV reference 4000); accuracy_bits 12.4..16.6 (HV reference 12); data_width on the front 19..22 (registry 8..28).

Per family:
- unrolled_k: 33 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 12.75 bits
- pipelined: 133 evals, 106 feasible; max throughput seen 273 MSPS; best accuracy 16.62 bits; best feasible luts_plus_ffs=1848; feasible ranges: data_width 19..22, n_iter 14..18, angle_guard -2..2, frac_guard 1..3
- pipelined_m: 34 evals, 0 feasible; max throughput seen 124 MSPS; best accuracy 11.94 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The `pipelined` family dominates the current Pareto front, achieving the minimum area of 1848 LUTs+FFs. The `unrolled_k` and `pipelined_m` families failed to produce feasible designs in Round 2, likely because their throughput or area characteristics were not well-sampled in the feasible region. 

1. **Refine `pipelined`**: The current front spans data_width 19-22. To improve hypervolume, we need to densely sample the low-area corner (data_width 19-20, n_iter 14-16) to ensure we have found the absolute minimum area design that meets the 2^-12 accuracy constraint. The previous search may have missed optimal combinations of `angle_guard` and `frac_guard` in this tight range.

2. **Retry `pipelined_m` with m=2**: `pipelined_m` with m=2 has the same throughput as `pipelined` (1 result/cycle) but different register overhead. It is possible that for specific `n_iter` and `data_width` combinations, `pipelined_m` (m=2) could have lower area than `pipelined` due to different critical path or LUT usage patterns. The previous round's 0 feasible designs for `pipelined_m` suggests the search space was too broad or poorly targeted. Focusing on m=2 and the known feasible data_width/n_iter ranges from `pipelined` gives it a fair chance to compete.

3. **Skip `iterative`**: `iterative` has a throughput of 1 result per N+3 cycles. For N=14, this is ~1/17 results/cycle. To meet 32 MSPS, Fmax would need to be >544 MHz, which is likely infeasible on Artix-7 for this logic depth. Thus, `iterative` is unlikely to be feasible for the throughput constraint.

4. **Skip `unrolled_k`**: Similar to `iterative`, `unrolled_k` with k=2 has throughput 1 result per ceil(N/2)+3 cycles. For N=14, this is 1/10 results/cycle. To meet 32 MSPS, Fmax > 320 MHz. While more plausible than `iterative`, the previous round showed max throughput of 12 MSPS for `unrolled_k`, suggesting the cost model estimates Fmax to be much lower or the area/latency trade-off is unfavorable. Given the strong performance of `pipelined`, it is more efficient to refine `pipelined` and retry `pipelined_m` (m=2) than to spend budget on `unrolled_k` which has already shown poor throughput estimates.*)
- `pipelined` (20 evals): data_width=19..20, n_iter=14..16, angle_guard=-1..2, frac_guard=1..2, rounding=trunc|round. *Why:* The current front is entirely composed of pipelined designs, with the minimum area (1848 LUTs+FFs) achieved at data_width=19, n_iter=14. To maximize hypervolume and find the true minimum area point, we must densely sample the lower-left corner of the feasible region (data_width 19-20, n_iter 14-16) where the trade-off between area and accuracy is steepest.
- `pipelined_m` (20 evals): data_width=19..20, n_iter=14..16, angle_guard=-1..2, frac_guard=1..2, rounding=trunc|round, m=2..2. *Why:* pipelined_m with m=2 is functionally similar to pipelined in terms of throughput (1 result/cycle) but may offer different area/latency trade-offs due to register placement. Since pipelined_m had 0 feasible designs in the previous round (likely due to poor initial sampling or strict constraints on m), we focus strictly on m=2 to see if it can beat the pipelined area figures while maintaining the required throughput and accuracy.

**Result (code):** 40 evaluations this round, 240 total; 146 feasible; hypervolume 9128 (+14.8%).

**LLM decision:** `stop` — The exploration has successfully identified a robust Pareto front dominated by `pipelined` and `pipelined_m` architectures that satisfy all constraints. The minimum area feasible design is a `pipelined_m` with `luts_plus_ffs=1417` and `accuracy_bits=12.4`, which comfortably meets the `max_abs_err <= 2^-12` requirement (12.44 bits > 12 bits) and the throughput constraint (164 MSPS >= 32 MSPS). The system constraint `sys_p99_batch_us <= 0.44` is also met by the best designs (best seen 0.161 us). The front covers a wide range of accuracy (12.4 to 16.6 bits) and area (1417 to 2841 LUTs+FFs), providing a good trade-off curve for the final selection rule (min luts_plus_ffs). Since this is the final round, we stop to allow the system-level simulation (L2) to validate the top candidates from this front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 9128 (gain this round: +14.8%).
Feasible designs: 146 of 240 evaluations (111 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 14% violate; best seen 273
- max_abs_err <= 0.000244141: 39% violate; best seen 9.91e-06 (2^-16.62)
- sys_p99_batch_us <= 0.44: 23% violate; best seen 0.161

Pareto front (feasible, 23 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=2 rounding=trunc m=2] luts_plus_ffs=1417, accuracy_bits=12.4, luts=909, ffs=507, throughput_msps=164, max_abs_err=0.00018 (2^-12.44), power_index=1.71
- pipelined_m [data_width=19 n_iter=16 angle_guard=-1 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=1578, accuracy_bits=13.2, luts=1017, ffs=561, throughput_msps=164, max_abs_err=0.000105 (2^-13.21), power_index=1.9
- pipelined_m [data_width=20 n_iter=16 angle_guard=-1 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=1651, accuracy_bits=13.9, luts=1064, ffs=587, throughput_msps=164, max_abs_err=6.62e-05 (2^-13.88), power_index=1.99
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=1723, accuracy_bits=14.5, luts=1112, ffs=611, throughput_msps=164, max_abs_err=4.27e-05 (2^-14.51), power_index=2.07
- pipelined [data_width=20 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2358, accuracy_bits=14.8, luts=1185, ffs=1172, throughput_msps=264, max_abs_err=3.61e-05 (2^-14.76), power_index=2.84
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=2463, accuracy_bits=15.2, luts=1219, ffs=1244, throughput_msps=264, max_abs_err=2.57e-05 (2^-15.25), power_index=2.96
- pipelined [data_width=21 n_iter=17 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=2577, accuracy_bits=15.6, luts=1297, ffs=1280, throughput_msps=257, max_abs_err=2.07e-05 (2^-15.56), power_index=3.1
- pipelined [data_width=22 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=2603, accuracy_bits=15.7, luts=1287, ffs=1317, throughput_msps=257, max_abs_err=1.83e-05 (2^-15.74), power_index=3.13
- pipelined [data_width=21 n_iter=18 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=2731, accuracy_bits=16.2, luts=1375, ffs=1356, throughput_msps=257, max_abs_err=1.31e-05 (2^-16.22), power_index=3.29
- pipelined [data_width=22 n_iter=18 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=2841, accuracy_bits=16.6, luts=1431, ffs=1410, throughput_msps=257, max_abs_err=9.91e-06 (2^-16.62), power_index=3.42
Front coverage: luts_plus_ffs 1417..2841 (HV reference 4000); accuracy_bits 12.4..16.6 (HV reference 12); data_width on the front 19..22 (registry 8..28).

Per family:
- unrolled_k: 33 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 12.75 bits
- pipelined: 153 evals, 126 feasible; max throughput seen 273 MSPS; best accuracy 16.62 bits; best feasible luts_plus_ffs=1848; feasible ranges: data_width 19..22, n_iter 14..18, angle_guard -2..2, frac_guard 1..3
- pipelined_m: 54 evals, 20 feasible; max throughput seen 164 MSPS; best accuracy 14.64 bits; best feasible luts_plus_ffs=1417; feasible ranges: data_width 19..20, n_iter 14..16, angle_guard -1..2, frac_guard 1..2, m 2..2
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (63 evals): data_width=18..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (9 front designs; box front_anchored)
- `pipelined` (97 evals): data_width=19..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (14 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 271 feasible; hypervolume 1.639e+04 (+79.6%).

**No LLM call** (code's front-mapping round): The exploration has successfully identified a robust Pareto front dominated by `pipelined` and `pipelined_m` architectures that satisfy all constraints. The minimum area feasible design is a `pipelined_m` with `luts_plus_ffs=1417` and `accuracy_bits=12.4`, which comfortably meets the `max_abs_err <= 2^-12` requirement (12.44 bits > 12 bits) and the throughput constraint (164 MSPS >= 32 MSPS). The system constraint `sys_p99_batch_us <= 0.44` is also met by the best designs (best seen 0.161 us). The front covers a wide range of accuracy (12.4 to 16.6 bits) and area (1417 to 2841 LUTs+FFs), providing a good trade-off curve for the final selection rule (min luts_plus_ffs). Since this is the final round, we stop to allow the system-level simulation (L2) to validate the top candidates from this front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.639e+04 (gain this round: +79.6%).
Feasible designs: 271 of 400 evaluations (221 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 8% violate; best seen 273
- max_abs_err <= 0.000244141: 26% violate; best seen 1.68e-08 (2^-25.83)
- sys_p99_batch_us <= 0.44: 21% violate; best seen 0.161

Pareto front (feasible, 30 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=2 rounding=trunc m=2] luts_plus_ffs=1417, accuracy_bits=12.4, luts=909, ffs=507, throughput_msps=164, max_abs_err=0.00018 (2^-12.44), power_index=1.71
- pipelined_m [data_width=19 n_iter=16 angle_guard=-1 frac_guard=1 rounding=round m=2] luts_plus_ffs=1620, accuracy_bits=13.3, luts=1057, ffs=563, throughput_msps=164, max_abs_err=0.000101 (2^-13.28), power_index=1.95
- pipelined_m [data_width=20 n_iter=16 angle_guard=-1 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=1651, accuracy_bits=13.9, luts=1064, ffs=587, throughput_msps=164, max_abs_err=6.62e-05 (2^-13.88), power_index=1.99
- pipelined_m [data_width=24 n_iter=20 angle_guard=4 frac_guard=0 rounding=round m=4] luts_plus_ffs=2114, accuracy_bits=18.5, luts=1647, ffs=467, throughput_msps=86, max_abs_err=2.71e-06 (2^-18.49), power_index=2.54
- pipelined_m [data_width=26 n_iter=20 angle_guard=4 frac_guard=1 rounding=round m=3] luts_plus_ffs=2557, accuracy_bits=18.9, luts=1862, ffs=695, throughput_msps=110, max_abs_err=2.01e-06 (2^-18.92), power_index=3.08
- pipelined_m [data_width=28 n_iter=22 angle_guard=-1 frac_guard=3 rounding=round m=3] luts_plus_ffs=2994, accuracy_bits=20.6, luts=2167, ffs=827, throughput_msps=106, max_abs_err=6.24e-07 (2^-20.61), power_index=3.6
- pipelined [data_width=28 n_iter=22 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=4105, accuracy_bits=20.8, luts=2041, ffs=2064, throughput_msps=249, max_abs_err=5.32e-07 (2^-20.84), power_index=4.94
- pipelined [data_width=28 n_iter=24 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=4677, accuracy_bits=22.4, luts=2332, ffs=2345, throughput_msps=242, max_abs_err=1.85e-07 (2^-22.37), power_index=5.63
- pipelined [data_width=28 n_iter=25 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=5177, accuracy_bits=23.7, luts=2619, ffs=2559, throughput_msps=242, max_abs_err=7.42e-08 (2^-23.68), power_index=6.23
- pipelined [data_width=28 n_iter=30 angle_guard=4 frac_guard=4 rounding=round] luts_plus_ffs=6285, accuracy_bits=25.8, luts=3181, ffs=3103, throughput_msps=242, max_abs_err=1.68e-08 (2^-25.83), power_index=7.56
Front coverage: luts_plus_ffs 1417..6285 (HV reference 4000); accuracy_bits 12.4..25.8 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- unrolled_k: 33 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 12.75 bits
- pipelined: 250 evals, 223 feasible; max throughput seen 273 MSPS; best accuracy 25.83 bits; best feasible luts_plus_ffs=1848; feasible ranges: data_width 19..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 117 evals, 48 feasible; max throughput seen 164 MSPS; best accuracy 22.70 bits; best feasible luts_plus_ffs=1417; feasible ranges: data_width 18..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 32817 in, 4895 out
- provider-reported cost: $0.0100
- full prompts and replies: `llm_trace.jsonl`

