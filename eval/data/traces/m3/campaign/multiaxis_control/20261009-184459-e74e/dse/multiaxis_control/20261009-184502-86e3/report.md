# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 400 of 400 budgeted, over 5 round(s).  
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
`pipelined_m:data_width=17,n_iter=15,angle_guard=0,frac_guard=2,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 905 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 280 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.43 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000217 (2^-12.17) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 7.1 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 4.62e-05 (2^-14.40) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.51 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.2 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 5 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 98.5 dBc, SNR 84.3 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc,m=5` | 0.4342 → 0.4465 | no |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=0,frac_guard=2,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=15,angle_guard=-1,frac_guard=2,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=19,n_iter=14,angle_guard=0,frac_guard=4,rounding=round,m=4` | 0.4016 → 0.4126 | yes |
| `pipelined_m:data_width=20,n_iter=14,angle_guard=1,frac_guard=2,rounding=round,m=4` | 0.3848 → 0.3953 | yes |

**WINNER CHANGED AT L2**: the L1 selection pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc,m=5 fails the simulated system constraints (sys_p99_batch_us <= 0.44 by 1.5%); the best shortlisted design that passes is pipelined_m:data_width=17,n_iter=15,angle_guard=0,frac_guard=2,rounding=trunc,m=4.

## Pareto front (24 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc,m=5` | 890 | 217 | 80.6 | 5 | 1.33 | 0.000219 (2^-12.16) | 12.16 |
| 1 | `pipelined_m:data_width=17,n_iter=15,angle_guard=0,frac_guard=2,rounding=trunc,m=4` | 905 | 280 | 93.6 | 6 | 1.43 | 0.000217 (2^-12.17) | 12.17 |
| 2 | `pipelined_m:data_width=18,n_iter=15,angle_guard=-1,frac_guard=2,rounding=trunc,m=4` | 935 | 291 | 93.6 | 6 | 1.47 | 0.00019 (2^-12.36) | 12.36 |
| 3 | `pipelined_m:data_width=19,n_iter=14,angle_guard=0,frac_guard=4,rounding=round,m=4` | 1018 | 323 | 89.6 | 6 | 1.61 | 0.000151 (2^-12.69) | 12.69 |
| 4 | `pipelined_m:data_width=20,n_iter=14,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1020 | 329 | 93.6 | 6 | 1.62 | 0.00013 (2^-12.91) | 12.91 |
| 5 | `pipelined_m:data_width=19,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc,m=3` | 979 | 374 | 119.3 | 7 | 1.63 | 9.41e-05 (2^-13.38) | 13.38 |
| 6 | `pipelined_m:data_width=18,n_iter=17,angle_guard=2,frac_guard=0,rounding=round,m=4` | 1051 | 354 | 93.6 | 7 | 1.69 | 7.75e-05 (2^-13.65) | 13.65 |
| 7 | `pipelined_m:data_width=20,n_iter=15,angle_guard=1,frac_guard=4,rounding=trunc,m=4` | 1112 | 339 | 89.6 | 6 | 1.75 | 7.07e-05 (2^-13.79) | 13.79 |
| 8 | `pipelined_m:data_width=19,n_iter=17,angle_guard=0,frac_guard=2,rounding=round,m=4` | 1175 | 379 | 93.6 | 7 | 1.87 | 5.66e-05 (2^-14.11) | 14.11 |
| 9 | `pipelined_m:data_width=20,n_iter=16,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 1128 | 474 | 114.5 | 8 | 1.93 | 4.27e-05 (2^-14.51) | 14.51 |
| 10 | `pipelined_m:data_width=19,n_iter=17,angle_guard=3,frac_guard=3,rounding=round,m=4` | 1259 | 403 | 93.6 | 7 | 2 | 2.41e-05 (2^-15.34) | 15.34 |
| 11 | `pipelined_m:data_width=21,n_iter=20,angle_guard=0,frac_guard=2,rounding=trunc,m=4` | 1467 | 412 | 89.6 | 7 | 2.26 | 1.49e-05 (2^-16.03) | 16.03 |
| 12 | `pipelined_m:data_width=21,n_iter=19,angle_guard=3,frac_guard=0,rounding=round,m=3` | 1371 | 558 | 114.5 | 9 | 2.32 | 1.21e-05 (2^-16.33) | 16.33 |
| 13 | `pipelined_m:data_width=24,n_iter=19,angle_guard=-2,frac_guard=1,rounding=round,m=4` | 1535 | 447 | 89.6 | 7 | 2.39 | 8.44e-06 (2^-16.86) | 16.86 |
| 14 | `pipelined_m:data_width=21,n_iter=21,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1609 | 494 | 89.6 | 8 | 2.53 | 7.67e-06 (2^-16.99) | 16.99 |
| 15 | `pipelined_m:data_width=24,n_iter=20,angle_guard=0,frac_guard=2,rounding=trunc,m=4` | 1647 | 463 | 89.6 | 7 | 2.54 | 3.57e-06 (2^-18.10) | 18.10 |
| 16 | `pipelined_m:data_width=24,n_iter=20,angle_guard=3,frac_guard=0,rounding=round,m=3` | 1627 | 628 | 110.0 | 9 | 2.71 | 2.8e-06 (2^-18.44) | 18.44 |
| 17 | `pipelined_m:data_width=27,n_iter=20,angle_guard=3,frac_guard=0,rounding=trunc,m=3` | 1807 | 697 | 110.0 | 9 | 3.01 | 2.08e-06 (2^-18.88) | 18.88 |
| 18 | `pipelined_m:data_width=27,n_iter=20,angle_guard=4,frac_guard=2,rounding=trunc,m=3` | 1907 | 728 | 105.9 | 9 | 3.17 | 1.95e-06 (2^-18.97) | 18.97 |
| 19 | `pipelined_m:data_width=28,n_iter=20,angle_guard=2,frac_guard=2,rounding=round,m=3` | 1986 | 740 | 110.0 | 9 | 3.28 | 1.92e-06 (2^-18.99) | 18.99 |
| 20 | `pipelined_m:data_width=24,n_iter=22,angle_guard=2,frac_guard=1,rounding=round,m=2` | 1870 | 970 | 158.3 | 13 | 3.42 | 1.32e-06 (2^-19.54) | 19.54 |
| 21 | `pipelined_m:data_width=28,n_iter=23,angle_guard=-1,frac_guard=0,rounding=round,m=3` | 2069 | 783 | 110.0 | 10 | 3.43 | 4.19e-07 (2^-21.19) | 21.19 |
| 22 | `pipelined_m:data_width=28,n_iter=23,angle_guard=0,frac_guard=0,rounding=trunc,m=3` | 2092 | 791 | 110.0 | 10 | 3.47 | 4.09e-07 (2^-21.22) | 21.22 |
| 23 | `pipelined_m:data_width=28,n_iter=23,angle_guard=1,frac_guard=0,rounding=trunc,m=3` | 2115 | 799 | 110.0 | 10 | 3.51 | 4.04e-07 (2^-21.24) | 21.24 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraints are the system burst (32 requests back within 0.44us) and 12-bit accuracy; throughput>=32 Msps is easy for anything that produces ~1 result/cycle. Accuracy depends only on data_width/n_iter/guards/rounding, so all families share the same accuracy knob ranges (W 12..20, N 10..22, guards -2..4 / 0..4, both roundings) — wide enough to bracket the ~14-16 bit W and ~13-16 iteration region where 12-bit error is met with margin. The real architectural question is area vs the burst bound: pipelined_m (1 result/cycle) clears the burst with large margin and is the safest L2 survivor, so it takes 60% of the budget across m=1..8 to map the area/latency trade. unrolled_k (shared datapath, low LUTs) gets 30% to test whether high k can make it both fast enough for the burst and accurate enough. iterative gets 10% purely to document that it cannot meet the burst bound. Round 1 is broad within these ranges; later rounds will narrow around the feasible front and spend the reserved budget mapping it over the full ranges of whichever families survive.*)
- `pipelined_m` (60 evals): data_width=12..20, n_iter=10..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Only family that trivially clears the 32-request burst: 1 result/cycle means a 32-request tick drains in ~32 cycles + pipeline latency, far inside the 0.44us p99 batch bound at any plausible Fmax, giving L2 margin. m=1..8 spans the whole area/latency trade: small m = deep pipelining (more FFs, lower latency), large m = fewer pipeline registers (lower LUTs+FFs, slightly higher latency). This is where the min-area / max-accuracy Pareto front will live, so it gets the largest share.
- `unrolled_k` (30 evals): data_width=12..20, n_iter=10..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=3..8. *Why:* Shared datapath means far fewer LUTs than a fully pipelined design, so if it can clear the burst bound it could dominate on luts_plus_ffs. The risk is that it serialises: a 32-request tick costs 32*(ceil(N/k)+3) cycles, so it only fits 0.44us if ceil(N/k) is small (high k, modest N) AND Fmax is high. k=3..8 probes that boundary; if the front shows it cannot meet both the batch bound and 12-bit accuracy, later rounds drop it.
- `iterative` (10 evals): data_width=12..20, n_iter=10..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Smallest area by construction, but it serialises one result every N+3 cycles, so 32 requests need 32*(N+3) cycles — impossible to fit 0.44us at any realistic Fmax. Included only with a small share to confirm infeasibility on the record (and to catch any surprise in the analytic sys bound) rather than to win the front.
- clamped by code: pipelined_m.m: clamped [1, 8] to [2, 8] (registry 2..8)

**Result (code):** 100 evaluations this round, 100 total; 27 feasible; hypervolume 8365 (n/a).

**LLM decision:** `add_family` — Only pipelined_m produced feasible designs (27/60); iterative and unrolled_k are throughput-infeasible by construction (max seen 15.3 and 10.7 MSPS vs the 32 MSPS floor, since their results/cycle is 1/(N+3) and 1/(ceil(N/k)+3)). The one family never tried, `pipelined`, is the only other 1-result/cycle architecture and can plausibly reach the throughput floor, so it must be mapped before the reserved front-mapping round. Also, the cheapest front point (1107 LUT+FF, throughput 80.6 MSPS) sits close to the L1 batch bound (32/80.6 ≈ 0.40 us plus ~5 cycles latency), so the L2 re-selection may drop it; I want higher-throughput pipelined_m points (small m) and pipelined points on the front as insurance. The cheap end is bounded by the accuracy constraint (data_width=17, n_iter=15 already gives only 12.16 bits), so I keep data_width near 15-22 rather than the full 8-28.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 8365 (gain this round: n/a (first round)).
Feasible designs: 27 of 100 evaluations (21 unique).
Families explored so far: iterative, unrolled_k, pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 40% violate; best seen 178
- max_abs_err <= 0.000244141: 41% violate; best seen 2.41e-05 (2^-15.34)
- sys_p99_batch_us <= 0.44: 60% violate; best seen 0.213

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=5] luts_plus_ffs=1107, accuracy_bits=12.2, luts=890, ffs=217, throughput_msps=80.6, max_abs_err=0.000219 (2^-12.16), power_index=1.33
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1353, accuracy_bits=13.4, luts=979, ffs=374, throughput_msps=119, max_abs_err=9.41e-05 (2^-13.38), power_index=1.63
- pipelined_m [data_width=18 n_iter=17 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1405, accuracy_bits=13.7, luts=1051, ffs=354, throughput_msps=93.6, max_abs_err=7.75e-05 (2^-13.65), power_index=1.69
- pipelined_m [data_width=19 n_iter=17 angle_guard=0 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=1625, accuracy_bits=14.1, luts=1169, ffs=456, throughput_msps=119, max_abs_err=5.66e-05 (2^-14.11), power_index=1.96
- pipelined_m [data_width=19 n_iter=17 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1662, accuracy_bits=15.3, luts=1259, ffs=403, throughput_msps=93.6, max_abs_err=2.41e-05 (2^-15.34), power_index=2
Front coverage: luts_plus_ffs 1107..1662 (HV reference 4000); accuracy_bits 12.2..15.3 (HV reference 12); data_width on the front 17..19 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 13.39 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 10.7 MSPS; best accuracy 15.01 bits
- pipelined_m: 60 evals, 27 feasible; max throughput seen 178 MSPS; best accuracy 15.34 bits; best feasible luts_plus_ffs=1107; feasible ranges: data_width 17..20, n_iter 14..22, angle_guard -1..3, frac_guard 0..4, m 2..5
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 2 spends the budget on the untried pipelined family plus a focused pipelined_m refinement, keeping the cheap end near the accuracy floor and pushing throughput up for the system batch constraint.*)
- `pipelined` (45 evals): data_width=15..22, n_iter=12..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Unexplored 1-result/cycle family; the only untried architecture that can clear the 32 MSPS floor, and full pipelining may give the highest Fmax for the batch-latency constraint.
- `pipelined_m` (55 evals): data_width=15..21, n_iter=12..24, angle_guard=-1..3, frac_guard=0..4, rounding=trunc|round, m=2..5. *Why:* Only feasible family so far; refine around its feasible box (data_width 17-20, n_iter 14-22, angle_guard -1..3, frac_guard 0-4, m 2-5) and probe slightly cheaper (data_width 15-16) and higher-throughput (small m) points to extend the front and add L2 margin.

**Result (code):** 100 evaluations this round, 200 total; 101 feasible; hypervolume 1.197e+04 (+43.0%).

**LLM decision:** `map_front` — The feasible front is entirely dominated by pipelined_m (12 of 12 shown designs, cheapest at 1107 LUT+FF) with a single pipelined point at the high-accuracy corner (3040 LUT+FF, 17.4 bits). Coverage is thin: luts_plus_ffs spans 1107..3040 against an HV reference of 4000, and accuracy_bits only reaches 17.4 while the registry allows data_width up to 28 — so the high-accuracy end of the trade-off curve is unmapped. iterative and unrolled_k are infeasible (0 feasible, max throughput 15.3 and 10.7 MSPS vs the 32 MSPS constraint), so the front lives on pipelined/pipelined_m only. With 200 of 400 evals left and a +43% HV gain this round, a code-driven NSGA-II coverage pass over the full ranges of pipelined and pipelined_m, seeded with the current front, is the best use of the remaining budget to fill the 3040..4000 area and the accuracy tail before final selection (min luts_plus_ffs).

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.197e+04 (gain this round: +43.0%).
Feasible designs: 101 of 200 evaluations (88 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 20% violate; best seen 273
- max_abs_err <= 0.000244141: 30% violate; best seen 5.85e-06 (2^-17.38)
- sys_p99_batch_us <= 0.44: 35% violate; best seen 0.166

Pareto front (feasible, 12 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=5] luts_plus_ffs=1107, accuracy_bits=12.2, luts=890, ffs=217, throughput_msps=80.6, max_abs_err=0.000219 (2^-12.16), power_index=1.33
- pipelined_m [data_width=17 n_iter=15 angle_guard=0 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1186, accuracy_bits=12.2, luts=905, ffs=280, throughput_msps=93.6, max_abs_err=0.000217 (2^-12.17), power_index=1.43
- pipelined_m [data_width=19 n_iter=14 angle_guard=0 frac_guard=4 rounding=round m=4] luts_plus_ffs=1341, accuracy_bits=12.7, luts=1018, ffs=323, throughput_msps=89.6, max_abs_err=0.000151 (2^-12.69), power_index=1.61
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1353, accuracy_bits=13.4, luts=979, ffs=374, throughput_msps=119, max_abs_err=9.41e-05 (2^-13.38), power_index=1.63
- pipelined_m [data_width=18 n_iter=17 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1405, accuracy_bits=13.7, luts=1051, ffs=354, throughput_msps=93.6, max_abs_err=7.75e-05 (2^-13.65), power_index=1.69
- pipelined_m [data_width=20 n_iter=15 angle_guard=1 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=1451, accuracy_bits=13.8, luts=1112, ffs=339, throughput_msps=89.6, max_abs_err=7.07e-05 (2^-13.79), power_index=1.75
- pipelined_m [data_width=19 n_iter=17 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1554, accuracy_bits=14.1, luts=1175, ffs=379, throughput_msps=93.6, max_abs_err=5.66e-05 (2^-14.11), power_index=1.87
- pipelined_m [data_width=20 n_iter=21 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=2026, accuracy_bits=15.9, luts=1544, ffs=482, throughput_msps=89.6, max_abs_err=1.68e-05 (2^-15.86), power_index=2.44
- pipelined_m [data_width=21 n_iter=21 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=2103, accuracy_bits=17, luts=1609, ffs=494, throughput_msps=89.6, max_abs_err=7.67e-06 (2^-16.99), power_index=2.53
- pipelined [data_width=22 n_iter=20 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=3040, accuracy_bits=17.4, luts=1507, ffs=1534, throughput_msps=257, max_abs_err=5.85e-06 (2^-17.38), power_index=3.66
Front coverage: luts_plus_ffs 1107..3040 (HV reference 4000); accuracy_bits 12.2..17.4 (HV reference 12); data_width on the front 17..22 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 13.39 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 10.7 MSPS; best accuracy 15.01 bits
- pipelined: 45 evals, 39 feasible; max throughput seen 273 MSPS; best accuracy 17.38 bits; best feasible luts_plus_ffs=1848; feasible ranges: data_width 18..22, n_iter 14..22, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 115 evals, 62 feasible; max throughput seen 178 MSPS; best accuracy 16.99 bits; best feasible luts_plus_ffs=1107; feasible ranges: data_width 16..21, n_iter 14..22, angle_guard -1..3, frac_guard 0..4, m 2..5
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (35 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (11 front designs; box front_anchored)
- `pipelined` (5 evals): data_width=21..28, n_iter=18..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 240 total; 125 feasible; hypervolume 1.647e+04 (+37.6%).

**LLM decision:** `map_front` — Round 3 left a feasible, still-improving front (HV 1.647e4, +37.6% this round) but it is thin (14 designs) and concentrated: every front point is pipelined_m, with pipelined only feasible at higher area (best 1848 vs 1107). iterative and unrolled_k are dead for this spec — 0 feasible in 10 and 30 evals, max throughput 15.3 and 10.7 MSPS against the 32 MSPS constraint — so they should not consume budget. The front spans luts_plus_ffs 1107..2914 against HV ref 4000 and accuracy 12.2..21.2 against ref 12; because the accuracy ref is 12 and the front already clears it everywhere, the HV is dominated by the high-accuracy end (the (4000 - area_max)*(acc_max - 12) term, ~1.0e4 of the 1.65e4 total). That means the biggest HV gains come from finding high-accuracy designs at lower area, not from the low-area corner alone. With this being the final round (4 of 4) and 160 evals still unused, the right move is to let code spend the reserved budget mapping the whole front over the full ranges of the two families that actually appear on it (pipelined_m, pipelined), seeded with the current front, rather than narrowing onto one corner. This both fills the area gap toward the 4000 ref and searches for cheaper high-accuracy points, while keeping the min-luts_plus_ffs selection corner (1107) in play.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 1.647e+04 (gain this round: +37.6%).
Feasible designs: 125 of 240 evaluations (106 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 17% violate; best seen 273
- max_abs_err <= 0.000244141: 26% violate; best seen 3.6e-07 (2^-21.40)
- sys_p99_batch_us <= 0.44: 35% violate; best seen 0.166

Pareto front (feasible, 14 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=5] luts_plus_ffs=1107, accuracy_bits=12.2, luts=890, ffs=217, throughput_msps=80.6, max_abs_err=0.000219 (2^-12.16), power_index=1.33
- pipelined_m [data_width=17 n_iter=15 angle_guard=0 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1186, accuracy_bits=12.2, luts=905, ffs=280, throughput_msps=93.6, max_abs_err=0.000217 (2^-12.17), power_index=1.43
- pipelined_m [data_width=20 n_iter=14 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1349, accuracy_bits=12.9, luts=1020, ffs=329, throughput_msps=93.6, max_abs_err=0.00013 (2^-12.91), power_index=1.62
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1353, accuracy_bits=13.4, luts=979, ffs=374, throughput_msps=119, max_abs_err=9.41e-05 (2^-13.38), power_index=1.63
- pipelined_m [data_width=20 n_iter=15 angle_guard=1 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=1451, accuracy_bits=13.8, luts=1112, ffs=339, throughput_msps=89.6, max_abs_err=7.07e-05 (2^-13.79), power_index=1.75
- pipelined_m [data_width=19 n_iter=17 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1554, accuracy_bits=14.1, luts=1175, ffs=379, throughput_msps=93.6, max_abs_err=5.66e-05 (2^-14.11), power_index=1.87
- pipelined_m [data_width=20 n_iter=21 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=2026, accuracy_bits=15.9, luts=1544, ffs=482, throughput_msps=89.6, max_abs_err=1.68e-05 (2^-15.86), power_index=2.44
- pipelined_m [data_width=21 n_iter=21 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=2103, accuracy_bits=17, luts=1609, ffs=494, throughput_msps=89.6, max_abs_err=7.67e-06 (2^-16.99), power_index=2.53
- pipelined_m [data_width=28 n_iter=23 angle_guard=0 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=2883, accuracy_bits=21.2, luts=2092, ffs=791, throughput_msps=110, max_abs_err=4.09e-07 (2^-21.22), power_index=3.47
- pipelined_m [data_width=28 n_iter=23 angle_guard=1 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=2914, accuracy_bits=21.2, luts=2115, ffs=799, throughput_msps=110, max_abs_err=4.04e-07 (2^-21.24), power_index=3.51
Front coverage: luts_plus_ffs 1107..2914 (HV reference 4000); accuracy_bits 12.2..21.2 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 13.39 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 10.7 MSPS; best accuracy 15.01 bits
- pipelined: 50 evals, 44 feasible; max throughput seen 273 MSPS; best accuracy 18.87 bits; best feasible luts_plus_ffs=1848; feasible ranges: data_width 18..25, n_iter 14..26, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 150 evals, 81 feasible; max throughput seen 178 MSPS; best accuracy 21.40 bits; best feasible luts_plus_ffs=1107; feasible ranges: data_width 16..28, n_iter 14..23, angle_guard -1..4, frac_guard 0..4, m 2..5
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (14 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 340 total; 184 feasible; hypervolume 1.793e+04 (+8.9%).

**LLM decision:** `stop` — Final round (4 of 4, 340/400 evals). The feasible front is well mapped: 23 Pareto designs spanning luts_plus_ffs 1107..2914 (HV ref 4000) and accuracy_bits 12.2..21.2 (HV ref 12), with hypervolume 1.793e+04 and only +8.9% gain this round. All three constraints are comfortably met by the front: throughput best 273 MSPS vs 32 required, max_abs_err best 2^-23.45 vs 2^-12 required, sys_p99_batch_us best 0.166 us vs 0.44 us required. pipelined_m dominates (140 feasible, cheapest at 1107 LUT+FF, best accuracy 23.45 bits); iterative and unrolled_k are infeasible on throughput (max 15.3 and 10.7 MSPS) and are correctly excluded. The selection rule (min luts_plus_ffs) picks the pipelined_m [W=17 N=15 ag=1 fg=1 trunc m=5] design at 1107 LUT+FF with 12.2 accuracy bits, which satisfies every constraint. No further exploration is warranted within the budget.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 60 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 340 of 400.
Hypervolume of the feasible front: 1.793e+04 (gain this round: +8.9%).
Feasible designs: 184 of 340 evaluations (161 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 12% violate; best seen 273
- max_abs_err <= 0.000244141: 22% violate; best seen 8.76e-08 (2^-23.45)
- sys_p99_batch_us <= 0.44: 34% violate; best seen 0.166

Pareto front (feasible, 23 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=5] luts_plus_ffs=1107, accuracy_bits=12.2, luts=890, ffs=217, throughput_msps=80.6, max_abs_err=0.000219 (2^-12.16), power_index=1.33
- pipelined_m [data_width=19 n_iter=14 angle_guard=0 frac_guard=4 rounding=round m=4] luts_plus_ffs=1341, accuracy_bits=12.7, luts=1018, ffs=323, throughput_msps=89.6, max_abs_err=0.000151 (2^-12.69), power_index=1.61
- pipelined_m [data_width=18 n_iter=17 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1405, accuracy_bits=13.7, luts=1051, ffs=354, throughput_msps=93.6, max_abs_err=7.75e-05 (2^-13.65), power_index=1.69
- pipelined_m [data_width=19 n_iter=17 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1554, accuracy_bits=14.1, luts=1175, ffs=379, throughput_msps=93.6, max_abs_err=5.66e-05 (2^-14.11), power_index=1.87
- pipelined_m [data_width=21 n_iter=20 angle_guard=0 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1878, accuracy_bits=16, luts=1467, ffs=412, throughput_msps=89.6, max_abs_err=1.49e-05 (2^-16.03), power_index=2.26
- pipelined_m [data_width=24 n_iter=19 angle_guard=-2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1982, accuracy_bits=16.9, luts=1535, ffs=447, throughput_msps=89.6, max_abs_err=8.44e-06 (2^-16.86), power_index=2.39
- pipelined_m [data_width=24 n_iter=20 angle_guard=3 frac_guard=0 rounding=round m=3] luts_plus_ffs=2255, accuracy_bits=18.4, luts=1627, ffs=628, throughput_msps=110, max_abs_err=2.8e-06 (2^-18.44), power_index=2.71
- pipelined_m [data_width=27 n_iter=20 angle_guard=4 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=2636, accuracy_bits=19, luts=1907, ffs=728, throughput_msps=106, max_abs_err=1.95e-06 (2^-18.97), power_index=3.17
- pipelined_m [data_width=28 n_iter=23 angle_guard=-1 frac_guard=0 rounding=round m=3] luts_plus_ffs=2851, accuracy_bits=21.2, luts=2069, ffs=783, throughput_msps=110, max_abs_err=4.19e-07 (2^-21.19), power_index=3.43
- pipelined_m [data_width=28 n_iter=23 angle_guard=1 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=2914, accuracy_bits=21.2, luts=2115, ffs=799, throughput_msps=110, max_abs_err=4.04e-07 (2^-21.24), power_index=3.51
Front coverage: luts_plus_ffs 1107..2914 (HV reference 4000); accuracy_bits 12.2..21.2 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 13.39 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 10.7 MSPS; best accuracy 15.01 bits
- pipelined: 50 evals, 44 feasible; max throughput seen 273 MSPS; best accuracy 18.87 bits; best feasible luts_plus_ffs=1848; feasible ranges: data_width 18..25, n_iter 14..26, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 250 evals, 140 feasible; max throughput seen 178 MSPS; best accuracy 23.45 bits; best feasible luts_plus_ffs=1107; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..5
```
</details>

