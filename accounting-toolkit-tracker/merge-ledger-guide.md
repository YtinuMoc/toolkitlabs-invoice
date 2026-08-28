# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [theaccountantguy Ultimate Accounting Toolkit (92 sales)](https://theaccountantguy.gumroad.com/l/notionaccountingtoolkit).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 accounting_toolkit.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as theaccountantguy's connected income + expense + debt + savings views.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility (run337)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run336)
- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run335)
- [start-here.md](start-here.md) — kit setup

Full bundle: [Accounting Toolkit Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/accounting-toolkit-tracker/).
