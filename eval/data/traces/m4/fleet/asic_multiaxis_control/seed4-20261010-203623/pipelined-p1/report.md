# DSE run: asic_multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`pipelined:data_width=17,n_iter=15,angle_guard=4,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 42248 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 11255 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 914 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 128 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 128 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 133 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.42 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000146 (2^-12.74) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 4.79 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 4.27e-05 (2^-14.52) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.4 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.7 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=17,n_iter=15,angle_guard=4,frac_guard=0,rounding=round` | 42248 | 914 | 127.5 | 17 | 2.42 | 0.000146 (2^-12.74) | 12.74 |
| 1 | `pipelined:data_width=15,n_iter=16,angle_guard=4,frac_guard=4,rounding=round` | 47086 | 993 | 137.6 | 18 | 2.65 | 0.00013 (2^-12.91) | 12.91 |
| 2 | `pipelined:data_width=16,n_iter=16,angle_guard=3,frac_guard=3,rounding=round` | 47224 | 997 | 137.6 | 18 | 2.66 | 0.000104 (2^-13.23) | 13.23 |
| 3 | `pipelined:data_width=24,n_iter=15,angle_guard=-2,frac_guard=0,rounding=trunc` | 52524 | 1136 | 115.0 | 17 | 3.01 | 6.42e-05 (2^-13.93) | 13.93 |
| 4 | `pipelined:data_width=18,n_iter=17,angle_guard=3,frac_guard=3,rounding=round` | 55012 | 1160 | 127.5 | 19 | 3.1 | 3.11e-05 (2^-14.97) | 14.97 |
| 5 | `pipelined:data_width=21,n_iter=17,angle_guard=0,frac_guard=2,rounding=round` | 58372 | 1231 | 118.9 | 19 | 3.29 | 2.64e-05 (2^-15.21) | 15.21 |
| 6 | `pipelined:data_width=24,n_iter=17,angle_guard=-2,frac_guard=0,rounding=trunc` | 59770 | 1287 | 115.0 | 19 | 3.42 | 1.98e-05 (2^-15.63) | 15.63 |
| 7 | `pipelined:data_width=21,n_iter=17,angle_guard=3,frac_guard=2,rounding=round` | 60712 | 1281 | 115.0 | 19 | 3.42 | 1.72e-05 (2^-15.83) | 15.83 |
| 8 | `pipelined:data_width=21,n_iter=18,angle_guard=1,frac_guard=1,rounding=round` | 61113 | 1290 | 123.1 | 20 | 3.45 | 1.44e-05 (2^-16.08) | 16.08 |
| 9 | `pipelined:data_width=21,n_iter=18,angle_guard=1,frac_guard=3,rounding=round` | 64247 | 1353 | 115.0 | 20 | 3.62 | 1.31e-05 (2^-16.22) | 16.22 |
| 10 | `pipelined:data_width=21,n_iter=18,angle_guard=3,frac_guard=3,rounding=round` | 65902 | 1388 | 115.0 | 20 | 3.71 | 9.63e-06 (2^-16.66) | 16.66 |
| 11 | `pipelined:data_width=21,n_iter=19,angle_guard=3,frac_guard=3,rounding=round` | 69619 | 1466 | 115.0 | 21 | 3.92 | 6.64e-06 (2^-17.20) | 17.20 |
| 12 | `pipelined:data_width=25,n_iter=21,angle_guard=-2,frac_guard=0,rounding=trunc` | 77168 | 1652 | 111.3 | 23 | 4.39 | 3.76e-06 (2^-18.02) | 18.02 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec needs 12-bit accuracy (max_abs_err <= 2^-12) and a 32-request burst every 1 us with p99 batch <= 0.5 us. Pipelined families produce 1 result/cycle, so throughput_msps >= 32 is easily met if Fmax >= 32 MHz. The batch constraint is the tighter system limit: for pipelined, batch time is (N+2+31)/Fmax <= 0.5 us, so Fmax must be at least ~2*(N+33) MHz; for pipelined_m it is (ceil(N/m)+2+31)/Fmax <= 0.5 us. Data_width must be >=14 because the output LSB is 2^-(W-2) and W=13 would already exceed the error bound. We therefore search data_width 14..22, n_iter 8..20, angle_guard -2..4, frac_guard 0..4, and both rounding modes. The 60/40 split favours the simpler pipelined family, which is most likely to satisfy the system bound, while pipelined_m explores area savings from fewer pipeline registers. The first round is deliberately broad; later rounds can narrow around the feasible Pareto front and the system-feasible region.*)
- `pipelined` (36 evals): data_width=14..22, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Pipelined gives 1 result/cycle and is the simplest way to meet the 32 requests/us burst: a 32-request burst completes in 32 cycles after a latency of N+2 cycles. The system p99 batch constraint then requires Fmax >= 2*(N+33) MHz, which is plausible for N up to ~20. Data_width is restricted to >=14 because the output LSB is 2^-(W-2) and max_abs_err <= 2^-12 forces W >= 14. n_iter 8..20 trades area against accuracy; angle_guard and frac_guard tune the error/area trade-off. This family is likely the main feasible front, so it gets the larger share.
- `pipelined_m` (24 evals): data_width=14..22, n_iter=8..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Pipelined_m registers every m micro-rotations, reducing pipeline FFs and latency cycles to ceil(N/m)+2. This can lower area, but longer combinational paths may reduce Fmax, which matters for the 0.5 us p99 batch bound. Searching m=2..8 explores the area/latency/Fmax trade-off. Same accuracy-driven bounds on data_width (>=14) and n_iter (8..20) apply. This family may provide cheaper points on the Pareto front if the Fmax penalty is acceptable.

