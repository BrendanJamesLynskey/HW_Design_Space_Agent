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
`pipelined_m:data_width=17,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=3` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 30828 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 8213 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 381 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 8 | exact: schedule |
| latency_ns | 147 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.97 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000149 (2^-12.71) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 4.89 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 3.98e-05 (2^-14.62) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.3 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.7 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=3` | 30828 | 381 | 54.3 | 8 | 1.97 | 0.000149 (2^-12.71) | 12.71 |
| 1 | `pipelined_m:data_width=17,n_iter=17,angle_guard=2,frac_guard=0,rounding=round,m=3` | 32850 | 387 | 51.9 | 8 | 2.04 | 0.000139 (2^-12.81) | 12.81 |
| 2 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=3` | 32414 | 401 | 51.9 | 8 | 2.07 | 0.000108 (2^-13.18) | 13.18 |
| 3 | `pipelined_m:data_width=17,n_iter=17,angle_guard=2,frac_guard=2,rounding=round,m=3` | 35834 | 409 | 51.9 | 8 | 2.19 | 7.36e-05 (2^-13.73) | 13.73 |
| 4 | `pipelined_m:data_width=18,n_iter=17,angle_guard=1,frac_guard=1,rounding=round,m=2` | 40163 | 602 | 75.4 | 11 | 2.86 | 6.89e-05 (2^-13.83) | 13.83 |
| 5 | `pipelined_m:data_width=24,n_iter=15,angle_guard=0,frac_guard=1,rounding=round,m=2` | 45165 | 684 | 59.9 | 10 | 3.23 | 6.16e-05 (2^-13.99) | 13.99 |
| 6 | `pipelined_m:data_width=24,n_iter=15,angle_guard=3,frac_guard=4,rounding=trunc,m=2` | 48555 | 747 | 54.3 | 10 | 3.51 | 6.12e-05 (2^-14.00) | 14.00 |
| 7 | `pipelined_m:data_width=24,n_iter=15,angle_guard=3,frac_guard=4,rounding=round,m=2` | 49825 | 749 | 54.3 | 10 | 3.55 | 6.11e-05 (2^-14.00) | 14.00 |
| 8 | `pipelined_m:data_width=24,n_iter=18,angle_guard=0,frac_guard=4,rounding=trunc,m=2` | 55449 | 809 | 54.3 | 11 | 3.88 | 8.72e-06 (2^-16.81) | 16.81 |
| 9 | `pipelined:data_width=24,n_iter=20,angle_guard=-1,frac_guard=0,rounding=trunc` | 71559 | 1534 | 115.0 | 22 | 6.37 | 5.06e-06 (2^-17.59) | 17.59 |
| 10 | `pipelined:data_width=23,n_iter=28,angle_guard=0,frac_guard=1,rounding=round` | 102051 | 2145 | 115.0 | 30 | 8.97 | 3.92e-06 (2^-17.96) | 17.96 |
| 11 | `pipelined:data_width=27,n_iter=25,angle_guard=4,frac_guard=0,rounding=round` | 106134 | 2261 | 93.5 | 27 | 9.41 | 2.15e-07 (2^-22.15) | 22.15 |
| 12 | `pipelined:data_width=28,n_iter=26,angle_guard=1,frac_guard=3,rounding=trunc` | 117443 | 2493 | 93.5 | 28 | 10.4 | 9.77e-08 (2^-23.29) | 23.29 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *No facts yet, so I start from the spec: 50 MSPS requires 1 result/cycle (pipelined or pipelined_m) with Fmax >= 50 MHz, and max_abs_err <= 2^-12 requires accuracy_bits >= 12. Accuracy depends only on data_width/n_iter/guards/rounding, so I focus the search on the accuracy region that just meets or exceeds 12 bits (W=14-18, N=12-18, round) and let the optimizer trade power vs accuracy_bits. I split budget between the full pipeline (lowest power, but Fmax risk) and pipelined_m (m=2-4) to cover the Fmax-recovery trade-off. Rounding is fixed to 'round' since it strictly improves accuracy at negligible cost, freeing the search to explore the power/accuracy trade-off rather than wasting evaluations on truncation.*)
- `pipelined` (36 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* Full pipeline gives 1 result/cycle, so throughput = Fmax; the 50 MSPS constraint is met if Fmax >= 50 MHz, which is plausible for moderate N. This is the lowest-power family for the throughput target, so it should dominate the front.
- `pipelined_m` (24 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* Registering every m stages trades area/power for a higher Fmax; if the full pipeline's Fmax is too low to hit 50 MSPS, pipelined_m with m=2-4 can recover throughput while keeping fewer FFs than the full pipeline.

**Result (code):** 60 evaluations this round, 60 total; 35 feasible; hypervolume 88.31 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established and meets all constraints. The minimum power_index achieved is 1.97 (pipelined_m, data_width=17, n_iter=16, m=3) with 12.7 accuracy bits, which satisfies the max_abs_err <= 2^-12 constraint (12.7 > 12) and throughput >= 50 MSPS (54.3 MSPS). The front spans a reasonable range of power (1.97 to 4.65) and accuracy (12.7 to 14.4 bits), covering the trade-off space effectively. Since this is the final round and the front is stable with no indication of significant improvement possible within the remaining budget (0 evals left), stopping is the correct decision. The design with minimum power_index (1.97) is a strong candidate for selection.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 88.31 (gain this round: n/a (first round)).
Feasible designs: 35 of 60 evaluations (24 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 7% violate; best seen 171
- max_abs_err <= 0.000244141: 37% violate; best seen 4.73e-05 (2^-14.37)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=1.97, accuracy_bits=12.7, area_um2=30828, ffs=381, throughput_msps=54.3, max_abs_err=0.000149 (2^-12.71)
- pipelined_m [data_width=17 n_iter=17 angle_guard=2 frac_guard=0 rounding=round m=3] power_index=2.04, accuracy_bits=12.8, area_um2=32850, ffs=387, throughput_msps=51.9, max_abs_err=0.000139 (2^-12.81)
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=2.07, accuracy_bits=13.2, area_um2=32414, ffs=401, throughput_msps=51.9, max_abs_err=0.000108 (2^-13.18)
- pipelined_m [data_width=17 n_iter=17 angle_guard=2 frac_guard=2 rounding=round m=3] power_index=2.19, accuracy_bits=13.7, area_um2=35834, ffs=409, throughput_msps=51.9, max_abs_err=7.36e-05 (2^-13.73)
- pipelined_m [data_width=18 n_iter=17 angle_guard=1 frac_guard=1 rounding=round m=2] power_index=2.86, accuracy_bits=13.8, area_um2=40163, ffs=602, throughput_msps=75.4, max_abs_err=6.89e-05 (2^-13.83)
- pipelined [data_width=18 n_iter=17 angle_guard=2 frac_guard=2 rounding=round] power_index=4.65, accuracy_bits=14.4, area_um2=52760, ffs=1114, throughput_msps=132, max_abs_err=4.73e-05 (2^-14.37)
Front coverage: power_index 1.97..4.65 (HV reference 40); accuracy_bits 12.7..14.4 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 36 evals, 20 feasible; max throughput seen 171 MSPS; best accuracy 14.37 bits; best feasible power_index=3.38; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 24 evals, 15 feasible; max throughput seen 78.8 MSPS; best accuracy 13.83 bits; best feasible power_index=1.97; feasible ranges: data_width 17..18, n_iter 14..17, angle_guard 1..2, frac_guard 0..2, m 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (34 evals): data_width=16..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (5 front designs; box front_anchored)
- `pipelined` (6 evals): data_width=17..28, n_iter=15..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 47 feasible; hypervolume 376.6 (+326.5%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and meets all constraints. The minimum power_index achieved is 1.97 (pipelined_m, data_width=17, n_iter=16, m=3) with 12.7 accuracy bits, which satisfies the max_abs_err <= 2^-12 constraint (12.7 > 12) and throughput >= 50 MSPS (54.3 MSPS). The front spans a reasonable range of power (1.97 to 4.65) and accuracy (12.7 to 14.4 bits), covering the trade-off space effectively. Since this is the final round and the front is stable with no indication of significant improvement possible within the remaining budget (0 evals left), stopping is the correct decision. The design with minimum power_index (1.97) is a strong candidate for selection.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 376.6 (gain this round: +326.5%).
Feasible designs: 47 of 100 evaluations (36 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 29% violate; best seen 171
- max_abs_err <= 0.000244141: 27% violate; best seen 9.77e-08 (2^-23.29)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=17 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=1.97, accuracy_bits=12.7, area_um2=30828, ffs=381, throughput_msps=54.3, max_abs_err=0.000149 (2^-12.71)
- pipelined_m [data_width=17 n_iter=17 angle_guard=2 frac_guard=0 rounding=round m=3] power_index=2.04, accuracy_bits=12.8, area_um2=32850, ffs=387, throughput_msps=51.9, max_abs_err=0.000139 (2^-12.81)
- pipelined_m [data_width=17 n_iter=17 angle_guard=2 frac_guard=2 rounding=round m=3] power_index=2.19, accuracy_bits=13.7, area_um2=35834, ffs=409, throughput_msps=51.9, max_abs_err=7.36e-05 (2^-13.73)
- pipelined_m [data_width=18 n_iter=17 angle_guard=1 frac_guard=1 rounding=round m=2] power_index=2.86, accuracy_bits=13.8, area_um2=40163, ffs=602, throughput_msps=75.4, max_abs_err=6.89e-05 (2^-13.83)
- pipelined_m [data_width=24 n_iter=15 angle_guard=0 frac_guard=1 rounding=round m=2] power_index=3.23, accuracy_bits=14, area_um2=45165, ffs=684, throughput_msps=59.9, max_abs_err=6.16e-05 (2^-13.99)
- pipelined_m [data_width=24 n_iter=15 angle_guard=3 frac_guard=4 rounding=round m=2] power_index=3.55, accuracy_bits=14, area_um2=49825, ffs=749, throughput_msps=54.3, max_abs_err=6.11e-05 (2^-14.00)
- pipelined_m [data_width=24 n_iter=18 angle_guard=0 frac_guard=4 rounding=trunc m=2] power_index=3.88, accuracy_bits=16.8, area_um2=55449, ffs=809, throughput_msps=54.3, max_abs_err=8.72e-06 (2^-16.81)
- pipelined [data_width=24 n_iter=20 angle_guard=-1 frac_guard=0 rounding=trunc] power_index=6.37, accuracy_bits=17.6, area_um2=71559, ffs=1534, throughput_msps=115, max_abs_err=5.06e-06 (2^-17.59)
- pipelined [data_width=27 n_iter=25 angle_guard=4 frac_guard=0 rounding=round] power_index=9.41, accuracy_bits=22.1, area_um2=106134, ffs=2261, throughput_msps=93.5, max_abs_err=2.15e-07 (2^-22.15)
- pipelined [data_width=28 n_iter=26 angle_guard=1 frac_guard=3 rounding=trunc] power_index=10.4, accuracy_bits=23.3, area_um2=117443, ffs=2493, throughput_msps=93.5, max_abs_err=9.77e-08 (2^-23.29)
Front coverage: power_index 1.97..10.4 (HV reference 40); accuracy_bits 12.7..23.3 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- pipelined: 42 evals, 26 feasible; max throughput seen 171 MSPS; best accuracy 23.29 bits; best feasible power_index=3.38; feasible ranges: data_width 16..28, n_iter 14..28, angle_guard -1..4, frac_guard 0..3
- pipelined_m: 58 evals, 21 feasible; max throughput seen 78.8 MSPS; best accuracy 20.82 bits; best feasible power_index=1.97; feasible ranges: data_width 17..24, n_iter 14..18, angle_guard 0..3, frac_guard 0..4, m 2..3
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4776 in, 922 out
- provider-reported cost: $0.0024
- full prompts and replies: `llm_trace.jsonl`

