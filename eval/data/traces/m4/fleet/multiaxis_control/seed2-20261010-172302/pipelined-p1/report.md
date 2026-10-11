# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec multiaxis_control: Shared sin/cos unit for a 16-axis motor-control loop: a 1 MHz control tick issues 32 requests at once (Park + inverse Park per axis); all 32 results must be back within 0.44 us of the tick (p99 over ticks). Max error <= 2^-12. Minimise LUTs + FFs.
  constraint: throughput_msps >= 32
  constraint: max_abs_err <= 0.000244141
  constraint: sys_p99_batch_us <= 0.44
  objective: min luts_plus_ffs (HV ref 4000)
  objective: max accuracy_bits (HV ref 12)
  select: min luts_plus_ffs
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average)
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 954 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 282 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 61.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.49 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000121 (2^-13.02) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 7.9 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.65e-05 (2^-15.20) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.74 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (10 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,m=4` | 954 | 282 | 97.8 | 6 | 1.49 | 0.000121 (2^-13.02) | 13.02 |
| 1 | `pipelined_m:data_width=16,n_iter=16,angle_guard=2,frac_guard=4,rounding=round,m=4` | 1051 | 289 | 93.6 | 6 | 1.61 | 0.00011 (2^-13.15) | 13.15 |
| 2 | `pipelined_m:data_width=19,n_iter=16,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1080 | 315 | 93.6 | 6 | 1.68 | 5.64e-05 (2^-14.11) | 14.11 |
| 3 | `pipelined_m:data_width=18,n_iter=17,angle_guard=2,frac_guard=4,rounding=round,m=4` | 1223 | 388 | 93.6 | 7 | 1.94 | 3.87e-05 (2^-14.66) | 14.66 |
| 4 | `pipelined_m:data_width=19,n_iter=20,angle_guard=3,frac_guard=2,rounding=round,m=3` | 1447 | 538 | 119.3 | 9 | 2.39 | 1.48e-05 (2^-16.05) | 16.05 |
| 5 | `pipelined_m:data_width=19,n_iter=23,angle_guard=3,frac_guard=4,rounding=round,m=4` | 1761 | 486 | 89.6 | 8 | 2.7 | 1.02e-05 (2^-16.59) | 16.59 |
| 6 | `pipelined:data_width=23,n_iter=18,angle_guard=2,frac_guard=0,rounding=round` | 1385 | 1417 | 256.5 | 20 | 3.37 | 9.4e-06 (2^-16.70) | 16.70 |
| 7 | `pipelined:data_width=22,n_iter=18,angle_guard=3,frac_guard=3,rounding=round` | 1503 | 1479 | 256.5 | 20 | 3.59 | 8.49e-06 (2^-16.85) | 16.85 |
| 8 | `pipelined_m:data_width=27,n_iter=23,angle_guard=3,frac_guard=1,rounding=round,m=3` | 2195 | 805 | 110.0 | 10 | 3.61 | 3.1e-07 (2^-21.62) | 21.62 |
| 9 | `pipelined_m:data_width=27,n_iter=23,angle_guard=3,frac_guard=4,rounding=round,m=3` | 2334 | 847 | 105.9 | 10 | 3.83 | 2.67e-07 (2^-21.84) | 21.84 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 results within 0.44us of a 1us tick, which at a realistic ~74MHz Fmax means ~32 cycles of processing time. Only pipelined and pipelined_m families achieve 1 result/cycle throughput, making them the only viable families for this bursty workload. The throughput constraint (>=32 Msps) further confirms 1/cycle is needed. For accuracy, max_abs_err <= 2^-12 (~0.000244) is the binding constraint; CORDIC with N=12-16 iterations and W=14-18 bits should meet this. I focus data_width 14-18 and n_iter 12-20 to bracket the accuracy/area trade-off. frac_guard 0-4 and angle_guard -2..2 sweep the remaining accuracy knobs. For pipelined_m, m=2-4 balances FF reduction against latency (must stay well under 32 cycles to fit the burst window). The budget is split 55/45 between the two families since pipelined is the baseline and pipelined_m offers the main area-reduction opportunity.*)
- `pipelined` (33 evals): data_width=14..18, n_iter=12..20, angle_guard=-2..2, frac_guard=0..4, rounding=trunc|round. *Why:* Full pipelining gives 1 result/cycle, which is required to absorb the 32-request burst within the 0.44us window (needs ~32 cycles at 74MHz). n_iter 12-20 and data_width 14-18 target the 2^-12 error bound with minimal area; frac_guard/angle_guard sweep the accuracy/area trade-off.
- `pipelined_m` (27 evals): data_width=14..18, n_iter=12..20, angle_guard=-2..2, frac_guard=0..4, rounding=trunc|round, m=2..4. *Why:* pipelined_m with m=2-4 reduces FF count vs full pipelining while still achieving 1 result/cycle throughput. The burst of 32 requests must complete in ~32 cycles, so 1/cycle throughput is mandatory. m=2-4 keeps latency manageable (ceil(N/m)+2 cycles) while cutting register area. Same accuracy parameter sweep as pipelined.

