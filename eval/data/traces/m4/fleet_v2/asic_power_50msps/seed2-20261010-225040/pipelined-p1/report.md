# DSE run: asic_power_50msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_power_50msps: A 50 MSPS sin/cos unit in sky130 standard cells for a battery-powered radio: max error <= 2^-12. Minimise the relative power index; accuracy is the trade-off.
  target: asic-sky130hd
  constraint: throughput_msps >= 50
  constraint: max_abs_err <= 0.000244141
  objective: min power_index (HV ref 40)
  objective: max accuracy_bits (HV ref 12)
  select: min power_index
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=15,n_iter=17,angle_guard=3,frac_guard=3,rounding=round,m=3` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 33981 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 9053 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 385 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 54.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 8 | exact: schedule |
| latency_ns | 147 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.07 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000158 (2^-12.63) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 1.3 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 4.49e-05 (2^-14.44) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 0.368 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 12.6 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (8 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=17,angle_guard=3,frac_guard=3,rounding=round,m=3` | 33981 | 385 | 54.3 | 8 | 2.07 | 0.000158 (2^-12.63) | 12.63 |
| 1 | `pipelined_m:data_width=16,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=2` | 35249 | 509 | 78.8 | 10 | 2.45 | 0.000134 (2^-12.86) | 12.86 |
| 2 | `pipelined_m:data_width=18,n_iter=18,angle_guard=2,frac_guard=1,rounding=round,m=2` | 42403 | 611 | 72.3 | 11 | 2.95 | 5.02e-05 (2^-14.28) | 14.28 |
| 3 | `pipelined:data_width=18,n_iter=18,angle_guard=2,frac_guard=2,rounding=round` | 55909 | 1180 | 132.4 | 20 | 4.93 | 3.81e-05 (2^-14.68) | 14.68 |
| 4 | `pipelined:data_width=21,n_iter=17,angle_guard=2,frac_guard=4,rounding=trunc` | 61760 | 1321 | 111.3 | 19 | 5.49 | 1.83e-05 (2^-15.74) | 15.74 |
| 5 | `pipelined:data_width=23,n_iter=23,angle_guard=3,frac_guard=0,rounding=round` | 83633 | 1786 | 107.9 | 25 | 7.43 | 2.9e-06 (2^-18.39) | 18.39 |
| 6 | `pipelined:data_width=22,n_iter=23,angle_guard=3,frac_guard=3,rounding=round` | 87732 | 1844 | 111.3 | 25 | 7.71 | 1.66e-06 (2^-19.20) | 19.20 |
| 7 | `pipelined:data_width=24,n_iter=27,angle_guard=3,frac_guard=3,rounding=round` | 110794 | 2326 | 104.7 | 29 | 9.73 | 4.1e-07 (2^-21.22) | 21.22 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec needs throughput >= 50 MSPS, which for a 1-result/cycle architecture means Fmax >= 50 MHz, plus max_abs_err <= 2^-12. Both pipelined and pipelined_m produce one result per cycle, so they are the natural fit (iterative/unrolled_k would need Fmax >= 50*N and are not in my assigned set anyway). I split the 100-eval budget 50/50 between the two families. pipelined (m=1) is the safe, high-Fmax baseline that reliably clears the throughput constraint; pipelined_m (m=2..4) trades a longer per-stage path for fewer registers, targeting the low-power_index end of the front. I keep n_iter in 12..20 because N>=12 is the minimum to reach the 2^-12 accuracy floor and N>20 adds area/power with diminishing accuracy. data_width 14..18 gives 12..16 fractional output bits, enough to satisfy the error bound with small guard bits. angle_guard -2..2 and frac_guard 0..2 span the accuracy-vs-area knobs that shape the accuracy_bits objective. Rounding is fixed to 'round' since it only helps accuracy at negligible cost. This covers the full power-vs-accuracy trade-off curve so the hypervolume is maximized and the min-power feasible point is found.*)
- `pipelined` (30 evals): data_width=14..18, n_iter=12..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Fully pipelined gives 1 result/cycle, so throughput = Fmax. To hit 50 MSPS we need Fmax >= 50 MHz. N=12..20 keeps the per-stage logic (one micro-rotation) shallow enough for a high Fmax while N>=12 is the minimum to reach the 2^-12 accuracy floor. data_width 14..18 gives enough output precision (Q1.(W-2)) to keep max_abs_err <= 2^-12 with modest guard bits; W=14 already yields 12 fractional output bits. angle_guard -2..2 and frac_guard 0..2 cover the accuracy knobs that trade a few extra bits (area/power) against error. Rounding fixed to 'round' since it strictly improves accuracy at negligible cost and the spec wants accuracy as the trade-off axis. This is the primary family for the power-vs-accuracy front.
- `pipelined_m` (30 evals): data_width=14..18, n_iter=12..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m registers every m stages, so it still yields 1 result/cycle (throughput = Fmax) but with fewer pipeline registers than fully pipelined, lowering FF count and power_index at the cost of a longer combinational path per stage (m micro-rotations in series). m=2..4 keeps the per-stage path short enough to plausibly hold Fmax >= 50 MHz while cutting register area/power versus the m=1 case. Same data_width/n_iter/guard/rounding ranges as pipelined so the accuracy axis is comparable and the fronts merge cleanly. This family should expose the low-power corner of the front (fewer FFs, lower power_index) at slightly reduced Fmax margin, which is exactly the trade-off the spec wants mapped.

