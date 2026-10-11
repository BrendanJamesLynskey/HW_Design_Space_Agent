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

## Pareto front (17 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 39973 | 867 | 132.4 | 16 | 2.3 | 0.00017 (2^-12.53) | 12.53 |
| 1 | `pipelined:data_width=18,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc` | 41712 | 901 | 132.4 | 16 | 2.39 | 0.000163 (2^-12.58) | 12.58 |
| 2 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=2,rounding=round` | 43313 | 916 | 132.4 | 16 | 2.45 | 0.000144 (2^-12.76) | 12.76 |
| 3 | `pipelined:data_width=17,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 43694 | 944 | 137.6 | 18 | 2.5 | 0.000139 (2^-12.81) | 12.81 |
| 4 | `pipelined:data_width=18,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 45159 | 975 | 137.6 | 18 | 2.59 | 0.000108 (2^-13.18) | 13.18 |
| 5 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 45892 | 991 | 132.4 | 18 | 2.63 | 8.35e-05 (2^-13.55) | 13.55 |
| 6 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 48233 | 1020 | 132.4 | 18 | 2.72 | 6.45e-05 (2^-13.92) | 13.92 |
| 7 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 49611 | 1048 | 132.4 | 18 | 2.8 | 5.46e-05 (2^-14.16) | 14.16 |
| 8 | `pipelined:data_width=22,n_iter=16,angle_guard=3,frac_guard=0,rounding=trunc` | 55414 | 1195 | 111.3 | 18 | 3.17 | 3.7e-05 (2^-14.72) | 14.72 |
| 9 | `pipelined:data_width=21,n_iter=17,angle_guard=2,frac_guard=0,rounding=trunc` | 55870 | 1203 | 118.9 | 19 | 3.19 | 3.12e-05 (2^-14.97) | 14.97 |
| 10 | `pipelined:data_width=25,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 59809 | 1290 | 111.3 | 18 | 3.42 | 3.1e-05 (2^-14.98) | 14.98 |
| 11 | `pipelined:data_width=25,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc` | 61274 | 1321 | 104.7 | 18 | 3.51 | 3.08e-05 (2^-14.99) | 14.99 |
| 12 | `pipelined:data_width=26,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 62007 | 1337 | 107.9 | 18 | 3.55 | 3.08e-05 (2^-14.99) | 14.99 |
| 13 | `pipelined:data_width=26,n_iter=16,angle_guard=3,frac_guard=0,rounding=trunc` | 64204 | 1384 | 98.8 | 18 | 3.67 | 3.06e-05 (2^-14.99) | 14.99 |
| 14 | `pipelined:data_width=25,n_iter=17,angle_guard=2,frac_guard=0,rounding=round` | 65229 | 1404 | 104.7 | 19 | 3.73 | 1.56e-05 (2^-15.97) | 15.97 |
| 15 | `pipelined:data_width=26,n_iter=17,angle_guard=2,frac_guard=0,rounding=round` | 67568 | 1454 | 101.6 | 19 | 3.86 | 1.54e-05 (2^-15.99) | 15.99 |
| 16 | `pipelined:data_width=21,n_iter=25,angle_guard=2,frac_guard=0,rounding=round` | 82956 | 1770 | 118.9 | 27 | 4.71 | 1.15e-05 (2^-16.41) | 16.41 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires throughput >= 32 Msps and p99 batch latency <= 0.5 us for 32 simultaneous requests. The pipelined family is the natural fit: it produces 1 result/cycle, so throughput = Fmax. The critical constraint is the batch latency: all 32 requests arrive at the tick, and the last one exits after N+2 cycles. So (N+2)/Fmax <= 0.5 us. This couples N and Fmax tightly. For the minimum-area design, I want the smallest N and data_width that meet max_abs_err <= 2^-12. With rounding=round and modest guards, n_iter=14 with data_width=16 should give ~14-bit accuracy. The Fmax must then be >= (N+2)/0.5us = 2*(N+2) MHz. For N=14, Fmax >= 32 MHz. I search n_iter 12..20 to find the sweet spot where the area (which grows with N and data_width) is minimized while both the accuracy and batch-latency constraints are met. data_width 14..18 brackets the minimum width that achieves 12-bit accuracy with the chosen guards. angle_guard and frac_guard are kept small (0..2) to limit area while providing the accuracy margin. I allocate all budget to pipelined since pipelined_m with m>1 would have the same per-cycle throughput but higher latency (ceil(N/m)+2), making the batch constraint harder to meet, and m=1 is just pipelined. So pipelined is the only viable family for this spec's tight batch-latency constraint.*)
- `pipelined` (60 evals): data_width=14..18, n_iter=12..20, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Fully pipelined gives 1 result/cycle, so at Fmax >= 32 MHz it meets throughput_msps >= 32. Latency is N+2 cycles; with N in 12..20 and Fmax >= 32 MHz, latency is 14..22 cycles = 0.44..0.69 us. The p99_batch constraint (0.5 us) is tight: the 32 requests arrive at once, so the last result exits at (N+2) cycles after the tick. At 32 MHz, 15 cycles = 0.469 us passes, 16 cycles = 0.5 us is borderline. So N must be low enough that (N+2)/Fmax <= 0.5 us, i.e. N+2 <= 0.5e-6 * Fmax. For Fmax=32 MHz, N+2 <= 16, so N <= 14. For Fmax=40 MHz, N+2 <= 20, so N <= 18. The accuracy constraint max_abs_err <= 2^-12 = 0.000244 requires enough iterations and guard bits. With data_width=16, n_iter=14, angle_guard=1, frac_guard=1, rounding=round, accuracy should be around 14-15 bits. I focus on the low-N, moderate-width region where the batch latency constraint is satisfiable. data_width 14..18 covers the accuracy requirement (16 is the natural fit for 12-bit error with margin). n_iter 12..20 spans the latency/accuracy trade-off. angle_guard 0..2 and frac_guard 0..2 give the accuracy margin without excessive area.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 60 evaluations this round, 60 total; 38 feasible; hypervolume 1.193e+05 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established and robust. The minimum area design (39,973 um^2) comfortably satisfies the throughput constraint (132 MSPS >= 32) and the accuracy constraint (12.53 bits > 12 bits). The system constraint (sys_p99_batch_us <= 0.5 us) is also met with a margin (best seen 0.282 us). The front covers a reasonable range of accuracy (12.5 to 14.2 bits) against area (39,973 to 49,611 um^2). Since this is the final round and the current front provides a clear, feasible solution that minimizes area while meeting all constraints, stopping is the appropriate action. The selection rule (min area) will pick the 39,973 um^2 design, which is a valid and efficient solution.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.193e+05 (gain this round: n/a (first round)).
Feasible designs: 38 of 60 evaluations (25 unique).
Families explored so far: pipelined. Not yet explored: pipelined_m.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 163
- max_abs_err <= 0.000244141: 37% violate; best seen 5.46e-05 (2^-14.16)
- sys_p99_batch_us <= 0.5: 0% violate; best seen 0.282

Pareto front (feasible, 8 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.5, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53), power_index=2.3
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc] area_um2=41712, accuracy_bits=12.6, ffs=901, throughput_msps=132, max_abs_err=0.000163 (2^-12.58), power_index=2.39
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=43313, accuracy_bits=12.8, ffs=916, throughput_msps=132, max_abs_err=0.000144 (2^-12.76), power_index=2.45
- pipelined [data_width=17 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=43694, accuracy_bits=12.8, ffs=944, throughput_msps=138, max_abs_err=0.000139 (2^-12.81), power_index=2.5
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=45159, accuracy_bits=13.2, ffs=975, throughput_msps=138, max_abs_err=0.000108 (2^-13.18), power_index=2.59
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=1 rounding=round] area_um2=48233, accuracy_bits=13.9, ffs=1020, throughput_msps=132, max_abs_err=6.45e-05 (2^-13.92), power_index=2.72
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
Front coverage: area_um2 39973..49611 (HV reference 100000); accuracy_bits 12.5..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 60 evals, 38 feasible; max throughput seen 163 MSPS; best accuracy 14.16 bits; best feasible area_um2=39973; feasible ranges: data_width 16..18, n_iter 14..19, angle_guard 0..2, frac_guard 0..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (40 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (8 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 71 feasible; hypervolume 1.979e+05 (+65.9%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and robust. The minimum area design (39,973 um^2) comfortably satisfies the throughput constraint (132 MSPS >= 32) and the accuracy constraint (12.53 bits > 12 bits). The system constraint (sys_p99_batch_us <= 0.5 us) is also met with a margin (best seen 0.282 us). The front covers a reasonable range of accuracy (12.5 to 14.2 bits) against area (39,973 to 49,611 um^2). Since this is the final round and the current front provides a clear, feasible solution that minimizes area while meeting all constraints, stopping is the appropriate action. The selection rule (min area) will pick the 39,973 um^2 design, which is a valid and efficient solution.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.979e+05 (gain this round: +65.9%).
Feasible designs: 71 of 100 evaluations (55 unique).
Families explored so far: pipelined. Not yet explored: pipelined_m.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 163
- max_abs_err <= 0.000244141: 24% violate; best seen 1.41e-07 (2^-22.76)
- sys_p99_batch_us <= 0.5: 5% violate; best seen 0.282

Pareto front (feasible, 17 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] area_um2=39973, accuracy_bits=12.5, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53), power_index=2.3
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=43313, accuracy_bits=12.8, ffs=916, throughput_msps=132, max_abs_err=0.000144 (2^-12.76), power_index=2.45
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=45159, accuracy_bits=13.2, ffs=975, throughput_msps=138, max_abs_err=0.000108 (2^-13.18), power_index=2.59
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] area_um2=49611, accuracy_bits=14.2, ffs=1048, throughput_msps=132, max_abs_err=5.46e-05 (2^-14.16), power_index=2.8
- pipelined [data_width=21 n_iter=17 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=55870, accuracy_bits=15, ffs=1203, throughput_msps=119, max_abs_err=3.12e-05 (2^-14.97), power_index=3.19
- pipelined [data_width=25 n_iter=16 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=61274, accuracy_bits=15, ffs=1321, throughput_msps=105, max_abs_err=3.08e-05 (2^-14.99), power_index=3.51
- pipelined [data_width=26 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] area_um2=62007, accuracy_bits=15, ffs=1337, throughput_msps=108, max_abs_err=3.08e-05 (2^-14.99), power_index=3.55
- pipelined [data_width=25 n_iter=17 angle_guard=2 frac_guard=0 rounding=round] area_um2=65229, accuracy_bits=16, ffs=1404, throughput_msps=105, max_abs_err=1.56e-05 (2^-15.97), power_index=3.73
- pipelined [data_width=21 n_iter=25 angle_guard=2 frac_guard=0 rounding=round] area_um2=82956, accuracy_bits=16.4, ffs=1770, throughput_msps=119, max_abs_err=1.15e-05 (2^-16.41), power_index=4.71
Front coverage: area_um2 39973..82956 (HV reference 100000); accuracy_bits 12.5..16.4 (HV reference 12); data_width on the front 17..26 (registry 8..28).

Per family:
- pipelined: 100 evals, 71 feasible; max throughput seen 163 MSPS; best accuracy 22.76 bits; best feasible area_um2=39973; feasible ranges: data_width 16..26, n_iter 14..30, angle_guard -2..4, frac_guard 0..3
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5389 in, 1244 out
- provider-reported cost: $0.0031
- full prompts and replies: `llm_trace.jsonl`

