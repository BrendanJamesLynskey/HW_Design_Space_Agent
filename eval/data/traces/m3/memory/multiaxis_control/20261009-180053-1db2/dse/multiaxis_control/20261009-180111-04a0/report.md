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
`pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 861 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 276 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 61.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.37 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000204 (2^-12.26) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.34 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 5.69e-05 (2^-14.10) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 0.932 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.3 | exact: bit-accurate model, exhaustive (65536 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 94.9 dBc, SNR 81.9 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=1,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=16,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=4` | 0.3679 → 0.378 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (23 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=4` | 861 | 276 | 97.8 | 6 | 1.37 | 0.000204 (2^-12.26) | 12.26 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 896 | 299 | 93.6 | 6 | 1.44 | 0.000163 (2^-12.58) | 12.58 |
| 2 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=4` | 926 | 280 | 97.8 | 6 | 1.45 | 0.000158 (2^-12.63) | 12.63 |
| 3 | `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=1,rounding=round,m=4` | 958 | 291 | 93.6 | 6 | 1.5 | 0.00014 (2^-12.80) | 12.80 |
| 4 | `pipelined_m:data_width=16,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=4` | 987 | 276 | 97.8 | 6 | 1.52 | 0.000134 (2^-12.86) | 12.86 |
| 5 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=4` | 973 | 295 | 93.6 | 6 | 1.53 | 0.000101 (2^-13.27) | 13.27 |
| 6 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 979 | 303 | 93.6 | 6 | 1.54 | 9.49e-05 (2^-13.36) | 13.36 |
| 7 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 1017 | 297 | 93.6 | 6 | 1.58 | 8.82e-05 (2^-13.47) | 13.47 |
| 8 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1039 | 295 | 93.6 | 6 | 1.61 | 8.41e-05 (2^-13.54) | 13.54 |
| 9 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc,m=3` | 1033 | 432 | 119.3 | 8 | 1.76 | 8.08e-05 (2^-13.60) | 13.60 |
| 10 | `pipelined_m:data_width=18,n_iter=17,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1156 | 372 | 93.6 | 7 | 1.84 | 4.73e-05 (2^-14.37) | 14.37 |
| 11 | `pipelined_m:data_width=19,n_iter=17,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1169 | 387 | 93.6 | 7 | 1.87 | 3.81e-05 (2^-14.68) | 14.68 |
| 12 | `pipelined_m:data_width=19,n_iter=17,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1209 | 389 | 93.6 | 7 | 1.92 | 2.76e-05 (2^-15.14) | 15.14 |
| 13 | `pipelined_m:data_width=20,n_iter=18,angle_guard=2,frac_guard=1,rounding=trunc,m=3` | 1259 | 468 | 119.3 | 8 | 2.08 | 2.4e-05 (2^-15.35) | 15.35 |
| 14 | `pipelined_m:data_width=21,n_iter=21,angle_guard=3,frac_guard=0,rounding=round,m=4` | 1523 | 484 | 89.6 | 8 | 2.42 | 1.15e-05 (2^-16.41) | 16.41 |
| 15 | `pipelined_m:data_width=22,n_iter=21,angle_guard=2,frac_guard=0,rounding=round,m=4` | 1565 | 498 | 89.6 | 8 | 2.48 | 5.49e-06 (2^-17.47) | 17.47 |
| 16 | `pipelined_m:data_width=22,n_iter=21,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1632 | 504 | 89.6 | 8 | 2.57 | 4.62e-06 (2^-17.72) | 17.72 |
| 17 | `pipelined_m:data_width=22,n_iter=21,angle_guard=1,frac_guard=4,rounding=round,m=4` | 1759 | 535 | 89.6 | 8 | 2.76 | 3.73e-06 (2^-18.03) | 18.03 |
| 18 | `pipelined_m:data_width=24,n_iter=23,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 1906 | 549 | 89.6 | 8 | 2.96 | 1.76e-06 (2^-19.11) | 19.11 |
| 19 | `pipelined_m:data_width=24,n_iter=23,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1953 | 559 | 89.6 | 8 | 3.02 | 1.14e-06 (2^-19.74) | 19.74 |
| 20 | `pipelined_m:data_width=28,n_iter=23,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 2184 | 817 | 105.9 | 10 | 3.61 | 6.95e-07 (2^-20.46) | 20.46 |
| 21 | `pipelined_m:data_width=28,n_iter=25,angle_guard=1,frac_guard=0,rounding=trunc,m=2` | 2307 | 1263 | 152.6 | 15 | 4.3 | 2.55e-07 (2^-21.91) | 21.91 |
| 22 | `pipelined_m:data_width=27,n_iter=27,angle_guard=2,frac_guard=3,rounding=round,m=3` | 2665 | 922 | 110.0 | 11 | 4.32 | 9.01e-08 (2^-23.40) | 23.40 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires draining a 32-request burst within 0.44us, which is a tight latency constraint. The campaign notes suggest pipelined_m with m>=4 is the most promising family for this bursty workload. I allocate 50% of the budget to pipelined_m to thoroughly explore the m=4-8 range and find the optimal area/latency trade-off. Pipelined (m=1) gets 30% as a baseline to compare against, since it has the lowest per-stage latency but highest area. Unrolled_k gets 20% as a secondary option, since it has lower area than pipelined_m but higher latency per result. I exclude iterative because it is too slow for burst draining (1 micro-rotation/cycle means N+3 cycles/result, which is too many for 32 requests in 0.44us). The parameter ranges are focused on data_width 15-18, n_iter 12-15, and angle_guard 1-2 to meet the 2^-12 error constraint while keeping area low. Rounding is fixed to 'round' for better accuracy. frac_guard is limited to 0-1 to minimize area.*)
- `pipelined_m` (50 evals): data_width=15..18, n_iter=12..15, angle_guard=1..2, frac_guard=0..1, rounding=round, m=4..8. *Why:* Primary candidate. The 32-request burst must drain within 0.44us. With a 1us tick, the CORDIC has ~0.44us to process 32 items. A pipelined_m with m=4-8 allows 4-8 micro-rotations per cycle, drastically reducing the per-result latency compared to m=1 (pipelined). This is critical for meeting the tight p99 batch latency. The previous campaign note suggests m>=4 is likely needed. data_width 15-18 and n_iter 12-15 target the 2^-12 error constraint while keeping area low. angle_guard 1-2 and rounding=round are standard for this accuracy level.
- `pipelined` (30 evals): data_width=15..18, n_iter=12..15, angle_guard=1..2, frac_guard=0..1, rounding=round. *Why:* Baseline comparison. Pipelined (m=1) has the lowest latency per stage but the highest area (registers every stage). It may not meet the 0.44us burst constraint if Fmax is limited, but it's a necessary reference point for the Pareto front. If pipelined_m designs are too slow or have too much area, pipelined might be the only option that meets latency, or vice versa. This helps map the area vs. latency trade-off.
- `unrolled_k` (20 evals): data_width=15..18, n_iter=12..15, angle_guard=1..2, frac_guard=0..1, rounding=round, k=4..8. *Why:* Secondary candidate. Unrolled_k processes k micro-rotations per cycle with a shared FSM. It has lower area than pipelined_m (no pipeline registers between every m stages, just FSM state) but higher latency per result than pipelined_m. However, its throughput is 1 result every ceil(N/k) cycles. For N=12-15 and k=4-8, this is 2-4 cycles/result. If Fmax is high enough, this could drain 32 requests in 64-128 cycles. At 200MHz, that's 0.32-0.64us, which might be borderline for the 0.44us constraint. Worth exploring to see if it offers a better area/latency trade-off than pipelined_m.

**Result (code):** 100 evaluations this round, 100 total; 24 feasible; hypervolume 3758 (n/a).

**LLM decision:** `refine` — The pipelined_m family yielded the best area (1207 luts_plus_ffs) but only 4 feasible points in a tight range (m=4, n_iter=15, data_width 17-18). The pipelined family has higher area (1633+) but better throughput (264 MSPS). The sys_p99_batch_us constraint (<=0.44 us) is violated by 63% of evals, suggesting many designs are too slow for the burst. We need to explore pipelined_m more broadly to see if smaller m or different n_iter can improve area or accuracy while staying feasible, and check if pipelined can be pushed to lower area with tighter ranges. The iterative family is not yet explored but likely too slow for the throughput constraint.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 3758 (gain this round: n/a (first round)).
Feasible designs: 24 of 100 evaluations (13 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 20% violate; best seen 273
- max_abs_err <= 0.000244141: 30% violate; best seen 9.31e-05 (2^-13.39)
- sys_p99_batch_us <= 0.44: 63% violate; best seen 0.161

Pareto front (feasible, 3 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1207, accuracy_bits=12.6, luts=926, ffs=280, throughput_msps=97.8, max_abs_err=0.000158 (2^-12.63), power_index=1.45
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1267, accuracy_bits=13.3, luts=973, ffs=295, throughput_msps=93.6, max_abs_err=0.000101 (2^-13.27), power_index=1.53
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=1969, accuracy_bits=13.4, luts=987, ffs=982, throughput_msps=264, max_abs_err=9.31e-05 (2^-13.39), power_index=2.37
Front coverage: luts_plus_ffs 1207..1969 (HV reference 4000); accuracy_bits 12.6..13.4 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 13.04 bits
- pipelined: 30 evals, 20 feasible; max throughput seen 273 MSPS; best accuracy 13.39 bits; best feasible luts_plus_ffs=1633; feasible ranges: data_width 16..18, n_iter 14..15, angle_guard 1..2, frac_guard 0..1
- pipelined_m: 50 evals, 4 feasible; max throughput seen 97.8 MSPS; best accuracy 13.27 bits; best feasible luts_plus_ffs=1207; feasible ranges: data_width 17..18, n_iter 15..15, angle_guard 1..1, frac_guard 1..1, m 4..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Focus on pipelined_m (best area) with wider ranges to explore m=2..8 and n_iter=13..17, and pipelined with slightly wider ranges to check for improvements. Avoid iterative/unrolled_k as they are likely too slow for the throughput constraint.*)
- `pipelined_m` (60 evals): data_width=16..19, n_iter=13..17, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* Expand pipelined_m ranges to explore smaller m (higher throughput, potentially lower latency) and wider n_iter/data_width to find better area/accuracy trade-offs. The current front is very narrow (only m=4, n_iter=15), so widening may reveal cheaper or more accurate feasible points.
- `pipelined` (40 evals): data_width=15..18, n_iter=13..16, angle_guard=0..2, frac_guard=0..1, rounding=trunc|round. *Why:* Refine pipelined around its feasible region (data_width 16-18, n_iter 14-15) but slightly wider to check if lower area or higher accuracy is possible. Pipelined has higher throughput which may help with sys_p99_batch_us.

**Result (code):** 100 evaluations this round, 200 total; 69 feasible; hypervolume 8177 (+117.6%).

**LLM decision:** `refine` — The current front is dominated by pipelined_m (10/10 designs) with best area 1137 and best accuracy 15.14 bits. However, 40% of evaluations violated sys_p99_batch_us <= 0.44 us, suggesting the bursty 32-request pattern is challenging. pipelined offers higher throughput (273 MSPS vs 171 MSPS max for pipelined_m) which may help with system latency, but its best area is 1633. Refining both families in their proven feasible regions will densify the front and clarify the area-accuracy-system trade-off. unrolled_k is infeasible (max throughput 10.3 MSPS < 32 MSPS constraint) and iterative is likely similar (1 result every N+3 cycles), so they are not worth exploring. The front covers luts_plus_ffs 1137-1598 and accuracy 12.3-15.1 bits, which is a good spread, but the system constraint violation rate suggests we need to understand the system-level behavior better before stopping.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 8177 (gain this round: +117.6%).
Feasible designs: 69 of 200 evaluations (48 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 10% violate; best seen 273
- max_abs_err <= 0.000244141: 36% violate; best seen 2.76e-05 (2^-15.14)
- sys_p99_batch_us <= 0.44: 40% violate; best seen 0.161

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1137, accuracy_bits=12.3, luts=861, ffs=276, throughput_msps=97.8, max_abs_err=0.000204 (2^-12.26), power_index=1.37
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1207, accuracy_bits=12.6, luts=926, ffs=280, throughput_msps=97.8, max_abs_err=0.000158 (2^-12.63), power_index=1.45
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1252, accuracy_bits=12.8, luts=947, ffs=305, throughput_msps=93.6, max_abs_err=0.000144 (2^-12.76), power_index=1.51
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1264, accuracy_bits=12.9, luts=987, ffs=276, throughput_msps=97.8, max_abs_err=0.000134 (2^-12.86), power_index=1.52
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1267, accuracy_bits=13.3, luts=973, ffs=295, throughput_msps=93.6, max_abs_err=0.000101 (2^-13.27), power_index=1.53
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1282, accuracy_bits=13.4, luts=979, ffs=303, throughput_msps=93.6, max_abs_err=9.49e-05 (2^-13.36), power_index=1.54
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1334, accuracy_bits=13.5, luts=1039, ffs=295, throughput_msps=93.6, max_abs_err=8.41e-05 (2^-13.54), power_index=1.61
- pipelined_m [data_width=18 n_iter=17 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1528, accuracy_bits=14.4, luts=1156, ffs=372, throughput_msps=93.6, max_abs_err=4.73e-05 (2^-14.37), power_index=1.84
- pipelined_m [data_width=19 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1556, accuracy_bits=14.7, luts=1169, ffs=387, throughput_msps=93.6, max_abs_err=3.81e-05 (2^-14.68), power_index=1.87
- pipelined_m [data_width=19 n_iter=17 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1598, accuracy_bits=15.1, luts=1209, ffs=389, throughput_msps=93.6, max_abs_err=2.76e-05 (2^-15.14), power_index=1.92
Front coverage: luts_plus_ffs 1137..1598 (HV reference 4000); accuracy_bits 12.3..15.1 (HV reference 12); data_width on the front 16..19 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 13.04 bits
- pipelined: 70 evals, 27 feasible; max throughput seen 273 MSPS; best accuracy 13.54 bits; best feasible luts_plus_ffs=1633; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 1..2, frac_guard 0..1
- pipelined_m: 110 evals, 42 feasible; max throughput seen 171 MSPS; best accuracy 15.14 bits; best feasible luts_plus_ffs=1137; feasible ranges: data_width 16..19, n_iter 14..17, angle_guard 0..2, frac_guard 1..2, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The current front is dominated by pipelined_m (10/10 designs) with best area 1137 and best accuracy 15.14 bits. However, 40% of evaluations violated sys_p99_batch_us <= 0.44 us, suggesting the bursty 32-request pattern is challenging. pipelined offers higher throughput (273 MSPS vs 171 MSPS max for pipelined_m) which may help with system latency, but its best area is 1633. Refining both families in their proven feasible regions will densify the front and clarify the area-accuracy-system trade-off. unrolled_k is infeasible (max throughput 10.3 MSPS < 32 MSPS constraint) and iterative is likely similar (1 result every N+3 cycles), so they are not worth exploring. The front covers luts_plus_ffs 1137-1598 and accuracy 12.3-15.1 bits, which is a good spread, but the system constraint violation rate suggests we need to understand the system-level behavior better before stopping.*)
- `pipelined_m` (20 evals): data_width=16..18, n_iter=14..16, angle_guard=0..2, frac_guard=1..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m dominates the current front (10/10 designs) with the best area (1137) and best accuracy (15.14 bits). The feasible region is tightly clustered around data_width 16-18, n_iter 14-16, m 2-4. Refining here will densify the front in the high-value region near the selection rule (min luts_plus_ffs) and push accuracy higher without wasting budget on infeasible corners.
- `pipelined` (20 evals): data_width=16..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..1, rounding=trunc|round. *Why:* pipelined has higher throughput (up to 273 MSPS) which helps with the sys_p99_batch_us constraint (40% of evals violated it). Its best feasible area is 1633, which is worse than pipelined_m's 1137, but it may offer better system-level latency for the bursty 32-request pattern. Exploring its feasible range (data_width 16-18, n_iter 14-16) will clarify if it can beat pipelined_m on the system constraint while staying competitive on area.

**Result (code):** 40 evaluations this round, 240 total; 95 feasible; hypervolume 8188 (+0.1%).

**LLM decision:** `stop` — The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 1137 LUTs+FFs) meets all constraints: throughput 97.8 MSPS >= 32, max_abs_err 2.04e-04 <= 2.44e-04, and sys_p99_batch_us is bounded by the pipelined architecture's 1-result/cycle throughput which easily handles the 32-request burst within the 1us tick (latency ~14-16 cycles at >90MHz is <0.2us). The front covers the trade-off space from 1137 to 1598 area and 12.3 to 15.1 accuracy bits. Since this is the final round, we stop and select the minimum area design (1137) per the selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 8188 (gain this round: +0.1%).
Feasible designs: 95 of 240 evaluations (66 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 8% violate; best seen 273
- max_abs_err <= 0.000244141: 36% violate; best seen 2.76e-05 (2^-15.14)
- sys_p99_batch_us <= 0.44: 33% violate; best seen 0.161

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1137, accuracy_bits=12.3, luts=861, ffs=276, throughput_msps=97.8, max_abs_err=0.000204 (2^-12.26), power_index=1.37
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1194, accuracy_bits=12.6, luts=896, ffs=299, throughput_msps=93.6, max_abs_err=0.000163 (2^-12.58), power_index=1.44
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=1248, accuracy_bits=12.8, luts=958, ffs=291, throughput_msps=93.6, max_abs_err=0.00014 (2^-12.80), power_index=1.5
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1264, accuracy_bits=12.9, luts=987, ffs=276, throughput_msps=97.8, max_abs_err=0.000134 (2^-12.86), power_index=1.52
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1267, accuracy_bits=13.3, luts=973, ffs=295, throughput_msps=93.6, max_abs_err=0.000101 (2^-13.27), power_index=1.53
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1313, accuracy_bits=13.5, luts=1017, ffs=297, throughput_msps=93.6, max_abs_err=8.82e-05 (2^-13.47), power_index=1.58
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1334, accuracy_bits=13.5, luts=1039, ffs=295, throughput_msps=93.6, max_abs_err=8.41e-05 (2^-13.54), power_index=1.61
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=1464, accuracy_bits=13.6, luts=1033, ffs=432, throughput_msps=119, max_abs_err=8.08e-05 (2^-13.60), power_index=1.76
- pipelined_m [data_width=19 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1556, accuracy_bits=14.7, luts=1169, ffs=387, throughput_msps=93.6, max_abs_err=3.81e-05 (2^-14.68), power_index=1.87
- pipelined_m [data_width=19 n_iter=17 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1598, accuracy_bits=15.1, luts=1209, ffs=389, throughput_msps=93.6, max_abs_err=2.76e-05 (2^-15.14), power_index=1.92
Front coverage: luts_plus_ffs 1137..1598 (HV reference 4000); accuracy_bits 12.3..15.1 (HV reference 12); data_width on the front 16..19 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 13.04 bits
- pipelined: 90 evals, 37 feasible; max throughput seen 273 MSPS; best accuracy 13.54 bits; best feasible luts_plus_ffs=1633; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..1
- pipelined_m: 130 evals, 58 feasible; max throughput seen 171 MSPS; best accuracy 15.14 bits; best feasible luts_plus_ffs=1137; feasible ranges: data_width 16..19, n_iter 14..17, angle_guard 0..2, frac_guard 1..2, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (160 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (13 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 192 feasible; hypervolume 1.838e+04 (+124.5%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 1137 LUTs+FFs) meets all constraints: throughput 97.8 MSPS >= 32, max_abs_err 2.04e-04 <= 2.44e-04, and sys_p99_batch_us is bounded by the pipelined architecture's 1-result/cycle throughput which easily handles the 32-request burst within the 1us tick (latency ~14-16 cycles at >90MHz is <0.2us). The front covers the trade-off space from 1137 to 1598 area and 12.3 to 15.1 accuracy bits. Since this is the final round, we stop and select the minimum area design (1137) per the selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.838e+04 (gain this round: +124.5%).
Feasible designs: 192 of 400 evaluations (155 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 5% violate; best seen 273
- max_abs_err <= 0.000244141: 26% violate; best seen 9.01e-08 (2^-23.40)
- sys_p99_batch_us <= 0.44: 33% violate; best seen 0.161

Pareto front (feasible, 23 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1137, accuracy_bits=12.3, luts=861, ffs=276, throughput_msps=97.8, max_abs_err=0.000204 (2^-12.26), power_index=1.37
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1207, accuracy_bits=12.6, luts=926, ffs=280, throughput_msps=97.8, max_abs_err=0.000158 (2^-12.63), power_index=1.45
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1267, accuracy_bits=13.3, luts=973, ffs=295, throughput_msps=93.6, max_abs_err=0.000101 (2^-13.27), power_index=1.53
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1313, accuracy_bits=13.5, luts=1017, ffs=297, throughput_msps=93.6, max_abs_err=8.82e-05 (2^-13.47), power_index=1.58
- pipelined_m [data_width=18 n_iter=17 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1528, accuracy_bits=14.4, luts=1156, ffs=372, throughput_msps=93.6, max_abs_err=4.73e-05 (2^-14.37), power_index=1.84
- pipelined_m [data_width=19 n_iter=17 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1598, accuracy_bits=15.1, luts=1209, ffs=389, throughput_msps=93.6, max_abs_err=2.76e-05 (2^-15.14), power_index=1.92
- pipelined_m [data_width=22 n_iter=21 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=2063, accuracy_bits=17.5, luts=1565, ffs=498, throughput_msps=89.6, max_abs_err=5.49e-06 (2^-17.47), power_index=2.48
- pipelined_m [data_width=22 n_iter=21 angle_guard=1 frac_guard=4 rounding=round m=4] luts_plus_ffs=2293, accuracy_bits=18, luts=1759, ffs=535, throughput_msps=89.6, max_abs_err=3.73e-06 (2^-18.03), power_index=2.76
- pipelined_m [data_width=28 n_iter=23 angle_guard=-2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3002, accuracy_bits=20.5, luts=2184, ffs=817, throughput_msps=106, max_abs_err=6.95e-07 (2^-20.46), power_index=3.61
- pipelined_m [data_width=27 n_iter=27 angle_guard=2 frac_guard=3 rounding=round m=3] luts_plus_ffs=3587, accuracy_bits=23.4, luts=2665, ffs=922, throughput_msps=110, max_abs_err=9.01e-08 (2^-23.40), power_index=4.32
Front coverage: luts_plus_ffs 1137..3587 (HV reference 4000); accuracy_bits 12.3..23.4 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 13.04 bits
- pipelined: 90 evals, 37 feasible; max throughput seen 273 MSPS; best accuracy 13.54 bits; best feasible luts_plus_ffs=1633; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..1
- pipelined_m: 290 evals, 155 feasible; max throughput seen 171 MSPS; best accuracy 23.40 bits; best feasible luts_plus_ffs=1137; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 32969 in, 4556 out
- provider-reported cost: $0.0105
- full prompts and replies: `llm_trace.jsonl`

