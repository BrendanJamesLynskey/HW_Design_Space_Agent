# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
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
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=17,n_iter=14,angle_guard=3,frac_guard=1,rounding=trunc,m=3` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 855 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 350 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 119 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 119 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 58.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.45 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000231 (2^-12.08) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 7.58 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.88e-05 (2^-14.05) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.93 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.1 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (17 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 855 | 350 | 119.3 | 7 | 1.45 | 0.000231 (2^-12.08) | 12.08 |
| 1 | `pipelined_m:data_width=17,n_iter=14,angle_guard=3,frac_guard=4,rounding=trunc,m=3` | 937 | 374 | 119.3 | 7 | 1.58 | 0.000162 (2^-12.59) | 12.59 |
| 2 | `pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=2,rounding=round,m=4` | 1055 | 297 | 93.6 | 6 | 1.63 | 0.000102 (2^-13.25) | 13.25 |
| 3 | `pipelined_m:data_width=19,n_iter=15,angle_guard=0,frac_guard=2,rounding=round,m=3` | 1034 | 379 | 119.3 | 7 | 1.7 | 9.42e-05 (2^-13.37) | 13.37 |
| 4 | `pipelined_m:data_width=19,n_iter=15,angle_guard=1,frac_guard=2,rounding=round,m=3` | 1048 | 384 | 119.3 | 7 | 1.72 | 7.76e-05 (2^-13.65) | 13.65 |
| 5 | `pipelined_m:data_width=22,n_iter=15,angle_guard=0,frac_guard=2,rounding=trunc,m=4` | 1126 | 351 | 89.6 | 6 | 1.78 | 6.44e-05 (2^-13.92) | 13.92 |
| 6 | `pipelined_m:data_width=20,n_iter=16,angle_guard=0,frac_guard=2,rounding=round,m=4` | 1154 | 325 | 93.6 | 6 | 1.78 | 4.88e-05 (2^-14.32) | 14.32 |
| 7 | `pipelined_m:data_width=20,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc,m=2` | 1128 | 617 | 164.4 | 10 | 2.1 | 4.33e-05 (2^-14.50) | 14.50 |
| 8 | `pipelined_m:data_width=22,n_iter=17,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 1287 | 504 | 114.5 | 8 | 2.16 | 3.32e-05 (2^-14.88) | 14.88 |
| 9 | `pipelined_m:data_width=20,n_iter=19,angle_guard=0,frac_guard=3,rounding=round,m=4` | 1413 | 405 | 89.6 | 7 | 2.19 | 2.93e-05 (2^-15.06) | 15.06 |
| 10 | `pipelined_m:data_width=22,n_iter=18,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 1367 | 504 | 114.5 | 8 | 2.25 | 2.88e-05 (2^-15.08) | 15.08 |
| 11 | `pipelined_m:data_width=22,n_iter=18,angle_guard=3,frac_guard=3,rounding=trunc,m=3` | 1456 | 535 | 114.5 | 8 | 2.4 | 9.04e-06 (2^-16.75) | 16.75 |
| 12 | `pipelined_m:data_width=24,n_iter=21,angle_guard=1,frac_guard=3,rounding=trunc,m=3` | 1797 | 650 | 110.0 | 9 | 2.94 | 1.77e-06 (2^-19.11) | 19.11 |
| 13 | `pipelined_m:data_width=27,n_iter=25,angle_guard=-2,frac_guard=3,rounding=round,m=3` | 2364 | 886 | 110.0 | 11 | 3.91 | 9.46e-07 (2^-20.01) | 20.01 |
| 14 | `pipelined:data_width=28,n_iter=22,angle_guard=-1,frac_guard=3,rounding=trunc` | 2107 | 2119 | 242.0 | 24 | 5.09 | 6.36e-07 (2^-20.58) | 20.58 |
| 15 | `pipelined:data_width=24,n_iter=23,angle_guard=4,frac_guard=4,rounding=round` | 2142 | 2098 | 249.0 | 25 | 5.1 | 4.17e-07 (2^-21.19) | 21.19 |
| 16 | `pipelined:data_width=25,n_iter=25,angle_guard=4,frac_guard=3,rounding=round` | 2359 | 2310 | 249.0 | 27 | 5.62 | 2.16e-07 (2^-22.14) | 22.14 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec has two hard throughput/latency constraints (throughput_msps >= 32 and sys_p99_batch_us <= 0.44 for 32 back-to-back results) plus max_abs_err <= 2^-12. Only the 1-result/cycle families (pipelined, pipelined_m) can plausibly sustain 32 results/us, so I restrict to those two. The accuracy constraint (accuracy_bits >= 12) is the binding accuracy floor; I set n_iter >= 12 and data_width >= 14 so the search stays on the feasible side of the accuracy constraint and spends budget on the area-vs-accuracy trade-off (HV refs 4000 luts_plus_ffs and 12 accuracy_bits) rather than on infeasible low-accuracy corners. I split the budget 55/45 between pipelined (the throughput/latency-safe baseline that defines the upper accuracy/throughput envelope) and pipelined_m (the area-reduction variant via the m knob that can beat pipelined on luts_plus_ffs while still meeting throughput, provided Fmax and latency hold). Both families share identical accuracy behaviour, so the same data_width/n_iter/guard/rounding ranges apply; the distinguishing dimension is m. This gives a well-covered Pareto front across area, accuracy, and the system latency/throughput bounds within the 100-eval budget.*)
- `pipelined` (33 evals): data_width=14..28, n_iter=12..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* pipelined gives 1 result/cycle, so throughput_msps = Fmax. To clear the 32 Msps throughput constraint and the 0.44 us p99 batch bound (32 back-to-back results must finish within 0.44 us of the tick, i.e. the datapath must sustain >= 32 results/us), Fmax must be comfortably above 32 MHz, which a fully pipelined CORDIC can hit. This is the only family that can plausibly satisfy both throughput and the tight batch-latency bound. I sweep data_width 14..28 and n_iter 12..22 to map the accuracy-vs-area curve: n_iter 12..14 with modest guards should already clear max_abs_err <= 2^-12 (accuracy_bits >= 12), while higher n_iter/data_width push accuracy_bits up (HV ref 12) at the cost of luts_plus_ffs (HV ref 4000). Keeping n_iter >= 12 avoids the infeasible low-accuracy corner and keeps the search on the trade-off curve. angle_guard -2..4 and frac_guard 0..4 cover the accuracy levers; rounding both ways since it shifts error slightly and costs little.
- `pipelined_m` (27 evals): data_width=14..28, n_iter=12..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* pipelined_m registers every m stages, trading some area (fewer FFs than fully pipelined) for a slightly lower Fmax and higher latency (ceil(N/m)+2). It still produces 1 result/cycle, so throughput_msps = Fmax and it can meet the 32 Msps constraint if Fmax stays above 32 MHz. The m=2..4 range lets the search find the area sweet spot: larger m cuts FFs (helping the min luts_plus_ffs objective) but lowers Fmax and raises latency, which pressures the 0.44 us p99 batch bound. I cap m at 4 so latency stays low enough that 32 back-to-back results still fit in 0.44 us. Same accuracy ranges as pipelined since accuracy is family-independent; this family mainly explores the area/latency trade-off that pipelined cannot (it has no m knob).

**Result (code):** 60 evaluations this round, 60 total; 47 feasible; hypervolume 1.425e+04 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established and covers the objective space effectively. The minimum area design (pipelined_m, 1351 LUTs+FFs) meets all constraints with 13.3 bits of accuracy (max_abs_err 0.000102 < 0.000244) and high throughput (93.6 MSPS > 32 MSPS). The front extends to high accuracy (20.6 bits) for those needing more precision. The selection rule (min luts_plus_ffs) clearly points to the 1351 design. Since this is the final round and the front spans the relevant trade-off space (area 1351-4226, accuracy 13.3-20.6 bits) with no obvious gaps or unexplored promising regions, stopping is appropriate.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.425e+04 (gain this round: n/a (first round)).
Feasible designs: 47 of 60 evaluations (46 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 22% violate; best seen 6.36e-07 (2^-20.58)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.166

Pareto front (feasible, 11 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1351, accuracy_bits=13.3, luts=1055, ffs=297, throughput_msps=93.6, max_abs_err=0.000102 (2^-13.25), power_index=1.63
- pipelined_m [data_width=19 n_iter=15 angle_guard=0 frac_guard=2 rounding=round m=3] luts_plus_ffs=1413, accuracy_bits=13.4, luts=1034, ffs=379, throughput_msps=119, max_abs_err=9.42e-05 (2^-13.37), power_index=1.7
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=1433, accuracy_bits=13.7, luts=1048, ffs=384, throughput_msps=119, max_abs_err=7.76e-05 (2^-13.65), power_index=1.72
- pipelined_m [data_width=22 n_iter=15 angle_guard=0 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1478, accuracy_bits=13.9, luts=1126, ffs=351, throughput_msps=89.6, max_abs_err=6.44e-05 (2^-13.92), power_index=1.78
- pipelined_m [data_width=20 n_iter=16 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1479, accuracy_bits=14.3, luts=1154, ffs=325, throughput_msps=93.6, max_abs_err=4.88e-05 (2^-14.32), power_index=1.78
- pipelined_m [data_width=20 n_iter=19 angle_guard=0 frac_guard=3 rounding=round m=4] luts_plus_ffs=1818, accuracy_bits=15.1, luts=1413, ffs=405, throughput_msps=89.6, max_abs_err=2.93e-05 (2^-15.06), power_index=2.19
- pipelined_m [data_width=20 n_iter=19 angle_guard=1 frac_guard=4 rounding=round m=2] luts_plus_ffs=2271, accuracy_bits=16.1, luts=1470, ffs=801, throughput_msps=158, max_abs_err=1.42e-05 (2^-16.11), power_index=2.73
- pipelined_m [data_width=24 n_iter=21 angle_guard=1 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=2446, accuracy_bits=19.1, luts=1797, ffs=650, throughput_msps=110, max_abs_err=1.77e-06 (2^-19.11), power_index=2.94
- pipelined [data_width=25 n_iter=21 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=3699, accuracy_bits=19.5, luts=1839, ffs=1860, throughput_msps=249, max_abs_err=1.36e-06 (2^-19.49), power_index=4.45
- pipelined [data_width=28 n_iter=22 angle_guard=-1 frac_guard=3 rounding=trunc] luts_plus_ffs=4226, accuracy_bits=20.6, luts=2107, ffs=2119, throughput_msps=242, max_abs_err=6.36e-07 (2^-20.58), power_index=5.09
Front coverage: luts_plus_ffs 1351..4226 (HV reference 4000); accuracy_bits 13.3..20.6 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- pipelined: 33 evals, 27 feasible; max throughput seen 273 MSPS; best accuracy 20.58 bits; best feasible luts_plus_ffs=2034; feasible ranges: data_width 15..28, n_iter 14..22, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 27 evals, 20 feasible; max throughput seen 164 MSPS; best accuracy 19.11 bits; best feasible luts_plus_ffs=1351; feasible ranges: data_width 16..28, n_iter 15..21, angle_guard 0..4, frac_guard 2..4, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (33 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (9 front designs; box front_anchored)
- `pipelined` (7 evals): data_width=24..28, n_iter=19..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 70 feasible; hypervolume 1.544e+04 (+8.4%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and covers the objective space effectively. The minimum area design (pipelined_m, 1351 LUTs+FFs) meets all constraints with 13.3 bits of accuracy (max_abs_err 0.000102 < 0.000244) and high throughput (93.6 MSPS > 32 MSPS). The front extends to high accuracy (20.6 bits) for those needing more precision. The selection rule (min luts_plus_ffs) clearly points to the 1351 design. Since this is the final round and the front spans the relevant trade-off space (area 1351-4226, accuracy 13.3-20.6 bits) with no obvious gaps or unexplored promising regions, stopping is appropriate.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.544e+04 (gain this round: +8.4%).
Feasible designs: 70 of 100 evaluations (66 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 13% violate; best seen 1.33e-07 (2^-22.84)
- sys_p99_batch_us <= 0.44: 17% violate; best seen 0.166

Pareto front (feasible, 17 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=3 frac_guard=1 rounding=trunc m=3] luts_plus_ffs=1205, accuracy_bits=12.1, luts=855, ffs=350, throughput_msps=119, max_abs_err=0.000231 (2^-12.08), power_index=1.45
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=2 rounding=round m=4] luts_plus_ffs=1351, accuracy_bits=13.3, luts=1055, ffs=297, throughput_msps=93.6, max_abs_err=0.000102 (2^-13.25), power_index=1.63
- pipelined_m [data_width=19 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=1433, accuracy_bits=13.7, luts=1048, ffs=384, throughput_msps=119, max_abs_err=7.76e-05 (2^-13.65), power_index=1.72
- pipelined_m [data_width=22 n_iter=15 angle_guard=0 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1478, accuracy_bits=13.9, luts=1126, ffs=351, throughput_msps=89.6, max_abs_err=6.44e-05 (2^-13.92), power_index=1.78
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=2] luts_plus_ffs=1745, accuracy_bits=14.5, luts=1128, ffs=617, throughput_msps=164, max_abs_err=4.33e-05 (2^-14.50), power_index=2.1
- pipelined_m [data_width=20 n_iter=19 angle_guard=0 frac_guard=3 rounding=round m=4] luts_plus_ffs=1818, accuracy_bits=15.1, luts=1413, ffs=405, throughput_msps=89.6, max_abs_err=2.93e-05 (2^-15.06), power_index=2.19
- pipelined_m [data_width=22 n_iter=18 angle_guard=3 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=1991, accuracy_bits=16.8, luts=1456, ffs=535, throughput_msps=114, max_abs_err=9.04e-06 (2^-16.75), power_index=2.4
- pipelined_m [data_width=24 n_iter=21 angle_guard=1 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=2446, accuracy_bits=19.1, luts=1797, ffs=650, throughput_msps=110, max_abs_err=1.77e-06 (2^-19.11), power_index=2.94
- pipelined [data_width=28 n_iter=22 angle_guard=-1 frac_guard=3 rounding=trunc] luts_plus_ffs=4226, accuracy_bits=20.6, luts=2107, ffs=2119, throughput_msps=242, max_abs_err=6.36e-07 (2^-20.58), power_index=5.09
- pipelined [data_width=25 n_iter=25 angle_guard=4 frac_guard=3 rounding=round] luts_plus_ffs=4670, accuracy_bits=22.1, luts=2359, ffs=2310, throughput_msps=249, max_abs_err=2.16e-07 (2^-22.14), power_index=5.62
Front coverage: luts_plus_ffs 1205..4670 (HV reference 4000); accuracy_bits 12.1..22.1 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- pipelined: 40 evals, 34 feasible; max throughput seen 273 MSPS; best accuracy 22.14 bits; best feasible luts_plus_ffs=2034; feasible ranges: data_width 15..28, n_iter 14..26, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 60 evals, 36 feasible; max throughput seen 164 MSPS; best accuracy 22.84 bits; best feasible luts_plus_ffs=1205; feasible ranges: data_width 16..28, n_iter 13..30, angle_guard -2..4, frac_guard 1..4, m 2..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5690 in, 1578 out
- provider-reported cost: $0.0027
- full prompts and replies: `llm_trace.jsonl`

