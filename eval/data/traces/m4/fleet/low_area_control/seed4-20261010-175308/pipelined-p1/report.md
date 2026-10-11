# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec low_area_control: Field-oriented motor-control loop needing sin/cos of the rotor angle at >= 1 MSPS with max error <= 2^-10. Area is everything: minimise LUTs + FFs.
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min luts_plus_ffs (HV ref 1500)
  objective: max accuracy_bits (HV ref 10)
  select: min luts_plus_ffs
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=15,n_iter=14,angle_guard=2,frac_guard=3,rounding=trunc,m=8` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 813 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 145 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 52.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 52.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 4 | exact: schedule |
| latency_ns | 75.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.0361 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000359 (2^-11.44) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 2.94 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 9.21e-05 (2^-13.41) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 0.754 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 11.4 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (14 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=15,n_iter=14,angle_guard=2,frac_guard=3,rounding=trunc,m=8` | 813 | 145 | 52.7 | 4 | 0.0361 | 0.000359 (2^-11.44) | 11.44 |
| 1 | `pipelined_m:data_width=16,n_iter=14,angle_guard=4,frac_guard=3,rounding=trunc,m=8` | 882 | 157 | 50.3 | 4 | 0.0391 | 0.000208 (2^-12.23) | 12.23 |
| 2 | `pipelined_m:data_width=20,n_iter=20,angle_guard=-2,frac_guard=2,rounding=trunc,m=6` | 1367 | 315 | 65.4 | 6 | 0.0633 | 9.69e-05 (2^-13.33) | 13.33 |
| 3 | `pipelined:data_width=16,n_iter=16,angle_guard=3,frac_guard=4,rounding=round` | 1066 | 1051 | 264.5 | 18 | 0.0797 | 9.1e-05 (2^-13.42) | 13.42 |
| 4 | `pipelined_m:data_width=20,n_iter=28,angle_guard=2,frac_guard=0,rounding=round,m=7` | 1940 | 319 | 56.8 | 6 | 0.085 | 2.17e-05 (2^-15.49) | 15.49 |
| 5 | `pipelined_m:data_width=28,n_iter=17,angle_guard=3,frac_guard=3,rounding=round,m=3` | 1733 | 658 | 105.9 | 8 | 0.0899 | 1.53e-05 (2^-16.00) | 16.00 |
| 6 | `pipelined_m:data_width=24,n_iter=28,angle_guard=-2,frac_guard=1,rounding=trunc,m=7` | 2224 | 365 | 54.3 | 6 | 0.0974 | 7.66e-06 (2^-16.99) | 16.99 |
| 7 | `pipelined_m:data_width=24,n_iter=27,angle_guard=-2,frac_guard=0,rounding=round,m=3` | 2087 | 748 | 114.5 | 11 | 0.107 | 6.97e-06 (2^-17.13) | 17.13 |
| 8 | `pipelined:data_width=22,n_iter=25,angle_guard=1,frac_guard=3,rounding=trunc` | 2003 | 2006 | 256.5 | 27 | 0.151 | 4.19e-06 (2^-17.86) | 17.86 |
| 9 | `pipelined:data_width=27,n_iter=24,angle_guard=1,frac_guard=0,rounding=trunc` | 2138 | 2155 | 249.0 | 26 | 0.161 | 4.31e-07 (2^-21.14) | 21.14 |
| 10 | `pipelined:data_width=27,n_iter=24,angle_guard=4,frac_guard=0,rounding=round` | 2211 | 2228 | 242.0 | 26 | 0.167 | 2.65e-07 (2^-21.85) | 21.85 |
| 11 | `pipelined:data_width=28,n_iter=25,angle_guard=-1,frac_guard=3,rounding=trunc` | 2408 | 2409 | 242.0 | 27 | 0.181 | 2.56e-07 (2^-21.90) | 21.90 |
| 12 | `pipelined:data_width=28,n_iter=25,angle_guard=1,frac_guard=3,rounding=trunc` | 2458 | 2460 | 242.0 | 27 | 0.185 | 1.15e-07 (2^-23.05) | 23.05 |
| 13 | `pipelined:data_width=28,n_iter=25,angle_guard=3,frac_guard=3,rounding=round` | 2568 | 2512 | 242.0 | 27 | 0.191 | 7.81e-08 (2^-23.61) | 23.61 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Both pipelined and pipelined_m produce 1 result per cycle, so throughput_msps = Fmax/1000. The constraint requires >=1 MSPS, i.e. Fmax >= 1000 MHz. Artix-7 FPGAs typically max out around 200-400 MHz depending on the part and design complexity. Even with aggressive pipelining (m=8), the per-cycle logic depth for 8 CORDIC micro-rotations is substantial and unlikely to reach 1 GHz. Therefore, both families are likely infeasible for the throughput constraint. I allocate 60% to pipelined and 40% to pipelined_m to let code confirm this. The accuracy constraint (max_abs_err <= 2^-10) is easily satisfied with N>=12 and W>=12, so I narrow n_iter and data_width to 12-16 to focus the search on the area/accuracy trade-off within the feasible accuracy region. If both families are confirmed infeasible for throughput, the fleet will need to rely on iterative or unrolled_k (handled by other architects) to meet the spec, since those families produce one result every several cycles and can achieve higher Fmax per cycle, but their throughput will be Fmax/(cycles_per_result), which also needs to be >=1 MSPS. For example, iterative with N=12 needs 15 cycles/result, so Fmax >= 1500 MHz is needed, which is also impossible. unrolled_k with k=8 and N=12 needs ceil(12/8)+3 = 5 cycles/result, so Fmax >= 500 MHz, which is more plausible. This suggests the spec may be infeasible for all families, but that determination is for the fleet to make. My job is to map the front for my assigned families as best as possible.*)
- `pipelined` (36 evals): data_width=12..16, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* pipelined gives 1 result/cycle, so throughput_msps = Fmax/1000. To clear >=1 MSPS we need Fmax >= 1000 MHz, which is impossible on Artix-7. Therefore pipelined cannot meet the throughput constraint at any parameter setting. I include it with a small share only to let code confirm infeasibility and populate the front with its best-area points for the accuracy objective, but I expect it to be cut by the throughput constraint.
- `pipelined_m` (24 evals): data_width=12..16, n_iter=12..16, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* pipelined_m also produces 1 result/cycle, so it faces the same Fmax >= 1000 MHz problem as pipelined. However, by registering every m stages (m=2..8), the combinational depth per cycle is reduced, which may push Fmax higher than the fully-pipelined case. With m=8 and N=12, each stage does 8 micro-rotations of logic; this is still deep. I search the full m range to let code determine whether any (m, n_iter, data_width) combination can reach >=1000 MHz. If not, this family is also infeasible for throughput. The accuracy constraint (max_abs_err <= 2^-10) is easily met with N>=12 and W>=12, so accuracy is not the binding constraint here; throughput is. I focus n_iter and data_width in the 12-16 range because lower values risk missing the accuracy target while higher values increase area without helping throughput.

