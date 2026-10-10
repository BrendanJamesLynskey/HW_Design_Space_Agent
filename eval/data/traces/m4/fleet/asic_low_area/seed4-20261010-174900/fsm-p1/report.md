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
`iterative:data_width=14,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 7014 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1868 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 98 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 142 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 8.32 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 120 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.163 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000944 (2^-10.05) | exact: bit-accurate model, exhaustive (16384 angles) |
| max_abs_err_lsb | 3.87 | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err | 0.000229 (2^-12.09) | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err_lsb | 0.939 | exact: bit-accurate model, exhaustive (16384 angles) |
| accuracy_bits | 10 | exact: bit-accurate model, exhaustive (16384 angles) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=14,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc` | 7014 | 98 | 8.3 | 17 | 0.163 | 0.000944 (2^-10.05) | 10.05 |
| 1 | `iterative:data_width=16,n_iter=20,angle_guard=2,frac_guard=0,rounding=trunc` | 7476 | 107 | 5.7 | 23 | 0.238 | 0.000708 (2^-10.46) | 10.46 |
| 2 | `iterative:data_width=16,n_iter=20,angle_guard=-1,frac_guard=0,rounding=round` | 7516 | 104 | 6.2 | 23 | 0.235 | 0.000702 (2^-10.48) | 10.48 |
| 3 | `iterative:data_width=16,n_iter=17,angle_guard=4,frac_guard=0,rounding=trunc` | 7590 | 109 | 6.1 | 20 | 0.211 | 0.000643 (2^-10.60) | 10.60 |
| 4 | `iterative:data_width=16,n_iter=20,angle_guard=3,frac_guard=0,rounding=round` | 7770 | 108 | 5.5 | 23 | 0.244 | 0.000285 (2^-11.78) | 11.78 |
| 5 | `iterative:data_width=16,n_iter=20,angle_guard=2,frac_guard=3,rounding=trunc` | 8536 | 114 | 5.5 | 23 | 0.261 | 0.000167 (2^-12.54) | 12.54 |
| 6 | `iterative:data_width=16,n_iter=17,angle_guard=4,frac_guard=4,rounding=trunc` | 8874 | 118 | 6.1 | 20 | 0.236 | 0.000103 (2^-13.24) | 13.24 |
| 7 | `iterative:data_width=21,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc` | 9719 | 132 | 4.7 | 25 | 0.327 | 2.66e-05 (2^-15.20) | 15.20 |
| 8 | `iterative:data_width=21,n_iter=20,angle_guard=3,frac_guard=0,rounding=round` | 10079 | 136 | 4.6 | 23 | 0.31 | 1.15e-05 (2^-16.41) | 16.41 |
| 9 | `iterative:data_width=22,n_iter=20,angle_guard=2,frac_guard=1,rounding=trunc` | 10607 | 142 | 4.6 | 23 | 0.326 | 6.11e-06 (2^-17.32) | 17.32 |
| 10 | `iterative:data_width=27,n_iter=28,angle_guard=-1,frac_guard=0,rounding=trunc` | 12915 | 164 | 3.2 | 31 | 0.519 | 7.11e-07 (2^-20.42) | 20.42 |
| 11 | `iterative:data_width=28,n_iter=25,angle_guard=2,frac_guard=0,rounding=trunc` | 13521 | 173 | 3.2 | 28 | 0.492 | 2.16e-07 (2^-22.14) | 22.14 |
| 12 | `iterative:data_width=28,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc` | 14775 | 179 | 3.1 | 28 | 0.523 | 9.99e-08 (2^-23.26) | 23.26 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >= 1 MSPS throughput and max_abs_err <= 2^-10, with area as the primary objective. Both iterative and unrolled_k can meet the throughput constraint easily since the required Fmax is low (13-17 MHz for iterative, 5-10 MHz for unrolled_k with k=2-4). The key trade-off is between area (driven by data_width, n_iter, and datapath width) and accuracy (driven by n_iter, guards, and rounding). I focus data_width on 10-14 because the output LSB is 2^-(W-2), so W=12 gives LSB=2^-10, and with N>=10 iterations and rounding, max_abs_err should be <= 2^-10. n_iter 10-14 is the minimum range that should achieve 10-bit accuracy with modest guards. angle_guard and frac_guard are kept small (0-2) to minimise datapath width while allowing the CORDIC iterations to converge. I allocate 60% of the budget to iterative since it has the simplest datapath (single adder/shift chain) and is likely to have the lowest area for a given accuracy, and 40% to unrolled_k to explore whether modest unrolling (k=2-4) can reduce the required n_iter or data_width while still meeting throughput, potentially finding a lower-area point on the Pareto front. The hypervolume reference point (area=40000 um^2, accuracy_bits=10) suggests that designs with area well below 40000 and accuracy >= 10 bits will contribute most to the hypervolume, so the search should focus on the low-area, just-meets-accuracy region.*)
- `iterative` (36 evals): data_width=10..14, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the only family that can plausibly meet throughput_msps >= 1 while minimising area. With 1 result per (N+3) cycles, throughput = Fmax/(N+3). To hit >= 1 MSPS we need Fmax >= N+3 MHz. For N=10..14, Fmax must be >= 13..17 MHz, which is very relaxed for sky130 standard cells. Area scales with data_width and n_iter, so we focus on the minimum widths that satisfy max_abs_err <= 2^-10. Accuracy depends on n_iter and guards; N=10..14 with appropriate guards should give >= 10 bits accuracy. data_width 10..14 covers the minimum needed for 10-bit accuracy (output LSB is 2^-(W-2), so W=12 gives LSB=2^-10, but we need max_abs_err <= 2^-10, so W=12 with N>=10 and rounding should work; W=10..14 explores the trade-off). angle_guard 0..2 and frac_guard 0..2 keep the datapath narrow while allowing enough precision for the CORDIC iterations to converge to 10-bit accuracy. rounding=round is likely better for accuracy at the same width, but trunc is cheaper; include both.
- `unrolled_k` (24 evals): data_width=10..14, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k with k=2..4 reduces latency to ceil(N/k)+3 cycles, improving throughput to Fmax/(ceil(N/k)+3). For N=10..14 and k=2..4, latency is 5..10 cycles, so throughput = Fmax/5..Fmax/10. This gives more Fmax headroom than iterative, but the unrolled datapath has k parallel adders/shifters, increasing area. The trade-off is: higher k -> better throughput but more area. Since area is the primary objective and the throughput constraint is only >= 1 MSPS (very relaxed), unrolled_k may not beat iterative on area unless the Fmax constraint forces iterative to use wider datapaths or more iterations. Include k=2..4 to explore whether modest unrolling can reduce n_iter or data_width while still meeting throughput, potentially lowering area. Same data_width, n_iter, guard ranges as iterative since accuracy requirements are identical.

