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

## Pareto front (26 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=19,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 935 | 969 | 264.5 | 17 | 17.9 | 0.000108 (2^-13.18) | 13.18 |
| 1 | `pipelined:data_width=19,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 964 | 999 | 264.5 | 17 | 18.5 | 8.33e-05 (2^-13.55) | 13.55 |
| 2 | `pipelined:data_width=19,n_iter=15,angle_guard=1,frac_guard=2,rounding=trunc` | 1008 | 1036 | 264.5 | 17 | 19.2 | 8.04e-05 (2^-13.60) | 13.60 |
| 3 | `pipelined:data_width=19,n_iter=15,angle_guard=1,frac_guard=1,rounding=round` | 1019 | 1012 | 264.5 | 17 | 19.1 | 7.94e-05 (2^-13.62) | 13.62 |
| 4 | `pipelined:data_width=19,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 1033 | 1065 | 264.5 | 18 | 19.7 | 5.75e-05 (2^-14.09) | 14.09 |
| 5 | `pipelined:data_width=19,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc` | 1080 | 1106 | 264.5 | 18 | 20.6 | 5.43e-05 (2^-14.17) | 14.17 |
| 6 | `pipelined:data_width=19,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 1096 | 1122 | 264.5 | 18 | 20.9 | 4.81e-05 (2^-14.34) | 14.34 |
| 7 | `pipelined:data_width=19,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 1136 | 1124 | 264.5 | 18 | 21.3 | 4.29e-05 (2^-14.51) | 14.51 |
| 8 | `pipelined:data_width=19,n_iter=18,angle_guard=1,frac_guard=0,rounding=round` | 1152 | 1180 | 264.5 | 20 | 21.9 | 4.26e-05 (2^-14.52) | 14.52 |
| 9 | `pipelined:data_width=20,n_iter=16,angle_guard=2,frac_guard=1,rounding=round` | 1154 | 1144 | 264.5 | 18 | 21.6 | 3.91e-05 (2^-14.64) | 14.64 |
| 10 | `pipelined:data_width=19,n_iter=18,angle_guard=2,frac_guard=0,rounding=round` | 1170 | 1199 | 264.5 | 20 | 22.3 | 3.86e-05 (2^-14.66) | 14.66 |
| 11 | `pipelined:data_width=19,n_iter=17,angle_guard=2,frac_guard=2,rounding=round` | 1209 | 1195 | 264.5 | 19 | 22.6 | 2.76e-05 (2^-15.14) | 15.14 |
| 12 | `pipelined:data_width=20,n_iter=19,angle_guard=1,frac_guard=0,rounding=round` | 1276 | 1304 | 264.5 | 21 | 24.3 | 2.52e-05 (2^-15.28) | 15.28 |
| 13 | `pipelined:data_width=19,n_iter=18,angle_guard=2,frac_guard=2,rounding=round` | 1281 | 1265 | 264.5 | 20 | 23.9 | 2.34e-05 (2^-15.38) | 15.38 |
| 14 | `pipelined:data_width=20,n_iter=18,angle_guard=1,frac_guard=4,rounding=trunc` | 1349 | 1364 | 256.5 | 20 | 25.5 | 2.09e-05 (2^-15.55) | 15.55 |
| 15 | `pipelined:data_width=19,n_iter=19,angle_guard=2,frac_guard=2,rounding=round` | 1354 | 1336 | 264.5 | 21 | 25.3 | 1.92e-05 (2^-15.67) | 15.67 |
| 16 | `pipelined:data_width=20,n_iter=19,angle_guard=1,frac_guard=1,rounding=round` | 1356 | 1340 | 264.5 | 21 | 25.4 | 1.9e-05 (2^-15.68) | 15.68 |
| 17 | `pipelined:data_width=23,n_iter=19,angle_guard=-2,frac_guard=0,rounding=trunc` | 1390 | 1419 | 256.5 | 21 | 26.4 | 1.46e-05 (2^-16.06) | 16.06 |
| 18 | `pipelined:data_width=24,n_iter=18,angle_guard=2,frac_guard=0,rounding=trunc` | 1438 | 1471 | 256.5 | 20 | 27.4 | 9.16e-06 (2^-16.74) | 16.74 |
| 19 | `pipelined:data_width=26,n_iter=18,angle_guard=0,frac_guard=0,rounding=round` | 1510 | 1544 | 256.5 | 20 | 28.7 | 7.95e-06 (2^-16.94) | 16.94 |
| 20 | `pipelined:data_width=22,n_iter=19,angle_guard=2,frac_guard=3,rounding=trunc` | 1523 | 1541 | 256.5 | 21 | 28.8 | 6.24e-06 (2^-17.29) | 17.29 |
| 21 | `pipelined:data_width=25,n_iter=19,angle_guard=1,frac_guard=0,rounding=trunc` | 1561 | 1591 | 256.5 | 21 | 29.6 | 4.66e-06 (2^-17.71) | 17.71 |
| 22 | `pipelined:data_width=23,n_iter=19,angle_guard=3,frac_guard=3,rounding=trunc` | 1599 | 1617 | 256.5 | 21 | 30.2 | 4.49e-06 (2^-17.76) | 17.76 |
| 23 | `pipelined:data_width=23,n_iter=24,angle_guard=2,frac_guard=0,rounding=round` | 1871 | 1889 | 256.5 | 26 | 35.4 | 2.9e-06 (2^-18.39) | 18.39 |
| 24 | `pipelined:data_width=23,n_iter=24,angle_guard=1,frac_guard=2,rounding=round` | 1993 | 1955 | 256.5 | 26 | 37.1 | 2.3e-06 (2^-18.73) | 18.73 |
| 25 | `pipelined:data_width=26,n_iter=24,angle_guard=0,frac_guard=0,rounding=round` | 2041 | 2058 | 256.5 | 26 | 38.5 | 6.15e-07 (2^-20.63) | 20.63 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=250 MSPS throughput and max_abs_err <= 2^-13. The iterative family is far too slow (1 result per N+3 cycles) and is excluded. The key challenge is achieving 250 MSPS: pipelined_m with large m (4-8) reduces register count and relaxes timing, making it the primary candidate. pipelined (m=1) is a fallback with maximum timing margin but higher FF count. unrolled_k with large k is a small area check. Accuracy is controlled by n_iter and data_width; ranges are set to cover the 2^-13 error bound while exploring the LUT/accuracy trade-off. Budget is weighted toward pipelined_m (60%) as the most promising family, with pipelined (30%) as fallback and unrolled_k (10%) for area comparison.*)
- `pipelined_m` (60 evals): data_width=14..20, n_iter=12..20, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=4..8. *Why:* Only family that can plausibly hit >=250 MSPS with 1 result/cycle. Larger m (4-8) reduces FF count and relaxes timing to push Fmax higher, directly addressing the throughput constraint. n_iter 12-20 and data_width 14-20 cover the accuracy trade-off needed for max_abs_err <= 2^-13 while keeping LUTs low.
- `pipelined` (30 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Full pipelined (m=1) gives the highest Fmax potential since every stage is registered, which may be needed to reach 250 MSPS if pipelined_m with large m cannot close timing. Slightly narrower ranges since it is a fallback; if it cannot beat pipelined_m on LUTs at equal throughput, it will not be on the front.
- `unrolled_k` (10 evals): data_width=14..18, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=4..8. *Why:* Small check for area: unrolled_k with large k (4-8) has fewer FFs than pipelined_m and may have lower LUT count due to shared datapath. Throughput is Fmax * k / ceil(N/k), so with k=8 and N=12, it produces 1 result every 2 cycles at Fmax. If Fmax is high enough (>=500 MHz), it could meet 250 MSPS. Worth a small budget slice to confirm or rule out.

**Result (code):** 100 evaluations this round, 100 total; 2 feasible; hypervolume 1137 (n/a).

**LLM decision:** `refine` — Evidence shows only the `pipelined` family can meet the throughput constraint (>=250 MSPS). `unrolled_k` and `pipelined_m` are infeasible due to throughput limits (max 10.3 and 97.8 MSPS respectively). The 2 feasible designs found in Round 1 are both `pipelined` with data_width 17-18 and n_iter 16-18. The best LUT count is 1023. To minimize LUTs (the selection rule) and improve hypervolume, I should focus the remaining budget on refining the `pipelined` family within the narrow range where feasibility was observed. I will slightly widen the ranges to ensure we don't miss a better corner (e.g., data_width 16, n_iter 14) but keep it tight to maximize the number of evaluations in the promising region.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 1137 (gain this round: n/a (first round)).
Feasible designs: 2 of 100 evaluations (2 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 70% violate; best seen 273
- max_abs_err <= 0.00012207: 63% violate; best seen 2.28e-05 (2^-15.42)

Pareto front (feasible, 2 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=16 angle_guard=0 frac_guard=1 rounding=round] luts=1023, accuracy_bits=13, ffs=1015, throughput_msps=264, max_abs_err=0.00012 (2^-13.03), power_index=19.2
- pipelined [data_width=17 n_iter=18 angle_guard=2 frac_guard=1 rounding=round] luts=1134, accuracy_bits=13.4, ffs=1124, throughput_msps=264, max_abs_err=9.28e-05 (2^-13.40), power_index=21.2
Front coverage: luts 1023..1134 (HV reference 4000); accuracy_bits 13..13.4 (HV reference 13); data_width on the front 17..18 (registry 8..28).

Per family:
- unrolled_k: 10 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 12.26 bits
- pipelined: 30 evals, 2 feasible; max throughput seen 273 MSPS; best accuracy 13.40 bits; best feasible luts=1023; feasible ranges: data_width 17..18, n_iter 16..18, angle_guard 0..2, frac_guard 1..1
- pipelined_m: 60 evals, 0 feasible; max throughput seen 97.8 MSPS; best accuracy 15.42 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Evidence shows only the `pipelined` family can meet the throughput constraint (>=250 MSPS). `unrolled_k` and `pipelined_m` are infeasible due to throughput limits (max 10.3 and 97.8 MSPS respectively). The 2 feasible designs found in Round 1 are both `pipelined` with data_width 17-18 and n_iter 16-18. The best LUT count is 1023. To minimize LUTs (the selection rule) and improve hypervolume, I should focus the remaining budget on refining the `pipelined` family within the narrow range where feasibility was observed. I will slightly widen the ranges to ensure we don't miss a better corner (e.g., data_width 16, n_iter 14) but keep it tight to maximize the number of evaluations in the promising region.*)
- `pipelined` (100 evals): data_width=16..19, n_iter=14..20, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Only pipelined meets the 250 MSPS throughput constraint (unrolled_k max 10.3 MSPS, pipelined_m max 97.8 MSPS). The 2 feasible designs are clustered at data_width 17-18 and n_iter 16-18. I am narrowing the search to this region to find the minimum LUT design that satisfies max_abs_err <= 2^-13 (0.00012207). The current best is 1023 LUTs at 13.03 bits accuracy. I want to see if slightly lower n_iter or different guard bits can reduce LUTs while staying feasible, or if we can push accuracy higher for better hypervolume.

**Result (code):** 100 evaluations this round, 200 total; 52 feasible; hypervolume 7577 (+566.4%).

**LLM decision:** `refine` — The pipelined family is the only one meeting the throughput constraint (>= 250 MSPS). The current Pareto front has a minimum LUT count of 935 (data_width=19). The selection rule is 'min luts', so finding a feasible design with fewer LUTs is the primary goal. Data_width=18 designs are inherently cheaper than data_width=19. In Round 2, we saw a data_width=18 design (n_iter=16, angle_guard=2, frac_guard=2) achieve 13.8 bits accuracy with 1048 LUTs, which is worse than the 935 LUT design. However, we haven't fully explored the low-LUT region for data_width=18. Specifically, we need to check if data_width=18 with lower n_iter (e.g., 15) and appropriate guards can meet the 2^-13 accuracy constraint with fewer than 935 LUTs. The previous search may have missed this corner. By narrowing the search to data_width=18 and 19, and focusing on the lower end of the LUT spectrum (which corresponds to lower n_iter and guards), we can determine if a better solution exists. If not, we will have confirmed that 935 LUTs is the minimum for this spec.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 7577 (gain this round: +566.4%).
Feasible designs: 52 of 200 evaluations (34 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 35% violate; best seen 273
- max_abs_err <= 0.00012207: 56% violate; best seen 1.92e-05 (2^-15.67)

Pareto front (feasible, 12 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=19 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc] luts=935, accuracy_bits=13, ffs=969, throughput_msps=264, max_abs_err=0.000119 (2^-13.04), power_index=17.9
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=0 rounding=trunc] luts=949, accuracy_bits=13.2, ffs=984, throughput_msps=264, max_abs_err=0.000109 (2^-13.17), power_index=18.2
- pipelined [data_width=19 n_iter=15 angle_guard=0 frac_guard=1 rounding=trunc] luts=964, accuracy_bits=13.3, ffs=995, throughput_msps=264, max_abs_err=0.000101 (2^-13.27), power_index=18.4
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=2 rounding=trunc] luts=1008, accuracy_bits=13.6, ffs=1036, throughput_msps=264, max_abs_err=8.04e-05 (2^-13.60), power_index=19.2
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] luts=1019, accuracy_bits=13.6, ffs=1012, throughput_msps=264, max_abs_err=7.94e-05 (2^-13.62), power_index=19.1
- pipelined [data_width=19 n_iter=16 angle_guard=0 frac_guard=1 rounding=trunc] luts=1033, accuracy_bits=13.7, ffs=1061, throughput_msps=264, max_abs_err=7.43e-05 (2^-13.72), power_index=19.7
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts=1048, accuracy_bits=13.8, ffs=1073, throughput_msps=264, max_abs_err=6.86e-05 (2^-13.83), power_index=20
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts=1096, accuracy_bits=14.3, ffs=1122, throughput_msps=264, max_abs_err=4.81e-05 (2^-14.34), power_index=20.9
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=trunc] luts=1241, accuracy_bits=15, ffs=1263, throughput_msps=264, max_abs_err=3.04e-05 (2^-15.00), power_index=23.6
- pipelined [data_width=19 n_iter=19 angle_guard=2 frac_guard=2 rounding=round] luts=1354, accuracy_bits=15.7, ffs=1336, throughput_msps=264, max_abs_err=1.92e-05 (2^-15.67), power_index=25.3
Front coverage: luts 935..1354 (HV reference 4000); accuracy_bits 13..15.7 (HV reference 13); data_width on the front 18..19 (registry 8..28).

