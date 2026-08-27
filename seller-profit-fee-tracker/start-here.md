# Start here — Seller Profit & Fee Tracker

Clone of [smadsby ejxcg](https://smadsby.gumroad.com/l/ejxcg) ($14.99 · SimpleBizDash).

## 1. Log sales

Add every sale to `sales-log-template.csv` — date, product, platform, gross. Fees calculate automatically.

## 2. Log expenses

Ads, software, refunds, supplies in `expense-log-template.csv`.

## 3. Run the CLI

```bash
python3 seller_profit_fee_tracker.py sales-log-template.csv expense-log-template.csv
```

You get: seller dashboard, platform performance comparison, monthly summary, lowest-net order flag.

See `sales-sample.csv` for a worked example across Gumroad, Etsy, Shopify, eBay, and Amazon.
