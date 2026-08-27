# Freelancer 1099-K gross vs taxable net (l_d/5284 shape)

Clone of [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os) + [l_d/5284](https://dev.to/l_d_985a85beff7511/tiktok-shop-taxes-2026-what-every-seller-needs-to-know-about-1099-k-sales-tax-deductions-5284) buyer channel: 1099-K panic → gross vs net → deductible fees → quarterly set-aside from **net**.

**Not tax advice.** Planning numbers only — confirm with a CPA.

## The January panic (freelancers who sell on platforms)

You freelance **and** sell templates/courses on Gumroad, Etsy, or Stripe. In January a **1099-K** arrives. The number looks huge — often much larger than what landed in your bank.

That is because the 1099-K reports **gross buyer payments**, not net payout. Report gross as income without deducting platform fees and you pay tax on money you never kept.

Client work (1099-NEC) has the same trap if you only look at deposits without logging deductible expenses.

## What the 1099-K actually shows

| Concept | What it means |
|---------|---------------|
| Gross payments | Total buyer payments processed through the platform |
| Not included | Gumroad/Stripe fees, refunds, chargebacks, ad spend |
| Your job | Subtract legitimate business expenses (IRC §162) → **taxable net profit** |

Income is taxable whether or not a 1099-K arrives. Many platforms still use **$20,000 + 200 transactions** before issuing the form — but quarterly estimates are owed on net profit either way.

## Deductible fees to track monthly

| Category | Examples |
|----------|----------|
| `platform_fee` | Gumroad cut, Stripe processing, Etsy fees |
| `fulfillment` | Print-on-demand, shipping labels |
| `creator_commission` | Affiliate payouts on your sales |
| `ad_spend` | Meta, Google, TikTok ads for your products |
| `refund_fee` | Chargeback admin, refund processing |

Log each fee the month it hits — not in April.

## Worked example (freelancer + Gumroad, Q1)

| Item | Amount |
|------|--------|
| Gross marketplace payments (1099-K style) | $23,100 |
| Platform fees | −$1,386 |
| Ad spend | −$320 |
| Refund fees | −$25 |
| Client income (1099-NEC, separate) | $2,500 |
| Software (deductible) | −$55 |
| **Taxable net profit** | **$23,814** |

Quarterly set-aside at 25% of **net**: **$5,954** — not 25% of gross deposits.

## How to use with this kit

1. Log gross marketplace sales as `income` / `marketplace_sales`
2. Log client invoices in `invoice-log.csv` (or as `client_invoice` rows)
3. Log every fee in its own expense category
4. Run `python3 freelance_finance_os.py --1099k 1099k-freelance-sample.csv`
5. Read **1099-K RECONCILIATION** — gross vs deductible fees vs taxable net
6. Transfer quarterly set-aside from **net**, not gross deposits

Sample file: [1099k-freelance-sample.csv](1099k-freelance-sample.csv)

Full four-tool bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) · EUR 9 one-time · same delivery shape as [By the Loop on Gumroad ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).
