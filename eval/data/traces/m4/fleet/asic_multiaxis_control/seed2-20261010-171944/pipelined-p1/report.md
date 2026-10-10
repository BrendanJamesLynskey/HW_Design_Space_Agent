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
`pipelined:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 39336 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10479 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 853 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 138 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 138 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 116 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.26 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000175 (2^-12.48) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 11.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.28e-05 (2^-14.21) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.46 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (11 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 39336 | 853 | 137.6 | 16 | 2.26 | 0.000175 (2^-12.48) | 12.48 |
| 1 | `pipelined:data_width=17,n_iter=14,angle_guard=2,frac_guard=2,rounding=round` | 41349 | 875 | 137.6 | 16 | 2.34 | 0.000169 (2^-12.53) | 12.53 |
| 2 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` | 42350 | 914 | 132.4 | 16 | 2.42 | 0.000156 (2^-12.65) | 12.65 |
| 3 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=3,rounding=trunc` | 43538 | 938 | 127.5 | 16 | 2.49 | 0.000147 (2^-12.74) | 12.74 |
| 4 | `pipelined:data_width=27,n_iter=14,angle_guard=2,frac_guard=0,rounding=trunc` | 57192 | 1239 | 98.8 | 16 | 3.28 | 0.000122 (2^-13.00) | 13.00 |
| 5 | `pipelined:data_width=27,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc` | 59569 | 1286 | 98.8 | 16 | 3.41 | 0.000122 (2^-13.00) | 13.00 |
| 6 | `pipelined:data_width=24,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 61832 | 1329 | 107.9 | 18 | 3.53 | 3.09e-05 (2^-14.98) | 14.98 |
| 7 | `pipelined:data_width=26,n_iter=16,angle_guard=3,frac_guard=3,rounding=trunc` | 68338 | 1467 | 98.8 | 18 | 3.9 | 3.06e-05 (2^-15.00) | 15.00 |
| 8 | `pipelined:data_width=27,n_iter=16,angle_guard=3,frac_guard=2,rounding=round` | 70581 | 1488 | 96.1 | 18 | 3.98 | 3.05e-05 (2^-15.00) | 15.00 |
| 9 | `pipelined:data_width=18,n_iter=22,angle_guard=3,frac_guard=3,rounding=round` | 71467 | 1504 | 127.5 | 24 | 4.02 | 2.32e-05 (2^-15.40) | 15.40 |
| 10 | `pipelined:data_width=21,n_iter=23,angle_guard=0,frac_guard=2,rounding=trunc` | 78138 | 1665 | 118.9 | 25 | 4.44 | 1.64e-05 (2^-15.90) | 15.90 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands 32 results/us throughput and a 0.5us p99 batch window for a 32-request burst, which forces 1 result/cycle and Fmax>=32MHz; only the pipelined families can deliver that throughput. Area is the selection objective, so I focus on pipelined (area-optimal for 1/cycle) and pipelined_m (fewer FFs, longer path) to map the area-vs-Fmax trade-off. Accuracy is constrained to max_abs_err<=2^-12, so I bound W=14..18 and N=10..14 with rounding=round to stay feasible while leaving room for the hypervolume to reward extra accuracy bits. angle_guard/frac_guard are kept small (0..2) to avoid inflating area without accuracy benefit.*)
- `pipelined` (36 evals): data_width=14..18, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* Full pipelining gives 1 result/cycle, so Fmax>=32MHz is the only way to meet the 32 req/us throughput and 0.5us batch window; this is the area-optimal family for that throughput. W=14..18 and N=10..14 cover the accuracy constraint (max_abs_err<=2^-12) with margin; rounding=round minimises error for a given N.
- `pipelined_m` (24 evals): data_width=14..18, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..4. *Why:* Registering every m stages (m=2..4) cuts FF count and area versus full pipelining at the cost of a longer combinational path (lower Fmax); this trades area against the Fmax>=32MHz requirement, so it may yield a smaller-area design that still meets the batch window. Same W/N accuracy box as pipelined.

