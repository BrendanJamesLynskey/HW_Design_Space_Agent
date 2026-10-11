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
`pipelined_m:data_width=15,n_iter=12,angle_guard=4,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 19909 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 5304 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 195 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 39.6 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 39.6 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 126 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.0226 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000807 (2^-10.27) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.61 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000238 (2^-12.04) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.95 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=12,angle_guard=4,frac_guard=0,rounding=round,m=4` | 19909 | 195 | 39.6 | 5 | 0.0226 | 0.000807 (2^-10.27) | 10.27 |
| 1 | `pipelined_m:data_width=15,n_iter=13,angle_guard=1,frac_guard=0,rounding=round,m=4` | 21355 | 238 | 45.8 | 6 | 0.0258 | 0.000673 (2^-10.54) | 10.54 |
| 2 | `pipelined_m:data_width=15,n_iter=13,angle_guard=3,frac_guard=3,rounding=trunc,m=8` | 21713 | 144 | 21.3 | 4 | 0.0208 | 0.000439 (2^-11.15) | 11.15 |
| 3 | `pipelined_m:data_width=15,n_iter=13,angle_guard=3,frac_guard=3,rounding=trunc,m=7` | 21713 | 144 | 24.2 | 4 | 0.0208 | 0.000439 (2^-11.15) | 11.15 |
| 4 | `pipelined_m:data_width=16,n_iter=13,angle_guard=1,frac_guard=0,rounding=round,m=4` | 22580 | 252 | 43.5 | 6 | 0.0273 | 0.000417 (2^-11.23) | 11.23 |
| 5 | `pipelined_m:data_width=16,n_iter=13,angle_guard=2,frac_guard=0,rounding=round,m=3` | 24218 | 312 | 54.3 | 7 | 0.0316 | 0.00041 (2^-11.25) | 11.25 |
| 6 | `pipelined_m:data_width=15,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=4` | 25504 | 256 | 43.5 | 6 | 0.0292 | 0.000362 (2^-11.43) | 11.43 |
| 7 | `pipelined_m:data_width=23,n_iter=13,angle_guard=3,frac_guard=3,rounding=round,m=6` | 33544 | 292 | 20.3 | 5 | 0.036 | 0.000244 (2^-12.00) | 12.00 |
| 8 | `pipelined_m:data_width=25,n_iter=13,angle_guard=2,frac_guard=4,rounding=round,m=7` | 34286 | 224 | 15.8 | 4 | 0.0327 | 0.000244 (2^-12.00) | 12.00 |
| 9 | `pipelined_m:data_width=15,n_iter=26,angle_guard=2,frac_guard=4,rounding=round,m=6` | 47154 | 328 | 26.8 | 7 | 0.046 | 0.000203 (2^-12.27) | 12.27 |
| 10 | `pipelined_m:data_width=15,n_iter=25,angle_guard=4,frac_guard=4,rounding=round,m=3` | 52627 | 590 | 51.9 | 11 | 0.0638 | 0.000114 (2^-13.10) | 13.10 |
| 11 | `pipelined_m:data_width=26,n_iter=20,angle_guard=4,frac_guard=4,rounding=round,m=7` | 55422 | 331 | 15.3 | 5 | 0.0511 | 1.93e-06 (2^-18.99) | 18.99 |
| 12 | `pipelined_m:data_width=26,n_iter=24,angle_guard=3,frac_guard=2,rounding=trunc,m=7` | 62691 | 409 | 15.8 | 6 | 0.0597 | 3.21e-07 (2^-21.57) | 21.57 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >= 1 MSPS throughput and max_abs_err <= 2^-10, with area as the sole objective. Only pipelined and pipelined_m produce 1 result/cycle, so they are the only families that can meet the throughput constraint without relying on high Fmax. I focus data_width on 12-16 and n_iter on 10-16 to cover the accuracy sweet spot where the error constraint is met with minimal area. Rounding is fixed to 'round' to minimize error for a given width. pipelined gets 60% of budget as the baseline area reference, and pipelined_m gets 40% to explore the area-reduction trade-off from fewer registers. This should map the Pareto front between area and accuracy_bits effectively within the 100-eval budget.*)
- `pipelined` (36 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* Full pipelining gives 1 result/cycle, so Fmax alone must be >= 1 MHz; the critical path is a single micro-rotation, so it is the most likely family to meet the throughput constraint while keeping area low. Narrowing n_iter to 10-16 and data_width to 12-16 focuses on the accuracy/area sweet spot where max_abs_err <= 2^-10 is achievable with minimal area.
- `pipelined_m` (24 evals): data_width=12..16, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* Registering every m stages (m=2-4) reduces flip-flop count and area versus full pipelining, at the cost of a longer critical path (m micro-rotations per stage). This trades area for Fmax, which is exactly the trade-off the spec cares about; it may yield smaller area designs that still meet the 1 MSPS throughput floor.

**Result (code):** 60 evaluations this round, 60 total; 25 feasible; hypervolume 2.506e+04 (n/a).

**LLM decision:** `stop` — The Pareto front is well-established with 5 feasible designs covering the area range 21355-40143 um^2 and accuracy 10.5-11.8 bits. The minimum area design (pipelined_m, 21355 um^2) meets all constraints: throughput 45.8 MSPS >= 1 MSPS and max_abs_err 0.000673 <= 0.000976562. The front spans a meaningful trade-off curve with good hypervolume (2.506e+04). Since this is the final round, the current front is sufficient for selection via min area_um2, which picks the 21355 um^2 pipelined_m design.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 2.506e+04 (gain this round: n/a (first round)).
Feasible designs: 25 of 60 evaluations (19 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 58% violate; best seen 0.000271 (2^-11.85)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=15 n_iter=13 angle_guard=1 frac_guard=0 rounding=round m=4] area_um2=21355, accuracy_bits=10.5, ffs=238, throughput_msps=45.8, max_abs_err=0.000673 (2^-10.54), power_index=0.0258
- pipelined_m [data_width=16 n_iter=13 angle_guard=1 frac_guard=0 rounding=round m=4] area_um2=22580, accuracy_bits=11.2, ffs=252, throughput_msps=43.5, max_abs_err=0.000417 (2^-11.23), power_index=0.0273
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=0 rounding=round m=3] area_um2=24218, accuracy_bits=11.3, ffs=312, throughput_msps=54.3, max_abs_err=0.00041 (2^-11.25), power_index=0.0316
- pipelined_m [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=4] area_um2=25504, accuracy_bits=11.4, ffs=256, throughput_msps=43.5, max_abs_err=0.000362 (2^-11.43), power_index=0.0292
- pipelined [data_width=15 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=40143, accuracy_bits=11.8, ffs=849, throughput_msps=149, max_abs_err=0.000271 (2^-11.85), power_index=0.0709
Front coverage: area_um2 21355..40143 (HV reference 40000); accuracy_bits 10.5..11.8 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- pipelined: 36 evals, 13 feasible; max throughput seen 171 MSPS; best accuracy 11.85 bits; best feasible area_um2=30890; feasible ranges: data_width 13..16, n_iter 12..16, angle_guard 0..2, frac_guard 1..2
- pipelined_m: 24 evals, 12 feasible; max throughput seen 96.1 MSPS; best accuracy 11.43 bits; best feasible area_um2=21355; feasible ranges: data_width 13..16, n_iter 13..16, angle_guard 0..2, frac_guard 0..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (32 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)
- `pipelined` (8 evals): data_width=14..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 61 feasible; hypervolume 2.966e+04 (+18.4%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established with 5 feasible designs covering the area range 21355-40143 um^2 and accuracy 10.5-11.8 bits. The minimum area design (pipelined_m, 21355 um^2) meets all constraints: throughput 45.8 MSPS >= 1 MSPS and max_abs_err 0.000673 <= 0.000976562. The front spans a meaningful trade-off curve with good hypervolume (2.506e+04). Since this is the final round, the current front is sufficient for selection via min area_um2, which picks the 21355 um^2 pipelined_m design.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 2.966e+04 (gain this round: +18.4%).
Feasible designs: 61 of 100 evaluations (49 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 171
- max_abs_err <= 0.000976562: 39% violate; best seen 3.21e-07 (2^-21.57)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=4 frac_guard=0 rounding=round m=4] area_um2=19909, accuracy_bits=10.3, ffs=195, throughput_msps=39.6, max_abs_err=0.000807 (2^-10.27), power_index=0.0226
- pipelined_m [data_width=15 n_iter=13 angle_guard=1 frac_guard=0 rounding=round m=4] area_um2=21355, accuracy_bits=10.5, ffs=238, throughput_msps=45.8, max_abs_err=0.000673 (2^-10.54), power_index=0.0258
- pipelined_m [data_width=15 n_iter=13 angle_guard=3 frac_guard=3 rounding=trunc m=7] area_um2=21713, accuracy_bits=11.2, ffs=144, throughput_msps=24.2, max_abs_err=0.000439 (2^-11.15), power_index=0.0208
- pipelined_m [data_width=16 n_iter=13 angle_guard=1 frac_guard=0 rounding=round m=4] area_um2=22580, accuracy_bits=11.2, ffs=252, throughput_msps=43.5, max_abs_err=0.000417 (2^-11.23), power_index=0.0273
- pipelined_m [data_width=16 n_iter=13 angle_guard=2 frac_guard=0 rounding=round m=3] area_um2=24218, accuracy_bits=11.3, ffs=312, throughput_msps=54.3, max_abs_err=0.00041 (2^-11.25), power_index=0.0316
- pipelined_m [data_width=23 n_iter=13 angle_guard=3 frac_guard=3 rounding=round m=6] area_um2=33544, accuracy_bits=12, ffs=292, throughput_msps=20.3, max_abs_err=0.000244 (2^-12.00), power_index=0.036
- pipelined_m [data_width=25 n_iter=13 angle_guard=2 frac_guard=4 rounding=round m=7] area_um2=34286, accuracy_bits=12, ffs=224, throughput_msps=15.8, max_abs_err=0.000244 (2^-12.00), power_index=0.0327
- pipelined_m [data_width=15 n_iter=26 angle_guard=2 frac_guard=4 rounding=round m=6] area_um2=47154, accuracy_bits=12.3, ffs=328, throughput_msps=26.8, max_abs_err=0.000203 (2^-12.27), power_index=0.046
- pipelined_m [data_width=26 n_iter=20 angle_guard=4 frac_guard=4 rounding=round m=7] area_um2=55422, accuracy_bits=19, ffs=331, throughput_msps=15.3, max_abs_err=1.93e-06 (2^-18.99), power_index=0.0511
- pipelined_m [data_width=26 n_iter=24 angle_guard=3 frac_guard=2 rounding=trunc m=7] area_um2=62691, accuracy_bits=21.6, ffs=409, throughput_msps=15.8, max_abs_err=3.21e-07 (2^-21.57), power_index=0.0597
Front coverage: area_um2 19909..62691 (HV reference 40000); accuracy_bits 10.3..21.6 (HV reference 10); data_width on the front 15..26 (registry 8..28).

Per family:
- pipelined: 44 evals, 20 feasible; max throughput seen 171 MSPS; best accuracy 18.89 bits; best feasible area_um2=30890; feasible ranges: data_width 13..27, n_iter 12..29, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 56 evals, 41 feasible; max throughput seen 96.1 MSPS; best accuracy 21.57 bits; best feasible area_um2=19909; feasible ranges: data_width 13..26, n_iter 12..30, angle_guard -1..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4680 in, 1079 out
- provider-reported cost: $0.0028
- full prompts and replies: `llm_trace.jsonl`

