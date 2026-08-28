# Product profitability — which Etsy listing actually earns (sundayscope clone)

Clone of [sundayscope Profit After Fees ($27 on Gumroad)](https://sundayscope.gumroad.com/l/jmqyil) **Product Profitability** tab.

Buyer-channel shape: [faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo) — bestseller on dashboard ≠ highest margin after Etsy fee stack.

## The problem

Etsy ranks listings by orders and revenue. Your **Wall Art Bundle** might outsell your **Wedding Invite Set** — but after listing fees, transaction fees, processing, and offsite ads, the ranking flips.

Sunday Current's workbook ranks products by **net after fees**, not gross.

## Free CLI preview

```bash
python3 profit_after_fees_tracker.py sales-sample.csv expense-sample.csv
```

Look for `=== PRODUCT PROFITABILITY (sundayscope tab) ===`:

```plaintext
  #1 Wedding Invite Set            units   1  gross $  55.00  net $  42.73  margin  77.7%
  #2 Custom Pet Portrait           units   1  gross $  45.00  net $  33.52  margin  74.5%
  ...
  #8 Sticker Pack                  units   2  gross $   9.99  net $   8.39  margin  84.0%
```

**Margin** = net after Etsy fees ÷ gross. Use this to decide which listings to scale ads on — not ROAS alone.

## Sales CSV shape

```csv
date,product,gross,quantity,offsite_ad,high_volume_shop
2026-01-05,Printable Budget Planner,24.99,1,yes,no
```

Full workbook: [EUR 9 checkout](https://buy.stripe.com/cNicN68X45LK8Jgd8h5Ne0H?client_reference_id=product-profitability-guide-run240).
