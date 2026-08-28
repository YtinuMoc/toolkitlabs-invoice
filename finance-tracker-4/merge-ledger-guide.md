# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [jnkxstudio Finance Tracker 4.0 (2,995 sales · 4.9★)](https://jnkxstudio.gumroad.com/l/Finance_Tracker_3).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 finance_tracker_4.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as jnkxstudio's connected income + expense + goals views.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility (run312)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run311)
- [late-payment-guide.md](late-payment-guide.md) — wilsonhoe/2gnj buyer channel (run310)
- [start-here.md](start-here.md) — kit setup

Full bundle: [Finance Tracker 4.0 landing](https://ytinumoc.github.io/toolkitlabs-invoice/finance-tracker-4/).
