# DSE run: asic_low_area

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_low_area: Motor-control sin/cos in sky130 standard cells: >= 1 MSPS, max error <= 2^-10. Area is everything: minimise cell area.
  target: asic-sky130hd
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min area_um2 (HV ref 40000)
  objective: max accuracy_bits (HV ref 10)
  select: min area_um2
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=19,n_iter=12,angle_guard=-1,frac_guard=1,rounding=trunc,m=4` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 23159 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 6170 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 227 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 37.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 37.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 132 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.0263 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000526 (2^-10.89) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 68.9 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 0.0002 (2^-12.29) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 26.2 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 10.9 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (17 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=12,angle_guard=-1,frac_guard=1,rounding=trunc,m=4` | 23159 | 227 | 37.9 | 5 | 0.0263 | 0.000526 (2^-10.89) | 10.89 |
| 1 | `pipelined_m:data_width=17,n_iter=13,angle_guard=-1,frac_guard=1,rounding=trunc,m=4` | 23762 | 263 | 41.5 | 6 | 0.0286 | 0.000456 (2^-11.10) | 11.10 |
| 2 | `pipelined_m:data_width=17,n_iter=13,angle_guard=-1,frac_guard=1,rounding=round,m=4` | 24675 | 265 | 41.5 | 6 | 0.0293 | 0.000448 (2^-11.12) | 11.12 |
| 3 | `pipelined_m:data_width=17,n_iter=13,angle_guard=0,frac_guard=1,rounding=trunc,m=3` | 25466 | 326 | 54.3 | 7 | 0.0332 | 0.000395 (2^-11.30) | 11.30 |
| 4 | `pipelined_m:data_width=19,n_iter=13,angle_guard=-1,frac_guard=1,rounding=trunc,m=2` | 30469 | 483 | 72.3 | 9 | 0.0448 | 0.000296 (2^-11.72) | 11.72 |
| 5 | `pipelined_m:data_width=19,n_iter=14,angle_guard=0,frac_guard=2,rounding=trunc,m=3` | 30548 | 368 | 47.7 | 7 | 0.0384 | 0.000158 (2^-12.63) | 12.63 |
| 6 | `pipelined_m:data_width=19,n_iter=18,angle_guard=1,frac_guard=2,rounding=trunc,m=8` | 34928 | 237 | 18.6 | 5 | 0.0338 | 3.99e-05 (2^-14.61) | 14.61 |
| 7 | `pipelined_m:data_width=20,n_iter=16,angle_guard=3,frac_guard=4,rounding=round,m=7` | 36514 | 263 | 18.8 | 5 | 0.0362 | 3.31e-05 (2^-14.88) | 14.88 |
| 8 | `pipelined_m:data_width=25,n_iter=16,angle_guard=2,frac_guard=3,rounding=trunc,m=7` | 41095 | 309 | 16.3 | 5 | 0.0414 | 3.06e-05 (2^-15.00) | 15.00 |
| 9 | `pipelined_m:data_width=19,n_iter=21,angle_guard=1,frac_guard=3,rounding=round,m=6` | 43815 | 313 | 23.6 | 6 | 0.0432 | 2.63e-05 (2^-15.21) | 15.21 |
| 10 | `pipelined_m:data_width=19,n_iter=21,angle_guard=4,frac_guard=2,rounding=round,m=5` | 46028 | 389 | 27.1 | 7 | 0.0488 | 1.5e-05 (2^-16.03) | 16.03 |
| 11 | `pipelined_m:data_width=25,n_iter=21,angle_guard=1,frac_guard=3,rounding=round,m=7` | 53212 | 308 | 16.3 | 5 | 0.0485 | 1.43e-06 (2^-19.42) | 19.42 |
| 12 | `pipelined_m:data_width=28,n_iter=21,angle_guard=-2,frac_guard=2,rounding=round,m=8` | 55846 | 327 | 13.4 | 5 | 0.0511 | 1.4e-06 (2^-19.45) | 19.45 |
| 13 | `pipelined_m:data_width=28,n_iter=21,angle_guard=1,frac_guard=2,rounding=trunc,m=8` | 56101 | 334 | 13.4 | 5 | 0.0516 | 1e-06 (2^-19.93) | 19.93 |
| 14 | `pipelined_m:data_width=28,n_iter=30,angle_guard=0,frac_guard=2,rounding=trunc,m=7` | 81290 | 518 | 15.3 | 7 | 0.0767 | 1.45e-07 (2^-22.72) | 22.72 |
| 15 | `pipelined_m:data_width=28,n_iter=30,angle_guard=0,frac_guard=2,rounding=round,m=7` | 82764 | 520 | 15.3 | 7 | 0.0777 | 1.41e-07 (2^-22.76) | 22.76 |
| 16 | `pipelined_m:data_width=28,n_iter=30,angle_guard=0,frac_guard=3,rounding=trunc,m=7` | 82946 | 526 | 14.9 | 7 | 0.0781 | 1.33e-07 (2^-22.84) | 22.84 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-dominated with a hard throughput floor (>=1 MSPS) and a hard accuracy floor (max_abs_err <= 2^-10). Both pipelined and pipelined_m produce one result per cycle, so throughput equals Fmax; the 1 MSPS floor is non-binding (Fmax will be far above 1 MHz), leaving area and accuracy as the real trade-off. Accuracy is set by n_iter plus the guard bits and the output LSB (2^-(W-2)), independent of the pipeline structure, so I use identical data_width/n_iter/angle_guard/frac_guard/rounding ranges across both families to make their fronts comparable. The key differentiator is register count: pipelined_m with m>1 uses fewer FFs than pipelined at equal N, so it should host the minimum-area designs, while pipelined (m=1) gives the lowest latency and a clean reference point on the front. I keep n_iter in 10..14 (enough to clear 2^-10 without over-designing) and data_width in 12..22 to map the area-vs-accuracy curve. I split the budget 55/45 toward pipelined to first confirm the accuracy-feasible region and establish the reference front, with pipelined_m carrying the area-minimization search. If the first round shows the accuracy constraint is tight or the area floor is high, I will tighten n_iter/data_width and push more budget into pipelined_m with larger m in the next round.*)
- `pipelined` (33 evals): data_width=12..22, n_iter=10..14, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Fully pipelined gives 1 result/cycle, so throughput = Fmax. To hit >=1 MSPS we need Fmax >= 1 MHz, which is trivially met, so the binding constraint is max_abs_err <= 2^-10. Accuracy is driven by n_iter and the guard bits; data_width sets the output LSB (2^-(W-2)) so W must be large enough that the truncation floor plus CORDIC residual stays under 2^-10. I focus n_iter in 10..14 (enough to push residual below 2^-10 while keeping area low) and keep data_width in 12..22 to capture the area/accuracy trade-off. angle_guard -2..2 and frac_guard 0..2 cover the accuracy levers without wasting area on over-guarding. Both rounding modes included since rounding can shave error at negligible area cost.
- `pipelined_m` (27 evals): data_width=12..22, n_iter=10..14, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m registers every m stages, so it uses fewer flip-flops than fully pipelined at the same N, directly reducing area (the primary objective) while still delivering 1 result/cycle (throughput = Fmax, constraint easily met). m in 2..4 trades latency (ceil(N/m)+2) against register count; since latency is not a spec constraint, larger m is favored for area. Same data_width/n_iter/guard/rounding ranges as pipelined so the two fronts are directly comparable and the merged Pareto front spans the register-density trade-off. This family is where the minimum-area corner is most likely to live.

