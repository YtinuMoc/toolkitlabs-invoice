# Tax buffer calculator — the day client money lands

Clone of [faisalmq/4gao](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-4gao) buyer channel + [Anna Hickman's Freelance Dashboard ($97 · 1,251 sales · 69 ratings)](https://cedabranding.gumroad.com/l/pro-dashboard).

## The five-minute panic

You finish a project, watch the deposit land in your account. It feels great for five minutes. Then:

- How much is actually yours to spend?
- How much goes to quarterly taxes?
- Did subscriptions and software eat the margin?

faisalmq/4gao calls this "mental accounting" — treating your checking account like a slush fund. cedabranding's Freelance Dashboard rolls revenue, expenses, client mix, and tax set-aside into one planning view — the tax buffer habit belongs in the same workbook.

## Per-payment withholding (faisalmq/4gao shape)

Default reserve: **25% of net profit** (adjust `DEFAULT_TAX_PCT` in `freelance_dashboard_tracker.py`).

| Client | Collected | Est. buffer (25%) | Safe to spend |
|--------|-----------|-------------------|---------------|
| Acme Coaching | $3,200 | $800 | $2,400 |
| Beta Consulting | $1,800 | $450 | $1,350 |

Run:

```bash
python3 freelance_dashboard_tracker.py --tax-buffer revenue-sample.csv expenses-sample.csv
```

Read **EXPENSE + TAX BUFFER** — net profit, 25% earmark, safe-to-spend number.

## Tax-only savings account

faisalmq/4gao users set up a separate account and transfer the buffer amount **when the payment lands**, not in April. cedabranding's dashboard pairs this habit with client revenue % and cash runway in one view.

## Pair with

- [spreadsheet-trap-guide.md](spreadsheet-trap-guide.md) — wilsonhoe/4khk buyer channel (run292)
- [daily-check-guide.md](daily-check-guide.md) — wilsonhoe/2kdc buyer channel (run293)
- [freelance-finance-tracker-guide.md](freelance-finance-tracker-guide.md) — faisalmq/5598 buyer channel (run294)
- [start-here.md](start-here.md) — full revenue + expense setup
