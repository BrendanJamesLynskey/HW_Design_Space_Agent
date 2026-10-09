# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: anthropic/claude-sonnet-5.5.  
**Evaluations:** 240 of 240 budgeted, over 3 round(s).  
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
  budget: 240 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=17,n_iter=15,angle_guard=3,frac_guard=2,rounding=trunc,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 949 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 293 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 93.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 64.1 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.5 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.00013 (2^-12.91) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 4.25 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 3.27e-05 (2^-14.90) | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.07 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 12.9 | exact: bit-accurate model, dense (91168 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 5 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 93.3 dBc, SNR 83.6 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=5` | 0.4342 → 0.4465 | no |
| `pipelined_m:data_width=17,n_iter=15,angle_guard=3,frac_guard=2,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=3,rounding=round,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=16,angle_guard=2,frac_guard=3,rounding=trunc,m=4` | 0.3848 → 0.3953 | yes |
| `pipelined_m:data_width=17,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=4` | 0.3848 → 0.3953 | yes |

**WINNER CHANGED AT L2**: the L1 selection pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=5 fails the simulated system constraints (sys_p99_batch_us <= 0.44 by 1.5%); the best shortlisted design that passes is pipelined_m:data_width=17,n_iter=15,angle_guard=3,frac_guard=2,rounding=trunc,m=4.

## Pareto front (20 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=15,angle_guard=2,frac_guard=1,rounding=round,m=5` | 895 | 211 | 80.6 | 5 | 1.33 | 0.00018 (2^-12.44) | 12.44 |
| 1 | `pipelined_m:data_width=17,n_iter=15,angle_guard=3,frac_guard=2,rounding=trunc,m=4` | 949 | 293 | 93.6 | 6 | 1.5 | 0.00013 (2^-12.91) | 12.91 |
| 2 | `pipelined_m:data_width=18,n_iter=15,angle_guard=0,frac_guard=3,rounding=round,m=4` | 1017 | 303 | 93.6 | 6 | 1.59 | 0.000125 (2^-12.97) | 12.97 |
| 3 | `pipelined_m:data_width=17,n_iter=16,angle_guard=2,frac_guard=3,rounding=trunc,m=4` | 1033 | 295 | 93.6 | 6 | 1.6 | 9.12e-05 (2^-13.42) | 13.42 |
| 4 | `pipelined_m:data_width=17,n_iter=16,angle_guard=2,frac_guard=2,rounding=round,m=4` | 1037 | 291 | 93.6 | 6 | 1.6 | 8.59e-05 (2^-13.51) | 13.51 |
| 5 | `pipelined_m:data_width=18,n_iter=16,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1102 | 309 | 93.6 | 6 | 1.7 | 5.17e-05 (2^-14.24) | 14.24 |
| 6 | `pipelined_m:data_width=18,n_iter=18,angle_guard=2,frac_guard=3,rounding=trunc,m=3` | 1223 | 448 | 119.3 | 8 | 2.01 | 4.39e-05 (2^-14.48) | 14.48 |
| 7 | `pipelined_m:data_width=20,n_iter=22,angle_guard=3,frac_guard=1,rounding=round,m=4` | 1619 | 476 | 89.6 | 8 | 2.52 | 1.24e-05 (2^-16.30) | 16.30 |
| 8 | `pipelined_m:data_width=20,n_iter=22,angle_guard=3,frac_guard=3,rounding=trunc,m=4` | 1665 | 494 | 89.6 | 8 | 2.6 | 8.7e-06 (2^-16.81) | 16.81 |
| 9 | `pipelined_m:data_width=27,n_iter=18,angle_guard=-1,frac_guard=2,rounding=trunc,m=3` | 1618 | 601 | 110.0 | 8 | 2.67 | 7.98e-06 (2^-16.94) | 16.94 |
| 10 | `pipelined_m:data_width=27,n_iter=18,angle_guard=-2,frac_guard=3,rounding=trunc,m=3` | 1635 | 605 | 110.0 | 8 | 2.7 | 7.97e-06 (2^-16.94) | 16.94 |
| 11 | `pipelined_m:data_width=27,n_iter=18,angle_guard=-1,frac_guard=4,rounding=round,m=3` | 1746 | 624 | 105.9 | 8 | 2.85 | 7.95e-06 (2^-16.94) | 16.94 |
| 12 | `pipelined_m:data_width=26,n_iter=21,angle_guard=-1,frac_guard=0,rounding=round,m=3` | 1754 | 646 | 114.5 | 9 | 2.89 | 1.66e-06 (2^-19.20) | 19.20 |
| 13 | `pipelined_m:data_width=26,n_iter=21,angle_guard=-1,frac_guard=3,rounding=trunc,m=3` | 1881 | 682 | 110.0 | 9 | 3.09 | 1.58e-06 (2^-19.27) | 19.27 |
| 14 | `pipelined_m:data_width=26,n_iter=24,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 2041 | 567 | 89.6 | 8 | 3.14 | 9.44e-07 (2^-20.02) | 20.02 |
| 15 | `pipelined_m:data_width=27,n_iter=22,angle_guard=-1,frac_guard=2,rounding=trunc,m=3` | 1997 | 785 | 110.0 | 10 | 3.35 | 9.19e-07 (2^-20.05) | 20.05 |
| 16 | `pipelined_m:data_width=26,n_iter=22,angle_guard=4,frac_guard=2,rounding=trunc,m=3` | 2041 | 799 | 110.0 | 10 | 3.42 | 6.45e-07 (2^-20.56) | 20.56 |
| 17 | `pipelined_m:data_width=28,n_iter=22,angle_guard=-1,frac_guard=1,rounding=round,m=3` | 2078 | 799 | 110.0 | 10 | 3.46 | 6.24e-07 (2^-20.61) | 20.61 |
| 18 | `pipelined_m:data_width=26,n_iter=24,angle_guard=3,frac_guard=1,rounding=trunc,m=3` | 2162 | 777 | 110.0 | 10 | 3.54 | 4.63e-07 (2^-21.04) | 21.04 |
| 19 | `pipelined_m:data_width=26,n_iter=26,angle_guard=3,frac_guard=3,rounding=trunc,m=3` | 2455 | 900 | 110.0 | 11 | 4.04 | 1.72e-07 (2^-22.47) | 22.47 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The 32 requests arrive together and must all return within 0.44 us, so the unit needs about 73 MSPS effective, and iterative designs are unlikely to meet that. Accuracy of 2^-12 needs roughly W of 14-16 and N of 12-14, so the ranges stay around those values. Most budget goes to pipelined and pipelined_m, which are most likely to be feasible. A smaller share probes high-k unrolled as a possible area saver. Later rounds can narrow in on the Pareto front once feasibility is known.*)
- `pipelined` (51 evals): data_width=12..18, n_iter=11..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round. *Why:* One result per cycle at Fmax means a batch of 32 drains in about 32 cycles plus latency, which should fit the 0.44 us window and the 32 MSPS throughput. Narrow ranges around the accuracy needed for 2^-12 error keep area low.
- `pipelined_m` (33 evals): data_width=12..18, n_iter=11..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, m=2..4. *Why:* Registering every m stages saves FFs and latency cycles while keeping 1 result per cycle. Fmax drops with larger m, which risks the batch deadline, so m is kept small.
- `unrolled_k` (16 evals): data_width=12..18, n_iter=11..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, k=4..8. *Why:* A shared datapath is smaller, but it accepts a request only every few cycles, so the burst of 32 queues. Only high k could plausibly meet the 0.44 us batch bound, so this is a smaller exploratory share to test whether it can.

