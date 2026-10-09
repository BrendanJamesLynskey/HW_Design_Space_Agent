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
`pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 841 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 287 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.36 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000175 (2^-12.48) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 11.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.28e-05 (2^-14.21) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.46 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 5 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 95.0 dBc, SNR 82.4 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=5` | 0.4342 → 0.4465 | no |
| `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=0,rounding=round,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |

**WINNER CHANGED AT L2**: the L1 selection pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=5 fails the simulated system constraints (sys_p99_batch_us <= 0.44 by 1.5%); the best shortlisted design that passes is pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=4.

## Pareto front (25 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=5` | 827 | 221 | 80.6 | 5 | 1.26 | 0.0002 (2^-12.28) | 12.28 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=4` | 841 | 287 | 93.6 | 6 | 1.36 | 0.000175 (2^-12.48) | 12.48 |
| 2 | `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=0,rounding=round,m=4` | 890 | 282 | 97.8 | 6 | 1.41 | 0.000145 (2^-12.75) | 12.75 |
| 3 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=4` | 905 | 287 | 93.6 | 6 | 1.43 | 0.000119 (2^-13.04) | 13.04 |
| 4 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=4` | 920 | 291 | 93.6 | 6 | 1.46 | 0.000109 (2^-13.17) | 13.17 |
| 5 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=4` | 969 | 287 | 93.6 | 6 | 1.51 | 0.000108 (2^-13.18) | 13.18 |
| 6 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 964 | 299 | 93.6 | 6 | 1.52 | 0.000102 (2^-13.26) | 13.26 |
| 7 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 979 | 303 | 93.6 | 6 | 1.54 | 9.49e-05 (2^-13.36) | 13.36 |
| 8 | `pipelined_m:data_width=20,n_iter=15,angle_guard=-1,frac_guard=1,rounding=trunc,m=4` | 994 | 313 | 93.6 | 6 | 1.57 | 9.32e-05 (2^-13.39) | 13.39 |
| 9 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1017 | 305 | 93.6 | 6 | 1.59 | 8.26e-05 (2^-13.56) | 13.56 |
| 10 | `pipelined_m:data_width=23,n_iter=15,angle_guard=-1,frac_guard=1,rounding=trunc,m=4` | 1126 | 355 | 89.6 | 6 | 1.78 | 6.44e-05 (2^-13.92) | 13.92 |
| 11 | `pipelined_m:data_width=20,n_iter=19,angle_guard=4,frac_guard=0,rounding=round,m=4` | 1333 | 399 | 89.6 | 7 | 2.08 | 2.17e-05 (2^-15.49) | 15.49 |
| 12 | `pipelined_m:data_width=23,n_iter=17,angle_guard=0,frac_guard=2,rounding=trunc,m=3` | 1337 | 527 | 114.5 | 8 | 2.24 | 1.73e-05 (2^-15.82) | 15.82 |
| 13 | `pipelined_m:data_width=21,n_iter=20,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 1467 | 414 | 89.6 | 7 | 2.26 | 1.31e-05 (2^-16.21) | 16.21 |
| 14 | `pipelined_m:data_width=21,n_iter=20,angle_guard=3,frac_guard=0,rounding=round,m=3` | 1447 | 558 | 114.5 | 9 | 2.41 | 1.15e-05 (2^-16.41) | 16.41 |
| 15 | `pipelined_m:data_width=22,n_iter=19,angle_guard=2,frac_guard=4,rounding=round,m=4` | 1607 | 457 | 89.6 | 7 | 2.48 | 5.47e-06 (2^-17.48) | 17.48 |
| 16 | `pipelined_m:data_width=27,n_iter=19,angle_guard=-2,frac_guard=0,rounding=round,m=4` | 1618 | 488 | 86.0 | 7 | 2.53 | 4.26e-06 (2^-17.84) | 17.84 |
| 17 | `pipelined_m:data_width=25,n_iter=20,angle_guard=0,frac_guard=2,rounding=trunc,m=4` | 1707 | 480 | 86.0 | 7 | 2.63 | 2.57e-06 (2^-18.57) | 18.57 |
| 18 | `pipelined_m:data_width=25,n_iter=20,angle_guard=0,frac_guard=2,rounding=round,m=4` | 1760 | 482 | 86.0 | 7 | 2.7 | 2.56e-06 (2^-18.57) | 18.57 |
| 19 | `pipelined_m:data_width=28,n_iter=20,angle_guard=-1,frac_guard=2,rounding=trunc,m=4` | 1867 | 527 | 86.0 | 7 | 2.88 | 2.04e-06 (2^-18.91) | 18.91 |
| 20 | `pipelined_m:data_width=28,n_iter=20,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1927 | 542 | 86.0 | 7 | 2.97 | 1.93e-06 (2^-18.99) | 18.99 |
| 21 | `pipelined_m:data_width=27,n_iter=22,angle_guard=2,frac_guard=4,rounding=round,m=3` | 2209 | 839 | 105.9 | 10 | 3.67 | 5.26e-07 (2^-20.86) | 20.86 |
| 22 | `pipelined_m:data_width=28,n_iter=23,angle_guard=3,frac_guard=4,rounding=trunc,m=3` | 2347 | 872 | 105.9 | 10 | 3.87 | 2.59e-07 (2^-21.88) | 21.88 |
| 23 | `pipelined_m:data_width=25,n_iter=26,angle_guard=3,frac_guard=4,rounding=trunc,m=2` | 2429 | 1262 | 152.6 | 15 | 4.44 | 2.56e-07 (2^-21.90) | 21.90 |
| 24 | `pipelined_m:data_width=28,n_iter=28,angle_guard=3,frac_guard=4,rounding=trunc,m=3` | 2879 | 1078 | 105.9 | 12 | 4.76 | 3.75e-08 (2^-24.67) | 24.67 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The key constraint is sys_p99_batch_us <= 0.44us for a 32-request burst. iterative and unrolled_k produce one result every several cycles, so a 32-request burst would take 32*(N+3) or 32*ceil(N/k) cycles, which at any reasonable Fmax far exceeds 440ns. Only pipelined/pipelined_m produce 1 result/cycle, allowing the 32 requests to be processed in ~32+latency cycles. pipelined_m with m=4-8 gives latency of 3-4 cycles (for N=12-16), which at 200+ MHz is ~15-20ns, leaving ample margin for the 32-cycle throughput window. The batch p99 is dominated by the time to push all 32 requests through the pipeline (32 cycles) plus the pipeline latency, which at 200 MHz is ~160+20=180ns, well under 440ns. Accuracy requires max_abs_err <= 2^-12, so accuracy_bits >= 12. For CORDIC, N=12-16 iterations with data_width=14-18 and appropriate guards should achieve this. I focus the entire budget on pipelined_m since it is the only family that can meet the system latency constraint while offering the best area trade-off. The ranges are narrowed to focus the search: data_width 14-18 (enough for 12-bit accuracy with margin), n_iter 12-16 (enough for 12-bit accuracy), angle_guard 0-2 and frac_guard 0-2 (small guards to minimise area), m 4-8 (balance pipeline depth vs area). Rounding is explored as both options since it affects accuracy at the boundary.*)
- `pipelined_m` (100 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=4..8. *Why:* pipelined_m is the only family that can plausibly meet the 0.44us batch latency constraint while minimising area. With m=8, latency is ceil(N/8)+2 cycles. For N=12-16, latency is 3-4 cycles. At Fmax ~200-300 MHz, 4 cycles = 13-20ns, well under 440ns. The 32-request burst is handled by the pipeline accepting one request per cycle, so all 32 are in-flight within 32 cycles, and results stream out at 1/cycle. The batch p99 latency is dominated by the pipeline latency + queueing, which should be well within 0.44us. Area is minimised by keeping N and data_width low while meeting accuracy_bits >= 12. m=4-8 balances pipeline depth (area) against latency.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 10 feasible; hypervolume 3829 (n/a).

**LLM decision:** `add_family` — Round 1 established a feasible front for pipelined_m with best area 1048 and accuracy up to 13.4 bits. The sys_p99_batch_us constraint is tight (79% violation rate in general, but feasible designs exist). To maximize hypervolume and find the true minimum area, we must compare pipelined_m against the fully pipelined family. Pipelined_m saves area by sharing registers, but pipelined might allow higher Fmax or different trade-offs. We narrow the ranges to the promising region found in Round 1 (data_width 16-18, n_iter 14-16) to focus the 100 evals on the relevant trade-off space rather than exploring infeasible low-accuracy or low-throughput corners.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 3829 (gain this round: n/a (first round)).
Feasible designs: 10 of 100 evaluations (9 unique).
Families explored so far: pipelined_m. Not yet explored: iterative, unrolled_k, pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 97.8
- max_abs_err <= 0.000244141: 35% violate; best seen 6.45e-05 (2^-13.92)
- sys_p99_batch_us <= 0.44: 79% violate; best seen 0.358

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=5] luts_plus_ffs=1048, accuracy_bits=12.3, luts=827, ffs=221, throughput_msps=80.6, max_abs_err=0.0002 (2^-12.28), power_index=1.26
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=5] luts_plus_ffs=1139, accuracy_bits=12.5, luts=924, ffs=215, throughput_msps=80.6, max_abs_err=0.000176 (2^-12.48), power_index=1.37
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1192, accuracy_bits=13, luts=905, ffs=287, throughput_msps=93.6, max_abs_err=0.000119 (2^-13.04), power_index=1.43
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1210, accuracy_bits=13.2, luts=920, ffs=291, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=1.46
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1263, accuracy_bits=13.3, luts=964, ffs=299, throughput_msps=93.6, max_abs_err=0.000102 (2^-13.26), power_index=1.52
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1303, accuracy_bits=13.4, luts=1002, ffs=301, throughput_msps=93.6, max_abs_err=9.56e-05 (2^-13.35), power_index=1.57
Front coverage: luts_plus_ffs 1048..1303 (HV reference 4000); accuracy_bits 12.3..13.4 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined_m: 100 evals, 10 feasible; max throughput seen 97.8 MSPS; best accuracy 13.92 bits; best feasible luts_plus_ffs=1048; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2, m 4..5
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 1 established a feasible front for pipelined_m with best area 1048 and accuracy up to 13.4 bits. The sys_p99_batch_us constraint is tight (79% violation rate in general, but feasible designs exist). To maximize hypervolume and find the true minimum area, we must compare pipelined_m against the fully pipelined family. Pipelined_m saves area by sharing registers, but pipelined might allow higher Fmax or different trade-offs. We narrow the ranges to the promising region found in Round 1 (data_width 16-18, n_iter 14-16) to focus the 100 evals on the relevant trade-off space rather than exploring infeasible low-accuracy or low-throughput corners.*)
- `pipelined_m` (50 evals): data_width=16..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=4..5. *Why:* Refine the current best family around the known Pareto region (data_width 16-18, n_iter 14-16, m 4-5) to squeeze out lower area designs that still meet the strict 0.44us batch latency and 32 MSPS throughput.
- `pipelined` (50 evals): data_width=16..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Explore the fully pipelined family. It has 1 result/cycle throughput (easiest to meet 32 MSPS and burst latency) but typically higher area due to full pipeline registers. Comparing it against pipelined_m (which registers every m stages) is critical to see if the area saving from m>1 outweighs the potential Fmax/latency benefits of full pipelining, or if pipelined_m is strictly better for area.

