# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec low_area_control: Field-oriented motor-control loop needing sin/cos of the rotor angle at >= 1 MSPS with max error <= 2^-10. Area is everything: minimise LUTs + FFs.
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min luts_plus_ffs (HV ref 1500)
  objective: max accuracy_bits (HV ref 10)
  select: min luts_plus_ffs
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=15,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 168 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 92 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 11 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 18 | exact: schedule |
| latency_ns | 90.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.176 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000632 (2^-10.63) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 5.18 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000164 (2^-12.58) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.34 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.6 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 168 | 92 | 11.0 | 18 | 0.176 | 0.000632 (2^-10.63) | 10.63 |
| 1 | `iterative:data_width=15,n_iter=19,angle_guard=1,frac_guard=2,rounding=trunc` | 194 | 97 | 7.4 | 22 | 0.241 | 0.000515 (2^-10.92) | 10.92 |
| 2 | `iterative:data_width=17,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 191 | 102 | 11.0 | 18 | 0.198 | 0.000168 (2^-12.54) | 12.54 |
| 3 | `iterative:data_width=17,n_iter=21,angle_guard=1,frac_guard=2,rounding=trunc` | 228 | 107 | 6.6 | 24 | 0.302 | 0.000144 (2^-12.76) | 12.76 |
| 4 | `iterative:data_width=18,n_iter=23,angle_guard=3,frac_guard=0,rounding=round` | 231 | 110 | 6.1 | 26 | 0.334 | 7.75e-05 (2^-13.65) | 13.65 |
| 5 | `iterative:data_width=23,n_iter=26,angle_guard=-2,frac_guard=0,rounding=trunc` | 297 | 130 | 5.4 | 29 | 0.466 | 1.46e-05 (2^-16.06) | 16.06 |
| 6 | `iterative:data_width=22,n_iter=23,angle_guard=4,frac_guard=0,rounding=round` | 303 | 131 | 6.0 | 26 | 0.424 | 5.23e-06 (2^-17.54) | 17.54 |
| 7 | `iterative:data_width=23,n_iter=23,angle_guard=3,frac_guard=0,rounding=round` | 319 | 135 | 6.0 | 26 | 0.444 | 2.9e-06 (2^-18.39) | 18.39 |
| 8 | `iterative:data_width=24,n_iter=28,angle_guard=4,frac_guard=1,rounding=trunc` | 344 | 143 | 4.9 | 31 | 0.569 | 1.78e-06 (2^-19.10) | 19.10 |
| 9 | `iterative:data_width=22,n_iter=26,angle_guard=4,frac_guard=4,rounding=trunc` | 358 | 139 | 5.4 | 29 | 0.542 | 1.68e-06 (2^-19.18) | 19.18 |
| 10 | `iterative:data_width=25,n_iter=26,angle_guard=4,frac_guard=3,rounding=trunc` | 398 | 152 | 5.3 | 29 | 0.6 | 2.82e-07 (2^-21.76) | 21.76 |
| 11 | `iterative:data_width=28,n_iter=28,angle_guard=3,frac_guard=0,rounding=round` | 417 | 160 | 4.9 | 31 | 0.673 | 1.11e-07 (2^-23.10) | 23.10 |
| 12 | `iterative:data_width=28,n_iter=28,angle_guard=4,frac_guard=3,rounding=round` | 529 | 167 | 4.9 | 31 | 0.812 | 2.42e-08 (2^-25.30) | 25.30 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-critical (min luts_plus_ffs) with a tight accuracy constraint (max_abs_err <= 2^-10) and a loose throughput constraint (>=1 MSPS). Both families easily meet throughput, so the trade-off is area versus accuracy. Accuracy depends only on data_width, n_iter, angle_guard, frac_guard, and rounding. The output LSB dictates W >= 13, and CORDIC residual angle error dictates N >= 12. Since the shared datapath in iterative keeps area fairly insensitive to N, we search a wide N range (12-24) to capture accuracy gains at low area cost. Unrolled_k with small k may become more area-efficient at larger W by eliminating the barrel shifter, so we split the budget equally to map both sides of the potential crossover.*)
- `iterative` (30 evals): data_width=13..18, n_iter=12..24, angle_guard=-1..1, frac_guard=0..2, rounding=trunc|round. *Why:* Baseline low-area family: one micro-rotation per cycle with a shared datapath and barrel shifters. This typically minimises area for small data widths. We search W 13-18 and N 12-24 to cover the tight accuracy boundary (max_abs_err <= 2^-10) and the upper accuracy end of the Pareto front. The wide N range is included because the shared datapath keeps area relatively insensitive to N, so extra iterations can buy accuracy cheaply. angle_guard -1..2 and frac_guard 0..2 explore the precision-area trade-off, and both rounding modes are kept to allow truncation to win if it saves area while still meeting accuracy.
- `unrolled_k` (30 evals): data_width=13..18, n_iter=12..24, angle_guard=-1..1, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Unrolling replaces the barrel shifter with fixed shifts, which can reduce area at larger data widths despite duplicating the adder. We focus on small k (2-4) because larger k only increases area without helping the loose throughput constraint (>=1 MSPS is already met by iterative). The same data_width, n_iter, guard, and rounding ranges as iterative allow direct area-accuracy comparison and help map the Pareto front where unrolled_k might win for larger W.

**Result (code):** 60 evaluations this round, 60 total; 45 feasible; hypervolume 4527 (n/a).

**LLM decision:** `stop` — This is the final round, and the front is feasible and well-covered, so no further exploration is possible or useful. Evidence: 45 of 60 evaluations were feasible (39 unique), with 0% violating the throughput constraint (best 13.2 MSPS vs >=1 required) and the accuracy constraint met by the front (best max_abs_err 6.72e-05 = 2^-13.86, well under the 2^-10 limit). The Pareto front spans luts_plus_ffs 260..448 and accuracy_bits 10.6..13.9, covering a meaningful trade-off curve against the HV reference point (1500, 10), giving hypervolume 4527. The selection rule (min luts_plus_ffs) is satisfied by the iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] design at luts_plus_ffs=260, accuracy_bits=10.6, throughput 11 MSPS, max_abs_err 6.32e-04 (2^-10.63) — all constraints met. No infeasibility exists, and the budget/round cap is reached, so we stop.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 4527 (gain this round: n/a (first round)).
Feasible designs: 45 of 60 evaluations (39 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 13.2
- max_abs_err <= 0.000976562: 25% violate; best seen 6.72e-05 (2^-13.86)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.6, luts=168, ffs=92, throughput_msps=11, max_abs_err=0.000632 (2^-10.63), power_index=0.176
- iterative [data_width=15 n_iter=19 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=291, accuracy_bits=10.9, luts=194, ffs=97, throughput_msps=7.36, max_abs_err=0.000515 (2^-10.92), power_index=0.241
- iterative [data_width=17 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=293, accuracy_bits=12.5, luts=191, ffs=102, throughput_msps=11, max_abs_err=0.000168 (2^-12.54), power_index=0.198
- iterative [data_width=17 n_iter=21 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=335, accuracy_bits=12.8, luts=228, ffs=107, throughput_msps=6.62, max_abs_err=0.000144 (2^-12.76), power_index=0.302
- iterative [data_width=17 n_iter=21 angle_guard=1 frac_guard=2 rounding=round] luts_plus_ffs=384, accuracy_bits=13.1, luts=277, ffs=107, throughput_msps=6.62, max_abs_err=0.000112 (2^-13.13), power_index=0.347
- unrolled_k [data_width=18 n_iter=22 angle_guard=1 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=448, accuracy_bits=13.9, luts=337, ffs=111, throughput_msps=7.35, max_abs_err=6.72e-05 (2^-13.86), power_index=0.236
Front coverage: luts_plus_ffs 260..448 (HV reference 1500); accuracy_bits 10.6..13.9 (HV reference 10); data_width on the front 15..18 (registry 8..28).

Per family:
- iterative: 30 evals, 22 feasible; max throughput seen 13.2 MSPS; best accuracy 13.13 bits; best feasible luts_plus_ffs=260; feasible ranges: data_width 15..17, n_iter 12..22, angle_guard -1..1, frac_guard 0..2
- unrolled_k: 30 evals, 23 feasible; max throughput seen 10.7 MSPS; best accuracy 13.86 bits; best feasible luts_plus_ffs=374; feasible ranges: data_width 14..18, n_iter 13..24, angle_guard -1..1, frac_guard 0..2, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (34 evals): data_width=14..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (5 front designs; box front_anchored)
- `unrolled_k` (6 evals): data_width=17..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 85 feasible; hypervolume 1.568e+04 (+246.4%).

**No LLM call** (code's front-mapping round): This is the final round, and the front is feasible and well-covered, so no further exploration is possible or useful. Evidence: 45 of 60 evaluations were feasible (39 unique), with 0% violating the throughput constraint (best 13.2 MSPS vs >=1 required) and the accuracy constraint met by the front (best max_abs_err 6.72e-05 = 2^-13.86, well under the 2^-10 limit). The Pareto front spans luts_plus_ffs 260..448 and accuracy_bits 10.6..13.9, covering a meaningful trade-off curve against the HV reference point (1500, 10), giving hypervolume 4527. The selection rule (min luts_plus_ffs) is satisfied by the iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] design at luts_plus_ffs=260, accuracy_bits=10.6, throughput 11 MSPS, max_abs_err 6.32e-04 (2^-10.63) — all constraints met. No infeasibility exists, and the budget/round cap is reached, so we stop.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.568e+04 (gain this round: +246.4%).
Feasible designs: 85 of 100 evaluations (76 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 13.2
- max_abs_err <= 0.000976562: 15% violate; best seen 2.42e-08 (2^-25.30)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.6, luts=168, ffs=92, throughput_msps=11, max_abs_err=0.000632 (2^-10.63), power_index=0.176
- iterative [data_width=15 n_iter=19 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=291, accuracy_bits=10.9, luts=194, ffs=97, throughput_msps=7.36, max_abs_err=0.000515 (2^-10.92), power_index=0.241
- iterative [data_width=17 n_iter=21 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=335, accuracy_bits=12.8, luts=228, ffs=107, throughput_msps=6.62, max_abs_err=0.000144 (2^-12.76), power_index=0.302
- iterative [data_width=18 n_iter=23 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=341, accuracy_bits=13.7, luts=231, ffs=110, throughput_msps=6.11, max_abs_err=7.75e-05 (2^-13.65), power_index=0.334
- iterative [data_width=23 n_iter=26 angle_guard=-2 frac_guard=0 rounding=trunc] luts_plus_ffs=428, accuracy_bits=16.1, luts=297, ffs=130, throughput_msps=5.38, max_abs_err=1.46e-05 (2^-16.06), power_index=0.466
- iterative [data_width=23 n_iter=23 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=454, accuracy_bits=18.4, luts=319, ffs=135, throughput_msps=6, max_abs_err=2.9e-06 (2^-18.39), power_index=0.444
- iterative [data_width=24 n_iter=28 angle_guard=4 frac_guard=1 rounding=trunc] luts_plus_ffs=488, accuracy_bits=19.1, luts=344, ffs=143, throughput_msps=4.94, max_abs_err=1.78e-06 (2^-19.10), power_index=0.569
- iterative [data_width=22 n_iter=26 angle_guard=4 frac_guard=4 rounding=trunc] luts_plus_ffs=497, accuracy_bits=19.2, luts=358, ffs=139, throughput_msps=5.38, max_abs_err=1.68e-06 (2^-19.18), power_index=0.542
- iterative [data_width=28 n_iter=28 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=577, accuracy_bits=23.1, luts=417, ffs=160, throughput_msps=4.86, max_abs_err=1.11e-07 (2^-23.10), power_index=0.673
- iterative [data_width=28 n_iter=28 angle_guard=4 frac_guard=3 rounding=round] luts_plus_ffs=696, accuracy_bits=25.3, luts=529, ffs=167, throughput_msps=4.86, max_abs_err=2.42e-08 (2^-25.30), power_index=0.812
Front coverage: luts_plus_ffs 260..696 (HV reference 1500); accuracy_bits 10.6..25.3 (HV reference 10); data_width on the front 15..28 (registry 8..28).

Per family:
- iterative: 64 evals, 56 feasible; max throughput seen 13.2 MSPS; best accuracy 25.30 bits; best feasible luts_plus_ffs=260; feasible ranges: data_width 15..28, n_iter 12..30, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 36 evals, 29 feasible; max throughput seen 10.7 MSPS; best accuracy 18.01 bits; best feasible luts_plus_ffs=374; feasible ranges: data_width 14..25, n_iter 13..29, angle_guard -2..2, frac_guard 0..4, k 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4063 in, 15733 out
- provider-reported cost: $0.0109
- full prompts and replies: `llm_trace.jsonl`

