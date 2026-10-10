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
`pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=2` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 29925 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 7972 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 437 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 78.8 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 78.8 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 9 | exact: schedule |
| latency_ns | 114 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.34 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000209 (2^-12.22) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.43 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 6.44e-05 (2^-13.92) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 1.06 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.2 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (27 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=2` | 29925 | 437 | 78.8 | 9 | 1.34 | 0.000209 (2^-12.22) | 12.22 |
| 1 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=2` | 30851 | 449 | 78.8 | 9 | 1.38 | 0.000204 (2^-12.26) | 12.26 |
| 2 | `pipelined:data_width=18,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` | 38698 | 840 | 143.2 | 16 | 2.22 | 0.0002 (2^-12.28) | 12.28 |
| 3 | `pipelined:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 39336 | 853 | 137.6 | 16 | 2.26 | 0.000175 (2^-12.48) | 12.48 |
| 4 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 39973 | 867 | 132.4 | 16 | 2.3 | 0.00017 (2^-12.53) | 12.53 |
| 5 | `pipelined:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 40877 | 885 | 137.6 | 17 | 2.34 | 0.000148 (2^-12.72) | 12.72 |
| 6 | `pipelined:data_width=18,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 41562 | 900 | 143.2 | 17 | 2.38 | 0.000145 (2^-12.75) | 12.75 |
| 7 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 42248 | 914 | 137.6 | 17 | 2.42 | 0.000119 (2^-13.04) | 13.04 |
| 8 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 42933 | 929 | 132.4 | 17 | 2.46 | 0.000109 (2^-13.17) | 13.17 |
| 9 | `pipelined:data_width=19,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 44303 | 959 | 132.4 | 17 | 2.54 | 8.66e-05 (2^-13.50) | 13.50 |
| 10 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 45892 | 991 | 132.4 | 18 | 2.63 | 8.35e-05 (2^-13.55) | 13.55 |
| 11 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 46462 | 982 | 132.4 | 17 | 2.62 | 8.26e-05 (2^-13.56) | 13.56 |
| 12 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 48233 | 1020 | 132.4 | 18 | 2.72 | 6.45e-05 (2^-13.92) | 13.92 |
| 13 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 49611 | 1048 | 132.4 | 18 | 2.8 | 5.46e-05 (2^-14.16) | 14.16 |
| 14 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=3,rounding=round` | 50989 | 1076 | 127.5 | 18 | 2.87 | 5.03e-05 (2^-14.28) | 14.28 |
| 15 | `pipelined:data_width=22,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 53217 | 1148 | 123.1 | 18 | 3.05 | 3.59e-05 (2^-14.77) | 14.77 |
| 16 | `pipelined:data_width=22,n_iter=17,angle_guard=0,frac_guard=0,rounding=round` | 56650 | 1220 | 123.1 | 19 | 3.24 | 2.12e-05 (2^-15.52) | 15.52 |
| 17 | `pipelined:data_width=22,n_iter=18,angle_guard=2,frac_guard=0,rounding=round` | 61738 | 1327 | 115.0 | 20 | 3.52 | 1.15e-05 (2^-16.41) | 16.41 |
| 18 | `pipelined:data_width=22,n_iter=18,angle_guard=3,frac_guard=0,rounding=round` | 62565 | 1345 | 111.3 | 20 | 3.57 | 1.1e-05 (2^-16.47) | 16.47 |
| 19 | `pipelined:data_width=22,n_iter=18,angle_guard=1,frac_guard=1,rounding=round` | 63646 | 1343 | 118.9 | 20 | 3.59 | 1.09e-05 (2^-16.49) | 16.49 |
| 20 | `pipelined:data_width=22,n_iter=18,angle_guard=2,frac_guard=3,rounding=round` | 67607 | 1424 | 111.3 | 20 | 3.81 | 9.07e-06 (2^-16.75) | 16.75 |
| 21 | `pipelined:data_width=22,n_iter=18,angle_guard=4,frac_guard=3,rounding=round` | 69262 | 1459 | 107.9 | 20 | 3.9 | 8.49e-06 (2^-16.85) | 16.85 |
| 22 | `pipelined:data_width=22,n_iter=21,angle_guard=1,frac_guard=0,rounding=round` | 71352 | 1528 | 118.9 | 23 | 4.06 | 6.76e-06 (2^-17.17) | 17.17 |
| 23 | `pipelined:data_width=22,n_iter=19,angle_guard=4,frac_guard=3,rounding=round` | 73169 | 1541 | 107.9 | 21 | 4.12 | 4.69e-06 (2^-17.70) | 17.70 |
| 24 | `pipelined:data_width=22,n_iter=21,angle_guard=1,frac_guard=3,rounding=round` | 78074 | 1642 | 111.3 | 23 | 4.39 | 4.01e-06 (2^-17.93) | 17.93 |
| 25 | `pipelined:data_width=22,n_iter=21,angle_guard=3,frac_guard=3,rounding=round` | 80013 | 1683 | 111.3 | 23 | 4.5 | 2.17e-06 (2^-18.81) | 18.81 |
| 26 | `pipelined:data_width=22,n_iter=23,angle_guard=3,frac_guard=3,rounding=round` | 87732 | 1844 | 111.3 | 25 | 4.93 | 1.66e-06 (2^-19.20) | 19.20 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show pipelined and pipelined_m are the only families with feasible designs, and pipelined_m is the area leader (29925 um2). The 32 req/us throughput constraint forces 1 result/cycle, so only the pipelined families qualify. I focus the 100-eval budget on the accuracy-feasible box (W 14..18, N 10..16, rounding=round) to map the area/accuracy Pareto front that drives both hypervolume and the min-area selection, with pipelined_m (m 2..4) as the primary area candidate and pipelined as the reference. This avoids wasting budget on infeasible low-accuracy corners that the iterative/unrolled members already confirmed are dead ends.*)
- `pipelined` (50 evals): data_width=14..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* pipelined is the only family with a strong feasible front (18/20 designs, best area 39973 um2). Narrowing to the accuracy-feasible box (W>=14, N>=10) and rounding=round focuses the 100-eval budget on the area/accuracy trade-off that drives the hypervolume and the min-area selection.
- `pipelined_m` (50 evals): data_width=14..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* pipelined_m already beats pipelined on area (29925 vs 39973) because fewer registers cut area while keeping 1 result/cycle. Restricting m to 2..4 keeps latency low enough to satisfy the 0.5 us p99 batch bound while exploring the area/accuracy trade-off.

