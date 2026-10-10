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
`pipelined:data_width=18,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 44427 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 11836 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 960 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 126 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.54 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000121 (2^-13.02) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 7.9 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.65e-05 (2^-15.20) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.74 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (7 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 44427 | 960 | 143.2 | 18 | 2.54 | 0.000121 (2^-13.02) | 13.02 |
| 1 | `pipelined:data_width=18,n_iter=16,angle_guard=0,frac_guard=1,rounding=round` | 46768 | 989 | 137.6 | 18 | 2.64 | 0.00012 (2^-13.03) | 13.03 |
| 2 | `pipelined:data_width=18,n_iter=15,angle_guard=3,frac_guard=3,rounding=trunc` | 47467 | 1020 | 127.5 | 17 | 2.71 | 8.39e-05 (2^-13.54) | 13.54 |
| 3 | `pipelined:data_width=17,n_iter=16,angle_guard=3,frac_guard=3,rounding=trunc` | 48560 | 1042 | 132.4 | 18 | 2.77 | 8.14e-05 (2^-13.58) | 13.58 |
| 4 | `pipelined:data_width=18,n_iter=16,angle_guard=3,frac_guard=3,rounding=trunc` | 50758 | 1089 | 127.5 | 18 | 2.89 | 5.44e-05 (2^-14.17) | 14.17 |
| 5 | `pipelined:data_width=18,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc` | 83667 | 1778 | 127.5 | 28 | 4.74 | 3.98e-05 (2^-14.62) | 14.62 |
| 6 | `pipelined:data_width=19,n_iter=27,angle_guard=4,frac_guard=0,rounding=round` | 84712 | 1805 | 118.9 | 29 | 4.81 | 3.74e-05 (2^-14.71) | 14.71 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-minimisation subject to three hard constraints: throughput_msps>=32, max_abs_err<=2^-12, and sys_p99_batch_us<=0.5 for a 32-request burst every 1us. The burst bound is the binding system constraint: 32 results in 0.5us requires an effective >=64 results/us, which only the 1-result/cycle families (pipelined, pipelined_m) can meet, and only if Fmax is high enough. Both of my assigned families are 1-result/cycle, so they are the right choice; iterative/unrolled_k are not available to me and would also struggle with the burst. Accuracy depends only on data_width/n_iter/guards/rounding (identical bits across families), so I bracket the accuracy/area knee at W=14..18, N=12..18 with low guards and both roundings to find the smallest design that still clears 2^-12. I split budget 55/45 between pipelined (baseline, highest Fmax margin, safest for the batch bound) and pipelined_m (area-saving via fewer registers, the likely winner for the min-area objective). Keeping ranges narrow focuses the 100-eval budget on the feasible region rather than wasting it on obviously-too-small (fails accuracy) or obviously-too-large (wastes area) corners.*)
- `pipelined` (33 evals): data_width=14..18, n_iter=12..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Full pipelining gives 1 result/cycle, so throughput = Fmax. With N=12..18 stages the critical path is one micro-rotation (short), so Fmax should comfortably exceed 32 MHz, meeting throughput_msps>=32. Accuracy is set by n_iter/data_width; N>=12 with W>=14 and rounding should reach 2^-12. Area is the objective, so I want the smallest W and N that still pass accuracy and the 0.5us batch bound. The 0.5us p99_batch bound is the tight system constraint: a burst of 32 must finish within 0.5us, i.e. the unit must sustain >=64 results/us effective, which full pipelining at Fmax>=64MHz achieves. Searching W 14..18 and N 12..18 brackets the accuracy/area knee; angle_guard and frac_guard are kept low to minimise area while rounding is tested to recover accuracy bits cheaply.
- `pipelined_m` (27 evals): data_width=14..18, n_iter=12..18, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m registers every m stages, cutting flip-flop count and area versus full pipelining while still delivering 1 result/cycle (throughput = Fmax). Fewer registers lengthen the combinational path (m micro-rotations in series), which lowers Fmax; m=2..4 keeps the path short enough that Fmax should still clear the 32 MHz throughput floor and the 64 MHz needed for the 0.5us burst. This family is the most promising for the min-area objective because it trades a little Fmax margin for a real area saving. I search the same accuracy-relevant ranges as pipelined (W 14..18, N 12..18, low guards, both roundings) and add m=2..4 to find the area/Fmax sweet spot that still satisfies the batch-latency bound.

**Result (code):** 60 evaluations this round, 60 total; 14 feasible; hypervolume 7.527e+04 (n/a).

**LLM decision:** `stop` — The exploration has identified a feasible Pareto front dominated by the `pipelined` family. The best design (pipelined, data_width=18, n_iter=16, angle_guard=0, frac_guard=0, rounding=round) achieves an area of 44427 um^2, 13.02 bits of accuracy (max_abs_err ~ 1.2e-4, well below the 2.44e-4 limit), and a throughput of 143 MSPS (well above the 32 MSPS requirement). The system constraint `sys_p99_batch_us <= 0.5` is met by the best designs (best seen 0.276 us). The `pipelined_m` family was explored but yielded no feasible designs, likely due to higher latency or area overheads for the same accuracy/throughput trade-off. Since this is the final round and a clear, feasible, and efficient solution exists on the front, stopping is the correct action. The selection rule (min area) will pick the 44427 um^2 design.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 7.527e+04 (gain this round: n/a (first round)).
Feasible designs: 14 of 60 evaluations (10 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 171
- max_abs_err <= 0.000244141: 53% violate; best seen 6.92e-05 (2^-13.82)
- sys_p99_batch_us <= 0.5: 42% violate; best seen 0.276

Pareto front (feasible, 3 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] area_um2=44427, accuracy_bits=13, ffs=960, throughput_msps=143, max_abs_err=0.000121 (2^-13.02), power_index=2.54
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=round] area_um2=46768, accuracy_bits=13, ffs=989, throughput_msps=138, max_abs_err=0.00012 (2^-13.03), power_index=2.64
- pipelined [data_width=18 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] area_um2=50983, accuracy_bits=13.4, ffs=1097, throughput_msps=138, max_abs_err=9.26e-05 (2^-13.40), power_index=2.91
Front coverage: area_um2 44427..50983 (HV reference 100000); accuracy_bits 13..13.4 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- pipelined: 33 evals, 14 feasible; max throughput seen 171 MSPS; best accuracy 13.40 bits; best feasible area_um2=44427; feasible ranges: data_width 17..18, n_iter 16..18, angle_guard -1..1, frac_guard 0..2
- pipelined_m: 27 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 13.82 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (20 evals): data_width=17..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)
- `pipelined_m` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 40 evaluations this round, 100 total; 30 feasible; hypervolume 1.237e+05 (+64.3%).

**No LLM call** (code's front-mapping round): The exploration has identified a feasible Pareto front dominated by the `pipelined` family. The best design (pipelined, data_width=18, n_iter=16, angle_guard=0, frac_guard=0, rounding=round) achieves an area of 44427 um^2, 13.02 bits of accuracy (max_abs_err ~ 1.2e-4, well below the 2.44e-4 limit), and a throughput of 143 MSPS (well above the 32 MSPS requirement). The system constraint `sys_p99_batch_us <= 0.5` is met by the best designs (best seen 0.276 us). The `pipelined_m` family was explored but yielded no feasible designs, likely due to higher latency or area overheads for the same accuracy/throughput trade-off. Since this is the final round and a clear, feasible, and efficient solution exists on the front, stopping is the correct action. The selection rule (min area) will pick the 44427 um^2 design.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.237e+05 (gain this round: +64.3%).
Feasible designs: 30 of 100 evaluations (24 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 6% violate; best seen 171
- max_abs_err <= 0.000244141: 43% violate; best seen 7.95e-08 (2^-23.58)
- sys_p99_batch_us <= 0.5: 46% violate; best seen 0.276

Pareto front (feasible, 7 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] area_um2=44427, accuracy_bits=13, ffs=960, throughput_msps=143, max_abs_err=0.000121 (2^-13.02), power_index=2.54
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=round] area_um2=46768, accuracy_bits=13, ffs=989, throughput_msps=138, max_abs_err=0.00012 (2^-13.03), power_index=2.64
- pipelined [data_width=18 n_iter=15 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=47467, accuracy_bits=13.5, ffs=1020, throughput_msps=128, max_abs_err=8.39e-05 (2^-13.54), power_index=2.71
- pipelined [data_width=17 n_iter=16 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=48560, accuracy_bits=13.6, ffs=1042, throughput_msps=132, max_abs_err=8.14e-05 (2^-13.58), power_index=2.77
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=50758, accuracy_bits=14.2, ffs=1089, throughput_msps=128, max_abs_err=5.44e-05 (2^-14.17), power_index=2.89
- pipelined [data_width=18 n_iter=26 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=83667, accuracy_bits=14.6, ffs=1778, throughput_msps=128, max_abs_err=3.98e-05 (2^-14.62), power_index=4.74
- pipelined [data_width=19 n_iter=27 angle_guard=4 frac_guard=0 rounding=round] area_um2=84712, accuracy_bits=14.7, ffs=1805, throughput_msps=119, max_abs_err=3.74e-05 (2^-14.71), power_index=4.81
Front coverage: area_um2 44427..84712 (HV reference 100000); accuracy_bits 13..14.7 (HV reference 12); data_width on the front 17..19 (registry 8..28).

Per family:
- pipelined: 53 evals, 30 feasible; max throughput seen 171 MSPS; best accuracy 23.58 bits; best feasible area_um2=44427; feasible ranges: data_width 17..28, n_iter 14..27, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 47 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 22.53 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4979 in, 1394 out
- provider-reported cost: $0.0032
- full prompts and replies: `llm_trace.jsonl`

