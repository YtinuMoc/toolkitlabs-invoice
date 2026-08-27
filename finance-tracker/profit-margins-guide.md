# Profit margins at a glance — categorized income & expense (Quillenhart qaduu clone)

Clone of [faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo) buyer channel + Quillenhart Gumroad **"Income & expense tracking, fully categorized"** and **"Auto-calculated net profit for any month you select"** ($15, 7 ratings).

## The problem faisalmq names

Without a clear view of profit margins, you make pricing decisions on guesswork. Are you actually profitable on that long-term project, or are overhead costs eating the margin? [faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo) sells three outcomes:

1. **Automated summaries** — profit margins at a glance
2. **Tax preparedness** — expenses categorized before filing season
3. **Centralized data** — one log, not emails + bank statements

Quillenhart's Transactions tab is the same promise: log once, categorized, net profit recalculates per month.

## Free preview

```bash
python3 monthly_dashboard.py sample-transactions.csv
```

Look for `PROFIT MARGINS AT A GLANCE` in stdout:

```
=== PROFIT MARGINS AT A GLANCE (faisalmq/3cpo + Quillenhart categorized tracking) ===
  Active month: 2026-02
    2026-01  income $5,000.00  expense $544.99  net $4,455.01  margin 89.1%
    2026-02  income $3,200.00  expense $50.00  net $3,150.00  margin 98.4% ← selected

  Categorized breakdown (2026-02) — tax preparedness:
    client_work: income $3,200.00  expense $0.00  net $3,200.00
    software: income $0.00  expense $50.00  net $-50.00
```

Switch months (Quillenhart dropdown equivalent):

```bash
FINANCE_MONTH=2026-01 python3 monthly_dashboard.py sample-transactions.csv
```

## Why Google Sheets / CSV beats enterprise software

[faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo): no accounting degree, no bloated subscription. Quillenhart: **shaded cells only** — you type in the log, margins calculate themselves.

## Paid kit

Full 9-tab system: [finance tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/finance-tracker/) · EUR 9 one-time · [Stripe checkout](https://buy.stripe.com/6oUeVe5KS6PO7Fc5FP5Ne0t?client_reference_id=profit-margins-guide)