**Result (code):** 100 evaluations this round, 200 total; 79 feasible; hypervolume 4403 (+15.0%).

**LLM decision:** `add_family` — The current front is dominated by `pipelined_m` designs with `luts_plus_ffs` starting at 1048. However, the `iterative` and `unrolled_k` families have not been explored. Given the objective to minimize `luts_plus_ffs`, `iterative` (shared datapath, 1 micro-rotation/cycle) is typically the most area-efficient architecture, often significantly cheaper than pipelined variants, provided the throughput constraint is met. The throughput constraint is `>= 32 MSPS`. An `iterative` CORDIC with N=14 iterations takes 17 cycles. To achieve 32 MSPS, the clock frequency must be at least 32 * 17 = 544 MHz. This is likely infeasible on Artix-7 for a 18-bit datapath. However, `unrolled_k` with k=2 or k=4 reduces the cycle count. For example, `unrolled_k` with k=4 and N=14 takes ceil(14/4)+3 = 7 cycles. Required Fmax = 32 * 7 = 224 MHz. This is a very reasonable frequency for Artix-7, and the area cost of unrolling k=4 is likely lower than the full pipeline registers of `pipelined_m` (which has 221-305 FFs). The `pipelined_m` front shows a minimum of 1048 LUTs+FFs. It is highly probable that an `unrolled_k` design with k=4 or k=8, or even a high-frequency `iterative` design if Fmax allows, could offer a lower area cost while meeting the 32 MSPS throughput and 0.44us batch latency constraints. The batch latency constraint (0.44us) is tight. For `pipelined_m`, the latency is low (N/m + 2 cycles). For `unrolled_k`, latency is ceil(N/k)+3 cycles. If Fmax is ~200-300 MHz, 7 cycles is ~23-35 ns, well within 440 ns. The main risk is Fmax, but the cost model will handle that. Exploring `unrolled_k` is the highest-value next step to potentially break the 1048 area floor.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 4403 (gain this round: +15.0%).
Feasible designs: 79 of 200 evaluations (54 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 30% violate; best seen 6.45e-05 (2^-13.92)
- sys_p99_batch_us <= 0.44: 43% violate; best seen 0.169

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=5] luts_plus_ffs=1048, accuracy_bits=12.3, luts=827, ffs=221, throughput_msps=80.6, max_abs_err=0.0002 (2^-12.28), power_index=1.26
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1127, accuracy_bits=12.5, luts=841, ffs=287, throughput_msps=93.6, max_abs_err=0.000175 (2^-12.48), power_index=1.36
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1173, accuracy_bits=12.8, luts=890, ffs=282, throughput_msps=97.8, max_abs_err=0.000145 (2^-12.75), power_index=1.41
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1192, accuracy_bits=13, luts=905, ffs=287, throughput_msps=93.6, max_abs_err=0.000119 (2^-13.04), power_index=1.43
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1210, accuracy_bits=13.2, luts=920, ffs=291, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=1.46
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=1.51
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1263, accuracy_bits=13.3, luts=964, ffs=299, throughput_msps=93.6, max_abs_err=0.000102 (2^-13.26), power_index=1.52
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1282, accuracy_bits=13.4, luts=979, ffs=303, throughput_msps=93.6, max_abs_err=9.49e-05 (2^-13.36), power_index=1.54
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1322, accuracy_bits=13.6, luts=1017, ffs=305, throughput_msps=93.6, max_abs_err=8.26e-05 (2^-13.56), power_index=1.59
Front coverage: luts_plus_ffs 1048..1322 (HV reference 4000); accuracy_bits 12.3..13.6 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- pipelined: 50 evals, 35 feasible; max throughput seen 273 MSPS; best accuracy 13.39 bits; best feasible luts_plus_ffs=1665; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 150 evals, 44 feasible; max throughput seen 97.8 MSPS; best accuracy 13.92 bits; best feasible luts_plus_ffs=1048; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2, m 4..5
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The current front is dominated by `pipelined_m` designs with `luts_plus_ffs` starting at 1048. However, the `iterative` and `unrolled_k` families have not been explored. Given the objective to minimize `luts_plus_ffs`, `iterative` (shared datapath, 1 micro-rotation/cycle) is typically the most area-efficient architecture, often significantly cheaper than pipelined variants, provided the throughput constraint is met. The throughput constraint is `>= 32 MSPS`. An `iterative` CORDIC with N=14 iterations takes 17 cycles. To achieve 32 MSPS, the clock frequency must be at least 32 * 17 = 544 MHz. This is likely infeasible on Artix-7 for a 18-bit datapath. However, `unrolled_k` with k=2 or k=4 reduces the cycle count. For example, `unrolled_k` with k=4 and N=14 takes ceil(14/4)+3 = 7 cycles. Required Fmax = 32 * 7 = 224 MHz. This is a very reasonable frequency for Artix-7, and the area cost of unrolling k=4 is likely lower than the full pipeline registers of `pipelined_m` (which has 221-305 FFs). The `pipelined_m` front shows a minimum of 1048 LUTs+FFs. It is highly probable that an `unrolled_k` design with k=4 or k=8, or even a high-frequency `iterative` design if Fmax allows, could offer a lower area cost while meeting the 32 MSPS throughput and 0.44us batch latency constraints. The batch latency constraint (0.44us) is tight. For `pipelined_m`, the latency is low (N/m + 2 cycles). For `unrolled_k`, latency is ceil(N/k)+3 cycles. If Fmax is ~200-300 MHz, 7 cycles is ~23-35 ns, well within 440 ns. The main risk is Fmax, but the cost model will handle that. Exploring `unrolled_k` is the highest-value next step to potentially break the 1048 area floor.*)
- `unrolled_k` (40 evals): data_width=16..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..8. *Why:* Explore unrolled_k to find lower area designs that meet the 32 MSPS throughput constraint. k=4-8 are likely candidates to balance area and speed.

