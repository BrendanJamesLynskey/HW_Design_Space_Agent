# DSE run: bursty_offload

**Verdict:** converged: hypervolume gain fell below epsilon.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 400 of 400 budgeted, over 3 round(s).  
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
`pipelined_m:data_width=19,n_iter=12,angle_guard=0,frac_guard=0,rounding=trunc,m=7` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 736 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 167 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 56.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 56.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 70.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0679 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000525 (2^-10.90) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 68.8 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 0.0002 (2^-12.29) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 26.2 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 10.9 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 4 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 79.0 dBc, SNR 71.0 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: bursty requests: bursts of 8 (0 ns apart) arriving as a Poisson process, 2 requests/us on average. Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_latency_us <= 0.4 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=19,n_iter=12,angle_guard=0,frac_guard=0,rounding=trunc,m=7` | 0.1759 → 0.245 | yes |
| `pipelined_m:data_width=20,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=6` | 0.1529 → 0.2076 | yes |
| `pipelined_m:data_width=20,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=7` | 0.1759 → 0.245 | yes |
| `pipelined_m:data_width=16,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=7` | 0.1845 → 0.2495 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=8` | 0.199 → 0.2825 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (33 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=12,angle_guard=0,frac_guard=0,rounding=trunc,m=7` | 736 | 167 | 56.8 | 4 | 0.0679 | 0.000525 (2^-10.90) | 10.90 |
| 1 | `pipelined_m:data_width=20,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=6` | 793 | 180 | 65.4 | 4 | 0.0732 | 0.000492 (2^-10.99) | 10.99 |
| 2 | `pipelined_m:data_width=20,n_iter=12,angle_guard=2,frac_guard=0,rounding=round,m=7` | 793 | 180 | 56.8 | 4 | 0.0732 | 0.000492 (2^-10.99) | 10.99 |
| 3 | `pipelined_m:data_width=16,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=7` | 875 | 202 | 59.6 | 5 | 0.081 | 0.000301 (2^-11.70) | 11.70 |
| 4 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=8` | 941 | 159 | 50.3 | 4 | 0.0828 | 0.00013 (2^-12.91) | 12.91 |
| 5 | `pipelined_m:data_width=16,n_iter=15,angle_guard=3,frac_guard=2,rounding=round,m=5` | 939 | 218 | 77.0 | 5 | 0.087 | 0.000128 (2^-12.93) | 12.93 |
| 6 | `pipelined_m:data_width=19,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc,m=8` | 1033 | 172 | 50.3 | 4 | 0.0906 | 8.56e-05 (2^-13.51) | 13.51 |
| 7 | `pipelined_m:data_width=21,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc,m=8` | 1023 | 184 | 50.3 | 4 | 0.0908 | 7.62e-05 (2^-13.68) | 13.68 |
| 8 | `pipelined_m:data_width=20,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,m=6` | 1048 | 243 | 65.4 | 5 | 0.0972 | 5.27e-05 (2^-14.21) | 14.21 |
| 9 | `pipelined_m:data_width=19,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=8` | 1136 | 178 | 50.3 | 4 | 0.0988 | 4.29e-05 (2^-14.51) | 14.51 |
| 10 | `pipelined_m:data_width=20,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=6` | 1080 | 249 | 65.4 | 5 | 0.1 | 4.12e-05 (2^-14.57) | 14.57 |
| 11 | `pipelined_m:data_width=19,n_iter=16,angle_guard=2,frac_guard=3,rounding=round,m=8` | 1168 | 180 | 50.3 | 4 | 0.101 | 3.97e-05 (2^-14.62) | 14.62 |
| 12 | `pipelined_m:data_width=20,n_iter=16,angle_guard=2,frac_guard=1,rounding=round,m=6` | 1154 | 255 | 65.4 | 5 | 0.106 | 3.91e-05 (2^-14.64) | 14.64 |
| 13 | `pipelined_m:data_width=20,n_iter=16,angle_guard=1,frac_guard=2,rounding=round,m=6` | 1170 | 256 | 65.4 | 5 | 0.107 | 3.84e-05 (2^-14.67) | 14.67 |
| 14 | `pipelined_m:data_width=20,n_iter=17,angle_guard=2,frac_guard=2,rounding=round,m=6` | 1261 | 259 | 65.4 | 5 | 0.114 | 2.23e-05 (2^-15.45) | 15.45 |
| 15 | `pipelined_m:data_width=22,n_iter=17,angle_guard=3,frac_guard=1,rounding=round,m=8` | 1350 | 280 | 48.0 | 5 | 0.123 | 1.67e-05 (2^-15.87) | 15.87 |
| 16 | `pipelined_m:data_width=19,n_iter=19,angle_guard=4,frac_guard=2,rounding=round,m=8` | 1392 | 254 | 48.0 | 5 | 0.124 | 1.5e-05 (2^-16.03) | 16.03 |
| 17 | `pipelined_m:data_width=20,n_iter=19,angle_guard=3,frac_guard=1,rounding=round,m=8` | 1394 | 258 | 48.0 | 5 | 0.124 | 1.31e-05 (2^-16.22) | 16.22 |
| 18 | `pipelined_m:data_width=19,n_iter=20,angle_guard=4,frac_guard=3,rounding=round,m=8` | 1507 | 258 | 48.0 | 5 | 0.133 | 1.03e-05 (2^-16.57) | 16.57 |
| 19 | `pipelined_m:data_width=22,n_iter=20,angle_guard=2,frac_guard=2,rounding=round,m=7` | 1613 | 281 | 54.3 | 5 | 0.143 | 4.44e-06 (2^-17.78) | 17.78 |
| 20 | `pipelined_m:data_width=25,n_iter=20,angle_guard=2,frac_guard=2,rounding=trunc,m=8` | 1747 | 313 | 45.9 | 5 | 0.155 | 2.21e-06 (2^-18.79) | 18.79 |
| 21 | `pipelined_m:data_width=25,n_iter=20,angle_guard=4,frac_guard=2,rounding=trunc,m=8` | 1787 | 319 | 45.9 | 5 | 0.158 | 2.12e-06 (2^-18.85) | 18.85 |
| 22 | `pipelined_m:data_width=25,n_iter=20,angle_guard=3,frac_guard=4,rounding=trunc,m=8` | 1847 | 324 | 45.9 | 5 | 0.163 | 2.09e-06 (2^-18.87) | 18.87 |
| 23 | `pipelined_m:data_width=25,n_iter=22,angle_guard=3,frac_guard=1,rounding=trunc,m=8` | 1908 | 312 | 45.9 | 5 | 0.167 | 1e-06 (2^-19.93) | 19.93 |
| 24 | `pipelined_m:data_width=25,n_iter=22,angle_guard=2,frac_guard=2,rounding=trunc,m=6` | 1930 | 402 | 59.9 | 6 | 0.175 | 8.19e-07 (2^-20.22) | 20.22 |
| 25 | `pipelined_m:data_width=26,n_iter=22,angle_guard=4,frac_guard=0,rounding=round,m=6` | 1953 | 412 | 59.9 | 6 | 0.178 | 6.47e-07 (2^-20.56) | 20.56 |
| 26 | `pipelined_m:data_width=27,n_iter=23,angle_guard=3,frac_guard=2,rounding=round,m=8` | 2241 | 340 | 45.9 | 5 | 0.194 | 2.75e-07 (2^-21.79) | 21.79 |
| 27 | `pipelined_m:data_width=27,n_iter=23,angle_guard=3,frac_guard=4,rounding=round,m=8` | 2334 | 348 | 44.0 | 5 | 0.202 | 2.67e-07 (2^-21.84) | 21.84 |
| 28 | `pipelined_m:data_width=26,n_iter=27,angle_guard=4,frac_guard=2,rounding=round,m=8` | 2581 | 426 | 45.9 | 6 | 0.226 | 1.28e-07 (2^-22.89) | 22.89 |
| 29 | `pipelined_m:data_width=27,n_iter=26,angle_guard=3,frac_guard=2,rounding=trunc,m=5` | 2482 | 626 | 70.6 | 8 | 0.234 | 1.26e-07 (2^-22.92) | 22.92 |
| 30 | `pipelined_m:data_width=28,n_iter=28,angle_guard=1,frac_guard=1,rounding=round,m=8` | 2710 | 436 | 45.9 | 6 | 0.237 | 8.86e-08 (2^-23.43) | 23.43 |
| 31 | `pipelined_m:data_width=28,n_iter=26,angle_guard=2,frac_guard=4,rounding=round,m=8` | 2699 | 458 | 44.0 | 6 | 0.237 | 6.35e-08 (2^-23.91) | 23.91 |
| 32 | `pipelined_m:data_width=28,n_iter=28,angle_guard=2,frac_guard=4,rounding=round,m=3` | 2909 | 1069 | 105.9 | 12 | 0.299 | 4.07e-08 (2^-24.55) | 24.55 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraint is the bursty system one: bursts of 8 back-to-back requests must finish inside 0.4 us, so a design that accepts one request every several cycles queues the burst and fails (and the L1 bound is optimistic, so I want real headroom, not a marginal pass). That rules out `iterative` (N+3 cycles/result: even at high fmax a burst of 8 blows the bound, and the N needed for 2^-10 accuracy makes it worse) and low-k `unrolled_k`, so I spend nothing on `iterative` and restrict `unrolled_k` to k=4..8. I focus on the two 1-result/cycle families: `pipelined_m` (fewest FFs, likely the min-luts_plus_ffs winner the selection rule picks) and `pipelined` (highest fmax, best latency headroom). Accuracy 2^-10 forces W>=~12 (output LSB 2^-(W-2)) and N>=~11 (CORDIC residual ~2^-N), so I centre data_width on 11..20 and n_iter on 10..20, keeping the low end near the feasibility boundary for the cheap corner and the high end to span accuracy_bits up to ~18 for hypervolume coverage against the (3000, 10) reference point. angle_guard -2..3 and frac_guard 0..3 let the search trade angle/frac precision against area, and both rounding modes are kept since round can buy a bit of accuracy for free.*)
- `pipelined_m` (40 evals): data_width=11..20, n_iter=10..20, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* Still 1 result/cycle (so it survives the bursty p99 bound with headroom) but registers only every m stages, so it should own the low-luts_plus_ffs end of the front that the min-area selection rule picks; m=2..8 spans the area/fmax trade-off.
- `pipelined` (30 evals): data_width=11..20, n_iter=10..20, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round. *Why:* One register per micro-rotation gives the shortest combinational path and highest fmax, hence the most latency headroom for the L2 system simulation; it anchors the high-accuracy/high-throughput part of the front.
- `unrolled_k` (30 evals): data_width=11..20, n_iter=10..20, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round, k=4..8. *Why:* Shares k micro-rotation units across cycles, so it can be smaller than a fully pipelined datapath; only high k (4..8) keeps ceil(N/k)+3 cycles/result low enough to have any chance on the burst p99 bound.

