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
`pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 834 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 270 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 61.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.33 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000209 (2^-12.22) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.43 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 6.44e-05 (2^-13.92) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 1.06 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.2 | exact: bit-accurate model, exhaustive (65536 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 93.3 dBc, SNR 81.1 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=22,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 0.4016 → 0.4126 | yes |
| `pipelined_m:data_width=22,n_iter=15,angle_guard=0,frac_guard=1,rounding=round,m=4` | 0.4016 → 0.4126 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (19 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=4` | 834 | 270 | 97.8 | 6 | 1.33 | 0.000209 (2^-12.22) | 12.22 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round,m=4` | 855 | 291 | 93.6 | 6 | 1.38 | 0.00017 (2^-12.53) | 12.53 |
| 2 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=4` | 920 | 291 | 93.6 | 6 | 1.46 | 0.000109 (2^-13.17) | 13.17 |
| 3 | `pipelined_m:data_width=22,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 1097 | 345 | 89.6 | 6 | 1.74 | 6.63e-05 (2^-13.88) | 13.88 |
| 4 | `pipelined_m:data_width=22,n_iter=15,angle_guard=0,frac_guard=1,rounding=round,m=4` | 1143 | 347 | 89.6 | 6 | 1.79 | 6.41e-05 (2^-13.93) | 13.93 |
| 5 | `pipelined_m:data_width=18,n_iter=18,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1190 | 364 | 93.6 | 7 | 1.87 | 5.02e-05 (2^-14.28) | 14.28 |
| 6 | `pipelined_m:data_width=19,n_iter=18,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1246 | 381 | 93.6 | 7 | 1.96 | 3.09e-05 (2^-14.98) | 14.98 |
| 7 | `pipelined_m:data_width=23,n_iter=17,angle_guard=-2,frac_guard=0,rounding=trunc,m=3` | 1236 | 494 | 114.5 | 8 | 2.08 | 2.36e-05 (2^-15.37) | 15.37 |
| 8 | `pipelined_m:data_width=19,n_iter=18,angle_guard=4,frac_guard=3,rounding=round,m=4` | 1353 | 408 | 89.6 | 7 | 2.12 | 1.49e-05 (2^-16.03) | 16.03 |
| 9 | `pipelined_m:data_width=23,n_iter=18,angle_guard=-1,frac_guard=1,rounding=trunc,m=4` | 1367 | 433 | 89.6 | 7 | 2.17 | 1.27e-05 (2^-16.26) | 16.26 |
| 10 | `pipelined_m:data_width=20,n_iter=18,angle_guard=4,frac_guard=3,rounding=round,m=4` | 1409 | 425 | 89.6 | 7 | 2.21 | 1.09e-05 (2^-16.49) | 16.49 |
| 11 | `pipelined_m:data_width=22,n_iter=18,angle_guard=4,frac_guard=4,rounding=round,m=4` | 1556 | 467 | 89.6 | 7 | 2.44 | 8.31e-06 (2^-16.88) | 16.88 |
| 12 | `pipelined_m:data_width=22,n_iter=21,angle_guard=0,frac_guard=1,rounding=round,m=4` | 1611 | 498 | 89.6 | 8 | 2.54 | 7.37e-06 (2^-17.05) | 17.05 |
| 13 | `pipelined_m:data_width=24,n_iter=21,angle_guard=-1,frac_guard=0,rounding=round,m=4` | 1628 | 521 | 89.6 | 8 | 2.59 | 3.92e-06 (2^-17.96) | 17.96 |
| 14 | `pipelined_m:data_width=22,n_iter=21,angle_guard=4,frac_guard=3,rounding=round,m=4` | 1780 | 543 | 89.6 | 8 | 2.8 | 1.9e-06 (2^-19.01) | 19.01 |
| 15 | `pipelined_m:data_width=26,n_iter=23,angle_guard=-1,frac_guard=1,rounding=trunc,m=3` | 1976 | 745 | 110.0 | 10 | 3.27 | 1.05e-06 (2^-19.86) | 19.86 |
| 16 | `pipelined_m:data_width=26,n_iter=23,angle_guard=2,frac_guard=1,rounding=round,m=3` | 2100 | 771 | 110.0 | 10 | 3.46 | 4.4e-07 (2^-21.12) | 21.12 |
| 17 | `pipelined_m:data_width=28,n_iter=28,angle_guard=2,frac_guard=3,rounding=round,m=3` | 2852 | 1051 | 105.9 | 12 | 4.7 | 4.38e-08 (2^-24.45) | 24.45 |
| 18 | `pipelined_m:data_width=28,n_iter=28,angle_guard=2,frac_guard=4,rounding=round,m=3` | 2909 | 1069 | 105.9 | 12 | 4.79 | 4.07e-08 (2^-24.55) | 24.55 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 Msps throughput (32 results per 1us tick) and all 32 results back within 440 ns p99. Only pipelined and pipelined_m families produce 1 result/cycle, making them the only plausible candidates for the throughput constraint. Iterative (1 result per N+3 cycles) and unrolled_k (1 result per ceil(N/k)+3 cycles) would need k>=32 or N very small to meet 32 Msps, which is impractical or area-prohibitive. For accuracy, max_abs_err <= 2^-12 requires roughly 12+ bits of accuracy; data_width 14-18 with n_iter 12-18 and modest guards should cover this range. I focus the budget on pipelined and pipelined_m to map the area vs accuracy trade-off, with pipelined_m likely offering lower FF counts. The 440 ns p99 batch constraint is easily met by both families given their low latencies (5-20 cycles at 200+ MHz). I allocate budget equally between the two families to explore the full trade-off surface, as pipelined_m with m>1 may dominate pipelined on area while maintaining throughput.*)
- `pipelined` (50 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* 1 result/cycle meets the 32 Msps throughput constraint. With N=12-18 iterations, latency is 14-20 cycles. At Fmax ~200-300 MHz, latency is ~50-100 ns, well within the 440 ns p99 batch window. Data width 14-18 with appropriate guards should achieve 12+ bits accuracy. This is the primary candidate for the Pareto front.
- `pipelined_m` (50 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Registering every m stages (m=2-4) reduces FF count versus fully pipelined while maintaining 1 result/cycle throughput. Latency is ceil(N/m)+2 cycles, which for N=12-18 and m=2-4 gives 5-11 cycles, even shorter than fully pipelined. This family may offer a better area/latency trade-off and could dominate pipelined on luts_plus_ffs.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 59 feasible; hypervolume 6074 (n/a).

**LLM decision:** `add_family` — The current front is dominated by pipelined_m with a minimum area of 1104 LUTs+FFs. The `iterative` family is unexplored and typically has a much smaller area footprint (shared datapath, no pipeline registers) than pipelined architectures. Since the throughput constraint (>= 32 MSPS) is easily met by pipelined designs (best seen 273 MSPS) and `iterative` can achieve high throughput with high `n_iter` or by operating at a higher Fmax, it is a strong candidate to push the area objective lower. We will explore `iterative` to see if it can beat the 1104 area floor while maintaining the required accuracy (>= 12 bits) and system latency.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 6074 (gain this round: n/a (first round)).
Feasible designs: 59 of 100 evaluations (33 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 41% violate; best seen 5.02e-05 (2^-14.28)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.161

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1104, accuracy_bits=12.2, luts=834, ffs=270, throughput_msps=97.8, max_abs_err=0.000209 (2^-12.22), power_index=1.33
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1145, accuracy_bits=12.5, luts=855, ffs=291, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.53), power_index=1.38
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1210, accuracy_bits=13.2, luts=920, ffs=291, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=1.46
- pipelined_m [data_width=18 n_iter=18 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1447, accuracy_bits=13.4, luts=1098, ffs=349, throughput_msps=93.6, max_abs_err=9.26e-05 (2^-13.40), power_index=1.74
- pipelined_m [data_width=18 n_iter=18 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1470, accuracy_bits=13.7, luts=1116, ffs=354, throughput_msps=93.6, max_abs_err=7.75e-05 (2^-13.65), power_index=1.77
- pipelined_m [data_width=18 n_iter=18 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1554, accuracy_bits=14.3, luts=1190, ffs=364, throughput_msps=93.6, max_abs_err=5.02e-05 (2^-14.28), power_index=1.87
Front coverage: luts_plus_ffs 1104..1554 (HV reference 4000); accuracy_bits 12.2..14.3 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 50 evals, 26 feasible; max throughput seen 273 MSPS; best accuracy 13.81 bits; best feasible luts_plus_ffs=1818; feasible ranges: data_width 17..18, n_iter 15..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 33 feasible; max throughput seen 171 MSPS; best accuracy 14.28 bits; best feasible luts_plus_ffs=1104; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 0..2, frac_guard 0..1, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Adding the iterative family to check if it can achieve the required accuracy and throughput with a significantly lower area than the current pipelined_m front (1104 LUTs+FFs).*)
- `iterative` (100 evals): data_width=14..18, n_iter=12..20, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* Exploring the iterative family to find lower-area designs. The ranges are centered on the data_widths (16-18) that provided good accuracy in the pipelined front, but extended to 14 to allow for lower area if accuracy can be compensated by n_iter. Rounding is fixed to 'round' as it is generally superior for accuracy.

**Result (code):** 100 evaluations this round, 200 total; 59 feasible; hypervolume 6074 (+0.0%).

**LLM decision:** `add_family` — The current Pareto front is dominated by pipelined_m designs (1104-1554 luts_plus_ffs). The iterative family failed the throughput constraint (max 13.2 MSPS < 32), and pipelined is significantly more expensive (min 1818 luts_plus_ffs) than pipelined_m. However, unrolled_k has not been explored. With k=2..8, unrolled_k can achieve high throughput (potentially matching or exceeding pipelined_m) while using a shared datapath that might be more area-efficient than the full pipelined_m register stages, especially for lower n_iter. Exploring unrolled_k is necessary to ensure we haven't missed a cheaper solution on the Pareto front before finalizing the design space.
- **rule applied by code:** 'add_family' overridden to stop: HV gain 0.00% < epsilon 1.00%
- **rule applied by code:** code: before stopping (converged), one front-mapping round with the remaining 200 evaluations
- effective decision: `stop`

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 6074 (gain this round: +0.0%).
Feasible designs: 59 of 200 evaluations (33 unique).
Families explored so far: iterative, pipelined, pipelined_m. Not yet explored: unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 50% violate; best seen 273
- max_abs_err <= 0.000244141: 57% violate; best seen 3.99e-05 (2^-14.61)
- sys_p99_batch_us <= 0.44: 50% violate; best seen 0.161

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1104, accuracy_bits=12.2, luts=834, ffs=270, throughput_msps=97.8, max_abs_err=0.000209 (2^-12.22), power_index=1.33
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1145, accuracy_bits=12.5, luts=855, ffs=291, throughput_msps=93.6, max_abs_err=0.00017 (2^-12.53), power_index=1.38
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1210, accuracy_bits=13.2, luts=920, ffs=291, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=1.46
- pipelined_m [data_width=18 n_iter=18 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=1447, accuracy_bits=13.4, luts=1098, ffs=349, throughput_msps=93.6, max_abs_err=9.26e-05 (2^-13.40), power_index=1.74
- pipelined_m [data_width=18 n_iter=18 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1470, accuracy_bits=13.7, luts=1116, ffs=354, throughput_msps=93.6, max_abs_err=7.75e-05 (2^-13.65), power_index=1.77
- pipelined_m [data_width=18 n_iter=18 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1554, accuracy_bits=14.3, luts=1190, ffs=364, throughput_msps=93.6, max_abs_err=5.02e-05 (2^-14.28), power_index=1.87
Front coverage: luts_plus_ffs 1104..1554 (HV reference 4000); accuracy_bits 12.2..14.3 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- iterative: 100 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 14.61 bits
- pipelined: 50 evals, 26 feasible; max throughput seen 273 MSPS; best accuracy 13.81 bits; best feasible luts_plus_ffs=1818; feasible ranges: data_width 17..18, n_iter 15..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 33 feasible; max throughput seen 171 MSPS; best accuracy 14.28 bits; best feasible luts_plus_ffs=1104; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 0..2, frac_guard 0..1, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 200 evaluations*)
- `pipelined_m` (200 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (6 front designs; box front_anchored)

**Result (code):** 200 evaluations this round, 400 total; 187 feasible; hypervolume 1.85e+04 (+204.6%).

**No LLM call** (code's front-mapping round): The current Pareto front is dominated by pipelined_m designs (1104-1554 luts_plus_ffs). The iterative family failed the throughput constraint (max 13.2 MSPS < 32), and pipelined is significantly more expensive (min 1818 luts_plus_ffs) than pipelined_m. However, unrolled_k has not been explored. With k=2..8, unrolled_k can achieve high throughput (potentially matching or exceeding pipelined_m) while using a shared datapath that might be more area-efficient than the full pipelined_m register stages, especially for lower n_iter. Exploring unrolled_k is necessary to ensure we haven't missed a cheaper solution on the Pareto front before finalizing the design space.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.85e+04 (gain this round: +204.6%).
Feasible designs: 187 of 400 evaluations (149 unique).
Families explored so far: iterative, pipelined, pipelined_m. Not yet explored: unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 25% violate; best seen 273
- max_abs_err <= 0.000244141: 34% violate; best seen 4.07e-08 (2^-24.55)
- sys_p99_batch_us <= 0.44: 40% violate; best seen 0.161

Pareto front (feasible, 19 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1104, accuracy_bits=12.2, luts=834, ffs=270, throughput_msps=97.8, max_abs_err=0.000209 (2^-12.22), power_index=1.33
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1210, accuracy_bits=13.2, luts=920, ffs=291, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=1.46
- pipelined_m [data_width=22 n_iter=15 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=1490, accuracy_bits=13.9, luts=1143, ffs=347, throughput_msps=89.6, max_abs_err=6.41e-05 (2^-13.93), power_index=1.79
- pipelined_m [data_width=19 n_iter=18 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1627, accuracy_bits=15, luts=1246, ffs=381, throughput_msps=93.6, max_abs_err=3.09e-05 (2^-14.98), power_index=1.96
- pipelined_m [data_width=19 n_iter=18 angle_guard=4 frac_guard=3 rounding=round m=4] luts_plus_ffs=1761, accuracy_bits=16, luts=1353, ffs=408, throughput_msps=89.6, max_abs_err=1.49e-05 (2^-16.03), power_index=2.12
- pipelined_m [data_width=20 n_iter=18 angle_guard=4 frac_guard=3 rounding=round m=4] luts_plus_ffs=1834, accuracy_bits=16.5, luts=1409, ffs=425, throughput_msps=89.6, max_abs_err=1.09e-05 (2^-16.49), power_index=2.21
- pipelined_m [data_width=22 n_iter=21 angle_guard=0 frac_guard=1 rounding=round m=4] luts_plus_ffs=2110, accuracy_bits=17, luts=1611, ffs=498, throughput_msps=89.6, max_abs_err=7.37e-06 (2^-17.05), power_index=2.54
- pipelined_m [data_width=22 n_iter=21 angle_guard=4 frac_guard=3 rounding=round m=4] luts_plus_ffs=2323, accuracy_bits=19, luts=1780, ffs=543, throughput_msps=89.6, max_abs_err=1.9e-06 (2^-19.01), power_index=2.8
- pipelined_m [data_width=26 n_iter=23 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=2871, accuracy_bits=21.1, luts=2100, ffs=771, throughput_msps=110, max_abs_err=4.4e-07 (2^-21.12), power_index=3.46
- pipelined_m [data_width=28 n_iter=28 angle_guard=2 frac_guard=4 rounding=round m=3] luts_plus_ffs=3979, accuracy_bits=24.6, luts=2909, ffs=1069, throughput_msps=106, max_abs_err=4.07e-08 (2^-24.55), power_index=4.79
Front coverage: luts_plus_ffs 1104..3979 (HV reference 4000); accuracy_bits 12.2..24.6 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- iterative: 100 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 14.61 bits
- pipelined: 50 evals, 26 feasible; max throughput seen 273 MSPS; best accuracy 13.81 bits; best feasible luts_plus_ffs=1818; feasible ranges: data_width 17..18, n_iter 15..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 250 evals, 161 feasible; max throughput seen 171 MSPS; best accuracy 24.55 bits; best feasible luts_plus_ffs=1104; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 6 (failed/unparsed attempts: 0)
- tokens: 23074 in, 2512 out
- provider-reported cost: $0.0069
- full prompts and replies: `llm_trace.jsonl`

