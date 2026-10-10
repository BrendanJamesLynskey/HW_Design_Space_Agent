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
`pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 654 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 205 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 51.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0646 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000654 (2^-10.58) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 10.7 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000208 (2^-12.23) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 3.41 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.6 | exact: bit-accurate model, exhaustive (65536 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 5 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 79.3 dBc, SNR 70.6 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: bursty requests: bursts of 8 (0 ns apart) arriving as a Poisson process, 2 requests/us on average. Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_latency_us <= 0.4 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=4` | 0.1124 → 0.1351 | yes |
| `pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 0.1124 → 0.1351 | yes |
| `pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=1,rounding=round,m=4` | 0.1124 → 0.1351 | yes |
| `pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=2,rounding=round,m=4` | 0.1124 → 0.1351 | yes |
| `pipelined_m:data_width=15,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=5` | 0.1365 → 0.172 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (30 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=4` | 654 | 205 | 97.8 | 5 | 0.0646 | 0.000654 (2^-10.58) | 10.58 |
| 1 | `pipelined_m:data_width=16,n_iter=12,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 689 | 210 | 97.8 | 5 | 0.0676 | 0.000609 (2^-10.68) | 10.68 |
| 2 | `pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=1,rounding=round,m=4` | 711 | 211 | 97.8 | 5 | 0.0694 | 0.000568 (2^-10.78) | 10.78 |
| 3 | `pipelined_m:data_width=16,n_iter=12,angle_guard=2,frac_guard=2,rounding=round,m=4` | 734 | 215 | 97.8 | 5 | 0.0714 | 0.000548 (2^-10.83) | 10.83 |
| 4 | `pipelined_m:data_width=15,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=5` | 790 | 200 | 80.6 | 5 | 0.0745 | 0.000403 (2^-11.28) | 11.28 |
| 5 | `pipelined_m:data_width=15,n_iter=14,angle_guard=3,frac_guard=1,rounding=round,m=5` | 804 | 203 | 80.6 | 5 | 0.0757 | 0.000346 (2^-11.50) | 11.50 |
| 6 | `pipelined_m:data_width=19,n_iter=13,angle_guard=0,frac_guard=0,rounding=trunc,m=5` | 802 | 232 | 77.0 | 5 | 0.0778 | 0.000287 (2^-11.77) | 11.77 |
| 7 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 827 | 274 | 97.8 | 6 | 0.0829 | 0.00027 (2^-11.85) | 11.85 |
| 8 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=4` | 834 | 270 | 97.8 | 6 | 0.083 | 0.000209 (2^-12.22) | 12.22 |
| 9 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=4` | 861 | 276 | 97.8 | 6 | 0.0856 | 0.000204 (2^-12.26) | 12.26 |
| 10 | `pipelined_m:data_width=20,n_iter=14,angle_guard=-2,frac_guard=1,rounding=round,m=5` | 952 | 243 | 77.0 | 5 | 0.0899 | 0.000175 (2^-12.48) | 12.48 |
| 11 | `pipelined_m:data_width=24,n_iter=14,angle_guard=-2,frac_guard=0,rounding=round,m=7` | 1046 | 204 | 54.3 | 4 | 0.0941 | 0.000124 (2^-12.98) | 12.98 |
| 12 | `pipelined_m:data_width=20,n_iter=15,angle_guard=3,frac_guard=2,rounding=round,m=8` | 1124 | 188 | 48.0 | 4 | 0.0987 | 6.44e-05 (2^-13.92) | 13.92 |
| 13 | `pipelined_m:data_width=20,n_iter=18,angle_guard=3,frac_guard=0,rounding=trunc,m=7` | 1241 | 252 | 54.3 | 5 | 0.112 | 4.23e-05 (2^-14.53) | 14.53 |
| 14 | `pipelined_m:data_width=22,n_iter=17,angle_guard=-1,frac_guard=3,rounding=trunc,m=5` | 1303 | 353 | 73.7 | 6 | 0.125 | 2.45e-05 (2^-15.32) | 15.32 |
| 15 | `pipelined_m:data_width=20,n_iter=18,angle_guard=3,frac_guard=2,rounding=round,m=5` | 1355 | 337 | 73.7 | 6 | 0.127 | 1.42e-05 (2^-16.11) | 16.11 |
| 16 | `pipelined_m:data_width=26,n_iter=18,angle_guard=0,frac_guard=4,rounding=trunc,m=7` | 1653 | 326 | 52.0 | 5 | 0.149 | 7.89e-06 (2^-16.95) | 16.95 |
| 17 | `pipelined_m:data_width=24,n_iter=19,angle_guard=0,frac_guard=2,rounding=trunc,m=4` | 1561 | 463 | 89.6 | 7 | 0.152 | 5.47e-06 (2^-17.48) | 17.48 |
| 18 | `pipelined_m:data_width=26,n_iter=20,angle_guard=-2,frac_guard=0,rounding=trunc,m=5` | 1647 | 387 | 73.7 | 6 | 0.153 | 3.27e-06 (2^-18.22) | 18.22 |
| 19 | `pipelined_m:data_width=26,n_iter=20,angle_guard=-1,frac_guard=0,rounding=trunc,m=5` | 1667 | 391 | 73.7 | 6 | 0.155 | 2.63e-06 (2^-18.54) | 18.54 |
| 20 | `pipelined_m:data_width=26,n_iter=20,angle_guard=0,frac_guard=0,rounding=trunc,m=6` | 1687 | 395 | 62.5 | 6 | 0.157 | 2.47e-06 (2^-18.63) | 18.63 |
| 21 | `pipelined_m:data_width=27,n_iter=20,angle_guard=0,frac_guard=0,rounding=round,m=5` | 1747 | 410 | 70.6 | 6 | 0.162 | 2.1e-06 (2^-18.86) | 18.86 |
| 22 | `pipelined_m:data_width=27,n_iter=20,angle_guard=0,frac_guard=4,rounding=trunc,m=5` | 1907 | 434 | 67.8 | 6 | 0.176 | 2.07e-06 (2^-18.88) | 18.88 |
| 23 | `pipelined_m:data_width=24,n_iter=24,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 2017 | 555 | 86.0 | 8 | 0.193 | 1.76e-06 (2^-19.11) | 19.11 |
| 24 | `pipelined_m:data_width=24,n_iter=24,angle_guard=3,frac_guard=1,rounding=round,m=4` | 2067 | 557 | 86.0 | 8 | 0.197 | 9.16e-07 (2^-20.06) | 20.06 |
| 25 | `pipelined_m:data_width=24,n_iter=25,angle_guard=2,frac_guard=3,rounding=round,m=5` | 2231 | 483 | 70.6 | 7 | 0.204 | 6.35e-07 (2^-20.59) | 20.59 |
| 26 | `pipelined_m:data_width=27,n_iter=26,angle_guard=-1,frac_guard=3,rounding=trunc,m=8` | 2429 | 424 | 45.9 | 6 | 0.215 | 6.21e-07 (2^-20.62) | 20.62 |
| 27 | `pipelined_m:data_width=27,n_iter=26,angle_guard=0,frac_guard=3,rounding=trunc,m=8` | 2455 | 428 | 45.9 | 6 | 0.217 | 2.81e-07 (2^-21.76) | 21.76 |
| 28 | `pipelined_m:data_width=26,n_iter=26,angle_guard=4,frac_guard=2,rounding=round,m=4` | 2484 | 707 | 86.0 | 9 | 0.24 | 1.39e-07 (2^-22.78) | 22.78 |
| 29 | `pipelined_m:data_width=27,n_iter=30,angle_guard=3,frac_guard=3,rounding=trunc,m=6` | 2939 | 538 | 59.9 | 7 | 0.262 | 8.12e-08 (2^-23.55) | 23.55 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The p99 <= 0.4us burst constraint and 2 req/us throughput favor high sustained throughput, so I focus on pipelined and pipelined_m (1 result/cycle) plus unrolled_k (k/cycle) rather than iterative. Accuracy needs >=10 bits, so data_width ~12-16 with n_iter ~10-14 and round rounding should clear max_abs_err <= 2^-10. Budget is split to map the area/latency trade-off across these families, with the reserved front-mapping later covering full ranges.*)
- `pipelined` (40 evals): data_width=12..16, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* One result/cycle drains 8-request bursts fastest, making p99 <= 0.4us most plausible; full pipeline is the area/latency trade-off core.
- `pipelined_m` (35 evals): data_width=12..16, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* Register-every-m stages keeps 1 result/cycle throughput while cutting FFs vs full pipeline, directly targeting the min luts_plus_ffs objective.
- `unrolled_k` (25 evals): data_width=12..16, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=round, k=2..4. *Why:* k chained rotations/cycle gives sub-cycle burst drain with lower area than full pipeline; covers the throughput-vs-area region between iterative and pipelined.

