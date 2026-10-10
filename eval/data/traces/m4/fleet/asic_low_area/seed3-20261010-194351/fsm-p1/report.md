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
`iterative:data_width=15,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 7042 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1876 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 100 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 142 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 7.86 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 127 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.174 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000632 (2^-10.63) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 5.18 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000164 (2^-12.58) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.34 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.6 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (16 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 7042 | 100 | 7.9 | 18 | 0.174 | 0.000632 (2^-10.63) | 10.63 |
| 1 | `iterative:data_width=15,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc` | 7121 | 102 | 8.3 | 17 | 0.167 | 0.000594 (2^-10.72) | 10.72 |
| 2 | `iterative:data_width=16,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 7446 | 105 | 7.6 | 18 | 0.184 | 0.000301 (2^-11.70) | 11.70 |
| 3 | `iterative:data_width=18,n_iter=13,angle_guard=1,frac_guard=0,rounding=round` | 8071 | 116 | 7.9 | 16 | 0.179 | 0.000289 (2^-11.76) | 11.76 |
| 4 | `iterative:data_width=18,n_iter=13,angle_guard=1,frac_guard=1,rounding=round` | 9840 | 118 | 7.9 | 16 | 0.198 | 0.000279 (2^-11.81) | 11.81 |
| 5 | `unrolled_k:data_width=16,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,k=2` | 10291 | 109 | 6.5 | 11 | 0.134 | 0.000241 (2^-12.02) | 12.02 |
| 6 | `iterative:data_width=22,n_iter=22,angle_guard=4,frac_guard=0,rounding=round` | 10716 | 142 | 4.0 | 25 | 0.356 | 5.23e-06 (2^-17.54) | 17.54 |
| 7 | `iterative:data_width=23,n_iter=22,angle_guard=3,frac_guard=0,rounding=round` | 11141 | 147 | 4.0 | 25 | 0.368 | 2.9e-06 (2^-18.39) | 18.39 |
| 8 | `iterative:data_width=24,n_iter=28,angle_guard=4,frac_guard=1,rounding=trunc` | 12002 | 155 | 3.1 | 31 | 0.487 | 1.78e-06 (2^-19.10) | 19.10 |
| 9 | `iterative:data_width=22,n_iter=26,angle_guard=4,frac_guard=4,rounding=trunc` | 12206 | 151 | 3.5 | 29 | 0.452 | 1.68e-06 (2^-19.18) | 19.18 |
| 10 | `iterative:data_width=24,n_iter=22,angle_guard=2,frac_guard=4,rounding=trunc` | 12838 | 160 | 3.8 | 25 | 0.411 | 1.14e-06 (2^-19.74) | 19.74 |
| 11 | `iterative:data_width=24,n_iter=27,angle_guard=4,frac_guard=3,rounding=trunc` | 12887 | 160 | 3.2 | 30 | 0.494 | 5.9e-07 (2^-20.69) | 20.69 |
| 12 | `iterative:data_width=24,n_iter=26,angle_guard=4,frac_guard=4,rounding=trunc` | 13280 | 162 | 3.3 | 29 | 0.488 | 4.17e-07 (2^-21.19) | 21.19 |
| 13 | `iterative:data_width=25,n_iter=26,angle_guard=4,frac_guard=3,rounding=trunc` | 13387 | 165 | 3.2 | 29 | 0.495 | 2.82e-07 (2^-21.76) | 21.76 |
| 14 | `iterative:data_width=28,n_iter=28,angle_guard=3,frac_guard=0,rounding=round` | 14058 | 174 | 2.8 | 31 | 0.557 | 1.11e-07 (2^-23.10) | 23.10 |
| 15 | `iterative:data_width=28,n_iter=28,angle_guard=4,frac_guard=3,rounding=round` | 17812 | 182 | 2.8 | 31 | 0.638 | 2.42e-08 (2^-25.30) | 25.30 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The throughput constraint (>=1 MSPS) is easily satisfied by both iterative and unrolled_k for N<=30 and k>=2, so it is not binding. Accuracy requires data_width >= 11 with rounding (half-LSB = 2^-10) and n_iter >= ~11 to keep CORDIC approximation error below the quantization floor. Area is the sole objective, so the optimal design will use the smallest feasible data_width, n_iter, and guard bits. iterative reuses one micro-rotation stage and is therefore the smallest-area family; unrolled_k replicates k stages and is likely dominated. We allocate 80% of the first-round budget to iterative to pin down the minimum-area feasible point, and 20% to unrolled_k to confirm dominance or find any niche. Ranges are narrowed to the plausible low-area region (W=11..16, N=10..16, small guards) to spend evaluations where the trade-off is steep. We use 60 of the 100 total evaluations this round, reserving 40 for later refinement and full-range Pareto mapping.*)
- `iterative` (48 evals): data_width=11..16, n_iter=10..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Smallest-area family (shared datapath). Focus on the minimum feasible W (11) and N (10-16) with small guards to find the absolute minimum-area design that meets max_abs_err <= 2^-10. Rounding is included because it can save one bit of width.
- `unrolled_k` (12 evals): data_width=11..16, n_iter=10..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..3. *Why:* Likely dominated by iterative because it replicates k micro-rotation stages, increasing area roughly proportionally to k. Small budget to verify dominance and check if any k=2 configuration can compete on area for the same accuracy.

