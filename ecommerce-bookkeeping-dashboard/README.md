# Automated E-Commerce Bookkeeping Dashboard

Shameless clone of [vivre05 Automated E-Commerce Bookkeeping Dashboard](https://vivre05.gumroad.com/l/xytjqh) ($29+ on Gumroad).

Transaction log + automated dashboard + tax set-aside estimator for Etsy, Gumroad, Amazon, and other e-commerce sellers.

## Quick start

```bash
python3 ecommerce_bookkeeping_dashboard.py transactions-sample.csv
```

## Custom tax rate

```bash
python3 ecommerce_bookkeeping_dashboard.py transactions-sample.csv --tax-rate 30
```

## What's included

- Transaction log — sales and expenses in one CSV
- Automated dashboard — revenue, costs, profit, margin
- Tax set-aside estimator — customizable rate (default 28%)
- Platform summary — revenue and costs by channel
- Monthly rollup — see trends without QuickBooks
