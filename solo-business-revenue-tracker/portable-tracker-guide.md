# Portable solo business revenue tracker — single source of truth

Clone of [faisalmq/3gcp](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3gcp) buyer channel + [amyragland's Solo Business Revenue & Expense Tracker ($10)](https://amyragland.gumroad.com/l/tckuq).

faisalmq ships a Google Sheets tracker: income logging, expense categorization, tax estimation, net profit view — update from phone or desktop. Our clone uses plain CSV + Python — same delivery shape, no Google account, syncs via any cloud folder.

## Why "winging it" costs money

Mental math and scattered invoices lead to missed deductions, overspent SaaS, and April surprises. A single portable log fixes that.

## Four metrics that matter

| Metric | What it answers |
|--------|-----------------|
| Income tracking | How much did clients actually pay? |
| Expense categorization | Where is the money going? |
| Tax estimation | What to set aside before spending? |
| Net profit view | What's actually yours to keep? |

## Five-minute setup

1. Copy `revenue-template.csv` and `expenses-template.csv` from the [landing page](https://ytinumoc.github.io/toolkitlabs-invoice/solo-business-revenue-tracker/).
2. Drop them in Dropbox, iCloud, or any synced folder.
3. Log client payments and expenses as they happen — phone or desktop.
4. Run the portable preview:

```bash
python3 solo_business_revenue_tracker.py --portable revenue-sample.csv expenses-sample.csv
```

## Portability checklist

- **Plain-text CSV** — opens in Excel, Numbers, Google Sheets, or any editor
- **No subscription** — one-time kit, yours forever
- **Offline CLI** — preview numbers without opening a browser
- **Expandable** — duplicate template rows as transaction volume grows

## Sample output

```
=== PORTABLE SOLO BUSINESS TRACKER (faisalmq/3gcp shape) ===
  Income tracking:     $12,150.00 collected (8 revenue rows)
  Expense categories:  $380.49 (6 expense rows)
    Tax estimation:      $2,942.38 set aside (25% of net)
    Net profit view:     $11,769.51 → take-home $8,827.13
```

## Paid kit

[Solo Business Revenue Tracker — EUR 9](https://buy.stripe.com/14A14o1uCfmkbVsecl5Ne0O) — monthly/quarterly P&L, client revenue %, expense categories. Same architecture as [amyragland on Gumroad ($10)](https://amyragland.gumroad.com/l/tckuq).
