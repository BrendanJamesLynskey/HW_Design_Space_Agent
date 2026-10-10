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
`pipelined_m:data_width=26,n_iter=22,angle_guard=4,frac_guard=0,rounding=round,m=7` — selection: auto (spec rule: min luts_plus_ffs)

| metric | value | provenance |
|---|---|---|
| luts | 1953 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| ffs | 412 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| fmax_mhz | 52 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| throughput_msps | 52 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| latency_cycles | 6 | exact: schedule |
| latency_ns | 115 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| power_index | 4.45 | estimate: cost_fpga (artix7-xc7a35t-vivado2025.2-2anchor-v1, 2 anchors) |
| max_abs_err | 6.47e-07 (2^-20.56) | exact: bit-accurate model, dense (130961 angles: 65536 strided + 65536 random, seed 20260401+W) |
| max_abs_err_lsb | 10.9 | exact: bit-accurate model, dense (130961 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err | 2.08e-07 (2^-22.20) | exact: bit-accurate model, dense (130961 angles: 65536 strided + 65536 random, seed 20260401+W) |
| rms_err_lsb | 3.49 | exact: bit-accurate model, dense (130961 angles: 65536 strided + 65536 random, seed 20260401+W) |
| accuracy_bits | 20.6 | exact: bit-accurate model, dense (130961 angles: 65536 strided + 65536 random, seed 20260401+W) |

## L2: cycle-level contract and system simulation

Interface contract of the L1 selection (cycle model, checked against the RTL cycle for cycle): latency 6 cycles, a new input every 1 cycle(s). DDS tone from its exact outputs: SFDR 141.8 dBc, SNR 130.7 dB (*simulated (hw_dse.l2.dds l2-v1: golden-model DDS, 32-bit phase accumulator, coherent 16384-point FFT, tone bin 1297)*).

No system scenario in this spec: the spec has no system scenario: nothing to re-select.

## Pareto front (1 feasible non-dominated designs)

Columns marked † are *estimates* (cost model); ‡ are *exact* (golden model / schedule).

| # | design | LUTs † | FFs † | MSPS † | latency cyc ‡ | power idx † | max err ‡ | acc. bits ‡ |
|---|---|---|---|---|---|---|---|---|
| 0 | `pipelined_m:data_width=26,n_iter=22,angle_guard=4,frac_guard=0,rounding=round,m=7` | 1953 | 412 | 52.0 | 6 | 4.45 | 6.47e-07 (2^-20.56) | 20.56 |

![Pareto plot](pareto.png)

## Rounds: what the architect proposed, saw and decided
### Round 1

**Plan explored** (LLM rationale: *Accuracy is the binding constraint: max_abs_err <= 2^-20 needs ~20+ bits, driven jointly by data_width (truncation/rounding ~2^-W) and n_iter (angle quantisation ~2^-N). So every family is searched at data_width 22..28 and n_iter 20..30, with angle_guard/frac_guard spanning their full ranges and both rounding modes, so the search can find the cheapest parameter set that just crosses the error bar rather than over-provisioning. Throughput >= 50 MSPS is a floor, not a target: only the 1-result/cycle families (pipelined, pipelined_m) can realistically reach it at high n_iter, so they take 75% of the budget and are where the min-luts_plus_ffs / min-power_index trade-off actually lives. pipelined_m is weighted highest because registering every m stages is the direct lever on pipeline FF count (the dominant area cost at large n_iter) and the 50 MSPS bar is low enough that large m should remain feasible. unrolled_k and iterative get smaller shares purely to test whether they can clear the throughput bar at high N; if they cannot, the front collapses onto the two pipelined families and later rounds concentrate there. Round 1 spends the full 100 evals with these shares; subsequent rounds re-weight toward whichever pipelined variant produces the feasible low-area corner and densify the area/power front.*)
- `pipelined_m` (40 evals): data_width=22..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* Best candidate for the min-luts_plus_ffs corner: 1 result/cycle so throughput = Fmax easily clears 50 MSPS, while registering only every m stages cuts pipeline FFs (the dominant area term at high n_iter) versus full pipelining. Large m trades Fmax for area, and the 50 MSPS bar is low, so the area-optimal feasible point likely lives here. m range 2..8 spans the whole register-density trade-off.
- `pipelined` (35 evals): data_width=22..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Full per-stage pipelining: highest Fmax and shortest latency, so it anchors the high-throughput / low-power-index end of the front and guarantees the 50 MSPS constraint is met. Its higher FF count makes it the area-expensive reference against which pipelined_m's savings are measured; needed for dense front coverage.
- `unrolled_k` (15 evals): data_width=22..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, k=2..8. *Why:* Shares one datapath across k micro-rotations/cycle, so it could undercut pipelined area if it can still hit 50 MSPS. At the n_iter>=20 needed for 2^-20 accuracy it needs ~ceil(N/k)+3 cycles, i.e. a high Fmax; this family is the main feasibility question mark, so a modest share probes whether any (k, N) combination clears the throughput bar while staying small.
- `iterative` (10 evals): data_width=22..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round. *Why:* Smallest datapath (shared barrel shifters) so it would win on area if feasible, but N+3 cycles/result at N>=20 demands >1 GHz to reach 50 MSPS, which is implausible on Artix-7. A small share confirms/refutes infeasibility so the front is not left with an untested family, without wasting budget that belongs on the pipelined variants.

**Result (code):** 100 evaluations this round, 100 total; 56 feasible; hypervolume 8.766e+04 (n/a).

**LLM decision:** `map_front` — Round 1 left the feasible front as a single point: pipelined_m [W=26, N=22, angle_guard=4, frac_guard=0, round, m=7] at luts_plus_ffs=2364 and power_index=4.45. Against the HV reference (8000, 20) that is coverage of 2364..2364 and 4.45..4.45, i.e. essentially 0% of both objective ranges — the classic trigger for map_front. It is not for lack of feasible material: 56/100 evals were feasible (39 unique) across pipelined and pipelined_m, yet only 1 of those is non-dominated, so the front is badly under-sampled while the HV headroom (up to 8000 area / 20 power) is enormous. The constraint evidence also tells us which families can even be on the front: iterative (max 6.66 MSPS) and unrolled_k (max 6.54 MSPS) cannot reach the 50 MSPS floor, whereas both pipelined families do (257 and 114 MSPS), and pipelined_m's feasible box is still wide (W 25..28, N 22..27, m 3..7). Notably the only front design sits right on the throughput edge (52 vs 50 MSPS, m=7 already at the top of the feasible m range), which suggests other non-dominated corners (e.g. lower data_width with more iterations, or other m/k splits) are unexplored rather than absent. A broad NSGA-II pass over the full ranges of the front's families, seeded with the current point, is therefore the best way to recover the rest of the trade-off curve before spending later rounds refining; narrow refining around the single point now risks entrenching a possibly-local corner.

<details><summary>Summary the LLM was shown</summary>

```
Round 1 of at most 4 complete. Evaluations used: 100 of 400.
Hypervolume of the feasible front: 8.766e+04 (gain this round: n/a (first round)).
Feasible designs: 56 of 100 evaluations (39 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 28% violate; best seen 257
- max_abs_err <= 9.53674e-07: 30% violate; best seen 2.3e-08 (2^-25.37)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=26 n_iter=22 angle_guard=4 frac_guard=0 rounding=round m=7] luts_plus_ffs=2364, power_index=4.45, luts=1953, ffs=412, throughput_msps=52, max_abs_err=6.47e-07 (2^-20.56)
Front coverage: luts_plus_ffs 2364..2364 (HV reference 8000); power_index 4.45..4.45 (HV reference 20); data_width on the front 26..26 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 6.66 MSPS; best accuracy 25.37 bits
- unrolled_k: 15 evals, 0 feasible; max throughput seen 6.54 MSPS; best accuracy 23.61 bits
- pipelined: 35 evals, 27 feasible; max throughput seen 257 MSPS; best accuracy 24.55 bits; best feasible luts_plus_ffs=3970; feasible ranges: data_width 24..28, n_iter 22..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 40 evals, 29 feasible; max throughput seen 114 MSPS; best accuracy 24.63 bits; best feasible luts_plus_ffs=2364; feasible ranges: data_width 25..28, n_iter 22..27, angle_guard -1..4, frac_guard 0..3, m 3..7
```
</details>

### Round 2

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=25..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 200 total; 133 feasible; hypervolume 8.766e+04 (+0.0%).

**LLM decision:** `map_front` — Only one feasible Pareto design exists (pipelined_m, luts_plus_ffs=2364, power_index=4.45) and hypervolume gain this round was +0.0%, so the front is essentially a single point rather than a curve. The feasible region is clearly established: only pipelined and pipelined_m reach >=50 MSPS (iterative/unrolled_k max ~6.6 MSPS, 0 feasible), and pipelined_m dominates on area (best 2364 vs pipelined's 3970). Feasible ranges are wide (data_width 25..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7) yet only one point landed on the front, so the trade-off curve between area and power is badly under-sampled. A code-driven NSGA-II coverage search over the full ranges of pipelined and pipelined_m, seeded with the current front, is the right use of the remaining budget to map the whole curve before the final selection.

<details><summary>Summary the LLM was shown</summary>

```
Round 2 of at most 4 complete. Evaluations used: 200 of 400.
Hypervolume of the feasible front: 8.766e+04 (gain this round: +0.0%).
Feasible designs: 133 of 200 evaluations (106 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 16% violate; best seen 257
- max_abs_err <= 9.53674e-07: 25% violate; best seen 2.3e-08 (2^-25.37)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=26 n_iter=22 angle_guard=4 frac_guard=0 rounding=round m=7] luts_plus_ffs=2364, power_index=4.45, luts=1953, ffs=412, throughput_msps=52, max_abs_err=6.47e-07 (2^-20.56)
Front coverage: luts_plus_ffs 2364..2364 (HV reference 8000); power_index 4.45..4.45 (HV reference 20); data_width on the front 26..26 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 6.66 MSPS; best accuracy 25.37 bits
- unrolled_k: 15 evals, 0 feasible; max throughput seen 6.54 MSPS; best accuracy 23.61 bits
- pipelined: 35 evals, 27 feasible; max throughput seen 257 MSPS; best accuracy 24.55 bits; best feasible luts_plus_ffs=3970; feasible ranges: data_width 24..28, n_iter 22..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 140 evals, 106 feasible; max throughput seen 153 MSPS; best accuracy 25.08 bits; best feasible luts_plus_ffs=2364; feasible ranges: data_width 25..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

### Round 3

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=25..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 300 total; 203 feasible; hypervolume 8.766e+04 (+0.0%).

**LLM decision:** `map_front` — The feasible front has collapsed to a single design (pipelined_m, luts_plus_ffs=2364, power_index=4.45) despite 203 feasible evaluations, so hypervolume gain is +0.0% and the front covers only a point of each objective's range (luts_plus_ffs 2364..2364 vs HV ref 8000; power_index 4.45..4.45 vs ref 20). The throughput constraint (>=50 MSPS) is the binding one: iterative and unrolled_k never exceed ~6.6 MSPS and are structurally infeasible, while pipelined (best area 3970) and pipelined_m (best 2364) both clear 50 MSPS. With 100 evals left and a reserved coverage budget, the right move is to let code run NSGA-II over the full ranges of the two feasible families (pipelined, pipelined_m) seeded with the current front, to spread the trade-off curve across area and power instead of a single point.

<details><summary>Summary the LLM was shown</summary>

```
Round 3 of at most 4 complete. Evaluations used: 300 of 400.
Hypervolume of the feasible front: 8.766e+04 (gain this round: +0.0%).
Feasible designs: 203 of 300 evaluations (172 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 14% violate; best seen 257
- max_abs_err <= 9.53674e-07: 23% violate; best seen 2.3e-08 (2^-25.37)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=26 n_iter=22 angle_guard=4 frac_guard=0 rounding=round m=7] luts_plus_ffs=2364, power_index=4.45, luts=1953, ffs=412, throughput_msps=52, max_abs_err=6.47e-07 (2^-20.56)
Front coverage: luts_plus_ffs 2364..2364 (HV reference 8000); power_index 4.45..4.45 (HV reference 20); data_width on the front 26..26 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 6.66 MSPS; best accuracy 25.37 bits
- unrolled_k: 15 evals, 0 feasible; max throughput seen 6.54 MSPS; best accuracy 23.61 bits
- pipelined: 35 evals, 27 feasible; max throughput seen 257 MSPS; best accuracy 24.55 bits; best feasible luts_plus_ffs=3970; feasible ranges: data_width 24..28, n_iter 22..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 240 evals, 176 feasible; max throughput seen 158 MSPS; best accuracy 25.08 bits; best feasible luts_plus_ffs=2364; feasible ranges: data_width 25..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

### Round 4

**Plan explored** (LLM rationale: *code-driven front-mapping round: NSGA-II over the front families' front_anchored ranges with 100 evaluations*)
- `pipelined_m` (100 evals): data_width=25..28, n_iter=20..30, angle_guard=-2..4, frac_guard=0..4, rounding=trunc|round, m=2..8. *Why:* code: map the front of pipelined_m (1 front designs; box front_anchored)

**Result (code):** 100 evaluations this round, 400 total; 271 feasible; hypervolume 8.766e+04 (+0.0%).

**LLM decision:** `stop` — Budget and round cap are both exhausted (400/400 evals, round 4 of 4), and this round produced +0.0% hypervolume gain, so further search is not warranted. The spec is satisfiable: 271 of 400 evaluations were feasible, and the Pareto front contains a valid design — pipelined_m [data_width=26, n_iter=22, angle_guard=4, frac_guard=0, rounding=round, m=7] with luts_plus_ffs=2364, power_index=4.45, throughput_msps=52 (>= 50) and max_abs_err=6.47e-07 (2^-20.56, <= 2^-20). Both constraints are met, so `infeasible` is not appropriate. The front is a single point, but it is the minimum-area feasible design (2364 vs the next-best family's 3970 for pipelined), and it is the design the selection rule (min luts_plus_ffs) would pick; the remaining objective ranges are already well inside the HV reference points (2364 vs 8000, 4.45 vs 20). Note the throughput margin is thin (52 vs 50 MSPS) and the accuracy margin is ~0.56 bits, both from cost-model/bit-exact estimates, so this is the converged answer under the given model.

<details><summary>Summary the LLM was shown</summary>

```
Round 4 of at most 4 complete. Evaluations used: 400 of 400.
Hypervolume of the feasible front: 8.766e+04 (gain this round: +0.0%).
Feasible designs: 271 of 400 evaluations (229 unique).
Families explored so far: iterative, unrolled_k, pipelined, pipelined_m. Not yet explored: none.
Provenance: LUTs/FFs/Fmax/throughput/power are cost-model ESTIMATES (Artix-7, 2-anchor calibration); errors/accuracy bits are EXACT (bit-accurate model).

Constraints (fraction of evaluations violating; best value any design achieved):
- throughput_msps >= 50: 14% violate; best seen 257
- max_abs_err <= 9.53674e-07: 22% violate; best seen 2.3e-08 (2^-25.37)

Pareto front (feasible, 1 designs; showing up to 10), objectives: min luts_plus_ffs, min power_index
- pipelined_m [data_width=26 n_iter=22 angle_guard=4 frac_guard=0 rounding=round m=7] luts_plus_ffs=2364, power_index=4.45, luts=1953, ffs=412, throughput_msps=52, max_abs_err=6.47e-07 (2^-20.56)
Front coverage: luts_plus_ffs 2364..2364 (HV reference 8000); power_index 4.45..4.45 (HV reference 20); data_width on the front 26..26 (registry 8..28).

Per family:
- iterative: 10 evals, 0 feasible; max throughput seen 6.66 MSPS; best accuracy 25.37 bits
- unrolled_k: 15 evals, 0 feasible; max throughput seen 6.54 MSPS; best accuracy 23.61 bits
- pipelined: 35 evals, 27 feasible; max throughput seen 257 MSPS; best accuracy 24.55 bits; best feasible luts_plus_ffs=3970; feasible ranges: data_width 24..28, n_iter 22..29, angle_guard -2..4, frac_guard 0..4
- pipelined_m: 340 evals, 244 feasible; max throughput seen 158 MSPS; best accuracy 25.08 bits; best feasible luts_plus_ffs=2364; feasible ranges: data_width 25..28, n_iter 22..30, angle_guard -2..4, frac_guard 0..4, m 2..7
```
</details>

## LLM usage
- calls: 8 (failed/unparsed attempts: 0)
- tokens: 25506 in, 12394 out
- provider-reported cost: $0.0135
- full prompts and replies: `llm_trace.jsonl`

