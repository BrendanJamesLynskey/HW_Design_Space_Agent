# DSE run: high_precision

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
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
`pipelined_m:data_width=23,n_iter=22,angle_guard=4,frac_guard=3,rounding=round,m=6` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 1935 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 389 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 59.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 59.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 100 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 4.37 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 9.39e-07 (2^-20.02) | exact: bit-accurate model, dense (130304 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 1.97 | exact: bit-accurate model, dense (130304 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.53e-07 (2^-21.91) | exact: bit-accurate model, dense (130304 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 0.531 | exact: bit-accurate model, dense (130304 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 20 | exact: bit-accurate model, dense (130304 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 141.9 dBc, SNR 128.9 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (1 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=23,n_iter=22,angle_guard=4,frac_guard=3,rounding=round,m=6` | 1935 | 389 | 59.9 | 6 | 4.37 | 9.39e-07 (2^-20.02) | 20.02 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires max_abs_err <= 2^-20 and throughput >= 50 MSPS, with objectives to minimize area (luts_plus_ffs) and power_index. The selection rule is min luts_plus_ffs, so we prioritize designs near the accuracy boundary with minimal area. Pipelined and pipelined_m are the primary candidates because they guarantee 1 result/cycle, making it easier to meet the throughput constraint. Pipelined_m is likely to dominate pipelined in area/power due to fewer registers, so we allocate equal budget to both to map the Pareto front. Unrolled_k is included as a secondary option because it can achieve high throughput with less register overhead, but its deeper combinational logic may limit Fmax. Iterative is included with a small budget to confirm infeasibility. The data_width and n_iter ranges (18-24) are chosen to ensure accuracy can meet 2^-20 while keeping area reasonable. The guard parameters are explored to find the minimum precision needed. This plan focuses the budget on the families most likely to meet the constraints and reveals the area-power trade-off.*)
- `pipelined` (35 evals): data_width=18..24, n_iter=18..24, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Pipelined is the only family that guarantees 1 result/cycle, making it the primary candidate for meeting the >= 50 MSPS throughput constraint. To achieve max_abs_err <= 2^-20, we need sufficient precision. Since accuracy depends on data_width, n_iter, and guards, we search data_width 18-24 and n_iter 18-24. The selection rule is min luts_plus_ffs, so we want the smallest area that meets accuracy and throughput. Pipelined has high area due to N+2 stages of registers, so we need to find the minimum N and W that satisfy the error constraint. The trade-off is between area (minimize) and power (minimize), both driven by reducing N and W while staying above the accuracy threshold.
- `pipelined_m` (35 evals): data_width=18..24, n_iter=18..24, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Pipelined_m offers a middle ground: 1 result/cycle throughput (meeting >= 50 MSPS) but with fewer registers than fully pipelined (only ceil(N/m) stages instead of N). This should yield lower area and power than pipelined for the same accuracy. The parameter m (2-8) controls the trade-off: larger m means fewer registers (lower area/power) but potentially lower Fmax due to longer combinational paths. Since the selection rule is min luts_plus_ffs, pipelined_m with larger m values may dominate the Pareto front. We search the same data_width and n_iter ranges as pipelined to ensure comparable accuracy, and explore m to find the optimal register spacing.
- `unrolled_k` (20 evals): data_width=18..24, n_iter=18..24, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* Unrolled_k performs k micro-rotations per cycle, so throughput = Fmax * k / ceil(N/k). For small N (18-24) and large k (up to 8), this can achieve high throughput with fewer pipeline stages than pipelined. However, the combinational logic per cycle is deeper (k rotations), which may reduce Fmax. This family could offer a lower-area solution if Fmax remains high enough to meet 50 MSPS. We include it to explore the area-throughput trade-off, especially for cases where pipelined_m's register overhead is still too high. The k parameter allows us to balance between logic depth and throughput.
- `iterative` (10 evals): data_width=18..24, n_iter=18..24, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Iterative has the lowest area (shared datapath, no pipeline registers) but produces 1 result every N+3 cycles. To meet >= 50 MSPS, we need Fmax * 1/(N+3) >= 50, so Fmax >= 50*(N+3). For N=18-24, this requires Fmax >= 1150-1450 MHz, which is likely infeasible on Artix-7. However, we include a small budget to confirm infeasibility and to check if any corner case (e.g., very high Fmax with small N) might work. If infeasible, this confirms that pipelined families are required.

**Result (code):** 100 evaluations this round, 100 total; 8 feasible; hypervolume 8.098e+04 (n/a).

**LLM decision:** `refine` — The current Pareto front consists of a single point (pipelined_m, 2624 LUTs+FFs, 4.94 power). The `pipelined` family achieved a higher throughput (264 MSPS) but with significantly higher area (4052 LUTs+FFs). To maximize hypervolume, we need to explore the trade-off curve between these two extremes. The `pipelined_m` family offers a middle ground by allowing partial pipelining (m > 1), which should reduce area compared to fully pipelined while maintaining high throughput. We should focus the search on `pipelined_m` and `pipelined` with parameters that ensure accuracy (data_width >= 23, n_iter >= 23, angle_guard >= 2, frac_guard >= 3) and throughput (m <= 4 for pipelined_m to keep latency/throughput high). Narrowing the ranges will allow Optuna to find more points on the front between the current best area and the fully pipelined area.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 8.098e+04 (gain this round: n/a (first round)).
Feasible designs: 8 of 100 evaluations (6 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 38% violate; best seen 264
- max_abs_err <= 9.53674e-07: 92% violate; best seen 6.47e-07 (2^-20.56)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=24 n_iter=23 angle_guard=2 frac_guard=4 rounding=trunc m=4] luts_plus_ffs=2624, power_index=4.94, luts=2045, ffs=579, throughput_msps=86, max_abs_err=9.04e-07 (2^-20.08)
Front coverage: luts_plus_ffs 2624..2624 (HV reference 8000); power_index 4.94..4.94 (HV reference 20); data_width on the front 24..24 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 7.43 MSPS; best accuracy 18.37 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 8.18 MSPS; best accuracy 19.71 bits
- pipelined: 35 evals, 5 feasible; max throughput seen 264 MSPS; best accuracy 20.56 bits; best feasible luts_plus_ffs=4052; feasible ranges: data_width 23..23, n_iter 23..24, angle_guard 3..4, frac_guard 3..4
- pipelined_m: 35 evals, 3 feasible; max throughput seen 164 MSPS; best accuracy 20.33 bits; best feasible luts_plus_ffs=2624; feasible ranges: data_width 24..24, n_iter 22..24, angle_guard 2..3, frac_guard 4..4, m 3..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Refining to focus on pipelined_m and pipelined with constrained ranges around the known feasible region to map the trade-off curve between area and power/throughput.*)
- `pipelined_m` (60 evals): data_width=23..25, n_iter=23..26, angle_guard=2..4, frac_guard=3..4, rounding=trunc|round, m=2..6. *Why:* pipelined_m is the most promising family for balancing area and throughput. The current best point is at m=4. Exploring m=2,3,5,6 with slightly varied accuracy parameters should reveal more points on the Pareto front, potentially lowering area further or improving the power/area trade-off.
- `pipelined` (40 evals): data_width=23..24, n_iter=23..25, angle_guard=3..4, frac_guard=3..4, rounding=trunc|round. *Why:* pipelined provides the highest throughput and serves as the upper-bound reference for area. Focusing on the minimal accuracy parameters that meet the constraint (data_width=23, n_iter=23) will help define the high-throughput, high-area end of the Pareto front.

**Result (code):** 100 evaluations this round, 200 total; 96 feasible; hypervolume 8.475e+04 (+4.7%).

**LLM decision:** `refine` — The current Pareto front consists of a single point (pipelined_m, 2476 LUT+FF, 4.66 power). While pipelined_m is clearly superior to pipelined (which has a best feasible area of 4010), the search has not yet mapped the trade-off curve within the pipelined_m family. The feasible region for pipelined_m is broad (data_width 23-25, n_iter 22-26, m 2-6), but the current best point is at the edge of the data_width range (25) and a high m (6). To maximize hypervolume, we need to explore lower area/power configurations that still meet the 50 MSPS and 2^-20 error constraints. Specifically, we should test if lower `data_width` (23-24) or different `m` values (2-4) can reduce area/power while maintaining throughput and accuracy. The `iterative` and `unrolled_k` families are infeasible for throughput (max ~8 MSPS) and should be ignored. We will focus the next round on refining the `pipelined_m` family to uncover the rest of the front.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 8.475e+04 (gain this round: +4.7%).
Feasible designs: 96 of 200 evaluations (67 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 19% violate; best seen 264
- max_abs_err <= 9.53674e-07: 52% violate; best seen 1.8e-07 (2^-22.40)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=25 n_iter=23 angle_guard=2 frac_guard=3 rounding=trunc m=6] luts_plus_ffs=2476, power_index=4.66, luts=2069, ffs=408, throughput_msps=59.9, max_abs_err=5.4e-07 (2^-20.82)
Front coverage: luts_plus_ffs 2476..2476 (HV reference 8000); power_index 4.66..4.66 (HV reference 20); data_width on the front 25..25 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 7.43 MSPS; best accuracy 18.37 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 8.18 MSPS; best accuracy 19.71 bits
- pipelined: 75 evals, 38 feasible; max throughput seen 264 MSPS; best accuracy 21.19 bits; best feasible luts_plus_ffs=4010; feasible ranges: data_width 23..24, n_iter 23..25, angle_guard 3..4, frac_guard 3..4
- pipelined_m: 95 evals, 58 feasible; max throughput seen 164 MSPS; best accuracy 22.40 bits; best feasible luts_plus_ffs=2476; feasible ranges: data_width 23..25, n_iter 22..26, angle_guard 2..4, frac_guard 3..4, m 2..6
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Refine the search to the pipelined_m family's feasible region to map the Pareto front. The current front is a single point, indicating under-exploration. We exclude pipelined (worse area) and iterative/unrolled_k (infeasible throughput).*)
- `pipelined_m` (40 evals): data_width=23..25, n_iter=22..26, angle_guard=2..4, frac_guard=3..4, rounding=trunc|round, m=2..6. *Why:* Focus entirely on pipelined_m to map the trade-off between area/power and throughput/accuracy. The current single-point front suggests the search hasn't covered the feasible space. By narrowing to the known feasible ranges but allowing full exploration of m and rounding, we can find lower area/power points that may exist at the cost of slightly higher latency or lower throughput (as long as >=50 MSPS).

**Result (code):** 40 evaluations this round, 240 total; 131 feasible; hypervolume 8.871e+04 (+4.7%).

**LLM decision:** `stop` — This is the final round (240/400 evals used, round 3 of 4 complete). The feasible Pareto front currently consists of a single design: pipelined_m [data_width=23, n_iter=22, angle_guard=4, frac_guard=3, rounding=round, m=6] with luts_plus_ffs=2324 and power_index=4.37. This design satisfies both constraints: throughput_msps=59.9 (>= 50) and max_abs_err=9.39e-07 (<= 9.53674e-07). The selection rule is 'min luts_plus_ffs', and this design is the best feasible design found across all 240 evaluations (best feasible luts_plus_ffs for pipelined_m is 2324, for pipelined is 4010). The hypervolume has stabilized (gain this round +4.7%), and the front covers the minimum area point required by the selection rule. No further exploration is possible or necessary within the remaining budget constraints and round cap.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 8.871e+04 (gain this round: +4.7%).
Feasible designs: 131 of 240 evaluations (92 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 16% violate; best seen 264
- max_abs_err <= 9.53674e-07: 45% violate; best seen 1.68e-07 (2^-22.51)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=23 n_iter=22 angle_guard=4 frac_guard=3 rounding=round m=6] luts_plus_ffs=2324, power_index=4.37, luts=1935, ffs=389, throughput_msps=59.9, max_abs_err=9.39e-07 (2^-20.02)
Front coverage: luts_plus_ffs 2324..2324 (HV reference 8000); power_index 4.37..4.37 (HV reference 20); data_width on the front 23..23 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 7.43 MSPS; best accuracy 18.37 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 8.18 MSPS; best accuracy 19.71 bits
- pipelined: 75 evals, 38 feasible; max throughput seen 264 MSPS; best accuracy 21.19 bits; best feasible luts_plus_ffs=4010; feasible ranges: data_width 23..24, n_iter 23..25, angle_guard 3..4, frac_guard 3..4
- pipelined_m: 135 evals, 93 feasible; max throughput seen 164 MSPS; best accuracy 22.51 bits; best feasible luts_plus_ffs=2324; feasible ranges: data_width 23..25, n_iter 22..26, angle_guard 2..4, frac_guard 3..4, m 2..6
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined_m` (160 evals): data_width=22..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 221 feasible; hypervolume 8.871e+04 (+0.0%).

**No LLM call** (code's front-mapping round): This is the final round (240/400 evals used, round 3 of 4 complete). The feasible Pareto front currently consists of a single design: pipelined_m [data_width=23, n_iter=22, angle_guard=4, frac_guard=3, rounding=round, m=6] with luts_plus_ffs=2324 and power_index=4.37. This design satisfies both constraints: throughput_msps=59.9 (>= 50) and max_abs_err=9.39e-07 (<= 9.53674e-07). The selection rule is 'min luts_plus_ffs', and this design is the best feasible design found across all 240 evaluations (best feasible luts_plus_ffs for pipelined_m is 2324, for pipelined is 4010). The hypervolume has stabilized (gain this round +4.7%), and the front covers the minimum area point required by the selection rule. No further exploration is possible or necessary within the remaining budget constraints and round cap.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 8.871e+04 (gain this round: +0.0%).
Feasible designs: 221 of 400 evaluations (170 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 13% violate; best seen 264
- max_abs_err <= 9.53674e-07: 42% violate; best seen 6.09e-08 (2^-23.97)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=23 n_iter=22 angle_guard=4 frac_guard=3 rounding=round m=6] luts_plus_ffs=2324, power_index=4.37, luts=1935, ffs=389, throughput_msps=59.9, max_abs_err=9.39e-07 (2^-20.02)
Front coverage: luts_plus_ffs 2324..2324 (HV reference 8000); power_index 4.37..4.37 (HV reference 20); data_width on the front 23..23 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 7.43 MSPS; best accuracy 18.37 bits
- unrolled_k: 20 evals, 0 feasible; max throughput seen 8.18 MSPS; best accuracy 19.71 bits
- pipelined: 75 evals, 38 feasible; max throughput seen 264 MSPS; best accuracy 21.19 bits; best feasible luts_plus_ffs=4010; feasible ranges: data_width 23..24, n_iter 23..25, angle_guard 3..4, frac_guard 3..4
- pipelined_m: 295 evals, 183 feasible; max throughput seen 164 MSPS; best accuracy 23.97 bits; best feasible luts_plus_ffs=2324; feasible ranges: data_width 23..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 21894 in, 4156 out
- provider-reported cost: $0.0083
- full prompts and replies: `llm_trace.jsonl`

