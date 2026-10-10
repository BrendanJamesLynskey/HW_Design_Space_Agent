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
`iterative:data_width=15,n_iter=12,angle_guard=1,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 6860 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1828 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 100 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 142 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 9.43 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 15 | exact: schedule |
| latency_ns | 106 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.144 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000917 (2^-10.09) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 7.51 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000249 (2^-11.97) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 2.04 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.1 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (20 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=12,angle_guard=1,frac_guard=0,rounding=round` | 6860 | 100 | 9.4 | 15 | 0.144 | 0.000917 (2^-10.09) | 10.09 |
| 1 | `iterative:data_width=15,n_iter=13,angle_guard=0,frac_guard=0,rounding=round` | 6870 | 98 | 9.2 | 16 | 0.152 | 0.000879 (2^-10.15) | 10.15 |
| 2 | `iterative:data_width=15,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` | 6930 | 98 | 8.7 | 17 | 0.162 | 0.00081 (2^-10.27) | 10.27 |
| 3 | `iterative:data_width=17,n_iter=13,angle_guard=2,frac_guard=0,rounding=trunc` | 7610 | 112 | 7.9 | 16 | 0.171 | 0.000429 (2^-11.19) | 11.19 |
| 4 | `iterative:data_width=18,n_iter=13,angle_guard=0,frac_guard=0,rounding=round` | 8008 | 115 | 8.2 | 16 | 0.178 | 0.000316 (2^-11.63) | 11.63 |
| 5 | `iterative:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=trunc` | 8074 | 117 | 7.2 | 17 | 0.192 | 0.00024 (2^-12.03) | 12.03 |
| 6 | `iterative:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 8168 | 116 | 7.4 | 17 | 0.191 | 0.000175 (2^-12.48) | 12.48 |
| 7 | `iterative:data_width=18,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc` | 8359 | 119 | 7.2 | 17 | 0.196 | 0.000166 (2^-12.55) | 12.55 |
| 8 | `iterative:data_width=17,n_iter=17,angle_guard=3,frac_guard=2,rounding=trunc` | 8597 | 118 | 6.1 | 20 | 0.233 | 9.91e-05 (2^-13.30) | 13.30 |
| 9 | `iterative:data_width=21,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc` | 9231 | 131 | 6.5 | 18 | 0.229 | 7.62e-05 (2^-13.68) | 13.68 |
| 10 | `iterative:data_width=21,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 9401 | 131 | 6.5 | 18 | 0.231 | 6.94e-05 (2^-13.81) | 13.81 |
| 11 | `iterative:data_width=20,n_iter=16,angle_guard=-1,frac_guard=2,rounding=trunc` | 9467 | 129 | 6.0 | 19 | 0.242 | 6.6e-05 (2^-13.89) | 13.89 |
| 12 | `iterative:data_width=17,n_iter=21,angle_guard=3,frac_guard=3,rounding=round` | 10744 | 120 | 5.1 | 24 | 0.313 | 4.73e-05 (2^-14.37) | 14.37 |
| 13 | `iterative:data_width=21,n_iter=23,angle_guard=3,frac_guard=3,rounding=trunc` | 11103 | 142 | 4.1 | 26 | 0.376 | 4.3e-06 (2^-17.83) | 17.83 |
| 14 | `iterative:data_width=26,n_iter=21,angle_guard=-2,frac_guard=0,rounding=round` | 12193 | 158 | 4.2 | 24 | 0.383 | 2.38e-06 (2^-18.68) | 18.68 |
| 15 | `iterative:data_width=27,n_iter=23,angle_guard=-1,frac_guard=2,rounding=trunc` | 13460 | 169 | 3.6 | 26 | 0.45 | 7.61e-07 (2^-20.33) | 20.33 |
| 16 | `iterative:data_width=27,n_iter=23,angle_guard=3,frac_guard=2,rounding=trunc` | 13713 | 173 | 3.5 | 26 | 0.46 | 3.16e-07 (2^-21.59) | 21.59 |
| 17 | `iterative:data_width=27,n_iter=27,angle_guard=0,frac_guard=2,rounding=trunc` | 13839 | 170 | 3.1 | 30 | 0.527 | 2.6e-07 (2^-21.88) | 21.88 |
| 18 | `iterative:data_width=27,n_iter=25,angle_guard=3,frac_guard=3,rounding=trunc` | 14313 | 175 | 3.2 | 28 | 0.509 | 1.19e-07 (2^-23.01) | 23.01 |
| 19 | `iterative:data_width=27,n_iter=30,angle_guard=3,frac_guard=3,rounding=round` | 17213 | 175 | 2.7 | 33 | 0.656 | 5.3e-08 (2^-24.17) | 24.17 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *No fleet facts yet, so I seed both of my assigned families. The spec is area-dominated with a hard throughput floor (>=1 MSPS) and a hard accuracy floor (max_abs_err <= 2^-10). Accuracy is width/iteration driven and identical across families, so I pin a tight accuracy box (W 12-18, N 10-14, small guards, both roundings) that comfortably clears 2^-10 without wasting budget on over-accurate corners. The real trade-off is area vs throughput: iterative is the area floor but does 1 result per N+3 cycles, so it needs a high Fmax to hit 1 MSPS; unrolled_k trades duplicated-datapath area for kx throughput. I give iterative the larger share because it is the most likely area winner, and unrolled_k the remainder to map the throughput-vs-area knee in case iterative's Fmax falls short of the throughput constraint. Both families share the same accuracy ranges so the merged front is directly comparable on area/accuracy.*)
- `iterative` (30 evals): data_width=12..18, n_iter=10..14, angle_guard=0..2, frac_guard=0..1, rounding=trunc|round. *Why:* iterative is the shared-datapath family: one adder/shift stage reused, so it is the area floor for any given accuracy. It is the only family that can plausibly beat the area objective while still hitting >=1 MSPS at a modest Fmax. Accuracy needs max_abs_err <= 2^-10, which is met by W~14-16 with N~12-14; I keep W in 12-18 and N in 10-14 to let the optimizer find the cheapest (W,N) that clears the error bar, with small guards to avoid over-designing the angle/frac paths.
- `unrolled_k` (30 evals): data_width=12..18, n_iter=10..14, angle_guard=0..2, frac_guard=0..1, rounding=trunc|round, k=2..4. *Why:* unrolled_k duplicates the datapath k times to raise throughput per cycle. It is the fallback if iterative's Fmax is too low to reach 1 MSPS (iterative does 1 result per N+3 cycles, so it needs Fmax >= (N+3) MHz). k=2..4 gives 2-4x throughput at the cost of kx datapath area; I keep k small (2-4) because area is the primary objective, so only the minimum k that clears the throughput constraint should win. Same accuracy ranges as iterative since the bits are identical.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 60 evaluations this round, 60 total; 36 feasible; hypervolume 8.221e+04 (n/a).

