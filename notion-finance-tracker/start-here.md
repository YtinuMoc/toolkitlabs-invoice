# Start here — Notion Finance Tracker

Clone of [Rosidssoy Notion Finance Tracker ($5+ · 190 ratings · 13,696 sales)](https://rosidssoy.gumroad.com/l/financetracker).

## 10-minute setup

1. Copy the six template CSVs to your workspace.
2. Log income, expenses, accounts, goals, debts, and subscriptions.
3. Run the dashboard:

```bash
python3 notion_finance_tracker.py income-sample.csv expenses-sample.csv accounts-sample.csv goals-sample.csv debts-sample.csv subscriptions-sample.csv
```

4. For quarterly tax planning (wilsonhoe/4lhd buyer channel):

```bash
python3 notion_finance_tracker.py --quarterly-tax income-sample.csv expenses-sample.csv
```

## Monthly routine

- Log transactions when they happen — not at month-end.
- Run `--quarterly-tax` at the end of each quarter.
- Transfer the set-aside amount to a dedicated tax reserve account.

Not financial advice. Confirm tax estimates with a licensed professional.
