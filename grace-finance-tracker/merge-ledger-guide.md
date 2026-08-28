# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [gracedigitalsco Finance Tracker (3,000 sales · 91 ratings · 5.0★)](https://gracedigitalsco.gumroad.com/l/FinanceTracker).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 grace_finance_tracker.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as gracedigitalsco's connected income + expense + savings goals views.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility (run322)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run321)
- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run320)
- [start-here.md](start-here.md) — kit setup

Full bundle: [Grace Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/grace-finance-tracker/).
