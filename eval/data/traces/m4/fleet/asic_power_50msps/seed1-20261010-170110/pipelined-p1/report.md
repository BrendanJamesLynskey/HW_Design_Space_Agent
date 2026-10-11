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
`pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=3` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 28525 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 7599 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 328 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 135 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.75 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000148 (2^-12.72) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 4.86 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 4.29e-05 (2^-14.51) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.4 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.7 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (12 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=3` | 28525 | 328 | 51.9 | 7 | 1.75 | 0.000148 (2^-12.72) | 12.72 |
| 1 | `pipelined_m:data_width=16,n_iter=18,angle_guard=2,frac_guard=2,rounding=round,m=3` | 35653 | 389 | 54.3 | 8 | 2.13 | 0.000138 (2^-12.83) | 12.83 |
| 2 | `pipelined_m:data_width=17,n_iter=18,angle_guard=2,frac_guard=2,rounding=round,m=3` | 37444 | 409 | 51.9 | 8 | 2.24 | 7.61e-05 (2^-13.68) | 13.68 |
| 3 | `pipelined:data_width=18,n_iter=16,angle_guard=1,frac_guard=2,rounding=round` | 48878 | 1032 | 132.4 | 18 | 4.31 | 7.47e-05 (2^-13.71) | 13.71 |
| 4 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 49611 | 1048 | 132.4 | 18 | 4.37 | 5.46e-05 (2^-14.16) | 14.16 |
| 5 | `pipelined:data_width=20,n_iter=20,angle_guard=4,frac_guard=4,rounding=trunc` | 72132 | 1538 | 115.0 | 22 | 6.4 | 7.11e-06 (2^-17.10) | 17.10 |
| 6 | `pipelined:data_width=20,n_iter=22,angle_guard=4,frac_guard=4,rounding=trunc` | 79567 | 1693 | 115.0 | 24 | 7.05 | 6.34e-06 (2^-17.27) | 17.27 |
| 7 | `pipelined:data_width=27,n_iter=20,angle_guard=0,frac_guard=2,rounding=trunc` | 84293 | 1801 | 98.8 | 22 | 7.49 | 2.06e-06 (2^-18.89) | 18.89 |
| 8 | `pipelined:data_width=22,n_iter=22,angle_guard=4,frac_guard=4,rounding=trunc` | 85667 | 1823 | 107.9 | 24 | 7.59 | 1.93e-06 (2^-18.99) | 18.99 |
| 9 | `pipelined:data_width=27,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc` | 89067 | 1903 | 104.7 | 24 | 7.91 | 7.54e-07 (2^-20.34) | 20.34 |
| 10 | `pipelined:data_width=28,n_iter=22,angle_guard=0,frac_guard=3,rounding=round` | 99431 | 2088 | 93.5 | 24 | 8.73 | 5.43e-07 (2^-20.81) | 20.81 |
| 11 | `pipelined:data_width=27,n_iter=30,angle_guard=2,frac_guard=0,rounding=trunc` | 125009 | 2654 | 98.8 | 32 | 11.1 | 4.7e-07 (2^-21.02) | 21.02 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *No prior results, so I seed the two throughput-capable families. The 50 MSPS constraint forces 1 result/cycle, so only pipelined and pipelined_m qualify; iterative/unrolled_k are excluded. I focus data_width 14-18 and n_iter 12-18 because the 2^-12 error bound is met with modest precision plus rounding, and I keep angle/frac guards small to control area/power. pipelined_m is given a smaller share to probe the Fmax/power benefit of multi-stage registers, which is the key lever for the power objective.*)
- `pipelined` (36 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* Full pipeline gives 1 result/cycle so Fmax alone must reach 50 MHz; moderate N (12-18) keeps critical path short while meeting 2^-12 error, and rounding is the cheapest accuracy lever.
- `pipelined_m` (24 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* Registering every m stages shortens the combinational path per cycle, raising Fmax and lowering power_index; m=2-4 balances the 1 result/cycle throughput against the area/power of extra registers.

**Result (code):** 60 evaluations this round, 60 total; 30 feasible; hypervolume 80.89 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 5 distinct designs covering the trade-off space effectively. The minimum power_index achieved is 1.75 (pipelined_m, data_width=17, n_iter=15, m=3) with accuracy_bits=12.7, which satisfies the constraint max_abs_err <= 2^-12 (0.000244141) as 2^-12.72 < 2^-12. The throughput constraint (>= 50 MSPS) is met by all front designs (51.9 to 132 MSPS). The front spans power_index 1.75..4.37 and accuracy_bits 12.7..14.2, providing a good coverage of the objective space relative to the reference point (40, 12). Since this is the final round and the front already contains a clear winner for the selection rule (min power_index) with robust constraint satisfaction, further exploration would not significantly improve the hypervolume or the final design choice.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 80.89 (gain this round: n/a (first round)).
Feasible designs: 30 of 60 evaluations (21 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 15% violate; best seen 163
- max_abs_err <= 0.000244141: 47% violate; best seen 5.46e-05 (2^-14.16)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=3] power_index=1.75, accuracy_bits=12.7, area_um2=28525, ffs=328, throughput_msps=51.9, max_abs_err=0.000148 (2^-12.72)
- pipelined_m [data_width=16 n_iter=18 angle_guard=2 frac_guard=2 rounding=round m=3] power_index=2.13, accuracy_bits=12.8, area_um2=35653, ffs=389, throughput_msps=54.3, max_abs_err=0.000138 (2^-12.83)
- pipelined_m [data_width=17 n_iter=18 angle_guard=2 frac_guard=2 rounding=round m=3] power_index=2.24, accuracy_bits=13.7, area_um2=37444, ffs=409, throughput_msps=51.9, max_abs_err=7.61e-05 (2^-13.68)
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] power_index=4.31, accuracy_bits=13.7, area_um2=48878, ffs=1032, throughput_msps=132, max_abs_err=7.47e-05 (2^-13.71)
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] power_index=4.37, accuracy_bits=14.2, area_um2=49611, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16)
Front coverage: power_index 1.75..4.37 (HV reference 40); accuracy_bits 12.7..14.2 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 36 evals, 25 feasible; max throughput seen 163 MSPS; best accuracy 14.16 bits; best feasible power_index=3.49; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 24 evals, 5 feasible; max throughput seen 91.1 MSPS; best accuracy 13.68 bits; best feasible power_index=1.75; feasible ranges: data_width 16..17, n_iter 15..18, angle_guard 0..2, frac_guard 0..2, m 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (24 evals): data_width=15..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (3 front designs; box front_anchored)
- `pipelined` (16 evals): data_width=17..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 46 feasible; hypervolume 305.3 (+277.4%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 5 distinct designs covering the trade-off space effectively. The minimum power_index achieved is 1.75 (pipelined_m, data_width=17, n_iter=15, m=3) with accuracy_bits=12.7, which satisfies the constraint max_abs_err <= 2^-12 (0.000244141) as 2^-12.72 < 2^-12. The throughput constraint (>= 50 MSPS) is met by all front designs (51.9 to 132 MSPS). The front spans power_index 1.75..4.37 and accuracy_bits 12.7..14.2, providing a good coverage of the objective space relative to the reference point (40, 12). Since this is the final round and the front already contains a clear winner for the selection rule (min power_index) with robust constraint satisfaction, further exploration would not significantly improve the hypervolume or the final design choice.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 305.3 (gain this round: +277.4%).
Feasible designs: 46 of 100 evaluations (36 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 33% violate; best seen 163
- max_abs_err <= 0.000244141: 30% violate; best seen 3.71e-07 (2^-21.36)

Pareto front (feasible, 12 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=3] power_index=1.75, accuracy_bits=12.7, area_um2=28525, ffs=328, throughput_msps=51.9, max_abs_err=0.000148 (2^-12.72)
- pipelined_m [data_width=16 n_iter=18 angle_guard=2 frac_guard=2 rounding=round m=3] power_index=2.13, accuracy_bits=12.8, area_um2=35653, ffs=389, throughput_msps=54.3, max_abs_err=0.000138 (2^-12.83)
- pipelined_m [data_width=17 n_iter=18 angle_guard=2 frac_guard=2 rounding=round m=3] power_index=2.24, accuracy_bits=13.7, area_um2=37444, ffs=409, throughput_msps=51.9, max_abs_err=7.61e-05 (2^-13.68)
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] power_index=4.37, accuracy_bits=14.2, area_um2=49611, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16)
- pipelined [data_width=20 n_iter=20 angle_guard=4 frac_guard=4 rounding=trunc] power_index=6.4, accuracy_bits=17.1, area_um2=72132, ffs=1538, throughput_msps=115, max_abs_err=7.11e-06 (2^-17.10)
- pipelined [data_width=20 n_iter=22 angle_guard=4 frac_guard=4 rounding=trunc] power_index=7.05, accuracy_bits=17.3, area_um2=79567, ffs=1693, throughput_msps=115, max_abs_err=6.34e-06 (2^-17.27)
- pipelined [data_width=27 n_iter=20 angle_guard=0 frac_guard=2 rounding=trunc] power_index=7.49, accuracy_bits=18.9, area_um2=84293, ffs=1801, throughput_msps=98.8, max_abs_err=2.06e-06 (2^-18.89)
- pipelined [data_width=27 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc] power_index=7.91, accuracy_bits=20.3, area_um2=89067, ffs=1903, throughput_msps=105, max_abs_err=7.54e-07 (2^-20.34)
- pipelined [data_width=28 n_iter=22 angle_guard=0 frac_guard=3 rounding=round] power_index=8.73, accuracy_bits=20.8, area_um2=99431, ffs=2088, throughput_msps=93.5, max_abs_err=5.43e-07 (2^-20.81)
- pipelined [data_width=27 n_iter=30 angle_guard=2 frac_guard=0 rounding=trunc] power_index=11.1, accuracy_bits=21, area_um2=125009, ffs=2654, throughput_msps=98.8, max_abs_err=4.7e-07 (2^-21.02)
Front coverage: power_index 1.75..11.1 (HV reference 40); accuracy_bits 12.7..21 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- pipelined: 52 evals, 41 feasible; max throughput seen 163 MSPS; best accuracy 21.02 bits; best feasible power_index=3.49; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 48 evals, 5 feasible; max throughput seen 91.1 MSPS; best accuracy 21.36 bits; best feasible power_index=1.75; feasible ranges: data_width 16..17, n_iter 15..18, angle_guard 0..2, frac_guard 0..2, m 2..3
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4677 in, 1007 out
- provider-reported cost: $0.0026
- full prompts and replies: `llm_trace.jsonl`

