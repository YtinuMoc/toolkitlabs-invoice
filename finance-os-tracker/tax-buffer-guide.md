# Tax buffer calculator — the day income lands

Clone of [faisalmq/4gao](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-4gao) buyer channel + [heyismail's Finance OS Pro ($29+)](https://heyismail.gumroad.com/l/TheUltimateFinanceTracker).

## The five-minute panic

You finish a project, watch the deposit land, feel great for five minutes. Then:

- How much is actually yours?
- How much goes to taxes?
- Did subscriptions eat the margin?

faisalmq/4gao calls this "mental accounting" — treating your business account like personal checking. heyismail's Finance OS includes debt, liability, and tax set-aside modules for exactly this problem.

## Per-payment withholding (faisalmq/4gao shape)

Default reserve: **25% of net profit** (adjust `DEFAULT_TAX_PCT` in `finance_os_tracker.py`).

| Source | Collected | Est. buffer (25%) | Safe to spend |
|--------|-----------|-------------------|---------------|
| Client retainer | $4,500 | $1,125 | $3,375 |
| Digital product | $890 | $223 | $667 |

Run:

```bash
python3 finance_os_tracker.py --tax-buffer income-sample.csv expenses-sample.csv
```

Read **EXPENSE + TAX BUFFER** — net profit, 25% earmark, safe-to-spend number.

## Tax-only savings account

faisalmq/4gao users set up a separate account and transfer the buffer amount **when the payment lands**, not in April. heyismail's Finance OS rolls the same numbers into monthly and quarterly reporting views.

## Pair with

- [finance-os-guide.md](finance-os-guide.md) — full command center setup
- [start-here.md](start-here.md) — income, expense, budget, subscription modules
- [dev.to Notion vs spreadsheets article](https://dev.to/toolkitlabs/notion-vs-spreadsheets-for-business-finance-i-ran-both-for-6-months-heyismail-finance-os-clone-59pd) — wilsonhoe/48cn buyer channel (run279)

Full bundle: [Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/finance-os-tracker/) — income + expense + budget + subscription + net worth + goals.
