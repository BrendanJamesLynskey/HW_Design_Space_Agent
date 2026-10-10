# DSE run: asic_power_50msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 200 of 200 budgeted, over 3 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_power_50msps: A 50 MSPS sin/cos unit in sky130 standard cells for a battery-powered radio: max error <= 2^-12. Minimise the relative power index; accuracy is the trade-off.
  target: asic-sky130hd
  constraint: throughput_msps >= 50
  constraint: max_abs_err <= 0.000244141
  objective: min power_index (HV ref 40)
  objective: max accuracy_bits (HV ref 12)
  select: min power_index
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=3` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 27943 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 7444 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 340 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 135 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.77 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000175 (2^-12.48) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 11.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.28e-05 (2^-14.21) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.46 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (7 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round,m=3` | 27943 | 340 | 51.9 | 7 | 1.77 | 0.000175 (2^-12.48) | 12.48 |
| 1 | `pipelined_m:data_width=17,n_iter=19,angle_guard=1,frac_guard=2,rounding=round,m=3` | 39838 | 465 | 51.9 | 9 | 2.47 | 0.000112 (2^-13.13) | 13.13 |
| 2 | `pipelined_m:data_width=21,n_iter=17,angle_guard=1,frac_guard=2,rounding=round,m=2` | 47061 | 703 | 64.3 | 11 | 3.34 | 2.07e-05 (2^-15.56) | 15.56 |
| 3 | `pipelined_m:data_width=21,n_iter=20,angle_guard=1,frac_guard=0,rounding=round,m=2` | 50527 | 739 | 66.8 | 12 | 3.54 | 1.21e-05 (2^-16.34) | 16.34 |
| 4 | `pipelined_m:data_width=21,n_iter=19,angle_guard=1,frac_guard=2,rounding=trunc,m=2` | 51363 | 775 | 64.3 | 12 | 3.67 | 1.16e-05 (2^-16.40) | 16.40 |
| 5 | `pipelined_m:data_width=21,n_iter=30,angle_guard=3,frac_guard=2,rounding=round,m=2` | 83602 | 1175 | 62.0 | 17 | 5.73 | 3.88e-06 (2^-17.97) | 17.97 |
| 6 | `pipelined_m:data_width=21,n_iter=30,angle_guard=3,frac_guard=4,rounding=round,m=2` | 87789 | 1230 | 59.9 | 17 | 6 | 2.8e-06 (2^-18.45) | 18.45 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The fleet facts show pipelined_m is clearly the best family for this spec (best power_index 2.12, 5/7 front points), while pipelined is secondary (3.49, 2/7 points). Both iterative and unrolled_k have 0 feasible designs, confirming they cannot meet the 50 MSPS throughput constraint. I allocate 60% of budget to pipelined_m to densely map its Pareto front in the accuracy-constrained region (data_width 14-16, n_iter 12-16) where the power/accuracy trade-off is sharpest, and 40% to pipelined to refine its existing front points. The ranges are narrowed from the full registry to focus evaluations where feasible designs cluster, maximizing hypervolume coverage of the trade-off curve. m=2-4 for pipelined_m covers the main latency/power trade-off axis. Rounding is included as a categorical choice since it affects accuracy at the boundary.*)
- `pipelined` (40 evals): data_width=14..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* pipelined already has 2 designs on the merged front with best power_index 3.49. It is the only family that reliably hits 50 MSPS (1 result/cycle) with full throughput. Narrowing data_width to 14-16 and n_iter to 12-16 focuses on the accuracy boundary (max_abs_err <= 2^-12) where the trade-off between power and accuracy_bits is sharpest. angle_guard 0-2 and frac_guard 0-2 cover the small guard ranges that affect accuracy without inflating area/power. This refines the existing front points.
- `pipelined_m` (60 evals): data_width=14..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..4. *Why:* pipelined_m dominates the merged front with 5 of 7 designs and best power_index 2.12, significantly lower than pipelined. Registering every m stages reduces FF count and power while maintaining 1 result/cycle throughput. m=2-4 is the sweet spot: m=2 gives lowest latency and highest Fmax potential, m=4 saves more area/power but may reduce Fmax. Focusing on data_width 14-16, n_iter 12-16, angle_guard 0-2, frac_guard 0-2 targets the accuracy-constrained region where the power/accuracy trade-off curve is densest. This should extend the front toward lower power_index while maintaining accuracy_bits >= 12.

**Result (code):** 100 evaluations this round, 100 total; 10 feasible; hypervolume 17.94 (n/a).