**Result (code):** 60 evaluations this round, 60 total; 44 feasible; hypervolume 1144 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (pipelined_m, luts_plus_ffs=959) meets the throughput constraint (52.7 MSPS >= 1) and accuracy constraint (11.4 bits >= 10 bits). The front covers a reasonable range of the trade-off space (luts_plus_ffs 959-2118, accuracy_bits 11.4-13.4). Since this is the final round, we stop and select the design with minimum luts_plus_ffs from the front, which is the pipelined_m design with luts_plus_ffs=959.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1144 (gain this round: n/a (first round)).
Feasible designs: 44 of 60 evaluations (37 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 27% violate; best seen 9.1e-05 (2^-13.42)

Pareto front (feasible, 10 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=2 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=959, accuracy_bits=11.4, luts=813, ffs=145, throughput_msps=52.7, max_abs_err=0.000359 (2^-11.44), power_index=0.0361
- pipelined_m [data_width=16 n_iter=14 angle_guard=4 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1039, accuracy_bits=12.2, luts=882, ffs=157, throughput_msps=50.3, max_abs_err=0.000208 (2^-12.23), power_index=0.0391
- pipelined [data_width=16 n_iter=14 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=1744, accuracy_bits=12.4, luts=875, ffs=870, throughput_msps=264, max_abs_err=0.000189 (2^-12.37), power_index=0.0656
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=3 rounding=round] luts_plus_ffs=1768, accuracy_bits=12.4, luts=888, ffs=880, throughput_msps=264, max_abs_err=0.000187 (2^-12.38), power_index=0.0665
- pipelined [data_width=16 n_iter=14 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=1796, accuracy_bits=12.5, luts=902, ffs=894, throughput_msps=264, max_abs_err=0.000171 (2^-12.51), power_index=0.0676
- pipelined [data_width=16 n_iter=14 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=1848, accuracy_bits=12.5, luts=929, ffs=918, throughput_msps=264, max_abs_err=0.00017 (2^-12.52), power_index=0.0695
- pipelined [data_width=16 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=1871, accuracy_bits=12.9, luts=939, ffs=932, throughput_msps=264, max_abs_err=0.000128 (2^-12.93), power_index=0.0704
- pipelined [data_width=16 n_iter=15 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=1927, accuracy_bits=13.1, luts=968, ffs=958, throughput_msps=264, max_abs_err=0.000117 (2^-13.06), power_index=0.0725
- pipelined [data_width=16 n_iter=15 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=1983, accuracy_bits=13.2, luts=998, ffs=985, throughput_msps=264, max_abs_err=0.000109 (2^-13.16), power_index=0.0746
- pipelined [data_width=16 n_iter=16 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=2118, accuracy_bits=13.4, luts=1066, ffs=1051, throughput_msps=264, max_abs_err=9.1e-05 (2^-13.42), power_index=0.0797
Front coverage: luts_plus_ffs 959..2118 (HV reference 1500); accuracy_bits 11.4..13.4 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- pipelined: 36 evals, 28 feasible; max throughput seen 282 MSPS; best accuracy 13.42 bits; best feasible luts_plus_ffs=1273; feasible ranges: data_width 12..16, n_iter 12..16, angle_guard 0..4, frac_guard 0..4
- pipelined_m: 24 evals, 16 feasible; max throughput seen 171 MSPS; best accuracy 12.23 bits; best feasible luts_plus_ffs=959; feasible ranges: data_width 13..16, n_iter 14..16, angle_guard -1..4, frac_guard 2..4, m 2..8
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (8 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (2 front designs; box front_anchored)
- `pipelined` (32 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (8 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 83 feasible; hypervolume 1144 (+0.0%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and satisfies all constraints. The minimum area design (pipelined_m, luts_plus_ffs=959) meets the throughput constraint (52.7 MSPS >= 1) and accuracy constraint (11.4 bits >= 10 bits). The front covers a reasonable range of the trade-off space (luts_plus_ffs 959-2118, accuracy_bits 11.4-13.4). Since this is the final round, we stop and select the design with minimum luts_plus_ffs from the front, which is the pipelined_m design with luts_plus_ffs=959.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1144 (gain this round: +0.0%).
Feasible designs: 83 of 100 evaluations (73 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 282
- max_abs_err <= 0.000976562: 17% violate; best seen 7.81e-08 (2^-23.61)

Pareto front (feasible, 14 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=15 n_iter=14 angle_guard=2 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=959, accuracy_bits=11.4, luts=813, ffs=145, throughput_msps=52.7, max_abs_err=0.000359 (2^-11.44), power_index=0.0361
- pipelined_m [data_width=16 n_iter=14 angle_guard=4 frac_guard=3 rounding=trunc m=8] luts_plus_ffs=1039, accuracy_bits=12.2, luts=882, ffs=157, throughput_msps=50.3, max_abs_err=0.000208 (2^-12.23), power_index=0.0391
- pipelined [data_width=16 n_iter=16 angle_guard=3 frac_guard=4 rounding=round] luts_plus_ffs=2118, accuracy_bits=13.4, luts=1066, ffs=1051, throughput_msps=264, max_abs_err=9.1e-05 (2^-13.42), power_index=0.0797
- pipelined_m [data_width=20 n_iter=28 angle_guard=2 frac_guard=0 rounding=round m=7] luts_plus_ffs=2259, accuracy_bits=15.5, luts=1940, ffs=319, throughput_msps=56.8, max_abs_err=2.17e-05 (2^-15.49), power_index=0.085
- pipelined_m [data_width=24 n_iter=28 angle_guard=-2 frac_guard=1 rounding=trunc m=7] luts_plus_ffs=2590, accuracy_bits=17, luts=2224, ffs=365, throughput_msps=54.3, max_abs_err=7.66e-06 (2^-16.99), power_index=0.0974
- pipelined_m [data_width=24 n_iter=27 angle_guard=-2 frac_guard=0 rounding=round m=3] luts_plus_ffs=2835, accuracy_bits=17.1, luts=2087, ffs=748, throughput_msps=114, max_abs_err=6.97e-06 (2^-17.13), power_index=0.107
- pipelined [data_width=27 n_iter=24 angle_guard=1 frac_guard=0 rounding=trunc] luts_plus_ffs=4293, accuracy_bits=21.1, luts=2138, ffs=2155, throughput_msps=249, max_abs_err=4.31e-07 (2^-21.14), power_index=0.161
- pipelined [data_width=27 n_iter=24 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=4438, accuracy_bits=21.8, luts=2211, ffs=2228, throughput_msps=242, max_abs_err=2.65e-07 (2^-21.85), power_index=0.167
- pipelined [data_width=28 n_iter=25 angle_guard=1 frac_guard=3 rounding=trunc] luts_plus_ffs=4918, accuracy_bits=23, luts=2458, ffs=2460, throughput_msps=242, max_abs_err=1.15e-07 (2^-23.05), power_index=0.185
- pipelined [data_width=28 n_iter=25 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=5080, accuracy_bits=23.6, luts=2568, ffs=2512, throughput_msps=242, max_abs_err=7.81e-08 (2^-23.61), power_index=0.191
Front coverage: luts_plus_ffs 959..5080 (HV reference 1500); accuracy_bits 11.4..23.6 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- pipelined: 68 evals, 60 feasible; max throughput seen 282 MSPS; best accuracy 23.61 bits; best feasible luts_plus_ffs=1273; feasible ranges: data_width 12..28, n_iter 12..27, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 32 evals, 23 feasible; max throughput seen 171 MSPS; best accuracy 17.13 bits; best feasible luts_plus_ffs=959; feasible ranges: data_width 13..28, n_iter 13..28, angle_guard -2..4, frac_guard 0..4, m 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4623 in, 1420 out
- provider-reported cost: $0.0023
- full prompts and replies: `llm_trace.jsonl`

