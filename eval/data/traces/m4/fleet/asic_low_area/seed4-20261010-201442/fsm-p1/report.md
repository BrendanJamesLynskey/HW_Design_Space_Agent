# DSE run: asic_low_area

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`iterative:data_width=16,n_iter=20,angle_guard=2,frac_guard=0,rounding=trunc` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 7476 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1992 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 107 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 131 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 5.69 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 23 | exact: schedule |
| latency_ns | 176 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.238 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000708 (2^-10.46) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 11.6 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000169 (2^-12.53) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 2.77 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.5 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (22 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=16,n_iter=20,angle_guard=2,frac_guard=0,rounding=trunc` | 7476 | 107 | 5.7 | 23 | 0.238 | 0.000708 (2^-10.46) | 10.46 |
| 1 | `iterative:data_width=17,n_iter=14,angle_guard=-2,frac_guard=1,rounding=trunc` | 7714 | 109 | 7.7 | 17 | 0.181 | 0.00065 (2^-10.59) | 10.59 |
| 2 | `iterative:data_width=18,n_iter=16,angle_guard=-2,frac_guard=1,rounding=trunc` | 8263 | 115 | 6.6 | 19 | 0.214 | 0.000323 (2^-11.60) | 11.60 |
| 3 | `iterative:data_width=17,n_iter=18,angle_guard=1,frac_guard=2,rounding=trunc` | 8519 | 116 | 6.0 | 21 | 0.241 | 0.000137 (2^-12.84) | 12.84 |
| 4 | `iterative:data_width=19,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc` | 8623 | 123 | 6.2 | 19 | 0.226 | 8.56e-05 (2^-13.51) | 13.51 |
| 5 | `iterative:data_width=18,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 8762 | 120 | 6.4 | 19 | 0.225 | 8.08e-05 (2^-13.60) | 13.60 |
| 6 | `iterative:data_width=19,n_iter=20,angle_guard=2,frac_guard=0,rounding=trunc` | 8857 | 124 | 5.1 | 23 | 0.278 | 7.83e-05 (2^-13.64) | 13.64 |
| 7 | `iterative:data_width=18,n_iter=18,angle_guard=1,frac_guard=2,rounding=trunc` | 8959 | 121 | 5.8 | 21 | 0.253 | 6.72e-05 (2^-13.86) | 13.86 |
| 8 | `iterative:data_width=20,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc` | 9039 | 128 | 6.0 | 19 | 0.236 | 5.76e-05 (2^-14.08) | 14.08 |
| 9 | `iterative:data_width=19,n_iter=20,angle_guard=2,frac_guard=0,rounding=round` | 9087 | 124 | 5.1 | 23 | 0.281 | 3.86e-05 (2^-14.66) | 14.66 |
| 10 | `iterative:data_width=19,n_iter=20,angle_guard=3,frac_guard=0,rounding=round` | 9151 | 125 | 5.0 | 23 | 0.284 | 3.74e-05 (2^-14.71) | 14.71 |
| 11 | `iterative:data_width=19,n_iter=20,angle_guard=2,frac_guard=2,rounding=trunc` | 9571 | 128 | 5.1 | 23 | 0.293 | 3.04e-05 (2^-15.00) | 15.00 |
| 12 | `iterative:data_width=20,n_iter=20,angle_guard=1,frac_guard=1,rounding=trunc` | 9615 | 130 | 5.1 | 23 | 0.297 | 2.8e-05 (2^-15.12) | 15.12 |
| 13 | `iterative:data_width=20,n_iter=22,angle_guard=1,frac_guard=2,rounding=trunc` | 10057 | 132 | 4.6 | 25 | 0.332 | 1.79e-05 (2^-15.77) | 15.77 |
| 14 | `iterative:data_width=22,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc` | 10208 | 138 | 4.6 | 25 | 0.342 | 1.39e-05 (2^-16.14) | 16.14 |
| 15 | `iterative:data_width=23,n_iter=27,angle_guard=-1,frac_guard=0,rounding=trunc` | 10706 | 142 | 3.7 | 30 | 0.426 | 9.92e-06 (2^-16.62) | 16.62 |
| 16 | `iterative:data_width=23,n_iter=23,angle_guard=0,frac_guard=0,rounding=trunc` | 10733 | 143 | 4.2 | 26 | 0.372 | 6.55e-06 (2^-17.22) | 17.22 |
| 17 | `iterative:data_width=23,n_iter=25,angle_guard=2,frac_guard=1,rounding=trunc` | 11314 | 148 | 3.7 | 28 | 0.417 | 3.08e-06 (2^-18.31) | 18.31 |
| 18 | `iterative:data_width=23,n_iter=20,angle_guard=2,frac_guard=3,rounding=trunc` | 11786 | 152 | 4.4 | 23 | 0.354 | 2.98e-06 (2^-18.36) | 18.36 |
| 19 | `iterative:data_width=28,n_iter=25,angle_guard=2,frac_guard=0,rounding=trunc` | 13521 | 173 | 3.2 | 28 | 0.492 | 2.16e-07 (2^-22.14) | 22.14 |
| 20 | `iterative:data_width=28,n_iter=25,angle_guard=2,frac_guard=1,rounding=trunc` | 13939 | 175 | 3.2 | 28 | 0.502 | 1.41e-07 (2^-22.76) | 22.76 |
| 21 | `iterative:data_width=28,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc` | 14775 | 179 | 3.1 | 28 | 0.523 | 9.99e-08 (2^-23.26) | 23.26 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=1 MSPS and max_abs_err <= 2^-10 while minimising area. Both allowed families compute identical output bits for the same data_width, n_iter, angle_guard, frac_guard and rounding. However, unrolled_k instantiates k parallel micro-rotation datapaths, so for any given accuracy it has strictly larger area than iterative. Since the throughput constraint is only 1 MSPS, iterative with N up to 22 and typical Fmax easily exceeds this (e.g. Fmax/25 > 1 MHz). Therefore unrolled_k cannot appear on the min-area Pareto front and is not worth budget. We focus 100% of the first-round budget on iterative to map the area-accuracy trade-off. The ranges cover the likely feasible region: data_width >=12 is required because W=11 output quantisation alone can exceed the error bound; n_iter 10..22 covers convergence and truncation-error needs; angle_guard and frac_guard are varied to find the minimal area that still meets accuracy; rounding is included because it can improve accuracy at low area cost.*)
- `iterative` (60 evals): data_width=12..20, n_iter=10..22, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Iterative is the lowest-area family for any given accuracy because it shares a single datapath across all N micro-rotations. The throughput constraint is easily met. The parameter ranges are chosen to explore the low-area corner (small W, small N, small guards) while also covering enough range to map the front up to higher accuracy.