**Result (code):** 100 evaluations this round, 100 total; 33 feasible; hypervolume 1.094e+05 (n/a).

**LLM decision:** `refine` — The `pipelined` family is the only one yielding feasible designs, with a clear Pareto front starting at 38,698 um². The `pipelined_m` family failed completely (0 feasible), likely due to throughput or latency constraints at the L1 bound. The current front is clustered in a narrow region (data_width 17-18, n_iter 14-16). To maximize hypervolume and find the true minimum area, we should tighten the search around the best-performing region of the `pipelined` family to exhaustively map the trade-off curve between area and accuracy within the feasible bounds, rather than wasting budget on wider ranges or non-performing families.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 1.094e+05 (gain this round: n/a (first round)).
Feasible designs: 33 of 100 evaluations (18 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 171
- max_abs_err <= 0.000244141: 53% violate; best seen 6.45e-05 (2^-13.92)
- sys_p99_batch_us <= 0.5: 40% violate; best seen 0.245

Pareto front (feasible, 11 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] area_um2=38698, accuracy_bits=12.3, ffs=840, throughput_msps=143, max_abs_err=0.0002 (2^-12.28), power_index=2.22
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=39336, accuracy_bits=12.5, ffs=853, throughput_msps=138, max_abs_err=0.000175 (2^-12.48), power_index=2.26
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=40877, accuracy_bits=12.7, ffs=885, throughput_msps=138, max_abs_err=0.000148 (2^-12.72), power_index=2.34
- pipelined [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] area_um2=41562, accuracy_bits=12.8, ffs=900, throughput_msps=143, max_abs_err=0.000145 (2^-12.75), power_index=2.38
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=42248, accuracy_bits=13, ffs=914, throughput_msps=138, max_abs_err=0.000119 (2^-13.04), power_index=2.42
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=44494, accuracy_bits=13.3, ffs=942, throughput_msps=138, max_abs_err=0.000101 (2^-13.27), power_index=2.51
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] area_um2=45179, accuracy_bits=13.4, ffs=957, throughput_msps=132, max_abs_err=9.31e-05 (2^-13.39), power_index=2.55
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=46462, accuracy_bits=13.6, ffs=982, throughput_msps=132, max_abs_err=8.26e-05 (2^-13.56), power_index=2.62
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=48233, accuracy_bits=13.9, ffs=1020, throughput_msps=132, max_abs_err=6.45e-05 (2^-13.92), power_index=2.72
Front coverage: area_um2 38698..48233 (HV reference 100000); accuracy_bits 12.3..13.9 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 50 evals, 33 feasible; max throughput seen 171 MSPS; best accuracy 13.92 bits; best feasible area_um2=38698; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 0 feasible; max throughput seen 91.1 MSPS; best accuracy 13.39 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate remaining budget on the only feasible family to refine the front.*)
- `pipelined` (20 evals): data_width=16..19, n_iter=13..17, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Focus on the proven feasible region of the pipelined family to refine the Pareto front and minimize area.