**Result (code):** 100 evaluations this round, 100 total; 59 feasible; hypervolume 1.006e+04 (n/a).

**LLM decision:** `add_family` — Round 1 mapped the front well on both objectives: luts_plus_ffs spans 903..2761 against HV ref 3000 and accuracy_bits spans 10.9..16.4 against HV ref 10, so the pipelined/pipelined_m front already covers the reference box. The one structural gap is that the `iterative` family (1 micro-rotation/cycle, shared datapath) has never been evaluated, and it is the family most likely to push luts_plus_ffs below the current cheapest design (pipelined_m @ 903). The throughput constraint is only >=2 MSPS and the best feasible throughput seen is 282 MSPS, so a low-throughput shared-datapath design has ample headroom on that constraint; the binding risk is the sys_p99_latency_us<=0.4 bound (best seen 0.066, so there is margin, but L1 is optimistic and L2 may drop the cheapest burst-queuing designs). unrolled_k produced 0 feasible designs in 30 evals, so it is not worth more budget. Bringing in `iterative` is the highest-value move for extending the area end of the front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 1.006e+04 (gain this round: n/a (first round)).
Feasible designs: 59 of 100 evaluations (46 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 20% violate; best seen 1.19e-05 (2^-16.36)
- sys_p99_latency_us <= 0.4: 30% violate; best seen 0.066

Pareto front (feasible, 17 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=903, accuracy_bits=10.9, luts=736, ffs=167, throughput_msps=56.8, max_abs_err=0.000525 (2^-10.90), power_index=0.0679
- pipelined_m [data_width=20 n_iter=12 angle_guard=2 frac_guard=0 rounding=round m=7] luts_plus_ffs=973, accuracy_bits=11, luts=793, ffs=180, throughput_msps=56.8, max_abs_err=0.000492 (2^-10.99), power_index=0.0732
- pipelined_m [data_width=16 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=1148, accuracy_bits=12, luts=938, ffs=210, throughput_msps=59.6, max_abs_err=0.000237 (2^-12.04), power_index=0.0863
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=1 rounding=round m=5] luts_plus_ffs=1185, accuracy_bits=12.8, luts=958, ffs=227, throughput_msps=77, max_abs_err=0.00014 (2^-12.80), power_index=0.0891
- pipelined_m [data_width=20 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=1240, accuracy_bits=13.5, luts=994, ffs=246, throughput_msps=56.8, max_abs_err=8.71e-05 (2^-13.49), power_index=0.0933
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=6] luts_plus_ffs=1329, accuracy_bits=14.6, luts=1080, ffs=249, throughput_msps=65.4, max_abs_err=4.12e-05 (2^-14.57), power_index=0.1
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=6] luts_plus_ffs=1409, accuracy_bits=14.6, luts=1154, ffs=255, throughput_msps=65.4, max_abs_err=3.91e-05 (2^-14.64), power_index=0.106
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=round m=6] luts_plus_ffs=1426, accuracy_bits=14.7, luts=1170, ffs=256, throughput_msps=65.4, max_abs_err=3.84e-05 (2^-14.67), power_index=0.107
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=3 rounding=round] luts_plus_ffs=2689, accuracy_bits=15.6, luts=1355, ffs=1334, throughput_msps=257, max_abs_err=1.96e-05 (2^-15.64), power_index=0.202
- pipelined [data_width=20 n_iter=18 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=2761, accuracy_bits=16.4, luts=1391, ffs=1370, throughput_msps=257, max_abs_err=1.19e-05 (2^-16.36), power_index=0.208
Front coverage: luts_plus_ffs 903..2761 (HV reference 3000); accuracy_bits 10.9..16.4 (HV reference 10); data_width on the front 16..20 (registry 8..28).

Per family:
- unrolled_k: 30 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 13.92 bits
- pipelined: 30 evals, 25 feasible; max throughput seen 282 MSPS; best accuracy 16.36 bits; best feasible luts_plus_ffs=1480; feasible ranges: data_width 14..20, n_iter 12..19, angle_guard -2..3, frac_guard 0..3
- pipelined_m: 40 evals, 34 feasible; max throughput seen 130 MSPS; best accuracy 15.45 bits; best feasible luts_plus_ffs=903; feasible ranges: data_width 16..20, n_iter 12..20, angle_guard -1..3, frac_guard 0..2, m 3..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Focus the round on the unexplored iterative family around the accuracy-feasible region seen on the front, to try to extend luts_plus_ffs below 903; keep a share for pipelined_m refinement near its 903..1426 corner.*)
- `iterative` (100 evals): data_width=14..22, n_iter=12..20, angle_guard=-1..3, frac_guard=0..2, rounding=trunc|round. *Why:* shared datapath should give the lowest LUT+FF; keep data_width/n_iter near the accuracy-feasible region (front uses 16..20 / 12..20) so max_abs_err<=2^-10 is met while exploring cheaper area points

