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
`pipelined:data_width=15,n_iter=14,angle_guard=3,frac_guard=3,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 39246 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10456 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 830 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 112 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.22 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000215 (2^-12.18) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 1.76 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 6.43e-05 (2^-13.93) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 0.526 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 12.2 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (8 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=15,n_iter=14,angle_guard=3,frac_guard=3,rounding=round` | 39246 | 830 | 143.2 | 16 | 2.22 | 0.000215 (2^-12.18) | 12.18 |
| 1 | `pipelined:data_width=16,n_iter=14,angle_guard=3,frac_guard=3,rounding=trunc` | 40349 | 869 | 137.6 | 16 | 2.31 | 0.000209 (2^-12.23) | 12.23 |
| 2 | `pipelined:data_width=16,n_iter=14,angle_guard=3,frac_guard=3,rounding=round` | 41211 | 871 | 137.6 | 16 | 2.33 | 0.000171 (2^-12.51) | 12.51 |
| 3 | `pipelined:data_width=20,n_iter=17,angle_guard=2,frac_guard=0,rounding=trunc` | 53531 | 1153 | 123.1 | 19 | 3.06 | 4.61e-05 (2^-14.40) | 14.40 |
| 4 | `pipelined:data_width=19,n_iter=16,angle_guard=3,frac_guard=4,rounding=round` | 55347 | 1166 | 118.9 | 18 | 3.12 | 3.62e-05 (2^-14.75) | 14.75 |
| 5 | `pipelined:data_width=24,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 57612 | 1243 | 115.0 | 18 | 3.3 | 3.16e-05 (2^-14.95) | 14.95 |
| 6 | `pipelined:data_width=24,n_iter=17,angle_guard=0,frac_guard=0,rounding=trunc` | 61329 | 1320 | 115.0 | 19 | 3.5 | 1.7e-05 (2^-15.84) | 15.84 |
| 7 | `pipelined:data_width=24,n_iter=23,angle_guard=0,frac_guard=0,rounding=round` | 83633 | 1786 | 115.0 | 25 | 4.75 | 2.49e-06 (2^-18.62) | 18.62 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Burst of 32 within 0.5 us needs about 64+ MSPS effective, so only pipelined-type designs (1 result/cycle) can plausibly meet it from my families. Accuracy of 2^-12 sets minimal width and iteration counts, so I focus the ranges there to minimise area. The first round tests both families and the register-spacing trade-off, then I narrow based on feasibility.*)
- `pipelined` (28 evals): data_width=13..16, n_iter=11..15, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* One result per cycle, so 32 results in a burst arrive after about 32 cycles at Fmax plus latency; the 0.5 us deadline needs a high clock. Max error of 2^-12 needs W about 13-16 and N about 11-15, so the range is tight around that.
- `pipelined_m` (32 evals): data_width=13..16, n_iter=11..15, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, m=2..4. *Why:* Registering every m stages cuts FF area versus a full pipeline. Small m keeps Fmax high enough to drain the 32-request burst plus the shorter latency within 0.5 us. Slightly larger budget share since it is likely the cheaper option.

**Result (code):** 60 evaluations this round, 60 total; 6 feasible; hypervolume 3.062e+04 (n/a).

**LLM decision:** `stop` — This is the final round, so only stop or infeasible are valid. The constraints are reachable: 6 of 60 evaluations were feasible, and the front has 3 designs. They span area 39246..41211 um2 and accuracy 12.2..12.5 bits, and all meet throughput (138..143 MSPS vs >=32) and max_abs_err <= 2^-12. The cheapest, pipelined at data_width=15, n_iter=14, angle_guard=3, frac_guard=3 with round, has area 39246 um2 and error 0.000215. Selection by min area picks it. pipelined_m produced no feasible designs in 32 evals. The remaining evaluation budget is small, so further gains are unlikely. Declaring infeasible would be wrong because feasible designs exist.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 3.062e+04 (gain this round: n/a (first round)).
Feasible designs: 6 of 60 evaluations (4 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 163
- max_abs_err <= 0.000244141: 82% violate; best seen 0.000128 (2^-12.93)
- sys_p99_batch_us <= 0.5: 43% violate; best seen 0.263

Pareto front (feasible, 3 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=15 n_iter=14 angle_guard=3 frac_guard=3 rounding=round] area_um2=39246, accuracy_bits=12.2, ffs=830, throughput_msps=143, max_abs_err=0.000215 (2^-12.18), power_index=2.22
- pipelined [data_width=16 n_iter=14 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=40349, accuracy_bits=12.2, ffs=869, throughput_msps=138, max_abs_err=0.000209 (2^-12.23), power_index=2.31
- pipelined [data_width=16 n_iter=14 angle_guard=3 frac_guard=3 rounding=round] area_um2=41211, accuracy_bits=12.5, ffs=871, throughput_msps=138, max_abs_err=0.000171 (2^-12.51), power_index=2.33
Front coverage: area_um2 39246..41211 (HV reference 100000); accuracy_bits 12.2..12.5 (HV reference 12); data_width on the front 15..16 (registry 8..28).

Per family:
- pipelined: 28 evals, 6 feasible; max throughput seen 163 MSPS; best accuracy 12.51 bits; best feasible area_um2=39246; feasible ranges: data_width 15..16, n_iter 14..15, angle_guard 3..3, frac_guard 3..3
- pipelined_m: 32 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 12.93 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (20 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)
- `pipelined_m` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 40 evaluations this round, 100 total; 22 feasible; hypervolume 2.222e+05 (+625.6%).

**No LLM call** (code's front-mapping round): This is the final round, so only stop or infeasible are valid. The constraints are reachable: 6 of 60 evaluations were feasible, and the front has 3 designs. They span area 39246..41211 um2 and accuracy 12.2..12.5 bits, and all meet throughput (138..143 MSPS vs >=32) and max_abs_err <= 2^-12. The cheapest, pipelined at data_width=15, n_iter=14, angle_guard=3, frac_guard=3 with round, has area 39246 um2 and error 0.000215. Selection by min area picks it. pipelined_m produced no feasible designs in 32 evals. The remaining evaluation budget is small, so further gains are unlikely. Declaring infeasible would be wrong because feasible designs exist.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 2.222e+05 (gain this round: +625.6%).
Feasible designs: 22 of 100 evaluations (17 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 12% violate; best seen 163
- max_abs_err <= 0.000244141: 61% violate; best seen 1.15e-07 (2^-23.05)
- sys_p99_batch_us <= 0.5: 47% violate; best seen 0.263

Pareto front (feasible, 8 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=15 n_iter=14 angle_guard=3 frac_guard=3 rounding=round] area_um2=39246, accuracy_bits=12.2, ffs=830, throughput_msps=143, max_abs_err=0.000215 (2^-12.18), power_index=2.22
- pipelined [data_width=16 n_iter=14 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=40349, accuracy_bits=12.2, ffs=869, throughput_msps=138, max_abs_err=0.000209 (2^-12.23), power_index=2.31
- pipelined [data_width=16 n_iter=14 angle_guard=3 frac_guard=3 rounding=round] area_um2=41211, accuracy_bits=12.5, ffs=871, throughput_msps=138, max_abs_err=0.000171 (2^-12.51), power_index=2.33
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=53531, accuracy_bits=14.4, ffs=1153, throughput_msps=123, max_abs_err=4.61e-05 (2^-14.40), power_index=3.06
- pipelined [data_width=19 n_iter=16 angle_guard=3 frac_guard=4 rounding=round] area_um2=55347, accuracy_bits=14.8, ffs=1166, throughput_msps=119, max_abs_err=3.62e-05 (2^-14.75), power_index=3.12
- pipelined [data_width=24 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] area_um2=57612, accuracy_bits=15, ffs=1243, throughput_msps=115, max_abs_err=3.16e-05 (2^-14.95), power_index=3.3
- pipelined [data_width=24 n_iter=17 angle_guard=0 frac_guard=0 rounding=trunc] area_um2=61329, accuracy_bits=15.8, ffs=1320, throughput_msps=115, max_abs_err=1.7e-05 (2^-15.84), power_index=3.5
- pipelined [data_width=24 n_iter=23 angle_guard=0 frac_guard=0 rounding=round] area_um2=83633, accuracy_bits=18.6, ffs=1786, throughput_msps=115, max_abs_err=2.49e-06 (2^-18.62), power_index=4.75
Front coverage: area_um2 39246..83633 (HV reference 100000); accuracy_bits 12.2..18.6 (HV reference 12); data_width on the front 15..24 (registry 8..28).

Per family:
- pipelined: 48 evals, 22 feasible; max throughput seen 163 MSPS; best accuracy 23.05 bits; best feasible area_um2=39246; feasible ranges: data_width 15..25, n_iter 14..30, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 52 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 17.13 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 9676 in, 946 out
- provider-reported cost: $0.0288
- full prompts and replies: `llm_trace.jsonl`

