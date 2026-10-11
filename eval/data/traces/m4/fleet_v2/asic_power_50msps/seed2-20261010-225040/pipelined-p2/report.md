# DSE run: asic_power_50msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
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
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=3` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 27502 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 7327 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 335 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 129 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.74 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.0002 (2^-12.28) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 13.1 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.41e-05 (2^-14.17) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.55 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (9 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=round,m=3` | 27502 | 335 | 54.3 | 7 | 1.74 | 0.0002 (2^-12.28) | 12.28 |
| 1 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=3` | 27943 | 340 | 51.9 | 7 | 1.77 | 0.000175 (2^-12.48) | 12.48 |
| 2 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round,m=3` | 29502 | 340 | 51.9 | 7 | 1.81 | 0.000119 (2^-13.04) | 13.04 |
| 3 | `pipelined_m:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=round,m=2` | 35546 | 539 | 75.4 | 10 | 2.54 | 0.000101 (2^-13.27) | 13.27 |
| 4 | `pipelined_m:data_width=19,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=2` | 37770 | 572 | 69.4 | 10 | 2.7 | 7.74e-05 (2^-13.66) | 13.66 |
| 5 | `pipelined_m:data_width=18,n_iter=23,angle_guard=1,frac_guard=1,rounding=round,m=3` | 48425 | 539 | 51.9 | 10 | 2.92 | 6.95e-05 (2^-13.81) | 13.81 |
| 6 | `pipelined_m:data_width=24,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=2` | 43938 | 684 | 57.9 | 10 | 3.2 | 6.17e-05 (2^-13.98) | 13.98 |
| 7 | `pipelined_m:data_width=25,n_iter=15,angle_guard=2,frac_guard=0,rounding=round,m=2` | 45579 | 710 | 56.1 | 10 | 3.32 | 6.12e-05 (2^-14.00) | 14.00 |
| 8 | `pipelined_m:data_width=26,n_iter=20,angle_guard=-1,frac_guard=4,rounding=trunc,m=2` | 65349 | 948 | 51.2 | 12 | 4.56 | 2.46e-06 (2^-18.63) | 18.63 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *iterative and unrolled_k are infeasible for 50 MSPS, so the entire front lives in pipelined/pipelined_m. pipelined_m is the current power leader (2.07 vs 3.59), so I weight it more heavily and concentrate both families on the narrow W=14..18, N=10..14, round-only box that the feasible points already occupy, to map the full power-vs-accuracy trade-off curve and drive the power floor down.*)
- `pipelined` (40 evals): data_width=14..18, n_iter=10..14, angle_guard=0..2, frac_guard=0..1, rounding=round. *Why:* pipelined is the only family with a strong feasible front (best power 3.59); refine the low-power corner and the accuracy trade-off curve within the constraint envelope.
- `pipelined_m` (60 evals): data_width=14..18, n_iter=10..14, angle_guard=0..2, frac_guard=0..1, rounding=round, m=2..4. *Why:* pipelined_m already beats pipelined on power (best 2.07); focus on the m=2..4 register-sparsity sweet spot to push the power floor lower while keeping 50 MSPS and the 2^-12 error bound.

**Result (code):** 100 evaluations this round, 100 total; 27 feasible; hypervolume 25.94 (n/a).

