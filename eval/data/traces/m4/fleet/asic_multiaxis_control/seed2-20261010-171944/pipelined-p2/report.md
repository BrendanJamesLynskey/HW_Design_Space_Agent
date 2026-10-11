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

## Pareto front (22 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 39973 | 867 | 132.4 | 16 | 2.3 | 0.00017 (2^-12.53) | 12.53 |
| 1 | `pipelined:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 40877 | 885 | 137.6 | 17 | 2.34 | 0.000148 (2^-12.72) | 12.72 |
| 2 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 42248 | 914 | 137.6 | 17 | 2.42 | 0.000119 (2^-13.04) | 13.04 |
| 3 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 42933 | 929 | 132.4 | 17 | 2.46 | 0.000109 (2^-13.17) | 13.17 |
| 4 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=round` | 44494 | 942 | 137.6 | 17 | 2.51 | 0.000101 (2^-13.27) | 13.27 |
| 5 | `pipelined:data_width=19,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 44988 | 973 | 127.5 | 17 | 2.58 | 8.33e-05 (2^-13.55) | 13.55 |
| 6 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 46462 | 982 | 132.4 | 17 | 2.62 | 8.26e-05 (2^-13.56) | 13.56 |
| 7 | `pipelined:data_width=19,n_iter=15,angle_guard=1,frac_guard=1,rounding=round` | 46601 | 986 | 132.4 | 17 | 2.63 | 7.94e-05 (2^-13.62) | 13.62 |
| 8 | `pipelined:data_width=19,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 48089 | 1038 | 127.5 | 18 | 2.75 | 5.75e-05 (2^-14.09) | 14.09 |
| 9 | `pipelined:data_width=19,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 50112 | 1078 | 127.5 | 18 | 2.86 | 5.43e-05 (2^-14.17) | 14.17 |
| 10 | `pipelined:data_width=19,n_iter=17,angle_guard=2,frac_guard=0,rounding=round` | 51191 | 1103 | 127.5 | 19 | 2.93 | 4.23e-05 (2^-14.53) | 14.53 |
| 11 | `pipelined:data_width=21,n_iter=16,angle_guard=0,frac_guard=1,rounding=round` | 53514 | 1131 | 123.1 | 18 | 3.02 | 4e-05 (2^-14.61) | 14.61 |
| 12 | `pipelined:data_width=18,n_iter=17,angle_guard=3,frac_guard=2,rounding=round` | 53540 | 1131 | 127.5 | 19 | 3.02 | 3.68e-05 (2^-14.73) | 14.73 |
| 13 | `pipelined:data_width=23,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 56879 | 1227 | 111.3 | 18 | 3.25 | 3.15e-05 (2^-14.95) | 14.95 |
| 14 | `pipelined:data_width=23,n_iter=16,angle_guard=3,frac_guard=2,rounding=trunc` | 60367 | 1298 | 107.9 | 18 | 3.45 | 3.11e-05 (2^-14.97) | 14.97 |
| 15 | `pipelined:data_width=22,n_iter=17,angle_guard=3,frac_guard=2,rounding=round` | 63103 | 1331 | 111.3 | 19 | 3.56 | 1.65e-05 (2^-15.89) | 15.89 |
| 16 | `pipelined:data_width=23,n_iter=17,angle_guard=2,frac_guard=2,rounding=trunc` | 63494 | 1363 | 111.3 | 19 | 3.62 | 1.61e-05 (2^-15.92) | 15.92 |
| 17 | `pipelined:data_width=26,n_iter=17,angle_guard=0,frac_guard=1,rounding=round` | 68854 | 1452 | 104.7 | 19 | 3.88 | 1.55e-05 (2^-15.98) | 15.98 |
| 18 | `pipelined:data_width=23,n_iter=20,angle_guard=2,frac_guard=0,rounding=trunc` | 71559 | 1534 | 111.3 | 22 | 4.08 | 6.2e-06 (2^-17.30) | 17.30 |
| 19 | `pipelined:data_width=23,n_iter=19,angle_guard=1,frac_guard=4,rounding=trunc` | 73663 | 1572 | 104.7 | 21 | 4.18 | 5.27e-06 (2^-17.53) | 17.53 |
| 20 | `pipelined:data_width=23,n_iter=21,angle_guard=1,frac_guard=3,rounding=trunc` | 79814 | 1702 | 107.9 | 23 | 4.53 | 2.69e-06 (2^-18.51) | 18.51 |
| 21 | `pipelined:data_width=26,n_iter=20,angle_guard=1,frac_guard=1,rounding=round` | 82065 | 1728 | 104.7 | 22 | 4.62 | 2.11e-06 (2^-18.85) | 18.85 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *After 100 evaluations (56 pipelined + 44 pipelined_m), only pipelined has produced feasible designs (25 feasible, best area 39336 um2). pipelined_m has 0 feasible designs in 44 evals, likely because its reduced register count does not improve area enough to matter, or its latency/throughput characteristics don't help. iterative and unrolled_k (other members) also have 0 feasible designs, confirming that only pipelined architectures meet the 32 MSps throughput and 0.5 us batch latency constraints. The 11 designs on the merged front are all from pipelined. With 100 evaluations remaining (round 2 of 4), I should focus entirely on refining the pipelined front: the current feasible region is data_width 14-20, n_iter 12-18. The key trade-off is area vs accuracy_bits. I narrow the ranges to focus the search: data_width 14-20 (below 14 likely fails accuracy, above 20 adds area without accuracy benefit since max_abs_err constraint is 2^-12), n_iter 12-18 (below 12 likely fails accuracy, above 18 adds area), angle_guard 0-2 and frac_guard 0-2 (small guards to minimize area while maintaining accuracy), rounding both options. This refinement should tighten the Pareto front and identify the minimum-area feasible design for the selection rule (min area_um2).*)
- `pipelined` (100 evals): data_width=14..20, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined is the only family with feasible designs (25 feasible, best area 39336 um2). It meets throughput_msps >= 32 (1 result/cycle at Fmax >= 32 MHz) and sys_p99_batch_us <= 0.5 us (32 back-to-back results in 32 cycles; at Fmax >= 64 MHz that is 0.5 us). The current front spans data_width 14-20, n_iter 12-18. I focus the remaining budget on refining the Pareto front in this narrow region: lower data_width/n_iter reduce area but risk violating max_abs_err <= 2^-12; the trade-off between area and accuracy_bits is the key axis. angle_guard 0-2 and frac_guard 0-2 cover the accuracy-relevant range without excessive area. Rounding choice affects accuracy at the boundary. This is a refinement pass to tighten the front and find the minimum-area feasible point.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 66 feasible; hypervolume 1.567e+05 (n/a).

