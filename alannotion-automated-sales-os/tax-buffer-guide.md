# Tax buffer calculator — the day digital product revenue lands

Clone of [faisalmq/4gao](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-4gao) buyer channel + [alannotion Automated Sales OS ($15 · creator 5★/20 reviews)](https://alannotion.gumroad.com/l/automatedsalesos).

## The five-minute panic

A Gumroad sale notification hits. Stripe deposits land. It feels great for five minutes. Then:

- How much of this sale is actually yours to spend?
- How much goes to quarterly taxes?
- Did you already spend it on ads?

faisalmq/4gao calls this "mental accounting" — treating your business account like a slush fund. Automated Sales OS rolls Gumroad + Stripe sales into daily/weekly/monthly dashboards — the tax buffer habit belongs in the same morning routine.

## Per-sale withholding (faisalmq/4gao shape)

Default reserve: **25% of net sales** (adjust `--tax-pct` or `DEFAULT_TAX_PCT` in `automated_sales_os.py`).

| Product | Net (after fees) | Est. buffer (25%) | Safe to spend |
|---------|------------------|-------------------|---------------|
| Annual license | $187.14 | $46.79 | $140.35 |
| E-book Bundle | $44.10 | $11.03 | $33.07 |

Run:

```bash
python3 automated_sales_os.py --tax-buffer gumroad-sample.csv stripe-sample.csv
```

Read **SALES REVENUE + TAX BUFFER** — net sales, 25% earmark, safe-to-spend number.

## Tax-only savings account

faisalmq/4gao users set up a separate account and transfer the buffer amount **when the payment lands**, not in April. Automated Sales OS pairs this habit with merged Gumroad + Stripe sales in one dashboard.

## Pair with

- [sales-dashboard-guide.md](sales-dashboard-guide.md) — goldenalien/206o merge-ledger buyer channel (run405)
- [start-here.md](start-here.md) — full sales merge setup
