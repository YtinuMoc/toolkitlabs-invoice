# Platform Summary (PattyBun rauxja tab 3)

Clone of [PattyBun's Platform Summary tab](https://pattybun.gumroad.com/l/rauxja) ($14.99): side-by-side gross, fees, net, and effective fee rate for Gumroad, Etsy, Shopify, and Payhip — plus monthly net rollups.

## One revenue log, four storefronts

```csv
date,platform,product,gross,notes
2026-01-05,gumroad,Finance Tracker,29.00,
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
=== PLATFORM SUMMARY (PattyBun tab 3) ===
  gumroad     gross $   87.00  fees $  11.20  net $   75.80  eff fee 12.9%
  etsy        gross $   37.00  fees $   3.53  net $   33.47  eff fee  9.5%
  payhip      gross $   12.00  fees $   0.60  net $   11.40  eff fee  5.0%
  shopify     gross $   49.00  fees $   1.72  net $   47.28  eff fee  3.5%

  Highest fee drag: gumroad (12.9% of gross)
  Lowest fee drag:  shopify (3.5% of gross)

  Monthly net by platform:
    2026-01: etsy $33.47, gumroad $75.80, payhip $11.40, shopify $47.28
```

## Default fee models

| Platform | Model |
|----------|-------|
| gumroad | 10% + $0.50 flat |
| etsy | 6.5% + 3% payment processing |
| shopify | 2.9% + $0.30 |
| payhip | 5% |
| other | manual `fee=12.34` in notes |

Effective fee rate = fees ÷ gross × 100. The flat Gumroad $0.50 hurts more on low-ticket SKUs — that's why net-by-platform beats dashboard gross.

Override any row with `fee=12.34` in notes when your storefront tier differs.
