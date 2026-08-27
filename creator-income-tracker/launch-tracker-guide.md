# Launch Tracker (PattyBun rauxja tab 5)

Clone of [PattyBun's Launch Tracker tab](https://pattybun.gumroad.com/l/rauxja) ($14.99): first **7-day** and **30-day** net revenue per product launch, promo notes, and a simple outcome rating.

## How to tag launches

Add `launch` anywhere in the `notes` column on sales from a product's launch window:

```csv
date,platform,product,gross,notes
2026-03-01,gumroad,Notion Planner,19.00,launch Product Hunt day
2026-03-02,gumroad,Notion Planner,19.00,launch
2026-03-04,etsy,Notion Planner,22.00,launch
```

Run:

```bash
python3 creator_dashboard.py sample-revenue.csv
```

## Output shape

```
=== LAUNCH TRACKER (PattyBun tab 5 — 7-day + 30-day windows) ===
  Finance Tracker:
    launch start: 2026-01-05  promo: launch week
    7-day:   3 sales  gross $   87.00  net $   75.80  outcome strong
    30-day:  5 sales  gross $  120.00  net $  105.20
```

Outcome ratings (clone of PattyBun's outcome field):

| 7-day net | Rating |
|-----------|--------|
| ≥ $200 | strong |
| ≥ $50 | ok |
| > $0 | weak |
| $0 | no traction |

Adjust thresholds in `creator_dashboard.py` if your niche differs.
