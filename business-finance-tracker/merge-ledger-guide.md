# Merge Gumroad, Stripe, and PayPal CSVs

Buyer-channel shape: [goldenalien/206o merge_payment_ledger](https://dev.to/goldenalien/mergepaymentledger-merge-gumroad-stripe-and-paypal-csvs-into-a-unified-ledger-for-easy-206o).

Clone target: [fayedinua Finance OS Business Finance Tracker ($39+ · 2 ratings · 5★ · 952 seller reviews)](https://fayedinua.gumroad.com/l/business-finance-tracker-notion).

## Export paths

| Platform | Export |
|----------|--------|
| Gumroad | Sales → Export CSV |
| Stripe | Balance → Export |
| PayPal | Activity download |

## Merge

```bash
python3 business_finance_tracker.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

Output columns: `date`, `platform`, `transaction_id`, `description`, `amount`, `fee`, `net`, `buyer`.

Import `ledger-merged.csv` into your income log — same workflow as fayedinua's Finance OS income, expenses, VAT, invoices, and cash flow dashboard.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility (run377)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run376)
- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run375)
- [start-here.md](start-here.md) — kit setup

Full bundle: [Business Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/business-finance-tracker/).
