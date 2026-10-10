# DSE run: multiaxis_control

**Verdict:** converged: hypervolume gain fell below epsilon.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 3 round(s).  
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

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Every L1-feasible design (144) was simulated at its estimated Fmax (SimPy); 140 pass. Top 5 by the selection rule, L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=2,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=3` | 0.2973 → 0.3052 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=16,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 0.3679 → 0.378 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (22 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 855 | 285 | 93.6 | 6 | 1.37 | 0.000204 (2^-12.26) | 12.26 |
| 1 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=2,rounding=round,m=4` | 890 | 287 | 93.6 | 6 | 1.42 | 0.000171 (2^-12.51) | 12.51 |
| 2 | `pipelined_m:data_width=17,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=4` | 926 | 280 | 97.8 | 6 | 1.45 | 0.000158 (2^-12.63) | 12.63 |
| 3 | `pipelined_m:data_width=17,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 985 | 285 | 93.6 | 6 | 1.53 | 0.000145 (2^-12.76) | 12.76 |
| 4 | `pipelined_m:data_width=17,n_iter=16,angle_guard=1,frac_guard=1,rounding=round,m=4` | 989 | 280 | 97.8 | 6 | 1.53 | 0.000128 (2^-12.94) | 12.94 |
| 5 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=3,rounding=trunc,m=4` | 994 | 305 | 93.6 | 6 | 1.56 | 0.000102 (2^-13.26) | 13.26 |
| 6 | `pipelined_m:data_width=21,n_iter=15,angle_guard=-1,frac_guard=2,rounding=round,m=4` | 1112 | 335 | 89.6 | 6 | 1.74 | 7.4e-05 (2^-13.72) | 13.72 |
| 7 | `pipelined_m:data_width=21,n_iter=15,angle_guard=2,frac_guard=0,rounding=trunc,m=3` | 1053 | 406 | 114.5 | 7 | 1.76 | 7.32e-05 (2^-13.74) | 13.74 |
| 8 | `pipelined_m:data_width=20,n_iter=15,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1124 | 337 | 89.6 | 6 | 1.76 | 6.44e-05 (2^-13.92) | 13.92 |
| 9 | `pipelined_m:data_width=20,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=3` | 1064 | 452 | 119.3 | 8 | 1.83 | 4.64e-05 (2^-14.39) | 14.39 |
| 10 | `pipelined_m:data_width=20,n_iter=18,angle_guard=1,frac_guard=0,rounding=round,m=4` | 1205 | 383 | 93.6 | 7 | 1.91 | 2.9e-05 (2^-15.07) | 15.07 |
| 11 | `pipelined_m:data_width=21,n_iter=18,angle_guard=2,frac_guard=0,rounding=round,m=4` | 1277 | 406 | 89.6 | 7 | 2.03 | 1.59e-05 (2^-15.94) | 15.94 |
| 12 | `pipelined_m:data_width=20,n_iter=18,angle_guard=3,frac_guard=4,rounding=round,m=4` | 1427 | 428 | 89.6 | 7 | 2.23 | 1.13e-05 (2^-16.43) | 16.43 |
| 13 | `pipelined_m:data_width=20,n_iter=19,angle_guard=3,frac_guard=4,rounding=trunc,m=4` | 1466 | 426 | 89.6 | 7 | 2.28 | 1.03e-05 (2^-16.57) | 16.57 |
| 14 | `pipelined_m:data_width=21,n_iter=19,angle_guard=3,frac_guard=3,rounding=trunc,m=4` | 1485 | 435 | 89.6 | 7 | 2.31 | 7.43e-06 (2^-17.04) | 17.04 |
| 15 | `pipelined_m:data_width=21,n_iter=19,angle_guard=3,frac_guard=4,rounding=trunc,m=4` | 1523 | 443 | 89.6 | 7 | 2.37 | 7.12e-06 (2^-17.10) | 17.10 |
| 16 | `pipelined_m:data_width=26,n_iter=20,angle_guard=-1,frac_guard=2,rounding=trunc,m=4` | 1747 | 492 | 86.0 | 7 | 2.7 | 2.51e-06 (2^-18.60) | 18.60 |
| 17 | `pipelined_m:data_width=25,n_iter=21,angle_guard=2,frac_guard=0,rounding=trunc,m=3` | 1754 | 644 | 110.0 | 9 | 2.89 | 1.89e-06 (2^-19.01) | 19.01 |
| 18 | `pipelined_m:data_width=27,n_iter=21,angle_guard=2,frac_guard=0,rounding=round,m=3` | 1881 | 690 | 110.0 | 9 | 3.09 | 1.05e-06 (2^-19.87) | 19.87 |
| 19 | `pipelined_m:data_width=25,n_iter=24,angle_guard=4,frac_guard=1,rounding=round,m=2` | 2167 | 1116 | 152.6 | 14 | 3.95 | 4.27e-07 (2^-21.16) | 21.16 |
| 20 | `pipelined_m:data_width=27,n_iter=24,angle_guard=1,frac_guard=1,rounding=trunc,m=2` | 2187 | 1154 | 152.6 | 14 | 4.02 | 3.19e-07 (2^-21.58) | 21.58 |
| 21 | `pipelined_m:data_width=27,n_iter=26,angle_guard=1,frac_guard=2,rounding=round,m=3` | 2486 | 897 | 110.0 | 11 | 4.07 | 1.48e-07 (2^-22.69) | 22.69 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is throughput- and deadline-bound: 32 requests per 1us tick with all 32 results back within 0.44us of the tick. Only the 1-result-per-cycle families (pipelined, pipelined_m) can sustain 32 Msps and finish a 32-deep back-to-back batch inside the tick window; iterative and unrolled_k (1 result every several cycles) would queue the burst and blow the p99-batch bound, so they are excluded. The accuracy constraint max_abs_err<=2^-12 is met by modest W and N (W=14/N=12 is the likely minimal corner), so I bracket data_width 14..18 and n_iter 12..16 to map the area-vs-accuracy trade-off rather than oversizing. angle_guard 0..2 and frac_guard 0..2 keep the datapath lean for the min-luts_plus_ffs objective while still exposing the accuracy knobs. pipelined is the Fmax/latency-strong end; pipelined_m (m=2..4) is the area-reduction end; together they should span the feasible Pareto front. I split the budget evenly between the two because both are plausible front members and the hypervolume rewards covering the whole curve, not just the min-area corner the selection rule picks.*)
- `pipelined` (50 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* 1 result/cycle is the only way to clear the 32 req/us throughput and the 0.44us p99-batch bound (32 back-to-back results must finish inside the 1us tick window). Full pipelining gives the best Fmax of the 1/cycle families, which is what the tight batch deadline needs. W=14..18 and N=12..16 bracket the max_abs_err<=2^-12 constraint (W=14/N=12 is the likely minimal corner; W=18/N=16 the accuracy-rich end) so the front spans the area-vs-accuracy trade-off. angle_guard 0..2 and frac_guard 0..2 keep the datapath lean (minimise LUTs+FFs) while still allowing the accuracy knobs to be explored.
- `pipelined_m` (50 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Same 1 result/cycle throughput as pipelined, so it also clears the throughput and batch-deadline constraints, but register-every-m trades area (fewer FFs, smaller luts_plus_ffs) for a lower Fmax. Since the objective is min luts_plus_ffs, this family is the natural area-reduction candidate against pipelined; m=2..4 keeps latency (ceil(N/m)+2) and Fmax high enough to still meet the 0.44us batch bound. Same W/N/guard ranges as pipelined so the two families are directly comparable on the front.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 52 feasible; hypervolume 5618 (n/a).

**LLM decision:** `add_family` — The current front is dominated by pipelined_m designs with a minimum area of 1139 LUTs+FFs. The `iterative` and `unrolled_k` families have not been explored yet. `iterative` uses a shared datapath with barrel shifters and no pipeline registers (or very few), which typically results in significantly lower LUT and FF counts compared to pipelined architectures, potentially pushing the area objective well below the current 1139. Although `iterative` has a higher latency (N+3 cycles), the system constraint `sys_p99_batch_us <= 0.44` is currently met with a large margin (best seen 0.161 us) by the pipelined designs, and the throughput constraint (>= 32 MSPS) is also easily met by pipelined designs. However, for `iterative`, throughput is 1 result every N+3 cycles. To meet 32 MSPS, we need Fmax * (1/(N+3)) >= 32 MHz. If Fmax is ~100-200 MHz, N+3 must be small (e.g., N=4 -> 7 cycles -> ~14-28 MSPS, which might fail). Wait, let's check the throughput constraint. `throughput_msps >= 32`. For `iterative`, throughput = Fmax / (N+3). If Fmax is 100 MHz and N=4, throughput is 100/7 = 14.28 MSPS, which violates the constraint. If N=1 (not allowed, min 4), it would be better. So `iterative` might struggle with the throughput constraint unless Fmax is very high or N is very small. `unrolled_k` with k=2 or 3 might offer a better balance: it processes k rotations per cycle, so throughput = Fmax / (ceil(N/k)+3). This is higher than iterative but lower than pipelined. It likely has fewer FFs than pipelined_m because it doesn't register every stage, but more than iterative. Given the area objective is primary, exploring `unrolled_k` and `iterative` is crucial to see if they can beat 1139 LUTs+FFs while meeting the throughput and system latency constraints. The system latency constraint `sys_p99_batch_us <= 0.44` is tight for non-pipelined designs if the batch of 32 requests must be processed within that window. If the CORDIC is iterative, it takes N+3 cycles per request. For 32 requests, that's 32*(N+3) cycles. At 100 MHz, 1 cycle = 10 ns. 32*7 = 224 cycles = 2.24 us, which violates the 0.44 us constraint. Thus, `iterative` is likely infeasible for the system constraint. `unrolled_k` with k=4, N=16: ceil(16/4)+3 = 7 cycles per request. 32 requests * 7 cycles = 224 cycles = 2.24 us. Still too slow. Wait, the system constraint is on the *batch* latency. The spec says 

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 5618 (gain this round: n/a (first round)).
Feasible designs: 52 of 100 evaluations (38 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 48% violate; best seen 5.46e-05 (2^-14.16)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.161

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1139, accuracy_bits=12.3, luts=855, ffs=285, throughput_msps=93.6, max_abs_err=0.000204 (2^-12.26), power_index=1.37
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1177, accuracy_bits=12.5, luts=890, ffs=287, throughput_msps=93.6, max_abs_err=0.000171 (2^-12.51), power_index=1.42
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1207, accuracy_bits=12.6, luts=926, ffs=280, throughput_msps=97.8, max_abs_err=0.000158 (2^-12.63), power_index=1.45
- pipelined_m [data_width=17 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1270, accuracy_bits=12.8, luts=985, ffs=285, throughput_msps=93.6, max_abs_err=0.000145 (2^-12.76), power_index=1.53
- pipelined_m [data_width=17 n_iter=16 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1270, accuracy_bits=12.9, luts=989, ffs=280, throughput_msps=97.8, max_abs_err=0.000128 (2^-12.94), power_index=1.53
- pipelined_m [data_width=17 n_iter=16 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=1435, accuracy_bits=13.2, luts=1021, ffs=414, throughput_msps=119, max_abs_err=0.000109 (2^-13.16), power_index=1.73
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=1504, accuracy_bits=13.7, luts=1071, ffs=434, throughput_msps=119, max_abs_err=7.47e-05 (2^-13.71), power_index=1.81
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=2] luts_plus_ffs=1662, accuracy_bits=14.2, luts=1086, ffs=575, throughput_msps=164, max_abs_err=5.46e-05 (2^-14.16), power_index=2
Front coverage: luts_plus_ffs 1139..1662 (HV reference 4000); accuracy_bits 12.3..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 50 evals, 27 feasible; max throughput seen 273 MSPS; best accuracy 14.16 bits; best feasible luts_plus_ffs=1744; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 25 feasible; max throughput seen 171 MSPS; best accuracy 14.16 bits; best feasible luts_plus_ffs=1139; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Adding unrolled_k and iterative to explore the area-accuracy trade-off space not covered by pipelined families, focusing on whether lower area designs can meet the strict system batch latency constraint.*)
- `unrolled_k` (67 evals): data_width=16..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..8. *Why:* unrolled_k may offer lower area than pipelined_m by reducing register count while maintaining higher throughput than iterative, potentially meeting the system batch latency constraint if k is large enough.
- `iterative` (33 evals): data_width=16..18, n_iter=4..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative has the lowest area but likely fails the system batch latency constraint due to high per-request latency; exploring it confirms infeasibility or finds a corner case with very high Fmax.

**Result (code):** 100 evaluations this round, 200 total; 52 feasible; hypervolume 5618 (+0.0%).

**LLM decision:** `refine` — The current Pareto front is dominated by `pipelined_m` designs, which are significantly more area-efficient (min 1139 LUTs+FFs) than the `pipelined` family (min 1744 LUTs+FFs). The `iterative` and `unrolled_k` families are infeasible due to throughput constraints (max 24.8 and 10.5 MSPs respectively, well below the 32 MSPs requirement). The `pipelined_m` family has already explored m=2, 3, and 4. To maximize hypervolume and find the true minimum area design, we should focus the remaining budget on refining the `pipelined_m` family in the region where it dominates. Specifically, we should narrow the search to `data_width` 16-18, `n_iter` 14-16, `angle_guard` 0-2, `frac_guard` 0-2, and `m` 2-4. This will allow Optuna to densely sample the trade-off curve between area and accuracy within the feasible region, potentially uncovering designs with lower area or higher accuracy than the current 8-point front.
- **rule applied by code:** 'refine' overridden to stop: HV gain 0.00% < epsilon 1.00%
- **rule applied by code:** code: before stopping (converged), one front-mapping round with the remaining 200 evaluations
- effective decision: `stop`

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 5618 (gain this round: +0.0%).
Feasible designs: 52 of 200 evaluations (38 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 50% violate; best seen 273
- max_abs_err <= 0.000244141: 48% violate; best seen 5.46e-05 (2^-14.16)
- sys_p99_batch_us <= 0.44: 50% violate; best seen 0.161

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1139, accuracy_bits=12.3, luts=855, ffs=285, throughput_msps=93.6, max_abs_err=0.000204 (2^-12.26), power_index=1.37
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1177, accuracy_bits=12.5, luts=890, ffs=287, throughput_msps=93.6, max_abs_err=0.000171 (2^-12.51), power_index=1.42
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1207, accuracy_bits=12.6, luts=926, ffs=280, throughput_msps=97.8, max_abs_err=0.000158 (2^-12.63), power_index=1.45
- pipelined_m [data_width=17 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1270, accuracy_bits=12.8, luts=985, ffs=285, throughput_msps=93.6, max_abs_err=0.000145 (2^-12.76), power_index=1.53
- pipelined_m [data_width=17 n_iter=16 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1270, accuracy_bits=12.9, luts=989, ffs=280, throughput_msps=97.8, max_abs_err=0.000128 (2^-12.94), power_index=1.53
- pipelined_m [data_width=17 n_iter=16 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=1435, accuracy_bits=13.2, luts=1021, ffs=414, throughput_msps=119, max_abs_err=0.000109 (2^-13.16), power_index=1.73
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=1504, accuracy_bits=13.7, luts=1071, ffs=434, throughput_msps=119, max_abs_err=7.47e-05 (2^-13.71), power_index=1.81
- pipelined_m [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=2] luts_plus_ffs=1662, accuracy_bits=14.2, luts=1086, ffs=575, throughput_msps=164, max_abs_err=5.46e-05 (2^-14.16), power_index=2
Front coverage: luts_plus_ffs 1139..1662 (HV reference 4000); accuracy_bits 12.3..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- iterative: 33 evals, 0 feasible; max throughput seen 24.8 MSPS; best accuracy 12.53 bits
- unrolled_k: 67 evals, 0 feasible; max throughput seen 10.5 MSPS; best accuracy 13.92 bits
- pipelined: 50 evals, 27 feasible; max throughput seen 273 MSPS; best accuracy 14.16 bits; best feasible luts_plus_ffs=1744; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 25 feasible; max throughput seen 171 MSPS; best accuracy 14.16 bits; best feasible luts_plus_ffs=1139; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 200 evaluations*)
- `pipelined_m` (200 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (8 front designs; box front_anchored)

**Result (code):** 200 evaluations this round, 400 total; 173 feasible; hypervolume 1.886e+04 (+235.7%).

**No LLM call** (code's front-mapping round): The current Pareto front is dominated by `pipelined_m` designs, which are significantly more area-efficient (min 1139 LUTs+FFs) than the `pipelined` family (min 1744 LUTs+FFs). The `iterative` and `unrolled_k` families are infeasible due to throughput constraints (max 24.8 and 10.5 MSPs respectively, well below the 32 MSPs requirement). The `pipelined_m` family has already explored m=2, 3, and 4. To maximize hypervolume and find the true minimum area design, we should focus the remaining budget on refining the `pipelined_m` family in the region where it dominates. Specifically, we should narrow the search to `data_width` 16-18, `n_iter` 14-16, `angle_guard` 0-2, `frac_guard` 0-2, and `m` 2-4. This will allow Optuna to densely sample the trade-off curve between area and accuracy within the feasible region, potentially uncovering designs with lower area or higher accuracy than the current 8-point front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.886e+04 (gain this round: +235.7%).
Feasible designs: 173 of 400 evaluations (144 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 25% violate; best seen 273
- max_abs_err <= 0.000244141: 30% violate; best seen 8.19e-08 (2^-23.54)
- sys_p99_batch_us <= 0.44: 42% violate; best seen 0.161

Pareto front (feasible, 22 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1139, accuracy_bits=12.3, luts=855, ffs=285, throughput_msps=93.6, max_abs_err=0.000204 (2^-12.26), power_index=1.37
- pipelined_m [data_width=17 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1207, accuracy_bits=12.6, luts=926, ffs=280, throughput_msps=97.8, max_abs_err=0.000158 (2^-12.63), power_index=1.45
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1298, accuracy_bits=13.3, luts=994, ffs=305, throughput_msps=93.6, max_abs_err=0.000102 (2^-13.26), power_index=1.56
- pipelined_m [data_width=21 n_iter=15 angle_guard=2 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=1458, accuracy_bits=13.7, luts=1053, ffs=406, throughput_msps=114, max_abs_err=7.32e-05 (2^-13.74), power_index=1.76
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=3] luts_plus_ffs=1516, accuracy_bits=14.4, luts=1064, ffs=452, throughput_msps=119, max_abs_err=4.64e-05 (2^-14.39), power_index=1.83
- pipelined_m [data_width=20 n_iter=18 angle_guard=3 frac_guard=4 rounding=round m=4] luts_plus_ffs=1855, accuracy_bits=16.4, luts=1427, ffs=428, throughput_msps=89.6, max_abs_err=1.13e-05 (2^-16.43), power_index=2.23
- pipelined_m [data_width=21 n_iter=19 angle_guard=3 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1920, accuracy_bits=17, luts=1485, ffs=435, throughput_msps=89.6, max_abs_err=7.43e-06 (2^-17.04), power_index=2.31
- pipelined_m [data_width=26 n_iter=20 angle_guard=-1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=2239, accuracy_bits=18.6, luts=1747, ffs=492, throughput_msps=86, max_abs_err=2.51e-06 (2^-18.60), power_index=2.7
- pipelined_m [data_width=25 n_iter=24 angle_guard=4 frac_guard=1 rounding=round m=2] luts_plus_ffs=3282, accuracy_bits=21.2, luts=2167, ffs=1116, throughput_msps=153, max_abs_err=4.27e-07 (2^-21.16), power_index=3.95
- pipelined_m [data_width=27 n_iter=26 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=3383, accuracy_bits=22.7, luts=2486, ffs=897, throughput_msps=110, max_abs_err=1.48e-07 (2^-22.69), power_index=4.07
Front coverage: luts_plus_ffs 1139..3383 (HV reference 4000); accuracy_bits 12.3..22.7 (HV reference 12); data_width on the front 17..27 (registry 8..28).

Per family:
- iterative: 33 evals, 0 feasible; max throughput seen 24.8 MSPS; best accuracy 12.53 bits
- unrolled_k: 67 evals, 0 feasible; max throughput seen 10.5 MSPS; best accuracy 13.92 bits
- pipelined: 50 evals, 27 feasible; max throughput seen 273 MSPS; best accuracy 14.16 bits; best feasible luts_plus_ffs=1744; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 250 evals, 146 feasible; max throughput seen 171 MSPS; best accuracy 23.54 bits; best feasible luts_plus_ffs=1139; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8819 in, 3104 out
- provider-reported cost: $0.0143
- full prompts and replies: `llm_trace.jsonl`

