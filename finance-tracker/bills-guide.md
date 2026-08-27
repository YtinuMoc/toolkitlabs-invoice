# Recurring Bills Calendar Guide

Clone of Quillenhart qaduu **bills tab** — 12-month payment grid — plus the recurring-list shape from bill-calendar spreadsheet posts (one row per bill, not one row per month).

## Why a bills tab exists

Freelancers track income in a transaction log but forget fixed costs until they hit the bank. A recurring bills list answers: **what must leave my account this month regardless of client work?**

## One row per bill (forever)

| Bill | Amount | Frequency | Due day | Status |
|------|--------|-----------|---------|--------|
| Hosting | $20 | monthly | 1 | paid |
| Software | $54 | monthly | 15 | pending |
| Insurance | $120 | quarterly | 1 | pending |

Mark `paid` when the charge clears. Add rows when you subscribe — delete when you cancel.

## Monthly ritual (5 minutes)

1. Open `bills-tracker.md` or `bills-sample.csv`
2. Mark fixed bills paid for the current month
3. Run `monthly_dashboard.py` — see if net profit covers bills + debt minimums

Free template: [bills-tracker.md](bills-tracker.md) · [sample CSV](bills-sample.csv)
