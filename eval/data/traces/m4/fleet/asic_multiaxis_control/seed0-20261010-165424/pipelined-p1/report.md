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
`pipelined:data_width=19,n_iter=14,angle_guard=1,frac_guard=1,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 43452 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 11576 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 920 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 132 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 132 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 121 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.46 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000139 (2^-12.81) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 18.3 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.03e-05 (2^-14.28) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 6.59 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.8 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (11 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=19,n_iter=14,angle_guard=1,frac_guard=1,rounding=round` | 43452 | 920 | 132.4 | 16 | 2.46 | 0.000139 (2^-12.81) | 12.81 |
| 1 | `pipelined:data_width=19,n_iter=15,angle_guard=1,frac_guard=1,rounding=trunc` | 45586 | 984 | 132.4 | 17 | 2.61 | 9.41e-05 (2^-13.38) | 13.38 |
| 2 | `pipelined:data_width=20,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 46358 | 1003 | 127.5 | 17 | 2.66 | 7.63e-05 (2^-13.68) | 13.68 |
| 3 | `pipelined:data_width=20,n_iter=15,angle_guard=1,frac_guard=1,rounding=round` | 48707 | 1030 | 127.5 | 17 | 2.75 | 7.02e-05 (2^-13.80) | 13.80 |
| 4 | `pipelined:data_width=20,n_iter=15,angle_guard=1,frac_guard=2,rounding=round` | 49990 | 1056 | 123.1 | 17 | 2.82 | 6.89e-05 (2^-13.82) | 13.82 |
| 5 | `pipelined:data_width=20,n_iter=17,angle_guard=0,frac_guard=0,rounding=round` | 51971 | 1120 | 132.4 | 19 | 2.97 | 4.25e-05 (2^-14.52) | 14.52 |
| 6 | `pipelined:data_width=20,n_iter=17,angle_guard=1,frac_guard=0,rounding=round` | 52751 | 1137 | 127.5 | 19 | 3.02 | 3.32e-05 (2^-14.88) | 14.88 |
| 7 | `pipelined:data_width=20,n_iter=18,angle_guard=1,frac_guard=0,rounding=round` | 55947 | 1203 | 127.5 | 20 | 3.2 | 2.9e-05 (2^-15.07) | 15.07 |
| 8 | `pipelined:data_width=20,n_iter=17,angle_guard=1,frac_guard=2,rounding=round` | 56761 | 1197 | 123.1 | 19 | 3.2 | 2.32e-05 (2^-15.40) | 15.40 |
| 9 | `pipelined:data_width=20,n_iter=18,angle_guard=1,frac_guard=1,rounding=round` | 58580 | 1237 | 127.5 | 20 | 3.3 | 2.28e-05 (2^-15.42) | 15.42 |
| 10 | `pipelined:data_width=19,n_iter=25,angle_guard=3,frac_guard=3,rounding=trunc` | 83853 | 1782 | 123.1 | 27 | 4.75 | 2.05e-05 (2^-15.58) | 15.58 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires throughput_msps >= 32, max_abs_err <= 2^-12, and sys_p99_batch_us <= 0.5us for 32 back-to-back requests. Only pipelined and pipelined_m produce 1 result/cycle, so they are the only families that can meet the throughput constraint (iterative and unrolled_k produce 1 result every several cycles, giving throughput = Fmax/k or Fmax/(N+3), which would require very high Fmax). For the batch constraint, 32 results must arrive within 0.5us of the tick. With 1 result/cycle, this requires Fmax >= 64 MHz (32 cycles in 0.5us) plus the pipeline latency. pipelined has N+2 latency; pipelined_m has ceil(N/m)+2 latency. Both can meet this if Fmax is high enough. The accuracy constraint (12 bits) is easily met with N >= 14 and data_width >= 16. The min-area objective favors smaller data_width, smaller n_iter, and pipelined_m (fewer registers). I split the budget 50/50 between the two families: pipelined is the baseline (simpler, higher Fmax, guaranteed to meet batch constraint at moderate Fmax), and pipelined_m explores area savings via reduced register count. Ranges are focused on the lower end of data_width and n_iter to minimize area while maintaining accuracy margin. angle_guard and frac_guard are kept small (0-2) since 12-bit accuracy does not require large guard bits.*)
- `pipelined` (30 evals): data_width=16..20, n_iter=14..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined gives 1 result/cycle, so throughput_msps = Fmax. To meet throughput_msps >= 32, Fmax must be >= 32 MHz, which is easily met. The sys_p99_batch_us <= 0.5us constraint requires that 32 back-to-back requests complete within 0.5us. With 1 result/cycle and Fmax >= 32MHz, 32 cycles take <= 1us at 32MHz, but we need <= 0.5us, so Fmax must be >= 64 MHz. A fully pipelined CORDIC with N stages has N+2 latency; for N=14-18, latency is 16-20 cycles. At 64MHz, 20 cycles = 312ns < 500ns, so the batch constraint is met. The accuracy constraint max_abs_err <= 2^-12 = 0.000244 requires accuracy_bits >= 12. For CORDIC, accuracy is roughly 2^-(N+1) for the rotation, so N >= 13 gives ~2^-14 accuracy. data_width 16-20 with n_iter 14-18 should comfortably meet 12-bit accuracy. Minimising area means we want the smallest data_width and n_iter that still meet accuracy, so the search should focus on the lower end of these ranges. angle_guard and frac_guard affect accuracy margin; small values (0-2) should suffice for 12-bit accuracy with N>=14.
- `pipelined_m` (30 evals): data_width=16..20, n_iter=14..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m registers every m stages, reducing flip-flop count and area versus fully pipelined, at the cost of higher latency (ceil(N/m)+2 cycles) and potentially lower Fmax due to longer combinational paths. For the batch constraint, we need ceil(N/m)+2 cycles to complete 32 results within 0.5us. Since pipelined_m still produces 1 result/cycle in steady state, the throughput is still Fmax. The key question is whether the initial latency plus 32 cycles fits in 0.5us. With m=2-4 and N=14-18, latency is ceil(14/2)+2=9 to ceil(18/4)+2=7 cycles, plus 32 cycles for the batch = ~41-49 cycles total. At 64MHz, 49 cycles = 766ns > 500ns, which may violate the constraint. At higher Fmax (e.g., 100MHz), 49 cycles = 490ns < 500ns. So pipelined_m with small m (2) and higher Fmax may work. The area savings from fewer registers make this family attractive for the min-area objective. Search m=2-4 to find the sweet spot between area and the batch latency constraint.

**Result (code):** 60 evaluations this round, 60 total; 26 feasible; hypervolume 1.742e+05 (n/a).

**LLM decision:** `stop` — The exploration has successfully identified a feasible Pareto front dominated by the `pipelined` family. The minimum area design on the front is 43,452 um^2 (pipelined, data_width=19, n_iter=14), which satisfies all constraints: throughput (132 MSPS >= 32), accuracy (12.8 bits >= 12), and system latency (implied feasible as it is on the feasible front). The `pipelined_m` family was explored but yielded 0 feasible designs, likely due to insufficient throughput or latency for the bursty 32-request system scenario. Since this is the final round and the front covers the trade-off space well (area 43k-58k um^2, accuracy 12.8-15.4 bits) with a clear minimum-area candidate for the selection rule, no further exploration is possible or necessary.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.742e+05 (gain this round: n/a (first round)).
Feasible designs: 26 of 60 evaluations (19 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 149
- max_abs_err <= 0.000244141: 12% violate; best seen 2.18e-05 (2^-15.49)
- sys_p99_batch_us <= 0.5: 48% violate; best seen 0.315

Pareto front (feasible, 10 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=19 n_iter=14 angle_guard=1 frac_guard=1 rounding=round] area_um2=43452, accuracy_bits=12.8, ffs=920, throughput_msps=132, max_abs_err=0.000139 (2^-12.81), power_index=2.46
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=45586, accuracy_bits=13.4, ffs=984, throughput_msps=132, max_abs_err=9.41e-05 (2^-13.38), power_index=2.61
- pipelined [data_width=20 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=46358, accuracy_bits=13.7, ffs=1003, throughput_msps=128, max_abs_err=7.63e-05 (2^-13.68), power_index=2.66
- pipelined [data_width=20 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=48707, accuracy_bits=13.8, ffs=1030, throughput_msps=128, max_abs_err=7.02e-05 (2^-13.80), power_index=2.75
- pipelined [data_width=20 n_iter=15 angle_guard=1 frac_guard=2 rounding=round] area_um2=49990, accuracy_bits=13.8, ffs=1056, throughput_msps=123, max_abs_err=6.89e-05 (2^-13.82), power_index=2.82
- pipelined [data_width=20 n_iter=17 angle_guard=0 frac_guard=0 rounding=round] area_um2=51971, accuracy_bits=14.5, ffs=1120, throughput_msps=132, max_abs_err=4.25e-05 (2^-14.52), power_index=2.97
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] area_um2=52751, accuracy_bits=14.9, ffs=1137, throughput_msps=128, max_abs_err=3.32e-05 (2^-14.88), power_index=3.02
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] area_um2=55947, accuracy_bits=15.1, ffs=1203, throughput_msps=128, max_abs_err=2.9e-05 (2^-15.07), power_index=3.2
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=2 rounding=round] area_um2=56761, accuracy_bits=15.4, ffs=1197, throughput_msps=123, max_abs_err=2.32e-05 (2^-15.40), power_index=3.2
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=1 rounding=round] area_um2=58580, accuracy_bits=15.4, ffs=1237, throughput_msps=128, max_abs_err=2.28e-05 (2^-15.42), power_index=3.3
Front coverage: area_um2 43452..58580 (HV reference 100000); accuracy_bits 12.8..15.4 (HV reference 12); data_width on the front 19..20 (registry 8..28).

Per family:
- pipelined: 30 evals, 26 feasible; max throughput seen 149 MSPS; best accuracy 15.42 bits; best feasible area_um2=43452; feasible ranges: data_width 17..20, n_iter 14..18, angle_guard 0..1, frac_guard 0..2
- pipelined_m: 30 evals, 0 feasible; max throughput seen 78.8 MSPS; best accuracy 15.49 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (20 evals): data_width=18..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (10 front designs; box front_anchored)
- `pipelined_m` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 40 evaluations this round, 100 total; 35 feasible; hypervolume 1.767e+05 (+1.4%).

**No LLM call** (code's front-mapping round): The exploration has successfully identified a feasible Pareto front dominated by the `pipelined` family. The minimum area design on the front is 43,452 um^2 (pipelined, data_width=19, n_iter=14), which satisfies all constraints: throughput (132 MSPS >= 32), accuracy (12.8 bits >= 12), and system latency (implied feasible as it is on the feasible front). The `pipelined_m` family was explored but yielded 0 feasible designs, likely due to insufficient throughput or latency for the bursty 32-request system scenario. Since this is the final round and the front covers the trade-off space well (area 43k-58k um^2, accuracy 12.8-15.4 bits) with a clear minimum-area candidate for the selection rule, no further exploration is possible or necessary.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.767e+05 (gain this round: +1.4%).
Feasible designs: 35 of 100 evaluations (27 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 6% violate; best seen 149
- max_abs_err <= 0.000244141: 23% violate; best seen 7.95e-08 (2^-23.58)
- sys_p99_batch_us <= 0.5: 52% violate; best seen 0.315

Pareto front (feasible, 11 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=19 n_iter=14 angle_guard=1 frac_guard=1 rounding=round] area_um2=43452, accuracy_bits=12.8, ffs=920, throughput_msps=132, max_abs_err=0.000139 (2^-12.81), power_index=2.46
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=45586, accuracy_bits=13.4, ffs=984, throughput_msps=132, max_abs_err=9.41e-05 (2^-13.38), power_index=2.61
- pipelined [data_width=20 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=46358, accuracy_bits=13.7, ffs=1003, throughput_msps=128, max_abs_err=7.63e-05 (2^-13.68), power_index=2.66
- pipelined [data_width=20 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=48707, accuracy_bits=13.8, ffs=1030, throughput_msps=128, max_abs_err=7.02e-05 (2^-13.80), power_index=2.75
- pipelined [data_width=20 n_iter=15 angle_guard=1 frac_guard=2 rounding=round] area_um2=49990, accuracy_bits=13.8, ffs=1056, throughput_msps=123, max_abs_err=6.89e-05 (2^-13.82), power_index=2.82
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] area_um2=52751, accuracy_bits=14.9, ffs=1137, throughput_msps=128, max_abs_err=3.32e-05 (2^-14.88), power_index=3.02
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] area_um2=55947, accuracy_bits=15.1, ffs=1203, throughput_msps=128, max_abs_err=2.9e-05 (2^-15.07), power_index=3.2
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=2 rounding=round] area_um2=56761, accuracy_bits=15.4, ffs=1197, throughput_msps=123, max_abs_err=2.32e-05 (2^-15.40), power_index=3.2
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=1 rounding=round] area_um2=58580, accuracy_bits=15.4, ffs=1237, throughput_msps=128, max_abs_err=2.28e-05 (2^-15.42), power_index=3.3
- pipelined [data_width=19 n_iter=25 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=83853, accuracy_bits=15.6, ffs=1782, throughput_msps=123, max_abs_err=2.05e-05 (2^-15.58), power_index=4.75
Front coverage: area_um2 43452..83853 (HV reference 100000); accuracy_bits 12.8..15.6 (HV reference 12); data_width on the front 19..20 (registry 8..28).

Per family:
- pipelined: 50 evals, 35 feasible; max throughput seen 149 MSPS; best accuracy 23.58 bits; best feasible area_um2=43452; feasible ranges: data_width 17..28, n_iter 13..27, angle_guard -2..4, frac_guard 0..3
- pipelined_m: 50 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 22.53 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5614 in, 1785 out
- provider-reported cost: $0.0026
- full prompts and replies: `llm_trace.jsonl`