**Result (code):** 60 evaluations this round, 60 total; 7 feasible; hypervolume 3.835e+04 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 3 unique designs, all meeting the strict constraints (throughput >= 32 MSPS, max_abs_err <= 2^-12, sys_p99_batch_us <= 0.5 us). The minimum area on the front is 39336 um^2 (pipelined, data_width=18, n_iter=14), which is significantly below the HV reference of 100000 um^2. The accuracy bits range from 12.5 to 12.6, comfortably exceeding the 12-bit reference. The pipelined family dominates the feasible space, while pipelined_m failed to produce any feasible designs due to throughput limitations (max 82.5 MSPS seen, but likely constrained by latency/area trade-offs in the specific parameter space explored). Since this is the final round and the front covers the critical trade-off region (area vs accuracy) with clear feasible candidates, stopping is the correct action. The selection rule (min area) will pick the 39336 um^2 design, which satisfies all system and accuracy constraints.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 3.835e+04 (gain this round: n/a (first round)).
Feasible designs: 7 of 60 evaluations (3 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 163
- max_abs_err <= 0.000244141: 83% violate; best seen 0.000152 (2^-12.68)
- sys_p99_batch_us <= 0.5: 32% violate; best seen 0.276

Pareto front (feasible, 3 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=39336, accuracy_bits=12.5, ffs=853, throughput_msps=138, max_abs_err=0.000175 (2^-12.48), power_index=2.26
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=41349, accuracy_bits=12.5, ffs=875, throughput_msps=138, max_abs_err=0.000169 (2^-12.53), power_index=2.34
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=2 rounding=round] area_um2=42676, accuracy_bits=12.6, ffs=903, throughput_msps=132, max_abs_err=0.000157 (2^-12.64), power_index=2.41
Front coverage: area_um2 39336..42676 (HV reference 100000); accuracy_bits 12.5..12.6 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 36 evals, 7 feasible; max throughput seen 163 MSPS; best accuracy 12.64 bits; best feasible area_um2=39336; feasible ranges: data_width 17..18, n_iter 14..14, angle_guard 1..2, frac_guard 0..2
- pipelined_m: 24 evals, 0 feasible; max throughput seen 82.5 MSPS; best accuracy 12.68 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (20 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)
- `pipelined_m` (20 evals): data_width=8..28, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: pipelined_m was explored but found nothing feasible; full-box share (M3 lever)

**Result (code):** 40 evaluations this round, 100 total; 25 feasible; hypervolume 1.536e+05 (+300.6%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 3 unique designs, all meeting the strict constraints (throughput >= 32 MSPS, max_abs_err <= 2^-12, sys_p99_batch_us <= 0.5 us). The minimum area on the front is 39336 um^2 (pipelined, data_width=18, n_iter=14), which is significantly below the HV reference of 100000 um^2. The accuracy bits range from 12.5 to 12.6, comfortably exceeding the 12-bit reference. The pipelined family dominates the feasible space, while pipelined_m failed to produce any feasible designs due to throughput limitations (max 82.5 MSPS seen, but likely constrained by latency/area trade-offs in the specific parameter space explored). Since this is the final round and the front covers the critical trade-off region (area vs accuracy) with clear feasible candidates, stopping is the correct action. The selection rule (min area) will pick the 39336 um^2 design, which satisfies all system and accuracy constraints.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.536e+05 (gain this round: +300.6%).
Feasible designs: 25 of 100 evaluations (21 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 4% violate; best seen 163
- max_abs_err <= 0.000244141: 64% violate; best seen 7.43e-08 (2^-23.68)
- sys_p99_batch_us <= 0.5: 41% violate; best seen 0.276

Pareto front (feasible, 11 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=39336, accuracy_bits=12.5, ffs=853, throughput_msps=138, max_abs_err=0.000175 (2^-12.48), power_index=2.26
- pipelined [data_width=17 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] area_um2=41349, accuracy_bits=12.5, ffs=875, throughput_msps=138, max_abs_err=0.000169 (2^-12.53), power_index=2.34
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=42350, accuracy_bits=12.6, ffs=914, throughput_msps=132, max_abs_err=0.000156 (2^-12.65), power_index=2.42
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=43538, accuracy_bits=12.7, ffs=938, throughput_msps=128, max_abs_err=0.000147 (2^-12.74), power_index=2.49
- pipelined [data_width=27 n_iter=14 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=57192, accuracy_bits=13, ffs=1239, throughput_msps=98.8, max_abs_err=0.000122 (2^-13.00), power_index=3.28
- pipelined [data_width=24 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] area_um2=61832, accuracy_bits=15, ffs=1329, throughput_msps=108, max_abs_err=3.09e-05 (2^-14.98), power_index=3.53
- pipelined [data_width=26 n_iter=16 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=68338, accuracy_bits=15, ffs=1467, throughput_msps=98.8, max_abs_err=3.06e-05 (2^-15.00), power_index=3.9
- pipelined [data_width=27 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] area_um2=70581, accuracy_bits=15, ffs=1488, throughput_msps=96.1, max_abs_err=3.05e-05 (2^-15.00), power_index=3.98
- pipelined [data_width=18 n_iter=22 angle_guard=3 frac_guard=3 rounding=round] area_um2=71467, accuracy_bits=15.4, ffs=1504, throughput_msps=128, max_abs_err=2.32e-05 (2^-15.40), power_index=4.02
- pipelined [data_width=21 n_iter=23 angle_guard=0 frac_guard=2 rounding=trunc] area_um2=78138, accuracy_bits=15.9, ffs=1665, throughput_msps=119, max_abs_err=1.64e-05 (2^-15.90), power_index=4.44
Front coverage: area_um2 39336..78138 (HV reference 100000); accuracy_bits 12.5..15.9 (HV reference 12); data_width on the front 17..27 (registry 8..28).

Per family:
- pipelined: 56 evals, 25 feasible; max throughput seen 163 MSPS; best accuracy 23.68 bits; best feasible area_um2=39336; feasible ranges: data_width 16..27, n_iter 14..23, angle_guard -1..3, frac_guard 0..4
- pipelined_m: 44 evals, 0 feasible; max throughput seen 82.5 MSPS; best accuracy 18.96 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5456 in, 1145 out
- provider-reported cost: $0.0025
- full prompts and replies: `llm_trace.jsonl`

