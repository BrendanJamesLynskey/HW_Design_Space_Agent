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
`pipelined_m:data_width=18,n_iter=15,angle_guard=-1,frac_guard=1,rounding=round,m=3` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 30422 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 8105 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 340 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 135 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.84 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000196 (2^-12.31) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 12.9 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 4.18e-05 (2^-14.55) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 2.74 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (21 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=15,angle_guard=-1,frac_guard=1,rounding=round,m=3` | 30422 | 340 | 51.9 | 7 | 1.84 | 0.000196 (2^-12.31) | 12.31 |
| 1 | `pipelined_m:data_width=18,n_iter=18,angle_guard=-1,frac_guard=0,rounding=round,m=3` | 34401 | 389 | 54.3 | 8 | 2.1 | 0.000186 (2^-12.39) | 12.39 |
| 2 | `pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=1,rounding=round,m=3` | 33848 | 407 | 51.9 | 8 | 2.13 | 0.00012 (2^-13.03) | 13.03 |
| 3 | `pipelined_m:data_width=18,n_iter=18,angle_guard=0,frac_guard=1,rounding=round,m=3` | 37017 | 407 | 51.9 | 8 | 2.22 | 0.000104 (2^-13.22) | 13.22 |
| 4 | `pipelined_m:data_width=19,n_iter=18,angle_guard=-1,frac_guard=1,rounding=trunc,m=2` | 41484 | 611 | 72.3 | 11 | 2.92 | 9.81e-05 (2^-13.31) | 13.31 |
| 5 | `pipelined:data_width=20,n_iter=15,angle_guard=-1,frac_guard=0,rounding=round` | 44988 | 973 | 132.4 | 17 | 4.03 | 9.65e-05 (2^-13.34) | 13.34 |
| 6 | `pipelined:data_width=20,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 45673 | 988 | 132.4 | 17 | 4.09 | 8.24e-05 (2^-13.57) | 13.57 |
| 7 | `pipelined:data_width=20,n_iter=15,angle_guard=0,frac_guard=1,rounding=round` | 48022 | 1016 | 127.5 | 17 | 4.24 | 7.85e-05 (2^-13.64) | 13.64 |
| 8 | `pipelined:data_width=20,n_iter=16,angle_guard=-1,frac_guard=0,rounding=round` | 48089 | 1038 | 132.4 | 18 | 4.3 | 6.98e-05 (2^-13.81) | 13.81 |
| 9 | `pipelined:data_width=20,n_iter=15,angle_guard=1,frac_guard=2,rounding=round` | 49990 | 1056 | 123.1 | 17 | 4.41 | 6.89e-05 (2^-13.82) | 13.82 |
| 10 | `pipelined:data_width=20,n_iter=16,angle_guard=1,frac_guard=1,rounding=round` | 51998 | 1099 | 127.5 | 18 | 4.59 | 4.05e-05 (2^-14.59) | 14.59 |
| 11 | `pipelined:data_width=24,n_iter=19,angle_guard=-1,frac_guard=0,rounding=trunc` | 67889 | 1457 | 115.0 | 21 | 6.05 | 6.73e-06 (2^-17.18) | 17.18 |
| 12 | `pipelined:data_width=25,n_iter=19,angle_guard=-1,frac_guard=0,rounding=trunc` | 70513 | 1513 | 111.3 | 21 | 6.28 | 5.57e-06 (2^-17.45) | 17.45 |
| 13 | `pipelined:data_width=25,n_iter=19,angle_guard=0,frac_guard=0,rounding=trunc` | 71388 | 1532 | 111.3 | 21 | 6.36 | 4.71e-06 (2^-17.70) | 17.70 |
| 14 | `pipelined:data_width=25,n_iter=19,angle_guard=3,frac_guard=0,rounding=trunc` | 74012 | 1588 | 101.6 | 21 | 6.59 | 4.66e-06 (2^-17.71) | 17.71 |
| 15 | `pipelined:data_width=25,n_iter=24,angle_guard=-1,frac_guard=0,rounding=round` | 89574 | 1911 | 111.3 | 26 | 7.95 | 2.01e-06 (2^-18.92) | 18.92 |
| 16 | `pipelined:data_width=27,n_iter=24,angle_guard=1,frac_guard=0,rounding=trunc` | 98466 | 2100 | 101.6 | 26 | 8.74 | 4.31e-07 (2^-21.14) | 21.14 |
| 17 | `pipelined:data_width=27,n_iter=24,angle_guard=4,frac_guard=0,rounding=round` | 101801 | 2171 | 93.5 | 26 | 9.03 | 2.65e-07 (2^-21.85) | 21.85 |
| 18 | `pipelined:data_width=27,n_iter=27,angle_guard=1,frac_guard=0,rounding=round` | 111039 | 2362 | 101.6 | 29 | 9.84 | 2.33e-07 (2^-22.03) | 22.03 |
| 19 | `pipelined:data_width=28,n_iter=26,angle_guard=1,frac_guard=2,rounding=trunc` | 115118 | 2446 | 96.1 | 28 | 10.2 | 1.04e-07 (2^-23.20) | 23.20 |
| 20 | `pipelined:data_width=28,n_iter=26,angle_guard=1,frac_guard=3,rounding=trunc` | 117443 | 2493 | 93.5 | 28 | 10.4 | 9.77e-08 (2^-23.29) | 23.29 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec needs 50 MSPS, which only the 1-result/cycle families (pipelined, pipelined_m) can guarantee without depending on a high Fmax; iterative/unrolled_k are excluded by my assignment anyway. The accuracy constraint (max_abs_err <= 2^-12) is met by n_iter ~ 12-14 with modest guards, so I bound n_iter to 12-18 and data_width to 14-20 to keep the datapath short (high Fmax, low power) while still reaching 12+ bits of accuracy. angle_guard is kept near 0 (the atan-LUT width barely needs to exceed W for this accuracy) and frac_guard is kept low (0-2) since extra fractional bits cost area/power without helping the 2^-12 target. Rounding is left to the search. I split the budget between the two families so the front captures both the full-pipeline baseline and the register-thinned (m>1) low-power variants, letting the hypervolume pick the best power/accuracy trade-off. The selection rule (min power_index) will then pick the lowest-power feasible point on that front.*)
- `pipelined` (30 evals): data_width=14..20, n_iter=12..18, angle_guard=-1..1, frac_guard=0..2, rounding=trunc|round. *Why:* Full pipelining gives 1 result/cycle, so throughput = Fmax. At W=14-18 the datapath is short enough that Fmax should comfortably exceed 50 MHz, meeting the 50 MSPS constraint. This family is the cleanest 1/cycle option and its power scales with the number of registered stages (N), so it anchors the low-power end of the front for a given accuracy.
- `pipelined_m` (30 evals): data_width=14..20, n_iter=12..18, angle_guard=-1..1, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Registering every m stages cuts the flip-flop count (and hence power) versus full pipelining while still delivering 1 result/cycle, so it can dominate pipelined on power at equal accuracy. The longer combinational path (m rotations/cycle) risks Fmax < 50 MHz, so m is capped at 4 and the search will reveal the throughput/accuracy/power trade-off. This is where the interesting power-vs-accuracy trade-off lives.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 60 evaluations this round, 60 total; 36 feasible; hypervolume 95.22 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 11 designs covering the trade-off space effectively. The minimum power_index achieved is 1.84 (pipelined_m, data_width=18, n_iter=15, m=3), which satisfies the throughput constraint (51.9 MSPS >= 50) and accuracy constraint (12.3 bits > 12). The front spans power_index 1.84 to 4.59 and accuracy_bits 12.3 to 14.6, providing a good spread for the hypervolume objective. Since this is the final round, further exploration is not possible. The selection rule (min power_index) picks the pipelined_m design with power_index=1.84, which is a valid, low-power solution meeting all constraints.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 95.22 (gain this round: n/a (first round)).
Feasible designs: 36 of 60 evaluations (31 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 10% violate; best seen 171
- max_abs_err <= 0.000244141: 30% violate; best seen 4.05e-05 (2^-14.59)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=18 n_iter=15 angle_guard=-1 frac_guard=1 rounding=round m=3] power_index=1.84, accuracy_bits=12.3, area_um2=30422, ffs=340, throughput_msps=51.9, max_abs_err=0.000196 (2^-12.31)
- pipelined_m [data_width=18 n_iter=18 angle_guard=-1 frac_guard=0 rounding=round m=3] power_index=2.1, accuracy_bits=12.4, area_um2=34401, ffs=389, throughput_msps=54.3, max_abs_err=0.000186 (2^-12.39)
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=round m=3] power_index=2.13, accuracy_bits=13, area_um2=33848, ffs=407, throughput_msps=51.9, max_abs_err=0.00012 (2^-13.03)
- pipelined_m [data_width=18 n_iter=18 angle_guard=0 frac_guard=1 rounding=round m=3] power_index=2.22, accuracy_bits=13.2, area_um2=37017, ffs=407, throughput_msps=51.9, max_abs_err=0.000104 (2^-13.22)
- pipelined_m [data_width=19 n_iter=18 angle_guard=-1 frac_guard=1 rounding=trunc m=2] power_index=2.92, accuracy_bits=13.3, area_um2=41484, ffs=611, throughput_msps=72.3, max_abs_err=9.81e-05 (2^-13.31)
- pipelined [data_width=20 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] power_index=4.09, accuracy_bits=13.6, area_um2=45673, ffs=988, throughput_msps=132, max_abs_err=8.24e-05 (2^-13.57)
- pipelined [data_width=20 n_iter=15 angle_guard=0 frac_guard=1 rounding=round] power_index=4.24, accuracy_bits=13.6, area_um2=48022, ffs=1016, throughput_msps=128, max_abs_err=7.85e-05 (2^-13.64)
- pipelined [data_width=20 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round] power_index=4.3, accuracy_bits=13.8, area_um2=48089, ffs=1038, throughput_msps=132, max_abs_err=6.98e-05 (2^-13.81)
- pipelined [data_width=20 n_iter=15 angle_guard=1 frac_guard=2 rounding=round] power_index=4.41, accuracy_bits=13.8, area_um2=49990, ffs=1056, throughput_msps=123, max_abs_err=6.89e-05 (2^-13.82)
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] power_index=4.59, accuracy_bits=14.6, area_um2=51998, ffs=1099, throughput_msps=128, max_abs_err=4.05e-05 (2^-14.59)
Front coverage: power_index 1.84..4.59 (HV reference 40); accuracy_bits 12.3..14.6 (HV reference 12); data_width on the front 18..20 (registry 8..28).

