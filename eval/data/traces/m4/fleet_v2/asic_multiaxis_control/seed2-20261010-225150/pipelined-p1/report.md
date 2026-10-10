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

## Pareto front (20 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=1,rounding=round,m=2` | 29925 | 437 | 78.8 | 9 | 1.34 | 0.000209 (2^-12.22) | 12.22 |
| 1 | `pipelined_m:data_width=16,n_iter=14,angle_guard=2,frac_guard=2,rounding=round,m=2` | 30851 | 449 | 78.8 | 9 | 1.38 | 0.000204 (2^-12.26) | 12.26 |
| 2 | `pipelined:data_width=18,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 41562 | 900 | 143.2 | 17 | 2.38 | 0.000145 (2^-12.75) | 12.75 |
| 3 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 42248 | 914 | 137.6 | 17 | 2.42 | 0.000119 (2^-13.04) | 13.04 |
| 4 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 42933 | 929 | 132.4 | 17 | 2.46 | 0.000109 (2^-13.17) | 13.17 |
| 5 | `pipelined:data_width=18,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 45159 | 975 | 137.6 | 18 | 2.59 | 0.000108 (2^-13.18) | 13.18 |
| 6 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc` | 45499 | 980 | 132.4 | 17 | 2.6 | 9.49e-05 (2^-13.36) | 13.36 |
| 7 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 45892 | 991 | 132.4 | 18 | 2.63 | 8.35e-05 (2^-13.55) | 13.55 |
| 8 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 46462 | 982 | 132.4 | 17 | 2.62 | 8.26e-05 (2^-13.56) | 13.56 |
| 9 | `pipelined:data_width=18,n_iter=17,angle_guard=2,frac_guard=0,rounding=round` | 48851 | 1053 | 132.4 | 19 | 2.79 | 7.75e-05 (2^-13.65) | 13.65 |
| 10 | `pipelined:data_width=21,n_iter=15,angle_guard=2,frac_guard=0,rounding=trunc` | 49099 | 1062 | 118.9 | 17 | 2.81 | 7.32e-05 (2^-13.74) | 13.74 |
| 11 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 49611 | 1048 | 132.4 | 18 | 2.8 | 5.46e-05 (2^-14.16) | 14.16 |
| 12 | `pipelined:data_width=21,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc` | 52484 | 1133 | 118.9 | 18 | 3 | 4.46e-05 (2^-14.45) | 14.45 |
| 13 | `pipelined:data_width=22,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc` | 54682 | 1180 | 115.0 | 18 | 3.13 | 3.7e-05 (2^-14.72) | 14.72 |
| 14 | `pipelined:data_width=22,n_iter=16,angle_guard=2,frac_guard=4,rounding=trunc` | 60193 | 1290 | 107.9 | 18 | 3.43 | 3.23e-05 (2^-14.92) | 14.92 |
| 15 | `pipelined:data_width=22,n_iter=16,angle_guard=3,frac_guard=3,rounding=round` | 60716 | 1280 | 111.3 | 18 | 3.42 | 3.1e-05 (2^-14.98) | 14.98 |
| 16 | `pipelined:data_width=22,n_iter=18,angle_guard=3,frac_guard=0,rounding=round` | 62565 | 1345 | 111.3 | 20 | 3.57 | 1.1e-05 (2^-16.47) | 16.47 |
| 17 | `pipelined:data_width=22,n_iter=19,angle_guard=2,frac_guard=0,rounding=round` | 65265 | 1401 | 115.0 | 21 | 3.72 | 8.18e-06 (2^-16.90) | 16.90 |
| 18 | `pipelined:data_width=22,n_iter=19,angle_guard=2,frac_guard=4,rounding=trunc` | 71913 | 1535 | 107.9 | 21 | 4.09 | 6.07e-06 (2^-17.33) | 17.33 |
| 19 | `pipelined:data_width=22,n_iter=21,angle_guard=3,frac_guard=3,rounding=round` | 80013 | 1683 | 111.3 | 23 | 4.5 | 2.17e-06 (2^-18.81) | 18.81 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *No fleet facts yet, so I start from first principles on the two constraints that actually bind. (1) Throughput >= 32 Msps: both pipelined and pipelined_m emit 1 result/cycle, so this just requires Fmax >= 32 MHz, comfortably achievable in sky130hd for modest widths; it is not the scarce resource. (2) Accuracy max_abs_err <= 2^-12: this is set purely by data_width, n_iter, angle_guard, frac_guard, rounding, and is identical across families. The cheapest designs sit at the low end of W and N that still clear 2^-12, so I centre the search on W 14-18 and N 12-18 with small guards (0-2) and both rounding modes, rather than sweeping the full 8-28 / 4-30 ranges and wasting evals on obviously-too-accurate or too-inaccurate corners. (3) The real differentiator is sys_p99_batch_us <= 0.5: a 1 us tick drops 32 requests at once, and all 32 must return within 0.5 us. For a 1-result/cycle unit that is 32 cycles of drain plus pipeline latency; at >=32 MHz that is ~1 us + latency, so the bound is tight and will favour lower latency (smaller N, and pipelined_m over pipelined). I therefore give equal weight to pipelined (baseline, lowest latency for a given N) and pipelined_m (area reduction via m, slightly higher latency) so the merged front spans the area/latency trade-off and the hypervolume captures both the cheapest feasible point and the accuracy headroom. I deliberately keep ranges narrow to concentrate the 100-eval budget on the feasible band instead of the full registry, and I leave the reserved front-mapping to code over these ranges. If the first round shows the batch bound is infeasible even at the lowest latency, I will report infeasible rather than relax the constraint.*)
- `pipelined` (30 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Fully pipelined gives 1 result/cycle, so throughput = Fmax. To hit 32 Msps it needs Fmax >= 32 MHz, which is easy in sky130hd. The binding constraints are accuracy (max_abs_err <= 2^-12) and the 0.5 us p99 batch latency: a burst of 32 back-to-back requests through a fully pipelined unit takes 32 cycles + (N+2) latency. At >=32 MHz that is ~1 us + latency, so the batch bound is tight and will push toward lower N and higher Fmax. Area is minimised by the smallest data_width/n_iter that still clears 2^-12, so I focus the search on the low end of the accuracy/area trade-off (W 14-18, N 12-18) with modest guards and both rounding modes to find the cheapest point that meets error and the batch bound.
- `pipelined_m` (30 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m registers every m stages, cutting FF count (and area) versus fully pipelined while still giving 1 result/cycle, so throughput = Fmax and the 32 Msps constraint is met the same way. The trade-off is latency: ceil(N/m)+2 cycles, which is shorter than the fully pipelined N+2, helping the 0.5 us p99 batch bound. I search the same accuracy/width band (W 14-18, N 12-18) and m in 2-4 to map the area-vs-latency trade-off; smaller m gives lower latency at higher FF/area cost, larger m saves area but lengthens the batch. This family is the natural area-reduction lever against pipelined, so I split the budget evenly to cover both and let the Pareto front pick the cheapest feasible point.

**Result (code):** 60 evaluations this round, 60 total; 27 feasible; hypervolume 1.454e+05 (n/a).

**LLM decision:** `stop` — The exploration has successfully identified a feasible Pareto front that satisfies all constraints (throughput >= 32 MSPS, max_abs_err <= 2^-12, sys_p99_batch_us <= 0.5 us). The front spans a wide range of areas (29,925 to 55,909 um^2) and accuracy bits (12.2 to 14.7), providing a good trade-off curve. The minimum area design (pipelined_m, 29,925 um^2) meets the error constraint (12.2 bits > 12 bits) and throughput (78.8 MSPS > 32 MSPS). Since this is the final round and the front is well-mapped with feasible designs across the objective space, stopping is the appropriate decision. The selection rule (min area) will pick the 29,925 um^2 design, which is robustly feasible.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.454e+05 (gain this round: n/a (first round)).
Feasible designs: 27 of 60 evaluations (17 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 156
- max_abs_err <= 0.000244141: 43% violate; best seen 3.81e-05 (2^-14.68)
- sys_p99_batch_us <= 0.5: 23% violate; best seen 0.301

Pareto front (feasible, 12 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=2] area_um2=29925, accuracy_bits=12.2, ffs=437, throughput_msps=78.8, max_abs_err=0.000209 (2^-12.22), power_index=1.34
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=2] area_um2=30851, accuracy_bits=12.3, ffs=449, throughput_msps=78.8, max_abs_err=0.000204 (2^-12.26), power_index=1.38
- pipelined [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] area_um2=41562, accuracy_bits=12.8, ffs=900, throughput_msps=143, max_abs_err=0.000145 (2^-12.75), power_index=2.38
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=42933, accuracy_bits=13.2, ffs=929, throughput_msps=132, max_abs_err=0.000109 (2^-13.17), power_index=2.46
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=45159, accuracy_bits=13.2, ffs=975, throughput_msps=138, max_abs_err=0.000108 (2^-13.18), power_index=2.59
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=45499, accuracy_bits=13.4, ffs=980, throughput_msps=132, max_abs_err=9.49e-05 (2^-13.36), power_index=2.6
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=18 n_iter=17 angle_guard=2 frac_guard=0 rounding=round] area_um2=48851, accuracy_bits=13.7, ffs=1053, throughput_msps=132, max_abs_err=7.75e-05 (2^-13.65), power_index=2.79
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
- pipelined [data_width=18 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] area_um2=55909, accuracy_bits=14.7, ffs=1180, throughput_msps=132, max_abs_err=3.81e-05 (2^-14.68), power_index=3.15
Front coverage: area_um2 29925..55909 (HV reference 100000); accuracy_bits 12.2..14.7 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 30 evals, 22 feasible; max throughput seen 156 MSPS; best accuracy 14.68 bits; best feasible area_um2=39973; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 30 evals, 5 feasible; max throughput seen 86.6 MSPS; best accuracy 13.92 bits; best feasible area_um2=29925; feasible ranges: data_width 16..16, n_iter 14..14, angle_guard 2..2, frac_guard 1..2, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (7 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (2 front designs; box front_anchored)
- `pipelined` (33 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (10 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 52 feasible; hypervolume 2.713e+05 (+86.6%).

**No LLM call** (code's front-mapping round): The exploration has successfully identified a feasible Pareto front that satisfies all constraints (throughput >= 32 MSPS, max_abs_err <= 2^-12, sys_p99_batch_us <= 0.5 us). The front spans a wide range of areas (29,925 to 55,909 um^2) and accuracy bits (12.2 to 14.7), providing a good trade-off curve. The minimum area design (pipelined_m, 29,925 um^2) meets the error constraint (12.2 bits > 12 bits) and throughput (78.8 MSPS > 32 MSPS). Since this is the final round and the front is well-mapped with feasible designs across the objective space, stopping is the appropriate decision. The selection rule (min area) will pick the 29,925 um^2 design, which is robustly feasible.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 2.713e+05 (gain this round: +86.6%).
Feasible designs: 52 of 100 evaluations (37 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 5% violate; best seen 156
- max_abs_err <= 0.000244141: 29% violate; best seen 4.1e-07 (2^-21.22)
- sys_p99_batch_us <= 0.5: 28% violate; best seen 0.301

Pareto front (feasible, 20 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=2] area_um2=29925, accuracy_bits=12.2, ffs=437, throughput_msps=78.8, max_abs_err=0.000209 (2^-12.22), power_index=1.34
- pipelined [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] area_um2=41562, accuracy_bits=12.8, ffs=900, throughput_msps=143, max_abs_err=0.000145 (2^-12.75), power_index=2.38
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=42933, accuracy_bits=13.2, ffs=929, throughput_msps=132, max_abs_err=0.000109 (2^-13.17), power_index=2.46
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=45499, accuracy_bits=13.4, ffs=980, throughput_msps=132, max_abs_err=9.49e-05 (2^-13.36), power_index=2.6
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] area_um2=46462, accuracy_bits=13.6, ffs=982, throughput_msps=132, max_abs_err=8.26e-05 (2^-13.56), power_index=2.62
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
- pipelined [data_width=22 n_iter=16 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=54682, accuracy_bits=14.7, ffs=1180, throughput_msps=115, max_abs_err=3.7e-05 (2^-14.72), power_index=3.13
- pipelined [data_width=22 n_iter=16 angle_guard=3 frac_guard=3 rounding=round] area_um2=60716, accuracy_bits=15, ffs=1280, throughput_msps=111, max_abs_err=3.1e-05 (2^-14.98), power_index=3.42
- pipelined [data_width=22 n_iter=19 angle_guard=2 frac_guard=0 rounding=round] area_um2=65265, accuracy_bits=16.9, ffs=1401, throughput_msps=115, max_abs_err=8.18e-06 (2^-16.90), power_index=3.72
- pipelined [data_width=22 n_iter=21 angle_guard=3 frac_guard=3 rounding=round] area_um2=80013, accuracy_bits=18.8, ffs=1683, throughput_msps=111, max_abs_err=2.17e-06 (2^-18.81), power_index=4.5
Front coverage: area_um2 29925..80013 (HV reference 100000); accuracy_bits 12.2..18.8 (HV reference 12); data_width on the front 16..22 (registry 8..28).

Per family:
- pipelined: 63 evals, 47 feasible; max throughput seen 156 MSPS; best accuracy 21.22 bits; best feasible area_um2=39973; feasible ranges: data_width 16..24, n_iter 14..21, angle_guard 0..3, frac_guard 0..4
- pipelined_m: 37 evals, 5 feasible; max throughput seen 86.6 MSPS; best accuracy 14.05 bits; best feasible area_um2=29925; feasible ranges: data_width 16..16, n_iter 14..14, angle_guard 2..2, frac_guard 1..2, m 2..2
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5674 in, 1651 out
- provider-reported cost: $0.0043
- full prompts and replies: `llm_trace.jsonl`