**Result (code):** 100 evaluations this round, 100 total; 48 feasible; hypervolume 4446 (n/a).

**LLM decision:** `refine` — The front is entirely pipelined_m (982-1137 luts_plus_ffs, 10.8-12.3 accuracy_bits) with pipelined as a distant second (1358+). unrolled_k produced 0 feasible designs. The feasible region is well-localized: data_width 14-16, n_iter 12-14, angle_guard 0-2, frac_guard 0-2. Narrowing both pipelined_m and pipelined to these proven feasible ranges will let NSGA-II densely map the trade-off curve, improving hypervolume. iterative is not worth adding: its N+3 cycle latency and shared datapath make it unlikely to beat pipelined_m on area while meeting the bursty p99 latency constraint.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 4446 (gain this round: n/a (first round)).
Feasible designs: 48 of 100 evaluations (36 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 46% violate; best seen 0.000204 (2^-12.26)
- sys_p99_latency_us <= 0.4: 25% violate; best seen 0.066

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=982, accuracy_bits=10.8, luts=711, ffs=270, throughput_msps=124, max_abs_err=0.000568 (2^-10.78), power_index=0.0739
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=2 rounding=round m=3] luts_plus_ffs=1011, accuracy_bits=10.8, luts=734, ffs=276, throughput_msps=124, max_abs_err=0.000548 (2^-10.83), power_index=0.0761
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1035, accuracy_bits=11.7, luts=772, ffs=262, throughput_msps=97.8, max_abs_err=0.000294 (2^-11.73), power_index=0.0778
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1104, accuracy_bits=12.2, luts=834, ffs=270, throughput_msps=97.8, max_abs_err=0.000209 (2^-12.22), power_index=0.083
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1137, accuracy_bits=12.3, luts=861, ffs=276, throughput_msps=97.8, max_abs_err=0.000204 (2^-12.26), power_index=0.0856
Front coverage: luts_plus_ffs 982..1137 (HV reference 3000); accuracy_bits 10.8..12.3 (HV reference 10); data_width on the front 16..16 (registry 8..28).

