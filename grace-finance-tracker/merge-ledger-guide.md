# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [chrisnotion Finance OS Dashboard (30,427 sales · 4.9★)](https://chrisnotion.gumroad.com/l/fcufra).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 finance_os_dashboard.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as chrisnotion's connected income + expense + budget views.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility (run317)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run316)
- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run315)
- [start-here.md](start-here.md) — kit setup

Full bundle: [Finance OS Dashboard landing](https://ytinumoc.github.io/toolkitlabs-invoice/finance-os-dashboard/).
