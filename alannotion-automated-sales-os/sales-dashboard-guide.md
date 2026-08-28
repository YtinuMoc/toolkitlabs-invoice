# Sales dashboard guide

Clone of [goldenalien/206o](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o) buyer channel + [alannotion Automated Sales OS](https://alannotion.gumroad.com/l/automatedsalesos) ($15).

## Merge platform exports

```bash
python3 automated_sales_os.py gumroad.csv stripe.csv -o sales-ledger.csv
```

## What you get

- **Daily revenue** — last 7 days of net sales
- **Weekly trend** — rolling weekly totals
- **Monthly summary** — month-by-month net
- **Best-selling products** — ranked by net revenue

Same promise as Automated Sales OS: one live view of Gumroad + marketplace sales without manual spreadsheet updates.