**Result (code):** 100 evaluations this round, 100 total; 36 feasible; hypervolume 5477 (n/a).

**LLM decision:** `refine` — The whole front is pipelined_m (7 designs, 1210..1691 LUTs+FFs, 12.4..14.2 bits). Pipelined has a best feasible area of 1798, which is dominated. unrolled_k never gets above 12.4 MSPS and has 0 feasible designs. Plain iterative is slower than unrolled_k, so it cannot reach the 32 MSPS throughput constraint and I won't spend budget on it. The cheapest front points use m=4 and data_width 15..18, so lower area probably lies at slightly smaller widths, fewer iterations and larger m. m is bounded by Fmax and the 0.44 us batch bound, so I will test m 3..6. The feasible region seen has data_width 15..18 and n_iter 14..16. I will extend the lower edge to 13 and 12 to test the 2^-12 error limit, which is the main driver of infeasibility (61% violate). Pipelined gets a small share to confirm it stays dominated.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 240.
Hypervolume of the feasible front: 5477 (gain this round: n/a (first round)).
Feasible designs: 36 of 100 evaluations (28 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 16% violate; best seen 282
- max_abs_err <= 0.000244141: 61% violate; best seen 5.44e-05 (2^-14.17)
- sys_p99_batch_us <= 0.44: 16% violate; best seen 0.158

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1210, accuracy_bits=12.4, luts=909, ffs=301, throughput_msps=93.6, max_abs_err=0.000185 (2^-12.40), power_index=1.46
- pipelined_m [data_width=15 n_iter=16 angle_guard=3 frac_guard=3 rounding=round m=4] luts_plus_ffs=1258, accuracy_bits=12.6, luts=985, ffs=272, throughput_msps=97.8, max_abs_err=0.000158 (2^-12.63), power_index=1.51
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=3 rounding=round m=4] luts_plus_ffs=1320, accuracy_bits=13, luts=1017, ffs=303, throughput_msps=93.6, max_abs_err=0.000125 (2^-12.97), power_index=1.59
- pipelined_m [data_width=18 n_iter=15 angle_guard=2 frac_guard=1 rounding=trunc m=2] luts_plus_ffs=1508, accuracy_bits=13.1, luts=949, ffs=559, throughput_msps=164, max_abs_err=0.000118 (2^-13.05), power_index=1.82
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=2 rounding=round m=2] luts_plus_ffs=1614, accuracy_bits=13.3, luts=1055, ffs=559, throughput_msps=164, max_abs_err=0.000102 (2^-13.25), power_index=1.94
- pipelined_m [data_width=17 n_iter=16 angle_guard=3 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=1618, accuracy_bits=13.6, luts=1048, ffs=569, throughput_msps=164, max_abs_err=8.14e-05 (2^-13.58), power_index=1.95
- pipelined_m [data_width=18 n_iter=16 angle_guard=3 frac_guard=3 rounding=trunc m=2] luts_plus_ffs=1691, accuracy_bits=14.2, luts=1096, ffs=595, throughput_msps=164, max_abs_err=5.44e-05 (2^-14.17), power_index=2.04
Front coverage: luts_plus_ffs 1210..1691 (HV reference 4000); accuracy_bits 12.4..14.2 (HV reference 12); data_width on the front 15..18 (registry 8..28).

Per family:
- unrolled_k: 16 evals, 0 feasible; max throughput seen 12.4 MSPS; best accuracy 12.68 bits
- pipelined: 51 evals, 19 feasible; max throughput seen 282 MSPS; best accuracy 13.57 bits; best feasible luts_plus_ffs=1798; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 33 evals, 17 feasible; max throughput seen 171 MSPS; best accuracy 14.17 bits; best feasible luts_plus_ffs=1210; feasible ranges: data_width 15..18, n_iter 14..16, angle_guard -1..3, frac_guard 0..3, m 2..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *Concentrate on pipelined_m at lower widths and larger m to push the area end of the front below 1210, while keeping accuracy at or above 12 bits.*)
- `pipelined_m` (36 evals): data_width=13..18, n_iter=12..16, angle_guard=-1..3, frac_guard=0..3, rounding=trunc|round, m=3..6. *Why:* All front points come from this family. Larger m and smaller width or n_iter may cut LUTs+FFs while still meeting 2^-12 error, throughput and the 0.44 us batch bound.
- `pipelined` (8 evals): data_width=14..17, n_iter=12..15, angle_guard=-1..2, frac_guard=0..2, rounding=trunc|round. *Why:* Fully pipelined has the best Fmax but higher area (best feasible 1798). A small check at the lower-width corner confirms whether it stays dominated.

