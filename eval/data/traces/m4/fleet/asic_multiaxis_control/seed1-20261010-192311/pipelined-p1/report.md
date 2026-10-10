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
`pipelined:data_width=18,n_iter=14,angle_guard=0,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 41074 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10943 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 887 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 132 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 132 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 121 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.35 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000186 (2^-12.40) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 12.2 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.29e-05 (2^-14.21) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.47 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.4 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (12 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=14,angle_guard=0,frac_guard=2,rounding=trunc` | 41074 | 887 | 132.4 | 16 | 2.35 | 0.000186 (2^-12.40) | 12.40 |
| 1 | `pipelined:data_width=17,n_iter=14,angle_guard=2,frac_guard=2,rounding=round` | 41349 | 875 | 137.6 | 16 | 2.34 | 0.000169 (2^-12.53) | 12.53 |
| 2 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` | 42350 | 914 | 132.4 | 16 | 2.42 | 0.000156 (2^-12.65) | 12.65 |
| 3 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=2,rounding=round` | 43313 | 916 | 132.4 | 16 | 2.45 | 0.000144 (2^-12.76) | 12.76 |
| 4 | `pipelined:data_width=17,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 47362 | 1001 | 137.6 | 18 | 2.67 | 8.59e-05 (2^-13.51) | 13.51 |
| 5 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 49611 | 1048 | 132.4 | 18 | 2.8 | 5.46e-05 (2^-14.16) | 14.16 |
| 6 | `pipelined:data_width=18,n_iter=17,angle_guard=2,frac_guard=2,rounding=round` | 52760 | 1114 | 132.4 | 19 | 2.98 | 4.73e-05 (2^-14.37) | 14.37 |
| 7 | `pipelined:data_width=21,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 55240 | 1188 | 118.9 | 18 | 3.15 | 3.41e-05 (2^-14.84) | 14.84 |
| 8 | `pipelined:data_width=21,n_iter=17,angle_guard=2,frac_guard=0,rounding=round` | 55870 | 1203 | 118.9 | 19 | 3.19 | 2.18e-05 (2^-15.48) | 15.48 |
| 9 | `pipelined:data_width=21,n_iter=23,angle_guard=0,frac_guard=1,rounding=trunc` | 76097 | 1624 | 123.1 | 25 | 4.32 | 1.69e-05 (2^-15.85) | 15.85 |
| 10 | `pipelined:data_width=20,n_iter=23,angle_guard=3,frac_guard=1,rounding=round` | 77163 | 1626 | 118.9 | 25 | 4.35 | 1.24e-05 (2^-16.30) | 16.30 |
| 11 | `pipelined:data_width=25,n_iter=23,angle_guard=0,frac_guard=0,rounding=round` | 86826 | 1854 | 111.3 | 25 | 4.93 | 1.33e-06 (2^-19.52) | 19.52 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The system scenario is a 1 MHz tick that issues 32 requests at once and requires all 32 results within 0.5 us. Only pipelined and pipelined_m produce one result per cycle; iterative and unrolled_k would need multiple cycles per result and cannot meet the burst deadline. The accuracy constraint max_abs_err <= 2^-12 requires at least data_width >= 14 and n_iter >= 13, so the search is centred just above those minima to find the smallest-area designs that still pass. The system constraint also imposes a minimum Fmax that depends on latency: pipelined needs roughly (N+2+31)*2 MHz, while pipelined_m needs (ceil(N/m)+2+31)*2 MHz. The proposed ranges cover the plausible feasible region for both families, with a slight budget bias toward pipelined because its shorter combinational path makes it more likely to satisfy the Fmax bound. The first round will map the front; later rounds can refine around the feasible Pareto points and extend ranges if the cost model shows margin.*)
- `pipelined` (33 evals): data_width=14..18, n_iter=13..18, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Pipelined gives 1 result/cycle and latency N+2, so it is one of only two families that can drain a 32-request burst inside 0.5 us. The accuracy floor 2^-12 forces data_width >= 14 and n_iter >= 13; the ranges start there and extend upward to expose the area-accuracy trade-off. angle_guard and frac_guard are kept small because extra guard bits cost area and the objective is minimum area. Both rounding modes are kept because trunc may save a little logic if the guard bits compensate. The 55% share reflects that pipelined has the shortest combinational path and is the most likely to satisfy the system Fmax bound.
- `pipelined_m` (27 evals): data_width=14..18, n_iter=13..18, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, m=2..6. *Why:* Pipelined_m also gives 1 result/cycle but registers every m stages, so it can cut flip-flop area at the cost of a longer combinational path and lower Fmax. The system bound requires Fmax >= (ceil(N/m)+2+31)*2 MHz, so m=2..6 spans the useful trade-off: small m keeps Fmax high but needs more registers, large m saves registers but risks missing the 0.5 us batch deadline. The same accuracy-driven ranges for data_width, n_iter, angle_guard, frac_guard and rounding are used so the two families are directly comparable on the Pareto front.

