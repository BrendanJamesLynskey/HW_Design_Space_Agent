# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 200 of 200 budgeted, over 2 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec multiaxis_control: Shared sin/cos unit for a 16-axis motor-control loop: a 1 MHz control tick issues 32 requests at once (Park + inverse Park per axis); all 32 results must be back within 0.44 us of the tick (p99 over ticks). Max error <= 2^-12. Minimise LUTs + FFs.
  constraint: throughput_msps >= 32
  constraint: max_abs_err <= 0.000244141
  constraint: sys_p99_batch_us <= 0.44
  objective: min luts_plus_ffs (HV ref 4000)
  objective: max accuracy_bits (HV ref 12)
  select: min luts_plus_ffs
  system (simulated at L2 for the shortlist; screened at L1 by an analytic bound): control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average)
  budget: 200 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 841 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 282 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.35 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000235 (2^-12.06) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 7.7 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.91e-05 (2^-14.05) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.94 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.1 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (25 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=17,n_iter=14,angle_guard=2,frac_guard=1,rounding=trunc,m=4` | 841 | 282 | 93.6 | 6 | 1.35 | 0.000235 (2^-12.06) | 12.06 |
| 1 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=2,rounding=trunc,m=3` | 855 | 348 | 119.3 | 7 | 1.45 | 0.000204 (2^-12.26) | 12.26 |
| 2 | `pipelined_m:data_width=19,n_iter=14,angle_guard=-1,frac_guard=2,rounding=trunc,m=4` | 909 | 305 | 93.6 | 6 | 1.46 | 0.00018 (2^-12.44) | 12.44 |
| 3 | `pipelined_m:data_width=17,n_iter=14,angle_guard=1,frac_guard=2,rounding=round,m=3` | 890 | 350 | 119.3 | 7 | 1.49 | 0.000171 (2^-12.51) | 12.51 |
| 4 | `pipelined_m:data_width=19,n_iter=14,angle_guard=2,frac_guard=3,rounding=trunc,m=4` | 978 | 323 | 93.6 | 6 | 1.57 | 0.000136 (2^-12.84) | 12.84 |
| 5 | `pipelined_m:data_width=19,n_iter=14,angle_guard=4,frac_guard=1,rounding=round,m=4` | 991 | 321 | 89.6 | 6 | 1.58 | 0.000132 (2^-12.88) | 12.88 |
| 6 | `pipelined_m:data_width=19,n_iter=14,angle_guard=4,frac_guard=3,rounding=trunc,m=4` | 1005 | 331 | 89.6 | 6 | 1.61 | 0.000132 (2^-12.89) | 12.89 |
| 7 | `pipelined_m:data_width=20,n_iter=15,angle_guard=0,frac_guard=0,rounding=round,m=3` | 979 | 378 | 119.3 | 7 | 1.63 | 8.24e-05 (2^-13.57) | 13.57 |
| 8 | `pipelined_m:data_width=20,n_iter=15,angle_guard=2,frac_guard=3,rounding=trunc,m=4` | 1097 | 337 | 89.6 | 6 | 1.73 | 6.77e-05 (2^-13.85) | 13.85 |
| 9 | `pipelined_m:data_width=20,n_iter=15,angle_guard=2,frac_guard=4,rounding=trunc,m=4` | 1126 | 343 | 89.6 | 6 | 1.77 | 6.58e-05 (2^-13.89) | 13.89 |
| 10 | `pipelined_m:data_width=20,n_iter=16,angle_guard=1,frac_guard=2,rounding=trunc,m=3` | 1128 | 472 | 119.3 | 8 | 1.93 | 4.33e-05 (2^-14.50) | 14.50 |
| 11 | `pipelined_m:data_width=19,n_iter=16,angle_guard=2,frac_guard=3,rounding=round,m=3` | 1168 | 470 | 119.3 | 8 | 1.97 | 3.97e-05 (2^-14.62) | 14.62 |
| 12 | `pipelined_m:data_width=21,n_iter=17,angle_guard=0,frac_guard=1,rounding=round,m=3` | 1247 | 478 | 119.3 | 8 | 2.08 | 2.64e-05 (2^-15.21) | 15.21 |
| 13 | `pipelined_m:data_width=19,n_iter=17,angle_guard=4,frac_guard=4,rounding=round,m=4` | 1310 | 416 | 89.6 | 7 | 2.08 | 2.02e-05 (2^-15.59) | 15.59 |
| 14 | `pipelined_m:data_width=21,n_iter=18,angle_guard=1,frac_guard=2,rounding=trunc,m=4` | 1331 | 417 | 89.6 | 7 | 2.1 | 1.43e-05 (2^-16.10) | 16.10 |
| 15 | `pipelined_m:data_width=21,n_iter=18,angle_guard=2,frac_guard=2,rounding=trunc,m=3` | 1349 | 498 | 114.5 | 8 | 2.22 | 1.3e-05 (2^-16.23) | 16.23 |
| 16 | `pipelined_m:data_width=21,n_iter=22,angle_guard=1,frac_guard=0,rounding=round,m=4` | 1554 | 472 | 93.6 | 8 | 2.44 | 1.21e-05 (2^-16.34) | 16.34 |
| 17 | `pipelined_m:data_width=21,n_iter=18,angle_guard=3,frac_guard=3,rounding=trunc,m=2` | 1403 | 754 | 158.3 | 11 | 2.6 | 1.08e-05 (2^-16.50) | 16.50 |
| 18 | `pipelined_m:data_width=24,n_iter=21,angle_guard=-2,frac_guard=0,rounding=round,m=3` | 1607 | 592 | 114.5 | 9 | 2.65 | 6.44e-06 (2^-17.25) | 17.25 |
| 19 | `pipelined_m:data_width=24,n_iter=22,angle_guard=0,frac_guard=0,rounding=round,m=3` | 1731 | 686 | 114.5 | 10 | 2.91 | 2.73e-06 (2^-18.48) | 18.48 |
| 20 | `pipelined_m:data_width=24,n_iter=28,angle_guard=0,frac_guard=0,rounding=round,m=4` | 2224 | 606 | 89.6 | 9 | 3.41 | 2.49e-06 (2^-18.62) | 18.62 |
| 21 | `pipelined_m:data_width=26,n_iter=22,angle_guard=0,frac_guard=0,rounding=trunc,m=2` | 1864 | 996 | 158.3 | 13 | 3.44 | 1.23e-06 (2^-19.64) | 19.64 |
| 22 | `pipelined_m:data_width=28,n_iter=22,angle_guard=3,frac_guard=0,rounding=round,m=3` | 2063 | 815 | 105.9 | 10 | 3.46 | 5.3e-07 (2^-20.85) | 20.85 |
| 23 | `pipelined_m:data_width=28,n_iter=22,angle_guard=3,frac_guard=4,rounding=round,m=3` | 2299 | 874 | 105.9 | 10 | 3.82 | 4.9e-07 (2^-20.96) | 20.96 |
| 24 | `pipelined_m:data_width=28,n_iter=23,angle_guard=3,frac_guard=1,rounding=round,m=2` | 2267 | 1219 | 147.4 | 14 | 4.2 | 2.72e-07 (2^-21.81) | 21.81 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Accuracy is the binding constraint (max_abs_err <= 2^-12), so W and N are centred on the threshold (W 14-20, N 10-18) with full guard-bit ranges; the batch deadline (32 results in 0.44us) is met by the 1-result/cycle families, so the real trade-off is area vs Fmax via m. pipelined_m already dominates the merged front (8/8, best 1201 LUT+FF), so it takes most of the budget to map its low-area corner, with a small pipelined share for diversity.*)
- `pipelined_m` (80 evals): data_width=14..20, n_iter=10..18, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* pipelined_m owns 8/8 of the merged front and the cheapest feasible design (1201 LUT+FF); it gives 1 result/cycle so it can clear the 32-request/0.44us batch, and m trades pipeline FFs against Fmax. Search the low-area corner (small W, small N) while keeping m full-range because Fmax interacts with the batch deadline.
- `pipelined` (20 evals): data_width=14..20, n_iter=10..18, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Same 1-result/cycle throughput and identical accuracy bits as pipelined_m, but register-every-stage costs more FFs; keep a small share to confirm it is dominated and to catch any Fmax advantage that could help the batch deadline.

