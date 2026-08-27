# Year-to-date totals — always current

Clone of Quillenhart qaduu Gumroad promise: *"Year-to-date totals, always current."*

Log transactions as they happen (or import monthly). YTD income, expenses, net profit, and tax set-aside update every time you run the dashboard — no December scramble.

## What updates automatically

| Metric | Source |
|--------|--------|
| YTD income | Sum of all income rows in transaction log |
| YTD expenses | Sum of all expense rows |
| YTD net profit | Income − expenses |
| YTD tax set-aside | Net × your set-aside % (default 25%) |
| Monthly trend | Each month in the log |

## Run it

```bash
python3 monthly_dashboard.py sample-transactions.csv
```

Look for the `YEAR-TO-DATE TOTALS` block in stdout.

## Orion / Quillenhart shape

[orion/40gi](https://dev.to/orion_operator/the-solo-gumroad-sellers-guide-to-tracking-income-expenses-quarterly-taxes-with-a-google-sheet-40gi) uses a P&L Dashboard tab that never gets typed into — it pulls from Transactions. Our CLI mirrors that: type rows once, YTD recalculates on every run.

## Habit

- **Weekly:** log new sales, fees, and expenses
- **Monthly:** reconcile against bank statement, run dashboard for one month (`FINANCE_MONTH=2026-01`)
- **Quarterly:** transfer set-aside to tax-only account using YTD set-aside target

Planning only — confirm rates with a qualified tax professional.