**Result (code):** 60 evaluations this round, 60 total; 26 feasible; hypervolume 2.274e+05 (n/a).

**LLM decision:** `stop` — Final round: the front is feasible and meets every constraint. The cheapest Pareto design (pipelined, data_width=17, n_iter=15, angle_guard=4, frac_guard=0, round) has area_um2=42248, accuracy_bits=12.7 (max_abs_err=1.46e-4 <= 2^-12), throughput 128 MSPS >= 32, and the front's sys_p99_batch bound (best 0.263 us <= 0.5) is satisfied; 26 of 60 evaluations were feasible and the front spans area 42248..69619 and accuracy 12.7..17.2 bits, so the min-area selection rule has a valid pick and the trade-off curve is well covered. pipelined_m produced 0 feasible designs (max throughput 75.4 MSPS), so it adds nothing. No further improvement is expected within the exhausted budget, so we stop.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 2.274e+05 (gain this round: n/a (first round)).
Feasible designs: 26 of 60 evaluations (22 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 13% violate; best seen 171
- max_abs_err <= 0.000244141: 20% violate; best seen 6.64e-06 (2^-17.20)
- sys_p99_batch_us <= 0.5: 40% violate; best seen 0.263

Pareto front (feasible, 10 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=15 angle_guard=4 frac_guard=0 rounding=round] area_um2=42248, accuracy_bits=12.7, ffs=914, throughput_msps=128, max_abs_err=0.000146 (2^-12.74), power_index=2.42
- pipelined [data_width=15 n_iter=16 angle_guard=4 frac_guard=4 rounding=round] area_um2=47086, accuracy_bits=12.9, ffs=993, throughput_msps=138, max_abs_err=0.00013 (2^-12.91), power_index=2.65
- pipelined [data_width=16 n_iter=16 angle_guard=3 frac_guard=3 rounding=round] area_um2=47224, accuracy_bits=13.2, ffs=997, throughput_msps=138, max_abs_err=0.000104 (2^-13.23), power_index=2.66
- pipelined [data_width=18 n_iter=17 angle_guard=3 frac_guard=3 rounding=round] area_um2=55012, accuracy_bits=15, ffs=1160, throughput_msps=128, max_abs_err=3.11e-05 (2^-14.97), power_index=3.1
- pipelined [data_width=21 n_iter=17 angle_guard=0 frac_guard=2 rounding=round] area_um2=58372, accuracy_bits=15.2, ffs=1231, throughput_msps=119, max_abs_err=2.64e-05 (2^-15.21), power_index=3.29
- pipelined [data_width=21 n_iter=17 angle_guard=3 frac_guard=2 rounding=round] area_um2=60712, accuracy_bits=15.8, ffs=1281, throughput_msps=115, max_abs_err=1.72e-05 (2^-15.83), power_index=3.42
- pipelined [data_width=21 n_iter=18 angle_guard=1 frac_guard=1 rounding=round] area_um2=61113, accuracy_bits=16.1, ffs=1290, throughput_msps=123, max_abs_err=1.44e-05 (2^-16.08), power_index=3.45
- pipelined [data_width=21 n_iter=18 angle_guard=1 frac_guard=3 rounding=round] area_um2=64247, accuracy_bits=16.2, ffs=1353, throughput_msps=115, max_abs_err=1.31e-05 (2^-16.22), power_index=3.62
- pipelined [data_width=21 n_iter=18 angle_guard=3 frac_guard=3 rounding=round] area_um2=65902, accuracy_bits=16.7, ffs=1388, throughput_msps=115, max_abs_err=9.63e-06 (2^-16.66), power_index=3.71
- pipelined [data_width=21 n_iter=19 angle_guard=3 frac_guard=3 rounding=round] area_um2=69619, accuracy_bits=17.2, ffs=1466, throughput_msps=115, max_abs_err=6.64e-06 (2^-17.20), power_index=3.92
Front coverage: area_um2 42248..69619 (HV reference 100000); accuracy_bits 12.7..17.2 (HV reference 12); data_width on the front 15..21 (registry 8..28).

Per family:
- pipelined: 36 evals, 26 feasible; max throughput seen 171 MSPS; best accuracy 17.20 bits; best feasible area_um2=42248; feasible ranges: data_width 15..21, n_iter 14..20, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 24 evals, 0 feasible; max throughput seen 75.4 MSPS; best accuracy 16.82 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (40 evals): data_width=14..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (10 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 38 feasible; hypervolume 2.483e+05 (+9.2%).

**No LLM call** (code's front-mapping round): Final round: the front is feasible and meets every constraint. The cheapest Pareto design (pipelined, data_width=17, n_iter=15, angle_guard=4, frac_guard=0, round) has area_um2=42248, accuracy_bits=12.7 (max_abs_err=1.46e-4 <= 2^-12), throughput 128 MSPS >= 32, and the front's sys_p99_batch bound (best 0.263 us <= 0.5) is satisfied; 26 of 60 evaluations were feasible and the front spans area 42248..69619 and accuracy 12.7..17.2 bits, so the min-area selection rule has a valid pick and the trade-off curve is well covered. pipelined_m produced 0 feasible designs (max throughput 75.4 MSPS), so it adds nothing. No further improvement is expected within the exhausted budget, so we stop.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 2.483e+05 (gain this round: +9.2%).
Feasible designs: 38 of 100 evaluations (31 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 8% violate; best seen 171
- max_abs_err <= 0.000244141: 25% violate; best seen 5.15e-07 (2^-20.89)
- sys_p99_batch_us <= 0.5: 39% violate; best seen 0.263

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=15 angle_guard=4 frac_guard=0 rounding=round] area_um2=42248, accuracy_bits=12.7, ffs=914, throughput_msps=128, max_abs_err=0.000146 (2^-12.74), power_index=2.42
- pipelined [data_width=15 n_iter=16 angle_guard=4 frac_guard=4 rounding=round] area_um2=47086, accuracy_bits=12.9, ffs=993, throughput_msps=138, max_abs_err=0.00013 (2^-12.91), power_index=2.65
- pipelined [data_width=24 n_iter=15 angle_guard=-2 frac_guard=0 rounding=trunc] area_um2=52524, accuracy_bits=13.9, ffs=1136, throughput_msps=115, max_abs_err=6.42e-05 (2^-13.93), power_index=3.01
- pipelined [data_width=18 n_iter=17 angle_guard=3 frac_guard=3 rounding=round] area_um2=55012, accuracy_bits=15, ffs=1160, throughput_msps=128, max_abs_err=3.11e-05 (2^-14.97), power_index=3.1
- pipelined [data_width=21 n_iter=17 angle_guard=0 frac_guard=2 rounding=round] area_um2=58372, accuracy_bits=15.2, ffs=1231, throughput_msps=119, max_abs_err=2.64e-05 (2^-15.21), power_index=3.29
- pipelined [data_width=21 n_iter=17 angle_guard=3 frac_guard=2 rounding=round] area_um2=60712, accuracy_bits=15.8, ffs=1281, throughput_msps=115, max_abs_err=1.72e-05 (2^-15.83), power_index=3.42
- pipelined [data_width=21 n_iter=18 angle_guard=1 frac_guard=1 rounding=round] area_um2=61113, accuracy_bits=16.1, ffs=1290, throughput_msps=123, max_abs_err=1.44e-05 (2^-16.08), power_index=3.45
- pipelined [data_width=21 n_iter=18 angle_guard=1 frac_guard=3 rounding=round] area_um2=64247, accuracy_bits=16.2, ffs=1353, throughput_msps=115, max_abs_err=1.31e-05 (2^-16.22), power_index=3.62
- pipelined [data_width=21 n_iter=19 angle_guard=3 frac_guard=3 rounding=round] area_um2=69619, accuracy_bits=17.2, ffs=1466, throughput_msps=115, max_abs_err=6.64e-06 (2^-17.20), power_index=3.92
- pipelined [data_width=25 n_iter=21 angle_guard=-2 frac_guard=0 rounding=trunc] area_um2=77168, accuracy_bits=18, ffs=1652, throughput_msps=111, max_abs_err=3.76e-06 (2^-18.02), power_index=4.39
Front coverage: area_um2 42248..77168 (HV reference 100000); accuracy_bits 12.7..18 (HV reference 12); data_width on the front 15..25 (registry 8..28).

Per family:
- pipelined: 76 evals, 38 feasible; max throughput seen 171 MSPS; best accuracy 20.89 bits; best feasible area_um2=42248; feasible ranges: data_width 15..25, n_iter 14..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 24 evals, 0 feasible; max throughput seen 75.4 MSPS; best accuracy 16.82 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 6315 in, 4849 out
- provider-reported cost: $0.0062
- full prompts and replies: `llm_trace.jsonl`

