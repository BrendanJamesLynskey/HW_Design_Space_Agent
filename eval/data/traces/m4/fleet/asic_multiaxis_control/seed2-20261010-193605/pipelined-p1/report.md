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
`pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 39973 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10649 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 867 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 132 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 132 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 121 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.3 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.00017 (2^-12.53) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 11.1 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.25e-05 (2^-14.22) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.44 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (11 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 39973 | 867 | 132.4 | 16 | 2.3 | 0.00017 (2^-12.53) | 12.53 |
| 1 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` | 42350 | 914 | 132.4 | 16 | 2.42 | 0.000156 (2^-12.65) | 12.65 |
| 2 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=3,rounding=trunc` | 43538 | 938 | 127.5 | 16 | 2.49 | 0.000147 (2^-12.74) | 12.74 |
| 3 | `pipelined:data_width=18,n_iter=14,angle_guard=3,frac_guard=3,rounding=round` | 45139 | 954 | 127.5 | 16 | 2.55 | 0.000134 (2^-12.86) | 12.86 |
| 4 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 45892 | 991 | 132.4 | 18 | 2.63 | 8.35e-05 (2^-13.55) | 13.55 |
| 5 | `pipelined:data_width=17,n_iter=16,angle_guard=3,frac_guard=3,rounding=round` | 49473 | 1044 | 132.4 | 18 | 2.79 | 6.42e-05 (2^-13.93) | 13.93 |
| 6 | `pipelined:data_width=24,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 61832 | 1329 | 107.9 | 18 | 3.53 | 3.09e-05 (2^-14.98) | 14.98 |
| 7 | `pipelined:data_width=26,n_iter=16,angle_guard=3,frac_guard=3,rounding=trunc` | 68338 | 1467 | 98.8 | 18 | 3.9 | 3.06e-05 (2^-15.00) | 15.00 |
| 8 | `pipelined:data_width=27,n_iter=16,angle_guard=3,frac_guard=2,rounding=round` | 70581 | 1488 | 96.1 | 18 | 3.98 | 3.05e-05 (2^-15.00) | 15.00 |
| 9 | `pipelined:data_width=18,n_iter=22,angle_guard=3,frac_guard=3,rounding=round` | 71467 | 1504 | 127.5 | 24 | 4.02 | 2.32e-05 (2^-15.40) | 15.40 |
| 10 | `pipelined:data_width=21,n_iter=23,angle_guard=0,frac_guard=2,rounding=trunc` | 78138 | 1665 | 118.9 | 25 | 4.44 | 1.64e-05 (2^-15.90) | 15.90 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec's binding constraint is the system one: a 1 MHz tick dumps 32 requests at once and all 32 must return within 0.5 us (p99). Both of my allowed families are 1-result/cycle, so a burst drains in roughly 31 + latency cycles; with latency = N+2 (pipelined) or ceil(N/m)+2 (pipelined_m) this demands Fmax of roughly 64-95 MHz depending on N and m, well above the trivial throughput_msps >= 32 floor (which only needs Fmax >= 32 MHz). Accuracy max_abs_err <= 2^-12 needs output LSB 2^-(W-2) at or below ~2^-12, i.e. W >= ~13-14, plus enough micro-rotations (N >= ~13) and/or angle_guard to kill the residual-angle error. Area is minimised by pushing W and N down to the accuracy boundary and, for pipelined_m, by pushing m up to the Fmax boundary. I therefore search W 12..18 and N 10..18 (straddling the expected feasible boundary so code can locate it exactly), angle_guard -1..3 and frac_guard 0..3 to let the search trade guard bits against W/N, both rounding modes, and m 2..8. Round 1 is broad exploration over these ranges; later rounds should refine around the feasible front and the reserved tail should map the front over the full W/N/m ranges of whichever family lands on it. I deliberately keep some Fmax margin in the front because the L1 batch bound is optimistic and the cheapest designs that only just pass it may be dropped at L2.*)
- `pipelined` (21 evals): data_width=12..18, n_iter=10..18, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* One register per micro-rotation gives the shortest per-stage combinational path and therefore the highest Fmax of my two families. The 32-request burst must drain in <=0.5 us, so the batch deadline (31 + N + 2 cycles) is the binding constraint; this family is the safe corner that can still meet it at larger N. It also anchors the accuracy/area reference against which pipelined_m's register savings are judged.
- `pipelined_m` (39 evals): data_width=12..18, n_iter=10..18, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* Same 1 result/cycle throughput and identical bit-accurate accuracy as pipelined, but only ceil(N/m) register banks instead of N, so it should dominate on area_um2 (the objective) whenever m is large enough to keep Fmax above the batch requirement. m is the key trade lever: larger m cuts FF area and shortens latency (ceil(N/m)+2), but lengthens the critical path (m chained adders), so the search must find the largest m that still clears the 0.5 us p99 batch bound with margin for the L2 re-simulation. This family gets the larger share because it is the most likely source of the area-minimising front.

**Result (code):** 60 evaluations this round, 60 total; 11 feasible; hypervolume 1.063e+05 (n/a).

