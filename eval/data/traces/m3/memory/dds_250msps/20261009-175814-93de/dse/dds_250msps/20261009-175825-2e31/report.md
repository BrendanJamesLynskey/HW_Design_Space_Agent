# DSE run: dds_250msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
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
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined:data_width=19,n_iter=15,angle_guard=2,frac_guard=0,rounding=trunc` — selection: auto (spec rule: min luts)

| metric | value | provenance |
|---|---|---|
| luts | 964 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 999 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 264 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 64.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 18.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000109 (2^-13.17) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 14.2 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.9e-05 (2^-15.07) | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.8 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.2 | exact: bit-accurate model, dense (119307 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 17 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 96.8 dBc, SNR 87.8 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (11 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=19,n_iter=15,angle_guard=2,frac_guard=0,rounding=trunc` | 964 | 999 | 264.5 | 17 | 18.5 | 0.000109 (2^-13.17) | 13.17 |
| 1 | `pipelined:data_width=19,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc` | 1033 | 1065 | 264.5 | 18 | 19.7 | 8.56e-05 (2^-13.51) | 13.51 |
| 2 | `pipelined:data_width=19,n_iter=15,angle_guard=1,frac_guard=3,rounding=trunc` | 1038 | 1062 | 264.5 | 17 | 19.8 | 7.96e-05 (2^-13.62) | 13.62 |
| 3 | `pipelined:data_width=20,n_iter=15,angle_guard=3,frac_guard=1,rounding=trunc` | 1053 | 1086 | 256.5 | 17 | 20.1 | 7.32e-05 (2^-13.74) | 13.74 |
| 4 | `pipelined:data_width=22,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 1082 | 1120 | 256.5 | 17 | 20.7 | 6.35e-05 (2^-13.94) | 13.94 |
| 5 | `pipelined:data_width=22,n_iter=16,angle_guard=2,frac_guard=0,rounding=trunc` | 1175 | 1211 | 256.5 | 18 | 22.4 | 3.7e-05 (2^-14.72) | 14.72 |
| 6 | `pipelined:data_width=22,n_iter=16,angle_guard=0,frac_guard=4,rounding=round` | 1316 | 1293 | 256.5 | 18 | 24.5 | 3.42e-05 (2^-14.84) | 14.84 |
| 7 | `pipelined:data_width=21,n_iter=19,angle_guard=0,frac_guard=1,rounding=trunc` | 1352 | 1376 | 264.5 | 21 | 25.7 | 1.88e-05 (2^-15.70) | 15.70 |
| 8 | `pipelined:data_width=20,n_iter=18,angle_guard=3,frac_guard=4,rounding=round` | 1427 | 1402 | 256.5 | 20 | 26.6 | 1.13e-05 (2^-16.43) | 16.43 |
| 9 | `pipelined:data_width=22,n_iter=18,angle_guard=4,frac_guard=4,rounding=trunc` | 1510 | 1528 | 256.5 | 20 | 28.6 | 8.72e-06 (2^-16.81) | 16.81 |
| 10 | `pipelined:data_width=22,n_iter=18,angle_guard=4,frac_guard=4,rounding=round` | 1556 | 1530 | 256.5 | 20 | 29 | 8.31e-06 (2^-16.88) | 16.88 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The throughput constraint (>=250 MSPS, 1 sample/clock) forces a pipelined architecture. iterative is infeasible (N+3 cycles/result gives ~83 MSPS even at 1 GHz). unrolled_k is likely area-hungry for the same throughput and offers no accuracy advantage over pipelined_m, so it is excluded to concentrate the 100-eval budget. pipelined_m with m=1 is the natural 1-sample/clock family; allowing m up to 4 lets the search discover whether partial pipelining reduces area at acceptable latency. The parameter ranges are centred on the prior calibration (data_width ~16-18, n_iter ~14-16 for 2^-13) but widened to 14-20 and 12-18 so the Pareto front can be mapped on both the low-LUT/low-accuracy and high-accuracy sides. angle_guard and frac_guard are kept small (0-2) because the objective is min LUTs and the error budget is tight (2^-13); large guard widths would inflate area without helping the selection rule. All 100 evals go to pipelined_m since it is the only family that can plausibly satisfy both constraints; the reserved front-mapping portion of the budget will sweep m and the width/iter ranges to cover the full trade-off curve between LUTs and accuracy_bits.*)
- `pipelined_m` (60 evals): data_width=14..20, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* The spec demands 1 sample/clock at >=250 MSPS, which rules out iterative (N+3 cycles/result) and makes unrolled_k area-hungry. pipelined_m with m=1 is the canonical 1-result/cycle CORDIC; m=2..4 trade latency for fewer registers, potentially lowering LUT+FF area while keeping throughput at Fmax. data_width 14-20 and n_iter 12-18 bracket the 2^-13 accuracy requirement (accuracy_bits >= 13) with headroom on both sides so the Pareto front can trade accuracy_bits against LUTs. angle_guard 0-2 and frac_guard 0-2 keep the datapath narrow (minimising LUTs) while allowing enough guard bits to hit the error target. Rounding is included because round vs trunc shifts max_abs_err by up to ~1 LSB, which matters near the 2^-13 boundary.
- clamped by code: budget shares were all zero; split equally
- clamped by code: pipelined_m.m: clamped [1, 4] to [2, 4] (registry 2..8)

**Result (code):** 60 evaluations this round, 60 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `add_family` — Round 1 found 0 feasible designs. The pipelined_m family hit a hard throughput ceiling of 171 MSPS (52.3% below the 250 MSPS constraint) across all 60 evaluations, while accuracy was achievable (best 15.38 bits vs 13 required). The bottleneck is Fmax, not accuracy. The fully-registered pipelined family should have higher Fmax due to shorter combinational paths per stage. I will split the remaining 40 evaluations between pipelined (50%) to test if it can meet throughput, and pipelined_m (50%) with wider m range to see if different pipeline depths can also reach 250 MSPS. The data_width and n_iter ranges are narrowed around the promising region (16-22 and 14-20) where accuracy was already met, to focus the search on the Fmax/throughput dimension.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 60 evaluations (0 unique).
Families explored so far: pipelined_m. Not yet explored: iterative, unrolled_k, pipelined.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 100% violate; best seen 171
- max_abs_err <= 0.00012207: 45% violate; best seen 2.34e-05 (2^-15.38)

No feasible design found yet. Least-violating designs:
- pipelined_m [data_width=19 n_iter=17 angle_guard=2 frac_guard=0 rounding=round m=3]: throughput=119, max_abs_err=4.23e-05 (2^-14.53); throughput_msps >= 250 violated by 52.3%
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=0 rounding=trunc m=3]: throughput=119, max_abs_err=8.56e-05 (2^-13.51); throughput_msps >= 250 violated by 52.3%
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=3]: throughput=119, max_abs_err=5.84e-05 (2^-14.06); throughput_msps >= 250 violated by 52.3%
- pipelined_m [data_width=19 n_iter=16 angle_guard=0 frac_guard=2 rounding=trunc m=3]: throughput=119, max_abs_err=6.89e-05 (2^-13.83); throughput_msps >= 250 violated by 52.3%
- pipelined_m [data_width=19 n_iter=16 angle_guard=1 frac_guard=0 rounding=trunc m=3]: throughput=119, max_abs_err=8.56e-05 (2^-13.51); throughput_msps >= 250 violated by 52.3%

Per family:
- pipelined_m: 60 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.38 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 1 found 0 feasible designs. The pipelined_m family hit a hard throughput ceiling of 171 MSPS (52.3% below the 250 MSPS constraint) across all 60 evaluations, while accuracy was achievable (best 15.38 bits vs 13 required). The bottleneck is Fmax, not accuracy. The fully-registered pipelined family should have higher Fmax due to shorter combinational paths per stage. I will split the remaining 40 evaluations between pipelined (50%) to test if it can meet throughput, and pipelined_m (50%) with wider m range to see if different pipeline depths can also reach 250 MSPS. The data_width and n_iter ranges are narrowed around the promising region (16-22 and 14-20) where accuracy was already met, to focus the search on the Fmax/throughput dimension.*)
- `pipelined` (20 evals): data_width=16..22, n_iter=14..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* pipelined_m hit a throughput ceiling of 171 MSPS (52% short of 250) because its shared datapath limits Fmax. The fully-registered pipelined family has one stage per micro-rotation, which should push Fmax higher and reach the 250 MSPS throughput constraint while keeping LUTs low.
- `pipelined_m` (20 evals): data_width=16..22, n_iter=14..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Keep exploring pipelined_m with wider m range (2-8) and slightly wider data_width/n_iter to see if a different m or wider datapath can push Fmax above the 250 MSPS threshold. The previous search was stuck at m=3 with 171 MSPS; larger m reduces register count which may help Fmax, while smaller m increases pipeline depth which may hurt it.

**Result (code):** 40 evaluations this round, 100 total; 17 feasible; hypervolume 1.058e+04 (+inf).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 11 unique designs covering the trade-off between LUTs (964-1556) and accuracy (13.2-16.9 bits). The minimum LUT design (964 LUTs) meets all constraints (throughput 264 MSPS >= 250, max_abs_err 0.000109 <= 0.00012207). The front spans a meaningful range of accuracy bits above the 13-bit reference point, providing good hypervolume coverage. pipelined_m was explored but yielded no feasible designs (max throughput 171 MSPS), confirming that full pipelining (pipelined family) is necessary for the 250 MSPS throughput constraint. iterative and unrolled_k are not on the front and would have lower throughput due to multiple cycles per result, making them unlikely to meet the throughput constraint without excessive area. The budget is exhausted (100/100 evals, round 2 of 4 but budget cap reached), so further exploration is not possible. The current front provides a solid basis for selecting the final design (min LUTs = 964).

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.058e+04 (gain this round: +inf (first feasible designs)).
Feasible designs: 17 of 100 evaluations (16 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: iterative, unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 250: 80% violate; best seen 273
- max_abs_err <= 0.00012207: 41% violate; best seen 8.31e-06 (2^-16.88)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min luts, max accuracy_bits
- pipelined [data_width=19 n_iter=15 angle_guard=2 frac_guard=0 rounding=trunc] luts=964, accuracy_bits=13.2, ffs=999, throughput_msps=264, max_abs_err=0.000109 (2^-13.17), power_index=18.5
- pipelined [data_width=19 n_iter=16 angle_guard=2 frac_guard=0 rounding=trunc] luts=1033, accuracy_bits=13.5, ffs=1065, throughput_msps=264, max_abs_err=8.56e-05 (2^-13.51), power_index=19.7
- pipelined [data_width=19 n_iter=15 angle_guard=1 frac_guard=3 rounding=trunc] luts=1038, accuracy_bits=13.6, ffs=1062, throughput_msps=264, max_abs_err=7.96e-05 (2^-13.62), power_index=19.8
- pipelined [data_width=20 n_iter=15 angle_guard=3 frac_guard=1 rounding=trunc] luts=1053, accuracy_bits=13.7, ffs=1086, throughput_msps=257, max_abs_err=7.32e-05 (2^-13.74), power_index=20.1
- pipelined [data_width=22 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts=1082, accuracy_bits=13.9, ffs=1120, throughput_msps=257, max_abs_err=6.35e-05 (2^-13.94), power_index=20.7
- pipelined [data_width=22 n_iter=16 angle_guard=0 frac_guard=4 rounding=round] luts=1316, accuracy_bits=14.8, ffs=1293, throughput_msps=257, max_abs_err=3.42e-05 (2^-14.84), power_index=24.5
- pipelined [data_width=21 n_iter=19 angle_guard=0 frac_guard=1 rounding=trunc] luts=1352, accuracy_bits=15.7, ffs=1376, throughput_msps=264, max_abs_err=1.88e-05 (2^-15.70), power_index=25.7
- pipelined [data_width=20 n_iter=18 angle_guard=3 frac_guard=4 rounding=round] luts=1427, accuracy_bits=16.4, ffs=1402, throughput_msps=257, max_abs_err=1.13e-05 (2^-16.43), power_index=26.6
- pipelined [data_width=22 n_iter=18 angle_guard=4 frac_guard=4 rounding=trunc] luts=1510, accuracy_bits=16.8, ffs=1528, throughput_msps=257, max_abs_err=8.72e-06 (2^-16.81), power_index=28.6
- pipelined [data_width=22 n_iter=18 angle_guard=4 frac_guard=4 rounding=round] luts=1556, accuracy_bits=16.9, ffs=1530, throughput_msps=257, max_abs_err=8.31e-06 (2^-16.88), power_index=29
Front coverage: luts 964..1556 (HV reference 4000); accuracy_bits 13.2..16.9 (HV reference 13); data_width on the front 19..22 (registry 8..28).

Per family:
- pipelined: 20 evals, 17 feasible; max throughput seen 273 MSPS; best accuracy 16.88 bits; best feasible luts=964; feasible ranges: data_width 19..22, n_iter 15..19, angle_guard 0..4, frac_guard 0..4
- pipelined_m: 80 evals, 0 feasible; max throughput seen 171 MSPS; best accuracy 15.38 bits
```
</details>

## LLM usage
- calls: 6 (failed/unparsed attempts: 0)
- tokens: 25403 in, 2570 out
- provider-reported cost: $0.0051
- full prompts and replies: `llm_trace.jsonl`

