# Beginner-friendly finance — no spreadsheet formulas (By the Loop clone)

Clone of [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os). Buyer-channel shape: [faisalmq/2fj6](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-2fj6): end-of-month dread → clarity without an accounting degree → paid bundle upsell.

## The faisalmq/2fj6 promise

[faisalmq/2fj6](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-2fj6) names three outcomes freelancers actually want:

1. **Track income and expenses in one place** — no hunting email for invoice history
2. **Visualize take-home pay** — net after business costs, not gross deposits
3. **Prepare for tax season** — organized data so filing isn't a month-long headache

By the Loop's bundle adds four tools behind the same rule: **you only type into the log cells**. Everything else calculates itself.

## Shaded cells in this kit

| You type (shaded) | Auto-calculated |
|-------------------|-----------------|
| `invoice-log-template.csv` rows | Collected vs awaiting vs overdue |
| `expense-log-template.csv` rows | Category totals, net profit |
| Rate calculator HTML inputs | Minimum hourly floor |
| | 25% tax buffer + safe-to-spend |
| | Quarterly 1040-ES deadlines |

No `SUMIFS`. No pivot tables. Run the CLI after you log.

## Free preview

```bash
python3 freelance_finance_os.py invoice-log-sample.csv expense-log-sample.csv
```

Look for `BEGINNER-FRIENDLY` in stdout:

```plaintext
=== BEGINNER-FRIENDLY (faisalmq/2fj6 — no formulas required) ===
  You only type into shaded cells. In this kit that's your CSV rows.
  Type here:     invoice + expense CSV columns (see templates)
  Auto-calculated: collected, net profit, tax buffer, safe-to-spend, quarterly
  Invoice log: 6 rows · Expense log: 8 rows (expandable — duplicate templates)
```

## Who it's for

- Freelancers who've never touched a spreadsheet formula
- Creators who want bookkeeping to get out of the way
- Anyone replacing "hope my bank balance looks healthy" with a five-minute weekly log

## Pair with

- [invoice-panic-guide.md](invoice-panic-guide.md) — faisalmq/43dl invoice clarity
- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend
- [start-here.md](start-here.md) — four-tool bundle setup

Full bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) — invoice tracker + expense/tax buffer + rate calculator + quarterly estimator.