**LLM decision:** `refine` — The current front is dominated by pipelined_m with m=2, which achieves the best power index (2.1) and meets the throughput constraint (78.8 MSPS). The pipelined family is significantly less efficient (best power 3.7) and should be deprioritized. The accuracy constraint is tight (89% violation rate), but the feasible designs show that data_width=16, n_iter=14-15, angle_guard=2, and frac_guard=1-2 are the critical sweet spots. To improve hypervolume and find lower power designs, we should narrow the search space to these high-performing regions and explore if slightly lower n_iter or different rounding/guard combinations can reduce power while maintaining accuracy >= 12 bits. We will focus exclusively on pipelined_m with m=2, as m>2 likely increases latency or area without power benefit for this throughput target, and m<2 is not allowed. We will tighten data_width to 16 (since 15 might violate accuracy and 17+ increases area/power), n_iter to 13-16, angle_guard to 1-3, and frac_guard to 0-2 to map the trade-off curve more densely around the knee of the Pareto front.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 17.94 (gain this round: n/a (first round)).
Feasible designs: 10 of 100 evaluations (5 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 20% violate; best seen 163
- max_abs_err <= 0.000244141: 89% violate; best seen 0.000176 (2^-12.48)

Pareto front (feasible, 3 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.1, accuracy_bits=12.2, area_um2=29925, ffs=437, throughput_msps=78.8, max_abs_err=0.000209 (2^-12.22)
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.34, accuracy_bits=12.4, area_um2=32695, ffs=495, throughput_msps=78.8, max_abs_err=0.00018 (2^-12.44)
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=2.41, accuracy_bits=12.5, area_um2=33716, ffs=509, throughput_msps=78.8, max_abs_err=0.000176 (2^-12.48)
Front coverage: power_index 2.1..2.41 (HV reference 40); accuracy_bits 12.2..12.5 (HV reference 12); data_width on the front 16..16 (registry 8..28).

Per family:
- pipelined: 40 evals, 7 feasible; max throughput seen 163 MSPS; best accuracy 12.48 bits; best feasible power_index=3.7; feasible ranges: data_width 16..16, n_iter 15..15, angle_guard 2..2, frac_guard 2..2
- pipelined_m: 60 evals, 3 feasible; max throughput seen 91.1 MSPS; best accuracy 12.48 bits; best feasible power_index=2.1; feasible ranges: data_width 16..16, n_iter 14..15, angle_guard 2..2, frac_guard 1..2, m 2..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Narrowing to the proven high-performance region of pipelined_m (m=2, W=16) allows Optuna to spend the remaining budget on fine-grained exploration of the accuracy-power trade-off, rather than wasting evaluations on less efficient families or out-of-range parameters.*)
- `pipelined_m` (20 evals): data_width=16..16, n_iter=13..16, angle_guard=1..3, frac_guard=0..2, rounding=trunc|round, m=2..2. *Why:* Focus on the most efficient family and parameter region identified in Round 1 to densely map the Pareto front and minimize power index while satisfying accuracy and throughput constraints.

**Result (code):** 20 evaluations this round, 120 total; 13 feasible; hypervolume 17.95 (+0.0%).

**LLM decision:** `stop` — The feasible Pareto front is well-established with 4 distinct designs covering the trade-off between power_index (2.1-2.41) and accuracy_bits (12.2-12.5). The best design (pipelined_m, data_width=16, n_iter=14, angle_guard=2, frac_guard=1, rounding=round, m=2) achieves power_index=2.1 and accuracy_bits=12.2, satisfying both constraints (throughput 78.8 MSPS >= 50, max_abs_err 0.000209 <= 0.000244). The front has stabilized (0% hypervolume gain in round 2), and all feasible designs cluster tightly around data_width=16, n_iter=14-15, angle_guard=1-2, frac_guard=1-2, m=2. Since this is the final round, the current front adequately maps the feasible region for the selection rule (min power_index), which picks the first design with power_index=2.1.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 80 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 17.95 (gain this round: +0.0%).
Feasible designs: 13 of 120 evaluations (7 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 17% violate; best seen 163
- max_abs_err <= 0.000244141: 88% violate; best seen 0.000176 (2^-12.48)

Pareto front (feasible, 4 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.1, accuracy_bits=12.2, area_um2=29925, ffs=437, throughput_msps=78.8, max_abs_err=0.000209 (2^-12.22)
- pipelined_m [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=2.16, accuracy_bits=12.3, area_um2=30851, ffs=449, throughput_msps=78.8, max_abs_err=0.000204 (2^-12.26)
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=2] power_index=2.34, accuracy_bits=12.4, area_um2=32695, ffs=495, throughput_msps=78.8, max_abs_err=0.00018 (2^-12.44)
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round m=2] power_index=2.41, accuracy_bits=12.5, area_um2=33716, ffs=509, throughput_msps=78.8, max_abs_err=0.000176 (2^-12.48)
Front coverage: power_index 2.1..2.41 (HV reference 40); accuracy_bits 12.2..12.5 (HV reference 12); data_width on the front 16..16 (registry 8..28).

Per family:
- pipelined: 40 evals, 7 feasible; max throughput seen 163 MSPS; best accuracy 12.48 bits; best feasible power_index=3.7; feasible ranges: data_width 16..16, n_iter 15..15, angle_guard 2..2, frac_guard 2..2
- pipelined_m: 80 evals, 6 feasible; max throughput seen 91.1 MSPS; best accuracy 12.48 bits; best feasible power_index=2.1; feasible ranges: data_width 16..16, n_iter 14..15, angle_guard 1..2, frac_guard 1..2, m 2..2
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined_m` (80 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (4 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 34 feasible; hypervolume 232.4 (+1194.7%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established with 4 distinct designs covering the trade-off between power_index (2.1-2.41) and accuracy_bits (12.2-12.5). The best design (pipelined_m, data_width=16, n_iter=14, angle_guard=2, frac_guard=1, rounding=round, m=2) achieves power_index=2.1 and accuracy_bits=12.2, satisfying both constraints (throughput 78.8 MSPS >= 50, max_abs_err 0.000209 <= 0.000244). The front has stabilized (0% hypervolume gain in round 2), and all feasible designs cluster tightly around data_width=16, n_iter=14-15, angle_guard=1-2, frac_guard=1-2, m=2. Since this is the final round, the current front adequately maps the feasible region for the selection rule (min power_index), which picks the first design with power_index=2.1.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 232.4 (gain this round: +1194.7%).
Feasible designs: 34 of 200 evaluations (23 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 38% violate; best seen 163
- max_abs_err <= 0.000244141: 58% violate; best seen 6.73e-08 (2^-23.82)

Pareto front (feasible, 7 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=1.77, accuracy_bits=12.5, area_um2=27943, ffs=340, throughput_msps=51.9, max_abs_err=0.000175 (2^-12.48)
- pipelined_m [data_width=17 n_iter=19 angle_guard=1 frac_guard=2 rounding=round m=3] power_index=2.47, accuracy_bits=13.1, area_um2=39838, ffs=465, throughput_msps=51.9, max_abs_err=0.000112 (2^-13.13)
- pipelined_m [data_width=21 n_iter=17 angle_guard=1 frac_guard=2 rounding=round m=2] power_index=3.34, accuracy_bits=15.6, area_um2=47061, ffs=703, throughput_msps=64.3, max_abs_err=2.07e-05 (2^-15.56)
- pipelined_m [data_width=21 n_iter=20 angle_guard=1 frac_guard=0 rounding=round m=2] power_index=3.54, accuracy_bits=16.3, area_um2=50527, ffs=739, throughput_msps=66.8, max_abs_err=1.21e-05 (2^-16.34)
- pipelined_m [data_width=21 n_iter=19 angle_guard=1 frac_guard=2 rounding=trunc m=2] power_index=3.67, accuracy_bits=16.4, area_um2=51363, ffs=775, throughput_msps=64.3, max_abs_err=1.16e-05 (2^-16.40)
- pipelined_m [data_width=21 n_iter=30 angle_guard=3 frac_guard=2 rounding=round m=2] power_index=5.73, accuracy_bits=18, area_um2=83602, ffs=1175, throughput_msps=62, max_abs_err=3.88e-06 (2^-17.97)
- pipelined_m [data_width=21 n_iter=30 angle_guard=3 frac_guard=4 rounding=round m=2] power_index=6, accuracy_bits=18.4, area_um2=87789, ffs=1230, throughput_msps=59.9, max_abs_err=2.8e-06 (2^-18.45)
Front coverage: power_index 1.77..6 (HV reference 40); accuracy_bits 12.5..18.4 (HV reference 12); data_width on the front 17..21 (registry 8..28).

Per family:
- pipelined: 40 evals, 7 feasible; max throughput seen 163 MSPS; best accuracy 12.48 bits; best feasible power_index=3.7; feasible ranges: data_width 16..16, n_iter 15..15, angle_guard 2..2, frac_guard 2..2
- pipelined_m: 160 evals, 27 feasible; max throughput seen 91.1 MSPS; best accuracy 23.82 bits; best feasible power_index=1.77; feasible ranges: data_width 16..21, n_iter 14..30, angle_guard 0..4, frac_guard 0..4, m 2..3
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 0)
- tokens: 6630 in, 2089 out
- provider-reported cost: $0.0058
- full prompts and replies: `llm_trace.jsonl`