**LLM decision:** `refine` — The current front is dominated by pipelined_m designs with m=3, which offer the best power efficiency (1.74-1.85) while meeting the 50 MSPS throughput constraint. The full pipelined family is significantly more power-hungry (3.72) and thus less relevant for the 'min power_index' objective, although it provides higher throughput. The accuracy constraint (max_abs_err <= 2^-12) is the binding constraint, with the best feasible designs hovering around 12.3-12.6 bits. The search has converged on data_width=18 and n_iter=14. To improve hypervolume, we should focus the budget on exploring the trade-off between power and accuracy within the pipelined_m family more densely, specifically looking at whether slightly higher n_iter or different guard bits can push accuracy higher without excessive power cost, or if m=2 offers a better power/throughput balance for higher accuracy points. We will narrow the ranges to focus on the promising pipelined_m region.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 25.94 (gain this round: n/a (first round)).
Feasible designs: 27 of 100 evaluations (11 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 29% violate; best seen 171
- max_abs_err <= 0.000244141: 64% violate; best seen 0.000152 (2^-12.68)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=3] power_index=1.74, accuracy_bits=12.3, area_um2=27502, ffs=335, throughput_msps=54.3, max_abs_err=0.0002 (2^-12.28)
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=1.77, accuracy_bits=12.5, area_um2=27943, ffs=340, throughput_msps=51.9, max_abs_err=0.000175 (2^-12.48)
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=3] power_index=1.85, accuracy_bits=12.6, area_um2=29746, ffs=350, throughput_msps=51.9, max_abs_err=0.00016 (2^-12.61)
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] power_index=3.72, accuracy_bits=12.7, area_um2=42125, ffs=893, throughput_msps=132, max_abs_err=0.000152 (2^-12.68)
Front coverage: power_index 1.74..3.72 (HV reference 40); accuracy_bits 12.3..12.7 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- pipelined: 40 evals, 17 feasible; max throughput seen 171 MSPS; best accuracy 12.68 bits; best feasible power_index=3.53; feasible ranges: data_width 18..18, n_iter 14..14, angle_guard 0..2, frac_guard 0..1
- pipelined_m: 60 evals, 10 feasible; max throughput seen 91.1 MSPS; best accuracy 12.68 bits; best feasible power_index=1.74; feasible ranges: data_width 17..18, n_iter 14..14, angle_guard 0..2, frac_guard 0..1, m 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate the remaining budget on the pipelined_m family which has demonstrated the best power efficiency. The previous round showed that data_width=18 and n_iter=14 are the sweet spots for meeting the accuracy constraint with low power. By slightly widening the search space for n_iter (up to 16) and data_width (up to 20), we can explore if there are designs with higher accuracy bits that still maintain low power indices. Including m=2 and m=4 allows us to verify if m=3 is indeed the optimal pipeline depth for this specific power/throughput/accuracy trade-off.*)
- `pipelined_m` (20 evals): data_width=18..20, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* Focus on the most power-efficient family that meets throughput. Expand n_iter and data_width slightly to see if higher accuracy is achievable within the power budget. Include m=2 and m=4 to check if different pipeline depths offer better power/accuracy trade-offs.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 20 evaluations this round, 120 total; 35 feasible; hypervolume 62.38 (+140.5%).

