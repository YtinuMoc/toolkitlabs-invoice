# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [heyismail Finance OS Pro ($29+ · 15,254 sales)](https://heyismail.gumroad.com/l/TheUltimateFinanceTracker).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 finance_os_tracker.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your Finance OS income log — same workflow as heyismail's all-in-one command center.

## Pair with

- [finance-os-guide.md](finance-os-guide.md) — full command center setup
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day buffer
- [start-here.md](start-here.md) — income, expense, budget, subscription modules

Full bundle: [Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/finance-os-tracker/).