**Result (code):** 40 evaluations this round, 240 total; 79 feasible; hypervolume 4403 (+0.0%).

**LLM decision:** `stop` — The Pareto front is well-established and stable (0.0% hypervolume gain in Round 3). The `pipelined_m` family dominates the feasible space, achieving a minimum area of 1048 LUTs+FFs (well below the 4000 HV reference) while satisfying all constraints: throughput (80.6-97.8 MSPS >= 32), accuracy (12.3-13.6 bits >= 12.04 bits required for 2^-12 error), and system latency (best seen 0.169 us <= 0.44 us). The `pipelined` family is strictly dominated by `pipelined_m` in area (min 1665 vs 1048) for similar accuracy/throughput. `unrolled_k` is infeasible due to throughput limits (max 9.7 MSPS). Since this is the final round and the front covers the relevant trade-off space effectively with a clear selection candidate (the 1048 LUTs+FFs design), stopping is the correct action.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 4403 (gain this round: +0.0%).
Feasible designs: 79 of 240 evaluations (54 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 17% violate; best seen 273
- max_abs_err <= 0.000244141: 28% violate; best seen 6.45e-05 (2^-13.92)
- sys_p99_batch_us <= 0.44: 52% violate; best seen 0.169

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=5] luts_plus_ffs=1048, accuracy_bits=12.3, luts=827, ffs=221, throughput_msps=80.6, max_abs_err=0.0002 (2^-12.28), power_index=1.26
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1127, accuracy_bits=12.5, luts=841, ffs=287, throughput_msps=93.6, max_abs_err=0.000175 (2^-12.48), power_index=1.36
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1173, accuracy_bits=12.8, luts=890, ffs=282, throughput_msps=97.8, max_abs_err=0.000145 (2^-12.75), power_index=1.41
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1192, accuracy_bits=13, luts=905, ffs=287, throughput_msps=93.6, max_abs_err=0.000119 (2^-13.04), power_index=1.43
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1210, accuracy_bits=13.2, luts=920, ffs=291, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=1.46
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=1.51
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1263, accuracy_bits=13.3, luts=964, ffs=299, throughput_msps=93.6, max_abs_err=0.000102 (2^-13.26), power_index=1.52
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1282, accuracy_bits=13.4, luts=979, ffs=303, throughput_msps=93.6, max_abs_err=9.49e-05 (2^-13.36), power_index=1.54
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1322, accuracy_bits=13.6, luts=1017, ffs=305, throughput_msps=93.6, max_abs_err=8.26e-05 (2^-13.56), power_index=1.59
Front coverage: luts_plus_ffs 1048..1322 (HV reference 4000); accuracy_bits 12.3..13.6 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- unrolled_k: 40 evals, 0 feasible; max throughput seen 9.7 MSPS; best accuracy 13.83 bits
- pipelined: 50 evals, 35 feasible; max throughput seen 273 MSPS; best accuracy 13.39 bits; best feasible luts_plus_ffs=1665; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 150 evals, 44 feasible; max throughput seen 97.8 MSPS; best accuracy 13.92 bits; best feasible luts_plus_ffs=1048; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2, m 4..5
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (160 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (9 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 178 feasible; hypervolume 1.824e+04 (+314.4%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and stable (0.0% hypervolume gain in Round 3). The `pipelined_m` family dominates the feasible space, achieving a minimum area of 1048 LUTs+FFs (well below the 4000 HV reference) while satisfying all constraints: throughput (80.6-97.8 MSPS >= 32), accuracy (12.3-13.6 bits >= 12.04 bits required for 2^-12 error), and system latency (best seen 0.169 us <= 0.44 us). The `pipelined` family is strictly dominated by `pipelined_m` in area (min 1665 vs 1048) for similar accuracy/throughput. `unrolled_k` is infeasible due to throughput limits (max 9.7 MSPS). Since this is the final round and the front covers the relevant trade-off space effectively with a clear selection candidate (the 1048 LUTs+FFs design), stopping is the correct action.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.824e+04 (gain this round: +314.4%).
Feasible designs: 178 of 400 evaluations (149 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 10% violate; best seen 273
- max_abs_err <= 0.000244141: 22% violate; best seen 2.86e-08 (2^-25.06)
- sys_p99_batch_us <= 0.44: 43% violate; best seen 0.169

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=5] luts_plus_ffs=1048, accuracy_bits=12.3, luts=827, ffs=221, throughput_msps=80.6, max_abs_err=0.0002 (2^-12.28), power_index=1.26
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1192, accuracy_bits=13, luts=905, ffs=287, throughput_msps=93.6, max_abs_err=0.000119 (2^-13.04), power_index=1.43
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=1.51
- pipelined_m [data_width=20 n_iter=15 angle_guard=-1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1306, accuracy_bits=13.4, luts=994, ffs=313, throughput_msps=93.6, max_abs_err=9.32e-05 (2^-13.39), power_index=1.57
- pipelined_m [data_width=20 n_iter=19 angle_guard=4 frac_guard=0 rounding=round m=4] luts_plus_ffs=1732, accuracy_bits=15.5, luts=1333, ffs=399, throughput_msps=89.6, max_abs_err=2.17e-05 (2^-15.49), power_index=2.08
- pipelined_m [data_width=21 n_iter=20 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1880, accuracy_bits=16.2, luts=1467, ffs=414, throughput_msps=89.6, max_abs_err=1.31e-05 (2^-16.21), power_index=2.26
- pipelined_m [data_width=27 n_iter=19 angle_guard=-2 frac_guard=0 rounding=round m=4] luts_plus_ffs=2106, accuracy_bits=17.8, luts=1618, ffs=488, throughput_msps=86, max_abs_err=4.26e-06 (2^-17.84), power_index=2.53
- pipelined_m [data_width=28 n_iter=20 angle_guard=-1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=2394, accuracy_bits=18.9, luts=1867, ffs=527, throughput_msps=86, max_abs_err=2.04e-06 (2^-18.91), power_index=2.88
- pipelined_m [data_width=27 n_iter=22 angle_guard=2 frac_guard=4 rounding=round m=3] luts_plus_ffs=3048, accuracy_bits=20.9, luts=2209, ffs=839, throughput_msps=106, max_abs_err=5.26e-07 (2^-20.86), power_index=3.67
- pipelined_m [data_width=28 n_iter=28 angle_guard=3 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=3956, accuracy_bits=24.7, luts=2879, ffs=1078, throughput_msps=106, max_abs_err=3.75e-08 (2^-24.67), power_index=4.76
Front coverage: luts_plus_ffs 1048..3956 (HV reference 4000); accuracy_bits 12.3..24.7 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- unrolled_k: 40 evals, 0 feasible; max throughput seen 9.7 MSPS; best accuracy 13.83 bits
- pipelined: 50 evals, 35 feasible; max throughput seen 273 MSPS; best accuracy 13.39 bits; best feasible luts_plus_ffs=1665; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 310 evals, 143 feasible; max throughput seen 171 MSPS; best accuracy 25.06 bits; best feasible luts_plus_ffs=1048; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..5
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 26103 in, 4030 out
- provider-reported cost: $0.0091
- full prompts and replies: `llm_trace.jsonl`

