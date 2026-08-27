# Complete finance workbook — Excel/CSV, no Notion (Quillenhart qaduu clone)

Clone of [hemantdev/1iae](https://dev.to/hemantdev/i-built-a-freepaid-finance-gst-tracker-for-indian-freelancers-excel-no-notion-needed-1iae) buyer channel + Quillenhart Gumroad **"Nothing left out. Nothing extra to buy"** promise ($15, 7 ratings).

## Why a file, not Notion

Notion templates need an account, sync, and block syntax. Quillenhart sells a **single workbook** that opens offline in Excel or Google Sheets — shaded cells only, everything else calculates. Our clone ships CSV + Python CLI with the same shape: log once, every view updates.

## Six connected views (hemantdev → Quillenhart)

| hemantdev sheet | Quillenhart tab | Our clone |
|-----------------|-----------------|-----------|
| Dashboard | Dashboard | `monthly_dashboard.py` — pick any month |
| Income | Transactions | `sample-transactions.csv` / your log |
| Expenses | Transactions (categorized) | same log, category column |
| Clients | Invoices | `invoices-sample.csv` + AR stdout |
| Invoices | Invoices | overdue/pending/paid split |
| Tax Estimator | Quarterly set-aside | 25% of net (configurable in setup) |

Quillenhart adds Bills, Savings, Debt, and Annual Summary — same log, no re-typing.

## One-click month switching (core Gumroad feature)

Quillenhart's headline: *"Pick any month from a dropdown and your whole dashboard updates instantly."*

CLI equivalent:

```bash
# default = latest month in log
python3 monthly_dashboard.py sample-transactions.csv

# switch month (dropdown equivalent)
FINANCE_MONTH=2026-01 python3 monthly_dashboard.py sample-transactions.csv
```

Every module (P&L, category breakdown, tax set-aside, YTD) recalculates from the same transaction log — no duplicate entry.

## Free preview

```bash
python3 monthly_dashboard.py sample-transactions.csv invoices-sample.csv bills-sample.csv debt-sample.csv
```

Look for `ONE-CLICK MONTH SWITCHING` and `COMPLETE WORKBOOK` blocks in stdout.

## Paid kit

Full 9-tab system: [finance tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/finance-tracker/) · EUR 9 one-time · [Stripe checkout](https://buy.stripe.com/6oUeVe5KS6PO7Fc5FP5Ne0t?client_reference_id=complete-system-guide)
