# DSE run: asic_multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
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
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined:data_width=21,n_iter=14,angle_guard=-2,frac_guard=0,rounding=trunc` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 43162 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 11499 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 936 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 128 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 128 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 125 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.48 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000152 (2^-12.69) | exact: bit-accurate model, dense (128030 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 79.5 | exact: bit-accurate model, dense (128030 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.06e-05 (2^-14.27) | exact: bit-accurate model, dense (128030 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 26.5 | exact: bit-accurate model, dense (128030 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.7 | exact: bit-accurate model, dense (128030 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (19 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=21,n_iter=14,angle_guard=-2,frac_guard=0,rounding=trunc` | 43162 | 936 | 127.5 | 16 | 2.48 | 0.000152 (2^-12.69) | 12.69 |
| 1 | `pipelined:data_width=19,n_iter=14,angle_guard=1,frac_guard=1,rounding=round` | 43452 | 920 | 132.4 | 16 | 2.46 | 0.000139 (2^-12.81) | 12.81 |
| 2 | `pipelined:data_width=20,n_iter=14,angle_guard=1,frac_guard=1,rounding=trunc` | 44350 | 960 | 127.5 | 16 | 2.54 | 0.000135 (2^-12.86) | 12.86 |
| 3 | `pipelined:data_width=19,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 47357 | 1022 | 132.4 | 18 | 2.71 | 5.84e-05 (2^-14.06) | 14.06 |
| 4 | `pipelined:data_width=20,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 49554 | 1070 | 127.5 | 18 | 2.84 | 4.64e-05 (2^-14.39) | 14.39 |
| 5 | `pipelined:data_width=20,n_iter=16,angle_guard=1,frac_guard=1,rounding=round` | 51998 | 1099 | 127.5 | 18 | 2.94 | 4.05e-05 (2^-14.59) | 14.59 |
| 6 | `pipelined:data_width=20,n_iter=17,angle_guard=1,frac_guard=0,rounding=round` | 52751 | 1137 | 127.5 | 19 | 3.02 | 3.32e-05 (2^-14.88) | 14.88 |
| 7 | `pipelined:data_width=20,n_iter=17,angle_guard=2,frac_guard=0,rounding=round` | 53531 | 1153 | 123.1 | 19 | 3.06 | 2.85e-05 (2^-15.10) | 15.10 |
| 8 | `pipelined:data_width=20,n_iter=17,angle_guard=1,frac_guard=1,rounding=round` | 55289 | 1168 | 127.5 | 19 | 3.12 | 2.58e-05 (2^-15.24) | 15.24 |
| 9 | `pipelined:data_width=20,n_iter=17,angle_guard=1,frac_guard=3,rounding=trunc` | 57168 | 1225 | 118.9 | 19 | 3.26 | 2.56e-05 (2^-15.25) | 15.25 |
| 10 | `pipelined:data_width=22,n_iter=19,angle_guard=-1,frac_guard=0,rounding=trunc` | 62642 | 1345 | 123.1 | 21 | 3.57 | 1.72e-05 (2^-15.83) | 15.83 |
| 11 | `pipelined:data_width=22,n_iter=17,angle_guard=2,frac_guard=4,rounding=trunc` | 64100 | 1371 | 107.9 | 19 | 3.65 | 1.7e-05 (2^-15.84) | 15.84 |
| 12 | `pipelined:data_width=22,n_iter=17,angle_guard=4,frac_guard=3,rounding=trunc` | 64187 | 1375 | 107.9 | 19 | 3.66 | 1.68e-05 (2^-15.86) | 15.86 |
| 13 | `pipelined:data_width=23,n_iter=19,angle_guard=-2,frac_guard=0,rounding=trunc` | 64391 | 1382 | 118.9 | 21 | 3.67 | 1.46e-05 (2^-16.06) | 16.06 |
| 14 | `pipelined:data_width=20,n_iter=19,angle_guard=4,frac_guard=1,rounding=round` | 64495 | 1362 | 115.0 | 21 | 3.64 | 1.26e-05 (2^-16.28) | 16.28 |
| 15 | `pipelined:data_width=24,n_iter=19,angle_guard=-1,frac_guard=0,rounding=trunc` | 67889 | 1457 | 115.0 | 21 | 3.87 | 6.73e-06 (2^-17.18) | 17.18 |
| 16 | `pipelined:data_width=24,n_iter=19,angle_guard=-1,frac_guard=1,rounding=trunc` | 69551 | 1490 | 111.3 | 21 | 3.96 | 6.25e-06 (2^-17.29) | 17.29 |
| 17 | `pipelined:data_width=25,n_iter=19,angle_guard=-1,frac_guard=0,rounding=round` | 70513 | 1513 | 111.3 | 21 | 4.02 | 5.17e-06 (2^-17.56) | 17.56 |
| 18 | `pipelined:data_width=22,n_iter=21,angle_guard=4,frac_guard=2,rounding=trunc` | 77963 | 1664 | 107.9 | 23 | 4.43 | 3.58e-06 (2^-18.09) | 18.09 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is min-area subject to max_abs_err <= 2^-12 and a burst constraint (32 simultaneous requests per 1 us tick, all back within 0.5 us). Only pipelined has ever produced feasible points and it holds the entire merged front, so the fleet budget should be concentrated there; unrolled_k/iterative-style sharing is not in my remit anyway and is already 0/100 across the fleet. The burst constraint is not the bottleneck for pipelined: the schedule is N+2 latency then 1 result/cycle, so a 32-request burst drains in about N+33 cycles, i.e. roughly 100 MHz suffices for N~20, well under any plausible Fmax for a single-micro-rotation stage. That makes accuracy-vs-area the only real trade-off, with area growing roughly as N x (W+frac_guard) plus N x 3(W+frac_guard) flops. I therefore sweep the accuracy-parameter space that defines the front (W, N, guards, rounding) rather than the timing space, centred on the smallest feasible (W,N) corner that the selection rule will pick, and still reaching far enough into the high-accuracy corner (W=20, N=20 -> ~16 accuracy_bits) to give the hypervolume calculation something to cover against the accuracy-12 reference. pipelined_m gets a deliberately small probe at m=2..4, since fewer registers is the only structural way to beat pipelined on the min-area objective; if that probe is feasible it should appear at the low-area end of the front, and if it is not, the evidence is strong enough to spend everything else on pipelined.*)
- `pipelined` (75 evals): data_width=13..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* pipelined is the only family that has produced feasible designs (23/44) and owns 9/9 of the current merged front, so it is where the trade-off curve actually lives. Its per-stage critical path is one fixed-shift micro-rotation (wired shifts, no barrel shifter), so Fmax is high and the burst requirement (32 requests from one 1 MHz tick inside 0.5 us = ~(N+2+31)/Fmax) is met with large margin; the binding constraint is accuracy vs. area, not timing. The selection rule is min area_um2, so the useful region is the smallest (W,N) that still satisfies max_abs_err <= 2^-12: output LSB is 2^-(W-2), so W>=14 is essentially forced, and the residual-angle term needs N>=~13. Ranges 13..20 / 10..20 bracket that boundary (some cheap low-N, low-W probes to find the true feasible edge) while still reaching the high-accuracy end (W=20 gives ~16 accuracy_bits, which is what pulls the HV reference point at accuracy 12). Guards and rounding are kept fully open because they are the second-order accuracy levers and cost almost nothing in area.
- `pipelined_m` (25 evals): data_width=13..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* pipelined_m computes identical bits to pipelined but registers only ceil(N/m) stages instead of N, so it is the one family that can undercut pipelined on the min-area objective while still delivering 1 result/cycle. Its 0/56 record is almost certainly a timing artefact: it spends m micro-rotations per registered stage, so Fmax falls roughly with m, and at larger m the analytic burst bound (N+2+31 cycles inside 0.5 us) becomes the binding constraint while accuracy is unchanged. That is testable cheaply by restricting m to 2..4, where the combinational path is at most 4 micro-rotations and Fmax should stay in the same band as pipelined, and by reusing exactly the accuracy window that pipelined proved feasible (13..20 / 10..20). If any pipelined_m point lands on the front it wins on area; if the small-m probe again yields nothing feasible, that fact is decisive and the remaining budget should go entirely to pipelined.

