# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [BodegaLabs Emotional Finance Tracker (1,253 sales · 39 ratings · 5★)](https://bodegalaabs.gumroad.com/l/emotional-finance-tracker).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 emotional_finance_tracker.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as BodegaLabs' connected income, expense, savings goals, and spending-trigger views.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility (run352)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run351)
- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run350)
- [start-here.md](start-here.md) — kit setup

Full bundle: [Emotional Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/emotional-finance-tracker/).
