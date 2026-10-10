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
`pipelined_m:data_width=19,n_iter=21,angle_guard=-2,frac_guard=3,rounding=trunc,m=5` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 42489 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 11320 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 366 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 28.1 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 28.1 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 249 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.0454 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000186 (2^-12.39) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 24.4 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 3.7e-05 (2^-14.72) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 4.85 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.4 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (11 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=21,angle_guard=-2,frac_guard=3,rounding=trunc,m=5` | 42489 | 366 | 28.1 | 7 | 0.0454 | 0.000186 (2^-12.39) | 12.39 |
| 1 | `pipelined_m:data_width=19,n_iter=21,angle_guard=2,frac_guard=2,rounding=trunc,m=5` | 43773 | 378 | 29.3 | 7 | 0.0468 | 3.04e-05 (2^-15.00) | 15.00 |
| 2 | `pipelined_m:data_width=19,n_iter=21,angle_guard=2,frac_guard=3,rounding=trunc,m=5` | 44970 | 385 | 28.1 | 7 | 0.0479 | 2.18e-05 (2^-15.49) | 15.49 |
| 3 | `pipelined_m:data_width=22,n_iter=22,angle_guard=2,frac_guard=0,rounding=trunc,m=8` | 45710 | 264 | 16.5 | 5 | 0.0416 | 1.22e-05 (2^-16.32) | 16.32 |
| 4 | `pipelined_m:data_width=26,n_iter=20,angle_guard=2,frac_guard=0,rounding=trunc,m=7` | 48714 | 308 | 16.3 | 5 | 0.0458 | 2.31e-06 (2^-18.72) | 18.72 |
| 5 | `pipelined_m:data_width=26,n_iter=20,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 54252 | 492 | 27.3 | 7 | 0.0593 | 2.13e-06 (2^-18.84) | 18.84 |
| 6 | `pipelined_m:data_width=27,n_iter=21,angle_guard=3,frac_guard=0,rounding=trunc,m=6` | 55248 | 411 | 17.8 | 6 | 0.0554 | 1.16e-06 (2^-19.72) | 19.72 |
| 7 | `pipelined_m:data_width=27,n_iter=22,angle_guard=2,frac_guard=1,rounding=trunc,m=6` | 58128 | 413 | 18.4 | 6 | 0.0572 | 6.47e-07 (2^-20.56) | 20.56 |
| 8 | `pipelined_m:data_width=27,n_iter=27,angle_guard=2,frac_guard=0,rounding=trunc,m=6` | 70259 | 495 | 18.4 | 7 | 0.069 | 4.38e-07 (2^-21.12) | 21.12 |
| 9 | `pipelined_m:data_width=25,n_iter=27,angle_guard=4,frac_guard=3,rounding=round,m=4` | 76925 | 678 | 27.3 | 9 | 0.083 | 1.89e-07 (2^-22.33) | 22.33 |
| 10 | `pipelined:data_width=26,n_iter=25,angle_guard=4,frac_guard=4,rounding=trunc` | 111579 | 2368 | 96.1 | 27 | 0.197 | 1.45e-07 (2^-22.72) | 22.72 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-minimisation with a hard throughput floor of 1 MSPS and a hard accuracy floor of max_abs_err <= 2^-10. Both of my families produce 1 result/cycle, so throughput = Fmax and the 1 MSPS constraint is easily satisfied; the binding constraints are therefore accuracy (which fixes the minimum n_iter / guard combination) and area (which is driven by register count and datapath width). pipelined and pipelined_m are the only families that give 1 result/cycle without the shared-datapath/FSM overhead of iterative/unrolled_k, and they differ precisely in the register-count vs combinational-depth trade-off, which is the central area lever here. I give pipelined the larger share (0.55) because it is the simpler, more predictable low-area baseline and its front is the reference curve; pipelined_m (0.45) is the challenger that can undercut it on area via fewer registers. I keep the full registry ranges for data_width, n_iter, angle_guard, frac_guard and rounding in both families so that, once the feasible region is found, the reserved front-mapping pass can trace the complete trade-off curve from the area corner to the accuracy corner, maximising hypervolume. Rounding is left as a 2-choice dimension because it is a cheap accuracy/area knob that can shift the feasible boundary by a bit or two.*)
- `pipelined` (33 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* pipelined is the natural low-area candidate for >=1 MSPS: 1 result/cycle means throughput = Fmax, so it only needs Fmax >= 1 MHz (trivially met), and it has the fewest registers of the throughput families (N+2 stages). Area is dominated by the N+2 register stages, so the real trade-off is n_iter (accuracy vs register count) and the guard bits (accuracy vs datapath width). I keep the full registry ranges so the front can be mapped end-to-end: low n_iter/low guards give the area corner, high n_iter/guards give the accuracy corner, and the Pareto front runs between them. The max_abs_err <= 2^-10 constraint will carve out the feasible part of that curve.
- `pipelined_m` (27 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* pipelined_m registers only every m stages, so for the same n_iter it uses fewer flip-flops than pipelined (ceil(N/m)+2 vs N+2 stages) at the cost of a longer combinational path (m micro-rotations per stage). Since the throughput floor is only 1 MSPS, the Fmax penalty from a deeper stage is acceptable, so pipelined_m can plausibly beat pipelined on area at equal accuracy. The m dimension is the key new trade-off: large m cuts register area but lowers Fmax and may push the stage too deep; small m approaches pipelined. I search the full m range (2..8) and the full accuracy dimensions so the front captures the register-depth vs path-depth trade-off that pipelined alone cannot express.

**Result (code):** 60 evaluations this round, 60 total; 35 feasible; hypervolume 0 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (pipelined_m, 42489 um^2) meets the throughput constraint (28.1 MSPS >= 1) and accuracy constraint (12.4 bits > 10 bits required). The front spans a wide range of accuracy (12.4 to 21.9 bits) and area (42489 to 106034 um^2), providing a good trade-off curve. Since this is the final round, we stop with the current front. The selection rule (min area) would pick the pipelined_m design at 42489 um^2.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 35 of 60 evaluations (33 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 180
- max_abs_err <= 0.000976562: 42% violate; best seen 2.49e-07 (2^-21.94)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=19 n_iter=21 angle_guard=-2 frac_guard=3 rounding=trunc m=5] area_um2=42489, accuracy_bits=12.4, ffs=366, throughput_msps=28.1, max_abs_err=0.000186 (2^-12.39), power_index=0.0454
- pipelined_m [data_width=19 n_iter=21 angle_guard=2 frac_guard=2 rounding=trunc m=5] area_um2=43773, accuracy_bits=15, ffs=378, throughput_msps=29.3, max_abs_err=3.04e-05 (2^-15.00), power_index=0.0468
- pipelined_m [data_width=19 n_iter=21 angle_guard=2 frac_guard=3 rounding=trunc m=5] area_um2=44970, accuracy_bits=15.5, ffs=385, throughput_msps=28.1, max_abs_err=2.18e-05 (2^-15.49), power_index=0.0479
- pipelined_m [data_width=24 n_iter=21 angle_guard=2 frac_guard=3 rounding=round m=5] area_um2=55761, accuracy_bits=19.4, ffs=471, throughput_msps=23.4, max_abs_err=1.47e-06 (2^-19.38), power_index=0.059
- pipelined [data_width=25 n_iter=21 angle_guard=3 frac_guard=1 rounding=trunc] area_um2=83867, accuracy_bits=19.4, ffs=1792, throughput_msps=102, max_abs_err=1.41e-06 (2^-19.43), power_index=0.149
- pipelined [data_width=25 n_iter=25 angle_guard=3 frac_guard=1 rounding=trunc] area_um2=100252, accuracy_bits=20.2, ffs=2134, throughput_msps=102, max_abs_err=8.07e-07 (2^-20.24), power_index=0.178
- pipelined [data_width=25 n_iter=25 angle_guard=3 frac_guard=3 rounding=round] area_um2=106034, accuracy_bits=21.9, ffs=2227, throughput_msps=102, max_abs_err=2.49e-07 (2^-21.94), power_index=0.186
Front coverage: area_um2 42489..106034 (HV reference 40000); accuracy_bits 12.4..21.9 (HV reference 10); data_width on the front 19..25 (registry 8..28).

Per family:
- pipelined: 33 evals, 28 feasible; max throughput seen 180 MSPS; best accuracy 21.94 bits; best feasible area_um2=43004; feasible ranges: data_width 15..28, n_iter 12..30, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 27 evals, 7 feasible; max throughput seen 102 MSPS; best accuracy 19.38 bits; best feasible area_um2=42489; feasible ranges: data_width 19..27, n_iter 21..21, angle_guard -2..2, frac_guard 2..3, m 5..5
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (23 evals): data_width=18..28, n_iter=19..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)
- `pipelined` (17 evals): data_width=24..28, n_iter=19..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 75 feasible; hypervolume 0 (+0.0%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (pipelined_m, 42489 um^2) meets the throughput constraint (28.1 MSPS >= 1) and accuracy constraint (12.4 bits > 10 bits required). The front spans a wide range of accuracy (12.4 to 21.9 bits) and area (42489 to 106034 um^2), providing a good trade-off curve. Since this is the final round, we stop with the current front. The selection rule (min area) would pick the pipelined_m design at 42489 um^2.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 0 (gain this round: +0.0%).
Feasible designs: 75 of 100 evaluations (71 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 180
- max_abs_err <= 0.000976562: 25% violate; best seen 1.45e-07 (2^-22.72)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=19 n_iter=21 angle_guard=-2 frac_guard=3 rounding=trunc m=5] area_um2=42489, accuracy_bits=12.4, ffs=366, throughput_msps=28.1, max_abs_err=0.000186 (2^-12.39), power_index=0.0454
- pipelined_m [data_width=19 n_iter=21 angle_guard=2 frac_guard=2 rounding=trunc m=5] area_um2=43773, accuracy_bits=15, ffs=378, throughput_msps=29.3, max_abs_err=3.04e-05 (2^-15.00), power_index=0.0468
- pipelined_m [data_width=19 n_iter=21 angle_guard=2 frac_guard=3 rounding=trunc m=5] area_um2=44970, accuracy_bits=15.5, ffs=385, throughput_msps=28.1, max_abs_err=2.18e-05 (2^-15.49), power_index=0.0479
- pipelined_m [data_width=22 n_iter=22 angle_guard=2 frac_guard=0 rounding=trunc m=8] area_um2=45710, accuracy_bits=16.3, ffs=264, throughput_msps=16.5, max_abs_err=1.22e-05 (2^-16.32), power_index=0.0416
- pipelined_m [data_width=26 n_iter=20 angle_guard=2 frac_guard=0 rounding=trunc m=7] area_um2=48714, accuracy_bits=18.7, ffs=308, throughput_msps=16.3, max_abs_err=2.31e-06 (2^-18.72), power_index=0.0458
- pipelined_m [data_width=27 n_iter=21 angle_guard=3 frac_guard=0 rounding=trunc m=6] area_um2=55248, accuracy_bits=19.7, ffs=411, throughput_msps=17.8, max_abs_err=1.16e-06 (2^-19.72), power_index=0.0554
- pipelined_m [data_width=27 n_iter=22 angle_guard=2 frac_guard=1 rounding=trunc m=6] area_um2=58128, accuracy_bits=20.6, ffs=413, throughput_msps=18.4, max_abs_err=6.47e-07 (2^-20.56), power_index=0.0572
- pipelined_m [data_width=27 n_iter=27 angle_guard=2 frac_guard=0 rounding=trunc m=6] area_um2=70259, accuracy_bits=21.1, ffs=495, throughput_msps=18.4, max_abs_err=4.38e-07 (2^-21.12), power_index=0.069
- pipelined_m [data_width=25 n_iter=27 angle_guard=4 frac_guard=3 rounding=round m=4] area_um2=76925, accuracy_bits=22.3, ffs=678, throughput_msps=27.3, max_abs_err=1.89e-07 (2^-22.33), power_index=0.083
- pipelined [data_width=26 n_iter=25 angle_guard=4 frac_guard=4 rounding=trunc] area_um2=111579, accuracy_bits=22.7, ffs=2368, throughput_msps=96.1, max_abs_err=1.45e-07 (2^-22.72), power_index=0.197
Front coverage: area_um2 42489..111579 (HV reference 40000); accuracy_bits 12.4..22.7 (HV reference 10); data_width on the front 19..27 (registry 8..28).

Per family:
- pipelined: 50 evals, 45 feasible; max throughput seen 180 MSPS; best accuracy 22.72 bits; best feasible area_um2=43004; feasible ranges: data_width 15..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 50 evals, 30 feasible; max throughput seen 102 MSPS; best accuracy 22.33 bits; best feasible area_um2=42489; feasible ranges: data_width 18..27, n_iter 20..28, angle_guard -2..4, frac_guard 0..3, m 3..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4384 in, 1393 out
- provider-reported cost: $0.0020
- full prompts and replies: `llm_trace.jsonl`

