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
`pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 890 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 274 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 61.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000241 (2^-12.02) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.94 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 5.15e-05 (2^-14.25) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 0.844 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12 | exact: bit-accurate model, exhaustive (65536 angles) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 89.5 dBc, SNR 82.9 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Every L1-feasible design (241) was simulated at its estimated Fmax (SimPy); 235 pass. Top 5 by the selection rule, L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=0,frac_guard=1,rounding=round,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=2,rounding=round,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=0,frac_guard=2,rounding=round,m=4` | 0.3848 → 0.3953 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## L5 back-annotation: measured vs estimate

No measured data for the selected design in `l4_synthesis.csv`; nothing to compare.
- no measured data for the selected design; nothing to compare

## Pareto front (37 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 890 | 274 | 97.8 | 6 | 1.4 | 0.000241 (2^-12.02) | 12.02 |
| 1 | `pipelined_m:data_width=17,n_iter=15,angle_guard=0,frac_guard=1,rounding=round,m=4` | 911 | 276 | 97.8 | 6 | 1.43 | 0.000224 (2^-12.12) | 12.12 |
| 2 | `pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=4` | 904 | 291 | 93.6 | 6 | 1.44 | 0.000169 (2^-12.53) | 12.53 |
| 3 | `pipelined_m:data_width=20,n_iter=14,angle_guard=-1,frac_guard=1,rounding=trunc,m=3` | 923 | 381 | 119.3 | 7 | 1.57 | 0.000151 (2^-12.69) | 12.69 |
| 4 | `pipelined_m:data_width=20,n_iter=14,angle_guard=2,frac_guard=0,rounding=trunc,m=3` | 937 | 388 | 119.3 | 7 | 1.6 | 0.000141 (2^-12.79) | 12.79 |
| 5 | `pipelined_m:data_width=19,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=4` | 1019 | 309 | 93.6 | 6 | 1.6 | 7.94e-05 (2^-13.62) | 13.62 |
| 6 | `pipelined_m:data_width=19,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1023 | 317 | 93.6 | 6 | 1.61 | 7.77e-05 (2^-13.65) | 13.65 |
| 7 | `pipelined_m:data_width=20,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=4` | 1067 | 331 | 93.6 | 6 | 1.68 | 6.78e-05 (2^-13.85) | 13.85 |
| 8 | `pipelined_m:data_width=20,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,m=3` | 1048 | 446 | 119.3 | 8 | 1.8 | 5.27e-05 (2^-14.21) | 14.21 |
| 9 | `pipelined_m:data_width=20,n_iter=16,angle_guard=1,frac_guard=1,rounding=trunc,m=3` | 1096 | 462 | 119.3 | 8 | 1.88 | 4.71e-05 (2^-14.37) | 14.37 |
| 10 | `pipelined_m:data_width=20,n_iter=17,angle_guard=0,frac_guard=0,rounding=round,m=3` | 1118 | 446 | 119.3 | 8 | 1.88 | 4.25e-05 (2^-14.52) | 14.52 |
| 11 | `pipelined_m:data_width=21,n_iter=17,angle_guard=-1,frac_guard=1,rounding=trunc,m=4` | 1185 | 399 | 93.6 | 7 | 1.91 | 3.78e-05 (2^-14.69) | 14.69 |
| 12 | `pipelined_m:data_width=21,n_iter=17,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 1236 | 414 | 89.6 | 7 | 1.99 | 2.27e-05 (2^-15.43) | 15.43 |
| 13 | `pipelined_m:data_width=21,n_iter=17,angle_guard=1,frac_guard=1,rounding=round,m=3` | 1263 | 484 | 119.3 | 8 | 2.1 | 2.15e-05 (2^-15.51) | 15.51 |
| 14 | `pipelined_m:data_width=21,n_iter=17,angle_guard=2,frac_guard=1,rounding=round,m=3` | 1280 | 490 | 114.5 | 8 | 2.13 | 1.98e-05 (2^-15.62) | 15.62 |
| 15 | `pipelined_m:data_width=19,n_iter=20,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1447 | 394 | 93.6 | 7 | 2.22 | 1.48e-05 (2^-16.05) | 16.05 |
| 16 | `pipelined_m:data_width=19,n_iter=20,angle_guard=3,frac_guard=4,rounding=round,m=4` | 1527 | 411 | 89.6 | 7 | 2.33 | 1.08e-05 (2^-16.50) | 16.50 |
| 17 | `pipelined_m:data_width=25,n_iter=19,angle_guard=1,frac_guard=0,rounding=round,m=4` | 1561 | 469 | 89.6 | 7 | 2.44 | 4.46e-06 (2^-17.77) | 17.77 |
| 18 | `pipelined_m:data_width=23,n_iter=20,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1675 | 458 | 89.6 | 7 | 2.57 | 2.95e-06 (2^-18.37) | 18.37 |
| 19 | `pipelined_m:data_width=23,n_iter=20,angle_guard=2,frac_guard=4,rounding=round,m=4` | 1756 | 474 | 86.0 | 7 | 2.68 | 2.78e-06 (2^-18.46) | 18.46 |
| 20 | `pipelined_m:data_width=26,n_iter=20,angle_guard=-1,frac_guard=2,rounding=round,m=4` | 1802 | 494 | 86.0 | 7 | 2.76 | 2.52e-06 (2^-18.60) | 18.60 |
| 21 | `pipelined_m:data_width=27,n_iter=20,angle_guard=-1,frac_guard=2,rounding=trunc,m=4` | 1807 | 510 | 86.0 | 7 | 2.79 | 2.27e-06 (2^-18.75) | 18.75 |
| 22 | `pipelined_m:data_width=22,n_iter=24,angle_guard=3,frac_guard=4,rounding=round,m=3` | 2063 | 716 | 114.5 | 10 | 3.35 | 1.28e-06 (2^-19.57) | 19.57 |
| 23 | `pipelined_m:data_width=23,n_iter=28,angle_guard=3,frac_guard=2,rounding=round,m=4` | 2387 | 631 | 89.6 | 9 | 3.63 | 1.19e-06 (2^-19.68) | 19.68 |
| 24 | `pipelined_m:data_width=27,n_iter=24,angle_guard=1,frac_guard=2,rounding=trunc,m=3` | 2235 | 801 | 110.0 | 10 | 3.65 | 2.3e-07 (2^-22.05) | 22.05 |
| 25 | `pipelined_m:data_width=27,n_iter=24,angle_guard=1,frac_guard=3,rounding=trunc,m=3` | 2283 | 815 | 110.0 | 10 | 3.73 | 2.3e-07 (2^-22.05) | 22.05 |
| 26 | `pipelined_m:data_width=28,n_iter=24,angle_guard=1,frac_guard=2,rounding=round,m=3` | 2367 | 829 | 110.0 | 10 | 3.85 | 1.69e-07 (2^-22.50) | 22.50 |
| 27 | `pipelined_m:data_width=27,n_iter=24,angle_guard=3,frac_guard=3,rounding=round,m=3` | 2389 | 833 | 110.0 | 10 | 3.88 | 1.54e-07 (2^-22.63) | 22.63 |
| 28 | `pipelined_m:data_width=28,n_iter=24,angle_guard=4,frac_guard=3,rounding=trunc,m=3` | 2429 | 866 | 105.9 | 10 | 3.97 | 1.42e-07 (2^-22.74) | 22.74 |
| 29 | `pipelined_m:data_width=28,n_iter=24,angle_guard=3,frac_guard=3,rounding=round,m=3` | 2464 | 860 | 105.9 | 10 | 4 | 1.37e-07 (2^-22.80) | 22.80 |
| 30 | `pipelined_m:data_width=28,n_iter=26,angle_guard=1,frac_guard=1,rounding=round,m=3` | 2514 | 910 | 110.0 | 11 | 4.12 | 1.04e-07 (2^-23.20) | 23.20 |
| 31 | `pipelined_m:data_width=27,n_iter=25,angle_guard=3,frac_guard=4,rounding=round,m=3` | 2541 | 947 | 105.9 | 11 | 4.2 | 9.31e-08 (2^-23.36) | 23.36 |
| 32 | `pipelined_m:data_width=28,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc,m=3` | 2613 | 958 | 105.9 | 11 | 4.3 | 5.73e-08 (2^-24.06) | 24.06 |
| 33 | `pipelined_m:data_width=28,n_iter=26,angle_guard=3,frac_guard=4,rounding=trunc,m=3` | 2666 | 975 | 105.9 | 11 | 4.38 | 5.72e-08 (2^-24.06) | 24.06 |
| 34 | `pipelined_m:data_width=27,n_iter=27,angle_guard=3,frac_guard=4,rounding=round,m=3` | 2747 | 947 | 105.9 | 11 | 4.45 | 5.51e-08 (2^-24.11) | 24.11 |
| 35 | `pipelined_m:data_width=27,n_iter=30,angle_guard=3,frac_guard=4,rounding=round,m=3` | 3057 | 1047 | 105.9 | 12 | 4.94 | 4.6e-08 (2^-24.37) | 24.37 |
| 36 | `pipelined_m:data_width=28,n_iter=30,angle_guard=3,frac_guard=4,rounding=round,m=3` | 3151 | 1080 | 105.9 | 12 | 5.09 | 2.41e-08 (2^-25.31) | 25.31 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraint is the system batch bound: a 1 MHz tick dumps 32 requests at once and the last result must land within 0.44 us, i.e. an effective burst rate of ~73 Msps. On Artix-7 only the 1-result/cycle families can reach that: pipelined (latency N+2, 1/cyc) and pipelined_m (latency ceil(N/m)+2, 1/cyc). iterative needs N+3 cyc/result and unrolled_k needs ceil(N/k)+3 cyc/result, so a 32-deep burst costs >=128-224 cycles and would require >290 MHz to clear 0.44 us - not reachable, so they only get small probe budgets to document infeasibility rather than a real share. Accuracy 2^-12 forces W>=14 (output LSB 2^-(W-2)) plus CORDIC residual, so N in the low-to-mid teens and a little angle/frac guard. The area objective (min LUTs+FFs) favours pipelined_m, which registers only every m stages and therefore carries far fewer FFs than the fully-registered pipelined chain, but its Fmax falls as m grows; pipelined has the best Fmax at the cost of N register banks. That Fmax-vs-FF trade between the two pipelined families (and m within pipelined_m) is where the Pareto front lives, so they take 85% of round 1. Round 1 deliberately spans W, N, guard and rounding so later rounds can tighten around the feasible region and then map the front over full ranges.*)
- `pipelined_m` (50 evals): data_width=14..20, n_iter=12..20, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* Primary area candidate: 1 result/cycle clears the 32-request burst, and registering only every m stages cuts the FF count that dominates luts_plus_ffs. m is the key knob - small m keeps Fmax (and hence the 0.44 us batch margin) high, large m shrinks registers. W/N/guards set the accuracy-vs-area trade against the 2^-12 limit.
- `pipelined` (35 evals): data_width=14..20, n_iter=12..20, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Best-Fmax 1-result/cycle option: constant per-stage shifts, no barrel muxes, so it should give the highest clock and the safest batch margin, at the cost of N pipeline register banks (high FFs). Needed to anchor the high-throughput/low-latency end of the front and to test whether its Fmax advantage outweighs its FF penalty for the min-area objective.
- `unrolled_k` (10 evals): data_width=14..20, n_iter=8..20, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=6..8. *Why:* Probe only. Even at k=8 the FSM overhead gives >=4 cycles/result, so a 32-request burst needs >290 MHz to fit 0.44 us - almost certainly infeasible. A small budget confirms this and checks the throughput_msps>=32 edge, so we do not wrongly exclude it.
- `iterative` (5 evals): data_width=14..20, n_iter=8..20, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Probe only. N+3 cycles/result means a 32-deep burst costs >=224 cycles, needing >500 MHz, and even the throughput_msps>=32 floor is marginal at small N. Tiny budget to document infeasibility rather than assume it.

