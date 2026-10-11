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
`pipelined:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 38197 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10176 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 810 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 112 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.16 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000209 (2^-12.22) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.43 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 6.44e-05 (2^-13.92) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 1.06 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.2 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (10 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` | 38197 | 810 | 143.2 | 16 | 2.16 | 0.000209 (2^-12.22) | 12.22 |
| 1 | `pipelined:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=round` | 39385 | 834 | 143.2 | 16 | 2.23 | 0.000204 (2^-12.26) | 12.26 |
| 2 | `pipelined:data_width=16,n_iter=15,angle_guard=1,frac_guard=4,rounding=round` | 44130 | 930 | 132.4 | 17 | 2.49 | 0.000203 (2^-12.27) | 12.27 |
| 3 | `pipelined:data_width=20,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 47043 | 1018 | 123.1 | 17 | 2.7 | 7.03e-05 (2^-13.80) | 13.80 |
| 4 | `pipelined:data_width=20,n_iter=15,angle_guard=2,frac_guard=1,rounding=round` | 49392 | 1045 | 123.1 | 17 | 2.79 | 6.81e-05 (2^-13.84) | 13.84 |
| 5 | `pipelined:data_width=21,n_iter=17,angle_guard=-2,frac_guard=0,rounding=trunc` | 52751 | 1137 | 127.5 | 19 | 3.02 | 5.61e-05 (2^-14.12) | 14.12 |
| 6 | `pipelined:data_width=21,n_iter=17,angle_guard=-2,frac_guard=1,rounding=trunc` | 54223 | 1166 | 123.1 | 19 | 3.1 | 5.32e-05 (2^-14.20) | 14.20 |
| 7 | `pipelined:data_width=20,n_iter=22,angle_guard=1,frac_guard=0,rounding=trunc` | 68732 | 1471 | 127.5 | 24 | 3.91 | 4.65e-05 (2^-14.39) | 14.39 |
| 8 | `pipelined:data_width=20,n_iter=22,angle_guard=2,frac_guard=0,rounding=round` | 69748 | 1492 | 123.1 | 24 | 3.97 | 2.17e-05 (2^-15.49) | 15.49 |
| 9 | `pipelined:data_width=21,n_iter=22,angle_guard=1,frac_guard=0,rounding=round` | 71782 | 1536 | 123.1 | 24 | 4.08 | 1.21e-05 (2^-16.34) | 16.34 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 results within 0.5us of a 1MHz control tick, which demands 1 result/cycle throughput. Only pipelined and pipelined_m families provide this. The accuracy constraint (max_abs_err <= 2^-12) requires sufficient iterations and data width. Based on CORDIC theory, 14 iterations with 16-bit data width should meet the accuracy requirement. The area is minimized by keeping parameters at their minimum feasible values. The pipelined_m family may offer area savings through reduced register count, so both families are explored with equal budget share to map the Pareto front.*)
- `pipelined` (30 evals): data_width=16..16, n_iter=14..14, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* The 32-request burst within 0.5us requires 1 result/cycle throughput (pipelined). With 14 iterations and 16-bit width, the accuracy constraint (max_abs_err <= 2^-12) is met. The area is minimized by keeping data_width and n_iter at the minimum values that satisfy accuracy. The angle_guard and frac_guard are kept minimal to reduce area while maintaining accuracy.
- `pipelined_m` (30 evals): data_width=16..16, n_iter=14..14, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m can reduce area by registering every m stages instead of every stage. With m=2-4, the number of pipeline registers is reduced, potentially lowering area while maintaining 1 result/cycle throughput. The same accuracy constraints apply, so data_width and n_iter are kept at minimum values that satisfy max_abs_err <= 2^-12.

**Result (code):** 60 evaluations this round, 60 total; 9 feasible; hypervolume 1.602e+04 (n/a).

**LLM decision:** `stop` — The feasible Pareto front contains two pipelined designs that satisfy all constraints (throughput >= 32 MSPS, max_abs_err <= 2^-12, sys_p99_batch_us <= 0.5 us). The best area is 38197 um^2 with 12.2 accuracy bits. The front is narrow in accuracy (12.2-12.3 bits) but the constraint is max_abs_err <= 2^-12, so both designs pass. The hypervolume is 1.602e+04. Since this is the final round and we have a feasible front with a clear minimum-area design (38197 um^2), we stop. The selection rule (min area) will pick the 38197 um^2 design.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.602e+04 (gain this round: n/a (first round)).
Feasible designs: 9 of 60 evaluations (2 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 156
- max_abs_err <= 0.000244141: 85% violate; best seen 0.000204 (2^-12.26)
- sys_p99_batch_us <= 0.5: 37% violate; best seen 0.295

Pareto front (feasible, 2 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=38197, accuracy_bits=12.2, ffs=810, throughput_msps=143, max_abs_err=0.000209 (2^-12.22), power_index=2.16
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=39385, accuracy_bits=12.3, ffs=834, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=2.23
Front coverage: area_um2 38197..39385 (HV reference 100000); accuracy_bits 12.2..12.3 (HV reference 12); data_width on the front 16..16 (registry 8..28).

Per family:
- pipelined: 30 evals, 9 feasible; max throughput seen 156 MSPS; best accuracy 12.26 bits; best feasible area_um2=38197; feasible ranges: data_width 16..16, n_iter 14..14, angle_guard 2..2, frac_guard 1..2
- pipelined_m: 30 evals, 0 feasible; max throughput seen 82.5 MSPS; best accuracy 11.85 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (20 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (2 front designs; box front_anchored)
- `pipelined_m` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 40 evaluations this round, 100 total; 20 feasible; hypervolume 1.796e+05 (+1021.4%).

**No LLM call** (code's front-mapping round): The feasible Pareto front contains two pipelined designs that satisfy all constraints (throughput >= 32 MSPS, max_abs_err <= 2^-12, sys_p99_batch_us <= 0.5 us). The best area is 38197 um^2 with 12.2 accuracy bits. The front is narrow in accuracy (12.2-12.3 bits) but the constraint is max_abs_err <= 2^-12, so both designs pass. The hypervolume is 1.602e+04. Since this is the final round and we have a feasible front with a clear minimum-area design (38197 um^2), we stop. The selection rule (min area) will pick the 38197 um^2 design.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.796e+05 (gain this round: +1021.4%).
Feasible designs: 20 of 100 evaluations (13 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 7% violate; best seen 156
- max_abs_err <= 0.000244141: 70% violate; best seen 2.19e-07 (2^-22.13)
- sys_p99_batch_us <= 0.5: 39% violate; best seen 0.295

Pareto front (feasible, 10 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=38197, accuracy_bits=12.2, ffs=810, throughput_msps=143, max_abs_err=0.000209 (2^-12.22), power_index=2.16
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=39385, accuracy_bits=12.3, ffs=834, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=2.23
- pipelined [data_width=16 n_iter=15 angle_guard=1 frac_guard=4 rounding=round] area_um2=44130, accuracy_bits=12.3, ffs=930, throughput_msps=132, max_abs_err=0.000203 (2^-12.27), power_index=2.49
- pipelined [data_width=20 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=47043, accuracy_bits=13.8, ffs=1018, throughput_msps=123, max_abs_err=7.03e-05 (2^-13.80), power_index=2.7
- pipelined [data_width=20 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] area_um2=49392, accuracy_bits=13.8, ffs=1045, throughput_msps=123, max_abs_err=6.81e-05 (2^-13.84), power_index=2.79
- pipelined [data_width=21 n_iter=17 angle_guard=-2 frac_guard=0 rounding=trunc] area_um2=52751, accuracy_bits=14.1, ffs=1137, throughput_msps=128, max_abs_err=5.61e-05 (2^-14.12), power_index=3.02
- pipelined [data_width=21 n_iter=17 angle_guard=-2 frac_guard=1 rounding=trunc] area_um2=54223, accuracy_bits=14.2, ffs=1166, throughput_msps=123, max_abs_err=5.32e-05 (2^-14.20), power_index=3.1
- pipelined [data_width=20 n_iter=22 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=68732, accuracy_bits=14.4, ffs=1471, throughput_msps=128, max_abs_err=4.65e-05 (2^-14.39), power_index=3.91
- pipelined [data_width=20 n_iter=22 angle_guard=2 frac_guard=0 rounding=round] area_um2=69748, accuracy_bits=15.5, ffs=1492, throughput_msps=123, max_abs_err=2.17e-05 (2^-15.49), power_index=3.97
- pipelined [data_width=21 n_iter=22 angle_guard=1 frac_guard=0 rounding=round] area_um2=71782, accuracy_bits=16.3, ffs=1536, throughput_msps=123, max_abs_err=1.21e-05 (2^-16.34), power_index=4.08
Front coverage: area_um2 38197..71782 (HV reference 100000); accuracy_bits 12.2..16.3 (HV reference 12); data_width on the front 16..21 (registry 8..28).

Per family:
- pipelined: 50 evals, 20 feasible; max throughput seen 156 MSPS; best accuracy 20.46 bits; best feasible area_um2=38197; feasible ranges: data_width 16..21, n_iter 14..30, angle_guard -2..2, frac_guard 0..4
- pipelined_m: 50 evals, 0 feasible; max throughput seen 102 MSPS; best accuracy 22.13 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5037 in, 1152 out
- provider-reported cost: $0.0021
- full prompts and replies: `llm_trace.jsonl`

