# Start here — Side Hustle Income + Expense Tracker

Clone of PattyBun tdmuz ($9.99 Gumroad). Track 1–8 income streams in one place.

## Step 1 — Name your hustles

Edit the `hustle` column in `income-log-template.csv`. Examples: `etsy_shop`, `fiverr_gigs`, `doordash`, `kdp`.

Up to 8 simultaneous streams — same shape as PattyBun's 8 hustle tabs.

## Step 2 — Log income

```csv
date,hustle,source,amount,category,notes
2026-01-05,etsy_shop,Etsy payout,142.00,product_sales,
```

## Step 3 — Log expenses

```csv
date,hustle,category,amount,vendor,notes
2026-01-06,etsy_shop,supplies,34.20,Etsy listing fees,
```

Use `shared` for tools that span all hustles.

## Step 4 — Run dashboard

```bash
python3 side_hustle_dashboard.py income-sample.csv expense-sample.csv
```

Check **Best performer** on the Dashboard — that's which hustle is actually worth your time.

See [hustle-settings.md](hustle-settings.md) for tax defaults and [faq.md](faq.md).
