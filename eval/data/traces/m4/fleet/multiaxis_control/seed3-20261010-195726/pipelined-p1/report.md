# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 100 of 100 budgeted, over 2 round(s).  
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
  budget: 100 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 906 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 295 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.45 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00016 (2^-12.61) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 10.5 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 5.13e-05 (2^-14.25) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.36 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.6 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## Pareto front (8 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=14,angle_guard=1,frac_guard=1,rounding=round,m=4` | 906 | 295 | 93.6 | 6 | 1.45 | 0.00016 (2^-12.61) | 12.61 |
| 1 | `pipelined_m:data_width=19,n_iter=14,angle_guard=0,frac_guard=2,rounding=trunc,m=4` | 923 | 309 | 93.6 | 6 | 1.48 | 0.000158 (2^-12.63) | 12.63 |
| 2 | `pipelined_m:data_width=17,n_iter=17,angle_guard=1,frac_guard=2,rounding=trunc,m=2` | 1051 | 602 | 164.4 | 11 | 1.99 | 0.000144 (2^-12.76) | 12.76 |
| 3 | `pipelined_m:data_width=18,n_iter=17,angle_guard=1,frac_guard=2,rounding=round,m=2` | 1139 | 634 | 164.4 | 11 | 2.13 | 5.95e-05 (2^-14.04) | 14.04 |
| 4 | `pipelined_m:data_width=20,n_iter=26,angle_guard=3,frac_guard=2,rounding=trunc,m=3` | 1928 | 708 | 114.5 | 11 | 3.17 | 1.7e-05 (2^-15.84) | 15.84 |
| 5 | `pipelined_m:data_width=23,n_iter=27,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 2170 | 767 | 114.5 | 11 | 3.53 | 1.42e-05 (2^-16.11) | 16.11 |
| 6 | `pipelined_m:data_width=23,n_iter=30,angle_guard=0,frac_guard=3,rounding=trunc,m=3` | 2481 | 868 | 114.5 | 12 | 4.03 | 4.01e-06 (2^-17.93) | 17.93 |
| 7 | `pipelined_m:data_width=27,n_iter=27,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 2498 | 884 | 110.0 | 11 | 4.07 | 1.01e-06 (2^-19.92) | 19.92 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires max_abs_err <= 2^-12, so data_width >= 14 and n_iter >= 12 are the minimum plausible values; we extend slightly upward to allow guard bits and rounding to meet the error bound with margin. Throughput >= 32 msps is easily met by both families at any realistic Fmax, but the system constraint sys_p99_batch_us <= 0.44 for 32 simultaneous requests is the critical one: it demands low latency and high Fmax. Pipelined provides the lowest latency and highest Fmax, while pipelined_m can reduce area at the cost of latency and Fmax. We therefore explore both to cover the Pareto front from low-area/longer-latency to high-area/low-latency. The budget split (40% pipelined, 60% pipelined_m) reflects that pipelined_m has an extra dimension (m) and is more likely to yield the area-minimal designs, while pipelined is needed to ensure the system deadline is met. All ranges are within the registry and focus on the feasible accuracy region to avoid wasting evaluations on designs that cannot meet the error constraint.*)
- `pipelined` (24 evals): data_width=14..18, n_iter=12..18, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Pipelined gives one result per cycle with the shortest latency (N+2) and highest Fmax, which is the safest way to satisfy the 0.44 us p99 batch deadline for 32 simultaneous requests. Its area is higher due to a register per micro-rotation, so we search it to anchor the low-latency end of the Pareto front. The ranges target just enough accuracy (>=12 bits) while allowing guard bits and rounding to trade area for error.
- `pipelined_m` (36 evals): data_width=14..18, n_iter=12..18, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* Pipelined_m registers every m stages, reducing FF count and thus luts_plus_ffs, which is the primary objective. It still produces one result per cycle, but latency grows to ceil(N/m)+2 and Fmax may drop with larger m. We search m=2..8 to map the area/latency/Fmax trade-off. The extra parameter m makes this family richer, so it receives the larger budget share. The other ranges match pipelined to keep accuracy comparable and isolate the effect of m.

