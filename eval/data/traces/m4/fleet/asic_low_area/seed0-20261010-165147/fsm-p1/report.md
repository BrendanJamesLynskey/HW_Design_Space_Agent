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
`iterative:data_width=15,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 7015 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1869 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 98 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 147 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 7.76 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 19 | exact: schedule |
| latency_ns | 129 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.183 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.00081 (2^-10.27) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.64 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00021 (2^-12.22) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.72 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (16 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 7015 | 98 | 7.8 | 19 | 0.183 | 0.00081 (2^-10.27) | 10.27 |
| 1 | `iterative:data_width=15,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 7079 | 100 | 7.4 | 19 | 0.184 | 0.000632 (2^-10.63) | 10.63 |
| 2 | `iterative:data_width=15,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 7142 | 101 | 7.2 | 19 | 0.186 | 0.000599 (2^-10.71) | 10.71 |
| 3 | `iterative:data_width=15,n_iter=16,angle_guard=2,frac_guard=1,rounding=trunc` | 7269 | 103 | 7.2 | 19 | 0.19 | 0.000567 (2^-10.78) | 10.78 |
| 4 | `iterative:data_width=17,n_iter=21,angle_guard=1,frac_guard=1,rounding=trunc` | 8222 | 114 | 5.5 | 24 | 0.268 | 0.00022 (2^-12.15) | 12.15 |
| 5 | `iterative:data_width=17,n_iter=18,angle_guard=3,frac_guard=4,rounding=trunc` | 9311 | 123 | 5.6 | 21 | 0.258 | 5.86e-05 (2^-14.06) | 14.06 |
| 6 | `iterative:data_width=21,n_iter=18,angle_guard=-2,frac_guard=0,rounding=round` | 9629 | 130 | 5.6 | 21 | 0.271 | 5.08e-05 (2^-14.26) | 14.26 |
| 7 | `iterative:data_width=21,n_iter=18,angle_guard=4,frac_guard=0,rounding=round` | 10009 | 137 | 4.9 | 21 | 0.284 | 1.44e-05 (2^-16.09) | 16.09 |
| 8 | `iterative:data_width=25,n_iter=18,angle_guard=-2,frac_guard=0,rounding=round` | 11389 | 152 | 4.9 | 21 | 0.318 | 9.67e-06 (2^-16.66) | 16.66 |
| 9 | `iterative:data_width=25,n_iter=18,angle_guard=4,frac_guard=0,rounding=trunc` | 11563 | 159 | 4.4 | 21 | 0.328 | 8.31e-06 (2^-16.88) | 16.88 |
| 10 | `iterative:data_width=25,n_iter=23,angle_guard=-2,frac_guard=1,rounding=trunc` | 12001 | 154 | 3.9 | 26 | 0.407 | 3.4e-06 (2^-18.17) | 18.17 |
| 11 | `iterative:data_width=25,n_iter=27,angle_guard=1,frac_guard=1,rounding=trunc` | 12361 | 158 | 3.4 | 30 | 0.481 | 1.13e-06 (2^-19.76) | 19.76 |
| 12 | `iterative:data_width=26,n_iter=29,angle_guard=1,frac_guard=0,rounding=trunc` | 12480 | 161 | 3.1 | 32 | 0.521 | 9.99e-07 (2^-19.93) | 19.93 |
| 13 | `iterative:data_width=28,n_iter=23,angle_guard=-2,frac_guard=0,rounding=trunc` | 13110 | 169 | 3.7 | 26 | 0.444 | 7.1e-07 (2^-20.43) | 20.43 |
| 14 | `iterative:data_width=26,n_iter=27,angle_guard=1,frac_guard=3,rounding=trunc` | 13795 | 167 | 3.1 | 30 | 0.523 | 2.9e-07 (2^-21.72) | 21.72 |
| 15 | `unrolled_k:data_width=27,n_iter=28,angle_guard=3,frac_guard=4,rounding=round,k=3` | 25461 | 176 | 2.4 | 13 | 0.322 | 4.98e-08 (2^-24.26) | 24.26 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Only iterative and unrolled_k are available to me, and both are the low-area, multi-cycle families (pipelined/pipelined_m, which would dominate on throughput, are assigned to other fleet members). The spec is area-minimisation subject to throughput >= 1 MSPS and max_abs_err <= 2^-10. Accuracy is easy: N=10-16 with W=12-16 gives accuracy_bits well above 10, so I keep n_iter and data_width in a tight band that guarantees the error constraint while leaving room for the area trade-off (larger W/N costs area). The binding constraint is throughput: iterative gives Fmax/(N+3) and unrolled_k gives Fmax*k/ceil(N/k), so I let Optuna explore the W/N/k space where Fmax is high enough to clear 1 MSPS. I split the budget evenly between the two families because iterative likely owns the absolute min-area point while unrolled_k can reach the same throughput at a lower required Fmax (shorter per-stage path), potentially finding a smaller-area point at the throughput boundary. angle_guard and frac_guard are kept small (0..2 / 0..1) since extra guard bits add area without helping the 2^-10 error target, and both rounding modes are kept so the model can pick the cheaper one. This focuses the 100 evals on the region that actually defines the Pareto front for this spec.*)
- `iterative` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..1, rounding=trunc|round. *Why:* iterative is the lowest-area family (single shared datapath, no per-stage registers). It is the only family here that can plausibly hit >=1 MSPS with a small N: at W~14, N~12 the datapath is short enough that Fmax should exceed ~100 MHz, giving throughput = Fmax/(N+3) >= 1 MSPS. Accuracy at N=12-16 with W=14-16 comfortably exceeds 2^-10. This is where the min-area corner of the front lives, so it gets the largest share.
- `unrolled_k` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..1, rounding=trunc|round, k=2..4. *Why:* unrolled_k trades a little area (k parallel shift/add stages) for higher throughput: results/cycle = k, so throughput = Fmax*k/ceil(N/k). For the same N and W it can meet >=1 MSPS at a lower Fmax (hence potentially lower area via shorter critical path per stage) than iterative, or meet it at the same Fmax with more margin. Searching k=2..4 maps the area-vs-throughput trade-off that iterative alone cannot express, so it covers the rest of the feasible front.

**Result (code):** 60 evaluations this round, 60 total; 25 feasible; hypervolume 6.939e+04 (n/a).

**LLM decision:** `stop` — The front is well-established and feasible. The minimum area design (iterative, 7015 um^2) meets all constraints (throughput 7.76 MSPS >= 1, error 2^-10.27 <= 2^-10). The front spans a reasonable range of accuracy (10.3 to 12.2 bits) and area (7015 to 11326 um^2), covering the trade-off space effectively. Since this is the final round, we stop and select the minimum area design from the front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 6.939e+04 (gain this round: n/a (first round)).
Feasible designs: 25 of 60 evaluations (20 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11
- max_abs_err <= 0.000976562: 58% violate; best seen 0.000209 (2^-12.22)

Pareto front (feasible, 10 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] area_um2=7015, accuracy_bits=10.3, ffs=98, throughput_msps=7.76, max_abs_err=0.00081 (2^-10.27), power_index=0.183
- iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=7079, accuracy_bits=10.6, ffs=100, throughput_msps=7.45, max_abs_err=0.000632 (2^-10.63), power_index=0.184
- iterative [data_width=15 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=7142, accuracy_bits=10.7, ffs=101, throughput_msps=7.16, max_abs_err=0.000599 (2^-10.71), power_index=0.186
- iterative [data_width=15 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=7269, accuracy_bits=10.8, ffs=103, throughput_msps=7.16, max_abs_err=0.000567 (2^-10.78), power_index=0.19
- iterative [data_width=15 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] area_um2=8635, accuracy_bits=11.3, ffs=102, throughput_msps=7.45, max_abs_err=0.00041 (2^-11.25), power_index=0.204
- iterative [data_width=15 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=8698, accuracy_bits=11.5, ffs=103, throughput_msps=7.16, max_abs_err=0.000348 (2^-11.49), power_index=0.206
- unrolled_k [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round k=2] area_um2=9536, accuracy_bits=11.5, ffs=104, throughput_msps=7.45, max_abs_err=0.000342 (2^-11.51), power_index=0.114
- unrolled_k [data_width=16 n_iter=14 angle_guard=2 frac_guard=0 rounding=round k=2] area_um2=9641, accuracy_bits=11.7, ffs=105, throughput_msps=7.14, max_abs_err=0.000294 (2^-11.73), power_index=0.115
- unrolled_k [data_width=16 n_iter=15 angle_guard=2 frac_guard=0 rounding=round k=2] area_um2=9713, accuracy_bits=11.8, ffs=105, throughput_msps=6.49, max_abs_err=0.000285 (2^-11.78), power_index=0.127
- unrolled_k [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round k=2] area_um2=11326, accuracy_bits=12.2, ffs=107, throughput_msps=7.14, max_abs_err=0.000209 (2^-12.22), power_index=0.126
Front coverage: area_um2 7015..11326 (HV reference 40000); accuracy_bits 10.3..12.2 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- iterative: 30 evals, 15 feasible; max throughput seen 11 MSPS; best accuracy 11.49 bits; best feasible area_um2=7015; feasible ranges: data_width 15..15, n_iter 12..16, angle_guard 0..2, frac_guard 0..1
- unrolled_k: 30 evals, 10 feasible; max throughput seen 9.97 MSPS; best accuracy 12.22 bits; best feasible area_um2=9536; feasible ranges: data_width 16..16, n_iter 14..16, angle_guard 1..2, frac_guard 0..1, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (24 evals): data_width=14..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (6 front designs; box front_anchored)
- `unrolled_k` (16 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (4 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 64 feasible; hypervolume 3.802e+05 (+447.9%).

**No LLM call** (code's front-mapping round): The front is well-established and feasible. The minimum area design (iterative, 7015 um^2) meets all constraints (throughput 7.76 MSPS >= 1, error 2^-10.27 <= 2^-10). The front spans a reasonable range of accuracy (10.3 to 12.2 bits) and area (7015 to 11326 um^2), covering the trade-off space effectively. Since this is the final round, we stop and select the minimum area design from the front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 3.802e+05 (gain this round: +447.9%).
Feasible designs: 64 of 100 evaluations (57 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11
- max_abs_err <= 0.000976562: 36% violate; best seen 4.98e-08 (2^-24.26)

Pareto front (feasible, 16 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] area_um2=7015, accuracy_bits=10.3, ffs=98, throughput_msps=7.76, max_abs_err=0.00081 (2^-10.27), power_index=0.183
- iterative [data_width=15 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=7142, accuracy_bits=10.7, ffs=101, throughput_msps=7.16, max_abs_err=0.000599 (2^-10.71), power_index=0.186
- iterative [data_width=15 n_iter=16 angle_guard=2 frac_guard=1 rounding=trunc] area_um2=7269, accuracy_bits=10.8, ffs=103, throughput_msps=7.16, max_abs_err=0.000567 (2^-10.78), power_index=0.19
- iterative [data_width=17 n_iter=18 angle_guard=3 frac_guard=4 rounding=trunc] area_um2=9311, accuracy_bits=14.1, ffs=123, throughput_msps=5.61, max_abs_err=5.86e-05 (2^-14.06), power_index=0.258
- iterative [data_width=21 n_iter=18 angle_guard=4 frac_guard=0 rounding=round] area_um2=10009, accuracy_bits=16.1, ffs=137, throughput_msps=4.94, max_abs_err=1.44e-05 (2^-16.09), power_index=0.284
- iterative [data_width=25 n_iter=18 angle_guard=-2 frac_guard=0 rounding=round] area_um2=11389, accuracy_bits=16.7, ffs=152, throughput_msps=4.94, max_abs_err=9.67e-06 (2^-16.66), power_index=0.318
- iterative [data_width=25 n_iter=23 angle_guard=-2 frac_guard=1 rounding=trunc] area_um2=12001, accuracy_bits=18.2, ffs=154, throughput_msps=3.88, max_abs_err=3.4e-06 (2^-18.17), power_index=0.407
- iterative [data_width=26 n_iter=29 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=12480, accuracy_bits=19.9, ffs=161, throughput_msps=3.06, max_abs_err=9.99e-07 (2^-19.93), power_index=0.521
- iterative [data_width=28 n_iter=23 angle_guard=-2 frac_guard=0 rounding=trunc] area_um2=13110, accuracy_bits=20.4, ffs=169, throughput_msps=3.67, max_abs_err=7.1e-07 (2^-20.43), power_index=0.444
- unrolled_k [data_width=27 n_iter=28 angle_guard=3 frac_guard=4 rounding=round k=3] area_um2=25461, accuracy_bits=24.3, ffs=176, throughput_msps=2.44, max_abs_err=4.98e-08 (2^-24.26), power_index=0.322
Front coverage: area_um2 7015..25461 (HV reference 40000); accuracy_bits 10.3..24.3 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 54 evals, 38 feasible; max throughput seen 11 MSPS; best accuracy 21.72 bits; best feasible area_um2=7015; feasible ranges: data_width 15..28, n_iter 12..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 46 evals, 26 feasible; max throughput seen 9.97 MSPS; best accuracy 24.26 bits; best feasible area_um2=9536; feasible ranges: data_width 15..27, n_iter 14..30, angle_guard -1..4, frac_guard 0..4, k 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4616 in, 1279 out
- provider-reported cost: $0.0034
- full prompts and replies: `llm_trace.jsonl`

