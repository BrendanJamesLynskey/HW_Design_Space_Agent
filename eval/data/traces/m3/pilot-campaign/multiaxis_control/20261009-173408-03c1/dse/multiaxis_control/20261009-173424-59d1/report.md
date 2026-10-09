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
`pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 868 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 293 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000172 (2^-12.50) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 11.3 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.26e-05 (2^-14.21) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.45 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 98.3 dBc, SNR 82.6 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (24 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 868 | 293 | 93.6 | 6 | 1.4 | 0.000172 (2^-12.50) | 12.50 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 882 | 297 | 93.6 | 6 | 1.42 | 0.000166 (2^-12.55) | 12.55 |
| 2 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 935 | 293 | 93.6 | 6 | 1.48 | 0.000127 (2^-12.95) | 12.95 |
| 3 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=4` | 969 | 287 | 93.6 | 6 | 1.51 | 0.000108 (2^-13.18) | 13.18 |
| 4 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=4` | 985 | 291 | 93.6 | 6 | 1.54 | 8.35e-05 (2^-13.55) | 13.55 |
| 5 | `pipelined_m:data_width=18,n_iter=16,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1055 | 299 | 93.6 | 6 | 1.63 | 6.45e-05 (2^-13.92) | 13.92 |
| 6 | `pipelined_m:data_width=23,n_iter=15,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1185 | 371 | 89.6 | 6 | 1.87 | 6.2e-05 (2^-13.98) | 13.98 |
| 7 | `pipelined_m:data_width=20,n_iter=17,angle_guard=2,frac_guard=1,rounding=trunc,m=3` | 1185 | 468 | 119.3 | 8 | 1.99 | 3.13e-05 (2^-14.96) | 14.96 |
| 8 | `pipelined_m:data_width=21,n_iter=17,angle_guard=1,frac_guard=1,rounding=trunc,m=3` | 1219 | 482 | 119.3 | 8 | 2.05 | 2.41e-05 (2^-15.34) | 15.34 |
| 9 | `pipelined_m:data_width=21,n_iter=17,angle_guard=1,frac_guard=3,rounding=trunc,m=4` | 1287 | 425 | 89.6 | 7 | 2.06 | 2.07e-05 (2^-15.56) | 15.56 |
| 10 | `pipelined_m:data_width=23,n_iter=17,angle_guard=3,frac_guard=0,rounding=trunc,m=4` | 1320 | 445 | 89.6 | 7 | 2.12 | 1.81e-05 (2^-15.75) | 15.75 |
| 11 | `pipelined_m:data_width=22,n_iter=20,angle_guard=1,frac_guard=1,rounding=trunc,m=3` | 1507 | 579 | 114.5 | 9 | 2.51 | 6.93e-06 (2^-17.14) | 17.14 |
| 12 | `pipelined_m:data_width=21,n_iter=21,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1630 | 500 | 89.6 | 8 | 2.56 | 5.47e-06 (2^-17.48) | 17.48 |
| 13 | `pipelined_m:data_width=23,n_iter=21,angle_guard=0,frac_guard=1,rounding=trunc,m=3` | 1628 | 595 | 114.5 | 9 | 2.68 | 4.61e-06 (2^-17.73) | 17.73 |
| 14 | `pipelined_m:data_width=23,n_iter=21,angle_guard=0,frac_guard=2,rounding=round,m=4` | 1719 | 529 | 89.6 | 8 | 2.71 | 3.77e-06 (2^-18.02) | 18.02 |
| 15 | `pipelined_m:data_width=23,n_iter=21,angle_guard=1,frac_guard=1,rounding=trunc,m=3` | 1649 | 602 | 114.5 | 9 | 2.71 | 3.47e-06 (2^-18.14) | 18.14 |
| 16 | `pipelined_m:data_width=23,n_iter=22,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1780 | 525 | 89.6 | 8 | 2.77 | 2.54e-06 (2^-18.58) | 18.58 |
| 17 | `pipelined_m:data_width=25,n_iter=20,angle_guard=0,frac_guard=1,rounding=round,m=3` | 1720 | 644 | 114.5 | 9 | 2.84 | 2.49e-06 (2^-18.61) | 18.61 |
| 18 | `pipelined_m:data_width=24,n_iter=21,angle_guard=0,frac_guard=2,rounding=round,m=3` | 1784 | 633 | 114.5 | 9 | 2.91 | 2.44e-06 (2^-18.65) | 18.65 |
| 19 | `pipelined_m:data_width=23,n_iter=23,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1955 | 547 | 89.6 | 8 | 3.01 | 1.18e-06 (2^-19.69) | 19.69 |
| 20 | `pipelined_m:data_width=28,n_iter=23,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 2208 | 829 | 105.9 | 10 | 3.66 | 3.01e-07 (2^-21.66) | 21.66 |
| 21 | `pipelined_m:data_width=27,n_iter=24,angle_guard=4,frac_guard=2,rounding=round,m=3` | 2365 | 827 | 105.9 | 10 | 3.84 | 1.63e-07 (2^-22.55) | 22.55 |
| 22 | `pipelined_m:data_width=27,n_iter=28,angle_guard=4,frac_guard=2,rounding=trunc,m=3` | 2708 | 1019 | 105.9 | 12 | 4.49 | 1.15e-07 (2^-23.05) | 23.05 |
| 23 | `pipelined_m:data_width=28,n_iter=28,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 2708 | 1023 | 105.9 | 12 | 4.49 | 1e-07 (2^-23.25) | 23.25 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec needs >=32 Msps throughput and a 0.44us p99 batch deadline for a 32-request burst every 1us, with max_abs_err <= 2^-12 (accuracy_bits >= 12) and minimised luts+ffs. Only the pipelined families produce one result/cycle, so they are the natural fit for sustained 32 Msps; pipelined_m adds the m knob that directly trades FFs against Fmax and batch latency, which is exactly the trade-off the hypervolume should map, so it gets the largest share. pipelined (m=1) anchors the low-latency/high-Fmax corner that most reliably clears the batch bound. unrolled_k is included at a smaller share to test whether a shared-FSM, multi-rotation/cycle design yields a cheaper area point that still meets the deadline. data_width 14-18 and n_iter 12-18 are chosen so accuracy_bits comfortably exceeds 12 (leaving margin for the L2 re-screen) while keeping area low; angle_guard 0-2 and frac_guard 0-2 cover the small accuracy/area trade-offs without wasting budget on wide guards that only add area. iterative is excluded because its one-result-per-several-cycles throughput cannot plausibly reach 32 Msps within a reasonable Fmax.*)
- `pipelined_m` (45 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..6. *Why:* One result/cycle meets throughput>=32 Msps at modest Fmax. Registering every m stages trades FFs (area) against Fmax and batch latency; m is the key trade-off knob for the 0.44us p99 batch deadline, so this family spans the area-vs-latency curve the hypervolume rewards.
- `pipelined` (35 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Fully registered (m=1) gives the lowest latency per stage and the highest Fmax, so it most safely clears the 0.44us batch bound; it is the latency/throughput corner of the front. Costs more FFs than pipelined_m, so it anchors the high-accuracy/high-Fmax end of the trade-off.
- `unrolled_k` (20 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=4..8. *Why:* k chained rotations/cycle with a shared FSM can hit 32 Msps at lower Fmax than pipelined and with fewer FFs than full pipelining, potentially giving a cheaper area point on the front. k is capped at 8 so it needs Fmax ~4-8 MHz to clear 32 Msps; included to test whether it lands a cheaper luts+ffs point that still meets the batch bound.

**Result (code):** 100 evaluations this round, 100 total; 11 feasible; hypervolume 3112 (n/a).

**LLM decision:** `refine` — Round 1 established that pipelined and pipelined_m are the only feasible families, with pipelined_m achieving the best area (1510) and pipelined achieving the best accuracy (13.40 bits) and throughput (273 MSPS). The front currently has only 3 designs, and the area range (1510-2258) and accuracy range (12.9-13.4) are narrow. The 67% violation rate on max_abs_err suggests that many designs fail the accuracy constraint, so focusing on the region where accuracy is met with margin (data_width 15-18, n_iter 14-18) is appropriate. The 42% violation rate on sys_p99_batch_us is concerning but the best seen (0.161 us) is well below the 0.44 us constraint, so the system constraint is likely met for the feasible designs. The 20% throughput violation is driven by unrolled_k (max 10.3 MSPS) and possibly some low-Fmax pipelined designs, but the feasible pipelined/pipelined_m designs all exceed 32 MSPS. Refining the ranges around the known feasible region for pipelined and pipelined_m, and adding a small exploration of iterative to confirm infeasibility, should improve the front coverage and hypervolume in Round 2.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 3112 (gain this round: n/a (first round)).
Feasible designs: 11 of 100 evaluations (11 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 20% violate; best seen 273
- max_abs_err <= 0.000244141: 67% violate; best seen 9.28e-05 (2^-13.40)
- sys_p99_batch_us <= 0.44: 42% violate; best seen 0.161

Pareto front (feasible, 3 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=2] luts_plus_ffs=1510, accuracy_bits=12.9, luts=987, ffs=523, throughput_msps=171, max_abs_err=0.000134 (2^-12.86), power_index=1.82
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=round] luts_plus_ffs=2038, accuracy_bits=13, luts=1023, ffs=1015, throughput_msps=264, max_abs_err=0.00012 (2^-13.03), power_index=2.45
- pipelined [data_width=17 n_iter=18 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=2258, accuracy_bits=13.4, luts=1134, ffs=1124, throughput_msps=264, max_abs_err=9.28e-05 (2^-13.40), power_index=2.72
Front coverage: luts_plus_ffs 1510..2258 (HV reference 4000); accuracy_bits 12.9..13.4 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 12.76 bits
- pipelined: 35 evals, 10 feasible; max throughput seen 273 MSPS; best accuracy 13.40 bits; best feasible luts_plus_ffs=1665; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 0..2, frac_guard 1..2
- pipelined_m: 45 evals, 1 feasible; max throughput seen 171 MSPS; best accuracy 13.23 bits; best feasible luts_plus_ffs=1510; feasible ranges: data_width 16..16, n_iter 16..16, angle_guard 2..2, frac_guard 2..2, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 1 established that pipelined and pipelined_m are the only feasible families, with pipelined_m achieving the best area (1510) and pipelined achieving the best accuracy (13.40 bits) and throughput (273 MSPS). The front currently has only 3 designs, and the area range (1510-2258) and accuracy range (12.9-13.4) are narrow. The 67% violation rate on max_abs_err suggests that many designs fail the accuracy constraint, so focusing on the region where accuracy is met with margin (data_width 15-18, n_iter 14-18) is appropriate. The 42% violation rate on sys_p99_batch_us is concerning but the best seen (0.161 us) is well below the 0.44 us constraint, so the system constraint is likely met for the feasible designs. The 20% throughput violation is driven by unrolled_k (max 10.3 MSPS) and possibly some low-Fmax pipelined designs, but the feasible pipelined/pipelined_m designs all exceed 32 MSPS. Refining the ranges around the known feasible region for pipelined and pipelined_m, and adding a small exploration of iterative to confirm infeasibility, should improve the front coverage and hypervolume in Round 2.*)
- `pipelined` (50 evals): data_width=15..18, n_iter=14..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined is the dominant family (10 feasible, best area 1665, best accuracy 13.40 bits). The current front's area minimum (1510) comes from a single pipelined_m point, but pipelined has much higher throughput headroom (273 vs 171 MSPS) and a broader feasible region. Narrowing data_width to 15-18 and n_iter to 14-18 focuses the search on the accuracy/area trade-off knee where the constraint max_abs_err <= 2^-12 is met with margin, while allowing angle_guard/frac_guard to vary to find cheaper guard-bit configurations.
- `pipelined_m` (30 evals): data_width=15..18, n_iter=14..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m found the single best area point (1510 LUTs+FFs) but only 1 feasible design out of 45 evals, suggesting the feasible region is narrow. The m=2 setting was the only one tested. Expanding m to 2-4 and widening data_width/n_iter slightly around the known feasible point (16,16) may reveal other low-area configurations. The lower area of pipelined_m (523 FFs vs 1015 for pipelined) makes it attractive for the min luts_plus_ffs objective, but its lower throughput (171 vs 273 MSPS) is still well above the 32 MSPS constraint, so it remains a strong candidate.
- `iterative` (20 evals): data_width=15..18, n_iter=14..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative has not been explored yet. It has the lowest area overhead (shared datapath, no pipeline registers) and may offer the best luts_plus_ffs for the min objective. However, its throughput is 1 result per N+3 cycles, so for N=14-18, throughput is ~1/(17-21) results/cycle. At Fmax ~100-200 MHz, this gives ~5-12 MSPS, which is below the 32 MSPS constraint. This is likely infeasible for throughput, but it is worth a small budget share to confirm. If iterative is infeasible, the budget is better spent on pipelined/pipelined_m.

**Result (code):** 100 evaluations this round, 200 total; 65 feasible; hypervolume 5290 (+70.0%).

**LLM decision:** `refine` — The current Pareto front is dominated by `pipelined_m` designs with `data_width=18`, `n_iter` between 14 and 16, and `m=4`. The `pipelined` family is significantly less efficient (best area 1665 vs 1161) and `iterative`/`unrolled_k` fail the throughput constraint entirely. The front currently spans `luts_plus_ffs` 1161..1353 and `accuracy_bits` 12.5..13.9. To maximize hypervolume, we need to explore if we can push `accuracy_bits` higher (towards 14+) without excessive area penalty, or if we can reduce area below 1161 by lowering `n_iter` or `data_width` slightly while maintaining the error constraint. The `max_abs_err` constraint is 2^-12, and the current best is 2^-13.92, so there is headroom. However, the front is clustered at `data_width=18`. We should narrow the search to `pipelined_m` only, focusing on `data_width` 16-18, `n_iter` 12-16, `angle_guard` 0-2, `frac_guard` 0-1, and `m` 2-4 to densely map the trade-off curve in this specific region.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 5290 (gain this round: +70.0%).
Feasible designs: 65 of 200 evaluations (50 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 20% violate; best seen 273
- max_abs_err <= 0.000244141: 48% violate; best seen 6.45e-05 (2^-13.92)
- sys_p99_batch_us <= 0.44: 31% violate; best seen 0.161

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1161, accuracy_bits=12.5, luts=868, ffs=293, throughput_msps=93.6, max_abs_err=0.000172 (2^-12.50), power_index=1.4
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1179, accuracy_bits=12.6, luts=882, ffs=297, throughput_msps=93.6, max_abs_err=0.000166 (2^-12.55), power_index=1.42
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1227, accuracy_bits=12.9, luts=935, ffs=293, throughput_msps=93.6, max_abs_err=0.000127 (2^-12.95), power_index=1.48
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=1.51
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1276, accuracy_bits=13.5, luts=985, ffs=291, throughput_msps=93.6, max_abs_err=8.35e-05 (2^-13.55), power_index=1.54
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1353, accuracy_bits=13.9, luts=1055, ffs=299, throughput_msps=93.6, max_abs_err=6.45e-05 (2^-13.92), power_index=1.63
Front coverage: luts_plus_ffs 1161..1353 (HV reference 4000); accuracy_bits 12.5..13.9 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- iterative: 20 evals, 0 feasible; max throughput seen 11 MSPS; best accuracy 13.92 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 12.76 bits
- pipelined: 85 evals, 37 feasible; max throughput seen 273 MSPS; best accuracy 13.60 bits; best feasible luts_plus_ffs=1665; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 75 evals, 28 feasible; max throughput seen 171 MSPS; best accuracy 13.92 bits; best feasible luts_plus_ffs=1161; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Narrowing to pipelined_m and the observed feasible ranges allows the optimizer to spend the remaining budget densely sampling the high-performing region rather than wasting evaluations on less efficient families or out-of-range parameters.*)
- `pipelined_m` (40 evals): data_width=16..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..1, rounding=trunc|round, m=2..4. *Why:* Focus exclusively on the most efficient family and the specific parameter region that produced the current Pareto front to refine the trade-off curve.

**Result (code):** 40 evaluations this round, 240 total; 91 feasible; hypervolume 5290 (+0.0%).

**LLM decision:** `stop` — The Pareto front is well-established and stable (0.0% hypervolume gain in Round 3). The `pipelined_m` family dominates the feasible space, offering a clear trade-off curve from 1161 to 1353 LUTs+FFs with accuracy bits ranging from 12.5 to 13.9. All designs on the front satisfy the strict constraints: throughput is consistently ~93.6 MSPS (well above the 32 MSPS requirement), max_abs_err is below 2^-12 (best 2^-13.92), and the system p99 batch latency is bounded well under 0.44 us (best seen 0.161 us). The selection rule (min luts_plus_ffs) points to the `pipelined_m` design with 1161 LUTs+FFs and 12.5 accuracy bits, which is a robust choice. Since this is the final round and the front covers the relevant trade-off space effectively without violating any constraints, stopping is the correct action.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 5290 (gain this round: +0.0%).
Feasible designs: 91 of 240 evaluations (65 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 17% violate; best seen 273
- max_abs_err <= 0.000244141: 46% violate; best seen 6.45e-05 (2^-13.92)
- sys_p99_batch_us <= 0.44: 26% violate; best seen 0.161

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1161, accuracy_bits=12.5, luts=868, ffs=293, throughput_msps=93.6, max_abs_err=0.000172 (2^-12.50), power_index=1.4
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1179, accuracy_bits=12.6, luts=882, ffs=297, throughput_msps=93.6, max_abs_err=0.000166 (2^-12.55), power_index=1.42
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1227, accuracy_bits=12.9, luts=935, ffs=293, throughput_msps=93.6, max_abs_err=0.000127 (2^-12.95), power_index=1.48
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=1.51
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1276, accuracy_bits=13.5, luts=985, ffs=291, throughput_msps=93.6, max_abs_err=8.35e-05 (2^-13.55), power_index=1.54
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1353, accuracy_bits=13.9, luts=1055, ffs=299, throughput_msps=93.6, max_abs_err=6.45e-05 (2^-13.92), power_index=1.63
Front coverage: luts_plus_ffs 1161..1353 (HV reference 4000); accuracy_bits 12.5..13.9 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- iterative: 20 evals, 0 feasible; max throughput seen 11 MSPS; best accuracy 13.92 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 12.76 bits
- pipelined: 85 evals, 37 feasible; max throughput seen 273 MSPS; best accuracy 13.60 bits; best feasible luts_plus_ffs=1665; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 115 evals, 54 feasible; max throughput seen 171 MSPS; best accuracy 13.92 bits; best feasible luts_plus_ffs=1161; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (160 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (6 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 193 feasible; hypervolume 1.922e+04 (+263.3%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and stable (0.0% hypervolume gain in Round 3). The `pipelined_m` family dominates the feasible space, offering a clear trade-off curve from 1161 to 1353 LUTs+FFs with accuracy bits ranging from 12.5 to 13.9. All designs on the front satisfy the strict constraints: throughput is consistently ~93.6 MSPS (well above the 32 MSPS requirement), max_abs_err is below 2^-12 (best 2^-13.92), and the system p99 batch latency is bounded well under 0.44 us (best seen 0.161 us). The selection rule (min luts_plus_ffs) points to the `pipelined_m` design with 1161 LUTs+FFs and 12.5 accuracy bits, which is a robust choice. Since this is the final round and the front covers the relevant trade-off space effectively without violating any constraints, stopping is the correct action.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.922e+04 (gain this round: +263.3%).
Feasible designs: 193 of 400 evaluations (154 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 10% violate; best seen 273
- max_abs_err <= 0.000244141: 29% violate; best seen 3.07e-08 (2^-24.96)
- sys_p99_batch_us <= 0.44: 29% violate; best seen 0.161

Pareto front (feasible, 24 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1161, accuracy_bits=12.5, luts=868, ffs=293, throughput_msps=93.6, max_abs_err=0.000172 (2^-12.50), power_index=1.4
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1256, accuracy_bits=13.2, luts=969, ffs=287, throughput_msps=93.6, max_abs_err=0.000108 (2^-13.18), power_index=1.51
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1353, accuracy_bits=13.9, luts=1055, ffs=299, throughput_msps=93.6, max_abs_err=6.45e-05 (2^-13.92), power_index=1.63
- pipelined_m [data_width=21 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1701, accuracy_bits=15.3, luts=1219, ffs=482, throughput_msps=119, max_abs_err=2.41e-05 (2^-15.34), power_index=2.05
- pipelined_m [data_width=23 n_iter=17 angle_guard=3 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1765, accuracy_bits=15.7, luts=1320, ffs=445, throughput_msps=89.6, max_abs_err=1.81e-05 (2^-15.75), power_index=2.12
- pipelined_m [data_width=23 n_iter=21 angle_guard=0 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=2223, accuracy_bits=17.7, luts=1628, ffs=595, throughput_msps=114, max_abs_err=4.61e-06 (2^-17.73), power_index=2.68
- pipelined_m [data_width=23 n_iter=21 angle_guard=1 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=2251, accuracy_bits=18.1, luts=1649, ffs=602, throughput_msps=114, max_abs_err=3.47e-06 (2^-18.14), power_index=2.71
- pipelined_m [data_width=24 n_iter=21 angle_guard=0 frac_guard=2 rounding=round m=3] luts_plus_ffs=2417, accuracy_bits=18.6, luts=1784, ffs=633, throughput_msps=114, max_abs_err=2.44e-06 (2^-18.65), power_index=2.91
- pipelined_m [data_width=28 n_iter=23 angle_guard=3 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=3037, accuracy_bits=21.7, luts=2208, ffs=829, throughput_msps=106, max_abs_err=3.01e-07 (2^-21.66), power_index=3.66
- pipelined_m [data_width=28 n_iter=28 angle_guard=3 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=3731, accuracy_bits=23.3, luts=2708, ffs=1023, throughput_msps=106, max_abs_err=1e-07 (2^-23.25), power_index=4.49
Front coverage: luts_plus_ffs 1161..3731 (HV reference 4000); accuracy_bits 12.5..23.3 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- iterative: 20 evals, 0 feasible; max throughput seen 11 MSPS; best accuracy 13.92 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 12.76 bits
- pipelined: 85 evals, 37 feasible; max throughput seen 273 MSPS; best accuracy 13.60 bits; best feasible luts_plus_ffs=1665; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 275 evals, 156 feasible; max throughput seen 171 MSPS; best accuracy 24.96 bits; best feasible luts_plus_ffs=1161; feasible ranges: data_width 16..28, n_iter 13..29, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 1)
- tokens: 25553 in, 4494 out
- provider-reported cost: $0.0143
- full prompts and replies: `llm_trace.jsonl`