**Result (code):** 60 evaluations this round, 60 total; 33 feasible; hypervolume 99.03 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 7 distinct designs covering the trade-off space effectively. The minimum power_index achieved is 2.1 (pipelined_m, data_width=16, n_iter=14), which satisfies the throughput constraint (78.8 MSPS >= 50) and accuracy constraint (12.22 bits >= 12). The front extends to higher accuracy (14.7 bits) at the cost of power (4.93). The hypervolume of 99.03 indicates good coverage relative to the reference point (40, 12). Since this is the final round and the front clearly identifies the optimal design for the selection rule (min power_index) as the pipelined_m design with power_index=2.1, further exploration is unnecessary. The constraints are met, and the trade-off curve is mapped sufficiently to select the best design.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 99.03 (gain this round: n/a (first round)).
Feasible designs: 33 of 60 evaluations (25 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 13% violate; best seen 156
- max_abs_err <= 0.000244141: 40% violate; best seen 3.81e-05 (2^-14.68)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.1, accuracy_bits=12.2, area_um2=29925, ffs=437, throughput_msps=78.8, max_abs_err=0.000209 (2^-12.22)
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.34, accuracy_bits=12.4, area_um2=32695, ffs=495, throughput_msps=78.8, max_abs_err=0.00018 (2^-12.44)
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.38, accuracy_bits=12.5, area_um2=34177, ffs=495, throughput_msps=78.8, max_abs_err=0.000177 (2^-12.47)
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=2.41, accuracy_bits=12.5, area_um2=33716, ffs=509, throughput_msps=78.8, max_abs_err=0.000176 (2^-12.48)
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=2.45, accuracy_bits=12.9, area_um2=35249, ffs=509, throughput_msps=78.8, max_abs_err=0.000134 (2^-12.86)
- pipelined_m [data_width=18 n_iter=18 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.95, accuracy_bits=14.3, area_um2=42403, ffs=611, throughput_msps=72.3, max_abs_err=5.02e-05 (2^-14.28)
- pipelined [data_width=18 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] power_index=4.93, accuracy_bits=14.7, area_um2=55909, ffs=1180, throughput_msps=132, max_abs_err=3.81e-05 (2^-14.68)
Front coverage: power_index 2.1..4.93 (HV reference 40); accuracy_bits 12.2..14.7 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 30 evals, 22 feasible; max throughput seen 156 MSPS; best accuracy 14.68 bits; best feasible power_index=3.59; feasible ranges: data_width 17..18, n_iter 14..20, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 30 evals, 11 feasible; max throughput seen 86.6 MSPS; best accuracy 14.28 bits; best feasible power_index=2.1; feasible ranges: data_width 16..18, n_iter 14..20, angle_guard 2..2, frac_guard 1..2, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (35 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (6 front designs; box front_anchored)
- `pipelined` (5 evals): data_width=17..28, n_iter=16..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 45 feasible; hypervolume 309.3 (+212.3%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 7 distinct designs covering the trade-off space effectively. The minimum power_index achieved is 2.1 (pipelined_m, data_width=16, n_iter=14), which satisfies the throughput constraint (78.8 MSPS >= 50) and accuracy constraint (12.22 bits >= 12). The front extends to higher accuracy (14.7 bits) at the cost of power (4.93). The hypervolume of 99.03 indicates good coverage relative to the reference point (40, 12). Since this is the final round and the front clearly identifies the optimal design for the selection rule (min power_index) as the pipelined_m design with power_index=2.1, further exploration is unnecessary. The constraints are met, and the trade-off curve is mapped sufficiently to select the best design.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 309.3 (gain this round: +212.3%).
Feasible designs: 45 of 100 evaluations (33 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 29% violate; best seen 156
- max_abs_err <= 0.000244141: 35% violate; best seen 2.67e-07 (2^-21.84)

Pareto front (feasible, 8 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=15 n_iter=17 angle_guard=3 frac_guard=3 rounding=round m=3] power_index=2.07, accuracy_bits=12.6, area_um2=33981, ffs=385, throughput_msps=54.3, max_abs_err=0.000158 (2^-12.63)
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=2.45, accuracy_bits=12.9, area_um2=35249, ffs=509, throughput_msps=78.8, max_abs_err=0.000134 (2^-12.86)
- pipelined_m [data_width=18 n_iter=18 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.95, accuracy_bits=14.3, area_um2=42403, ffs=611, throughput_msps=72.3, max_abs_err=5.02e-05 (2^-14.28)
- pipelined [data_width=18 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] power_index=4.93, accuracy_bits=14.7, area_um2=55909, ffs=1180, throughput_msps=132, max_abs_err=3.81e-05 (2^-14.68)
- pipelined [data_width=21 n_iter=17 angle_guard=2 frac_guard=4 rounding=trunc] power_index=5.49, accuracy_bits=15.7, area_um2=61760, ffs=1321, throughput_msps=111, max_abs_err=1.83e-05 (2^-15.74)
- pipelined [data_width=23 n_iter=23 angle_guard=3 frac_guard=0 rounding=round] power_index=7.43, accuracy_bits=18.4, area_um2=83633, ffs=1786, throughput_msps=108, max_abs_err=2.9e-06 (2^-18.39)
- pipelined [data_width=22 n_iter=23 angle_guard=3 frac_guard=3 rounding=round] power_index=7.71, accuracy_bits=19.2, area_um2=87732, ffs=1844, throughput_msps=111, max_abs_err=1.66e-06 (2^-19.20)
- pipelined [data_width=24 n_iter=27 angle_guard=3 frac_guard=3 rounding=round] power_index=9.73, accuracy_bits=21.2, area_um2=110794, ffs=2326, throughput_msps=105, max_abs_err=4.1e-07 (2^-21.22)
Front coverage: power_index 2.07..9.73 (HV reference 40); accuracy_bits 12.6..21.2 (HV reference 12); data_width on the front 15..24 (registry 8..28).

Per family:
- pipelined: 35 evals, 26 feasible; max throughput seen 156 MSPS; best accuracy 21.22 bits; best feasible power_index=3.59; feasible ranges: data_width 17..24, n_iter 14..27, angle_guard 0..3, frac_guard 0..4
- pipelined_m: 65 evals, 19 feasible; max throughput seen 86.6 MSPS; best accuracy 21.84 bits; best feasible power_index=2.07; feasible ranges: data_width 15..18, n_iter 14..23, angle_guard 2..3, frac_guard 1..4, m 2..3
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4394 in, 1539 out
- provider-reported cost: $0.0026
- full prompts and replies: `llm_trace.jsonl`

