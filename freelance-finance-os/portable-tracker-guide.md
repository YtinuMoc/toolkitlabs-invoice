# Portable freelance finance tracker — single source of truth

Clone of [faisalmq/3gcp](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3gcp) buyer channel + [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).

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

1. Copy `invoice-log-template.csv` and `expense-log-template.csv` from the [landing page](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/).
2. Drop them in Dropbox, iCloud, or any synced folder.
3. Log client payments and expenses as they happen — phone or desktop.
4. Run the portable preview:

```bash
python3 freelance_finance_os.py --portable invoice-log-sample.csv expense-log-sample.csv
```

## Portability checklist

- **Plain-text CSV** — opens in Excel, Numbers, Google Sheets, or any editor
- **No subscription** — one-time kit, yours forever
- **Offline CLI** — preview numbers without opening a browser
- **Expandable** — duplicate template rows as transaction volume grows

## Sample output

```
=== PORTABLE FREELANCE FINANCE TRACKER (faisalmq/3gcp shape) ===
  Vessel: plain CSV logs — sync via Dropbox/iCloud/Git; no Google account.
  Four metrics that matter:
    Income tracking:     $3,550.00 collected (6 invoice rows)
    Expense categories:  $213.99 (8 expense rows)
    Tax estimation:      $834.00 set aside (25% of net)
    Net profit view:     $3,336.01 → take-home $2,502.01
```

## Paid kit

[Freelance Finance OS — EUR 9](https://buy.stripe.com/4gM3cw0qy8XWgbI2tD5Ne0E) — four tools in one bundle (invoice tracker, tax buffer, rate calculator, quarterly estimator). Same architecture as [By the Loop on Gumroad ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).