Per family:
- unrolled_k: 10 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 12.26 bits
- pipelined: 130 evals, 52 feasible; max throughput seen 273 MSPS; best accuracy 15.67 bits; best feasible luts=935; feasible ranges: data_width 17..19, n_iter 15..20, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 60 evals, 0 feasible; max throughput seen 97.8 MSPS; best accuracy 15.42 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The pipelined family is the only one meeting the throughput constraint (>= 250 MSPS). The current Pareto front has a minimum LUT count of 935 (data_width=19). The selection rule is 'min luts', so finding a feasible design with fewer LUTs is the primary goal. Data_width=18 designs are inherently cheaper than data_width=19. In Round 2, we saw a data_width=18 design (n_iter=16, angle_guard=2, frac_guard=2) achieve 13.8 bits accuracy with 1048 LUTs, which is worse than the 935 LUT design. However, we haven't fully explored the low-LUT region for data_width=18. Specifically, we need to check if data_width=18 with lower n_iter (e.g., 15) and appropriate guards can meet the 2^-13 accuracy constraint with fewer than 935 LUTs. The previous search may have missed this corner. By narrowing the search to data_width=18 and 19, and focusing on the lower end of the LUT spectrum (which corresponds to lower n_iter and guards), we can determine if a better solution exists. If not, we will have confirmed that 935 LUTs is the minimum for this spec.*)
- `pipelined` (40 evals): data_width=18..19, n_iter=15..20, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Focus on the only family that meets the 250 MSPS constraint (pipelined). The current front is dominated by data_width=19. We need to verify if data_width=18 can achieve the required accuracy (<= 2^-13) with fewer LUTs, as data_width=18 designs are cheaper. The current best LUT count is 935 at data_width=19. If data_width=18 can meet the accuracy constraint with < 935 LUTs, it will improve the Pareto front significantly. We restrict n_iter to 15-20 and guards to 0-2 based on the feasible region found so far to maximize the chance of finding a better low-LUT design.

