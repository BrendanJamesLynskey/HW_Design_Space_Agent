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
`pipelined_m:data_width=27,n_iter=22,angle_guard=-1,frac_guard=0,rounding=round,m=7` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 1908 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 406 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 52 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 52 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 115 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 4.35 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 9.53e-07 (2^-20.00) | exact: bit-accurate model, dense (131024 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 32 | exact: bit-accurate model, dense (131024 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.22e-07 (2^-22.10) | exact: bit-accurate model, dense (131024 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 7.45 | exact: bit-accurate model, dense (131024 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 20 | exact: bit-accurate model, dense (131024 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 144.6 dBc, SNR 130.3 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (1 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=27,n_iter=22,angle_guard=-1,frac_guard=0,rounding=round,m=7` | 1908 | 406 | 52.0 | 6 | 4.35 | 9.53e-07 (2^-20.00) | 20.00 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands max_abs_err <= 2^-20 and >=50 MSPS. Iterative is excluded because with N>=20 (needed for 2^-20 angle resolution) it takes N+3 >= 23 cycles/result, so meeting 50 MSPS would require Fmax > 1.15 GHz, which is infeasible on Artix-7. Pipelined and pipelined_m give 1 result/cycle, so throughput = Fmax and the 50 MSPS constraint is easily satisfied; they are the most promising for the min-area objective. unrolled_k is included because it can also reach 50 MSPS if k is large, but it is less certain. For all families we start with data_width 22..26 (22 is the minimum for LSB 2^-20, higher values add margin), n_iter 20..26 (20 is the minimum for angle resolution, higher values add margin), and small angle_guard/frac_guard 0..2 to keep area low while allowing extra precision. Rounding is fixed to 'round' because it improves accuracy at small area cost. This first round (100 evals) will locate the feasible region and initial Pareto front; later rounds can expand ranges if needed.*)
- `pipelined` (30 evals): data_width=22..26, n_iter=20..26, angle_guard=0..2, frac_guard=0..2, rounding=round. *Why:* Pipelined gives 1 result/cycle, so throughput = Fmax and the >=50 MSPS constraint is easily met. Area is dominated by N stages and W; we search moderate W/N with small guards to find the minimum-area point that still meets the 2^-20 error bound. Rounding is fixed to 'round' because it improves accuracy at negligible area cost.
- `pipelined_m` (40 evals): data_width=22..26, n_iter=20..26, angle_guard=0..2, frac_guard=0..2, rounding=round, m=2..8. *Why:* pipelined_m also gives 1 result/cycle, so throughput = Fmax and the 50 MSPS constraint is safe. It can reduce flip-flop count by registering every m stages, which directly targets the min luts_plus_ffs objective. We search m from 2 to 8; larger m lowers area but may reduce Fmax, so we need to map the trade-off. Same accuracy-critical parameters as pipelined.
- `unrolled_k` (30 evals): data_width=22..26, n_iter=20..26, angle_guard=0..2, frac_guard=0..2, rounding=round, k=6..8. *Why:* unrolled_k can meet the 50 MSPS constraint only if k is large enough: with N~24, k=6 gives ~7 cycles/result and k=8 gives ~6 cycles/result, requiring Fmax around 300-350 MHz. This is plausible on Artix-7 but tighter than pipelined. We restrict k to 6..8 to focus on throughput-feasible designs. It may offer a different area/power trade-off than the pipelined families.

**Result (code):** 100 evaluations this round, 100 total; 20 feasible; hypervolume 8.462e+04 (n/a).

**LLM decision:** `map_front` — Only 1 feasible design reached the Pareto front (pipelined_m, luts_plus_ffs=2481, power_index=4.67), so the front covers a single point of both objective ranges (2481..2481 vs HV ref 8000; 4.67..4.67 vs ref 20). pipelined_m clearly dominates on area (best feasible 2481 vs pipelined's 3879) and both pipelined/pipelined_m have wide feasible ranges (data_width 24..26, n_iter 23..26, angle_guard 0..2, frac_guard 0..2, m 2..7) that are far from exhausted, while unrolled_k is throughput-starved (max 6.55 MSPS) and iterative is untested but inherently slow (N+3 cycles/result). With 300 evals left and 3 rounds, the best use of this round is a code-driven NSGA-II coverage search over the full ranges of pipelined and pipelined_m (the families on the front), seeded with the current front, to map the whole trade-off curve before refining.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 8.462e+04 (gain this round: n/a (first round)).
Feasible designs: 20 of 100 evaluations (13 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 31% violate; best seen 257
- max_abs_err <= 9.53674e-07: 77% violate; best seen 2.45e-07 (2^-21.96)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=24 n_iter=24 angle_guard=2 frac_guard=2 rounding=round m=7] luts_plus_ffs=2481, power_index=4.67, luts=2092, ffs=389, throughput_msps=54.3, max_abs_err=7.24e-07 (2^-20.40)
Front coverage: luts_plus_ffs 2481..2481 (HV reference 8000); power_index 4.67..4.67 (HV reference 20); data_width on the front 24..24 (registry 8..28).

Per family:
- unrolled_k: 30 evals, 0 feasible; max throughput seen 6.55 MSPS; best accuracy 21.00 bits
- pipelined: 30 evals, 12 feasible; max throughput seen 257 MSPS; best accuracy 21.38 bits; best feasible luts_plus_ffs=3879; feasible ranges: data_width 25..26, n_iter 23..24, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 40 evals, 8 feasible; max throughput seen 158 MSPS; best accuracy 21.96 bits; best feasible luts_plus_ffs=2481; feasible ranges: data_width 24..26, n_iter 24..26, angle_guard 0..2, frac_guard 1..2, m 2..7
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=23..28, n_iter=22..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 90 feasible; hypervolume 8.855e+04 (+4.6%).

**LLM decision:** `map_front` — The front is a single point: pipelined_m [data_width=24 n_iter=22 angle_guard=3 frac_guard=2 rounding=round m=6] at luts_plus_ffs=2330, power_index=4.38. Coverage is 2330..2330 against the HV ref of 8000 and 4.38..4.38 against 20, i.e. the reported HV 8.855e4 is just the rectangle of that one design ((8000-2330)*(20-4.38)=8.86e4). Yet 90 of 200 evals were feasible (75 unique) with only 1 non-dominated, so the trade-off curve is unresolved, not exhausted. Round 3 should therefore be a full-range NSGA-II map over the two families that actually produced feasible designs (pipelined: 12/30 feasible, up to 257 MSPS, best area 3879; pipelined_m: 78/140 feasible, best area 2330, best accuracy 2^-25.31), seeded with the current front point. Note the feasible region is thin and pinned to both constraints (best accuracy 2^-20.25 vs the 2^-20 limit; best feasible throughput 59.9 vs 50 MSPS), so mapping should stay near data_width 24..28, n_iter 22..30 with m free and let code measure where the constraint boundaries fall. Do not spend budget on iterative or unrolled_k: unrolled_k is 0/30 feasible with max throughput 6.55 MSPS, and iterative takes N+3 cycles/result, needing >=350 MHz even at N=4 to reach 50 MSPS, for which there is no supporting evidence.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 8.855e+04 (gain this round: +4.6%).
Feasible designs: 90 of 200 evaluations (75 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 18% violate; best seen 257
- max_abs_err <= 9.53674e-07: 52% violate; best seen 2.41e-08 (2^-25.31)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=24 n_iter=22 angle_guard=3 frac_guard=2 rounding=round m=6] luts_plus_ffs=2330, power_index=4.38, luts=1937, ffs=393, throughput_msps=59.9, max_abs_err=8e-07 (2^-20.25)
Front coverage: luts_plus_ffs 2330..2330 (HV reference 8000); power_index 4.38..4.38 (HV reference 20); data_width on the front 24..24 (registry 8..28).

Per family:
- unrolled_k: 30 evals, 0 feasible; max throughput seen 6.55 MSPS; best accuracy 21.00 bits
- pipelined: 30 evals, 12 feasible; max throughput seen 257 MSPS; best accuracy 21.38 bits; best feasible luts_plus_ffs=3879; feasible ranges: data_width 25..26, n_iter 23..24, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 140 evals, 78 feasible; max throughput seen 158 MSPS; best accuracy 25.31 bits; best feasible luts_plus_ffs=2330; feasible ranges: data_width 24..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=23..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 300 total; 154 feasible; hypervolume 8.855e+04 (+0.0%).

**LLM decision:** `map_front` — The feasible Pareto front is a single design (pipelined_m: 2330 LUT+FF, power 4.38), covering only 29% of the luts_plus_ffs reference range (2330/8000) and 22% of the power reference range (4.38/20). The hypervolume gain this round was +0.0%, so local refinement around this point has stalled. The unexplored iterative family cannot meet the 50 MSPS constraint for the N≈22 iterations required for 2^-20 accuracy: it issues one result per N+3 cycles, needing Fmax ≥ 50×25 = 1250 MHz. The unrolled_k family (same serial datapath, k chained) already produced 0 feasible designs in 30 evals with max throughput 6.55 MSPS, confirming the serial families are throughput-infeasible for this spec. Therefore the remaining 100 evals are best spent mapping the front over the full ranges of the families that actually appear on it (pipelined_m, and possibly pipelined), seeded with the current point, to try to find additional non-dominated designs with lower area or power.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 8.855e+04 (gain this round: +0.0%).
Feasible designs: 154 of 300 evaluations (131 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 15% violate; best seen 257
- max_abs_err <= 9.53674e-07: 44% violate; best seen 2.41e-08 (2^-25.31)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=24 n_iter=22 angle_guard=3 frac_guard=2 rounding=round m=6] luts_plus_ffs=2330, power_index=4.38, luts=1937, ffs=393, throughput_msps=59.9, max_abs_err=8e-07 (2^-20.25)
Front coverage: luts_plus_ffs 2330..2330 (HV reference 8000); power_index 4.38..4.38 (HV reference 20); data_width on the front 24..24 (registry 8..28).

Per family:
- unrolled_k: 30 evals, 0 feasible; max throughput seen 6.55 MSPS; best accuracy 21.00 bits
- pipelined: 30 evals, 12 feasible; max throughput seen 257 MSPS; best accuracy 21.38 bits; best feasible luts_plus_ffs=3879; feasible ranges: data_width 25..26, n_iter 23..24, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 240 evals, 142 feasible; max throughput seen 158 MSPS; best accuracy 25.31 bits; best feasible luts_plus_ffs=2330; feasible ranges: data_width 24..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=23..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 213 feasible; hypervolume 8.898e+04 (+0.5%).

**LLM decision:** `stop` — Final round: all 400/400 evaluations and 4/4 rounds are used, so no further narrowing, widening, or add_family is possible. The problem is not infeasible: a feasible pipelined_m design exists at data_width=27, n_iter=22, angle_guard=-1, frac_guard=0, rounding=round, m=7, meeting both constraints with throughput_msps=52 >= 50 and max_abs_err=9.53e-07 <= 9.53674e-07. The selection rule (min luts_plus_ffs) picks this front point at luts_plus_ffs=2314, power_index=4.35, luts=1908, ffs=406. Hypervolume is 8.898e+04, but this round's gain was only +0.5%, and the front currently has a single feasible design. Other explored families do not dominate it: unrolled_k produced 0 feasible designs (max throughput 6.55 MSPS), and pipelined feasible designs have best luts_plus_ffs=3879. The `iterative` family is unexplored, but the budget is exhausted and no new evaluations remain; given an existing feasible design satisfying both constraints, `infeasible` would be incorrect.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 8.898e+04 (gain this round: +0.5%).
Feasible designs: 213 of 400 evaluations (181 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 15% violate; best seen 257
- max_abs_err <= 9.53674e-07: 41% violate; best seen 2.41e-08 (2^-25.31)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=27 n_iter=22 angle_guard=-1 frac_guard=0 rounding=round m=7] luts_plus_ffs=2314, power_index=4.35, luts=1908, ffs=406, throughput_msps=52, max_abs_err=9.53e-07 (2^-20.00)
Front coverage: luts_plus_ffs 2314..2314 (HV reference 8000); power_index 4.35..4.35 (HV reference 20); data_width on the front 27..27 (registry 8..28).

Per family:
- unrolled_k: 30 evals, 0 feasible; max throughput seen 6.55 MSPS; best accuracy 21.00 bits
- pipelined: 30 evals, 12 feasible; max throughput seen 257 MSPS; best accuracy 21.38 bits; best feasible luts_plus_ffs=3879; feasible ranges: data_width 25..26, n_iter 23..24, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 340 evals, 201 feasible; max throughput seen 158 MSPS; best accuracy 25.31 bits; best feasible luts_plus_ffs=2314; feasible ranges: data_width 23..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 24306 in, 13598 out
- provider-reported cost: $0.0183
- full prompts and replies: `llm_trace.jsonl`

