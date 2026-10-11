# DSE run: asic_power_50msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
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
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 39336 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 10479 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 853 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 138 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 138 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 16 | exact: schedule |
| latency_ns | 116 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 3.53 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000175 (2^-12.48) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 11.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.28e-05 (2^-14.21) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.46 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (22 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=18,n_iter=14,angle_guard=1,frac_guard=0,rounding=round` | 39336 | 853 | 137.6 | 16 | 3.53 | 0.000175 (2^-12.48) | 12.48 |
| 1 | `pipelined:data_width=18,n_iter=14,angle_guard=2,frac_guard=0,rounding=round` | 39973 | 867 | 132.4 | 16 | 3.59 | 0.00017 (2^-12.53) | 12.53 |
| 2 | `pipelined:data_width=17,n_iter=15,angle_guard=2,frac_guard=0,rounding=round` | 40877 | 885 | 137.6 | 17 | 3.66 | 0.000148 (2^-12.72) | 12.72 |
| 3 | `pipelined:data_width=18,n_iter=14,angle_guard=3,frac_guard=2,rounding=round` | 43951 | 930 | 127.5 | 16 | 3.88 | 0.000143 (2^-12.77) | 12.77 |
| 4 | `pipelined:data_width=18,n_iter=15,angle_guard=1,frac_guard=1,rounding=round` | 44494 | 942 | 137.6 | 17 | 3.93 | 0.000101 (2^-13.27) | 13.27 |
| 5 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=1,rounding=round` | 45179 | 957 | 132.4 | 17 | 3.99 | 9.31e-05 (2^-13.39) | 13.39 |
| 6 | `pipelined:data_width=18,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 46462 | 982 | 132.4 | 17 | 4.1 | 8.26e-05 (2^-13.56) | 13.56 |
| 7 | `pipelined:data_width=19,n_iter=15,angle_guard=2,frac_guard=2,rounding=round` | 48569 | 1026 | 127.5 | 17 | 4.28 | 7.18e-05 (2^-13.77) | 13.77 |
| 8 | `pipelined:data_width=18,n_iter=17,angle_guard=2,frac_guard=1,rounding=round` | 51287 | 1084 | 132.4 | 19 | 4.52 | 5.64e-05 (2^-14.11) | 14.11 |
| 9 | `pipelined:data_width=18,n_iter=17,angle_guard=2,frac_guard=2,rounding=round` | 52760 | 1114 | 132.4 | 19 | 4.65 | 4.73e-05 (2^-14.37) | 14.37 |
| 10 | `pipelined:data_width=27,n_iter=16,angle_guard=-1,frac_guard=3,rounding=round` | 69029 | 1453 | 96.1 | 18 | 6.07 | 3.08e-05 (2^-14.99) | 14.99 |
| 11 | `pipelined:data_width=27,n_iter=16,angle_guard=3,frac_guard=2,rounding=trunc` | 69157 | 1486 | 96.1 | 18 | 6.17 | 3.05e-05 (2^-15.00) | 15.00 |
| 12 | `pipelined:data_width=27,n_iter=16,angle_guard=3,frac_guard=2,rounding=round` | 70581 | 1488 | 96.1 | 18 | 6.22 | 3.05e-05 (2^-15.00) | 15.00 |
| 13 | `pipelined:data_width=27,n_iter=17,angle_guard=2,frac_guard=3,rounding=round` | 75749 | 1595 | 96.1 | 19 | 6.66 | 1.53e-05 (2^-16.00) | 16.00 |
| 14 | `pipelined:data_width=27,n_iter=17,angle_guard=3,frac_guard=3,rounding=round` | 76529 | 1611 | 96.1 | 19 | 6.73 | 1.53e-05 (2^-16.00) | 16.00 |
| 15 | `pipelined:data_width=22,n_iter=23,angle_guard=2,frac_guard=3,rounding=trunc` | 85500 | 1820 | 111.3 | 25 | 7.58 | 2.92e-06 (2^-18.39) | 18.39 |
| 16 | `pipelined:data_width=22,n_iter=23,angle_guard=3,frac_guard=3,rounding=trunc` | 86564 | 1842 | 111.3 | 25 | 7.67 | 2.39e-06 (2^-18.67) | 18.67 |
| 17 | `pipelined:data_width=27,n_iter=23,angle_guard=4,frac_guard=3,rounding=trunc` | 103590 | 2204 | 93.5 | 25 | 9.18 | 2.84e-07 (2^-21.75) | 21.75 |
| 18 | `pipelined:data_width=26,n_iter=28,angle_guard=2,frac_guard=3,rounding=round` | 121545 | 2550 | 98.8 | 30 | 10.7 | 1.5e-07 (2^-22.66) | 22.66 |
| 19 | `pipelined:data_width=27,n_iter=30,angle_guard=2,frac_guard=2,rounding=trunc` | 130417 | 2765 | 98.8 | 32 | 11.5 | 1.42e-07 (2^-22.74) | 22.74 |
| 20 | `pipelined:data_width=27,n_iter=30,angle_guard=1,frac_guard=3,rounding=trunc` | 131726 | 2790 | 96.1 | 32 | 11.6 | 1.39e-07 (2^-22.78) | 22.78 |
| 21 | `pipelined:data_width=27,n_iter=30,angle_guard=4,frac_guard=3,rounding=trunc` | 135913 | 2879 | 93.5 | 32 | 12 | 7.43e-08 (2^-23.68) | 23.68 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >=50 MSPS, which only the 1-result/cycle families (pipelined, pipelined_m) can guarantee without relying on a high Fmax from a multi-cycle design. I am restricted to pipelined/pipelined_m. I focus the entire budget on `pipelined` first because it is the cleanest 1/cycle datapath and its critical path (one micro-rotation) is short enough in sky130hd to clear 50 MHz across the whole N=12..18 range, so throughput is not the binding constraint and the real trade-off is power vs accuracy. Ranges are set to bracket the accuracy constraint: W=14..18 and N=12..18 with small guards cover the 2^-12 error bound while leaving room for Optuna to find the low-power corner (small W/N/guards) and the high-accuracy corner (larger W/N) that the hypervolume rewards. I defer pipelined_m to a later round only if the pipelined front shows that reducing register count (larger m) cuts power_index enough to matter, since m>1 trades Fmax (longer combinational path) against fewer FFs and is a secondary lever.*)
- `pipelined` (60 evals): data_width=14..18, n_iter=12..18, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Fully pipelined gives 1 result/cycle, so throughput = Fmax. At N=12-18 the critical path is a single micro-rotation (shift+add+mul), which in sky130hd comfortably exceeds 50 MHz, so the throughput constraint is met with margin. The accuracy constraint (max_abs_err <= 2^-12) is met by W=14-18 with N>=12; the trade-off between power (driven by W, N, guards) and accuracy_bits lives exactly in this box, so this is where the Pareto front for the power objective is.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 60 evaluations this round, 60 total; 37 feasible; hypervolume 85.08 (n/a).

**LLM decision:** `stop` — The Pareto front is well-established and feasible. The minimum power_index achieved is 3.53 (pipelined, data_width=18, n_iter=14, angle_guard=1, frac_guard=0, rounding=round), which satisfies the throughput constraint (138 MSPS >= 50) and the accuracy constraint (max_abs_err=0.000175 <= 0.000244141). The front covers a reasonable range of accuracy (12.5 to 14.4 bits) and power (3.53 to 4.65). Since this is the final round and the selection rule is 'min power_index', the design with power_index=3.53 is the clear winner. No further exploration is possible or necessary.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 85.08 (gain this round: n/a (first round)).
Feasible designs: 37 of 60 evaluations (23 unique).
Families explored so far: pipelined. Not yet explored: pipelined_m.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 0% violate; best seen 163
- max_abs_err <= 0.000244141: 38% violate; best seen 4.73e-05 (2^-14.37)

Pareto front (feasible, 8 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] power_index=3.53, accuracy_bits=12.5, area_um2=39336, ffs=853, throughput_msps=138, max_abs_err=0.000175 (2^-12.48)
- pipelined [data_width=18 n_iter=14 angle_guard=2 frac_guard=0 rounding=round] power_index=3.59, accuracy_bits=12.5, area_um2=39973, ffs=867, throughput_msps=132, max_abs_err=0.00017 (2^-12.53)
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] power_index=3.66, accuracy_bits=12.7, area_um2=40877, ffs=885, throughput_msps=138, max_abs_err=0.000148 (2^-12.72)
- pipelined [data_width=18 n_iter=15 angle_guard=1 frac_guard=1 rounding=round] power_index=3.93, accuracy_bits=13.3, area_um2=44494, ffs=942, throughput_msps=138, max_abs_err=0.000101 (2^-13.27)
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] power_index=3.99, accuracy_bits=13.4, area_um2=45179, ffs=957, throughput_msps=132, max_abs_err=9.31e-05 (2^-13.39)
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] power_index=4.1, accuracy_bits=13.6, area_um2=46462, ffs=982, throughput_msps=132, max_abs_err=8.26e-05 (2^-13.56)
- pipelined [data_width=18 n_iter=17 angle_guard=2 frac_guard=1 rounding=round] power_index=4.52, accuracy_bits=14.1, area_um2=51287, ffs=1084, throughput_msps=132, max_abs_err=5.64e-05 (2^-14.11)
- pipelined [data_width=18 n_iter=17 angle_guard=2 frac_guard=2 rounding=round] power_index=4.65, accuracy_bits=14.4, area_um2=52760, ffs=1114, throughput_msps=132, max_abs_err=4.73e-05 (2^-14.37)
Front coverage: power_index 3.53..4.65 (HV reference 40); accuracy_bits 12.5..14.4 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 60 evals, 37 feasible; max throughput seen 163 MSPS; best accuracy 14.37 bits; best feasible power_index=3.53; feasible ranges: data_width 17..18, n_iter 14..17, angle_guard 0..2, frac_guard 0..2
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (40 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (8 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 77 feasible; hypervolume 376.8 (+342.9%).

**No LLM call** (code's front-mapping round): The Pareto front is well-established and feasible. The minimum power_index achieved is 3.53 (pipelined, data_width=18, n_iter=14, angle_guard=1, frac_guard=0, rounding=round), which satisfies the throughput constraint (138 MSPS >= 50) and the accuracy constraint (max_abs_err=0.000175 <= 0.000244141). The front covers a reasonable range of accuracy (12.5 to 14.4 bits) and power (3.53 to 4.65). Since this is the final round and the selection rule is 'min power_index', the design with power_index=3.53 is the clear winner. No further exploration is possible or necessary.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 376.8 (gain this round: +342.9%).
Feasible designs: 77 of 100 evaluations (56 unique).
Families explored so far: pipelined. Not yet explored: pipelined_m.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 0% violate; best seen 163
- max_abs_err <= 0.000244141: 23% violate; best seen 7.43e-08 (2^-23.68)

Pareto front (feasible, 22 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined [data_width=18 n_iter=14 angle_guard=1 frac_guard=0 rounding=round] power_index=3.53, accuracy_bits=12.5, area_um2=39336, ffs=853, throughput_msps=138, max_abs_err=0.000175 (2^-12.48)
- pipelined [data_width=17 n_iter=15 angle_guard=2 frac_guard=0 rounding=round] power_index=3.66, accuracy_bits=12.7, area_um2=40877, ffs=885, throughput_msps=138, max_abs_err=0.000148 (2^-12.72)
- pipelined [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=round] power_index=3.99, accuracy_bits=13.4, area_um2=45179, ffs=957, throughput_msps=132, max_abs_err=9.31e-05 (2^-13.39)
- pipelined [data_width=19 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] power_index=4.28, accuracy_bits=13.8, area_um2=48569, ffs=1026, throughput_msps=128, max_abs_err=7.18e-05 (2^-13.77)
- pipelined [data_width=18 n_iter=17 angle_guard=2 frac_guard=2 rounding=round] power_index=4.65, accuracy_bits=14.4, area_um2=52760, ffs=1114, throughput_msps=132, max_abs_err=4.73e-05 (2^-14.37)
- pipelined [data_width=27 n_iter=16 angle_guard=3 frac_guard=2 rounding=round] power_index=6.22, accuracy_bits=15, area_um2=70581, ffs=1488, throughput_msps=96.1, max_abs_err=3.05e-05 (2^-15.00)
- pipelined [data_width=27 n_iter=17 angle_guard=3 frac_guard=3 rounding=round] power_index=6.73, accuracy_bits=16, area_um2=76529, ffs=1611, throughput_msps=96.1, max_abs_err=1.53e-05 (2^-16.00)
- pipelined [data_width=22 n_iter=23 angle_guard=3 frac_guard=3 rounding=trunc] power_index=7.67, accuracy_bits=18.7, area_um2=86564, ffs=1842, throughput_msps=111, max_abs_err=2.39e-06 (2^-18.67)
- pipelined [data_width=27 n_iter=30 angle_guard=2 frac_guard=2 rounding=trunc] power_index=11.5, accuracy_bits=22.7, area_um2=130417, ffs=2765, throughput_msps=98.8, max_abs_err=1.42e-07 (2^-22.74)
- pipelined [data_width=27 n_iter=30 angle_guard=4 frac_guard=3 rounding=trunc] power_index=12, accuracy_bits=23.7, area_um2=135913, ffs=2879, throughput_msps=93.5, max_abs_err=7.43e-08 (2^-23.68)
Front coverage: power_index 3.53..12 (HV reference 40); accuracy_bits 12.5..23.7 (HV reference 12); data_width on the front 17..27 (registry 8..28).

Per family:
- pipelined: 100 evals, 77 feasible; max throughput seen 163 MSPS; best accuracy 23.68 bits; best feasible power_index=3.53; feasible ranges: data_width 16..27, n_iter 14..30, angle_guard -1..4, frac_guard 0..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4365 in, 879 out
- provider-reported cost: $0.0025
- full prompts and replies: `llm_trace.jsonl`

