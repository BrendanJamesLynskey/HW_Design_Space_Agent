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
`pipelined:data_width=19,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 49467 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 13179 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 1066 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 128 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 128 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 141 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 4.42 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 6.35e-05 (2^-13.94) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 8.33 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 1.51e-05 (2^-16.01) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.98 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.9 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (21 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=19,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc` | 49467 | 1066 | 127.5 | 18 | 4.42 | 6.35e-05 (2^-13.94) | 13.94 |
| 1 | `pipelined:data_width=19,n_iter=16,angle_guard=3,frac_guard=1,rounding=trunc` | 50200 | 1081 | 123.1 | 18 | 4.48 | 5.64e-05 (2^-14.11) | 14.11 |
| 2 | `pipelined:data_width=20,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 50287 | 1085 | 123.1 | 18 | 4.5 | 4.12e-05 (2^-14.57) | 14.57 |
| 3 | `pipelined:data_width=20,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 53042 | 1140 | 123.1 | 18 | 4.73 | 3.93e-05 (2^-14.63) | 14.63 |
| 4 | `pipelined:data_width=20,n_iter=17,angle_guard=2,frac_guard=0,rounding=round` | 53531 | 1153 | 123.1 | 19 | 4.78 | 2.85e-05 (2^-15.10) | 15.10 |
| 5 | `pipelined:data_width=20,n_iter=18,angle_guard=2,frac_guard=0,rounding=round` | 56774 | 1221 | 123.1 | 20 | 5.07 | 2.42e-05 (2^-15.34) | 15.34 |
| 6 | `pipelined:data_width=20,n_iter=17,angle_guard=2,frac_guard=2,rounding=round` | 57541 | 1214 | 123.1 | 19 | 5.07 | 2.23e-05 (2^-15.45) | 15.45 |
| 7 | `pipelined:data_width=19,n_iter=18,angle_guard=4,frac_guard=4,rounding=round` | 63230 | 1331 | 118.9 | 20 | 5.56 | 1.35e-05 (2^-16.17) | 16.17 |
| 8 | `pipelined:data_width=23,n_iter=18,angle_guard=-1,frac_guard=3,rounding=trunc` | 66439 | 1422 | 107.9 | 20 | 5.91 | 1.23e-05 (2^-16.32) | 16.32 |
| 9 | `pipelined:data_width=27,n_iter=18,angle_guard=3,frac_guard=2,rounding=round` | 79532 | 1675 | 96.1 | 20 | 7 | 7.64e-06 (2^-17.00) | 17.00 |
| 10 | `pipelined:data_width=28,n_iter=18,angle_guard=3,frac_guard=2,rounding=trunc` | 80590 | 1726 | 93.5 | 20 | 7.17 | 7.64e-06 (2^-17.00) | 17.00 |
| 11 | `pipelined:data_width=27,n_iter=18,angle_guard=3,frac_guard=4,rounding=trunc` | 81243 | 1736 | 93.5 | 20 | 7.22 | 7.64e-06 (2^-17.00) | 17.00 |
| 12 | `pipelined:data_width=27,n_iter=19,angle_guard=3,frac_guard=4,rounding=round` | 87331 | 1836 | 93.5 | 21 | 7.67 | 3.84e-06 (2^-17.99) | 17.99 |
| 13 | `pipelined:data_width=23,n_iter=24,angle_guard=0,frac_guard=2,rounding=trunc` | 88288 | 1880 | 111.3 | 26 | 7.82 | 3.72e-06 (2^-18.04) | 18.04 |
| 14 | `pipelined:data_width=23,n_iter=24,angle_guard=1,frac_guard=3,rounding=trunc` | 91535 | 1947 | 107.9 | 26 | 8.11 | 2.2e-06 (2^-18.79) | 18.79 |
| 15 | `pipelined:data_width=23,n_iter=24,angle_guard=2,frac_guard=3,rounding=trunc` | 92646 | 1970 | 107.9 | 26 | 8.2 | 1.53e-06 (2^-19.32) | 19.32 |
| 16 | `pipelined:data_width=23,n_iter=24,angle_guard=3,frac_guard=3,rounding=trunc` | 93758 | 1994 | 107.9 | 26 | 8.3 | 1.25e-06 (2^-19.61) | 19.61 |
| 17 | `pipelined:data_width=23,n_iter=24,angle_guard=3,frac_guard=3,rounding=round` | 94977 | 1996 | 107.9 | 26 | 8.34 | 7.96e-07 (2^-20.26) | 20.26 |
| 18 | `pipelined:data_width=26,n_iter=29,angle_guard=2,frac_guard=3,rounding=round` | 125926 | 2642 | 98.8 | 31 | 11.1 | 1.5e-07 (2^-22.66) | 22.66 |
| 19 | `pipelined:data_width=28,n_iter=29,angle_guard=2,frac_guard=3,rounding=trunc` | 132644 | 2811 | 93.5 | 31 | 11.7 | 5.37e-08 (2^-24.15) | 24.15 |
| 20 | `pipelined:data_width=28,n_iter=30,angle_guard=4,frac_guard=3,rounding=trunc` | 140100 | 2967 | 91.1 | 32 | 12.4 | 3.83e-08 (2^-24.64) | 24.64 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Both assigned families produce one result per cycle, so throughput_msps equals Fmax and the 50 MSPS constraint is non-binding at these widths; the real constraint is max_abs_err <= 2^-12, which depends only on data_width, n_iter, angle_guard, frac_guard and rounding. I therefore centre the search on the accuracy boundary (W 12-20, N 8-20, guards -2..4 / 0..4, both rounding modes) so the front is mapped on both sides of feasibility, and weight pipelined_m higher because its reduced register count is the plausible route to the minimum power_index that the selection rule picks.*)
- `pipelined` (24 evals): data_width=12..20, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Fully-registered baseline: 1 result/cycle means the 50 MSPS constraint is met by any plausible Fmax, so the binding constraint is max_abs_err <= 2^-12. Sweeping W and N around the accuracy boundary (W~14-16, N~13-16) maps the power/accuracy trade-off and gives the reference point for the partially-registered variant.
- `pipelined_m` (36 evals): data_width=12..20, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Same bit-accurate datapath as pipelined but registers only every m stages, cutting pipeline FF count and hence power; since only 50 MSPS is required, the Fmax loss from larger m is affordable. This is the most likely source of the minimum-power feasible designs, so it gets the larger share, with m swept to expose the FF/Fmax trade-off.

