# Start here — Notion Finance Tracker

Clone of [EasyBlocks Notion Finance Tracker (11 ratings · 5★ · $39)](https://easyblocks.gumroad.com/l/notion-finance-tracker).

## 10-minute setup

1. Copy the template CSVs to your workspace.
2. Log income and expenses (same promise as EasyBlocks' finance system).
3. Set account balances, monthly budgets, goals, and subscriptions.
4. Run the dashboard:

```bash
python3 easyblocks_finance_tracker.py income-sample.csv expenses-sample.csv accounts-sample.csv goals-sample.csv debts-sample.csv subscriptions-sample.csv
```

5. For take-home estimate (marginmap/14ag buyer channel):

```bash
python3 easyblocks_finance_tracker.py --take-home income-sample.csv expenses-sample.csv
```

## Monthly routine

- Record transactions when money moves — one row per entry.
- Run `--take-home` after deposits to earmark tax reserve.
- Review subscription burn monthly.

Not financial advice. Confirm tax estimates with a licensed professional.
