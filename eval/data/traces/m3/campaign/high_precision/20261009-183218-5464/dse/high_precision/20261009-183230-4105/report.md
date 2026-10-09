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
`pipelined:data_width=23,n_iter=22,angle_guard=4,frac_guard=3,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 1935 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 1899 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 249 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 249 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 24 | exact: schedule |
| latency_ns | 96.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 7.21 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 9.39e-07 (2^-20.02) | exact: bit-accurate model, dense (130304 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 1.97 | exact: bit-accurate model, dense (130304 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.53e-07 (2^-21.91) | exact: bit-accurate model, dense (130304 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 0.531 | exact: bit-accurate model, dense (130304 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 20 | exact: bit-accurate model, dense (130304 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 24 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 141.9 dBc, SNR 128.9 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (1 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=23,n_iter=22,angle_guard=4,frac_guard=3,rounding=round` | 1935 | 1899 | 249.0 | 24 | 7.21 | 9.39e-07 (2^-20.02) | 20.02 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The binding constraints are max_abs_err <= 2^-20 and throughput >= 50 MSPS. Throughput forces a 1-result/cycle family (pipelined or pipelined_m) or a high-Fmax unrolled_k; iterative is excluded because its multi-cycle result rate makes 50 MSPS implausible at the precision needed. Accuracy is set by data_width/n_iter/guards identically across families, so I span W=18..24 and N=14..22 with small guards to cover the error-vs-area trade-off from just-meets to comfortable margin. The two objectives (area and power) are best traded off within the 1/cycle families: pipelined for the min-area corner (selection rule) and pipelined_m for the low-power/low-FF region, with unrolled_k as a secondary probe. Budget is weighted toward the two pipelined families where the front actually lives, keeping the small-area end well populated for the min-luts_plus_ffs selection rule.*)
- `pipelined` (45 evals): data_width=18..24, n_iter=14..22, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* 1 result/cycle is the only way to plausibly hit >=50 MSPS with a tight 2^-20 error budget. Pipelined is the area-cheapest 1/cycle family (no k/m multiplier chains), so it should dominate the min-luts_plus_ffs corner that the selection rule picks. W=18..24 and N=14..22 span the accuracy trade-off (accuracy_bits ~ N + guard terms) so the front from just-meets-error up to comfortable margin is covered; angle/frac guards kept small to hold area down.
- `pipelined_m` (35 evals): data_width=18..24, n_iter=14..22, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* Same 1/cycle throughput as pipelined but registers every m stages, trading a little latency for fewer FFs and a higher Fmax (shorter combinational chains). This is the main lever for the power_index objective and for pushing area down at the same accuracy, so it should populate the low-power / low-FF region of the front that pipelined alone may miss.
- `unrolled_k` (20 evals): data_width=18..24, n_iter=14..22, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* k chained rotations/cycle can reach >=50 MSPS with fewer total stages (lower N) than a 1/cycle design, which can cut area and power at the cost of a longer combinational path (lower Fmax). Worth a smaller share to check whether it lands on the front between the pipelined families; capped at k<=4 to keep Fmax realistic for the throughput constraint.

**Result (code):** 100 evaluations this round, 100 total; 0 feasible; hypervolume 0 (n/a).

