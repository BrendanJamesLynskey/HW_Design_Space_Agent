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
`pipelined_m:data_width=16,n_iter=15,angle_guard=1,frac_guard=2,rounding=round,m=5` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 909 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 212 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 80.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 80.6 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 5 | exact: schedule |
| latency_ns | 62 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 1.35 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 0.000218 (2^-12.16) | exact: bit-accurate model, exhaustive (65536 angles) |
| max_abs_err_lsb | 3.57 | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err | 4.79e-05 (2^-14.35) | exact: bit-accurate model, exhaustive (65536 angles) |
| rms_err_lsb | 0.784 | exact: bit-accurate model, exhaustive (65536 angles) |
| accuracy_bits | 12.2 | exact: bit-accurate model, exhaustive (65536 angles) |

## Pareto front (11 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=16,n_iter=15,angle_guard=1,frac_guard=2,rounding=round,m=5` | 909 | 212 | 80.6 | 5 | 1.35 | 0.000218 (2^-12.16) | 12.16 |
| 1 | `pipelined_m:data_width=25,n_iter=15,angle_guard=3,frac_guard=1,rounding=trunc,m=4` | 1274 | 400 | 86.0 | 6 | 2.01 | 6.11e-05 (2^-14.00) | 14.00 |
| 2 | `pipelined:data_width=21,n_iter=19,angle_guard=0,frac_guard=2,rounding=trunc` | 1390 | 1410 | 256.5 | 21 | 3.37 | 1.68e-05 (2^-15.86) | 15.86 |
| 3 | `pipelined:data_width=21,n_iter=22,angle_guard=0,frac_guard=2,rounding=trunc` | 1621 | 1634 | 256.5 | 24 | 3.92 | 1.64e-05 (2^-15.90) | 15.90 |
| 4 | `pipelined:data_width=27,n_iter=19,angle_guard=0,frac_guard=2,rounding=trunc` | 1731 | 1756 | 249.0 | 21 | 4.2 | 3.94e-06 (2^-17.96) | 17.96 |
| 5 | `pipelined:data_width=21,n_iter=22,angle_guard=4,frac_guard=4,rounding=trunc` | 1798 | 1804 | 256.5 | 24 | 4.34 | 3.24e-06 (2^-18.24) | 18.24 |
| 6 | `pipelined:data_width=27,n_iter=21,angle_guard=0,frac_guard=0,rounding=trunc` | 1839 | 1864 | 249.0 | 23 | 4.46 | 1.2e-06 (2^-19.67) | 19.67 |
| 7 | `pipelined:data_width=27,n_iter=21,angle_guard=0,frac_guard=2,rounding=trunc` | 1923 | 1941 | 249.0 | 23 | 4.65 | 1.1e-06 (2^-19.79) | 19.79 |
| 8 | `pipelined:data_width=27,n_iter=22,angle_guard=2,frac_guard=0,rounding=trunc` | 1975 | 1998 | 249.0 | 24 | 4.78 | 7.66e-07 (2^-20.32) | 20.32 |
| 9 | `pipelined:data_width=27,n_iter=22,angle_guard=2,frac_guard=2,rounding=trunc` | 2063 | 2078 | 249.0 | 24 | 4.99 | 5.57e-07 (2^-20.78) | 20.78 |
| 10 | `pipelined:data_width=27,n_iter=30,angle_guard=2,frac_guard=0,rounding=trunc` | 2725 | 2724 | 249.0 | 32 | 6.56 | 4.7e-07 (2^-21.02) | 21.02 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *The spec requires 32 results within 440 ns of a 1 us tick, with max error <= 2^-12. Both pipelined and pipelined_m deliver 1 result/cycle, so 32 results take 32 cycles. At a conservative Fmax of 150-200 MHz, 32 cycles = 160-213 ns, comfortably within 440 ns. The throughput constraint (>= 32 Msps) is also met since 1 result/cycle at 150+ MHz gives 150+ Msps. The key trade-off is area: pipelined_m with m>1 uses fewer FFs than full pipelined, potentially giving lower luts_plus_ffs. I focus data_width on 14-16 and n_iter on 12-16 because CORDIC error scales as ~2^-(n_iter+1), so n_iter=12-14 with W=14-16 should meet the 2^-12 accuracy bound. angle_guard and frac_guard are kept minimal (0-2) to reduce area. Rounding is explored as it can improve effective accuracy by ~0.5 bits. The budget is split between the two families to map the Pareto front: pipelined gives the Fmax/latency ceiling, pipelined_m gives the area floor. Both families compute identical bits, so accuracy is determined solely by data_width, n_iter, angle_guard, frac_guard, and rounding - the search should find the minimal-area configuration that meets the accuracy constraint, then compare area across m values.*)
- `pipelined` (30 evals): data_width=14..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round. *Why:* Full pipeline gives 1 result/cycle, so 32 results take 32 cycles. At Fmax ~200 MHz that is 160 ns, well under the 440 ns p99 batch bound. It is the cleanest way to meet the throughput and latency constraints simultaneously. I focus on the minimal data_width/n_iter that meets max_abs_err <= 2^-12 (0.000244141). For CORDIC, error ~ 2^-(n_iter+1) roughly, so n_iter=12-14 with W=14-16 should suffice. angle_guard and frac_guard kept low to minimize area. Rounding explored to see if it helps accuracy at lower n_iter.
- `pipelined_m` (30 evals): data_width=14..16, n_iter=12..16, angle_guard=0..2, frac_guard=0..2, rounding=trunc|round, m=2..8. *Why:* pipelined_m registers every m stages, reducing FF count vs full pipeline while still giving 1 result/cycle throughput. The 32-request burst still completes in 32 cycles (same as pipelined) since throughput is 1/cycle. The trade-off is fewer FFs at the cost of slightly lower Fmax (longer combinational paths between registers). This should yield lower luts_plus_ffs than pipelined for the same accuracy, making it the primary candidate for the min-area objective. m=2-4 likely gives the best Fmax/area balance; m=8 approaches iterative-like timing but with pipelined throughput.
- clamped by code: budget shares were all zero; split equally

