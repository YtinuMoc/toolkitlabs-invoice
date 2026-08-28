# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [Tony David Notion Finance Tracker (52 ratings · 5★)](https://tonydavid.gumroad.com/l/rjwua).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 tonydavid_finance_tracker.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as Tony David's connected income + summary cards + budget tracking views.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility (run347)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run346)
- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run345)
- [start-here.md](start-here.md) — kit setup

Full bundle: [Tony David Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/tonydavid-finance-tracker/).