**Result (code):** 40 evaluations this round, 240 total; 90 feasible; hypervolume 7680 (+1.4%).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 13 designs spanning 935-1354 LUTs and 13.2-15.7 accuracy bits. The minimum LUT design (935 LUTs, pipelined W=19 N=15) meets all constraints: throughput 264 MSPS >= 250 and max_abs_err 2^-13.18 <= 2^-13. The front covers the critical trade-off region effectively, with hypervolume 7680. Since this is the final round, the current front is sufficient for selection (min LUTs = 935).
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 7680 (gain this round: +1.4%).
Feasible designs: 90 of 240 evaluations (55 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 29% violate; best seen 273
- max_abs_err <= 0.00012207: 48% violate; best seen 1.92e-05 (2^-15.67)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=19 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts=935, accuracy_bits=13.2, ffs=969, throughput_msps=264, max_abs_err=0.000108 (2^-13.18), power_index=17.9
- pipelined [data_width=19 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] luts=964, accuracy_bits=13.6, ffs=999, throughput_msps=264, max_abs_err=8.33e-05 (2^-13.55), power_index=18.5
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] luts=1019, accuracy_bits=13.6, ffs=1012, throughput_msps=264, max_abs_err=7.94e-05 (2^-13.62), power_index=19.1
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] luts=1033, accuracy_bits=14.1, ffs=1065, throughput_msps=264, max_abs_err=5.75e-05 (2^-14.09), power_index=19.7
- pipelined [data_width=19 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc] luts=1080, accuracy_bits=14.2, ffs=1106, throughput_msps=264, max_abs_err=5.43e-05 (2^-14.17), power_index=20.6
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts=1136, accuracy_bits=14.5, ffs=1124, throughput_msps=264, max_abs_err=4.29e-05 (2^-14.51), power_index=21.3
- pipelined [data_width=19 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] luts=1152, accuracy_bits=14.5, ffs=1180, throughput_msps=264, max_abs_err=4.26e-05 (2^-14.52), power_index=21.9
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=0 rounding=round] luts=1170, accuracy_bits=14.7, ffs=1199, throughput_msps=264, max_abs_err=3.86e-05 (2^-14.66), power_index=22.3
- pipelined [data_width=19 n_iter=18 angle_guard=2 frac_guard=2 rounding=round] luts=1281, accuracy_bits=15.4, ffs=1265, throughput_msps=264, max_abs_err=2.34e-05 (2^-15.38), power_index=23.9
- pipelined [data_width=19 n_iter=19 angle_guard=2 frac_guard=2 rounding=round] luts=1354, accuracy_bits=15.7, ffs=1336, throughput_msps=264, max_abs_err=1.92e-05 (2^-15.67), power_index=25.3
Front coverage: luts 935..1354 (HV reference 4000); accuracy_bits 13.2..15.7 (HV reference 13); data_width on the front 19..19 (registry 8..28).