**Result (code):** 100 evaluations this round, 200 total; 59 feasible; hypervolume 1.006e+04 (+0.0%).

**LLM decision:** `refine` — Only pipelined and pipelined_m are feasible (iterative/unrolled_k: 0/130 feasible — their multi-cycle-per-result schedule blows the sys_p99_latency_us<=0.4 bound under 8-request bursts, even though their raw throughput 12-13.5 MSPS clears the >=2 MSPS constraint). The front is well covered on both objectives (luts_plus_ffs 903..2761 vs ref 3000; accuracy 10.9..16.4 vs ref 10), and round 2 gained +0.0%, so the search has plateaued inside the ranges used. Two concrete gaps remain: (1) the selection objective sits at the low-area corner, pipelined_m data_width=19 n_iter=12 -> 903, yet data_width 16..18 are feasible for pipelined_m and accuracy at n_iter=12 is n_iter-limited (data_width 19->20 at n_iter=12 moves accuracy only 10.9->11.0), so a data_width 17-18 / n_iter 12-13 point should be cheaper at ~10.5-10.8 bits and is not on the front — it looks under-sampled; (2) the shown front jumps from 1426 (14.7 bits) to 2689 (15.6 bits), a wide x-gap at y~14.7 that dominates a large slice of the HV. Both are inside the already-feasible ranges, so this is a refine, not a widen (data_width 16..20 / n_iter 12..20 already covers the useful region; going below data_width~16 or above ~22 only adds infeasible or >ref-area designs).
- **rule applied by code:** 'refine' overridden to stop: HV gain 0.00% < epsilon 1.00%
- **rule applied by code:** code: before stopping (converged), one front-mapping round with the remaining 200 evaluations
- effective decision: `stop`

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.006e+04 (gain this round: +0.0%).
Feasible designs: 59 of 200 evaluations (46 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 14% violate; best seen 1.19e-05 (2^-16.36)
- sys_p99_latency_us <= 0.4: 65% violate; best seen 0.066

Pareto front (feasible, 17 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=903, accuracy_bits=10.9, luts=736, ffs=167, throughput_msps=56.8, max_abs_err=0.000525 (2^-10.90), power_index=0.0679
- pipelined_m [data_width=20 n_iter=12 angle_guard=2 frac_guard=0 rounding=round m=7] luts_plus_ffs=973, accuracy_bits=11, luts=793, ffs=180, throughput_msps=56.8, max_abs_err=0.000492 (2^-10.99), power_index=0.0732
- pipelined_m [data_width=16 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=7] luts_plus_ffs=1148, accuracy_bits=12, luts=938, ffs=210, throughput_msps=59.6, max_abs_err=0.000237 (2^-12.04), power_index=0.0863
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=1 rounding=round m=5] luts_plus_ffs=1185, accuracy_bits=12.8, luts=958, ffs=227, throughput_msps=77, max_abs_err=0.00014 (2^-12.80), power_index=0.0891
- pipelined_m [data_width=20 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=1240, accuracy_bits=13.5, luts=994, ffs=246, throughput_msps=56.8, max_abs_err=8.71e-05 (2^-13.49), power_index=0.0933
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=6] luts_plus_ffs=1329, accuracy_bits=14.6, luts=1080, ffs=249, throughput_msps=65.4, max_abs_err=4.12e-05 (2^-14.57), power_index=0.1
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=6] luts_plus_ffs=1409, accuracy_bits=14.6, luts=1154, ffs=255, throughput_msps=65.4, max_abs_err=3.91e-05 (2^-14.64), power_index=0.106
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=round m=6] luts_plus_ffs=1426, accuracy_bits=14.7, luts=1170, ffs=256, throughput_msps=65.4, max_abs_err=3.84e-05 (2^-14.67), power_index=0.107
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=3 rounding=round] luts_plus_ffs=2689, accuracy_bits=15.6, luts=1355, ffs=1334, throughput_msps=257, max_abs_err=1.96e-05 (2^-15.64), power_index=0.202
- pipelined [data_width=20 n_iter=18 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=2761, accuracy_bits=16.4, luts=1391, ffs=1370, throughput_msps=257, max_abs_err=1.19e-05 (2^-16.36), power_index=0.208
Front coverage: luts_plus_ffs 903..2761 (HV reference 3000); accuracy_bits 10.9..16.4 (HV reference 10); data_width on the front 16..20 (registry 8..28).

Per family:
- iterative: 100 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 15.94 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 13.92 bits
- pipelined: 30 evals, 25 feasible; max throughput seen 282 MSPS; best accuracy 16.36 bits; best feasible luts_plus_ffs=1480; feasible ranges: data_width 14..20, n_iter 12..19, angle_guard -2..3, frac_guard 0..3
- pipelined_m: 40 evals, 34 feasible; max throughput seen 130 MSPS; best accuracy 15.45 bits; best feasible luts_plus_ffs=903; feasible ranges: data_width 16..20, n_iter 12..20, angle_guard -1..3, frac_guard 0..2, m 3..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 200 evaluations*)
- `pipelined_m` (165 evals): data_width=15..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (14 front designs; box front_anchored)
- `pipelined` (35 evals): data_width=19..28, n_iter=16..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)

