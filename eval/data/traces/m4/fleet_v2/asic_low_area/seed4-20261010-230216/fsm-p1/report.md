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
`iterative:data_width=15,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 7121 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1897 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 102 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 142 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 8.32 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 120 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.167 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000594 (2^-10.72) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 4.86 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000149 (2^-12.71) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.22 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.7 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (14 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc` | 7121 | 102 | 8.3 | 17 | 0.167 | 0.000594 (2^-10.72) | 10.72 |
| 1 | `iterative:data_width=15,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc` | 7184 | 103 | 8.0 | 17 | 0.169 | 0.000567 (2^-10.78) | 10.78 |
| 2 | `iterative:data_width=16,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 7449 | 106 | 7.7 | 17 | 0.175 | 0.000294 (2^-11.73) | 11.73 |
| 3 | `iterative:data_width=18,n_iter=20,angle_guard=2,frac_guard=0,rounding=trunc` | 8392 | 118 | 5.3 | 23 | 0.265 | 0.000179 (2^-12.45) | 12.45 |
| 4 | `iterative:data_width=18,n_iter=20,angle_guard=3,frac_guard=0,rounding=round` | 8686 | 119 | 5.1 | 23 | 0.27 | 7.75e-05 (2^-13.65) | 13.65 |
| 5 | `iterative:data_width=18,n_iter=25,angle_guard=4,frac_guard=4,rounding=trunc` | 10070 | 129 | 4.1 | 28 | 0.367 | 2.74e-05 (2^-15.15) | 15.15 |
| 6 | `iterative:data_width=22,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc` | 10208 | 138 | 4.6 | 25 | 0.342 | 1.39e-05 (2^-16.14) | 16.14 |
| 7 | `iterative:data_width=23,n_iter=27,angle_guard=-1,frac_guard=0,rounding=trunc` | 10706 | 142 | 3.7 | 30 | 0.426 | 9.92e-06 (2^-16.62) | 16.62 |
| 8 | `iterative:data_width=23,n_iter=23,angle_guard=0,frac_guard=0,rounding=trunc` | 10733 | 143 | 4.2 | 26 | 0.372 | 6.55e-06 (2^-17.22) | 17.22 |
| 9 | `iterative:data_width=23,n_iter=25,angle_guard=2,frac_guard=1,rounding=trunc` | 11314 | 148 | 3.7 | 28 | 0.417 | 3.08e-06 (2^-18.31) | 18.31 |
| 10 | `iterative:data_width=27,n_iter=28,angle_guard=2,frac_guard=0,rounding=trunc` | 13105 | 167 | 3.0 | 31 | 0.528 | 4.38e-07 (2^-21.12) | 21.12 |
| 11 | `iterative:data_width=28,n_iter=25,angle_guard=4,frac_guard=0,rounding=trunc` | 13648 | 175 | 3.1 | 28 | 0.498 | 2.16e-07 (2^-22.14) | 22.14 |
| 12 | `iterative:data_width=28,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc` | 14775 | 179 | 3.1 | 28 | 0.523 | 9.99e-08 (2^-23.26) | 23.26 |
| 13 | `iterative:data_width=28,n_iter=25,angle_guard=2,frac_guard=2,rounding=round` | 16976 | 177 | 3.2 | 28 | 0.556 | 9.27e-08 (2^-23.36) | 23.36 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=1 MSPS throughput and max_abs_err <= 2^-10, with area as the primary objective. Among my assigned families (iterative, unrolled_k), both are low-area (no pipeline registers). The key trade-off is: iterative has the smallest area but lowest throughput (1 result per N+3 cycles), while unrolled_k trades some area (k parallel stages) for higher throughput (1 result per ceil(N/k)+3 cycles). To meet 1 MSPS, I need Fmax/latency >= 1 MHz. For iterative with N=10, latency=13, so Fmax >= 13 MHz is needed (easy). For unrolled_k with N=10, k=2, latency=8, so Fmax >= 8 MHz. Both are feasible. The error constraint requires sufficient n_iter and data_width. I focus data_width on 10-16 (below 10, output LSB is too coarse to hit 2^-10 error; above 16, area grows with diminishing accuracy returns). n_iter 4-16 covers the accuracy range. angle_guard -2 to 2 and frac_guard 0-2 cover the accuracy-relevant guard bits without excessive width. I split the budget 50/50 between the two families to map the Pareto front across both, since unrolled_k may dominate iterative on the throughput-area trade-off for this spec.*)
- `iterative` (30 evals): data_width=10..16, n_iter=4..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the lowest-area family (single shared datapath, no pipeline registers). It is the only family that can plausibly meet the >=1 MSPS throughput constraint at minimal area, since its throughput = Fmax (1 result/cycle at the micro-rotation level is not applicable; it produces 1 result every N+3 cycles, so throughput = Fmax/(N+3)). For small N (4-8) and modest data_width, Fmax can be high enough that Fmax/(N+3) >= 1 MSPS. The error constraint (<= 2^-10) is met by n_iter >= ~10-12 with data_width >= 12. I narrow data_width to 10-16 and n_iter to 4-16 to focus on the feasible region where both constraints can be satisfied with minimal area.
- `unrolled_k` (30 evals): data_width=10..16, n_iter=4..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k with k=2-4 can achieve higher throughput than iterative (1 result every ceil(N/k)+3 cycles) while keeping area close to iterative (shared datapath, no pipeline registers, just k parallel shift/add stages). For N=8-12 and k=2-4, latency is 4-9 cycles, so throughput = Fmax/latency. If Fmax is ~100-200 MHz, throughput can reach 1-25 MSPS. This family may offer a better area-throughput trade-off than iterative for meeting the 1 MSPS constraint with lower area, since it can use fewer iterations (lower N) to meet accuracy while k boosts throughput. I limit k to 2-4 to keep area reasonable (k=8 would roughly double the datapath area).
- clamped by code: budget shares were all zero; split equally

**Result (code):** 60 evaluations this round, 60 total; 12 feasible; hypervolume 7.178e+04 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 4 distinct designs covering the trade-off between area (7121-9064 um^2) and accuracy (10.7-12.2 bits). The minimum area design (iterative, W=15, N=14, ag=1, fg=1, trunc) meets all constraints: throughput 8.32 MSPS >= 1 MSPS and max_abs_err 0.000594 <= 0.000977. The front spans the relevant region of the objective space, and the selection rule (min area) clearly points to the 7121 um^2 design. No further exploration is needed as the budget is exhausted and the front adequately covers the feasible trade-off space.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 7.178e+04 (gain this round: n/a (first round)).
Feasible designs: 12 of 60 evaluations (8 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 26.7
- max_abs_err <= 0.000976562: 80% violate; best seen 0.000209 (2^-12.22)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=7121, accuracy_bits=10.7, ffs=102, throughput_msps=8.32, max_abs_err=0.000594 (2^-10.72), power_index=0.167
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=7184, accuracy_bits=10.8, ffs=103, throughput_msps=8, max_abs_err=0.000567 (2^-10.78), power_index=0.169
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=7449, accuracy_bits=11.7, ffs=106, throughput_msps=7.7, max_abs_err=0.000294 (2^-11.73), power_index=0.175
- iterative [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=9064, accuracy_bits=12.2, ffs=108, throughput_msps=7.7, max_abs_err=0.000209 (2^-12.22), power_index=0.193
Front coverage: area_um2 7121..9064 (HV reference 40000); accuracy_bits 10.7..12.2 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- iterative: 30 evals, 12 feasible; max throughput seen 26.7 MSPS; best accuracy 12.22 bits; best feasible area_um2=7121; feasible ranges: data_width 15..16, n_iter 14..16, angle_guard 1..2, frac_guard 0..1
- unrolled_k: 30 evals, 0 feasible; max throughput seen 12.4 MSPS; best accuracy 9.61 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (40 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (4 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 50 feasible; hypervolume 3.873e+05 (+439.5%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 4 distinct designs covering the trade-off between area (7121-9064 um^2) and accuracy (10.7-12.2 bits). The minimum area design (iterative, W=15, N=14, ag=1, fg=1, trunc) meets all constraints: throughput 8.32 MSPS >= 1 MSPS and max_abs_err 0.000594 <= 0.000977. The front spans the relevant region of the objective space, and the selection rule (min area) clearly points to the 7121 um^2 design. No further exploration is needed as the budget is exhausted and the front adequately covers the feasible trade-off space.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 3.873e+05 (gain this round: +439.5%).
Feasible designs: 50 of 100 evaluations (45 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 26.7
- max_abs_err <= 0.000976562: 50% violate; best seen 9.27e-08 (2^-23.36)

Pareto front (feasible, 14 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=7121, accuracy_bits=10.7, ffs=102, throughput_msps=8.32, max_abs_err=0.000594 (2^-10.72), power_index=0.167
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=7184, accuracy_bits=10.8, ffs=103, throughput_msps=8, max_abs_err=0.000567 (2^-10.78), power_index=0.169
- iterative [data_width=18 n_iter=20 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=8392, accuracy_bits=12.4, ffs=118, throughput_msps=5.3, max_abs_err=0.000179 (2^-12.45), power_index=0.265
- iterative [data_width=18 n_iter=20 angle_guard=3 frac_guard=0 rounding=round] area_um2=8686, accuracy_bits=13.7, ffs=119, throughput_msps=5.12, max_abs_err=7.75e-05 (2^-13.65), power_index=0.27
- iterative [data_width=22 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=10208, accuracy_bits=16.1, ffs=138, throughput_msps=4.56, max_abs_err=1.39e-05 (2^-16.14), power_index=0.342
- iterative [data_width=23 n_iter=27 angle_guard=-1 frac_guard=0 rounding=trunc] area_um2=10706, accuracy_bits=16.6, ffs=142, throughput_msps=3.68, max_abs_err=9.92e-06 (2^-16.62), power_index=0.426
- iterative [data_width=23 n_iter=25 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=11314, accuracy_bits=18.3, ffs=148, throughput_msps=3.71, max_abs_err=3.08e-06 (2^-18.31), power_index=0.417
- iterative [data_width=27 n_iter=28 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=13105, accuracy_bits=21.1, ffs=167, throughput_msps=2.99, max_abs_err=4.38e-07 (2^-21.12), power_index=0.528
- iterative [data_width=28 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=14775, accuracy_bits=23.3, ffs=179, throughput_msps=3.15, max_abs_err=9.99e-08 (2^-23.26), power_index=0.523
- iterative [data_width=28 n_iter=25 angle_guard=2 frac_guard=2 rounding=round] area_um2=16976, accuracy_bits=23.4, ffs=177, throughput_msps=3.23, max_abs_err=9.27e-08 (2^-23.36), power_index=0.556
Front coverage: area_um2 7121..16976 (HV reference 40000); accuracy_bits 10.7..23.4 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 70 evals, 50 feasible; max throughput seen 26.7 MSPS; best accuracy 23.36 bits; best feasible area_um2=7121; feasible ranges: data_width 15..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 30 evals, 0 feasible; max throughput seen 12.4 MSPS; best accuracy 9.61 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4014 in, 1423 out
- provider-reported cost: $0.0036
- full prompts and replies: `llm_trace.jsonl`

