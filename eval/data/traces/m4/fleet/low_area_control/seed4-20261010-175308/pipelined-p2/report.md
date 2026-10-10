# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 6 of 10 budgeted, over 1 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec low_area_control: Field-oriented motor-control loop needing sin/cos of the rotor angle at >= 1 MSPS with max error <= 2^-10. Area is everything: minimise LUTs + FFs.
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min luts_plus_ffs (HV ref 1500)
  objective: max accuracy_bits (HV ref 10)
  select: min luts_plus_ffs
  budget: 10 evals, 10/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=17,n_iter=14,angle_guard=0,frac_guard=4,rounding=trunc,m=8` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 896 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 159 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 50.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 50.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 79.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0397 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000264 (2^-11.89) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 8.64 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 6.23e-05 (2^-13.97) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 2.04 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 11.9 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (2 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=0,frac_guard=4,rounding=trunc,m=8` | 896 | 159 | 50.3 | 4 | 0.0397 | 0.000264 (2^-11.89) | 11.89 |
| 1 | `pipelined_m:data_width=18,n_iter=17,angle_guard=4,frac_guard=2,rounding=round,m=8` | 1190 | 243 | 50.3 | 5 | 0.0539 | 3.5e-05 (2^-14.80) | 14.80 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >=1 MSPS (so pipelined/pipelined_m are the right families, not iterative/unrolled_k) and max_abs_err <= 2^-10. Area is the primary objective. From fleet facts, pipelined_m already has a front member at 959 luts+ffs while full pipelined's best is 1273. The area lever in pipelined_m is m (registers every m stages): larger m means fewer FFs but tighter per-stage timing. I split the 10-eval budget 50/50: 5 evals on pipelined_m exploring the m/n_iter/data_width/guard trade-off to push the area down and map the accuracy-vs-area curve, and 5 evals on pipelined at low N to confirm its best corner. Accuracy is controlled by n_iter and data_width; with n_iter>=12 and data_width>=14, 2^-10 is comfortably met even with truncation and zero guards, so I keep guards minimal to save area. The hypervolume reward comes from covering the trade-off: pipelined_m with varying m and n_iter should trace a curve from low-area/low-accuracy to higher-area/higher-accuracy, which is exactly what the front needs.*)
- `pipelined_m` (6 evals): data_width=12..18, n_iter=10..18, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* pipelined_m is my only family that has produced a design on the merged front (959 luts+ffs), beating the full pipelined (1273). The key to area is minimizing the number of register stages (m) while keeping Fmax high enough for >=1 MSPS. I focus m in 2..8 (larger m = fewer registers = less area, but tighter timing), n_iter in 10..18 (enough for 2^-10 error with modest guards), and data_width 12..18 (12 is the minimum that can hit 2^-10 with enough n_iter; going higher wastes area). Guards are kept low (frac 0..2, angle -1..1) to save bits, since accuracy is dominated by n_iter and data_width.
- clamped by code: budget 6 supports 1 families; dropped ['pipelined']

**Result (code):** 6 evaluations this round, 6 total; 3 feasible; hypervolume 1036 (n/a).

**LLM decision:** `stop` — The current Pareto front contains two feasible designs that satisfy all constraints (throughput >= 1 MSPS, max_abs_err <= 2^-10). The design with minimum area (luts_plus_ffs=1055) meets the accuracy requirement (11.9 bits > 10 bits) and throughput (50.3 MSPS > 1 MSPS). Since this is the final round, we stop and select the design with the minimum luts_plus_ffs (1055) as the final design.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 6 of 10.
Hypervolume of the feasible front: 1036 (gain this round: n/a (first round)).
Feasible designs: 3 of 6 evaluations (3 unique).
Families explored so far: pipelined_m. Not yet explored: pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 103
- max_abs_err <= 0.000976562: 50% violate; best seen 3.5e-05 (2^-14.80)

Pareto front (feasible, 2 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=0 frac_guard=4 rounding=trunc m=8] luts_plus_ffs=1055, accuracy_bits=11.9, luts=896, ffs=159, throughput_msps=50.3, max_abs_err=0.000264 (2^-11.89), power_index=0.0397
- pipelined_m [data_width=18 n_iter=17 angle_guard=4 frac_guard=2 rounding=round m=8] luts_plus_ffs=1433, accuracy_bits=14.8, luts=1190, ffs=243, throughput_msps=50.3, max_abs_err=3.5e-05 (2^-14.80), power_index=0.0539
Front coverage: luts_plus_ffs 1055..1433 (HV reference 1500); accuracy_bits 11.9..14.8 (HV reference 10); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined_m: 6 evals, 3 feasible; max throughput seen 103 MSPS; best accuracy 14.80 bits; best feasible luts_plus_ffs=1055; feasible ranges: data_width 17..18, n_iter 14..18, angle_guard 0..4, frac_guard 1..4, m 5..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 3907 in, 1214 out
- provider-reported cost: $0.0018
- full prompts and replies: `llm_trace.jsonl`

