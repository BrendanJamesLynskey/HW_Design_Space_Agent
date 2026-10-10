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
`pipelined:data_width=17,n_iter=17,angle_guard=4,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 48071 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 12807 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 1036 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 128 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 128 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 19 | exact: schedule |
| latency_ns | 149 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.75 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000146 (2^-12.74) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 4.79 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 3.77e-05 (2^-14.70) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.23 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.7 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (9 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=17,n_iter=17,angle_guard=4,frac_guard=0,rounding=round` | 48071 | 1036 | 127.5 | 19 | 2.75 | 0.000146 (2^-12.74) | 12.74 |
| 1 | `pipelined:data_width=20,n_iter=17,angle_guard=2,frac_guard=0,rounding=trunc` | 53531 | 1153 | 123.1 | 19 | 3.06 | 4.61e-05 (2^-14.40) | 14.40 |
| 2 | `pipelined:data_width=20,n_iter=17,angle_guard=2,frac_guard=2,rounding=trunc` | 56475 | 1212 | 123.1 | 19 | 3.22 | 2.57e-05 (2^-15.25) | 15.25 |
| 3 | `pipelined:data_width=20,n_iter=17,angle_guard=3,frac_guard=2,rounding=trunc` | 57255 | 1229 | 118.9 | 19 | 3.27 | 2.37e-05 (2^-15.36) | 15.36 |
| 4 | `pipelined:data_width=20,n_iter=17,angle_guard=2,frac_guard=4,rounding=trunc` | 59420 | 1271 | 115.0 | 19 | 3.38 | 2.22e-05 (2^-15.46) | 15.46 |
| 5 | `pipelined:data_width=20,n_iter=19,angle_guard=4,frac_guard=0,rounding=round` | 61767 | 1326 | 115.0 | 21 | 3.52 | 2.17e-05 (2^-15.49) | 15.49 |
| 6 | `pipelined:data_width=20,n_iter=19,angle_guard=4,frac_guard=2,rounding=round` | 66157 | 1395 | 115.0 | 21 | 3.73 | 1.04e-05 (2^-16.56) | 16.56 |
| 7 | `pipelined:data_width=25,n_iter=18,angle_guard=1,frac_guard=1,rounding=round` | 71244 | 1502 | 107.9 | 20 | 4.02 | 8.01e-06 (2^-16.93) | 16.93 |
| 8 | `pipelined:data_width=20,n_iter=20,angle_guard=4,frac_guard=4,rounding=trunc` | 72132 | 1538 | 115.0 | 22 | 4.09 | 7.11e-06 (2^-17.10) | 17.10 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Both families I own are fully pipelined and emit 1 result/cycle, so the throughput_msps >= 32 constraint is met at any plausible Fmax and is not the discriminator. The two binding constraints are accuracy (max_abs_err <= 2^-12) and the system burst bound (32 requests issued at one 1 MHz tick, all back within 0.5 us). Accuracy depends only on W, N, angle_guard, frac_guard and rounding, so I search the accuracy-relevant ranges once and let both families share them: W from 13 (smallest width whose output LSB 2^-(W-2) can reach 2^-12 with rounding; W=12 cannot) to 20, N from 10 (below the ~13-iteration accuracy threshold, to let the optimiser locate the feasibility boundary) to 20, angle_guard -2..4 and frac_guard 0..4 to let the optimiser trim angle-path and datapath widths, and both rounding modes. The burst bound is what separates the families: pipelined latency is (N+2+31)/Fmax, pipelined_m is (ceil(N/m)+2+31)/Fmax, so m is a genuine area-vs-Fmax-vs-latency knob and is swept 2..8. The Pareto front is therefore area_um2 vs accuracy_bits, with the min-area feasible point sitting where accuracy just clears 12 bits and m is as large as the 0.5 us batch bound allows. I weight pipelined_m 0.6 because it should dominate the low-area end, and keep pipelined at 0.4 as the high-Fmax anchor and fallback. I keep the first round to a subset of the 100-eval share so later rounds can refine the accuracy-feasibility boundary and the largest feasible m; code's reserved mapping pass should then cover the full ranges of whichever of these two families lands on the front.*)
- `pipelined` (24 evals): data_width=13..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Fully pipelined, 1 result/cycle, one register per micro-rotation: the highest-Fmax family I own, so it clears the burst-latency constraint (N+2+31 cycles inside 0.5 us) even at large N. It anchors the high-accuracy / high-Fmax end of the front and is the safe fallback if pipelined_m cannot close timing at any m. Its cost is one register bank per stage, so it will be area-dominated by pipelined_m at equal accuracy; I still need it to bound the front and to keep a feasible design if the batch bound bites.
- `pipelined_m` (36 evals): data_width=13..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Same bit-exact accuracy as pipelined for the same (W, N, guards, rounding) but registers only every m stages, so it trades register area against Fmax: larger m means fewer FFs (lower area) but a longer combinational path and lower Fmax, which pushes the batch latency (ceil(N/m)+2+31)/Fmax up. Since the objective is min area and the selection rule is min area, this is the family most likely to own the low-area end of the front; m 2..8 is the main structural lever and must be swept fully to find the largest m that still meets sys_p99_batch_us <= 0.5. I give it the larger share because the front is expected to be dominated by it, with pipelined only as the timing-safe corner.

