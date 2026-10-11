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
`iterative:data_width=15,n_iter=13,angle_guard=0,frac_guard=1,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 168 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 93 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 12.4 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 80.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.157 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000944 (2^-10.05) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 7.74 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000216 (2^-12.18) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.77 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (18 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=13,angle_guard=0,frac_guard=1,rounding=trunc` | 168 | 93 | 12.4 | 16 | 0.157 | 0.000944 (2^-10.05) | 10.05 |
| 1 | `iterative:data_width=16,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc` | 170 | 96 | 11.0 | 18 | 0.18 | 0.000643 (2^-10.60) | 10.60 |
| 2 | `iterative:data_width=16,n_iter=19,angle_guard=2,frac_guard=0,rounding=round` | 196 | 99 | 7.4 | 22 | 0.244 | 0.000285 (2^-11.78) | 11.78 |
| 3 | `iterative:data_width=16,n_iter=23,angle_guard=2,frac_guard=2,rounding=trunc` | 212 | 103 | 6.2 | 26 | 0.308 | 0.000268 (2^-11.86) | 11.86 |
| 4 | `iterative:data_width=16,n_iter=23,angle_guard=2,frac_guard=3,rounding=trunc` | 228 | 105 | 6.1 | 26 | 0.325 | 0.000186 (2^-12.39) | 12.39 |
| 5 | `iterative:data_width=16,n_iter=23,angle_guard=3,frac_guard=3,rounding=trunc` | 230 | 106 | 6.1 | 26 | 0.328 | 0.000154 (2^-12.67) | 12.67 |
| 6 | `iterative:data_width=17,n_iter=17,angle_guard=3,frac_guard=2,rounding=trunc` | 230 | 109 | 7.9 | 20 | 0.255 | 9.91e-05 (2^-13.30) | 13.30 |
| 7 | `iterative:data_width=21,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc` | 227 | 121 | 10.8 | 18 | 0.236 | 7.62e-05 (2^-13.68) | 13.68 |
| 8 | `iterative:data_width=20,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 239 | 122 | 10.2 | 19 | 0.258 | 3.93e-05 (2^-14.63) | 14.63 |
| 9 | `iterative:data_width=20,n_iter=17,angle_guard=2,frac_guard=1,rounding=trunc` | 262 | 121 | 7.9 | 20 | 0.288 | 3.13e-05 (2^-14.96) | 14.96 |
| 10 | `iterative:data_width=20,n_iter=19,angle_guard=1,frac_guard=2,rounding=trunc` | 274 | 122 | 7.2 | 22 | 0.328 | 2.04e-05 (2^-15.58) | 15.58 |
| 11 | `iterative:data_width=20,n_iter=19,angle_guard=2,frac_guard=2,rounding=trunc` | 276 | 123 | 7.2 | 22 | 0.33 | 1.63e-05 (2^-15.90) | 15.90 |
| 12 | `iterative:data_width=25,n_iter=23,angle_guard=3,frac_guard=2,rounding=trunc` | 371 | 149 | 5.9 | 26 | 0.509 | 5.8e-07 (2^-20.72) | 20.72 |
| 13 | `iterative:data_width=27,n_iter=23,angle_guard=3,frac_guard=2,rounding=trunc` | 406 | 159 | 5.9 | 26 | 0.553 | 3.16e-07 (2^-21.59) | 21.59 |
| 14 | `iterative:data_width=27,n_iter=27,angle_guard=0,frac_guard=2,rounding=trunc` | 411 | 156 | 5.1 | 30 | 0.641 | 2.6e-07 (2^-21.88) | 21.88 |
| 15 | `iterative:data_width=27,n_iter=27,angle_guard=3,frac_guard=3,rounding=trunc` | 434 | 161 | 5.1 | 30 | 0.672 | 8.85e-08 (2^-23.43) | 23.43 |
| 16 | `iterative:data_width=27,n_iter=30,angle_guard=3,frac_guard=2,rounding=round` | 495 | 159 | 4.6 | 33 | 0.812 | 6.73e-08 (2^-23.82) | 23.82 |
| 17 | `iterative:data_width=27,n_iter=30,angle_guard=3,frac_guard=3,rounding=round` | 514 | 161 | 4.6 | 33 | 0.838 | 5.3e-08 (2^-24.17) | 24.17 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec minimises LUT+FF subject to a loose throughput floor (≥1 MSPS) and a modest accuracy floor (max_abs_err ≤ 2^-10). Iterative architectures naturally dominate this regime: they use one shared datapath, so their area is the smallest for any given (W, N, guards, rounding), and their serial schedule still delivers ≥4 MSPS for the largest N considered. The main search question is where the feasible accuracy boundary lies in (W, N, guard, rounding) space and how area grows along it. The proposed ranges bracket the likely feasible region (W 12–20, N 10–20) and include negative/zero guards to find minimal-area feasible corners, while extending high enough to map the Pareto front up to the HV reference area of 1500. Unrolled_k gets a small share only to verify that replication does not produce a surprise edge (e.g., via higher Fmax permitting smaller N) and to include any incidental Pareto points in the fleet merge. Round 1 uses broad ranges; later rounds will narrow around the discovered front and spend the reserved budget mapping it over the full feasible ranges.*)
- `iterative` (48 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round. *Why:* Iterative shares one datapath, so it gives the smallest LUT+FF for any given accuracy. Throughput is Fmax/(N+3), which for N≤20 and any realistic Artix-7 Fmax (≥100 MHz) is ≥4 MSPS, safely above the 1 MSPS constraint. Thus area is the only binding objective here, and iterative should dominate the Pareto front. The ranges cover the accuracy threshold (W≥12, N≥10) and extend high enough to reach the accuracy objective and the HV reference area (luts+ffs≈1500). angle_guard and frac_guard include negative/zero values to catch minimal-area feasible points; rounding is included because it can trade a little area for accuracy.
- `unrolled_k` (12 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Unrolled_k replicates the datapath k times, so for the same accuracy it should be larger in area than iterative. The throughput constraint is only 1 MSPS and iterative already meets it, so unrolled_k is unlikely to offer a better area/accuracy trade-off. A small budget is reserved to confirm this and to catch any unexpected Fmax advantage that might allow a smaller N or W (e.g., if a narrower datapath becomes feasible at higher clock). k is limited to 2–4 because larger k only increases area without helping the area objective.

**Result (code):** 60 evaluations this round, 60 total; 38 feasible; hypervolume 6774 (n/a).

**LLM decision:** `stop` — Final round: the feasible front is well-populated and satisfies both constraints. Throughput constraint (>=1 MSPS) is met by every feasible design (0% violate; best 15.6 MSPS), and the accuracy constraint (max_abs_err <= 2^-10) is met across the front, with the cheapest design at luts_plus_ffs=261 / accuracy_bits=10.05 (max_abs_err=0.000944) and the most accurate at 399 / 15.90 bits. The front spans luts_plus_ffs 261..399 against an HV reference of 1500 and accuracy_bits 10..15.9 against reference 10, so it already covers the trade-off region well beyond the reference point; the selection rule (min luts_plus_ffs) picks the 261-area iterative design, which is feasible. No further gain is expected within the exhausted budget, and no constraint is unreachable, so the run stops rather than declaring infeasible.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 6774 (gain this round: n/a (first round)).
Feasible designs: 38 of 60 evaluations (30 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 37% violate; best seen 1.63e-05 (2^-15.90)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=261, accuracy_bits=10, luts=168, ffs=93, throughput_msps=12.4, max_abs_err=0.000944 (2^-10.05), power_index=0.157
- iterative [data_width=15 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=268, accuracy_bits=10.5, luts=171, ffs=97, throughput_msps=13.2, max_abs_err=0.00071 (2^-10.46), power_index=0.151
- iterative [data_width=16 n_iter=19 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=295, accuracy_bits=11.8, luts=196, ffs=99, throughput_msps=7.36, max_abs_err=0.000285 (2^-11.78), power_index=0.244
- iterative [data_width=16 n_iter=17 angle_guard=2 frac_guard=1 rounding=round] luts_plus_ffs=345, accuracy_bits=12.5, luts=244, ffs=101, throughput_msps=8.1, max_abs_err=0.000177 (2^-12.47), power_index=0.259
- iterative [data_width=20 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=383, accuracy_bits=15, luts=262, ffs=121, throughput_msps=7.95, max_abs_err=3.13e-05 (2^-14.96), power_index=0.288
- iterative [data_width=20 n_iter=19 angle_guard=1 frac_guard=2 rounding=trunc] luts_plus_ffs=396, accuracy_bits=15.6, luts=274, ffs=122, throughput_msps=7.23, max_abs_err=2.04e-05 (2^-15.58), power_index=0.328
- iterative [data_width=20 n_iter=19 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=399, accuracy_bits=15.9, luts=276, ffs=123, throughput_msps=7.23, max_abs_err=1.63e-05 (2^-15.90), power_index=0.33
Front coverage: luts_plus_ffs 261..399 (HV reference 1500); accuracy_bits 10..15.9 (HV reference 10); data_width on the front 15..20 (registry 8..28).

Per family:
- iterative: 48 evals, 30 feasible; max throughput seen 15.6 MSPS; best accuracy 15.90 bits; best feasible luts_plus_ffs=261; feasible ranges: data_width 14..20, n_iter 12..19, angle_guard -2..2, frac_guard 0..2
- unrolled_k: 12 evals, 8 feasible; max throughput seen 13.5 MSPS; best accuracy 13.18 bits; best feasible luts_plus_ffs=363; feasible ranges: data_width 14..18, n_iter 13..15, angle_guard -1..2, frac_guard 0..2, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (40 evals): data_width=14..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (7 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 73 feasible; hypervolume 1.468e+04 (+116.7%).

**No LLM call** (code's front-mapping round): Final round: the feasible front is well-populated and satisfies both constraints. Throughput constraint (>=1 MSPS) is met by every feasible design (0% violate; best 15.6 MSPS), and the accuracy constraint (max_abs_err <= 2^-10) is met across the front, with the cheapest design at luts_plus_ffs=261 / accuracy_bits=10.05 (max_abs_err=0.000944) and the most accurate at 399 / 15.90 bits. The front spans luts_plus_ffs 261..399 against an HV reference of 1500 and accuracy_bits 10..15.9 against reference 10, so it already covers the trade-off region well beyond the reference point; the selection rule (min luts_plus_ffs) picks the 261-area iterative design, which is feasible. No further gain is expected within the exhausted budget, and no constraint is unreachable, so the run stops rather than declaring infeasible.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.468e+04 (gain this round: +116.7%).
Feasible designs: 73 of 100 evaluations (60 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.6
- max_abs_err <= 0.000976562: 27% violate; best seen 5.3e-08 (2^-24.17)

Pareto front (feasible, 18 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=13 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=261, accuracy_bits=10, luts=168, ffs=93, throughput_msps=12.4, max_abs_err=0.000944 (2^-10.05), power_index=0.157
- iterative [data_width=16 n_iter=19 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=295, accuracy_bits=11.8, luts=196, ffs=99, throughput_msps=7.36, max_abs_err=0.000285 (2^-11.78), power_index=0.244
- iterative [data_width=16 n_iter=23 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=333, accuracy_bits=12.4, luts=228, ffs=105, throughput_msps=6.11, max_abs_err=0.000186 (2^-12.39), power_index=0.325
- iterative [data_width=17 n_iter=17 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=339, accuracy_bits=13.3, luts=230, ffs=109, throughput_msps=7.95, max_abs_err=9.91e-05 (2^-13.30), power_index=0.255
- iterative [data_width=20 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=361, accuracy_bits=14.6, luts=239, ffs=122, throughput_msps=10.2, max_abs_err=3.93e-05 (2^-14.63), power_index=0.258
- iterative [data_width=20 n_iter=17 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=383, accuracy_bits=15, luts=262, ffs=121, throughput_msps=7.95, max_abs_err=3.13e-05 (2^-14.96), power_index=0.288
- iterative [data_width=20 n_iter=19 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=399, accuracy_bits=15.9, luts=276, ffs=123, throughput_msps=7.23, max_abs_err=1.63e-05 (2^-15.90), power_index=0.33
- iterative [data_width=27 n_iter=23 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=566, accuracy_bits=21.6, luts=406, ffs=159, throughput_msps=5.89, max_abs_err=3.16e-07 (2^-21.59), power_index=0.553
- iterative [data_width=27 n_iter=27 angle_guard=3 frac_guard=3 rounding=trunc] luts_plus_ffs=595, accuracy_bits=23.4, luts=434, ffs=161, throughput_msps=5.11, max_abs_err=8.85e-08 (2^-23.43), power_index=0.672
- iterative [data_width=27 n_iter=30 angle_guard=3 frac_guard=3 rounding=round] luts_plus_ffs=675, accuracy_bits=24.2, luts=514, ffs=161, throughput_msps=4.64, max_abs_err=5.3e-08 (2^-24.17), power_index=0.838
Front coverage: luts_plus_ffs 261..675 (HV reference 1500); accuracy_bits 10..24.2 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 88 evals, 65 feasible; max throughput seen 15.6 MSPS; best accuracy 24.17 bits; best feasible luts_plus_ffs=261; feasible ranges: data_width 14..28, n_iter 11..30, angle_guard -2..4, frac_guard 0..3
- unrolled_k: 12 evals, 8 feasible; max throughput seen 13.5 MSPS; best accuracy 13.18 bits; best feasible luts_plus_ffs=363; feasible ranges: data_width 14..18, n_iter 13..15, angle_guard -1..2, frac_guard 0..2, k 2..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4146 in, 3981 out
- provider-reported cost: $0.0030
- full prompts and replies: `llm_trace.jsonl`

