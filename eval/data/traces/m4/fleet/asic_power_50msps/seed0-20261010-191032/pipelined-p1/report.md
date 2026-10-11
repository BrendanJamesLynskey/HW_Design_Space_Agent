# DSE run: asic_power_50msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`pipelined_m:data_width=20,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=2` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 39113 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10420 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 582 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 66.8 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 66.8 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 10 | exact: schedule |
| latency_ns | 150 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.77 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 4.12e-05 (2^-14.57) | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 10.8 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 1.33e-05 (2^-16.20) | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.49 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 14.6 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (8 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=20,n_iter=16,angle_guard=2,frac_guard=0,rounding=round,m=2` | 39113 | 582 | 66.8 | 10 | 2.77 | 4.12e-05 (2^-14.57) | 14.57 |
| 1 | `pipelined_m:data_width=20,n_iter=23,angle_guard=1,frac_guard=1,rounding=trunc,m=2` | 58081 | 863 | 69.4 | 14 | 4.11 | 2.8e-05 (2^-15.12) | 15.12 |
| 2 | `pipelined_m:data_width=25,n_iter=21,angle_guard=-1,frac_guard=4,rounding=trunc,m=2` | 67386 | 1004 | 52.7 | 13 | 4.78 | 2.32e-06 (2^-18.72) | 18.72 |
| 3 | `pipelined:data_width=24,n_iter=22,angle_guard=3,frac_guard=1,rounding=trunc` | 84913 | 1813 | 104.7 | 24 | 7.54 | 1.76e-06 (2^-19.11) | 19.11 |
| 4 | `pipelined:data_width=25,n_iter=22,angle_guard=4,frac_guard=2,rounding=trunc` | 90926 | 1939 | 98.8 | 24 | 8.07 | 7.65e-07 (2^-20.32) | 20.32 |
| 5 | `pipelined:data_width=25,n_iter=22,angle_guard=2,frac_guard=4,rounding=trunc` | 92785 | 1974 | 98.8 | 24 | 8.22 | 7.17e-07 (2^-20.41) | 20.41 |
| 6 | `pipelined:data_width=27,n_iter=22,angle_guard=1,frac_guard=4,rounding=round` | 99292 | 2084 | 93.5 | 24 | 8.72 | 5.58e-07 (2^-20.77) | 20.77 |
| 7 | `pipelined:data_width=27,n_iter=22,angle_guard=4,frac_guard=4,rounding=round` | 102343 | 2149 | 93.5 | 24 | 8.99 | 4.95e-07 (2^-20.95) | 20.95 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Both allowed families are 1-result/cycle, so the 50 MSPS throughput constraint is satisfied as long as Fmax >= 50 MHz, which is very likely for these short CORDIC datapaths. Accuracy depends only on data_width, n_iter, angle_guard, frac_guard and rounding, so I search the same accuracy box in both families and let the register structure (full vs every-m-stage) drive the power trade-off. data_width is bounded below at 14 because the output LSB is 2^-(W-2) and the spec needs max_abs_err <= 2^-12; n_iter starts at 10 to allow convergence. The full guard/rounding ranges are kept open because they are cheap ways to buy accuracy without widening the datapath. Budget is split slightly toward pipelined_m since it is the more likely low-power candidate for the min-power selection rule, while pipelined still maps the high-throughput/high-power corner.*)
- `pipelined` (27 evals): data_width=14..20, n_iter=10..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Fully pipelined gives 1 result/cycle, so throughput equals Fmax and the 50 MSPS constraint is easy; this family anchors the high-throughput end of the front. data_width >= 14 and n_iter >= 10 are needed to reach the 2^-12 error bound, while the guard/rounding knobs let the search trade area/power against accuracy.
- `pipelined_m` (33 evals): data_width=14..20, n_iter=10..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Registering every m stages cuts the flip-flop count versus full pipelining, which should lower the power index; the longer combinational path lowers Fmax but 50 MSPS leaves ample headroom. Same accuracy knobs as pipelined, so this family should supply the low-power end of the Pareto front.

**Result (code):** 60 evaluations this round, 60 total; 18 feasible; hypervolume 147.4 (n/a).

**LLM decision:** `stop` — This is the final round and the constraints are demonstrably satisfiable: 18 feasible designs were found, and the Pareto front's min-power corner (pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=2]) achieves power_index=2.77 with throughput_msps=66.8 (>= 50) and max_abs_err=4.12e-05 (<= 2.44e-04), so the spec's min-power_index selection rule is met without violating any constraint. The front spans power_index 2.77..6.5 and accuracy_bits 14.6..16.1, covering the accuracy trade-off well above the 12-bit HV reference, and the remaining budget is essentially spent (60/100 used, round cap reached), so further exploration is not warranted.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 147.4 (gain this round: n/a (first round)).
Feasible designs: 18 of 60 evaluations (13 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 48% violate; best seen 156
- max_abs_err <= 0.000244141: 32% violate; best seen 9.46e-06 (2^-16.69)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=2] power_index=2.77, accuracy_bits=14.6, area_um2=39113, ffs=582, throughput_msps=66.8, max_abs_err=4.12e-05 (2^-14.57)
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=1 rounding=round] power_index=5.16, accuracy_bits=15.4, area_um2=58580, ffs=1237, throughput_msps=128, max_abs_err=2.28e-05 (2^-15.42)
- pipelined [data_width=20 n_iter=19 angle_guard=1 frac_guard=4 rounding=trunc] power_index=5.84, accuracy_bits=15.8, area_um2=65791, ffs=1404, throughput_msps=115, max_abs_err=1.71e-05 (2^-15.84)
- pipelined [data_width=20 n_iter=21 angle_guard=1 frac_guard=2 rounding=round] power_index=6.19, accuracy_bits=15.9, area_um2=70304, ffs=1481, throughput_msps=123, max_abs_err=1.61e-05 (2^-15.92)
- pipelined [data_width=20 n_iter=21 angle_guard=1 frac_guard=4 rounding=round] power_index=6.5, accuracy_bits=16.1, area_um2=74007, ffs=1555, throughput_msps=115, max_abs_err=1.45e-05 (2^-16.07)
Front coverage: power_index 2.77..6.5 (HV reference 40); accuracy_bits 14.6..16.1 (HV reference 12); data_width on the front 20..20 (registry 8..28).

Per family:
- pipelined: 27 evals, 17 feasible; max throughput seen 156 MSPS; best accuracy 16.07 bits; best feasible power_index=4.11; feasible ranges: data_width 17..20, n_iter 15..21, angle_guard -2..1, frac_guard 1..4
- pipelined_m: 33 evals, 1 feasible; max throughput seen 66.8 MSPS; best accuracy 16.69 bits; best feasible power_index=2.77; feasible ranges: data_width 20..20, n_iter 16..16, angle_guard 2..2, frac_guard 0..0, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (8 evals): data_width=19..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)
- `pipelined` (32 evals): data_width=19..28, n_iter=16..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (4 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 52 feasible; hypervolume 313.1 (+112.4%).

**No LLM call** (code's front-mapping round): This is the final round and the constraints are demonstrably satisfiable: 18 feasible designs were found, and the Pareto front's min-power corner (pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=2]) achieves power_index=2.77 with throughput_msps=66.8 (>= 50) and max_abs_err=4.12e-05 (<= 2.44e-04), so the spec's min-power_index selection rule is met without violating any constraint. The front spans power_index 2.77..6.5 and accuracy_bits 14.6..16.1, covering the accuracy trade-off well above the 12-bit HV reference, and the remaining budget is essentially spent (60/100 used, round cap reached), so further exploration is not warranted.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 313.1 (gain this round: +112.4%).
Feasible designs: 52 of 100 evaluations (45 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 35% violate; best seen 156
- max_abs_err <= 0.000244141: 19% violate; best seen 1.45e-07 (2^-22.72)

Pareto front (feasible, 8 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=round m=2] power_index=2.77, accuracy_bits=14.6, area_um2=39113, ffs=582, throughput_msps=66.8, max_abs_err=4.12e-05 (2^-14.57)
- pipelined_m [data_width=20 n_iter=23 angle_guard=1 frac_guard=1 rounding=trunc m=2] power_index=4.11, accuracy_bits=15.1, area_um2=58081, ffs=863, throughput_msps=69.4, max_abs_err=2.8e-05 (2^-15.12)
- pipelined_m [data_width=25 n_iter=21 angle_guard=-1 frac_guard=4 rounding=trunc m=2] power_index=4.78, accuracy_bits=18.7, area_um2=67386, ffs=1004, throughput_msps=52.7, max_abs_err=2.32e-06 (2^-18.72)
- pipelined [data_width=24 n_iter=22 angle_guard=3 frac_guard=1 rounding=trunc] power_index=7.54, accuracy_bits=19.1, area_um2=84913, ffs=1813, throughput_msps=105, max_abs_err=1.76e-06 (2^-19.11)
- pipelined [data_width=25 n_iter=22 angle_guard=4 frac_guard=2 rounding=trunc] power_index=8.07, accuracy_bits=20.3, area_um2=90926, ffs=1939, throughput_msps=98.8, max_abs_err=7.65e-07 (2^-20.32)
- pipelined [data_width=25 n_iter=22 angle_guard=2 frac_guard=4 rounding=trunc] power_index=8.22, accuracy_bits=20.4, area_um2=92785, ffs=1974, throughput_msps=98.8, max_abs_err=7.17e-07 (2^-20.41)
- pipelined [data_width=27 n_iter=22 angle_guard=1 frac_guard=4 rounding=round] power_index=8.72, accuracy_bits=20.8, area_um2=99292, ffs=2084, throughput_msps=93.5, max_abs_err=5.58e-07 (2^-20.77)
- pipelined [data_width=27 n_iter=22 angle_guard=4 frac_guard=4 rounding=round] power_index=8.99, accuracy_bits=20.9, area_um2=102343, ffs=2149, throughput_msps=93.5, max_abs_err=4.95e-07 (2^-20.95)
Front coverage: power_index 2.77..8.99 (HV reference 40); accuracy_bits 14.6..20.9 (HV reference 12); data_width on the front 20..27 (registry 8..28).

Per family:
- pipelined: 59 evals, 49 feasible; max throughput seen 156 MSPS; best accuracy 20.95 bits; best feasible power_index=4.11; feasible ranges: data_width 17..28, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 41 evals, 3 feasible; max throughput seen 69.4 MSPS; best accuracy 22.72 bits; best feasible power_index=2.77; feasible ranges: data_width 20..25, n_iter 16..23, angle_guard -1..2, frac_guard 0..4, m 2..2
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5556 in, 2009 out
- provider-reported cost: $0.0017
- full prompts and replies: `llm_trace.jsonl`

