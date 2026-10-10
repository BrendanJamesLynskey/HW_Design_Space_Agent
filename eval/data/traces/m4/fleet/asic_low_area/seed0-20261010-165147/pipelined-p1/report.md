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

## Pareto front (9 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=12,angle_guard=4,frac_guard=0,rounding=round,m=4` | 19909 | 195 | 39.6 | 5 | 0.0226 | 0.000807 (2^-10.27) | 10.27 |
| 1 | `pipelined_m:data_width=15,n_iter=13,angle_guard=3,frac_guard=3,rounding=trunc,m=8` | 21713 | 144 | 21.3 | 4 | 0.0208 | 0.000439 (2^-11.15) | 11.15 |
| 2 | `pipelined_m:data_width=15,n_iter=13,angle_guard=3,frac_guard=3,rounding=trunc,m=7` | 21713 | 144 | 24.2 | 4 | 0.0208 | 0.000439 (2^-11.15) | 11.15 |
| 3 | `pipelined:data_width=16,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` | 34871 | 757 | 155.9 | 16 | 0.0626 | 0.0004 (2^-11.29) | 11.29 |
| 4 | `pipelined_m:data_width=15,n_iter=24,angle_guard=3,frac_guard=3,rounding=trunc,m=7` | 41241 | 263 | 24.2 | 6 | 0.039 | 0.000341 (2^-11.52) | 11.52 |
| 5 | `pipelined:data_width=16,n_iter=14,angle_guard=4,frac_guard=4,rounding=trunc` | 42175 | 906 | 132.4 | 16 | 0.0752 | 0.000197 (2^-12.31) | 12.31 |
| 6 | `pipelined_m:data_width=15,n_iter=25,angle_guard=4,frac_guard=4,rounding=round,m=3` | 52627 | 590 | 51.9 | 11 | 0.0638 | 0.000114 (2^-13.10) | 13.10 |
| 7 | `pipelined_m:data_width=23,n_iter=20,angle_guard=-1,frac_guard=4,rounding=trunc,m=2` | 58885 | 853 | 56.1 | 12 | 0.0821 | 7.35e-06 (2^-17.05) | 17.05 |
| 8 | `pipelined_m:data_width=26,n_iter=24,angle_guard=3,frac_guard=2,rounding=trunc,m=7` | 62691 | 409 | 15.8 | 6 | 0.0597 | 3.21e-07 (2^-21.57) | 21.57 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Both pipelined and pipelined_m guarantee 1 result/cycle, easily satisfying >=1 MSPS. n_iter=10 yields ~10-bit accuracy (max_abs_err ~2^-10), meeting the <=2^-10 constraint. data_width 10-16 and small guards keep area low while preserving accuracy. pipelined_m may offer lower area due to fewer pipeline registers at the same throughput. Split budget evenly to map both fronts.*)
- `pipelined` (30 evals): data_width=10..16, n_iter=10..16, angle_guard=-2..1, frac_guard=0..2, rounding=trunc|round. *Why:* Full pipelining (1 result/cycle) is required to easily meet >=1 MSPS with modest area. n_iter=10 gives ~10-bit accuracy (2^-10), meeting the error constraint with margin. data_width 10-16 balances area vs accuracy. angle_guard -2..1 and frac_guard 0..2 explore guard-bit trade-offs for area minimization.
- `pipelined_m` (30 evals): data_width=10..16, n_iter=10..16, angle_guard=-2..1, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m with m=2..4 reduces register count vs fully pipelined while still achieving 1 result/cycle throughput. Lower area at similar accuracy makes it competitive for the min-area objective. Same width/iter/guard ranges as pipelined for consistency.

