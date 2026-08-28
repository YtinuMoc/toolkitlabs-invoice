# Tax buffer calculator — the day client money lands

Clone of [faisalmq/4gao](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-4gao) buyer channel + [jahazielgpz Smart Finance ($8.99+ · 35 ratings · 4.9★)](https://jahazielgpz.gumroad.com/l/smartfinance2025).

## The five-minute panic

You finish a project, watch the deposit land in your account. It feels great for five minutes. Then:

- How much is actually yours to spend?
- How much goes to quarterly taxes?
- Did impulse spending eat the margin?

faisalmq/4gao calls this "mental accounting" — treating your checking account like a slush fund. jahazielgpz's Smart Finance rolls income, expenses, subscriptions, and savings goals into one workspace — the tax buffer habit belongs in the same workbook.

## Per-payment withholding (faisalmq/4gao shape)

Default reserve: **25% of net profit** (adjust `DEFAULT_TAX_PCT` in `smart_finance_tracker.py`).

| Source | Collected | Est. buffer (25%) | Safe to spend |
|--------|-----------|-------------------|---------------|
| Client A | $8,000 | $2,000 | $6,000 |
| Retainer | $2,400 | $600 | $1,800 |

Run:

```bash
python3 smart_finance_tracker.py --tax-buffer income-sample.csv expenses-sample.csv
```

Read **EXPENSE + TAX BUFFER** — net profit, 25% earmark, safe-to-spend number.

## Tax-only savings account

faisalmq/4gao users set up a separate account and transfer the buffer amount **when the payment lands**, not in April. Smart Finance pairs this habit with subscription tracking and savings goals in one view.

## Pair with

- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run380)
- [start-here.md](start-here.md) — full income + expense setup
