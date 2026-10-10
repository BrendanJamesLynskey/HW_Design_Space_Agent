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
`pipelined_m:data_width=26,n_iter=22,angle_guard=2,frac_guard=0,rounding=round,m=7` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 1908 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 404 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 52 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 52 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 115 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 4.35 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 6.89e-07 (2^-20.47) | exact: bit-accurate model, dense (130961 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 11.6 | exact: bit-accurate model, dense (130961 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.09e-07 (2^-22.19) | exact: bit-accurate model, dense (130961 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.51 | exact: bit-accurate model, dense (130961 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 20.5 | exact: bit-accurate model, dense (130961 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 141.5 dBc, SNR 130.6 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (1 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=26,n_iter=22,angle_guard=2,frac_guard=0,rounding=round,m=7` | 1908 | 404 | 52.0 | 6 | 4.35 | 6.89e-07 (2^-20.47) | 20.47 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The 2^-20 error bound forces data_width >= ~22 and n_iter >= ~22 (output LSB is 2^-(W-2), and CORDIC residual scales as 2^-N), while the 50 MSPS constraint rules out iterative (N+3 cycles/result) and almost certainly unrolled_k (ceil(N/k)+3 cycles/result with k<=8). That leaves pipelined and pipelined_m, both of which deliver 1 result/cycle and therefore meet throughput at any reasonable Fmax. Round 1 searches the full width/iteration/guard/rounding space for both, with pipelined_m given the largest share because its m parameter directly trades Fmax for pipeline FFs and should contain the minimum-area feasible designs the selection rule favours, while pipelined covers the high-Fmax/power end of the front. A small unrolled_k probe checks the infeasibility hypothesis cheaply.*)
- `pipelined` (40 evals): data_width=20..28, n_iter=18..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Pipelined gives 1 result/cycle so it clears the 50 MSPS constraint at any plausible Fmax; it anchors the high-Fmax / high-power end of the front. Search the full width and iteration space to find where 2^-20 error saturates and to expose the cheapest feasible pipelined point.
- `pipelined_m` (45 evals): data_width=20..28, n_iter=18..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Same 1 result/cycle throughput but registers every m stages, so larger m cuts pipeline FFs (area) and power at the cost of Fmax; since only 50 MSPS is required, this family should hold the low-area end that the min-luts_plus_ffs selection rule will pick. Largest share because it is the most likely source of the winning design.
- `unrolled_k` (15 evals): data_width=20..28, n_iter=18..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=4..8. *Why:* Small probe only: with k<=8 and N>=20 the schedule is ceil(N/k)+3 >= 6 cycles/result, so it would need an implausible Fmax to reach 50 MSPS. A few evaluations confirm or refute this before we commit the remaining budget elsewhere.

**Result (code):** 100 evaluations this round, 100 total; 36 feasible; hypervolume 8.432e+04 (n/a).

**LLM decision:** `map_front` — The feasible Pareto front contains only one design (pipelined_m W=26 N=24 angle_guard=-1 frac_guard=0 m=5), so it covers a negligible fraction of both objective ranges: luts_plus_ffs 2493..2493 vs HV ref 8000, and power_index 4.69..4.69 vs HV ref 20. Hypervolume is 8.432e4, far below the 1.6e5 maximum for this reference point. The other explored families cannot improve the front: unrolled_k is infeasible for throughput (max seen 5.75 MSPS < 50), and pipelined is dominated (best feasible luts_plus_ffs=4492 > 2493). The unexplored iterative family is structurally unable to meet 50 MSPS because it takes N+3 cycles/result with N>=4, so even at an optimistic 300 MHz it would yield <50 MSPS. Therefore the best next step is to let code map the full pipelined_m design space (the only family on the front) with NSGA-II seeded by the current front, which will explore the full registry ranges and discover the true trade-off curve, improving hypervolume before any refinement.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 8.432e+04 (gain this round: n/a (first round)).
Feasible designs: 36 of 100 evaluations (28 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 17% violate; best seen 264
- max_abs_err <= 9.53674e-07: 62% violate; best seen 5.86e-08 (2^-24.02)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=26 n_iter=24 angle_guard=-1 frac_guard=0 rounding=round m=5] luts_plus_ffs=2493, power_index=4.69, luts=2017, ffs=476, throughput_msps=73.7, max_abs_err=9.43e-07 (2^-20.02)
Front coverage: luts_plus_ffs 2493..2493 (HV reference 8000); power_index 4.69..4.69 (HV reference 20); data_width on the front 26..26 (registry 8..28).

Per family:
- unrolled_k: 15 evals, 0 feasible; max throughput seen 5.75 MSPS; best accuracy 19.99 bits
- pipelined: 40 evals, 15 feasible; max throughput seen 264 MSPS; best accuracy 23.19 bits; best feasible luts_plus_ffs=4492; feasible ranges: data_width 24..27, n_iter 26..28, angle_guard 0..3, frac_guard 1..4
- pipelined_m: 45 evals, 21 feasible; max throughput seen 158 MSPS; best accuracy 24.02 bits; best feasible luts_plus_ffs=2493; feasible ranges: data_width 24..28, n_iter 23..27, angle_guard -1..4, frac_guard 0..3, m 2..6
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=25..28, n_iter=22..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 120 feasible; hypervolume 8.432e+04 (+0.0%).

**LLM decision:** `map_front` — The feasible Pareto front is a single point: pipelined_m [W=26 N=24 angle_guard=-1 frac_guard=0 round m=5] at luts_plus_ffs=2493, power_index=4.69. Against the HV reference (8000, 20) this one point yields the entire HV of 8.43e4, and the round gain was +0.0%, so the search has stalled on a degenerate front. Coverage is minimal on both objectives: luts_plus_ffs spans only 2493..2493 vs registry/reference 8000, and power_index only 4.69..4.69 vs reference 20. The feasible region is clearly much larger than the front suggests: pipelined_m alone has 105 feasible designs over data_width 24..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7, and pipelined has 15 feasible designs (best luts_plus_ffs=4492) over data_width 24..27, n_iter 26..28, angle_guard 0..3, frac_guard 1..4. Both families produce 1 result/cycle, so both can satisfy throughput>=50 (best seen 264 and 158 MSPS) while trading area against power. The unexplored iterative family cannot help: it emits 1 result per N+3 cycles, so at N~24 it would need >1 GHz to reach 50 MSPS, and unrolled_k already showed 0 feasible with max throughput 5.75 MSPS. Therefore the correct use of the remaining budget is to let code run NSGA-II over the full ranges of the two on-front families (pipelined_m, pipelined), seeded with the current point, to spread the front across the luts_plus_ffs and power_index ranges and capture the hypervolume that the single-point front is leaving on the table.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 8.432e+04 (gain this round: +0.0%).
Feasible designs: 120 of 200 evaluations (102 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 12% violate; best seen 264
- max_abs_err <= 9.53674e-07: 36% violate; best seen 4.04e-08 (2^-24.56)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=26 n_iter=24 angle_guard=-1 frac_guard=0 rounding=round m=5] luts_plus_ffs=2493, power_index=4.69, luts=2017, ffs=476, throughput_msps=73.7, max_abs_err=9.43e-07 (2^-20.02)
Front coverage: luts_plus_ffs 2493..2493 (HV reference 8000); power_index 4.69..4.69 (HV reference 20); data_width on the front 26..26 (registry 8..28).

Per family:
- unrolled_k: 15 evals, 0 feasible; max throughput seen 5.75 MSPS; best accuracy 19.99 bits
- pipelined: 40 evals, 15 feasible; max throughput seen 264 MSPS; best accuracy 23.19 bits; best feasible luts_plus_ffs=4492; feasible ranges: data_width 24..27, n_iter 26..28, angle_guard 0..3, frac_guard 1..4
- pipelined_m: 145 evals, 105 feasible; max throughput seen 158 MSPS; best accuracy 24.56 bits; best feasible luts_plus_ffs=2493; feasible ranges: data_width 24..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=25..28, n_iter=22..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 300 total; 201 feasible; hypervolume 8.903e+04 (+5.6%).

**LLM decision:** `map_front` — The feasible Pareto front is a single point: pipelined_m [W=26 N=22 ag=2 fg=0 round m=7] at luts_plus_ffs=2312, power_index=4.35, throughput=52 MSPS, max_abs_err=6.89e-07. Front coverage is degenerate (luts_plus_ffs 2312..2312 vs HV ref 8000; power_index 4.35..4.35 vs HV ref 20), so the entire hypervolume (8.903e+04) comes from one rectangle and there is no trade-off curve mapped at all. 201 feasible designs collapse to 1 non-dominated point, meaning the search has not yet revealed whether lower-area or lower-power feasible designs exist. With 100 evals left and the reserved mapping step due before the run ends, the right move is to let NSGA-II map the full front over the full ranges of the family that actually reaches feasibility (pipelined_m: data_width 24..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7), seeded with the current front. iterative is not worth adding: its N+3 cycles/result cannot reach 50 MSPS at the Fmax implied by the 264 MSPS pipelined result, and the analogous serial family unrolled_k already produced 0 feasible designs (max 5.75 MSPS).

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 8.903e+04 (gain this round: +5.6%).
Feasible designs: 201 of 300 evaluations (165 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 11% violate; best seen 264
- max_abs_err <= 9.53674e-07: 28% violate; best seen 4.04e-08 (2^-24.56)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=26 n_iter=22 angle_guard=2 frac_guard=0 rounding=round m=7] luts_plus_ffs=2312, power_index=4.35, luts=1908, ffs=404, throughput_msps=52, max_abs_err=6.89e-07 (2^-20.47)
Front coverage: luts_plus_ffs 2312..2312 (HV reference 8000); power_index 4.35..4.35 (HV reference 20); data_width on the front 26..26 (registry 8..28).

Per family:
- unrolled_k: 15 evals, 0 feasible; max throughput seen 5.75 MSPS; best accuracy 19.99 bits
- pipelined: 40 evals, 15 feasible; max throughput seen 264 MSPS; best accuracy 23.19 bits; best feasible luts_plus_ffs=4492; feasible ranges: data_width 24..27, n_iter 26..28, angle_guard 0..3, frac_guard 1..4
- pipelined_m: 245 evals, 186 feasible; max throughput seen 158 MSPS; best accuracy 24.56 bits; best feasible luts_plus_ffs=2312; feasible ranges: data_width 24..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=25..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 280 feasible; hypervolume 8.903e+04 (+0.0%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), and this round produced +0.0% hypervolume gain, so further search is not justified. The spec is satisfiable: 280 of 400 evaluations are feasible, with a valid Pareto design pipelined_m [data_width=26 n_iter=22 angle_guard=2 frac_guard=0 rounding=round m=7] at luts_plus_ffs=2312, power_index=4.35, throughput_msps=52 (>= 50) and max_abs_err=6.89e-07 (2^-20.47, <= 2^-20). So `infeasible` is not warranted. The front is thin (1 design, luts_plus_ffs 2312..2312 vs HV ref 8000; power_index 4.35..4.35 vs ref 20), but with no remaining budget and no gain this round, the correct terminal action is stop; the selection rule (min luts_plus_ffs) picks the single feasible front point above.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 8.903e+04 (gain this round: +0.0%).
Feasible designs: 280 of 400 evaluations (235 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 9% violate; best seen 264
- max_abs_err <= 9.53674e-07: 26% violate; best seen 3.4e-08 (2^-24.81)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=26 n_iter=22 angle_guard=2 frac_guard=0 rounding=round m=7] luts_plus_ffs=2312, power_index=4.35, luts=1908, ffs=404, throughput_msps=52, max_abs_err=6.89e-07 (2^-20.47)
Front coverage: luts_plus_ffs 2312..2312 (HV reference 8000); power_index 4.35..4.35 (HV reference 20); data_width on the front 26..26 (registry 8..28).

Per family:
- unrolled_k: 15 evals, 0 feasible; max throughput seen 5.75 MSPS; best accuracy 19.99 bits
- pipelined: 40 evals, 15 feasible; max throughput seen 264 MSPS; best accuracy 23.19 bits; best feasible luts_plus_ffs=4492; feasible ranges: data_width 24..27, n_iter 26..28, angle_guard 0..3, frac_guard 1..4
- pipelined_m: 345 evals, 265 feasible; max throughput seen 158 MSPS; best accuracy 24.81 bits; best feasible luts_plus_ffs=2312; feasible ranges: data_width 24..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 24197 in, 14342 out
- provider-reported cost: $0.0129
- full prompts and replies: `llm_trace.jsonl`