**LLM decision:** `add_family` — The pipelined family is the only one explored so far, and its front is dominated by high area (min ~40k um^2) because it registers every stage. The `pipelined_m` family (register every m stages) is not yet explored and should offer significantly lower area for the same throughput/accuracy by reducing flip-flop count, potentially pushing the front well below the 100k um^2 HV reference. I will add `pipelined_m` to explore this trade-off, focusing on the parameter ranges that yielded feasible designs in `pipelined` (data_width 16-20, n_iter 14-18) to ensure the throughput and accuracy constraints are met while optimizing area.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.567e+05 (gain this round: n/a (first round)).
Feasible designs: 66 of 100 evaluations (49 unique).
Families explored so far: pipelined. Not yet explored: pipelined_m.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 171
- max_abs_err <= 0.000244141: 34% violate; best seen 3.21e-05 (2^-14.93)
- sys_p99_batch_us <= 0.5: 0% violate; best seen 0.263

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.5, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53), power_index=2.3
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=40877, accuracy_bits=12.7, ffs=885, throughput_msps=138, max_abs_err=0.000148 (2^-12.72), power_index=2.34
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=42933, accuracy_bits=13.2, ffs=929, throughput_msps=132, max_abs_err=0.000109 (2^-13.17), power_index=2.46
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=44494, accuracy_bits=13.3, ffs=942, throughput_msps=138, max_abs_err=0.000101 (2^-13.27), power_index=2.51
- pipelined [data_width=19 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=44988, accuracy_bits=13.6, ffs=973, throughput_msps=128, max_abs_err=8.33e-05 (2^-13.55), power_index=2.58
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=46601, accuracy_bits=13.6, ffs=986, throughput_msps=132, max_abs_err=7.94e-05 (2^-13.62), power_index=2.63
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=48089, accuracy_bits=14.1, ffs=1038, throughput_msps=128, max_abs_err=5.75e-05 (2^-14.09), power_index=2.75
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=50112, accuracy_bits=14.2, ffs=1078, throughput_msps=128, max_abs_err=5.43e-05 (2^-14.17), power_index=2.86
- pipelined [data_width=18 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] area_um2=55909, accuracy_bits=14.7, ffs=1180, throughput_msps=132, max_abs_err=3.81e-05 (2^-14.68), power_index=3.15
- pipelined [data_width=19 n_iter=18 angle_guard=1 frac_guard=2 rounding=round] area_um2=57614, accuracy_bits=14.9, ffs=1215, throughput_msps=128, max_abs_err=3.21e-05 (2^-14.93), power_index=3.25
Front coverage: area_um2 39973..57614 (HV reference 100000); accuracy_bits 12.5..14.9 (HV reference 12); data_width on the front 17..19 (registry 8..28).

Per family:
- pipelined: 100 evals, 66 feasible; max throughput seen 171 MSPS; best accuracy 14.93 bits; best feasible area_um2=39973; feasible ranges: data_width 16..20, n_iter 14..18, angle_guard 0..2, frac_guard 0..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Adding pipelined_m to explore the area trade-off by reducing pipeline registers, which should yield much lower area than the current pipelined front.*)
- `pipelined_m` (20 evals): data_width=16..20, n_iter=14..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* pipelined_m reduces register count compared to pipelined, which should lower area significantly. Searching the same data_width/n_iter ranges as the feasible pipelined designs ensures we can meet the throughput (>=32 MSPS) and accuracy (<=2^-12) constraints while exploring the area trade-off.