**Result (code):** 60 evaluations this round, 60 total; 11 feasible; hypervolume 2.114e+05 (n/a).

**LLM decision:** `stop` — Final round: the registry is not infeasible — round 1 produced a feasible Pareto front of 7 designs (8 unique feasible of 60 evals), all satisfying the three constraints. The min-area corner the selection rule picks (pipelined, data_width=17, n_iter=17, angle_guard=4, frac_guard=0, round) is 48071 um^2 at 12.7 accuracy bits, 128 MSPS throughput (>= 32 required) and 2^-12.74 max error (<= 2^-12 required), and the front's best sys_p99_batch_us seen is 0.293 us (<= 0.5 required), so the constraint set is reachable with margin. The front already spans the accuracy objective well (12.7..17.1 bits vs HV ref 12) and area 48071..72132 vs HV ref 100000, i.e. it covers the useful trade-off region; pipelined_m contributed 0 feasible designs (max 78.8 MSPS, best 15.92 bits) and no unexplored family remains, so further exploration would not change the selection outcome. Stopping with the front as mapped.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 2.114e+05 (gain this round: n/a (first round)).
Feasible designs: 11 of 60 evaluations (8 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 17% violate; best seen 163
- max_abs_err <= 0.000244141: 60% violate; best seen 7.11e-06 (2^-17.10)
- sys_p99_batch_us <= 0.5: 58% violate; best seen 0.293

Pareto front (feasible, 7 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=17 angle_guard=4 frac_guard=0 rounding=round] area_um2=48071, accuracy_bits=12.7, ffs=1036, throughput_msps=128, max_abs_err=0.000146 (2^-12.74), power_index=2.75
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=53531, accuracy_bits=14.4, ffs=1153, throughput_msps=123, max_abs_err=4.61e-05 (2^-14.40), power_index=3.06
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=56475, accuracy_bits=15.2, ffs=1212, throughput_msps=123, max_abs_err=2.57e-05 (2^-15.25), power_index=3.22
- pipelined [data_width=20 n_iter=17 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=57255, accuracy_bits=15.4, ffs=1229, throughput_msps=119, max_abs_err=2.37e-05 (2^-15.36), power_index=3.27
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=4 rounding=trunc] area_um2=59420, accuracy_bits=15.5, ffs=1271, throughput_msps=115, max_abs_err=2.22e-05 (2^-15.46), power_index=3.38
- pipelined [data_width=20 n_iter=20 angle_guard=2 frac_guard=2 rounding=round] area_um2=67840, accuracy_bits=16.5, ffs=1429, throughput_msps=123, max_abs_err=1.11e-05 (2^-16.46), power_index=3.82
- pipelined [data_width=20 n_iter=20 angle_guard=4 frac_guard=4 rounding=trunc] area_um2=72132, accuracy_bits=17.1, ffs=1538, throughput_msps=115, max_abs_err=7.11e-06 (2^-17.10), power_index=4.09
Front coverage: area_um2 48071..72132 (HV reference 100000); accuracy_bits 12.7..17.1 (HV reference 12); data_width on the front 17..20 (registry 8..28).

Per family:
- pipelined: 24 evals, 11 feasible; max throughput seen 163 MSPS; best accuracy 17.10 bits; best feasible area_um2=48071; feasible ranges: data_width 17..20, n_iter 17..20, angle_guard 2..4, frac_guard 0..4
- pipelined_m: 36 evals, 0 feasible; max throughput seen 78.8 MSPS; best accuracy 15.92 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (20 evals): data_width=16..28, n_iter=15..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (7 front designs; box front_anchored)
- `pipelined_m` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 40 evaluations this round, 100 total; 23 feasible; hypervolume 2.141e+05 (+1.3%).

**No LLM call** (code's front-mapping round): Final round: the registry is not infeasible — round 1 produced a feasible Pareto front of 7 designs (8 unique feasible of 60 evals), all satisfying the three constraints. The min-area corner the selection rule picks (pipelined, data_width=17, n_iter=17, angle_guard=4, frac_guard=0, round) is 48071 um^2 at 12.7 accuracy bits, 128 MSPS throughput (>= 32 required) and 2^-12.74 max error (<= 2^-12 required), and the front's best sys_p99_batch_us seen is 0.293 us (<= 0.5 required), so the constraint set is reachable with margin. The front already spans the accuracy objective well (12.7..17.1 bits vs HV ref 12) and area 48071..72132 vs HV ref 100000, i.e. it covers the useful trade-off region; pipelined_m contributed 0 feasible designs (max 78.8 MSPS, best 15.92 bits) and no unexplored family remains, so further exploration would not change the selection outcome. Stopping with the front as mapped.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 2.141e+05 (gain this round: +1.3%).
Feasible designs: 23 of 100 evaluations (20 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 16% violate; best seen 163
- max_abs_err <= 0.000244141: 49% violate; best seen 7.31e-07 (2^-20.38)
- sys_p99_batch_us <= 0.5: 61% violate; best seen 0.293

Pareto front (feasible, 9 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=17 angle_guard=4 frac_guard=0 rounding=round] area_um2=48071, accuracy_bits=12.7, ffs=1036, throughput_msps=128, max_abs_err=0.000146 (2^-12.74), power_index=2.75
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=53531, accuracy_bits=14.4, ffs=1153, throughput_msps=123, max_abs_err=4.61e-05 (2^-14.40), power_index=3.06
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=56475, accuracy_bits=15.2, ffs=1212, throughput_msps=123, max_abs_err=2.57e-05 (2^-15.25), power_index=3.22
- pipelined [data_width=20 n_iter=17 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=57255, accuracy_bits=15.4, ffs=1229, throughput_msps=119, max_abs_err=2.37e-05 (2^-15.36), power_index=3.27
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=4 rounding=trunc] area_um2=59420, accuracy_bits=15.5, ffs=1271, throughput_msps=115, max_abs_err=2.22e-05 (2^-15.46), power_index=3.38
- pipelined [data_width=20 n_iter=19 angle_guard=4 frac_guard=0 rounding=round] area_um2=61767, accuracy_bits=15.5, ffs=1326, throughput_msps=115, max_abs_err=2.17e-05 (2^-15.49), power_index=3.52
- pipelined [data_width=20 n_iter=19 angle_guard=4 frac_guard=2 rounding=round] area_um2=66157, accuracy_bits=16.6, ffs=1395, throughput_msps=115, max_abs_err=1.04e-05 (2^-16.56), power_index=3.73
- pipelined [data_width=25 n_iter=18 angle_guard=1 frac_guard=1 rounding=round] area_um2=71244, accuracy_bits=16.9, ffs=1502, throughput_msps=108, max_abs_err=8.01e-06 (2^-16.93), power_index=4.02
- pipelined [data_width=20 n_iter=20 angle_guard=4 frac_guard=4 rounding=trunc] area_um2=72132, accuracy_bits=17.1, ffs=1538, throughput_msps=115, max_abs_err=7.11e-06 (2^-17.10), power_index=4.09
Front coverage: area_um2 48071..72132 (HV reference 100000); accuracy_bits 12.7..17.1 (HV reference 12); data_width on the front 17..25 (registry 8..28).

Per family:
- pipelined: 44 evals, 23 feasible; max throughput seen 163 MSPS; best accuracy 20.38 bits; best feasible area_um2=48071; feasible ranges: data_width 16..25, n_iter 17..24, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 56 evals, 0 feasible; max throughput seen 115 MSPS; best accuracy 17.87 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5184 in, 6084 out
- provider-reported cost: $0.0082
- full prompts and replies: `llm_trace.jsonl`

