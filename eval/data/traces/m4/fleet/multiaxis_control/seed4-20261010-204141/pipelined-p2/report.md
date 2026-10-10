# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
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
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=15,n_iter=15,angle_guard=2,frac_guard=4,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 937 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 274 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.46 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00024 (2^-12.03) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 1.96 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 5.35e-05 (2^-14.19) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 0.438 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 12 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (18 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=15,angle_guard=2,frac_guard=4,rounding=round,m=4` | 937 | 274 | 93.6 | 6 | 1.46 | 0.00024 (2^-12.03) | 12.03 |
| 1 | `pipelined_m:data_width=16,n_iter=15,angle_guard=3,frac_guard=2,rounding=round,m=4` | 939 | 280 | 93.6 | 6 | 1.47 | 0.000128 (2^-12.93) | 12.93 |
| 2 | `pipelined_m:data_width=19,n_iter=15,angle_guard=3,frac_guard=0,rounding=trunc,m=4` | 979 | 309 | 93.6 | 6 | 1.55 | 0.000109 (2^-13.17) | 13.17 |
| 3 | `pipelined_m:data_width=18,n_iter=15,angle_guard=2,frac_guard=3,rounding=trunc,m=4` | 1008 | 309 | 93.6 | 6 | 1.59 | 8.58e-05 (2^-13.51) | 13.51 |
| 4 | `pipelined_m:data_width=19,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1008 | 313 | 93.6 | 6 | 1.59 | 8.04e-05 (2^-13.60) | 13.60 |
| 5 | `pipelined_m:data_width=19,n_iter=15,angle_guard=3,frac_guard=3,rounding=trunc,m=4` | 1067 | 327 | 93.6 | 6 | 1.68 | 7.13e-05 (2^-13.78) | 13.78 |
| 6 | `pipelined_m:data_width=20,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=3` | 1067 | 405 | 119.3 | 7 | 1.77 | 6.78e-05 (2^-13.85) | 13.85 |
| 7 | `pipelined_m:data_width=22,n_iter=15,angle_guard=1,frac_guard=3,rounding=trunc,m=3` | 1171 | 442 | 114.5 | 7 | 1.94 | 6.3e-05 (2^-13.95) | 13.95 |
| 8 | `pipelined_m:data_width=19,n_iter=17,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1226 | 394 | 93.6 | 7 | 1.95 | 2.76e-05 (2^-15.14) | 15.14 |
| 9 | `pipelined_m:data_width=22,n_iter=20,angle_guard=0,frac_guard=4,rounding=trunc,m=4` | 1607 | 445 | 89.6 | 7 | 2.47 | 7.68e-06 (2^-16.99) | 16.99 |
| 10 | `pipelined_m:data_width=22,n_iter=20,angle_guard=2,frac_guard=2,rounding=round,m=3` | 1613 | 600 | 114.5 | 9 | 2.66 | 4.44e-06 (2^-17.78) | 17.78 |
| 11 | `pipelined_m:data_width=22,n_iter=21,angle_guard=1,frac_guard=3,rounding=round,m=4` | 1717 | 525 | 89.6 | 8 | 2.7 | 4.01e-06 (2^-17.93) | 17.93 |
| 12 | `pipelined_m:data_width=22,n_iter=21,angle_guard=2,frac_guard=2,rounding=round,m=3` | 1695 | 600 | 114.5 | 9 | 2.76 | 3.49e-06 (2^-18.13) | 18.13 |
| 13 | `pipelined_m:data_width=28,n_iter=21,angle_guard=1,frac_guard=0,rounding=trunc,m=3` | 1923 | 706 | 110.0 | 9 | 3.16 | 1.09e-06 (2^-19.81) | 19.81 |
| 14 | `pipelined_m:data_width=24,n_iter=26,angle_guard=3,frac_guard=2,rounding=round,m=2` | 2295 | 1174 | 152.6 | 15 | 4.18 | 4.95e-07 (2^-20.95) | 20.95 |
| 15 | `pipelined_m:data_width=25,n_iter=29,angle_guard=3,frac_guard=2,rounding=round,m=3` | 2654 | 946 | 110.0 | 12 | 4.33 | 2.93e-07 (2^-21.71) | 21.71 |
| 16 | `pipelined_m:data_width=27,n_iter=29,angle_guard=3,frac_guard=0,rounding=round,m=3` | 2661 | 973 | 110.0 | 12 | 4.37 | 2.03e-07 (2^-22.23) | 22.23 |
| 17 | `pipelined_m:data_width=28,n_iter=26,angle_guard=2,frac_guard=0,rounding=trunc,m=2` | 2429 | 1276 | 152.6 | 15 | 4.46 | 2.01e-07 (2^-22.24) | 22.24 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Only the two pipelined families can plausibly satisfy the 32-request burst: both emit 1 result/cycle, so 32 requests drain in ~32 cycles and the binding constraint is sys_p99_batch_us <= 0.44us, i.e. latency+32 cycles must fit in 0.44us at Fmax. Accuracy (max_abs_err <= 2^-12) needs W >= ~13-14 and N >= ~12, so I centre the search on the feasible accuracy boundary (W 13-20, N 11-20) and let the exact model place the guard-bit/rounding choices; the upper ends of W/N are kept because accuracy_bits is a second HV objective with reference 12, so points with accuracy above 12 still add hypervolume. pipelined_m gets the larger share since it dominates the merged front and holds the cheapest feasible design, with the full m range left open to expose the latency-vs-Fmax trade-off that decides whether a cheap design survives the L2 system simulation.*)
- `pipelined_m` (65 evals): data_width=13..20, n_iter=11..20, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* pipelined_m owns 11 of the 14 merged-front points and the cheapest feasible design (1258 LUT+FF) because registering every m stages cuts FFs and latency while still yielding 1 result/cycle; the full m range is kept so Optuna can trade the 0.44us batch constraint (favours large m -> low latency) against Fmax (favours small m).
- `pipelined` (35 evals): data_width=13..20, n_iter=11..20, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round. *Why:* pipelined still contributes 3 of the 14 merged-front points and gives a different latency/area trade-off (N+2 latency, one register per stage); a smaller share is enough to keep its slice of the front mapped.

**Result (code):** 100 evaluations this round, 100 total; 32 feasible; hypervolume 8107 (n/a).

**LLM decision:** `map_front` — All 7 front designs are pipelined_m and the front spans only luts_plus_ffs 1219..1620 against an HV reference of 4000, with accuracy 12.9..15.1 bits against a reference of 12 — i.e. the front covers only a small slice of the luts_plus_ffs objective range, exactly the condition for a full-front mapping round. The trade-off curve is clearly under-sampled: the best accuracy seen (16.56 bits) is not on the front, and pipelined's best feasible luts_plus_ffs (1723) is worse than pipelined_m's 1219, so the two families on the front have not been jointly mapped. The throughput constraint (>=32 MSPS) is met by every evaluation (best 273), while the binding constraints are accuracy (46% violate) and sys_p99_batch_us (36% violate, best 0.158 vs 0.44) — so the feasible region is defined by accuracy/system timing, not throughput, and iterative/unrolled_k (N+3 and ceil(N/k)+3 cycles/result, well under 32 MSPS at these N) cannot enter the front. With 100 of 200 evals left, the best use is to let NSGA-II map the whole front over the full ranges of pipelined and pipelined_m, seeded with the current front, rather than narrowing around a 7-point slice.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 8107 (gain this round: n/a (first round)).
Feasible designs: 32 of 100 evaluations (28 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 46% violate; best seen 1.04e-05 (2^-16.56)
- sys_p99_batch_us <= 0.44: 36% violate; best seen 0.158

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1219, accuracy_bits=12.9, luts=939, ffs=280, throughput_msps=93.6, max_abs_err=0.000128 (2^-12.93), power_index=1.47
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1288, accuracy_bits=13.2, luts=979, ffs=309, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=1.55
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1317, accuracy_bits=13.5, luts=1008, ffs=309, throughput_msps=93.6, max_abs_err=8.58e-05 (2^-13.51), power_index=1.59
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1321, accuracy_bits=13.6, luts=1008, ffs=313, throughput_msps=93.6, max_abs_err=8.04e-05 (2^-13.60), power_index=1.59
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1394, accuracy_bits=13.8, luts=1067, ffs=327, throughput_msps=93.6, max_abs_err=7.13e-05 (2^-13.78), power_index=1.68
- pipelined_m [data_width=19 n_iter=15 angle_guard=2 frac_guard=3 rounding=round m=3] luts_plus_ffs=1490, accuracy_bits=13.8, luts=1093, ffs=398, throughput_msps=119, max_abs_err=7.02e-05 (2^-13.80), power_index=1.79
- pipelined_m [data_width=19 n_iter=17 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1620, accuracy_bits=15.1, luts=1226, ffs=394, throughput_msps=93.6, max_abs_err=2.76e-05 (2^-15.14), power_index=1.95
Front coverage: luts_plus_ffs 1219..1620 (HV reference 4000); accuracy_bits 12.9..15.1 (HV reference 12); data_width on the front 16..19 (registry 8..28).

Per family:
- pipelined: 35 evals, 19 feasible; max throughput seen 273 MSPS; best accuracy 15.06 bits; best feasible luts_plus_ffs=1723; feasible ranges: data_width 17..20, n_iter 14..19, angle_guard -2..3, frac_guard 0..3
- pipelined_m: 65 evals, 13 feasible; max throughput seen 171 MSPS; best accuracy 16.56 bits; best feasible luts_plus_ffs=1219; feasible ranges: data_width 16..20, n_iter 14..18, angle_guard -2..3, frac_guard 0..3, m 3..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `pipelined_m` (20 evals): data_width=15..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (7 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 41 feasible; hypervolume 1.325e+04 (+63.5%).

**LLM decision:** `map_front` — Round 2 done: 120/200 evals used, 2 rounds left, HV 1.325e4 (+63.5%). The feasible front has 9 designs but is unevenly covered: 7 designs crowd the low-area end (1219–1620 luts+ffs, 12.9–15.1 bits) while the high-accuracy half is nearly empty (1620 → 2052 → 3705 luts+ffs, 15.1 → 17 → 22.2 bits). Since HV is scored against ref (4000, 12), that 2052–3705 gap is the largest remaining HV opportunity, and the front already spans most of both objective ranges (1219..3705 of 4000; 12.9..22.2 of 12), so refining a narrow region has little upside. Both families on the front (pipelined, pipelined_m) are already explored, so there is no add_family move. The low-area end is pinned by the accuracy constraint (cheapest design is 12.9 bits vs the 2^-12 = 12-bit floor), so it cannot be pushed much cheaper. The system constraint is the real risk: every cheap front design runs at ~93.6 MSPS (m=4), giving a batch time of ~0.395 us against the 0.44 us bound — only ~10% margin on an L1 bound that is optimistic by construction, and the note warns such designs can be lost at L2. Mapping the full ranges (including m 2..8, which raises Fmax/throughput, e.g. m=3 already gives 119 MSPS and m=2 gives 153 MSPS) will both fill the HV gap and populate robust high-throughput alternatives for the L2 re-selection.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.325e+04 (gain this round: +63.5%).
Feasible designs: 41 of 120 evaluations (36 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 42% violate; best seen 2.01e-07 (2^-22.24)
- sys_p99_batch_us <= 0.44: 37% violate; best seen 0.158

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1219, accuracy_bits=12.9, luts=939, ffs=280, throughput_msps=93.6, max_abs_err=0.000128 (2^-12.93), power_index=1.47
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1288, accuracy_bits=13.2, luts=979, ffs=309, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=1.55
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1317, accuracy_bits=13.5, luts=1008, ffs=309, throughput_msps=93.6, max_abs_err=8.58e-05 (2^-13.51), power_index=1.59
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1321, accuracy_bits=13.6, luts=1008, ffs=313, throughput_msps=93.6, max_abs_err=8.04e-05 (2^-13.60), power_index=1.59
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1394, accuracy_bits=13.8, luts=1067, ffs=327, throughput_msps=93.6, max_abs_err=7.13e-05 (2^-13.78), power_index=1.68
- pipelined_m [data_width=19 n_iter=15 angle_guard=2 frac_guard=3 rounding=round m=3] luts_plus_ffs=1490, accuracy_bits=13.8, luts=1093, ffs=398, throughput_msps=119, max_abs_err=7.02e-05 (2^-13.80), power_index=1.79
- pipelined_m [data_width=19 n_iter=17 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1620, accuracy_bits=15.1, luts=1226, ffs=394, throughput_msps=93.6, max_abs_err=2.76e-05 (2^-15.14), power_index=1.95
- pipelined_m [data_width=22 n_iter=20 angle_guard=0 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=2052, accuracy_bits=17, luts=1607, ffs=445, throughput_msps=89.6, max_abs_err=7.68e-06 (2^-16.99), power_index=2.47
- pipelined_m [data_width=28 n_iter=26 angle_guard=2 frac_guard=0 rounding=trunc m=2] luts_plus_ffs=3705, accuracy_bits=22.2, luts=2429, ffs=1276, throughput_msps=153, max_abs_err=2.01e-07 (2^-22.24), power_index=4.46
Front coverage: luts_plus_ffs 1219..3705 (HV reference 4000); accuracy_bits 12.9..22.2 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- pipelined: 35 evals, 19 feasible; max throughput seen 273 MSPS; best accuracy 15.06 bits; best feasible luts_plus_ffs=1723; feasible ranges: data_width 17..20, n_iter 14..19, angle_guard -2..3, frac_guard 0..3
- pipelined_m: 85 evals, 22 feasible; max throughput seen 171 MSPS; best accuracy 22.24 bits; best feasible luts_plus_ffs=1219; feasible ranges: data_width 16..28, n_iter 14..29, angle_guard -2..3, frac_guard 0..4, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (80 evals): data_width=15..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (9 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 90 feasible; hypervolume 1.713e+04 (+29.3%).

**LLM decision:** `stop` — Budget is exhausted (200/200 evals, round 3 of 4 complete), so this is the terminal decision point. The spec is feasible, not infeasible: all three constraints are met with margin by designs on the front — throughput_msps best 273 vs >=32 (0% violations), max_abs_err best 3.14e-08 vs <=2.44e-04 (2^-12), and sys_p99_batch_us best 0.158 us vs <=0.44 us. The feasible front is well populated (90 feasible / 78 unique, 18 Pareto designs) and spans luts_plus_ffs 1211..3705 against the HV reference 4000, with accuracy_bits 12..22.2 against reference 12, i.e. it covers both objective ranges rather than a single corner, and hypervolume improved +29.3% this round. The selection rule (min luts_plus_ffs) lands on pipelined_m [W=15 N=15 angle_guard=2 frac_guard=4 round m=4] at luts_plus_ffs=1211, accuracy_bits=12.03 (max_abs_err 2.40e-04, just inside the 2^-12 limit) and throughput 93.6 MSPS, comfortably above the 32 MSPS floor. The only residual risk is that this cheapest design's sys_p99_batch_us margin is an L1 analytic bound and will be re-checked by L2 simulation, but that re-selection is handled by code after this loop, and no further exploration budget remains to change the front. Stopping is therefore the correct terminal action.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.713e+04 (gain this round: +29.3%).
Feasible designs: 90 of 200 evaluations (78 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 33% violate; best seen 3.14e-08 (2^-24.93)
- sys_p99_batch_us <= 0.44: 32% violate; best seen 0.158

Pareto front (feasible, 18 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=15 angle_guard=2 frac_guard=4 rounding=round m=4] luts_plus_ffs=1211, accuracy_bits=12, luts=937, ffs=274, throughput_msps=93.6, max_abs_err=0.00024 (2^-12.03), power_index=1.46
- pipelined_m [data_width=19 n_iter=15 angle_guard=3 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1288, accuracy_bits=13.2, luts=979, ffs=309, throughput_msps=93.6, max_abs_err=0.000109 (2^-13.17), power_index=1.55
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1321, accuracy_bits=13.6, luts=1008, ffs=313, throughput_msps=93.6, max_abs_err=8.04e-05 (2^-13.60), power_index=1.59
- pipelined_m [data_width=20 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=1472, accuracy_bits=13.8, luts=1067, ffs=405, throughput_msps=119, max_abs_err=6.78e-05 (2^-13.85), power_index=1.77
- pipelined_m [data_width=19 n_iter=17 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1620, accuracy_bits=15.1, luts=1226, ffs=394, throughput_msps=93.6, max_abs_err=2.76e-05 (2^-15.14), power_index=1.95
- pipelined_m [data_width=22 n_iter=20 angle_guard=0 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=2052, accuracy_bits=17, luts=1607, ffs=445, throughput_msps=89.6, max_abs_err=7.68e-06 (2^-16.99), power_index=2.47
- pipelined_m [data_width=22 n_iter=21 angle_guard=1 frac_guard=3 rounding=round m=4] luts_plus_ffs=2241, accuracy_bits=17.9, luts=1717, ffs=525, throughput_msps=89.6, max_abs_err=4.01e-06 (2^-17.93), power_index=2.7
- pipelined_m [data_width=28 n_iter=21 angle_guard=1 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=2629, accuracy_bits=19.8, luts=1923, ffs=706, throughput_msps=110, max_abs_err=1.09e-06 (2^-19.81), power_index=3.16
- pipelined_m [data_width=25 n_iter=29 angle_guard=3 frac_guard=2 rounding=round m=3] luts_plus_ffs=3601, accuracy_bits=21.7, luts=2654, ffs=946, throughput_msps=110, max_abs_err=2.93e-07 (2^-21.71), power_index=4.33
- pipelined_m [data_width=28 n_iter=26 angle_guard=2 frac_guard=0 rounding=trunc m=2] luts_plus_ffs=3705, accuracy_bits=22.2, luts=2429, ffs=1276, throughput_msps=153, max_abs_err=2.01e-07 (2^-22.24), power_index=4.46
Front coverage: luts_plus_ffs 1211..3705 (HV reference 4000); accuracy_bits 12..22.2 (HV reference 12); data_width on the front 15..28 (registry 8..28).

Per family:
- pipelined: 35 evals, 19 feasible; max throughput seen 273 MSPS; best accuracy 15.06 bits; best feasible luts_plus_ffs=1723; feasible ranges: data_width 17..20, n_iter 14..19, angle_guard -2..3, frac_guard 0..3
- pipelined_m: 165 evals, 71 feasible; max throughput seen 171 MSPS; best accuracy 24.93 bits; best feasible luts_plus_ffs=1211; feasible ranges: data_width 15..28, n_iter 14..30, angle_guard -2..3, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 12810 in, 12202 out
- provider-reported cost: $0.0090
- full prompts and replies: `llm_trace.jsonl`

