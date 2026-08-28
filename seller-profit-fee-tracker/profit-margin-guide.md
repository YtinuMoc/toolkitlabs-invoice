# Profit margin tracking — per-SKU and YTD (smadsby clone)

Clone of [SimpleBizDash Seller Profit & Fee Tracker ($14.99)](https://smadsby.gumroad.com/l/ejxcg). Buyer-channel shape: [faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo).

## The problem faisalmq names

Without a clear view of profit margins, you price SKUs on guesswork. Gumroad says a $12.99 template sold 40 times — but after Etsy listing fees, Pinterest ads, and Gumroad's $0.30 flat, **which product actually earns margin?**

[faisalmq/3cpo](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-3cpo) sells three outcomes a tracker should deliver:

1. **Automated summaries** — profit margins at a glance
2. **Tax preparedness** — expenses categorized before filing season
3. **Centralized data** — one log, not four platform dashboards

SimpleBizDash's **Profit Margin Tracking** tab is the same promise for Etsy, Gumroad, Shopify sellers.

## Free CLI preview

```bash
python3 seller_profit_fee_tracker.py sales-sample.csv expense-sample.csv
```

Look for `PROFIT MARGINS AT A GLANCE` in stdout:

```plaintext
=== PROFIT MARGINS AT A GLANCE (smadsby ejxcg / faisalmq/3cpo shape) ===
  Gross sales:         $114.42
  Platform fees:       $18.63
  Expenses:            $85.50
  Real profit:         $10.29
  Profit margin:       9.0%

  Per-SKU margin after platform fees (pricing decisions):
    Notion Budget Template        4 orders · gross $51.96 · fees 15.9% · net $43.70 · contrib 84.1%
    Etsy Art Bundle               3 orders · gross $25.50 · fees 22.3% · net $19.82 · contrib 77.7%
    ...
```

**Profit margin** = (gross − fees − expenses) ÷ gross. If margin drops, ads or low-fee SKUs are eating you — not just tax surprises.

## Why gross revenue lies

A bestseller on Gumroad can have **sub-10% real margin** after ads. Without per-SKU contribution margin after platform fees, you double down on the wrong listing.

## Pair with

- [platform-comparison-guide.md](platform-comparison-guide.md) — which marketplace pays after fees
- [monthly-summary-guide.md](monthly-summary-guide.md) — month-end rollup
- [expense-drag-guide.md](expense-drag-guide.md) — ad spend as % of gross
- [start-here.md](start-here.md) — full setup

Full workbook: [Seller Profit & Fee Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/seller-profit-fee-tracker/) — EUR 9 one-time.
