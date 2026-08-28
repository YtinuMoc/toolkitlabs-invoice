# Start here — Matthew Finance Tracker

Clone of [matthewnotion Finance Tracker (58 sales)](https://matthewnotion.gumroad.com/l/financetracker).

## Guide index

See [mesh-hub.md](mesh-hub.md) for all 4 dev.to buyer-channel guides.

## 10-minute setup

1. Copy the seven template CSVs to your workspace.
2. Log income, expenses, accounts, goals, debts, and subscriptions.
3. Run the dashboard:

```bash
python3 matthew_finance_tracker.py income-sample.csv expenses-sample.csv accounts-sample.csv goals-sample.csv debts-sample.csv subscriptions-sample.csv
```

4. For take-home estimate (marginmap/14ag buyer channel):

```bash
python3 matthew_finance_tracker.py --take-home income-sample.csv expenses-sample.csv
```

## Monthly routine

- Log transactions when they happen — not at month-end.
- Run `--take-home` after deposits land to earmark tax reserve.
- Review subscription CSV monthly — cancel what you forgot about.

Not financial advice. Confirm tax estimates with a licensed professional.
