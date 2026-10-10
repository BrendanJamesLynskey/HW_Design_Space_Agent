# DSE run: asic_power_50msps

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 200 of 200 budgeted, over 2 round(s).  
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
`pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=3,rounding=trunc,m=3` — selection: auto (spec rule: min power_index)

| metric | value | provenance |
|---|---|---|
| area_um2 | 29751 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| gate_eq | 7926 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| ffs | 335 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| fmax_mhz | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| throughput_msps | 51.9 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| latency_cycles | 7 | exact: schedule |
| latency_ns | 135 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| power_index | 1.81 | estimate: cost_asic (sky130hd-tt_025C_1v80-yosys0.33-opensta-v1, 57 measured points) |
| max_abs_err | 0.000187 (2^-12.39) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.06 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 4.64e-05 (2^-14.39) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 0.761 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.4 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (17 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | area µm² † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=3,rounding=trunc,m=3` | 29751 | 335 | 51.9 | 7 | 1.81 | 0.000187 (2^-12.39) | 12.39 |
| 1 | `pipelined_m:data_width=16,n_iter=14,angle_guard=3,frac_guard=3,rounding=round,m=3` | 29469 | 342 | 51.9 | 7 | 1.82 | 0.000171 (2^-12.51) | 12.51 |
| 2 | `pipelined_m:data_width=18,n_iter=16,angle_guard=1,frac_guard=0,rounding=round,m=3` | 32414 | 401 | 51.9 | 8 | 2.07 | 0.000108 (2^-13.18) | 13.18 |
| 3 | `pipelined_m:data_width=19,n_iter=15,angle_guard=0,frac_guard=1,rounding=trunc,m=2` | 35691 | 554 | 72.3 | 10 | 2.59 | 0.000101 (2^-13.27) | 13.27 |
| 4 | `pipelined_m:data_width=19,n_iter=15,angle_guard=0,frac_guard=3,rounding=trunc,m=2` | 37733 | 582 | 66.8 | 10 | 2.73 | 9.73e-05 (2^-13.33) | 13.33 |
| 5 | `pipelined_m:data_width=19,n_iter=15,angle_guard=2,frac_guard=2,rounding=trunc,m=2` | 37777 | 584 | 69.4 | 10 | 2.74 | 7.77e-05 (2^-13.65) | 13.65 |
| 6 | `pipelined_m:data_width=19,n_iter=17,angle_guard=2,frac_guard=0,rounding=round,m=2` | 40497 | 621 | 69.4 | 11 | 2.92 | 4.23e-05 (2^-14.53) | 14.53 |
| 7 | `pipelined_m:data_width=19,n_iter=17,angle_guard=2,frac_guard=3,rounding=trunc,m=2` | 43998 | 669 | 66.8 | 11 | 3.15 | 3.2e-05 (2^-14.93) | 14.93 |
| 8 | `pipelined_m:data_width=19,n_iter=17,angle_guard=2,frac_guard=3,rounding=round,m=2` | 45012 | 670 | 66.8 | 11 | 3.19 | 2.52e-05 (2^-15.28) | 15.28 |
| 9 | `pipelined_m:data_width=21,n_iter=23,angle_guard=1,frac_guard=2,rounding=trunc,m=2` | 62201 | 922 | 64.3 | 14 | 4.4 | 9.95e-06 (2^-16.62) | 16.62 |
| 10 | `pipelined_m:data_width=21,n_iter=25,angle_guard=1,frac_guard=3,rounding=trunc,m=2` | 69370 | 1020 | 62.0 | 15 | 4.88 | 9.28e-06 (2^-16.72) | 16.72 |
| 11 | `pipelined_m:data_width=25,n_iter=25,angle_guard=2,frac_guard=3,rounding=trunc,m=2` | 81206 | 1194 | 54.3 | 15 | 5.71 | 4.08e-07 (2^-21.23) | 21.23 |
| 12 | `pipelined_m:data_width=28,n_iter=25,angle_guard=0,frac_guard=1,rounding=trunc,m=2` | 84115 | 1242 | 52.7 | 15 | 5.93 | 1.81e-07 (2^-22.40) | 22.40 |
| 13 | `pipelined_m:data_width=28,n_iter=25,angle_guard=0,frac_guard=1,rounding=round,m=2` | 85590 | 1244 | 52.7 | 15 | 5.98 | 1.66e-07 (2^-22.52) | 22.52 |
| 14 | `pipelined:data_width=28,n_iter=24,angle_guard=2,frac_guard=1,rounding=round` | 106523 | 2240 | 96.1 | 26 | 9.36 | 1.64e-07 (2^-22.54) | 22.54 |
| 15 | `pipelined:data_width=28,n_iter=24,angle_guard=4,frac_guard=2,rounding=trunc` | 109407 | 2328 | 91.1 | 26 | 9.69 | 1.55e-07 (2^-22.62) | 22.62 |
| 16 | `pipelined:data_width=28,n_iter=24,angle_guard=4,frac_guard=2,rounding=round` | 110881 | 2330 | 91.1 | 26 | 9.74 | 1.38e-07 (2^-22.79) | 22.79 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Constraints are throughput_msps >= 50 and max_abs_err <= 2^-12; objectives are min power_index (selection rule) and max accuracy_bits (HV ref 12). Both my families are 1-result/cycle, so the throughput constraint reduces to Fmax >= 50 MHz, and accuracy is identical across families for the same datapath parameters. That makes this a pure register-count/power problem: pipelined_m with the largest m that still holds Fmax >= 50 should dominate pipelined, which is exactly what the fleet numbers show (best power 2.11 vs 4.21). So I weight pipelined_m 60% to attack the min-power corner the selection rule cares about, and pipelined 40% to keep the accuracy end of the front populated where pipelined_m's longer combinational path may fall below 50 MHz. Accuracy ranges are set from the LSB: output LSB = 2^-(W-2), so W>=13 is the hard floor for 2^-12 and W=14+ gives rounding margin; n_iter 10..20 covers both the convergence-limited low-power corner and full precision. Guards and rounding are included as cheap accuracy knobs. Round 1 spends the full 100-eval round on this split; later rounds should re-center m and W/N on the feasible boundary the first round reveals.*)
- `pipelined_m` (60 evals): data_width=13..20, n_iter=10..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round, m=2..6. *Why:* This is the family that owns the selection objective. It already produced the fleet's lowest feasible power_index (2.11) and 3 of the 18 merged-front points, so it is the only family that can push the min-power corner. Its risk is Fmax: with m>1 the combinational path grows and throughput_msps = Fmax x 1 must stay >= 50, which is why only 15/45 of its draws were feasible. I therefore keep m in 2..6 (small enough to plausibly hold Fmax >= 50, large enough to actually cut register count and power) and let the search find the m where Fmax crosses 50. data_width starts at 13 because the output LSB is 2^-(W-2) and max_abs_err <= 2^-12 is only reachable at W>=13 (W=13 is borderline, W=14+ gives rounding margin); n_iter 10..20 spans the convergence-limited low-power corner up to full-precision. angle_guard/frac_guard 0..3 and both rounding modes are cheap accuracy levers that let the search trade a few bits of datapath for fewer iterations.
- `pipelined` (40 evals): data_width=13..20, n_iter=10..20, angle_guard=0..3, frac_guard=0..3, rounding=trunc|round. *Why:* The fleet's evidence says pipelined is the workhorse of the merged front (15 of 18 points, 39/55 feasible, best power 4.21). It computes identical bits to pipelined_m for the same (W, N, guards, rounding), so it is the reliable way to populate the mid/high-accuracy part of the front where pipelined_m may be Fmax-infeasible. It is unlikely to win the min-power selection rule (its per-stage registers cost more than pipelined_m), but hypervolume rewards covering the whole curve, and its higher Fmax gives headroom at the accuracy end. Same accuracy ranges as pipelined_m so the two families are directly comparable point-for-point on the (power_index, accuracy_bits) plane.

**Result (code):** 100 evaluations this round, 100 total; 20 feasible; hypervolume 121.1 (n/a).

**LLM decision:** `stop` — [LLM failed to answer: openrouter:deepseek/deepseek-v4.1-flash failed to produce AnalysisDecision: LengthFinishReasonError: Could not parse response content as the length limit was reached - CompletionUsage(completion_tokens=16000, prompt_tokens=2512, total_tokens=18512, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=0, reasoning_tokens=16000, rejected_prediction_tokens=None, text_tokens=None, image_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cache_write_tokens=0, cached_tokens=2048, image_tokens=None, text_tokens=None,]
- **rule applied by code:** LLM produced no valid decision; treated as stop
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 100 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 121.1 (gain this round: n/a (first round)).
Feasible designs: 20 of 100 evaluations (16 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 45% violate; best seen 163
- max_abs_err <= 0.000244141: 50% violate; best seen 1.04e-05 (2^-16.56)

Pareto front (feasible, 6 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=3] power_index=1.81, accuracy_bits=12.4, area_um2=29751, ffs=335, throughput_msps=51.9, max_abs_err=0.000187 (2^-12.39)
- pipelined_m [data_width=16 n_iter=14 angle_guard=3 frac_guard=3 rounding=round m=3] power_index=1.82, accuracy_bits=12.5, area_um2=29469, ffs=342, throughput_msps=51.9, max_abs_err=0.000171 (2^-12.51)
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=2.07, accuracy_bits=13.2, area_um2=32414, ffs=401, throughput_msps=51.9, max_abs_err=0.000108 (2^-13.18)
- pipelined [data_width=20 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] power_index=4.77, accuracy_bits=14.8, area_um2=54108, ffs=1142, throughput_msps=123, max_abs_err=3.61e-05 (2^-14.76)
- pipelined [data_width=20 n_iter=17 angle_guard=2 frac_guard=2 rounding=trunc] power_index=5.03, accuracy_bits=15.2, area_um2=56475, ffs=1212, throughput_msps=123, max_abs_err=2.57e-05 (2^-15.25)
- pipelined [data_width=20 n_iter=18 angle_guard=2 frac_guard=1 rounding=trunc] power_index=5.2, accuracy_bits=15.3, area_um2=58341, ffs=1253, throughput_msps=123, max_abs_err=2.4e-05 (2^-15.35)
Front coverage: power_index 1.81..5.2 (HV reference 40); accuracy_bits 12.4..15.3 (HV reference 12); data_width on the front 16..20 (registry 8..28).

Per family:
- pipelined: 40 evals, 15 feasible; max throughput seen 163 MSPS; best accuracy 15.35 bits; best feasible power_index=3.85; feasible ranges: data_width 15..20, n_iter 16..19, angle_guard 0..3, frac_guard 1..2
- pipelined_m: 60 evals, 5 feasible; max throughput seen 82.5 MSPS; best accuracy 16.56 bits; best feasible power_index=1.81; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard 1..3, frac_guard 0..3, m 3..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (50 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (3 front designs; box front_anchored)
- `pipelined` (50 evals): data_width=19..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 91 feasible; hypervolume 380.6 (+214.2%).

**No LLM call** (code's front-mapping round): [LLM failed to answer: openrouter:deepseek/deepseek-v4.1-flash failed to produce AnalysisDecision: LengthFinishReasonError: Could not parse response content as the length limit was reached - CompletionUsage(completion_tokens=16000, prompt_tokens=2512, total_tokens=18512, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=0, reasoning_tokens=16000, rejected_prediction_tokens=None, text_tokens=None, image_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cache_write_tokens=0, cached_tokens=2048, image_tokens=None, text_tokens=None,]
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 380.6 (gain this round: +214.2%).
Feasible designs: 91 of 200 evaluations (77 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: area/gate equivalents/FFs/Fmax/throughput/power are cost-model ESTIMATES (sky130 standard cells, calibrated on Yosys + OpenSTA synthesis); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 36% violate; best seen 163
- max_abs_err <= 0.000244141: 28% violate; best seen 1.38e-07 (2^-22.79)

Pareto front (feasible, 17 designs; showing up to 10), objectives: min power_index, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=3] power_index=1.81, accuracy_bits=12.4, area_um2=29751, ffs=335, throughput_msps=51.9, max_abs_err=0.000187 (2^-12.39)
- pipelined_m [data_width=18 n_iter=16 angle_guard=1 frac_guard=0 rounding=round m=3] power_index=2.07, accuracy_bits=13.2, area_um2=32414, ffs=401, throughput_msps=51.9, max_abs_err=0.000108 (2^-13.18)
- pipelined_m [data_width=19 n_iter=15 angle_guard=0 frac_guard=3 rounding=trunc m=2] power_index=2.73, accuracy_bits=13.3, area_um2=37733, ffs=582, throughput_msps=66.8, max_abs_err=9.73e-05 (2^-13.33)
- pipelined_m [data_width=19 n_iter=15 angle_guard=2 frac_guard=2 rounding=trunc m=2] power_index=2.74, accuracy_bits=13.7, area_um2=37777, ffs=584, throughput_msps=69.4, max_abs_err=7.77e-05 (2^-13.65)
- pipelined_m [data_width=19 n_iter=17 angle_guard=2 frac_guard=3 rounding=trunc m=2] power_index=3.15, accuracy_bits=14.9, area_um2=43998, ffs=669, throughput_msps=66.8, max_abs_err=3.2e-05 (2^-14.93)
- pipelined_m [data_width=21 n_iter=23 angle_guard=1 frac_guard=2 rounding=trunc m=2] power_index=4.4, accuracy_bits=16.6, area_um2=62201, ffs=922, throughput_msps=64.3, max_abs_err=9.95e-06 (2^-16.62)
- pipelined_m [data_width=25 n_iter=25 angle_guard=2 frac_guard=3 rounding=trunc m=2] power_index=5.71, accuracy_bits=21.2, area_um2=81206, ffs=1194, throughput_msps=54.3, max_abs_err=4.08e-07 (2^-21.23)
- pipelined_m [data_width=28 n_iter=25 angle_guard=0 frac_guard=1 rounding=trunc m=2] power_index=5.93, accuracy_bits=22.4, area_um2=84115, ffs=1242, throughput_msps=52.7, max_abs_err=1.81e-07 (2^-22.40)
- pipelined [data_width=28 n_iter=24 angle_guard=2 frac_guard=1 rounding=round] power_index=9.36, accuracy_bits=22.5, area_um2=106523, ffs=2240, throughput_msps=96.1, max_abs_err=1.64e-07 (2^-22.54)
- pipelined [data_width=28 n_iter=24 angle_guard=4 frac_guard=2 rounding=round] power_index=9.74, accuracy_bits=22.8, area_um2=110881, ffs=2330, throughput_msps=91.1, max_abs_err=1.38e-07 (2^-22.79)
Front coverage: power_index 1.81..9.74 (HV reference 40); accuracy_bits 12.4..22.8 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- pipelined: 90 evals, 65 feasible; max throughput seen 163 MSPS; best accuracy 22.79 bits; best feasible power_index=3.85; feasible ranges: data_width 15..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 110 evals, 26 feasible; max throughput seen 82.5 MSPS; best accuracy 22.52 bits; best feasible power_index=1.81; feasible ranges: data_width 16..28, n_iter 14..27, angle_guard -1..3, frac_guard 0..3, m 2..3
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 2)
- tokens: 1731 in, 3330 out
- provider-reported cost: $0.0041
- full prompts and replies: `llm_trace.jsonl`

