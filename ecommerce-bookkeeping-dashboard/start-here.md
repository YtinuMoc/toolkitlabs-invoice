# Start here — Automated E-Commerce Bookkeeping Dashboard

Clone of [vivre05 xytjqh](https://vivre05.gumroad.com/l/xytjqh) ($29+ Gumroad).

## 1. Run the free sample

```bash
python3 ecommerce_bookkeeping_dashboard.py transactions-sample.csv
```

The dashboard shows total revenue, costs, take-home profit, and a tax set-aside — the same promise as vivre05's automated Excel dashboard.

## 2. Log your transactions

Copy `transactions-template.csv` and add one row per sale or expense:

| Column | Example |
|--------|---------|
| `type` | `sale` or `expense` |
| `category` | `product`, `materials`, `shipping`, `ads`, `software` |
| `amount` | 25.00 |
| `platform` | `etsy`, `gumroad`, `amazon`, `vinted`, `other` |

## 3. Adjust your tax rate

```bash
python3 ecommerce_bookkeeping_dashboard.py my-transactions.csv --tax-rate 30
```

## 4. Full zip

EUR 9 one-time checkout on the landing page — same delivery shape as the Gumroad original.
