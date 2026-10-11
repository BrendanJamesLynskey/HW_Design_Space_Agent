# DSE run: asic_multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_multiaxis_control: Shared sin/cos unit in sky130 standard cells for a 16-axis motor-control loop: a 1 MHz control tick issues 32 requests at once; all 32 results must be back within 0.5 us of the tick (p99 over ticks). Max error <= 2^-12. Minimise area.
  target: asic-sky130hd
  constraint: throughput_msps >= 32
  constraint: max_abs_err <= 0.000244141
  constraint: sys_p99_batch_us <= 0.5
  objective: min area_um2 (HV ref 100000)
  objective: max accuracy_bits (HV ref 12)
  select: min area_um2
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average)
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined:data_width=18,n_iter=15,angle_guard=-1,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 40877 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10890 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 885 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 119 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.34 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000201 (2^-12.28) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 13.2 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 4.45e-05 (2^-14.46) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 2.92 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (11 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=15,angle_guard=-1,frac_guard=0,rounding=round` | 40877 | 885 | 143.2 | 17 | 2.34 | 0.000201 (2^-12.28) | 12.28 |
| 1 | `pipelined:data_width=19,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` | 44090 | 934 | 127.5 | 16 | 2.49 | 0.000136 (2^-12.84) | 12.84 |
| 2 | `pipelined:data_width=20,n_iter=14,angle_guard=3,frac_guard=2,rounding=round` | 47880 | 1013 | 118.9 | 16 | 2.7 | 0.000125 (2^-12.97) | 12.97 |
| 3 | `pipelined:data_width=19,n_iter=17,angle_guard=1,frac_guard=0,rounding=trunc` | 50411 | 1086 | 132.4 | 19 | 2.88 | 7.8e-05 (2^-13.65) | 13.65 |
| 4 | `pipelined:data_width=20,n_iter=15,angle_guard=1,frac_guard=3,rounding=round` | 51273 | 1081 | 118.9 | 17 | 2.89 | 6.87e-05 (2^-13.83) | 13.83 |
| 5 | `pipelined:data_width=18,n_iter=17,angle_guard=1,frac_guard=2,rounding=round` | 51980 | 1097 | 132.4 | 19 | 2.93 | 5.95e-05 (2^-14.04) | 14.04 |
| 6 | `pipelined:data_width=20,n_iter=17,angle_guard=1,frac_guard=0,rounding=round` | 52751 | 1137 | 127.5 | 19 | 3.02 | 3.32e-05 (2^-14.88) | 14.88 |
| 7 | `pipelined:data_width=20,n_iter=18,angle_guard=3,frac_guard=0,rounding=round` | 57601 | 1239 | 118.9 | 20 | 3.29 | 2.54e-05 (2^-15.26) | 15.26 |
| 8 | `pipelined:data_width=20,n_iter=18,angle_guard=3,frac_guard=2,rounding=round` | 61802 | 1304 | 118.9 | 20 | 3.48 | 1.42e-05 (2^-16.11) | 16.11 |
| 9 | `pipelined:data_width=21,n_iter=21,angle_guard=4,frac_guard=1,rounding=round` | 74320 | 1567 | 111.3 | 23 | 4.19 | 5.85e-06 (2^-17.38) | 17.38 |
| 10 | `pipelined:data_width=20,n_iter=23,angle_guard=3,frac_guard=4,rounding=round` | 83286 | 1750 | 115.0 | 25 | 4.68 | 5.15e-06 (2^-17.57) | 17.57 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Two families only, both the 1-result/cycle kind, because the binding system constraint is the 1 MHz tick releasing 32 requests that must all land within 0.5 us: a design that emits one result every k cycles would need roughly 32*k cycles for the burst. Pipelined/pipelined_m emit one per cycle, so the burst reduces to (n_iter(+ceil/m)+2+31)/fmax <= 0.5 us plus a trivial 32 Msps throughput floor (fmax >= 32 MHz, comfortably below any realistic pipelined Fmax). Accuracy is family-independent (identical bits for the same data_width/n_iter/angle_guard/frac_guard/rounding) and the spec floor max_abs_err <= 2^-12 means data_width >= 14 with round; the search therefore only has to trade n_iter/width/guards against area. pipelined already owns the entire merged front (14/14, best 45673 um^2) and has 74% feasibility, so it gets ~72% of the budget and a broad-but-focused box whose upper n_iter/width edges are clipped where accuracy saturates and area only grows; ~28% goes to pipelined_m, the only plausible route to a smaller FF count, restricted to small m and small guards so that Fmax can still clear the burst window, with the intent to reallocate that share to pipelined next round if it again yields zero feasible points. Round-1 plan: 100 evals split pipelined 72 / pipelined_m 28, leaving ~72/28 for rounds 2-3 to refine the front before the reserved full-range mapping pass.*)
- `pipelined` (72 evals): data_width=13..20, n_iter=8..22, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round. *Why:* The only family with proven feasibility and the sole contributor to the merged front (54/73 feasible, best area 45673 um^2, 14/14 front points). It is also the only 1-result/cycle family whose Fmax comfortably clears the batch window: with 1 result/cycle the 32-request tick needs (n_iter+33)/fmax_us <= 0.5, i.e. fmax >= 2*(n_iter+33) MHz (>= ~102 MHz at n_iter=18), which a fully-pipelined micro-rotation chain reaches even at the wide end, and throughput >= 32 Msps is automatic. Spreading data_width 13-20 spans the 2^-12 error floor (LSB 2^-(W-2), so W>=14 is needed and W>=15 gives rounding margin) while staying out of the large-W/high-N corner that only buys area; n_iter 8-22 brackets the convergence-limited accuracy knee so the low-area end of the front is mapped; angle_guard and frac_guard are kept near zero because they cost datapath width without adding recoverable accuracy. This is where the extra evals should go: refine the low-area edge of the accuracy-vs-area trade-off, which is what 'select: min area' consumes, while preserving HV coverage of the accuracy tail.
- `pipelined_m` (28 evals): data_width=13..20, n_iter=8..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..5. *Why:* It shares pipelined's bit-exact accuracy and its 1-result/cycle rate, so it is the only other family that can satisfy the 32-in-0.5 us burst at all, and registering every m stages replaces ~n_iter register stages with ~n_iter/m, which is exactly the lever for 'min area' if Fmax survives. It is 0/27 feasible so far, so the share is deliberately modest and the ranges are pushed to survivability: small m (2-5, with m>=2 as the only regime that keeps the critical path short enough to still meet fmax >= 2*(ceil(n_iter/m)+33) MHz for the burst) and small guard bits (the m>1 chain already lengthens the combinational path, so extra angle/frac width is pure cost). If round 1 confirms no feasible pipelined_m point, its remaining share should be folded into pipelined rather than spending it on the m>=6 regime, which can only lower Fmax further.

**Result (code):** 100 evaluations this round, 100 total; 38 feasible; hypervolume 1.923e+05 (n/a).

**LLM decision:** `map_front` — Round 1 leaves 100 of 200 evals. The feasible front is entirely pipelined (8 designs) and covers only a slice of both objective ranges: area_um2 40877..61802 against the HV reference 100000, and accuracy_bits 12.3..16.1 while the registry permits far higher accuracy (data_width on the front is only 17..20 of 8..28). The min-area corner (40877 um^2, 12.3 bits) already sits just above the 2^-12 error constraint, so there is little room to shrink area, but the curve is truncated on the high-accuracy side, which is exactly where hypervolume is being left on the table. pipelined_m produced 0 feasible designs in 28 evals (best accuracy 13.02 bits, max throughput 91.1 MSPS) so it is not obviously a source of new front points, and no family remains unexplored. The best use of the remaining budget is therefore to let NSGA-II map the full front over the full ranges of the pipelined family (seeded with the current front), extending accuracy_bits well past 16 and filling the area range up to the reference point, rather than narrowing around the already-dense low-area region.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.923e+05 (gain this round: n/a (first round)).
Feasible designs: 38 of 100 evaluations (32 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 3% violate; best seen 180
- max_abs_err <= 0.000244141: 60% violate; best seen 1.42e-05 (2^-16.11)
- sys_p99_batch_us <= 0.5: 23% violate; best seen 0.263

Pareto front (feasible, 8 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=-1 frac_guard=0 rounding=round] area_um2=40877, accuracy_bits=12.3, ffs=885, throughput_msps=143, max_abs_err=0.000201 (2^-12.28), power_index=2.34
- pipelined [data_width=18 n_iter=17 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=48071, accuracy_bits=12.4, ffs=1036, throughput_msps=138, max_abs_err=0.000179 (2^-12.45), power_index=2.75
- pipelined [data_width=17 n_iter=17 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=48677, accuracy_bits=12.8, ffs=1045, throughput_msps=138, max_abs_err=0.000144 (2^-12.76), power_index=2.78
- pipelined [data_width=19 n_iter=17 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=50411, accuracy_bits=13.6, ffs=1086, throughput_msps=132, max_abs_err=7.8e-05 (2^-13.65), power_index=2.88
- pipelined [data_width=18 n_iter=17 angle_guard=1 frac_guard=2 rounding=round] area_um2=51980, accuracy_bits=14, ffs=1097, throughput_msps=132, max_abs_err=5.95e-05 (2^-14.04), power_index=2.93
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] area_um2=52751, accuracy_bits=14.9, ffs=1137, throughput_msps=128, max_abs_err=3.32e-05 (2^-14.88), power_index=3.02
- pipelined [data_width=20 n_iter=18 angle_guard=3 frac_guard=0 rounding=round] area_um2=57601, accuracy_bits=15.3, ffs=1239, throughput_msps=119, max_abs_err=2.54e-05 (2^-15.26), power_index=3.29
- pipelined [data_width=20 n_iter=18 angle_guard=3 frac_guard=2 rounding=round] area_um2=61802, accuracy_bits=16.1, ffs=1304, throughput_msps=119, max_abs_err=1.42e-05 (2^-16.11), power_index=3.48
Front coverage: area_um2 40877..61802 (HV reference 100000); accuracy_bits 12.3..16.1 (HV reference 12); data_width on the front 17..20 (registry 8..28).

Per family:
- pipelined: 72 evals, 38 feasible; max throughput seen 180 MSPS; best accuracy 16.11 bits; best feasible area_um2=40877; feasible ranges: data_width 17..20, n_iter 15..22, angle_guard -2..3, frac_guard 0..3
- pipelined_m: 28 evals, 0 feasible; max throughput seen 91.1 MSPS; best accuracy 13.02 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `pipelined` (10 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (8 front designs; box front_anchored)
- `pipelined_m` (10 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 20 evaluations this round, 120 total; 45 feasible; hypervolume 1.923e+05 (+0.0%).

**LLM decision:** `map_front` — Round 2 produced +0.0% hypervolume gain, so refining the current box is no longer paying off, yet the front is badly truncated in one objective: it spans accuracy_bits 12.3..16.1 while the search has already seen feasible-quality designs up to 20.32 bits (pipelined) and 21.74 bits (pipelined_m), and area only reaches 61802 against the HV reference of 100000. The 8-design front is therefore covering only a small slice of the achievable accuracy range, and the 37 dominated feasible designs suggest the high-accuracy/large-area region was never properly sampled. All 8 front members are `pipelined` (data_width 17..20, n_iter 15..18, angle_guard -1..3, frac_guard 0..2), while `pipelined_m` yielded 0 feasible designs in 38 evals (max throughput 91.1 MSPS, so it is not throughput-limited) and should not be seeded. With 80 of 200 evals left, the best use is a code-driven NSGA-II coverage search over the full pipelined ranges seeded with the current front, to extend the curve toward the high-accuracy end and fill the area gap before the reserved mapping budget is exhausted.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.923e+05 (gain this round: +0.0%).
Feasible designs: 45 of 120 evaluations (39 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 6% violate; best seen 180
- max_abs_err <= 0.000244141: 53% violate; best seen 2.85e-07 (2^-21.74)
- sys_p99_batch_us <= 0.5: 28% violate; best seen 0.263

Pareto front (feasible, 8 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=-1 frac_guard=0 rounding=round] area_um2=40877, accuracy_bits=12.3, ffs=885, throughput_msps=143, max_abs_err=0.000201 (2^-12.28), power_index=2.34
- pipelined [data_width=18 n_iter=17 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=48071, accuracy_bits=12.4, ffs=1036, throughput_msps=138, max_abs_err=0.000179 (2^-12.45), power_index=2.75
- pipelined [data_width=17 n_iter=17 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=48677, accuracy_bits=12.8, ffs=1045, throughput_msps=138, max_abs_err=0.000144 (2^-12.76), power_index=2.78
- pipelined [data_width=19 n_iter=17 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=50411, accuracy_bits=13.6, ffs=1086, throughput_msps=132, max_abs_err=7.8e-05 (2^-13.65), power_index=2.88
- pipelined [data_width=18 n_iter=17 angle_guard=1 frac_guard=2 rounding=round] area_um2=51980, accuracy_bits=14, ffs=1097, throughput_msps=132, max_abs_err=5.95e-05 (2^-14.04), power_index=2.93
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] area_um2=52751, accuracy_bits=14.9, ffs=1137, throughput_msps=128, max_abs_err=3.32e-05 (2^-14.88), power_index=3.02
- pipelined [data_width=20 n_iter=18 angle_guard=3 frac_guard=0 rounding=round] area_um2=57601, accuracy_bits=15.3, ffs=1239, throughput_msps=119, max_abs_err=2.54e-05 (2^-15.26), power_index=3.29
- pipelined [data_width=20 n_iter=18 angle_guard=3 frac_guard=2 rounding=round] area_um2=61802, accuracy_bits=16.1, ffs=1304, throughput_msps=119, max_abs_err=1.42e-05 (2^-16.11), power_index=3.48
Front coverage: area_um2 40877..61802 (HV reference 100000); accuracy_bits 12.3..16.1 (HV reference 12); data_width on the front 17..20 (registry 8..28).

Per family:
- pipelined: 82 evals, 45 feasible; max throughput seen 180 MSPS; best accuracy 20.32 bits; best feasible area_um2=40877; feasible ranges: data_width 17..24, n_iter 14..28, angle_guard -2..4, frac_guard 0..3
- pipelined_m: 38 evals, 0 feasible; max throughput seen 91.1 MSPS; best accuracy 21.74 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined` (40 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (8 front designs; box front_anchored)
- `pipelined_m` (40 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 80 evaluations this round, 200 total; 76 feasible; hypervolume 2.312e+05 (+20.3%).

**LLM decision:** `stop` — Budget is exhausted (200/200 evals) and this is the final round, so the only valid choices are stop or infeasible. Infeasible is ruled out by evidence: 76 of 200 evaluations are feasible and the Pareto front holds 11 feasible designs, with every constraint satisfiable — throughput best seen 180 MSPS vs the >=32 requirement, max_abs_err best 2.85e-07 vs the <=2.44e-04 limit, and sys_p99_batch_us best 0.263 us vs the <=0.5 us bound. The front spans area_um2 40877..83286 against the HV reference 100000 and accuracy_bits 12.3..17.6 against reference 12, and hypervolume gained +20.3% this round, so the front is well covered rather than truncated. The selection rule (min area_um2) is already served by the cheapest front point, pipelined [data_width=18 n_iter=15 angle_guard=-1 frac_guard=0 rounding=round] at area_um2=40877 with accuracy_bits=12.3 (max_abs_err 2.01e-04, still inside the 2^-12 limit) and throughput 143 MSPS. Note the L2 caveat: this cheapest point's sys_p99_batch_us margin is the tightest on the front, so the post-selection SimPy re-selection may fall back to a slightly larger front point; that is handled by the reserved L2 step, not by further exploration. Stop.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 2.312e+05 (gain this round: +20.3%).
Feasible designs: 76 of 200 evaluations (64 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 18% violate; best seen 180
- max_abs_err <= 0.000244141: 38% violate; best seen 2.85e-07 (2^-21.74)
- sys_p99_batch_us <= 0.5: 40% violate; best seen 0.263

Pareto front (feasible, 11 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=-1 frac_guard=0 rounding=round] area_um2=40877, accuracy_bits=12.3, ffs=885, throughput_msps=143, max_abs_err=0.000201 (2^-12.28), power_index=2.34
- pipelined [data_width=19 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=44090, accuracy_bits=12.8, ffs=934, throughput_msps=128, max_abs_err=0.000136 (2^-12.84), power_index=2.49
- pipelined [data_width=20 n_iter=14 angle_guard=3 frac_guard=2 rounding=round] area_um2=47880, accuracy_bits=13, ffs=1013, throughput_msps=119, max_abs_err=0.000125 (2^-12.97), power_index=2.7
- pipelined [data_width=19 n_iter=17 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=50411, accuracy_bits=13.6, ffs=1086, throughput_msps=132, max_abs_err=7.8e-05 (2^-13.65), power_index=2.88
- pipelined [data_width=20 n_iter=15 angle_guard=1 frac_guard=3 rounding=round] area_um2=51273, accuracy_bits=13.8, ffs=1081, throughput_msps=119, max_abs_err=6.87e-05 (2^-13.83), power_index=2.89
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] area_um2=52751, accuracy_bits=14.9, ffs=1137, throughput_msps=128, max_abs_err=3.32e-05 (2^-14.88), power_index=3.02
- pipelined [data_width=20 n_iter=18 angle_guard=3 frac_guard=0 rounding=round] area_um2=57601, accuracy_bits=15.3, ffs=1239, throughput_msps=119, max_abs_err=2.54e-05 (2^-15.26), power_index=3.29
- pipelined [data_width=20 n_iter=18 angle_guard=3 frac_guard=2 rounding=round] area_um2=61802, accuracy_bits=16.1, ffs=1304, throughput_msps=119, max_abs_err=1.42e-05 (2^-16.11), power_index=3.48
- pipelined [data_width=21 n_iter=21 angle_guard=4 frac_guard=1 rounding=round] area_um2=74320, accuracy_bits=17.4, ffs=1567, throughput_msps=111, max_abs_err=5.85e-06 (2^-17.38), power_index=4.19
- pipelined [data_width=20 n_iter=23 angle_guard=3 frac_guard=4 rounding=round] area_um2=83286, accuracy_bits=17.6, ffs=1750, throughput_msps=115, max_abs_err=5.15e-06 (2^-17.57), power_index=4.68
Front coverage: area_um2 40877..83286 (HV reference 100000); accuracy_bits 12.3..17.6 (HV reference 12); data_width on the front 18..21 (registry 8..28).

Per family:
- pipelined: 122 evals, 76 feasible; max throughput seen 180 MSPS; best accuracy 20.52 bits; best feasible area_um2=40877; feasible ranges: data_width 17..27, n_iter 14..28, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 78 evals, 0 feasible; max throughput seen 91.1 MSPS; best accuracy 21.74 bits
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 12733 in, 8292 out
- provider-reported cost: $0.0077
- full prompts and replies: `llm_trace.jsonl`

