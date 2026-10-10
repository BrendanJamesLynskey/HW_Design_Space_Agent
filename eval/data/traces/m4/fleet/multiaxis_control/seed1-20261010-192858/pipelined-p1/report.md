# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`pipelined_m:data_width=17,n_iter=17,angle_guard=0,frac_guard=1,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 1000 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 335 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 71.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.61 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000217 (2^-12.17) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 7.1 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 4.97e-05 (2^-14.30) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.63 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.2 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (14 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=17,angle_guard=0,frac_guard=1,rounding=trunc,m=4` | 1000 | 335 | 97.8 | 7 | 1.61 | 0.000217 (2^-12.17) | 12.17 |
| 1 | `pipelined_m:data_width=17,n_iter=17,angle_guard=1,frac_guard=1,rounding=trunc,m=4` | 1017 | 340 | 97.8 | 7 | 1.63 | 0.00019 (2^-12.36) | 12.36 |
| 2 | `pipelined_m:data_width=17,n_iter=17,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1051 | 348 | 93.6 | 7 | 1.68 | 0.000144 (2^-12.76) | 12.76 |
| 3 | `pipelined_m:data_width=19,n_iter=17,angle_guard=1,frac_guard=2,rounding=round,m=4` | 1192 | 384 | 93.6 | 7 | 1.9 | 3.97e-05 (2^-14.62) | 14.62 |
| 4 | `pipelined_m:data_width=25,n_iter=17,angle_guard=3,frac_guard=0,rounding=trunc,m=4` | 1422 | 479 | 86.0 | 7 | 2.29 | 1.58e-05 (2^-15.95) | 15.95 |
| 5 | `pipelined_m:data_width=25,n_iter=17,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1455 | 487 | 86.0 | 7 | 2.34 | 1.54e-05 (2^-15.98) | 15.98 |
| 6 | `pipelined_m:data_width=25,n_iter=17,angle_guard=4,frac_guard=3,rounding=round,m=4` | 1592 | 511 | 86.0 | 7 | 2.53 | 1.53e-05 (2^-15.99) | 15.99 |
| 7 | `pipelined_m:data_width=26,n_iter=18,angle_guard=3,frac_guard=0,rounding=trunc,m=3` | 1564 | 585 | 110.0 | 8 | 2.59 | 7.87e-06 (2^-16.96) | 16.96 |
| 8 | `pipelined:data_width=23,n_iter=20,angle_guard=0,frac_guard=2,rounding=trunc` | 1587 | 1606 | 256.5 | 22 | 3.84 | 4.67e-06 (2^-17.71) | 17.71 |
| 9 | `pipelined:data_width=28,n_iter=20,angle_guard=0,frac_guard=0,rounding=trunc` | 1807 | 1836 | 249.0 | 22 | 4.39 | 2.03e-06 (2^-18.91) | 18.91 |
| 10 | `pipelined:data_width=28,n_iter=20,angle_guard=0,frac_guard=2,rounding=trunc` | 1887 | 1909 | 249.0 | 22 | 4.57 | 1.97e-06 (2^-18.95) | 18.95 |
| 11 | `pipelined:data_width=23,n_iter=22,angle_guard=4,frac_guard=4,rounding=trunc` | 1930 | 1937 | 249.0 | 24 | 4.66 | 1.17e-06 (2^-19.70) | 19.70 |
| 12 | `pipelined:data_width=28,n_iter=22,angle_guard=0,frac_guard=3,rounding=round` | 2189 | 2143 | 242.0 | 24 | 5.21 | 5.43e-07 (2^-20.81) | 20.81 |
| 13 | `pipelined:data_width=28,n_iter=30,angle_guard=2,frac_guard=0,rounding=trunc` | 2817 | 2815 | 249.0 | 32 | 6.78 | 2.17e-07 (2^-22.13) | 22.13 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 results within 0.44 us of a 1 MHz tick, i.e. a burst of 32 requests must drain in 0.44 us. With 1 result/cycle, this needs roughly Fmax >= (32 + latency)/0.44 MHz. Pipelined has the lowest latency and highest expected Fmax, so it gets the larger share. Pipelined_m may reduce LUT+FF area by sharing pipeline registers, but its lower Fmax could violate the system bound; exploring m=2..6 maps that risk. Accuracy needs at least 12 effective bits, so n_iter starts at 12 and data_width at 14 (output LSB 2^-12) to avoid wasting budget on clearly infeasible points. The ranges are deliberately moderate to let Optuna find the Pareto front within 100 evaluations, with later rounds reserved for refinement around the feasible region.*)
- `pipelined` (33 evals): data_width=14..20, n_iter=12..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Pipelined gives 1 result/cycle and the shortest latency among my families (N+2). The system burst of 32 requests must drain within 0.44 us, so a high Fmax is essential; pipelined has the best chance of meeting sys_p99_batch_us. I search data_width 14..20 and n_iter 12..20 to cover the accuracy constraint (max_abs_err <= 2^-12) while allowing area reduction. angle_guard and frac_guard are kept small to limit area, and rounding is included because it can improve accuracy at no area cost.
- `pipelined_m` (27 evals): data_width=14..20, n_iter=12..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, m=2..6. *Why:* Pipelined_m registers every m stages, reducing FF count at the cost of a longer combinational path and lower Fmax. It can also shorten latency to ceil(N/m)+2, which helps the burst deadline if Fmax remains high enough. I explore m=2..6 to find the area/latency/Fmax trade-off. The accuracy ranges match pipelined so the merged front compares like-for-like on error.