**Result (code):** 44 evaluations this round, 144 total; 51 feasible; hypervolume 6033 (+10.2%).

**LLM decision:** `stop` — This is the final round, so only stop or infeasible are valid. The constraints are clearly reachable: 51 of 144 evaluations are feasible and the front has 7 designs. The cheapest feasible design is pipelined_m at 1143 LUTs+FFs with 12.3 accuracy bits, 93.6 MSPS against the 32 MSPS requirement, and error 2^-12.25 against the 2^-12 limit. Accuracy reaches 14.24 bits at 1411 LUTs+FFs. The unrolled_k family is at most 12.4 MSPS and has 0 feasible designs, so it cannot meet the 32 MSPS throughput constraint. The best pipelined design, at 1798, is dominated by pipelined_m. The final design will be chosen by min luts_plus_ffs with L2 re-selection among the shortlist.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 96 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 144 of 240.
Hypervolume of the feasible front: 6033 (gain this round: +10.2%).
Feasible designs: 51 of 144 evaluations (42 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 11% violate; best seen 282
- max_abs_err <= 0.000244141: 59% violate; best seen 5.17e-05 (2^-14.24)
- sys_p99_batch_us <= 0.44: 19% violate; best seen 0.158

Pareto front (feasible, 7 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1143, accuracy_bits=12.3, luts=855, ffs=289, throughput_msps=93.6, max_abs_err=0.000205 (2^-12.25), power_index=1.38
- pipelined_m [data_width=18 n_iter=14 angle_guard=0 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1210, accuracy_bits=12.4, luts=909, ffs=301, throughput_msps=93.6, max_abs_err=0.000185 (2^-12.40), power_index=1.46
- pipelined_m [data_width=17 n_iter=15 angle_guard=3 frac_guard=2 rounding=trunc m=4] luts_plus_ffs=1242, accuracy_bits=12.9, luts=949, ffs=293, throughput_msps=93.6, max_abs_err=0.00013 (2^-12.91), power_index=1.5
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=3 rounding=round m=4] luts_plus_ffs=1320, accuracy_bits=13, luts=1017, ffs=303, throughput_msps=93.6, max_abs_err=0.000125 (2^-12.97), power_index=1.59
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=1327, accuracy_bits=13.4, luts=1033, ffs=295, throughput_msps=93.6, max_abs_err=9.12e-05 (2^-13.42), power_index=1.6
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1327, accuracy_bits=13.5, luts=1037, ffs=291, throughput_msps=93.6, max_abs_err=8.59e-05 (2^-13.51), power_index=1.6
- pipelined_m [data_width=18 n_iter=16 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1411, accuracy_bits=14.2, luts=1102, ffs=309, throughput_msps=93.6, max_abs_err=5.17e-05 (2^-14.24), power_index=1.7
Front coverage: luts_plus_ffs 1143..1411 (HV reference 4000); accuracy_bits 12.3..14.2 (HV reference 12); data_width on the front 17..18 (registry 8..28).

Per family:
- unrolled_k: 16 evals, 0 feasible; max throughput seen 12.4 MSPS; best accuracy 12.68 bits
- pipelined: 59 evals, 19 feasible; max throughput seen 282 MSPS; best accuracy 13.57 bits; best feasible luts_plus_ffs=1798; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 69 evals, 32 feasible; max throughput seen 171 MSPS; best accuracy 14.24 bits; best feasible luts_plus_ffs=1143; feasible ranges: data_width 15..18, n_iter 14..16, angle_guard -1..3, frac_guard 0..3, m 2..4
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 96 evaluations*)
- `pipelined_m` (96 evals): data_width=16..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (7 front designs; box front_anchored)

**Result (code):** 96 evaluations this round, 240 total; 116 feasible; hypervolume 1.808e+04 (+199.7%).

**No LLM call** (code's front-mapping round): This is the final round, so only stop or infeasible are valid. The constraints are clearly reachable: 51 of 144 evaluations are feasible and the front has 7 designs. The cheapest feasible design is pipelined_m at 1143 LUTs+FFs with 12.3 accuracy bits, 93.6 MSPS against the 32 MSPS requirement, and error 2^-12.25 against the 2^-12 limit. Accuracy reaches 14.24 bits at 1411 LUTs+FFs. The unrolled_k family is at most 12.4 MSPS and has 0 feasible designs, so it cannot meet the 32 MSPS throughput constraint. The best pipelined design, at 1798, is dominated by pipelined_m. The final design will be chosen by min luts_plus_ffs with L2 re-selection among the shortlist.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 240 of 240.
Hypervolume of the feasible front: 1.808e+04 (gain this round: +199.7%).
Feasible designs: 116 of 240 evaluations (104 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 7% violate; best seen 282
- max_abs_err <= 0.000244141: 39% violate; best seen 1.72e-07 (2^-22.47)
- sys_p99_batch_us <= 0.44: 22% violate; best seen 0.158

Pareto front (feasible, 20 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=2 frac_guard=1 rounding=round m=5] luts_plus_ffs=1105, accuracy_bits=12.4, luts=895, ffs=211, throughput_msps=80.6, max_abs_err=0.00018 (2^-12.44), power_index=1.33
- pipelined_m [data_width=18 n_iter=15 angle_guard=0 frac_guard=3 rounding=round m=4] luts_plus_ffs=1320, accuracy_bits=13, luts=1017, ffs=303, throughput_msps=93.6, max_abs_err=0.000125 (2^-12.97), power_index=1.59
- pipelined_m [data_width=17 n_iter=16 angle_guard=2 frac_guard=2 rounding=round m=4] luts_plus_ffs=1327, accuracy_bits=13.5, luts=1037, ffs=291, throughput_msps=93.6, max_abs_err=8.59e-05 (2^-13.51), power_index=1.6
- pipelined_m [data_width=18 n_iter=18 angle_guard=2 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=1671, accuracy_bits=14.5, luts=1223, ffs=448, throughput_msps=119, max_abs_err=4.39e-05 (2^-14.48), power_index=2.01
- pipelined_m [data_width=20 n_iter=22 angle_guard=3 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=2159, accuracy_bits=16.8, luts=1665, ffs=494, throughput_msps=89.6, max_abs_err=8.7e-06 (2^-16.81), power_index=2.6
- pipelined_m [data_width=27 n_iter=18 angle_guard=-1 frac_guard=4 rounding=round m=3] luts_plus_ffs=2370, accuracy_bits=16.9, luts=1746, ffs=624, throughput_msps=106, max_abs_err=7.95e-06 (2^-16.94), power_index=2.85
- pipelined_m [data_width=26 n_iter=21 angle_guard=-1 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=2563, accuracy_bits=19.3, luts=1881, ffs=682, throughput_msps=110, max_abs_err=1.58e-06 (2^-19.27), power_index=3.09
- pipelined_m [data_width=27 n_iter=22 angle_guard=-1 frac_guard=2 rounding=trunc m=3] luts_plus_ffs=2782, accuracy_bits=20.1, luts=1997, ffs=785, throughput_msps=110, max_abs_err=9.19e-07 (2^-20.05), power_index=3.35
- pipelined_m [data_width=28 n_iter=22 angle_guard=-1 frac_guard=1 rounding=round m=3] luts_plus_ffs=2877, accuracy_bits=20.6, luts=2078, ffs=799, throughput_msps=110, max_abs_err=6.24e-07 (2^-20.61), power_index=3.46
- pipelined_m [data_width=26 n_iter=26 angle_guard=3 frac_guard=3 rounding=trunc m=3] luts_plus_ffs=3355, accuracy_bits=22.5, luts=2455, ffs=900, throughput_msps=110, max_abs_err=1.72e-07 (2^-22.47), power_index=4.04
Front coverage: luts_plus_ffs 1105..3355 (HV reference 4000); accuracy_bits 12.4..22.5 (HV reference 12); data_width on the front 16..28 (registry 8..28).

Per family:
- unrolled_k: 16 evals, 0 feasible; max throughput seen 12.4 MSPS; best accuracy 12.68 bits
- pipelined: 59 evals, 19 feasible; max throughput seen 282 MSPS; best accuracy 13.57 bits; best feasible luts_plus_ffs=1798; feasible ranges: data_width 16..18, n_iter 14..16, angle_guard -1..3, frac_guard 0..3
- pipelined_m: 165 evals, 97 feasible; max throughput seen 171 MSPS; best accuracy 22.47 bits; best feasible luts_plus_ffs=1105; feasible ranges: data_width 15..28, n_iter 14..29, angle_guard -2..4, frac_guard 0..4, m 2..5
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 28996 in, 2748 out
- provider-reported cost: $0.0855
- full prompts and replies: `llm_trace.jsonl`