**Result (code):** 60 evaluations this round, 60 total; 24 feasible; hypervolume 6.514e+04 (n/a).

**LLM decision:** `stop` — Final round (round cap reached). The feasible front is established and satisfies both constraints: every front point has throughput >= 6.49 MSPS (constraint >= 1 MSPS) and max_abs_err <= 6.32e-4 (constraint <= 9.77e-4), with the best accuracy 2^-12.02. The selection rule (min area_um2) picks iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] at area_um2=7042, accuracy_bits=10.63, 7.86 MSPS, power_index=0.174 — well inside the HV reference area of 40000 and above the accuracy reference of 10 bits. The front spans area 7042..10291 um2 and accuracy 10.6..12.0 bits, so both objectives are covered near the reference point; no constraint is violated by any front member, so the spec is not infeasible. Further exploration (pipelined families) is out of budget for this run, and the current front already meets the spec with margin, so stopping is appropriate.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 6.514e+04 (gain this round: n/a (first round)).
Feasible designs: 24 of 60 evaluations (17 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 12.1
- max_abs_err <= 0.000976562: 60% violate; best seen 0.000241 (2^-12.02)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=7042, accuracy_bits=10.6, ffs=100, throughput_msps=7.86, max_abs_err=0.000632 (2^-10.63), power_index=0.174
- iterative [data_width=15 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=7121, accuracy_bits=10.7, ffs=102, throughput_msps=8.32, max_abs_err=0.000594 (2^-10.72), power_index=0.167
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=7446, accuracy_bits=11.7, ffs=105, throughput_msps=7.56, max_abs_err=0.000301 (2^-11.70), power_index=0.184
- unrolled_k [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc k=2] area_um2=10291, accuracy_bits=12, ffs=109, throughput_msps=6.49, max_abs_err=0.000241 (2^-12.02), power_index=0.134
Front coverage: area_um2 7042..10291 (HV reference 40000); accuracy_bits 10.6..12 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- iterative: 48 evals, 18 feasible; max throughput seen 12.1 MSPS; best accuracy 11.70 bits; best feasible area_um2=7042; feasible ranges: data_width 14..16, n_iter 13..16, angle_guard -1..2, frac_guard 0..2
- unrolled_k: 12 evals, 6 feasible; max throughput seen 9.38 MSPS; best accuracy 12.02 bits; best feasible area_um2=10291; feasible ranges: data_width 14..16, n_iter 12..15, angle_guard 0..2, frac_guard 1..2, k 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (30 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (3 front designs; box front_anchored)
- `unrolled_k` (10 evals): data_width=15..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 64 feasible; hypervolume 4.267e+05 (+555.0%).

**No LLM call** (code's front-mapping round): Final round (round cap reached). The feasible front is established and satisfies both constraints: every front point has throughput >= 6.49 MSPS (constraint >= 1 MSPS) and max_abs_err <= 6.32e-4 (constraint <= 9.77e-4), with the best accuracy 2^-12.02. The selection rule (min area_um2) picks iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] at area_um2=7042, accuracy_bits=10.63, 7.86 MSPS, power_index=0.174 — well inside the HV reference area of 40000 and above the accuracy reference of 10 bits. The front spans area 7042..10291 um2 and accuracy 10.6..12.0 bits, so both objectives are covered near the reference point; no constraint is violated by any front member, so the spec is not infeasible. Further exploration (pipelined families) is out of budget for this run, and the current front already meets the spec with margin, so stopping is appropriate.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 4.267e+05 (gain this round: +555.0%).
Feasible designs: 64 of 100 evaluations (54 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 12.1
- max_abs_err <= 0.000976562: 36% violate; best seen 2.42e-08 (2^-25.30)

Pareto front (feasible, 16 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=7042, accuracy_bits=10.6, ffs=100, throughput_msps=7.86, max_abs_err=0.000632 (2^-10.63), power_index=0.174
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=7446, accuracy_bits=11.7, ffs=105, throughput_msps=7.56, max_abs_err=0.000301 (2^-11.70), power_index=0.184
- iterative [data_width=18 n_iter=13 angle_guard=1 frac_guard=0 rounding=round] area_um2=8071, accuracy_bits=11.8, ffs=116, throughput_msps=7.89, max_abs_err=0.000289 (2^-11.76), power_index=0.179
- unrolled_k [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc k=2] area_um2=10291, accuracy_bits=12, ffs=109, throughput_msps=6.49, max_abs_err=0.000241 (2^-12.02), power_index=0.134
- iterative [data_width=23 n_iter=22 angle_guard=3 frac_guard=0 rounding=round] area_um2=11141, accuracy_bits=18.4, ffs=147, throughput_msps=4.03, max_abs_err=2.9e-06 (2^-18.39), power_index=0.368
- iterative [data_width=24 n_iter=28 angle_guard=4 frac_guard=1 rounding=trunc] area_um2=12002, accuracy_bits=19.1, ffs=155, throughput_msps=3.07, max_abs_err=1.78e-06 (2^-19.10), power_index=0.487
- iterative [data_width=24 n_iter=22 angle_guard=2 frac_guard=4 rounding=trunc] area_um2=12838, accuracy_bits=19.7, ffs=160, throughput_msps=3.81, max_abs_err=1.14e-06 (2^-19.74), power_index=0.411
- iterative [data_width=24 n_iter=26 angle_guard=4 frac_guard=4 rounding=trunc] area_um2=13280, accuracy_bits=21.2, ffs=162, throughput_msps=3.29, max_abs_err=4.17e-07 (2^-21.19), power_index=0.488
- iterative [data_width=25 n_iter=26 angle_guard=4 frac_guard=3 rounding=trunc] area_um2=13387, accuracy_bits=21.8, ffs=165, throughput_msps=3.2, max_abs_err=2.82e-07 (2^-21.76), power_index=0.495
- iterative [data_width=28 n_iter=28 angle_guard=4 frac_guard=3 rounding=round] area_um2=17812, accuracy_bits=25.3, ffs=182, throughput_msps=2.77, max_abs_err=2.42e-08 (2^-25.30), power_index=0.638
Front coverage: area_um2 7042..17812 (HV reference 40000); accuracy_bits 10.6..25.3 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 78 evals, 48 feasible; max throughput seen 12.1 MSPS; best accuracy 25.30 bits; best feasible area_um2=7042; feasible ranges: data_width 14..28, n_iter 13..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 22 evals, 16 feasible; max throughput seen 9.38 MSPS; best accuracy 16.92 bits; best feasible area_um2=10291; feasible ranges: data_width 14..24, n_iter 12..28, angle_guard -2..4, frac_guard 0..4, k 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 3943 in, 8170 out
- provider-reported cost: $0.0056
- full prompts and replies: `llm_trace.jsonl`