**Result (code):** 60 evaluations this round, 60 total; 20 feasible; hypervolume 1.612e+04 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 5 distinct designs spanning the required trade-off space. The minimum area design (pipelined_m, 22096 um^2) significantly beats the hypervolume reference point (40000 um^2) while meeting the accuracy constraint (10.2 bits > 10 bits reference, max_abs_err 0.000879 < 0.000976562). The front covers accuracy from 10.2 to 11.4 bits and area from 22096 to 42271 um^2, providing a clear trade-off curve. Both pipelined and pipelined_m families have been explored, with pipelined_m yielding the best area efficiency. The selection rule (min area) clearly points to the 22096 um^2 design. Since this is the final round, stopping is appropriate as the front adequately maps the feasible region and the optimal design per the selection rule has been identified.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.612e+04 (gain this round: n/a (first round)).
Feasible designs: 20 of 60 evaluations (15 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 213
- max_abs_err <= 0.000976562: 67% violate; best seen 0.000369 (2^-11.40)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=15 n_iter=13 angle_guard=0 frac_guard=0 rounding=round m=3] area_um2=22096, accuracy_bits=10.2, ffs=285, throughput_msps=63.2, max_abs_err=0.000879 (2^-10.15), power_index=0.0289
- pipelined_m [data_width=15 n_iter=13 angle_guard=1 frac_guard=0 rounding=round m=2] area_um2=24825, accuracy_bits=10.5, ffs=394, throughput_msps=86.6, max_abs_err=0.000673 (2^-10.54), power_index=0.0365
- pipelined_m [data_width=15 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=2] area_um2=28006, accuracy_bits=11.1, ffs=418, throughput_msps=82.5, max_abs_err=0.000462 (2^-11.08), power_index=0.0397
- pipelined [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] area_um2=34871, accuracy_bits=11.3, ffs=757, throughput_msps=156, max_abs_err=0.0004 (2^-11.29), power_index=0.0626
- pipelined [data_width=16 n_iter=16 angle_guard=0 frac_guard=1 rounding=round] area_um2=42271, accuracy_bits=11.4, ffs=895, throughput_msps=149, max_abs_err=0.000369 (2^-11.40), power_index=0.0746
Front coverage: area_um2 22096..42271 (HV reference 40000); accuracy_bits 10.2..11.4 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- pipelined: 30 evals, 12 feasible; max throughput seen 213 MSPS; best accuracy 11.40 bits; best feasible area_um2=29168; feasible ranges: data_width 15..16, n_iter 12..16, angle_guard -1..0, frac_guard 0..2
- pipelined_m: 30 evals, 8 feasible; max throughput seen 108 MSPS; best accuracy 11.08 bits; best feasible area_um2=22096; feasible ranges: data_width 15..16, n_iter 13..16, angle_guard 0..1, frac_guard 0..2, m 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (24 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (3 front designs; box front_anchored)
- `pipelined` (16 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 57 feasible; hypervolume 2.227e+04 (+38.1%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 5 distinct designs spanning the required trade-off space. The minimum area design (pipelined_m, 22096 um^2) significantly beats the hypervolume reference point (40000 um^2) while meeting the accuracy constraint (10.2 bits > 10 bits reference, max_abs_err 0.000879 < 0.000976562). The front covers accuracy from 10.2 to 11.4 bits and area from 22096 to 42271 um^2, providing a clear trade-off curve. Both pipelined and pipelined_m families have been explored, with pipelined_m yielding the best area efficiency. The selection rule (min area) clearly points to the 22096 um^2 design. Since this is the final round, stopping is appropriate as the front adequately maps the feasible region and the optimal design per the selection rule has been identified.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 2.227e+04 (gain this round: +38.1%).
Feasible designs: 57 of 100 evaluations (47 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 213
- max_abs_err <= 0.000976562: 43% violate; best seen 3.21e-07 (2^-21.57)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=15 n_iter=12 angle_guard=4 frac_guard=0 rounding=round m=4] area_um2=19909, accuracy_bits=10.3, ffs=195, throughput_msps=39.6, max_abs_err=0.000807 (2^-10.27), power_index=0.0226
- pipelined_m [data_width=15 n_iter=13 angle_guard=3 frac_guard=3 rounding=trunc m=8] area_um2=21713, accuracy_bits=11.2, ffs=144, throughput_msps=21.3, max_abs_err=0.000439 (2^-11.15), power_index=0.0208
- pipelined_m [data_width=15 n_iter=13 angle_guard=3 frac_guard=3 rounding=trunc m=7] area_um2=21713, accuracy_bits=11.2, ffs=144, throughput_msps=24.2, max_abs_err=0.000439 (2^-11.15), power_index=0.0208
- pipelined [data_width=16 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] area_um2=34871, accuracy_bits=11.3, ffs=757, throughput_msps=156, max_abs_err=0.0004 (2^-11.29), power_index=0.0626
- pipelined_m [data_width=15 n_iter=24 angle_guard=3 frac_guard=3 rounding=trunc m=7] area_um2=41241, accuracy_bits=11.5, ffs=263, throughput_msps=24.2, max_abs_err=0.000341 (2^-11.52), power_index=0.039
- pipelined [data_width=16 n_iter=14 angle_guard=4 frac_guard=4 rounding=trunc] area_um2=42175, accuracy_bits=12.3, ffs=906, throughput_msps=132, max_abs_err=0.000197 (2^-12.31), power_index=0.0752
- pipelined_m [data_width=15 n_iter=25 angle_guard=4 frac_guard=4 rounding=round m=3] area_um2=52627, accuracy_bits=13.1, ffs=590, throughput_msps=51.9, max_abs_err=0.000114 (2^-13.10), power_index=0.0638
- pipelined_m [data_width=23 n_iter=20 angle_guard=-1 frac_guard=4 rounding=trunc m=2] area_um2=58885, accuracy_bits=17.1, ffs=853, throughput_msps=56.1, max_abs_err=7.35e-06 (2^-17.05), power_index=0.0821
- pipelined_m [data_width=26 n_iter=24 angle_guard=3 frac_guard=2 rounding=trunc m=7] area_um2=62691, accuracy_bits=21.6, ffs=409, throughput_msps=15.8, max_abs_err=3.21e-07 (2^-21.57), power_index=0.0597
Front coverage: area_um2 19909..62691 (HV reference 40000); accuracy_bits 10.3..21.6 (HV reference 10); data_width on the front 15..26 (registry 8..28).

Per family:
- pipelined: 46 evals, 27 feasible; max throughput seen 213 MSPS; best accuracy 18.96 bits; best feasible area_um2=29168; feasible ranges: data_width 15..27, n_iter 12..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 54 evals, 30 feasible; max throughput seen 108 MSPS; best accuracy 21.57 bits; best feasible area_um2=19909; feasible ranges: data_width 15..26, n_iter 12..30, angle_guard -1..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4199 in, 1019 out
- provider-reported cost: $0.0039
- full prompts and replies: `llm_trace.jsonl`

