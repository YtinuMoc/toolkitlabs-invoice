# Freelancer Finance Pack

Shameless clone of [Sam Arora — Freelancer Finance Pack](https://saksham82.gumroad.com/l/cueko) ($9 on Gumroad).

Seven-sheet Excel promise as CSV + Python CLI: invoices, expenses, US quarterly tax, India advance tax, profit dashboard, and multi-platform payment ledger merge.

## Quick start

```bash
python3 freelancer_finance_pack.py invoices-sample.csv expenses-sample.csv 120
```

Merge Gumroad + Stripe + PayPal exports:

```bash
python3 freelancer_finance_pack.py --merge gumroad.csv stripe.csv paypal.csv -o ledger-merged.csv
```

## Files

- `invoices-template.csv` / `invoices-sample.csv`
- `expenses-template.csv` / `expenses-sample.csv`
- `freelancer_finance_pack.py` — dashboard + ledger merge CLI
- `start-here.md` / `faq.md` / `merge-ledger-guide.md`

EUR 9 one-time via Stripe on the [landing page](https://ytinumoc.github.io/toolkitlabs-invoice/freelancer-finance-pack/).