**LLM decision:** `stop` — This is the final round, and the run is not infeasible: 11 of 60 evaluations are feasible and a 4-design Pareto front exists. The front spans area_um2 39973..49473 and accuracy_bits 12.5..13.9, all comfortably inside the constraints (max_abs_err best 6.42e-05 vs limit 2.44e-04; throughput 128-132 MSPS vs 32 required; sys_p99_batch best seen 0.263 us vs 0.5 us). The selection rule (min area_um2) is already satisfied by the front's cheapest point, pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] at 39973 um^2, 12.5 accuracy bits, 132 MSPS. pipelined_m produced 0 feasible designs in 39 evals (max throughput 96.1 MSPS), so adding families or widening would not improve the front within the remaining budget; the front is good enough to stop.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.063e+05 (gain this round: n/a (first round)).
Feasible designs: 11 of 60 evaluations (9 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 23% violate; best seen 163
- max_abs_err <= 0.000244141: 75% violate; best seen 6.42e-05 (2^-13.93)
- sys_p99_batch_us <= 0.5: 48% violate; best seen 0.263

Pareto front (feasible, 4 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.5, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53), power_index=2.3
- pipelined [data_width=18 n_iter=14 angle_guard=3 frac_guard=3 rounding=round] area_um2=45139, accuracy_bits=12.9, ffs=954, throughput_msps=128, max_abs_err=0.000134 (2^-12.86), power_index=2.55
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=17 n_iter=16 angle_guard=3 frac_guard=3 rounding=round] area_um2=49473, accuracy_bits=13.9, ffs=1044, throughput_msps=132, max_abs_err=6.42e-05 (2^-13.93), power_index=2.79
Front coverage: area_um2 39973..49473 (HV reference 100000); accuracy_bits 12.5..13.9 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 21 evals, 11 feasible; max throughput seen 163 MSPS; best accuracy 13.93 bits; best feasible area_um2=39973; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 1..3, frac_guard 0..3
- pipelined_m: 39 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 13.86 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (20 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (4 front designs; box front_anchored)
- `pipelined_m` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 40 evaluations this round, 100 total; 29 feasible; hypervolume 1.699e+05 (+59.8%).

**No LLM call** (code's front-mapping round): This is the final round, and the run is not infeasible: 11 of 60 evaluations are feasible and a 4-design Pareto front exists. The front spans area_um2 39973..49473 and accuracy_bits 12.5..13.9, all comfortably inside the constraints (max_abs_err best 6.42e-05 vs limit 2.44e-04; throughput 128-132 MSPS vs 32 required; sys_p99_batch best seen 0.263 us vs 0.5 us). The selection rule (min area_um2) is already satisfied by the front's cheapest point, pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] at 39973 um^2, 12.5 accuracy bits, 132 MSPS. pipelined_m produced 0 feasible designs in 39 evals (max throughput 96.1 MSPS), so adding families or widening would not improve the front within the remaining budget; the front is good enough to stop.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.699e+05 (gain this round: +59.8%).
Feasible designs: 29 of 100 evaluations (27 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 18% violate; best seen 163
- max_abs_err <= 0.000244141: 59% violate; best seen 7.43e-08 (2^-23.68)
- sys_p99_batch_us <= 0.5: 51% violate; best seen 0.263

Pareto front (feasible, 11 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.5, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53), power_index=2.3
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=42350, accuracy_bits=12.6, ffs=914, throughput_msps=132, max_abs_err=0.000156 (2^-12.65), power_index=2.42
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=43538, accuracy_bits=12.7, ffs=938, throughput_msps=128, max_abs_err=0.000147 (2^-12.74), power_index=2.49
- pipelined [data_width=18 n_iter=14 angle_guard=3 frac_guard=3 rounding=round] area_um2=45139, accuracy_bits=12.9, ffs=954, throughput_msps=128, max_abs_err=0.000134 (2^-12.86), power_index=2.55
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=24 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=61832, accuracy_bits=15, ffs=1329, throughput_msps=108, max_abs_err=3.09e-05 (2^-14.98), power_index=3.53
- pipelined [data_width=26 n_iter=16 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=68338, accuracy_bits=15, ffs=1467, throughput_msps=98.8, max_abs_err=3.06e-05 (2^-15.00), power_index=3.9
- pipelined [data_width=27 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] area_um2=70581, accuracy_bits=15, ffs=1488, throughput_msps=96.1, max_abs_err=3.05e-05 (2^-15.00), power_index=3.98
- pipelined [data_width=18 n_iter=22 angle_guard=3 frac_guard=3 rounding=round] area_um2=71467, accuracy_bits=15.4, ffs=1504, throughput_msps=128, max_abs_err=2.32e-05 (2^-15.40), power_index=4.02
- pipelined [data_width=21 n_iter=23 angle_guard=0 frac_guard=2 rounding=trunc] area_um2=78138, accuracy_bits=15.9, ffs=1665, throughput_msps=119, max_abs_err=1.64e-05 (2^-15.90), power_index=4.44
Front coverage: area_um2 39973..78138 (HV reference 100000); accuracy_bits 12.5..15.9 (HV reference 12); data_width on the front 17..27 (registry 8..28).

Per family:
- pipelined: 41 evals, 29 feasible; max throughput seen 163 MSPS; best accuracy 23.68 bits; best feasible area_um2=39973; feasible ranges: data_width 16..27, n_iter 14..23, angle_guard -1..3, frac_guard 0..4
- pipelined_m: 59 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 18.96 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5839 in, 5429 out
- provider-reported cost: $0.0069
- full prompts and replies: `llm_trace.jsonl`