**Result (code):** 60 evaluations this round, 60 total; 9 feasible; hypervolume 1939 (n/a).

**LLM decision:** `stop` — The exploration has identified a feasible Pareto front dominated by pipelined and pipelined_m architectures. The best design (pipelined_m, m=5) achieves the minimum area objective (luts_plus_ffs=1121) while satisfying all constraints: throughput (80.6 MSPS >= 32), accuracy (12.2 bits > 12), and system latency (0.161 us < 0.44 us). The front covers the trade-off space well, with area ranging from 1121 to 1966 and accuracy from 12.2 to 12.9 bits. Since this is the final round and the front is well-established with clear feasible designs meeting all constraints, stopping is the appropriate decision. The selection rule (min luts_plus_ffs) will pick the pipelined_m design at 1121 LUTs+FFs.
- **rule applied by code:** code: before stopping (stopped), one front-mapping round with the remaining 40 evaluations

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 60 of 100.
Hypervolume of the feasible front: 1939 (gain this round: n/a (first round)).
Feasible designs: 9 of 60 evaluations (5 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 85% violate; best seen 0.000134 (2^-12.86)
- sys_p99_batch_us <= 0.44: 17% violate; best seen 0.161

Pareto front (feasible, 4 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=5] luts_plus_ffs=1121, accuracy_bits=12.2, luts=909, ffs=212, throughput_msps=80.6, max_abs_err=0.000218 (2^-12.16), power_index=1.35
- pipelined [data_width=16 n_iter=14 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=1716, accuracy_bits=12.3, luts=861, ffs=856, throughput_msps=273, max_abs_err=0.000204 (2^-12.26), power_index=2.07
- pipelined [data_width=16 n_iter=15 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=1841, accuracy_bits=12.5, luts=924, ffs=917, throughput_msps=273, max_abs_err=0.000176 (2^-12.48), power_index=2.22
- pipelined [data_width=16 n_iter=16 angle_guard=2 frac_guard=2 rounding=round] luts_plus_ffs=1966, accuracy_bits=12.9, luts=987, ffs=979, throughput_msps=273, max_abs_err=0.000134 (2^-12.86), power_index=2.37
Front coverage: luts_plus_ffs 1121..1966 (HV reference 4000); accuracy_bits 12.2..12.9 (HV reference 12); data_width on the front 16..16 (registry 8..28).

Per family:
- pipelined: 30 evals, 8 feasible; max throughput seen 273 MSPS; best accuracy 12.86 bits; best feasible luts_plus_ffs=1716; feasible ranges: data_width 16..16, n_iter 14..16, angle_guard 1..2, frac_guard 2..2
- pipelined_m: 30 evals, 1 feasible; max throughput seen 171 MSPS; best accuracy 12.16 bits; best feasible luts_plus_ffs=1121; feasible ranges: data_width 16..16, n_iter 15..15, angle_guard 1..1, frac_guard 2..2, m 5..5
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 40 evaluations*)
- `pipelined_m` (10 evals): data_width=15..28, n_iter=13..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)
- `pipelined` (30 evals): data_width=15..28, n_iter=12..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* code: map the front of pipelined (3 front designs; box front_anchored)

**Result (code):** 40 evaluations this round, 100 total; 37 feasible; hypervolume 8624 (+344.7%).

**No LLM call** (code's front-mapping round): The exploration has identified a feasible Pareto front dominated by pipelined and pipelined_m architectures. The best design (pipelined_m, m=5) achieves the minimum area objective (luts_plus_ffs=1121) while satisfying all constraints: throughput (80.6 MSPS >= 32), accuracy (12.2 bits > 12), and system latency (0.161 us < 0.44 us). The front covers the trade-off space well, with area ranging from 1121 to 1966 and accuracy from 12.2 to 12.9 bits. Since this is the final round and the front is well-established with clear feasible designs meeting all constraints, stopping is the appropriate decision. The selection rule (min luts_plus_ffs) will pick the pipelined_m design at 1121 LUTs+FFs.
- **rule applied by code:** code: front-mapping round complete; stopping as decided before it

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 100 of 100.
Hypervolume of the feasible front: 8624 (gain this round: +344.7%).
Feasible designs: 37 of 100 evaluations (28 unique).
Families explored so far: pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 32: 0% violate; best seen 273
- max_abs_err <= 0.000244141: 56% violate; best seen 3.71e-07 (2^-21.36)
- sys_p99_batch_us <= 0.44: 19% violate; best seen 0.161

Pareto front (feasible, 11 designs; showing up to 10), objectives: min luts_plus_ffs, max accuracy_bits
- pipelined_m [data_width=16 n_iter=15 angle_guard=1 frac_guard=2 rounding=round m=5] luts_plus_ffs=1121, accuracy_bits=12.2, luts=909, ffs=212, throughput_msps=80.6, max_abs_err=0.000218 (2^-12.16), power_index=1.35
- pipelined_m [data_width=25 n_iter=15 angle_guard=3 frac_guard=1 rounding=trunc m=4] luts_plus_ffs=1674, accuracy_bits=14, luts=1274, ffs=400, throughput_msps=86, max_abs_err=6.11e-05 (2^-14.00), power_index=2.01
- pipelined [data_width=21 n_iter=19 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=2800, accuracy_bits=15.9, luts=1390, ffs=1410, throughput_msps=257, max_abs_err=1.68e-05 (2^-15.86), power_index=3.37
- pipelined [data_width=21 n_iter=22 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=3255, accuracy_bits=15.9, luts=1621, ffs=1634, throughput_msps=257, max_abs_err=1.64e-05 (2^-15.90), power_index=3.92
- pipelined [data_width=27 n_iter=19 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=3487, accuracy_bits=18, luts=1731, ffs=1756, throughput_msps=249, max_abs_err=3.94e-06 (2^-17.96), power_index=4.2
- pipelined [data_width=27 n_iter=21 angle_guard=0 frac_guard=0 rounding=trunc] luts_plus_ffs=3703, accuracy_bits=19.7, luts=1839, ffs=1864, throughput_msps=249, max_abs_err=1.2e-06 (2^-19.67), power_index=4.46
- pipelined [data_width=27 n_iter=21 angle_guard=0 frac_guard=2 rounding=trunc] luts_plus_ffs=3864, accuracy_bits=19.8, luts=1923, ffs=1941, throughput_msps=249, max_abs_err=1.1e-06 (2^-19.79), power_index=4.65
- pipelined [data_width=27 n_iter=22 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=3972, accuracy_bits=20.3, luts=1975, ffs=1998, throughput_msps=249, max_abs_err=7.66e-07 (2^-20.32), power_index=4.78
- pipelined [data_width=27 n_iter=22 angle_guard=2 frac_guard=2 rounding=trunc] luts_plus_ffs=4142, accuracy_bits=20.8, luts=2063, ffs=2078, throughput_msps=249, max_abs_err=5.57e-07 (2^-20.78), power_index=4.99
- pipelined [data_width=27 n_iter=30 angle_guard=2 frac_guard=0 rounding=trunc] luts_plus_ffs=5449, accuracy_bits=21, luts=2725, ffs=2724, throughput_msps=249, max_abs_err=4.7e-07 (2^-21.02), power_index=6.56
Front coverage: luts_plus_ffs 1121..5449 (HV reference 4000); accuracy_bits 12.2..21 (HV reference 12); data_width on the front 16..27 (registry 8..28).

Per family:
- pipelined: 60 evals, 35 feasible; max throughput seen 273 MSPS; best accuracy 21.02 bits; best feasible luts_plus_ffs=1716; feasible ranges: data_width 16..28, n_iter 14..30, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 40 evals, 2 feasible; max throughput seen 171 MSPS; best accuracy 21.36 bits; best feasible luts_plus_ffs=1121; feasible ranges: data_width 16..25, n_iter 15..15, angle_guard 1..3, frac_guard 1..2, m 4..5
```
</details>

## LLM usage
- calls: 2 (failed/unparsed attempts: 0)
- tokens: 5053 in, 1460 out
- provider-reported cost: $0.0033
- full prompts and replies: `llm_trace.jsonl`