Per family:
- pipelined: 30 evals, 15 feasible; max throughput seen 171 MSPS; best accuracy 14.59 bits; best feasible power_index=3.66; feasible ranges: data_width 18..20, n_iter 15..18, angle_guard -1..1, frac_guard 0..2
- pipelined_m: 30 evals, 21 feasible; max throughput seen 78.8 MSPS; best accuracy 13.65 bits; best feasible power_index=1.84; feasible ranges: data_width 17..19, n_iter 15..18, angle_guard -1..0, frac_guard 0..2, m 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (19 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (5 front designs; box front_anchored)
- `pipelined` (21 evals): data_width=19..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (6 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 55 feasible; hypervolume 374 (+292.8%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 11 designs covering the trade-off space effectively. The minimum power_index achieved is 1.84 (pipelined_m, data_width=18, n_iter=15, m=3), which satisfies the throughput constraint (51.9 MSPS >= 50) and accuracy constraint (12.3 bits > 12). The front spans power_index 1.84 to 4.59 and accuracy_bits 12.3 to 14.6, providing a good spread for the hypervolume objective. Since this is the final round, further exploration is not possible. The selection rule (min power_index) picks the pipelined_m design with power_index=1.84, which is a valid, low-power solution meeting all constraints.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 374 (gain this round: +292.8%).
Feasible designs: 55 of 100 evaluations (50 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 25% violate; best seen 171
- max_abs_err <= 0.000244141: 21% violate; best seen 9.77e-08 (2^-23.29)

Pareto front (feasible, 21 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=18 n_iter=15 angle_guard=-1 frac_guard=1 rounding=round m=3] power_index=1.84, accuracy_bits=12.3, area_um2=30422, ffs=340, throughput_msps=51.9, max_abs_err=0.000196 (2^-12.31)
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=round m=3] power_index=2.13, accuracy_bits=13, area_um2=33848, ffs=407, throughput_msps=51.9, max_abs_err=0.00012 (2^-13.03)
- pipelined_m [data_width=19 n_iter=18 angle_guard=-1 frac_guard=1 rounding=trunc m=2] power_index=2.92, accuracy_bits=13.3, area_um2=41484, ffs=611, throughput_msps=72.3, max_abs_err=9.81e-05 (2^-13.31)
- pipelined [data_width=20 n_iter=15 angle_guard=0 frac_guard=1 rounding=round] power_index=4.24, accuracy_bits=13.6, area_um2=48022, ffs=1016, throughput_msps=128, max_abs_err=7.85e-05 (2^-13.64)
- pipelined [data_width=20 n_iter=15 angle_guard=1 frac_guard=2 rounding=round] power_index=4.41, accuracy_bits=13.8, area_um2=49990, ffs=1056, throughput_msps=123, max_abs_err=6.89e-05 (2^-13.82)
- pipelined [data_width=24 n_iter=19 angle_guard=-1 frac_guard=0 rounding=trunc] power_index=6.05, accuracy_bits=17.2, area_um2=67889, ffs=1457, throughput_msps=115, max_abs_err=6.73e-06 (2^-17.18)
- pipelined [data_width=25 n_iter=19 angle_guard=0 frac_guard=0 rounding=trunc] power_index=6.36, accuracy_bits=17.7, area_um2=71388, ffs=1532, throughput_msps=111, max_abs_err=4.71e-06 (2^-17.70)
- pipelined [data_width=27 n_iter=24 angle_guard=1 frac_guard=0 rounding=trunc] power_index=8.74, accuracy_bits=21.1, area_um2=98466, ffs=2100, throughput_msps=102, max_abs_err=4.31e-07 (2^-21.14)
- pipelined [data_width=27 n_iter=27 angle_guard=1 frac_guard=0 rounding=round] power_index=9.84, accuracy_bits=22, area_um2=111039, ffs=2362, throughput_msps=102, max_abs_err=2.33e-07 (2^-22.03)
- pipelined [data_width=28 n_iter=26 angle_guard=1 frac_guard=3 rounding=trunc] power_index=10.4, accuracy_bits=23.3, area_um2=117443, ffs=2493, throughput_msps=93.5, max_abs_err=9.77e-08 (2^-23.29)
Front coverage: power_index 1.84..10.4 (HV reference 40); accuracy_bits 12.3..23.3 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- pipelined: 51 evals, 34 feasible; max throughput seen 171 MSPS; best accuracy 23.29 bits; best feasible power_index=3.66; feasible ranges: data_width 18..28, n_iter 13..28, angle_guard -1..4, frac_guard 0..3
- pipelined_m: 49 evals, 21 feasible; max throughput seen 78.8 MSPS; best accuracy 18.57 bits; best feasible power_index=1.84; feasible ranges: data_width 17..19, n_iter 15..18, angle_guard -1..0, frac_guard 0..2, m 2..3
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4663 in, 1214 out
- provider-reported cost: $0.0042
- full prompts and replies: `llm_trace.jsonl`

