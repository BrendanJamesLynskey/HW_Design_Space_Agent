# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 855 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 285 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.37 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000204 (2^-12.26) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 6.69 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.51e-05 (2^-14.15) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.81 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 94.9 dBc, SNR 82.2 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Every L1-feasible design (173) was simulated at its estimated Fmax (SimPy); 166 pass. Top 5 by the selection rule, L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=2,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=20,n_iter=15,angle_guard=-2,frac_guard=2,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=21,n_iter=15,angle_guard=-1,frac_guard=0,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (23 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 855 | 285 | 93.6 | 6 | 1.37 | 0.000204 (2^-12.26) | 12.26 |
| 1 | `pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 868 | 289 | 93.6 | 6 | 1.39 | 0.000178 (2^-12.46) | 12.46 |
| 2 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=2,rounding=round,m=4` | 890 | 287 | 93.6 | 6 | 1.42 | 0.000171 (2^-12.51) | 12.51 |
| 3 | `pipelined_m:data_width=20,n_iter=15,angle_guard=-2,frac_guard=2,rounding=trunc,m=4` | 1008 | 315 | 93.6 | 6 | 1.59 | 0.000121 (2^-13.02) | 13.02 |
| 4 | `pipelined_m:data_width=21,n_iter=15,angle_guard=-1,frac_guard=0,rounding=trunc,m=4` | 1008 | 321 | 93.6 | 6 | 1.6 | 8.04e-05 (2^-13.60) | 13.60 |
| 5 | `pipelined_m:data_width=21,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 1023 | 325 | 93.6 | 6 | 1.62 | 7.62e-05 (2^-13.68) | 13.68 |
| 6 | `pipelined_m:data_width=20,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1128 | 327 | 93.6 | 6 | 1.75 | 4.33e-05 (2^-14.50) | 14.50 |
| 7 | `pipelined_m:data_width=21,n_iter=18,angle_guard=-1,frac_guard=0,rounding=trunc,m=4` | 1223 | 390 | 93.6 | 7 | 1.94 | 3.61e-05 (2^-14.76) | 14.76 |
| 8 | `pipelined_m:data_width=22,n_iter=17,angle_guard=-2,frac_guard=1,rounding=round,m=4` | 1266 | 413 | 89.6 | 7 | 2.02 | 3.29e-05 (2^-14.89) | 14.89 |
| 9 | `pipelined_m:data_width=20,n_iter=18,angle_guard=0,frac_guard=2,rounding=round,m=4` | 1301 | 397 | 93.6 | 7 | 2.04 | 2.91e-05 (2^-15.07) | 15.07 |
| 10 | `pipelined_m:data_width=20,n_iter=18,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1319 | 402 | 93.6 | 7 | 2.07 | 1.92e-05 (2^-15.67) | 15.67 |
| 11 | `pipelined_m:data_width=21,n_iter=18,angle_guard=3,frac_guard=2,rounding=trunc,m=4` | 1367 | 427 | 89.6 | 7 | 2.16 | 1.24e-05 (2^-16.30) | 16.30 |
| 12 | `pipelined_m:data_width=21,n_iter=19,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1409 | 417 | 89.6 | 7 | 2.2 | 1.16e-05 (2^-16.40) | 16.40 |
| 13 | `pipelined_m:data_width=22,n_iter=18,angle_guard=1,frac_guard=1,rounding=round,m=3` | 1395 | 504 | 114.5 | 8 | 2.29 | 1.09e-05 (2^-16.49) | 16.49 |
| 14 | `pipelined_m:data_width=22,n_iter=18,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1467 | 446 | 89.6 | 7 | 2.3 | 8.89e-06 (2^-16.78) | 16.78 |
| 15 | `pipelined_m:data_width=21,n_iter=20,angle_guard=3,frac_guard=3,rounding=trunc,m=4` | 1567 | 435 | 89.6 | 7 | 2.41 | 5.52e-06 (2^-17.47) | 17.47 |
| 16 | `pipelined_m:data_width=22,n_iter=20,angle_guard=3,frac_guard=3,rounding=round,m=4` | 1673 | 454 | 89.6 | 7 | 2.56 | 3.04e-06 (2^-18.33) | 18.33 |
| 17 | `pipelined_m:data_width=24,n_iter=25,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 2079 | 633 | 89.6 | 9 | 3.26 | 1.76e-06 (2^-19.11) | 19.11 |
| 18 | `pipelined_m:data_width=25,n_iter=25,angle_guard=2,frac_guard=1,rounding=round,m=3` | 2208 | 831 | 110.0 | 11 | 3.66 | 4.12e-07 (2^-21.21) | 21.21 |
| 19 | `pipelined_m:data_width=28,n_iter=25,angle_guard=2,frac_guard=2,rounding=trunc,m=3` | 2433 | 933 | 110.0 | 11 | 4.05 | 1.08e-07 (2^-23.14) | 23.14 |
| 20 | `pipelined_m:data_width=28,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc,m=3` | 2484 | 949 | 105.9 | 11 | 4.13 | 9.99e-08 (2^-23.26) | 23.26 |
| 21 | `pipelined_m:data_width=27,n_iter=30,angle_guard=2,frac_guard=3,rounding=round,m=2` | 2965 | 1503 | 152.6 | 17 | 5.38 | 8.19e-08 (2^-23.54) | 23.54 |
| 22 | `pipelined:data_width=28,n_iter=27,angle_guard=3,frac_guard=2,rounding=round` | 2722 | 2664 | 242.0 | 29 | 6.48 | 4.62e-08 (2^-24.37) | 24.37 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The system scenario is the binding constraint: a 1 us tick dumps 32 requests at once and all 32 must be back within 0.44 us (p99). That means the unit must retire roughly one result per cycle. `iterative` needs N+3 >= 7 cycles/result and `unrolled_k` needs ceil(N/k)+3 >= 4 cycles/result, so 32 results cost >= 128-224 cycles; even at an optimistic 200-300 MHz that is 0.6-1.1 us, and their Fmax is far below that for large k/N. They also miss the 32 Msps throughput floor. So only the two fully-pipelined families (1 result/cycle) can plausibly satisfy the spec, and I spend the whole budget on them. Accuracy 2^-12 (output LSB = 2^-(W-2)) forces W >= ~15 and N >= ~13; the area objective with HV ref 4000 means the useful front runs from the minimum-area feasible corner (small W/N, minimal guards) up to ~4000 LUT+FF, so I keep W and N wide enough to reach that corner and to expose the accuracy/area knee. `pipelined_m` should win on FFs (registers every m stages instead of every stage) but loses Fmax, which directly trades against the batch-latency bound, so both families must be mapped. angle_guard/frac_guard are cheap accuracy knobs and are included on both.*)
- `pipelined` (45 evals): data_width=13..22, n_iter=10..22, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round. *Why:* Fully pipelined, 1 result/cycle, best Fmax of the two feasible families -> most margin on sys_p99_batch_us (latency N+2 plus 31 drain cycles). This is the family most likely to survive the L2 re-simulation, and it anchors the high-accuracy / high-area end of the front. W and N ranges cover the 2^-12 feasibility boundary up to ~20 accuracy bits; guards and rounding are the fine accuracy/area knobs.
- `pipelined_m` (55 evals): data_width=13..22, n_iter=10..22, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round, m=2..6. *Why:* Same 1 result/cycle throughput, but registers only every m stages, so it should give the smallest LUT+FF designs (the min-area corner the objective and the 4000 HV ref care about). The cost is a longer combinational path (lower Fmax) and latency ceil(N/m)+2, which eats into the 0.44 us batch budget, so m is kept moderate (2..6) to keep Fmax comfortably above the ~85-110 MHz implied by (latency+31)/0.44us. This is where the area/accuracy knee most likely lives.