**LLM decision:** `stop` — The Pareto front is well-established and feasible. The minimum area design (iterative, area_um2=6860, accuracy_bits=10.1) comfortably meets the constraints: throughput 9.43 MSPS >= 1 MSPS and max_abs_err 0.000917 <= 0.000976562. The front spans a reasonable range of accuracy (10.1 to 12.6 bits) and area (6860 to 8359 um^2). Since this is the final round, we stop and select the minimum area design from the front as per the selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 8.221e+04 (gain this round: n/a (first round)).
Feasible designs: 36 of 60 evaluations (24 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 12.4
- max_abs_err <= 0.000976562: 40% violate; best seen 0.000166 (2^-12.55)

Pareto front (feasible, 8 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=0 rounding=round] area_um2=6860, accuracy_bits=10.1, ffs=100, throughput_msps=9.43, max_abs_err=0.000917 (2^-10.09), power_index=0.144
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] area_um2=6870, accuracy_bits=10.2, ffs=98, throughput_msps=9.22, max_abs_err=0.000879 (2^-10.15), power_index=0.152
- iterative [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] area_um2=6930, accuracy_bits=10.3, ffs=98, throughput_msps=8.68, max_abs_err=0.00081 (2^-10.27), power_index=0.162
- iterative [data_width=17 n_iter=13 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=7610, accuracy_bits=11.2, ffs=112, throughput_msps=7.89, max_abs_err=0.000429 (2^-11.19), power_index=0.171
- iterative [data_width=18 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] area_um2=8008, accuracy_bits=11.6, ffs=115, throughput_msps=8.18, max_abs_err=0.000316 (2^-11.63), power_index=0.178
- iterative [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=8074, accuracy_bits=12, ffs=117, throughput_msps=7.17, max_abs_err=0.00024 (2^-12.03), power_index=0.192
- iterative [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=8168, accuracy_bits=12.5, ffs=116, throughput_msps=7.42, max_abs_err=0.000175 (2^-12.48), power_index=0.191
- iterative [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=8359, accuracy_bits=12.6, ffs=119, throughput_msps=7.17, max_abs_err=0.000166 (2^-12.55), power_index=0.196
Front coverage: area_um2 6860..8359 (HV reference 40000); accuracy_bits 10.1..12.6 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 30 evals, 17 feasible; max throughput seen 12.4 MSPS; best accuracy 12.55 bits; best feasible area_um2=6860; feasible ranges: data_width 15..18, n_iter 12..14, angle_guard 0..2, frac_guard 0..1
- unrolled_k: 30 evals, 19 feasible; max throughput seen 10.7 MSPS; best accuracy 10.87 bits; best feasible area_um2=11761; feasible ranges: data_width 14..17, n_iter 12..14, angle_guard 0..2, frac_guard 0..1, k 3..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (40 evals): data_width=14..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (8 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 70 feasible; hypervolume 4.014e+05 (+388.2%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and feasible. The minimum area design (iterative, area_um2=6860, accuracy_bits=10.1) comfortably meets the constraints: throughput 9.43 MSPS >= 1 MSPS and max_abs_err 0.000917 <= 0.000976562. The front spans a reasonable range of accuracy (10.1 to 12.6 bits) and area (6860 to 8359 um^2). Since this is the final round, we stop and select the minimum area design from the front as per the selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 4.014e+05 (gain this round: +388.2%).
Feasible designs: 70 of 100 evaluations (54 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 12.4
- max_abs_err <= 0.000976562: 30% violate; best seen 5.3e-08 (2^-24.17)

Pareto front (feasible, 20 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=0 rounding=round] area_um2=6860, accuracy_bits=10.1, ffs=100, throughput_msps=9.43, max_abs_err=0.000917 (2^-10.09), power_index=0.144
- iterative [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] area_um2=6930, accuracy_bits=10.3, ffs=98, throughput_msps=8.68, max_abs_err=0.00081 (2^-10.27), power_index=0.162
- iterative [data_width=18 n_iter=13 angle_guard=0 frac_guard=0 rounding=round] area_um2=8008, accuracy_bits=11.6, ffs=115, throughput_msps=8.18, max_abs_err=0.000316 (2^-11.63), power_index=0.178
- iterative [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=8168, accuracy_bits=12.5, ffs=116, throughput_msps=7.42, max_abs_err=0.000175 (2^-12.48), power_index=0.191
- iterative [data_width=17 n_iter=17 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=8597, accuracy_bits=13.3, ffs=118, throughput_msps=6.09, max_abs_err=9.91e-05 (2^-13.30), power_index=0.233
- iterative [data_width=20 n_iter=16 angle_guard=-1 frac_guard=2 rounding=trunc] area_um2=9467, accuracy_bits=13.9, ffs=129, throughput_msps=5.99, max_abs_err=6.6e-05 (2^-13.89), power_index=0.242
- iterative [data_width=21 n_iter=23 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=11103, accuracy_bits=17.8, ffs=142, throughput_msps=4.11, max_abs_err=4.3e-06 (2^-17.83), power_index=0.376
- iterative [data_width=27 n_iter=23 angle_guard=-1 frac_guard=2 rounding=trunc] area_um2=13460, accuracy_bits=20.3, ffs=169, throughput_msps=3.57, max_abs_err=7.61e-07 (2^-20.33), power_index=0.45
- iterative [data_width=27 n_iter=27 angle_guard=0 frac_guard=2 rounding=trunc] area_um2=13839, accuracy_bits=21.9, ffs=170, throughput_msps=3.09, max_abs_err=2.6e-07 (2^-21.88), power_index=0.527
- iterative [data_width=27 n_iter=30 angle_guard=3 frac_guard=3 rounding=round] area_um2=17213, accuracy_bits=24.2, ffs=175, throughput_msps=2.74, max_abs_err=5.3e-08 (2^-24.17), power_index=0.656
Front coverage: area_um2 6860..17213 (HV reference 40000); accuracy_bits 10.1..24.2 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 70 evals, 51 feasible; max throughput seen 12.4 MSPS; best accuracy 24.17 bits; best feasible area_um2=6860; feasible ranges: data_width 15..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..3
- unrolled_k: 30 evals, 19 feasible; max throughput seen 10.7 MSPS; best accuracy 10.87 bits; best feasible area_um2=11761; feasible ranges: data_width 14..17, n_iter 12..14, angle_guard 0..2, frac_guard 0..1, k 3..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4422 in, 1061 out
- provider-reported cost: $0.0032
- full prompts and replies: `llm_trace.jsonl`

