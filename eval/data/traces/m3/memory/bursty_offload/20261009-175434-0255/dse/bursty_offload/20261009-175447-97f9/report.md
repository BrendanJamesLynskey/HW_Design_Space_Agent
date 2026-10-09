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
`pipelined_m:data_width=15,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 620 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 194 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 51.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0612 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000835 (2^-10.23) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.84 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00024 (2^-12.02) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.97 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.2 | exact: bit-accurate model, exhaustive (32768 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 5 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 79.7 dBc, SNR 69.5 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: bursty requests: bursts of 8 (0 ns apart) arriving as a Poisson process, 2 requests/us on average. Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_latency_us <= 0.4 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=15,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=4` | 0.1124 → 0.1351 | yes |
| `pipelined_m:data_width=15,n_iter=12,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 0.1124 → 0.1351 | yes |
| `pipelined_m:data_width=15,n_iter=12,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 0.1124 → 0.1351 | yes |
| `pipelined_m:data_width=16,n_iter=12,angle_guard=0,frac_guard=0,rounding=round,m=3` | 0.09642 → 0.1066 | yes |
| `pipelined_m:data_width=17,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=4` | 0.1176 → 0.1412 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (39 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=4` | 620 | 194 | 97.8 | 5 | 0.0612 | 0.000835 (2^-10.23) | 10.23 |
| 1 | `pipelined_m:data_width=15,n_iter=12,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 643 | 198 | 97.8 | 5 | 0.0632 | 0.000811 (2^-10.27) | 10.27 |
| 2 | `pipelined_m:data_width=15,n_iter=12,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 654 | 199 | 97.8 | 5 | 0.0642 | 0.000772 (2^-10.34) | 10.34 |
| 3 | `pipelined_m:data_width=16,n_iter=12,angle_guard=0,frac_guard=0,rounding=round,m=3` | 631 | 254 | 124.5 | 6 | 0.0666 | 0.000712 (2^-10.46) | 10.46 |
| 4 | `pipelined_m:data_width=17,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=4` | 689 | 216 | 93.6 | 5 | 0.0681 | 0.000556 (2^-10.81) | 10.81 |
| 5 | `pipelined_m:data_width=19,n_iter=12,angle_guard=-1,frac_guard=1,rounding=trunc,m=8` | 747 | 167 | 50.3 | 4 | 0.0688 | 0.000526 (2^-10.89) | 10.89 |
| 6 | `pipelined_m:data_width=20,n_iter=12,angle_guard=-1,frac_guard=0,rounding=trunc,m=8` | 759 | 174 | 50.3 | 4 | 0.0701 | 0.000517 (2^-10.92) | 10.92 |
| 7 | `pipelined_m:data_width=16,n_iter=13,angle_guard=1,frac_guard=0,rounding=round,m=4` | 701 | 258 | 97.8 | 6 | 0.0721 | 0.000417 (2^-11.23) | 11.23 |
| 8 | `pipelined_m:data_width=16,n_iter=13,angle_guard=2,frac_guard=0,rounding=round,m=4` | 713 | 262 | 97.8 | 6 | 0.0734 | 0.00041 (2^-11.25) | 11.25 |
| 9 | `pipelined_m:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=4` | 745 | 254 | 97.8 | 6 | 0.0752 | 0.0004 (2^-11.29) | 11.29 |
| 10 | `pipelined_m:data_width=17,n_iter=13,angle_guard=2,frac_guard=0,rounding=round,m=4` | 751 | 276 | 93.6 | 6 | 0.0773 | 0.000312 (2^-11.65) | 11.65 |
| 11 | `pipelined_m:data_width=17,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=4` | 786 | 268 | 97.8 | 6 | 0.0793 | 0.000301 (2^-11.70) | 11.70 |
| 12 | `pipelined_m:data_width=18,n_iter=13,angle_guard=2,frac_guard=0,rounding=round,m=4` | 789 | 291 | 93.6 | 6 | 0.0812 | 0.000277 (2^-11.82) | 11.82 |
| 13 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 827 | 274 | 97.8 | 6 | 0.0829 | 0.00027 (2^-11.85) | 11.85 |
| 14 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=4` | 861 | 276 | 97.8 | 6 | 0.0856 | 0.000204 (2^-12.26) | 12.26 |
| 15 | `pipelined_m:data_width=16,n_iter=14,angle_guard=4,frac_guard=1,rounding=round,m=4` | 861 | 278 | 93.6 | 6 | 0.0857 | 0.000203 (2^-12.26) | 12.26 |
| 16 | `pipelined_m:data_width=19,n_iter=15,angle_guard=-1,frac_guard=2,rounding=trunc,m=8` | 979 | 169 | 50.3 | 4 | 0.0864 | 0.000127 (2^-12.94) | 12.94 |
| 17 | `pipelined_m:data_width=19,n_iter=15,angle_guard=-1,frac_guard=3,rounding=trunc,m=8` | 1008 | 172 | 50.3 | 4 | 0.0888 | 0.000125 (2^-12.97) | 12.97 |
| 18 | `pipelined_m:data_width=19,n_iter=15,angle_guard=0,frac_guard=2,rounding=trunc,m=7` | 994 | 240 | 56.8 | 5 | 0.0928 | 9.73e-05 (2^-13.33) | 13.33 |
| 19 | `pipelined_m:data_width=19,n_iter=15,angle_guard=4,frac_guard=4,rounding=trunc,m=8` | 1112 | 184 | 48.0 | 4 | 0.0974 | 6.96e-05 (2^-13.81) | 13.81 |
| 20 | `pipelined_m:data_width=19,n_iter=16,angle_guard=3,frac_guard=2,rounding=round,m=6` | 1152 | 251 | 65.4 | 5 | 0.106 | 4.29e-05 (2^-14.51) | 14.51 |
| 21 | `pipelined_m:data_width=21,n_iter=17,angle_guard=-1,frac_guard=1,rounding=round,m=7` | 1230 | 257 | 56.8 | 5 | 0.112 | 3.38e-05 (2^-14.85) | 14.85 |
| 22 | `pipelined_m:data_width=24,n_iter=16,angle_guard=-1,frac_guard=0,rounding=trunc,m=6` | 1222 | 285 | 62.5 | 5 | 0.113 | 3.23e-05 (2^-14.92) | 14.92 |
| 23 | `pipelined_m:data_width=21,n_iter=18,angle_guard=1,frac_guard=0,rounding=trunc,m=4` | 1259 | 401 | 93.6 | 7 | 0.125 | 2.55e-05 (2^-15.26) | 15.26 |
| 24 | `pipelined_m:data_width=25,n_iter=18,angle_guard=-2,frac_guard=0,rounding=trunc,m=8` | 1420 | 293 | 48.0 | 5 | 0.129 | 9.71e-06 (2^-16.65) | 16.65 |
| 25 | `pipelined_m:data_width=25,n_iter=18,angle_guard=1,frac_guard=0,rounding=trunc,m=8` | 1474 | 302 | 48.0 | 5 | 0.134 | 8.31e-06 (2^-16.88) | 16.88 |
| 26 | `pipelined_m:data_width=24,n_iter=18,angle_guard=1,frac_guard=2,rounding=round,m=6` | 1543 | 301 | 62.5 | 5 | 0.139 | 8e-06 (2^-16.93) | 16.93 |
| 27 | `pipelined_m:data_width=24,n_iter=20,angle_guard=-1,frac_guard=1,rounding=round,m=8` | 1638 | 291 | 48.0 | 5 | 0.145 | 4.26e-06 (2^-17.84) | 17.84 |
| 28 | `pipelined_m:data_width=24,n_iter=21,angle_guard=-1,frac_guard=2,rounding=trunc,m=8` | 1712 | 293 | 48.0 | 5 | 0.151 | 3.76e-06 (2^-18.02) | 18.02 |
| 29 | `pipelined_m:data_width=23,n_iter=23,angle_guard=1,frac_guard=3,rounding=trunc,m=6` | 1906 | 375 | 62.5 | 6 | 0.172 | 2.2e-06 (2^-18.79) | 18.79 |
| 30 | `pipelined_m:data_width=24,n_iter=22,angle_guard=3,frac_guard=0,rounding=round,m=4` | 1798 | 545 | 86.0 | 8 | 0.176 | 1.62e-06 (2^-19.24) | 19.24 |
| 31 | `pipelined_m:data_width=24,n_iter=23,angle_guard=1,frac_guard=2,rounding=trunc,m=5` | 1929 | 468 | 73.7 | 7 | 0.18 | 1.34e-06 (2^-19.51) | 19.51 |
| 32 | `pipelined_m:data_width=24,n_iter=22,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1937 | 567 | 86.0 | 8 | 0.188 | 8e-07 (2^-20.25) | 20.25 |
| 33 | `pipelined_m:data_width=28,n_iter=23,angle_guard=1,frac_guard=0,rounding=trunc,m=6` | 2115 | 428 | 59.9 | 6 | 0.191 | 4.04e-07 (2^-21.24) | 21.24 |
| 34 | `pipelined_m:data_width=28,n_iter=24,angle_guard=-1,frac_guard=1,rounding=round,m=6` | 2270 | 428 | 59.9 | 6 | 0.203 | 3.19e-07 (2^-21.58) | 21.58 |
| 35 | `pipelined_m:data_width=28,n_iter=24,angle_guard=-1,frac_guard=1,rounding=round,m=7` | 2270 | 428 | 52.0 | 6 | 0.203 | 3.19e-07 (2^-21.58) | 21.58 |
| 36 | `pipelined_m:data_width=28,n_iter=24,angle_guard=3,frac_guard=0,rounding=trunc,m=5` | 2259 | 531 | 67.8 | 7 | 0.21 | 2.63e-07 (2^-21.86) | 21.86 |
| 37 | `pipelined_m:data_width=27,n_iter=24,angle_guard=3,frac_guard=1,rounding=round,m=5` | 2292 | 524 | 70.6 | 7 | 0.212 | 1.96e-07 (2^-22.28) | 22.28 |
| 38 | `pipelined_m:data_width=27,n_iter=24,angle_guard=3,frac_guard=3,rounding=round,m=5` | 2389 | 540 | 70.6 | 7 | 0.22 | 1.54e-07 (2^-22.63) | 22.63 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The key challenge is meeting the p99 latency constraint of 0.4 us for 8-request bursts arriving as a Poisson process at 2 requests/us. The prior campaign showed that iterative CORDIC dominates for low-rate area-min specs, but for this bursty workload, higher throughput is needed. I'm prioritizing pipelined_m (45% budget) because it offers 1 result/cycle throughput with reduced FF count compared to fully pipelined, making it the best area-throughput trade-off. unrolled_k (30%) is next because k=2..4 micro-rotations/cycle can achieve sufficient throughput with moderate area. pipelined (15%) serves as a high-throughput reference, and iterative (10%) is included to capture the low-area end of the Pareto front, even though it may fail the latency constraint. All families use data_width 14-18 and n_iter 10-14 to target the max_abs_err <= 2^-10 constraint while keeping area low. The angle_guard and frac_guard ranges are kept narrow (0-2) to focus the search on configurations that meet accuracy without excessive area overhead.*)
- `pipelined_m` (45 evals): data_width=14..18, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m is the primary candidate for meeting the p99 latency constraint. It provides 1 result/cycle throughput, which is essential to drain 8-request bursts within 0.4 us. By registering every m stages (m=2..4), it reduces FF count compared to fully pipelined while maintaining high throughput. The data_width range 14-18 and n_iter 10-14 target the accuracy requirement (max_abs_err <= 2^-10) while keeping area low. m=2-4 balances latency (ceil(N/m)+2 cycles) against FF savings.
- `unrolled_k` (30 evals): data_width=14..18, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k with k=2..4 micro-rotations/cycle can achieve higher effective throughput than iterative while using fewer FFs than pipelined_m. With k=4 and N=12, it completes in 3+3=6 cycles per result, which at ~150 MHz gives ~40 ns/result. For 8 back-to-back requests, this is ~320 ns, potentially meeting the 0.4 us p99 bound. The shared FSM and barrel shifters keep LUT count moderate. This family offers a good area-throughput trade-off for bursty workloads.
- `pipelined` (15 evals): data_width=14..18, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Fully pipelined CORDIC guarantees 1 result/cycle with N+2 latency. While it uses more FFs than pipelined_m, it provides the highest Fmax potential and lowest per-request latency. This family serves as a reference point for the Pareto front and may be needed if pipelined_m and unrolled_k fail to meet the p99 latency constraint. The same data_width and n_iter ranges target the accuracy requirement.
- `iterative` (10 evals): data_width=14..18, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative has the lowest area but produces one result every N+3 cycles. At ~150 MHz with N=12, that's ~80 ns per request, so 8 back-to-back requests take ~640 ns, which likely violates the 0.4 us p99 latency bound. However, it may still appear on the Pareto front for the area-accuracy trade-off, and the system simulation will confirm whether it can meet the latency constraint under the Poisson burst pattern. Including it with a small budget share ensures we capture the full trade-off curve.

**Result (code):** 100 evaluations this round, 100 total; 49 feasible; hypervolume 4443 (n/a).

**LLM decision:** `refine` — The current front is dominated by pipelined_m designs with n_iter=13. To improve hypervolume, we need to: (1) explore lower n_iter (12) in pipelined_m to potentially find cheaper designs, and (2) explore higher accuracy designs in pipelined (n_iter 13-15) to extend the front towards higher accuracy_bits. The iterative and unrolled_k families are infeasible due to throughput constraints (max 15.3 and 13.5 MSPS respectively, well below the 2 MSPS requirement when considering the bursty system constraints), so they should be excluded. The sys_p99_latency constraint is met by all feasible designs (best seen 0.066 us << 0.4 us), so it is not a binding constraint for the feasible region.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 4443 (gain this round: n/a (first round)).
Feasible designs: 49 of 100 evaluations (36 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 273
- max_abs_err <= 0.000976562: 31% violate; best seen 0.000163 (2^-12.58)
- sys_p99_latency_us <= 0.4: 40% violate; best seen 0.066

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=13 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=938, accuracy_bits=10.5, luts=688, ffs=250, throughput_msps=97.8, max_abs_err=0.000689 (2^-10.50), power_index=0.0706
- pipelined_m [data_width=16 n_iter=13 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=959, accuracy_bits=11.2, luts=701, ffs=258, throughput_msps=97.8, max_abs_err=0.000417 (2^-11.23), power_index=0.0721
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=976, accuracy_bits=11.3, luts=713, ffs=262, throughput_msps=97.8, max_abs_err=0.00041 (2^-11.25), power_index=0.0734
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1038, accuracy_bits=11.4, luts=764, ffs=274, throughput_msps=97.8, max_abs_err=0.000378 (2^-11.37), power_index=0.0781
- pipelined_m [data_width=18 n_iter=13 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1046, accuracy_bits=11.6, luts=764, ffs=282, throughput_msps=97.8, max_abs_err=0.000316 (2^-11.63), power_index=0.0787
- pipelined_m [data_width=18 n_iter=13 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1080, accuracy_bits=11.8, luts=789, ffs=291, throughput_msps=93.6, max_abs_err=0.000277 (2^-11.82), power_index=0.0812
- pipelined_m [data_width=18 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1143, accuracy_bits=11.8, luts=840, ffs=303, throughput_msps=93.6, max_abs_err=0.000274 (2^-11.83), power_index=0.086
- pipelined [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=round] luts_plus_ffs=1780, accuracy_bits=12.4, luts=893, ffs=888, throughput_msps=264, max_abs_err=0.000179 (2^-12.45), power_index=0.134
Front coverage: luts_plus_ffs 938..1780 (HV reference 3000); accuracy_bits 10.5..12.4 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 12.26 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 12.58 bits
- pipelined: 15 evals, 11 feasible; max throughput seen 273 MSPS; best accuracy 12.45 bits; best feasible luts_plus_ffs=1433; feasible ranges: data_width 14..18, n_iter 13..14, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 45 evals, 38 feasible; max throughput seen 171 MSPS; best accuracy 11.83 bits; best feasible luts_plus_ffs=938; feasible ranges: data_width 14..18, n_iter 12..14, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *The current front is dominated by pipelined_m designs with n_iter=13. To improve hypervolume, we need to: (1) explore lower n_iter (12) in pipelined_m to potentially find cheaper designs, and (2) explore higher accuracy designs in pipelined (n_iter 13-15) to extend the front towards higher accuracy_bits. The iterative and unrolled_k families are infeasible due to throughput constraints (max 15.3 and 13.5 MSPS respectively, well below the 2 MSPS requirement when considering the bursty system constraints), so they should be excluded. The sys_p99_latency constraint is met by all feasible designs (best seen 0.066 us << 0.4 us), so it is not a binding constraint for the feasible region.*)
- `pipelined_m` (50 evals): data_width=15..17, n_iter=12..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m dominates the area objective (938 vs 1433 for pipelined) and meets throughput/latency constraints comfortably. The current front is clustered at n_iter=13; exploring n_iter=12 may reduce area further while maintaining accuracy > 10 bits. data_width 15-17 covers the trade-off between area and accuracy.
- `pipelined` (50 evals): data_width=15..18, n_iter=13..15, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined provides higher accuracy (up to 12.45 bits) at higher area. Exploring n_iter=13-15 and data_width 15-18 helps map the accuracy-area trade-off on the high-accuracy end of the front, which is needed for hypervolume coverage.

**Result (code):** 100 evaluations this round, 200 total; 148 feasible; hypervolume 5777 (+30.0%).

**LLM decision:** `refine` — The Pareto front is dominated by `pipelined_m` designs, which are significantly more area-efficient (841-1157 LUTs+FFs) than `pipelined` (1358-1955 LUTs+FFs) while maintaining high throughput (97-124 MSPS) and meeting the strict p99 latency constraint (best seen 0.066 us). `iterative` and `unrolled_k` are infeasible due to low throughput. The current front covers accuracy bits 10.3 to 13.3, but the selection rule minimizes area, so the low-area end (841) is the primary target. To improve hypervolume and ensure the best area/accuracy trade-off is found, we should focus the search on the `pipelined_m` family in the region where it dominates: data_width 15-17, n_iter 12-14, m 3-4. This narrows the search space to find potentially better area/accuracy points than the current front, specifically looking for designs with area < 841 or higher accuracy at similar area.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 5777 (gain this round: +30.0%).
Feasible designs: 148 of 200 evaluations (111 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 273
- max_abs_err <= 0.000976562: 16% violate; best seen 0.000102 (2^-13.26)
- sys_p99_latency_us <= 0.4: 20% violate; best seen 0.066

Pareto front (feasible, 15 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=841, accuracy_bits=10.3, luts=643, ffs=198, throughput_msps=97.8, max_abs_err=0.000811 (2^-10.27), power_index=0.0632
- pipelined_m [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=round m=3] luts_plus_ffs=885, accuracy_bits=10.5, luts=631, ffs=254, throughput_msps=124, max_abs_err=0.000712 (2^-10.46), power_index=0.0666
- pipelined_m [data_width=15 n_iter=13 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=938, accuracy_bits=10.5, luts=688, ffs=250, throughput_msps=97.8, max_abs_err=0.000689 (2^-10.50), power_index=0.0706
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=976, accuracy_bits=11.3, luts=713, ffs=262, throughput_msps=97.8, max_abs_err=0.00041 (2^-11.25), power_index=0.0734
- pipelined_m [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=999, accuracy_bits=11.3, luts=745, ffs=254, throughput_msps=97.8, max_abs_err=0.0004 (2^-11.29), power_index=0.0752
- pipelined_m [data_width=18 n_iter=13 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1046, accuracy_bits=11.6, luts=764, ffs=282, throughput_msps=97.8, max_abs_err=0.000316 (2^-11.63), power_index=0.0787
- pipelined_m [data_width=18 n_iter=13 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1080, accuracy_bits=11.8, luts=789, ffs=291, throughput_msps=93.6, max_abs_err=0.000277 (2^-11.82), power_index=0.0812
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1137, accuracy_bits=12.3, luts=861, ffs=276, throughput_msps=97.8, max_abs_err=0.000204 (2^-12.26), power_index=0.0856
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1157, accuracy_bits=12.5, luts=868, ffs=289, throughput_msps=93.6, max_abs_err=0.000178 (2^-12.46), power_index=0.087
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=1955, accuracy_bits=13.3, luts=964, ffs=991, throughput_msps=264, max_abs_err=0.000102 (2^-13.26), power_index=0.147
Front coverage: luts_plus_ffs 841..1955 (HV reference 3000); accuracy_bits 10.3..13.3 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 12.26 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 12.58 bits
- pipelined: 65 evals, 60 feasible; max throughput seen 273 MSPS; best accuracy 13.26 bits; best feasible luts_plus_ffs=1358; feasible ranges: data_width 14..18, n_iter 13..15, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 95 evals, 88 feasible; max throughput seen 171 MSPS; best accuracy 12.51 bits; best feasible luts_plus_ffs=841; feasible ranges: data_width 14..18, n_iter 12..14, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Refine the search to the dominant family and its most promising parameter sub-space to maximize hypervolume gain in the remaining budget.*)
- `pipelined_m` (40 evals): data_width=15..17, n_iter=12..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=3..4. *Why:* pipelined_m dominates the front in area efficiency. Focusing on the core parameter ranges (data_width 15-17, n_iter 12-14, m 3-4) where feasible designs cluster will allow Optuna to refine the Pareto front, potentially finding designs with lower area or higher accuracy than the current best (841 LUTs+FFs, 10.3 bits).

**Result (code):** 40 evaluations this round, 240 total; 186 feasible; hypervolume 5809 (+0.6%).

**LLM decision:** `stop` — The Pareto front is well-established and the selection rule (min luts_plus_ffs) is satisfied by a robust design. The best feasible design is `pipelined_m` with `luts_plus_ffs=813`, `accuracy_bits=10.2` (max_abs_err=0.000835), and `sys_p99_latency_us` well within the 0.4us bound (best seen 0.066us). The front covers the trade-off space effectively from 813 to 1955 LUTs+FFs and 10.2 to 13.3 accuracy bits. Since this is the final round and the hypervolume gain has plateaued (+0.6% in the last round), further exploration would yield diminishing returns. The `pipelined_m` family dominates the low-area end of the front, which is critical for the selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 5809 (gain this round: +0.6%).
Feasible designs: 186 of 240 evaluations (138 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 273
- max_abs_err <= 0.000976562: 14% violate; best seen 0.000102 (2^-13.26)
- sys_p99_latency_us <= 0.4: 17% violate; best seen 0.066

Pareto front (feasible, 16 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=813, accuracy_bits=10.2, luts=620, ffs=194, throughput_msps=97.8, max_abs_err=0.000835 (2^-10.23), power_index=0.0612
- pipelined_m [data_width=15 n_iter=12 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=853, accuracy_bits=10.3, luts=654, ffs=199, throughput_msps=97.8, max_abs_err=0.000772 (2^-10.34), power_index=0.0642
- pipelined_m [data_width=16 n_iter=12 angle_guard=0 frac_guard=0 rounding=round m=3] luts_plus_ffs=885, accuracy_bits=10.5, luts=631, ffs=254, throughput_msps=124, max_abs_err=0.000712 (2^-10.46), power_index=0.0666
- pipelined_m [data_width=16 n_iter=13 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=959, accuracy_bits=11.2, luts=701, ffs=258, throughput_msps=97.8, max_abs_err=0.000417 (2^-11.23), power_index=0.0721
- pipelined_m [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=999, accuracy_bits=11.3, luts=745, ffs=254, throughput_msps=97.8, max_abs_err=0.0004 (2^-11.29), power_index=0.0752
- pipelined_m [data_width=17 n_iter=13 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1028, accuracy_bits=11.6, luts=751, ffs=276, throughput_msps=93.6, max_abs_err=0.000312 (2^-11.65), power_index=0.0773
- pipelined_m [data_width=18 n_iter=13 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1080, accuracy_bits=11.8, luts=789, ffs=291, throughput_msps=93.6, max_abs_err=0.000277 (2^-11.82), power_index=0.0812
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1137, accuracy_bits=12.3, luts=861, ffs=276, throughput_msps=97.8, max_abs_err=0.000204 (2^-12.26), power_index=0.0856
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1157, accuracy_bits=12.5, luts=868, ffs=289, throughput_msps=93.6, max_abs_err=0.000178 (2^-12.46), power_index=0.087
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=1955, accuracy_bits=13.3, luts=964, ffs=991, throughput_msps=264, max_abs_err=0.000102 (2^-13.26), power_index=0.147
Front coverage: luts_plus_ffs 813..1955 (HV reference 3000); accuracy_bits 10.2..13.3 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 12.26 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 12.58 bits
- pipelined: 65 evals, 60 feasible; max throughput seen 273 MSPS; best accuracy 13.26 bits; best feasible luts_plus_ffs=1358; feasible ranges: data_width 14..18, n_iter 13..15, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 135 evals, 126 feasible; max throughput seen 171 MSPS; best accuracy 12.51 bits; best feasible luts_plus_ffs=813; feasible ranges: data_width 14..18, n_iter 12..14, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (150 evals): data_width=14..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (15 front designs; box front_anchored)
- `pipelined` (10 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 335 feasible; hypervolume 1.491e+04 (+156.6%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and the selection rule (min luts_plus_ffs) is satisfied by a robust design. The best feasible design is `pipelined_m` with `luts_plus_ffs=813`, `accuracy_bits=10.2` (max_abs_err=0.000835), and `sys_p99_latency_us` well within the 0.4us bound (best seen 0.066us). The front covers the trade-off space effectively from 813 to 1955 LUTs+FFs and 10.2 to 13.3 accuracy bits. Since this is the final round and the hypervolume gain has plateaued (+0.6% in the last round), further exploration would yield diminishing returns. The `pipelined_m` family dominates the low-area end of the front, which is critical for the selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.491e+04 (gain this round: +156.6%).
Feasible designs: 335 of 400 evaluations (283 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 273
- max_abs_err <= 0.000976562: 11% violate; best seen 1.54e-07 (2^-22.63)
- sys_p99_latency_us <= 0.4: 10% violate; best seen 0.066

Pareto front (feasible, 39 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=813, accuracy_bits=10.2, luts=620, ffs=194, throughput_msps=97.8, max_abs_err=0.000835 (2^-10.23), power_index=0.0612
- pipelined_m [data_width=17 n_iter=12 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=905, accuracy_bits=10.8, luts=689, ffs=216, throughput_msps=93.6, max_abs_err=0.000556 (2^-10.81), power_index=0.0681
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=976, accuracy_bits=11.3, luts=713, ffs=262, throughput_msps=97.8, max_abs_err=0.00041 (2^-11.25), power_index=0.0734
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1102, accuracy_bits=11.9, luts=827, ffs=274, throughput_msps=97.8, max_abs_err=0.00027 (2^-11.85), power_index=0.0829
- pipelined_m [data_width=19 n_iter=15 angle_guard=-1 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1180, accuracy_bits=13, luts=1008, ffs=172, throughput_msps=50.3, max_abs_err=0.000125 (2^-12.97), power_index=0.0888
- pipelined_m [data_width=21 n_iter=17 angle_guard=-1 frac_guard=1 rounding=round m=7] luts_plus_ffs=1487, accuracy_bits=14.9, luts=1230, ffs=257, throughput_msps=56.8, max_abs_err=3.38e-05 (2^-14.85), power_index=0.112
- pipelined_m [data_width=25 n_iter=18 angle_guard=1 frac_guard=0 rounding=trunc m=8] luts_plus_ffs=1776, accuracy_bits=16.9, luts=1474, ffs=302, throughput_msps=48, max_abs_err=8.31e-06 (2^-16.88), power_index=0.134
- pipelined_m [data_width=24 n_iter=22 angle_guard=3 frac_guard=0 rounding=round m=4] luts_plus_ffs=2343, accuracy_bits=19.2, luts=1798, ffs=545, throughput_msps=86, max_abs_err=1.62e-06 (2^-19.24), power_index=0.176
- pipelined_m [data_width=28 n_iter=24 angle_guard=-1 frac_guard=1 rounding=round m=6] luts_plus_ffs=2698, accuracy_bits=21.6, luts=2270, ffs=428, throughput_msps=59.9, max_abs_err=3.19e-07 (2^-21.58), power_index=0.203
- pipelined_m [data_width=27 n_iter=24 angle_guard=3 frac_guard=3 rounding=round m=5] luts_plus_ffs=2929, accuracy_bits=22.6, luts=2389, ffs=540, throughput_msps=70.6, max_abs_err=1.54e-07 (2^-22.63), power_index=0.22
Front coverage: luts_plus_ffs 813..2929 (HV reference 3000); accuracy_bits 10.2..22.6 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 12.26 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 12.58 bits
- pipelined: 75 evals, 70 feasible; max throughput seen 273 MSPS; best accuracy 17.96 bits; best feasible luts_plus_ffs=1358; feasible ranges: data_width 14..25, n_iter 13..30, angle_guard 0..4, frac_guard 0..2
- pipelined_m: 285 evals, 265 feasible; max throughput seen 171 MSPS; best accuracy 22.63 bits; best feasible luts_plus_ffs=813; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 29972 in, 4528 out
- provider-reported cost: $0.0073
- full prompts and replies: `llm_trace.jsonl`

