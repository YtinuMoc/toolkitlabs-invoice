# Net income visibility — what's actually safe to spend

Clone of [faisalmq/5797](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-5797) buyer channel + [Rosidssoy's Notion Finance Tracker ($5+ · 190 ratings · 13,696 sales)](https://rosidssoy.gumroad.com/l/financetracker).

## The financial fog

You finish a freelance project, send the invoice, watch the payment land. For a brief moment you feel flush.

Then the fog:

- How much of this is actually mine?
- Did I already owe quarterly taxes on the gross?
- Can I upgrade software or is that money already spoken for?

faisalmq/5797 frames the fix as **net income visibility** — see safe-to-spend after obligations, not gross deposits.

Rosidssoy's **Notion Finance Tracker** rolls income, expenses, accounts, goals, and debts into one dashboard — the safe-spend number belongs in the same workbook.

## Free CLI preview

```bash
python3 notion_finance_tracker.py --net-income income-sample.csv expenses-sample.csv
```

Read the **NET INCOME VISIBILITY** block — gross collected, deductible expenses, tax set-aside, and safe-to-spend.

## Why gross deposits lie

| What your invoice says | What your bank shows | What you can spend |
|------------------------|----------------------|--------------------|
| Client paid $4,500 | Deposit $4,500 | Less after expenses, SaaS, tax reserve |

Spending from gross deposits is how freelancers overspend in Q3 and panic in April.

## Pair with

- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run306)
- [tax-quarter-guide.md](tax-quarter-guide.md) — wilsonhoe/4lhd quarterly set-aside (run305)
- [start-here.md](start-here.md) — full income + expense setup

Full bundle: [Notion Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/notion-finance-tracker/) — 6 CSV templates, dashboard CLI, and all buyer-channel guides.
