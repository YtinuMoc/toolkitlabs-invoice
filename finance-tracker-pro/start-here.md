# Start here — Finance Tracker Pro

Clone of [organizeddashboard Finance Tracker Pro ($12 · 15 ratings · 5★)](https://organizeddashboard.gumroad.com/l/cyezap).

## 10-minute setup

1. Copy the template CSVs to your workspace.
2. Log income and expenses (same promise as organizeddashboard's Finance Tracker Pro).
3. Set account balances, budgets, goals, debts, and subscriptions.
4. Run the dashboard:

```bash
python3 finance_tracker_pro.py income-sample.csv expenses-sample.csv accounts-sample.csv goals-sample.csv debts-sample.csv subscriptions-sample.csv
```

5. For take-home estimate (marginmap/14ag buyer channel):

```bash
python3 finance_tracker_pro.py --take-home income-sample.csv expenses-sample.csv
```

## Monthly routine

- Record transactions when money moves — one row per entry.
- Review monthly summary before month-end.
- Run `--take-home` after client deposits to earmark tax reserve.
- Check subscription renewals so nothing auto-charges unnoticed.

Not financial advice. Confirm tax estimates with a licensed professional.