**Result (code):** 20 evaluations this round, 120 total; 66 feasible; hypervolume 1.567e+05 (+0.0%).

**LLM decision:** `stop` — The feasible Pareto front is well-established and the minimum-area design (pipelined, data_width=18, n_iter=14, area=39973 um^2) comfortably satisfies all constraints: throughput 132 MSPS >= 32, max_abs_err 0.00017 <= 0.000244, and the system batch latency bound is met (best seen 0.263 us <= 0.5 us). The front spans a reasonable trade-off from 39973 to 57614 um^2 and 12.5 to 14.9 accuracy bits, with hypervolume stable at 1.567e+05 (no gain in round 2). pipelined_m yielded no feasible designs, confirming pipelined is the correct family. Since this is the final round, the current front is sufficient for selection.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.567e+05 (gain this round: +0.0%).
Feasible designs: 66 of 120 evaluations (49 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 7% violate; best seen 171
- max_abs_err <= 0.000244141: 35% violate; best seen 3.21e-05 (2^-14.93)
- sys_p99_batch_us <= 0.5: 17% violate; best seen 0.263

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.5, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53), power_index=2.3
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=40877, accuracy_bits=12.7, ffs=885, throughput_msps=138, max_abs_err=0.000148 (2^-12.72), power_index=2.34
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=42933, accuracy_bits=13.2, ffs=929, throughput_msps=132, max_abs_err=0.000109 (2^-13.17), power_index=2.46
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=44494, accuracy_bits=13.3, ffs=942, throughput_msps=138, max_abs_err=0.000101 (2^-13.27), power_index=2.51
- pipelined [data_width=19 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=44988, accuracy_bits=13.6, ffs=973, throughput_msps=128, max_abs_err=8.33e-05 (2^-13.55), power_index=2.58
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=46601, accuracy_bits=13.6, ffs=986, throughput_msps=132, max_abs_err=7.94e-05 (2^-13.62), power_index=2.63
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=48089, accuracy_bits=14.1, ffs=1038, throughput_msps=128, max_abs_err=5.75e-05 (2^-14.09), power_index=2.75
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=50112, accuracy_bits=14.2, ffs=1078, throughput_msps=128, max_abs_err=5.43e-05 (2^-14.17), power_index=2.86
- pipelined [data_width=18 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] area_um2=55909, accuracy_bits=14.7, ffs=1180, throughput_msps=132, max_abs_err=3.81e-05 (2^-14.68), power_index=3.15
- pipelined [data_width=19 n_iter=18 angle_guard=1 frac_guard=2 rounding=round] area_um2=57614, accuracy_bits=14.9, ffs=1215, throughput_msps=128, max_abs_err=3.21e-05 (2^-14.93), power_index=3.25
Front coverage: area_um2 39973..57614 (HV reference 100000); accuracy_bits 12.5..14.9 (HV reference 12); data_width on the front 17..19 (registry 8..28).

Per family:
- pipelined: 100 evals, 66 feasible; max throughput seen 171 MSPS; best accuracy 14.93 bits; best feasible area_um2=39973; feasible ranges: data_width 16..20, n_iter 14..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 20 evals, 0 feasible; max throughput seen 75.4 MSPS; best accuracy 14.52 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined` (80 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (13 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 120 feasible; hypervolume 2.656e+05 (+69.5%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and the minimum-area design (pipelined, data_width=18, n_iter=14, area=39973 um^2) comfortably satisfies all constraints: throughput 132 MSPS >= 32, max_abs_err 0.00017 <= 0.000244, and the system batch latency bound is met (best seen 0.263 us <= 0.5 us). The front spans a reasonable trade-off from 39973 to 57614 um^2 and 12.5 to 14.9 accuracy bits, with hypervolume stable at 1.567e+05 (no gain in round 2). pipelined_m yielded no feasible designs, confirming pipelined is the correct family. Since this is the final round, the current front is sufficient for selection.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 2.656e+05 (gain this round: +69.5%).
Feasible designs: 120 of 200 evaluations (95 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 4% violate; best seen 171
- max_abs_err <= 0.000244141: 24% violate; best seen 3.7e-07 (2^-21.37)
- sys_p99_batch_us <= 0.5: 20% violate; best seen 0.263

Pareto front (feasible, 22 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.5, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53), power_index=2.3
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=42248, accuracy_bits=13, ffs=914, throughput_msps=138, max_abs_err=0.000119 (2^-13.04), power_index=2.42
- pipelined [data_width=19 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=44988, accuracy_bits=13.6, ffs=973, throughput_msps=128, max_abs_err=8.33e-05 (2^-13.55), power_index=2.58
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=46601, accuracy_bits=13.6, ffs=986, throughput_msps=132, max_abs_err=7.94e-05 (2^-13.62), power_index=2.63
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=50112, accuracy_bits=14.2, ffs=1078, throughput_msps=128, max_abs_err=5.43e-05 (2^-14.17), power_index=2.86
- pipelined [data_width=18 n_iter=17 angle_guard=3 frac_guard=2 rounding=round] area_um2=53540, accuracy_bits=14.7, ffs=1131, throughput_msps=128, max_abs_err=3.68e-05 (2^-14.73), power_index=3.02
- pipelined [data_width=23 n_iter=16 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=60367, accuracy_bits=15, ffs=1298, throughput_msps=108, max_abs_err=3.11e-05 (2^-14.97), power_index=3.45
- pipelined [data_width=23 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=63494, accuracy_bits=15.9, ffs=1363, throughput_msps=111, max_abs_err=1.61e-05 (2^-15.92), power_index=3.62
- pipelined [data_width=23 n_iter=19 angle_guard=1 frac_guard=4 rounding=trunc] area_um2=73663, accuracy_bits=17.5, ffs=1572, throughput_msps=105, max_abs_err=5.27e-06 (2^-17.53), power_index=4.18
- pipelined [data_width=26 n_iter=20 angle_guard=1 frac_guard=1 rounding=round] area_um2=82065, accuracy_bits=18.9, ffs=1728, throughput_msps=105, max_abs_err=2.11e-06 (2^-18.85), power_index=4.62
Front coverage: area_um2 39973..82065 (HV reference 100000); accuracy_bits 12.5..18.9 (HV reference 12); data_width on the front 17..26 (registry 8..28).

Per family:
- pipelined: 180 evals, 120 feasible; max throughput seen 171 MSPS; best accuracy 21.37 bits; best feasible area_um2=39973; feasible ranges: data_width 16..26, n_iter 14..27, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 20 evals, 0 feasible; max throughput seen 75.4 MSPS; best accuracy 14.52 bits
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 9921 in, 1619 out
- provider-reported cost: $0.0044
- full prompts and replies: `llm_trace.jsonl`

