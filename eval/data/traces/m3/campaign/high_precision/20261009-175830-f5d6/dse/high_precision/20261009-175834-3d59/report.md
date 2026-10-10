# DSE run: high_precision

**Verdict:** converged: the architect stopped exploring.  
**Architect (LLM):** openrouter: deepseek/deepseek-v4.1-flash.  
**Evaluations:** 400 of 400 budgeted, over 4 round(s).  
**Spec intake:** provided as a validated Spec; confirmed before exploration.

> Provenance key. *exact*: bit-accurate golden model over the stated angle sweep, or the cycle schedule. *estimate*: analytical Artix-7 cost model calibrated to two Vivado anchor points (weak calibration; see the L5 refit in eval/data/). *measured*: real synthesis / place-and-route results, named by tool and version (back-annotation section). The LLM produced no numbers in this report; its plans and reasoning are quoted as text.

## Spec
```
spec high_precision: Coherent demodulator for a precision instrument: max error <= 2^-20 at >= 50 MSPS. Minimise area (LUTs + FFs) and the relative power index.
  constraint: throughput_msps >= 50
  constraint: max_abs_err <= 9.53674e-07
  objective: min luts_plus_ffs (HV ref 8000)
  objective: min power_index (HV ref 20)
  select: min luts_plus_ffs
  budget: 400 evals, 100/round, <= 4 rounds, eps 0.01
```

