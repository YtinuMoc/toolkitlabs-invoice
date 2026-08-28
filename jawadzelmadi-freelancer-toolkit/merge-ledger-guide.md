# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [jawadzelmadi Ultimate Freelancer Toolkit (39 sales · 5 ratings · 5.0★ · $9+)](https://jawadzelmadi.gumroad.com/l/FreelancerToolkit).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 jawadzelmadi_freelancer_toolkit.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as Ultimate Freelancer Toolkit's clients, projects, and income/expense tracker.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility (run392)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run391)
- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run390)
- [start-here.md](start-here.md) — kit setup

Full bundle: [Ultimate Freelancer Toolkit landing](https://ytinumoc.github.io/toolkitlabs-invoice/jawadzelmadi-freelancer-toolkit/).
