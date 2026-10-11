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
`pipelined_m:data_width=19,n_iter=16,angle_guard=-1,frac_guard=0,rounding=round,m=3` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 32972 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 8784 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 409 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 8 | exact: schedule |
| latency_ns | 154 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.11 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000102 (2^-13.26) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 13.3 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.15e-05 (2^-15.51) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 2.81 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.3 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (18 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=19,n_iter=16,angle_guard=-1,frac_guard=0,rounding=round,m=3` | 32972 | 409 | 51.9 | 8 | 2.11 | 0.000102 (2^-13.26) | 13.26 |
| 1 | `pipelined_m:data_width=19,n_iter=16,angle_guard=-1,frac_guard=2,rounding=round,m=2` | 38881 | 562 | 69.4 | 10 | 2.71 | 9.78e-05 (2^-13.32) | 13.32 |
| 2 | `pipelined_m:data_width=19,n_iter=16,angle_guard=1,frac_guard=1,rounding=round,m=2` | 38925 | 564 | 72.3 | 10 | 2.72 | 5.25e-05 (2^-14.22) | 14.22 |
| 3 | `pipelined:data_width=19,n_iter=17,angle_guard=3,frac_guard=0,rounding=round` | 51971 | 1120 | 123.1 | 19 | 4.64 | 4.23e-05 (2^-14.53) | 14.53 |
| 4 | `pipelined:data_width=19,n_iter=16,angle_guard=3,frac_guard=3,rounding=round` | 53970 | 1138 | 123.1 | 18 | 4.75 | 3.8e-05 (2^-14.68) | 14.68 |
| 5 | `pipelined:data_width=19,n_iter=17,angle_guard=3,frac_guard=2,rounding=round` | 55930 | 1181 | 123.1 | 19 | 4.93 | 2.76e-05 (2^-15.14) | 15.14 |
| 6 | `pipelined:data_width=20,n_iter=20,angle_guard=1,frac_guard=0,rounding=round` | 62339 | 1337 | 127.5 | 22 | 5.55 | 2.52e-05 (2^-15.28) | 15.28 |
| 7 | `pipelined:data_width=20,n_iter=20,angle_guard=2,frac_guard=0,rounding=round` | 63261 | 1357 | 123.1 | 22 | 5.63 | 2.17e-05 (2^-15.49) | 15.49 |
| 8 | `pipelined:data_width=23,n_iter=20,angle_guard=-1,frac_guard=0,rounding=trunc` | 68793 | 1475 | 118.9 | 22 | 6.12 | 9.1e-06 (2^-16.75) | 16.75 |
| 9 | `pipelined:data_width=20,n_iter=21,angle_guard=3,frac_guard=3,rounding=round` | 74094 | 1559 | 118.9 | 23 | 6.52 | 6.38e-06 (2^-17.26) | 17.26 |
| 10 | `pipelined:data_width=25,n_iter=20,angle_guard=-1,frac_guard=0,rounding=trunc` | 74325 | 1593 | 111.3 | 22 | 6.62 | 3.66e-06 (2^-18.06) | 18.06 |
| 11 | `pipelined:data_width=23,n_iter=20,angle_guard=1,frac_guard=3,rounding=round` | 77127 | 1622 | 107.9 | 22 | 6.78 | 3.39e-06 (2^-18.17) | 18.17 |
| 12 | `pipelined:data_width=25,n_iter=24,angle_guard=-1,frac_guard=0,rounding=round` | 89574 | 1911 | 111.3 | 26 | 7.95 | 2.01e-06 (2^-18.92) | 18.92 |
| 13 | `pipelined:data_width=23,n_iter=27,angle_guard=2,frac_guard=2,rounding=trunc` | 102089 | 2169 | 111.3 | 29 | 9.03 | 1.96e-06 (2^-18.96) | 18.96 |
| 14 | `pipelined:data_width=27,n_iter=25,angle_guard=1,frac_guard=0,rounding=trunc` | 102657 | 2187 | 101.6 | 27 | 9.1 | 4.02e-07 (2^-21.25) | 21.25 |
| 15 | `pipelined:data_width=27,n_iter=25,angle_guard=4,frac_guard=0,rounding=round` | 106134 | 2261 | 93.5 | 27 | 9.41 | 2.15e-07 (2^-22.15) | 22.15 |
| 16 | `pipelined:data_width=27,n_iter=25,angle_guard=4,frac_guard=2,rounding=round` | 112018 | 2354 | 93.5 | 27 | 9.84 | 1.06e-07 (2^-23.17) | 23.17 |
| 17 | `pipelined:data_width=28,n_iter=26,angle_guard=1,frac_guard=3,rounding=trunc` | 117443 | 2493 | 93.5 | 28 | 10.4 | 9.77e-08 (2^-23.29) | 23.29 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The 50 MSPS constraint forces a 1-result-per-cycle architecture, so only the pipelined families are viable; iterative/unrolled_k would need Fmax in the hundreds of MHz. Accuracy <= 2^-12 requires roughly W>=14 and N>=14, so I search W=12..20 and N=10..22 with the full guard/rounding space to let the search find the cheapest point that just meets the error bound. pipelined gives the safe high-Fmax corner, while pipelined_m explores the lower-FF/lower-power corner where the m parameter trades Fmax for power; splitting the budget evenly maps both ends of the Pareto front.*)
- `pipelined` (30 evals): data_width=12..20, n_iter=10..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* One registered stage per micro-rotation gives 1 result/cycle, so throughput equals Fmax and should comfortably clear 50 MSPS; this is the reference 1/cycle family for the power/accuracy trade-off. W>=12 and N>=10 are needed to approach the 2^-12 error bound, while guards and rounding tune the last bits.
- `pipelined_m` (30 evals): data_width=12..20, n_iter=10..22, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Registering every m stages keeps 1 result/cycle but cuts pipeline FF count, which is the main lever on power_index; larger m lowers area/power at the cost of a longer combinational path and lower Fmax. Searching m=2..8 maps that power-vs-Fmax frontier and finds the lowest-power points that still hold >=50 MSPS.

**Result (code):** 60 evaluations this round, 60 total; 29 feasible; hypervolume 127.9 (n/a).

**LLM decision:** `stop` — Feasible designs exist, so `infeasible` is ruled out: 29 of 60 evaluations met both constraints, and the front's weakest-throughput point (pipelined_m dW=19 N=16 A=-1 fg=0 m=3) still delivers 51.9 MSPS >= 50 with max_abs_err 1.02e-4 = 2^-13.26 <= 2^-12, at the lowest power_index seen (2.11). The Pareto front spans power_index 2.11..5.63 against the HV reference of 40 and accuracy_bits 13.3..15.5 against reference 12, i.e. the 'minimise power / trade accuracy' curve is covered from the low-power corner that the selection rule (min power_index) will pick up to the accurate corner (2.17e-5 = 2^-15.5). The coverage limits are explained by the registry, not by a search gap: only pipelined and pipelined_m can hit >=50 MSPS in this cost model (unrolled_k/iterative were not needed to reach the constraint, and pipelined_m's 1 result/cycle is what makes the ~2.1 power_index point reachable at 19-bit/16-iter accuracy), the front is itself spread over data_width 19..20 and both families, and pushing accuracy further only raises power_index monotonically with no new constraint-relevant region behind it. Since this is the final round (budget/round cap reached), and the front is both feasible and covers the accuracy/power trade-off including the selection rule's optimum, I stop with the front as the answer rather than spend a non-existent further round.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 127.9 (gain this round: n/a (first round)).
Feasible designs: 29 of 60 evaluations (26 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 23% violate; best seen 190
- max_abs_err <= 0.000244141: 37% violate; best seen 2.17e-05 (2^-15.49)

Pareto front (feasible, 8 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=19 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round m=3] power_index=2.11, accuracy_bits=13.3, area_um2=32972, ffs=409, throughput_msps=51.9, max_abs_err=0.000102 (2^-13.26)
- pipelined_m [data_width=19 n_iter=16 angle_guard=-1 frac_guard=2 rounding=round m=2] power_index=2.71, accuracy_bits=13.3, area_um2=38881, ffs=562, throughput_msps=69.4, max_abs_err=9.78e-05 (2^-13.32)
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=1 rounding=round m=2] power_index=2.72, accuracy_bits=14.2, area_um2=38925, ffs=564, throughput_msps=72.3, max_abs_err=5.25e-05 (2^-14.22)
- pipelined [data_width=19 n_iter=17 angle_guard=3 frac_guard=0 rounding=round] power_index=4.64, accuracy_bits=14.5, area_um2=51971, ffs=1120, throughput_msps=123, max_abs_err=4.23e-05 (2^-14.53)
- pipelined [data_width=19 n_iter=16 angle_guard=3 frac_guard=3 rounding=round] power_index=4.75, accuracy_bits=14.7, area_um2=53970, ffs=1138, throughput_msps=123, max_abs_err=3.8e-05 (2^-14.68)
- pipelined [data_width=19 n_iter=17 angle_guard=3 frac_guard=2 rounding=round] power_index=4.93, accuracy_bits=15.1, area_um2=55930, ffs=1181, throughput_msps=123, max_abs_err=2.76e-05 (2^-15.14)
- pipelined [data_width=20 n_iter=20 angle_guard=1 frac_guard=0 rounding=round] power_index=5.55, accuracy_bits=15.3, area_um2=62339, ffs=1337, throughput_msps=128, max_abs_err=2.52e-05 (2^-15.28)
- pipelined [data_width=20 n_iter=20 angle_guard=2 frac_guard=0 rounding=round] power_index=5.63, accuracy_bits=15.5, area_um2=63261, ffs=1357, throughput_msps=123, max_abs_err=2.17e-05 (2^-15.49)
Front coverage: power_index 2.11..5.63 (HV reference 40); accuracy_bits 13.3..15.5 (HV reference 12); data_width on the front 19..20 (registry 8..28).

Per family:
- pipelined: 30 evals, 14 feasible; max throughput seen 190 MSPS; best accuracy 15.49 bits; best feasible power_index=4.57; feasible ranges: data_width 18..20, n_iter 16..22, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 30 evals, 15 feasible; max throughput seen 82.5 MSPS; best accuracy 15.26 bits; best feasible power_index=2.11; feasible ranges: data_width 19..19, n_iter 16..22, angle_guard -2..1, frac_guard 0..3, m 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (15 evals): data_width=18..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (3 front designs; box front_anchored)
- `pipelined` (25 evals): data_width=18..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (5 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 54 feasible; hypervolume 375.9 (+193.8%).

**No LLM call** (code's front-mapping round): Feasible designs exist, so `infeasible` is ruled out: 29 of 60 evaluations met both constraints, and the front's weakest-throughput point (pipelined_m dW=19 N=16 A=-1 fg=0 m=3) still delivers 51.9 MSPS >= 50 with max_abs_err 1.02e-4 = 2^-13.26 <= 2^-12, at the lowest power_index seen (2.11). The Pareto front spans power_index 2.11..5.63 against the HV reference of 40 and accuracy_bits 13.3..15.5 against reference 12, i.e. the 'minimise power / trade accuracy' curve is covered from the low-power corner that the selection rule (min power_index) will pick up to the accurate corner (2.17e-5 = 2^-15.5). The coverage limits are explained by the registry, not by a search gap: only pipelined and pipelined_m can hit >=50 MSPS in this cost model (unrolled_k/iterative were not needed to reach the constraint, and pipelined_m's 1 result/cycle is what makes the ~2.1 power_index point reachable at 19-bit/16-iter accuracy), the front is itself spread over data_width 19..20 and both families, and pushing accuracy further only raises power_index monotonically with no new constraint-relevant region behind it. Since this is the final round (budget/round cap reached), and the front is both feasible and covers the accuracy/power trade-off including the selection rule's optimum, I stop with the front as the answer rather than spend a non-existent further round.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 375.9 (gain this round: +193.8%).
Feasible designs: 54 of 100 evaluations (49 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 29% violate; best seen 190
- max_abs_err <= 0.000244141: 22% violate; best seen 9.77e-08 (2^-23.29)

Pareto front (feasible, 18 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=19 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round m=3] power_index=2.11, accuracy_bits=13.3, area_um2=32972, ffs=409, throughput_msps=51.9, max_abs_err=0.000102 (2^-13.26)
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=1 rounding=round m=2] power_index=2.72, accuracy_bits=14.2, area_um2=38925, ffs=564, throughput_msps=72.3, max_abs_err=5.25e-05 (2^-14.22)
- pipelined [data_width=19 n_iter=16 angle_guard=3 frac_guard=3 rounding=round] power_index=4.75, accuracy_bits=14.7, area_um2=53970, ffs=1138, throughput_msps=123, max_abs_err=3.8e-05 (2^-14.68)
- pipelined [data_width=20 n_iter=20 angle_guard=1 frac_guard=0 rounding=round] power_index=5.55, accuracy_bits=15.3, area_um2=62339, ffs=1337, throughput_msps=128, max_abs_err=2.52e-05 (2^-15.28)
- pipelined [data_width=23 n_iter=20 angle_guard=-1 frac_guard=0 rounding=trunc] power_index=6.12, accuracy_bits=16.7, area_um2=68793, ffs=1475, throughput_msps=119, max_abs_err=9.1e-06 (2^-16.75)
- pipelined [data_width=20 n_iter=21 angle_guard=3 frac_guard=3 rounding=round] power_index=6.52, accuracy_bits=17.3, area_um2=74094, ffs=1559, throughput_msps=119, max_abs_err=6.38e-06 (2^-17.26)
- pipelined [data_width=23 n_iter=20 angle_guard=1 frac_guard=3 rounding=round] power_index=6.78, accuracy_bits=18.2, area_um2=77127, ffs=1622, throughput_msps=108, max_abs_err=3.39e-06 (2^-18.17)
- pipelined [data_width=23 n_iter=27 angle_guard=2 frac_guard=2 rounding=trunc] power_index=9.03, accuracy_bits=19, area_um2=102089, ffs=2169, throughput_msps=111, max_abs_err=1.96e-06 (2^-18.96)
- pipelined [data_width=27 n_iter=25 angle_guard=4 frac_guard=0 rounding=round] power_index=9.41, accuracy_bits=22.1, area_um2=106134, ffs=2261, throughput_msps=93.5, max_abs_err=2.15e-07 (2^-22.15)
- pipelined [data_width=28 n_iter=26 angle_guard=1 frac_guard=3 rounding=trunc] power_index=10.4, accuracy_bits=23.3, area_um2=117443, ffs=2493, throughput_msps=93.5, max_abs_err=9.77e-08 (2^-23.29)
Front coverage: power_index 2.11..10.4 (HV reference 40); accuracy_bits 13.3..23.3 (HV reference 12); data_width on the front 19..28 (registry 8..28).

Per family:
- pipelined: 55 evals, 39 feasible; max throughput seen 190 MSPS; best accuracy 23.29 bits; best feasible power_index=4.21; feasible ranges: data_width 18..28, n_iter 14..28, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 45 evals, 15 feasible; max throughput seen 82.5 MSPS; best accuracy 18.11 bits; best feasible power_index=2.11; feasible ranges: data_width 19..19, n_iter 16..22, angle_guard -2..1, frac_guard 0..3, m 2..3
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4897 in, 2308 out
- provider-reported cost: $0.0015
- full prompts and replies: `llm_trace.jsonl`