**Result (code):** 100 evaluations this round, 100 total; 47 feasible; hypervolume 2.212e+05 (n/a).

**LLM decision:** `map_front` — The feasible front is entirely `pipelined` and covers only data_width 19..20 of the registry's 8..28 — a very small slice of the accuracy/area dimensionality. Accuracy on the front runs 12.8..16.8 bits while the constraint floor is 12, so the whole low-accuracy/low-area corner (the region that actually pays off under `select: min area_um2` and that extends the front toward the HV reference at 12) is unexplored; the min-area point 43452 sits at the n_iter=14 edge of the explored range, so cheaper designs almost certainly exist at data_width~17-18 or n_iter~12-13. The other objectives are clearly non-binding (throughput 0% violate, best 156 >= 32; sys_p99_batch 24% violate, best 0.289 <= 0.5), so the trade-off to map is purely area vs accuracy. pipelined_m contributed 0 feasible in 25 evals and iterative/unrolled_k are not on the front (their Fmax/(N+3) throughput cannot reach 32 MSPS at the N>=13 needed for 12 bits), so mapping should focus the full parameter ranges seeded from the current pipelined front. This is the reserved full-range mapping pass that covers the objective curve rather than just the corner the selection rule picks.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 2.212e+05 (gain this round: n/a (first round)).
Feasible designs: 47 of 100 evaluations (34 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 156
- max_abs_err <= 0.000244141: 35% violate; best seen 8.54e-06 (2^-16.84)
- sys_p99_batch_us <= 0.5: 24% violate; best seen 0.289

Pareto front (feasible, 11 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=19 n_iter=14 angle_guard=1 frac_guard=1 rounding=round] area_um2=43452, accuracy_bits=12.8, ffs=920, throughput_msps=132, max_abs_err=0.000139 (2^-12.81), power_index=2.46
- pipelined [data_width=20 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=44350, accuracy_bits=12.9, ffs=960, throughput_msps=128, max_abs_err=0.000135 (2^-12.86), power_index=2.54
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=47357, accuracy_bits=14.1, ffs=1022, throughput_msps=132, max_abs_err=5.84e-05 (2^-14.06), power_index=2.71
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=49554, accuracy_bits=14.4, ffs=1070, throughput_msps=128, max_abs_err=4.64e-05 (2^-14.39), power_index=2.84
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] area_um2=51998, accuracy_bits=14.6, ffs=1099, throughput_msps=128, max_abs_err=4.05e-05 (2^-14.59), power_index=2.94
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=0 rounding=round] area_um2=53531, accuracy_bits=15.1, ffs=1153, throughput_msps=123, max_abs_err=2.85e-05 (2^-15.10), power_index=3.06
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=1 rounding=round] area_um2=55289, accuracy_bits=15.2, ffs=1168, throughput_msps=128, max_abs_err=2.58e-05 (2^-15.24), power_index=3.12
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=3 rounding=trunc] area_um2=57168, accuracy_bits=15.3, ffs=1225, throughput_msps=119, max_abs_err=2.56e-05 (2^-15.25), power_index=3.26
- pipelined [data_width=20 n_iter=19 angle_guard=4 frac_guard=1 rounding=round] area_um2=64495, accuracy_bits=16.3, ffs=1362, throughput_msps=115, max_abs_err=1.26e-05 (2^-16.28), power_index=3.64
- pipelined [data_width=20 n_iter=20 angle_guard=2 frac_guard=4 rounding=round] area_um2=71354, accuracy_bits=16.8, ffs=1500, throughput_msps=115, max_abs_err=8.54e-06 (2^-16.84), power_index=4.01
Front coverage: area_um2 43452..71354 (HV reference 100000); accuracy_bits 12.8..16.8 (HV reference 12); data_width on the front 19..20 (registry 8..28).

