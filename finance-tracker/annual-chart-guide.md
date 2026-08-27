# Annual income vs expenses chart

Clone of Quillenhart qaduu **Annual Summary** tab — the built-in 12-month income vs expenses chart Gumroad buyers see after logging transactions.

## Why the chart matters

[timmothybuilder tracked every dollar for six months](https://dev.to/timmothybuilder/i-tracked-every-dollar-for-6-months-as-a-freelance-developer-heres-what-i-learned-3fb2) and found surprises only visible when months sit side by side: subscription creep, undercharging, and quarterly tax shock. A year-at-a-glance chart turns a transaction log into a pattern you can act on.

## Run the chart

```bash
python3 monthly_dashboard.py sample-transactions.csv
```

Look for the **ANNUAL INCOME VS EXPENSES CHART** block after the annual summary table. Each month shows proportional bars for income (in) and expenses (out) plus net.

## What to do with it

1. **Spot lumpy income** — feast months vs famine months; plan tax set-aside on net, not gross deposits.
2. **Catch expense creep** — bars growing month over month without matching revenue (subscriptions, ads, contractors).
3. **Year-end sanity check** — compare YTD net to your gut; open [annual-summary.md](annual-summary.md) for the tabular view.
4. **Pair with tax stack** — use [tax-stack-guide.md](tax-stack-guide.md) for quarterly estimates after you trust the YTD numbers.

## Files

| File | Purpose |
|------|---------|
| `sample-transactions.csv` | Example multi-month log |
| `annual-summary.md` | Month-by-month table template |
| `setup-guide.md` | Tax set-aside % used in chart labels |
| `monthly_dashboard.py` | Auto chart from your CSV |

Not tax advice. Clone of [Quillenhart qaduu ($15, 7 ratings)](https://quillenhart.gumroad.com/l/qaduu).
