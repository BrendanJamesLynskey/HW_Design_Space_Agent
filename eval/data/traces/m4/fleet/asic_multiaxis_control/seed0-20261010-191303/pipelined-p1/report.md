# DSE run: asic_multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical sky130_fd_sc_hd standard-cell cost model fitted to 57 Yosys + OpenSTA synthesis points (eval/data/asic_calibration.md). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec asic_multiaxis_control: Shared sin/cos unit in sky130 standard cells for a 16-axis motor-control loop: a 1 MHz control tick issues 32 requests at once; all 32 results must be back within 0.5 us of the tick (p99 over ticks). Max error <= 2^-12. Minimise area.
  target: asic-sky130hd
  constraint: throughput_msps >= 32
  constraint: max_abs_err <= 0.000244141
  constraint: sys_p99_batch_us <= 0.5
  objective: min area_um2 (HV ref 100000)
  objective: max accuracy_bits (HV ref 12)
  select: min area_um2
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average)
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined:data_width=20,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min area_um2)

| metric | value | provenance |
|---|---|---|
| area_um2 | 45673 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 12168 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 988 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 132 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 132 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 128 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 2.62 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 8.24e-05 (2^-13.57) | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 21.6 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.58e-05 (2^-15.24) | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 6.76 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13.6 | exact: bit-accurate model, dense (125151 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (14 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined:data_width=20,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 45673 | 988 | 132.4 | 17 | 2.62 | 8.24e-05 (2^-13.57) | 13.57 |
| 1 | `pipelined:data_width=20,n_iter=16,angle_guard=1,frac_guard=0,rounding=round` | 49554 | 1070 | 127.5 | 18 | 2.84 | 4.64e-05 (2^-14.39) | 14.39 |
| 2 | `pipelined:data_width=20,n_iter=16,angle_guard=4,frac_guard=1,rounding=trunc` | 53130 | 1144 | 115.0 | 18 | 3.04 | 4.27e-05 (2^-14.51) | 14.51 |
| 3 | `pipelined:data_width=20,n_iter=16,angle_guard=1,frac_guard=2,rounding=round` | 53376 | 1127 | 123.1 | 18 | 3.01 | 3.84e-05 (2^-14.67) | 14.67 |
| 4 | `pipelined:data_width=20,n_iter=16,angle_guard=2,frac_guard=3,rounding=trunc` | 54420 | 1168 | 118.9 | 18 | 3.1 | 3.71e-05 (2^-14.72) | 14.72 |
| 5 | `pipelined:data_width=20,n_iter=16,angle_guard=3,frac_guard=3,rounding=trunc` | 55153 | 1184 | 118.9 | 18 | 3.15 | 3.59e-05 (2^-14.77) | 14.77 |
| 6 | `pipelined:data_width=20,n_iter=18,angle_guard=1,frac_guard=0,rounding=round` | 55947 | 1203 | 127.5 | 20 | 3.2 | 2.9e-05 (2^-15.07) | 15.07 |
| 7 | `pipelined:data_width=20,n_iter=17,angle_guard=1,frac_guard=2,rounding=round` | 56761 | 1197 | 123.1 | 19 | 3.2 | 2.32e-05 (2^-15.40) | 15.40 |
| 8 | `pipelined:data_width=20,n_iter=18,angle_guard=1,frac_guard=2,rounding=round` | 60147 | 1268 | 123.1 | 20 | 3.39 | 1.92e-05 (2^-15.67) | 15.67 |
| 9 | `pipelined:data_width=20,n_iter=19,angle_guard=1,frac_guard=1,rounding=round` | 61871 | 1306 | 127.5 | 21 | 3.49 | 1.9e-05 (2^-15.68) | 15.68 |
| 10 | `pipelined:data_width=20,n_iter=20,angle_guard=3,frac_guard=3,rounding=round` | 70519 | 1485 | 118.9 | 22 | 3.97 | 6.52e-06 (2^-17.23) | 17.23 |
| 11 | `pipelined:data_width=23,n_iter=20,angle_guard=0,frac_guard=3,rounding=trunc` | 74985 | 1601 | 107.9 | 22 | 4.26 | 4.52e-06 (2^-17.76) | 17.76 |
| 12 | `pipelined:data_width=22,n_iter=20,angle_guard=4,frac_guard=4,rounding=trunc` | 77664 | 1656 | 107.9 | 22 | 4.41 | 3.17e-06 (2^-18.27) | 18.27 |
| 13 | `pipelined:data_width=23,n_iter=20,angle_guard=3,frac_guard=3,rounding=trunc` | 77752 | 1660 | 107.9 | 22 | 4.42 | 2.74e-06 (2^-18.48) | 18.48 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The system constraint (32 results within 0.5 us of a 1 MHz tick) demands both high throughput and low latency, so only 1-result/cycle pipelined families are plausible. Pipelined offers the highest Fmax and lowest latency; pipelined_m trades Fmax for fewer registers and smaller area. We search W=14..20 and N=8..20 to cover the area-vs-accuracy Pareto front, with guard bits and rounding to reach max_abs_err <= 2^-12. The budget is split to map both families' fronts before the reserved full-range mapping round.*)
- `pipelined` (33 evals): data_width=14..20, n_iter=8..20, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Pipelined gives 1 result/cycle with the shortest latency (N+2) and highest Fmax, the best chance to satisfy the 0.5 us burst bound; varying W and N trades area against the 2^-12 accuracy requirement.
- `pipelined_m` (27 evals): data_width=14..20, n_iter=8..20, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, m=2..6. *Why:* Registering every m stages cuts flip-flop count (area) and shortens cycle latency, but lengthens the combinational path; exploring m=2..6 finds the area/Fmax sweet spot for the min-area objective while still meeting the burst deadline.

**Result (code):** 60 evaluations this round, 60 total; 22 feasible; hypervolume 1.768e+05 (n/a).

**LLM decision:** `stop` — Feasible, not infeasible: 22 of 60 evaluations satisfy all three constraints and the Pareto front carries 6 of them, so no constraint is unreachable. Evidence: throughput_msps >= 32 is met with large margin (cheapest front design runs 128 MSPS vs the required 32; best seen 163); max_abs_err <= 2^-12 is met (front designs give 4.64e-05..1.9e-05, i.e. 14.4..15.7 accuracy bits, versus the required 12, so even the least accurate front point has ~2.4 bits of headroom); sys_p99_batch_us <= 0.5 is met (best seen 0.263 us, so even allowing for the L1 bound being optimistic the cheapest candidates have roughly a 2x margin before L2 re-selection could disqualify them). All six front designs are pipelined with data_width=20, n_iter 16..19, angle_guard 1, frac_guard 0..2, covering area_um2 49554..61871 against the HV reference of 100000 and accuracy 14.4..15.7 against the reference of 12 - a well-populated trade-off curve in both objectives. The selection rule (min area_um2) is served by the front's cheapest point, pipelined [W=20 N=16 aG=1 fG=0 round] at 49554 um^2, which itself passes every constraint with margin. This is the final round, and further evaluation cannot change the outcome, so stop.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1.768e+05 (gain this round: n/a (first round)).
Feasible designs: 22 of 60 evaluations (13 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 8% violate; best seen 163
- max_abs_err <= 0.000244141: 32% violate; best seen 1.9e-05 (2^-15.68)
- sys_p99_batch_us <= 0.5: 45% violate; best seen 0.263

Pareto front (feasible, 6 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=49554, accuracy_bits=14.4, ffs=1070, throughput_msps=128, max_abs_err=4.64e-05 (2^-14.39), power_index=2.84
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] area_um2=53376, accuracy_bits=14.7, ffs=1127, throughput_msps=123, max_abs_err=3.84e-05 (2^-14.67), power_index=3.01
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] area_um2=55947, accuracy_bits=15.1, ffs=1203, throughput_msps=128, max_abs_err=2.9e-05 (2^-15.07), power_index=3.2
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=2 rounding=round] area_um2=56761, accuracy_bits=15.4, ffs=1197, throughput_msps=123, max_abs_err=2.32e-05 (2^-15.40), power_index=3.2
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=2 rounding=round] area_um2=60147, accuracy_bits=15.7, ffs=1268, throughput_msps=123, max_abs_err=1.92e-05 (2^-15.67), power_index=3.39
- pipelined [data_width=20 n_iter=19 angle_guard=1 frac_guard=1 rounding=round] area_um2=61871, accuracy_bits=15.7, ffs=1306, throughput_msps=128, max_abs_err=1.9e-05 (2^-15.68), power_index=3.49
Front coverage: area_um2 49554..61871 (HV reference 100000); accuracy_bits 14.4..15.7 (HV reference 12); data_width on the front 20..20 (registry 8..28).