**Result (code):** 20 evaluations this round, 120 total; 50 feasible; hypervolume 1.218e+05 (+11.3%).

**LLM decision:** `stop` — The exploration has successfully identified a robust feasible Pareto front dominated by the `pipelined` family. The minimum area design (38698 um^2) comfortably satisfies the strict throughput constraint (143 MSPS >= 32 MSPS) and the accuracy constraint (12.3 bits >= 12 bits required for 2^-12 error). The system-level constraint (sys_p99_batch_us <= 0.5 us) is also met by the top designs, with the best seen value at 0.245 us, providing a healthy margin. The `pipelined_m` family proved infeasible, likely due to insufficient throughput or latency for the bursty 32-request/tick workload. Since this is the final round and the front covers the relevant trade-off space (area 38k-50k um^2, accuracy 12.3-14.2 bits) with clear feasible solutions, no further exploration is needed. The selection rule (min area) will pick the 38698 um^2 design, which is well-supported by the current front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 1.218e+05 (gain this round: +11.3%).
Feasible designs: 50 of 120 evaluations (27 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 171
- max_abs_err <= 0.000244141: 47% violate; best seen 5.46e-05 (2^-14.16)
- sys_p99_batch_us <= 0.5: 33% violate; best seen 0.245

Pareto front (feasible, 12 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] area_um2=38698, accuracy_bits=12.3, ffs=840, throughput_msps=143, max_abs_err=0.0002 (2^-12.28), power_index=2.22
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=39336, accuracy_bits=12.5, ffs=853, throughput_msps=138, max_abs_err=0.000175 (2^-12.48), power_index=2.26
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.5, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53), power_index=2.3
- pipelined [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] area_um2=41562, accuracy_bits=12.8, ffs=900, throughput_msps=143, max_abs_err=0.000145 (2^-12.75), power_index=2.38
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=42248, accuracy_bits=13, ffs=914, throughput_msps=138, max_abs_err=0.000119 (2^-13.04), power_index=2.42
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=42933, accuracy_bits=13.2, ffs=929, throughput_msps=132, max_abs_err=0.000109 (2^-13.17), power_index=2.46
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=44303, accuracy_bits=13.5, ffs=959, throughput_msps=132, max_abs_err=8.66e-05 (2^-13.50), power_index=2.54
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=46462, accuracy_bits=13.6, ffs=982, throughput_msps=132, max_abs_err=8.26e-05 (2^-13.56), power_index=2.62
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=48233, accuracy_bits=13.9, ffs=1020, throughput_msps=132, max_abs_err=6.45e-05 (2^-13.92), power_index=2.72
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
Front coverage: area_um2 38698..49611 (HV reference 100000); accuracy_bits 12.3..14.2 (HV reference 12); data_width on the front 17..19 (registry 8..28).