**Result (code):** 200 evaluations this round, 400 total; 249 feasible; hypervolume 1.555e+04 (+54.6%).

**No LLM call** (code's front-mapping round): Only pipelined and pipelined_m are feasible (iterative/unrolled_k: 0/130 feasible — their multi-cycle-per-result schedule blows the sys_p99_latency_us<=0.4 bound under 8-request bursts, even though their raw throughput 12-13.5 MSPS clears the >=2 MSPS constraint). The front is well covered on both objectives (luts_plus_ffs 903..2761 vs ref 3000; accuracy 10.9..16.4 vs ref 10), and round 2 gained +0.0%, so the search has plateaued inside the ranges used. Two concrete gaps remain: (1) the selection objective sits at the low-area corner, pipelined_m data_width=19 n_iter=12 -> 903, yet data_width 16..18 are feasible for pipelined_m and accuracy at n_iter=12 is n_iter-limited (data_width 19->20 at n_iter=12 moves accuracy only 10.9->11.0), so a data_width 17-18 / n_iter 12-13 point should be cheaper at ~10.5-10.8 bits and is not on the front — it looks under-sampled; (2) the shown front jumps from 1426 (14.7 bits) to 2689 (15.6 bits), a wide x-gap at y~14.7 that dominates a large slice of the HV. Both are inside the already-feasible ranges, so this is a refine, not a widen (data_width 16..20 / n_iter 12..20 already covers the useful region; going below data_width~16 or above ~22 only adds infeasible or >ref-area designs).
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.555e+04 (gain this round: +54.6%).
Feasible designs: 249 of 400 evaluations (217 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 2: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 10% violate; best seen 4.07e-08 (2^-24.55)
- sys_p99_latency_us <= 0.4: 32% violate; best seen 0.066

Pareto front (feasible, 33 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=12 angle_guard=0 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=903, accuracy_bits=10.9, luts=736, ffs=167, throughput_msps=56.8, max_abs_err=0.000525 (2^-10.90), power_index=0.0679
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=8] luts_plus_ffs=1100, accuracy_bits=12.9, luts=941, ffs=159, throughput_msps=50.3, max_abs_err=0.00013 (2^-12.91), power_index=0.0828
- pipelined_m [data_width=21 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc m=8] luts_plus_ffs=1207, accuracy_bits=13.7, luts=1023, ffs=184, throughput_msps=50.3, max_abs_err=7.62e-05 (2^-13.68), power_index=0.0908
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=3 rounding=round m=8] luts_plus_ffs=1347, accuracy_bits=14.6, luts=1168, ffs=180, throughput_msps=50.3, max_abs_err=3.97e-05 (2^-14.62), power_index=0.101
- pipelined_m [data_width=20 n_iter=17 angle_guard=2 frac_guard=2 rounding=round m=6] luts_plus_ffs=1521, accuracy_bits=15.5, luts=1261, ffs=259, throughput_msps=65.4, max_abs_err=2.23e-05 (2^-15.45), power_index=0.114
- pipelined_m [data_width=19 n_iter=20 angle_guard=4 frac_guard=3 rounding=round m=8] luts_plus_ffs=1765, accuracy_bits=16.6, luts=1507, ffs=258, throughput_msps=48, max_abs_err=1.03e-05 (2^-16.57), power_index=0.133
- pipelined_m [data_width=25 n_iter=20 angle_guard=4 frac_guard=2 rounding=trunc m=8] luts_plus_ffs=2106, accuracy_bits=18.8, luts=1787, ffs=319, throughput_msps=45.9, max_abs_err=2.12e-06 (2^-18.85), power_index=0.158
- pipelined_m [data_width=26 n_iter=22 angle_guard=4 frac_guard=0 rounding=round m=6] luts_plus_ffs=2364, accuracy_bits=20.6, luts=1953, ffs=412, throughput_msps=59.9, max_abs_err=6.47e-07 (2^-20.56), power_index=0.178
- pipelined_m [data_width=26 n_iter=27 angle_guard=4 frac_guard=2 rounding=round m=8] luts_plus_ffs=3006, accuracy_bits=22.9, luts=2581, ffs=426, throughput_msps=45.9, max_abs_err=1.28e-07 (2^-22.89), power_index=0.226
- pipelined_m [data_width=28 n_iter=28 angle_guard=2 frac_guard=4 rounding=round m=3] luts_plus_ffs=3979, accuracy_bits=24.6, luts=2909, ffs=1069, throughput_msps=106, max_abs_err=4.07e-08 (2^-24.55), power_index=0.299
Front coverage: luts_plus_ffs 903..3979 (HV reference 3000); accuracy_bits 10.9..24.6 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- iterative: 100 evals, 0 feasible; max throughput seen 13.5 MSPS; best accuracy 15.94 bits
- unrolled_k: 30 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 13.92 bits
- pipelined: 65 evals, 60 feasible; max throughput seen 282 MSPS; best accuracy 22.70 bits; best feasible luts_plus_ffs=1480; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 205 evals, 189 feasible; max throughput seen 164 MSPS; best accuracy 24.55 bits; best feasible luts_plus_ffs=903; feasible ranges: data_width 15..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 6 (failed/unparsed attempts: 0)
- tokens: 23299 in, 24968 out
- provider-reported cost: $0.0175
- full prompts and replies: `llm_trace.jsonl`

