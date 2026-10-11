# DSE run: asic_power_50msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
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
`pipelined:data_width=16,n_iter=14,angle_guard=4,frac_guard=1,rounding=round` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 39472 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10516 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 838 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 132 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 132 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 121 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 3.49 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000203 (2^-12.26) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.33 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 6.39e-05 (2^-13.93) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 1.05 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.3 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (29 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=16,n_iter=14,angle_guard=4,frac_guard=1,rounding=round` | 39472 | 838 | 132.4 | 16 | 3.49 | 0.000203 (2^-12.26) | 12.26 |
| 1 | `pipelined:data_width=18,n_iter=14,angle_guard=1,frac_guard=1,rounding=round` | 41487 | 879 | 137.6 | 16 | 3.66 | 0.00016 (2^-12.61) | 12.61 |
| 2 | `pipelined:data_width=18,n_iter=14,angle_guard=1,frac_guard=2,rounding=round` | 42676 | 903 | 132.4 | 16 | 3.77 | 0.000157 (2^-12.64) | 12.64 |
| 3 | `pipelined:data_width=18,n_iter=14,angle_guard=1,frac_guard=3,rounding=round` | 43864 | 926 | 127.5 | 16 | 3.87 | 0.00015 (2^-12.70) | 12.70 |
| 4 | `pipelined:data_width=18,n_iter=14,angle_guard=4,frac_guard=2,rounding=round` | 44589 | 944 | 123.1 | 16 | 3.94 | 0.000136 (2^-12.85) | 12.85 |
| 5 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc` | 45499 | 980 | 132.4 | 17 | 4.06 | 9.49e-05 (2^-13.36) | 13.36 |
| 6 | `pipelined:data_width=18,n_iter=16,angle_guard=2,frac_guard=2,rounding=trunc` | 48647 | 1046 | 132.4 | 18 | 4.34 | 6.86e-05 (2^-13.83) | 13.83 |
| 7 | `pipelined:data_width=18,n_iter=16,angle_guard=3,frac_guard=2,rounding=round` | 50343 | 1064 | 127.5 | 18 | 4.44 | 5.17e-05 (2^-14.24) | 14.24 |
| 8 | `pipelined:data_width=18,n_iter=17,angle_guard=4,frac_guard=1,rounding=round` | 52847 | 1118 | 123.1 | 19 | 4.66 | 4.97e-05 (2^-14.30) | 14.30 |
| 9 | `pipelined:data_width=20,n_iter=16,angle_guard=2,frac_guard=2,rounding=round` | 54108 | 1142 | 123.1 | 18 | 4.77 | 3.61e-05 (2^-14.76) | 14.76 |
| 10 | `pipelined:data_width=21,n_iter=16,angle_guard=4,frac_guard=1,rounding=round` | 56444 | 1194 | 111.3 | 18 | 4.98 | 3.39e-05 (2^-14.85) | 14.85 |
| 11 | `pipelined:data_width=20,n_iter=17,angle_guard=4,frac_guard=1,rounding=round` | 57629 | 1218 | 115.0 | 19 | 5.08 | 2.24e-05 (2^-15.45) | 15.45 |
| 12 | `pipelined:data_width=20,n_iter=18,angle_guard=1,frac_guard=2,rounding=round` | 60147 | 1268 | 123.1 | 20 | 5.3 | 1.92e-05 (2^-15.67) | 15.67 |
| 13 | `pipelined:data_width=22,n_iter=17,angle_guard=4,frac_guard=1,rounding=round` | 62410 | 1318 | 107.9 | 19 | 5.5 | 1.67e-05 (2^-15.87) | 15.87 |
| 14 | `pipelined:data_width=23,n_iter=17,angle_guard=3,frac_guard=2,rounding=round` | 65493 | 1381 | 107.9 | 19 | 5.77 | 1.57e-05 (2^-15.96) | 15.96 |
| 15 | `pipelined:data_width=26,n_iter=17,angle_guard=1,frac_guard=2,rounding=trunc` | 69733 | 1496 | 101.6 | 19 | 6.21 | 1.54e-05 (2^-15.99) | 15.99 |
| 16 | `pipelined:data_width=23,n_iter=20,angle_guard=-1,frac_guard=1,rounding=round` | 71769 | 1512 | 115.0 | 22 | 6.32 | 7.46e-06 (2^-17.03) | 17.03 |
| 17 | `pipelined:data_width=23,n_iter=20,angle_guard=2,frac_guard=0,rounding=trunc` | 71559 | 1534 | 111.3 | 22 | 6.37 | 6.2e-06 (2^-17.30) | 17.30 |
| 18 | `pipelined:data_width=24,n_iter=19,angle_guard=3,frac_guard=2,rounding=round` | 75982 | 1601 | 104.7 | 21 | 6.69 | 4.03e-06 (2^-17.92) | 17.92 |
| 19 | `pipelined:data_width=26,n_iter=20,angle_guard=1,frac_guard=1,rounding=round` | 82065 | 1728 | 104.7 | 22 | 7.22 | 2.11e-06 (2^-18.85) | 18.85 |
| 20 | `pipelined:data_width=26,n_iter=20,angle_guard=1,frac_guard=2,rounding=round` | 83821 | 1764 | 101.6 | 22 | 7.37 | 2.05e-06 (2^-18.89) | 18.89 |
| 21 | `pipelined:data_width=26,n_iter=20,angle_guard=3,frac_guard=1,rounding=round` | 83909 | 1768 | 98.8 | 22 | 7.38 | 2.01e-06 (2^-18.92) | 18.92 |
| 22 | `pipelined:data_width=26,n_iter=21,angle_guard=1,frac_guard=1,rounding=trunc` | 84836 | 1813 | 104.7 | 23 | 7.54 | 1.23e-06 (2^-19.63) | 19.63 |
| 23 | `pipelined:data_width=24,n_iter=21,angle_guard=4,frac_guard=3,rounding=round` | 86901 | 1828 | 101.6 | 23 | 7.64 | 1.22e-06 (2^-19.64) | 19.64 |
| 24 | `pipelined:data_width=26,n_iter=21,angle_guard=3,frac_guard=2,rounding=round` | 89999 | 1894 | 98.8 | 23 | 7.91 | 1.04e-06 (2^-19.87) | 19.87 |
| 25 | `pipelined:data_width=26,n_iter=22,angle_guard=1,frac_guard=3,rounding=round` | 94245 | 1980 | 98.8 | 24 | 8.28 | 6.23e-07 (2^-20.62) | 20.62 |
| 26 | `pipelined:data_width=26,n_iter=23,angle_guard=1,frac_guard=1,rounding=round` | 94496 | 1988 | 104.7 | 25 | 8.31 | 4.43e-07 (2^-21.11) | 21.11 |
| 27 | `pipelined:data_width=26,n_iter=23,angle_guard=1,frac_guard=2,rounding=round` | 96537 | 2029 | 101.6 | 25 | 8.48 | 4.28e-07 (2^-21.16) | 21.16 |
| 28 | `pipelined:data_width=26,n_iter=26,angle_guard=1,frac_guard=2,rounding=round` | 109252 | 2295 | 101.6 | 28 | 9.6 | 3.1e-07 (2^-21.62) | 21.62 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The merged front is currently 100% pipelined, so the hypervolume is entirely carried by one family and one region of the space. Two things are needed: (1) keep pipelined searching, because it is the only proven feasible family and its front must be mapped over the full width/iter/guard ranges before the run ends; (2) give pipelined_m a genuine, properly-ranged attempt, since its only structural difference from pipelined is fewer pipeline registers at identical throughput and identical bit-level accuracy, which is precisely the direction that lowers power_index. Both families are given the same accuracy-enabling window (data_width 12..20, n_iter 10..20) so any feasible point they find is directly comparable on the power/accuracy trade-off, and the guards/rounding are left wide because they are free accuracy levers. Budget is split evenly (50/50) rather than favouring pipelined, because the front is already saturated with pipelined points and the marginal hypervolume gain is more likely to come from opening a second family than from re-sampling a region we already cover.*)
- `pipelined` (50 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Only family with feasible designs so far (54/64) and it owns the entire merged front (21/21), best power_index 4.42. It is the proven backbone of the trade-off curve, so it keeps the largest share. Ranges are centred on the accuracy-enabling region (data_width/n_iter large enough to clear 2^-12) but widened downward to 12/10 so the search can push power_index below 4.42; angle_guard/frac_guard/rounding are left at full registry range because they are cheap accuracy levers that shift the front without changing the schedule.
- `pipelined_m` (50 evals): data_width=12..20, n_iter=10..20, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* 0 feasible so far, but that is almost certainly a range problem, not a capability problem: accuracy depends only on data_width/n_iter/angle_guard/frac_guard/rounding, which are identical across families, and pipelined_m still delivers 1 result/cycle so the 50 MSPS constraint is met for any m. Registering only every m stages removes pipeline flip-flops, which is exactly the lever that can beat pipelined on power_index at equal accuracy. Giving it half the budget with the same accuracy-enabling width/iter window plus the full m=2..8 sweep is the cheapest way to test whether it extends the front to lower power; if it stays infeasible after this, it can be dropped in later rounds.

**Result (code):** 100 evaluations this round, 100 total; 23 feasible; hypervolume 138.9 (n/a).

**LLM decision:** `map_front` — Round 1 found a valid but narrow front: 23/100 feasible, all on pipelined (pipelined_m 0/50 feasible); min power_index 3.49 at data_width=16, n_iter=14, angle_guard=4, frac_guard=1, rounding=round, which satisfies throughput 132 MSPS and 2^-12.26 error. The front spans only power_index 3.49..5.89 against reference 40 and accuracy_bits 12.3..15.9 against reference 12, with data_width 16..20 of 8..28, so most of the accuracy axis (and any sub-16-bit power corner) is unexplored. Hypervolume is dominated by the accuracy tail ((40 - 5.89) x 3.9 bits ≈ 133 of 138.9), so mapping the full ranges of the families on the front is worth far more than local refinement. Ties to the selection rule too: the same mapping is the only way to find a cheaper-than-3.49 feasible point, since data_width < 16 was never sampled.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 138.9 (gain this round: n/a (first round)).
Feasible designs: 23 of 100 evaluations (20 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 20% violate; best seen 190
- max_abs_err <= 0.000244141: 77% violate; best seen 1.61e-05 (2^-15.92)

Pareto front (feasible, 11 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=4 frac_guard=1 rounding=round] power_index=3.49, accuracy_bits=12.3, area_um2=39472, ffs=838, throughput_msps=132, max_abs_err=0.000203 (2^-12.26)
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=round] power_index=3.66, accuracy_bits=12.6, area_um2=41487, ffs=879, throughput_msps=138, max_abs_err=0.00016 (2^-12.61)
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=2 rounding=round] power_index=3.77, accuracy_bits=12.6, area_um2=42676, ffs=903, throughput_msps=132, max_abs_err=0.000157 (2^-12.64)
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=3 rounding=round] power_index=3.87, accuracy_bits=12.7, area_um2=43864, ffs=926, throughput_msps=128, max_abs_err=0.00015 (2^-12.70)
- pipelined [data_width=18 n_iter=14 angle_guard=4 frac_guard=2 rounding=round] power_index=3.94, accuracy_bits=12.8, area_um2=44589, ffs=944, throughput_msps=123, max_abs_err=0.000136 (2^-12.85)
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] power_index=4.34, accuracy_bits=13.8, area_um2=48647, ffs=1046, throughput_msps=132, max_abs_err=6.86e-05 (2^-13.83)
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] power_index=4.44, accuracy_bits=14.2, area_um2=50343, ffs=1064, throughput_msps=128, max_abs_err=5.17e-05 (2^-14.24)
- pipelined [data_width=20 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] power_index=4.77, accuracy_bits=14.8, area_um2=54108, ffs=1142, throughput_msps=123, max_abs_err=3.61e-05 (2^-14.76)
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=2 rounding=round] power_index=5.3, accuracy_bits=15.7, area_um2=60147, ffs=1268, throughput_msps=123, max_abs_err=1.92e-05 (2^-15.67)
- pipelined [data_width=20 n_iter=20 angle_guard=1 frac_guard=2 rounding=round] power_index=5.89, accuracy_bits=15.9, area_um2=66918, ffs=1410, throughput_msps=123, max_abs_err=1.61e-05 (2^-15.92)
Front coverage: power_index 3.49..5.89 (HV reference 40); accuracy_bits 12.3..15.9 (HV reference 12); data_width on the front 16..20 (registry 8..28).