Per family:
- unrolled_k: 10 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 12.26 bits
- pipelined: 170 evals, 90 feasible; max throughput seen 273 MSPS; best accuracy 15.67 bits; best feasible luts=935; feasible ranges: data_width 17..19, n_iter 15..20, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 60 evals, 0 feasible; max throughput seen 97.8 MSPS; best accuracy 15.42 bits
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined` (160 evals): data_width=18..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (13 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 197 feasible; hypervolume 1.87e+04 (+143.6%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 13 designs spanning 935-1354 LUTs and 13.2-15.7 accuracy bits. The minimum LUT design (935 LUTs, pipelined W=19 N=15) meets all constraints: throughput 264 MSPS >= 250 and max_abs_err 2^-13.18 <= 2^-13. The front covers the critical trade-off region effectively, with hypervolume 7680. Since this is the final round, the current front is sufficient for selection (min LUTs = 935).
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.87e+04 (gain this round: +143.6%).
Feasible designs: 197 of 400 evaluations (153 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 28% violate; best seen 273
- max_abs_err <= 0.00012207: 33% violate; best seen 5.57e-08 (2^-24.10)

Pareto front (feasible, 26 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=19 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts=935, accuracy_bits=13.2, ffs=969, throughput_msps=264, max_abs_err=0.000108 (2^-13.18), power_index=17.9
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] luts=1019, accuracy_bits=13.6, ffs=1012, throughput_msps=264, max_abs_err=7.94e-05 (2^-13.62), power_index=19.1
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts=1096, accuracy_bits=14.3, ffs=1122, throughput_msps=264, max_abs_err=4.81e-05 (2^-14.34), power_index=20.9
- pipelined [data_width=19 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] luts=1152, accuracy_bits=14.5, ffs=1180, throughput_msps=264, max_abs_err=4.26e-05 (2^-14.52), power_index=21.9
- pipelined [data_width=19 n_iter=17 angle_guard=2 frac_guard=2 rounding=round] luts=1209, accuracy_bits=15.1, ffs=1195, throughput_msps=264, max_abs_err=2.76e-05 (2^-15.14), power_index=22.6
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=4 rounding=trunc] luts=1349, accuracy_bits=15.5, ffs=1364, throughput_msps=257, max_abs_err=2.09e-05 (2^-15.55), power_index=25.5
- pipelined [data_width=23 n_iter=19 angle_guard=-2 frac_guard=0 rounding=trunc] luts=1390, accuracy_bits=16.1, ffs=1419, throughput_msps=257, max_abs_err=1.46e-05 (2^-16.06), power_index=26.4
- pipelined [data_width=26 n_iter=18 angle_guard=0 frac_guard=0 rounding=round] luts=1510, accuracy_bits=16.9, ffs=1544, throughput_msps=257, max_abs_err=7.95e-06 (2^-16.94), power_index=28.7
- pipelined [data_width=23 n_iter=19 angle_guard=3 frac_guard=3 rounding=trunc] luts=1599, accuracy_bits=17.8, ffs=1617, throughput_msps=257, max_abs_err=4.49e-06 (2^-17.76), power_index=30.2
- pipelined [data_width=26 n_iter=24 angle_guard=0 frac_guard=0 rounding=round] luts=2041, accuracy_bits=20.6, ffs=2058, throughput_msps=257, max_abs_err=6.15e-07 (2^-20.63), power_index=38.5
Front coverage: luts 935..2041 (HV reference 4000); accuracy_bits 13.2..20.6 (HV reference 13); data_width on the front 19..26 (registry 8..28).

Per family:
- unrolled_k: 10 evals, 0 feasible; max throughput seen 10.3 MSPS; best accuracy 12.26 bits
- pipelined: 330 evals, 197 feasible; max throughput seen 273 MSPS; best accuracy 24.10 bits; best feasible luts=935; feasible ranges: data_width 17..26, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 60 evals, 0 feasible; max throughput seen 97.8 MSPS; best accuracy 15.42 bits
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 27672 in, 3990 out
- provider-reported cost: $0.0064
- full prompts and replies: `llm_trace.jsonl`

