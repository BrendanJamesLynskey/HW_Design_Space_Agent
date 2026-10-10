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
`iterative:data_width=15,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 166 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 91 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 198 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 11.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 17 | exact: schedule |
| latency_ns | 85.7 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 0.164 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00081 (2^-10.27) | exact: bit-accurate model, exhaustive (32768 angles) |
| max_abs_err_lsb | 6.64 | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err | 0.00021 (2^-12.22) | exact: bit-accurate model, exhaustive (32768 angles) |
| rms_err_lsb | 1.72 | exact: bit-accurate model, exhaustive (32768 angles) |
| accuracy_bits | 10.3 | exact: bit-accurate model, exhaustive (32768 angles) |

## Pareto front (13 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `iterative:data_width=15,n_iter=15,angle_guard=0,frac_guard=0,rounding=round` | 166 | 91 | 11.0 | 18 | 0.174 | 0.00081 (2^-10.27) | 10.27 |
| 1 | `iterative:data_width=15,n_iter=14,angle_guard=0,frac_guard=0,rounding=round` | 166 | 91 | 11.7 | 17 | 0.164 | 0.00081 (2^-10.27) | 10.27 |
| 2 | `iterative:data_width=15,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 168 | 92 | 11.0 | 18 | 0.176 | 0.000632 (2^-10.63) | 10.63 |
| 3 | `iterative:data_width=16,n_iter=15,angle_guard=1,frac_guard=0,rounding=round` | 179 | 97 | 11.0 | 18 | 0.187 | 0.000301 (2^-11.70) | 11.70 |
| 4 | `iterative:data_width=17,n_iter=22,angle_guard=3,frac_guard=4,rounding=trunc` | 263 | 113 | 6.4 | 25 | 0.353 | 6.21e-05 (2^-13.97) | 13.97 |
| 5 | `iterative:data_width=22,n_iter=21,angle_guard=-1,frac_guard=0,rounding=round` | 294 | 126 | 6.6 | 24 | 0.379 | 1.52e-05 (2^-16.01) | 16.01 |
| 6 | `iterative:data_width=22,n_iter=29,angle_guard=3,frac_guard=0,rounding=round` | 304 | 130 | 4.9 | 32 | 0.523 | 5.23e-06 (2^-17.54) | 17.54 |
| 7 | `iterative:data_width=22,n_iter=26,angle_guard=3,frac_guard=2,rounding=trunc` | 322 | 134 | 5.4 | 29 | 0.497 | 3.55e-06 (2^-18.10) | 18.10 |
| 8 | `iterative:data_width=25,n_iter=22,angle_guard=1,frac_guard=0,rounding=round` | 350 | 143 | 6.2 | 25 | 0.464 | 1.41e-06 (2^-19.44) | 19.44 |
| 9 | `iterative:data_width=27,n_iter=23,angle_guard=-1,frac_guard=0,rounding=round` | 381 | 151 | 5.9 | 26 | 0.521 | 7.31e-07 (2^-20.38) | 20.38 |
| 10 | `iterative:data_width=27,n_iter=24,angle_guard=0,frac_guard=0,rounding=round` | 383 | 152 | 5.7 | 27 | 0.544 | 3.79e-07 (2^-21.33) | 21.33 |
| 11 | `iterative:data_width=27,n_iter=24,angle_guard=2,frac_guard=0,rounding=round` | 387 | 154 | 5.7 | 27 | 0.549 | 2.66e-07 (2^-21.84) | 21.84 |
| 12 | `iterative:data_width=27,n_iter=26,angle_guard=0,frac_guard=2,rounding=round` | 483 | 156 | 5.3 | 29 | 0.698 | 2.57e-07 (2^-21.89) | 21.89 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec demands >=1 MSPS throughput and max_abs_err <= 2^-10, with area (luts_plus_ffs) as the primary objective. Among my assigned families (iterative, unrolled_k), iterative is the absolute minimum-area option but produces only 1 result every N+3 cycles, so at a realistic Fmax (~100-200 MHz) its throughput is ~0.02-0.06 MSPS — far below the 1 MSPS constraint. Thus iterative designs will likely be infeasible on throughput, but I still allocate 50% budget to them because: (1) if Fmax is high enough (e.g., >300 MHz with small N), iterative could barely meet throughput, and (2) the accuracy-vs-area trade-off is identical across families, so iterative results anchor the accuracy side of the front. unrolled_k with k=2-4 is the realistic path to >=1 MSPS: at Fmax ~100-200 MHz, k=2 gives 2 results/cycle → 200-400 MSPS, easily meeting the constraint, while area is only modestly above iterative. I focus data_width 12-16 and n_iter 10-16 because CORDIC accuracy is roughly min(W, N) bits; W=12, N=12 gives ~10-11 bits, and W=16, N=12 gives ~12 bits, bracketing the 2^-10 requirement. angle_guard and frac_guard are kept small (0-1) to minimise area since the accuracy budget is already met by W and N. Both rounding modes are explored to capture the free accuracy gain from rounding.*)
- `iterative` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=-1..1, frac_guard=0..1, rounding=trunc|round. *Why:* iterative is the lowest-area family (shared datapath, no pipeline registers). It is the only family that can plausibly minimise luts_plus_ffs while meeting max_abs_err <= 2^-10. data_width 12-16 and n_iter 10-16 cover the accuracy sweet spot: W=12 with N~12-14 typically gives ~10-12 bits accuracy; W=16 with N~10-12 gives higher accuracy at modest area cost. angle_guard -1..1 and frac_guard 0..1 keep the datapath narrow. Both rounding modes are explored since round can buy ~0.5 bit accuracy for negligible area.
- `unrolled_k` (30 evals): data_width=12..16, n_iter=10..16, angle_guard=-1..1, frac_guard=0..1, rounding=trunc|round, k=2..4. *Why:* unrolled_k with k=2..4 can hit >=1 MSPS throughput at moderate Fmax while keeping area close to iterative (shared FSM, no per-stage pipeline registers). k=2 halves latency vs iterative; k=3-4 further reduce latency at the cost of more parallel adders/shifters. The same accuracy parameters (data_width, n_iter, angle_guard, frac_guard, rounding) apply, so the accuracy-vs-area trade-off is identical to iterative; the k parameter trades area for throughput/latency. This family maps the throughput-vs-area portion of the Pareto front that iterative cannot reach (iterative at 100 MHz gives ~0.03 MSPS, far below 1 MSPS, so iterative designs will be infeasible on throughput unless Fmax is very high — but unrolled_k with small k can meet 1 MSPS at realistic Fmax).

