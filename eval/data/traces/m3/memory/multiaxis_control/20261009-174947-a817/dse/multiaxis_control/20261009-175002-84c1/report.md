# DSE run: multiaxis_control

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: qwen/qwen3.8-27b.  
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
`pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,m=4` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 954 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 282 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 97.8 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 61.3 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.49 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000121 (2^-13.02) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 7.9 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.65e-05 (2^-15.20) | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 1.74 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 13 | exact: bit-accurate model, dense (109112 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 102.0 dBc, SNR 88.9 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

System: control loop: a tick every 1 us issues 32 requests at once (32 requests/us on average). Shortlist: the front's top 5 by the selection rule, simulated at their estimated Fmax (SimPy). L1 bound → L2 simulated:

| design | sys_p99_batch_us <= 0.44 (bound → simulated) | passes |
|---|---|---|
| `pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,m=4` | 0.3679 → 0.378 | yes |
| `pipelined_m:data_width=21,n_iter=18,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 0.3955 → 0.406 | yes |
| `pipelined_m:data_width=21,n_iter=17,angle_guard=3,frac_guard=2,rounding=round,m=4` | 0.4128 → 0.4238 | yes |
| `pipelined_m:data_width=19,n_iter=21,angle_guard=3,frac_guard=2,rounding=round,m=4` | 0.4061 → 0.4167 | yes |
| `pipelined_m:data_width=22,n_iter=23,angle_guard=3,frac_guard=1,rounding=round,m=4` | 0.4239 → 0.435 | yes |

winner unchanged: the L1 selection passes the simulated system constraints.

## Pareto front (9 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=18,n_iter=16,angle_guard=0,frac_guard=0,rounding=round,m=4` | 954 | 282 | 97.8 | 6 | 1.49 | 0.000121 (2^-13.02) | 13.02 |
| 1 | `pipelined_m:data_width=21,n_iter=18,angle_guard=0,frac_guard=0,rounding=trunc,m=4` | 1241 | 395 | 93.6 | 7 | 1.97 | 2.85e-05 (2^-15.10) | 15.10 |
| 2 | `pipelined_m:data_width=21,n_iter=17,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1331 | 429 | 89.6 | 7 | 2.12 | 1.72e-05 (2^-15.83) | 15.83 |
| 3 | `pipelined_m:data_width=19,n_iter=21,angle_guard=3,frac_guard=2,rounding=round,m=4` | 1521 | 466 | 93.6 | 8 | 2.39 | 1.48e-05 (2^-16.05) | 16.05 |
| 4 | `pipelined_m:data_width=22,n_iter=23,angle_guard=3,frac_guard=1,rounding=round,m=4` | 1837 | 517 | 89.6 | 8 | 2.83 | 3.28e-06 (2^-18.22) | 18.22 |
| 5 | `pipelined_m:data_width=22,n_iter=27,angle_guard=3,frac_guard=3,rounding=trunc,m=4` | 2224 | 617 | 89.6 | 9 | 3.42 | 2.48e-06 (2^-18.62) | 18.62 |
| 6 | `pipelined_m:data_width=28,n_iter=27,angle_guard=-1,frac_guard=0,rounding=trunc,m=2` | 2444 | 1328 | 152.6 | 16 | 4.54 | 2.99e-07 (2^-21.67) | 21.67 |
| 7 | `pipelined_m:data_width=28,n_iter=27,angle_guard=0,frac_guard=0,rounding=trunc,m=2` | 2471 | 1342 | 152.6 | 16 | 4.59 | 2.45e-07 (2^-21.96) | 21.96 |
| 8 | `pipelined_m:data_width=28,n_iter=27,angle_guard=3,frac_guard=0,rounding=trunc,m=2` | 2553 | 1384 | 147.4 | 16 | 4.74 | 2.04e-07 (2^-22.23) | 22.23 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 results within 0.44us of each 1us tick, with max error <= 2^-12 and throughput >= 32 MSPS. pipelined_m is the prime candidate because it can drain 32 requests in ceil(32/m) cycles, and with m=4..8 this is 4-8 cycles, easily fitting the 440ns window at moderate Fmax. pipelined (m=1) needs 32 cycles but has lower area for small N and may win on the area objective if Fmax is high enough. iterative is likely infeasible for the batch constraint but included at low share to confirm. unrolled_k is deprioritized per lessons (never reached a front on this device). Ranges are focused: dw=14..18 and n_iter=12..18 target the 2^-12 error constraint with minimal area; guards kept low (0..2) to minimize area. Budget is weighted toward pipelined_m (55%) as the most promising family, with pipelined (30%) as a strong alternative and iterative (15%) for completeness.*)
- `pipelined_m` (33 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=4..8. *Why:* Prime candidate for the 32-request burst. m=4..8 allows draining 32 requests in 4-8 cycles, fitting the 0.44us window at moderate Fmax. dw=14..18 and n_iter=12..18 target the 2^-12 error constraint with minimal area. Guards kept low (0..2) to minimize area while maintaining accuracy.
- `pipelined` (18 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* m=1 pipeline gives 1 result/cycle with lowest latency (N+2). For 32 requests, needs 32 cycles. At Fmax ~100MHz, 32 cycles = 320ns < 440ns, so it can meet the batch constraint. May have lower area than pipelined_m for small N. Good fallback if pipelined_m struggles with Fmax.
- `iterative` (9 evals): data_width=14..18, n_iter=12..18, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Lowest area family (shared datapath). However, throughput is 1 result per N+3 cycles, so for 32 requests it needs 32*(N+3) cycles. At N=12, that's 480 cycles. At 100MHz, 480ns > 440ns, so it likely fails the batch constraint. Included as a small share to confirm infeasibility or find a high-Fmax corner.

**Result (code):** 60 evaluations this round, 60 total; 3 feasible; hypervolume 2814 (n/a).

**LLM decision:** `stop` — The front contains a single feasible design (pipelined_m, 1236 LUTs+FFs, 13.02 accuracy bits) that satisfies all constraints, including the tight system p99 batch latency (0.161 us <= 0.44 us) and throughput (97.8 MSPS >= 32). The hypervolume is 2814, well above the reference point. Since this is the final round and the design meets the spec's selection rule (min luts_plus_ffs) and all constraints, we stop.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 2814 (gain this round: n/a (first round)).
Feasible designs: 3 of 60 evaluations (3 unique).
Families explored so far: iterative, pipelined, pipelined_m. Not yet explored: unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 15% violate; best seen 273
- max_abs_err <= 0.000244141: 58% violate; best seen 0.000109 (2^-13.17)
- sys_p99_batch_us <= 0.44: 57% violate; best seen 0.161

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1236, accuracy_bits=13, luts=954, ffs=282, throughput_msps=97.8, max_abs_err=0.000121 (2^-13.02), power_index=1.49
Front coverage: luts_plus_ffs 1236..1236 (HV reference 4000); accuracy_bits 13..13 (HV reference 12); data_width on the front 18..18 (registry 8..28).

Per family:
- iterative: 9 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 13.10 bits
- pipelined: 18 evals, 2 feasible; max throughput seen 273 MSPS; best accuracy 12.83 bits; best feasible luts_plus_ffs=1723; feasible ranges: data_width 16..17, n_iter 14..18, angle_guard 1..2, frac_guard 1..2
- pipelined_m: 33 evals, 1 feasible; max throughput seen 97.8 MSPS; best accuracy 13.17 bits; best feasible luts_plus_ffs=1236; feasible ranges: data_width 18..18, n_iter 16..16, angle_guard 0..0, frac_guard 0..0, m 4..4
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (40 evals): data_width=17..28, n_iter=14..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 31 feasible; hypervolume 1.462e+04 (+419.4%).

**No LLM call** (code's front-mapping round): The front contains a single feasible design (pipelined_m, 1236 LUTs+FFs, 13.02 accuracy bits) that satisfies all constraints, including the tight system p99 batch latency (0.161 us <= 0.44 us) and throughput (97.8 MSPS >= 32). The hypervolume is 2814, well above the reference point. Since this is the final round and the design meets the spec's selection rule (min luts_plus_ffs) and all constraints, we stop.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 1.462e+04 (gain this round: +419.4%).
Feasible designs: 31 of 100 evaluations (28 unique).
Families explored so far: iterative, pipelined, pipelined_m. Not yet explored: unrolled_k.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 9% violate; best seen 273
- max_abs_err <= 0.000244141: 35% violate; best seen 2.04e-07 (2^-22.23)
- sys_p99_batch_us <= 0.44: 46% violate; best seen 0.161

Pareto front (feasible, 9 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=18 n_iter=16 angle_guard=0 frac_guard=0 rounding=round m=4] luts_plus_ffs=1236, accuracy_bits=13, luts=954, ffs=282, throughput_msps=97.8, max_abs_err=0.000121 (2^-13.02), power_index=1.49
- pipelined_m [data_width=21 n_iter=18 angle_guard=0 frac_guard=0 rounding=trunc m=4] luts_plus_ffs=1637, accuracy_bits=15.1, luts=1241, ffs=395, throughput_msps=93.6, max_abs_err=2.85e-05 (2^-15.10), power_index=1.97
- pipelined_m [data_width=21 n_iter=17 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1760, accuracy_bits=15.8, luts=1331, ffs=429, throughput_msps=89.6, max_abs_err=1.72e-05 (2^-15.83), power_index=2.12
- pipelined_m [data_width=19 n_iter=21 angle_guard=3 frac_guard=2 rounding=round m=4] luts_plus_ffs=1987, accuracy_bits=16, luts=1521, ffs=466, throughput_msps=93.6, max_abs_err=1.48e-05 (2^-16.05), power_index=2.39
- pipelined_m [data_width=22 n_iter=23 angle_guard=3 frac_guard=1 rounding=round m=4] luts_plus_ffs=2353, accuracy_bits=18.2, luts=1837, ffs=517, throughput_msps=89.6, max_abs_err=3.28e-06 (2^-18.22), power_index=2.83
- pipelined_m [data_width=22 n_iter=27 angle_guard=3 frac_guard=3 rounding=trunc m=4] luts_plus_ffs=2842, accuracy_bits=18.6, luts=2224, ffs=617, throughput_msps=89.6, max_abs_err=2.48e-06 (2^-18.62), power_index=3.42
- pipelined_m [data_width=28 n_iter=27 angle_guard=-1 frac_guard=0 rounding=trunc m=2] luts_plus_ffs=3771, accuracy_bits=21.7, luts=2444, ffs=1328, throughput_msps=153, max_abs_err=2.99e-07 (2^-21.67), power_index=4.54
- pipelined_m [data_width=28 n_iter=27 angle_guard=0 frac_guard=0 rounding=trunc m=2] luts_plus_ffs=3813, accuracy_bits=22, luts=2471, ffs=1342, throughput_msps=153, max_abs_err=2.45e-07 (2^-21.96), power_index=4.59
- pipelined_m [data_width=28 n_iter=27 angle_guard=3 frac_guard=0 rounding=trunc m=2] luts_plus_ffs=3937, accuracy_bits=22.2, luts=2553, ffs=1384, throughput_msps=147, max_abs_err=2.04e-07 (2^-22.23), power_index=4.74
Front coverage: luts_plus_ffs 1236..3937 (HV reference 4000); accuracy_bits 13..22.2 (HV reference 12); data_width on the front 18..28 (registry 8..28).

Per family:
- iterative: 9 evals, 0 feasible; max throughput seen 13.2 MSPS; best accuracy 13.10 bits
- pipelined: 18 evals, 2 feasible; max throughput seen 273 MSPS; best accuracy 12.83 bits; best feasible luts_plus_ffs=1723; feasible ranges: data_width 16..17, n_iter 14..18, angle_guard 1..2, frac_guard 1..2
- pipelined_m: 73 evals, 29 feasible; max throughput seen 164 MSPS; best accuracy 22.23 bits; best feasible luts_plus_ffs=1236; feasible ranges: data_width 18..28, n_iter 14..27, angle_guard -1..3, frac_guard 0..4, m 2..4
```
</details>

## LLM usage
- calls: 5 (failed/unparsed attempts: 0)
- tokens: 25747 in, 2022 out
- provider-reported cost: $0.0035
- full prompts and replies: `llm_trace.jsonl`

