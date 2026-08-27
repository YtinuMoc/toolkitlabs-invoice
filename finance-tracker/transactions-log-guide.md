# Transactions log — single source of truth

Clone of Quillenhart qaduu **Transactions tab** + [orion_operator/40gi](https://dev.to/orion_operator/the-solo-gumroad-sellers-guide-to-tracking-income-expenses-quarterly-taxes-with-a-google-sheet-40gi) single-source-of-truth shape.

One row per money event. Every dashboard tab pulls from this log — you never re-type totals.

## Columns (CSV)

| Column | Example | Notes |
|--------|---------|-------|
| `date` | 2026-01-15 | When money moved |
| `type` | income / expense | income or expense |
| `category` | client_work | Consistent dropdown |
| `description` | Invoice #101 | Human-readable |
| `amount` | 2500.00 | Positive income, negative expense |

## Category tags (starter set)

- Income: `client_work`, `product_sales`, `other_income`
- Expenses: `software`, `marketing`, `contractor`, `platform_fee`, `home_office`, `equipment`
- Fees: `platform_fee`, `fulfillment`, `creator_commission`, `ad_spend`

## Workflow

1. Copy [transaction-log-template.csv](transaction-log-template.csv) → `my-transactions.csv`
2. Log every sale, fee, refund, and expense as one row
3. Run: `python3 monthly_dashboard.py my-transactions.csv`
4. Dashboard, annual summary, tax set-aside, and category breakdown all derive from this file

## Quillenhart promise

> Log everything once on the Transactions tab, and the rest handles itself.

Our CLI mirrors that: shaded cells = CSV rows you type. Everything else calculates.

## Free samples

- [sample-transactions.csv](sample-transactions.csv) — multi-month example
- [free-preview.md](free-preview.md) — one-month P&L walkthrough
