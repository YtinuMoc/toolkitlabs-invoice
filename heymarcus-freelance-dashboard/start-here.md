# Start here — Finance Tracker

Clone of [heymarcus All-in-One Freelance Dashboard (257 sales · 11 ratings · 4.9★ · $19+)](https://heymarcus.gumroad.com/l/bpqsi).

## 10-minute setup

1. Copy the template CSVs to your workspace.
2. Log income and expenses (same promise as heymarcus's income/expense tracking).
3. Set account balances, monthly budgets, goals, and subscriptions.
4. Run the dashboard:

```bash
python3 heymarcus_freelance_dashboard.py income-sample.csv expenses-sample.csv accounts-sample.csv goals-sample.csv debts-sample.csv subscriptions-sample.csv
```

5. For take-home estimate (marginmap/14ag buyer channel):

```bash
python3 heymarcus_freelance_dashboard.py --take-home income-sample.csv expenses-sample.csv
```

## Monthly routine

- Record transactions when money moves — one row per entry.
- Run `--take-home` after deposits to earmark tax reserve.
- Review subscription burn monthly.

Not financial advice. Confirm tax estimates with a licensed professional.
