# Start here — Tony David Finance Tracker

Clone of [Tony David Notion Finance Tracker (52 ratings · 5★ · $5+)](https://tonydavid.gumroad.com/l/rjwua).

## 10-minute setup

1. Copy the template CSVs to your workspace.
2. Log income and expenses by category.
3. Run the dashboard:

```bash
python3 tonydavid_finance_tracker.py income-sample.csv expenses-sample.csv accounts-sample.csv goals-sample.csv debts-sample.csv subscriptions-sample.csv
```

4. For take-home estimate (marginmap/14ag buyer channel):

```bash
python3 tonydavid_finance_tracker.py --take-home income-sample.csv expenses-sample.csv
```

## Monthly routine

- Log transactions when they happen — not at month-end.
- Run `--take-home` after deposits land to earmark tax reserve.
- Review summary cards monthly to see where money goes.

Not financial advice. Confirm tax estimates with a licensed professional.
