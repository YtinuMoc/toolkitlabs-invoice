# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [EasyBlocks Notion Finance Tracker (11 ratings · 5★ · $39)](https://easyblocks.gumroad.com/l/notion-finance-tracker).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 easyblocks_finance_tracker.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as EasyBlocks' accounts, categories, income, expenses, transfers, and recurring payments tracker.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility (run402)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run401)
- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run400)
- [start-here.md](start-here.md) — full income + expense setup

Full bundle: [Notion Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/easyblocks-finance-tracker/).
