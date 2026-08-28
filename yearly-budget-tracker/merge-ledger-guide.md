# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [mariesells Yearly Budget Tracker (6 ratings · 5★ · $5.99+)](https://mariesells.gumroad.com/l/yearly-budget-tracker).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 yearly_budget_tracker.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as mariesells's yearly overview, monthly breakdowns, income/expenses, debt tracker, and savings goals.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility (run372)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run371)
- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run370)
- [start-here.md](start-here.md) — kit setup

Full bundle: [Yearly Budget Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/yearly-budget-tracker/).
