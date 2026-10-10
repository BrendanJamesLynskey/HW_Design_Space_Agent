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
`pipelined_m:data_width=19,n_iter=14,angle_guard=0,frac_guard=1,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 896 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 303 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.44 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000158 (2^-12.63) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 20.7 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.1e-05 (2^-14.26) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 6.69 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.6 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 98.3 dBc, SNR 82.9 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Every L1-feasible design (236) was simulated at its estimated Fmax (SimPy); 235 pass. Top 5 by the selection rule, L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=19,n_iter=14,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=3` | 0.2973 → 0.3052 | yes |
| `pipelined_m:data_width=19,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=19,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=19,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=4` | 0.3848 → 0.3953 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (34 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=14,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 896 | 303 | 93.6 | 6 | 1.44 | 0.000158 (2^-12.63) | 12.63 |
| 1 | `pipelined_m:data_width=19,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 935 | 297 | 93.6 | 6 | 1.48 | 0.000119 (2^-13.04) | 13.04 |
| 2 | `pipelined_m:data_width=19,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 964 | 303 | 93.6 | 6 | 1.52 | 0.000101 (2^-13.27) | 13.27 |
| 3 | `pipelined_m:data_width=20,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 979 | 311 | 93.6 | 6 | 1.55 | 8.73e-05 (2^-13.48) | 13.48 |
| 4 | `pipelined_m:data_width=19,n_iter=16,angle_guard=1,frac_guard=0,rounding=trunc,m=4` | 1017 | 301 | 93.6 | 6 | 1.59 | 8.56e-05 (2^-13.51) | 13.51 |
| 5 | `pipelined_m:data_width=19,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 1033 | 303 | 93.6 | 6 | 1.61 | 7.43e-05 (2^-13.72) | 13.72 |
| 6 | `pipelined_m:data_width=20,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 1048 | 311 | 93.6 | 6 | 1.64 | 6.06e-05 (2^-14.01) | 14.01 |
| 7 | `pipelined_m:data_width=20,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 1080 | 317 | 93.6 | 6 | 1.68 | 5.62e-05 (2^-14.12) | 14.12 |
| 8 | `pipelined_m:data_width=20,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 1112 | 325 | 93.6 | 6 | 1.73 | 4.27e-05 (2^-14.51) | 14.51 |
| 9 | `pipelined_m:data_width=20,n_iter=16,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1154 | 327 | 93.6 | 6 | 1.78 | 3.91e-05 (2^-14.64) | 14.64 |
| 10 | `pipelined_m:data_width=19,n_iter=18,angle_guard=2,frac_guard=0,rounding=round,m=4` | 1170 | 371 | 93.6 | 7 | 1.85 | 3.86e-05 (2^-14.66) | 14.66 |
| 11 | `pipelined_m:data_width=20,n_iter=17,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 1169 | 391 | 93.6 | 7 | 1.88 | 3.57e-05 (2^-14.78) | 14.78 |
| 12 | `pipelined_m:data_width=20,n_iter=17,angle_guard=1,frac_guard=0,rounding=round,m=3` | 1135 | 452 | 119.3 | 8 | 1.91 | 3.32e-05 (2^-14.88) | 14.88 |
| 13 | `pipelined_m:data_width=20,n_iter=18,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 1259 | 397 | 93.6 | 7 | 1.99 | 2.4e-05 (2^-15.35) | 15.35 |
| 14 | `pipelined_m:data_width=20,n_iter=18,angle_guard=2,frac_guard=1,rounding=round,m=4` | 1301 | 399 | 93.6 | 7 | 2.05 | 1.89e-05 (2^-15.69) | 15.69 |
| 15 | `pipelined_m:data_width=22,n_iter=19,angle_guard=2,frac_guard=4,rounding=trunc,m=4` | 1561 | 455 | 89.6 | 7 | 2.43 | 6.07e-06 (2^-17.33) | 17.33 |
| 16 | `pipelined_m:data_width=23,n_iter=19,angle_guard=2,frac_guard=3,rounding=trunc,m=3` | 1580 | 634 | 114.5 | 9 | 2.66 | 4.84e-06 (2^-17.66) | 17.66 |
| 17 | `pipelined_m:data_width=23,n_iter=19,angle_guard=3,frac_guard=3,rounding=trunc,m=3` | 1599 | 641 | 114.5 | 9 | 2.7 | 4.49e-06 (2^-17.76) | 17.76 |
| 18 | `pipelined_m:data_width=25,n_iter=19,angle_guard=2,frac_guard=1,rounding=trunc,m=3` | 1618 | 656 | 110.0 | 9 | 2.74 | 4.2e-06 (2^-17.86) | 17.86 |
| 19 | `pipelined_m:data_width=25,n_iter=19,angle_guard=2,frac_guard=1,rounding=round,m=3` | 1670 | 658 | 110.0 | 9 | 2.8 | 4.01e-06 (2^-17.93) | 17.93 |
| 20 | `pipelined_m:data_width=25,n_iter=20,angle_guard=1,frac_guard=2,rounding=round,m=3` | 1780 | 663 | 110.0 | 9 | 2.94 | 2.27e-06 (2^-18.75) | 18.75 |
| 21 | `pipelined_m:data_width=28,n_iter=20,angle_guard=-2,frac_guard=0,rounding=round,m=3` | 1767 | 685 | 110.0 | 9 | 2.95 | 2.26e-06 (2^-18.76) | 18.76 |
| 22 | `pipelined_m:data_width=26,n_iter=23,angle_guard=0,frac_guard=0,rounding=round,m=4` | 1953 | 567 | 89.6 | 8 | 3.03 | 7.26e-07 (2^-20.39) | 20.39 |
| 23 | `pipelined_m:data_width=27,n_iter=24,angle_guard=-1,frac_guard=1,rounding=trunc,m=3` | 2138 | 771 | 110.0 | 10 | 3.5 | 6.51e-07 (2^-20.55) | 20.55 |
| 24 | `pipelined_m:data_width=25,n_iter=23,angle_guard=4,frac_guard=4,rounding=trunc,m=3` | 2161 | 801 | 110.0 | 10 | 3.57 | 3.97e-07 (2^-21.26) | 21.26 |
| 25 | `pipelined_m:data_width=26,n_iter=23,angle_guard=2,frac_guard=4,rounding=trunc,m=3` | 2184 | 811 | 110.0 | 10 | 3.61 | 3.57e-07 (2^-21.42) | 21.42 |
| 26 | `pipelined_m:data_width=27,n_iter=24,angle_guard=0,frac_guard=1,rounding=round,m=3` | 2219 | 781 | 110.0 | 10 | 3.61 | 3.47e-07 (2^-21.46) | 21.46 |
| 27 | `pipelined_m:data_width=28,n_iter=23,angle_guard=0,frac_guard=3,rounding=trunc,m=3` | 2231 | 833 | 105.9 | 10 | 3.69 | 3.2e-07 (2^-21.58) | 21.58 |
| 28 | `pipelined_m:data_width=28,n_iter=23,angle_guard=0,frac_guard=3,rounding=round,m=3` | 2290 | 835 | 105.9 | 10 | 3.76 | 3.13e-07 (2^-21.61) | 21.61 |
| 29 | `pipelined_m:data_width=27,n_iter=24,angle_guard=0,frac_guard=4,rounding=trunc,m=3` | 2308 | 821 | 105.9 | 10 | 3.77 | 3.09e-07 (2^-21.63) | 21.63 |
| 30 | `pipelined_m:data_width=27,n_iter=24,angle_guard=2,frac_guard=3,rounding=trunc,m=3` | 2308 | 823 | 110.0 | 10 | 3.77 | 1.93e-07 (2^-22.30) | 22.30 |
| 31 | `pipelined_m:data_width=27,n_iter=24,angle_guard=2,frac_guard=4,rounding=trunc,m=3` | 2356 | 837 | 105.9 | 10 | 3.84 | 1.85e-07 (2^-22.36) | 22.36 |
| 32 | `pipelined_m:data_width=27,n_iter=24,angle_guard=2,frac_guard=4,rounding=round,m=3` | 2413 | 839 | 105.9 | 10 | 3.92 | 1.68e-07 (2^-22.51) | 22.51 |
| 33 | `pipelined_m:data_width=27,n_iter=26,angle_guard=2,frac_guard=1,rounding=round,m=3` | 2459 | 890 | 110.0 | 11 | 4.03 | 1.67e-07 (2^-22.51) | 22.51 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The two hard system constraints force the architecture: throughput>=32 msps and sys_p99_batch<=0.44us mean 32 results must be produced within 0.44us of a tick, i.e. ~14 cycles. Only the 1-result/cycle families (pipelined, pipelined_m) can do that; iterative and unrolled_k emit one result every several cycles and would queue the burst, blowing the p99 batch bound, so they are excluded. The accuracy constraint (max_abs_err<=2^-12) depends only on data_width/n_iter/guards/rounding, so I bound data_width 14-20 and n_iter 12-18 to bracket the feasible accuracy region without wasting evals on grossly over- or under-accurate corners. The trade-off to map is area (luts_plus_ffs, the objective and selection rule) vs Fmax (needed to meet the batch deadline) vs accuracy_bits: pipelined gives the highest Fmax (safest for the deadline) at higher FF cost, while pipelined_m trades Fmax for lower FFs. Searching both with equal weight lets NSGA-II map the full front between the Fmax-limited and area-limited corners, which is what the hypervolume rewards. I split the budget evenly (0.5/0.5) since both families are plausible front members and the selection rule will pick the cheapest passing design, which could come from either.*)
- `pipelined` (50 evals): data_width=14..20, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* 1 result/cycle is the only way to plausibly clear the 32 req/us throughput and the 0.44us p99 batch bound (32 back-to-back results must fit in 0.44us, i.e. ~14 cycles at the clock). Full pipeline gives the best Fmax of the 1/cycle families, which is what the tight batch deadline needs. data_width 14-20 and n_iter 12-18 bracket the max_abs_err<=2^-12 constraint (accuracy depends only on these + guards + rounding), so the search can find the cheapest width/iter that meets it while the cost model trades area vs Fmax.
- `pipelined_m` (50 evals): data_width=14..20, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Same 1 result/cycle throughput as pipelined, but registering only every m stages cuts FFs (the dominant term in luts_plus_ffs, the selection objective) at the cost of a longer combinational path (lower Fmax). Since the batch deadline is tight, m is capped at 2-4 so Fmax can still clear it; this family likely owns the low-area corner of the front that the selection rule (min luts_plus_ffs) will pick, so it must be on the front.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 66 feasible; hypervolume 8580 (n/a).

