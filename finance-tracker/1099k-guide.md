# 1099-K gross vs taxable net — creator & marketplace seller guide

Clone of [l_d's TikTok Shop Taxes 2026 guide](https://dev.to/l_d_985a85beff7511/tiktok-shop-taxes-2026-what-every-seller-needs-to-know-about-1099-k-sales-tax-deductions-5284) shape + Quillenhart qaduu transaction log tab.

**Not tax advice.** Planning numbers only — confirm with a CPA.

## The panic in January

Your 1099-K arrives. The number looks huge — often **much larger than what landed in your bank**.

That is because the 1099-K reports **gross buyer payments**, not net payout. Report that gross as income without deducting fees and you pay tax on money you never kept.

## What the 1099-K actually shows

| Box / concept | What it means |
|---------------|---------------|
| Gross payments | Total buyer payments processed through the platform |
| Not included | Platform referral fees, fulfillment, creator commissions, ad spend, refunds clawbacks |
| Your job | Subtract legitimate business expenses (IRC §162) to get **taxable net profit** |

Income is taxable whether or not a 1099-K arrives. Under current rules many sellers need **$20,000 + 200 transactions** before a form is issued — but you still owe quarterly estimates on net profit.

## Deductible fees to track monthly (marketplace sellers)

| Category | Examples |
|----------|----------|
| `platform_fee` | TikTok referral fee, Gumroad/Stripe processing, Etsy fees |
| `fulfillment` | FBT, shipping labels, 3PL |
| `creator_commission` | Affiliate/creator payouts on your sales |
| `ad_spend` | TikTok Ads, Meta, Google |
| `refund_fee` | Refund admin fees, chargeback costs |

Log each fee as an **expense** row the month it hits — not in April.

## Worked example (TikTok Shop seller, Q1)

| Item | Amount |
|------|--------|
| Gross buyer payments (1099-K style) | $48,000 |
| Platform referral fees | −$2,880 |
| Fulfillment (FBT) | −$4,200 |
| Creator commissions | −$6,720 |
| Ad spend | −$3,600 |
| **Taxable net profit** | **$30,600** |

Quarterly set-aside at 25% of net: **$7,650** — not 25% of $48,000.

## How to use with this kit

1. Log gross sales as `income` / `marketplace_sales`
2. Log every fee in its own expense category (see table above)
3. Run `python3 monthly_dashboard.py your-log.csv`
4. Read **1099-K RECONCILIATION** — gross vs deductible fees vs taxable net
5. Transfer quarterly set-aside from **net**, not gross deposits

Sample file: [1099k-sample.csv](1099k-sample.csv)

Full kit: [Quillenhart qaduu clone ($15 → EUR 9)](https://ytinumoc.github.io/toolkitlabs-invoice/finance-tracker/)
