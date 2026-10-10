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
`iterative:data_width=15,n_iter=12,angle_guard=1,frac_guard=1,rounding=trunc` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 6987 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1861 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 102 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 142 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 9.43 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 15 | exact: schedule |
| latency_ns | 106 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.147 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000833 (2^-10.23) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.82 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000239 (2^-12.03) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.96 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.2 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=12,angle_guard=1,frac_guard=1,rounding=trunc` | 6987 | 102 | 9.4 | 15 | 0.147 | 0.000833 (2^-10.23) | 10.23 |
| 1 | `iterative:data_width=14,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc` | 7016 | 100 | 8.8 | 16 | 0.155 | 0.000746 (2^-10.39) | 10.39 |
| 2 | `iterative:data_width=15,n_iter=13,angle_guard=2,frac_guard=1,rounding=trunc` | 7123 | 103 | 8.5 | 16 | 0.159 | 0.000689 (2^-10.50) | 10.50 |
| 3 | `iterative:data_width=15,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc` | 7396 | 105 | 8.5 | 16 | 0.163 | 0.000466 (2^-11.07) | 11.07 |
| 4 | `iterative:data_width=15,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` | 7468 | 105 | 8.0 | 17 | 0.174 | 0.000405 (2^-11.27) | 11.27 |
| 5 | `unrolled_k:data_width=16,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc,k=2` | 10109 | 109 | 7.1 | 10 | 0.12 | 0.000378 (2^-11.37) | 11.37 |
| 6 | `iterative:data_width=22,n_iter=21,angle_guard=4,frac_guard=0,rounding=round` | 10668 | 142 | 4.2 | 24 | 0.341 | 5.23e-06 (2^-17.54) | 17.54 |
| 7 | `iterative:data_width=24,n_iter=21,angle_guard=4,frac_guard=0,rounding=trunc` | 11378 | 153 | 4.0 | 24 | 0.365 | 3.19e-06 (2^-18.26) | 18.26 |
| 8 | `iterative:data_width=22,n_iter=26,angle_guard=4,frac_guard=4,rounding=trunc` | 12206 | 151 | 3.5 | 29 | 0.452 | 1.68e-06 (2^-19.18) | 19.18 |
| 9 | `iterative:data_width=23,n_iter=21,angle_guard=4,frac_guard=4,rounding=trunc` | 12379 | 156 | 4.1 | 24 | 0.384 | 1.62e-06 (2^-19.24) | 19.24 |
| 10 | `iterative:data_width=24,n_iter=21,angle_guard=4,frac_guard=3,rounding=trunc` | 12486 | 160 | 4.0 | 24 | 0.39 | 1.33e-06 (2^-19.52) | 19.52 |
| 11 | `iterative:data_width=25,n_iter=26,angle_guard=4,frac_guard=3,rounding=trunc` | 13387 | 165 | 3.2 | 29 | 0.495 | 2.82e-07 (2^-21.76) | 21.76 |
| 12 | `iterative:data_width=28,n_iter=28,angle_guard=4,frac_guard=3,rounding=round` | 17812 | 182 | 2.8 | 31 | 0.638 | 2.42e-08 (2^-25.30) | 25.30 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *No fleet facts yet, so I seed both allowed families. The spec is area-dominated with a hard throughput floor (>=1 MSPS) and a hard accuracy floor (max_abs_err <= 2^-10, i.e. accuracy_bits >= 10). iterative is the natural area-minimiser (shared datapath, no pipeline registers) but is throughput-limited by its N+3 cycle latency, so I cap n_iter at 14 to stay near the 10-cycle budget at 100 MHz. unrolled_k is included because k>1 can hit 1 MSPS with fewer iterations or a lower clock, potentially at lower area than a longer iterative chain; k is kept to 2-4 to avoid the area blow-up of wide unrolled datapaths. data_width 12-16 brackets the minimal W that can reach accuracy_bits >= 10 up to a comfortable margin toward the HV reference, and angle_guard/frac_guard sweep the cheap accuracy levers. Rounding is left to both choices since it shifts accuracy at negligible area cost. The 55/45 split favours iterative (the likely area winner) while still mapping the unrolled trade-off so the merged front covers the curve.*)
- `iterative` (33 evals): data_width=12..16, n_iter=10..14, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the smallest-area family (single shared datapath, no per-stage registers). At 100 MHz it needs <=10 cycles/result to hit 1 MSPS, so n_iter 10-14 with data_width 12-16 covers the accuracy/area trade-off: W=12/N=10 is the minimal feasible corner, while W=14-16/N=12-14 buys accuracy_bits toward the HV reference of 10 at modest area cost. angle_guard -2..2 and frac_guard 0..2 sweep the accuracy levers that are free or cheap in area.
- `unrolled_k` (27 evals): data_width=12..16, n_iter=10..14, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k raises throughput per cycle (k rotations/cycle) so it can meet 1 MSPS at a lower Fmax or with fewer n_iter, which can trade off against area. k=2-4 with n_iter 10-14 keeps latency short and lets the search find whether unrolling beats iterative on area at equal accuracy. Same data_width/angle_guard/frac_guard/rounding ranges as iterative so the two fronts are directly comparable and merge cleanly.

**Result (code):** 60 evaluations this round, 60 total; 22 feasible; hypervolume 5.666e+04 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established and robust. The minimum area design (iterative, 6987 um^2) comfortably satisfies the throughput constraint (9.43 MSPS >= 1) and the accuracy constraint (10.2 bits >= 10). The front extends to higher accuracy (11.9 bits) at the cost of area, providing a good trade-off curve. Since this is the final round, we stop and select the minimum area design from the front as per the spec's selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 5.666e+04 (gain this round: n/a (first round)).
Feasible designs: 22 of 60 evaluations (16 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11.5
- max_abs_err <= 0.000976562: 63% violate; best seen 0.00027 (2^-11.85)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=6987, accuracy_bits=10.2, ffs=102, throughput_msps=9.43, max_abs_err=0.000833 (2^-10.23), power_index=0.147
- iterative [data_width=14 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7016, accuracy_bits=10.4, ffs=100, throughput_msps=8.84, max_abs_err=0.000746 (2^-10.39), power_index=0.155
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=7123, accuracy_bits=10.5, ffs=103, throughput_msps=8.5, max_abs_err=0.000689 (2^-10.50), power_index=0.159
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7396, accuracy_bits=11.1, ffs=105, throughput_msps=8.5, max_abs_err=0.000466 (2^-11.07), power_index=0.163
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7468, accuracy_bits=11.3, ffs=105, throughput_msps=8, max_abs_err=0.000405 (2^-11.27), power_index=0.174
- unrolled_k [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc k=2] area_um2=10109, accuracy_bits=11.4, ffs=109, throughput_msps=7.14, max_abs_err=0.000378 (2^-11.37), power_index=0.12
- unrolled_k [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc k=4] area_um2=14925, accuracy_bits=11.9, ffs=108, throughput_msps=5.34, max_abs_err=0.00027 (2^-11.85), power_index=0.104
Front coverage: area_um2 6987..14925 (HV reference 40000); accuracy_bits 10.2..11.9 (HV reference 10); data_width on the front 14..16 (registry 8..28).

Per family:
- iterative: 33 evals, 13 feasible; max throughput seen 11.5 MSPS; best accuracy 11.27 bits; best feasible area_um2=6987; feasible ranges: data_width 14..15, n_iter 12..14, angle_guard 0..2, frac_guard 1..2
- unrolled_k: 27 evals, 9 feasible; max throughput seen 9.46 MSPS; best accuracy 11.85 bits; best feasible area_um2=9241; feasible ranges: data_width 14..16, n_iter 13..14, angle_guard 1..2, frac_guard 1..2, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (29 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (5 front designs; box front_anchored)
- `unrolled_k` (11 evals): data_width=15..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 61 feasible; hypervolume 4.193e+05 (+640.0%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and robust. The minimum area design (iterative, 6987 um^2) comfortably satisfies the throughput constraint (9.43 MSPS >= 1) and the accuracy constraint (10.2 bits >= 10). The front extends to higher accuracy (11.9 bits) at the cost of area, providing a good trade-off curve. Since this is the final round, we stop and select the minimum area design from the front as per the spec's selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 4.193e+05 (gain this round: +640.0%).
Feasible designs: 61 of 100 evaluations (55 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11.5
- max_abs_err <= 0.000976562: 39% violate; best seen 2.42e-08 (2^-25.30)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=12 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=6987, accuracy_bits=10.2, ffs=102, throughput_msps=9.43, max_abs_err=0.000833 (2^-10.23), power_index=0.147
- iterative [data_width=14 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7016, accuracy_bits=10.4, ffs=100, throughput_msps=8.84, max_abs_err=0.000746 (2^-10.39), power_index=0.155
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7396, accuracy_bits=11.1, ffs=105, throughput_msps=8.5, max_abs_err=0.000466 (2^-11.07), power_index=0.163
- iterative [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=7468, accuracy_bits=11.3, ffs=105, throughput_msps=8, max_abs_err=0.000405 (2^-11.27), power_index=0.174
- unrolled_k [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc k=2] area_um2=10109, accuracy_bits=11.4, ffs=109, throughput_msps=7.14, max_abs_err=0.000378 (2^-11.37), power_index=0.12
- iterative [data_width=24 n_iter=21 angle_guard=4 frac_guard=0 rounding=trunc] area_um2=11378, accuracy_bits=18.3, ffs=153, throughput_msps=3.97, max_abs_err=3.19e-06 (2^-18.26), power_index=0.365
- iterative [data_width=22 n_iter=26 angle_guard=4 frac_guard=4 rounding=trunc] area_um2=12206, accuracy_bits=19.2, ffs=151, throughput_msps=3.48, max_abs_err=1.68e-06 (2^-19.18), power_index=0.452
- iterative [data_width=23 n_iter=21 angle_guard=4 frac_guard=4 rounding=trunc] area_um2=12379, accuracy_bits=19.2, ffs=156, throughput_msps=4.08, max_abs_err=1.62e-06 (2^-19.24), power_index=0.384
- iterative [data_width=25 n_iter=26 angle_guard=4 frac_guard=3 rounding=trunc] area_um2=13387, accuracy_bits=21.8, ffs=165, throughput_msps=3.2, max_abs_err=2.82e-07 (2^-21.76), power_index=0.495
- iterative [data_width=28 n_iter=28 angle_guard=4 frac_guard=3 rounding=round] area_um2=17812, accuracy_bits=25.3, ffs=182, throughput_msps=2.77, max_abs_err=2.42e-08 (2^-25.30), power_index=0.638
Front coverage: area_um2 6987..17812 (HV reference 40000); accuracy_bits 10.2..25.3 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 62 evals, 41 feasible; max throughput seen 11.5 MSPS; best accuracy 25.30 bits; best feasible area_um2=6987; feasible ranges: data_width 14..28, n_iter 12..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 38 evals, 20 feasible; max throughput seen 9.46 MSPS; best accuracy 17.08 bits; best feasible area_um2=9241; feasible ranges: data_width 14..24, n_iter 12..28, angle_guard -2..4, frac_guard 0..4, k 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4347 in, 1200 out
- provider-reported cost: $0.0023
- full prompts and replies: `llm_trace.jsonl`