**Result (code):** 100 evaluations this round, 100 total; 50 feasible; hypervolume 1.142e+04 (n/a).

**LLM decision:** `map_front` — Feasible families are pipelined and pipelined_m only. iterative/unrolled_k are ruled out analytically by the system constraint: a 32-request burst must finish in 0.44 us, so throughput must be ~>=73 MSPS. iterative needs Fmax >= 32*(N+3)/0.44us (>=509 MHz at N=4) and unrolled_k needs >=291 MHz even at its best case (ceil(N/k)=1, i.e. N<=k=8, which only gives ~2^-8 accuracy) — neither is reachable, so add_family would waste budget. The current front is narrow in parameter space: data_width is only 21..22 (registry 8..28), and accuracy_bits spans 13.7..17.2 while the HV reference is 12 and the datapath can clearly go higher (data_width up to 28, n_iter up to 30). The cheap end (data_width 18..20) is also unmapped on the front even though pipelined_m was feasible down to data_width=18, so cheaper feasible designs may exist below luts_plus_ffs=1348. HV is dominated by the mid-front segments and by the uncovered region between the front and the ref point (4000, 12) on both axes, so the highest-value action is to broaden the front across the full ranges of the two families that actually appear on it, seeded with the current 9 designs.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 1.142e+04 (gain this round: n/a (first round)).
Feasible designs: 50 of 100 evaluations (39 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 41% violate; best seen 5.47e-06 (2^-17.48)
- sys_p99_batch_us <= 0.44: 16% violate; best seen 0.154

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=21 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1348, accuracy_bits=13.7, luts=1023, ffs=325, throughput_msps=93.6, max_abs_err=7.62e-05 (2^-13.68), power_index=1.62
- pipelined_m [data_width=22 n_iter=15 angle_guard=-1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1494, accuracy_bits=13.8, luts=1141, ffs=353, throughput_msps=89.6, max_abs_err=6.8e-05 (2^-13.84), power_index=1.8
- pipelined_m [data_width=22 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1509, accuracy_bits=14, luts=1158, ffs=351, throughput_msps=89.6, max_abs_err=6.25e-05 (2^-13.97), power_index=1.82
- pipelined_m [data_width=21 n_iter=18 angle_guard=0 frac_guard=1 rounding=round m=3] luts_plus_ffs=1800, accuracy_bits=15.7, luts=1321, ffs=478, throughput_msps=119, max_abs_err=1.88e-05 (2^-15.70), power_index=2.17
- pipelined_m [data_width=22 n_iter=18 angle_guard=-1 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1803, accuracy_bits=15.8, luts=1313, ffs=490, throughput_msps=114, max_abs_err=1.78e-05 (2^-15.77), power_index=2.17
- pipelined_m [data_width=22 n_iter=18 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=1900, accuracy_bits=16.5, luts=1395, ffs=504, throughput_msps=114, max_abs_err=1.09e-05 (2^-16.49), power_index=2.29
- pipelined_m [data_width=22 n_iter=18 angle_guard=2 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=2212, accuracy_bits=16.6, luts=1438, ffs=774, throughput_msps=158, max_abs_err=1.01e-05 (2^-16.60), power_index=2.66
- pipelined [data_width=21 n_iter=19 angle_guard=3 frac_guard=1 rounding=round] luts_plus_ffs=2889, accuracy_bits=16.8, luts=1453, ffs=1436, throughput_msps=257, max_abs_err=8.82e-06 (2^-16.79), power_index=3.48
- pipelined [data_width=21 n_iter=21 angle_guard=3 frac_guard=1 rounding=round] luts_plus_ffs=3196, accuracy_bits=17.2, luts=1609, ffs=1587, throughput_msps=257, max_abs_err=6.45e-06 (2^-17.24), power_index=3.85
Front coverage: luts_plus_ffs 1348..3196 (HV reference 4000); accuracy_bits 13.7..17.2 (HV reference 12); data_width on the front 21..22 (registry 8..28).

Per family:
- pipelined: 45 evals, 28 feasible; max throughput seen 282 MSPS; best accuracy 17.24 bits; best feasible luts_plus_ffs=1981; feasible ranges: data_width 19..21, n_iter 14..21, angle_guard -2..3, frac_guard 0..3
- pipelined_m: 55 evals, 22 feasible; max throughput seen 171 MSPS; best accuracy 17.48 bits; best feasible luts_plus_ffs=1348; feasible ranges: data_width 18..22, n_iter 14..22, angle_guard -1..2, frac_guard 0..3, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (78 evals): data_width=20..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (7 front designs; box front_anchored)
- `pipelined` (22 evals): data_width=20..28, n_iter=17..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (2 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 133 feasible; hypervolume 1.786e+04 (+56.3%).

**LLM decision:** `refine` — Round 2 of 4, 200/400 evals used. The front already spans luts_plus_ffs 1348..5385 against HV ref 4000 and accuracy 13.7..24.4 against ref 12, so global coverage is good and the remaining gain is in (a) the cheap corner that the selection rule (min luts_plus_ffs) actually picks and (b) L2 robustness. Evidence: accuracy is far from binding (best 4.62e-08 vs 2^-12, 20% violate but never the good designs), throughput never binds (0% violate), but sys_p99_batch_us is close (best 0.154 vs 0.44) and is only an optimistic L1 bound — the note warns cheap designs that just pass L1 may be lost at L2. The cheapest front design (pipelined_m dW=21/N=15/m=4, 1348 luts+ffs) runs at 93.6 MSPS; a smaller datapath is both cheaper and faster, so probing dW 14..22 buys area and batch margin at once. I am NOT adding iterative/unrolled_k: they emit ≤1 result per ceil(N/k)+3 (or N+3) cycles, so at the N≥13 needed for 2^-12 they would need Fmax ≳ 73*(cycles/result) ≈ 300 MHz (unrolled_k) to >1 GHz (iterative) just to place 32 results in 0.44us — unreachable, and only against the optimistic bound. Round 3 explores the low-width region; round 4 stays reserved for the full-front mapping over pipelined/pipelined_m.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.786e+04 (gain this round: +56.3%).
Feasible designs: 133 of 200 evaluations (112 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 20% violate; best seen 4.62e-08 (2^-24.37)
- sys_p99_batch_us <= 0.44: 16% violate; best seen 0.154

Pareto front (feasible, 20 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=21 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1348, accuracy_bits=13.7, luts=1023, ffs=325, throughput_msps=93.6, max_abs_err=7.62e-05 (2^-13.68), power_index=1.62
- pipelined_m [data_width=22 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1509, accuracy_bits=14, luts=1158, ffs=351, throughput_msps=89.6, max_abs_err=6.25e-05 (2^-13.97), power_index=1.82
- pipelined_m [data_width=22 n_iter=15 angle_guard=4 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1588, accuracy_bits=14, luts=1215, ffs=373, throughput_msps=89.6, max_abs_err=6.2e-05 (2^-13.98), power_index=1.91
- pipelined_m [data_width=26 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1749, accuracy_bits=14, luts=1333, ffs=416, throughput_msps=86, max_abs_err=6.11e-05 (2^-14.00), power_index=2.1
- pipelined_m [data_width=22 n_iter=18 angle_guard=-1 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1803, accuracy_bits=15.8, luts=1313, ffs=490, throughput_msps=114, max_abs_err=1.78e-05 (2^-15.77), power_index=2.17
- pipelined_m [data_width=22 n_iter=18 angle_guard=2 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=2212, accuracy_bits=16.6, luts=1438, ffs=774, throughput_msps=158, max_abs_err=1.01e-05 (2^-16.60), power_index=2.66
- pipelined_m [data_width=28 n_iter=19 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=2429, accuracy_bits=18, luts=1885, ffs=544, throughput_msps=86, max_abs_err=3.82e-06 (2^-18.00), power_index=2.92
- pipelined_m [data_width=25 n_iter=25 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=3039, accuracy_bits=21.2, luts=2208, ffs=831, throughput_msps=110, max_abs_err=4.12e-07 (2^-21.21), power_index=3.66
- pipelined_m [data_width=28 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3433, accuracy_bits=23.3, luts=2484, ffs=949, throughput_msps=106, max_abs_err=9.99e-08 (2^-23.26), power_index=4.13
- pipelined [data_width=28 n_iter=27 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=5385, accuracy_bits=24.4, luts=2722, ffs=2664, throughput_msps=242, max_abs_err=4.62e-08 (2^-24.37), power_index=6.48
Front coverage: luts_plus_ffs 1348..5385 (HV reference 4000); accuracy_bits 13.7..24.4 (HV reference 12); data_width on the front 21..28 (registry 8..28).

Per family:
- pipelined: 67 evals, 50 feasible; max throughput seen 282 MSPS; best accuracy 24.37 bits; best feasible luts_plus_ffs=1981; feasible ranges: data_width 19..28, n_iter 14..29, angle_guard -2..3, frac_guard 0..4
- pipelined_m: 133 evals, 83 feasible; max throughput seen 171 MSPS; best accuracy 23.54 bits; best feasible luts_plus_ffs=1348; feasible ranges: data_width 18..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Do NOT add iterative/unrolled_k. The system issues a 32-request burst per 1us tick and requires sys_p99_batch_us<=0.44 (best seen 0.154) — i.e. ~73 results/us from one shared unit. Non-pipelined families give 1 result per ceil(N/k)+3 (or N+3) cycles, so at the N>=13-15 needed for the 2^-12 error floor they would need Fmax>=73*(N+3) ~ 1.2-2.6 GHz (iterative) or >=73*4-6 cycles ~ 300-450 MHz (unrolled_k) — unattainable on Artix-7, and these are only optimistic L1 bounds. Only the 1-result/cycle families (already on the front) can carry the burst. Accuracy is nowhere near binding (best 4.62e-8 vs 2^-12), area is: the front's cheap corner is 1348 luts+ffs at dW=21, while the registry allows dW down to 8 and per-family feasible sampling only reached dW=18. Reducing data_width lowers luts_plus_ffs (the selection objective) AND raises Fmax, which buys margin on the batch bound that the current cheapest design (93.6 MSPS -> ~0.35-0.4us at L1) only just satisfies — directly de-risking the L2 re-selection. That is the highest-value region; keep the last round for the reserved full-front mapping.*)
- `pipelined_m` (95 evals): data_width=14..22, n_iter=13..20, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round, m=2..6. *Why:* cheapest family (min feasible luts_plus_ffs=1348 at dW=21/N=15/m=4); push data_width down toward the output-quantisation floor (~dW14 for 2^-12) to cut area and raise Fmax
- `pipelined` (5 evals): data_width=14..22, n_iter=13..20, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round. *Why:* placeholder
- clamped by code: dropped duplicate family pipelined_m

**Result (code):** 100 evaluations this round, 300 total; 204 feasible; hypervolume 1.907e+04 (+6.8%).

**LLM decision:** `add_family` — The front is already well-covered on both objectives (luts_plus_ffs 1139..5385 vs HV ref 4000; accuracy_bits 12.3..24.4 vs HV ref 12), so map_front is not indicated by the 'front covers only a small part of an objective's range' rule, and the +6.8% HV gain shows it is still improving, so stop is premature. The binding gap is that only pipelined/pipelined_m have been searched (300 evals, 228 of them pipelined_m), while iterative and unrolled_k are untouched. Since the objective is min luts_plus_ffs and the current cheapest feasible point is 1139 (pipelined_m, W=17/N=14/ag=1/fg=2/trunc/m=4), the shared-datapath families are the only untested place a cheaper design could hide. Note the effective system requirement is stricter than the stated throughput_msps>=32: 32 requests inside 0.44 us needs ~73 MSPS, and the cheapest front point at 93.6 MSPS already sits at 0.342 us, so any new family must clear that bar (iterative's N+3 cycles/result likely cannot, unrolled_k with large k can).

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.907e+04 (gain this round: +6.8%).
Feasible designs: 204 of 300 evaluations (173 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 282
- max_abs_err <= 0.000244141: 19% violate; best seen 4.62e-08 (2^-24.37)
- sys_p99_batch_us <= 0.44: 15% violate; best seen 0.154

Pareto front (feasible, 23 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1139, accuracy_bits=12.3, luts=855, ffs=285, throughput_msps=93.6, max_abs_err=0.000204 (2^-12.26), power_index=1.37
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1177, accuracy_bits=12.5, luts=890, ffs=287, throughput_msps=93.6, max_abs_err=0.000171 (2^-12.51), power_index=1.42
- pipelined_m [data_width=21 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1348, accuracy_bits=13.7, luts=1023, ffs=325, throughput_msps=93.6, max_abs_err=7.62e-05 (2^-13.68), power_index=1.62
- pipelined_m [data_width=21 n_iter=18 angle_guard=-1 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1614, accuracy_bits=14.8, luts=1223, ffs=390, throughput_msps=93.6, max_abs_err=3.61e-05 (2^-14.76), power_index=1.94
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1721, accuracy_bits=15.7, luts=1319, ffs=402, throughput_msps=93.6, max_abs_err=1.92e-05 (2^-15.67), power_index=2.07
- pipelined_m [data_width=21 n_iter=19 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1826, accuracy_bits=16.4, luts=1409, ffs=417, throughput_msps=89.6, max_abs_err=1.16e-05 (2^-16.40), power_index=2.2
- pipelined_m [data_width=21 n_iter=20 angle_guard=3 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=2002, accuracy_bits=17.5, luts=1567, ffs=435, throughput_msps=89.6, max_abs_err=5.52e-06 (2^-17.47), power_index=2.41
- pipelined_m [data_width=24 n_iter=25 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=2712, accuracy_bits=19.1, luts=2079, ffs=633, throughput_msps=89.6, max_abs_err=1.76e-06 (2^-19.11), power_index=3.26
- pipelined_m [data_width=28 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3433, accuracy_bits=23.3, luts=2484, ffs=949, throughput_msps=106, max_abs_err=9.99e-08 (2^-23.26), power_index=4.13
- pipelined [data_width=28 n_iter=27 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=5385, accuracy_bits=24.4, luts=2722, ffs=2664, throughput_msps=242, max_abs_err=4.62e-08 (2^-24.37), power_index=6.48
Front coverage: luts_plus_ffs 1139..5385 (HV reference 4000); accuracy_bits 12.3..24.4 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- pipelined: 72 evals, 52 feasible; max throughput seen 282 MSPS; best accuracy 24.37 bits; best feasible luts_plus_ffs=1981; feasible ranges: data_width 16..28, n_iter 14..29, angle_guard -2..3, frac_guard 0..4
- pipelined_m: 228 evals, 152 feasible; max throughput seen 171 MSPS; best accuracy 23.54 bits; best feasible luts_plus_ffs=1139; feasible ranges: data_width 15..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *Seed with the current front (esp. the 1139-point accuracy recipe W=17/N=14/ag=1/fg=2) so the search starts in the feasible low-area corner; keep the accuracy constraint (max_abs_err<=2^-12) and system bound active as hard filters.*)
- `unrolled_k` (70 evals): data_width=15..22, n_iter=12..20, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round, k=4..8. *Why:* k>=4 keeps ceil(N/k)+3 small enough that Fmax can still deliver the ~73 MSPS the 0.44 us batch bound implies; shared barrel-shifter datapath is the best candidate to undercut 1139 LUT+FF.
- `iterative` (30 evals): data_width=15..22, n_iter=12..20, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round. *Why:* Cheapest possible datapath; include a small slice to confirm/deny feasibility against throughput_msps>=32 and sys_p99_batch_us<=0.44 rather than assume it.

**Result (code):** 100 evaluations this round, 400 total; 204 feasible; hypervolume 1.907e+04 (+0.0%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), and hypervolume gain this round is +0.0% — the front has stopped improving. The spec is feasible, not infeasible: all three constraints are met by real designs (throughput best 282 MSPS vs >=32; max_abs_err best 4.62e-08 vs <=2.44e-04; sys_p99_batch best 0.154 us vs <=0.44 us), and 204 of 400 evaluations are feasible with 23 on the Pareto front. The front already spans the objectives well (luts_plus_ffs 1139..5385 against HV ref 4000; accuracy_bits 12.3..24.4 against HV ref 12), and the selection rule (min luts_plus_ffs) is served by the cheapest front point, pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=4] at luts_plus_ffs=1139 with accuracy_bits=12.3 (max_abs_err 2.04e-04, still under the 2.44e-04 limit) and throughput 93.6 MSPS. All four families were explored; iterative and unrolled_k yielded 0 feasible designs (max throughput ~12 MSPS, far below the 32 MSPS constraint), so no unexplored family remains. Stopping is the correct terminal action.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.907e+04 (gain this round: +0.0%).
Feasible designs: 204 of 400 evaluations (173 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 25% violate; best seen 282
- max_abs_err <= 0.000244141: 25% violate; best seen 4.62e-08 (2^-24.37)
- sys_p99_batch_us <= 0.44: 36% violate; best seen 0.154

Pareto front (feasible, 23 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1139, accuracy_bits=12.3, luts=855, ffs=285, throughput_msps=93.6, max_abs_err=0.000204 (2^-12.26), power_index=1.37
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1177, accuracy_bits=12.5, luts=890, ffs=287, throughput_msps=93.6, max_abs_err=0.000171 (2^-12.51), power_index=1.42
- pipelined_m [data_width=21 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1348, accuracy_bits=13.7, luts=1023, ffs=325, throughput_msps=93.6, max_abs_err=7.62e-05 (2^-13.68), power_index=1.62
- pipelined_m [data_width=21 n_iter=18 angle_guard=-1 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1614, accuracy_bits=14.8, luts=1223, ffs=390, throughput_msps=93.6, max_abs_err=3.61e-05 (2^-14.76), power_index=1.94
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1721, accuracy_bits=15.7, luts=1319, ffs=402, throughput_msps=93.6, max_abs_err=1.92e-05 (2^-15.67), power_index=2.07
- pipelined_m [data_width=21 n_iter=19 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1826, accuracy_bits=16.4, luts=1409, ffs=417, throughput_msps=89.6, max_abs_err=1.16e-05 (2^-16.40), power_index=2.2
- pipelined_m [data_width=21 n_iter=20 angle_guard=3 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=2002, accuracy_bits=17.5, luts=1567, ffs=435, throughput_msps=89.6, max_abs_err=5.52e-06 (2^-17.47), power_index=2.41
- pipelined_m [data_width=24 n_iter=25 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=2712, accuracy_bits=19.1, luts=2079, ffs=633, throughput_msps=89.6, max_abs_err=1.76e-06 (2^-19.11), power_index=3.26
- pipelined_m [data_width=28 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3433, accuracy_bits=23.3, luts=2484, ffs=949, throughput_msps=106, max_abs_err=9.99e-08 (2^-23.26), power_index=4.13
- pipelined [data_width=28 n_iter=27 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=5385, accuracy_bits=24.4, luts=2722, ffs=2664, throughput_msps=242, max_abs_err=4.62e-08 (2^-24.37), power_index=6.48
Front coverage: luts_plus_ffs 1139..5385 (HV reference 4000); accuracy_bits 12.3..24.4 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- iterative: 30 evals, 0 feasible; max throughput seen 12.4 MSPS; best accuracy 16.56 bits
- unrolled_k: 70 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 16.51 bits
- pipelined: 72 evals, 52 feasible; max throughput seen 282 MSPS; best accuracy 24.37 bits; best feasible luts_plus_ffs=1981; feasible ranges: data_width 16..28, n_iter 14..29, angle_guard -2..3, frac_guard 0..4
- pipelined_m: 228 evals, 152 feasible; max throughput seen 171 MSPS; best accuracy 23.54 bits; best feasible luts_plus_ffs=1139; feasible ranges: data_width 15..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 15737 in, 42444 out
- provider-reported cost: $0.0329
- full prompts and replies: `llm_trace.jsonl`

