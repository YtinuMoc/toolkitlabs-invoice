# Etsy quarterly tax set-aside — from NET profit, not gross deposits

Clone of [sundayscope Profit After Fees ($27 on Gumroad)](https://sundayscope.gumroad.com/l/jmqyil) **Tax Set-Aside Estimator** tab.

Buyer-channel shape: [l_d/5284 marketplace 1099-K guide](https://dev.to/l_d_985a85beff7511/tiktok-shop-taxes-2026-what-every-seller-needs-to-know-about-1099-k-sales-tax-deductions-5284) — gross panic → fee deductions → quarterly set-aside from **net** → paid workbook upsell.

## The mistake Etsy sellers make

Etsy deposits land in your bank. You spend from the full amount. In January the 1099-K shows **gross buyer payments** — much larger than what you kept after listing fees, transaction fees, payment processing, Offsite Ads, and refunds.

Set aside 25% of **gross deposits** and you over-save (or under-save if you forgot fees). Set aside nothing and April hurts.

## What to track monthly

| Category | Examples |
|----------|----------|
| `listing_fee` | $0.20 per listing |
| `transaction_fee` | 6.5% of order total |
| `payment_processing` | 3% + $0.25 |
| `offsite_ads` | 12–15% on attributed sales |
| `materials` | Supplies, packaging |
| `ad_spend` | Etsy Ads daily budget |

## Worked example (Q1 Etsy shop)

| Item | Amount |
|------|--------|
| Gross sales (1099-K style) | $8,420 |
| Etsy fees | −$1,264 |
| Materials + shipping supplies | −$1,890 |
| Etsy Ads | −$310 |
| **Taxable net profit** | **$4,956** |

Quarterly set-aside at 28% of **net**: **$1,388** — not 28% of $8,420.

## CLI workflow

```bash
python3 profit_after_fees_tracker.py sales-sample.csv expense-sample.csv
```

Look for the `TAX SET-ASIDE ESTIMATOR` block in output. Adjust `DEFAULT_TAX_SET_ASIDE_PCT` in the script to match your tax professional's planning rate.

## Habit

Transfer the set-aside amount to a **tax-only savings account** when the Etsy payout lands — same day, not in April.

Full kit: [Profit After Fees tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/profit-after-fees-tracker/) · EUR 9 one-time.