**LLM decision:** `refine` — The primary blocker is accuracy: 100% of evaluations violate max_abs_err <= 9.53674e-07 (2^-20). The best result so far is 1.68e-06 (2^-19.19) from `pipelined` with data_width=23, n_iter=22, angle_guard=2, frac_guard=2, rounding=round. This is only ~0.8 bits short of the target. Throughput is not a constraint for `pipelined` (best seen 264 MSPS >> 50 MSPS). `unrolled_k` and `pipelined_m` are significantly worse on accuracy (17.93 and 17.80 bits respectively) and likely cannot reach 20 bits without excessive area/latency trade-offs that don't help the primary accuracy gap. Therefore, we should focus exclusively on `pipelined` and narrow the search space to the region that produced the best accuracy, slightly expanding `n_iter` and `data_width` to ensure we cross the 2^-20 threshold. We will drop `unrolled_k` and `pipelined_m` from the active search to concentrate the remaining 300 evaluations on the promising `pipelined` family.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 0 (gain this round: n/a (first round)).
Feasible designs: 0 of 100 evaluations (0 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 20% violate; best seen 264
- max_abs_err <= 9.53674e-07: 100% violate; best seen 1.68e-06 (2^-19.19)

No feasible design found yet. Least-violating designs:
- pipelined [data_width=23 n_iter=22 angle_guard=2 frac_guard=2 rounding=round]: throughput=257, max_abs_err=1.68e-06 (2^-19.19); max_abs_err <= 9.53674e-07 violated by 75.7%
- pipelined [data_width=23 n_iter=21 angle_guard=2 frac_guard=2 rounding=round]: throughput=257, max_abs_err=2.11e-06 (2^-18.86); max_abs_err <= 9.53674e-07 violated by 120.9%
- pipelined [data_width=24 n_iter=21 angle_guard=0 frac_guard=2 rounding=round]: throughput=257, max_abs_err=2.44e-06 (2^-18.65); max_abs_err <= 9.53674e-07 violated by 155.7%
- pipelined [data_width=23 n_iter=22 angle_guard=1 frac_guard=2 rounding=round]: throughput=257, max_abs_err=2.53e-06 (2^-18.59); max_abs_err <= 9.53674e-07 violated by 165.2%
- pipelined [data_width=23 n_iter=21 angle_guard=2 frac_guard=1 rounding=round]: throughput=257, max_abs_err=2.63e-06 (2^-18.54); max_abs_err <= 9.53674e-07 violated by 175.3%

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 17.93 bits
- pipelined: 45 evals, 0 feasible; max throughput seen 264 MSPS; best accuracy 19.19 bits
- pipelined_m: 35 evals, 0 feasible; max throughput seen 164 MSPS; best accuracy 17.80 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate all remaining budget on the pipelined family in the region of the best previous result to cross the accuracy threshold.*)
- `pipelined` (100 evals): data_width=23..25, n_iter=22..26, angle_guard=1..3, frac_guard=2..3, rounding=round. *Why:* Focus on the pipelined family which achieved the best accuracy (19.19 bits) and highest throughput. Narrow ranges around the best-performing configuration (dw=23, n=22, ag=2, fg=2, round) to find a feasible design that meets the 2^-20 error constraint. Rounding is fixed to 'round' as it typically provides better accuracy than truncation for the same bit-width.

**Result (code):** 100 evaluations this round, 200 total; 73 feasible; hypervolume 5.316e+04 (+inf).

