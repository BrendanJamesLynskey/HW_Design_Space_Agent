# DSE run: high_precision

**Verdict:** converged: hypervolume gain fell below epsilon.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 3 round(s).  
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
`pipelined_m:data_width=25,n_iter=24,angle_guard=2,frac_guard=0,rounding=round,m=6` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 2017 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 389 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 59.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 59.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 100 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 4.53 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 8.15e-07 (2^-20.23) | exact: bit-accurate model, dense (130882 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 6.84 | exact: bit-accurate model, dense (130882 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 1.89e-07 (2^-22.33) | exact: bit-accurate model, dense (130882 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.59 | exact: bit-accurate model, dense (130882 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 20.2 | exact: bit-accurate model, dense (130882 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 142.7 dBc, SNR 131.5 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (1 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=25,n_iter=24,angle_guard=2,frac_guard=0,rounding=round,m=6` | 2017 | 389 | 59.9 | 6 | 4.53 | 8.15e-07 (2^-20.23) | 20.23 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires max_abs_err <= 2^-20 and throughput >= 50 MSPS, with selection by min luts_plus_ffs. The error constraint requires sufficient n_iter and data_width; the throughput constraint requires either pipelined/pipelined_m (1 result/cycle) or very high Fmax for iterative. Pipelined_m is likely the best area/throughput trade-off since it reduces FF count vs fully pipelined while maintaining 1 result/cycle. We allocate 40% to pipelined, 35% to pipelined_m, and 15% to iterative (to confirm infeasibility). We search n_iter 20-30 and data_width 22-28 to find the minimal-area designs that meet the 2^-20 error bound. angle_guard and frac_guard are kept small (0-2) to minimize area while still meeting error. Rounding is explored for both trunc and round to see if rounding helps meet the error bound with fewer iterations.*)
- `pipelined` (45 evals): data_width=22..28, n_iter=20..30, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Pipelined gives 1 result/cycle, so throughput = Fmax. To hit 50 MSPS we need Fmax >= 50 MHz, which is easily met. The error constraint (<= 2^-20) requires sufficient n_iter and data_width. Since selection is min luts_plus_ffs, we want the smallest area design that meets error and throughput. Pipelined has high FF count due to per-stage registers, but it's the only family that guarantees 1 result/cycle without the complexity of unrolled_k. We search moderate-to-high n_iter (20-30) and data_width (22-28) to find the minimal-area point that meets 2^-20 error. angle_guard and frac_guard kept small to minimize area while still meeting error.
- `pipelined_m` (39 evals): data_width=22..28, n_iter=20..30, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* Pipelined_m registers every m stages, reducing FF count compared to fully pipelined while still achieving 1 result/cycle. This is likely the best area/throughput trade-off for this spec. By varying m (2-8), we can find the sweet spot where FF count is minimized while maintaining adequate Fmax for 50 MSPS. Same error constraints apply, so we search the same n_iter and data_width ranges as pipelined.
- `iterative` (16 evals): data_width=22..28, n_iter=20..30, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Iterative has the lowest area (shared datapath, minimal FFs) but produces one result every N+3 cycles. To meet 50 MSPS, we need Fmax * (1/(N+3)) >= 50 MHz, so Fmax >= 50*(N+3) MHz. For N=20-30, this requires Fmax >= 1150-1650 MHz, which is infeasible on Artix-7. Therefore iterative likely cannot meet the throughput constraint. We include it with a small budget share to confirm infeasibility and to capture any unexpected high-Fmax designs that might work.

**Result (code):** 100 evaluations this round, 100 total; 48 feasible; hypervolume 8.519e+04 (n/a).

**LLM decision:** `map_front` — The current Pareto front consists of a single point (pipelined_m, 2459 LUTs+FFs, 4.62 power), which is a poor representation of the trade-off space given the hypervolume reference points (8000, 20). The `pipelined` family has demonstrated a much larger feasible region (best area 3879, max throughput 264 MSPS) and `pipelined_m` has found the current best area (2459). Since `iterative` is infeasible for throughput and `unrolled_k` is unlikely to beat `pipelined_m` on area while maintaining the required 50 MSPS throughput (due to shared datapath constraints and lower throughput than fully pipelined designs), the relevant families are `pipelined` and `pipelined_m`. To maximize hypervolume, we need to map the full trade-off curve between area and power for these two families. The current exploration has only sampled a small subset of the feasible ranges (e.g., `pipelined` feasible ranges are data_width 25..28, n_iter 23..30). Using `map_front` will allow the code to run NSGA-II over the full feasible ranges of these families, seeding with the current front, to properly populate the Pareto front and maximize the hypervolume score before the final selection.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 8.519e+04 (gain this round: n/a (first round)).
Feasible designs: 48 of 100 evaluations (42 unique).
Families explored so far: iterative, pipelined, pipelined_m. Not yet explored: unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 22% violate; best seen 264
- max_abs_err <= 9.53674e-07: 36% violate; best seen 8.36e-08 (2^-23.51)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=27 n_iter=23 angle_guard=1 frac_guard=0 rounding=trunc m=7] luts_plus_ffs=2459, power_index=4.62, luts=2045, ffs=414, throughput_msps=52, max_abs_err=5.21e-07 (2^-20.87)
Front coverage: luts_plus_ffs 2459..2459 (HV reference 8000); power_index 4.62..4.62 (HV reference 20); data_width on the front 27..27 (registry 8..28).

Per family:
- iterative: 16 evals, 0 feasible; max throughput seen 6.78 MSPS; best accuracy 21.66 bits
- pipelined: 45 evals, 25 feasible; max throughput seen 264 MSPS; best accuracy 23.51 bits; best feasible luts_plus_ffs=3879; feasible ranges: data_width 25..28, n_iter 23..30, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 39 evals, 23 feasible; max throughput seen 114 MSPS; best accuracy 23.19 bits; best feasible luts_plus_ffs=2459; feasible ranges: data_width 25..28, n_iter 23..30, angle_guard 0..1, frac_guard 0..2, m 3..7
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=26..28, n_iter=21..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 128 feasible; hypervolume 8.6e+04 (+0.9%).

**LLM decision:** `add_family` — The current Pareto front is a single point (pipelined_m, 2428 LUTs+FFs, 4.57 power). The `pipelined` family has a higher best feasible area (3879) but much higher throughput (264 MSPS), suggesting a trade-off exists that `pipelined_m` might not fully capture at the low-area end. `unrolled_k` is unexplored. It offers a middle ground: higher throughput than `iterative` (which failed throughput constraints) and potentially lower area/power than `pipelined` for the same latency/throughput requirements, or better area than `pipelined_m` if the FSM overhead is lower than the pipeline register overhead for specific k values. Given we have 200 evals left and the front is very narrow, exploring `unrolled_k` is the best way to potentially find a design with lower `luts_plus_ffs` or `power_index` that satisfies the 50 MSPS and accuracy constraints.
- **rule applied by code:** 'add_family' overridden to stop: HV gain 0.95% < epsilon 1.00%
- **rule applied by code:** code: before stopping (converged), one front-mapping round with the remaining 200 evaluations
- effective decision: `stop`

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 8.6e+04 (gain this round: +0.9%).
Feasible designs: 128 of 200 evaluations (111 unique).
Families explored so far: iterative, pipelined, pipelined_m. Not yet explored: unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 14% violate; best seen 264
- max_abs_err <= 9.53674e-07: 26% violate; best seen 2.41e-08 (2^-25.31)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=26 n_iter=23 angle_guard=1 frac_guard=1 rounding=trunc m=6] luts_plus_ffs=2428, power_index=4.57, luts=2022, ffs=406, throughput_msps=59.9, max_abs_err=5.95e-07 (2^-20.68)
Front coverage: luts_plus_ffs 2428..2428 (HV reference 8000); power_index 4.57..4.57 (HV reference 20); data_width on the front 26..26 (registry 8..28).

Per family:
- iterative: 16 evals, 0 feasible; max throughput seen 6.78 MSPS; best accuracy 21.66 bits
- pipelined: 45 evals, 25 feasible; max throughput seen 264 MSPS; best accuracy 23.51 bits; best feasible luts_plus_ffs=3879; feasible ranges: data_width 25..28, n_iter 23..30, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 139 evals, 103 feasible; max throughput seen 158 MSPS; best accuracy 25.31 bits; best feasible luts_plus_ffs=2428; feasible ranges: data_width 25..28, n_iter 22..30, angle_guard -1..4, frac_guard 0..4, m 2..7
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 200 evaluations*)
- `pipelined_m` (200 evals): data_width=25..28, n_iter=21..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 200 evaluations this round, 400 total; 266 feasible; hypervolume 8.656e+04 (+0.6%).

**No LLM call** (code's front-mapping round): The current Pareto front is a single point (pipelined_m, 2428 LUTs+FFs, 4.57 power). The `pipelined` family has a higher best feasible area (3879) but much higher throughput (264 MSPS), suggesting a trade-off exists that `pipelined_m` might not fully capture at the low-area end. `unrolled_k` is unexplored. It offers a middle ground: higher throughput than `iterative` (which failed throughput constraints) and potentially lower area/power than `pipelined` for the same latency/throughput requirements, or better area than `pipelined_m` if the FSM overhead is lower than the pipeline register overhead for specific k values. Given we have 200 evals left and the front is very narrow, exploring `unrolled_k` is the best way to potentially find a design with lower `luts_plus_ffs` or `power_index` that satisfies the 50 MSPS and accuracy constraints.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 8.656e+04 (gain this round: +0.6%).
Feasible designs: 266 of 400 evaluations (234 unique).
Families explored so far: iterative, pipelined, pipelined_m. Not yet explored: unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 14% violate; best seen 264
- max_abs_err <= 9.53674e-07: 23% violate; best seen 2.41e-08 (2^-25.31)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=25 n_iter=24 angle_guard=2 frac_guard=0 rounding=round m=6] luts_plus_ffs=2406, power_index=4.53, luts=2017, ffs=389, throughput_msps=59.9, max_abs_err=8.15e-07 (2^-20.23)
Front coverage: luts_plus_ffs 2406..2406 (HV reference 8000); power_index 4.53..4.53 (HV reference 20); data_width on the front 25..25 (registry 8..28).

Per family:
- iterative: 16 evals, 0 feasible; max throughput seen 6.78 MSPS; best accuracy 21.66 bits
- pipelined: 45 evals, 25 feasible; max throughput seen 264 MSPS; best accuracy 23.51 bits; best feasible luts_plus_ffs=3879; feasible ranges: data_width 25..28, n_iter 23..30, angle_guard 0..2, frac_guard 0..2
- pipelined_m: 339 evals, 241 feasible; max throughput seen 158 MSPS; best accuracy 25.31 bits; best feasible luts_plus_ffs=2406; feasible ranges: data_width 25..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 1)
- tokens: 19683 in, 2753 out
- provider-reported cost: $0.0053
- full prompts and replies: `llm_trace.jsonl`