**Result (code):** 60 evaluations this round, 60 total; 34 feasible; hypervolume 2236 (n/a).

**LLM decision:** `stop` — The feasible Pareto front is well-established and meets all constraints. The minimum area design (iterative, 257 LUTs+FFs) achieves 10.3 bits accuracy (max_abs_err 0.00081 < 0.000976562) and 11 MSPS throughput (> 1 MSPS). The front extends to 11.8 bits accuracy with 411 LUTs+FFs, covering the trade-off space effectively. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (257) as per the selection rule.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 2236 (gain this round: n/a (first round)).
Feasible designs: 34 of 60 evaluations (17 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14.2
- max_abs_err <= 0.000976562: 43% violate; best seen 0.000274 (2^-11.83)

Pareto front (feasible, 5 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11, max_abs_err=0.00081 (2^-10.27), power_index=0.174
- iterative [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11.7, max_abs_err=0.00081 (2^-10.27), power_index=0.164
- iterative [data_width=15 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=260, accuracy_bits=10.6, luts=168, ffs=92, throughput_msps=11, max_abs_err=0.000632 (2^-10.63), power_index=0.176
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.7, luts=179, ffs=97, throughput_msps=11, max_abs_err=0.000301 (2^-11.70), power_index=0.187
- unrolled_k [data_width=16 n_iter=16 angle_guard=1 frac_guard=1 rounding=round k=2] luts_plus_ffs=411, accuracy_bits=11.8, luts=313, ffs=98, throughput_msps=9.58, max_abs_err=0.000274 (2^-11.83), power_index=0.17
Front coverage: luts_plus_ffs 257..411 (HV reference 1500); accuracy_bits 10.3..11.8 (HV reference 10); data_width on the front 15..16 (registry 8..28).

Per family:
- iterative: 30 evals, 13 feasible; max throughput seen 14.2 MSPS; best accuracy 11.70 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 15..16, n_iter 13..15, angle_guard -1..1, frac_guard 0..0
- unrolled_k: 30 evals, 21 feasible; max throughput seen 13.5 MSPS; best accuracy 11.83 bits; best feasible luts_plus_ffs=362; feasible ranges: data_width 15..16, n_iter 13..16, angle_guard 0..1, frac_guard 0..1, k 2..3
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `iterative` (32 evals): data_width=14..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of iterative (4 front designs; box front_anchored)
- `unrolled_k` (8 evals): data_width=15..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* code: map the front of unrolled_k (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 73 feasible; hypervolume 1.277e+04 (+471.3%).

**No LLM call** (code's front-mapping round): The feasible Pareto front is well-established and meets all constraints. The minimum area design (iterative, 257 LUTs+FFs) achieves 10.3 bits accuracy (max_abs_err 0.00081 < 0.000976562) and 11 MSPS throughput (> 1 MSPS). The front extends to 11.8 bits accuracy with 411 LUTs+FFs, covering the trade-off space effectively. Since this is the final round, we stop and select the design with minimum luts_plus_ffs (257) as per the selection rule.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.277e+04 (gain this round: +471.3%).
Feasible designs: 73 of 100 evaluations (52 unique).
Families explored so far: iterative, unrolled_k. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 1: 0% violate; best seen 14.2
- max_abs_err <= 0.000976562: 27% violate; best seen 2.57e-07 (2^-21.89)

Pareto front (feasible, 13 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- iterative [data_width=15 n_iter=15 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11, max_abs_err=0.00081 (2^-10.27), power_index=0.174
- iterative [data_width=15 n_iter=14 angle_guard=0 frac_guard=0 rounding=round] luts_plus_ffs=257, accuracy_bits=10.3, luts=166, ffs=91, throughput_msps=11.7, max_abs_err=0.00081 (2^-10.27), power_index=0.164
- iterative [data_width=16 n_iter=15 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=276, accuracy_bits=11.7, luts=179, ffs=97, throughput_msps=11, max_abs_err=0.000301 (2^-11.70), power_index=0.187
- iterative [data_width=17 n_iter=22 angle_guard=3 frac_guard=4 rounding=trunc] luts_plus_ffs=376, accuracy_bits=14, luts=263, ffs=113, throughput_msps=6.36, max_abs_err=6.21e-05 (2^-13.97), power_index=0.353
- iterative [data_width=22 n_iter=21 angle_guard=-1 frac_guard=0 rounding=round] luts_plus_ffs=420, accuracy_bits=16, luts=294, ffs=126, throughput_msps=6.62, max_abs_err=1.52e-05 (2^-16.01), power_index=0.379
- iterative [data_width=22 n_iter=26 angle_guard=3 frac_guard=2 rounding=trunc] luts_plus_ffs=456, accuracy_bits=18.1, luts=322, ffs=134, throughput_msps=5.38, max_abs_err=3.55e-06 (2^-18.10), power_index=0.497
- iterative [data_width=25 n_iter=22 angle_guard=1 frac_guard=0 rounding=round] luts_plus_ffs=493, accuracy_bits=19.4, luts=350, ffs=143, throughput_msps=6.24, max_abs_err=1.41e-06 (2^-19.44), power_index=0.464
- iterative [data_width=27 n_iter=23 angle_guard=-1 frac_guard=0 rounding=round] luts_plus_ffs=533, accuracy_bits=20.4, luts=381, ffs=151, throughput_msps=5.89, max_abs_err=7.31e-07 (2^-20.38), power_index=0.521
- iterative [data_width=27 n_iter=24 angle_guard=2 frac_guard=0 rounding=round] luts_plus_ffs=541, accuracy_bits=21.8, luts=387, ffs=154, throughput_msps=5.68, max_abs_err=2.66e-07 (2^-21.84), power_index=0.549
- iterative [data_width=27 n_iter=26 angle_guard=0 frac_guard=2 rounding=round] luts_plus_ffs=640, accuracy_bits=21.9, luts=483, ffs=156, throughput_msps=5.28, max_abs_err=2.57e-07 (2^-21.89), power_index=0.698
Front coverage: luts_plus_ffs 257..640 (HV reference 1500); accuracy_bits 10.3..21.9 (HV reference 10); data_width on the front 15..27 (registry 8..28).

Per family:
- iterative: 62 evals, 44 feasible; max throughput seen 14.2 MSPS; best accuracy 21.89 bits; best feasible luts_plus_ffs=257; feasible ranges: data_width 15..27, n_iter 13..29, angle_guard -1..4, frac_guard 0..4
- unrolled_k: 38 evals, 29 feasible; max throughput seen 13.5 MSPS; best accuracy 19.86 bits; best feasible luts_plus_ffs=362; feasible ranges: data_width 15..28, n_iter 13..27, angle_guard -1..4, frac_guard 0..3, k 2..8
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4084 in, 1468 out
- provider-reported cost: $0.0042
- full prompts and replies: `llm_trace.jsonl`

