# DSE run: dds_250msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 200 of 200 budgeted, over 2 round(s).  
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
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=2,rounding=round` — selection: auto (spec rule: min luts)

| metric | value | provenance |
|---|---|---|
| luts | 1002 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 993 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 64.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 18.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 9.56e-05 (2^-13.35) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 6.27 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.69e-05 (2^-15.18) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.76 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.4 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 17 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 100.6 dBc, SNR 88.4 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (18 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=2,rounding=round` | 1002 | 993 | 264.5 | 17 | 18.8 | 9.56e-05 (2^-13.35) | 13.35 |
| 1 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 1017 | 1008 | 264.5 | 17 | 19 | 8.26e-05 (2^-13.56) | 13.56 |
| 2 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=3,rounding=round` | 1046 | 1034 | 264.5 | 17 | 19.6 | 8.08e-05 (2^-13.60) | 13.60 |
| 3 | `pipelined:data_width=19,n_iter=15,angle_guard=1,frac_guard=2,rounding=round` | 1048 | 1038 | 264.5 | 17 | 19.6 | 7.76e-05 (2^-13.65) | 13.65 |
| 4 | `pipelined:data_width=19,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 1063 | 1053 | 264.5 | 17 | 19.9 | 7.18e-05 (2^-13.77) | 13.77 |
| 5 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 1086 | 1076 | 264.5 | 18 | 20.3 | 5.46e-05 (2^-14.16) | 14.16 |
| 6 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=3,rounding=round` | 1118 | 1104 | 264.5 | 18 | 20.9 | 5.03e-05 (2^-14.28) | 14.28 |
| 7 | `pipelined:data_width=19,n_iter=16,angle_guard=1,frac_guard=2,rounding=round` | 1120 | 1108 | 264.5 | 18 | 21 | 5.03e-05 (2^-14.28) | 14.28 |
| 8 | `pipelined:data_width=19,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 1136 | 1124 | 264.5 | 18 | 21.3 | 4.29e-05 (2^-14.51) | 14.51 |
| 9 | `pipelined:data_width=20,n_iter=16,angle_guard=1,frac_guard=2,rounding=round` | 1170 | 1156 | 264.5 | 18 | 21.9 | 3.84e-05 (2^-14.67) | 14.67 |
| 10 | `pipelined:data_width=20,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 1185 | 1172 | 264.5 | 18 | 22.2 | 3.61e-05 (2^-14.76) | 14.76 |
| 11 | `pipelined:data_width=19,n_iter=17,angle_guard=2,frac_guard=2,rounding=round` | 1209 | 1195 | 264.5 | 19 | 22.6 | 2.76e-05 (2^-15.14) | 15.14 |
| 12 | `pipelined:data_width=20,n_iter=17,angle_guard=1,frac_guard=2,rounding=round` | 1244 | 1229 | 264.5 | 19 | 23.3 | 2.32e-05 (2^-15.40) | 15.40 |
| 13 | `pipelined:data_width=20,n_iter=17,angle_guard=2,frac_guard=2,rounding=round` | 1261 | 1246 | 264.5 | 19 | 23.6 | 2.23e-05 (2^-15.45) | 15.45 |
| 14 | `pipelined:data_width=19,n_iter=18,angle_guard=2,frac_guard=3,rounding=round` | 1317 | 1297 | 264.5 | 20 | 24.6 | 2.1e-05 (2^-15.54) | 15.54 |
| 15 | `pipelined:data_width=20,n_iter=18,angle_guard=1,frac_guard=2,rounding=round` | 1319 | 1302 | 264.5 | 20 | 24.6 | 1.92e-05 (2^-15.67) | 15.67 |
| 16 | `pipelined:data_width=20,n_iter=18,angle_guard=2,frac_guard=2,rounding=round` | 1337 | 1320 | 264.5 | 20 | 25 | 1.51e-05 (2^-16.01) | 16.01 |
| 17 | `pipelined:data_width=20,n_iter=18,angle_guard=2,frac_guard=3,rounding=round` | 1373 | 1352 | 256.5 | 20 | 25.6 | 1.32e-05 (2^-16.21) | 16.21 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands 1 sample/clock at >=250 MSPS, which rules out `iterative` (1 result per n_iter cycles) outright, so I exclude it. The accuracy target (max_abs_err <= 2^-13) pins n_iter around 12-14 and data_width around 14-18, since accuracy depends only on those plus the guards and rounding. The objective is min LUTs with a secondary max accuracy_bits, so the interesting trade-off is area (LUTs/FFs) vs accuracy near the 2^-13 boundary. `pipelined_m` is the natural fit (1 result/cycle, tunable register density via m) and prior campaigns located the front there, so it gets the largest share (55%). `pipelined` (m=1) gets 25% as a clean reference and to ensure the low-latency/high-FF corner is well sampled. `unrolled_k` gets 20% as a focused check on whether a shared-FSM unrolled design can beat the pipelined front on LUTs. All three share identical accuracy-relevant ranges so their results are directly comparable on the Pareto front. angle_guard and frac_guard are kept small (low values) to minimise the atan-LUT and datapath width, consistent with the min-LUT objective, while still allowing the search to find the accuracy sweet spot.*)
- `pipelined_m` (55 evals): data_width=14..18, n_iter=12..14, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Primary candidate: 1 result/cycle meets throughput, and register-every-m stages trades area (LUTs/FFs) against latency/Fmax. Prior campaigns found the front here with m=4..7, dw=15..20, n_iter=12..13. I widen m down to 1 (plain pipelined is a special case of m=1) and keep dw 14..18 / n_iter 12..14 to cover the accuracy-vs-area trade-off near the 2^-13 boundary. Small angle_guard/frac_guard keep the atan-LUT and datapath narrow to minimise LUTs.
- `pipelined` (25 evals): data_width=14..18, n_iter=12..14, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Full per-stage pipelining is the m=1 limit of pipelined_m; searching it explicitly guards against the m=1 corner being under-sampled and gives a clean reference point on the front (lowest latency, highest FF count). Same accuracy-relevant ranges as pipelined_m so results are directly comparable.
- `unrolled_k` (20 evals): data_width=14..18, n_iter=12..14, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=2..8. *Why:* Secondary check: unrolled_k with large k (k>=n_iter) can also reach 1 result/cycle with a shared FSM and fewer pipeline registers, potentially beating pipelined_m on LUTs. Prior campaigns said it never reached a front, but that was with different ranges; a focused slice (k 2..8, dw 14..18, n_iter 12..14) is cheap insurance to confirm or refute whether it can undercut the pipelined front on the min-LUT objective.
- clamped by code: pipelined_m.m: clamped [1, 4] to [2, 4] (registry 2..8)

**Result (code):** 100 evaluations this round, 100 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `refine` — The primary bottleneck is accuracy: 100% of evaluations violated max_abs_err <= 2^-13, with the best seen being 2^-12.64 (pipelined, W=18, N=14, ag=1, fg=2, round). Throughput is also tight (75% violate), with the best seen at 273 MSPS (same design family/params). The pipelined family is the only one capable of meeting the throughput constraint (max 273 MSPS vs 12 for unrolled_k and 171 for pipelined_m), so we must focus there. To improve accuracy, we need to increase n_iter (more micro-rotations reduce error) and potentially increase data_width or angle_guard. However, increasing n_iter increases latency and may reduce Fmax, hurting throughput. The current best (N=14) is close but not enough. We should explore higher N (15-18) with W=18-20, ag=1-2, fg=2-3, rounding=round, while keeping the design lean to maintain Fmax > 250 MHz. We also need to ensure Fmax stays high enough; W=18 seems to be the sweet spot for area vs Fmax. Let's narrow the search to pipelined with W=18-20, N=15-18, ag=1-2, fg=2-3, rounding=round.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 75% violate; best seen 273
- max_abs_err <= 0.00012207: 100% violate; best seen 0.000157 (2^-12.64)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=2 rounding=round]: throughput=264, max_abs_err=0.000157 (2^-12.64); max_abs_err <= 0.00012207 violated by 28.3%
- pipelined [data_width=18 n_iter=14 angle_guard=-1 frac_guard=2 rounding=round]: throughput=264, max_abs_err=0.00024 (2^-12.03); max_abs_err <= 0.00012207 violated by 96.2%
- pipelined [data_width=18 n_iter=13 angle_guard=2 frac_guard=2 rounding=round]: throughput=264, max_abs_err=0.000266 (2^-11.88); max_abs_err <= 0.00012207 violated by 117.7%
- pipelined [data_width=18 n_iter=13 angle_guard=1 frac_guard=2 rounding=round]: throughput=264, max_abs_err=0.000272 (2^-11.84); max_abs_err <= 0.00012207 violated by 123.2%
- pipelined [data_width=18 n_iter=13 angle_guard=1 frac_guard=0 rounding=round]: throughput=264, max_abs_err=0.000289 (2^-11.76); max_abs_err <= 0.00012207 violated by 136.3%

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 12.26 bits
- pipelined: 25 evals, 0 feasible; max throughput seen 273 MSPS; best accuracy 12.64 bits
- pipelined_m: 55 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 11.84 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Narrowing to pipelined with higher n_iter to meet accuracy constraint while maintaining throughput.*)
- `pipelined` (100 evals): data_width=18..20, n_iter=15..18, angle_guard=1..2, frac_guard=2..3, rounding=round. *Why:* Focus on pipelined (only family meeting throughput) with higher n_iter (15-18) to push accuracy below 2^-13, while keeping W=18-20 and ag/fg moderate to preserve Fmax.

**Result (code):** 100 evaluations this round, 200 total; 100 feasible; hypervolume 9072 (+inf).

**LLM decision:** `stop` — The budget (200/200 evals) and round cap (4/4) are exhausted, so this is the final round. The `pipelined` family successfully mapped a feasible Pareto front (18 designs) that satisfies both constraints: throughput >= 250 MSPS (best 273, front range 257-264) and max_abs_err <= 2^-13 (front range 13.4-16.2 bits). The front spans a useful trade-off space from 1002 LUTs/13.4 bits to 1373 LUTs/16.2 bits, providing a clear selection path for the 'min luts' objective. Other families (`unrolled_k`, `pipelined_m`) failed to meet the throughput constraint, confirming `pipelined` is the only viable architecture for this spec. No further exploration is possible or needed.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 9072 (gain this round: +inf (first feasible designs)).
Feasible designs: 100 of 200 evaluations (38 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 38% violate; best seen 273
- max_abs_err <= 0.00012207: 50% violate; best seen 1.32e-05 (2^-16.21)

Pareto front (feasible, 18 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=2 rounding=round] luts=1002, accuracy_bits=13.4, ffs=993, throughput_msps=264, max_abs_err=9.56e-05 (2^-13.35), power_index=18.8
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=3 rounding=round] luts=1046, accuracy_bits=13.6, ffs=1034, throughput_msps=264, max_abs_err=8.08e-05 (2^-13.60), power_index=19.6
- pipelined [data_width=19 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] luts=1063, accuracy_bits=13.8, ffs=1053, throughput_msps=264, max_abs_err=7.18e-05 (2^-13.77), power_index=19.9
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=3 rounding=round] luts=1118, accuracy_bits=14.3, ffs=1104, throughput_msps=264, max_abs_err=5.03e-05 (2^-14.28), power_index=20.9
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts=1136, accuracy_bits=14.5, ffs=1124, throughput_msps=264, max_abs_err=4.29e-05 (2^-14.51), power_index=21.3
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] luts=1170, accuracy_bits=14.7, ffs=1156, throughput_msps=264, max_abs_err=3.84e-05 (2^-14.67), power_index=21.9
- pipelined [data_width=19 n_iter=17 angle_guard=2 frac_guard=2 rounding=round] luts=1209, accuracy_bits=15.1, ffs=1195, throughput_msps=264, max_abs_err=2.76e-05 (2^-15.14), power_index=22.6
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=2 rounding=round] luts=1261, accuracy_bits=15.5, ffs=1246, throughput_msps=264, max_abs_err=2.23e-05 (2^-15.45), power_index=23.6
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=2 rounding=round] luts=1319, accuracy_bits=15.7, ffs=1302, throughput_msps=264, max_abs_err=1.92e-05 (2^-15.67), power_index=24.6
- pipelined [data_width=20 n_iter=18 angle_guard=2 frac_guard=3 rounding=round] luts=1373, accuracy_bits=16.2, ffs=1352, throughput_msps=257, max_abs_err=1.32e-05 (2^-16.21), power_index=25.6
Front coverage: luts 1002..1373 (HV reference 4000); accuracy_bits 13.4..16.2 (HV reference 13); data_width on the front 18..20 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 12 MSPS; best accuracy 12.26 bits
- pipelined: 125 evals, 100 feasible; max throughput seen 273 MSPS; best accuracy 16.21 bits; best feasible luts=1002; feasible ranges: data_width 18..20, n_iter 15..18, angle_guard 1..2, frac_guard 2..3
- pipelined_m: 55 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 11.84 bits
```
</details>

## LLM usage
- calls: 6 (failed/unparsed attempts: 0)
- tokens: 25492 in, 2874 out
- provider-reported cost: $0.0062
- full prompts and replies: `llm_trace.jsonl`

