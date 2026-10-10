# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
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
`iterative:data_width=14,n_iter=12,angle_guard=2,frac_guard=2,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 161 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 92 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 13.2 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 15 | exact: schedule |
| latency_ns | 75.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.143 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000894 (2^-10.13) | exact: bit-accurate model, exhaustive (16384 angles) |
| max_abs_err_lsb | 3.66 | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err | 0.000262 (2^-11.90) | exact: bit-accurate model, exhaustive (16384 angles) |
| rms_err_lsb | 1.07 | exact: bit-accurate model, exhaustive (16384 angles) |
| accuracy_bits | 10.1 | exact: bit-accurate model, exhaustive (16384 angles) |

## Pareto front (15 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=14,n_iter=12,angle_guard=2,frac_guard=2,rounding=trunc` | 161 | 92 | 13.2 | 15 | 0.143 | 0.000894 (2^-10.13) | 10.13 |
| 1 | `iterative:data_width=15,n_iter=12,angle_guard=2,frac_guard=1,rounding=trunc` | 163 | 95 | 13.2 | 15 | 0.145 | 0.000811 (2^-10.27) | 10.27 |
| 2 | `iterative:data_width=15,n_iter=13,angle_guard=1,frac_guard=0,rounding=round` | 168 | 92 | 12.4 | 16 | 0.156 | 0.000673 (2^-10.54) | 10.54 |
| 3 | `iterative:data_width=15,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc` | 181 | 97 | 12.4 | 16 | 0.168 | 0.000466 (2^-11.07) | 11.07 |
| 4 | `iterative:data_width=15,n_iter=13,angle_guard=2,frac_guard=2,rounding=round` | 221 | 97 | 12.4 | 16 | 0.191 | 0.000431 (2^-11.18) | 11.18 |
| 5 | `unrolled_k:data_width=15,n_iter=14,angle_guard=2,frac_guard=2,rounding=trunc,k=2` | 270 | 96 | 10.5 | 10 | 0.138 | 0.000405 (2^-11.27) | 11.27 |
| 6 | `unrolled_k:data_width=16,n_iter=13,angle_guard=2,frac_guard=2,rounding=trunc,k=2` | 286 | 101 | 10.5 | 10 | 0.146 | 0.000378 (2^-11.37) | 11.37 |
| 7 | `iterative:data_width=20,n_iter=26,angle_guard=-2,frac_guard=1,rounding=round` | 316 | 117 | 5.5 | 29 | 0.473 | 0.0001 (2^-13.28) | 13.28 |
| 8 | `iterative:data_width=22,n_iter=21,angle_guard=4,frac_guard=0,rounding=round` | 303 | 131 | 6.5 | 24 | 0.392 | 5.23e-06 (2^-17.54) | 17.54 |
| 9 | `iterative:data_width=24,n_iter=21,angle_guard=4,frac_guard=0,rounding=trunc` | 324 | 141 | 6.4 | 24 | 0.42 | 3.19e-06 (2^-18.26) | 18.26 |
| 10 | `iterative:data_width=22,n_iter=26,angle_guard=4,frac_guard=4,rounding=trunc` | 358 | 139 | 5.4 | 29 | 0.542 | 1.68e-06 (2^-19.18) | 19.18 |
| 11 | `iterative:data_width=23,n_iter=29,angle_guard=2,frac_guard=4,rounding=trunc` | 375 | 142 | 4.8 | 32 | 0.623 | 1.43e-06 (2^-19.41) | 19.41 |
| 12 | `iterative:data_width=23,n_iter=26,angle_guard=4,frac_guard=4,rounding=trunc` | 377 | 144 | 5.3 | 29 | 0.569 | 8.73e-07 (2^-20.13) | 20.13 |
| 13 | `iterative:data_width=23,n_iter=28,angle_guard=4,frac_guard=3,rounding=round` | 423 | 142 | 4.9 | 31 | 0.66 | 5.73e-07 (2^-20.73) | 20.73 |
| 14 | `iterative:data_width=28,n_iter=28,angle_guard=4,frac_guard=3,rounding=round` | 529 | 167 | 4.9 | 31 | 0.812 | 2.42e-08 (2^-25.30) | 25.30 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-dominated (min luts_plus_ffs) with a hard throughput floor of 1 MSPS and a hard accuracy floor of 2^-10. Only iterative and unrolled_k are available to me. iterative is the natural starting point because it has the smallest area footprint; the question is whether its Fmax is high enough to deliver 1 MSPS. unrolled_k is the fallback that buys throughput with area. I focus the search on the narrow W=12-16, N=10-14 window because the 2^-10 error bound is tight enough that W<12 or N<10 will likely violate it, while W>16 or N>14 adds area without improving the selection objective. Guard bits are kept minimal (0-2) to avoid paying area for accuracy headroom the spec does not require. Both rounding modes are included because truncation is cheaper and may still meet the error bound, while rounding may be needed at the edge of the N/W range. The budget is split between the two families so that if iterative cannot meet throughput, unrolled_k results are already available to map the feasible front. Since no fleet facts exist yet, I allocate the full 100-eval budget across these two families in a single round to get an initial Pareto picture before deciding on any refinement.*)
- `iterative` (30 evals): data_width=12..16, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* iterative is the lowest-area family in the registry (shared datapath, no pipeline registers). It is the only family that can plausibly minimise luts_plus_ffs while still meeting the >=1 MSPS throughput constraint at a realistic Fmax. I narrow data_width to 12-16 and n_iter to 10-14 because the error constraint (<= 2^-10) is the binding accuracy requirement; W=12 with N~12 typically gives ~10-11 bits of accuracy, and going much wider or deeper wastes area without helping the selection rule (min luts_plus_ffs). angle_guard and frac_guard are kept small (0-2) since extra guard bits add area but only marginally improve accuracy beyond the 2^-10 floor. Both rounding modes are included to let the search find the cheapest rounding that still meets the error bound.
- `unrolled_k` (30 evals): data_width=12..16, n_iter=10..14, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* unrolled_k trades some area (k parallel datapath elements) for higher throughput per cycle. If iterative at a given W/N cannot hit >=1 MSPS at its Fmax, unrolled_k with k=2-4 can multiply throughput by k at the cost of roughly kx the datapath LUTs. I keep the same W/N/guard ranges as iterative so the accuracy trade-off is comparable, and limit k to 2-4 because k>4 would multiply area too aggressively for a spec where area is the primary objective. This family covers the part of the Pareto front where a slightly larger area buys enough throughput margin to allow a lower-Fmax (and thus potentially lower-area) configuration, or where iterative simply cannot meet 1 MSPS.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 60 evaluations this round, 60 total; 25 feasible; hypervolume 2148 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established and robust. The minimum area design (iterative, 253 LUTs+FFs) comfortably meets the throughput constraint (13.2 MSPS >> 1 MSPS) and the accuracy constraint (10.13 bits > 10 bits). The front extends to higher accuracy (11.9 bits) with modest area increases, providing a good trade-off curve. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (253) as per the spec's selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 2148 (gain this round: n/a (first round)).
Feasible designs: 25 of 60 evaluations (18 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.3
- max_abs_err <= 0.000976562: 58% violate; best seen 0.00027 (2^-11.85)

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=253, accuracy_bits=10.1, luts=161, ffs=92, throughput_msps=13.2, max_abs_err=0.000894 (2^-10.13), power_index=0.143
- iterative [data_width=15 n_iter=12 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=258, accuracy_bits=10.3, luts=163, ffs=95, throughput_msps=13.2, max_abs_err=0.000811 (2^-10.27), power_index=0.145
- iterative [data_width=15 n_iter=13 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.5, luts=168, ffs=92, throughput_msps=12.4, max_abs_err=0.000673 (2^-10.54), power_index=0.156
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=278, accuracy_bits=11.1, luts=181, ffs=97, throughput_msps=12.4, max_abs_err=0.000466 (2^-11.07), power_index=0.168
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=317, accuracy_bits=11.2, luts=221, ffs=97, throughput_msps=12.4, max_abs_err=0.000431 (2^-11.18), power_index=0.191
- unrolled_k [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=366, accuracy_bits=11.3, luts=270, ffs=96, throughput_msps=10.5, max_abs_err=0.000405 (2^-11.27), power_index=0.138
- unrolled_k [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=387, accuracy_bits=11.4, luts=286, ffs=101, throughput_msps=10.5, max_abs_err=0.000378 (2^-11.37), power_index=0.146
- unrolled_k [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc k=4] luts_plus_ffs=493, accuracy_bits=11.9, luts=393, ffs=100, throughput_msps=10.3, max_abs_err=0.00027 (2^-11.85), power_index=0.13
Front coverage: luts_plus_ffs 253..493 (HV reference 1500); accuracy_bits 10.1..11.9 (HV reference 10); data_width on the front 14..16 (registry 8..28).

Per family:
- iterative: 30 evals, 14 feasible; max throughput seen 15.3 MSPS; best accuracy 11.18 bits; best feasible luts_plus_ffs=253; feasible ranges: data_width 14..15, n_iter 12..13, angle_guard 0..2, frac_guard 0..2
- unrolled_k: 30 evals, 11 feasible; max throughput seen 14 MSPS; best accuracy 11.85 bits; best feasible luts_plus_ffs=350; feasible ranges: data_width 14..16, n_iter 13..14, angle_guard 2..2, frac_guard 1..2, k 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (25 evals): data_width=13..28, n_iter=10..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (5 front designs; box front_anchored)
- `unrolled_k` (15 evals): data_width=14..28, n_iter=11..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (3 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 63 feasible; hypervolume 1.507e+04 (+601.9%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and robust. The minimum area design (iterative, 253 LUTs+FFs) comfortably meets the throughput constraint (13.2 MSPS >> 1 MSPS) and the accuracy constraint (10.13 bits > 10 bits). The front extends to higher accuracy (11.9 bits) with modest area increases, providing a good trade-off curve. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (253) as per the spec's selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.507e+04 (gain this round: +601.9%).
Feasible designs: 63 of 100 evaluations (53 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 15.3
- max_abs_err <= 0.000976562: 37% violate; best seen 2.42e-08 (2^-25.30)

Pareto front (feasible, 15 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=14 n_iter=12 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=253, accuracy_bits=10.1, luts=161, ffs=92, throughput_msps=13.2, max_abs_err=0.000894 (2^-10.13), power_index=0.143
- iterative [data_width=15 n_iter=13 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.5, luts=168, ffs=92, throughput_msps=12.4, max_abs_err=0.000673 (2^-10.54), power_index=0.156
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=278, accuracy_bits=11.1, luts=181, ffs=97, throughput_msps=12.4, max_abs_err=0.000466 (2^-11.07), power_index=0.168
- unrolled_k [data_width=15 n_iter=14 angle_guard=2 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=366, accuracy_bits=11.3, luts=270, ffs=96, throughput_msps=10.5, max_abs_err=0.000405 (2^-11.27), power_index=0.138
- unrolled_k [data_width=16 n_iter=13 angle_guard=2 frac_guard=2 rounding=trunc k=2] luts_plus_ffs=387, accuracy_bits=11.4, luts=286, ffs=101, throughput_msps=10.5, max_abs_err=0.000378 (2^-11.37), power_index=0.146
- iterative [data_width=22 n_iter=21 angle_guard=4 frac_guard=0 rounding=round] luts_plus_ffs=434, accuracy_bits=17.5, luts=303, ffs=131, throughput_msps=6.5, max_abs_err=5.23e-06 (2^-17.54), power_index=0.392
- iterative [data_width=24 n_iter=21 angle_guard=4 frac_guard=0 rounding=trunc] luts_plus_ffs=465, accuracy_bits=18.3, luts=324, ffs=141, throughput_msps=6.39, max_abs_err=3.19e-06 (2^-18.26), power_index=0.42
- iterative [data_width=23 n_iter=29 angle_guard=2 frac_guard=4 rounding=trunc] luts_plus_ffs=517, accuracy_bits=19.4, luts=375, ffs=142, throughput_msps=4.79, max_abs_err=1.43e-06 (2^-19.41), power_index=0.623
- iterative [data_width=23 n_iter=26 angle_guard=4 frac_guard=4 rounding=trunc] luts_plus_ffs=521, accuracy_bits=20.1, luts=377, ffs=144, throughput_msps=5.28, max_abs_err=8.73e-07 (2^-20.13), power_index=0.569
- iterative [data_width=28 n_iter=28 angle_guard=4 frac_guard=3 rounding=round] luts_plus_ffs=696, accuracy_bits=25.3, luts=529, ffs=167, throughput_msps=4.86, max_abs_err=2.42e-08 (2^-25.30), power_index=0.812
Front coverage: luts_plus_ffs 253..696 (HV reference 1500); accuracy_bits 10.1..25.3 (HV reference 10); data_width on the front 14..28 (registry 8..28).

Per family:
- iterative: 55 evals, 38 feasible; max throughput seen 15.3 MSPS; best accuracy 25.30 bits; best feasible luts_plus_ffs=253; feasible ranges: data_width 14..28, n_iter 12..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 45 evals, 25 feasible; max throughput seen 14 MSPS; best accuracy 19.11 bits; best feasible luts_plus_ffs=350; feasible ranges: data_width 14..24, n_iter 12..28, angle_guard -2..4, frac_guard 0..4, k 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4391 in, 1363 out
- provider-reported cost: $0.0043
- full prompts and replies: `llm_trace.jsonl`

