# Instant download trust (Quillenhart qaduu clone)

Clone of [Quillenhart Co. Finance Tracker on Gumroad](https://quillenhart.gumroad.com/l/qaduu) delivery promise:

> **Instant digital download.** One-time purchase, yours to reuse every year.

> **Thoughtfully made, ready to use.** This isn't a basic budget template — it's a complete, all-inclusive finance system built for the small business owner who doesn't want to pay for bookkeeping software.

## What you get after checkout

| Step | Gumroad qaduu | This kit (EUR 9 Stripe) |
|------|---------------|-------------------------|
| Pay | Gumroad checkout | Stripe checkout |
| Delivery | Instant `.xlsx` download | Instant zip (CSV + Python + guides) |
| Recurring fee | None | None |
| Reuse next year | Same file, new rows | Same zip, new CSV rows |
| Account required | Gumroad library | Email receipt + zip link |

## Why one-time beats subscription

- **No $30/mo QuickBooks creep** — Quillenhart's whole pitch is replacing bookkeeping SaaS with one file.
- **Yours forever** — not a template locked inside Notion or a vendor dashboard.
- **Offline** — open Excel or import CSV on a flight; no sync dependency.
- **Predictable cost** — $15 once on Gumroad · EUR 9 on our clone.

## Free preview (no checkout)

Run the dashboard on sample data:

```bash
python3 monthly_dashboard.py sample-transactions.csv
```

Look for the `INSTANT DOWNLOAD TRUST` block in stdout.

## Stack upsell (Quillenhart cross-sell)

Quillenhart also sells a separate [**Small Business Command Center**](https://quillenhart.gumroad.com/l/acrum) ($29) — clients, invoices, and business dashboard in one calm spreadsheet. See `command-center-crosssell-guide.md`.
