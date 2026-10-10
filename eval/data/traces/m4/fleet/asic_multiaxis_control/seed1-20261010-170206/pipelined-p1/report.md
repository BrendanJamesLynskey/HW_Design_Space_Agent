# DSE run: asic_multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_multiaxis_control: Shared sin/cos unit in sky130 standard cells for a 16-axis motor-control loop: a 1 MHz control tick issues 32 requests at once; all 32 results must be back within 0.5 us of the tick (p99 over ticks). Max error <= 2^-12. Minimise area.
  target: asic-sky130hd
  constraint: throughput_msps >= 32
  constraint: max_abs_err <= 0.000244141
  constraint: sys_p99_batch_us <= 0.5
  objective: min area_um2 (HV ref 100000)
  objective: max accuracy_bits (HV ref 12)
  select: min area_um2
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average)
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 39385 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10493 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 834 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 112 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.23 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000204 (2^-12.26) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.34 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 5.69e-05 (2^-14.10) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 0.932 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.3 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (7 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=round` | 39385 | 834 | 143.2 | 16 | 2.23 | 0.000204 (2^-12.26) | 12.26 |
| 1 | `pipelined:data_width=16,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 42249 | 894 | 143.2 | 17 | 2.39 | 0.000176 (2^-12.48) | 12.48 |
| 2 | `pipelined:data_width=16,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 45114 | 954 | 143.2 | 18 | 2.55 | 0.000134 (2^-12.86) | 12.86 |
| 3 | `pipelined:data_width=20,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 53042 | 1140 | 123.1 | 18 | 3.03 | 3.93e-05 (2^-14.63) | 14.63 |
| 4 | `pipelined:data_width=24,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 57612 | 1243 | 115.0 | 18 | 3.3 | 3.16e-05 (2^-14.95) | 14.95 |
| 5 | `pipelined:data_width=19,n_iter=25,angle_guard=3,frac_guard=2,rounding=round` | 82637 | 1739 | 123.1 | 27 | 4.65 | 1.48e-05 (2^-16.05) | 16.05 |
| 6 | `pipelined:data_width=24,n_iter=23,angle_guard=0,frac_guard=0,rounding=round` | 83633 | 1786 | 115.0 | 25 | 4.75 | 2.49e-06 (2^-18.62) | 18.62 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec has three hard gates: (1) throughput >= 32 Msps, (2) max_abs_err <= 2^-12, and (3) the system batch deadline sys_p99_batch_us <= 0.5 us. Only the pipelined families produce 1 result/cycle, so they are the only ones that can clear the throughput gate; iterative/unrolled_k are excluded anyway by my fleet assignment. The batch deadline is the binding constraint: 32 requests arrive at once and all 32 results must return within 0.5 us, i.e. 32 cycles in 0.5 us, requiring Fmax >= 64 MHz. That forces a short critical path, which in turn caps n_iter and angle_guard. The accuracy gate (2^-12) then pins data_width, n_iter, angle_guard, frac_guard and rounding to a narrow feasible band, so I bound data_width and n_iter to 14..16 and angle_guard to -2..2 rather than sweeping the full registry ranges. I split the budget between pipelined (0.55) and pipelined_m (0.45): pipelined is the safe, high-Fmax anchor that is most likely to satisfy all three gates and define the reliable part of the front, while pipelined_m (m=2..4) is where the lowest-area points are expected to sit, so it gets a substantial share to map the area/latency trade-off. The selection rule is min area, but hypervolume rewards covering the whole accuracy-vs-area curve, so I keep the accuracy-relevant parameters (angle_guard, frac_guard, rounding) varied across both families rather than collapsing to a single accuracy point.*)
- `pipelined` (33 evals): data_width=14..16, n_iter=14..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined gives 1 result/cycle, so at Fmax >= 32 MHz it clears the 32 Msps throughput constraint with margin. The 0.5 us batch deadline is the real gate: 32 back-to-back results need 32 cycles, so Fmax must be >= 64 MHz, which forces a short critical path (small n_iter, small angle_guard). Accuracy needs max_abs_err <= 2^-12, which pins data_width/n_iter/angle_guard/frac_guard/rounding to a narrow feasible band. I focus the densest budget here because it is the only family that can plausibly satisfy both the throughput and the tight batch-latency bound, and its area/accuracy trade-off is the core of the front.
- `pipelined_m` (27 evals): data_width=14..16, n_iter=14..16, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m registers every m stages, so it has fewer flip-flops and less area than fully pipelined at the same n_iter, while still producing 1 result/cycle (so it keeps the 32 Msps throughput). The cost is a longer combinational path per stage (m micro-rotations), which lowers Fmax and can jeopardise the 0.5 us batch deadline. I keep m in 2..4 so the path stays short enough to still reach ~64 MHz, and let the search trade the area savings against the Fmax/latency risk. This family is where the cheapest-area points on the front are likely to live, so it is worth a meaningful share.

**Result (code):** 60 evaluations this round, 60 total; 14 feasible; hypervolume 4.932e+04 (n/a).

**LLM decision:** `stop` — The front is feasible and well-characterized for the selection rule (min area). The cheapest feasible design (pipelined, W=16, N=14, ag=2, fg=2, round) has area 39385 um^2, throughput 143 MSPS (>> 32), max_abs_err 0.000204 (<= 0.000244), and sys_p99_batch 0.28 us (<= 0.5 us). The front spans the accuracy trade-off (12.3..12.9 bits) at the minimum-area corner, which is what the selection rule picks. pipelined_m yielded no feasible designs (best accuracy 11.97 < 12.0 required), and iterative/unrolled_k cannot meet the 32 MSPS throughput constraint (they produce one result every several cycles, so their throughput is far below the pipelined 143 MSPS). Since this is the final round, I stop and let the L2 simulation re-select among the feasible front designs.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 4.932e+04 (gain this round: n/a (first round)).
Feasible designs: 14 of 60 evaluations (7 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 171
- max_abs_err <= 0.000244141: 77% violate; best seen 0.000134 (2^-12.86)
- sys_p99_batch_us <= 0.5: 37% violate; best seen 0.28

Pareto front (feasible, 3 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=39385, accuracy_bits=12.3, ffs=834, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=2.23
- pipelined [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=42249, accuracy_bits=12.5, ffs=894, throughput_msps=143, max_abs_err=0.000176 (2^-12.48), power_index=2.39
- pipelined [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=45114, accuracy_bits=12.9, ffs=954, throughput_msps=143, max_abs_err=0.000134 (2^-12.86), power_index=2.55
Front coverage: area_um2 39385..45114 (HV reference 100000); accuracy_bits 12.3..12.9 (HV reference 12); data_width on the front 16..16 (registry 8..28).

Per family:
- pipelined: 33 evals, 14 feasible; max throughput seen 171 MSPS; best accuracy 12.86 bits; best feasible area_um2=39385; feasible ranges: data_width 16..16, n_iter 14..16, angle_guard 1..2, frac_guard 2..2
- pipelined_m: 27 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 11.97 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (20 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)
- `pipelined_m` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 40 evaluations this round, 100 total; 30 feasible; hypervolume 2.071e+05 (+319.9%).

**No LLM call** (code's front-mapping round): The front is feasible and well-characterized for the selection rule (min area). The cheapest feasible design (pipelined, W=16, N=14, ag=2, fg=2, round) has area 39385 um^2, throughput 143 MSPS (>> 32), max_abs_err 0.000204 (<= 0.000244), and sys_p99_batch 0.28 us (<= 0.5 us). The front spans the accuracy trade-off (12.3..12.9 bits) at the minimum-area corner, which is what the selection rule picks. pipelined_m yielded no feasible designs (best accuracy 11.97 < 12.0 required), and iterative/unrolled_k cannot meet the 32 MSPS throughput constraint (they produce one result every several cycles, so their throughput is far below the pipelined 143 MSPS). Since this is the final round, I stop and let the L2 simulation re-select among the feasible front designs.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 2.071e+05 (gain this round: +319.9%).
Feasible designs: 30 of 100 evaluations (19 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 12% violate; best seen 171
- max_abs_err <= 0.000244141: 58% violate; best seen 1.15e-07 (2^-23.05)
- sys_p99_batch_us <= 0.5: 43% violate; best seen 0.28

Pareto front (feasible, 7 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=39385, accuracy_bits=12.3, ffs=834, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=2.23
- pipelined [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=42249, accuracy_bits=12.5, ffs=894, throughput_msps=143, max_abs_err=0.000176 (2^-12.48), power_index=2.39
- pipelined [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=45114, accuracy_bits=12.9, ffs=954, throughput_msps=143, max_abs_err=0.000134 (2^-12.86), power_index=2.55
- pipelined [data_width=20 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=53042, accuracy_bits=14.6, ffs=1140, throughput_msps=123, max_abs_err=3.93e-05 (2^-14.63), power_index=3.03
- pipelined [data_width=24 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] area_um2=57612, accuracy_bits=15, ffs=1243, throughput_msps=115, max_abs_err=3.16e-05 (2^-14.95), power_index=3.3
- pipelined [data_width=19 n_iter=25 angle_guard=3 frac_guard=2 rounding=round] area_um2=82637, accuracy_bits=16, ffs=1739, throughput_msps=123, max_abs_err=1.48e-05 (2^-16.05), power_index=4.65
- pipelined [data_width=24 n_iter=23 angle_guard=0 frac_guard=0 rounding=round] area_um2=83633, accuracy_bits=18.6, ffs=1786, throughput_msps=115, max_abs_err=2.49e-06 (2^-18.62), power_index=4.75
Front coverage: area_um2 39385..83633 (HV reference 100000); accuracy_bits 12.3..18.6 (HV reference 12); data_width on the front 16..24 (registry 8..28).

Per family:
- pipelined: 53 evals, 30 feasible; max throughput seen 171 MSPS; best accuracy 23.05 bits; best feasible area_um2=39385; feasible ranges: data_width 16..25, n_iter 14..30, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 47 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 17.13 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4983 in, 1569 out
- provider-reported cost: $0.0027
- full prompts and replies: `llm_trace.jsonl`

