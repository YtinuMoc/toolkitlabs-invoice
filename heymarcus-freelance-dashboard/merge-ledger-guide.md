# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [heymarcus All-in-One Freelance Dashboard (257 sales · 11 ratings · 4.9★ · $19+)](https://heymarcus.gumroad.com/l/bpqsi).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 heymarcus_freelance_dashboard.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as heymarcus's connected account balances, income, expenses, budgets, subscriptions, and goals.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility (run362)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run361)
- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run360)
- [start-here.md](start-here.md) — kit setup

Full bundle: [Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/heymarcus-freelance-dashboard/).
