# DSE run: dds_250msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 4 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec dds_250msps: NCO / DDS sin-cos generator for a digital up-converter. One sample per clock at >= 250 MSPS, max error <= 2^-13. Minimise LUTs.
  constraint: throughput_msps >= 250
  constraint: max_abs_err <= 0.00012207
  objective: min luts (HV ref 4000)
  objective: max accuracy_bits (HV ref 13)
  select: min luts
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined:data_width=19,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts)

| metric | value | provenance |
|---|---|---|
| luts | 935 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 969 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 64.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 17.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000108 (2^-13.18) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 14.1 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.75e-05 (2^-15.15) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.6 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.2 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 17 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 100.5 dBc, SNR 88.3 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (27 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=19,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 935 | 969 | 264.5 | 17 | 17.9 | 0.000108 (2^-13.18) | 13.18 |
| 1 | `pipelined:data_width=19,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc` | 964 | 995 | 264.5 | 17 | 18.4 | 0.000101 (2^-13.27) | 13.27 |
| 2 | `pipelined:data_width=19,n_iter=15,angle_guard=3,frac_guard=0,rounding=round` | 979 | 1014 | 264.5 | 17 | 18.7 | 8.25e-05 (2^-13.57) | 13.57 |
| 3 | `pipelined:data_width=19,n_iter=15,angle_guard=1,frac_guard=1,rounding=round` | 1019 | 1012 | 264.5 | 17 | 19.1 | 7.94e-05 (2^-13.62) | 13.62 |
| 4 | `pipelined:data_width=19,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc` | 1033 | 1061 | 264.5 | 18 | 19.7 | 7.43e-05 (2^-13.72) | 13.72 |
| 5 | `pipelined:data_width=19,n_iter=15,angle_guard=3,frac_guard=1,rounding=round` | 1048 | 1042 | 264.5 | 17 | 19.7 | 7.28e-05 (2^-13.75) | 13.75 |
| 6 | `pipelined:data_width=19,n_iter=15,angle_guard=3,frac_guard=3,rounding=trunc` | 1067 | 1093 | 264.5 | 17 | 20.3 | 7.13e-05 (2^-13.78) | 13.78 |
| 7 | `pipelined:data_width=18,n_iter=16,angle_guard=3,frac_guard=1,rounding=round` | 1071 | 1063 | 264.5 | 18 | 20.1 | 6.51e-05 (2^-13.91) | 13.91 |
| 8 | `pipelined:data_width=19,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 1080 | 1106 | 264.5 | 18 | 20.6 | 5.43e-05 (2^-14.17) | 14.17 |
| 9 | `pipelined:data_width=19,n_iter=16,angle_guard=1,frac_guard=1,rounding=round` | 1089 | 1080 | 264.5 | 18 | 20.4 | 5.25e-05 (2^-14.22) | 14.22 |
| 10 | `pipelined:data_width=18,n_iter=16,angle_guard=3,frac_guard=2,rounding=round` | 1102 | 1092 | 264.5 | 18 | 20.6 | 5.17e-05 (2^-14.24) | 14.24 |
| 11 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=3,rounding=round` | 1118 | 1104 | 264.5 | 18 | 20.9 | 5.03e-05 (2^-14.28) | 14.28 |
| 12 | `pipelined:data_width=19,n_iter=16,angle_guard=3,frac_guard=1,rounding=round` | 1120 | 1112 | 264.5 | 18 | 21 | 4.5e-05 (2^-14.44) | 14.44 |
| 13 | `pipelined:data_width=20,n_iter=17,angle_guard=1,frac_guard=0,rounding=round` | 1135 | 1166 | 264.5 | 19 | 21.6 | 3.32e-05 (2^-14.88) | 14.88 |
| 14 | `pipelined:data_width=19,n_iter=17,angle_guard=2,frac_guard=2,rounding=round` | 1209 | 1195 | 264.5 | 19 | 22.6 | 2.76e-05 (2^-15.14) | 15.14 |
| 15 | `pipelined:data_width=20,n_iter=17,angle_guard=2,frac_guard=2,rounding=round` | 1261 | 1246 | 264.5 | 19 | 23.6 | 2.23e-05 (2^-15.45) | 15.45 |
| 16 | `pipelined:data_width=21,n_iter=17,angle_guard=3,frac_guard=2,rounding=trunc` | 1287 | 1313 | 256.5 | 19 | 24.4 | 1.97e-05 (2^-15.63) | 15.63 |
| 17 | `pipelined:data_width=20,n_iter=18,angle_guard=2,frac_guard=2,rounding=round` | 1337 | 1320 | 264.5 | 20 | 25 | 1.51e-05 (2^-16.01) | 16.01 |
| 18 | `pipelined:data_width=22,n_iter=18,angle_guard=3,frac_guard=0,rounding=round` | 1349 | 1380 | 256.5 | 20 | 25.7 | 1.1e-05 (2^-16.47) | 16.47 |
| 19 | `pipelined:data_width=21,n_iter=19,angle_guard=2,frac_guard=3,rounding=trunc` | 1466 | 1483 | 256.5 | 21 | 27.7 | 8.4e-06 (2^-16.86) | 16.86 |
| 20 | `pipelined:data_width=25,n_iter=18,angle_guard=1,frac_guard=0,rounding=round` | 1474 | 1507 | 256.5 | 20 | 28 | 8.18e-06 (2^-16.90) | 16.90 |
| 21 | `pipelined:data_width=21,n_iter=20,angle_guard=1,frac_guard=2,rounding=round` | 1531 | 1507 | 256.5 | 22 | 28.6 | 8.09e-06 (2^-16.91) | 16.91 |
| 22 | `pipelined:data_width=22,n_iter=20,angle_guard=3,frac_guard=1,rounding=round` | 1593 | 1572 | 256.5 | 22 | 29.8 | 4.05e-06 (2^-17.91) | 17.91 |
| 23 | `pipelined:data_width=22,n_iter=20,angle_guard=3,frac_guard=2,rounding=round` | 1633 | 1608 | 256.5 | 22 | 30.5 | 3.33e-06 (2^-18.20) | 18.20 |
| 24 | `pipelined:data_width=23,n_iter=24,angle_guard=2,frac_guard=1,rounding=round` | 1968 | 1935 | 256.5 | 26 | 36.7 | 1.94e-06 (2^-18.98) | 18.98 |
| 25 | `pipelined:data_width=25,n_iter=24,angle_guard=-1,frac_guard=1,rounding=round` | 2045 | 2008 | 256.5 | 26 | 38.1 | 1.85e-06 (2^-19.05) | 19.05 |
| 26 | `pipelined:data_width=25,n_iter=26,angle_guard=1,frac_guard=0,rounding=round` | 2165 | 2177 | 256.5 | 28 | 40.8 | 1.05e-06 (2^-19.86) | 19.86 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The throughput constraint (>=250 MSPS, one sample/clock) rules out iterative and unrolled_k, which emit one result every several cycles and would need Fmax far above 250 MHz to hit 250 MSPS. So I restrict to the two per-cycle families, pipelined and pipelined_m. The accuracy constraint (max_abs_err <= 2^-13) is met by keeping data_width and n_iter modest (12-18 / 10-16) with small angle_guard/frac_guard, which keeps LUTs low for the min-LUTs objective while the upper ends of those ranges map the accuracy_bits objective for hypervolume. I split the budget evenly between the two families: pipelined for the best-Fmax corner and pipelined_m for the area/latency trade-off, together covering the feasible Pareto front. I will let the code report which family actually clears 250 MSPS and refine in later rounds; if neither clears throughput at any point I will declare infeasible rather than relax the constraint.*)
- `pipelined` (50 evals): data_width=12..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* 1 result/cycle is mandatory for >=250 MSPS; full pipeline gives the best Fmax of the per-cycle families, so it is the most likely to clear the throughput constraint while keeping LUTs low. data_width 12-18 and n_iter 10-16 bracket the 2^-13 accuracy requirement (accuracy_bits ~ n_iter + frac_guard + angle_guard, so W=12-14 with N=12-14 should already reach 13 bits, and the upper end maps the accuracy-vs-LUT trade-off for hypervolume). angle_guard 0-2 and frac_guard 0-2 are the cheap knobs that buy accuracy bits without adding full-width datapath LUTs; rounding both to see the trunc/round error difference.
- `pipelined_m` (50 evals): data_width=12..18, n_iter=10..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Also 1 result/cycle, so it meets throughput, but registering every m stages cuts FF count and can relax the per-stage timing (higher Fmax) at the cost of latency. m=2-4 is the sweet spot: m=1 is just pipelined, m>4 adds latency without meaningful area/timing gain. This family often sits on the Pareto front between pipelined (best Fmax) and iterative (lowest area), so it is where the LUT-vs-accuracy trade-off is most interesting for hypervolume.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 6 feasible; hypervolume 1065 (n/a).

