# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: anthropic/claude-sonnet-5.5.  
**Evaluations:** 300 of 300 budgeted, over 3 round(s).  
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
  budget: 300 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=15,n_iter=14,angle_guard=3,frac_guard=3,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 859 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 272 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 61.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.36 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000215 (2^-12.18) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 1.76 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 6.43e-05 (2^-13.93) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 0.526 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 12.2 | exact: bit-accurate model, exhaustive (32768 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 94.8 dBc, SNR 80.9 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=15,n_iter=14,angle_guard=3,frac_guard=3,rounding=round,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=5` | 0.4342 → 0.4465 | no |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=3` | 0.3103 → 0.3186 | yes |
| `pipelined_m:data_width=19,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=3` | 0.3103 → 0.3186 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=3` | 0.3103 → 0.3186 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (25 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=14,angle_guard=3,frac_guard=3,rounding=round,m=4` | 859 | 272 | 97.8 | 6 | 1.36 | 0.000215 (2^-12.18) | 12.18 |
| 1 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=5` | 926 | 219 | 80.6 | 5 | 1.38 | 0.000158 (2^-12.63) | 12.63 |
| 2 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=3` | 876 | 337 | 119.3 | 7 | 1.46 | 0.000148 (2^-12.72) | 12.72 |
| 3 | `pipelined_m:data_width=19,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=3` | 882 | 366 | 119.3 | 7 | 1.5 | 0.000145 (2^-12.76) | 12.76 |
| 4 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=3` | 935 | 353 | 119.3 | 7 | 1.55 | 0.000143 (2^-12.77) | 12.77 |
| 5 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=3` | 941 | 347 | 119.3 | 7 | 1.55 | 0.00013 (2^-12.91) | 12.91 |
| 6 | `pipelined_m:data_width=17,n_iter=15,angle_guard=3,frac_guard=1,rounding=round,m=3` | 956 | 352 | 119.3 | 7 | 1.57 | 0.000124 (2^-12.98) | 12.98 |
| 7 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1017 | 305 | 93.6 | 6 | 1.59 | 8.26e-05 (2^-13.56) | 13.56 |
| 8 | `pipelined_m:data_width=18,n_iter=16,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1102 | 309 | 93.6 | 6 | 1.7 | 5.17e-05 (2^-14.24) | 14.24 |
| 9 | `pipelined_m:data_width=19,n_iter=18,angle_guard=1,frac_guard=0,rounding=round,m=4` | 1152 | 366 | 93.6 | 7 | 1.83 | 4.26e-05 (2^-14.52) | 14.52 |
| 10 | `pipelined_m:data_width=21,n_iter=18,angle_guard=0,frac_guard=0,rounding=round,m=3` | 1241 | 466 | 119.3 | 8 | 2.06 | 2.12e-05 (2^-15.53) | 15.53 |
| 11 | `pipelined_m:data_width=21,n_iter=20,angle_guard=0,frac_guard=0,rounding=round,m=4` | 1387 | 395 | 93.6 | 7 | 2.15 | 1.79e-05 (2^-15.77) | 15.77 |
| 12 | `pipelined_m:data_width=25,n_iter=18,angle_guard=-1,frac_guard=0,rounding=trunc,m=4` | 1438 | 459 | 89.6 | 7 | 2.28 | 9.2e-06 (2^-16.73) | 16.73 |
| 13 | `pipelined_m:data_width=25,n_iter=18,angle_guard=1,frac_guard=0,rounding=trunc,m=3` | 1474 | 553 | 114.5 | 8 | 2.44 | 8.31e-06 (2^-16.88) | 16.88 |
| 14 | `pipelined_m:data_width=22,n_iter=20,angle_guard=1,frac_guard=2,rounding=trunc,m=3` | 1547 | 591 | 114.5 | 9 | 2.57 | 5.54e-06 (2^-17.46) | 17.46 |
| 15 | `pipelined_m:data_width=25,n_iter=20,angle_guard=-1,frac_guard=2,rounding=trunc,m=4` | 1687 | 475 | 86.0 | 7 | 2.6 | 3.39e-06 (2^-18.17) | 18.17 |
| 16 | `pipelined_m:data_width=25,n_iter=20,angle_guard=0,frac_guard=0,rounding=trunc,m=3` | 1627 | 630 | 114.5 | 9 | 2.72 | 2.92e-06 (2^-18.39) | 18.39 |
| 17 | `pipelined_m:data_width=25,n_iter=20,angle_guard=2,frac_guard=1,rounding=trunc,m=3` | 1707 | 656 | 110.0 | 9 | 2.84 | 2.35e-06 (2^-18.70) | 18.70 |
| 18 | `pipelined_m:data_width=27,n_iter=20,angle_guard=-1,frac_guard=2,rounding=round,m=4` | 1864 | 512 | 86.0 | 7 | 2.86 | 2.3e-06 (2^-18.73) | 18.73 |
| 19 | `pipelined_m:data_width=27,n_iter=20,angle_guard=2,frac_guard=2,rounding=round,m=3` | 1924 | 716 | 110.0 | 9 | 3.18 | 1.94e-06 (2^-18.97) | 18.97 |
| 20 | `pipelined_m:data_width=24,n_iter=26,angle_guard=4,frac_guard=0,rounding=round,m=3` | 2165 | 802 | 110.0 | 11 | 3.57 | 1.62e-06 (2^-19.24) | 19.24 |
| 21 | `pipelined_m:data_width=27,n_iter=26,angle_guard=0,frac_guard=0,rounding=trunc,m=3` | 2297 | 854 | 110.0 | 11 | 3.79 | 4.33e-07 (2^-21.14) | 21.14 |
| 22 | `pipelined_m:data_width=27,n_iter=26,angle_guard=1,frac_guard=0,rounding=round,m=3` | 2324 | 863 | 110.0 | 11 | 3.84 | 2.33e-07 (2^-22.03) | 22.03 |
| 23 | `pipelined_m:data_width=26,n_iter=26,angle_guard=4,frac_guard=2,rounding=round,m=3` | 2484 | 895 | 110.0 | 11 | 4.07 | 1.39e-07 (2^-22.78) | 22.78 |
| 24 | `pipelined_m:data_width=27,n_iter=30,angle_guard=3,frac_guard=2,rounding=trunc,m=3` | 2878 | 1009 | 110.0 | 12 | 4.68 | 1.14e-07 (2^-23.06) | 23.06 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The 32 requests arrive together and must all finish within 0.44 us. That needs about 1 result per cycle at a fast clock, or very low latency, so pipelined and pipelined_m are the main candidates. Plain iterative is excluded because it takes N+3 cycles per result and cannot meet 32 MSps. Unrolled_k is included as a lower-weight probe for area. Accuracy must reach 12 bits, so data_width and n_iter are bounded near that floor, with some headroom to map the accuracy/area trade-off. Later rounds should refine around whichever family dominates.*)
- `pipelined` (38 evals): data_width=12..18, n_iter=10..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* One result per cycle meets throughput of 32 MSps and batch timing if Fmax is high enough. Narrow width and iteration ranges target the 2^-12 error floor to minimise LUTs+FFs.
- `pipelined_m` (37 evals): data_width=12..18, n_iter=10..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, m=2..4. *Why:* Registering every m stages cuts FFs while still giving 1 result per cycle. Lower area may be possible if Fmax stays adequate and latency fits the 0.44 us batch window.
- `unrolled_k` (25 evals): data_width=12..18, n_iter=10..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, k=4..8. *Why:* A high k gives multiple micro-rotations per cycle with a shared FSM and smaller area than a full pipeline. It may still meet 32 MSps and the batch deadline only if the cycles per result stay very low, so this is a riskier probe.

**Result (code):** 100 evaluations this round, 100 total; 34 feasible; hypervolume 5156 (n/a).

**LLM decision:** `refine` — Pipelined_m holds 6 of the 7 front points, and the cheapest feasible design (1131 LUTs+FFs, 12.2 bits). Pipelined holds the last point (2182, 14 bits) and its best feasible area is 1796, so it is dominated at the low-area end. Unrolled_k had 0 feasible designs out of 25 and topped out at 12 MSPS against the 32 MSPS requirement, so it is dropped. Iterative would be slower still (N+3 cycles per result), so I am not exploring it. Feasible designs sit in data_width 15..18 and n_iter 14..16, with m up to 4. The error limit of 2^-12 is only just met at the cheap end (12.2 bits), so the next gain is likely from slightly smaller widths and iteration counts. I will also test m 5..6, which could cut FFs while keeping throughput well above 32 MSPS (m=4 reaches about 94 MSPS).

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 300.
Hypervolume of the feasible front: 5156 (gain this round: n/a (first round)).
Feasible designs: 34 of 100 evaluations (24 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 25% violate; best seen 282
- max_abs_err <= 0.000244141: 64% violate; best seen 5.94e-05 (2^-14.04)
- sys_p99_batch_us <= 0.44: 25% violate; best seen 0.149

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1131, accuracy_bits=12.2, luts=859, ffs=272, throughput_msps=97.8, max_abs_err=0.000215 (2^-12.18), power_index=1.36
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=1278, accuracy_bits=12.4, luts=909, ffs=368, throughput_msps=119, max_abs_err=0.000185 (2^-12.40), power_index=1.54
- pipelined_m [data_width=18 n_iter=14 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1303, accuracy_bits=12.9, luts=988, ffs=315, throughput_msps=93.6, max_abs_err=0.000134 (2^-12.86), power_index=1.57
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round m=3] luts_plus_ffs=1359, accuracy_bits=13, luts=954, ffs=406, throughput_msps=124, max_abs_err=0.000121 (2^-13.02), power_index=1.64
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=3 rounding=round m=4] luts_plus_ffs=1389, accuracy_bits=13.2, luts=1086, ffs=303, throughput_msps=93.6, max_abs_err=0.000105 (2^-13.22), power_index=1.67
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=3 rounding=round m=3] luts_plus_ffs=1546, accuracy_bits=13.8, luts=1102, ffs=444, throughput_msps=119, max_abs_err=7.04e-05 (2^-13.79), power_index=1.86
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=2182, accuracy_bits=14, luts=1080, ffs=1102, throughput_msps=264, max_abs_err=5.94e-05 (2^-14.04), power_index=2.63
Front coverage: luts_plus_ffs 1131..2182 (HV reference 4000); accuracy_bits 12.2..14 (HV reference 12); data_width on the front 15..18 (registry 8..28).

Per family:
- unrolled_k: 25 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 12.77 bits
- pipelined: 38 evals, 17 feasible; max throughput seen 282 MSPS; best accuracy 14.04 bits; best feasible luts_plus_ffs=1796; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 37 evals, 17 feasible; max throughput seen 178 MSPS; best accuracy 13.79 bits; best feasible luts_plus_ffs=1131; feasible ranges: data_width 15..18, n_iter 14..16, angle_guard 0..3, frac_guard 0..3, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate the budget on pipelined_m near the feasible region and extend m and the lower width and iteration bounds to find cheaper designs.*)
- `pipelined_m` (64 evals): data_width=13..18, n_iter=12..16, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, m=2..6. *Why:* This family produced the cheapest feasible designs and most of the front. Slightly smaller widths and iteration counts, and larger m, may lower area while still meeting 2^-12 error.
- `pipelined` (16 evals): data_width=14..18, n_iter=13..16, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* It anchors the high-accuracy, high-throughput end of the front (14 bits at 264 MSPS), so a small share keeps that end covered.

**Result (code):** 80 evaluations this round, 180 total; 62 feasible; hypervolume 6069 (+17.7%).

**LLM decision:** `stop` — This is the final round, so stop. The front has 8 feasible designs, all pipelined_m, with luts_plus_ffs from 1131 to 1411 and accuracy_bits from 12.2 to 14.2. The cheapest design (data_width=15, n_iter=14, m=4) has max_abs_err 0.000215, which meets the 2^-12 bound, and throughput 97.8 MSPS, against the 32 MSPS requirement. The latest round gained +17.7% hypervolume, but the budget is nearly used. unrolled_k had 0 feasible designs in 25 evals, with throughput at most 12 MSPS. The plain pipelined family's best feasible area was 1780, well above 1131. The selection rule (min luts_plus_ffs) picks the 1131 design. The sys_p99_batch_us bound has margin, with the best value seen at 0.149 against 0.44.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 120 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 180 of 300.
Hypervolume of the feasible front: 6069 (gain this round: +17.7%).
Feasible designs: 62 of 180 evaluations (47 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 14% violate; best seen 282
- max_abs_err <= 0.000244141: 61% violate; best seen 5.17e-05 (2^-14.24)
- sys_p99_batch_us <= 0.44: 23% violate; best seen 0.149

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1131, accuracy_bits=12.2, luts=859, ffs=272, throughput_msps=97.8, max_abs_err=0.000215 (2^-12.18), power_index=1.36
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=5] luts_plus_ffs=1145, accuracy_bits=12.6, luts=926, ffs=219, throughput_msps=80.6, max_abs_err=0.000158 (2^-12.63), power_index=1.38
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1213, accuracy_bits=12.7, luts=876, ffs=337, throughput_msps=119, max_abs_err=0.000148 (2^-12.72), power_index=1.46
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=1288, accuracy_bits=12.8, luts=935, ffs=353, throughput_msps=119, max_abs_err=0.000143 (2^-12.77), power_index=1.55
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=1288, accuracy_bits=12.9, luts=941, ffs=347, throughput_msps=119, max_abs_err=0.00013 (2^-12.91), power_index=1.55
- pipelined_m [data_width=17 n_iter=15 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=1308, accuracy_bits=13, luts=956, ffs=352, throughput_msps=119, max_abs_err=0.000124 (2^-12.98), power_index=1.57
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1322, accuracy_bits=13.6, luts=1017, ffs=305, throughput_msps=93.6, max_abs_err=8.26e-05 (2^-13.56), power_index=1.59
- pipelined_m [data_width=18 n_iter=16 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1411, accuracy_bits=14.2, luts=1102, ffs=309, throughput_msps=93.6, max_abs_err=5.17e-05 (2^-14.24), power_index=1.7
Front coverage: luts_plus_ffs 1131..1411 (HV reference 4000); accuracy_bits 12.2..14.2 (HV reference 12); data_width on the front 15..18 (registry 8..28).

Per family:
- unrolled_k: 25 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 12.77 bits
- pipelined: 54 evals, 25 feasible; max throughput seen 282 MSPS; best accuracy 14.04 bits; best feasible luts_plus_ffs=1780; feasible ranges: data_width 15..18, n_iter 14..16, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 101 evals, 37 feasible; max throughput seen 178 MSPS; best accuracy 14.24 bits; best feasible luts_plus_ffs=1131; feasible ranges: data_width 15..18, n_iter 14..16, angle_guard 0..3, frac_guard 0..3, m 2..5
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 120 evaluations*)
- `pipelined_m` (120 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (8 front designs; box front_anchored)

**Result (code):** 120 evaluations this round, 300 total; 134 feasible; hypervolume 1.869e+04 (+208.0%).

**No LLM call** (code's front-mapping round): This is the final round, so stop. The front has 8 feasible designs, all pipelined_m, with luts_plus_ffs from 1131 to 1411 and accuracy_bits from 12.2 to 14.2. The cheapest design (data_width=15, n_iter=14, m=4) has max_abs_err 0.000215, which meets the 2^-12 bound, and throughput 97.8 MSPS, against the 32 MSPS requirement. The latest round gained +17.7% hypervolume, but the budget is nearly used. unrolled_k had 0 feasible designs in 25 evals, with throughput at most 12 MSPS. The plain pipelined family's best feasible area was 1780, well above 1131. The selection rule (min luts_plus_ffs) picks the 1131 design. The sys_p99_batch_us bound has margin, with the best value seen at 0.149 against 0.44.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 300.
Hypervolume of the feasible front: 1.869e+04 (gain this round: +208.0%).
Feasible designs: 134 of 300 evaluations (112 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 8% violate; best seen 282
- max_abs_err <= 0.000244141: 42% violate; best seen 1.14e-07 (2^-23.06)
- sys_p99_batch_us <= 0.44: 28% violate; best seen 0.149

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1131, accuracy_bits=12.2, luts=859, ffs=272, throughput_msps=97.8, max_abs_err=0.000215 (2^-12.18), power_index=1.36
- pipelined_m [data_width=19 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=3] luts_plus_ffs=1248, accuracy_bits=12.8, luts=882, ffs=366, throughput_msps=119, max_abs_err=0.000145 (2^-12.76), power_index=1.5
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=1288, accuracy_bits=12.9, luts=941, ffs=347, throughput_msps=119, max_abs_err=0.00013 (2^-12.91), power_index=1.55
- pipelined_m [data_width=18 n_iter=16 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1411, accuracy_bits=14.2, luts=1102, ffs=309, throughput_msps=93.6, max_abs_err=5.17e-05 (2^-14.24), power_index=1.7
- pipelined_m [data_width=21 n_iter=20 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1782, accuracy_bits=15.8, luts=1387, ffs=395, throughput_msps=93.6, max_abs_err=1.79e-05 (2^-15.77), power_index=2.15
- pipelined_m [data_width=25 n_iter=18 angle_guard=1 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=2027, accuracy_bits=16.9, luts=1474, ffs=553, throughput_msps=114, max_abs_err=8.31e-06 (2^-16.88), power_index=2.44
- pipelined_m [data_width=25 n_iter=20 angle_guard=0 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=2257, accuracy_bits=18.4, luts=1627, ffs=630, throughput_msps=114, max_abs_err=2.92e-06 (2^-18.39), power_index=2.72
- pipelined_m [data_width=27 n_iter=20 angle_guard=2 frac_guard=2 rounding=round m=3] luts_plus_ffs=2640, accuracy_bits=19, luts=1924, ffs=716, throughput_msps=110, max_abs_err=1.94e-06 (2^-18.97), power_index=3.18
- pipelined_m [data_width=27 n_iter=26 angle_guard=0 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=3151, accuracy_bits=21.1, luts=2297, ffs=854, throughput_msps=110, max_abs_err=4.33e-07 (2^-21.14), power_index=3.79
- pipelined_m [data_width=27 n_iter=30 angle_guard=3 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=3887, accuracy_bits=23.1, luts=2878, ffs=1009, throughput_msps=110, max_abs_err=1.14e-07 (2^-23.06), power_index=4.68
Front coverage: luts_plus_ffs 1131..3887 (HV reference 4000); accuracy_bits 12.2..23.1 (HV reference 12); data_width on the front 15..27 (registry 8..28).

Per family:
- unrolled_k: 25 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 12.77 bits
- pipelined: 54 evals, 25 feasible; max throughput seen 282 MSPS; best accuracy 14.04 bits; best feasible luts_plus_ffs=1780; feasible ranges: data_width 15..18, n_iter 14..16, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 221 evals, 109 feasible; max throughput seen 178 MSPS; best accuracy 23.06 bits; best feasible luts_plus_ffs=1131; feasible ranges: data_width 15..27, n_iter 13..30, angle_guard -2..4, frac_guard 0..4, m 2..5
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 29084 in, 2887 out
- provider-reported cost: $0.0870
- full prompts and replies: `llm_trace.jsonl`

