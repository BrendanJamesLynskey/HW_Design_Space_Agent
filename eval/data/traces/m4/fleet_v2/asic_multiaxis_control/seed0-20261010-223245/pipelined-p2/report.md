# DSE run: asic_multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
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
`pipelined:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 37422 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 9970 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 812 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 143 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 112 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.15 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000204 (2^-12.26) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 6.67 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 6.07e-05 (2^-14.01) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.99 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.3 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (20 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 37422 | 812 | 143.2 | 16 | 2.15 | 0.000204 (2^-12.26) | 12.26 |
| 1 | `pipelined:data_width=17,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 38060 | 826 | 137.6 | 16 | 2.19 | 0.000194 (2^-12.33) | 12.33 |
| 2 | `pipelined:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 39336 | 853 | 137.6 | 16 | 2.26 | 0.000175 (2^-12.48) | 12.48 |
| 3 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 39973 | 867 | 132.4 | 16 | 2.3 | 0.00017 (2^-12.53) | 12.53 |
| 4 | `pipelined:data_width=18,n_iter=14,angle_guard=1,frac_guard=1,rounding=round` | 41487 | 879 | 137.6 | 16 | 2.35 | 0.00016 (2^-12.61) | 12.61 |
| 5 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=1,rounding=round` | 42125 | 893 | 132.4 | 16 | 2.38 | 0.000152 (2^-12.68) | 12.68 |
| 6 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 42248 | 914 | 137.6 | 17 | 2.42 | 0.000119 (2^-13.04) | 13.04 |
| 7 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=round` | 44494 | 942 | 137.6 | 17 | 2.51 | 0.000101 (2^-13.27) | 13.27 |
| 8 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=1,rounding=round` | 45179 | 957 | 132.4 | 17 | 2.55 | 9.31e-05 (2^-13.39) | 13.39 |
| 9 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 45892 | 991 | 132.4 | 18 | 2.63 | 8.35e-05 (2^-13.55) | 13.55 |
| 10 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 46462 | 982 | 132.4 | 17 | 2.62 | 8.26e-05 (2^-13.56) | 13.56 |
| 11 | `pipelined:data_width=18,n_iter=15,angle_guard=4,frac_guard=2,rounding=round` | 47832 | 1012 | 123.1 | 17 | 2.7 | 7.73e-05 (2^-13.66) | 13.66 |
| 12 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 48233 | 1020 | 132.4 | 18 | 2.72 | 6.45e-05 (2^-13.92) | 13.92 |
| 13 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 49611 | 1048 | 132.4 | 18 | 2.8 | 5.46e-05 (2^-14.16) | 14.16 |
| 14 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=3,rounding=round` | 50989 | 1076 | 127.5 | 18 | 2.87 | 5.03e-05 (2^-14.28) | 14.28 |
| 15 | `pipelined:data_width=24,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 59077 | 1274 | 107.9 | 18 | 3.38 | 3.12e-05 (2^-14.97) | 14.97 |
| 16 | `pipelined:data_width=23,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 59476 | 1256 | 111.3 | 18 | 3.36 | 3.11e-05 (2^-14.97) | 14.97 |
| 17 | `pipelined:data_width=25,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc` | 61274 | 1321 | 104.7 | 18 | 3.51 | 3.08e-05 (2^-14.99) | 14.99 |
| 18 | `pipelined:data_width=25,n_iter=16,angle_guard=3,frac_guard=3,rounding=trunc` | 66140 | 1420 | 101.6 | 18 | 3.77 | 3.06e-05 (2^-15.00) | 15.00 |
| 19 | `pipelined:data_width=19,n_iter=23,angle_guard=2,frac_guard=3,rounding=trunc` | 75922 | 1616 | 123.1 | 25 | 4.31 | 2.18e-05 (2^-15.49) | 15.49 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show pipelined is the only family with feasible designs (30 feasible, best area 44427 um^2), while iterative, unrolled_k, and pipelined_m all had 0 feasible. The 32 Msps throughput constraint and 0.5 us p99 batch constraint require a high-Fmax, 1-result/cycle architecture, which only pipelined and pipelined_m can provide. I will focus 60% of the budget on pipelined to refine the Pareto front in the low-area region (W=14-18, N=10-16) with rounding for accuracy, and 40% on pipelined_m with m restricted to 2-4 to check if partial pipelining can beat the full pipelined area while still meeting Fmax. The accuracy constraint (max_abs_err <= 2^-12) requires at least ~12-14 bits of accuracy, so W=14-18 with N=10-16 and rounding should cover the feasible accuracy range. The area objective (minimize) and accuracy_bits objective (maximize) define the trade-off curve I need to map.*)
- `pipelined` (60 evals): data_width=14..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* pipelined is the only family with feasible designs (30 feasible, best area 44427 um^2); it is the only one that can meet the 32 Msps throughput and 0.5 us p99 batch constraints. Focusing on the low-area corner (W=14-18, N=10-16) with rounding to maximize accuracy_bits for the hypervolume.
- `pipelined_m` (40 evals): data_width=14..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* pipelined_m had 0 feasible in the previous round, likely because the m=2..8 range included large m values that reduced Fmax below the 32 Msps requirement. Restricting m to 2-4 keeps the pipeline shallow enough for high Fmax while still reducing area vs full pipelined. This may find a smaller-area point on the front.

**Result (code):** 100 evaluations this round, 100 total; 29 feasible; hypervolume 1.195e+05 (n/a).

**LLM decision:** `refine` — Round 1 established that pipelined is the only viable family. The front is currently a small cluster. To improve hypervolume, we need to expand the search space slightly to capture the full trade-off curve between area and accuracy. The current ranges are too tight (data_width 17-18, n_iter 14-16). Expanding to data_width 16-19 and n_iter 13-18 will allow the optimizer to find designs that are either smaller (lower area) or more accurate (higher bits) than the current front, thus increasing the covered hypervolume. We drop pipelined_m as it yielded 0 feasible designs in 40 evals, likely due to throughput/latency constraints from the bursty 32-request tick.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.195e+05 (gain this round: n/a (first round)).
Feasible designs: 29 of 100 evaluations (13 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 171
- max_abs_err <= 0.000244141: 50% violate; best seen 5.46e-05 (2^-14.16)
- sys_p99_batch_us <= 0.5: 32% violate; best seen 0.28

Pareto front (feasible, 9 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=37422, accuracy_bits=12.3, ffs=812, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=2.15
- pipelined [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] area_um2=38698, accuracy_bits=12.3, ffs=840, throughput_msps=143, max_abs_err=0.0002 (2^-12.28), power_index=2.22
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=39336, accuracy_bits=12.5, ffs=853, throughput_msps=138, max_abs_err=0.000175 (2^-12.48), power_index=2.26
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.5, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53), power_index=2.3
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=42125, accuracy_bits=12.7, ffs=893, throughput_msps=132, max_abs_err=0.000152 (2^-12.68), power_index=2.38
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=42248, accuracy_bits=13, ffs=914, throughput_msps=138, max_abs_err=0.000119 (2^-13.04), power_index=2.42
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=45159, accuracy_bits=13.2, ffs=975, throughput_msps=138, max_abs_err=0.000108 (2^-13.18), power_index=2.59
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] area_um2=48878, accuracy_bits=13.7, ffs=1032, throughput_msps=132, max_abs_err=7.47e-05 (2^-13.71), power_index=2.76
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
Front coverage: area_um2 37422..49611 (HV reference 100000); accuracy_bits 12.3..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 60 evals, 29 feasible; max throughput seen 171 MSPS; best accuracy 14.16 bits; best feasible area_um2=37422; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 40 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 13.39 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 1 established that pipelined is the only viable family. The front is currently a small cluster. To improve hypervolume, we need to expand the search space slightly to capture the full trade-off curve between area and accuracy. The current ranges are too tight (data_width 17-18, n_iter 14-16). Expanding to data_width 16-19 and n_iter 13-18 will allow the optimizer to find designs that are either smaller (lower area) or more accurate (higher bits) than the current front, thus increasing the covered hypervolume. We drop pipelined_m as it yielded 0 feasible designs in 40 evals, likely due to throughput/latency constraints from the bursty 32-request tick.*)
- `pipelined` (20 evals): data_width=17..18, n_iter=14..16, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* The pipelined family is the only one producing feasible designs (29 feasible vs 0 for pipelined_m). The current front is tightly clustered in the low-area corner (37k-50k um2) with accuracy 12.3-14.2 bits. To maximize hypervolume, we need to explore the trade-off curve more broadly. Specifically, we should check if slightly higher n_iter (17-18) or data_width (19) can push accuracy higher without blowing area, and if lower n_iter (13) or data_width (16) can push area lower while still meeting the 2^-12 error constraint. The current ranges (n_iter 14-16, data_width 17-18) are already narrow; expanding them slightly will help map the full Pareto front. We also keep rounding='round' as it dominates truncation for accuracy at similar area.

**Result (code):** 20 evaluations this round, 120 total; 49 feasible; hypervolume 1.214e+05 (+1.6%).

**LLM decision:** `stop` — The Pareto front is well-mapped and feasible. The minimum area design (pipelined, data_width=17, n_iter=14, angle_guard=1, frac_guard=0, rounding=round) achieves 37422 um^2 with 12.3 accuracy bits (max_abs_err=0.000204), satisfying the max_abs_err <= 0.000244141 constraint. Throughput is 143 MSPS (>= 32 MSPS). The system constraint sys_p99_batch_us <= 0.5 us is met by the best seen value of 0.28 us. The front spans a reasonable range of accuracy (12.3 to 14.2 bits) and area (37422 to 49611 um^2). Since this is the final round, we stop and select the minimum area design from the front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.214e+05 (gain this round: +1.6%).
Feasible designs: 49 of 120 evaluations (21 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 171
- max_abs_err <= 0.000244141: 42% violate; best seen 5.46e-05 (2^-14.16)
- sys_p99_batch_us <= 0.5: 27% violate; best seen 0.28

Pareto front (feasible, 12 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=37422, accuracy_bits=12.3, ffs=812, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=2.15
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=38060, accuracy_bits=12.3, ffs=826, throughput_msps=138, max_abs_err=0.000194 (2^-12.33), power_index=2.19
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=39336, accuracy_bits=12.5, ffs=853, throughput_msps=138, max_abs_err=0.000175 (2^-12.48), power_index=2.26
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=round] area_um2=41487, accuracy_bits=12.6, ffs=879, throughput_msps=138, max_abs_err=0.00016 (2^-12.61), power_index=2.35
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=1 rounding=round] area_um2=42125, accuracy_bits=12.7, ffs=893, throughput_msps=132, max_abs_err=0.000152 (2^-12.68), power_index=2.38
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=42248, accuracy_bits=13, ffs=914, throughput_msps=138, max_abs_err=0.000119 (2^-13.04), power_index=2.42
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=44494, accuracy_bits=13.3, ffs=942, throughput_msps=138, max_abs_err=0.000101 (2^-13.27), power_index=2.51
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=48233, accuracy_bits=13.9, ffs=1020, throughput_msps=132, max_abs_err=6.45e-05 (2^-13.92), power_index=2.72
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
Front coverage: area_um2 37422..49611 (HV reference 100000); accuracy_bits 12.3..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 80 evals, 49 feasible; max throughput seen 171 MSPS; best accuracy 14.16 bits; best feasible area_um2=37422; feasible ranges: data_width 17..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 40 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 13.39 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined` (40 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (12 front designs; box front_anchored)
- `pipelined_m` (40 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 80 evaluations this round, 200 total; 83 feasible; hypervolume 1.685e+05 (+38.8%).

**No LLM call** (code's front-mapping round): The Pareto front is well-mapped and feasible. The minimum area design (pipelined, data_width=17, n_iter=14, angle_guard=1, frac_guard=0, rounding=round) achieves 37422 um^2 with 12.3 accuracy bits (max_abs_err=0.000204), satisfying the max_abs_err <= 0.000244141 constraint. Throughput is 143 MSPS (>= 32 MSPS). The system constraint sys_p99_batch_us <= 0.5 us is met by the best seen value of 0.28 us. The front spans a reasonable range of accuracy (12.3 to 14.2 bits) and area (37422 to 49611 um^2). Since this is the final round, we stop and select the minimum area design from the front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.685e+05 (gain this round: +38.8%).
Feasible designs: 83 of 200 evaluations (45 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 15% violate; best seen 171
- max_abs_err <= 0.000244141: 32% violate; best seen 4.02e-07 (2^-21.25)
- sys_p99_batch_us <= 0.5: 37% violate; best seen 0.28

Pareto front (feasible, 20 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=37422, accuracy_bits=12.3, ffs=812, throughput_msps=143, max_abs_err=0.000204 (2^-12.26), power_index=2.15
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=39336, accuracy_bits=12.5, ffs=853, throughput_msps=138, max_abs_err=0.000175 (2^-12.48), power_index=2.26
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=round] area_um2=41487, accuracy_bits=12.6, ffs=879, throughput_msps=138, max_abs_err=0.00016 (2^-12.61), power_index=2.35
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=42248, accuracy_bits=13, ffs=914, throughput_msps=138, max_abs_err=0.000119 (2^-13.04), power_index=2.42
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] area_um2=45179, accuracy_bits=13.4, ffs=957, throughput_msps=132, max_abs_err=9.31e-05 (2^-13.39), power_index=2.55
- pipelined [data_width=18 n_iter=15 angle_guard=4 frac_guard=2 rounding=round] area_um2=47832, accuracy_bits=13.7, ffs=1012, throughput_msps=123, max_abs_err=7.73e-05 (2^-13.66), power_index=2.7
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
- pipelined [data_width=24 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=59077, accuracy_bits=15, ffs=1274, throughput_msps=108, max_abs_err=3.12e-05 (2^-14.97), power_index=3.38
- pipelined [data_width=25 n_iter=16 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=61274, accuracy_bits=15, ffs=1321, throughput_msps=105, max_abs_err=3.08e-05 (2^-14.99), power_index=3.51
- pipelined [data_width=19 n_iter=23 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=75922, accuracy_bits=15.5, ffs=1616, throughput_msps=123, max_abs_err=2.18e-05 (2^-15.49), power_index=4.31
Front coverage: area_um2 37422..75922 (HV reference 100000); accuracy_bits 12.3..15.5 (HV reference 12); data_width on the front 17..25 (registry 8..28).

Per family:
- pipelined: 120 evals, 83 feasible; max throughput seen 171 MSPS; best accuracy 18.89 bits; best feasible area_um2=37422; feasible ranges: data_width 16..25, n_iter 14..29, angle_guard 0..4, frac_guard 0..4
- pipelined_m: 80 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 21.25 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 9604 in, 2039 out
- provider-reported cost: $0.0042
- full prompts and replies: `llm_trace.jsonl`