**Result (code):** 60 evaluations this round, 60 total; 14 feasible; hypervolume 147.1 (n/a).

**LLM decision:** `stop` — Final round with 60/100 evals spent and no further exploration possible. The front is feasible and well-covered: 7 Pareto designs spanning power_index 4.42..5.56 and accuracy_bits 13.9..16.2, all satisfying throughput >= 50 MSPS (119-128 MSPS) and max_abs_err <= 2^-12 (best 1.35e-05 = 2^-16.17). The selection rule (min power_index) picks pipelined [data_width=19, n_iter=16, angle_guard=2, frac_guard=1, trunc] at power_index=4.42, 128 MSPS, max_abs_err=6.35e-05 (2^-13.94), comfortably inside both constraints. pipelined_m produced 0 feasible designs (max throughput 86.6 MSPS), so no unexplored family can improve the front; stopping is correct.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 147.1 (gain this round: n/a (first round)).
Feasible designs: 14 of 60 evaluations (11 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 52% violate; best seen 156
- max_abs_err <= 0.000244141: 48% violate; best seen 6.52e-06 (2^-17.23)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] power_index=4.42, accuracy_bits=13.9, area_um2=49467, ffs=1066, throughput_msps=128, max_abs_err=6.35e-05 (2^-13.94)
- pipelined [data_width=19 n_iter=16 angle_guard=3 frac_guard=1 rounding=trunc] power_index=4.48, accuracy_bits=14.1, area_um2=50200, ffs=1081, throughput_msps=123, max_abs_err=5.64e-05 (2^-14.11)
- pipelined [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] power_index=4.5, accuracy_bits=14.6, area_um2=50287, ffs=1085, throughput_msps=123, max_abs_err=4.12e-05 (2^-14.57)
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=0 rounding=round] power_index=4.78, accuracy_bits=15.1, area_um2=53531, ffs=1153, throughput_msps=123, max_abs_err=2.85e-05 (2^-15.10)
- pipelined [data_width=20 n_iter=18 angle_guard=2 frac_guard=0 rounding=round] power_index=5.07, accuracy_bits=15.3, area_um2=56774, ffs=1221, throughput_msps=123, max_abs_err=2.42e-05 (2^-15.34)
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=4 rounding=trunc] power_index=5.38, accuracy_bits=15.3, area_um2=60561, ffs=1294, throughput_msps=119, max_abs_err=2.42e-05 (2^-15.34)
- pipelined [data_width=19 n_iter=18 angle_guard=4 frac_guard=4 rounding=round] power_index=5.56, accuracy_bits=16.2, area_um2=63230, ffs=1331, throughput_msps=119, max_abs_err=1.35e-05 (2^-16.17)
Front coverage: power_index 4.42..5.56 (HV reference 40); accuracy_bits 13.9..16.2 (HV reference 12); data_width on the front 19..20 (registry 8..28).

