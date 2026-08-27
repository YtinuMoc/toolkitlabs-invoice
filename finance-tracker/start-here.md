# Start Here — Small Business Finance Tracker

Clone of Quillenhart qaduu start-here shape.

## What this kit is

A complete finance system without monthly bookkeeping software. Log income and expenses once in `transaction-log-template.csv`, run `monthly_dashboard.py`, and get:

- Net profit for any month
- Category breakdown
- Quarterly tax set-aside estimate
- Year-to-date totals

Supporting trackers: `bills-tracker.md`, `debt-tracker.md`, `invoices-tracker.md`.

## 5-minute setup

1. Copy `transaction-log-template.csv` → `my-transactions.csv`
2. Edit `setup-guide.md` with your business name, tax year, and tax set-aside %
3. Log this month's transactions (date, type, category, amount)
4. Run: `python3 monthly_dashboard.py my-transactions.csv`
5. Open `bills-tracker.md` and mark recurring bills for the month

## Who it's for

Freelancers, solopreneurs, and small business owners who want the complete financial picture without a subscription.

## Shaded cells = you type

In the CSV: only add rows under the header. The Python script handles all math.
