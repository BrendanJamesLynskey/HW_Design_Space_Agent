# DSE run: dds_250msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 5 round(s).  
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
`pipelined:data_width=20,n_iter=15,angle_guard=-1,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts)

| metric | value | provenance |
|---|---|---|
| luts | 964 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 999 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 64.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 18.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 9.65e-05 (2^-13.34) | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 25.3 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.67e-05 (2^-15.19) | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 6.99 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.3 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 17 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 100.5 dBc, SNR 88.6 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (34 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=20,n_iter=15,angle_guard=-1,frac_guard=0,rounding=round` | 964 | 999 | 264.5 | 17 | 18.5 | 9.65e-05 (2^-13.34) | 13.34 |
| 1 | `pipelined:data_width=21,n_iter=15,angle_guard=-1,frac_guard=0,rounding=round` | 1008 | 1044 | 264.5 | 17 | 19.3 | 7.76e-05 (2^-13.65) | 13.65 |
| 2 | `pipelined:data_width=21,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc` | 1023 | 1059 | 264.5 | 17 | 19.6 | 7.62e-05 (2^-13.68) | 13.68 |
| 3 | `pipelined:data_width=20,n_iter=16,angle_guard=-1,frac_guard=0,rounding=round` | 1033 | 1065 | 264.5 | 18 | 19.7 | 6.98e-05 (2^-13.81) | 13.81 |
| 4 | `pipelined:data_width=20,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc` | 1080 | 1114 | 264.5 | 18 | 20.6 | 5.76e-05 (2^-14.08) | 14.08 |
| 5 | `pipelined:data_width=19,n_iter=17,angle_guard=2,frac_guard=0,rounding=round` | 1101 | 1132 | 264.5 | 19 | 21 | 4.23e-05 (2^-14.53) | 14.53 |
| 6 | `pipelined:data_width=22,n_iter=16,angle_guard=-1,frac_guard=0,rounding=trunc` | 1128 | 1162 | 264.5 | 18 | 21.5 | 4.1e-05 (2^-14.57) | 14.57 |
| 7 | `pipelined:data_width=21,n_iter=17,angle_guard=-1,frac_guard=0,rounding=round` | 1152 | 1183 | 264.5 | 19 | 22 | 3.65e-05 (2^-14.74) | 14.74 |
| 8 | `pipelined:data_width=22,n_iter=16,angle_guard=0,frac_guard=1,rounding=trunc` | 1175 | 1207 | 256.5 | 18 | 22.4 | 3.58e-05 (2^-14.77) | 14.77 |
| 9 | `pipelined:data_width=23,n_iter=16,angle_guard=0,frac_guard=0,rounding=trunc` | 1191 | 1227 | 256.5 | 18 | 22.7 | 3.32e-05 (2^-14.88) | 14.88 |
| 10 | `pipelined:data_width=20,n_iter=17,angle_guard=2,frac_guard=2,rounding=trunc` | 1219 | 1244 | 264.5 | 19 | 23.2 | 2.57e-05 (2^-15.25) | 15.25 |
| 11 | `pipelined:data_width=21,n_iter=17,angle_guard=2,frac_guard=1,rounding=trunc` | 1236 | 1265 | 256.5 | 19 | 23.5 | 2.27e-05 (2^-15.43) | 15.43 |
| 12 | `pipelined:data_width=23,n_iter=17,angle_guard=-1,frac_guard=0,rounding=trunc` | 1253 | 1286 | 256.5 | 19 | 23.9 | 2.1e-05 (2^-15.54) | 15.54 |
| 13 | `pipelined:data_width=22,n_iter=18,angle_guard=-1,frac_guard=0,rounding=trunc` | 1277 | 1308 | 264.5 | 20 | 24.3 | 2e-05 (2^-15.61) | 15.61 |
| 14 | `pipelined:data_width=20,n_iter=18,angle_guard=2,frac_guard=1,rounding=round` | 1301 | 1287 | 264.5 | 20 | 24.3 | 1.89e-05 (2^-15.69) | 15.69 |
| 15 | `pipelined:data_width=22,n_iter=17,angle_guard=2,frac_guard=1,rounding=round` | 1333 | 1319 | 256.5 | 19 | 24.9 | 1.67e-05 (2^-15.87) | 15.87 |
| 16 | `pipelined:data_width=23,n_iter=17,angle_guard=2,frac_guard=1,rounding=trunc` | 1337 | 1368 | 256.5 | 19 | 25.4 | 1.66e-05 (2^-15.88) | 15.88 |
| 17 | `pipelined:data_width=21,n_iter=18,angle_guard=1,frac_guard=1,rounding=round` | 1339 | 1324 | 264.5 | 20 | 25 | 1.44e-05 (2^-16.08) | 16.08 |
| 18 | `pipelined:data_width=23,n_iter=18,angle_guard=-1,frac_guard=2,rounding=trunc` | 1403 | 1427 | 256.5 | 20 | 26.6 | 1.23e-05 (2^-16.32) | 16.32 |
| 19 | `pipelined:data_width=22,n_iter=19,angle_guard=0,frac_guard=1,rounding=trunc` | 1409 | 1434 | 256.5 | 21 | 26.7 | 1.1e-05 (2^-16.47) | 16.47 |
| 20 | `pipelined:data_width=22,n_iter=19,angle_guard=2,frac_guard=1,rounding=trunc` | 1447 | 1472 | 256.5 | 21 | 27.4 | 8.01e-06 (2^-16.93) | 16.93 |
| 21 | `pipelined:data_width=22,n_iter=19,angle_guard=2,frac_guard=1,rounding=round` | 1493 | 1474 | 256.5 | 21 | 27.9 | 6.05e-06 (2^-17.33) | 17.33 |
| 22 | `pipelined:data_width=24,n_iter=19,angle_guard=0,frac_guard=1,rounding=trunc` | 1523 | 1549 | 256.5 | 21 | 28.9 | 5.51e-06 (2^-17.47) | 17.47 |
| 23 | `pipelined:data_width=21,n_iter=20,angle_guard=2,frac_guard=2,rounding=round` | 1551 | 1528 | 256.5 | 22 | 29 | 5.43e-06 (2^-17.49) | 17.49 |
| 24 | `pipelined:data_width=25,n_iter=19,angle_guard=-1,frac_guard=1,rounding=trunc` | 1561 | 1587 | 256.5 | 21 | 29.6 | 5.1e-06 (2^-17.58) | 17.58 |
| 25 | `pipelined:data_width=24,n_iter=20,angle_guard=0,frac_guard=0,rounding=round` | 1567 | 1594 | 256.5 | 22 | 29.7 | 3.6e-06 (2^-18.08) | 18.08 |
| 26 | `pipelined:data_width=23,n_iter=21,angle_guard=1,frac_guard=1,rounding=trunc` | 1649 | 1670 | 256.5 | 23 | 31.2 | 3.47e-06 (2^-18.14) | 18.14 |
| 27 | `pipelined:data_width=23,n_iter=21,angle_guard=2,frac_guard=1,rounding=trunc` | 1670 | 1691 | 256.5 | 23 | 31.6 | 3.24e-06 (2^-18.24) | 18.24 |
| 28 | `pipelined:data_width=23,n_iter=20,angle_guard=2,frac_guard=2,rounding=round` | 1675 | 1649 | 256.5 | 22 | 31.3 | 2.95e-06 (2^-18.37) | 18.37 |
| 29 | `pipelined:data_width=23,n_iter=20,angle_guard=3,frac_guard=3,rounding=trunc` | 1687 | 1703 | 256.5 | 22 | 31.9 | 2.74e-06 (2^-18.48) | 18.48 |
| 30 | `pipelined:data_width=24,n_iter=21,angle_guard=0,frac_guard=1,rounding=round` | 1742 | 1714 | 256.5 | 23 | 32.5 | 2.57e-06 (2^-18.57) | 18.57 |
| 31 | `pipelined:data_width=23,n_iter=21,angle_guard=2,frac_guard=2,rounding=round` | 1761 | 1731 | 256.5 | 23 | 32.8 | 2.11e-06 (2^-18.86) | 18.86 |
| 32 | `pipelined:data_width=23,n_iter=21,angle_guard=2,frac_guard=3,rounding=round` | 1803 | 1770 | 256.5 | 23 | 33.6 | 1.92e-06 (2^-18.99) | 18.99 |
| 33 | `pipelined:data_width=26,n_iter=26,angle_guard=-1,frac_guard=0,rounding=trunc` | 2192 | 2203 | 256.5 | 28 | 41.3 | 1.16e-06 (2^-19.72) | 19.72 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 1 sample/clock at >=250 MSPS, which strongly favors pipelined architectures. Pipelined is the primary candidate (50% budget) as it directly meets the throughput requirement with 1 result/cycle. Pipelined_m (30% budget) is included because it can reduce register count and potentially improve Fmax or reduce area, offering a different point on the Pareto front. Unrolled_k (20% budget) is included with a smaller share to verify if any configuration can meet the throughput constraint; if not, the budget is spent confirming infeasibility for that family. The data_width range starts at 12 because 13-bit accuracy requires at least 13-14 bits of precision, and we want to find the minimum width that meets the error constraint. The n_iter range starts at 12 because fewer iterations will likely not meet the 2^-13 error requirement. The angle_guard and frac_guard ranges are kept wide to explore how guard bits affect accuracy and area.*)
- `pipelined` (50 evals): data_width=12..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* The spec requires 1 sample/clock at >=250 MSPS, which mandates a pipelined architecture (iterative/unrolled_k produce 1 result every several cycles and will fail the throughput constraint). Pipelined is the baseline for this requirement. We search a wide range of data_width and n_iter to map the LUT vs accuracy trade-off, since accuracy depends on these parameters and we need to find the minimum LUT design that meets max_abs_err <= 2^-13.
- `pipelined_m` (30 evals): data_width=12..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Pipelined_m registers every m stages, which can reduce FF count and potentially improve Fmax or reduce area compared to fully pipelined. It still produces 1 result/cycle, so it meets the throughput constraint. The m parameter adds a new dimension for trade-off exploration: larger m means fewer registers but potentially lower Fmax. This family may find designs with fewer LUTs+FFs or better Fmax that push the Pareto front.
- `unrolled_k` (20 evals): data_width=12..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* Unrolled_k chains k micro-rotations per cycle. While it produces 1 result every ceil(N/k)+3 cycles, if k is large enough and N is small, the throughput might approach 1 result/cycle. However, this is unlikely to meet the 250 MSPS constraint unless Fmax is very high. Including it with a small budget share allows us to verify whether any unrolled configuration can meet the throughput constraint, and if so, whether it offers a better LUT trade-off. The k parameter allows exploring the trade-off between parallelism and resource usage.

