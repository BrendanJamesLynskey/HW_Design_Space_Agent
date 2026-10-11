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
`pipelined:data_width=18,n_iter=14,angle_guard=3,frac_guard=3,rounding=trunc` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 44176 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 11769 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 952 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 128 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 128 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 125 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.53 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000145 (2^-12.75) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 9.49 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.07e-05 (2^-14.27) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.32 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.8 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (9 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=14,angle_guard=3,frac_guard=3,rounding=trunc` | 44176 | 952 | 127.5 | 16 | 2.53 | 0.000145 (2^-12.75) | 12.75 |
| 1 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=round` | 44494 | 942 | 137.6 | 17 | 2.51 | 0.000101 (2^-13.27) | 13.27 |
| 2 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=4,rounding=trunc` | 47379 | 1017 | 123.1 | 17 | 2.7 | 9.56e-05 (2^-13.35) | 13.35 |
| 3 | `pipelined:data_width=18,n_iter=15,angle_guard=3,frac_guard=3,rounding=trunc` | 47467 | 1020 | 127.5 | 17 | 2.71 | 8.39e-05 (2^-13.54) | 13.54 |
| 4 | `pipelined:data_width=18,n_iter=16,angle_guard=1,frac_guard=2,rounding=round` | 48878 | 1032 | 132.4 | 18 | 2.76 | 7.47e-05 (2^-13.71) | 13.71 |
| 5 | `pipelined:data_width=18,n_iter=16,angle_guard=1,frac_guard=4,rounding=round` | 51634 | 1087 | 123.1 | 18 | 2.91 | 6.75e-05 (2^-13.85) | 13.85 |
| 6 | `pipelined:data_width=19,n_iter=27,angle_guard=0,frac_guard=0,rounding=round` | 79698 | 1699 | 137.6 | 29 | 4.52 | 6.48e-05 (2^-13.91) | 13.91 |
| 7 | `pipelined:data_width=18,n_iter=25,angle_guard=3,frac_guard=3,rounding=trunc` | 80376 | 1709 | 127.5 | 27 | 4.55 | 3.81e-05 (2^-14.68) | 14.68 |
| 8 | `pipelined:data_width=19,n_iter=27,angle_guard=4,frac_guard=0,rounding=round` | 84712 | 1805 | 118.9 | 29 | 4.81 | 3.74e-05 (2^-14.71) | 14.71 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec needs 32 Msps sustained throughput (32 requests every 1 us tick) and all 32 results back within 0.5 us of the tick. Only pipelined and pipelined_m produce 1 result/cycle, so they are the only families that can meet the throughput constraint without requiring Fmax > 32 MHz (pipelined) or > 32 MHz (pipelined_m). The accuracy constraint max_abs_err <= 2^-12 = 0.000244141 requires roughly 12+ effective bits; CORDIC with N=12..16 micro-rotations and W=14..18 with modest guards should cover this. Area is the primary objective, so I focus on the low-W, low-N end of the feasible accuracy region. pipelined_m with m=2..4 trades a small latency increase for significant FF/area savings, making it a strong area-minimiser candidate. I split the budget evenly between the two families to map the trade-off between full pipeline latency (lower latency, more FFs) and partial pipeline (higher latency, fewer FFs) and find where the area front bends. The sys_p99_batch_us <= 0.5 us constraint is the tightest system constraint: at Fmax = 64 MHz, 10 cycles = 156 ns, leaving ample margin for 32 results in 0.5 us; at Fmax = 32 MHz, 10 cycles = 312 ns, still within 0.5 us. So both families should have feasible points, and the search will reveal the exact area/accuracy/latency trade-off.*)
- `pipelined` (30 evals): data_width=14..18, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* 1 result/cycle meets the 32 Msps throughput constraint at Fmax >= 32 MHz. N=12..16 with W=14..18 and guards 0..4 is the region where max_abs_err <= 2^-12 is achievable; area grows with W and N, so the front lives here.
- `pipelined_m` (30 evals): data_width=14..18, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* Registering every m stages (m=2..4) cuts FF count and area vs fully pipelined while still giving 1 result/cycle. Latency ceil(N/m)+2 must stay small enough that 32 back-to-back results finish within 0.5 us of the tick; m=2..4 keeps latency <= ~10 cycles, which at Fmax >= 64 MHz fits the 0.5 us batch window.

**Result (code):** 60 evaluations this round, 60 total; 13 feasible; hypervolume 1.001e+05 (n/a).

**LLM decision:** `stop` — The exploration has successfully identified a feasible Pareto front that satisfies all system and accuracy constraints. The best design (pipelined, data_width=18, n_iter=15) achieves an area of 44,494 um^2, which is well below the hypervolume reference of 100,000 um^2, and provides 13.3 bits of accuracy, exceeding the 12-bit reference and the 2^-12 error constraint. The system constraint (sys_p99_batch_us <= 0.5 us) is met by the top designs (best seen 0.301 us), and throughput is sufficient (138 MSPS > 32 MSPS). Since this is the final round and the front covers the trade-off space effectively with a clear minimum-area candidate for the selection rule, stopping is the appropriate action.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.001e+05 (gain this round: n/a (first round)).
Feasible designs: 13 of 60 evaluations (9 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 156
- max_abs_err <= 0.000244141: 53% violate; best seen 6.75e-05 (2^-13.85)
- sys_p99_batch_us <= 0.5: 45% violate; best seen 0.301

Pareto front (feasible, 4 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=44494, accuracy_bits=13.3, ffs=942, throughput_msps=138, max_abs_err=0.000101 (2^-13.27), power_index=2.51
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=4 rounding=trunc] area_um2=47379, accuracy_bits=13.4, ffs=1017, throughput_msps=123, max_abs_err=9.56e-05 (2^-13.35), power_index=2.7
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] area_um2=48878, accuracy_bits=13.7, ffs=1032, throughput_msps=132, max_abs_err=7.47e-05 (2^-13.71), power_index=2.76
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=4 rounding=round] area_um2=51634, accuracy_bits=13.9, ffs=1087, throughput_msps=123, max_abs_err=6.75e-05 (2^-13.85), power_index=2.91
Front coverage: area_um2 44494..51634 (HV reference 100000); accuracy_bits 13.3..13.9 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- pipelined: 30 evals, 13 feasible; max throughput seen 156 MSPS; best accuracy 13.85 bits; best feasible area_um2=44494; feasible ranges: data_width 17..18, n_iter 15..16, angle_guard 0..1, frac_guard 1..4
- pipelined_m: 30 evals, 0 feasible; max throughput seen 86.6 MSPS; best accuracy 13.66 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (20 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (4 front designs; box front_anchored)
- `pipelined_m` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 40 evaluations this round, 100 total; 26 feasible; hypervolume 1.173e+05 (+17.1%).

**No LLM call** (code's front-mapping round): The exploration has successfully identified a feasible Pareto front that satisfies all system and accuracy constraints. The best design (pipelined, data_width=18, n_iter=15) achieves an area of 44,494 um^2, which is well below the hypervolume reference of 100,000 um^2, and provides 13.3 bits of accuracy, exceeding the 12-bit reference and the 2^-12 error constraint. The system constraint (sys_p99_batch_us <= 0.5 us) is met by the top designs (best seen 0.301 us), and throughput is sufficient (138 MSPS > 32 MSPS). Since this is the final round and the front covers the trade-off space effectively with a clear minimum-area candidate for the selection rule, stopping is the appropriate action.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.173e+05 (gain this round: +17.1%).
Feasible designs: 26 of 100 evaluations (20 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 6% violate; best seen 156
- max_abs_err <= 0.000244141: 45% violate; best seen 7.95e-08 (2^-23.58)
- sys_p99_batch_us <= 0.5: 49% violate; best seen 0.301

Pareto front (feasible, 9 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=44176, accuracy_bits=12.8, ffs=952, throughput_msps=128, max_abs_err=0.000145 (2^-12.75), power_index=2.53
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] area_um2=44494, accuracy_bits=13.3, ffs=942, throughput_msps=138, max_abs_err=0.000101 (2^-13.27), power_index=2.51
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=4 rounding=trunc] area_um2=47379, accuracy_bits=13.4, ffs=1017, throughput_msps=123, max_abs_err=9.56e-05 (2^-13.35), power_index=2.7
- pipelined [data_width=18 n_iter=15 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=47467, accuracy_bits=13.5, ffs=1020, throughput_msps=128, max_abs_err=8.39e-05 (2^-13.54), power_index=2.71
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] area_um2=48878, accuracy_bits=13.7, ffs=1032, throughput_msps=132, max_abs_err=7.47e-05 (2^-13.71), power_index=2.76
- pipelined [data_width=18 n_iter=16 angle_guard=1 frac_guard=4 rounding=round] area_um2=51634, accuracy_bits=13.9, ffs=1087, throughput_msps=123, max_abs_err=6.75e-05 (2^-13.85), power_index=2.91
- pipelined [data_width=19 n_iter=27 angle_guard=0 frac_guard=0 rounding=round] area_um2=79698, accuracy_bits=13.9, ffs=1699, throughput_msps=138, max_abs_err=6.48e-05 (2^-13.91), power_index=4.52
- pipelined [data_width=18 n_iter=25 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=80376, accuracy_bits=14.7, ffs=1709, throughput_msps=128, max_abs_err=3.81e-05 (2^-14.68), power_index=4.55
- pipelined [data_width=19 n_iter=27 angle_guard=4 frac_guard=0 rounding=round] area_um2=84712, accuracy_bits=14.7, ffs=1805, throughput_msps=119, max_abs_err=3.74e-05 (2^-14.71), power_index=4.81
Front coverage: area_um2 44176..84712 (HV reference 100000); accuracy_bits 12.8..14.7 (HV reference 12); data_width on the front 18..19 (registry 8..28).

Per family:
- pipelined: 50 evals, 26 feasible; max throughput seen 156 MSPS; best accuracy 23.58 bits; best feasible area_um2=44176; feasible ranges: data_width 17..28, n_iter 14..27, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 50 evals, 0 feasible; max throughput seen 96.1 MSPS; best accuracy 22.53 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5076 in, 1267 out
- provider-reported cost: $0.0022
- full prompts and replies: `llm_trace.jsonl`

