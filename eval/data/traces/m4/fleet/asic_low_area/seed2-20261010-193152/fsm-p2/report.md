# DSE run: asic_low_area

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_low_area: Motor-control sin/cos in sky130 standard cells: >= 1 MSPS, max error <= 2^-10. Area is everything: minimise cell area.
  target: asic-sky130hd
  constraint: throughput_msps >= 1
  constraint: max_abs_err <= 0.000976562
  objective: min area_um2 (HV ref 40000)
  objective: max accuracy_bits (HV ref 10)
  select: min area_um2
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`iterative:data_width=15,n_iter=13,angle_guard=2,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 6997 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 1864 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 101 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 136 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 8.5 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 118 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 0.155 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000642 (2^-10.61) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 5.26 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00017 (2^-12.52) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.39 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.6 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (18 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=13,angle_guard=2,frac_guard=0,rounding=round` | 6997 | 101 | 8.5 | 16 | 0.155 | 0.000642 (2^-10.61) | 10.61 |
| 1 | `iterative:data_width=15,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 7057 | 101 | 8.0 | 17 | 0.166 | 0.000599 (2^-10.71) | 10.71 |
| 2 | `iterative:data_width=15,n_iter=17,angle_guard=1,frac_guard=1,rounding=trunc` | 7293 | 103 | 7.1 | 20 | 0.2 | 0.000594 (2^-10.72) | 10.72 |
| 3 | `iterative:data_width=15,n_iter=17,angle_guard=3,frac_guard=1,rounding=trunc` | 7420 | 105 | 6.5 | 20 | 0.204 | 0.000586 (2^-10.74) | 10.74 |
| 4 | `iterative:data_width=14,n_iter=14,angle_guard=3,frac_guard=3,rounding=trunc` | 7425 | 103 | 8.0 | 17 | 0.172 | 0.000502 (2^-10.96) | 10.96 |
| 5 | `iterative:data_width=16,n_iter=16,angle_guard=0,frac_guard=0,rounding=round` | 7431 | 104 | 7.4 | 19 | 0.193 | 0.000373 (2^-11.39) | 11.39 |
| 6 | `iterative:data_width=16,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 7509 | 106 | 7.3 | 18 | 0.186 | 0.000285 (2^-11.78) | 11.78 |
| 7 | `iterative:data_width=17,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 7777 | 111 | 7.7 | 17 | 0.182 | 0.000204 (2^-12.26) | 12.26 |
| 8 | `iterative:data_width=17,n_iter=18,angle_guard=1,frac_guard=0,rounding=round` | 8059 | 112 | 6.2 | 21 | 0.23 | 0.000149 (2^-12.71) | 12.71 |
| 9 | `iterative:data_width=18,n_iter=17,angle_guard=3,frac_guard=2,rounding=trunc` | 9025 | 124 | 5.9 | 20 | 0.244 | 5.67e-05 (2^-14.11) | 14.11 |
| 10 | `iterative:data_width=18,n_iter=20,angle_guard=3,frac_guard=3,rounding=trunc` | 9528 | 126 | 5.1 | 23 | 0.29 | 3.81e-05 (2^-14.68) | 14.68 |
| 11 | `iterative:data_width=21,n_iter=17,angle_guard=2,frac_guard=0,rounding=trunc` | 9603 | 135 | 5.5 | 20 | 0.263 | 3.12e-05 (2^-14.97) | 14.97 |
| 12 | `iterative:data_width=21,n_iter=18,angle_guard=1,frac_guard=0,rounding=trunc` | 9613 | 134 | 5.4 | 21 | 0.275 | 2.55e-05 (2^-15.26) | 15.26 |
| 13 | `iterative:data_width=21,n_iter=19,angle_guard=1,frac_guard=0,rounding=trunc` | 9673 | 134 | 5.2 | 22 | 0.289 | 2.36e-05 (2^-15.37) | 15.37 |
| 14 | `iterative:data_width=21,n_iter=19,angle_guard=1,frac_guard=0,rounding=round` | 9892 | 134 | 5.2 | 22 | 0.291 | 1.29e-05 (2^-16.24) | 16.24 |
| 15 | `iterative:data_width=21,n_iter=20,angle_guard=2,frac_guard=3,rounding=round` | 12834 | 141 | 4.6 | 23 | 0.354 | 5.18e-06 (2^-17.56) | 17.56 |
| 16 | `iterative:data_width=23,n_iter=23,angle_guard=4,frac_guard=2,rounding=round` | 13953 | 152 | 3.8 | 26 | 0.434 | 1.08e-06 (2^-19.83) | 19.83 |
| 17 | `iterative:data_width=26,n_iter=26,angle_guard=0,frac_guard=4,rounding=trunc` | 14101 | 169 | 3.1 | 29 | 0.513 | 5.63e-07 (2^-20.76) | 20.76 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec is area-first with a loose throughput floor (>=1 MSPS) and a 2^-10 error ceiling, which is exactly the regime where the shared-datapath iterative family wins: it already holds all 20 merged-front designs with a best feasible area of 7254 um^2, while unrolled_k (12500), pipelined (34059) and pipelined_m (18385) are all dominated. Accuracy depends only on data_width/n_iter/angle_guard/frac_guard/rounding, so the useful search axis is the accuracy-vs-area curve: I sweep data_width 10-22 and n_iter 9-24 to cover both the minimum-area feasible corner (where error just crosses 2^-10) and the higher-accuracy points that fill the hypervolume up to the 40000 um^2 reference, with guards and rounding left open because they trade a little area for error margin. A 15% share on unrolled_k is a cheap confirmation that it cannot contribute a niche point to the front.*)
- `iterative` (85 evals): data_width=10..22, n_iter=9..24, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round. *Why:* Iterative owns the entire merged front (20/20 designs, best feasible area 7254 um^2) and the >=1 MSPS constraint is trivially met at N+3 cycles/result, so area is the only real pressure. The box spans the low-area/low-accuracy corner (W~12, N~11, where max_abs_err first drops under 2^-10) up to high-accuracy points (W~20-22, N~20+) that extend the front toward the HV reference area of 40000.
- `unrolled_k` (15 evals): data_width=10..18, n_iter=9..18, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, k=2..4. *Why:* Only 9 evals so far (3 feasible, best area 12500 vs iterative's 7254) and 0/20 on the front, so it is almost certainly dominated: k chained micro-rotations duplicate the datapath while throughput is not an objective. A small share with small k (2-4) confirms whether fixed-shift stages can ever undercut the iterative barrel-shifter datapath at equal accuracy, without stealing budget from the family that actually defines the front.

**Result (code):** 100 evaluations this round, 100 total; 65 feasible; hypervolume 2.314e+05 (n/a).

**LLM decision:** `map_front` — The feasible front is narrow and entirely one family: all 13 Pareto designs are `iterative`, spanning area_um2 7149..12834 and accuracy_bits 10.2..17.6, while the registry permits data_width up to 28 and n_iter up to 30 (so accuracy well beyond 17.6 bits is reachable) and the HV reference area is 40000. The front therefore covers only a small slice of the accuracy objective's range, and the low-area corner (7149 um2, accuracy 10.2 bits) sits right against the 2^-10 constraint, so there is a narrow unexplored window between 10.0 and 10.2 bits where a smaller-area design could still be feasible. With 100 evals left in the budget, the right move is to let NSGA-II map the whole front over the full ranges of the families already on it (iterative, and unrolled_k which had 4 feasible designs but none on the front), seeded with the current front — this both pushes the low-area corner down and extends the high-accuracy end, maximising hypervolume coverage rather than over-focusing on one corner.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 2.314e+05 (gain this round: n/a (first round)).
Feasible designs: 65 of 100 evaluations (54 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11.5
- max_abs_err <= 0.000976562: 35% violate; best seen 5.18e-06 (2^-17.56)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=16 n_iter=15 angle_guard=-1 frac_guard=0 rounding=trunc] area_um2=7149, accuracy_bits=10.2, ffs=103, throughput_msps=7.86, max_abs_err=0.000829 (2^-10.24), power_index=0.179
- iterative [data_width=16 n_iter=14 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=7228, accuracy_bits=10.6, ffs=105, throughput_msps=8, max_abs_err=0.000643 (2^-10.60), power_index=0.172
- iterative [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=7619, accuracy_bits=11.5, ffs=111, throughput_msps=7.7, max_abs_err=0.000338 (2^-11.53), power_index=0.181
- iterative [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] area_um2=7777, accuracy_bits=12.3, ffs=111, throughput_msps=7.7, max_abs_err=0.000204 (2^-12.26), power_index=0.182
- iterative [data_width=17 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] area_um2=8059, accuracy_bits=12.7, ffs=112, throughput_msps=6.24, max_abs_err=0.000149 (2^-12.71), power_index=0.23
- iterative [data_width=18 n_iter=20 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=9528, accuracy_bits=14.7, ffs=126, throughput_msps=5.12, max_abs_err=3.81e-05 (2^-14.68), power_index=0.29
- iterative [data_width=21 n_iter=17 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=9603, accuracy_bits=15, ffs=135, throughput_msps=5.52, max_abs_err=3.12e-05 (2^-14.97), power_index=0.263
- iterative [data_width=21 n_iter=18 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=9613, accuracy_bits=15.3, ffs=134, throughput_msps=5.42, max_abs_err=2.55e-05 (2^-15.26), power_index=0.275
- iterative [data_width=21 n_iter=19 angle_guard=1 frac_guard=0 rounding=round] area_um2=9892, accuracy_bits=16.2, ffs=134, throughput_msps=5.18, max_abs_err=1.29e-05 (2^-16.24), power_index=0.291
- iterative [data_width=21 n_iter=20 angle_guard=2 frac_guard=3 rounding=round] area_um2=12834, accuracy_bits=17.6, ffs=141, throughput_msps=4.65, max_abs_err=5.18e-06 (2^-17.56), power_index=0.354
Front coverage: area_um2 7149..12834 (HV reference 40000); accuracy_bits 10.2..17.6 (HV reference 10); data_width on the front 15..21 (registry 8..28).

Per family:
- iterative: 85 evals, 61 feasible; max throughput seen 11.5 MSPS; best accuracy 17.56 bits; best feasible area_um2=7149; feasible ranges: data_width 14..22, n_iter 13..24, angle_guard -2..3, frac_guard 0..3
- unrolled_k: 15 evals, 4 feasible; max throughput seen 10.7 MSPS; best accuracy 11.42 bits; best feasible area_um2=12012; feasible ranges: data_width 16..17, n_iter 13..15, angle_guard -1..0, frac_guard 0..1, k 3..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `iterative` (20 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (13 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 85 feasible; hypervolume 3.148e+05 (+36.0%).

**LLM decision:** `refine` — Front is entirely `iterative`; unrolled_k is dominated (12012 um^2 / 11.42 bits) and throughput is not binding (0% violations, min front throughput 3.12 MSPS >> 1 MSPS), so adding pipelined families would only inflate area. Refine both ends of the front instead.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 3.148e+05 (gain this round: +36.0%).
Feasible designs: 85 of 120 evaluations (72 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11.5
- max_abs_err <= 0.000976562: 29% violate; best seen 5.63e-07 (2^-20.76)

Pareto front (feasible, 15 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=16 n_iter=15 angle_guard=-1 frac_guard=0 rounding=trunc] area_um2=7149, accuracy_bits=10.2, ffs=103, throughput_msps=7.86, max_abs_err=0.000829 (2^-10.24), power_index=0.179
- iterative [data_width=16 n_iter=16 angle_guard=0 frac_guard=0 rounding=round] area_um2=7431, accuracy_bits=11.4, ffs=104, throughput_msps=7.45, max_abs_err=0.000373 (2^-11.39), power_index=0.193
- iterative [data_width=17 n_iter=14 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=7619, accuracy_bits=11.5, ffs=111, throughput_msps=7.7, max_abs_err=0.000338 (2^-11.53), power_index=0.181
- iterative [data_width=17 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] area_um2=8059, accuracy_bits=12.7, ffs=112, throughput_msps=6.24, max_abs_err=0.000149 (2^-12.71), power_index=0.23
- iterative [data_width=18 n_iter=17 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=9025, accuracy_bits=14.1, ffs=124, throughput_msps=5.89, max_abs_err=5.67e-05 (2^-14.11), power_index=0.244
- iterative [data_width=21 n_iter=17 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=9603, accuracy_bits=15, ffs=135, throughput_msps=5.52, max_abs_err=3.12e-05 (2^-14.97), power_index=0.263
- iterative [data_width=21 n_iter=18 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=9613, accuracy_bits=15.3, ffs=134, throughput_msps=5.42, max_abs_err=2.55e-05 (2^-15.26), power_index=0.275
- iterative [data_width=21 n_iter=19 angle_guard=1 frac_guard=0 rounding=round] area_um2=9892, accuracy_bits=16.2, ffs=134, throughput_msps=5.18, max_abs_err=1.29e-05 (2^-16.24), power_index=0.291
- iterative [data_width=21 n_iter=20 angle_guard=2 frac_guard=3 rounding=round] area_um2=12834, accuracy_bits=17.6, ffs=141, throughput_msps=4.65, max_abs_err=5.18e-06 (2^-17.56), power_index=0.354
- iterative [data_width=26 n_iter=26 angle_guard=0 frac_guard=4 rounding=trunc] area_um2=14101, accuracy_bits=20.8, ffs=169, throughput_msps=3.12, max_abs_err=5.63e-07 (2^-20.76), power_index=0.513
Front coverage: area_um2 7149..14101 (HV reference 40000); accuracy_bits 10.2..20.8 (HV reference 10); data_width on the front 16..26 (registry 8..28).

Per family:
- iterative: 105 evals, 81 feasible; max throughput seen 11.5 MSPS; best accuracy 20.76 bits; best feasible area_um2=7149; feasible ranges: data_width 14..26, n_iter 13..28, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 15 evals, 4 feasible; max throughput seen 10.7 MSPS; best accuracy 11.42 bits; best feasible area_um2=12012; feasible ranges: data_width 16..17, n_iter 13..15, angle_guard -1..0, frac_guard 0..1, k 3..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *The feasible front is 100% `iterative`; `unrolled_k` was already sampled (15 evals) and is fully dominated on this spec (best feasible area 12012 > 7149, best accuracy 11.42 << 20.76). The throughput constraint is a non-issue (0% violations, worst front point still 3.12 MSPS vs the 1 MSPS floor), so pipelined/pipelined_m and higher k cannot help an area-first spec. Two things are still loose: (1) the min-area corner, where the current winner (7149 um^2, 10.24 bits) sits only 0.24 bit inside the error constraint and data_width=14 already proved feasible, so the true area minimum is unpinned; (2) the accuracy ceiling, where the front ends at 20.8 bits against a registry limit of W=28/N=30, leaving HV on the table. Refining those two ends is better use of the 80 remaining evals than another broad map, and the reserved end-of-run mapping pass can still cover the full front afterwards.*)
- `iterative` (80 evals): data_width=12..17, n_iter=13..22, angle_guard=-2..3, frac_guard=0..3, rounding=trunc|round. *Why:* Low-area corner: the selection rule is min area_um2 and the front's cheapest point (W=16,n=15 -> 7149) sits only 0.24 bit above the 2^-10 error constraint, so the true minimum-area feasible point is very likely just below it in width. data_width=14 was already seen feasible, so 12..17 will pin the feasibility boundary in W and find designs cheaper than 7149.
- clamped by code: dropped duplicate family iterative

**Result (code):** 80 evaluations this round, 200 total; 145 feasible; hypervolume 3.151e+05 (+0.1%).

**LLM decision:** `stop` — Final round with the 200-eval budget fully spent. The front is feasible and non-degenerate: 145/200 evaluations feasible (121 unique), 18 Pareto designs spanning area_um2 6997..14101 and accuracy_bits 10.6..20.8, with 0% throughput violations (best 11.5 MSPS vs the >=1 MSPS constraint) and the error constraint met by every front point (best 5.63e-07 = 2^-20.76 vs the 2^-10 limit). The selection rule (min area_um2) is satisfied by iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=0 rounding=round] at 6997 um^2 with max_abs_err 0.000642 (2^-10.61), i.e. within spec. Both registry families have been explored (iterative 185 evals, unrolled_k 15 evals with no better area than 12012 um^2), and hypervolume gained only +0.1% this round, so further search is not worth it. No infeasibility: no constraint is unreachable.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 3.151e+05 (gain this round: +0.1%).
Feasible designs: 145 of 200 evaluations (121 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 11.5
- max_abs_err <= 0.000976562: 28% violate; best seen 5.63e-07 (2^-20.76)

Pareto front (feasible, 18 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- iterative [data_width=15 n_iter=13 angle_guard=2 frac_guard=0 rounding=round] area_um2=6997, accuracy_bits=10.6, ffs=101, throughput_msps=8.5, max_abs_err=0.000642 (2^-10.61), power_index=0.155
- iterative [data_width=15 n_iter=17 angle_guard=1 frac_guard=1 rounding=trunc] area_um2=7293, accuracy_bits=10.7, ffs=103, throughput_msps=7.08, max_abs_err=0.000594 (2^-10.72), power_index=0.2
- iterative [data_width=14 n_iter=14 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=7425, accuracy_bits=11, ffs=103, throughput_msps=8, max_abs_err=0.000502 (2^-10.96), power_index=0.172
- iterative [data_width=16 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] area_um2=7509, accuracy_bits=11.8, ffs=106, throughput_msps=7.27, max_abs_err=0.000285 (2^-11.78), power_index=0.186
- iterative [data_width=17 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] area_um2=8059, accuracy_bits=12.7, ffs=112, throughput_msps=6.24, max_abs_err=0.000149 (2^-12.71), power_index=0.23
- iterative [data_width=18 n_iter=17 angle_guard=3 frac_guard=2 rounding=trunc] area_um2=9025, accuracy_bits=14.1, ffs=124, throughput_msps=5.89, max_abs_err=5.67e-05 (2^-14.11), power_index=0.244
- iterative [data_width=21 n_iter=17 angle_guard=2 frac_guard=0 rounding=trunc] area_um2=9603, accuracy_bits=15, ffs=135, throughput_msps=5.52, max_abs_err=3.12e-05 (2^-14.97), power_index=0.263
- iterative [data_width=21 n_iter=19 angle_guard=1 frac_guard=0 rounding=trunc] area_um2=9673, accuracy_bits=15.4, ffs=134, throughput_msps=5.18, max_abs_err=2.36e-05 (2^-15.37), power_index=0.289
- iterative [data_width=21 n_iter=20 angle_guard=2 frac_guard=3 rounding=round] area_um2=12834, accuracy_bits=17.6, ffs=141, throughput_msps=4.65, max_abs_err=5.18e-06 (2^-17.56), power_index=0.354
- iterative [data_width=26 n_iter=26 angle_guard=0 frac_guard=4 rounding=trunc] area_um2=14101, accuracy_bits=20.8, ffs=169, throughput_msps=3.12, max_abs_err=5.63e-07 (2^-20.76), power_index=0.513
Front coverage: area_um2 6997..14101 (HV reference 40000); accuracy_bits 10.6..20.8 (HV reference 10); data_width on the front 14..26 (registry 8..28).

Per family:
- iterative: 185 evals, 141 feasible; max throughput seen 11.5 MSPS; best accuracy 20.76 bits; best feasible area_um2=6997; feasible ranges: data_width 13..26, n_iter 13..28, angle_guard -2..4, frac_guard 0..4
- unrolled_k: 15 evals, 4 feasible; max throughput seen 10.7 MSPS; best accuracy 11.42 bits; best feasible area_um2=12012; feasible ranges: data_width 16..17, n_iter 13..15, angle_guard -1..0, frac_guard 0..1, k 3..4
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 11694 in, 12849 out
- provider-reported cost: $0.0111
- full prompts and replies: `llm_trace.jsonl`