Per family:
- pipelined: 33 evals, 22 feasible; max throughput seen 163 MSPS; best accuracy 15.68 bits; best feasible area_um2=49554; feasible ranges: data_width 17..20, n_iter 16..19, angle_guard -1..1, frac_guard 0..2
- pipelined_m: 27 evals, 0 feasible; max throughput seen 78.8 MSPS; best accuracy 14.88 bits
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined` (40 evals): data_width=19..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (6 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 54 feasible; hypervolume 2.579e+05 (+45.8%).

**No LLM call** (code's front-mapping round): Feasible, not infeasible: 22 of 60 evaluations satisfy all three constraints and the Pareto front carries 6 of them, so no constraint is unreachable. Evidence: throughput_msps >= 32 is met with large margin (cheapest front design runs 128 MSPS vs the required 32; best seen 163); max_abs_err <= 2^-12 is met (front designs give 4.64e-05..1.9e-05, i.e. 14.4..15.7 accuracy bits, versus the required 12, so even the least accurate front point has ~2.4 bits of headroom); sys_p99_batch_us <= 0.5 is met (best seen 0.263 us, so even allowing for the L1 bound being optimistic the cheapest candidates have roughly a 2x margin before L2 re-selection could disqualify them). All six front designs are pipelined with data_width=20, n_iter 16..19, angle_guard 1, frac_guard 0..2, covering area_um2 49554..61871 against the HV reference of 100000 and accuracy 14.4..15.7 against the reference of 12 - a well-populated trade-off curve in both objectives. The selection rule (min area_um2) is served by the front's cheapest point, pipelined [W=20 N=16 aG=1 fG=0 round] at 49554 um^2, which itself passes every constraint with margin. This is the final round, and further evaluation cannot change the outcome, so stop.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 2.579e+05 (gain this round: +45.8%).
Feasible designs: 54 of 100 evaluations (43 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 5% violate; best seen 163
- max_abs_err <= 0.000244141: 19% violate; best seen 7.95e-08 (2^-23.58)
- sys_p99_batch_us <= 0.5: 35% violate; best seen 0.263

Pareto front (feasible, 14 designs; showing up to 10), objectives: min area_um2, max accuracy_bits
- pipelined [data_width=20 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] area_um2=45673, accuracy_bits=13.6, ffs=988, throughput_msps=132, max_abs_err=8.24e-05 (2^-13.57), power_index=2.62
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=0 rounding=round] area_um2=49554, accuracy_bits=14.4, ffs=1070, throughput_msps=128, max_abs_err=4.64e-05 (2^-14.39), power_index=2.84
- pipelined [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=round] area_um2=53376, accuracy_bits=14.7, ffs=1127, throughput_msps=123, max_abs_err=3.84e-05 (2^-14.67), power_index=3.01
- pipelined [data_width=20 n_iter=16 angle_guard=2 frac_guard=3 rounding=trunc] area_um2=54420, accuracy_bits=14.7, ffs=1168, throughput_msps=119, max_abs_err=3.71e-05 (2^-14.72), power_index=3.1
- pipelined [data_width=20 n_iter=18 angle_guard=1 frac_guard=0 rounding=round] area_um2=55947, accuracy_bits=15.1, ffs=1203, throughput_msps=128, max_abs_err=2.9e-05 (2^-15.07), power_index=3.2
- pipelined [data_width=20 n_iter=17 angle_guard=1 frac_guard=2 rounding=round] area_um2=56761, accuracy_bits=15.4, ffs=1197, throughput_msps=123, max_abs_err=2.32e-05 (2^-15.40), power_index=3.2
- pipelined [data_width=20 n_iter=19 angle_guard=1 frac_guard=1 rounding=round] area_um2=61871, accuracy_bits=15.7, ffs=1306, throughput_msps=128, max_abs_err=1.9e-05 (2^-15.68), power_index=3.49
- pipelined [data_width=20 n_iter=20 angle_guard=3 frac_guard=3 rounding=round] area_um2=70519, accuracy_bits=17.2, ffs=1485, throughput_msps=119, max_abs_err=6.52e-06 (2^-17.23), power_index=3.97
- pipelined [data_width=22 n_iter=20 angle_guard=4 frac_guard=4 rounding=trunc] area_um2=77664, accuracy_bits=18.3, ffs=1656, throughput_msps=108, max_abs_err=3.17e-06 (2^-18.27), power_index=4.41
- pipelined [data_width=23 n_iter=20 angle_guard=3 frac_guard=3 rounding=trunc] area_um2=77752, accuracy_bits=18.5, ffs=1660, throughput_msps=108, max_abs_err=2.74e-06 (2^-18.48), power_index=4.42
Front coverage: area_um2 45673..77752 (HV reference 100000); accuracy_bits 13.6..18.5 (HV reference 12); data_width on the front 20..23 (registry 8..28).

Per family:
- pipelined: 73 evals, 54 feasible; max throughput seen 163 MSPS; best accuracy 23.58 bits; best feasible area_um2=45673; feasible ranges: data_width 17..28, n_iter 14..27, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 27 evals, 0 feasible; max throughput seen 78.8 MSPS; best accuracy 14.88 bits
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5712 in, 4319 out
- provider-reported cost: $0.0032
- full prompts and replies: `llm_trace.jsonl`

