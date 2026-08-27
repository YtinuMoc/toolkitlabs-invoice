# Command Center cross-sell (Quillenhart acrum clone)

Clone of Quillenhart's **separate Gumroad SKU** cross-sold from [qaduu Finance Tracker](https://quillenhart.gumroad.com/l/qaduu):

- **Product:** [Small Business Command Center](https://quillenhart.gumroad.com/l/acrum)
- **Price:** $29 one-time (Gumroad)
- **Promise:** "Your entire small business, organized in one calm, beautiful system."

## What's included (acrum shape)

| Module | What it tracks |
|--------|----------------|
| Business Dashboard | Revenue, expenses, profit, outstanding invoices, active clients |
| Client tracker | Who owes what, follow-up status |
| Invoice pipeline | Sent · pending · overdue |
| Financial rollup | Links to finance tracker tabs |

Quillenhart cross-sells acrum **from the qaduu product page** — finance tracker handles money; command center handles clients + ops in one view.

## Our clone stack (EUR 9)

The [finance tracker kit](../finance-tracker/) already ships the **9-tab financial command center** (timmothybuilder/4e81 shape — template #5 in `command-center-guide.md`).

If you need the full acrum client+invoice ops layer:

1. Start with finance tracker CSV + `monthly_dashboard.py` (transactions, bills, debt, tax set-aside).
2. Add `invoices-sample.csv` + `invoices-tracker.md` for receivable pipeline.
3. Mirror acrum's "one calm system" by importing both into one Excel workbook (two sheets minimum).

Run:

```bash
python3 monthly_dashboard.py sample-transactions.csv invoices-sample.csv
```

Look for `COMMAND CENTER CROSS-SELL` in stdout — stack math vs buying qaduu ($15) + acrum ($29) separately on Gumroad.

## Original vs clone pricing

| Stack | Gumroad | Our clone |
|-------|---------|-----------|
| Finance tracker only (qaduu) | $15 | EUR 9 |
| Command Center only (acrum) | $29 | included guides + invoice module |
| Both SKUs | $44 | EUR 9 one-time zip |
