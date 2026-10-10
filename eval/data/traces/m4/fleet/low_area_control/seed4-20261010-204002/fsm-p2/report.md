# DSE run: low_area_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 188 of 188 budgeted, over 3 round(s).  
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
  budget: 188 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=15,n_iter=23,angle_guard=2,frac_guard=1,rounding=trunc` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 182 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 96 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 162 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 6.23 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 26 | exact: schedule |
| latency_ns | 161 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.272 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000899 (2^-10.12) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 7.37 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.000305 (2^-11.68) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 2.5 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.1 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (22 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=23,angle_guard=2,frac_guard=1,rounding=trunc` | 182 | 96 | 6.2 | 26 | 0.272 | 0.000899 (2^-10.12) | 10.12 |
| 1 | `iterative:data_width=17,n_iter=15,angle_guard=0,frac_guard=0,rounding=trunc` | 181 | 101 | 11.0 | 18 | 0.191 | 0.000307 (2^-11.67) | 11.67 |
| 2 | `iterative:data_width=18,n_iter=14,angle_guard=-1,frac_guard=0,rounding=trunc` | 191 | 105 | 11.7 | 17 | 0.189 | 0.000265 (2^-11.88) | 11.88 |
| 3 | `iterative:data_width=17,n_iter=18,angle_guard=2,frac_guard=1,rounding=trunc` | 214 | 106 | 7.6 | 21 | 0.253 | 0.000174 (2^-12.49) | 12.49 |
| 4 | `iterative:data_width=17,n_iter=22,angle_guard=3,frac_guard=0,rounding=round` | 215 | 105 | 6.4 | 25 | 0.301 | 0.000146 (2^-12.74) | 12.74 |
| 5 | `iterative:data_width=20,n_iter=16,angle_guard=-2,frac_guard=0,rounding=trunc` | 212 | 114 | 10.2 | 19 | 0.233 | 9.85e-05 (2^-13.31) | 13.31 |
| 6 | `iterative:data_width=20,n_iter=16,angle_guard=-1,frac_guard=0,rounding=trunc` | 214 | 115 | 10.2 | 19 | 0.235 | 7.12e-05 (2^-13.78) | 13.78 |
| 7 | `iterative:data_width=19,n_iter=20,angle_guard=0,frac_guard=1,rounding=trunc` | 242 | 114 | 6.9 | 23 | 0.308 | 5.9e-05 (2^-14.05) | 14.05 |
| 8 | `iterative:data_width=21,n_iter=16,angle_guard=-1,frac_guard=1,rounding=trunc` | 235 | 122 | 10.2 | 19 | 0.255 | 4.8e-05 (2^-14.35) | 14.35 |
| 9 | `iterative:data_width=22,n_iter=16,angle_guard=-1,frac_guard=0,rounding=trunc` | 237 | 125 | 10.2 | 19 | 0.259 | 4.1e-05 (2^-14.57) | 14.57 |
| 10 | `iterative:data_width=20,n_iter=24,angle_guard=1,frac_guard=0,rounding=round` | 262 | 118 | 5.9 | 27 | 0.386 | 2.52e-05 (2^-15.28) | 15.28 |
| 11 | `iterative:data_width=21,n_iter=24,angle_guard=2,frac_guard=0,rounding=trunc` | 268 | 124 | 5.8 | 27 | 0.398 | 2.5e-05 (2^-15.29) | 15.29 |
| 12 | `iterative:data_width=21,n_iter=25,angle_guard=2,frac_guard=0,rounding=round` | 283 | 124 | 5.6 | 28 | 0.429 | 1.15e-05 (2^-16.41) | 16.41 |
| 13 | `iterative:data_width=22,n_iter=20,angle_guard=0,frac_guard=1,rounding=trunc` | 290 | 129 | 6.8 | 23 | 0.363 | 9.12e-06 (2^-16.74) | 16.74 |
| 14 | `iterative:data_width=21,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc` | 318 | 130 | 5.6 | 28 | 0.472 | 5.65e-06 (2^-17.43) | 17.43 |
| 15 | `iterative:data_width=24,n_iter=24,angle_guard=2,frac_guard=0,rounding=trunc` | 321 | 139 | 5.8 | 27 | 0.467 | 2.96e-06 (2^-18.37) | 18.37 |
| 16 | `iterative:data_width=24,n_iter=24,angle_guard=2,frac_guard=0,rounding=round` | 334 | 139 | 5.8 | 27 | 0.481 | 1.57e-06 (2^-19.28) | 19.28 |
| 17 | `iterative:data_width=24,n_iter=29,angle_guard=1,frac_guard=2,rounding=trunc` | 356 | 142 | 4.9 | 32 | 0.6 | 1.38e-06 (2^-19.47) | 19.47 |
| 18 | `iterative:data_width=24,n_iter=24,angle_guard=3,frac_guard=4,rounding=trunc` | 385 | 148 | 5.7 | 27 | 0.542 | 5.27e-07 (2^-20.86) | 20.86 |
| 19 | `iterative:data_width=27,n_iter=24,angle_guard=2,frac_guard=1,rounding=trunc` | 389 | 156 | 5.7 | 27 | 0.554 | 3.19e-07 (2^-21.58) | 21.58 |
| 20 | `iterative:data_width=27,n_iter=24,angle_guard=2,frac_guard=2,rounding=trunc` | 404 | 158 | 5.7 | 27 | 0.572 | 2.19e-07 (2^-22.12) | 22.12 |
| 21 | `iterative:data_width=27,n_iter=28,angle_guard=2,frac_guard=3,rounding=trunc` | 432 | 160 | 4.9 | 31 | 0.691 | 1.04e-07 (2^-23.20) | 23.20 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is min-area with a modest accuracy floor (max_abs_err <= 2^-10) and a trivial throughput floor (>= 1 MSPS). That makes it an area/accuracy problem, not a throughput problem, so the budget should go where the (luts_plus_ffs, accuracy_bits) trade-off lives. Iterative is the smallest family and already owns 15/16 of the merged front (best area 289), so it gets 80% of the budget over a wide W/N range that spans from the accuracy floor up to the 1500-area reference point. unrolled_k gets 20% only as a dominance check, since k chained rotations multiply area and buy throughput that the spec does not reward. The reserved end-of-run budget should map iterative's full ranges, as it is the family found on the front.*)
- `iterative` (80 evals): data_width=8..24, n_iter=4..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Smallest family in the registry: one shared datapath, N+3 cycles/result. It already holds 15/16 of the merged front with best feasible luts_plus_ffs 289, so it is the family that actually defines the area-accuracy trade-off here. Throughput is a non-issue: Fmax/(N+3) is far above the 1 MSPS floor for any N<=30, so the whole budget can go to area/accuracy. Ranges span the HV-relevant band: W 8..24 lets accuracy_bits reach ~22 while keeping area under the 1500 ref for most (W,N) pairs, and N 4..30 covers the accuracy floor (2^-10 needs roughly N>=10-12) up through the high-accuracy corner. Guards and rounding are left free because they trade a little area for accuracy and the model must decide that, not me.
- `unrolled_k` (20 evals): data_width=8..20, n_iter=4..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* Structurally dominated for this spec: k chained micro-rotations/cycle means roughly k copies of the iterative datapath, so area grows with k while the only thing it buys is throughput, which is not an objective (the 1 MSPS floor is already met by iterative). Fleet evidence agrees: 0/16 on the merged front, best area 391 vs 289 for iterative. Keep a small share purely to confirm the dominance and to catch any surprise where a small-k, small-W/N point lands on the front; ranges are capped tighter (W,N<=20) because anything larger is guaranteed to sit above the 1500 area ref.

