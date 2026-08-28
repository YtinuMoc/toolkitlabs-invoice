# Start here — Smart Financial Tracker

Clone of [hyeukiyo Notion Smart Financial (133 sales · 5 ratings · 5★ · $10.73)](https://hyeukiyo.gumroad.com/l/Fimgntemp).

## 10-minute setup

1. Copy the template CSVs to your workspace.
2. Log income and expenses in the cashflow CSVs (same promise as the Gumroad CASHFLOW section).
3. Set monthly budgets per category and track subscriptions + wishlist.
4. Run the dashboard:

```bash
python3 smart_financial_tracker.py income-sample.csv expenses-sample.csv accounts-sample.csv goals-sample.csv debts-sample.csv subscriptions-sample.csv
```

5. For take-home estimate (marginmap/14ag buyer channel):

```bash
python3 smart_financial_tracker.py --take-home income-sample.csv expenses-sample.csv
```

6. For wishlist vs savings goals:

```bash
python3 smart_financial_tracker.py --wishlist wishlist-sample.csv goals-sample.csv
```

## Monthly routine

- Record cashflows when money moves — one row per transaction.
- Run `--take-home` after deposits to earmark tax reserve.
- Run `--wishlist` before discretionary purchases.

Not financial advice. Confirm tax estimates with a licensed professional.
