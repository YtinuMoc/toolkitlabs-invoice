# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [organizeddashboard Finance Tracker Pro ($12 · 15 ratings · 5★)](https://organizeddashboard.gumroad.com/l/cyezap).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 finance_tracker_pro.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as Finance Tracker Pro's accounts, income, expenses, subscriptions, and savings goals dashboard.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility (run387)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run386)
- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run385)
- [start-here.md](start-here.md) — kit setup

Full bundle: [Finance Tracker Pro landing](https://ytinumoc.github.io/toolkitlabs-invoice/finance-tracker-pro/).
