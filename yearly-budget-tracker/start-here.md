# Start here — Yearly Budget Tracker

Clone of [mariesells Notion Yearly Budget Tracker (6 ratings · 5★ · $5.99+)](https://mariesells.gumroad.com/l/yearly-budget-tracker).

## 10-minute setup

1. Copy the template CSVs to your workspace.
2. Log income and expenses (same promise as mariesells's income/expense trackers).
3. Set account balances, monthly budgets, goals, debts, and subscriptions.
4. Run the dashboard:

```bash
python3 yearly_budget_tracker.py income-sample.csv expenses-sample.csv accounts-sample.csv goals-sample.csv debts-sample.csv subscriptions-sample.csv
```

5. For take-home estimate (marginmap/14ag buyer channel):

```bash
python3 yearly_budget_tracker.py --take-home income-sample.csv expenses-sample.csv
```

## Yearly routine

- Record transactions when money moves — one row per entry.
- Review 12 monthly breakdowns quarterly.
- Run `--take-home` after deposits to earmark tax reserve.
- Track debt repayments and savings goals monthly.

Not financial advice. Confirm tax estimates with a licensed professional.
