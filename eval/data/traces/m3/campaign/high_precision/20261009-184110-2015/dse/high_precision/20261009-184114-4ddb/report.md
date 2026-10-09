# DSE run: high_precision

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 400 of 400 budgeted, over 4 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec high_precision: Coherent demodulator for a precision instrument: max error <= 2^-20 at >= 50 MSPS. Minimise area (LUTs + FFs) and the relative power index.
  constraint: throughput_msps >= 50
  constraint: max_abs_err <= 9.53674e-07
  objective: min luts_plus_ffs (HV ref 8000)
  objective: min power_index (HV ref 20)
  select: min luts_plus_ffs
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=27,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc,m=7` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 1930 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 410 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 52 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 52 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 115 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 4.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 7.54e-07 (2^-20.34) | exact: bit-accurate model, dense (131024 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 25.3 | exact: bit-accurate model, dense (131024 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.12e-07 (2^-22.17) | exact: bit-accurate model, dense (131024 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 7.11 | exact: bit-accurate model, dense (131024 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 20.3 | exact: bit-accurate model, dense (131024 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 142.3 dBc, SNR 130.5 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (1 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=27,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc,m=7` | 1930 | 410 | 52.0 | 6 | 4.4 | 7.54e-07 (2^-20.34) | 20.34 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands max_abs_err <= 2^-20 (~9.54e-7) at >=50 MSPS, while minimising LUTs+FFs and power. Accuracy depends only on data_width, n_iter, angle_guard, frac_guard and rounding. From the output LSB = 2^-(W-2), W=23 gives LSB=4.77e-7 and is likely too coarse; W=24 (LSB=2.38e-7) is borderline; W>=25 is safe. Similarly, CORDIC angle error ~2^-N means N>=22 is likely needed. The ranges therefore focus on W=23..27 and N=20..26 to locate the minimum feasible values. Throughput rules out iterative: its throughput is Fmax/(N+3), so even at N=20 and Fmax=200 MHz it yields <10 MSPS, far below 50. Unrolled_k can reach 50 MSPS only with high Fmax and large k, but it replicates datapath hardware, inflating LUTs. Pipelined and pipelined_m both give 1 result/cycle, so they meet 50 MSPS as long as Fmax>=50. Pipelined_m is the most promising for area because increasing m reduces flip-flops while the relaxed throughput requirement allows the resulting Fmax drop. The first round therefore allocates 60% to pipelined_m, 20% to pipelined (baseline m=1), and 20% to unrolled_k (to confirm whether it can compete). Iterative is omitted as mathematically infeasible for the required accuracy and throughput.*)
- `pipelined_m` (60 evals): data_width=23..27, n_iter=20..26, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* Primary family for area minimisation. It produces 1 result/cycle, so the 50 MSPS throughput constraint is easily met even if Fmax is reduced by registering every m stages. Increasing m cuts flip-flop count (fewer pipeline registers) at the cost of Fmax; since only 50 MSPS is required, we can trade Fmax for area. The ranges cover the critical accuracy region (W=23..27, N=20..26) and allow the search to find the smallest W/N/guards that still meet max_abs_err <= 2^-20, while m=2..8 explores the area-vs-Fmax trade-off.
- `pipelined` (20 evals): data_width=23..27, n_iter=20..26, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* Baseline fully pipelined design (m=1). It has the highest Fmax but also the most flip-flops. Included to provide a reference point for area and power, and to check whether the extra registers are ever justified by a lower LUT count or better power index. The accuracy ranges are identical to pipelined_m so the comparison is fair.
- `unrolled_k` (20 evals): data_width=23..27, n_iter=20..26, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, k=2..8. *Why:* Included to verify whether a partially unrolled datapath can meet the 50 MSPS constraint with a smaller area than pipelined_m. It uses k micro-rotation units per cycle, which tends to increase LUTs, but it may achieve the required throughput with fewer pipeline registers. The k range 2..8 covers the trade-off between cycles per result and hardware replication. A smaller budget is allocated because its area profile is expected to be worse than pipelined_m for this throughput-constrained, area-minimising spec.

**Result (code):** 100 evaluations this round, 100 total; 56 feasible; hypervolume 8.737e+04 (n/a).

