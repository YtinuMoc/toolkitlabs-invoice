# Start here — Business Finance Tracker

Clone of [fayedinua Finance OS Business Finance Tracker ($39+ · 2 ratings · 5★)](https://fayedinua.gumroad.com/l/business-finance-tracker-notion).

## 10-minute setup

1. Copy the template CSVs to your workspace.
2. Log business income and expenses (same promise as fayedinua's Finance OS).
3. Set account balances, budgets, goals, debts, and subscriptions.
4. Run the dashboard:

```bash
python3 business_finance_tracker.py income-sample.csv expenses-sample.csv accounts-sample.csv goals-sample.csv debts-sample.csv subscriptions-sample.csv
```

5. For take-home estimate (marginmap/14ag buyer channel):

```bash
python3 business_finance_tracker.py --take-home income-sample.csv expenses-sample.csv
```

## Monthly routine

- Record transactions when money moves — one row per entry.
- Review cash flow and VAT summary before month-end.
- Run `--take-home` after client deposits to earmark tax reserve.
- Chase overdue invoices from the pipeline view.

Not financial advice. Confirm tax estimates with a licensed professional.
