# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [matthewnotion Finance Tracker (58 sales)](https://matthewnotion.gumroad.com/l/financetracker).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 matthew_finance_tracker.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as matthewnotion's connected income + expense + savings goals views.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility (run332)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run331)
- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run330)
- [start-here.md](start-here.md) — kit setup

Full bundle: [Matthew Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/matthew-finance-tracker/).
