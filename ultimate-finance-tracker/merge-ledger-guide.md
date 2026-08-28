# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [simonotion Ultimate Finance Tracker ($47 · 109 ratings · 5.0★)](https://simonotion.gumroad.com/l/finance-tracker).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 ultimate_finance_tracker.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as simonotion's connected income + expense + subscription views.

## Pair with

- [complete-workbook-guide.md](complete-workbook-guide.md) — hemantdev/1iae six-view workbook
- [beginner-guide.md](beginner-guide.md) — faisalmq/2fj6 no-formulas shape
- [guesswork-guide.md](guesswork-guide.md) — faisalmq/54h7 guesswork → clarity
- [start-here.md](start-here.md) — kit setup

Full bundle: [Ultimate Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/ultimate-finance-tracker/).