**Result (code):** 60 evaluations this round, 60 total; 40 feasible; hypervolume 3.391e+04 (n/a).

**LLM decision:** `stop` — The spec constraints are met: 100% of feasible designs achieve throughput >= 1 MSPS (best 171) and the best accuracy is 13 bits (max_abs_err 0.000125 <= 0.000976562). The Pareto front is well-populated with 10 designs spanning area 23159..48707 um^2 and accuracy 10.9..13 bits, with the minimum-area design at 23159 um^2 (pipelined_m, data_width=19, n_iter=12, m=4) comfortably below the HV reference of 40000. Since this is the final round and the front adequately covers the trade-off space, stopping is appropriate.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 3.391e+04 (gain this round: n/a (first round)).
Feasible designs: 40 of 60 evaluations (35 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 33% violate; best seen 0.000125 (2^-12.97)

Pareto front (feasible, 10 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=19 n_iter=12 angle_guard=-1 frac_guard=1 rounding=trunc m=4] area_um2=23159, accuracy_bits=10.9, ffs=227, throughput_msps=37.9, max_abs_err=0.000526 (2^-10.89), power_index=0.0263
- pipelined_m [data_width=17 n_iter=13 angle_guard=-1 frac_guard=1 rounding=trunc m=4] area_um2=23762, accuracy_bits=11.1, ffs=263, throughput_msps=41.5, max_abs_err=0.000456 (2^-11.10), power_index=0.0286
- pipelined_m [data_width=17 n_iter=13 angle_guard=-1 frac_guard=1 rounding=round m=4] area_um2=24675, accuracy_bits=11.1, ffs=265, throughput_msps=41.5, max_abs_err=0.000448 (2^-11.12), power_index=0.0293
- pipelined_m [data_width=17 n_iter=13 angle_guard=0 frac_guard=1 rounding=trunc m=3] area_um2=25466, accuracy_bits=11.3, ffs=326, throughput_msps=54.3, max_abs_err=0.000395 (2^-11.30), power_index=0.0332
- pipelined_m [data_width=19 n_iter=13 angle_guard=-1 frac_guard=1 rounding=trunc m=2] area_um2=30469, accuracy_bits=11.7, ffs=483, throughput_msps=72.3, max_abs_err=0.000296 (2^-11.72), power_index=0.0448
- pipelined_m [data_width=19 n_iter=14 angle_guard=0 frac_guard=2 rounding=trunc m=3] area_um2=30548, accuracy_bits=12.6, ffs=368, throughput_msps=47.7, max_abs_err=0.000158 (2^-12.63), power_index=0.0384
- pipelined [data_width=20 n_iter=14 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=43800, accuracy_bits=12.8, ffs=950, throughput_msps=123, max_abs_err=0.000141 (2^-12.79), power_index=0.0786
- pipelined [data_width=22 n_iter=14 angle_guard=-2 frac_guard=2 rounding=trunc] area_um2=47452, accuracy_bits=12.9, ffs=1024, throughput_msps=115, max_abs_err=0.000132 (2^-12.89), power_index=0.0849
- pipelined [data_width=22 n_iter=14 angle_guard=-1 frac_guard=2 rounding=trunc] area_um2=48089, accuracy_bits=12.9, ffs=1038, throughput_msps=115, max_abs_err=0.000129 (2^-12.92), power_index=0.086
- pipelined [data_width=22 n_iter=14 angle_guard=0 frac_guard=1 rounding=round] area_um2=48707, accuracy_bits=13, ffs=1030, throughput_msps=119, max_abs_err=0.000125 (2^-12.97), power_index=0.086
Front coverage: area_um2 23159..48707 (HV reference 40000); accuracy_bits 10.9..13 (HV reference 10); data_width on the front 17..22 (registry 8..28).

Per family:
- pipelined: 33 evals, 24 feasible; max throughput seen 171 MSPS; best accuracy 12.97 bits; best feasible area_um2=32882; feasible ranges: data_width 15..22, n_iter 13..14, angle_guard -2..2, frac_guard 0..2
- pipelined_m: 27 evals, 16 feasible; max throughput seen 91.1 MSPS; best accuracy 12.63 bits; best feasible area_um2=23159; feasible ranges: data_width 16..22, n_iter 12..14, angle_guard -1..0, frac_guard 1..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (24 evals): data_width=16..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (6 front designs; box front_anchored)
- `pipelined` (16 evals): data_width=19..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (4 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 77 feasible; hypervolume 4.494e+04 (+32.5%).

**No LLM call** (code's front-mapping round): The spec constraints are met: 100% of feasible designs achieve throughput >= 1 MSPS (best 171) and the best accuracy is 13 bits (max_abs_err 0.000125 <= 0.000976562). The Pareto front is well-populated with 10 designs spanning area 23159..48707 um^2 and accuracy 10.9..13 bits, with the minimum-area design at 23159 um^2 (pipelined_m, data_width=19, n_iter=12, m=4) comfortably below the HV reference of 40000. Since this is the final round and the front adequately covers the trade-off space, stopping is appropriate.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 4.494e+04 (gain this round: +32.5%).
Feasible designs: 77 of 100 evaluations (70 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 23% violate; best seen 1.33e-07 (2^-22.84)

Pareto front (feasible, 17 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=19 n_iter=12 angle_guard=-1 frac_guard=1 rounding=trunc m=4] area_um2=23159, accuracy_bits=10.9, ffs=227, throughput_msps=37.9, max_abs_err=0.000526 (2^-10.89), power_index=0.0263
- pipelined_m [data_width=17 n_iter=13 angle_guard=-1 frac_guard=1 rounding=round m=4] area_um2=24675, accuracy_bits=11.1, ffs=265, throughput_msps=41.5, max_abs_err=0.000448 (2^-11.12), power_index=0.0293
- pipelined_m [data_width=19 n_iter=13 angle_guard=-1 frac_guard=1 rounding=trunc m=2] area_um2=30469, accuracy_bits=11.7, ffs=483, throughput_msps=72.3, max_abs_err=0.000296 (2^-11.72), power_index=0.0448
- pipelined_m [data_width=19 n_iter=14 angle_guard=0 frac_guard=2 rounding=trunc m=3] area_um2=30548, accuracy_bits=12.6, ffs=368, throughput_msps=47.7, max_abs_err=0.000158 (2^-12.63), power_index=0.0384
- pipelined_m [data_width=20 n_iter=16 angle_guard=3 frac_guard=4 rounding=round m=7] area_um2=36514, accuracy_bits=14.9, ffs=263, throughput_msps=18.8, max_abs_err=3.31e-05 (2^-14.88), power_index=0.0362
- pipelined_m [data_width=19 n_iter=21 angle_guard=1 frac_guard=3 rounding=round m=6] area_um2=43815, accuracy_bits=15.2, ffs=313, throughput_msps=23.6, max_abs_err=2.63e-05 (2^-15.21), power_index=0.0432
- pipelined_m [data_width=25 n_iter=21 angle_guard=1 frac_guard=3 rounding=round m=7] area_um2=53212, accuracy_bits=19.4, ffs=308, throughput_msps=16.3, max_abs_err=1.43e-06 (2^-19.42), power_index=0.0485
- pipelined_m [data_width=28 n_iter=21 angle_guard=-2 frac_guard=2 rounding=round m=8] area_um2=55846, accuracy_bits=19.5, ffs=327, throughput_msps=13.4, max_abs_err=1.4e-06 (2^-19.45), power_index=0.0511
- pipelined_m [data_width=28 n_iter=30 angle_guard=0 frac_guard=2 rounding=trunc m=7] area_um2=81290, accuracy_bits=22.7, ffs=518, throughput_msps=15.3, max_abs_err=1.45e-07 (2^-22.72), power_index=0.0767
- pipelined_m [data_width=28 n_iter=30 angle_guard=0 frac_guard=3 rounding=trunc m=7] area_um2=82946, accuracy_bits=22.8, ffs=526, throughput_msps=14.9, max_abs_err=1.33e-07 (2^-22.84), power_index=0.0781
Front coverage: area_um2 23159..82946 (HV reference 40000); accuracy_bits 10.9..22.8 (HV reference 10); data_width on the front 17..28 (registry 8..28).

Per family:
- pipelined: 49 evals, 40 feasible; max throughput seen 171 MSPS; best accuracy 19.01 bits; best feasible area_um2=32882; feasible ranges: data_width 15..25, n_iter 13..24, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 51 evals, 37 feasible; max throughput seen 91.1 MSPS; best accuracy 22.84 bits; best feasible area_um2=23159; feasible ranges: data_width 16..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5397 in, 1341 out
- provider-reported cost: $0.0022
- full prompts and replies: `llm_trace.jsonl`

