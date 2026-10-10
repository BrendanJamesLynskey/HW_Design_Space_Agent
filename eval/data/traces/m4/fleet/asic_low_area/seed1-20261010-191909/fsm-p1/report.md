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
`iterative:data_width=15,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 7106 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1893 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 101 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 142 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 7.86 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 127 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.176 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000822 (2^-10.25) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.74 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000203 (2^-12.27) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.66 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.2 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (25 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc` | 7106 | 101 | 7.9 | 18 | 0.176 | 0.000822 (2^-10.25) | 10.25 |
| 1 | `iterative:data_width=15,n_iter=19,angle_guard=3,frac_guard=1,rounding=trunc` | 7432 | 105 | 6.0 | 22 | 0.225 | 0.000653 (2^-10.58) | 10.58 |
| 2 | `iterative:data_width=17,n_iter=22,angle_guard=1,frac_guard=0,rounding=trunc` | 7865 | 112 | 5.2 | 25 | 0.271 | 0.000398 (2^-11.29) | 11.29 |
| 3 | `iterative:data_width=17,n_iter=17,angle_guard=3,frac_guard=1,rounding=trunc` | 8276 | 116 | 6.1 | 20 | 0.226 | 0.00017 (2^-12.52) | 12.52 |
| 4 | `iterative:data_width=17,n_iter=17,angle_guard=3,frac_guard=2,rounding=trunc` | 8597 | 118 | 6.1 | 20 | 0.233 | 9.91e-05 (2^-13.30) | 13.30 |
| 5 | `iterative:data_width=18,n_iter=17,angle_guard=3,frac_guard=2,rounding=trunc` | 9025 | 124 | 5.9 | 20 | 0.244 | 5.67e-05 (2^-14.11) | 14.11 |
| 6 | `iterative:data_width=18,n_iter=19,angle_guard=2,frac_guard=2,rounding=trunc` | 9071 | 123 | 5.5 | 22 | 0.267 | 5.33e-05 (2^-14.20) | 14.20 |
| 7 | `iterative:data_width=20,n_iter=19,angle_guard=3,frac_guard=0,rounding=trunc` | 9348 | 130 | 5.0 | 22 | 0.28 | 4.23e-05 (2^-14.53) | 14.53 |
| 8 | `iterative:data_width=20,n_iter=19,angle_guard=3,frac_guard=1,rounding=trunc` | 9693 | 132 | 5.0 | 22 | 0.288 | 2.4e-05 (2^-15.35) | 15.35 |
| 9 | `iterative:data_width=21,n_iter=22,angle_guard=1,frac_guard=0,rounding=trunc` | 9783 | 134 | 4.6 | 25 | 0.33 | 2.36e-05 (2^-15.37) | 15.37 |
| 10 | `iterative:data_width=22,n_iter=18,angle_guard=0,frac_guard=0,rounding=trunc` | 9989 | 138 | 5.4 | 21 | 0.285 | 1.77e-05 (2^-15.79) | 15.79 |
| 11 | `iterative:data_width=21,n_iter=22,angle_guard=1,frac_guard=0,rounding=round` | 10037 | 134 | 4.6 | 25 | 0.333 | 1.21e-05 (2^-16.34) | 16.34 |
| 12 | `iterative:data_width=21,n_iter=27,angle_guard=3,frac_guard=0,rounding=round` | 10237 | 136 | 3.6 | 30 | 0.407 | 1.15e-05 (2^-16.41) | 16.41 |
| 13 | `iterative:data_width=22,n_iter=18,angle_guard=3,frac_guard=0,rounding=round` | 10386 | 141 | 4.9 | 21 | 0.293 | 1.1e-05 (2^-16.47) | 16.47 |
| 14 | `iterative:data_width=22,n_iter=29,angle_guard=3,frac_guard=0,rounding=round` | 10774 | 141 | 3.2 | 32 | 0.454 | 5.23e-06 (2^-17.54) | 17.54 |
| 15 | `iterative:data_width=23,n_iter=22,angle_guard=0,frac_guard=0,rounding=round` | 10951 | 143 | 4.4 | 25 | 0.361 | 3.98e-06 (2^-17.94) | 17.94 |
| 16 | `iterative:data_width=24,n_iter=23,angle_guard=1,frac_guard=0,rounding=trunc` | 11297 | 150 | 4.0 | 26 | 0.39 | 2.96e-06 (2^-18.37) | 18.37 |
| 17 | `iterative:data_width=22,n_iter=22,angle_guard=4,frac_guard=4,rounding=trunc` | 11988 | 151 | 4.0 | 25 | 0.386 | 1.93e-06 (2^-18.99) | 18.99 |
| 18 | `iterative:data_width=25,n_iter=22,angle_guard=1,frac_guard=0,rounding=round` | 11992 | 155 | 4.0 | 25 | 0.393 | 1.41e-06 (2^-19.44) | 19.44 |
| 19 | `iterative:data_width=25,n_iter=24,angle_guard=2,frac_guard=0,rounding=round` | 12189 | 156 | 3.6 | 27 | 0.429 | 8.15e-07 (2^-20.23) | 20.23 |
| 20 | `iterative:data_width=27,n_iter=24,angle_guard=0,frac_guard=0,rounding=round` | 13088 | 165 | 3.6 | 27 | 0.456 | 3.79e-07 (2^-21.33) | 21.33 |
| 21 | `iterative:data_width=27,n_iter=24,angle_guard=2,frac_guard=0,rounding=round` | 13214 | 167 | 3.4 | 27 | 0.462 | 2.66e-07 (2^-21.84) | 21.84 |
| 22 | `iterative:data_width=28,n_iter=25,angle_guard=1,frac_guard=1,rounding=trunc` | 13876 | 174 | 3.3 | 28 | 0.5 | 1.59e-07 (2^-22.59) | 22.59 |
| 23 | `unrolled_k:data_width=28,n_iter=30,angle_guard=2,frac_guard=4,rounding=trunc,k=3` | 23735 | 181 | 2.4 | 13 | 0.312 | 4.72e-08 (2^-24.34) | 24.34 |
| 24 | `unrolled_k:data_width=28,n_iter=29,angle_guard=3,frac_guard=2,rounding=round,k=5` | 33043 | 176 | 2.2 | 9 | 0.263 | 3.6e-08 (2^-24.73) | 24.73 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-minimising with a loose throughput floor (>=1 MSPS) and a moderate accuracy floor (max_abs_err <= 2^-10). Iterative reuses a single micro-rotation datapath, so it should achieve the smallest area for any given accuracy; unrolled_k replicates the datapath k times and is therefore expected to be dominated. We allocate 85% of the budget to iterative to densely map its Pareto front, focusing on the region where the accuracy constraint becomes feasible (roughly W >= 12, N >= 11) and extending to larger sizes to cover the hypervolume reference area (40000 um^2). The remaining 15% checks unrolled_k for any unexpected advantage, but we expect the final front to be entirely iterative. Ranges are chosen to include the feasibility boundary (slightly below the expected minimum W and N) and to cover the trade-off up to the reference point without wasting budget on clearly infeasible or dominated regions.*)
- `iterative` (51 evals): data_width=10..28, n_iter=8..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Iterative shares one datapath, so it has the smallest area per accuracy point. The throughput constraint (>=1 MSPS) is easily met by iterative at these sizes (N+3 cycles/result, Fmax in the tens to hundreds of MHz). The accuracy constraint (max_abs_err <= 2^-10) requires at least ~12-bit data width and ~11 iterations; ranges start slightly below to let the search find the exact feasibility boundary and extend upward to map the area-accuracy trade-off up to the HV reference area.
- `unrolled_k` (9 evals): data_width=10..28, n_iter=8..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..4. *Why:* Unrolled_k replicates the datapath k times, so for the same accuracy it should have larger area than iterative. However, it is the only other family available to us, and a small budget verifies whether any k=2 configuration can be competitive (e.g., if iterative's Fmax is unexpectedly low, unrolled_k might trade area for speed, but the throughput constraint is only 1 MSPS so this is unlikely). The ranges mirror iterative to allow direct comparison.

**Result (code):** 60 evaluations this round, 60 total; 52 feasible; hypervolume 3.955e+05 (n/a).

**LLM decision:** `stop` — This is the final round, so the only valid choices are stop or infeasible. The spec is satisfiable: 52 of 60 evaluations are feasible, and the throughput constraint is met by every design (0% violate, best 10.1 MSPS vs >=1 required) while the error constraint is met by the whole Pareto front (best 2^-24.34 vs <=2^-10 required). The front already spans the objectives well: area_um2 7106..23735 against the HV reference 40000, and accuracy_bits 10.2..24.3 against the HV reference 10, with data_width 15..28 covering most of the registry range. The selection rule (min area_um2) is satisfied by iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc] at area_um2=7106, accuracy_bits=10.2, max_abs_err=0.000822 (2^-10.25), throughput 7.86 MSPS — comfortably inside both constraints. No further round is available to improve the front, and no constraint is unreachable, so stopping is correct rather than declaring infeasible.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 3.955e+05 (gain this round: n/a (first round)).
Feasible designs: 52 of 60 evaluations (45 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 10.1
- max_abs_err <= 0.000976562: 13% violate; best seen 4.72e-08 (2^-24.34)

Pareto front (feasible, 17 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc] area_um2=7106, accuracy_bits=10.2, ffs=101, throughput_msps=7.86, max_abs_err=0.000822 (2^-10.25), power_index=0.176
- iterative [data_width=17 n_iter=22 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=7865, accuracy_bits=11.3, ffs=112, throughput_msps=5.24, max_abs_err=0.000398 (2^-11.29), power_index=0.271
- iterative [data_width=17 n_iter=17 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=8597, accuracy_bits=13.3, ffs=118, throughput_msps=6.09, max_abs_err=9.91e-05 (2^-13.30), power_index=0.233
- iterative [data_width=18 n_iter=17 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=9025, accuracy_bits=14.1, ffs=124, throughput_msps=5.89, max_abs_err=5.67e-05 (2^-14.11), power_index=0.244
- iterative [data_width=20 n_iter=19 angle_guard=3 frac_guard=0 rounding=trunc] area_um2=9348, accuracy_bits=14.5, ffs=130, throughput_msps=5.01, max_abs_err=4.23e-05 (2^-14.53), power_index=0.28
- iterative [data_width=21 n_iter=22 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=9783, accuracy_bits=15.4, ffs=134, throughput_msps=4.56, max_abs_err=2.36e-05 (2^-15.37), power_index=0.33
- iterative [data_width=21 n_iter=27 angle_guard=3 frac_guard=0 rounding=round] area_um2=10237, accuracy_bits=16.4, ffs=136, throughput_msps=3.56, max_abs_err=1.15e-05 (2^-16.41), power_index=0.407
- iterative [data_width=24 n_iter=23 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=11297, accuracy_bits=18.4, ffs=150, throughput_msps=3.99, max_abs_err=2.96e-06 (2^-18.37), power_index=0.39
- iterative [data_width=28 n_iter=22 angle_guard=3 frac_guard=1 rounding=trunc] area_um2=13711, accuracy_bits=20.8, ffs=176, throughput_msps=3.52, max_abs_err=5.39e-07 (2^-20.82), power_index=0.447
- unrolled_k [data_width=28 n_iter=30 angle_guard=2 frac_guard=4 rounding=trunc k=3] area_um2=23735, accuracy_bits=24.3, ffs=181, throughput_msps=2.38, max_abs_err=4.72e-08 (2^-24.34), power_index=0.312
Front coverage: area_um2 7106..23735 (HV reference 40000); accuracy_bits 10.2..24.3 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 51 evals, 45 feasible; max throughput seen 10.1 MSPS; best accuracy 22.59 bits; best feasible area_um2=7106; feasible ranges: data_width 15..28, n_iter 11..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 9 evals, 7 feasible; max throughput seen 5.33 MSPS; best accuracy 24.34 bits; best feasible area_um2=17039; feasible ranges: data_width 19..28, n_iter 17..30, angle_guard -2..4, frac_guard 1..4, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (35 evals): data_width=14..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (16 front designs; box front_anchored)
- `unrolled_k` (5 evals): data_width=27..28, n_iter=28..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 91 feasible; hypervolume 4.028e+05 (+1.9%).

**No LLM call** (code's front-mapping round): This is the final round, so the only valid choices are stop or infeasible. The spec is satisfiable: 52 of 60 evaluations are feasible, and the throughput constraint is met by every design (0% violate, best 10.1 MSPS vs >=1 required) while the error constraint is met by the whole Pareto front (best 2^-24.34 vs <=2^-10 required). The front already spans the objectives well: area_um2 7106..23735 against the HV reference 40000, and accuracy_bits 10.2..24.3 against the HV reference 10, with data_width 15..28 covering most of the registry range. The selection rule (min area_um2) is satisfied by iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc] at area_um2=7106, accuracy_bits=10.2, max_abs_err=0.000822 (2^-10.25), throughput 7.86 MSPS — comfortably inside both constraints. No further round is available to improve the front, and no constraint is unreachable, so stopping is correct rather than declaring infeasible.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 4.028e+05 (gain this round: +1.9%).
Feasible designs: 91 of 100 evaluations (78 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 10.1
- max_abs_err <= 0.000976562: 9% violate; best seen 3.6e-08 (2^-24.73)

Pareto front (feasible, 25 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc] area_um2=7106, accuracy_bits=10.2, ffs=101, throughput_msps=7.86, max_abs_err=0.000822 (2^-10.25), power_index=0.176
- iterative [data_width=17 n_iter=17 angle_guard=3 frac_guard=1 rounding=trunc] area_um2=8276, accuracy_bits=12.5, ffs=116, throughput_msps=6.09, max_abs_err=0.00017 (2^-12.52), power_index=0.226
- iterative [data_width=18 n_iter=17 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=9025, accuracy_bits=14.1, ffs=124, throughput_msps=5.89, max_abs_err=5.67e-05 (2^-14.11), power_index=0.244
- iterative [data_width=20 n_iter=19 angle_guard=3 frac_guard=1 rounding=trunc] area_um2=9693, accuracy_bits=15.3, ffs=132, throughput_msps=5.01, max_abs_err=2.4e-05 (2^-15.35), power_index=0.288
- iterative [data_width=21 n_iter=22 angle_guard=1 frac_guard=0 rounding=round] area_um2=10037, accuracy_bits=16.3, ffs=134, throughput_msps=4.56, max_abs_err=1.21e-05 (2^-16.34), power_index=0.333
- iterative [data_width=22 n_iter=18 angle_guard=3 frac_guard=0 rounding=round] area_um2=10386, accuracy_bits=16.5, ffs=141, throughput_msps=4.94, max_abs_err=1.1e-05 (2^-16.47), power_index=0.293
- iterative [data_width=24 n_iter=23 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=11297, accuracy_bits=18.4, ffs=150, throughput_msps=3.99, max_abs_err=2.96e-06 (2^-18.37), power_index=0.39
- iterative [data_width=25 n_iter=24 angle_guard=2 frac_guard=0 rounding=round] area_um2=12189, accuracy_bits=20.2, ffs=156, throughput_msps=3.63, max_abs_err=8.15e-07 (2^-20.23), power_index=0.429
- iterative [data_width=27 n_iter=24 angle_guard=2 frac_guard=0 rounding=round] area_um2=13214, accuracy_bits=21.8, ffs=167, throughput_msps=3.44, max_abs_err=2.66e-07 (2^-21.84), power_index=0.462
- unrolled_k [data_width=28 n_iter=29 angle_guard=3 frac_guard=2 rounding=round k=5] area_um2=33043, accuracy_bits=24.7, ffs=176, throughput_msps=2.15, max_abs_err=3.6e-08 (2^-24.73), power_index=0.263
Front coverage: area_um2 7106..33043 (HV reference 40000); accuracy_bits 10.2..24.7 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 86 evals, 79 feasible; max throughput seen 10.1 MSPS; best accuracy 22.59 bits; best feasible area_um2=7106; feasible ranges: data_width 15..28, n_iter 11..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 14 evals, 12 feasible; max throughput seen 5.33 MSPS; best accuracy 24.73 bits; best feasible area_um2=17039; feasible ranges: data_width 19..28, n_iter 17..30, angle_guard -2..4, frac_guard 1..4, k 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4434 in, 5661 out
- provider-reported cost: $0.0036
- full prompts and replies: `llm_trace.jsonl`

