# Freelance Monthly Dashboard Guide

Clone of Quillenhart qaduu **Dashboard tab** — pick any month from a dropdown and see income, expenses, net profit, category breakdown, and tax set-aside in one view. This guide pairs with [datanestdigital's freelance pricing post](https://dev.to/datanestdigital/how-to-price-freelance-work-without-undercharging-3ma7): your rate only makes sense once the dashboard shows real net profit, not gross deposits.

## Why a monthly dashboard beats checking your bank balance

Bank balance is a lagging, blended number. It mixes last month's tax reserve with this month's client payment and next week's software renewal.

Quillenhart's [$15 Gumroad tracker](https://quillenhart.gumroad.com/l/qaduu) (**7 ratings**) solves this with a **Dashboard tab**: select a month → profit, bills context, savings, debt, invoices, and tax set-aside update together. Log transactions once on the master sheet; the dashboard is a view, not a second data entry job.

## The one-click month view

Every row in `transaction-log-template.csv` feeds the dashboard:

| Column | Role in dashboard |
|--------|-------------------|
| `date` | Determines which month bucket the row belongs to |
| `type` | `income` vs `expense` |
| `category` | Category breakdown chart for the selected month |
| `amount` | Signed amount — positive income, negative expense |
| `description` | Audit trail only; dashboard aggregates |

## Free CLI — select a month

```bash
python3 monthly_dashboard.py sample-transactions.csv "" "" "" "" "" "" 2026-01
```

Or set `FINANCE_MONTH=2026-01` before running with invoice/bills/debt/savings files attached.

Look for the `FREELANCE MONTHLY DASHBOARD (Quillenhart Dashboard tab shape)` block — income, expenses, net, top categories, and tax set-aside for that month only.

With full kit files:

```bash
python3 monthly_dashboard.py sample-transactions.csv invoices-sample.csv bills-sample.csv debt-sample.csv savings-sample.csv "" "" 2026-02
```

## Connect pricing to the dashboard

[datanestdigital's pricing guide](https://dev.to/datanestdigital/how-to-price-freelance-work-without-undercharging-3ma7) starts from the income and costs you need to cover — not what feels polite. The dashboard is where those numbers live after you bill clients:

1. Log each payment and expense when it clears.
2. Pick the month you want to review.
3. Read **net profit** — that is the number for rate math and tax set-aside, not gross deposits.

Pair with the [freelance rate calculator](calculators-guide.md) in the calculators hub when you are repricing.

## Who it's for

- Freelancers who price from gut feel and wonder why good months still feel tight
- Solopreneurs who want Quillenhart's Dashboard tab promise without a $30/mo bookkeeping subscription
- Anyone who already logs transactions but lacks a single-month summary view

Full EUR 9 kit: all nine Quillenhart tabs as CSV + Python modules — bills, debt, invoices, savings, annual summary, take-home, 1099-K, self-assessment, calculators.
