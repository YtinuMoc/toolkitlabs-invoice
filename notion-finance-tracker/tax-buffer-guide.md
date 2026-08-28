# Tax buffer calculator — the day client money lands

Clone of [faisalmq/4gao](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-4gao) buyer channel + [Rosidssoy's Notion Finance Tracker ($5+ · 190 ratings · 13,696 sales)](https://rosidssoy.gumroad.com/l/financetracker).

## The five-minute panic

You finish a project, watch the deposit land in your account. It feels great for five minutes. Then:

- How much is actually yours to spend?
- How much goes to quarterly taxes?
- Did subscriptions and software eat the margin?

faisalmq/4gao calls this "mental accounting" — treating your checking account like a slush fund. Rosidssoy's Notion Finance Tracker rolls income, expenses, accounts, and goals into one dashboard — the tax buffer habit belongs in the same workbook.

## Per-payment withholding (faisalmq/4gao shape)

Default reserve: **25% of net profit** (adjust `DEFAULT_TAX_PCT` in `notion_finance_tracker.py`).

| Source | Collected | Est. buffer (25%) | Safe to spend |
|--------|-----------|-------------------|---------------|
| Salary | $4,200 | $1,050 | $3,150 |
| Freelance | $850 | $212.50 | $637.50 |

Run:

```bash
python3 notion_finance_tracker.py --tax-buffer income-sample.csv expenses-sample.csv
```

Read **EXPENSE + TAX BUFFER** — net profit, 25% earmark, safe-to-spend number.

## Tax-only savings account

faisalmq/4gao users set up a separate account and transfer the buffer amount **when the payment lands**, not in April. Rosidssoy's tracker pairs this habit with income sources, expense categories, and financial goals in one view.

## Pair with

- [tax-quarter-guide.md](tax-quarter-guide.md) — wilsonhoe/4lhd buyer channel (run305)
- [start-here.md](start-here.md) — full income + expense setup
