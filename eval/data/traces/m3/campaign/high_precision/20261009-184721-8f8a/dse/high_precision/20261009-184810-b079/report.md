# DSE run: high_precision

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 400 of 400 budgeted, over 5 round(s).  
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
`pipelined_m:data_width=27,n_iter=22,angle_guard=-1,frac_guard=0,rounding=round,m=6` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 1908 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 406 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 59.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 59.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 100 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
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
| 0 | `pipelined_m:data_width=27,n_iter=22,angle_guard=-1,frac_guard=0,rounding=round,m=6` | 1908 | 406 | 59.9 | 6 | 4.35 | 9.53e-07 (2^-20.00) | 20.00 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires >=50 MSPS throughput and <=2^-20 max error. Throughput constraint eliminates iterative (1 result every N+3 cycles, so at 100 MHz with N=20 that's ~4.5 MSPS, far below 50). This leaves pipelined, pipelined_m, and unrolled_k. The accuracy constraint (20-bit) requires sufficient n_iter and data_width; CORDIC error scales roughly as 2^(-2N) for the rotation part plus quantization from data_width, so N>=20 and W>=18 are needed, with guard bits providing margin. The two objectives (area and power) are correlated but not identical: pipelined_m with large m reduces registers (lower area, lower power) but increases combinational depth (lower Fmax, which may force lower throughput or higher power per operation). unrolled_k with large k similarly trades Fmax for register count. The Pareto front for (area, power) will likely be populated by pipelined_m sweeping m from 2 to 8 and unrolled_k sweeping k from 2 to 8, with pipelined (m=1) as the high-Fmax/low-power anchor. I allocate 55% to pipelined_m (richest trade-off surface), 30% to pipelined (reference anchor), and 15% to unrolled_k (potential area winner). Rounding is fixed to 'round' since truncation would waste accuracy budget; the optimizer can confirm. data_width 18-24 and n_iter 20-26 give the optimizer room to find the minimum-accuracy configuration that still meets 2^-20, which is where the area/power optimum will lie.*)
- `pipelined_m` (55 evals): data_width=18..24, n_iter=20..26, angle_guard=-1..2, frac_guard=0..3, rounding=trunc|round, m=2..8. *Why:* pipelined_m is the primary candidate: it delivers 1 result/cycle (satisfying 50 MSPS at moderate Fmax) while allowing m>1 to trade latency for area/power. The m parameter creates a rich trade-off surface between area (fewer registers) and Fmax (longer combinational paths), which is exactly where the Pareto front for (area, power) will lie. n_iter 20-26 and data_width 18-24 cover the accuracy requirement (2^-20) with some margin for the guard-bit interactions.
- `pipelined` (30 evals): data_width=18..24, n_iter=20..26, angle_guard=-1..2, frac_guard=0..3, rounding=trunc|round. *Why:* pipelined (m=1) is the upper-bound reference: maximum Fmax (shortest combinational path per stage) but maximum register count. It anchors the low-power, low-area end of the front only if Fmax is high enough; more importantly, it defines the latency/area trade-off boundary that pipelined_m must beat. Including it lets the optimizer see the full spectrum of register density.
- `unrolled_k` (15 evals): data_width=18..24, n_iter=20..26, angle_guard=-1..2, frac_guard=0..3, rounding=trunc|round, k=2..8. *Why:* unrolled_k with high k (6-8) can achieve 1 result/cycle throughput with far fewer pipeline registers than pipelined, potentially yielding lower area and power. The shared FSM and k chained rotations per cycle create a different area/Fmax trade-off than pipelined_m. Worth exploring as a potential area winner, though Fmax may be limited by the long combinational chain of k rotations.

**Result (code):** 100 evaluations this round, 100 total; 9 feasible; hypervolume 8.462e+04 (n/a).

**LLM decision:** `refine` — Round 1 found only 1 feasible design (pipelined_m) with a single point on the Pareto front. The accuracy constraint is the binding constraint (91% violation rate), so the search must focus on the accuracy boundary. The current front covers only a tiny slice of the objective space (luts_plus_ffs 2481..2481, power_index 4.67..4.67), so we need to refine around the feasible region to map out the trade-off curve. Pipelined_m is the only family with feasible points, so it gets the largest budget share. Pipelined gets a moderate share because it has high throughput but may have lower area/power at the same accuracy. Unrolled_k gets a small share to confirm it cannot meet the throughput constraint. Iterative is not explored because it produces one result every N+3 cycles, which will make it very hard to reach 50 MSPS unless N is very small, but small N means poor accuracy. The evidence suggests iterative is unlikely to be feasible for this spec.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 8.462e+04 (gain this round: n/a (first round)).
Feasible designs: 9 of 100 evaluations (7 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 16% violate; best seen 264
- max_abs_err <= 9.53674e-07: 91% violate; best seen 6.35e-07 (2^-20.59)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=24 n_iter=24 angle_guard=2 frac_guard=2 rounding=round m=6] luts_plus_ffs=2481, power_index=4.67, luts=2092, ffs=389, throughput_msps=62.5, max_abs_err=7.24e-07 (2^-20.40)
Front coverage: luts_plus_ffs 2481..2481 (HV reference 8000); power_index 4.67..4.67 (HV reference 20); data_width on the front 24..24 (registry 8..28).

Per family:
- unrolled_k: 15 evals, 0 feasible; max throughput seen 7.35 MSPS; best accuracy 18.76 bits
- pipelined: 30 evals, 0 feasible; max throughput seen 264 MSPS; best accuracy 19.74 bits
- pipelined_m: 55 evals, 9 feasible; max throughput seen 164 MSPS; best accuracy 20.59 bits; best feasible luts_plus_ffs=2481; feasible ranges: data_width 24..24, n_iter 24..25, angle_guard 2..2, frac_guard 2..3, m 3..7
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Round 1 found only 1 feasible design (pipelined_m) with a single point on the Pareto front. The accuracy constraint is the binding constraint (91% violation rate), so the search must focus on the accuracy boundary. The current front covers only a tiny slice of the objective space (luts_plus_ffs 2481..2481, power_index 4.67..4.67), so we need to refine around the feasible region to map out the trade-off curve. Pipelined_m is the only family with feasible points, so it gets the largest budget share. Pipelined gets a moderate share because it has high throughput but may have lower area/power at the same accuracy. Unrolled_k gets a small share to confirm it cannot meet the throughput constraint. Iterative is not explored because it produces one result every N+3 cycles, which will make it very hard to reach 50 MSPS unless N is very small, but small N means poor accuracy. The evidence suggests iterative is unlikely to be feasible for this spec.*)
- `pipelined_m` (50 evals): data_width=22..28, n_iter=22..28, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Only family with feasible points. Round 1 found a single point at data_width=24, n_iter=24, angle_guard=2, frac_guard=2, m=6. The accuracy constraint (2^-20) is tight (91% of all evals violated it), so we need to explore the boundary where accuracy just meets the spec while minimizing area/power. Widen data_width and n_iter slightly to find if lower-width designs can still meet accuracy with different guard/rounding settings. Widen m to explore the latency/area tradeoff. Keep angle_guard and frac_guard ranges broad to find the minimal guard bits that still satisfy accuracy.
- `pipelined` (30 evals): data_width=22..28, n_iter=22..28, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Pipelined has the highest throughput (264 MSPS) but 0 feasible points in Round 1, with best accuracy only 19.74 bits. However, it may have lower area/power than pipelined_m for the same accuracy since it has no m parameter (fully pipelined). Explore the same accuracy boundary region to see if pipelined can achieve 2^-20 accuracy with less area/power than pipelined_m.
- `unrolled_k` (20 evals): data_width=22..28, n_iter=22..28, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* Unrolled_k had 0 feasible points with max throughput only 7.35 MSPS, well below the 50 MSPS constraint. However, with higher k values (up to 8) and higher Fmax, it might reach 50 MSPS. Worth a small budget share to confirm infeasibility or find a low-area design if it can meet throughput.