### Round 5

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 60 evaluations*)
- `pipelined_m` (60 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (23 front designs; box front_anchored)

**Result (code):** 60 evaluations this round, 400 total; 214 feasible; hypervolume 1.795e+04 (+0.1%).

**No LLM call** (code's front-mapping round): Final round (4 of 4, 340/400 evals). The feasible front is well mapped: 23 Pareto designs spanning luts_plus_ffs 1107..2914 (HV ref 4000) and accuracy_bits 12.2..21.2 (HV ref 12), with hypervolume 1.793e+04 and only +8.9% gain this round. All three constraints are comfortably met by the front: throughput best 273 MSPS vs 32 required, max_abs_err best 2^-23.45 vs 2^-12 required, sys_p99_batch_us best 0.166 us vs 0.44 us required. pipelined_m dominates (140 feasible, cheapest at 1107 LUT+FF, best accuracy 23.45 bits); iterative and unrolled_k are infeasible on throughput (max 15.3 and 10.7 MSPS) and are correctly excluded. The selection rule (min luts_plus_ffs) picks the pipelined_m [W=17 N=15 ag=1 fg=1 trunc m=5] design at 1107 LUT+FF with 12.2 accuracy bits, which satisfies every constraint. No further exploration is warranted within the budget.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 5 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.795e+04 (gain this round: +0.1%).
Feasible designs: 214 of 400 evaluations (187 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 10% violate; best seen 273
- max_abs_err <= 0.000244141: 21% violate; best seen 8.76e-08 (2^-23.45)
- sys_p99_batch_us <= 0.44: 35% violate; best seen 0.166

Pareto front (feasible, 24 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=5] luts_plus_ffs=1107, accuracy_bits=12.2, luts=890, ffs=217, throughput_msps=80.6, max_abs_err=0.000219 (2^-12.16), power_index=1.33
- pipelined_m [data_width=19 n_iter=14 angle_guard=0 frac_guard=4 rounding=round m=4] luts_plus_ffs=1341, accuracy_bits=12.7, luts=1018, ffs=323, throughput_msps=89.6, max_abs_err=0.000151 (2^-12.69), power_index=1.61
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1353, accuracy_bits=13.4, luts=979, ffs=374, throughput_msps=119, max_abs_err=9.41e-05 (2^-13.38), power_index=1.63
- pipelined_m [data_width=19 n_iter=17 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1554, accuracy_bits=14.1, luts=1175, ffs=379, throughput_msps=93.6, max_abs_err=5.66e-05 (2^-14.11), power_index=1.87
- pipelined_m [data_width=19 n_iter=17 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1662, accuracy_bits=15.3, luts=1259, ffs=403, throughput_msps=93.6, max_abs_err=2.41e-05 (2^-15.34), power_index=2
- pipelined_m [data_width=24 n_iter=19 angle_guard=-2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1982, accuracy_bits=16.9, luts=1535, ffs=447, throughput_msps=89.6, max_abs_err=8.44e-06 (2^-16.86), power_index=2.39
- pipelined_m [data_width=24 n_iter=20 angle_guard=0 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=2110, accuracy_bits=18.1, luts=1647, ffs=463, throughput_msps=89.6, max_abs_err=3.57e-06 (2^-18.10), power_index=2.54
- pipelined_m [data_width=27 n_iter=20 angle_guard=4 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=2636, accuracy_bits=19, luts=1907, ffs=728, throughput_msps=106, max_abs_err=1.95e-06 (2^-18.97), power_index=3.17
- pipelined_m [data_width=24 n_iter=22 angle_guard=2 frac_guard=1 rounding=round m=2] luts_plus_ffs=2840, accuracy_bits=19.5, luts=1870, ffs=970, throughput_msps=158, max_abs_err=1.32e-06 (2^-19.54), power_index=3.42
- pipelined_m [data_width=28 n_iter=23 angle_guard=1 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=2914, accuracy_bits=21.2, luts=2115, ffs=799, throughput_msps=110, max_abs_err=4.04e-07 (2^-21.24), power_index=3.51
Front coverage: luts_plus_ffs 1107..2914 (HV reference 4000); accuracy_bits 12.2..21.2 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 13.39 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 10.7 MSPS; best accuracy 15.01 bits
- pipelined: 50 evals, 44 feasible; max throughput seen 273 MSPS; best accuracy 18.87 bits; best feasible luts_plus_ffs=1848; feasible ranges: data_width 18..25, n_iter 14..26, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 310 evals, 170 feasible; max throughput seen 178 MSPS; best accuracy 23.45 bits; best feasible luts_plus_ffs=1107; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..5
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 31847 in, 15421 out
- provider-reported cost: $0.0134
- full prompts and replies: `llm_trace.jsonl`