**Result (code):** 60 evaluations this round, 60 total; 38 feasible; hypervolume 7173 (n/a).

**LLM decision:** `stop` — The exploration has successfully identified a feasible Pareto front that satisfies all system and accuracy constraints. The best design (pipelined_m, data_width=18, n_iter=16, m=4) achieves 13.02 bits of accuracy (well above the 12-bit requirement) with a resource cost of 1236 LUTs+FFs, which is significantly below the hypervolume reference point of 4000. The throughput (97.8 MSPS) and system latency (0.165 us p99 batch) comfortably meet the 32 MSPS and 0.44 us constraints. Since this is the final round, the current front is sufficient for selection.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 7173 (gain this round: n/a (first round)).
Feasible designs: 38 of 60 evaluations (31 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 37% violate; best seen 3.16e-05 (2^-14.95)
- sys_p99_batch_us <= 0.44: 0% violate; best seen 0.165

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1236, accuracy_bits=13, luts=954, ffs=282, throughput_msps=97.8, max_abs_err=0.000121 (2^-13.02), power_index=1.49
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=4 rounding=round m=4] luts_plus_ffs=1339, accuracy_bits=13.1, luts=1051, ffs=289, throughput_msps=93.6, max_abs_err=0.00011 (2^-13.15), power_index=1.61
- pipelined_m [data_width=18 n_iter=17 angle_guard=2 frac_guard=4 rounding=round m=4] luts_plus_ffs=1612, accuracy_bits=14.7, luts=1223, ffs=388, throughput_msps=93.6, max_abs_err=3.87e-05 (2^-14.66), power_index=1.94
- pipelined [data_width=18 n_iter=18 angle_guard=2 frac_guard=4 rounding=round] luts_plus_ffs=2572, accuracy_bits=14.9, luts=1297, ffs=1275, throughput_msps=264, max_abs_err=3.21e-05 (2^-14.93), power_index=3.1
- pipelined [data_width=18 n_iter=20 angle_guard=2 frac_guard=4 rounding=round] luts_plus_ffs=2863, accuracy_bits=14.9, luts=1445, ffs=1419, throughput_msps=264, max_abs_err=3.16e-05 (2^-14.95), power_index=3.45
Front coverage: luts_plus_ffs 1236..2863 (HV reference 4000); accuracy_bits 13..14.9 (HV reference 12); data_width on the front 16..18 (registry 8..28).

