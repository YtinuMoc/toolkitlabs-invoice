# Start here — Online Seller Profit & Fee Tracker

Clone of [ambrosetheshield xdjzq](https://ambrosetheshield.gumroad.com/l/xdjzq) (£14.85 Gumroad).

## 1. Run the free sample

```bash
python3 multi_platform_seller_tracker.py orders-sample.csv
```

The £25 Etsy mug row shows the ambrosetheshield promise: gross sale price ≠ money in your pocket after fees, postage, packaging, and materials.

## 2. Log your orders

Copy `orders-template.csv` and add one row per sale:

| Column | Example |
|--------|---------|
| `platform` | `etsy`, `ebay`, `vinted`, `depop`, `amazon_handmade`, `gumroad`, `own_site` |
| `sale_price` | 25.00 |
| `platform_fee` | leave blank to auto-calculate |
| `postage` | 3.50 |
| `packaging` | 1.20 |
| `cogs` | 8.00 |
| `time_minutes` | 75 (for hourly rate) |

## 3. Price new listings

```bash
python3 multi_platform_seller_tracker.py --price-profit 10 8 3 1 etsy
```

## 4. Full zip

EUR 9 one-time checkout on the landing page — same delivery shape as the Gumroad original.
See also: [pricing calculator guide](pricing-calculator-guide.md) for Vinted/eBay hourly-rate examples.
