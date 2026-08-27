# Start here — Freelancer Income Tracker

Clone of PattyBun dcklyf ($14.99 Gumroad). Four CSV logs + one Python CLI.

## Step 1 — Income log

Copy `income-log-template.csv`. Log every 1099 payment:

```csv
date,client,amount,payment_method
2026-01-05,Client Name,2500.00,transfer
```

## Step 2 — Expense log

Copy `expense-log-template.csv`. Use Schedule C categories from `tax-settings.md`.

## Step 3 — Mileage (optional)

Copy `mileage-log-template.csv`. Miles × IRS rate = deduction.

## Step 4 — Invoices (optional)

Copy `invoice-log-template.csv`. Overdue rows print `*** OVERDUE ***`.

## Step 5 — Run dashboard

```bash
python3 freelancer_dashboard.py income.csv expenses.csv mileage.csv invoices.csv
```

Check **REAL TAKE-HOME** on the Live Profit Dashboard — that's the number PattyBun promises.
