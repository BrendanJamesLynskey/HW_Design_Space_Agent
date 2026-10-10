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
`pipelined:data_width=19,n_iter=14,angle_guard=-1,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 39973 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10649 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 867 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 138 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 138 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 116 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000181 (2^-12.43) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 23.8 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.2e-05 (2^-14.23) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 6.82 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.4 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=19,n_iter=14,angle_guard=-1,frac_guard=0,rounding=round` | 39973 | 867 | 137.6 | 16 | 2.3 | 0.000181 (2^-12.43) | 12.43 |
| 1 | `pipelined:data_width=19,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 41249 | 895 | 132.4 | 16 | 2.37 | 0.000145 (2^-12.76) | 12.76 |
| 2 | `pipelined:data_width=20,n_iter=14,angle_guard=2,frac_guard=0,rounding=trunc` | 43800 | 950 | 123.1 | 16 | 2.51 | 0.000141 (2^-12.79) | 12.79 |
| 3 | `pipelined:data_width=20,n_iter=14,angle_guard=2,frac_guard=2,rounding=round` | 47242 | 999 | 123.1 | 16 | 2.67 | 0.000126 (2^-12.96) | 12.96 |
| 4 | `pipelined:data_width=19,n_iter=17,angle_guard=-1,frac_guard=0,rounding=round` | 48851 | 1053 | 137.6 | 19 | 2.79 | 0.000104 (2^-13.23) | 13.23 |
| 5 | `pipelined:data_width=19,n_iter=16,angle_guard=4,frac_guard=0,rounding=round` | 49554 | 1070 | 118.9 | 18 | 2.84 | 5.75e-05 (2^-14.09) | 14.09 |
| 6 | `pipelined:data_width=19,n_iter=17,angle_guard=1,frac_guard=0,rounding=round` | 50411 | 1086 | 132.4 | 19 | 2.88 | 5.02e-05 (2^-14.28) | 14.28 |
| 7 | `pipelined:data_width=19,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 50482 | 1068 | 127.5 | 18 | 2.85 | 4.95e-05 (2^-14.30) | 14.30 |
| 8 | `pipelined:data_width=19,n_iter=17,angle_guard=4,frac_guard=0,rounding=round` | 52751 | 1137 | 118.9 | 19 | 3.02 | 4.23e-05 (2^-14.53) | 14.53 |
| 9 | `pipelined:data_width=19,n_iter=19,angle_guard=2,frac_guard=0,rounding=round` | 57394 | 1233 | 127.5 | 21 | 3.27 | 3.86e-05 (2^-14.66) | 14.66 |
| 10 | `pipelined:data_width=20,n_iter=17,angle_guard=2,frac_guard=3,rounding=trunc` | 57948 | 1242 | 118.9 | 19 | 3.3 | 2.35e-05 (2^-15.38) | 15.38 |
| 11 | `pipelined:data_width=20,n_iter=17,angle_guard=2,frac_guard=3,rounding=round` | 59014 | 1244 | 118.9 | 19 | 3.32 | 2.07e-05 (2^-15.56) | 15.56 |
| 12 | `pipelined:data_width=19,n_iter=20,angle_guard=4,frac_guard=4,rounding=round` | 70381 | 1481 | 118.9 | 22 | 3.96 | 8.07e-06 (2^-16.92) | 16.92 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Both allowed families produce 1 result/cycle, so throughput_msps = Fmax and the 32 Msps constraint reduces to needing Fmax >= 32 MHz, which is easily met; the real trade-offs are area vs accuracy (W, N, guards, rounding) and, for pipelined_m, area vs latency (m). The binding accuracy constraint is max_abs_err <= 2^-12, which is set by N and W (guards/rounding are secondary), so I concentrate W and N in 14..20 and keep guards low to minimise area. I split the budget 55/45 between pipelined (the baseline full pipeline, likely to anchor the accuracy end of the front) and pipelined_m (the area-reduction variant, likely to anchor the low-area end), so the merged front covers the whole area/accuracy curve. The p99 batch deadline (0.5 us for 32 results) is the main risk for pipelined_m's higher latency, so I keep m modest (2..4) and let the L1 bound/L2 sim screen out designs that miss it.*)
- `pipelined` (33 evals): data_width=14..20, n_iter=14..20, angle_guard=-1..2, frac_guard=0..4, rounding=trunc|round. *Why:* Full pipeline gives 1 result/cycle, so throughput_msps = Fmax and it can meet the 32 Msps constraint at a modest Fmax. It is the natural area/accuracy trade-off family: area scales with N and W, accuracy with N and guards. I focus W and N in the 14..20 band because the 2^-12 error bound is the binding accuracy constraint and W=14..16 with N~14..18 is where trunc/round and small guards can hit it at minimum area; I keep angle_guard/frac_guard low to save area since accuracy is dominated by N and W.
- `pipelined_m` (27 evals): data_width=14..20, n_iter=14..20, angle_guard=-1..2, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* pipelined_m registers every m stages, cutting flip-flops (and area) versus the full pipeline while still giving 1 result/cycle, so it can meet the 32 Msps throughput constraint at lower area. The cost is higher latency (ceil(N/m)+2 cycles), which must stay within the 0.5 us p99 batch window at the achievable Fmax. I search m=2..4 to find the area/latency sweet spot: larger m saves registers but risks the batch deadline, so the front should show where that trade-off breaks. Same W/N/guard band as pipelined since accuracy is identical across families.