Per family:
- unrolled_k: 25 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 10.70 bits
- pipelined: 40 evals, 24 feasible; max throughput seen 282 MSPS; best accuracy 11.73 bits; best feasible luts_plus_ffs=1358; feasible ranges: data_width 15..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 35 evals, 24 feasible; max throughput seen 178 MSPS; best accuracy 12.26 bits; best feasible luts_plus_ffs=982; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The front is entirely pipelined_m (982-1137 luts_plus_ffs, 10.8-12.3 accuracy_bits) with pipelined as a distant second (1358+). unrolled_k produced 0 feasible designs (max throughput 13.5 MSPS, but likely failing sys_p99_latency or accuracy). The feasible region is well-localized: data_width 14-16, n_iter 12-14, angle_guard 0-2, frac_guard 0-2. The 46% accuracy violation rate in round 1 suggests many random points fell outside this box. Narrowing both pipelined_m and pipelined to the proven feasible ranges will let NSGA-II densely map the trade-off curve within the region that satisfies all constraints, improving hypervolume coverage. iterative is not worth adding: it produces one result every N+3 cycles (e.g., 15+ cycles for N=12), giving throughput ~6.7 MSPS at 100 MHz, which is above the 2 MSPS constraint but its latency (15+ cycles) and shared-datapath structure make it unlikely to beat pipelined_m on area while meeting the 0.4 us p99 latency bound for bursty traffic. The current front already spans a useful range of accuracy (10.8-12.3 bits) and area (982-1137), and refining within the feasible box should tighten the front and push hypervolume up.*)
- `pipelined_m` (50 evals): data_width=14..16, n_iter=12..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m dominates the front (982-1137 luts_plus_ffs vs 1358 for pipelined). Narrowing to the proven feasible box (data_width 14-16, n_iter 12-14, angle_guard 0-2, frac_guard 0-2, m 2-4) focuses the budget on refining the trade-off curve between area and accuracy within the region that actually meets the constraints.
- `pipelined` (50 evals): data_width=14..16, n_iter=12..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined is the second-best family (best feasible 1358 luts_plus_ffs). Keeping it in the search with the same narrowed ranges ensures the front captures any pipelined designs that might beat pipelined_m at higher accuracy_bits (pipelined reached 11.73 bits feasible; pipelined_m reached 12.26). This maintains coverage of the accuracy axis of the Pareto front.