**Result (code):** 60 evaluations this round, 60 total; 42 feasible; hypervolume 1.8e+05 (n/a).

**LLM decision:** `stop` — This is the final round, so only stop/infeasible are available. Infeasible is ruled out: 42 of 60 evaluations are feasible, with 0% violating throughput_msps >= 1 (best seen 12.4 MSPS vs the 1 MSPS floor) and the accuracy constraint met by the whole front (best max_abs_err 1.79e-05 = 2^-15.77, far under the 2^-10 limit). The feasible Pareto front is well-populated (12 designs) and spans area_um2 7714..10057 against the HV reference 40000, and accuracy_bits 10.6..15.8 against the HV reference 10 — i.e. it already covers the useful trade-off region, with the selection rule's pick (min area_um2) being the iterative [data_width=17 n_iter=14 angle_guard=-2 frac_guard=1 rounding=trunc] design at 7714 um^2, 10.6 accuracy bits, 7.7 MSPS, comfortably satisfying both constraints. The only unexplored family (unrolled_k) cannot beat the iterative corner on area for this low-area spec, since it shares the same datapath but adds chained-rotation hardware; the front's area floor is already set by the smallest feasible iterative configuration. No further improvement is expected within the remaining budget, so I stop on the current front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.8e+05 (gain this round: n/a (first round)).
Feasible designs: 42 of 60 evaluations (32 unique).
Families explored so far: iterative. Not yet explored: unrolled_k.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 12.4
- max_abs_err <= 0.000976562: 30% violate; best seen 1.79e-05 (2^-15.77)