## Selected design
`pipelined_m:data_width=27,n_iter=22,angle_guard=-1,frac_guard=0,rounding=round,m=6` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 1908 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 406 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 59.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 59.9 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 100 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 4.35 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 9.53e-07 (2^-20.00) | exact: bit-accurate model, dense (131024 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 32 | exact: bit-accurate model, dense (131024 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.22e-07 (2^-22.10) | exact: bit-accurate model, dense (131024 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 7.45 | exact: bit-accurate model, dense (131024 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 20 | exact: bit-accurate model, dense (131024 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 144.6 dBc, SNR 130.3 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (1 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=27,n_iter=22,angle_guard=-1,frac_guard=0,rounding=round,m=6` | 1908 | 406 | 59.9 | 6 | 4.35 | 9.53e-07 (2^-20.00) | 20.00 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Accuracy is family-independent (data_width, n_iter, angle_guard, frac_guard, rounding), so the 2^-20 error budget forces high W and high N regardless of family; ranges are set wide enough (W 20..28, N 16..30, guards up to 4, both roundings) for the search to locate the accuracy boundary. The binding architectural constraint is throughput >= 50 MSPS. iterative is excluded outright: N+3 cycles/result would need >1 GHz Fmax. unrolled_k is borderline (needs ~300 MHz at k=8) and gets a small probe. The real trade-off lives in pipelined vs pipelined_m, both 1 result/cycle: pipelined_m with large m trades Fmax for far fewer FFs, and since only 50 MSPS is required there is likely a small-area large-m corner. Round 1 therefore spends 50% on pipelined_m (main trade-off), 30% on pipelined (fast anchor), 20% on unrolled_k (feasibility probe), all with identical accuracy ranges so the front is comparable across families.*)
- `pipelined_m` (50 evals): data_width=20..28, n_iter=16..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Only pipelined families give 1 result/cycle, so throughput = Fmax and the >=50 MSPS constraint is easy to satisfy. pipelined_m registers every m stages: large m cuts FF count (area) at the cost of Fmax. Since the spec only needs 50 MSPS, there is likely a large-m corner that is far smaller than fully pipelined while still meeting throughput. This is the most promising area/throughput trade-off, so it gets the largest share.
- `pipelined` (30 evals): data_width=20..28, n_iter=16..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Fully pipelined (m=1) is the high-Fmax / high-FF corner of the same trade-off curve. It anchors the fast end of the Pareto front and gives the accuracy-vs-area boundary at maximum throughput. Needed to keep the front well-spread even though it is unlikely to be the min-area winner.
- `unrolled_k` (20 evals): data_width=20..28, n_iter=16..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* Shared-datapath family, so LUTs/FFs could be much lower than pipelined if it can hit 50 MSPS. With N~20 and k=8 it needs ceil(N/k)+3 = 6 cycles/result, i.e. Fmax >= ~300 MHz, which is doubtful for 8 chained micro-rotations. A modest probe confirms feasibility or rules it out cheaply; if feasible it could dominate on area.

**Result (code):** 100 evaluations this round, 100 total; 47 feasible; hypervolume 8.093e+04 (n/a).

**LLM decision:** `map_front` — Round 1 leaves a degenerate front: exactly one feasible design (pipelined_m W=24 N=25 angle_guard=2 frac_guard=3 m=7, luts_plus_ffs=2626, power_index=4.94), so the front spans 0% of both objective ranges and HV=8.09e4 is only ~51% of the 160000 maximum — the whole trade-off curve is unmapped. The throughput constraint is nearly binding at this corner (52 vs 50 MSPS), so the min-area corner is pinned by throughput and we cannot tell from 50 sparse pipelined_m evals whether smaller feasible designs exist just outside the explored box. iterative and unrolled_k cannot reach 50 MSPS at all (unrolled_k max seen 9.36 MSPS, N+3 cycles/result), so adding them would waste budget. The correct move is to spend this round letting NSGA-II map the full registry ranges of the families that actually appear on the front — pipelined_m (and pipelined, whose feasible best is 4413) — seeded with the current point, to expose the real curve and any lower-area/lower-power feasible designs.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 8.093e+04 (gain this round: n/a (first round)).
Feasible designs: 47 of 100 evaluations (34 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 23% violate; best seen 257
- max_abs_err <= 9.53674e-07: 42% violate; best seen 6.11e-08 (2^-23.96)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=24 n_iter=25 angle_guard=2 frac_guard=3 rounding=round m=7] luts_plus_ffs=2626, power_index=4.94, luts=2231, ffs=395, throughput_msps=52, max_abs_err=6.35e-07 (2^-20.59)
Front coverage: luts_plus_ffs 2626..2626 (HV reference 8000); power_index 4.94..4.94 (HV reference 20); data_width on the front 24..24 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 9.36 MSPS; best accuracy 23.61 bits
- pipelined: 30 evals, 15 feasible; max throughput seen 257 MSPS; best accuracy 23.96 bits; best feasible luts_plus_ffs=4413; feasible ranges: data_width 24..28, n_iter 23..29, angle_guard -2..4, frac_guard 1..4
- pipelined_m: 50 evals, 32 feasible; max throughput seen 158 MSPS; best accuracy 23.60 bits; best feasible luts_plus_ffs=2626; feasible ranges: data_width 24..27, n_iter 22..30, angle_guard -1..4, frac_guard 0..4, m 2..7
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=23..28, n_iter=23..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 112 feasible; hypervolume 8.519e+04 (+5.3%).

**LLM decision:** `map_front` — The feasible Pareto front contains only a single design (pipelined_m, luts_plus_ffs=2459, power_index=4.62), so it covers essentially none of either objective's range (2459..2459 vs ref 8000; 4.62..4.62 vs ref 20) and the reported HV of 8.519e4 is just that one corner. With 200 evals left and 112/200 feasible designs already found, the priority is to map the whole trade-off curve rather than refine a single point. The unexplored family iterative is very unlikely to help: it issues 1 micro-rotation/cycle (N+3 cycles/result), and even the faster unrolled_k family topped out at 9.36 MSPS with 0 feasible designs, so iterative cannot reach the 50 MSPS constraint. pipelined (15 feasible, up to 257 MSPS) and pipelined_m (97 feasible, best area 2459) are the families that actually populate the front, so the coverage search should span their full ranges.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 8.519e+04 (gain this round: +5.3%).
Feasible designs: 112 of 200 evaluations (96 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 18% violate; best seen 257
- max_abs_err <= 9.53674e-07: 34% violate; best seen 6.11e-08 (2^-23.96)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=27 n_iter=23 angle_guard=1 frac_guard=0 rounding=trunc m=6] luts_plus_ffs=2459, power_index=4.62, luts=2045, ffs=414, throughput_msps=59.9, max_abs_err=5.21e-07 (2^-20.87)
Front coverage: luts_plus_ffs 2459..2459 (HV reference 8000); power_index 4.62..4.62 (HV reference 20); data_width on the front 27..27 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 9.36 MSPS; best accuracy 23.61 bits
- pipelined: 30 evals, 15 feasible; max throughput seen 257 MSPS; best accuracy 23.96 bits; best feasible luts_plus_ffs=4413; feasible ranges: data_width 24..28, n_iter 23..29, angle_guard -2..4, frac_guard 1..4
- pipelined_m: 150 evals, 97 feasible; max throughput seen 158 MSPS; best accuracy 23.68 bits; best feasible luts_plus_ffs=2459; feasible ranges: data_width 24..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=26..28, n_iter=21..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 300 total; 190 feasible; hypervolume 8.898e+04 (+4.4%).

**LLM decision:** `map_front` — The feasible front holds a single design (pipelined_m, luts_plus_ffs=2314, power_index=4.35), so coverage is minimal: luts_plus_ffs 2314..2314 against an HV reference of 8000 and power_index 4.35..4.35 against 20 — the trade-off curve is essentially unmapped. Both pipelined (15/30 feasible, best luts_plus_ffs=4413, up to 257 MSPS) and pipelined_m (175/250 feasible, best accuracy 24.64 bits) are viable and sit on/near the front, so the remaining 100 evaluations are best spent on a code-driven NSGA-II coverage search over their full ranges seeded with the current front. unrolled_k is excluded (0/20 feasible, max throughput 9.36 MSPS < 50) and iterative is structurally slower still (N+3 cycles/result), so neither can satisfy the 50 MSPS constraint; no new family is worth adding.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 8.898e+04 (gain this round: +4.4%).
Feasible designs: 190 of 300 evaluations (166 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 16% violate; best seen 257
- max_abs_err <= 9.53674e-07: 26% violate; best seen 3.83e-08 (2^-24.64)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=27 n_iter=22 angle_guard=-1 frac_guard=0 rounding=round m=6] luts_plus_ffs=2314, power_index=4.35, luts=1908, ffs=406, throughput_msps=59.9, max_abs_err=9.53e-07 (2^-20.00)
Front coverage: luts_plus_ffs 2314..2314 (HV reference 8000); power_index 4.35..4.35 (HV reference 20); data_width on the front 27..27 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 9.36 MSPS; best accuracy 23.61 bits
- pipelined: 30 evals, 15 feasible; max throughput seen 257 MSPS; best accuracy 23.96 bits; best feasible luts_plus_ffs=4413; feasible ranges: data_width 24..28, n_iter 23..29, angle_guard -2..4, frac_guard 1..4
- pipelined_m: 250 evals, 175 feasible; max throughput seen 158 MSPS; best accuracy 24.64 bits; best feasible luts_plus_ffs=2314; feasible ranges: data_width 24..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=26..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 265 feasible; hypervolume 8.898e+04 (+0.0%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), so no further exploration is possible. The spec is satisfiable: the feasible front contains pipelined_m [W=27, N=22, angle_guard=-1, frac_guard=0, round, m=6] with throughput 59.9 MSPS (>= 50) and max_abs_err 9.53e-07 (<= 9.53674e-07), i.e. it meets both constraints, so `infeasible` is not warranted. Hypervolume was flat this round (+0.0%, 8.898e+04), and the front is a single point at luts_plus_ffs=2314 / power_index=4.35, which is also exactly what the selection rule (min luts_plus_ffs) picks. The unexplored `iterative` family is not a loss here: it yields one result per N+3 cycles, and the only family that reached the 50 MSPS constraint at low area was pipelined_m (unrolled_k saw max 9.36 MSPS, 0 feasible). With no budget left to map the front further, stopping is the correct terminal decision.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 8.898e+04 (gain this round: +0.0%).
Feasible designs: 265 of 400 evaluations (226 unique).
Families explored so far: unrolled_k, pipelined, pipelined_m. Not yet explored: iterative.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 14% violate; best seen 257
- max_abs_err <= 9.53674e-07: 24% violate; best seen 3.83e-08 (2^-24.64)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=27 n_iter=22 angle_guard=-1 frac_guard=0 rounding=round m=6] luts_plus_ffs=2314, power_index=4.35, luts=1908, ffs=406, throughput_msps=59.9, max_abs_err=9.53e-07 (2^-20.00)
Front coverage: luts_plus_ffs 2314..2314 (HV reference 8000); power_index 4.35..4.35 (HV reference 20); data_width on the front 27..27 (registry 8..28).

Per family:
- unrolled_k: 20 evals, 0 feasible; max throughput seen 9.36 MSPS; best accuracy 23.61 bits
- pipelined: 30 evals, 15 feasible; max throughput seen 257 MSPS; best accuracy 23.96 bits; best feasible luts_plus_ffs=4413; feasible ranges: data_width 24..28, n_iter 23..29, angle_guard -2..4, frac_guard 1..4
- pipelined_m: 350 evals, 250 feasible; max throughput seen 158 MSPS; best accuracy 24.64 bits; best feasible luts_plus_ffs=2314; feasible ranges: data_width 24..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 25274 in, 16381 out
- provider-reported cost: $0.0188
- full prompts and replies: `llm_trace.jsonl`