**Result (code):** 100 evaluations this round, 200 total; 65 feasible; hypervolume 8.898e+04 (+5.1%).

**LLM decision:** `map_front` — The current front is a single point (pipelined_m) because the previous round was a narrow refinement. The `pipelined` family offers much higher throughput (up to 264 MSPS) but at a higher area cost (3928 vs 2314), while `pipelined_m` offers lower area but lower throughput. To maximize hypervolume, we need to map the trade-off curve between these two families. Since `unrolled_k` has a maximum throughput of 7.35 MSPS (far below the 50 MSPS constraint) and `iterative` is even slower, they are infeasible for this spec. Therefore, the code should use NSGA-II to map the full front across the feasible ranges of `pipelined` and `pipelined_m` to capture the entire area-vs-power trade-off curve.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 8.898e+04 (gain this round: +5.1%).
Feasible designs: 65 of 200 evaluations (55 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 20% violate; best seen 264
- max_abs_err <= 9.53674e-07: 61% violate; best seen 4.1e-08 (2^-24.54)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=27 n_iter=22 angle_guard=-1 frac_guard=0 rounding=round m=6] luts_plus_ffs=2314, power_index=4.35, luts=1908, ffs=406, throughput_msps=59.9, max_abs_err=9.53e-07 (2^-20.00)
Front coverage: luts_plus_ffs 2314..2314 (HV reference 8000); power_index 4.35..4.35 (HV reference 20); data_width on the front 27..27 (registry 8..28).