**Result (code):** 100 evaluations this round, 100 total; 32 feasible; hypervolume 8399 (n/a).

**LLM decision:** `map_front` — Only pipelined/pipelined_m are feasible: iterative (best 15.3 MSPS) and unrolled_k (best 13.1 MSPS) cannot reach the 32 MSPS constraint, so the front will stay in those two families. The current feasible front is a narrow ribbon of 7 pipelined_m designs covering luts_plus_ffs 1328-1959, i.e. only ~33-49% of the 0-4000 HV reference span, and accuracy_bits 13.6-15.4. Working from the given numbers, the dominant hypervolume term is the strip between the largest-area front point and the reference, (4000-1959)x(15.4-12) ~ 6.9k out of the 8399 total, and that region is essentially empty. Yet the registry allows data_width up to 28 and n_iter up to 30 while the front only uses data_width 18-20 / n_iter 15-20, so larger, higher-accuracy designs that would still satisfy throughput (>=32 MSPS is met with huge margin: best seen 273) and sys_p99_batch_us (best seen 0.161 vs 0.44) should exist and would extend the front toward the reference point. A refine of the already-dense low-area corner (min feasible luts_plus_ffs floor appears to be ~1328) can add only a few hundred HV, whereas filling the unpopulated high-accuracy/high-area part of the range can add thousands. Mapping the whole front (NSGA-II over full pipelined_m/pipelined ranges, seeded with the current 7 points) also usefully populates safer higher-throughput points (the cheapest m=4 designs sit at 93.6 MSPS with an L1 batch bound close to the 0.44 us limit and may be lost at L2), hedging the L1-to-L2 risk noted in the spec.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 8399 (gain this round: n/a (first round)).
Feasible designs: 32 of 100 evaluations (26 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 15% violate; best seen 273
- max_abs_err <= 0.000244141: 55% violate; best seen 2.28e-05 (2^-15.42)
- sys_p99_batch_us <= 0.44: 34% violate; best seen 0.161

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1328, accuracy_bits=13.6, luts=1019, ffs=309, throughput_msps=93.6, max_abs_err=7.94e-05 (2^-13.62), power_index=1.6
- pipelined_m [data_width=19 n_iter=18 angle_guard=1 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1518, accuracy_bits=13.6, luts=1152, ffs=366, throughput_msps=93.6, max_abs_err=7.8e-05 (2^-13.65), power_index=1.83
- pipelined_m [data_width=18 n_iter=18 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1531, accuracy_bits=13.8, luts=1172, ffs=359, throughput_msps=93.6, max_abs_err=6.95e-05 (2^-13.81), power_index=1.84
- pipelined_m [data_width=19 n_iter=18 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1562, accuracy_bits=14.3, luts=1188, ffs=374, throughput_msps=93.6, max_abs_err=4.91e-05 (2^-14.31), power_index=1.88
- pipelined_m [data_width=19 n_iter=20 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1743, accuracy_bits=14.8, luts=1367, ffs=376, throughput_msps=93.6, max_abs_err=3.6e-05 (2^-14.76), power_index=2.1
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=1915, accuracy_bits=15.1, luts=1241, ffs=674, throughput_msps=164, max_abs_err=2.8e-05 (2^-15.12), power_index=2.31
- pipelined_m [data_width=20 n_iter=18 angle_guard=1 frac_guard=1 rounding=round m=2] luts_plus_ffs=1959, accuracy_bits=15.4, luts=1283, ffs=676, throughput_msps=164, max_abs_err=2.28e-05 (2^-15.42), power_index=2.36
Front coverage: luts_plus_ffs 1328..1959 (HV reference 4000); accuracy_bits 13.6..15.4 (HV reference 12); data_width on the front 18..20 (registry 8..28).

Per family:
- iterative: 5 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 13.91 bits
- unrolled_k: 10 evals, 0 feasible; max throughput seen 13.1 MSPS; best accuracy 13.26 bits
- pipelined: 35 evals, 14 feasible; max throughput seen 273 MSPS; best accuracy 15.12 bits; best feasible luts_plus_ffs=1717; feasible ranges: data_width 17..20, n_iter 14..20, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 18 feasible; max throughput seen 171 MSPS; best accuracy 15.42 bits; best feasible luts_plus_ffs=1328; feasible ranges: data_width 16..20, n_iter 15..20, angle_guard 1..2, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (7 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 91 feasible; hypervolume 1.67e+04 (+98.9%).

**LLM decision:** `refine` — Round 2 left a valid 21-design front but with two concrete gaps: (1) all 21 front designs are pipelined_m, and the non-dominated curve has a hole between 2296 LUT+FF/18.6 bits and 3482 LUT+FF/19.9 bits, even though 24.39 bits is achievable and the front only reaches 22.6 bits - with HV ref 4000, samples in the cost 2000-4000 / accuracy 19-24.5 band are what raise hypervolume; (2) the selector's current pick (1288 LUT+FF, 12.5 bits) sits only 0.5 bit above the 2^-12 error limit, and the system constraint is L1-optimistic (best sys_p99_batch_us=0.161 vs 0.44), so the cheap corner needs redundancy before the L2 re-selection. iterative/unrolled_k cannot be refined - they never reached 32 MSPS - and pipelined (m=1) is under-sampled at 35/200 evals, so its feasible box (data_width 17..20) should be re-checked rather than trusted. Refining these three bands is more sample-efficient than a broad re-map, and leaves round 4 free for the reserved full-range front mapping.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.67e+04 (gain this round: +98.9%).
Feasible designs: 91 of 200 evaluations (81 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 8% violate; best seen 273
- max_abs_err <= 0.000244141: 30% violate; best seen 4.54e-08 (2^-24.39)
- sys_p99_batch_us <= 0.44: 36% violate; best seen 0.161

Pareto front (feasible, 21 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=1 rounding=round m=3] luts_plus_ffs=1288, accuracy_bits=12.5, luts=922, ffs=366, throughput_msps=119, max_abs_err=0.000177 (2^-12.46), power_index=1.55
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1328, accuracy_bits=13.6, luts=1019, ffs=309, throughput_msps=93.6, max_abs_err=7.94e-05 (2^-13.62), power_index=1.6
- pipelined_m [data_width=18 n_iter=18 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1531, accuracy_bits=13.8, luts=1172, ffs=359, throughput_msps=93.6, max_abs_err=6.95e-05 (2^-13.81), power_index=1.84
- pipelined_m [data_width=18 n_iter=20 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1762, accuracy_bits=15, luts=1385, ffs=377, throughput_msps=93.6, max_abs_err=3.15e-05 (2^-14.95), power_index=2.12
- pipelined_m [data_width=19 n_iter=20 angle_guard=3 frac_guard=4 rounding=round m=4] luts_plus_ffs=1938, accuracy_bits=16.5, luts=1527, ffs=411, throughput_msps=89.6, max_abs_err=1.08e-05 (2^-16.50), power_index=2.33
- pipelined_m [data_width=23 n_iter=20 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=2134, accuracy_bits=18.4, luts=1675, ffs=458, throughput_msps=89.6, max_abs_err=2.95e-06 (2^-18.37), power_index=2.57
- pipelined_m [data_width=26 n_iter=20 angle_guard=-1 frac_guard=2 rounding=round m=4] luts_plus_ffs=2296, accuracy_bits=18.6, luts=1802, ffs=494, throughput_msps=86, max_abs_err=2.52e-06 (2^-18.60), power_index=2.76
- pipelined_m [data_width=23 n_iter=30 angle_guard=4 frac_guard=2 rounding=round m=3] luts_plus_ffs=3482, accuracy_bits=19.9, luts=2590, ffs=892, throughput_msps=110, max_abs_err=1.04e-06 (2^-19.88), power_index=4.19
- pipelined_m [data_width=25 n_iter=30 angle_guard=3 frac_guard=3 rounding=round m=3] luts_plus_ffs=3773, accuracy_bits=22.2, luts=2808, ffs=965, throughput_msps=110, max_abs_err=2.1e-07 (2^-22.18), power_index=4.54
- pipelined_m [data_width=28 n_iter=30 angle_guard=0 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=4279, accuracy_bits=22.6, luts=2817, ffs=1462, throughput_msps=153, max_abs_err=1.6e-07 (2^-22.57), power_index=5.15
Front coverage: luts_plus_ffs 1288..4279 (HV reference 4000); accuracy_bits 12.5..22.6 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- iterative: 5 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 13.91 bits
- unrolled_k: 10 evals, 0 feasible; max throughput seen 13.1 MSPS; best accuracy 13.26 bits
- pipelined: 35 evals, 14 feasible; max throughput seen 273 MSPS; best accuracy 15.12 bits; best feasible luts_plus_ffs=1717; feasible ranges: data_width 17..20, n_iter 14..20, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 150 evals, 77 feasible; max throughput seen 171 MSPS; best accuracy 24.39 bits; best feasible luts_plus_ffs=1288; feasible ranges: data_width 16..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *iterative and unrolled_k are dead for this spec (max throughput 15.3 and 13.1 MSPS vs the 32 MSPS constraint; 0 feasible in 15 evals), so all remaining budget belongs to pipelined/pipelined_m. The front's HV is concentrated in the cost 2000-4000 band (HV ref 4000), yet the existing front jumps from 2296 LUT+FF/18.6 bits straight to 3482/19.9 bits while 24.39 bits is reachable and the front tops out at only 22.6 bits - that sparse mid/high-accuracy band is where round-3 samples buy the most hypervolume. The second band keeps several cheap designs around the selector pick (1288 LUT+FF, 12.5 bits) so the L1-optimistic system bound (best sys_p99_batch_us 0.161 vs 0.44) is not the only thing standing between the front and L2. Because pipelined_m already spans nearly its full registry ranges, a targeted refine is more sample-efficient than a broad map_front; the reserved round-4 pass can then map the full front over both live families.*)
- `pipelined_m` (67 evals): data_width=22..28, n_iter=24..30, angle_guard=1..4, frac_guard=1..4, rounding=trunc|round, m=2..3. *Why:* the HV-ref cost of 4000 and the 24.39-bit accuracy achieved elsewhere mean the front is thin between the 2296 LUT+FF / 18.6-bit point and the 3482 / 19.9-bit point.
- `pipelined` (33 evals): data_width=17..22, n_iter=14..22, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* pipelined (m=1) is the second live family but got only 35 of 200 evals; its feasible box (data_width 17..20, n_iter 14..20) is almost certainly a sampling artefact, not a real boundary.
- clamped by code: dropped duplicate family pipelined_m

**Result (code):** 100 evaluations this round, 300 total; 191 feasible; hypervolume 1.966e+04 (+17.7%).

**LLM decision:** `refine` — The front is still improving (+17.7% HV this round), so stop is premature, and all four families have already been explored so add_family is moot. The selection rule is min luts_plus_ffs, and the cheapest feasible design is pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=1 rounding=round m=3] at luts_plus_ffs=1288 — far below the HV reference of 4000 — so the low-area corner is the highest-value region to sharpen. The feasible ranges for pipelined_m are still wide (data_width 16..28, n_iter 13..30, m 2..4), so narrowing to the low-area corner spends the remaining 100 evals where they can actually move the selection objective. Constraints have ample margin (throughput best 273 vs >=32; sys_p99_batch_us best 0.161 vs <=0.44), so cheaper/slower designs in this corner are viable. The reserved full-range front mapping will still be run by code, so this refine round is complementary rather than redundant.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 1.966e+04 (gain this round: +17.7%).
Feasible designs: 191 of 300 evaluations (167 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 5% violate; best seen 273
- max_abs_err <= 0.000244141: 20% violate; best seen 2.41e-08 (2^-25.31)
- sys_p99_batch_us <= 0.44: 24% violate; best seen 0.161

Pareto front (feasible, 30 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=1 rounding=round m=3] luts_plus_ffs=1288, accuracy_bits=12.5, luts=922, ffs=366, throughput_msps=119, max_abs_err=0.000177 (2^-12.46), power_index=1.55
- pipelined_m [data_width=19 n_iter=18 angle_guard=1 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1518, accuracy_bits=13.6, luts=1152, ffs=366, throughput_msps=93.6, max_abs_err=7.8e-05 (2^-13.65), power_index=1.83
- pipelined_m [data_width=19 n_iter=20 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1743, accuracy_bits=14.8, luts=1367, ffs=376, throughput_msps=93.6, max_abs_err=3.6e-05 (2^-14.76), power_index=2.1
- pipelined_m [data_width=25 n_iter=19 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=2030, accuracy_bits=17.8, luts=1561, ffs=469, throughput_msps=89.6, max_abs_err=4.46e-06 (2^-17.77), power_index=2.44
- pipelined_m [data_width=26 n_iter=20 angle_guard=-1 frac_guard=2 rounding=round m=4] luts_plus_ffs=2296, accuracy_bits=18.6, luts=1802, ffs=494, throughput_msps=86, max_abs_err=2.52e-06 (2^-18.60), power_index=2.76
- pipelined_m [data_width=23 n_iter=28 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=3017, accuracy_bits=19.7, luts=2387, ffs=631, throughput_msps=89.6, max_abs_err=1.19e-06 (2^-19.68), power_index=3.63
- pipelined_m [data_width=28 n_iter=24 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=3196, accuracy_bits=22.5, luts=2367, ffs=829, throughput_msps=110, max_abs_err=1.69e-07 (2^-22.50), power_index=3.85
- pipelined_m [data_width=28 n_iter=26 angle_guard=1 frac_guard=1 rounding=round m=3] luts_plus_ffs=3424, accuracy_bits=23.2, luts=2514, ffs=910, throughput_msps=110, max_abs_err=1.04e-07 (2^-23.20), power_index=4.12
- pipelined_m [data_width=28 n_iter=26 angle_guard=3 frac_guard=4 rounding=trunc m=3] luts_plus_ffs=3641, accuracy_bits=24.1, luts=2666, ffs=975, throughput_msps=106, max_abs_err=5.72e-08 (2^-24.06), power_index=4.38
- pipelined_m [data_width=28 n_iter=30 angle_guard=3 frac_guard=4 rounding=round m=3] luts_plus_ffs=4230, accuracy_bits=25.3, luts=3151, ffs=1080, throughput_msps=106, max_abs_err=2.41e-08 (2^-25.31), power_index=5.09
Front coverage: luts_plus_ffs 1288..4230 (HV reference 4000); accuracy_bits 12.5..25.3 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- iterative: 5 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 13.91 bits
- unrolled_k: 10 evals, 0 feasible; max throughput seen 13.1 MSPS; best accuracy 13.26 bits
- pipelined: 68 evals, 47 feasible; max throughput seen 273 MSPS; best accuracy 15.64 bits; best feasible luts_plus_ffs=1717; feasible ranges: data_width 17..20, n_iter 14..22, angle_guard 0..3, frac_guard 0..3
- pipelined_m: 217 evals, 144 feasible; max throughput seen 171 MSPS; best accuracy 25.31 bits; best feasible luts_plus_ffs=1288; feasible ranges: data_width 16..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

### Round 4

**Plan explored** (LLM rationale: *Focus the last exploration round on the low-area corner (data_width 16-21, n_iter 13-17, m 2-4) where the min-luts_plus_ffs selection rule lives, while code's reserved budget maps the full front over the families already on it.*)
- `pipelined_m` (75 evals): data_width=16..21, n_iter=13..17, angle_guard=-2..2, frac_guard=0..2, rounding=round|trunc, m=2..4. *Why:* Contains the current cheapest feasible design (1288) and the whole low-area corner; m=2..4 covers the register-density trade-off that drives FF count.
- `pipelined` (25 evals): data_width=16..21, n_iter=13..17, angle_guard=-2..2, frac_guard=0..2, rounding=round|trunc. *Why:* Best feasible pipelined area is 1717, close enough to the pipelined_m corner that a cheaper pipelined variant may exist; keep it in the mix for the low-area end.

**Result (code):** 100 evaluations this round, 400 total; 273 feasible; hypervolume 1.997e+04 (+1.6%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), so the only valid choices are stop or infeasible. Infeasible is ruled out by the evidence: 273 of 400 evaluations are feasible, all three constraints are met by real designs (throughput best 273 MSPS vs >=32; max_abs_err best 2.41e-08 vs <=2.44e-04; sys_p99_batch best 0.161 us vs <=0.44 us), and the feasible Pareto front holds 37 designs spanning luts_plus_ffs 1165..4230 and accuracy_bits 12..25.3, i.e. it covers both objective ranges rather than a corner. All four registry families were explored, so there is no unexplored family to add, and the front already reaches the registry limits on data_width (16..28) and near the HV reference points (4000 area, 12 bits). The last round's hypervolume gain was only +1.6% (1.997e+04), indicating the front has converged, so further refinement would not be a good use of a budget that no longer exists. The spec's selection rule (min luts_plus_ffs) picks the pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=4] design at luts_plus_ffs=1165, which satisfies every constraint (throughput 97.8 MSPS, max_abs_err 2.41e-04 <= 2.44e-04, sys_p99_batch 0.161 us <= 0.44 us). Caveat for the L2 stage: that cheapest design's error margin is thin (2.41e-04 against a 2.44e-04 limit) and its L1 system bound is optimistic, so if L2 simulation rejects it the next front points (e.g. luts_plus_ffs=1325 at 12.8 bits, or 1494 at 14.2 bits) are the fallbacks. Stopping with the converged feasible front is the correct final decision.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.997e+04 (gain this round: +1.6%).
Feasible designs: 273 of 400 evaluations (241 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 4% violate; best seen 273
- max_abs_err <= 0.000244141: 19% violate; best seen 2.41e-08 (2^-25.31)
- sys_p99_batch_us <= 0.44: 18% violate; best seen 0.161

Pareto front (feasible, 37 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1165, accuracy_bits=12, luts=890, ffs=274, throughput_msps=97.8, max_abs_err=0.000241 (2^-12.02), power_index=1.4
- pipelined_m [data_width=20 n_iter=14 angle_guard=2 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=1325, accuracy_bits=12.8, luts=937, ffs=388, throughput_msps=119, max_abs_err=0.000141 (2^-12.79), power_index=1.6
- pipelined_m [data_width=20 n_iter=16 angle_guard=0 frac_guard=0 rounding=round m=3] luts_plus_ffs=1494, accuracy_bits=14.2, luts=1048, ffs=446, throughput_msps=119, max_abs_err=5.27e-05 (2^-14.21), power_index=1.8
- pipelined_m [data_width=21 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1650, accuracy_bits=15.4, luts=1236, ffs=414, throughput_msps=89.6, max_abs_err=2.27e-05 (2^-15.43), power_index=1.99
- pipelined_m [data_width=19 n_iter=20 angle_guard=3 frac_guard=4 rounding=round m=4] luts_plus_ffs=1938, accuracy_bits=16.5, luts=1527, ffs=411, throughput_msps=89.6, max_abs_err=1.08e-05 (2^-16.50), power_index=2.33
- pipelined_m [data_width=26 n_iter=20 angle_guard=-1 frac_guard=2 rounding=round m=4] luts_plus_ffs=2296, accuracy_bits=18.6, luts=1802, ffs=494, throughput_msps=86, max_abs_err=2.52e-06 (2^-18.60), power_index=2.76
- pipelined_m [data_width=27 n_iter=24 angle_guard=1 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=3036, accuracy_bits=22.1, luts=2235, ffs=801, throughput_msps=110, max_abs_err=2.3e-07 (2^-22.05), power_index=3.65
- pipelined_m [data_width=28 n_iter=24 angle_guard=4 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3295, accuracy_bits=22.7, luts=2429, ffs=866, throughput_msps=106, max_abs_err=1.42e-07 (2^-22.74), power_index=3.97
- pipelined_m [data_width=28 n_iter=26 angle_guard=3 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3572, accuracy_bits=24.1, luts=2613, ffs=958, throughput_msps=106, max_abs_err=5.73e-08 (2^-24.06), power_index=4.3
- pipelined_m [data_width=28 n_iter=30 angle_guard=3 frac_guard=4 rounding=round m=3] luts_plus_ffs=4230, accuracy_bits=25.3, luts=3151, ffs=1080, throughput_msps=106, max_abs_err=2.41e-08 (2^-25.31), power_index=5.09
Front coverage: luts_plus_ffs 1165..4230 (HV reference 4000); accuracy_bits 12..25.3 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- iterative: 5 evals, 0 feasible; max throughput seen 15.3 MSPS; best accuracy 13.91 bits
- unrolled_k: 10 evals, 0 feasible; max throughput seen 13.1 MSPS; best accuracy 13.26 bits
- pipelined: 93 evals, 68 feasible; max throughput seen 273 MSPS; best accuracy 15.64 bits; best feasible luts_plus_ffs=1713; feasible ranges: data_width 17..21, n_iter 14..22, angle_guard -2..3, frac_guard 0..3
- pipelined_m: 292 evals, 205 feasible; max throughput seen 171 MSPS; best accuracy 25.31 bits; best feasible luts_plus_ffs=1165; feasible ranges: data_width 16..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 6 (failed/unparsed attempts: 1)
- tokens: 15743 in, 36834 out
- provider-reported cost: $0.0251
- full prompts and replies: `llm_trace.jsonl`