**LLM decision:** `refine` — The current front is dominated by `pipelined_m` with `m=3` and `data_width` 18-20. The best area (1274 LUT+FF) is at `data_width=18, n_iter=15, m=3`. The `pipelined` family is less efficient (best 1810 vs 1274). The accuracy constraint (max_abs_err <= 2^-12) is easily met by the current front (best 2^-15.4), but the area objective is the primary driver for the selection rule. To improve hypervolume and find a potentially better trade-off, I should focus the search on the `pipelined_m` family where the best designs are found. I will narrow the ranges to `data_width` 17-20, `n_iter` 14-18, `angle_guard` 0-2, `frac_guard` 0-1, and `m` 2-4. This focuses the budget on the region that has already proven to be the most efficient, allowing Optuna to refine the Pareto front within this high-probability zone. I will exclude `pipelined` as it is strictly worse in area for similar accuracy, and `iterative`/`unrolled_k` are unlikely to beat the pipelined throughput/area trade-off for this high-throughput requirement (32 MSPS) without significant area overhead or latency issues that might violate the system constraints if not carefully tuned, but `pipelined_m` is already meeting them comfortably.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 8580 (gain this round: n/a (first round)).
Feasible designs: 66 of 100 evaluations (52 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 34% violate; best seen 2.32e-05 (2^-15.40)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.161

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1274, accuracy_bits=13.2, luts=920, ffs=354, throughput_msps=119, max_abs_err=0.000109 (2^-13.17), power_index=1.53
- pipelined_m [data_width=19 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1335, accuracy_bits=13.6, luts=964, ffs=371, throughput_msps=119, max_abs_err=8.33e-05 (2^-13.55), power_index=1.61
- pipelined_m [data_width=18 n_iter=17 angle_guard=2 frac_guard=0 rounding=round m=3] luts_plus_ffs=1468, accuracy_bits=13.7, luts=1051, ffs=418, throughput_msps=119, max_abs_err=7.75e-05 (2^-13.65), power_index=1.77
- pipelined_m [data_width=19 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1469, accuracy_bits=13.7, luts=1033, ffs=436, throughput_msps=119, max_abs_err=7.43e-05 (2^-13.72), power_index=1.77
- pipelined_m [data_width=19 n_iter=17 angle_guard=0 frac_guard=0 rounding=round m=3] luts_plus_ffs=1493, accuracy_bits=13.9, luts=1067, ffs=426, throughput_msps=119, max_abs_err=6.32e-05 (2^-13.95), power_index=1.8
- pipelined_m [data_width=19 n_iter=18 angle_guard=2 frac_guard=0 rounding=round m=4] luts_plus_ffs=1541, accuracy_bits=14.7, luts=1170, ffs=371, throughput_msps=93.6, max_abs_err=3.86e-05 (2^-14.66), power_index=1.85
- pipelined_m [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=round m=3] luts_plus_ffs=1587, accuracy_bits=14.9, luts=1135, ffs=452, throughput_msps=119, max_abs_err=3.32e-05 (2^-14.88), power_index=1.91
- pipelined_m [data_width=20 n_iter=17 angle_guard=2 frac_guard=0 rounding=round m=2] luts_plus_ffs=1819, accuracy_bits=15.1, luts=1152, ffs=667, throughput_msps=164, max_abs_err=2.85e-05 (2^-15.10), power_index=2.19
- pipelined_m [data_width=20 n_iter=17 angle_guard=1 frac_guard=2 rounding=round m=2] luts_plus_ffs=1937, accuracy_bits=15.4, luts=1244, ffs=692, throughput_msps=164, max_abs_err=2.32e-05 (2^-15.40), power_index=2.33
Front coverage: luts_plus_ffs 1274..1937 (HV reference 4000); accuracy_bits 13.2..15.4 (HV reference 12); data_width on the front 18..20 (registry 8..28).

Per family:
- pipelined: 50 evals, 30 feasible; max throughput seen 273 MSPS; best accuracy 15.14 bits; best feasible luts_plus_ffs=1810; feasible ranges: data_width 17..19, n_iter 15..17, angle_guard 0..2, frac_guard 1..2
- pipelined_m: 50 evals, 36 feasible; max throughput seen 171 MSPS; best accuracy 15.40 bits; best feasible luts_plus_ffs=1274; feasible ranges: data_width 18..20, n_iter 14..18, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Refine the search space to the promising region of pipelined_m to maximize hypervolume improvement within the remaining budget.*)
- `pipelined_m` (100 evals): data_width=17..20, n_iter=14..18, angle_guard=0..2, frac_guard=0..1, rounding=trunc|round, m=2..4. *Why:* Focus on the most efficient family and parameter region identified in Round 1 to refine the Pareto front and potentially lower the minimum area or improve accuracy at the same area.

**Result (code):** 100 evaluations this round, 200 total; 162 feasible; hypervolume 9584 (+11.7%).

**LLM decision:** `add_family` — The current front is dominated by pipelined_m designs with a minimum area of 1198 LUTs+FFs. However, the spec requires a throughput of 32 MSPS and a p99 batch latency of 0.44 us. While pipelined_m meets these, the iterative and unrolled_k families have not been explored. Iterative CORDIC typically has a much smaller area footprint (shared datapath) than pipelined versions. Although iterative has a latency of N+3 cycles, if N is small (e.g., 14-16), the latency is ~17-19 cycles. At a high Fmax (e.g., 200+ MHz), 19 cycles is ~95 ns, which is well within the 440 ns budget. The throughput constraint is 32 MSPS; iterative produces 1 result every N+3 cycles. If N=15, it takes 18 cycles. To achieve 32 MSPS, the clock must be at least 32 * 18 = 576 MHz, which is likely infeasible on Artix-7. Wait, let's re-evaluate. The constraint is throughput_msps >= 32. For iterative, throughput = Fmax / (N+3). If Fmax is ~200 MHz, and N=15, throughput = 200/18 = 11 MSPS. This violates the constraint. Unrolled_k with k=4 or 8 might work. If k=8, cycles = ceil(N/8)+3. If N=16, cycles = 2+3=5. Throughput = Fmax/5. If Fmax=200, throughput=40 MSPS. This meets the constraint. Unrolled_k often has lower area than pipelined_m for the same throughput because it reuses logic more aggressively than a full pipeline but faster than iterative. The current best pipelined_m is 1198. Unrolled_k might offer a better area/throughput trade-off. We should explore unrolled_k to see if it can beat 1198 LUTs+FFs while meeting the 32 MSPS and latency constraints.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 9584 (gain this round: +11.7%).
Feasible designs: 162 of 200 evaluations (122 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 19% violate; best seen 1.89e-05 (2^-15.69)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.161

Pareto front (feasible, 15 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1198, accuracy_bits=12.6, luts=896, ffs=303, throughput_msps=93.6, max_abs_err=0.000158 (2^-12.63), power_index=1.44
- pipelined_m [data_width=19 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1267, accuracy_bits=13.3, luts=964, ffs=303, throughput_msps=93.6, max_abs_err=0.000101 (2^-13.27), power_index=1.52
- pipelined_m [data_width=20 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1290, accuracy_bits=13.5, luts=979, ffs=311, throughput_msps=93.6, max_abs_err=8.73e-05 (2^-13.48), power_index=1.55
- pipelined_m [data_width=19 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1335, accuracy_bits=13.7, luts=1033, ffs=303, throughput_msps=93.6, max_abs_err=7.43e-05 (2^-13.72), power_index=1.61
- pipelined_m [data_width=20 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1359, accuracy_bits=14, luts=1048, ffs=311, throughput_msps=93.6, max_abs_err=6.06e-05 (2^-14.01), power_index=1.64
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1437, accuracy_bits=14.5, luts=1112, ffs=325, throughput_msps=93.6, max_abs_err=4.27e-05 (2^-14.51), power_index=1.73
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1481, accuracy_bits=14.6, luts=1154, ffs=327, throughput_msps=93.6, max_abs_err=3.91e-05 (2^-14.64), power_index=1.78
- pipelined_m [data_width=20 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1560, accuracy_bits=14.8, luts=1169, ffs=391, throughput_msps=93.6, max_abs_err=3.57e-05 (2^-14.78), power_index=1.88
- pipelined_m [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=round m=3] luts_plus_ffs=1587, accuracy_bits=14.9, luts=1135, ffs=452, throughput_msps=119, max_abs_err=3.32e-05 (2^-14.88), power_index=1.91
- pipelined_m [data_width=20 n_iter=18 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1700, accuracy_bits=15.7, luts=1301, ffs=399, throughput_msps=93.6, max_abs_err=1.89e-05 (2^-15.69), power_index=2.05
Front coverage: luts_plus_ffs 1198..1700 (HV reference 4000); accuracy_bits 12.6..15.7 (HV reference 12); data_width on the front 19..20 (registry 8..28).

Per family:
- pipelined: 50 evals, 30 feasible; max throughput seen 273 MSPS; best accuracy 15.14 bits; best feasible luts_plus_ffs=1810; feasible ranges: data_width 17..19, n_iter 15..17, angle_guard 0..2, frac_guard 1..2
- pipelined_m: 150 evals, 132 feasible; max throughput seen 171 MSPS; best accuracy 15.69 bits; best feasible luts_plus_ffs=1198; feasible ranges: data_width 17..20, n_iter 14..18, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Add unrolled_k family to explore potential area savings over pipelined_m while maintaining required throughput and latency.*)
- `unrolled_k` (40 evals): data_width=16..22, n_iter=12..20, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=4..8. *Why:* Explore unrolled_k to find designs with lower area than pipelined_m (1198) that still meet the 32 MSPS throughput and 0.44 us latency constraints. k=4..8 allows for high throughput with moderate latency.

**Result (code):** 40 evaluations this round, 240 total; 162 feasible; hypervolume 9584 (+0.0%).

**LLM decision:** `stop` — The Pareto front is well-established and stable (HV gain +0.0% in Round 3). The `pipelined_m` family dominates the feasible space, providing designs that comfortably meet the strict system constraint (sys_p99_batch_us <= 0.44 us) and throughput (>= 32 MSPS) while achieving the required accuracy (max_abs_err <= 2^-12). The current front spans a useful trade-off from 1198 LUTs+FFs (12.6 bits accuracy) to 1700 LUTs+FFs (15.7 bits accuracy). Since this is the final round and the front has converged, further exploration would not significantly improve the hypervolume or the final selection (min luts_plus_ffs), which is already identified at the 1198 LUTs+FFs point.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 9584 (gain this round: +0.0%).
Feasible designs: 162 of 240 evaluations (122 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 17% violate; best seen 273
- max_abs_err <= 0.000244141: 20% violate; best seen 1.52e-05 (2^-16.01)
- sys_p99_batch_us <= 0.44: 17% violate; best seen 0.161

Pareto front (feasible, 15 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1198, accuracy_bits=12.6, luts=896, ffs=303, throughput_msps=93.6, max_abs_err=0.000158 (2^-12.63), power_index=1.44
- pipelined_m [data_width=19 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1267, accuracy_bits=13.3, luts=964, ffs=303, throughput_msps=93.6, max_abs_err=0.000101 (2^-13.27), power_index=1.52
- pipelined_m [data_width=20 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1290, accuracy_bits=13.5, luts=979, ffs=311, throughput_msps=93.6, max_abs_err=8.73e-05 (2^-13.48), power_index=1.55
- pipelined_m [data_width=19 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1335, accuracy_bits=13.7, luts=1033, ffs=303, throughput_msps=93.6, max_abs_err=7.43e-05 (2^-13.72), power_index=1.61
- pipelined_m [data_width=20 n_iter=16 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1359, accuracy_bits=14, luts=1048, ffs=311, throughput_msps=93.6, max_abs_err=6.06e-05 (2^-14.01), power_index=1.64
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1437, accuracy_bits=14.5, luts=1112, ffs=325, throughput_msps=93.6, max_abs_err=4.27e-05 (2^-14.51), power_index=1.73
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1481, accuracy_bits=14.6, luts=1154, ffs=327, throughput_msps=93.6, max_abs_err=3.91e-05 (2^-14.64), power_index=1.78
- pipelined_m [data_width=20 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1560, accuracy_bits=14.8, luts=1169, ffs=391, throughput_msps=93.6, max_abs_err=3.57e-05 (2^-14.78), power_index=1.88
- pipelined_m [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=round m=3] luts_plus_ffs=1587, accuracy_bits=14.9, luts=1135, ffs=452, throughput_msps=119, max_abs_err=3.32e-05 (2^-14.88), power_index=1.91
- pipelined_m [data_width=20 n_iter=18 angle_guard=2 frac_guard=1 rounding=round m=4] luts_plus_ffs=1700, accuracy_bits=15.7, luts=1301, ffs=399, throughput_msps=93.6, max_abs_err=1.89e-05 (2^-15.69), power_index=2.05
Front coverage: luts_plus_ffs 1198..1700 (HV reference 4000); accuracy_bits 12.6..15.7 (HV reference 12); data_width on the front 19..20 (registry 8..28).

Per family:
- unrolled_k: 40 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 16.01 bits
- pipelined: 50 evals, 30 feasible; max throughput seen 273 MSPS; best accuracy 15.14 bits; best feasible luts_plus_ffs=1810; feasible ranges: data_width 17..19, n_iter 15..17, angle_guard 0..2, frac_guard 1..2
- pipelined_m: 150 evals, 132 feasible; max throughput seen 171 MSPS; best accuracy 15.69 bits; best feasible luts_plus_ffs=1198; feasible ranges: data_width 17..20, n_iter 14..18, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (160 evals): data_width=18..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (15 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 288 feasible; hypervolume 1.961e+04 (+104.6%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and stable (HV gain +0.0% in Round 3). The `pipelined_m` family dominates the feasible space, providing designs that comfortably meet the strict system constraint (sys_p99_batch_us <= 0.44 us) and throughput (>= 32 MSPS) while achieving the required accuracy (max_abs_err <= 2^-12). The current front spans a useful trade-off from 1198 LUTs+FFs (12.6 bits accuracy) to 1700 LUTs+FFs (15.7 bits accuracy). Since this is the final round and the front has converged, further exploration would not significantly improve the hypervolume or the final selection (min luts_plus_ffs), which is already identified at the 1198 LUTs+FFs point.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.961e+04 (gain this round: +104.6%).
Feasible designs: 288 of 400 evaluations (236 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 10% violate; best seen 273
- max_abs_err <= 0.000244141: 14% violate; best seen 1.31e-07 (2^-22.87)
- sys_p99_batch_us <= 0.44: 18% violate; best seen 0.161

Pareto front (feasible, 34 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1198, accuracy_bits=12.6, luts=896, ffs=303, throughput_msps=93.6, max_abs_err=0.000158 (2^-12.63), power_index=1.44
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1318, accuracy_bits=13.5, luts=1017, ffs=301, throughput_msps=93.6, max_abs_err=8.56e-05 (2^-13.51), power_index=1.59
- pipelined_m [data_width=20 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1397, accuracy_bits=14.1, luts=1080, ffs=317, throughput_msps=93.6, max_abs_err=5.62e-05 (2^-14.12), power_index=1.68
- pipelined_m [data_width=20 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1560, accuracy_bits=14.8, luts=1169, ffs=391, throughput_msps=93.6, max_abs_err=3.57e-05 (2^-14.78), power_index=1.88
- pipelined_m [data_width=22 n_iter=19 angle_guard=2 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=2016, accuracy_bits=17.3, luts=1561, ffs=455, throughput_msps=89.6, max_abs_err=6.07e-06 (2^-17.33), power_index=2.43
- pipelined_m [data_width=25 n_iter=19 angle_guard=2 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=2273, accuracy_bits=17.9, luts=1618, ffs=656, throughput_msps=110, max_abs_err=4.2e-06 (2^-17.86), power_index=2.74
- pipelined_m [data_width=26 n_iter=23 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=2520, accuracy_bits=20.4, luts=1953, ffs=567, throughput_msps=89.6, max_abs_err=7.26e-07 (2^-20.39), power_index=3.03
- pipelined_m [data_width=27 n_iter=24 angle_guard=0 frac_guard=1 rounding=round m=3] luts_plus_ffs=3000, accuracy_bits=21.5, luts=2219, ffs=781, throughput_msps=110, max_abs_err=3.47e-07 (2^-21.46), power_index=3.61
- pipelined_m [data_width=27 n_iter=24 angle_guard=0 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=3129, accuracy_bits=21.6, luts=2308, ffs=821, throughput_msps=106, max_abs_err=3.09e-07 (2^-21.63), power_index=3.77
- pipelined_m [data_width=27 n_iter=26 angle_guard=2 frac_guard=1 rounding=round m=3] luts_plus_ffs=3349, accuracy_bits=22.5, luts=2459, ffs=890, throughput_msps=110, max_abs_err=1.67e-07 (2^-22.51), power_index=4.03
Front coverage: luts_plus_ffs 1198..3349 (HV reference 4000); accuracy_bits 12.6..22.5 (HV reference 12); data_width on the front 19..28 (registry 8..28).

Per family:
- unrolled_k: 40 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 16.01 bits
- pipelined: 50 evals, 30 feasible; max throughput seen 273 MSPS; best accuracy 15.14 bits; best feasible luts_plus_ffs=1810; feasible ranges: data_width 17..19, n_iter 15..17, angle_guard 0..2, frac_guard 1..2
- pipelined_m: 310 evals, 258 feasible; max throughput seen 171 MSPS; best accuracy 22.87 bits; best feasible luts_plus_ffs=1198; feasible ranges: data_width 17..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 12752 in, 2735 out
- provider-reported cost: $0.0079
- full prompts and replies: `llm_trace.jsonl`