Pareto front (feasible, 12 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=17 n_iter=14 angle_guard=-2 frac_guard=1 rounding=trunc] area_um2=7714, accuracy_bits=10.6, ffs=109, throughput_msps=7.7, max_abs_err=0.00065 (2^-10.59), power_index=0.181
- iterative [data_width=18 n_iter=16 angle_guard=-2 frac_guard=1 rounding=trunc] area_um2=8263, accuracy_bits=11.6, ffs=115, throughput_msps=6.64, max_abs_err=0.000323 (2^-11.60), power_index=0.214
- iterative [data_width=17 n_iter=18 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=8519, accuracy_bits=12.8, ffs=116, throughput_msps=6.01, max_abs_err=0.000137 (2^-12.84), power_index=0.241
- iterative [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=8762, accuracy_bits=13.6, ffs=120, throughput_msps=6.41, max_abs_err=8.08e-05 (2^-13.60), power_index=0.225
- iterative [data_width=18 n_iter=18 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=8959, accuracy_bits=13.9, ffs=121, throughput_msps=5.8, max_abs_err=6.72e-05 (2^-13.86), power_index=0.253
- iterative [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=9039, accuracy_bits=14.1, ffs=128, throughput_msps=5.99, max_abs_err=5.76e-05 (2^-14.08), power_index=0.236
- iterative [data_width=19 n_iter=20 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=9151, accuracy_bits=14.3, ffs=125, throughput_msps=5.3, max_abs_err=4.91e-05 (2^-14.31), power_index=0.284
- iterative [data_width=19 n_iter=20 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=9571, accuracy_bits=15, ffs=128, throughput_msps=5.12, max_abs_err=3.04e-05 (2^-15.00), power_index=0.293
- iterative [data_width=20 n_iter=20 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=9615, accuracy_bits=15.1, ffs=130, throughput_msps=5.12, max_abs_err=2.8e-05 (2^-15.12), power_index=0.297
- iterative [data_width=20 n_iter=22 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=10057, accuracy_bits=15.8, ffs=132, throughput_msps=4.56, max_abs_err=1.79e-05 (2^-15.77), power_index=0.332
Front coverage: area_um2 7714..10057 (HV reference 40000); accuracy_bits 10.6..15.8 (HV reference 10); data_width on the front 17..20 (registry 8..28).

Per family:
- iterative: 60 evals, 42 feasible; max throughput seen 12.4 MSPS; best accuracy 15.77 bits; best feasible area_um2=7714; feasible ranges: data_width 14..20, n_iter 12..22, angle_guard -2..2, frac_guard 0..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (40 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (12 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 82 feasible; hypervolume 3.844e+05 (+113.6%).

**No LLM call** (code's front-mapping round): This is the final round, so only stop/infeasible are available. Infeasible is ruled out: 42 of 60 evaluations are feasible, with 0% violating throughput_msps >= 1 (best seen 12.4 MSPS vs the 1 MSPS floor) and the accuracy constraint met by the whole front (best max_abs_err 1.79e-05 = 2^-15.77, far under the 2^-10 limit). The feasible Pareto front is well-populated (12 designs) and spans area_um2 7714..10057 against the HV reference 40000, and accuracy_bits 10.6..15.8 against the HV reference 10 — i.e. it already covers the useful trade-off region, with the selection rule's pick (min area_um2) being the iterative [data_width=17 n_iter=14 angle_guard=-2 frac_guard=1 rounding=trunc] design at 7714 um^2, 10.6 accuracy bits, 7.7 MSPS, comfortably satisfying both constraints. The only unexplored family (unrolled_k) cannot beat the iterative corner on area for this low-area spec, since it shares the same datapath but adds chained-rotation hardware; the front's area floor is already set by the smallest feasible iterative configuration. No further improvement is expected within the remaining budget, so I stop on the current front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 3.844e+05 (gain this round: +113.6%).
Feasible designs: 82 of 100 evaluations (72 unique).
Families explored so far: iterative. Not yet explored: unrolled_k.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 12.4
- max_abs_err <= 0.000976562: 18% violate; best seen 9.99e-08 (2^-23.26)

Pareto front (feasible, 22 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=16 n_iter=20 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=7476, accuracy_bits=10.5, ffs=107, throughput_msps=5.69, max_abs_err=0.000708 (2^-10.46), power_index=0.238
- iterative [data_width=18 n_iter=16 angle_guard=-2 frac_guard=1 rounding=trunc] area_um2=8263, accuracy_bits=11.6, ffs=115, throughput_msps=6.64, max_abs_err=0.000323 (2^-11.60), power_index=0.214
- iterative [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=8762, accuracy_bits=13.6, ffs=120, throughput_msps=6.41, max_abs_err=8.08e-05 (2^-13.60), power_index=0.225
- iterative [data_width=18 n_iter=18 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=8959, accuracy_bits=13.9, ffs=121, throughput_msps=5.8, max_abs_err=6.72e-05 (2^-13.86), power_index=0.253
- iterative [data_width=19 n_iter=20 angle_guard=2 frac_guard=0 rounding=round] area_um2=9087, accuracy_bits=14.7, ffs=124, throughput_msps=5.12, max_abs_err=3.86e-05 (2^-14.66), power_index=0.281
- iterative [data_width=20 n_iter=20 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=9615, accuracy_bits=15.1, ffs=130, throughput_msps=5.12, max_abs_err=2.8e-05 (2^-15.12), power_index=0.297
- iterative [data_width=22 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=10208, accuracy_bits=16.1, ffs=138, throughput_msps=4.56, max_abs_err=1.39e-05 (2^-16.14), power_index=0.342
- iterative [data_width=23 n_iter=23 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=10733, accuracy_bits=17.2, ffs=143, throughput_msps=4.24, max_abs_err=6.55e-06 (2^-17.22), power_index=0.372
- iterative [data_width=28 n_iter=25 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=13521, accuracy_bits=22.1, ffs=173, throughput_msps=3.23, max_abs_err=2.16e-07 (2^-22.14), power_index=0.492
- iterative [data_width=28 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=14775, accuracy_bits=23.3, ffs=179, throughput_msps=3.15, max_abs_err=9.99e-08 (2^-23.26), power_index=0.523
Front coverage: area_um2 7476..14775 (HV reference 40000); accuracy_bits 10.5..23.3 (HV reference 10); data_width on the front 16..28 (registry 8..28).

Per family:
- iterative: 100 evals, 82 feasible; max throughput seen 12.4 MSPS; best accuracy 23.26 bits; best feasible area_um2=7476; feasible ranges: data_width 14..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4343 in, 9629 out
- provider-reported cost: $0.0070
- full prompts and replies: `llm_trace.jsonl`

