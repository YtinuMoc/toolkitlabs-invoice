# Pricing calculator — Vinted, eBay & Etsy

Clone of [ambrosetheshield's pricing tab](https://ambrosetheshield.gumroad.com/l/xdjzq) (£14.85 Gumroad).

ambrosetheshield's promise: you tell it your costs and the profit you want — it tells you what to charge. Same math in the CLI.

## Target profit → minimum list price

```bash
python3 multi_platform_seller_tracker.py --price-profit 10 8 3 1 vinted
```

Example: £10 target profit, £8 COGS, £3 postage, £1 packaging on Vinted.

```plaintext
=== PRICING CALCULATOR (target profit £10.00) ===
  Platform: vinted
  Charge at least: £23.89
```

Vinted fee model in the CLI: 5% + £0.70 buyer protection per sale.

## Target margin → minimum list price

```bash
python3 multi_platform_seller_tracker.py --price-margin 40 6 4 1 ebay
```

40% margin after all costs on eBay (12.9% + £0.30 fee model).

## Effective hourly rate (the number handmade sellers need)

Log `time_minutes` per order. The dashboard prints average and lowest hourly rate:

```bash
python3 multi_platform_seller_tracker.py orders-sample.csv
```

```plaintext
=== EFFECTIVE HOURLY RATE ===
  Average across timed orders: £12.40/hr
  Lowest: Low-margin sticker pack at £0.24/hr
```

A £25 Vinted sale that took 90 minutes and netted £4.12 is **£2.75/hr** — below minimum wage. The pricing calculator fixes the list price before you list.

## Reality-check prices you already use

1. Run `--price-profit` with your real COGS + postage + packaging.
2. Compare the output to your current list price.
3. If current price < calculated minimum, you are subsidizing buyers.

Full order log + 400 rows: EUR 9 zip on the [landing page](https://ytinumoc.github.io/toolkitlabs-invoice/online-seller-profit-tracker/).
