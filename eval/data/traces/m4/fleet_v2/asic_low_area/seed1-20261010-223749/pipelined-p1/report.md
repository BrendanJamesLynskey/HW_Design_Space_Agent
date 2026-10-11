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
`pipelined_m:data_width=16,n_iter=15,angle_guard=-1,frac_guard=1,rounding=trunc,m=3` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 26570 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 7079 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 305 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 57 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 57 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 123 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.0326 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.0007 (2^-10.48) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 11.5 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.000169 (2^-12.53) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 2.76 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 10.5 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=15,angle_guard=-1,frac_guard=1,rounding=trunc,m=3` | 26570 | 305 | 57.0 | 7 | 0.0326 | 0.0007 (2^-10.48) | 10.48 |
| 1 | `pipelined_m:data_width=21,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc,m=5` | 31539 | 255 | 28.1 | 5 | 0.0327 | 6.67e-05 (2^-13.87) | 13.87 |
| 2 | `pipelined_m:data_width=20,n_iter=16,angle_guard=3,frac_guard=0,rounding=trunc,m=6` | 32032 | 246 | 22.7 | 5 | 0.0325 | 5.76e-05 (2^-14.08) | 14.08 |
| 3 | `pipelined_m:data_width=20,n_iter=18,angle_guard=2,frac_guard=0,rounding=trunc,m=8` | 35059 | 243 | 17.8 | 5 | 0.0342 | 4.23e-05 (2^-14.53) | 14.53 |
| 4 | `pipelined_m:data_width=20,n_iter=18,angle_guard=2,frac_guard=0,rounding=trunc,m=6` | 35059 | 243 | 23.6 | 5 | 0.0342 | 4.23e-05 (2^-14.53) | 14.53 |
| 5 | `pipelined_m:data_width=24,n_iter=18,angle_guard=-2,frac_guard=0,rounding=round,m=8` | 39233 | 274 | 16.5 | 5 | 0.0384 | 1.21e-05 (2^-16.33) | 16.33 |
| 6 | `pipelined_m:data_width=24,n_iter=18,angle_guard=2,frac_guard=0,rounding=round,m=8` | 41232 | 286 | 15.3 | 5 | 0.0402 | 8.55e-06 (2^-16.84) | 16.84 |
| 7 | `pipelined_m:data_width=25,n_iter=18,angle_guard=2,frac_guard=0,rounding=trunc,m=8` | 42776 | 297 | 14.8 | 5 | 0.0417 | 8.31e-06 (2^-16.88) | 16.88 |
| 8 | `pipelined_m:data_width=23,n_iter=21,angle_guard=3,frac_guard=1,rounding=trunc,m=6` | 49046 | 362 | 20.3 | 6 | 0.049 | 3.2e-06 (2^-18.25) | 18.25 |
| 9 | `pipelined_m:data_width=24,n_iter=20,angle_guard=2,frac_guard=3,rounding=round,m=4` | 53564 | 471 | 29.1 | 7 | 0.0577 | 2.42e-06 (2^-18.66) | 18.66 |
| 10 | `pipelined_m:data_width=26,n_iter=23,angle_guard=2,frac_guard=0,rounding=round,m=8` | 55307 | 308 | 14.3 | 5 | 0.0497 | 4.56e-07 (2^-21.06) | 21.06 |
| 11 | `pipelined_m:data_width=26,n_iter=23,angle_guard=2,frac_guard=3,rounding=round,m=5` | 64374 | 504 | 22.0 | 7 | 0.066 | 3.37e-07 (2^-21.50) | 21.50 |
| 12 | `pipelined_m:data_width=26,n_iter=23,angle_guard=3,frac_guard=3,rounding=round,m=2` | 79406 | 1156 | 52.7 | 14 | 0.111 | 3.04e-07 (2^-21.65) | 21.65 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-minimum with a loose throughput floor (>=1 MSPS) and a hard accuracy bound (max_abs_err <= 2^-10). Both of my families are 1-result/cycle, so throughput is simply Fmax, which is trivially satisfied at motor-control clock rates; the real trade-off is area vs accuracy_bits. Accuracy is identical across families for the same (data_width, n_iter, angle_guard, frac_guard, rounding), so I keep those ranges aligned and let n_iter (10..18) and data_width (12..28) span the accuracy/area curve, with the small guards as fine knobs. I split the budget 60/40 between pipelined (baseline, full register set) and pipelined_m (register-every-m, the main area-reduction mechanism). This covers the whole feasible trade-off curve: pipelined_m should claim the minimum-area corner (the selection point), while pipelined and higher n_iter/data_width points extend the front toward higher accuracy_bits, maximizing hypervolume against the reference (area 40000, accuracy 10).*)
- `pipelined` (36 evals): data_width=12..28, n_iter=10..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Full pipelining gives 1 result/cycle, so throughput is just Fmax. For a motor-control unit at >=1 MSPS, Fmax only needs to be ~1 MHz, which is trivially met even with wide datapaths. The binding constraint is max_abs_err <= 2^-10. Accuracy is set by n_iter (dominant), data_width, and the guards. I focus n_iter in 10..18 (10 is the classic minimum for ~2^-10 class accuracy, going higher buys accuracy_bits for the second objective at the cost of area). data_width 12..28 lets the optimizer find the minimum W that still meets the error bound while also exploring the accuracy_bits trade-off. angle_guard -2..2 and frac_guard 0..2 cover the small accuracy/area knobs. This is the primary family for the area-minimum corner.
- `pipelined_m` (24 evals): data_width=12..28, n_iter=10..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* pipelined_m registers every m stages, so it uses fewer flip-flops and less area than full pipelining for the same accuracy, while still delivering 1 result/cycle (throughput = Fmax, easily >= 1 MSPS). Since area is the primary objective and the throughput constraint is loose, pipelined_m with larger m is the natural area-reduction lever. I keep the same accuracy-relevant ranges as pipelined and add m in 2..8 to let the optimizer trade register count (area) against the slightly longer latency (ceil(N/m)+2, which is not a constraint here). This family should dominate the low-area end of the front.

**Result (code):** 60 evaluations this round, 60 total; 45 feasible; hypervolume 3.559e+04 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established and robust. The minimum area design (pipelined_m, area=26570 um^2) comfortably meets the throughput constraint (57 MSPS >= 1 MSPS) and the accuracy constraint (10.5 bits > 10 bits). The front extends to high accuracy (16.2 bits) with reasonable area (40768 um^2), covering the trade-off space effectively. Since this is the final round, we stop and select the design with minimum area from the front: pipelined_m [data_width=16 n_iter=15 angle_guard=-1 frac_guard=1 rounding=trunc m=3] with area_um2=26570.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 3.559e+04 (gain this round: n/a (first round)).
Feasible designs: 45 of 60 evaluations (38 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 156
- max_abs_err <= 0.000976562: 25% violate; best seen 1.31e-05 (2^-16.22)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=-1 frac_guard=1 rounding=trunc m=3] area_um2=26570, accuracy_bits=10.5, ffs=305, throughput_msps=57, max_abs_err=0.0007 (2^-10.48), power_index=0.0326
- pipelined_m [data_width=21 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=5] area_um2=31539, accuracy_bits=13.9, ffs=255, throughput_msps=28.1, max_abs_err=6.67e-05 (2^-13.87), power_index=0.0327
- pipelined_m [data_width=21 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=5] area_um2=32342, accuracy_bits=13.9, ffs=259, throughput_msps=27.1, max_abs_err=6.5e-05 (2^-13.91), power_index=0.0334
- pipelined_m [data_width=27 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc m=8] area_um2=38192, accuracy_bits=14, ffs=232, throughput_msps=13.9, max_abs_err=6.11e-05 (2^-14.00), power_index=0.0354
- pipelined_m [data_width=21 n_iter=18 angle_guard=1 frac_guard=2 rounding=round m=5] area_um2=40768, accuracy_bits=16.2, ffs=334, throughput_msps=27.1, max_abs_err=1.31e-05 (2^-16.22), power_index=0.0426
Front coverage: area_um2 26570..40768 (HV reference 40000); accuracy_bits 10.5..16.2 (HV reference 10); data_width on the front 16..27 (registry 8..28).

Per family:
- pipelined: 36 evals, 34 feasible; max throughput seen 156 MSPS; best accuracy 14.00 bits; best feasible area_um2=35509; feasible ranges: data_width 14..26, n_iter 12..18, angle_guard -2..2, frac_guard 0..2
- pipelined_m: 24 evals, 11 feasible; max throughput seen 96.1 MSPS; best accuracy 16.22 bits; best feasible area_um2=26570; feasible ranges: data_width 13..27, n_iter 13..18, angle_guard -2..2, frac_guard 0..2, m 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=15..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (5 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 83 feasible; hypervolume 4.042e+04 (+13.6%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and robust. The minimum area design (pipelined_m, area=26570 um^2) comfortably meets the throughput constraint (57 MSPS >= 1 MSPS) and the accuracy constraint (10.5 bits > 10 bits). The front extends to high accuracy (16.2 bits) with reasonable area (40768 um^2), covering the trade-off space effectively. Since this is the final round, we stop and select the design with minimum area from the front: pipelined_m [data_width=16 n_iter=15 angle_guard=-1 frac_guard=1 rounding=trunc m=3] with area_um2=26570.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 4.042e+04 (gain this round: +13.6%).
Feasible designs: 83 of 100 evaluations (73 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 156
- max_abs_err <= 0.000976562: 17% violate; best seen 3.04e-07 (2^-21.65)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=-1 frac_guard=1 rounding=trunc m=3] area_um2=26570, accuracy_bits=10.5, ffs=305, throughput_msps=57, max_abs_err=0.0007 (2^-10.48), power_index=0.0326
- pipelined_m [data_width=21 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc m=5] area_um2=31539, accuracy_bits=13.9, ffs=255, throughput_msps=28.1, max_abs_err=6.67e-05 (2^-13.87), power_index=0.0327
- pipelined_m [data_width=20 n_iter=18 angle_guard=2 frac_guard=0 rounding=trunc m=8] area_um2=35059, accuracy_bits=14.5, ffs=243, throughput_msps=17.8, max_abs_err=4.23e-05 (2^-14.53), power_index=0.0342
- pipelined_m [data_width=20 n_iter=18 angle_guard=2 frac_guard=0 rounding=trunc m=6] area_um2=35059, accuracy_bits=14.5, ffs=243, throughput_msps=23.6, max_abs_err=4.23e-05 (2^-14.53), power_index=0.0342
- pipelined_m [data_width=24 n_iter=18 angle_guard=-2 frac_guard=0 rounding=round m=8] area_um2=39233, accuracy_bits=16.3, ffs=274, throughput_msps=16.5, max_abs_err=1.21e-05 (2^-16.33), power_index=0.0384
- pipelined_m [data_width=25 n_iter=18 angle_guard=2 frac_guard=0 rounding=trunc m=8] area_um2=42776, accuracy_bits=16.9, ffs=297, throughput_msps=14.8, max_abs_err=8.31e-06 (2^-16.88), power_index=0.0417
- pipelined_m [data_width=23 n_iter=21 angle_guard=3 frac_guard=1 rounding=trunc m=6] area_um2=49046, accuracy_bits=18.3, ffs=362, throughput_msps=20.3, max_abs_err=3.2e-06 (2^-18.25), power_index=0.049
- pipelined_m [data_width=24 n_iter=20 angle_guard=2 frac_guard=3 rounding=round m=4] area_um2=53564, accuracy_bits=18.7, ffs=471, throughput_msps=29.1, max_abs_err=2.42e-06 (2^-18.66), power_index=0.0577
- pipelined_m [data_width=26 n_iter=23 angle_guard=2 frac_guard=3 rounding=round m=5] area_um2=64374, accuracy_bits=21.5, ffs=504, throughput_msps=22, max_abs_err=3.37e-07 (2^-21.50), power_index=0.066
- pipelined_m [data_width=26 n_iter=23 angle_guard=3 frac_guard=3 rounding=round m=2] area_um2=79406, accuracy_bits=21.6, ffs=1156, throughput_msps=52.7, max_abs_err=3.04e-07 (2^-21.65), power_index=0.111
Front coverage: area_um2 26570..79406 (HV reference 40000); accuracy_bits 10.5..21.6 (HV reference 10); data_width on the front 16..26 (registry 8..28).

Per family:
- pipelined: 36 evals, 34 feasible; max throughput seen 156 MSPS; best accuracy 14.00 bits; best feasible area_um2=35509; feasible ranges: data_width 14..26, n_iter 12..18, angle_guard -2..2, frac_guard 0..2
- pipelined_m: 64 evals, 49 feasible; max throughput seen 96.1 MSPS; best accuracy 21.65 bits; best feasible area_um2=26570; feasible ranges: data_width 13..27, n_iter 13..25, angle_guard -2..4, frac_guard 0..3, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4209 in, 1275 out
- provider-reported cost: $0.0023
- full prompts and replies: `llm_trace.jsonl`

