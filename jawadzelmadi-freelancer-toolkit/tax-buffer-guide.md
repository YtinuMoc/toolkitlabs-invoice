# Tax buffer calculator — the day client money lands

Clone of [faisalmq/4gao](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-4gao) buyer channel + [jawadzelmadi Ultimate Freelancer Toolkit (39 sales · 5 ratings · 5.0★ · $9+)](https://jawadzelmadi.gumroad.com/l/FreelancerToolkit).

## The five-minute panic

You finish a project, watch the deposit land in your account. It feels great for five minutes. Then:

- How much is actually yours to spend?
- How much goes to quarterly taxes?
- Did impulse spending eat the margin?

faisalmq/4gao calls this "mental accounting" — treating your checking account like a slush fund. jawadzelmadi's Ultimate Freelancer Toolkit rolls income, expenses, clients, and projects into one workspace — the tax buffer habit belongs in the same workbook.

## Per-payment withholding (faisalmq/4gao shape)

Default reserve: **25% of net profit** (adjust `DEFAULT_TAX_PCT` in `jawadzelmadi_freelancer_toolkit.py`).

| Source | Collected | Est. buffer (25%) | Safe to spend |
|--------|-----------|-------------------|---------------|
| Client A | $8,000 | $2,000 | $6,000 |
| Retainer | $2,400 | $600 | $1,800 |

Run:

```bash
python3 jawadzelmadi_freelancer_toolkit.py --tax-buffer income-sample.csv expenses-sample.csv
```

Read **EXPENSE + TAX BUFFER** — net profit, 25% earmark, safe-to-spend number.

## Tax-only savings account

faisalmq/4gao users set up a separate account and transfer the buffer amount **when the payment lands**, not in April. Ultimate Freelancer Toolkit pairs this habit with client/project tracking and income/expense totals in one view.

## Pair with

- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run390)
- [start-here.md](start-here.md) — full income + expense setup
