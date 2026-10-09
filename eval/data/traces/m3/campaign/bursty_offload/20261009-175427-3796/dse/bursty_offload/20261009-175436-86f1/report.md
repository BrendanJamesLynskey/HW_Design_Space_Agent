# DSE run: bursty_offload

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 4 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec bursty_offload: Sin/cos offload for an 8-channel sensor front end: bursts of 8 requests arrive as a Poisson process, 2 requests/us on average; p99 request latency must be <= 0.4 us. Max error <= 2^-10. Minimise LUTs + FFs.
  constraint: throughput_msps >= 2
  constraint: max_abs_err <= 0.000976562
  constraint: sys_p99_latency_us <= 0.4
  objective: min luts_plus_ffs (HV ref 3000)
  objective: max accuracy_bits (HV ref 10)
  select: min luts_plus_ffs
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): bursty requests: bursts of 8 (0 ns apart) arriving as a Poisson process, 2 requests/us on average
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=15,n_iter=12,angle_guard=1,frac_guard=1,rounding=trunc,m=6` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 631 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 139 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 68.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 68.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 58.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.058 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000833 (2^-10.23) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.82 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000239 (2^-12.03) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.96 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.2 | exact: bit-accurate model, exhaustive (32768 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 4 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 79.9 dBc, SNR 69.7 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: bursty requests: bursts of 8 (0 ns apart) arriving as a Poisson process, 2 requests/us on average. Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_latency_us <= 0.4 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=15,n_iter=12,angle_guard=1,frac_guard=1,rounding=trunc,m=6` | 0.1459 → 0.1953 | yes |
| `pipelined_m:data_width=15,n_iter=12,angle_guard=1,frac_guard=1,rounding=trunc,m=7` | 0.1678 → 0.2328 | yes |
| `pipelined_m:data_width=15,n_iter=12,angle_guard=2,frac_guard=1,rounding=trunc,m=7` | 0.1678 → 0.2328 | yes |
| `pipelined_m:data_width=14,n_iter=12,angle_guard=3,frac_guard=2,rounding=round,m=6` | 0.1459 → 0.1953 | yes |
| `pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=1,rounding=trunc,m=6` | 0.1459 → 0.1953 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (47 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=12,angle_guard=1,frac_guard=1,rounding=trunc,m=7` | 631 | 139 | 59.6 | 4 | 0.058 | 0.000833 (2^-10.23) | 10.23 |
| 1 | `pipelined_m:data_width=15,n_iter=12,angle_guard=1,frac_guard=1,rounding=trunc,m=6` | 631 | 139 | 68.5 | 4 | 0.058 | 0.000833 (2^-10.23) | 10.23 |
| 2 | `pipelined_m:data_width=15,n_iter=12,angle_guard=2,frac_guard=1,rounding=trunc,m=7` | 643 | 141 | 59.6 | 4 | 0.059 | 0.000811 (2^-10.27) | 10.27 |
| 3 | `pipelined_m:data_width=14,n_iter=12,angle_guard=3,frac_guard=2,rounding=round,m=6` | 672 | 139 | 68.5 | 4 | 0.0611 | 0.000724 (2^-10.43) | 10.43 |
| 4 | `pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=1,rounding=trunc,m=7` | 666 | 147 | 59.6 | 4 | 0.0612 | 0.000649 (2^-10.59) | 10.59 |
| 5 | `pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=1,rounding=trunc,m=6` | 666 | 147 | 68.5 | 4 | 0.0612 | 0.000649 (2^-10.59) | 10.59 |
| 6 | `pipelined_m:data_width=16,n_iter=12,angle_guard=3,frac_guard=1,rounding=trunc,m=6` | 689 | 151 | 65.4 | 4 | 0.0632 | 0.000643 (2^-10.60) | 10.60 |
| 7 | `pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=1,rounding=round,m=7` | 700 | 149 | 59.6 | 4 | 0.0639 | 0.000624 (2^-10.65) | 10.65 |
| 8 | `pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 701 | 151 | 52.7 | 4 | 0.0641 | 0.000597 (2^-10.71) | 10.71 |
| 9 | `pipelined_m:data_width=15,n_iter=13,angle_guard=1,frac_guard=2,rounding=trunc,m=7` | 713 | 141 | 59.6 | 4 | 0.0643 | 0.000528 (2^-10.89) | 10.89 |
| 10 | `pipelined_m:data_width=14,n_iter=13,angle_guard=3,frac_guard=2,rounding=round,m=7` | 730 | 139 | 59.6 | 4 | 0.0654 | 0.00049 (2^-10.99) | 10.99 |
| 11 | `pipelined_m:data_width=15,n_iter=13,angle_guard=3,frac_guard=2,rounding=trunc,m=7` | 739 | 145 | 59.6 | 4 | 0.0665 | 0.000466 (2^-11.07) | 11.07 |
| 12 | `pipelined_m:data_width=16,n_iter=13,angle_guard=2,frac_guard=1,rounding=trunc,m=8` | 739 | 149 | 52.7 | 4 | 0.0668 | 0.00046 (2^-11.09) | 11.09 |
| 13 | `pipelined_m:data_width=15,n_iter=13,angle_guard=3,frac_guard=2,rounding=round,m=8` | 770 | 147 | 52.7 | 4 | 0.069 | 0.000385 (2^-11.34) | 11.34 |
| 14 | `pipelined_m:data_width=16,n_iter=13,angle_guard=2,frac_guard=1,rounding=round,m=8` | 772 | 151 | 52.7 | 4 | 0.0695 | 0.000325 (2^-11.59) | 11.59 |
| 15 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 827 | 151 | 52.7 | 4 | 0.0736 | 0.00027 (2^-11.85) | 11.85 |
| 16 | `pipelined_m:data_width=16,n_iter=14,angle_guard=3,frac_guard=2,rounding=trunc,m=8` | 841 | 153 | 50.3 | 4 | 0.0748 | 0.000264 (2^-11.89) | 11.89 |
| 17 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=6` | 861 | 215 | 68.5 | 5 | 0.0809 | 0.000204 (2^-12.26) | 12.26 |
| 18 | `pipelined_m:data_width=16,n_iter=14,angle_guard=3,frac_guard=4,rounding=round,m=6` | 929 | 226 | 65.4 | 5 | 0.0869 | 0.00017 (2^-12.52) | 12.52 |
| 19 | `pipelined_m:data_width=16,n_iter=14,angle_guard=4,frac_guard=4,rounding=round,m=6` | 943 | 229 | 65.4 | 5 | 0.0882 | 0.000161 (2^-12.60) | 12.60 |
| 20 | `pipelined_m:data_width=21,n_iter=14,angle_guard=-1,frac_guard=1,rounding=trunc,m=6` | 964 | 255 | 65.4 | 5 | 0.0917 | 0.000133 (2^-12.88) | 12.88 |
| 21 | `pipelined_m:data_width=24,n_iter=14,angle_guard=-2,frac_guard=1,rounding=trunc,m=8` | 1074 | 206 | 48.0 | 4 | 0.0963 | 0.000124 (2^-12.98) | 12.98 |
| 22 | `pipelined_m:data_width=16,n_iter=17,angle_guard=3,frac_guard=4,rounding=trunc,m=7` | 1101 | 224 | 56.8 | 5 | 0.0997 | 0.00011 (2^-13.15) | 13.15 |
| 23 | `pipelined_m:data_width=19,n_iter=17,angle_guard=2,frac_guard=0,rounding=trunc,m=6` | 1101 | 238 | 65.4 | 5 | 0.101 | 7.8e-05 (2^-13.65) | 13.65 |
| 24 | `pipelined_m:data_width=19,n_iter=17,angle_guard=3,frac_guard=1,rounding=trunc,m=6` | 1152 | 245 | 65.4 | 5 | 0.105 | 4.85e-05 (2^-14.33) | 14.33 |
| 25 | `pipelined_m:data_width=21,n_iter=16,angle_guard=-1,frac_guard=2,rounding=trunc,m=6` | 1143 | 259 | 62.5 | 5 | 0.106 | 4.68e-05 (2^-14.38) | 14.38 |
| 26 | `pipelined_m:data_width=21,n_iter=17,angle_guard=3,frac_guard=1,rounding=round,m=7` | 1297 | 269 | 54.3 | 5 | 0.118 | 1.95e-05 (2^-15.64) | 15.64 |
| 27 | `pipelined_m:data_width=24,n_iter=17,angle_guard=2,frac_guard=0,rounding=trunc,m=8` | 1354 | 294 | 48.0 | 5 | 0.124 | 1.65e-05 (2^-15.88) | 15.88 |
| 28 | `pipelined_m:data_width=23,n_iter=17,angle_guard=3,frac_guard=1,rounding=round,m=5` | 1403 | 373 | 73.7 | 6 | 0.134 | 1.61e-05 (2^-15.92) | 15.92 |
| 29 | `pipelined_m:data_width=26,n_iter=17,angle_guard=1,frac_guard=1,rounding=trunc,m=6` | 1472 | 317 | 59.9 | 5 | 0.135 | 1.54e-05 (2^-15.99) | 15.99 |
| 30 | `pipelined_m:data_width=21,n_iter=21,angle_guard=1,frac_guard=1,rounding=trunc,m=6` | 1523 | 335 | 65.4 | 6 | 0.14 | 1.38e-05 (2^-16.15) | 16.15 |
| 31 | `pipelined_m:data_width=24,n_iter=20,angle_guard=-2,frac_guard=1,rounding=round,m=8` | 1618 | 288 | 48.0 | 5 | 0.143 | 7.33e-06 (2^-17.06) | 17.06 |
| 32 | `pipelined_m:data_width=24,n_iter=21,angle_guard=-1,frac_guard=0,rounding=trunc,m=7` | 1628 | 285 | 54.3 | 5 | 0.144 | 4.38e-06 (2^-17.80) | 17.80 |
| 33 | `pipelined_m:data_width=24,n_iter=20,angle_guard=1,frac_guard=0,rounding=trunc,m=6` | 1587 | 371 | 62.5 | 6 | 0.147 | 3.91e-06 (2^-17.96) | 17.96 |
| 34 | `pipelined_m:data_width=24,n_iter=20,angle_guard=2,frac_guard=1,rounding=round,m=6` | 1698 | 383 | 62.5 | 6 | 0.157 | 2.59e-06 (2^-18.56) | 18.56 |
| 35 | `pipelined_m:data_width=26,n_iter=20,angle_guard=2,frac_guard=1,rounding=trunc,m=7` | 1767 | 320 | 52.0 | 5 | 0.157 | 2.13e-06 (2^-18.84) | 18.84 |
| 36 | `pipelined_m:data_width=22,n_iter=21,angle_guard=4,frac_guard=3,rounding=round,m=6` | 1780 | 375 | 62.5 | 6 | 0.162 | 1.9e-06 (2^-19.01) | 19.01 |
| 37 | `pipelined_m:data_width=23,n_iter=22,angle_guard=3,frac_guard=3,rounding=round,m=4` | 1913 | 557 | 89.6 | 8 | 0.186 | 1.1e-06 (2^-19.79) | 19.79 |
| 38 | `pipelined_m:data_width=28,n_iter=24,angle_guard=-1,frac_guard=1,rounding=trunc,m=8` | 2211 | 333 | 45.9 | 5 | 0.191 | 3.05e-07 (2^-21.64) | 21.64 |
| 39 | `pipelined_m:data_width=28,n_iter=24,angle_guard=-1,frac_guard=3,rounding=trunc,m=7` | 2308 | 438 | 49.9 | 6 | 0.207 | 3.04e-07 (2^-21.65) | 21.65 |
| 40 | `pipelined_m:data_width=26,n_iter=24,angle_guard=4,frac_guard=4,rounding=trunc,m=7` | 2332 | 436 | 52.0 | 6 | 0.208 | 2.02e-07 (2^-22.24) | 22.24 |
| 41 | `pipelined_m:data_width=27,n_iter=24,angle_guard=2,frac_guard=3,rounding=round,m=6` | 2365 | 438 | 59.9 | 6 | 0.211 | 1.7e-07 (2^-22.49) | 22.49 |
| 42 | `pipelined_m:data_width=28,n_iter=25,angle_guard=3,frac_guard=1,rounding=trunc,m=6` | 2408 | 539 | 57.5 | 7 | 0.222 | 1.3e-07 (2^-22.88) | 22.88 |
| 43 | `pipelined_m:data_width=27,n_iter=25,angle_guard=3,frac_guard=3,rounding=trunc,m=6` | 2433 | 538 | 59.9 | 7 | 0.224 | 1.19e-07 (2^-23.01) | 23.01 |
| 44 | `pipelined_m:data_width=28,n_iter=25,angle_guard=3,frac_guard=4,rounding=round,m=6` | 2619 | 565 | 57.5 | 7 | 0.24 | 7.42e-08 (2^-23.68) | 23.68 |
| 45 | `pipelined_m:data_width=26,n_iter=30,angle_guard=4,frac_guard=4,rounding=round,m=6` | 2994 | 536 | 59.9 | 7 | 0.266 | 6.94e-08 (2^-23.78) | 23.78 |
| 46 | `pipelined_m:data_width=27,n_iter=29,angle_guard=3,frac_guard=4,rounding=round,m=4` | 2954 | 847 | 82.7 | 10 | 0.286 | 4.54e-08 (2^-24.39) | 24.39 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires throughput >= 2 Msps, max_abs_err <= 2^-10 (accuracy_bits >= 10), and sys_p99_latency <= 0.4 us under bursty Poisson load (bursts of 8, 2 req/us mean). The selection rule minimises luts_plus_ffs. Pipelined families (pipelined_m, pipelined) are the natural fit: 1 result/cycle throughput trivially meets the 2 Msps constraint, and their low per-result latency handles 8-deep bursts well. pipelined_m is prioritised (55%) because the m parameter lets us trade pipeline registers for area, directly targeting the luts_plus_ffs objective. pipelined (30%) maps the minimum-latency corner to confirm the p99 bound is met and to see if the extra registers are worth it. unrolled_k (15%) is included as a potentially cheaper alternative: with k=8 and N~10-14, it needs only 2-4 cycles per result, giving ample throughput, and avoids the per-stage register cost of pipelined designs. The iterative family is excluded because its 1-result-per-(N+3)-cycles throughput and high latency make it very likely to violate the p99 latency constraint under burst load. Parameter ranges are focused: data_width 12-16 and n_iter 10-14 bracket the accuracy_bits >= 10 requirement (accuracy depends on these plus guards); angle_guard and frac_guard span their full ranges to let the optimizer find the cheapest guard configuration that still meets accuracy; rounding is binary. This focuses the 400-eval budget on the region where feasible, competitive designs live.*)
- `pipelined_m` (55 evals): data_width=12..16, n_iter=10..14, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Primary candidate. 1 result/cycle throughput easily clears the 2 Msps constraint and handles 8-deep bursts without queueing. The m parameter allows trading area (fewer registers) against latency/Fmax. With n_iter ~10-14 and data_width ~12-16, accuracy_bits >= 10 is achievable. Minimising luts_plus_ffs is the selection rule, so pipelined_m with larger m (fewer pipeline registers) should find the cheapest point on the front.
- `pipelined` (30 evals): data_width=12..16, n_iter=10..14, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Full pipeline (m=1) gives minimum latency (N+2 cycles) which is best for p99 latency under burst load. Higher area than pipelined_m but may be needed if pipelined_m's latency is too high. Useful to map the latency-vs-area trade-off and confirm whether pipelined_m can match the p99 bound.
- `unrolled_k` (15 evals): data_width=12..16, n_iter=10..14, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* Secondary candidate. With k=8, latency is ceil(N/8)+3 ~ 4-5 cycles, which at high Fmax could meet p99 <= 0.4 us. Lower area than pipelined (no per-stage registers) but throughput is 1 result per ceil(N/k) cycles. For N=10, k=8: 2 cycles/result, so at 100 MHz = 500 Msps throughput, well above 2 Msps. The risk is burst handling: 8 requests in 0 ns need 8 consecutive slots; with 2 cycles/result, a burst takes 16 cycles. At 100 MHz that is 160 ns, well within 0.4 us. Worth exploring as a potentially cheaper alternative.

**Result (code):** 100 evaluations this round, 100 total; 39 feasible; hypervolume 3901 (n/a).

**LLM decision:** `refine` — The current Pareto front is dominated by `pipelined_m` designs with `data_width` 15-16 and `n_iter` 12-14. The `pipelined` family is significantly more expensive (min 1427 LUTs+FFs vs 841 for `pipelined_m`) and `unrolled_k` failed to meet throughput constraints. The `iterative` family is not yet explored, but given the throughput requirement (>= 2 MSPS) and the bursty nature of the system (p99 latency <= 0.4us), `iterative` (N+3 cycles/result) is likely too slow for high-throughput scenarios unless N is very small, which would compromise accuracy. However, the current front is clustered in a narrow region of the parameter space. To maximize hypervolume and find the true minimum area design, we should refine the search around the best `pipelined_m` candidates. Specifically, we should focus on `data_width` 14-16, `n_iter` 11-13, `angle_guard` 1-3, `frac_guard` 1-2, and `m` 4-8. This will allow Optuna to explore the trade-off between area and accuracy more densely in the promising region. We should also consider adding `iterative` to see if it offers any low-area solutions, but given the throughput constraint, it is less likely to be competitive. Therefore, refining the `pipelined_m` ranges is the best next step.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 3901 (gain this round: n/a (first round)).
Feasible designs: 39 of 100 evaluations (30 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 59% violate; best seen 0.00027 (2^-11.85)
- sys_p99_latency_us <= 0.4: 15% violate; best seen 0.0639

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=2 frac_guard=1 rounding=trunc m=5] luts_plus_ffs=841, accuracy_bits=10.3, luts=643, ffs=198, throughput_msps=80.6, max_abs_err=0.000811 (2^-10.27), power_index=0.0632
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=852, accuracy_bits=10.7, luts=701, ffs=151, throughput_msps=52.7, max_abs_err=0.000597 (2^-10.71), power_index=0.0641
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=1 rounding=round m=8] luts_plus_ffs=863, accuracy_bits=10.8, luts=711, ffs=151, throughput_msps=52.7, max_abs_err=0.000568 (2^-10.78), power_index=0.0649
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=2 rounding=round m=7] luts_plus_ffs=888, accuracy_bits=10.8, luts=734, ffs=153, throughput_msps=59.6, max_abs_err=0.000548 (2^-10.83), power_index=0.0668
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=1 rounding=trunc m=8] luts_plus_ffs=888, accuracy_bits=11.1, luts=739, ffs=149, throughput_msps=52.7, max_abs_err=0.00046 (2^-11.09), power_index=0.0668
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=1 rounding=round m=8] luts_plus_ffs=924, accuracy_bits=11.6, luts=772, ffs=151, throughput_msps=52.7, max_abs_err=0.000325 (2^-11.59), power_index=0.0695
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=979, accuracy_bits=11.9, luts=827, ffs=151, throughput_msps=52.7, max_abs_err=0.00027 (2^-11.85), power_index=0.0736
Front coverage: luts_plus_ffs 841..979 (HV reference 3000); accuracy_bits 10.3..11.9 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- unrolled_k: 15 evals, 0 feasible; max throughput seen 12.4 MSPS; best accuracy 10.89 bits
- pipelined: 30 evals, 8 feasible; max throughput seen 282 MSPS; best accuracy 11.74 bits; best feasible luts_plus_ffs=1427; feasible ranges: data_width 13..16, n_iter 13..14, angle_guard 2..3, frac_guard 2..3
- pipelined_m: 55 evals, 31 feasible; max throughput seen 178 MSPS; best accuracy 11.85 bits; best feasible luts_plus_ffs=841; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard -1..4, frac_guard 1..4, m 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Refine the search around the best `pipelined_m` candidates and explore the `iterative` family to ensure comprehensive coverage of the design space.*)
- `pipelined_m` (80 evals): data_width=14..16, n_iter=11..13, angle_guard=1..3, frac_guard=1..2, rounding=trunc|round, m=4..8. *Why:* Refine around the best feasible designs to find the minimum area solution and improve hypervolume coverage in the promising region.
- `iterative` (20 evals): data_width=14..16, n_iter=10..14, angle_guard=1..3, frac_guard=1..2, rounding=trunc|round. *Why:* Explore the unexplored `iterative` family to see if it offers any low-area solutions, although it is less likely to be competitive due to throughput constraints.

**Result (code):** 100 evaluations this round, 200 total; 98 feasible; hypervolume 3940 (+1.0%).

**LLM decision:** `refine` — The front is dominated by `pipelined_m` (90 feasible vs 8 for `pipelined`), with the best area (770 LUTs+FFs) and a wide spread of accuracy (10.2-11.9 bits). `iterative` and `unrolled_k` are infeasible due to throughput constraints (max 15.3/12.4 MSPs vs required 2 MSPs, but likely failing p99 latency or throughput in the specific bursty context, though the summary says 0 feasible, likely due to the strict p99 latency bound of 0.4us which requires high throughput/low latency). The current front covers luts_plus_ffs 770-979. To maximize hypervolume and find the true Pareto optimum, we should focus the search on the `pipelined_m` family in the region where it is clearly superior. We will narrow the ranges to exclude the less efficient `pipelined` family and focus on the high-performing `pipelined_m` parameters: data_width 14-16, n_iter 12-14, m 6-8 (which covers the best designs), and explore angle_guard/frac_guard/rounding more densely in this box to fill in the trade-off curve between area and accuracy.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 3940 (gain this round: +1.0%).
Feasible designs: 98 of 200 evaluations (75 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 44% violate; best seen 0.000225 (2^-12.12)
- sys_p99_latency_us <= 0.4: 18% violate; best seen 0.0639

Pareto front (feasible, 15 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=1 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=770, accuracy_bits=10.2, luts=631, ffs=139, throughput_msps=59.6, max_abs_err=0.000833 (2^-10.23), power_index=0.058
- pipelined_m [data_width=15 n_iter=12 angle_guard=2 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=784, accuracy_bits=10.3, luts=643, ffs=141, throughput_msps=59.6, max_abs_err=0.000811 (2^-10.27), power_index=0.059
- pipelined_m [data_width=14 n_iter=12 angle_guard=3 frac_guard=2 rounding=round m=6] luts_plus_ffs=812, accuracy_bits=10.4, luts=672, ffs=139, throughput_msps=68.5, max_abs_err=0.000724 (2^-10.43), power_index=0.0611
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=813, accuracy_bits=10.6, luts=666, ffs=147, throughput_msps=68.5, max_abs_err=0.000649 (2^-10.59), power_index=0.0612
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=1 rounding=round m=7] luts_plus_ffs=849, accuracy_bits=10.6, luts=700, ffs=149, throughput_msps=59.6, max_abs_err=0.000624 (2^-10.65), power_index=0.0639
- pipelined_m [data_width=15 n_iter=13 angle_guard=1 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=855, accuracy_bits=10.9, luts=713, ffs=141, throughput_msps=59.6, max_abs_err=0.000528 (2^-10.89), power_index=0.0643
- pipelined_m [data_width=14 n_iter=13 angle_guard=3 frac_guard=2 rounding=round m=7] luts_plus_ffs=869, accuracy_bits=11, luts=730, ffs=139, throughput_msps=59.6, max_abs_err=0.00049 (2^-10.99), power_index=0.0654
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=1 rounding=trunc m=8] luts_plus_ffs=888, accuracy_bits=11.1, luts=739, ffs=149, throughput_msps=52.7, max_abs_err=0.00046 (2^-11.09), power_index=0.0668
- pipelined_m [data_width=15 n_iter=13 angle_guard=3 frac_guard=2 rounding=round m=8] luts_plus_ffs=918, accuracy_bits=11.3, luts=770, ffs=147, throughput_msps=52.7, max_abs_err=0.000385 (2^-11.34), power_index=0.069
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=979, accuracy_bits=11.9, luts=827, ffs=151, throughput_msps=52.7, max_abs_err=0.00027 (2^-11.85), power_index=0.0736
Front coverage: luts_plus_ffs 770..979 (HV reference 3000); accuracy_bits 10.2..11.9 (HV reference 10); data_width on the front 14..16 (registry 8..28).

Per family:
- iterative: 20 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 12.12 bits
- unrolled_k: 15 evals, 0 feasible; max throughput seen 12.4 MSPS; best accuracy 10.89 bits
- pipelined: 30 evals, 8 feasible; max throughput seen 282 MSPS; best accuracy 11.74 bits; best feasible luts_plus_ffs=1427; feasible ranges: data_width 13..16, n_iter 13..14, angle_guard 2..3, frac_guard 2..3
- pipelined_m: 135 evals, 90 feasible; max throughput seen 178 MSPS; best accuracy 11.85 bits; best feasible luts_plus_ffs=770; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard -1..4, frac_guard 1..4, m 2..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Narrowing to pipelined_m with m=6-8 and data_width=14-16 focuses the budget on the proven efficient region.*)
- `pipelined_m` (40 evals): data_width=14..16, n_iter=12..14, angle_guard=-1..4, frac_guard=1..4, rounding=trunc|round, m=6..8. *Why:* Focus on the dominant family and the specific parameter ranges that produced the current Pareto front to refine the trade-off curve.

**Result (code):** 40 evaluations this round, 240 total; 136 feasible; hypervolume 5352 (+35.8%).

**LLM decision:** `stop` — The front is well-populated and feasible: 136 feasible designs with a hypervolume of 5352, and the front spans luts_plus_ffs 770..1172 and accuracy_bits 10.2..12.6. The cheapest design (pipelined_m, 770 LUTs+FFs) meets all constraints (throughput 59.6 MSPS >= 2, max_abs_err 0.000833 <= 0.000976562, and the family's best sys_p99_latency is 0.0639 us <= 0.4 us). Since this is the final round, the front is good enough to select from.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 5352 (gain this round: +35.8%).
Feasible designs: 136 of 240 evaluations (103 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 37% violate; best seen 0.000161 (2^-12.60)
- sys_p99_latency_us <= 0.4: 15% violate; best seen 0.0639

Pareto front (feasible, 20 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=1 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=770, accuracy_bits=10.2, luts=631, ffs=139, throughput_msps=59.6, max_abs_err=0.000833 (2^-10.23), power_index=0.058
- pipelined_m [data_width=15 n_iter=12 angle_guard=2 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=784, accuracy_bits=10.3, luts=643, ffs=141, throughput_msps=59.6, max_abs_err=0.000811 (2^-10.27), power_index=0.059
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=813, accuracy_bits=10.6, luts=666, ffs=147, throughput_msps=59.6, max_abs_err=0.000649 (2^-10.59), power_index=0.0612
- pipelined_m [data_width=16 n_iter=12 angle_guard=3 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=840, accuracy_bits=10.6, luts=689, ffs=151, throughput_msps=65.4, max_abs_err=0.000643 (2^-10.60), power_index=0.0632
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=852, accuracy_bits=10.7, luts=701, ffs=151, throughput_msps=52.7, max_abs_err=0.000597 (2^-10.71), power_index=0.0641
- pipelined_m [data_width=15 n_iter=13 angle_guard=3 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=884, accuracy_bits=11.1, luts=739, ffs=145, throughput_msps=59.6, max_abs_err=0.000466 (2^-11.07), power_index=0.0665
- pipelined_m [data_width=15 n_iter=13 angle_guard=3 frac_guard=2 rounding=round m=8] luts_plus_ffs=918, accuracy_bits=11.3, luts=770, ffs=147, throughput_msps=52.7, max_abs_err=0.000385 (2^-11.34), power_index=0.069
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=979, accuracy_bits=11.9, luts=827, ffs=151, throughput_msps=52.7, max_abs_err=0.00027 (2^-11.85), power_index=0.0736
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=6] luts_plus_ffs=1076, accuracy_bits=12.3, luts=861, ffs=215, throughput_msps=68.5, max_abs_err=0.000204 (2^-12.26), power_index=0.0809
- pipelined_m [data_width=16 n_iter=14 angle_guard=4 frac_guard=4 rounding=round m=6] luts_plus_ffs=1172, accuracy_bits=12.6, luts=943, ffs=229, throughput_msps=65.4, max_abs_err=0.000161 (2^-12.60), power_index=0.0882
Front coverage: luts_plus_ffs 770..1172 (HV reference 3000); accuracy_bits 10.2..12.6 (HV reference 10); data_width on the front 14..16 (registry 8..28).

Per family:
- iterative: 20 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 12.12 bits
- unrolled_k: 15 evals, 0 feasible; max throughput seen 12.4 MSPS; best accuracy 10.89 bits
- pipelined: 30 evals, 8 feasible; max throughput seen 282 MSPS; best accuracy 11.74 bits; best feasible luts_plus_ffs=1427; feasible ranges: data_width 13..16, n_iter 13..14, angle_guard 2..3, frac_guard 2..3
- pipelined_m: 175 evals, 128 feasible; max throughput seen 178 MSPS; best accuracy 12.60 bits; best feasible luts_plus_ffs=770; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard -1..4, frac_guard 1..4, m 2..8
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (160 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (20 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 282 feasible; hypervolume 1.515e+04 (+183.0%).

**No LLM call** (code's front-mapping round): The front is well-populated and feasible: 136 feasible designs with a hypervolume of 5352, and the front spans luts_plus_ffs 770..1172 and accuracy_bits 10.2..12.6. The cheapest design (pipelined_m, 770 LUTs+FFs) meets all constraints (throughput 59.6 MSPS >= 2, max_abs_err 0.000833 <= 0.000976562, and the family's best sys_p99_latency is 0.0639 us <= 0.4 us). Since this is the final round, the front is good enough to select from.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.515e+04 (gain this round: +183.0%).
Feasible designs: 282 of 400 evaluations (244 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 26% violate; best seen 4.54e-08 (2^-24.39)
- sys_p99_latency_us <= 0.4: 9% violate; best seen 0.0639

Pareto front (feasible, 47 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=1 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=770, accuracy_bits=10.2, luts=631, ffs=139, throughput_msps=59.6, max_abs_err=0.000833 (2^-10.23), power_index=0.058
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=813, accuracy_bits=10.6, luts=666, ffs=147, throughput_msps=68.5, max_abs_err=0.000649 (2^-10.59), power_index=0.0612
- pipelined_m [data_width=14 n_iter=13 angle_guard=3 frac_guard=2 rounding=round m=7] luts_plus_ffs=869, accuracy_bits=11, luts=730, ffs=139, throughput_msps=59.6, max_abs_err=0.00049 (2^-10.99), power_index=0.0654
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=979, accuracy_bits=11.9, luts=827, ffs=151, throughput_msps=52.7, max_abs_err=0.00027 (2^-11.85), power_index=0.0736
- pipelined_m [data_width=21 n_iter=14 angle_guard=-1 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=1219, accuracy_bits=12.9, luts=964, ffs=255, throughput_msps=65.4, max_abs_err=0.000133 (2^-12.88), power_index=0.0917
- pipelined_m [data_width=21 n_iter=17 angle_guard=3 frac_guard=1 rounding=round m=7] luts_plus_ffs=1567, accuracy_bits=15.6, luts=1297, ffs=269, throughput_msps=54.3, max_abs_err=1.95e-05 (2^-15.64), power_index=0.118
- pipelined_m [data_width=24 n_iter=20 angle_guard=-2 frac_guard=1 rounding=round m=8] luts_plus_ffs=1905, accuracy_bits=17.1, luts=1618, ffs=288, throughput_msps=48, max_abs_err=7.33e-06 (2^-17.06), power_index=0.143
- pipelined_m [data_width=22 n_iter=21 angle_guard=4 frac_guard=3 rounding=round m=6] luts_plus_ffs=2155, accuracy_bits=19, luts=1780, ffs=375, throughput_msps=62.5, max_abs_err=1.9e-06 (2^-19.01), power_index=0.162
- pipelined_m [data_width=27 n_iter=24 angle_guard=2 frac_guard=3 rounding=round m=6] luts_plus_ffs=2802, accuracy_bits=22.5, luts=2365, ffs=438, throughput_msps=59.9, max_abs_err=1.7e-07 (2^-22.49), power_index=0.211
- pipelined_m [data_width=27 n_iter=29 angle_guard=3 frac_guard=4 rounding=round m=4] luts_plus_ffs=3801, accuracy_bits=24.4, luts=2954, ffs=847, throughput_msps=82.7, max_abs_err=4.54e-08 (2^-24.39), power_index=0.286
Front coverage: luts_plus_ffs 770..3801 (HV reference 3000); accuracy_bits 10.2..24.4 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 20 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 12.12 bits
- unrolled_k: 15 evals, 0 feasible; max throughput seen 12.4 MSPS; best accuracy 10.89 bits
- pipelined: 30 evals, 8 feasible; max throughput seen 282 MSPS; best accuracy 11.74 bits; best feasible luts_plus_ffs=1427; feasible ranges: data_width 13..16, n_iter 13..14, angle_guard 2..3, frac_guard 2..3
- pipelined_m: 335 evals, 274 feasible; max throughput seen 178 MSPS; best accuracy 24.39 bits; best feasible luts_plus_ffs=770; feasible ranges: data_width 13..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 27285 in, 3893 out
- provider-reported cost: $0.0085
- full prompts and replies: `llm_trace.jsonl`