**Result (code):** 100 evaluations this round, 100 total; 25 feasible; hypervolume 1.516e+04 (n/a).

**LLM decision:** `refine` — The `pipelined` family is the only one meeting the throughput constraint (>=250 MSPS), while `unrolled_k` and `pipelined_m` failed significantly (max 9.97 and 164 MSPS respectively). The current Pareto front is dominated by `pipelined` designs with `data_width` 22-24, `n_iter` 17-21, and `angle_guard`=2. The minimum LUT count on the front is 1333, which is well below the HV reference of 4000, but we can likely push this lower by exploring smaller `data_width` values (down to 19, which was seen in feasible ranges) and optimizing `n_iter` and guards more tightly. The accuracy constraint (<= 2^-13) is easily met by all front designs (best 15.9 bits), so we have room to trade accuracy for area. I will narrow the search space to focus on the promising `pipelined` region with lower `data_width` and optimized parameters to minimize LUTs.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 1.516e+04 (gain this round: n/a (first round)).
Feasible designs: 25 of 100 evaluations (22 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 62% violate; best seen 273
- max_abs_err <= 0.00012207: 25% violate; best seen 2.51e-07 (2^-21.93)

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=22 n_iter=17 angle_guard=2 frac_guard=1 rounding=round] luts=1333, accuracy_bits=15.9, ffs=1319, throughput_msps=257, max_abs_err=1.67e-05 (2^-15.87), power_index=24.9
- pipelined [data_width=23 n_iter=17 angle_guard=2 frac_guard=1 rounding=round] luts=1386, accuracy_bits=15.9, ffs=1370, throughput_msps=257, max_abs_err=1.61e-05 (2^-15.92), power_index=25.9
- pipelined [data_width=24 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc] luts=1388, accuracy_bits=15.9, ffs=1420, throughput_msps=257, max_abs_err=1.61e-05 (2^-15.93), power_index=26.4
- pipelined [data_width=24 n_iter=17 angle_guard=2 frac_guard=1 rounding=round] luts=1438, accuracy_bits=16, ffs=1422, throughput_msps=257, max_abs_err=1.56e-05 (2^-15.96), power_index=26.9
- pipelined [data_width=22 n_iter=19 angle_guard=2 frac_guard=1 rounding=trunc] luts=1447, accuracy_bits=16.9, ffs=1472, throughput_msps=257, max_abs_err=8.01e-06 (2^-16.93), power_index=27.4
- pipelined [data_width=22 n_iter=19 angle_guard=2 frac_guard=1 rounding=round] luts=1493, accuracy_bits=17.3, ffs=1474, throughput_msps=257, max_abs_err=6.05e-06 (2^-17.33), power_index=27.9
- pipelined [data_width=23 n_iter=21 angle_guard=2 frac_guard=1 rounding=trunc] luts=1670, accuracy_bits=18.2, ffs=1691, throughput_msps=257, max_abs_err=3.24e-06 (2^-18.24), power_index=31.6
- pipelined [data_width=23 n_iter=21 angle_guard=2 frac_guard=2 rounding=round] luts=1761, accuracy_bits=18.9, ffs=1731, throughput_msps=257, max_abs_err=2.11e-06 (2^-18.86), power_index=32.8
- pipelined [data_width=23 n_iter=21 angle_guard=2 frac_guard=3 rounding=round] luts=1803, accuracy_bits=19, ffs=1770, throughput_msps=257, max_abs_err=1.92e-06 (2^-18.99), power_index=33.6
Front coverage: luts 1333..1803 (HV reference 4000); accuracy_bits 15.9..19 (HV reference 13); data_width on the front 22..24 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 19.43 bits
- pipelined: 50 evals, 25 feasible; max throughput seen 273 MSPS; best accuracy 21.93 bits; best feasible luts=1333; feasible ranges: data_width 19..24, n_iter 17..28, angle_guard -2..4, frac_guard 0..3
- pipelined_m: 30 evals, 0 feasible; max throughput seen 164 MSPS; best accuracy 21.87 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Narrowing the search space to the promising pipelined region with lower data_width and optimized parameters to minimize LUTs while maintaining throughput and accuracy constraints.*)
- `pipelined` (100 evals): data_width=19..23, n_iter=15..22, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Focus on pipelined family which is the only one meeting throughput. Narrow data_width to 19-23 to find lower LUT counts, n_iter to 15-22 to balance accuracy and area, and angle_guard to -1 to 2 to reduce LUTs while maintaining accuracy. Exclude pipelined_m and unrolled_k as they cannot meet throughput.