**LLM decision:** `refine` — The `pipelined` family is the only one currently yielding feasible designs, with a best LUT count of 964 and throughput of 264 MSPS (meeting the >= 250 MSPS constraint). The `pipelined_m` family failed to meet the throughput constraint (max 178 MSPS), likely due to the reduced clock frequency from fewer pipeline registers or the specific parameter ranges explored. The current feasible region is narrow (data_width 17-18, n_iter 15-16). To maximize hypervolume and find a better trade-off (potentially lower LUTs or higher accuracy), I should focus the search on the `pipelined` family around the known feasible region while allowing slight variations in `angle_guard` and `frac_guard` to see if accuracy can be improved without excessive area cost, or if LUTs can be reduced. I will also include `unrolled_k` in the next round as it might offer a different area/throughput trade-off, but `pipelined` is the primary candidate for the final design given the strict throughput requirement. The `iterative` family is likely too slow for 250 MSPS unless Fmax is very high, which is risky, so I will prioritize `pipelined` and `unrolled_k`.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 1065 (gain this round: n/a (first round)).
Feasible designs: 6 of 100 evaluations (4 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 50% violate; best seen 282
- max_abs_err <= 0.00012207: 93% violate; best seen 9.56e-05 (2^-13.35)

Pareto front (feasible, 2 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts=964, accuracy_bits=13.3, ffs=991, throughput_msps=264, max_abs_err=0.000102 (2^-13.26), power_index=18.4
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=round] luts=1002, accuracy_bits=13.4, ffs=993, throughput_msps=264, max_abs_err=9.56e-05 (2^-13.35), power_index=18.8
Front coverage: luts 964..1002 (HV reference 4000); accuracy_bits 13.3..13.4 (HV reference 13); data_width on the front 18..18 (registry 8..28).

Per family:
- pipelined: 50 evals, 6 feasible; max throughput seen 282 MSPS; best accuracy 13.35 bits; best feasible luts=964; feasible ranges: data_width 17..18, n_iter 15..16, angle_guard 1..2, frac_guard 2..2
- pipelined_m: 50 evals, 0 feasible; max throughput seen 178 MSPS; best accuracy 13.23 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate budget on `pipelined` (proven feasible) and `unrolled_k` (potential alternative). Avoid `iterative` and `pipelined_m` which showed poor throughput or no feasible designs in Round 1.*)
- `pipelined` (70 evals): data_width=16..19, n_iter=14..17, angle_guard=0..3, frac_guard=1..3, rounding=trunc|round. *Why:* Focus on the only family meeting throughput constraints. Expand ranges slightly to explore trade-offs in accuracy and area.
- `unrolled_k` (30 evals): data_width=16..19, n_iter=14..17, angle_guard=0..3, frac_guard=1..3, rounding=trunc|round, k=2..4. *Why:* Explore unrolled_k as a potential alternative for area/throughput trade-off, focusing on higher k to maintain throughput.

