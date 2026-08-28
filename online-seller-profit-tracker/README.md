# Online Seller Profit & Fee Tracker

Shameless clone of [ambrosetheshield Online Seller Profit & Fee Tracker](https://ambrosetheshield.gumroad.com/l/xdjzq) (£14.85 on Gumroad).

Etsy, eBay, Vinted, Depop, Amazon Handmade, Gumroad, and your own site — one CSV log + Python CLI.

## Quick start

```bash
python3 multi_platform_seller_tracker.py orders-sample.csv
```

## Pricing calculator

```bash
# Target £8 profit on an Etsy order with £6 COGS, £3 postage, £1 packaging
python3 multi_platform_seller_tracker.py --price-profit 8 6 3 1 etsy

# Target 40% margin on Vinted
python3 multi_platform_seller_tracker.py --price-margin 40 6 3 1 vinted
```

## What's included

- Order log with auto platform fees (editable in CSV)
- Profit by platform and month
- Pricing calculator (target profit or target margin)
- Effective hourly rate per order
- Worst-order report — the single sale that lost you the most
