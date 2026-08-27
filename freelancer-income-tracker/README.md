# Freelancer Income Tracker — PattyBun dcklyf clone

Shameless clone of [PattyBun's Freelancer Income Tracker ($14.99)](https://pattybun.gumroad.com/l/dcklyf) on Gumroad.

## What's inside (7 modules)

1. **Live Profit Dashboard** — real take-home after federal, state, and SE tax
2. **Quarterly Tax Estimator** — Q1–Q4 set-aside amounts
3. **Income & Expense Logs** — IRS Schedule C categories
4. **Mileage Tracker** — IRS standard rate deduction
5. **Client & Invoice Tracker** — overdue invoices flagged
6. **Monthly Breakdown** — 12-month profit view
7. **Plain-Language Tax Reference** — built-in explanations

## Quick start

```bash
python3 freelancer_dashboard.py income-sample.csv expense-sample.csv mileage-sample.csv invoice-sample.csv
```

Copy `income-log-template.csv` and log every payment. Add expenses, mileage, and invoices as separate CSVs.

## Settings

Edit rates at top of `freelancer_dashboard.py`:

- `FEDERAL_RATE` — default 22%
- `STATE_RATE` — default 5%
- `SE_TAX_RATE` — 15.3%
- `IRS_MILEAGE_RATE` — $0.67/mi

## Disclaimer

Planning tool, not tax software. Consult a CPA for filing.
