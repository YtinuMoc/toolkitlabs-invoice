# Tax buffer calculator — the day client money lands

Clone of [faisalmq/4gao](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-4gao) buyer channel + [chrisnotion Finance OS Dashboard (30,427 sales · 506 ratings · 4.9★)](https://chrisnotion.gumroad.com/l/fcufra).

## The five-minute panic

You finish a project, watch the deposit land in your account. It feels great for five minutes. Then:

- How much is actually yours to spend?
- How much goes to quarterly taxes?
- Did subscriptions and software eat the margin?

faisalmq/4gao calls this "mental accounting" — treating your checking account like a slush fund. chrisnotion's Finance OS Dashboard rolls income, expenses, subscriptions, and bank accounts into one overview — the tax buffer habit belongs in the same workbook.

## Per-payment withholding (faisalmq/4gao shape)

Default reserve: **25% of net profit** (adjust `DEFAULT_TAX_PCT` in `finance_os_dashboard.py`).

| Source | Collected | Est. buffer (25%) | Safe to spend |
|--------|-----------|-------------------|---------------|
| Salary | $4,200 | $1,050 | $3,150 |
| Freelance | $850 | $212.50 | $637.50 |

Run:

```bash
python3 finance_os_dashboard.py --tax-buffer income-sample.csv expenses-sample.csv
```

Read **EXPENSE + TAX BUFFER** — net profit, 25% earmark, safe-to-spend number.

## Tax-only savings account

faisalmq/4gao users set up a separate account and transfer the buffer amount **when the payment lands**, not in April. chrisnotion's Finance OS pairs this habit with income sources, expense categories, and subscription tracking in one view.

## Pair with

- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run315)
- [start-here.md](start-here.md) — full income + expense setup