**Result (code):** 60 evaluations this round, 60 total; 27 feasible; hypervolume 1.752e+05 (n/a).

**LLM decision:** `stop` — The Pareto front is well-established with 7 feasible designs spanning area 39973-59014 um^2 and accuracy 12.4-15.6 bits. The minimum area design (pipelined, data_width=19, n_iter=14, angle_guard=-1, frac_guard=0, rounding=round) achieves 39973 um^2 with 12.4 bits accuracy (max_abs_err=0.000181 < 0.000244141 constraint) and 138 MSPS throughput (>> 32 MSPS constraint). The sys_p99_batch_us constraint is met by the best designs (0.28 us < 0.5 us). The pipelined family dominates the front; pipelined_m yielded 0 feasible designs. Since this is the final round, the current front adequately maps the trade-off space for the selection rule (min area), which picks the 39973 um^2 design.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.752e+05 (gain this round: n/a (first round)).
Feasible designs: 27 of 60 evaluations (22 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 171
- max_abs_err <= 0.000244141: 15% violate; best seen 2.07e-05 (2^-15.56)
- sys_p99_batch_us <= 0.5: 45% violate; best seen 0.28

Pareto front (feasible, 7 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=19 n_iter=14 angle_guard=-1 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.4, ffs=867, throughput_msps=138, max_abs_err=0.000181 (2^-12.43), power_index=2.3
- pipelined [data_width=19 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=41249, accuracy_bits=12.8, ffs=895, throughput_msps=132, max_abs_err=0.000145 (2^-12.76), power_index=2.37
- pipelined [data_width=20 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=47242, accuracy_bits=13, ffs=999, throughput_msps=123, max_abs_err=0.000126 (2^-12.96), power_index=2.67
- pipelined [data_width=19 n_iter=17 angle_guard=-1 frac_guard=0 rounding=round] area_um2=48851, accuracy_bits=13.2, ffs=1053, throughput_msps=138, max_abs_err=0.000104 (2^-13.23), power_index=2.79
- pipelined [data_width=19 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] area_um2=50411, accuracy_bits=14.3, ffs=1086, throughput_msps=132, max_abs_err=5.02e-05 (2^-14.28), power_index=2.88
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=57948, accuracy_bits=15.4, ffs=1242, throughput_msps=119, max_abs_err=2.35e-05 (2^-15.38), power_index=3.3
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=3 rounding=round] area_um2=59014, accuracy_bits=15.6, ffs=1244, throughput_msps=119, max_abs_err=2.07e-05 (2^-15.56), power_index=3.32
Front coverage: area_um2 39973..59014 (HV reference 100000); accuracy_bits 12.4..15.6 (HV reference 12); data_width on the front 19..20 (registry 8..28).

Per family:
- pipelined: 33 evals, 27 feasible; max throughput seen 171 MSPS; best accuracy 15.56 bits; best feasible area_um2=39973; feasible ranges: data_width 15..20, n_iter 14..20, angle_guard -1..2, frac_guard 0..4
- pipelined_m: 27 evals, 0 feasible; max throughput seen 78.8 MSPS; best accuracy 14.95 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (40 evals): data_width=18..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (7 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 54 feasible; hypervolume 2.177e+05 (+24.3%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established with 7 feasible designs spanning area 39973-59014 um^2 and accuracy 12.4-15.6 bits. The minimum area design (pipelined, data_width=19, n_iter=14, angle_guard=-1, frac_guard=0, rounding=round) achieves 39973 um^2 with 12.4 bits accuracy (max_abs_err=0.000181 < 0.000244141 constraint) and 138 MSPS throughput (>> 32 MSPS constraint). The sys_p99_batch_us constraint is met by the best designs (0.28 us < 0.5 us). The pipelined family dominates the front; pipelined_m yielded 0 feasible designs. Since this is the final round, the current front adequately maps the trade-off space for the selection rule (min area), which picks the 39973 um^2 design.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 2.177e+05 (gain this round: +24.3%).
Feasible designs: 54 of 100 evaluations (47 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 171
- max_abs_err <= 0.000244141: 16% violate; best seen 6.05e-07 (2^-20.66)
- sys_p99_batch_us <= 0.5: 33% violate; best seen 0.28

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=19 n_iter=14 angle_guard=-1 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.4, ffs=867, throughput_msps=138, max_abs_err=0.000181 (2^-12.43), power_index=2.3
- pipelined [data_width=19 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=41249, accuracy_bits=12.8, ffs=895, throughput_msps=132, max_abs_err=0.000145 (2^-12.76), power_index=2.37
- pipelined [data_width=20 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=47242, accuracy_bits=13, ffs=999, throughput_msps=123, max_abs_err=0.000126 (2^-12.96), power_index=2.67
- pipelined [data_width=19 n_iter=17 angle_guard=-1 frac_guard=0 rounding=round] area_um2=48851, accuracy_bits=13.2, ffs=1053, throughput_msps=138, max_abs_err=0.000104 (2^-13.23), power_index=2.79
- pipelined [data_width=19 n_iter=16 angle_guard=4 frac_guard=0 rounding=round] area_um2=49554, accuracy_bits=14.1, ffs=1070, throughput_msps=119, max_abs_err=5.75e-05 (2^-14.09), power_index=2.84
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=50482, accuracy_bits=14.3, ffs=1068, throughput_msps=128, max_abs_err=4.95e-05 (2^-14.30), power_index=2.85
- pipelined [data_width=19 n_iter=17 angle_guard=4 frac_guard=0 rounding=round] area_um2=52751, accuracy_bits=14.5, ffs=1137, throughput_msps=119, max_abs_err=4.23e-05 (2^-14.53), power_index=3.02
- pipelined [data_width=19 n_iter=19 angle_guard=2 frac_guard=0 rounding=round] area_um2=57394, accuracy_bits=14.7, ffs=1233, throughput_msps=128, max_abs_err=3.86e-05 (2^-14.66), power_index=3.27
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=3 rounding=round] area_um2=59014, accuracy_bits=15.6, ffs=1244, throughput_msps=119, max_abs_err=2.07e-05 (2^-15.56), power_index=3.32
- pipelined [data_width=19 n_iter=20 angle_guard=4 frac_guard=4 rounding=round] area_um2=70381, accuracy_bits=16.9, ffs=1481, throughput_msps=119, max_abs_err=8.07e-06 (2^-16.92), power_index=3.96
Front coverage: area_um2 39973..70381 (HV reference 100000); accuracy_bits 12.4..16.9 (HV reference 12); data_width on the front 19..20 (registry 8..28).

Per family:
- pipelined: 73 evals, 54 feasible; max throughput seen 171 MSPS; best accuracy 20.66 bits; best feasible area_um2=39973; feasible ranges: data_width 15..26, n_iter 14..26, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 27 evals, 0 feasible; max throughput seen 78.8 MSPS; best accuracy 14.95 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5341 in, 1291 out
- provider-reported cost: $0.0020
- full prompts and replies: `llm_trace.jsonl`