**Result (code):** 100 evaluations this round, 200 total; 52 feasible; hypervolume 4947 (+364.3%).

**LLM decision:** `refine` — The current Pareto front is entirely composed of pipelined designs with LUTs ranging from 949 to 1183. The minimum LUT design (949) is at the boundary of the explored parameter space (data_width=18, n_iter=15, angle_guard=2, frac_guard=1). To improve the hypervolume and potentially find a lower-LUT design, we need to explore slightly lower n_iter (14) and lower angle_guard (0-1) while maintaining the accuracy constraint (max_abs_err <= 2^-13). The throughput constraint is tight (best seen 282 MSPS), so we must be careful not to reduce Fmax too much. Additionally, pipelined_m had 0 feasible designs in Round 2, but its max throughput (178 MSPS) suggests that with the right m value (2-4) and n_iter (14-17), it might be possible to achieve throughput >= 250 MSPS with fewer pipeline registers (and thus lower LUTs) than the fully pipelined design. We allocate 60% of the budget to refining the pipelined family around the current front and 40% to exploring pipelined_m with m=2-4 to see if it can produce feasible designs with lower LUTs.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 4947 (gain this round: +364.3%).
Feasible designs: 52 of 200 evaluations (31 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 40% violate; best seen 282
- max_abs_err <= 0.00012207: 66% violate; best seen 3.8e-05 (2^-14.68)

Pareto front (feasible, 15 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=trunc] luts=949, accuracy_bits=13.1, ffs=980, throughput_msps=264, max_abs_err=0.000118 (2^-13.05), power_index=18.1
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] luts=979, accuracy_bits=13.4, ffs=1006, throughput_msps=264, max_abs_err=9.49e-05 (2^-13.36), power_index=18.7
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] luts=987, accuracy_bits=13.4, ffs=982, throughput_msps=264, max_abs_err=9.31e-05 (2^-13.39), power_index=18.5
- pipelined [data_width=18 n_iter=15 angle_guard=3 frac_guard=3 rounding=trunc] luts=1023, accuracy_bits=13.5, ffs=1047, throughput_msps=264, max_abs_err=8.39e-05 (2^-13.54), power_index=19.5
- pipelined [data_width=18 n_iter=15 angle_guard=3 frac_guard=2 rounding=round] luts=1032, accuracy_bits=13.6, ffs=1023, throughput_msps=264, max_abs_err=8.22e-05 (2^-13.57), power_index=19.3
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=1 rounding=round] luts=1071, accuracy_bits=13.9, ffs=1063, throughput_msps=264, max_abs_err=6.51e-05 (2^-13.91), power_index=20.1
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts=1080, accuracy_bits=14.2, ffs=1106, throughput_msps=264, max_abs_err=5.43e-05 (2^-14.17), power_index=20.6
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] luts=1102, accuracy_bits=14.2, ffs=1092, throughput_msps=264, max_abs_err=5.17e-05 (2^-14.24), power_index=20.6
- pipelined [data_width=19 n_iter=16 angle_guard=3 frac_guard=1 rounding=round] luts=1120, accuracy_bits=14.4, ffs=1112, throughput_msps=264, max_abs_err=4.5e-05 (2^-14.44), power_index=21
- pipelined [data_width=19 n_iter=16 angle_guard=3 frac_guard=3 rounding=round] luts=1183, accuracy_bits=14.7, ffs=1168, throughput_msps=264, max_abs_err=3.8e-05 (2^-14.68), power_index=22.1
Front coverage: luts 949..1183 (HV reference 4000); accuracy_bits 13.1..14.7 (HV reference 13); data_width on the front 18..19 (registry 8..28).