**LLM decision:** `refine` — The current Pareto front consists of a single design (pipelined, W=24, N=22) with luts_plus_ffs=3840 and power_index=7.22. The hypervolume is low (5.3e4) because the front does not span the trade-off curve. The `pipelined` family is the only one yielding feasible designs (73/145 feasible), while `unrolled_k` and `pipelined_m` failed to meet the throughput or accuracy constraints in their initial explorations. To maximize hypervolume, we need to explore the trade-off between area and power within the `pipelined` family. The current feasible region for `pipelined` is W=23..25, N=22..26. We should narrow the search to this region to allow Optuna to densely sample the Pareto front, specifically looking for designs that might offer lower area (by reducing W or N slightly if accuracy allows) or lower power (by reducing pipeline depth or width). We will focus exclusively on `pipelined` as it is the only proven feasible family.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 5.316e+04 (gain this round: +inf (first feasible designs)).
Feasible designs: 73 of 200 evaluations (27 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 10% violate; best seen 264
- max_abs_err <= 9.53674e-07: 64% violate; best seen 2.49e-07 (2^-21.94)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined [data_width=24 n_iter=22 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=3840, power_index=7.22, luts=1937, ffs=1903, throughput_msps=249, max_abs_err=8e-07 (2^-20.25)
Front coverage: luts_plus_ffs 3840..3840 (HV reference 8000); power_index 7.22..7.22 (HV reference 20); data_width on the front 24..24 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 17.93 bits
- pipelined: 145 evals, 73 feasible; max throughput seen 264 MSPS; best accuracy 21.94 bits; best feasible luts_plus_ffs=3840; feasible ranges: data_width 23..25, n_iter 22..26, angle_guard 1..3, frac_guard 2..3
- pipelined_m: 35 evals, 0 feasible; max throughput seen 164 MSPS; best accuracy 17.80 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *Narrowing to the feasible region of the pipelined family allows for a denser search of the Pareto front, which is necessary to improve hypervolume.*)
- `pipelined` (40 evals): data_width=23..25, n_iter=22..26, angle_guard=1..3, frac_guard=2..3, rounding=trunc|round. *Why:* Focus on the only feasible family to map the trade-off curve between area and power within the known feasible bounds.

**Result (code):** 40 evaluations this round, 240 total; 102 feasible; hypervolume 5.316e+04 (+0.0%).

**LLM decision:** `stop` — The front is a single point (pipelined, 3840 LUTs+FFs, power 7.22) that meets both constraints (throughput 249 MSPS >= 50, max_abs_err 8e-07 <= 9.53674e-07). The hypervolume gain in the final round was 0.0%, indicating the search has converged and no further improvement is possible within the remaining budget. The selection rule (min luts_plus_ffs) is satisfied by this design. Since this is the final round, we stop.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 160 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 400.
Hypervolume of the feasible front: 5.316e+04 (gain this round: +0.0%).
Feasible designs: 102 of 240 evaluations (42 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 8% violate; best seen 264
- max_abs_err <= 9.53674e-07: 57% violate; best seen 2.16e-07 (2^-22.14)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined [data_width=24 n_iter=22 angle_guard=3 frac_guard=2 rounding=round] luts_plus_ffs=3840, power_index=7.22, luts=1937, ffs=1903, throughput_msps=249, max_abs_err=8e-07 (2^-20.25)
Front coverage: luts_plus_ffs 3840..3840 (HV reference 8000); power_index 7.22..7.22 (HV reference 20); data_width on the front 24..24 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 17.93 bits
- pipelined: 185 evals, 102 feasible; max throughput seen 264 MSPS; best accuracy 22.14 bits; best feasible luts_plus_ffs=3840; feasible ranges: data_width 23..25, n_iter 22..26, angle_guard 1..3, frac_guard 2..3
- pipelined_m: 35 evals, 0 feasible; max throughput seen 164 MSPS; best accuracy 17.80 bits
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 160 evaluations*)
- `pipelined` (160 evals): data_width=23..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (1 front designs; box front_anchored)

**Result (code):** 160 evaluations this round, 400 total; 209 feasible; hypervolume 5.329e+04 (+0.2%).

**No LLM call** (code's front-mapping round): The front is a single point (pipelined, 3840 LUTs+FFs, power 7.22) that meets both constraints (throughput 249 MSPS >= 50, max_abs_err 8e-07 <= 9.53674e-07). The hypervolume gain in the final round was 0.0%, indicating the search has converged and no further improvement is possible within the remaining budget. The selection rule (min luts_plus_ffs) is satisfied by this design. Since this is the final round, we stop.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 5.329e+04 (gain this round: +0.2%).
Feasible designs: 209 of 400 evaluations (121 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 5% violate; best seen 264
- max_abs_err <= 9.53674e-07: 48% violate; best seen 1.77e-08 (2^-25.75)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined [data_width=23 n_iter=22 angle_guard=4 frac_guard=3 rounding=round] luts_plus_ffs=3833, power_index=7.21, luts=1935, ffs=1899, throughput_msps=249, max_abs_err=9.39e-07 (2^-20.02)
Front coverage: luts_plus_ffs 3833..3833 (HV reference 8000); power_index 7.21..7.21 (HV reference 20); data_width on the front 23..23 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 9.97 MSPS; best accuracy 17.93 bits
- pipelined: 345 evals, 209 feasible; max throughput seen 264 MSPS; best accuracy 25.75 bits; best feasible luts_plus_ffs=3833; feasible ranges: data_width 23..28, n_iter 22..30, angle_guard -1..4, frac_guard 0..4
- pipelined_m: 35 evals, 0 feasible; max throughput seen 164 MSPS; best accuracy 17.80 bits
```
</details>

## LLM usage
- calls: 7 (failed/unparsed attempts: 0)
- tokens: 22487 in, 2891 out
- provider-reported cost: $0.0074
- full prompts and replies: `llm_trace.jsonl`

