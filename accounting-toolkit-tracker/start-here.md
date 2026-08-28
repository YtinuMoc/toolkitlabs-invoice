# Start here — Accounting Toolkit Tracker

Clone of [theaccountantguy Ultimate Accounting Toolkit (92 sales)](https://theaccountantguy.gumroad.com/l/notionaccountingtoolkit).

## 10-minute setup

1. Copy the six template CSVs to your workspace.
2. Log income, expenses, accounts, savings goals, debts, and subscriptions.
3. Run the dashboard:

```bash
python3 accounting_toolkit.py income-sample.csv expenses-sample.csv accounts-sample.csv goals-sample.csv debts-sample.csv subscriptions-sample.csv
```

4. For take-home estimate (marginmap/14ag buyer channel):

```bash
python3 accounting_toolkit.py --take-home income-sample.csv expenses-sample.csv
```

## Monthly routine

- Log transactions when they happen — not at month-end.
- Run `--take-home` after deposits land to earmark tax reserve.
- Review debt + savings goal progress monthly.

Not financial advice. Confirm tax estimates with a licensed professional.