**Result (code):** 100 evaluations this round, 200 total; 125 feasible; hypervolume 1.581e+04 (+4.3%).

**LLM decision:** `map_front` — The pipelined family is the only one that meets the throughput constraint (>=250 MSPS); unrolled_k (max 9.97) and pipelined_m (max 164) are infeasible, and iterative is structurally infeasible (1 result/cycle at ~250 MHz = 250 MSPS, which is < 250). The current front covers luts 964..1803 and accuracy 13.3..19 bits, but the pipelined family's feasible region extends to data_width 24 and n_iter 28, and the hypervolume gain this round was only +4.3%, indicating the front is not yet fully mapped. Since only pipelined is on the front, I will let code run NSGA-II over the full pipelined parameter ranges to map the complete trade-off curve, maximizing hypervolume coverage before the final design is selected by min LUTs.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.581e+04 (gain this round: +4.3%).
Feasible designs: 125 of 200 evaluations (105 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 31% violate; best seen 273
- max_abs_err <= 0.00012207: 12% violate; best seen 2.51e-07 (2^-21.93)

Pareto front (feasible, 24 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=20 n_iter=15 angle_guard=-1 frac_guard=0 rounding=round] luts=964, accuracy_bits=13.3, ffs=999, throughput_msps=264, max_abs_err=9.65e-05 (2^-13.34), power_index=18.5
- pipelined [data_width=20 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round] luts=1033, accuracy_bits=13.8, ffs=1065, throughput_msps=264, max_abs_err=6.98e-05 (2^-13.81), power_index=19.7
- pipelined [data_width=19 n_iter=17 angle_guard=2 frac_guard=0 rounding=round] luts=1101, accuracy_bits=14.5, ffs=1132, throughput_msps=264, max_abs_err=4.23e-05 (2^-14.53), power_index=21
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc] luts=1219, accuracy_bits=15.2, ffs=1244, throughput_msps=264, max_abs_err=2.57e-05 (2^-15.25), power_index=23.2
- pipelined [data_width=23 n_iter=17 angle_guard=-1 frac_guard=0 rounding=trunc] luts=1253, accuracy_bits=15.5, ffs=1286, throughput_msps=257, max_abs_err=2.1e-05 (2^-15.54), power_index=23.9
- pipelined [data_width=23 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc] luts=1337, accuracy_bits=15.9, ffs=1368, throughput_msps=257, max_abs_err=1.66e-05 (2^-15.88), power_index=25.4
- pipelined [data_width=23 n_iter=18 angle_guard=-1 frac_guard=2 rounding=trunc] luts=1403, accuracy_bits=16.3, ffs=1427, throughput_msps=257, max_abs_err=1.23e-05 (2^-16.32), power_index=26.6
- pipelined [data_width=21 n_iter=20 angle_guard=2 frac_guard=2 rounding=round] luts=1551, accuracy_bits=17.5, ffs=1528, throughput_msps=257, max_abs_err=5.43e-06 (2^-17.49), power_index=29
- pipelined [data_width=23 n_iter=21 angle_guard=2 frac_guard=1 rounding=trunc] luts=1670, accuracy_bits=18.2, ffs=1691, throughput_msps=257, max_abs_err=3.24e-06 (2^-18.24), power_index=31.6
- pipelined [data_width=23 n_iter=21 angle_guard=2 frac_guard=3 rounding=round] luts=1803, accuracy_bits=19, ffs=1770, throughput_msps=257, max_abs_err=1.92e-06 (2^-18.99), power_index=33.6
Front coverage: luts 964..1803 (HV reference 4000); accuracy_bits 13.3..19 (HV reference 13); data_width on the front 19..23 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 19.43 bits
- pipelined: 150 evals, 125 feasible; max throughput seen 273 MSPS; best accuracy 21.93 bits; best feasible luts=964; feasible ranges: data_width 19..24, n_iter 15..28, angle_guard -2..4, frac_guard 0..3
- pipelined_m: 30 evals, 0 feasible; max throughput seen 164 MSPS; best accuracy 21.87 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (40 evals): data_width=18..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (24 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 240 total; 150 feasible; hypervolume 1.581e+04 (+0.0%).

**LLM decision:** `map_front` — The `pipelined` family is the only one capable of meeting the throughput constraint (>= 250 MSPS), as evidenced by `unrolled_k` (max 9.97 MSPS) and `pipelined_m` (max 164 MSPS) failing completely. The current Pareto front for `pipelined` is well-established with 150 feasible points, covering a wide range of LUTs (964-1803) and accuracy bits (13.3-19.0). The hypervolume gain in Round 3 was 0.0%, indicating that the search has converged on the current front and further random sampling or narrow refinement is unlikely to yield significant improvements. Since we have 1 round left (Round 4) and the goal is to maximize hypervolume by mapping the feasible Pareto front as well as possible, the best use of the remaining budget is to let the code perform a final, dense mapping of the `pipelined` family's full parameter space (or the specific sub-space identified as feasible) to ensure no better trade-offs are missed before the final selection.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 1.581e+04 (gain this round: +0.0%).
Feasible designs: 150 of 240 evaluations (128 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 31% violate; best seen 273
- max_abs_err <= 0.00012207: 12% violate; best seen 4.99e-08 (2^-24.25)

Pareto front (feasible, 24 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=20 n_iter=15 angle_guard=-1 frac_guard=0 rounding=round] luts=964, accuracy_bits=13.3, ffs=999, throughput_msps=264, max_abs_err=9.65e-05 (2^-13.34), power_index=18.5
- pipelined [data_width=20 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round] luts=1033, accuracy_bits=13.8, ffs=1065, throughput_msps=264, max_abs_err=6.98e-05 (2^-13.81), power_index=19.7
- pipelined [data_width=19 n_iter=17 angle_guard=2 frac_guard=0 rounding=round] luts=1101, accuracy_bits=14.5, ffs=1132, throughput_msps=264, max_abs_err=4.23e-05 (2^-14.53), power_index=21
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc] luts=1219, accuracy_bits=15.2, ffs=1244, throughput_msps=264, max_abs_err=2.57e-05 (2^-15.25), power_index=23.2
- pipelined [data_width=23 n_iter=17 angle_guard=-1 frac_guard=0 rounding=trunc] luts=1253, accuracy_bits=15.5, ffs=1286, throughput_msps=257, max_abs_err=2.1e-05 (2^-15.54), power_index=23.9
- pipelined [data_width=23 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc] luts=1337, accuracy_bits=15.9, ffs=1368, throughput_msps=257, max_abs_err=1.66e-05 (2^-15.88), power_index=25.4
- pipelined [data_width=23 n_iter=18 angle_guard=-1 frac_guard=2 rounding=trunc] luts=1403, accuracy_bits=16.3, ffs=1427, throughput_msps=257, max_abs_err=1.23e-05 (2^-16.32), power_index=26.6
- pipelined [data_width=21 n_iter=20 angle_guard=2 frac_guard=2 rounding=round] luts=1551, accuracy_bits=17.5, ffs=1528, throughput_msps=257, max_abs_err=5.43e-06 (2^-17.49), power_index=29
- pipelined [data_width=23 n_iter=21 angle_guard=2 frac_guard=1 rounding=trunc] luts=1670, accuracy_bits=18.2, ffs=1691, throughput_msps=257, max_abs_err=3.24e-06 (2^-18.24), power_index=31.6
- pipelined [data_width=23 n_iter=21 angle_guard=2 frac_guard=3 rounding=round] luts=1803, accuracy_bits=19, ffs=1770, throughput_msps=257, max_abs_err=1.92e-06 (2^-18.99), power_index=33.6
Front coverage: luts 964..1803 (HV reference 4000); accuracy_bits 13.3..19 (HV reference 13); data_width on the front 19..23 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 19.43 bits
- pipelined: 190 evals, 150 feasible; max throughput seen 273 MSPS; best accuracy 24.25 bits; best feasible luts=964; feasible ranges: data_width 19..25, n_iter 15..28, angle_guard -2..4, frac_guard 0..3
- pipelined_m: 30 evals, 0 feasible; max throughput seen 164 MSPS; best accuracy 21.87 bits
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined` (100 evals): data_width=18..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (24 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 340 total; 217 feasible; hypervolume 1.715e+04 (+8.5%).

**LLM decision:** `stop` — The search has reached the round and evaluation budget limits (Round 4/4, 340/400 evals). The feasible Pareto front is well-established with 217 feasible designs, dominated by the `pipelined` family which is the only architecture capable of meeting the strict throughput constraint (>= 250 MSPS). The `unrolled_k` and `pipelined_m` families were explored and found infeasible for this spec due to throughput limitations (max 9.97 and 164 MSPS respectively). The front covers a wide range of the objective space (LUTs 964..2192, accuracy 13.3..19.7 bits) relative to the reference point (4000 LUTs, 13 bits), yielding a hypervolume of 1.715e+04. The selection rule (min LUTs) points to the design `pipelined [data_width=20 n_iter=15 angle_guard=-1 frac_guard=0 rounding=round]` with 964 LUTs and 13.3 accuracy bits, which satisfies all constraints (throughput 264 MSPS, max_abs_err 9.65e-05 <= 1.22e-04). No further exploration is possible or necessary within the budget.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 60 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 340 of 400.
Hypervolume of the feasible front: 1.715e+04 (gain this round: +8.5%).
Feasible designs: 217 of 340 evaluations (185 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 29% violate; best seen 273
- max_abs_err <= 0.00012207: 12% violate; best seen 4.99e-08 (2^-24.25)

Pareto front (feasible, 30 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=20 n_iter=15 angle_guard=-1 frac_guard=0 rounding=round] luts=964, accuracy_bits=13.3, ffs=999, throughput_msps=264, max_abs_err=9.65e-05 (2^-13.34), power_index=18.5
- pipelined [data_width=20 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round] luts=1033, accuracy_bits=13.8, ffs=1065, throughput_msps=264, max_abs_err=6.98e-05 (2^-13.81), power_index=19.7
- pipelined [data_width=21 n_iter=17 angle_guard=-1 frac_guard=0 rounding=round] luts=1152, accuracy_bits=14.7, ffs=1183, throughput_msps=264, max_abs_err=3.65e-05 (2^-14.74), power_index=22
- pipelined [data_width=23 n_iter=17 angle_guard=-1 frac_guard=0 rounding=trunc] luts=1253, accuracy_bits=15.5, ffs=1286, throughput_msps=257, max_abs_err=2.1e-05 (2^-15.54), power_index=23.9
- pipelined [data_width=22 n_iter=17 angle_guard=2 frac_guard=1 rounding=round] luts=1333, accuracy_bits=15.9, ffs=1319, throughput_msps=257, max_abs_err=1.67e-05 (2^-15.87), power_index=24.9
- pipelined [data_width=23 n_iter=18 angle_guard=-1 frac_guard=2 rounding=trunc] luts=1403, accuracy_bits=16.3, ffs=1427, throughput_msps=257, max_abs_err=1.23e-05 (2^-16.32), power_index=26.6
- pipelined [data_width=21 n_iter=20 angle_guard=2 frac_guard=2 rounding=round] luts=1551, accuracy_bits=17.5, ffs=1528, throughput_msps=257, max_abs_err=5.43e-06 (2^-17.49), power_index=29
- pipelined [data_width=23 n_iter=21 angle_guard=1 frac_guard=1 rounding=trunc] luts=1649, accuracy_bits=18.1, ffs=1670, throughput_msps=257, max_abs_err=3.47e-06 (2^-18.14), power_index=31.2
- pipelined [data_width=23 n_iter=20 angle_guard=3 frac_guard=3 rounding=trunc] luts=1687, accuracy_bits=18.5, ffs=1703, throughput_msps=257, max_abs_err=2.74e-06 (2^-18.48), power_index=31.9
- pipelined [data_width=26 n_iter=26 angle_guard=-1 frac_guard=0 rounding=trunc] luts=2192, accuracy_bits=19.7, ffs=2203, throughput_msps=257, max_abs_err=1.16e-06 (2^-19.72), power_index=41.3
Front coverage: luts 964..2192 (HV reference 4000); accuracy_bits 13.3..19.7 (HV reference 13); data_width on the front 19..26 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 19.43 bits
- pipelined: 290 evals, 217 feasible; max throughput seen 273 MSPS; best accuracy 24.25 bits; best feasible luts=964; feasible ranges: data_width 18..26, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 30 evals, 0 feasible; max throughput seen 164 MSPS; best accuracy 21.87 bits
```
</details>

### Round 5

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 60 evaluations*)
- `pipelined` (60 evals): data_width=18..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (30 front designs; box front_anchored)

