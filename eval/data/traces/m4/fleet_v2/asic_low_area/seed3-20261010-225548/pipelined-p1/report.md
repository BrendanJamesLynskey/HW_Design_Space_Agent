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
`pipelined_m:data_width=14,n_iter=13,angle_guard=1,frac_guard=2,rounding=round,m=8` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 20020 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 5334 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 132 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 23.6 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 23.6 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 170 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.0191 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000803 (2^-10.28) | exact: bit-accurate model, exhaustive (16384 angles) |
| max_abs_err_lsb | 3.29 | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err | 0.000213 (2^-12.20) | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err_lsb | 0.871 | exact: bit-accurate model, exhaustive (16384 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (16384 angles) |

## Pareto front (6 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=14,n_iter=13,angle_guard=1,frac_guard=2,rounding=round,m=8` | 20020 | 132 | 23.6 | 4 | 0.0191 | 0.000803 (2^-10.28) | 10.28 |
| 1 | `pipelined_m:data_width=16,n_iter=13,angle_guard=1,frac_guard=2,rounding=round,m=8` | 22311 | 147 | 21.3 | 4 | 0.0213 | 0.000358 (2^-11.45) | 11.45 |
| 2 | `pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=3,rounding=round,m=7` | 31431 | 229 | 21.2 | 5 | 0.0313 | 0.000105 (2^-13.22) | 13.22 |
| 3 | `pipelined_m:data_width=24,n_iter=16,angle_guard=2,frac_guard=3,rounding=round,m=7` | 40976 | 300 | 16.9 | 5 | 0.0408 | 3.07e-05 (2^-14.99) | 14.99 |
| 4 | `pipelined_m:data_width=28,n_iter=22,angle_guard=1,frac_guard=2,rounding=trunc,m=8` | 58528 | 334 | 13.4 | 5 | 0.0531 | 5.33e-07 (2^-20.84) | 20.84 |
| 5 | `pipelined_m:data_width=28,n_iter=30,angle_guard=0,frac_guard=3,rounding=trunc,m=7` | 82946 | 526 | 14.9 | 7 | 0.0781 | 1.33e-07 (2^-22.84) | 22.84 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *No results yet, so I open the search on the two throughput-friendly families I own. The error constraint (<=2^-10) and the 1 MSPS throughput constraint both push toward moderate data_width and n_iter, while area minimization pulls toward the low end; I bracket data_width 12-16 and n_iter 10-16 to cover the feasible region where accuracy_bits can exceed the 10-bit reference and Fmax can sustain 1 MSPS. I fix rounding to round since it strictly improves accuracy at negligible area cost, and keep angle/frac guards small to hold area down. I split budget 60/40 between pipelined (baseline, best Fmax) and pipelined_m (fewer registers, lower area) to map the area/accuracy trade-off across both.*)
- `pipelined` (36 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* Full pipeline gives 1 result/cycle so throughput scales with Fmax; area is the objective, so I focus on the smallest widths that clear the 2^-10 error bound and the Fmax needed for >=1 MSPS, letting the optimizer trade area vs accuracy_bits.
- `pipelined_m` (24 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..8. *Why:* Registering every m stages cuts flip-flops and area versus the full pipeline while keeping 1 result/cycle, so it can dominate on area; I search m to find the area/latency sweet spot that still meets throughput and error.

**Result (code):** 60 evaluations this round, 60 total; 39 feasible; hypervolume 2.828e+04 (n/a).

**LLM decision:** `stop` — The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 20020 um^2) comfortably meets the throughput constraint (23.6 MSPS >= 1 MSPS) and the accuracy constraint (10.3 bits > 10 bits, max_abs_err 0.000803 <= 0.000977). The front extends to higher accuracy (12.5 bits) at the cost of area, covering the relevant trade-off space. Since this is the final round, we stop and select the minimum area design from the front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 2.828e+04 (gain this round: n/a (first round)).
Feasible designs: 39 of 60 evaluations (30 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 35% violate; best seen 0.000177 (2^-12.47)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=14 n_iter=13 angle_guard=1 frac_guard=2 rounding=round m=8] area_um2=20020, accuracy_bits=10.3, ffs=132, throughput_msps=23.6, max_abs_err=0.000803 (2^-10.28), power_index=0.0191
- pipelined_m [data_width=16 n_iter=13 angle_guard=1 frac_guard=2 rounding=round m=8] area_um2=22311, accuracy_bits=11.4, ffs=147, throughput_msps=21.3, max_abs_err=0.000358 (2^-11.45), power_index=0.0213
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=36147, accuracy_bits=11.7, ffs=785, throughput_msps=143, max_abs_err=0.000294 (2^-11.73), power_index=0.0649
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=38197, accuracy_bits=12.2, ffs=810, throughput_msps=143, max_abs_err=0.000209 (2^-12.22), power_index=0.0675
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=39385, accuracy_bits=12.3, ffs=834, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=0.0695
- pipelined [data_width=16 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=43736, accuracy_bits=12.5, ffs=926, throughput_msps=143, max_abs_err=0.000177 (2^-12.47), power_index=0.0772
Front coverage: area_um2 20020..43736 (HV reference 40000); accuracy_bits 10.3..12.5 (HV reference 10); data_width on the front 14..16 (registry 8..28).

Per family:
- pipelined: 36 evals, 26 feasible; max throughput seen 171 MSPS; best accuracy 12.47 bits; best feasible area_um2=31701; feasible ranges: data_width 14..16, n_iter 13..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 24 evals, 13 feasible; max throughput seen 102 MSPS; best accuracy 11.45 bits; best feasible area_um2=20020; feasible ranges: data_width 13..16, n_iter 12..16, angle_guard 0..2, frac_guard 0..2, m 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (14 evals): data_width=13..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (2 front designs; box front_anchored)
- `pipelined` (26 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (4 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 75 feasible; hypervolume 4.147e+04 (+46.7%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and feasible. The minimum area design (pipelined_m, 20020 um^2) comfortably meets the throughput constraint (23.6 MSPS >= 1 MSPS) and the accuracy constraint (10.3 bits > 10 bits, max_abs_err 0.000803 <= 0.000977). The front extends to higher accuracy (12.5 bits) at the cost of area, covering the relevant trade-off space. Since this is the final round, we stop and select the minimum area design from the front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 4.147e+04 (gain this round: +46.7%).
Feasible designs: 75 of 100 evaluations (62 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 25% violate; best seen 1.33e-07 (2^-22.84)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=14 n_iter=13 angle_guard=1 frac_guard=2 rounding=round m=8] area_um2=20020, accuracy_bits=10.3, ffs=132, throughput_msps=23.6, max_abs_err=0.000803 (2^-10.28), power_index=0.0191
- pipelined_m [data_width=16 n_iter=13 angle_guard=1 frac_guard=2 rounding=round m=8] area_um2=22311, accuracy_bits=11.4, ffs=147, throughput_msps=21.3, max_abs_err=0.000358 (2^-11.45), power_index=0.0213
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=3 rounding=round m=7] area_um2=31431, accuracy_bits=13.2, ffs=229, throughput_msps=21.2, max_abs_err=0.000105 (2^-13.22), power_index=0.0313
- pipelined_m [data_width=24 n_iter=16 angle_guard=2 frac_guard=3 rounding=round m=7] area_um2=40976, accuracy_bits=15, ffs=300, throughput_msps=16.9, max_abs_err=3.07e-05 (2^-14.99), power_index=0.0408
- pipelined_m [data_width=28 n_iter=22 angle_guard=1 frac_guard=2 rounding=trunc m=8] area_um2=58528, accuracy_bits=20.8, ffs=334, throughput_msps=13.4, max_abs_err=5.33e-07 (2^-20.84), power_index=0.0531
- pipelined_m [data_width=28 n_iter=30 angle_guard=0 frac_guard=3 rounding=trunc m=7] area_um2=82946, accuracy_bits=22.8, ffs=526, throughput_msps=14.9, max_abs_err=1.33e-07 (2^-22.84), power_index=0.0781
Front coverage: area_um2 20020..82946 (HV reference 40000); accuracy_bits 10.3..22.8 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- pipelined: 62 evals, 50 feasible; max throughput seen 171 MSPS; best accuracy 17.68 bits; best feasible area_um2=31701; feasible ranges: data_width 14..23, n_iter 13..23, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 38 evals, 25 feasible; max throughput seen 102 MSPS; best accuracy 22.84 bits; best feasible area_um2=20020; feasible ranges: data_width 13..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..3, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4761 in, 836 out
- provider-reported cost: $0.0023
- full prompts and replies: `llm_trace.jsonl`

