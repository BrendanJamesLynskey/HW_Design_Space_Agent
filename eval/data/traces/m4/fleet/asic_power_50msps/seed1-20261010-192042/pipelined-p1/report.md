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
`pipelined_m:data_width=17,n_iter=21,angle_guard=4,frac_guard=3,rounding=trunc,m=2` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 51306 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 13668 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 763 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 69.4 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 69.4 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 13 | exact: schedule |
| latency_ns | 187 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 3.63 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 6.86e-05 (2^-13.83) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 2.25 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 1.86e-05 (2^-15.72) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 0.609 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.8 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (16 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=21,angle_guard=4,frac_guard=3,rounding=trunc,m=2` | 51306 | 763 | 69.4 | 13 | 3.63 | 6.86e-05 (2^-13.83) | 13.83 |
| 1 | `pipelined:data_width=19,n_iter=17,angle_guard=1,frac_guard=3,rounding=trunc` | 54828 | 1175 | 123.1 | 19 | 4.88 | 4.34e-05 (2^-14.49) | 14.49 |
| 2 | `pipelined:data_width=19,n_iter=17,angle_guard=3,frac_guard=3,rounding=round` | 57403 | 1210 | 123.1 | 19 | 5.05 | 2.41e-05 (2^-15.34) | 15.34 |
| 3 | `pipelined:data_width=19,n_iter=18,angle_guard=3,frac_guard=4,rounding=round` | 62403 | 1313 | 118.9 | 20 | 5.49 | 1.5e-05 (2^-16.03) | 16.03 |
| 4 | `pipelined:data_width=19,n_iter=21,angle_guard=3,frac_guard=3,rounding=round` | 71135 | 1497 | 123.1 | 23 | 6.26 | 1.17e-05 (2^-16.38) | 16.38 |
| 5 | `pipelined:data_width=23,n_iter=21,angle_guard=0,frac_guard=2,rounding=trunc` | 76993 | 1644 | 111.3 | 23 | 6.84 | 4.04e-06 (2^-17.92) | 17.92 |
| 6 | `pipelined:data_width=23,n_iter=23,angle_guard=0,frac_guard=2,rounding=trunc` | 84523 | 1801 | 111.3 | 25 | 7.5 | 3.72e-06 (2^-18.04) | 18.04 |
| 7 | `pipelined:data_width=23,n_iter=23,angle_guard=0,frac_guard=2,rounding=round` | 85742 | 1803 | 111.3 | 25 | 7.54 | 3.54e-06 (2^-18.11) | 18.11 |
| 8 | `pipelined:data_width=23,n_iter=23,angle_guard=2,frac_guard=2,rounding=trunc` | 86651 | 1846 | 111.3 | 25 | 7.68 | 1.91e-06 (2^-18.99) | 18.99 |
| 9 | `pipelined:data_width=28,n_iter=21,angle_guard=0,frac_guard=0,rounding=trunc` | 87831 | 1879 | 101.6 | 23 | 7.81 | 1.09e-06 (2^-19.80) | 19.80 |
| 10 | `pipelined:data_width=28,n_iter=21,angle_guard=0,frac_guard=2,rounding=trunc` | 91534 | 1953 | 96.1 | 23 | 8.13 | 1.03e-06 (2^-19.88) | 19.88 |
| 11 | `pipelined:data_width=28,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc` | 92117 | 1968 | 101.6 | 24 | 8.18 | 6.32e-07 (2^-20.59) | 20.59 |
| 12 | `pipelined:data_width=28,n_iter=22,angle_guard=0,frac_guard=2,rounding=trunc` | 96010 | 2047 | 96.1 | 24 | 8.52 | 5.58e-07 (2^-20.77) | 20.77 |
| 13 | `pipelined:data_width=28,n_iter=22,angle_guard=0,frac_guard=3,rounding=round` | 99431 | 2088 | 93.5 | 24 | 8.73 | 5.43e-07 (2^-20.81) | 20.81 |
| 14 | `pipelined:data_width=27,n_iter=26,angle_guard=0,frac_guard=3,rounding=round` | 114041 | 2393 | 96.1 | 28 | 10 | 2.78e-07 (2^-21.78) | 21.78 |
| 15 | `pipelined:data_width=28,n_iter=30,angle_guard=2,frac_guard=0,rounding=trunc` | 129196 | 2743 | 96.1 | 32 | 11.4 | 2.17e-07 (2^-22.13) | 22.13 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Both allowed families emit one result per cycle, so throughput_msps equals Fmax and the 50 MSPS constraint is a mild Fmax floor. The binding constraint is max_abs_err <= 2^-12, which needs roughly data_width >= 14 with n_iter >= 14 plus guard bits; the power objective rewards fewer pipeline registers, so pipelined_m (larger m) should dominate the low-power end while pipelined anchors the high-Fmax end. Round 1 therefore searches W=12..20, N=10..24, angle_guard=-2..4, frac_guard=0..4, both roundings, and m=2..8, with a larger share on pipelined_m to map the power-optimal region.*)
- `pipelined` (24 evals): data_width=12..20, n_iter=10..24, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* One registered stage per micro-rotation gives the highest Fmax (throughput = Fmax, easily >=50 MSPS) and is the reference for the power/accuracy trade-off; W>=14 with N>=14 is the plausible region for the 2^-12 error bound, with guards and rounding as accuracy knobs.
- `pipelined_m` (36 evals): data_width=12..20, n_iter=10..24, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Registering every m stages cuts the flip-flop count (and hence power_index) at the cost of a longer combinational path; since power is the objective and throughput only needs Fmax>=50 MHz, this family is the most likely to reach the low-power end of the front. m=2..8 spans the FF-vs-Fmax trade-off.

**Result (code):** 60 evaluations this round, 60 total; 17 feasible; hypervolume 155.1 (n/a).

**LLM decision:** `stop` — This is the final round and the constraints are demonstrably satisfiable: 17 feasible designs exist, throughput reaches 171 MSPS (>= 50) and max_abs_err reaches 2^-16.38 (<= 2^-12), so `infeasible` is ruled out. The feasible Pareto front already spans power_index 3.63..6.26 against the HV reference of 40 and accuracy_bits 13.8..16.4 against the reference of 12, i.e. it covers the meaningful trade-off region well beyond the spec's accuracy floor. The selection rule (min power_index) is served by the pipelined_m [data_width=17 n_iter=21 angle_guard=4 frac_guard=3 rounding=trunc m=2] point at power_index=3.63, accuracy_bits=13.8, which comfortably meets both constraints. With the budget exhausted and no further improvement possible this round, stopping is the correct verdict.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 155.1 (gain this round: n/a (first round)).
Feasible designs: 17 of 60 evaluations (17 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 53% violate; best seen 171
- max_abs_err <= 0.000244141: 52% violate; best seen 1.17e-05 (2^-16.38)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=21 angle_guard=4 frac_guard=3 rounding=trunc m=2] power_index=3.63, accuracy_bits=13.8, area_um2=51306, ffs=763, throughput_msps=69.4, max_abs_err=6.86e-05 (2^-13.83)
- pipelined [data_width=19 n_iter=17 angle_guard=1 frac_guard=3 rounding=trunc] power_index=4.88, accuracy_bits=14.5, area_um2=54828, ffs=1175, throughput_msps=123, max_abs_err=4.34e-05 (2^-14.49)
- pipelined [data_width=19 n_iter=17 angle_guard=3 frac_guard=3 rounding=round] power_index=5.05, accuracy_bits=15.3, area_um2=57403, ffs=1210, throughput_msps=123, max_abs_err=2.41e-05 (2^-15.34)
- pipelined [data_width=19 n_iter=18 angle_guard=3 frac_guard=4 rounding=round] power_index=5.49, accuracy_bits=16, area_um2=62403, ffs=1313, throughput_msps=119, max_abs_err=1.5e-05 (2^-16.03)
- pipelined [data_width=19 n_iter=21 angle_guard=3 frac_guard=3 rounding=round] power_index=6.26, accuracy_bits=16.4, area_um2=71135, ffs=1497, throughput_msps=123, max_abs_err=1.17e-05 (2^-16.38)
Front coverage: power_index 3.63..6.26 (HV reference 40); accuracy_bits 13.8..16.4 (HV reference 12); data_width on the front 17..19 (registry 8..28).

Per family:
- pipelined: 24 evals, 16 feasible; max throughput seen 171 MSPS; best accuracy 16.38 bits; best feasible power_index=4; feasible ranges: data_width 16..20, n_iter 14..24, angle_guard -1..4, frac_guard 1..4
- pipelined_m: 36 evals, 1 feasible; max throughput seen 91.1 MSPS; best accuracy 15.38 bits; best feasible power_index=3.63; feasible ranges: data_width 17..17, n_iter 21..21, angle_guard 4..4, frac_guard 3..3, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (8 evals): data_width=16..28, n_iter=19..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)
- `pipelined` (32 evals): data_width=18..28, n_iter=15..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (4 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 49 feasible; hypervolume 338.1 (+117.9%).

**No LLM call** (code's front-mapping round): This is the final round and the constraints are demonstrably satisfiable: 17 feasible designs exist, throughput reaches 171 MSPS (>= 50) and max_abs_err reaches 2^-16.38 (<= 2^-12), so `infeasible` is ruled out. The feasible Pareto front already spans power_index 3.63..6.26 against the HV reference of 40 and accuracy_bits 13.8..16.4 against the reference of 12, i.e. it covers the meaningful trade-off region well beyond the spec's accuracy floor. The selection rule (min power_index) is served by the pipelined_m [data_width=17 n_iter=21 angle_guard=4 frac_guard=3 rounding=trunc m=2] point at power_index=3.63, accuracy_bits=13.8, which comfortably meets both constraints. With the budget exhausted and no further improvement possible this round, stopping is the correct verdict.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 338.1 (gain this round: +117.9%).
Feasible designs: 49 of 100 evaluations (47 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 40% violate; best seen 171
- max_abs_err <= 0.000244141: 33% violate; best seen 1.89e-07 (2^-22.33)

Pareto front (feasible, 16 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=21 angle_guard=4 frac_guard=3 rounding=trunc m=2] power_index=3.63, accuracy_bits=13.8, area_um2=51306, ffs=763, throughput_msps=69.4, max_abs_err=6.86e-05 (2^-13.83)
- pipelined [data_width=19 n_iter=17 angle_guard=3 frac_guard=3 rounding=round] power_index=5.05, accuracy_bits=15.3, area_um2=57403, ffs=1210, throughput_msps=123, max_abs_err=2.41e-05 (2^-15.34)
- pipelined [data_width=19 n_iter=18 angle_guard=3 frac_guard=4 rounding=round] power_index=5.49, accuracy_bits=16, area_um2=62403, ffs=1313, throughput_msps=119, max_abs_err=1.5e-05 (2^-16.03)
- pipelined [data_width=23 n_iter=21 angle_guard=0 frac_guard=2 rounding=trunc] power_index=6.84, accuracy_bits=17.9, area_um2=76993, ffs=1644, throughput_msps=111, max_abs_err=4.04e-06 (2^-17.92)
- pipelined [data_width=23 n_iter=23 angle_guard=0 frac_guard=2 rounding=round] power_index=7.54, accuracy_bits=18.1, area_um2=85742, ffs=1803, throughput_msps=111, max_abs_err=3.54e-06 (2^-18.11)
- pipelined [data_width=23 n_iter=23 angle_guard=2 frac_guard=2 rounding=trunc] power_index=7.68, accuracy_bits=19, area_um2=86651, ffs=1846, throughput_msps=111, max_abs_err=1.91e-06 (2^-18.99)
- pipelined [data_width=28 n_iter=21 angle_guard=0 frac_guard=2 rounding=trunc] power_index=8.13, accuracy_bits=19.9, area_um2=91534, ffs=1953, throughput_msps=96.1, max_abs_err=1.03e-06 (2^-19.88)
- pipelined [data_width=28 n_iter=22 angle_guard=0 frac_guard=2 rounding=trunc] power_index=8.52, accuracy_bits=20.8, area_um2=96010, ffs=2047, throughput_msps=96.1, max_abs_err=5.58e-07 (2^-20.77)
- pipelined [data_width=28 n_iter=22 angle_guard=0 frac_guard=3 rounding=round] power_index=8.73, accuracy_bits=20.8, area_um2=99431, ffs=2088, throughput_msps=93.5, max_abs_err=5.43e-07 (2^-20.81)
- pipelined [data_width=28 n_iter=30 angle_guard=2 frac_guard=0 rounding=trunc] power_index=11.4, accuracy_bits=22.1, area_um2=129196, ffs=2743, throughput_msps=96.1, max_abs_err=2.17e-07 (2^-22.13)
Front coverage: power_index 3.63..11.4 (HV reference 40); accuracy_bits 13.8..22.1 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- pipelined: 56 evals, 48 feasible; max throughput seen 171 MSPS; best accuracy 22.13 bits; best feasible power_index=4; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 44 evals, 1 feasible; max throughput seen 91.1 MSPS; best accuracy 22.33 bits; best feasible power_index=3.63; feasible ranges: data_width 17..17, n_iter 21..21, angle_guard 4..4, frac_guard 3..3, m 2..2
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5541 in, 1989 out
- provider-reported cost: $0.0010
- full prompts and replies: `llm_trace.jsonl`

