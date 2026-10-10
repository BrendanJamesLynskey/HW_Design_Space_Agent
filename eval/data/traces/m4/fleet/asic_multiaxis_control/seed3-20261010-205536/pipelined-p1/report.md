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
`pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=2` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 30990 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 8256 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 453 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 78.8 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 78.8 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 9 | exact: schedule |
| latency_ns | 114 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.39 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000192 (2^-12.35) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 6.29 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.46e-05 (2^-14.16) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.79 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (12 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=2` | 30990 | 453 | 78.8 | 9 | 1.39 | 0.000192 (2^-12.35) | 12.35 |
| 1 | `pipelined:data_width=17,n_iter=15,angle_guard=3,frac_guard=3,rounding=trunc` | 45411 | 976 | 132.4 | 17 | 2.59 | 0.000112 (2^-13.13) | 13.13 |
| 2 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc` | 45499 | 980 | 132.4 | 17 | 2.6 | 9.49e-05 (2^-13.36) | 13.36 |
| 3 | `pipelined:data_width=18,n_iter=15,angle_guard=3,frac_guard=2,rounding=trunc` | 46184 | 995 | 127.5 | 17 | 2.64 | 9.41e-05 (2^-13.38) | 13.38 |
| 4 | `pipelined:data_width=17,n_iter=15,angle_guard=3,frac_guard=3,rounding=round` | 46324 | 978 | 132.4 | 17 | 2.61 | 8.99e-05 (2^-13.44) | 13.44 |
| 5 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 49611 | 1048 | 132.4 | 18 | 2.8 | 5.46e-05 (2^-14.16) | 14.16 |
| 6 | `pipelined:data_width=22,n_iter=16,angle_guard=-2,frac_guard=2,rounding=round` | 55675 | 1174 | 115.0 | 18 | 3.14 | 4.7e-05 (2^-14.38) | 14.38 |
| 7 | `pipelined:data_width=24,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 61100 | 1313 | 107.9 | 18 | 3.49 | 3.08e-05 (2^-14.99) | 14.99 |
| 8 | `pipelined:data_width=24,n_iter=16,angle_guard=1,frac_guard=3,rounding=round` | 63748 | 1343 | 104.7 | 18 | 3.59 | 3.06e-05 (2^-14.99) | 14.99 |
| 9 | `pipelined:data_width=21,n_iter=20,angle_guard=-1,frac_guard=2,rounding=round` | 67892 | 1429 | 118.9 | 22 | 3.82 | 2.68e-05 (2^-15.19) | 15.19 |
| 10 | `pipelined:data_width=21,n_iter=20,angle_guard=4,frac_guard=2,rounding=round` | 72502 | 1528 | 111.3 | 22 | 4.08 | 4.6e-06 (2^-17.73) | 17.73 |
| 11 | `pipelined:data_width=21,n_iter=20,angle_guard=4,frac_guard=4,rounding=round` | 76015 | 1599 | 111.3 | 22 | 4.28 | 3.67e-06 (2^-18.05) | 18.05 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Both pipelined families give 1 result/cycle, so the 32-request burst needs about 32 cycles plus latency inside 0.5 us, meaning a clock of roughly 70-100+ MHz. Max error <= 2^-12 needs about 13-16 bit width and about 12-16 iterations. I focus on small widths to minimise area. pipelined_m gets the larger share because fewer registers should reduce area, and m is kept small to protect Fmax. Later rounds can refine according to the measured front.*)
- `pipelined` (24 evals): data_width=13..18, n_iter=12..16, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* Accepts one request per cycle, so 32 requests drain in 32 cycles. It must be fast enough for the 0.5 us bound, so Fmax must be high, and a fully registered pipeline gives the highest Fmax. Ranges target error <= 2^-12 with minimal width.
- `pipelined_m` (36 evals): data_width=13..18, n_iter=12..16, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, m=2..4. *Why:* Registering every m stages cuts FF count and area, which is the objective. A small m keeps Fmax high enough for 32 results to drain within 0.5 us (about 64+ MSPS needed). Fewer registers likely wins on area if the bound still holds.

**Result (code):** 60 evaluations this round, 60 total; 11 feasible; hypervolume 1.198e+05 (n/a).

**LLM decision:** `stop` — This is the final round, so only stop or infeasible are valid. The constraints are reachable: 11 of 60 evaluations were feasible, and the front has 6 designs. The cheapest feasible design is pipelined_m (data_width=17, n_iter=14, m=2) at 30990 um2 with 12.3 accuracy bits, 78.8 MSPS and max error 0.000192, which is inside the 2^-12 limit. The front spans 30990..49611 um2 and 12.3..14.2 bits, so it is a usable trade-off curve. The 0.5 us p99 batch constraint was met, with a best seen of 0.282 us. Iterative and unrolled_k were not run, but their multi-cycle issue would likely queue the 32-request burst, so I am not declaring infeasibility.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.198e+05 (gain this round: n/a (first round)).
Feasible designs: 11 of 60 evaluations (8 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 163
- max_abs_err <= 0.000244141: 55% violate; best seen 5.46e-05 (2^-14.16)
- sys_p99_batch_us <= 0.5: 48% violate; best seen 0.282

Pareto front (feasible, 6 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=2] area_um2=30990, accuracy_bits=12.3, ffs=453, throughput_msps=78.8, max_abs_err=0.000192 (2^-12.35), power_index=1.39
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=45411, accuracy_bits=13.1, ffs=976, throughput_msps=132, max_abs_err=0.000112 (2^-13.13), power_index=2.59
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=45499, accuracy_bits=13.4, ffs=980, throughput_msps=132, max_abs_err=9.49e-05 (2^-13.36), power_index=2.6
- pipelined [data_width=18 n_iter=15 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=46184, accuracy_bits=13.4, ffs=995, throughput_msps=128, max_abs_err=9.41e-05 (2^-13.38), power_index=2.64
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=3 rounding=round] area_um2=46324, accuracy_bits=13.4, ffs=978, throughput_msps=132, max_abs_err=8.99e-05 (2^-13.44), power_index=2.61
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
Front coverage: area_um2 30990..49611 (HV reference 100000); accuracy_bits 12.3..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 24 evals, 10 feasible; max throughput seen 163 MSPS; best accuracy 14.16 bits; best feasible area_um2=42933; feasible ranges: data_width 16..18, n_iter 15..16, angle_guard 2..3, frac_guard 0..3
- pipelined_m: 36 evals, 1 feasible; max throughput seen 91.1 MSPS; best accuracy 13.92 bits; best feasible area_um2=30990; feasible ranges: data_width 17..17, n_iter 14..14, angle_guard 1..1, frac_guard 1..1, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (7 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)
- `pipelined` (33 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (5 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 40 feasible; hypervolume 2.373e+05 (+98.1%).

**No LLM call** (code's front-mapping round): This is the final round, so only stop or infeasible are valid. The constraints are reachable: 11 of 60 evaluations were feasible, and the front has 6 designs. The cheapest feasible design is pipelined_m (data_width=17, n_iter=14, m=2) at 30990 um2 with 12.3 accuracy bits, 78.8 MSPS and max error 0.000192, which is inside the 2^-12 limit. The front spans 30990..49611 um2 and 12.3..14.2 bits, so it is a usable trade-off curve. The 0.5 us p99 batch constraint was met, with a best seen of 0.282 us. Iterative and unrolled_k were not run, but their multi-cycle issue would likely queue the 32-request burst, so I am not declaring infeasibility.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 2.373e+05 (gain this round: +98.1%).
Feasible designs: 40 of 100 evaluations (31 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 6% violate; best seen 163
- max_abs_err <= 0.000244141: 37% violate; best seen 5.33e-07 (2^-20.84)
- sys_p99_batch_us <= 0.5: 38% violate; best seen 0.282

Pareto front (feasible, 12 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=2] area_um2=30990, accuracy_bits=12.3, ffs=453, throughput_msps=78.8, max_abs_err=0.000192 (2^-12.35), power_index=1.39
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=45411, accuracy_bits=13.1, ffs=976, throughput_msps=132, max_abs_err=0.000112 (2^-13.13), power_index=2.59
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=45499, accuracy_bits=13.4, ffs=980, throughput_msps=132, max_abs_err=9.49e-05 (2^-13.36), power_index=2.6
- pipelined [data_width=17 n_iter=15 angle_guard=3 frac_guard=3 rounding=round] area_um2=46324, accuracy_bits=13.4, ffs=978, throughput_msps=132, max_abs_err=8.99e-05 (2^-13.44), power_index=2.61
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
- pipelined [data_width=22 n_iter=16 angle_guard=-2 frac_guard=2 rounding=round] area_um2=55675, accuracy_bits=14.4, ffs=1174, throughput_msps=115, max_abs_err=4.7e-05 (2^-14.38), power_index=3.14
- pipelined [data_width=24 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=61100, accuracy_bits=15, ffs=1313, throughput_msps=108, max_abs_err=3.08e-05 (2^-14.99), power_index=3.49
- pipelined [data_width=21 n_iter=20 angle_guard=-1 frac_guard=2 rounding=round] area_um2=67892, accuracy_bits=15.2, ffs=1429, throughput_msps=119, max_abs_err=2.68e-05 (2^-15.19), power_index=3.82
- pipelined [data_width=21 n_iter=20 angle_guard=4 frac_guard=2 rounding=round] area_um2=72502, accuracy_bits=17.7, ffs=1528, throughput_msps=111, max_abs_err=4.6e-06 (2^-17.73), power_index=4.08
- pipelined [data_width=21 n_iter=20 angle_guard=4 frac_guard=4 rounding=round] area_um2=76015, accuracy_bits=18.1, ffs=1599, throughput_msps=111, max_abs_err=3.67e-06 (2^-18.05), power_index=4.28
Front coverage: area_um2 30990..76015 (HV reference 100000); accuracy_bits 12.3..18.1 (HV reference 12); data_width on the front 17..24 (registry 8..28).

Per family:
- pipelined: 57 evals, 39 feasible; max throughput seen 163 MSPS; best accuracy 20.30 bits; best feasible area_um2=42175; feasible ranges: data_width 16..24, n_iter 14..24, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 43 evals, 1 feasible; max throughput seen 91.1 MSPS; best accuracy 20.84 bits; best feasible area_um2=30990; feasible ranges: data_width 17..17, n_iter 14..14, angle_guard 1..1, frac_guard 1..1, m 2..2
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 10072 in, 993 out
- provider-reported cost: $0.0301
- full prompts and replies: `llm_trace.jsonl`

