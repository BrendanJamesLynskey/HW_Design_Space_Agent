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
`pipelined:data_width=16,n_iter=14,angle_guard=2,frac_guard=3,rounding=trunc` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 39712 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10580 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 855 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 138 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 138 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 116 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.27 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000217 (2^-12.17) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.56 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 6.18e-05 (2^-13.98) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 1.01 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.2 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=16,n_iter=14,angle_guard=2,frac_guard=3,rounding=trunc` | 39712 | 855 | 137.6 | 16 | 2.27 | 0.000217 (2^-12.17) | 12.17 |
| 1 | `pipelined:data_width=16,n_iter=14,angle_guard=3,frac_guard=3,rounding=trunc` | 40349 | 869 | 137.6 | 16 | 2.31 | 0.000209 (2^-12.23) | 12.23 |
| 2 | `pipelined:data_width=16,n_iter=14,angle_guard=4,frac_guard=3,rounding=trunc` | 40987 | 883 | 132.4 | 16 | 2.34 | 0.000208 (2^-12.23) | 12.23 |
| 3 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` | 42125 | 893 | 132.4 | 16 | 2.38 | 0.000152 (2^-12.68) | 12.68 |
| 4 | `pipelined:data_width=18,n_iter=15,angle_guard=0,frac_guard=1,rounding=round` | 43809 | 927 | 137.6 | 17 | 2.47 | 0.00014 (2^-12.80) | 12.80 |
| 5 | `pipelined:data_width=16,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 45114 | 954 | 143.2 | 18 | 2.55 | 0.000134 (2^-12.86) | 12.86 |
| 6 | `pipelined:data_width=18,n_iter=16,angle_guard=0,frac_guard=1,rounding=round` | 46768 | 989 | 137.6 | 18 | 2.64 | 0.00012 (2^-13.03) | 13.03 |
| 7 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=3,rounding=trunc` | 46782 | 1006 | 127.5 | 17 | 2.67 | 8.58e-05 (2^-13.51) | 13.51 |
| 8 | `pipelined:data_width=18,n_iter=16,angle_guard=1,frac_guard=1,rounding=round` | 47501 | 1005 | 137.6 | 18 | 2.68 | 8.41e-05 (2^-13.54) | 13.54 |
| 9 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=3,rounding=round` | 47745 | 1008 | 127.5 | 17 | 2.69 | 8.08e-05 (2^-13.60) | 13.60 |
| 10 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 48233 | 1020 | 132.4 | 18 | 2.72 | 6.45e-05 (2^-13.92) | 13.92 |
| 11 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=3,rounding=trunc` | 50025 | 1074 | 127.5 | 18 | 2.85 | 5.94e-05 (2^-14.04) | 14.04 |
| 12 | `pipelined:data_width=21,n_iter=25,angle_guard=0,frac_guard=0,rounding=round` | 80638 | 1720 | 127.5 | 27 | 4.58 | 1.79e-05 (2^-15.77) | 15.77 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The burst needs 32 results within 0.5 us, so the unit must sustain at least 64 results/us, which only the pipelined families can plausibly offer. Accuracy of 2^-12 needs roughly W>=14 and N around 12-14, so I search a narrow band around that to save area. pipelined_m gets slightly more budget because fewer registers likely lowers area, which is the objective. Both accuracy_bits and area are objectives, so the ranges span a little above the minimum accuracy for front coverage.*)
- `pipelined` (28 evals): data_width=13..18, n_iter=11..16, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* Pipelined gives 1 result/cycle, so 32 results in a burst take about 32 cycles plus latency. At high Fmax this should fit within 0.5 us, and throughput is far above 32 MSPS. Ranges target the 2^-12 error bound with minimal width and iterations.
- `pipelined_m` (32 evals): data_width=13..18, n_iter=11..16, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* Registering every m stages cuts FF count, which should reduce area. The lower Fmax from longer combinational paths must still clear the burst deadline, so m is searched broadly to find where that tradeoff sits.

**Result (code):** 60 evaluations this round, 60 total; 17 feasible; hypervolume 1.112e+05 (n/a).

