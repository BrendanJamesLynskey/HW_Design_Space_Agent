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
`pipelined:data_width=20,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts)

| metric | value | provenance |
|---|---|---|
| luts | 979 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 1014 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 64.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 18.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 8.24e-05 (2^-13.57) | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 21.6 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.58e-05 (2^-15.24) | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 6.76 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.6 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 17 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 98.2 dBc, SNR 88.8 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (25 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=20,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 979 | 1014 | 264.5 | 17 | 18.7 | 8.24e-05 (2^-13.57) | 13.57 |
| 1 | `pipelined:data_width=19,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 1001 | 1033 | 264.5 | 18 | 19.1 | 7.72e-05 (2^-13.66) | 13.66 |
| 2 | `pipelined:data_width=20,n_iter=16,angle_guard=-1,frac_guard=0,rounding=trunc` | 1033 | 1065 | 264.5 | 18 | 19.7 | 7.12e-05 (2^-13.78) | 13.78 |
| 3 | `pipelined:data_width=20,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 1064 | 1098 | 264.5 | 18 | 20.3 | 4.64e-05 (2^-14.39) | 14.39 |
| 4 | `pipelined:data_width=21,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 1096 | 1130 | 264.5 | 18 | 20.9 | 4.14e-05 (2^-14.56) | 14.56 |
| 5 | `pipelined:data_width=21,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 1112 | 1146 | 264.5 | 18 | 21.2 | 3.91e-05 (2^-14.64) | 14.64 |
| 6 | `pipelined:data_width=21,n_iter=16,angle_guard=2,frac_guard=0,rounding=round` | 1128 | 1162 | 256.5 | 18 | 21.5 | 3.65e-05 (2^-14.74) | 14.74 |
| 7 | `pipelined:data_width=21,n_iter=17,angle_guard=-1,frac_guard=0,rounding=round` | 1152 | 1183 | 264.5 | 19 | 22 | 3.65e-05 (2^-14.74) | 14.74 |
| 8 | `pipelined:data_width=21,n_iter=16,angle_guard=1,frac_guard=1,rounding=round` | 1188 | 1176 | 264.5 | 18 | 22.2 | 3.61e-05 (2^-14.76) | 14.76 |
| 9 | `pipelined:data_width=22,n_iter=17,angle_guard=-1,frac_guard=0,rounding=trunc` | 1202 | 1235 | 264.5 | 19 | 22.9 | 2.67e-05 (2^-15.19) | 15.19 |
| 10 | `pipelined:data_width=22,n_iter=17,angle_guard=0,frac_guard=0,rounding=trunc` | 1219 | 1252 | 264.5 | 19 | 23.2 | 2.44e-05 (2^-15.32) | 15.32 |
| 11 | `pipelined:data_width=22,n_iter=17,angle_guard=1,frac_guard=0,rounding=round` | 1236 | 1269 | 256.5 | 19 | 23.6 | 1.95e-05 (2^-15.64) | 15.64 |
| 12 | `pipelined:data_width=21,n_iter=18,angle_guard=1,frac_guard=0,rounding=round` | 1259 | 1289 | 264.5 | 20 | 24 | 1.68e-05 (2^-15.87) | 15.87 |
| 13 | `pipelined:data_width=21,n_iter=19,angle_guard=1,frac_guard=0,rounding=round` | 1333 | 1361 | 264.5 | 21 | 25.3 | 1.29e-05 (2^-16.24) | 16.24 |
| 14 | `pipelined:data_width=23,n_iter=18,angle_guard=-1,frac_guard=1,rounding=trunc` | 1367 | 1394 | 256.5 | 20 | 26 | 1.27e-05 (2^-16.26) | 16.26 |
| 15 | `pipelined:data_width=21,n_iter=19,angle_guard=1,frac_guard=1,rounding=round` | 1415 | 1397 | 264.5 | 21 | 26.4 | 1.06e-05 (2^-16.52) | 16.52 |
| 16 | `pipelined:data_width=22,n_iter=18,angle_guard=1,frac_guard=2,rounding=round` | 1431 | 1410 | 256.5 | 20 | 26.7 | 9.91e-06 (2^-16.62) | 16.62 |
| 17 | `pipelined:data_width=22,n_iter=18,angle_guard=4,frac_guard=1,rounding=round` | 1449 | 1433 | 256.5 | 20 | 27.1 | 9.76e-06 (2^-16.64) | 16.64 |
| 18 | `pipelined:data_width=22,n_iter=20,angle_guard=1,frac_guard=0,rounding=round` | 1467 | 1493 | 256.5 | 22 | 27.8 | 6.49e-06 (2^-17.23) | 17.23 |
| 19 | `pipelined:data_width=22,n_iter=20,angle_guard=2,frac_guard=1,rounding=trunc` | 1527 | 1550 | 256.5 | 22 | 28.9 | 6.11e-06 (2^-17.32) | 17.32 |
| 20 | `pipelined:data_width=22,n_iter=19,angle_guard=2,frac_guard=3,rounding=round` | 1569 | 1543 | 256.5 | 21 | 29.3 | 5.47e-06 (2^-17.48) | 17.48 |
| 21 | `pipelined:data_width=22,n_iter=21,angle_guard=2,frac_guard=1,rounding=round` | 1653 | 1629 | 256.5 | 23 | 30.9 | 3.51e-06 (2^-18.12) | 18.12 |
| 22 | `pipelined:data_width=22,n_iter=24,angle_guard=2,frac_guard=1,rounding=round` | 1894 | 1862 | 256.5 | 26 | 35.3 | 3.37e-06 (2^-18.18) | 18.18 |
| 23 | `pipelined:data_width=25,n_iter=26,angle_guard=0,frac_guard=0,rounding=round` | 2139 | 2151 | 256.5 | 28 | 40.3 | 1.37e-06 (2^-19.48) | 19.48 |
| 24 | `pipelined:data_width=24,n_iter=28,angle_guard=1,frac_guard=2,rounding=round` | 2417 | 2367 | 256.5 | 30 | 45 | 1.06e-06 (2^-19.84) | 19.84 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands one sample per clock at >=250 MSPS, which rules out the iterative family (one result every N+3 cycles) and makes throughput a function of Fmax (pipelined/pipelined_m) or Fmax x k (unrolled_k). I therefore search only the three 1-result/cycle families. The accuracy constraint (max_abs_err <= 2^-13, i.e. accuracy_bits >= 13) is met by n_iter ~14-16 with adequate data_width, so I bracket data_width 14..22 and n_iter 14..24 to cover the accuracy objective while keeping area low for the min-LUTs objective. angle_guard (-1..2) and frac_guard (0..2) are kept narrow because they are small second-order accuracy/area knobs; rounding is both since round can add ~0.5 accuracy bit cheaply. pipelined_m is the lead family because its m knob trades FFs/area against Fmax/latency at fixed 1/cycle throughput, which is exactly the trade-off the min-LUTs objective wants to exploit; pipelined anchors the feasible region and unrolled_k probes a lower-area throughput path. The three families share identical accuracy bits, so the front is driven by the area/Fmax/latency trade-offs, which is where the hypervolume value lies. I will let the code allocate the 100-eval round across these three and re-weight toward whichever families actually satisfy the throughput constraint in round 1.*)
- `pipelined_m` (34 evals): data_width=14..22, n_iter=14..24, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* Primary candidate: 1 result/cycle so throughput = Fmax (MHz) = MSPS, making the >=250 MSPS constraint a pure Fmax requirement that a moderately pipelined CORDIC can meet. Registering every m stages (m>1) cuts FFs and area vs full pipelined while keeping 1/cycle throughput, directly serving the min-LUTs objective. m is the key area/latency/Fmax knob, so I sweep the full 2..8 range. data_width 14..22 and n_iter 14..24 bracket the accuracy_bits>=13 requirement (error ~2^-n_iter, so N~14-16 suffices; width must carry the fractional output), leaving headroom for the accuracy objective. angle_guard -1..2 and frac_guard 0..2 cover the small guard-bit trade-offs that affect both accuracy and LUT count. rounding both, since round can buy ~0.5 bit of accuracy at a small LUT cost.
- `pipelined` (33 evals): data_width=14..22, n_iter=14..24, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Full one-register-per-stage pipeline is the throughput-safe baseline (1/cycle, Fmax=MSPS) and gives the cleanest Fmax, so it anchors the feasible region and the accuracy-vs-area trade-off. It is the natural reference against which pipelined_m's area savings are measured; including it lets the front show the latency/area/Fmax curve that the m-family compresses. Same accuracy-bracketing ranges as pipelined_m so the two are directly comparable on the identical-bit accuracy axis.
- `unrolled_k` (33 evals): data_width=14..22, n_iter=14..24, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=2..8. *Why:* Secondary candidate: k chained micro-rotations/cycle with a shared FSM can reach 1 result/cycle-equivalent throughput (Fmax x k) at lower area than a full pipeline, potentially beating pipelined_m on LUTs while still clearing 250 MSPS. k is the throughput/area knob, so I sweep 2..8. It is a plausible LUT-minimiser, so it belongs on the front; if its Fmax is too low to hit 250 MSPS at the needed k, the constraint will simply exclude it and the budget is not wasted on a dead family.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 100 evaluations this round, 100 total; 28 feasible; hypervolume 1.088e+04 (n/a).

**LLM decision:** `refine` — The `pipelined` family is the only one meeting the throughput constraint (>= 250 MSPS), while `unrolled_k` (max ~10 MSPS) and `pipelined_m` (max ~171 MSPS) are infeasible. The current Pareto front spans 1001 to 1845 LUTs. To maximize hypervolume and find the true minimum LUT design, we should focus the search on the `pipelined` family within the proven feasible region (data_width 19-22, n_iter 16-24) and specifically target the lower LUT end (data_width 19-20) to see if we can push accuracy bits higher with fewer resources or find a lower LUT point that still meets the 13-bit accuracy constraint. We will narrow the ranges to exclude the high-LUT, high-accuracy tail that is less relevant for the 'min LUTs' selection rule, and focus on the trade-off curve near the constraint boundary.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 1.088e+04 (gain this round: n/a (first round)).
Feasible designs: 28 of 100 evaluations (26 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 67% violate; best seen 273
- max_abs_err <= 0.00012207: 19% violate; best seen 7.43e-06 (2^-17.04)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=19 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts=1001, accuracy_bits=13.7, ffs=1033, throughput_msps=264, max_abs_err=7.72e-05 (2^-13.66), power_index=19.1
- pipelined [data_width=21 n_iter=16 angle_guard=-1 frac_guard=0 rounding=round] luts=1080, accuracy_bits=14.3, ffs=1114, throughput_msps=264, max_abs_err=4.91e-05 (2^-14.31), power_index=20.6
- pipelined [data_width=21 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts=1096, accuracy_bits=14.6, ffs=1130, throughput_msps=264, max_abs_err=4.14e-05 (2^-14.56), power_index=20.9
- pipelined [data_width=21 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] luts=1128, accuracy_bits=14.7, ffs=1162, throughput_msps=257, max_abs_err=3.65e-05 (2^-14.74), power_index=21.5
- pipelined [data_width=21 n_iter=17 angle_guard=2 frac_guard=0 rounding=trunc] luts=1202, accuracy_bits=15, ffs=1235, throughput_msps=257, max_abs_err=3.12e-05 (2^-14.97), power_index=22.9
- pipelined [data_width=21 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc] luts=1236, accuracy_bits=15.4, ffs=1265, throughput_msps=257, max_abs_err=2.27e-05 (2^-15.43), power_index=23.5
- pipelined [data_width=22 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc] luts=1287, accuracy_bits=15.7, ffs=1317, throughput_msps=257, max_abs_err=1.83e-05 (2^-15.74), power_index=24.5
- pipelined [data_width=21 n_iter=22 angle_guard=1 frac_guard=0 rounding=round] luts=1554, accuracy_bits=16.3, ffs=1576, throughput_msps=264, max_abs_err=1.21e-05 (2^-16.34), power_index=29.4
- pipelined [data_width=22 n_iter=22 angle_guard=0 frac_guard=0 rounding=round] luts=1599, accuracy_bits=16.8, ffs=1620, throughput_msps=264, max_abs_err=8.91e-06 (2^-16.78), power_index=30.3
- pipelined [data_width=22 n_iter=24 angle_guard=0 frac_guard=1 rounding=round] luts=1845, accuracy_bits=17, ffs=1814, throughput_msps=257, max_abs_err=7.63e-06 (2^-17.00), power_index=34.4
Front coverage: luts 1001..1845 (HV reference 4000); accuracy_bits 13.7..17 (HV reference 13); data_width on the front 19..22 (registry 8..28).

Per family:
- unrolled_k: 33 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 16.07 bits
- pipelined: 33 evals, 28 feasible; max throughput seen 273 MSPS; best accuracy 17.00 bits; best feasible luts=1001; feasible ranges: data_width 19..22, n_iter 16..24, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 34 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 17.04 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Refine the search space to the most promising region of the only feasible family.*)
- `pipelined` (100 evals): data_width=19..21, n_iter=16..20, angle_guard=-1..1, frac_guard=0..1, rounding=trunc|round. *Why:* Focus on the lowest LUT region of the feasible pipelined front to refine the trade-off curve and potentially find a design with <1001 LUTs that still meets accuracy and throughput constraints.

**Result (code):** 100 evaluations this round, 200 total; 127 feasible; hypervolume 1.107e+04 (+1.8%).

**LLM decision:** `refine` — The `pipelined` family is the only one meeting the throughput constraint (>=250 MSPS), while `unrolled_k` and `pipelined_m` failed completely (max 9.97 and 171 MSPS respectively). The current Pareto front is dominated by `pipelined` designs with `data_width` 19-22 and `n_iter` 16-24. To maximize hypervolume and find the true minimum LUT corner, we should focus the remaining budget on the `pipelined` family within these proven feasible ranges. Specifically, we will narrow `data_width` to 19-22, `n_iter` to 16-24, and keep `angle_guard` and `frac_guard` tight around the values that yielded the best LUT/accuracy trade-offs (e.g., `angle_guard` 0-2, `frac_guard` 0-1). This avoids wasting evaluations on infeasible families or out-of-range parameters that have already been shown to violate constraints or offer no benefit.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 1.107e+04 (gain this round: +1.8%).
Feasible designs: 127 of 200 evaluations (79 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 34% violate; best seen 273
- max_abs_err <= 0.00012207: 10% violate; best seen 7.43e-06 (2^-17.04)

Pareto front (feasible, 16 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=19 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts=1001, accuracy_bits=13.7, ffs=1033, throughput_msps=264, max_abs_err=7.72e-05 (2^-13.66), power_index=19.1
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] luts=1064, accuracy_bits=14.4, ffs=1098, throughput_msps=264, max_abs_err=4.64e-05 (2^-14.39), power_index=20.3
- pipelined [data_width=21 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts=1096, accuracy_bits=14.6, ffs=1130, throughput_msps=264, max_abs_err=4.14e-05 (2^-14.56), power_index=20.9
- pipelined [data_width=21 n_iter=16 angle_guard=2 frac_guard=0 rounding=round] luts=1128, accuracy_bits=14.7, ffs=1162, throughput_msps=257, max_abs_err=3.65e-05 (2^-14.74), power_index=21.5
- pipelined [data_width=21 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts=1188, accuracy_bits=14.8, ffs=1176, throughput_msps=264, max_abs_err=3.61e-05 (2^-14.76), power_index=22.2
- pipelined [data_width=21 n_iter=17 angle_guard=2 frac_guard=0 rounding=trunc] luts=1202, accuracy_bits=15, ffs=1235, throughput_msps=257, max_abs_err=3.12e-05 (2^-14.97), power_index=22.9
- pipelined [data_width=21 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc] luts=1236, accuracy_bits=15.4, ffs=1265, throughput_msps=257, max_abs_err=2.27e-05 (2^-15.43), power_index=23.5
- pipelined [data_width=21 n_iter=19 angle_guard=1 frac_guard=0 rounding=round] luts=1333, accuracy_bits=16.2, ffs=1361, throughput_msps=264, max_abs_err=1.29e-05 (2^-16.24), power_index=25.3
- pipelined [data_width=21 n_iter=19 angle_guard=1 frac_guard=1 rounding=round] luts=1415, accuracy_bits=16.5, ffs=1397, throughput_msps=264, max_abs_err=1.06e-05 (2^-16.52), power_index=26.4
- pipelined [data_width=22 n_iter=24 angle_guard=0 frac_guard=1 rounding=round] luts=1845, accuracy_bits=17, ffs=1814, throughput_msps=257, max_abs_err=7.63e-06 (2^-17.00), power_index=34.4
Front coverage: luts 1001..1845 (HV reference 4000); accuracy_bits 13.7..17 (HV reference 13); data_width on the front 19..22 (registry 8..28).

Per family:
- unrolled_k: 33 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 16.07 bits
- pipelined: 133 evals, 127 feasible; max throughput seen 273 MSPS; best accuracy 17.00 bits; best feasible luts=1001; feasible ranges: data_width 19..22, n_iter 16..24, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 34 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 17.04 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Focus exclusively on the feasible `pipelined` family within the ranges that produced feasible designs to maximize hypervolume gain and identify the optimal trade-off.*)
- `pipelined` (40 evals): data_width=19..22, n_iter=16..24, angle_guard=-1..2, frac_guard=0..1, rounding=trunc|round. *Why:* Only pipelined meets throughput; refining ranges around the known feasible region to map the Pareto front more densely and find the minimum LUT design.

**Result (code):** 40 evaluations this round, 240 total; 166 feasible; hypervolume 1.401e+04 (+26.5%).

**LLM decision:** `stop` — The feasible Pareto front is well-established and robust. The `pipelined` family dominates the solution space, with 166 feasible evaluations yielding a clear trade-off curve from 1001 LUTs (13.7 bits accuracy) to 1894 LUTs (18.2 bits accuracy). The minimum LUT design (1001 LUTs, 13.7 bits) comfortably satisfies the strict constraints: throughput of 264 MSPS (>= 250) and max error of 7.72e-05 (<= 0.00012207). Other families (`unrolled_k`, `pipelined_m`) failed to meet the throughput constraint, confirming `pipelined` as the only viable architecture. Since this is the final round and the front covers the relevant objective ranges with a clear selection candidate, further exploration would not improve the hypervolume or the final design choice.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 1.401e+04 (gain this round: +26.5%).
Feasible designs: 166 of 240 evaluations (106 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 28% violate; best seen 273
- max_abs_err <= 0.00012207: 9% violate; best seen 3.37e-06 (2^-18.18)

Pareto front (feasible, 18 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=19 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] luts=1001, accuracy_bits=13.7, ffs=1033, throughput_msps=264, max_abs_err=7.72e-05 (2^-13.66), power_index=19.1
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] luts=1064, accuracy_bits=14.4, ffs=1098, throughput_msps=264, max_abs_err=4.64e-05 (2^-14.39), power_index=20.3
- pipelined [data_width=21 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] luts=1112, accuracy_bits=14.6, ffs=1146, throughput_msps=264, max_abs_err=3.91e-05 (2^-14.64), power_index=21.2
- pipelined [data_width=21 n_iter=17 angle_guard=-1 frac_guard=0 rounding=round] luts=1152, accuracy_bits=14.7, ffs=1183, throughput_msps=264, max_abs_err=3.65e-05 (2^-14.74), power_index=22
- pipelined [data_width=22 n_iter=17 angle_guard=-1 frac_guard=0 rounding=trunc] luts=1202, accuracy_bits=15.2, ffs=1235, throughput_msps=264, max_abs_err=2.67e-05 (2^-15.19), power_index=22.9
- pipelined [data_width=22 n_iter=17 angle_guard=0 frac_guard=0 rounding=trunc] luts=1219, accuracy_bits=15.3, ffs=1252, throughput_msps=264, max_abs_err=2.44e-05 (2^-15.32), power_index=23.2
- pipelined [data_width=21 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] luts=1259, accuracy_bits=15.9, ffs=1289, throughput_msps=264, max_abs_err=1.68e-05 (2^-15.87), power_index=24
- pipelined [data_width=21 n_iter=19 angle_guard=1 frac_guard=1 rounding=round] luts=1415, accuracy_bits=16.5, ffs=1397, throughput_msps=264, max_abs_err=1.06e-05 (2^-16.52), power_index=26.4
- pipelined [data_width=22 n_iter=20 angle_guard=2 frac_guard=1 rounding=trunc] luts=1527, accuracy_bits=17.3, ffs=1550, throughput_msps=257, max_abs_err=6.11e-06 (2^-17.32), power_index=28.9
- pipelined [data_width=22 n_iter=24 angle_guard=2 frac_guard=1 rounding=round] luts=1894, accuracy_bits=18.2, ffs=1862, throughput_msps=257, max_abs_err=3.37e-06 (2^-18.18), power_index=35.3
Front coverage: luts 1001..1894 (HV reference 4000); accuracy_bits 13.7..18.2 (HV reference 13); data_width on the front 19..22 (registry 8..28).

Per family:
- unrolled_k: 33 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 16.07 bits
- pipelined: 173 evals, 166 feasible; max throughput seen 273 MSPS; best accuracy 18.18 bits; best feasible luts=1001; feasible ranges: data_width 19..22, n_iter 16..24, angle_guard -1..2, frac_guard 0..2
- pipelined_m: 34 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 17.04 bits
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined` (160 evals): data_width=18..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (18 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 269 feasible; hypervolume 1.703e+04 (+21.6%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and robust. The `pipelined` family dominates the solution space, with 166 feasible evaluations yielding a clear trade-off curve from 1001 LUTs (13.7 bits accuracy) to 1894 LUTs (18.2 bits accuracy). The minimum LUT design (1001 LUTs, 13.7 bits) comfortably satisfies the strict constraints: throughput of 264 MSPS (>= 250) and max error of 7.72e-05 (<= 0.00012207). Other families (`unrolled_k`, `pipelined_m`) failed to meet the throughput constraint, confirming `pipelined` as the only viable architecture. Since this is the final round and the front covers the relevant objective ranges with a clear selection candidate, further exploration would not improve the hypervolume or the final design choice.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 1.703e+04 (gain this round: +21.6%).
Feasible designs: 269 of 400 evaluations (193 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 30% violate; best seen 273
- max_abs_err <= 0.00012207: 7% violate; best seen 5.57e-08 (2^-24.10)

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=20 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts=979, accuracy_bits=13.6, ffs=1014, throughput_msps=264, max_abs_err=8.24e-05 (2^-13.57), power_index=18.7
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] luts=1064, accuracy_bits=14.4, ffs=1098, throughput_msps=264, max_abs_err=4.64e-05 (2^-14.39), power_index=20.3
- pipelined [data_width=21 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] luts=1112, accuracy_bits=14.6, ffs=1146, throughput_msps=264, max_abs_err=3.91e-05 (2^-14.64), power_index=21.2
- pipelined [data_width=21 n_iter=16 angle_guard=1 frac_guard=1 rounding=round] luts=1188, accuracy_bits=14.8, ffs=1176, throughput_msps=264, max_abs_err=3.61e-05 (2^-14.76), power_index=22.2
- pipelined [data_width=22 n_iter=17 angle_guard=1 frac_guard=0 rounding=round] luts=1236, accuracy_bits=15.6, ffs=1269, throughput_msps=257, max_abs_err=1.95e-05 (2^-15.64), power_index=23.6
- pipelined [data_width=21 n_iter=19 angle_guard=1 frac_guard=0 rounding=round] luts=1333, accuracy_bits=16.2, ffs=1361, throughput_msps=264, max_abs_err=1.29e-05 (2^-16.24), power_index=25.3
- pipelined [data_width=22 n_iter=18 angle_guard=1 frac_guard=2 rounding=round] luts=1431, accuracy_bits=16.6, ffs=1410, throughput_msps=257, max_abs_err=9.91e-06 (2^-16.62), power_index=26.7
- pipelined [data_width=22 n_iter=20 angle_guard=2 frac_guard=1 rounding=trunc] luts=1527, accuracy_bits=17.3, ffs=1550, throughput_msps=257, max_abs_err=6.11e-06 (2^-17.32), power_index=28.9
- pipelined [data_width=22 n_iter=21 angle_guard=2 frac_guard=1 rounding=round] luts=1653, accuracy_bits=18.1, ffs=1629, throughput_msps=257, max_abs_err=3.51e-06 (2^-18.12), power_index=30.9
- pipelined [data_width=24 n_iter=28 angle_guard=1 frac_guard=2 rounding=round] luts=2417, accuracy_bits=19.8, ffs=2367, throughput_msps=257, max_abs_err=1.06e-06 (2^-19.84), power_index=45
Front coverage: luts 979..2417 (HV reference 4000); accuracy_bits 13.6..19.8 (HV reference 13); data_width on the front 19..25 (registry 8..28).

Per family:
- unrolled_k: 33 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 16.07 bits
- pipelined: 333 evals, 269 feasible; max throughput seen 273 MSPS; best accuracy 24.10 bits; best feasible luts=979; feasible ranges: data_width 18..25, n_iter 15..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 34 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 17.04 bits
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 24009 in, 3147 out
- provider-reported cost: $0.0073
- full prompts and replies: `llm_trace.jsonl`

