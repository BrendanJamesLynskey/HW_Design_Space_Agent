# DSE run: asic_low_area

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 27 of 27 budgeted, over 2 round(s).  
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
  budget: 27 evals, 27/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined:data_width=16,n_iter=13,angle_guard=1,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 32882 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 8760 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 716 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 149 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 149 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 15 | exact: schedule |
| latency_ns | 100 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.0592 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000417 (2^-11.23) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 6.83 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 0.00012 (2^-13.03) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 1.96 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 11.2 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (5 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=16,n_iter=13,angle_guard=1,frac_guard=0,rounding=round` | 32882 | 716 | 149.3 | 15 | 0.0592 | 0.000417 (2^-11.23) | 11.23 |
| 1 | `pipelined:data_width=16,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 35509 | 771 | 149.3 | 16 | 0.0638 | 0.000342 (2^-11.51) | 11.51 |
| 2 | `pipelined:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 37422 | 812 | 143.2 | 16 | 0.0672 | 0.000204 (2^-12.26) | 12.26 |
| 3 | `pipelined:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 39336 | 853 | 137.6 | 16 | 0.0706 | 0.000175 (2^-12.48) | 12.48 |
| 4 | `pipelined:data_width=17,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 42962 | 928 | 143.2 | 18 | 0.0769 | 0.000149 (2^-12.71) | 12.71 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=1 MSPS throughput, which only pipelined and pipelined_m can meet (1 result/cycle). The fleet facts confirm that iterative (best area 7405) and unrolled_k (best area 12183) cannot meet the throughput constraint, so they are irrelevant for this spec. My job is to find the minimum-area design within pipelined/pipelined_m that satisfies max_abs_err <= 2^-10. The key trade-off is: lower data_width and n_iter reduce area but hurt accuracy; higher values improve accuracy but increase area. I'll focus on the narrow band where accuracy just meets the 2^-10 constraint, with minimal guard bits to save area. pipelined_m with m>1 should reduce area vs fully pipelined by having fewer registers, so I'll allocate budget to both to map the front. The 27-eval budget is split 55/45 between the two families to explore both the fully-pipelined baseline and the partially-pipelined variants.*)
- `pipelined` (9 evals): data_width=12..14, n_iter=10..14, angle_guard=0..1, frac_guard=0..1, rounding=trunc|round. *Why:* pipelined is the only family that can plausibly meet the >=1 MSPS throughput constraint (1 result/cycle) while keeping area low. The fleet facts show pipelined's best feasible area is 43004 um^2, far above iterative's 7405, but iterative cannot meet the throughput constraint. To minimize area within pipelined, I need to find the minimum n_iter that satisfies max_abs_err <= 2^-10 (0.000976562). With data_width=12, the output LSB is 2^-10, so the quantization alone is at the limit; n_iter must be large enough that the CORDIC residual error plus quantization stays under 2^-10. I'll focus on data_width 12-14 (lower width = less area, but must still meet accuracy), n_iter 10-14 (enough iterations for 2^-10 accuracy), and minimal guards (angle_guard 0-1, frac_guard 0-1) to reduce area. Rounding=round helps accuracy at the same n_iter.
- `pipelined_m` (7 evals): data_width=12..14, n_iter=10..14, angle_guard=0..1, frac_guard=0..1, rounding=trunc|round, m=2..4. *Why:* pipelined_m registers every m stages, reducing flip-flops and area compared to fully pipelined while still achieving 1 result/cycle throughput. The fleet facts show pipelined_m's best feasible area is 42489 um^2, slightly better than pipelined's 43004. By using m=2-4, we can reduce the number of pipeline registers (and thus FFs and area) while maintaining throughput. The same accuracy constraints apply: data_width 12-14, n_iter 10-14, minimal guards. This family may find a lower-area point on the Pareto front by trading some latency (ceil(N/m)+2 cycles) for fewer registers.

**Result (code):** 16 evaluations this round, 16 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `refine` — The primary blocker is accuracy: the best design so far (pipelined, W=14, N=12, angle_guard=1, round) achieves only 9.47 bits (max_abs_err=0.00141), which is 44.3% above the 2^-10 limit. Throughput is not a constraint (best seen 180 MSPS vs 1 MSPS required). To reach 2^-10 accuracy, we need to increase the effective precision. This can be done by increasing data_width (W) and/or n_iter (N). The current search focused on W=14 and N=11-13. We need to explore higher W (e.g., 16-18) and higher N (e.g., 14-16) to push accuracy below 2^-10. Since area is the objective, we want the minimum W and N that satisfy accuracy. I will refine the ranges to focus on W=15-18 and N=13-16 for the pipelined family, which offers the best throughput/area trade-off for this spec. I will also keep angle_guard=1 and rounding=round as they showed the best accuracy in the previous round.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 16 of 27.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 16 evaluations (0 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 180
- max_abs_err <= 0.000976562: 100% violate; best seen 0.00141 (2^-9.47)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=14 n_iter=12 angle_guard=1 frac_guard=0 rounding=round]: throughput=163, max_abs_err=0.00141 (2^-9.47); max_abs_err <= 0.000976562 violated by 44.3%
- pipelined [data_width=14 n_iter=13 angle_guard=0 frac_guard=0 rounding=round]: throughput=171, max_abs_err=0.00181 (2^-9.11); max_abs_err <= 0.000976562 violated by 85.4%
- pipelined [data_width=14 n_iter=12 angle_guard=0 frac_guard=0 rounding=round]: throughput=171, max_abs_err=0.00194 (2^-9.01); max_abs_err <= 0.000976562 violated by 99.2%
- pipelined [data_width=14 n_iter=11 angle_guard=1 frac_guard=0 rounding=trunc]: throughput=163, max_abs_err=0.0022 (2^-8.83); max_abs_err <= 0.000976562 violated by 125.5%
- pipelined [data_width=14 n_iter=11 angle_guard=0 frac_guard=0 rounding=trunc]: throughput=171, max_abs_err=0.00244 (2^-8.68); max_abs_err <= 0.000976562 violated by 149.9%

Per family:
- pipelined: 9 evals, 0 feasible; max throughput seen 180 MSPS; best accuracy 9.47 bits
- pipelined_m: 7 evals, 0 feasible; max throughput seen 108 MSPS; best accuracy 8.68 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Refine to higher W and N to meet accuracy constraint.*)
- `pipelined` (11 evals): data_width=15..18, n_iter=13..16, angle_guard=1..1, frac_guard=0..0, rounding=round. *Why:* Focus on increasing W and N to meet the 2^-10 accuracy constraint while keeping area minimal. Pipelined is preferred for its high throughput and regular structure.

**Result (code):** 11 evaluations this round, 27 total; 11 feasible; hypervolume 1.21e+04 (+inf).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 5 distinct designs covering the trade-off between area (32882-42962 um^2) and accuracy (11.2-12.7 bits). The minimum area design (pipelined, data_width=16, n_iter=13) meets all constraints: throughput 149 MSPS >= 1 MSPS and max_abs_err 0.000417 <= 0.000976562. The hypervolume is 1.21e+04, which is substantial relative to the reference point. Since this is the final round (budget exhausted: 27/27 evals used), no further exploration is possible. The front adequately maps the feasible region for the spec's objectives, and the selection rule (min area) clearly points to the 32882 um^2 design.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 27 of 27.
Hypervolume of the feasible front: 1.21e+04 (gain this round: +inf (first feasible designs)).
Feasible designs: 11 of 27 evaluations (7 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 180
- max_abs_err <= 0.000976562: 59% violate; best seen 0.000149 (2^-12.71)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=16 n_iter=13 angle_guard=1 frac_guard=0 rounding=round] area_um2=32882, accuracy_bits=11.2, ffs=716, throughput_msps=149, max_abs_err=0.000417 (2^-11.23), power_index=0.0592
- pipelined [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=35509, accuracy_bits=11.5, ffs=771, throughput_msps=149, max_abs_err=0.000342 (2^-11.51), power_index=0.0638
- pipelined [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=37422, accuracy_bits=12.3, ffs=812, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=0.0672
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=39336, accuracy_bits=12.5, ffs=853, throughput_msps=138, max_abs_err=0.000175 (2^-12.48), power_index=0.0706
- pipelined [data_width=17 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=42962, accuracy_bits=12.7, ffs=928, throughput_msps=143, max_abs_err=0.000149 (2^-12.71), power_index=0.0769
Front coverage: area_um2 32882..42962 (HV reference 40000); accuracy_bits 11.2..12.7 (HV reference 10); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 20 evals, 11 feasible; max throughput seen 180 MSPS; best accuracy 12.71 bits; best feasible area_um2=32882; feasible ranges: data_width 15..18, n_iter 13..16, angle_guard 1..1, frac_guard 0..0
- pipelined_m: 7 evals, 0 feasible; max throughput seen 108 MSPS; best accuracy 8.68 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 6571 in, 1825 out
- provider-reported cost: $0.0044
- full prompts and replies: `llm_trace.jsonl`

