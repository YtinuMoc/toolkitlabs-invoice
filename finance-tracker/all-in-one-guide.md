# All-in-one finance system — replaces four apps (Quillenhart qaduu clone)

Clone of [faisalmq/54h7](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-54h7) buyer channel + Quillenhart Gumroad promise: *"This one file replaces a bookkeeping app, a budget planner, an invoice tracker, and a P&L report — all built to work together."*

## What Quillenhart replaces ($15, 7 ratings)

| Paid app | Monthly cost | Quillenhart tab | Our clone |
|----------|--------------|-----------------|-----------|
| Bookkeeping app (QuickBooks, Wave) | $15–$30/mo | Transactions + Dashboard | `sample-transactions.csv` + `monthly_dashboard.py` |
| Budget planner (YNAB, Monarch) | $8–$15/mo | Bills + Savings | `bills-tracker.md` + `savings-tracker.md` |
| Invoice tracker (FreshBooks) | $15–$25/mo | Invoices | `invoices-sample.csv` + AR stdout |
| P&L report (accountant export) | ad hoc | Annual Summary + Dashboard | YTD + monthly P&L stdout |

**Nothing extra to buy.** One-time purchase, reuse every year.

## Five-minute weekly check-in (faisalmq/54h7 shape)

1. **Monday (2 min):** Log last week's income and expenses in the transaction CSV — one row per event.
2. **Wednesday (1 min):** Mark recurring bills paid in `bills-tracker.md`.
3. **Friday (2 min):** Run `python3 monthly_dashboard.py your-log.csv` — scan P&L, margins, and tax set-aside.

If a system takes longer, you won't use it. This kit is built for the five-minute habit.

## Free preview

```bash
python3 monthly_dashboard.py sample-transactions.csv invoices-sample.csv bills-sample.csv debt-sample.csv savings-sample.csv
```

Look for the `ALL-IN-ONE REPLACEMENT` block in stdout — it maps each replaced app to active modules in your log.

## Full kit

Quillenhart: [$15 on Gumroad](https://quillenhart.gumroad.com/l/qaduu). Our clone: EUR 9 one-time zip — all guides + CSV templates + dashboard CLI.
