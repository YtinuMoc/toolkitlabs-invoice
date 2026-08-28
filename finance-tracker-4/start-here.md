# Start here — Finance Tracker 4.0

Clone of [jnkxstudio Finance Tracker 4.0 (2,995 sales · 4.9★)](https://jnkxstudio.gumroad.com/l/Finance_Tracker_3).

## 10-minute setup

1. Copy the seven template CSVs to your workspace.
2. Log income, expenses, accounts, goals, debts, subscriptions, and invoices.
3. Run the dashboard:

```bash
python3 finance_tracker_4.py income-sample.csv expenses-sample.csv accounts-sample.csv goals-sample.csv debts-sample.csv subscriptions-sample.csv
```

4. For late payment tracking (wilsonhoe/2gnj buyer channel):

```bash
python3 finance_tracker_4.py --late-payment invoices-sample.csv
```

## Monthly routine

- Log transactions when they happen — not at month-end.
- Log every invoice at send with due date and status.
- Run `--late-payment` weekly to surface overdue invoices before they pile up.

Not financial advice. Confirm tax estimates with a licensed professional.
