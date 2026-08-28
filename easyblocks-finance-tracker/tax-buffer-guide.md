# Tax buffer calculator — the day client money lands

Clone of [faisalmq/4gao](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-4gao) buyer channel + [EasyBlocks Notion Finance Tracker (11 ratings · 5★ · $39)](https://easyblocks.gumroad.com/l/notion-finance-tracker).

## The five-minute panic

You finish a project, watch the deposit land in your account. It feels great for five minutes. Then:

- How much is actually yours to spend?
- How much goes to quarterly taxes?
- Did impulse spending eat the margin?

faisalmq/4gao calls this "mental accounting" — treating your checking account like a slush fund. EasyBlocks' Notion Finance Tracker rolls income, expenses, accounts, and budgets into one workspace — the tax buffer habit belongs in the same system.

## Per-payment withholding (faisalmq/4gao shape)

Default reserve: **25% of net profit** (adjust `DEFAULT_TAX_PCT` in `easyblocks_finance_tracker.py`).

| Source | Collected | Est. buffer (25%) | Safe to spend |
|--------|-----------|-------------------|---------------|
| Client A | $8,000 | $2,000 | $6,000 |
| Retainer | $2,400 | $600 | $1,800 |

Run:

```bash
python3 easyblocks_finance_tracker.py --tax-buffer income-sample.csv expenses-sample.csv
```

Read **EXPENSE + TAX BUFFER** — net profit, 25% earmark, safe-to-spend number.

## Tax-only savings account

faisalmq/4gao users set up a separate account and transfer the buffer amount **when the payment lands**, not in April. Notion Finance Tracker pairs this habit with income/expense tracking and budget categories in one view.

## Pair with

- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run400)
- [start-here.md](start-here.md) — full income + expense setup