Per family:
- unrolled_k: 35 evals, 0 feasible; max throughput seen 7.35 MSPS; best accuracy 24.54 bits
- pipelined: 60 evals, 23 feasible; max throughput seen 264 MSPS; best accuracy 24.28 bits; best feasible luts_plus_ffs=3928; feasible ranges: data_width 23..28, n_iter 22..27, angle_guard 2..4, frac_guard 0..4
- pipelined_m: 105 evals, 42 feasible; max throughput seen 164 MSPS; best accuracy 23.30 bits; best feasible luts_plus_ffs=2314; feasible ranges: data_width 24..28, n_iter 22..27, angle_guard -1..4, frac_guard 0..4, m 2..7
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=26..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 240 total; 94 feasible; hypervolume 8.898e+04 (+0.0%).

**LLM decision:** `map_front` — The current Pareto front consists of a single point (pipelined_m, luts_plus_ffs=2314, power_index=4.35). The hypervolume gain in Round 3 was 0.0%, indicating that the search has stagnated and is not exploring the trade-off curve between area and power. The `pipelined` family achieved a much higher throughput (264 MSPS) but with significantly higher area (3928 LUTs+FFs), while `pipelined_m` offers the best area (2314) but lower throughput (59.9 MSPS). There is a large gap in the objective space between these two families (area 2314 vs 3928) that likely contains intermediate designs with different power/area trade-offs. Since we have 160 evaluations remaining (40% of budget) and 1 round left, the most effective use of the final round is to let the code map the full front over the feasible ranges of `pipelined` and `pipelined_m` to capture the entire trade-off curve, maximizing hypervolume coverage before the final selection.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 8.898e+04 (gain this round: +0.0%).
Feasible designs: 94 of 240 evaluations (79 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 19% violate; best seen 264
- max_abs_err <= 9.53674e-07: 53% violate; best seen 3.75e-08 (2^-24.67)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=27 n_iter=22 angle_guard=-1 frac_guard=0 rounding=round m=6] luts_plus_ffs=2314, power_index=4.35, luts=1908, ffs=406, throughput_msps=59.9, max_abs_err=9.53e-07 (2^-20.00)
Front coverage: luts_plus_ffs 2314..2314 (HV reference 8000); power_index 4.35..4.35 (HV reference 20); data_width on the front 27..27 (registry 8..28).

Per family:
- unrolled_k: 35 evals, 0 feasible; max throughput seen 7.35 MSPS; best accuracy 24.54 bits
- pipelined: 60 evals, 23 feasible; max throughput seen 264 MSPS; best accuracy 24.28 bits; best feasible luts_plus_ffs=3928; feasible ranges: data_width 23..28, n_iter 22..27, angle_guard 2..4, frac_guard 0..4
- pipelined_m: 145 evals, 71 feasible; max throughput seen 164 MSPS; best accuracy 24.67 bits; best feasible luts_plus_ffs=2314; feasible ranges: data_width 24..28, n_iter 22..30, angle_guard -1..4, frac_guard 0..4, m 2..7
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=26..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 340 total; 162 feasible; hypervolume 8.898e+04 (+0.0%).