Per family:
- pipelined: 33 evals, 25 feasible; max throughput seen 273 MSPS; best accuracy 14.95 bits; best feasible luts_plus_ffs=1843; feasible ranges: data_width 17..18, n_iter 14..20, angle_guard 0..2, frac_guard 0..4
- pipelined_m: 27 evals, 13 feasible; max throughput seen 171 MSPS; best accuracy 14.66 bits; best feasible luts_plus_ffs=1236; feasible ranges: data_width 16..18, n_iter 14..20, angle_guard 0..2, frac_guard 0..4, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (24 evals): data_width=15..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (3 front designs; box front_anchored)
- `pipelined` (16 evals): data_width=17..28, n_iter=16..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (2 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 65 feasible; hypervolume 1.595e+04 (+122.4%).

**No LLM call** (code's front-mapping round): The exploration has successfully identified a feasible Pareto front that satisfies all system and accuracy constraints. The best design (pipelined_m, data_width=18, n_iter=16, m=4) achieves 13.02 bits of accuracy (well above the 12-bit requirement) with a resource cost of 1236 LUTs+FFs, which is significantly below the hypervolume reference point of 4000. The throughput (97.8 MSPS) and system latency (0.165 us p99 batch) comfortably meet the 32 MSPS and 0.44 us constraints. Since this is the final round, the current front is sufficient for selection.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.595e+04 (gain this round: +122.4%).
Feasible designs: 65 of 100 evaluations (57 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 27% violate; best seen 2.67e-07 (2^-21.84)
- sys_p99_batch_us <= 0.44: 9% violate; best seen 0.165

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1236, accuracy_bits=13, luts=954, ffs=282, throughput_msps=97.8, max_abs_err=0.000121 (2^-13.02), power_index=1.49
- pipelined_m [data_width=16 n_iter=16 angle_guard=2 frac_guard=4 rounding=round m=4] luts_plus_ffs=1339, accuracy_bits=13.1, luts=1051, ffs=289, throughput_msps=93.6, max_abs_err=0.00011 (2^-13.15), power_index=1.61
- pipelined_m [data_width=19 n_iter=16 angle_guard=3 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1395, accuracy_bits=14.1, luts=1080, ffs=315, throughput_msps=93.6, max_abs_err=5.64e-05 (2^-14.11), power_index=1.68
- pipelined_m [data_width=18 n_iter=17 angle_guard=2 frac_guard=4 rounding=round m=4] luts_plus_ffs=1612, accuracy_bits=14.7, luts=1223, ffs=388, throughput_msps=93.6, max_abs_err=3.87e-05 (2^-14.66), power_index=1.94
- pipelined_m [data_width=19 n_iter=20 angle_guard=3 frac_guard=2 rounding=round m=3] luts_plus_ffs=1985, accuracy_bits=16, luts=1447, ffs=538, throughput_msps=119, max_abs_err=1.48e-05 (2^-16.05), power_index=2.39
- pipelined_m [data_width=19 n_iter=23 angle_guard=3 frac_guard=4 rounding=round m=4] luts_plus_ffs=2247, accuracy_bits=16.6, luts=1761, ffs=486, throughput_msps=89.6, max_abs_err=1.02e-05 (2^-16.59), power_index=2.7
- pipelined [data_width=23 n_iter=18 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=2801, accuracy_bits=16.7, luts=1385, ffs=1417, throughput_msps=257, max_abs_err=9.4e-06 (2^-16.70), power_index=3.37
- pipelined [data_width=22 n_iter=18 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=2982, accuracy_bits=16.8, luts=1503, ffs=1479, throughput_msps=257, max_abs_err=8.49e-06 (2^-16.85), power_index=3.59
- pipelined_m [data_width=27 n_iter=23 angle_guard=3 frac_guard=1 rounding=round m=3] luts_plus_ffs=3000, accuracy_bits=21.6, luts=2195, ffs=805, throughput_msps=110, max_abs_err=3.1e-07 (2^-21.62), power_index=3.61
- pipelined_m [data_width=27 n_iter=23 angle_guard=3 frac_guard=4 rounding=round m=3] luts_plus_ffs=3182, accuracy_bits=21.8, luts=2334, ffs=847, throughput_msps=106, max_abs_err=2.67e-07 (2^-21.84), power_index=3.83
Front coverage: luts_plus_ffs 1236..3182 (HV reference 4000); accuracy_bits 13..21.8 (HV reference 12); data_width on the front 16..27 (registry 8..28).

Per family:
- pipelined: 49 evals, 40 feasible; max throughput seen 273 MSPS; best accuracy 21.22 bits; best feasible luts_plus_ffs=1843; feasible ranges: data_width 17..24, n_iter 14..27, angle_guard 0..3, frac_guard 0..4
- pipelined_m: 51 evals, 25 feasible; max throughput seen 171 MSPS; best accuracy 21.84 bits; best feasible luts_plus_ffs=1236; feasible ranges: data_width 15..27, n_iter 14..23, angle_guard 0..3, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5163 in, 1117 out
- provider-reported cost: $0.0017
- full prompts and replies: `llm_trace.jsonl`

