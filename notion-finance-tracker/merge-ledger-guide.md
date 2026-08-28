# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [Rosidssoy Notion Finance Tracker ($5+ · 190 ratings · 13,696 sales)](https://rosidssoy.gumroad.com/l/financetracker).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 notion_finance_tracker.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as Rosidssoy's connected income + expense + goals views.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility (run307)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run306)
- [tax-quarter-guide.md](tax-quarter-guide.md) — wilsonhoe/4lhd quarterly set-aside (run305)
- [start-here.md](start-here.md) — kit setup

Full bundle: [Notion Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/notion-finance-tracker/).
