# Cash runway forecast — which month you run dry

Clone of [agentchip/33mm](https://dev.to/agentchip/your-spreadsheet-cant-tell-you-the-month-youll-run-out-of-cash-this-can-33mm) buyer channel + Quillenhart **Dashboard tab** forward view.

## The blind spot

Your P&L is a rearview mirror. The question that keeps freelancers alive is forward-looking:

> Given planned income, recurring bills, and debt minimums — **which month does cash go negative?**

## What this module does

`monthly_dashboard.py` prints a **12-month cash runway forecast** from your transaction log:

1. **Rolling forecast** — opening balance, income, expenses, net, closing balance per month
2. **Cash-gap alarm** — flags the lowest-balance month; warns if balance goes negative
3. **Three scenarios** — optimistic (income ×1.2), base, pessimistic (×0.8)

## Quick start

```bash
python3 monthly_dashboard.py sample-transactions.csv invoices-sample.csv bills-sample.csv debt-sample.csv
```

Look for the `CASH RUNWAY FORECAST` block in stdout.

## Inputs

| File | Role |
|------|------|
| `sample-transactions.csv` | Historical income/expense by month |
| `bills-sample.csv` | Recurring monthly obligations |
| `debt-sample.csv` | Minimum debt payments |

Set starting cash in `FINANCE_STARTING_CASH` env var (default: $3,000).

## When to run it

- **Monthly** — after updating your transaction log
- **Before hiring** — see what a new $2,000/mo cost does to the curve
- **Before a slow season** — pessimistic scenario shows the danger month early

## Full kit

Quillenhart's 9-tab finance tracker is [$15 on Gumroad](https://quillenhart.gumroad.com/l/qaduu). Our clone: EUR 9 one-time at https://ytinumoc.github.io/toolkitlabs-invoice/finance-tracker/
