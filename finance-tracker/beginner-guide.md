# Beginner-friendly finance tracker — shaded cells only (Quillenhart qaduu clone)

Clone of Quillenhart Gumroad **"Built for people who've never touched a spreadsheet formula"** + [faisalmq/2fj6](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-2fj6) buyer channel: end-of-month dread → clarity without an accounting degree → paid kit upsell ($15 Gumroad, 7 ratings).

## The faisalmq/2fj6 promise

[faisalmq/2fj6](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-2fj6) names three outcomes freelancers actually want:

1. **Track income and expenses in one place** — no hunting email for invoice history
2. **Visualize take-home pay** — net after business costs, not gross deposits
3. **Prepare for tax season** — organized data so filing isn't a month-long headache

Quillenhart adds the mechanical rule: **shaded cells are the only ones you type into**. Everything else calculates itself.

## Shaded cells in this kit

| You type (shaded) | Auto-calculated |
|-------------------|-----------------|
| CSV row: date, type, category, description, amount | Monthly P&L per month |
| setup-guide.md: business name, tax year, set-aside % | Net profit and margin % |
| bills/debt/invoices sample CSVs | YTD totals |
| savings goal rows | Quarterly tax set-aside |
| | Category breakdown by month |

No `SUMIFS`. No pivot tables. Run the dashboard script after you log.

## Free preview

```bash
python3 monthly_dashboard.py sample-transactions.csv
```

Look for `BEGINNER-FRIENDLY` in stdout:

```
=== BEGINNER-FRIENDLY (Quillenhart — no formulas required) ===
  You only type into shaded cells. In this kit that's your CSV rows.
  Type here:     date, type, category, description, amount (CSV rows)
  Auto-calculated: monthly P&L, margins, YTD, tax set-aside, category %
  Transaction log: 8/150 rows used (expandable — duplicate template)
```

## 150 rows, expandable

Quillenhart ships **150 transaction rows** in the Transactions tab. Our kit uses `transaction-log-template.csv` — duplicate rows or append to `sample-transactions.csv` as your business grows.

## Who it's for

- Freelancers who've never touched a spreadsheet formula
- Creators and indie hackers who want bookkeeping to get out of the way
- Anyone replacing "hope my bank balance looks healthy" with a five-minute weekly log

## Paid kit

Full 9-tab system: [finance tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/finance-tracker/) · EUR 9 one-time · [Stripe checkout](https://buy.stripe.com/6oUeVe5KS6PO7Fc5FP5Ne0t?client_reference_id=beginner-guide)