Per family:
- unrolled_k: 30 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 14.43 bits
- pipelined: 120 evals, 52 feasible; max throughput seen 282 MSPS; best accuracy 14.68 bits; best feasible luts=949; feasible ranges: data_width 16..19, n_iter 15..17, angle_guard 0..3, frac_guard 1..3
- pipelined_m: 50 evals, 0 feasible; max throughput seen 178 MSPS; best accuracy 13.23 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The current Pareto front is entirely composed of pipelined designs with LUTs ranging from 949 to 1183. The minimum LUT design (949) is at the boundary of the explored parameter space (data_width=18, n_iter=15, angle_guard=2, frac_guard=1). To improve the hypervolume and potentially find a lower-LUT design, we need to explore slightly lower n_iter (14) and lower angle_guard (0-1) while maintaining the accuracy constraint (max_abs_err <= 2^-13). The throughput constraint is tight (best seen 282 MSPS), so we must be careful not to reduce Fmax too much. Additionally, pipelined_m had 0 feasible designs in Round 2, but its max throughput (178 MSPS) suggests that with the right m value (2-4) and n_iter (14-17), it might be possible to achieve throughput >= 250 MSPS with fewer pipeline registers (and thus lower LUTs) than the fully pipelined design. We allocate 60% of the budget to refining the pipelined family around the current front and 40% to exploring pipelined_m with m=2-4 to see if it can produce feasible designs with lower LUTs.*)
- `pipelined` (24 evals): data_width=17..19, n_iter=14..17, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* All 15 Pareto-optimal designs are pipelined with data_width 18-19, n_iter 15-16, angle_guard 2-3, frac_guard 1-3. The minimum LUT design (949) sits at the edge of the explored range (data_width=18, n_iter=15, angle_guard=2, frac_guard=1). We need to probe slightly lower n_iter (14) and lower angle_guard (0-1) to see if we can push LUTs below 949 while maintaining throughput >= 250 MSPS and max_abs_err <= 2^-13. The throughput constraint is tight (best seen 282 MSPS, only 12% margin), so we must be careful not to drop Fmax too much by reducing n_iter or data_width.
- `pipelined_m` (16 evals): data_width=17..19, n_iter=14..17, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, m=2..4. *Why:* pipelined_m had 0 feasible designs in Round 2, but its max throughput was 178 MSPS, which is below the 250 MSPS constraint. However, the throughput of pipelined_m depends on Fmax and the pipeline depth (ceil(N/m)+2). With m=2-4 and n_iter=14-17, the pipeline depth is 5-9 stages, which should give a higher Fmax than the fully pipelined version (15-17 stages). The previous 50 evals may have sampled m values that resulted in too many stages or too low Fmax. Let's try m=2-4 with the same accuracy parameters as the pipelined front to see if we can get feasible designs with potentially lower LUTs (fewer pipeline registers).

