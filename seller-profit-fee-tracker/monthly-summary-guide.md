# Monthly summary (smadsby ejxcg shape)

[SimpleBizDash on Gumroad](https://smadsby.gumroad.com/l/ejxcg) ships a **Monthly Summary** tab — gross, fees, expenses, and profit rolled up by calendar month. Tax season and quarterly estimates need month-level totals, not a single YTD number.

## What to log

**Sales CSV** — one row per order:

```csv
date,product,platform,gross
2026-01-05,Template Pack,gumroad,29.00
2026-01-18,Digital Planner,etsy,18.50
```

**Expense CSV** — ads, software, supplies:

```csv
date,category,amount,vendor
2026-01-03,ads,25.00,Pinterest
```

## CLI

```bash
python3 seller_profit_fee_tracker.py sales-sample.csv expense-sample.csv
```

Look for the `=== MONTHLY SUMMARY ===` block — last six months with gross, fees, expenses, and profit per month.

## Why monthly beats dashboard gross

- Gumroad and Etsy dashboards show **current-month gross** — not fees or ads logged elsewhere.
- A bad January (high ad spend) hides inside a good February gross if you only check YTD.
- Month-over-month profit tells you when to pause ads or shift SKUs to a lower-fee platform.

Full workbook: [EUR 9 checkout](https://buy.stripe.com/9B68wQc9g7TS1gOgkt5Ne0G?client_reference_id=monthly-summary-guide).