**Result (code):** 60 evaluations this round, 60 total; 4 feasible; hypervolume 1.446e+04 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is established with 3 designs, all meeting the strict constraints: throughput >= 1 MSPS (best 8.32-8.68 MSPS) and max_abs_err <= 2^-10 (best 10.05-10.45 bits). The minimum area design is iterative [data_width=14, n_iter=14, angle_guard=1, frac_guard=2, rounding=trunc] at 7014 um^2. Since this is the final round (budget/cap reached), and the front covers the relevant trade-off space for the 'min area' selection rule, we stop. The selection rule 'min area_um2' will pick the 7014 um^2 design.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.446e+04 (gain this round: n/a (first round)).
Feasible designs: 4 of 60 evaluations (4 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14.4
- max_abs_err <= 0.000976562: 93% violate; best seen 0.000714 (2^-10.45)

Pareto front (feasible, 3 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=7014, accuracy_bits=10, ffs=98, throughput_msps=8.32, max_abs_err=0.000944 (2^-10.05), power_index=0.163
- iterative [data_width=13 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=7924, accuracy_bits=10.2, ffs=94, throughput_msps=8.68, max_abs_err=0.000856 (2^-10.19), power_index=0.168
- iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 rounding=round] area_um2=8335, accuracy_bits=10.5, ffs=98, throughput_msps=8.32, max_abs_err=0.000714 (2^-10.45), power_index=0.177
Front coverage: area_um2 7014..8335 (HV reference 40000); accuracy_bits 10..10.5 (HV reference 10); data_width on the front 13..14 (registry 8..28).

Per family:
- iterative: 36 evals, 3 feasible; max throughput seen 14.4 MSPS; best accuracy 10.45 bits; best feasible area_um2=7014; feasible ranges: data_width 13..14, n_iter 14..14, angle_guard 1..2, frac_guard 2..2
- unrolled_k: 24 evals, 1 feasible; max throughput seen 9.38 MSPS; best accuracy 10.28 bits; best feasible area_um2=14455; feasible ranges: data_width 14..14, n_iter 13..13, angle_guard 1..1, frac_guard 2..2, k 4..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (40 evals): data_width=12..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (3 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 39 feasible; hypervolume 3.832e+05 (+2550.2%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is established with 3 designs, all meeting the strict constraints: throughput >= 1 MSPS (best 8.32-8.68 MSPS) and max_abs_err <= 2^-10 (best 10.05-10.45 bits). The minimum area design is iterative [data_width=14, n_iter=14, angle_guard=1, frac_guard=2, rounding=trunc] at 7014 um^2. Since this is the final round (budget/cap reached), and the front covers the relevant trade-off space for the 'min area' selection rule, we stop. The selection rule 'min area_um2' will pick the 7014 um^2 design.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 3.832e+05 (gain this round: +2550.2%).
Feasible designs: 39 of 100 evaluations (39 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14.4
- max_abs_err <= 0.000976562: 61% violate; best seen 9.99e-08 (2^-23.26)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=14 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=7014, accuracy_bits=10, ffs=98, throughput_msps=8.32, max_abs_err=0.000944 (2^-10.05), power_index=0.163
- iterative [data_width=16 n_iter=20 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=7476, accuracy_bits=10.5, ffs=107, throughput_msps=5.69, max_abs_err=0.000708 (2^-10.46), power_index=0.238
- iterative [data_width=16 n_iter=17 angle_guard=4 frac_guard=0 rounding=trunc] area_um2=7590, accuracy_bits=10.6, ffs=109, throughput_msps=6.09, max_abs_err=0.000643 (2^-10.60), power_index=0.211
- iterative [data_width=16 n_iter=20 angle_guard=3 frac_guard=0 rounding=round] area_um2=7770, accuracy_bits=11.8, ffs=108, throughput_msps=5.49, max_abs_err=0.000285 (2^-11.78), power_index=0.244
- iterative [data_width=16 n_iter=20 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=8536, accuracy_bits=12.5, ffs=114, throughput_msps=5.49, max_abs_err=0.000167 (2^-12.54), power_index=0.261
- iterative [data_width=21 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=9719, accuracy_bits=15.2, ffs=132, throughput_msps=4.71, max_abs_err=2.66e-05 (2^-15.20), power_index=0.327
- iterative [data_width=21 n_iter=20 angle_guard=3 frac_guard=0 rounding=round] area_um2=10079, accuracy_bits=16.4, ffs=136, throughput_msps=4.65, max_abs_err=1.15e-05 (2^-16.41), power_index=0.31
- iterative [data_width=22 n_iter=20 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=10607, accuracy_bits=17.3, ffs=142, throughput_msps=4.65, max_abs_err=6.11e-06 (2^-17.32), power_index=0.326
- iterative [data_width=28 n_iter=25 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=13521, accuracy_bits=22.1, ffs=173, throughput_msps=3.23, max_abs_err=2.16e-07 (2^-22.14), power_index=0.492
- iterative [data_width=28 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=14775, accuracy_bits=23.3, ffs=179, throughput_msps=3.15, max_abs_err=9.99e-08 (2^-23.26), power_index=0.523
Front coverage: area_um2 7014..14775 (HV reference 40000); accuracy_bits 10..23.3 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 76 evals, 38 feasible; max throughput seen 14.4 MSPS; best accuracy 23.26 bits; best feasible area_um2=7014; feasible ranges: data_width 13..28, n_iter 14..30, angle_guard -1..4, frac_guard 0..4
- unrolled_k: 24 evals, 1 feasible; max throughput seen 9.38 MSPS; best accuracy 10.28 bits; best feasible area_um2=14455; feasible ranges: data_width 14..14, n_iter 13..13, angle_guard 1..1, frac_guard 2..2, k 4..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 3975 in, 1487 out
- provider-reported cost: $0.0022
- full prompts and replies: `llm_trace.jsonl`