Per family:
- pipelined: 24 evals, 14 feasible; max throughput seen 156 MSPS; best accuracy 16.17 bits; best feasible power_index=4.42; feasible ranges: data_width 19..20, n_iter 16..18, angle_guard 2..4, frac_guard 0..4
- pipelined_m: 36 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 17.23 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (40 evals): data_width=18..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (7 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 54 feasible; hypervolume 403.9 (+174.5%).

**No LLM call** (code's front-mapping round): Final round with 60/100 evals spent and no further exploration possible. The front is feasible and well-covered: 7 Pareto designs spanning power_index 4.42..5.56 and accuracy_bits 13.9..16.2, all satisfying throughput >= 50 MSPS (119-128 MSPS) and max_abs_err <= 2^-12 (best 1.35e-05 = 2^-16.17). The selection rule (min power_index) picks pipelined [data_width=19, n_iter=16, angle_guard=2, frac_guard=1, trunc] at power_index=4.42, 128 MSPS, max_abs_err=6.35e-05 (2^-13.94), comfortably inside both constraints. pipelined_m produced 0 feasible designs (max throughput 86.6 MSPS), so no unexplored family can improve the front; stopping is correct.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 403.9 (gain this round: +174.5%).
Feasible designs: 54 of 100 evaluations (46 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 31% violate; best seen 156
- max_abs_err <= 0.000244141: 29% violate; best seen 3.83e-08 (2^-24.64)

Pareto front (feasible, 21 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] power_index=4.42, accuracy_bits=13.9, area_um2=49467, ffs=1066, throughput_msps=128, max_abs_err=6.35e-05 (2^-13.94)
- pipelined [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] power_index=4.5, accuracy_bits=14.6, area_um2=50287, ffs=1085, throughput_msps=123, max_abs_err=4.12e-05 (2^-14.57)
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=0 rounding=round] power_index=4.78, accuracy_bits=15.1, area_um2=53531, ffs=1153, throughput_msps=123, max_abs_err=2.85e-05 (2^-15.10)
- pipelined [data_width=19 n_iter=18 angle_guard=4 frac_guard=4 rounding=round] power_index=5.56, accuracy_bits=16.2, area_um2=63230, ffs=1331, throughput_msps=119, max_abs_err=1.35e-05 (2^-16.17)
- pipelined [data_width=27 n_iter=18 angle_guard=3 frac_guard=2 rounding=round] power_index=7, accuracy_bits=17, area_um2=79532, ffs=1675, throughput_msps=96.1, max_abs_err=7.64e-06 (2^-17.00)
- pipelined [data_width=27 n_iter=18 angle_guard=3 frac_guard=4 rounding=trunc] power_index=7.22, accuracy_bits=17, area_um2=81243, ffs=1736, throughput_msps=93.5, max_abs_err=7.64e-06 (2^-17.00)
- pipelined [data_width=23 n_iter=24 angle_guard=0 frac_guard=2 rounding=trunc] power_index=7.82, accuracy_bits=18, area_um2=88288, ffs=1880, throughput_msps=111, max_abs_err=3.72e-06 (2^-18.04)
- pipelined [data_width=23 n_iter=24 angle_guard=3 frac_guard=3 rounding=trunc] power_index=8.3, accuracy_bits=19.6, area_um2=93758, ffs=1994, throughput_msps=108, max_abs_err=1.25e-06 (2^-19.61)
- pipelined [data_width=26 n_iter=29 angle_guard=2 frac_guard=3 rounding=round] power_index=11.1, accuracy_bits=22.7, area_um2=125926, ffs=2642, throughput_msps=98.8, max_abs_err=1.5e-07 (2^-22.66)
- pipelined [data_width=28 n_iter=30 angle_guard=4 frac_guard=3 rounding=trunc] power_index=12.4, accuracy_bits=24.6, area_um2=140100, ffs=2967, throughput_msps=91.1, max_abs_err=3.83e-08 (2^-24.64)
Front coverage: power_index 4.42..12.4 (HV reference 40); accuracy_bits 13.9..24.6 (HV reference 12); data_width on the front 19..28 (registry 8..28).

Per family:
- pipelined: 64 evals, 54 feasible; max throughput seen 156 MSPS; best accuracy 24.64 bits; best feasible power_index=4.42; feasible ranges: data_width 18..28, n_iter 16..30, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 36 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 17.23 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5665 in, 2217 out
- provider-reported cost: $0.0014
- full prompts and replies: `llm_trace.jsonl`

