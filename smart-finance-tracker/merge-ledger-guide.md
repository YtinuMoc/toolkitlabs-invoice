# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [jahazielgpz Smart Finance ($8.99+ · 35 ratings · 4.9★)](https://jahazielgpz.gumroad.com/l/smartfinance2025).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 smart_finance_tracker.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as Smart Finance's accounts, income, expenses, subscriptions, and savings goals dashboard.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility (run382)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run381)
- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run380)
- [start-here.md](start-here.md) — kit setup

Full bundle: [Smart Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/smart-finance-tracker/).