**Result (code):** 60 evaluations this round, 60 total; 31 feasible; hypervolume 8446 (n/a).

**LLM decision:** `stop` — Final round: the front is feasible and well-covered, so no further exploration is warranted. All three constraints are met by the front: throughput_msps best 273 (>=32, 0% violate), max_abs_err best 1.57e-05 (<=2.44e-04, 2^-15.96), and sys_p99_batch_us best 0.165 (<=0.44). The Pareto front spans luts_plus_ffs 1335..2768 against the HV reference 4000 and accuracy_bits 12.2..16 against the reference 12, i.e. it already covers the objective ranges with 9 feasible designs. The selection rule (min luts_plus_ffs) is satisfied by the pipelined_m [data_width=17 n_iter=17 angle_guard=0 frac_guard=1 trunc m=4] design at luts_plus_ffs=1335, accuracy_bits=12.2, throughput 97.8 MSPS, comfortably inside all constraints. No constraint is unreachable, so infeasible is not appropriate; stopping preserves the mapped front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 8446 (gain this round: n/a (first round)).
Feasible designs: 31 of 60 evaluations (27 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 45% violate; best seen 1.57e-05 (2^-15.96)
- sys_p99_batch_us <= 0.44: 15% violate; best seen 0.165

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=17 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1335, accuracy_bits=12.2, luts=1000, ffs=335, throughput_msps=97.8, max_abs_err=0.000217 (2^-12.17), power_index=1.61
- pipelined_m [data_width=17 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1357, accuracy_bits=12.4, luts=1017, ffs=340, throughput_msps=97.8, max_abs_err=0.00019 (2^-12.36), power_index=1.63
- pipelined_m [data_width=17 n_iter=17 angle_guard=1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1399, accuracy_bits=12.8, luts=1051, ffs=348, throughput_msps=93.6, max_abs_err=0.000144 (2^-12.76), power_index=1.68
- pipelined_m [data_width=19 n_iter=17 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1576, accuracy_bits=14.6, luts=1192, ffs=384, throughput_msps=93.6, max_abs_err=3.97e-05 (2^-14.62), power_index=1.9
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=2326, accuracy_bits=14.7, luts=1170, ffs=1156, throughput_msps=264, max_abs_err=3.84e-05 (2^-14.67), power_index=2.8
- pipelined [data_width=19 n_iter=17 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2403, accuracy_bits=15.1, luts=1209, ffs=1195, throughput_msps=264, max_abs_err=2.76e-05 (2^-15.14), power_index=2.89
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=2473, accuracy_bits=15.4, luts=1244, ffs=1229, throughput_msps=264, max_abs_err=2.32e-05 (2^-15.40), power_index=2.98
- pipelined [data_width=19 n_iter=19 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=2690, accuracy_bits=15.7, luts=1354, ffs=1336, throughput_msps=264, max_abs_err=1.92e-05 (2^-15.67), power_index=3.24
- pipelined [data_width=20 n_iter=19 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=2768, accuracy_bits=16, luts=1394, ffs=1374, throughput_msps=264, max_abs_err=1.57e-05 (2^-15.96), power_index=3.33
Front coverage: luts_plus_ffs 1335..2768 (HV reference 4000); accuracy_bits 12.2..16 (HV reference 12); data_width on the front 17..20 (registry 8..28).

Per family:
- pipelined: 33 evals, 26 feasible; max throughput seen 273 MSPS; best accuracy 15.96 bits; best feasible luts_plus_ffs=1848; feasible ranges: data_width 16..20, n_iter 14..20, angle_guard -1..2, frac_guard 1..2
- pipelined_m: 27 evals, 5 feasible; max throughput seen 171 MSPS; best accuracy 15.12 bits; best feasible luts_plus_ffs=1335; feasible ranges: data_width 17..19, n_iter 17..17, angle_guard 0..1, frac_guard 1..2, m 4..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (18 evals): data_width=16..28, n_iter=15..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)
- `pipelined` (22 evals): data_width=18..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (5 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 57 feasible; hypervolume 1.231e+04 (+45.7%).

**No LLM call** (code's front-mapping round): Final round: the front is feasible and well-covered, so no further exploration is warranted. All three constraints are met by the front: throughput_msps best 273 (>=32, 0% violate), max_abs_err best 1.57e-05 (<=2.44e-04, 2^-15.96), and sys_p99_batch_us best 0.165 (<=0.44). The Pareto front spans luts_plus_ffs 1335..2768 against the HV reference 4000 and accuracy_bits 12.2..16 against the reference 12, i.e. it already covers the objective ranges with 9 feasible designs. The selection rule (min luts_plus_ffs) is satisfied by the pipelined_m [data_width=17 n_iter=17 angle_guard=0 frac_guard=1 trunc m=4] design at luts_plus_ffs=1335, accuracy_bits=12.2, throughput 97.8 MSPS, comfortably inside all constraints. No constraint is unreachable, so infeasible is not appropriate; stopping preserves the mapped front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.231e+04 (gain this round: +45.7%).
Feasible designs: 57 of 100 evaluations (49 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 29% violate; best seen 2.16e-07 (2^-22.14)
- sys_p99_batch_us <= 0.44: 23% violate; best seen 0.165

Pareto front (feasible, 14 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=17 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1335, accuracy_bits=12.2, luts=1000, ffs=335, throughput_msps=97.8, max_abs_err=0.000217 (2^-12.17), power_index=1.61
- pipelined_m [data_width=17 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1357, accuracy_bits=12.4, luts=1017, ffs=340, throughput_msps=97.8, max_abs_err=0.00019 (2^-12.36), power_index=1.63
- pipelined_m [data_width=19 n_iter=17 angle_guard=1 frac_guard=2 rounding=round m=4] luts_plus_ffs=1576, accuracy_bits=14.6, luts=1192, ffs=384, throughput_msps=93.6, max_abs_err=3.97e-05 (2^-14.62), power_index=1.9
- pipelined_m [data_width=25 n_iter=17 angle_guard=3 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1901, accuracy_bits=15.9, luts=1422, ffs=479, throughput_msps=86, max_abs_err=1.58e-05 (2^-15.95), power_index=2.29
- pipelined_m [data_width=25 n_iter=17 angle_guard=4 frac_guard=3 rounding=round m=4] luts_plus_ffs=2103, accuracy_bits=16, luts=1592, ffs=511, throughput_msps=86, max_abs_err=1.53e-05 (2^-15.99), power_index=2.53
- pipelined_m [data_width=26 n_iter=18 angle_guard=3 frac_guard=0 rounding=trunc m=3] luts_plus_ffs=2149, accuracy_bits=17, luts=1564, ffs=585, throughput_msps=110, max_abs_err=7.87e-06 (2^-16.96), power_index=2.59
- pipelined [data_width=28 n_iter=20 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=3643, accuracy_bits=18.9, luts=1807, ffs=1836, throughput_msps=249, max_abs_err=2.03e-06 (2^-18.91), power_index=4.39
- pipelined [data_width=28 n_iter=20 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=3796, accuracy_bits=19, luts=1887, ffs=1909, throughput_msps=249, max_abs_err=1.97e-06 (2^-18.95), power_index=4.57
- pipelined [data_width=28 n_iter=22 angle_guard=0 frac_guard=3 rounding=round] luts_plus_ffs=4332, accuracy_bits=20.8, luts=2189, ffs=2143, throughput_msps=242, max_abs_err=5.43e-07 (2^-20.81), power_index=5.21
- pipelined [data_width=28 n_iter=30 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=5632, accuracy_bits=22.1, luts=2817, ffs=2815, throughput_msps=249, max_abs_err=2.17e-07 (2^-22.13), power_index=6.78
Front coverage: luts_plus_ffs 1335..5632 (HV reference 4000); accuracy_bits 12.2..22.1 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- pipelined: 55 evals, 48 feasible; max throughput seen 273 MSPS; best accuracy 22.13 bits; best feasible luts_plus_ffs=1848; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 45 evals, 9 feasible; max throughput seen 171 MSPS; best accuracy 22.14 bits; best feasible luts_plus_ffs=1335; feasible ranges: data_width 17..26, n_iter 17..18, angle_guard 0..4, frac_guard 0..3, m 3..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5402 in, 3240 out
- provider-reported cost: $0.0044
- full prompts and replies: `llm_trace.jsonl`