**Result (code):** 40 evaluations this round, 240 total; 68 feasible; hypervolume 4956 (+0.2%).

**LLM decision:** `stop` — The `pipelined` family has successfully mapped a robust feasible Pareto front that satisfies all constraints (throughput >= 250 MSPS, max_abs_err <= 2^-13). The front spans a wide range of accuracy (13.2 to 14.7 bits) and area (935 to 1183 LUTs), with the minimum LUT design at 935 LUTs meeting the 250 MSPS requirement (264 MSPS). Other families (`unrolled_k`, `pipelined_m`) failed to meet the throughput constraint, and `iterative` is inherently too slow for 250 MSPS. The hypervolume gain in the last round was negligible (+0.2%), indicating the front is well-characterized. Since this is the final round, we stop and select the design with minimum LUTs from the front.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 4956 (gain this round: +0.2%).
Feasible designs: 68 of 240 evaluations (39 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 40% violate; best seen 282
- max_abs_err <= 0.00012207: 61% violate; best seen 3.42e-05 (2^-14.83)

Pareto front (feasible, 17 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=19 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts=935, accuracy_bits=13.2, ffs=969, throughput_msps=264, max_abs_err=0.000108 (2^-13.18), power_index=17.9
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] luts=979, accuracy_bits=13.4, ffs=1006, throughput_msps=264, max_abs_err=9.49e-05 (2^-13.36), power_index=18.7
- pipelined [data_width=18 n_iter=15 angle_guard=3 frac_guard=1 rounding=round] luts=1002, accuracy_bits=13.4, ffs=997, throughput_msps=264, max_abs_err=8.97e-05 (2^-13.44), power_index=18.8
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] luts=1019, accuracy_bits=13.6, ffs=1012, throughput_msps=264, max_abs_err=7.94e-05 (2^-13.62), power_index=19.1
- pipelined [data_width=19 n_iter=15 angle_guard=3 frac_guard=1 rounding=round] luts=1048, accuracy_bits=13.7, ffs=1042, throughput_msps=264, max_abs_err=7.28e-05 (2^-13.75), power_index=19.7
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=1 rounding=round] luts=1071, accuracy_bits=13.9, ffs=1063, throughput_msps=264, max_abs_err=6.51e-05 (2^-13.91), power_index=20.1
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts=1089, accuracy_bits=14.2, ffs=1080, throughput_msps=264, max_abs_err=5.25e-05 (2^-14.22), power_index=20.4
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] luts=1102, accuracy_bits=14.2, ffs=1092, throughput_msps=264, max_abs_err=5.17e-05 (2^-14.24), power_index=20.6
- pipelined [data_width=19 n_iter=16 angle_guard=3 frac_guard=1 rounding=round] luts=1120, accuracy_bits=14.4, ffs=1112, throughput_msps=264, max_abs_err=4.5e-05 (2^-14.44), power_index=21
- pipelined [data_width=19 n_iter=16 angle_guard=3 frac_guard=3 rounding=round] luts=1183, accuracy_bits=14.7, ffs=1168, throughput_msps=264, max_abs_err=3.8e-05 (2^-14.68), power_index=22.1
Front coverage: luts 935..1183 (HV reference 4000); accuracy_bits 13.2..14.7 (HV reference 13); data_width on the front 18..19 (registry 8..28).

