# Debt Payment Tracker Guide

Clone of Quillenhart qaduu **debt tab** + the buyer-channel shape from [crazychief's debt spreadsheet post](https://dev.to/crazychief/the-spreadsheet-that-eliminated-debt-in-five-months-and-what-it-taught-me-about-system-design-jg5): label, balance, minimum — no fancy payoff optimizer until the habit runs.

## The habit, not the dashboard

The spreadsheet had three columns: label, amount, balance. SUM formulas. No macros.

The system worked because income arrived → fixed allocation ran → debt balance shrank month by month. The tool tracked what was already happening — it did not ask for daily attention.

## Minimum columns

| Creditor | Original | Current balance | Min payment | Due day | APR |
|----------|----------|-----------------|-------------|---------|-----|
| Business card | $2,400 | $1,850 | $75 | 15 | 22.9% |
| Equipment loan | $5,000 | $3,200 | $210 | 1 | 8.5% |

Update **current balance** after each payment. Run the CLI to see if **net profit covers all minimums**.

## Progressive allocation (optional)

After minimums are covered, direct a fixed % of each income deposit to the highest-APR balance. Percentages stay fixed — no re-optimization every month.

Free template: [debt-tracker.md](debt-tracker.md) · [sample CSV](debt-sample.csv)