Per family:
- pipelined: 75 evals, 47 feasible; max throughput seen 156 MSPS; best accuracy 16.84 bits; best feasible area_um2=43452; feasible ranges: data_width 17..20, n_iter 14..20, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 25 evals, 0 feasible; max throughput seen 78.8 MSPS; best accuracy 16.46 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `pipelined` (10 evals): data_width=18..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (11 front designs; box front_anchored)
- `pipelined_m` (10 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 20 evaluations this round, 120 total; 54 feasible; hypervolume 2.212e+05 (+0.0%).

**LLM decision:** `map_front` — The feasible front is entirely pipelined and clustered in a narrow band (data_width 19..20, n_iter 14..20, area 43.5k..71.4k um^2), while the registry allows data_width 8..28 and n_iter 4..30 — so the low-area end of the trade-off curve is almost certainly unmapped. The selection rule is min area_um2, and the cheapest feasible design (43452 um^2) sits right at the edge of the explored box, meaning a smaller/cheaper feasible design likely exists just outside it. pipelined_m produced 0 feasible designs in 35 evals (max throughput 102 MSPS, so it is not throughput-limited; the failures are accuracy or sys_p99_batch), and no other family has been tried, so the front may also be missing cheaper families. With 80 evals left and hypervolume gain flat this round (+0.0%), a code-driven NSGA-II coverage search over the full ranges of the families on the front (seeded with the current front) is the right use of the budget to map the whole curve before selection.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 2.212e+05 (gain this round: +0.0%).
Feasible designs: 54 of 120 evaluations (41 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 3% violate; best seen 156
- max_abs_err <= 0.000244141: 36% violate; best seen 2.19e-07 (2^-22.13)
- sys_p99_batch_us <= 0.5: 27% violate; best seen 0.289

Pareto front (feasible, 11 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=19 n_iter=14 angle_guard=1 frac_guard=1 rounding=round] area_um2=43452, accuracy_bits=12.8, ffs=920, throughput_msps=132, max_abs_err=0.000139 (2^-12.81), power_index=2.46
- pipelined [data_width=20 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=44350, accuracy_bits=12.9, ffs=960, throughput_msps=128, max_abs_err=0.000135 (2^-12.86), power_index=2.54
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=47357, accuracy_bits=14.1, ffs=1022, throughput_msps=132, max_abs_err=5.84e-05 (2^-14.06), power_index=2.71
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=49554, accuracy_bits=14.4, ffs=1070, throughput_msps=128, max_abs_err=4.64e-05 (2^-14.39), power_index=2.84
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] area_um2=51998, accuracy_bits=14.6, ffs=1099, throughput_msps=128, max_abs_err=4.05e-05 (2^-14.59), power_index=2.94
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=0 rounding=round] area_um2=53531, accuracy_bits=15.1, ffs=1153, throughput_msps=123, max_abs_err=2.85e-05 (2^-15.10), power_index=3.06
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=1 rounding=round] area_um2=55289, accuracy_bits=15.2, ffs=1168, throughput_msps=128, max_abs_err=2.58e-05 (2^-15.24), power_index=3.12
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=3 rounding=trunc] area_um2=57168, accuracy_bits=15.3, ffs=1225, throughput_msps=119, max_abs_err=2.56e-05 (2^-15.25), power_index=3.26
- pipelined [data_width=20 n_iter=19 angle_guard=4 frac_guard=1 rounding=round] area_um2=64495, accuracy_bits=16.3, ffs=1362, throughput_msps=115, max_abs_err=1.26e-05 (2^-16.28), power_index=3.64
- pipelined [data_width=20 n_iter=20 angle_guard=2 frac_guard=4 rounding=round] area_um2=71354, accuracy_bits=16.8, ffs=1500, throughput_msps=115, max_abs_err=8.54e-06 (2^-16.84), power_index=4.01
Front coverage: area_um2 43452..71354 (HV reference 100000); accuracy_bits 12.8..16.8 (HV reference 12); data_width on the front 19..20 (registry 8..28).