**Result (code):** 100 evaluations this round, 200 total; 131 feasible; hypervolume 4546 (+2.3%).

**LLM decision:** `add_family` — The current Pareto front is dominated by `pipelined_m` designs with `data_width=16` and `n_iter` between 12 and 14. The best area is 859 LUTs+FFs. However, `unrolled_k` has been explored (25 evals) and yielded 0 feasible designs, likely due to throughput or latency constraints in the bursty scenario, or simply because the cost model penalized the shared datapath/FSM overhead for the required accuracy. The `iterative` family has not been explored yet. While `iterative` typically has higher latency (N+3 cycles) and lower throughput (1 result per N+3 cycles), it has the lowest area overhead (single datapath, no pipeline registers). Given the objective is to minimize `luts_plus_ffs`, it is possible that a low-iteration `iterative` design (e.g., N=12-14) could beat the 859 area mark if the throughput constraint (>= 2 MSPS) and p99 latency constraint (<= 0.4 us) are met. With N=12, latency is 15 cycles. If Fmax is high enough (e.g., > 37.5 MHz), throughput is > 2 MSPS. The p99 latency constraint is tight (0.4 us). If the clock is fast, the latency in ns might be small. However, `iterative` throughput is 1/(N+3) * Fmax. For N=12, that's 1/15 * Fmax. To get 2 MSPS, Fmax must be >= 30 MHz. This is easily achievable. The main risk is the p99 latency in the system simulation. But since we are at L1 screening, we can check the analytic bound. The `iterative` family might offer a lower area solution (e.g., < 859) because it avoids the pipeline registers of `pipelined_m`. Therefore, exploring `iterative` is a logical next step to see if it can push the area lower on the front.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 4546 (gain this round: +2.3%).
Feasible designs: 131 of 200 evaluations (90 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 32% violate; best seen 0.000204 (2^-12.26)
- sys_p99_latency_us <= 0.4: 12% violate; best seen 0.066

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=859, accuracy_bits=10.6, luts=654, ffs=205, throughput_msps=97.8, max_abs_err=0.000654 (2^-10.58), power_index=0.0646
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=899, accuracy_bits=10.7, luts=689, ffs=210, throughput_msps=97.8, max_abs_err=0.000609 (2^-10.68), power_index=0.0676
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=922, accuracy_bits=10.8, luts=711, ffs=211, throughput_msps=97.8, max_abs_err=0.000568 (2^-10.78), power_index=0.0694
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=949, accuracy_bits=10.8, luts=734, ffs=215, throughput_msps=97.8, max_abs_err=0.000548 (2^-10.83), power_index=0.0714
- pipelined_m [data_width=16 n_iter=13 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=990, accuracy_bits=11.1, luts=726, ffs=264, throughput_msps=97.8, max_abs_err=0.00046 (2^-11.09), power_index=0.0745
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1033, accuracy_bits=11.3, luts=713, ffs=320, throughput_msps=124, max_abs_err=0.00041 (2^-11.25), power_index=0.0777
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1035, accuracy_bits=11.7, luts=772, ffs=262, throughput_msps=97.8, max_abs_err=0.000294 (2^-11.73), power_index=0.0778
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1102, accuracy_bits=11.9, luts=827, ffs=274, throughput_msps=97.8, max_abs_err=0.00027 (2^-11.85), power_index=0.0829
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1104, accuracy_bits=12.2, luts=834, ffs=270, throughput_msps=97.8, max_abs_err=0.000209 (2^-12.22), power_index=0.083
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1137, accuracy_bits=12.3, luts=861, ffs=276, throughput_msps=97.8, max_abs_err=0.000204 (2^-12.26), power_index=0.0856
Front coverage: luts_plus_ffs 859..1137 (HV reference 3000); accuracy_bits 10.6..12.3 (HV reference 10); data_width on the front 16..16 (registry 8..28).

Per family:
- unrolled_k: 25 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 10.70 bits
- pipelined: 90 evals, 61 feasible; max throughput seen 282 MSPS; best accuracy 11.73 bits; best feasible luts_plus_ffs=1297; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 85 evals, 70 feasible; max throughput seen 178 MSPS; best accuracy 12.26 bits; best feasible luts_plus_ffs=859; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The `iterative` family is the only one not yet explored. It has the lowest area overhead per stage but higher latency. Given the area objective, it is worth checking if it can provide a better area-accuracy trade-off than `pipelined_m` in the feasible region.*)
- `iterative` (40 evals): data_width=14..16, n_iter=12..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Explore the unexplored `iterative` family in the same parameter region as the current front (data_width 14-16, n_iter 12-14) to check if its lower area overhead (no pipeline registers) can beat the current best of 859 LUTs+FFs while meeting throughput and latency constraints.

**Result (code):** 40 evaluations this round, 240 total; 131 feasible; hypervolume 4546 (+0.0%).

**LLM decision:** `stop` — The front is dominated by pipelined_m designs, which are strictly cheaper than pipelined (best 859 vs 1297 luts_plus_ffs) and cover the full accuracy range of interest (10.6 to 12.3 bits). The selection rule (min luts_plus_ffs) picks the pipelined_m design with 859 luts_plus_ffs, which comfortably meets the throughput (97.8 >= 2) and accuracy (10.6 bits >= 10) constraints. The system constraint (sys_p99_latency_us <= 0.4) is also met by the best designs (best seen 0.066 us). Since this is the final round and the front is well-mapped with no further improvement possible, we stop.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 4546 (gain this round: +0.0%).
Feasible designs: 131 of 240 evaluations (90 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 29% violate; best seen 0.000204 (2^-12.26)
- sys_p99_latency_us <= 0.4: 27% violate; best seen 0.066

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=859, accuracy_bits=10.6, luts=654, ffs=205, throughput_msps=97.8, max_abs_err=0.000654 (2^-10.58), power_index=0.0646
- pipelined_m [data_width=16 n_iter=12 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=899, accuracy_bits=10.7, luts=689, ffs=210, throughput_msps=97.8, max_abs_err=0.000609 (2^-10.68), power_index=0.0676
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=922, accuracy_bits=10.8, luts=711, ffs=211, throughput_msps=97.8, max_abs_err=0.000568 (2^-10.78), power_index=0.0694
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=949, accuracy_bits=10.8, luts=734, ffs=215, throughput_msps=97.8, max_abs_err=0.000548 (2^-10.83), power_index=0.0714
- pipelined_m [data_width=16 n_iter=13 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=990, accuracy_bits=11.1, luts=726, ffs=264, throughput_msps=97.8, max_abs_err=0.00046 (2^-11.09), power_index=0.0745
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1033, accuracy_bits=11.3, luts=713, ffs=320, throughput_msps=124, max_abs_err=0.00041 (2^-11.25), power_index=0.0777
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1035, accuracy_bits=11.7, luts=772, ffs=262, throughput_msps=97.8, max_abs_err=0.000294 (2^-11.73), power_index=0.0778
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1102, accuracy_bits=11.9, luts=827, ffs=274, throughput_msps=97.8, max_abs_err=0.00027 (2^-11.85), power_index=0.0829
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1104, accuracy_bits=12.2, luts=834, ffs=270, throughput_msps=97.8, max_abs_err=0.000209 (2^-12.22), power_index=0.083
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1137, accuracy_bits=12.3, luts=861, ffs=276, throughput_msps=97.8, max_abs_err=0.000204 (2^-12.26), power_index=0.0856
Front coverage: luts_plus_ffs 859..1137 (HV reference 3000); accuracy_bits 10.6..12.3 (HV reference 10); data_width on the front 16..16 (registry 8..28).

Per family:
- iterative: 40 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 11.27 bits
- unrolled_k: 25 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 10.70 bits
- pipelined: 90 evals, 61 feasible; max throughput seen 282 MSPS; best accuracy 11.73 bits; best feasible luts_plus_ffs=1297; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 85 evals, 70 feasible; max throughput seen 178 MSPS; best accuracy 12.26 bits; best feasible luts_plus_ffs=859; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (160 evals): data_width=15..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (10 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 276 feasible; hypervolume 1.386e+04 (+204.9%).

**No LLM call** (code's front-mapping round): The front is dominated by pipelined_m designs, which are strictly cheaper than pipelined (best 859 vs 1297 luts_plus_ffs) and cover the full accuracy range of interest (10.6 to 12.3 bits). The selection rule (min luts_plus_ffs) picks the pipelined_m design with 859 luts_plus_ffs, which comfortably meets the throughput (97.8 >= 2) and accuracy (10.6 bits >= 10) constraints. The system constraint (sys_p99_latency_us <= 0.4) is also met by the best designs (best seen 0.066 us). Since this is the final round and the front is well-mapped with no further improvement possible, we stop.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.386e+04 (gain this round: +204.9%).
Feasible designs: 276 of 400 evaluations (229 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 21% violate; best seen 8.12e-08 (2^-23.55)
- sys_p99_latency_us <= 0.4: 16% violate; best seen 0.066

Pareto front (feasible, 30 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=859, accuracy_bits=10.6, luts=654, ffs=205, throughput_msps=97.8, max_abs_err=0.000654 (2^-10.58), power_index=0.0646
- pipelined_m [data_width=16 n_iter=12 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=949, accuracy_bits=10.8, luts=734, ffs=215, throughput_msps=97.8, max_abs_err=0.000548 (2^-10.83), power_index=0.0714
- pipelined_m [data_width=19 n_iter=13 angle_guard=0 frac_guard=0 rounding=trunc m=5] luts_plus_ffs=1034, accuracy_bits=11.8, luts=802, ffs=232, throughput_msps=77, max_abs_err=0.000287 (2^-11.77), power_index=0.0778
- pipelined_m [data_width=20 n_iter=14 angle_guard=-2 frac_guard=1 rounding=round m=5] luts_plus_ffs=1195, accuracy_bits=12.5, luts=952, ffs=243, throughput_msps=77, max_abs_err=0.000175 (2^-12.48), power_index=0.0899
- pipelined_m [data_width=20 n_iter=18 angle_guard=3 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=1494, accuracy_bits=14.5, luts=1241, ffs=252, throughput_msps=54.3, max_abs_err=4.23e-05 (2^-14.53), power_index=0.112
- pipelined_m [data_width=26 n_iter=18 angle_guard=0 frac_guard=4 rounding=trunc m=7] luts_plus_ffs=1979, accuracy_bits=17, luts=1653, ffs=326, throughput_msps=52, max_abs_err=7.89e-06 (2^-16.95), power_index=0.149
- pipelined_m [data_width=26 n_iter=20 angle_guard=-1 frac_guard=0 rounding=trunc m=5] luts_plus_ffs=2058, accuracy_bits=18.5, luts=1667, ffs=391, throughput_msps=73.7, max_abs_err=2.63e-06 (2^-18.54), power_index=0.155
- pipelined_m [data_width=24 n_iter=24 angle_guard=3 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=2572, accuracy_bits=19.1, luts=2017, ffs=555, throughput_msps=86, max_abs_err=1.76e-06 (2^-19.11), power_index=0.193
- pipelined_m [data_width=27 n_iter=26 angle_guard=-1 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=2853, accuracy_bits=20.6, luts=2429, ffs=424, throughput_msps=45.9, max_abs_err=6.21e-07 (2^-20.62), power_index=0.215
- pipelined_m [data_width=27 n_iter=30 angle_guard=3 frac_guard=3 rounding=trunc m=6] luts_plus_ffs=3477, accuracy_bits=23.6, luts=2939, ffs=538, throughput_msps=59.9, max_abs_err=8.12e-08 (2^-23.55), power_index=0.262
Front coverage: luts_plus_ffs 859..3477 (HV reference 3000); accuracy_bits 10.6..23.6 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 40 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 11.27 bits
- unrolled_k: 25 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 10.70 bits
- pipelined: 90 evals, 61 feasible; max throughput seen 282 MSPS; best accuracy 11.73 bits; best feasible luts_plus_ffs=1297; feasible ranges: data_width 14..16, n_iter 12..14, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 245 evals, 215 feasible; max throughput seen 178 MSPS; best accuracy 23.55 bits; best feasible luts_plus_ffs=859; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 1)
- tokens: 27608 in, 3418 out
- provider-reported cost: $0.0075
- full prompts and replies: `llm_trace.jsonl`

