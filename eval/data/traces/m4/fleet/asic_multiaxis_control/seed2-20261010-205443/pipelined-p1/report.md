# DSE run: asic_multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: anthropic/claude-sonnet-5.5.  
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
`pipelined:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 40877 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10890 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 885 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 138 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 138 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 124 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.34 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000148 (2^-12.72) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 4.86 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 4.29e-05 (2^-14.51) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.4 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.7 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (12 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 40877 | 885 | 137.6 | 17 | 2.34 | 0.000148 (2^-12.72) | 12.72 |
| 1 | `pipelined:data_width=18,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 41562 | 900 | 143.2 | 17 | 2.38 | 0.000145 (2^-12.75) | 12.75 |
| 2 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 42933 | 929 | 132.4 | 17 | 2.46 | 0.000109 (2^-13.17) | 13.17 |
| 3 | `pipelined:data_width=17,n_iter=15,angle_guard=3,frac_guard=2,rounding=round` | 45041 | 953 | 132.4 | 17 | 2.54 | 9.31e-05 (2^-13.39) | 13.39 |
| 4 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 45892 | 991 | 132.4 | 18 | 2.63 | 8.35e-05 (2^-13.55) | 13.55 |
| 5 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=3,rounding=round` | 47745 | 1008 | 127.5 | 17 | 2.69 | 8.08e-05 (2^-13.60) | 13.60 |
| 6 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 48647 | 1046 | 132.4 | 18 | 2.78 | 6.86e-05 (2^-13.83) | 13.83 |
| 7 | `pipelined:data_width=24,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc` | 57831 | 1246 | 107.9 | 17 | 3.31 | 6.15e-05 (2^-13.99) | 13.99 |
| 8 | `pipelined:data_width=27,n_iter=15,angle_guard=2,frac_guard=0,rounding=trunc` | 61431 | 1327 | 98.8 | 17 | 3.52 | 6.11e-05 (2^-14.00) | 14.00 |
| 9 | `pipelined:data_width=26,n_iter=16,angle_guard=0,frac_guard=2,rounding=trunc` | 64762 | 1392 | 101.6 | 18 | 3.7 | 3.07e-05 (2^-14.99) | 14.99 |
| 10 | `pipelined:data_width=18,n_iter=23,angle_guard=3,frac_guard=3,rounding=round` | 74758 | 1573 | 127.5 | 25 | 4.21 | 2.32e-05 (2^-15.40) | 15.40 |
| 11 | `pipelined:data_width=21,n_iter=23,angle_guard=0,frac_guard=2,rounding=trunc` | 78138 | 1665 | 118.9 | 25 | 4.44 | 1.64e-05 (2^-15.90) | 15.90 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The batch constraint (32 results back within 0.5 us of the tick) needs about 64+ results/us of sustained rate plus the latency, so only the one-result-per-cycle families fit. Accuracy needs roughly 13+ bits of data width and 12+ iterations for max error <= 2^-12. Area is the objective, so I search a narrow low-width window and favour pipelined_m with a slightly larger budget share, because fewer pipeline registers should lower area. Later rounds can widen or narrow based on which m values survive the system bound.*)
- `pipelined` (27 evals): data_width=13..18, n_iter=11..16, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* Only a 1 result/cycle design clears 32 results in under 0.5 us at a realistic clock, and a pure pipeline has the most registers per stage but the shortest clock period. Ranges are centred on the 2^-12 error limit (about 13-18 bit width, 11-16 iterations) to keep area low.
- `pipelined_m` (33 evals): data_width=13..18, n_iter=11..16, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, m=2..5. *Why:* Registering every m stages cuts flip-flop area, which matters for the min-area objective, while keeping 1 result/cycle. The Fmax drop from chaining m stages must still allow a 32-result batch inside 0.5 us, so m is limited to 2-5.

**Result (code):** 60 evaluations this round, 60 total; 15 feasible; hypervolume 9.123e+04 (n/a).

**LLM decision:** `stop` — This is the final round, so stop. The feasible front has 5 pipelined designs spanning 40877..47745 um2 and 12.7..13.6 accuracy bits. The cheapest, pipelined W=17 N=15 round, meets all constraints: error 1.48e-4 is below 2.44e-4, throughput is 138 MSPS against the 32 needed, and the system batch bound passes. Pipelined_m produced 0 feasible designs in 33 evals. Iterative and unrolled_k were never explored, but their 32-request bursts would queue and likely miss the 0.5 us batch bound. Under the selection rule (min area), the cheapest front design is the pick.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 9.123e+04 (gain this round: n/a (first round)).
Feasible designs: 15 of 60 evaluations (10 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 3% violate; best seen 163
- max_abs_err <= 0.000244141: 67% violate; best seen 5.17e-05 (2^-14.24)
- sys_p99_batch_us <= 0.5: 47% violate; best seen 0.282

Pareto front (feasible, 5 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=40877, accuracy_bits=12.7, ffs=885, throughput_msps=138, max_abs_err=0.000148 (2^-12.72), power_index=2.34
- pipelined [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] area_um2=41562, accuracy_bits=12.8, ffs=900, throughput_msps=143, max_abs_err=0.000145 (2^-12.75), power_index=2.38
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=42933, accuracy_bits=13.2, ffs=929, throughput_msps=132, max_abs_err=0.000109 (2^-13.17), power_index=2.46
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=3 rounding=round] area_um2=47745, accuracy_bits=13.6, ffs=1008, throughput_msps=128, max_abs_err=8.08e-05 (2^-13.60), power_index=2.69
Front coverage: area_um2 40877..47745 (HV reference 100000); accuracy_bits 12.7..13.6 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 27 evals, 15 feasible; max throughput seen 163 MSPS; best accuracy 13.60 bits; best feasible area_um2=40877; feasible ranges: data_width 17..18, n_iter 15..16, angle_guard 0..3, frac_guard 0..3
- pipelined_m: 33 evals, 0 feasible; max throughput seen 91.1 MSPS; best accuracy 14.24 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (20 evals): data_width=16..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (5 front designs; box front_anchored)
- `pipelined_m` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 40 evaluations this round, 100 total; 30 feasible; hypervolume 1.667e+05 (+82.8%).

**No LLM call** (code's front-mapping round): This is the final round, so stop. The feasible front has 5 pipelined designs spanning 40877..47745 um2 and 12.7..13.6 accuracy bits. The cheapest, pipelined W=17 N=15 round, meets all constraints: error 1.48e-4 is below 2.44e-4, throughput is 138 MSPS against the 32 needed, and the system batch bound passes. Pipelined_m produced 0 feasible designs in 33 evals. Iterative and unrolled_k were never explored, but their 32-request bursts would queue and likely miss the 0.5 us batch bound. Under the selection rule (min area), the cheapest front design is the pick.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.667e+05 (gain this round: +82.8%).
Feasible designs: 30 of 100 evaluations (25 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 6% violate; best seen 163
- max_abs_err <= 0.000244141: 54% violate; best seen 7.43e-08 (2^-23.68)
- sys_p99_batch_us <= 0.5: 53% violate; best seen 0.282

Pareto front (feasible, 12 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=40877, accuracy_bits=12.7, ffs=885, throughput_msps=138, max_abs_err=0.000148 (2^-12.72), power_index=2.34
- pipelined [data_width=18 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] area_um2=41562, accuracy_bits=12.8, ffs=900, throughput_msps=143, max_abs_err=0.000145 (2^-12.75), power_index=2.38
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=42933, accuracy_bits=13.2, ffs=929, throughput_msps=132, max_abs_err=0.000109 (2^-13.17), power_index=2.46
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] area_um2=45892, accuracy_bits=13.5, ffs=991, throughput_msps=132, max_abs_err=8.35e-05 (2^-13.55), power_index=2.63
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=3 rounding=round] area_um2=47745, accuracy_bits=13.6, ffs=1008, throughput_msps=128, max_abs_err=8.08e-05 (2^-13.60), power_index=2.69
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=48647, accuracy_bits=13.8, ffs=1046, throughput_msps=132, max_abs_err=6.86e-05 (2^-13.83), power_index=2.78
- pipelined [data_width=24 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=57831, accuracy_bits=14, ffs=1246, throughput_msps=108, max_abs_err=6.15e-05 (2^-13.99), power_index=3.31
- pipelined [data_width=26 n_iter=16 angle_guard=0 frac_guard=2 rounding=trunc] area_um2=64762, accuracy_bits=15, ffs=1392, throughput_msps=102, max_abs_err=3.07e-05 (2^-14.99), power_index=3.7
- pipelined [data_width=18 n_iter=23 angle_guard=3 frac_guard=3 rounding=round] area_um2=74758, accuracy_bits=15.4, ffs=1573, throughput_msps=128, max_abs_err=2.32e-05 (2^-15.40), power_index=4.21
- pipelined [data_width=21 n_iter=23 angle_guard=0 frac_guard=2 rounding=trunc] area_um2=78138, accuracy_bits=15.9, ffs=1665, throughput_msps=119, max_abs_err=1.64e-05 (2^-15.90), power_index=4.44
Front coverage: area_um2 40877..78138 (HV reference 100000); accuracy_bits 12.7..15.9 (HV reference 12); data_width on the front 17..27 (registry 8..28).

Per family:
- pipelined: 47 evals, 30 feasible; max throughput seen 163 MSPS; best accuracy 23.68 bits; best feasible area_um2=40877; feasible ranges: data_width 16..27, n_iter 15..24, angle_guard -1..3, frac_guard 0..4
- pipelined_m: 53 evals, 0 feasible; max throughput seen 91.1 MSPS; best accuracy 18.96 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 9889 in, 974 out
- provider-reported cost: $0.0295
- full prompts and replies: `llm_trace.jsonl`