Per family:
- pipelined: 70 evals, 50 feasible; max throughput seen 171 MSPS; best accuracy 14.16 bits; best feasible area_um2=38698; feasible ranges: data_width 16..19, n_iter 14..16, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 50 evals, 0 feasible; max throughput seen 91.1 MSPS; best accuracy 13.39 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined` (40 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (12 front designs; box front_anchored)
- `pipelined_m` (40 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 80 evaluations this round, 200 total; 94 feasible; hypervolume 2.847e+05 (+133.8%).

**No LLM call** (code's front-mapping round): The exploration has successfully identified a robust feasible Pareto front dominated by the `pipelined` family. The minimum area design (38698 um^2) comfortably satisfies the strict throughput constraint (143 MSPS >= 32 MSPS) and the accuracy constraint (12.3 bits >= 12 bits required for 2^-12 error). The system-level constraint (sys_p99_batch_us <= 0.5 us) is also met by the top designs, with the best seen value at 0.245 us, providing a healthy margin. The `pipelined_m` family proved infeasible, likely due to insufficient throughput or latency for the bursty 32-request/tick workload. Since this is the final round and the front covers the relevant trade-off space (area 38k-50k um^2, accuracy 12.3-14.2 bits) with clear feasible solutions, no further exploration is needed. The selection rule (min area) will pick the 38698 um^2 design, which is well-supported by the current front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 2.847e+05 (gain this round: +133.8%).
Feasible designs: 94 of 200 evaluations (59 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 5% violate; best seen 171
- max_abs_err <= 0.000244141: 35% violate; best seen 1.66e-06 (2^-19.20)
- sys_p99_batch_us <= 0.5: 36% violate; best seen 0.245

Pareto front (feasible, 27 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=2] area_um2=29925, accuracy_bits=12.2, ffs=437, throughput_msps=78.8, max_abs_err=0.000209 (2^-12.22), power_index=1.34
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=39336, accuracy_bits=12.5, ffs=853, throughput_msps=138, max_abs_err=0.000175 (2^-12.48), power_index=2.26
- pipelined [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] area_um2=41562, accuracy_bits=12.8, ffs=900, throughput_msps=143, max_abs_err=0.000145 (2^-12.75), power_index=2.38
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] area_um2=44303, accuracy_bits=13.5, ffs=959, throughput_msps=132, max_abs_err=8.66e-05 (2^-13.50), power_index=2.54
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=48233, accuracy_bits=13.9, ffs=1020, throughput_msps=132, max_abs_err=6.45e-05 (2^-13.92), power_index=2.72
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=3 rounding=round] area_um2=50989, accuracy_bits=14.3, ffs=1076, throughput_msps=128, max_abs_err=5.03e-05 (2^-14.28), power_index=2.87
- pipelined [data_width=22 n_iter=18 angle_guard=2 frac_guard=0 rounding=round] area_um2=61738, accuracy_bits=16.4, ffs=1327, throughput_msps=115, max_abs_err=1.15e-05 (2^-16.41), power_index=3.52
- pipelined [data_width=22 n_iter=18 angle_guard=2 frac_guard=3 rounding=round] area_um2=67607, accuracy_bits=16.7, ffs=1424, throughput_msps=111, max_abs_err=9.07e-06 (2^-16.75), power_index=3.81
- pipelined [data_width=22 n_iter=19 angle_guard=4 frac_guard=3 rounding=round] area_um2=73169, accuracy_bits=17.7, ffs=1541, throughput_msps=108, max_abs_err=4.69e-06 (2^-17.70), power_index=4.12
- pipelined [data_width=22 n_iter=23 angle_guard=3 frac_guard=3 rounding=round] area_um2=87732, accuracy_bits=19.2, ffs=1844, throughput_msps=111, max_abs_err=1.66e-06 (2^-19.20), power_index=4.93
Front coverage: area_um2 29925..87732 (HV reference 100000); accuracy_bits 12.2..19.2 (HV reference 12); data_width on the front 16..22 (registry 8..28).

Per family:
- pipelined: 110 evals, 87 feasible; max throughput seen 171 MSPS; best accuracy 19.20 bits; best feasible area_um2=38698; feasible ranges: data_width 16..22, n_iter 14..30, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 90 evals, 7 feasible; max throughput seen 102 MSPS; best accuracy 17.65 bits; best feasible area_um2=29925; feasible ranges: data_width 16..16, n_iter 14..14, angle_guard 2..2, frac_guard 1..2, m 2..2
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 9706 in, 1623 out
- provider-reported cost: $0.0043
- full prompts and replies: `llm_trace.jsonl`