**Result (code):** 60 evaluations this round, 400 total; 257 feasible; hypervolume 1.72e+04 (+0.3%).

**No LLM call** (code's front-mapping round): The search has reached the round and evaluation budget limits (Round 4/4, 340/400 evals). The feasible Pareto front is well-established with 217 feasible designs, dominated by the `pipelined` family which is the only architecture capable of meeting the strict throughput constraint (>= 250 MSPS). The `unrolled_k` and `pipelined_m` families were explored and found infeasible for this spec due to throughput limitations (max 9.97 and 164 MSPS respectively). The front covers a wide range of the objective space (LUTs 964..2192, accuracy 13.3..19.7 bits) relative to the reference point (4000 LUTs, 13 bits), yielding a hypervolume of 1.715e+04. The selection rule (min LUTs) points to the design `pipelined [data_width=20 n_iter=15 angle_guard=-1 frac_guard=0 rounding=round]` with 964 LUTs and 13.3 accuracy bits, which satisfies all constraints (throughput 264 MSPS, max_abs_err 9.65e-05 <= 1.22e-04). No further exploration is possible or necessary within the budget.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 5 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.72e+04 (gain this round: +0.3%).
Feasible designs: 257 of 400 evaluations (218 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 29% violate; best seen 273
- max_abs_err <= 0.00012207: 11% violate; best seen 4.99e-08 (2^-24.25)

Pareto front (feasible, 34 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=20 n_iter=15 angle_guard=-1 frac_guard=0 rounding=round] luts=964, accuracy_bits=13.3, ffs=999, throughput_msps=264, max_abs_err=9.65e-05 (2^-13.34), power_index=18.5
- pipelined [data_width=20 n_iter=16 angle_guard=2 frac_guard=0 rounding=trunc] luts=1080, accuracy_bits=14.1, ffs=1114, throughput_msps=264, max_abs_err=5.76e-05 (2^-14.08), power_index=20.6
- pipelined [data_width=21 n_iter=17 angle_guard=-1 frac_guard=0 rounding=round] luts=1152, accuracy_bits=14.7, ffs=1183, throughput_msps=264, max_abs_err=3.65e-05 (2^-14.74), power_index=22
- pipelined [data_width=21 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc] luts=1236, accuracy_bits=15.4, ffs=1265, throughput_msps=257, max_abs_err=2.27e-05 (2^-15.43), power_index=23.5
- pipelined [data_width=22 n_iter=17 angle_guard=2 frac_guard=1 rounding=round] luts=1333, accuracy_bits=15.9, ffs=1319, throughput_msps=257, max_abs_err=1.67e-05 (2^-15.87), power_index=24.9
- pipelined [data_width=23 n_iter=18 angle_guard=-1 frac_guard=2 rounding=trunc] luts=1403, accuracy_bits=16.3, ffs=1427, throughput_msps=257, max_abs_err=1.23e-05 (2^-16.32), power_index=26.6
- pipelined [data_width=24 n_iter=19 angle_guard=0 frac_guard=1 rounding=trunc] luts=1523, accuracy_bits=17.5, ffs=1549, throughput_msps=257, max_abs_err=5.51e-06 (2^-17.47), power_index=28.9
- pipelined [data_width=23 n_iter=21 angle_guard=1 frac_guard=1 rounding=trunc] luts=1649, accuracy_bits=18.1, ffs=1670, throughput_msps=257, max_abs_err=3.47e-06 (2^-18.14), power_index=31.2
- pipelined [data_width=23 n_iter=20 angle_guard=3 frac_guard=3 rounding=trunc] luts=1687, accuracy_bits=18.5, ffs=1703, throughput_msps=257, max_abs_err=2.74e-06 (2^-18.48), power_index=31.9
- pipelined [data_width=26 n_iter=26 angle_guard=-1 frac_guard=0 rounding=trunc] luts=2192, accuracy_bits=19.7, ffs=2203, throughput_msps=257, max_abs_err=1.16e-06 (2^-19.72), power_index=41.3
Front coverage: luts 964..2192 (HV reference 4000); accuracy_bits 13.3..19.7 (HV reference 13); data_width on the front 19..26 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 19.43 bits
- pipelined: 350 evals, 257 feasible; max throughput seen 273 MSPS; best accuracy 24.25 bits; best feasible luts=964; feasible ranges: data_width 18..26, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 30 evals, 0 feasible; max throughput seen 164 MSPS; best accuracy 21.87 bits
```
</details>

## LLM usage
- calls: 9 (failed/unparsed attempts: 1)
- tokens: 27536 in, 3053 out
- provider-reported cost: $0.0073
- full prompts and replies: `llm_trace.jsonl`

