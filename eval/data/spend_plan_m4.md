# Milestone 4 spend plan (written before any M4 LLM call)

Cap: **$5.00** for the whole milestone, pilots included. Key usage at the start of the
session: **$7.8163** (limit $15, $7.1837 remaining, read 2026-10-10T16:23:17Z from
`GET /api/v1/key`; `eval/data/key_usage_m4.json`). The remaining headroom is above $5,
so the plan is sized to the $5 cap. The ledger (`eval/data/spend_ledger.jsonl`,
`milestone: m4`) is checked before every run: a run is refused when the M4 total plus
twice the expected cost of the next run would pass the cap.

Per-run costs assumed from the committed ledger (provider-reported means):
structured graph, Qwen3.8-27B reasoning off **$0.008** (M3), DeepSeek V4.1 Flash
**$0.014** (M3), Sonnet 5.5 **$0.096** (M3 system specs; $0.064 on the M2 specs). A
fleet run is up to four member graphs (two members x two phases) with smaller budgets;
assumed **2.5x** a structured run until the pilot measures it.

| step | runs | assumed / run | assumed total |
|---|---|---|---|
| pilot: Qwen structured, `asic_multiaxis_control` seed 0 | 1 | $0.009 | $0.01 |
| pilot: Qwen fleet, `asic_multiaxis_control` seed 0 | 1 | $0.020 | $0.02 |
| ASIC specs, structured graph: Qwen, DeepSeek, Sonnet x 3 specs x 5 seeds | 45 | $0.008 / $0.014 / $0.096 | $1.77 |
| A/B single arm on the two FPGA specs (`low_area_control`, `multiaxis_control`): Qwen, DeepSeek x 5 seeds | 20 | $0.008 / $0.014 | $0.22 |
| A/B fleet arm, 5 specs (3 ASIC + 2 FPGA) x 5 seeds: Qwen, DeepSeek | 50 | $0.020 / $0.035 | $1.38 |
| **planned total** | 117 | | **$3.40** |

The A/B's single arm on the ASIC specs *is* the ASIC structured eval (same graph, same
budget, same seeds, run in the same session), so it is not paid for twice.

**Cut, by the rule "models before seeds":** the fleet arm for Sonnet 5.5 (25 runs at an
assumed ~$0.24 = ~$6, more than the cap on its own). If the headroom after the DeepSeek
fleet arm exceeds $1.3, the Sonnet fleet arm runs on `asic_multiaxis_control` only
(5 seeds), and the report says so; otherwise it is reported missing.

**Wall-clock**: every live run is started only after the previous one has finished, with
no baseline, ground-truth or test job running alongside, so each run's wall-clock is
measured alone. A fleet's own members run in parallel threads inside that run (that is
what the fleet is).

Order: pilots (cheapest model first) → Qwen (ASIC structured, single FPGA, fleet) →
DeepSeek (same) → Sonnet (ASIC structured) → optional Sonnet fleet subset.