**Result (code):** 100 evaluations this round, 100 total; 60 feasible; hypervolume 8115 (n/a).

**LLM decision:** `add_family` — The front is entirely iterative; unrolled_k was only lightly sampled (20 evals) and already shows higher throughput (25.5 vs 19.8 MSPS) though worse area (best 514). The spec's selection rule is min luts_plus_ffs, and iterative already reaches 278 at 10.1 bits — but the front's low-area corner is thin (only 2 designs under 300) and pipelined/pipelined_m families are completely unexplored, so we cannot yet claim the area-optimal corner is covered. Before spending the reserved budget on map_front, I want to test whether pipelined_m (register every m stages) can beat iterative's 278 LUT+FF at >=1 MSPS, since it gives 1 result/cycle with fewer registers than full pipelined. This round: probe pipelined_m across a wide range plus deepen unrolled_k around its feasible region.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 188.
Hypervolume of the feasible front: 8115 (gain this round: n/a (first round)).
Feasible designs: 60 of 100 evaluations (53 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 25.5
- max_abs_err <= 0.000976562: 40% violate; best seen 7.21e-06 (2^-17.08)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=23 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=278, accuracy_bits=10.1, luts=182, ffs=96, throughput_msps=6.23, max_abs_err=0.000899 (2^-10.12), power_index=0.272
- iterative [data_width=17 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=282, accuracy_bits=11.7, luts=181, ffs=101, throughput_msps=11, max_abs_err=0.000307 (2^-11.67), power_index=0.191
- iterative [data_width=17 n_iter=22 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=320, accuracy_bits=12.7, luts=215, ffs=105, throughput_msps=6.36, max_abs_err=0.000146 (2^-12.74), power_index=0.301
- iterative [data_width=18 n_iter=20 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=335, accuracy_bits=12.8, luts=226, ffs=109, throughput_msps=6.91, max_abs_err=0.000136 (2^-12.84), power_index=0.29
- iterative [data_width=18 n_iter=23 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=335, accuracy_bits=13.4, luts=227, ffs=108, throughput_msps=6.11, max_abs_err=9.26e-05 (2^-13.40), power_index=0.328
- iterative [data_width=19 n_iter=20 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=356, accuracy_bits=14, luts=242, ffs=114, throughput_msps=6.91, max_abs_err=5.9e-05 (2^-14.05), power_index=0.308
- iterative [data_width=20 n_iter=24 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=380, accuracy_bits=15.3, luts=262, ffs=118, throughput_msps=5.89, max_abs_err=2.52e-05 (2^-15.28), power_index=0.386
- iterative [data_width=22 n_iter=20 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=419, accuracy_bits=16.7, luts=290, ffs=129, throughput_msps=6.78, max_abs_err=9.12e-06 (2^-16.74), power_index=0.363
- iterative [data_width=22 n_iter=20 angle_guard=0 frac_guard=4 rounding=round] luts_plus_ffs=526, accuracy_bits=17, luts=391, ffs=135, throughput_msps=6.78, max_abs_err=7.68e-06 (2^-16.99), power_index=0.455
- iterative [data_width=23 n_iter=29 angle_guard=-1 frac_guard=4 rounding=round] luts_plus_ffs=574, accuracy_bits=17.1, luts=435, ffs=139, throughput_msps=4.79, max_abs_err=7.21e-06 (2^-17.08), power_index=0.691
Front coverage: luts_plus_ffs 278..574 (HV reference 1500); accuracy_bits 10.1..17.1 (HV reference 10); data_width on the front 15..23 (registry 8..28).

Per family:
- iterative: 80 evals, 51 feasible; max throughput seen 19.8 MSPS; best accuracy 17.08 bits; best feasible luts_plus_ffs=278; feasible ranges: data_width 15..23, n_iter 13..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 20 evals, 9 feasible; max throughput seen 25.5 MSPS; best accuracy 14.97 bits; best feasible luts_plus_ffs=514; feasible ranges: data_width 17..19, n_iter 15..20, angle_guard -2..4, frac_guard 0..4, k 4..6
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Add the two unexplored/low-coverage families to check whether the min-area corner can be beaten before committing the reserved budget to map_front.*)
- `unrolled_k` (13 evals): data_width=15..20, n_iter=13..22, angle_guard=-2..2, frac_guard=0..2, rounding=trunc|round, k=2..8. *Why:* Only 20 evals so far and best area 514; widen k down to 2 and data_width down to 15 to see if a low-area unrolled point exists near iterative's corner.
- clamped by code: fleet member: dropped families outside its assignment ['pipelined_m'] (allowed: ['iterative', 'unrolled_k'])

**Result (code):** 13 evaluations this round, 113 total; 71 feasible; hypervolume 8115 (+0.0%).

**LLM decision:** `stop` — Final round and the front is feasible and converged. Both spec constraints are met by designs on the front: throughput_msps >= 1 shows 0% violations (best seen 25.5 MSPS; every front point >= 4.79 MSPS), and max_abs_err <= 0.000976562 is satisfied by the whole front (worst front point 2^-10.12 = 0.000899), so `infeasible` is ruled out. The selection rule (min luts_plus_ffs) lands on iterative [data_width=15, n_iter=23, angle_guard=2, frac_guard=1, rounding=trunc] at luts_plus_ffs=278 with accuracy_bits=10.1 (max_abs_err 0.000899) and 6.23 MSPS — the cheapest feasible point and still above the 10-bit accuracy HV reference. Hypervolume stayed at 8115 with +0.0% gain this round over 113 of 188 evals (62 unique feasible designs), and round 2 explored both remaining families (unrolled_k best feasible area 423, well above iterative's 278; best accuracy 17.08 bits), indicating no further improvement to chase within the budget.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 75 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 113 of 188.
Hypervolume of the feasible front: 8115 (gain this round: +0.0%).
Feasible designs: 71 of 113 evaluations (62 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 25.5
- max_abs_err <= 0.000976562: 37% violate; best seen 7.21e-06 (2^-17.08)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=23 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=278, accuracy_bits=10.1, luts=182, ffs=96, throughput_msps=6.23, max_abs_err=0.000899 (2^-10.12), power_index=0.272
- iterative [data_width=17 n_iter=15 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=282, accuracy_bits=11.7, luts=181, ffs=101, throughput_msps=11, max_abs_err=0.000307 (2^-11.67), power_index=0.191
- iterative [data_width=17 n_iter=22 angle_guard=3 frac_guard=0 rounding=round] luts_plus_ffs=320, accuracy_bits=12.7, luts=215, ffs=105, throughput_msps=6.36, max_abs_err=0.000146 (2^-12.74), power_index=0.301
- iterative [data_width=18 n_iter=20 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=335, accuracy_bits=12.8, luts=226, ffs=109, throughput_msps=6.91, max_abs_err=0.000136 (2^-12.84), power_index=0.29
- iterative [data_width=18 n_iter=23 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=335, accuracy_bits=13.4, luts=227, ffs=108, throughput_msps=6.11, max_abs_err=9.26e-05 (2^-13.40), power_index=0.328
- iterative [data_width=19 n_iter=20 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=356, accuracy_bits=14, luts=242, ffs=114, throughput_msps=6.91, max_abs_err=5.9e-05 (2^-14.05), power_index=0.308
- iterative [data_width=20 n_iter=24 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=380, accuracy_bits=15.3, luts=262, ffs=118, throughput_msps=5.89, max_abs_err=2.52e-05 (2^-15.28), power_index=0.386
- iterative [data_width=22 n_iter=20 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=419, accuracy_bits=16.7, luts=290, ffs=129, throughput_msps=6.78, max_abs_err=9.12e-06 (2^-16.74), power_index=0.363
- iterative [data_width=22 n_iter=20 angle_guard=0 frac_guard=4 rounding=round] luts_plus_ffs=526, accuracy_bits=17, luts=391, ffs=135, throughput_msps=6.78, max_abs_err=7.68e-06 (2^-16.99), power_index=0.455
- iterative [data_width=23 n_iter=29 angle_guard=-1 frac_guard=4 rounding=round] luts_plus_ffs=574, accuracy_bits=17.1, luts=435, ffs=139, throughput_msps=4.79, max_abs_err=7.21e-06 (2^-17.08), power_index=0.691
Front coverage: luts_plus_ffs 278..574 (HV reference 1500); accuracy_bits 10.1..17.1 (HV reference 10); data_width on the front 15..23 (registry 8..28).

Per family:
- iterative: 80 evals, 51 feasible; max throughput seen 19.8 MSPS; best accuracy 17.08 bits; best feasible luts_plus_ffs=278; feasible ranges: data_width 15..23, n_iter 13..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 33 evals, 20 feasible; max throughput seen 25.5 MSPS; best accuracy 14.97 bits; best feasible luts_plus_ffs=423; feasible ranges: data_width 17..19, n_iter 15..20, angle_guard -2..4, frac_guard 0..4, k 2..8
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 75 evaluations*)
- `iterative` (75 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (13 front designs; box front_anchored)

**Result (code):** 75 evaluations this round, 188 total; 144 feasible; hypervolume 1.416e+04 (+74.4%).

**No LLM call** (code's front-mapping round): Final round and the front is feasible and converged. Both spec constraints are met by designs on the front: throughput_msps >= 1 shows 0% violations (best seen 25.5 MSPS; every front point >= 4.79 MSPS), and max_abs_err <= 0.000976562 is satisfied by the whole front (worst front point 2^-10.12 = 0.000899), so `infeasible` is ruled out. The selection rule (min luts_plus_ffs) lands on iterative [data_width=15, n_iter=23, angle_guard=2, frac_guard=1, rounding=trunc] at luts_plus_ffs=278 with accuracy_bits=10.1 (max_abs_err 0.000899) and 6.23 MSPS — the cheapest feasible point and still above the 10-bit accuracy HV reference. Hypervolume stayed at 8115 with +0.0% gain this round over 113 of 188 evals (62 unique feasible designs), and round 2 explored both remaining families (unrolled_k best feasible area 423, well above iterative's 278; best accuracy 17.08 bits), indicating no further improvement to chase within the budget.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 188 of 188.
Hypervolume of the feasible front: 1.416e+04 (gain this round: +74.4%).
Feasible designs: 144 of 188 evaluations (128 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 25.5
- max_abs_err <= 0.000976562: 23% violate; best seen 1.04e-07 (2^-23.20)

Pareto front (feasible, 22 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=23 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=278, accuracy_bits=10.1, luts=182, ffs=96, throughput_msps=6.23, max_abs_err=0.000899 (2^-10.12), power_index=0.272
- iterative [data_width=18 n_iter=14 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=296, accuracy_bits=11.9, luts=191, ffs=105, throughput_msps=11.7, max_abs_err=0.000265 (2^-11.88), power_index=0.189
- iterative [data_width=20 n_iter=16 angle_guard=-2 frac_guard=0 rounding=trunc] luts_plus_ffs=326, accuracy_bits=13.3, luts=212, ffs=114, throughput_msps=10.2, max_abs_err=9.85e-05 (2^-13.31), power_index=0.233
- iterative [data_width=19 n_iter=20 angle_guard=0 frac_guard=1 rounding=trunc] luts_plus_ffs=356, accuracy_bits=14, luts=242, ffs=114, throughput_msps=6.91, max_abs_err=5.9e-05 (2^-14.05), power_index=0.308
- iterative [data_width=22 n_iter=16 angle_guard=-1 frac_guard=0 rounding=trunc] luts_plus_ffs=362, accuracy_bits=14.6, luts=237, ffs=125, throughput_msps=10.2, max_abs_err=4.1e-05 (2^-14.57), power_index=0.259
- iterative [data_width=21 n_iter=25 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=407, accuracy_bits=16.4, luts=283, ffs=124, throughput_msps=5.57, max_abs_err=1.15e-05 (2^-16.41), power_index=0.429
- iterative [data_width=21 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=448, accuracy_bits=17.4, luts=318, ffs=130, throughput_msps=5.57, max_abs_err=5.65e-06 (2^-17.43), power_index=0.472
- iterative [data_width=24 n_iter=24 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=473, accuracy_bits=19.3, luts=334, ffs=139, throughput_msps=5.78, max_abs_err=1.57e-06 (2^-19.28), power_index=0.481
- iterative [data_width=27 n_iter=24 angle_guard=2 frac_guard=1 rounding=trunc] luts_plus_ffs=545, accuracy_bits=21.6, luts=389, ffs=156, throughput_msps=5.68, max_abs_err=3.19e-07 (2^-21.58), power_index=0.554
- iterative [data_width=27 n_iter=28 angle_guard=2 frac_guard=3 rounding=trunc] luts_plus_ffs=593, accuracy_bits=23.2, luts=432, ffs=160, throughput_msps=4.94, max_abs_err=1.04e-07 (2^-23.20), power_index=0.691
Front coverage: luts_plus_ffs 278..593 (HV reference 1500); accuracy_bits 10.1..23.2 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 155 evals, 124 feasible; max throughput seen 19.8 MSPS; best accuracy 23.20 bits; best feasible luts_plus_ffs=278; feasible ranges: data_width 15..28, n_iter 12..29, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 33 evals, 20 feasible; max throughput seen 25.5 MSPS; best accuracy 14.97 bits; best feasible luts_plus_ffs=423; feasible ranges: data_width 17..19, n_iter 15..20, angle_guard -2..4, frac_guard 0..4, k 2..8
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 8279 in, 7655 out
- provider-reported cost: $0.0091
- full prompts and replies: `llm_trace.jsonl`

