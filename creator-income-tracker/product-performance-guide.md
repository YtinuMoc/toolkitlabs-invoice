# Product Performance (PattyBun rauxja tab 4)

Clone of [PattyBun's Product Performance tab](https://pattybun.gumroad.com/l/rauxja) ($14.99): units, gross, net, margin %, platforms, and last sale date per SKU — ranked by net revenue.

## One revenue log, every SKU

```csv
date,platform,product,gross,notes
2026-01-05,gumroad,Finance Tracker,29.00,launch week
2026-01-08,etsy,Digital Planner,18.50,
2026-01-12,payhip,Notion Template,12.00,
2026-01-15,shopify,Course Workbook,49.00,
```

Run:

```bash
python3 creator_dashboard.py sample-revenue.csv
```

## Output shape

```
=== PRODUCT PERFORMANCE (PattyBun tab 4) ===
  #1 Finance Tracker       units   2  gross $   58.00  net $   50.30  margin 86.7%  platforms [gumroad]  last 2026-01-20  (0d ago)
  #2 Course Workbook        units   1  gross $   49.00  net $   47.28  margin 96.5%  platforms [shopify]  last 2026-01-15  (5d ago)
  ...
```

Margin % = net ÷ gross × 100. Rank by net revenue — the dashboard's "best product" is only one line; tab 4 shows the full stack so you know which SKU to promote vs retire.

Override fees per row with `fee=12.34` in notes when your storefront tier differs.
