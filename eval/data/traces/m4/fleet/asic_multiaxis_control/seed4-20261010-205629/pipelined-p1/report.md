# DSE run: asic_multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: anthropic/claude-sonnet-5.5.  
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
`pipelined:data_width=16,n_iter=14,angle_guard=3,frac_guard=3,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 41211 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10979 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 871 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 138 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 138 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 116 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.33 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000171 (2^-12.51) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 2.8 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 5.39e-05 (2^-14.18) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 0.883 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.5 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (3 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=16,n_iter=14,angle_guard=3,frac_guard=3,rounding=round` | 41211 | 871 | 137.6 | 16 | 2.33 | 0.000171 (2^-12.51) | 12.51 |
| 1 | `pipelined:data_width=25,n_iter=14,angle_guard=-2,frac_guard=1,rounding=trunc` | 52003 | 1125 | 107.9 | 16 | 2.98 | 0.000122 (2^-13.00) | 13.00 |
| 2 | `pipelined:data_width=23,n_iter=19,angle_guard=2,frac_guard=0,rounding=trunc` | 67889 | 1457 | 111.3 | 21 | 3.87 | 7.63e-06 (2^-17.00) | 17.00 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The batch deadline needs roughly 32 results plus the pipeline latency within 0.5 us, which means a clock of at least about 70 MHz for a fully pipelined design. Only fully pipelined designs can sustain the 32 results/us throughput constraint here. Both of my families are therefore plausible. Accuracy of 2^-12 needs about 13 to 14 bits of width and 12 to 14 iterations, so I narrow the search box around that to spend the 100 evals on minimising area. Pipelined_m gets slightly more budget because its register savings may give lower area, and the ranges leave room to trade accuracy bits for area along the front.*)
- `pipelined` (28 evals): data_width=13..16, n_iter=11..15, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* Pipelined issues 1 result/cycle, so 32 requests at once drain in about 32 cycles plus latency. Fmax must be high enough to return all 32 within 0.5 us. Ranges target the 2^-12 error bound with few stages to limit area.
- `pipelined_m` (32 evals): data_width=13..16, n_iter=11..15, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, m=2..4. *Why:* Registering every m stages cuts FF count and so area, but lowers Fmax. The batch deadline of 0.5 us is tight, so small m values (2 to 4) keep the clock high enough while still saving registers.

**Result (code):** 60 evaluations this round, 60 total; 1 feasible; hypervolume 3.023e+04 (n/a).

**LLM decision:** `stop` — This is the final round, so only stop or infeasible is allowed. The constraints are reachable: one feasible design exists, a pipelined unit with data_width=16, n_iter=14, angle_guard=3, frac_guard=3 and rounding=round. It has area 41211 um2, 12.5 accuracy bits, 138 MSPS throughput and meets the batch-latency bound. So infeasible does not apply. I stop with that design as the pick, since it is the only feasible point and the minimum-area selection rule leaves no alternative.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 3.023e+04 (gain this round: n/a (first round)).
Feasible designs: 1 of 60 evaluations (1 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 180
- max_abs_err <= 0.000244141: 98% violate; best seen 0.000171 (2^-12.51)
- sys_p99_batch_us <= 0.5: 27% violate; best seen 0.25

Pareto front (feasible, 1 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=3 frac_guard=3 rounding=round] area_um2=41211, accuracy_bits=12.5, ffs=871, throughput_msps=138, max_abs_err=0.000171 (2^-12.51), power_index=2.33
Front coverage: area_um2 41211..41211 (HV reference 100000); accuracy_bits 12.5..12.5 (HV reference 12); data_width on the front 16..16 (registry 8..28).

Per family:
- pipelined: 28 evals, 1 feasible; max throughput seen 180 MSPS; best accuracy 12.51 bits; best feasible area_um2=41211; feasible ranges: data_width 16..16, n_iter 14..14, angle_guard 3..3, frac_guard 3..3
- pipelined_m: 32 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 11.46 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (20 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)
- `pipelined_m` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 40 evaluations this round, 100 total; 10 feasible; hypervolume 1.819e+05 (+501.9%).

**No LLM call** (code's front-mapping round): This is the final round, so only stop or infeasible is allowed. The constraints are reachable: one feasible design exists, a pipelined unit with data_width=16, n_iter=14, angle_guard=3, frac_guard=3 and rounding=round. It has area 41211 um2, 12.5 accuracy bits, 138 MSPS throughput and meets the batch-latency bound. So infeasible does not apply. I stop with that design as the pick, since it is the only feasible point and the minimum-area selection rule leaves no alternative.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.819e+05 (gain this round: +501.9%).
Feasible designs: 10 of 100 evaluations (8 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 8% violate; best seen 180
- max_abs_err <= 0.000244141: 73% violate; best seen 2.93e-07 (2^-21.71)
- sys_p99_batch_us <= 0.5: 39% violate; best seen 0.25

Pareto front (feasible, 3 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=3 frac_guard=3 rounding=round] area_um2=41211, accuracy_bits=12.5, ffs=871, throughput_msps=138, max_abs_err=0.000171 (2^-12.51), power_index=2.33
- pipelined [data_width=25 n_iter=14 angle_guard=-2 frac_guard=1 rounding=trunc] area_um2=52003, accuracy_bits=13, ffs=1125, throughput_msps=108, max_abs_err=0.000122 (2^-13.00), power_index=2.98
- pipelined [data_width=23 n_iter=19 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=67889, accuracy_bits=17, ffs=1457, throughput_msps=111, max_abs_err=7.63e-06 (2^-17.00), power_index=3.87
Front coverage: area_um2 41211..67889 (HV reference 100000); accuracy_bits 12.5..17 (HV reference 12); data_width on the front 16..25 (registry 8..28).

Per family:
- pipelined: 48 evals, 10 feasible; max throughput seen 180 MSPS; best accuracy 21.35 bits; best feasible area_um2=41211; feasible ranges: data_width 16..25, n_iter 14..28, angle_guard -2..3, frac_guard 0..3
- pipelined_m: 52 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 21.71 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 9466 in, 927 out
- provider-reported cost: $0.0282
- full prompts and replies: `llm_trace.jsonl`