Per family:
- pipelined: 50 evals, 23 feasible; max throughput seen 190 MSPS; best accuracy 15.92 bits; best feasible power_index=3.49; feasible ranges: data_width 16..20, n_iter 14..20, angle_guard -1..4, frac_guard 1..3
- pipelined_m: 50 evals, 0 feasible; max throughput seen 91.1 MSPS; best accuracy 11.98 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 20 evaluations*)
- `pipelined` (20 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (11 front designs; box front_anchored)

**Result (code):** 20 evaluations this round, 120 total; 38 feasible; hypervolume 321.6 (+131.5%).

**LLM decision:** `map_front` — The feasible front is entirely pipelined (38/70 feasible) while pipelined_m produced 0 feasible designs, so the front lives in one family. Coverage is still thin at the low-power end: the best feasible power_index is 3.49 at accuracy 12.3 bits, and the front spans data_width 16..28 while the registry allows 8..28 — the cheap/low-width corner (data_width 8..15) and the low-n_iter corner are essentially unmapped, and the throughput constraint (best seen 190 MSPS, 17% violations) means there is room to trade throughput for power. With 80 evals left and a +131.5% hypervolume gain this round, a code-driven NSGA-II coverage search over the full pipelined ranges (seeded with the current front) is the best use of the remaining budget to fill the low-power/low-accuracy end and the high-accuracy tail before the final selection (min power_index).

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 120 of 200.
Hypervolume of the feasible front: 321.6 (gain this round: +131.5%).
Feasible designs: 38 of 120 evaluations (34 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 17% violate; best seen 190
- max_abs_err <= 0.000244141: 68% violate; best seen 3.1e-07 (2^-21.62)

Pareto front (feasible, 16 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=4 frac_guard=1 rounding=round] power_index=3.49, accuracy_bits=12.3, area_um2=39472, ffs=838, throughput_msps=132, max_abs_err=0.000203 (2^-12.26)
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=2 rounding=round] power_index=3.77, accuracy_bits=12.6, area_um2=42676, ffs=903, throughput_msps=132, max_abs_err=0.000157 (2^-12.64)
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=3 rounding=round] power_index=3.87, accuracy_bits=12.7, area_um2=43864, ffs=926, throughput_msps=128, max_abs_err=0.00015 (2^-12.70)
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc] power_index=4.06, accuracy_bits=13.4, area_um2=45499, ffs=980, throughput_msps=132, max_abs_err=9.49e-05 (2^-13.36)
- pipelined [data_width=18 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] power_index=4.44, accuracy_bits=14.2, area_um2=50343, ffs=1064, throughput_msps=128, max_abs_err=5.17e-05 (2^-14.24)
- pipelined [data_width=20 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] power_index=4.77, accuracy_bits=14.8, area_um2=54108, ffs=1142, throughput_msps=123, max_abs_err=3.61e-05 (2^-14.76)
- pipelined [data_width=20 n_iter=20 angle_guard=1 frac_guard=2 rounding=round] power_index=5.89, accuracy_bits=15.9, area_um2=66918, ffs=1410, throughput_msps=123, max_abs_err=1.61e-05 (2^-15.92)
- pipelined [data_width=26 n_iter=21 angle_guard=-2 frac_guard=2 rounding=round] power_index=7.48, accuracy_bits=18.7, area_um2=85152, ffs=1790, throughput_msps=102, max_abs_err=2.32e-06 (2^-18.72)
- pipelined [data_width=26 n_iter=21 angle_guard=1 frac_guard=4 rounding=round] power_index=8.06, accuracy_bits=19.8, area_um2=91763, ffs=1927, throughput_msps=96.1, max_abs_err=1.1e-06 (2^-19.79)
- pipelined [data_width=26 n_iter=26 angle_guard=1 frac_guard=2 rounding=round] power_index=9.6, accuracy_bits=21.6, area_um2=109252, ffs=2295, throughput_msps=102, max_abs_err=3.1e-07 (2^-21.62)
Front coverage: power_index 3.49..9.6 (HV reference 40); accuracy_bits 12.3..21.6 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- pipelined: 70 evals, 38 feasible; max throughput seen 190 MSPS; best accuracy 21.62 bits; best feasible power_index=3.49; feasible ranges: data_width 15..28, n_iter 14..26, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 50 evals, 0 feasible; max throughput seen 91.1 MSPS; best accuracy 11.98 bits
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 80 evaluations*)
- `pipelined` (80 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (16 front designs; box front_anchored)

**Result (code):** 80 evaluations this round, 200 total; 110 feasible; hypervolume 324.7 (+1.0%).

**LLM decision:** `stop` — Budget is exhausted (200/200 evals, round 3 of 4) and the front is both feasible and converged. Feasibility is proven: 110 of 200 evaluations meet both constraints, and the selection rule (min power_index) is satisfied by pipelined [data_width=16 n_iter=14 angle_guard=4 frac_guard=1 rounding=round] at power_index=3.49, accuracy_bits=12.3 (max_abs_err=0.000203 <= 0.000244141) and throughput 132 MSPS >= 50. The front spans power_index 3.49..9.6 against an HV reference of 40 and accuracy_bits 12.3..21.6 against a reference of 12, i.e. it already covers the useful trade-off curve well past both reference points, and the round-over-round hypervolume gain is only +1.0%, indicating diminishing returns. The only unexplored family, pipelined_m, produced 0 feasible designs in 50 evals (best accuracy 11.98 bits, max throughput 91.1 MSPS), so adding or widening families offers no route to a better front. Nothing in the registry is unreachable, so infeasible is not warranted; stopping is the correct final decision.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 324.7 (gain this round: +1.0%).
Feasible designs: 110 of 200 evaluations (99 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 10% violate; best seen 190
- max_abs_err <= 0.000244141: 45% violate; best seen 3.1e-07 (2^-21.62)

Pareto front (feasible, 29 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined [data_width=16 n_iter=14 angle_guard=4 frac_guard=1 rounding=round] power_index=3.49, accuracy_bits=12.3, area_um2=39472, ffs=838, throughput_msps=132, max_abs_err=0.000203 (2^-12.26)
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=3 rounding=round] power_index=3.87, accuracy_bits=12.7, area_um2=43864, ffs=926, throughput_msps=128, max_abs_err=0.00015 (2^-12.70)
- pipelined [data_width=18 n_iter=16 angle_guard=2 frac_guard=2 rounding=trunc] power_index=4.34, accuracy_bits=13.8, area_um2=48647, ffs=1046, throughput_msps=132, max_abs_err=6.86e-05 (2^-13.83)
- pipelined [data_width=20 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] power_index=4.77, accuracy_bits=14.8, area_um2=54108, ffs=1142, throughput_msps=123, max_abs_err=3.61e-05 (2^-14.76)
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=2 rounding=round] power_index=5.3, accuracy_bits=15.7, area_um2=60147, ffs=1268, throughput_msps=123, max_abs_err=1.92e-05 (2^-15.67)
- pipelined [data_width=23 n_iter=20 angle_guard=-1 frac_guard=1 rounding=round] power_index=6.32, accuracy_bits=17, area_um2=71769, ffs=1512, throughput_msps=115, max_abs_err=7.46e-06 (2^-17.03)
- pipelined [data_width=26 n_iter=20 angle_guard=1 frac_guard=1 rounding=round] power_index=7.22, accuracy_bits=18.9, area_um2=82065, ffs=1728, throughput_msps=105, max_abs_err=2.11e-06 (2^-18.85)
- pipelined [data_width=26 n_iter=21 angle_guard=1 frac_guard=1 rounding=trunc] power_index=7.54, accuracy_bits=19.6, area_um2=84836, ffs=1813, throughput_msps=105, max_abs_err=1.23e-06 (2^-19.63)
- pipelined [data_width=26 n_iter=22 angle_guard=1 frac_guard=3 rounding=round] power_index=8.28, accuracy_bits=20.6, area_um2=94245, ffs=1980, throughput_msps=98.8, max_abs_err=6.23e-07 (2^-20.62)
- pipelined [data_width=26 n_iter=26 angle_guard=1 frac_guard=2 rounding=round] power_index=9.6, accuracy_bits=21.6, area_um2=109252, ffs=2295, throughput_msps=102, max_abs_err=3.1e-07 (2^-21.62)
Front coverage: power_index 3.49..9.6 (HV reference 40); accuracy_bits 12.3..21.6 (HV reference 12); data_width on the front 16..26 (registry 8..28).

Per family:
- pipelined: 150 evals, 110 feasible; max throughput seen 190 MSPS; best accuracy 21.62 bits; best feasible power_index=3.49; feasible ranges: data_width 15..28, n_iter 14..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 50 evals, 0 feasible; max throughput seen 91.1 MSPS; best accuracy 11.98 bits
```
</details>

## LLM usage
- calls: 4 (failed/unparsed attempts: 0)
- tokens: 10937 in, 5910 out
- provider-reported cost: $0.0056
- full prompts and replies: `llm_trace.jsonl`

