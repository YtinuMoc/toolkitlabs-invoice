# Start here — Freelancer Finance Tracker

Clone of [moonlight573 unsjlk ($10)](https://moonlight573.gumroad.com/l/unsjlk).

## Guide index

See [mesh-hub.md](mesh-hub.md) for all 5 dev.to buyer-channel guides.

## 10-minute setup

1. Copy `income-template.csv`, `expenses-template.csv`, and `invoices-template.csv` to your workspace.
2. Log paid income, expenses, and open invoices.
3. Run the dashboard:

```bash
python3 freelancer_finance_tracker.py income-sample.csv expenses-sample.csv invoices-sample.csv
```

4. Move the **Tax set-aside** number to a separate savings account when payments land.

## Monthly routine

- Log new payments in the income sheet.
- Log subscriptions and one-off costs in expenses.
- Mark invoices paid or unpaid — overdue rows flag automatically.
- Re-run the CLI — dashboard totals update instantly.

Not tax advice. Confirm rates with a licensed professional before filing.