**Result (code):** 100 evaluations this round, 100 total; 43 feasible; hypervolume 8977 (n/a).

**LLM decision:** `stop` — [LLM failed to answer: openrouter:deepseek/deepseek-v4.1-flash failed to produce AnalysisDecision: LengthFinishReasonError: Could not parse response content as the length limit was reached - CompletionUsage(completion_tokens=16000, prompt_tokens=3433, total_tokens=19433, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=0, reasoning_tokens=16000, rejected_prediction_tokens=None, text_tokens=None, image_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cache_write_tokens=0, cached_tokens=3072, image_tokens=None, text_tokens=None,]
- **rule applied by code:** LLM produced no valid decision; treated as stop
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 100 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 200.
Hypervolume of the feasible front: 8977 (gain this round: n/a (first round)).
Feasible designs: 43 of 100 evaluations (36 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 43% violate; best seen 2.02e-05 (2^-15.59)
- sys_p99_batch_us <= 0.44: 24% violate; best seen 0.159

Pareto front (feasible, 12 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1123, accuracy_bits=12.1, luts=841, ffs=282, throughput_msps=93.6, max_abs_err=0.000235 (2^-12.06), power_index=1.35
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=1203, accuracy_bits=12.3, luts=855, ffs=348, throughput_msps=119, max_abs_err=0.000204 (2^-12.26), power_index=1.45
- pipelined_m [data_width=19 n_iter=14 angle_guard=-1 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1214, accuracy_bits=12.4, luts=909, ffs=305, throughput_msps=93.6, max_abs_err=0.00018 (2^-12.44), power_index=1.46
- pipelined_m [data_width=19 n_iter=14 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1301, accuracy_bits=12.8, luts=978, ffs=323, throughput_msps=93.6, max_abs_err=0.000136 (2^-12.84), power_index=1.57
- pipelined_m [data_width=19 n_iter=14 angle_guard=4 frac_guard=1 rounding=round m=4] luts_plus_ffs=1311, accuracy_bits=12.9, luts=991, ffs=321, throughput_msps=89.6, max_abs_err=0.000132 (2^-12.88), power_index=1.58
- pipelined_m [data_width=19 n_iter=14 angle_guard=4 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1336, accuracy_bits=12.9, luts=1005, ffs=331, throughput_msps=89.6, max_abs_err=0.000132 (2^-12.89), power_index=1.61
- pipelined_m [data_width=20 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1434, accuracy_bits=13.9, luts=1097, ffs=337, throughput_msps=89.6, max_abs_err=6.77e-05 (2^-13.85), power_index=1.73
- pipelined_m [data_width=20 n_iter=16 angle_guard=1 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=1600, accuracy_bits=14.5, luts=1128, ffs=472, throughput_msps=119, max_abs_err=4.33e-05 (2^-14.50), power_index=1.93
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=3 rounding=round m=3] luts_plus_ffs=1638, accuracy_bits=14.6, luts=1168, ffs=470, throughput_msps=119, max_abs_err=3.97e-05 (2^-14.62), power_index=1.97
- pipelined_m [data_width=19 n_iter=17 angle_guard=4 frac_guard=4 rounding=round m=4] luts_plus_ffs=1725, accuracy_bits=15.6, luts=1310, ffs=416, throughput_msps=89.6, max_abs_err=2.02e-05 (2^-15.59), power_index=2.08
Front coverage: luts_plus_ffs 1123..1725 (HV reference 4000); accuracy_bits 12.1..15.6 (HV reference 12); data_width on the front 17..20 (registry 8..28).

Per family:
- pipelined: 20 evals, 6 feasible; max throughput seen 273 MSPS; best accuracy 15.38 bits; best feasible luts_plus_ffs=1806; feasible ranges: data_width 17..18, n_iter 14..18, angle_guard 3..4, frac_guard 1..4
- pipelined_m: 80 evals, 37 feasible; max throughput seen 171 MSPS; best accuracy 15.59 bits; best feasible luts_plus_ffs=1123; feasible ranges: data_width 17..20, n_iter 14..18, angle_guard -2..4, frac_guard 1..4, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (12 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 109 feasible; hypervolume 1.747e+04 (+94.6%).

**No LLM call** (code's front-mapping round): [LLM failed to answer: openrouter:deepseek/deepseek-v4.1-flash failed to produce AnalysisDecision: LengthFinishReasonError: Could not parse response content as the length limit was reached - CompletionUsage(completion_tokens=16000, prompt_tokens=3433, total_tokens=19433, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=0, reasoning_tokens=16000, rejected_prediction_tokens=None, text_tokens=None, image_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cache_write_tokens=0, cached_tokens=3072, image_tokens=None, text_tokens=None,]
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 200.
Hypervolume of the feasible front: 1.747e+04 (gain this round: +94.6%).
Feasible designs: 109 of 200 evaluations (100 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 28% violate; best seen 2.63e-07 (2^-21.86)
- sys_p99_batch_us <= 0.44: 26% violate; best seen 0.159

Pareto front (feasible, 25 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=17 n_iter=14 angle_guard=2 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1123, accuracy_bits=12.1, luts=841, ffs=282, throughput_msps=93.6, max_abs_err=0.000235 (2^-12.06), power_index=1.35
- pipelined_m [data_width=17 n_iter=14 angle_guard=1 frac_guard=2 rounding=round m=3] luts_plus_ffs=1241, accuracy_bits=12.5, luts=890, ffs=350, throughput_msps=119, max_abs_err=0.000171 (2^-12.51), power_index=1.49
- pipelined_m [data_width=19 n_iter=14 angle_guard=4 frac_guard=1 rounding=round m=4] luts_plus_ffs=1311, accuracy_bits=12.9, luts=991, ffs=321, throughput_msps=89.6, max_abs_err=0.000132 (2^-12.88), power_index=1.58
- pipelined_m [data_width=20 n_iter=15 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1434, accuracy_bits=13.9, luts=1097, ffs=337, throughput_msps=89.6, max_abs_err=6.77e-05 (2^-13.85), power_index=1.73
- pipelined_m [data_width=19 n_iter=16 angle_guard=2 frac_guard=3 rounding=round m=3] luts_plus_ffs=1638, accuracy_bits=14.6, luts=1168, ffs=470, throughput_msps=119, max_abs_err=3.97e-05 (2^-14.62), power_index=1.97
- pipelined_m [data_width=19 n_iter=17 angle_guard=4 frac_guard=4 rounding=round m=4] luts_plus_ffs=1725, accuracy_bits=15.6, luts=1310, ffs=416, throughput_msps=89.6, max_abs_err=2.02e-05 (2^-15.59), power_index=2.08
- pipelined_m [data_width=21 n_iter=22 angle_guard=1 frac_guard=0 rounding=round m=4] luts_plus_ffs=2026, accuracy_bits=16.3, luts=1554, ffs=472, throughput_msps=93.6, max_abs_err=1.21e-05 (2^-16.34), power_index=2.44
- pipelined_m [data_width=24 n_iter=22 angle_guard=0 frac_guard=0 rounding=round m=3] luts_plus_ffs=2417, accuracy_bits=18.5, luts=1731, ffs=686, throughput_msps=114, max_abs_err=2.73e-06 (2^-18.48), power_index=2.91
- pipelined_m [data_width=26 n_iter=22 angle_guard=0 frac_guard=0 rounding=trunc m=2] luts_plus_ffs=2860, accuracy_bits=19.6, luts=1864, ffs=996, throughput_msps=158, max_abs_err=1.23e-06 (2^-19.64), power_index=3.44
- pipelined_m [data_width=28 n_iter=23 angle_guard=3 frac_guard=1 rounding=round m=2] luts_plus_ffs=3485, accuracy_bits=21.8, luts=2267, ffs=1219, throughput_msps=147, max_abs_err=2.72e-07 (2^-21.81), power_index=4.2
Front coverage: luts_plus_ffs 1123..3485 (HV reference 4000); accuracy_bits 12.1..21.8 (HV reference 12); data_width on the front 17..28 (registry 8..28).

Per family:
- pipelined: 20 evals, 6 feasible; max throughput seen 273 MSPS; best accuracy 15.38 bits; best feasible luts_plus_ffs=1806; feasible ranges: data_width 17..18, n_iter 14..18, angle_guard 3..4, frac_guard 1..4
- pipelined_m: 180 evals, 103 feasible; max throughput seen 171 MSPS; best accuracy 21.86 bits; best feasible luts_plus_ffs=1123; feasible ranges: data_width 16..28, n_iter 13..29, angle_guard -2..4, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 3 (failed/unparsed attempts: 2)
- tokens: 2816 in, 2425 out
- provider-reported cost: $0.0017
- full prompts and replies: `llm_trace.jsonl`