**Result (code):** 60 evaluations this round, 60 total; 23 feasible; hypervolume 1.401e+05 (n/a).

**LLM decision:** `stop` — This is the final round, and the front is feasible and well-formed, so `infeasible` is not warranted. All three constraints are met by the 8-design Pareto front: throughput (best seen 163 MSPS, front designs 132-138 MSPS, all >= 32), max_abs_err (front spans 2^-12.40 to 2^-14.68, all <= 2^-12), and sys_p99_batch_us (best seen 0.288 <= 0.5). The selection rule (min area_um2) picks the pipelined [data_width=18, n_iter=14, angle_guard=0, frac_guard=2, trunc] design at area_um2=41074 with accuracy_bits=12.4, which clears the error bound with margin. The front already covers the accuracy range 12.4..14.7 bits and area 41074..55909 um^2, and pipelined_m contributed 0 feasible designs, so no unexplored family is likely to extend the front. Stopping here is the correct terminal action.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.401e+05 (gain this round: n/a (first round)).
Feasible designs: 23 of 60 evaluations (17 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 17% violate; best seen 163
- max_abs_err <= 0.000244141: 50% violate; best seen 3.81e-05 (2^-14.68)
- sys_p99_batch_us <= 0.5: 43% violate; best seen 0.288

Pareto front (feasible, 8 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=0 frac_guard=2 rounding=trunc] area_um2=41074, accuracy_bits=12.4, ffs=887, throughput_msps=132, max_abs_err=0.000186 (2^-12.40), power_index=2.35
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=41349, accuracy_bits=12.5, ffs=875, throughput_msps=138, max_abs_err=0.000169 (2^-12.53), power_index=2.34
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=42350, accuracy_bits=12.6, ffs=914, throughput_msps=132, max_abs_err=0.000156 (2^-12.65), power_index=2.42
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=43313, accuracy_bits=12.8, ffs=916, throughput_msps=132, max_abs_err=0.000144 (2^-12.76), power_index=2.45
- pipelined [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=47362, accuracy_bits=13.5, ffs=1001, throughput_msps=138, max_abs_err=8.59e-05 (2^-13.51), power_index=2.67
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
- pipelined [data_width=18 n_iter=17 angle_guard=2 frac_guard=2 rounding=round] area_um2=52760, accuracy_bits=14.4, ffs=1114, throughput_msps=132, max_abs_err=4.73e-05 (2^-14.37), power_index=2.98
- pipelined [data_width=18 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] area_um2=55909, accuracy_bits=14.7, ffs=1180, throughput_msps=132, max_abs_err=3.81e-05 (2^-14.68), power_index=3.15
Front coverage: area_um2 41074..55909 (HV reference 100000); accuracy_bits 12.4..14.7 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 33 evals, 23 feasible; max throughput seen 163 MSPS; best accuracy 14.68 bits; best feasible area_um2=41074; feasible ranges: data_width 17..18, n_iter 14..18, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 27 evals, 0 feasible; max throughput seen 91.1 MSPS; best accuracy 13.60 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (20 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (8 front designs; box front_anchored)
- `pipelined_m` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 40 evaluations this round, 100 total; 39 feasible; hypervolume 2.374e+05 (+69.4%).

**No LLM call** (code's front-mapping round): This is the final round, and the front is feasible and well-formed, so `infeasible` is not warranted. All three constraints are met by the 8-design Pareto front: throughput (best seen 163 MSPS, front designs 132-138 MSPS, all >= 32), max_abs_err (front spans 2^-12.40 to 2^-14.68, all <= 2^-12), and sys_p99_batch_us (best seen 0.288 <= 0.5). The selection rule (min area_um2) picks the pipelined [data_width=18, n_iter=14, angle_guard=0, frac_guard=2, trunc] design at area_um2=41074 with accuracy_bits=12.4, which clears the error bound with margin. The front already covers the accuracy range 12.4..14.7 bits and area 41074..55909 um^2, and pipelined_m contributed 0 feasible designs, so no unexplored family is likely to extend the front. Stopping here is the correct terminal action.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 2.374e+05 (gain this round: +69.4%).
Feasible designs: 39 of 100 evaluations (31 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 22% violate; best seen 163
- max_abs_err <= 0.000244141: 41% violate; best seen 2.15e-07 (2^-22.15)
- sys_p99_batch_us <= 0.5: 48% violate; best seen 0.288

Pareto front (feasible, 12 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=0 frac_guard=2 rounding=trunc] area_um2=41074, accuracy_bits=12.4, ffs=887, throughput_msps=132, max_abs_err=0.000186 (2^-12.40), power_index=2.35
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=41349, accuracy_bits=12.5, ffs=875, throughput_msps=138, max_abs_err=0.000169 (2^-12.53), power_index=2.34
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=42350, accuracy_bits=12.6, ffs=914, throughput_msps=132, max_abs_err=0.000156 (2^-12.65), power_index=2.42
- pipelined [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=47362, accuracy_bits=13.5, ffs=1001, throughput_msps=138, max_abs_err=8.59e-05 (2^-13.51), power_index=2.67
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
- pipelined [data_width=18 n_iter=17 angle_guard=2 frac_guard=2 rounding=round] area_um2=52760, accuracy_bits=14.4, ffs=1114, throughput_msps=132, max_abs_err=4.73e-05 (2^-14.37), power_index=2.98
- pipelined [data_width=21 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=55240, accuracy_bits=14.8, ffs=1188, throughput_msps=119, max_abs_err=3.41e-05 (2^-14.84), power_index=3.15
- pipelined [data_width=21 n_iter=23 angle_guard=0 frac_guard=1 rounding=trunc] area_um2=76097, accuracy_bits=15.8, ffs=1624, throughput_msps=123, max_abs_err=1.69e-05 (2^-15.85), power_index=4.32
- pipelined [data_width=20 n_iter=23 angle_guard=3 frac_guard=1 rounding=round] area_um2=77163, accuracy_bits=16.3, ffs=1626, throughput_msps=119, max_abs_err=1.24e-05 (2^-16.30), power_index=4.35
- pipelined [data_width=25 n_iter=23 angle_guard=0 frac_guard=0 rounding=round] area_um2=86826, accuracy_bits=19.5, ffs=1854, throughput_msps=111, max_abs_err=1.33e-06 (2^-19.52), power_index=4.93
Front coverage: area_um2 41074..86826 (HV reference 100000); accuracy_bits 12.4..19.5 (HV reference 12); data_width on the front 17..25 (registry 8..28).

Per family:
- pipelined: 53 evals, 39 feasible; max throughput seen 163 MSPS; best accuracy 22.15 bits; best feasible area_um2=41074; feasible ranges: data_width 16..25, n_iter 14..30, angle_guard -1..4, frac_guard 0..3
- pipelined_m: 47 evals, 0 feasible; max throughput seen 91.1 MSPS; best accuracy 17.13 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5250 in, 6239 out
- provider-reported cost: $0.0085
- full prompts and replies: `llm_trace.jsonl`