Per family:
- unrolled_k: 30 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 14.43 bits
- pipelined: 144 evals, 68 feasible; max throughput seen 282 MSPS; best accuracy 14.68 bits; best feasible luts=935; feasible ranges: data_width 16..19, n_iter 15..17, angle_guard 0..3, frac_guard 0..3
- pipelined_m: 66 evals, 0 feasible; max throughput seen 178 MSPS; best accuracy 14.83 bits
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined` (160 evals): data_width=17..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (17 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 170 feasible; hypervolume 1.724e+04 (+247.8%).

**No LLM call** (code's front-mapping round): The `pipelined` family has successfully mapped a robust feasible Pareto front that satisfies all constraints (throughput >= 250 MSPS, max_abs_err <= 2^-13). The front spans a wide range of accuracy (13.2 to 14.7 bits) and area (935 to 1183 LUTs), with the minimum LUT design at 935 LUTs meeting the 250 MSPS requirement (264 MSPS). Other families (`unrolled_k`, `pipelined_m`) failed to meet the throughput constraint, and `iterative` is inherently too slow for 250 MSPS. The hypervolume gain in the last round was negligible (+0.2%), indicating the front is well-characterized. Since this is the final round, we stop and select the design with minimum LUTs from the front.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.724e+04 (gain this round: +247.8%).
Feasible designs: 170 of 400 evaluations (130 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 34% violate; best seen 282
- max_abs_err <= 0.00012207: 42% violate; best seen 8.54e-08 (2^-23.48)

Pareto front (feasible, 27 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=19 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts=935, accuracy_bits=13.2, ffs=969, throughput_msps=264, max_abs_err=0.000108 (2^-13.18), power_index=17.9
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] luts=1019, accuracy_bits=13.6, ffs=1012, throughput_msps=264, max_abs_err=7.94e-05 (2^-13.62), power_index=19.1
- pipelined [data_width=19 n_iter=15 angle_guard=3 frac_guard=3 rounding=trunc] luts=1067, accuracy_bits=13.8, ffs=1093, throughput_msps=264, max_abs_err=7.13e-05 (2^-13.78), power_index=20.3
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts=1089, accuracy_bits=14.2, ffs=1080, throughput_msps=264, max_abs_err=5.25e-05 (2^-14.22), power_index=20.4
- pipelined [data_width=19 n_iter=16 angle_guard=3 frac_guard=1 rounding=round] luts=1120, accuracy_bits=14.4, ffs=1112, throughput_msps=264, max_abs_err=4.5e-05 (2^-14.44), power_index=21
- pipelined [data_width=19 n_iter=17 angle_guard=2 frac_guard=2 rounding=round] luts=1209, accuracy_bits=15.1, ffs=1195, throughput_msps=264, max_abs_err=2.76e-05 (2^-15.14), power_index=22.6
- pipelined [data_width=20 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] luts=1337, accuracy_bits=16, ffs=1320, throughput_msps=264, max_abs_err=1.51e-05 (2^-16.01), power_index=25
- pipelined [data_width=25 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] luts=1474, accuracy_bits=16.9, ffs=1507, throughput_msps=257, max_abs_err=8.18e-06 (2^-16.90), power_index=28
- pipelined [data_width=22 n_iter=20 angle_guard=3 frac_guard=2 rounding=round] luts=1633, accuracy_bits=18.2, ffs=1608, throughput_msps=257, max_abs_err=3.33e-06 (2^-18.20), power_index=30.5
- pipelined [data_width=25 n_iter=26 angle_guard=1 frac_guard=0 rounding=round] luts=2165, accuracy_bits=19.9, ffs=2177, throughput_msps=257, max_abs_err=1.05e-06 (2^-19.86), power_index=40.8
Front coverage: luts 935..2165 (HV reference 4000); accuracy_bits 13.2..19.9 (HV reference 13); data_width on the front 18..25 (registry 8..28).

Per family:
- unrolled_k: 30 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 14.43 bits
- pipelined: 304 evals, 170 feasible; max throughput seen 282 MSPS; best accuracy 23.48 bits; best feasible luts=935; feasible ranges: data_width 16..25, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 66 evals, 0 feasible; max throughput seen 178 MSPS; best accuracy 14.83 bits
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 23268 in, 4073 out
- provider-reported cost: $0.0093
- full prompts and replies: `llm_trace.jsonl`

