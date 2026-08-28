# Start here — Emotional Finance Tracker

Clone of [BodegaLabs Emotional Finance Tracker (1,253 sales · 39 ratings · 5★ · $8+)](https://bodegalaabs.gumroad.com/l/emotional-finance-tracker).

## 10-minute setup

1. Copy the template CSVs to your workspace.
2. Log income, expenses, and savings goals.
3. Add wishlist items you want but haven't funded yet.
4. Run the dashboard:

```bash
python3 emotional_finance_tracker.py income-sample.csv expenses-sample.csv accounts-sample.csv goals-sample.csv debts-sample.csv subscriptions-sample.csv
```

5. For take-home estimate (marginmap/14ag buyer channel):

```bash
python3 emotional_finance_tracker.py --take-home income-sample.csv expenses-sample.csv
```

6. For wishlist impulse check:

```bash
python3 emotional_finance_tracker.py --wishlist wishlist-sample.csv goals-sample.csv
```

## Monthly routine

- Log transactions when they happen — note emotional triggers in expense descriptions.
- Run `--wishlist` before any non-essential purchase.
- Run `--take-home` after deposits land to earmark tax reserve.

Not financial advice. Confirm tax estimates with a licensed professional.
