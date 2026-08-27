# Start here — Seller Profit & Content Tracker

Clone of [AnahitDigitalStudio nxqiai](https://anahitstudio.gumroad.com/l/nxqiai) ($14.99).

## 1. Product catalog

List every SKU in `product-catalog-template.csv` — name, platform, list price.

## 2. Log sales

One row per sale in `sales-log-template.csv`. Platform fees auto-calculate (Gumroad, Etsy, Shopify).

## 3. Log expenses

Ads, software, supplies in `expense-log-template.csv`.

## 4. Track content

Pinterest pins and social posts in `content-planner-template.csv` — clicks, conversions, attributed revenue.

## 5. UTM campaigns

Campaign links in `utm-campaigns-template.csv` — match `utm_source` / `utm_medium` to GA4.

## 6. Launches

Product launch outcomes in `launch-planner-template.csv` — 7-day and 30-day revenue.

## Run the CLI

```bash
python3 seller_dashboard.py product-catalog-template.csv sales-log-template.csv expense-log-template.csv content-planner-template.csv utm-campaigns-template.csv launch-planner-template.csv
```

See `sales-sample.csv` and siblings for worked examples.