**LLM decision:** `stop` — The Pareto front is well-established and feasible. We have identified a clear trade-off curve between power_index (1.74 to 2.7) and accuracy_bits (12.3 to 13.7). The lowest power design (pipelined_m, m=3, W=18, N=14) meets the throughput constraint (54.3 MSPS >= 50) and the accuracy constraint (12.28 bits > 12 bits). Since this is the final round, we stop and select the design with the minimum power_index from the front, which is the pipelined_m design with power_index=1.74.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 62.38 (gain this round: +140.5%).
Feasible designs: 35 of 120 evaluations (15 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 34% violate; best seen 171
- max_abs_err <= 0.000244141: 53% violate; best seen 5.03e-05 (2^-14.28)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=3] power_index=1.74, accuracy_bits=12.3, area_um2=27502, ffs=335, throughput_msps=54.3, max_abs_err=0.0002 (2^-12.28)
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=1.77, accuracy_bits=12.5, area_um2=27943, ffs=340, throughput_msps=51.9, max_abs_err=0.000175 (2^-12.48)
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=3] power_index=1.85, accuracy_bits=12.6, area_um2=29746, ffs=350, throughput_msps=51.9, max_abs_err=0.00016 (2^-12.61)
- pipelined_m [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.31, accuracy_bits=12.7, area_um2=33024, ffs=483, throughput_msps=72.3, max_abs_err=0.000152 (2^-12.68)
- pipelined_m [data_width=19 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.7, accuracy_bits=13.7, area_um2=37770, ffs=572, throughput_msps=69.4, max_abs_err=7.74e-05 (2^-13.66)
Front coverage: power_index 1.74..2.7 (HV reference 40); accuracy_bits 12.3..13.7 (HV reference 12); data_width on the front 18..19 (registry 8..28).

Per family:
- pipelined: 40 evals, 17 feasible; max throughput seen 171 MSPS; best accuracy 12.68 bits; best feasible power_index=3.53; feasible ranges: data_width 18..18, n_iter 14..14, angle_guard 0..2, frac_guard 0..1
- pipelined_m: 80 evals, 18 feasible; max throughput seen 91.1 MSPS; best accuracy 14.28 bits; best feasible power_index=1.74; feasible ranges: data_width 17..19, n_iter 14..15, angle_guard 0..2, frac_guard 0..1, m 2..3
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (80 evals): data_width=17..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (5 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 62 feasible; hypervolume 239.6 (+284.1%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and feasible. We have identified a clear trade-off curve between power_index (1.74 to 2.7) and accuracy_bits (12.3 to 13.7). The lowest power design (pipelined_m, m=3, W=18, N=14) meets the throughput constraint (54.3 MSPS >= 50) and the accuracy constraint (12.28 bits > 12 bits). Since this is the final round, we stop and select the design with the minimum power_index from the front, which is the pipelined_m design with power_index=1.74.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 239.6 (gain this round: +284.1%).
Feasible designs: 62 of 200 evaluations (28 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 46% violate; best seen 171
- max_abs_err <= 0.000244141: 33% violate; best seen 8.36e-08 (2^-23.51)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round m=3] power_index=1.74, accuracy_bits=12.3, area_um2=27502, ffs=335, throughput_msps=54.3, max_abs_err=0.0002 (2^-12.28)
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=1.77, accuracy_bits=12.5, area_um2=27943, ffs=340, throughput_msps=51.9, max_abs_err=0.000175 (2^-12.48)
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=1.81, accuracy_bits=13, area_um2=29502, ffs=340, throughput_msps=51.9, max_abs_err=0.000119 (2^-13.04)
- pipelined_m [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round m=2] power_index=2.54, accuracy_bits=13.3, area_um2=35546, ffs=539, throughput_msps=75.4, max_abs_err=0.000101 (2^-13.27)
- pipelined_m [data_width=19 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.7, accuracy_bits=13.7, area_um2=37770, ffs=572, throughput_msps=69.4, max_abs_err=7.74e-05 (2^-13.66)
- pipelined_m [data_width=18 n_iter=23 angle_guard=1 frac_guard=1 rounding=round m=3] power_index=2.92, accuracy_bits=13.8, area_um2=48425, ffs=539, throughput_msps=51.9, max_abs_err=6.95e-05 (2^-13.81)
- pipelined_m [data_width=24 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=2] power_index=3.2, accuracy_bits=14, area_um2=43938, ffs=684, throughput_msps=57.9, max_abs_err=6.17e-05 (2^-13.98)
- pipelined_m [data_width=25 n_iter=15 angle_guard=2 frac_guard=0 rounding=round m=2] power_index=3.32, accuracy_bits=14, area_um2=45579, ffs=710, throughput_msps=56.1, max_abs_err=6.12e-05 (2^-14.00)
- pipelined_m [data_width=26 n_iter=20 angle_guard=-1 frac_guard=4 rounding=trunc m=2] power_index=4.56, accuracy_bits=18.6, area_um2=65349, ffs=948, throughput_msps=51.2, max_abs_err=2.46e-06 (2^-18.63)
Front coverage: power_index 1.74..4.56 (HV reference 40); accuracy_bits 12.3..18.6 (HV reference 12); data_width on the front 18..26 (registry 8..28).

Per family:
- pipelined: 40 evals, 17 feasible; max throughput seen 171 MSPS; best accuracy 12.68 bits; best feasible power_index=3.53; feasible ranges: data_width 18..18, n_iter 14..14, angle_guard 0..2, frac_guard 0..1
- pipelined_m: 160 evals, 45 feasible; max throughput seen 91.1 MSPS; best accuracy 23.51 bits; best feasible power_index=1.74; feasible ranges: data_width 17..26, n_iter 14..30, angle_guard -1..2, frac_guard 0..4, m 2..3
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 7299 in, 1670 out
- provider-reported cost: $0.0040
- full prompts and replies: `llm_trace.jsonl`