**LLM decision:** `map_front` — The feasible front is a single point (pipelined_m [26,23,1,0,trunc,m=7], luts_plus_ffs=2375, power_index=4.47), so it covers only 2375..2375 of the 8000 area reference and 4.47..4.47 of the 20 power reference — the reported HV (8.737e4) is just that one rectangle, i.e. essentially zero coverage of the trade-off curve. Yet the round shows real spread to exploit: pipelined reaches 257 MSPS (vs 52 for the front point) and pipelined_m spans m 2..7 with feasible data_width 25..27, n_iter 22..26, angle_guard -1..2, frac_guard 0..3, so a proper NSGA-II sweep over the full ranges of the families on the front should fill in the area/power/throughput curve. iterative is not worth adding: it issues 1 micro-rotation/cycle (slower than unrolled_k, which already topped out at 7.17 MSPS and 0 feasible), so it cannot reach the 50 MSPS constraint. Handing this round to code-driven front mapping is the highest-value use of the remaining budget.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 8.737e+04 (gain this round: n/a (first round)).
Feasible designs: 56 of 100 evaluations (48 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 25% violate; best seen 257
- max_abs_err <= 9.53674e-07: 40% violate; best seen 1.72e-07 (2^-22.47)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=26 n_iter=23 angle_guard=1 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=2375, power_index=4.47, luts=1976, ffs=400, throughput_msps=52, max_abs_err=9.02e-07 (2^-20.08)
Front coverage: luts_plus_ffs 2375..2375 (HV reference 8000); power_index 4.47..4.47 (HV reference 20); data_width on the front 26..26 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 7.17 MSPS; best accuracy 20.73 bits
- pipelined: 20 evals, 14 feasible; max throughput seen 257 MSPS; best accuracy 22.06 bits; best feasible luts_plus_ffs=3839; feasible ranges: data_width 25..27, n_iter 22..26, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 60 evals, 42 feasible; max throughput seen 158 MSPS; best accuracy 22.47 bits; best feasible luts_plus_ffs=2375; feasible ranges: data_width 25..27, n_iter 22..26, angle_guard -1..2, frac_guard 0..3, m 2..7
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=25..28, n_iter=21..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 129 feasible; hypervolume 8.737e+04 (+0.0%).

**LLM decision:** `map_front` — The feasible Pareto front is a single point (pipelined_m data_width=26 n_iter=23 angle_guard=1 frac_guard=0 rounding=trunc m=7 at luts_plus_ffs=2375, power_index=4.47), covering only 2375..2375 of the 8000 area reference and 4.47..4.47 of the 20 power reference, and hypervolume gain this round was +0.0%. With 115 feasible pipelined_m designs collapsing to one non-dominated point, the trade-off curve is essentially unmapped, so the budget is best spent on a code-driven coverage search over the full ranges of the families on the front (pipelined_m, and pipelined which reached 257 MSPS and best feasible luts_plus_ffs=3839) seeded with the current front. The unexplored iterative family is not worth a round: at 1 micro-rotation/cycle it needs Fmax ~= 50*(N+3) MHz (e.g. ~1300 MHz at N=23) to reach the 50 MSPS constraint, which is unreachable, and unrolled_k already showed 0 feasible designs with max throughput 7.17 MSPS. The accuracy constraint (max_abs_err <= 9.53674e-07) is tight but satisfiable (best seen 3.07e-08), so the problem is feasible and only needs better front coverage.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 8.737e+04 (gain this round: +0.0%).
Feasible designs: 129 of 200 evaluations (113 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 17% violate; best seen 257
- max_abs_err <= 9.53674e-07: 30% violate; best seen 3.07e-08 (2^-24.96)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=26 n_iter=23 angle_guard=1 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=2375, power_index=4.47, luts=1976, ffs=400, throughput_msps=52, max_abs_err=9.02e-07 (2^-20.08)
Front coverage: luts_plus_ffs 2375..2375 (HV reference 8000); power_index 4.47..4.47 (HV reference 20); data_width on the front 26..26 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 7.17 MSPS; best accuracy 20.73 bits
- pipelined: 20 evals, 14 feasible; max throughput seen 257 MSPS; best accuracy 22.06 bits; best feasible luts_plus_ffs=3839; feasible ranges: data_width 25..27, n_iter 22..26, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 160 evals, 115 feasible; max throughput seen 158 MSPS; best accuracy 24.96 bits; best feasible luts_plus_ffs=2375; feasible ranges: data_width 25..28, n_iter 22..30, angle_guard -1..4, frac_guard 0..4, m 2..7
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=25..28, n_iter=21..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 300 total; 193 feasible; hypervolume 8.829e+04 (+1.1%).

**LLM decision:** `map_front` — The feasible front has collapsed to a single design (pipelined_m, luts_plus_ffs=2340, power_index=4.4), so hypervolume coverage is poor: luts_plus_ffs spans only 2340..2340 against an HV reference of 8000, and power_index only 4.4..4.4 against 20. The constraint is throughput >= 50 MSPS, and the lone front point sits right at 52 MSPS, meaning the true trade-off curve (cheaper/slower vs. faster/pricier) is almost certainly under-sampled. pipelined_m already shows 179 feasible designs with best accuracy 24.96 bits and best area 2340, so there is room to trade area against power/throughput across the full parameter ranges. With 100 evals left in the final round, a code-driven NSGA-II coverage search over the full ranges of pipelined_m (and pipelined, which also produced 14 feasible designs) seeded with the current front is the best use of budget to map the whole Pareto curve before selection.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 8.829e+04 (gain this round: +1.1%).
Feasible designs: 193 of 300 evaluations (168 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 15% violate; best seen 257
- max_abs_err <= 9.53674e-07: 29% violate; best seen 3.07e-08 (2^-24.96)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=27 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=2340, power_index=4.4, luts=1930, ffs=410, throughput_msps=52, max_abs_err=7.54e-07 (2^-20.34)
Front coverage: luts_plus_ffs 2340..2340 (HV reference 8000); power_index 4.4..4.4 (HV reference 20); data_width on the front 27..27 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 7.17 MSPS; best accuracy 20.73 bits
- pipelined: 20 evals, 14 feasible; max throughput seen 257 MSPS; best accuracy 22.06 bits; best feasible luts_plus_ffs=3839; feasible ranges: data_width 25..27, n_iter 22..26, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 260 evals, 179 feasible; max throughput seen 158 MSPS; best accuracy 24.96 bits; best feasible luts_plus_ffs=2340; feasible ranges: data_width 25..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=26..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 261 feasible; hypervolume 8.829e+04 (+0.0%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4) and the last round produced no hypervolume gain (+0.0%). The spec is satisfiable: 261 of 400 evaluations are feasible, and the front holds pipelined_m [W=27, N=22, angle_guard=0, frac_guard=0, trunc, m=7] at luts_plus_ffs=2340, power_index=4.4, throughput 52 MSPS (>= 50) and max_abs_err 7.54e-07 (2^-20.34, within the 2^-20 bound), which is also the min-area selection pick. Coverage is narrow (luts_plus_ffs and power_index each span a single point, data_width 27 only), but with no evaluations left there is nothing further to map; iterative was never explored, yet unrolled_k (its closest relative, 1 result per several cycles) reached only 7.17 MSPS with 0 feasible designs, so it cannot plausibly beat the 50 MSPS constraint. Stopping with the feasible front as-is.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 8.829e+04 (gain this round: +0.0%).
Feasible designs: 261 of 400 evaluations (231 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 14% violate; best seen 257
- max_abs_err <= 9.53674e-07: 28% violate; best seen 3.07e-08 (2^-24.96)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=27 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=2340, power_index=4.4, luts=1930, ffs=410, throughput_msps=52, max_abs_err=7.54e-07 (2^-20.34)
Front coverage: luts_plus_ffs 2340..2340 (HV reference 8000); power_index 4.4..4.4 (HV reference 20); data_width on the front 27..27 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 7.17 MSPS; best accuracy 20.73 bits
- pipelined: 20 evals, 14 feasible; max throughput seen 257 MSPS; best accuracy 22.06 bits; best feasible luts_plus_ffs=3839; feasible ranges: data_width 25..27, n_iter 22..26, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 360 evals, 247 feasible; max throughput seen 158 MSPS; best accuracy 24.96 bits; best feasible luts_plus_ffs=2340; feasible ranges: data_width 25..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 27069 in, 13921 out
- provider-reported cost: $0.0157
- full prompts and replies: `llm_trace.jsonl`