Per family:
- pipelined: 85 evals, 54 feasible; max throughput seen 156 MSPS; best accuracy 20.46 bits; best feasible area_um2=43452; feasible ranges: data_width 17..22, n_iter 14..22, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 35 evals, 0 feasible; max throughput seen 102 MSPS; best accuracy 22.13 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined` (40 evals): data_width=18..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (11 front designs; box front_anchored)
- `pipelined_m` (40 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 80 evaluations this round, 200 total; 84 feasible; hypervolume 2.585e+05 (+16.8%).

**LLM decision:** `stop` — Budget is exhausted (200/200 evals, final round) and the registry is demonstrably feasible: 84 feasible evaluations (67 unique) with all three constraints met simultaneously — throughput best 156 MSPS vs >=32, max_abs_err best 7.32e-08 vs <=2.44e-4, sys_p99_batch_us best 0.289 vs <=0.5 — so `infeasible` is ruled out. The feasible Pareto front (19 designs) spans area_um2 43162..77963 against the HV reference 100000 and accuracy_bits 12.7..18.1 against reference 12, i.e. it already covers the useful part of both objective ranges, and hypervolume is still improving (+16.8% this round) but no further evaluations remain. The selection rule (min area_um2) picks pipelined [data_width=21, n_iter=14, angle_guard=-2, frac_guard=0, rounding=trunc] at 43162 um2, 12.7 accuracy bits (max_abs_err 1.52e-4, inside the 2^-12 budget) and 128 MSPS. The only residual risk is that the L1 sys_p99_batch bound is optimistic, so the cheapest front points may be re-screened at L2; that is a post-selection simulation step, not something a further exploration round can resolve.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 2.585e+05 (gain this round: +16.8%).
Feasible designs: 84 of 200 evaluations (67 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 10% violate; best seen 156
- max_abs_err <= 0.000244141: 32% violate; best seen 7.32e-08 (2^-23.70)
- sys_p99_batch_us <= 0.5: 39% violate; best seen 0.289

Pareto front (feasible, 19 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=21 n_iter=14 angle_guard=-2 frac_guard=0 rounding=trunc] area_um2=43162, accuracy_bits=12.7, ffs=936, throughput_msps=128, max_abs_err=0.000152 (2^-12.69), power_index=2.48
- pipelined [data_width=20 n_iter=14 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=44350, accuracy_bits=12.9, ffs=960, throughput_msps=128, max_abs_err=0.000135 (2^-12.86), power_index=2.54
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=49554, accuracy_bits=14.4, ffs=1070, throughput_msps=128, max_abs_err=4.64e-05 (2^-14.39), power_index=2.84
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] area_um2=52751, accuracy_bits=14.9, ffs=1137, throughput_msps=128, max_abs_err=3.32e-05 (2^-14.88), power_index=3.02
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=1 rounding=round] area_um2=55289, accuracy_bits=15.2, ffs=1168, throughput_msps=128, max_abs_err=2.58e-05 (2^-15.24), power_index=3.12
- pipelined [data_width=22 n_iter=19 angle_guard=-1 frac_guard=0 rounding=trunc] area_um2=62642, accuracy_bits=15.8, ffs=1345, throughput_msps=123, max_abs_err=1.72e-05 (2^-15.83), power_index=3.57
- pipelined [data_width=22 n_iter=17 angle_guard=4 frac_guard=3 rounding=trunc] area_um2=64187, accuracy_bits=15.9, ffs=1375, throughput_msps=108, max_abs_err=1.68e-05 (2^-15.86), power_index=3.66
- pipelined [data_width=20 n_iter=19 angle_guard=4 frac_guard=1 rounding=round] area_um2=64495, accuracy_bits=16.3, ffs=1362, throughput_msps=115, max_abs_err=1.26e-05 (2^-16.28), power_index=3.64
- pipelined [data_width=24 n_iter=19 angle_guard=-1 frac_guard=1 rounding=trunc] area_um2=69551, accuracy_bits=17.3, ffs=1490, throughput_msps=111, max_abs_err=6.25e-06 (2^-17.29), power_index=3.96
- pipelined [data_width=22 n_iter=21 angle_guard=4 frac_guard=2 rounding=trunc] area_um2=77963, accuracy_bits=18.1, ffs=1664, throughput_msps=108, max_abs_err=3.58e-06 (2^-18.09), power_index=4.43
Front coverage: area_um2 43162..77963 (HV reference 100000); accuracy_bits 12.7..18.1 (HV reference 12); data_width on the front 19..25 (registry 8..28).

Per family:
- pipelined: 125 evals, 84 feasible; max throughput seen 156 MSPS; best accuracy 23.70 bits; best feasible area_um2=43162; feasible ranges: data_width 17..25, n_iter 14..27, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 75 evals, 0 feasible; max throughput seen 102 MSPS; best accuracy 22.13 bits
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 13943 in, 12110 out
- provider-reported cost: $0.0093
- full prompts and replies: `llm_trace.jsonl`