**LLM decision:** `stop` — The spec is feasible: the pipelined_m design [data_width=27, n_iter=22, angle_guard=-1, frac_guard=0, rounding=round, m=6] meets both constraints (throughput 59.9 MSPS >= 50, max_abs_err 9.53e-07 <= 9.53674e-07) with luts_plus_ffs=2314 and power_index=4.35, well within the HV reference point. The front is a single point because the accuracy constraint (2^-20) tightly couples data_width and n_iter, and the throughput constraint (>=50 MSPS) forces the pipelined/pipelined_m families (unrolled_k maxed at 7.35 MSPS). The hypervolume gain this round was 0.0%, indicating the front has converged and no further improvement is possible within the remaining budget. This is the final round, so we stop with the best feasible design.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 60 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 340 of 400.
Hypervolume of the feasible front: 8.898e+04 (gain this round: +0.0%).
Feasible designs: 162 of 340 evaluations (140 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 17% violate; best seen 264
- max_abs_err <= 9.53674e-07: 44% violate; best seen 3.53e-08 (2^-24.76)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=27 n_iter=22 angle_guard=-1 frac_guard=0 rounding=round m=6] luts_plus_ffs=2314, power_index=4.35, luts=1908, ffs=406, throughput_msps=59.9, max_abs_err=9.53e-07 (2^-20.00)
Front coverage: luts_plus_ffs 2314..2314 (HV reference 8000); power_index 4.35..4.35 (HV reference 20); data_width on the front 27..27 (registry 8..28).

Per family:
- unrolled_k: 35 evals, 0 feasible; max throughput seen 7.35 MSPS; best accuracy 24.54 bits
- pipelined: 60 evals, 23 feasible; max throughput seen 264 MSPS; best accuracy 24.28 bits; best feasible luts_plus_ffs=3928; feasible ranges: data_width 23..28, n_iter 22..27, angle_guard 2..4, frac_guard 0..4
- pipelined_m: 245 evals, 139 feasible; max throughput seen 164 MSPS; best accuracy 24.76 bits; best feasible luts_plus_ffs=2314; feasible ranges: data_width 24..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

### Round 5

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 60 evaluations*)
- `pipelined_m` (60 evals): data_width=26..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 60 evaluations this round, 400 total; 201 feasible; hypervolume 8.898e+04 (+0.0%).

**No LLM call** (code's front-mapping round): The spec is feasible: the pipelined_m design [data_width=27, n_iter=22, angle_guard=-1, frac_guard=0, rounding=round, m=6] meets both constraints (throughput 59.9 MSPS >= 50, max_abs_err 9.53e-07 <= 9.53674e-07) with luts_plus_ffs=2314 and power_index=4.35, well within the HV reference point. The front is a single point because the accuracy constraint (2^-20) tightly couples data_width and n_iter, and the throughput constraint (>=50 MSPS) forces the pipelined/pipelined_m families (unrolled_k maxed at 7.35 MSPS). The hypervolume gain this round was 0.0%, indicating the front has converged and no further improvement is possible within the remaining budget. This is the final round, so we stop with the best feasible design.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 5 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 8.898e+04 (gain this round: +0.0%).
Feasible designs: 201 of 400 evaluations (174 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 17% violate; best seen 264
- max_abs_err <= 9.53674e-07: 40% violate; best seen 3.53e-08 (2^-24.76)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=27 n_iter=22 angle_guard=-1 frac_guard=0 rounding=round m=6] luts_plus_ffs=2314, power_index=4.35, luts=1908, ffs=406, throughput_msps=59.9, max_abs_err=9.53e-07 (2^-20.00)
Front coverage: luts_plus_ffs 2314..2314 (HV reference 8000); power_index 4.35..4.35 (HV reference 20); data_width on the front 27..27 (registry 8..28).

Per family:
- unrolled_k: 35 evals, 0 feasible; max throughput seen 7.35 MSPS; best accuracy 24.54 bits
- pipelined: 60 evals, 23 feasible; max throughput seen 264 MSPS; best accuracy 24.28 bits; best feasible luts_plus_ffs=3928; feasible ranges: data_width 23..28, n_iter 22..27, angle_guard 2..4, frac_guard 0..4
- pipelined_m: 305 evals, 178 feasible; max throughput seen 164 MSPS; best accuracy 24.76 bits; best feasible luts_plus_ffs=2314; feasible ranges: data_width 24..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 25373 in, 4335 out
- provider-reported cost: $0.0070
- full prompts and replies: `llm_trace.jsonl`

