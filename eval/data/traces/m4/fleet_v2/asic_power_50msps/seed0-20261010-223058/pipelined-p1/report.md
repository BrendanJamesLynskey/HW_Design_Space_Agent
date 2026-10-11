# DSE run: asic_power_50msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_power_50msps: A 50 MSPS sin/cos unit in sky130 standard cells for a battery-powered radio: max error <= 2^-12. Minimise the relative power index; accuracy is the trade-off.
  target: asic-sky130hd
  constraint: throughput_msps >= 50
  constraint: max_abs_err <= 0.000244141
  objective: min power_index (HV ref 40)
  objective: max accuracy_bits (HV ref 12)
  select: min power_index
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=17,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=3` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 31342 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 8350 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 387 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 8 | exact: schedule |
| latency_ns | 154 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000139 (2^-12.81) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 4.55 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 3.84e-05 (2^-14.67) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.26 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.8 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=3` | 31342 | 387 | 51.9 | 8 | 2 | 0.000139 (2^-12.81) | 12.81 |
| 1 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=2,rounding=round,m=2` | 35408 | 535 | 75.4 | 10 | 2.53 | 0.000108 (2^-13.18) | 13.18 |
| 2 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=2,rounding=round` | 45777 | 967 | 132.4 | 17 | 4.04 | 9.56e-05 (2^-13.35) | 13.35 |
| 3 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 46462 | 982 | 132.4 | 17 | 4.1 | 8.26e-05 (2^-13.56) | 13.56 |
| 4 | `pipelined_m:data_width=24,n_iter=21,angle_guard=-1,frac_guard=4,rounding=trunc,m=2` | 65088 | 969 | 54.3 | 13 | 4.61 | 3.54e-06 (2^-18.11) | 18.11 |
| 5 | `pipelined_m:data_width=24,n_iter=25,angle_guard=-1,frac_guard=4,rounding=round,m=2` | 78801 | 1140 | 54.3 | 15 | 5.49 | 3.47e-06 (2^-18.14) | 18.14 |
| 6 | `pipelined:data_width=24,n_iter=20,angle_guard=4,frac_guard=2,rounding=trunc` | 79683 | 1703 | 101.6 | 22 | 7.08 | 2.49e-06 (2^-18.61) | 18.61 |
| 7 | `pipelined:data_width=27,n_iter=20,angle_guard=1,frac_guard=4,rounding=round` | 90152 | 1894 | 93.5 | 22 | 7.92 | 1.96e-06 (2^-18.96) | 18.96 |
| 8 | `pipelined:data_width=27,n_iter=20,angle_guard=2,frac_guard=4,rounding=round` | 91074 | 1913 | 93.5 | 22 | 8 | 1.95e-06 (2^-18.97) | 18.97 |
| 9 | `pipelined:data_width=27,n_iter=20,angle_guard=4,frac_guard=4,rounding=round` | 92918 | 1953 | 93.5 | 22 | 8.16 | 1.92e-06 (2^-18.99) | 18.99 |
| 10 | `pipelined:data_width=22,n_iter=26,angle_guard=4,frac_guard=2,rounding=round` | 98191 | 2065 | 107.9 | 28 | 8.63 | 1.83e-06 (2^-19.06) | 19.06 |
| 11 | `pipelined:data_width=23,n_iter=26,angle_guard=4,frac_guard=1,rounding=round` | 99536 | 2094 | 104.7 | 28 | 8.75 | 1.73e-06 (2^-19.14) | 19.14 |
| 12 | `pipelined:data_width=22,n_iter=26,angle_guard=4,frac_guard=4,rounding=round` | 102842 | 2159 | 107.9 | 28 | 9.03 | 1e-06 (2^-19.93) | 19.93 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *No fleet facts yet, so I seed the front. The 50 MSPS throughput constraint forces 1 result/cycle, which only pipelined and pipelined_m provide (iterative/unrolled_k are cut anyway). I focus on W=14-18 and N=12-18 where the accuracy constraint (err <= 2^-12) is satisfiable with margin, and use round for best accuracy. I split budget 60/40 between the two families to map the area/Fmax trade-off: pipelined for the speed/area extreme and pipelined_m (m=2-4) for the intermediate power-optimal points, since the selection rule minimises power_index.*)
- `pipelined` (36 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* Full pipeline gives 1 result/cycle so Fmax alone sets throughput; this is the only family that can plausibly hit 50 MSPS in sky130hd. W=14-18 and N=12-18 cover the accuracy sweet spot (err <= 2^-12) while keeping the critical path short; round is the accuracy-optimal choice.
- `pipelined_m` (24 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* Registering every m stages trades area/FFs against Fmax; with 1 result/cycle it still meets throughput if Fmax is high enough. m=2-4 explores the area-vs-speed trade-off that the power objective rewards, complementing the fully-pipelined front.

**Result (code):** 60 evaluations this round, 60 total; 16 feasible; hypervolume 75.19 (n/a).

**LLM decision:** `stop` — The Pareto front is well-established and feasible. We have identified a clear trade-off curve between power and accuracy. The minimum power design (pipelined_m, power_index=2.0) meets the throughput constraint (51.9 MSPS >= 50) and the accuracy constraint (12.8 bits > 12 bits). Higher accuracy designs (up to 14.04 bits) are also available at the cost of higher power (up to 4.85). The hypervolume is 75.19, indicating good coverage of the objective space. Since this is the final round, and the front covers the relevant range of the objectives (power 2-4.85, accuracy 12.8-14.0) with feasible designs at both ends, stopping is the appropriate action. The selection rule (min power_index) will pick the pipelined_m design with power_index=2.0.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 75.19 (gain this round: n/a (first round)).
Feasible designs: 16 of 60 evaluations (13 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 20% violate; best seen 156
- max_abs_err <= 0.000244141: 60% violate; best seen 5.94e-05 (2^-14.04)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=3] power_index=2, accuracy_bits=12.8, area_um2=31342, ffs=387, throughput_msps=51.9, max_abs_err=0.000139 (2^-12.81)
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=2.53, accuracy_bits=13.2, area_um2=35408, ffs=535, throughput_msps=75.4, max_abs_err=0.000108 (2^-13.18)
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=round] power_index=4.04, accuracy_bits=13.4, area_um2=45777, ffs=967, throughput_msps=132, max_abs_err=9.56e-05 (2^-13.35)
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] power_index=4.1, accuracy_bits=13.6, area_um2=46462, ffs=982, throughput_msps=132, max_abs_err=8.26e-05 (2^-13.56)
- pipelined [data_width=18 n_iter=18 angle_guard=1 frac_guard=1 rounding=round] power_index=4.72, accuracy_bits=13.8, area_um2=53514, ffs=1131, throughput_msps=138, max_abs_err=6.95e-05 (2^-13.81)
- pipelined [data_width=18 n_iter=18 angle_guard=1 frac_guard=2 rounding=round] power_index=4.85, accuracy_bits=14, area_um2=55081, ffs=1162, throughput_msps=132, max_abs_err=5.94e-05 (2^-14.04)
Front coverage: power_index 2..4.85 (HV reference 40); accuracy_bits 12.8..14 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 36 evals, 13 feasible; max throughput seen 156 MSPS; best accuracy 14.04 bits; best feasible power_index=3.73; feasible ranges: data_width 16..18, n_iter 15..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 24 evals, 3 feasible; max throughput seen 86.6 MSPS; best accuracy 13.51 bits; best feasible power_index=2; feasible ranges: data_width 17..17, n_iter 15..16, angle_guard 2..2, frac_guard 0..2, m 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (14 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (2 front designs; box front_anchored)
- `pipelined` (26 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (4 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 42 feasible; hypervolume 277.1 (+268.6%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and feasible. We have identified a clear trade-off curve between power and accuracy. The minimum power design (pipelined_m, power_index=2.0) meets the throughput constraint (51.9 MSPS >= 50) and the accuracy constraint (12.8 bits > 12 bits). Higher accuracy designs (up to 14.04 bits) are also available at the cost of higher power (up to 4.85). The hypervolume is 75.19, indicating good coverage of the objective space. Since this is the final round, and the front covers the relevant range of the objectives (power 2-4.85, accuracy 12.8-14.0) with feasible designs at both ends, stopping is the appropriate action. The selection rule (min power_index) will pick the pipelined_m design with power_index=2.0.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 277.1 (gain this round: +268.6%).
Feasible designs: 42 of 100 evaluations (37 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 22% violate; best seen 156
- max_abs_err <= 0.000244141: 40% violate; best seen 1.45e-07 (2^-22.72)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=3] power_index=2, accuracy_bits=12.8, area_um2=31342, ffs=387, throughput_msps=51.9, max_abs_err=0.000139 (2^-12.81)
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=2.53, accuracy_bits=13.2, area_um2=35408, ffs=535, throughput_msps=75.4, max_abs_err=0.000108 (2^-13.18)
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] power_index=4.1, accuracy_bits=13.6, area_um2=46462, ffs=982, throughput_msps=132, max_abs_err=8.26e-05 (2^-13.56)
- pipelined_m [data_width=24 n_iter=21 angle_guard=-1 frac_guard=4 rounding=trunc m=2] power_index=4.61, accuracy_bits=18.1, area_um2=65088, ffs=969, throughput_msps=54.3, max_abs_err=3.54e-06 (2^-18.11)
- pipelined_m [data_width=24 n_iter=25 angle_guard=-1 frac_guard=4 rounding=round m=2] power_index=5.49, accuracy_bits=18.1, area_um2=78801, ffs=1140, throughput_msps=54.3, max_abs_err=3.47e-06 (2^-18.14)
- pipelined [data_width=27 n_iter=20 angle_guard=1 frac_guard=4 rounding=round] power_index=7.92, accuracy_bits=19, area_um2=90152, ffs=1894, throughput_msps=93.5, max_abs_err=1.96e-06 (2^-18.96)
- pipelined [data_width=27 n_iter=20 angle_guard=2 frac_guard=4 rounding=round] power_index=8, accuracy_bits=19, area_um2=91074, ffs=1913, throughput_msps=93.5, max_abs_err=1.95e-06 (2^-18.97)
- pipelined [data_width=27 n_iter=20 angle_guard=4 frac_guard=4 rounding=round] power_index=8.16, accuracy_bits=19, area_um2=92918, ffs=1953, throughput_msps=93.5, max_abs_err=1.92e-06 (2^-18.99)
- pipelined [data_width=23 n_iter=26 angle_guard=4 frac_guard=1 rounding=round] power_index=8.75, accuracy_bits=19.1, area_um2=99536, ffs=2094, throughput_msps=105, max_abs_err=1.73e-06 (2^-19.14)
- pipelined [data_width=22 n_iter=26 angle_guard=4 frac_guard=4 rounding=round] power_index=9.03, accuracy_bits=19.9, area_um2=102842, ffs=2159, throughput_msps=108, max_abs_err=1e-06 (2^-19.93)
Front coverage: power_index 2..9.03 (HV reference 40); accuracy_bits 12.8..19.9 (HV reference 12); data_width on the front 17..27 (registry 8..28).

Per family:
- pipelined: 62 evals, 36 feasible; max throughput seen 156 MSPS; best accuracy 19.93 bits; best feasible power_index=3.73; feasible ranges: data_width 16..27, n_iter 15..29, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 38 evals, 6 feasible; max throughput seen 86.6 MSPS; best accuracy 22.72 bits; best feasible power_index=2; feasible ranges: data_width 17..24, n_iter 15..25, angle_guard -1..2, frac_guard 0..4, m 2..3
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4748 in, 916 out
- provider-reported cost: $0.0020
- full prompts and replies: `llm_trace.jsonl`

