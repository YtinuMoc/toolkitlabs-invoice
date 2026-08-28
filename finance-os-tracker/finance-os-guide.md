# Finance OS guide

Clone of [wilsonhoe/48cn](https://dev.to/wilsonhoe/notion-vs-spreadsheets-for-business-finance-tracking-i-ran-both-for-6-months-the-numbers-48cn) buyer channel + [heyismail Finance OS Pro ($29+)](https://heyismail.gumroad.com/l/TheUltimateFinanceTracker).

[wilsonhoe's post](https://dev.to/wilsonhoe/notion-vs-spreadsheets-for-business-finance-tracking-i-ran-both-for-6-months-the-numbers-48cn) ran Notion and Google Sheets side-by-side for six months. The spreadsheet wasn't wrong — it was slow and fragile. Notion won on invoice kanban and relational data. But for solopreneurs under 50 transactions/month, a well-structured spreadsheet still wins on simplicity and accountant compatibility.

heyismail's Finance OS (15,254 sales · 177 ratings · 4.9★) packages that relational promise into a Notion template: income, expenses, budgets, subscriptions, goals, net worth — one command center.

Our shameless clone ships the same modules as CSV + Python CLI at EUR 9.

## The 6 modules

1. **Income tracker** — log every deposit by source and category
2. **Expense tracker** — categorized spending with account tags
3. **Budget vs actual** — set monthly limits, see overruns instantly
4. **Subscription tracker** — monthly burn + renewal dates
5. **Net worth** — assets minus liabilities across accounts
6. **Financial goals** — target vs current progress %

## Free CLI

```bash
python3 finance_os_tracker.py income-sample.csv expenses-sample.csv budgets-sample.csv subscriptions-sample.csv accounts-sample.csv goals-sample.csv
```

## When to use this vs QuickBooks

wilsonhoe/48cn framework:

- Under $5K/year, <50 transactions/month: spreadsheet (or this CLI)
- $5K–$30K/year: structured tracker like Finance OS
- $30K+/year: export to your accountant's preferred format

## Paid clone

[heyismail's Finance OS Pro](https://heyismail.gumroad.com/l/TheUltimateFinanceTracker) is $29+ on Gumroad (15,254 sales).

Our clone: EUR 9 one-time instant zip via Stripe on the [landing page](index.html).
