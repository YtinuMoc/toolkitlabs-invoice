# Seller Profit & Fee Tracker

Shameless clone of [SimpleBizDash / smadsby on Gumroad ($14.99)](https://smadsby.gumroad.com/l/ejxcg).

Sales tracker, platform fee calculator, expense log, profit margin, monthly summary, seller dashboard, platform performance comparison — Etsy, Gumroad, Shopify, eBay, Amazon.

## Files

- `sales-log-template.csv` — one row per sale (gross; fees auto-calc)
- `expense-log-template.csv` — ads, software, supplies
- `seller_profit_fee_tracker.py` — dashboard + platform comparison CLI

## Quick start

```bash
python3 seller_profit_fee_tracker.py sales-sample.csv expense-sample.csv
```

EUR 9 checkout on landing — instant zip after Stripe.