**LLM decision:** `stop` — This is the final round, so only stop or infeasible is available. Feasible designs exist, so infeasible does not apply. Round 1 found 17 feasible designs out of 60 evaluations, with 9 on the Pareto front. All of them are pipelined and meet throughput (128..143 MSPS against a 32 MSPS requirement) and error (worst 0.000152 against the 0.000244 limit). The cheapest design is pipelined W=18, N=14, angle_guard=2, frac_guard=1, round, at area 42125 um2 and 12.7 accuracy bits. The front spans 42125..50025 um2 and 12.7..14 bits, and the hypervolume is 1.112e+05. pipelined_m produced 0 feasible designs in 32 evaluations, with a maximum throughput of 72.3 MSPS, so it is not a competitive alternative. The remaining budget is too small to change the selection, and the minimum-area pick is already on the front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.112e+05 (gain this round: n/a (first round)).
Feasible designs: 17 of 60 evaluations (12 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 18% violate; best seen 163
- max_abs_err <= 0.000244141: 43% violate; best seen 5.94e-05 (2^-14.04)
- sys_p99_batch_us <= 0.5: 53% violate; best seen 0.27

Pareto front (feasible, 9 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=42125, accuracy_bits=12.7, ffs=893, throughput_msps=132, max_abs_err=0.000152 (2^-12.68), power_index=2.38
- pipelined [data_width=18 n_iter=15 angle_guard=0 frac_guard=1 rounding=round] area_um2=43809, accuracy_bits=12.8, ffs=927, throughput_msps=138, max_abs_err=0.00014 (2^-12.80), power_index=2.47
- pipelined [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=45114, accuracy_bits=12.9, ffs=954, throughput_msps=143, max_abs_err=0.000134 (2^-12.86), power_index=2.55
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=round] area_um2=46768, accuracy_bits=13, ffs=989, throughput_msps=138, max_abs_err=0.00012 (2^-13.03), power_index=2.64
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=46782, accuracy_bits=13.5, ffs=1006, throughput_msps=128, max_abs_err=8.58e-05 (2^-13.51), power_index=2.67
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] area_um2=47501, accuracy_bits=13.5, ffs=1005, throughput_msps=138, max_abs_err=8.41e-05 (2^-13.54), power_index=2.68
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=3 rounding=round] area_um2=47745, accuracy_bits=13.6, ffs=1008, throughput_msps=128, max_abs_err=8.08e-05 (2^-13.60), power_index=2.69
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=48233, accuracy_bits=13.9, ffs=1020, throughput_msps=132, max_abs_err=6.45e-05 (2^-13.92), power_index=2.72
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=50025, accuracy_bits=14, ffs=1074, throughput_msps=128, max_abs_err=5.94e-05 (2^-14.04), power_index=2.85
Front coverage: area_um2 42125..50025 (HV reference 100000); accuracy_bits 12.7..14 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 28 evals, 17 feasible; max throughput seen 163 MSPS; best accuracy 14.04 bits; best feasible area_um2=42125; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 1..3
- pipelined_m: 32 evals, 0 feasible; max throughput seen 72.3 MSPS; best accuracy 13.59 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (40 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (9 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 36 feasible; hypervolume 1.453e+05 (+30.6%).

**No LLM call** (code's front-mapping round): This is the final round, so only stop or infeasible is available. Feasible designs exist, so infeasible does not apply. Round 1 found 17 feasible designs out of 60 evaluations, with 9 on the Pareto front. All of them are pipelined and meet throughput (128..143 MSPS against a 32 MSPS requirement) and error (worst 0.000152 against the 0.000244 limit). The cheapest design is pipelined W=18, N=14, angle_guard=2, frac_guard=1, round, at area 42125 um2 and 12.7 accuracy bits. The front spans 42125..50025 um2 and 12.7..14 bits, and the hypervolume is 1.112e+05. pipelined_m produced 0 feasible designs in 32 evaluations, with a maximum throughput of 72.3 MSPS, so it is not a competitive alternative. The remaining budget is too small to change the selection, and the minimum-area pick is already on the front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.453e+05 (gain this round: +30.6%).
Feasible designs: 36 of 100 evaluations (26 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 11% violate; best seen 163
- max_abs_err <= 0.000244141: 36% violate; best seen 1.53e-07 (2^-22.64)
- sys_p99_batch_us <= 0.5: 43% violate; best seen 0.27

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=39712, accuracy_bits=12.2, ffs=855, throughput_msps=138, max_abs_err=0.000217 (2^-12.17), power_index=2.27
- pipelined [data_width=16 n_iter=14 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=40349, accuracy_bits=12.2, ffs=869, throughput_msps=138, max_abs_err=0.000209 (2^-12.23), power_index=2.31
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=42125, accuracy_bits=12.7, ffs=893, throughput_msps=132, max_abs_err=0.000152 (2^-12.68), power_index=2.38
- pipelined [data_width=18 n_iter=15 angle_guard=0 frac_guard=1 rounding=round] area_um2=43809, accuracy_bits=12.8, ffs=927, throughput_msps=138, max_abs_err=0.00014 (2^-12.80), power_index=2.47
- pipelined [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=45114, accuracy_bits=12.9, ffs=954, throughput_msps=143, max_abs_err=0.000134 (2^-12.86), power_index=2.55
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=46782, accuracy_bits=13.5, ffs=1006, throughput_msps=128, max_abs_err=8.58e-05 (2^-13.51), power_index=2.67
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] area_um2=47501, accuracy_bits=13.5, ffs=1005, throughput_msps=138, max_abs_err=8.41e-05 (2^-13.54), power_index=2.68
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=3 rounding=round] area_um2=47745, accuracy_bits=13.6, ffs=1008, throughput_msps=128, max_abs_err=8.08e-05 (2^-13.60), power_index=2.69
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=50025, accuracy_bits=14, ffs=1074, throughput_msps=128, max_abs_err=5.94e-05 (2^-14.04), power_index=2.85
- pipelined [data_width=21 n_iter=25 angle_guard=0 frac_guard=0 rounding=round] area_um2=80638, accuracy_bits=15.8, ffs=1720, throughput_msps=128, max_abs_err=1.79e-05 (2^-15.77), power_index=4.58
Front coverage: area_um2 39712..80638 (HV reference 100000); accuracy_bits 12.2..15.8 (HV reference 12); data_width on the front 16..21 (registry 8..28).

Per family:
- pipelined: 68 evals, 36 feasible; max throughput seen 163 MSPS; best accuracy 22.64 bits; best feasible area_um2=39712; feasible ranges: data_width 16..28, n_iter 13..28, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 32 evals, 0 feasible; max throughput seen 72.3 MSPS; best accuracy 13.59 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 10313 in, 1033 out
- provider-reported cost: $0.0310
- full prompts and replies: `llm_trace.jsonl`