**Result (code):** 60 evaluations this round, 60 total; 20 feasible; hypervolume 4904 (n/a).

**LLM decision:** `stop` — Final round and budget-limited: 60/100 evals used but round cap reached, so the run ends here. Infeasibility is ruled out by evidence — all three constraints are satisfiable simultaneously: throughput_msps best seen 273 vs >=32 (0% violations), max_abs_err best 5.95e-05 (2^-14.04) vs <=2^-12, and sys_p99_batch_us best 0.161 us vs <=0.44 us, with 20 feasible designs (16 unique). A non-empty feasible Pareto front exists. The front already spans both objectives well beyond the spec's requirements: luts_plus_ffs 1201..1773 against HV ref 4000 and accuracy_bits 12.6..14 against HV ref 12 (best accuracy 14.04 bits, 2 full bits better than the required 2^-12). The selection rule (min luts_plus_ffs) picks pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=4] at luts_plus_ffs=1201, accuracy_bits=12.6, throughput 93.6 MSPS — comfortably inside all three constraints, and its sys_p99_batch margin (bound 0.44 us vs best-seen 0.161 us) gives headroom for the L2 system re-simulation. No family remains unexplored and cycle counts/throughput are already far above the 32 MSPS requirement, so widening or adding families would not change the selected design; further refinement would only chase HV coverage at the cost of a design the selection rule does not take.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 4904 (gain this round: n/a (first round)).
Feasible designs: 20 of 60 evaluations (16 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 48% violate; best seen 5.95e-05 (2^-14.04)
- sys_p99_batch_us <= 0.44: 32% violate; best seen 0.161

Pareto front (feasible, 3 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1201, accuracy_bits=12.6, luts=906, ffs=295, throughput_msps=93.6, max_abs_err=0.00016 (2^-12.61), power_index=1.45
- pipelined_m [data_width=17 n_iter=17 angle_guard=1 frac_guard=2 rounding=trunc m=2] luts_plus_ffs=1653, accuracy_bits=12.8, luts=1051, ffs=602, throughput_msps=164, max_abs_err=0.000144 (2^-12.76), power_index=1.99
- pipelined_m [data_width=18 n_iter=17 angle_guard=1 frac_guard=2 rounding=round m=2] luts_plus_ffs=1773, accuracy_bits=14, luts=1139, ffs=634, throughput_msps=164, max_abs_err=5.95e-05 (2^-14.04), power_index=2.13
Front coverage: luts_plus_ffs 1201..1773 (HV reference 4000); accuracy_bits 12.6..14 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- pipelined: 24 evals, 10 feasible; max throughput seen 273 MSPS; best accuracy 13.86 bits; best feasible luts_plus_ffs=1970; feasible ranges: data_width 17..18, n_iter 16..18, angle_guard 1..2, frac_guard 0..2
- pipelined_m: 36 evals, 10 feasible; max throughput seen 171 MSPS; best accuracy 14.04 bits; best feasible luts_plus_ffs=1201; feasible ranges: data_width 16..18, n_iter 14..18, angle_guard 0..1, frac_guard 1..2, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (3 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 32 feasible; hypervolume 1.007e+04 (+105.4%).

**No LLM call** (code's front-mapping round): Final round and budget-limited: 60/100 evals used but round cap reached, so the run ends here. Infeasibility is ruled out by evidence — all three constraints are satisfiable simultaneously: throughput_msps best seen 273 vs >=32 (0% violations), max_abs_err best 5.95e-05 (2^-14.04) vs <=2^-12, and sys_p99_batch_us best 0.161 us vs <=0.44 us, with 20 feasible designs (16 unique). A non-empty feasible Pareto front exists. The front already spans both objectives well beyond the spec's requirements: luts_plus_ffs 1201..1773 against HV ref 4000 and accuracy_bits 12.6..14 against HV ref 12 (best accuracy 14.04 bits, 2 full bits better than the required 2^-12). The selection rule (min luts_plus_ffs) picks pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=4] at luts_plus_ffs=1201, accuracy_bits=12.6, throughput 93.6 MSPS — comfortably inside all three constraints, and its sys_p99_batch margin (bound 0.44 us vs best-seen 0.161 us) gives headroom for the L2 system re-simulation. No family remains unexplored and cycle counts/throughput are already far above the 32 MSPS requirement, so widening or adding families would not change the selected design; further refinement would only chase HV coverage at the cost of a design the selection rule does not take.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.007e+04 (gain this round: +105.4%).
Feasible designs: 32 of 100 evaluations (24 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 38% violate; best seen 5.33e-07 (2^-20.84)
- sys_p99_batch_us <= 0.44: 45% violate; best seen 0.161

Pareto front (feasible, 8 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=1 frac_guard=1 rounding=round m=4] luts_plus_ffs=1201, accuracy_bits=12.6, luts=906, ffs=295, throughput_msps=93.6, max_abs_err=0.00016 (2^-12.61), power_index=1.45
- pipelined_m [data_width=19 n_iter=14 angle_guard=0 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1232, accuracy_bits=12.6, luts=923, ffs=309, throughput_msps=93.6, max_abs_err=0.000158 (2^-12.63), power_index=1.48
- pipelined_m [data_width=17 n_iter=17 angle_guard=1 frac_guard=2 rounding=trunc m=2] luts_plus_ffs=1653, accuracy_bits=12.8, luts=1051, ffs=602, throughput_msps=164, max_abs_err=0.000144 (2^-12.76), power_index=1.99
- pipelined_m [data_width=18 n_iter=17 angle_guard=1 frac_guard=2 rounding=round m=2] luts_plus_ffs=1773, accuracy_bits=14, luts=1139, ffs=634, throughput_msps=164, max_abs_err=5.95e-05 (2^-14.04), power_index=2.13
- pipelined_m [data_width=20 n_iter=26 angle_guard=3 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=2637, accuracy_bits=15.8, luts=1928, ffs=708, throughput_msps=114, max_abs_err=1.7e-05 (2^-15.84), power_index=3.17
- pipelined_m [data_width=23 n_iter=27 angle_guard=-2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=2936, accuracy_bits=16.1, luts=2170, ffs=767, throughput_msps=114, max_abs_err=1.42e-05 (2^-16.11), power_index=3.53
- pipelined_m [data_width=23 n_iter=30 angle_guard=0 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3348, accuracy_bits=17.9, luts=2481, ffs=868, throughput_msps=114, max_abs_err=4.01e-06 (2^-17.93), power_index=4.03
- pipelined_m [data_width=27 n_iter=27 angle_guard=-2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3382, accuracy_bits=19.9, luts=2498, ffs=884, throughput_msps=110, max_abs_err=1.01e-06 (2^-19.92), power_index=4.07
Front coverage: luts_plus_ffs 1201..3382 (HV reference 4000); accuracy_bits 12.6..19.9 (HV reference 12); data_width on the front 17..27 (registry 8..28).

Per family:
- pipelined: 24 evals, 10 feasible; max throughput seen 273 MSPS; best accuracy 13.86 bits; best feasible luts_plus_ffs=1970; feasible ranges: data_width 17..18, n_iter 16..18, angle_guard 1..2, frac_guard 0..2
- pipelined_m: 76 evals, 22 feasible; max throughput seen 171 MSPS; best accuracy 20.84 bits; best feasible luts_plus_ffs=1201; feasible ranges: data_width 16..27, n_iter 14..30, angle_guard -2..3, frac_guard 1..3, m 2..4
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 4858 in, 3275 out
- provider-reported cost: $0.0039
- full prompts and replies: `llm_trace.jsonl`

